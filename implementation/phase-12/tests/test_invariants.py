"""Phase 12 MVP — deterministic tests for the approved architecture invariants.

Status: PROPOSED. Run with:

    python3 -m unittest discover -s implementation/phase-12/tests -v

Every test names the approved rule it holds. Where a rule is about something being impossible,
the test asserts the raise, not a return value: a rule that can be violated and merely logged
is not enforced. `TestStructuralBypasses` is the independent audit's findings, one test each.
"""

import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "examples"))

from adapters import (  # noqa: E402
    InMemoryDecisionDesk, InMemoryReviewerDesk, InMemoryRouter, StubModel,
)
from domain import (  # noqa: E402
    ALLOWED_TRANSITIONS, AUTOMATICALLY_RETRYABLE, AgentInstanceRef, AppendOnlyError,
    ArtifactRef, CONTINUING_GATE_OUTCOMES, Canonicality, CanonicalRecordRef, CredentialRef,
    DecisionRecord, DecisionRecordRef, DecisionRightRef, EVIDENCE_CONTRACT, EvidenceError,
    ExecutionEventLog, GateInstance, GateKind, GateOutcome, GateRequirement,
    GateRequirementRef, GovernanceError, GovernancePosture, HandoffRef, HumanAuthorityRef,
    HumanInterventionRecord, HumanWorkCompletion, HumanWorkRef, IdentityError, InterventionRef,
    LineageError, ModelProfileRef, ModelRef, ModelResult, NEVER_AUTOMATICALLY_RETRYABLE,
    Origin, OrchestratorRef, POSTURE_PERMITS_COMPLETION, PrerequisiteEvidence, PrerequisiteRef,
    RaceOutcome, RecordStore, RetryClass, ReviewInstance, ReviewInstanceRef, ReviewProfileRef,
    RoleRef, RouterOutcome, RouterRef, RoutingDecision, RoutingDecisionRef, RoutingRequest,
    RoutingRequestRef, RunPhase, RuntimeEventRef, SEPARATION_CHAIN, ScopeBinding, ScopeRef,
    ScopeTransferAuthorisation, ScopeTransferRef, StateAccessError, StorageRecordRef, Task,
    TaskRef, TerminalOutcome, TransitionError, WaitReason, WorkItem, WorkItemRef,
    WorkflowDefinition, WorkflowRef, WorkflowRunRef, require,
)
from orchestrator import Orchestrator  # noqa: E402

SCOPE = ScopeBinding(ScopeRef("project.apollo"), frozenset({"INTERNAL"}), "EU")
AUTHOR = RoleRef("role.author")
TASK = TaskRef("task.t")


def review_gate(ref="gate.r", profile="rp", independence="INDEPENDENT"):
    return GateRequirement(GateRequirementRef(ref), GateKind.REVIEW,
                           review_profile=ReviewProfileRef(profile),
                           independence_class=independence)


def decision_gate(ref="gate.d", right="dr"):
    return GateRequirement(GateRequirementRef(ref), GateKind.DECISION,
                           decision_right=DecisionRightRef(right))


def simple_task(gates=(), retry=RetryClass.SAFE_AUTOMATIC_RETRY, capability=""):
    return Task(TASK, "T", AUTHOR, retry, gates=gates, capability=capability)


def build(rights=None, reviews=None, eligible=None, missing_right_for=()):
    router = InMemoryRouter(RouterRef("router.phase9"), eligible=eligible or {},
                            missing_right_for=missing_right_for)
    return Orchestrator(router, InMemoryReviewerDesk(reviews or {}),
                        InMemoryDecisionDesk(rights or {}), StubModel())


def started(orch, task, run_id="run.t", workflow="wf.t", version="v1"):
    definition = WorkflowDefinition(WorkflowRef(workflow), version, (task,), SCOPE)
    run = orch.create_run(definition, WorkflowRunRef(run_id))
    return run, orch.activate_stage(run, task.ref)


# ===========================================================================================


class TestIdentitySeparation(unittest.TestCase):
    """`ROLE != AGENT INSTANCE != ... != HUMAN AUTHORITY`, enforced by type."""

    def test_chain_has_twenty_one_objects(self):
        self.assertEqual(len(SEPARATION_CHAIN), 21)
        self.assertEqual(len({cls.KIND for cls in SEPARATION_CHAIN}), 21)

    def test_same_id_different_kind_is_not_equal(self):
        self.assertNotEqual(RoleRef("x"), AgentInstanceRef("x"))
        self.assertNotEqual(ModelRef("x"), ModelProfileRef("x"))
        self.assertNotEqual(CredentialRef("x"), HumanAuthorityRef("x"))

    def test_role_id_cannot_be_used_where_agent_instance_is_required(self):
        with self.assertRaises(IdentityError):
            require(RoleRef("a"), AgentInstanceRef, "agent instance slot")

    def test_structured_identity_collapse_attempt_fails(self):
        for offered, required in ((RoleRef("x"), AgentInstanceRef),
                                  (RouterRef("x"), OrchestratorRef),
                                  (DecisionRightRef("x"), DecisionRecordRef),
                                  (ArtifactRef("x"), CanonicalRecordRef),
                                  (RuntimeEventRef("x"), ArtifactRef)):
            with self.assertRaises(IdentityError):
                require(offered, required)


