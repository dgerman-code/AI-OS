# Phase 17 — Final Human Approval

Status: `APPROVED — HUMAN DECISION`

Approval Date: `2026-09-15`

Approved Phase: `Phase 17 — GitHub Mode A / Provider-Neutral AI Connection`

Human-approved implementation baseline: `47c1c5299db900373cf1adb0efba3bc6820eb226`

Implementation branch: `implementation/phase-17-github-mode-a`

## Human decision

The human approver explicitly approved Phase 17 on 2026-09-15 with the instruction:

`APPROVE PHASE 17 MODE A`

This is an explicit human governance decision accepting the Phase 17 Mode A provider-neutral GitHub connection layer on the exact independently reviewed baseline named above.

## Approved scope

This approval accepts Mode A only:

`Human -> external AI -> GitHub AI-OS`

The approved Mode A basis establishes that an external AI with repository access can discover and use AI-OS from GitHub without provider-specific governance redesign.

The approved Phase 17 interface includes:

- root discovery entrypoint `AI_OS_ENTRYPOINT.md`;
- machine-readable repository manifest `ai-os.yaml`;
- universal connection guide `docs/HOW_TO_CONNECT_ANY_AI.md`;
- provider-neutral governed result contract `contracts/ai-result-envelope.schema.json`;
- thin Mode A adapters for generic AI, OpenAI ChatGPT, Anthropic Claude, OpenAI Codex and Google Gemini;
- example cold-start session `examples/mode-a-generic-session.md`;
- fail-closed static conformance validator `validation/phase_17_mode_a_validation.py`.

The approved design preserves the governing boundary that GitHub repository content at the reported ref/commit is the Mode A source of truth. Provider memory, chat history, project state, hidden summaries, scratch state or generated output do not silently become canonical AI-OS state.

Provider adapters are syntax/capability guidance only. They do not create provider-specific Role, Workflow, Skill, Review Profile, Decision Right, canonical-memory or governance semantics. Repository governance overrides adapter wording.

## Authority and governance boundary

This approval preserves all previously approved AI-OS authority boundaries.

In particular:

- an external AI may analyse, draft, propose, classify, review, prepare work products and, where explicitly authorised, make repository changes within the granted branch/scope;
- repository write permission does not grant governance authority;
- AI completion does not create approval;
- external AI may not self-approve or self-promote Roles, Skills, Workflows, Review Profiles, Decision Rights, canonical memory/evidence, governance records or phase approvals;
- Skill applicability, Skill card existence, individual Skill approval and execution eligibility remain distinct states;
- missing approval, evidence, scope, authority or required repository source fails closed;
- governed results must report repository identity, ref/branch and exact commit SHA used, or explicitly disclose that the result is unpinned;
- the standard result envelope records `authority_status` separately from task/result completion status.

No new Decision Right is created by Phase 17.

## Mode B remains deferred

This approval does not approve or implement Mode B.

Phase 17 does not introduce active:

- provider/model API invocation by AI-OS;
- automatic model routing;
- API-key or secret management;
- billing controls;
- retry/fallback orchestration;
- workers, queues or schedulers;
- deployment runtime or production execution infrastructure.

References to Mode B in Phase 17 are solely as prohibited or deferred scope.

A future Mode B phase may build on the approved provider-neutral repository interface, but it requires its own governed design, review and human approval.

## Independent review history

The independent review process is preserved faithfully.

### Initial independent review

The original independently audited implementation baseline was:

`831436a73874816ac907faf87065bfe7309169ab`

The review found the Mode A artifacts themselves coherent and passed:

- cold-start discovery;
- manifest/canonical-source design;
- result-envelope representation;
- provider-adapter content and neutrality;
- Skill/authority safety;
- actual Mode B containment;
- upstream Phase 1–16 containment.

However, the review returned `FAIL` because the Phase 17 static conformance validator produced material false greens. The blocker was limited to the assurance layer, not the Mode A architecture/content.

### First targeted validator remediation

Targeted validator remediation commit:

`2c7e2e113b0bbecc0b1d7b47b74ec91c940ee0e3`

A short closure review still returned `FAIL` because the validator:

- falsely rejected existing Markdown-formatted safe negation;
- allowed provider-memory canonicalisation to escape;
- regressed provider-specific governance-fork detection;
- permitted an unrelated negative clause to suppress a later unsafe automatic-approval statement.

### Second targeted validator remediation

Targeted validator remediation commit:

`1e8be2f810fb988d80f6ffd34e091deb34b25884`

A further short closure review still returned `FAIL`. It found:

- pristine validation failing on legitimate safe manifest wording;
- safe `Provider memory is not canonical` being falsely rejected;
- safe Skill-card/approval distinction wording being falsely rejected;
- newline-separated safe and unsafe statements still allowing the unsafe claim to escape.

Again, these findings remained confined to validator assurance logic.

### Final targeted validator remediation

Final independently reviewed remediation baseline:

`47c1c5299db900373cf1adb0efba3bc6820eb226`

The final closure review returned:

- final verdict: `PASS`;
- pristine text validator: `93/93 PASS`, exit `0`;
- pristine JSON validator: `93/93 PASS`, exit `0`, no failed checks;
- `git diff --check`: `PASS`;
- remediation diff whitespace check: `PASS`;
- final worktree: clean;
- remaining blockers: `NONE`;
- readiness: `READY FOR HUMAN APPROVAL OF PHASE 17 MODE A`.

The review independently reproduced all requested safe and unsafe semantic controls.

## Final assurance record

At the approved baseline `47c1c5299db900373cf1adb0efba3bc6820eb226`:

- validator default mode: `93/93 PASS`;
- validator JSON mode: `93/93 PASS`;
- safe controls: all six accepted;
- unsafe controls: all eleven detected as failures;
- invalid JSON Schema type: detected;
- removal of source-reporting requirement: detected;
- removal of `authority_status`: detected;
- provider output auto-approval assertions: detected, including semicolon and newline variants;
- carded-Skill approval / automatic eligibility assertions: detected;
- provider-memory canonicalisation: detected;
- provider-specific authoritative Role semantics: detected;
- active Mode B/provider model API call semantics: detected;
- Markdown-formatted negative safety wording: accepted;
- provider-memory non-canonical wording: accepted;
- Skill-card / approval distinction wording: accepted.

The final independent closure therefore closed the only remaining Phase 17 blocker.

## Upstream containment

Phase 17 is additive to the Phase 16 approval commit:

`3a8cc7b98720c2666791fa7f83c12239f701b7c5`

The independent review confirmed that Phase 17 added Mode A interface/conformance artifacts and did not semantically modify approved Phase 1–16 artifacts.

The approved Phase 17 implementation baseline is exactly:

`47c1c5299db900373cf1adb0efba3bc6820eb226`

## Explicit non-scope

This approval does not:

- certify production/deployment/runtime-service readiness;
- implement Mode B;
- grant an external AI unrestricted repository write access;
- grant any provider governance authority;
- create or exercise a Decision Right;
- individually approve any unapproved Skill card;
- make provider memory canonical;
- allow provider-specific governance semantics;
- bypass Phase 15/16 planning, execution-basis, review or authority controls;
- authorise silent promotion of PROPOSED artifacts;
- authorise a pull request.

## Approval boundary

The governing human-approved Phase 17 Mode A implementation baseline is:

`47c1c5299db900373cf1adb0efba3bc6820eb226`

This approval establishes the provider-neutral GitHub-connected AI-OS Mode A interface as an approved system layer.

Any later semantic change to this approved Mode A baseline, or any future implementation of Mode B, requires governed change control, appropriate independent review and applicable human authority.
