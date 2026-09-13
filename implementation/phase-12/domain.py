"""Phase 12 MVP — governed domain objects.

Status: PROPOSED (implementation-equivalent non-approved status).

This module is the structured-data layer of the Phase 12 MVP. Its job is to make the
Phase 1-11 governance model *representable* and to make the collapses the architecture denies
*unrepresentable*, so that assurance stops depending on reading prose.

Four design rules run through the file. The first two were there from the foundation; the last
two are the answer to the independent audit, which found that the first two were not enough on
their own because the reference layer still trusted whatever a caller handed it.

1. **Every governed identity is its own type.** A `RoleRef` and an `AgentInstanceRef` carrying
   the same string are different objects. `require()` raises rather than coercing.
2. **Authority is never inferred.** Nothing here derives an approval, a review outcome or a
   Decision Record from anything else.
3. **Every governed object validates its own references at construction.** Not when some
   downstream method happens to look: a malformed governed object never exists at all.
4. **Lineage is bound, not asserted.** A Work Item carries the definition, version, task and
   run it was created from, and every later act is checked against that binding rather than
   against an argument the caller passes at the time.

Standard library only. No provider SDK, no I/O, no clock of its own.
"""

import dataclasses
import collections.abc
import typing
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


class LineageError(GovernanceError):
    """An object was offered that does not belong to the governed lineage in hand."""


class EvidenceError(GovernanceError):
    """Evidence was offered that does not answer the requirement it was offered for."""


class MissingEvidenceError(EvidenceError):
    """A continuing outcome arrived with no governed record behind it.

    Its own class, because it is a different failure from evidence that is merely wrong: there
    is nothing to examine at all, and an approval with no record of a human exercising a Right
    is the single thing this phase exists to make impossible."""


class TransitionError(GovernanceError):
    """A run-phase transition the approved state machine does not allow."""


class AppendOnlyError(GovernanceError):
    """An attempt to rewrite recorded history."""


class StateAccessError(GovernanceError):
    """An attempt to change governed run state from outside the orchestrator."""


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


class RoutingRequestRef(Ref):
    KIND = "routing_request"


class ModelResultRef(Ref):
    KIND = "model_result"


class ScopeTransferRef(Ref):
    KIND = "scope_transfer"


class InterventionRef(Ref):
    KIND = "intervention"


class GateRequirementRef(Ref):
    KIND = "gate_requirement"


class HumanWorkRef(Ref):
    KIND = "human_work"


class PrerequisiteRef(Ref):
    KIND = "governed_prerequisite"


class GateInstanceRef(Ref):
    KIND = "gate_instance"


class HumanWorkRecordRef(Ref):
    KIND = "human_work_record"


class PrerequisiteRecordRef(Ref):
    KIND = "prerequisite_record"


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


_HINTS_CACHE: Dict[type, Dict[str, object]] = {}


def _unwrap_optional(annotation):
    """(annotation without NoneType, optional?)."""
    if typing.get_origin(annotation) is typing.Union:
        args = typing.get_args(annotation)
        named = [a for a in args if a is not type(None)]
        if len(named) == 1:
            return named[0], type(None) in args
    return annotation, False


def _describe(value) -> str:
    return getattr(type(value), "KIND", type(value).__name__)


