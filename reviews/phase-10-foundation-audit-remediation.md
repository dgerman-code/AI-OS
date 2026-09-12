# Phase 10 — Remediation after the independent foundation audit

Status: PROPOSED — remediation record
Audited architecture baseline: `3d8eb7b667b1374485cda5733867def4380a035e`
Independent audit verdict: **FAIL** · Human approval verdict: **NOT READY**

The audit found the architecture otherwise materially sound and three defects that were not. All three were genuine, and two of them were defects in the harness rather than in the architecture — which is the more uncomfortable kind, because the suite had reported `143/143 PASS` over exactly the properties it was failing to check.

## Finding 1 — source-of-truth row 18 had two authorities

**HIGH.** Row 18 combined bounded runtime-event metadata with operational logs, named `DB` **or** an operational log sink as authority, and then carried a conflict rule stating that an operational log is not a source of truth. One row, two object classes, two authorities, and a conflict rule contradicting its own authority cell.

**Fixed by splitting, not by rewording.** A data class needing two authorities is not one data class:

| Row | Class | Authority | Conflict outcome |
|---:|---|---|---|
| 18 | Bounded runtime-event / correlation metadata | `DB` | `APPEND_ONLY_NO_CONFLICT`, then `QUARANTINE` on a duplicate |
| 19 | Operational logs (telemetry and diagnostics) | `NONE` | `NOT_A_SOURCE_OF_TRUTH` |

The same defect existed in the configuration row, which named a three-way split in prose. It is now three rows — governed configuration (`GITHUB`), environment-specific values (`ENV`), secret-valued items (`SECRETS`) — so **every authority cell in the matrix is a single token and the prose exception is gone**. The matrix goes from 21 rows to **24**.

`storage/data-domain-model.md` §2.1 now states the boundary explicitly: the `runtime_meta` domain is not where operational logs live and never becomes that; **a log is never promoted into it to make the log survive**. Anything that must survive is written to row 18 or to `audit` in the first place.

## Finding 2 — the authority parser was closed-world

**The audit demonstrated it by writing `GITHUB or the external wiki` and watching it pass.** The parser counted occurrences of tokens it already knew, so an undeclared co-authority was invisible: it introduced nothing to count. The same weakness is why the baseline's `or the operational log sink` survived the foundation pass.

**Replaced with a fail-closed grammar.** The authority vocabulary is now **declared in the architecture** (`storage/source-of-truth-matrix.md` §0.1) and **parsed out of it** by the harness rather than duplicated in Python — a hard-coded list is a closed world by construction. Six values: `GITHUB` · `DB` · `OBJECT` · `SECRETS` · `ENV` · `NONE`.

A cell must **be** exactly one declared token written as a bare code span. It fails on a compound or alternative (`or`, `and`, `/`, `,`, fallback, otherwise, either), on an undeclared phrase, on an empty cell, and on prose that merely contains a token. A separate check fails on any telemetry, log, sink, wiki, cache or index word appearing in an authority position, and requires `NONE` and `NOT_A_SOURCE_OF_TRUTH` to imply each other in both directions — so a half-edited row that quietly gives telemetry an authority, or quietly declares an authoritative class to be telemetry, is caught either way round.

## Finding 3 — the conflict-rule check measured length

**The audit passed it a long sentence whose content was that no conflict-resolution rule existed.** The check required ten characters. Length is not a contract.

**Replaced with a structural one.** A conflict outcome vocabulary is declared in §0.2 and parsed from it: nine values — `AUTHORITY_WINS` · `SECONDARY_REBUILT` · `QUARANTINE` · `RECONCILE` · `BLOCK_AND_ESCALATE` · `APPEND_ONLY_NO_CONFLICT` · `NOT_APPLICABLE_NO_SECONDARY` · `NOT_A_SOURCE_OF_TRUTH` · `REGENERATE_DERIVATIVE`.

Every conflict cell must **begin with** one or more declared outcomes and may then explain itself. Prose alone fails regardless of length. An undeclared outcome fails. An empty cell fails. And because last-write-wins is **not** a declared outcome — it is deliberately absent, because it silently discards a governed change — a cell reintroducing it in prose fails, as does any Phase 10 artifact that does — a scan that immediately found one, in `storage/failure-modes.md` mode 9, where the phrase appeared without a denial on its own line.

## Controlled failure probes

Fifteen mutations, each reverted, each exit 1:

| Probe | Result |
|---|---|
| `GITHUB or the external wiki` | `144/146` — authority grammar and telemetry position |
| `DB (bounded metadata) or the operational log sink` | `144/146` — the exact baseline phrase |
| Unknown authority token | `145/146` |
| Empty authority cell | `144/146` |
| Comma-separated dual authority | `145/146` |
| Slash-separated dual authority | `145/146` |
| Empty conflict cell | `145/146` |
| **The audit's adversarial sentence** — a long, well-formed statement that no conflict rule exists | `145/146` |
| Unknown conflict outcome | `145/146` |
| A conflict cell permitting last-write-wins, which the vocabulary does **not** | `145/146` |
| Operational-logs row given a real authority | `145/146` |
| Runtime-metadata row declared not a source of truth | `145/146` |
| Plus the twelve foundation-pass probes (dual master, scalar sensitivity, atomicity claim, committed secret, schema statement, URL, stale totals, missing outcome, inventory drift, RLS as authority, vacuous check) | all still exit 1 |

## Counts, all derived

Source-of-truth rows **24** · authority vocabulary **6** · conflict outcomes **9** · data domains **10** · artifact fields **22** · audit event fields **11** · access dimensions **7** · consistency boundaries **6** · deletion acts **6** · failure modes **15** · adapter boundaries **5** · common constraints **31** · templates **3** · exemplars **5**.

Suite: **143 → 146** checks; `source-of-truth` 8 → 11. The number is what the new checks come to.

## Scope

Conformance and validation only. No governance semantics were introduced, changed or removed; no new Decision Right was invented; no access, sensitivity, residency, audit, retention or failure semantic was weakened; no approved Phase 1–9 artifact was touched. Nothing was connected to, created or deployed. **Phase 10 remains `PROPOSED` and human approval is pending.**
