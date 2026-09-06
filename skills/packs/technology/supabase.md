# Supabase Technology Pack

Status: PROPOSED — Phase 4 exemplar Skill Pack Card

## Identity
- Pack Name: Supabase
- Pack ID: `skill_pack.supabase`
- Type: Skill Pack
- Pack Class: `TECHNOLOGY`
- Contributing Skill Families: Software / Integration / Platform / Security; Data / Analytics / AI
- Included Specialisations: `specialisation.relational_data_platform`
- Version: 0.1
- Status: PROPOSED
- Governance Owner: AI-OS Skill Registry Governance — human-controlled
- Effective Date: bound at instantiation to the platform version and service tier in use
- Review Date: on platform major version change or service-limit revision
- Expiry / Invalidation Trigger: see Deactivation / Invalidation Criteria
- Inherits: `standard.skill.common_constraints@0.1`
- Supersedes: none
- Superseded By: none

## Purpose
Carry the platform-specific constraints that Supabase imposes on architecture and data design, so that a design is made against what the platform actually does at a known version rather than against a general idea of a managed Postgres backend.

**This card defines architecture and controlled-source requirements only. It deliberately contains no current service limits, quotas, pricing tiers, feature availability or API surface.** Those change without notice and any figure written here would become a confidently stated falsehood. They are bound at instantiation from authoritative vendor documentation and refreshed whenever the Pack is updated.

## Scope
### Covers
Platform-specific controlled topics, each to be populated from authoritative vendor documentation at instantiation:

- **Relational platform use** — the managed PostgreSQL layer: extension availability, connection and pooling behaviour, migration mechanics, backup and point-in-time recovery characteristics, and which Postgres capabilities the managed layer constrains.
- **Authentication and authorisation** — the identity model, session and token behaviour, and row-level security as the platform's primary authorisation mechanism, including the design consequence that authorisation lives in the database rather than only in application code.
- **Storage** — object storage model, access control, and how storage authorisation relates to the database authorisation model.
- **API surface** — auto-generated interfaces, their coupling to schema, and the versioning consequence that schema change is interface change.
- **Realtime and edge behaviour** where in scope.
- **Version and service-limit currency** — the bound platform version, service tier and the limits applying to it.
- **Deployment and integration assumptions** — environment separation, migration promotion path, secret handling, and integration constraints with adjacent platforms.
- **Data, confidentiality and residency constraints** — region selection, data location and what the platform can and cannot guarantee.

### Does Not Cover
- first-class professional Role authority;
- independent review authority;
- human approval authority;
- model/runtime selection;
- any Role scope not already granted by the assigned Role Card.

This Pack binds a **platform**, not a model or runtime. It introduces no AI model, agent framework or execution binding of any kind, and nothing in it may be read as selecting one.

## Compatible Roles — Allowlist Only

**Role-to-Skill mapping records are the sole authoritative source for relationship type and context trigger. This card is not.**

- Compatible Role allowlist: `role.solution_architect`, `role.data_database_architect`, `role.full_stack_software_engineer`, `role.integration_api_engineer`, `role.platform_devops_engineer`, `role.database_data_engineer`
- Canonical mapping reference: `skills/mappings/wave-1-exemplar-role-skill-mapping.md`, sections 8 and 9
- Canonical mapping reference (Wave 2): `skills/mappings/wave-2-domain-completion-role-skill-mapping.md`

### Wave 2 allowlist basis

Four engineering Roles are admitted — the "Wave 2 mapping decisions" the paragraph above anticipated. Each works directly against the platform within its own approved scope: Full-Stack implements features against it, Integration / API builds against its interface surface, Platform / DevOps operates its environments and release path, and Database / Data Engineer implements migrations and pipelines on its managed relational layer.

`role.security_engineer` remains deliberately absent, and Wave 2 does not map this Pack to it. Platform-specific security constraints reach that Role through the architecture Roles' outputs. Its exclusion, and the matching exclusion on `skill.quality_attribute_analysis`, were independently confirmed as correct and are unchanged.

Activation still authorizes no production change: `decision.production_release`, `decision.production_infrastructure_change` and `decision.production_database_migration` remain human decision rights. Eligibility only; relationship and trigger come from the Wave 2 mapping record.

`role.full_stack_software_engineer`, `role.integration_api_engineer`, `role.platform_devops_engineer`, `role.database_data_engineer` and `role.security_engineer` all work against this platform in practice, but none is mapped to this Pack in the current record and none is listed. That is a Wave 2 mapping decision, and the omission is deliberate rather than an oversight.

Listing a Role confers eligibility, never a requirement.

### Typical Use — Advisory, Non-Authoritative
Non-binding: usually relevant where Supabase is part of the selected or constrained platform context and its behaviour materially bounds the architecture or data design. States no obligation; the mapping record decides.

## Included Skills
### Required Skills
- `skill.quality_attribute_analysis` — platform constraints bound achievable quality attributes, and the constraint set is only useful once allocated.
- `skill.data_model_design` — the platform's authorisation model is expressed in the data model, so the two cannot be designed independently.

