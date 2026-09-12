# Claude Code Prompt — Phase 9 Remediation After Independent Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-9-model-registry-router`
Audited foundation baseline: `212f42e4453033d63b761fe6c19c63538ce772d8`
Phase 8 approval-record baseline: `00fb92e1b2dd1209ee2f69550c5962158b881e3e`

The independent Phase 9 foundation audit returned **FAIL**.

This is a bounded architecture remediation pass.
Fix the audit findings without redesigning unrelated Phase 9 concepts and without changing approved Phase 3–8 semantics.

Do NOT implement runtime routing, SDKs, API calls, secrets, DB, UI, RAG, embeddings, agents, orchestration, queues, health monitoring, evaluation service, telemetry, billing or deployment.
Do NOT create real vendor/model/provider/deployment cards.
Do NOT create a PR.
Do NOT mark Phase 9 APPROVED or CANONICAL.
All Phase 9 architecture artifacts remain `PROPOSED`.

The audit identified 5 HIGH and 7 MEDIUM findings. Treat each as real unless repository evidence proves otherwise.

---

# 1. Resolve Model Profile identity granularity

Audit finding:
- `models/_templates/model-profile-template.md` and lifecycle docs do not sufficiently distinguish underlying model version, provider-hosted variant, provider release/alias, registry profile version and provider/deployment relationship.

Required architecture:

Define a strict identity stack with no overlap.

At minimum distinguish:

1. **Model Family** — lineage/family classification used for diversity and grouping.
2. **Underlying Model Release** — the model/release identity whose behavior/capabilities are being profiled.
3. **Model Profile** — AI-OS governed registry record describing one underlying model release/capability identity; internal stable ID + profile version.
4. **Provider Offering / Provider Mapping** — provider-specific exposure/alias/catalog mapping to that model release where applicable.
5. **Deployment Profile** — concrete conceptual deployment class/tenant/region/sensitivity/residency posture through which the model is used.
6. **Registry Profile Version** — version of the governed AI-OS record itself, distinct from underlying model version.

Do not necessarily create a sixth first-class registry object if provider offering can be represented cleanly as a bounded mapping inside Provider/Deployment. But runtime must never need to guess whether a provider-specific variant is the same underlying model, a different release, or merely an alias.

Required rules:
- Model Profile must not carry provider-specific governance properties that belong to Provider or Deployment;
- one Model Profile may map to multiple provider/deployment combinations where they genuinely expose the same underlying release;
- if provider-specific behavior is materially different and cannot be evidenced as the same release, it must be represented as a distinct Model Profile or explicit provider-specific variant with unambiguous identity;
- provider marketing alias never defines Model Profile identity;
- registry profile version != underlying model version;
- historical Routing Decision preserves both exact Model Profile version and provider/deployment mapping used;
- silent provider backend changes trigger review and may require a new mapping/profile version depending on materiality.

Remove or relocate duplicated `Data Handling Posture` fields from Model Profile if they are deployment/provider governance properties rather than intrinsic model characteristics. Establish precedence explicitly where the same concept appears at multiple layers.

Re-adjudicate open question #1 after this fix.

---

# 2. Define reproducible candidate-universe construction

Audit finding:
“Candidate set where practical” is not auditable and cannot detect accidental omission.

Required architecture:

Every Routing Decision must bind to a **Candidate Universe Definition** before filtering/ranking.

Define at minimum:
- registry snapshot/version or equivalent deterministic registry-state reference;
- inclusion rule / enumeration rule;
- relevant routing scope (e.g. active profiles + eligible deployment classes + provider allowlist context);
- explicit pre-filter exclusions that are outside the universe versus hard-constraint exclusions inside the universe;
- any candidate omitted from normal enumeration must have a recorded omission reason;
- runtime load failure must not silently shrink the universe;
- candidate availability/unavailability is a candidate property/result, not a reason to make the candidate disappear from the universe unless the policy explicitly defines such pre-enumeration behavior;
- a registered candidate accidentally not loaded must be detectable as `CANDIDATE_UNIVERSE_INCOMPLETE` / equivalent and routing must block or escalate according to policy;
- Routing Decision must record the universe definition version/reference plus the evaluated candidate set and exclusion reason.

The architecture may use bounded candidate-universe construction rather than enumerate the entire registry, but the bound must be reproducible and explainable.

Replace “where practical” with normative semantics.

