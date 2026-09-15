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


def a_workflow_ref():
    """`workflow.<id>@<version>` at the version the approved card DECLARES.

    Not `@1`. The registry used to invent version 1 for every Workflow, so every MATCH test
    bound a version nobody approved and still passed.
    """
    wf = a_workflow()
    return "%s@%s" % (wf, registries.approved_workflows()[wf])


def a_skill_for(role_ref):
    """A CARDED Skill the authoritative mapping records positively relate to that Role.

    Drawn from `carded_skills()`, never from `approved_skills()`. A mapping is evidence that a
    capability is APPLICABLE to a Role; it says nothing whatever about whether that Skill is
    individually approved, and these fixtures must not imply that it is.
    """
    for skill in sorted(registries.carded_skills()):
        ok, _why = registries.skill_is_compatible_with_role(skill, role_ref)
        if ok:
            return skill
    raise AssertionError("no carded Skill is mapped to %s" % role_ref)


def a_mapped_role():
    """An approved Role that the mapping records positively relate to a CARDED Skill."""
    for role in sorted(registries.approved_roles()):
        for skill in sorted(registries.carded_skills()):
            if registries.skill_is_compatible_with_role(skill, role)[0]:
                return role
    raise AssertionError("no approved Role is mapped to a carded Skill")


class simulated_individual_skill_approval(object):
    """A LABELLED TEST DOUBLE that temporarily makes named Skills individually approved.

    It creates no approval and asserts none. It exists because the downstream Skill gates —
    Role compatibility and wrong-Role binding — sit BEHIND the individual-approval gate, and
    with no Skill individually approved in this repository today those gates are unreachable
    and would lose their coverage silently.

    Every use is explicit, scoped to one assertion and restored afterwards. No test uses it to
    claim that a Skill IS approved: the test that asks that question reads the real
    `approved_skills()` and expects the empty set.
    """

    def __init__(self, *skills):
        self.skills = set(skills)
        self._original = None

    def __enter__(self):
        self._original = registries.approved_skills
        registries.approved_skills = lambda: set(self.skills)
        return self

    def __exit__(self, *_exc):
        registries.approved_skills = self._original
        return False


def issued(plan, **preflight_kwargs):
    """Preflight, then ISSUE. A basis that was never issued produces no trigger at all."""
    store = ActivationStore()
    result = run_preflight(plan, **preflight_kwargs)
    assert result.basis is not None, result.detail
    return store, store.issue(result.basis)


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
        plan = base(execution_mode=ExecutionMode.MATCH, work_plan=None,
                    workflow_ref=a_workflow_ref())
        result = run_preflight(plan)
        self.assertIs(result.state, PlannerState.VALIDATED, result.detail)
        self.assertIs(result.basis.status, BasisStatus.EXECUTABLE)
        store, basis = issued(plan)
        trigger = build_trigger(basis, plan, originator="human.alice", store=store)
        self.assertEqual(trigger.command, "CreateWorkflowRun")
        self.assertEqual(trigger.workflow_ref, a_workflow_ref())
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
                    workflow_ref="%s@99.9" % a_workflow())
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
        store, basis = issued(plan)
        trigger = build_trigger(basis, plan, originator="human.alice", store=store)
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
        store, basis = issued(plan)
        trigger = build_trigger(basis, plan, originator="human.alice", store=store)
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
        # The issued basis is immutable, so the caller's copy is not silently rewritten: the
        # STORE is the authority on lifecycle, and it now reports STALE.
        self.assertIs(store.issued(first.ref).status, BasisStatus.STALE)
        with self.assertRaises(ActivationError):
            build_trigger(first, changed, originator="human.alice", store=store)

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
        # Snapshots are values, not shared mutable objects, so identity is the wrong question;
        # what matters is that the SAME issued basis came back and no second one was minted.
        self.assertEqual(first.ref, second.ref)
        self.assertEqual(first.payload_seal(), second.payload_seal())
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
        plan = base(execution_mode=ExecutionMode.MATCH, work_plan=None,
                    workflow_ref=a_workflow_ref(),
                    criticality=Criticality.ENHANCED_DECISION_GRADE,
                    review_requirements=(ReviewRequirement(a_review(), True),),
                    decision_requirements=(DecisionRequirement(a_right(), "publish"),))
        store, basis = issued(plan)
        trigger = build_trigger(basis, plan, originator="human.alice", store=store)
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
        store, basis = issued(plan)
        trigger = build_trigger(basis, plan, originator="human.alice", store=store)
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
        plan = base()
        store, basis = issued(plan)
        for status in (BasisStatus.DRAFT, BasisStatus.VALIDATED, BasisStatus.BLOCKED,
                       BasisStatus.STALE, BasisStatus.SUPERSEDED):
            with self.assertRaises(ActivationError, msg=status.value):
                build_trigger(basis.with_status(status), plan,
                              originator="human.alice", store=store)


