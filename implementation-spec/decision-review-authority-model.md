# Decision, Review and Authority Model

Status: `PROPOSED` — Phase 14 implementation specification
Version: 0.1
Authority: approved Phase 1–13 architecture. Where this document and the approved architecture
differ, the architecture wins and this document is defective.

Closes Phase 13 finding **M-4**.

## 1. The two separations this document exists to keep

> **`DECISION RIGHT != DECISION RECORD`** — the Right is a **type**: this class of decision
> exists, this is who may make it, this is what making it does. The Record is an **instance**:
> this decision was made, on this subject, by this holder, on this basis. Confusing them
> produces the most common governance failure in practice — a registry entry treated as though
> its existence were the decision.

> **`REVIEW != APPROVAL`** — a review may **find**, and may not **approve**. `REVIEWED` means a
> stated methodology was applied and its findings recorded. It does not mean true, and it does
> not satisfy a decision gate.

## 2. Decision Right — the definition record

A Decision Right is served from Git (C1) at a named registry version. It is never created,
widened or inferred by the runtime.

| Field | Type | Null | Mut | Notes |
|---|---|---|---|---|
| `decision_right_ref` | `DecisionRightRef` | NO | IMM | `decision.<name>`; may not contain a human name, organisation, client, project, provider, model, technology, version number or job title |
| `registry_version` | version id | NO | IMM | |
| `decision_class` | enum §2.1 | NO | IMM | **Exactly one** primary class |
| `decision_subject` | bounded text | NO | IMM | A Right whose subject is "the project" is **not bounded and is defective** |
| `decision_effect` | structured, per outcome | NO | IMM | §2.2 |
| `permitted_outcomes` | subset of §2.2 | NO | IMM | No Right must permit all six |
| `holder_eligibility` | set of eligibility classes | NO | IMM | Classes, never named humans |
| `cardinality` | enum §3 | NO | IMM | |
| `delegation` | structured | NO | IMM | Whether permitted, within what eligibility, and whether re-delegation is allowed |
| `prerequisites` | structured | YES | IMM | Required review states, evidence, upstream decisions |
| `separation_relationships` | list §6 | YES | IMM | `DECISION_RIGHT_SEPARATION` rows |
| `expiry_or_re_decision` | structured | YES | IMM | |

### 2.1 Decision classes — eight, and `decision.approve_anything` is not admitted

`PROGRESSION_DECISION` · `APPROVAL_DECISION` · `COMMITMENT_DECISION` ·
`RISK_ACCEPTANCE_DECISION` · `EXCEPTION_DECISION` · `EMERGENCY_DECISION` ·
`REJECTION_DECISION` · `CANCELLATION_OR_TERMINATION_DECISION`

A Right declares exactly one primary class. Where outcomes span classes — a progression Right
whose `REJECT` routes to termination — the secondary effect is declared **in the effect table**,
never by claiming two classes.

### 2.2 Outcomes — six, each with a declared effect

| Outcome | Meaning |
|---|---|
| `APPROVE` | The decision is made positively as scoped |
| `REJECT` | Refused |
| `APPROVE_WITH_CONDITIONS` | Positive, subject to conditions that **remain open and carried** |
| `DEFER` | No decision made; the gate remains unsatisfied |
| `ESCALATE` | Referred to a higher or different authority; no decision made here |
| `CANCEL` | The governed path is stopped |

For each permitted outcome the card declares the effect on: workflow progression; handoff
eligibility; external action or commitment; review status; knowledge state; whether conditions
and open items remain active; and whether expiry or re-decision is required. **A Right that
permits an outcome without stating its effect is defective** and is rejected by the definition
validator at load.

### 2.3 The five mandatory boundaries, as enforcement

| # | Boundary | Enforcement |
|---:|---|---|
| 1 | A Right may permit progression while a review stands `NOT_SATISFIED` — **it must not relabel the review `SATISFIED`** | No command writes a Review Instance outcome from C6. The gate records exceptional progression with element 11 of the Decision Record, and the Review Instance is untouched |
| 2 | A Right may accept risk. **It does not erase the risk or the finding** | The risk and finding records are `APP`; acceptance adds a link, never a delete or an update |
| 3 | A Right may approve an artifact for a bounded use. **It does not make the artifact `CANONICAL`** | Promotion requires precondition 9 of `knowledge-and-canonical-model.md` §7.1 — a separate mapped Right |
| 4 | A Right **cannot create professional conclusions** outside upstream Role ownership | A Decision Record has no `conclusion` field; it references the Role-owned artifact it decides about |
| 5 | A Right **does not rewrite source facts, assumptions, findings, `UNKNOWN` or `CONFLICT_DETECTED` states** | Those columns are `IMM`/`APP` and no C6 command targets them |

