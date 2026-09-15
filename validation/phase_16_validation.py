"""Phase 16 — planner activation and execution-basis validator.

Status: PROPOSED. Standard library only, deterministic, no network, no third-party imports.

    python3 validation/phase_16_validation.py [--verbose] [--json]

This harness is an ASSURANCE TOOL AND NEVER GOVERNANCE AUTHORITY. A passing check is evidence
that a check passed. It approves nothing, satisfies no review, creates no Decision Right, and
does not make the Phase 16 proposal correct.

It is deliberately BEHAVIOURAL first. Most checks import the reference implementation and try to
do the forbidden thing, because a rule that is only written down is a rule a mutation can dodge
by editing one sentence. The prose layer then checks that the package says what the code does,
so the two cannot drift apart silently.

It modifies no approved validator and reads no approved artifact except by path existence.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
#: The mutation probes run this validator against a throwaway COPY of the package, so the repo
#: root is overridable. Nothing else reads it, and it never points at the real tree during a
#: probe run - a probe that mutated the working tree would be a destructive test, not a test.
REPO = os.environ.get("PHASE_16_REPO_ROOT") or os.path.dirname(HERE)
PKG = os.path.join(REPO, "planner-activation")
IMPL = os.path.join(REPO, "implementation", "phase-16")

sys.path.insert(0, IMPL)

RESULTS = []

PACKAGE_DOCS = (
    "README.md",
    "planner-output-contract.md",
    "workflow-resolution-contract.md",
    "execution-basis-contract.md",
    "planner-orchestrator-handoff.md",
    "change-control-contract.md",
    "clarification-and-ambiguity-contract.md",
    "criticality-review-authority-binding.md",
    "role-skill-assignment-binding.md",
    "idempotency-versioning-replay.md",
    "observability-audit-provenance.md",
    "po-4-and-po-12-closure.md",
    "phase-16-self-check.md",
)

IMPL_MODULES = ("domain.py", "registries.py", "preflight.py", "handoff.py", "store.py")


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def doc(name):
    return read(os.path.join(PKG, name))


def flat(text):
    text = text.replace("*", "").replace("`", "").replace("—", " ")
    text = re.sub(r"(?m)^\s*>+\s?", " ", text)
    text = re.sub(r"(?m)^\s*[-*+]\s+", " ", text)
    return " ".join(text.split()).lower()


def check(group, name, passed, evidence=""):
    RESULTS.append({"group": group, "name": name, "pass": bool(passed),
                    "evidence": evidence})


def refuses(fn, *exc):
    """Did the call refuse with one of the expected governance exceptions?

    A rule that can be violated and merely logged is not enforced, so a check that accepts a
    returned error object instead of a raised one would be testing nothing.
    """
    try:
        fn()
    except exc as err:
        return True, "%s: %s" % (type(err).__name__, str(err)[:110])
    except Exception as err:                                          # pragma: no cover
        return False, "wrong exception %s: %s" % (type(err).__name__, err)
    return False, "the call returned instead of refusing"


# =========================================================== imports

import registries                                                         # noqa: E402
from domain import (                                                      # noqa: E402
    ActivationError, BasisStatus, ClarificationRequirement, Criticality, DecisionRequirement,
    EvidenceRequirement, ExecutionMode, GovernanceError, PlanStage, PlannerOutput, PlannerState,
    PrerequisiteState, ReviewRequirement, RoleRequirement, SkillRequirement, WorkMode, WorkPlan,
)
from handoff import (                                                     # noqa: E402
    FORBIDDEN_IN_TRIGGER, PlannedWorkItemSpec, build_trigger, idempotency_key,
)
from preflight import IMPLEMENTATION_SPEC_VERSION, run_preflight          # noqa: E402
from store import ActivationStore                                         # noqa: E402


def a_role():
    return sorted(registries.approved_roles())[0]


def a_workflow():
    return sorted(registries.approved_workflows())[0]


def plan(**overrides):
    fields = dict(
        request_id="request.V", request_text="Prepare the partner response.",
        intent_id="intent.V", scope_ref="scope.project.alpha",
        scope_ancestry=("scope.org.root", "scope.project.alpha"),
        objective="Produce a governed response", deliverables=("A drafted response",),
        primary_work_mode=WorkMode.DRAFTING, secondary_work_modes=(),
        criticality=Criticality.ROUTINE, execution_mode=ExecutionMode.COMPOSE,
        role_requirements=(RoleRequirement(a_role(), "the domain conclusion"),),
        work_plan=WorkPlan("work_plan.V", 1, (
            PlanStage("S1", a_role(), (), False, "draft"),
            PlanStage("S2", None, ("S1",), True, ""),
        )),
    )
    fields.update(overrides)
    return PlannerOutput(**fields)


def executable(**overrides):
    p = plan(**overrides)
    result = run_preflight(p)
    return p, result


# =========================================================== 1. package shape

G = "package"

for name in PACKAGE_DOCS:
    check(G, "document present: %s" % name, os.path.isfile(os.path.join(PKG, name)))

for name in IMPL_MODULES:
    check(G, "module present: implementation/phase-16/%s" % name,
          os.path.isfile(os.path.join(IMPL, name)))

check(G, "acceptance tests present",
      os.path.isfile(os.path.join(IMPL, "tests", "test_activation_invariants.py")))
check(G, "both examples present",
      os.path.isfile(os.path.join(IMPL, "examples", "executable_run.py"))
      and os.path.isfile(os.path.join(IMPL, "examples", "blocked_run.py")))

_readme = flat(doc("README.md"))
check(G, "the package declares itself PROPOSED and unapproved",
      "nothing in this package is approved" in _readme,
      "README.md governance banner")
check(G, "every package document is named in the README map",
      all(n in doc("README.md") for n in PACKAGE_DOCS if n != "README.md"),
      "README.md §3")

_impl_text = "\n".join(read(os.path.join(IMPL, m)) for m in IMPL_MODULES)
check(G, "the reference implementation imports no third-party module",
      not re.search(r"(?m)^\s*(import|from)\s+(?!os|sys|re|json|hashlib|dataclasses|"
                    r"typing|enum|collections|itertools|__future__|domain|registries|"
                    r"preflight|handoff|store)\w", _impl_text),
      "standard library plus sibling modules only")
check(G, "the reference implementation opens no network or database connection",
      not re.search(r"\b(requests|urllib|socket|httpx|psycopg|sqlite3|supabase|boto3)\b",
                    _impl_text),
      "no client library appears anywhere in the implementation")


# =========================================================== 2. the twelve classes

G = "C-1 COMPOSE executable without a basis"

_p, _r = executable()
check(G, "a COMPOSE plan reaches EXECUTABLE only through an issued basis",
      _r.basis is not None and _r.basis.status is BasisStatus.EXECUTABLE,
      "preflight returned %s" % _r.state.value)
def _basis_in(status):
    p, r = executable(request_id="request.C1")
    r.basis.status = status
    return p, r.basis


for _status in (BasisStatus.DRAFT, BasisStatus.VALIDATED, BasisStatus.BLOCKED,
                BasisStatus.STALE, BasisStatus.SUPERSEDED):
    _p2, _b2 = _basis_in(_status)
    _ok, _ev = refuses(lambda: build_trigger(_b2, _p2, originator="human.a"), ActivationError)
    check(G, "no trigger from a %s basis" % _status.value, _ok, _ev)


G = "C-2 the basis exercising authority"

_p3, _r3 = executable(request_id="request.C2")
_ok, _ev = refuses(lambda: _r3.basis.exercise("decision.external_publication"), GovernanceError)
check(G, "ExecutionBasis.exercise() refuses", _ok, _ev)
_ok, _ev = refuses(lambda: _r3.basis.satisfy_review("review.any"), GovernanceError)
check(G, "ExecutionBasis.satisfy_review() refuses", _ok, _ev)
check(G, "is_approval is a declared false field, not an omission",
      getattr(_r3.basis, "is_approval", None) is False,
      "is_approval=%r" % getattr(_r3.basis, "is_approval", "MISSING"))
check(G, "is_authority is a declared false field, not an omission",
      getattr(_r3.basis, "is_authority", None) is False,
      "is_authority=%r" % getattr(_r3.basis, "is_authority", "MISSING"))
check(G, "a trigger declares itself neither an approval nor a run creation",
      build_trigger(_r3.basis, _p3, originator="human.a").is_approval is False
      and build_trigger(_r3.basis, _p3, originator="human.a").creates_run is False)


G = "C-3 planner-created governed records"

for _record in ("decision_record", "review_instance", "approval_state"):
    _ok, _ev = refuses(
        lambda r=_record: run_preflight(plan(request_id="request.C3",
                                             injected_governed_records=(r,))),
        GovernanceError)
    check(G, "preflight refuses an injected %s" % _record, _ok, _ev)

check(G, "no requirement object carries a satisfied or exercised default of true",
      ReviewRequirement("review.x", "why").satisfied is False
      and DecisionRequirement("decision.x", "why").exercised is False)
check(G, "no implementation module writes a Decision Record or Review Instance",
      not re.search(r"(?i)\b(create|write|issue|record)_(decision_record|review_instance)\b",
                    _impl_text),
      "no creation path exists for either record")


G = "C-4 material change not invalidating the basis"

_store = ActivationStore()
_p4, _r4 = executable(request_id="request.C4")
_store.issue(_r4.basis)
_changed = plan(request_id="request.C4", objective="A materially different objective")
_stale = _store.invalidate_on_material_change("request.C4", _changed.material_digest())
check(G, "a material change makes the live basis STALE",
      _stale and _store.live_basis("request.C4") is None,
      "stale=%r" % _stale)
check(G, "the stale basis stays readable rather than being deleted",
      len(_store.history("request.C4")) == 1
      and _store.history("request.C4")[0].status is BasisStatus.STALE)
_presentation = plan(request_id="request.C4", request_text="Reworded, same plan.")
check(G, "a presentation-only change does not change the material digest",
      _presentation.material_digest() == _p4.material_digest(),
      "request_text is excluded from MATERIAL_FIELDS")
check(G, "every field whose change alters scope or authority is material",
      set(("scope_ref", "objective", "deliverables", "criticality", "execution_mode",
           "role_requirements", "review_requirements", "decision_requirements",
           "evidence_requirements", "workflow_ref")).issubset(set(PlannerOutput.MATERIAL_FIELDS)),
      "MATERIAL_FIELDS=%r" % (PlannerOutput.MATERIAL_FIELDS,))


G = "C-5 unapproved or stale Workflow under MATCH"

_ok, _ev = refuses(lambda: run_preflight(plan(
    request_id="request.C5", execution_mode=ExecutionMode.MATCH, work_plan=None,
    workflow_ref="workflow.invented_by_the_planner@1")), ActivationError)
_r5 = None
if not _ok:
    _r5 = run_preflight(plan(request_id="request.C5", execution_mode=ExecutionMode.MATCH,
                             work_plan=None, workflow_ref="workflow.invented@1"))
    _ok = _r5.state is PlannerState.BLOCKED and _r5.basis is None
    _ev = "state=%s basis=%r" % (_r5.state.value, _r5.basis)
check(G, "an unapproved Workflow identity never reaches an Execution Basis", _ok, _ev)

_r5b = run_preflight(plan(request_id="request.C5b", execution_mode=ExecutionMode.MATCH,
                          work_plan=None, workflow_ref="%s@99" % a_workflow()))
check(G, "an approved Workflow at an unapproved version is BLOCKED",
      _r5b.state is PlannerState.BLOCKED and _r5b.basis is None,
      "state=%s" % _r5b.state.value)
_r5c = run_preflight(plan(request_id="request.C5c", execution_mode=ExecutionMode.MATCH,
                          work_plan=None, workflow_ref="%s@1" % a_workflow()))
check(G, "an approved Workflow at its approved version proceeds",
      _r5c.state is PlannerState.VALIDATED, _r5c.detail)


G = "C-6 unregistered Role or Skill made assignable"

_r6 = run_preflight(plan(request_id="request.C6",
                         role_requirements=(RoleRequirement("role.invented", "a conclusion"),)))
check(G, "an unregistered Role blocks",
      _r6.state is PlannerState.BLOCKED and _r6.basis is None, _r6.detail)
_r6b = run_preflight(plan(
    request_id="request.C6b",
    skill_requirements=(SkillRequirement("skill.invented", a_role()),)))
check(G, "an unregistered Skill blocks",
      _r6b.state is PlannerState.BLOCKED and _r6b.basis is None, _r6b.detail)
check(G, "no registry view exposes a write path",
      not re.search(r"(?i)\bdef\s+(add|register|create|insert|approve)_", read(
          os.path.join(IMPL, "registries.py"))),
      "registries.py is read-only by construction")
check(G, "the approved 59-role universe is unchanged by this phase",
      len(registries.approved_roles()) == 59,
      "derived count=%d" % len(registries.approved_roles()))


G = "C-7 separation of duties"

_reviewer_role = a_role()
_r7 = run_preflight(
    plan(request_id="request.C7", criticality=Criticality.CRITICAL,
         review_requirements=(ReviewRequirement(
             sorted(registries.approved_review_profiles())[0], "final critical review"),)),
    author_identity="human.alice", reviewer_identity="human.alice")
check(G, "author as final critical reviewer blocks",
      _r7.state is PlannerState.BLOCKED and _r7.basis is None, _r7.detail)
_r7b = run_preflight(
    plan(request_id="request.C7b", criticality=Criticality.CRITICAL,
         review_requirements=(ReviewRequirement(
             sorted(registries.approved_review_profiles())[0], "final critical review"),)),
    author_identity="human.alice", reviewer_identity="human.bob")
check(G, "a distinct reviewer does not trip the SoD gate",
      "sod" not in (_r7b.detail or "").lower(), _r7b.detail)


G = "C-8 clarification-required entering execution"

_r8 = run_preflight(plan(
    request_id="request.C8",
    clarifications=(ClarificationRequirement("Which entity is the client?", True),)))
check(G, "a blocking clarification yields CLARIFICATION_REQUIRED",
      _r8.state is PlannerState.CLARIFICATION_REQUIRED, _r8.state.value)
check(G, "and issues no Execution Basis at all", _r8.basis is None, repr(_r8.basis))
_r8b = run_preflight(plan(
    request_id="request.C8b",
    clarifications=(ClarificationRequirement("Prefer bullets or prose?", False, "prose"),)))
check(G, "a non-blocking clarification does not block",
      _r8b.state is PlannerState.VALIDATED, _r8b.detail)


G = "C-9 duplicate request creating duplicate lineage"

_store9 = ActivationStore()
_p9, _r9 = executable(request_id="request.C9")
_store9.issue(_r9.basis)
_key = idempotency_key(_p9)
_lineage_a, _created_a = _store9.record_trigger(_key, _r9.basis.ref)
_lineage_b, _created_b = _store9.record_trigger(_key, _r9.basis.ref)
check(G, "the same request at the same material version yields one lineage",
      _created_a is True and _created_b is False and _lineage_a == _lineage_b,
      "%s created=%r then %r" % (_lineage_a, _created_a, _created_b))
_p9b, _r9b = executable(request_id="request.C9")
_reused = _store9.issue(_r9b.basis)
check(G, "re-issuing on unchanged inputs reuses the live basis rather than minting a second",
      _reused.ref == _r9.basis.ref and len(_store9.history("request.C9")) == 1,
      "history=%d" % len(_store9.history("request.C9")))
check(G, "the idempotency key binds scope, request and material version",
      idempotency_key(plan(request_id="request.C9", scope_ref="scope.project.beta",
                           scope_ancestry=("scope.org.root", "scope.project.beta")))
      != _key)


G = "C-10 Work Plan promoted to reusable Workflow"

_ok, _ev = refuses(lambda: WorkPlan("workflow.pretending_to_be_a_plan", 1,
                                    (PlanStage("S1", None, (), False, "x"),)), GovernanceError)
check(G, "a Work Plan may not be rendered in the workflow identifier space", _ok, _ev)
_store10 = ActivationStore()
_cand = _store10.observe_composed_pattern("sig-abc", "work_plan.V@1")
_store10.observe_composed_pattern("sig-abc", "work_plan.W@1")
check(G, "a repeated COMPOSE shape emits a PROPOSED candidate only",
      _cand["status"] == "PROPOSED" and _cand["is_approved"] is False
      and _cand["is_matchable"] is False, repr(_cand))
check(G, "and one candidate, not one per observation", len(_store10.candidates) == 1)
check(G, "the store has no method that registers a Workflow or approves a candidate",
      not re.search(r"(?i)\bdef\s+\w*(register|approve|promote)\w*\(", read(
          os.path.join(IMPL, "store.py"))),
      "no promotion path exists")
check(G, "a candidate identity is never a workflow identity",
      not _cand["candidate_id"].startswith("workflow."),
      _cand["candidate_id"])


G = "C-11 caller-injected governed records in the handoff"

_p11, _r11 = executable(request_id="request.C11")
for _record in FORBIDDEN_IN_TRIGGER:
    _bad = plan(request_id="request.C11", injected_governed_records=(_record,))
    _ok, _ev = refuses(lambda b=_bad: build_trigger(_r11.basis, b, originator="human.a"),
                       GovernanceError, ActivationError)
    check(G, "the trigger builder refuses a pre-formed %s" % _record, _ok, _ev)

_trigger = build_trigger(_r11.basis, _p11, originator="human.a")
_trigger_fields = set(_trigger.__dataclass_fields__)
check(G, "no governed-record field appears on the envelope at all",
      not (_trigger_fields & set(FORBIDDEN_IN_TRIGGER)),
      "envelope carries %d fields, none of them a governed record" % len(_trigger_fields))
check(G, "the envelope is the approved CreateWorkflowRun command, not a bespoke call",
      _trigger.command == "CreateWorkflowRun", _trigger.command)
check(G, "all seven approved intake checks are answerable from the envelope",
      set(_trigger.intake_answers()) == set(range(1, 8))
      and all(_trigger.intake_answers()[i] != "" for i in (1, 2, 3, 4, 5, 6)),
      repr(sorted(_trigger.intake_answers())))
check(G, "a planned spec is never a work item",
      all(s.spec_id.startswith("planned_work_item_spec.")
          for s in _trigger.planned_work_item_specs)
      and not any(s.spec_id.startswith("work_item.")
                  for s in _trigger.planned_work_item_specs))
_ok, _ev = refuses(lambda: PlannedWorkItemSpec(
    "work_item.001", "S1", None, (), (), "x", (), (), "ROUTINE", False), GovernanceError)
check(G, "and the spec type refuses work_item identity outright", _ok, _ev)


G = "C-12 stale or mismatched scope or version lineage"

_p12, _r12 = executable(request_id="request.C12")
_other = plan(request_id="request.C12", objective="A materially different objective")
_ok, _ev = refuses(lambda: build_trigger(_r12.basis, _other, originator="human.a"),
                   ActivationError)
check(G, "a basis may not produce a trigger for planning inputs it was not issued against",
      _ok, _ev)
check(G, "the basis binds the implementation-spec version it was validated under",
      _r12.basis.implementation_spec_version == IMPLEMENTATION_SPEC_VERSION,
      _r12.basis.implementation_spec_version)
check(G, "the basis binds scope and its ancestry, not scope alone",
      _r12.basis.scope_ref == _p12.scope_ref
      and tuple(_r12.basis.scope_ancestry) == _p12.scope_ancestry)

_store12 = ActivationStore()
_pA, _rA = executable(request_id="request.C12v")
_store12.issue(_rA.basis)
_store12.invalidate_on_material_change("request.C12v", "a-different-digest")
_pB, _rB = executable(request_id="request.C12v", objective="A materially different objective")
_store12.issue(_rB.basis)
check(G, "a basis issued after a STALE one is version 2 and links what it supersedes",
      _rB.basis.version == 2 and _rB.basis.supersedes == _rA.basis.ref,
      "v=%d supersedes=%r" % (_rB.basis.version, _rB.basis.supersedes))
check(G, "and the superseded record is still readable",
      len(_store12.history("request.C12v")) == 2)


# =========================================================== 3. prose agrees with behaviour

G = "prose"


def says(name, *phrases):
    body = flat(doc(name))
    return [p for p in phrases if flat(p) not in body]


#: Keyed on TWO spellings of the same statement rather than one. A check that demanded a
#: single phrase would read a rule restated more strongly as a failure - the harness failure
#: pattern named in phase-16-self-check.md §4.
_missing = says("execution-basis-contract.md", "may accept", "is_approval", "is_authority")
if not any(flat(p) in flat(doc("execution-basis-contract.md"))
           for p in ("authorises entry", "entry to intake")):
    _missing.append("authorises entry / entry to intake")
check(G, "the basis contract states what the object authorises and declares its false fields",
      not _missing, "missing: %r" % _missing)

_missing = says("po-4-and-po-12-closure.md",
                "PROPOSED", "intake may accept", "PO-16-A", "PO-16-E")
check(G, "the closure document states the proposal status and records its new open items",
      not _missing, "missing: %r" % _missing)

_closure = flat(doc("po-4-and-po-12-closure.md"))
check(G, "the closure document does not claim either obligation is closed outright",
      "neither is closed by this package alone" in _closure,
      "PO-4 and PO-12 are reported as proposed closures")

_missing = says("workflow-resolution-contract.md", "work_plan.", "workflow.")
check(G, "the resolution contract keeps the two identifier spaces distinct in writing",
      not _missing, "missing: %r" % _missing)

_missing = says("idempotency-versioning-replay.md",
                "most recently issued", "append-only", "material_digest")
check(G, "the idempotency document states the lineage rule the store implements",
      not _missing, "missing: %r" % _missing)

_missing = says("observability-audit-provenance.md",
                "operational", "governed", "provenance")
check(G, "the observability document separates operational from governed events",
      not _missing, "missing: %r" % _missing)

check(G, "no package document claims production readiness",
      not any(re.search(r"(?i)production[- ]ready|ready for production|is approved for use",
                        doc(n)) for n in PACKAGE_DOCS),
      "no readiness claim in any of the %d documents" % len(PACKAGE_DOCS))

check(G, "no package document claims to approve, register or grant anything",
      not any(re.search(r"(?i)\b(hereby|we hereby)\s+(approve|grant|register)\b", doc(n))
              for n in PACKAGE_DOCS))

_self = flat(doc("phase-16-self-check.md"))
check(G, "the self-check disclaims governance authority",
      "never governance authority" in _self or "not governance authority" in _self,
      "phase-16-self-check.md")
check(G, "the self-check names at least one limit of its own assurance",
      "cannot" in _self or "limit" in _self)


# =========================================================== 4. containment

G = "containment"

check(G, "Phase 16 adds nothing under architecture/",
      not any(p.startswith("phase-16") or p.startswith("phase_16")
              for p in os.listdir(os.path.join(REPO, "architecture"))
              if os.path.isdir(os.path.join(REPO, "architecture"))),
      "approved architecture/ untouched")
check(G, "Phase 16 adds nothing under planning/ (the approved Phase 15 package)",
      not any("phase-16" in p or "phase_16" in p
              for p in os.listdir(os.path.join(REPO, "planning"))))
check(G, "Phase 16 adds nothing under implementation-spec/ (approved Phase 14)",
      not any("phase-16" in p or "phase_16" in p
              for p in os.listdir(os.path.join(REPO, "implementation-spec"))))
check(G, "this validator disclaims governance authority",
      "NEVER GOVERNANCE AUTHORITY" in read(os.path.abspath(__file__)))
check(G, "no Phase 16 file is written under validation/ beyond this pair",
      sorted(p for p in os.listdir(HERE) if "phase_16" in p)
      == ["phase_16_mutation_probes.py", "phase_16_validation.py"],
      "validation/ carries exactly the Phase 16 validator and its probes")


# =========================================================== main


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
