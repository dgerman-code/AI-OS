# Phase 11 — Orchestrator Foundation Self-Check

Status: PROPOSED — READY FOR INDEPENDENT PHASE 11 FOUNDATION AUDIT

Branch: `architecture/phase-11-orchestrator`
Start baseline: Phase 10 human-approval record `eb789263b4dcc7c4a966a19359522173c57ac8ec`
Approved Phase 10 architecture baseline: `b184b074c1de5416fcfc56036ee033f6e52fed46`

**This is not an independent review.** Under Phase 6's vocabulary it is `PRODUCER_REVIEW` — internal quality control by the pass that produced the work, which cannot satisfy an independent review requirement and does not claim to. It carries no results of its own; it points at the harness that produces them.

## Running the check

```
python3 validation/phase_11_validation.py
```

Python 3 standard library and `git` only. No network, no third-party packages, no writes. Deterministic; exit code 0 on pass, non-zero on any failure. `--verbose` prints each check's evidence; `--json` emits machine-readable results. Conventions are in `validation/README.md`.

**Current result: `=== 155/155 PASS ===`.** Normal, `--verbose` and `--json` modes all report the same total. The harness asserts that this document states the total and the group counts the suite actually emits, so a stale number here is a failure rather than a cosmetic slip.

**Scope boundary.** These 155 are **offline, deterministic checks over committed content**. Remote repository state and the configuration of any engine, queue, database or forge are **not provable offline and are not claimed**.