# =========================================================== B1 — registry eligibility


class TestRegistryEligibility(unittest.TestCase):
    """Eligibility is declared evidence, never a slug or a mention."""

    #: The three IDs the previous display-name slugger invented. Each is what you get by
    #: splitting an ampersand into its own word: "Asset O&M", "ESG / E&S", "FP&A".
    MISPARSED = (
        "role.asset_o_m_technical_operations_specialist",
        "role.esg_e_s_specialist",
        "role.fp_a_management_finance_specialist",
    )
    #: What the Role Cards actually declare.
    DECLARED = (
        "role.asset_om_technical_operations_specialist",
        "role.esg_es_specialist",
        "role.fpa_management_finance_specialist",
    )

    def test_the_three_misparsed_role_ids_are_not_eligible(self):
        approved = registries.approved_roles()
        for invented in self.MISPARSED:
            self.assertNotIn(invented, approved)
            result = run_preflight(base(
                role_requirements=(RoleRequirement(invented, "a conclusion"),),
                work_plan=WorkPlan("work_plan.mp", 1, (
                    PlanStage("S1", invented, (), False, "draft"),))))
            self.assertIs(result.state, PlannerState.BLOCKED, invented)
            self.assertIn(BlockReason.UNREGISTERED_CAPABILITY, result.reasons)

    def test_the_three_declared_role_ids_are_eligible(self):
        approved = registries.approved_roles()
        for declared in self.DECLARED:
            self.assertIn(declared, approved)
            result = run_preflight(base(
                role_requirements=(RoleRequirement(declared, "a conclusion"),),
                work_plan=WorkPlan("work_plan.dc", 1, (
                    PlanStage("S1", declared, (), False, "draft"),))))
            self.assertIs(result.state, PlannerState.VALIDATED, result.detail)

    def test_the_approved_role_universe_is_exactly_fifty_nine(self):
        self.assertEqual(len(registries.approved_roles()), 59)

    def test_every_eligible_identity_resolves_to_a_declaring_card(self):
        for kind, identities in (("role", registries.approved_roles()),
                                 ("skill", registries.approved_skills()),
                                 ("review", registries.approved_review_profiles()),
                                 ("decision", registries.approved_decision_rights()),
                                 ("workflow", set(registries.approved_workflows()))):
            for identity in identities:
                self.assertIsNotNone(registries.card_path(kind, identity),
                                     "%s has no declaring card" % identity)

    def test_carded_skills_are_declared_cards_and_not_thereby_approved(self):
        """Card existence is evidence of a CARD. It is not evidence of approval."""
        carded = registries.carded_skills()
        self.assertEqual(len(carded), 6, sorted(carded))
        self.assertIn("skill.source_verification", carded)
        self.assertEqual(registries.approved_skills(), set(),
                         "no Skill card carries explicit individual approval evidence")
        self.assertLessEqual(registries.approved_skills(), carded)

    def test_an_uncarded_universe_entry_is_not_eligible(self):
        """A candidate held in a consolidation group is a mention, not a registration."""
        uncarded = {
            "review": "review.legal_regulatory",
            "decision": "decision.stage_gate_progression_routine",
            "workflow": "workflow.feasibility_study_preparation",
            "skill": "skill.scope_definition",
        }
        self.assertNotIn(uncarded["review"], registries.approved_review_profiles())
        self.assertNotIn(uncarded["decision"], registries.approved_decision_rights())
        self.assertNotIn(uncarded["workflow"], registries.approved_workflows())
        # Checked against the CARDED set, the wider of the two: absent from it is absent from
        # the approved set a fortiori, and checking the empty set would prove nothing.
        self.assertNotIn(uncarded["skill"], registries.carded_skills())

    def test_an_uncarded_workflow_is_blocked_under_match(self):
        plan = base(execution_mode=ExecutionMode.MATCH, work_plan=None,
                    workflow_ref="workflow.feasibility_study_preparation@0.1")
        result = run_preflight(plan)
        self.assertIs(result.state, PlannerState.BLOCKED)
        self.assertIn(BlockReason.WORKFLOW_NOT_APPROVED, result.reasons)

    def test_an_uncarded_review_profile_blocks(self):
        plan = base(criticality=Criticality.ENHANCED_DECISION_GRADE,
                    review_requirements=(ReviewRequirement("review.legal_regulatory", True),))
        result = run_preflight(plan)
        self.assertIs(result.state, PlannerState.BLOCKED)
        self.assertIn(BlockReason.REVIEW_UNRESOLVED, result.reasons)

    def test_an_uncarded_decision_right_blocks(self):
        plan = base(decision_requirements=(
            DecisionRequirement("decision.stage_gate_progression_routine", "progress"),))
        result = run_preflight(plan)
        self.assertIs(result.state, PlannerState.BLOCKED)
        self.assertIn(BlockReason.NO_APPLICABLE_DECISION_RIGHT, result.reasons)

    def test_a_retired_id_named_only_by_a_supersedes_line_is_not_eligible(self):
        """`Supersedes: `skill.legal_source_currency_check`` names a RETIRED identity."""
        self.assertNotIn("skill.legal_source_currency_check", registries.carded_skills())

    def test_the_approved_workflow_version_is_the_one_the_card_declares(self):
        for wf, version in registries.approved_workflows().items():
            self.assertNotEqual(version, 1, "%s: version 1 was invented, never declared" % wf)
            self.assertRegex(version, r"^\d+\.\d+$")


