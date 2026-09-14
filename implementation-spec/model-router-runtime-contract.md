# Model and Router Runtime Contract

Status: `PROPOSED` — Phase 14 implementation specification
Version: 0.1
Authority: approved Phase 1–13 architecture. Where this document and the approved architecture
differ, the architecture wins and this document is defective.

Closes Phase 13 finding **M-3**.

## 1. The two separations that matter most in practice

> **`ROUTER != ORCHESTRATOR`** — the Router answers *which execution capability is eligible and
> preferred for this bounded piece of work*. It does not decide what work happens, in what
> order, by which Role, or whether it is done.

> **`ROUTING DECISION != DECISION RIGHT`** — a Routing Decision selects a **tool**. It approves
> no work, accepts no risk, satisfies no review, promotes no knowledge, and **creates no
> authority**. A Decision Record is a human governance act under a Phase 7 Right; a Routing
> Decision is a record of tool selection, and the two are never the same object however senior
> the person who made the selection.

And the five that keep a model in its place:

`MODEL != ROLE` · `MODEL != AGENT INSTANCE` · `MODEL != AUTHORITY` ·
`MODEL != REVIEWER IDENTITY` · `MODEL != KNOWLEDGE SOURCE BY DEFAULT` ·
`MODEL != CANONICAL KNOWLEDGE` · `MODEL != PROVIDER != ENDPOINT`

## 2. The routing chain

```
ROLE PROFILE + ASSIGNMENT ATTRIBUTES + SKILL SET + WORKFLOW CONTEXT + TASK CRITICALITY
      -> MODEL REQUIREMENTS
           -> ROUTING POLICY
                -> CANDIDATE UNIVERSE
                     -> ELIGIBLE MODEL SET
                          -> ROUTING DECISION
```

**Rule M-1.** Each arrow is a narrowing, and **the left-hand side never names a model**.
Requirements are expressed in the capability vocabulary. Replacing a vendor changes the registry
and the eligible set and changes **nothing** to the left of `MODEL REQUIREMENTS`.

**Rule M-2.** The implementation must make M-1 checkable: a `routing_request` has no column in
which a model, provider, endpoint or deployment can be named. A caller wishing to "suggest" one
has no field to put it in.

## 3. `routing_request`

Produced by C9, consumed by C7. Recorded only when the act commits (see §7).

| Field | Type | Null | Mut | Notes |
|---|---|---|---|---|
| `routing_request_ref` | `RoutingRequestRef` | NO | IMM | |
| `run_ref`, `work_item_ref` | refs | NO | IMM | Exact binding; validated by lookup |
| `capability_requirements` | structured | NO | IMM | Capability vocabulary only — **no model, provider, endpoint or deployment field exists** |
| `role_ref` + version | ref pair | NO | IMM | The Role whose work this is |
| `skill_refs` + versions | set | YES | IMM | |
| `criticality_band` | enum | NO | IMM | Phase 3 bands, used not redefined |
| `scope_binding` | scope path + labels + residency | NO | IMM | Carried from the run, never widened |
| `routing_policy_ref` + `policy_version` | ref pair | NO | IMM | The versioned policy in force |
| `requested_at` | timestamp | NO | IMM | |

## 4. Eligibility input and evaluation

**Rule M-3 — one rule.** A candidate is eligible when it satisfies **every** eligibility
constraint. Preferences then rank what is left. Act requirements then withhold or release
finalisation. **There is no partial eligibility and no "closest fit."**

Three kinds of requirement, never confused:

| Kind | Does |
|---|---|
| **Eligibility constraint** | Filters. Fails closed |
| **Preference** | Ranks what survived filtering. Never restores an excluded candidate |
| **Act requirement** | Withholds or releases *finalisation* — human selection, acknowledgement, governance review — **without touching eligibility in either direction** |

### 4.1 Candidate universe binding

**Rule M-4.** Filtering presupposes a set. **Every Routing Decision binds a Candidate Universe
Definition first**: a deterministic registry state reference, an inclusion rule, the enumerated
set, omission reasons, and a completeness result.

A load failure yields `CANDIDATE_UNIVERSE_INCOMPLETE`, which is deterministic: the run is written
`BLOCKED` and **then** `ESCALATED`, posture `GATE_UNSATISFIED`, in the same transaction as the
decision (§5.2, Rule M-7a; `api-command-contracts.md` Rule Q-17b). It is never a choice between
the two, and never
silently shrinks the universe. "Where practical" does not meet the requirement: given the same
registry state reference and the same universe definition version, the same enumeration results.

