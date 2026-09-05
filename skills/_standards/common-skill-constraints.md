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

## 4. Knowledge-State Discipline

Activation of a Skill or Pack does not change knowledge state by itself.

A Skill or Pack must not:
- treat AI-generated material as SOURCE or FACT;
- convert ASSUMPTION to FACT without evidence;
- convert DRAFT to REVIEWED without the applicable review path;
- convert REVIEWED to APPROVED without the applicable human decision path;
- convert any material to CANONICAL without canonical-governance authority.

Conflicts among controlled sources, versions or requirements must be surfaced as `CONFLICT_DETECTED` or equivalent workflow escalation.

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

## 6. Role Compatibility

Every Skill or Pack must define compatible Role IDs or a governed compatibility rule.

Compatibility does not mean ownership. A Skill may be reusable across multiple Roles.

Relationship types:
- `REQUIRED_CORE`
- `REQUIRED_FOR_CONTEXT`
- `OPTIONAL`
- `ALTERNATIVE`
- `PROHIBITED_IN_CONTEXT`

A Role-Skill mapping must not create a new Role identity by combination.

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

Recommended levels may later include:
- AWARENESS
- WORKING
- ADVANCED
- EXPERT

These levels do not grant professional or human authority.

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

## 11. Role-vs-Skill Escalation Test

If a candidate capability appears to require any of the following, stop and reassess whether it should be a Role or another registry entity:
- distinct professional methodology ownership;
- materially distinct authority boundary;
- recurring standalone professional decision-grade artifact ownership;
- independent reviewer identity;
- human approval authority;
- system-control orchestration authority.

Do not solve ambiguity by creating a hybrid Skill that behaves like a hidden Role.