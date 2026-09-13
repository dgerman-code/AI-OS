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
#
# These import the implementation and assert on behaviour. After the independent audit they
# also cover the ten structural findings: every act is checked against lineage the orchestrator
# recorded, never against an object a caller hands in at the time.


SCOPE = domain.ScopeBinding(domain.ScopeRef("scope.v"), frozenset({"INTERNAL"}), "EU")
AUTHOR = domain.RoleRef("role.v")


def _fresh(rights=None, reviews=None, eligible=None):
    router = adapters.InMemoryRouter(domain.RouterRef("router.v"), eligible=eligible or {})
    return orch_mod.Orchestrator(router, adapters.InMemoryReviewerDesk(reviews or {}),
                                 adapters.InMemoryDecisionDesk(rights or {}),
                                 adapters.StubModel())


def _task(gates=(), retry=None, capability=""):
    return domain.Task(domain.TaskRef("task.v"), "V", AUTHOR,
                       retry or domain.RetryClass.SAFE_AUTOMATIC_RETRY,
                       gates=gates, capability=capability)


def _started(task, orch=None, run_id="run.v"):
    orch = orch or _fresh()
    definition = domain.WorkflowDefinition(domain.WorkflowRef("wf.v"), "v1", (task,), SCOPE)
    run = orch.create_run(definition, domain.WorkflowRunRef(run_id))
    return orch, run, orch.activate_stage(run, task.ref)


def _decision_gate(ref="gate.d", right="dr"):
    return domain.GateRequirement(domain.GateRequirementRef(ref), domain.GateKind.DECISION,
                                  decision_right=domain.DecisionRightRef(right))


def _review_gate(ref="gate.r", profile="rp", independence="INDEPENDENT"):
    return domain.GateRequirement(domain.GateRequirementRef(ref), domain.GateKind.REVIEW,
                                  review_profile=domain.ReviewProfileRef(profile),
                                  independence_class=independence)


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


def construction_enforces_reference_types():
    """Finding 1: every governed object validates its references at construction."""
    good_result = dict(ref=domain.ModelResultRef("mr"), run=domain.WorkflowRunRef("r"),
                       work_item=domain.WorkItemRef("wi"),
                       routing_decision=domain.RoutingDecisionRef("rd"),
                       model=domain.ModelRef("m"),
                       model_profile=domain.ModelProfileRef("mp"), content="t")
    good_routing = dict(ref=domain.RoutingDecisionRef("rd"),
                        request=domain.RoutingRequestRef("rr"), run=domain.WorkflowRunRef("r"),
                        work_item=domain.WorkItemRef("wi"),
                        outcome=domain.RouterOutcome.NO_ELIGIBLE_MODEL,
                        decided_by=domain.RouterRef("router"))
    cases = [
        ("ModelResult.work_item", domain.ModelResult,
         dict(good_result, work_item=domain.TaskRef("t"))),
        ("ModelResult.model", domain.ModelResult,
         dict(good_result, model=domain.ModelProfileRef("mp"))),
        ("RoutingDecision.decided_by", domain.RoutingDecision,
         dict(good_routing, decided_by=domain.OrchestratorRef("o"))),
        ("RoutingDecision.decided_by missing", domain.RoutingDecision,
         dict(good_routing, decided_by=None)),
        ("GateInstance.work_item", domain.GateInstance, None),
        ("HumanWorkCompletion.outcome as a string", domain.HumanWorkCompletion,
         dict(ref=domain.HumanWorkRecordRef("hwr"),
              requirement=domain.GateRequirementRef("g"), run=domain.WorkflowRunRef("r"),
              work_item=domain.WorkItemRef("wi"), human_work=domain.HumanWorkRef("hw"),
              outcome="SATISFIED", completed_by=domain.HumanAuthorityRef("h"))),
        ("PrerequisiteEvidence.outcome as a string", domain.PrerequisiteEvidence,
         dict(ref=domain.PrerequisiteRecordRef("prr"),
              requirement=domain.GateRequirementRef("g"), run=domain.WorkflowRunRef("r"),
              work_item=domain.WorkItemRef("wi"), prerequisite=domain.PrerequisiteRef("pr"),
              outcome="SATISFIED", evaluated_against=domain.StorageRecordRef("sr"))),
        ("RoutingRequest.scope as a string", domain.RoutingRequest,
         dict(ref=domain.RoutingRequestRef("rr"), run=domain.WorkflowRunRef("r"),
              work_item=domain.WorkItemRef("wi"), capability="cap", scope="project.apollo",
              routing_policy="p@1")),
        ("Task.retry_class as a string", domain.Task,
         dict(ref=domain.TaskRef("t"), name="T", required_role=AUTHOR,
              retry_class="SAFE_AUTOMATIC_RETRY")),
        ("WorkflowDefinition.tasks holding a non-task", domain.WorkflowDefinition,
         dict(ref=domain.WorkflowRef("wf"), version="v1", tasks=("not a task",),
              scope=SCOPE)),
        ("ScopeBinding.sensitivity as a list", domain.ScopeBinding,
         dict(scope=domain.ScopeRef("s"), sensitivity=["A"], residency="EU")),
    ]
    problems = []
    for label, cls, kwargs in cases:
        if kwargs is None:
            if not _raises(lambda: domain.GateInstance(domain.GateInstanceRef("gi"),
                                                       _decision_gate(),
                                                       domain.WorkflowRunRef("r"),
                                                       domain.TaskRef("t"),
                                                       domain.GateKind.DECISION),
                           domain.IdentityError):
                problems.append(label)
            continue
        if not _raises(lambda cls=cls, kwargs=kwargs: cls(**kwargs), domain.IdentityError):
            problems.append(label)
    # And the well-formed ones still exist.
    domain.ModelResult(**good_result)
    domain.RoutingDecision(**good_routing)
    return (not problems, str(problems) if problems
            else "%d malformed constructions refused" % len(cases))


check("assurance", "every governed object enforces its field types at construction",
      construction_enforces_reference_types)


def every_governed_dataclass_enforces_itself():
    """Structural, not by example: each governed dataclass calls the enforcement itself."""
    import dataclasses
    governed = [obj for _name, obj in vars(domain).items()
                if isinstance(obj, type) and dataclasses.is_dataclass(obj)
                and obj is not domain.Ref and not issubclass(obj, domain.Ref)]
    missing = [cls.__name__ for cls in governed
               if "enforce_field_types" not in getattr(
                   getattr(cls, "__post_init__", None), "__code__",
                   type("x", (), {"co_names": ()})).co_names]
    return (not missing and len(governed) >= 15, str(missing) if missing
            else "%d governed dataclasses, each enforcing its own fields" % len(governed))


check("assurance", "every governed dataclass enforces its own fields",
      every_governed_dataclass_enforces_itself)


def lineage_is_bound():
    """Finding 2: an undeclared Task, a foreign Work Item or a foreign run are refused."""
    orch, run, item = _started(_task())
    problems = []
    if not _raises(lambda: orch.activate_stage(run, domain.TaskRef("task.undeclared")),
                   domain.LineageError):
        problems.append("an undeclared Task was activated")
    other, other_run, other_item = _started(_task(), run_id="run.other")
    if not _raises(lambda: orch.assign(run, other_item, AUTHOR), domain.LineageError):
        problems.append("a Work Item from another run was accepted")
    if not _raises(lambda: other.activate_stage(run, domain.TaskRef("task.v")),
                   domain.StateAccessError):
        problems.append("a run was driven by an orchestrator that did not create it")
    if item.workflow_version != "v1" or item.run != run.ref:
        problems.append("the Work Item does not carry its lineage")
    return (not problems, str(problems) if problems
            else "task, work item and run lineage are all bound")


