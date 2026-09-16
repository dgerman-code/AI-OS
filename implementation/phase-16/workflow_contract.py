"""Phase 16 — derive minimum MATCH requirements from the selected approved Workflow card.

This module is deliberately read-only. It does not create requirements or widen Workflow
semantics; it reads the approved Workflow definition and exposes the requirements that a planner
must not be allowed to omit when asking preflight to issue a MATCH ExecutionBasis.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import FrozenSet

import registries


@dataclass(frozen=True)
class WorkflowContract:
    mandatory_roles: FrozenSet[str]
    required_reviews: FrozenSet[str]
    required_decisions: FrozenSet[str]
    required_evidence: FrozenSet[str]
    required_skills: FrozenSet[str]


def _section(body: str, heading: str, next_heading: str | None = None) -> str:
    start = body.find(heading)
    if start < 0:
        return ""
    start += len(heading)
    if next_heading is None:
        return body[start:]
    end = body.find(next_heading, start)
    return body[start:] if end < 0 else body[start:end]


def workflow_contract(workflow_id: str) -> WorkflowContract:
    """Return the non-optional requirement surface declared by an approved Workflow.

    The parser intentionally uses only explicit card conventions already present in Phase 5:
    ALWAYS Role rows, PRECONDITION artifact references, REVIEW_REQUIRED_REFERENCE and
    HUMAN_GATE_REFERENCE identities. Required-core Skills are derived from the authoritative
    Role-to-Skill mapping for those mandatory Roles. Conditional Role rows are not promoted to
    mandatory by this function; their activation remains an instance-level determination.
    """
    path = registries.card_path("workflow", workflow_id)
    if path is None:
        raise registries.RegistryEvidenceError(
            "approved Workflow card cannot be resolved: %s" % workflow_id)
    with open(os.path.join(registries.REPO, path), encoding="utf-8") as handle:
        body = handle.read()

    roles_block = _section(body, "## Participating Roles", "## Composed Workflow References")
    mandatory_roles = frozenset(re.findall(
        r"(?m)^\|\s*`(role\.[a-z0-9_]+)`\s*\|[^\n]*?\|\s*`ALWAYS`\s*\|",
        roles_block,
    ))

    preconditions = _section(body, "## Preconditions", "## Scope")
    required_evidence = frozenset(re.findall(
        r"`(artifact\.[a-z0-9_]+)`", preconditions
    ))

    required_reviews = frozenset(re.findall(
        r"REVIEW_REQUIRED_REFERENCE`?\s*(?:→|->)\s*`(review\.[a-z0-9_]+)`",
        body,
    ))
    required_decisions = frozenset(re.findall(
        r"HUMAN_GATE_REFERENCE`?\s*(?:→|->)\s*`(decision\.[a-z0-9_]+)`",
        body,
    ))

    mappings = registries.role_skill_mappings()
    required_skills = frozenset(
        skill
        for role in mandatory_roles
        for skill, relationship in mappings.get(role, {}).items()
        if relationship == "REQUIRED_CORE"
    )

    return WorkflowContract(
        mandatory_roles=mandatory_roles,
        required_reviews=required_reviews,
        required_decisions=required_decisions,
        required_evidence=required_evidence,
        required_skills=required_skills,
    )
