# Astra-6 Targeted Remediation Candidate

Status: `READY FOR VALIDATION — NOT HUMAN APPROVED`

Baseline reviewed by Astra-6: `a489efe55aa1088f2e8a19c39bc58c2c34c7dbc5`

Working branch: `remediation/astra-6-targeted-fixes`

## Purpose

This record tracks only the targeted remediation arising from the independent Astra-6 review. It does not reopen unrelated approved phases and does not itself create human approval.

## Findings addressed

### F1 — Workflow requirement omission

Implemented a read-only Workflow contract extractor plus MATCH preflight completeness checks. A valid Workflow identity/version is no longer sufficient by itself: omitted mandatory Workflow Roles, REQUIRED_CORE Skills, Review references, Decision Right references and explicit artifact preconditions block issuance. Referenced Review Profiles and Decision Rights must also resolve in the approved registries.

Regression tests: `implementation/phase-16/tests/test_workflow_requirement_completeness.py`.

Important validation point: the historical positive MATCH fixture predates requirement-completeness enforcement and may require fixture remediation so that it represents a genuinely complete MATCH rather than relying on the former omission behaviour. Do not weaken the new completeness check merely to preserve a false-positive historical fixture.

### F2 — Direct Expert Mode vs constitutional activation wording

`architecture/system-principles.md` now distinguishes:

- governed execution: Role participation through an admissible Workflow or governed Work Plan; and
- bounded ad-hoc professional assistance: direct task-level Role resolution without claiming Workflow execution, Skill execution eligibility, Review satisfaction, canonical status or authority.

Direct Expert Mode is a routing preference, not a governance override.

This is a semantic clarification and therefore requires human acceptance before becoming an approved baseline.

### F3 — continuity / audit retention

Added `docs/CONVERSATION_CHECKPOINT.md` with stable scope identity, source/version pointers, last verification point, unresolved items and next action. It explicitly remains non-canonical and requires truthful disclosure when historical provenance was not retained.

No new storage system or registry was introduced.

### F4 — ordinary assistance vs governed Skill execution

Entry point, system principles, checklist and conversational model now distinguish supplied-number arithmetic / bounded expert assistance from decision-grade governed execution. Ordinary assistance cannot be used to imply Skill approval or lender-grade execution.

### F5 — conversational acceptance evidence

Added `tests/ASTRA6_REMEDIATION_ACCEPTANCE.md` covering multi-turn continuity, same-name project collisions, material objective changes, output modes, ad-hoc expert use and embedded-document instruction attacks.

The test plan is not a pass result. Representative external-provider runs and retained outputs remain required before stronger conversational reliability claims.

### F6 — stale status

Updated `SYSTEM_STATUS.md`, `README.md`, `ai-os.yaml` and discovery guidance to reflect Phase 18 approval, the recorded cold-start result and the distinction between approved core and later conversational/remediation changes.

### Embedded source instruction hardening

Added `docs/DOCUMENT_INSTRUCTION_BOUNDARY.md`. Instructions inside documents, attachments, quotations or imported content are treated as evidence/content and cannot change AI-OS governance, repository permission or external-action authority.

## Explicitly unchanged

- 59-role approved professional universe;
- Role / Skill / Review Profile / Decision Right separation;
- Workflow MATCH vs instance-level COMPOSE distinction;
- Decision Rights and human authority;
- zero automatic Skill approvals;
- provider-neutral Mode A architecture;
- Mode B deferred status;
- historical approval records.

## Required closure sequence

1. Run targeted Phase 16 regression tests and relevant existing tests.
2. Confirm the Astra-6 F1 negative probe now fails closed.
3. Resolve any historical test fixture that encoded the old omission behaviour; do not weaken completeness semantics.
4. Run the Mode A Phase 17/18 validators as regression checks.
5. Execute representative multi-turn conversational acceptance tests with retained outputs.
6. Obtain one independent closure review.
7. Human decides whether to approve this remediation as a new baseline and whether to move it to `main`.

No PR or merge is authorised by this record.
