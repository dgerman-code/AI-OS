# Phase 9 — Model Registry and Router Foundation Audit Remediation

Status: PROPOSED — READY FOR FINAL INDEPENDENT PHASE 9 RE-AUDIT

Branch: `architecture/phase-9-model-registry-router`
Audited foundation baseline: `212f42e4453033d63b761fe6c19c63538ce772d8`
Phase 8 approval-record baseline: `00fb92e1b2dd1209ee2f69550c5962158b881e3e`

The independent Phase 9 foundation audit returned **FAIL** with 5 HIGH and 7 MEDIUM findings. **Every one was genuine.** None is contested, and two of them — H3 and H5 — identify places where the architecture contradicted either an approved upstream phase or itself.

---

## H1 — Model Profile identity granularity

**Finding.** The template and lifecycle docs did not distinguish underlying model version, provider-hosted variant, provider alias, registry profile version and the provider/deployment relationship. A runtime would have to guess whether a provider variant is the same underlying model, a different release, or a renamed catalogue entry.

**Status: RESOLVED.** A six-layer identity stack, `models/model-lifecycle-and-versioning.md` §0:

| # | Layer | Identified by |
|---:|---|---|
| 1 | Model Family | `family.<stable_name>` |
| 2 | **Underlying Model Release** | The originator's release identity — **recorded, never the registry ID** |
| 3 | Model Profile | `model.<stable_snake_case_name>` |
| 4 | **Registry Profile Version** | `v<n>` on the record — **not the model's version** |
| 5 | **Provider Offering Mapping** | A bounded mapping inside the Provider Profile |
| 6 | Deployment Profile | `deployment.<stable_snake_case_name>` |

**Provider Offering is a mapping, not a seventh registry object**: it has no lifecycle, no capability claims and no governance properties that are not already the Provider's or the Deployment's. Seven rules follow, of which three carry the weight: a registry profile version moves **independently** of the model's; one profile may map to several provider/deployment combinations **only where they expose the same underlying release, evidenced**; and where provider-specific behaviour is materially different and cannot be evidenced as the same release, it is a **distinct Model Profile**, never an ambiguous mapping.

**Data-handling posture was removed from Model Profile entirely** — see M7. A historical Routing Decision now preserves **both** the profile version and the mapping used, because either alone under-determines what ran.

---

## H2 — Candidate universe not reproducible

**Finding.** "Candidate set where practical" is not auditable and cannot detect accidental omission. Flagged as a human-approval blocker.

**Status: RESOLVED.** `models/routing-precedence-and-fallback.md` §1: **every Routing Decision binds a Candidate Universe Definition before any filtering or ranking occurs** — a deterministic registry state reference (**not a timestamp alone, which reconstructs nothing**), a universe definition version, an inclusion rule, the routing scope, pre-filter exclusions, the enumerated set, omission reasons, and a completeness result.

Three rules the phrase "where practical" was hiding:

1. **Outside the universe and ineligible inside it are different exclusions**, separately recorded. A candidate appearing in neither list is the defect this makes impossible.
2. **Availability does not remove a candidate from the universe.** An `UNAVAILABLE` candidate is enumerated, evaluated and excluded **with availability named** — so the record distinguishes "a compliant option existed and was unreachable" from "no compliant option existed". Pre-enumeration availability filtering is permitted **only** where the policy declares it explicitly.
3. **A load failure never silently shrinks the universe.** It yields **`CANDIDATE_UNIVERSE_INCOMPLETE`**, and the policy declares `BLOCK` or `ESCALATE`. This is the failure mode that is invisible from the inside: a router that enumerated three of five and picked the best of three produces a record indistinguishable from a correct decision — **unless the universe was bound first**.

A bounded universe is permitted; an unexplainable one is not.

---

## H3 — Ordinal sensitivity model was invalid

**Finding.** Phase 8 sensitivity is multi-valued and orthogonal; Phase 9 treated it as one scalar maximum compared "at or above".

**Status: RESOLVED.** The audit was right, and the repository evidence is explicit: Phase 8 states that an item "may carry several" labels, that `PERSONAL_DATA` "carries obligations independent of every other class here", and that restrictions from `PRIVILEGED` or `THIRD_PARTY_RESTRICTED` "cannot be relaxed by an internal decision at all". **There is no total order to compare against**, and `MAX_DATA_SENSITIVITY_ALLOWED` was asking a question Phase 8 does not answer.

Replaced by a **set-compatibility model** (`models/routing-constraint-model.md` §3): `SUPPORTED_SENSITIVITY_CLASSES`, `PROHIBITED_SENSITIVITY_CLASSES`, `REQUIRED_HANDLING_CONTROLS`, `REQUIRED_DATA_HANDLING_POSTURE`.

> **A deployment is eligible only if every applicable label is explicitly supported, every handling obligation those labels impose is satisfied, and no prohibited condition applies.**

A **subset test with obligations**, not a comparison: `PERSONAL_DATA + PRIVILEGED` requires **both** regimes; `TRADE_SECRET` support implies nothing about `PERSONAL_DATA`; **no label outranks another, because there is no higher**; **unknown support is not support**; a prohibition wins over any support; and compound material takes the **union** of obligations under Phase 8's most-restrictive rule.

**Phase 8's semantics are used exactly as written and are not redefined.**

---

## H4 — Residency semantics incomplete

**Status: RESOLVED.** Deployment-level residency now carries exact jurisdiction(s), a region/residency class with five values, a **class-to-jurisdiction mapping**, cross-border processing (`FORBIDDEN` / `CONDITIONAL` / `ALLOWED`), **`UNKNOWN_RESIDENCY`**, and evidence with a review-by.