check("assurance", "workflow, task, work item and run lineage are bound", lineage_is_bound)


def run_state_is_not_bypassable():
    """Finding 3: the audit's three-step bypass no longer reaches completion."""
    gate = _decision_gate(right="dr.absent")
    orch, run, item = _started(_task(gates=(gate,)))
    orch.run_decision_gate(run, item, gate.ref)
    if run.posture is not domain.GovernancePosture.AUTHORITY_ABSENT:
        return (False, "the missing Right did not produce AUTHORITY_ABSENT")
    refused = []
    for name, value in (("phase", domain.RunPhase.RUNNING),
                        ("posture", domain.GovernancePosture.GOVERNANCE_CLEAR),
                        ("terminal", domain.TerminalOutcome.COMPLETED),
                        ("gates", {}), ("scope", SCOPE)):
        if not _raises(lambda n=name, v=value: setattr(run, n, v), domain.StateAccessError):
            refused.append("%s was settable" % name)
    if not _raises(lambda: orch.complete(run, domain.TerminalOutcome.COMPLETED), Exception):
        refused.append("completion succeeded after the bypass attempt")
    return (not refused, str(refused) if refused
            else "phase, posture, terminal, gates and scope are read-only; completion refused")


check("assurance", "governed run state cannot be set from outside the orchestrator",
      run_state_is_not_bypassable)


def gates_keep_their_identities():
    """Finding 4: two Decision gates on one Work Item remain two requirements."""
    first, second = _decision_gate("gate.d1", "dr.one"), _decision_gate("gate.d2", "dr.two")
    orch = _fresh(rights={"dr.one": (domain.HumanAuthorityRef("h"),
                                     domain.GateOutcome.SATISFIED)})
    orch, run, item = _started(_task(gates=(first, second)), orch)
    if len(run.gates()) != 2:
        return (False, "two declared gates collapsed into %d" % len(run.gates()))
    orch.run_decision_gate(run, item, first.ref)
    open_gates = len(orch.unsatisfied_gates(run))
    refused = _raises(lambda: orch.complete(run, domain.TerminalOutcome.COMPLETED))
    return (open_gates == 1 and refused,
            "%d of 2 gates still open, completion refused" % open_gates)


check("assurance", "two gates of one kind on one Work Item do not collapse",
      gates_keep_their_identities)


def evidence_must_answer_its_requirement():
    """Finding 5: evidence is checked against the exact requirement, not a loose type."""
    gate = _decision_gate(right="dr.ok")
    orch = _fresh(rights={"dr.ok": (domain.HumanAuthorityRef("h"),
                                    domain.GateOutcome.SATISFIED)})
    orch, run, item = _started(_task(gates=(gate,)), orch)
    base = dict(ref=domain.DecisionRecordRef("dr.x"), requirement=gate.ref, run=run.ref,
                work_item=item.ref, decision_right=domain.DecisionRightRef("dr.ok"),
                outcome=domain.GateOutcome.SATISFIED,
                decided_by=domain.HumanAuthorityRef("h"))
    variants = {
        "another run": dict(base, run=domain.WorkflowRunRef("run.elsewhere")),
        "another requirement": dict(base, requirement=domain.GateRequirementRef("gate.other")),
        "another Right": dict(base, decision_right=domain.DecisionRightRef("dr.other")),
        "a non-holder": dict(base, decided_by=domain.HumanAuthorityRef("human.passer-by")),
    }
    problems = [label for label, kwargs in variants.items()
                if not _raises(lambda kwargs=kwargs: orch.satisfy_gate_with(
                    run, item, gate.ref, domain.DecisionRecord(**kwargs)),
                    domain.EvidenceError)]
    contradicting = domain.DecisionRecord(**dict(base,
                                                 outcome=domain.GateOutcome.NOT_SATISFIED))
    if not _raises(lambda: orch.satisfy_gate_with(run, item, gate.ref, contradicting,
                                                  domain.GateOutcome.SATISFIED),
                   domain.EvidenceError):
        problems.append("an applied outcome contradicted its evidence")
    return (not problems, str(problems) if problems
            else "%d mismatched Decision Records refused" % (len(variants) + 1))


check("assurance", "gate evidence must answer the exact requirement",
      evidence_must_answer_its_requirement)


def evidence_contracts_are_exclusive():
    """Finding 5: one admissible evidence type per gate kind, and no crossing over."""
    if set(domain.EVIDENCE_CONTRACT) != set(domain.GateKind):
        return (False, "the evidence contract does not cover every gate kind")
    human = domain.GateRequirement(domain.GateRequirementRef("gate.hw"),
                                   domain.GateKind.HUMAN_WORK,
                                   human_work=domain.HumanWorkRef("hw.1"))
    prereq = domain.GateRequirement(domain.GateRequirementRef("gate.pre"),
                                    domain.GateKind.GOVERNED_PREREQUISITE,
                                    prerequisite=domain.PrerequisiteRef("pre.1"))
    review = _review_gate("gate.rv", "rp.any")
    orch = _fresh(reviews={"rp.any": (domain.GateOutcome.SATISFIED,
                                      domain.HumanAuthorityRef("h"), "INDEPENDENT")})
    orch, run, item = _started(_task(gates=(human, prereq, review)), orch)
    instance = orch.run_review_gate(run, item, review.ref)
    record = domain.DecisionRecord(domain.DecisionRecordRef("dr.x"), prereq.ref, run.ref,
                                   item.ref, domain.DecisionRightRef("dr.any"),
                                   domain.GateOutcome.SATISFIED,
                                   domain.HumanAuthorityRef("h"))
    problems = []
    if not _raises(lambda: orch.satisfy_gate_with(run, item, human.ref, instance),
                   domain.EvidenceError):
        problems.append("a Review Instance satisfied a HUMAN_WORK gate")
    if not _raises(lambda: orch.satisfy_gate_with(run, item, prereq.ref, record),
                   domain.EvidenceError):
        problems.append("a Decision Record satisfied a GOVERNED_PREREQUISITE gate")
    return (not problems, str(problems) if problems
            else "four gate kinds, four exclusive evidence contracts")


check("assurance", "each gate kind admits only its own evidence type",
      evidence_contracts_are_exclusive)


def review_independence_is_enforced():
    gate = _review_gate("gate.ind", "rp.ind", "INDEPENDENT")
    orch = _fresh(reviews={"rp.ind": (domain.GateOutcome.SATISFIED,
                                      domain.HumanAuthorityRef("h"), "NOT_INDEPENDENT")})
    orch, run, item = _started(_task(gates=(gate,)), orch)
    return (_raises(lambda: orch.run_review_gate(run, item, gate.ref), domain.EvidenceError),
            "a NOT_INDEPENDENT review cannot satisfy an INDEPENDENT gate")


check("assurance", "a review's independence class must match the gate's",
      review_independence_is_enforced)


