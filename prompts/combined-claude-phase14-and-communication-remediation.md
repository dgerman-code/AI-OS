# Combined Claude Remediation Prompt — Phase 14 + Communication Specialist

You are working in repository `dgerman-code/AI-OS`.

This is ONE coordinator prompt containing TWO strictly separated workstreams. Execute them sequentially. Do not mix branches, files, assumptions, governance states, or commits between the workstreams.

## GLOBAL RULES

- No PRs.
- Do not modify approved Phase 1–13 artifacts.
- Do not manufacture human approval, Decision Rights, review satisfaction, authority, canonical status, or production readiness.
- Keep every new or remediated Phase 14 / communication-specialist artifact `PROPOSED` unless an already-approved upstream artifact explicitly says otherwise.
- Preserve inherited Phase 10 and Phase 11 validator findings exactly; do not repair or reinterpret them as current regressions.
- Do not add runtime, DDL, migrations, SDKs, workers, queues, schedulers, secrets, IaC, deployment logic, or provider integrations unless the current branch already explicitly contains such implementation scope. These workstreams are specification / proposal remediation only.
- If a required governance decision is genuinely human-only, do not decide it silently. Produce a clear decision memo and stop at the proper governance boundary.
- After each workstream, commit and push only that branch. Report exact full SHA, changed-file list, validation totals, containment status, remaining blockers, and readiness verdict.

---

# WORKSTREAM 1 — PHASE 14 IMPLEMENTATION SPECIFICATION REMEDIATION

## Branch

`spec/phase-14-implementation-specification`

## Exact audited baseline to remediate

`28d663203876c41cc264108b33c7ce91c61ab4ce`

The independent V6 audit verdict was `FAIL` with HIGH review credibility.

Do not audit or remediate a later prompt-only commit as if it were the implementation-spec baseline.

## Objective

Close ALL six V6 blockers without weakening approved Phase 1–13 semantics and without inventing guarantees that are not implementable.

## Required remediation

### P14-1. Crossed-boundary redispatch must have a complete state-machine path or be removed

Current defect:
- PO-14 / PO-19 permit redispatch after `boundary_crossed=true` under safe conditions such as recorded provider deduplication or `CONFIRMED_NOT_APPLIED`.
- T1–T10 contain no complete fenced ownership/transition path that actually reacquires such an item for redispatch.

Choose exactly one coherent architecture and apply it everywhere:

**Option A — implement conditional redispatch fully**
- define the exact eligible source state;
- define exact target state;
- define ownership acquisition;
- require current `claim_generation` fencing;
- require current `claim_token` where the row is owned;
- define idempotency-key reuse;
- define provider-dedup evidence requirement;
- define whether reconciliation closes before redispatch;
- define exact operational state transition and governed Provider Attempt consequence;
- define crash behavior before, during and after the redispatch boundary;
- define whether a new ProviderAttemptRef is created or the existing attempt is reused, and reconcile that with identity rules;
- add exact assurance cases and mutation probes.

**Option B — remove crossed-boundary redispatch entirely**
- once `boundary_crossed=true`, require reconciliation only;
- remove every contradictory permission in PO-14, PO-19 and secondary prose;
- preserve same-idempotency semantics only for genuinely pre-boundary dispatch;
- ensure no later document implies safe automatic redispatch after the boundary.

Prefer the simpler architecture if it satisfies the approved Phase 11 semantics without loss.

### P14-2. Reconcile F-9a / F-9d / PO-8 with T6 and the chosen PO-14/PO-19 model

The final specification must distinguish at least:
- expired claim before boundary crossing;
- expired claim after boundary crossing;
- unknown external effect;
- confirmed-not-applied effect;
- settled effect.

An expired lease/claim must never by itself prove provider non-occurrence.

### P14-3. Correct T10 exact predicates and fencing

T10 currently permits `PENDING` or `CLAIMED` → `SETTLED` without sufficiently exact state/ownership predicates.

