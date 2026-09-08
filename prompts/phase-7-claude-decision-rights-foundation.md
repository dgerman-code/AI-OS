# Claude Code Prompt — Phase 7 Decision Rights / Human Approval Matrix Foundation

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-7-decision-rights`
Starting baseline: Phase 6 human-approval commit `332750bf19e167d1ae0dd2f6350e9bf84731ddd4`

## Objective

Build the Phase 7 architecture foundation for **Decision Rights / Human Approval Matrix**.

Phase 7 defines the reusable governance model behind stable `decision.<id>` references already used by approved Phase 5 Workflow and approved Phase 6 Review/Handoff architecture.

This phase must answer:
- what a Decision Right is;
- what it is allowed to decide;
- who may hold it by **eligibility class**, not by named person;
- how delegation, revocation, emergency authority, evidence, gate satisfaction, exceptional progression, waiver/risk acceptance, rejection, cancellation and supersession are governed;
- what a human approval record must contain;
- how a Decision Right interacts with Workflow, Review, Handoff and knowledge states without absorbing any of them.

This is architecture/registry work only.

Do not modify approved Phase 3 Role Cards.
Do not modify approved Phase 4 Skill architecture/mappings.
Do not modify approved Phase 5 Workflow semantics.
Do not modify approved Phase 6 Handoff/Review semantics except for narrow downstream reference clarification if absolutely required.
Do not implement database schema, API, UI, notifications, workflow runtime, model routing, agents, signatures, IAM, authentication or authorization systems.
Do not bind real people, organisations, job titles, model providers or runtime identities.
Do not create a PR.
Do not mark Phase 7 APPROVED or CANONICAL.

All Phase 7 artifacts created in this pass must remain `PROPOSED`.

---

# 1. Core identity separation

Preserve:

`ROLE != SKILL != WORKFLOW != HANDOFF != REVIEW PROFILE != DECISION RIGHT != DECISION RECORD != MODEL != RUNTIME`

Definitions:

- **Role** owns professional methodology, scope, conclusions and artifact interfaces.
- **Workflow** coordinates progression and references gates.
- **Handoff** governs transfer without ownership transfer.
- **Review Profile** governs review requirements and satisfaction, without approval authority.
- **Decision Right** is a reusable definition of a bounded human authority to make one class of decision.
- **Decision Record** is evidence that one concrete human decision was made under a Decision Right in a specific context.
- **Model/runtime** remain implementation concerns.

A Decision Right is NOT:
- a Role;
- a reviewer;
- a Workflow stage;
- a business rule engine;
- a model;
- a generic “approver” label;
- a permission to decide anything outside its declared scope.

A Decision Record is not the Decision Right itself.

---

# 2. Decision Right identity

Stable IDs:

`decision.<stable_snake_case_name>`

IDs must not include:
- human name;
- organisation/client/project;
- provider/model;
- implementation technology;
- version number;
- transient job title.

Each Decision Right must declare a bounded **decision subject** and a bounded **decision effect**.

Examples already referenced upstream include concepts such as:
- exceptional progression;
- production release;
- emergency production change;
- grant submission;
- external publication;
- risk acceptance;
- project readiness progression;
- contract/commercial commitment;
- canonical promotion;
- cancellation/termination.

Do not assume these examples are all valid separate Decision Rights. Build the universe from actual upstream `decision.<id>` references plus architecture need, then normalize duplicates/overlaps.

---

# 3. Decision classes

Define a compact decision-class taxonomy.

At minimum distinguish:

1. `PROGRESSION_DECISION`
   - permits or refuses movement to a next governed state/stage despite conditions that require human authority.

2. `APPROVAL_DECISION`
   - approves a bounded artifact/action for a declared purpose.

3. `COMMITMENT_DECISION`
   - creates an external, financial, contractual, regulatory, submission, publication or release commitment.

4. `RISK_ACCEPTANCE_DECISION`
   - accepts a declared residual risk / unresolved issue within bounded authority.

5. `EXCEPTION_DECISION`
   - permits a governed exception without rewriting the underlying rule or falsely satisfying an unsatisfied review.

6. `EMERGENCY_DECISION`
   - permits a time-critical exceptional act under explicit emergency conditions and mandatory retrospective controls.

7. `REJECTION_DECISION`
   - refuses approval/progression/commitment and may route to rework/termination.

8. `CANCELLATION_OR_TERMINATION_DECISION`
   - cancels a Workflow/project/action or terminates a pending governed path.

You may refine names, but preserve semantic separation.

Do not use one universal `decision.approve_anything` pattern.

---

# 4. Decision effect model

Every Decision Right must explicitly state what a positive, negative or exceptional decision does.

At minimum support outcome semantics equivalent to:

- `APPROVE`
- `REJECT`
- `APPROVE_WITH_CONDITIONS`
- `DEFER`
- `ESCALATE`
- `CANCEL`

Not every Decision Right must allow every outcome.

For each permitted outcome, define:
- effect on Workflow progression;
- effect on Handoff eligibility;
- effect on external action/commitment;
- effect on Review status;
- effect on knowledge state;
- whether conditions/open items remain active;
- whether expiry or re-decision is required.

Mandatory boundaries:

- A Decision Right may permit progression while a Review remains `NOT_SATISFIED`, if that Decision Right explicitly governs exceptional progression; it **must not** relabel the review `SATISFIED`.
- A Decision Right may accept risk; it does not erase the risk/finding.
- A Decision Right may approve an artifact for a bounded use; it does not automatically make the artifact `CANONICAL` unless a separate Decision Right explicitly governs canonical promotion.
- A Decision Right cannot create professional conclusions outside upstream Role ownership.
- A Decision Right does not rewrite source facts, assumptions, findings, `UNKNOWN`, or `CONFLICT_DETECTED` states.

---

# 5. Holder eligibility model

Phase 7 must define **holder eligibility**, not named holders.

Create a bounded taxonomy such as:

- `DESIGNATED_HUMAN_AUTHORITY`
- `GOVERNANCE_BODY_AUTHORITY`
- `EXECUTIVE_AUTHORITY`
- `FUNCTIONAL_AUTHORITY`
- `PROJECT_OR_PROGRAMME_SPONSOR_AUTHORITY`
- `LEGAL_ENTITY_SIGNATORY_AUTHORITY`

You may refine or reduce these classes.

Eligibility rules must be based on the authority needed, not Role competence alone.

Mandatory rules:

1. Role competence does not automatically create Decision Right authority.
2. Being Workflow LEAD_ROLE does not create approval authority.
3. Being reviewer does not create Decision Right authority.
4. Being artifact owner does not automatically create external commitment authority.
5. Decision Right eligibility may require one or more authority bases, e.g. legal, organisational, financial, programme, governance, security, release or sponsor authority.
6. A Decision Right must state whether one holder is sufficient or a multi-human governance act is required.
7. Holder identity is runtime/assignment data later; the registry only defines eligibility rules.
8. If no eligible holder is available, the decision is unsatisfied/unmade; authority cannot be inferred from convenience.

---

# 6. Cardinality and collective authority

Decision Rights must declare decision cardinality:

- `SINGLE_HOLDER`
- `MULTI_HOLDER_ALL_REQUIRED`
- `MULTI_HOLDER_THRESHOLD`
- `GOVERNANCE_BODY_DECISION`

If using `MULTI_HOLDER_THRESHOLD`, the registry must state the threshold semantics declaratively without implementing voting/runtime.

Rules:
- cardinality cannot be bypassed by delegation unless the Decision Right explicitly permits it;
- one person cannot count twice under two labels in the same decision instance;
- a governance-body decision is not equivalent to one member acting alone;
- absent required participants => decision not made.

---

# 7. Delegation model

This is a core Phase 7 question.

Define a declarative delegation policy per Decision Right:

- `NON_DELEGABLE`
- `DELEGABLE_WITHIN_ELIGIBILITY`
- `DELEGABLE_WITH_ADDITIONAL_CONSTRAINTS`

A delegation declaration must define:
- who may delegate by eligibility class;
- who may receive delegation by eligibility class;
- scope of delegation;
- time/context limits;
- whether re-delegation is prohibited or allowed;
- evidence required;
- revocation semantics.

Mandatory rules:

1. Delegation transfers only the declared Decision Right scope, not Role authority or professional ownership.
2. Delegation never widens the Decision Right subject/effect.
3. Delegation cannot bypass cardinality requirements.
4. Delegation chain must be bounded; default re-delegation = prohibited unless explicitly allowed.
5. Delegation expiry/revocation must invalidate future exercise but not erase historical valid decisions.
6. A revoked delegation does not automatically reverse a previously valid decision.
7. Emergency delegation must not become permanent authority by use.
8. Runtime later records delegation instances; Phase 7 defines semantics only.

---

# 8. Revocation and supersession

Distinguish:

- **holder/delegation revocation** — removes future ability to exercise authority;
- **decision supersession** — a later valid decision replaces the operative effect of an earlier one;
- **decision reversal** — where the Decision Right explicitly permits reversing an earlier decision;
- **artifact/workflow supersession** — upstream object version becomes obsolete.

Mandatory rules:
- deleting or revoking a holder does not erase the audit trail;
- superseded decision remains historically visible;
- reversal requires a Decision Right whose scope permits it;
- a decision cannot be silently “edited” after the fact;
- correction is a new Decision Record linked to the prior record.

---

# 9. Decision evidence model

Every Decision Record must later be able to prove:

1. `decision.<id>` used;
2. Decision Right version;
3. exact subject/artifact/workflow/handoff/review context;
4. subject version/hash/reference identity where applicable;
5. human holder identity later at runtime;
6. holder eligibility basis;
7. delegation chain/reference if applicable;
8. decision outcome;
9. declared conditions;
10. open findings/risks/assumptions known at decision time;
11. required prerequisite reviews/gates and their statuses;
12. rationale / decision basis;
13. evidence considered;
14. timestamp later at runtime;
15. expiry/review date if applicable;
16. supersedes/superseded-by linkage;
17. dissent/abstention where collective authority uses it, if governance design requires;
18. emergency basis and retrospective obligations where relevant.

This is a semantic record model, not DB schema.

---

# 10. Gate satisfaction semantics

Define the relationship:

`HUMAN_GATE_REFERENCE -> decision.<id> -> Decision Record`

A human gate is satisfied only when:
- the referenced Decision Right exists;
- an eligible holder/cardinality requirement is met;
- prerequisites required by the Decision Right are met or an allowed exceptional path is explicitly used;
- required evidence is present;
- the Decision Record contains a permitted outcome whose declared effect satisfies that gate.

Critical distinctions:

- “Decision requested” != gate satisfied.
- “Decision meeting happened” != gate satisfied.
- “Approval email exists” != gate satisfied unless it can be attributable to the Decision Right and required evidence.
- `DEFER`, `ESCALATE` or `REJECT` normally do not satisfy a positive progression gate unless the Decision Right explicitly defines another effect.
- missing or invalid authority => gate unsatisfied.

---

# 11. Exceptional progression

This must close the forward-reference semantics already used in Phase 5/6.

Define a reusable rule:

A named external `decision.<id>` may permit exceptional progression with an unresolved item/review only if:
- the Decision Right explicitly includes that exception in its scope;
- the unresolved item remains visible/open;
- Review status remains unchanged (`NOT_SATISFIED`, open finding, etc.);
- the Decision Record names the unresolved item/finding/risk;
- consequences/conditions are recorded;
- expiry/revisit trigger is declared where applicable;
- downstream Workflow/Handoff receives the open-item carry;
- the decision does not claim the underlying issue is resolved.

Decision Right may authorize **progression**, not fictional resolution.

---

# 12. Risk acceptance / waiver boundary

Do not conflate:

- accepting risk;
- waiving a process requirement;
- approving progression;
- approving an artifact;
- accepting legal/compliance nonconformance;
- overriding law/regulation.

Rules:

1. No Decision Right may waive mandatory law/regulation by registry declaration.
2. A risk-acceptance Decision Right must declare which risk class/scope it may accept.
3. It must identify residual risk and evidence basis.
4. Risk remains recorded after acceptance.
5. Acceptance may have expiry/review trigger.
6. A process waiver must be separately scoped from risk acceptance if effects differ.
7. Review findings remain findings after waiver/risk acceptance.
8. A human authority cannot approve outside the legal/organisational authority represented by the Decision Right.

---

# 13. Emergency authority

Define one bounded emergency-decision architecture.

Emergency Decision Rights must declare:
- objective emergency trigger;
- what normal prerequisite/gate may be bypassed, if any;
- what can never be bypassed;
- eligible emergency authority class;
- maximum decision scope;
- time validity;
- mandatory evidence at exercise time;
- mandatory retrospective review/ratification or follow-up;
- expiry and rollback/recovery expectations where relevant.

Rules:
- urgency itself is never authority;
- emergency authority is not standing ordinary authority;
- emergency use does not satisfy skipped reviews retroactively;
- skipped reviews remain skipped/open until separately completed;
- retrospective review does not rewrite the historical emergency decision.

Use `decision.emergency_production_change` as one stress-test reference, but do not make software the only emergency model.

---

# 14. Cancellation / termination authority

Define who may cancel/terminate governed paths by Decision Right semantics, not Workflow ownership.

A Workflow itself cannot decide cancellation authority.

Decision Right must state whether it may:
- cancel before commitment;
- terminate after commitment;
- pause/suspend;
- reject and return to rework;
- abandon with open items retained;
- reverse a prior progression decision.

Cancellation/termination must preserve:
- reason;
- current state;
- open findings/risks;
- artifacts/evidence;
- prior decisions;
- external commitments already made.

No destructive history erasure.

---

# 15. Knowledge-state boundary

Decision Right may support bounded knowledge-state transitions only where explicitly governed.

At minimum distinguish:

- `REVIEWED` remains review-governed, not Decision Right-created by default;
- `APPROVED` requires a bounded approval Decision Right if the architecture uses that state;
- `CANONICAL` requires a distinct canonical-promotion authority and cannot be inferred from generic approval;
- `SUPERSEDED` may follow a valid supersession decision but prior artifact/record remains retained.

A Decision Right may never turn:
- `UNKNOWN` into FACT;
- `ASSUMPTION` into FACT;
- `CONFLICT_DETECTED` into resolved;
- `AI_SUGGESTION` directly into CANONICAL without governed human decision and prerequisite controls.

---

# 16. Decision Right composition / dependencies

Define whether Decision Rights may depend on other Decision Rights.

Preferred foundation rule:
- dependencies allowed only as bounded prerequisite references;
- dependency points to concrete `decision.<id>`;
- required prior outcome is declared;
- satisfaction is not transitive;
- authority does not transfer;
- direct/transitive cycles prohibited;
- dependency creates no runtime call semantics;
- collective/dual-control requirements should generally use cardinality inside one Decision Right rather than chaining pseudo-decisions.

If you find a stronger architecture, document it.

---

# 17. Decision Right Universe

Build a candidate universe from all existing upstream `decision.<id>` references plus necessary architecture-level gaps.

Target approximately **20–35 candidate Decision Rights** across 7–10 families.

Suggested families:

1. Workflow / Progression
2. Project / Investment / Readiness
3. Programme / Grant / Submission
4. Financial / Commercial / Contractual Commitment
5. Legal / Compliance / Risk Acceptance
6. Publication / Disclosure / Canonical Promotion
7. Product / Software / Security / Release
8. Emergency / Exception
9. Cancellation / Termination / Reversal

Classify every upstream `decision.<id>` as:
- VALID DECISION RIGHT
- LIKELY DECISION RIGHT NEEDS BOUNDARY REFINEMENT
- REVIEW / QUALITY GATE IN DISGUISE
- ROLE RESPONSIBILITY IN DISGUISE
- WORKFLOW PROGRESSION LOGIC IN DISGUISE
- RUNTIME PERMISSION / IAM IN DISGUISE
- DUPLICATE / OVERLAP

Do not silently normalize references. Record proposed consolidations separately.

---

# 18. Required exemplar Decision Rights

Create **8 exemplar Decision Right Cards** chosen to stress-test distinct authority boundaries:

1. `decision.exceptional_progression`
2. `decision.project_readiness_progression`
3. `decision.grant_submission`
4. `decision.external_publication`
5. `decision.contractual_commitment`
6. `decision.risk_acceptance`
7. `decision.production_release`
8. `decision.emergency_production_change`

If exact upstream IDs differ, preserve existing IDs where possible and explain any normalization proposal rather than silently renaming them.

Each exemplar must include:
- identity;
- decision family/class;
- decision subject;
- allowed outcomes;
- effect of each allowed outcome;
- holder eligibility classes;
- cardinality;
- delegation policy;
- revocation/supersession semantics;
- prerequisites;
- Review/Handoff/Workflow references;
- required evidence;
- open-item/finding/risk handling;
- expiry/re-decision trigger;
- exceptional progression rule if applicable;
- risk/waiver boundary if applicable;
- emergency rule if applicable;
- knowledge-state effect;
- out-of-scope authority;
- version/change control;
- non-runtime statement.

All exemplar cards remain `PROPOSED`.

---

# 19. Required deliverables

Create:

1. `architecture/decision-rights-registry-design.md`
2. `decisions/_standards/common-decision-right-constraints.md`
3. `decisions/_templates/decision-right-card-template.md`
4. `decisions/_templates/decision-record-template.md`
5. `decisions/master-decision-right-universe.md`
6. `decisions/exemplars/exceptional-progression.md`
7. `decisions/exemplars/project-readiness-progression.md`
8. `decisions/exemplars/grant-submission.md`
9. `decisions/exemplars/external-publication.md`
10. `decisions/exemplars/contractual-commitment.md`
11. `decisions/exemplars/risk-acceptance.md`
12. `decisions/exemplars/production-release.md`
13. `decisions/exemplars/emergency-production-change.md`
14. `reviews/phase-7-foundation-self-check.md`

No DB schema or runtime implementation.

---

# 20. Common Decision Right Constraints — minimum rules

Include at least:

1. Decision Right grants no professional competence.
2. Role competence does not create Decision Right authority.
3. Workflow leadership does not create approval authority.
4. Reviewer status does not create approval authority.
5. Artifact ownership does not automatically create commitment authority.
6. Decision Right subject/effect must be bounded.
7. Decision Record != Decision Right.
8. Decision requested != decision made.
9. Meeting/email != valid Decision Record unless attributable to right/evidence.
10. Decision Right cannot make Review `SATISFIED`.
11. Decision Right cannot erase findings, risks, assumptions, UNKNOWN or conflicts.
12. Exceptional progression keeps unresolved items open.
13. Risk acceptance does not erase risk.
14. No registry Decision Right may waive law/regulation.
15. Generic approval does not imply canonical promotion.
16. Delegation cannot widen scope or bypass cardinality.
17. Revocation affects future exercise, not historical records.
18. Decision records are immutable historical events; corrections use superseding records.
19. Emergency urgency != authority.
20. Emergency authority is bounded/temporary and requires retrospective obligations.
21. Cancellation retains history/evidence/open items.
22. Decision dependencies cannot transfer authority or satisfaction.
23. Runtime must validate against registry, not mutate semantics.
24. No model/agent may become Decision Right holder by model identity alone.

---

# 21. Human Approval Matrix

Create a matrix section in the architecture or universe showing at minimum, for each exemplar:

- Decision Right ID
- Decision class
- Subject
- Holder eligibility class
- Cardinality
- Delegation policy
- Primary upstream trigger/reference
- Required review state
- External commitment? yes/no
- Can permit exceptional progression? yes/no
- Can accept risk? yes/no
- Can change knowledge state? bounded value

This is architecture guidance, not runtime assignment.

---

# 22. Self-checks

`reviews/phase-7-foundation-self-check.md` must run at least **40 checks**.

At minimum verify:

1. Phase 3 Role Cards unchanged.
2. Approved Phase 4 architecture/mappings unchanged.
3. Approved Phase 5 Workflow semantics unchanged.
4. Approved Phase 6 Handoff/Review semantics unchanged.
5. All Phase 7 artifacts PROPOSED.
6. Identity separation preserved.
7. Decision Right != Decision Record explicit.
8. No named human holder bound.
9. No model/provider holder bound.
10. No Decision Right grants professional competence.
11. Workflow lead does not imply authority.
12. Reviewer does not imply authority.
13. Artifact owner does not imply commitment authority.
14. Holder eligibility class exists on every exemplar.
15. Cardinality exists on every exemplar.
16. Delegation policy exists on every exemplar.
17. Revocation/supersession semantics exist.
18. Required Decision Record evidence model complete.
19. Gate satisfaction requires valid Decision Record.
20. Requested/pending decision != gate satisfied.
21. Review `NOT_SATISFIED` cannot be relabelled by Decision Right.
22. Exceptional progression keeps finding/open item unresolved.
23. Decision Right cannot erase risk/finding/UNKNOWN/conflict.
24. Risk acceptance retains residual risk.
25. Law/regulation cannot be waived.
26. Generic approval does not imply CANONICAL.
27. Canonical promotion requires distinct bounded authority if represented.
28. Emergency urgency != authority.
29. Emergency right has objective trigger/time scope/retrospective obligation.
30. Delegation cannot widen scope.
31. Delegation cannot bypass cardinality.
32. Default re-delegation prohibited unless explicit.
33. Revocation does not erase historical decisions.
34. Corrections use new superseding record.
35. Cancellation retains history.
36. Decision dependency cycles prohibited.
37. Universe candidate count within target 20–35 unless explicitly justified.
38. Duplicate candidate IDs = 0.
39. All existing upstream `decision.<id>` references accounted for.
40. Eight exemplar cards exist.
41. Human Approval Matrix covers all eight exemplars.
42. No DB/API/UI/runtime/orchestrator/model/agent implementation.
43. No PR created.
44. No Phase 7 APPROVED/CANONICAL artifact.
45. No exemplar allows `APPROVE_WITH_CONDITIONS` without open-condition carry/expiry semantics.
46. No exemplar treats email/meeting as sufficient authority evidence by itself.
47. Production release and emergency production change remain distinct.
48. Risk acceptance and process exception remain distinct.
49. External publication and canonical promotion remain distinct unless explicitly justified otherwise.
50. Grant submission authority does not absorb programme-compliance review.

If a check fails, fix architecture/content, not the test, unless the test is demonstrably wrong.

---

# 23. Open architecture questions

Surface and classify at minimum:

1. Whether organisational authority eligibility can be fully registry-defined or partly runtime/organisation-specific.
2. Whether one human may exercise multiple Decision Rights in the same decision chain.
3. Whether some Decision Rights require mandatory separation of duties.
4. Whether collective decisions need abstention/dissent semantics in foundation.
5. Whether approval expiry should be globally standardised or right-specific.
6. Whether risk-acceptance authority should use a shared risk-class ceiling model.
7. Whether canonical promotion belongs here or Phase 8 Memory/Canonical governance.
8. Whether Decision Right dependency needs first-class composition or only prerequisites.
9. Whether emergency retrospective ratification is a new Decision Right or a review/decision dependency.
10. Whether reversal is always a new Decision Right or an allowed outcome of the original right.

Classify each as:
- MUST RESOLVE IN PHASE 7 FOUNDATION
- SAFE TO DEFER WITH EXPLICIT RULE
- PHASE 8 CONCERN
- RUNTIME/ORGANISATION-PHASE CONCERN

Do not hide unresolved authority ambiguity.

---

# 24. Commit / push

If and only if all required deliverables exist and the self-check is complete, commit exactly:

`docs: add Phase 7 Decision Rights foundation`

Push to:

`origin architecture/phase-7-decision-rights`

Do not create a PR.

---

# 25. Required final output

Return exactly:

### A. FOUNDATION CREATED
Files, baseline, status.

### B. DECISION RIGHT MODEL
Identity, classes, effect semantics.

### C. HOLDER / CARDINALITY / DELEGATION
Eligibility, collective authority, delegation/revocation.

### D. DECISION RECORD / GATE SATISFACTION
Evidence model and gate semantics.

### E. EXCEPTION / RISK / EMERGENCY
Exceptional progression, risk acceptance, emergency boundaries.

### F. DECISION UNIVERSE
Families, candidate count, upstream reference accounting, overlaps.

### G. EXEMPLAR DECISION RIGHTS
Eight exemplars and key stress-test boundary of each.

### H. HUMAN APPROVAL MATRIX
Summary and any authority gaps.

### I. PHASE BOUNDARIES
What remains Phase 8/runtime/organisation-specific; upstream immutability.

### J. SELF-CHECK
PASS/FAIL count and honesty notes.

### K. OPEN ARCHITECTURE QUESTIONS
Each question with disposition.

### L. COMMIT / PUSH
Commit SHA, exact message, push result, remote HEAD, PR status.

### M. NEXT-STEP READINESS
Choose exactly one:
- READY FOR INDEPENDENT PHASE 7 FOUNDATION AUDIT
- NOT READY

Do not claim Phase 7 approval.