def routing_output_is_bound_to_its_request():
    """Finding 6: only the Router output this run recorded can reach model invocation."""
    orch = _fresh(eligible={"cap": (domain.ModelRef("m"), domain.ModelProfileRef("p"))})
    orch, run, item = _started(_task(capability="cap"), orch)
    fabricated = domain.RoutingDecision(
        domain.RoutingDecisionRef("rd.fake"), domain.RoutingRequestRef("rr.fake"), run.ref,
        item.ref, domain.RouterOutcome.ELIGIBLE_CANDIDATE, domain.RouterRef("router.v"),
        domain.ModelRef("model.chosen"), domain.ModelProfileRef("profile.chosen"))
    problems = []
    if not _raises(lambda: orch.invoke_model(run, item, fabricated), domain.LineageError):
        problems.append("a fabricated Routing Decision reached model invocation")
    if hasattr(orch, "record_routing_decision") or hasattr(orch, "_record_routing_decision"):
        problems.append("a public path exists for recording a manufactured Routing Decision")
    def unrelated(request):
        return domain.RoutingDecision(
            domain.RoutingDecisionRef("rd.y"), domain.RoutingRequestRef("rr.other"), run.ref,
            item.ref, domain.RouterOutcome.ELIGIBLE_CANDIDATE, domain.RouterRef("router.v"),
            domain.ModelRef("m"), domain.ModelProfileRef("p"))
    orch.router.route = unrelated
    if not _raises(lambda: orch.route(run, item, "policy@1"), domain.LineageError):
        problems.append("a decision answering another request was recorded")
    def impostor(request):
        return domain.RoutingDecision(
            domain.RoutingDecisionRef("rd.i"), request.ref, run.ref, item.ref,
            domain.RouterOutcome.ELIGIBLE_CANDIDATE, domain.RouterRef("router.other"),
            domain.ModelRef("m"), domain.ModelProfileRef("p"))
    orch.router.route = impostor
    if not _raises(lambda: orch.route(run, item, "policy@2"), domain.LineageError):
        problems.append("a decision from an unconfigured Router was recorded")
    orch.router = adapters.InMemoryRouter(
        domain.RouterRef("router.v"),
        eligible={"cap": (domain.ModelRef("m"), domain.ModelProfileRef("p"))})
    recorded = orch.route(run, item, "policy@3")
    if run.routing_decisions()[-1] is not recorded:
        problems.append("the recorded decision is not the object the Router returned")
    orch.invoke_model(run, item, recorded)
    foreign = domain.ModelResult(domain.ModelResultRef("mr.foreign"),
                                 domain.WorkflowRunRef("run.elsewhere"), item.ref,
                                 recorded.ref, recorded.model, recorded.model_profile, "t")
    orch.model.execute = lambda request: foreign
    before = len(run.model_results())
    if not _raises(lambda: orch.invoke_model(run, item, recorded), domain.LineageError):
        problems.append("a model result for another run was accepted")
    if len(run.model_results()) != before:
        problems.append("a rejected model result was still recorded")
    foreign_profile = domain.ModelResult(
        domain.ModelResultRef("mr.profile"), run.ref, item.ref, recorded.ref, recorded.model,
        domain.ModelProfileRef("profile.other"), "t")
    orch.model.execute = lambda request: foreign_profile
    if not _raises(lambda: orch.invoke_model(run, item, recorded), domain.LineageError):
        problems.append("a model result for another Model Profile was accepted")
    return (not problems, str(problems) if problems
            else "only the recorded Router output for this exact request is executable")


check("assurance", "model invocation requires the recorded Router output for that request",
      routing_output_is_bound_to_its_request)


def retry_class_cannot_be_substituted():
    """Finding 7: retry eligibility comes from the Work Item, and takes no argument."""
    problems = []
    for cls in domain.NEVER_AUTOMATICALLY_RETRYABLE:
        orch, run, item = _started(_task(retry=cls))
        if item.retry_class is not cls:
            problems.append("%s was not bound to the work item" % cls.value)
        orch.retry(run, item)
        if "retry:dispatched" in orch.log.kinds():
            problems.append("%s was retried automatically" % cls.value)
        if run.phase is not domain.RunPhase.ESCALATED:
            problems.append("%s did not escalate" % cls.value)
    orch, run, item = _started(_task(retry=domain.RetryClass.RETRY_REQUIRING_REVALIDATION))
    if not _raises(lambda: orch.retry(run, item)):
        problems.append("a revalidation-class retry ran without revalidating")
    return (not problems, str(problems) if problems
            else "retry reads the work item's bound class; there is no task argument")


check("assurance", "the retry class is bound to the work item and cannot be substituted",
      retry_class_cannot_be_substituted)


def scope_crossing_needs_governed_evidence():
    """A bare reference authorises nothing, and a well-shaped claim is not evidence either.

    Every clause is corroborated against the source run's own retained history: the Decision
    Record, the human who exercised the Right, the mechanism at its version, the complete
    source and target bindings, and the carried sensitivity and residency."""
    target = domain.ScopeBinding(domain.ScopeRef("scope.other"), frozenset({"INTERNAL"}), "EU")
    problems = []
    for label, bare in (("nothing", None),
                        ("a bare transfer id", domain.ScopeTransferRef("st")),
                        ("a bare handoff id", domain.HandoffRef("ho"))):
        orch, run, item = _started(_task(), run_id="run.%s" % label.replace(" ", "-"))
        if not _raises(lambda: orch.transfer_scope(run, run.definition,
                                                   domain.WorkflowRunRef("run.x"), target,
                                                   bare)):
            problems.append("%s authorised a crossing" % label)

    def authorised(target_binding, run_id):
        gate = _decision_gate("gate.tr", "dr.tr")
        registry = adapters.InMemoryMechanismRegistry()
        registry.register(domain.ScopeTransferRef("st.1"), "v2", SCOPE, target_binding,
                          domain.DecisionRightRef("dr.tr"), "scope_transfer")
        orch = _fresh(rights={"dr.tr": (domain.HumanAuthorityRef("h"),
                                        domain.GateOutcome.SATISFIED)})
        orch.mechanisms = registry
        orch, run, item = _started(_task(gates=(gate,)), orch, run_id=run_id)
        _outcome, record = orch.run_decision_gate(run, item, gate.ref)
        return orch, run, item, gate, record

    def build_authorisation(run, item, gate, record, target_binding, **overrides):
        fields = dict(mechanism=domain.ScopeTransferRef("st.1"), mechanism_version="v2",
                      source_run=run.ref, source_scope=run.scope, target_scope=target_binding,
                      work_item=item.ref, requirement=gate.ref,
                      decision_right=domain.DecisionRightRef("dr.tr"),
                      authorised_act="scope_transfer",
                      authorised_by=record.decided_by, decision_record=record.ref)
        fields.update(overrides)
        return domain.ScopeTransferAuthorisation(**fields)

    orch, run, item, gate, record = authorised(target, "run.fab")
    fabricated = build_authorisation(run, item, gate, record, target,
                                     decision_record=domain.DecisionRecordRef("dr.never"))
    if not _raises(lambda: orch.transfer_scope(run, run.definition,
                                               domain.WorkflowRunRef("run.x"), target,
                                               fabricated)):
        problems.append("an authorisation naming an unretained Decision Record was accepted")
    wrong_human = build_authorisation(run, item, gate, record, target,
                                      authorised_by=domain.HumanAuthorityRef("human.other"))
    if not _raises(lambda: orch.transfer_scope(run, run.definition,
                                               domain.WorkflowRunRef("run.x"), target,
                                               wrong_human)):
        problems.append("an authorisation by someone who did not decide was accepted")
    unknown = build_authorisation(run, item, gate, record, target, mechanism_version="v99")
    if not _raises(lambda: orch.transfer_scope(run, run.definition,
                                               domain.WorkflowRunRef("run.x"), target,
                                               unknown)):
        problems.append("an unrecognised mechanism version was accepted")
    orch.mechanisms.register(domain.ScopeTransferRef("st.1"), "v2", SCOPE, target,
                             domain.DecisionRightRef("dr.some-other-act"))
    if not _raises(lambda: orch.transfer_scope(
            run, run.definition, domain.WorkflowRunRef("run.wrong-right"), target,
            build_authorisation(run, item, gate, record, target))):
        problems.append("a mechanism approved for another Decision Right was accepted")

    wider = domain.ScopeBinding(domain.ScopeRef("scope.other"),
                                frozenset({"INTERNAL", "SECRET"}), "EU")
    orch_w, run_w, item_w, gate_w, record_w = authorised(wider, "run.wide")
    if not _raises(lambda: orch_w.transfer_scope(
            run_w, run_w.definition, domain.WorkflowRunRef("run.w"), wider,
            build_authorisation(run_w, item_w, gate_w, record_w, wider))):
        problems.append("a crossing widened sensitivity")

    orch_ok, run_ok, item_ok, gate_ok, record_ok = authorised(target, "run.ok")
    before = (run_ok.scope, len(orch_ok.log))
    transferred = orch_ok.transfer_scope(run_ok, run_ok.definition,
                                         domain.WorkflowRunRef("run.z"), target,
                                         build_authorisation(run_ok, item_ok, gate_ok,
                                                             record_ok, target))
    if run_ok.scope != before[0]:
        problems.append("the source run's scope binding was rewritten")
    if transferred.scope != target or transferred is run_ok:
        problems.append("the crossing did not produce a new execution in the target scope")
    return (not problems, str(problems)[:300] if problems
            else "a crossing needs corroborated governed evidence and creates a new execution")


