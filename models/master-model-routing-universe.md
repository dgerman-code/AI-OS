# Master Model and Routing Universe

Status: PROPOSED — Phase 9 inventory
Version: 0.1
Inherits: `standard.model.common_constraints@0.1`

## 1. What this is, and what it deliberately is not

The inventory of what Phase 9 governs, what it inherits, what it leaves alone, and what it hands on.

**It is not a catalogue of models or providers.** No Model Profile, Provider Profile or Deployment Profile is created by Phase 9, and none is implied. Profiles are populated by a governed pass with evidence in hand; generating them now would produce **vendor claims transcribed as architecture** — the precise failure `standard.model.common_constraints` §7 exists to prevent, committed by the document that defines the rule.

The nine exemplars are **Routing Decisions over synthetic identifiers**. They demonstrate the model. They assert nothing about any real product.

## 2. Governed vocabularies

| Vocabulary | Members | Owner document |
|---|---:|---|
| Capability families | **23** | `models/model-capability-taxonomy.md` §2 |
| Capability claim classes | 4 | `models/model-capability-taxonomy.md` §3 |
| Evidence classes | 6 | `models/evaluation-evidence-model.md` §2 |
| Negative-evidence applicability dimensions | 8 | `models/evaluation-evidence-model.md` §2a |
| Evaluation dimensions | 11 | `models/evaluation-evidence-model.md` §3 |
| Confidence levels | 3 | `models/evaluation-evidence-model.md` §4 |
| Refresh triggers | 7 | `models/evaluation-evidence-model.md` §5 |
| Identity-stack layers | 6 | `models/model-lifecycle-and-versioning.md` §0 |
| Primary lifecycle states | **6**, mutually exclusive | `models/model-lifecycle-and-versioning.md` §1 |
| Lifecycle annotations | 2 kinds — `PREFERRED` designation, restriction annotations | `models/model-lifecycle-and-versioning.md` §1 |
| Eligibility constraints | **24** | `models/routing-constraint-model.md` §2 |
| Act requirements | **3** | `models/routing-constraint-model.md` §7 |
| Exceptionability classes | **3** | `models/routing-constraint-model.md` §5 |
| Preferences | **9**, lexicographically ordered by the policy | `models/routing-constraint-model.md` §6 |
| Precedence stages | **9** (0–8); stages 1–5 globally fixed, stage 6 policy-owned | `models/routing-precedence-and-fallback.md` §2 |
| Candidate Universe Definition elements | 8 | `models/routing-precedence-and-fallback.md` §1 |
| Availability classes | 4 | `models/routing-precedence-and-fallback.md` §2 |
| Fallback kinds | 5 | `models/routing-precedence-and-fallback.md` §3 |
| Model diversity values | 6 | `models/review-diversity-and-criticality.md` §2 |
| Deployment classes | 5 + declared | `models/_templates/deployment-profile-template.md` |
| Residency / jurisdiction fields | 6 | `models/_templates/deployment-profile-template.md` |
| Region / residency classes | 5 | `models/_templates/deployment-profile-template.md` |
| Cost / latency bands | 4 + 4 | `models/_templates/model-profile-template.md` |
| Routing Decision elements | **31** | `models/_templates/routing-decision-template.md` |
| Enforceable constraints | **43** | `models/_standards/common-model-governance-constraints.md` |

## 3. Artifacts

| File | Purpose |
|---|---|
| `architecture/model-registry-router.md` | Master architecture: identity separation, routing chain, eligibility, upstream integration, privacy, human control, reproducibility |
| `models/model-capability-taxonomy.md` | Capability families, claim classes, limitations and prohibited contexts |
| `models/model-lifecycle-and-versioning.md` | Lifecycle, versioning, aliases, anti-lock-in, pinning, incidents |
| `models/routing-constraint-model.md` | Hard constraints, soft preferences, sources, conflicts |
| `models/routing-precedence-and-fallback.md` | Precedence, tie-break, availability, fallback, blocking |
| `models/review-diversity-and-criticality.md` | Model diversity against Phase 6 independence; criticality bands |
| `models/evaluation-evidence-model.md` | Evidence classes, dimensions, confidence, freshness |
| `models/_standards/common-model-governance-constraints.md` | 33 inherited rules |
| `models/_templates/` × 5 | Model, Provider, Deployment, Routing Policy, Routing Decision |
| `models/exemplars/` × 9 | Worked Routing Decisions, each proving one boundary |
| `models/master-model-routing-universe.md` | This inventory |
| `reviews/phase-9-foundation-self-check.md` | Self-check pointing at the harness |
| `validation/phase_9_validation.py` | Deterministic validation harness |

