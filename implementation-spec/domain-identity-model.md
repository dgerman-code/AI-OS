# Domain Identity Model

Status: `PROPOSED` — Phase 14 implementation specification
Version: 0.1
Authority: approved Phase 1–13 architecture. Where this document and the approved architecture
differ, the architecture wins and this document is defective.

## 1. The approved separation chain

```
ROLE != AGENT INSTANCE != MODEL != MODEL PROFILE != ROUTER != ORCHESTRATOR != WORKFLOW
     != WORKFLOW RUN != TASK != HANDOFF != REVIEW PROFILE != REVIEW INSTANCE
     != DECISION RIGHT != DECISION RECORD != KNOWLEDGE != CANONICAL RECORD != ARTIFACT
     != STORAGE RECORD != RUNTIME EVENT != CREDENTIAL != HUMAN AUTHORITY
```

Twenty-one objects, 210 ordered pairs, and **every pair is a denial**. The implementation must
make each denial a type error or a constraint violation, never a convention.

## 2. Identifier kinds — Phase 10 `storage/versioning-and-lineage.md` §1, applied

| # | Kind | Shape | Names | May it appear in a governed record? |
|---:|---|---|---|---|
| 1 | **Stable logical ID** | `<kind>.<stable_snake_case_name>` | The governed object for the life of the architecture | **Yes — it *is* the governance identity** |
| 2 | **Internal surrogate key** | Opaque database key | One row in one database | **Never.** Not a governance reference, not quoted in a governed record, not stable across a rebuild |
| 3 | **Version identifier** | Registry version, record version, policy version | Which version of the logical object | Yes, always paired with (1) |
| 4 | **Storage object identifier** | Bucket, prefix, key, object version | Where bytes currently are | Yes, as location — **never as artifact identity** |
| 5 | **External provider identifier** | Originator release identity, offering reference | Something outside AI-OS that a profile describes | Yes, as a described value — never as an internal identity and never authoritative |

**Rule I-1 — two reference categories, and only one of them carries a version.** An earlier
revision of this document said *every* governed reference is a stable-ID/version pair, while its
own inventory listed runtime-instance references that are intentionally unversioned. Both cannot
be true. The rule, stated per category:

| Category | What it names | Reference form | Why |
|---|---|---|---|
| **A — Governed definition or profile** | A thing that is authored, revised and re-approved: Role Card, Skill Card, Workflow Definition, Task within it, Review Profile, Decision Right Card, Orchestrator Policy, Routing Policy, Model Profile, Provider Profile, Deployment Profile, Offering Mapping, Router, Schema | **(stable logical ID, version identity)**, both written as recorded values | The definition changes over time, so a record that names it without a version reconstructs nothing |
| **B — Immutable runtime-instance or governed-record identity** | A thing that happened once and is never revised: Workflow Run, Work Item, Assignment, Agent Instance, Gate Instance, Routing Request, Routing Decision, Model Invocation, Model Result, Review Instance, Decision Record, Handoff, Human Intervention, Scope Node, Runtime Event, Execution Event, Audit Event, Provenance Record, Human Authority, Scope Transfer, Compensation, Rework Loop Instance | **stable immutable record identity alone** | There is no second version of an event that occurred. Inventing one would imply the instance can be revised, which is exactly what append-only forbids |

Two categories sit deliberately in neither and are named so they are not mistaken for an
omission: a **versioned governed record** — Knowledge item, Canonical Record, Artifact, Storage
Record, Approval State — is referenced as *(record identity, record version)* because a
**new version** is created rather than the old one edited; and a **Credential** carries a
rotation generation, which is a lifecycle generation and not a governed version.

**Rule I-1a.** In every category the reference is written as a **recorded value**, never as a
foreign key to a mutable row and never re-resolved at read time. A historical record must
reconstruct what it used, not what the registry says today.

**Rule I-1b — reproducibility without invented versions.** A category-B record is reproducible
because it is immutable and because every category-A reference it holds carries its version. A
Routing Decision has no version of its own and needs none: it is fixed at the instant it was
written, and the six-part set inside it names the versions of everything it depended on. Giving
instance records versions would not add reproducibility; it would suggest a revision path that
must not exist.

**Rule I-2.** A surrogate key never crosses a component boundary, never appears in an API
payload, and never appears in an audit, provenance, Decision, Review, Routing or Knowledge
record.

## 3. Identity kinds and their reference types

Each row defines one non-substitutable reference type. `ID pattern` is the stable logical ID.
`Versioned?` says whether a reference to it must carry a version identity.