Five rules: **`UNKNOWN_RESIDENCY` never satisfies a residency requirement** and is never read as "probably fine"; **prohibited outranks allowed**, and an overlap is a defect to correct rather than resolve case by case; **exact jurisdiction and region class are not interchangeable** without an explicit declared mapping; **provider-level claims constrain but never substitute** for deployment-specific evidence; and **cross-border processing is assessed separately** from the primary jurisdiction, since a compliant primary region with unbounded cross-border processing satisfies nothing.

---

## H5 — Fallback, eligibility and exception contradicted each other

**Finding.** Exemplar 9 called a `BASELINE` candidate eligible despite a `STRONG` requirement, then used a Phase 7 exception because the requirement was unmet.

**Status: RESOLVED.** The contradiction was real. `models/routing-precedence-and-fallback.md` §5 separates three cases:

| | Requirement met? | Governed act? | Eligible? |
|---|---|---|---|
| **A — ordinary fallback** | Yes, all of them | No | Yes, under the policy |
| **B — exception-adjusted** | No, then adjusted | **Yes, before re-evaluation** | Yes, **under the adjusted context only** |
| **C — non-waivable failure** | No, and unadjustable | Not available | **No. Blocked** |

Case B runs in a fixed order: the candidate **is ineligible and that is recorded**; the constraint's exceptionability class is checked; a **named, valid Phase 7 Right whose scope covers that class** is exercised, producing a bounded, expiring **adjusted routing context**; and only then is eligibility **re-evaluated against the adjusted set**.

> **A candidate is never called eligible before the governing act changes the applicable requirement set.** Reversing that order converts a governance record into a justification written afterwards.

The Routing Decision preserves the original constraint, **the original ineligibility result**, the Right and Decision Record reference, the adjusted constraint and its effect, the expiry, and the re-evaluated result. Nothing is rewritten.

---

## M1 — Hard constraints not classified by exceptionability

**Finding.** The architecture said ordinary humans cannot bypass law, privacy, security or contract, and elsewhere spoke generically of Phase 7 exceptions to hard constraints. Both could not be true.

**Status: RESOLVED.** Exceptionability is a property of **where the requirement comes from** (`models/routing-constraint-model.md` §5):

- **`ABSOLUTELY_NON_WAIVABLE`** — no routing exception exists inside AI-OS. Statute, regulation, binding contract, `PRIVILEGED` and `THIRD_PARTY_RESTRICTED` handling, an unsupported sensitivity label, physical impossibility.
- **`GOVERNED_EXCEPTION_POSSIBLE`** — adjustable by a named valid Phase 7 Right covering that class, bounded and expiring.
- **`OPERATOR_CONFIGURABLE_WITHIN_POLICY`** — ordinary choice inside the permitted envelope; not an exception at all.

Every eligibility constraint in §2 carries a class or a derivation rule, validated mechanically. Five rules: **a Phase 7 Right cannot create legal authority the legal order does not grant**; exceptionability is anchored to the source **and to a specific named Right** — "a Decision Right exists" is not a basis; **unknown or unrecognised exceptionability defaults to non-waivable**; **human acknowledgement never changes eligibility**; and an adjustment is bounded and expiring.

---

## M2 — Negative evidence precedence unbounded

**Status: RESOLVED.** `models/evaluation-evidence-model.md` §2a: **negative evidence restricts a claim only where it applies to it**, assessed on eight recorded dimensions — release and profile version, provider/deployment context, capability dimension, task domain, materiality and severity, evidence quality, freshness and effective period, remediation status.

Six rules: stale evidence about a **superseded** release does not dominate current evidence; a context-specific incident does not invalidate unrelated contexts; low-quality anecdote does not permanently override verified evidence without a recorded materiality assessment; a **severe, current** safety or data-handling incident may restrict routing immediately pending review; conflicting applicable evidence creates a governed **`EVIDENCE_CONFLICT`** under Phase 8's conflict rules rather than an average; and **no composite score is introduced by any of it**.

**Unassessed applicability is treated as applicable until assessed** — the strict reading.

---

## M3 — Lifecycle exclusivity unclear

**Status: RESOLVED, by removing two states.** **Exactly one primary lifecycle state at a time**, six of them: `CANDIDATE`, `EVALUATING`, `ELIGIBLE`, `DEPRECATED`, `SUSPENDED`, `RETIRED`.

`PREFERRED` and `RESTRICTED` were removed **as states** because neither is one: preference is a **ranking** property that collided with `ELIGIBLE` (which every preferred profile also is), and a restriction is **contextual** by nature, so as a state it forced one global answer to a per-context question. They are now a **routing designation** and **restriction annotations**, orthogonal to the state and to each other.

Transition rules are defined; **`RETIRED` is terminal** — restoring a retired profile is a new profile, because the evidence that retired it does not un-apply. **No transition touches history.**

---

## M4 — Act requirements masquerading as eligibility filters

**Status: RESOLVED.** Three kinds of requirement, not two (`models/routing-constraint-model.md` §1):

| Kind | Does | On failure |
|---|---|---|
| `ELIGIBILITY_CONSTRAINT` | Filters | Candidate is ineligible |
| `PREFERENCE` | Ranks the eligible | Ranks lower, stays eligible |
| **`ROUTING_ACT_REQUIREMENT`** | Requires an **act** | **No selection finalises.** Candidate set unchanged |

