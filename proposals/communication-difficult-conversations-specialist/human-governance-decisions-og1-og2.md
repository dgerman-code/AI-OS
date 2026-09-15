# Communication Specialist — Human Governance Decisions OG-1 / OG-2

Status: `APPROVED — HUMAN DECISION`

Decision Date: `2026-09-15`

Package branch: `proposal/communication-difficult-conversations-specialist`

Governed package baseline at decision time: `9686c90339cd0d2dd4b9a7d3a8a4076dfce660d0`

## Human decisions

The human governance authority explicitly decided:

`DECIDE OG-1: NORMALIZE IDENTIFIERS`

`DECIDE OG-2: PROFESSIONAL DELIVERY ROLE`

These are explicit governance decisions. They do not by themselves approve the communication-specialist package, activate any capability, create or approve any Decision Right, or make any runtime or production claim.

## OG-1 — identifier shape

Decision: **NORMALIZE IDENTIFIERS**.

The candidate package is to use the existing AI-OS registry conventions rather than preserve the dotted namespace variants from the originating prompt.

Required normalization includes, at minimum:

- Skill Pack IDs: `skill_pack.<stable_snake_case_id>`;
- Methodology IDs: `method.<stable_snake_case_id>` unless an approved registry convention requires a more specific existing shape;
- Workflow IDs: `workflow.<stable_snake_case_name>`;
- Review Profile IDs: `review.<stable_snake_case_name>`;
- all internal references, mappings, examples, evaluation fixtures and validation assertions must be updated consistently;
- obsolete aliases may be recorded for traceability but must not become second canonical identities.

This decision authorises the mechanical normalization required to align the candidate package with existing registry conventions. It does not approve the normalized artifacts.

## OG-2 — Role versus Specialisation

Decision: **PROFESSIONAL DELIVERY ROLE**.

The difficult-conversations / communication-strategy capability is to be modelled as a candidate Professional Delivery Role rather than only as a Specialisation or methodology pack attached to existing Roles.

Governance rationale accepted by the human decision:

- the capability owns recurring standalone professional artifacts;
- it owns a distinct professional communication-strategy conclusion;
- it requires discoverable cross-domain activation;
- it needs a clear full-Profile reviewer path;
- its domain boundary is distinct from substantive legal, commercial, financial, HR, institutional, marketing or editorial authority;
- it must remain non-authoritative with respect to substantive conclusions owned by those other Roles.

The candidate Role is therefore to be treated as the proposed 60th Professional Delivery Role in the Role universe, subject to the normal Role Registry, Skill Registry, mapping, review and approval process.

This decision does not itself register or approve the Role.

## Consequences for the package

The next change-control pass may now:

1. normalize all affected candidate identifiers and references;
2. retain the candidate Role as a Professional Delivery Role and align its Role Card to the standard Role Card contract;
3. align candidate Skills, Skill Pack, methodology, workflows and Review Profiles to the Role decision;
4. create or update candidate Role-to-Skill / Role-to-Workflow / review-eligibility mapping artifacts where the package architecture requires them;
5. close OG-1 and OG-2 in the package self-check and governance note as `HUMAN DECISION RECORDED`;
6. reassess OG-5, OG-6 and OG-8 mechanically in light of the Role decision;
7. keep OG-4 as a Phase 7 observation and OG-7 as an evidence/calibration question unless separately governed;
8. keep `decision.external_high_stakes_communication_send` withdrawn from the current package;
9. keep `decision.external_publication` and any other approved Decision Rights separate from the Role — Role ownership never grants send/publication authority.

## Attribution / methodology boundary

The package may continue to describe the methodology as informed by publicly available principles associated with Jefferson Fisher's work on difficult conversations, boundaries, clarity, assertiveness, emotional self-control and conversational leadership, but it must not impersonate him, claim affiliation, endorsement, training or licensing, or reproduce proprietary material.

Recommended public-facing attribution remains:

> Communication methodology informed by publicly available principles associated with Jefferson Fisher's work on difficult conversations, boundaries, clarity, assertiveness, emotional self-control, and conversational leadership.

Recommended disclaimer remains:

> Not affiliated with or endorsed by Jefferson Fisher.

## Approval boundary

This record settles only OG-1 and OG-2.

It does **not**:

- approve the communication-specialist package;
- approve or activate the candidate Role;
- approve candidate Skills, Skill Packs, Workflows or Review Profiles;
- create or approve any Decision Right;
- grant publication, sending, contractual, legal or other authority;
- satisfy an independent package audit;
- claim runtime, production or deployment readiness;
- create a pull request.

After the decisions are mechanically applied, the resulting candidate baseline requires an independent package re-audit before any package-level approval may be requested.
