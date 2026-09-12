# Routing Constraint Model

Status: PROPOSED — Phase 9 architecture candidate
Version: 0.1
Inherits: `standard.model.common_constraints@0.1`

## 1. Three kinds of requirement, not two

The first draft had two kinds and put `HUMAN_SELECTION_REQUIRED` among the filters — where it cannot work, because it filters nothing. The independent audit was right: a requirement that every candidate passes and that can still be unmet is **not an eligibility constraint at all**.

| Kind | What it does | Failure to meet it |
|---|---|---|
| **`ELIGIBILITY_CONSTRAINT`** | **Filters** the candidate set | The candidate is **ineligible**. Not disfavoured — ineligible |
| **`PREFERENCE`** | **Ranks** candidates already eligible | The candidate ranks lower and stays eligible |
| **`ROUTING_ACT_REQUIREMENT`** | Requires **an act** before a selection can finalise | **No selection is final.** The candidate set is unchanged; routing does not complete |

> **A preference may never override an eligibility constraint, and no accumulation of preferences ever makes an ineligible candidate eligible.**

> **An act requirement never changes eligibility in either direction.** It cannot make an ineligible candidate usable, and it cannot disqualify an eligible one. What it withholds is **completion**.

Ranking happens **only inside the eligible set**, so no weighting, scoring or aggregation can reach a candidate an eligibility constraint removed — the structural reason cost cannot buy its way past privacy.

## 2. Eligibility constraints

Each carries an **exceptionability class** (§5). The class is a property of the **source** of the requirement, not of the constraint's name.

| Constraint | Satisfied when | Exceptionability |
|---|---|---|
| `REQUIRED_CAPABILITY` | The profile claims the named capability at or above the required class, on evidence the policy accepts | Derived from source (§5.2) |
| `REQUIRED_MODALITY` | The profile supports the named input and output modalities | `ABSOLUTELY_NON_WAIVABLE` — a text-only model cannot be excepted into reading an image |
| `REQUIRED_CONTEXT_CLASS` | The profile's context class meets the minimum | Derived from source |
| `REQUIRED_TOOL_USE` | The profile claims tool calling at the required class | Derived from source |
| `REQUIRED_STRUCTURED_OUTPUT` | The profile claims schema adherence at the required class | Derived from source |
| `REQUIRED_DEPLOYMENT_CLASS` | The deployment is of a required class | Derived from source |
| `REQUIRED_JURISDICTION` | The deployment's residency satisfies the allowed set and violates no prohibited entry (§4) | Derived from source; legal sources are non-waivable |
| `SUPPORTED_SENSITIVITY_CLASSES` | The deployment **explicitly supports every** sensitivity label the material carries (§3) | Derived from source; legal and third-party sources are non-waivable |
| `REQUIRED_HANDLING_CONTROLS` | Every handling obligation the material's labels impose is satisfied by the deployment (§3) | Derived from source |
| `PROHIBITED_SENSITIVITY_CLASSES` | The material carries **no** label the deployment prohibits | `ABSOLUTELY_NON_WAIVABLE` |
| `REQUIRED_DATA_HANDLING_POSTURE` | The **effective deployment posture** (§3.4) satisfies the required retention, training and logging terms | Derived from source |
| `PROVIDER_ALLOWED` / `PROVIDER_PROHIBITED` | The provider is on the allow list / not on the prohibit list | Derived from source |
| `MODEL_ALLOWED` / `MODEL_PROHIBITED` | As above, at profile level | Derived from source |
| `MODEL_FAMILY_ALLOWED` / `MODEL_FAMILY_PROHIBITED` | As above, at family level | Derived from source |
| `MINIMUM_REASONING_CLASS` | The reasoning claim meets the minimum | `GOVERNED_EXCEPTION_POSSIBLE` where the policy declares the class exceptionable |
| `MINIMUM_RELIABILITY_CLASS` | The reliability claim meets the minimum | `GOVERNED_EXCEPTION_POSSIBLE` where the policy declares it |
| `MINIMUM_CONTEXT_CAPACITY_CLASS` | The context class meets the minimum | `ABSOLUTELY_NON_WAIVABLE` where exceeding capacity would truncate material silently |
| `MODEL_DIVERSITY_REQUIRED` | The candidate differs from a **named prior Routing Decision's** selection at the required level | `GOVERNED_EXCEPTION_POSSIBLE` — and see §5.4 |
| `PROVIDER_DIVERSITY_REQUIRED` | The candidate's provider differs from that prior selection's — **only where justified, never a default** | `GOVERNED_EXCEPTION_POSSIBLE` |
| `NO_EXTERNAL_PROVIDER` | The deployment class is internal, private or local | Derived from source |
| `MAX_COST_CLASS` / `MAX_LATENCY_CLASS` | At or below the bound — **an eligibility constraint only where a task policy declares a bound** (§6) | `OPERATOR_CONFIGURABLE_WITHIN_POLICY` |
| `LIFECYCLE_ROUTABLE` | The profile's primary lifecycle state permits new routing, and no restriction annotation excludes this context | `ABSOLUTELY_NON_WAIVABLE` for `SUSPENDED`; otherwise derived from source |
| `AVAILABILITY_ELIGIBLE` | The candidate's availability class satisfies the policy's requirement for this band | `OPERATOR_CONFIGURABLE_WITHIN_POLICY` |

