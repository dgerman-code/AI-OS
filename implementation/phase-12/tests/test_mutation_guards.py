"""Phase 12 MVP — committed controlled weakenings of the load-bearing governance guards.

Status: PROPOSED. Run with the rest of the suite:

    python3 -m unittest discover -s implementation/phase-12/tests -v

A test that asserts a guard raises proves the guard *fires*. It does not prove the guard is
what makes the behaviour safe: a second, redundant mechanism can hold the line while the named
guard does nothing. This module answers that question by removing each guard and re-running a
scenario that must then break.

Nothing on disk is edited. Each weakening is applied to the module **source** in memory and
executed into a fresh set of modules, so the running implementation is never mutated and the
runner is reproducible from a clean checkout.

Each entry is honest about its own strength:

* `DETECTED`   - removing the guard changes observable governed behaviour, and the scenario
                 catches it;
* `REDUNDANT`  - removing the guard changes nothing observable, because another mechanism
                 independently preserves the behaviour. Recorded, never presented as a pass.
"""

import os
import sys
import types
import unittest
from contextlib import contextmanager

PACKAGE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PACKAGE)

MODULE_ORDER = ("domain", "adapters", "orchestrator")


def _source(name):
    with open(os.path.join(PACKAGE, "%s.py" % name), encoding="utf-8") as handle:
        return handle.read()


@contextmanager
def implementation(mutations=()):
    """A freshly executed copy of the implementation, optionally with guards removed.

    `mutations` is a sequence of `(module, old, new)`. A weakening whose text is not found is
    an error rather than a silent no-op: a mutation runner that quietly matches nothing proves
    exactly as much as no runner at all."""
    sources = {name: _source(name) for name in MODULE_ORDER}
    for module_name, old, new in mutations:
        if old not in sources[module_name]:
            raise AssertionError("weakening text not found in %s.py: %r" % (module_name, old))
        sources[module_name] = sources[module_name].replace(old, new, 1)
    saved = {name: sys.modules.get(name) for name in MODULE_ORDER}
    built = {}
    try:
        for name in MODULE_ORDER:
            module = types.ModuleType(name)
            module.__file__ = os.path.join(PACKAGE, "%s.py" % name)
            sys.modules[name] = module
            exec(compile(sources[name], module.__file__, "exec"), module.__dict__)
            built[name] = module
        yield types.SimpleNamespace(**built)
    finally:
        for name, previous in saved.items():
            if previous is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = previous


# ===========================================================================================
# Scenario helpers, written against whichever implementation copy is passed in
# ===========================================================================================


def scope(env):
    return env.domain.ScopeBinding(env.domain.ScopeRef("scope.m"), frozenset({"INTERNAL"}),
                                   "EU")


def orchestrator(env, rights=None, reviews=None, eligible=None, mechanisms=None):
    d, a = env.domain, env.adapters
    return env.orchestrator.Orchestrator(
        a.InMemoryRouter(d.RouterRef("router.m"), eligible=eligible or {}),
        a.InMemoryReviewerDesk(reviews or {}), a.InMemoryDecisionDesk(rights or {}),
        a.StubModel(), mechanisms=mechanisms)


def task(env, gates=(), retry=None, capability=""):
    d = env.domain
    return d.Task(d.TaskRef("task.m"), "M", d.RoleRef("role.m"),
                  retry or d.RetryClass.SAFE_AUTOMATIC_RETRY, gates=gates,
                  capability=capability)


def started(env, orch, declared, run_id="run.m"):
    d = env.domain
    definition = d.WorkflowDefinition(d.WorkflowRef("wf.m"), "v1", (declared,), scope(env))
    run = orch.create_run(definition, d.WorkflowRunRef(run_id))
    return run, orch.activate_stage(run, declared.ref)


def decision_gate(env, ref="gate.m", right="dr.m"):
    d = env.domain
    return d.GateRequirement(d.GateRequirementRef(ref), d.GateKind.DECISION,
                             decision_right=d.DecisionRightRef(right))


def prerequisite_gate(env, ref="gate.p", prerequisite="pre.m"):
    d = env.domain
    return d.GateRequirement(d.GateRequirementRef(ref), d.GateKind.GOVERNED_PREREQUISITE,
                             prerequisite=d.PrerequisiteRef(prerequisite))


