# AI-OS Model Registry and Router

Status: PROPOSED — Phase 9 architecture candidate
Version: 0.1
Depends on: approved Phase 3 Role Registry, Phase 4 Skill Registry, Phase 5 Workflow Registry, Phase 6 Handoff & Review architecture, Phase 7 Decision Rights architecture, Phase 8 Memory & Canonical Governance

## Purpose

`architecture/registry-separation.md` §8 has said since Phase 2 that a Model Registry would "describe available runtime models and their capabilities, constraints, cost and routing suitability", and that "models are replaceable execution runtimes and do not define the roles themselves". Six phases have been written on that promise: every Workflow, Handoff, Review Profile and Decision Right card carries a non-runtime statement disclaiming model routing, and Phase 7 states that no model may hold a Decision Right by model identity alone.

Phase 9 makes the promise real. It defines how AI-OS **describes models and chooses among them** — and it does so without naming a vendor, because an architecture that names one has already lost the property it exists to protect.

Phase 9 executes nothing. It is the semantic control layer a future runtime routes against.

## The separation this phase must preserve

```
ROLE != SKILL != WORKFLOW != HANDOFF != REVIEW PROFILE != DECISION RIGHT != KNOWLEDGE
     != MODEL PROFILE != MODEL CAPABILITY != ROUTING POLICY != ROUTING DECISION
     != PROVIDER != ENDPOINT != RUNTIME
```

| Object | Is |
|---|---|
| **Model Profile** | A versioned description of **one execution capability**, with claims, evidence and limitations |
| **Model Capability** | A named dimension on which a claim may be made |
| **Provider Profile** | The organisation operating a deployment, with its contractual and data-handling posture |
| **Deployment Profile** | A conceptual **target** — hosted, tenant, private, local, sovereign — with residency and sensitivity properties |
| **Routing Policy** | A versioned, reusable rule set: what is eligible, what is preferred |
| **Routing Decision** | A record that **one task instance** selected one candidate, and why |
| **Runtime** | Execution. Out of scope |

### The seven denials

| | |
|---|---|
| **`MODEL != ROLE`** | A Role is a reusable professional profile with methodology, scope and owned conclusions. A model is a replaceable execution capability. Roles are not staffed by models; models execute work a Role defines |
| **`MODEL != AGENT INSTANCE`** | The profile is a type; a running instance is not the registry's object |
| **`MODEL != AUTHORITY`** | Phase 7: no model holds a Decision Right **by being capable, by being trusted, or by being the thing that reached the gate** |
| **`MODEL != REVIEWER IDENTITY`** | A model may execute a review task. The **reviewer** is the Role and human accountability structure Phase 6 defines, and diversity of models is not independence of reviewers |
| **`MODEL != KNOWLEDGE SOURCE BY DEFAULT`** | Model output is `AI_SUGGESTION` with `ORIGIN: AI_GENERATED`. A model is not a source; a source is material the entity holds |
| **`MODEL != CANONICAL KNOWLEDGE`** | Nothing a model emits is canonical, and no capability evidence shortens the promotion path |
| **`MODEL != PROVIDER != ENDPOINT`** | One family may exist through several providers; one provider may expose many models; one model may be reachable at several deployments with different residency and sensitivity properties |

### The two that matter most in practice

> **`ROUTER != ORCHESTRATOR`** — The Router answers *which execution capability is eligible and preferred for this bounded piece of work*. It does not decide what work happens, in what order, by which Role, or whether it is done. That is Phase 5's for coordination and Phase 11's for execution.

> **`ROUTING DECISION != DECISION RIGHT`** — A Routing Decision selects a tool. It **approves no work, accepts no risk, satisfies no review, promotes no knowledge, and creates no authority.** A Decision Record is a human governance act under a Phase 7 Right; a Routing Decision is a record of tool selection, and the two are never the same object however senior the person who made the selection.

## 1. Component documents

| Document | Owns |
|---|---|
| `models/model-capability-taxonomy.md` | 24 capability families, 4 claim classes, limitations |
| `models/model-lifecycle-and-versioning.md` | 8 lifecycle states, versioning, aliases, anti-lock-in, incidents |
| `models/routing-constraint-model.md` | Hard constraints, soft preferences, and the rule between them |
| `models/routing-precedence-and-fallback.md` | 8-stage precedence, availability, fallback, blocking |
| `models/review-diversity-and-criticality.md` | Model diversity vs Phase 6 independence; criticality bands |
| `models/evaluation-evidence-model.md` | 6 evidence classes, 11 dimensions, confidence, freshness |
| `models/_standards/` | The rules every model artifact inherits |
| `models/_templates/` | Model, Provider, Deployment, Routing Policy, Routing Decision |
| `models/master-model-routing-universe.md` | Inventory, forward reference resolution, deferred work |

## 2. The routing chain

```
ROLE PROFILE + ASSIGNMENT ATTRIBUTES + SKILL SET + WORKFLOW CONTEXT + TASK CRITICALITY
      -> MODEL REQUIREMENTS
           -> ROUTING POLICY
                -> ELIGIBLE MODEL SET
                     -> ROUTING DECISION
```

