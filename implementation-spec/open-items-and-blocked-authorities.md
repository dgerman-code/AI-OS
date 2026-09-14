# Open Items and Blocked Authorities

Status: `PROPOSED` — Phase 14 implementation specification
Version: 0.1
Authority: approved Phase 1–13 architecture. Where this document and the approved architecture
differ, the architecture wins and this document is defective.

This document exists so that nothing in this package is quietly resolved. Every item below is
either an authority AI-OS does not have, a choice a human must make, or a known deferral carried
forward from an approval record. **None of them is filled in by Phase 14.**

## 1. Blocked authorities — `UNIMPLEMENTABLE UNTIL RIGHT IS MAPPED`

For each: the operation is **specified**, its enforcement hook is **built**, and every call
**refuses** with `NO_APPLICABLE_DECISION_RIGHT`. Phase 14 creates no Right, names no placeholder,
and provides no bypass.

### BA-1 — Canonical knowledge promotion and status change

| | |
|---|---|
| **Operations blocked** | `PromoteToCanonical`; any governance-state transition into `CANONICAL`; `ApplyConsequentStatusChange` where the consequent change is a canonical one; canonical rollback (which re-promotes). **`ResolveConflict` itself is not blocked** — it is an eligible Role's reviewed conclusion, not an exercise of authority (`knowledge-and-canonical-model.md` Rule K-13a) |
| **Candidate identifiers** | `decision.canonical_knowledge_promotion`, `decision.canonical_knowledge_status_change` — both recorded in `decisions/master-decision-right-universe.md`, both **uncarded**, and deliberately not merged pending the phase that owns the subject |
| **Why not carded** | Phase 7 recorded that distinguishing them requires the canonical state model itself, which Phase 8 owns; carding or merging either would presuppose the answer |
| **Where the semantics live** | `knowledge/canonical-promotion-governance.md` §7 defines the semantics **and specifies the Phase 7 pass that must card the Right** |
| **Enforcement hook** | `knowledge-and-canonical-model.md` §7.1 precondition 9; `canonical_record.promotion_decision_record` is `NOT NULL` |
| **Resolution path** | A Phase 7 governed change carding one or both Rights, with bounded subject, declared effects, holder eligibility, cardinality and separation relationships |
| **Consequence while blocked** | AI-OS records knowledge on four axes, reviews it, and approves it for bounded purposes. It holds **no canonical positions**. Every "what is the organisation's position" query answers *no position* |

### BA-2 — Scope re-parenting and cross-scope authority where not already mapped

| | |
|---|---|
| **Operations blocked** | `ReparentScopeNode`; any scope crossing whose mechanism is not registered for the exact act and Decision Right |
| **Status** | A crossing **is** implementable where an approved mechanism, registered for the exact Right and act, and a corroborated Decision Record exist. What is blocked is (a) re-parenting, which changes applicability for a whole subtree, and (b) any crossing where the mechanism registry has no matching registration |
| **Enforcement hook** | `scope-and-context-model.md` §3.3 and §7.1 element 9 |
| **Resolution path** | Phase 7 carding for re-parenting; mechanism registration through the Phase 6/Phase 8 mechanism path for crossings |

### BA-3 — Controlled destruction of governed content

| | |
|---|---|
| **Operations blocked** | `DestroyGovernedContent`; physical purge of a superseded payload; deletion of any governed record; hard deletion of artifact bytes outside retention-class expiry |
| **Why** | `orchestration/exemplars/missing-decision-right-blocks.md` establishes this exactly: of the eight carded Rights, **none covers the destruction of governed content**, and the nearest candidates are instructive rather than usable — risk acceptance authorises no act, and exceptional progression's subject is a governed work item, not a dataset |
| **Enforcement hook** | `persistence-and-transaction-model.md` §10, act 5 |
| **Resolution path** | A Phase 7 pass carding a Right whose **declared subject covers destruction of governed content** |
| **Consequence while blocked** | Content expires under its retention class or persists. Nothing is destroyed by an act. **Nothing is lost by blocking: the cost of stopping is a delay, and the cost of guessing is unrecoverable** |

### BA-4 — Destructive production database migration

| | |
|---|---|
| **Operations blocked** | `ApplyDestructiveMigration`; any migration the classifier derives as `DESTRUCTIVE` |
| **Candidate identifier** | `decision.production_database_migration` — recorded, **uncarded** |
| **Enforcement hook** | `migrations-versioning-compatibility.md` §3, four closures including a classifier whose disagreement with the declared class fails the build |
| **Resolution path** | A Phase 7 pass carding the Right |
| **Consequence while blocked** | Expand and migrate proceed; **contract against governed data does not**. Schemas accumulate deprecated structures until the Right exists. This is a real, accepted cost |

**Rule B-1 — none of the four is approximated.** No workaround, no equivalent operation under a
different name, no "administrative" path, no manual database intervention presented as
operations. A blocked act stays blocked, visibly, and the block is the system working.

## 2. Open items requiring a human architectural decision

These are choices Phase 14 **cannot** make, because making them would be creating governance no
approved phase authorised. Each names what must be decided and by whom.

Each is classified as an **implementation precondition** — something an implementation cannot
proceed without — or a **production/organisational engineering deferral**, which an
implementation can be built without and an operator must settle before use.