def snapshot(run, orch):
    return (run.axes(),
            tuple((g.ref.id, g.outcome, g.satisfied_by) for g in run.gates()),
            tuple(r.ref for r in run.decision_records()),
            tuple(r.ref for r in run.prerequisite_records()),
            tuple(r.ref for r in run.model_results()), len(orch.log))


def halted(env, run_id="run.m"):
    """A run stopped by a missing Decision Right: ESCALATED / AUTHORITY_ABSENT."""
    gate = decision_gate(env, "gate.absent", "dr.absent")
    orch = orchestrator(env, rights={})
    run, item = started(env, orch, task(env, gates=(gate,)), run_id)
    orch.run_decision_gate(run, item, gate.ref)
    assert run.posture is env.domain.GovernancePosture.AUTHORITY_ABSENT
    return orch, run, item


def refuses(call):
    """True when `call` is refused by a governance error rather than succeeding."""
    try:
        call()
    except Exception as exc:                      # noqa: BLE001 - any refusal counts
        if isinstance(exc, AssertionError):
            raise
        return True
    return False


# ===========================================================================================
# The scenarios. Each must pass against the pristine implementation and fail when its guard
# is removed. Raising AssertionError is how a scenario reports that the guard is gone.
# ===========================================================================================


def halted_run_refuses_every_api(env):
    orch, run, item = halted(env)
    apis = {
        "activate a stage": lambda: orch.activate_stage(run, env.domain.TaskRef("task.m")),
        "assign": lambda: orch.assign(run, item, env.domain.RoleRef("role.m")),
        "request routing": lambda: orch.request_routing(run, item, "policy@1"),
        "route": lambda: orch.route(run, item, "policy@1"),
        "record an intervention": lambda: orch.record_intervention(
            run, env.domain.HumanInterventionRecord(
                env.domain.InterventionRef("iv.x"), run.ref,
                env.domain.HumanAuthorityRef("h"), "note", "while halted")),
    }
    for name, call in apis.items():
        if not refuses(call):
            raise AssertionError("a halted run permitted: %s" % name)


def halted_run_refuses_retry(env):
    orch, run, item = halted(env)
    if not refuses(lambda: orch.retry(run, item)):
        raise AssertionError("a halted run dispatched a retry")


def halted_run_refuses_gate_work(env):
    orch, run, item = halted(env)
    gate = prerequisite_gate(env)
    evidence = env.domain.PrerequisiteEvidence(
        env.domain.PrerequisiteRecordRef("prr.x"), gate.ref, run.ref, item.ref,
        env.domain.PrerequisiteRef("pre.m"), env.domain.GateOutcome.SATISFIED,
        env.domain.StorageRecordRef("sr"))
    for name, call in (("satisfy a gate",
                        lambda: orch.satisfy_gate_with(run, item, gate.ref, evidence)),
                       ("record a prerequisite",
                        lambda: orch.record_prerequisite(run, item, gate.ref, evidence)),
                       ("run a decision gate",
                        lambda: orch.run_decision_gate(run, item,
                                                       env.domain.GateRequirementRef(
                                                           "gate.absent")))):
        if not refuses(call):
            raise AssertionError("a halted run permitted: %s" % name)


def duplicate_evidence_leaves_no_partial_mutation(env):
    d = env.domain
    gate = prerequisite_gate(env, "gate.dup", "pre.dup")
    orch = orchestrator(env)
    run, item = started(env, orch, task(env, gates=(gate,)))
    evidence = d.PrerequisiteEvidence(
        d.PrerequisiteRecordRef("prr.dup"), gate.ref, run.ref, item.ref,
        d.PrerequisiteRef("pre.dup"), d.GateOutcome.SATISFIED, d.StorageRecordRef("sr"))
    orch.record_prerequisite(run, item, gate.ref, evidence)
    before = snapshot(run, orch)
    if not refuses(lambda: orch.record_prerequisite(run, item, gate.ref, evidence)):
        raise AssertionError("a duplicate governed record identity was admitted")
    if snapshot(run, orch) != before:
        raise AssertionError("a refused append left a partial mutation behind")


