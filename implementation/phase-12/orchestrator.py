"""Phase 12 MVP — the reference orchestrator.

Status: PROPOSED (implementation-equivalent non-approved status).

The orchestrator coordinates. It detects that a gate applies, creates the governed request,
records the outcome by reference, and moves the run between states the approved table allows.

It does none of the following, and each is a raise rather than a convention: infer or
manufacture approval; act as reviewer, Decision Right holder or signatory; accept risk;
canonicalise knowledge; choose a model or relax a routing constraint; substitute a model result
for a human gate; cross a scope silently; rewrite recorded history; retry a non-replayable
governed act automatically; or treat operational success as governance completion.

After the independent audit, one further rule runs through the whole file:

    **nothing the caller passes is taken on trust.**

Every act is checked against state the orchestrator itself recorded - the run's bound
definition, its declared tasks, its own routing requests, its own gate instances - rather than
against an object handed in at the time. A caller may still *construct* a plausible-looking
Decision Record or Routing Decision; it simply will not be found in the governed lineage, and
so it satisfies nothing.
"""

from typing import Dict, Optional, Tuple

from adapters import (
    DecisionAuthorityAdapter, ModelAdapter, ReviewerAdapter, RouterAdapter,
)
from domain import (
    ALLOWED_TRANSITIONS, Assignment, CONTINUING_GATE_OUTCOMES, DecisionRecord, DecisionRequest,
    EVIDENCE_CONTRACT, EvidenceError, ExecutionEventLog, GateInstance, GateInstanceRef,
    MissingEvidenceError,
    GateKind, GateOutcome, GateRequirement, GateRequirementRef, GovernanceError,
    HaltedRunError,
    GovernancePosture, HumanAuthorityRef, HumanInterventionRecord, HumanWorkCompletion,
    LineageError, ModelInvocationRequest, ModelResult, NEVER_AUTOMATICALLY_RETRYABLE,
    NON_COMPLETION_TERMINALS, POSTURE_PERMITS_COMPLETION, PrerequisiteEvidence, Ref,
    ReviewInstance, ReviewRequest, RetryClass, RoleRef, RouterOutcome, RouterRef,
    RoutingDecision, RoutingRequest, RoutingRequestRef, RunPhase, ScopeBinding,
    ScopeTransferAuthorisation, StateAccessError, TERMINAL_REACHABLE_FROM, TaskRef,
    TerminalOutcome, TransitionError, WaitReason, WorkItem, WorkItemRef, WorkflowDefinition,
    WorkflowRun, WorkflowRunRef, require,
)

#: Phases a run may not leave through an ordinary stage API. Leaving them is a governed act,
#: not a side effect of asking for the next piece of work - the audit found that a run left
#: BLOCKED and ESCALATED by `NO_APPLICABLE_DECISION_RIGHT` would happily activate another
#: stage, which is continuation without the authority that was found to be missing.
HALTED_PHASES = frozenset({RunPhase.BLOCKED, RunPhase.ESCALATED})


