# Phase 9 — Model Registry and Router Foundation Self-Check

Status: PROPOSED — READY FOR INDEPENDENT PHASE 9 FOUNDATION AUDIT

Branch: `architecture/phase-9-model-registry-router`
Start baseline: Phase 8 human-approval record `00fb92e1b2dd1209ee2f69550c5962158b881e3e`
Approved Phase 8 architecture baseline: `516c91eb98ce89751b97d21c74553afaf7bed21b`

This is a **self**-check by the producing pass. Under Phase 6's vocabulary it is `PRODUCER_REVIEW` — internal quality control, which cannot satisfy an independent review requirement. It carries no results of its own; it points at the harness that produces them.

## Running the check

```
python3 validation/phase_9_validation.py
```

Python 3 standard library and `git` only. No network, no third-party packages, no writes. Deterministic; exit code 0 on pass, non-zero on any failure. `--verbose` prints each check's evidence; `--json` emits machine-readable results. Conventions are in `validation/README.md`.

**Current result: `=== 141/141 PASS ===`.** Normal, `--verbose` and `--json` modes all report the same total.

**The count is derived from the suite, not chosen.** No number was carried over from Phase 8, and none was targeted.

**Scope boundary.** These 141 are **offline, deterministic checks over committed content**. Remote repository state — open pull requests, branch protection, review state — is **not provable offline and is not claimed**; it is checked separately against the GitHub API and reported alongside this foundation.

| Group | Checks | Covers |
|---|---:|---|
| `identity` | 8 | The 14-object chain; all nine denials verbatim; model/provider/deployment separation; output enters Phase 8 as `AI_SUGGESTION` |
| `capability` | 13 | 24 families; 4 claim classes; `NOT_CLAIMED` ≠ `NOT_CAPABLE`; 6 evidence classes; provider declaration ≠ proof; benchmark ≠ authority; no composite; confidence ≠ eligibility; Phase 8 freshness reused |
| `constraints` | 10 | 24 constraint types; hard filters, soft ranks; no partial eligibility; unrecognised constraint blocks; sensitivity is a deployment property; unstated ≠ satisfied |
| `precedence` | 7 | 8 ordered stages; each filters the next; cost never overrides governance; reliability ordered before cost; ordered not weighted; deterministic tie-break |
| `lifecycle` | 8 | 8 states; status ≠ task eligibility; `PREFERRED` not mandatory; deprecation removes nothing; three versioned objects |
| `anti-lock-in` | 8 | Stable ID forms; aliases never constrained against; pinning exceptional and expiring; **zero vendor names anywhere**; exemplars declared synthetic |
| `diversity` | 10 | 6 diversity values; independence ≠ diversity; all four combinations; no Phase 6 class added; different-provider never default; named prior selection required |
| `fallback` | 12 | 4 availability classes; availability ≠ capability; `UNKNOWN_AVAILABILITY` not silently available; 5 fallback kinds; no silent degradation; no compounding; block is correct |
| `human` | 5 | What a human may do, and the four things no human override reaches |
| `privacy` | 7 | Phase 8 classes reused; classification never names a provider; no scope crossing; canonicality and visibility unchanged; no IAM |
| `decision-record` | 17 | 24 elements; policy and profile versions; per-candidate eligibility; degraded-selection disclosure; not editable; routing reproducibility only |
| `templates` | 8 | 5 templates; non-runtime statements; no URLs or credentials; bands not prices; contiguous constraint numbering matched against the inventory |
| `exemplars` | 14 | 9 discovered on disk; each states what it proves; block, outage and history exemplars checked specifically |
| `regression` | 14 | Phases 3–8 and inherited architecture unchanged since the baseline; all `PROPOSED`; no runtime; no profile instances created; harness read-only; no vacuous checks; no local PR action |

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

Recorded for the audit rather than left to be discovered:

1. **The capability taxonomy is a judgement, not a derivation.** Twenty-four families is a reasonable cut of a continuous space, and the boundaries between `general_reasoning` / `advanced_reasoning`, and between `coding` / `code_review`, will be argued. The architecture depends on requirements and claims sharing a vocabulary — not on this particular vocabulary being right.
2. **`MODEL_DIVERSITY_REQUIRED` depends on a registry that does not exist yet.** With few profiles, family diversity may be unsatisfiable in practice, and the honest outcome is then `BLOCKED_FOR_ROUTING` more often than an organisation will find comfortable. That is the control working, and it will be read as the control failing.
3. **No Routing Policy instance exists**, so the constraint model is unexercised against a real policy. The nine exemplars are decisions under policies described in prose, not authored.
4. **The cost/latency-as-sometimes-hard rule is the weakest joint.** It is where a future policy author could, by declaring a bound aggressively, squeeze the eligible set until only the cheap candidate survives — technically without violating anything. §4 of the constraint model forbids relaxing other constraints to fit a budget; whether that is enough without a policy review gate is a fair audit question.
5. **`HUMAN_SELECTION_REQUIRED` is a constraint that nothing in the architecture can satisfy on its own.** That is deliberate, and it means a policy declaring it without a human process behind it produces a permanent block.

## Standing statement

Every Phase 9 artifact is `PROPOSED`. Nothing is APPROVED or CANONICAL. No Decision Right was created, no Role gained authority, no review status was set or changed, no Model, Provider or Deployment Profile was created, no model or provider is endorsed, and no approved Phase 3–8 artifact was modified. This record does not claim human approval and is not an independent audit.
