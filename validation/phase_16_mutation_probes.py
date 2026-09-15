"""Phase 16 — mutation probes for the planner-activation validator.

Status: PROPOSED. Standard library only, deterministic, no network.

    python3 validation/phase_16_mutation_probes.py [--verbose] [--json]

A validator that passes proves nothing on its own: it may be passing because it is not looking.
Each probe breaks exactly one rule inside a throwaway COPY of the package and re-runs the
validator there, expecting it to fail.

WHAT CHANGED AND WHY. The first harness was not a valid fixture and its accounting was not
honest.

  * The copy contained only `planner-activation/`, `implementation/phase-16/` and three
    directories the containment checks list. It did NOT contain `roles/`, `skills/`,
    `reviews/`, `decisions/` or `workflows/` - the approved documents the registry views read -
    and the registry module computed the repository root from its own `__file__`, so a probe
    silently read the REAL tree. The fixture was incomplete and the isolation was fictional.
  * Any non-zero exit counted as detection. An import error, a path error, a syntax error or a
    crashed interpreter all looked exactly like "the validator caught it".

Both are fixed. The copy carries every read-only dependency, the registry root is pinned to the
copy through `PHASE_16_REPO_ROOT`, a PRISTINE COPIED CONTROL must pass before a single mutation
result is counted, and outcomes are four, not two:

    DETECTED      the validator ran, produced valid JSON, and reported at least one failure
    ESCAPED       the validator ran, produced valid JSON, and reported everything passing
    REDUNDANT     the mutation did not apply - the pattern matched nothing, so the probe is dead
    RUNNER_ERROR  the validator could not produce a verdict at all (no JSON on stdout)

A RUNNER_ERROR is never counted as a detection. It is a harness defect to be fixed, and the
run reports it as one.

OUTCOMES ARE ASSERTED, NOT ASSUMED. Each probe declares the outcome it expects. Almost all
expect DETECTED; two expect RUNNER_ERROR, because "an unexpected runtime fault is never counted
as a semantic detection" is itself an invariant worth testing rather than trusting. A probe is
satisfied when it gets the outcome it asserts, and the totals below report both numbers.

ESCAPES THAT ARE NOT VALIDATOR GAPS. Eight probes escape, and every one of them breaks a
SECOND line of defence while a stronger first line still holds. They are kept rather than
deleted, because a probe that escapes for a stated reason is evidence and a probe quietly
removed is not:

  * `the store stops checking the basis version`, `the builder stops checking the
    implementation-spec version`, `the builder accepts a basis claiming to be an approval`
    - the payload SEAL already covers version, spec version and both false flags, so the
    tampered basis is refused before the dropped check would have run;
  * `the scope binding quietly leaves the list`, `the builder stops checking the Work Plan
    binding` - scope and the Work Plan are both inside the material digest, which is compared
    independently;
  * `a Work Plan may be rendered in the workflow identifier space` - the `work_plan.` prefix
    check raises first, so the `workflow.` check is a second guard on the same rule;
  * `planned spec identities may collide` - duplicate stage ids are blocked before a basis is
    issued, so the collision assertion is unreachable by construction;
  * `the Role cross-check against the approved universe is dropped` - on a clean tree the
    cross-check finds nothing to reject, so removing it changes no result. The probes that
    BREAK the evidence it protects (a slugged card ID, a renamed card, a missing version, a
    superseded card, a demoted approval record) are all detected;
  * `a carded Skill card status is no longer required to be APPROVED` - individual Skill
    approval needs BOTH an APPROVED card status and a separate human approval record naming
    the identity, and no card satisfies the second either, so dropping the first changes
    nothing. `individual Skill approval is asserted rather than evidenced`, which drops both,
    is detected;
  * `a non-EXECUTABLE candidate becomes issuable` - the one-time preflight provenance refuses
    a `with_status` copy before the status check would have mattered;
  * `explicit negative wording stops denying a mapping` - the heading reset already keeps
    boundary and exclusion sections from being read as mappings, so the negative-wording rule
    is a second guard on the same prose. `boundary and exclusion prose leaks into positive
    mappings`, which drops all three guards together, is detected.

Each is defence in depth working as intended, not a rule nobody is checking. Reporting them as
detections would be the dishonest option.

This file is an ASSURANCE TOOL AND NEVER GOVERNANCE AUTHORITY.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
VALIDATOR = os.path.join(HERE, "phase_16_validation.py")

#: Everything the validator and the reference implementation READ. The first five are the
#: approved registry documents and approval records the registry views resolve identities and
#: approval evidence from; the last three are read by the containment checks. Omitting any of
#: them does not fail loudly - it makes the registries resolve to nothing and the fixture lie.
COPY_PATHS = (
    "planner-activation",
    os.path.join("implementation", "phase-16"),
    "roles", "skills", "reviews", "decisions", "workflows",
    "architecture", "planning", "implementation-spec",
)

DETECTED = "DETECTED"
ESCAPED = "ESCAPED"
REDUNDANT = "REDUNDANT"
RUNNER_ERROR = "RUNNER_ERROR"

PROBES = []


def probe(name, path, pattern, replacement, count=1, expect=None):
    """Register a single-rule mutation. `path` is repo-relative; `pattern` is a regex.

    `expect` names the outcome the probe is asserting. It defaults to DETECTED; the one probe
    that asserts RUNNER_ERROR sets it explicitly, because "the harness must not read a crash as
    a detection" is itself an invariant worth testing rather than trusting.
    """
    PROBES.append({"name": name, "path": path, "expect": expect or DETECTED,
                   "edits": [(pattern, replacement, count)]})


def probe_edits(name, path, edits):
    """A mutation that needs more than one edit to stay SYNTACTICALLY AND STRUCTURALLY VALID.

    Removing a field from MATERIAL_FIELDS alone trips the classification invariant at import,
    which is a runner error rather than a detection. Reclassifying the field - taking it out of
    material and calling it presentation-only - is the mutation actually worth probing: it
    loads cleanly, it is exactly the defect being guarded against, and the validator either
    notices or does not.
    """
    PROBES.append({"name": name, "path": path, "expect": DETECTED,
                   "edits": [(p, r, c) for p, r, c in edits]})


def impl(name):
    return os.path.join("implementation", "phase-16", name)


def pkg(name):
    return os.path.join("planner-activation", name)


D, P, H, S, R = "domain.py", "preflight.py", "handoff.py", "store.py", "registries.py"


# ------------------------------------------------- B1 / C-0 registry eligibility
#
# These mutate the APPROVED DOCUMENTS in the copy, not only the parsing code. Disabling a guard
# on a clean tree changes nothing - the evidence is there either way - so a probe that only
# flipped an `if` was inert and reported as escaped. Breaking the evidence is what tests whether
# the registry actually reads it. These probes are also the reason the copied fixture must carry
# roles/, skills/, reviews/, decisions/ and workflows/: without them there is nothing to break.

ROLE_CARD = os.path.join("roles", "economics-finance-transaction",
                         "fpa-management-finance-specialist.md")
REVIEW_CARD = os.path.join("reviews", "exemplars", "security.md")
WORKFLOW_CARD = os.path.join("workflows", "exemplars", "software-change-delivery.md")
DECISION_CARD = os.path.join("decisions", "exemplars", "external-publication.md")
SKILL_CARD = os.path.join("skills", "research-evidence", "source-verification.md")
P3_APPROVAL = os.path.join("reviews", "phase-3-final-approval.md")
P6_APPROVAL = os.path.join("reviews", "phase-6-final-approval.md")
P7_APPROVAL = os.path.join("reviews", "phase-7-final-approval.md")

probe("a Role Card declares a display-name SLUG instead of its declared ID", ROLE_CARD,
      r"`role\.fpa_management_finance_specialist`",
      "`role.fp_a_management_finance_specialist`", 0)
probe("a Role Card loses its declared ID entirely", ROLE_CARD,
      r"(?m)^- Role ID: .*$", "- Role Identifier: withheld")
probe("a Role Card loses its declared Version", ROLE_CARD, r"(?m)^- Version: .*$", "")
probe("a Role Card is marked superseded", ROLE_CARD,
      r"(?m)^- Superseded By: none$", "- Superseded By: `role.something_else`")
probe("a Role Card's display name stops matching the approved universe", ROLE_CARD,
      r"(?m)^- Role Name: .*$", "- Role Name: Something Else Entirely")
probe("the Phase 3 approval record loses the scope phrase the Roles rest on", P3_APPROVAL,
      r"59 unique Role IDs", "some Role IDs")
probe("the Phase 3 approval record is no longer marked APPROVED", P3_APPROVAL,
      r"Status: APPROVED — HUMAN DECISION", "Status: PROPOSED — awaiting decision")
probe("the Phase 6 approval record loses the scope phrase the Reviews rest on", P6_APPROVAL,
      r"the six exemplar Review Profiles", "some Review Profiles")
probe("the Phase 7 approval record is no longer marked APPROVED", P7_APPROVAL,
      r"Status: \*\*APPROVED — HUMAN DECISION\*\*", "Status: **PROPOSED**")
probe("a Review Profile Card loses its declared ID", REVIEW_CARD,
      r"(?m)^- Review ID: .*$", "- Review Identifier: withheld")
probe("a Decision Right Card loses its declared ID", DECISION_CARD,
      r"(?m)^- Decision ID: .*$", "- Decision Identifier: withheld")
probe("a Skill Card loses its declared ID", SKILL_CARD,
      r"(?m)^- Skill ID: .*$", "- Skill Identifier: withheld")
probe("a Workflow Card declares a different version from the one MATCH binds", WORKFLOW_CARD,
      r"(?m)^- Version: 0\.1$", "- Version: 2.0")
probe("a Workflow Card is marked superseded", WORKFLOW_CARD,
      r"(?m)^- Superseded By: none$", "- Superseded By: `workflow.something_else`")

# The parsing guards themselves. Each is paired with the evidence it protects, so that
# disabling the guard is visible rather than inert on a clean tree.
probe("the Role cross-check against the approved universe is dropped", impl(R),
      r"if len\(cards\) != _APPROVED_ROLE_COUNT or carded_names != listed:", "if False:")
probe("the approved Workflow version is invented rather than declared", impl(R),
      r"return \{k: v for k, \(v, _n, _p\) in _registered\(\"workflow\"\)\.items\(\)\}",
      "return {k: 1 for k in _registered(\"workflow\")}")
probe("an unmapped Skill/Role pair becomes compatible", impl(R),
      r"if relationship is None:\n        return False, \(",
      "if relationship is None:\n        return True, (")
probe("PROHIBITED_IN_CONTEXT becomes a compatible relationship", impl(R),
      r'COMPATIBLE_RELATIONSHIPS = \("REQUIRED_CORE", "REQUIRED_FOR_CONTEXT", "OPTIONAL", "ALTERNATIVE"\)',
      'COMPATIBLE_RELATIONSHIPS = ("REQUIRED_CORE", "REQUIRED_FOR_CONTEXT", "OPTIONAL", '
      '"ALTERNATIVE", "PROHIBITED_IN_CONTEXT")')

# ------------------------------------------------- B2 / C-4 material digest

probe("a material change leaves the live basis standing", impl(S),
      r"entry\._transition\(BasisStatus\.STALE\)", "pass")
probe_edits("clarifications is reclassified as presentation-only", impl(D), [
    (r'"evidence_requirements", "clarifications", "workflow_ref", "work_plan",', '"evidence_requirements", "workflow_ref", "work_plan",', 1),
    (r'PRESENTATION_ONLY_FIELDS = \("request_text",\)',
     'PRESENTATION_ONLY_FIELDS = ("request_text", "clarifications")', 1),
])
probe_edits("scope_ancestry is reclassified as presentation-only", impl(D), [
    (r'"scope_ref", "scope_ancestry", "objective"', '"scope_ref", "objective"', 1),
    (r'PRESENTATION_ONLY_FIELDS = \("request_text",\)',
     'PRESENTATION_ONLY_FIELDS = ("request_text", "scope_ancestry")', 1),
])
probe_edits("orchestrator_policy_ref is reclassified as presentation-only", impl(D), [
    (r'"orchestrator_policy_ref", "unknown_fields",', '"unknown_fields",', 1),
    (r'PRESENTATION_ONLY_FIELDS = \("request_text",\)',
     'PRESENTATION_ONLY_FIELDS = ("request_text", "orchestrator_policy_ref")', 1),
])
probe_edits("unknown_fields is reclassified as presentation-only", impl(D), [
    (r'"orchestrator_policy_ref", "unknown_fields",', '"orchestrator_policy_ref",', 1),
    (r'PRESENTATION_ONLY_FIELDS = \("request_text",\)',
     'PRESENTATION_ONLY_FIELDS = ("request_text", "unknown_fields")', 1),
])
probe_edits("work_plan is reclassified as presentation-only", impl(D), [
    (r'"workflow_ref", "work_plan",', '"workflow_ref",', 1),
    (r'PRESENTATION_ONLY_FIELDS = \("request_text",\)',
     'PRESENTATION_ONLY_FIELDS = ("request_text", "work_plan")', 1),
])
probe_edits("objective is reclassified as presentation-only", impl(D), [
    (r'"objective", "deliverables"', '"deliverables"', 1),
    (r'PRESENTATION_ONLY_FIELDS = \("request_text",\)',
     'PRESENTATION_ONLY_FIELDS = ("request_text", "objective")', 1),
])
probe_edits("criticality is reclassified as presentation-only", impl(D), [
    (r'"criticality", "execution_mode"', '"execution_mode"', 1),
    (r'PRESENTATION_ONLY_FIELDS = \("request_text",\)',
     'PRESENTATION_ONLY_FIELDS = ("request_text", "criticality")', 1),
])
probe("the field-classification invariant stops running", impl(D),
      r"(?m)^_assert_every_planner_field_is_classified\(\)$",
      "pass  # invariant disabled")
probe_edits("request_text is reclassified as material", impl(D), [
    (r'PRESENTATION_ONLY_FIELDS = \("request_text",\)', 'PRESENTATION_ONLY_FIELDS = ()', 1),
    (r'"orchestrator_policy_ref", "unknown_fields",',
     '"orchestrator_policy_ref", "unknown_fields", "request_text",', 1),
])

# ------------------------------------------------- B3 / C-13 basis integrity

probe("the issued basis becomes mutable again", impl(D),
      r"@dataclasses\.dataclass\(frozen=True\)\nclass ExecutionBasis:",
      "@dataclasses.dataclass\nclass ExecutionBasis:")
probe("the seal covers nothing, so any edit verifies", impl(D),
      r'_UNSEALED_FIELDS = \("status",\)',
      '_UNSEALED_FIELDS = tuple(f.name for f in dataclasses.fields(ExecutionBasisSealHack)) '
      'if False else ("status", "scope_ref", "planning_digest", "review_requirements", '
      '"decision_requirements", "evidence_requirements", "role_bindings", "skill_bindings", '
      '"implementation_spec_version", "orchestrator_policy_ref", "criticality", '
      '"work_plan_ref", "workflow_ref", "is_approval", "is_authority", "version", '
      '"request_id", "intent_id", "scope_ancestry", "execution_mode")')
probe("a holder may mark an issued basis stale again", impl(D),
      r'def mark_stale\(self, \*_args, \*\*_kwargs\):\n        raise GovernanceError\(',
      'def mark_stale(self, *_args, **_kwargs):\n        return None\n        raise '
      'GovernanceError(')
probe("the store stops verifying the seal", impl(S),
      r"if entry\.seal != basis\.payload_seal\(\):", "if False:")
probe("the store stops noticing a basis it never issued", impl(S),
      r"if entry is None:\n            return False,", "if False:\n            return False,")
probe("the store stops checking the basis version", impl(S),
      r"if entry\.payload\.version != basis\.version:", "if False:")
probe("the store stops checking the lifecycle status it owns", impl(S),
      r"if entry\.status is not basis\.status:", "if False:")
probe("a basis may be built without the issuing store", impl(H),
      r"if store is None:\n        raise ActivationError\(",
      "if False:\n        raise ActivationError(")
probe("the builder stops verifying the basis at all", impl(H),
      r"(?m)^    verify_basis\(basis, plan, store\)$", "    pass")
probe("the builder stops checking EXECUTABLE status", impl(H),
      r"if basis\.status is not BasisStatus\.EXECUTABLE:", "if False:")
probe("the builder stops comparing basis and plan bindings", impl(H),
      r"for basis_attr, plan_attr, description in _BINDINGS:", "for basis_attr, plan_attr, "
      "description in ():")
probe("the request identity binding quietly leaves the list", impl(H),
      r'\("request_id", "request_id", "originating request identity"\),\n', "")
probe("the scope binding quietly leaves the list", impl(H),
      r'\("scope_ref", "scope_ref", "governed scope"\),\n', "")
probe("the builder stops comparing the planning digest", impl(H),
      r"if basis\.planning_digest != plan\.material_digest\(\):", "if False:")
probe("the builder stops checking the implementation-spec version", impl(H),
      r"if basis\.implementation_spec_version != IMPLEMENTATION_SPEC_VERSION:", "if False:")
probe("the builder accepts a basis claiming to be an approval", impl(H),
      r"if basis\.is_approval or basis\.is_authority:\n        raise GovernanceError\(",
      "if False:\n        raise GovernanceError(")
probe("the builder stops checking the Work Plan binding", impl(H),
      r"if basis\.work_plan_ref != expected_plan_ref:", "if False:")
probe("the store issues a basis that declares itself an approval", impl(S),
      r"if basis\.is_approval or basis\.is_authority:\n            raise GovernanceError\(",
      "if False:\n            raise GovernanceError(")
probe("a trigger may be recorded against a basis nobody issued", impl(S),
      r"if basis_ref not in self\._issued:", "if False:")
probe("is_approval is declared true on the basis", impl(D),
      r"is_approval: bool = False", "is_approval: bool = True")
probe("is_authority is declared true on the basis", impl(D),
      r"is_authority: bool = False", "is_authority: bool = True")
probe("a trigger declares itself an approval", impl(H),
      r"is_approval: bool = False", "is_approval: bool = True")
probe("ExecutionBasis.exercise() returns instead of refusing", impl(D),
      r"(def exercise\(self, \*_args, \*\*_kwargs\):\n\s*)raise GovernanceError\(",
      r"\1return None  # noqa\n        _unused = GovernanceError(")
probe("ExecutionBasis.satisfy_review() returns instead of refusing", impl(D),
      r"(def satisfy_review\(self, \*_args, \*\*_kwargs\):\n\s*)raise GovernanceError\(",
      r"\1return None  # noqa\n        _unused = GovernanceError(")
probe("a ReviewRequirement arrives already satisfied", impl(D),
      r"satisfied: bool = False", "satisfied: bool = True")
probe("a DecisionRequirement arrives already exercised", impl(D),
      r"exercised: bool = False", "exercised: bool = True")

# ------------------------------------------------- B4 / C-14 composition bindings

probe("duplicate stage identities are collapsed silently again", impl(P),
      r"for duplicate in sorted\(duplicates\):", "for duplicate in ():")
probe("an unregistered stage owner is accepted", impl(P),
      r"elif stage\.role_ref not in approved_roles:", "elif False:")
probe("a stage owner nobody declared a conclusion for is accepted", impl(P),
      r"elif stage\.role_ref not in owned_conclusions:", "elif False:")
probe("a non-gate stage with no owner is accepted", impl(P),
      r"if stage\.role_ref is None:\n                block\(BlockReason\.STAGE_OWNER_UNRESOLVED,",
      "if False:\n                block(BlockReason.STAGE_OWNER_UNRESOLVED,")
probe("Skill-to-Role compatibility stops being checked", impl(P),
      r"        if not compatible:\n            block\(BlockReason\.SKILL_ROLE_INCOMPATIBLE, why\)",
      "        if False:\n            block(BlockReason.SKILL_ROLE_INCOMPATIBLE, why)")
probe("a Skill claimed for an unresolved Role is accepted", impl(P),
      r"if skill\.for_role is None or skill\.for_role not in approved_roles:", "if False:")
probe("an unregistered Role is accepted for assignment", impl(P),
      r"elif role\.role_ref not in approved_roles or not role\.registered:", "elif False:")
probe("an unapproved Skill is accepted for assignment", impl(P),
      r"if skill\.skill_ref not in approved_skills or not skill\.registered:", "if False:")
probe("planned spec identities may collide", impl(H),
      r"if len\(set\(spec_ids\)\) != len\(spec_ids\):", "if False:")

# ------------------------------------------------- the remaining required classes

probe("preflight accepts a caller-supplied governed record", impl(P),
      r"if plan\.injected_governed_records:", "if False:")
probe("MATCH accepts any Workflow identity the planner names", impl(P),
      r"if wf_id not in approved:", "if False:")
probe("MATCH ignores the Workflow version", impl(P),
      r'plan\.workflow_ref\.partition\("@"\)', 'plan.workflow_ref.partition("#")')
probe("author and final critical reviewer may be the same identity", impl(P),
      r"author_identity == reviewer_identity", "author_identity != reviewer_identity")
probe("a blocking clarification no longer blocks", impl(P),
      r"if any\(c\.blocking for c in plan\.clarifications\):", "if False:")
probe("a repeated trigger mints a second lineage", impl(S),
      r"if idempotency_key in self\._triggers:", "if False:")
probe("the idempotency key ignores the material planning version", impl(H),
      r'"%s\|%s\|%s" % \(plan\.scope_ref, plan\.request_id, plan\.material_digest\(\)\)',
      '"%s|%s" % (plan.scope_ref, plan.request_id)')
probe("re-issuing on unchanged inputs mints a second basis", impl(S),
      r"                return previous\.snapshot\(\)\n", "                pass\n")
probe("a Work Plan may be rendered in the workflow identifier space", impl(D),
      r'if self\.work_plan_id\.startswith\("workflow\."\):', "if False:")
probe("a repeated pattern is emitted as APPROVED rather than PROPOSED", impl(S),
      r'"status": "PROPOSED",', '"status": "APPROVED",')
probe("a workflow candidate is declared matchable", impl(S),
      r'"is_matchable": False,', '"is_matchable": True,')
probe("the store grows a promotion path", impl(S),
      r"(?m)\Z", '\n\ndef promote_candidate(candidate):\n    candidate["status"] = "APPROVED"'
                 "\n    return candidate\n")
probe("the registry view grows a write path", impl(R),
      r"(?m)\Z", "\n\ndef register_role(role_ref):\n    return role_ref\n")
probe("the trigger builder stops screening for governed records", impl(H),
      r"for field in FORBIDDEN_IN_TRIGGER:", "for field in ():")
probe("the forbidden list quietly loses the Review Instance", impl(H),
      r'"decision_record", "review_instance", ', '"decision_record", ')
probe("a planned spec may take work_item identity", impl(H),
      r'if not self\.spec_id\.startswith\("planned_work_item_spec\."\):', "if False:")
probe("the handoff invents its own command instead of the approved one", impl(H),
      r'command="CreateWorkflowRun",', 'command="ActivatePlanDirectly",')
probe("basis versioning reads the live basis, losing the lineage across a STALE one", impl(S),
      r"previous = self\._latest\(basis\.request_id\)",
      "previous = None if not self._by_request.get(basis.request_id) else next(\n"
      "            (self._issued[r] for r in reversed(self._by_request[basis.request_id])\n"
      "             if self._issued[r].status in (BasisStatus.VALIDATED, "
      "BasisStatus.EXECUTABLE)), None)")
probe("a new basis no longer records what it supersedes", impl(S),
      r"supersedes = previous\.payload\.ref", "supersedes = None")
probe("the basis stops binding the implementation-spec version", impl(D),
      r'IMPLEMENTATION_SPEC_VERSION = "phase-14@ba9e3fee"',
      'IMPLEMENTATION_SPEC_VERSION = "unversioned"')

# ------------------------------------------------- survivors: B1 / B3 / B4 / B5

# B1. The exact defect: reading the Phase 4 ARCHITECTURE approval as individual Skill approval.
probe("Skill eligibility is inferred from the Phase 4 architecture approval", impl(R),
      r'    if kind_name == "skill":', "    if False:")
probe("the individual-approval test accepts the phase-level Phase 4 record", impl(R),
      r'if not name\.endswith\("\.md"\) or name == "phase-4-final-approval\.md":',
      'if not name.endswith(".md"):')
probe("individual Skill approval is asserted rather than evidenced", impl(R),
      r"(?m)^    try:\n        card = _read\(card_path\)",
      "    return True\n    try:\n        card = _read(card_path)")
probe("a carded Skill card status is no longer required to be APPROVED", impl(R),
      r'if status is None or status\.group\(1\)\.strip\(\) != "APPROVED":', "if False:")

# B3. Issuance provenance: sealing arbitrary caller input is not validation.
probe("issuance stops requiring successful-preflight provenance", impl(S),
      r"request_id, digest, seal = _consume_issuance_provenance\(basis\)",
      "request_id, digest, seal = (basis.request_id, basis.planning_digest, "
      "basis.payload_seal())")
probe("provenance is no longer consumed, so one proof issues for ever", impl(P),
      r"entry = _ISSUABLE\.pop\(id\(basis\), None\)", "entry = _ISSUABLE.get(id(basis))")
probe_edits("provenance is keyed by value, so an equal-value copy issues", impl(P), [
    (r"_ISSUABLE\[id\(basis\)\] = ", "_ISSUABLE[basis.ref] = ", 1),
    (r"entry = _ISSUABLE\.pop\(id\(basis\), None\)",
     "entry = _ISSUABLE.pop(basis.ref, None)", 1),
    (r"if entry is None or entry\[0\] is not basis:", "if entry is None:", 1),
])
probe("a non-EXECUTABLE candidate becomes issuable", impl(S),
      r"if basis\.status is not BasisStatus\.EXECUTABLE:", "if False:")

# B4. Mapping boundaries and owned-conclusion substance.
probe("a non-relationship heading no longer resets the parser's relationship state", impl(R),
      r"relationship = heading_text if heading_text in _RELATIONSHIPS else None",
      "relationship = heading_text if heading_text in _RELATIONSHIPS else relationship")
probe_edits("boundary and exclusion prose leaks into positive mappings", impl(R), [
    (r"relationship = heading_text if heading_text in _RELATIONSHIPS else None",
     "relationship = heading_text if heading_text in _RELATIONSHIPS else relationship", 1),
    (r"\(\?:\\s\*\[-—:\]\\s\*\(\.\*\)\)\?\$", "(.*)$", 1),
    (r'effective = "PROHIBITED_IN_CONTEXT" if _NEGATIVE\.search\(trailing\) else relationship',
     "effective = relationship", 1),
])
probe("explicit negative wording stops denying a mapping", impl(R),
      r'effective = "PROHIBITED_IN_CONTEXT" if _NEGATIVE\.search\(trailing\) else relationship',
      "effective = relationship")

probe("a blank or placeholder owned conclusion is accepted", impl(P),
      r"if role\.load_bearing and not _substantive_conclusion\(role\.owned_conclusion\):",
      "if False:")
probe("the placeholder set empties, so TBD counts as a conclusion", impl(P),
      r"(?s)_PLACEHOLDER_CONCLUSIONS = \{.*?\}", "_PLACEHOLDER_CONCLUSIONS = set()")

# B5. The harness's own invariant: an unexpected runtime fault is never a detection. Three
# probes, because there are three distinct paths to it: a fault at IMPORT, which leaves no JSON
# on stdout at all; a fault INSIDE a running section; and - the one the final review found - a
# fault raised by a call the assurance REFUSAL HELPER is wrapping. The helper used to absorb
# that third case into an ordinary failed check, so a crash was counted as a DETECTION. It now
# re-raises, and this probe is what holds it to that.
probe("an unexpected RuntimeError is raised THROUGH the assurance refusal helper", impl(D),
      r"(    def exercise\(self, \*_args, \*\*_kwargs\):\n)(        raise GovernanceError\()",
      '\\1        raise RuntimeError("deliberate unexpected fault injected by the Phase 16 '
      'probe harness")\n\\2',
      1, RUNNER_ERROR)
probe("an unexpected RuntimeError is raised inside a running validator section", impl(R),
      r"(?m)^    mappings: Dict\[str, Dict\[str, str\]\] = \{\}$",
      '    raise RuntimeError("deliberate unexpected fault injected by the Phase 16 probe '
      'harness")\n    mappings: Dict[str, Dict[str, str]] = {}',
      1, RUNNER_ERROR)
probe("an unexpected RuntimeError is raised inside the validated implementation", impl(D),
      r"(?m)^IMPLEMENTATION_SPEC_VERSION = ",
      'raise RuntimeError("deliberate unexpected fault injected by the Phase 16 probe harness")'
      "\nIMPLEMENTATION_SPEC_VERSION = ",
      1, RUNNER_ERROR)

# ------------------------------------------------- prose

probe("the closure document claims PO-4 is closed outright", pkg("po-4-and-po-12-closure.md"),
      r"Neither is closed by this package alone", "Both obligations are closed by this package")
probe("the closure document drops its new open items", pkg("po-4-and-po-12-closure.md"),
      r"PO-16-E", "PO-16-Z", 0)
probe("the closure document promises intake will accept", pkg("po-4-and-po-12-closure.md"),
      r"intake may accept", "intake will accept")
probe("the basis contract drops the declared false fields",
      pkg("execution-basis-contract.md"), r"is_authority", "is-authority-omitted", 0)
probe("the basis contract stops saying an issued basis is immutable",
      pkg("execution-basis-contract.md"), r"(?i)immutable", "convenient", 0)
probe("the basis contract stops saying an issued basis is sealed",
      pkg("execution-basis-contract.md"), r"(?i)seal(ed|s|)\b", "noted", 0)
probe("the eligibility contract stops naming the misparsed Role IDs",
      pkg("registry-eligibility-contract.md"),
      r"role\.asset_o_m_technical_operations_specialist", "role.asset_om_slug_example")
probe("the eligibility contract stops failing closed",
      pkg("registry-eligibility-contract.md"), r"(?i)fail closed", "proceed anyway", 0)
probe("the eligibility contract stops distinguishing a card from a mention",
      pkg("registry-eligibility-contract.md"), r"(?i)mention", "reference", 0)
probe("the role/skill document stops reading the mapping records",
      pkg("role-skill-assignment-binding.md"), r"(?i)mapping", "guidance", 0)
probe("the README drops its unapproved banner", pkg("README.md"),
      r"\*\*Nothing in this package is approved\.\*\*", "This package is ready.")
probe("the README stops listing the self-check", pkg("README.md"),
      r"phase-16-self-check\.md", "phase-16-notes.md")
probe("a package document claims production readiness", pkg("README.md"),
      r"## 5\. Non-Runtime Statement",
      "## 5. This package is production-ready\n\nNon-Runtime Statement")
probe("the self-check drops its governance disclaimer", pkg("phase-16-self-check.md"),
      r"NEVER GOVERNANCE AUTHORITY", "an authoritative record")
probe("the idempotency document contradicts the store's lineage rule",
      pkg("idempotency-versioning-replay.md"), r"most recently issued", "currently live")
probe("the observability document loses the governed/operational split",
      pkg("observability-audit-provenance.md"), r"(?i)\bgoverned\b", "recorded", 0)


# --------------------------------------------------------------- runner


def build_root(tmp):
    root = os.path.join(tmp, "repo")
    os.makedirs(root)
    for rel in COPY_PATHS:
        src = os.path.join(REPO, rel)
        dst = os.path.join(root, rel)
        if not os.path.isdir(src):
            raise RuntimeError("required fixture dependency is missing: %s" % rel)
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return root


def run_validator(root):
    """(parsed json or None, returncode, stderr tail). None means: no verdict was produced."""
    env = dict(os.environ)
    env["PHASE_16_REPO_ROOT"] = root
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run([sys.executable, VALIDATOR, "--json"], env=env,
                          capture_output=True, text=True, cwd=root)
    try:
        report = json.loads(proc.stdout)
    except (ValueError, TypeError):
        report = None
    return report, proc.returncode, (proc.stderr or "").strip()[-400:]


def classify(root):
    """What did the validator actually say? Read the status field, never the exit code."""
    report, code, stderr = run_validator(root)
    if report is None:
        return RUNNER_ERROR, ("the validator produced no parseable JSON (exit %d): %s"
                              % (code, stderr))
    status = report.get("status")
    if status == "RUNNER_ERROR":
        errors = report.get("runner_errors") or ["unspecified"]
        return RUNNER_ERROR, str(errors[0])[:200]
    if "total" not in report or "passed" not in report:
        return RUNNER_ERROR, "the validator verdict has no counts (exit %d)" % code
    if report["passed"] < report["total"]:
        first = report["failed"][0] if report.get("failed") else {}
        return DETECTED, "%d/%d, first failure: %s" % (
            report["passed"], report["total"], first.get("name", "?"))
    return ESCAPED, "%d/%d and nothing failed" % (report["passed"], report["total"])


def main():
    verbose = "--verbose" in sys.argv
    as_json = "--json" in sys.argv
    out = [] if as_json else None

    def say(line):
        if not as_json:
            print(line)

    with tempfile.TemporaryDirectory() as tmp:
        root = build_root(tmp)

        # The PRISTINE COPIED CONTROL. Not the working tree: the copy itself, with the
        # registry root pinned to it. Until this passes, every mutation result below is
        # meaningless, so nothing is counted and nothing is reported as caught.
        control, code, stderr = run_validator(root)
        if control is None:
            say("CONTROL: the copied fixture produces no verdict (exit %d)\n%s" % (code, stderr))
            if as_json:
                sys.stdout.write(json.dumps(
                    {"control": "RUNNER_ERROR", "detail": stderr, "probes": []}, indent=2)
                    + "\n")
            return 2
        if control["passed"] < control["total"]:
            failures = [f["name"] for f in control.get("failed", [])][:8]
            say("CONTROL: the copied fixture FAILS %d/%d before any mutation: %s"
                % (control["total"] - control["passed"], control["total"], failures))
            if as_json:
                sys.stdout.write(json.dumps(
                    {"control": "FAILED", "passed": control["passed"],
                     "total": control["total"], "failed": failures, "probes": []}, indent=2)
                    + "\n")
            return 2
        say("control (pristine copy): %d/%d PASS\n" % (control["passed"], control["total"]))

        outcomes = []
        for entry in PROBES:
            target = os.path.join(root, entry["path"])
            original = open(target, encoding="utf-8").read()
            mutated, applied = original, 0
            for pattern, replacement, count in entry["edits"]:
                mutated, n = re.subn(pattern, replacement, mutated, count=count,
                                     flags=re.MULTILINE)
                applied += n
            if applied < len(entry["edits"]) or mutated == original:
                outcomes.append((entry["name"], REDUNDANT,
                                 "the pattern matched nothing; the probe is dead",
                                 entry["expect"]))
                say("  %-13s %s" % (REDUNDANT, entry["name"]))
                continue
            try:
                open(target, "w", encoding="utf-8").write(mutated)
                outcome, detail = classify(root)
            finally:
                open(target, "w", encoding="utf-8").write(original)
            outcomes.append((entry["name"], outcome, detail, entry["expect"]))
            if outcome == entry["expect"]:
                if verbose:
                    say("  %-13s %s" % (outcome, entry["name"]))
            else:
                say("  %-13s %s  (expected %s; %s)"
                    % (outcome, entry["name"], entry["expect"], detail))

    counts = {DETECTED: 0, ESCAPED: 0, REDUNDANT: 0, RUNNER_ERROR: 0}
    for _name, outcome, _detail, _expect in outcomes:
        counts[outcome] += 1
    #: A probe is SATISFIED when it got the outcome it asserts. That is not the same as being
    #: DETECTED: the RuntimeError probe asserts RUNNER_ERROR, and counting it as a detection
    #: would be exactly the dishonesty it exists to rule out.
    unsatisfied = [(n, o, d, e) for n, o, d, e in outcomes if o != e]

    if as_json:
        sys.stdout.write(json.dumps({
            "control": "PASS",
            "control_passed": control["passed"], "control_total": control["total"],
            "total_probes": len(PROBES), "counts": counts,
            "satisfied": len(PROBES) - len(unsatisfied),
            "probes": [{"name": n, "outcome": o, "detail": d, "expected": e}
                       for n, o, d, e in outcomes],
        }, indent=2) + "\n")
    else:
        print("\n=== %d DETECTED, %d ESCAPED, %d REDUNDANT, %d RUNNER_ERROR of %d probes ==="
              % (counts[DETECTED], counts[ESCAPED], counts[REDUNDANT], counts[RUNNER_ERROR],
                 len(PROBES)))
        print("=== %d/%d probes returned the outcome they assert ==="
              % (len(PROBES) - len(unsatisfied), len(PROBES)))
        if unsatisfied:
            print("\nDid not return the asserted outcome:")
            for name, outcome, detail, expect in unsatisfied:
                print("  - %s: got %s, expected %s (%s)" % (name, outcome, expect, detail))
    return 0 if not unsatisfied else 1


if __name__ == "__main__":
    sys.exit(main())
