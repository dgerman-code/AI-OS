"""Phase 12 MVP — governed domain objects.

Status: PROPOSED (implementation-equivalent non-approved status).

This module is the structured-data layer of the Phase 12 MVP. Its job is to make the
Phase 1-11 governance model *representable* and to make the collapses the architecture denies
*unrepresentable*, so that assurance stops depending on reading prose.

Two design rules run through the whole file.

1. **Every governed identity is its own type.** The twenty-one-object separation chain is not a
   naming convention here; a `RoleRef` and an `AgentInstanceRef` carrying the same string are
   different objects and cannot be substituted for one another. `require()` raises rather than
   coercing.
2. **Authority is never inferred.** Nothing in this module derives an approval, a review
   outcome or a Decision Record from anything else. Those objects exist only when a governed
   party creates them, and the orchestrator records them by reference.

Standard library only. No provider SDK, no I/O, no clock of its own.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, FrozenSet, List, Optional, Sequence, Tuple


# ===========================================================================================
# Errors
# ===========================================================================================


class GovernanceError(Exception):
    """An act the approved architecture does not permit."""


class IdentityError(GovernanceError):
    """One governed identity was offered where another is required."""


class TransitionError(GovernanceError):
    """A run-phase transition the approved state machine does not allow."""


class AppendOnlyError(GovernanceError):
    """An attempt to rewrite recorded history."""


# ===========================================================================================
# Identity references - the twenty-one-object separation, as types
# ===========================================================================================


@dataclass(frozen=True)
class Ref:
    """A governed identity reference.

    Subclasses differ by KIND, and equality includes the type, so a Role reference is never
    equal to an Agent Instance reference even when both carry the same id string."""

    id: str

    KIND = "ref"

    def __post_init__(self):
        if not self.id or not isinstance(self.id, str):
            raise IdentityError("a %s reference needs a non-empty id" % self.KIND)

    def __str__(self):
        return "%s:%s" % (self.KIND, self.id)


class RoleRef(Ref):
    KIND = "role"


class AgentInstanceRef(Ref):
    KIND = "agent_instance"


class ModelRef(Ref):
    KIND = "model"


class ModelProfileRef(Ref):
    KIND = "model_profile"


class RouterRef(Ref):
    KIND = "router"


class OrchestratorRef(Ref):
    KIND = "orchestrator"


class WorkflowRef(Ref):
    KIND = "workflow"


class WorkflowRunRef(Ref):
    KIND = "workflow_run"


class TaskRef(Ref):
    KIND = "task"


class WorkItemRef(Ref):
    KIND = "work_item"


class HandoffRef(Ref):
    KIND = "handoff"


class ReviewProfileRef(Ref):
    KIND = "review_profile"


class ReviewInstanceRef(Ref):
    KIND = "review_instance"


class DecisionRightRef(Ref):
    KIND = "decision_right"


class DecisionRecordRef(Ref):
    KIND = "decision_record"


class KnowledgeRef(Ref):
    KIND = "knowledge"


class CanonicalRecordRef(Ref):
    KIND = "canonical_record"


class ArtifactRef(Ref):
    KIND = "artifact"


class StorageRecordRef(Ref):
    KIND = "storage_record"


class RuntimeEventRef(Ref):
    KIND = "runtime_event"


class CredentialRef(Ref):
    KIND = "credential"


class HumanAuthorityRef(Ref):
    KIND = "human_authority"


class ScopeRef(Ref):
    KIND = "scope"


class RoutingDecisionRef(Ref):
    KIND = "routing_decision"


class ScopeTransferRef(Ref):
    KIND = "scope_transfer"


class InterventionRef(Ref):
    KIND = "intervention"


#: The approved separation chain, in order, as the types that carry it.
SEPARATION_CHAIN: Tuple[type, ...] = (
    RoleRef, AgentInstanceRef, ModelRef, ModelProfileRef, RouterRef, OrchestratorRef,
    WorkflowRef, WorkflowRunRef, TaskRef, HandoffRef, ReviewProfileRef, ReviewInstanceRef,
    DecisionRightRef, DecisionRecordRef, KnowledgeRef, CanonicalRecordRef, ArtifactRef,
    StorageRecordRef, RuntimeEventRef, CredentialRef, HumanAuthorityRef,
)


def require(value, expected: type, what: str = ""):
    """Return `value` if it is exactly `expected`, else raise.

    Deliberately not `isinstance`-with-subclassing-slack: the separation is the point, and a
    reference that merely resembles the required one is the collapse the architecture denies."""
    if type(value) is not expected:
        raise IdentityError(
            "%s requires %s, got %s"
            % (what or expected.KIND, expected.KIND,
               getattr(type(value), "KIND", type(value).__name__)))
    return value


# ===========================================================================================
# The four orthogonal state axes
# ===========================================================================================


class RunPhase(Enum):
    """Axis A - where the execution is. Exactly one at a time, from ten."""

    CREATED = "CREATED"
    VALIDATING = "VALIDATING"
    READY = "READY"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    PAUSED = "PAUSED"
    RETRY_PENDING = "RETRY_PENDING"
    REWORK_REQUIRED = "REWORK_REQUIRED"
    BLOCKED = "BLOCKED"
    ESCALATED = "ESCALATED"


class TerminalOutcome(Enum):
    """Axis B - how it ended. Absent before terminal, exactly one once terminal."""

    COMPLETED = "COMPLETED"
    COMPLETED_WITH_OPEN_ITEMS = "COMPLETED_WITH_OPEN_ITEMS"
    CANCELLED = "CANCELLED"
    TERMINATED = "TERMINATED"
    FAILED = "FAILED"
    SUPERSEDED = "SUPERSEDED"


class WaitReason(Enum):
    """Axis C - present only while WAITING, and never without a named subject."""

    WAITING_FOR_DEPENDENCY = "WAITING_FOR_DEPENDENCY"
    WAITING_FOR_REVIEW = "WAITING_FOR_REVIEW"
    WAITING_FOR_DECISION = "WAITING_FOR_DECISION"
    WAITING_FOR_HUMAN = "WAITING_FOR_HUMAN"
    WAITING_FOR_EXTERNAL_EVENT = "WAITING_FOR_EXTERNAL_EVENT"


class GovernancePosture(Enum):
    """Axis D - always present, and the only thing that permits a terminal outcome."""

    GOVERNANCE_CLEAR = "GOVERNANCE_CLEAR"
    OPEN_ITEMS_CARRIED = "OPEN_ITEMS_CARRIED"
    GATE_UNSATISFIED = "GATE_UNSATISFIED"
    AUTHORITY_ABSENT = "AUTHORITY_ABSENT"


#: Which terminal outcome each posture permits. `GATE_UNSATISFIED` and `AUTHORITY_ABSENT`
#: permit no completion at all - that is the whole point of the axis.
POSTURE_PERMITS_COMPLETION: Dict[GovernancePosture, FrozenSet[TerminalOutcome]] = {
    GovernancePosture.GOVERNANCE_CLEAR: frozenset({TerminalOutcome.COMPLETED}),
    GovernancePosture.OPEN_ITEMS_CARRIED: frozenset({TerminalOutcome.COMPLETED_WITH_OPEN_ITEMS}),
    GovernancePosture.GATE_UNSATISFIED: frozenset(),
    GovernancePosture.AUTHORITY_ABSENT: frozenset(),
}

#: Terminal outcomes that are stops rather than completions. They are reachable under any
#: posture, because stopping is always permitted; only *completing* is governed.
NON_COMPLETION_TERMINALS: FrozenSet[TerminalOutcome] = frozenset({
    TerminalOutcome.CANCELLED, TerminalOutcome.TERMINATED,
    TerminalOutcome.FAILED, TerminalOutcome.SUPERSEDED,
})

#: Axis A transitions, exactly as approved in
#: `orchestration/state-machine-and-transitions.md` section 6.
ALLOWED_TRANSITIONS: Dict[RunPhase, FrozenSet[RunPhase]] = {
    RunPhase.CREATED: frozenset({RunPhase.VALIDATING}),
    RunPhase.VALIDATING: frozenset({RunPhase.READY, RunPhase.BLOCKED}),
    RunPhase.READY: frozenset({RunPhase.RUNNING, RunPhase.WAITING, RunPhase.PAUSED,
                               RunPhase.BLOCKED}),
    RunPhase.RUNNING: frozenset({RunPhase.WAITING, RunPhase.PAUSED, RunPhase.RETRY_PENDING,
                                 RunPhase.REWORK_REQUIRED, RunPhase.BLOCKED,
                                 RunPhase.ESCALATED}),
    RunPhase.WAITING: frozenset({RunPhase.RUNNING, RunPhase.REWORK_REQUIRED, RunPhase.BLOCKED,
                                 RunPhase.ESCALATED, RunPhase.PAUSED}),
    RunPhase.PAUSED: frozenset({RunPhase.RUNNING, RunPhase.READY}),
    RunPhase.RETRY_PENDING: frozenset({RunPhase.RUNNING, RunPhase.BLOCKED,
                                       RunPhase.ESCALATED}),
    RunPhase.REWORK_REQUIRED: frozenset({RunPhase.RUNNING, RunPhase.BLOCKED,
                                         RunPhase.ESCALATED}),
    RunPhase.BLOCKED: frozenset({RunPhase.RUNNING, RunPhase.WAITING, RunPhase.ESCALATED}),
    RunPhase.ESCALATED: frozenset({RunPhase.RUNNING, RunPhase.WAITING, RunPhase.BLOCKED,
                                   RunPhase.REWORK_REQUIRED}),
}

#: Phases from which each terminal outcome may be reached, from the same table. Terminal
#: outcomes are held separately from Axis A because they are a different axis.
TERMINAL_REACHABLE_FROM: Dict[TerminalOutcome, FrozenSet[RunPhase]] = {
    TerminalOutcome.COMPLETED: frozenset({RunPhase.RUNNING}),
    TerminalOutcome.COMPLETED_WITH_OPEN_ITEMS: frozenset({RunPhase.RUNNING}),
    TerminalOutcome.CANCELLED: frozenset({RunPhase.CREATED, RunPhase.READY, RunPhase.RUNNING,
                                          RunPhase.WAITING, RunPhase.PAUSED,
                                          RunPhase.RETRY_PENDING, RunPhase.REWORK_REQUIRED,
                                          RunPhase.BLOCKED, RunPhase.ESCALATED}),
    TerminalOutcome.TERMINATED: frozenset({RunPhase.VALIDATING, RunPhase.RUNNING,
                                           RunPhase.WAITING, RunPhase.PAUSED,
                                           RunPhase.REWORK_REQUIRED, RunPhase.BLOCKED,
                                           RunPhase.ESCALATED}),
    TerminalOutcome.FAILED: frozenset({RunPhase.RUNNING, RunPhase.RETRY_PENDING}),
    TerminalOutcome.SUPERSEDED: frozenset({RunPhase.RUNNING, RunPhase.WAITING,
                                           RunPhase.PAUSED}),
}


# ===========================================================================================
# Gates, routing, retry and races
# ===========================================================================================


class GateKind(Enum):
    REVIEW = "REVIEW"
    DECISION = "DECISION"
    HUMAN_WORK = "HUMAN_WORK"
    GOVERNED_PREREQUISITE = "GOVERNED_PREREQUISITE"


class GateOutcome(Enum):
    """Seven outcomes, none of which collapse into approval."""

    SATISFIED = "SATISFIED"
    SATISFIED_WITH_OPEN_ITEMS = "SATISFIED_WITH_OPEN_ITEMS"
    NOT_SATISFIED = "NOT_SATISFIED"
    DEFER = "DEFER"
    ESCALATE = "ESCALATE"
    EXPIRED = "EXPIRED"
    NO_APPLICABLE_DECISION_RIGHT = "NO_APPLICABLE_DECISION_RIGHT"


#: The only two outcomes that let a run continue past a gate. Everything else - a deferral, an
#: escalation, an expiry, an absent Right - is explicitly not an approval.
CONTINUING_GATE_OUTCOMES: FrozenSet[GateOutcome] = frozenset({
    GateOutcome.SATISFIED, GateOutcome.SATISFIED_WITH_OPEN_ITEMS,
})


class RouterOutcome(Enum):
    ELIGIBLE_CANDIDATE = "ELIGIBLE_CANDIDATE"
    NO_ELIGIBLE_MODEL = "NO_ELIGIBLE_MODEL"
    CANDIDATE_UNIVERSE_INCOMPLETE = "CANDIDATE_UNIVERSE_INCOMPLETE"
    NO_APPLICABLE_DECISION_RIGHT = "NO_APPLICABLE_DECISION_RIGHT"


class RetryClass(Enum):
    """Seven classes. Exactly-once is claimed nowhere."""

    SAFE_AUTOMATIC_RETRY = "SAFE_AUTOMATIC_RETRY"
    RETRY_REQUIRING_REVALIDATION = "RETRY_REQUIRING_REVALIDATION"
    RETRY_REQUIRING_HUMAN_ACKNOWLEDGEMENT = "RETRY_REQUIRING_HUMAN_ACKNOWLEDGEMENT"
    NON_RETRYABLE_GOVERNED_ACT = "NON_RETRYABLE_GOVERNED_ACT"
    REPLAYABLE_READ_ONLY = "REPLAYABLE_READ_ONLY"
    NON_REPLAYABLE_EXTERNAL_SIDE_EFFECT = "NON_REPLAYABLE_EXTERNAL_SIDE_EFFECT"
    IDEMPOTENT_AT_LEAST_ONCE = "IDEMPOTENT_AT_LEAST_ONCE"


#: Classes the orchestrator may retry without a further governed act.
AUTOMATICALLY_RETRYABLE: FrozenSet[RetryClass] = frozenset({
    RetryClass.SAFE_AUTOMATIC_RETRY, RetryClass.RETRY_REQUIRING_REVALIDATION,
    RetryClass.REPLAYABLE_READ_ONLY, RetryClass.IDEMPOTENT_AT_LEAST_ONCE,
})

#: Classes that are never re-executed automatically, for two different reasons: a governed act
#: was performed once by a governed party, and an external effect already left the system.
NEVER_AUTOMATICALLY_RETRYABLE: FrozenSet[RetryClass] = frozenset({
    RetryClass.NON_RETRYABLE_GOVERNED_ACT,
    RetryClass.NON_REPLAYABLE_EXTERNAL_SIDE_EFFECT,
})


class RaceOutcome(Enum):
    BLOCK = "BLOCK"
    IGNORE_AS_STALE = "IGNORE_AS_STALE"
    SUPERSEDE = "SUPERSEDE"
    RECONCILE = "RECONCILE"
    ESCALATE = "ESCALATE"


class Origin(Enum):
    """Where a produced content came from. A model produces a suggestion, never canon."""

    AI_GENERATED = "AI_GENERATED"
    HUMAN_AUTHORED = "HUMAN_AUTHORED"


class Canonicality(Enum):
    AI_SUGGESTION = "AI_SUGGESTION"
    CANONICAL = "CANONICAL"


# ===========================================================================================
# Scope, sensitivity and residency
# ===========================================================================================


@dataclass(frozen=True)
class ScopeBinding:
    """Exactly one governed scope per execution, bound at intake.

    Sensitivity is an unordered multi-label set, as Phase 8 defines it: there is no ceiling to
    compare, so narrowing is subset containment and widening is anything else."""

    scope: ScopeRef
    sensitivity: FrozenSet[str]
    residency: str

    def __post_init__(self):
        require(self.scope, ScopeRef, "scope binding")
        if not isinstance(self.sensitivity, frozenset):
            raise GovernanceError("sensitivity must be an unordered label set")
        if not self.residency:
            raise GovernanceError("a scope binding needs a residency constraint")

    def narrows_to(self, other: "ScopeBinding") -> bool:
        """True when `other` is a narrowing of this binding, and only then."""
        return (other.scope == self.scope
                and other.sensitivity <= self.sensitivity
                and other.residency == self.residency)


# ===========================================================================================
# Definition-side objects
# ===========================================================================================


@dataclass(frozen=True)
class GateRequirement:
    """A gate the definition declares, named by the governed object that can satisfy it."""

    kind: GateKind
    review_profile: Optional[ReviewProfileRef] = None
    decision_right: Optional[DecisionRightRef] = None
    description: str = ""

    def __post_init__(self):
        if self.kind is GateKind.REVIEW and self.review_profile is None:
            raise GovernanceError("a review gate must name its Review Profile")
        if self.kind is GateKind.DECISION and self.decision_right is None:
            raise GovernanceError("a decision gate must name its Decision Right")
        if self.review_profile is not None:
            require(self.review_profile, ReviewProfileRef, "review gate")
        if self.decision_right is not None:
            require(self.decision_right, DecisionRightRef, "decision gate")


@dataclass(frozen=True)
class Task:
    """A unit of DEFINITION. Never edited by a run - editing it would rewrite the workflow."""

    ref: TaskRef
    name: str
    required_role: RoleRef
    retry_class: RetryClass
    gates: Tuple[GateRequirement, ...] = ()
    needs_model: bool = False
    capability: str = ""

    def __post_init__(self):
        require(self.ref, TaskRef, "task")
        require(self.required_role, RoleRef, "task role requirement")


@dataclass(frozen=True)
class WorkflowDefinition:
    """A governed, versioned definition. A run executes it; it never mutates."""

    ref: WorkflowRef
    version: str
    tasks: Tuple[Task, ...]
    scope: ScopeBinding

    def __post_init__(self):
        require(self.ref, WorkflowRef, "workflow definition")
        if not self.version:
            raise GovernanceError("a workflow definition must be versioned")
        if not self.tasks:
            raise GovernanceError("a workflow definition needs at least one task")


# ===========================================================================================
# Run-side objects
# ===========================================================================================


@dataclass(frozen=True)
class WorkItem:
    """A unit of ASSIGNMENT, created by a run from a Task. Distinct from the Task itself."""

    ref: WorkItemRef
    task: TaskRef
    run: WorkflowRunRef

    def __post_init__(self):
        require(self.ref, WorkItemRef, "work item")
        require(self.task, TaskRef, "work item task")
        require(self.run, WorkflowRunRef, "work item run")


@dataclass(frozen=True)
class Assignment:
    """One attempt to bind a Role - and, where permitted, an Agent Instance - to a Work Item.

    An assignment carries no authority of its own. It does not make its holder a reviewer and
    it does not make them a Decision Right holder; both of those are separate governed objects
    naming separate parties."""

    work_item: WorkItemRef
    role: RoleRef
    agent_instance: Optional[AgentInstanceRef] = None
    attempt: int = 1
    valid: bool = True

    def __post_init__(self):
        require(self.work_item, WorkItemRef, "assignment")
        require(self.role, RoleRef, "assignment role")
        if self.agent_instance is not None:
            require(self.agent_instance, AgentInstanceRef, "assignment agent instance")

    # An assignment grants no review or decision authority. These are methods rather than
    # comments so the property is testable rather than merely asserted.
    def grants_review_authority(self) -> bool:
        return False

    def grants_decision_authority(self) -> bool:
        return False


@dataclass(frozen=True)
class AgentInstance:
    """A running execution of work under a Role. Not the Role, and not a persona."""

    ref: AgentInstanceRef
    role: RoleRef
    run: WorkflowRunRef

    def __post_init__(self):
        require(self.ref, AgentInstanceRef, "agent instance")
        require(self.role, RoleRef, "agent instance role")
        require(self.run, WorkflowRunRef, "agent instance run")


@dataclass(frozen=True)
class RoutingRequest:
    """What the orchestrator may ask the Router.

    It carries requirements and constraints. It carries no chosen model, no relaxed constraint
    and no pre-filtered candidate set - those would make the orchestrator the Router."""

    work_item: WorkItemRef
    capability: str
    scope: ScopeBinding
    routing_policy: str
    independence_class: str = ""

    def __post_init__(self):
        require(self.work_item, WorkItemRef, "routing request")
        if not self.capability:
            raise GovernanceError("a routing request must declare a capability requirement")
        if not self.routing_policy:
            raise GovernanceError("a routing request must name its routing policy at version")


@dataclass(frozen=True)
class RoutingDecision:
    """What the Router returns. A different object from the request, by a different party."""

    ref: RoutingDecisionRef
    request_work_item: WorkItemRef
    outcome: RouterOutcome
    model: Optional[ModelRef] = None
    model_profile: Optional[ModelProfileRef] = None
    decided_by: Optional[RouterRef] = None

    def __post_init__(self):
        require(self.ref, RoutingDecisionRef, "routing decision")
        if self.outcome is RouterOutcome.ELIGIBLE_CANDIDATE:
            require(self.model, ModelRef, "routing decision model")
            require(self.model_profile, ModelProfileRef, "routing decision model profile")
        elif self.model is not None:
            raise GovernanceError("a non-eligible routing outcome may not name a model")


@dataclass(frozen=True)
class ModelInvocationRequest:
    """A request to execute a model that a Routing Decision already selected.

    The orchestrator may not name the model itself; it passes the Routing Decision through."""

    work_item: WorkItemRef
    routing_decision: RoutingDecisionRef
    model: ModelRef
    prompt_context: str = ""

    def __post_init__(self):
        require(self.routing_decision, RoutingDecisionRef, "model invocation request")
        require(self.model, ModelRef, "model invocation request")


@dataclass(frozen=True)
class ModelResult:
    """Model output. Always a suggestion, never an approval and never canonical knowledge."""

    work_item: WorkItemRef
    model: ModelRef
    content: str
    origin: Origin = Origin.AI_GENERATED
    canonicality: Canonicality = Canonicality.AI_SUGGESTION

    def __post_init__(self):
        if self.origin is not Origin.AI_GENERATED:
            raise GovernanceError("a model result is AI_GENERATED by construction")
        if self.canonicality is not Canonicality.AI_SUGGESTION:
            raise GovernanceError("a model result is an AI_SUGGESTION, never canonical")

    def satisfies_gate(self) -> bool:
        """A model result satisfies no gate of any kind. Stated as code, not as prose."""
        return False


@dataclass(frozen=True)
class ReviewRequest:
    """The orchestrator's whole part in a review gate: detect, and ask."""

    work_item: WorkItemRef
    review_profile: ReviewProfileRef
    independence_class: str

    def __post_init__(self):
        require(self.review_profile, ReviewProfileRef, "review request")