check("assurance", "a scope crossing needs governed evidence and rewrites no binding",
      scope_crossing_needs_governed_evidence)


def governed_history_is_append_only():
    """Finding 9: nothing is overwritten by Work Item id, and no backing list is reachable."""
    gate = _decision_gate(right="dr.rep")
    orch = _fresh(rights={"dr.rep": (domain.HumanAuthorityRef("h"),
                                     domain.GateOutcome.SATISFIED)})
    orch, run, item = _started(_task(gates=(gate,)), orch)
    orch.run_decision_gate(run, item, gate.ref)
    first = run.decision_records()[0]
    orch.run_decision_gate(run, item, gate.ref)
    problems = []
    if len(run.decision_records()) != 2 or first not in run.decision_records():
        problems.append("a repeated Decision replaced the earlier governed record")
    log = domain.ExecutionEventLog()
    log.append(domain.WorkflowRunRef("r"), "a")
    for label, act in (("item assignment", lambda: log.__setitem__(0, "x")),
                       ("item deletion", lambda: log.__delitem__(0)),
                       ("attribute assignment", lambda: setattr(log, "_events", []))):
        if not _raises(act, domain.AppendOnlyError):
            problems.append("the event log permitted %s" % label)
    if "_events" in vars(log):
        problems.append("the event log exposes its backing list")
    return (not problems, str(problems) if problems
            else "repeated records stand; the log has no reachable backing list")


check("assurance", "governed history is append-only and nothing is overwritten",
      governed_history_is_append_only)


check("assurance", "a model result is a suggestion and satisfies no gate",
      lambda: (lambda result: (result.canonicality is domain.Canonicality.AI_SUGGESTION
                               and result.origin is domain.Origin.AI_GENERATED
                               and result.satisfies_gate() is False, ""))(
          domain.ModelResult(domain.ModelResultRef("mr"), domain.WorkflowRunRef("r"),
                             domain.WorkItemRef("wi"), domain.RoutingDecisionRef("rd"),
                             domain.ModelRef("m"), domain.ModelProfileRef("mp"), "t")))


def missing_right_blocks():
    gate = _decision_gate(right="dr.absent")
    orch, run, item = _started(_task(gates=(gate,)))
    outcome, record = orch.run_decision_gate(run, item, gate.ref)
    blocked = (outcome is domain.GateOutcome.NO_APPLICABLE_DECISION_RIGHT
               and record is None
               and run.phase is domain.RunPhase.ESCALATED
               and run.posture is domain.GovernancePosture.AUTHORITY_ABSENT)
    return (blocked and _raises(lambda: orch.complete(run, domain.TerminalOutcome.COMPLETED),
                                Exception),
            "%s / %s, no Decision Record produced" % (run.phase.value, run.posture.value))


check("assurance", "a missing Decision Right blocks, escalates and cannot complete",
      missing_right_blocks)


def timeout_is_not_approval():
    gate = _decision_gate(right="dr.e")
    orch = _fresh(rights={"dr.e": (domain.HumanAuthorityRef("h"),
                                   domain.GateOutcome.EXPIRED)})
    orch, run, item = _started(_task(gates=(gate,)), orch)
    outcome, _ = orch.run_decision_gate(run, item, gate.ref)
    return (outcome is domain.GateOutcome.EXPIRED
            and outcome not in domain.CONTINUING_GATE_OUTCOMES
            and run.phase is domain.RunPhase.ESCALATED, "expiry escalates, never approves")


check("assurance", "a timeout escalates and never becomes an approval", timeout_is_not_approval)


def completion_is_governed():
    gate = _review_gate()
    orch = _fresh(reviews={"rp": (domain.GateOutcome.SATISFIED,
                                  domain.HumanAuthorityRef("h"), "INDEPENDENT")})
    orch, run, item = _started(_task(gates=(gate,)), orch)
    denied = _raises(lambda: orch.complete(run, domain.TerminalOutcome.COMPLETED))
    orch.run_review_gate(run, item, gate.ref)
    orch.complete(run, domain.TerminalOutcome.COMPLETED)
    return (denied and run.terminal is domain.TerminalOutcome.COMPLETED,
            "completion denied while the gate was open, permitted once satisfied")


check("assurance", "completion is denied until every gate is satisfied", completion_is_governed)


def operational_success_is_not_completion():
    gate = _review_gate()
    orch = _fresh(eligible={"cap": (domain.ModelRef("m"), domain.ModelProfileRef("p"))},
                  reviews={"rp": (domain.GateOutcome.SATISFIED,
                                  domain.HumanAuthorityRef("h"), "INDEPENDENT")})
    orch, run, item = _started(_task(gates=(gate,), capability="cap"), orch)
    decision = orch.route(run, item, "policy@1")
    orch.invoke_model(run, item, decision)
    return (_raises(lambda: orch.complete(run, domain.TerminalOutcome.COMPLETED)),
            "the model ran and the run still cannot complete")


check("assurance", "operational success is not governance completion",
      operational_success_is_not_completion)


def _snapshot(run, orch):
    return (run.axes(),
            tuple((g.ref.id, g.outcome, g.satisfied_by) for g in run.gates()),
            tuple(r.ref for r in run.decision_records()),
            tuple(r.ref for r in run.review_instances()),
            tuple(r.ref for r in run.human_work_records()),
            tuple(r.ref for r in run.prerequisite_records()),
            tuple(r.ref for r in run.routing_requests()),
            tuple(r.ref for r in run.routing_decisions()),
            tuple(r.ref for r in run.model_results()),
            len(run.assignments()), tuple(r.ref for r in run.interventions()), len(orch.log))