## 3. Cardinality

| Cardinality | Satisfied when |
|---|---|
| `SINGLE_HOLDER` | One eligible holder decided positively |
| `MULTI_HOLDER_ALL_REQUIRED` | Every named eligibility class decided positively |
| `MULTI_HOLDER_THRESHOLD` | The declared threshold of eligible holders decided positively |
| `GOVERNANCE_BODY_DECISION` | A constituted body decided as a body under its own constituting rules |

**Rule A-1.** Cardinality governs separation **inside one decision**. It says nothing about the
same human taking two different decisions along a chain — that is §6.

## 4. Decision Record — the evidence of exercise

Append-only, **never amended**. A correction is a new record that links to the prior one.

The 19-element evidence model, carried in full:

| # | Element | Null | Notes |
|---:|---|---|---|
| 1 | `decision_record_ref` | NO | `decision_record.<uuid>` |
| 2 | `decision_right_ref` + `registry_version` | NO | Recorded values |
| 3 | `decided_by` — `HumanAuthorityRef` | NO | **Check constraint: kind must be `human`.** A credential, service identity, agent instance, role or orchestrator reference is rejected at the database, not only in code |
| 4 | `holder_eligibility_basis` | NO | Which eligibility class, and how it was established |
| 5 | `governed_subject` | NO | The bounded subject actually decided about |
| 6 | `scope_path` | NO | |
| 7 | `outcome` | NO | One of §2.2 |
| 8 | `decided_at` | NO | |
| 9 | `basis` | NO | What the decision relied on, as ref+version values |
| 10 | `conditions` | YES | Required when outcome is `APPROVE_WITH_CONDITIONS`; carried open |
| 11 | `review_state_at_decision` | NO | The review states in force — **the element that makes exceptional progression auditable** |
| 12 | `evidence_refs` | NO | Recorded values |
| 13 | `work_item_ref` / `gate_instance_ref` | YES | Where the decision answers a gate |
| 14 | `cardinality_satisfaction` | NO | Which holders, which classes, threshold met |
| 15 | `expiry_or_review_date` | YES | |
| 16 | `supersedes` / `superseded_by` | YES | Append-only linkage |
| 17 | `dissent_or_abstention` | YES | Where collective authority uses it |
| 18 | `emergency_basis` + `retrospective_obligations` | YES | Required when the class is `EMERGENCY_DECISION` |
| 19 | `separation_compliance` | NO | Which `DECISION_RIGHT_SEPARATION` relationships were active, and that this holder was not the separated decision's holder |

Constraints: `UNIQUE (decision_record_ref)`; no `UPDATE` permitted on any column except the
append-only linkage in element 16; check that element 18 is present iff the class is
`EMERGENCY_DECISION`; check that element 10 is present iff the outcome is
`APPROVE_WITH_CONDITIONS`.

## 5. Review — profiles, instances and independence

### 5.1 Independence classes

| Class | Independence | Satisfies an independent-review requirement? |
|---|---|---|
| `PRODUCER_REVIEW` | **None** — the producing Role checking its own work | **Never** |
| `PEER_REVIEW` | Assignment-level — a different Role instance in the same or similar domain that did not produce the artifact | Where the requirement asks for peer level |
| `CROSS_DOMAIN_REVIEW` | Domain-level — a reviewer from a different Role or domain checking interfaces, consistency, assumptions, dependencies | **Does not substitute for domain review**; it cannot conclude on the domain it checks across |
| `INDEPENDENT_ASSURANCE_REVIEW` | Heightened — full separation from the producing assignment **and from the delivery line** | Yes; required for decision-grade and high-criticality work |

`PRODUCER_REVIEW` is in the vocabulary precisely so internal QC has a name, can be recorded, and
can therefore be recognised as **not** the thing an independent requirement asks for.

### 5.2 Reviewer eligibility classes

| Class | May satisfy |
|---|---|
| `FULL_PROFILE_REVIEWER_ELIGIBLE` | The whole Profile, alone |
| `BOUNDED_REVIEW_CONTRIBUTOR` | One dimension — a bounded `CROSS_DOMAIN_REVIEW`, an evidence or reconciliation check. **Cannot satisfy the whole Profile** |

**Rule A-2.** A Review Instance produced by a `BOUNDED_REVIEW_CONTRIBUTOR` never sets a gate to
`SATISFIED` for a Profile requiring full coverage. The gate remains unsatisfied and the
contribution is recorded as a contribution.

### 5.3 `review_instance`

