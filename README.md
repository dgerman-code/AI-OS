# AI-OS

Provider-independent AI Operating System for managing organisations, programmes, projects, ventures, digital products and operational work through reusable professional Roles, Skills, Workflows, evidence, review and explicit human governance.

## Start here

For the current system state and approval boundary, read:

1. `SYSTEM_STATUS.md`
2. `AI_OS_ENTRYPOINT.md`
3. `ai-os.yaml`

If you are connecting an external AI through GitHub, use the approved **Mode A** path and follow `docs/HOW_TO_CONNECT_ANY_AI.md` plus `docs/MODE_A_OPERATIONAL_CHECKLIST.md`.

## Current operating model

**Mode A — approved current connection mode**

`Human -> external AI -> GitHub AI-OS`

The external AI reads AI-OS from GitHub at a reported ref/commit and works under repository governance. Provider memory, chat history and generated output are not canonical AI-OS state by themselves.

**Mode B — deferred**

AI-OS calling/routing model-provider APIs is intentionally deferred. Provider API orchestration, billing, key management, retry/fallback workers, queues and deployment runtime are not part of the current approved operating mode.

## Core principles

- ROLE != MODEL.
- ROLE != AGENT INSTANCE.
- Roles, Skills, Workflows and canonical knowledge live outside any individual AI provider.
- Models are replaceable runtimes that temporarily assume Roles.
- Context is isolated by organisation / programme / project / product / workstream / task.
- AI output does not automatically become canonical truth or governance approval.
- Critical authors do not self-approve their own work.
- Delivery, independent assurance and human authority are separate layers.
- New Roles are created only when a distinct methodology, authority boundary, review requirement or recurring professional artifact justifies them.

## Governance and status

Historical phase approval records live under `reviews/`. Phase-level approval does not automatically approve or canonicalise every child artifact. Existence, applicability, validation success and execution eligibility must not be confused with governance approval.

See `SYSTEM_STATUS.md` for the Phase 1–18 approval chain, inherited assurance notes and current limitations.

## Operational guidance

- Mode A connection guide: `docs/HOW_TO_CONNECT_ANY_AI.md`
- Mode A operational checklist: `docs/MODE_A_OPERATIONAL_CHECKLIST.md`
- GitHub access/least-privilege guidance: `docs/GITHUB_ACCESS_MODEL.md`
- Main-readiness/consolidation guidance: `docs/MAIN_READINESS.md`
- Provider-neutral result contract: `contracts/ai-result-envelope.schema.json`
- Final post-approval cold-start test plan: `tests/FINAL_COLD_START_TEST_PLAN.md`

## Validation

Current completion and Astra 6 remediation work should be checked with:

```bash
python3 validation/phase_18_completion_validation.py
python3 validation/phase_18_completion_validation.py --json
python3 validation/phase_17_mode_a_validation.py
python3 validation/phase_17_mode_a_validation.py --json
python3 validation/astra_6_remediation_validation.py
python3 validation/phase_16_validation.py
```

Validation does not create human approval.

## Readiness boundary

AI-OS Phase 18 is human-approved as a coherent GitHub-based Mode A system package, and the first post-approval external-AI cold-start test has been recorded as `PASS WITH NON-BLOCKING NOTES` in `tests/FINAL_COLD_START_TEST_RESULT.md`. This repository does **not** claim a deployed production service, production SLA, active Mode B runtime, universal provider compatibility, or universal approval of all child artifacts.

`tests/FINAL_COLD_START_TEST_PLAN.md` remains the reusable cold-start procedure for later baselines/providers.