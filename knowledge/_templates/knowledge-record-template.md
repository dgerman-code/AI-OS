# Knowledge Record Template

Status: PROPOSED — Phase 8 standard candidate
Template Version: 0.1
Inherits: `standard.knowledge.common_constraints@0.1`

A **Knowledge Record** holds one claim, of one epistemic type, at one governance state, in one scope. This is a **semantic model**: it states what must be expressible and provable, not how anything is stored. No field type, identifier format, index or storage mechanism is specified or implied.

Sections are mandatory. One that does not apply is filled with an explicit "None" and a reason, never deleted.

---

## Identity
- Knowledge ID: `knowledge.<stable_snake_case_subject>.<discriminator>`
- Version:
- Subject / entity identity: *what this is about, named so that it cannot be confused with a same-named subject in another scope*
- Scope: *full path — `ORGANISATION/<x>`, `PROJECT/<x>`, `PERSONAL/<human>`*
- Memory class: `WORKING` / `EPISODIC` / `SEMANTIC` / `PREFERENCE` / `PROCEDURAL` / `CANONICAL` / `AUDIT`
- Sensitivity classification: one or more of `PUBLIC` / `INTERNAL` / `CONFIDENTIAL` / `RESTRICTED` / `PERSONAL_DATA` / `PRIVILEGED` / `TRADE_SECRET` / `SECURITY_SENSITIVE` / `THIRD_PARTY_RESTRICTED`

## Statement

The claim itself, in one determinate sentence where possible. A statement that cannot be contradicted is not a claim.

## Epistemic Type

`SOURCE` / `EVIDENCE` / `FACT_CLAIM` / `ASSUMPTION` / `CALCULATION` / `INFERENCE` / `AI_SUGGESTION` / `UNKNOWN` — with, for `ASSUMPTION`, what evidence would be needed to replace it, and for `UNKNOWN`, the determinate question that is unanswered.

## Governance State

`DRAFT` / `REVIEWED` / `APPROVED` / `CANONICAL` / `SUPERSEDED` / `RETRACTED` / `REJECTED`, with what act put it here.

## Conflict Flags

Each `CONFLICT_DETECTED` flag: its class, the items in tension, and whether it is material to this claim. **None** where there are none.

## Provenance

The chain to the depth the criticality band requires, per `knowledge/conflict-and-provenance-model.md`:
- source(s) and version(s);
- located evidence;
- derivation, calculation or reasoning, with inputs bound **by version**;
- transformations applied — unit, currency, basis, aggregation, rounding;
- human edit lineage;
- **AI contribution, and which governed human act moved it out of `AI_SUGGESTION`**;
- **every omitted step, with the reason it is omitted.**

## Review

Which Phase 6 Review Profiles apply, their statuses, and their findings. Review satisfaction is recorded, never asserted by this record.

## Decision References

Any Phase 7 `decision.<id>` exercised in respect of this item, with the outcome. **None** where none was.

## Applicability and Conditions

Where and when this holds: scope, period, conditions, and what falls outside it. A claim with no stated conditions is claiming to hold unconditionally, which is usually a defect rather than a strong position.

## Uncertainty and Limitations

What is not established, the range where there is one, what the claim is sensitive to, and what would change it.

## Freshness

Freshness expectation; current freshness; review-by; expiry; refresh triggers — including **every bound input whose supersession makes this stale**.

## Lineage of Status

Supersedes / superseded-by; prior versions; the reason for each change. Never edited; always appended.

## Scope Transfer History

Where this came from, if it came from another scope: source scope and version, **what was revalidated and what was not**, and what could invalidate it here. **None** for records originating in this scope.

## Governance Owner Class

The class of owner accountable for this record — never a named person.

## Audit History

Every state transition, who or what performed it (runtime identity), and on what basis. Append-only.

## Non-Runtime Statement

This record is declarative. It specifies no schema, storage, index, embedding, retrieval, API, interface, access control or runtime, and binds no person, organisation, provider or model identity.