| Group | Checks | Covers |
|---|---:|---|
| `identity` | 7 | The 21-object chain verbatim; each named collapse denied **with its consequence**; the eight load-bearing denials individually; Role activated not instantiated; **no seniority variants**; runtime ID ≠ governance identity; router and orchestrator remain two components |
| `authority` | 10 | The may / may-never table populated on both sides; **a pattern scan proving no artifact grants the orchestrator a governed power**; completion ≠ approval; absence of a Right ≠ permission; timeout ≠ approval; `DEFER`/`ESCALATE` never become `APPROVE`; no self-satisfied gate; confidence ≠ authority; a model result is `AI_SUGGESTION`; a credential grants nothing |
| `state` | 10 | Four orthogonal axes rather than one enum; 10 phases, 6 terminals, 5 wait reasons, 4 postures, each parsed; **completion gated on posture, not on stages finishing**; **no waiting, paused or blocked state reaches completion**; terminals have no outgoing edges; a block is not resumed by retry; postures compose strictly |
| `scope` | 9 | Every boundary named; one scope per run, bound at intake; crossing needs an approved mechanism; a sub-run narrows and never widens; scope mismatch stops the run; **a scan reading every scope-crossing sentence by its predicate** — a prohibition is allowed however worded, a permission only when it names an approved mechanism and does not dispense with one — plus a twelve-case guard on that verdict function; sensitivity carried never widened; **no scalar sensitivity ceiling** |
| `scheduling` | 10 | 6 dispatch kinds classified; **human, review and decision dispatches are requested, never scheduled**; 8 dependency kinds with outcomes; a branch may not read a model's opinion; acyclic graph with a bounded rework loop; exhaustion escalates; sequencing belongs to the definition; **policy may not change what a stage means**; freshness at point of use; lapsed assignments invalidated |
| `assignment` | 6 | 12 envelope fields, all present; activation confers nothing new; executor eligibility declared never inferred; **review and decision exclusions recorded at assignment time**; task / work item / attempt stay three objects |
| `router` | 6 | Request and decision are two objects; no chosen model or relaxed constraint in the request; a routing block is a block; decisions recorded by value; **retry may not switch models to evade independence**; a model completes an activity, not a gate |
| `gates` | 8 | 7 outcomes parsed; **no non-satisfying outcome permits continuation**; four gate kinds apart; re-request needs a recorded change; a missing Right blocks with four refusals named; independence enforced mechanically; a waiting window governs escalation only; **the policy template forbids an auto-approve setting** |
| `retry` | 9 | 7 classes parsed; unclassified is non-retryable; **authority-bearing and external acts never blindly replayed**; every authority act class enumerated; **exactly-once denied wherever it appears**; at-most-once grounded in the governed record; replay walks the classes; retry never widens or unblocks; compensation ≠ rollback |
| `concurrency` | 12 | 5 outcomes as a fixed vocabulary; 10 races each resolving to one; every required case; late results recorded never applied; **a late Decision Record is neither discarded nor characterised as stale**, checked on the authoritative row, again phase-wide wherever a Decision Record is named, a third time by feeding the matcher its own cases, and a fourth requiring that **Markdown formatting exempt nothing** — the invariant reads **rendered** text through a structured standard-library path — an HTML parser for tags, comments and character references, a depth-counting scanner for link destinations, a quote-aware scan for unterminated openers, then inline code, `*`, `_`, `**`, `__` and `~~` — with visible content never removed, by a normaliser scoped to this invariant so the declared vocabulary survives, on both the Phase-11-wide path and the authoritative row's own reading path; only an explicit specimen fence, available to review records alone, claims an exemption; a human beats automated continuation; last-write-wins absent; limits delay but never skip; causation not timestamps |
| `failure` | 8 | 7 distinctions with the harm of collapsing each; every required pair; 12 stop conditions with outcomes; every required condition; **no distributed transaction claimed**; external uncertainty stops the run; no failure path weakens a constraint; a resume re-enters current constraints |
| `manual` | 6 | 6 acts, each stating whether a Right is required; human and system identity separate; **an operational exception touches no governed requirement**; no refusal becomes a continuation; history cannot be edited; seniority is not authority |
| `audit` | 9 | 8 histories apart; 13 execution-event fields; a log is never evidence; **a scan for any artifact treating a log as evidence**; append-only; an unenforceable immutability claim recorded as a gap; authority reference required where the class needs one; historical reconstruction by recorded value; **nothing governed relocated** |
| `independence` | 4 | 5 adapter boundaries; an adapter isolates a mechanism never a meaning; the replacement test stated so it can be applied; determinism bounded honestly |
| `intake` | 3 | 7 intake checks before anything is scheduled; unassessed sensitivity restricted; a failing trigger refused rather than started |
| `templates` | 4 | 3 templates, `PROPOSED`, inheriting the standard; contiguous numbering; the policy template's cannot-declare list |
| `exemplars` | 10 | 6 on disk, `PROPOSED` and synthetic; each states what it proves; the missing-Right exemplar blocks and names what did not happen; the cancellation exemplar keeps the late Decision Record; the independence exemplar blocks rather than relaxing a class |
| `regression` | 19 | Phases 3–10 unchanged against the Phase 10 approval baseline; the Phase 9 and Phase 10 approval records untouched; the three prior validators untouched; all `PROPOSED`; **no orchestrator, queue, engine, schema or client implemented**; **no secret-shaped string anywhere**; harness read-only and non-vacuous; no claim about remote PR state |
| `inventory` | 5 | Every count derived from a parsed source; the master inventory reconciled; prose counts reconciled; heading-versus-list cardinality; and that this document's total and group counts are the ones the suite emits |

## Adversarial probes

Twelve deliberate mutations, each reverted, each producing a non-zero exit. They are recorded here because a suite's value is what it rejects, not what it counts.

| # | Mutation | Exit | Passing | Check that caught it |
|---:|---|:--:|---:|---|
| 1 | The orchestrator given power to approve a stage directly | 1 | 149 | no artifact grants the orchestrator a governed power |
| 2 | A gate `EXPIRED` outcome made to continue | 1 | 148 | timeout is never an approval; no non-satisfying outcome continues |
| 3 | `WAITING` given a direct edge to `COMPLETED` | 1 | 149 | no waiting, paused or blocked state reaches completion |
| 4 | `COMPLETED` allowed without `GOVERNANCE_CLEAR` | 1 | 149 | completion requires a clear posture |
| 5 | `NO_APPLICABLE_DECISION_RIGHT` made to continue | 1 | 149 | no non-satisfying gate outcome permits continuation |
| 6 | `NON_RETRYABLE_GOVERNED_ACT` made automatically retryable | 1 | 149 | authority-bearing acts never blindly replayed |
| 7 | Exactly-once asserted across all systems | 1 | 149 | exactly-once is never asserted |
| 8 | A project-boundary crossing described without a mechanism | 1 | 149 | no scope crossing is implicit |
| 9 | An operational log described as evidence | 1 | 149 | no artifact turns a log into evidence |
| 10 | `ROLE` and `AGENT INSTANCE` collapsed in the chain | 1 | 149 | the 21-object separation chain |
| 11 | `ROUTER` and `ORCHESTRATOR` collapsed in the chain | 1 | 149 | the 21-object separation chain |
| 12 | A vacuous `or True` check added to the harness | 1 | 150 of 152 | the vacuity scan |

