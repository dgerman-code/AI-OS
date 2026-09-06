# Common Skill Constraints

Status: PROPOSED — Phase 4 standard candidate
Standard ID: `standard.skill.common_constraints`
Version: 0.1

## Purpose

Defines the universal constraints inherited by every Skill, Specialisation and Skill Pack in AI-OS.

## 1. Registry Separation

A Skill, Specialisation or Skill Pack:
- is not a Role;
- is not a Review Profile;
- is not a Human Decision Right;
- is not a System Control Profile;
- is not a model/runtime binding.

It must not acquire authority merely because it is activated on an assignment.

## 2. Authority Boundary

A Skill or Pack may refine how an approved Role performs work, but must not:
- widen the Role Card's Professional Scope;
- create a new Professional Decision Right;
- create, transfer or assume human approval authority;
- authorize external submission, publication, filing, deployment or binding commitment;
- override required independent review;
- promote an artifact to APPROVED or CANONICAL;
- override a more restrictive Role Card, workflow rule or assignment control.

Where a Skill or Pack identifies a need for review or human decision, it may only reference the applicable `review.<id>` or `decision.<id>` dependency.

## 3. Output Ownership

Skills do not own first-class professional artifacts independently of Roles.

A Skill may:
- contribute methods, calculations, checks, templates or sub-artifacts;
- refine how a Role-owned artifact is produced;
- specify evidence or validation requirements.

The assigned Role remains authoritative for professional output ownership and professional conclusions.

### 3.1 Support-only boundary

Where a Skill touches the methodology of a different approved Role, it is **support-only** and must say so explicitly, naming the Role that retains ownership. A support-only Skill produces inputs to that Role's conclusion; it never produces the conclusion, and it never allows the mapped Role to be represented as the owner of it.

### 3.2 Quality control is not independent review

Capabilities that evaluate, validate, test, check readiness or otherwise assess work — including publication-requirements validation, control validation, security testing, output evaluation and editorial quality control — are **quality-control techniques, not independent review**. They do not satisfy an `Author != Critical Reviewer` obligation, do not discharge a Review Profile, and do not create reviewer identity. Where independent review is required, it is performed under the applicable `review.<id>` by someone who did not author the work.

### 3.3 Role-owned artifact boundary

Every Skill states which Role-owned artifact it contributes to and what part of that artifact it does **not** produce. A Skill that cannot name an owning Role and artifact is a candidate hidden Role and must be reassessed under section 11.

## 4. Knowledge-State Discipline

Activation of a Skill or Pack does not change knowledge state by itself.

A Skill or Pack must not:
- treat AI-generated material as SOURCE or FACT;
- convert ASSUMPTION to FACT without evidence;
- convert DRAFT to REVIEWED without the applicable review path;
- convert REVIEWED to APPROVED without the applicable human decision path;
- convert any material to CANONICAL without canonical-governance authority.

Conflicts among controlled sources, versions or requirements must be surfaced as `CONFLICT_DETECTED` or equivalent workflow escalation.

A Skill may contribute to Role-owned knowledge-state work — recording state metadata, assembling the evidence a transition would require, checking that stated conditions are met — but **a Skill can never execute a knowledge-state transition**. The transition is performed by the owning Role under the applicable review and decision path, or it does not happen.

## 5. Controlled Sources and Currency

Where a Skill or Pack depends on external rules, standards, programmes, institutions, technologies or jurisdiction-specific requirements, it must identify enough metadata to determine currency.

As applicable, record:
- source / authority;
- version;
- effective date;
- expiry / review date;
- jurisdiction;
- programme call / framework version;
- technology version;
- supersedes / superseded-by relationship.

Expired, superseded or unverifiable references must not be treated as current requirements.

## 6. Role Compatibility and the Canonical Mapping Source

**Role-to-Skill mapping records are the sole authoritative source for relationship type and context trigger.**

Every Skill or Pack must define compatible Role IDs or a governed compatibility rule. Compatibility does not mean ownership, and a Skill may be reusable across multiple Roles.

A Skill, Specialisation or Pack Card **may**:
- declare a compatible-Role allowlist or a governed compatibility rule;
- reference the canonical mapping record;
- describe typical use in clearly advisory, non-authoritative language.

A Skill, Specialisation or Pack Card **must not**:
- independently declare `REQUIRED_CORE`, `REQUIRED_FOR_CONTEXT`, `OPTIONAL`, `ALTERNATIVE` or `PROHIBITED_IN_CONTEXT` as a writable role relationship;
- define, qualify or override a context trigger or an alternative choice condition.

The five relationship classes remain the controlled vocabulary, but they are written only in mapping records. Where a card's advisory text diverges from the mapping record, the mapping record governs and the divergence is raised as `CONFLICT_DETECTED`.

