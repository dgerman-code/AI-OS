"""Phase 12 MVP — prohibited paths, and where each one stops.

Status: PROPOSED. Run with `python3 implementation/phase-12/examples/blocked_run.py`.

Four governance stops, then eight structural bypasses the independent audit found. Nothing here
is a caught-and-continued error: each case ends in a state the architecture names, or in a
refusal, and none of them ends in an approval.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adapters import (
    InMemoryDecisionDesk, InMemoryMechanismRegistry, InMemoryReviewerDesk, InMemoryRouter,
    StubModel,
)
from domain import (
    AppendOnlyError, DecisionRecord, DecisionRecordRef, DecisionRightRef, GateKind,
    GateOutcome, GateRequirement, GateRequirementRef, GovernanceError, GovernancePosture,
    HandoffRef, HumanAuthorityRef, HumanWorkCompletion, HumanWorkRecordRef, HumanWorkRef,
    IdentityError, ModelProfileRef, ModelRef, ModelResultRef, PrerequisiteEvidence, PrerequisiteRecordRef,
    PrerequisiteRef, ReviewProfileRef, RetryClass, RoleRef, RouterOutcome, RouterRef,
    RoutingDecision, RoutingDecisionRef, RoutingRequestRef, RunPhase, ScopeBinding, ScopeRef,
    ScopeTransferAuthorisation, ScopeTransferRef, StateAccessError, StorageRecordRef, Task,
    TaskRef, TerminalOutcome, WorkflowDefinition, WorkflowRef, WorkflowRunRef,
)
from orchestrator import Orchestrator

SCOPE = ScopeBinding(ScopeRef("project.apollo"), frozenset({"INTERNAL"}), "EU")
AUTHOR = RoleRef("role.author")


def _orchestrator(rights=None, reviews=None, eligible=None, mechanisms=None):
    return Orchestrator(InMemoryRouter(RouterRef("router.phase9"), eligible=eligible or {}),
                        InMemoryReviewerDesk(reviews or {}),
                        InMemoryDecisionDesk(rights or {}), StubModel(),
                        mechanisms=mechanisms)


def _refused_any(fn):
    """Run `fn`, expecting any refusal this implementation raises."""
    try:
        fn()
    except (GovernanceError, AppendOnlyError) as exc:
        return "%s: %s" % (type(exc).__name__, exc)
    raise AssertionError("the act was not refused")


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
    return "undeclared Task activation", _refused_any(
        lambda: orch.activate_stage(run, TaskRef("task.not-declared")))[:88]


def bypass_malformed_enum_field():
    return "malformed Enum field", _refused_any(
        lambda: HumanWorkCompletion(HumanWorkRecordRef("hwr.1"), GateRequirementRef("g"),
                                    WorkflowRunRef("r"), __import__("domain").WorkItemRef("wi"),
                                    HumanWorkRef("hw"), "SATISFIED",
                                    HumanAuthorityRef("h")))[:88]


def bypass_malformed_structured_field():
    return "malformed ScopeBinding field", _refused_any(
        lambda: __import__("domain").RoutingRequest(
            RoutingRequestRef("rr"), WorkflowRunRef("r"),
            __import__("domain").WorkItemRef("wi"), "cap", "project.apollo", "p@1"))[:88]


def bypass_repeated_activation_displaces_gates():
    gate = GateRequirement(GateRequirementRef("gate.shared"), GateKind.DECISION,
                           decision_right=DecisionRightRef("dr.shared"))
    orch, run, task, first = _governed_setup(
        gates=(gate,), rights={"dr.shared": (HumanAuthorityRef("h"),
                                             GateOutcome.SATISFIED)}, run_id="run.byp.11")
    second = orch.activate_stage(run, task.ref)
    orch.run_decision_gate(run, second, gate.ref)
    open_gates = len(orch.unsatisfied_gates(run))
    refusal = _refused_any(lambda: orch.complete(run, TerminalOutcome.COMPLETED))
    return "repeated activation of one gated Task", (
        "%d work items, %d gate instances, %d still open; %s"
        % (len(run.work_items()), len(run.gates()), open_gates, refusal[:40]))


def bypass_progression_after_missing_authority():
    gate = GateRequirement(GateRequirementRef("gate.absent"), GateKind.DECISION,
                           decision_right=DecisionRightRef("dr.absent"))
    orch, run, task, item = _governed_setup(gates=(gate,), rights={}, run_id="run.byp.12")
    orch.run_decision_gate(run, item, gate.ref)
    retained = len(run.gates())
    refusal = _refused_any(lambda: orch.activate_stage(run, task.ref))
    return "progression after missing authority", (
        "%s / %s; %d gate retained; %s"
        % (run.phase.value, run.posture.value, retained, refusal[:74]))


def bypass_continuing_decision_without_record():
    gate = GateRequirement(GateRequirementRef("gate.norec"), GateKind.DECISION,
                           decision_right=DecisionRightRef("dr.norec"))
    orch, run, task, item = _governed_setup(gates=(gate,), rights={}, run_id="run.byp.13")
    orch.decisions.decide = lambda request: (GateOutcome.SATISFIED, None)
    before = (run.phase, run.posture, len(orch.log), len(run.decision_records()))
    refusal = _refused_any(lambda: orch.run_decision_gate(run, item, gate.ref))
    after = (run.phase, run.posture, len(orch.log), len(run.decision_records()))
    return "continuing outcome with no Decision Record", (
        "%s; state unchanged: %s" % (refusal[:52], before == after))


def bypass_partial_mutation_on_rejected_evidence():
    gate = GateRequirement(GateRequirementRef("gate.part"), GateKind.DECISION,
                           decision_right=DecisionRightRef("dr.part"))
    orch, run, task, item = _governed_setup(
        gates=(gate,), rights={"dr.part": (HumanAuthorityRef("h"), GateOutcome.SATISFIED)},
        run_id="run.byp.14")
    forged = DecisionRecord(DecisionRecordRef("dr.forged"), gate.ref,
                            WorkflowRunRef("run.elsewhere"), item.ref,
                            DecisionRightRef("dr.part"), GateOutcome.SATISFIED,
                            HumanAuthorityRef("h"))
    before = (run.axes(), len(orch.log), len(run.decision_records()),
              tuple(g.outcome for g in run.gates()))
    refusal = _refused_any(lambda: orch.satisfy_gate_with(run, item, gate.ref, forged))
    after = (run.axes(), len(orch.log), len(run.decision_records()),
             tuple(g.outcome for g in run.gates()))
    return "no partial mutation on rejected evidence", (
        "%s; state and history identical: %s" % (refusal[:44], before == after))


def bypass_open_items_on_human_work():
    gate = GateRequirement(GateRequirementRef("gate.hw2"), GateKind.HUMAN_WORK,
                           human_work=HumanWorkRef("hw.2"))
    orch, run, task, item = _governed_setup(gates=(gate,), run_id="run.byp.15")
    completion = HumanWorkCompletion(HumanWorkRecordRef("hwr.2"), gate.ref, run.ref, item.ref,
                                     HumanWorkRef("hw.2"),
                                     GateOutcome.SATISFIED_WITH_OPEN_ITEMS,
                                     HumanAuthorityRef("h"))
    orch.record_human_work(run, item, gate.ref, completion)
    refusal = _refused_any(lambda: orch.complete(run, TerminalOutcome.COMPLETED))
    orch.complete(run, TerminalOutcome.COMPLETED_WITH_OPEN_ITEMS)
    return "HUMAN_WORK satisfied with open items", (
        "posture %s; COMPLETED refused; terminal %s"
        % (run.posture.value, run.terminal.value))


def bypass_open_items_on_prerequisite():
    gate = GateRequirement(GateRequirementRef("gate.pre2"), GateKind.GOVERNED_PREREQUISITE,
                           prerequisite=PrerequisiteRef("pre.2"))
    orch, run, task, item = _governed_setup(gates=(gate,), run_id="run.byp.16")
    evidence = PrerequisiteEvidence(PrerequisiteRecordRef("prr.2"), gate.ref, run.ref,
                                    item.ref, PrerequisiteRef("pre.2"),
                                    GateOutcome.SATISFIED_WITH_OPEN_ITEMS,
                                    StorageRecordRef("sr.2"))
    orch.record_prerequisite(run, item, gate.ref, evidence)
    _refused_any(lambda: orch.complete(run, TerminalOutcome.COMPLETED))
    return "GOVERNED_PREREQUISITE with open items", (
        "posture %s; COMPLETED refused" % run.posture.value)


def bypass_fabricated_scope_authorisation():
    gate = GateRequirement(GateRequirementRef("gate.tr"), GateKind.DECISION,
                           decision_right=DecisionRightRef("dr.tr"))
    registry = InMemoryMechanismRegistry()
    orch, run, task, item = _governed_setup(
        gates=(gate,), rights={"dr.tr": (HumanAuthorityRef("h"), GateOutcome.SATISFIED)},
        run_id="run.byp.17")
    orch.mechanisms = registry
    target = ScopeBinding(ScopeRef("project.zephyr"), frozenset({"INTERNAL"}), "EU")
    fabricated = ScopeTransferAuthorisation(
        ScopeTransferRef("st.fab"), "v9", run.ref, run.scope, target, item.ref, gate.ref,
        DecisionRightRef("dr.tr"), HumanAuthorityRef("h"), DecisionRecordRef("dr.never"))
    return "fabricated scope authorisation", _refused_any(
        lambda: orch.transfer_scope(run, run.definition, WorkflowRunRef("run.byp.17a"),
                                    target, fabricated))[:88]


def bypass_bare_scope_mechanism():
    """A bare mechanism identifier is a name, not an approval."""
    orch, run, task, item = _governed_setup(run_id="run.byp.8")
    other = ScopeBinding(ScopeRef("project.zephyr"), frozenset({"INTERNAL"}), "EU")
    return "bare mechanism reference", _refused_any(
        lambda: orch.transfer_scope(run, run.definition, WorkflowRunRef("run.byp.8a"), other,
                                    authorisation=ScopeTransferRef("st.bare")))[:88]


def bypass_fabricated_routing_decision():
    orch, run, task, item = _governed_setup(capability="cap", run_id="run.byp.6")
    fabricated = RoutingDecision(RoutingDecisionRef("rd.fake"), RoutingRequestRef("rr.fake"),
                                 run.ref, item.ref, RouterOutcome.ELIGIBLE_CANDIDATE,
                                 RouterRef("router.phase9"), model=ModelRef("model.chosen"),
                                 model_profile=ModelProfileRef("profile.chosen"))
    public = hasattr(orch, "record_routing_decision")
    return "fabricated Routing Decision", (
        "no public recording path: %s; invocation refused: %s"
        % (not public, _refused_any(lambda: orch.invoke_model(run, item, fabricated))[:46]))


def bypass_router_mismatch():
    orch, run, task, item = _governed_setup(capability="cap", run_id="run.byp.18")
    def impostor(request):
        return RoutingDecision(RoutingDecisionRef("rd.imp"), request.ref, run.ref, item.ref,
                               RouterOutcome.ELIGIBLE_CANDIDATE, RouterRef("router.other"),
                               ModelRef("m"), ModelProfileRef("p"))
    orch.router.route = impostor
    return "Router identity mismatch", _refused_any(
        lambda: orch.route(run, item, "policy@1"))[:88]


def bypass_foreign_model_result():
    orch, run, task, item = _governed_setup(
        capability="cap", eligible={"cap": (ModelRef("m"), ModelProfileRef("p"))},
        run_id="run.byp.19")
    decision = orch.route(run, item, "policy@1")
    foreign = __import__("domain").ModelResult(
        ModelResultRef("mr.foreign"), WorkflowRunRef("run.elsewhere"), item.ref,
        decision.ref, ModelRef("m"), ModelProfileRef("p"), "text")
    orch.model.execute = lambda request: foreign
    before = len(run.model_results())
    refusal = _refused_any(lambda: orch.invoke_model(run, item, decision))
    return "foreign-lineage Model Result", (
        "%s; nothing recorded: %s" % (refusal[:50], len(run.model_results()) == before))


def bypass_duplicate_record_identity():
    gate = GateRequirement(GateRequirementRef("gate.dup"), GateKind.GOVERNED_PREREQUISITE,
                           prerequisite=PrerequisiteRef("pre.dup"))
    orch, run, task, item = _governed_setup(gates=(gate,), run_id="run.byp.20")
    evidence = PrerequisiteEvidence(PrerequisiteRecordRef("prr.dup"), gate.ref, run.ref,
                                    item.ref, PrerequisiteRef("pre.dup"),
                                    GateOutcome.SATISFIED, StorageRecordRef("sr.dup"))
    orch.record_prerequisite(run, item, gate.ref, evidence)
    return "duplicate record identity", _refused_any(
        lambda: orch.record_prerequisite(run, item, gate.ref, evidence))[:88]


def bypass_evidence_without_retention():
    gate = GateRequirement(GateRequirementRef("gate.ret"), GateKind.GOVERNED_PREREQUISITE,
                           prerequisite=PrerequisiteRef("pre.ret"))
    orch, run, task, item = _governed_setup(gates=(gate,), run_id="run.byp.21")
    evidence = PrerequisiteEvidence(PrerequisiteRecordRef("prr.ret"), gate.ref, run.ref,
                                    item.ref, PrerequisiteRef("pre.ret"),
                                    GateOutcome.SATISFIED, StorageRecordRef("sr.ret"))
    state = orch.satisfy_gate_with(run, item, gate.ref, evidence)
    retained = run.evidence_for(state)
    return "externally supplied evidence retention", (
        "gate %s; evidence retained and reconstructable: %s"
        % (state.outcome.value, retained is evidence))


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
    return "foreign Decision Record", _refused_any(
        lambda: orch.satisfy_gate_with(run, item, gate.ref, forged))[:88]


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
    refusal = _refused_any(lambda: orch.complete(run, TerminalOutcome.COMPLETED))
    return "two decision gates do not collapse", (
        "%d of %d still open; %s" % (open_gates, len(run.gates()), refusal[:50]))


def bypass_review_independence_mismatch():
    gate = GateRequirement(GateRequirementRef("gate.r"), GateKind.REVIEW,
                           review_profile=ReviewProfileRef("rp.ind"),
                           independence_class="INDEPENDENT")
    orch, run, task, item = _governed_setup(
        gates=(gate,), reviews={"rp.ind": (GateOutcome.SATISFIED, HumanAuthorityRef("h"),
                                           "NOT_INDEPENDENT")}, run_id="run.byp.4")
    return "review independence mismatch", _refused_any(
        lambda: orch.run_review_gate(run, item, gate.ref))[:88]


def bypass_review_in_a_human_work_gate():
    human = GateRequirement(GateRequirementRef("gate.hw"), GateKind.HUMAN_WORK,
                            human_work=HumanWorkRef("hw.1"))
    review = GateRequirement(GateRequirementRef("gate.rv"), GateKind.REVIEW,
                             review_profile=ReviewProfileRef("rp.any"),
                             independence_class="INDEPENDENT")
    orch, run, task, item = _governed_setup(
        gates=(human, review),
        reviews={"rp.any": (GateOutcome.SATISFIED, HumanAuthorityRef("h"), "INDEPENDENT")},
        run_id="run.byp.5")
    instance = orch.run_review_gate(run, item, review.ref)
    return "Review Instance in a HUMAN_WORK gate", _refused_any(
        lambda: orch.satisfy_gate_with(run, item, human.ref, instance))[:88]


def bypass_retry_class_substitution():
    orch, run, task, item = _governed_setup(retry=RetryClass.NON_RETRYABLE_GOVERNED_ACT,
                                            run_id="run.byp.7")
    orch.retry(run, item)
    dispatched = "retry:dispatched" in orch.log.kinds()
    return "retry-class substitution", (
        "work item class %s, retried automatically: %s" % (item.retry_class.value, dispatched))


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
    for probe in (bypass_undeclared_task, bypass_malformed_enum_field,
                  bypass_malformed_structured_field,
                  bypass_repeated_activation_displaces_gates,
                  bypass_progression_after_missing_authority,
                  bypass_continuing_decision_without_record,
                  bypass_partial_mutation_on_rejected_evidence,
                  bypass_open_items_on_human_work, bypass_open_items_on_prerequisite,
                  bypass_fabricated_scope_authorisation, bypass_foreign_decision_record,
                  bypass_two_gates_of_one_kind, bypass_review_independence_mismatch,
                  bypass_review_in_a_human_work_gate, bypass_fabricated_routing_decision,
                  bypass_router_mismatch, bypass_foreign_model_result,
                  bypass_duplicate_record_identity, bypass_evidence_without_retention,
                  bypass_bare_scope_mechanism,
                  bypass_retry_class_substitution, bypass_direct_state_mutation,
                  bypass_repeated_decision_overwrite):
        name, detail = probe()
        print("  REFUSED  %-38s %s" % (name, detail))
    return 0


if __name__ == "__main__":
    sys.exit(main())