### Three that are commonly misread

- **`SUPPORTED_SENSITIVITY_CLASSES` is a property of the deployment, not of the model.** The same model behind two deployments has two different answers, which is what lets a provider change without the architecture changing.
- **`REQUIRED_DATA_HANDLING_POSTURE` reads the effective deployment posture**, after provider-level constraints are applied (§3.4). It is never assumed from a provider's marketing, a default setting, or the absence of a statement: **unstated is not satisfied**.
- **`PROVIDER_DIVERSITY_REQUIRED` is never a default.** It is the strongest diversity constraint and the easiest to impose reflexively; it applies only where a policy states the justification.

## 3. Sensitivity: set compatibility, never an ordinal maximum

The first draft used a single `MAX_DATA_SENSITIVITY_ALLOWED` and compared "at or above". **That was wrong, and the audit was right to call it invalid.** Phase 8 defines **no total order** over its sensitivity classes: an item "may carry several", and `PERSONAL_DATA`, `PRIVILEGED` and `THIRD_PARTY_RESTRICTED` each carry obligations *independent of every other class*. There is no sense in which `TRADE_SECRET` is "above" `PERSONAL_DATA`, and a deployment approved for one is told nothing about the other.

**Phase 8's semantics are used unchanged.** Phase 9 imposes no order on them and adds no class.

### 3.1 The three sets

| Declared on | Field | Meaning |
|---|---|---|
| Material / task | **Applicable sensitivity labels** | Every Phase 8 label the material carries — often several |
| Deployment | **`SUPPORTED_SENSITIVITY_CLASSES`** | The labels this deployment is **explicitly approved** to handle, each with what approved it |
| Deployment | **`PROHIBITED_SENSITIVITY_CLASSES`** | Labels this deployment must never handle, whatever else it supports |

### 3.2 The eligibility rule

> **A deployment is eligible only if every applicable sensitivity label is explicitly supported, every handling obligation those labels impose is satisfied, and no prohibited condition applies.**

It is a **subset test with obligations**, not a comparison:

1. **Every label must be individually supported.** `PERSONAL_DATA + PRIVILEGED` requires **both** regimes simultaneously; support for either alone is insufficient.
2. **Support for one label implies support for no other.** `TRADE_SECRET` approval says nothing about `PERSONAL_DATA`.
3. **No label outranks another by being "higher".** There is no higher.
4. **Unknown support is not support.** A label the deployment has not been assessed for is **unsupported** for routing, and the record says so rather than inferring.
5. **A prohibition wins over any support.** Prohibited and supported for the same label is a defective Deployment Profile, and the safe reading is prohibited.
6. **Compound material takes the union of obligations.** Where two labels impose conflicting handling, Phase 8 governs: the **most restrictive handling applies**, and restrictions arising from `PRIVILEGED` or `THIRD_PARTY_RESTRICTED` **cannot be relaxed by an internal decision at all** — which makes them `ABSOLUTELY_NON_WAIVABLE` here.

### 3.3 Handling obligations

A label may impose obligations beyond the fact of support — retention limits, logging suppression, no-training, deletion rights, sub-processing limits, confidentiality undertakings. `REQUIRED_HANDLING_CONTROLS` tests those, **per label**, against the effective deployment posture. Supporting a label without meeting its obligations is not support.

### 3.4 Effective deployment posture

Data-handling posture exists at three layers and has **one authoritative reading**:

| Layer | Owns |
|---|---|
| **Model Profile** | **Nothing.** Intrinsic technical characteristics only — modality, context, tool use. **No retention, training or logging posture** |
| **Provider Profile** | Provider-level contractual and default posture, and the constraints it places on every deployment beneath it |
| **Deployment Profile** | The **effective posture** — deployment-specific retention, training, logging, tenancy, residency and approved labels |

> **Routing reads the effective deployment posture, after provider-level constraints are applied.** A deployment may be **more** restrictive than its provider's default; it may be less restrictive **only where explicitly evidenced and permitted by the provider-level instrument**, and an unevidenced relaxation is not a posture but a defect.