# =========================================================== B2 — digest completeness


class TestMaterialDigestCompleteness(unittest.TestCase):
    """Every load-bearing input is inside the digest; every exclusion is stated."""

    def test_every_planner_field_is_classified(self):
        import dataclasses as _dc
        declared = {f.name for f in _dc.fields(PlannerOutput)}
        self.assertEqual(declared, PlannerOutput.classified_fields())

    def test_only_the_request_text_is_presentation_only(self):
        self.assertEqual(PlannerOutput.PRESENTATION_ONLY_FIELDS, ("request_text",))

    def _digest_changes(self, **overrides):
        return base().material_digest() != base(**overrides).material_digest()

    def test_a_clarification_changes_the_digest(self):
        self.assertTrue(self._digest_changes(clarifications=(
            ClarificationRequirement("Bullets or prose?", False, "prose"),)))

    def test_a_clarifications_default_changes_the_digest(self):
        one = base(clarifications=(ClarificationRequirement("Q?", False, "prose"),))
        two = base(clarifications=(ClarificationRequirement("Q?", False, "bullets"),))
        self.assertNotEqual(one.material_digest(), two.material_digest())

    def test_a_clarifications_blocking_flag_changes_the_digest(self):
        one = base(clarifications=(ClarificationRequirement("Q?", False, "prose"),))
        two = base(clarifications=(ClarificationRequirement("Q?", True),))
        self.assertNotEqual(one.material_digest(), two.material_digest())

    def test_scope_ancestry_changes_the_digest(self):
        self.assertTrue(self._digest_changes(
            scope_ancestry=("scope.org.root", "scope.programme.x", "scope.project.alpha")))

    def test_the_orchestrator_policy_reference_changes_the_digest(self):
        self.assertTrue(self._digest_changes(orchestrator_policy_ref="policy.strict@2"))

    def test_a_stages_expected_artifact_changes_the_digest(self):
        one = base()
        two = base(work_plan=WorkPlan("work_plan.001", 1, (
            PlanStage("S1", a_role(), (), False, "a materially different artifact"),
            PlanStage("S2", None, ("S1",), True, ""))))
        self.assertNotEqual(one.material_digest(), two.material_digest())

    def test_a_declared_open_item_changes_the_digest(self):
        self.assertTrue(self._digest_changes(unknown_fields=("residency",)))

    def test_an_evidence_requirements_timing_flag_changes_the_digest(self):
        one = base(evidence_requirements=(EvidenceRequirement(
            "artifact.x@1", PrerequisiteState.RESOLVED, required_before_first_act=True),))
        two = base(evidence_requirements=(EvidenceRequirement(
            "artifact.x@1", PrerequisiteState.RESOLVED, required_before_first_act=False),))
        self.assertNotEqual(one.material_digest(), two.material_digest())

    def test_each_omitted_family_makes_the_issued_basis_unusable(self):
        """The point of the digest: a load-bearing change must invalidate, not merely differ."""
        cases = {
            "clarification": dict(clarifications=(
                ClarificationRequirement("Bullets or prose?", False, "prose"),)),
            "scope ancestry": dict(
                scope_ancestry=("scope.org.root", "scope.programme.x", "scope.project.alpha")),
            "policy binding": dict(orchestrator_policy_ref="policy.strict@2"),
            "expected artifact": dict(work_plan=WorkPlan("work_plan.001", 1, (
                PlanStage("S1", a_role(), (), False, "something else"),
                PlanStage("S2", None, ("S1",), True, "")))),
            "open items": dict(unknown_fields=("residency",)),
        }
        for label, override in cases.items():
            plan = base()
            store, basis = issued(plan)
            changed = base(**override)
            stale = store.invalidate_on_material_change(plan.request_id,
                                                        changed.material_digest())
            self.assertTrue(stale, "%s did not invalidate the basis" % label)
            self.assertIs(store.issued(basis.ref).status, BasisStatus.STALE, label)
            with self.assertRaises(ActivationError, msg=label):
                build_trigger(basis, changed, originator="human.alice", store=store)