def _check_value(where: str, annotation, value) -> None:
    """Check one value against one declared annotation, with no coercion anywhere.

    The audit's first finding, second pass: reference fields were validated and everything
    else was not, so a plain string could sit where a `GateOutcome` or a `ScopeBinding`
    belongs. Enums are matched exactly, structured governed values by their own class,
    containers element by element, and a plain `str` where an Enum is declared is exactly the
    case this exists to refuse."""
    annotation, optional = _unwrap_optional(annotation)
    if value is None:
        if optional:
            return
        raise IdentityError("%s requires %s, got nothing"
                            % (where, getattr(annotation, "__name__", annotation)))
    origin = typing.get_origin(annotation)
    if origin in (tuple, Tuple):
        args = typing.get_args(annotation)
        if not isinstance(value, tuple):
            raise IdentityError("%s requires a tuple, got %s" % (where, _describe(value)))
        if args and args[-1] is Ellipsis:
            for index, element in enumerate(value):
                _check_value("%s[%d]" % (where, index), args[0], element)
        elif args:
            if len(args) != len(value):
                raise IdentityError("%s requires %d elements, got %d"
                                    % (where, len(args), len(value)))
            for index, (element_annotation, element) in enumerate(zip(args, value)):
                _check_value("%s[%d]" % (where, index), element_annotation, element)
        return
    if origin in (frozenset, FrozenSet):
        args = typing.get_args(annotation)
        if not isinstance(value, frozenset):
            raise IdentityError("%s requires a frozenset, got %s" % (where, _describe(value)))
        for element in value:
            _check_value("%s{}" % where, args[0] if args else object, element)
        return
    if origin in (list, List, collections.abc.Sequence, Sequence):
        args = typing.get_args(annotation)
        if isinstance(value, (str, bytes)) or not isinstance(value, collections.abc.Sequence):
            raise IdentityError("%s requires a sequence, got %s" % (where, _describe(value)))
        for index, element in enumerate(value):
            _check_value("%s[%d]" % (where, index), args[0] if args else object, element)
        return
    if origin is not None:
        return                                   # a construct this MVP does not use
    if annotation is object or annotation is typing.Any:
        return
    if annotation is Ref:
        # A field declared as the base type accepts any governed reference, and nothing else.
        if not isinstance(value, Ref):
            raise IdentityError("%s requires a governed reference, got %s"
                                % (where, _describe(value)))
        return
    if isinstance(annotation, type) and issubclass(annotation, Ref):
        if type(value) is not annotation:
            raise IdentityError("%s requires %s, got %s"
                                % (where, annotation.KIND, _describe(value)))
        return
    if isinstance(annotation, type) and issubclass(annotation, Enum):
        if type(value) is not annotation:
            raise IdentityError("%s requires the %s enum, got %s"
                                % (where, annotation.__name__, _describe(value)))
        return
    if annotation is bool:
        if type(value) is not bool:
            raise IdentityError("%s requires a bool, got %s" % (where, _describe(value)))
        return
    if annotation is int:
        if type(value) is not int:
            raise IdentityError("%s requires an int, got %s" % (where, _describe(value)))
        return
    if annotation is str:
        if not isinstance(value, str):
            raise IdentityError("%s requires a string, got %s" % (where, _describe(value)))
        return
    if isinstance(annotation, type):
        if not isinstance(value, annotation):
            raise IdentityError("%s requires %s, got %s"
                                % (where, annotation.__name__, _describe(value)))


def enforce_field_types(instance) -> None:
    """Validate EVERY declared field of `instance`, not only its governed references.

    Called from each governed object's `__post_init__`, so a malformed governed object never
    comes into existence."""
    cls = type(instance)
    hints = _HINTS_CACHE.get(cls)
    if hints is None:
        hints = typing.get_type_hints(cls)
        _HINTS_CACHE[cls] = hints
    for f in dataclasses.fields(instance):
        annotation = hints.get(f.name, f.type)
        if isinstance(annotation, str):
            continue                             # an unresolved forward reference
        _check_value("%s.%s" % (cls.__name__, f.name), annotation,
                     getattr(instance, f.name))


#: The former name, kept so the intent reads the same at every call site.
enforce_reference_types = enforce_field_types


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


POSTURE_PERMITS_COMPLETION: Dict[GovernancePosture, FrozenSet[TerminalOutcome]] = {
    GovernancePosture.GOVERNANCE_CLEAR: frozenset({TerminalOutcome.COMPLETED}),
    GovernancePosture.OPEN_ITEMS_CARRIED: frozenset({TerminalOutcome.COMPLETED_WITH_OPEN_ITEMS}),
    GovernancePosture.GATE_UNSATISFIED: frozenset(),
    GovernancePosture.AUTHORITY_ABSENT: frozenset(),
}

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


AUTOMATICALLY_RETRYABLE: FrozenSet[RetryClass] = frozenset({
    RetryClass.SAFE_AUTOMATIC_RETRY, RetryClass.RETRY_REQUIRING_REVALIDATION,
    RetryClass.REPLAYABLE_READ_ONLY, RetryClass.IDEMPOTENT_AT_LEAST_ONCE,
})

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
    """Exactly one governed scope per execution, bound at intake and never mutated.

    Sensitivity is an unordered multi-label set, as Phase 8 defines it: there is no ceiling to
    compare, so narrowing is subset containment and widening is anything else."""

    scope: ScopeRef
    sensitivity: FrozenSet[str]
    residency: str

    def __post_init__(self):
        enforce_field_types(self)
        if not isinstance(self.sensitivity, frozenset):
            raise GovernanceError("sensitivity must be an unordered label set")
        if not self.residency:
            raise GovernanceError("a scope binding needs a residency constraint")

    def narrows_to(self, other: "ScopeBinding") -> bool:
        """True when `other` is a narrowing of this binding, and only then."""
        return (isinstance(other, ScopeBinding)
                and other.scope == self.scope
                and other.sensitivity <= self.sensitivity
                and other.residency == self.residency)


