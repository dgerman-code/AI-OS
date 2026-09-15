"""Phase 16 — authoritative, read-only views of the approved registries.

Status: PROPOSED. Nothing here writes, registers, promotes or widens anything: a capability
absent from an approved registry is absent, and this module has no path that could add one.

WHY THIS MODULE WAS REWRITTEN. The first version derived Role IDs by slugging display names out
of the master universe list, and derived every other identity by scraping backticked tokens out
of whole documents. Both are mention-based, and mention-based parsing INVENTS eligibility:

  * slugging produced `role.asset_o_m_technical_operations_specialist`,
    `role.esg_e_s_specialist` and `role.fp_a_management_finance_specialist`, none of which is a
    declared Role ID - the ampersands in "Asset O&M", "ESG / E&S" and "FP&A" were split into
    separate words;
  * scraping counted prose references, candidate IDs held in consolidation groups, worked
    examples, counter-examples and even `Supersedes:` lines naming RETIRED identities, and
    reported them as approved - 224 Skills, 44 Review Profiles, 97 Decision Rights and 57
    Workflows, where the approved carded sets are 6, 6, 8 and 4.

An identity is eligible here only when THREE things hold, all of them evidence and none of them
inference:

  1. a card DECLARES the identity, in its Identity block, as `- <Kind> ID: `<prefix>.<id>``;
  2. the card declares a Version, and is not superseded;
  3. a human approval record covers that card class, by its own approved-scope wording.

Anything else - an uncarded universe entry, a prose mention, a candidate in an overlap group, a
retired ID named by a `Supersedes:` line, a template - is NOT eligible, and the caller gets a
refusal rather than a silent pass. If the approval evidence for a kind cannot be read, that
kind resolves to the empty set: fail closed, never fail open.
"""

from __future__ import annotations

import os
import re
from typing import Dict, Optional, Set, Tuple

#: The repository root. Overridable so the mutation harness can run this code against a
#: throwaway COPY of the tree; without it a probe would silently read the real repository and
#: the fixture would be invalid. Nothing else reads the variable.
REPO = os.environ.get("PHASE_16_REPO_ROOT") or os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#: Directories that hold templates and shared standards, never registered identities.
_NON_CARD_DIRS = ("_templates", "_standards")

#: `- Role ID: `role.x`` and `- Decision ID: **`decision.x`**` are the same declaration; the
#: emphasis is typography. Nothing else in a document is a declaration.
_DECLARATION = r"(?m)^- %s ID: \*{0,2}`(%s\.[a-z0-9_]+)`"
_VERSION = re.compile(r"(?m)^- Version: (\S+)\s*$")
_SUPERSEDED_BY = re.compile(r"(?m)^- Superseded By: (.+?)\s*$")
_BOTH_WAYS = re.compile(r"(?m)^- Supersedes / Superseded By: (.+?)\s*$")


class RegistryEvidenceError(Exception):
    """The approval evidence for a registry could not be read. Callers fail closed."""


class _Kind:
    """One registered identity class, with the human approval record that covers it."""

    def __init__(self, prefix: str, label: str, root: str,
                 approval_record: str, approved_scope_phrase: str):
        self.prefix = prefix
        self.label = label
        self.root = root
        self.approval_record = approval_record
        self.approved_scope_phrase = approved_scope_phrase


#: Approval evidence, one record per kind, quoted from that record's own approved scope. A
#: phrase that stops appearing in its record takes the whole kind to empty rather than leaving
#: the registry to assert an approval nobody gave.
KINDS = {
    "role": _Kind("role", "Role", "roles",
                  os.path.join("reviews", "phase-3-final-approval.md"),
                  "59 unique Role IDs"),
    "skill": _Kind("skill", "Skill", "skills",
                   os.path.join("reviews", "phase-4-final-approval.md"),
                   "the current selective exemplar card set"),
    "review": _Kind("review", "Review", "reviews",
                    os.path.join("reviews", "phase-6-final-approval.md"),
                    "the six exemplar Review Profiles"),
    "decision": _Kind("decision", "Decision", "decisions",
                      os.path.join("reviews", "phase-7-final-approval.md"),
                      "the eight exemplar Decision Right Cards"),
    "workflow": _Kind("workflow", "Workflow", "workflows",
                      os.path.join("reviews", "phase-5-final-approval.md"),
                      "the four exemplar Workflow Cards"),
}

