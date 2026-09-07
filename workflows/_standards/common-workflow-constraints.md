# Common Workflow Constraints

Status: PROPOSED — Phase 5 standard candidate
Standard ID: `standard.workflow.common_constraints`
Version: 0.1

Every Workflow Card inherits this document by reference and does not repeat it. Where a Workflow Card contradicts this standard, this standard governs and the card is defective.

## Purpose

These are the enforceable architecture rules that keep a coordination pattern from becoming authority. They are written so that a violation is detectable by reading the card, not only by watching an execution.

---

## 1. Workflow coordination grants no professional authority

Participation in a Workflow — in any participation type, including `LEAD_ROLE` — grants a Role nothing beyond its own Role Card. A Workflow cannot enlarge scope, transfer a conclusion, create a methodology entitlement or make a Role competent in a domain its card excludes.

Detection: a stage in which a Role contributes something its Role Card's *Does Not Own* clause excludes.

## 2. Role Card authority always outranks Workflow prose

Where a Workflow describes a Role doing something its Role Card does not permit, the Role Card governs. The Workflow is wrong and must be corrected — never the reverse, and never by amending the Role Card to fit the Workflow.

This is the same precedence rule Phase 4 applies to Skill Cards, extended to coordination.

## 3. Phase 4 Role-to-Skill compatibility cannot be widened by Workflow

A Workflow may reference a Skill, Specialisation or Pack for a Role **only** where the approved Phase 4 mapping records already establish compatibility, directly or through the Transitive Pack Compatibility Rule.

A Workflow that appears to require an incompatible activation has found a Phase 4 mapping question. It is raised as a finding against the mapping records. It is never resolved inside the Workflow Card, and a Workflow Card is never evidence of compatibility.

## 4. Workflow stage completion is not human approval

Satisfying a stage's exit criteria means the stage's exit criteria are satisfied. It does not mean the work is approved, accepted, signed off, endorsed or relied upon. No stage outcome — including `COMPLETE` — is an approval.

Language that implies otherwise ("the plan is approved at the end of Stage 4") is prohibited in card prose.

## 5. Workflow cannot create or satisfy independent review identity

A Workflow may state that a review is required and reference a `review.<id>`. It may not:

- define who is independent;
- define the review's scope, method, materiality or severity criteria;
- name a participating Role as the reviewer of work that Role or its stage produced;
- treat a stage's own quality control as satisfying an independent review requirement.

Self-review by a stage is not review. The Review Profile Registry is a later phase and owns all of the above.

## 6. Workflow cannot self-promote knowledge states

A Workflow may require a knowledge state as an entry or exit condition. It may not promote one. The transitions `DRAFT -> REVIEWED -> APPROVED -> CANONICAL` occur only under the governed human or review rule that permits them, and the promotion is attributable to that rule.

A stage exit criterion may read "the demand study is `REVIEWED`". It may not read "on exit, the demand study becomes `REVIEWED`".

## 7. AI output remains AI_SUGGESTION / DRAFT until a governed transition

Content produced by an AI-assumed Role enters as `AI_SUGGESTION` or `DRAFT`. Workflow progression does not change that. There is no stage, no number of stages and no accumulation of contributions that converts AI output into `APPROVED` or `CANONICAL` without the governed transition that rule 6 describes.

`FACT`, `ASSUMPTION` and `CALCULATION` must remain separable in every artifact a Workflow advances; a Workflow may not collapse them into undifferentiated narrative.

## 8. Human gates on transmitting acts are preserved

**Every external or costly-to-reverse transmitting act must preserve the applicable human-gate reference where one exists.** Where a Role Card marks an artifact with a `Transmitting Act` and a `Decision Right Reference`, any Workflow that reaches that transmission carries the same `HUMAN_GATE_REFERENCE`. Submission, filing, publication, release, external reliance and binding communication are all transmitting acts.

A Workflow may not reach a transmitting act by a path that has no gate on it.

## 9. Exceptions must not silently bypass a gate

An `EXCEPTION_PATH` may reroute, escalate, block or terminate. It may not route around a `HUMAN_GATE_REFERENCE` or a `REVIEW_REQUIRED_REFERENCE` that the normal path carries.

Where urgency is genuine, the exception path names the *emergency* decision right that governs it — an emergency gate is still a gate — and records what was bypassed, by whom and on what authority. "Expedited" is not an authority.

## 10. Rework loops must preserve provenance and prior state history

A `REWORK_LOOP` returns to an earlier stage. It does not erase what happened. The prior artifact versions, their knowledge states, the evidence links, the open items and the reason for rework are preserved and remain traceable.

Rework must not be usable as a way to make an inconvenient prior state disappear.

## 11. Cancellation does not delete evidence or audit history

`CANCELLED` stops a Workflow instance. It does not delete artifacts, evidence, provenance, gate records or the history of what was decided and when. A cancelled instance remains auditable, and any artifact that reached a governed state keeps it.

## 12. Workflow version change must not silently alter authority or Role scope

A new Workflow version may refine sequence, wording, criteria and depth. Where a version changes participating Roles, participation types, gate references, review references, artifact contributions or authority language, the change is stated explicitly in the card's change record and is treated as a governance change requiring the same scrutiny as a new Workflow.

Silent authority drift across versions is the slowest and least visible way this architecture can fail.

## 13. A Workflow may narrow applicability but cannot widen it

A Workflow may state that it applies only in a narrower context than a Role or Skill otherwise permits — fewer Roles, tighter triggers, stricter states. It cannot widen: it cannot make a Role applicable where its card excludes it, cannot make a Skill compatible where Phase 4 does not, and cannot relax an evidence, review or gate requirement that a Role Card or the criticality policy imposes.

Narrowing is a coordination choice. Widening is an authority change, and coordination has none.

## 14. Runtime must validate against the registry, not mutate it

A later orchestrator, scheduler or agent runtime validates its behaviour against this registry. It does not redefine registry semantics to fit an execution model. Where a runtime cannot express a registry rule, that is a runtime limitation to be reported — not a licence to weaken the rule.

No Workflow Card names a model, provider, framework, queue, database or deployment target.

---

## 15. Role-vs-Workflow escalation test

A candidate Workflow is actually a Role in disguise if it:

- accumulates methodology that is not traceable to a participating Role Card;
- produces a conclusion that no participating Role owns;
- needs an "approver" that is not an existing `decision.<id>`;
- needs a "reviewer" that is not an existing or planned `review.<id>`;
- would need to be assigned to a person as a job rather than run across people.

Any of these is a finding against the Role Registry or the Decision Rights Register, raised there. It is never resolved by letting the Workflow keep the capability.

## 16. Granularity rule

Create a Workflow only where it represents a **reusable coordination pattern across multiple activities and stages**, involving more than one Role or more than one governed state transition.

Do not create a Workflow for:

- a single skill invocation;
- a single document section or heading;
- a one-off approval click;
- a trivial two-step action with no branch, gate or rework path;
- a variation that differs from an existing Workflow only in depth (use criticality conditioning);
- an organisation-specific procedure (that is an SOP, referenced by a Workflow).

## 17. Status discipline

All Phase 5 artifacts are `PROPOSED`. Inclusion in the Master Workflow Universe confers no approval. No Workflow Card may set its own status to `APPROVED` or `CANONICAL`; those states are reached only through a governed human decision recorded outside the card.
