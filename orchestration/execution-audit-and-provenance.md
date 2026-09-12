# Execution Audit and Provenance

Status: PROPOSED — Phase 11 architecture candidate
Version: 0.1
Inherits: `standard.orchestration.common_constraints@0.1`

## 1. Eight histories, and none substitutes for another

| History | Answers | Retention | May it stand in for another? |
|---|---|---|---|
| **Operational runtime event** | What a process did mechanically | Rotated, sampled, discarded | **No.** Never governance evidence |
| **Execution event** | What the orchestrator did and why, at which position in which run | Retained by policy, append-only | **No.** It records coordination, not conclusions |
| **Audit event** (Phase 10) | Who or what changed which governed record, from what to what | Retained, never deleted | **No.** It records the change, not the authority |
| **Decision Record** (Phase 7) | That an eligible human exercised a named Right | Permanent, append-only | **No.** It is the authority |
| **Review result** (Phase 6) | Whether a review was satisfied, by whom, under which independence class | Permanent, append-only | **No** |
| **Routing Decision** (Phase 9) | Which execution capability was eligible and selected, reproducibly | Permanent, append-only | **No** |
| **Knowledge provenance** (Phase 8) | Where content came from and what supports it | Permanent with supersession | **No.** Provenance is about content |
| **Git architecture history** | How the definitions themselves changed | Permanent, not rewritten | **No** |

**An execution event is not an audit event.** The execution event says "stage 3 dispatched at this position, because dependency 2 was satisfied by review instance X". The audit event says "record R moved from version 4 to version 5, by identity I, under authority D". Both exist for one governed write, and neither reconstructs the other.

## 2. The execution event — 13 fields

| # | Field | Content |
|---:|---|---|
| 1 | **Event ID** | Stable, unique, never reused |
| 2 | **Run reference** | `run.<id>`, and the stage or activity instance |
| 3 | **Event class** | Created · validated · dispatched · requested · state transition · gate outcome recorded · retry · checkpoint · intervention · reconciliation · terminal |
| 4 | **State before / after** | The four axes, both sides |
| 5 | **Reason** | The dependency, outcome or policy rule that caused it, in governed vocabulary |
| 6 | **Governed references** | Review Instance, Decision Record, Routing Decision, handoff, artifact — each **ID and version, as recorded values** |
| 7 | **Definition bindings** | `workflow.<id>` @ version, `orch_policy.<id>` @ version in force for this event |
| 8 | **Scope and sensitivity** | The run's scope; the label set in force |
| 9 | **Identities** | The **human identity reference** where a human caused it, and, separately, the **system identity** that executed it — two fields, always |
| 10 | **Authority reference** | The Decision Record where the event class requires one. **Absent is a failure for those classes** |
| 11 | **Timestamps** | Event time; effective time where they differ |
| 12 | **Correlation and causation** | Which operation this belongs to, and which event caused it |
| 13 | **Retry / iteration ordinal** | Which attempt, which rework iteration |

## 3. Append-only

The execution event stream has **no update and no delete operation to grant** — the Phase 10 `audit` domain rule, applied here. A correction is an appended event naming the one it corrects.

Where the backend can enforce append-only structurally, it must. Where it can only enforce it by permission, **the limitation is recorded rather than assumed away.**

## 4. Reconstructing a historical execution

A completed run must answer, years later: which workflow version ran, under which orchestrator policy, in which scope, with which labels, using which model through which Routing Decision, reviewed under which Profile by whom, authorised by which Decision Record.

It answers because **every one of those is a recorded value in the event stream**, not a pointer resolved at read time. Joining to current state is enrichment for display; the record is the recorded values, and a display that substitutes current values for recorded ones is a defect (`storage/versioning-and-lineage.md` §7, unchanged).

## 5. Relationship to Phase 10

Execution records are **operational governance records** in Phase 10's terms: `DB`-authoritative, append-only, not replicated, with conflicts resolving `APPEND_ONLY_NO_CONFLICT`. They sit alongside the `runtime_meta` boundary rather than inside it — correlation metadata is bounded and citable by nothing, whereas an execution event is a record of coordination that governed records may legitimately reference.

**Nothing in Phase 11 relocates a governed object.** Reviews stay in `review`, decisions in `decision`, knowledge in `knowledge`, routing in `routing`, artifacts in `artifact`. The orchestrator references them; it does not hold them.