#: The approved Role universe document, used only to CROSS-CHECK the carded Roles. A Role that
#: is carded but absent from the approved universe is not approved; a universe entry with no
#: card has no resolvable identity. Either mismatch empties the Role registry.
_ROLE_UNIVERSE = os.path.join("roles", "master-role-universe.md")
_APPROVED_ROLE_COUNT = 59


def _read(relative: str) -> str:
    with open(os.path.join(REPO, relative), encoding="utf-8") as handle:
        return handle.read()


def _approval_is_recorded(kind: _Kind) -> bool:
    """Is there a human approval record, marked APPROVED, whose scope names this card class?"""
    try:
        body = _read(kind.approval_record)
    except OSError:
        return False
    flat = body.replace("*", "")
    if "Status: APPROVED — HUMAN DECISION" not in flat:
        return False
    return kind.approved_scope_phrase in flat


def _cards(kind: _Kind) -> Dict[str, Tuple[str, str, str]]:
    """Declared identities of one kind: id -> (version, display name, card path)."""
    declaration = re.compile(_DECLARATION % (kind.label, kind.prefix))
    name_line = re.compile(r"(?m)^- %s Name: (.+?)\s*$" % kind.label)
    found: Dict[str, Tuple[str, str, str]] = {}
    base = os.path.join(REPO, kind.root)
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in _NON_CARD_DIRS]
        if any(part in _NON_CARD_DIRS for part in root.split(os.sep)):
            continue
        for name in sorted(files):
            if not name.endswith(".md"):
                continue
            path = os.path.join(root, name)
            with open(path, encoding="utf-8") as handle:
                body = handle.read()
            declared = declaration.search(body)
            if declared is None:
                continue                      # a universe, a mapping, an audit note: not a card
            identity = declared.group(1)
            version = _VERSION.search(body)
            if version is None:
                continue                      # no version evidence: not resolvable, fail closed
            if _is_superseded(body):
                continue
            display = name_line.search(body)
            found[identity] = (version.group(1),
                               display.group(1) if display else "",
                               os.path.relpath(path, REPO))
    return found


def _is_superseded(body: str) -> bool:
    for pattern in (_SUPERSEDED_BY, _BOTH_WAYS):
        found = pattern.search(body)
        if found and found.group(1).strip().lower() not in ("none", "none / none"):
            return True
    return False


def _registered(kind_name: str) -> Dict[str, Tuple[str, str, str]]:
    kind = KINDS[kind_name]
    if not _approval_is_recorded(kind):
        return {}                              # no approval evidence, no registry. Fail closed.
    return _cards(kind)


# --------------------------------------------------------------------------- public views


def approved_roles() -> Set[str]:
    """The approved 59-Role universe, from the 59 Role Cards that declare their own IDs.

    Cross-checked in both directions against the approved master universe by DISPLAY NAME, and
    against the count the Phase 3 approval record states. Any mismatch empties the registry:
    a Role universe that silently gained or lost a member is not one this phase may read.
    """
    cards = _registered("role")
    if not cards:
        return set()
    try:
        listed = set(re.findall(r"(?m)^\d+\.\s+(.+?)\s*$", _read(_ROLE_UNIVERSE)))
    except OSError:
        return set()
    carded_names = {display for _v, display, _p in cards.values()}
    if len(cards) != _APPROVED_ROLE_COUNT or carded_names != listed:
        return set()
    return set(cards)


def role_versions() -> Dict[str, str]:
    return {k: v for k, (v, _n, _p) in _registered("role").items()}


