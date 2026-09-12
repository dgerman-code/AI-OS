# Phase 9 — Model Registry and Router Foundation Self-Check

Status: PROPOSED — READY FOR FINAL INDEPENDENT PHASE 9 RE-AUDIT

**Updated after the independent Phase 9 audit returned FAIL (5 HIGH, 7 MEDIUM).** Every finding was genuine; the remediation and its 204-check suite are recorded in `reviews/phase-9-foundation-audit-remediation.md`.

Branch: `architecture/phase-9-model-registry-router`
Start baseline: Phase 8 human-approval record `00fb92e1b2dd1209ee2f69550c5962158b881e3e`
Approved Phase 8 architecture baseline: `516c91eb98ce89751b97d21c74553afaf7bed21b`

This is a **self**-check by the producing pass. Under Phase 6's vocabulary it is `PRODUCER_REVIEW` — internal quality control, which cannot satisfy an independent review requirement. It carries no results of its own; it points at the harness that produces them.

## Running the check

```
python3 validation/phase_9_validation.py
```

Python 3 standard library and `git` only. No network, no third-party packages, no writes. Deterministic; exit code 0 on pass, non-zero on any failure. `--verbose` prints each check's evidence; `--json` emits machine-readable results. Conventions are in `validation/README.md`.

**Current result: `=== 239/239 PASS ===`.** Normal, `--verbose` and `--json` modes all report the same total.

**The count is derived from the suite, not chosen.** 141 → 204 after the first audit, → 219, → 239 after the re-audit; nothing was preserved cosmetically, and no number was targeted.

**Scope boundary.** These 141 are **offline, deterministic checks over committed content**. Remote repository state — open pull requests, branch protection, review state — is **not provable offline and is not claimed**; it is checked separately against the GitHub API and reported alongside this foundation.

| Group | Checks | Covers |
|---|---:|---|
| `identity` | 8 | The 14-object chain; all nine denials verbatim; model/provider/deployment separation; output enters Phase 8 as `AI_SUGGESTION` |
| `identity-stack` | 9 | Six layers; registry version ≠ model version; offering is a mapping; materially different behaviour becomes a distinct profile; alias never defines identity |
| `capability` | 13 | 23 families; 4 claim classes; 6 evidence classes; provider declaration ≠ proof; no composite; confidence ≠ eligibility; Phase 8 freshness reused |
| `constraints` | 10 | 27 eligibility constraints; three requirement kinds; act requirements absent from the eligibility table; no partial eligibility |
| `exceptionability` | 7 | Three classes; derived from source; legal and privileged sources non-waivable; unknown defaults non-waivable; acknowledgement changes nothing |
| `candidate-universe` | 9 | Eight elements; bound before filtering; pre-filter vs constraint exclusion; availability does not remove; incomplete blocks or escalates |
| `sensitivity` | 7 | No ordinal construct survives; subset test with obligations; compound labels; unknown ≠ supported; prohibition wins |
| `residency` | 6 | Six fields; `UNKNOWN_RESIDENCY` never satisfies; prohibited outranks allowed; class needs a mapping; deployment-owned |
| `posture` | 4 | One authoritative reading; Model Profile carries none; deployment effective posture; evidenced relaxation only |
| `precedence` | 9 | Nine stages; 1–5 globally fixed, 6 policy-owned; no fixed reliability-before-cost; lexicographic; deterministic tie-break |
| `exception` | 10 | Cases A/B/C; never eligible before the act; original ineligibility preserved; ordering proven by position; bounded and expiring |
| `lifecycle` | 11 | Six exclusive states; `PREFERRED` and restrictions as annotations; transitions; `RETIRED` terminal; history untouched |
| `anti-lock-in` | 8 | Stable IDs; aliases never constrained against; pinning expiring; **zero vendor names**; exemplars synthetic |
| `diversity` | 10 | Six values; independence ≠ diversity; no Phase 6 class added; provider diversity never default; named prior selection |
| `fallback` | 12 | Four availability classes; five fallback kinds; no silent degradation; no compounding; block is correct |
| `human` | 5 | What a human may do; four unreachable things; three acts kept apart |
| `privacy` | 7 | Phase 8 classes reused; classification never names a provider; no scope crossing; no IAM |
| `decision-record` | 17 | 31 elements; universe binding; per-candidate results; case-B chain; routing reproducibility only |
| `templates` | 8 | Five templates; non-runtime statements; no URLs or credentials; bands not prices; 43 contiguous constraints |
| `exemplars` | 14 | Nine on disk; each states what it proves; block, outage and history exemplars checked specifically |
| `cross-registry` | 8 | **Every `review.<id>` and `decision.<id>` in Phase 9 resolves to an approved registry object**; exception paths cite only carded Rights; the check proves the registries were found, so it cannot pass vacuously |
| `inventory` | 21 | Counts derived from the files and compared to every statement of them; stale word-form counts; heading-versus-list consistency; no live reference to a removed capability |
| `regression` | 14 | Phases 3–8 unchanged; all `PROPOSED`; no runtime; no profile instances; harness read-only; no vacuous checks |

