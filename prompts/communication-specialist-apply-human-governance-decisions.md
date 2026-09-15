# Claude Prompt — Apply Human Governance Decisions OG-1 / OG-2

Repository: `dgerman-code/AI-OS`

Branch: `proposal/communication-difficult-conversations-specialist`

Human decision record commit: `903c58dfa565f5f14a9af19efcccceabae328f26`

Governed package baseline before the decision record: `9686c90339cd0d2dd4b9a7d3a8a4076dfce660d0`

## Mission

Apply the two explicit human governance decisions recorded in:

`proposals/communication-difficult-conversations-specialist/human-governance-decisions-og1-og2.md`

The decisions are:

`DECIDE OG-1: NORMALIZE IDENTIFIERS`

`DECIDE OG-2: PROFESSIONAL DELIVERY ROLE`

This is a controlled package update, not package approval.

## Hard boundaries

Do not modify approved Phase 1–13 artifacts.
Do not modify Phase 14 artifacts.
Do not modify the approved Phase 15 architecture or its approval record.
Do not create or approve any Decision Right.
Do not resurrect `decision.external_high_stakes_communication_send`; it remains `WITHDRAWN_FROM_CURRENT_PACKAGE`.
Do not grant send/publication/contract/legal authority to the Role.
Do not create runtime code, database migrations, provider bindings, deployments, secrets, queues, workers or infrastructure.
Do not create a PR.
Do not mark the package or its candidate registry artifacts `APPROVED` or `CANONICAL`.
Do not claim activation, production readiness or execution readiness.

## Required work

### 1. Record the decisions in active package governance material

Update the existing governance note and self-check so that OG-1 and OG-2 are no longer shown as unresolved human decisions.

They must be shown as:

- OG-1 — `HUMAN DECISION RECORDED: NORMALIZE IDENTIFIERS`
- OG-2 — `HUMAN DECISION RECORDED: PROFESSIONAL DELIVERY ROLE`

Reference the human decision record and its commit.

Do not rewrite history: preserve that the earlier baseline correctly deferred the decisions.

### 2. Normalize candidate identifiers

Apply the existing AI-OS identifier conventions consistently across the package.

At minimum, normalize:

- `pack.communication.difficult_conversations@0.1` -> `skill_pack.communication_difficult_conversations@0.1`
- `method.communication.calm_direct_control@0.1` -> a single normalized methodology ID consistent with the package's chosen registry convention; prefer `method.communication_calm_direct_control@0.1` unless an already-approved convention requires another exact form
- dotted workflow candidates -> `workflow.<stable_snake_case_name>@0.1`
- any other dotted candidate identifiers that conflict with the established templates

`review.communication_strategy@0.1` is already conformant unless the current package proves otherwise.

Update every cross-reference, mapping, evaluation scenario, workflow reference, validator assertion and probe.

Do not retain two canonical IDs for the same candidate object. Historical aliases may be documented only as traceability metadata.

### 3. Model the capability as a candidate Professional Delivery Role

The capability is a candidate **Professional Delivery Role**, proposed as the 60th Role in the existing Role universe.

The Role must remain clearly distinct from:

- `role.institutional_communications_editorial_specialist`
- `role.institutional_affairs_stakeholder_specialist`
- `role.people_organisation_specialist`
- `role.marketing_growth_specialist`
- substantive Legal, Procurement, Grant, Finance, Technical and other domain Roles

The Role owns communication-strategy outputs only. It must never own or overwrite substantive domain conclusions supplied by other Roles.

Preserve the package's existing principles:

- communication strategy / framing / tone / brevity / boundary formulation / respond-or-not / de-escalation / redirect / documentation strategy / meeting preparation
- no legal conclusion
- no financial conclusion
- no contract interpretation
- no compliance conclusion
- no technical truth
- no institutional position unless supplied by the owning Role/human authority
- no publication/send authority
- no canonicalisation authority
- no psychological diagnosis

Align the Role Card to the current Role Card standard and candidate status conventions.

### 4. Candidate Skills / Skill Pack / methodology alignment

Reconcile the eight candidate Skills, Skill Pack and methodology with the Role decision.

Create or update candidate mapping artifacts where necessary so that:

- the Role's required Skills are explicit;
- required candidate Skills remain candidate / PROPOSED and cannot activate until governed registration permits them;
- approved existing Skills are referenced rather than duplicated;
- Skill Pack composition follows Phase 4 conventions;
- candidate Skill absence fails closed where the package already specifies blocking behaviour.

