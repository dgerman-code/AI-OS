# Common Model Governance Constraints

Status: PROPOSED — Phase 9 standard candidate
Standard ID: `standard.model.common_constraints`
Version: 0.1

Every Phase 9 artifact inherits this document by reference and does not repeat it. Where anything in `models/` contradicts this standard, this standard governs and the contradicting artifact is defective.

## 1. A model is a replaceable execution capability
It is not a Role, not an agent instance, not a reviewer identity, and not a member of the organisation. Replacing it changes the registry and nothing above it.

## 2. A model holds no authority
No model, provider, deployment or automated process holds a Decision Right, by capability, by trust, or by being the thing that reached the gate. Phase 7 governs authority and Phase 9 adds nothing to it.

## 3. A Routing Decision is not a Decision Record
Selecting a tool approves no work, accepts no risk, satisfies no review, promotes no knowledge and creates no authority.

## 4. A Router is not an Orchestrator
The Router answers which execution capability is eligible and preferred for bounded work. What work happens, in what order, by which Role, and whether it is done, are not its questions.

## 5. Model, provider and deployment are three objects
One family may exist through several providers; one provider may expose many models; one model may be reachable at several deployments with different residency, sensitivity and retention properties. A statement about one is not a statement about another.

## 6. A capability claim is a claim
It carries evidence and confidence. It is never a guarantee of performance, never knowledge about the world, and never canonical.

## 7. Provider assertion is evidence of a provider assertion
Admissible; not proof. No quantity of it becomes internal evaluation evidence.

## 8. No benchmark score is authority
A score is evidence about a benchmark. Its relevance to the work is a separate claim requiring its own justification.

## 9. No composite score exists
Evaluation is dimension-specific. A single number must never become routing authority, and no ranking of models is expressible in this architecture.

## 10. Confidence does not create eligibility
It ranks within the eligible set. It never satisfies a constraint, never compensates for a failed one, and never applies to a capability it was not measured on.

## 11. `NOT_CLAIMED` is not `NOT_CAPABLE`
An unevaluated dimension is an absence of assertion. A known weakness is recorded as a limitation, never as a low claim.

## 12. A soft preference never overrides a hard constraint
Hard constraints filter; preferences rank what survives. No accumulation of preferences makes an ineligible candidate eligible.

## 13. Cost and latency never override governance
They never displace legality, confidentiality, residency, required capability, review independence or a criticality requirement. The cheapest eligible model is not automatically preferred, and the most expensive is not automatically best.

## 14. Lifecycle status is not task eligibility
`ELIGIBLE` means admitted to the registry. A globally eligible model may be prohibited for a specific task, and a `PREFERRED` model is not mandatory where policy disqualifies it.

## 15. There is no partial eligibility
A candidate satisfies every hard constraint or it is not a candidate. "Closest fit" and "fewest violations" are not concepts this architecture contains.

## 16. An unrecognised constraint blocks routing
It is never ignored. Ignoring a constraint silently grants everything it was written to prevent.

## 17. No silent degradation
A degraded fallback is declared as degraded, names the dimension on which it is weaker, and is recorded as such. Each fallback is assessed against the original requirements, never against the previous fallback.

## 18. Where nothing is eligible, routing blocks
`NO_ELIGIBLE_MODEL` and `BLOCKED_FOR_ROUTING` are correct outcomes. There is no "best available", and an outage is never a reason to relax a constraint.

## 19. Availability is not capability
An unavailable model has lost no claim; an available one has gained no competence. `UNKNOWN_AVAILABILITY` is never silently treated as `AVAILABLE` in high-criticality routing.

## 20. Reviewer independence is not model diversity
Phase 6 governs reviewer and Profile independence; Phase 9 governs model diversity. They are orthogonal, neither implies the other, and **Phase 9 adds no independence class and changes no review status**.

## 21. Different-provider review is never a default
Diversity requirements are tied to the risk in the work. Imposed reflexively they shrink the eligible set, often to one, which is the opposite of a diversity control.

## 22. A diversity constraint is evaluated against a named prior selection
Where the prior Routing Decision is unknown or unrecorded, the constraint is unsatisfiable and routing blocks. It is never treated as satisfied because nothing contradicts it.

## 23. Criticality raises rigour, not authority or truth
Higher bands require stronger evidence, freshness, reliability and independence. They grant the model nothing, make its output no truer, and do not mean "the largest model".

## 24. Human override cannot reach a mandatory constraint
No human makes an ineligible model eligible where law, privacy, security or contract forbids it; waives mandatory review independence without a valid upstream Decision Right; makes output true or canonical; or rewrites routing history.

## 25. Model output enters Phase 8 as `AI_SUGGESTION`
With `ORIGIN: AI_GENERATED`, permanently. No capability evidence, criticality band or provider approval shortens the governed path to any other state.

## 26. Routing changes nothing about knowledge
Not its canonicality, not its sensitivity classification, not its scope, not its visibility. Selecting a deployment never moves knowledge across a scope boundary.

## 27. Upper architecture names no vendor
Role Cards, Workflow stages and Review Profiles express capability requirements, routing policy references or diversity values — never a model, provider or product name.

## 28. Model pinning is exceptional and governed
It requires a recorded justification, a named owner, and an expiry or review-by. An unexpiring pin is lock-in acquired one task at a time.

## 29. A rename is an alias, never an identity change
Stable internal IDs do not move when a provider renames a product, and no routing constraint is ever expressed against an alias.

## 30. Routing history is preserved through everything
Deprecation, retirement, suspension, incident and provider disappearance leave historical Routing Decisions intact, naming the profile and version actually used. A correction is a new linked decision, never an edit.

## 31. Routing reproducibility only
Given the same requirements, registry state and policy version, the same candidate is selected. Model-output reproducibility and provider availability are not claimed and are not architecture's to promise.

## 32. Runtime validates against this registry; it does not mutate it
A later system may call providers, observe availability and record instances. It may not redefine what eligibility is, what a constraint means, or what a Routing Decision does.

---

## 33. Status discipline
All Phase 9 artifacts are `PROPOSED`. No Phase 9 artifact may set its own status to `APPROVED` or `CANONICAL`, no exemplar is a live profile or decision, and no provider or product is endorsed by appearing in one.