| # | Identity | Reference type | ID pattern | Versioned? | Source of truth |
|---:|---|---|---|---|---|
| 1 | Role | `RoleRef` | `role.<name>` | Yes (registry version) | Git (C1) |
| 2 | Agent Instance | `AgentInstanceRef` | `agent_instance.<uuid>` | No — an instance is not versioned | DB (C10) |
| 3 | Model — the **Underlying Model Release** | `ModelReleaseIdentity` — a recorded **external** value, not an AI-OS stable logical ID | *the originator's release identity, as the originator versions it* | n/a — §3.2 | The originator, **recorded** by AI-OS; never authoritative for an internal object |
| 4 | Model Profile | `ModelProfileRef` | **`model.<stable_snake_case_name>`** | Yes (Registry Profile Version) | Git (C1) |
| 5 | Router | `RouterRef` | `router.<name>` | Yes | Git (C1) |
| 6 | Orchestrator | `OrchestratorRef` | `orchestrator.<name>` | Yes (policy version) | Git (C1) |
| 7 | Workflow | `WorkflowRef` | `workflow.<name>` | Yes | Git (C1) |
| 8 | Workflow Run | `WorkflowRunRef` | `run.<uuid>` | No — a run is an instance | DB (C10) |
| 9 | Task | `TaskRef` | `task.<name>` | Yes (within its Workflow version) | Git (C1) |
| 10 | Handoff | `HandoffRef` | `handoff.<uuid>` | No | DB (C10) |
| 11 | Review Profile | `ReviewProfileRef` | `review.<name>` | Yes | Git (C1) |
| 12 | Review Instance | `ReviewInstanceRef` | `review_instance.<uuid>` | No | DB (C10) |
| 13 | Decision Right | `DecisionRightRef` | `decision.<name>` | Yes | Git (C1) |
| 14 | Decision Record | `DecisionRecordRef` | `decision_record.<uuid>` | No — append-only, never amended | DB (C10) |
| 15 | Knowledge | `KnowledgeRef` | `knowledge.<uuid>` | Yes (item version) | DB (C10) |
| 16 | Canonical Record | `CanonicalRecordRef` | `canonical.<uuid>` | Yes | DB (C10) |
| 17 | Artifact | `ArtifactRef` | `artifact.<uuid>` | Yes | DB (C10) |
| 18 | Storage Record | `StorageRecordRef` | `storage_record.<uuid>` | Yes (object version) | DB (C10) → bytes in C11 |
| 19 | Runtime Event | `RuntimeEventRef` | `runtime_event.<uuid>` | No | Observability plane (C13) |
| 20 | Credential | `CredentialRef` | `credential.<uuid>` | Yes (rotation generation) | C14 |
| 21 | Human Authority | `HumanAuthorityRef` | `human.<uuid>` | No | C14 |

### 3.1 Identities beyond the chain

The chain names the twenty-one objects whose collapse is a governance failure. The
implementation also carries these, each with its own non-substitutable type:

| Identity | Reference type | Versioned? | Notes |
|---|---|---|---|
| Skill | `SkillRef` (`skill.<name>`) | Yes | Bound to assignments; confers no authority |
| Work Item | `WorkItemRef` (`work_item.<uuid>`) | No | `TASK != WORK ITEM`: definition vs unit of assignment |
| Assignment | `AssignmentRef` (`assignment.<uuid>`) | No | Carries an attempt ordinal |
| Gate Requirement | `GateRequirementRef` (`gate.<name>`) | Yes | Declared in a Workflow Definition |
| Gate Instance | `GateInstanceRef` (`gate_instance.<uuid>`) | No | The run's instance of a requirement |
| Routing Request | `RoutingRequestRef` (`routing_request.<uuid>`) | No | |
| Routing Decision | `RoutingDecisionRef` (`routing_decision.<uuid>`) | No | Append-only; a correction is a new linked record |
| Model Invocation | `ModelInvocationRef` (`model_invocation.<uuid>`) | No | |
| Model Result | `ModelResultRef` (`model_result.<uuid>`) | No | |
| Model Family | `ModelFamilyRef` (`family.<stable_name>`) | No | Layer 1 of the Phase 9 stack; grouping and diversity constraints |
| Provider Profile | `ProviderRef` (`provider.<stable_snake_case_name>`) | Yes | Holds the layer-5 mappings |
| Deployment Profile | `DeploymentRef` (`deployment.<stable_snake_case_name>`) | Yes | Layer 6 |
| Provider Offering Mapping | `OfferingMappingRef` (`offering.<...>`) | Yes (mapping version) | **A bounded mapping held inside the Provider Profile, not a separate registry object** — no lifecycle, no capability claims, no governance properties of its own |
| Routing Policy | `RoutingPolicyRef` (`routing_policy.<name>`) | Yes | |
| Scope Node | `ScopeNodeRef` (`scope_node.<uuid>`) | No | Path identity is separate — see `scope-and-context-model.md` |
| Human Work Record | `HumanWorkRecordRef` | No | Gate evidence |
| Prerequisite Record | `PrerequisiteRecordRef` | No | Gate evidence |
| Human Intervention | `InterventionRef` (`intervention.<uuid>`) | No | |
| Scope Transfer | `ScopeTransferRef` (`scope_transfer.<uuid>`) | No | |
| Audit Event | `AuditEventRef` (`audit_event.<uuid>`) | No | |
| Provenance Record | `ProvenanceRef` (`provenance.<uuid>`) | No | |
| Execution Event | `ExecutionEventRef` (`execution_event.<uuid>`) | No | Coordination history, **not governance evidence** |
| Approval State Record | `ApprovalStateRef` (`approval.<uuid>`) | Yes | See `approval-state-registry.md` |
| Rework Loop Instance | `ReworkLoopRef` (`rework_loop.<uuid>`) | No | |
| Compensation Request | `CompensationRef` (`compensation.<uuid>`) | No | |

