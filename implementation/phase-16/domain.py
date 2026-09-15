"""Phase 16 — planner activation domain model.

Status: PROPOSED. Standard library only, deterministic, no network, no provider calls.

Typed objects for the bridge between the approved Phase 15 planning architecture and the
approved Phase 11 Orchestrator under the Phase 14 implementation contracts. Nothing here
approves anything, exercises a Decision Right, registers a Role, Skill or Workflow, or claims
production readiness. Every governed act remains where the approved architecture put it.

The three objects that matter:

    PlannerOutput    what Phase 15 produces, made machine-readable
    WorkPlan         the instance-level composition, never a Workflow definition
    ExecutionBasis   the governed object that lets a valid plan reach Orchestrator intake
"""

from __future__ import annotations

import dataclasses
import enum
import hashlib
import json
from typing import Dict, List, Optional, Tuple


#: The Phase 14 implementation-specification baseline this bridge is written against. It lives
#: here rather than in the preflight so that the trigger builder can compare against it without
#: importing the preflight, and so that a basis carrying a different value is detectable.
IMPLEMENTATION_SPEC_VERSION = "phase-14@ba9e3fee"


class ActivationError(Exception):
    """A refusal. Raised where a rule makes an action impossible, never logged and continued."""


class GovernanceError(ActivationError):
    """An attempt to create, grant or assume authority the planner does not hold."""


# --------------------------------------------------------------------------- enumerations


class ExecutionMode(enum.Enum):
    MATCH = "MATCH"
    COMPOSE = "COMPOSE"


class PlannerState(enum.Enum):
    DRAFT = "DRAFT"
    CLARIFICATION_REQUIRED = "CLARIFICATION_REQUIRED"
    VALIDATED = "VALIDATED"
    BLOCKED = "BLOCKED"


class BasisStatus(enum.Enum):
    """The Execution Basis lifecycle.

    EXECUTABLE means intake may ACCEPT the trigger. It does not mean the work is approved, that
    any gate is satisfied, or that any Right has been exercised - the Orchestrator still runs
    intake checks 1-7 and every gate still stands.
    """
    DRAFT = "DRAFT"
    VALIDATED = "VALIDATED"
    EXECUTABLE = "EXECUTABLE"
    BLOCKED = "BLOCKED"
    STALE = "STALE"
    SUPERSEDED = "SUPERSEDED"


class PrerequisiteState(enum.Enum):
    """Phase 14 / Phase 15 tri-state. A plain UNKNOWN blocks; it is never a deferral."""
    RESOLVED = "RESOLVED"
    FUTURE_GOVERNANCE_REFERENCE = "FUTURE_GOVERNANCE_REFERENCE"
    UNKNOWN = "UNKNOWN"


class Criticality(enum.Enum):
    ROUTINE = "ROUTINE"
    ENHANCED_REVIEW_CANDIDATE = "ENHANCED_REVIEW_CANDIDATE"
    ENHANCED_DECISION_GRADE = "ENHANCED_DECISION_GRADE"
    CRITICAL = "CRITICAL"


#: Bands at or above which an independent review requirement may not be waived by planning.
REVIEW_FLOOR = (Criticality.ENHANCED_DECISION_GRADE, Criticality.CRITICAL)


class WorkMode(enum.Enum):
    ACTION = "ACTION"
    ANALYSIS = "ANALYSIS"
    ADVICE = "ADVICE"
    DRAFTING = "DRAFTING"
    MONITORING = "MONITORING"
    DECISION_SUPPORT = "DECISION_SUPPORT"
    UNKNOWN = "UNKNOWN"