def gate_instances_keep_their_identities():
    """Re-audit finding 2: repeated activation and reused requirement ids do not displace."""
    gate = _decision_gate("gate.shared", "dr.shared")
    orch = _fresh(rights={"dr.shared": (domain.HumanAuthorityRef("h"),
                                        domain.GateOutcome.SATISFIED)})
    orch, run, first = _started(_task(gates=(gate,)), orch)
    second = orch.activate_stage(run, domain.TaskRef("task.v"))
    problems = []
    if len(run.work_items()) != 2 or len(run.gates()) != 2:
        problems.append("a second activation did not create its own work item and gate")
    if len({g.ref for g in run.gates()}) != 2:
        problems.append("two gate instances share one identity")
    orch.run_decision_gate(run, second, gate.ref)
    open_gates = orch.unsatisfied_gates(run)
    if len(open_gates) != 1 or open_gates[0].work_item != first.ref:
        problems.append("satisfying the second gate displaced the first")
    if not _raises(lambda: orch.complete(run, domain.TerminalOutcome.COMPLETED)):
        problems.append("completion was permitted with a gate still open")
    # Two tasks reusing one requirement id.
    shared = domain.GateRequirementRef("gate.reused")
    task_a = domain.Task(domain.TaskRef("task.a"), "A", AUTHOR,
                         domain.RetryClass.SAFE_AUTOMATIC_RETRY,
                         gates=(domain.GateRequirement(
                             shared, domain.GateKind.DECISION,
                             decision_right=domain.DecisionRightRef("dr.a")),))
    task_b = domain.Task(domain.TaskRef("task.b"), "B", AUTHOR,
                         domain.RetryClass.SAFE_AUTOMATIC_RETRY,
                         gates=(domain.GateRequirement(
                             shared, domain.GateKind.DECISION,
                             decision_right=domain.DecisionRightRef("dr.b")),))
    orch2 = _fresh(rights={"dr.a": (domain.HumanAuthorityRef("h"),
                                    domain.GateOutcome.SATISFIED)})
    definition = domain.WorkflowDefinition(domain.WorkflowRef("wf.two"), "v1",
                                           (task_a, task_b), SCOPE)
    run2 = orch2.create_run(definition, domain.WorkflowRunRef("run.two"))
    item_a = orch2.activate_stage(run2, task_a.ref)
    item_b = orch2.activate_stage(run2, task_b.ref)
    orch2.run_decision_gate(run2, item_a, shared)
    remaining = orch2.unsatisfied_gates(run2)
    if len(remaining) != 1 or remaining[0].work_item != item_b.ref:
        problems.append("two tasks reusing one requirement id aliased their gates")
    return (not problems, str(problems)[:300] if problems
            else "gate instances are identified per run, work item and requirement")


check("assurance", "gate instances keep their own identities",
      gate_instances_keep_their_identities)


def a_halted_run_cannot_progress():
    """Re-audit finding 3: BLOCKED, ESCALATED and AUTHORITY_ABSENT stop ordinary progression."""
    gate = _decision_gate("gate.absent", "dr.absent")
    review = _review_gate("gate.review", "rp", "INDEPENDENT")
    human = domain.GateRequirement(domain.GateRequirementRef("gate.human"),
                                   domain.GateKind.HUMAN_WORK,
                                   human_work=domain.HumanWorkRef("hw"))
    prereq = domain.GateRequirement(domain.GateRequirementRef("gate.pre"),
                                    domain.GateKind.GOVERNED_PREREQUISITE,
                                    prerequisite=domain.PrerequisiteRef("pre"))
    orch = _fresh(eligible={"cap": (domain.ModelRef("m"), domain.ModelProfileRef("p"))},
                  reviews={"rp": (domain.GateOutcome.SATISFIED,
                                    domain.HumanAuthorityRef("reviewer"), "INDEPENDENT")})
    orch, run, item = _started(_task(gates=(gate, review, human, prereq), capability="cap"),
                               orch)
    routed = orch.route(run, item, "policy@1")
    orch.run_decision_gate(run, item, gate.ref)
    problems = []
    if run.posture is not domain.GovernancePosture.AUTHORITY_ABSENT:
        problems.append("the missing Right did not produce AUTHORITY_ABSENT")
    if not _raises(lambda: orch.activate_stage(run, domain.TaskRef("task.v")), Exception):
        problems.append("a halted run activated another stage")
    human_record = domain.HumanWorkCompletion(
        domain.HumanWorkRecordRef("hwr.blocked"), human.ref, run.ref, item.ref,
        domain.HumanWorkRef("hw"), domain.GateOutcome.SATISFIED,
        domain.HumanAuthorityRef("h"))
    prerequisite_record = domain.PrerequisiteEvidence(
        domain.PrerequisiteRecordRef("prr.blocked"), prereq.ref, run.ref, item.ref,
        domain.PrerequisiteRef("pre"), domain.GateOutcome.SATISFIED,
        domain.StorageRecordRef("sr"))
    ordinary = (
        lambda: orch.assign(run, item, AUTHOR),
        lambda: orch.request_routing(run, item, "policy@2"),
        lambda: orch.route(run, item, "policy@2"),
        lambda: orch.invoke_model(run, item, routed),
        lambda: orch.run_review_gate(run, item, review.ref),
        lambda: orch.run_decision_gate(run, item, gate.ref),
        lambda: orch.record_human_work(run, item, human.ref, human_record),
        lambda: orch.record_prerequisite(run, item, prereq.ref, prerequisite_record),
        lambda: orch.satisfy_gate_with(run, item, prereq.ref, prerequisite_record),
        lambda: orch.retry(run, item),
        lambda: orch.complete(run, domain.TerminalOutcome.COMPLETED),
    )
    for act in ordinary:
        before = _snapshot(run, orch)
        if not _raises(act):
            problems.append("an ordinary progression API advanced a halted run")
        if _snapshot(run, orch) != before:
            problems.append("a refused halted-run act changed state or history")
    retained_missing = [g for g in run.gates() if g.requirement.ref == gate.ref]
    if len(retained_missing) != 1 or retained_missing[0].outcome is not \
            domain.GateOutcome.NO_APPLICABLE_DECISION_RIGHT:
        problems.append("the original gate was not retained")
    intervention = domain.HumanInterventionRecord(
        domain.InterventionRef("iv"), run.ref, domain.HumanAuthorityRef("h"), "unblock",
        "asking politely")
    if not _raises(lambda: orch.unblock(run, intervention)):
        problems.append("a standing unresolved gate did not prevent unblocking")
    return (not problems, str(problems) if problems
            else "all ordinary progression APIs stop until governed unblock/reconciliation")


check("assurance", "a blocked or escalated run cannot progress through the stage API",
      a_halted_run_cannot_progress)


