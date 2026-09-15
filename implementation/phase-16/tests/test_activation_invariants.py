"""Phase 16 — the planner-to-execution invariants, one test per mandatory acceptance scenario.

Status: PROPOSED. Run with:

    python3 -m unittest discover -s implementation/phase-16/tests -v

Where a rule says something is impossible, the test asserts the refusal, not a return value: a
rule that can be violated and merely logged is not enforced.
"""

import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import registries                                                         # noqa: E402
from domain import (                                                      # noqa: E402
    ActivationError, BasisStatus, BlockReason, ClarificationRequirement, Criticality,
    DecisionRequirement, EvidenceRequirement, ExecutionMode, GovernanceError, PlanStage,
    PlannerOutput, PlannerState, PrerequisiteState, ReviewRequirement, RoleRequirement,
    SkillRequirement, WorkMode, WorkPlan,
)
from handoff import build_trigger, idempotency_key                        # noqa: E402
from preflight import run_preflight                                       # noqa: E402
from store import ActivationStore                                         # noqa: E402


def a_role():
    return sorted(registries.approved_roles())[0]


def a_review():
    return sorted(registries.approved_review_profiles())[0]


def a_right():
    return "decision.external_publication"


def a_workflow():
    return sorted(registries.approved_workflows())[0]


def base(**overrides):
    fields = dict(
        request_id="request.001",
        request_text="Prepare the partner response.",
        intent_id="intent.001",
        scope_ref="scope.project.alpha",
        scope_ancestry=("scope.org.root", "scope.project.alpha"),
        objective="Produce a governed response",
        deliverables=("A drafted response",),
        primary_work_mode=WorkMode.DRAFTING,
        secondary_work_modes=(),
        criticality=Criticality.ROUTINE,
        execution_mode=ExecutionMode.COMPOSE,
        role_requirements=(RoleRequirement(a_role(), "the domain conclusion"),),
        work_plan=WorkPlan("work_plan.001", 1, (
            PlanStage("S1", a_role(), (), False, "draft"),
            PlanStage("S2", None, ("S1",), True, ""),
        )),
    )
    fields.update(overrides)
    return PlannerOutput(**fields)


class TestMatchPath(unittest.TestCase):
    """Scenario 1 — simple MATCH reaches intake through an approved Workflow at its version."""

    def test_match_produces_an_executable_basis_and_a_trigger(self):
        wf = a_workflow()
        plan = base(execution_mode=ExecutionMode.MATCH, work_plan=None,
                    workflow_ref="%s@1" % wf)
        result = run_preflight(plan)
        self.assertIs(result.state, PlannerState.VALIDATED, result.detail)
        self.assertIs(result.basis.status, BasisStatus.EXECUTABLE)
        trigger = build_trigger(result.basis, plan, originator="human.alice")
        self.assertEqual(trigger.command, "CreateWorkflowRun")
        self.assertEqual(trigger.workflow_ref, "%s@1" % wf)
        self.assertIsNone(trigger.work_plan_ref)
        self.assertFalse(trigger.creates_run)
        self.assertEqual(set(trigger.intake_answers()), {1, 2, 3, 4, 5, 6, 7})

    def test_unapproved_workflow_blocks(self):
        plan = base(execution_mode=ExecutionMode.MATCH, work_plan=None,
                    workflow_ref="workflow.not_a_real_workflow@1")
        result = run_preflight(plan)
        self.assertIs(result.state, PlannerState.BLOCKED)
        self.assertIn(BlockReason.WORKFLOW_NOT_APPROVED, result.reasons)

    def test_stale_workflow_version_blocks(self):
        """Scenario 11 — a version that is not the approved one is not a binding."""
        plan = base(execution_mode=ExecutionMode.MATCH, work_plan=None,
                    workflow_ref="%s@99" % a_workflow())
        result = run_preflight(plan)
        self.assertIs(result.state, PlannerState.BLOCKED)
        self.assertIn(BlockReason.WORKFLOW_VERSION_STALE, result.reasons)