A Role-Skill mapping must not create a new Role identity by combination.

### 6.1b Duplicate effective activation

Where a Skill is both individually mapped to a Role and included as a required Skill of an active Pack, it is activated once, under the stricter of the two obligations, with the Pack's currency and evidence rules applied on top. Duplicate effective activation must be detectable at validation time; it must not be left to resolve itself at execution.

### 6.1 Direct Mapping Compatibility Rule

**For every active Role-to-Skill, Role-to-Specialisation or Role-to-Skill-Pack mapping: if the target capability has a card, the consuming Role MUST be permitted by that card's compatible-role allowlist or by a governed compatibility rule. Absence from the allowlist is a validation failure.**

- Runtime may **not** widen an allowlist. A mapping that names a Role the card does not permit fails validation; it does not quietly succeed.
- Remediation has exactly two governed outcomes: **(a)** widen compatibility through a card change, after reviewing the consuming Role Card and confirming the capability does not widen its authority; or **(b)** remove or reclassify the mapping. Choosing (a) because the Role looks adjacent, without a Role Card basis, is not one of them.
- This rule defines **compatibility only**. It does not define relationship type or context trigger, which remain solely in Role-to-Skill mapping records.

This rule and the transitive rule below are complementary, and together they must cover four cases:

1. direct Role → Skill;
2. direct Role → Specialisation, where the Specialisation is carded;
3. direct Role → Skill Pack;
4. transitive Pack → component Skill.

The direct rule catches what the transitive rule cannot: a Role mapped straight to a capability without any Pack in between. Case 4 alone was checked before this rule existed, and cases 1 to 3 went unvalidated as a result.

### 6.1c Reverse Allowlist Basis Rule

Compatibility must be validated in **both** directions.

**Every Role named in a capability card's compatible-role allowlist must have an actual direct mapping to that capability, or a governed transitive basis through a Pack that is itself mapped to that Role. An allowlist entry with neither is an orphan, and an orphan is a defect.**

The forward rules (6.1, 6.1a) stop a mapping from naming a Role its target card rejects. This rule stops the opposite drift: a card quietly accumulating Roles that no mapping ever justified, which would let a future mapping be waved through on an allowlist entry that was never reviewed against a Role Card.

Where the basis for an allowlist entry disappears — a Pack mapping is removed, a direct mapping is reclassified — the entry must be removed in the same governed change, not left standing.

### Validation specification — the five checks a Phase 4 audit must run

Any independent audit of this registry must run all five and report them separately, never as a single aggregate:

| # | Path | Direction | Failure meaning |
|---|---|---|---|
| 1 | direct Role → Skill | forward | mapping names a Role the Skill Card rejects |
| 2 | direct Role → Specialisation, where carded | forward | mapping names a Role the Specialisation Card rejects |
| 3 | direct Role → Skill Pack | forward | mapping names a Role the Pack Card rejects |
| 4 | transitive Pack → component Skill | forward | Pack activation would pull in a component that rejects the consuming Role |
| 5 | allowlist entry → mapping basis | **reverse** | card permits a Role that no mapping justifies |

Targets without a card are reported as **NOT YET VALIDATABLE**, never as a pass: a check that cannot run has not succeeded. An audit reporting zero conflicts must state how many targets were actually checkable, because zero-of-few and zero-of-many are different results.

None of these five checks defines relationship type or context trigger. All five test compatibility only; relationship and trigger come solely from mapping records.

### 6.1a Transitive Pack Compatibility Rule

**If a Role is permitted to activate a Skill Pack, every Required Skill and every conditionally activated Skill inside that Pack must be compatible with that Role, either through the Skill Card allowlist or through a governed compatibility rule. A Pack must not transitively activate a Skill that explicitly excludes the consuming Role. This check does not create a Role relationship or trigger; it validates compatibility only.**

Clarifications:

- **Optional Pack components** that can be selected for a Role must likewise not be prohibited by their Skill Card allowlist. An Optional component is selectable, and a selectable component that the Role's own Skill Card rejects is the same defect as a Required one, discovered later.
- **Transitive dependencies count.** Where a Pack layers over another Pack, the components of the inherited Pack are activated for the consuming Role too, and are subject to this rule at every level of the chain.
- **On incompatibility, activation fails validation.** It must not silently widen the Skill allowlist at runtime. A runtime widening would let a Pack grant eligibility that no reviewed card records, which is precisely the second source of truth this architecture excludes. The correct resolutions are to add the Role to the Skill Card allowlist after review, to remove the Skill from the Pack, or to remove the Role from the Pack's allowlist — each a governed change to a card, not an inference at activation.
- **Compatibility is not a relationship.** Adding a Role to a Skill Card allowlist for Pack compatibility states only that the Role may use the capability. It creates no `REQUIRED_CORE`, `REQUIRED_FOR_CONTEXT`, `OPTIONAL`, `ALTERNATIVE` or `PROHIBITED_IN_CONTEXT` relationship, and no trigger. **Relationship type and context trigger still come only from Role-to-Skill mapping records.**
- **Direction of the fix matters.** This rule is satisfied by making the card set consistent, never by having a Pack override a Skill Card at activation time.

