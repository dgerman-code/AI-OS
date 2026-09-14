# Audit, Provenance and Observability

Status: `PROPOSED` — Phase 14 implementation specification
Version: 0.1
Authority: approved Phase 1–13 architecture. Where this document and the approved architecture
differ, the architecture wins and this document is defective.

Closes Phase 13 finding **M-2**.

## 1. Eight histories, and none substitutes for another

| History | Answers | Retention | Stands in for another? |
|---|---|---|---|
| **Operational runtime event** | What a process did mechanically | Rotated, sampled, discarded | **No. Never governance evidence** |
| **Execution event** | What the orchestrator did and why, at which position in which run | Retained by policy, append-only | **No.** It records coordination, not conclusions |
| **Audit event** | Who or what changed which governed record, from what to what | Retained, never deleted | **No.** It records the change, not the authority |
| **Decision Record** | That an eligible human exercised a named Right | Permanent, append-only | **No. It is the authority** |
| **Review result** | Whether a review was satisfied, by whom, under which independence class | Permanent, append-only | **No** |
| **Routing Decision** | Which execution capability was eligible and selected, reproducibly | Permanent, append-only | **No** |
| **Knowledge provenance** | Where content came from and what supports it | Permanent with supersession | **No.** Provenance is about content |
| **Git architecture history** | How the definitions themselves changed | Permanent, not rewritten | **No** |

> **An execution event is not an audit event.** The execution event says "stage 3 dispatched at
> this position, because dependency 2 was satisfied by review instance X". The audit event says
> "record R moved from version 4 to version 5, by identity I, under authority D". Both exist for
> one governed write, and **neither reconstructs the other**.

## 2. The rule this document exists to enforce

**Rule V-1.** No operational log, metric, trace, span, runtime event or execution event may
satisfy a **review**, a **decision**, a **canonicalisation**, a **publication**, a
**risk-acceptance**, or any other governance gate — and none may serve as evidence in any of
them.

**Rule V-2 — enforced by construction, not by discipline.** The execution event store and the
observability plane are **written to and never read from** on any governed path. The
implementation makes this structural:

1. governed components hold a **write-only** handle to the execution event writer — the
   interface has an `append` operation and **no read operation at all**;
2. the observability plane (C13) is in a separate store with no foreign key from any governance
   table and no read grant for any governance service role;
3. the gate evidence contract admits four typed evidence classes and none of them is an event
   (`orchestrator-runtime-contract.md` §6.1);
4. a static check in CI fails the build on any read of the execution event or observability
   store from a governed module (`test-and-assurance-strategy.md` §8).

The Phase 12 reference implementation satisfied (1) behaviourally — all 19 uses of its log were
appends — but its docstring called the event "governance evidence", which it is not. That is
corrected here and
the property is made structural.

## 3. The execution event — 13 fields

Written by C9. **Coordination history. Not governance evidence.**

| # | Field | Type | Null | Content |
|---:|---|---|---|---|
| 1 | `execution_event_ref` | ref | NO | Stable, unique, **never reused** |
| 2 | `run_ref` + `stage_or_activity_instance_ref` | refs | NO / YES | The run, and the stage or activity instance |
| 3 | `event_class` | enum | NO | `CREATED` · `VALIDATED` · `DISPATCHED` · `REQUESTED` · `STATE_TRANSITION` · `GATE_OUTCOME_RECORDED` · `RETRY` · `CHECKPOINT` · `INTERVENTION` · `RECONCILIATION` · `TERMINAL` |
| 4 | `state_before` / `state_after` | structured | NO | **The four axes, both sides** |
| 5 | `reason` | text | NO | The dependency, outcome or policy rule that caused it, **in governed vocabulary** |
| 6 | `governed_references` | list of ref+version | YES | Review Instance, Decision Record, Routing Decision, handoff, artifact — each **ID and version, as recorded values** |
| 7 | `definition_bindings` | structured | NO | `workflow.<id>` @ version and `orch_policy.<id>` @ version **in force for this event** |
| 8 | `scope_and_sensitivity` | structured | NO | The run's scope path; the label set in force |
| 9 | `human_identity_ref` / `system_identity_ref` | refs | YES / NO | The human where a human caused it, and — **separately, always** — the system identity that executed it. **Two fields, never merged** |
| 10 | `authority_reference` | `DecisionRecordRef` | Conditional | Required for `GATE_OUTCOME_RECORDED` on a decision gate, for `TERMINAL` where a Right was exercised, and for `INTERVENTION` where the act required one. **Absent is a failure for those classes** |
| 11 | `event_time` / `effective_time` | timestamptz | NO / YES | Where they differ |
| 12 | `correlation_id` / `causation_id` | ids | NO / YES | Which operation this belongs to; which event caused it |
| 13 | `retry_ordinal` / `rework_iteration_ordinal` | ints | YES | Which attempt; which rework iteration |

