# Communication Control Filter

Status: `PROPOSED`
Version: 0.1
Rubric Version: `filter.communication_control@0.1`
Governance Owner: AI-OS architecture governance
Compatibility alias (never canonical): `FISHER COMMUNICATION FILTER`

> **The filter is advisory and confers no authority.** A score is not a review, not an approval,
> not evidence, and not a gate. A draft may score well and still be blocked; a draft may score
> poorly and still be the right message.

## 1. What the filter is for

A final structured pass over a draft, before it goes to review, that asks ten questions in a fixed
order and records ten answers. Its value is that the answers are **recorded and reproducible**: a
reviewer can see which factor the producer thought was weak and what was done about it.

Its value is **not** that it produces a number. §6 states the ways the number must not be used,
and they are the ways numbers in systems like this usually get used.

## 2. The ten factors

Each is scored `0`–`10` against the rubric in §3.

| # | Factor | The question it asks |
|---:|---|---|
| 1 | **GOAL** | Is the desired outcome explicit, and does this draft serve it? |
| 2 | **EMOTION** | Is the wording deliberate rather than reactive? |
| 3 | **CLARITY** | Is the position immediately understandable on one reading? |
| 4 | **BREVITY** | Is there text whose removal would not weaken the message? |
| 5 | **BOUNDARY** | Where a boundary is needed, is it explicit and self-directed? |
| 6 | **DEFENSIVENESS** | Has unnecessary justification and rebuttal been removed? |
| 7 | **CONTROL** | Does the draft return the exchange to the issue that matters? |
| 8 | **RELEVANCE** | Are non-material accusations left unrewarded by attention? |
| 9 | **ESCALATION** | Does the tone add conflict the situation does not require? |
| 10 | **NEXT STEP** | Is the expected action, its owner and its timing clear where applicable? |

## 3. Scoring rubric

The same anchors apply to every factor, so that a `7` means the same thing in factor 2 as in
factor 9:

| Score | Anchor |
|---:|---|
| `0–2` | The factor is actively violated. The draft does the opposite of what the factor asks |
| `3–4` | The factor is mostly unmet; a reader would notice the problem |
| `5–6` | The factor is partially met; the weakness is visible but not damaging |
| `7–8` | The factor is met; a critical reader would not object |
| `9–10` | The factor is met and the draft is strong on it specifically |

**Rule CF-1 — a score requires a reason.** Every component score below `7` is recorded with the
specific text that caused it. A number with no reason is not reviewable and is treated as absent.

**Rule CF-2 — "not applicable" is a value, not a 10.** Where a factor does not apply — BOUNDARY on
a purely informational message, NEXT STEP on a message that closes an issue — the recorded value
is `N/A` with a reason. Scoring an inapplicable factor `10` inflates every derived figure below.

## 4. Derived figures

Derived from the components, purely for readability. They add no information and carry no
authority.

| Derived figure | Formula |
|---|---|
| `clarity_score` | `(GOAL + CLARITY + NEXT_STEP) / 30 × 100` |
| `brevity_score` | `BREVITY × 10` |
| `emotional_control_score` | `EMOTION × 10` |
| `boundary_strength_score` | `BOUNDARY × 10` |
| `defensiveness_risk` | `100 − (DEFENSIVENESS × 10)` |
| `escalation_risk` | `100 − (ESCALATION × 10)` |
| `conversational_control_score` | `CONTROL × 10` |

**Rule CF-3 — `N/A` components are excluded, not zeroed.** Where a component in a formula is
`N/A`, the derived figure is computed over the applicable components only and is labelled as such.
Treating `N/A` as `0` would report a message as high-risk for lacking something it did not need.

**Rule CF-4 — there is no single overall score.** The ten components are not averaged into one
number. An average lets a strong CLARITY hide a violated BOUNDARY, which is exactly the trade this
methodology refuses to make (`methodology-card.md` MC-1).

## 5. Advisory release thresholds