Specify:
- exact source-state predicate;
- exact terminal reason;
- whether ownership is required;
- for `CLAIMED`, current `lease_owner`, `claim_generation`, and `claim_token` predicates;
- stale claimant result = zero writes;
- no unauthorised owner can retire another claimant's row;
- exact operational write set and governed consequences.

### P14-4. Fix O5 claim-generation semantics

Current `CHECK (claim_generation >= 0)` is only a row-shape constraint and cannot enforce monotonic increase across updates.

Do not claim otherwise.

Either:
- reclassify O5 explicitly as a row-level nonnegative-domain constraint while placing monotonicity exclusively in atomic CAS/transition predicates; or
- specify another actually implementable database mechanism that enforces monotonicity.

Do not introduce a fake SQL guarantee.

### P14-5. Remove active O1–O4 vs O1–O5 drift

Every active normative and explanatory location must agree on the current outbox constraint inventory.

Historical text may mention prior states only if it is unmistakably historical and cannot be read as current normative content.

### P14-6. Harden assurance against all V6 escapes

The V6 reviewer independently tested 14 nearby mutations and 9 escaped.

Add substantive validation and mutation coverage for all of them, especially:
- B3 missing run-state append in a second active location;
- B4n missing inherited consequence in a second active location;
- B1r consuming an ordinal in a second active location;
- stale/concurrent writer or stale-generation semantics weakened outside the canonical transition table;
- regenerated provider idempotency key in a second active location;
- outbox reclassified as governed outside the canonical owner location;
- refusal observational equality incorrectly includes total execution-event count;
- stale command/transaction count in non-canonical active prose;
- unknown-effect automatic redispatch without the required safe precondition.

Also:
- fix the normative-rule parser so blockquoted definitions such as `P-14a` are included;
- derive the normative-definition count instead of freezing it;
- reject duplicate rule IDs across all active specification documents;
- reject unresolved active `Rule <id>` references;
- keep historical exclusions sentence-scoped and explicit;
- do not give mutation credit merely because containment/git-dependent checks fail.

## Phase 14 validation requirements

Run and report:
- Phase 14 validator default / verbose / JSON;
- Phase 14 mutation harness;
- Phase 12 unit suite;
- Phase 12 validator;
- Phase 11 validator;
- Phase 10 validator;
- Phase 9 validator;
- Phase 8 validator;
- governed example;
- blocked example;
- `git diff --check`;
- protected Phase 1–13 containment verification.

The self-check must state harness credibility conservatively. A green validator does not prove architectural correctness.

## Phase 14 output / commit

Commit all Phase 14 remediation changes on this branch with a clear message such as:

`docs: close Phase 14 redispatch fencing and assurance blockers`

Push the branch.

Return sections:
A. remediation summary
B. exact baseline and new commit SHA
C. crossed-boundary model chosen
D. recovery consistency
E. T10 fencing
F. O5 semantics
G. constraint inventory consistency
H. assurance hardening
I. validator/mutation results
J. regression results
K. containment
L. known limitations
M. harness credibility
N. remaining blockers
O. readiness verdict

The correct positive readiness wording, and only if true, is:

`READY FOR INDEPENDENT PHASE 14 IMPLEMENTATION SPECIFICATION RE-AUDIT V7`

Do NOT human-approve Phase 14.

---

# WORKSTREAM 2 — COMMUNICATION SPECIALIST PACKAGE REMEDIATION + GOVERNANCE DECISION PREPARATION

After Workstream 1 is committed and pushed, switch cleanly to:

## Branch

`proposal/communication-difficult-conversations-specialist`

## Package baseline under review

`81623de03034529d2a1a52d0062703338e8ad658`

The independent package review verdict was `FAIL` with remaining blockers.

Do not modify the Phase 14 branch while doing this workstream.

## Objective

Remediate all package defects that are specification errors, and prepare explicit human governance decisions for items that must not be silently decided by Claude.