### Optional Skills
- `skill.schema_design`
- `skill.api_contract_design`
- `skill.integration_pattern_selection`
- `skill.data_quality_rule_design`
- `skill.observability_design`

### Alternative Skills
None.

## Pack Dependencies and Layering
- Depends on / layers over: none declared. A PostgreSQL Pack and this Pack overlap on the relational layer, but the relationship is resolved by precedence rather than dependency, since Supabase constrains rather than extends generic PostgreSQL behaviour.
- Depended on by (informational): none currently.
- Layering metadata: not applicable.

No circular dependency is possible for this Pack, since it declares none.

## Precedence With Overlapping Packs
Where another active Pack addresses the same subject with different requirements:
1. the **stricter** requirement prevails;
2. where strictness is not comparable, the **more specific** Pack prevails — on the managed relational layer, this platform Pack is more specific than a generic PostgreSQL Pack and prevails where the managed platform constrains generic behaviour;
3. where neither is clearly more specific, raise `CONFLICT_DETECTED` and escalate rather than resolving silently;
4. the Role Card and any stricter workflow or assignment control prevail over this Pack.

Precedence never operates in the permissive direction. Where generic PostgreSQL guidance permits something the managed platform does not, the platform constraint governs.

## Duplicate Effective Activation
`skill.quality_attribute_analysis` and `skill.data_model_design` are both individually mapped to Roles in the current record and are also required Skills here.

Where a Skill in this Pack is also mapped individually to the same Role, it is activated **once**, under the **stricter** of the two obligations, with this Pack's platform constraints applied on top. The individual mapping is retained only where it has meaning independent of this Pack — which it does for both, since neither is Supabase-specific.

Duplicate effective activation must be detectable at validation time, not discovered during execution.

## Authority Limits of Activation
Activating this Pack **cannot** satisfy:
- a licensing or regulated-authorisation requirement;
- a competence requirement for a licensed or authorised professional;
- a review-independence requirement or any `review.<id>`;
- a human authority requirement or any `decision.<id>`.

Specifically:
- **Activation does not authorize production change.** Production release is gated by `decision.production_release`, infrastructure change by `decision.production_infrastructure_change`, and database migration by `decision.production_database_migration`. Knowing the platform is not permission to change it.
- **Does not replace Security Engineer ownership.** Row-level security design produced under this Pack is an architecture constraint, not a security control adequacy conclusion; that remains with `role.security_engineer` under `review.security`.
- **Does not replace Data Protection ownership.** Region and residency selection informs but never substitutes for `role.data_protection_gdpr_specialist`'s conclusions, gated by `decision.dpia_acceptance` and `decision.lawful_basis_adoption`.
- **Does not replace Data Architect, DevOps or Integration ownership.** Migration design, deployment pipeline and integration implementation remain with `role.data_database_architect`, `role.platform_devops_engineer`, `role.database_data_engineer` and `role.integration_api_engineer` respectively.
- **Does not authorize vendor commitment.** Technology selection is gated by `decision.technology_selection`.

## Applicability
- Jurisdiction(s): unrestricted; region selection has jurisdictional consequences for data location.
- Sector(s): unrestricted.
- Programme / framework: not applicable.
- Institution / financing framework: not applicable.
- Technology / version: Supabase at the bound platform version and service tier. The Pack is not applicable outside the version it was bound against.
- Operating context: architecture and data design for a Supabase-backed product.
- Criticality conditions: at Enhanced Decision-Grade and above, platform constraints relied on must be evidenced from vendor documentation at a stated version, not from practitioner recollection.
- Assignment prerequisites: the platform version, service tier and region must be identified.

## Controlled Methodology / Source Package
Required at instantiation and **refreshed from authoritative vendor documentation whenever the Pack is instantiated or updated**, each captured with source / authority, title / identifier, version, effective date, expiry or supersession status, and applicability:
- vendor platform documentation for the bound version;
- published service limits and quotas for the bound tier;
- the underlying PostgreSQL version and its documentation;
- authentication, authorisation and storage documentation;
- API and client-library documentation at the bound versions;
- region, residency and sub-processor documentation;
- the vendor's terms, service levels and data-processing terms.

**AI-generated content must not be listed as a controlled source**, and neither may a blog post, a community answer or recollection of prior platform behaviour. A platform constraint asserted without a versioned vendor reference is an ASSUMPTION and must be labelled one.

## Evidence Requirements
- Required evidence classes: versioned vendor documentation; measured behaviour from a bound environment where documentation is silent.
- Minimum source quality: vendor's own current documentation for the bound version.
- Required provenance: every stated constraint traceable to a document and version, or to a dated measurement.
- Currency requirements: constraints current for the bound platform version; a constraint from a prior version is SUPERSEDED.
- Assumptions that must remain explicit: any constraint inferred from behaviour rather than documented.
- Reproducibility requirements: measurements repeatable in the bound environment.

