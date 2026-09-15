"""Phase 16 — planner to Orchestrator handoff builder.

Status: PROPOSED. Standard library only, deterministic, no network.

Converts an EXECUTABLE Execution Basis into the shape the approved Phase 11 intake accepts,
expressed as the approved Phase 14 command `CreateWorkflowRun` with its envelope. It builds a
TRIGGER. It does not create a run, activate a stage, assign work, route, invoke a model, open a
review, request a decision, or write any governed record: every one of those is a separate
approved Phase 14 command, performed by the Orchestrator.
"""

from __future__ import annotations

import dataclasses
import hashlib
from typing import Dict, List, Optional, Tuple

from domain import (
    ActivationError, BasisStatus, ExecutionBasis, ExecutionMode, GovernanceError,
    PlannerOutput,
)

#: Governed records a caller might try to smuggle into a trigger. Each is created only by its
#: own approved Phase 14 command, and the builder refuses the envelope that carries one.
FORBIDDEN_IN_TRIGGER = (
    "decision_record", "review_instance", "approval_state", "gate_outcome",
    "routing_decision", "model_result", "intervention", "knowledge_item",
)


@dataclasses.dataclass(frozen=True)
class PlannedWorkItemSpec:
    """What Phase 11 would need to instantiate a Work Item, and nothing more.

    TASK != PLANNED WORK ITEM SPEC != WORK ITEM. This carries no run reference, no runtime
    state, no assignment, no execution status and no model. Phase 11 creates `work_item.<id>`
    itself, inside a run, or refuses.
    """
    spec_id: str
    stage_id: str
    role_envelope: Optional[str]
    skill_envelope: Tuple[str, ...]
    depends_on: Tuple[str, ...]
    expected_artifact: str
    review_requirements: Tuple[str, ...]
    decision_requirements: Tuple[str, ...]
    criticality: str
    is_gate: bool

    def __post_init__(self) -> None:
        if not self.spec_id.startswith("planned_work_item_spec."):
            raise GovernanceError(
                "a planned spec lives in its own identifier space, never work_item.")


@dataclasses.dataclass(frozen=True)
class TriggerEnvelope:
    """The `CreateWorkflowRun` envelope, built to make intake checks 1-7 answerable.

    It does not perform them. The Orchestrator validates every one independently, and may
    refuse - which is the design working, not an error to route around.
    """
    command: str
    execution_basis_ref: str
    execution_basis_status: str
    execution_mode: str
    workflow_ref: Optional[str]
    work_plan_ref: Optional[str]
    orchestrator_policy_ref: str
    scope_ref: str
    scope_ancestry: Tuple[str, ...]
    originator: str
    sensitivity: str
    residency: str
    criticality_band: str
    idempotency_key: str
    prerequisite_refs: Tuple[Tuple[str, str], ...]
    planning_provenance: Dict[str, str]
    planned_work_item_specs: Tuple[PlannedWorkItemSpec, ...]
    open_items: Tuple[str, ...]

    #: Declared rather than omitted: a trigger is a request, not a start, and never an approval.
    is_approval: bool = False
    creates_run: bool = False

    def intake_answers(self) -> Dict[int, str]:
        """What each approved intake check can read from this envelope.

        Answering is not performing: check 1 still resolves the definition itself, check 3 still
        decides whether the originator may act in the scope, and so on.
        """
        return {
            1: self.workflow_ref or self.work_plan_ref or "",
            2: self.orchestrator_policy_ref,
            3: "%s | %s" % (self.scope_ref, self.originator),
            4: "%s | %s" % (self.sensitivity, self.residency),
            5: self.criticality_band,
            6: self.idempotency_key,
            7: ";".join("%s=%s" % (r, s) for r, s in self.prerequisite_refs),
        }


def build_trigger(basis: ExecutionBasis, plan: PlannerOutput, *, originator: str,
                  sensitivity: str = "UNASSESSED",
                  residency: str = "UNASSESSED") -> TriggerEnvelope:
    if basis.status is not BasisStatus.EXECUTABLE:
        raise ActivationError(
            "only an EXECUTABLE Execution Basis produces a trigger; this one is %s"
            % basis.status.value)
    if basis.planning_digest != plan.material_digest():
        raise ActivationError(
            "the basis was issued against different planning inputs; it is stale and a trigger "
            "may not be built from it")
    for field in FORBIDDEN_IN_TRIGGER:
        if field in plan.unknown_fields or field in plan.injected_governed_records:
            raise GovernanceError(
                "a trigger carries no pre-formed governed record: %r" % field)

    specs: List[PlannedWorkItemSpec] = []
    if plan.work_plan is not None:
        for stage in plan.work_plan.stages:
            specs.append(PlannedWorkItemSpec(
                spec_id="planned_work_item_spec." + hashlib.sha256(
                    (basis.ref + "|" + stage.stage_id).encode()).hexdigest()[:12],
                stage_id=stage.stage_id,
                role_envelope=stage.role_ref,
                skill_envelope=tuple(s.skill_ref for s in plan.skill_requirements
                                     if s.for_role == stage.role_ref),
                depends_on=stage.depends_on,
                expected_artifact=stage.expected_artifact,
                review_requirements=basis.review_requirements,
                decision_requirements=basis.decision_requirements,
                criticality=basis.criticality.value,
                is_gate=stage.is_gate,
            ))

    return TriggerEnvelope(
        command="CreateWorkflowRun",
        execution_basis_ref=basis.ref,
        execution_basis_status=basis.status.value,
        execution_mode=basis.execution_mode.value,
        workflow_ref=basis.workflow_ref,
        work_plan_ref=basis.work_plan_ref,
        orchestrator_policy_ref=basis.orchestrator_policy_ref,
        scope_ref=basis.scope_ref,
        scope_ancestry=basis.scope_ancestry,
        originator=originator,
        sensitivity=sensitivity,
        residency=residency,
        criticality_band=basis.criticality.value,
        idempotency_key=idempotency_key(plan),
        prerequisite_refs=basis.evidence_requirements,
        planning_provenance={
            "request": plan.request_id,
            "intent": plan.intent_id,
            "work_plan": basis.work_plan_ref or "",
            "execution_basis": basis.ref,
        },
        planned_work_item_specs=tuple(specs),
        open_items=tuple(plan.unknown_fields),
    )


def idempotency_key(plan: PlannerOutput) -> str:
    """Durable request identity: the same request at the same material version is one trigger.

    Scoped to (scope, request, material planning version), matching the Phase 14 envelope's
    at-most-once-at-the-API-boundary semantics. A material replan changes the digest and is
    therefore a different key - a new lineage, never a mutation of the old one.
    """
    return "idem." + hashlib.sha256(
        ("%s|%s|%s" % (plan.scope_ref, plan.request_id, plan.material_digest())).encode()
    ).hexdigest()[:24]
