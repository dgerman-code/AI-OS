# Phase 11 — Late Decision Race Validator Remediation

Status: PROPOSED — targeted Phase 11 remediation record

## Independent audit finding

The independent foundation audit returned **FAIL** with one HIGH validator finding: the
authoritative late-Decision race row could be changed to `IGNORE_AS_STALE` and say that the
Decision Record was discarded while the validator still passed on positive prose elsewhere.

## Targeted change

`validation/phase_11_validation.py` now parses the authoritative race table and requires:

- exactly one late-Decision race row;
- no `IGNORE_AS_STALE` outcome for that row;
- `RECONCILE` and/or `ESCALATE` current-state handling;
- wording that the Decision Record stands or is retained;
- rejection of wording that discards, ignores, drops, erases, voids or treats the Decision
  Record as stale.

The architecture row itself is unchanged. The Decision Record remains in append-only governed
history; only its effect on current execution state is reconciled or escalated.

## Intentional asymmetry preserved

The same structured check requires the late-review row to retain `IGNORE_AS_STALE` and to keep
the review recorded against its Review Instance. A late review is an assessment of superseded
work. A late Decision Record is an authority-bearing governed act that occurred. They remain
different cases.

## Adversarial verification

All 17 controlled mutations from the independent audit were applied separately and reverted.
Each produced a non-zero Phase 11 validator exit for its intended reason. In particular, the
exact formerly missed mutation — changing the authoritative late-Decision row to
`IGNORE_AS_STALE` and saying the Decision Record was discarded — is now rejected by the
structured late-Decision assertion.

## Validation

- Phase 11 default: **151/151 PASS**
- Phase 11 verbose: **151/151 PASS**
- Phase 11 JSON: **151/151 PASS**
- Phase 10: **145/147**, the unchanged inherited approval-record-only validator defect
- Phase 9: **277/277 PASS**
- Phase 8: **119/119 PASS**

No Phase 10 validator or approval record was changed. All Phase 11 architecture remains
`PROPOSED`; no runtime or infrastructure was introduced.

---

# Final targeted remediation — a late Decision Record may not be called stale

Approval re-audit: **FAIL**, one remaining HIGH validator gap.

**One defect, and it was in the harness.** The previous pass rejected `IGNORE_AS_STALE`, the discard vocabulary, and the exact phrase `treated as stale` — a **word list**, and a word list only knows the words someone thought of. The re-audit wrote `The Decision Record stands but is stale` and it passed: the row still said the record stands, still carried `RECONCILE`/`ESCALATE`, and named no forbidden word.

That wording is the whole failure in miniature. Staleness is a property a coordinator would be **assigning to a governed act that occurred** — and a record that stands while being stale is a record nobody has to act on, which is exactly the outcome this race case exists to refuse.

## The rule

A late Decision Record:

- **remains a valid authority-bearing governed historical fact** — it stands, or is retained;
- **may require `RECONCILE` and/or `ESCALATE`** for current-state handling;
- **may not be ignored or discarded**;
- **may not be characterised as stale itself** merely because the execution state changed.

The asymmetry with a late **review** result is preserved deliberately and is checked in the same place: `IGNORE_AS_STALE` remains correct there, with the result recorded against its Review Instance. A review is an assessment of superseded work. A Decision Record is an act that happened.

## Predication, not a word ban

The check moved from listing phrases to matching **predications of staleness** — constructions in which staleness is asserted *of* something. At two widths, deliberately:

| Scope | Width | Why |
|---|---|---|
| **The authoritative late-Decision race row** (its outcome and reason cells) | Broad: any predication of staleness at all | It is two cells of one row, where a sentence about anything being stale does not belong |
| **Every Phase 11 artifact** | Narrow: the predication must **name a Decision Record** | So that stale **evidence** — a real and blocking condition in this architecture — is never touched |

A negation immediately before a predication inverts it, so "the Decision Record is **not** stale" is the correct characterisation and passes. The declared vocabulary token `IGNORE_AS_STALE` is scrubbed before matching, so the row may still reference the contrast without tripping the rule.

Rejected at minimum: `is stale` · `was stale` · `becomes stale` · `considered stale` · `deemed stale` · `marked stale` · `treated as stale` · `stale Decision Record`.

**The architecture row is unchanged.** The audit was right that committed content is correct; this was validator coverage.

## The rule, executed rather than described

A third check feeds the matcher its own cases — twelve of them, each asserted against **both** scopes — including the audit's exact bypass. Relaxing the patterns fails it **without any document being edited**, which is the property the previous word list did not have.

## Probes

| Probe | Exit |
|---|:--:|
| `The Decision Record stands but is stale` — the exact bypass, now **rejected** | 1 |
| `was deemed stale` · `stale Decision Record` · `considered stale` · `marked stale` · `becomes stale` · `treated as stale` — each **rejected** | 1 each |
| `IGNORE_AS_STALE` + discarded | 1 |
| `voided` | 1 |
| `RECONCILE`/`ESCALATE` removed | 1 |
| Late review loses `IGNORE_AS_STALE`, or is no longer recorded against its Review Instance | 1 each |
| **Control** — retained + `RECONCILE` + `ESCALATE` | **0** |
| **Control** — the row says the record is **not** stale | **0** |
| **Control** — stale *evidence* prose elsewhere in Phase 11 | **0** |

The twelve foundation probes were re-run and all still exit 1.

Suite **151 → 153**; `concurrency` 9 → 11. **Phase 11 remains `PROPOSED`; human approval is pending.**
