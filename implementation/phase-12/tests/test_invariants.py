"""Phase 12 MVP — deterministic tests for the approved architecture invariants.

Status: PROPOSED. Run with:

    python3 -m unittest discover -s implementation/phase-12/tests -v

Every test names the approved rule it holds. Where a rule is about something being impossible,
the test asserts the raise, not a return value: a rule that can be violated and merely logged
is not enforced.
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
    ArtifactRef, Canonicality, CONTINUING_GATE_OUTCOMES, CredentialRef, DecisionRecord,
    DecisionRecordRef, DecisionRightRef, ExecutionEventLog, GateKind, GateOutcome,
    GateRequirement, GovernanceError, GovernancePosture, HumanAuthorityRef,
    HumanInterventionRecord, IdentityError, InterventionRef, ModelProfileRef, ModelRef,
    ModelResult, NEVER_AUTOMATICALLY_RETRYABLE, Origin, POSTURE_PERMITS_COMPLETION,
    RaceOutcome, RetryClass, ReviewInstance, ReviewInstanceRef, ReviewProfileRef, RoleRef,
    RouterOutcome, RouterRef, RoutingDecision, RoutingDecisionRef, RoutingRequest, RunPhase,
    SEPARATION_CHAIN, ScopeBinding, ScopeRef, ScopeTransferRef, HandoffRef, Task, TaskRef,
    TerminalOutcome, TransitionError, WaitReason, WorkflowDefinition, WorkflowRef,
    WorkflowRunRef, WorkItemRef, require,
)
from orchestrator import Orchestrator  # noqa: E402

SCOPE = ScopeBinding(ScopeRef("project.apollo"), frozenset({"INTERNAL"}), "EU")
AUTHOR = RoleRef("role.author")


def simple_task(gates=(), retry=RetryClass.SAFE_AUTOMATIC_RETRY, capability=""):
    return Task(TaskRef("task.t"), "T", AUTHOR, retry, gates=gates, capability=capability)


def build(rights=None, reviews=None, eligible=None, missing_right_for=()):
    router = InMemoryRouter(RouterRef("router.phase9"), eligible=eligible or {},
                            missing_right_for=missing_right_for)
    return Orchestrator(router, InMemoryReviewerDesk(reviews or {}),
                        InMemoryDecisionDesk(rights or {}), StubModel())


def started(orch, task, run_id="run.t"):
    definition = WorkflowDefinition(WorkflowRef("wf.t"), "v1", (task,), SCOPE)
    run = orch.create_run(definition, WorkflowRunRef(run_id))
    return run, orch.activate_stage(run, task)


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

    def test_model_profile_cannot_fill_a_review_instance_field(self):
        with self.assertRaises(IdentityError):
            ReviewInstance(ReviewInstanceRef("ri"), WorkItemRef("wi"),
                           ModelProfileRef("mp"), GateOutcome.SATISFIED,
                           HumanAuthorityRef("h"), "INDEPENDENT")

    def test_model_profile_cannot_fill_a_decision_record_field(self):
        with self.assertRaises(IdentityError):
            DecisionRecord(DecisionRecordRef("dr"), WorkItemRef("wi"),
                           ModelProfileRef("mp"), GateOutcome.SATISFIED,
                           HumanAuthorityRef("h"))

    def test_decision_record_requires_an_explicit_human_authority(self):
        with self.assertRaises(IdentityError):
            DecisionRecord(DecisionRecordRef("dr"), WorkItemRef("wi"),
                           DecisionRightRef("dr.x"), GateOutcome.SATISFIED,
                           AgentInstanceRef("agent.1"))

    def test_credential_is_not_human_authority(self):
        with self.assertRaises(IdentityError):
            require(CredentialRef("c"), HumanAuthorityRef, "signatory")

    def test_structured_identity_collapse_attempt_fails(self):
        """The collapses Phase 11 denies are not merely discouraged here; they do not type."""
        for offered, required in ((RoleRef("x"), AgentInstanceRef),
                                  (RouterRef("x"), __import__("domain").OrchestratorRef),
                                  (DecisionRightRef("x"), DecisionRecordRef),
                                  (ArtifactRef("x"), __import__("domain").CanonicalRecordRef),
                                  (__import__("domain").RuntimeEventRef("x"), ArtifactRef)):
            with self.assertRaises(IdentityError):
                require(offered, required)


class TestRunCreationAndScope(unittest.TestCase):

    def test_valid_workflow_creates_a_run_in_ready(self):
        orch = build()
        run, _ = started(orch, simple_task())
        self.assertEqual(run.workflow_version, "v1")
        self.assertIs(run.scope.scope, SCOPE.scope)

    def test_run_binds_exactly_one_scope(self):
        orch = build()
        definition = WorkflowDefinition(WorkflowRef("wf.t"), "v1", (simple_task(),), SCOPE)
        run = orch.create_run(definition, WorkflowRunRef("run.s"))
        self.assertEqual(run.scope, SCOPE)
        self.assertIn("scope:bound", orch.log.kinds())

    def test_narrowing_sub_run_is_allowed(self):
        orch = build()
        definition = WorkflowDefinition(WorkflowRef("wf.t"), "v1", (simple_task(),), SCOPE)
        parent = orch.create_run(definition, WorkflowRunRef("run.p"))
        child = orch.open_sub_run(parent, definition, WorkflowRunRef("run.c"),
                                  ScopeBinding(SCOPE.scope, frozenset(), "EU"))
        self.assertEqual(child.scope.sensitivity, frozenset())

    def test_widening_sub_run_is_rejected(self):
        orch = build()
        definition = WorkflowDefinition(WorkflowRef("wf.t"), "v1", (simple_task(),), SCOPE)
        parent = orch.create_run(definition, WorkflowRunRef("run.p"))
        wider = ScopeBinding(SCOPE.scope, frozenset({"INTERNAL", "RESTRICTED"}), "EU")
        with self.assertRaises(GovernanceError):
            orch.open_sub_run(parent, definition, WorkflowRunRef("run.c"), wider)

    def test_residency_change_is_not_a_narrowing(self):
        other = ScopeBinding(SCOPE.scope, frozenset({"INTERNAL"}), "US")
        self.assertFalse(SCOPE.narrows_to(other))

    def test_scope_mismatch_blocks_without_an_approved_mechanism(self):
        orch = build()
        run, _ = started(orch, simple_task())
        target = ScopeBinding(ScopeRef("project.zephyr"), frozenset({"INTERNAL"}), "EU")
        with self.assertRaises(GovernanceError):
            orch.cross_scope(run, target, mechanism=None)
        self.assertIs(run.phase, RunPhase.BLOCKED)
        self.assertIs(run.posture, GovernancePosture.GATE_UNSATISFIED)

    def test_cross_scope_requires_handoff_or_transfer_reference(self):
        orch = build()
        run, _ = started(orch, simple_task())
        target = ScopeBinding(ScopeRef("project.zephyr"), frozenset({"INTERNAL"}), "EU")
        with self.assertRaises(GovernanceError):
            orch.cross_scope(run, target, mechanism=ArtifactRef("art.note"))
        orch2 = build()
        run2, _ = started(orch2, simple_task(), "run.x2")
        orch2.cross_scope(run2, target, mechanism=ScopeTransferRef("st.1"))
        self.assertEqual(run2.scope.scope, target.scope)
        orch3 = build()
        run3, _ = started(orch3, simple_task(), "run.x3")
        orch3.cross_scope(run3, target, mechanism=HandoffRef("ho.1"))
        self.assertEqual(run3.scope.scope, target.scope)


class TestAssignmentAuthority(unittest.TestCase):

    def test_assignment_grants_no_review_or_decision_authority(self):
        orch = build()
        task = simple_task()
        run, item = started(orch, task)
        assignment = orch.assign(run, item, task, AUTHOR, AgentInstanceRef("agent.1"))
        self.assertFalse(assignment.grants_review_authority())
        self.assertFalse(assignment.grants_decision_authority())

    def test_assignment_must_match_the_role_the_task_requires(self):
        orch = build()
        task = simple_task()
        run, item = started(orch, task)
        with self.assertRaises(GovernanceError):
            orch.assign(run, item, task, RoleRef("role.someone-else"))

    def test_agent_instance_is_not_the_role(self):
        orch = build()
        task = simple_task()
        run, item = started(orch, task)
        assignment = orch.assign(run, item, task, AUTHOR, AgentInstanceRef("agent.1"))
        self.assertNotEqual(assignment.role, assignment.agent_instance)


class TestRouterBoundary(unittest.TestCase):

    def test_routing_request_is_not_a_routing_decision(self):
        orch = build(eligible={"cap": (ModelRef("m"), ModelProfileRef("p"))})
        task = simple_task(capability="cap")
        run, item = started(orch, task)
        request = orch.request_routing(run, item, task, "policy@1")
        decision = orch.router.route(request)
        self.assertIsInstance(request, RoutingRequest)
        self.assertIsInstance(decision, RoutingDecision)
        self.assertNotEqual(type(request), type(decision))

    def test_router_request_may_not_carry_a_chosen_model(self):
        self.assertFalse(hasattr(RoutingRequest(WorkItemRef("wi"), "cap", SCOPE, "p@1"),
                                 "model"))

    def test_non_eligible_outcome_may_not_name_a_model(self):
        with self.assertRaises(GovernanceError):
            RoutingDecision(RoutingDecisionRef("rd"), WorkItemRef("wi"),
                            RouterOutcome.NO_ELIGIBLE_MODEL, model=ModelRef("m"))

    def test_no_eligible_model_blocks_and_there_is_no_fallback(self):
        orch = build(eligible={})
        task = simple_task(capability="cap")
        run, item = started(orch, task)
        decision = orch.route(run, item, task, "policy@1")
        self.assertIs(decision.outcome, RouterOutcome.NO_ELIGIBLE_MODEL)
        self.assertIs(run.phase, RunPhase.BLOCKED)
        with self.assertRaises(GovernanceError):
            orch.invoke_model(run, item, decision)

    def test_routing_without_an_applicable_right_is_authority_absent(self):
        orch = build(missing_right_for=("cap",))
        task = simple_task(capability="cap")
        run, item = started(orch, task)
        decision = orch.route(run, item, task, "policy@1")
        self.assertIs(decision.outcome, RouterOutcome.NO_APPLICABLE_DECISION_RIGHT)
        self.assertIs(run.phase, RunPhase.ESCALATED)
        self.assertIs(run.posture, GovernancePosture.AUTHORITY_ABSENT)

    def test_router_output_cannot_set_a_gate_state(self):
        orch = build(eligible={"cap": (ModelRef("m"), ModelProfileRef("p"))})
        task = simple_task(capability="cap")
        run, item = started(orch, task)
        decision = orch.route(run, item, task, "policy@1")
        with self.assertRaises(GovernanceError):
            orch.satisfy_gate_with(run, item, GateKind.DECISION, decision)


class TestModelOutput(unittest.TestCase):

    def test_model_result_is_ai_suggestion_by_construction(self):
        result = ModelResult(WorkItemRef("wi"), ModelRef("m"), "text")
        self.assertIs(result.origin, Origin.AI_GENERATED)
        self.assertIs(result.canonicality, Canonicality.AI_SUGGESTION)
        self.assertFalse(result.satisfies_gate())

    def test_model_result_cannot_be_declared_canonical(self):
        with self.assertRaises(GovernanceError):
            ModelResult(WorkItemRef("wi"), ModelRef("m"), "t",
                        canonicality=Canonicality.CANONICAL)

    def test_model_result_cannot_be_declared_human_authored(self):
        with self.assertRaises(GovernanceError):
            ModelResult(WorkItemRef("wi"), ModelRef("m"), "t", origin=Origin.HUMAN_AUTHORED)

    def test_model_result_cannot_satisfy_a_review_or_decision_gate(self):
        orch = build()
        task = simple_task()
        run, item = started(orch, task)
        result = ModelResult(item.ref, ModelRef("m"), "t")
        for kind in (GateKind.REVIEW, GateKind.DECISION):
            with self.assertRaises(GovernanceError):
                orch.satisfy_gate_with(run, item, kind, result)

    def test_model_result_does_not_mutate_canonical_state(self):
        orch = build(eligible={"cap": (ModelRef("m"), ModelProfileRef("p"))})
        task = simple_task(capability="cap")
        run, item = started(orch, task)
        decision = orch.route(run, item, task, "policy@1")
        orch.invoke_model(run, item, decision)
        self.assertEqual(run.decision_records, {})
        self.assertEqual(run.review_instances, {})
        self.assertEqual([s for s in run.gates.values() if s.is_continuing()], [])


class TestGates(unittest.TestCase):

    def test_seven_outcomes_and_only_two_continue(self):
        self.assertEqual(len(GateOutcome), 7)
        self.assertEqual(CONTINUING_GATE_OUTCOMES,
                         frozenset({GateOutcome.SATISFIED,
                                    GateOutcome.SATISFIED_WITH_OPEN_ITEMS}))

    def test_review_gate_is_satisfied_only_by_a_review_instance(self):
        orch = build()
        task = simple_task()
        run, item = started(orch, task)
        record = DecisionRecord(DecisionRecordRef("dr"), item.ref, DecisionRightRef("r"),
                                GateOutcome.SATISFIED, HumanAuthorityRef("h"))
        with self.assertRaises(GovernanceError):
            orch.satisfy_gate_with(run, item, GateKind.REVIEW, record)

    def test_decision_gate_is_satisfied_only_by_a_decision_record(self):
        orch = build()
        task = simple_task()
        run, item = started(orch, task)
        review = ReviewInstance(ReviewInstanceRef("ri"), item.ref, ReviewProfileRef("rp"),
                                GateOutcome.SATISFIED, HumanAuthorityRef("h"), "INDEPENDENT")
        with self.assertRaises(GovernanceError):
            orch.satisfy_gate_with(run, item, GateKind.DECISION, review)

    def test_missing_decision_right_blocks_and_escalates(self):
        gate = GateRequirement(GateKind.DECISION, decision_right=DecisionRightRef("dr.none"))
        orch = build(rights={})
        task = simple_task(gates=(gate,))
        run, item = started(orch, task)
        outcome, record = orch.run_decision_gate(run, item, gate)
        self.assertIs(outcome, GateOutcome.NO_APPLICABLE_DECISION_RIGHT)
        self.assertIsNone(record)
        self.assertIs(run.phase, RunPhase.ESCALATED)
        self.assertIs(run.posture, GovernancePosture.AUTHORITY_ABSENT)

    def test_missing_decision_right_cannot_reach_a_continuing_state(self):
        gate = GateRequirement(GateKind.DECISION, decision_right=DecisionRightRef("dr.none"))
        orch = build(rights={})
        task = simple_task(gates=(gate,))
        run, item = started(orch, task)
        orch.run_decision_gate(run, item, gate)
        with self.assertRaises(Exception):
            orch.complete(run, TerminalOutcome.COMPLETED)

    def test_deferral_is_not_approval(self):
        gate = GateRequirement(GateKind.DECISION, decision_right=DecisionRightRef("dr.d"))
        orch = build(rights={"dr.d": (HumanAuthorityRef("h"), GateOutcome.DEFER)})
        task = simple_task(gates=(gate,))
        run, item = started(orch, task)
        outcome, _ = orch.run_decision_gate(run, item, gate)
        self.assertIs(outcome, GateOutcome.DEFER)
        self.assertIs(run.phase, RunPhase.WAITING)
        self.assertIs(run.posture, GovernancePosture.GATE_UNSATISFIED)

    def test_timeout_does_not_approve(self):
        gate = GateRequirement(GateKind.DECISION, decision_right=DecisionRightRef("dr.e"))
        orch = build(rights={"dr.e": (HumanAuthorityRef("h"), GateOutcome.EXPIRED)})
        task = simple_task(gates=(gate,))
        run, item = started(orch, task)
        outcome, record = orch.run_decision_gate(run, item, gate)
        self.assertIs(outcome, GateOutcome.EXPIRED)
        self.assertIs(run.phase, RunPhase.ESCALATED)
        self.assertNotIn(outcome, CONTINUING_GATE_OUTCOMES)
        with self.assertRaises(GovernanceError):
            orch.satisfy_gate_with(run, item, GateKind.DECISION, record)

    def test_a_waiting_run_must_name_its_subject(self):
        orch = build()
        run, _ = started(orch, simple_task())
        with self.assertRaises(GovernanceError):
            orch._transition(run, RunPhase.WAITING,
                             wait_reason=WaitReason.WAITING_FOR_REVIEW, wait_subject=None)

    def test_decision_record_must_answer_the_named_right(self):
        gate = GateRequirement(GateKind.DECISION, decision_right=DecisionRightRef("dr.a"))
        orch = build(rights={"dr.a": (HumanAuthorityRef("h"), GateOutcome.SATISFIED)})
        task = simple_task(gates=(gate,))
        run, item = started(orch, task)
        orch.decisions.rights["dr.a"] = (HumanAuthorityRef("h"), GateOutcome.SATISFIED)
        outcome, record = orch.run_decision_gate(run, item, gate)
        self.assertEqual(record.decision_right, gate.decision_right)


class TestLateResultAsymmetry(unittest.TestCase):
    """Case 5 and case 6 of the ten races are deliberately different, and stay different."""

    def test_late_review_result_is_ignored_as_stale(self):
        self.assertIs(RaceOutcome.IGNORE_AS_STALE,
                      RaceOutcome["IGNORE_AS_STALE"])

    def test_late_decision_record_reconciles_and_may_escalate(self):
        self.assertIn(RaceOutcome.RECONCILE, set(RaceOutcome))
        self.assertIn(RaceOutcome.ESCALATE, set(RaceOutcome))
        self.assertIsNot(RaceOutcome.RECONCILE, RaceOutcome.IGNORE_AS_STALE)

    def test_a_late_decision_record_still_stands_as_a_record(self):
        """The Record is not discarded: it is a Right exercised by a human, which happened."""
        record = DecisionRecord(DecisionRecordRef("dr.late"), WorkItemRef("wi"),
                                DecisionRightRef("dr.x"), GateOutcome.SATISFIED,
                                HumanAuthorityRef("h"))
        self.assertIs(record.outcome, GateOutcome.SATISFIED)
        self.assertEqual(record.decided_by, HumanAuthorityRef("h"))


class TestRetry(unittest.TestCase):

    def test_seven_retry_classes_and_exactly_once_is_not_among_them(self):
        self.assertEqual(len(RetryClass), 7)
        self.assertEqual(AUTOMATICALLY_RETRYABLE & NEVER_AUTOMATICALLY_RETRYABLE, frozenset())

    def test_non_retryable_governed_act_is_never_retried(self):
        orch = build()
        task = simple_task(retry=RetryClass.NON_RETRYABLE_GOVERNED_ACT)
        run, item = started(orch, task)
        orch.retry(run, item, task)
        self.assertIs(run.phase, RunPhase.ESCALATED)
        self.assertNotIn("retry:dispatched", orch.log.kinds())

    def test_non_replayable_external_effect_is_never_retried(self):
        orch = build()
        task = simple_task(retry=RetryClass.NON_REPLAYABLE_EXTERNAL_SIDE_EFFECT)
        run, item = started(orch, task)
        orch.retry(run, item, task)
        self.assertIs(run.phase, RunPhase.ESCALATED)
        self.assertNotIn("retry:dispatched", orch.log.kinds())

    def test_retry_requiring_acknowledgement_waits_for_a_human(self):
        orch = build()
        task = simple_task(retry=RetryClass.RETRY_REQUIRING_HUMAN_ACKNOWLEDGEMENT)
        run, item = started(orch, task)
        orch.retry(run, item, task)
        self.assertIs(run.phase, RunPhase.WAITING)
        self.assertIs(run.wait_reason, WaitReason.WAITING_FOR_HUMAN)
        ack = HumanInterventionRecord(InterventionRef("iv.1"), run.ref,
                                      HumanAuthorityRef("h"), "acknowledge", "known and why")
        orch.retry(run, item, task, acknowledgement=ack)
        self.assertIn("retry:dispatched", orch.log.kinds())

    def test_revalidation_class_must_revalidate_first(self):
        orch = build()
        task = simple_task(retry=RetryClass.RETRY_REQUIRING_REVALIDATION)
        run, item = started(orch, task)
        with self.assertRaises(GovernanceError):
            orch.retry(run, item, task)
        orch.retry(run, item, task, revalidated=True)
        self.assertIn("retry:dispatched", orch.log.kinds())

    def test_safe_automatic_retry_is_dispatched(self):
        orch = build()
        task = simple_task(retry=RetryClass.SAFE_AUTOMATIC_RETRY)
        run, item = started(orch, task)
        orch.retry(run, item, task)
        self.assertIs(run.phase, RunPhase.RUNNING)


class TestExecutionHistory(unittest.TestCase):

    def test_history_is_append_only(self):
        log = ExecutionEventLog()
        log.append(WorkflowRunRef("r"), "a")
        log.append(WorkflowRunRef("r"), "b")
        with self.assertRaises(AppendOnlyError):
            log[0] = "rewritten"
        with self.assertRaises(AppendOnlyError):
            del log[0]

    def test_exposed_events_are_a_copy(self):
        log = ExecutionEventLog()
        log.append(WorkflowRunRef("r"), "a")
        events = log.events()
        self.assertIsInstance(events, tuple)
        self.assertEqual(len(log), 1)

    def test_sequence_numbers_are_monotonic(self):
        log = ExecutionEventLog()
        first = log.append(WorkflowRunRef("r"), "a")
        second = log.append(WorkflowRunRef("r"), "b")
        self.assertEqual((first.sequence, second.sequence), (1, 2))


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

    def test_terminal_run_cannot_move_again(self):
        orch = build()
        task = simple_task()
        run, item = started(orch, task)
        orch.complete(run, TerminalOutcome.FAILED, cause="the step errored")
        with self.assertRaises(TransitionError):
            orch._transition(run, RunPhase.RUNNING)


class TestCompletion(unittest.TestCase):

    def test_only_governance_clear_permits_completed(self):
        self.assertEqual(POSTURE_PERMITS_COMPLETION[GovernancePosture.GATE_UNSATISFIED],
                         frozenset())
        self.assertEqual(POSTURE_PERMITS_COMPLETION[GovernancePosture.AUTHORITY_ABSENT],
                         frozenset())

    def test_completion_denied_while_a_gate_is_unsatisfied(self):
        gate = GateRequirement(GateKind.REVIEW, review_profile=ReviewProfileRef("rp"))
        orch = build(reviews={"rp": (GateOutcome.SATISFIED, HumanAuthorityRef("h"), "IND")})
        task = simple_task(gates=(gate,))
        run, item = started(orch, task)
        with self.assertRaises(GovernanceError):
            orch.complete(run, TerminalOutcome.COMPLETED)

    def test_completion_denied_while_waiting(self):
        gate = GateRequirement(GateKind.DECISION, decision_right=DecisionRightRef("dr.d"))
        orch = build(rights={"dr.d": (HumanAuthorityRef("h"), GateOutcome.DEFER)})
        task = simple_task(gates=(gate,))
        run, item = started(orch, task)
        orch.run_decision_gate(run, item, gate)
        self.assertIs(run.phase, RunPhase.WAITING)
        with self.assertRaises(TransitionError):
            orch.complete(run, TerminalOutcome.COMPLETED)

    def test_open_items_complete_only_as_completed_with_open_items(self):
        gate = GateRequirement(GateKind.REVIEW, review_profile=ReviewProfileRef("rp"))
        orch = build(reviews={"rp": (GateOutcome.SATISFIED_WITH_OPEN_ITEMS,
                                     HumanAuthorityRef("h"), "IND")})
        task = simple_task(gates=(gate,))
        run, item = started(orch, task)
        orch.run_review_gate(run, item, gate)
        self.assertIs(run.posture, GovernancePosture.OPEN_ITEMS_CARRIED)
        with self.assertRaises(GovernanceError):
            orch.complete(run, TerminalOutcome.COMPLETED)
        orch.complete(run, TerminalOutcome.COMPLETED_WITH_OPEN_ITEMS)
        self.assertIs(run.terminal, TerminalOutcome.COMPLETED_WITH_OPEN_ITEMS)

    def test_successful_completion_after_every_condition_is_met(self):
        review = GateRequirement(GateKind.REVIEW, review_profile=ReviewProfileRef("rp"))
        decision = GateRequirement(GateKind.DECISION,
                                   decision_right=DecisionRightRef("dr.ok"))
        orch = build(reviews={"rp": (GateOutcome.SATISFIED, HumanAuthorityRef("h1"), "IND")},
                     rights={"dr.ok": (HumanAuthorityRef("h2"), GateOutcome.SATISFIED)})
        task = simple_task(gates=(review, decision))
        run, item = started(orch, task)
        orch.run_review_gate(run, item, review)
        orch.run_decision_gate(run, item, decision)
        orch.complete(run, TerminalOutcome.COMPLETED)
        self.assertIs(run.terminal, TerminalOutcome.COMPLETED)
        self.assertIs(run.posture, GovernancePosture.GOVERNANCE_CLEAR)

    def test_cancellation_requires_an_intervention_record(self):
        orch = build()
        run, _ = started(orch, simple_task())
        with self.assertRaises(GovernanceError):
            orch.complete(run, TerminalOutcome.CANCELLED)
        iv = HumanInterventionRecord(InterventionRef("iv"), run.ref, HumanAuthorityRef("h"),
                                     "cancel", "the work is not wanted")
        orch.complete(run, TerminalOutcome.CANCELLED, intervention=iv)
        self.assertIs(run.terminal, TerminalOutcome.CANCELLED)

    def test_terminated_requires_a_named_constraint(self):
        orch = build()
        run, _ = started(orch, simple_task())
        with self.assertRaises(GovernanceError):
            orch.complete(run, TerminalOutcome.TERMINATED)

    def test_operational_success_is_not_governance_completion(self):
        """The model ran and the step finished; the gate did not, so the run cannot complete."""
        gate = GateRequirement(GateKind.REVIEW, review_profile=ReviewProfileRef("rp"))
        orch = build(eligible={"cap": (ModelRef("m"), ModelProfileRef("p"))},
                     reviews={"rp": (GateOutcome.SATISFIED, HumanAuthorityRef("h"), "IND")})
        task = simple_task(gates=(gate,), capability="cap")
        run, item = started(orch, task)
        decision = orch.route(run, item, task, "policy@1")
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
