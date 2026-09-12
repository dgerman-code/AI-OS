# Claude Code Prompt — Phase 9 Model Registry / Router Foundation

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-9-model-registry-router`
Start baseline: Phase 8 human-approval record commit `00fb92e1b2dd1209ee2f69550c5962158b881e3e`
Approved Phase 8 architecture baseline: `516c91eb98ce89751b97d21c74553afaf7bed21b`

Build **Phase 9 — Model Registry / Router architecture foundation**.

Architecture and registry only.

Do NOT implement:
- runtime routing code;
- provider SDKs;
- API calls;
- secrets or credentials;
- billing integrations;
- live latency probes;
- model execution;
- prompt execution engines;
- agent orchestration;
- queues;
- databases;
- Supabase schema;
- UI;
- dashboards;
- telemetry pipelines;
- evaluation service;
- automatic failover service;
- production deployment.

Do NOT modify approved Phase 3–8 semantics except where Phase 9 resolves an explicit model-related forward reference.

Do NOT create a PR.

All Phase 9 artifacts remain `PROPOSED`.

---

# 1. Core architecture identity

The foundation must preserve this separation:

`ROLE != SKILL != WORKFLOW != HANDOFF != REVIEW PROFILE != DECISION RIGHT != KNOWLEDGE != MODEL PROFILE != MODEL CAPABILITY != ROUTING POLICY != ROUTING DECISION != PROVIDER != ENDPOINT != RUNTIME`

Also preserve:

`MODEL != ROLE`

`MODEL != AGENT INSTANCE`

`MODEL != AUTHORITY`

`MODEL != REVIEWER IDENTITY`

`MODEL != KNOWLEDGE SOURCE BY DEFAULT`

`MODEL != CANONICAL KNOWLEDGE`

`MODEL != PROVIDER`

`MODEL != ENDPOINT`

`ROUTER != ORCHESTRATOR`

`ROUTING DECISION != DECISION RIGHT`

A model is a replaceable execution capability. A Role remains a reusable professional profile. A Router selects a model/runtime candidate for bounded work; it does not decide organisational outcomes, review findings, canonical promotion, or authority.

---

# 2. Phase 9 purpose

Phase 9 must define how AI-OS can describe and choose among models/providers without binding the architecture to OpenAI, Anthropic, Google, local models, or any specific vendor.

The architecture should make it possible later to answer:

- Which model is eligible for this task?
- Which model is preferred?
- Which model is prohibited?
- Which model family should be used for independent review?
- When should a task be escalated to a stronger model?
- When can a cheaper/faster model be used safely?
- How do privacy, residency, provider, modality, context-window, tool-use, structured-output, reasoning, coding, vision, document, latency, cost and availability constraints affect eligibility?
- How do we preserve deterministic governance when model capabilities and provider names change over time?
- How can the system switch providers without rewriting Role, Skill, Workflow or Decision architecture?

Phase 9 does **not** execute models. It defines the semantic control layer required for future runtime routing.

---

# 3. Model Registry object model

Define at minimum the following semantic objects.

## 3.1 Model Profile

Stable architecture record describing a model family/version capability profile.

Minimum fields:
- stable model profile ID;
- display name;
- provider family reference;
- model family;
- version / release identifier;
- lifecycle status;
- capability claims;
- supported modalities;
- context characteristics;
- tool-use capability;
- structured-output capability;
- coding capability;
- reasoning capability;
- vision/document capability;
- multilingual capability;
- safety/compliance constraints;
- data handling / retention / training posture as declared by provider or deployment policy;
- deployment class (hosted provider / private hosted / local / sovereign / other conceptual class);
- region/residency applicability where relevant;
- cost class / latency class / availability class as semantic bands, not live prices;
- evaluation evidence refs;
- known limitations;
- prohibited contexts;
- review-by / freshness;
- supersedes / superseded-by;
- status.

Do not turn this into a vendor API schema.

## 3.2 Provider Profile

Separate provider/company/deployment operator from model identity.

Minimum semantics:
- stable provider ID;
- provider type/class;
- contractual/data-handling posture references;
- supported deployment/residency classes;
- availability/commercial constraints;
- provider-level prohibited contexts;
- provider lifecycle status.

One model family may exist through multiple providers/deployments; one provider may expose multiple models.

## 3.3 Endpoint / Deployment Profile

Conceptual deployment target distinct from model and provider.

Examples:
- public hosted endpoint;
- enterprise tenant endpoint;
- private cloud endpoint;
- local inference endpoint;
- sovereign-region deployment.

Define semantics only. No URLs, credentials or infrastructure config.

## 3.4 Model Capability

Reusable capability taxonomy rather than prose-only model descriptions.

Possible capability families to assess and refine:
- general reasoning;
- advanced reasoning;
- long-context analysis;
- coding;
- code review;
- mathematical reasoning;
- structured extraction;
- structured generation / schema adherence;
- document analysis;
- vision;
- multimodal reasoning;
- multilingual;
- summarisation;
- research synthesis;
- planning;
- tool calling;
- function/structured tool use;
- low-latency interaction;
- high-reliability constrained output;
- large-file handling;
- instruction fidelity;
- citation/evidence handling;
- safety-sensitive handling;
- privacy-sensitive deployment suitability.

Do not equate a capability claim with guaranteed performance.

---

# 4. Capability evidence and confidence

Model capability must not be declared true merely because a vendor says so or because one benchmark exists.

Define evidence classes such as:
- provider-declared capability;
- internal evaluation evidence;
- external benchmark evidence;
- observed production evidence (future/runtime);
- human expert assessment;
- known limitation / incident evidence.

Keep these distinct.

A Model Profile may contain **claims about capability** with evidence and confidence, but confidence does not create eligibility by itself.

No benchmark score should become authority.

Define freshness/review requirements because model behavior changes over time.

---

# 5. Model lifecycle

Define lifecycle states such as semantic equivalents of:
- CANDIDATE;
- EVALUATING;
- ELIGIBLE;
- PREFERRED;
- RESTRICTED;
- DEPRECATED;
- SUSPENDED;
- RETIRED.

Ensure lifecycle status is distinct from task-specific routing eligibility.

A model can be globally ELIGIBLE but prohibited for a specific task/context.

A PREFERRED model is not mandatory where policy constraints disqualify it.

A DEPRECATED model is not automatically deleted from historical routing records.

---

# 6. Routing Policy vs Routing Decision

Define:

## Routing Policy

A reusable, versioned rule set describing eligibility and preference.

## Routing Decision

A task-instance selection record stating which eligible candidate was chosen and why.

Critical separation:

`ROUTING POLICY != ROUTING DECISION != DECISION RIGHT`

A Routing Decision does not approve work, accept risk, satisfy review, promote canonical knowledge or create organisational authority.

Minimum Routing Decision evidence:
- task/work item reference;
- Role / activity context;
- criticality band;
- required capabilities;
- prohibited conditions;
- candidate set considered;
- eligibility result for each relevant candidate;
- selected Model Profile;
- selected Provider/Deployment Profile where applicable;
- policy version;
- reason for selection;
- fallback candidates if declared;
- diversity requirement if review/assurance task;
- cost/latency/privacy constraints applied;
- timestamp/effective context;
- any human override or exception reference;
- provenance/audit history.

No runtime implementation.

---

# 7. Routing constraint model

Define reusable routing constraint types.

At minimum cover:
- REQUIRED_CAPABILITY;
- REQUIRED_MODALITY;
- REQUIRED_CONTEXT_CLASS;
- REQUIRED_TOOL_USE;
- REQUIRED_STRUCTURED_OUTPUT;
- REQUIRED_DEPLOYMENT_CLASS;
- REQUIRED_RESIDENCY_OR_JURISDICTION;
- MAX_DATA_SENSITIVITY_ALLOWED;
- PROVIDER_ALLOWED / PROVIDER_PROHIBITED;
- MODEL_ALLOWED / MODEL_PROHIBITED;
- MODEL_FAMILY_ALLOWED / MODEL_FAMILY_PROHIBITED;
- MINIMUM_REASONING_CLASS;
- MINIMUM_RELIABILITY_CLASS;
- MAX_COST_CLASS;
- MAX_LATENCY_CLASS;
- MINIMUM_CONTEXT_CAPACITY_CLASS;
- MODEL_DIVERSITY_REQUIRED;
- PROVIDER_DIVERSITY_REQUIRED where justified;
- HUMAN_SELECTION_REQUIRED;
- NO_EXTERNAL_PROVIDER where justified;
- NO_TRAINING_ON_INPUT / retention posture requirement as a declared governance property, not a vendor assumption.

Classify each constraint as hard eligibility constraint or soft preference.

Hard constraints filter candidates.
Soft preferences rank eligible candidates.

A soft preference may never override a hard constraint.

---

# 8. Routing priority order

Define an explicit precedence model.

A candidate should normally be selected in this conceptual order:

1. task/scope legality and governance constraints;
2. sensitivity/privacy/residency constraints;
3. required capabilities/modalities/context/tooling;
4. independence/diversity requirements;
5. lifecycle/availability eligibility;
6. quality/reliability preference;
7. latency/cost preference;
8. deterministic tie-breaking rule.

Do not hard-code this exact list if a better precedence model is justified, but the architecture must prevent cost/latency preference from overriding legality, confidentiality, capability, review independence or criticality requirements.

---

# 9. Criticality-aware routing

Reuse approved criticality architecture; do not redefine it.

Define how higher criticality changes routing rigor.

Expected pattern:
- routine work may use a lower-cost eligible model if capability is sufficient;
- high-criticality work requires stronger capability evidence, freshness and reliability evidence;
- Enhanced Decision-Grade may require stronger reasoning class, independent review diversity, stricter provider/deployment constraints, or human selection depending on workflow/decision architecture;
- criticality raises routing rigor but does not grant the model authority or make its output true.

Do not equate “largest model” with “best model”.

Do not assume one model is globally strongest.

---

# 10. Role-to-model boundary

Define how Roles express requirements without becoming bound to a specific vendor model.

Preferred pattern:

`ROLE PROFILE + ASSIGNMENT ATTRIBUTES + SKILL SET + WORKFLOW CONTEXT + TASK CRITICALITY -> MODEL REQUIREMENTS -> ROUTING POLICY -> ELIGIBLE MODEL SET -> ROUTING DECISION`

A Role Card should normally express capability requirements or routing profile references, not model names.

Specific model pinning should be exceptional and governed.

No Role should say “this Role is Claude/GPT/Gemini”.

---

# 11. Workflow / Review integration

Define how Phase 5/6 workflows and reviews may reference routing requirements without becoming routers themselves.

Examples:
- a workflow stage may require minimum reasoning/coding/document capability;
- a Review Profile may require model-family diversity;
- independent assurance may prohibit using the same model family that produced the artifact where material;
- cross-domain review may require a different Role but not necessarily a different model unless policy says so;
- handoff does not automatically trigger model change;
- stage completion does not imply model adequacy.

The Router does not determine review satisfaction.

---

# 12. Independent review / model-family diversity

This is a critical Phase 9 concern.

Phase 6 already established review-independence classes at the reviewer/profile level. Phase 9 must define model-level diversity without confusing the two.

Required separation:

`REVIEWER / REVIEW PROFILE INDEPENDENCE != MODEL DIVERSITY`

A review can be organisationally independent but model-homogeneous, or model-diverse but organisationally non-independent.

Define policy options such as:
- SAME_MODEL_ALLOWED;
- DIFFERENT_MODEL_VERSION_REQUIRED;
- DIFFERENT_MODEL_FAMILY_REQUIRED;
- DIFFERENT_PROVIDER_REQUIRED;
- HUMAN_ONLY_REVIEW_REQUIRED;
- MODEL_DIVERSITY_NOT_APPLICABLE.

Do not make different-provider mandatory by default.

Enhanced Decision-Grade should strongly consider model-family diversity for material independent review, but exact requirement must be tied to review/risk context rather than blanket rule.

---

# 13. Fallback / degradation semantics

Define conceptual fallback behavior without implementing it.

Required distinctions:
- equivalent fallback;
- degraded fallback;
- prohibited fallback;
- human-selection fallback;
- defer/block rather than route.

A fallback is permitted only if it still satisfies hard constraints.

If fallback fails required capability, privacy, residency, independence or criticality constraints, the correct result is `NO_ELIGIBLE_MODEL` / `BLOCKED_FOR_ROUTING`, not “best available”.

No silent degradation.

A degraded fallback must be explicitly declared and may require human approval/acknowledgement depending on materiality.

---

# 14. Availability / outage semantics

Do not build monitoring.

Define how future runtime should represent conceptual status such as:
- AVAILABLE;
- DEGRADED;
- UNAVAILABLE;
- UNKNOWN_AVAILABILITY.

Availability is not capability.

A currently unavailable preferred model may lead to fallback, block, or human selection depending on policy.

`UNKNOWN_AVAILABILITY` must never be silently treated as AVAILABLE in high-criticality routing.

---

# 15. Cost and latency semantics

No live prices.

Use semantic classes/bands rather than provider-specific price tables.

Possible classes:
- COST_LOW / COST_MEDIUM / COST_HIGH / COST_PREMIUM;
- LATENCY_INTERACTIVE / LATENCY_STANDARD / LATENCY_SLOW / LATENCY_BATCH.

Refine if needed.

Rules:
- cost/latency are routing preferences unless explicitly hard-bounded by task policy;
- they never override privacy, legality, capability, review independence or Decision-Grade requirements;
- cheapest eligible model is not automatically preferred;
- most expensive model is not automatically best.

---

# 16. Provider independence / anti-lock-in

Phase 9 must make vendor replacement possible without rewriting higher architecture.

Define stable internal identifiers distinct from vendor display names.

Examples:
- `model.<stable_name>`
- `provider.<stable_name>`
- `deployment.<stable_name>`
- `routing_policy.<stable_name>`

Do not bake current product names into semantic IDs unless intentionally versioned as provider-specific profiles.

Define alias/mapping strategy so provider product renames do not rewrite historical records.

Historical Routing Decisions must preserve the exact profile/version actually used.

---

# 17. Versioning and reproducibility

A Routing Decision must be reproducible semantically even if the model later changes.

Preserve:
- exact Model Profile version;
- exact Provider/Deployment Profile version;
- exact Routing Policy version;
- exact requirements/constraints considered;
- candidate set where practical;
- selection reason.

Do not claim bit-for-bit output reproducibility.

Distinguish:
- routing reproducibility;
- model-output reproducibility;
- provider availability reproducibility.

Only the first belongs to Phase 9 architecture.

---

# 18. Evaluation boundary

Phase 9 may define evaluation evidence semantics but must not build the evaluation system.

Define evaluation dimensions such as:
- capability fitness;
- instruction fidelity;
- structured-output reliability;
- hallucination/unsupported-claim risk;
- coding correctness;
- review-detection quality;
- citation/evidence handling;
- latency class;
- cost class;
- safety/privacy suitability;
- language/domain performance.

Do not collapse all evaluation into one score.

A single composite score must never become automatic routing authority.

Prefer dimension-specific evidence and thresholds.

---

# 19. Model freshness / drift

A model profile can become stale as providers update behavior/version/terms.

Define:
- review-by;
- capability-evidence refresh trigger;
- provider-term change trigger;
- version change trigger;
- incident trigger;
- deprecation trigger.

A stale profile may be:
- usable for low-risk routing with warning;
- blocking for Decision-Grade routing;
- restricted pending re-evaluation.

Reuse Phase 8 freshness semantics rather than inventing conflicting states.

---

# 20. Sensitivity / privacy / residency integration

Use Phase 8 sensitivity classes.

Define mapping semantics between task/data sensitivity and provider/deployment eligibility.

Important:
- sensitivity classification does not itself name a provider;
- provider suitability must be explicit policy/evidence;
- PERSONAL / organisational scope separation remains intact;
- model selection must not cause knowledge to cross scope boundaries;
- routing to a provider does not change canonicality or visibility.

No IAM implementation.

---

# 21. Human control / overrides

Define human controls without granting unlimited bypass.

Possible human routing actions:
- select among eligible candidates;
- require a stronger model;
- require a different family/provider;
- prohibit a candidate;
- accept a declared degraded fallback where policy allows;
- block execution.

Human override must not:
- make an ineligible model eligible where law/privacy/security forbids it;
- waive mandatory review independence unless a valid Decision Right exists upstream;
- make output true/canonical;
- rewrite routing history.

Distinguish ordinary operator choice from a governed exception requiring a Decision Right.

---

# 22. Model incident / restriction semantics

Define conceptual handling for discovered issues:
- incorrect capability assumption;
- provider incident;
- data-handling concern;
- safety concern;
- severe quality regression;
- outage;
- policy violation.

Possible consequences:
- RESTRICTED;
- SUSPENDED;
- DEPRECATED;
- route prohibition for bounded context;
- re-evaluation required.

Do not build incident management runtime.

Historical Routing Decisions remain preserved.

---

# 23. Required Phase 9 artifacts

Create at minimum:

1. `architecture/model-registry-router.md`
2. `models/_standards/common-model-governance-constraints.md`
3. `models/_templates/model-profile-template.md`
4. `models/_templates/provider-profile-template.md`
5. `models/_templates/deployment-profile-template.md`
6. `models/_templates/routing-policy-template.md`
7. `models/_templates/routing-decision-template.md`
8. `models/model-capability-taxonomy.md`
9. `models/model-lifecycle-and-versioning.md`
10. `models/routing-constraint-model.md`
11. `models/routing-precedence-and-fallback.md`
12. `models/review-diversity-and-criticality.md`
13. `models/evaluation-evidence-model.md`
14. `models/master-model-routing-universe.md`
15. `reviews/phase-9-foundation-self-check.md`
16. a deterministic Phase 9 validation harness under `validation/` following the quality bar established by Phase 8.

Small additional files are permitted only if necessary.

Do not mass-generate provider/model cards.

---

# 24. Controlled exemplars

Create a small controlled exemplar set, all `PROPOSED`, with architecture-safe synthetic/internal IDs rather than claiming current vendor facts unless clearly marked as illustrative.

At minimum 8 exemplars:

1. routine text drafting task selecting a low-cost eligible model;
2. high-criticality legal/financial analysis requiring stronger reasoning profile;
3. independent assurance requiring different model family from producer;
4. privacy-sensitive task restricted to approved deployment class;
5. vision/document task where text-only candidate is ineligible;
6. provider outage causing equivalent fallback;
7. no eligible model causing BLOCK rather than silent degradation;
8. deprecated model retained in historical Routing Decision but excluded from new routing.

Optional ninth exemplar:
9. degraded fallback requiring explicit human acknowledgement / governed exception.

No real provider claims are required for exemplars.

---

# 25. Validation harness

Create deterministic architecture validation comparable in rigor to Phase 8.

Must check at least:
- identity separations;
- MODEL != ROLE;
- ROUTER != ORCHESTRATOR;
- ROUTING DECISION != DECISION RIGHT;
- provider/model/deployment separation;
- capability evidence != capability truth;
- hard constraint cannot be overridden by soft preference;
- cost/latency cannot override privacy/capability/criticality;
- lifecycle != task eligibility;
- no silent fallback degradation;
- no eligible model => BLOCK/NO_ELIGIBLE_MODEL;
- review independence != model diversity;
- model-family diversity rules do not rewrite Phase 6 reviewer independence;
- human override cannot bypass mandatory illegality/privacy constraints;
- model pinning is exceptional;
- Role Cards are not rewritten to vendor names;
- Routing Decision contains policy/profile version references;
- history preserved after deprecation;
- no runtime/provider SDK/API implementation;
- all Phase 9 artifacts remain PROPOSED;
- Phase 3–8 approved semantics/files unchanged;
- no PR created for Phase 9 branch.

Do not use vacuous checks.
Do not claim local validator can prove remote PR state unless actually checked externally.

Report exact deterministic total; do not target a cosmetic count.

---

# 26. Architecture questions to resolve or explicitly defer

Adjudicate at least these questions:

1. Is a Model Profile one vendor model/version, one family, or an internal capability abstraction?
2. Should Provider and Deployment be first-class registry objects?
3. How do model family and exact version differ for review diversity?
4. When is same-model review allowed?
5. When is different-model-family review mandatory?
6. Is different-provider review ever mandatory?
7. How are capability claims evidenced and refreshed?
8. How are cost/latency represented without live runtime data?
9. Can a human select a model directly, and under what constraints?
10. What is the difference between fallback, degraded fallback and exception?
11. When should routing block rather than choose “best available”?
12. How should deprecated/retired models appear in historical records?
13. How are privacy/residency constraints attached without IAM/runtime implementation?
14. Can one model be preferred for a Role but prohibited for a particular Workflow stage?
15. Does Phase 9 own evaluation methodology or only evaluation evidence semantics?
16. Which concerns belong to Phase 11 Orchestrator rather than Router?
17. What belongs to Phase 10 storage/infrastructure rather than Phase 9 architecture?

For each choose exactly one:
- RESOLVED IN FOUNDATION
- MUST RESOLVE BEFORE HUMAN APPROVAL
- SAFE TO DEFER WITH EXPLICIT RULE
- PHASE 10+
- PHASE 11+
- RUNTIME CONCERN

No unresolved authority/privacy/independence ambiguity may be silently deferred.

---

# 27. Regression boundary

Prove from git diff against Phase 8 approval-record baseline `00fb92e1b2dd1209ee2f69550c5962158b881e3e` that:
- approved Phase 3 Role semantics/files changed = 0;
- approved Phase 4 Skill semantics/files changed = 0;
- approved Phase 5 Workflow semantics/files changed = 0;
- approved Phase 6 Handoff/Review semantics/files changed = 0;
- approved Phase 7 Decision semantics/files changed = 0;
- approved Phase 8 Memory/Canonical semantics/files changed = 0;
- Phase 9 only adds model/routing architecture, exemplars, validation and review evidence.

No reapproval of prior phases is implied.

---

# 28. Producer self-check threshold

The foundation is producer-ready only if:
- no Role/Model collapse;
- no Router/Orchestrator collapse;
- no Routing Decision/Decision Right collapse;
- no model/provider/deployment collapse;
- no capability-confidence-as-truth collapse;
- no cost preference overriding hard governance;
- no silent degraded fallback;
- no review-independence/model-diversity collapse;
- no human override bypassing mandatory constraints;
- no provider lock-in in higher architecture;
- no Phase 3–8 regression;
- no runtime implementation;
- all deterministic validation passes.

If any of these fail, report `NOT READY`.

---

# 29. Commit / push

If and only if the foundation passes its producer self-check, commit exactly:

`docs: add Phase 9 Model Registry and Router foundation`

Push to:

`origin architecture/phase-9-model-registry-router`

Do not create a PR.

---

# Required final output

Return exactly:

### A. FOUNDATION SUMMARY
What Phase 9 defines and what it deliberately does not implement.

### B. IDENTITY MODEL
Final separation of Role / Model / Provider / Deployment / Router / Orchestrator / Routing Decision / Decision Right.

### C. MODEL REGISTRY
Model Profile, Provider Profile, Deployment Profile, lifecycle and versioning.

### D. CAPABILITY / EVIDENCE MODEL
Capability taxonomy, evidence classes, freshness, limitations.

### E. ROUTING POLICY MODEL
Hard constraints, soft preferences, precedence and eligibility.

### F. ROUTING DECISION MODEL
Required evidence and auditability of a task-instance selection.

### G. CRITICALITY / REVIEW DIVERSITY
How criticality and model-family diversity integrate with Phase 6 without replacing reviewer independence.

### H. FALLBACK / AVAILABILITY
Equivalent fallback, degraded fallback, block/no-eligible-model, outage semantics.

### I. HUMAN CONTROL
Human selection, override and exception boundaries.

### J. PRIVACY / SENSITIVITY / RESIDENCY
Phase 8 sensitivity integration and provider/deployment eligibility boundaries.

### K. EXEMPLARS
Each controlled exemplar and what it proves.

### L. OPEN QUESTIONS
All 17 dispositions.

### M. VALIDATION
Harness files, exact command, exact deterministic PASS/FAIL total, regression checks, local-vs-external boundary.

### N. REGRESSION
Phase 3–8 changes, Phase 9 status, runtime status, PR status.

### O. FILES CHANGED
Exact files and purpose.

### P. COMMIT / PUSH
Commit SHA, exact message, push result, remote HEAD, clean-tree status.

### Q. NEXT STEP
Choose exactly one:
- READY FOR INDEPENDENT PHASE 9 FOUNDATION AUDIT
- NOT READY

Do not claim Phase 9 approval.