This is a human-approval blocker.

---

# 3. Replace ordinal maximum-sensitivity model with multi-label handling compatibility

Audit finding:
Phase 8 sensitivity is multi-valued / orthogonal, but Phase 9 treats it as one scalar “maximum sensitivity” and compares “at or above”. This is invalid for categories such as `PERSONAL_DATA`, `PRIVILEGED`, `TRADE_SECRET`, etc.

Required architecture:

Do not impose a total order on Phase 8 sensitivity classes unless Phase 8 itself defines one.

Represent task/data requirements and deployment/provider suitability as a **set / policy compatibility model**.

At minimum distinguish:
- required sensitivity/handling labels on material/task;
- deployment-supported / approved sensitivity labels;
- required handling obligations per label;
- prohibited labels/contexts;
- compound/multi-label cases;
- unknown/unevaluated handling support.

Eligibility rule:
A deployment is eligible only if **every applicable sensitivity/handling requirement** is explicitly satisfied and no prohibited condition applies.

Examples:
- `PERSONAL_DATA + PRIVILEGED` requires both handling regimes simultaneously;
- `TRADE_SECRET` support does not imply `PERSONAL_DATA` support;
- no label outranks another merely by being “higher”;
- unknown support != supported.

Replace `MAX_DATA_SENSITIVITY_ALLOWED` if necessary with a better model such as:
- `SUPPORTED_SENSITIVITY_CLASSES`;
- `REQUIRED_HANDLING_CONTROLS`;
- `PROHIBITED_SENSITIVITY_CLASSES`;
- `REQUIRED_DATA_HANDLING_POSTURE`.

Update architecture, deployment template, constraint model, exemplars 1/4/6/7, universe and validation.

Preserve Phase 8 sensitivity semantics exactly; do not redefine them.

---

# 4. Complete residency / jurisdiction semantics

Audit finding:
Deployment Profile lacks explicit representation for exact jurisdiction, region class, allowed/prohibited sets and unknown residency.

Define deployment-level residency/jurisdiction semantics with clear fields such as equivalents of:
- exact jurisdiction(s);
- region/residency class;
- allowed jurisdiction set;
- prohibited jurisdiction set;
- sovereign/private/local requirement;
- cross-border processing allowed/forbidden/conditional;
- unknown residency state;
- evidence/source/review-by.

Rules:
- residency belongs primarily to Deployment Profile, not generic Model Profile;
- unknown residency never satisfies a hard residency requirement;
- allowed and prohibited sets must have precedence semantics;
- provider-level claims may constrain deployments but do not replace deployment-specific evidence;
- exact jurisdiction and broad region class are not interchangeable without an explicit mapping.

No IAM/runtime implementation.

---

# 5. Reconcile fallback, hard eligibility and governed exception

Audit finding:
Exemplar 9 calls a `BASELINE` candidate eligible despite a `STRONG` required capability, then uses a Phase 7 exception because the hard requirement is unmet.

This is contradictory.

Required semantics:

Separate three distinct cases:

### A. Ordinary eligible fallback
Candidate satisfies **all current hard constraints**.
May be equivalent or degraded only on dimensions that are soft/preferences or explicitly permitted non-hard degradation bands.

### B. Policy-adjusted fallback under a valid governed exception
Original hard constraint is not met.
Candidate is **not eligible under the original policy**.
A specific Phase 7 Decision Right, where that constraint class is exceptionable, creates a new bounded **exception-adjusted routing context/policy instance** or equivalent governed requirements state.
Only after that governed act is recorded may eligibility be re-evaluated against the adjusted requirement set.

The Routing Decision must preserve:
- original constraint;
- original ineligibility result;
- Decision Right / Decision Record reference;
- exact adjusted constraint/effect;
- re-evaluated eligibility;
- no rewriting of original routing history.

### C. Non-waivable constraint failure
No exception path exists.
Result remains `BLOCKED_FOR_ROUTING` / `NO_ELIGIBLE_MODEL`.

Do not call a candidate “eligible” before the governing exception changes the applicable requirement set.

Rework Exemplar 9 accordingly.

---

# 6. Classify hard constraints by exceptionability

Audit finding:
Architecture says ordinary humans cannot bypass law/privacy/security/contract constraints, but elsewhere speaks generically about Phase 7 hard-constraint exceptions.

Define an explicit exceptionability taxonomy.

At minimum categories equivalent to:

1. **ABSOLUTELY_NON_WAIVABLE** — no routing exception inside AI-OS. Examples may include illegality, hard contractual prohibition, explicit privacy/security prohibition, provider/deployment unsupported handling where policy says no legal exception exists.
2. **GOVERNED_EXCEPTION_POSSIBLE** — may be adjusted only by a named valid Phase 7 Decision Right and Decision Record with bounded effect.
3. **OPERATOR_CONFIGURABLE_WITHIN_POLICY** — not really an exception; normal choice/tuning within allowed policy envelope.

Do not blindly classify every current hard constraint into category 1 or 2 without reasoning.

For each hard constraint type in `routing-constraint-model.md`, assign an exceptionability class or a rule for deriving it from its source.

Important:
- law/regulation/privacy/security/contract constraints are not automatically exceptionable;
- a Phase 7 Right cannot create legal authority where none exists;
- exceptionability must be anchored to the source of the constraint and the specific Decision Right;
- unrecognized/unknown exceptionability defaults to non-waivable for routing purposes;
- human acknowledgement alone never changes hard eligibility.

Update standard, templates, fallback docs, universe and validation.

Re-adjudicate open question #10.

---

# 7. Bound negative evidence precedence

Audit finding:
`KNOWN_LIMITATION_OR_INCIDENT` always outranks positive evidence with insufficient bounds.

Required model:
Negative evidence may restrict/override a positive capability claim only where **applicable**.

Applicability must consider at minimum:
- exact model/release/profile version;
- provider/deployment context if relevant;
- capability/evaluation dimension;
- task/domain context;
- materiality/severity;
- evidence quality/reliability;
- freshness/effective period;
- remediation/resolution status.

Rules:
- stale evidence about a superseded version does not automatically dominate current evidence;
- a context-specific incident does not automatically invalidate unrelated contexts;
- low-quality anecdotal evidence does not permanently override stronger verified evidence without materiality assessment;
- severe current safety/data-handling incident may immediately restrict routing pending review;
- conflicting evidence should create a governed evidence/conflict state rather than be averaged blindly.

Do not introduce a composite score.

Update evaluation evidence model and validation.

Re-adjudicate open question #7.

---

# 8. Make lifecycle state exclusivity explicit

Audit finding:
It is unclear whether lifecycle values are exclusive and whether `PREFERRED` and `RESTRICTED` can coexist.

Resolve explicitly.

Preferred architecture:
- one primary lifecycle state at a time;
- task/context restrictions are separate restriction annotations/policies rather than a second lifecycle state;
- `PREFERRED` may be a routing preference designation rather than lifecycle if that reduces semantic collision.

You may choose another coherent design, but runtime must not invent whether two states coexist.

Define transition rules and effect on new routing/history.

Update universe/validation.

---

# 9. Separate act requirements from eligibility constraints

Audit finding:
`HUMAN_SELECTION_REQUIRED` is listed as a hard eligibility constraint but explicitly does not filter candidates.

Refactor the taxonomy into at least three semantic kinds:
- **ELIGIBILITY_CONSTRAINT** — filters candidates;
- **PREFERENCE** — ranks eligible candidates;
- **ROUTING_ACT_REQUIREMENT** — requires a human/other act before selection can finalize but does not change candidate capability eligibility.

`HUMAN_SELECTION_REQUIRED` belongs to the third category.

Other act requirements may include human acknowledgement of declared degradation or required governance review where relevant.

Do not let act requirements masquerade as hard filters.

Update counts and validation mechanically.

---

# 10. Reconcile global precedence with policy-owned preference ordering

Audit finding:
Global architecture fixes reliability before cost while Routing Policy claims ownership of ordered soft preferences.

Resolve the boundary.

Recommended pattern:
- **hard-stage precedence is globally fixed**: legality/governance -> privacy/residency -> capabilities -> diversity -> lifecycle/availability;
- **soft preference ordering is versioned Routing Policy**, with bounded permissible dimensions such as reliability, latency, cost, provider concentration, energy/other future factors;
- policy may rank reliability above cost or vice versa where risk/criticality permits;
- criticality may impose mandatory minimum reliability thresholds as hard constraints;
- no soft ordering may restore an ineligible candidate;
- deterministic tie-break remains after policy preference evaluation.

Do not recreate opaque composite scoring unless explicitly justified; ordered lexicographic preferences are preferable.