class TestConstructionTimeTypeEnforcement(unittest.TestCase):
    """Audit finding 1: every governed object validates its references at construction."""

    def test_model_result_rejects_wrong_reference_types(self):
        good = dict(run=WorkflowRunRef("r"), work_item=WorkItemRef("wi"),
                    routing_decision=RoutingDecisionRef("rd"), model=ModelRef("m"),
                    content="t")
        ModelResult(**good)                                   # the well-formed one exists
        for field, wrong in (("work_item", TaskRef("t")), ("model", ModelProfileRef("mp")),
                             ("run", WorkItemRef("wi")),
                             ("routing_decision", RoutingRequestRef("rr"))):
            bad = dict(good, **{field: wrong})
            with self.assertRaises(IdentityError):
                ModelResult(**bad)

    def test_routing_decision_rejects_wrong_reference_types(self):
        good = dict(ref=RoutingDecisionRef("rd"), request=RoutingRequestRef("rr"),
                    run=WorkflowRunRef("r"), work_item=WorkItemRef("wi"),
                    outcome=RouterOutcome.NO_ELIGIBLE_MODEL, decided_by=RouterRef("router"))
        RoutingDecision(**good)
        for field, wrong in (("decided_by", OrchestratorRef("o")),
                             ("work_item", TaskRef("t")),
                             ("request", RoutingDecisionRef("rd"))):
            with self.assertRaises(IdentityError):
                RoutingDecision(**dict(good, **{field: wrong}))

    def test_gate_instance_rejects_wrong_reference_types(self):
        requirement = decision_gate()
        GateInstance(requirement, WorkflowRunRef("r"), WorkItemRef("wi"))
        with self.assertRaises(IdentityError):
            GateInstance(requirement, WorkflowRunRef("r"), TaskRef("t"))
        with self.assertRaises(IdentityError):
            GateInstance(requirement, WorkflowRunRef("r"), WorkItemRef("wi"),
                         GateOutcome.SATISFIED, "not a reference")

    def test_every_governed_object_enforces_its_references(self):
        """A sweep, so a new object added without enforcement is noticed."""
        cases = [
            (ReviewInstance, dict(ref=ReviewInstanceRef("ri"),
                                  requirement=GateRequirementRef("g"),
                                  run=WorkflowRunRef("r"), work_item=WorkItemRef("wi"),
                                  review_profile=ReviewProfileRef("rp"),
                                  outcome=GateOutcome.SATISFIED,
                                  reviewer=HumanAuthorityRef("h"),
                                  independence_class="IND"), "reviewer", ModelRef("m")),
            (DecisionRecord, dict(ref=DecisionRecordRef("dr"),
                                  requirement=GateRequirementRef("g"),
                                  run=WorkflowRunRef("r"), work_item=WorkItemRef("wi"),
                                  decision_right=DecisionRightRef("right"),
                                  outcome=GateOutcome.SATISFIED,
                                  decided_by=HumanAuthorityRef("h")),
             "decided_by", AgentInstanceRef("a")),
            (HumanWorkCompletion, dict(requirement=GateRequirementRef("g"),
                                       run=WorkflowRunRef("r"), work_item=WorkItemRef("wi"),
                                       human_work=HumanWorkRef("hw"),
                                       outcome=GateOutcome.SATISFIED,
                                       completed_by=HumanAuthorityRef("h")),
             "human_work", TaskRef("t")),
            (PrerequisiteEvidence, dict(requirement=GateRequirementRef("g"),
                                        run=WorkflowRunRef("r"), work_item=WorkItemRef("wi"),
                                        prerequisite=PrerequisiteRef("pr"),
                                        outcome=GateOutcome.SATISFIED,
                                        evaluated_against=StorageRecordRef("sr")),
             "evaluated_against", ArtifactRef("art")),
            (WorkItem, dict(ref=WorkItemRef("wi"), task=TaskRef("t"), run=WorkflowRunRef("r"),
                            workflow=WorkflowRef("wf"), workflow_version="v1",
                            retry_class=RetryClass.SAFE_AUTOMATIC_RETRY,
                            required_role=AUTHOR), "required_role", AgentInstanceRef("a")),
        ]
        for cls, good, field, wrong in cases:
            cls(**good)
            with self.assertRaises(IdentityError, msg="%s.%s" % (cls.__name__, field)):
                cls(**dict(good, **{field: wrong}))

    def test_model_result_cannot_be_declared_canonical_or_human(self):
        base = dict(run=WorkflowRunRef("r"), work_item=WorkItemRef("wi"),
                    routing_decision=RoutingDecisionRef("rd"), model=ModelRef("m"),
                    content="t")
        with self.assertRaises(GovernanceError):
            ModelResult(canonicality=Canonicality.CANONICAL, **base)
        with self.assertRaises(GovernanceError):
            ModelResult(origin=Origin.HUMAN_AUTHORED, **base)


class TestLineageBinding(unittest.TestCase):
    """Audit finding 2: lineage is bound, not asserted."""

    def test_work_item_carries_its_whole_lineage(self):
        orch = build()
        run, item = started(orch, simple_task())
        self.assertEqual((item.run, item.task, item.workflow, item.workflow_version),
                         (run.ref, TASK, WorkflowRef("wf.t"), "v1"))

    def test_undeclared_task_cannot_be_activated(self):
        orch = build()
        run, _ = started(orch, simple_task())
        with self.assertRaises(LineageError):
            orch.activate_stage(run, TaskRef("task.undeclared"))

    def test_a_task_from_another_definition_is_not_accepted(self):
        orch = build()
        run, _ = started(orch, simple_task())
        with self.assertRaises(LineageError):
            orch.activate_stage(run, TaskRef("task.other"))

    def test_a_work_item_from_another_run_is_refused(self):
        orch = build()
        run_a, item_a = started(orch, simple_task(), "run.a")
        run_b, _ = started(orch, simple_task(), "run.b")
        with self.assertRaises(LineageError):
            orch.assign(run_b, item_a, AUTHOR)

    def test_a_gate_of_another_work_item_is_refused(self):
        gate = decision_gate()
        orch = build(rights={"dr": (HumanAuthorityRef("h"), GateOutcome.SATISFIED)})
        run_a, item_a = started(orch, simple_task(gates=(gate,)), "run.a")
        run_b, item_b = started(orch, simple_task(gates=(gate,)), "run.b")
        with self.assertRaises(LineageError):
            orch.run_decision_gate(run_a, item_b, gate.ref)

    def test_a_run_from_another_orchestrator_is_refused(self):
        orch_a, orch_b = build(), build()
        run, _ = started(orch_a, simple_task())
        with self.assertRaises(StateAccessError):
            orch_b.activate_stage(run, TASK)


