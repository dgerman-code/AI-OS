# Phase 14 — Implementation Specification Foundation Prompt

## Repository / branch / baseline

Repository: `dgerman-code/AI-OS`

Branch: `spec/phase-14-implementation-specification`

Human-approved Phase 13 approval commit / starting point:

`2c4b90def9a60f8b384feef10f8428c5b437597c`

Phase 13 reviewed system baseline:

`66927a9d535ed8de31157ca1b23c860a75448a8e`

Phase 12 approved implementation baseline:

`f5f8dd76ca8283eed969928b4ec1cd9f48f04dc7`

## Mode

You are writing the **Phase 14 Implementation Specification** for AI-OS.

This is a specification phase, not a production implementation phase.

Do not deploy anything. Do not create infrastructure. Do not introduce live provider SDKs, secrets, production databases, queues, workers, schedulers, IAM, migrations, or external services unless only as explicitly specified interfaces / contracts / schemas. Do not create a PR.

Do not modify approved Phase 1–13 architecture semantics. If you find a real contradiction, stop and report it rather than silently changing the architecture.

All Phase 14 artifacts must remain `PROPOSED` until independent audit and explicit human approval.

---

# 1. GOVERNING OBJECTIVE

Turn the human-approved Phase 1–13 architecture into a production-grade **implementation specification** detailed enough that a separate engineering team can implement AI-OS without inventing governance semantics.

The specification must bridge:

approved architecture → concrete components → data contracts → schemas → APIs → storage constraints → transaction boundaries → runtime responsibilities → failure behavior → security boundaries → observability → migration strategy → test strategy → deployment topology.

But it must preserve the governing invariants:

- ROLE != AGENT INSTANCE
- MODEL != ROLE
- ROUTER != ORCHESTRATOR
- REVIEW PROFILE != REVIEW INSTANCE
- DECISION RIGHT != DECISION RECORD
- KNOWLEDGE != CANONICAL RECORD
- ARTIFACT != STORAGE RECORD
- RUNTIME EVENT != AUDIT EVENT
- CREDENTIAL != HUMAN AUTHORITY
- HUMAN AUTHORITY remains explicit and cannot be inferred from model output, service identity, urgency, timeout, confidence, RLS, credentials, logs, routing, or execution completion.

The implementation specification must fail closed wherever the architecture fails closed.

---

# 2. REQUIRED SOURCE MATERIAL

Before writing new Phase 14 artifacts, read the approved architecture and approval records for Phases 7–13, especially:

- `architecture/decision-rights-registry-design.md`
- `decisions/master-decision-right-universe.md`
- `knowledge/*`
- `architecture/model-registry-router.md`
- `models/_templates/routing-decision-template.md`
- `architecture/storage-persistence-architecture.md`
- `storage/*`
- `architecture/orchestrator-architecture.md`
- `orchestration/*`
- `implementation/phase-12/*`
- `reviews/phase-12-final-approval.md`
- `reviews/phase-13-final-approval.md`
- the Phase 13 system architecture review evidence / findings available in the repository or approval record.

Phase 12 is a reference implementation, not a source allowed to override architecture.

When Phase 12 and approved architecture differ, approved architecture wins.

---

# 3. PHASE 13 DEBT THAT PHASE 14 MUST RESOLVE IN SPECIFICATION

The Phase 13 review classified the following as implementation-spec items. They are mandatory Phase 14 work, not optional notes.

## M-1 — Four-axis knowledge model

Do not inherit the Phase 12 collapsed `Origin` / `Canonicality` shortcuts.

Specify the full four-axis knowledge model using the approved Phase 8 terminology:

Epistemic type:
- SOURCE
- EVIDENCE
- FACT_CLAIM
- ASSUMPTION
- CALCULATION
- INFERENCE
- AI_SUGGESTION
- UNKNOWN

Governance state:
- DRAFT
- REVIEWED
- APPROVED
- CANONICAL
- SUPERSEDED
- RETRACTED
- REJECTED

Origin:
- HUMAN_ORIGIN
- AI_ASSISTED
- AI_GENERATED
- EXTERNAL_ORIGIN

Conflict state / flag remains orthogonal.

Specify persistence, immutability/versioning, valid transitions, adoption of AI suggestions, conflict handling, freshness, supersession, canonical promotion preconditions, and cross-scope transfer behavior.

AI_SUGGESTION must never silently change epistemic type merely because a human reviewed, edited, approved, or accepted it.

## M-2 — Runtime event vs governance evidence

Execution/runtime events must be specified as coordination history, **not governance evidence**.