| Field | Type | Null | Mut | Notes |
|---|---|---|---|---|
| `review_instance_ref` | `ReviewInstanceRef` | NO | IMM | |
| `review_profile_ref` + `registry_version` | ref pair | NO | IMM | |
| `review_request_ref` | ref | NO | IMM | The request this answers; validated by lookup |
| `run_ref`, `work_item_ref`, `gate_instance_ref` | refs | NO | IMM | Exact lineage |
| `reviewed_artifact` | ref+version | NO | IMM | The exact version reviewed |
| `reviewer_identity` | `HumanAuthorityRef` | NO | IMM | Check: kind must be `human` |
| `reviewer_role_ref` + version | ref pair | NO | IMM | |
| `independence_class` | enum §5.1 | NO | IMM | |
| `eligibility_class` | enum §5.2 | NO | IMM | |
| `outcome` | gate outcome | NO | IMM | |
| `findings` | append-only list | YES | APP | Never deleted, never silently resolved |
| `open_items` | append-only list | YES | APP | Carried where an upstream rule permits |
| `performed_at` | timestamp | NO | IMM | |

## 6. Segregation of duties at identity level — M-4

**This section is the substance of Phase 13 finding M-4.** An `independence_class` label is a
*declaration*. Segregation of duties is a *relationship between actual identities*, and it must
be evaluated, recorded and enforced as one.

### 6.1 The actor identities a governed act distinguishes

| Actor | Identity type | Where recorded |
|---|---|---|
| **Producer / author** | `HumanAuthorityRef` where a human produced it; `AgentInstanceRef` + `RoleRef` where automation did | `assignment`, `work_product` |
| **Review assignee** | `HumanAuthorityRef` + `RoleRef` | `review_request` |
| **Reviewer** | `HumanAuthorityRef` | `review_instance.reviewer_identity` |
| **Decision Right holder** (eligible) | Eligibility class → resolved `HumanAuthorityRef` set | C6 holder resolution |
| **Decision Record author** (the human who decided) | `HumanAuthorityRef` | `decision_record.decided_by` |
| **Delegate** | `HumanAuthorityRef`, linked to the delegating holder | `delegation` record |

**Rule A-3.** The producer, the reviewer and the Decision Record author are three separately
recorded identity columns. An implementation that derives any of them from another — "the
reviewer is whoever is logged in", "the decider is the workflow owner" — has made the SoD checks
unevaluable.

### 6.2 Producer-review prohibition

**Rule A-4.** Where a gate requires an independence class above `PRODUCER_REVIEW`, the review is
refused when:

1. `reviewer_identity` equals any producer identity recorded on the reviewed artifact version; or
2. `reviewer_identity` equals the assignee of the producing assignment; or
3. for `INDEPENDENT_ASSURANCE_REVIEW`, `reviewer_identity` is within the **delivery line** of the
   producing assignment, as declared by the review request's independence declaration.

Conditions 1 and 2 are machine-checkable from recorded identities and are enforced by the
implementation. Condition 3 depends on an organisational relationship AI-OS does not own; it is
**declared and evidenced** on the review request, and the absence of a declaration is a
`BLOCK`, not a pass. See `open-items-and-blocked-authorities.md` OI-4.

**Rule A-5.** A model producing the work and a different model reviewing it is **not**
independence. Diversity of models is not diversity of reviewers: the reviewer is the Role and
human accountability structure Phase 6 defines.

### 6.3 `DECISION_RIGHT_SEPARATION`

A relationship-level declaration made by a Decision Right Card about a **concrete other Right**
— never inferred from a job title, a Role identity, a reporting line or seniority.

Each row declares five things:

| Element | Content |
|---|---|
| Related Right | A concrete `decision.<id>` that exists in the registry. A category or description is not a relationship |
| Activation condition | **Objective and testable** — same change set, same governed subject, same unresolved item, same decision chain. Not "where appropriate" |
| Separation mode | `SEPARATION_REQUIRED` or `SAME_HOLDER_PERMITTED` |
| Bounded subject / context | A relationship that applies to everything is not bounded |
| Reason | Why separation is required, or why sharing a holder preserves the control purpose |

Normative rules, enforced by C6 before a Decision Record is written:

| # | Rule |
|---:|---|
| 1 | Where `SEPARATION_REQUIRED` is active, **the same human instance must not exercise both Rights for the same governed subject or context within the same decision chain** |
| 2 | Eligibility is evaluated **independently for each Right**. Being eligible for both is ordinary; it is not permission to exercise both |
| 3 | Holding two eligibility classes does not bypass separation |
| 4 | **Delegation does not bypass separation.** A delegate of the first Right is, for this purpose, the first holder |
| 5 | Within-Right cardinality does not satisfy cross-Right separation |
| 6 | Separation is never inferred from a job title, Role identity, reporting line or seniority |
| 7 | `SAME_HOLDER_PERMITTED` only where the card declares it explicitly with a defensible reason. **Silence is not permission and not prohibition**: an undeclared relationship creates no obligation, and its absence is not evidence that separation was considered |
| 8 | This model introduces **no staffing algorithm, assignment engine, rota or runtime scheduling** |
| 9 | **If no separately eligible second holder is available, the second Right is not validly exercisable in that context.** The gate is unsatisfied. Authority is not relaxed and scarcity is not an emergency |
| 10 | A Decision Record must **evidence compliance** with every applicable separation relationship (element 19) |