class BlockReason(enum.Enum):
    NO_VALID_SCOPE = "NO_VALID_SCOPE"
    CLARIFICATION_REQUIRED = "CLARIFICATION_REQUIRED"
    NO_APPLICABLE_DECISION_RIGHT = "NO_APPLICABLE_DECISION_RIGHT"
    REVIEW_UNRESOLVED = "REVIEW_UNRESOLVED"
    UNREGISTERED_CAPABILITY = "UNREGISTERED_CAPABILITY"
    NO_APPROVED_ROLE_OWNS_CONCLUSION = "NO_APPROVED_ROLE_OWNS_CONCLUSION"
    WORKFLOW_NOT_APPROVED = "WORKFLOW_NOT_APPROVED"
    WORKFLOW_VERSION_STALE = "WORKFLOW_VERSION_STALE"
    SOD_VIOLATION = "SOD_VIOLATION"
    EVIDENCE_UNSATISFIED = "EVIDENCE_UNSATISFIED"
    DANGLING_PREREQUISITE = "DANGLING_PREREQUISITE"
    CRITICALITY_UNRESOLVED = "CRITICALITY_UNRESOLVED"
    SCOPE_AMBIGUOUS = "SCOPE_AMBIGUOUS"
    INJECTED_GOVERNED_RECORD = "INJECTED_GOVERNED_RECORD"
    BASIS_NOT_EXECUTABLE = "BASIS_NOT_EXECUTABLE"
    DUPLICATE_STAGE_IDENTITY = "DUPLICATE_STAGE_IDENTITY"
    STAGE_OWNER_UNRESOLVED = "STAGE_OWNER_UNRESOLVED"
    SKILL_ROLE_INCOMPATIBLE = "SKILL_ROLE_INCOMPATIBLE"
    BASIS_NOT_ISSUED = "BASIS_NOT_ISSUED"
    BASIS_INTEGRITY_FAILED = "BASIS_INTEGRITY_FAILED"


# --------------------------------------------------------------------------- requirements
#
# Every requirement below is a REQUIREMENT. None of them is the thing it names: a
# ReviewRequirement is not a satisfied review, a DecisionRequirement is not an exercised Right,
# and an EvidenceRequirement is not evidence.


@dataclasses.dataclass(frozen=True)
class RoleRequirement:
    role_ref: str
    owned_conclusion: str
    activation: str = "ALWAYS"
    registered: bool = True
    load_bearing: bool = True


@dataclasses.dataclass(frozen=True)
class SkillRequirement:
    skill_ref: str
    for_role: str
    registered: bool = True


@dataclasses.dataclass(frozen=True)
class ReviewRequirement:
    review_ref: str
    mandatory: bool
    #: Set only by a Review Instance recorded through the approved Phase 14 command. Planning
    #: never sets it, and the preflight refuses a plan that arrives with it set.
    satisfied: bool = False


@dataclasses.dataclass(frozen=True)
class DecisionRequirement:
    decision_ref: Optional[str]
    act: str
    #: Likewise: exercised only by ExerciseDecisionRight, never by planning.
    exercised: bool = False


@dataclasses.dataclass(frozen=True)
class EvidenceRequirement:
    reference: str
    state: PrerequisiteState
    required_before_first_act: bool = True


@dataclasses.dataclass(frozen=True)
class ClarificationRequirement:
    question: str
    blocking: bool
    #: A blocking class may carry no default. The preflight enforces it rather than trusting it.
    default_if_unanswered: Optional[str] = None


@dataclasses.dataclass(frozen=True)
class PlanStage:
    stage_id: str
    role_ref: Optional[str]
    depends_on: Tuple[str, ...] = ()
    is_gate: bool = False
    expected_artifact: str = ""


# --------------------------------------------------------------------------- planner output


@dataclasses.dataclass(frozen=True)
class WorkPlan:
    """An instance-level composition. Never a Workflow definition, by construction.

    Its identifier space is its own, it carries no registry status, and nothing in this module
    writes it anywhere a Workflow definition is read from.
    """
    work_plan_id: str
    version: int
    stages: Tuple[PlanStage, ...]

    def __post_init__(self) -> None:
        if not self.work_plan_id.startswith("work_plan."):
            raise GovernanceError(
                "a Work Plan identifier lives in the work_plan. space: %r" % self.work_plan_id)
        if self.work_plan_id.startswith("workflow."):
            raise GovernanceError("a Work Plan may never be rendered as a Workflow identity")

    @property
    def ref(self) -> str:
        return "%s@%d" % (self.work_plan_id, self.version)


