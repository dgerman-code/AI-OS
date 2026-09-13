"""Phase 12 MVP — four prohibited paths, and where each one stops.

Status: PROPOSED. Run with `python3 implementation/phase-12/examples/blocked_run.py`.

Nothing here is a caught-and-continued error. Each case ends in a state the architecture
names, and none of them ends in an approval.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adapters import InMemoryDecisionDesk, InMemoryReviewerDesk, InMemoryRouter, StubModel
from domain import (
    DecisionRightRef, GateKind, GateOutcome, GateRequirement, GovernanceError,
    GovernancePosture, HumanAuthorityRef, ModelProfileRef, ModelRef, ReviewProfileRef,
    RetryClass, RoleRef, RouterRef, RunPhase, ScopeBinding, ScopeRef, Task, TaskRef,
    TerminalOutcome, WorkflowDefinition, WorkflowRef, WorkflowRunRef,
)
from orchestrator import Orchestrator

SCOPE = ScopeBinding(ScopeRef("project.apollo"), frozenset({"INTERNAL"}), "EU")


def _orchestrator(rights=None, reviews=None, eligible=None):
    router = InMemoryRouter(RouterRef("router.phase9"), eligible=eligible or {})
    return Orchestrator(router,
                        InMemoryReviewerDesk(reviews or {}),
                        InMemoryDecisionDesk(rights or {}),
                        StubModel())


def case_missing_decision_right():
    """No approved Phase 7 Right covers the act: BLOCKED and ESCALATED, AUTHORITY_ABSENT."""
    task = Task(TaskRef("task.publish"), "Publish externally", RoleRef("role.author"),
                RetryClass.NON_RETRYABLE_GOVERNED_ACT,
                gates=(GateRequirement(GateKind.DECISION,
                                       decision_right=DecisionRightRef("dr.external")),))
    definition = WorkflowDefinition(WorkflowRef("wf.publish"), "v1", (task,), SCOPE)
    orch = _orchestrator(rights={})           # the desk holds no such Right
    run = orch.create_run(definition, WorkflowRunRef("run.block.1"))
    item = orch.activate_stage(run, task)
    outcome, record = orch.run_decision_gate(run, item, task.gates[0])
    assert outcome is GateOutcome.NO_APPLICABLE_DECISION_RIGHT
    assert record is None, "no Decision Record exists to be mistaken for an approval"
    assert run.phase is RunPhase.ESCALATED and run.posture is GovernancePosture.AUTHORITY_ABSENT
    try:
        orch.complete(run, TerminalOutcome.COMPLETED)
    except GovernanceError as exc:
        return "missing Decision Right", "%s / %s; completion refused: %s" % (
            run.phase.value, run.posture.value, exc)
    raise AssertionError("completion was not refused")


def case_scope_widening():
    """A sub-run may narrow what it sees. Widening is refused, and nothing is transferred."""
    task = Task(TaskRef("task.sub"), "Sub work", RoleRef("role.author"),
                RetryClass.SAFE_AUTOMATIC_RETRY)
    definition = WorkflowDefinition(WorkflowRef("wf.sub"), "v1", (task,), SCOPE)
    orch = _orchestrator()
    parent = orch.create_run(definition, WorkflowRunRef("run.block.2"))
    wider = ScopeBinding(SCOPE.scope, frozenset({"INTERNAL", "RESTRICTED"}), "EU")
    try:
        orch.open_sub_run(parent, definition, WorkflowRunRef("run.block.2a"), wider)
    except GovernanceError as exc:
        pass
    else:
        raise AssertionError("a widening sub-run was allowed")
    narrower = ScopeBinding(SCOPE.scope, frozenset(), "EU")
    child = orch.open_sub_run(parent, definition, WorkflowRunRef("run.block.2b"), narrower)
    # And crossing to another scope without an approved mechanism is refused outright.
    other = ScopeBinding(ScopeRef("project.zephyr"), frozenset({"INTERNAL"}), "EU")
    try:
        orch.cross_scope(child, other, mechanism=None)
    except GovernanceError as exc:
        return "scope widening and implicit crossing", (
            "widening refused; narrowing sub-run %s created; crossing refused: %s"
            % (child.ref, exc))
    raise AssertionError("an implicit scope crossing was allowed")


def case_failed_independent_review():
    """A review that is NOT_SATISFIED sends work back. It never becomes a continuation."""
    task = Task(TaskRef("task.review"), "Reviewed work", RoleRef("role.author"),
                RetryClass.SAFE_AUTOMATIC_RETRY,
                gates=(GateRequirement(GateKind.REVIEW,
                                       review_profile=ReviewProfileRef("rp.independent")),))
    definition = WorkflowDefinition(WorkflowRef("wf.review"), "v1", (task,), SCOPE)
    orch = _orchestrator(reviews={
        "rp.independent": (GateOutcome.NOT_SATISFIED,
                           HumanAuthorityRef("human.reviewer"), "INDEPENDENT")})
    run = orch.create_run(definition, WorkflowRunRef("run.block.3"))
    item = orch.activate_stage(run, task)
    review = orch.run_review_gate(run, item, task.gates[0])
    assert review.outcome is GateOutcome.NOT_SATISFIED
    assert run.phase is RunPhase.REWORK_REQUIRED
    try:
        orch.complete(run, TerminalOutcome.COMPLETED)
    except Exception as exc:
        return "failed independent review", "%s / %s; completion refused: %s" % (
            run.phase.value, run.posture.value, exc)
    raise AssertionError("completion was not refused")


def case_non_retryable_governed_act():
    """A governed act performed once is never re-executed automatically."""
    task = Task(TaskRef("task.sign"), "Sign the contract", RoleRef("role.author"),
                RetryClass.NON_RETRYABLE_GOVERNED_ACT)
    definition = WorkflowDefinition(WorkflowRef("wf.sign"), "v1", (task,), SCOPE)
    orch = _orchestrator()
    run = orch.create_run(definition, WorkflowRunRef("run.block.4"))
    item = orch.activate_stage(run, task)
    phase = orch.retry(run, item, task)
    assert phase is RunPhase.ESCALATED
    assert "retry:dispatched" not in orch.log.kinds()
    return "non-retryable governed act", (
        "%s / %s; no automatic retry was dispatched" % (run.phase.value, run.posture.value))


def main():
    for name, detail in (case_missing_decision_right(), case_scope_widening(),
                         case_failed_independent_review(),
                         case_non_retryable_governed_act()):
        print("BLOCKED  %-34s %s" % (name, detail))
    return 0


if __name__ == "__main__":
    sys.exit(main())