### 4.2 Precedence

Stages **1–5 are globally fixed**, in this order: legality → sensitivity/handling/residency →
capability → independence → lifecycle and availability. **Stage 6, the preference order, is owned
by the versioned Routing Policy** and is **lexicographic, not weighted**.

**Rule M-5.** A later stage cannot restore what an earlier one removed, and no preference
ordering reaches a candidate an eligibility constraint excluded. The implementation evaluates
stages as successive filters over an ordered list and never as a scoring function — a weighted
score can always trade a legality failure against a preference, which is exactly the behaviour
the fixed stages exist to prevent.

**Rule M-6 — no fallback outside the eligible set.** When nothing is eligible the answer is
`NO_ELIGIBLE_MODEL`, which the orchestrator turns into a **block** — not into a second attempt
with the constraints relaxed.

## 5. `routing_decision` — with the six-part reproducibility set

Append-only; no version; a correction is a new linked record.

| # | Field | Type | Null | Mut | Notes |
|---:|---|---|---|---|---|
| 1 | `routing_decision_ref` | `RoutingDecisionRef` | NO | IMM | |
| 2 | `routing_request_ref` | ref | NO | IMM | **Validated by lookup in this run's own requests** |
| 3 | `run_ref`, `work_item_ref` | refs | NO | IMM | Must equal the request's |
| 4 | `decided_by` | `RouterRef` | NO | IMM | **Check: kind must be `router`.** An `OrchestratorRef` or `HumanAuthorityRef` is rejected at the database |
| 5 | `router_version` | version id | NO | IMM | |
| 6 | `outcome` | enum §5.2 | NO | IMM | |
| **20** | `model_profile_ref` | `ModelProfileRef` (`model.<stable_snake_case_name>`) | NO* | IMM | **Six-part element 1** — stable Model Profile identity, in Phase 9's own identity scheme |
| **21** | `model_profile_registry_version` | version id | NO* | IMM | **Element 2** — the version of the AI-OS record |
| **22** | `originator_release_identity` | text | NO* | IMM | **Element 3** — the originator's release identity that the profile described **at that version** |
| **23** | `offering_mapping_ref` + `offering_mapping_version` | ref pair | NO* | IMM | **Element 4** |
| **24** | `provider_profile_ref` + `provider_profile_version` | ref pair | NO* | IMM | **Element 5** |
| **25** | `deployment_profile_ref` + `deployment_profile_version` | ref pair | NO* | IMM | **Element 6** |
| 26 | `routing_policy_ref` + `policy_version` + `declared_preference_order` | structured | NO | IMM | |
| 27 | `selection_reason` | text | NO | IMM | Which preference or tie-break decided it |
| 28 | `candidate_universe` | structured | NO | IMM | Registry state reference, inclusion rule, enumerated set, omission reasons, completeness result |
| 29 | `eligibility_evidence` | structured | NO | IMM | Per-candidate: which constraint excluded it, at which stage |
| 30 | `act_requirements` | structured | YES | IMM | Which were outstanding, and how released |
| 31 | `scope_binding_at_decision` | structured | NO | IMM | Recorded value, for re-evaluation under reclassification |
| 32 | `decided_at` | timestamp | NO | IMM | |

\* Elements 20–25 are `NOT NULL` when `outcome = ELIGIBLE_CANDIDATE`, and `NULL` for every
non-eligible outcome — a non-eligible outcome **may not name a model**. This is a check
constraint, both directions.

### 5.1 Why all six elements, stated exactly

A stable ID names a *lineage of records*; a registry version names *a record*; **only the
underlying release identity names the thing that actually ran.** Recording the first two without
the third leaves the question open precisely when it matters — after a provider has changed
something and the profile has moved on. The mapping, provider and deployment versions complete
it: the same release reached through a different mapping or a re-termed deployment is a
different set of governance facts, even where the model is identical.

**Rule M-7.** All six are `NOT NULL` together for an eligible outcome. Partial recording is
rejected at write, not tolerated and back-filled.

### 5.2 Router outcomes