## 4. Two things this architecture cannot express

Stated as inventory, because their absence is a design output rather than an omission:

1. **A ranking of models.** A profile is a vector of claims across 24 dimensions, with evidence of differing classes and ages. No composite exists, no ordering is derivable, and **"the best model" is not a sentence this vocabulary can form.**
2. **Partial eligibility.** A candidate meets every eligibility constraint or is not a candidate. "Closest fit", "fewest violations" and "best available" have no representation — **and neither does "eligible pending an exception"**, which is why a governed act changes the requirement *before* re-evaluation rather than justifying a selection afterwards.
3. **An ordering of sensitivity classes.** Phase 8 defines none and Phase 9 imposes none, so "maximum sensitivity" and "at or above" cannot be expressed. Eligibility is a subset test with obligations.

The first is why `models/evaluation-evidence-model.md` refuses a composite score; the second is why `BLOCKED_FOR_ROUTING` exists.

## 5. What Phase 9 inherits and does not change

| Inherited | From | Treatment |
|---|---|---|
| Registry separation, and the Model Registry forward reference | `architecture/registry-separation.md` §8 (Phase 2) | **Resolved by defining the registry.** The approved file is not modified |
| Criticality bands | `architecture/project-criticality-policy.md` (Phase 3) | Used, not redefined. Bands raise routing rigour only |
| Role independence from model and provider | `architecture/registry-separation.md` §2 | Enforced rather than restated: **no Role Card is rewritten to name a model** |
| Review independence classes | Phase 6 | Referenced. **No class added, none removed, no review status set or changed** |
| Decision Rights | Phase 7 | Referenced. **No Right carded, no authority granted.** A Routing Decision is not a Decision Record |
| Sensitivity classes, freshness model, `AI_SUGGESTION` and origin | Phase 8 | Used unchanged. No new sensitivity class, no new freshness state, no new epistemic type |

## 6. Forward reference resolved

`architecture/registry-separation.md` §8 (approved, Phase 2) promised a Model Registry describing "available runtime models and their capabilities, constraints, cost and routing suitability", and stated that "models are replaceable execution runtimes and do not define the roles themselves".

Phase 9 delivers each clause: **capabilities** as a 24-family taxonomy with evidence classes; **constraints** as 22 hard and 8 soft, with precedence; **cost** as semantic bands, never prices; **routing suitability** as eligibility rather than ranking; and **replaceability** through stable IDs, aliases, and the deployment-carries-sensitivity rule that lets a provider be substituted without touching anything above the registry.

Also relevant and unchanged: Phase 2 lists **Model Router** as a System Control Profile (§1). Phase 9 defines what that profile would route against; it does not implement the profile, and `ROUTER != ORCHESTRATOR` keeps the two apart.

## 7. Deliberately not built

| Not built | Why |
|---|---|
| Any Model, Provider or Deployment Profile | §1 — evidence first, profiles after |
| Any Routing Policy instance | Policies are organisational; a default would be a silent policy decision |
| A ranking, score or leaderboard | §4 |
| A sensitivity ordering or ceiling | §4 — Phase 8's classes are an unordered multi-label set and are used as one |
| An evaluation system, benchmark or harness | Phase 9 defines what evidence *means*; producing it is later work |
| Availability monitoring, health checks, failover | Runtime |
| Cost tables, price feeds, billing | Bands only, by construction |
| Any provider SDK, API, credential, endpoint or address | Out of scope by construction |
| An orchestrator, queue or execution engine | Phase 11 |
| Storage, schema or persistence for any of it | Phase 10 |
| IAM, authentication or access control | Never Phase 9's |

## 8. Handed to later phases

1. **A governed profile-population pass** — create Model, Provider and Deployment Profiles with evidence, under this architecture. Not mass generation.
2. **Routing Policy authoring** — organisational policies, including provider allow and prohibit lists and the accepted evidence classes per band.
3. **Phase 10 (storage / infrastructure)** — persistence for profiles, policies and Routing Decisions; retention of routing history.
4. **Phase 11 (orchestrator)** — what work happens, in what order, by which Role, with what concurrency and retry. **The Router answers none of this.**
5. **Runtime** — provider invocation, availability observation, decision recording. Validates against these semantics; does not mutate them.

## 9. Status

Every Phase 9 artifact is `PROPOSED`. Nothing is APPROVED or CANONICAL. No model or provider is endorsed, no profile exists, and the nine exemplars are illustrations over synthetic identifiers.
