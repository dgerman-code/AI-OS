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
- Memory class: `WORKING_MEMORY` / `EPISODIC_MEMORY` / `SEMANTIC_MEMORY` / `PREFERENCE_MEMORY` / `PROCEDURAL_MEMORY` / `AUDIT_MEMORY` — **full names only**; the class does not change when the governance state does
- Origin: `HUMAN_ORIGIN` / `AI_ASSISTED` / `AI_GENERATED` / `EXTERNAL_ORIGIN` — **permanent; nothing changes it**
- Sensitivity classification: one or more of `PUBLIC` / `INTERNAL` / `CONFIDENTIAL` / `RESTRICTED` / `PERSONAL_DATA` / `PRIVILEGED` / `TRADE_SECRET` / `SECURITY_SENSITIVE` / `THIRD_PARTY_RESTRICTED`

## Statement

The claim itself, in one determinate sentence where possible. A statement that cannot be contradicted is not a claim.

## Epistemic Type

`SOURCE` / `EVIDENCE` / `FACT_CLAIM` / `ASSUMPTION` / `CALCULATION` / `INFERENCE` / `AI_SUGGESTION` / `UNKNOWN` — with, for `ASSUMPTION`, what evidence would be needed to replace it, and for `UNKNOWN`, the determinate question that is unanswered.

**The type never changes.** A different type is a **different, linked item** with its own evidential basis. Where this item was adopted from an `AI_SUGGESTION`, record the link — and note that human acceptance is not the basis; the evidence or reasoning stated below is.

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
- **origin, permanently** — and where this item was adopted from a proposal, the link to that `AI_SUGGESTION` and the evidence or reasoning that justified **this** item's type;
- **every omitted step, with the reason it is omitted.**

## Review

Which Phase 6 Review Profiles apply, their statuses, and their findings. Review satisfaction is recorded, never asserted by this record.

## Decision References

Any Phase 7 `decision.<id>` exercised in respect of this item, with the outcome. **None** where none was.

## Applicability and Conditions

Where and when this holds: scope, period, conditions, and what falls outside it. A claim with no stated conditions is claiming to hold unconditionally, which is usually a defect rather than a strong position.

## Uncertainty and Limitations

What is not established, the range where there is one, what the claim is sensitive to, and what would change it.

## Temporal Facts

**Item-level facts only. No use verdict is stored here.**

- As-of date — the date the knowledge is about;
- Last verified / refreshed;
- Expected refresh interval;
- Review-by;
- Expiry, where applicable;
- Supersession / withdrawal state;
- Refresh triggers — including **every bound input whose supersession fires one**;
- Derived condition: `PAST_REFRESH_INTERVAL`, where the interval or review-by has passed. An age condition, not a usability judgement.

**Usability is assessed per use**, at the moment of use — `CURRENT_FOR_USE`, `STALE_BUT_USABLE`, `STALE_AND_BLOCKING`, `EXPIRED_FOR_USE` — against these facts and the task's criticality band. The same item may carry different verdicts for different tasks at the same moment, and **no verdict is written back here as a record-level label**.

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