def validation_precedes_every_mutation():
    """Re-audit finding 4: a refusal leaves run state and every history exactly as they were."""
    problems = []
    # A continuing decision outcome with no record.
    gate = _decision_gate("gate.norec", "dr.norec")
    orch, run, item = _started(_task(gates=(gate,)))
    orch.decisions.decide = lambda request: (domain.GateOutcome.SATISFIED, None)
    before = _snapshot(run, orch)
    if not _raises(lambda: orch.run_decision_gate(run, item, gate.ref), domain.EvidenceError):
        problems.append("a continuing outcome with no Decision Record was applied")
    if _snapshot(run, orch) != before:
        problems.append("the refused decision left state or history changed")
    # Rejected external evidence.
    gate2 = _decision_gate("gate.part", "dr.part")
    orch2 = _fresh(rights={"dr.part": (domain.HumanAuthorityRef("h"),
                                       domain.GateOutcome.SATISFIED)})
    orch2, run2, item2 = _started(_task(gates=(gate2,)), orch2, run_id="run.part")
    forged = domain.DecisionRecord(domain.DecisionRecordRef("dr.forged"), gate2.ref,
                                   domain.WorkflowRunRef("run.elsewhere"), item2.ref,
                                   domain.DecisionRightRef("dr.part"),
                                   domain.GateOutcome.SATISFIED,
                                   domain.HumanAuthorityRef("h"))
    before2 = _snapshot(run2, orch2)
    if not _raises(lambda: orch2.satisfy_gate_with(run2, item2, gate2.ref, forged),
                   domain.EvidenceError):
        problems.append("forged evidence satisfied a gate")
    if _snapshot(run2, orch2) != before2:
        problems.append("the refused evidence left state or history changed")
    # A rejected review.
    gate3 = _review_gate("gate.ind", "rp.ind", "INDEPENDENT")
    orch3 = _fresh(reviews={"rp.ind": (domain.GateOutcome.SATISFIED,
                                       domain.HumanAuthorityRef("h"), "NOT_INDEPENDENT")})
    orch3, run3, item3 = _started(_task(gates=(gate3,)), orch3, run_id="run.rev")
    before3 = _snapshot(run3, orch3)
    if not _raises(lambda: orch3.run_review_gate(run3, item3, gate3.ref),
                   domain.EvidenceError):
        problems.append("a mismatched review satisfied a gate")
    if _snapshot(run3, orch3) != before3:
        problems.append("the refused review left state or history changed")
    # A duplicate identity is invalid evidence for this history and must be rejected before
    # the review path moves the run into WAITING.
    first = _review_gate("gate.dup.1", "rp.dup", "INDEPENDENT")
    second = _review_gate("gate.dup.2", "rp.dup", "INDEPENDENT")
    orch4, run4, item4 = _started(_task(gates=(first, second)), run_id="run.dup")
    def repeated(request):
        return domain.ReviewInstance(
            domain.ReviewInstanceRef("ri.same"), request.requirement, request.run,
            request.work_item, request.review_profile, domain.GateOutcome.SATISFIED,
            domain.HumanAuthorityRef("h"), request.independence_class)
    orch4.reviewers.review = repeated
    orch4.run_review_gate(run4, item4, first.ref)
    before4 = _snapshot(run4, orch4)
    if not _raises(lambda: orch4.run_review_gate(run4, item4, second.ref),
                   domain.AppendOnlyError):
        problems.append("duplicate evidence identity was accepted")
    if _snapshot(run4, orch4) != before4:
        problems.append("duplicate evidence changed state before append refusal")
    return (not problems, str(problems)[:300] if problems
            else "four refusals, each leaving run state and every history identical")


check("assurance", "validation completes before any state or history is changed",
      validation_precedes_every_mutation)


def open_items_apply_to_every_gate_kind():
    """Re-audit finding 5: SATISFIED_WITH_OPEN_ITEMS means the same thing everywhere."""
    problems = []
    human = domain.GateRequirement(domain.GateRequirementRef("gate.hw"),
                                   domain.GateKind.HUMAN_WORK,
                                   human_work=domain.HumanWorkRef("hw"))
    orch, run, item = _started(_task(gates=(human,)), run_id="run.hw")
    orch.record_human_work(run, item, human.ref, domain.HumanWorkCompletion(
        domain.HumanWorkRecordRef("hwr"), human.ref, run.ref, item.ref,
        domain.HumanWorkRef("hw"), domain.GateOutcome.SATISFIED_WITH_OPEN_ITEMS,
        domain.HumanAuthorityRef("h")))
    if run.posture is not domain.GovernancePosture.OPEN_ITEMS_CARRIED:
        problems.append("HUMAN_WORK did not carry open items")
    if not _raises(lambda: orch.complete(run, domain.TerminalOutcome.COMPLETED)):
        problems.append("a run carrying open items completed as GOVERNANCE_CLEAR")
    orch.complete(run, domain.TerminalOutcome.COMPLETED_WITH_OPEN_ITEMS)

    prereq = domain.GateRequirement(domain.GateRequirementRef("gate.pre"),
                                    domain.GateKind.GOVERNED_PREREQUISITE,
                                    prerequisite=domain.PrerequisiteRef("pre"))
    orch2, run2, item2 = _started(_task(gates=(prereq,)), run_id="run.pre")
    evidence = domain.PrerequisiteEvidence(
        domain.PrerequisiteRecordRef("prr"), prereq.ref, run2.ref, item2.ref,
        domain.PrerequisiteRef("pre"), domain.GateOutcome.SATISFIED_WITH_OPEN_ITEMS,
        domain.StorageRecordRef("sr"))
    orch2.satisfy_gate_with(run2, item2, prereq.ref, evidence)
    if run2.posture is not domain.GovernancePosture.OPEN_ITEMS_CARRIED:
        problems.append("externally supplied evidence did not carry open items")

    decision = _decision_gate("gate.oi", "dr.oi")
    orch3 = _fresh(rights={"dr.oi": (domain.HumanAuthorityRef("h"),
                                     domain.GateOutcome.SATISFIED_WITH_OPEN_ITEMS)})
    orch3, run3, item3 = _started(_task(gates=(decision,)), orch3, run_id="run.oi")
    orch3.run_decision_gate(run3, item3, decision.ref)
    if run3.posture is not domain.GovernancePosture.OPEN_ITEMS_CARRIED:
        problems.append("DECISION did not carry open items")
    return (not problems, str(problems) if problems
            else "open items carry for human work, prerequisites, decisions and reviews")


check("assurance", "satisfied-with-open-items carries for every gate kind",
      open_items_apply_to_every_gate_kind)