@dataclass(frozen=True)
class ReviewInstance:
    """A review that happened, by a reviewer, under a Profile. Produced by Phase 6, not here."""

    ref: ReviewInstanceRef
    request_work_item: WorkItemRef
    review_profile: ReviewProfileRef
    outcome: GateOutcome
    reviewer: HumanAuthorityRef
    independence_class: str

    def __post_init__(self):
        require(self.ref, ReviewInstanceRef, "review instance")
        require(self.review_profile, ReviewProfileRef, "review instance profile")
        require(self.reviewer, HumanAuthorityRef, "review instance reviewer")


@dataclass(frozen=True)
class DecisionRequest:
    """The orchestrator's whole part in a decision gate: detect, name the Right, and ask."""

    work_item: WorkItemRef
    decision_right: DecisionRightRef
    question: str = ""

    def __post_init__(self):
        require(self.decision_right, DecisionRightRef, "decision request")


@dataclass(frozen=True)
class DecisionRecord:
    """A Right exercised by an eligible human. Produced by Phase 7, recorded here by reference.

    A Decision Record requires an explicit human authority reference. There is no path in this
    module that creates one from a model result, a timeout or an orchestrator inference."""

    ref: DecisionRecordRef
    request_work_item: WorkItemRef
    decision_right: DecisionRightRef
    outcome: GateOutcome
    decided_by: HumanAuthorityRef

    def __post_init__(self):
        require(self.ref, DecisionRecordRef, "decision record")
        require(self.decision_right, DecisionRightRef, "decision record right")
        require(self.decided_by, HumanAuthorityRef, "decision record human authority")


