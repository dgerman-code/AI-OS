# Phase 17 — Independent Mode A Review

Repository: `dgerman-code/AI-OS`
Branch: `implementation/phase-17-github-mode-a`

AUDIT / REVIEW ONLY. Do not modify files. Do not commit. Do not create a PR.

Audit exact implementation baseline:

`831436a73874816ac907faf87065bfe7309169ab`

Do NOT audit a later prompt-only commit as the implementation baseline.

## Review objective

Determine whether a new external AI with GitHub read access and no hidden conversation context can discover and use AI-OS in provider-neutral Mode A:

`Human -> external AI -> GitHub AI-OS`

Do not review or require Mode B (AI-OS calling provider APIs).

## Required checks

1. **Cold-start discovery**
   - Start from repository root with no hidden AI-OS context.
   - Find `AI_OS_ENTRYPOINT.md` and `ai-os.yaml`.
   - Verify they answer where to start, what must be read, what the AI may do, and how results must be returned.

2. **Canonical-source / provenance**
   - GitHub at the reported ref/commit must remain the Mode A source of truth.
   - Provider memory/chat/session state must not become canonical silently.
   - Governed output must report repository/ref/commit SHA or explicitly state that it is unpinned.

3. **Governance neutrality**
   - No adapter may create provider-specific Role, Workflow, Skill, Review Profile or Decision Right semantics.
   - Repository governance must override adapter wording.
   - External AI must not self-approve or self-promote governed artifacts.

4. **Skill safety**
   - Card existence/applicability must remain distinct from individual Skill approval and execution eligibility.
   - No Mode A artifact may imply that Phase 4 architecture approval individually approved the six Skill cards.

5. **Result envelope**
   - Validate `contracts/ai-result-envelope.schema.json` as JSON Schema syntax as far as the local tooling permits.
   - Confirm request identity, source ref/SHA, scope, roles, Skill applicability/approval/eligibility separation, workflow mode/reference, reviews, Decision Rights, evidence, ambiguities, proposed changes, artifacts, authority status and result status are represented.
   - Completion alone must not imply governance approval.

6. **Adapters**
   Review:
   - `adapters/mode-a/generic.md`
   - `adapters/mode-a/openai-chatgpt.md`
   - `adapters/mode-a/anthropic-claude.md`
   - `adapters/mode-a/openai-codex.md`
   - `adapters/mode-a/google-gemini.md`

   Confirm they are thin, capability-conditional and semantically equivalent.

7. **Mode B containment**
   - No model API calling, provider routing, billing, key management, retry/fallback, queue, worker, scheduler or deployment runtime may be introduced as Mode A behavior.
   - References to Mode B solely as prohibited/deferred scope are allowed.

8. **Static validation**
   Run:

```bash
python3 validation/phase_17_mode_a_validation.py
python3 validation/phase_17_mode_a_validation.py --json
git diff --check
```

9. **Upstream containment**
   - Compare implementation baseline to Phase 16 approval commit `3a8cc7b98720c2666791fa7f83c12239f701b7c5`.
   - Confirm approved Phase 1–16 artifacts were not semantically changed; Phase 17 should add only Mode A interface/conformance artifacts and its prompt.

10. **Fresh adversarial spot checks**
    Try at least these contradictory cases mentally or on temporary copies:
    - adapter says provider output is automatically approved;
    - manifest says carded Skills are approved;
    - entrypoint omits commit/ref reporting;
    - result envelope removes authority status;
    - adapter claims provider memory is canonical;
    - Mode B API orchestration is presented as active Mode A behavior.

    Confirm the design/validator fails closed or that any uncovered case is reported as an assurance limitation.

## Required report

A. FINAL VERDICT
B. EXACT BASELINE / CONTAINMENT
C. COLD-START DISCOVERY
D. MANIFEST / CANONICAL SOURCE
E. RESULT ENVELOPE
F. PROVIDER ADAPTERS
G. SKILL / AUTHORITY SAFETY
H. VALIDATION / ADVERSARIAL CHECKS
I. NON-BLOCKING NOTES
J. REMAINING BLOCKERS
K. READINESS VERDICT

If and only if the Mode A foundation is coherent, discoverable, provider-neutral, fail-closed, contains no Mode B implementation, preserves upstream governance, and has no blocker, end exactly:

`READY FOR HUMAN APPROVAL OF PHASE 17 MODE A`

Otherwise end exactly:

`NOT READY — PHASE 17 MODE A BLOCKER REMAINS`