`HUMAN_SELECTION_REQUIRED`, `HUMAN_ACKNOWLEDGEMENT_REQUIRED` and `GOVERNANCE_REVIEW_REQUIRED` are the third kind. **None filters a candidate; none changes eligibility in either direction.** The harness parses the eligibility table and **fails if an act requirement appears in it**.

---

## M5 — Global precedence versus policy-owned preference ordering

**Status: RESOLVED.** The boundary is now explicit:

- **Stages 1–5 are globally fixed and no policy reorders them**: legality/governance → sensitivity/handling/residency → capability/modality/context/tooling → independence/diversity → lifecycle/availability.
- **Stage 6, the preference order, is owned by the versioned Routing Policy**, as an **ordered lexicographic list**. A policy may rank reliability above cost or cost above reliability where the work's risk permits.

Three bounds the policy does not own: no ordering restores an ineligible candidate; the hard stages stay fixed; and **where risk requires reliability it is stated as `MINIMUM_RELIABILITY_CLASS` — an eligibility constraint** — because a preference is negotiable by definition. The old global "reliability before cost" rule is gone, and the harness fails if it returns.

---

## M6 — Model-diversity / reviewer-independence leakage

**Status: RESOLVED.** Exemplar 9 said dropping family diversity waives review independence. **It does not, and cannot.**

Model-family diversity is an **execution** control: reducing it reduces protection against correlated model failure, and nothing else. **Reviewer independence is an organisational property of who reviews** — Phase 6's, waived if ever by Phase 6 and Phase 7 acting on the review itself, **never by a routing choice, an acknowledgement, or any Right exercised over a routing constraint**. Where a Review Profile requires both, they are two controls, and an exception to one leaves the other exactly as it was.

Stated in `models/review-diversity-and-criticality.md` §1, constraint model §5.4, standard §41, architecture §6, the decision template, and the rewritten exemplar 9. A repository-wide scan for similar leakage found no other occurrence.

---

## M7 — Privacy-suitability capability duplicated governance

**Status: RESOLVED — the capability was removed.** `capability.privacy_sensitive_suitability` conceded in its own description that it was "a deployment and contractual property as much as a model one". **A capability token that can be satisfied by signing a contract is not a capability.**

Privacy suitability is expressed only where it is determined: on the Deployment Profile, tested by `SUPPORTED_SENSITIVITY_CLASSES`, `REQUIRED_HANDLING_CONTROLS` and `REQUIRED_DATA_HANDLING_POSTURE`. **23 capability families**, down from 24. Were a genuine intrinsic privacy-relevant model property identified later, it would be named narrowly for that property and kept distinct from contractual eligibility; nothing currently evidenced requires one.

---

## M8 — Data-handling posture ownership

**Status: RESOLVED.** One authoritative reading:

| Layer | Owns |
|---|---|
| **Model Profile** | **Nothing.** Intrinsic technical characteristics only. No retention, training or logging posture |
| **Provider Profile** | The contractual default **and the constraints it places on deployments beneath it** |
| **Deployment Profile** | The **effective posture** routing reads |

A deployment may be **more** restrictive freely; **less** restrictive only where the provider instrument explicitly permits and the deployment evidences it — an unevidenced relaxation is a defect, and the provider-level constraint governs. The Model Profile template's data-handling section now states that recording posture there **is a defect**, because it creates a second source of truth that will diverge.

---

## Validation

**Command:** `python3 validation/phase_9_validation.py`
**Result: `=== 204/204 PASS ===`**, exit 0. Normal, `--verbose` and `--json` all report 204.

**141 → 204.** The count is derived from the suite; nothing was preserved cosmetically.

New semantic groups target the findings directly: `identity-stack` (9), `candidate-universe` (9), `sensitivity` (7), `residency` (6), `posture` (4), `exceptionability` (7), `exception` (10), plus rebuilt `constraints`, `precedence`, `lifecycle`, `human`, `decision-record` and `exemplars` groups.

Checks that parse rather than match: the **eligibility-constraint table** is parsed and every row must carry an exceptionability class or a derivation, and **fails if an act requirement appears in it**; the **lifecycle state table** is parsed from the first table only, so the explanatory table beneath it cannot be read as a declaration; a **scan for ordinal sensitivity constructs** across all normative documents, exempting only text that quotes the rejected model; a scan for `where practical`; a scan for a fixed global reliability-before-cost ordering; and **section-position comparisons** proving the universe section precedes precedence and that case B records ineligibility before re-evaluation.

### What the strengthened harness caught

Rebuilding it against the new semantics surfaced **two real content defects my own edits had left**, both silent:

1. **The standard's §12 rewrite never applied.** An earlier bulk vocabulary normalisation had changed the sentence my replacement targeted, the replacement failed without an assertion, and the standard still carried the **two-kind** requirement model while every other document carried three.
2. **The architecture still said "candidate set where practical"** in its reproducibility section — the exact phrase H2 is about, in the one place the H2 edits had not reached.

Several further failures were stale needles in the harness itself, each replaced with a **stricter** test rather than relaxed — most notably the act-requirement check, which now requires the rule in **three independent places** (§1 and §7 of the constraint model, and the policy template) instead of one phrase.

**Phase 8 harness: `119/119 PASS`, unchanged.** No Phase 8 file was modified in this pass.

---

## Open questions — all 17 re-adjudicated