Preserve the architecture:
- canonical capability is not a celebrity-named autonomous agent;
- canonical proposed capability remains `Difficult Conversations & Communication Strategy Specialist` unless human governance later changes the classification;
- `jefferson-fisher-communication` is compatibility/research alias only;
- `Fisher Mode` is compatibility alias only; canonical mode is `Calm Direct Mode`;
- `FISHER COMMUNICATION FILTER` is compatibility alias only; canonical construct is `Communication Control Filter`;
- no impersonation, endorsement, licensing, training, approval or affiliation claim;
- no proprietary copying;
- ROLE != AGENT INSTANCE;
- communication strategy cannot override substantive legal/financial/compliance/technical conclusions;
- scores do not create authority, approval, review satisfaction or model choice.

## Required remediation

### COM-1. Phase 8 epistemic vocabulary

Replace active deprecated `FACT` usage with `FACT_CLAIM` everywhere new architecture is being defined.

Remove every active `SOURCE → FACT` or equivalent epistemic-type mutation.

Required semantics:
- source remains `SOURCE`;
- a supported factual assertion is a separate linked `FACT_CLAIM`;
- evidence/provenance links support the claim;
- no epistemic type mutation shortcut.

Update Role Card, Skill Pack, diagnostics, examples, evaluation cases and self-check consistently.

### COM-2. Reconcile Communication Strategy Review triggers

Independent review found a contradiction:
- Review Profile requires review whenever a draft carries another Role's substantive conclusion or states a boundary with a consequence;
- Role Card/workflows required review mainly at high/critical stakes.

Make one authoritative rule and apply it everywhere.

Recommended fail-closed interpretation:
`review.communication_strategy@0.1` is mandatory when ANY of the following is true:
1. high/critical stakes;
2. draft carries or reformulates another Role's substantive conclusion;
3. draft states a consequential boundary, refusal, escalation, commitment, deadline, admission-sensitive statement, or institutional position;
4. a workflow-specific rule explicitly requires it.

Low/medium stakes alone must not bypass review when one of these conditions exists.

If a less strict design is chosen, explain why it does not weaken independence or substantive-owner protection.

### COM-3. Add explicit NOT_APPLICABLE gate semantics for read-only diagnostics

`workflow-thread-diagnostics` is intentionally read-only and may produce no transmissible artifact.

Do not force `AUTHORITY_ABSENT` when no external act is contemplated.

Add an explicit representation such as:
- `human_gate_status: NOT_APPLICABLE`
- `human_gate_reference: null`
- reason: `NO_EXTERNAL_ACT_CONTEMPLATED`

Reserve `AUTHORITY_ABSENT` for an act that actually requires authority but lacks an applicable Right.

Update diagnostics contract, workflows, examples, evaluation spec and self-check.

### COM-4. Separate diagnostic-risk schema from Communication Control Filter schema

The ten-factor filter is normative and contains:
GOAL, EMOTION, CLARITY, BREVITY, BOUNDARY, DEFENSIVENESS, CONTROL, RELEVANCE, ESCALATION, NEXT STEP.

Do not represent a different nine-field mixed object as if it were the same filter.

Create two explicit structures if needed:
1. `communication_control_filter` — exact ten component scores / N/A + reasons and documented derived figures;
2. `diagnostic_risks` — relationship risk, documentation risk, legal sensitivity, reputational exposure, timing/channel risk, etc.

No overall score may become approval or authority.

### COM-5. Reassess TA-7 against approved `decision.external_publication`

The prior package likely misread the approved subject.

Approved subject covers release of a content item to an audience outside the entity under the entity's name. A private letter/email to a partner may therefore already be within scope.

Do NOT create or preserve `decision.external_high_stakes_communication_send` merely because correspondence is private.

Perform exact subject/applicability analysis against the approved Phase 7 card and classify TA-1…TA-7.

Outcomes allowed:
- existing approved Right clearly applies;
- existing Right clearly does not apply;
- boundary genuinely ambiguous → HUMAN GOVERNANCE DECISION REQUIRED.

If the existing Right covers TA-7, remove the proposed duplicate Right from the package and repair all dependent text, E23, PC-2, Role Card gate wording and self-check.

