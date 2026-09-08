# Claude Code Prompt — Phase 6 Handoff & Review Foundation

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-6-handoff-review`
Starting baseline: Phase 5 human-approval commit `97b02e897c86cfa059a453b8e26c166b6dd134d0`

## Objective

Build the Phase 6 architecture foundation for **Handoff & Review**.

Phase 6 must define how Role-owned work is handed from one Role to another and how independent review requirements are represented, scoped, satisfied, failed, escalated, and routed back to rework — without creating human Decision Rights, runtime orchestration, model identity, or hidden approval semantics.

This is architecture/registry work only.

Do not modify approved Phase 3 Role Cards.
Do not modify approved Phase 4 Skill Registry architecture/mappings.
Do not redesign approved Phase 5 Workflow Registry semantics except for narrow downstream references needed to integrate Phase 6.
Do not implement database schema, APIs, UI, runtime scheduling, queues, agent execution, model routing, or orchestration.
Do not create a PR.
Do not mark Phase 6 APPROVED or CANONICAL.

All Phase 6 artifacts created in this pass must be `PROPOSED`.

---

# 1. Core separation

Preserve this architecture boundary:

`ROLE != SKILL != WORKFLOW != HANDOFF != REVIEW PROFILE != DECISION RIGHT != MODEL != RUNTIME`

Definitions:

- **Role** owns methodology, professional scope, conclusions and artifact interfaces.
- **Skill** is reusable capability, bounded by Phase 4 mapping.
- **Workflow** coordinates stages, participation, state expectations and gate references.
- **Handoff** is the governed transfer of a Role-owned work product, evidence package, dependency or responsibility-for-next-action between Roles/stages without transferring professional ownership.
- **Review Profile** is a reusable independent review definition: what is reviewed, for what purpose, under what independence constraints, with what review outputs and severity/materiality semantics.
- **Decision Right** is external human authority; Phase 6 may reference it but must not define who holds it or how it is exercised.
- **Model/runtime** remain implementation concerns.

A Handoff must never transfer artifact ownership unless the upstream Role Card already defines a legitimate ownership transition outside the Handoff architecture.

A Review Profile must never make the human decision it informs.

---

# 2. Phase 6 scope

Phase 6 must define two related but distinct registries/models:

1. **Handoff Model**
2. **Review Profile Registry**

They may interact, but do not merge them into one mega-object.

## 2.1 Handoff Model must cover

- handoff identity and purpose;
- sending Role and receiving Role references;
- artifact/evidence/dependency being handed over;
- required knowledge state(s) and provenance at handoff;
- unresolved assumptions, conflicts, unknowns and open items carried with the handoff;
- required context package and traceability minimum;
- acceptance/receipt semantics without implying professional approval;
- rejection/return-for-rework semantics;
- chained handoffs;
- handoff completeness vs artifact correctness distinction;
- human-gate/review references that block the handoff where applicable;
- criticality-sensitive handoff depth;
- version/status/change control;
- non-runtime semantics.

## 2.2 Review Profile Registry must cover

- review identity;
- review purpose;
- review subject/artifact scope;
- review independence requirements;
- reviewer eligibility constraints;
- prohibited reviewer conditions;
- required evidence package;
- review method at architecture level;
- finding classes;
- finding severity/materiality model;
- review result/status semantics;
- review satisfaction criteria;
- review expiry/staleness triggers where relevant;
- re-review triggers;
- rework routing references back to Workflow stages or handoffs;
- criticality scaling;
- Decision Right references where unresolved findings require human decision;
- version/status/change control;
- non-runtime semantics.

---

# 3. Handoff primitives and semantics

Define a small declarative vocabulary. Do not create a runtime DSL.

At minimum include:

- `HANDOFF_TRIGGER`
- `SENDER_ROLE`
- `RECEIVER_ROLE`
- `HANDOFF_SUBJECT`
- `HANDOFF_PACKAGE`
- `STATE_REQUIREMENT`
- `OPEN_ITEM_CARRY`
- `PROVENANCE_REQUIREMENT`
- `RECEIPT_ACKNOWLEDGEMENT`
- `RETURN_FOR_REWORK`
- `HANDOFF_BLOCK`
- `REVIEW_REFERENCE`
- `DECISION_REFERENCE`

You may refine names if there is a strong architecture reason, but keep the primitive set compact and human-readable.

A Handoff must answer at least:

1. What exactly is being handed over?
2. Who sends it?
3. Who receives it?
4. What does the receiver need in order to proceed?
5. What provenance/evidence must accompany it?
6. Which assumptions/open items/conflicts remain unresolved?
7. What state must the subject be in?
8. What does acknowledgement mean?
9. What causes return for rework?
10. Which review or Decision Right may block progression?

## Receipt semantics

Define clearly:

- `RECEIVED` means the package was accepted as complete enough to inspect/use for the next bounded activity.
- It does **not** mean the receiver agrees with the conclusion.
- It does **not** mean `REVIEWED`, `APPROVED` or `CANONICAL`.
- It does **not** transfer professional ownership.

If you use another term instead of `RECEIVED`, preserve this exact conceptual boundary.

---

# 4. Review Profile identity and boundaries

Review Profile IDs:

`review.<stable_snake_case_name>`

Stable ID must not contain:
- organisation;
- project/client;
- model/provider;
- individual reviewer;
- version number;
- runtime technology.

A Review Profile defines review architecture, not a reviewer instance.

A Review Profile must NOT:

1. grant a Role new professional authority;
2. create a Decision Right;
3. approve/canonicalize an artifact by itself unless a separately governed knowledge-state transition explicitly permits `REVIEWED` only;
4. define business/policy decisions;
5. bind a model/vendor as reviewer identity;
6. execute the review;
7. override the owning Role's professional scope;
8. allow the author/producer to satisfy an independent-review requirement through self-check or QC.

---

# 5. Reviewer independence model

This is the most important Phase 6 architecture question.

Define reusable reviewer eligibility rules that can be checked against Role/Workflow participation without inventing runtime assignment logic.

At minimum distinguish:

- **PRODUCER_REVIEW** — not independent; may be internal quality control only.
- **PEER_REVIEW** — separate reviewer with same/similar professional domain, not the producer of the reviewed artifact/conclusion.
- **CROSS_DOMAIN_REVIEW** — reviewer from a different Role/domain checking interfaces, consistency, assumptions or dependencies, not substituting for domain review.
- **INDEPENDENT_ASSURANCE_REVIEW** — heightened independence requirement for decision-grade/high-criticality work.

You may rename/refine these if needed, but the architecture must explicitly distinguish internal QC from independent review.

## Independence constraints

Define at least these prohibitions for an independent review requirement:

- the reviewer cannot be the author/producer of the reviewed artifact/conclusion;
- the reviewer cannot be the Workflow stage lead if that Role authored the subject under review and independence would be compromised;
- a reviewer cannot review a conclusion it owns as producer in the same assignment instance;
- a Review Profile cannot declare a participating Role independent merely by naming it so;
- model-family diversity may be recorded as a runtime/assignment preference later, but must not be used as a substitute for Role/assignment independence;
- where adequate independent reviewer eligibility cannot be satisfied, review is unsatisfied and the Workflow/handoff must block, rework or escalate.

Do not define human names, staffing assignments or model selection.

---

# 6. Review subject and scope

Review scope must be bounded.

A Review Profile must state:

- subject artifact(s) / conclusion(s);
- owning Role(s);
- review purpose;
- what the review checks;
- what it explicitly does **not** check;
- required inputs/evidence;
- required traceability;
- criticality applicability;
- any dependency on another review.

Avoid generic "review everything" profiles.

Do not let one review profile absorb technical, financial, legal, ESG, security and evidence integrity review into a single universal mega-review.

---

# 7. Finding taxonomy

Define a compact reusable finding model.

At minimum include finding status/class concepts equivalent to:

- `NO_FINDING`
- `OBSERVATION`
- `MINOR_FINDING`
- `MAJOR_FINDING`
- `CRITICAL_FINDING`

You may choose a different vocabulary if justified, but it must distinguish materiality/severity clearly enough to drive rework/block/escalation semantics.

Also distinguish **finding severity** from **workflow open-item materiality**:

- severity belongs to review assessment;
- open-item materiality answers whether progression may continue.

Define mapping rules carefully; do not assume every minor finding blocks, and do not assume every critical finding can be carried forward.

At minimum:

- unresolved `CRITICAL_FINDING` must block/rework/escalate and cannot be review-satisfied;
- unresolved `MAJOR_FINDING` normally blocks review satisfaction unless the Review Profile explicitly permits a bounded conditional disposition and a named external Decision Right governs any exceptional progression;
- observations/minor findings may remain open only where they are non-material to the next step/gate and review satisfaction criteria allow it;
- a Review Profile cannot itself waive a finding.

---

# 8. Review result / satisfaction semantics

Do not conflate "review performed" with "review satisfied".

Define at least these concepts (names may be refined):

- `NOT_STARTED`
- `IN_REVIEW`
- `REVIEW_PERFORMED_WITH_OPEN_FINDINGS`
- `SATISFIED`
- `NOT_SATISFIED`
- `REVIEW_BLOCKED`
- `SUPERSEDED` / `STALE`

The architecture must make clear:

- `SATISFIED` is a review requirement status, not artifact approval;
- `SATISFIED` may permit a Workflow Stage/Handoff requirement to be considered met;
- it does not make the artifact `APPROVED` or `CANONICAL`;
- a human Decision Right remains separate;
- if an artifact changes materially after review, the review may become stale and require re-review;
- review satisfaction must be attributable to the Review Profile criteria and an eligible independent reviewer instance later, not to Workflow progression.

---

# 9. Rework semantics

Phase 6 must connect review findings back to Workflow/Handoff architecture without becoming runtime orchestration.

Define declarative references such as:

- affected artifact;
- affected owning Role;
- affected Workflow Stage(s);
- required rework destination;
- required evidence to close finding;
- whether re-review is mandatory.

Review Profile does not schedule the rework.

A finding cannot be silently closed because the Workflow revisited a Stage.

Closure must preserve:

- original finding;
- finding severity;
- reviewer attribution/eligibility record later;
- response/remediation evidence;
- closure rationale;
- prior artifact version;
- new artifact version;
- re-review outcome where required.

---

# 10. Handoff vs review boundaries

Define explicitly:

- Handoff checks **package completeness and transfer readiness**.
- Review checks **substantive quality / compliance / integrity / assurance** according to the Review Profile.
- A receiver acknowledging a handoff is not performing independent review.
- A Handoff may require a `review.<id>` to already be `SATISFIED` before transfer.
- A Review may itself consume a handoff package.
- Handoff rejection is not a review finding unless a Review Profile says it is.

---

# 11. Criticality scaling

Inherit `architecture/project-criticality-policy.md`.

Criticality may increase:

- required review types;
- independence depth;
- evidence depth;
- required reviewer eligibility constraints;
- number of handoff checkpoints;
- mandatory re-review after material change;
- traceability granularity;
- finding closure evidence;
- escalation rigor.

Criticality must not:

- change Role identity;
- create a new Review Profile merely because the project is larger if the review purpose is the same;
- turn a reviewer into a Decision Right holder;
- make review satisfaction equivalent to approval.

---

# 12. Review universe

Create a bounded candidate Review Profile universe.

Target approximately **20–35 candidate Review Profiles** across 7–10 families.

Suggested families:

1. Evidence / Factual Integrity
2. Project / Investment
3. Finance / Economics
4. Legal / Compliance / Procurement
5. ESG / Risk / Integrity
6. Programme / Grant
7. Product / Software / Data / Security
8. Documentation / Publication / Disclosure
9. Cross-Workstream / Decision-Grade Assurance

Candidate profiles should correspond to real review purposes already referenced in Phase 5, e.g.:

- `review.factual_evidence`
- `review.evidence_integrity_provenance`
- `review.engineering_technical`
- `review.operational_feasibility`
- `review.cost_estimate`
- `review.financial_model`
- `review.bankability`
- `review.legal_compliance`
- `review.procurement_state_aid`
- `review.esg_safeguards`
- `review.risk_quantification`
- `review.insurance_adequacy`
- `review.project_integration_coherence`
- `review.project_readiness`
- `review.eu_programme_compliance`
- `review.learning_design_quality`
- `review.mel_methodology`
- `review.data_protection`
- `review.architecture`
- `review.data_architecture`
- `review.security`
- `review.code`
- `review.test_coverage`
- `review.design_quality`
- `review.accessibility`
- `review.product_requirements_quality`

Do not blindly card every reference. Build a candidate universe and identify overlaps/duplicates.

Flag any Phase 5 `review.<id>` that appears too granular, duplicate, or better represented as a method inside a broader Review Profile.

---

# 13. Required exemplar Review Profiles

Create **6 exemplar Review Profile Cards** chosen to stress-test distinct domains and independence models:

1. `review.evidence_integrity_provenance`
2. `review.financial_model`
3. `review.legal_compliance`
4. `review.project_integration_coherence`
5. `review.eu_programme_compliance`
6. `review.security`

Each exemplar must include:

- identity;
- purpose;
- review family;
- subject / owning Role(s);
- applicability / trigger;
- required evidence package;
- independence class;
- reviewer eligibility;
- reviewer prohibitions;
- review scope;
- out-of-scope;
- method at architecture level;
- finding taxonomy/application;
- satisfaction criteria;
- rework/closure requirements;
- re-review triggers;
- criticality scaling;
- Workflow/Handoff references;
- Decision Right boundary;
- versioning/change control;
- non-runtime statement.

Keep all six `PROPOSED`.

---

# 14. Required Handoff exemplars

Create **4 exemplar Handoff Cards**:

1. `handoff.project_definition_to_technical_feasibility`
2. `handoff.technical_commercial_cost_to_financial_model`
3. `handoff.application_content_to_compliance_review`
4. `handoff.software_implementation_to_security_and_test_review`

Use stable IDs:

`handoff.<stable_snake_case_name>`

Each Handoff Card must include:

- identity;
- purpose;
- sender Role(s);
- receiver Role(s);
- subject artifacts;
- required package contents;
- required knowledge states;
- provenance/traceability requirements;
- carried open items/assumptions/conflicts;
- receipt semantics;
- return-for-rework conditions;
- required review/Decision references;
- criticality scaling;
- versioning/change control;
- non-runtime statement.

Do not allow a Handoff to create new Role ownership.

---

# 15. Required deliverables

Create all of the following:

1. `architecture/handoff-review-registry-design.md`
2. `reviews/_standards/common-review-constraints.md`
3. `reviews/_templates/review-profile-card-template.md`
4. `reviews/master-review-profile-universe.md`
5. `handoffs/_standards/common-handoff-constraints.md`
6. `handoffs/_templates/handoff-card-template.md`
7. `handoffs/exemplars/project-definition-to-technical-feasibility.md`
8. `handoffs/exemplars/technical-commercial-cost-to-financial-model.md`
9. `handoffs/exemplars/application-content-to-compliance-review.md`
10. `handoffs/exemplars/software-implementation-to-security-and-test-review.md`
11. `reviews/exemplars/evidence-integrity-provenance.md`
12. `reviews/exemplars/financial-model.md`
13. `reviews/exemplars/legal-compliance.md`
14. `reviews/exemplars/project-integration-coherence.md`
15. `reviews/exemplars/eu-programme-compliance.md`
16. `reviews/exemplars/security.md`
17. `reviews/phase-6-foundation-self-check.md`

Do not create a database schema or implementation files.

---

# 16. Common Review Constraints — minimum required rules

`reviews/_standards/common-review-constraints.md` must include at least:

1. Review grants no professional authority beyond reviewer Role Card.
2. Review Profile cannot create Decision Rights.
3. Review Profile cannot approve/canonicalize artifacts.
4. Producer QC cannot satisfy independent review.
5. Reviewer eligibility must be independently checkable against producer/assignment participation.
6. Reviewer independence cannot be declared merely by Workflow prose.
7. Reviewer cannot own/produce the reviewed conclusion in the same assignment instance where independent review is required.
8. Review scope must be bounded; no universal mega-review.
9. Review performed != review satisfied.
10. Review satisfied != human approval.
11. Finding severity != workflow open-item materiality.
12. Critical/major unresolved findings block satisfaction according to the Profile rules.
13. Review cannot waive its own findings.
14. Material artifact change can invalidate/stale prior review.
15. Rework preserves original finding and provenance.
16. Review-triggered rework does not silently close findings.
17. Review version changes cannot silently alter independence, severity, or satisfaction semantics.
18. Runtime must validate against registry, not mutate it.

---

# 17. Common Handoff Constraints — minimum required rules

`handoffs/_standards/common-handoff-constraints.md` must include at least:

1. Handoff does not transfer professional ownership.
2. Receipt acknowledgement != agreement with conclusion.
3. Receipt acknowledgement != review satisfaction.
4. Receipt acknowledgement != approval/canonicalization.
5. Sender cannot omit material assumptions/conflicts/unknowns.
6. Receiver cannot silently reinterpret missing inputs as assumptions.
7. Handoff package must preserve provenance and version identity.
8. Materially incomplete package blocks or returns for rework.
9. Required review/gate references cannot be bypassed by handoff.
10. Handoff may narrow but cannot widen Role/Skill applicability.
11. Rejected handoff preserves history and reason.
12. Re-handoff after rework must identify superseded/prior package.
13. Criticality increases package/evidence depth but not Role identity.
14. Runtime later executes handoff but cannot redefine semantics.

---

# 18. Self-checks

`reviews/phase-6-foundation-self-check.md` must perform at least **30 checks**.

At minimum verify:

1. Phase 3 Role Cards unchanged.
2. Approved Phase 4 architecture/mappings unchanged.
3. Approved Phase 5 Workflow architecture unchanged except explicit downstream references if unavoidable.
4. All Phase 6 artifacts `PROPOSED`.
5. Core identity separation preserved.
6. Handoff never transfers professional ownership.
7. Receipt never implies review/approval/canonical.
8. Review Profile never creates a Decision Right.
9. Review Profile never self-approves/canonicalizes.
10. Producer QC cannot satisfy independent review.
11. Independent reviewer cannot be producer of reviewed subject in same assignment.
12. Reviewer independence cannot be manufactured by naming a Role.
13. Review satisfaction semantics explicit.
14. Review performed != satisfied.
15. Satisfied != approval.
16. Finding severity/materiality semantics explicit.
17. Critical finding blocks satisfaction.
18. Major finding handling explicit.
19. Review cannot waive finding.
20. Material artifact change creates re-review/staleness behavior.
21. Rework preserves finding/provenance/version history.
22. Handoff package carries assumptions/conflicts/unknowns.
23. Handoff blocks/returns on material incompleteness.
24. All 6 exemplar reviews have bounded scope/out-of-scope.
25. All 6 exemplar reviews have reviewer eligibility/prohibitions.
26. All 4 handoff exemplars have sender/receiver/subject/package/receipt/rework semantics.
27. Master Review Universe is between 20 and 35 candidates.
28. Duplicate Review IDs = 0.
29. Review Universe flags overlaps/duplicates instead of mass-carding.
30. No runtime/database/API/orchestrator/model implementation.
31. No PR created.
32. No Phase 6 artifact marked APPROVED/CANONICAL.
33. Phase 5 forward `review.<id>` references are classified as existing candidate/profile or deliberate unresolved reference.
34. No Review Profile grants cross-domain professional conclusion authority.
35. No Handoff or Review object changes Role-to-Skill compatibility.
36. Criticality changes review/handoff depth, not identity.

If a check fails, fix the architecture/content, not the test, unless the test itself is demonstrably checking the wrong property. Record that honestly.

---

# 19. Open architecture questions to surface, not hide

The self-check must explicitly list unresolved questions, including at minimum:

- whether Review Profile composition/dependencies need a first-class declarative reference;
- whether one Review Profile may require another Review Profile as prerequisite;
- whether one reviewer instance may satisfy multiple compatible Review Profiles;
- whether reviewer eligibility should include organisational independence in addition to Role/assignment independence;
- whether review staleness should use one shared material-change rule or Profile-specific triggers;
- whether Handoff Cards should be first-class registry entries or embedded reusable patterns inside Workflows;
- how Review satisfaction is later recorded/observed by Workflow runtime;
- how Decision Rights in Phase 7 may permit exceptional progression without converting unsatisfied review into satisfied review.

Classify each as one of:
- MUST RESOLVE IN PHASE 6 FOUNDATION
- SAFE TO DEFER WITH EXPLICIT RULE
- PHASE 7 CONCERN
- RUNTIME-PHASE CONCERN

Do not prematurely define Phase 7 holder/delegation semantics.

---

# 20. Commit / push

If and only if the self-check is complete and all required deliverables exist, commit exactly:

`docs: add Phase 6 Handoff & Review foundation`

Push to:

`origin architecture/phase-6-handoff-review`

Do not create a PR.

---

# 21. Required final output

Return exactly:

### A. FOUNDATION CREATED
Files created and commit baseline.

### B. HANDOFF MODEL
Core identity, primitives, receipt/rework semantics.

### C. REVIEW PROFILE MODEL
Identity, independence, scope, finding and satisfaction semantics.

### D. REVIEW UNIVERSE
Families, candidate count, overlap/duplicate findings.

### E. EXEMPLAR REVIEWS
Six exemplar results and the key boundary each stress-tests.

### F. EXEMPLAR HANDOFFS
Four exemplar results and the key boundary each stress-tests.

### G. PHASE BOUNDARIES
What remains Phase 7 / runtime and what was not changed upstream.

### H. SELF-CHECK
Checks PASS / FAIL, with count.

### I. OPEN ARCHITECTURE QUESTIONS
List each with disposition.

### J. COMMIT / PUSH
Commit SHA, message, push result, remote HEAD, PR status.

### K. NEXT-STEP READINESS
Choose exactly one:
- READY FOR INDEPENDENT PHASE 6 FOUNDATION AUDIT
- NOT READY

Do not claim Phase 6 approval.