| # | Question | Disposition | The concrete rule |
|---:|---|---|---|
| 1 | Model Profile identity granularity | **RESOLVED IN FOUNDATION** *(was MUST RESOLVE)* | Six-layer stack; profile describes **one underlying release**; registry version independent of model version; provider offering a bounded mapping; materially different behaviour becomes a distinct profile |
| 2 | Provider and Deployment first-class? | **RESOLVED IN FOUNDATION** | Both, separately; Provider Offering is a mapping inside Provider, with a stated reason |
| 3 | Family versus version for diversity | **RESOLVED IN FOUNDATION** | Version diversity is the weakest form; family addresses correlated blind spots |
| 4 | When is same-model review allowed? | **RESOLVED IN FOUNDATION** | Where the Review Profile declares `SAME_MODEL_ALLOWED` |
| 5 | When is family diversity mandatory? | **RESOLVED IN FOUNDATION** | Where declared; the expected value at Decision-Grade for material independent review, departed from only with a recorded justification |
| 6 | Is different-provider ever mandatory? | **RESOLVED IN FOUNDATION** | Where justified by a provider-level concern; **never a default**, never on quality grounds alone |
| 7 | Capability evidence and refresh | **RESOLVED IN FOUNDATION** *(was MUST RESOLVE)* | Six classes that never merge; **negative evidence bounded by eight applicability dimensions**; `EVIDENCE_CONFLICT` instead of averaging; Phase 8 freshness reused; unassessed applicability treated as applicable |
| 8 | Cost and latency without runtime data | **RESOLVED IN FOUNDATION** | Semantic bands only; preferences unless a task policy declares a bound; a bound blocks rather than relaxing anything else |
| 9 | Human selection and its constraints | **RESOLVED IN FOUNDATION** | A **`ROUTING_ACT_REQUIREMENT`**, not a filter; four things no human act reaches; operator choice, acknowledgement and governed exception separated |
| 10 | Fallback vs degraded vs exception | **RESOLVED IN FOUNDATION** *(was MUST RESOLVE)* | Cases A, B, C; the candidate is **never eligible before the governing act**; the original ineligibility is preserved |
| 11 | When to block rather than choose | **RESOLVED IN FOUNDATION** | Whenever no candidate satisfies every eligibility constraint, or the universe is incomplete and the policy says block |
| 12 | Deprecated and retired in history | **RESOLVED IN FOUNDATION** | Excluded from new routing, removed from nothing; decisions name the profile **version and mapping** used |
| 13 | Privacy and residency attachment | **RESOLVED IN FOUNDATION** *(was MUST RESOLVE)* | Multi-label supported/prohibited sets, handling controls and **effective deployment posture**, plus the six-field residency model with `UNKNOWN_RESIDENCY` never satisfying. No IAM |
| 14 | Preferred for a Role, prohibited for a stage | **RESOLVED IN FOUNDATION** | Lifecycle is a gate, not a grant; `PREFERRED` is a designation, restrictions are annotations |
| 15 | Evaluation methodology or evidence semantics | **RESOLVED IN FOUNDATION** | Evidence semantics only; no benchmark, harness or score |
| 16 | Orchestrator concerns | **PHASE 11+** | What work happens, in what order, by which Role; concurrency, retry, scheduling |
| 17 | Storage and infrastructure | **PHASE 10+** | Persistence for profiles, policies and decisions; **including the registry snapshot mechanism** the Candidate Universe Definition references |

All four audit blockers are resolved by rules that **did not exist before this pass**. No authority, privacy or independence ambiguity is deferred.

---

## Files changed

| File | Purpose |
|---|---|
| `models/routing-constraint-model.md` | Rewritten: three requirement kinds (M4), multi-label sensitivity (H3), residency (H4), exceptionability (M1), posture ownership (M8), policy-owned preference order (M5) |
| `models/routing-precedence-and-fallback.md` | Candidate Universe Definition (H2); fixed/owned precedence split (M5); cases A/B/C (H5) |
| `models/model-lifecycle-and-versioning.md` | Six-layer identity stack (H1); six exclusive states with annotations and transitions (M3) |
| `models/evaluation-evidence-model.md` | Negative-evidence applicability and `EVIDENCE_CONFLICT` (M2) |
| `models/model-capability-taxonomy.md` | `capability.privacy_sensitive_suitability` removed; 23 families (M7) |
| `models/review-diversity-and-criticality.md` | Diversity cannot waive reviewer independence (M6) |
| `models/_standards/common-model-governance-constraints.md` | §12 corrected; **ten new rules (33–42)**; 43 total, contiguous |
| `models/_templates/model-profile-template.md` | Identity stack layers; data-handling removed as a defect (H1, M8) |
| `models/_templates/provider-profile-template.md` | Provider Offering Mappings; provider-level posture and its constraints (H1, M8) |
| `models/_templates/deployment-profile-template.md` | Residency fields (H4); supported/prohibited label sets (H3); effective posture (M8) |
| `models/_templates/routing-policy-template.md` | Candidate Universe Definition; exceptionability column; policy-owned preference order; act requirements (H2, M1, M4, M5) |
| `models/_templates/routing-decision-template.md` | 24 → **31 elements**: universe binding, per-candidate availability, the case-B chain (H2, H5) |
| `models/master-model-routing-universe.md` | Every count corrected; two inexpressible things become three |
| `models/exemplars/` × 6 | 1, 4, 5, 6, 7 reworked for multi-label sensitivity and universe binding; **9 rewritten entirely** (H3, H5, M6) |
| `architecture/model-registry-router.md` | Three requirement kinds; universe binding; multi-label sensitivity; posture ownership; three human acts (H2, H3, H5, M1, M4, M8) |
| `validation/phase_9_validation.py` | 141 → **204 checks**; seven new semantic groups |
| `reviews/phase-9-foundation-self-check.md` | Counts, groups, and where this foundation is most likely to be wrong |
| `reviews/phase-9-foundation-audit-remediation.md` | This record |