@dataclass(frozen=True)
class ScopeTransferAuthorisation:
    """Governed evidence that one specific crossing was approved.

    A bare `HandoffRef` or `ScopeTransferRef` proves nothing - the audit's eighth finding. The
    approved mechanism is an object binding the mechanism at a version to the source run and
    scope, the target scope, and the Decision Record by which a human authorised it."""

    mechanism: Ref
    mechanism_version: str
    source_run: WorkflowRunRef
    source_scope: ScopeBinding
    target_scope: ScopeBinding
    work_item: WorkItemRef
    requirement: GateRequirementRef
    decision_right: DecisionRightRef
    authorised_by: HumanAuthorityRef
    decision_record: DecisionRecordRef

    def __post_init__(self):
        enforce_field_types(self)
        if type(self.mechanism) not in (HandoffRef, ScopeTransferRef):
            raise IdentityError(
                "an approved crossing mechanism is a Phase 6 handoff or a Phase 8 scope "
                "transfer, got %s" % _describe(self.mechanism))
        if not self.mechanism_version:
            raise GovernanceError("an approved mechanism must be named at a version")

    def covers(self, run: "WorkflowRun", target: ScopeBinding) -> bool:
        """The authorisation must name THIS run, THIS whole source binding and THAT whole
        target binding - sensitivity and residency included, not merely the scope id."""
        return (self.source_run == run.ref
                and self.source_scope == run.scope
                and self.target_scope == target)


# ===========================================================================================
# Definition-side objects
# ===========================================================================================


@dataclass(frozen=True)
class GateRequirement:
    """One gate the definition declares, with its own stable identity.

    Identity matters: two Decision gates on one Work Item are two requirements, and collapsing
    them into a `(work_item, kind)` key - the audit's fourth finding - let evidence for one
    satisfy the other."""

    ref: GateRequirementRef
    kind: GateKind
    review_profile: Optional[ReviewProfileRef] = None
    decision_right: Optional[DecisionRightRef] = None
    human_work: Optional[HumanWorkRef] = None
    prerequisite: Optional[PrerequisiteRef] = None
    independence_class: str = ""
    description: str = ""

    def __post_init__(self):
        enforce_field_types(self)
        if not isinstance(self.kind, GateKind):
            raise GovernanceError("a gate requirement needs one of the four approved kinds")
        named = {
            GateKind.REVIEW: self.review_profile,
            GateKind.DECISION: self.decision_right,
            GateKind.HUMAN_WORK: self.human_work,
            GateKind.GOVERNED_PREREQUISITE: self.prerequisite,
        }
        if named[self.kind] is None:
            raise GovernanceError("a %s gate must name what satisfies it" % self.kind.value)
        for kind, value in named.items():
            if kind is not self.kind and value is not None:
                raise GovernanceError(
                    "a %s gate may not also name a %s subject" % (self.kind.value, kind.value))
        if self.kind is GateKind.REVIEW and not self.independence_class:
            raise GovernanceError("a review gate must declare its independence class")


@dataclass(frozen=True)
class Task:
    """A unit of DEFINITION. Never edited by a run - editing it would rewrite the workflow."""

    ref: TaskRef
    name: str
    required_role: RoleRef
    retry_class: RetryClass
    gates: Tuple[GateRequirement, ...] = ()
    capability: str = ""

    def __post_init__(self):
        enforce_field_types(self)
        if not isinstance(self.retry_class, RetryClass):
            raise GovernanceError("a task must declare one of the seven retry classes")
        if len({g.ref for g in self.gates}) != len(self.gates):
            raise GovernanceError("each gate requirement needs its own identity")


@dataclass(frozen=True)
class WorkflowDefinition:
    """A governed, versioned definition. A run executes it; it never mutates."""

    ref: WorkflowRef
    version: str
    tasks: Tuple[Task, ...]
    scope: ScopeBinding

    def __post_init__(self):
        enforce_field_types(self)
        if not self.version:
            raise GovernanceError("a workflow definition must be versioned")
        if not self.tasks:
            raise GovernanceError("a workflow definition needs at least one task")
        if len({t.ref for t in self.tasks}) != len(self.tasks):
            raise GovernanceError("each task in a definition needs its own identity")

    def task(self, ref: TaskRef) -> Task:
        """The declared Task with this reference, or a refusal.

        Lookup rather than acceptance: an undeclared Task cannot be activated, and a Task
        object from another definition is never taken on trust."""
        require(ref, TaskRef, "task lookup")
        for declared in self.tasks:
            if declared.ref == ref:
                return declared
        raise LineageError("%s is not declared by %s @ %s" % (ref, self.ref, self.version))