Constraints: `UNIQUE (execution_event_ref)`; no `UPDATE`, no `DELETE`; a check enforcing field 10
for the classes that require it; field 9's two columns are separate and neither defaults from the
other.

**Rule V-3 — field 9 is two fields.** A single `actor` column is prohibited. Merging the human
and the system identity is how "the system did it on behalf of someone" becomes indistinguishable
from "someone did it".

**Rule V-3a — an absent human identity is a fact, not a gap to fill.** Where an act had no human
— a constraint-driven `TERMINATED`, an automatic retry within its class, a reconciliation
determination — `human_identity_ref` is `NULL` and the system identity carries the provenance.
Defaulting the field from the authenticated principal, the run's creator, or the last human to
touch the run **fabricates human provenance for a machine act** and is prohibited. The
asymmetry between `CANCELLED` (a human act, with an intervention) and `TERMINATED` (the system
stopping work that would breach a constraint) is visible in this field and must stay visible.

**Rule V-4 — field 10 is not authority.** It *references* the Decision Record that authorised the
act. The event is not the authority and citing it as one is Rule V-1's violation in a new place.

## 4. The audit event — 11 fields

Written by C12, for every governed record write.

| # | Field | Null | Content |
|---:|---|---|---|
| 1 | `audit_event_ref` | NO | Stable, unique, never reused |
| 2 | `governed_record_ref` | NO | Which record this event is about — **exactly one** |
| 2a | `record_version_before` | **Conditional on `mutation_kind` — §4.1** | The version the record held before this mutation |
| 2b | `record_version_after` | **Conditional on `mutation_kind` — §4.1** | The version it holds after |
| 3 | `mutation_kind` | NO | The enum of §4.1. It is what makes 2a's nullability checkable |
| 4 | `changed_fields` | NO | Field-level, before/after for governed fields. On `INSERT` the before side is empty, consistently with 2a |
| 5 | `human_identity_ref` | YES | Where a human caused it. **`NULL` for a system act, never synthesised** — a constraint-driven `TERMINATED` has no human and says so |
| 6 | `system_identity_ref` | NO | The service identity that executed the write |
| 7 | `authority_reference` | Conditional | The Decision Record where the change class requires one |
| 8 | `scope_path` | NO | |
| 9 | `occurred_at` | NO | |
| 10 | `correlation_id` / `causation_id` | NO / YES | |
| 11 | `retention_class` + `legal_hold_flag` | NO | Retained by policy, **never deleted** |

### 4.1 `mutation_kind`, and the version-nullability matrix

An earlier revision required both `record_version_before` and `record_version_after` to be
non-null. An insert has no prior version, so that contract could not be satisfied by the most
common mutation there is. The contract is stated once, as an enum plus a matrix, and the enum is
what makes the nullability rule checkable rather than a convention.

