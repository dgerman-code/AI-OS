# AI-OS

Provider-independent AI Operating System for managing organisations, programmes, projects, ventures, digital products and operational work through reusable professional Roles, Skills, Workflows, evidence, review and explicit human governance.

## Start here

For the current system state and approval boundary, read:

1. `SYSTEM_STATUS.md`
2. `AI_OS_ENTRYPOINT.md`
3. `ai-os.yaml`

If you are connecting an external AI through GitHub, use the approved **Mode A** path and follow `docs/HOW_TO_CONNECT_ANY_AI.md` plus `docs/MODE_A_OPERATIONAL_CHECKLIST.md`.

For long-running conversational work also use:

- `docs/CONVERSATIONAL_OPERATION_MODEL.md`
- `docs/CONVERSATION_CHECKPOINT.md`
- `docs/DOCUMENT_INSTRUCTION_BOUNDARY.md`

## Current operating model

**Mode A — approved current connection mode**

`Human -> external AI -> GitHub AI-OS`

The external AI reads AI-OS from GitHub at a reported ref/commit and works under repository governance. Provider memory, chat history, Conversation Checkpoints and generated output are not canonical AI-OS state by themselves.

**Mode B — deferred**

AI-OS calling/routing model-provider APIs is intentionally deferred. Provider API orchestration, billing, key management, retry/fallback workers, queues and deployment runtime are not part of the current approved operating mode.

## Core principles

- ROLE != MODEL.
- ROLE != AGENT INSTANCE.
- Roles are reusable professional definitions, not permanently active personas.
- Governed execution activates Roles through an admissible Workflow or governed Work Plan.
- Bounded ad-hoc expert assistance may resolve a Role directly without claiming governed Workflow execution, Skill eligibility, review satisfaction or authority.
- Roles, Skills, Workflows and canonical knowledge live outside any individual AI provider.
- Models are replaceable runtimes that temporarily assume Roles.
- Context is isolated by organisation / programme / project / product / workstream / task.
- AI output does not automatically become canonical truth or governance approval.
- Critical authors do not self-approve their own work.
- Delivery, independent assurance and human authority are separate layers.
- New Roles are created only when a distinct methodology, authority boundary, review requirement or recurring professional artifact justifies them.

## Governance and status

Historical phase approval records live under `reviews/`. Phase-level approval does not automatically approve or canonicalise every child artifact. Existence, applicability, validation success and execution eligibility must not be confused with governance approval.

Phases 1–18 have human approval records. The final Mode A cold-start test was executed after Phase 18 approval and recorded in `tests/FINAL_COLD_START_TEST_RESULT.md`.

Later conversational refinements and current targeted remediation are separate post-approval changes and require their own validation/human acceptance before becoming a new approved baseline.

See `SYSTEM_STATUS.md` for the complete current boundary and inherited assurance notes.

## Conversational operation

The conversational layer is designed so ordinary users do not need to see internal governance mechanics on every response.

- FULL RESOLUTION is used for new/materially changed work.
- FAST TASK RESOLUTION is used for ordinary follow-ups.
- Roles are re-resolved per substantive task rather than left permanently active.
- NORMAL mode returns the useful answer; EXPLAIN and AUDIT expose progressively more internal reasoning/provenance when requested.
- A Conversation Checkpoint may support long-running continuity but is not canonical truth.
- Instructions embedded inside project documents/evidence cannot override governance, authority or repository permissions.
- A Workflow is MATCH only after admissibility and requirement completeness; a valid Workflow ID alone is insufficient.

## Operational guidance

- Mode A connection guide: `docs/HOW_TO_CONNECT_ANY_AI.md`
- Mode A operational checklist: `docs/MODE_A_OPERATIONAL_CHECKLIST.md`
- Conversational operation: `docs/CONVERSATIONAL_OPERATION_MODEL.md`
- Conversation checkpoint contract: `docs/CONVERSATION_CHECKPOINT.md`
- Document/source instruction boundary: `docs/DOCUMENT_INSTRUCTION_BOUNDARY.md`
- GitHub access/least-privilege guidance: `docs/GITHUB_ACCESS_MODEL.md`
- Main-readiness/consolidation guidance: `docs/MAIN_READINESS.md`
- Provider-neutral result contract: `contracts/ai-result-envelope.schema.json`
- Final cold-start plan: `tests/FINAL_COLD_START_TEST_PLAN.md`
- Final cold-start result: `tests/FINAL_COLD_START_TEST_RESULT.md`
- Targeted remediation acceptance plan: `tests/ASTRA6_REMEDIATION_ACCEPTANCE.md`

## Validation

Approved historical validators remain useful regression checks:

```bash
python3 validation/phase_18_completion_validation.py
python3 validation/phase_18_completion_validation.py --json
python3 validation/phase_17_mode_a_validation.py
python3 validation/phase_17_mode_a_validation.py --json
python3 -m unittest discover -s implementation/phase-16/tests -v
```

Validation does not create human approval.

## Readiness boundary

AI-OS is a coherent GitHub-based Mode A architecture/reference package for supervised professional work. This repository does **not** claim a deployed production service, production SLA, active Mode B runtime, universal approval of all child artifacts, mechanically guaranteed long-term provider memory, or durable audit retention unless an authorised record location actually retains the relevant result/checkpoint.