Specify separate schemas and storage responsibilities for:

- runtime/execution event
- audit event
- provenance record
- Decision Record
- review record
- knowledge evidence record

Specify the 13-field execution event contract required by the approved orchestration architecture, including separate human and system identities and authority reference where applicable.

No operational log may satisfy a review, decision, canonicalisation, publication, risk-acceptance, or other governance gate.

## M-3 — Full six-part routing reproducibility lineage

A recorded Routing Decision must carry the approved six-part reproducibility set, not just model + profile:

1. stable Model Profile identity
2. Model Profile registry version
3. originator release identity
4. provider-offering mapping identity + version
5. Provider Profile version
6. Deployment Profile version

Also include routing policy version and eligibility evidence / constraints sufficient to reconstruct why the candidate was selected.

Reproducibility of routing decision != deterministic reproduction of model output.

## M-4 — Identity-level segregation of duties

Do not stop at an `independence_class` label.

Specify actor identity relationships and enforcement for:

- author / producer identity
- reviewer identity
- review assignment identity
- Decision Right holder identity
- Decision Record author identity
- `DECISION_RIGHT_SEPARATION`
- producer-review prohibition where independent review is required
- conflict-of-interest / incompatible-duty rules

A bounded contributor cannot satisfy a full independent review requirement.

## M-5 — Scope identity as path

Do not implement Scope as an opaque flat string only.

Specify scope path identity and full ancestry across the approved hierarchy:

GLOBAL →
- ORGANISATION
- INDEPENDENT BUSINESS / VENTURE
- PERSONAL / AD-HOC INITIATIVE

Under ORGANISATION as applicable:
- PERMANENT FUNCTION / BUSINESS AREA
- PROGRAMME / PORTFOLIO
- PRODUCT / SERVICE
- PROJECT
- OPERATIONAL WORKSTREAM
- TASK

PROJECT may be directly under ORGANISATION or under PROGRAMME / PORTFOLIO.

Specify:

- canonical scope path representation
- stable scope node identity vs path identity
- ancestry queries
- scope compatibility / applicability modes from Phase 8
- ancestor fallback
- narrowing
- cross-scope transfer
- sensitivity labels
- residency
- no implicit sibling or unrelated-scope inheritance

## M-6 — Machine-readable approval state

Human approval must not exist only as prose in `reviews/phase-N-final-approval.md`.

Specify a machine-readable approval registry / approval-state record that can answer:

- what artifact / architecture baseline / registry version is approved
- approval status
- approving human authority
- Decision Right used where applicable
- approval date/time
- source approval record
- superseded/revoked status
- scope of approval
- explicit non-scope / conditions / deferred items

Do not rewrite historical artifact Status fields merely to make validators green. Specify a forward-compatible authoritative approval-state mechanism.

---

# 4. ADDITIONAL MANDATORY PHASE 14 ITEMS

The Phase 13 review also requires explicit specification of these items.

## 4.1 Bounded rework loops

Specify:

- rework loop identity
- iteration counter
- max iteration limit
- preserved historical review/work instances
- criteria for re-entry
- escalation on exhaustion
- no graph-cycle ambiguity

## 4.2 Persistent uniqueness and at-most-once governed records

The Phase 12 in-memory append-only store is not sufficient for production.

Specify database-level uniqueness and transaction rules for stable governed identities, including at least:

- Decision Records
- Review Instances
- Routing Decisions
- Model Results
- Human interventions
- gate evidence records
- authority-bearing irreversible act records

At-most-once must be tied to governed record identity and durable uniqueness, not process memory.

Do not claim distributed exactly-once semantics.

## 4.3 Concurrency and race implementation

Translate the approved Phase 11 race table into enforceable persistence semantics:

- optimistic concurrency / version columns or equivalent
- stale write detection
- idempotency keys
- causation / correlation identities
- late review handling
- late Decision Record handling
- no last-write-wins for governance state
- BLOCK / IGNORE_AS_STALE / SUPERSEDE / RECONCILE / ESCALATE outcomes

## 4.4 Compensation and non-replayable acts

Specify how compensation is represented as a **new governed act**, never as magical rollback of a completed external act.

For irreversible or non-retryable actions specify:

- intent record
- authorisation record
- execution record
- external-effect uncertainty state
- reconciliation
- compensation request / approval / execution lineage

## 4.5 Full SUPERSEDED path

Specify how workflow runs, records, knowledge, artifacts, policies, and registry versions become superseded without destructive rewrite.

## 4.6 Deferred Decision Rights

Do not invent authority.

Phase 13 noted missing mapped Decision Rights for:

