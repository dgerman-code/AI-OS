# Phase 4 — Final Audit Remediation Record

Status: `PROPOSED — READY FOR FINAL RE-AUDIT`

Branch: `architecture/phase-4-skill-registry`
Preceding record: `reviews/phase-4-wave-3-cross-domain-normalization.md`

The final independent Phase 4 audit returned FAIL on three blockers, all of them internal consistency and evidence accuracy. Role coverage, all five compatibility paths, authority boundaries, the two new Wave 3 cards and the phase boundary all passed and are untouched by this cleanup.

This is a narrow reconciliation. No mapping relationship, trigger, allowlist or Role Card was changed. No new Skill, Specialisation or Pack Card was created. No new normalization wave was started.

---

## 1. Blocker 1 — retired taxonomy still presented as active governing guidance

### 1A. Requirement Traceability Card

File: `skills/legal-compliance-procurement/requirement-traceability.md`

| | Before | After |
|---|---|---|
| Adjacent Skills / Packs | Listed `skill.traceability_matrix_design` — "designs the matrix instrument; this Skill maintains and analyses the linkage" — presenting a retired ID as a live, distinct, adjacent Skill | Line removed. Matrix design is retained as a method of this Skill, where the Methods / Techniques section already carries "matrix granularity design proportionate to criticality" |
| Wave 3 allowlist basis | Named the retired ID without marking it retired | Same migration narrative, now explicitly labelling the identifier retired and tombstoned, and not activatable |
| Wave 2 allowlist basis | "Wave 2 adds `role.project_development_lead` … for transitive Pack compatibility" — contradicted the paragraph directly above it, which records that the Role's only basis was removed in the Wave 2 remediation | Paragraph rewritten to name only the Roles that actually hold a transitive basis: `role.learning_vet_design_specialist` via `skill_pack.cove`, and `role.eu_programme_implementation_grant_management_specialist`, which holds both a direct and a transitive basis |
| Allowlist basis statement | Not stated per-Role | New "Current allowlist basis" subsection stating all 15 Roles by basis class |

The merge-created Knowledge & Evidence Steward mapping basis is preserved unchanged. The allowlist itself was not modified.

**Recomputed basis for all 15 allowlisted Roles** — 11 direct only, 2 direct and transitive, 2 transitive only, 0 orphans, 0 Roles with a basis missing from the allowlist. `role.project_development_lead` holds neither basis and is correctly absent.

### 1B. Master Skill Universe — retired affordability / tariff controls

File: `skills/master-skill-universe.md`

| | Before | After |
|---|---|---|
| Duplication / Granularity Controls | "tariff analysis vs tariff modelling specialisation" and "affordability analysis vs affordability specialisation" listed as pairs that **must remain distinct** — an active instruction to preserve two identifiers the deprecation register on the same page records as retired | Both lines removed. Replaced with explicit normalized guidance: each names a method, not a bounded context; each is represented by the surviving Skill; neither may be recreated as a Specialisation unless a future bounded context distinct from the method is defined |
| Initial Scale inventory | "43 Specialisations" | 41 Specialisations, plus 267 total active entries and 23 retired identifiers, with a note that 43 was stale because it predated the group-14 merges |

### 1B. Architecture files

File: `architecture/skill-registry-design.md`

| Location | Before | After |
|---|---|---|
| §1 Skill examples | "tariff modelling" | "tariff analysis, including modelling the tariff structure itself" — names the surviving Skill |
| §2 Specialisation class examples | "method / metric: DSCR, LLCR, PLCR, tariff modelling, affordability" — an **active definitional example** presenting two retired method-like pseudo-Specialisations as live Specialisation classes | "method / metric: DSCR, LLCR, PLCR — bounded, defined metric conventions, not the methods that compute them", followed by a new paragraph stating that a Specialisation names a bounded context and never a method, recording why the two were retired, and prohibiting their reintroduction |
| §11 Phase 3 seed list | Ended "This is a seed list, not the final registry" — historical, but not labelled as to disposition, so "tariff modelling" and "affordability" still read as live Phase 4 candidates | Labelled a historical Phase 3 seed list and explicitly not a live candidate list, with the disposition of both entries recorded and the Master Skill Universe named as the authoritative inventory. The historical list itself is preserved rather than rewritten |

Other Phase 4 governing files were searched and required no change: `skills/_standards/common-skill-constraints.md`, `architecture/role-to-skill-mapping-rules.md` and the card templates contain no retired-ID examples.

### Global stale-reference scan

