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
    EVIDENCE_CONTRACT, EvidenceError, ExecutionEventLog, GateInstance, GateKind, GateOutcome,
    GateRequirement, GateRequirementRef, GovernanceError, GovernancePosture,
    HumanAuthorityRef, HumanInterventionRecord, HumanWorkCompletion, LineageError,
    ModelInvocationRequest, ModelResult, NEVER_AUTOMATICALLY_RETRYABLE,
    NON_COMPLETION_TERMINALS, POSTURE_PERMITS_COMPLETION, PrerequisiteEvidence, Ref,
    ReviewInstance, ReviewRequest, RetryClass, RoleRef, RouterOutcome, RoutingDecision,
    RoutingRequest, RoutingRequestRef, RunPhase, ScopeBinding, ScopeTransferAuthorisation,
    StateAccessError, TERMINAL_REACHABLE_FROM, TaskRef, TerminalOutcome, TransitionError,
    WaitReason, WorkItem, WorkItemRef, WorkflowDefinition, WorkflowRun, WorkflowRunRef,
    require,
)


class Orchestrator:
    """A coordination control plane. It holds no authority of its own."""

    def __init__(self, router: RouterAdapter, reviewers: ReviewerAdapter,
                 decisions: DecisionAuthorityAdapter, model: ModelAdapter,
                 log: Optional[ExecutionEventLog] = None):
        self.router = router
        self.reviewers = reviewers
        self.decisions = decisions
        self.model = model
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
        self._token(parent)                      # the parent must be this orchestrator's
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
        crossing produces a new run in the target scope, and it happens only on the strength of
        a `ScopeTransferAuthorisation` that names this run, this source scope, that target
        scope, the mechanism at a version, and the Decision Record authorising it. A bare
        handoff or transfer reference proves nothing and is refused."""
        self._token(run)
        if not isinstance(authorisation, ScopeTransferAuthorisation):
            self._transition(run, RunPhase.BLOCKED,
                             detail="scope crossing without approved authorisation")
            self._set_posture(run, GovernancePosture.GATE_UNSATISFIED,
                              "no approved transfer or handoff evidence")
            raise GovernanceError(
                "crossing a scope boundary requires an approved mechanism authorisation")
        if not authorisation.authorises(run, target):
            self._transition(run, RunPhase.BLOCKED,
                             detail="authorisation does not cover this crossing")
            self._set_posture(run, GovernancePosture.GATE_UNSATISFIED,
                              "the authorisation names a different run, scope or target")
            raise GovernanceError(
                "the authorisation does not cover %s -> %s for %s"
                % (run.scope.scope, target.scope, run.ref))
        self.log.append(run.ref, "scope:transfer_authorised",
                        "%s @ %s" % (authorisation.mechanism, authorisation.mechanism_version),
                        authorisation.decision_record)
        transferred = self._create_run(definition, run_ref, target, authorisation)
        self.log.append(transferred.ref, "scope:transferred_from", str(run.ref), run.ref)
        return transferred

    # ---------------------------------------------------------------- stages and assignment

    def activate_stage(self, run: WorkflowRun, task_ref: TaskRef) -> WorkItem:
        """Create the Work Item for a Task the run's OWN definition declares.

        The Task is looked up in the bound definition rather than accepted as an argument, so
        an undeclared Task, or one from another workflow or version, cannot be activated."""
        require(task_ref, TaskRef, "stage activation")
        task = run.definition.task(task_ref)      # raises LineageError when undeclared
        state = self._state(run)
        if state.phase in (RunPhase.READY, RunPhase.WAITING, RunPhase.BLOCKED,
                           RunPhase.ESCALATED, RunPhase.RETRY_PENDING,
                           RunPhase.REWORK_REQUIRED, RunPhase.PAUSED):
            self._transition(run, RunPhase.RUNNING, detail="stage activation")
        elif state.phase is not RunPhase.RUNNING:
            raise TransitionError("a stage cannot be activated from %s" % state.phase.value)
        item = WorkItem(WorkItemRef(self._next("wi")), task.ref, run.ref,
                        run.workflow, run.workflow_version, task.retry_class,
                        task.required_role, task.capability)
        state.work_items[item.ref.id] = item
        state.attempts[item.ref.id] = 0
        for requirement in task.gates:
            state.gates[requirement.ref.id] = GateInstance(requirement, run.ref, item.ref)
        self.log.append(run.ref, "stage:activated", task.name, item.ref)
        return item

    def _bound_item(self, run: WorkflowRun, work_item) -> WorkItem:
        """The Work Item this run created, looked up rather than accepted."""
        ref = work_item.ref if isinstance(work_item, WorkItem) else work_item
        item = run.work_item(ref)
        if isinstance(work_item, WorkItem) and work_item != item:
            raise LineageError("the Work Item offered is not the one %s created" % run.ref)
        return item

    def _bound_gate(self, run: WorkflowRun, item: WorkItem,
                    requirement) -> GateInstance:
        ref = requirement.ref if isinstance(requirement, GateRequirement) else requirement
        instance = run.gate(ref)
        if instance.work_item != item.ref:
            raise LineageError("%s is not a gate of %s" % (ref, item.ref))
        if isinstance(requirement, GateRequirement) and requirement != instance.requirement:
            raise LineageError("the gate requirement offered is not the declared one")
        return instance

    def assign(self, run: WorkflowRun, work_item, role: RoleRef,
               agent_instance=None) -> Assignment:
        """Bind a Role - and where permitted an Agent Instance - to a Work Item.

        The required Role comes from the Work Item's bound lineage, not from a Task argument."""
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
        item = self._bound_item(run, work_item)
        request = RoutingRequest(RoutingRequestRef(self._next("rr")), run.ref, item.ref,
                                 item.capability, run.scope, routing_policy)
        self._store(run, "routing_requests").add(request)
        self.log.append(run.ref, "routing:requested", item.capability, request.ref)
        return request

    def record_routing_decision(self, run: WorkflowRun, request: RoutingRequest,
                                decision: RoutingDecision) -> RoutingDecision:
        """Record the Router's answer, bound to the exact request it answers."""
        if not isinstance(decision, RoutingDecision):
            raise GovernanceError("only a Routing Decision can be recorded as routing")
        if not self._store(run, "routing_requests").contains(request):
            raise LineageError("that routing request was not issued by this run")
        if not decision.answers(request):
            raise LineageError("the routing decision does not answer %s" % request.ref)
        self._store(run, "routing").add(decision)
        self.log.append(run.ref, "routing:decided", decision.outcome.value, decision.ref)
        if decision.outcome is RouterOutcome.NO_APPLICABLE_DECISION_RIGHT:
            self._transition(run, RunPhase.BLOCKED, detail="routing has no applicable Right")
            self._transition(run, RunPhase.ESCALATED, detail="governance design escalation")
            self._set_posture(run, GovernancePosture.AUTHORITY_ABSENT,
                              "no approved Decision Right covers the routing act")
        elif decision.outcome is not RouterOutcome.ELIGIBLE_CANDIDATE:
            self._transition(run, RunPhase.BLOCKED, detail=decision.outcome.value)
            self._set_posture(run, GovernancePosture.GATE_UNSATISFIED,
                              "no eligible candidate, and no fallback outside the eligible set")
        return decision

    def route(self, run: WorkflowRun, work_item, routing_policy: str) -> RoutingDecision:
        """Ask, then record. Request and decision stay two objects, by two parties."""
        request = self.request_routing(run, work_item, routing_policy)
        return self.record_routing_decision(run, request, self.router.route(request))

    # ---------------------------------------------------------------- model execution

    def invoke_model(self, run: WorkflowRun, work_item, decision: RoutingDecision,
                     prompt_context: str = "") -> ModelResult:
        """Execute the model a RECORDED Routing Decision selected.

        The decision must be the very object this run recorded from its own Router request. A
        fabricated decision naming an arbitrary model is refused here, before any execution."""
        item = self._bound_item(run, work_item)
        if not self._store(run, "routing").contains(decision):
            raise LineageError(
                "that Routing Decision is not the recorded Router output for this run")
        if decision.work_item != item.ref or decision.run != run.ref:
            raise LineageError("the Routing Decision was made for other work")
        if decision.outcome is not RouterOutcome.ELIGIBLE_CANDIDATE:
            raise GovernanceError("no eligible candidate was selected; there is nothing to run")
        request = ModelInvocationRequest(run.ref, item.ref, decision.ref, decision.model,
                                         prompt_context)
        result = self.model.execute(request)
        if result.model != decision.model or result.routing_decision != decision.ref:
            raise LineageError("the model result does not answer the recorded Routing Decision")
        self._store(run, "model_results").add(result)
        self.log.append(run.ref, "model:result",
                        "%s / %s" % (result.origin.value, result.canonicality.value),
                        decision.ref)
        return result

    # ---------------------------------------------------------------- gates

    def _resolve_gate(self, run: WorkflowRun, instance: GateInstance, outcome: GateOutcome,
                      satisfied_by: Optional[Ref]) -> GateInstance:
        state = self._state(run)
        resolved = instance.resolved(outcome, satisfied_by)
        state.gates[instance.requirement.ref.id] = resolved
        self.log.append(run.ref, "gate:%s" % instance.kind.value, outcome.value, satisfied_by)
        return resolved

    def validate_evidence(self, run: WorkflowRun, item: WorkItem, instance: GateInstance,
                          evidence, outcome: GateOutcome) -> None:
        """Evidence must answer THIS requirement, and say what it is being read as saying.

        Per gate kind there is exactly one admissible evidence type, so a Review Instance can
        never satisfy a HUMAN_WORK gate and a Decision Record can never satisfy a
        GOVERNED_PREREQUISITE gate. Beyond the type, every binding is checked: run, Work Item,
        requirement identity, the named Profile or Right, the declared independence class, and
        for a decision the holder's standing in the approved decision path. Finally the
        evidence's own outcome must equal the outcome being applied - an adapter tuple cannot
        override the record it came with."""
        requirement = instance.requirement
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

    def _apply_gate_outcome(self, run: WorkflowRun, outcome: GateOutcome,
                            subject: Ref) -> None:
        """The declared run effect of each of the seven outcomes. None of them approve."""
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
        """Record a gate outcome, only on evidence that answers this exact requirement."""
        item = self._bound_item(run, work_item)
        instance = self._bound_gate(run, item, requirement)
        applied = outcome if outcome is not None else getattr(evidence, "outcome", None)
        if not isinstance(applied, GateOutcome):
            raise EvidenceError("a gate outcome must be one of the seven approved outcomes")
        self.validate_evidence(run, item, instance, evidence, applied)
        if applied not in CONTINUING_GATE_OUTCOMES:
            raise EvidenceError("%s does not satisfy a gate" % applied.value)
        return self._resolve_gate(run, instance, applied, evidence.ref
                                  if hasattr(evidence, "ref") else None)

    def run_review_gate(self, run: WorkflowRun, work_item, requirement) -> ReviewInstance:
        """Detect, request, record. The orchestrator is not the reviewer."""
        item = self._bound_item(run, work_item)
        instance = self._bound_gate(run, item, requirement)
        declared = instance.requirement
        if declared.kind is not GateKind.REVIEW:
            raise EvidenceError("%s is not a review gate" % declared.ref)
        request = ReviewRequest(declared.ref, run.ref, item.ref, declared.review_profile,
                                declared.independence_class)
        self._transition(run, RunPhase.WAITING, detail="review requested",
                         wait_reason=WaitReason.WAITING_FOR_REVIEW,
                         wait_subject=declared.review_profile)
        result = self.reviewers.review(request)
        self.validate_evidence(run, item, instance, result, result.outcome)
        self._store(run, "reviews").add(result)
        self._resolve_gate(run, instance, result.outcome, result.ref)
        if result.outcome in CONTINUING_GATE_OUTCOMES:
            self._transition(run, RunPhase.RUNNING, detail="review satisfied")
        self._apply_gate_outcome(run, result.outcome, result.ref)
        return result

    def run_decision_gate(self, run: WorkflowRun, work_item,
                          requirement) -> Tuple[GateOutcome, Optional[DecisionRecord]]:
        """Detect, name the Right, request, record. The orchestrator is not the decider."""
        item = self._bound_item(run, work_item)
        instance = self._bound_gate(run, item, requirement)
        declared = instance.requirement
        if declared.kind is not GateKind.DECISION:
            raise EvidenceError("%s is not a decision gate" % declared.ref)
        request = DecisionRequest(declared.ref, run.ref, item.ref, declared.decision_right)
        self._transition(run, RunPhase.WAITING, detail="decision requested",
                         wait_reason=WaitReason.WAITING_FOR_DECISION,
                         wait_subject=declared.decision_right)
        outcome, record = self.decisions.decide(request)
        if record is not None:
            # The adapter's tuple may not contradict the record it came with.
            self.validate_evidence(run, item, instance, record, outcome)
            self._store(run, "decisions").add(record)
        self._resolve_gate(run, instance, outcome, record.ref if record is not None else None)
        if outcome in CONTINUING_GATE_OUTCOMES:
            self._transition(run, RunPhase.RUNNING, detail="decision satisfied")
            self._apply_gate_outcome(run, outcome, record.ref)
        else:
            self._apply_gate_outcome(run, outcome, declared.decision_right)
        return outcome, record

    def record_human_work(self, run: WorkflowRun, work_item, requirement,
                          completion: HumanWorkCompletion) -> GateInstance:
        item = self._bound_item(run, work_item)
        instance = self._bound_gate(run, item, requirement)
        self.validate_evidence(run, item, instance, completion, completion.outcome)
        self._store(run, "human_work").add(completion)
        return self._resolve_gate(run, instance, completion.outcome, completion.human_work)

    def record_prerequisite(self, run: WorkflowRun, work_item, requirement,
                            evidence: PrerequisiteEvidence) -> GateInstance:
        item = self._bound_item(run, work_item)
        instance = self._bound_gate(run, item, requirement)
        self.validate_evidence(run, item, instance, evidence, evidence.outcome)
        self._store(run, "prerequisites").add(evidence)
        return self._resolve_gate(run, instance, evidence.outcome, evidence.prerequisite)

    # ---------------------------------------------------------------- retry

    def retry(self, run: WorkflowRun, work_item, *,
              acknowledgement: Optional[HumanInterventionRecord] = None,
              revalidated: bool = False) -> RunPhase:
        """Retry according to the retry class bound to the WORK ITEM, and no further.

        The class comes from the lineage the Work Item was created under. A caller who presents
        a substitute Task claiming a friendlier class changes nothing: the argument is not
        consulted, because there is no argument."""
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
        require(intervention.by, HumanAuthorityRef, "intervention")
        if intervention.run != run.ref:
            raise LineageError("the intervention names another run")
        self._store(run, "interventions").add(intervention)
        self.log.append(run.ref, "intervention:recorded", intervention.act, intervention.ref)
        return intervention

    def pause(self, run: WorkflowRun, intervention: HumanInterventionRecord) -> WorkflowRun:
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
            self.record_intervention(run, intervention)
        state.terminal = outcome
        self.log.append(run.ref, "terminal:%s" % outcome.value, cause)
        return run