**No approved Phase 3–8 file was modified.** Phase 8's harness was not touched in this pass and still reports 119/119.

---

## Regression

Verified in the harness by `git diff` against `00fb92e` plus a clean-tree check: **Phase 3 Roles 0 · Phase 4 Skills 0 · Phase 5 Workflows 0 · Phase 6 Handoff/Review 0 · Phase 7 Decisions 0 · Phase 8 Knowledge 0 · inherited Phase 2/3 architecture 0.**

Phase 9 changes only its own architecture, models, exemplars, validation and review evidence. No runtime, SDK, API call, credential, endpoint, price, probe, storage, UI or orchestration. **No Model, Provider or Deployment Profile instance exists.** No real vendor or product is named anywhere — verified mechanically across every Phase 9 file.

## External repository checks — separate from the offline count

Performed against the GitHub API, **not** folded into the 204:

- Open pull requests on the repository: **1** — PR #1, `architecture/phase-1-2` → `main`, pre-existing and unrelated.
- Open pull requests for `architecture/phase-9-model-registry-router`: **0**.
- Pull requests created by this pass: **0**.

The local validator states its scope honestly and makes no remote claim.

## Status

**Phase 9 remains `PROPOSED`.** Nothing is APPROVED or CANONICAL. No Decision Right was created, no Role gained authority, no review status was set or changed, no profile was created, and no approved Phase 3–8 artifact was modified. Under Phase 6's vocabulary this record is `PRODUCER_REVIEW` and is not an independent audit.

**Post-remediation architecture baseline:** the commit carrying this record — `docs: remediate Phase 9 foundation after independent audit` on this branch. A commit cannot contain its own SHA, so it is not written here rather than written wrongly; resolve it with `git rev-parse HEAD`, and reproduce the result from that tree with `python3 validation/phase_9_validation.py` → `204/204 PASS`.

---
---

# Second Re-Audit Remediation — first pass

Re-audited baseline: `69a119f59c8fc1687944ed27df594dc809aadf78`
Verdict: **FAIL** — 9 of 13 prior findings resolved; **H1, H5, M1 and M7 not resolved**, plus 10 inventory inconsistencies.

Everything above this line is the first remediation and is preserved unaltered.

**The re-audit was right on every count**, and two of its findings are the same defect at different scales: an architecture that says one thing in one section and its opposite in another, and an exemplar that demonstrated a governed mechanism over **objects that do not exist**.

## R1 — H1: the versioning rule contradicted the identity rule

**Finding.** §0 says a Model Profile describes **one underlying release**; §4 said a provider/model change becomes a **Registry Profile Version** change. Both cannot hold.

**Status: RESOLVED.** §4 now derives from §0 rather than qualifying it:

> **A registry profile version never absorbs a change of the underlying release.** Bumping the version records that *the record* changed. It cannot record that *the thing* changed, because the profile's identity is the release it describes.

| What changed | Consequence |
|---|---|
| A claim, evidence, a limitation, a field, a mapping | **New Registry Profile Version** — same profile, same release |
| **The underlying release**, by any route | **A different Model Profile**, linked to its predecessor. **Never a version bump** |
| **Uncertainty about which happened** | **Treated as a changed release** until evidence says otherwise, and the profile is `SUSPENDED` pending it |

The third row is the operative one. Provider version changes are opaque from outside, and a version bump in that situation makes every prior decision naming `model.x v3` ambiguous about what actually ran — the precise failure versioning exists to prevent. **`PROVIDER_VERSION_CHANGE` therefore fires an identity review, not a version bump**, and the review's outcome is never assumed to be the first row.

## R2 — H5 and M1: exemplar 9 exercised registry objects that do not exist

**Finding.** The A/B/C sequence was correct, and the exemplar ran it over an invented model-capability-threshold exception Right and an invented software-security-change Review Profile — **neither of which exists in any approved registry**. Their names are not reproduced here in code form, for the same reason the exemplar no longer reproduces them: a code-form `decision.<id>` or `review.<id>` that resolves to nothing **is** the defect, in a remediation record as much as anywhere else. Semantically correct and legally inoperable.

**Status: RESOLVED — by following the architecture to its actual conclusion rather than inventing a way past it.**

The approved Phase 7 registry carries **eight carded Rights**, and **none covers a model-capability threshold or a model-diversity requirement.** The nearest candidate is instructive: `decision.exceptional_progression` governs *one named unresolved work item at one progression point* — an open finding, an unsatisfied review — **not a routing requirement**, and reading it otherwise would widen a declared subject its own card forbids widening.

The constraint model already answers this: **"a Decision Right exists" is not a basis** — *this* Right must cover *this* class — and **unknown or unrecognised exceptionability defaults to `ABSOLUTELY_NON_WAIVABLE`.**

So exemplar 9 is rewritten as **"The governed exception that is not available"**. Four candidates, all ineligible, each exceptionability class named, **no approved Right covering the two adjustable classes**, and the outcome **`BLOCKED_FOR_ROUTING`** — case C. It then sets out, in order, exactly what case B would have required and where the chain stops: at the third step, for want of a carded Right.

**Every `review.<id>` and `decision.<id>` in it is now a real approved object** — `review.security` and `review.code` for the two controls, `decision.production_release` for the gate, and the eight carded Rights enumerated where the exemplar explains why none of them fits. The two invented names survive only in the note recording that they were invented, **deliberately not in code form**, because a `decision.<id>` string that resolves to nothing is the defect itself.

