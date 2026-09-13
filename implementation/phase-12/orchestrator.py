"""Phase 12 MVP — the reference orchestrator.

Status: PROPOSED (implementation-equivalent non-approved status).

The orchestrator coordinates. It detects that a gate applies, creates the governed request,
records the outcome by reference, and moves the run between states the approved table allows.

It does none of the following, and each is a raise rather than a convention:

* infer or manufacture approval;
* act as reviewer, Decision Right holder or signatory;
* accept risk or canonicalise knowledge;
* choose a model, or relax a routing constraint;
* substitute a model result for a human gate;
* cross a scope without an approved transfer or handoff;
* rewrite recorded history;
* retry a non-replayable governed act automatically;
* treat a timeout, a deferral or an operational success as governance completion.

Every state change goes through `_transition`, which is the only place Axis A moves.
"""

from typing import Dict, Optional, Tuple

from adapters import (
    DecisionAuthorityAdapter, ModelAdapter, ReviewerAdapter, RouterAdapter,
)
from domain import (
    ALLOWED_TRANSITIONS, AUTOMATICALLY_RETRYABLE, Assignment, CONTINUING_GATE_OUTCOMES,
    DecisionRecord, DecisionRequest, DecisionRightRef, ExecutionEventLog, GateKind,
    GateOutcome, GateRequirement, GateState, GovernanceError, GovernancePosture,
    HumanAuthorityRef, HumanInterventionRecord, ModelInvocationRequest, ModelResult,
    NEVER_AUTOMATICALLY_RETRYABLE, POSTURE_PERMITS_COMPLETION, NON_COMPLETION_TERMINALS, Ref,
    ReviewInstance, ReviewProfileRef, ReviewRequest, RetryClass, RoleRef, RouterOutcome,
    RoutingDecision, RoutingRequest, RunPhase, ScopeBinding, ScopeTransferRef, HandoffRef,
    Task, TERMINAL_REACHABLE_FROM, TerminalOutcome, TransitionError, WaitReason,
    WorkItem, WorkItemRef, WorkflowDefinition, WorkflowRun, WorkflowRunRef, require,
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
        self._serial = 0

    # ---------------------------------------------------------------- state transitions

    def _transition(self, run: WorkflowRun, phase: RunPhase, *, detail: str = "",
                    wait_reason: Optional[WaitReason] = None,
                    wait_subject: Optional[Ref] = None) -> WorkflowRun:
        """The only place Axis A moves. Validated against the approved table."""
        if run.is_terminal:
            raise TransitionError("run %s is terminal as %s and cannot move again"
                                  % (run.ref, run.terminal.value))
        if phase not in ALLOWED_TRANSITIONS[run.phase]:
            raise TransitionError("%s -> %s is not an approved transition"
                                  % (run.phase.value, phase.value))
        if phase is RunPhase.WAITING:
            # A wait with no named subject is a defect: it cannot be told from a stall.
            if wait_reason is None or wait_subject is None:
                raise GovernanceError("a WAITING run must name its reason and its subject")
        run.phase = phase
        run.wait_reason = wait_reason if phase is RunPhase.WAITING else None
        run.wait_subject = wait_subject if phase is RunPhase.WAITING else None
        self.log.append(run.ref, "phase:%s" % phase.value, detail, wait_subject)
        return run

    def _ensure_phase(self, run: WorkflowRun, phase: RunPhase, **kwargs) -> WorkflowRun:
        """Move to `phase`, or stay there if the run is already in it.

        The approved table has no self-transitions, and a run that is already WAITING on the
        gate it just asked about has not moved: re-recording the wait keeps the named subject
        current without inventing a transition the architecture does not list."""
        if run.phase is phase:
            if phase is RunPhase.WAITING:
                run.wait_reason = kwargs.get("wait_reason", run.wait_reason)
                run.wait_subject = kwargs.get("wait_subject", run.wait_subject)
                self.log.append(run.ref, "wait:still", kwargs.get("detail", ""),
                                run.wait_subject)
            return run
        return self._transition(run, phase, **kwargs)

    def _set_posture(self, run: WorkflowRun, posture: GovernancePosture, detail: str = ""):
        run.posture = posture
        self.log.append(run.ref, "posture:%s" % posture.value, detail)

    # ---------------------------------------------------------------- run creation and scope

    def create_run(self, definition: WorkflowDefinition, run_ref: WorkflowRunRef,
                   scope: Optional[ScopeBinding] = None) -> WorkflowRun:
        """Create a run from a governed definition, bound to exactly one scope."""
        require(run_ref, WorkflowRunRef, "run creation")
        binding = scope or definition.scope
        if binding is not definition.scope and not definition.scope.narrows_to(binding):
            raise GovernanceError(
                "a run may narrow the definition's scope, never widen it")
        run = WorkflowRun(run_ref, definition.ref, definition.version, binding)
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
        if not parent.scope.narrows_to(scope):
            raise GovernanceError(
                "a sub-run may narrow the parent scope, never widen it: %s is not within %s"
                % (sorted(scope.sensitivity), sorted(parent.scope.sensitivity)))
        return self.create_run(definition, run_ref, scope)

    def cross_scope(self, run: WorkflowRun, target: ScopeBinding,
                    mechanism: Optional[Ref] = None) -> WorkflowRun:
        """Crossing a scope requires an approved Phase 6 handoff or Phase 8 scope transfer.

        There is no argument that makes this happen without one, and no default."""
        if type(mechanism) not in (HandoffRef, ScopeTransferRef):
            self._transition(run, RunPhase.BLOCKED,
                             detail="scope crossing without an approved mechanism")
            self._set_posture(run, GovernancePosture.GATE_UNSATISFIED,
                              "no approved transfer or handoff")
            raise GovernanceError(
                "crossing a scope boundary requires an approved handoff or scope transfer")
        run.scope = target
        self.log.append(run.ref, "scope:transferred", str(target.scope), mechanism)
        return run

    # ---------------------------------------------------------------- stages and assignment

    def activate_stage(self, run: WorkflowRun, task: Task) -> WorkItem:
        """Create the Work Item for a Task. The Task itself is never edited by a run."""
        if run.phase in (RunPhase.READY, RunPhase.WAITING, RunPhase.BLOCKED,
                         RunPhase.ESCALATED, RunPhase.RETRY_PENDING,
                         RunPhase.REWORK_REQUIRED, RunPhase.PAUSED):
            self._transition(run, RunPhase.RUNNING, detail="stage activation")
        elif run.phase is not RunPhase.RUNNING:
            raise TransitionError("a stage cannot be activated from %s" % run.phase.value)
        self._serial += 1
        item = WorkItem(WorkItemRef("wi-%d" % self._serial), task.ref, run.ref)
        run.work_items[item.ref.id] = item
        run.attempts[item.ref.id] = 0
        for requirement in task.gates:
            run.gates[(item.ref.id, requirement.kind.value)] = GateState(item.ref,
                                                                        requirement.kind)
        self.log.append(run.ref, "stage:activated", task.name, item.ref)
        return item

    def assign(self, run: WorkflowRun, item: WorkItem, task: Task, role: RoleRef,
               agent_instance=None) -> Assignment:
        """Bind a Role - and where permitted an Agent Instance - to a Work Item.

        The assignment grants no authority beyond doing the work: it does not make the
        assignee a reviewer and it does not make them a Decision Right holder."""
        require(role, RoleRef, "assignment")
        if role != task.required_role:
            raise GovernanceError("%s is not the Role the task requires (%s)"
                                  % (role, task.required_role))
        run.attempts[item.ref.id] = run.attempts.get(item.ref.id, 0) + 1
        assignment = Assignment(item.ref, role, agent_instance,
                                attempt=run.attempts[item.ref.id])
        run.assignments[item.ref.id] = assignment
        self.log.append(run.ref, "assignment:created",
                        "attempt %d" % assignment.attempt, item.ref)
        return assignment

    # ---------------------------------------------------------------- routing

    def request_routing(self, run: WorkflowRun, item: WorkItem, task: Task,
                        routing_policy: str) -> RoutingRequest:
        """Create the Routing Request. The orchestrator may not choose the model."""
        request = RoutingRequest(item.ref, task.capability, run.scope, routing_policy)
        self.log.append(run.ref, "routing:requested", task.capability, item.ref)
        return request

    def record_routing_decision(self, run: WorkflowRun,
                                decision: RoutingDecision) -> RoutingDecision:
        """Record the Router's answer by reference, and let it have its declared run effect."""
        if not isinstance(decision, RoutingDecision):
            raise GovernanceError("only a Routing Decision can be recorded as routing")
        run.routing_decisions[decision.request_work_item.id] = decision
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

    def route(self, run: WorkflowRun, item: WorkItem, task: Task,
              routing_policy: str) -> RoutingDecision:
        """Ask, then record. Request and decision stay two objects, by two parties."""
        request = self.request_routing(run, item, task, routing_policy)
        return self.record_routing_decision(run, self.router.route(request))

    # ---------------------------------------------------------------- model execution

    def invoke_model(self, run: WorkflowRun, item: WorkItem,
                     decision: RoutingDecision, prompt_context: str = "") -> ModelResult:
        """Execute the model the Routing Decision selected. Its output is a suggestion."""
        if decision.outcome is not RouterOutcome.ELIGIBLE_CANDIDATE:
            raise GovernanceError("no eligible candidate was selected; there is nothing to run")
        request = ModelInvocationRequest(item.ref, decision.ref, decision.model, prompt_context)
        result = self.model.execute(request)
        run.model_results[item.ref.id] = result
        self.log.append(run.ref, "model:result",
                        "%s / %s" % (result.origin.value, result.canonicality.value),
                        decision.ref)
        return result

    # ---------------------------------------------------------------- gates

    def _record_gate(self, run: WorkflowRun, item: WorkItem, kind: GateKind,
                     outcome: GateOutcome, satisfied_by: Optional[Ref]) -> GateState:
        state = GateState(item.ref, kind, outcome, satisfied_by)
        run.gates[(item.ref.id, kind.value)] = state
        self.log.append(run.ref, "gate:%s" % kind.value, outcome.value, satisfied_by)
        return state

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
            self._set_posture(run, GovernancePosture.GATE_UNSATISFIED, "escalated, not approved")
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

    def run_review_gate(self, run: WorkflowRun, item: WorkItem,
                        requirement: GateRequirement,
                        independence_class: str = "INDEPENDENT") -> ReviewInstance:
        """Detect, request, record. The orchestrator is not the reviewer."""
        require(requirement.review_profile, ReviewProfileRef, "review gate")
        request = ReviewRequest(item.ref, requirement.review_profile, independence_class)
        self._transition(run, RunPhase.WAITING, detail="review requested",
                         wait_reason=WaitReason.WAITING_FOR_REVIEW,
                         wait_subject=requirement.review_profile)
        instance = self.reviewers.review(request)
        run.review_instances[item.ref.id] = instance
        self._record_gate(run, item, GateKind.REVIEW, instance.outcome, instance.ref)
        if instance.outcome in CONTINUING_GATE_OUTCOMES:
            self._transition(run, RunPhase.RUNNING, detail="review satisfied")
            self._apply_gate_outcome(run, instance.outcome, instance.ref)
        else:
            self._apply_gate_outcome(run, instance.outcome, instance.ref)
        return instance

    def run_decision_gate(self, run: WorkflowRun, item: WorkItem,
                          requirement: GateRequirement) -> Tuple[GateOutcome,
                                                                 Optional[DecisionRecord]]:
        """Detect, name the Right, request, record. The orchestrator is not the decider."""
        require(requirement.decision_right, DecisionRightRef, "decision gate")
        request = DecisionRequest(item.ref, requirement.decision_right)
        self._transition(run, RunPhase.WAITING, detail="decision requested",
                         wait_reason=WaitReason.WAITING_FOR_DECISION,
                         wait_subject=requirement.decision_right)
        outcome, record = self.decisions.decide(request)
        if record is not None:
            if record.decision_right != requirement.decision_right:
                raise GovernanceError("a Decision Record must answer the Right that was named")
            run.decision_records[item.ref.id] = record
        self._record_gate(run, item, GateKind.DECISION, outcome,
                          record.ref if record is not None else None)
        if outcome in CONTINUING_GATE_OUTCOMES:
            self._transition(run, RunPhase.RUNNING, detail="decision satisfied")
            self._apply_gate_outcome(run, outcome, record.ref)
        else:
            self._apply_gate_outcome(run, outcome, requirement.decision_right)
        return outcome, record

    def satisfy_gate_with(self, run: WorkflowRun, item: WorkItem, kind: GateKind,
                          evidence) -> GateState:
        """Record a gate as satisfied by a named governed object, and nothing else.

        A model result, a routing decision, an assignment or an elapsed timer offered here is
        refused: only the object the gate's owning phase produces can satisfy it."""
        if kind is GateKind.REVIEW and not isinstance(evidence, ReviewInstance):
            raise GovernanceError("a review gate is satisfied only by a Review Instance")
        if kind is GateKind.DECISION and not isinstance(evidence, DecisionRecord):
            raise GovernanceError("a decision gate is satisfied only by a Decision Record")
        if isinstance(evidence, ModelResult):
            raise GovernanceError("a model result satisfies no gate")
        if evidence.outcome not in CONTINUING_GATE_OUTCOMES:
            raise GovernanceError("%s does not satisfy a gate" % evidence.outcome.value)
        return self._record_gate(run, item, kind, evidence.outcome, evidence.ref)

    # ---------------------------------------------------------------- retry

    def retry(self, run: WorkflowRun, item: WorkItem, task: Task, *,
              acknowledgement: Optional[HumanInterventionRecord] = None,
              revalidated: bool = False) -> RunPhase:
        """Retry according to the task's approved retry class, and no further.

        Classes 4 and 6 are never re-executed automatically. Class 3 waits for a recorded human
        acknowledgement. Class 2 is re-executed only after preconditions are re-checked."""
        cls = task.retry_class
        if cls in NEVER_AUTOMATICALLY_RETRYABLE:
            self._transition(run, RunPhase.BLOCKED,
                             detail="%s is never retried automatically" % cls.value)
            self._transition(run, RunPhase.ESCALATED, detail="compensation is a new act")
            self._set_posture(run, GovernancePosture.GATE_UNSATISFIED,
                              "recovery requires a separately authorised act")
            return run.phase
        if cls is RetryClass.RETRY_REQUIRING_HUMAN_ACKNOWLEDGEMENT:
            if acknowledgement is None:
                self._transition(run, RunPhase.WAITING, detail="retry needs acknowledgement",
                                 wait_reason=WaitReason.WAITING_FOR_HUMAN,
                                 wait_subject=item.ref)
                return run.phase
            run.interventions.append(acknowledgement)
            self.log.append(run.ref, "intervention:acknowledged", acknowledgement.reason,
                            acknowledgement.ref)
        if cls is RetryClass.RETRY_REQUIRING_REVALIDATION and not revalidated:
            raise GovernanceError(
                "%s must re-check preconditions, evidence freshness, scope, sensitivity and "
                "assignment eligibility before the retry" % cls.value)
        # RETRY_PENDING is reachable only from RUNNING in the approved table. From any other
        # permitted phase the retry is dispatched directly, rather than inventing a hop.
        if run.phase is RunPhase.RUNNING:
            self._transition(run, RunPhase.RETRY_PENDING, detail="retry scheduled")
        self._ensure_phase(run, RunPhase.RUNNING, detail="retry dispatched")
        self.log.append(run.ref, "retry:dispatched", cls.value, item.ref)
        return run.phase

    # ---------------------------------------------------------------- human intervention

    def record_intervention(self, run: WorkflowRun,
                            intervention: HumanInterventionRecord) -> HumanInterventionRecord:
        """A human act on the run. The human is recorded first; automation refuses after."""
        require(intervention.by, HumanAuthorityRef, "intervention")
        run.interventions.append(intervention)
        self.log.append(run.ref, "intervention:recorded", intervention.act, intervention.ref)
        return intervention

    def pause(self, run: WorkflowRun, intervention: HumanInterventionRecord) -> WorkflowRun:
        self.record_intervention(run, intervention)
        return self._transition(run, RunPhase.PAUSED, detail=intervention.reason)

    # ---------------------------------------------------------------- completion

    def unsatisfied_gates(self, run: WorkflowRun):
        return [state for state in run.gates.values() if not state.is_continuing()]

    def complete(self, run: WorkflowRun, outcome: TerminalOutcome,
                 *, cause: str = "",
                 intervention: Optional[HumanInterventionRecord] = None) -> WorkflowRun:
        """Reach a terminal outcome, only where the governance posture permits it.

        Completion is not approval and approval is not completion: a run whose posture is
        `GATE_UNSATISFIED` or `AUTHORITY_ABSENT` cannot complete at all, however successful the
        operational work was."""
        if run.is_terminal:
            raise TransitionError("run %s is already terminal" % run.ref)
        if run.phase not in TERMINAL_REACHABLE_FROM[outcome]:
            raise TransitionError("%s is not reachable from %s"
                                  % (outcome.value, run.phase.value))
        if outcome in NON_COMPLETION_TERMINALS:
            if outcome is TerminalOutcome.CANCELLED and intervention is None:
                raise GovernanceError("CANCELLED requires an intervention record")
            if outcome is TerminalOutcome.TERMINATED and not cause:
                raise GovernanceError("TERMINATED requires a named constraint")
            if outcome is TerminalOutcome.FAILED and not cause:
                raise GovernanceError("FAILED requires a recorded cause")
        else:
            permitted = POSTURE_PERMITS_COMPLETION[run.posture]
            if outcome not in permitted:
                raise GovernanceError(
                    "posture %s does not permit %s" % (run.posture.value, outcome.value))
            outstanding = self.unsatisfied_gates(run)
            if outstanding:
                raise GovernanceError(
                    "%d gate(s) are not satisfied; completion is not available"
                    % len(outstanding))
        if intervention is not None:
            self.record_intervention(run, intervention)
        run.terminal = outcome
        self.log.append(run.ref, "terminal:%s" % outcome.value, cause)
        return run