- canonical knowledge promotion/status change
- cross-scope transfer authority where not already explicitly mapped
- controlled destruction of governed content
- destructive production database migration

For Phase 14:

- identify every implementation operation that requires one of these rights;
- mark it BLOCKED / UNIMPLEMENTABLE UNTIL RIGHT IS MAPPED where no approved Right exists;
- define the technical enforcement hook / interface;
- do not create a new approved Decision Right in Phase 14.

A later explicit Phase 7 governance change may map them.

---

# 5. REQUIRED PHASE 14 ARTIFACT SET

Create a coherent specification package under a new top-level directory:

`implementation-spec/`

At minimum produce:

1. `implementation-spec/README.md`
   - purpose
   - authority hierarchy
   - approved baselines
   - non-goals
   - document map

2. `implementation-spec/system-component-model.md`
   - production component boundaries
   - ownership of responsibilities
   - forbidden responsibility crossings

3. `implementation-spec/domain-identity-model.md`
   - all governed identities
   - stable IDs
   - version identities
   - references
   - non-substitutability

4. `implementation-spec/scope-and-context-model.md`
   - path-based scope model
   - ancestry
   - sensitivity / residency
   - transfer and narrowing

5. `implementation-spec/knowledge-and-canonical-model.md`
   - full four-axis model
   - versioning
   - conflicts
   - freshness
   - canonical promotion hooks

6. `implementation-spec/decision-review-authority-model.md`
   - Decision Rights / Decision Records
   - holder resolution
   - SoD
   - review independence
   - missing-right handling

7. `implementation-spec/model-router-runtime-contract.md`
   - routing request
   - eligibility input
   - six-part reproducibility
   - Routing Decision persistence
   - Model Invocation / Model Result lineage

8. `implementation-spec/orchestrator-runtime-contract.md`
   - Workflow Run / Work Item
   - states
   - gates
   - halted guard
   - atomic acts
   - retry / replay
   - compensation
   - rework loops

9. `implementation-spec/persistence-and-transaction-model.md`
   - PostgreSQL logical schema boundaries
   - transaction scopes
   - uniqueness
   - optimistic concurrency
   - append-only records
   - object storage commit protocol
   - orphan handling

10. `implementation-spec/audit-provenance-observability.md`
   - separate runtime event / audit / provenance / logs / Decision Records
   - correlation / causation
   - observability never authority

11. `implementation-spec/api-command-contracts.md`
   - command/query boundary
   - API-level preconditions
   - idempotency
   - expected errors
   - no authority inference

12. `implementation-spec/security-identity-access.md`
   - human identities
   - service identities
   - credentials
   - RLS/authorization enforcement boundary
   - secrets
   - tenant/scope isolation
   - admin limitations

13. `implementation-spec/approval-state-registry.md`
   - machine-readable approval state
   - provenance
   - supersession / revocation

14. `implementation-spec/migrations-versioning-compatibility.md`
   - schema migration rules
   - destructive migration blocking
   - backward compatibility
   - registry version compatibility

15. `implementation-spec/failure-recovery-race-model.md`
   - failures
   - retries
   - races
   - unknown external effects
   - reconciliation / compensation

16. `implementation-spec/deployment-topology-and-environments.md`
   - logical environments only
   - dev/test/staging/prod separation
   - no secrets or provider-specific deployment implementation

17. `implementation-spec/test-and-assurance-strategy.md`
   - unit / contract / integration / adversarial / mutation / concurrency / migration / recovery tests
   - architecture invariant tests
   - approval-gate tests

18. `implementation-spec/implementation-sequencing.md`
   - build order
   - dependencies
   - safe milestones
   - stop/go gates

19. `implementation-spec/open-items-and-blocked-authorities.md`
   - all known deferred items
   - missing Decision Rights
   - unresolved production choices

20. `implementation-spec/phase-14-self-check.md`
   - completeness matrix against Phase 13 findings M-1…M-7
   - Phase 1–13 invariant preservation
   - explicit non-production status

Also create:

`validation/phase_14_validation.py`

The validator must be deterministic and standard-library only.

---

# 6. SPECIFICATION DEPTH

This must not be aspirational prose.

For every major domain object / persisted record specify, where applicable:

- canonical name
- stable identity type
- version identity
- owning source of truth
- required fields
- field types
- nullability
- immutable vs mutable fields
- uniqueness constraints
- foreign/reference constraints
- lifecycle states
- valid transitions
- actor allowed to propose/change
- human authority required
- review required
- audit requirements
- provenance requirements
- idempotency behavior
- concurrency behavior
- retention / supersession behavior
- error outcomes