def duplicate_review_leaves_no_partial_mutation(env):
    """A review moves the run to WAITING before its evidence is appended.

    That ordering is where an append that can still refuse becomes a partial mutation, so this
    is the scenario the preflight exists for."""
    d = env.domain
    gate = d.GateRequirement(d.GateRequirementRef("gate.rv"), d.GateKind.REVIEW,
                             review_profile=d.ReviewProfileRef("rp.m"),
                             independence_class="INDEPENDENT")
    orch = orchestrator(env, reviews={"rp.m": (d.GateOutcome.SATISFIED,
                                               d.HumanAuthorityRef("h"), "INDEPENDENT")})
    run, item = started(env, orch, task(env, gates=(gate,)))
    first = orch.run_review_gate(run, item, gate.ref)
    orch.reviewers.review = lambda request: first     # the same identity, a second time
    before = snapshot(run, orch)
    if not refuses(lambda: orch.run_review_gate(run, item, gate.ref)):
        raise AssertionError("a duplicate Review Instance identity was admitted")
    if snapshot(run, orch) != before:
        raise AssertionError("a refused review left a partial mutation behind")


def duplicate_model_result_leaves_no_partial_mutation(env):
    d = env.domain
    orch = orchestrator(env, eligible={"cap": (d.ModelRef("m"), d.ModelProfileRef("p"))})
    run, item = started(env, orch, task(env, capability="cap"))
    decision = orch.route(run, item, "policy@1")
    first = orch.invoke_model(run, item, decision)
    orch.model.execute = lambda request: first        # the same identity, a second time
    before = snapshot(run, orch)
    if not refuses(lambda: orch.invoke_model(run, item, decision)):
        raise AssertionError("a duplicate Model Result identity was admitted")
    if snapshot(run, orch) != before:
        raise AssertionError("a refused Model Result left a partial mutation behind")


def fabricated_routing_decision_is_refused(env):
    d = env.domain
    orch = orchestrator(env, eligible={"cap": (d.ModelRef("m"), d.ModelProfileRef("p"))})
    run, item = started(env, orch, task(env, capability="cap"))
    request = orch.request_routing(run, item, "policy@1")
    fabricated = d.RoutingDecision(
        d.RoutingDecisionRef("rd.fake"), request.ref, run.ref, item.ref,
        d.RouterOutcome.ELIGIBLE_CANDIDATE, d.RouterRef("router.m"),
        d.ModelRef("model.chosen"), d.ModelProfileRef("profile.chosen"))
    if not refuses(lambda: orch.invoke_model(run, item, fabricated)):
        raise AssertionError("a fabricated Routing Decision reached model invocation")
    if any(recorded.ref == fabricated.ref for recorded in run.routing_decisions()):
        raise AssertionError("a fabricated Routing Decision entered governed history")


def model_profile_lineage_is_verified(env):
    d = env.domain
    orch = orchestrator(env, eligible={"cap": (d.ModelRef("m"), d.ModelProfileRef("p"))})
    run, item = started(env, orch, task(env, capability="cap"))
    decision = orch.route(run, item, "policy@1")
    orch.model.execute = lambda request: d.ModelResult(
        d.ModelResultRef("mr.wrong"), run.ref, item.ref, decision.ref, decision.model,
        d.ModelProfileRef("profile.somethingelse"), "text")
    before = snapshot(run, orch)
    if not refuses(lambda: orch.invoke_model(run, item, decision)):
        raise AssertionError("a result under a different Model Profile was accepted")
    if snapshot(run, orch) != before:
        raise AssertionError("a refused Model Result left a partial mutation behind")


def _crossing_fixture(env, registered_right="dr.tr", registered_act="scope_transfer"):
    d = env.domain
    target = d.ScopeBinding(d.ScopeRef("scope.other"), frozenset({"INTERNAL"}), "EU")
    registry = env.adapters.InMemoryMechanismRegistry()
    registry.register(d.ScopeTransferRef("st.1"), "v2", scope(env), target,
                      d.DecisionRightRef(registered_right), registered_act)
    gate = decision_gate(env, "gate.tr", "dr.tr")
    orch = orchestrator(env, rights={"dr.tr": (d.HumanAuthorityRef("h"),
                                               d.GateOutcome.SATISFIED)},
                        mechanisms=registry)
    run, item = started(env, orch, task(env, gates=(gate,)), "run.tr")
    _outcome, record = orch.run_decision_gate(run, item, gate.ref)
    return orch, run, item, gate, record, target


