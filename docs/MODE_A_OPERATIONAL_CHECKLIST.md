# Mode A Operational Checklist

Use this checklist whenever a human or external AI works with AI-OS in approved Mode A.

## Before access

- Prefer **read-only** repository access by default.
- Give write access only when the human explicitly asks for repository changes.
- Use least privilege. Repository visibility or connection convenience does not justify broader permissions.
- For governed work, identify the repository, branch/ref and preferably an exact commit SHA before analysis begins.

## Discovery

1. Read `AI_OS_ENTRYPOINT.md` first.
2. Read `ai-os.yaml` second.
3. In interactive chat, read `docs/CONVERSATIONAL_OPERATION_MODEL.md`.
4. Resolve the relevant governing sources referenced by the manifest.
5. For planning/execution-basis reasoning, inspect the relevant Phase 15/16 sources rather than inventing a local substitute.
6. Keep governed result structure compatible with `contracts/ai-result-envelope.schema.json`; do not display raw JSON by default in normal conversation.

## Task-resolution depth

Use **FULL RESOLUTION** for:

- a new project/scope;
- a fresh intake/baseline;
- a material change of objective;
- a materially changed evidence set;
- stale/ambiguous working state;
- relevant governance change.

Use **FAST TASK RESOLUTION** for ordinary follow-up questions where the context is sufficiently clear.

For every substantive task, re-resolve the minimum sufficient Role set. Prior Role use does not keep a Role permanently active.

If the conversation detours and later clearly returns to a prior project/workstream, resume the non-canonical working context rather than forcing the human to repeat it. Ask a short clarification only when the referent is materially ambiguous.

## Governance checks before acting

Confirm internally or explicitly mark unresolved as needed:

- scope/context;
- applicable approved Role(s);
- Skill requirements, keeping applicability separate from individual approval and eligibility;
- Workflow path (`MATCH`, `COMPOSE`, or unresolved as applicable);
- review requirements;
- Decision Right requirements;
- evidence/source dependencies;
- ambiguity or missing-access blockers.

A card, mention, applicability assessment or successful validator does not create approval.

## Workflow matching check

Before reporting `MATCH`, confirm the Workflow is admissible under `planning/workflow-matching-and-composition.md`.

- Semantic fit alone is not MATCH.
- A failed trigger, precondition, Role entitlement, Review Profile, Decision Right, scope, criticality or other governing admissibility requirement keeps the candidate non-MATCH.
- Do not use `MATCH + execution_eligible=false` as a substitute for failed admissibility.
- A matched Workflow is used as written.
- If the objective expands and needs extra Roles/stages/reviews/gates, re-resolve the task; select another approved Workflow or use governed COMPOSE where eligible.

## Conversational Role routing

- Default to Automatic Expert Mode: infer the minimum sufficient Role(s) from the request.
- Support Direct Expert Mode when the human names an AI-OS Role explicitly.
- Do not force a Project scope on a narrow ad-hoc analytical, financial, tax, legal or other professional task when none is needed.
- Preserve Role boundaries even when one real person or organisation performs several compatible Role assignments.

## Read-only mode

Read-only mode is the standard mode for:

- research;
- interpretation;
- planning;
- review;
- comparison;
- drafting;
- calculation;
- external cold-start validation.

The AI may propose changes but should not modify repository state.

## Write-capable mode

Use write-capable access only when the human explicitly authorises edits.

When write access is allowed:

- use a dedicated branch where practical;
- pin the starting ref/SHA;
- stay within the requested file/task scope;
- do not self-approve the resulting changes;
- do not promote `PROPOSED` artifacts merely because they were edited;
- do not merge to `main` or create a PR unless explicitly requested;
- report the resulting commit SHA and files changed.

## Canonical-state boundary

Provider memory, chat history, workspace memory, local scratch state, generated summaries and uncommitted model output are **not canonical AI-OS state**.

They may support conversational continuity only. If such material should become governed AI-OS state, it must enter through the appropriate repository/governance process and applicable human authority.

## Human authority

External AI may analyse, draft, classify, compare, calculate, recommend next actions, prepare changes and surface required decisions. It may not:

- exercise a Decision Right by implication;
- create human approval;
- say it `allows`, `approves` or `authorises` progression without valid human authority evidence;
- self-approve Roles, Skills, Workflows, Review Profiles or canonical state;
- treat successful completion as approval;
- auto-register repeated COMPOSE plans as Workflows.

## User-facing output

Default to **NORMAL MODE**:

- answer the user's question directly;
- give only material explanation/recommendation;
- recommend one best next step;
- ask at most one targeted clarification question when useful.

Do not normally expose:

- repository-reading narration;
- exact SHA/ref;
- internal Role IDs;
- Skill eligibility mechanics;
- Workflow diagnostics;
- Review/Decision Right mechanics;
- raw result-envelope JSON;
- registry/debug comments.

Use **EXPLAIN MODE** when the human asks why, which specialists were used, or how AI-OS reached the answer.

Use **AUDIT MODE** when the human explicitly requests technical provenance, exact SHA/ref, validation/governance diagnostics or the structured result envelope.

Material limitations that affect what can safely be claimed must still be stated in plain language.

## Next-step check

Every substantive answer should normally end with one primary next-step type:

`DO NEXT` · `REQUEST EVIDENCE` · `ASK USER` · `ACTIVATE ROLE` · `HUMAN DECISION` · `WAIT / BLOCKED`

Prefer one best next action over a long menu of equal options.

## Result reporting

Every governed result should still be able to resolve:

- repository identity;
- source branch/ref;
- exact commit SHA used, or explicit unpinned status;
- scope;
- Role/Skill/Workflow/review/Decision Right context;
- evidence used;
- assumptions and unresolved ambiguities;
- proposed changes/output artifacts;
- authority status;
- overall outcome/status.

Use the result-envelope schema for structured governance state. In NORMAL MODE, keep this structure internal unless the human asks to see it or a material limitation needs explanation.

## Missing access or evidence

If a required file, approval record, source or authority state cannot be read:

- stop the governed inference that depends on it;
- identify what is materially missing;
- do not guess approval, eligibility, authority or canonical state;
- clearly separate any still-useful non-governed analysis from the blocked governed conclusion.

## End-of-session check

Before treating governed work as complete, confirm:

- source ref/SHA retained where required;
- no hidden provider memory treated as canonical;
- no human authority implied by AI output;
- Workflow MATCH was not claimed across a failed admissibility gate;
- matched Workflows were not silently modified;
- no unintended repository writes;
- any write session remained branch-scoped;
- all required reviews/decisions are surfaced rather than silently assumed;
- the user-facing answer remained proportionate and did not expose unnecessary internal diagnostics;
- a useful next step was provided where appropriate.