| `mutation_kind` | Means | `record_version_before` | `record_version_after` |
|---|---|---|---|
| `INSERT` | A governed record exists that did not exist | **NULL** — required to be null; there is no prior version, and a value would be a fiction | **NOT NULL** |
| `VERSION_APPEND` | A new version row of an existing governed record | **NOT NULL** | **NOT NULL** |
| `UPDATE` | A `MUT` column changed on an existing record | **NOT NULL** | **NOT NULL** |
| `LINK_APPEND` | An append-only lineage link added | **NOT NULL** | **NOT NULL** |
| `LIFECYCLE_STATE_CHANGE` | A lifecycle or governance state moved | **NOT NULL** | **NOT NULL** |
| `SUPERSEDE` | A record was superseded by a named successor | **NOT NULL** | **NOT NULL** |
| `POINTER_MOVE` | A current-pointer row was created or re-pointed | **NULL on creation, NOT NULL on a move** | **NOT NULL** |
| `DESTROY` | A governed record was destroyed | **NOT NULL** | **NULL** — there is no after |

**Rule V-5-matrix — the matrix in this section is the only statement of nullability.** The field
table above states *conditional on `mutation_kind`* and nothing more; an earlier revision said
`record_version_after` was mandatory for every successful write, which contradicts `DESTROY`.
Where the field table and this matrix could be read as disagreeing, this matrix governs — and
the field table no longer says anything a reader could take as a second rule.

**Rule V-5a — the matrix is a constraint, not guidance.** It is expressed as a check constraint
keyed on `mutation_kind`, so a row that claims `INSERT` and carries a before-version is rejected
by the database, as is a `VERSION_APPEND` that carries none.

**Rule V-5b — `DESTROY` is defined and unreachable.** Its row exists so that the pair is
specified *now*, before anyone needs it under pressure. **BA-3 remains blocked**: no command
produces a `DESTROY` audit event, `destroy_governed_content` writes zero governed records and
zero audit events, and defining the shape enables nothing. A specification that left the pair
undefined would be inviting whoever unblocks BA-3 later to invent it.

**Rule V-5c — `POINTER_MOVE` is the approval-state case.** Creating the first
`approval_state_current` row for a subject version is a creation and has no before; every later
re-point has one. Both are `POINTER_MOVE`, and the nullability follows the act rather than a
second enum value.

**Rule V-5d — no audit event exists for a refused transaction**, of any kind, at any
`mutation_kind`. See Rule V-6c.

**Rule V-5.** An audit event records **the change, not the authority for it**. Where authority
was required, field 7 points at the Decision Record; the audit event never becomes the reason.

**Rule V-6 — one audit event per persisted governed-record mutation**, in the **same
transaction** as that mutation, linked to that exact record. This is
`persistence-and-transaction-model.md` Rule P-14a, stated from the audit side; the two documents
say the same thing and §7.2 of that document enumerates the exact rows each governed act
produces.

The unit is the **record mutation**, not the governed act. An act that mutates four governed
records writes four audit events. They share one `correlation_id`, and each carries the
`causation_id` of the execution event that coordinated it — which is how they are gathered back
into one act without any of them describing more than one record.

**Rule V-6a — no grouping, ever.** Multiple governed-record changes are never written behind one
audit event. Phase 10 authorises no such grouping, and a grouped row cannot answer *which record
moved from which version to which* — the only question this record exists to answer.

**Rule V-6b — an audit event without its record, or a record without its audit event**, is a
detectable inconsistency and is reported by the reconciliation sweep.

**Rule V-6c — a refusal mutates nothing and therefore writes no audit event.** It writes one
execution event. The blocked hooks of `open-items-and-blocked-authorities.md` §1 are the standing
case: they refuse every call, and their history is entirely execution events.

## 5. Provenance record

Provenance is **about content**: where it came from and what supports it.