| # | Item | Class | Decision needed | Owner |
|---:|---|---|---|---|
| **OI-1** | production/organisational | Retention periods per retention class | Concrete durations, per class and per sensitivity label, including `PERSONAL_DATA` obligations | The organisation, under legal/compliance review |
| **OI-2** | implementation precondition | `max_iterations` default guidance | Whether a repository-wide guidance range exists, or every Workflow Definition sets its own with no guidance. Phase 14 requires the value to be **declared**; it declines to invent a number | Workflow governance (Phase 5 path) |
| **OI-3** | implementation precondition | Criticality-band thresholds for freshness blocking | Which bands treat `STALE_BUT_USABLE` as blocking beyond the Enhanced Decision-Grade rule already approved | Phase 3/Phase 8 path |
| **OI-4** | implementation precondition | "Delivery line" definition for `INDEPENDENT_ASSURANCE_REVIEW` | AI-OS does not own organisation charts. Condition 3 of Rule A-4 is **declared and evidenced** on the review request; the organisation must define what it declares | The organisation |
| **OI-5** | production/organisational | Organisation-specific incompatible-duty rules | Expressed as additional `DECISION_RIGHT_SEPARATION` rows through the Phase 7 change path, never as runtime configuration | The organisation, via Phase 7 |
| **OI-6** | implementation precondition | Holder eligibility → real people | Phase 7 binds no person, organisation, job title or system. Mapping eligibility classes to `HumanAuthorityRef`s is an organisational act, governed separately | The organisation |
| **OI-7** | production/organisational | Identity provider and human-identity source of record | Which system is authoritative for `HumanAuthorityRef`, and how a person's identity survives account changes (Rule X-2) | The organisation |
| **OI-8** | implementation precondition | Residency constraint vocabulary | The concrete residency values (jurisdictions, regions) the organisation uses. Phase 14 treats residency as an opaque comparable constraint | The organisation, under legal review |
| **OI-9** | production/organisational | PostgreSQL hosting choice | Supabase or plain PostgreSQL. Phase 14 requires only that no invariant depend on a capability unique to a hosted product (Rule P-23) | Engineering, recorded |
| **OI-10** | production/organisational | Reconciliation sweep thresholds | How long `ATTEMPTED_OUTCOME_UNKNOWN` and `WAITING` persist before escalation. Phase 14 requires escalation, not a number | Operations, recorded as policy |
| **OI-11** | production/organisational | Whether execution events are retained permanently or by policy | Phase 11 says "retained by policy". The policy is not set | The organisation |

### 2.1 A correction: OI-12 was false and has been removed

An earlier revision of this document recorded `OI-12`, claiming that
`reviews/phase-4-final-approval.md` carried no baseline SHA and that Phase 4's artifacts could
therefore not be verified against their approval.

**That was wrong.** The Phase 4 approval record states, at its line 7:

```
Approved Baseline Commit: `8ddacb2b2d2bc47e1a65099df575a0b16205d046`
```

The commit exists, is an ancestor of this branch, and Phase 4's artifacts (`skills/`,
`architecture/skill-registry-design.md`, `architecture/role-to-skill-mapping-rules.md`) are
byte-identical to it. The error originated in the Phase 13 review, which searched the record for
the word "baseline" and matched a later prose line instead of the labelled field. It was then
carried into the Phase 13 approval record's deferred list and into this document.

`OI-12` is therefore **removed, not resolved**: there was never an open question. The Phase 13
approval record is an approved artifact and is **not edited**; this correction is recorded here,
and the validator now reads the Phase 4 approval record and verifies the cited SHA rather than
trusting either document's prose.

## 3. Deferred items carried forward from approval records

Not resolved here, and **not rewritten as resolved**.

| # | Item | Status |
|---:|---|---|
| **DF-1** | Phase 11 validator-language hardening | Deferred exactly as recorded in the Phase 11 human approval. Its final audit remains `FAIL / NOT READY`; harness credibility remains `MEDIUM` |
| **DF-2** | Phase 11 validator `159/160` | Inherited approval-record wording condition. **Not repaired from Phase 14** |
| **DF-3** | Phase 10 validator `145/147` | Inherited approval-record status conditions. **Not repaired from Phase 14** |
| **DF-4** | Phase 12 harness credibility `MEDIUM-HIGH` | Not elevated by this specification |
| **DF-5** | Stale Phase 12 self-check prose ("65 tests" where the suite executes 157) | Documentation-cleanup item, accepted as non-blocking by the Phase 12 approval |
| **DF-6** | `decision.cancellation_or_termination` | `NOT CARDABLE UNTIL BOUNDED` — probably to be split into a governed-path cancellation Right and an external-commitment termination Right. No final ID is created, and none by implication |
| **DF-7** | Artifact `Status:` headers vs the approval registry | The eight approved Decision Right Cards carry `Status: PROPOSED` while the Phase 7 record approves them. Surfaced as a reconciliation report; **not fixed by editing either side** (Rule AP-8) |

## 4. Known limits of this specification

Stated plainly, because an unqualified claim would be false:

| # | Limit |
|---:|---|
| 1 | **Nothing here is built or tested.** It is a specification; its claims are about what an implementation must do, not about what any implementation does |
| 2 | **A database owner can write rows.** This specification claims detectability and attribution, not prevention (Rule X-18) |
| 3 | **Exactly-once is not claimed anywhere**, and no governed behaviour depends on it |
| 4 | **Atomicity does not span external systems.** Staged commit, outbox and reconciliation are specified precisely because it does not |
| 5 | **AI-OS holds no canonical positions** while BA-1 stands, and destroys nothing while BA-3 stands |
| 6 | **Independence condition 3** depends on an organisational fact AI-OS does not own (OI-4) |
| 7 | **This specification has not been audited.** It is `PROPOSED` |

## 5. What this document is not

It is not a backlog, not a roadmap, and not a list of things someone intends to do. Sections 1
and 3 are **governed positions**: acts that must fail closed until a human governance change
opens them. Section 2 is a list of questions whose answers belong to people, not to this
document.
