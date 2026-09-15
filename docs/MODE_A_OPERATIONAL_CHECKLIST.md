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
3. Resolve the relevant governing sources referenced by the manifest.
4. For planning/execution-basis reasoning, inspect the relevant Phase 15/16 sources rather than inventing a local substitute.
5. Use `contracts/ai-result-envelope.schema.json` for governed result reporting.

## Governance checks before acting

Confirm or explicitly mark unresolved:

- scope/context;
- applicable approved Role(s);
- Skill requirements, keeping applicability separate from individual approval and eligibility;
- Workflow path (`MATCH`, `COMPOSE`, or unresolved as applicable);
- review requirements;
- Decision Right requirements;
- evidence/source dependencies;
- ambiguity or missing-access blockers.

A card, mention, applicability assessment or successful validator does not create approval.

## Read-only mode

Read-only mode is the standard mode for:

- research;
- interpretation;
- planning;
- review;
- comparison;
- drafting;
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

If such material should become governed AI-OS state, it must enter through the appropriate repository/governance process and applicable human authority.

## Human authority

External AI may analyse, draft, classify, compare, prepare changes and surface required decisions. It may not:

- exercise a Decision Right by implication;
- create human approval;
- self-approve Roles, Skills, Workflows, Review Profiles or canonical state;
- treat successful completion as approval;
- auto-register repeated COMPOSE plans as Workflows.

## Result reporting

Every governed result should include:

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

Use the result envelope schema rather than provider-specific result semantics.

## Missing access or evidence

If a required file, approval record, source or authority state cannot be read:

- stop the governed inference that depends on it;
- identify exactly what is missing;
- do not guess approval, eligibility, authority or canonical state;
- clearly separate any still-useful non-governed analysis from the blocked governed conclusion.

## End-of-session check

Before treating the work as complete, confirm:

- source ref/SHA reported;
- no hidden provider memory treated as canonical;
- no human authority implied by AI output;
- no unintended repository writes;
- any write session remained branch-scoped;
- all required reviews/decisions are surfaced rather than silently assumed.