class TestRunStateIsNotBypassable(unittest.TestCase):
    """Audit finding 3: governed state cannot be set from outside the orchestrator."""

    def test_phase_posture_terminal_and_scope_are_read_only(self):
        orch = build()
        run, _ = started(orch, simple_task())
        for name, value in (("phase", RunPhase.RUNNING),
                            ("posture", GovernancePosture.GOVERNANCE_CLEAR),
                            ("terminal", TerminalOutcome.COMPLETED),
                            ("scope", SCOPE), ("ref", WorkflowRunRef("other"))):
            with self.assertRaises(StateAccessError, msg=name):
                setattr(run, name, value)

    def test_governed_collections_are_not_settable(self):
        orch = build()
        run, _ = started(orch, simple_task())
        for name in ("gates", "work_items", "attempts"):
            with self.assertRaises(StateAccessError):
                setattr(run, name, {})

    def test_state_token_is_required_to_mutate(self):
        orch = build()
        run, _ = started(orch, simple_task())
        with self.assertRaises(StateAccessError):
            run._state(object())

    def test_the_audit_bypass_no_longer_completes(self):
        """missing Right -> caller sets phase/posture/gates -> complete() succeeded."""
        gate = decision_gate(right="dr.absent")
        orch = build(rights={})
        run, item = started(orch, simple_task(gates=(gate,)))
        orch.run_decision_gate(run, item, gate.ref)
        self.assertIs(run.posture, GovernancePosture.AUTHORITY_ABSENT)
        with self.assertRaises(StateAccessError):
            setattr(run, "posture", GovernancePosture.GOVERNANCE_CLEAR)
        with self.assertRaises(Exception):
            orch.complete(run, TerminalOutcome.COMPLETED)


class TestGateRequirementIdentity(unittest.TestCase):
    """Audit finding 4: gates are identified objects, not `(work_item, kind)` keys."""

    def test_two_decision_gates_on_one_work_item_stay_two(self):
        first, second = decision_gate("gate.d1", "dr.one"), decision_gate("gate.d2", "dr.two")
        orch = build(rights={"dr.one": (HumanAuthorityRef("h"), GateOutcome.SATISFIED)})
        run, item = started(orch, simple_task(gates=(first, second)))
        self.assertEqual(len(run.gates()), 2)
        orch.run_decision_gate(run, item, first.ref)
        self.assertEqual(len(orch.unsatisfied_gates(run)), 1)
        with self.assertRaises(GovernanceError):
            orch.complete(run, TerminalOutcome.COMPLETED)

    def test_a_requirement_must_name_exactly_one_subject(self):
        with self.assertRaises(GovernanceError):
            GateRequirement(GateRequirementRef("g"), GateKind.DECISION)
        with self.assertRaises(GovernanceError):
            GateRequirement(GateRequirementRef("g"), GateKind.DECISION,
                            decision_right=DecisionRightRef("d"),
                            review_profile=ReviewProfileRef("rp"))

    def test_a_review_gate_must_declare_an_independence_class(self):
        with self.assertRaises(GovernanceError):
            GateRequirement(GateRequirementRef("g"), GateKind.REVIEW,
                            review_profile=ReviewProfileRef("rp"))

    def test_duplicate_gate_identities_are_refused(self):
        gate = decision_gate()
        with self.assertRaises(GovernanceError):
            Task(TASK, "T", AUTHOR, RetryClass.SAFE_AUTOMATIC_RETRY, gates=(gate, gate))