# =========================================================== B3 — basis integrity


class TestBasisIntegrity(unittest.TestCase):

    def test_an_issued_basis_is_immutable(self):
        _store, basis = issued(base())
        for field, value in (("status", BasisStatus.BLOCKED), ("scope_ref", "scope.other"),
                             ("planning_digest", "0" * 64), ("is_approval", True)):
            with self.assertRaises(Exception, msg=field):
                setattr(basis, field, value)

    def test_an_issued_basis_may_not_be_marked_stale_by_its_holder(self):
        _store, basis = issued(base())
        with self.assertRaises(GovernanceError):
            basis.mark_stale()
        with self.assertRaises(GovernanceError):
            basis.mark_superseded("execution_basis.x@2")

    def test_a_never_issued_basis_produces_no_trigger(self):
        plan = base()
        candidate = run_preflight(plan).basis          # valid, EXECUTABLE, and never issued
        with self.assertRaises(ActivationError):
            build_trigger(candidate, plan, originator="human.alice",
                          store=ActivationStore())

    def test_a_trigger_may_not_be_built_without_the_issuing_store(self):
        plan = base()
        _store, basis = issued(plan)
        with self.assertRaises(ActivationError):
            build_trigger(basis, plan, originator="human.alice")

    def test_a_fabricated_basis_is_refused(self):
        import dataclasses as _dc
        plan = base()
        store, basis = issued(plan)
        forged = _dc.replace(basis, basis_id="execution_basis.forged")
        with self.assertRaises(ActivationError):
            build_trigger(forged, plan, originator="human.alice", store=store)

    def test_a_tampered_basis_is_refused_field_by_field(self):
        import dataclasses as _dc
        # A plan that actually CARRIES every field the tamper list edits: blanking an empty
        # tuple is not a tamper, and a test that blanked one would be asserting nothing.
        plan = base(criticality=Criticality.ENHANCED_DECISION_GRADE,
                    review_requirements=(ReviewRequirement(a_review(), True),),
                    decision_requirements=(DecisionRequirement(a_right(), "publish"),),
                    evidence_requirements=(EvidenceRequirement(
                        "artifact.x@1", PrerequisiteState.RESOLVED),))
        store, basis = issued(plan)
        self.assertTrue(basis.review_requirements and basis.decision_requirements
                        and basis.evidence_requirements)
        tampers = {
            "scope_ref": "scope.project.someone_elses",
            "scope_ancestry": ("scope.org.root",),
            "planning_digest": "0" * 64,
            "implementation_spec_version": "phase-14@deadbeef",
            "orchestrator_policy_ref": "policy.permissive@9",
            "criticality": Criticality.ROUTINE if plan.criticality is not Criticality.ROUTINE
            else Criticality.CRITICAL,
            "review_requirements": (),
            "decision_requirements": (),
            "evidence_requirements": (),
            "skill_bindings": ("skill.invented",),
            "role_bindings": ("role.invented",),
            "work_plan_ref": "work_plan.someone_elses@1",
            "is_approval": True,
            "is_authority": True,
            "version": 7,
        }
        for field, value in tampers.items():
            with self.assertRaises(ActivationError, msg=field):
                build_trigger(_dc.replace(basis, **{field: value}), plan,
                              originator="human.alice", store=store)

    def test_cross_request_reuse_is_refused_even_when_the_digests_match(self):
        """Two requests, byte-identical planning material, one basis. Not transferable."""
        first = base(request_id="request.aaa", intent_id="intent.aaa")
        second = base(request_id="request.bbb", intent_id="intent.bbb")
        self.assertEqual(first.material_digest(), second.material_digest(),
                         "the premise of this test is that the digests DO match")
        store, basis = issued(first)
        with self.assertRaises(ActivationError):
            build_trigger(basis, second, originator="human.alice", store=store)

    def test_a_trigger_may_not_be_recorded_against_an_unissued_basis(self):
        plan = base()
        candidate = run_preflight(plan).basis
        with self.assertRaises(ActivationError):
            ActivationStore().record_trigger(idempotency_key(plan), candidate.ref)

    def test_lineage_survives_stale_and_superseded(self):
        store = ActivationStore()
        plan = base()
        first = store.issue(run_preflight(plan).basis)
        changed = base(objective="A materially different objective")
        store.invalidate_on_material_change(plan.request_id, changed.material_digest())
        second = store.issue(run_preflight(changed).basis)
        lineage = store.lineage(plan.request_id)
        self.assertEqual(len(lineage), 2)
        self.assertEqual(lineage[0][0], first.ref)
        self.assertEqual(lineage[0][1], "SUPERSEDED")
        self.assertEqual(lineage[0][2], second.ref)
        self.assertEqual(second.version, 2)
        self.assertEqual(second.supersedes, first.ref)
        self.assertIsNotNone(store.issued(first.ref),
                             "a superseded basis stays readable; history is append-only")

    def test_a_basis_claiming_to_be_an_approval_is_never_issued(self):
        import dataclasses as _dc
        candidate = run_preflight(base()).basis
        for field in ("is_approval", "is_authority"):
            with self.assertRaises(GovernanceError, msg=field):
                ActivationStore().issue(_dc.replace(candidate, **{field: True}))