@dataclasses.dataclass(frozen=True)
class PlannerOutput:
    """The machine-readable Phase 15 planning result.

    No model, provider, prompt, temperature or token field appears here, and none may be added:
    model selection is the Phase 9 Router's, after the Orchestrator creates a routing request.
    """
    request_id: str
    request_text: str
    intent_id: str
    scope_ref: str
    scope_ancestry: Tuple[str, ...]
    objective: str
    deliverables: Tuple[str, ...]
    primary_work_mode: WorkMode
    secondary_work_modes: Tuple[WorkMode, ...]
    criticality: Optional[Criticality]
    execution_mode: ExecutionMode
    role_requirements: Tuple[RoleRequirement, ...] = ()
    skill_requirements: Tuple[SkillRequirement, ...] = ()
    review_requirements: Tuple[ReviewRequirement, ...] = ()
    decision_requirements: Tuple[DecisionRequirement, ...] = ()
    evidence_requirements: Tuple[EvidenceRequirement, ...] = ()
    clarifications: Tuple[ClarificationRequirement, ...] = ()
    work_plan: Optional[WorkPlan] = None
    workflow_ref: Optional[str] = None          # MATCH only, "workflow.<id>@<version>"
    orchestrator_policy_ref: str = "policy.default@1"
    unknown_fields: Tuple[str, ...] = ()
    #: Anything the caller tried to hand over pre-formed. Always refused; kept so the refusal
    #: can name what was attempted rather than failing anonymously.
    injected_governed_records: Tuple[str, ...] = ()

    _MODEL_FIELDS = ("model", "model_profile", "provider", "temperature", "max_tokens", "prompt")

    def __post_init__(self) -> None:
        if self.primary_work_mode in self.secondary_work_modes:
            raise ActivationError("secondary_work_modes may not contain the primary mode")
        if len(set(self.secondary_work_modes)) != len(self.secondary_work_modes):
            raise ActivationError("secondary_work_modes is a set: no duplicates")
        for field in self._MODEL_FIELDS:
            if field in self.unknown_fields:
                raise GovernanceError(
                    "the canonical planner contract carries no model-specific field: %r" % field)
        if self.execution_mode is ExecutionMode.MATCH and self.work_plan is not None:
            raise ActivationError("a MATCH result binds a Workflow, not a composed Work Plan")
        if self.execution_mode is ExecutionMode.COMPOSE and self.workflow_ref is not None:
            raise ActivationError("a COMPOSE result carries no workflow_ref")

    # -- the staleness mechanism -------------------------------------------------------------

    #: Every input whose change can alter preflight, basis issuance, the handoff envelope, or
    #: an authority / review / evidence requirement. The first version omitted five families -
    #: clarifications, scope ancestry, the Orchestrator policy reference, the composed stages'
    #: expected artifacts, and the declared open items - each of which is read downstream, so a
    #: change to any of them left an issued basis standing that no longer described the plan.
    MATERIAL_FIELDS = (
        "scope_ref", "scope_ancestry", "objective", "deliverables", "primary_work_mode",
        "secondary_work_modes", "criticality", "execution_mode", "role_requirements",
        "skill_requirements", "review_requirements", "decision_requirements",
        "evidence_requirements", "clarifications", "workflow_ref", "work_plan",
        "orchestrator_policy_ref", "unknown_fields",
    )

    #: The ONLY excluded fields, each excluded for a stated reason rather than by omission.
    #: `request_text` is presentation: a reworded summary is not a new plan. The two identity
    #: fields are excluded because identity is bound EXACTLY and separately - see the trigger
    #: builder's request/intent equality check - and folding them into the digest would hide a
    #: cross-request reuse behind a digest mismatch instead of naming it.
    PRESENTATION_ONLY_FIELDS = ("request_text",)
    IDENTITY_FIELDS = ("request_id", "intent_id")
    #: Never digested because a plan carrying one is refused outright, before any digest.
    REFUSED_FIELDS = ("injected_governed_records",)

    def material_digest(self) -> str:
        """A digest over every load-bearing planning input.

        `_canonical` expands dataclasses recursively, so a stage's `expected_artifact`, a
        clarification's blocking flag and its default, and each requirement's every field are
        all inside the digest. Changing any of them changes the digest, which is what makes an
        already-issued basis unusable and forces re-preflight.
        """
        payload = {}
        for name in self.MATERIAL_FIELDS:
            payload[name] = _canonical(getattr(self, name))
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    @classmethod
    def classified_fields(cls):
        """Every declared field, partitioned. Used by the completeness invariant below."""
        return (set(cls.MATERIAL_FIELDS) | set(cls.PRESENTATION_ONLY_FIELDS)
                | set(cls.IDENTITY_FIELDS) | set(cls.REFUSED_FIELDS))


def _assert_every_planner_field_is_classified() -> None:
    """A new PlannerOutput field must be classified before it can be added.

    Without this, the ordinary way a digest goes stale is silent: somebody adds a load-bearing
    field, forgets MATERIAL_FIELDS, and a change to it stops invalidating the basis. Here the
    omission is an ImportError at load, not a defect discovered later.
    """
    declared = {f.name for f in dataclasses.fields(PlannerOutput)}
    classified = PlannerOutput.classified_fields()
    unclassified = declared - classified
    phantom = classified - declared
    if unclassified:
        raise ActivationError(
            "PlannerOutput field(s) %s are neither material, presentation-only, identity nor "
            "refused. Classify them before use." % sorted(unclassified))
    if phantom:
        raise ActivationError(
            "PlannerOutput classifies field(s) %s that do not exist" % sorted(phantom))