class TestEvidenceBinding(unittest.TestCase):
    """Audit finding 5: evidence must answer the exact requirement."""

    def test_each_gate_kind_has_exactly_one_admissible_evidence_type(self):
        self.assertEqual(set(EVIDENCE_CONTRACT), set(GateKind))
        self.assertEqual(len(set(EVIDENCE_CONTRACT.values())), 4)

    def _decision_setup(self):
        gate = decision_gate(right="dr.ok")
        orch = build(rights={"dr.ok": (HumanAuthorityRef("h"), GateOutcome.SATISFIED)})
        run, item = started(orch, simple_task(gates=(gate,)))
        return orch, run, item, gate

    def test_a_foreign_decision_record_cannot_satisfy_a_gate(self):
        orch, run, item, gate = self._decision_setup()
        forged = DecisionRecord(DecisionRecordRef("dr.x"), gate.ref,
                                WorkflowRunRef("run.elsewhere"), item.ref,
                                DecisionRightRef("dr.ok"), GateOutcome.SATISFIED,
                                HumanAuthorityRef("h"))
        with self.assertRaises(EvidenceError):
            orch.satisfy_gate_with(run, item, gate.ref, forged)

    def test_a_record_for_another_requirement_cannot_satisfy_this_one(self):
        orch, run, item, gate = self._decision_setup()
        forged = DecisionRecord(DecisionRecordRef("dr.x"), GateRequirementRef("gate.other"),
                                run.ref, item.ref, DecisionRightRef("dr.ok"),
                                GateOutcome.SATISFIED, HumanAuthorityRef("h"))
        with self.assertRaises(EvidenceError):
            orch.satisfy_gate_with(run, item, gate.ref, forged)

    def test_a_record_exercising_another_right_cannot_satisfy_this_one(self):
        orch, run, item, gate = self._decision_setup()
        forged = DecisionRecord(DecisionRecordRef("dr.x"), gate.ref, run.ref, item.ref,
                                DecisionRightRef("dr.somethingelse"), GateOutcome.SATISFIED,
                                HumanAuthorityRef("h"))
        with self.assertRaises(EvidenceError):
            orch.satisfy_gate_with(run, item, gate.ref, forged)

    def test_a_record_by_someone_who_holds_no_right_cannot_satisfy_it(self):
        orch, run, item, gate = self._decision_setup()
        forged = DecisionRecord(DecisionRecordRef("dr.x"), gate.ref, run.ref, item.ref,
                                DecisionRightRef("dr.ok"), GateOutcome.SATISFIED,
                                HumanAuthorityRef("human.passer-by"))
        with self.assertRaises(EvidenceError):
            orch.satisfy_gate_with(run, item, gate.ref, forged)

    def test_an_applied_outcome_may_not_contradict_the_evidence(self):
        orch, run, item, gate = self._decision_setup()
        record = DecisionRecord(DecisionRecordRef("dr.x"), gate.ref, run.ref, item.ref,
                                DecisionRightRef("dr.ok"), GateOutcome.NOT_SATISFIED,
                                HumanAuthorityRef("h"))
        with self.assertRaises(EvidenceError):
            orch.satisfy_gate_with(run, item, gate.ref, record, GateOutcome.SATISFIED)

    def test_an_adapter_tuple_may_not_override_its_own_record(self):
        """The desk answers SATISFIED while handing back a NOT_SATISFIED record."""
        gate = decision_gate(right="dr.ok")
        orch = build(rights={"dr.ok": (HumanAuthorityRef("h"), GateOutcome.NOT_SATISFIED)})
        run, item = started(orch, simple_task(gates=(gate,)))

        original = orch.decisions.decide

        def contradicting(request):
            _outcome, record = original(request)
            return (GateOutcome.SATISFIED, record)

        orch.decisions.decide = contradicting
        with self.assertRaises(EvidenceError):
            orch.run_decision_gate(run, item, gate.ref)

    def test_review_independence_mismatch_is_refused(self):
        gate = review_gate(profile="rp.ind", independence="INDEPENDENT")
        orch = build(reviews={"rp.ind": (GateOutcome.SATISFIED, HumanAuthorityRef("h"),
                                         "NOT_INDEPENDENT")})
        run, item = started(orch, simple_task(gates=(gate,)))
        with self.assertRaises(EvidenceError):
            orch.run_review_gate(run, item, gate.ref)

    def test_review_under_another_profile_is_refused(self):
        gate = review_gate(profile="rp.a")
        orch = build(reviews={"rp.a": (GateOutcome.SATISFIED, HumanAuthorityRef("h"),
                                       "INDEPENDENT")})
        run, item = started(orch, simple_task(gates=(gate,)))
        other = ReviewInstance(ReviewInstanceRef("ri.x"), gate.ref, run.ref, item.ref,
                               ReviewProfileRef("rp.b"), GateOutcome.SATISFIED,
                               HumanAuthorityRef("h"), "INDEPENDENT")
        with self.assertRaises(EvidenceError):
            orch.satisfy_gate_with(run, item, gate.ref, other)

    def test_review_instance_cannot_satisfy_a_human_work_gate(self):
        human = GateRequirement(GateRequirementRef("gate.hw"), GateKind.HUMAN_WORK,
                                human_work=HumanWorkRef("hw.1"))
        review = review_gate("gate.rv", "rp.any")
        orch = build(reviews={"rp.any": (GateOutcome.SATISFIED, HumanAuthorityRef("h"),
                                         "INDEPENDENT")})
        run, item = started(orch, simple_task(gates=(human, review)))
        instance = orch.run_review_gate(run, item, review.ref)
        with self.assertRaises(EvidenceError):
            orch.satisfy_gate_with(run, item, human.ref, instance)

    def test_decision_record_cannot_satisfy_a_governed_prerequisite_gate(self):
        prereq = GateRequirement(GateRequirementRef("gate.pre"),
                                 GateKind.GOVERNED_PREREQUISITE,
                                 prerequisite=PrerequisiteRef("pre.residency"))
        orch = build()
        run, item = started(orch, simple_task(gates=(prereq,)))
        record = DecisionRecord(DecisionRecordRef("dr.x"), prereq.ref, run.ref, item.ref,
                                DecisionRightRef("dr.any"), GateOutcome.SATISFIED,
                                HumanAuthorityRef("h"))
        with self.assertRaises(EvidenceError):
            orch.satisfy_gate_with(run, item, prereq.ref, record)

    def test_a_model_result_cannot_satisfy_any_gate(self):
        gate = decision_gate()
        orch = build()
        run, item = started(orch, simple_task(gates=(gate,)))
        result = ModelResult(run.ref, item.ref, RoutingDecisionRef("rd"), ModelRef("m"), "t")
        self.assertFalse(result.satisfies_gate())
        with self.assertRaises(EvidenceError):
            orch.satisfy_gate_with(run, item, gate.ref, result)

    def test_correct_evidence_does_satisfy_its_gate(self):
        prereq = GateRequirement(GateRequirementRef("gate.pre"),
                                 GateKind.GOVERNED_PREREQUISITE,
                                 prerequisite=PrerequisiteRef("pre.residency"))
        orch = build()
        run, item = started(orch, simple_task(gates=(prereq,)))
        evidence = PrerequisiteEvidence(prereq.ref, run.ref, item.ref,
                                        PrerequisiteRef("pre.residency"),
                                        GateOutcome.SATISFIED, StorageRecordRef("sr.1"))
        state = orch.record_prerequisite(run, item, prereq.ref, evidence)
        self.assertTrue(state.is_continuing())


