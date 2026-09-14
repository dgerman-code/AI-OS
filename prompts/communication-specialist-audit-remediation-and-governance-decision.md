# Communication Specialist Package — Audit Remediation and Governance Decision Preparation

Repository: `dgerman-code/AI-OS`
Branch: `proposal/communication-difficult-conversations-specialist`

## Exact remediation baseline

Remediate the package produced at:

`81623de03034529d2a1a52d0062703338e8ad658`

The later independent-review prompt and this remediation prompt are not part of that package baseline.

## Mode

This is a targeted remediation of the PROPOSED communication-specialist package after independent review.

Do NOT modify approved Phase 1–13 artifacts.
Do NOT modify the Phase 14 branch.
Do NOT create a PR.
Do NOT promote any package artifact to APPROVED or CANONICAL.
Do NOT create, map, widen, exercise, or approve a Decision Right.
Do NOT silently resolve governance items that require a human decision.

All package artifacts must remain `PROPOSED`.

## Independent review findings to remediate

The independent review of baseline `81623de...` returned `FAIL` and identified seven blocking areas.

### 1. Phase 8 epistemic vocabulary and immutability

Replace every active use of deprecated `FACT` with `FACT_CLAIM` where the package defines new architecture or contracts.

Remove every semantic or literal `SOURCE -> FACT` / `SOURCE -> FACT_CLAIM` mutation.

Required semantics:

- SOURCE remains SOURCE.
- A supported factual assertion is a separate linked `FACT_CLAIM` item.
- Evidence/provenance links connect the claim to the source.
- No epistemic type mutation is permitted.
- AI suggestions remain AI_SUGGESTION unless a new linked item is created through the approved Phase 8 adoption semantics.

Sweep the entire 20-artifact package, examples, self-check and evaluation cases for old vocabulary or conversion semantics.

Add package-specific checks that fail if `FACT` is introduced as an active epistemic type or if a SOURCE-to-claim mutation is described.

### 2. Communication Strategy Review trigger consistency

Reconcile `review.communication_strategy@0.1` with:

- `role-card.md`;
- every workflow that can produce transmissible communication;
- trigger/routing rules;
- evaluation cases;
- self-check.

The independent review found that the Review Profile declares mandatory review when either:

- a draft carries another Role's substantive conclusion; or
- a consequential boundary is stated,

while the Role Card/workflows made review mandatory only for high/critical stakes.

Choose one internally coherent rule set consistent with approved review architecture.

Preferred fail-closed contract:

Review is mandatory whenever ANY of the following is true:

1. stakes are HIGH or CRITICAL;
2. another Role's substantive conclusion is carried into the draft;
3. the communication states a consequential boundary, refusal, escalation, commitment, concession, admission-sensitive position, or other material external consequence;
4. a workflow-specific mandatory-review condition applies.

For low/medium purely routine communication with none of those conditions, the review may remain advisory.

Do not lower the Review Profile's independence requirements to make activation easier.

### 3. Gate-free diagnostic representation

`workflow-thread-diagnostics.md` is read-only and may produce no transmissible act.

Do not force `human_gate_reference = AUTHORITY_ABSENT` where no authority is required.

Define an explicit representation such as:

`human_gate_reference: NOT_APPLICABLE`

with exact semantics:

- no external transmission is contemplated by this artifact/workflow output;
- no Decision Right is required for the diagnostic act itself;
- this is not equivalent to authority being present;
- if the diagnostic later feeds a transmission workflow, that later workflow resolves the applicable Decision Right independently.

Update the diagnostic schema, workflows, examples, evaluation suite and self-check consistently.

### 4. Diagnostic score contract vs Communication Control Filter

The ten-factor Communication Control Filter is normative for its own component scores.

Do not mix its component fields with separate diagnostic risk fields.

Refactor the diagnostic contract so it has separate namespaces, for example:

- `communication_control_filter.components`: the exact ten factors GOAL, EMOTION, CLARITY, BREVITY, BOUNDARY, DEFENSIVENESS, CONTROL, RELEVANCE, ESCALATION, NEXT_STEP, each using the filter's N/A semantics;
- `communication_control_filter.derived`: only the derived figures defined by the filter;
- `diagnostic_risks`: relationship risk, documentation risk, legal-sensitive risk, escalation context, etc.

The diagnostic contract must not invent a competing scoring rubric.

Add cross-document assurance that verifies exact field-set consistency between the filter and diagnostic schema.

### 5. TA-7 / `decision.external_publication` boundary

The independent review found a material misreading: the approved `decision.external_publication` subject is release of content to an audience outside the entity under the entity's name and is not limited by the word "public" or general availability.

Therefore DO NOT continue to assert that all private high-stakes correspondence is outside that Right merely because it is private.

Perform a source-faithful reassessment of TA-7 against the exact approved Phase 7 card.

Required safe outcome for this remediation:

- remove any categorical statement that TA-7 is uncovered solely because it is private;
- remove any claim that `decision.external_high_stakes_communication_send` is needed on that basis;
- mark the candidate Right as `WITHDRAWN_FROM_CURRENT_PACKAGE` or equivalent PROPOSED-package status that confers no authority, unless a genuinely distinct, non-overlapping act can be demonstrated from approved Phase 7 semantics;
- update Role Card gate wording, E23, PC-2, examples and self-check so they resolve an applicable existing Right first and fail closed only when no applicable approved Right can actually be found.