**This is the better exemplar.** The first version contradicted itself; the second illustrated a mechanism over fiction; this one demonstrates the mechanism **and** what the architecture does when the mechanism is unavailable — which is the case that actually obtains today, and the one an organisation will meet first.

## R3 — M7: the removed capability was still actively referenced

**Status: RESOLVED.** `capability.privacy_sensitive_suitability` was removed from the taxonomy and left in a worked rule in §4, where it read as live vocabulary. The rule now uses `capability.structured_generation` and adds the point the removal establishes: **a deployment-governed requirement is not a capability at all**, so confidence in a capability claim reaches none of them.

## R4 — Inventory inconsistencies

**Status: RESOLVED, and the class of defect is now mechanically prevented.** Ten corrections: capability families 24 → **23** in the architecture, the taxonomy's prose and the universe; eligibility constraints → **27**; preferences → **9**; inherited rules 33 → **43**; "22 hard and 8 soft" replaced; "Two things this architecture cannot express" → **Three**, matching its own list; component-table descriptions updated to current counts.

**Every one of these is now derived rather than maintained.** Seven new `inventory` checks parse the capability table, the eligibility table, the preference table and the constraint numbering, and **fail if any stated number disagrees with the count derived from the file** — including the heading-versus-list mismatch that produced "two things" above a list of three.

## R5 — Validation extended to the three gaps the re-audit named

**Status: RESOLVED. 204 → 219 checks.**

| Gap named | Added |
|---|---|
| Does not validate referenced Review/Decision IDs against approved registries | **`cross-registry` group (4)** — every `review.<id>` and `decision.<id>` in every Phase 9 file must resolve against the approved `reviews/` and `decisions/` trees; exception paths must cite only **carded** Rights or block; and one check asserts the registries were actually discovered (≥20 reviews, exactly 8 carded Rights) **so the scan cannot pass vacuously on an empty set** |
| Does not detect the residual profile-version contradiction | **3 `identity-stack` checks** — no document may assert that a provider version change is a profile version change outside a remediation note; the distinct-profile rule must be present; the uncertainty default must be stated |
| Does not scan active inventory prose for stale counts or removed capability references | **7 `inventory` checks** — all counts derived; stale word-form counts scanned; removed capability tokens permitted only inside their removal note |

**The cross-registry check would have caught the exemplar-9 defect on the first run**, which is the honest measure of the gap: 204 checks passed over two references to objects that do not exist.

## Validation

**`python3 validation/phase_9_validation.py` → `=== 219/219 PASS ===`**, exit 0. Normal, `--verbose` and `--json` all report 219.
**`python3 validation/phase_8_validation.py` → `119/119 PASS`**, unchanged and untouched in both passes.

## Open questions

The re-audit left **#1** and **#10** as MUST RESOLVE. Both are now resolved by concrete rules:

| # | Now | Rule |
|---:|---|---|
| **1** | **RESOLVED IN FOUNDATION** | A registry profile version never absorbs a release change; a changed release is a distinct profile; uncertainty is treated as a changed release and suspends the profile |
| **10** | **RESOLVED IN FOUNDATION** | Cases A/B/C stand, and case B additionally requires a **carded** Right covering the constraint class. **None exists today**, so every case-B path currently resolves to case C — stated in the architecture and demonstrated in exemplar 9 rather than assumed away |

The remaining 15 dispositions are unchanged from the first remediation.

## Files changed in this pass

| File | Purpose |
|---|---|
| `models/model-lifecycle-and-versioning.md` | §4 derived from §0; release change ≠ version bump; uncertainty default; identity review (H1) |
| `models/exemplars/degraded-fallback-governed-exception.md` | Rewritten — real registry objects only; no carded Right exists; outcome is `BLOCKED_FOR_ROUTING` (H5, M1) |
| `models/model-capability-taxonomy.md` | §4 rule no longer cites the removed capability; prose count corrected (M7) |
| `models/master-model-routing-universe.md` | Six count corrections; heading matched to its list |
| `architecture/model-registry-router.md` | Component-table counts corrected |
| `validation/phase_9_validation.py` | 204 → **219**; `cross-registry` (4), `identity-stack` (+3), `inventory` (7) |
| `reviews/phase-9-foundation-self-check.md` | Counts, two new groups, invented-ID reference removed |
| `reviews/phase-9-foundation-audit-remediation.md` | This section |

**No approved Phase 3–8 file was modified in either pass**, and the Phase 8 validator was not touched in either.

## Status after the second pass

**Phase 9 remains `PROPOSED`.** Nothing is APPROVED or CANONICAL. No Decision Right was created, no Role gained authority, no review status was set or changed, no Model, Provider or Deployment Profile exists, and no real vendor is named anywhere.