class TestRoutingBinding(unittest.TestCase):
    """Audit finding 6: routing output is bound to the exact recorded request."""

    def test_routing_request_is_not_a_routing_decision(self):
        orch = build(eligible={"cap": (ModelRef("m"), ModelProfileRef("p"))})
        run, item = started(orch, simple_task(capability="cap"))
        request = orch.request_routing(run, item, "policy@1")
        decision = orch.router.route(request)
        self.assertIsInstance(request, RoutingRequest)
        self.assertIsInstance(decision, RoutingDecision)
        self.assertTrue(decision.answers(request))

    def test_a_decision_answering_another_request_is_refused(self):
        orch = build(eligible={"cap": (ModelRef("m"), ModelProfileRef("p"))})
        run, item = started(orch, simple_task(capability="cap"))
        request = orch.request_routing(run, item, "policy@1")
        other = RoutingDecision(RoutingDecisionRef("rd.x"), RoutingRequestRef("rr.other"),
                                run.ref, item.ref, RouterOutcome.ELIGIBLE_CANDIDATE,
                                RouterRef("router.phase9"), ModelRef("m"), ModelProfileRef("p"))
        with self.assertRaises(LineageError):
            orch.record_routing_decision(run, request, other)

    def test_a_fabricated_decision_cannot_reach_model_invocation(self):
        orch = build(eligible={"cap": (ModelRef("m"), ModelProfileRef("p"))})
        run, item = started(orch, simple_task(capability="cap"))
        fabricated = RoutingDecision(RoutingDecisionRef("rd.fake"),
                                     RoutingRequestRef("rr.fake"), run.ref, item.ref,
                                     RouterOutcome.ELIGIBLE_CANDIDATE,
                                     RouterRef("router.phase9"), ModelRef("model.chosen"),
                                     ModelProfileRef("profile.chosen"))
        with self.assertRaises(LineageError):
            orch.invoke_model(run, item, fabricated)

    def test_a_routing_decision_needs_a_router(self):
        with self.assertRaises(IdentityError):
            RoutingDecision(RoutingDecisionRef("rd"), RoutingRequestRef("rr"),
                            WorkflowRunRef("r"), WorkItemRef("wi"),
                            RouterOutcome.NO_ELIGIBLE_MODEL, decided_by=None)

    def test_no_eligible_model_blocks_and_there_is_no_fallback(self):
        orch = build(eligible={})
        run, item = started(orch, simple_task(capability="cap"))
        decision = orch.route(run, item, "policy@1")
        self.assertIs(decision.outcome, RouterOutcome.NO_ELIGIBLE_MODEL)
        self.assertIs(run.phase, RunPhase.BLOCKED)
        with self.assertRaises(GovernanceError):
            orch.invoke_model(run, item, decision)

    def test_routing_without_an_applicable_right_is_authority_absent(self):
        orch = build(missing_right_for=("cap",))
        run, item = started(orch, simple_task(capability="cap"))
        decision = orch.route(run, item, "policy@1")
        self.assertIs(decision.outcome, RouterOutcome.NO_APPLICABLE_DECISION_RIGHT)
        self.assertIs(run.phase, RunPhase.ESCALATED)
        self.assertIs(run.posture, GovernancePosture.AUTHORITY_ABSENT)

    def test_a_non_eligible_outcome_may_not_name_a_model(self):
        with self.assertRaises(GovernanceError):
            RoutingDecision(RoutingDecisionRef("rd"), RoutingRequestRef("rr"),
                            WorkflowRunRef("r"), WorkItemRef("wi"),
                            RouterOutcome.NO_ELIGIBLE_MODEL, RouterRef("router"),
                            model=ModelRef("m"), model_profile=ModelProfileRef("p"))


