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

**One defect, and it was in the harness.** The previous pass rejected `IGNORE_AS_STALE`, the discard vocabulary, and the exact phrase `treated as stale` — a **word list**, and a word list only knows the words someone thought of. The re-audit wrote <!-- stale-specimen -->`The Decision Record stands but is stale`<!-- /stale-specimen --> and it passed: the row still said the record stands, still carried `RECONCILE`/`ESCALATE`, and named no forbidden word.

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

Rejected at minimum: <!-- stale-specimen -->`is stale` · `was stale` · `becomes stale` · `considered stale` · `deemed stale` · `marked stale` · `treated as stale` · `stale Decision Record`<!-- /stale-specimen -->.

**The architecture row is unchanged.** The audit was right that committed content is correct; this was validator coverage.

## The rule, executed rather than described

A third check feeds the matcher its own cases — twelve of them, each asserted against **both** scopes — including the audit's exact bypass. Relaxing the patterns fails it **without any document being edited**, which is the property the previous word list did not have.

## Probes

| Probe | Exit |
|---|:--:|
| <!-- stale-specimen -->`The Decision Record stands but is stale`<!-- /stale-specimen --> — the exact bypass, now **rejected** | 1 |
| <!-- stale-specimen -->`was deemed stale` · `stale Decision Record` · `considered stale` · `marked stale` · `becomes stale` · `treated as stale`<!-- /stale-specimen --> — each **rejected** | 1 each |
| `IGNORE_AS_STALE` + discarded | 1 |
| `voided` | 1 |
| `RECONCILE`/`ESCALATE` removed | 1 |
| Late review loses `IGNORE_AS_STALE`, or is no longer recorded against its Review Instance | 1 each |
| **Control** — retained + `RECONCILE` + `ESCALATE` | **0** |
| **Control** — the row says the record is **not** stale | **0** |
| **Control** — stale *evidence* prose elsewhere in Phase 11 | **0** |

The twelve foundation probes were re-run and all still exit 1.

Suite **151 → 153**; `concurrency` 9 → 11. **Phase 11 remains `PROPOSED`; human approval is pending.**

---

# Negation-scope remediation — a negation may only speak for its own predicate

Approval re-audit of `7b61d1125485b49f9d9f05282506f698b76367a4`: **FAIL**, one remaining HIGH validator defect.

**One defect, and it was mine again.** The previous pass replaced a forbidden-word list with predications — correct — and then added a **proximity-based** negation suppressor: any `not`, `never`, `no longer`, `neither` or `nor` within forty characters cancelled the match. The re-audit wrote <!-- stale-specimen -->`The Decision Record stands and is not optional but is stale`<!-- /stale-specimen -->.

The negation belongs to `optional`. The staleness is asserted anyway, and both checks passed. The Phase-11-wide check had the same shape of hole from a different direction: a line-wide denial exemption, where a denial anywhere on the line suppressed a positive stale predicate later in it.

Three versions of this rule, three bypasses, and the same root cause each time: **the check tested something near the rule instead of the rule.** First a word, then a distance, and only now the grammar.

## The rule

> **A negation suppresses a stale characterisation only when it is attached to the stale predicate itself.**

There is no lookback window and no line-wide denial exemption; both were ways for a negation elsewhere in a sentence to speak for a predicate it does not govern.

| Passes | Fails |
|---|---|
| `The Decision Record is not stale` | <!-- stale-specimen -->`...stands and is not optional but is stale`<!-- /stale-specimen --> |
| `The Decision Record was not stale` | `...is not optional and is stale` |
| `The Decision Record is never stale` | `...is not ignored but is stale` |
| <!-- stale-specimen -->`This is not a stale Decision Record`<!-- /stale-specimen --> | <!-- stale-specimen -->`...is neither optional nor revocable but is stale`<!-- /stale-specimen --> |
| Stale **evidence**, unrelated to a Decision Record | `...is no longer pending but is stale` |
| Late review `IGNORE_AS_STALE`, recorded against its Review Instance | `...is never discarded, but is stale` |

## Implementation

The negator slot sits **inside** each pattern, immediately before `stale`: a negative lookahead after the copula, and fixed-width lookbehinds for the adjectival and participle forms. A negation in that slot suppresses; a negation anywhere else does not reach. Standard library only, deterministic, four regex branches.

Where the phase-wide scan previously exempted a whole line on a denial marker, it now reads **prose only**: a wording quoted as a code span is a specimen someone is rejecting rather than an assertion, and the authoritative row is deliberately **not** given that latitude — there, a specimen has no business appearing at all.