| Outcome | Orchestrator effect |
|---|---|
| `ELIGIBLE_CANDIDATE` | Continue; a Model Invocation may be constructed |
| `NO_ELIGIBLE_MODEL` | `BLOCKED`, posture `GATE_UNSATISFIED` |
| `CANDIDATE_UNIVERSE_INCOMPLETE` | `BLOCKED`, **then** `ESCALATED`, posture `GATE_UNSATISFIED`; never a shrunken universe |
| `NO_APPLICABLE_DECISION_RIGHT` | `BLOCKED`, **then** `ESCALATED`, posture `AUTHORITY_ABSENT` |
| `ACT_REQUIREMENT_OUTSTANDING` | `WAITING`, wait reason `WAITING_FOR_DEPENDENCY`, with the act requirement as the named wait subject |

**Rule M-7a — the orchestrator effect is deterministic and commits with the decision.** "`BLOCKED`
or `ESCALATED`" was a choice left to an implementation, and an implementation that chose
`BLOCKED` alone would leave an incomplete candidate universe waiting for someone who was never
told. Each outcome above has exactly one mapping, the number of run-state appends it requires is
*s* in `api-command-contracts.md` Rule Q-17b, and the appends commit **in the same transaction as
the Routing Decision** (Rule Q-17c). No committed state exists in which a non-selection decision
is durable and the run is still eligible to continue.

### 5.3 Reproducibility — what is and is not claimed

| Property | Claimed? | Basis |
|---|---|---|
| **Routing reproducibility** — same requirements, registry state and policy version select the same candidate | **Yes** | The deterministic tie-break exists for this |
| **Model-output reproducibility** — the same input yields the same output | **No.** Not claimed, not achievable, not architecture's to promise | |

**Rule M-8.** No document, API field, metric or log in this system asserts model-output
determinism, and no governed behaviour depends on it.

## 6. Model Invocation and Model Result

### 6.1 `model_invocation`

| Field | Type | Null | Mut | Notes |
|---|---|---|---|---|
| `model_invocation_ref` | ref | NO | IMM | |
| `routing_decision_ref` | ref | NO | IMM | **Must be the decision this run recorded**, found by lookup |
| `run_ref`, `work_item_ref` | refs | NO | IMM | Must match the decision's |
| `deployment_profile_ref` + version | ref pair | NO | IMM | Copied from element 25; the gateway may not choose |
| `offering_mapping_ref` + version | ref pair | NO | IMM | Copied from element 23; the exposure actually used |
| `model_profile_ref` + `model_profile_registry_version` | ref pair | NO | IMM | Copied from elements 20–21 |
| `expected_release_identity` | recorded external value | NO | IMM | Copied from element 22. What the decision said would run |
| `scope_binding` | structured | NO | IMM | Residency and sensitivity carried into the call |
| `prompt_context_ref` | ref | NO | IMM | What was sent, by reference; never inline secrets |
| `idempotency_key` | text | NO | IMM | §7 |
| `requested_at` | timestamp | NO | IMM | |

**Rule M-9.** C8 executes against the deployment the **recorded** Routing Decision selected. It
performs no selection, no fallback, no "try the other provider", and no silent downgrade. A
deployment that is unavailable produces a failure with a retry class, not a substitution.

**Rule M-9a — the invocation is staged, not transactional.** A model call leaves the system, so
`InvokeModel` is not one local transaction that writes an invocation and a result. It commits
**intent only**; the provider call happens outside any transaction; the observed outcome and any
result are later, separate commits; and an unknown outcome is reconciled rather than assumed.
The five stages, the four identities, the transaction boundaries and the crash behaviour at
every boundary are specified in `api-command-contracts.md` §5.5, and the per-branch writes and
audit counts in `persistence-and-transaction-model.md` §7.2.

**Rule M-9b — a timeout is not proof that nothing happened.** A timeout, a reset, a dropped
response and a crash between the call and its recording all produce
`ATTEMPTED_OUTCOME_UNKNOWN`. The system neither re-runs the call (risking a duplicate external
effect) nor proceeds as though content exists. This is Phase 11's rule applied where the
uncertainty actually arises.

**Rule M-9c — the Model Result exists only on a confirmed applied outcome.** There is no path
that writes a result from an unknown attempt, and none that writes one in the same transaction
as the intent.

### 6.2 `model_result`

