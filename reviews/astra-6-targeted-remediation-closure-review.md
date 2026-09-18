# Astra 6 — Targeted Remediation Closure Review

Status: `CLOSURE REVIEW PASS — TARGETED SCOPE`
Date: 2026-09-17
Review type: independent closure pass over the remediation delta
Base: `a489efe55aa1088f2e8a19c39bc58c2c34c7dbc5`
Branch: `remediation/astra-6-targeted`

## Review boundary

This review is intentionally separate from implementation sequencing. It assesses only the six Astra 6 remediation items requested by the human and the stated constraints. It does not re-open approved phases, redesign AI-OS, approve governance state, or evaluate Mode B.

The branch comparison is cleanly based on the requested `main` SHA with no behind commits at review time. No Pull Request was created.

## Closure findings

| Item | Finding | Closure evidence |
|---|---|---|
| P0 F1 — MATCH trusts incomplete planner payload | **PASS** | `implementation/phase-16/preflight.py` now resolves the selected approved Workflow card and compares mandatory Workflow-declared static requirement references against `PlannerOutput`. Omitted concrete `ALWAYS` Roles, Review references, Decision Right references and artifact preconditions fail closed with no Execution Basis. An `ALWAYS` parameterised Role slot that cannot be proven by the present PlannerOutput contract also fails closed rather than being implicitly satisfied. `planner-activation/workflow-resolution-contract.md` records the same rule. |
| P0 F2 — Direct Expert Mode conflicts with system principle | **PASS** | `architecture/system-principles.md` now allows bounded ad-hoc professional assistance without Workflow execution while explicitly denying Workflow status, governed Skill eligibility or authority. |
| P1 — compact long-chat checkpoint | **PASS** | `docs/CONVERSATIONAL_GOVERNANCE_BOUNDARIES.md` defines a compact Conversation Checkpoint and explicitly keeps it non-canonical, non-evidentiary and subordinate to governed sources. |
| P1 — ordinary expert assistance vs governed Skill execution | **PASS** | The same boundary document distinguishes Role-based ordinary assistance from a governed Skill run, including claim-level restrictions and re-resolution when the task grows into governed execution. |
| P1 — document instruction / prompt-injection boundary | **PASS** | Project documents, uploads, web pages, email and evidence packs are defined as content/evidence inputs. Embedded imperative/system-like text cannot override AI-OS governance, eligibility or authority. |
| P1 — status/discovery | **PASS** | Discovery is wired through `AI_OS_ENTRYPOINT.md`, `ai-os.yaml` and `docs/HOW_TO_CONNECT_ANY_AI.md`. `SYSTEM_STATUS.md` is updated by the final remediation status commit. |

## F1 interpretation check

The review specifically checked two edge cases that could otherwise leave F1 partially open:

1. **Parameterized mandatory Role slots.** `workflow.decision_grade_document_preparation` declares `SLOT.document_owner` as `ALWAYS`. The current PlannerOutput schema cannot prove that slot's ownership/cardinality constraints, so the remediated preflight refuses to infer a binding and fails closed. No new slot registry or Role was introduced.
2. **Skills / Packs / Specialisations.** The inspected exemplar Workflow cards explicitly label their `Activated Skills / Packs` sections as **references only**. The remediation therefore does not incorrectly turn those reference lists into unconditional mandatory requirements. When such capabilities are actually activated, existing Phase 4 / Phase 16 eligibility rules still apply.

## Regression-harness check

The historical Phase 16 core validator contains an old positive fixture asserting that an approved Workflow identity/version alone "proceeds". That expectation is incompatible with Astra 6 F1 by design.

The historical core was left untouched. `validation/phase_16_validation.py` now transparently treats that single expectation as `superseded` **only when** `validation/astra_6_remediation_validation.py` passes. Any other legacy failure remains a failure. This is a narrow compatibility bridge, not a rewrite of the approved historical validator.

## Controlled conversational test

`tests/ASTRA_6_CONTROLLED_MULTI_TURN_TEST.md` records an eight-turn controlled conformance sequence covering:

- bounded project continuation;
- explicit Direct Expert Mode;
- attempted relabelling of ordinary assistance as governed Skill execution;
- document-embedded prompt injection;
- creation and later reuse of a non-canonical Conversation Checkpoint;
- incomplete MATCH payload;
- objective expansion beyond a matched Workflow.

Recorded result: `8/8 PASS`.

## Constraint audit

- No redesign: **PASS**
- No new Roles: **PASS**
- No new expert activation registry: **PASS**
- Mode B unchanged/deferred: **PASS**
- Approved phase semantics not broadly rewritten: **PASS** — only the Phase 16 wrapper is narrowly bridged because the old positive MATCH fixture is superseded by F1.
- Separate remediation branch: **PASS**
- No PR without human command: **PASS**

## Execution-evidence note

No GitHub Actions/status checks are configured for this branch in the connected repository view, and this environment does not have a local checkout/network path from which to execute the Python validators. The targeted validator was therefore reviewed structurally and wired into the Phase 16 wrapper, but this closure record does **not** falsely claim a remote CI execution that did not occur.

This limitation does not change the code-review verdict, but a merge decision should use an actual local/CI run of:

```text
python3 validation/astra_6_remediation_validation.py
python3 validation/phase_16_validation.py
```

as execution evidence.

## Closure verdict

**PASS — TARGETED REMEDIATION SCOPE CLOSED AT CODE / GOVERNANCE-CONTRACT LEVEL.**

No additional Astra 6 scope expansion is recommended. The only remaining evidence step is execution of the already-added deterministic validators in an environment with a repository checkout; that is verification, not additional design/remediation.