## The guard against reverting

The grammar self-check now carries **22 cases**, each asserted against both scopes, including all six contrastive forms. Proximity-based suppression passes every contrastive case; predicate-attached suppression fails every one. **Reinstating proximity suppression therefore fails the harness with no document edited** — verified by doing it: the check failed and nothing else did.

## Probes

| Group | Result |
|---|---|
| Six contrastive forms in the authoritative row | exit 1 each — row check **and** phase-wide check |
| Two contrastive forms inserted as prose elsewhere in Phase 11 | exit 1 each — phase-wide check |
| Four positive controls — `is not stale`, retained + `RECONCILE`/`ESCALATE`, unrelated stale evidence, late review `IGNORE_AS_STALE` still recorded | **exit 0 each** |
| Twelve prior stale-wording probes | exit 1 each |
| Twelve foundation probes | exit 1 each |
| Negation logic reverted to proximity | exit 1 — the grammar guard |

**No architecture content changed.** The committed row was correct before this pass and is byte-identical after it. Suite total unchanged at **153**. **Phase 11 remains `PROPOSED`; human approval is pending.**


---

# Inline-code remediation — formatting is not semantics

Approval re-audit: **MEDIUM**, one remaining validator defect. All negation-scope findings resolved; committed architecture correct.

**One defect, and it was mine — introduced by the previous fix.** To let a review record quote a rejected wording, I made the Phase-11-wide scan delete inline code spans. That treats a **typographic choice** as a **statement by an author**, and the re-audit showed what it buys someone who does not want to be caught: backticks around one word, or around half the subject, delete exactly the text the invariant needs to read.

Both of these passed, and neither is a quotation of anything:

| Bypass | Why it worked |
|---|---|
| <!-- stale-specimen -->`The Decision Record is ``stale``.`<!-- /stale-specimen --> | The predicate was deleted before matching |
| <!-- stale-specimen -->`The Decision ``Record`` is stale.`<!-- /stale-specimen --> | The subject was split, so the bridge never formed |

This is the fourth bypass of the same invariant, and the fourth time the check tested something adjacent to the rule: a word, then a distance, then a grammatical scope — and this time a **rendering**.

## The rule

> **Formatting is not semantics. A prose assertion predicating staleness of a Decision Record is rejected whether its tokens are plain, wrapped, or split by inline code.**
>
> **An exemption must be claimed explicitly, and a backtick claims nothing.**

## Implementation

Markup is **normalised, never deleted**: `plain()` removes every formatting marker while preserving the text it wrapped, so a wrapped or split word reads exactly as the sentence means it. `prose_only()` and its span-deletion regex are gone.

A specimen now claims its exemption in a fence that says what it is — `<!-- stale-specimen -->` … `<!-- /stale-specimen -->` — invisible when rendered, explicit in source, and **available to review records only**. A check asserts that **no document under `orchestration/` or `architecture/` opens one**: there, a specimen has no business appearing at all. This record uses the fence, which is why the wordings above can be quoted at all.

## Self-guards

Seven inline-code cases were added to the grammar table, and every case in it now reads through the **real** normalisation path rather than a raw string. A new check asserts the rule from both ends: an inline-code assertion **must** be caught, an explicitly fenced one **must not** be, normalisation must leave no marker and drop no text, and no architecture document may claim the fence.

Three weakenings were applied and reverted, each failing the harness with **no document edited**:

| Weakening | Result |
|---|---|
| Code-span deletion reintroduced | exit 1 — grammar table **and** the formatting check |
| Specimen fence widened to accept any code span | exit 1 — both |
| Negation logic reverted to proximity | exit 1 — grammar table |

## Probes

Six inline-code forms inserted as prose — stale in code, subject half in code, subject wholly in code, every token in code, `deemed` with stale in code, and the adjectival form — **exit 1 each**.

Four positive controls — `The `Decision Record` is not stale`, unrelated stale evidence, inline code making no stale-Decision assertion, and late review `IGNORE_AS_STALE` still recorded against its Review Instance — **exit 0 each**.

Eight contrastive-negation probes, twelve prior stale-wording probes and twelve foundation probes were re-run: **exit 1 each**.

## Scope

**No architecture content changed** — `orchestration/` and `architecture/` are byte-for-byte identical. Suite **153 → 154**; `concurrency` 11 → 12. **Phase 11 remains `PROPOSED`; human approval is pending.**

---