The rule is machine-checkable in principle: for each Pack, take its compatible-Role allowlist; for each Required and Optional component, take that component's compatible-Role allowlist; the Pack's allowlist must be a subset of every component's allowlist. Any Role in the Pack's allowlist but absent from a component's is a defect, reported per (Pack, component, Role).

### 6.2 Alternative choice sets

Where capabilities are alternatives, the mapping record names the choice set and the condition that selects between members. A card may reference the choice set it belongs to but must not define the selection condition.

### 6.3 Prerequisites and incompatibilities

A Skill or Pack must declare, where they exist:
- **prerequisite capabilities** — what must already be present for this capability to be applied competently;
- **incompatibilities** — capabilities, contexts or data classifications with which it must not be combined, and why.

Prerequisites are competence statements, not authority grants: satisfying every prerequisite still confers no authority beyond the assigned Role Card.

## 6A. Pack Structure and Dependency

A Skill Pack declares:
- `Type: Skill Pack`;
- the **Skill Families** it draws from (contributing families);
- the **Specialisations** it includes;
- the **Packs it depends on or layers over**, with direction stated;
- explicit dependency / layering metadata sufficient to resolve activation order.

Rules:
- **No circular pack dependencies.** A dependency cycle is a validation failure. If Pack A depends on Pack B, B must not depend directly or transitively on A.
- Dependency is transitive for activation, subject to the duplicate-activation rule in 6.1.
- **Precedence between overlapping Packs:** the stricter requirement prevails; where strictness is not comparable, the more specific Pack prevails over the more generic; where neither is clearly more specific, raise `CONFLICT_DETECTED` and escalate rather than resolving silently. Precedence never operates in the permissive direction.
- The Role Card and any stricter workflow or assignment control prevail over every Pack.
- **Pack activation cannot satisfy a licensing, competence, review-independence or human-authority requirement.** Activating a Pack never establishes that a licensed professional was involved, that an independent reviewer acted, or that a human decision right was exercised. Those obligations are discharged only through the Role Card, the applicable Review Profile and the applicable Decision Right.

## 7. Context and Assignment

Skills are activated per assignment.

Activation must respect:
- organisation / project / product / workstream isolation;
- assignment context;
- applicable jurisdiction / programme / sector / technology;
- criticality band;
- confidentiality / data classification;
- Role Card Context Breadth Limit.

A Pack must not silently import assumptions, confidential information or project-specific facts from another context.

## 8. Proficiency and Competence

Where proficiency is represented, it is an assignment attribute and not a new Skill identity.

The controlled proficiency vocabulary, used consistently across all Phase 4 architecture, standards and templates, is:
- AWARENESS
- WORKING
- ADVANCED
- EXPERT

No other proficiency vocabulary may be used in active Phase 4 files. These levels are assignment attributes only; they do not grant professional or human authority and must never be read as evidence of licensing, credentialing or regulated authorisation.

## 9. Model Independence

Skill identity must remain independent of AI model, agent framework and runtime.

Model-specific prompting, tool configuration or runtime optimization belongs to later Model / Execution architecture unless it is merely non-authoritative implementation guidance.

## 10. Change Control

A material change to any of the following requires a new Skill or Pack version rather than silent replacement:
- methodology;
- controlled-source basis;
- applicability boundary;
- compatible Roles;
- jurisdiction / programme / technology scope;
- mandatory evidence requirements;
- review / decision dependencies.

Historical versions must remain traceable when they were used in prior work.

Every Skill, Specialisation and Pack therefore carries explicit `Supersedes` and `Superseded By` metadata. A superseded item must not silently continue to satisfy a mapping: supersession is resolved at activation, and an expired or superseded item cannot discharge a `REQUIRED_CORE` or `REQUIRED_FOR_CONTEXT` obligation.

## 11. Role-vs-Skill Escalation Test

If a candidate capability appears to require any of the following, stop and reassess whether it should be a Role or another registry entity:
- distinct professional methodology ownership;
- materially distinct authority boundary;
- recurring standalone professional decision-grade artifact ownership;
- independent reviewer identity;
- human approval authority;
- system-control orchestration authority.

Do not solve ambiguity by creating a hybrid Skill that behaves like a hidden Role.