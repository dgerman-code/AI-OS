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
    PrerequisiteState, ReviewRequirement, RoleRequirement, SkillRequirement, WorkMode,
    WorkPlan,
)
from handoff import build_trigger                                        # noqa: E402
from preflight import run_preflight                                      # noqa: E402
from store import ActivationStore                                        # noqa: E402


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


def show_basis_refusals():
    """What the trigger builder refuses, on a plan that is otherwise entirely valid."""
    import dataclasses

    good = plan()
    store = ActivationStore()
    candidate = run_preflight(good).basis
    basis = store.issue(candidate)

    attempts = (
        ("never-issued basis", lambda: build_trigger(
            candidate, good, originator="human.a", store=ActivationStore())),
        ("no issuing store presented", lambda: build_trigger(
            basis, good, originator="human.a")),
        ("tampered scope on an issued basis", lambda: build_trigger(
            dataclasses.replace(basis, scope_ref="scope.someone_elses"), good,
            originator="human.a", store=store)),
        ("basis claiming to be an approval", lambda: build_trigger(
            dataclasses.replace(basis, is_approval=True), good,
            originator="human.a", store=store)),
        ("cross-request reuse of a valid basis", lambda: build_trigger(
            basis, plan(request_id="request.other", intent_id="intent.other"),
            originator="human.a", store=store)),
        ("holder marks an issued basis stale", basis.mark_stale),
    )
    for label, attempt in attempts:
        try:
            attempt()
        except (ActivationError, GovernanceError) as exc:
            print("  REFUSED  %-42s %s" % (label, str(exc)[:88]))
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
         workflow_ref=sorted(registries.approved_workflows())[0] + "@99.9")
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
    role = sorted(registries.approved_roles())[0]
    show("duplicate stage identity",
         work_plan=WorkPlan("work_plan.dup", 1, (PlanStage("S1", role, (), False, "x"),
                                                 PlanStage("S1", role, (), False, "y"))))
    show("stage owner the plan declares nothing for",
         work_plan=WorkPlan("work_plan.nd", 1, (
             PlanStage("S1", sorted(registries.approved_roles())[7], (), False, "x"),)))
    show("Skill bound to a Role the mappings do not allow",
         skill_requirements=(SkillRequirement(
             sorted(registries.approved_skills())[0], role),))

    print()
    show_basis_refusals()

    print("\nEach refusal names what is missing. None is a warning attached to something")
    print("that proceeded, and none was resolved by the planner deciding for itself.")


if __name__ == "__main__":
    main()