**Rule A-6 — the decision chain.** "The same decision chain" is implemented as an explicit
`decision_chain_id` propagated through the run and recorded on every Decision Record, not
inferred from timestamps or run proximity. Rule 1 is then a durable uniqueness question:
`UNIQUE (decision_chain_id, governed_subject, decided_by)` **must not** match across a separated
pair. Specified in `persistence-and-transaction-model.md` §5.4.

### 6.4 Conflict of interest / incompatible duties

**Rule A-7.** Two duties are incompatible when a declared `SEPARATION_REQUIRED` relationship is
active, or when Rule A-4 applies. AI-OS declares **no** further conflict-of-interest taxonomy:
inventing one would be creating governance that no approved phase authorised. Where an
organisation has its own incompatible-duty rules, they are expressed as additional
`DECISION_RIGHT_SEPARATION` rows on the cards through the Phase 7 change path — not as
configuration in the runtime. See `open-items-and-blocked-authorities.md` OI-5.

### 6.5 The criticality default

For decision-grade and high-criticality external-commitment chains, `SEPARATION_REQUIRED` is the
default between: risk acceptance and a final release/submission/publication/commitment Right on
the same unresolved risk; exceptional progression and the downstream final commitment on a
material unresolved item; and emergency exception authority and the ordinary ratification
authority that normalises it.

> The same human must not both accept the residual risk and authorise the release that carries
> it, where the separation relationship is active.

## 7. Gate satisfaction

```
HUMAN_GATE_REFERENCE  ->  decision.<id>  ->  Decision Record
```

A human gate is satisfied **only when all five hold**:

1. the referenced Decision Right exists at a resolvable registry version;
2. an eligible holder made the decision and the cardinality requirement is met;
3. the prerequisites the Right requires are met, **or** an allowed exceptional path is explicitly
   used and recorded;
4. every applicable `DECISION_RIGHT_SEPARATION` relationship is satisfied;
5. the Decision Record exists, is complete on all 19 elements, and names this gate instance.

**Rule A-8.** Gate satisfaction is evaluated against **records the system itself holds**, never
against an object supplied at call time. A caller may construct a plausible Decision Record; it
simply will not be found in the governed lineage, and so it satisfies nothing.

## 8. Missing-Right handling — fail closed

**Rule A-9.** Where no approved Decision Right covers an act:

- the outcome is `NO_APPLICABLE_DECISION_RIGHT`;
- the run goes `BLOCKED` **and** `ESCALATED`, posture `AUTHORITY_ABSENT`;
- the record states the act requested, the constraint class, **each Right considered and why it
  does not reach**, and the specific gap;
- the escalation goes to the Phase 7 carding governance path, **not to a senior person**.

Five things must not happen, and each is a named prohibition rather than an omission:

| # | Prohibition |
|---:|---|
| 1 | **The nearest Right is not stretched.** Widening a declared subject is the defect, not a workaround |
| 2 | **The absence is not read as permission.** An act nobody is authorised to perform is not an act everybody may perform |
| 3 | **No human is asked to "approve it anyway."** A human without a Right has no Right either; seniority is not authority |
| 4 | **It is not carried as an open item.** `AUTHORITY_ABSENT` permits no completion |
| 5 | **It is not retried.** A block is an unmet constraint, and no number of attempts produces a Right |

**Rule A-10 — no substitution.** None of the following ever stands in for a human Decision
Right: an admin role; an RLS bypass; a service account; a database owner; a model selection; a
reviewer; a workflow owner; the orchestrator; a system control profile; a configuration flag; an
environment variable; a feature toggle.

## 9. Divergences from the Phase 12 reference implementation

| # | Phase 12 reference | This specification | Why |
|---:|---|---|---|
| D1 | `independence_class` matched by exact string equality only | Identity-level SoD, §6 | Phase 6 §3; Phase 13 M-4 |
| D2 | No `DECISION_RIGHT_SEPARATION` evaluation | §6.3 with durable enforcement | Phase 7 §15A |
| D3 | Decision Record has a small field set | The full 19-element model | Phase 7 §8 |
| D4 | No delegation, cardinality beyond single holder, or emergency basis | §2, §3, element 18 | Phase 7 §5, §6 |