class Orchestrator:
    """A coordination control plane. It holds no authority of its own."""

    def __init__(self, router: RouterAdapter, reviewers: ReviewerAdapter,
                 decisions: DecisionAuthorityAdapter, model: ModelAdapter,
                 log: Optional[ExecutionEventLog] = None, mechanisms=None):
        self.router = router
        self.reviewers = reviewers
        self.decisions = decisions
        self.model = model
        self.mechanisms = mechanisms
        self.log = log if log is not None else ExecutionEventLog()
        self._tokens: Dict[int, object] = {}
        self._serial = 0

    # ---------------------------------------------------------------- token and state

    def _token(self, run: WorkflowRun) -> object:
        token = self._tokens.get(id(run))
        if token is None:
            raise StateAccessError("%s was not created by this orchestrator" % run.ref)
        return token

    def _state(self, run: WorkflowRun):
        return run._state(self._token(run))

    def _store(self, run: WorkflowRun, name: str):
        return run._store(self._token(run), name)

    def _next(self, prefix: str) -> str:
        self._serial += 1
        return "%s-%d" % (prefix, self._serial)

    def _require_progressible(self, run: WorkflowRun, act: str) -> None:
        """The one guard every ordinary API calls before it changes anything.

        A run that is terminal, BLOCKED, ESCALATED, or carrying AUTHORITY_ABSENT does not
        progress and does not append governed history. `unblock()` is the only way back, and it
        is a governed act in its own right. Calling `self._state` also proves the run belongs
        to this orchestrator, so the guard doubles as the ownership check every API needs."""
        state = self._state(run)
        if state.terminal is not None:
            raise HaltedRunError("%s is terminal as %s; %s is not available"
                                 % (run.ref, state.terminal.value, act))
        if state.phase in HALTED_PHASES or state.posture is GovernancePosture.AUTHORITY_ABSENT:
            raise HaltedRunError(
                "%s is %s / %s; %s requires governed unblock/reconciliation first"
                % (run.ref, state.phase.value, state.posture.value, act))

    # ---------------------------------------------------------------- state transitions

    def _transition(self, run: WorkflowRun, phase: RunPhase, *, detail: str = "",
                    wait_reason: Optional[WaitReason] = None,
                    wait_subject: Optional[Ref] = None) -> WorkflowRun:
        """The only place Axis A moves. Validated against the approved table."""
        state = self._state(run)
        if state.terminal is not None:
            raise TransitionError("run %s is terminal as %s and cannot move again"
                                  % (run.ref, state.terminal.value))
        if phase not in ALLOWED_TRANSITIONS[state.phase]:
            raise TransitionError("%s -> %s is not an approved transition"
                                  % (state.phase.value, phase.value))
        if phase is RunPhase.WAITING and (wait_reason is None or wait_subject is None):
            # A wait with no named subject is a defect: it cannot be told from a stall.
            raise GovernanceError("a WAITING run must name its reason and its subject")
        state.phase = phase
        state.wait_reason = wait_reason if phase is RunPhase.WAITING else None
        state.wait_subject = wait_subject if phase is RunPhase.WAITING else None
        self.log.append(run.ref, "phase:%s" % phase.value, detail, wait_subject)
        return run

    def _ensure_phase(self, run: WorkflowRun, phase: RunPhase, **kwargs) -> WorkflowRun:
        """Move to `phase`, or stay there if the run is already in it.

        The approved table has no self-transitions, and a run already WAITING on the gate it
        just asked about has not moved."""
        state = self._state(run)
        if state.phase is phase:
            if phase is RunPhase.WAITING:
                state.wait_reason = kwargs.get("wait_reason", state.wait_reason)
                state.wait_subject = kwargs.get("wait_subject", state.wait_subject)
                self.log.append(run.ref, "wait:still", kwargs.get("detail", ""),
                                state.wait_subject)
            return run
        return self._transition(run, phase, **kwargs)

    def _set_posture(self, run: WorkflowRun, posture: GovernancePosture, detail: str = ""):
        self._state(run).posture = posture
        self.log.append(run.ref, "posture:%s" % posture.value, detail)

    # ---------------------------------------------------------------- run creation and scope

    def create_run(self, definition: WorkflowDefinition, run_ref: WorkflowRunRef,
                   scope: Optional[ScopeBinding] = None) -> WorkflowRun:
        """Create a run bound to a governed definition and to exactly one scope."""
        return self._create_run(definition, run_ref, scope)

    def _create_run(self, definition: WorkflowDefinition, run_ref: WorkflowRunRef,
                    scope: Optional[ScopeBinding] = None,
                    authorisation: Optional[ScopeTransferAuthorisation] = None
                    ) -> WorkflowRun:
        """The one place a run is created.

        A run's scope is the definition's, or a narrowing of it. The single exception is a
        crossing that a `ScopeTransferAuthorisation` already covers - checked by the caller
        against the source run - which is how an approved mechanism moves work to another
        scope without any run's binding ever being rewritten."""
        if not isinstance(definition, WorkflowDefinition):
            raise LineageError("a run is created from a governed Workflow Definition")
        binding = definition.scope if scope is None else scope
        if (binding is not definition.scope and not definition.scope.narrows_to(binding)
                and authorisation is None):
            raise GovernanceError("a run may narrow the definition's scope, never widen it")
        token = object()
        run = WorkflowRun(run_ref, definition, binding, token)
        self._tokens[id(run)] = token
        self.log.append(run.ref, "run:created",
                        "%s @ %s" % (definition.ref, definition.version), definition.ref)
        self.log.append(run.ref, "scope:bound", "%s %s %s"
                        % (binding.scope, sorted(binding.sensitivity), binding.residency),
                        binding.scope)
        self._transition(run, RunPhase.VALIDATING, detail="intake validation")
        self._transition(run, RunPhase.READY, detail="validated")
        return run

    def open_sub_run(self, parent: WorkflowRun, definition: WorkflowDefinition,
                     run_ref: WorkflowRunRef, scope: ScopeBinding) -> WorkflowRun:
        """A sub-run may narrow what it sees. It may not widen it."""
        self._require_progressible(parent, "opening a sub-run")
        if not parent.scope.narrows_to(scope):
            raise GovernanceError(
                "a sub-run may narrow the parent scope, never widen it: %s is not within %s"
                % (sorted(scope.sensitivity), sorted(parent.scope.sensitivity)))
        child = self.create_run(definition, run_ref, scope)
        self.log.append(parent.ref, "sub_run:opened", str(child.ref), child.ref)
        return child

    def transfer_scope(self, run: WorkflowRun, definition: WorkflowDefinition,
                       run_ref: WorkflowRunRef, target: ScopeBinding,
                       authorisation: ScopeTransferAuthorisation) -> WorkflowRun:
        """Cross a scope boundary through an approved mechanism, into a NEW execution.

        One governed scope per execution: the source run's binding is never rewritten. The
        crossing happens only when every part of the authorisation is corroborated by the
        source run's own retained history - a well-shaped object a caller built is not
        evidence of anything, which was the audit's sixth finding."""
        self._require_progressible(run, "transferring scope")
        try:
            self._validate_transfer(run, target, authorisation)
        except GovernanceError:
            # Validation refused: nothing is recorded and nothing moves. The refusal is the
            # whole effect, because a crossing that was never authorised never happened.
            raise
        self.log.append(run.ref, "scope:transfer_authorised",
                        "%s @ %s" % (authorisation.mechanism, authorisation.mechanism_version),
                        authorisation.decision_record)
        transferred = self._create_run(definition, run_ref, target, authorisation)
        self.log.append(transferred.ref, "scope:transferred_from", str(run.ref), run.ref)
        return transferred

    def _validate_transfer(self, run: WorkflowRun, target: ScopeBinding,
                           authorisation: ScopeTransferAuthorisation) -> None:
        """Every clause of an approved crossing, checked against retained governed state."""
        if not isinstance(authorisation, ScopeTransferAuthorisation):
            raise GovernanceError(
                "crossing a scope boundary requires an approved mechanism authorisation")
        if not isinstance(target, ScopeBinding):
            raise GovernanceError("a crossing names a complete target scope binding")
        if not authorisation.covers(run, target):
            raise GovernanceError(
                "the authorisation does not cover %s -> %s for %s"
                % (run.scope.scope, target.scope, run.ref))
        # The Decision Record must be one this run actually retained, not one named in passing.
        record = None
        for retained in run.decision_records():
            if retained.ref == authorisation.decision_record:
                record = retained
                break
        if record is None:
            raise GovernanceError(
                "%s is not in %s's retained decision history"
                % (authorisation.decision_record, run.ref))
        if (record.run != run.ref or record.work_item != authorisation.work_item
                or record.requirement != authorisation.requirement
                or record.decision_right != authorisation.decision_right):
            raise GovernanceError(
                "the retained Decision Record does not answer the act being authorised")
        if record.outcome not in CONTINUING_GATE_OUTCOMES:
            raise GovernanceError("the retained Decision Record does not approve anything")
        if authorisation.authorised_by != record.decided_by:
            raise GovernanceError(
                "the authorising human is not the one who exercised the Right")
        if record.decided_by not in self.decisions.holders(authorisation.decision_right):
            raise GovernanceError(
                "%s does not hold %s in the approved decision path"
                % (record.decided_by, authorisation.decision_right))
        # The mechanism must be one the source run recognises as approved for this act.
        if self.mechanisms is None or not self.mechanisms.approves(
                authorisation.mechanism, authorisation.mechanism_version,
                run.scope, target, authorisation.decision_right,
                authorisation.authorised_act):
            raise GovernanceError(
                "%s @ %s is not approved for %s with %s on this crossing"
                % (authorisation.mechanism, authorisation.mechanism_version,
                   authorisation.authorised_act, authorisation.decision_right))
        # Sensitivity and residency are carried, never widened, across the boundary.
        if not target.sensitivity <= run.scope.sensitivity:
            raise GovernanceError(
                "a crossing may not widen sensitivity: %s is not within %s"
                % (sorted(target.sensitivity), sorted(run.scope.sensitivity)))
        if target.residency != run.scope.residency:
            raise GovernanceError(
                "a crossing may not change residency: %s is not %s"
                % (target.residency, run.scope.residency))

    # ---------------------------------------------------------------- stages and assignment

    def activate_stage(self, run: WorkflowRun, task_ref: TaskRef) -> WorkItem:
        """Create the Work Item for a Task the run's OWN definition declares.

        The Task is looked up in the bound definition rather than accepted as an argument, so
        an undeclared Task, or one from another workflow or version, cannot be activated."""
        self._require_progressible(run, "activating a stage")
        require(task_ref, TaskRef, "stage activation")
        task = run.definition.task(task_ref)      # raises LineageError when undeclared
        state = self._state(run)
        # Every remaining phase may reach RUNNING under the approved table, so the halted
        # check above is the ONLY thing that refuses a halted run - one rule, in one place,
        # rather than a second mechanism quietly doing the same work.
        if state.phase is not RunPhase.RUNNING:
            self._transition(run, RunPhase.RUNNING, detail="stage activation")
        item = WorkItem(WorkItemRef(self._next("wi")), task.ref, run.ref,
                        run.workflow, run.workflow_version, task.retry_class,
                        task.required_role, task.capability)
        state.work_items[item.ref.id] = item
        state.attempts[item.ref.id] = 0
        for requirement in task.gates:
            # Keyed by the INSTANCE identity, so activating the same Task twice, or two Tasks
            # that reuse a requirement id, produce separate retained gates.
            instance = GateInstance(GateInstanceRef(self._next("gi")), requirement, run.ref,
                                    item.ref, requirement.kind)
            state.gates[instance.ref.id] = instance
        self.log.append(run.ref, "stage:activated", task.name, item.ref)
        return item

    def unblock(self, run: WorkflowRun, intervention: HumanInterventionRecord) -> WorkflowRun:
        """Leave BLOCKED or ESCALATED, on a recorded human act and nothing else.

        A gate that resolved to a non-continuing outcome still stands: the run does not resume
        while one remains, and `AUTHORITY_ABSENT` is not cleared by asking nicely.

        This is the ONE method that does not call `_require_progressible`, and it earns the
        exemption by being harder rather than easier: a validated human intervention naming
        this run, no gate still standing against continuation, and every fallible check made
        before the first mutation."""
        state = self._state(run)
        if state.terminal is not None:
            raise TransitionError("%s is terminal" % run.ref)
        if state.phase not in HALTED_PHASES:
            raise TransitionError("%s is %s, not halted" % (run.ref, state.phase.value))
        if not isinstance(intervention, HumanInterventionRecord):
            raise GovernanceError("recovery needs a recorded human intervention")
        if intervention.run != run.ref:
            raise LineageError("the intervention names another run")
        require(intervention.by, HumanAuthorityRef, "intervention")
        standing = [g for g in run.gates() if g.is_resolved() and not g.is_continuing()]
        if standing:
            raise GovernanceError(
                "%d gate(s) still stand unresolved in favour of continuation; the blocking "
                "constraint is not satisfied" % len(standing))
        self._store(run, "interventions").validate_add(intervention)
        self._preflight_phases(run, (RunPhase.RUNNING,))
        self._record_intervention(run, intervention)
        self._transition(run, RunPhase.RUNNING, detail=intervention.reason)
        if state.posture is not GovernancePosture.OPEN_ITEMS_CARRIED:
            self._set_posture(run, GovernancePosture.GOVERNANCE_CLEAR,
                              "the blocking constraint was resolved by a governed act")
        return run

    def _bound_item(self, run: WorkflowRun, work_item) -> WorkItem:
        """The Work Item this run created, looked up rather than accepted."""
        ref = work_item.ref if isinstance(work_item, WorkItem) else work_item
        item = run.work_item(ref)
        if isinstance(work_item, WorkItem) and work_item != item:
            raise LineageError("the Work Item offered is not the one %s created" % run.ref)
        return item

    def _bound_gate(self, run: WorkflowRun, item: WorkItem, requirement) -> GateInstance:
        """The gate instance this run holds for that Work Item and that requirement."""
        if isinstance(requirement, GateInstanceRef):
            instance = run.gate(requirement)
            if instance.work_item != item.ref:
                raise LineageError("%s is not a gate of %s" % (requirement, item.ref))
            return instance
        ref = requirement.ref if isinstance(requirement, GateRequirement) else requirement
        instance = run.gate_instance(item.ref, ref)
        if isinstance(requirement, GateRequirement) and requirement != instance.requirement:
            raise LineageError("the gate requirement offered is not the declared one")
        return instance

    def assign(self, run: WorkflowRun, work_item, role: RoleRef,
               agent_instance=None) -> Assignment:
        """Bind a Role - and where permitted an Agent Instance - to a Work Item.

        The required Role comes from the Work Item's bound lineage, not from a Task argument."""
        self._require_progressible(run, "assignment")
        item = self._bound_item(run, work_item)
        require(role, RoleRef, "assignment")
        if role != item.required_role:
            raise GovernanceError("%s is not the Role the task requires (%s)"
                                  % (role, item.required_role))
        state = self._state(run)
        state.attempts[item.ref.id] = state.attempts.get(item.ref.id, 0) + 1
        assignment = Assignment(item.ref, role, agent_instance,
                                attempt=state.attempts[item.ref.id])
        self._store(run, "assignments").add(assignment)
        self.log.append(run.ref, "assignment:created",
                        "attempt %d" % assignment.attempt, item.ref)
        return assignment

    # ---------------------------------------------------------------- routing

    def request_routing(self, run: WorkflowRun, work_item,
                        routing_policy: str) -> RoutingRequest:
        """Create and RECORD the Routing Request. The orchestrator may not choose the model."""
        self._require_progressible(run, "routing")
        item = self._bound_item(run, work_item)
        request = RoutingRequest(RoutingRequestRef(self._next("rr")), run.ref, item.ref,
                                 item.capability, run.scope, routing_policy)
        self._store(run, "routing_requests").add(request)
        self.log.append(run.ref, "routing:requested", item.capability, request.ref)
        return request

    def _validate_router_answer(self, run: WorkflowRun, request: RoutingRequest,
                                decision: RoutingDecision) -> None:
        """Validate the configured Router's direct answer without recording it."""
        if not isinstance(decision, RoutingDecision):
            raise GovernanceError("only a Routing Decision can be recorded as routing")
        if not self._store(run, "routing_requests").contains(request):
            raise LineageError("that routing request was not issued by this run")
        if not decision.answers(request):
            raise LineageError("the routing decision does not answer %s" % request.ref)
        configured = getattr(self.router, "ref", None)
        if not isinstance(configured, RouterRef) or decision.decided_by != configured:
            raise LineageError(
                "the routing decision was not made by the configured Router (%s)" % configured)

    def route(self, run: WorkflowRun, work_item, routing_policy: str) -> RoutingDecision:
        """Ask the configured Router, then record exactly what it returned.

        This is the only path by which a Routing Decision reaches governed history."""
        request = self.request_routing(run, work_item, routing_policy)
        answer = self.router.route(request)
        self._validate_router_answer(run, request, answer)
        # Preflight every resulting phase before recording the answer. A malformed state cannot
        # leave a Routing Decision in history without its declared state effect.
        phases = ()
        if answer.outcome is RouterOutcome.NO_APPLICABLE_DECISION_RIGHT:
            phases = (RunPhase.BLOCKED, RunPhase.ESCALATED)
        elif answer.outcome is not RouterOutcome.ELIGIBLE_CANDIDATE:
            phases = (RunPhase.BLOCKED,)
        self._preflight_phases(run, phases)
        self._store(run, "routing").validate_add(answer)
        self._store(run, "routing").add(answer)
        self.log.append(run.ref, "routing:decided", answer.outcome.value, answer.ref)
        if answer.outcome is RouterOutcome.NO_APPLICABLE_DECISION_RIGHT:
            self._transition(run, RunPhase.BLOCKED, detail="routing has no applicable Right")
            self._transition(run, RunPhase.ESCALATED, detail="governance design escalation")
            self._set_posture(run, GovernancePosture.AUTHORITY_ABSENT,
                              "no approved Decision Right covers the routing act")
        elif answer.outcome is not RouterOutcome.ELIGIBLE_CANDIDATE:
            self._transition(run, RunPhase.BLOCKED, detail=answer.outcome.value)
            self._set_posture(run, GovernancePosture.GATE_UNSATISFIED,
                              "no eligible candidate, and no fallback outside the eligible set")
        return answer

    # ---------------------------------------------------------------- model execution

    def invoke_model(self, run: WorkflowRun, work_item, decision: RoutingDecision,
                     prompt_context: str = "") -> ModelResult:
        """Execute the model a RECORDED Routing Decision selected.

        The decision must be the very object this run recorded from its own Router request. A
        fabricated decision naming an arbitrary model is refused here, before any execution."""
        self._require_progressible(run, "model invocation")
        item = self._bound_item(run, work_item)
        if not self._store(run, "routing").contains(decision):
            raise LineageError(
                "that Routing Decision is not the recorded Router output for this run")
        if decision.work_item != item.ref or decision.run != run.ref:
            raise LineageError("the Routing Decision was made for other work")
        if decision.outcome is not RouterOutcome.ELIGIBLE_CANDIDATE:
            raise GovernanceError("no eligible candidate was selected; there is nothing to run")
        request = ModelInvocationRequest(run.ref, item.ref, decision.ref, decision.model,
                                         decision.model_profile, prompt_context)
        result = self.model.execute(request)
        # A model adapter answering for other work is refused before anything is recorded.
        if not isinstance(result, ModelResult):
            raise LineageError("the model adapter did not return a Model Result")
        if (result.run != run.ref or result.work_item != item.ref
                or result.routing_decision != decision.ref or result.model != decision.model
                or result.model_profile != decision.model_profile):
            raise LineageError(
                "the model result does not answer the recorded Routing Decision for this work")
        self._store(run, "model_results").validate_add(result)
        self._store(run, "model_results").add(result)
        self.log.append(run.ref, "model:result",
                        "%s / %s" % (result.origin.value, result.canonicality.value),
                        decision.ref)
        return result

    # ---------------------------------------------------------------- gates

    #: Which governed store retains the evidence that satisfies each gate kind. Evidence that
    #: satisfies a gate is retained by its own record identity, atomically with the outcome:
    #: a completion that cannot be explained from history is not explained at all.
    EVIDENCE_STORE = {
        GateKind.REVIEW: "reviews",
        GateKind.DECISION: "decisions",
        GateKind.HUMAN_WORK: "human_work",
        GateKind.GOVERNED_PREREQUISITE: "prerequisites",
    }

    def _preflight_phases(self, run: WorkflowRun, phases) -> None:
        """Prove a phase sequence is legal without changing the run or its log."""
        state = self._state(run)
        if state.terminal is not None:
            raise TransitionError("run %s is terminal as %s and cannot move again"
                                  % (run.ref, state.terminal.value))
        current = state.phase
        for phase in phases:
            if phase is current:
                continue
            if phase not in ALLOWED_TRANSITIONS[current]:
                raise TransitionError("%s -> %s is not an approved transition"
                                      % (current.value, phase.value))
            current = phase

    def _gate_phase_plan(self, run: WorkflowRun, outcome: GateOutcome,
                         wait_reason: Optional[WaitReason]) -> Tuple[RunPhase, ...]:
        """Return the exact phase sequence a gate commit will apply."""
        current = self._state(run).phase
        phases = []
        if wait_reason is not None and current is not RunPhase.WAITING:
            phases.append(RunPhase.WAITING)
            current = RunPhase.WAITING
        if outcome in CONTINUING_GATE_OUTCOMES and current is RunPhase.WAITING:
            phases.append(RunPhase.RUNNING)
            current = RunPhase.RUNNING
        if outcome is GateOutcome.NOT_SATISFIED:
            phases.append(RunPhase.REWORK_REQUIRED)
        elif outcome is GateOutcome.DEFER and current is not RunPhase.WAITING:
            phases.append(RunPhase.WAITING)
        elif outcome in (GateOutcome.ESCALATE, GateOutcome.EXPIRED):
            phases.append(RunPhase.ESCALATED)
        elif outcome is GateOutcome.NO_APPLICABLE_DECISION_RIGHT:
            phases.extend((RunPhase.BLOCKED, RunPhase.ESCALATED))
        return tuple(phases)

    def validate_evidence(self, run: WorkflowRun, item: WorkItem, instance: GateInstance,
                          evidence, outcome: GateOutcome) -> None:
        """Evidence must answer THIS requirement, and say what it is being read as saying.

        Per gate kind there is exactly one admissible evidence type, so a Review Instance can
        never satisfy a HUMAN_WORK gate and a Decision Record can never satisfy a
        GOVERNED_PREREQUISITE gate. Beyond the type, every binding is checked: run, Work Item,
        requirement identity, the named Profile or Right, the declared independence class, and
        for a decision the holder's standing in the approved decision path. Finally the
        evidence's own outcome must equal the outcome being applied - an adapter tuple cannot
        override the record it came with.

        This function only reads. Nothing it touches is mutated, which is what lets every
        governed act validate fully before anything is committed."""
        requirement = instance.requirement
        if not isinstance(outcome, GateOutcome):
            raise EvidenceError("a gate outcome must be one of the seven approved outcomes")
        admissible = EVIDENCE_CONTRACT[requirement.kind]
        if type(evidence) is not admissible:
            raise EvidenceError(
                "a %s gate is satisfied only by %s, got %s"
                % (requirement.kind.value, admissible.__name__, type(evidence).__name__))
        if evidence.run != run.ref or evidence.work_item != item.ref:
            raise EvidenceError("the evidence was produced for other work")
        if evidence.requirement != requirement.ref:
            raise EvidenceError("the evidence answers %s, not %s"
                                % (evidence.requirement, requirement.ref))
        if evidence.outcome is not outcome:
            raise EvidenceError("the evidence records %s, but %s is being applied"
                                % (evidence.outcome.value, outcome.value))
        if requirement.kind is GateKind.REVIEW:
            if evidence.review_profile != requirement.review_profile:
                raise EvidenceError("the review was done under a different Review Profile")
            if evidence.independence_class != requirement.independence_class:
                raise EvidenceError(
                    "the gate requires a %s review; the evidence is %s"
                    % (requirement.independence_class, evidence.independence_class))
        elif requirement.kind is GateKind.DECISION:
            if evidence.decision_right != requirement.decision_right:
                raise EvidenceError("the Decision Record exercises a different Right")
            holders = self.decisions.holders(requirement.decision_right)
            if evidence.decided_by not in holders:
                raise EvidenceError(
                    "%s does not hold %s in the approved decision path"
                    % (evidence.decided_by, requirement.decision_right))
        elif requirement.kind is GateKind.HUMAN_WORK:
            if evidence.human_work != requirement.human_work:
                raise EvidenceError("the completion answers a different human work request")
        elif requirement.kind is GateKind.GOVERNED_PREREQUISITE:
            if evidence.prerequisite != requirement.prerequisite:
                raise EvidenceError("the evidence evaluates a different prerequisite")

    def _commit_gate(self, run: WorkflowRun, instance: GateInstance, outcome: GateOutcome,
                     evidence, *, wait_reason: Optional[WaitReason] = None,
                     wait_subject: Optional[Ref] = None, detail: str = "") -> GateInstance:
        """Apply a fully validated gate result. Called only after validation has passed.

        The order is: record that the gate was asked, retain the evidence, resolve the gate,
        then let the outcome have its declared run effect. Everything before this point is a
        read, so a refusal leaves the run and its histories exactly as they were."""
        state = self._state(run)
        if wait_reason is not None and wait_subject is None:
            raise GovernanceError("a WAITING gate must name its subject")
        if evidence is not None:
            self._store(run, self.EVIDENCE_STORE[instance.kind]).validate_add(evidence)
        # All fallible state/history checks happen before the first mutation.
        self._preflight_phases(run, self._gate_phase_plan(run, outcome, wait_reason))
        if wait_reason is not None:
            self._ensure_phase(run, RunPhase.WAITING, detail=detail or "gate requested",
                               wait_reason=wait_reason, wait_subject=wait_subject)
        if evidence is not None:
            self._store(run, self.EVIDENCE_STORE[instance.kind]).add(evidence)
        satisfied_by = getattr(evidence, "ref", None) if evidence is not None else None
        resolved = instance.resolved(outcome, satisfied_by)
        state.gates[instance.ref.id] = resolved
        self.log.append(run.ref, "gate:%s" % instance.kind.value, outcome.value, satisfied_by)
        if outcome in CONTINUING_GATE_OUTCOMES and state.phase is RunPhase.WAITING:
            self._transition(run, RunPhase.RUNNING, detail="gate satisfied")
        self._apply_gate_outcome(run, outcome, satisfied_by or instance.ref)
        return resolved

    def _apply_gate_outcome(self, run: WorkflowRun, outcome: GateOutcome,
                            subject: Ref) -> None:
        """The declared run effect of each of the seven outcomes. None of them approve.

        Every public satisfaction path funnels through here, so `SATISFIED_WITH_OPEN_ITEMS`
        carries `OPEN_ITEMS_CARRIED` for all four gate kinds - the audit's fifth finding was
        that only the review path did."""
        if outcome is GateOutcome.SATISFIED:
            return
        if outcome is GateOutcome.SATISFIED_WITH_OPEN_ITEMS:
            self._set_posture(run, GovernancePosture.OPEN_ITEMS_CARRIED,
                              "items carried under a named upstream rule")
            return
        if outcome is GateOutcome.NOT_SATISFIED:
            self._transition(run, RunPhase.REWORK_REQUIRED, detail="gate not satisfied")
            self._set_posture(run, GovernancePosture.GATE_UNSATISFIED, "rework required")
            return
        if outcome is GateOutcome.DEFER:
            self._ensure_phase(run, RunPhase.WAITING, detail="gate deferred",
                               wait_reason=WaitReason.WAITING_FOR_DECISION,
                               wait_subject=subject)
            self._set_posture(run, GovernancePosture.GATE_UNSATISFIED, "deferred, not approved")
            return
        if outcome is GateOutcome.ESCALATE:
            self._transition(run, RunPhase.ESCALATED, detail="gate escalated")
            self._set_posture(run, GovernancePosture.GATE_UNSATISFIED,
                              "escalated, not approved")
            return
        if outcome is GateOutcome.EXPIRED:
            # A timeout is not an approval, and the posture is unchanged by expiry.
            self._transition(run, RunPhase.ESCALATED, detail="gate expired")
            return
        if outcome is GateOutcome.NO_APPLICABLE_DECISION_RIGHT:
            self._transition(run, RunPhase.BLOCKED, detail="no applicable Decision Right")
            self._transition(run, RunPhase.ESCALATED, detail="governance design escalation")
            self._set_posture(run, GovernancePosture.AUTHORITY_ABSENT,
                              "no approved Phase 7 Right covers the act")
            return
        raise GovernanceError("unknown gate outcome %r" % (outcome,))

    def satisfy_gate_with(self, run: WorkflowRun, work_item, requirement,
                          evidence, outcome: Optional[GateOutcome] = None) -> GateInstance:
        """Record a gate outcome, only on evidence that answers this exact requirement.

        The evidence is retained in its governed store as part of the same commit: there is no
        path here that changes gate state without the record that explains it."""
        self._require_progressible(run, "gate satisfaction")
        item = self._bound_item(run, work_item)
        instance = self._bound_gate(run, item, requirement)
        applied = outcome if outcome is not None else getattr(evidence, "outcome", None)
        self.validate_evidence(run, item, instance, evidence, applied)
        if applied not in CONTINUING_GATE_OUTCOMES:
            raise EvidenceError("%s does not satisfy a gate" % applied.value)
        return self._commit_gate(run, instance, applied, evidence)

    def run_review_gate(self, run: WorkflowRun, work_item, requirement) -> ReviewInstance:
        """Detect, request, record. The orchestrator is not the reviewer.

        The desk is asked, the answer is validated in full, and only then does any state move."""
        self._require_progressible(run, "review progression")
        item = self._bound_item(run, work_item)
        instance = self._bound_gate(run, item, requirement)
        declared = instance.requirement
        if declared.kind is not GateKind.REVIEW:
            raise EvidenceError("%s is not a review gate" % declared.ref)
        request = ReviewRequest(declared.ref, run.ref, item.ref, declared.review_profile,
                                declared.independence_class)
        result = self.reviewers.review(request)
        self.validate_evidence(run, item, instance, result, result.outcome)
        self._commit_gate(run, instance, result.outcome, result,
                          wait_reason=WaitReason.WAITING_FOR_REVIEW,
                          wait_subject=declared.review_profile, detail="review requested")
        return result

    def run_decision_gate(self, run: WorkflowRun, work_item,
                          requirement) -> Tuple[GateOutcome, Optional[DecisionRecord]]:
        """Detect, name the Right, request, record. The orchestrator is not the decider.

        A continuing outcome with no Decision Record is refused before anything moves: an
        approval with no record of a human exercising a Right is exactly what this phase
        exists to make impossible."""
        self._require_progressible(run, "decision progression")
        item = self._bound_item(run, work_item)
        instance = self._bound_gate(run, item, requirement)
        declared = instance.requirement
        if declared.kind is not GateKind.DECISION:
            raise EvidenceError("%s is not a decision gate" % declared.ref)
        request = DecisionRequest(declared.ref, run.ref, item.ref, declared.decision_right)
        answer = self.decisions.decide(request)
        if not (isinstance(answer, tuple) and len(answer) == 2):
            raise EvidenceError("the decision authority must answer (outcome, record)")
        outcome, record = answer
        if not isinstance(outcome, GateOutcome):
            raise EvidenceError("the decision authority must answer with a gate outcome")
        if outcome in CONTINUING_GATE_OUTCOMES:
            if record is None:
                raise MissingEvidenceError(
                    "%s was answered with no Decision Record; an approval with no record of a "
                    "human exercising a Right is not an approval" % outcome.value)
            self.validate_evidence(run, item, instance, record, outcome)
        elif record is not None:
            self.validate_evidence(run, item, instance, record, outcome)
        self._commit_gate(run, instance, outcome, record,
                          wait_reason=WaitReason.WAITING_FOR_DECISION,
                          wait_subject=declared.decision_right, detail="decision requested")
        return outcome, record

    def record_human_work(self, run: WorkflowRun, work_item, requirement,
                          completion: HumanWorkCompletion) -> GateInstance:
        """A human completing requested work, retained and applied like any other evidence."""
        self._require_progressible(run, "human-work progression")
        item = self._bound_item(run, work_item)
        instance = self._bound_gate(run, item, requirement)
        self.validate_evidence(run, item, instance, completion, completion.outcome)
        return self._commit_gate(run, instance, completion.outcome, completion,
                                 wait_reason=WaitReason.WAITING_FOR_HUMAN,
                                 wait_subject=instance.requirement.human_work,
                                 detail="human work requested")

    def record_prerequisite(self, run: WorkflowRun, work_item, requirement,
                            evidence: PrerequisiteEvidence) -> GateInstance:
        """A Phase 8-10 prerequisite evaluated against recorded state."""
        self._require_progressible(run, "prerequisite progression")
        item = self._bound_item(run, work_item)
        instance = self._bound_gate(run, item, requirement)
        self.validate_evidence(run, item, instance, evidence, evidence.outcome)
        return self._commit_gate(run, instance, evidence.outcome, evidence)

    # ---------------------------------------------------------------- retry

    def retry(self, run: WorkflowRun, work_item, *,
              acknowledgement: Optional[HumanInterventionRecord] = None,
              revalidated: bool = False) -> RunPhase:
        """Retry according to the retry class bound to the WORK ITEM, and no further.

        The class comes from the lineage the Work Item was created under. A caller who presents
        a substitute Task claiming a friendlier class changes nothing: the argument is not
        consulted, because there is no argument."""
        self._require_progressible(run, "retry")
        item = self._bound_item(run, work_item)
        cls = item.retry_class
        state = self._state(run)
        if cls in NEVER_AUTOMATICALLY_RETRYABLE:
            self._transition(run, RunPhase.BLOCKED,
                             detail="%s is never retried automatically" % cls.value)
            self._transition(run, RunPhase.ESCALATED, detail="compensation is a new act")
            self._set_posture(run, GovernancePosture.GATE_UNSATISFIED,
                              "recovery requires a separately authorised act")
            return state.phase
        if cls is RetryClass.RETRY_REQUIRING_HUMAN_ACKNOWLEDGEMENT:
            if acknowledgement is None:
                self._transition(run, RunPhase.WAITING, detail="retry needs acknowledgement",
                                 wait_reason=WaitReason.WAITING_FOR_HUMAN,
                                 wait_subject=item.ref)
                return state.phase
            if acknowledgement.run != run.ref:
                raise LineageError("the acknowledgement was recorded against another run")
            self._store(run, "interventions").add(acknowledgement)
            self.log.append(run.ref, "intervention:acknowledged", acknowledgement.reason,
                            acknowledgement.ref)
        if cls is RetryClass.RETRY_REQUIRING_REVALIDATION and not revalidated:
            raise GovernanceError(
                "%s must re-check preconditions, evidence freshness, scope, sensitivity and "
                "assignment eligibility before the retry" % cls.value)
        # RETRY_PENDING is reachable only from RUNNING in the approved table.
        if state.phase is RunPhase.RUNNING:
            self._transition(run, RunPhase.RETRY_PENDING, detail="retry scheduled")
        self._ensure_phase(run, RunPhase.RUNNING, detail="retry dispatched")
        self.log.append(run.ref, "retry:dispatched", cls.value, item.ref)
        return state.phase

    # ---------------------------------------------------------------- human intervention

    def record_intervention(self, run: WorkflowRun,
                            intervention: HumanInterventionRecord) -> HumanInterventionRecord:
        """A human act on the run. The human is recorded first; automation refuses after."""
        self._require_progressible(run, "recording an intervention")
        return self._record_intervention(run, intervention)

    def _record_intervention(self, run: WorkflowRun,
                             intervention: HumanInterventionRecord) -> HumanInterventionRecord:
        """The unguarded form, used by the governed recovery path and by stopping a run."""
        require(intervention.by, HumanAuthorityRef, "intervention")
        if intervention.run != run.ref:
            raise LineageError("the intervention names another run")
        self._store(run, "interventions").add(intervention)
        self.log.append(run.ref, "intervention:recorded", intervention.act, intervention.ref)
        return intervention

    def pause(self, run: WorkflowRun, intervention: HumanInterventionRecord) -> WorkflowRun:
        self._require_progressible(run, "pausing the run")
        self.record_intervention(run, intervention)
        return self._transition(run, RunPhase.PAUSED, detail=intervention.reason)

    # ---------------------------------------------------------------- completion

    def unsatisfied_gates(self, run: WorkflowRun) -> Tuple[GateInstance, ...]:
        return tuple(g for g in run.gates() if not g.is_continuing())

    def complete(self, run: WorkflowRun, outcome: TerminalOutcome,
                 *, cause: str = "",
                 intervention: Optional[HumanInterventionRecord] = None) -> WorkflowRun:
        """Reach a terminal outcome, only where the governed state permits it.

        Everything consulted here - phase, posture, open gates - is state this orchestrator
        recorded through its own token. A caller cannot set it and then complete."""
        if outcome not in NON_COMPLETION_TERMINALS:
            # A halted run may still be cancelled or terminated - stopping is always
            # permitted - but it may not COMPLETE.
            self._require_progressible(run, "completing the run")
        state = self._state(run)
        if state.terminal is not None:
            raise TransitionError("run %s is already terminal" % run.ref)
        if state.phase not in TERMINAL_REACHABLE_FROM[outcome]:
            raise TransitionError("%s is not reachable from %s"
                                  % (outcome.value, state.phase.value))
        if outcome in NON_COMPLETION_TERMINALS:
            if outcome is TerminalOutcome.CANCELLED and intervention is None:
                raise GovernanceError("CANCELLED requires an intervention record")
            if outcome is TerminalOutcome.TERMINATED and not cause:
                raise GovernanceError("TERMINATED requires a named constraint")
            if outcome is TerminalOutcome.FAILED and not cause:
                raise GovernanceError("FAILED requires a recorded cause")
        else:
            permitted = POSTURE_PERMITS_COMPLETION[state.posture]
            if outcome not in permitted:
                raise GovernanceError(
                    "posture %s does not permit %s" % (state.posture.value, outcome.value))
            outstanding = self.unsatisfied_gates(run)
            if outstanding:
                raise GovernanceError(
                    "%d gate(s) are not satisfied; completion is not available"
                    % len(outstanding))
        if intervention is not None:
            self._store(run, "interventions").validate_add(intervention)
            self._record_intervention(run, intervention)
        state.terminal = outcome
        self.log.append(run.ref, "terminal:%s" % outcome.value, cause)
        return run