There is no second source of truth. A generic retention promise on a Model Profile is a defect, not a shortcut.

## 4. Residency and jurisdiction

Residency belongs **primarily to the Deployment Profile**. A Model Profile has no residency; the same model is processed in different places depending on where it is reached.

| Field | Meaning |
|---|---|
| **Exact jurisdiction(s)** | The named legal orders under which processing occurs |
| **Region / residency class** | A broader grouping (`SOVEREIGN`, `REGIONAL_BLOC`, `PRIVATE_TENANT`, `LOCAL_ONLY`, `GLOBAL_UNSPECIFIED`) |
| **Allowed jurisdiction set** | Where the task permits processing |
| **Prohibited jurisdiction set** | Where it must not occur |
| **Cross-border processing** | `FORBIDDEN` / `CONDITIONAL` (conditions stated) / `ALLOWED` |
| **`UNKNOWN_RESIDENCY`** | Not established |
| **Evidence and review-by** | What establishes the above, and when it is re-checked |

Rules:

1. **`UNKNOWN_RESIDENCY` never satisfies a residency requirement.** It is not a permissive default and is never read as "probably fine".
2. **Prohibited outranks allowed.** A jurisdiction in both sets is prohibited, and the overlap is a defect to be corrected rather than resolved case by case.
3. **Exact jurisdiction and region class are not interchangeable.** A region class satisfies a requirement stated over exact jurisdictions **only through an explicit declared mapping**; without one, the requirement is unsatisfied.
4. **Provider-level claims constrain but do not substitute.** A provider's regional assurance narrows what its deployments may claim; **deployment-specific evidence is still required**.
5. **Cross-border processing is assessed separately from the primary jurisdiction.** A compliant primary region with unbounded cross-border processing does not satisfy a residency requirement.

## 5. Exceptionability

The first draft said humans cannot bypass law, privacy, security or contract, and elsewhere spoke generically of Phase 7 exceptions to hard constraints. **Both cannot be true.** The audit was right, and the resolution is that exceptionability is a property of **where the requirement comes from**.

### 5.1 The three classes

| Class | Meaning |
|---|---|
| **`ABSOLUTELY_NON_WAIVABLE`** | **No routing exception exists inside AI-OS.** Not by operator, not by seniority, not by any Phase 7 Right. The correct outcome is `BLOCKED_FOR_ROUTING` |
| **`GOVERNED_EXCEPTION_POSSIBLE`** | The requirement may be **adjusted** by a named, valid Phase 7 Decision Right whose scope covers this constraint class, with bounded effect and an expiry |
| **`OPERATOR_CONFIGURABLE_WITHIN_POLICY`** | Not an exception at all — ordinary choice inside the envelope the policy already permits |

### 5.2 Deriving the class from the source

| Source of the requirement | Class |
|---|---|
| Statute, regulation, or a binding legal obligation | **`ABSOLUTELY_NON_WAIVABLE`** |
| A contractual prohibition binding the entity | **`ABSOLUTELY_NON_WAIVABLE`** |
| `PRIVILEGED` or `THIRD_PARTY_RESTRICTED` handling restriction | **`ABSOLUTELY_NON_WAIVABLE`** (Phase 8: not relaxable by internal decision) |
| An explicit security prohibition adopted as policy | **`ABSOLUTELY_NON_WAIVABLE`** unless the policy itself names a Right that may adjust it |
| A deployment that does not support a required label | **`ABSOLUTELY_NON_WAIVABLE`** — no decision makes an unsupported capability supported |
| Physical impossibility — modality, context capacity | **`ABSOLUTELY_NON_WAIVABLE`** — an exception cannot make a text-only model read an image |
| An internal quality, reliability or diversity threshold | **`GOVERNED_EXCEPTION_POSSIBLE`**, where a Right names that class |
| A cost or latency bound, an availability preference | **`OPERATOR_CONFIGURABLE_WITHIN_POLICY`** |

### 5.3 The rules

1. **A Phase 7 Right cannot create legal authority the legal order does not grant** — Phase 7 says so itself, and Phase 9 adds nothing to it.
2. **Exceptionability is anchored to the source and to a specific named Right.** "A Decision Right exists" is not a basis; *this* Right must cover *this* constraint class.
3. **Unknown or unrecognised exceptionability defaults to `ABSOLUTELY_NON_WAIVABLE`** for routing purposes. The safe reading of an unclassified constraint is the strict one.
4. **Human acknowledgement never changes eligibility.** Acknowledging a degradation records that someone knows; it adjusts no requirement.
5. **An adjustment is bounded and expiring.** It covers this task or context, not a standing relaxation, and the exception's own record says what it covers and until when.