Every occurrence of the five Wave 3 retirements across the repository, excluding `prompts/`, classified:

| Retired ID | Hits | VALID HISTORICAL / DEPRECATION | ACTIVE STALE — FIXED |
|---|---:|---:|---:|
| `skill.resource_planning` | 4 | 4 | 0 |
| `skill.insurance_gap_analysis` | 4 | 4 | 0 |
| `skill.traceability_matrix_design` | 9 | 8 | 1 — the Adjacent Skills line (1A) |
| `specialisation.affordability` | 5 | 5 | 0 registry-ID hits; 2 prose hits fixed in the Duplication Controls and the architecture class list |
| `specialisation.tariff_modelling` | 5 | 5 | 0 registry-ID hits; 2 prose hits fixed in the same two places |

The valid historical hits are the surviving Skills' absorption notes, the deprecation register rows, the Wave 2 overlap-candidate and migration tables, the Wave 1 governed-correction section, and the Wave 3 review's own merge record. Each names the retired ID as retired or as history and none instructs future activation.

Stale-claim scan: `43 Specialisations` — 1 hit, fixed. `263` and `92` as capability statistics — fixed in the Wave 3 record. `235 Skills` uncarded — fixed. Phrases "not mapped" / "none is mapped" / "not listed" inside the five cards touched by Wave 2/3 allowlist changes — 4 hits, all fixed under blocker 2; the fifth card, `skills/packs/composite/bid-proposal-management.md`, carries no such claim.

`roles/master-role-universe.md` mentions "tariff modelling, affordability" as examples of metrics and modelling **packs**. That is a Phase 3 artifact, it does not present either as a Specialisation, and it was not modified.

**No active stale reference remains.**

---

## 2. Blocker 2 — four Pack Cards contradicted canonical mappings

In each card an advisory paragraph survived from before the Wave 2 mapping admitted the Roles, and contradicted the allowlist printed a few lines above it. In every case the **mapping record was treated as authoritative and only the prose was changed**. No allowlist was modified; reverse-basis validation shows no defect in any of the four.

| Card | Stale claim | Canonical state | Fix |
|---|---|---|---|
| `skills/packs/methods/project-finance-metrics.md` | Named Funding & Bankability, Project Finance / Transaction and PPP / Concession — all three admitted in the paragraph above — as "none is mapped to this Pack in the current record" | 4 Roles mapped, all 4 listed: Financial Modelling (W1) plus those three (W2), all REQUIRED_FOR_CONTEXT | Paragraph now separates the 4 mapped Roles from `role.ifi_dfi_project_preparation_specialist`, which is substantively relevant but genuinely unmapped and correctly unlisted |
| `skills/packs/programmes/cove.md` | Named `role.learning_vet_design_specialist`, admitted and reasoned for immediately above, as unmapped and unlisted | 3 Roles mapped, all 3 listed: EU Grants (W1, RFC), Learning / VET (W2, RFC), EU Programme Implementation (W2, inside an ALTERNATIVE set) | Paragraph now states the 3 mapped Roles and keeps M&E and Consortium Coordination as relevant-but-unmapped |
| `skills/packs/programmes/life-programme.md` | Named `role.eu_programme_implementation_grant_management_specialist`, admitted and reasoned for immediately above, as unmapped | 2 Roles mapped, both listed: EU Grants (W1, RFC), EU Programme Implementation (W2, ALTERNATIVE) | Paragraph now states both mapped Roles and keeps Grant Financial Compliance and Consortium Coordination as relevant-but-unmapped |
| `skills/packs/technology/supabase.md` | Named Full-Stack, Integration / API, Platform / DevOps and Database / Data Engineer — the four Roles the Wave 2 basis paragraph admits — as "none is mapped … and none is listed" | 6 Roles mapped, all 6 listed: Solution Architect and Data & Database Architect (W1, RFC), Full-Stack, Integration / API and Database / Data Engineer (W2, RFC), Platform / DevOps (W2, ALTERNATIVE) | Paragraph now states the 6 mapped Roles; `role.security_engineer` is identified as the one Role from the old list that genuinely remains unmapped and unlisted |

`role.security_engineer` remains absent from `skill_pack.supabase` and from `skill.quality_attribute_analysis`. No authority, boundary or source section was altered in any of the four cards; the only sentences changed were the factually stale mapping-status paragraphs.

---

## 3. Blocker 3 — stale and incomplete evidence

### 3A. Root cause

The Wave 3 statistics were produced by a parser that read `^- \`id\`` as the only entry form. Two syntaxes the mapping files genuinely use were therefore unread:

1. a **grouped parent bullet** whose members are nested one level below it — "`- one or more sector specialisations:`" followed by eight indented Specialisation IDs, in Technical / Feasibility Lead's REQUIRED_FOR_CONTEXT block. The parent carries no ID, so the parser counted zero instead of eight;
2. the **inline choice pair** "`` - `skill.user_story_design` OR `skill.use_case_modelling` ``" used by the Wave 1 ALTERNATIVE block. The parser captured the first ID only, and in the ALTERNATIVE branch captured neither.

Together these dropped 10 Wave 1 entries (8 REQUIRED_FOR_CONTEXT + 2 ALTERNATIVE) and hid `skill.use_case_modelling` from the usage set. Every discrepancy between the Wave 3 record and the independent audit traces to this one cause. **The audit's figures were correct; the earlier record's were not.** The parser now reads both forms, and the reconciliation reproduces each audited figure exactly.

### 3B. Recomputed statistics

Universe, from active declarations:

| | Value |
|---|---:|
| Active Skills | 205 |
| Active Specialisations | 41 |
| Active Packs | 21 |
| Total active entries | 267 |
| Retired / tombstoned IDs | 23 |

Mapping entries, from relationship blocks:

| | Wave 1 | Wave 2 | Combined |
|---|---:|---:|---:|
| REQUIRED_CORE | 52 | 188 | 240 |
| REQUIRED_FOR_CONTEXT | 61 | 230 | 291 |
| OPTIONAL | 32 | 192 | 224 |
| ALTERNATIVE | 2 | 56 | 58 |
| PROHIBITED_IN_CONTEXT | 0 | 10 | 10 |
| **Total** | **147** | **676** | **823** |

ALTERNATIVE choice sets: 11. REQUIRED_CORE per Role: min 2, max 8, average 4.07. Roles covered: 59, each exactly once.

Usage:

| | Value |
|---|---:|
| Unique capability IDs in positive use | 264 |
| — Skills / Specialisations / Packs | 205 / 38 / 21 |
| Used by exactly one Role | 93 (35.2%) |
| Declared but not positively mapped | 3 — `specialisation.dscr`, `specialisation.llcr`, `specialisation.plcr` |

The three unmapped Specialisations are required components of `skill_pack.project_finance_metrics` and reach Roles through it. They are not orphans.

Card coverage, counted from the card files:

| | Carded | Declared | Uncarded |
|---|---:|---:|---:|
| Skills | 6 | 205 | 199 |
| Specialisations | 1 | 41 | 40 |
| Packs | 5 | 21 | 16 |
| **Total** | **12** | **267** | **255** |

Distinct declared Pack components: 32, of which 28 are uncarded.

Corrections applied to `reviews/phase-4-wave-3-cross-domain-normalization.md`:

| Claim as published | Corrected to |
|---|---|
| 263 capability IDs in active use | 264 |
| 92 single-role IDs (35.0%) | 93 (35.2%) |
| 95 single-role before Wave 3 (35.8%) | 96 (36.1%), recomputed from commit `7facd10` |
| 235 Skills uncarded | 199 |
| Wave 1 and combined entry counts absent | 147 / 823, with the full relationship split |
| `skill.use_case_modelling` recorded as used by no Role | Mapped, inside the Wave 1 ALTERNATIVE choice set on `role.product_manager_business_analyst` |

### 3C. Wave 2 narrative counts

File: `skills/mappings/wave-2-domain-completion-role-skill-mapping.md`

| Claim | Actual block | Fix |
|---|---|---|
| Software QA gap row: "Left unmapped; core kept at two capabilities as a result" | Core is **3**: `skill.test_automation`, `skill.acceptance_criteria_design`, `skill.defect_management` | Row marked superseded by Wave 3, which added `skill.defect_management` and raised the core to three |
| Insurance migration row: "core reduced from 3 to 2" | Core is **2**: `skill.insurance_programme_analysis`, `skill.risk_identification` | The "3" is the correct pre-merge figure — verified against commit `7facd10`, where the core carried three entries — so the row is history, not an error. It is made unambiguous by naming the current core explicitly, so the 3 cannot be read as a current count |
| "4 universe entries are declared but used by no Role", listing `skill.use_case_modelling` | 3 entries, all Pack components | Corrected to 3, with the reason `skill.use_case_modelling` was wrongly listed |

No mapping relationship was changed to make prose true.

---

## 4. Exhaustive duplicate Pack/direct activation