class TestRetryBinding(unittest.TestCase):
    """Audit finding 7: retry eligibility comes from the Work Item's lineage."""

    def test_seven_retry_classes_and_exactly_once_is_not_among_them(self):
        self.assertEqual(len(RetryClass), 7)
        self.assertEqual(AUTOMATICALLY_RETRYABLE & NEVER_AUTOMATICALLY_RETRYABLE, frozenset())

    def test_retry_class_cannot_be_substituted(self):
        orch = build()
        run, item = started(orch, simple_task(retry=RetryClass.NON_RETRYABLE_GOVERNED_ACT))
        self.assertIs(item.retry_class, RetryClass.NON_RETRYABLE_GOVERNED_ACT)
        orch.retry(run, item)                     # no Task argument exists to substitute
        self.assertIs(run.phase, RunPhase.ESCALATED)
        self.assertNotIn("retry:dispatched", orch.log.kinds())

    def test_non_replayable_external_effect_is_never_retried(self):
        orch = build()
        run, item = started(orch,
                            simple_task(retry=RetryClass.NON_REPLAYABLE_EXTERNAL_SIDE_EFFECT))
        orch.retry(run, item)
        self.assertIs(run.phase, RunPhase.ESCALATED)
        self.assertNotIn("retry:dispatched", orch.log.kinds())

    def test_retry_requiring_acknowledgement_waits_for_a_human(self):
        orch = build()
        run, item = started(
            orch, simple_task(retry=RetryClass.RETRY_REQUIRING_HUMAN_ACKNOWLEDGEMENT))
        orch.retry(run, item)
        self.assertIs(run.phase, RunPhase.WAITING)
        self.assertIs(run.wait_reason, WaitReason.WAITING_FOR_HUMAN)
        ack = HumanInterventionRecord(InterventionRef("iv.1"), run.ref,
                                      HumanAuthorityRef("h"), "acknowledge", "known and why")
        orch.retry(run, item, acknowledgement=ack)
        self.assertIn("retry:dispatched", orch.log.kinds())

    def test_an_acknowledgement_for_another_run_is_refused(self):
        orch = build()
        run, item = started(
            orch, simple_task(retry=RetryClass.RETRY_REQUIRING_HUMAN_ACKNOWLEDGEMENT))
        orch.retry(run, item)
        foreign = HumanInterventionRecord(InterventionRef("iv.2"),
                                          WorkflowRunRef("run.elsewhere"),
                                          HumanAuthorityRef("h"), "acknowledge", "not this run")
        with self.assertRaises(LineageError):
            orch.retry(run, item, acknowledgement=foreign)

    def test_revalidation_class_must_revalidate_first(self):
        orch = build()
        run, item = started(orch, simple_task(retry=RetryClass.RETRY_REQUIRING_REVALIDATION))
        with self.assertRaises(GovernanceError):
            orch.retry(run, item)
        orch.retry(run, item, revalidated=True)
        self.assertIn("retry:dispatched", orch.log.kinds())


class TestScopeBinding(unittest.TestCase):
    """Audit finding 8: the approved mechanism is evidence, not an identifier."""

    def test_narrowing_sub_run_is_allowed_and_widening_is_not(self):
        orch = build()
        definition = WorkflowDefinition(WorkflowRef("wf.t"), "v1", (simple_task(),), SCOPE)
        parent = orch.create_run(definition, WorkflowRunRef("run.p"))
        child = orch.open_sub_run(parent, definition, WorkflowRunRef("run.c"),
                                  ScopeBinding(SCOPE.scope, frozenset(), "EU"))
        self.assertEqual(child.scope.sensitivity, frozenset())
        wider = ScopeBinding(SCOPE.scope, frozenset({"INTERNAL", "RESTRICTED"}), "EU")
        with self.assertRaises(GovernanceError):
            orch.open_sub_run(parent, definition, WorkflowRunRef("run.w"), wider)

    def test_residency_change_is_not_a_narrowing(self):
        self.assertFalse(SCOPE.narrows_to(ScopeBinding(SCOPE.scope, frozenset({"INTERNAL"}),
                                                       "US")))

    def test_a_bare_mechanism_reference_does_not_authorise_a_crossing(self):
        orch = build()
        run, _ = started(orch, simple_task())
        target = ScopeBinding(ScopeRef("project.zephyr"), frozenset({"INTERNAL"}), "EU")
        for bare in (None, ScopeTransferRef("st.bare"), HandoffRef("ho.bare")):
            fresh = build()
            run, _ = started(fresh, simple_task(), "run.%s" % id(bare))
            with self.assertRaises(GovernanceError):
                fresh.transfer_scope(run, run.definition, WorkflowRunRef("run.x"), target,
                                     authorisation=bare)

    def test_an_authorisation_for_another_run_or_scope_is_refused(self):
        orch = build()
        run, _ = started(orch, simple_task())
        target = ScopeBinding(ScopeRef("project.zephyr"), frozenset({"INTERNAL"}), "EU")
        wrong_run = ScopeTransferAuthorisation(
            ScopeTransferRef("st.1"), "v2", WorkflowRunRef("run.elsewhere"), SCOPE.scope,
            target.scope, HumanAuthorityRef("h"), DecisionRecordRef("dr.1"))
        with self.assertRaises(GovernanceError):
            orch.transfer_scope(run, run.definition, WorkflowRunRef("run.x"), target,
                                wrong_run)

    def test_an_approved_authorisation_creates_a_new_run_and_leaves_the_first_bound(self):
        orch = build()
        run, _ = started(orch, simple_task())
        target = ScopeBinding(ScopeRef("project.zephyr"), frozenset({"INTERNAL"}), "EU")
        authorisation = ScopeTransferAuthorisation(
            ScopeTransferRef("st.1"), "v2", run.ref, SCOPE.scope, target.scope,
            HumanAuthorityRef("h"), DecisionRecordRef("dr.1"))
        transferred = orch.transfer_scope(run, run.definition, WorkflowRunRef("run.x"),
                                          target, authorisation)
        self.assertEqual(transferred.scope.scope, target.scope)
        self.assertEqual(run.scope.scope, SCOPE.scope)          # one scope per execution
        self.assertIsNot(transferred, run)

    def test_an_authorisation_needs_a_real_mechanism_kind_and_version(self):
        with self.assertRaises(IdentityError):
            ScopeTransferAuthorisation(ArtifactRef("art"), "v1", WorkflowRunRef("r"),
                                       ScopeRef("a"), ScopeRef("b"), HumanAuthorityRef("h"),
                                       DecisionRecordRef("dr"))
        with self.assertRaises(GovernanceError):
            ScopeTransferAuthorisation(ScopeTransferRef("st"), "", WorkflowRunRef("r"),
                                       ScopeRef("a"), ScopeRef("b"), HumanAuthorityRef("h"),
                                       DecisionRecordRef("dr"))