**External checks, separate from the 219:** open PRs on the repository **1** (PR #1, unrelated, pre-existing); for this branch **0**; created by this pass **0**.

---

## Second Re-Audit Remediation — completion against the remediation prompt

`prompts/phase-9-claude-final-remediation-after-re-audit.md` was issued after the pass above and specifies requirements beyond it. Three were genuinely missing and are now implemented; the rest confirmed complete.

### Blockers, final status

| Blocker | Status |
|---|---|
| **1. Underlying release vs Registry Profile Version** | **RESOLVED** — plus the five provider-side cases (§1.2) and the six-part reproducibility set (§1.3) the prompt requires, neither of which the earlier pass had |
| **2. Invented Phase 6 / Phase 7 references in Exemplar 9** | **RESOLVED** — plus the general cross-registry integrity rule (§2.4) and the explicit `NO_APPLICABLE_DECISION_RIGHT` / `ESCALATED_FOR_GOVERNANCE_DESIGN` outcomes (§2.3) |
| **3. Stale privacy-capability reference** | **RESOLVED** — active undeclared-capability references: **0**, now enforced generically rather than by naming one token |
| **4. Stale inventory counts** | **RESOLVED** — every count derived; active inconsistencies: **0** |
| **5. Validation gaps** | **RESOLVED** — 219 → **239** checks |

### What this pass added

**§1.2 — five provider-side cases, distinguished:** alias rename → mapping update, identity unchanged where sameness is proven; contractual or data-handling change → Provider/Deployment version, identity unchanged; **backend behaviour materially changes and sameness cannot be proven → new Model Profile identity or a recorded identity conflict, never a version bump**; deployment configuration or residency change → Deployment Profile, not a release change; AI-OS metadata or evidence correction → Registry Profile Version only.

**§1.3 — the six-part reproducibility set** on the Routing Decision: stable ID · registry profile version · **underlying model release identity** · provider offering mapping · provider profile version · deployment profile version. The third was missing, and it is the one that matters: a stable ID names a lineage of records, a registry version names a record, and **only the release identity names the thing that ran.**

**§2.4 — the cross-registry integrity rule**, now normative in the architecture (§6a), the standard (§43) and the Routing Decision template: every `decision.<id>` and `review.<id>` resolves to an approved Phase 7 or Phase 6 object, or carries `FUTURE_GOVERNANCE_REFERENCE` and is **non-executable**. Where a review is conceptually needed and no Profile matches, `REVIEW_PROFILE_NOT_BOUND_IN_PHASE_9`. **Carding a Right is a Phase 7 act, never one Phase 9 performs, implies or assumes.**

**§2.3 — Exemplar 9's governance boundary is now a recorded outcome**, not an absence: `NO_APPLICABLE_DECISION_RIGHT`, with `BLOCKED_FOR_ROUTING` / `ESCALATED_FOR_GOVERNANCE_DESIGN`. Both its review references were checked against the registry and resolve, so no not-bound marker is used — and the exemplar says what it would carry if none had.

**Standard grows to 45 rules** (§43 cross-registry integrity, §44 identity bound to one release).

### What the new checks caught

Rebuilding the harness against the prompt's requirements surfaced **two more real content defects**, neither previously visible:

1. **`capability.review_detection` in exemplar 3** — an **undeclared capability ID**, invented in the first foundation pass and never noticed. The generic undeclared-capability check found it where the token-specific check could not. Corrected to `capability.code_review`, with the point it was reaching for made explicit: the dimension a review task turns on is not the dimension that produced the artifact.
2. **The constraint count in the universe** was 43 while the standard had grown to 45 — stale within minutes of being corrected, which is precisely why counts are now **derived and cross-checked** rather than maintained.

Two further failures were check defects, each replaced with a **stricter** correct test: the heading/list counter was counting table header and separator rows as items, and the Phase-7-act check matched case-sensitively against text that `plain()` had already normalised.

### Validation

**`python3 validation/phase_9_validation.py` → `=== 239/239 PASS ===`**, exit 0. `--verbose` exit 0; `--json` reports total 239, passed 239, **239 result entries**. **Injected failure → `239/240`, exit 1** — the harness is demonstrably able to fail.

**`python3 validation/phase_8_validation.py` → `119/119 PASS`**, untouched across all three Phase 9 passes.

New this pass: `cross-registry` grows to 8 (integrity rule in three layers, Phase-7-act boundary, **six-property exemplar-9 governance integrity**); `identity-stack` grows to 14 (five provider cases, unprovable-sameness rule, six-part set, standard-level rule); `inventory` grows to 21 (**ten derived counts cross-checked**, undeclared-capability scan, stale-number scan across active prose, heading/list cardinality).

### Open questions

| # | Now | Why |
|---:|---|---|
| **1** | **RESOLVED IN FOUNDATION** | The release/version rule is globally consistent — one normative statement, five enumerated provider cases, a standard-level rule, and a harness check that fails on contradictory wording anywhere. **No runtime guess remains**: every provider-side case has a stated consequence, and the unprovable case resolves to the safe reading |
| **10** | **RESOLVED IN FOUNDATION** | Ordinary fallback is executable under policy; the governed-exception path requires an **actually applicable approved Phase 7 Right**; its absence **blocks and escalates** rather than inventing governance; and future carding is stated as a **Phase 7 governance extension**, never something Phase 9 creates |

The other 15 are unchanged from the earlier passes.

### Regression

Verified in-harness against `00fb92e`: **Phase 3–8 all 0**, inherited Phase 2/3 architecture 0. **The Phase 8 validator was not modified in this pass**, and the only Phase 8 tooling change in the whole Phase 9 sequence remains the approval-record exemption made during the Phase 8 remediation, before Phase 9 began. No runtime, SDK, API, credential, endpoint, storage, UI or orchestration. **No Model, Provider or Deployment Profile exists**; no real vendor named.

**External checks, separate from the 239:** open PRs on the repository **1** (PR #1, unrelated, pre-existing); for this branch **0**; created by this pass **0**.

**Phase 9 remains `PROPOSED`.**

---

# Final conformance cleanup after the approval re-audit

**Scope of this pass: conformance, counts, exemplar completeness and validation strength only.** No governance semantics were introduced, changed or removed. No approved Phase 3–8 artifact was touched. Every Phase 9 artifact remains `PROPOSED`, and **human approval is still pending the final re-audit** — nothing here claims it.

The approval re-audit returned FAIL with every deep architecture blocker resolved. What remained was the uncomfortable kind of finding: a suite reporting `239/239 PASS` over conformance it did not actually check. Each fix below is therefore written twice — once in the content, once as a check that fails on exactly that defect.

## The blockers, and what was done

| # | Blocker | Fix |
|---:|---|---|
| 1 | Inventory claimed **31** Routing Decision elements; the template has **35** | Corrected in `models/master-model-routing-universe.md`; a line-scoped check now compares every active element claim against the count parsed from the template's numbered rows |
| 2 | Active prose said a profile is a vector across **24** dimensions; **23** families are declared | Corrected to name the 23 capability families; the existing derived-count scan now also covers this document |
| 3 | Negative-evidence applicability prose said **seven** dimensions; the table lists **eight** | Corrected in `models/evaluation-evidence-model.md`; the count is now derived from the authoritative table and compared to the prose |
| 4 | Exemplars **2, 3 and 8** carried no Candidate Universe Definition; **1, 4, 5, 6, 7 and 9** carried a prose approximation missing mandatory elements | All nine now bind the definition as an explicit nine-row table. A per-exemplar check requires every mandatory element and fails on a missing one |
| 5 | Exemplar 4 declared **4** enumerated candidates and assessed **5** | Declared count corrected to 5 and the candidate set enumerated by name. A per-exemplar check now requires declared cardinality to equal the rows actually assessed |
| 6 | Exemplar 1 placed a cost preference at **stage 7** | Corrected to stage 6, with stage 7 named as the tie-break that was not reached. A check parses the normative stage map from the precedence table and fails on any active sentence placing a preference at stage 7 |
| 7 | The producer self-check carried stale totals, stale group counts and scalar-ceiling sensitivity wording | Rewritten to describe only the current architecture. It is no longer exempt from the count scans, and a final check asserts the total it states is the total the suite actually produces |
| 8 | Exemplar 8's historical decision did not carry the six-part reproducibility identity set | The 2025 decision now records all six parts, unaltered by the later deprecation. A check derives which exemplars record a historical decision and requires the set in each |

Two further defects were found by the new checks rather than by the audit, and are recorded here because they are the point of writing checks at all: exemplar 4's heading said "three deployments" over four, and two self-check rows repeated the same miscount.

## Counts, all derived

| Quantity | Derived | Source of truth |
|---|---:|---|
| Capability families | 23 | `models/model-capability-taxonomy.md` §2 |
| Eligibility constraints | 27 | `models/routing-constraint-model.md` §2 |
| Preferences | 9 | `models/routing-constraint-model.md` §6 |
| Routing act requirements | 3 | `models/routing-constraint-model.md` §7 |
| Primary lifecycle states | 6 | `models/model-lifecycle-and-versioning.md` §1 |
| Evidence classes | 6 | `models/evaluation-evidence-model.md` §2 |
| Negative-evidence applicability dimensions | 8 | `models/evaluation-evidence-model.md` §2a |
| Common constraints | 45 | `models/_standards/common-model-governance-constraints.md` |
| Templates | 5 | `models/_templates/` |
| Exemplars | 9 | `models/exemplars/` |
| Routing Decision elements | 35 | `models/_templates/routing-decision-template.md` |

**Remaining inconsistencies: 0**, by the harness rather than by inspection.

## Validation

`validation/phase_9_validation.py` grows from **239** to **270** checks — `candidate-universe` 10 → 29, `inventory` 21 → 29, `precedence` 9 → 11, `decision-record` 16 → 18. The number was not targeted; it is what the new per-exemplar checks come to.

Eight controlled failure injections, each reverted, each failing exactly the intended check and nothing else:

| Injection | Result |
|---|---|
| Exemplar 2 loses its universe block | `268/270`, exit 1 — the two `high-criticality-reasoning` universe checks |
| Exemplar 4 declares 4 where it assesses 5 | `269/270` — the cardinality check |
| A cost preference placed at stage 7 | `269/270` — the stage-7 preference check |
| Self-check restates 31 Routing Decision elements | `269/270` — the element-claim check |
| Self-check restates a prior-pass total | `269/270` — the current-total check |
| Negative-evidence prose reverted to seven | `269/270` — the dimension-claim check |
| Precedence table renumbers the tie-break as stage 6 | `269/270` — the stage-map check |
| A vacuous `or True` check added to the harness | `269/271` — the vacuous-check scan |

`python3 validation/phase_8_validation.py` → **`119/119 PASS`**, and `validation/phase_8_validation.py` is **byte-identical** to its committed state: this pass did not touch it.

**Credibility.** Higher than the previous pass on exactly the dimension the re-audit attacked, and no higher elsewhere. The new checks are per-exemplar and derived, so a tenth exemplar added tomorrow is checked automatically and cannot pass by being absent from a list. What the harness still cannot do is judge whether the architecture is *right*; it checks that the documents agree with each other and with their own tables. It is also, still, a **producer** artifact: it cannot satisfy an independent review requirement, and the 270 prove consistency, not approval.

## Standing statement

Every Phase 9 artifact is `PROPOSED`. Nothing is APPROVED or CANONICAL. No Decision Right was created, no Review Profile bound, no review status set or changed, no Model, Provider or Deployment Profile created, no real model or provider named, no runtime, SDK, API, credential, storage, UI or orchestration written, and no approved Phase 3–8 artifact modified. No pull request was created. **Human approval remains pending the final re-audit.**