Each arrow is a narrowing, and **the left-hand side never names a model**. Requirements are expressed in the capability vocabulary; the policy turns requirements into constraints; constraints filter candidates; the decision records which candidate and why. Replacing a vendor changes the registry and the eligible set. It changes nothing to the left of `MODEL REQUIREMENTS`.

## 3. Eligibility, in one rule

> **A candidate is eligible when it satisfies *every* hard constraint. Preferences then rank what is left. There is no partial eligibility and no "closest fit".**

Precedence is `models/routing-precedence-and-fallback.md` §1: legality, then sensitivity and residency, then capability, then independence, then lifecycle and availability — all hard — then reliability, then cost and latency, then a deterministic tie-break. A later stage cannot restore what an earlier one removed.

## 4. Integration with the approved phases

**Nothing upstream changes.** Phase 9 adds a layer beneath the work and rewrites none of it.

| Phase | Boundary preserved |
|---|---|
| 3 — Roles | Professional conclusions stay Role-owned. **No Role Card is rewritten to name a model**, and no Role gains or loses anything here |
| 4 — Skills | Untouched |
| 5 — Workflows | A stage may state **capability requirements**; it does not route, and reaching a stage implies nothing about model adequacy |
| 6 — Handoffs and Reviews | A Profile may state a **model diversity** value. **Phase 9 adds no independence class and changes no review status**, and a handoff does not trigger a model change |
| 7 — Decision Rights | A Routing Decision is not a Decision Record. **Phase 9 cards no Right and grants none** |
| 8 — Knowledge | Model output is `AI_SUGGESTION` with `ORIGIN: AI_GENERATED`. **Routing changes no canonicality, no sensitivity classification and no scope**, and selecting a deployment never moves knowledge across a scope boundary |

Phase 9 resolves exactly one forward reference — the Model Registry promised in `architecture/registry-separation.md` §8 — and resolves it **by defining the registry**, without modifying that approved file.

## 5. Privacy, sensitivity and residency

Phase 8's sensitivity classes are **used, not redefined**. The mapping is a two-sided declaration:

- the **task** carries the sensitivity of the material it will handle, from Phase 8;
- the **deployment** carries an approved **maximum sensitivity**, a residency, and a retention and training posture.

A candidate is eligible only where the deployment's maximum is at or above the task's material sensitivity, its residency satisfies the requirement, and its posture satisfies `NO_TRAINING_ON_INPUT` where required.

Four rules:

1. **A sensitivity classification never names a provider.** Classification is a property of the material; provider suitability is a separate, evidenced policy determination. Wiring them together would make every reclassification a procurement decision.
2. **Provider suitability is explicit policy and evidence** — never inferred from reputation, scale, or the absence of a known incident.
3. **Scope separation survives routing.** Sending material to a deployment does not move it between scopes, and **PERSONAL / organisational separation is untouched** (`knowledge/scope-isolation-and-transfer.md` §7).
4. **Routing changes no canonicality and no visibility.** A canonical statement sent to a model is still canonical and no more visible; a model's output is not canonical and not more true for having been produced by an approved deployment.

No identity, permission or access-control mechanism is designed here.

## 6. Human control

A human may: **select** among eligible candidates; **require** a stronger model, a different family, or a different provider; **prohibit** a candidate; **accept a declared degraded fallback** where policy allows; and **block** execution entirely.

A human may **not**:

1. **make an ineligible model eligible** where law, regulation, contract, privacy or security forbids it — no role, seniority or urgency reaches that;
2. **waive mandatory review independence** — that requires a valid upstream Phase 7 Decision Right, and a routing choice is not one;
3. **make output true or canonical** — selection is about the instrument, and Phase 8 governs the claim;
4. **rewrite routing history** — a change is a new Routing Decision linked to the prior one.

**Ordinary operator choice and a governed exception are different acts.** Choosing among eligible candidates, or requiring something stronger, is ordinary and recorded. Proceeding where a hard constraint is unmet is **not an override at all** — it is either a governed exception under a Phase 7 Right, or it does not happen.

## 7. Reproducibility

Three different things, and Phase 9 owns exactly one:

| | Meaning | Phase 9? |
|---|---|---|
| **Routing reproducibility** | Given the same requirements, registry state and policy version, the same candidate is selected | **Yes** — the deterministic tie-break exists for this |
| **Model-output reproducibility** | The same input yields the same output | **No.** Not claimed, not achievable, not architecture's to promise |
| **Provider availability reproducibility** | The same deployment is reachable as before | **No.** A runtime observation |

A Routing Decision preserves the exact Model Profile version, Provider and Deployment Profile versions, Routing Policy version, the constraints considered, the candidate set where practical, and the selection reason — so the **selection** can be re-derived and questioned even after the model behind it has changed or gone.

## 8. Non-runtime statement

This document and every artifact in `models/` is declarative architecture. Nothing here implements or specifies a provider SDK, API call, credential, secret, endpoint address, billing integration, latency probe, health check, failover service, evaluation service, prompt execution engine, agent orchestration, queue, database schema, storage, user interface, dashboard, telemetry pipeline or deployment. A later runtime **validates against** these semantics and does not mutate them.

## 9. Status

All Phase 9 artifacts are `PROPOSED`. Nothing is APPROVED or CANONICAL, no Decision Right is created, no Role gains anything, no provider or model product is endorsed, and inclusion here confers authority on no one and nothing.
