"""Phase 12 MVP — a governed workflow that reaches COMPLETED, and how.

Status: PROPOSED. Run with `python3 implementation/phase-12/examples/governed_run.py`.

Demonstrates the twelve behaviours the Phase 12 objective names, in order. Every act is
addressed by reference into the run's own bound lineage — a Task reference the definition
declares, a Work Item the run created, a gate requirement with its own identity — rather than
by handing the orchestrator an object to trust.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adapters import InMemoryDecisionDesk, InMemoryReviewerDesk, InMemoryRouter, StubModel
from domain import (
    AgentInstanceRef, DecisionRightRef, GateKind, GateOutcome, GateRequirement,
    GateRequirementRef, GovernancePosture, HumanAuthorityRef, ModelProfileRef, ModelRef,
    ReviewProfileRef, RetryClass, RoleRef, RouterRef, ScopeBinding, ScopeRef, Task, TaskRef,
    TerminalOutcome, WorkflowDefinition, WorkflowRef, WorkflowRunRef,
)
from orchestrator import Orchestrator

REVIEW_GATE = GateRequirementRef("gate.peer-review")
DECISION_GATE = GateRequirementRef("gate.publish-approval")
DRAFT = TaskRef("task.draft")


def build():
    scope = ScopeBinding(ScopeRef("project.apollo"), frozenset({"INTERNAL"}), "EU")
    draft = Task(
        ref=DRAFT,
        name="Draft the change note",
        required_role=RoleRef("role.author"),
        retry_class=RetryClass.RETRY_REQUIRING_REVALIDATION,
        gates=(
            GateRequirement(REVIEW_GATE, GateKind.REVIEW,
                            review_profile=ReviewProfileRef("rp.peer"),
                            independence_class="INDEPENDENT"),
            GateRequirement(DECISION_GATE, GateKind.DECISION,
                            decision_right=DecisionRightRef("dr.publish")),
        ),
        capability="text.summarise",
    )
    definition = WorkflowDefinition(WorkflowRef("wf.change-note"), "v3", (draft,), scope)
    router = InMemoryRouter(
        RouterRef("router.phase9"),
        eligible={"text.summarise": (ModelRef("model.alpha"),
                                     ModelProfileRef("profile.alpha@2"))})
    reviewers = InMemoryReviewerDesk({
        "rp.peer": (GateOutcome.SATISFIED, HumanAuthorityRef("human.reviewer"), "INDEPENDENT")})
    decisions = InMemoryDecisionDesk({
        "dr.publish": (HumanAuthorityRef("human.approver"), GateOutcome.SATISFIED)})
    return definition, Orchestrator(router, reviewers, decisions, StubModel())


def main():
    definition, orch = build()
    say = lambda n, text: print("%2d. %s" % (n, text))

    # 1 run creation from a governed workflow definition; 2 explicit scope binding
    run = orch.create_run(definition, WorkflowRunRef("run.0001"))
    say(1, "run created from %s @ %s -> %s"
        % (run.workflow, run.workflow_version, run.phase.value))
    say(2, "scope bound: %s, sensitivity %s, residency %s"
        % (run.scope.scope, sorted(run.scope.sensitivity), run.scope.residency))

    # 3 stage activation, by reference into the run's own definition
    item = orch.activate_stage(run, DRAFT)
    say(3, "stage activated as %s, bound to %s @ %s (the Task itself is untouched)"
        % (item.ref, item.task, item.workflow_version))

    # 4 executor assignment without granting new authority
    assignment = orch.assign(run, item, RoleRef("role.author"), AgentInstanceRef("agent.0001"))
    say(4, "assigned %s / %s; grants review authority: %s, decision authority: %s"
        % (assignment.role, assignment.agent_instance,
           assignment.grants_review_authority(), assignment.grants_decision_authority()))

    # 5 router request creation distinct from routing decision, and bound to it
    request = orch.request_routing(run, item, "routing_policy.default@7")
    decision = orch.record_routing_decision(run, request, orch.router.route(request))
    say(5, "RoutingRequest(%s) -> RoutingDecision(%s) %s, answering that exact request: %s"
        % (request.ref, decision.ref, decision.outcome.value, decision.answers(request)))

    # 6 model result recorded as suggestion, not approval
    result = orch.invoke_model(run, item, decision, "draft the note")
    say(6, "model result: origin=%s canonicality=%s, satisfies a gate: %s"
        % (result.origin.value, result.canonicality.value, result.satisfies_gate()))

    # 7 review request and review result as separate governed objects
    review = orch.run_review_gate(run, item, REVIEW_GATE)
    say(7, "ReviewRequest -> ReviewInstance(%s) %s by %s at %s"
        % (review.ref, review.outcome.value, review.reviewer, review.independence_class))

    # 8 the absent-Right path is the second synthetic case, in examples/blocked_run.py
    say(8, "missing Decision Right -> BLOCKED + ESCALATED + AUTHORITY_ABSENT: "
           "see examples/blocked_run.py, case 1")

    # 9 a human decision record satisfying a gate where the Right exists
    outcome, record = orch.run_decision_gate(run, item, DECISION_GATE)
    say(9, "DecisionRequest -> DecisionRecord(%s) %s by %s, who holds %s"
        % (record.ref, outcome.value, record.decided_by, record.decision_right))

    # 10 retry behaviour taken from the Work Item's bound retry class
    phase = orch.retry(run, item, revalidated=True)
    say(10, "retry of a %s work item: revalidated first, phase now %s"
        % (item.retry_class.value, phase.value))

    # 11 append-only execution events
    say(11, "%d execution events recorded, append-only" % len(orch.log))

    # 12 terminal completion only when the posture permits it
    say(12, "posture %s, unsatisfied gates %d of %d"
        % (run.posture.value, len(orch.unsatisfied_gates(run)), len(run.gates())))
    orch.complete(run, TerminalOutcome.COMPLETED)
    print("\nfinal axes: phase=%s terminal=%s wait=%s posture=%s"
          % (run.phase.value, run.terminal.value, run.wait_reason, run.posture.value))
    assert run.terminal is TerminalOutcome.COMPLETED
    assert run.posture is GovernancePosture.GOVERNANCE_CLEAR
    return 0


if __name__ == "__main__":
    sys.exit(main())