@dataclass(frozen=True)
class HumanInterventionRecord:
    """A human act on the run, recorded. Pauses, acknowledgements and cancellations."""

    ref: InterventionRef
    run: WorkflowRunRef
    by: HumanAuthorityRef
    act: str
    reason: str

    def __post_init__(self):
        require(self.ref, InterventionRef, "intervention")
        require(self.by, HumanAuthorityRef, "intervention authority")
        if not self.reason:
            raise GovernanceError("an intervention record must state a reason")


@dataclass(frozen=True)
class GateState:
    """The recorded state of one gate on one Work Item."""

    work_item: WorkItemRef
    kind: GateKind
    outcome: Optional[GateOutcome] = None
    satisfied_by: Optional[Ref] = None

    def is_continuing(self) -> bool:
        return self.outcome in CONTINUING_GATE_OUTCOMES


# ===========================================================================================
# Execution events - append-only by construction
# ===========================================================================================


@dataclass(frozen=True)
class ExecutionEvent:
    """One recorded fact about a run. Governance evidence, distinct from an operational log."""

    sequence: int
    run: WorkflowRunRef
    kind: str
    detail: str = ""
    reference: Optional[Ref] = None


class ExecutionEventLog:
    """Append-only history.

    There is no update, no delete and no reordering, and the exposed sequence is a copy, so a
    caller that mutates what it is given changes nothing that was recorded."""

    def __init__(self):
        self._events: List[ExecutionEvent] = []

    def append(self, run: WorkflowRunRef, kind: str, detail: str = "",
               reference: Optional[Ref] = None) -> ExecutionEvent:
        event = ExecutionEvent(len(self._events) + 1, run, kind, detail, reference)
        self._events.append(event)
        return event

    def events(self) -> Sequence[ExecutionEvent]:
        return tuple(self._events)

    def kinds(self) -> Tuple[str, ...]:
        return tuple(e.kind for e in self._events)

    def __len__(self) -> int:
        return len(self._events)

    def __setitem__(self, index, value):
        raise AppendOnlyError("execution history cannot be rewritten")

    def __delitem__(self, index):
        raise AppendOnlyError("execution history cannot be deleted")