Every mutation was reverted. Note the second column of failures each time: **the self-check totals check also fires**, because a suite whose shape changed no longer matches what this document states — which is the guard working rather than noise.

## One finding about a prior harness, reported rather than fixed

Running `python3 validation/phase_10_validation.py` during this pass returns **145 of 147**, failing two checks on `reviews/phase-10-final-approval.md` — the human approval record, which is *supposed* to say `APPROVED` and is not a Phase 10 proposal. The Phase 10 harness discovers every `reviews/` file matching its phase and has no exemption for approval records; Phase 9's harness has one.

**This is pre-existing and was not caused by Phase 11.** Verified by checking out the Phase 10 human-approval commit `eb789263b4dcc7c4a966a19359522173c57ac8ec` in a separate worktree and running its own harness there: the same two failures, the same total.

**It was not fixed here.** `validation/phase_10_validation.py` is an approved upstream artifact under this phase's regression boundary, and repairing it is a Phase 10 remediation, not a Phase 11 foundation change. The Phase 11 harness carries the exemption from the start, with a comment recording why.

## What the harness does not prove

- **Nothing about a live system.** No orchestrator, queue, worker, scheduler, event bus, database, engine or credential was built, connected to or configured. The harness reads markdown.
- **Nothing about whether the architecture is right.** It checks that the documents agree with each other and with their own parsed tables. Internal consistency is not correctness.
- **Nothing an independent reviewer could not disagree with.** It is a `PRODUCER_REVIEW`.

## Open questions — all 14 classified

