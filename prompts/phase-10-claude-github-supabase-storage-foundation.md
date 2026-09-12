# Claude Code Prompt — Phase 10 GitHub / Supabase / Storage Architecture Foundation

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-10-github-supabase-storage`
Human-approved Phase 9 baseline: `a94de435f0a47f9910d804029cc74bb7c995434a`

You are now beginning **Phase 10 — GitHub / Supabase / Storage Architecture**.

This is an ARCHITECTURE FOUNDATION phase, not implementation.

Do not create a PR.
Do not mark Phase 10 APPROVED or CANONICAL.
All Phase 10 artifacts must remain `PROPOSED` until independent audit and explicit human approval.

## 0. Preserve approved upstream architecture

Do not redesign or weaken approved Phase 1–9 semantics.

Preserve these separations:
- ROLE != MODEL
- ROLE != AGENT INSTANCE
- WORKFLOW != DECISION RIGHT
- ROUTING DECISION != DECISION RIGHT
- REVIEWER INDEPENDENCE != MODEL DIVERSITY
- SOURCE != EVIDENCE != MEMORY ITEM != KNOWLEDGE CLAIM != CANONICAL RECORD != DECISION RECORD != ARTIFACT
- MODEL PROFILE != PROVIDER != DEPLOYMENT != RUNTIME
- ROUTER != ORCHESTRATOR

Preserve explicit human authority and canonical promotion semantics.

Phase 10 must provide persistence/storage architecture that supports the approved governance model; it must not silently change that model.

## 1. Scope of Phase 10

Design the storage and persistence architecture for AI-OS across three conceptual layers:

1. **GitHub** — governed architecture/code/configuration source, review history, versioned schemas/templates/policies, auditable human-readable artifacts.
2. **Supabase/PostgreSQL** — structured operational metadata, registries, records, relationships, status, lineage, indexes, queryable governance state.
3. **Object/File Storage** — binary/large artifacts, source documents, evidence files, generated outputs, immutable snapshots, exports and archives.

The architecture must explain what belongs where, what does **not** belong where, and which system is authoritative for each data class.

## 2. Required identity boundary

Define explicitly:

`REPOSITORY OBJECT != DATABASE RECORD != FILE OBJECT != ARTIFACT != CANONICAL RECORD != DECISION RECORD != RUNTIME EVENT != SECRET != CREDENTIAL`

Also distinguish:
- logical object identity;
- storage location;
- version identity;
- content hash;
- mutable metadata;
- immutable audit/history record;
- runtime instance/event identity.

A storage backend must never redefine governance identity.

## 3. Source-of-truth matrix

Create a normative Source-of-Truth Matrix for at least:
- system standards and architecture documents;
- Role Registry;
- Skill Registry;
- Review Profile Registry;
- Workflow Registry;
- Decision Rights Register;
- Knowledge / Canonical governance records;
- Model Registry / Provider / Deployment Profiles;
- Routing Policies;
- Routing Decisions;
- Handoff records;
- Review instances/findings;
- Decision Records;
- memory items;
- source/evidence metadata;
- file/binary artifacts;
- runtime logs/events;
- secrets/credentials;
- configuration;
- generated reports/exports;
- backups/snapshots.

For every row specify:
- authoritative system;
- secondary representation(s);
- whether replication is allowed;
- versioning authority;
- write authority;
- canonical promotion implications;
- conflict resolution rule.

No dual-master ambiguity.

## 4. GitHub architecture

Define GitHub's role precisely.

Cover:
- repository/branch/tag/commit semantics;
- architecture vs executable/runtime code boundaries;
- approved baseline recording;
- human approval records;
- schema/template/policy versioning;
- machine-generated artifacts allowed vs prohibited;
- branch naming and phase isolation;
- review/audit trail;
- immutable historical commits;
- protected human-approval semantics;
- how GitHub references DB schema migrations without becoming the operational DB;
- how the repository records expected schema/version compatibility;
- what must never be stored in GitHub (secrets, raw sensitive source payloads, private keys, etc.).

Do not assume GitHub branch protection is configured unless demonstrated; distinguish architectural requirement from runtime configuration.

## 5. Supabase / PostgreSQL architecture

Design conceptual database domains and ownership boundaries.

Do NOT implement SQL migrations yet unless the prompt explicitly asks for schema pseudocode only. Do not connect to any live Supabase project.

Define conceptual schemas/modules such as, if justified:
- governance;
- registry;
- workflow;
- review;
- decisions;
- knowledge;
- routing;
- artifacts;
- audit;
- identity/reference metadata;
- runtime-event metadata (bounded, future-facing).

Do not create arbitrary schemas just for neatness; justify boundaries.

For each domain define:
- owning object types;
- primary keys/stable IDs;
- version columns/version records;
- lifecycle/status ownership;
- lineage links;
- provenance links;
- scope fields;
- sensitivity labels;
- freshness/effective-time fields where relevant;
- audit requirements;
- immutable vs mutable fields;
- soft-delete / retraction / supersession semantics;
- foreign-key/reference expectations;
- cross-registry reference integrity.

Respect Phase 8 terminal `RETRACTED` semantics and Phase 7 append-only decision history.

## 6. Stable IDs and database keys

Define how stable architecture IDs such as:
- `role.*`
- `skill.*`
- `review.*`
- `workflow.*`
- `decision.*`
- `model.*`
- `provider.*`
- `deployment.*`
- `routing_policy.*`

map to database keys.

Required distinction:
- human-readable stable logical ID;
- internal database surrogate key if used;
- version identifier;
- storage object identifier;
- external-provider identifier.

Do not make UUID = governance identity by implication.

## 7. Versioning model

Define a coherent persistence version model across:
- Git commits;
- registry versions;
- database record versions;
- object/file versions;
- snapshot versions;
- policy versions;
- approval baselines;
- schema versions/migrations.

Answer explicitly:
- when a new version is a mutation of the same logical object;
- when a new logical object must be created;
- when supersession is required;
- when append-only history is mandatory;
- when immutability is required;
- how historical Routing Decisions and Decision Records reconstruct the exact references they used.

## 8. Artifact and object storage model

Define an Artifact Object model for file/binary content.

Cover:
- artifact stable ID;
- storage URI/location reference;
- filename/display name;
- MIME/type;
- size;
- content hash;
- encryption state;
- scope;
- sensitivity labels;
- provenance/source;
- producer;
- creation time;
- retention class;
- legal hold if applicable;
- immutable snapshot flag;
- supersedes/superseded-by;
- artifact-to-knowledge / evidence / review / decision links;
- deletion/retraction semantics.

A file path/name must not define artifact identity.

## 9. Content-addressability / integrity

Define how hashes/checksums are used.

Distinguish:
- identity;
- integrity proof;
- deduplication hint;
- immutable snapshot verification.

A content hash must not automatically become the governance ID.

Define expected algorithms abstractly unless a concrete standard is needed; avoid premature implementation lock-in.

## 10. Sensitivity / privacy / residency persistence

Reuse Phase 8 and Phase 9 semantics exactly.

Persist sensitivity as multi-label, not ordinal.

Design how records/files carry:
- multiple sensitivity labels;
- handling obligations;
- scope restrictions;
- residency constraints;
- cross-border restrictions;
- provider/deployment handling posture references where relevant.

Do not invent a total order.

Distinguish metadata that may be stored centrally from sensitive payload content that may require restricted storage.

## 11. RLS / access-control architecture boundary

Define RLS and access control conceptually, but do not implement live policies yet.

Required:
- DB authorization is an enforcement layer, not governance authority;
- Role Card competence != database permission;
- Decision Right holder eligibility != raw DB role;
- human signatory authority != service account capability;
- AI model/provider never gains authority by possessing credentials.

Define access dimensions such as:
- organisation/scope;
- object class;
- sensitivity;
- operation type;
- lifecycle state;
- human/service identity class;
- purpose/use context.

Explicitly discuss deny-by-default for sensitive domains and unknown classification.

## 12. Secrets and credentials

Define secrets architecture.

Must cover:
- secrets never in repository files;
- secret references vs secret values;
- environment-specific secrets;
- service accounts;
- rotation;
- revocation;
- auditability without exposing values;
- least privilege;
- separation between runtime credentials and governance identity;
- future vault/provider abstraction.

Do not name a specific secrets vendor as mandatory unless justified.

## 13. Audit / provenance / event history

Define an append-only audit model capable of recording:
- who/what changed a record;
- previous/new version reference;
- reason/context;
- linked Decision Record where required;
- source/provenance;
- timestamp/effective time;
- system/service identity;
- user/human identity reference;
- correlation/transaction ID;
- immutable event hash/reference if used.

Distinguish:
- operational log;
- audit event;
- Decision Record;
- knowledge provenance;
- Git commit history.

None may be substituted for another.

## 14. Transaction / consistency boundaries

Define consistency requirements for multi-object operations, including:
- Routing Decision + selected version references;
- Decision Record + linked artifact state;
- canonical promotion + canonical record/version;
- review finding + status transition;
- artifact metadata + object upload;
- supersession/retraction.

Specify where strong transactional consistency is required vs eventual consistency acceptable.

Do not promise distributed atomicity across GitHub + PostgreSQL + object storage where not realistic. Define compensating/verification patterns instead.

## 15. Schema migration governance

Define conceptual migration governance:
- migration ID/version;
- forward migration;
- rollback policy vs forward-fix policy;
- compatibility window;
- data backfill;
- destructive-change controls;
- human approval for high-risk migrations;
- migration evidence/testing;
- schema version recording;
- migration history immutability.

GitHub may version migrations; database applies them. Keep those roles separate.

## 16. Environment model

Define conceptual environments at least:
- development;
- test/staging;
- production.

Cover:
- data separation;
- credentials separation;
- schema compatibility;
- test fixtures/synthetic data;
- production-data cloning restrictions;
- promotion path;
- rollback/forward-fix expectations;
- environment-specific storage buckets/containers if appropriate.

Do not assume a particular cloud topology.

## 17. Backup / restore / disaster recovery

Define architecture-level requirements for:
- DB backups;
- object storage versioning/backups;
- repository history;
- point-in-time recovery expectation;
- restore testing;
- recovery metadata;
- corruption detection;
- ransomware/credential-compromise isolation;
- retention windows as policy-configurable;
- legal hold interaction.

Do not invent specific RPO/RTO numbers without evidence. Provide classes/placeholders if needed.

## 18. Retention / deletion / legal hold

Map Phase 8 retention/sensitivity concepts to storage.

Differentiate:
- logical retraction;
- business deletion request;
- physical purge;
- legal hold;
- backup expiry;
- supersession;
- archival.

A canonical or audit history record must not disappear simply because its current representation is superseded.

## 19. Storage failure modes

Model failure cases at minimum:
- DB unavailable;
- object upload succeeds but metadata transaction fails;
- metadata commits but object upload fails;
- hash mismatch;
- object missing;
- stale schema version;
- dangling cross-registry reference;
- duplicate stable ID;
- conflicting version write;
- incomplete migration;
- restore from stale backup;
- storage provider outage;
- secret compromise;
- RLS misconfiguration;
- accidental public exposure.

For each define architectural outcome: BLOCK / RETRY / RECONCILE / ESCALATE / QUARANTINE / RESTORE / HUMAN REVIEW as appropriate.

## 20. Anti-lock-in

Keep architecture provider-independent.

Supabase may be the current PostgreSQL/backend implementation, but conceptual architecture must distinguish:
- PostgreSQL semantics;
- Supabase-specific conveniences;
- object-storage interface;
- secret-management interface;
- Git host interface.

Do not make higher-level governance semantics dependent on a Supabase-specific proprietary feature unless explicitly isolated behind an adapter boundary.

## 21. Required deliverables

Create at minimum:

1. `architecture/storage-persistence-architecture.md`
2. `storage/source-of-truth-matrix.md`
3. `storage/data-domain-model.md`
4. `storage/versioning-and-lineage.md`
5. `storage/artifact-object-model.md`
6. `storage/access-control-and-rls-boundary.md`
7. `storage/audit-provenance-model.md`
8. `storage/migration-and-environment-governance.md`
9. `storage/backup-retention-recovery.md`
10. `storage/failure-modes.md`
11. `storage/_templates/storage-record-template.md`
12. `storage/_templates/artifact-record-template.md`
13. `storage/_templates/audit-event-template.md`
14. `reviews/phase-10-foundation-self-check.md`
15. `validation/phase_10_validation.py`
16. Update `validation/README.md` only as needed.

You may add tightly justified supporting artifacts, but do not proliferate files unnecessarily.

## 22. Validation requirements

Build a deterministic offline validator for Phase 10.

It must check materially, not only string presence.

At minimum validate:
- no dual-master source-of-truth rows;
- each major object class has one authoritative source;
- stable IDs distinct from storage/backend IDs;
- version lineage rules coherent;
- immutable/append-only requirements represented;
- multi-label sensitivity preserved;
- no scalar sensitivity ceiling introduced;
- GitHub/Supabase/object-storage responsibilities remain distinct;
- no secrets/credentials committed in architecture artifacts;
- access control does not create governance authority;
- no Decision Right collapse into IAM/RLS;
- cross-registry reference expectations explicit;
- audit event != Decision Record != Git commit != operational log;
- transaction boundaries explicit;
- no distributed-atomicity fiction across all systems;
- migration governance explicit;
- backup/retention/legal-hold distinctions explicit;
- failure modes cover dangling records / missing object / partial write / public exposure;
- no runtime implementation accidentally introduced;
- Phase 3–9 approved semantics unchanged;
- Phase 9 approval record remains untouched.

Use parsed tables/sections where feasible. Avoid a validator that can pass simply because a phrase exists.

Run Phase 9 validation and ensure its approved architecture remains intact.

## 23. Exemplar records

Create a small number of synthetic exemplars only where they prove architecture boundaries. Suggested:
- one artifact metadata + object reference exemplar;
- one canonical-record/version linkage exemplar;
- one cross-system partial-failure/reconciliation exemplar;
- one restricted multi-label sensitivity storage exemplar;
- one schema migration governance exemplar.

Synthetic IDs only. No real customer/project/user data. No real secrets.

## 24. Open questions

Create and adjudicate open questions for Phase 10.

At minimum address:
- GitHub vs DB source of truth for registry definitions;
- whether approved registry definitions are mirrored into DB or authored there;
- object storage provider abstraction;
- whether files are mutable or new-version-only;
- database temporal/version strategy;
- audit log immutability mechanism boundary;
- retention versus legal hold;
- environment data cloning;
- migration rollback versus forward-fix;
- where Supabase-specific RLS ends and portable authorization begins;
- handling of private/sensitive source documents;
- recovery from DB/object divergence;
- schema compatibility with future orchestrator Phase 11.

Classify each as one of:
- RESOLVED IN FOUNDATION
- MUST RESOLVE BEFORE HUMAN APPROVAL
- SAFE TO DEFER WITH EXPLICIT RULE
- PHASE 11+
- RUNTIME CONCERN

## 25. Non-goals

Do NOT:
- connect to live Supabase;
- create a Supabase project;
- run migrations;
- create live tables;
- create buckets;
- create RLS policies in production;
- create service accounts;
- create secrets;
- deploy anything;
- implement APIs;
- implement orchestration;
- implement RAG;
- implement agents;
- create real user/IAM accounts;
- create real Model/Provider/Deployment profiles;
- rewrite approved Phase 3–9 architecture;
- create a PR.

## 26. Commit / push

After completing and validating the foundation:

Commit exactly:
`docs: add Phase 10 GitHub Supabase Storage foundation`

Push to:
`origin architecture/phase-10-github-supabase-storage`

Do not create a PR.

## 27. Required final response

Return exactly these sections:

### A. PHASE 10 FOUNDATION SUMMARY
### B. SOURCE-OF-TRUTH ARCHITECTURE
### C. GITHUB BOUNDARY
### D. DATABASE / SUPABASE DOMAIN MODEL
### E. STORAGE / ARTIFACT MODEL
### F. IDENTITY / VERSIONING / LINEAGE
### G. SENSITIVITY / ACCESS CONTROL / RLS
### H. AUDIT / PROVENANCE
### I. TRANSACTION / CONSISTENCY MODEL
### J. MIGRATION / ENVIRONMENT GOVERNANCE
### K. BACKUP / RETENTION / RECOVERY
### L. FAILURE MODES
### M. OPEN QUESTIONS
### N. VALIDATION
### O. REGRESSION
### P. FILES CHANGED
### Q. COMMIT / PUSH
### R. NEXT STEP

For section R choose exactly one:
- `READY FOR INDEPENDENT PHASE 10 FOUNDATION AUDIT`
- `NOT READY`

Do not claim approval.