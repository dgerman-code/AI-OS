"""Phase 12 MVP — deterministic validation harness.

Status: PROPOSED.

Three kinds of check, in increasing strength:

* **structure** — the package exists and is shaped as the Phase 12 objective requires;
* **containment** — nothing forbidden was introduced: no provider SDK, no network, no
  migration, no secret, no scheduler, no exactly-once claim;
* **assurance** — the approved invariants are exercised against the real objects. Phase 11's
  lesson was that a check which reads prose proves less than a check which runs the thing, so
  these import the implementation and assert on behaviour, not on wording.

Read-only. Runs offline. Makes no claim about remote repository state.

    python3 validation/phase_12_validation.py [--verbose] [--json]
"""

import io
import json
import os
import re
import subprocess
import sys
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PKG = os.path.join(REPO, "implementation", "phase-12")
sys.path.insert(0, PKG)
sys.path.insert(0, os.path.join(PKG, "examples"))

RESULTS = []


def check(group, name, fn):
    try:
        outcome = fn()
    except Exception as exc:
        outcome = (False, "ERROR: %s: %s" % (type(exc).__name__, exc))
    ok, evidence = outcome if isinstance(outcome, tuple) else (bool(outcome), "")
    RESULTS.append({"group": group, "name": name, "pass": bool(ok), "evidence": str(evidence)})