## Producer self-check threshold

The prompt's twelve conditions, answered against the artifacts rather than asserted:

| Condition | Position |
|---|---|
| No Role/Model collapse | `MODEL != ROLE` stated verbatim; Roles are not staffed by models; no Role Card names a model, and none was modified |
| No Router/Orchestrator collapse | `ROUTER != ORCHESTRATOR`; what work happens, in what order, by which Role is explicitly not the Router's question |
| No Routing Decision/Decision Right collapse | Stated in the architecture, the standard and the decision template; the template's closing section denies each specific power |
| No model/provider/deployment collapse | Three templates, three ID families; exemplar 4 shows one model with three different eligibility answers |
| No capability-confidence-as-truth collapse | Claims carry evidence; confidence ranks and never qualifies; no composite exists; evidence is about a tool |
| No cost overriding hard governance | Precedence filters before ranking; cost sits at stage 7 after reliability; a hard cost bound blocks rather than relaxes anything else |
| No silent degraded fallback | Degraded fallback names its weaker dimension, is recorded as degraded, and at Decision-Grade requires a Phase 7 exception |
| No independence/diversity collapse | Orthogonality stated with all four combinations; Phase 9 adds no Phase 6 class and changes no review status |
| No human override bypassing mandatory constraints | Four explicit cannots; proceeding on an unmet hard constraint is a governed exception or does not happen |
| No provider lock-in in higher architecture | Stable IDs, aliases, deployment-carries-sensitivity; **zero vendor names in any Phase 9 file**, verified mechanically |
| No Phase 3–8 regression | `git diff` against the Phase 8 approval baseline, verified in the harness |
| No runtime implementation | No SDK, API, credential, endpoint, price, probe or storage; enforced by a pattern scan over every file |
| All deterministic validation passes | 141/141 |

## Open architecture questions — all 17 adjudicated