Update architecture, precedence doc, Routing Policy template, universe and validation.

---

# 11. Remove model-diversity / reviewer-independence leakage in Exemplar 9

Audit finding:
Exemplar 9 says dropping model-family diversity waives review independence.

Fix terminology and semantics.

Required:
- reviewer independence remains Phase 6 organisational/reviewer concept;
- model-family diversity is Phase 9 execution-diversity concept;
- waiving/reducing model diversity does **not** itself waive reviewer independence;
- if Review Profile separately requires both, they must be represented as two controls;
- a Phase 7 exception affecting one does not silently affect the other.

Search all Phase 9 artifacts for similar leakage and fix any occurrence.

---

# 12. Clarify privacy-sensitive suitability capability

Audit finding:
`capability.privacy_sensitive_suitability` overlaps provider/deployment contractual controls.

Decide whether this is genuinely a model capability.

Preferred direction:
- remove it from model capability taxonomy if it actually means governance suitability;
- represent privacy suitability through Provider/Deployment evidence and routing constraints;
- if there is an intrinsic model capability relevant to privacy-preserving processing, name it narrowly and distinguish it from contractual/data-handling eligibility.

No capability token should duplicate a provider/deployment governance decision.

Update taxonomy/counts/universe/validation.

---

# 13. Data-handling posture ownership / precedence

Audit found repeated data-handling posture across Model, Provider and Deployment.

Define authoritative ownership:

Suggested separation:
- **Model Profile:** intrinsic technical characteristics only, where evidenced (e.g. modality, context, tool use). No generic contractual retention/training promises.
- **Provider Profile:** provider-level contractual/default posture and policy constraints.
- **Deployment Profile:** effective deployment-specific posture, residency, tenant controls, retention/training mode, approved sensitivity/handling classes.

If deployment overrides provider default, it must be explicitly evidenced and permitted.

Routing uses the **effective deployment posture** after provider-level constraints are applied.

No duplicated conflicting sources of truth.

---

# 14. Strengthen validation harness

Current `141/141 PASS` missed multiple HIGH semantic defects. Credibility is MEDIUM.

Strengthen it to target the audit findings.

At minimum add semantic validation for:

1. Model Profile identity stack fields and separation of profile version vs underlying release vs provider/deployment mapping;
2. no provider-specific data-handling posture in Model Profile where prohibited by new ownership rule;
3. Candidate Universe Definition required in Routing Decision template;
4. registry snapshot/version or deterministic universe reference required;
5. omission reason / incomplete-universe behavior present;
6. no scalar `maximum sensitivity` / “at or above” ordinal Phase 8 sensitivity logic in normative Phase 9 docs;
7. multi-label sensitivity compatibility semantics;
8. residency exact/allowed/prohibited/unknown semantics;
9. fallback cannot call candidate eligible if original hard constraint failed;
10. exception-adjusted policy/context requires Decision Right reference and re-evaluation;
11. every hard constraint has exceptionability classification/derivation;
12. absolutely non-waivable constraints cannot be exceptioned by ordinary operator or generic Phase 7 language;
13. negative evidence applicability includes version/context/materiality/quality/freshness;
14. lifecycle exclusivity or chosen coexistence semantics explicit;
15. `HUMAN_SELECTION_REQUIRED` not in eligibility-filter constraint set;
16. soft preference order owned by Routing Policy rather than globally hard-coded beyond fixed governance stages;
17. no model-diversity/reviewer-independence conflation;
18. no privacy-governance concept duplicated as a model capability;
19. all nine exemplars conform to final semantics;
20. candidate universe / sensitivity / exception fixes cannot be bypassed by optional-field discovery gaps;
21. all Phase 9 artifacts remain PROPOSED;
22. Phase 3–8 semantic regression = 0;
23. no runtime/provider SDK/API implementation;
24. local validator makes no remote PR claim.

Remove/replace weak presence-only checks where they can pass contradictory semantics.

Do not preserve 141 cosmetically. Report actual deterministic count.

Run Phase 8 harness too and preserve `119/119 PASS` or explain any strictly tooling-only correction.

---

# 15. Update affected exemplars

At minimum rework:
- #1 routine drafting — remove invalid ordinal sensitivity logic;
- #4 privacy-restricted deployment — use multi-label handling compatibility;
- #6 provider outage — preserve multi-label/privacy compatibility;
- #7 no eligible model — multi-label `PRIVILEGED + PERSONAL_DATA` must require both;
- #9 degraded fallback — original candidate ineligible; governed exception produces adjusted requirement context before re-evaluation; model diversity != reviewer independence.