| Setting | Threshold |
|---|---|
| Internal, low stakes | No applicable component below `6` |
| External, medium stakes | GOAL, CLARITY, EMOTION, BOUNDARY and ESCALATION each `>= 7`; no applicable component below `6` |
| High or critical stakes | **The thresholds are advisory only.** `review.communication_strategy@0.1` and `review.high_stakes_external_communication@0.1` apply, and the human gate applies, whatever the scores are |

**Rule CF-5 — a threshold is a prompt to revise, not a permission to send.** Meeting the
medium-stakes threshold means the producer has finished their own pass. It does not start, skip,
shorten or satisfy any review, and it never identifies a Decision Right.

## 6. What the filter must never do

**Rule CF-6 — the filter is never a gate.** No workflow stage in this package uses a filter score
as an entry or exit criterion for a review or a decision. In
`workflow-difficult-interaction-response.md` the filter is stage S9 and the gate is stage S11, and
they are separate on purpose.

**Rule CF-7 — the filter is not evidence.** A score is a `CALCULATION` over a recorded rubric. It
is not a `FACT_CLAIM`, it is not governance evidence, and it may not be cited as a reason that a message
is safe, accurate, lawful or approved.

**Rule CF-8 — the filter never overrides a protection.** A revision made to raise ESCALATION or
EMOTION must not weaken a material refusal, deadline, condition, reservation of rights, evidence
point or escalation requirement (`methodology-card.md` MC-3, P-15). Where raising a score would
require weakening one, **the score stays low and the reason is recorded**. This is the single most
important rule in this document: a filter that optimises comfort will eventually optimise away the
protection.

**Rule CF-9 — the filter is not a reviewer.** It is a quality-control technique performed by the
producer. It discharges no `review.<id>`, satisfies no `Author != Critical Reviewer` obligation and
creates no reviewer identity (`skill-pack.md` §Review Dependencies).

**Rule CF-10 — the filter never scores a person.** It scores a draft. No component is computed
about the counterparty, and no score is stored against an individual.

**Rule CF-11 — the filter is not a routing input.** Filter scores must not feed the
`communication_conflict_score`, must not influence model selection, and must not appear in a
routing request (`trigger-routing-spec.md` TR-10).

## 7. Recorded output

The filter records, per draft version:

```json
{
  "rubric_version": "filter.communication_control@0.1",
  "draft_version": "<identifier>",
  "components": {
    "goal": 0, "emotion": 0, "clarity": 0, "brevity": 0, "boundary": 0,
    "defensiveness": 0, "control": 0, "relevance": 0, "escalation": 0, "next_step": 0
  },
  "not_applicable": ["<factor name>"],
  "reasons": { "<factor name>": "<the specific text that caused a score below 7>" },
  "derived": {
    "clarity_score": 0, "brevity_score": 0, "emotional_control_score": 0,
    "boundary_strength_score": 0, "defensiveness_risk": 0, "escalation_risk": 0,
    "conversational_control_score": 0
  },
  "protection_conflicts": ["<a revision that was NOT made, and the protection it would have weakened>"],
  "advisory_threshold_met": false,
  "is_approval": false,
  "is_review": false,
  "is_evidence": false
}
```

**`protection_conflicts` is the field that matters.** It is where CF-8 becomes visible: a draft
that scores `5` on ESCALATION because raising it would have softened a reservation of rights is a
**correct** draft, and the record says so.

The three `false` flags are declared explicitly rather than omitted, so that a consumer of this
structure cannot read a filter result as anything it is not.

## 8. Relationship to the assurance suite

`evaluation-spec.md` scores generated outputs on dimensions that overlap this filter's factors.
They are different instruments: the filter is the producer's own pass over one draft; the
evaluation suite is an offline assessment of the capability across a fixed scenario set. Neither
substitutes for the other, and neither is a review.

## 9. Non-Runtime Statement

This document is declarative architecture. It specifies no scorer implementation, orchestration,
model routing, database schema, API, interface or automation code, and binds no model, provider or
runtime technology. The JSON above is a contract shape, not a stored object.