# ===========================================================================================
# Run-side objects, each carrying its lineage
# ===========================================================================================


@dataclass(frozen=True)
class WorkItem:
    """A unit of ASSIGNMENT, created by a run from a declared Task.

    It carries the whole lineage it was created under - workflow, version, task, run - and its
    retry class, copied from the Task at creation. Later acts are checked against this, not
    against a Task the caller supplies at the time."""

    ref: WorkItemRef
    task: TaskRef
    run: WorkflowRunRef
    workflow: WorkflowRef
    workflow_version: str
    retry_class: RetryClass
    required_role: RoleRef
    capability: str = ""

    def __post_init__(self):
        enforce_field_types(self)
        if not isinstance(self.retry_class, RetryClass):
            raise GovernanceError("a work item carries its task's retry class")
        if not self.workflow_version:
            raise GovernanceError("a work item carries the definition version it came from")


@dataclass(frozen=True)
class GateInstance:
    """A declared requirement, INSTANTIATED against one run and one Work Item.

    A requirement reference alone is not an instantiated gate: the same Task may be activated
    twice, and two Tasks may reuse a requirement id. The instance therefore carries its own
    identity, and the run keys its gates by that identity, so nothing displaces anything."""

    ref: GateInstanceRef
    requirement: GateRequirement
    run: WorkflowRunRef
    work_item: WorkItemRef
    kind: GateKind
    outcome: Optional[GateOutcome] = None
    satisfied_by: Optional[Ref] = None

    def __post_init__(self):
        enforce_field_types(self)
        if self.kind is not self.requirement.kind:
            raise GovernanceError("a gate instance carries the kind its requirement declares")

    def is_continuing(self) -> bool:
        return self.outcome in CONTINUING_GATE_OUTCOMES

    def is_resolved(self) -> bool:
        return self.outcome is not None

    def addresses(self, work_item: WorkItemRef, requirement: GateRequirementRef) -> bool:
        return self.work_item == work_item and self.requirement.ref == requirement

    def resolved(self, outcome: GateOutcome, satisfied_by: Optional[Ref]) -> "GateInstance":
        return GateInstance(self.ref, self.requirement, self.run, self.work_item, self.kind,
                            outcome, satisfied_by)


@dataclass(frozen=True)
class Assignment:
    """One attempt to bind a Role - and, where permitted, an Agent Instance - to a Work Item.

    An assignment carries no authority of its own. It does not make its holder a reviewer and
    it does not make them a Decision Right holder."""

    work_item: WorkItemRef
    role: RoleRef
    agent_instance: Optional[AgentInstanceRef] = None
    attempt: int = 1

    def __post_init__(self):
        enforce_field_types(self)
        if self.attempt < 1:
            raise GovernanceError("an assignment attempt is numbered from one")

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
        enforce_field_types(self)


# ------------------------------------------------------------------ routing


@dataclass(frozen=True)
class RoutingRequest:
    """What the orchestrator may ask the Router.

    It carries requirements and constraints, and its own identity so that the answer can be
    bound back to it. It carries no chosen model, no relaxed constraint and no pre-filtered
    candidate set - those would make the orchestrator the Router."""

    ref: RoutingRequestRef
    run: WorkflowRunRef
    work_item: WorkItemRef
    capability: str
    scope: ScopeBinding
    routing_policy: str
    independence_class: str = ""

    def __post_init__(self):
        enforce_field_types(self)
        if not self.capability:
            raise GovernanceError("a routing request must declare a capability requirement")
        if not self.routing_policy:
            raise GovernanceError("a routing request must name its routing policy at version")