The Wave 3 record described five narratively examined cases as an exhaustive normalization. It was a subset. A mechanical detector now enumerates every path from the Wave 1 and Wave 2 relationship blocks against the component declarations on the five Pack Cards, plus the three metric components the Master Skill Universe declares for `skill_pack.project_finance_metrics`.

Definition: a path exists where a Role is mapped a Pack in any positive relationship **and** is separately mapped, in any positive relationship, a Skill that Pack declares as a component.

| Measure | Count |
|---|---:|
| Required-component overlap paths | 20 |
| Unique Role–Skill pairs among them | 14 |
| Unique Skills among them | 10 |
| Optional-component overlap paths | 36 |
| All required + optional paths | 56 |

These reproduce the independent audit's 20 / 14 / 10 / 56 exactly. Paths exceed pairs because a Role can reach one Skill through two Packs at once — six such doubled paths, five of them on the EU programme Packs.

By Pack, required: CoVE 5, LIFE 5, Bid / Proposal 4, Project Finance Metrics 4, Supabase 2. Optional: Supabase 17, Bid / Proposal 5, LIFE 5, Project Finance Metrics 5, CoVE 4.

Disposition, recorded in full in the Wave 3 record's section 5: all 56 resolve to a **single activation under the stricter obligation** with the Pack's constraints applied on top, per `standard.skill.common_constraints` §6.1b. Every direct mapping is retained because in every case it has meaning independent of the Pack. The 36 optional-component paths create no duplicate obligation at all, since an optional component imposes none; they are recorded for reproducibility.

**No direct mapping was removed to lower the count.** One watch item is carried forward: `skill.project_finance_ratio_analysis` and `skill.debt_schedule_modelling` are held directly by four Roles alongside the metrics Pack, and if no assignment ever needs them Pack-free the direct mappings should be withdrawn.

---

## 5. Compatibility and authority after cleanup

All five paths re-run against every existing card:

| Path | Direction | Result |
|---|---|---|
| direct Role → Skill | forward | 0 conflicts |
| direct Role → Specialisation (carded) | forward | 0 conflicts |
| direct Role → Skill Pack | forward | 0 conflicts |
| transitive Pack → component Skill | forward | 0 conflicts |
| allowlist entry → mapping basis | reverse | 0 orphans |

Bounded by coverage: 255 of 267 active capabilities have no card and remain **NOT YET VALIDATABLE**, not passes.

Preserved boundaries, re-verified after the edits:

- `role.security_engineer` is absent from `skill.quality_attribute_analysis` and from `skill_pack.supabase`;
- `skill.lifecycle_cost_analysis` remains support-only to `role.technical_feasibility_lead` — the card is byte-identical to its pre-cleanup state and its allowlist holds exactly that one Role;
- all 59 Phase 3 Role Cards are unchanged;
- every Phase 4 artifact remains `PROPOSED`;
- no model, runtime, orchestration, database or workflow implementation was introduced.

---

## 6. Remaining non-blocking notes

1. **Card coverage is still the dominant limitation.** 12 cards against 267 active capabilities. Every "zero conflicts" result is bounded by it, and the reverse-basis check can only test the 12.
2. **The three metric Specialisations reach Roles only through their Pack.** `specialisation.dscr`, `specialisation.llcr` and `specialisation.plcr` are correct as Pack components, but the METRIC Specialisation class now has no direct mapping anywhere. A future review should confirm the class earns its place rather than assume it.
3. **Watch item on `skill.project_finance_ratio_analysis` and `skill.debt_schedule_modelling`** — carried over from Wave 3, restated in section 4 above.
4. **Eight single-consumer capabilities flagged but not merged** — the AI / Knowledge Systems cluster and `skill.sanctions_screening` versus `skill.counterparty_screening`. Each needs its own Role-boundary review.
5. **35.2% single-role use** remains a watch metric, not a defect: 48 of 59 Roles have had exactly one mapping opportunity.
6. **The parser blind spots described in 3A are a governance lesson, not only a bug.** Any future audit of these files must read grouped parent bullets and inline choice pairs, or it will silently undercount Wave 1. The validation specification in `skills/_standards/common-skill-constraints.md` should absorb this before mass generation.

---

## 7. Standing statement

Everything above is `PROPOSED`. Nothing in the Skill Registry is APPROVED or CANONICAL, and this record does not claim human approval. Mass generation of cards remains prohibited and is not recommended: 255 uncarded capabilities against 12 cards is the reason the compatibility results are bounded, and the answer to that is selective carding driven by real assignments, not volume.
