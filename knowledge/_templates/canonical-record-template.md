# Canonical Record Template

Status: PROPOSED — Phase 8 standard candidate
Template Version: 0.1
Inherits: `standard.knowledge.common_constraints@0.1`

A **Canonical Record** is a Knowledge Record that has been promoted: the organisation's governed position on one subject, **for one scope, at one version, from one effective date**. It carries everything the Knowledge Record template requires, plus what follows.

It is a **semantic model**, not a schema. **It is never edited in place** — a correction is a new version, promoted, superseding this one.

---

## Canonical Identity
- Canonical ID: stable across every version of this subject in this scope
- Canonical version: the version **this** promotion adopted
- Subject / entity identity
- Scope — the one scope in which this governs

## Canonical Status
`CANONICAL` / `SUPERSEDED` / `RETRACTED`, with the act that produced it.

## Effective Period
- Effective from:
- Review-by:
- Expiry:

A canonical statement with no effective-from has not said when it began governing, and is defective.

## Scope Relationships

Any canonical statement on the same subject in a **wider** scope that this **overrides**, named explicitly; and any narrower-scope statements known to override this. An override that names nothing it overrides creates a scope conflict.

## Promotion Basis

- the epistemic type promoted, and why it is promotable;
- the evidence relied on, **at the versions relied on**;
- the Review Profiles satisfied, or the exceptional progression exercised over each unsatisfied one;
- the criticality band and what it required;
- the confirmation that no material conflict was outstanding;
- **the reason for promotion** — why this became the organisation's position now.

## Promotion Decision Reference

The `decision.<id>` exercised and its Decision Record reference. Until the Phase 7 pass of `knowledge/canonical-promotion-governance.md` §7 runs, this section records that **no promotion authority is yet exercisable** and the record is a candidate, not a canonical statement.

## Supersession Linkage

Supersedes / superseded-by, with the reason. Supersession is the automatic effect of promoting a successor for the same subject and scope — never a free-standing act. **The superseded version's content stays intact and readable.**

## Retraction

Where retracted: the reason, the finding that established it, **the gap this leaves** — what the scope now has no position on — and what depended on it. **None** where not retracted.

## Conflict Links

Conflicts raised against this record, before or after promotion, with class and materiality and resolution status. **A canonical record may be simultaneously canonical and in conflict**, and showing both is the point.

## Uncertainty Carried Into Canonical Status

What remains unestablished about a statement the organisation has nonetheless adopted. Promotion does not remove uncertainty; it decides to proceed with it, and this section is where that survives.

## Applicability Conditions

The conditions under which this governs, and the conditions under which it does not.

## Artifacts Expressing This

Which artifacts state this claim, at which of their versions. **Replacing any of them changes nothing here.**

## Governance Owner Class

Never a named person.

## Audit History

Every promotion, supersession, retraction, conflict, resolution and scope change, in order, append-only.

## Non-Runtime Statement

This record is declarative. It specifies no schema, storage, index, embedding, retrieval, API, interface, access control or runtime, and binds no person, organisation, provider or model identity.