# =========================================================== B4 — composition bindings


class TestCompositionBindings(unittest.TestCase):

    def test_duplicate_stage_ids_block(self):
        plan = base(work_plan=WorkPlan("work_plan.dup", 1, (
            PlanStage("S1", a_role(), (), False, "draft"),
            PlanStage("S1", a_role(), (), False, "a different artifact"),
            PlanStage("S2", None, ("S1",), True, ""))))
        result = run_preflight(plan)
        self.assertIs(result.state, PlannerState.BLOCKED)
        self.assertIn(BlockReason.DUPLICATE_STAGE_IDENTITY, result.reasons)

    def test_an_unregistered_stage_owner_blocks(self):
        plan = base(work_plan=WorkPlan("work_plan.uo", 1, (
            PlanStage("S1", "role.invented_by_the_planner", (), False, "draft"),
            PlanStage("S2", None, ("S1",), True, ""))))
        result = run_preflight(plan)
        self.assertIs(result.state, PlannerState.BLOCKED)
        self.assertIn(BlockReason.UNREGISTERED_CAPABILITY, result.reasons)

    def test_a_stage_owner_the_plan_declares_no_conclusion_for_blocks(self):
        other = sorted(registries.approved_roles())[5]
        plan = base(work_plan=WorkPlan("work_plan.nd", 1, (
            PlanStage("S1", other, (), False, "draft"),
            PlanStage("S2", None, ("S1",), True, ""))))
        result = run_preflight(plan)
        self.assertIs(result.state, PlannerState.BLOCKED)
        self.assertIn(BlockReason.STAGE_OWNER_UNRESOLVED, result.reasons)

    def test_a_non_gate_stage_with_no_owner_blocks(self):
        plan = base(work_plan=WorkPlan("work_plan.no", 1, (
            PlanStage("S1", None, (), False, "draft"),
            PlanStage("S2", None, ("S1",), True, ""))))
        result = run_preflight(plan)
        self.assertIs(result.state, PlannerState.BLOCKED)
        self.assertIn(BlockReason.STAGE_OWNER_UNRESOLVED, result.reasons)

    def test_a_positive_mapping_is_applicability_and_not_eligibility(self):
        """The parser says the pair is applicable; preflight still refuses it.

        This is the shape the corrected B1 semantics give the whole Skill path: a mapping
        record answers "may this Role use this capability at all", and individual approval
        answers "may this Skill be assigned in execution". Only the second one opens the gate.
        """
        role = a_mapped_role()
        skill = a_skill_for(role)
        ok, relationship = registries.skill_is_compatible_with_role(skill, role)
        self.assertTrue(ok, relationship)
        self.assertIn(skill, registries.carded_skills())
        self.assertNotIn(skill, registries.approved_skills())

        result = run_preflight(base(
            role_requirements=(RoleRequirement(role, "a substantive domain conclusion"),),
            skill_requirements=(SkillRequirement(skill, role),),
            work_plan=WorkPlan("work_plan.rs", 1, (
                PlanStage("S1", role, (), False, "draft"),))))
        self.assertIs(result.state, PlannerState.BLOCKED, result.detail)
        self.assertIn(BlockReason.UNREGISTERED_CAPABILITY, result.reasons)

    def test_a_skill_bound_to_the_wrong_role_blocks(self):
        """Reached through the labelled double: this gate sits behind individual approval."""
        role = a_mapped_role()
        skill = a_skill_for(role)
        wrong = next(r for r in sorted(registries.approved_roles())
                     if not registries.skill_is_compatible_with_role(skill, r)[0])
        with simulated_individual_skill_approval(skill):
            result = run_preflight(base(
                role_requirements=(RoleRequirement(wrong, "a substantive domain conclusion"),),
                skill_requirements=(SkillRequirement(skill, wrong),),
                work_plan=WorkPlan("work_plan.ws", 1, (
                    PlanStage("S1", wrong, (), False, "draft"),))))
        self.assertIs(result.state, PlannerState.BLOCKED)
        self.assertIn(BlockReason.SKILL_ROLE_INCOMPATIBLE, result.reasons)
        self.assertEqual(registries.approved_skills(), set(), "the double must be restored")

    def test_a_skill_bound_to_a_role_the_mapping_allows_passes_once_approved(self):
        """Also through the double, so the positive downstream path keeps its coverage."""
        role = a_mapped_role()
        skill = a_skill_for(role)
        with simulated_individual_skill_approval(skill):
            result = run_preflight(base(
                role_requirements=(RoleRequirement(role, "a substantive domain conclusion"),),
                skill_requirements=(SkillRequirement(skill, role),),
                work_plan=WorkPlan("work_plan.rs2", 1, (
                    PlanStage("S1", role, (), False, "draft"),))))
        self.assertIs(result.state, PlannerState.VALIDATED, result.detail)
        self.assertEqual(registries.approved_skills(), set(), "the double must be restored")

    def test_a_skill_claimed_for_an_unresolved_role_blocks(self):
        role = a_mapped_role()
        skill = a_skill_for(role)
        # Blocked twice over, and both are asserted: unapproved first, and — behind the
        # double — for a Role that does not resolve.
        result = run_preflight(base(
            role_requirements=(RoleRequirement(role, "a substantive domain conclusion"),),
            skill_requirements=(SkillRequirement(skill, "role.not_a_role"),),
            work_plan=WorkPlan("work_plan.ur", 1, (
                PlanStage("S1", role, (), False, "draft"),))))
        self.assertIs(result.state, PlannerState.BLOCKED)
        self.assertIn(BlockReason.UNREGISTERED_CAPABILITY, result.reasons)
        with simulated_individual_skill_approval(skill):
            result = run_preflight(base(
                role_requirements=(RoleRequirement(role, "a substantive domain conclusion"),),
                skill_requirements=(SkillRequirement(skill, "role.not_a_role"),),
                work_plan=WorkPlan("work_plan.ur2", 1, (
                    PlanStage("S1", role, (), False, "draft"),))))
        self.assertIs(result.state, PlannerState.BLOCKED)
        self.assertIn(BlockReason.UNREGISTERED_CAPABILITY, result.reasons)

    def test_an_unmapped_but_approved_skill_blocks(self):
        """Silence in the authoritative mapping records is not permission."""
        role = a_mapped_role()
        unmapped = next(
            (s for s in sorted(registries.carded_skills())
             if not registries.skill_is_compatible_with_role(s, role)[0]), None)
        self.assertIsNotNone(unmapped)
        with simulated_individual_skill_approval(unmapped):
            result = run_preflight(base(
                role_requirements=(RoleRequirement(role, "a substantive domain conclusion"),),
                skill_requirements=(SkillRequirement(unmapped, role),),
                work_plan=WorkPlan("work_plan.um", 1, (
                    PlanStage("S1", role, (), False, "draft"),))))
        self.assertIs(result.state, PlannerState.BLOCKED)
        self.assertIn(BlockReason.SKILL_ROLE_INCOMPATIBLE, result.reasons)
        self.assertEqual(registries.approved_skills(), set(), "the double must be restored")

    def test_planned_spec_identities_are_unique(self):
        plan = base(work_plan=WorkPlan("work_plan.many", 1, tuple(
            [PlanStage("S%d" % n, a_role(), (), False, "draft") for n in range(1, 8)]
            + [PlanStage("G", None, ("S1",), True, "")])))
        store, basis = issued(plan)
        trigger = build_trigger(basis, plan, originator="human.alice", store=store)
        ids = [s.spec_id for s in trigger.planned_work_item_specs]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(ids), 8)


if __name__ == "__main__":                                       # pragma: no cover
    unittest.main()