class TestComposePath(unittest.TestCase):
    """Scenario 2 — COMPOSE reaches intake on its Execution Basis, creating no Workflow."""

    def test_compose_reaches_intake_without_creating_a_workflow_definition(self):
        plan = base()
        result = run_preflight(plan)
        self.assertIs(result.state, PlannerState.VALIDATED, result.detail)
        basis = result.basis
        self.assertIs(basis.status, BasisStatus.EXECUTABLE)
        self.assertIsNone(basis.workflow_ref)
        self.assertEqual(basis.work_plan_ref, "work_plan.001@1")
        trigger = build_trigger(basis, plan, originator="human.alice")
        self.assertIsNone(trigger.workflow_ref)
        self.assertTrue(trigger.work_plan_ref.startswith("work_plan."))
        self.assertNotIn("workflow.", trigger.work_plan_ref)

    def test_a_work_plan_may_not_take_a_workflow_identity(self):
        with self.assertRaises(GovernanceError):
            WorkPlan("workflow.smuggled", 1, ())

    def test_a_gate_stage_has_no_role_participation(self):
        plan = base(work_plan=WorkPlan("work_plan.002", 1, (
            PlanStage("S1", a_role(), (), True, ""),)))
        result = run_preflight(plan)
        self.assertIs(result.state, PlannerState.BLOCKED)

    def test_a_dependency_cycle_blocks(self):
        plan = base(work_plan=WorkPlan("work_plan.003", 1, (
            PlanStage("S1", a_role(), ("S2",), False, "x"),
            PlanStage("S2", a_role(), ("S1",), False, "y"))))
        result = run_preflight(plan)
        self.assertIs(result.state, PlannerState.BLOCKED)


class TestAuthorityAndReview(unittest.TestCase):

    def test_missing_decision_right_blocks(self):
        """Scenario 3 — an act with no applicable approved Right does not reach intake."""
        plan = base(decision_requirements=(
            DecisionRequirement(None, "send the response externally"),))
        result = run_preflight(plan)
        self.assertIs(result.state, PlannerState.BLOCKED)
        self.assertIn(BlockReason.NO_APPLICABLE_DECISION_RIGHT, result.reasons)

    def test_high_criticality_without_a_required_review_blocks(self):
        """Scenario 4 — the band's review floor is not waivable by planning."""
        plan = base(criticality=Criticality.ENHANCED_DECISION_GRADE, review_requirements=())
        result = run_preflight(plan)
        self.assertIs(result.state, PlannerState.BLOCKED)
        self.assertIn(BlockReason.REVIEW_UNRESOLVED, result.reasons)

    def test_planning_may_not_mark_a_review_satisfied(self):
        plan = base(criticality=Criticality.ENHANCED_DECISION_GRADE,
                    review_requirements=(ReviewRequirement(a_review(), True, satisfied=True),))
        with self.assertRaises(GovernanceError):
            run_preflight(plan)

    def test_planning_may_not_exercise_a_right(self):
        plan = base(decision_requirements=(
            DecisionRequirement(a_right(), "send", exercised=True),))
        with self.assertRaises(GovernanceError):
            run_preflight(plan)

    def test_the_basis_itself_exercises_nothing(self):
        result = run_preflight(base())
        with self.assertRaises(GovernanceError):
            result.basis.exercise(a_right())
        with self.assertRaises(GovernanceError):
            result.basis.satisfy_review(a_review())
        self.assertFalse(result.basis.is_approval)
        self.assertFalse(result.basis.is_authority)

    def test_author_as_final_critical_reviewer_is_a_sod_failure(self):
        """Scenario 12 — separation of duties at identity level."""
        result = run_preflight(base(), author_identity="human.alice",
                               reviewer_identity="human.alice")
        self.assertIs(result.state, PlannerState.BLOCKED)
        self.assertIn(BlockReason.SOD_VIOLATION, result.reasons)