| # | Question | Disposition | The rule, or the reason for deferral |
|---:|---|---|---|
| 1 | Is a Model Profile one vendor model/version, one family, or an internal abstraction? | **RESOLVED IN FOUNDATION** | **One model at one version, through a stable internal ID.** Family is a declared attribute used by diversity constraints, not the unit of profiling — a family-level profile could not carry version-specific evidence, and evidence is version-specific because behaviour is |
| 2 | Should Provider and Deployment be first-class registry objects? | **RESOLVED IN FOUNDATION** | **Both, separately.** Deployment carries residency, maximum sensitivity and retention posture; provider carries contractual posture and concentration. Exemplar 4 is the proof: one model, three deployments, three different eligibility answers |
| 3 | How do family and exact version differ for review diversity? | **RESOLVED IN FOUNDATION** | Version diversity is the **weakest** form — versions of one lineage share training and share blind spots. Family diversity addresses correlated blind spots, which is the failure an independent review is usually for |
| 4 | When is same-model review allowed? | **RESOLVED IN FOUNDATION** | Where the Review Profile declares `SAME_MODEL_ALLOWED` — appropriate where the review checks something a shared blind spot cannot hide, such as arithmetic or schema conformance, and at bands where the risk does not warrant the cost |
| 5 | When is different-model-family review mandatory? | **RESOLVED IN FOUNDATION** | Where a Review Profile or policy declares it. At **Enhanced Decision-Grade it is the expected value for material independent review**, departed from only with a recorded justification — tied to risk in the work, not imposed as a blanket rule |
| 6 | Is different-provider review ever mandatory? | **RESOLVED IN FOUNDATION** | Yes, where justified by a provider-level concern — outage correlation, a data-handling concern, supply concentration. **Never a default**, and never on quality grounds alone, because family diversity already carries that. Imposed reflexively it shrinks the eligible set, often to one |
| 7 | How are capability claims evidenced and refreshed? | **RESOLVED IN FOUNDATION** | Six distinct evidence classes that never merge; a policy declares which it accepts per capability and band; Phase 8 freshness is reused unchanged, with seven refresh triggers including provider version and terms change |
| 8 | How are cost and latency represented without live runtime data? | **RESOLVED IN FOUNDATION** | Semantic bands only — four cost, four latency. No prices, rates or measured latencies appear anywhere. They are preferences unless a task policy declares a bound, and a bound blocks rather than relaxing anything else |
| 9 | Can a human select a model directly, and under what constraints? | **RESOLVED IN FOUNDATION** | Yes, among **eligible** candidates, and a human may also require stronger, require different, prohibit, accept a declared degraded fallback, or block. Four things no override reaches: eligibility where law or privacy forbids, mandatory review independence, the truth of output, and routing history |
| 10 | Fallback vs degraded fallback vs exception? | **RESOLVED IN FOUNDATION** | Equivalent fallback meets every hard constraint and is not materially weaker; degraded meets every hard constraint but is materially weaker and must be declared as such; an exception is a **Phase 7 Decision Right** exercised where a material Decision-Grade requirement is unmet. Exemplar 9 walks all three plus the two refusals |
| 11 | When should routing block rather than choose best available? | **RESOLVED IN FOUNDATION** | **Whenever no candidate satisfies every hard constraint.** There is no "best available" in this architecture, no partial eligibility, and an outage is never a reason to relax a constraint |
| 12 | How do deprecated and retired models appear in history? | **RESOLVED IN FOUNDATION** | Excluded from **new** routing; **removed from nothing**. Historical Routing Decisions stay intact naming the profile and version actually used, and the profile record is retained at its final version |
| 13 | How are privacy and residency attached without IAM or runtime? | **RESOLVED IN FOUNDATION** | As **declared properties of a Deployment Profile** — maximum approved sensitivity, jurisdiction, retention posture — tested by hard constraints. No identity, permission or access-control mechanism is designed, and a runtime enforces what the architecture declares |
| 14 | Can a model be preferred for a Role but prohibited for a Workflow stage? | **RESOLVED IN FOUNDATION** | Yes, and this is the ordinary case. Lifecycle status is a registry gate, never a task grant; a `PREFERRED` model disqualified by a stage's constraints is not in the set to be preferred |
| 15 | Does Phase 9 own evaluation methodology or only evidence semantics? | **RESOLVED IN FOUNDATION** | **Evidence semantics only.** Classes, dimensions, confidence and freshness are defined; no benchmark, harness, test or scoring function is. Building the evaluation system is later work, and its output has to mean something first |
| 16 | Which concerns belong to Phase 11 Orchestrator? | **PHASE 11+** | What work happens, in what order, by which Role; concurrency, retry, scheduling, queueing, execution. `ROUTER != ORCHESTRATOR` is the boundary, and Phase 9 answers only *which execution capability is eligible for this bounded work* |
| 17 | What belongs to Phase 10 storage/infrastructure? | **PHASE 10+** | Persistence for profiles, policies and Routing Decisions; retention of routing history; indexing and query. Phase 9 defines the semantic records; where they live is not its question |

**No authority, privacy or independence ambiguity is deferred.** Questions 5, 6, 9, 10, 11 and 13 all touch those concerns and are resolved in the foundation; only 16 and 17 are deferred, and both are scope boundaries rather than open questions about how routing governs.

## Where this foundation is most likely to be wrong

Recorded for the re-audit rather than left to be discovered. The first version of this section listed five; the audit found five HIGH findings, and **none of them was on that list** — which is the honest measure of how much weight to put on what follows.

1. **The exceptionability derivation table is a judgement about sources.** Classifying "an explicit security prohibition adopted as policy" as non-waivable-unless-the-policy-names-a-Right is defensible and arguable, and an organisation whose security policy is written loosely will find the classification doing more work than its authors intended.
2. **The candidate universe assumes a registry snapshot mechanism that does not exist.** The architecture requires a deterministic registry state reference and says storage is Phase 10's. Until Phase 10 provides one, the requirement is satisfiable only by convention, and a convention is not a snapshot.
3. **Case B depends on Phase 7 Rights nobody has carded.** No approved Decision Right covers a routing constraint class, so **today every case-B path is in fact case C**. Exemplar 9 now demonstrates exactly that rather than illustrating the mechanism over an invented Right — writing a `decision.<id>` that resolves to nothing is the defect, not a shortcut past it.
4. **23 capability families is still a judgement**, and the boundaries between `general_reasoning` / `advanced_reasoning` and `coding` / `code_review` will be argued. The architecture depends on requirements and claims sharing a vocabulary, not on this vocabulary being right.
5. **The multi-label sensitivity model makes eligibility harder to satisfy than the ceiling model did**, deliberately. Organisations will meet `BLOCKED_FOR_ROUTING` more often, and will read the control as an obstruction. Exemplar 7 exists to show it working.

## Standing statement

Every Phase 9 artifact is `PROPOSED`. Nothing is APPROVED or CANONICAL. No Decision Right was created, no Role gained authority, no review status was set or changed, no Model, Provider or Deployment Profile was created, no model or provider is endorsed, and no approved Phase 3–8 artifact was modified. This record does not claim human approval and is not an independent audit.