Use tables where they improve precision.

You may specify SQL-like constraints and REST/command shapes, but do not create executable production migrations or deployed API code in Phase 14.

---

# 7. TRANSACTIONAL RULE

Carry forward the Phase 12 invariant:

**construct → validate → preflight → commit**

But specify how this works under durable storage.

For every governed act identify:

- read set
- validation set
- concurrency token/version checks
- records to insert/update
- uniqueness constraints relied upon
- event/audit writes
- commit boundary
- failure behavior before commit
- behavior if external effect happens but local commit certainty is unknown

No ordinary governed failure may leave an internally inconsistent partial governance state.

Where atomicity cannot span an external system, specify staged / outbox / reconciliation semantics instead of pretending there is a distributed transaction.

---

# 8. APPROVAL / AUTHORITY SAFETY

The specification may describe how an approved Decision Right would be enforced, but it must never manufacture approval authority.

Missing Right → BLOCK / ESCALATE / UNIMPLEMENTABLE UNTIL GOVERNED CHANGE.

Do not substitute:

- admin role
- RLS bypass
- service account
- database owner
- model selection
- reviewer
- workflow owner
- orchestrator
- system control profile

for a human Decision Right.

---

# 9. MODEL / PROVIDER INDEPENDENCE

Keep the system provider-independent.

Specify adapter contracts rather than embedding one vendor.

Provider, endpoint, deployment, Model Profile, Model release, routing policy, Routing Decision, Model Invocation, and Model Result remain separate identities.

Do not make the product architecture depend on Claude, OpenAI, or any single vendor.

---

# 10. STORAGE / SUPABASE POSITION

The approved architecture allows PostgreSQL/Supabase as operational storage, but the Phase 14 specification must describe logical PostgreSQL constraints and security boundaries independently from a specific hosted product where possible.

If Supabase-specific capabilities are mentioned, label them as one implementation option, not as architecture identity.

RLS is enforcement, not authority.

Service-role credentials are credentials, not human authority.

---

# 11. VALIDATOR REQUIREMENTS

`validation/phase_14_validation.py` must verify at minimum:

- all required Phase 14 files exist;
- all remain `PROPOSED`;
- approved Phase 1–13 artifacts are unchanged;
- no production/runtime implementation files, migrations, secrets, SDK dependencies, or infrastructure manifests are added;
- identity separation statements are present and consistent;
- four-axis knowledge vocabulary is complete and exact;
- scope path hierarchy is complete;
- six-part routing reproducibility contract is complete;
- runtime event is explicitly not governance evidence;
- Decision Right gaps are not silently filled;
- machine-readable approval state is specified;
- bounded rework loop semantics are specified;
- persistent uniqueness / at-most-once semantics are specified without distributed exactly-once claims;
- SoD / author-reviewer / Decision Right separation is specified;
- race/concurrency outcomes match Phase 11;
- docs do not claim production readiness;
- a completeness matrix covers Phase 13 M-1 through M-7.

The validator itself is an assurance tool, not governance authority.

---

# 12. TEST / REVIEW EXPECTATION

Before declaring the Phase 14 foundation ready for independent audit:

1. run Phase 14 validator default / verbose / JSON;
2. run regression validators for Phases 8–12 and report inherited failures exactly, without fixing them out of scope;
3. verify no protected Phase 1–13 semantic files changed;
4. verify no PR exists / create none;
5. perform self-check against every Phase 13 implementation-spec item;
6. explicitly list any specification choice that still requires human architectural decision.

Do not declare Phase 14 approved.

Final readiness sentence only if all required specification artifacts and checks are complete:

`READY FOR INDEPENDENT PHASE 14 IMPLEMENTATION SPECIFICATION AUDIT`

---

# 13. OUTPUT REPORT

Return a concise but complete report with sections:

A. Specification summary
B. Approved baseline / containment
C. Component architecture
D. Domain identities
E. Scope/context model
F. Knowledge/canonical model
G. Decision/review/authority model
H. Model/router runtime contract
I. Orchestrator runtime contract
J. Persistence/transactions/concurrency
K. Audit/provenance/observability
L. Security/access/approval-state
M. Migration/deployment/test strategy
N. Phase 13 debt closure matrix M-1…M-7
O. Validation/regression results
P. Files created/changed
Q. Remaining open items / blocked authorities
R. Readiness verdict

Commit the Phase 14 specification foundation on `spec/phase-14-implementation-specification` with a clear commit message such as:

`docs: add Phase 14 implementation specification foundation`

Push the branch. Do not create a PR.