Do NOT amend the approved Phase 7 Right in this branch.
Do NOT reinterpret or widen it beyond its approved wording.

Create a short `governance-decision-note.md` explaining whether any residual gap remains after the reassessment and, if so, what exact external act is not covered. Do not invent a new Right to fill it.

### 6. Evaluation-suite coverage

Add adversarial tests / hard-fail checks for all six previously missed issues:

1. deprecated `FACT` used in new package architecture;
2. SOURCE epistemic type mutated into a claim type;
3. read-only diagnostics forced to report AUTHORITY_ABSENT instead of NOT_APPLICABLE;
4. diagnostic score schema diverges from the ten-factor filter;
5. low/medium consequential or domain-bearing communication skips a Profile-mandated review;
6. proposed TA-7 logic duplicates or overlaps an existing approved Decision Right.

The suite must fail for each weakening independently.

Also ensure E23 and PC-2 no longer encode the disputed TA-7 premise.

### 7. Governance blockers OG-1 and OG-2

These require human governance decisions and must NOT be silently decided by this remediation.

Prepare a concise decision memo in `governance-decision-note.md` with two explicit choices:

#### OG-1 — identifier shape

Present:

A. keep dotted candidate IDs; or
B. normalise candidate IDs to the approved Phase 4/5 registry shape.

Give the architectural consequences of each and identify the recommended option, but leave the status `HUMAN DECISION REQUIRED`.

Recommendation should favor conformance with the approved registry shape unless a concrete compatibility reason justifies divergence.

#### OG-2 — Role vs Specialisation

Present:

A. register a new 60th Professional Delivery Role; or
B. model the capability as a Specialisation attached to one or more existing Roles.

Give consequences for ownership, routing, review eligibility, skill mappings and governance surface.

Do not decide on behalf of the human authority.

Recommendation may be stated, but status remains `HUMAN DECISION REQUIRED`.

Until OG-1 and OG-2 are decided, package readiness must NOT say ready for human approval. It may say ready for governance decision on OG-1/OG-2 if all technical blockers are closed.

## Package-specific validation

Add or extend a lightweight deterministic package validator under the proposal directory or permitted proposal-local validation area. It must not modify approved validators.

At minimum it must verify:

- exactly the expected package artifact set plus explicitly added remediation artifacts;
- all package artifacts remain PROPOSED;
- no approved Phase 1–13 artifact changed;
- no Phase 14 file changed;
- no active deprecated `FACT` vocabulary in package contracts;
- no SOURCE-to-claim epistemic mutation language;
- exact Review Profile trigger consistency across Role Card and workflows;
- thread diagnostics permit NOT_APPLICABLE and do not require AUTHORITY_ABSENT where no transmission exists;
- exact ten filter factors match the diagnostic contract;
- no score/filter grants authority, review satisfaction or model selection;
- TA-7 analysis does not assume private == outside `decision.external_publication`;
- no candidate Decision Right is treated as available;
- candidate Skills remain non-activatable until registered/mapped;
- aliases never become canonical IDs;
- runtime prompt assembly remains projection-only and narrowing-only;
- OG-1 and OG-2 remain HUMAN DECISION REQUIRED.

Add controlled mutation probes for each newly added substantive check. Do not count git-state/containment failures as substantive mutation detection.

## Regression / containment

Run and report:

- package validator default / verbose / JSON if implemented;
- package mutation probes;
- Phase 8 validator;
- Phase 9 validator;
- Phase 10 validator with inherited findings reported exactly;
- Phase 11 validator with inherited finding reported exactly;
- `git diff --check`;
- byte-identity / changed-path containment against the approved architecture baseline;
- clean final working tree.

Do not repair inherited Phase 10 or Phase 11 validator findings.

## Commit and push

If the remediation is coherent and validation passes:

- commit all remediation changes on `proposal/communication-difficult-conversations-specialist`;
- push the branch;
- do not create a PR.

Suggested commit message:

`docs: remediate communication specialist governance and fidelity blockers`

## Required report

Return sections A–R:

A. Remediation summary
B. Exact baseline / containment
C. Epistemic-model remediation
D. Review-trigger remediation
E. Diagnostic no-gate contract
F. Filter / diagnostic schema reconciliation
G. TA-7 / external-publication reassessment
H. Evaluation / adversarial hardening
I. OG-1 decision memo
J. OG-2 decision memo
K. Remaining OG-3..OG-8 classification
L. Package validator / mutation results
M. Regression results
N. Changed files
O. Known limitations
P. Harness credibility
Q. Remaining blockers
R. Readiness verdict

If all technical blockers are closed but OG-1 and OG-2 still await human choice, the final verdict must be exactly:

`READY FOR HUMAN GOVERNANCE DECISION ON OG-1 AND OG-2 — NOT YET READY FOR PACKAGE APPROVAL`

If any technical blocker remains, report `NOT READY — REMAINING BLOCKERS`.