class TestAppendOnlyHistory(unittest.TestCase):
    """Audit finding 9: governed history is append-only and nothing is overwritten by id."""

    def test_event_log_cannot_be_rewritten_or_reattributed(self):
        log = ExecutionEventLog()
        log.append(WorkflowRunRef("r"), "a")
        log.append(WorkflowRunRef("r"), "b")
        with self.assertRaises(AppendOnlyError):
            log[0] = "rewritten"
        with self.assertRaises(AppendOnlyError):
            del log[0]
        with self.assertRaises(AppendOnlyError):
            log._events = []
        self.assertEqual(len(log), 2)

    def test_event_log_has_no_public_backing_list(self):
        log = ExecutionEventLog()
        log.append(WorkflowRunRef("r"), "a")
        self.assertNotIn("_events", vars(log))
        self.assertIsInstance(log.events(), tuple)

    def test_record_store_is_append_only(self):
        store = RecordStore("test")
        store.add("x")
        with self.assertRaises(AppendOnlyError):
            store[0] = "y"
        with self.assertRaises(AppendOnlyError):
            store._records = []

    def test_repeated_decision_records_both_stand(self):
        gate = decision_gate(right="dr.rep")
        orch = build(rights={"dr.rep": (HumanAuthorityRef("h"), GateOutcome.SATISFIED)})
        run, item = started(orch, simple_task(gates=(gate,)))
        orch.run_decision_gate(run, item, gate.ref)
        orch.run_decision_gate(run, item, gate.ref)
        records = run.decision_records()
        self.assertEqual(len(records), 2)
        self.assertNotEqual(records[0].ref, records[1].ref)

    def test_repeated_reviews_both_stand(self):
        gate = review_gate(profile="rp.rep")
        orch = build(reviews={"rp.rep": (GateOutcome.SATISFIED, HumanAuthorityRef("h"),
                                         "INDEPENDENT")})
        run, item = started(orch, simple_task(gates=(gate,)))
        orch.run_review_gate(run, item, gate.ref)
        orch.run_review_gate(run, item, gate.ref)
        self.assertEqual(len(run.review_instances()), 2)

    def test_sequence_numbers_are_monotonic(self):
        log = ExecutionEventLog()
        first = log.append(WorkflowRunRef("r"), "a")
        second = log.append(WorkflowRunRef("r"), "b")
        self.assertEqual((first.sequence, second.sequence), (1, 2))


class TestLateResultAsymmetry(unittest.TestCase):
    """Case 5 and case 6 of the ten races are deliberately different, and stay different."""

    def test_the_five_race_outcomes_are_distinct(self):
        self.assertEqual(len(RaceOutcome), 5)
        self.assertIsNot(RaceOutcome.RECONCILE, RaceOutcome.IGNORE_AS_STALE)

    def test_a_late_decision_record_still_stands_in_governed_history(self):
        gate = decision_gate(right="dr.late")
        orch = build(rights={"dr.late": (HumanAuthorityRef("h"), GateOutcome.SATISFIED)})
        run, item = started(orch, simple_task(gates=(gate,)))
        orch.run_decision_gate(run, item, gate.ref)
        first = run.decision_records()[0]
        orch.run_decision_gate(run, item, gate.ref)
        self.assertIn(first, run.decision_records())


class TestStateMachine(unittest.TestCase):

    def test_ten_phases_six_terminals_five_waits_four_postures(self):
        self.assertEqual(len(RunPhase), 10)
        self.assertEqual(len(TerminalOutcome), 6)
        self.assertEqual(len(WaitReason), 5)
        self.assertEqual(len(GovernancePosture), 4)

    def test_disallowed_transition_raises(self):
        orch = build()
        run, _ = started(orch, simple_task())
        with self.assertRaises(TransitionError):
            orch._transition(run, RunPhase.CREATED)

    def test_every_phase_has_a_transition_entry(self):
        self.assertEqual(set(ALLOWED_TRANSITIONS), set(RunPhase))

    def test_blocked_leaves_only_through_a_governed_act(self):
        self.assertNotIn(RunPhase.READY, ALLOWED_TRANSITIONS[RunPhase.BLOCKED])

    def test_a_waiting_run_must_name_its_subject(self):
        orch = build()
        run, _ = started(orch, simple_task())
        with self.assertRaises(GovernanceError):
            orch._transition(run, RunPhase.WAITING,
                             wait_reason=WaitReason.WAITING_FOR_REVIEW, wait_subject=None)

    def test_terminal_run_cannot_move_again(self):
        orch = build()
        run, _ = started(orch, simple_task())
        orch.complete(run, TerminalOutcome.FAILED, cause="the step errored")
        with self.assertRaises(TransitionError):
            orch._transition(run, RunPhase.RUNNING)