## Knowledge-State Constraints
- Minimum input state for ordinary use: platform constraints at SOURCE state from vendor documentation.
- Minimum input state for decision-grade use: constraints relied on for an architecture conclusion at REVIEWED or better, with version anchoring.
- States the Pack may support deriving: SOURCE and FACT for documented constraints; ASSUMPTION for inferred behaviour; CONFLICT_DETECTED where documentation and observed behaviour disagree; UNKNOWN where a limit is undocumented.
- States the Pack may not promote autonomously: REVIEWED, APPROVED, CANONICAL.
- Conflict / contradiction escalation rule: divergence between vendor documentation and observed platform behaviour is raised as `CONFLICT_DETECTED` and escalated. It is never resolved by assuming the documentation is merely out of date.

Skills in this Pack may contribute to Role-owned knowledge-state work but **can never execute a knowledge-state transition**.

## Review Dependencies
- Review Profile Reference(s): none at Pack level; resolved by the consuming Role and workflow. Consuming assignments carry `review.architecture`, `review.security` and `review.data_architecture` as applicable to their Role.
- Trigger condition: set by the consuming Role Card.

These are dependencies only; the Pack does not perform independent assurance by identity.

Any validation, testing or checking capability applied under this Pack is a **quality-control technique, not independent review**. It does not discharge a `review.<id>`, does not satisfy an `Author != Critical Reviewer` obligation and creates no reviewer identity.

## Decision Dependencies
- Decision Right Reference(s): none at Pack level; resolved by the consuming Role and workflow. Consuming assignments carry `decision.architecture_adoption`, `decision.technology_selection`, `decision.production_release`, `decision.production_database_migration` and `decision.data_retention_policy_change` as applicable to their Role.
- Trigger condition: set by the consuming Role Card.

These are dependencies only; the Pack does not acquire human authority.

## External / Regulated Boundary
- Licensed / regulated activity boundary: none intrinsic.
- Required authorised professional class: none intrinsic.
- External submission / filing / publication boundary: publishing an auto-generated interface to external consumers is an external act gated by `decision.api_contract_publication`.
- Production / deployment boundary: every production change is gated; activation grants none of it.
- Withdrawal / correction path: through the applicable engineering Role's rollback path, not through this Pack.

## Data / Confidentiality Controls
- personal data categories: whatever the product stores; the platform does not bound this.
- privileged / legally sensitive information: possible depending on product.
- commercial / restricted information: platform configuration and secrets.
- storage / residency requirements: determined by bound region; residency guarantees must come from vendor documentation, never assumption.
- cross-context reuse restrictions: configuration, keys and data from one project's instance must never be imported into another context.

## Version and Change Control
A new Pack version is required on material change in: platform major version; the underlying PostgreSQL version; service limits or tier definitions; authentication, authorisation or storage model; API surface or client libraries; region or sub-processor set; vendor terms; compatible Role set; or review / decision dependencies.

## Activation Criteria
Supabase is part of the selected or constrained platform context for the assignment.

## Deactivation / Invalidation Criteria
- the platform is no longer in the selected context;
- the bound platform version, tier or region changes;
- vendor documentation for the bound version is superseded;
- observed behaviour diverges materially from the bound documentation and remains unresolved.

A stale Pack must not silently satisfy a contextual mapping obligation.

## Pack Integrity Rules
- Required Skills must be present when the Pack is activated unless an explicit governed exception exists.
- Optional Skills do not widen Role authority.
- Pack activation must not silently import configuration, secrets or data from another project context.
- Controlled references must be current for the assignment date and the bound version.
- Where Pack requirements conflict with the Role Card or a stricter workflow control, the stricter rule prevails and the conflict is escalated.

## Prerequisites and Incompatibilities
- Prerequisite capabilities or Packs: none. Competence statements only; confer no authority.
- Incompatibilities: must not be applied to a different platform, nor used outside its bound version. Must not be treated as satisfying security or data-protection ownership.

## Adjacent Packs
- `skill_pack.postgresql` — generic relational platform; this Pack prevails on the managed layer where it constrains generic behaviour.
- `skill_pack.vercel` — adjacent deployment platform; boundary is the deployment and edge surface.

## Completion / Use Criteria
Properly applied when the platform version, tier and region are bound; every constraint relied on is traced to versioned vendor documentation or a dated measurement; inferred behaviour is labelled ASSUMPTION; quality attributes are allocated against real platform limits; and no production act is treated as authorised by activation.

## Failure Modes to Avoid
- Using the Pack outside its bound version.
- Asserting a service limit from recollection.
- Treating row-level security design as a security adequacy conclusion.
- Treating region selection as a data-protection conclusion.
- Reading platform knowledge as production-change authority.
- Importing configuration or data across project contexts.

## Reclassification Warning
If the Pack begins to own a recurring standalone professional artifact, professional conclusion or authority boundary independent of an assigned Role, stop and reassess whether the capability belongs in the Role Registry instead.
