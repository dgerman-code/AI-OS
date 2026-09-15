"""Phase 16 — authoritative, read-only views of the approved registries.

Status: PROPOSED. Nothing here writes, registers, promotes or widens anything: a capability
absent from an approved registry is absent, and this module has no path that could add one.

An identity is eligible here only from explicit evidence. Phase-level architecture approval is
never promoted into individual Skill approval. Mentioned, candidate, superseded, example and
boundary-only identities remain ineligible.
"""

from __future__ import annotations

import os
import re
from typing import Dict, Optional, Set, Tuple

REPO = os.environ.get("PHASE_16_REPO_ROOT") or os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_NON_CARD_DIRS = ("_templates", "_standards")
_DECLARATION = r"(?m)^- %s ID: \*{0,2}`(%s\.[a-z0-9_]+)`"
_VERSION = re.compile(r"(?m)^- Version: (\S+)\s*$")
_CARD_STATUS = re.compile(r"(?m)^- Status:\s*([A-Z_ -]+?)\s*$")
_SUPERSEDED_BY = re.compile(r"(?m)^- Superseded By: (.+?)\s*$")
_BOTH_WAYS = re.compile(r"(?m)^- Supersedes / Superseded By: (.+?)\s*$")


class RegistryEvidenceError(Exception):
    """The approval evidence for a registry could not be read. Callers fail closed."""


class _Kind:
    def __init__(self, prefix: str, label: str, root: str,
                 approval_record: str, approved_scope_phrase: str):
        self.prefix = prefix
        self.label = label
        self.root = root
        self.approval_record = approval_record
        self.approved_scope_phrase = approved_scope_phrase


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

_ROLE_UNIVERSE = os.path.join("roles", "master-role-universe.md")
_APPROVED_ROLE_COUNT = 59


def _read(relative: str) -> str:
    with open(os.path.join(REPO, relative), encoding="utf-8") as handle:
        return handle.read()


def _approval_is_recorded(kind: _Kind) -> bool:
    try:
        body = _read(kind.approval_record)
    except OSError:
        return False
    flat = body.replace("*", "")
    if "Status: APPROVED — HUMAN DECISION" not in flat:
        return False
    return kind.approved_scope_phrase in flat


def _cards(kind: _Kind) -> Dict[str, Tuple[str, str, str]]:
    declaration = re.compile(_DECLARATION % (kind.label, kind.prefix))
    name_line = re.compile(r"(?m)^- %s Name: (.+?)\s*$" % kind.label)
    found: Dict[str, Tuple[str, str, str]] = {}
    base = os.path.join(REPO, kind.root)
    if not os.path.isdir(base):
        return found
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
                continue
            identity = declared.group(1)
            version = _VERSION.search(body)
            if version is None or _is_superseded(body):
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


def _explicit_individual_skill_approval(identity: str, card_path: str) -> bool:
    """True only for an individually approved Skill with an explicit human approval record.

    Phase 4 explicitly approves the registry architecture while denying mass individual
    promotion. Therefore its phase-level record can never satisfy this function.
    """
    try:
        card = _read(card_path)
    except OSError:
        return False
    status = _CARD_STATUS.search(card)
    if status is None or status.group(1).strip() != "APPROVED":
        return False

    reviews_root = os.path.join(REPO, "reviews")
    if not os.path.isdir(reviews_root):
        return False
    for root, _dirs, files in os.walk(reviews_root):
        for name in files:
            if not name.endswith(".md") or name == "phase-4-final-approval.md":
                continue
            path = os.path.join(root, name)
            try:
                body = open(path, encoding="utf-8").read()
            except OSError:
                continue
            flat = body.replace("*", "")
            if ("Status: APPROVED — HUMAN DECISION" in flat
                    and identity in body
                    and re.search(r"(?i)\b(approve|approved|approval)\b", body)):
                return True
    return False


def _registered(kind_name: str) -> Dict[str, Tuple[str, str, str]]:
    kind = KINDS[kind_name]
    cards = _cards(kind)
    if kind_name == "skill":
        # Architecture approval alone is deliberately insufficient for individual Skills.
        return {identity: data for identity, data in cards.items()
                if _explicit_individual_skill_approval(identity, data[2])}
    if not _approval_is_recorded(kind):
        return {}
    return cards


def carded_skills() -> Set[str]:
    """Declared, versioned, non-superseded Skill cards, regardless of approval state."""
    return set(_cards(KINDS["skill"]))


def approved_roles() -> Set[str]:
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
    """Only Skills with explicit individual approval evidence.

    The Phase 4 architecture approval is not individual Skill approval. In the current approved
    history this may legitimately be empty; callers must fail closed rather than infer approval.
    """
    return set(_registered("skill"))


def approved_review_profiles() -> Set[str]:
    return set(_registered("review"))


def approved_decision_rights() -> Set[str]:
    return set(_registered("decision"))


def approved_workflows() -> Dict[str, str]:
    return {k: v for k, (v, _n, _p) in _registered("workflow").items()}


def card_path(kind_name: str, identity: str) -> Optional[str]:
    entry = _registered(kind_name).get(identity)
    return entry[2] if entry else None


_MAPPING_RECORDS = (
    os.path.join("skills", "mappings", "wave-1-exemplar-role-skill-mapping.md"),
    os.path.join("skills", "mappings", "wave-2-domain-completion-role-skill-mapping.md"),
)
_RELATIONSHIPS = ("REQUIRED_CORE", "REQUIRED_FOR_CONTEXT", "OPTIONAL", "ALTERNATIVE",
                  "PROHIBITED_IN_CONTEXT")
COMPATIBLE_RELATIONSHIPS = ("REQUIRED_CORE", "REQUIRED_FOR_CONTEXT", "OPTIONAL", "ALTERNATIVE")
_NEGATIVE = re.compile(
    r"(?i)\b(not mapped|not assigned|does not map|do not map|prohibited|excluded|not applicable)\b")


def role_skill_mappings() -> Dict[str, Dict[str, str]]:
    """Positive-evidence-only Role→Skill mappings from authoritative mapping records.

    Any heading that is not an exact relationship heading resets relationship state. Boundary,
    exclusion, examples, counterexamples and narrative sections cannot inherit the previous
    relationship. Explicit negative wording can only deny; it never creates a positive mapping.
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

            any_heading = re.match(r"^#{2,6}\s+(.+?)\s*$", line)
            if any_heading:
                heading_text = any_heading.group(1).strip()
                relationship = heading_text if heading_text in _RELATIONSHIPS else None
                continue

            entry = re.match(r"^-\s+`(skill\.[a-z0-9_]+)`(?:\s*[-—:]\s*(.*))?$", line)
            if not (entry and current_role and relationship):
                continue
            skill = entry.group(1)
            trailing = entry.group(2) or ""
            effective = "PROHIBITED_IN_CONTEXT" if _NEGATIVE.search(trailing) else relationship
            # A later explicit prohibition overrides an earlier positive relationship.
            prior = mappings.setdefault(current_role, {}).get(skill)
            if prior == "PROHIBITED_IN_CONTEXT":
                continue
            mappings[current_role][skill] = effective
    return mappings


def skill_is_compatible_with_role(skill_ref: str, role_ref: str) -> Tuple[bool, str]:
    relationship = role_skill_mappings().get(role_ref, {}).get(skill_ref)
    if relationship is None:
        return False, ("no authoritative Role-to-Skill mapping records %s for %s"
                       % (skill_ref, role_ref))
    if relationship not in COMPATIBLE_RELATIONSHIPS:
        return False, ("%s is %s for %s" % (skill_ref, relationship, role_ref))
    return True, relationship