| Field | Type | Null | Mut | Notes |
|---|---|---|---|---|
| `model_result_ref` | `ModelResultRef` | NO | IMM | Stable identity; duplicate is refused |
| `model_invocation_ref` | ref | NO | IMM | |
| `routing_decision_ref` | ref | NO | IMM | |
| `run_ref`, `work_item_ref` | refs | NO | IMM | |
| `model_profile_ref` + `model_profile_registry_version` | ref pair | NO | IMM | **Verified equal to elements 20–21 of the recorded Routing Decision** before the write |
| `offering_mapping_ref` + version | ref pair | NO | IMM | **Verified equal to element 23** |
| `provider_profile_ref` + version | ref pair | NO | IMM | **Verified equal to element 24** |
| `deployment_profile_ref` + version | ref pair | NO | IMM | **Verified equal to element 25** |
| `observed_release_identity` | recorded external value | NO | IMM | The originator release identity **as observed at invocation**. Compared against element 22 — see Rule M-11 |
| `release_identity_match` | `MATCHES` \| `DIVERGED` | NO | IMM | The result of that comparison, recorded rather than implied |
| `content_ref` | ref | NO | IMM | Content stored as an artifact, not inline in the governance row |
| `epistemic_type` | enum | NO | IMM | **Check: must be `AI_SUGGESTION`** |
| `origin` | enum | NO | IMM | **Check: must be `AI_GENERATED`** |
| `governance_state` | enum | NO | IMM | **Check: must be `DRAFT`** |
| `produced_at` | timestamp | NO | IMM | |

**Rule M-10.** A Model Result **satisfies no gate of any kind** — not a review gate, not a
decision gate, not a human-work gate, not a prerequisite gate. This is a constraint on the gate
evidence contract (`orchestrator-runtime-contract.md` §6), not a convention in calling code.

**Rule M-11 — lineage is checked against fields the Routing Decision actually persists.** Before
a Model Result is written, five of the decision's recorded elements are compared for equality:
Model Profile identity and registry version (20–21), offering mapping and version (23), provider
profile version (24) and deployment profile version (25). Any inequality is a lineage error and
the result is refused; it is not recorded with a warning. There is no comparison against a
`model_ref`, because Phase 9 defines no such registry identity (`domain-identity-model.md`
Rule I-5) and the Routing Decision therefore holds none.

**Rule M-11a — the sixth element is compared differently, and deliberately.** Element 22, the
originator release identity, is what the decision *recorded would run*. The gateway records what
it *observed*. These are compared and the outcome is stored as `release_identity_match`:

| Outcome | Meaning | Effect |
|---|---|---|
| `MATCHES` | The exposure ran the release the decision named | Ordinary |
| `DIVERGED` | The provider exposed a different release without a release change the consumer could see | **`PROVIDER_VERSION_CHANGE` fires**; the result is recorded with the divergence, the run `BLOCK`s, and the mapping is referred for review |

This is Phase 9 §0 rule 7 applied at the only point where the divergence is observable, and it
is why the result stores an observation rather than a copy. A specification that simply required
element 22 to equal itself would check nothing: the gateway would have written the expected
value into the observed field, and a silent backend change would be invisible — which is exactly
the failure Phase 9 names.

**Rule M-11b — divergence is a `BLOCK`, not a warning.** It is Phase 11 race 8 in a different
guise: a result produced under constraints that may no longer hold is re-evaluated, and where
the new facts would have made the candidate ineligible it is not used.

## 7. Idempotency and at-most-once for invocation

A model call is an external effect. Its retry class is declared by the step; where it is
`IDEMPOTENT_AT_LEAST_ONCE` the invocation carries an idempotency key and repetition is safe
**because the receiver makes it so**, not because the sender tried once.

**Rule M-12.** The `model_result_ref` carries a durable uniqueness constraint. A duplicate
arriving from a retry finds the first and fails the write; it does not produce a second result.
`persistence-and-transaction-model.md` §5.2.

**Rule M-13 — one lifecycle, and every branch of it.** `route()` follows construct → validate →
preflight → commit. The Routing Request is **prospective** until the Router's answer has been
fully validated (type, request identity, run and Work Item binding, Router identity, six-part
completeness on a selection); then request, decision and their events commit as **one
transaction**.

There is **no separate command that persists a Routing Request.** An earlier revision had one,
which contradicted this rule in the plainest way: a request could exist that no decision ever
answered. The prospective envelope is constructed inside `route()` and reaches storage only with
an answer. The branches are specified once, in `api-command-contracts.md` §5.4 Rule Q-17 —
and a count is deliberately not stated here, because a stated count is the thing that goes stale
when a branch is added. This contract encodes the same rows:

| Branch | Answer | Request durable? | Decision written? |
|---|---|---|---|
| B1 | Invalid — malformed, foreign Router, identity mismatch, incomplete six-part set — on a first submission | **No** | **No** |
| B1r | The same invalidity **after** a request is already durable | Already durable, **unchanged**; the ordinal is **not** advanced | **No** |
| B2 | Valid `ELIGIBLE_CANDIDATE`, first submission | Yes | Yes |
| B3 | Valid non-selection — `NO_ELIGIBLE_MODEL`, `CANDIDATE_UNIVERSE_INCOMPLETE`, `NO_APPLICABLE_DECISION_RIGHT`, `ACT_REQUIREMENT_OUTSTANDING` | Yes | Yes, **with the run-state appends of Rule Q-17b** |
| B4s | Valid `ELIGIBLE_CANDIDATE` re-submitted against an already durable request | Already durable | Yes, at the next ordinal |
| B4n | A valid non-selection re-submitted against an already durable request | Already durable | Yes, at the next ordinal, **with the same run-state appends as B3**

**Rule M-13d — an invalid answer leaves a durable request exactly as it found it.** B1r writes
nothing: the Routing Request stands at its current version, no Routing Decision is created, and
`submission_ordinal` is not advanced, so the next valid submission takes the ordinal the invalid
answer did not consume. One refusal execution event is appended, and it is coordination history
rather than evidence (Rule O-25a). Advancing the ordinal would leave a U6 gap no record explains.

**Rule M-13a — a valid refusal is recorded.** Phase 11
`orchestration/model-router-invocation-boundary.md` §3: "A Routing Decision, **or a refusal.
Both are recorded**, and the refusals are the important half." Why a run blocked for routing is
a governed fact; a blocked run whose reason was never written cannot be told from a stall.

**Rule M-13b — an invalid answer is not a refusal.** It is the absence of an answer. Committing
a request for it would leave a decision-shaped artifact that no decision answers, which is
exactly what B1 exists to prevent.

**Rule M-13c — a retry re-submits the same request.** Phase 11 §5 rule 1. The request identity
is stable across submissions; each submission's answer is a **new** Routing Decision carrying a
`submission_ordinal`, and **every attempt's decision is recorded** (§5 rule 3), because a
diversity check evaluates against the decision that produced the artifact under review — not the
last attempt that happened to run. Uniqueness is therefore
`UNIQUE (routing_request_ref, submission_ordinal)`, and **not** one decision per request.

## 8. Provider independence — adapter contract

**Rule M-14.** The adapter contract is expressed in the capability and deployment vocabulary and
names no vendor. A provider adapter implements:

| Operation | Input | Output | May never |
|---|---|---|---|
| `enumerate_offerings(registry_state_ref)` | Registry state reference | Offering mappings with versions | Invent an offering not in the registry |
| `describe_deployment(deployment_ref, version)` | Ref pair | Residency, sensitivity posture, availability | Assert a residency the Deployment Profile does not declare |
| `invoke(model_invocation)` | The recorded invocation | Raw content + originator release identity as observed | Choose a model; retry an authority-bearing act; alter the scope binding |

**Rule M-15.** No provider name, SDK, endpoint URL, model family name or vendor-specific
parameter appears in any governance object, schema column, API contract or routing rule. A
vendor appears only inside a Provider Profile and a Deployment Profile, which are data.

**Rule M-16.** Swapping a provider or a model **cannot change the Role's professional or legal
authority**, because authority is not a property of the runtime that executed the work. There is
no code path by which a model identity reaches a holder-eligibility evaluation.

## 9. Divergences from the Phase 12 reference implementation

| # | Phase 12 reference | This specification | Why |
|---:|---|---|---|
| D1 | `RoutingDecision` carries `model` and `model_profile` only — 2 of the 6 reproducibility elements, both unversioned | Elements 20–25 in full, `NOT NULL` together | Phase 9 routing-decision template §5; Phase 11 §7; Phase 13 M-3 |
| D5 | `ModelRef` is a stable governed reference distinct from `ModelProfileRef` | The Model Profile carries Phase 9's `model.<...>` identity; the release is a recorded external value with no registry ID | Phase 9 §0 layers 2–3; Rule I-5 |
| D2 | No candidate universe, eligibility evidence, act requirements or policy version on the decision | Fields 26–31 | Phase 9 `routing-precedence-and-fallback.md` §1 |
| D3 | `Canonicality`/`Origin` on the model result | `epistemic_type` / `origin` / `governance_state` on the approved axes | Phase 8; Phase 13 M-1 |
| D4 | Router adapter is a stub with an eligible-set dict | The §8 adapter contract | Provider independence |
