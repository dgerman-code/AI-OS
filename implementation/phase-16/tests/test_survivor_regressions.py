"""Targeted regressions for the final Phase 16 survivor remediation."""

import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import registries
from domain import (
    ActivationError, BasisStatus, Criticality, ExecutionBasis, ExecutionMode,
    IMPLEMENTATION_SPEC_VERSION, PlanStage, PlannerOutput, PlannerState,
    RoleRequirement, WorkMode, WorkPlan,
)
from preflight import run_preflight
from store import ActivationStore


def a_role():
    return sorted(registries.approved_roles())[0]


def plan(**overrides):
    fields = dict(
        request_id="request.survivor",
        request_text="Prepare the response.",
        intent_id="intent.survivor",
        scope_ref="scope.project.alpha",
        scope_ancestry=("scope.org.root", "scope.project.alpha"),
        objective="Produce a governed response",
        deliverables=("draft",),
        primary_work_mode=WorkMode.DRAFTING,
        secondary_work_modes=(),
        criticality=Criticality.ROUTINE,
        execution_mode=ExecutionMode.COMPOSE,
        role_requirements=(RoleRequirement(a_role(), "substantive domain conclusion"),),
        work_plan=WorkPlan("work_plan.survivor", 1, (
            PlanStage("S1", a_role(), (), False, "draft"),
        )),
    )
    fields.update(overrides)
    return PlannerOutput(**fields)


class SurvivorRegressions(unittest.TestCase):

    def test_phase4_architecture_approval_does_not_individually_approve_skills(self):
        self.assertTrue(registries.carded_skills(), "fixture must contain exemplar Skill cards")
        self.assertEqual(registries.approved_skills(), set(),
                         "no current Skill card has explicit individual human approval evidence")

    def test_boundary_prose_does_not_create_capex_lifecycle_mapping(self):
        ok, _why = registries.skill_is_compatible_with_role(
            "skill.lifecycle_cost_analysis", "role.capex_cost_engineering_specialist")
        self.assertFalse(ok)

    def test_blank_owned_conclusion_blocks(self):
        role = a_role()
        result = run_preflight(plan(
            role_requirements=(RoleRequirement(role, "   "),),
            work_plan=WorkPlan("work_plan.blank", 1, (
                PlanStage("S1", role, (), False, "draft"),))))
        self.assertIs(result.state, PlannerState.BLOCKED)
        self.assertIsNone(result.basis)

    def test_fabricated_basis_cannot_be_issued_after_blocked_preflight(self):
        blocked_plan = plan(criticality=Criticality.CRITICAL, review_requirements=())
        blocked = run_preflight(blocked_plan)
        self.assertIs(blocked.state, PlannerState.BLOCKED)
        self.assertIsNone(blocked.basis)

        fabricated = ExecutionBasis(
            basis_id="execution_basis.fabricated",
            version=1,
            request_id=blocked_plan.request_id,
            intent_id=blocked_plan.intent_id,
            scope_ref=blocked_plan.scope_ref,
            scope_ancestry=blocked_plan.scope_ancestry,
            execution_mode=blocked_plan.execution_mode,
            criticality=blocked_plan.criticality,
            planning_digest=blocked_plan.material_digest(),
            implementation_spec_version=IMPLEMENTATION_SPEC_VERSION,
            orchestrator_policy_ref=blocked_plan.orchestrator_policy_ref,
            status=BasisStatus.EXECUTABLE,
            work_plan_ref=blocked_plan.work_plan.ref,
            role_bindings=tuple(r.role_ref for r in blocked_plan.role_requirements),
        )
        with self.assertRaises(ActivationError):
            ActivationStore().issue(fabricated)

    def test_preflight_provenance_is_one_time(self):
        p = plan()
        result = run_preflight(p)
        self.assertIs(result.state, PlannerState.VALIDATED)
        store = ActivationStore()
        store.issue(result.basis)
        with self.assertRaises(ActivationError):
            ActivationStore().issue(result.basis)


if __name__ == "__main__":
    unittest.main()