# Markdown-formatting remediation — emphasis is not semantics either

Approval re-audit: inline-code, negation-scope and specimen-fence findings resolved; **one Markdown-formatting bypass remained.**

**The fifth bypass of the same invariant.** The previous pass normalised markup instead of deleting it — correct — but normalised only what the suite's shared `plain()` happens to strip: `**` and backticks. Emphasis and strikethrough went untouched, so the governed subject could still be split:

| Bypass | Why it worked |
|---|---|
| <!-- stale-specimen -->`The Decision *Record* is stale.`<!-- /stale-specimen --> | Asterisks survived, so the subject never read as `Decision Record` |
| <!-- stale-specimen -->`The Decision _Record_ is stale.`<!-- /stale-specimen --> | Same, with underscores |
| <!-- stale-specimen -->`The Decision ~~Record~~ is stale.`<!-- /stale-specimen --> | Same, with strikethrough |

Each earlier fix closed the shape it was shown and left the next rendering open: a word, a distance, a grammatical scope, one rendering, then the rest of them. What was missing throughout was a check on **the reading path itself** rather than on the phrase of the week.

## The rule

> **Formatting is not semantics. A prose assertion predicating staleness of a Decision Record is rejected regardless of any supported Markdown inline formatting around or within its tokens.**

## Implementation

`plain()` is **not** widened. It is the suite's general normaliser, used in roughly a hundred checks, and stripping underscores broadly would destroy the vocabulary this architecture is written in — `IGNORE_AS_STALE`, `NON_RETRYABLE_GOVERNED_ACT`, `GOVERNANCE_CLEAR`. Architecture correctness outranks convenience, so this invariant gets its own narrowly-scoped normaliser.

`semantic_text()` removes every supported marker — inline code, `*…*`, `_…_`, `**…**`, `__…__`, `~~…~~` — and **never removes enclosed text**. Markers are removed rather than matched as pairs, so an unbalanced, overlapping or nested marker cannot survive as a token splitter either. An underscore **between two alphanumerics is an identifier character and is kept**, which is what lets `_Record_` normalise away while `IGNORE_AS_STALE` survives intact.

Both scopes read through it: the Phase-11-wide scan, and — through a named `race_row_cells()` helper — the authoritative row.

## Self-guards

Fifteen formatting cases were added to the grammar table, at least one per marker class plus mixed and nested forms, and the formatting check now asserts each class twice: the marker must go, the enclosed text must stay, and an assertion wearing it must still be caught. The declared vocabulary is asserted to survive normalisation.

Seven weakenings were applied and reverted, each failing the harness with **no document edited**:

| Weakening | Result |
|---|---|
| Code-span deletion reintroduced | exit 1 |
| Specimen fence widened to any code span | exit 1 |
| Negation reverted to proximity | exit 1 |
| Strikethrough no longer normalised | exit 1 |
| Asterisk emphasis no longer normalised | exit 1 |
| Underscore emphasis no longer normalised | exit 1 |
| The authoritative row's reading path reverted to `plain()` | exit 1 |

The last one is worth recording honestly: **it passed at first.** The guards watched the helper functions but not the path the row is actually read through, and the committed row carries no formatted stale text, so the revert was invisible. A guard on half the rule is a guard that reports confidence it has not earned — so the reading path was named and is now asserted directly.

## Probes

Eight negative formatting probes — subject split by `*`, `_`, `**`, `__` and `~~`, whole subject emphasised, predicate emphasised, and a mixed form across both — **exit 1 each**.

Four positive controls — formatted attached negation `The *Decision Record* is not _stale_.`, formatted stale **evidence** unrelated to a Decision Record, late review `IGNORE_AS_STALE` retained against its Review Instance, and an additional allowed specimen fence in a review record — **exit 0 each**.

Every prior suite was re-run: six inline-code probes, twelve stale-wording probes, eight contrastive-negation probes and twelve foundation probes including the vacuity probe — **exit 1 each**.

## Scope

**No architecture content changed** — `orchestration/` and `architecture/` are byte-for-byte identical. Suite unchanged at **154**. **Phase 11 remains `PROPOSED`; human approval is pending.**

---

# Rendered-text remediation — links and inline HTML render away too

Approval re-audit: architecture semantics correct; **one Markdown/HTML rendering bypass remained.**

**The sixth bypass of the same invariant.** The previous pass normalised inline code, `*`, `_`, `**`, `__` and `~~` — every marker it had been shown. Two rendering mechanisms it had not been shown still split the governed subject:

| Bypass | Why it worked |
|---|---|
| <!-- stale-specimen -->`The Decision [Record](#term) is stale.`<!-- /stale-specimen --> | Link syntax survived, so the subject never read as `Decision Record` |
| <!-- stale-specimen -->`The Decision <em>Record</em> is stale.`<!-- /stale-specimen --> | Inline HTML tags survived |
| <!-- stale-specimen -->`The Decision <code>Record</code> is stale.`<!-- /stale-specimen --> | Same, and indistinguishable from a code span once rendered |

Six passes, six bypasses, and the shape of the mistake has been constant: **each fix enumerated the wrappers it had been shown, and the next reviewer brought a different one.** A marker list is a word list wearing different clothes.

## The rule

> **For this invariant the validator evaluates rendered semantic text, not raw Markdown. A prose assertion predicating staleness of a Decision Record is rejected regardless of any supported inline presentation wrapper.**

## Implementation

`semantic_text()` gains two transformations, both of the same shape as the existing ones — **remove presentation, keep visible text**:

- **Markdown links**, inline and reference: `[visible text](target)` and `[visible text][ref]` render to `visible text`. Only the destination syntax is discarded, because nobody reads a destination.
- **Inline HTML tags**: any `<tag …>` or `</tag>` is removed and its inner text kept. Removed rather than matched as pairs, so an unclosed or mismatched tag cannot survive as a token splitter either.

`plain()` is still untouched — it remains the suite's general normaliser for the other 150 checks, and this invariant keeps its own.

Every transformation in `semantic_text()` now satisfies one invariant of its own: **it removes presentation and never removes content.** Normalisation can therefore only join tokens that formatting split; it can hide nothing.

## Self-guards — the reading path, not the phrase list

Twelve rendering cases were added to the grammar table, but the substantive change is that the **rendering rules are now asserted directly** rather than only through example phrases:

- a link must render to its visible text alone, inline and reference forms;
- an HTML tag must be removed and its inner text kept, attributes included;
- an **unbalanced** tag must not survive as a splitter;
- the authoritative row's reading path must normalise emphasis, links **and** inline HTML — three synthetic rows, asserted through the real `race_row_cells()` helper;
- **both scopes must normalise identically** — the same sample read as a document and as a row cell must produce the same text.

That last one is the guard the earlier passes were missing. The previous remediation discovered, by probe, that reverting the row path alone was invisible; this asserts the two paths agree, so they cannot drift apart at all.

Eleven weakenings were applied and reverted, each failing the harness with **no document edited**: link normalisation removed · inline-HTML normalisation removed · reference-link normalisation removed · row path reverted to raw Markdown · document scan reverted to raw Markdown · specimen widened to ordinary formatting · code-span deletion reintroduced · strikethrough dropped · asterisk emphasis dropped · underscore emphasis dropped · negation reverted to proximity.

## Probes

Nine negative rendering probes in architecture prose — subject in a link, whole subject in a link, predicate in a link, subject in `<em>`, `<strong>`, `<code>` and `<span>`, HTML across subject and predicate, and a mixed Markdown + HTML + inline-code form — **exit 1 each**. Two more against the **authoritative row's** reading path, one link-wrapped and one HTML-wrapped — **exit 1 each**.

Six positive controls — plain attached negation, HTML-wrapped attached negation, unrelated stale evidence, a benign link and inline HTML asserting nothing, late review `IGNORE_AS_STALE` retained against its Review Instance, and an additional allowed specimen fence — **exit 0 each**.

Every prior suite was re-run: eight emphasis/strong/strikethrough probes, six inline-code probes, twelve stale-wording probes, eight contrastive-negation probes and twelve foundation probes including the vacuity probe — **exit 1 each**.

## Scope

**No architecture content changed** — `orchestration/` and `architecture/` are byte-for-byte identical, so no stop-and-report was required. Suite unchanged at **154**. **Phase 11 remains `PROPOSED`; human approval is pending.**

---

## A note on the specimen fence

This record quotes wordings in order to reject them. Since the inline-code remediation, the
validator **normalises** Markdown rather than deleting code spans — formatting is not
semantics, and a backtick is a typographic choice rather than a statement by an author. A
quotation must therefore claim its exemption explicitly, between `<!-- stale-specimen -->` and
`<!-- /stale-specimen -->`.

The fence is available to **review records that quote rejected wordings**. It is not available
to the authoritative race row, and no architecture document under `orchestration/` or
`architecture/` uses it: there, a specimen has no business appearing at all.