### 3.2 The Phase 9 model identity stack, used exactly as approved

The approved Phase 9 stack (`models/model-lifecycle-and-versioning.md` §0) has **six layers, no
overlap**. This specification uses its identities verbatim. An earlier revision of this document
invented a `model_profile.<name>` prefix and separately allocated `model.<name>` to a
`ModelRef`. Both were wrong and both are corrected here: **where this specification and the
approved architecture differ, the architecture wins.**

| # | Layer | Is | Identified by | In this specification |
|---:|---|---|---|---|
| 1 | **Model Family** | A lineage, for grouping and diversity constraints | `family.<stable_name>` | `ModelFamilyRef` |
| 2 | **Underlying Model Release** | The thing whose behaviour is profiled — **the thing that actually ran** | The originator's release identity, **recorded, never used as the registry ID** | `ModelReleaseIdentity`, a recorded external value (identifier kind 5) |
| 3 | **Model Profile** | The AI-OS governed record describing **one underlying model release** | `model.<stable_snake_case_name>` | `ModelProfileRef` |
| 4 | **Registry Profile Version** | The version of the **AI-OS record**, not of the model | `v<n>` on the profile | `model_profile_registry_version` |
| 5 | **Provider Offering Mapping** | A provider's exposure of that release — catalogue name, aliases, provider-specific behaviour | A bounded mapping **inside the Provider Profile** | `OfferingMappingRef` + mapping version |
| 6 | **Deployment Profile** | The concrete target: class, tenant, region, residency, supported handling labels, effective posture | `deployment.<stable_snake_case_name>` | `DeploymentRef` |

**Rule I-4 — `MODEL != MODEL PROFILE`, enforced by kind, not by prefix.** The chain's `MODEL` is
layer 2, the Underlying Model Release. It is an **external** identity: recorded as a value,
never an AI-OS stable logical ID, never a registry reference, and never authoritative for an
internal object. The Model Profile is layer 3, a governed registry object identified by
`model.<stable_snake_case_name>`. The two are not merely differently named — they are different
*kinds* of thing, one external and recorded, one internal and governed, and no column holds
both.

**Rule I-5 — there is no independent stable `ModelRef`.** Phase 9 defines none, so this
specification defines none. A field that says *which model ran* carries
`originator_release_identity` as a recorded value; a field that says *which governed record
described it* carries `model_profile_ref` + `model_profile_registry_version`.

**Rule I-6 — the registry profile version is not the underlying model version.** The record may
be revised while the model is unchanged, and the model may change while the record has not
caught up. A Routing Decision preserves **both**, and either alone under-determines what ran.

**Rule I-7 — a provider marketing alias never defines identity.** Aliases are metadata; identity
is the stable internal ID; **no constraint is ever expressed against an alias.**

**Rule I-8 — the offering mapping is not a registry object.** It has no independent lifecycle
and no source of truth of its own. It is versioned and referenced by a Routing Decision because
Phase 9 requires the exposure used to be reconstructable — but it is held inside the Provider
Profile, and giving it a registry of its own would create a seventh layer the approved stack
does not have.

**Rule I-9 — a materially changed release is a new Model Profile identity, never a version
increment.** A Registry Profile Version may change only the governed record **about the same
underlying release**; where sameness cannot be proven the result is a new identity or a recorded
identity conflict.

## 4. Non-substitutability — the enforcement rules

**Rule N-1 — Type-carried kind.** A reference is a value carrying both a kind and an id. Two
references of different kinds are never equal, even when the id strings are identical.

**Rule N-2 — No subclass slack.** A required reference type is matched **exactly**. A subtype,
a wrapper, a structurally identical object and a string are each refused. This is not pedantry:
substitution through a subtype is the ordinary way an identity boundary is crossed without
anyone editing the check.

**Rule N-3 — No coercion.** A string is never parsed into a reference at a governed boundary. A
caller that supplies `"human.42"` where a `HumanAuthorityRef` is required is refused; it is not
helpfully converted.

