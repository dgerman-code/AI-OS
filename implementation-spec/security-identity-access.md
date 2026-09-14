# Security, Identity and Access

Status: `PROPOSED` — Phase 14 implementation specification
Version: 0.1
Authority: approved Phase 1–13 architecture. Where this document and the approved architecture
differ, the architecture wins and this document is defective.

> **No secret, credential, key, IAM binding, policy document or identity-provider configuration
> is created by this document.** It specifies boundaries.

## 1. The governing statement

> **Enforcement is not authority. A credential is not a human. Access is not permission to
> decide.**

Access control answers *may this identity reach this resource*. Governance answers *may this act
be performed at all, and by whom*. The two are different questions, evaluated by different
components against different records, and an implementation that answers the second with the
first has replaced its governance model with its permission model.

## 2. Identity kinds — three, never merged

| Kind | Reference | Is | Is not |
|---|---|---|---|
| **Human authority identity** | `HumanAuthorityRef` (`human.<uuid>`) | A person who can hold eligibility for a Decision Right, be a reviewer, and intervene | An account, a session, a role name, or a job title |
| **Service identity** | `ServiceIdentityRef` (`service.<name>`) | A component acting as itself, always recorded, never authoritative | A human, a delegate, or an authority of any kind |
| **Agent instance identity** | `AgentInstanceRef` | One activation of a Role by a runtime | A Role, a person, or a standing persona |

**Rule X-1.** These three never share a column, a reference type, or a resolution path. Every
governed record that records an actor records **the human and the system separately**
(`audit-provenance-observability.md` §3 field 9).

**Rule X-2 — a human identity is stable and separable from its accounts.** A person may have
several accounts, several credentials and several sessions over time. The `HumanAuthorityRef`
survives all of them, because eligibility, separation of duties and historical Decision Records
are about the person, not the login. An implementation keyed on the account identifier loses
`DECISION_RIGHT_SEPARATION` the first time someone gets a new account.

**Rule X-3 — an agent instance is not a persona.** It has no memory across activations, no
standing, and no accumulated competence. `ROLE != AGENT INSTANCE` fails the moment an instance
outlives the work it was activated for.

## 3. Authentication, authorization, authority — three layers

| Layer | Question | Component | Output | Governance meaning |
|---|---|---|---|---|
| **Authentication** | Who is calling? | External IdP, projected by C14 | An identity reference | **None** |
| **Authorization** | May this identity reach this resource? | C14 + RLS | Allow / deny | **None** |
| **Authority** | May this act be performed, and by whom? | C6 against carded Decision Rights | Decision Record or refusal | **This is the only one** |

**Rule X-4.** Passing layers 1 and 2 gets a caller as far as *being able to make the request*.
Layer 3 is evaluated afterwards, against governed records, and it fails closed.

**Rule X-5.** No layer-2 artifact — a role membership, a group, an RLS policy, a grant, a
capability token — is ever consulted by layer 3. The holder-eligibility resolver reads the
Decision Right Card's declared eligibility classes and the human identity registry, and nothing
else.

## 4. RLS is enforcement, not authority

**Rule X-6.** Row Level Security is a **containment** mechanism: it reduces what a compromised
or mistaken caller can reach. It:

- **may** prevent a caller from reading rows outside their scope;
- **may** prevent a caller from writing to a domain they have no business in;
- **never** grants a Decision Right;
- **never** satisfies a gate;
- **never** substitutes for holder eligibility;
- **never** appears in a Decision Record's basis.

**Rule X-7 — RLS failing open is a defect, RLS passing is not a success.** A policy that admits
a row proves only that reading was permitted. Nothing governed follows.

**Rule X-8 — scope isolation is enforced in two independent places.** RLS at the row level **and**
the scope-binding checks in the governed act (`scope-and-context-model.md`). Neither is trusted
to be the only one: RLS can be bypassed by an elevated role, and application logic can be
bypassed by a direct connection. The two together mean one failure is not a leak.

## 5. Scope and tenant isolation

**Rule X-9.** Every governed row carries `scope_path`. RLS predicates are written on the
**path-prefix-with-separator** test (`scope-and-context-model.md` Rule S-2), never on a plain
`LIKE 'prefix%'`, which admits `ORGANISATION/acme_holdings` into `ORGANISATION/acme`.

**Rule X-10 — the three top-level families are isolated by construction.** No policy grants a
subject in one top-level branch access to another. Cross-family access exists only through a
governed transfer, which produces new records in the receiving scope rather than a read across.

**Rule X-11 — sensitivity is a second, independent filter.** A caller cleared for a scope is not
thereby cleared for every label in it. `PERSONAL_DATA`, `PRIVILEGED`, `TRADE_SECRET`,
`SECURITY_SENSITIVE` and `THIRD_PARTY_RESTRICTED` each gate access independently of scope, and
`PRIVILEGED` additionally records every access because privilege can be lost by handling.

**Rule X-12 — residency constrains storage and processing location**, and is evaluated when
choosing a storage location, a deployment for a model invocation, and a backup destination. An
`UNASSESSED` residency satisfies none of them.