@dataclass(frozen=True)
class RoutingDecision:
    """What the Router returns, bound to the exact request it answers."""

    ref: RoutingDecisionRef
    request: RoutingRequestRef
    run: WorkflowRunRef
    work_item: WorkItemRef
    outcome: RouterOutcome
    decided_by: RouterRef
    model: Optional[ModelRef] = None
    model_profile: Optional[ModelProfileRef] = None

    def __post_init__(self):
        enforce_field_types(self)
        if not isinstance(self.outcome, RouterOutcome):
            raise GovernanceError("a routing decision carries one of the router outcomes")
        if self.outcome is RouterOutcome.ELIGIBLE_CANDIDATE:
            require(self.model, ModelRef, "routing decision model")
            require(self.model_profile, ModelProfileRef, "routing decision model profile")
        elif self.model is not None or self.model_profile is not None:
            raise GovernanceError("a non-eligible routing outcome may not name a model")

    def answers(self, request: RoutingRequest) -> bool:
        return (self.request == request.ref and self.run == request.run
                and self.work_item == request.work_item)


@dataclass(frozen=True)
class ModelInvocationRequest:
    """A request to execute the model a recorded Routing Decision selected."""

    run: WorkflowRunRef
    work_item: WorkItemRef
    routing_decision: RoutingDecisionRef
    model: ModelRef
    model_profile: ModelProfileRef
    prompt_context: str = ""

    def __post_init__(self):
        enforce_field_types(self)


@dataclass(frozen=True)
class ModelResult:
    """Model output. Always a suggestion, never an approval and never canonical knowledge."""

    ref: ModelResultRef
    run: WorkflowRunRef
    work_item: WorkItemRef
    routing_decision: RoutingDecisionRef
    model: ModelRef
    model_profile: ModelProfileRef
    content: str
    origin: Origin = Origin.AI_GENERATED
    canonicality: Canonicality = Canonicality.AI_SUGGESTION

    def __post_init__(self):
        enforce_field_types(self)
        if self.origin is not Origin.AI_GENERATED:
            raise GovernanceError("a model result is AI_GENERATED by construction")
        if self.canonicality is not Canonicality.AI_SUGGESTION:
            raise GovernanceError("a model result is an AI_SUGGESTION, never canonical")

    def satisfies_gate(self) -> bool:
        """A model result satisfies no gate of any kind. Stated as code, not as prose."""
        return False


# ------------------------------------------------------------------ gate evidence


@dataclass(frozen=True)
class ReviewRequest:
    """The orchestrator's whole part in a review gate: detect, and ask."""

    requirement: GateRequirementRef
    run: WorkflowRunRef
    work_item: WorkItemRef
    review_profile: ReviewProfileRef
    independence_class: str

    def __post_init__(self):
        enforce_field_types(self)
        if not self.independence_class:
            raise GovernanceError("a review request must carry its independence class")


@dataclass(frozen=True)
class ReviewInstance:
    """A review that happened, by a reviewer, under a Profile. Produced by Phase 6."""

    ref: ReviewInstanceRef
    requirement: GateRequirementRef
    run: WorkflowRunRef
    work_item: WorkItemRef
    review_profile: ReviewProfileRef
    outcome: GateOutcome
    reviewer: HumanAuthorityRef
    independence_class: str

    def __post_init__(self):
        enforce_field_types(self)
        if not isinstance(self.outcome, GateOutcome):
            raise GovernanceError("a review instance carries one of the seven outcomes")
        if not self.independence_class:
            raise GovernanceError("a review instance records the independence it was done at")


@dataclass(frozen=True)
class DecisionRequest:
    """The orchestrator's whole part in a decision gate: detect, name the Right, and ask."""

    requirement: GateRequirementRef
    run: WorkflowRunRef
    work_item: WorkItemRef
    decision_right: DecisionRightRef
    question: str = ""

    def __post_init__(self):
        enforce_field_types(self)


@dataclass(frozen=True)
class DecisionRecord:
    """A Right exercised by an eligible human, bound to the exact request it answers."""

    ref: DecisionRecordRef
    requirement: GateRequirementRef
    run: WorkflowRunRef
    work_item: WorkItemRef
    decision_right: DecisionRightRef
    outcome: GateOutcome
    decided_by: HumanAuthorityRef

    def __post_init__(self):
        enforce_field_types(self)
        if not isinstance(self.outcome, GateOutcome):
            raise GovernanceError("a decision record carries one of the seven outcomes")


@dataclass(frozen=True)
class HumanWorkCompletion:
    """A human completing requested work. Not a review, and not a decision."""

    ref: HumanWorkRecordRef
    requirement: GateRequirementRef
    run: WorkflowRunRef
    work_item: WorkItemRef
    human_work: HumanWorkRef
    outcome: GateOutcome
    completed_by: HumanAuthorityRef

    def __post_init__(self):
        enforce_field_types(self)


