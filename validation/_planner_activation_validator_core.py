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

STRUCTURE. Every check lives inside a registered section, and a section that raises records a
FAIL naming the exception rather than killing the run. That matters for the mutation harness:
a mutation that makes a check blow up is a DETECTION, and must be distinguishable from a
harness that could not run at all. With `--json` this file writes valid JSON to stdout and
nothing else, so the harness can tell those two apart by parsing rather than by exit code.

It modifies no approved validator and reads no approved artifact except its own registries and
approval records, read-only.
"""

import json
import os
import re
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
#: The mutation probes run this validator against a throwaway COPY of the package, so the repo
#: root is overridable. Nothing else reads it, and it never points at the real tree during a
#: probe run - a probe that mutated the working tree would be a destructive test, not a test.
REPO = os.environ.get("PHASE_16_REPO_ROOT") or os.path.dirname(HERE)
PKG = os.path.join(REPO, "planner-activation")
IMPL = os.path.join(REPO, "implementation", "phase-16")

sys.path.insert(0, IMPL)

RESULTS = []
SECTIONS = []

#: Exceptions that mean THE HARNESS could not run, as opposed to the implementation under test
#: behaving differently. Only these become RUNNER_ERROR. `RuntimeError` is here deliberately:
#: it is the class the probe harness injects to prove that an unexpected runtime fault is never
#: counted as a semantic detection.
INFRASTRUCTURE_FAULTS = (
    ImportError, OSError, SyntaxError, RuntimeError, MemoryError, RecursionError, SystemError,
)


def section(name):
    def register(fn):
        SECTIONS.append((name, fn))
        return fn
    return register


def check(group, name, passed, evidence=""):
    RESULTS.append({"group": group, "name": name, "pass": bool(passed), "evidence": evidence})


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


def refuses(fn, *exc):
    """Did the call refuse with one of the expected governance exceptions?

    A rule that can be violated and merely logged is not enforced, so a check that accepted a
    returned error object instead of a raised one would be testing nothing.
    """
    try:
        fn()
    except exc as err:
        return True, "%s: %s" % (type(err).__name__, str(err)[:110])
    except Exception as err:
        return False, "wrong exception %s: %s" % (type(err).__name__, err)
    return False, "the call returned instead of refusing"


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
    "registry-eligibility-contract.md",
    "idempotency-versioning-replay.md",
    "observability-audit-provenance.md",
    "po-4-and-po-12-closure.md",
    "phase-16-self-check.md",
)

IMPL_MODULES = ("domain.py", "registries.py", "preflight.py", "handoff.py", "store.py")


# =========================================================== imports

import dataclasses                                                        # noqa: E402
import registries                                                         # noqa: E402
from domain import (                                                      # noqa: E402
    ActivationError, BasisStatus, BlockReason, ClarificationRequirement, Criticality,
    DecisionRequirement, EvidenceRequirement, ExecutionMode, GovernanceError,
    IMPLEMENTATION_SPEC_VERSION, PlanStage, PlannerOutput, PlannerState, PrerequisiteState,
    ReviewRequirement, RoleRequirement, SkillRequirement, WorkMode, WorkPlan,
)
from handoff import (                                                     # noqa: E402
    FORBIDDEN_IN_TRIGGER, PlannedWorkItemSpec, build_trigger, idempotency_key,
)
from preflight import run_preflight                                       # noqa: E402
from store import ActivationStore                                         # noqa: E402


def a_role():
    return sorted(registries.approved_roles())[0]


def a_workflow_ref():
    wf = sorted(registries.approved_workflows())[0]
    return "%s@%s" % (wf, registries.approved_workflows()[wf])


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


class simulated_individual_skill_approval(object):
    """A LABELLED TEST DOUBLE that temporarily makes named Skills individually approved.

    It creates no approval and asserts none: it exists because the downstream Skill gates -
    Role compatibility, wrong-Role binding - live BEHIND the individual-approval gate, and with
    no Skill individually approved in the repository today those gates are unreachable and
    would silently lose coverage. Every use is explicit, scoped to one check, and restored.

    It is never used to claim a Skill is approved. The check that asks that question reads the
    real `approved_skills()` and expects the empty set.
    """

    def __init__(self, *skills):
        self.skills = set(skills)
        self._original = None

    def __enter__(self):
        self._original = registries.approved_skills
        registries.approved_skills = lambda: set(self.skills)
        return self

    def __exit__(self, *_exc):
        registries.approved_skills = self._original
        return False


def a_mapped_pair():
    """(role, skill) that the AUTHORITATIVE MAPPING RECORDS positively relate.

    Drawn from `carded_skills()`, never from `approved_skills()`: a mapping is evidence of
    applicability, and carries no implication of execution eligibility whatsoever.
    """
    mappings = registries.role_skill_mappings()
    for role_ref in sorted(registries.approved_roles()):
        for skill_ref in sorted(registries.carded_skills()):
            if mappings.get(role_ref, {}).get(skill_ref) in \
                    registries.COMPATIBLE_RELATIONSHIPS:
                return role_ref, skill_ref
    return None, None


def issued(**overrides):
    """A plan, its issuing store, and the ISSUED basis. Never the unissued candidate."""
    p = plan(**overrides)
    store = ActivationStore()
    result = run_preflight(p)
    if result.basis is None:
        raise AssertionError("preflight refused a fixture plan: %s" % (result.detail,))
    return p, store, store.issue(result.basis)


# =========================================================== 1. package shape


@section("package")
def _package():
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

    check(G, "the package declares itself PROPOSED and unapproved",
          "nothing in this package is approved" in flat(doc("README.md")),
          "README.md governance banner")
    check(G, "every package document is named in the README map",
          all(n in doc("README.md") for n in PACKAGE_DOCS if n != "README.md"),
          "README.md §3")

    impl_text = "\n".join(read(os.path.join(IMPL, m)) for m in IMPL_MODULES)
    check(G, "the reference implementation imports no third-party module",
          not re.search(r"(?m)^\s*(import|from)\s+(?!os|sys|re|json|hashlib|dataclasses|"
                        r"typing|enum|collections|itertools|__future__|domain|registries|"
                        r"preflight|handoff|store)\w", impl_text),
          "standard library plus sibling modules only")
    # Keyed on the IMPORT, not on the bare word: "two different requests can..." in a comment
    # is English, and a check that read it as a network client was failing on prose.
    check(G, "the reference implementation opens no network or database connection",
          not re.search(r"(?m)^\s*(?:import|from)\s+"
                        r"(requests|urllib|socket|http|httpx|psycopg|sqlite3|supabase|boto3)\b",
                        impl_text),
          "no client library is imported anywhere in the implementation")


# =========================================================== 2. registry eligibility (B1)


#: Exactly the three IDs the previous display-name slugger invented out of "Asset O&M",
#: "ESG / E&S" and "FP&A". None of them is declared by any Role Card.
MISPARSED_ROLE_IDS = (
    "role.asset_o_m_technical_operations_specialist",
    "role.esg_e_s_specialist",
    "role.fp_a_management_finance_specialist",
)
DECLARED_ROLE_IDS = (
    "role.asset_om_technical_operations_specialist",
    "role.esg_es_specialist",
    "role.fpa_management_finance_specialist",
)
#: Identities that appear in an approved document as a candidate, a consolidation-group entry
#: or a prose reference, and are NOT carded. Mention-based parsing counted every one of them.
UNCARDED_MENTIONS = (
    ("review", "review.legal_regulatory"),
    ("decision", "decision.stage_gate_progression_routine"),
    ("workflow", "workflow.feasibility_study_preparation"),
    ("skill", "skill.scope_definition"),
    ("skill", "skill.legal_source_currency_check"),      # retired; named by a Supersedes line
)


@section("C-0 registry eligibility")
def _registry_eligibility():
    G = "C-0 registry eligibility"
    roles = registries.approved_roles()
    check(G, "the approved Role universe is exactly 59", len(roles) == 59, str(len(roles)))

    for invented in MISPARSED_ROLE_IDS:
        check(G, "the slugged id %s is not eligible" % invented, invented not in roles)
    for declared in DECLARED_ROLE_IDS:
        check(G, "the declared id %s is eligible" % declared, declared in roles)

    for kind, identity in UNCARDED_MENTIONS:
        registered = {
            "review": registries.approved_review_profiles(),
            "decision": registries.approved_decision_rights(),
            "workflow": set(registries.approved_workflows()),
            # Skills are checked against the CARDED set, which is the wider of the two: an id
            # absent from the carded set is absent from the approved set a fortiori, and
            # checking the empty set would prove nothing.
            "skill": registries.carded_skills(),
        }[kind]
        check(G, "the uncarded %s %s is not eligible" % (kind, identity),
              identity not in registered)

    for kind, identities in (("role", roles),
                             ("skill", registries.approved_skills()),
                             ("review", registries.approved_review_profiles()),
                             ("decision", registries.approved_decision_rights()),
                             ("workflow", set(registries.approved_workflows()))):
        missing = [i for i in sorted(identities) if registries.card_path(kind, i) is None]
        check(G, "every eligible %s resolves to a declaring card" % kind, not missing,
              "uncarded: %r" % missing)

    for kind, expected, known in (
            ("review", 6, "review.security"),
            ("decision", 8, "decision.external_publication"),
            ("workflow", 4, "workflow.software_change_delivery")):
        registered = {
            "review": registries.approved_review_profiles(),
            "decision": registries.approved_decision_rights(),
            "workflow": set(registries.approved_workflows()),
        }[kind]
        check(G, "the carded %s set is the %d its approval record names" % (kind, expected),
              len(registered) == expected, "%d: %r" % (len(registered), sorted(registered)))
        check(G, "%s is eligible" % known, known in registered)

    # -- CARDED is not APPROVED --------------------------------------------------------
    #
    # This block used to assert `len(approved_skills()) == 6`, reading the Phase 4 architecture
    # approval as if it individually approved the six exemplar Skill cards. It does not, and
    # says so in terms: cards "may remain individually PROPOSED", and the phase decision "must
    # not be interpreted as a mass status promotion". So the two questions are separated here,
    # and the answer to the second one is currently NONE.
    carded = registries.carded_skills()
    approved = registries.approved_skills()
    check(G, "the six Phase 4 exemplar Skill cards exist as declared cards",
          len(carded) == 6 and "skill.source_verification" in carded,
          "%d: %r" % (len(carded), sorted(carded)))
    check(G, "carded Skills are NOT individually approved by the Phase 4 architecture approval",
          approved == set(),
          "approved_skills() = %r; the Phase 4 record approves the architecture and denies "
          "mass individual promotion" % sorted(approved))
    check(G, "every individually approved Skill, if any, is also carded",
          approved <= carded, "%r" % sorted(approved - carded))

    versions = registries.approved_workflows()
    check(G, "every approved Workflow Card declares version 0.1, the current carded state",
          set(versions.values()) == {"0.1"}, repr(versions))
    check(G, "each approved Workflow carries the version its card declares",
          versions and all(re.match(r"^\d+\.\d+$", v) for v in versions.values()),
          repr(versions))
    check(G, "no Workflow version is the invented integer 1",
          all(v != 1 and v != "1" for v in versions.values()))

    check(G, "approval evidence is required per kind, and named",
          all(k.approval_record and k.approved_scope_phrase
              for k in registries.KINDS.values()),
          ", ".join(sorted(registries.KINDS)))
    # The Skill KIND still carries a phase-level record for symmetry, but that record is NOT
    # what decides Skill eligibility - see C-15. This check exists so nobody reads the table
    # above as meaning it is.
    check(G, "the Skill kind's phase-level record does not decide Skill eligibility",
          registries.approved_skills() == set()
          and registries._approval_is_recorded(registries.KINDS["skill"]),
          "the phase record reads as present, and the registry is still empty")
    check(G, "the implementation-spec version names the approved Phase 14 baseline",
          IMPLEMENTATION_SPEC_VERSION == "phase-14@ba9e3fee", IMPLEMENTATION_SPEC_VERSION)
    # Source-level, deliberately: the invariant's whole job is to fail at IMPORT, so a check
    # that only compared the two field sets would pass whether or not it still runs.
    check(G, "the planner-field classification invariant still runs at import",
          re.search(r"(?m)^_assert_every_planner_field_is_classified\(\)$",
                    read(os.path.join(IMPL, "domain.py"))) is not None)
    check(G, "no registry view exposes a write path",
          not re.search(r"(?m)^def\s+(add|register|create|insert|approve|promote)_",
                        read(os.path.join(IMPL, "registries.py"))),
          "registries.py is read-only by construction")

    # A Skill is compatible with a Role only where the authoritative mapping records say so.
    mappings = registries.role_skill_mappings()
    check(G, "Role-to-Skill compatibility is read from the mapping records",
          len(mappings) == 59, "roles with a mapping: %d" % len(mappings))
    # Found from the mapping records themselves, not guessed: a pair that appears in NO record
    # is the case the rule exists for, and a check that quietly tested a MAPPED pair would
    # prove the opposite of its name.
    absent = [(s_, r_) for s_ in sorted(registries.carded_skills())
              for r_ in sorted(registries.approved_roles())
              if s_ not in mappings.get(r_, {})]
    check(G, "the mapping records leave some carded Skill/Role pairs unrecorded",
          bool(absent), "%d unrecorded pairs" % len(absent))
    if absent:
        skill_ref, role_ref = absent[0]
        ok, why = registries.skill_is_compatible_with_role(skill_ref, role_ref)
        check(G, "a pair no mapping record names is not compatible",
              ok is False and "no authoritative" in why, why)
    check(G, "PROHIBITED_IN_CONTEXT is never a compatible relationship",
          "PROHIBITED_IN_CONTEXT" not in registries.COMPATIBLE_RELATIONSHIPS,
          repr(registries.COMPATIBLE_RELATIONSHIPS))
    prohibited = [(sk, ro) for ro, entries in mappings.items()
                  for sk, rel in entries.items() if rel == "PROHIBITED_IN_CONTEXT"]
    if prohibited:
        skill_ref, role_ref = prohibited[0]
        ok, why = registries.skill_is_compatible_with_role(skill_ref, role_ref)
        check(G, "a PROHIBITED_IN_CONTEXT pair is not compatible", ok is False, why)


# =========================================================== 3. the twelve classes


@section("C-1 COMPOSE executable without a basis")
def _c1():
    G = "C-1 COMPOSE executable without a basis"
    p, store, basis = issued()
    check(G, "a COMPOSE plan reaches EXECUTABLE only through an issued basis",
          basis.status is BasisStatus.EXECUTABLE, basis.status.value)
    for status in (BasisStatus.DRAFT, BasisStatus.VALIDATED, BasisStatus.BLOCKED,
                   BasisStatus.STALE, BasisStatus.SUPERSEDED):
        ok, ev = refuses(lambda s=status: build_trigger(basis.with_status(s), p,
                                                        originator="human.a", store=store),
                         ActivationError)
        check(G, "no trigger from a %s basis" % status.value, ok, ev)
    candidate = run_preflight(p).basis
    ok, ev = refuses(lambda: build_trigger(candidate, p, originator="human.a",
                                           store=ActivationStore()), ActivationError)
    check(G, "no trigger from a basis that was never issued", ok, ev)


@section("C-2 the basis exercising authority")
def _c2():
    G = "C-2 the basis exercising authority"
    p, store, basis = issued(request_id="request.C2")
    ok, ev = refuses(lambda: basis.exercise("decision.external_publication"), GovernanceError)
    check(G, "ExecutionBasis.exercise() refuses", ok, ev)
    ok, ev = refuses(lambda: basis.satisfy_review("review.any"), GovernanceError)
    check(G, "ExecutionBasis.satisfy_review() refuses", ok, ev)
    check(G, "is_approval is a declared false field, not an omission",
          getattr(basis, "is_approval", None) is False)
    check(G, "is_authority is a declared false field, not an omission",
          getattr(basis, "is_authority", None) is False)
    for field in ("is_approval", "is_authority"):
        ok, ev = refuses(
            lambda f=field: ActivationStore().issue(
                dataclasses.replace(run_preflight(p).basis, **{f: True})), GovernanceError)
        check(G, "a basis claiming %s is never issued" % field, ok, ev)
        ok, ev = refuses(
            lambda f=field: build_trigger(dataclasses.replace(basis, **{f: True}), p,
                                          originator="human.a", store=store),
            ActivationError, GovernanceError)
        check(G, "and one claiming %s produces no trigger" % field, ok, ev)
    trigger = build_trigger(basis, p, originator="human.a", store=store)
    check(G, "a trigger declares itself neither an approval nor a run creation",
          trigger.is_approval is False and trigger.creates_run is False)


@section("C-3 planner-created governed records")
def _c3():
    G = "C-3 planner-created governed records"
    for record in ("decision_record", "review_instance", "approval_state"):
        ok, ev = refuses(
            lambda r=record: run_preflight(plan(request_id="request.C3",
                                                injected_governed_records=(r,))),
            GovernanceError)
        check(G, "preflight refuses an injected %s" % record, ok, ev)
    check(G, "no requirement object carries a satisfied or exercised default of true",
          ReviewRequirement("review.x", True).satisfied is False
          and DecisionRequirement("decision.x", "why").exercised is False)
    impl_text = "\n".join(read(os.path.join(IMPL, m)) for m in IMPL_MODULES)
    check(G, "no implementation module writes a Decision Record or Review Instance",
          not re.search(r"(?i)\b(create|write|issue|record)_(decision_record|review_instance)\b",
                        impl_text))


@section("C-4 material change not invalidating the basis")
def _c4():
    G = "C-4 material change not invalidating the basis"
    p, store, basis = issued(request_id="request.C4")
    changed = plan(request_id="request.C4", objective="A materially different objective")
    stale = store.invalidate_on_material_change("request.C4", changed.material_digest())
    check(G, "a material change makes the live basis STALE",
          stale and store.live_basis("request.C4") is None, "stale=%r" % stale)
    check(G, "the stale basis stays readable rather than being deleted",
          store.issued(basis.ref) is not None
          and store.issued(basis.ref).status is BasisStatus.STALE)
    check(G, "a presentation-only change does not change the material digest",
          plan(request_id="request.C4",
               request_text="Reworded, same plan.").material_digest() == p.material_digest())

    # B2: every load-bearing family, one case each, each asserted to INVALIDATE rather than
    # merely to differ. The first four were outside the digest entirely.
    families = {
        "clarifications": dict(clarifications=(
            ClarificationRequirement("Bullets or prose?", False, "prose"),)),
        "clarification default": dict(clarifications=(
            ClarificationRequirement("Bullets or prose?", False, "bullets"),)),
        "scope ancestry": dict(
            scope_ancestry=("scope.org.root", "scope.programme.x", "scope.project.alpha")),
        "orchestrator policy": dict(orchestrator_policy_ref="policy.strict@2"),
        "stage expected_artifact": dict(work_plan=WorkPlan("work_plan.V", 1, (
            PlanStage("S1", a_role(), (), False, "a materially different artifact"),
            PlanStage("S2", None, ("S1",), True, "")))),
        "declared open items": dict(unknown_fields=("residency",)),
        "evidence timing": dict(evidence_requirements=(EvidenceRequirement(
            "artifact.x@1", PrerequisiteState.RESOLVED, required_before_first_act=False),)),
    }
    for label, override in families.items():
        p2, store2, basis2 = issued(request_id="request.C4f")
        after = plan(request_id="request.C4f", **override)
        stale2 = store2.invalidate_on_material_change("request.C4f", after.material_digest())
        ok, ev = refuses(lambda: build_trigger(basis2, after, originator="human.a",
                                               store=store2), ActivationError)
        check(G, "a change to %s invalidates the issued basis" % label,
              bool(stale2) and ok, ev)

    declared = {f.name for f in dataclasses.fields(PlannerOutput)}
    check(G, "every planner field is classified as material, presentation, identity or refused",
          declared == PlannerOutput.classified_fields(),
          "unclassified: %r" % sorted(declared - PlannerOutput.classified_fields()))
    check(G, "only request_text is presentation-only",
          PlannerOutput.PRESENTATION_ONLY_FIELDS == ("request_text",),
          repr(PlannerOutput.PRESENTATION_ONLY_FIELDS))


@section("C-5 unapproved or stale Workflow under MATCH")
def _c5():
    G = "C-5 unapproved or stale Workflow under MATCH"
    r = run_preflight(plan(request_id="request.C5", execution_mode=ExecutionMode.MATCH,
                           work_plan=None, workflow_ref="workflow.invented@0.1"))
    check(G, "an unapproved Workflow identity never reaches an Execution Basis",
          r.state is PlannerState.BLOCKED and r.basis is None, r.state.value)
    r = run_preflight(plan(request_id="request.C5b", execution_mode=ExecutionMode.MATCH,
                           work_plan=None,
                           workflow_ref=a_workflow_ref().split("@")[0] + "@99.9"))
    check(G, "an approved Workflow at an unapproved version is BLOCKED",
          r.state is PlannerState.BLOCKED and r.basis is None, r.state.value)
    r = run_preflight(plan(request_id="request.C5c", execution_mode=ExecutionMode.MATCH,
                           work_plan=None, workflow_ref=a_workflow_ref().split("@")[0] + "@1"))
    check(G, "the previously invented integer version 1 is now BLOCKED",
          r.state is PlannerState.BLOCKED, r.state.value)
    r = run_preflight(plan(request_id="request.C5d", execution_mode=ExecutionMode.MATCH,
                           work_plan=None, workflow_ref=a_workflow_ref()))
    check(G, "an approved Workflow at its declared version proceeds",
          r.state is PlannerState.VALIDATED, r.detail)


@section("C-6 unregistered Role or Skill made assignable")
def _c6():
    G = "C-6 unregistered Role or Skill made assignable"
    # MATCH, so there is no composed plan and no stage-owner guard to mask the result: this
    # isolates the REGISTRY check. Asserting the reason and not merely BLOCKED matters for the
    # same purpose - a plan blocked for some other reason is not this rule working.
    r = run_preflight(plan(request_id="request.C6", execution_mode=ExecutionMode.MATCH,
                           work_plan=None, workflow_ref=a_workflow_ref(),
                           role_requirements=(RoleRequirement("role.invented", "a conclusion"),)))
    check(G, "an unregistered Role blocks, as an unregistered capability",
          r.state is PlannerState.BLOCKED and r.basis is None
          and BlockReason.UNREGISTERED_CAPABILITY in r.reasons, r.detail)
    r = run_preflight(plan(request_id="request.C6b", execution_mode=ExecutionMode.MATCH,
                           work_plan=None, workflow_ref=a_workflow_ref(),
                           skill_requirements=(SkillRequirement("skill.invented", a_role()),)))
    check(G, "an unregistered Skill blocks, as an unregistered capability",
          r.state is PlannerState.BLOCKED and r.basis is None
          and BlockReason.UNREGISTERED_CAPABILITY in r.reasons, r.detail)
    r = run_preflight(plan(request_id="request.C6c", execution_mode=ExecutionMode.MATCH,
                           work_plan=None, workflow_ref=a_workflow_ref(),
                           skill_requirements=(SkillRequirement(
                               sorted(registries.carded_skills())[0], "role.not_a_role"),)))
    check(G, "a Skill claimed for an unresolved Role blocks as unregistered, not as incompatible",
          r.state is PlannerState.BLOCKED
          and BlockReason.UNREGISTERED_CAPABILITY in r.reasons, r.detail)
    check(G, "the approved 59-role universe is unchanged by this phase",
          len(registries.approved_roles()) == 59)


@section("C-7 separation of duties")
def _c7():
    G = "C-7 separation of duties"
    fixture = dict(criticality=Criticality.CRITICAL,
                   review_requirements=(ReviewRequirement(
                       sorted(registries.approved_review_profiles())[0], True),))
    r = run_preflight(plan(request_id="request.C7", **fixture),
                      author_identity="human.alice", reviewer_identity="human.alice")
    check(G, "author as final critical reviewer blocks",
          r.state is PlannerState.BLOCKED and r.basis is None
          and BlockReason.SOD_VIOLATION in r.reasons, r.detail)
    r = run_preflight(plan(request_id="request.C7b", **fixture),
                      author_identity="human.alice", reviewer_identity="human.bob")
    check(G, "a distinct reviewer does not trip the SoD gate",
          BlockReason.SOD_VIOLATION not in r.reasons, r.detail)


@section("C-8 clarification-required entering execution")
def _c8():
    G = "C-8 clarification-required entering execution"
    r = run_preflight(plan(request_id="request.C8", clarifications=(
        ClarificationRequirement("Which entity is the client?", True),)))
    check(G, "a blocking clarification yields CLARIFICATION_REQUIRED",
          r.state is PlannerState.CLARIFICATION_REQUIRED, r.state.value)
    check(G, "and issues no Execution Basis at all", r.basis is None, repr(r.basis))
    r = run_preflight(plan(request_id="request.C8b", clarifications=(
        ClarificationRequirement("Prefer bullets or prose?", False, "prose"),)))
    check(G, "a non-blocking clarification does not block",
          r.state is PlannerState.VALIDATED, r.detail)


@section("C-9 duplicate request creating duplicate lineage")
def _c9():
    G = "C-9 duplicate request creating duplicate lineage"
    p, store, basis = issued(request_id="request.C9")
    key = idempotency_key(p)
    lineage_a, created_a = store.record_trigger(key, basis.ref)
    lineage_b, created_b = store.record_trigger(key, basis.ref)
    check(G, "the same request at the same material version yields one lineage",
          created_a is True and created_b is False and lineage_a == lineage_b,
          "%s created=%r then %r" % (lineage_a, created_a, created_b))
    again = store.issue(run_preflight(plan(request_id="request.C9")).basis)
    check(G, "re-issuing on unchanged inputs reuses the live basis rather than minting a second",
          again.ref == basis.ref and len(store.history("request.C9")) == 1,
          "history=%d" % len(store.history("request.C9")))
    check(G, "the idempotency key binds the scope",
          idempotency_key(plan(request_id="request.C9", scope_ref="scope.project.beta",
                               scope_ancestry=("scope.org.root", "scope.project.beta")))
          != key)
    check(G, "the idempotency key binds the request",
          idempotency_key(plan(request_id="request.C9x")) != key)
    check(G, "the idempotency key binds the MATERIAL PLANNING VERSION",
          idempotency_key(plan(request_id="request.C9",
                               objective="A materially different objective")) != key,
          "a replanned request must not reuse the first plan's lineage")
    ok, ev = refuses(lambda: ActivationStore().record_trigger(key, basis.ref), ActivationError)
    check(G, "a trigger may not be recorded against a basis that store never issued", ok, ev)


@section("C-10 Work Plan promoted to reusable Workflow")
def _c10():
    G = "C-10 Work Plan promoted to reusable Workflow"
    ok, ev = refuses(lambda: WorkPlan("workflow.pretending_to_be_a_plan", 1,
                                      (PlanStage("S1", None, (), False, "x"),)),
                     GovernanceError)
    check(G, "a Work Plan may not be rendered in the workflow identifier space", ok, ev)
    store = ActivationStore()
    candidate = store.observe_composed_pattern("sig-abc", "work_plan.V@1")
    store.observe_composed_pattern("sig-abc", "work_plan.W@1")
    check(G, "a repeated COMPOSE shape emits a PROPOSED candidate only",
          candidate["status"] == "PROPOSED" and candidate["is_approved"] is False
          and candidate["is_matchable"] is False, repr(candidate))
    check(G, "and one candidate, not one per observation", len(store.candidates) == 1)
    check(G, "the store has no method that registers a Workflow or approves a candidate",
          not re.search(r"(?i)\bdef\s+\w*(register|approve|promote)\w*\(",
                        read(os.path.join(IMPL, "store.py"))))
    check(G, "a candidate identity is never a workflow identity",
          not candidate["candidate_id"].startswith("workflow."), candidate["candidate_id"])
    check(G, "a candidate identity is not eligible for MATCH",
          candidate["candidate_id"] not in registries.approved_workflows())


@section("C-11 caller-injected governed records in the handoff")
def _c11():
    G = "C-11 caller-injected governed records in the handoff"
    p, store, basis = issued(request_id="request.C11")
    for record in FORBIDDEN_IN_TRIGGER:
        bad = plan(request_id="request.C11", injected_governed_records=(record,))
        ok, ev = refuses(lambda b=bad: build_trigger(basis, b, originator="human.a",
                                                     store=store),
                         GovernanceError, ActivationError)
        check(G, "the trigger builder refuses a pre-formed %s" % record, ok, ev)
    trigger = build_trigger(basis, p, originator="human.a", store=store)
    # Listed literally, not read from the module. A check that iterates the module's own list
    # is satisfied by DELETING an entry from it, which is precisely the mutation worth catching.
    required_forbidden = ("decision_record", "review_instance", "approval_state",
                          "gate_outcome", "routing_decision", "model_result")
    missing = [f for f in required_forbidden if f not in FORBIDDEN_IN_TRIGGER]
    check(G, "the forbidden-record list still names every governed record it must",
          not missing, "missing: %r" % missing)
    check(G, "no governed-record field appears on the envelope at all",
          not (set(trigger.__dataclass_fields__) & set(FORBIDDEN_IN_TRIGGER)))
    check(G, "the envelope is the approved CreateWorkflowRun command, not a bespoke call",
          trigger.command == "CreateWorkflowRun", trigger.command)
    check(G, "all seven approved intake checks are answerable from the envelope",
          set(trigger.intake_answers()) == set(range(1, 8))
          and all(trigger.intake_answers()[i] != "" for i in (1, 2, 3, 4, 5, 6)))
    check(G, "a planned spec is never a work item",
          all(s.spec_id.startswith("planned_work_item_spec.")
              for s in trigger.planned_work_item_specs))
    ok, ev = refuses(lambda: PlannedWorkItemSpec(
        "work_item.001", "S1", None, (), (), "x", (), (), "ROUTINE", False), GovernanceError)
    check(G, "and the spec type refuses work_item identity outright", ok, ev)


@section("C-12 stale or mismatched scope or version lineage")
def _c12():
    G = "C-12 stale or mismatched scope or version lineage"
    p, store, basis = issued(request_id="request.C12")
    other = plan(request_id="request.C12", objective="A materially different objective")
    ok, ev = refuses(lambda: build_trigger(basis, other, originator="human.a", store=store),
                     ActivationError)
    check(G, "a basis may not produce a trigger for planning inputs it was not issued against",
          ok, ev)
    check(G, "the basis binds the implementation-spec version it was validated under",
          basis.implementation_spec_version == IMPLEMENTATION_SPEC_VERSION,
          basis.implementation_spec_version)
    check(G, "the basis binds scope and its ancestry, not scope alone",
          basis.scope_ref == p.scope_ref and tuple(basis.scope_ancestry) == p.scope_ancestry)

    store2 = ActivationStore()
    first = store2.issue(run_preflight(plan(request_id="request.C12v")).basis)
    store2.invalidate_on_material_change("request.C12v", "a-different-digest")
    changed = plan(request_id="request.C12v", objective="A materially different objective")
    second = store2.issue(run_preflight(changed).basis)
    check(G, "a basis issued after a STALE one is version 2 and links what it supersedes",
          second.version == 2 and second.supersedes == first.ref,
          "v=%d supersedes=%r" % (second.version, second.supersedes))
    lineage = store2.lineage("request.C12v")
    check(G, "and the superseded record is still readable, with what replaced it",
          len(lineage) == 2 and lineage[0][1] == "SUPERSEDED" and lineage[0][2] == second.ref,
          repr(lineage))


# =========================================================== 4. basis integrity (B3)


@section("C-13 basis integrity")
def _c13():
    G = "C-13 basis integrity"
    p, store, basis = issued(
        request_id="request.C13", criticality=Criticality.ENHANCED_DECISION_GRADE,
        review_requirements=(ReviewRequirement(
            sorted(registries.approved_review_profiles())[0], True),),
        decision_requirements=(DecisionRequirement(
            sorted(registries.approved_decision_rights())[0], "publish"),),
        evidence_requirements=(EvidenceRequirement("artifact.x@1",
                                                   PrerequisiteState.RESOLVED),))

    check(G, "an issued basis is a frozen dataclass",
          basis.__dataclass_params__.frozen is True)
    for field, value in (("status", BasisStatus.BLOCKED), ("scope_ref", "scope.other"),
                         ("is_approval", True)):
        ok, ev = refuses(lambda f=field, v=value: setattr(basis, f, v), Exception)
        check(G, "an issued basis refuses an in-place edit of %s" % field, ok, ev)
    ok, ev = refuses(basis.mark_stale, GovernanceError)
    check(G, "a holder may not mark an issued basis stale", ok, ev)
    ok, ev = refuses(lambda: basis.mark_superseded("x"), GovernanceError)
    check(G, "a holder may not mark an issued basis superseded", ok, ev)

    ok, ev = refuses(lambda: build_trigger(basis, p, originator="human.a"), ActivationError)
    check(G, "a trigger may not be built without the issuing store", ok, ev)
    ok, ev = refuses(lambda: build_trigger(
        dataclasses.replace(basis, basis_id="execution_basis.forged"), p,
        originator="human.a", store=store), ActivationError)
    check(G, "a fabricated basis reference is refused", ok, ev)

    tampers = {
        "scope_ref": "scope.project.someone_elses",
        "scope_ancestry": ("scope.org.root",),
        "planning_digest": "0" * 64,
        "implementation_spec_version": "phase-14@deadbeef",
        "orchestrator_policy_ref": "policy.permissive@9",
        "criticality": Criticality.ROUTINE,
        "execution_mode": ExecutionMode.MATCH,
        "review_requirements": (),
        "decision_requirements": (),
        "evidence_requirements": (),
        "role_bindings": ("role.invented",),
        "skill_bindings": ("skill.invented",),
        "work_plan_ref": "work_plan.someone_elses@1",
        "workflow_ref": "workflow.someone_elses@0.1",
        "version": 7,
        "intent_id": "intent.someone_elses",
        "request_id": "request.someone_elses",
    }
    for field, value in tampers.items():
        ok, ev = refuses(lambda f=field, v=value: build_trigger(
            dataclasses.replace(basis, **{f: v}), p, originator="human.a", store=store),
            ActivationError, GovernanceError)
        check(G, "a basis tampered at %s is refused" % field, ok, ev)

    # A basis the STORE has taken to STALE, presented exactly as the store holds it. Nothing
    # disagrees, no seal is broken, no status is misreported: only the EXECUTABLE rule stands
    # between this and a trigger, so this isolates that rule from the integrity checks.
    p2, store2, basis2 = issued(request_id="request.C13s")
    store2.invalidate_on_material_change("request.C13s", "a-different-digest")
    stale_as_stored = store2.issued(basis2.ref)
    check(G, "the store took the basis to STALE",
          stale_as_stored.status is BasisStatus.STALE, stale_as_stored.status.value)
    ok, ev = refuses(lambda: build_trigger(stale_as_stored, p2, originator="human.a",
                                           store=store2), ActivationError)
    check(G, "a basis the store holds as STALE produces no trigger", ok, ev)
    # And the converse: the holder presents EXECUTABLE while the store says STALE. Only the
    # store's lifecycle check stands here.
    ok, ev = refuses(lambda: build_trigger(
        stale_as_stored.with_status(BasisStatus.EXECUTABLE), p2, originator="human.a",
        store=store2), ActivationError)
    check(G, "a basis presented as EXECUTABLE while the store holds it STALE is refused", ok, ev)

    # Cross-request reuse where the digests genuinely match, which is the case a digest
    # comparison alone can never catch.
    left = plan(request_id="request.same.a", intent_id="intent.a")
    right = plan(request_id="request.same.b", intent_id="intent.b")
    check(G, "the cross-request fixture really does produce identical digests",
          left.material_digest() == right.material_digest())
    store3 = ActivationStore()
    basis3 = store3.issue(run_preflight(left).basis)
    ok, ev = refuses(lambda: build_trigger(basis3, right, originator="human.a", store=store3),
                     ActivationError)
    check(G, "a basis issued for one request is refused for another", ok, ev)

    # The two identity bindings, one at a time, so neither can stand in for the other.
    same_intent = plan(request_id="request.same.c", intent_id="intent.a")
    ok, ev = refuses(lambda: build_trigger(basis3, same_intent, originator="human.a",
                                           store=store3), ActivationError)
    check(G, "a differing request identity alone is refused", ok, ev)
    same_request = plan(request_id="request.same.a", intent_id="intent.c")
    ok, ev = refuses(lambda: build_trigger(basis3, same_request, originator="human.a",
                                           store=store3), ActivationError)
    check(G, "a differing intent identity alone is refused", ok, ev)


# =========================================================== 5. composition bindings (B4)


@section("C-14 composition bindings")
def _c14():
    G = "C-14 composition bindings"
    role = a_role()
    r = run_preflight(plan(request_id="request.C14", work_plan=WorkPlan(
        "work_plan.dup", 1, (PlanStage("S1", role, (), False, "draft"),
                             PlanStage("S1", role, (), False, "another artifact"),
                             PlanStage("S2", None, ("S1",), True, "")))))
    check(G, "duplicate stage identities block before a basis is issued",
          r.state is PlannerState.BLOCKED
          and BlockReason.DUPLICATE_STAGE_IDENTITY in r.reasons and r.basis is None, r.detail)

    r = run_preflight(plan(request_id="request.C14b", work_plan=WorkPlan(
        "work_plan.uo", 1, (PlanStage("S1", "role.invented_by_the_planner", (), False, "x"),))))
    check(G, "an unregistered stage owner blocks",
          r.state is PlannerState.BLOCKED
          and BlockReason.UNREGISTERED_CAPABILITY in r.reasons, r.detail)

    other = sorted(registries.approved_roles())[5]
    r = run_preflight(plan(request_id="request.C14c", work_plan=WorkPlan(
        "work_plan.nd", 1, (PlanStage("S1", other, (), False, "x"),))))
    check(G, "a stage owner the plan declares no owned conclusion for blocks",
          r.state is PlannerState.BLOCKED
          and BlockReason.STAGE_OWNER_UNRESOLVED in r.reasons, r.detail)

    r = run_preflight(plan(request_id="request.C14d", work_plan=WorkPlan(
        "work_plan.no", 1, (PlanStage("S1", None, (), False, "x"),))))
    check(G, "a non-gate stage with no effective owner blocks",
          r.state is PlannerState.BLOCKED
          and BlockReason.STAGE_OWNER_UNRESOLVED in r.reasons, r.detail)

    # -- Skill-to-Role binding, in the order the gates actually stand ------------------
    #
    # The compatibility gate lives BEHIND the individual-approval gate, so these are two
    # separate questions and the fixtures for them are drawn from two separate sets.
    mapped_role, mapped = a_mapped_pair()
    check(G, "the mapping records positively relate a carded Skill to an approved Role",
          mapped is not None, "%s / %s" % (mapped_role, mapped))

    # (a) Parser level. A positive mapping is evidence of APPLICABILITY and nothing else.
    ok, relationship = registries.skill_is_compatible_with_role(mapped, mapped_role)
    check(G, "the mapping parser reports that pair compatible", ok, relationship)
    check(G, "and the pair is carded, not individually approved",
          mapped in registries.carded_skills() and mapped not in registries.approved_skills(),
          "%s: carded=%r approved=%r" % (mapped, mapped in registries.carded_skills(),
                                         mapped in registries.approved_skills()))

    # (b) Preflight level. A positive mapping on a carded Skill still BLOCKS, because
    # applicability is not eligibility. This is the check that would have been quietly lost
    # by keeping the old "approved exemplar Skill" fixture.
    r = run_preflight(plan(
        request_id="request.C14e",
        role_requirements=(RoleRequirement(mapped_role, "a substantive domain conclusion"),),
        skill_requirements=(SkillRequirement(mapped, mapped_role),),
        work_plan=WorkPlan("work_plan.ok", 1, (PlanStage("S1", mapped_role, (), False, "x"),))))
    check(G, "a positively mapped but unapproved Skill still BLOCKS at preflight",
          r.state is PlannerState.BLOCKED
          and BlockReason.UNREGISTERED_CAPABILITY in r.reasons, r.detail)

    # (c) The gates behind it, reached through a LABELLED double. Without this the wrong-Role
    # and unresolved-Role rules are unreachable today and lose their coverage silently.
    with simulated_individual_skill_approval(mapped):
        r = run_preflight(plan(
            request_id="request.C14e2",
            role_requirements=(RoleRequirement(mapped_role, "a substantive domain conclusion"),),
            skill_requirements=(SkillRequirement(mapped, mapped_role),),
            work_plan=WorkPlan("work_plan.ok2", 1, (
                PlanStage("S1", mapped_role, (), False, "x"),))))
        check(G, "with individual approval simulated, the mapped pair reaches VALIDATED",
              r.state is PlannerState.VALIDATED, r.detail)

        wrong = next(x for x in sorted(registries.approved_roles())
                     if not registries.skill_is_compatible_with_role(mapped, x)[0])
        r = run_preflight(plan(
            request_id="request.C14f",
            role_requirements=(RoleRequirement(wrong, "a substantive domain conclusion"),),
            skill_requirements=(SkillRequirement(mapped, wrong),),
            work_plan=WorkPlan("work_plan.bad", 1, (PlanStage("S1", wrong, (), False, "x"),))))
        check(G, "a Skill bound to a Role the mappings do not allow blocks",
              r.state is PlannerState.BLOCKED
              and BlockReason.SKILL_ROLE_INCOMPATIBLE in r.reasons, r.detail)

        r = run_preflight(plan(
            request_id="request.C14g",
            role_requirements=(RoleRequirement(mapped_role,
                                               "a substantive domain conclusion"),),
            skill_requirements=(SkillRequirement(mapped, "role.not_a_role"),),
            work_plan=WorkPlan("work_plan.ur", 1, (
                PlanStage("S1", mapped_role, (), False, "x"),))))
        check(G, "a Skill claimed for an unresolved Role blocks",
              r.state is PlannerState.BLOCKED
              and BlockReason.UNREGISTERED_CAPABILITY in r.reasons, r.detail)

    check(G, "the double is restored and no Skill is approved afterwards",
          registries.approved_skills() == set(), repr(registries.approved_skills()))

    p, store, basis = issued(request_id="request.C14h", work_plan=WorkPlan(
        "work_plan.many", 1, tuple(
            [PlanStage("S%d" % n, role, (), False, "draft") for n in range(1, 8)]
            + [PlanStage("G", None, ("S1",), True, "")])))
    trigger = build_trigger(basis, p, originator="human.a", store=store)
    ids = [s.spec_id for s in trigger.planned_work_item_specs]
    check(G, "planned spec identities are unique by construction",
          len(ids) == len(set(ids)) == 8, "%d specs, %d unique" % (len(ids), len(set(ids))))


# =========================================================== 5a. survivor invariants


@section("C-15 architecture approval is not individual approval (B1)")
def _c15():
    G = "C-15 architecture approval is not individual approval (B1)"
    carded = registries.carded_skills()
    approved = registries.approved_skills()
    check(G, "carded and individually approved are separate questions with separate views",
          hasattr(registries, "carded_skills") and hasattr(registries, "approved_skills"))
    check(G, "the Phase 4 record approves the architecture and denies mass promotion",
          "must not be interpreted as a mass status promotion"
          in read(os.path.join(REPO, "reviews", "phase-4-final-approval.md")))
    check(G, "so no Skill card is individually approved today", approved == set(),
          repr(sorted(approved)))
    check(G, "while six Skill cards demonstrably exist", len(carded) == 6,
          "%d: %r" % (len(carded), sorted(carded)))

    # The consequence, proved rather than asserted: every carded Skill blocks at preflight.
    for skill_ref in sorted(carded):
        r = run_preflight(plan(request_id="request.C15.%s" % skill_ref,
                               execution_mode=ExecutionMode.MATCH, work_plan=None,
                               workflow_ref=a_workflow_ref(),
                               skill_requirements=(SkillRequirement(skill_ref, a_role()),)))
        check(G, "%s is carded and still not assignable" % skill_ref,
              r.state is PlannerState.BLOCKED and r.basis is None
              and BlockReason.UNREGISTERED_CAPABILITY in r.reasons, r.detail)

    # The individual-approval test itself must not accept the Phase 4 record as evidence.
    source = read(os.path.join(IMPL, "registries.py"))
    check(G, "the individual-approval test excludes the Phase 4 phase-level record",
          'name == "phase-4-final-approval.md"' in source,
          "registries.py _explicit_individual_skill_approval")


@section("C-16 issuance provenance (B3)")
def _c16():
    G = "C-16 issuance provenance (B3)"
    import domain

    # A BLOCKED preflight, then a hand-built basis carrying every field the real one would.
    blocked_plan = plan(request_id="request.C16", criticality=Criticality.CRITICAL,
                        review_requirements=())
    blocked = run_preflight(blocked_plan)
    check(G, "the fixture plan really is blocked",
          blocked.state is PlannerState.BLOCKED and blocked.basis is None, blocked.detail)
    fabricated = domain.ExecutionBasis(
        basis_id="execution_basis.fabricated", version=1,
        request_id=blocked_plan.request_id, intent_id=blocked_plan.intent_id,
        scope_ref=blocked_plan.scope_ref, scope_ancestry=blocked_plan.scope_ancestry,
        execution_mode=blocked_plan.execution_mode, criticality=blocked_plan.criticality,
        planning_digest=blocked_plan.material_digest(),
        implementation_spec_version=IMPLEMENTATION_SPEC_VERSION,
        orchestrator_policy_ref=blocked_plan.orchestrator_policy_ref,
        status=BasisStatus.EXECUTABLE,
        work_plan_ref=blocked_plan.work_plan.ref,
        role_bindings=tuple(r.role_ref for r in blocked_plan.role_requirements))
    ok, ev = refuses(lambda: ActivationStore().issue(fabricated), ActivationError)
    check(G, "a fabricated basis after a blocked preflight cannot be issued", ok, ev)

    # An EQUAL-VALUE copy of a genuine basis is still not the object preflight produced.
    good = plan(request_id="request.C16b")
    result = run_preflight(good)
    copy = dataclasses.replace(result.basis)
    ok, ev = refuses(lambda: ActivationStore().issue(copy), ActivationError)
    check(G, "an equal-value copy of a genuine basis carries no provenance", ok, ev)

    # The genuine object issues once, and its provenance is consumed.
    store = ActivationStore()
    first = store.issue(result.basis)
    check(G, "the genuine successful-preflight basis issues", first is not None)
    ok, ev = refuses(lambda: ActivationStore().issue(result.basis), ActivationError)
    check(G, "and its provenance is one-time, so a second store cannot reissue it", ok, ev)

    # A non-EXECUTABLE candidate is refused before provenance is even consulted.
    third = run_preflight(plan(request_id="request.C16c"))
    ok, ev = refuses(
        lambda: ActivationStore().issue(third.basis.with_status(BasisStatus.VALIDATED)),
        ActivationError)
    check(G, "a non-EXECUTABLE candidate is not issuable", ok, ev)

    check(G, "issuance consults preflight provenance in source, not caller assertion",
          "_consume_issuance_provenance" in read(os.path.join(IMPL, "store.py")))


@section("C-17 mapping boundaries and owned-conclusion substance (B4)")
def _c17():
    G = "C-17 mapping boundaries and owned-conclusion substance (B4)"
    mappings = registries.role_skill_mappings()

    # The exact case the review named. The Wave 2 record states in a Boundary section that
    # lifecycle cost analysis is "deliberately not mapped here" for CAPEX / Cost Engineering.
    # Prose that DENIES a mapping must never be parsed into one.
    boundary_pairs = (
        ("skill.lifecycle_cost_analysis", "role.capex_cost_engineering_specialist"),
        ("skill.lifecycle_cost_analysis", "role.asset_om_technical_operations_specialist"),
    )
    for skill_ref, role_ref in boundary_pairs:
        check(G, "%s is not mapped to %s by boundary prose" % (skill_ref, role_ref),
              skill_ref not in mappings.get(role_ref, {}),
              "relationship=%r" % mappings.get(role_ref, {}).get(skill_ref))
        ok, why = registries.skill_is_compatible_with_role(skill_ref, role_ref)
        check(G, "and the pair is therefore not compatible", ok is False, why)

    check(G, "the Wave 2 record does contain that boundary prose, so the check is live",
          "is deliberately **not** mapped here" in read(os.path.join(
              REPO, "skills", "mappings",
              "wave-2-domain-completion-role-skill-mapping.md")))
    check(G, "the Skill the boundary protects is still mapped to the Role that owns it",
          mappings.get("role.technical_feasibility_lead", {}).get(
              "skill.lifecycle_cost_analysis") in registries.COMPATIBLE_RELATIONSHIPS,
          repr(mappings.get("role.technical_feasibility_lead", {}).get(
              "skill.lifecycle_cost_analysis")))
    check(G, "a non-relationship heading resets relationship state in the parser",
          'relationship = heading_text if heading_text in _RELATIONSHIPS else None'
          in read(os.path.join(IMPL, "registries.py")))

    # Owned-conclusion substance. A load-bearing Role requirement whose conclusion is blank,
    # whitespace or a placeholder is not a declared conclusion.
    role = a_role()
    for label, conclusion in (("empty", ""), ("whitespace", "   "), ("newline", "\n\t "),
                              ("TBD", "TBD"), ("to be determined", "to be determined"),
                              ("placeholder", "placeholder"), ("n/a", "N/A"),
                              ("dash", "-"), ("ellipsis", "...")):
        r = run_preflight(plan(
            request_id="request.C17.%s" % label,
            role_requirements=(RoleRequirement(role, conclusion),),
            work_plan=WorkPlan("work_plan.oc", 1, (PlanStage("S1", role, (), False, "x"),))))
        check(G, "a %s owned conclusion blocks" % label,
              r.state is PlannerState.BLOCKED and r.basis is None
              and BlockReason.NO_APPROVED_ROLE_OWNS_CONCLUSION in r.reasons, r.detail)
    r = run_preflight(plan(
        request_id="request.C17.ok",
        role_requirements=(RoleRequirement(role, "the regulatory position on the transfer"),),
        work_plan=WorkPlan("work_plan.oc2", 1, (PlanStage("S1", role, (), False, "x"),))))
    check(G, "a substantive owned conclusion does not block",
          r.state is PlannerState.VALIDATED, r.detail)


# =========================================================== 6. prose agrees with behaviour


@section("prose")
def _prose():
    G = "prose"

    def says(name, *phrases):
        body = flat(doc(name))
        return [p for p in phrases if flat(p) not in body]

    missing = says("execution-basis-contract.md", "may accept", "is_approval", "is_authority")
    if not any(flat(p) in flat(doc("execution-basis-contract.md"))
               for p in ("authorises entry", "entry to intake")):
        missing.append("authorises entry / entry to intake")
    check(G, "the basis contract states what the object authorises and declares its false "
             "fields", not missing, "missing: %r" % missing)

    missing = says("po-4-and-po-12-closure.md", "PROPOSED", "intake may accept",
                   "PO-16-A", "PO-16-E")
    check(G, "the closure document states the proposal status and records its new open items",
          not missing, "missing: %r" % missing)
    check(G, "the closure document does not claim either obligation is closed outright",
          "neither is closed by this package alone" in flat(doc("po-4-and-po-12-closure.md")))

    missing = says("workflow-resolution-contract.md", "work_plan.", "workflow.")
    check(G, "the resolution contract keeps the two identifier spaces distinct in writing",
          not missing, "missing: %r" % missing)
    missing = says("idempotency-versioning-replay.md", "most recently issued", "append-only",
                   "material_digest")
    check(G, "the idempotency document states the lineage rule the store implements",
          not missing, "missing: %r" % missing)
    missing = says("observability-audit-provenance.md", "operational", "governed", "provenance")
    check(G, "the observability document separates operational from governed events",
          not missing, "missing: %r" % missing)

    missing = says("registry-eligibility-contract.md", "carded", "mention", "fail closed")
    check(G, "the eligibility contract distinguishes a card from a mention and fails closed",
          not missing, "missing: %r" % missing)
    body = doc("registry-eligibility-contract.md")
    check(G, "and it names the three misparsed Role IDs it exists to exclude",
          all(bad in body for bad in MISPARSED_ROLE_IDS),
          "missing: %r" % [b for b in MISPARSED_ROLE_IDS if b not in body])

    missing = says("execution-basis-contract.md", "immutable", "sealed")
    check(G, "the basis contract states that an issued basis is immutable and sealed",
          not missing, "missing: %r" % missing)
    missing = says("change-control-contract.md", "material")
    check(G, "the change-control contract governs material change", not missing)
    missing = says("role-skill-assignment-binding.md", "mapping")
    check(G, "the role/skill binding document reads compatibility from the mapping records",
          not missing)

    check(G, "no package document claims production readiness",
          not any(re.search(r"(?i)production[- ]ready|ready for production|is approved for use",
                            doc(n)) for n in PACKAGE_DOCS))
    check(G, "no package document claims to approve, register or grant anything",
          not any(re.search(r"(?i)\b(hereby|we hereby)\s+(approve|grant|register)\b", doc(n))
                  for n in PACKAGE_DOCS))
    self_check = flat(doc("phase-16-self-check.md"))
    check(G, "the self-check disclaims governance authority",
          "never governance authority" in self_check or "not governance authority" in self_check)
    check(G, "the self-check names at least one limit of its own assurance",
          "cannot" in self_check or "limit" in self_check)


# =========================================================== 7. containment


@section("containment")
def _containment():
    G = "containment"
    for tree in ("architecture", "planning", "implementation-spec", "roles", "skills",
                 "workflows", "decisions"):
        path = os.path.join(REPO, tree)
        check(G, "Phase 16 adds nothing under %s/" % tree,
              os.path.isdir(path) and not any("phase-16" in p or "phase_16" in p
                                              for p in os.listdir(path)),
              tree)
    check(G, "this validator disclaims governance authority",
          "NEVER GOVERNANCE AUTHORITY" in read(os.path.abspath(__file__)))
    check(G, "validation/ carries exactly the Phase 16 validator and its probes",
          sorted(p for p in os.listdir(HERE) if "phase_16" in p)
          == ["phase_16_mutation_probes.py", "phase_16_validation.py"])


# =========================================================== main


def main():
    verbose = "--verbose" in sys.argv
    as_json = "--json" in sys.argv
    runner_errors = []
    for name, fn in SECTIONS:
        try:
            fn()
        except INFRASTRUCTURE_FAULTS as err:
            # The harness could not RUN: an import failed, a path is missing, the interpreter
            # itself faulted. That is never a semantic finding, and the mutation harness must
            # not read it as one, so it is carried into the top-level status as RUNNER_ERROR.
            line = (traceback.format_exc().strip().splitlines() or [""])[-1][:200]
            runner_errors.append("%s: section raised %s: %s"
                                 % (name, type(err).__name__, line))
            check(name, "section raised %s" % type(err).__name__, False, line)
        except Exception as err:
            # The harness RAN, and the implementation under test behaved differently enough to
            # break a fixture - an empty registry where the check indexes one, a refusal where
            # the check expected a result. That is a finding about the implementation, so it
            # is a semantic FAIL. Recording it as a runner error would let a real regression
            # hide behind "infrastructure".
            line = (traceback.format_exc().strip().splitlines() or [""])[-1][:200]
            check(name, "section could not complete: %s" % type(err).__name__, False, line)
    passed = sum(1 for r in RESULTS if r["pass"])
    if runner_errors:
        status = "RUNNER_ERROR"
    elif passed == len(RESULTS):
        status = "PASS"
    else:
        status = "FAIL"
    if as_json:
        # Valid JSON on stdout and nothing else, carrying an explicit top-level execution
        # status, so the mutation harness can distinguish a semantic failure from a runner or
        # infrastructure failure by reading a field rather than guessing from an exit code.
        sys.stdout.write(json.dumps(
            {"status": status, "runner_errors": runner_errors,
             "total": len(RESULTS), "passed": passed,
             "failed": [r for r in RESULTS if not r["pass"]], "results": RESULTS}, indent=2))
        sys.stdout.write("\n")
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
        if runner_errors:
            print("\nRUNNER_ERROR")
            for item in runner_errors:
                print("  - %s" % item)
        print("\n=== %d/%d PASS === (%s)" % (passed, len(RESULTS), status))
    if status == "RUNNER_ERROR":
        return 2
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
