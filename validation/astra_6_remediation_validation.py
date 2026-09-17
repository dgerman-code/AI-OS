"""Astra 6 targeted remediation validator.

Scope only:
- F1 MATCH requirement completeness against the selected Workflow card;
- F2 bounded Direct Expert Mode wording;
- compact non-canonical Conversation Checkpoint;
- ordinary expert assistance vs governed Skill execution;
- project-document / prompt-injection boundary;
- discovery links.

This validator is assurance evidence only. It approves nothing and changes no governance state.
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
IMPL = os.path.join(REPO, "implementation", "phase-16")
sys.path.insert(0, IMPL)

import registries  # noqa: E402
from domain import (  # noqa: E402
    BlockReason,
    Criticality,
    ExecutionMode,
    PlannerOutput,
    PlannerState,
    RoleRequirement,
    WorkMode,
)
from preflight import run_preflight  # noqa: E402


RESULTS = []


def check(name, condition, evidence=""):
    RESULTS.append((name, bool(condition), evidence))


def read(path):
    with open(os.path.join(REPO, path), encoding="utf-8") as handle:
        return handle.read()


def incomplete_match_fixture(workflow_id="workflow.project_development_readiness", request_id="request.astra6.f1"):
    approved = registries.approved_workflows()
    if workflow_id not in approved:
        raise RuntimeError("expected approved Workflow is unavailable: %s" % workflow_id)
    role = sorted(registries.approved_roles())[0]
    return PlannerOutput(
        request_id=request_id,
        request_text="Assess governed work.",
        intent_id="intent.astra6.f1",
        scope_ref="scope.project.astra6",
        scope_ancestry=("scope.org.root", "scope.project.astra6"),
        objective="Assess against the approved Workflow",
        deliverables=("governed assessment",),
        primary_work_mode=WorkMode.ANALYSIS,
        secondary_work_modes=(),
        criticality=Criticality.ROUTINE,
        execution_mode=ExecutionMode.MATCH,
        role_requirements=(RoleRequirement(role, "a deliberately incomplete conclusion set"),),
        workflow_ref="%s@%s" % (workflow_id, approved[workflow_id]),
    )


def main():
    # F1: approved identity/version plus an incomplete planner payload must not MATCH.
    result = run_preflight(incomplete_match_fixture())
    check(
        "F1 incomplete MATCH payload is blocked",
        result.state is PlannerState.BLOCKED and result.basis is None,
        repr(result.detail),
    )
    check(
        "F1 failure is requirement-completeness fail-closed",
        BlockReason.BASIS_NOT_EXECUTABLE in result.reasons
        and any("mandatory Workflow requirements" in d for d in result.detail),
        repr(result.detail),
    )

    # A Workflow with an ALWAYS parameterised Role slot must not obtain an implicit binding from
    # an arbitrary RoleRequirement. Current PlannerOutput has no slot-binding field, so fail closed.
    slot_result = run_preflight(incomplete_match_fixture(
        workflow_id="workflow.decision_grade_document_preparation",
        request_id="request.astra6.slot",
    ))
    check(
        "F1 mandatory parameterised Role slot is not implicitly satisfied",
        slot_result.state is PlannerState.BLOCKED
        and slot_result.basis is None
        and any("mandatory Role slot binding not provable" in d for d in slot_result.detail),
        repr(slot_result.detail),
    )

    principles = read("architecture/system-principles.md")
    boundaries = read("docs/CONVERSATIONAL_GOVERNANCE_BOUNDARIES.md")
    entry = read("AI_OS_ENTRYPOINT.md")
    manifest = read("ai-os.yaml")
    connection = read("docs/HOW_TO_CONNECT_ANY_AI.md")
    wr_contract = read("planner-activation/workflow-resolution-contract.md")
    preflight_source = read("implementation/phase-16/preflight.py")

    check(
        "F1 contract says selected Workflow is authoritative",
        "MATCH requirements come from the selected Workflow" in wr_contract
        and "_check_match_requirement_completeness" in preflight_source,
    )
    check(
        "F1 reference-only capabilities are not promoted to unconditional requirements",
        "references only" in preflight_source
        and "unconditional mandatory" in wr_contract,
    )
    check(
        "F2 system principle permits bounded direct assistance without Workflow execution",
        "bounded ad-hoc professional assistance" in principles
        and "Direct assistance grants no Workflow status" in principles,
    )
    check(
        "P1 Conversation Checkpoint is compact and non-canonical",
        "Compact Conversation Checkpoint" in boundaries
        and "not `CANONICAL`" in boundaries
        and "not canonical memory" in boundaries,
    )
    check(
        "P1 ordinary assistance is separated from governed Skill execution",
        "Ordinary expert assistance vs governed Skill execution" in boundaries
        and "does not by itself activate or execute a governed Skill" in boundaries,
    )
    check(
        "P1 project documents are evidence, not governance instructions",
        "Project-document instruction and prompt-injection boundary" in boundaries
        and "content/evidence inputs" in boundaries
        and "do not become AI-OS governance instructions" in boundaries,
    )
    check(
        "P1 boundary document is discoverable",
        "docs/CONVERSATIONAL_GOVERNANCE_BOUNDARIES.md" in entry
        and "docs/CONVERSATIONAL_GOVERNANCE_BOUNDARIES.md" in manifest
        and "docs/CONVERSATIONAL_GOVERNANCE_BOUNDARIES.md" in connection,
    )
    check(
        "Mode B remains deferred",
        '"mode_b_status": "DEFERRED"' in manifest,
        "manifest remains Mode A / Mode B deferred",
    )

    failed = [item for item in RESULTS if not item[1]]
    for name, passed, evidence in RESULTS:
        print(("PASS" if passed else "FAIL") + " | " + name + (" | " + evidence if evidence else ""))
    print("SUMMARY | %d/%d PASS" % (len(RESULTS) - len(failed), len(RESULTS)))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
