"""Phase 12 MVP — prohibited paths, and where each one stops.

Status: PROPOSED. Run with `python3 implementation/phase-12/examples/blocked_run.py`.

Four governance stops, then eight structural bypasses the independent audit found. Nothing here
is a caught-and-continued error: each case ends in a state the architecture names, or in a
refusal, and none of them ends in an approval.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adapters import InMemoryDecisionDesk, InMemoryReviewerDesk, InMemoryRouter, StubModel
from domain import (
    DecisionRecord, DecisionRecordRef, DecisionRightRef, GateKind, GateOutcome,
    GateRequirement, GateRequirementRef, GovernanceError, GovernancePosture, HandoffRef,
    HumanAuthorityRef, ModelProfileRef, ModelRef, ReviewProfileRef, RetryClass, RoleRef,
    RouterOutcome, RouterRef, RoutingDecision, RoutingDecisionRef, RoutingRequestRef, RunPhase,
    ScopeBinding, ScopeRef, ScopeTransferRef, StateAccessError, Task, TaskRef, TerminalOutcome,
    WorkflowDefinition, WorkflowRef, WorkflowRunRef,
)
from orchestrator import Orchestrator

SCOPE = ScopeBinding(ScopeRef("project.apollo"), frozenset({"INTERNAL"}), "EU")
AUTHOR = RoleRef("role.author")


def _orchestrator(rights=None, reviews=None, eligible=None):
    return Orchestrator(InMemoryRouter(RouterRef("router.phase9"), eligible=eligible or {}),
                        InMemoryReviewerDesk(reviews or {}),
                        InMemoryDecisionDesk(rights or {}), StubModel())


def _definition(task, name="wf.x", version="v1"):
    return WorkflowDefinition(WorkflowRef(name), version, (task,), SCOPE)


def _refused(fn):
    """Run `fn`, expecting a governance refusal, and return its message."""
    try:
        fn()
    except GovernanceError as exc:
        return "%s: %s" % (type(exc).__name__, exc)
    raise AssertionError("the act was not refused")


# --------------------------------------------------------------------- governance stops


def case_missing_decision_right():
    gate = GateRequirement(GateRequirementRef("gate.external"), GateKind.DECISION,
                           decision_right=DecisionRightRef("dr.external"))
    task = Task(TaskRef("task.publish"), "Publish externally", AUTHOR,
                RetryClass.NON_RETRYABLE_GOVERNED_ACT, gates=(gate,))
    orch = _orchestrator(rights={})
    run = orch.create_run(_definition(task), WorkflowRunRef("run.block.1"))
    item = orch.activate_stage(run, task.ref)
    outcome, record = orch.run_decision_gate(run, item, gate.ref)
    assert outcome is GateOutcome.NO_APPLICABLE_DECISION_RIGHT and record is None
    assert run.phase is RunPhase.ESCALATED
    assert run.posture is GovernancePosture.AUTHORITY_ABSENT
    return "missing Decision Right", "%s / %s; no Decision Record exists at all" % (
        run.phase.value, run.posture.value)


def case_scope_widening_and_implicit_crossing():
    task = Task(TaskRef("task.sub"), "Sub work", AUTHOR, RetryClass.SAFE_AUTOMATIC_RETRY)
    definition = _definition(task, "wf.sub")
    orch = _orchestrator()
    parent = orch.create_run(definition, WorkflowRunRef("run.block.2"))
    wider = ScopeBinding(SCOPE.scope, frozenset({"INTERNAL", "RESTRICTED"}), "EU")
    widening = _refused(lambda: orch.open_sub_run(parent, definition,
                                                  WorkflowRunRef("run.block.2a"), wider))
    child = orch.open_sub_run(parent, definition, WorkflowRunRef("run.block.2b"),
                              ScopeBinding(SCOPE.scope, frozenset(), "EU"))
    other = ScopeBinding(ScopeRef("project.zephyr"), frozenset({"INTERNAL"}), "EU")
    crossing = _refused(lambda: orch.transfer_scope(child, definition,
                                                    WorkflowRunRef("run.block.2c"), other,
                                                    authorisation=None))
    return "scope widening and implicit crossing", "%s | %s" % (widening[:60], crossing[:70])


def case_failed_independent_review():
    gate = GateRequirement(GateRequirementRef("gate.independent"), GateKind.REVIEW,
                           review_profile=ReviewProfileRef("rp.independent"),
                           independence_class="INDEPENDENT")
    task = Task(TaskRef("task.review"), "Reviewed work", AUTHOR,
                RetryClass.SAFE_AUTOMATIC_RETRY, gates=(gate,))
    orch = _orchestrator(reviews={"rp.independent": (GateOutcome.NOT_SATISFIED,
                                                     HumanAuthorityRef("human.r"),
                                                     "INDEPENDENT")})
    run = orch.create_run(_definition(task, "wf.review"), WorkflowRunRef("run.block.3"))
    item = orch.activate_stage(run, task.ref)
    review = orch.run_review_gate(run, item, gate.ref)
    assert review.outcome is GateOutcome.NOT_SATISFIED
    assert run.phase is RunPhase.REWORK_REQUIRED
    return "failed independent review", "%s / %s; completion unreachable" % (
        run.phase.value, run.posture.value)


def case_non_retryable_governed_act():
    task = Task(TaskRef("task.sign"), "Sign the contract", AUTHOR,
                RetryClass.NON_RETRYABLE_GOVERNED_ACT)
    orch = _orchestrator()
    run = orch.create_run(_definition(task, "wf.sign"), WorkflowRunRef("run.block.4"))
    item = orch.activate_stage(run, task.ref)
    orch.retry(run, item)
    assert run.phase is RunPhase.ESCALATED
    assert "retry:dispatched" not in orch.log.kinds()
    return "non-retryable governed act", "%s / %s; no automatic retry dispatched" % (
        run.phase.value, run.posture.value)


# --------------------------------------------------------------------- structural bypasses


def _governed_setup(gates=(), retry=RetryClass.SAFE_AUTOMATIC_RETRY, capability="",
                    rights=None, reviews=None, eligible=None, run_id="run.byp"):
    task = Task(TaskRef("task.b"), "B", AUTHOR, retry, gates=gates, capability=capability)
    orch = _orchestrator(rights=rights, reviews=reviews, eligible=eligible)
    run = orch.create_run(_definition(task, "wf.b"), WorkflowRunRef(run_id))
    return orch, run, task, orch.activate_stage(run, task.ref)


def bypass_undeclared_task():
    orch, run, task, _ = _governed_setup(run_id="run.byp.1")
    return "undeclared Task activation", _refused(
        lambda: orch.activate_stage(run, TaskRef("task.not-declared")))[:90]


def bypass_foreign_decision_record():
    gate = GateRequirement(GateRequirementRef("gate.d"), GateKind.DECISION,
                           decision_right=DecisionRightRef("dr.ok"))
    orch, run, task, item = _governed_setup(
        gates=(gate,), rights={"dr.ok": (HumanAuthorityRef("h"), GateOutcome.SATISFIED)},
        run_id="run.byp.2")
    forged = DecisionRecord(DecisionRecordRef("dr.forged"), gate.ref,
                            WorkflowRunRef("run.elsewhere"), item.ref,
                            DecisionRightRef("dr.ok"), GateOutcome.SATISFIED,
                            HumanAuthorityRef("h"))
    return "foreign Decision Record", _refused(
        lambda: orch.satisfy_gate_with(run, item, gate.ref, forged))[:90]


def bypass_two_gates_of_one_kind():
    first = GateRequirement(GateRequirementRef("gate.d1"), GateKind.DECISION,
                            decision_right=DecisionRightRef("dr.one"))
    second = GateRequirement(GateRequirementRef("gate.d2"), GateKind.DECISION,
                             decision_right=DecisionRightRef("dr.two"))
    orch, run, task, item = _governed_setup(
        gates=(first, second),
        rights={"dr.one": (HumanAuthorityRef("h1"), GateOutcome.SATISFIED)},
        run_id="run.byp.3")
    orch.run_decision_gate(run, item, first.ref)
    open_gates = len(orch.unsatisfied_gates(run))
    refusal = _refused(lambda: orch.complete(run, TerminalOutcome.COMPLETED))
    return "two decision gates do not collapse", (
        "%d of %d still open; %s" % (open_gates, len(run.gates()), refusal[:55]))


def bypass_review_independence_mismatch():
    gate = GateRequirement(GateRequirementRef("gate.r"), GateKind.REVIEW,
                           review_profile=ReviewProfileRef("rp.ind"),
                           independence_class="INDEPENDENT")
    orch, run, task, item = _governed_setup(
        gates=(gate,), reviews={"rp.ind": (GateOutcome.SATISFIED, HumanAuthorityRef("h"),
                                           "NOT_INDEPENDENT")}, run_id="run.byp.4")
    return "review independence mismatch", _refused(
        lambda: orch.run_review_gate(run, item, gate.ref))[:90]


def bypass_review_in_a_human_work_gate():
    human = GateRequirement(GateRequirementRef("gate.hw"), GateKind.HUMAN_WORK,
                            human_work=__import__("domain").HumanWorkRef("hw.1"))
    review = GateRequirement(GateRequirementRef("gate.rv"), GateKind.REVIEW,
                             review_profile=ReviewProfileRef("rp.any"),
                             independence_class="INDEPENDENT")
    orch, run, task, item = _governed_setup(
        gates=(human, review),
        reviews={"rp.any": (GateOutcome.SATISFIED, HumanAuthorityRef("h"), "INDEPENDENT")},
        run_id="run.byp.5")
    instance = orch.run_review_gate(run, item, review.ref)
    return "Review Instance in a HUMAN_WORK gate", _refused(
        lambda: orch.satisfy_gate_with(run, item, human.ref, instance))[:90]


def bypass_fabricated_routing_decision():
    orch, run, task, item = _governed_setup(capability="cap", run_id="run.byp.6")
    fabricated = RoutingDecision(RoutingDecisionRef("rd.fake"), RoutingRequestRef("rr.fake"),
                                 run.ref, item.ref, RouterOutcome.ELIGIBLE_CANDIDATE,
                                 RouterRef("router.phase9"), model=ModelRef("model.chosen"),
                                 model_profile=ModelProfileRef("profile.chosen"))
    return "fabricated Routing Decision", _refused(
        lambda: orch.invoke_model(run, item, fabricated))[:90]


def bypass_retry_class_substitution():
    orch, run, task, item = _governed_setup(retry=RetryClass.NON_RETRYABLE_GOVERNED_ACT,
                                            run_id="run.byp.7")
    # There is no Task argument to substitute: the class comes from the Work Item's lineage.
    orch.retry(run, item)
    dispatched = "retry:dispatched" in orch.log.kinds()
    return "retry-class substitution", (
        "work item class %s, retried automatically: %s" % (item.retry_class.value, dispatched))


def bypass_fabricated_scope_mechanism():
    orch, run, task, item = _governed_setup(run_id="run.byp.8")
    other = ScopeBinding(ScopeRef("project.zephyr"), frozenset({"INTERNAL"}), "EU")
    definition = run.definition
    bare = _refused(lambda: orch.transfer_scope(run, definition,
                                                WorkflowRunRef("run.byp.8a"), other,
                                                authorisation=ScopeTransferRef("st.bare")))
    return "bare mechanism reference", bare[:90]


def bypass_direct_state_mutation():
    orch, run, task, item = _governed_setup(run_id="run.byp.9")
    attempts = []
    for name, value in (("phase", RunPhase.RUNNING),
                        ("posture", GovernancePosture.GOVERNANCE_CLEAR),
                        ("terminal", TerminalOutcome.COMPLETED),
                        ("scope", SCOPE)):
        try:
            setattr(run, name, value)
            attempts.append("%s WAS SETTABLE" % name)
        except StateAccessError:
            attempts.append(name)
    return "direct run-state mutation", "refused for: %s" % ", ".join(attempts)


def bypass_repeated_decision_overwrite():
    gate = GateRequirement(GateRequirementRef("gate.rep"), GateKind.DECISION,
                           decision_right=DecisionRightRef("dr.rep"))
    orch, run, task, item = _governed_setup(
        gates=(gate,), rights={"dr.rep": (HumanAuthorityRef("h"), GateOutcome.SATISFIED)},
        run_id="run.byp.10")
    orch.run_decision_gate(run, item, gate.ref)
    orch.run_decision_gate(run, item, gate.ref)
    records = run.decision_records()
    return "repeated Decision Records", (
        "%d records stand in governed history: %s"
        % (len(records), ", ".join(r.ref.id for r in records)))


def main():
    print("GOVERNANCE STOPS")
    for name, detail in (case_missing_decision_right(),
                         case_scope_widening_and_implicit_crossing(),
                         case_failed_independent_review(),
                         case_non_retryable_governed_act()):
        print("  BLOCKED  %-38s %s" % (name, detail))
    print("\nSTRUCTURAL BYPASSES CLOSED")
    for probe in (bypass_undeclared_task, bypass_foreign_decision_record,
                  bypass_two_gates_of_one_kind, bypass_review_independence_mismatch,
                  bypass_review_in_a_human_work_gate, bypass_fabricated_routing_decision,
                  bypass_retry_class_substitution, bypass_fabricated_scope_mechanism,
                  bypass_direct_state_mutation, bypass_repeated_decision_overwrite):
        name, detail = probe()
        print("  REFUSED  %-38s %s" % (name, detail))
    return 0


if __name__ == "__main__":
    sys.exit(main())