If a genuinely non-overlapping act remains, describe the narrow gap without silently creating a new Right.

### COM-6. Resolve specification errors dependent on TA-7

Correct all examples, positive controls, hard fails, role-card language, workflow gates and self-check claims that currently assume the old TA-7 interpretation.

### COM-7. Prepare human governance decision on OG-1 — identifier shape

Do not silently decide this unless the repository already contains a binding rule that makes the answer mechanical.

Prepare a decision memo comparing:
- dotted candidate IDs currently used by the proposal;
- existing Phase 4/5 registry conventions (`snake_case` forms).

Recommendation should strongly prefer one canonical convention and avoid dual canonical identities.

If existing approved registry standards make normalisation mandatory, state that with evidence and apply the mechanical normalisation. Otherwise mark:
`HUMAN GOVERNANCE DECISION REQUIRED — OG-1`.

### COM-8. Prepare human governance decision on OG-2 — Role vs Specialisation

Do not silently create a 60th approved Role.

Analyse whether this capability should be:
- a new Professional Delivery Role;
- a Specialisation attached to an existing Role;
- or a methodology/pack usable by more than one Role.

Use explicit criteria:
- independent domain ownership;
- stable output responsibility;
- unique competency boundary;
- need for independent review eligibility;
- overlap with Institutional Communications / Marketing / Business Development / Stakeholder roles;
- whether the capability can be reused across domains without giving it substantive authority.

Produce a recommendation, but if no approved rule mechanically determines the answer, finish with:
`HUMAN GOVERNANCE DECISION REQUIRED — OG-2`.

Do not approve the new Role or Specialisation yourself.

## Communication package assurance hardening

Add package-specific validation or at minimum executable self-check tooling sufficient to catch the independent review's missed defects:
- deprecated `FACT` in active package architecture;
- epistemic mutation `SOURCE → FACT/FACT_CLAIM`;
- review-trigger divergence across Role Card/Profile/workflows;
- gate-free diagnostic incorrectly marked `AUTHORITY_ABSENT`;
- filter/diagnostic schema divergence;
- candidate Skill treated as approved;
- alias becoming canonical identity;
- score becoming Model Profile selection or authority;
- Role rewriting another domain's substantive conclusion;
- TA-7/right overlap assumption presented as settled when unresolved.

Keep all package artifacts `PROPOSED`.

## Communication package validation / regression

Run:
- package self-check / validator if created;
- all relevant existing Phase 8–11 validators available on the branch;
- reference-resolution checks for cited Role/Skill/Review/Decision identifiers;
- `git diff --check`;
- containment verification showing approved Phase 1–13 and Phase 14 artifacts untouched.

## Communication package commit/output

Commit and push only `proposal/communication-difficult-conversations-specialist`.
No PR.

Return sections:
A. remediation summary
B. exact baseline and new commit SHA
C. Phase 8 knowledge corrections
D. review-trigger reconciliation
E. diagnostic no-gate semantics
F. filter vs diagnostic schema
G. TA-1…TA-7 Decision Right analysis
H. dependent text/evaluation corrections
I. OG-1 decision memo
J. OG-2 decision memo
K. validation/self-check results
L. containment
M. remaining change-control items
N. remaining blockers
O. readiness verdict

Unless OG-1 and OG-2 are mechanically resolved by already-approved registry rules, the strongest correct positive verdict is:

`READY FOR HUMAN GOVERNANCE DECISION ON OG-1 AND OG-2 — NOT YET READY FOR PACKAGE APPROVAL`

Do NOT human-approve the package.
Do NOT create or approve a new Decision Right.
Do NOT create a PR.

---

# FINAL COORDINATOR REPORT

After both workstreams are complete, return a compact final summary with:
- Phase 14 new remediation SHA and readiness;
- Communication package new remediation SHA and readiness;
- confirmation that the two branches remained isolated;
- confirmation that no PR was created;
- confirmation that no human approval was manufactured;
- exact next human decisions/actions required.