| # | Question | Disposition | The rule, or the reason for deferral |
|---:|---|---|---|
| 1 | Does the orchestrator ever hold authority? | **RESOLVED IN FOUNDATION** | **No, under any configuration.** It is the one component that sees everything at once, which is exactly why it is given authority over nothing — a coordinator that could approve would be the shortest path around every gate |
| 2 | May a run complete with unresolved items? | **RESOLVED IN FOUNDATION** | Only as `COMPLETED_WITH_OPEN_ITEMS`, posture `OPEN_ITEMS_CARRIED`, **each item naming the upstream rule that permits carrying it**. An item without one blocks |
| 3 | What happens when a gate expires? | **RESOLVED IN FOUNDATION** | `ESCALATED`, posture unchanged, gate still unsatisfied. There is no policy setting that makes expiry an approval, and the policy template forbids adding one |
| 4 | What happens when no Decision Right applies? | **RESOLVED IN FOUNDATION** | `NO_APPLICABLE_DECISION_RIGHT` → `BLOCKED` **and** `ESCALATED`, posture `AUTHORITY_ABSENT`. Carding a Right is a Phase 7 act; Phase 11 identifies the gap and cannot fill it |
| 5 | May retry replay an authority-bearing act? | **RESOLVED IN FOUNDATION** | Never. Class 4 is at-most-once **by governed record** — the append-only store with a uniqueness constraint is the mechanism, not the orchestrator's care |
| 6 | Is exactly-once provided? | **RESOLVED IN FOUNDATION** | **No, and it is not claimed.** Idempotent-at-least-once for replayable steps; at-most-once by governed record for authority-bearing acts; exactly-once nowhere |
| 7 | How are late results handled? | **RESOLVED IN FOUNDATION** | Recorded against their own request, applied nowhere — except a late **Decision Record**, which stands as a governed act and is reconciled and escalated rather than discarded |
| 8 | May the orchestrator choose a model? | **RESOLVED IN FOUNDATION** | No. It submits a request with the stage's declared constraints; Phase 9 decides. A retry re-submits the **same** request and never alters constraints or independence to make a different candidate eligible |
| 9 | May a scope be crossed? | **RESOLVED IN FOUNDATION** | Only through Phase 8 scope transfer or Phase 6 handoff. There is no orchestrator-level shortcut, and a sub-run may narrow but never widen |
| 10 | How is reviewer independence enforced? | **RESOLVED IN FOUNDATION** | Mechanically, at review request time, from the Assignment Envelope's recorded exclusions. Where no eligible reviewer exists the run **blocks** — there is no partial independence and criticality never lowers a requirement |
| 11 | What if an external side effect's outcome is unknown? | **RESOLVED IN FOUNDATION** | `BLOCKED` and `ESCALATED`. Never assumed in either direction, and recovery is **compensation** — a new, separately-authorised act — never a rollback |
| 12 | How long may a rework loop run? | **SAFE TO DEFER WITH EXPLICIT RULE** | The **rule** is fixed: a declared maximum, per loop, in the workflow definition, with `ESCALATED` on exhaustion. The **number** is an organisational choice and is deliberately not invented here |
| 13 | Which execution engine? | **IMPLEMENTATION DETAIL** | Genuinely one: five adapter boundaries fix what is portable, and the replacement test — would any governance semantic change if the engine were replaced? — makes the classification checkable rather than asserted |
| 14 | Observability, metrics and operational alerting | **PHASE 12+** | The execution event and its 13 fields are defined; what watches them, and how, is later work. **No operational signal becomes evidence in the meantime** |

**Nothing about authority, privacy, scope, replay, side effects, decisions or human control is filed under `IMPLEMENTATION DETAIL`.** Question 13 is the only such entry and concerns a mechanism behind a declared boundary.

## Where this foundation is most likely to be wrong

Recorded for the audit rather than left to be discovered. In Phase 10 the independent audit found three defects and **two of them were in the harness rather than the architecture** — which is the honest measure of how much weight to put on a passing suite, including this one.

1. **The four-axis state model is a judgement.** It is more correct than one enum and it is also more to get wrong: a posture and a phase can drift out of agreement, and the harness checks the rules relating them rather than every combination they permit.
2. **The orchestrator is the component best placed to erode this architecture accidentally.** Every rule here resists a pressure that is real: a blocked run is expensive, visible, and the natural fix is always a default. The rules say no; an implementation under deadline will test each one.
3. **Race case 6 — a late Decision Record — is the least settled.** The Record stands and the effect is escalated, which is right and also leaves a human holding a genuinely hard question with no procedure behind it.
4. **`COMPLETED_WITH_OPEN_ITEMS` depends on upstream rules that may not all exist.** The architecture requires each carried item to name a rule permitting it. Where the upstream phase never wrote one, the correct behaviour is to block — which will be read as an obstruction.
5. **Bounded determinism may be narrower than it sounds.** The orchestrator's own decisions are deterministic; almost everything interesting in a run is not. An auditor expecting to re-derive an execution will re-derive the coordination and nothing else.
6. **The exemplars are synthetic, and two of the six end in a block.** That is accurate — a missing Right and an unavailable independent reviewer both block today — and it means the two most instructive paths in this phase are ones nobody has yet been able to complete.

## Standing statement

Every Phase 11 artifact is `PROPOSED`. Nothing is APPROVED or CANONICAL. No orchestrator, queue, worker, scheduler, event bus, state-machine service, engine, schema, migration, API, SDK, agent, prompt-as-runtime, retrieval system, credential, secret, account or deployment was created, connected to or configured. No Decision Right was created, granted or exercised; no Role gained authority; no review status was set or changed; no knowledge was promoted; no Routing Decision was made; and no approved Phase 1–10 artifact was modified. This record does not claim human approval and is not an independent audit.