class TestClarificationAndCapability(unittest.TestCase):

    def test_material_ambiguity_requires_clarification_and_does_not_activate(self):
        """Scenario 5 — CLARIFICATION_REQUIRED yields no basis at all."""
        plan = base(clarifications=(
            ClarificationRequirement("Which project is this?", blocking=True),))
        result = run_preflight(plan)
        self.assertIs(result.state, PlannerState.CLARIFICATION_REQUIRED)
        self.assertIsNone(result.basis)
        self.assertFalse(result.executable)

    def test_a_blocking_clarification_may_carry_no_default(self):
        plan = base(clarifications=(
            ClarificationRequirement("Which project?", True, default_if_unanswered="alpha"),))
        with self.assertRaises(ActivationError):
            run_preflight(plan)

    def test_unregistered_role_blocks_and_registers_nothing(self):
        """Scenario 6 — an inferred capability that does not exist is not assignable."""
        before = set(registries.approved_roles())
        plan = base(role_requirements=(
            RoleRequirement("role.communication_difficult_conversations_specialist",
                            "communication strategy", registered=False),))
        result = run_preflight(plan)
        self.assertIs(result.state, PlannerState.BLOCKED)
        self.assertIn(BlockReason.UNREGISTERED_CAPABILITY, result.reasons)
        self.assertEqual(before, set(registries.approved_roles()),
                         "the approved Role universe was mutated by a planning attempt")

    def test_unregistered_skill_blocks(self):
        plan = base(skill_requirements=(
            SkillRequirement("skill.boundary_formulation", a_role(), registered=False),))
        result = run_preflight(plan)
        self.assertIs(result.state, PlannerState.BLOCKED)
        self.assertIn(BlockReason.UNREGISTERED_CAPABILITY, result.reasons)

    def test_no_approved_owner_blocks(self):
        plan = base(role_requirements=(RoleRequirement(None, "communication strategy"),))
        result = run_preflight(plan)
        self.assertIs(result.state, PlannerState.BLOCKED)
        self.assertIn(BlockReason.NO_APPROVED_ROLE_OWNS_CONCLUSION, result.reasons)


class TestEvidenceAndPrerequisites(unittest.TestCase):

    def test_unknown_prerequisite_is_dangling_and_blocks(self):
        """Scenario 13 — a plain UNKNOWN is never a deferral."""
        plan = base(evidence_requirements=(
            EvidenceRequirement("artifact.model@?", PrerequisiteState.UNKNOWN),))
        result = run_preflight(plan)
        self.assertIs(result.state, PlannerState.BLOCKED)
        self.assertIn(BlockReason.DANGLING_PREREQUISITE, result.reasons)

    def test_a_future_reference_required_before_the_first_act_blocks(self):
        plan = base(evidence_requirements=(
            EvidenceRequirement("artifact.model@2", PrerequisiteState.FUTURE_GOVERNANCE_REFERENCE,
                                required_before_first_act=True),))
        result = run_preflight(plan)
        self.assertIn(BlockReason.EVIDENCE_UNSATISFIED, result.reasons)

    def test_a_legitimately_deferred_reference_passes_as_declared(self):
        plan = base(evidence_requirements=(
            EvidenceRequirement("artifact.later@1", PrerequisiteState.FUTURE_GOVERNANCE_REFERENCE,
                                required_before_first_act=False),))
        result = run_preflight(plan)
        self.assertIs(result.state, PlannerState.VALIDATED, result.detail)
        trigger = build_trigger(result.basis, plan, originator="human.alice")
        self.assertIn(("artifact.later@1", "FUTURE_GOVERNANCE_REFERENCE"),
                      trigger.prerequisite_refs)