Do not mass-edit approved registries to insert the Role or Skills. Keep this package as the governed proposal surface unless an existing proposal-side mapping convention explicitly supports candidate records.

### 5. Workflow and Review Profile alignment

Update candidate workflows and Review Profiles to use normalized IDs and the Professional Delivery Role decision.

Preserve one mandatory review trigger RC-5 with its four conditions and RC-5a.

Preserve the distinction:

- Role produces communication-strategy artifacts/conclusions;
- Review Profile independently reviews them;
- Decision Right governs external release/send where applicable;
- substantive domain Roles own substantive conclusions carried into the communication artifact.

No self-review loophole may be introduced.

### 6. Reassess OG-5 / OG-6 / OG-8

Because OG-2 is now decided, reassess mechanically:

- OG-5 candidate Skills
- OG-6 Role-to-Skill mappings
- OG-8 full-Profile reviewer availability

Close only what is actually resolved by the package update.

Do not close:

- OG-4 Phase 7 adjacent-right observation unless the approved Phase 7 register changed separately
- OG-7 routing/evaluation calibration evidence question unless evidence actually exists

### 7. Attribution / Jefferson Fisher boundary

Retain the legally conservative attribution boundary:

> Communication methodology informed by publicly available principles associated with Jefferson Fisher's work on difficult conversations, boundaries, clarity, assertiveness, emotional self-control, and conversational leadership.

And, where public-facing attribution is present:

> Not affiliated with or endorsed by Jefferson Fisher.

Do not claim endorsement, affiliation, certification, training, licensing or proprietary access. Do not reproduce proprietary books, courses, transcripts or long-form copyrighted material.

### 8. Decision Rights

Revalidate TA-1 through TA-7 against the current approved Phase 7 material.

Expected posture unless the repository proves otherwise:

- `decision.external_publication` covers external release of one content item at a stated version to an audience outside the entity under the entity's name, including private correspondence where those elements are satisfied
- granting-authority / contract-commitment and other applicable rights remain separate where triggered
- `decision.external_high_stakes_communication_send` remains withdrawn

Do not invent a new Right to simplify the package.

### 9. Evaluation suite

Update the evaluation scenarios and hard-fail tests for normalized IDs and the Role decision.

Add explicit positive and negative cases that prove at least:

- cross-domain use without substantive-authority leakage
- legal conclusion remains legal-owned
- communication Role can own framing without owning legal truth
- low-stakes but consequential boundary still fires RC-5 when required
- read-only diagnosis stays gate-free only while no external act is contemplated
- external correspondence uses applicable Decision Rights
- no candidate Skill / Role / Workflow becomes approved merely because the planner wants it
- no user request is silently narrowed when a required professional conclusion is unavailable

### 10. Assurance

Run and strengthen:

- `validation/communication_package_validation.py`
- `validation/communication_package_probes.py`
- Phase 8 validator
- Phase 9 validator
- Phase 10 validator
- Phase 11 validator

Preserve inherited Phase 10 / Phase 11 failures exactly unless an approved upstream change independently changed them. Do not repair them from this branch.

Add adversarial probes for at least:

- old dotted IDs surviving in active normative locations
- duplicate canonical IDs
- Role accidentally treated as Specialisation-only
- candidate Role treated as approved/activatable
- candidate Skills treated as approved/activatable
- Role acquiring substantive legal/financial/contract authority
- Review Profile satisfied by the Role's own production
- Decision Right satisfied by Role ownership
- withdrawn TA-7 resurrected
- external send occurring without applicable Decision Right
- SOURCE -> FACT_CLAIM mutation
- diagnostic NOT_APPLICABLE incorrectly carried into a send workflow

Report first-run REDUNDANT / ERROR probes honestly and explain any assurance defects they expose.

## Completion criteria

Return a report with sections A–R.

At minimum state:

- exact starting baseline
- exact final commit SHA
- changed-file list
- identifier normalization table
- candidate Role status and ID
- candidate Skills / mapping status
- workflow / review-profile changes
- OG-1 / OG-2 status
- OG-4 through OG-8 status
- Decision Right reassessment
- attribution boundary
- validation results
- mutation results
- inherited Phase 10 / Phase 11 results
- containment check
- remaining blockers
- readiness verdict

The only acceptable positive readiness line is:

`READY FOR INDEPENDENT COMMUNICATION SPECIALIST PACKAGE RE-AUDIT`

Do not claim package approval.
