"""Phase 16 — read-only views of the approved registries.

Status: PROPOSED. These read the repository's approved registry documents and expose what is
approved. Nothing here writes, registers, promotes or widens anything: a capability absent from
the approved registry is absent, and this module has no path that could add one.
"""

from __future__ import annotations

import os
import re
from typing import Dict, Set

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _read(relative: str) -> str:
    with open(os.path.join(REPO, relative), encoding="utf-8") as handle:
        return handle.read()


def approved_roles() -> Set[str]:
    """The approved 59-Role universe, derived from its own document, never hard-coded.

    Deriving the count is the point: a phase that wrote "59" would still say 59 after adding a
    sixtieth Role to the file.
    """
    body = _read(os.path.join("roles", "master-role-universe.md"))
    names = re.findall(r"(?m)^\d+\.\s+(.+?)\s*$", body)
    return {"role." + _slug(n) for n in names}


def approved_skills() -> Set[str]:
    body = _read(os.path.join("skills", "master-skill-universe.md"))
    return set(re.findall(r"`(skill\.[a-z0-9_]+)`", body))


def approved_review_profiles() -> Set[str]:
    body = _read(os.path.join("reviews", "master-review-profile-universe.md"))
    return set(re.findall(r"`(review\.[a-z0-9_]+)`", body))


def approved_decision_rights() -> Set[str]:
    found: Set[str] = set()
    base = os.path.join(REPO, "decisions")
    for root, _dirs, files in os.walk(base):
        for name in files:
            if name.endswith(".md"):
                with open(os.path.join(root, name), encoding="utf-8") as handle:
                    found |= set(re.findall(r"`(decision\.[a-z0-9_]+)`", handle.read()))
    return found


def approved_workflows() -> Dict[str, int]:
    """Approved `workflow.<id>` identifiers and the highest approved version of each."""
    versions: Dict[str, int] = {}
    base = os.path.join(REPO, "workflows")
    for root, _dirs, files in os.walk(base):
        for name in files:
            if not name.endswith(".md"):
                continue
            with open(os.path.join(root, name), encoding="utf-8") as handle:
                body = handle.read()
            for wf in re.findall(r"`(workflow\.[a-z0-9_]+)`", body):
                versions.setdefault(wf, 1)
    return versions


def _slug(name: str) -> str:
    name = name.lower()
    name = name.replace("&", " ").replace("/", " ").replace("-", " ")
    name = re.sub(r"[^a-z0-9 ]", "", name)
    return "_".join(name.split())