**Rule N-4 — No structural typing.** An object bearing the right field names is not the right
object. Duck typing is refused at every governed boundary.

**Rule N-5 — Persisted kind.** Every stored reference persists its kind alongside its id, so a
reference cannot change identity class by being read into a different column. Storage-level
enforcement is specified in `persistence-and-transaction-model.md` §5.

**Rule N-6 — Uniform prefix.** The stable logical ID's prefix **is** the kind. A row whose
`ref_kind` column and `ref_id` prefix disagree is rejected by a check constraint.

### 4.1 What an ID may not contain

Carried from Phase 7 §1 and Phase 5's workflow ID rules, and applied to every stable logical ID:
a human name; an organisation, client or project name; a provider or model vendor; an
implementation technology; a version number; a transient job title; an environment name.

Renaming a display name never changes an ID. Retiring an object **tombstones** its ID; the ID is
never reused for a different object.

## 5. The ten denials, as enforceable statements

| # | Denial | Enforcement point |
|---:|---|---|
| 1 | `ROLE != AGENT INSTANCE` | Distinct reference types; an Assignment has separate `role` and `agent_instance` columns with distinct kind constraints; a Role has a registry version, an Agent Instance has none |
| 2 | `MODEL != ROLE` | Distinct types; a Role Card may not name a model, only capability requirements or a `routing_policy.<id>`; a Routing Decision may not name a Role as its selection |
| 3 | `ROUTER != ORCHESTRATOR` | Component boundary F1/F2; a Routing Decision's `decided_by` is a `RouterRef` and a check constraint refuses an `OrchestratorRef` |
| 4 | `REVIEW PROFILE != REVIEW INSTANCE` | Distinct types; a Review Request references a Profile, a Review Instance references both and is produced only by C5 |
| 5 | `DECISION RIGHT != DECISION RECORD` | Distinct types; a gate is satisfied by a Record, never by the existence of a Right |
| 6 | `KNOWLEDGE != CANONICAL RECORD` | Distinct tables; promotion is a governed act producing a new Canonical Record version, never an update to a knowledge row |
| 7 | `ARTIFACT != STORAGE RECORD` | Distinct tables; artifact identity is never a path; a storage record carries location and object version |
| 8 | `RUNTIME EVENT != AUDIT EVENT` | Different stores, different components (C13 vs C12), different schemas; no governed read path reaches C13 |
| 9 | `CREDENTIAL != HUMAN AUTHORITY` | Distinct types; a Decision Record's `decided_by` column accepts only `human.*` and a check constraint refuses `credential.*`, `agent_instance.*` and service identities |
| 10 | **Authority is never inferred** | No column anywhere derives a Decision Record from a timeout, an expiry, a retry count, a confidence value, a rank, an RLS outcome, a role membership or a successful execution |

## 6. Reference integrity rules

**Rule R-1 — Resolvable or declared.** Every governed reference in a persisted record either
resolves in its source of truth at the stated version, or is explicitly declared
`FUTURE_GOVERNANCE_REFERENCE` and is therefore **non-executable**. A dangling reference is a
`BLOCK` at intake, per Phase 11 §5 check 7.

**Rule R-2 — Version pinning at write.** The version identity recorded is the one in force when
the record was written. Re-resolution at read time is prohibited.

**Rule R-3 — Tombstones resolve.** A retired stable logical ID still resolves, to a tombstone
carrying its retirement reason and date. Historical records stay readable.

**Rule R-4 — No identity merge.** Two objects whose names match are not thereby the same object.
`IDENTITY_CONFLICT` (Phase 8) is raised, never auto-resolved. This is the quietest and most
damaging conflict class and it has no automatic resolution path anywhere in this specification.

## 7. Divergences from the Phase 12 reference implementation

| # | Phase 12 reference | This specification | Why |
|---:|---|---|---|
| D1 | `SEPARATION_CHAIN` of 21 types with `id: str` only | The same 21 objects, with the version rule of §4.1 applied per category | Phase 10 §7 recorded-value rule; the MVP carries no versions |
| D5 | `ModelRef` with `KIND = "model"` alongside `ModelProfileRef` with `KIND = "model_profile"` | No independent `ModelRef`; the Model Profile takes Phase 9's `model.<...>` identity and the release is a recorded external value | Phase 9 §0 layers 2–3. The reference implementation allocated the `model` prefix to the wrong layer; the architecture wins |
| D2 | `ScopeRef` is a flat opaque id | Scope carries node identity **and** canonical path | Phase 8; Phase 13 finding M-5 |
| D3 | No Skill, Provider, Deployment, Offering Mapping, Routing Policy, Audit Event, Provenance, Approval State, Rework Loop or Compensation identity | All specified in §3.1 | Approved architecture requires each |
