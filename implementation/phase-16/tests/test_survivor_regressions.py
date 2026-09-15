"""Targeted regressions for the final Phase 16 survivor remediation."""

import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

import dataclasses

import registries
from domain import (
    ActivationError, BasisStatus, BlockReason, Criticality, ExecutionBasis, ExecutionMode,
    IMPLEMENTATION_SPEC_VERSION, PlanStage, PlannerOutput, PlannerState,
    RoleRequirement, SkillRequirement, WorkMode, WorkPlan,
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

    def test_architecture_approval_makes_no_carded_skill_executable(self):
        """The consequence, not only the set. Every carded Skill still blocks at preflight."""
        workflow = sorted(registries.approved_workflows())[0]
        workflow_ref = "%s@%s" % (workflow, registries.approved_workflows()[workflow])
        for skill_ref in sorted(registries.carded_skills()):
            result = run_preflight(plan(
                request_id="request.b1.%s" % skill_ref,
                execution_mode=ExecutionMode.MATCH, work_plan=None,
                workflow_ref=workflow_ref,
                skill_requirements=(SkillRequirement(skill_ref, a_role()),)))
            self.assertIs(result.state, PlannerState.BLOCKED, skill_ref)
            self.assertIsNone(result.basis, skill_ref)
            self.assertIn(BlockReason.UNREGISTERED_CAPABILITY, result.reasons, skill_ref)

    def test_the_individual_approval_test_excludes_the_phase_level_record(self):
        """A phase-level architecture approval may never satisfy individual approval."""
        source = open(os.path.join(os.path.dirname(HERE), "registries.py"),
                      encoding="utf-8").read()
        self.assertIn('name == "phase-4-final-approval.md"', source)
        self.assertIn("must not be interpreted as a mass status promotion",
                      open(os.path.join(REPO, "reviews", "phase-4-final-approval.md"),
                           encoding="utf-8").read())

    def test_boundary_prose_does_not_create_capex_lifecycle_mapping(self):
        """The exact case the review named: prose that DENIES a mapping must not create one."""
        mappings = registries.role_skill_mappings()
        for role_ref in ("role.capex_cost_engineering_specialist",
                         "role.asset_om_technical_operations_specialist"):
            self.assertNotIn("skill.lifecycle_cost_analysis", mappings.get(role_ref, {}),
                             role_ref)
            ok, why = registries.skill_is_compatible_with_role(
                "skill.lifecycle_cost_analysis", role_ref)
            self.assertFalse(ok, why)
        # And the Role the boundary protects still holds the mapping, so the parser has not
        # simply stopped reading the record.
        self.assertIn(
            mappings.get("role.technical_feasibility_lead", {}).get(
                "skill.lifecycle_cost_analysis"),
            registries.COMPATIBLE_RELATIONSHIPS)

    def test_blank_whitespace_and_placeholder_owned_conclusions_block(self):
        role = a_role()
        for label, conclusion in (("empty", ""), ("spaces", "   "), ("newline", "\n\t "),
                                  ("dash", "-"), ("ellipsis", "..."), ("tbd", "TBD"),
                                  ("todo", "todo"), ("unknown", "Unknown"), ("na", "N/A"),
                                  ("none", "none"), ("placeholder", "Placeholder"),
                                  ("to be determined", "To Be Determined"),
                                  ("to be defined", "to be defined")):
            result = run_preflight(plan(
                request_id="request.oc.%s" % label,
                role_requirements=(RoleRequirement(role, conclusion),),
                work_plan=WorkPlan("work_plan.blank", 1, (
                    PlanStage("S1", role, (), False, "draft"),))))
            self.assertIs(result.state, PlannerState.BLOCKED, label)
            self.assertIsNone(result.basis, label)
            self.assertIn(BlockReason.NO_APPROVED_ROLE_OWNS_CONCLUSION, result.reasons, label)

    def test_a_substantive_owned_conclusion_does_not_block(self):
        role = a_role()
        result = run_preflight(plan(
            request_id="request.oc.ok",
            role_requirements=(RoleRequirement(role, "the regulatory position on transfer"),),
            work_plan=WorkPlan("work_plan.ok", 1, (
                PlanStage("S1", role, (), False, "draft"),))))
        self.assertIs(result.state, PlannerState.VALIDATED, result.detail)

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

    def test_an_equal_value_copy_of_a_genuine_basis_cannot_be_issued(self):
        """Provenance is bound to the object preflight returned, not to its field values."""
        result = run_preflight(plan(request_id="request.copy"))
        self.assertIs(result.state, PlannerState.VALIDATED, result.detail)
        copy = dataclasses.replace(result.basis)
        self.assertEqual(copy.payload_seal(), result.basis.payload_seal())
        with self.assertRaises(ActivationError):
            ActivationStore().issue(copy)

    def test_a_non_executable_candidate_is_not_issuable(self):
        result = run_preflight(plan(request_id="request.notexec"))
        with self.assertRaises(ActivationError):
            ActivationStore().issue(result.basis.with_status(BasisStatus.VALIDATED))

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
