"""Phase 14 — committed adversarial / controlled-weakening fixture.

Status: PROPOSED. Standard library only, deterministic, no network.

    python3 validation/phase_14_mutation_probes.py [--verbose] [--json]

This fixture answers a question a validator cannot answer about itself: **is each check
load-bearing, or would the specification pass anyway?** The independent Phase 14 audit rated the
harness `MEDIUM` because 8 of 9 materially contradictory mutations were accepted. This is the
mechanism for not being in that position silently.

How it works. Each probe names a load-bearing rule, a piece of specification text that carries
it, and a weakening of that text. The weakening is applied to the specification **in memory**;
the Phase 14 validator is re-run against the weakened copy in a temporary tree; and the probe
records whether any check failed.

Nothing on disk is edited. No Phase 1-13 artifact is read from anywhere but the real repository,
and none is copied, modified or written. The runner is reproducible from a clean checkout.

Each probe is classified from EXECUTED BEHAVIOUR, never from a label:

    DETECTED   - the weakening makes at least one validator check fail.
    REDUNDANT  - the weakening changes nothing the validator observes. Recorded honestly and
                 never presented as a pass; a redundant probe is a gap in the harness, stated.

A probe whose target text is not found is an ERROR, not a skip. A runner that quietly matches
nothing proves exactly as much as no runner at all.

This fixture is an assurance tool and NEVER GOVERNANCE AUTHORITY.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SPEC_DIR = "implementation-spec"

#: (name, document, old_text, new_text, rule the weakening attacks)
PROBES = [
    ("Model Profile takes an invented prefix instead of Phase 9's",
     "domain-identity-model.md",
     "| 4 | Model Profile | `ModelProfileRef` | **`model.<stable_snake_case_name>`** |",
     "| 4 | Model Profile | `ModelProfileRef` | **`model_profile.<name>`** |",
     "Phase 9 model identity compatibility"),

    ("an independent stable ModelRef is reintroduced",
     "domain-identity-model.md",
     "| 3 | Model — the **Underlying Model Release** | `ModelReleaseIdentity`",
     "| 3 | Model | `ModelRef` | `model.<name>` | Yes | Git (C1) |\n| 3b | ignored | `ModelReleaseIdentity`",
     "MODEL != MODEL PROFILE"),

    ("the Model Result is checked against a field the decision does not hold",
     "model-router-runtime-contract.md",
     "| `model_profile_ref` + `model_profile_registry_version` | ref pair | NO | IMM | **Verified equal to elements 20–21 of the recorded Routing Decision** before the write |",
     "| `model_ref` + versions | ref pair | NO | IMM | Verified equal to the recorded decision's |",
     "Routing Decision / Model Result lineage"),

    ("the release-identity divergence outcome is removed",
     "model-router-runtime-contract.md",
     "**`PROVIDER_VERSION_CHANGE` fires**",
     "the difference is noted",
     "Phase 9 silent-backend-change detection"),

    ("conflict resolution is made authority-bearing again",
     "api-command-contracts.md",
     "| `ResolveConflict` | **R** |",
     "| `ResolveConflict` | H |",
     "Phase 8 conflict-resolution authority boundary"),

    ("cancellation and termination are collapsed into one command",
     "api-command-contracts.md",
     "| `TerminateRun` | **S** |",
     "| `TerminateRun` | h |",
     "CANCELLED / TERMINATED asymmetry"),

    ("the transaction table stops stating audit counts",
     "persistence-and-transaction-model.md",
     "| **scope_transfer** | — | Source run, retained Decision Records, mechanism registry, target definition | All source-side clauses **and** every target-run creation condition, via one shared preflight | Source run `record_version` | `scope_transfer_authorisation`, target `workflow_run`, target `scope_binding`, provenance link | **4** |",
     "| **scope_transfer** | — | Source run, retained Decision Records, mechanism registry, target definition | All source-side clauses **and** every target-run creation condition, via one shared preflight | Source run `record_version` | `scope_transfer_authorisation`, target `workflow_run`, target `scope_binding`, provenance link | as needed |",
     "audit-event-per-governed-record-write cardinality"),

    ("U19 keys on a nonexistent ACTIVE approval status",
     "persistence-and-transaction-model.md",
     "| U19 | Approval state — **current pointer** | `PRIMARY KEY (subject_ref, subject_version)` on `approval_state_current` |",
     "| U19 | Approval state | `UNIQUE (subject_ref, subject_version) WHERE status = 'ACTIVE'` |",
     "approval-state current-row uniqueness"),

    ("the Phase 4 baseline is replaced with a contradictory claim",
     "README.md",
     "| Phase 4 — Skill Registry | `8ddacb2b2d2bc47e1a65099df575a0b16205d046` |",
     "| Phase 4 — Skill Registry | *(no SHA recorded)* |",
     "exact Phase 4 approved baseline citation"),

    ("the identity chain is reordered",
     "domain-identity-model.md",
     "ROLE != AGENT INSTANCE != MODEL != MODEL PROFILE",
     "ROLE != MODEL != AGENT INSTANCE != MODEL PROFILE",
     "exact ordered identity-chain equality"),

    ("an approved origin value is dropped",
     "knowledge-and-canonical-model.md",
     "| `EXTERNAL_ORIGIN` | Received from outside the entity |",
     "| `THIRD_PARTY` | Received from outside the entity |",
     "origin-axis completeness"),

    ("self-review is reduced to a class label",
     "decision-review-authority-model.md",
     "equals any producer identity recorded on the reviewed artifact version",
     "declares a class other than PRODUCER_REVIEW",
     "self-review identity inequality"),

    ("the separator-boundary ancestry rule is removed",
     "scope-and-context-model.md",
     "**Rule S-2 — the prefix trap.**",
     "**Rule S-2 — removed.**",
     "separator-boundary ancestry"),

    ("the approval registry is allowed to create approval",
     "approval-state-registry.md",
     "**Rule AP-2 — the registry records approval; it never creates it.**",
     "**Rule AP-2 — the registry may record or establish approval.**",
     "approval registry records but never creates approval"),

    ("the execution-event contract stops denying governance evidence",
     "audit-provenance-observability.md",
     "Written by C9. **Coordination history. Not governance evidence.**",
     "Written by C9. **Coordination history, and governance evidence where a gate needs it.**",
     "operational events never satisfy governance evidence"),

    ("the write-only event interface gains a read operation",
     "audit-provenance-observability.md",
     "interface has an `append` operation and **no read operation at all**",
     "interface has an `append` operation and a read operation for governed lookups",
     "structural enforcement of the runtime-event boundary"),

    ("a convenience exception is carved for governed uniqueness",
     "persistence-and-transaction-model.md",
     "`ON CONFLICT DO NOTHING` is\nprohibited on every table above",
     "`ON CONFLICT DO NOTHING` is\npermitted where convenient",
     "no ON CONFLICT DO NOTHING exception"),

    ("an administrative path is offered for a destructive migration",
     "migrations-versioning-compatibility.md",
     "there is no `--force`, no environment variable and no break-glass parameter on the applier",
     "a database owner may apply it directly where the Right is not yet mapped",
     "no admin substitution for the destructive-migration Right"),

    ("a blocked authority section is renamed away",
     "open-items-and-blocked-authorities.md",
     "### BA-3 — Controlled destruction of governed content",
     "### BX-3 — Controlled destruction of governed content",
     "missing Decision Rights are not silently filled"),

    # ---- re-audit v2 required coverage -------------------------------------------------
    ("A12 regresses to human-intervention termination semantics",
     "test-and-assurance-strategy.md",
     "| A12c | `TerminateRun` | CURRENT | Supply or smuggle a `HumanInterventionRecord` into a command whose contract accepts none | `UNEXPECTED_HUMAN_INTERVENTION`, and **no human identity appears in any resulting record** |",
     "| A12c | `TerminateRun` | CURRENT | Use an intervention naming run B when terminating run A | `FOREIGN_RUN_LINEAGE` |",
     "A12 attacks the real TerminateRun contract"),

    ("the termination positive control is removed",
     "test-and-assurance-strategy.md",
     "| P-A12 | `TerminateRun` | CURRENT |",
     "| P-A12 | `CancelRun` | CURRENT |",
     "a valid constraint-driven termination has a positive control"),

    ("a governed API command is dropped from the transaction table",
     "persistence-and-transaction-model.md",
     "| **supply_gate_evidence** |",
     "| **supply_gate_evidence_REMOVED** |",
     "API command set == transaction act set"),

    ("a transaction row has no governed API command",
     "api-command-contracts.md",
     "| 28 | `RaiseConflict` | N | `raise_conflict` |",
     "| 27 | `RaiseConflict` | N | `raise_conflict_other` |",
     "transaction act set == API command set"),

    ("the two approval acts collapse back into one ambiguous class",
     "api-command-contracts.md",
     "| 31 | `TranscribeApprovalState` | **h** | `transcribe_approval_state` |",
     "| 31 | `TranscribeApprovalState` | **H** | `transcribe_approval_state` |",
     "approval command classes match registry semantics"),

    ("transcription may create approval without an authoritative source",
     "approval-state-registry.md",
     "**Rule AP-2a — transcription is mechanical or it is refused.**",
     "**Rule AP-2a — transcription may fill gaps the source leaves.**",
     "transcription records but never creates approval"),

    ("approval history is written without the current-pointer update",
     "persistence-and-transaction-model.md",
     "`approval_state_record` (new immutable version), `approval_state_current` (create or move) | **2** |",
     "`approval_state_record` (new immutable version) | **1** |",
     "history and pointer move in one transaction"),

    ("the uniqueness count in a milestone drifts from the inventory",
     "implementation-sequencing.md",
     "Every constraint in the canonical uniqueness inventory (currently **23**)",
     "All 20 uniqueness constraints",
     "uniqueness inventory count == milestone references"),

    ("A17 mixes current and hypothetical Right availability",
     "test-and-assurance-strategy.md",
     "| A17b | `PromoteToCanonical` | **HYPOTHETICAL** |",
     "| A17b | `PromoteToCanonical` | CURRENT |",
     "A17 current-vs-hypothetical consistency"),

    ("an INSERT audit event is required to carry a before-version",
     "audit-provenance-observability.md",
     "| `INSERT` | A governed record exists that did not exist | **NULL** — required to be null; there is no prior version, and a value would be a fiction | **NOT NULL** |",
     "| `INSERT` | A governed record exists that did not exist | **NOT NULL** | **NOT NULL** |",
     "audit version-nullability matrix"),

    ("a newly covered governed act stops stating its audit count",
     "persistence-and-transaction-model.md",
     "posture in one append (P-14g) | **2** |",
     "posture in one append (P-14g) | as needed |",
     "audit cardinality after full command coverage"),

    ("a blocked command is allowed a governed write",
     "persistence-and-transaction-model.md",
     "| — | **0 — nothing is ever written** | **0** | 1 (refusal) | — | **Blocked at precondition 9 (BA-1).",
     "| — | `canonical_record` | **1** | 1 (refusal) | — | **Blocked at precondition 9 (BA-1).",
     "blocked commands declare zero writes"),

    # ---- re-audit v3 required coverage -------------------------------------------------
    ("the Routing Request is persisted by a separate command as well as by route()",
     "api-command-contracts.md",
     "| 4 | `Route` | S | `route` |",
     "| 4 | `RequestRouting` | S | `request_routing` | Halted guard | Routing request | `RUN_HALTED` |\n| 4 | `Route` | S | `route` |",
     "one Routing Request lifecycle"),

    ("a malformed Router answer leaves a committed request",
     "persistence-and-transaction-model.md",
     "| **route** | B1 invalid answer | Run, Work Item, Routing Policy @v, candidate universe | Halted guard; answer type, request identity, run and Work Item binding, Router identity, six-part completeness on a selection | Run `record_version` | **0 — no request, no decision** | **0** |",
     "| **route** | B1 invalid answer | Run, Work Item, Routing Policy @v, candidate universe | Halted guard; answer type, request identity, run and Work Item binding, Router identity, six-part completeness on a selection | Run `record_version` | `routing_request` | **1** |",
     "malformed Router output commits nothing"),

    ("U6 forbids a second decision for a re-submitted request",
     "persistence-and-transaction-model.md",
     "| U6 | Routing Decision | `UNIQUE (routing_request_ref, submission_ordinal)` |",
     "| U6 | Routing Decision | `UNIQUE (routing_request_ref)` |",
     "a retry re-submits the same request"),

    ("a class-4 retry writes nothing instead of blocking and escalating",
     "persistence-and-transaction-model.md",
     "| **retry** | R4 refused, non-retryable (class 4) | Work Item bound retry class | The request is made at all | Run `record_version` | `retry_refusal_record`, run state → `BLOCKED` **with posture `GATE_UNSATISFIED`**, run state → `ESCALATED` **with posture `GATE_UNSATISFIED`** | **3** |",
     "| **retry** | R4 refused, non-retryable (class 4) | Work Item bound retry class | The request is made at all | Run `record_version` | none | **0** |",
     "a refused retry is a governed write"),

    ("a class-6 unknown external effect is retried automatically",
     "persistence-and-transaction-model.md",
     "| **retry** | R6 refused, external side effect (class 6) | Work Item class, the attempt's external-effect state | The request is made at all | Run `record_version` | `retry_refusal_record` naming the external-effect state, run state → `BLOCKED` **with posture `GATE_UNSATISFIED`**, run state → `ESCALATED` **with posture `GATE_UNSATISFIED`** | **3** |",
     "| **retry** | R6 refused, external side effect (class 6) | Work Item class, the attempt's external-effect state | The request is made at all | Run `record_version` | `retry_attempt`, run phase | **2** |",
     "class 6 never becomes a retry"),

    ("model invocation claims local atomicity across the provider call",
     "persistence-and-transaction-model.md",
     "| **invoke_model** | S1 local intent | Recorded Routing Decision, Work Item | Halted guard, decision is this run's, outcome eligible. **No provider call occurs in this transaction** | Run `record_version` | `model_invocation` intent, `provider_attempt` at `NOT_ATTEMPTED` — **plus an outbox row, which is operational (P-20a) and is not audited** | **2** |",
     "| **invoke_model** | S1 local intent | Recorded Routing Decision, Work Item | Halted guard, decision is this run's, outcome eligible | Run `record_version` | `model_invocation`, `model_result` | **2** |",
     "model invocation is staged, not one local commit"),

    ("a timeout is treated as proof that no external effect occurred",
     "api-command-contracts.md",
     "**Rule Q-23 — a timeout is not proof that nothing happened.**",
     "**Rule Q-23 — a timeout means the call did not happen.**",
     "unknown external effects are neither assumed nor retried"),

    ("record_version_after is forced non-null for DESTROY",
     "audit-provenance-observability.md",
     "| `DESTROY` | A governed record was destroyed | **NOT NULL** | **NULL** — there is no after |",
     "| `DESTROY` | A governed record was destroyed | **NOT NULL** | **NOT NULL** |",
     "the version-nullability matrix"),

    ("the audit field table restates an unconditional nullability",
     "audit-provenance-observability.md",
     "| 2b | `record_version_after` | **Conditional on `mutation_kind` — §4.1** | The version it holds after |",
     "| 2b | `record_version_after` | **NO for every successful write** | The version it holds after |",
     "field table and matrix agree"),

    ("a normative gate states a stale uniqueness count in digits",
     "implementation-sequencing.md",
     "canonical uniqueness inventory (currently **23**)",
     "canonical uniqueness inventory (currently **21**)",
     "every normative count matches the inventory"),

    ("a normative gate states a stale uniqueness count in words",
     "implementation-sequencing.md",
     "**every constraint in the canonical uniqueness inventory**",
     "**twenty** uniqueness constraints",
     "word-form count drift"),

    ("the self-check states a stale governed-act count",
     "phase-14-self-check.md",
     "| Governed commands | **36**,",
     "| Governed commands | **seventeen**,",
     "stale governed-act count"),

    ("M20 omits a current adversarial test by reverting to a range",
     "implementation-sequencing.md",
     "| **M20** | Assurance completion | **Every ID in each canonical assurance inventory**",
     "| **M20** | Assurance completion | The adversarial set A1–A30",
     "assurance gates require the whole inventory"),

    ("G-R omits the positive controls",
     "implementation-sequencing.md",
     "| **G-R** | Leaving M20 | **Every ID in every canonical assurance inventory passes**",
     "| **G-R** | Leaving M20 | A1–A30 and I1–I12 pass",
     "assurance gates require the whole inventory"),

    ("a normative gate cites an assurance ID that does not exist",
     "implementation-sequencing.md",
     "| **G-G** | M8 | A1, A2, A3, A8, A9, A10 |",
     "| **G-G** | M8 | A1, A2, A3, A8, A9, A10, A99 |",
     "no orphan assurance IDs"),

    ("BA-1 stops covering governed downgrade",
     "open-items-and-blocked-authorities.md",
     "| **Also blocked: governed downgrade** |",
     "| **Also permitted: governed downgrade** |",
     "BA-1 fails closed in both directions"),

    # ---- revision 5: the seven V4 blockers ------------------------------------------------

    ("B3 commits a durable decision with no run-state append",
     "persistence-and-transaction-model.md",
     "`routing_request`, `routing_decision`, **run state \u00d7 *s*** \u2014 the exact appends, postures and wait subject of Rule Q-17b, in the same transaction | **2 + *s***",
     "`routing_request`, `routing_decision` | **2**",
     "a durable non-selection never leaves the run eligible to continue"),

    ("B4n loses its run-state consequence",
     "persistence-and-transaction-model.md",
     "| **route** | B4n re-submission, non-selection |",
     "| **route** | B4x re-submission, non-selection |",
     "every routing branch has a commit contract"),

    ("an invalid answer after a durable request advances the submission ordinal",
     "persistence-and-transaction-model.md",
     "**0 \u2014 the existing Routing Request is preserved, no decision is created, and `submission_ordinal` is not advanced**",
     "**0 governed records; `submission_ordinal` is advanced to reserve the attempt**",
     "an invalid answer never disturbs a durable request"),

    ("R2f stops stating its posture",
     "api-command-contracts.md",
     "| **R2f revalidation fails** | 2 | A re-evaluated precondition no longer holds | `RETRY_PENDING` \u2192 `BLOCKED` | unchanged \u2192 **`GATE_UNSATISFIED`** |",
     "| **R2f revalidation fails** | 2 | A re-evaluated precondition no longer holds | `RETRY_PENDING` \u2192 `BLOCKED` | unchanged |",
     "retry posture is a committed write"),

    ("R4 drops the halted posture from its exact governed writes",
     "persistence-and-transaction-model.md",
     "`retry_refusal_record`, run state \u2192 `BLOCKED` **with posture `GATE_UNSATISFIED`**, run state \u2192 `ESCALATED` **with posture `GATE_UNSATISFIED`** | **3** | 2 | \u2014 | Nothing written. **This branch is never",
     "`retry_refusal_record`, run phase \u2192 `BLOCKED`, run phase \u2192 `ESCALATED` | **3** | 2 | \u2014 | Nothing written. **This branch is never",
     "retry posture is a committed write"),

    ("the outbox loses its stable identity and durable uniqueness",
     "persistence-and-transaction-model.md",
     "| O1 | `PRIMARY KEY (outbox_ref)` | A duplicate dispatch identity. **This is the only identity constraint on the row**; no second constraint restates it |",
     "| O1 | *(no constraint required)* | \u2014 |",
     "the outbox has a stable identity and durable uniqueness"),

    ("two concurrently valid leases are permitted on one dispatch item",
     "persistence-and-transaction-model.md",
     "**Rule PO-3 \u2014 every state-changing write is one atomic conditional update, or it did not\nhappen.**",
     "**Rule PO-3 \u2014 claiming is advisory.**",
     "no concurrent valid lease for one dispatch item"),

    ("lease expiry is treated as proof that no provider effect occurred",
     "persistence-and-transaction-model.md",
     "**Rule PO-10 \u2014 an expired claim is never proof, and is never treated as one.**",
     "**Rule PO-10 \u2014 an expired claim establishes that no call occurred.**",
     "an expired lease is a redelivery condition, never a proof"),

    ("the outbox row is counted as a governed mutation",
     "persistence-and-transaction-model.md",
     "`model_invocation` intent, `provider_attempt` at `NOT_ATTEMPTED` \u2014 **plus an outbox row, which is operational (P-20a) and is not audited** | **2** |",
     "`model_invocation` intent, `provider_attempt` at `NOT_ATTEMPTED`, outbox row | **3** |",
     "the outbox is operational in every document that counts it"),

    ("a crash window is reintroduced between stages 3 and 4",
     "api-command-contracts.md",
     "| Between stages 3 and 4 | **Unreachable.** They are one transaction (Q-22b): there is no committed outcome without its result | \u2014 |",
     "| After stage 3, before stage 4 | Outcome recorded, no result | Stage 4 completes idempotently under U7 |",
     "stages 3 and 4 are one transaction"),

    ("a refused-act test requires total execution-event equality",
     "test-and-assurance-strategy.md",
     "| A38 | `Route` | CURRENT | Malformed, foreign-Router or identity-mismatched answer | **No Routing Request and no Routing Decision** is committed; zero audit events; one refusal execution event (branch B1) |",
     "| A38 | `Route` | CURRENT | Malformed, foreign-Router or identity-mismatched answer | **No Routing Request and no Routing Decision** is committed; the execution-event count is identical before and after |",
     "a required refusal event never contradicts observational equality"),

    ("the self-check restates a stale command/row count and reintroduces RequestRouting",
     "phase-14-self-check.md",
     '| 2 | The transaction table claimed exhaustiveness while covering 17 of the governed commands | `api-command-contracts.md` §5.1 became **the** canonical governed-command inventory, each entry carrying an explicit **Act** key naming its transaction contract, and `persistence-and-transaction-model.md` §7.2 was keyed identically. The validator derives both sets and requires exact equality in both directions; duplicate coverage is permitted only through an explicit alias, of which there are currently none. Every previously omitted act — `RecordIntervention`, `ResumeRun`, `UnblockRun`, `SupplyGateEvidence`, `CreateKnowledgeItem`, `AdoptAISuggestion`, `RaiseConflict`, `ApplyConsequentStatusChange`, `CompleteRun` — gained a full contract, as did `RequestReview`, `RequestDecision`, `Retry`, `OpenSubRun`, `OpenReworkIteration`, `SupersedeRun` and the four blocked acts. **This row records what revision 3 did and states no current total**: the inventory sizes it quoted were correct at that revision and are not, and must never be read as, a claim about the package as it now stands — §6 holds the only current counts, and every one of them is derived from its owning table. The `RequestRouting` command named in the revision-3 wording of this row **was removed in revision 4** and is not a member of any current inventory (§10, blocker 1) |',
     '| 2 | The transaction table claimed exhaustiveness while covering 17 of the governed commands | `api-command-contracts.md` §5.1 is now **the** canonical governed-command inventory — 35 numbered commands, each carrying an explicit **Act** key naming its transaction contract. `persistence-and-transaction-model.md` §7.2 has **35 rows**, keyed identically. The validator derives both sets and requires exact equality in both directions; duplicate coverage is permitted only through an explicit alias, of which there are currently none. Every previously omitted act — `RecordIntervention`, `ResumeRun`, `UnblockRun`, `SupplyGateEvidence`, `CreateKnowledgeItem`, `AdoptAISuggestion`, `RaiseConflict`, `ApplyConsequentStatusChange`, `CompleteRun` — now has a full contract, as do `RequestRouting`, `RequestReview`, `RequestDecision`, `Retry`, `OpenSubRun`, `OpenReworkIteration`, `SupersedeRun` and the four blocked acts |',
     "every normative count matches its canonical inventory; no removed command is current"),

    # ---- revision 6: the V5 blockers, and the six demonstrated nearby escapes -------------

    ("a time-dependent partial index returns as an ownership constraint",
     "persistence-and-transaction-model.md",
     "| O4 | `CHECK ( (claim_state IN ('CLAIMED','DISPATCH_PENDING')) = (lease_owner IS NOT NULL AND lease_expires_at IS NOT NULL AND claim_token IS NOT NULL) )` | A row that is owned without an owner, a token or an expiry — or unowned while still carrying them |",
     "| O4 | A partial unique index on `outbox_ref` `WHERE claim_state = 'CLAIMED' AND lease_expires_at > now()` | Two concurrently valid leases |",
     "ownership is a row property, never a time-dependent index"),

    ("a redundant identity uniqueness restates O1 and cannot enforce ownership",
     "persistence-and-transaction-model.md",
     '| O2 | `UNIQUE (provider_attempt_ref)` | Two dispatch items racing to satisfy one provider attempt |',
     "| O2 | `UNIQUE (outbox_ref)` | Two claimants on one dispatch item |",
     "one identity constraint on the dispatch item"),

    ("the crash point after provider acceptance is removed",
     "api-command-contracts.md",
     '| After provider acceptance, before the stage 3/4 commit | Identical to the row above: an outcome the system did not commit is an outcome the system does not have | Stage 5, via T7. **Never a redispatch of this dispatch item or its key** — PO-14 admits no exception, and reconciliation, not replay, resolves the unknown |',
     "| After provider acceptance, before the stage 3/4 commit | The attempt is `NOT_ATTEMPTED`, so nothing left the system | Re-dispatch |",
     "no local state is read as proof of non-occurrence after the boundary"),

    ("settlement stops being token-fenced, so a stale writer can settle",
     "persistence-and-transaction-model.md",
     "| T4 | `DISPATCH_PENDING` → `SETTLED`, outcome **observed** (`CONFIRMED_APPLIED` or `CONFIRMED_NOT_APPLIED`) | The row, the provider response | `claim_state='DISPATCH_PENDING'` **AND** `claim_token = <held>` **AND** `claim_generation = <read>` | `claim_state='SETTLED'`, `lease_owner`/`claim_token`/`lease_expires_at` cleared (O4), `claim_generation`+1 | Token **and** generation | n/a — terminal | No |",
     "| T4 | `DISPATCH_PENDING` \u2192 `SETTLED`, outcome **observed** (`CONFIRMED_APPLIED` or `CONFIRMED_NOT_APPLIED`) | The row, the provider response | `claim_state='DISPATCH_PENDING'` | `claim_state='SETTLED'` | none | n/a \u2014 terminal | No |",
     "every transition is token-fenced"),

    ("stage 3/4 success stops settling the dispatch item",
     "persistence-and-transaction-model.md",
     "**Rule PO-13 \u2014 successful governed persistence settles the dispatch item in the same\ntransaction.**",
     "**Rule PO-13 \u2014 the dispatch item is settled by the drain at its convenience.**",
     "stage 3/4 success settles the operational dispatch state"),

    ("a normative rule identifier is defined twice",
     "persistence-and-transaction-model.md",
     "**Rule PO-1 \u2014 the provider idempotency key is stable and never regenerated.**",
     "**Rule P-23 \u2014 the provider idempotency key is stable and never regenerated.**",
     "unique normative rule identifiers"),

    ("stale routing cardinality prose returns to the self-check narrative",
     "phase-14-self-check.md",
     "The branches are encoded identically in the API inventory, the router contract and the transaction table, and **their current cardinalities are stated only in those tables**",
     "Four branches are encoded identically: **B3** valid non-selection commits request and decision together, 2 audit events; **B4** re-submission commits the decision only, 1 audit event.",
     "no active location restates a routing branch's counts"),

    ("B3 loses its run-state append in the API branch table",
     "api-command-contracts.md",
     '| **B3 non-selection, first submission** | `NO_ELIGIBLE_MODEL`, `CANDIDATE_UNIVERSE_INCOMPLETE`, `NO_APPLICABLE_DECISION_RIGHT`, `ACT_REQUIREMENT_OUTSTANDING` | `routing_request`, `routing_decision`, **run state × *s*** (Q-17b) | **2 + *s*** | 2 | Exactly the run state Q-17b names. The run never continues |',
     "| **B3 non-selection, first submission** | `NO_ELIGIBLE_MODEL`, `CANDIDATE_UNIVERSE_INCOMPLETE`, `NO_APPLICABLE_DECISION_RIGHT`, `ACT_REQUIREMENT_OUTSTANDING` | `routing_request`, `routing_decision` | **2** | 2 | Blocked or waiting, per the outcome |",
     "no nearby location contradicts the routing branch semantics"),

    ("B4n loses its inherited consequence in the API branch table",
     "api-command-contracts.md",
     '| **B4n re-submission, non-selection** | A valid non-selection against an **already durable** request | `routing_decision`, **run state × *s*** (Q-17b) | **1 + *s*** | 1 | Exactly the run state Q-17b names. The run never continues |',
     "| **B4n re-submission, non-selection** | A valid non-selection against an **already durable** request | `routing_decision` only | **1** | 1 | Per the outcome |",
     "no nearby location contradicts the routing branch semantics"),

    ("B1r advances the submission ordinal in nearby API prose",
     "api-command-contracts.md",
     "`submission_ordinal` is **not** advanced, so the next valid submission takes the ordinal the\ninvalid one would have consumed.",
     "`submission_ordinal` is advanced, so the invalid submission consumes an ordinal of its own.",
     "no nearby location contradicts the routing branch semantics"),

    ("a nearby router location drops B4n's run-state appends",
     "model-router-runtime-contract.md",
     '| B4n | A valid non-selection re-submitted against an already durable request | Already durable | Yes, at the next ordinal, **with the same run-state appends as B3**',
     "| B4n | A valid non-selection re-submitted against an already durable request | Already durable | Yes, at the next ordinal, and the `routing_decision` only",
     "no nearby location contradicts the routing branch semantics"),

    ("a nearby assurance location requires equal total execution-event counts",
     "test-and-assurance-strategy.md",
     "**Rule T-18 \u2014 two assertions, never one conflated.**",
     "**Rule T-18 \u2014 one assertion.** A refused act leaves the execution-event count identical before and after.",
     "a required refusal event never contradicts observational equality"),

    ("a nearby location permits automatic redispatch of an unknown effect",
     "api-command-contracts.md",
     "**Rule Q-31 \u2014 the R6 branch never becomes a retry.**",
     "**Rule Q-31 \u2014 the R6 branch resumes.** An `ATTEMPTED_OUTCOME_UNKNOWN` external effect is safe to redispatch automatically once the lease expires.",
     "no active location permits auto-redispatch of an unknown effect"),

    ("a remediation test is required by no milestone gate",
     "implementation-sequencing.md",
     '| **G-N** | M15 | A41, A42, A43, A48, A49, A50, A51, A52, A56, A57, A58, A59, A60, A62, A63, A64, P-A41, P-A42, P-A49, P-A56, P-A62 |',
     '| **G-N** | M15 | A41, A42, A43, P-A41, P-A42 |',
     "the assurance manifest partitions the canonical inventories"),

    # ---- revision 7: the nine V6 escapes, each planted in a SECOND active location ---------

    ("B3 loses its run-state append in a third active location",
     "test-and-assurance-strategy.md",
     '| A54 | `Route` | CURRENT | Commit a valid non-selection decision while leaving the run eligible to continue | Refused. The decision and the run-state appends of Rule Q-17b are one transaction (Q-17c) |',
     "| A54 | `Route` | CURRENT | Commit a valid non-selection decision while leaving the run eligible to continue | Refused. B3 commits `routing_request` and `routing_decision` in one transaction |",
     "no active location contradicts the routing branch semantics"),

    ("B4n loses its inherited consequence in the Q-17d rule",
     "api-command-contracts.md",
     "**Rule Q-17d \u2014 B4 inherits B3's consequence, never a weaker one.**",
     "**Rule Q-17d \u2014 B4n writes the `routing_decision` and nothing else.**",
     "no active location contradicts the routing branch semantics"),

    ("B1r consumes an ordinal in a third active location",
     "test-and-assurance-strategy.md",
     '| A53 | `Route` | CURRENT | Send a malformed answer after the Routing Request is already durable, and expect the ordinal to advance or the request to change | Branch B1r: the request is preserved, no decision is written, `submission_ordinal` does **not** advance; one refusal execution event |',
     "| A53 | `Route` | CURRENT | Send a malformed answer after the Routing Request is already durable | Branch B1r: the durable request stands and `submission_ordinal` advances to reserve the attempt |",
     "no active location contradicts the routing branch semantics"),

    ("a stale owner's write is honoured outside the transition table",
     "failure-recovery-race-model.md",
     "**Rule F-9e \u2014 the call boundary is crossed before it is crossed.**",
     "**Rule F-9e \u2014 the call boundary is crossed before it is crossed.** A former owner's write is still honoured after the lease expires.",
     "no active location weakens the stale-writer fencing semantics"),

    ("the provider idempotency key is regenerated in a second active location",
     "test-and-assurance-strategy.md",
     '| A51 | *outbox drain* | CURRENT | Regenerate the provider idempotency key on redelivery | Refused. The key is derived once in the enqueuing transaction and is stable for the life of the row (PO-1) |',
     "| A51 | *outbox drain* | CURRENT | Regenerate the provider idempotency key on redelivery | Permitted. The drain derives a fresh key each time it redelivers |",
     "no active location permits regenerating a dispatch item's key"),

    ("the outbox is reclassified as governed outside the owning rule",
     "system-component-model.md",
     '| C16 | **Outbox & Reconciliation Worker** | Draining staged external effects, recording external-effect uncertainty, driving reconciliation (`failure-recovery-race-model.md` §6) | Compensate on its own authority; retry a non-retryable governed act |',
     "| C16 | **Outbox & Reconciliation Worker** | Its outbox rows are governed records and each one writes an audit event | Operational |",
     "no active location reclassifies the outbox as governed"),

    ("refusal equality is restated to include the execution-event count",
     "api-command-contracts.md",
     '| **B1 invalid, first submission** | Malformed, wrong request identity, foreign Router, or an incomplete six-part set on a selection | **0 — no request, no decision** | **0** | 1 (refusal) | None. Governed state and governed history unchanged (Rule O-25) |',
     "| **B1 invalid, first submission** | Malformed, wrong request identity, foreign Router, or an incomplete six-part set on a selection | **0 \u2014 no request, no decision** | **0** | 1 (refusal) | None. The execution-event count must remain identical |",
     "a required refusal event never contradicts observational equality"),

    ("a stale transaction-table row count survives in active prose",
     "phase-14-self-check.md",
     "| Governed commands | **36**, each with exactly one transaction contract; the two sets are compared and equal |",
     "| Governed commands | **36**, each with exactly one transaction contract; \u00a77.2 has 49 rows |",
     "every normative count matches its canonical inventory"),

    ("an unknown effect is auto-redispatched in a second active location",
     "failure-recovery-race-model.md",
     "**Rule F-9d \u2014 the drain protocol is specified once, in persistence \u00a79.**",
     "**Rule F-9d \u2014 the drain protocol is specified once, in persistence \u00a79.** An attempt whose `boundary_crossed` is true may be redispatched automatically once its claim expires.",
     "no active location permits auto-redispatch of an unknown external effect"),

    ("a blockquoted rule definition collides with an active rule id",
     "persistence-and-transaction-model.md",
     "> **Rule P-14a \u2014 one audit event per persisted governed-record mutation, in the same",
     "> **Rule P-20a \u2014 one audit event per persisted governed-record mutation, in the same",
     "unique normative rule identifiers, blockquoted definitions included"),

    ("an active rule reference points at a rule that does not exist",
     "api-command-contracts.md",
     "`persistence-and-transaction-model.md` PO-14 forbids that unconditionally, and PO-14b states that",
     "`persistence-and-transaction-model.md` Rule PO-27 forbids that unconditionally, and PO-14b states that",
     "every active rule reference resolves"),

    ("crossed-boundary redispatch returns as a conditional permission",
     "persistence-and-transaction-model.md",
     "| `UNCERTAIN`, reconciliation says `CONFIRMED_NOT_APPLIED` | **Never** | T8 to `SETTLED`. Continuation is a **new** governed provider attempt at the next ordinal, with a **new** key (PO-14) |",
     "| `UNCERTAIN`, reconciliation says `CONFIRMED_NOT_APPLIED` | **Yes**, only after reconciliation answers | T8 to `SETTLED`, then re-dispatch under the same key |",
     "crossed-boundary redispatch is prohibited outright"),

    ("T11 stops fencing retirement on the current owner",
     "persistence-and-transaction-model.md",
     "**AND** `lease_owner = <the writer's own service identity>` **AND** `claim_token = <held>` **AND** `claim_generation = <read>` | as T10 | Owner, token **and** generation |",
     "**AND** `claim_generation = <read>` | as T10 | Generation |",
     "retirement is owner-fenced"),

    ("O5 is presented as enforcing monotonic increase",
     "persistence-and-transaction-model.md",
     "**Monotonicity is not claimed as a database guarantee.**",
     "**Monotonicity is enforced by the O5 constraint.**",
     "monotonicity lives in the CAS predicates, not in a row CHECK"),

    # ---- V7 B1: external delivery / replay, each plant in a distinct active location ------
    ("Q-26 reintroduces external at-least-once delivery",
     "api-command-contracts.md",
     "| External **at-least-once** | This protocol does not redeliver. A crossed item never presents its key again (PO-14); a lost call is resolved by **reconciliation** and, where reconciliation reports `CONFIRMED_NOT_APPLIED`, by a **new** governed attempt with a new attempt identity, a new dispatch item identity and a new provider idempotency key, linked to the prior lineage (PO-14a, PO-19) |",
     "| External **at-least-once** | Provided across the boundary wherever the provider deduplicates on the attempt's idempotency key |",
     "no active location claims external at-least-once"),

    ("Q-24 conditionally permits same-item crossed-boundary redispatch",
     "api-command-contracts.md",
     "Stage 5, via T7. **Never a redispatch of this dispatch item or its key** — PO-14 admits no exception",
     "Stage 5, via T7. **Never a redispatch** unless PO-14 is satisfied",
     "the no-redispatch rule carries no condition"),

    ("T5 reintroduces conditional redispatch of the crossed item",
     "persistence-and-transaction-model.md",
     "| T5 | `DISPATCH_PENDING` → `UNCERTAIN`, outcome **unknown to the caller itself** (timeout, reset, ambiguous response) | The row | `claim_state='DISPATCH_PENDING'` **AND** `claim_token = <held>` **AND** `claim_generation = <read>` | `claim_state='UNCERTAIN'`, owner columns cleared, `claim_generation`+1 | Token **and** generation | **Never** — PO-14 is unconditional |",
     "| T5 | `DISPATCH_PENDING` → `UNCERTAIN`, outcome **unknown to the caller itself** (timeout, reset, ambiguous response) | The row | `claim_state='DISPATCH_PENDING'` **AND** `claim_token = <held>` **AND** `claim_generation = <read>` | `claim_state='UNCERTAIN'`, owner columns cleared, `claim_generation`+1 | Token **and** generation | **No** (except under PO-14) |",
     "a crossed-boundary transition denies redispatch unconditionally"),

    ("T7 reintroduces conditional redispatch of the crossed item",
     "persistence-and-transaction-model.md",
     "| T7 | `DISPATCH_PENDING` → `UNCERTAIN`, expired-claim recovery | The row | `claim_state='DISPATCH_PENDING'` **AND** `boundary_crossed = true` **AND** `lease_expires_at <= now()` **AND** `claim_generation = <read>` | `claim_state='UNCERTAIN'`, owner columns cleared, `claim_generation`+1 | Generation | **Never** — PO-14 is unconditional |",
     "| T7 | `DISPATCH_PENDING` → `UNCERTAIN`, expired-claim recovery | The row | `claim_state='DISPATCH_PENDING'` **AND** `boundary_crossed = true` **AND** `lease_expires_at <= now()` **AND** `claim_generation = <read>` | `claim_state='UNCERTAIN'`, owner columns cleared, `claim_generation`+1 | Generation | **No** (except where the provider deduplicates) |",
     "a crossed-boundary recovery denies redispatch unconditionally"),

    ("a crash summary says provider dedup permits crossed-item replay",
     "persistence-and-transaction-model.md",
     "**T7** to `UNCERTAIN`; attempt `ATTEMPTED_OUTCOME_UNKNOWN`; **reconciliation, never redispatch** — PO-14 admits no exception, and a provider's deduplication guarantee is not one (PO-14b)",
     "**T7** to `UNCERTAIN`; attempt `ATTEMPTED_OUTCOME_UNKNOWN`; reconciliation, or redispatch where provider deduplication permits it",
     "crash recovery agrees with PO-17"),

    ("CONFIRMED_NOT_APPLIED continuation reuses the old identity and key",
     "persistence-and-transaction-model.md",
     "| `UNCERTAIN`, reconciliation says `CONFIRMED_NOT_APPLIED` | **Never** | T8 to `SETTLED`. Continuation is a **new** governed provider attempt at the next ordinal, with a **new** key (PO-14) |",
     "| `UNCERTAIN`, reconciliation says `CONFIRMED_NOT_APPLIED` | **Yes** | T8 to `SETTLED`, then the same dispatch item is presented again under its own key |",
     "a continuation is a new attempt, identity and key"),

    ("the orchestrator guarantee table drops the external at-most-once statement",
     "orchestrator-runtime-contract.md",
     "**Rule O-21a — across the provider boundary the guarantee is at-most-once per dispatch item and\nkey.**",
     "**Rule O-21a — across the provider boundary the guarantee is at-least-once where the provider\ndeduplicates.**",
     "the external guarantee is stated in the orchestrator contract too"),

    # ---- V7 B2: retry classification, in the owner table and in a second location ---------
    ("a Stage 1 governed-write command is labelled SAFE_AUTOMATIC_RETRY",
     "api-command-contracts.md",
     "| 1 | `InvokeModel` | `model_invocation`, `provider_attempt` — **two**, plus two audit events (Q-22a) | **2 `RETRY_REQUIRING_REVALIDATION`** |",
     "| 1 | `InvokeModel` | `model_invocation`, `provider_attempt` — **two**, plus two audit events (Q-22a) | **1 `SAFE_AUTOMATIC_RETRY`** |",
     "no governed-write command carries a no-governed-write class"),

    ("a Stage 5 governed-write command is labelled SAFE_AUTOMATIC_RETRY",
     "api-command-contracts.md",
     "| 5 | `ReconcileExternalEffect` | `reconciliation`, `provider_attempt` state, and `model_result` where the effect is confirmed applied | **2 `RETRY_REQUIRING_REVALIDATION`** |",
     "| 5 | `ReconcileExternalEffect` | `reconciliation`, `provider_attempt` state, and `model_result` where the effect is confirmed applied | **1 `SAFE_AUTOMATIC_RETRY`** |",
     "no governed-write command carries a no-governed-write class"),

    ("the branch table lets a governed-write step reach the class-1 branch",
     "api-command-contracts.md",
     "| **R1 automatic** | 1 `SAFE_AUTOMATIC_RETRY`, 5 `REPLAYABLE_READ_ONLY` — **neither class writes a governed record**, so no `InvokeModel` stage reaches this branch (Q-25) |",
     "| **R1 automatic** | 1 `SAFE_AUTOMATIC_RETRY`, 5 `REPLAYABLE_READ_ONLY`, and the governed-write stages of `InvokeModel` |",
     "a second-location table classifies no governed-write command as class 1"),

    ("prose equates 'not authority-bearing' with safe automatic retry",
     "api-command-contracts.md",
     '**Rule Q-25b — "not authority-bearing" is not "not governed", and neither is "safe to re-run".**',
     "**Rule Q-25b — a step that is not authority-bearing is SAFE_AUTOMATIC_RETRY.**",
     "the three properties are kept apart"),

    ("durable request identity is presented as the retry class itself",
     "api-command-contracts.md",
     "**Rule Q-25c — durable request identity is the mechanism, not the class.**",
     "**Rule Q-25c — durable request identity makes these commands SAFE_AUTOMATIC_RETRY.**",
     "deduplication is a mechanism, never a class"),
]


#: Checks that read repository state (git history, untracked files) rather than specification
#: content. In a temporary tree they cannot be evaluated meaningfully, and a probe never weakens
#: containment, so their verdict is DISCARDED. Counting them would make every probe "detected"
#: by an artefact of the harness - which is precisely the kind of false credibility this fixture
#: exists to prevent.
GIT_DEPENDENT = {
    "no infrastructure, dependency or deployment artifact is added",
    "only the specification package and its validator are added",
    "approved Phase 1-13 artifacts are unchanged",
}


def run_validator(tree):
    result = subprocess.run([sys.executable,
                             os.path.join(tree, "validation", "phase_14_validation.py"),
                             "--json"],
                            capture_output=True, text=True, cwd=tree)
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None, result.stderr[-400:]
    failed = [r["name"] for r in payload["results"]
              if not r["pass"] and r["name"] not in GIT_DEPENDENT]
    return failed, ""


def build_tree(base, document, old, new):
    """A temporary copy of the specification package and the validator, weakened in one place.

    Phase 1-13 artifacts are symlinked from the real repository, never copied and never
    written: the validator reads them, and this fixture must not be able to touch them."""
    tree = os.path.join(base, "tree")
    os.makedirs(os.path.join(tree, "validation"), exist_ok=True)
    shutil.copytree(os.path.join(REPO, SPEC_DIR), os.path.join(tree, SPEC_DIR))
    for name in ("phase_14_validation.py",):
        shutil.copy2(os.path.join(REPO, "validation", name),
                     os.path.join(tree, "validation", name))
    # No `.git` symlink: the containment checks are discarded anyway (GIT_DEPENDENT), and a
    # temporary tree that could reach the real repository's git directory is a tree that could
    # write to it.
    for entry in ("architecture", "orchestration", "knowledge", "models", "storage", "decisions",
                  "roles", "skills", "workflows", "handoffs", "reviews", "implementation",
                  "prompts"):
        source = os.path.join(REPO, entry)
        if os.path.exists(source):
            os.symlink(source, os.path.join(tree, entry))
    target = os.path.join(tree, SPEC_DIR, document)
    with open(target, encoding="utf-8") as handle:
        body = handle.read()
    if old not in body:
        raise AssertionError("weakening text not found in %s: %r" % (document, old[:70]))
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(body.replace(old, new, 1))
    return tree


def main():
    verbose = "--verbose" in sys.argv
    as_json = "--json" in sys.argv

    baseline_failed, error = run_validator(REPO)
    # The baseline is checked in a pristine temporary tree too, so that "the package passes"
    # means the same thing for the baseline as it does for every probe.
    if baseline_failed is None:
        print("the validator did not run on the pristine package: %s" % error)
        return 1
    if baseline_failed:
        print("the pristine package does not pass; probes would prove nothing: %s"
              % baseline_failed)
        return 1

    results = []
    for name, document, old, new, rule in PROBES:
        base = tempfile.mkdtemp(prefix="phase14-probe-")
        try:
            tree = build_tree(base, document, old, new)
            failed, error = run_validator(tree)
            if failed is None:
                results.append({"probe": name, "rule": rule, "classification": "ERROR",
                                "detail": error})
                continue
            results.append({
                "probe": name, "rule": rule,
                "classification": "DETECTED" if failed else "REDUNDANT",
                "detected_by": failed[:3],
            })
        finally:
            shutil.rmtree(base, ignore_errors=True)

    detected = [r for r in results if r["classification"] == "DETECTED"]
    redundant = [r for r in results if r["classification"] == "REDUNDANT"]
    errors = [r for r in results if r["classification"] == "ERROR"]

    if as_json:
        print(json.dumps({"total": len(results), "detected": len(detected),
                          "redundant": len(redundant), "errors": len(errors),
                          "results": results}, indent=2))
    else:
        for r in results:
            print("  %-10s %s" % (r["classification"], r["probe"]))
            if r["classification"] == "DETECTED" and verbose:
                print("             caught by: %s" % "; ".join(r["detected_by"]))
            if r["classification"] == "REDUNDANT":
                print("             NOT CAUGHT - the validator does not observe this rule")
            if r["classification"] == "ERROR":
                print("             %s" % r["detail"][:200])
        print("\n=== %d probes: %d DETECTED, %d REDUNDANT, %d ERROR ==="
              % (len(results), len(detected), len(redundant), len(errors)))

    # An error is always a failure. A redundancy is reported, not hidden, and does not by itself
    # fail the run - but the caller is told, and the self-check must state the number.
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
