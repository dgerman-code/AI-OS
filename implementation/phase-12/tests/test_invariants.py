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
    InMemoryDecisionDesk, InMemoryMechanismRegistry, InMemoryReviewerDesk, InMemoryRouter,
    StubModel,
)
from domain import (  # noqa: E402
    ALLOWED_TRANSITIONS, AUTOMATICALLY_RETRYABLE, AgentInstanceRef, AppendOnlyError,
    ArtifactRef, CONTINUING_GATE_OUTCOMES, Canonicality, CanonicalRecordRef, CredentialRef,
    DecisionRecord, DecisionRecordRef, DecisionRightRef, EVIDENCE_CONTRACT, EvidenceError,
    ExecutionEventLog, GateInstance, GateKind, GateOutcome, GateRequirement,
    GateRequirementRef, GovernanceError, GovernancePosture, HandoffRef, HumanAuthorityRef,
    HumanInterventionRecord, HumanWorkCompletion, HumanWorkRef, IdentityError, InterventionRef,
    LineageError, MissingEvidenceError, ModelProfileRef, ModelRef, ModelResult, NEVER_AUTOMATICALLY_RETRYABLE,
    Origin, OrchestratorRef, POSTURE_PERMITS_COMPLETION, PrerequisiteEvidence, PrerequisiteRef,
    RaceOutcome, RecordStore, RetryClass, ReviewInstance, ReviewInstanceRef, ReviewProfileRef,
    RoleRef, RouterOutcome, RouterRef, RoutingDecision, RoutingDecisionRef, RoutingRequest,
    RoutingRequestRef, RunPhase, RuntimeEventRef, SEPARATION_CHAIN, ScopeBinding, ScopeRef,
    ScopeTransferAuthorisation, ScopeTransferRef, StateAccessError, StorageRecordRef, Task,
    TaskRef, TerminalOutcome, TransitionError, WaitReason, WorkItem, WorkItemRef,
    WorkflowDefinition, WorkflowRef, WorkflowRunRef, GateInstanceRef, HumanWorkRecordRef,
    PrerequisiteRecordRef, enforce_field_types, require,
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


def build(rights=None, reviews=None, eligible=None, missing_right_for=(), mechanisms=None):
    router = InMemoryRouter(RouterRef("router.phase9"), eligible=eligible or {},
                            missing_right_for=missing_right_for)
    return Orchestrator(router, InMemoryReviewerDesk(reviews or {}),
                        InMemoryDecisionDesk(rights or {}), StubModel(),
                        mechanisms=mechanisms)


def human_gate(ref="gate.hw", work="hw"):
    return GateRequirement(GateRequirementRef(ref), GateKind.HUMAN_WORK,
                           human_work=HumanWorkRef(work))


def prerequisite_gate(ref="gate.pre", prerequisite="pre"):
    return GateRequirement(GateRequirementRef(ref), GateKind.GOVERNED_PREREQUISITE,
                           prerequisite=PrerequisiteRef(prerequisite))


def snapshot(run, orch):
    """Everything observable about a run: axes, gate outcomes, histories, event count."""
    return (run.axes(),
            tuple((g.ref.id, g.outcome, g.satisfied_by) for g in run.gates()),
            tuple(r.ref for r in run.decision_records()),
            tuple(r.ref for r in run.review_instances()),
            tuple(r.ref for r in run.human_work_records()),
            tuple(r.ref for r in run.prerequisite_records()),
            tuple(r.ref for r in run.routing_decisions()),
            len(run.model_results()), len(orch.log))


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
        GateInstance(GateInstanceRef("gi"), requirement, WorkflowRunRef("r"),
                     WorkItemRef("wi"), GateKind.DECISION)
        with self.assertRaises(IdentityError):
            GateInstance(GateInstanceRef("gi"), requirement, WorkflowRunRef("r"), TaskRef("t"),
                         GateKind.DECISION)
        with self.assertRaises(IdentityError):
            GateInstance(GateInstanceRef("gi"), requirement, WorkflowRunRef("r"),
                         WorkItemRef("wi"), GateKind.DECISION, GateOutcome.SATISFIED,
                         "not a reference")

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
            (HumanWorkCompletion, dict(ref=HumanWorkRecordRef("hwr"),
                                       requirement=GateRequirementRef("g"),
                                       run=WorkflowRunRef("r"), work_item=WorkItemRef("wi"),
                                       human_work=HumanWorkRef("hw"),
                                       outcome=GateOutcome.SATISFIED,
                                       completed_by=HumanAuthorityRef("h")),
             "human_work", TaskRef("t")),
            (PrerequisiteEvidence, dict(ref=PrerequisiteRecordRef("prr"),
                                        requirement=GateRequirementRef("g"),
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
        evidence = PrerequisiteEvidence(PrerequisiteRecordRef("prr.1"), prereq.ref, run.ref,
                                        item.ref, PrerequisiteRef("pre.residency"),
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
            orch._record_routing_decision(run, request, other)

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

    def _authorised_setup(self, target):
        """A run that really did take a governed decision to cross, with a registry to match."""
        gate = decision_gate("gate.tr", "dr.tr")
        registry = InMemoryMechanismRegistry()
        registry.register(ScopeTransferRef("st.1"), "v2", SCOPE, target)
        orch = build(rights={"dr.tr": (HumanAuthorityRef("h"), GateOutcome.SATISFIED)},
                     mechanisms=registry)
        run, item = started(orch, simple_task(gates=(gate,)))
        _outcome, record = orch.run_decision_gate(run, item, gate.ref)
        return orch, run, item, gate, record

    def _authorisation(self, run, item, gate, record, target, **overrides):
        fields = dict(mechanism=ScopeTransferRef("st.1"), mechanism_version="v2",
                      source_run=run.ref, source_scope=run.scope, target_scope=target,
                      work_item=item.ref, requirement=gate.ref,
                      decision_right=DecisionRightRef("dr.tr"),
                      authorised_by=record.decided_by, decision_record=record.ref)
        fields.update(overrides)
        return ScopeTransferAuthorisation(**fields)

    def test_a_bare_mechanism_reference_does_not_authorise_a_crossing(self):
        target = ScopeBinding(ScopeRef("project.zephyr"), frozenset({"INTERNAL"}), "EU")
        for bare in (None, ScopeTransferRef("st.bare"), HandoffRef("ho.bare")):
            orch = build()
            run, _ = started(orch, simple_task(), "run.%s" % id(bare))
            with self.assertRaises(GovernanceError):
                orch.transfer_scope(run, run.definition, WorkflowRunRef("run.x"), target,
                                    authorisation=bare)

    def test_a_fabricated_authorisation_with_no_retained_record_is_refused(self):
        target = ScopeBinding(ScopeRef("project.zephyr"), frozenset({"INTERNAL"}), "EU")
        orch, run, item, gate, record = self._authorised_setup(target)
        fabricated = self._authorisation(run, item, gate, record, target,
                                         decision_record=DecisionRecordRef("dr.never"))
        with self.assertRaises(GovernanceError):
            orch.transfer_scope(run, run.definition, WorkflowRunRef("run.x"), target,
                                fabricated)

    def test_an_authorisation_naming_another_run_is_refused(self):
        target = ScopeBinding(ScopeRef("project.zephyr"), frozenset({"INTERNAL"}), "EU")
        orch, run, item, gate, record = self._authorised_setup(target)
        wrong = self._authorisation(run, item, gate, record, target,
                                    source_run=WorkflowRunRef("run.elsewhere"))
        with self.assertRaises(GovernanceError):
            orch.transfer_scope(run, run.definition, WorkflowRunRef("run.x"), target, wrong)

    def test_an_authorisation_naming_another_target_binding_is_refused(self):
        target = ScopeBinding(ScopeRef("project.zephyr"), frozenset({"INTERNAL"}), "EU")
        narrower = ScopeBinding(ScopeRef("project.zephyr"), frozenset(), "EU")
        orch, run, item, gate, record = self._authorised_setup(target)
        orch.mechanisms.register(ScopeTransferRef("st.1"), "v2", SCOPE, target)
        # The authorisation covers a different (narrower) target than the one being crossed to.
        wrong = self._authorisation(run, item, gate, record, narrower)
        with self.assertRaises(GovernanceError):
            orch.transfer_scope(run, run.definition, WorkflowRunRef("run.x"), target, wrong)

    def test_the_authorising_human_must_be_the_one_who_exercised_the_right(self):
        target = ScopeBinding(ScopeRef("project.zephyr"), frozenset({"INTERNAL"}), "EU")
        orch, run, item, gate, record = self._authorised_setup(target)
        wrong = self._authorisation(run, item, gate, record, target,
                                    authorised_by=HumanAuthorityRef("human.someone-else"))
        with self.assertRaises(GovernanceError):
            orch.transfer_scope(run, run.definition, WorkflowRunRef("run.x"), target, wrong)

    def test_the_mechanism_must_be_one_the_run_recognises(self):
        target = ScopeBinding(ScopeRef("project.zephyr"), frozenset({"INTERNAL"}), "EU")
        orch, run, item, gate, record = self._authorised_setup(target)
        unknown = self._authorisation(run, item, gate, record, target,
                                      mechanism_version="v99")
        with self.assertRaises(GovernanceError):
            orch.transfer_scope(run, run.definition, WorkflowRunRef("run.x"), target, unknown)

    def test_an_orchestrator_with_no_registry_approves_no_crossing(self):
        target = ScopeBinding(ScopeRef("project.zephyr"), frozenset({"INTERNAL"}), "EU")
        orch, run, item, gate, record = self._authorised_setup(target)
        orch.mechanisms = None
        authorisation = self._authorisation(run, item, gate, record, target)
        with self.assertRaises(GovernanceError):
            orch.transfer_scope(run, run.definition, WorkflowRunRef("run.x"), target,
                                authorisation)

    def test_a_crossing_may_not_widen_sensitivity_or_change_residency(self):
        wider = ScopeBinding(ScopeRef("project.zephyr"), frozenset({"INTERNAL", "SECRET"}),
                             "EU")
        orch, run, item, gate, record = self._authorised_setup(wider)
        orch.mechanisms.register(ScopeTransferRef("st.1"), "v2", SCOPE, wider)
        with self.assertRaises(GovernanceError):
            orch.transfer_scope(run, run.definition, WorkflowRunRef("run.x"), wider,
                                self._authorisation(run, item, gate, record, wider))
        elsewhere = ScopeBinding(ScopeRef("project.zephyr"), frozenset({"INTERNAL"}), "US")
        orch2, run2, item2, gate2, record2 = self._authorised_setup(elsewhere)
        orch2.mechanisms.register(ScopeTransferRef("st.1"), "v2", SCOPE, elsewhere)
        with self.assertRaises(GovernanceError):
            orch2.transfer_scope(run2, run2.definition, WorkflowRunRef("run.y"), elsewhere,
                                 self._authorisation(run2, item2, gate2, record2, elsewhere))

    def test_an_approved_authorisation_creates_a_new_run_and_leaves_the_first_bound(self):
        target = ScopeBinding(ScopeRef("project.zephyr"), frozenset({"INTERNAL"}), "EU")
        orch, run, item, gate, record = self._authorised_setup(target)
        authorisation = self._authorisation(run, item, gate, record, target)
        transferred = orch.transfer_scope(run, run.definition, WorkflowRunRef("run.x"),
                                          target, authorisation)
        self.assertEqual(transferred.scope, target)
        self.assertEqual(run.scope, SCOPE)                      # one scope per execution
        self.assertIsNot(transferred, run)

    def test_a_refused_crossing_records_nothing(self):
        target = ScopeBinding(ScopeRef("project.zephyr"), frozenset({"INTERNAL"}), "EU")
        orch, run, item, gate, record = self._authorised_setup(target)
        before = snapshot(run, orch)
        with self.assertRaises(GovernanceError):
            orch.transfer_scope(run, run.definition, WorkflowRunRef("run.x"), target,
                                self._authorisation(run, item, gate, record, target,
                                                    decision_record=DecisionRecordRef("dr.no")))
        self.assertEqual(before, snapshot(run, orch))

    def test_an_authorisation_needs_a_real_mechanism_kind_and_version(self):
        common = dict(source_run=WorkflowRunRef("r"), source_scope=SCOPE, target_scope=SCOPE,
                      work_item=WorkItemRef("wi"), requirement=GateRequirementRef("g"),
                      decision_right=DecisionRightRef("d"),
                      authorised_by=HumanAuthorityRef("h"),
                      decision_record=DecisionRecordRef("dr"))
        with self.assertRaises(IdentityError):
            ScopeTransferAuthorisation(mechanism=ArtifactRef("art"), mechanism_version="v1",
                                       **common)
        with self.assertRaises(GovernanceError):
            ScopeTransferAuthorisation(mechanism=ScopeTransferRef("st"), mechanism_version="",
                                       **common)


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


class TestConstructionTimeCompleteness(unittest.TestCase):
    """Re-audit finding 1: every declared field, not only the governed references."""

    def test_a_string_cannot_stand_where_an_enum_is_declared(self):
        with self.assertRaises(IdentityError):
            HumanWorkCompletion(HumanWorkRecordRef("hwr"), GateRequirementRef("g"),
                                WorkflowRunRef("r"), WorkItemRef("wi"), HumanWorkRef("hw"),
                                "SATISFIED", HumanAuthorityRef("h"))
        with self.assertRaises(IdentityError):
            PrerequisiteEvidence(PrerequisiteRecordRef("prr"), GateRequirementRef("g"),
                                 WorkflowRunRef("r"), WorkItemRef("wi"), PrerequisiteRef("pr"),
                                 "SATISFIED", StorageRecordRef("sr"))
        with self.assertRaises(IdentityError):
            Task(TASK, "T", AUTHOR, "SAFE_AUTOMATIC_RETRY")

    def test_a_string_cannot_stand_where_a_structured_value_is_declared(self):
        with self.assertRaises(IdentityError):
            RoutingRequest(RoutingRequestRef("rr"), WorkflowRunRef("r"), WorkItemRef("wi"),
                           "cap", "project.apollo", "p@1")
        with self.assertRaises(IdentityError):
            WorkflowDefinition(WorkflowRef("wf"), "v1", (simple_task(),), "project.apollo")

    def test_a_string_cannot_stand_where_a_string_is_not_declared(self):
        with self.assertRaises(IdentityError):
            ScopeBinding(ScopeRef("s"), frozenset({"A"}), 7)
        with self.assertRaises(IdentityError):
            Task(TASK, 7, AUTHOR, RetryClass.SAFE_AUTOMATIC_RETRY)

    def test_container_elements_are_checked(self):
        with self.assertRaises(IdentityError):
            WorkflowDefinition(WorkflowRef("wf"), "v1", ("not a task",), SCOPE)
        with self.assertRaises(IdentityError):
            Task(TASK, "T", AUTHOR, RetryClass.SAFE_AUTOMATIC_RETRY, gates=("not a gate",))
        with self.assertRaises(IdentityError):
            ScopeBinding(ScopeRef("s"), frozenset({7}), "EU")
        with self.assertRaises(IdentityError):
            ScopeBinding(ScopeRef("s"), {"A"}, "EU")

    def test_no_coercion_happens_anywhere(self):
        """A rejected value is rejected, never quietly converted."""
        binding = ScopeBinding(ScopeRef("s"), frozenset({"A"}), "EU")
        self.assertIsInstance(binding.sensitivity, frozenset)
        with self.assertRaises(IdentityError):
            ScopeBinding(ScopeRef("s"), ["A"], "EU")

    def test_the_enforcement_covers_every_governed_dataclass(self):
        """A sweep: a new governed object that forgets to enforce is noticed here."""
        import dataclasses
        import domain as domain_module
        governed = [obj for name, obj in vars(domain_module).items()
                    if dataclasses.is_dataclass(obj) and isinstance(obj, type)
                    and obj is not domain_module.Ref
                    and not issubclass(obj, domain_module.Ref)]
        self.assertGreaterEqual(len(governed), 15)
        for cls in governed:
            source = cls.__post_init__.__code__.co_names if hasattr(cls, "__post_init__") else ()
            self.assertIn("enforce_field_types", source,
                          "%s does not enforce its field types" % cls.__name__)


class TestGateInstanceIdentity(unittest.TestCase):
    """Re-audit finding 2: a requirement reference is not an instantiated gate identity."""

    def test_activating_one_gated_task_twice_keeps_both_gates(self):
        gate = decision_gate("gate.shared", "dr.shared")
        orch = build(rights={"dr.shared": (HumanAuthorityRef("h"), GateOutcome.SATISFIED)})
        run, first = started(orch, simple_task(gates=(gate,)))
        second = orch.activate_stage(run, TASK)
        self.assertNotEqual(first.ref, second.ref)
        self.assertEqual(len(run.work_items()), 2)
        self.assertEqual(len(run.gates()), 2)
        self.assertEqual(len({g.ref for g in run.gates()}), 2)

    def test_satisfying_the_second_leaves_the_first_open(self):
        gate = decision_gate("gate.shared", "dr.shared")
        orch = build(rights={"dr.shared": (HumanAuthorityRef("h"), GateOutcome.SATISFIED)})
        run, first = started(orch, simple_task(gates=(gate,)))
        second = orch.activate_stage(run, TASK)
        orch.run_decision_gate(run, second, gate.ref)
        open_gates = orch.unsatisfied_gates(run)
        self.assertEqual(len(open_gates), 1)
        self.assertEqual(open_gates[0].work_item, first.ref)
        with self.assertRaises(GovernanceError):
            orch.complete(run, TerminalOutcome.COMPLETED)

    def test_two_tasks_reusing_one_requirement_id_do_not_alias(self):
        shared = GateRequirementRef("gate.reused")
        first = Task(TaskRef("task.a"), "A", AUTHOR, RetryClass.SAFE_AUTOMATIC_RETRY,
                     gates=(GateRequirement(shared, GateKind.DECISION,
                                            decision_right=DecisionRightRef("dr.a")),))
        second = Task(TaskRef("task.b"), "B", AUTHOR, RetryClass.SAFE_AUTOMATIC_RETRY,
                      gates=(GateRequirement(shared, GateKind.DECISION,
                                             decision_right=DecisionRightRef("dr.b")),))
        orch = build(rights={"dr.a": (HumanAuthorityRef("h"), GateOutcome.SATISFIED)})
        definition = WorkflowDefinition(WorkflowRef("wf.two"), "v1", (first, second), SCOPE)
        run = orch.create_run(definition, WorkflowRunRef("run.two"))
        item_a = orch.activate_stage(run, first.ref)
        item_b = orch.activate_stage(run, second.ref)
        self.assertEqual(len(run.gates()), 2)
        orch.run_decision_gate(run, item_a, shared)
        still_open = orch.unsatisfied_gates(run)
        self.assertEqual(len(still_open), 1)
        self.assertEqual(still_open[0].work_item, item_b.ref)

    def test_a_gate_instance_carries_its_own_identity(self):
        gate = decision_gate()
        orch = build()
        run, item = started(orch, simple_task(gates=(gate,)))
        instance = run.gate_instance(item.ref, gate.ref)
        self.assertIsInstance(instance.ref, GateInstanceRef)
        self.assertEqual(instance.run, run.ref)
        self.assertEqual(instance.work_item, item.ref)
        self.assertIs(instance.kind, GateKind.DECISION)


class TestHaltedRunCannotProgress(unittest.TestCase):
    """Re-audit finding 3: a blocked or escalated run does not resume by being asked."""

    def _halted(self):
        gate = decision_gate("gate.absent", "dr.absent")
        orch = build(rights={})
        run, item = started(orch, simple_task(gates=(gate,)))
        orch.run_decision_gate(run, item, gate.ref)
        return orch, run, item, gate

    def test_the_exact_audit_chain_is_refused(self):
        orch, run, item, gate = self._halted()
        self.assertIs(run.phase, RunPhase.ESCALATED)
        self.assertIs(run.posture, GovernancePosture.AUTHORITY_ABSENT)
        with self.assertRaises(GovernanceError):
            orch.activate_stage(run, TASK)
        self.assertEqual(len(run.gates()), 1)
        self.assertIs(run.gates()[0].outcome, GateOutcome.NO_APPLICABLE_DECISION_RIGHT)

    def test_a_blocked_run_cannot_activate_a_stage(self):
        orch = build(eligible={})
        run, item = started(orch, simple_task(capability="cap"))
        orch.route(run, item, "policy@1")
        self.assertIs(run.phase, RunPhase.BLOCKED)
        self.assertIs(run.posture, GovernancePosture.GATE_UNSATISFIED)
        with self.assertRaises(TransitionError):
            orch.activate_stage(run, TASK)

    def test_authority_absent_always_arrives_with_an_escalated_phase(self):
        """Two guards, one reachable state.

        `activate_stage` refuses on the phase AND on the posture. Today the posture guard is
        unreachable on its own, because `AUTHORITY_ABSENT` is only ever set together with
        `ESCALATED`; the test records that coincidence rather than pretending the second guard
        is independently exercised. It is kept as defence for any future path that sets the
        posture without halting the phase."""
        gate = decision_gate("gate.absent", "dr.absent")
        orch = build(rights={})
        run, item = started(orch, simple_task(gates=(gate,)))
        orch.run_decision_gate(run, item, gate.ref)
        self.assertIs(run.posture, GovernancePosture.AUTHORITY_ABSENT)
        self.assertIs(run.phase, RunPhase.ESCALATED)
        with self.assertRaises(GovernanceError):
            orch.activate_stage(run, TASK)

    def test_unblocking_needs_a_recorded_human_act_and_a_resolved_constraint(self):
        orch, run, item, gate = self._halted()
        intervention = HumanInterventionRecord(InterventionRef("iv"), run.ref,
                                               HumanAuthorityRef("h"), "unblock",
                                               "the Right was created in Phase 7")
        with self.assertRaises(GovernanceError):
            orch.unblock(run, intervention)          # the gate still stands unresolved
        self.assertIs(run.phase, RunPhase.ESCALATED)

    def test_unblocking_a_run_whose_constraint_is_resolved_resumes_it(self):
        orch = build(eligible={})
        run, item = started(orch, simple_task(capability="cap"))
        orch.route(run, item, "policy@1")
        intervention = HumanInterventionRecord(InterventionRef("iv"), run.ref,
                                               HumanAuthorityRef("h"), "unblock",
                                               "an eligible deployment was registered")
        orch.unblock(run, intervention)
        self.assertIs(run.phase, RunPhase.RUNNING)
        self.assertIs(run.posture, GovernancePosture.GOVERNANCE_CLEAR)


class TestEvidenceBeforeMutation(unittest.TestCase):
    """Re-audit finding 4: validate, then commit. A refusal leaves nothing behind."""

    def test_a_continuing_outcome_with_no_record_is_refused_before_any_mutation(self):
        gate = decision_gate("gate.norec", "dr.norec")
        orch = build(rights={})
        run, item = started(orch, simple_task(gates=(gate,)))
        orch.decisions.decide = lambda request: (GateOutcome.SATISFIED, None)
        before = snapshot(run, orch)
        # Its own error class: "no record at all" is a different failure from "wrong record".
        with self.assertRaises(MissingEvidenceError):
            orch.run_decision_gate(run, item, gate.ref)
        self.assertEqual(before, snapshot(run, orch))

    def test_rejected_evidence_leaves_state_and_history_unchanged(self):
        gate = decision_gate("gate.part", "dr.part")
        orch = build(rights={"dr.part": (HumanAuthorityRef("h"), GateOutcome.SATISFIED)})
        run, item = started(orch, simple_task(gates=(gate,)))
        forged = DecisionRecord(DecisionRecordRef("dr.forged"), gate.ref,
                                WorkflowRunRef("run.elsewhere"), item.ref,
                                DecisionRightRef("dr.part"), GateOutcome.SATISFIED,
                                HumanAuthorityRef("h"))
        before = snapshot(run, orch)
        with self.assertRaises(EvidenceError):
            orch.satisfy_gate_with(run, item, gate.ref, forged)
        self.assertEqual(before, snapshot(run, orch))

    def test_a_rejected_review_leaves_state_and_history_unchanged(self):
        gate = review_gate(profile="rp.ind", independence="INDEPENDENT")
        orch = build(reviews={"rp.ind": (GateOutcome.SATISFIED, HumanAuthorityRef("h"),
                                         "NOT_INDEPENDENT")})
        run, item = started(orch, simple_task(gates=(gate,)))
        before = snapshot(run, orch)
        with self.assertRaises(EvidenceError):
            orch.run_review_gate(run, item, gate.ref)
        self.assertEqual(before, snapshot(run, orch))

    def test_a_rejected_model_result_leaves_nothing_recorded(self):
        orch = build(eligible={"cap": (ModelRef("m"), ModelProfileRef("p"))})
        run, item = started(orch, simple_task(capability="cap"))
        decision = orch.route(run, item, "policy@1")
        orch.model.execute = lambda request: ModelResult(
            WorkflowRunRef("run.elsewhere"), item.ref, decision.ref, ModelRef("m"), "t")
        before = snapshot(run, orch)
        with self.assertRaises(LineageError):
            orch.invoke_model(run, item, decision)
        self.assertEqual(before, snapshot(run, orch))

    def test_an_adapter_answer_that_is_not_a_pair_is_refused(self):
        gate = decision_gate("gate.bad", "dr.bad")
        orch = build(rights={})
        run, item = started(orch, simple_task(gates=(gate,)))
        orch.decisions.decide = lambda request: GateOutcome.SATISFIED
        before = snapshot(run, orch)
        with self.assertRaises(EvidenceError):
            orch.run_decision_gate(run, item, gate.ref)
        self.assertEqual(before, snapshot(run, orch))


class TestOpenItemsSemantics(unittest.TestCase):
    """Re-audit finding 5: SATISFIED_WITH_OPEN_ITEMS means the same thing everywhere."""

    def _carry(self, gate, evidence, record):
        orch = build()
        run, item = started(orch, simple_task(gates=(gate,)))
        record(orch, run, item)
        return orch, run

    def test_human_work_carries_open_items(self):
        gate = human_gate("gate.hw2", "hw.2")
        orch = build()
        run, item = started(orch, simple_task(gates=(gate,)))
        completion = HumanWorkCompletion(HumanWorkRecordRef("hwr"), gate.ref, run.ref,
                                         item.ref, HumanWorkRef("hw.2"),
                                         GateOutcome.SATISFIED_WITH_OPEN_ITEMS,
                                         HumanAuthorityRef("h"))
        orch.record_human_work(run, item, gate.ref, completion)
        self.assertIs(run.posture, GovernancePosture.OPEN_ITEMS_CARRIED)
        with self.assertRaises(GovernanceError):
            orch.complete(run, TerminalOutcome.COMPLETED)
        orch.complete(run, TerminalOutcome.COMPLETED_WITH_OPEN_ITEMS)

    def test_prerequisite_carries_open_items(self):
        gate = prerequisite_gate("gate.pre2", "pre.2")
        orch = build()
        run, item = started(orch, simple_task(gates=(gate,)))
        evidence = PrerequisiteEvidence(PrerequisiteRecordRef("prr"), gate.ref, run.ref,
                                        item.ref, PrerequisiteRef("pre.2"),
                                        GateOutcome.SATISFIED_WITH_OPEN_ITEMS,
                                        StorageRecordRef("sr"))
        orch.record_prerequisite(run, item, gate.ref, evidence)
        self.assertIs(run.posture, GovernancePosture.OPEN_ITEMS_CARRIED)
        with self.assertRaises(GovernanceError):
            orch.complete(run, TerminalOutcome.COMPLETED)

    def test_externally_supplied_evidence_carries_open_items(self):
        gate = prerequisite_gate("gate.pre3", "pre.3")
        orch = build()
        run, item = started(orch, simple_task(gates=(gate,)))
        evidence = PrerequisiteEvidence(PrerequisiteRecordRef("prr3"), gate.ref, run.ref,
                                        item.ref, PrerequisiteRef("pre.3"),
                                        GateOutcome.SATISFIED_WITH_OPEN_ITEMS,
                                        StorageRecordRef("sr"))
        orch.satisfy_gate_with(run, item, gate.ref, evidence)
        self.assertIs(run.posture, GovernancePosture.OPEN_ITEMS_CARRIED)

    def test_decision_carries_open_items(self):
        gate = decision_gate("gate.oi", "dr.oi")
        orch = build(rights={"dr.oi": (HumanAuthorityRef("h"),
                                       GateOutcome.SATISFIED_WITH_OPEN_ITEMS)})
        run, item = started(orch, simple_task(gates=(gate,)))
        orch.run_decision_gate(run, item, gate.ref)
        self.assertIs(run.posture, GovernancePosture.OPEN_ITEMS_CARRIED)


class TestEvidenceRetention(unittest.TestCase):
    """Re-audit finding 8: evidence that satisfies a gate is retained, by its own identity."""

    def test_externally_supplied_evidence_is_retained(self):
        gate = prerequisite_gate("gate.ret", "pre.ret")
        orch = build()
        run, item = started(orch, simple_task(gates=(gate,)))
        evidence = PrerequisiteEvidence(PrerequisiteRecordRef("prr.ret"), gate.ref, run.ref,
                                        item.ref, PrerequisiteRef("pre.ret"),
                                        GateOutcome.SATISFIED, StorageRecordRef("sr"))
        instance = orch.satisfy_gate_with(run, item, gate.ref, evidence)
        self.assertIn(evidence, run.prerequisite_records())
        self.assertIs(run.evidence_for(instance), evidence)

    def test_every_gate_kind_retains_its_evidence(self):
        review = review_gate("gate.r", "rp")
        decision = decision_gate("gate.d", "dr")
        human = human_gate("gate.h", "hw")
        prereq = prerequisite_gate("gate.p", "pre")
        orch = build(reviews={"rp": (GateOutcome.SATISFIED, HumanAuthorityRef("h1"),
                                     "INDEPENDENT")},
                     rights={"dr": (HumanAuthorityRef("h2"), GateOutcome.SATISFIED)})
        run, item = started(orch, simple_task(gates=(review, decision, human, prereq)))
        orch.run_review_gate(run, item, review.ref)
        orch.run_decision_gate(run, item, decision.ref)
        orch.record_human_work(run, item, human.ref, HumanWorkCompletion(
            HumanWorkRecordRef("hwr"), human.ref, run.ref, item.ref, HumanWorkRef("hw"),
            GateOutcome.SATISFIED, HumanAuthorityRef("h3")))
        orch.record_prerequisite(run, item, prereq.ref, PrerequisiteEvidence(
            PrerequisiteRecordRef("prr"), prereq.ref, run.ref, item.ref, PrerequisiteRef("pre"),
            GateOutcome.SATISFIED, StorageRecordRef("sr")))
        for instance in run.gates():
            self.assertIsNotNone(run.evidence_for(instance),
                                 "%s has no retained evidence" % instance.kind.value)
        orch.complete(run, TerminalOutcome.COMPLETED)

    def test_a_duplicate_record_identity_is_refused(self):
        gate = prerequisite_gate("gate.dup", "pre.dup")
        orch = build()
        run, item = started(orch, simple_task(gates=(gate,)))
        evidence = PrerequisiteEvidence(PrerequisiteRecordRef("prr.dup"), gate.ref, run.ref,
                                        item.ref, PrerequisiteRef("pre.dup"),
                                        GateOutcome.SATISFIED, StorageRecordRef("sr"))
        orch.record_prerequisite(run, item, gate.ref, evidence)
        with self.assertRaises(AppendOnlyError):
            orch.record_prerequisite(run, item, gate.ref, evidence)

    def test_review_independence_is_recorded_not_assumed(self):
        review = review_gate("gate.r", "rp", "INDEPENDENT")
        orch = build(reviews={"rp": (GateOutcome.SATISFIED, HumanAuthorityRef("h"),
                                     "INDEPENDENT")})
        run, item = started(orch, simple_task(gates=(review,)))
        instance = orch.run_review_gate(run, item, review.ref)
        retained = run.evidence_for(run.gate_instance(item.ref, review.ref))
        self.assertIs(retained, instance)
        self.assertEqual(retained.independence_class, "INDEPENDENT")


class TestRoutingProvenance(unittest.TestCase):
    """Re-audit finding 7: a Routing Decision enters history only from the configured Router."""

    def test_there_is_no_public_recording_path(self):
        orch = build()
        self.assertFalse(hasattr(orch, "record_routing_decision"))

    def test_a_decision_from_another_router_is_refused(self):
        orch = build(eligible={"cap": (ModelRef("m"), ModelProfileRef("p"))})
        run, item = started(orch, simple_task(capability="cap"))
        request = orch.request_routing(run, item, "policy@1")
        impostor = RoutingDecision(RoutingDecisionRef("rd.imp"), request.ref, run.ref,
                                   item.ref, RouterOutcome.ELIGIBLE_CANDIDATE,
                                   RouterRef("router.other"), ModelRef("m"),
                                   ModelProfileRef("p"))
        with self.assertRaises(LineageError):
            orch._record_routing_decision(run, request, impostor)

    def test_the_recorded_decision_is_the_object_the_router_returned(self):
        orch = build(eligible={"cap": (ModelRef("m"), ModelProfileRef("p"))})
        run, item = started(orch, simple_task(capability="cap"))
        decision = orch.route(run, item, "policy@1")
        self.assertIs(run.routing_decisions()[-1], decision)

    def test_a_model_result_for_another_run_is_refused(self):
        orch = build(eligible={"cap": (ModelRef("m"), ModelProfileRef("p"))})
        run, item = started(orch, simple_task(capability="cap"))
        decision = orch.route(run, item, "policy@1")
        orch.model.execute = lambda request: ModelResult(
            run.ref, WorkItemRef("wi.elsewhere"), decision.ref, ModelRef("m"), "t")
        with self.assertRaises(LineageError):
            orch.invoke_model(run, item, decision)
        self.assertEqual(len(run.model_results()), 0)


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