# ===========================================================================================
# The run
# ===========================================================================================


@dataclass
class WorkflowRun:
    """One governed execution of one Workflow Definition at one version.

    The run holds the four axes. It does not transition itself: `orchestrator.py` owns the
    transitions so that every state change goes through one validated place."""

    ref: WorkflowRunRef
    workflow: WorkflowRef
    workflow_version: str
    scope: ScopeBinding
    phase: RunPhase = RunPhase.CREATED
    terminal: Optional[TerminalOutcome] = None
    wait_reason: Optional[WaitReason] = None
    wait_subject: Optional[Ref] = None
    posture: GovernancePosture = GovernancePosture.GOVERNANCE_CLEAR
    work_items: Dict[str, WorkItem] = field(default_factory=dict)
    assignments: Dict[str, Assignment] = field(default_factory=dict)
    gates: Dict[Tuple[str, str], GateState] = field(default_factory=dict)
    attempts: Dict[str, int] = field(default_factory=dict)
    decision_records: Dict[str, DecisionRecord] = field(default_factory=dict)
    review_instances: Dict[str, ReviewInstance] = field(default_factory=dict)
    routing_decisions: Dict[str, RoutingDecision] = field(default_factory=dict)
    model_results: Dict[str, ModelResult] = field(default_factory=dict)
    interventions: List[HumanInterventionRecord] = field(default_factory=list)

    def __post_init__(self):
        require(self.ref, WorkflowRunRef, "workflow run")
        require(self.workflow, WorkflowRef, "workflow run definition")

    @property
    def is_terminal(self) -> bool:
        return self.terminal is not None

    def axes(self) -> Tuple[RunPhase, Optional[TerminalOutcome], Optional[WaitReason],
                            GovernancePosture]:
        """The four axes, read together. Useful in tests, which assert on all four."""
        return (self.phase, self.terminal, self.wait_reason, self.posture)