| Field | Null | Content |
|---|---|---|
| `provenance_ref` | NO | |
| `subject_ref` + `subject_version` | NO | The knowledge item, artifact or canonical record version |
| `origin` | NO | The Phase 8 origin value, permanent |
| `derived_from` | YES | Source and evidence refs at their versions |
| `producing_act` | YES | Model Invocation, human work record, or external receipt |
| `chain_complete` | NO | `COMPLETE` · `GAP_STATED` · `GAP_JUSTIFIED_PER_STEP` |
| `transfer_lineage` | YES | Where the item arrived by scope transfer; **lineage begins at the original source, not at the transfer** |

**Rule V-7.** Provenance survives transfer intact and is never truncated to the transfer event.
At Enhanced Decision-Grade the chain must be `COMPLETE` **or** each omission explicitly justified
per step.

## 6. Correlation and causation

| Id | Scope | Governance meaning |
|---|---|---|
| `correlation_id` | One logical operation, across components and events | **None** |
| `causation_id` | The immediately preceding event that caused this one | **None** |
| `decision_chain_id` | A chain of related governed decisions | **Used by SoD** (`decision-review-authority-model.md` §6.3) |

**Rule V-8.** `correlation_id` and `causation_id` are operational. They may be indexed, traced,
sampled and discarded. **No governed record may cite either as a reason**, and no gate reads
them. `decision_chain_id` is different in kind: it is a governed field on governed records,
propagated explicitly, and it is the only one of the three with governance meaning.

## 7. Observability plane

| Signal | Store | May be read by governance? |
|---|---|---|
| Structured application logs | Observability store | **No** |
| Metrics and counters | Observability store | **No** |
| Distributed traces / spans | Observability store | **No** |
| Health and readiness signals | Observability store | **No** |
| Alert state | Observability store | **No** |

**Rule V-9 — observability is never authority.** An alert is not an escalation. A metric
threshold is not a gate outcome. A trace is not provenance. A dashboard is not a Decision Record.
A green health check is not approval, and an outage is not an emergency authority.

**Rule V-10 — no secrets, no governed content.** Event payloads and log lines carry references,
never governed content and never secret material. `RUNTIME EVENT != SECRET`: event payloads that
carry content become an exfiltration surface by default.

**Rule V-11 — what observability is for.** Detecting that the system is not working, and
supporting reconciliation sweeps. Both are operational purposes with no governance meaning, and
that is the whole of its remit.

## 8. What must be observable without being authoritative

The following are **required operational signals**, precisely because they detect the failure
modes this architecture cares about — and none of them decides anything:

| Signal | Detects |
|---|---|
| Governed record without its audit event, and the reverse | A broken write path (V-6) |
| Orphaned object count and age | An interrupted staged commit (§8 of the persistence model) |
| Outbox rows in `ATTEMPTED_OUTCOME_UNKNOWN` | External-effect uncertainty needing reconciliation |
| Runs in `BLOCKED` / `ESCALATED` by posture and age | Governance gaps waiting on humans |
| Rework loops at `max_iterations - 1` | Loops about to be declared non-converging |
| `STALE_WRITE` rate by table | Contention, and possibly a design defect |
| `DUPLICATE_GOVERNED_IDENTITY` occurrences | A replay that the constraint correctly refused |
| Append-only grant verification result | Whether P-5's enforcement still holds |

## 9. Divergences from the Phase 12 reference implementation

| # | Phase 12 reference | This specification | Why |
|---:|---|---|---|
| D1 | `ExecutionEvent` docstring: "Governance evidence, distinct from an operational log" | Execution events are **coordination history and never governance evidence** | Phase 11 §1; Phase 13 M-2. The reference's behaviour was already correct — all log uses were appends — but its wording was not |
| D2 | 5 fields | The 13-field contract, with separate human and system identities and a conditional authority reference | Phase 11 `execution-audit-and-provenance.md` §2 |
| D3 | No audit event, no provenance record | §4, §5 | Phase 10 `audit-provenance-model.md` |
| D4 | No observability plane | §7, structurally unreadable from governance | Phase 13 M-2 |