def satisfying_evidence_is_retained():
    """Re-audit finding 8: no gate changes state without the record that explains it."""
    review = _review_gate("gate.r", "rp", "INDEPENDENT")
    decision = _decision_gate("gate.d", "dr")
    human = domain.GateRequirement(domain.GateRequirementRef("gate.h"),
                                   domain.GateKind.HUMAN_WORK,
                                   human_work=domain.HumanWorkRef("hw"))
    prereq = domain.GateRequirement(domain.GateRequirementRef("gate.p"),
                                    domain.GateKind.GOVERNED_PREREQUISITE,
                                    prerequisite=domain.PrerequisiteRef("pre"))
    orch = _fresh(reviews={"rp": (domain.GateOutcome.SATISFIED,
                                  domain.HumanAuthorityRef("h1"), "INDEPENDENT")},
                  rights={"dr": (domain.HumanAuthorityRef("h2"),
                                 domain.GateOutcome.SATISFIED)})
    orch, run, item = _started(_task(gates=(review, decision, human, prereq)), orch)
    orch.run_review_gate(run, item, review.ref)
    orch.run_decision_gate(run, item, decision.ref)
    orch.record_human_work(run, item, human.ref, domain.HumanWorkCompletion(
        domain.HumanWorkRecordRef("hwr"), human.ref, run.ref, item.ref,
        domain.HumanWorkRef("hw"), domain.GateOutcome.SATISFIED,
        domain.HumanAuthorityRef("h3")))
    evidence = domain.PrerequisiteEvidence(
        domain.PrerequisiteRecordRef("prr"), prereq.ref, run.ref, item.ref,
        domain.PrerequisiteRef("pre"), domain.GateOutcome.SATISFIED,
        domain.StorageRecordRef("sr"))
    orch.satisfy_gate_with(run, item, prereq.ref, evidence)
    problems = [g.kind.value for g in run.gates() if run.evidence_for(g) is None]
    if not _raises(lambda: orch.record_prerequisite(run, item, prereq.ref, evidence),
                   domain.AppendOnlyError):
        problems.append("a duplicate record identity was admitted")
    orch.complete(run, domain.TerminalOutcome.COMPLETED)
    model_orch = _fresh(eligible={"cap": (domain.ModelRef("m"),
                                           domain.ModelProfileRef("p"))})
    model_orch, model_run, model_item = _started(
        _task(capability="cap"), model_orch, run_id="run.model-history")
    routed = model_orch.route(model_run, model_item, "policy@1")
    model_record = domain.ModelResult(
        domain.ModelResultRef("mr.same"), model_run.ref, model_item.ref, routed.ref,
        routed.model, routed.model_profile, "t")
    model_orch.model.execute = lambda request: model_record
    model_orch.invoke_model(model_run, model_item, routed)
    if not _raises(lambda: model_orch.invoke_model(model_run, model_item, routed),
                   domain.AppendOnlyError):
        problems.append("a duplicate Model Result identity was admitted")
    return (not problems, str(problems) if problems
            else "all gate evidence and model results retain unique governed identities")


check("assurance", "every satisfying evidence object is retained in governed history",
      satisfying_evidence_is_retained)


def a_halted_run_refuses_every_ordinary_api():
    """One guard, every API. The re-audit found it in one place and absent from eleven."""
    gate = _decision_gate("gate.absent", "dr.absent")
    orch, run, item = _started(_task(gates=(gate,)), run_id="run.halt")
    orch.run_decision_gate(run, item, gate.ref)
    if run.posture is not domain.GovernancePosture.AUTHORITY_ABSENT:
        return (False, "the missing Right did not produce AUTHORITY_ABSENT")
    prereq = domain.GateRequirement(domain.GateRequirementRef("gate.p"),
                                    domain.GateKind.GOVERNED_PREREQUISITE,
                                    prerequisite=domain.PrerequisiteRef("pre"))
    evidence = domain.PrerequisiteEvidence(
        domain.PrerequisiteRecordRef("prr.h"), prereq.ref, run.ref, item.ref,
        domain.PrerequisiteRef("pre"), domain.GateOutcome.SATISFIED,
        domain.StorageRecordRef("sr"))
    intervention = domain.HumanInterventionRecord(
        domain.InterventionRef("iv.h"), run.ref, domain.HumanAuthorityRef("h"), "note",
        "while halted")
    apis = {
        "activate a stage": lambda: orch.activate_stage(run, domain.TaskRef("task.v")),
        "assign": lambda: orch.assign(run, item, AUTHOR),
        "request routing": lambda: orch.request_routing(run, item, "policy@1"),
        "route": lambda: orch.route(run, item, "policy@1"),
        "run a review gate": lambda: orch.run_review_gate(run, item, gate.ref),
        "run a decision gate": lambda: orch.run_decision_gate(run, item, gate.ref),
        "satisfy a gate": lambda: orch.satisfy_gate_with(run, item, prereq.ref, evidence),
        "record human work": lambda: orch.record_human_work(run, item, prereq.ref, evidence),
        "record a prerequisite": lambda: orch.record_prerequisite(run, item, prereq.ref,
                                                                  evidence),
        "retry": lambda: orch.retry(run, item),
        "record an intervention": lambda: orch.record_intervention(run, intervention),
        "pause": lambda: orch.pause(run, intervention),
        "complete": lambda: orch.complete(run, domain.TerminalOutcome.COMPLETED),
        "open a sub-run": lambda: orch.open_sub_run(run, run.definition,
                                                    domain.WorkflowRunRef("run.sub"),
                                                    run.scope),
        "transfer scope": lambda: orch.transfer_scope(run, run.definition,
                                                      domain.WorkflowRunRef("run.tx"),
                                                      run.scope, None),
    }
    before = _snapshot(run, orch)
    permitted = [name for name, call in apis.items() if not _raises(call, Exception)]
    problems = ["%s was permitted while halted" % name for name in permitted]
    if _snapshot(run, orch) != before:
        problems.append("a refused API left state or history changed")
    # And the one governed way out still refuses while the gate stands.
    if not _raises(lambda: orch.unblock(run, intervention)):
        problems.append("unblock resumed a run whose gate still stands")
    return (not problems, str(problems)[:300] if problems
            else "%d ordinary APIs refused, state and history unchanged, unblock refused"
                 % len(apis))


check("assurance", "a halted run refuses every ordinary API through one guard",
      a_halted_run_refuses_every_ordinary_api)


def a_halted_run_may_still_be_stopped_and_recovered():
    """Stopping is always permitted; recovery is a governed act with its own conditions."""
    orch, run, item = _started(_task(capability="cap"), run_id="run.stop")
    orch.route(run, item, "policy@1")                      # no eligible model -> BLOCKED
    problems = []
    if run.phase is not domain.RunPhase.BLOCKED:
        problems.append("the routing block did not reach BLOCKED")
    intervention = domain.HumanInterventionRecord(
        domain.InterventionRef("iv.s"), run.ref, domain.HumanAuthorityRef("h"), "unblock",
        "an eligible deployment was registered")
    orch.unblock(run, intervention)
    if run.phase is not domain.RunPhase.RUNNING:
        problems.append("the governed recovery path did not resume the run")
    orch2, run2, item2 = _started(_task(capability="cap"), run_id="run.stop2")
    orch2.route(run2, item2, "policy@1")
    stop = domain.HumanInterventionRecord(
        domain.InterventionRef("iv.c"), run2.ref, domain.HumanAuthorityRef("h"), "cancel",
        "the work is not wanted")
    orch2.complete(run2, domain.TerminalOutcome.CANCELLED, intervention=stop)
    if run2.terminal is not domain.TerminalOutcome.CANCELLED:
        problems.append("a halted run could not be cancelled")
    return (not problems, str(problems) if problems
            else "a halted run stops freely and resumes only through unblock()")


check("assurance", "a halted run may still be stopped, and recovers only through unblock",
      a_halted_run_may_still_be_stopped_and_recovered)


def routing_origin_is_not_caller_assertable():
    """There is no callable path that admits a Routing Decision the Router did not return."""
    orch, run, item = _started(_task(capability="cap"), run_id="run.prov")
    orch.router.eligible["cap"] = (domain.ModelRef("m"), domain.ModelProfileRef("p"))
    problems = []
    for name in ("record_routing_decision", "_record_routing_decision"):
        if hasattr(orch, name):
            problems.append("a recording path still exists: %s" % name)
    request = orch.request_routing(run, item, "policy@1")
    fabricated = domain.RoutingDecision(
        domain.RoutingDecisionRef("rd.fake"), request.ref, run.ref, item.ref,
        domain.RouterOutcome.ELIGIBLE_CANDIDATE, orch.router.ref,
        domain.ModelRef("model.chosen"), domain.ModelProfileRef("profile.chosen"))
    if not _raises(lambda: orch.invoke_model(run, item, fabricated), domain.LineageError):
        problems.append("a fabricated Routing Decision reached model invocation")
    if any(r.ref == fabricated.ref for r in run.routing_decisions()):
        problems.append("a fabricated Routing Decision entered governed history")
    calls = len(orch.router.requests)
    recorded = orch.route(run, item, "policy@2")
    if len(orch.router.requests) != calls + 1:
        problems.append("routing recorded without invoking the configured Router")
    if run.routing_decisions()[-1] is not recorded:
        problems.append("the recorded decision is not the object the Router returned")
    return (not problems, str(problems)[:300] if problems
            else "routing enters history only as the configured Router's own answer")


