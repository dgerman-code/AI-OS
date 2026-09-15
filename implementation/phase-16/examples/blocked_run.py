"""Phase 16 — the refusals, each printed with the reason it names.

Status: PROPOSED. No network, no provider call, no database, no deployment.

    python3 implementation/phase-16/examples/blocked_run.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import registries                                                        # noqa: E402
from domain import (                                                     # noqa: E402
    ActivationError, ClarificationRequirement, Criticality, DecisionRequirement,
    EvidenceRequirement, ExecutionMode, GovernanceError, PlanStage, PlannerOutput,
    PrerequisiteState, ReviewRequirement, RoleRequirement, WorkMode, WorkPlan,
)
from preflight import run_preflight                                      # noqa: E402


def plan(**overrides):
    role = sorted(registries.approved_roles())[0]
    fields = dict(
        request_id="request.blocked", request_text="...", intent_id="intent.blocked",
        scope_ref="scope.project.alpha",
        scope_ancestry=("scope.org.root", "scope.project.alpha"),
        objective="o", deliverables=("d",),
        primary_work_mode=WorkMode.DRAFTING, secondary_work_modes=(),
        criticality=Criticality.ROUTINE, execution_mode=ExecutionMode.COMPOSE,
        role_requirements=(RoleRequirement(role, "the conclusion"),),
        work_plan=WorkPlan("work_plan.b", 1, (PlanStage("S1", role, (), False, "x"),)),
    )
    fields.update(overrides)
    return PlannerOutput(**fields)


def show(label, **overrides):
    try:
        result = run_preflight(plan(**overrides))
    except (ActivationError, GovernanceError) as exc:
        print("  REFUSED  %-42s %s" % (label, str(exc)[:88]))
        return
    if result.state.value in ("BLOCKED", "CLARIFICATION_REQUIRED"):
        print("  %-8s %-42s %s" % (result.state.value[:8], label,
                                   ", ".join(r.value for r in result.reasons)))
    else:
        print("  PASSED   %-42s (unexpected)" % label)


def main():
    review = sorted(registries.approved_review_profiles())[0]
    print("Phase 16 — what the activation preflight refuses, and what it names\n")
    show("no applicable Decision Right",
         decision_requirements=(DecisionRequirement(None, "send externally"),))
    show("required review unresolved at the band",
         criticality=Criticality.ENHANCED_DECISION_GRADE, review_requirements=())
    show("material ambiguity",
         clarifications=(ClarificationRequirement("Which project?", blocking=True),))
    show("unregistered Role inferred",
         role_requirements=(RoleRequirement("role.not_registered", "x", registered=False),))
    show("no approved owner for a required conclusion",
         role_requirements=(RoleRequirement(None, "communication strategy"),))
    show("unapproved Workflow under MATCH",
         execution_mode=ExecutionMode.MATCH, work_plan=None,
         workflow_ref="workflow.invented@1")
    show("stale Workflow version under MATCH",
         execution_mode=ExecutionMode.MATCH, work_plan=None,
         workflow_ref=sorted(registries.approved_workflows())[0] + "@99")
    show("dangling UNKNOWN prerequisite",
         evidence_requirements=(EvidenceRequirement("a@?", PrerequisiteState.UNKNOWN),))
    show("criticality unresolved", criticality=None)
    show("planner marks a review satisfied",
         criticality=Criticality.ENHANCED_DECISION_GRADE,
         review_requirements=(ReviewRequirement(review, True, satisfied=True),))
    show("planner exercises a Decision Right",
         decision_requirements=(DecisionRequirement("decision.external_publication", "s",
                                                    exercised=True),))
    show("caller injects a governed record",
         injected_governed_records=("decision_record",))
    show("blocking clarification carries a default",
         clarifications=(ClarificationRequirement("Which?", True, default_if_unanswered="a"),))

    print("\nEach refusal names what is missing. None is a warning attached to something")
    print("that proceeded, and none was resolved by the planner deciding for itself.")


if __name__ == "__main__":
    main()
