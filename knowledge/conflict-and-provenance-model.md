# Conflict and Provenance Model

Status: PROPOSED — Phase 8 architecture candidate
Version: 0.1
Inherits: `standard.knowledge.common_constraints@0.1`

## Part I — Conflict

## 1. Conflict is a first-class object

A conflict is **not an error and not a defect**. It is a finding about the state of what the organisation holds, and an organisation whose register shows no conflicts has either a very small register or a resolution process that erases things.

A conflict is raised as a **flag on the items it concerns**, carries its own record, and is cleared **only by a recorded resolution**. Raising one requires no authority. Clearing one does.

## 2. Conflict taxonomy

| Class | What is in tension | Characteristic failure if untyped |
|---|---|---|
| `SOURCE_CONFLICT` | Two sources say different things | Treated as a claim dispute, so the sources are never compared on their own merits |
| `CLAIM_CONFLICT` | Two claims are incompatible, each with its own evidence | Resolved by picking an author rather than weighing evidence |
| `VERSION_CONFLICT` | Two versions of the same item are both in use | The older one keeps circulating in documents nobody re-checked |
| `SCOPE_CONFLICT` | Two scopes hold incompatible canonical statements on one subject **without a declared override** | Silently "resolved" by whichever scope the reader happens to be in |
| `TEMPORAL_CONFLICT` | Statements true at different times treated as competing | The newer one wins, discarding a correct historical position |
| `AUTHORITY_CONFLICT` | Two governed decisions point different ways | Escalated as a personality question rather than a decision-rights question |
| `IDENTITY_CONFLICT` | Is this the same entity, subject or claim at all? | Two things merged because their names matched — the most damaging and the quietest |

`IDENTITY_CONFLICT` is listed last and matters most: every other class assumes the two items are about the same subject. When that assumption is wrong, resolving the conflict merges two different things and destroys both.

## 3. Resolution rules

1. **Later is not automatically superior.** Recency is evidence about currency, not about correctness, and a newer source may simply be a worse one.
2. **Higher authority is not truer evidence.** A Decision Right may decide what the organisation does about a conflict. It cannot decide which source is accurate — that is a professional conclusion, owned by an eligible Role and checked by review.
3. **A resolution records why the prevailing interpretation prevailed** — on the evidence, in terms someone who disagrees can examine. "Resolved" with no reasoning is not a resolution.
4. **The losing evidence is retained**, linked to the resolution, readable afterwards. Resolution is a decision about what to rely on, never a deletion of what was set aside.
5. **Minority and dissenting evidence may remain attached** after resolution, and its continued presence is not a reopening of the conflict.
6. **An unresolved conflict that is material to a claim blocks that claim's canonical promotion and its decision-grade use.** A conflict is material where **the claim or the decision depends on the contested point**; a conflict about a figure the statement does not rest on stays visible and blocks nothing, at any criticality band.

   **Materiality is a determination, not an impression.** It is stated on the record, **attributable to a named eligible Role, and reviewable** — never inferred from retrieval ranking, model confidence, source count, or nobody having raised it. Criticality changes the tolerance and the burden, not the test: at Enhanced Decision-Grade every open conflict requires an explicit materiality assessment, and **an unassessed open conflict is treated as material until one is made.** That is a stronger default, not a different rule, and it does not make an irrelevant disagreement blocking.
7. **A conflict discovered after promotion does not un-promote anything.** The canonical record stays canonical **and visibly in conflict**; where material it becomes blocking for decision-grade use until resolved (`knowledge/sensitivity-and-retention-model.md` §3). Whether it is superseded or retracted is a governed decision taken on the resolution's findings.
8. **A conflict is never cleared by time, by re-assertion, by repetition across sources, by a model's agreement, or by nobody objecting.**

## 4. What a resolution record carries

The conflict class; the items and versions in tension; what each was based on; the evidence weighed; **what prevailed and why**; what was set aside and where it remains readable; any dissent retained; the consequent state changes; and the residual uncertainty that survives the resolution. The last is the one most often dropped: resolving which of two figures to use rarely means the other was baseless.

---

## Part II — Provenance

## 5. The required chain

```
SOURCE -> EVIDENCE -> CLAIM / CALCULATION / INFERENCE -> REVIEW -> DECISION (where required) -> CANONICAL VERSION
```

**Not every item traverses every step. Every omitted step must be explainable by item type and criticality band** — and the explanation is recorded in the item, not left to be reconstructed. An omitted step with no stated reason is a **provenance gap**, and a provenance gap is a defect.

## 6. Lineage types

| Lineage | What must be traceable |
|---|---|
| **Direct evidence** | The source, its version, and the location within it the evidence was taken from |
| **Derived evidence** | The evidence it derives from, plus the derivation and who performed it |
| **Calculation** | Every input at the **version relied on**, the method, and the parameters — enough that the value can be re-derived and shown to differ if an input changed |
| **Transformation** | Format, unit, currency, basis or aggregation changes — each one a step where a value silently becomes a different value |
| **Citation / reference** | What is cited, at what version, and whether the citation is load-bearing or contextual |
| **Human edit** | Who edited (runtime identity), what changed, and why — never an unattributed change |
| **AI-generated contribution** | The item's **origin** — `AI_GENERATED` or `AI_ASSISTED` — which part a model contributed, and, where this item was adopted from a proposal, the **link to that `AI_SUGGESTION` and the evidence or reasoning that justified this item's own type**. Origin is permanent: no act changes it, and the contribution is never anonymised into the human's authorship |
| **External source** | Publisher, date, accessed-at, version or edition, and whether the entity controls it — normally it does not |
| **Artifact linkage** | Which artifacts express this knowledge, and at which of their versions |

## 7. Provenance rules

1. **No silent provenance loss.** A step that cannot be shown is recorded as unknown, not omitted. An item whose lineage is partly unrecoverable says so — that is usable knowledge with a stated limitation, and it is not the same thing as an item that looks complete.
2. **Provenance survives every state transition, every version, every supersession, every retraction and every scope transfer.** It is the one property nothing removes.
3. **Provenance is not authorship.** Attribution of contribution is not attribution of responsibility, and neither is authority.
4. **Reformatting is a transformation.** So are unit conversion, rounding, currency conversion, re-basing and aggregation. Each is a lineage step, because each is a place where a number becomes a different number and the change is invisible in the result.
5. **A calculation binds its inputs by version.** When any bound input is superseded, the calculation's refresh trigger fires: it becomes stale, **not false**, and re-derivation — not re-approval — is what resolves it.
6. **AI contribution is always visible in the lineage**, however heavily edited afterwards. **Nothing in the lineage moves an item out of `AI_SUGGESTION`** — adoption is a new linked item with its own basis (`knowledge/knowledge-state-model.md` §2a), and the lineage records both it and the proposal.
7. **Citing an artifact is not citing evidence.** An artifact expresses claims; the evidence is what those claims rest on. A chain that stops at "the report says so" has stopped one step early, and the step it skipped is the one that mattered.

## 8. Criticality and provenance depth

Depth of required lineage rises with criticality; **the truth of the item does not change with it.** See `architecture/memory-canonical-governance.md` §9 for the band table.

## 9. Status

`PROPOSED`. Implements no storage, no graph, no lineage engine and no runtime.