@dataclass(frozen=True)
class PrerequisiteEvidence:
    """Evidence that a Phase 8-10 governed prerequisite is met. Not a human act."""

    ref: PrerequisiteRecordRef
    requirement: GateRequirementRef
    run: WorkflowRunRef
    work_item: WorkItemRef
    prerequisite: PrerequisiteRef
    outcome: GateOutcome
    evaluated_against: StorageRecordRef

    def __post_init__(self):
        enforce_field_types(self)


#: The evidence contract per gate kind. Anything else offered at a gate is refused outright,
#: which is what keeps a Review Instance out of a HUMAN_WORK gate and a Decision Record out of
#: a GOVERNED_PREREQUISITE gate.
EVIDENCE_CONTRACT: Dict[GateKind, type] = {
    GateKind.REVIEW: ReviewInstance,
    GateKind.DECISION: DecisionRecord,
    GateKind.HUMAN_WORK: HumanWorkCompletion,
    GateKind.GOVERNED_PREREQUISITE: PrerequisiteEvidence,
}


@dataclass(frozen=True)
class HumanInterventionRecord:
    """A human act on the run, recorded. Pauses, acknowledgements and cancellations."""

    ref: InterventionRef
    run: WorkflowRunRef
    by: HumanAuthorityRef
    act: str
    reason: str

    def __post_init__(self):
        enforce_field_types(self)
        if not self.reason:
            raise GovernanceError("an intervention record must state a reason")


# ===========================================================================================
# Append-only stores
# ===========================================================================================


@dataclass(frozen=True)
class ExecutionEvent:
    """One recorded fact about a run. Governance evidence, distinct from an operational log."""

    sequence: int
    run: WorkflowRunRef
    kind: str
    detail: str = ""
    reference: Optional[Ref] = None

    def __post_init__(self):
        enforce_field_types(self)


class ExecutionEventLog:
    """Append-only history.

    There is no update, no delete and no reordering. The backing list is held in a closure
    rather than on the instance, so there is no attribute for a caller to reach for and
    rewrite - the audit's ninth finding was that an underscore-private list is not a boundary."""

    def __init__(self):
        events: List[ExecutionEvent] = []

        def _append(run, kind, detail, reference):
            event = ExecutionEvent(len(events) + 1, run, kind, detail, reference)
            events.append(event)
            return event

        def _read():
            return tuple(events)

        object.__setattr__(self, "_ExecutionEventLog__append", _append)
        object.__setattr__(self, "_ExecutionEventLog__read", _read)

    def append(self, run: WorkflowRunRef, kind: str, detail: str = "",
               reference: Optional[Ref] = None) -> ExecutionEvent:
        require(run, WorkflowRunRef, "execution event run")
        return self.__append(run, kind, detail, reference)

    def events(self) -> Sequence[ExecutionEvent]:
        return self.__read()

    def kinds(self) -> Tuple[str, ...]:
        return tuple(e.kind for e in self.__read())

    def __len__(self) -> int:
        return len(self.__read())

    def __setitem__(self, index, value):
        raise AppendOnlyError("execution history cannot be rewritten")

    def __delitem__(self, index):
        raise AppendOnlyError("execution history cannot be deleted")

    def __setattr__(self, name, value):
        raise AppendOnlyError("the execution log has no settable attributes")


class RecordStore:
    """An append-only store of governed records, keyed by their own identities.

    Records are never replaced by Work Item id. A second Decision Record for the same Work Item
    is a second record: the first stands in governed history, which is what the architecture
    requires of a late or repeated governed act."""

    def __init__(self, name: str):
        records: List[object] = []

        def _validate_add(record):
            identity = getattr(record, "ref", None)
            # Some non-evidence collections (for example Assignment) have no architecture-
            # level record identity. Where a governed record does declare one, it must be a
            # governed reference and must be unique in this history.
            if identity is None:
                return
            if not isinstance(identity, Ref):
                raise AppendOnlyError("%s has a malformed record identity" % name)
            for existing in records:
                if getattr(existing, "ref", None) == identity:
                    raise AppendOnlyError(
                        "%s already holds a record with identity %s; ambiguous history is "
                        "not admitted" % (name, identity))

        def _add(record):
            _validate_add(record)
            records.append(record)
            return record

        def _read():
            return tuple(records)

        object.__setattr__(self, "_RecordStore__add", _add)
        object.__setattr__(self, "_RecordStore__validate_add", _validate_add)
        object.__setattr__(self, "_RecordStore__read", _read)
        object.__setattr__(self, "_RecordStore__name", name)

    def add(self, record):
        return self.__add(record)

    def validate_add(self, record) -> None:
        """Preflight an append without mutating history."""
        self.__validate_add(record)

    def all(self) -> Tuple[object, ...]:
        return self.__read()

    def for_work_item(self, work_item: WorkItemRef) -> Tuple[object, ...]:
        return tuple(r for r in self.__read() if getattr(r, "work_item", None) == work_item)

    def latest_for_work_item(self, work_item: WorkItemRef):
        found = self.for_work_item(work_item)
        return found[-1] if found else None

    def contains(self, record) -> bool:
        """Identity membership: this exact recorded object, not one that merely equals it."""
        return any(r is record for r in self.__read())

    def __len__(self) -> int:
        return len(self.__read())

    def __setattr__(self, name, value):
        raise AppendOnlyError("%s is append-only" % self.__name)

    def __setitem__(self, index, value):
        raise AppendOnlyError("%s is append-only" % self.__name)

    def __delitem__(self, index):
        raise AppendOnlyError("%s is append-only" % self.__name)