class TestGateOutcomes(unittest.TestCase):

    def test_seven_outcomes_and_only_two_continue(self):
        self.assertEqual(len(GateOutcome), 7)
        self.assertEqual(CONTINUING_GATE_OUTCOMES,
                         frozenset({GateOutcome.SATISFIED,
                                    GateOutcome.SATISFIED_WITH_OPEN_ITEMS}))

    def test_missing_decision_right_blocks_and_escalates(self):
        gate = decision_gate(right="dr.none")
        orch = build(rights={})
        run, item = started(orch, simple_task(gates=(gate,)))
        outcome, record = orch.run_decision_gate(run, item, gate.ref)
        self.assertIs(outcome, GateOutcome.NO_APPLICABLE_DECISION_RIGHT)
        self.assertIsNone(record)
        self.assertIs(run.phase, RunPhase.ESCALATED)
        self.assertIs(run.posture, GovernancePosture.AUTHORITY_ABSENT)

    def test_deferral_is_not_approval(self):
        gate = decision_gate(right="dr.d")
        orch = build(rights={"dr.d": (HumanAuthorityRef("h"), GateOutcome.DEFER)})
        run, item = started(orch, simple_task(gates=(gate,)))
        outcome, _ = orch.run_decision_gate(run, item, gate.ref)
        self.assertIs(outcome, GateOutcome.DEFER)
        self.assertIs(run.phase, RunPhase.WAITING)
        self.assertIs(run.posture, GovernancePosture.GATE_UNSATISFIED)

    def test_timeout_does_not_approve(self):
        gate = decision_gate(right="dr.e")
        orch = build(rights={"dr.e": (HumanAuthorityRef("h"), GateOutcome.EXPIRED)})
        run, item = started(orch, simple_task(gates=(gate,)))
        outcome, record = orch.run_decision_gate(run, item, gate.ref)
        self.assertIs(outcome, GateOutcome.EXPIRED)
        self.assertIs(run.phase, RunPhase.ESCALATED)
        with self.assertRaises(EvidenceError):
            orch.satisfy_gate_with(run, item, gate.ref, record)


class TestAssignmentAuthority(unittest.TestCase):

    def test_assignment_grants_no_review_or_decision_authority(self):
        orch = build()
        run, item = started(orch, simple_task())
        assignment = orch.assign(run, item, AUTHOR, AgentInstanceRef("agent.1"))
        self.assertFalse(assignment.grants_review_authority())
        self.assertFalse(assignment.grants_decision_authority())

    def test_assignment_must_match_the_role_the_task_requires(self):
        orch = build()
        run, item = started(orch, simple_task())
        with self.assertRaises(GovernanceError):
            orch.assign(run, item, RoleRef("role.someone-else"))


class TestCompletion(unittest.TestCase):

    def test_only_the_two_clear_postures_permit_a_completion(self):
        self.assertEqual(POSTURE_PERMITS_COMPLETION[GovernancePosture.GATE_UNSATISFIED],
                         frozenset())
        self.assertEqual(POSTURE_PERMITS_COMPLETION[GovernancePosture.AUTHORITY_ABSENT],
                         frozenset())

    def test_completion_denied_while_a_gate_is_unsatisfied(self):
        gate = review_gate()
        orch = build(reviews={"rp": (GateOutcome.SATISFIED, HumanAuthorityRef("h"),
                                     "INDEPENDENT")})
        run, item = started(orch, simple_task(gates=(gate,)))
        with self.assertRaises(GovernanceError):
            orch.complete(run, TerminalOutcome.COMPLETED)
        orch.run_review_gate(run, item, gate.ref)
        orch.complete(run, TerminalOutcome.COMPLETED)
        self.assertIs(run.terminal, TerminalOutcome.COMPLETED)

    def test_open_items_complete_only_as_completed_with_open_items(self):
        gate = review_gate()
        orch = build(reviews={"rp": (GateOutcome.SATISFIED_WITH_OPEN_ITEMS,
                                     HumanAuthorityRef("h"), "INDEPENDENT")})
        run, item = started(orch, simple_task(gates=(gate,)))
        orch.run_review_gate(run, item, gate.ref)
        self.assertIs(run.posture, GovernancePosture.OPEN_ITEMS_CARRIED)
        with self.assertRaises(GovernanceError):
            orch.complete(run, TerminalOutcome.COMPLETED)
        orch.complete(run, TerminalOutcome.COMPLETED_WITH_OPEN_ITEMS)

    def test_cancellation_requires_an_intervention_and_terminated_a_constraint(self):
        orch = build()
        run, _ = started(orch, simple_task())
        with self.assertRaises(GovernanceError):
            orch.complete(run, TerminalOutcome.CANCELLED)
        with self.assertRaises(GovernanceError):
            orch.complete(run, TerminalOutcome.TERMINATED)
        iv = HumanInterventionRecord(InterventionRef("iv"), run.ref, HumanAuthorityRef("h"),
                                     "cancel", "the work is not wanted")
        orch.complete(run, TerminalOutcome.CANCELLED, intervention=iv)

    def test_operational_success_is_not_governance_completion(self):
        gate = review_gate()
        orch = build(eligible={"cap": (ModelRef("m"), ModelProfileRef("p"))},
                     reviews={"rp": (GateOutcome.SATISFIED, HumanAuthorityRef("h"),
                                     "INDEPENDENT")})
        run, item = started(orch, simple_task(gates=(gate,), capability="cap"))
        decision = orch.route(run, item, "policy@1")
        orch.invoke_model(run, item, decision)
        with self.assertRaises(GovernanceError):
            orch.complete(run, TerminalOutcome.COMPLETED)


class TestExamplesRun(unittest.TestCase):
    """The two synthetic cases are executed, not merely shipped."""

    def test_governed_example_completes(self):
        import governed_run
        self.assertEqual(governed_run.main(), 0)

    def test_blocked_example_blocks(self):
        import blocked_run
        self.assertEqual(blocked_run.main(), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