def _authorisation(env, run, item, gate, record, target, **overrides):
    d = env.domain
    fields = dict(mechanism=d.ScopeTransferRef("st.1"), mechanism_version="v2",
                  source_run=run.ref, source_scope=run.scope, target_scope=target,
                  work_item=item.ref, requirement=gate.ref,
                  decision_right=d.DecisionRightRef("dr.tr"),
                  authorised_act="scope_transfer", authorised_by=record.decided_by,
                  decision_record=record.ref)
    fields.update(overrides)
    return d.ScopeTransferAuthorisation(**fields)


def crossing_needs_the_registered_decision_right(env):
    """A mechanism registered for one Right does not serve another."""
    orch, run, item, gate, record, target = _crossing_fixture(
        env, registered_right="dr.something-else")
    authorisation = _authorisation(env, run, item, gate, record, target)
    if not refuses(lambda: orch.transfer_scope(run, run.definition,
                                               env.domain.WorkflowRunRef("run.x"), target,
                                               authorisation)):
        raise AssertionError("a crossing was approved under an unregistered Decision Right")


def crossing_needs_the_registered_act(env):
    """A mechanism registered for one act does not serve another."""
    orch, run, item, gate, record, target = _crossing_fixture(
        env, registered_act="evidence_export")
    authorisation = _authorisation(env, run, item, gate, record, target)
    if not refuses(lambda: orch.transfer_scope(run, run.definition,
                                               env.domain.WorkflowRunRef("run.x"), target,
                                               authorisation)):
        raise AssertionError("a crossing was approved for an act it is not registered for")


def a_healthy_crossing_still_works(env):
    """The control for the two above: the fully corroborated crossing is permitted."""
    orch, run, item, gate, record, target = _crossing_fixture(env)
    transferred = orch.transfer_scope(run, run.definition,
                                      env.domain.WorkflowRunRef("run.x"), target,
                                      _authorisation(env, run, item, gate, record, target))
    if transferred.scope != target or run.scope == target:
        raise AssertionError("the approved crossing did not produce a new bound execution")


# ===========================================================================================
# The weakenings themselves
# ===========================================================================================