check("assurance", "a Routing Decision's origin cannot be asserted by a caller",
      routing_origin_is_not_caller_assertable)


def a_crossing_binds_the_right_and_the_act():
    """Mechanism and bindings are not enough: the Right and the act are part of the approval."""
    target = domain.ScopeBinding(domain.ScopeRef("scope.other"), frozenset({"INTERNAL"}), "EU")

    def fixture(right="dr.tr", act="scope_transfer", run_id="run.act"):
        gate = _decision_gate("gate.tr", "dr.tr")
        registry = adapters.InMemoryMechanismRegistry()
        registry.register(domain.ScopeTransferRef("st.1"), "v2", SCOPE, target,
                          domain.DecisionRightRef(right), act)
        orch = _fresh(rights={"dr.tr": (domain.HumanAuthorityRef("h"),
                                        domain.GateOutcome.SATISFIED)})
        orch.mechanisms = registry
        orch, run, item = _started(_task(gates=(gate,)), orch, run_id=run_id)
        _outcome, record = orch.run_decision_gate(run, item, gate.ref)
        return orch, run, item, gate, record

    def authorisation(run, item, gate, record, **overrides):
        fields = dict(mechanism=domain.ScopeTransferRef("st.1"), mechanism_version="v2",
                      source_run=run.ref, source_scope=run.scope, target_scope=target,
                      work_item=item.ref, requirement=gate.ref,
                      decision_right=domain.DecisionRightRef("dr.tr"),
                      authorised_act="scope_transfer", authorised_by=record.decided_by,
                      decision_record=record.ref)
        fields.update(overrides)
        return domain.ScopeTransferAuthorisation(**fields)

    problems = []
    orch, run, item, gate, record = fixture(right="dr.unrelated", run_id="run.act1")
    if not _raises(lambda: orch.transfer_scope(run, run.definition,
                                               domain.WorkflowRunRef("run.x"), target,
                                               authorisation(run, item, gate, record))):
        problems.append("an unrelated Decision Right authorised a registered crossing")
    orch, run, item, gate, record = fixture(act="evidence_export", run_id="run.act2")
    if not _raises(lambda: orch.transfer_scope(run, run.definition,
                                               domain.WorkflowRunRef("run.x"), target,
                                               authorisation(run, item, gate, record))):
        problems.append("a crossing registered for another act was approved")
    orch, run, item, gate, record = fixture(run_id="run.act3")
    before = _snapshot(run, orch)
    if not _raises(lambda: orch.transfer_scope(
            run, run.definition, domain.WorkflowRunRef("run.x"), target,
            authorisation(run, item, gate, record, authorised_act="something_else"))):
        problems.append("a mismatched authorised act was accepted")
    if _snapshot(run, orch) != before:
        problems.append("a refused crossing left state or history changed")
    transferred = orch.transfer_scope(run, run.definition, domain.WorkflowRunRef("run.ok"),
                                      target, authorisation(run, item, gate, record))
    if transferred.scope != target or run.scope == target:
        problems.append("the approved crossing did not produce a new bound execution")
    return (not problems, str(problems)[:300] if problems
            else "a crossing binds mechanism, version, bindings, Right and act")


check("assurance", "a scope crossing binds the exact Decision Right and authorised act",
      a_crossing_binds_the_right_and_the_act)


def model_results_carry_identity_and_profile_lineage():
    """A result is a governed record: it has an identity, and it names what was selected."""
    orch = _fresh(eligible={"cap": (domain.ModelRef("m"), domain.ModelProfileRef("p"))})
    orch, run, item = _started(_task(capability="cap"), orch, run_id="run.mr")
    decision = orch.route(run, item, "policy@1")
    first = orch.invoke_model(run, item, decision)
    problems = []
    if not isinstance(first.ref, domain.ModelResultRef):
        problems.append("a model result carries no governed identity")
    if first.model != decision.model or first.model_profile != decision.model_profile:
        problems.append("the retained result does not reconstruct the selection lineage")
    before = _snapshot(run, orch)
    orch.model.execute = lambda request: first                 # a duplicate identity
    if not _raises(lambda: orch.invoke_model(run, item, decision), Exception):
        problems.append("a duplicate Model Result identity was admitted")
    if _snapshot(run, orch) != before:
        problems.append("a refused duplicate left a partial mutation behind")
    orch.model.execute = lambda request: domain.ModelResult(
        domain.ModelResultRef("mr.wrong"), run.ref, item.ref, decision.ref, decision.model,
        domain.ModelProfileRef("profile.somethingelse"), "t")
    if not _raises(lambda: orch.invoke_model(run, item, decision), domain.LineageError):
        problems.append("a result under a different Model Profile was accepted")
    if _snapshot(run, orch) != before:
        problems.append("a refused profile mismatch left a partial mutation behind")
    return (not problems, str(problems)[:300] if problems
            else "model results carry identity, profile lineage and duplicate refusal")


check("assurance", "a Model Result carries its identity and its selection lineage",
      model_results_carry_identity_and_profile_lineage)


# =========================================================== the suite itself


MUTATION_HARNESS = "implementation/phase-12/tests/test_mutation_guards.py"

check("suite", "the controlled-weakening harness is committed",
      lambda: (os.path.exists(os.path.join(REPO, MUTATION_HARNESS))
               and "WEAKENINGS" in read(MUTATION_HARNESS), MUTATION_HARNESS))


def mutation_harness_classifications_hold():
    """Run the committed weakenings here too, and check the classification independently.

    The harness classifies each weakening DETECTED or REDUNDANT. This check re-derives the
    classification from the runner itself rather than trusting the label, so a weakening that
    quietly stopped biting is a validator failure and not merely a comment."""
    sys.path.insert(0, os.path.join(PKG, "tests"))
    captured, sys.stdout = sys.stdout, io.StringIO()
    try:
        import test_mutation_guards as harness
        results = {}
        for name, mutations, scenario, expectation in harness.WEAKENINGS:
            with harness.implementation(mutations) as env:
                try:
                    scenario(env)
                    detected = False
                except AssertionError:
                    detected = True
            results[name] = ("DETECTED" if detected else "REDUNDANT", expectation)
    finally:
        sys.stdout = captured
    wrong = ["%s: observed %s, classified %s" % (name, observed, claimed)
             for name, (observed, claimed) in results.items() if observed != claimed]
    detected = [n for n, (observed, _c) in results.items() if observed == "DETECTED"]
    if len(detected) < 10:
        wrong.append("only %d weakenings actually bite" % len(detected))
    return (not wrong, str(wrong)[:300] if wrong
            else "%d weakenings, %d detected, every classification reproduced"
                 % (len(results), len(detected)))


check("suite", "every committed weakening behaves as the harness classifies it",
      mutation_harness_classifications_hold)


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