Re-audit all nine after modifications.

No exemplar may contain real vendor claims.

---

# 16. Re-adjudicate all 17 open questions

The independent audit marked #1, #7, #10, #13 as MUST RESOLVE BEFORE HUMAN APPROVAL.

After remediation, independently adjudicate all 17 again.

Special attention:
- #1 Model Profile identity granularity;
- #7 capability evidence applicability/freshness;
- #10 fallback vs degraded fallback vs governed exception;
- #13 privacy/residency attachment semantics.

Also reconsider questions related to human selection and Routing Policy preference ownership where the audit exposed ambiguity.

Use only:
- RESOLVED IN FOUNDATION
- MUST RESOLVE BEFORE HUMAN APPROVAL
- SAFE TO DEFER WITH EXPLICIT RULE
- PHASE 10+
- PHASE 11+
- RUNTIME CONCERN

Do not label a blocker resolved unless a concrete normative rule now exists.

---

# 17. Required remediation record

Create:
`reviews/phase-9-foundation-audit-remediation.md`

Include:
- every HIGH/MEDIUM finding;
- exact remediation;
- files changed;
- new/changed counts;
- validation evidence;
- open-question re-adjudication;
- explicit statement Phase 9 remains PROPOSED;
- external repository checks separately from offline validation;
- post-remediation architecture baseline identified as the commit carrying this remediation record.

---

# 18. Regression boundary

Prove against `00fb92e1b2dd1209ee2f69550c5962158b881e3e`:
- Phase 3 Roles semantic/file changes = 0;
- Phase 4 Skills = 0;
- Phase 5 Workflows = 0;
- Phase 6 Handoff/Review = 0;
- Phase 7 Decisions = 0;
- Phase 8 Knowledge/Canonical semantics = 0;
- any Phase 8 validation change, if any, is tooling-only and strictly justified;
- Phase 9 only changes its architecture/models/exemplars/validation/review evidence;
- no runtime implementation;
- no real provider/model/deployment profiles;
- no PR.

---

# 19. Commit / push

If and only if all remediation checks pass, commit exactly:

`docs: remediate Phase 9 foundation after independent audit`

Push to:

`origin architecture/phase-9-model-registry-router`

Do not create a PR.

---

# Required final output

Return exactly:

### A. REMEDIATION SUMMARY
All HIGH/MEDIUM findings and final status.

### B. MODEL IDENTITY / OBJECT MODEL
Final identity stack, provider/deployment ownership and data-handling precedence.

### C. CANDIDATE UNIVERSE
Exact reproducible universe construction, registry snapshot semantics, omission/incomplete-universe behavior.

### D. SENSITIVITY / PRIVACY / RESIDENCY
Final multi-label handling compatibility and residency/jurisdiction model.

### E. CONSTRAINT TAXONOMY / EXCEPTIONABILITY
Eligibility constraints vs preferences vs act requirements; non-waivable vs governed-exception semantics.

### F. FALLBACK / EXCEPTION MODEL
Ordinary fallback vs degraded fallback vs exception-adjusted re-evaluation; no semantic contradiction.

### G. EVIDENCE / LIFECYCLE
Negative evidence applicability bounds; lifecycle exclusivity/final design.

### H. PRECEDENCE / ROUTING POLICY
Fixed hard-stage precedence vs policy-owned soft preference ordering.

### I. REVIEW DIVERSITY
Model-family diversity boundary vs Phase 6 reviewer independence.

### J. EXEMPLARS
All nine PASS/FAIL after remediation.

### K. OPEN QUESTIONS
All 17 dispositions.

### L. VALIDATION
Exact deterministic command/count/result; Phase 8 harness result; semantic checks added; credibility self-assessment.

### M. REGRESSION
Phase 3–8 changes; Phase 9 status; runtime/profile/PR status.

### N. FILES CHANGED
Exact files and purpose.

### O. COMMIT / PUSH
Commit SHA, exact message, push result, remote HEAD, clean-tree status.

### P. NEXT STEP
Choose exactly one:
- READY FOR FINAL INDEPENDENT PHASE 9 RE-AUDIT
- NOT READY

Do not claim Phase 9 approval.