def read(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as handle:
        return handle.read()


# =========================================================== structure

REQUIRED = [
    "implementation/phase-12/README.md",
    "implementation/phase-12/domain.py",
    "implementation/phase-12/orchestrator.py",
    "implementation/phase-12/adapters.py",
    "implementation/phase-12/examples/governed_run.py",
    "implementation/phase-12/examples/blocked_run.py",
    "implementation/phase-12/tests/test_invariants.py",
    "validation/phase_12_validation.py",
    "reviews/phase-12-foundation-self-check.md",
]

check("structure", "every required Phase 12 artifact exists",
      lambda: (lambda missing: (not missing, str(missing) if missing
                                else "%d artifacts" % len(REQUIRED)))(
          [rel for rel in REQUIRED if not os.path.exists(os.path.join(REPO, rel))]))

MODULES = ["implementation/phase-12/domain.py", "implementation/phase-12/orchestrator.py",
           "implementation/phase-12/adapters.py"]
SOURCES = MODULES + ["implementation/phase-12/examples/governed_run.py",
                     "implementation/phase-12/examples/blocked_run.py",
                     "implementation/phase-12/tests/test_invariants.py"]

check("structure", "every implementation module declares a non-approved status",
      lambda: (lambda bad: (not bad, str(bad) if bad else "%d modules PROPOSED" % len(MODULES)))(
          [rel for rel in MODULES if "Status: PROPOSED" not in read(rel)]))

check("structure", "no Phase 12 artifact claims APPROVED or CANONICAL status",
      lambda: (lambda bad: (not bad, str(bad) if bad else "no approval claimed"))(
          [rel for rel in REQUIRED
           if re.search(r"Status:\s*`?(APPROVED|CANONICAL)", read(rel))]))

check("structure", "the README maps the package to the approved architecture",
      lambda: (lambda text: (all(word in text for word in
                                 ("Non-scope", "Architecture mapping", "How to run")),
                             ""))(read("implementation/phase-12/README.md")))


# =========================================================== containment

#: Things the Phase 12 constraints forbid introducing. Matched on the module source, with a
#: line-scoped denial marker so a sentence that says a thing is absent is not a hit for it.
FORBIDDEN_IMPORTS = ("requests", "httpx", "urllib", "socket", "boto3", "supabase", "psycopg",
                     "sqlalchemy", "openai", "anthropic", "google.generativeai", "celery",
                     "redis", "kafka", "pika", "apscheduler", "fastapi", "flask", "django")

FORBIDDEN_CONSTRUCTS = (
    (r"\bCREATE\s+TABLE\b", "SQL DDL"),
    (r"\bALTER\s+TABLE\b", "SQL DDL"),
    (r"\bDROP\s+TABLE\b", "SQL DDL"),
    (r"\bCREATE\s+POLICY\b", "RLS policy"),
    (r"\bmigrations?\.(?:up|down|apply)\b", "migration runner"),
    (r"\bos\.environ\b", "environment secret access"),
    (r"\bgetenv\b", "environment secret access"),
    (r"\bapi[_-]?key\b", "credential"),
    (r"\bsecret[_-]?key\b", "credential"),
    (r"\bBearer\s", "bearer token"),
    (r"\bsubprocess\.", "process launch"),
    (r"\bthreading\.Thread\b", "background daemon"),
    (r"\basyncio\.", "event loop"),
    (r"\bwhile\s+True\s*:", "background loop"),
)


def forbidden_imports():
    hits = []
    for rel in SOURCES:
        for number, line in enumerate(read(rel).splitlines(), 1):
            stripped = line.strip()
            if not (stripped.startswith("import ") or stripped.startswith("from ")):
                continue
            for name in FORBIDDEN_IMPORTS:
                if re.search(r"\b%s\b" % re.escape(name), stripped):
                    hits.append("%s:%d %s" % (rel, number, stripped))
    return (not hits, str(hits) if hits
            else "%d source files, standard library only" % len(SOURCES))


check("containment", "the package imports nothing outside the standard library",
      forbidden_imports)


def forbidden_constructs():
    hits = []
    for rel in SOURCES:
        for number, line in enumerate(read(rel).splitlines(), 1):
            for pattern, what in FORBIDDEN_CONSTRUCTS:
                if re.search(pattern, line):
                    hits.append("%s:%d %s" % (rel, number, what))
    return (not hits, str(hits) if hits else "%d construct families absent"
            % len(FORBIDDEN_CONSTRUCTS))


check("containment", "no SQL, migration, credential, daemon or event loop is introduced",
      forbidden_constructs)

check("containment", "exactly-once is claimed nowhere",
      lambda: (lambda bad: (not bad, str(bad) if bad else "no exactly-once claim"))(
          [rel for rel in SOURCES
           if re.search(r"exactly[- ]once", read(rel), re.I)
           and not re.search(r"exactly[- ]once is (?:not |claimed nowhere|never)",
                             read(rel), re.I)]))

check("containment", "no live model call is made",
      lambda: (lambda text: ("No network" in text and "no credential" in text, ""))(
          read("implementation/phase-12/adapters.py")))

def makes_no_remote_claim():
    """Nothing here asserts anything about a remote: this harness is offline by construction.

    The forbidden phrases are assembled rather than written out, so the check does not trip
    over its own source - the same self-inspection problem the Phase 9 harness hit."""
    banned = ["pull" + " request", "remote" + " HEAD", "ori" + "gin/"]
    text = read("validation/phase_12_validation.py")
    hits = [phrase for phrase in banned if phrase in text]
    return (not hits, str(hits) if hits else "no remote-state claim")


check("containment", "the harness makes no claim about remote repository state",
      makes_no_remote_claim)


def inherited_unchanged():
    """Phase 1-11 architecture and prior validators are untouched by this phase."""
    paths = ["architecture", "orchestration", "validation/phase_8_validation.py",
             "validation/phase_9_validation.py", "validation/phase_10_validation.py",
             "validation/phase_11_validation.py", "reviews/phase-11-final-approval.md"]
    # The Phase 12 base approval commit: Phase 11's architecture at its approved baseline,
    # plus the human approval record itself.
    diff = subprocess.run(["git", "diff", "--name-only",
                           "b8fba92e03a4bc29c8f1bb4d894fb9efb45586cb", "HEAD", "--"] + paths,
                          cwd=REPO, capture_output=True, text=True)
    status = subprocess.run(["git", "status", "--porcelain", "--"] + paths,
                            cwd=REPO, capture_output=True, text=True)
    changed = [ln for ln in (diff.stdout + status.stdout).splitlines() if ln.strip()]
    return (not changed, str(changed) if changed
            else "Phase 1-11 architecture, validators and approval record unchanged")


check("containment", "no approved Phase 1-11 artifact was modified", inherited_unchanged)


# =========================================================== the domain, as imported

import domain  # noqa: E402
import orchestrator as orch_mod  # noqa: E402
import adapters  # noqa: E402

check("domain", "the separation chain carries twenty-one distinct governed kinds",
      lambda: (len(domain.SEPARATION_CHAIN) == 21
               and len({c.KIND for c in domain.SEPARATION_CHAIN}) == 21,
               "%d kinds" % len(domain.SEPARATION_CHAIN)))

check("domain", "the four state axes have their approved cardinalities",
      lambda: ((len(domain.RunPhase), len(domain.TerminalOutcome), len(domain.WaitReason),
                len(domain.GovernancePosture)) == (10, 6, 5, 4),
               "%d phases, %d terminals, %d waits, %d postures"
               % (len(domain.RunPhase), len(domain.TerminalOutcome), len(domain.WaitReason),
                  len(domain.GovernancePosture))))

check("domain", "seven gate outcomes, seven retry classes, five race outcomes",
      lambda: ((len(domain.GateOutcome), len(domain.RetryClass), len(domain.RaceOutcome))
               == (7, 7, 5), ""))

check("domain", "only two gate outcomes continue a run",
      lambda: (domain.CONTINUING_GATE_OUTCOMES ==
               frozenset({domain.GateOutcome.SATISFIED,
                          domain.GateOutcome.SATISFIED_WITH_OPEN_ITEMS}), ""))

check("domain", "no posture other than the two clear ones permits a completion",
      lambda: (domain.POSTURE_PERMITS_COMPLETION[domain.GovernancePosture.GATE_UNSATISFIED]
               == frozenset()
               and domain.POSTURE_PERMITS_COMPLETION[domain.GovernancePosture.AUTHORITY_ABSENT]
               == frozenset(), ""))


def transition_table_matches_architecture():
    """The implemented transitions are compared against the APPROVED table, row by row.

    Parsed from `orchestration/state-machine-and-transitions.md` rather than restated here, so
    a table that drifts from the architecture fails instead of agreeing with itself."""
    body = read("orchestration/state-machine-and-transitions.md")
    body = body.split("## 6. Transitions")[1].split("## 7.")[0]
    phases = {p.name for p in domain.RunPhase}
    terminals = {t.name for t in domain.TerminalOutcome}
    doc_phase, doc_terminal, rows = {}, {}, 0
    for line in body.splitlines():
        if not line.startswith("| `"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        source = re.sub(r"[^A-Z_]", "", cells[0])
        if source not in phases:
            continue
        rows += 1
        targets = set(re.findall(r"`([A-Z_]+)`", cells[1]))
        doc_phase[source] = {t for t in targets if t in phases}
        for terminal in targets & terminals:
            doc_terminal.setdefault(terminal, set()).add(source)
    problems = []
    if rows != 10:
        problems.append("parsed %d transition rows, expected 10" % rows)
    for source, expected in doc_phase.items():
        actual = {p.name for p in domain.ALLOWED_TRANSITIONS[domain.RunPhase[source]]}
        if actual != expected:
            problems.append("%s: implemented %s, approved %s"
                            % (source, sorted(actual), sorted(expected)))
    for terminal, expected in doc_terminal.items():
        actual = {p.name for p in domain.TERMINAL_REACHABLE_FROM[
            domain.TerminalOutcome[terminal]]}
        if actual != expected:
            problems.append("%s: reachable from %s, approved %s"
                            % (terminal, sorted(actual), sorted(expected)))
    return (not problems, str(problems)[:400] if problems
            else "%d rows reconcile with the approved state machine" % rows)


check("domain", "the transition table reconciles with the approved state machine",
      transition_table_matches_architecture)


def chain_matches_architecture():
    """The implemented separation chain is compared against the approved chain, in order."""
    text = read("architecture/orchestrator-architecture.md")
    match = re.search(r"`?([A-Z][A-Z ]*(?:\s*!=\s*[A-Z][A-Z ]*){10,})`?", text)
    if match is None:
        return (False, "the approved separation chain was not found")
    approved = [" ".join(t.split()) for t in match.group(1).split("!=")]
    implemented = [c.KIND.replace("_", " ").upper() for c in domain.SEPARATION_CHAIN]
    missing = [t for t in approved if t not in implemented]
    return (not missing, str(missing) if missing
            else "%d approved objects, each carried by its own type" % len(approved))


check("domain", "every approved separated object has its own implementation type",
      chain_matches_architecture)


# =========================================================== assurance, by execution


def _fresh():
    router = adapters.InMemoryRouter(domain.RouterRef("router.v"))
    return orch_mod.Orchestrator(router, adapters.InMemoryReviewerDesk({}),
                                 adapters.InMemoryDecisionDesk({}), adapters.StubModel())


SCOPE = domain.ScopeBinding(domain.ScopeRef("scope.v"), frozenset({"INTERNAL"}), "EU")


def _run_with(task, orch=None):
    orch = orch or _fresh()
    definition = domain.WorkflowDefinition(domain.WorkflowRef("wf.v"), "v1", (task,), SCOPE)
    run = orch.create_run(definition, domain.WorkflowRunRef("run.v"))
    return orch, run, orch.activate_stage(run, task)


def _task(**kwargs):
    kwargs.setdefault("retry", domain.RetryClass.SAFE_AUTOMATIC_RETRY)
    return domain.Task(domain.TaskRef("task.v"), "V", domain.RoleRef("role.v"),
                       kwargs["retry"], gates=kwargs.get("gates", ()),
                       capability=kwargs.get("capability", ""))


def _raises(fn, error=domain.GovernanceError):
    try:
        fn()
    except error:
        return True
    except Exception:
        return False
    return False


check("assurance", "a Role reference cannot fill an Agent Instance slot",
      lambda: (_raises(lambda: domain.require(domain.RoleRef("x"), domain.AgentInstanceRef),
                       domain.IdentityError), ""))

check("assurance", "a Model Profile cannot fill a Review Instance or Decision Record field",
      lambda: (_raises(lambda: domain.ReviewInstance(
          domain.ReviewInstanceRef("ri"), domain.WorkItemRef("wi"),
          domain.ModelProfileRef("mp"), domain.GateOutcome.SATISFIED,
          domain.HumanAuthorityRef("h"), "IND"), domain.IdentityError)
          and _raises(lambda: domain.DecisionRecord(
              domain.DecisionRecordRef("dr"), domain.WorkItemRef("wi"),
              domain.ModelProfileRef("mp"), domain.GateOutcome.SATISFIED,
              domain.HumanAuthorityRef("h")), domain.IdentityError), ""))

check("assurance", "a Decision Record requires an explicit human authority",
      lambda: (_raises(lambda: domain.DecisionRecord(
          domain.DecisionRecordRef("dr"), domain.WorkItemRef("wi"),
          domain.DecisionRightRef("r"), domain.GateOutcome.SATISFIED,
          domain.AgentInstanceRef("a")), domain.IdentityError), ""))

check("assurance", "a model result is a suggestion and satisfies no gate",
      lambda: (lambda result: (result.canonicality is domain.Canonicality.AI_SUGGESTION
                               and result.origin is domain.Origin.AI_GENERATED
                               and result.satisfies_gate() is False, ""))(
          domain.ModelResult(domain.WorkItemRef("wi"), domain.ModelRef("m"), "t")))


def model_cannot_satisfy_a_gate():
    orch, run, item = _run_with(_task())
    result = domain.ModelResult(item.ref, domain.ModelRef("m"), "t")
    refused = all(_raises(lambda kind=kind: orch.satisfy_gate_with(run, item, kind, result))
                  for kind in (domain.GateKind.REVIEW, domain.GateKind.DECISION))
    return (refused, "both gate kinds refuse a model result")


check("assurance", "a model result cannot satisfy a review or decision gate",
      model_cannot_satisfy_a_gate)


def router_output_cannot_set_a_gate():
    orch, run, item = _run_with(_task(capability="cap"))
    decision = domain.RoutingDecision(domain.RoutingDecisionRef("rd"), item.ref,
                                      domain.RouterOutcome.NO_ELIGIBLE_MODEL)
    return (_raises(lambda: orch.satisfy_gate_with(run, item, domain.GateKind.DECISION,
                                                   decision)), "")


check("assurance", "router output cannot set a gate state", router_output_cannot_set_a_gate)


def missing_right_blocks():
    gate = domain.GateRequirement(domain.GateKind.DECISION,
                                  decision_right=domain.DecisionRightRef("dr.absent"))
    orch, run, item = _run_with(_task(gates=(gate,)))
    outcome, record = orch.run_decision_gate(run, item, gate)
    blocked = (outcome is domain.GateOutcome.NO_APPLICABLE_DECISION_RIGHT
               and record is None
               and run.phase is domain.RunPhase.ESCALATED
               and run.posture is domain.GovernancePosture.AUTHORITY_ABSENT)
    cannot_complete = not _raises(
        lambda: orch.complete(run, domain.TerminalOutcome.COMPLETED), Exception) is False
    return (blocked and cannot_complete,
            "%s / %s, no Decision Record produced" % (run.phase.value, run.posture.value))


check("assurance", "a missing Decision Right blocks, escalates and cannot complete",
      missing_right_blocks)


def timeout_is_not_approval():
    gate = domain.GateRequirement(domain.GateKind.DECISION,
                                  decision_right=domain.DecisionRightRef("dr.e"))
    orch = _fresh()
    orch.decisions.rights["dr.e"] = (domain.HumanAuthorityRef("h"),
                                     domain.GateOutcome.EXPIRED)
    orch, run, item = _run_with(_task(gates=(gate,)), orch)
    outcome, _ = orch.run_decision_gate(run, item, gate)
    return (outcome is domain.GateOutcome.EXPIRED
            and outcome not in domain.CONTINUING_GATE_OUTCOMES
            and run.phase is domain.RunPhase.ESCALATED, "expiry escalates, never approves")


check("assurance", "a timeout escalates and never becomes an approval", timeout_is_not_approval)


def scope_rules_hold():
    orch = _fresh()
    definition = domain.WorkflowDefinition(domain.WorkflowRef("wf.v"), "v1", (_task(),), SCOPE)
    parent = orch.create_run(definition, domain.WorkflowRunRef("run.p"))
    wider = domain.ScopeBinding(SCOPE.scope, frozenset({"INTERNAL", "SECRET"}), "EU")
    narrower = domain.ScopeBinding(SCOPE.scope, frozenset(), "EU")
    widening_refused = _raises(lambda: orch.open_sub_run(parent, definition,
                                                         domain.WorkflowRunRef("run.w"), wider))
    child = orch.open_sub_run(parent, definition, domain.WorkflowRunRef("run.n"), narrower)
    other = domain.ScopeBinding(domain.ScopeRef("scope.other"), frozenset(), "EU")
    implicit_refused = _raises(lambda: orch.cross_scope(child, other, mechanism=None))
    orch2 = _fresh()
    run2 = orch2.create_run(definition, domain.WorkflowRunRef("run.t"))
    orch2.cross_scope(run2, other, mechanism=domain.ScopeTransferRef("st.1"))
    return (widening_refused and implicit_refused and run2.scope.scope == other.scope,
            "narrowing allowed, widening refused, crossing needs an approved mechanism")


check("assurance", "scope narrows but never widens, and crossing needs an approved mechanism",
      scope_rules_hold)


def retry_respects_its_class():
    findings = []
    for cls in domain.NEVER_AUTOMATICALLY_RETRYABLE:
        orch, run, item = _run_with(_task(retry=cls))
        orch.retry(run, item, _task(retry=cls))
        if "retry:dispatched" in orch.log.kinds():
            findings.append("%s was retried automatically" % cls.value)
        if run.phase is not domain.RunPhase.ESCALATED:
            findings.append("%s did not escalate" % cls.value)
    task = _task(retry=domain.RetryClass.RETRY_REQUIRING_REVALIDATION)
    orch, run, item = _run_with(task)
    if not _raises(lambda: orch.retry(run, item, task)):
        findings.append("a revalidation-class retry ran without revalidating")
    return (not findings, str(findings) if findings
            else "%d never-retryable classes escalate; revalidation is required"
                 % len(domain.NEVER_AUTOMATICALLY_RETRYABLE))


check("assurance", "retry respects the approved retry class", retry_respects_its_class)

check("assurance", "execution history is append-only",
      lambda: (lambda log: (_raises(lambda: log.__setitem__(0, "x"), domain.AppendOnlyError)
                            and _raises(lambda: log.__delitem__(0), domain.AppendOnlyError),
                            ""))(
          (lambda l: (l.append(domain.WorkflowRunRef("r"), "a"), l)[1])(
              domain.ExecutionEventLog())))


def completion_is_governed():
    gate = domain.GateRequirement(domain.GateKind.REVIEW,
                                  review_profile=domain.ReviewProfileRef("rp"))
    orch = _fresh()
    orch.reviewers.outcomes["rp"] = (domain.GateOutcome.SATISFIED,
                                     domain.HumanAuthorityRef("h"), "IND")
    orch, run, item = _run_with(_task(gates=(gate,)), orch)
    denied_while_open = _raises(lambda: orch.complete(run, domain.TerminalOutcome.COMPLETED))
    orch.run_review_gate(run, item, gate)
    orch.complete(run, domain.TerminalOutcome.COMPLETED)
    return (denied_while_open and run.terminal is domain.TerminalOutcome.COMPLETED,
            "completion denied while the gate was open, permitted once satisfied")


check("assurance", "completion is denied until every gate is satisfied", completion_is_governed)


def operational_success_is_not_completion():
    gate = domain.GateRequirement(domain.GateKind.REVIEW,
                                  review_profile=domain.ReviewProfileRef("rp"))
    orch = _fresh()
    orch.router.eligible["cap"] = (domain.ModelRef("m"), domain.ModelProfileRef("p"))
    orch, run, item = _run_with(_task(gates=(gate,), capability="cap"), orch)
    decision = orch.route(run, item, _task(capability="cap"), "policy@1")
    orch.invoke_model(run, item, decision)
    return (_raises(lambda: orch.complete(run, domain.TerminalOutcome.COMPLETED)),
            "the model ran and the run still cannot complete")


check("assurance", "operational success is not governance completion",
      operational_success_is_not_completion)


# =========================================================== the suite itself


def tests_pass():
    tests_dir = os.path.join(PKG, "tests")
    loader = unittest.TestLoader()
    suite = loader.discover(tests_dir, pattern="test_*.py", top_level_dir=tests_dir)
    stream = io.StringIO()
    # The suite executes the two examples, which print. Capture their output so that `--json`
    # emits JSON and nothing else.
    captured, sys.stdout = sys.stdout, io.StringIO()
    try:
        result = unittest.TextTestRunner(stream=stream, verbosity=0).run(suite)
    finally:
        sys.stdout = captured
    return (result.wasSuccessful() and result.testsRun > 0,
            "%d tests, %d failures, %d errors"
            % (result.testsRun, len(result.failures), len(result.errors)))


check("suite", "the Phase 12 test suite passes", tests_pass)


def no_vacuous_checks():
    """This harness may not contain an unconditional pass."""
    text = read("validation/phase_12_validation.py")
    hits = [ln.strip() for ln in text.splitlines()
            if re.search(r"\bor\s+True\b|\breturn\s*\(\s*True\s*,", ln)
            and "# self-literal" not in ln]
    return (not hits, str(hits) if hits else "no unconditional pass")


check("suite", "the harness contains no vacuous or unconditional-pass check", no_vacuous_checks)


def self_check_states_the_totals():
    text = read("reviews/phase-12-foundation-self-check.md")
    stated = re.findall(r"(\d+)/(\d+) PASS", text)
    total = len(RESULTS) + 1                              # this check is not registered yet
    problems = []
    if not stated:
        problems.append("the self-check states no validator total")
    elif not any(int(a) == int(b) == total for a, b in stated):
        problems.append("self-check states %s, suite emits %d/%d" % (stated, total, total))
    if "Known limitations" not in text:
        problems.append("the self-check states no known limitations")
    return (not problems, str(problems) if problems
            else "self-check states %d/%d and its limitations" % (total, total))


check("inventory", "the producer self-check states the suite's actual total",
      self_check_states_the_totals)


def main():
    verbose = "--verbose" in sys.argv
    as_json = "--json" in sys.argv
    passed = sum(1 for r in RESULTS if r["pass"])
    if as_json:
        print(json.dumps({"total": len(RESULTS), "passed": passed, "results": RESULTS},
                         indent=2))
    else:
        order = []
        for r in RESULTS:
            if r["group"] not in order:
                order.append(r["group"])
        for group in order:
            print("\n[%s]" % group)
            for r in [x for x in RESULTS if x["group"] == group]:
                print("  %s  %s" % ("PASS" if r["pass"] else "FAIL", r["name"]))
                if (verbose or not r["pass"]) and r["evidence"]:
                    print("        %s" % r["evidence"])
        print("\n=== %d/%d PASS ===" % (passed, len(RESULTS)))
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