_assert_every_planner_field_is_classified()


def _canonical(value):
    if isinstance(value, enum.Enum):
        return value.value
    if isinstance(value, (tuple, list)):
        return [_canonical(v) for v in value]
    if dataclasses.is_dataclass(value):
        return {k: _canonical(v) for k, v in sorted(dataclasses.asdict(value).items())}
    return value


# --------------------------------------------------------------------------- execution basis


@dataclasses.dataclass(frozen=True)
class ExecutionBasis:
    """The governed object that authorises a valid plan to ENTER Orchestrator intake.

    It authorises entry and nothing else. It exercises no Decision Right, satisfies no review,
    registers nothing, and grants no permission to perform any act: every gate the plan names
    still stands, and the Orchestrator still runs its own intake checks 1-7.

    IMMUTABLE BY CONSTRUCTION. The first version was a mutable dataclass, so any holder could
    set `status = EXECUTABLE`, repoint `scope_ref`, or blank `review_requirements` on a basis
    the store had already issued, and nothing downstream could tell. A governed record that any
    caller can edit in place is not a governed record. Every field is frozen; a lifecycle
    transition produces a NEW snapshot through `with_status`, and the store keeps the history.

    `payload_seal()` covers every field except `status`, which is lifecycle state the store
    owns. The trigger builder recomputes the seal and compares it with the seal taken at issue,
    so a fabricated or edited basis is refused by evidence rather than by trust.
    """
    basis_id: str
    version: int
    request_id: str
    intent_id: str
    scope_ref: str
    scope_ancestry: Tuple[str, ...]
    execution_mode: ExecutionMode
    criticality: Criticality
    planning_digest: str
    implementation_spec_version: str
    orchestrator_policy_ref: str
    status: BasisStatus = BasisStatus.DRAFT
    workflow_ref: Optional[str] = None
    work_plan_ref: Optional[str] = None
    role_bindings: Tuple[str, ...] = ()
    skill_bindings: Tuple[str, ...] = ()
    review_requirements: Tuple[str, ...] = ()
    decision_requirements: Tuple[str, ...] = ()
    evidence_requirements: Tuple[Tuple[str, str], ...] = ()
    supersedes: Optional[str] = None
    blocked_reasons: Tuple[BlockReason, ...] = ()

    #: Declared rather than omitted, so that no consumer can read an EXECUTABLE basis as one.
    is_approval: bool = False
    is_authority: bool = False

    @property
    def ref(self) -> str:
        return "%s@%d" % (self.basis_id, self.version)

    #: Excluded from the seal: the store owns the lifecycle, the issuer owns the payload.
    _UNSEALED_FIELDS = ("status",)

    def payload_seal(self) -> str:
        """A digest over the issued payload. Any edit to any sealed field changes it."""
        payload = {}
        for field in dataclasses.fields(self):
            if field.name in self._UNSEALED_FIELDS:
                continue
            payload[field.name] = _canonical(getattr(self, field.name))
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    def with_status(self, status: "BasisStatus", **changes) -> "ExecutionBasis":
        """A new snapshot. The old one stays exactly as it was issued."""
        return dataclasses.replace(self, status=status, **changes)

    def exercise(self, *_args, **_kwargs):
        raise GovernanceError(
            "an Execution Basis exercises nothing. A Decision Right is exercised by a human "
            "through the approved Phase 14 command ExerciseDecisionRight")

    def satisfy_review(self, *_args, **_kwargs):
        raise GovernanceError(
            "an Execution Basis satisfies no review. A review is satisfied by a reviewer "
            "through SubmitReviewInstance")

    def mark_stale(self, *_args, **_kwargs):
        raise GovernanceError(
            "an issued Execution Basis is immutable; a lifecycle transition is recorded by the "
            "store, which keeps the prior snapshot. Use ActivationStore.invalidate_on_material_"
            "change or ActivationStore.issue")

    def mark_superseded(self, *_args, **_kwargs):
        raise GovernanceError(
            "an issued Execution Basis is immutable; superseding is recorded by the store")