def approved_skills() -> Set[str]:
    """Carded Skills only. The Master Skill Universe is a candidate list, not a registry.

    Its own Phase 4 approval record says in terms that the phase approval is not a mass status
    promotion of universe entries, so an uncarded Skill ID is not assignable here.
    """
    return set(_registered("skill"))


def approved_review_profiles() -> Set[str]:
    """Carded Review Profiles only. The universe document calls itself a candidate list."""
    return set(_registered("review"))


def approved_decision_rights() -> Set[str]:
    """Carded Decision Rights only. Uncarded candidates are not exercisable identities."""
    return set(_registered("decision"))


def approved_workflows() -> Dict[str, str]:
    """Approved `workflow.<id>` -> the exact version its card declares.

    The version is evidence, not a default. The previous view invented `1` for every Workflow,
    so a MATCH at a version nobody approved resolved successfully.
    """
    return {k: v for k, (v, _n, _p) in _registered("workflow").items()}


def card_path(kind_name: str, identity: str) -> Optional[str]:
    """Where the declaration lives. Provenance, for a refusal that has to name its evidence."""
    entry = _registered(kind_name).get(identity)
    return entry[2] if entry else None


# --------------------------------------------------------------------------- role <-> skill


#: The Phase 4 mapping records state in terms that they are "the sole authoritative source for
#: relationship type", so Skill-to-Role compatibility is read from them and from nowhere else.
_MAPPING_RECORDS = (
    os.path.join("skills", "mappings", "wave-1-exemplar-role-skill-mapping.md"),
    os.path.join("skills", "mappings", "wave-2-domain-completion-role-skill-mapping.md"),
)

_RELATIONSHIPS = ("REQUIRED_CORE", "REQUIRED_FOR_CONTEXT", "OPTIONAL", "ALTERNATIVE",
                  "PROHIBITED_IN_CONTEXT")

#: A relationship that makes the Skill usable by that Role. PROHIBITED_IN_CONTEXT is exactly
#: the case the check exists for, so it is absent by design.
COMPATIBLE_RELATIONSHIPS = ("REQUIRED_CORE", "REQUIRED_FOR_CONTEXT", "OPTIONAL", "ALTERNATIVE")


def role_skill_mappings() -> Dict[str, Dict[str, str]]:
    """role id -> {skill id: relationship}, read from the authoritative mapping records.

    A pair that appears in no record is UNMAPPED, and an unmapped pair is not compatible. That
    is the fail-closed reading: the mapping records are the authority on applicability, so
    silence in them is not permission.
    """
    mappings: Dict[str, Dict[str, str]] = {}
    for record in _MAPPING_RECORDS:
        try:
            body = _read(record)
        except OSError:
            continue
        current_role: Optional[str] = None
        relationship: Optional[str] = None
        for line in body.splitlines():
            role = re.match(r"^Role: `(role\.[a-z0-9_]+)`", line)
            if role:
                current_role = role.group(1)
                relationship = None
                continue
            heading = re.match(r"^#{2,4}\s+([A-Z_]+)\s*$", line)
            if heading:
                relationship = heading.group(1) if heading.group(1) in _RELATIONSHIPS else None
                continue
            if line.startswith("## ") and not heading:
                relationship = None
            entry = re.match(r"^-\s+`(skill\.[a-z0-9_]+)`", line)
            if entry and current_role and relationship:
                mappings.setdefault(current_role, {})[entry.group(1)] = relationship
    return mappings


def skill_is_compatible_with_role(skill_ref: str, role_ref: str) -> Tuple[bool, str]:
    """(compatible, why-not). Unmapped and PROHIBITED_IN_CONTEXT both fail closed."""
    relationship = role_skill_mappings().get(role_ref, {}).get(skill_ref)
    if relationship is None:
        return False, ("no authoritative Role-to-Skill mapping records %s for %s"
                       % (skill_ref, role_ref))
    if relationship not in COMPATIBLE_RELATIONSHIPS:
        return False, ("%s is %s for %s" % (skill_ref, relationship, role_ref))
    return True, relationship