#: (name, mutations, scenario, expectation). `expectation` is "DETECTED" where the scenario
#: must break, or "REDUNDANT" where an independent mechanism preserves the behaviour and the
#: honest answer is that this particular removal changes nothing observable.
WEAKENINGS = [
    ("the common halted-run guard is removed",
     [("orchestrator",
       "        if state.phase in HALTED_PHASES or state.posture is "
       "GovernancePosture.AUTHORITY_ABSENT:",
       "        if False:")],
     halted_run_refuses_every_api, "DETECTED"),

    ("a halted run may retry",
     [("orchestrator",
       '        self._require_progressible(run, "retry")',
       "        pass")],
     halted_run_refuses_retry, "DETECTED"),

    ("a halted run may work its gates",
     [("orchestrator",
       '        self._require_progressible(run, "prerequisite progression")',
       "        pass"),
      ("orchestrator",
       '        self._require_progressible(run, "gate satisfaction")',
       "        pass"),
      ("orchestrator",
       '        self._require_progressible(run, "decision progression")',
       "        pass")],
     halted_run_refuses_gate_work, "DETECTED"),

    ("evidence append is no longer preflighted before the phase moves",
     [("orchestrator",
       "        if evidence is not None:\n"
       "            self._store(run, self.EVIDENCE_STORE[instance.kind]).validate_add(evidence)",
       "        if False:\n"
       "            self._store(run, self.EVIDENCE_STORE[instance.kind]).validate_add(evidence)")],
     duplicate_review_leaves_no_partial_mutation, "DETECTED"),

    ("duplicate governed record identities are admitted",
     [("domain",
       "            for existing in records:\n"
       '                if getattr(existing, "ref", None) == identity:',
       "            for existing in ():\n"
       '                if getattr(existing, "ref", None) == identity:')],
     duplicate_evidence_leaves_no_partial_mutation, "DETECTED"),

    ("duplicate governed record identities are admitted (model results)",
     [("domain",
       "            for existing in records:\n"
       '                if getattr(existing, "ref", None) == identity:',
       "            for existing in ():\n"
       '                if getattr(existing, "ref", None) == identity:')],
     duplicate_model_result_leaves_no_partial_mutation, "DETECTED"),

    ("the Model Result identity preflight is removed",
     [("orchestrator",
       '        self._store(run, "model_results").validate_add(result)',
       "        pass")],
     duplicate_model_result_leaves_no_partial_mutation, "REDUNDANT"),

    ("a caller-injected Routing Decision is accepted",
     [("orchestrator",
       '        if not self._store(run, "routing").contains(decision):',
       "        if False:")],
     fabricated_routing_decision_is_refused, "DETECTED"),

    ("the Model Profile lineage is no longer verified",
     [("orchestrator",
       "                or result.model_profile != decision.model_profile):",
       "                or False):")],
     model_profile_lineage_is_verified, "DETECTED"),

    ("the exact Decision Right is dropped from mechanism approval",
     [("adapters",
       "        return declared is not None and declared == (source, target, decision_right,\n"
       "                                                     authorised_act)",
       "        return declared is not None and declared[:2] == (source, target) \\\n"
       "            and declared[3] == authorised_act")],
     crossing_needs_the_registered_decision_right, "DETECTED"),

    ("the authorised act is dropped from mechanism approval",
     [("adapters",
       "        return declared is not None and declared == (source, target, decision_right,\n"
       "                                                     authorised_act)",
       "        return declared is not None and declared[:3] == (source, target,\n"
       "                                                         decision_right)")],
     crossing_needs_the_registered_act, "DETECTED"),

    ("the phase plan is no longer preflighted before the gate commits",
     [("orchestrator",
       "        self._preflight_phases(run, self._gate_phase_plan(run, outcome, wait_reason))",
       "        pass")],
     duplicate_evidence_leaves_no_partial_mutation, "REDUNDANT"),
]


class TestControlledWeakenings(unittest.TestCase):
    """Every named guard is removed in turn, and the scenario it protects is re-run."""

    def test_every_scenario_holds_against_the_pristine_implementation(self):
        """A scenario that fails on healthy code would make every detection meaningless."""
        with implementation() as env:
            for name, _mutations, scenario, _expectation in WEAKENINGS:
                try:
                    scenario(env)
                except AssertionError as exc:
                    self.fail("%s: the scenario fails on the pristine implementation: %s"
                              % (name, exc))

    def test_the_healthy_crossing_control_passes(self):
        with implementation() as env:
            a_healthy_crossing_still_works(env)

    def test_each_weakening_behaves_as_classified(self):
        misclassified = []
        for name, mutations, scenario, expectation in WEAKENINGS:
            with implementation(mutations) as env:
                try:
                    scenario(env)
                    detected = False
                except AssertionError:
                    detected = True
                except Exception as exc:               # noqa: BLE001
                    # An unrelated explosion is not a detection; it is a broken weakening.
                    misclassified.append("%s raised %s" % (name, type(exc).__name__))
                    continue
            if detected and expectation != "DETECTED":
                misclassified.append("%s was detected but is classified %s"
                                     % (name, expectation))
            if not detected and expectation == "DETECTED":
                misclassified.append("%s is classified DETECTED but changed nothing" % name)
        self.assertEqual(misclassified, [])

    def test_the_classification_is_mostly_detection(self):
        """Honesty check: most weakenings must actually bite, or the harness proves little."""
        detected = [w for w in WEAKENINGS if w[3] == "DETECTED"]
        self.assertGreaterEqual(len(detected), 10)
        self.assertGreaterEqual(len(detected) / float(len(WEAKENINGS)), 0.8)

    def test_a_weakening_that_matches_nothing_is_an_error(self):
        """The runner may not quietly no-op: an unmatched weakening fails loudly."""
        with self.assertRaises(AssertionError):
            with implementation([("domain", "text that is not in the module", "x")]):
                pass


if __name__ == "__main__":
    unittest.main(verbosity=2)