class TestVersioningAndReplay(unittest.TestCase):

    def test_material_replan_supersedes_the_prior_basis(self):
        """Scenario 7 — the old basis is stale and cannot produce a trigger."""
        store = ActivationStore()
        plan = base()
        first = store.issue(run_preflight(plan).basis)
        self.assertIs(first.status, BasisStatus.EXECUTABLE)

        changed = base(deliverables=("A drafted response", "A published statement"))
        store.invalidate_on_material_change(plan.request_id, changed.material_digest())
        self.assertIs(first.status, BasisStatus.STALE)
        with self.assertRaises(ActivationError):
            build_trigger(first, changed, originator="human.alice")

        second = store.issue(run_preflight(changed).basis)
        self.assertEqual(second.version, 2)
        self.assertEqual(second.supersedes, first.ref)
        self.assertEqual(len(store.history(plan.request_id)), 2,
                         "governed history is append-only; the old basis still exists")

    def test_non_material_change_creates_no_new_governed_version(self):
        """Scenario 8 — a reworded request is not a new plan."""
        one = base(request_text="Prepare the partner response.")
        two = base(request_text="Please prepare the partner response, thanks.")
        self.assertEqual(one.material_digest(), two.material_digest())
        store = ActivationStore()
        first = store.issue(run_preflight(one).basis)
        second = store.issue(run_preflight(two).basis)
        self.assertIs(first, second)
        self.assertEqual(len(store.history(one.request_id)), 1)

    def test_duplicate_request_is_idempotent(self):
        """Scenario 9 — the same request at the same version creates one lineage."""
        store = ActivationStore()
        plan = base()
        basis = store.issue(run_preflight(plan).basis)
        key = idempotency_key(plan)
        lineage_a, created_a = store.record_trigger(key, basis.ref)
        lineage_b, created_b = store.record_trigger(key, basis.ref)
        self.assertTrue(created_a)
        self.assertFalse(created_b)
        self.assertEqual(lineage_a, lineage_b)

    def test_a_material_replan_gets_a_different_idempotency_key(self):
        self.assertNotEqual(
            idempotency_key(base()),
            idempotency_key(base(criticality=Criticality.ENHANCED_DECISION_GRADE,
                                 review_requirements=(ReviewRequirement(a_review(), True),))))


class TestLearningBoundary(unittest.TestCase):

    def test_a_repeated_pattern_emits_only_a_proposed_candidate(self):
        """Scenario 10 — observation never promotes."""
        store = ActivationStore()
        for n in range(4):
            store.observe_composed_pattern("shape-abc", "work_plan.%03d@1" % n)
        self.assertEqual(len(store.candidates), 1)
        candidate = store.candidates[0]
        self.assertEqual(candidate["status"], "PROPOSED")
        self.assertFalse(candidate["is_approved"])
        self.assertFalse(candidate["is_matchable"])
        self.assertFalse(hasattr(store, "register_workflow"),
                         "the store has no path that could register a Workflow")
        self.assertNotIn(candidate["candidate_id"], registries.approved_workflows())


class TestHandoffPurity(unittest.TestCase):

    def test_a_valid_handoff_contains_no_synthetic_authority_object(self):
        """Scenario 14 — the trigger carries requirements, never satisfied gates."""
        wf = a_workflow()
        plan = base(execution_mode=ExecutionMode.MATCH, work_plan=None,
                    workflow_ref="%s@1" % wf,
                    criticality=Criticality.ENHANCED_DECISION_GRADE,
                    review_requirements=(ReviewRequirement(a_review(), True),),
                    decision_requirements=(DecisionRequirement(a_right(), "publish"),))
        trigger = build_trigger(run_preflight(plan).basis, plan, originator="human.alice")
        rendered = repr(trigger).lower()
        for forbidden in ("decision_record", "review_instance", "gate_outcome",
                          "approval_state", "routing_decision"):
            self.assertNotIn(forbidden, rendered)
        self.assertFalse(trigger.is_approval)
        self.assertFalse(trigger.creates_run)

    def test_injected_governed_records_are_refused(self):
        """Scenario 15 — a caller-supplied Decision Record or Review Instance is rejected."""
        plan = base(injected_governed_records=("decision_record", "review_instance"))
        with self.assertRaises(GovernanceError):
            run_preflight(plan)

    def test_a_planned_spec_is_never_a_work_item(self):
        plan = base()
        trigger = build_trigger(run_preflight(plan).basis, plan, originator="human.alice")
        for spec in trigger.planned_work_item_specs:
            self.assertTrue(spec.spec_id.startswith("planned_work_item_spec."))
            self.assertNotIn("work_item.", spec.spec_id)
            self.assertFalse(hasattr(spec, "run_ref"))
            self.assertFalse(hasattr(spec, "assignment"))
            self.assertFalse(hasattr(spec, "model"))

    def test_the_planner_contract_carries_no_model_field(self):
        with self.assertRaises(GovernanceError):
            base(unknown_fields=("model_profile",))

    def test_a_non_executable_basis_produces_no_trigger(self):
        result = run_preflight(base())
        result.basis.status = BasisStatus.BLOCKED
        with self.assertRaises(ActivationError):
            build_trigger(result.basis, base(), originator="human.alice")


if __name__ == "__main__":                                       # pragma: no cover
    unittest.main()
