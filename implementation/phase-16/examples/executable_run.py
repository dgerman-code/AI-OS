"""Phase 16 — a request that reaches Orchestrator intake, printed step by step.

Status: PROPOSED. No network, no provider call, no database, no deployment.

    python3 implementation/phase-16/examples/executable_run.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import registries                                                        # noqa: E402
from domain import (                                                     # noqa: E402
    Criticality, DecisionRequirement, EvidenceRequirement, ExecutionMode, PlanStage,
    PlannerOutput, PrerequisiteState, ReviewRequirement, RoleRequirement, WorkMode, WorkPlan,
)
from handoff import build_trigger, idempotency_key                       # noqa: E402
from preflight import run_preflight                                      # noqa: E402
from store import ActivationStore                                        # noqa: E402


def main():
    roles = sorted(registries.approved_roles())
    steward = [r for r in roles if "knowledge_evidence" in r][0]
    legal = [r for r in roles if "legal_regulatory" in r][0]
    review = sorted(registries.approved_review_profiles())[0]

    plan = PlannerOutput(
        request_id="request.eib-pack",
        request_text="Pull together what we do on the grant pilot and get me something to send.",
        intent_id="intent.eib-pack",
        scope_ref="scope.project.grant_pilot",
        scope_ancestry=("scope.org.root", "scope.programme.eu", "scope.project.grant_pilot"),
        objective="Produce a governed external response on the pilot's data handling",
        deliverables=("An evidence position", "A legal position", "A sendable draft"),
        primary_work_mode=WorkMode.UNKNOWN,
        secondary_work_modes=(WorkMode.ANALYSIS, WorkMode.DRAFTING),
        criticality=Criticality.ENHANCED_DECISION_GRADE,
        execution_mode=ExecutionMode.COMPOSE,
        role_requirements=(
            RoleRequirement(steward, "what the record shows"),
            RoleRequirement(legal, "the regulatory position"),
        ),
        review_requirements=(ReviewRequirement(review, mandatory=True),),
        decision_requirements=(
            DecisionRequirement("decision.external_publication", "send outside the entity"),),
        evidence_requirements=(
            EvidenceRequirement("artifact.dpa@3", PrerequisiteState.RESOLVED),
            EvidenceRequirement("artifact.audit_note@1",
                                PrerequisiteState.FUTURE_GOVERNANCE_REFERENCE,
                                required_before_first_act=False),
        ),
        work_plan=WorkPlan("work_plan.grant_pilot_response", 1, (
            PlanStage("S1", steward, (), False, "evidence position"),
            PlanStage("S2", legal, ("S1",), False, "regulatory position"),
            PlanStage("S3", steward, ("S1", "S2"), False, "draft carrying both verbatim"),
            PlanStage("S4", None, ("S3",), True, ""),
        )),
    )

    print("request          :", plan.request_text)
    print("scope            :", plan.scope_ref)
    print("primary mode     :", plan.primary_work_mode.value,
          "  secondary:", [m.value for m in plan.secondary_work_modes])
    print("criticality      :", plan.criticality.value)

    result = run_preflight(plan, author_identity="human.alice",
                           reviewer_identity="human.bob")
    print("\npreflight        :", result.state.value)
    basis = ActivationStore().issue(result.basis)
    print("execution basis  :", basis.ref, "-", basis.status.value)
    print("  mode           :", basis.execution_mode.value,
          "| work plan:", basis.work_plan_ref, "| workflow:", basis.workflow_ref)
    print("  is_approval    :", basis.is_approval, " is_authority:", basis.is_authority)
    print("  reviews        : REQUIRED, unsatisfied ->", list(basis.review_requirements))
    print("  rights         : REQUIRED, unexercised ->", list(basis.decision_requirements))

    trigger = build_trigger(basis, plan, originator="human.alice",
                            sensitivity="CONFIDENTIAL", residency="EU")
    print("\ntrigger          :", trigger.command,
          "| creates_run:", trigger.creates_run, "| is_approval:", trigger.is_approval)
    print("idempotency key  :", trigger.idempotency_key)
    print("intake answers the envelope makes available (it performs none of them):")
    for number, answer in sorted(trigger.intake_answers().items()):
        print("   check %d -> %s" % (number, answer))
    print("\nplanned work item specs (never Work Items, never Tasks):")
    for spec in trigger.planned_work_item_specs:
        print("   %-46s stage %s  role=%s  gate=%s"
              % (spec.spec_id, spec.stage_id, spec.role_envelope, spec.is_gate))

    print("\nnothing above created a run, satisfied a review, exercised a Right,")
    print("registered a capability, or promoted a Work Plan to a Workflow.")


if __name__ == "__main__":
    main()