# ===========================================================================================
# The run - governed state behind a token
# ===========================================================================================


class _RunState:
    """The mutable part of a run, reachable only by the holder of the run's token."""

    def __init__(self, scope: ScopeBinding):
        self.phase = RunPhase.CREATED
        self.terminal: Optional[TerminalOutcome] = None
        self.wait_reason: Optional[WaitReason] = None
        self.wait_subject: Optional[Ref] = None
        self.posture = GovernancePosture.GOVERNANCE_CLEAR
        self.scope = scope
        self.work_items: Dict[str, WorkItem] = {}
        self.gates: Dict[str, GateInstance] = {}
        self.attempts: Dict[str, int] = {}


class WorkflowRun:
    """One governed execution of one Workflow Definition at one version.

    The four axes are readable and not writable. `run.phase = RunPhase.RUNNING` raises, and so
    does assignment to posture, scope, gates or any governed collection: the audit's third
    finding was that a caller could set the state that `complete()` then consulted. State moves
    only through the orchestrator that created the run and holds its token."""

    _GOVERNED = frozenset({"phase", "terminal", "wait_reason", "wait_subject", "posture",
                           "scope", "work_items", "gates", "attempts", "ref", "definition",
                           "workflow", "workflow_version"})

    def __init__(self, ref: WorkflowRunRef, definition: WorkflowDefinition,
                 scope: ScopeBinding, token: object):
        require(ref, WorkflowRunRef, "workflow run")
        if not isinstance(definition, WorkflowDefinition):
            raise LineageError("a run binds to a governed Workflow Definition")
        if not isinstance(scope, ScopeBinding):
            raise GovernanceError("a run binds to exactly one governed scope")
        object.__setattr__(self, "_WorkflowRun__ref", ref)
        object.__setattr__(self, "_WorkflowRun__definition", definition)
        object.__setattr__(self, "_WorkflowRun__token", token)
        object.__setattr__(self, "_WorkflowRun__state", _RunState(scope))
        object.__setattr__(self, "_WorkflowRun__decisions", RecordStore("decision records"))
        object.__setattr__(self, "_WorkflowRun__reviews", RecordStore("review instances"))
        object.__setattr__(self, "_WorkflowRun__human_work", RecordStore("human work"))
        object.__setattr__(self, "_WorkflowRun__prerequisites", RecordStore("prerequisites"))
        object.__setattr__(self, "_WorkflowRun__routing_requests", RecordStore("routing requests"))
        object.__setattr__(self, "_WorkflowRun__routing", RecordStore("routing decisions"))
        object.__setattr__(self, "_WorkflowRun__model_results", RecordStore("model results"))
        object.__setattr__(self, "_WorkflowRun__assignments", RecordStore("assignments"))
        object.__setattr__(self, "_WorkflowRun__interventions", RecordStore("interventions"))

    # -- the boundary itself -------------------------------------------------------------

    def __setattr__(self, name, value):
        raise StateAccessError(
            "governed run state is not settable from outside the orchestrator (%s)" % name)

    def __delattr__(self, name):
        raise StateAccessError("governed run state cannot be deleted")

    def _state(self, token: object) -> _RunState:
        """The mutable state, for the orchestrator that created this run and nobody else."""
        if token is not self.__token:
            raise StateAccessError("only the orchestrator that created this run may change it")
        return self.__state

    def _store(self, token: object, name: str) -> RecordStore:
        if token is not self.__token:
            raise StateAccessError("only the orchestrator that created this run may record")
        return getattr(self, "_WorkflowRun__" + name)

    # -- read-only view ------------------------------------------------------------------

    @property
    def ref(self) -> WorkflowRunRef:
        return self.__ref

    @property
    def definition(self) -> WorkflowDefinition:
        return self.__definition

    @property
    def workflow(self) -> WorkflowRef:
        return self.__definition.ref

    @property
    def workflow_version(self) -> str:
        return self.__definition.version

    @property
    def phase(self) -> RunPhase:
        return self.__state.phase

    @property
    def terminal(self) -> Optional[TerminalOutcome]:
        return self.__state.terminal

    @property
    def wait_reason(self) -> Optional[WaitReason]:
        return self.__state.wait_reason

    @property
    def wait_subject(self) -> Optional[Ref]:
        return self.__state.wait_subject

    @property
    def posture(self) -> GovernancePosture:
        return self.__state.posture

    @property
    def scope(self) -> ScopeBinding:
        return self.__state.scope

    @property
    def is_terminal(self) -> bool:
        return self.__state.terminal is not None

    def work_items(self) -> Tuple[WorkItem, ...]:
        return tuple(self.__state.work_items.values())

    def work_item(self, ref: WorkItemRef) -> WorkItem:
        require(ref, WorkItemRef, "work item lookup")
        found = self.__state.work_items.get(ref.id)
        if found is None:
            raise LineageError("%s was not created by %s" % (ref, self.__ref))
        return found

    def gates(self) -> Tuple[GateInstance, ...]:
        return tuple(self.__state.gates.values())

    def gate_instance(self, work_item: WorkItemRef,
                      requirement: GateRequirementRef) -> GateInstance:
        """The gate this run instantiated for that Work Item and that requirement.

        Addressed by the pair, because a requirement id is not unique on its own: the same Task
        activated twice, and two Tasks sharing a requirement id, each hold their own gates."""
        require(work_item, WorkItemRef, "gate lookup")
        require(requirement, GateRequirementRef, "gate lookup")
        found = [g for g in self.__state.gates.values() if g.addresses(work_item, requirement)]
        if not found:
            raise LineageError("%s has no gate %s for %s"
                               % (self.__ref, requirement, work_item))
        if len(found) > 1:
            raise LineageError("%s addresses %d gate instances; this is ambiguous"
                               % (requirement, len(found)))
        return found[0]

    def gate(self, instance: GateInstanceRef) -> GateInstance:
        require(instance, GateInstanceRef, "gate lookup")
        found = self.__state.gates.get(instance.id)
        if found is None:
            raise LineageError("%s is not a gate of %s" % (instance, self.__ref))
        return found

    def attempts(self, work_item: WorkItemRef) -> int:
        return self.__state.attempts.get(work_item.id, 0)

    def decision_records(self) -> Tuple[DecisionRecord, ...]:
        return self.__decisions.all()

    def review_instances(self) -> Tuple[ReviewInstance, ...]:
        return self.__reviews.all()

    def routing_decisions(self) -> Tuple[RoutingDecision, ...]:
        return self.__routing.all()

    def routing_requests(self) -> Tuple[RoutingRequest, ...]:
        return self.__routing_requests.all()

    def model_results(self) -> Tuple[ModelResult, ...]:
        return self.__model_results.all()

    def assignments(self) -> Tuple[Assignment, ...]:
        return self.__assignments.all()

    def human_work_records(self) -> Tuple[HumanWorkCompletion, ...]:
        return self.__human_work.all()

    def prerequisite_records(self) -> Tuple[PrerequisiteEvidence, ...]:
        return self.__prerequisites.all()

    def interventions(self) -> Tuple[HumanInterventionRecord, ...]:
        return self.__interventions.all()

    def evidence_for(self, instance: "GateInstance"):
        """The retained governed record that satisfied a gate, found by its own identity.

        Completion has to be explainable from history: given a resolved gate, the object that
        resolved it is retrievable, rather than merely referenced by an id nobody kept."""
        if instance.satisfied_by is None:
            return None
        for store in (self.__reviews, self.__decisions, self.__human_work,
                      self.__prerequisites):
            for record in store.all():
                if getattr(record, "ref", None) == instance.satisfied_by:
                    return record
        return None

    def axes(self):
        state = self.__state
        return (state.phase, state.terminal, state.wait_reason, state.posture)

    def __repr__(self):
        return "<WorkflowRun %s %s/%s>" % (self.__ref.id, self.phase.value,
                                           self.posture.value)