### 5.4 Model diversity is not reviewer independence

`MODEL_DIVERSITY_REQUIRED` is `GOVERNED_EXCEPTION_POSSIBLE`, and adjusting it has **one** effect: the execution-diversity control is reduced, and the Routing Decision records that. **It does not touch reviewer independence**, which is Phase 6's, is an organisational property of who reviews, and **cannot be waived by any routing act whatsoever**. Where a Review Profile requires both, they are **two controls**, and an exception affecting one leaves the other exactly as it was.

## 6. Preferences

| Preference | Ranks toward |
|---|---|
| `PREFER_HIGHER_CAPABILITY_EVIDENCE` | Stronger or fresher evidence on the capabilities the task requires |
| `PREFER_LOWER_COST_CLASS` | Cheaper |
| `PREFER_LOWER_LATENCY_CLASS` | Faster |
| `PREFER_HIGHER_RELIABILITY_CLASS` | More reliable on constrained output |
| `PREFER_LIFECYCLE_PREFERRED` | Profiles carrying the `PREFERRED` routing designation |
| `PREFER_FRESHER_EVALUATION` | More recent capability evidence |
| `PREFER_FEWER_KNOWN_LIMITATIONS` | Fewer applicable limitations bearing on this task |
| `PREFER_EXISTING_DEPLOYMENT` | A deployment already approved for this context |
| `PREFER_LOWER_PROVIDER_CONCENTRATION` | A provider on which less of the eligible registry depends |

**Preferences are applied in a declared order, not weighted** — lexicographic, so a later preference decides only what an earlier one left tied. The **order is owned by the versioned Routing Policy** (§7 of `models/routing-precedence-and-fallback.md`), because the right ordering depends on the work; what is fixed globally is that **every preference runs after every eligibility constraint.**

### When cost or latency becomes an eligibility constraint

`MAX_COST_CLASS` and `MAX_LATENCY_CLASS` are **preferences by default**, and become eligibility constraints only where a **task policy declares a bound**. Even then:

1. **A bound never displaces a governance, privacy, residency, capability, independence or criticality requirement.** It filters within what those allow.
2. **Where a bound leaves nothing eligible, routing blocks.** It does not relax the bound, and it relaxes nothing else to fit inside it. A budget that cannot buy a compliant model has not found a cheaper compliant model; it has found that the work costs more than the budget.
3. **The cheapest eligible model is not automatically preferred, and the most expensive is not automatically best.**

## 7. Act requirements

| Requirement | Requires | Effect if unmet |
|---|---|---|
| `HUMAN_SELECTION_REQUIRED` | A human selects from the eligible set | **No selection finalises.** Routing does not complete |
| `HUMAN_ACKNOWLEDGEMENT_REQUIRED` | A human acknowledges a declared degradation | As above |
| `GOVERNANCE_REVIEW_REQUIRED` | A named governance review occurs before finalisation | As above |

**None of these filters a candidate, and none changes eligibility.** Every candidate may pass them and routing still not complete; no candidate becomes eligible because one was performed. They are conditions on **finalisation**, recorded on the Routing Decision, and a policy declaring one without a process behind it produces a permanent non-completion — which is a policy defect, and a visible one.

## 8. Where requirements come from

| Source | Typical requirements |
|---|---|
| Task or Workflow stage | Capabilities, modality, context class, tool use, structured output, latency |
| Data sensitivity (Phase 8) | Supported and prohibited labels, handling controls, data-handling posture, residency |
| Review Profile (Phase 6) | `MODEL_DIVERSITY_REQUIRED`, occasionally provider diversity, act requirements |
| Criticality band (Phase 3) | Minimum classes, evidence freshness, availability strictness, act requirements |
| Organisational policy | Provider allow and prohibit lists, deployment classes, `NO_EXTERNAL_PROVIDER` |
| Legal or contractual obligation | Jurisdiction, handling posture, prohibited providers — and these arrive `ABSOLUTELY_NON_WAIVABLE` |

**Requirements are declared by the governance that owns the concern and merged by the Routing Policy.** The Router invents none, and drops none it does not understand: **an unrecognised requirement blocks routing**, because the alternative is a silent grant of everything it was meant to prevent.

## 9. Conflicting requirements

Where two eligibility constraints cannot both be met, the result is **`NO_ELIGIBLE_MODEL`** and the conflict is reported. It is never resolved by dropping the harder one, preferring the more recent or more senior source, treating a prohibition as a preference, or selecting the candidate that violates the fewest.

**There is no partial eligibility.** "Closest fit" is not a concept this model contains.

## 10. Status

`PROPOSED`. Implements no matcher, no engine, no scoring function and no runtime.
