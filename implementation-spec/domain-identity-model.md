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

**Rule I-1.** Every governed reference persisted anywhere is the pair *(stable logical ID,
version identity)* written as **recorded values**, never as a foreign key to a mutable row and
never re-resolved at read time. A historical record must reconstruct what it used, not what the
registry says today.

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
| 3 | Model | `ModelRef` | `model.<name>` | Yes | Git (C1) |
| 4 | Model Profile | `ModelProfileRef` | `model_profile.<name>` | Yes | Git (C1) |
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
| Provider Profile | `ProviderRef` (`provider.<name>`) | Yes | |
| Deployment Profile | `DeploymentRef` (`deployment.<name>`) | Yes | |
| Provider Offering Mapping | `OfferingMappingRef` (`offering.<name>`) | Yes | |
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
| 2 | `MODEL != ROLE` | Distinct types; a Role Card may not name a model; a Routing Decision may not name a Role as its selection |
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
| D1 | `SEPARATION_CHAIN` of 21 types with `id: str` only | Same 21 types, plus a required version identity on the 13 versioned kinds | Phase 10 §7 recorded-value rule; the MVP carries no versions |
| D2 | `ScopeRef` is a flat opaque id | Scope carries node identity **and** canonical path | Phase 8; Phase 13 finding M-5 |
| D3 | No Skill, Provider, Deployment, Offering Mapping, Routing Policy, Audit Event, Provenance, Approval State, Rework Loop or Compensation identity | All specified in §3.1 | Approved architecture requires each |