## 6. Credentials and secrets

| Object | Is | Lifecycle |
|---|---|---|
| **Secret** | A value that must not be disclosed | Rotated; versioned by generation |
| **Credential** | An identity's means of authenticating | Issued, rotated, revoked |

**Rule X-13 — `SECRET != CREDENTIAL`.** Collapsing them makes a rotated value and the identity
that uses it share a lifecycle, and revocation loses its meaning.

**Rule X-14 — `CREDENTIAL != HUMAN AUTHORITY`.** Possession of access is never permission to
decide. Denied in Phase 10 for storage and again in Phase 11 for execution, and enforced here by
a database check constraint: a `credential.*` or `service.*` reference in
`decision_record.decided_by` is rejected by the database, not merely by application code.

**Rule X-15 — the secret manager holds secrets only.** No governed record, no policy, no
approval state and no Decision Right lives in it. A system whose authority model is partly in a
secret store has an authority model nobody can audit.

**Rule X-16 — secrets never enter events, logs, traces, payloads or governed records.**
`RUNTIME EVENT != SECRET`.

## 7. Administrative capability, bounded

**Rule X-17 — an administrator's ability to perform an action is not authority to authorise
one.** This is the single most common real-world bypass, and it is closed in four places:

| # | Closure |
|---:|---|
| 1 | `decision_record.decided_by` accepts only `human.*` — an admin is a person and may hold eligibility **only if the Right's declared eligibility classes cover them**, evaluated the same as anyone |
| 2 | No command accepts a bypass parameter; there is no `force`, no `skip_checks`, no `as_admin` |
| 3 | Elevated database roles can write, but every write produces an audit event and the append-only grant verification detects the elevation — the capability is detectable and attributable, never invisible |
| 4 | `NO_APPLICABLE_DECISION_RIGHT` is not an authorization error and cannot be resolved by granting a permission (`api-command-contracts.md` Rule Q-11) |

**Rule X-18 — the honest limit.** A database owner can write rows. This specification does not
claim otherwise. It claims that doing so is **outside the governed write path**, produces a
detectable inconsistency (missing audit event, broken record version chain, violated
append-only grant), and is itself an act someone must answer for. An architecture that claimed
immutability it cannot produce would be worse than one that states the gap.

**Rule X-19 — break-glass is an act, not a mode.** Where an organisation needs emergency access,
it is exercised under `EMERGENCY_DECISION` class authority with its objective trigger, bounded
scope and **mandatory retrospective obligations**, and it is recorded as a Decision Record like
any other. There is no "emergency mode" flag that relaxes checks, because a flag that relaxes
checks is the control being optional.

## 8. Service-to-service

**Rule X-20.** Every inter-component call carries the calling **service identity** and the
originating `correlation_id`, and — where a human initiated the chain — the
`actor_human_identity` **as a distinct field that is never synthesised**. A service that cannot
name the human did not have one, and commands requiring one are refused rather than attributed.

**Rule X-21 — least privilege per component.** Each component holds only the grants its
responsibilities require:

| Component | May write | May read |
|---|---|---|
| C9 Orchestrator | `execution` domain, execution events (append-only) | Governed records it coordinates; **not** C13 |
| C5 Review | `review` domain | Its requests and the reviewed artifact versions |
| C6 Decision Authority | `decision` domain | Rights, holders, separations, gate instances |
| C7 Router | `routing` domain | Registry projection, scope bindings |
| C4 Knowledge | `knowledge` domain | Its own; Decision Records for promotion preconditions |
| C12 Audit | `audit` domain (insert only) | Nothing governed |
| C13 Observability | Its own store | Nothing governed |
| C16 Outbox worker | Outbox and execution records | Intent and authorisation records |

**Rule X-22 — no component holds a grant that would let it perform another's governed act.** The
forbidden crossings in `system-component-model.md` §3 are enforced by grants as well as by code.

## 9. Data protection posture

**Rule X-23.** `PERSONAL_DATA` carries obligations independent of every other classification.
Purpose limitation, retention, subject rights and lawful basis are organisational obligations
AI-OS records and respects; AI-OS does not decide them. Where a lawful basis is required, it is a
Decision Right exercise recorded like any other, and its absence blocks.

**Rule X-24.** `PRIVILEGED` material can lose privilege by handling. Every access is recorded;
every transfer, routing request and artifact carries the label; and a routing candidate whose
Deployment Profile does not satisfy the handling constraint is **ineligible**, not merely
disfavoured.

## 10. What is deliberately not specified here

| Not specified | Why |
|---|---|
| An identity provider, protocol or product | Vendor independence; C14 projects whatever the organisation uses |
| A secret-manager product | Same |
| Concrete RLS policy text | It follows from §5 and the schema; writing it is implementation |
| An organisational role hierarchy | AI-OS does not own org charts, and separation is never inferred from one |
| A conflict-of-interest taxonomy | Would be inventing governance no approved phase authorised (see `decision-review-authority-model.md` §6.4) |
| Key lengths, algorithms, cipher suites | Implementation-level security engineering, reviewed under its own Review Profile |
