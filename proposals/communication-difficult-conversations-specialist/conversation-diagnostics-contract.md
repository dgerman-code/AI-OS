# Conversation Diagnostics Contract

Status: `PROPOSED`
Version: 0.1
Governance Owner: AI-OS architecture governance

> Contract shapes only. Nothing here specifies a schema, an API, a parser or a store.

## 1. Purpose

Fix the structured input and output of a conversation diagnosis, so that the diagnosis is
reproducible, reviewable, and bounded — in particular so that the vocabulary available for
describing what an exchange is doing cannot drift into describing what a person is.

## 2. Input contract

```json
{
  "task": "string",
  "conversation": "string | message[]",
  "user_goal": "string | null",
  "relationship": "string | null",
  "context": "string | null",
  "stakes": "low | medium | high | critical",
  "desired_tone": "string | null",
  "channel": "email | chat | meeting | phone | negotiation | board | public | other",
  "response_language": "string",
  "constraints": ["string"],
  "other_specialists": ["role-id"],
  "known_facts": ["fact"],
  "approved_positions": ["artifact-ref"],
  "must_not_admit": ["string"],
  "deadline": "string | null",
  "scope_binding": "scope-path",
  "sensitivity_labels": ["string"],
  "disclosure_basis": "string | null"
}
```

Where `conversation` is `message[]`, each message carries `sender`, `recipients`, `timestamp` and
`body`.

**Rule DC-1 — missing is `UNKNOWN`, never inferred into existence.** A field the assignment does
not supply is `null` or `UNKNOWN`. No field is populated by guessing, and `known_facts` is never
extended by the diagnosis itself.

**Rule DC-2 — four fields are mandatory.** `conversation`, `stakes`, `scope_binding` and
`sensitivity_labels`. Absence of any of them makes the assignment invalid (`role-card.md`
§Mandatory Assignment Attributes), and the last three are what keep a diagnosis from becoming an
unlabelled disclosure.

**Rule DC-3 — `disclosure_basis` is required where the labels require it.** Where
`sensitivity_labels` mark personal, special-category, privileged or restricted material, a
`disclosure_basis` must be present or the instance blocks
(`workflow-thread-diagnostics.md` S1).

## 3. Output contract — the full diagnostic

```json
{
  "situation_summary": "string",
  "primary_objective": "string",
  "objective_source": "STATED | INFERRED",
  "user_position": "string",
  "other_party_position": "string | UNKNOWN",
  "other_party_position_source": "STATED | RECONSTRUCTED | UNKNOWN",
  "actual_disagreement": ["string"],
  "evidence": [
    { "evidence_ref": "string", "source_ref": "string", "locator": "message id / position",
      "extract": "string" }
  ],
  "fact_claims": [
    { "claim_ref": "string", "claim": "string", "supported_by": ["evidence_ref"] }
  ],
  "assumptions": ["string"],
  "emotional_triggers": ["string"],
  "power_context": "string | UNKNOWN",
  "boundary_issues": ["string"],
  "pattern_labels": [
    { "label": "see §5", "observable_basis": "string", "source_ref": "string" }
  ],
  "unnecessary_arguments": ["string"],
  "issue_classification": [
    { "issue": "string", "classification": "RESPOND | CLARIFY | REDIRECT | IGNORE | DOCUMENT | ESCALATE",
      "reason": "string", "materiality": "MATERIAL | NON_MATERIAL" }
  ],
  "what_requires_response": ["string"],
  "what_does_not_require_response": ["string"],
  "position_changing_claims": [
    { "claim_ref": "string", "effect": "string" }
  ],
  "recommended_strategy": "string",
  "recommended_tone": "string",
  "recommended_channel": "string",
  "recommended_timing": "string",
  "recommended_next_move": "string",
  "recommended_response": "string | null",
  "shorter_response": "string | null",
  "stronger_response": "string | null",
  "non_response_considered": true,
  "non_response_reasoning": "string",
  "review_required": true,
  "review_trigger": ["RC-5.1 | RC-5.2 | RC-5.3 | RC-5.4"],
  "required_adjacent_review": ["role-or-review-id"],
  "human_gate_status": "REQUIRED | NOT_APPLICABLE | AUTHORITY_ABSENT",
  "human_gate_reference": "decision-id | null",
  "human_gate_reason": "string | null",
  "communication_control_filter": { "see §4a" },
  "diagnostic_risks": { "see §4b" },
  "knowledge_states": {
    "conversation": "SOURCE",
    "evidence": "EVIDENCE",
    "fact_claims": "FACT_CLAIM",
    "assumptions": "ASSUMPTION",
    "pattern_labels": "AI_SUGGESTION",
    "diagnostic": "DRAFT"
  }
}
```

**Rule DC-4 — a claim is a new linked item; nothing is converted.** The interaction record is
`SOURCE` and **stays** `SOURCE`. An extraction bound to its location is an `EVIDENCE` item; an
assertion the extraction supports is a **separate** `FACT_CLAIM` item that links to it. There is
no `SOURCE` → `FACT_CLAIM` transition, no relabelling, and the deprecated label `FACT` appears
nowhere in this package (`knowledge/knowledge-state-model.md` §2; `role-card.md` RC-4).

**Rule DC-4a — a claim with no `supported_by` is not a claim.** It belongs in `assumptions`, and
it is labelled as one.

**Rule DC-5 — `position_changing_claims` is surfaced before any drafting.** Where it is non-empty,
the diagnosis is escalated to the substantive owning Role and `recommended_response` stays `null`
until the position is re-derived (`role-card.md` RC-3).

**Rule DC-6 — `non_response_considered` is never omitted.** Silence and delay are options that
must be evaluated, and the reasoning is recorded whether or not they are chosen
(`methodology-card.md` P-12).

**Rule DC-7 — the gate has three statuses, and two of them are not each other.**

| `human_gate_status` | Means | `human_gate_reference` | When |
|---|---|---|---|
| `REQUIRED` | An external act is contemplated and an applicable approved Right resolves | the concrete `decision.<id>` | The ordinary case for anything transmissible |
| `NOT_APPLICABLE` | **No external act is contemplated by this artifact.** No Decision Right is required *for this act*; this is **not** a finding that authority is present | `null`, with `human_gate_reason` = `NO_EXTERNAL_ACT_CONTEMPLATED` | A read-only diagnosis (`workflow-thread-diagnostics.md`), an internal note, a strategy that recommends non-response |
| `AUTHORITY_ABSENT` | An external act **is** contemplated, it requires authority, and **no applicable approved Right could be resolved** | `null`, with `human_gate_reason` naming the act and why nothing applies | The genuine last resort, after the resolution of `decision-right-gap-analysis.md` §4 has been attempted and returned nothing |

**Rule DC-7a — `NOT_APPLICABLE` never travels.** It attaches to **this** artifact. Where a
diagnostic later feeds a workflow that contemplates a transmission, that workflow resolves its own
gate independently and may not inherit `NOT_APPLICABLE` from its input. An earlier revision forced
a read-only diagnosis to report `AUTHORITY_ABSENT`, which is the opposite claim: it says authority
is missing where none was ever needed, and a system that reports a missing authority on every
diagnosis trains its users to ignore the report that matters.

**Rule DC-7b — the field is never `null` on its own.** `human_gate_status` always carries one of
the three values. "TBD", an empty field, or a description of a category of authority are each a
defect.

**Rule DC-8 — the diagnostic transmits nothing.** It is `DRAFT`, and producing it exercises no
Right, satisfies no review and sends no message.

**Rule DC-8a — `review_required` is derived from RC-5, not restated.** The diagnostic records
which of the four RC-5 conditions fired, so that a reviewer can check the trigger rather than take
it on trust. It does not define the trigger; `role-card.md` RC-5 does, and no other document in
this package states a different one.

## 4. Minimal output contract

For a simple rewriting task where a full diagnosis is not warranted, the output is the improved
text plus the minimum useful note:

```json
{
  "improved_text": "string",
  "note": "string",
  "changes_made": ["string"],
  "protections_preserved": ["string"],
  "review_required": false,
  "review_trigger": [],
  "human_gate_status": "REQUIRED | NOT_APPLICABLE | AUTHORITY_ABSENT",
  "escalated_to_full_diagnostic": false
}
```

**Rule DC-9 — the minimal contract escalates itself.** Where a "just make it firmer" request turns
out to carry an H condition of `trigger-routing-spec.md` §5, an RC-5 condition, a
position-changing claim, or a material boundary issue, `escalated_to_full_diagnostic` is set
`true` and the full contract of §3 is produced instead. The minimal shape is a convenience for
simple cases, never a way around the review and gate path.

**Rule DC-10 — `protections_preserved` is not optional.** Every rewrite records which material
refusals, deadlines, conditions, reservations and evidence points survived it. A rewrite that
cannot list them has not checked (`communication-control-filter.md` CF-8).

## 4a. `communication_control_filter` — the ten factors, and nothing else

This namespace holds **exactly** the structure of `communication-control-filter.md` §7 and
**invents no field** — the same keys, in the same order, in the same case:

```json
{
  "rubric_version": "filter.communication_control@0.1",
  "draft_version": "string",
  "components": {
    "goal": 0, "emotion": 0, "clarity": 0, "brevity": 0, "boundary": 0,
    "defensiveness": 0, "control": 0, "relevance": 0, "escalation": 0, "next_step": 0
  },
  "not_applicable": ["<factor name>"],
  "reasons": { "<factor name>": "string" },
  "derived": {
    "clarity_score": 0, "brevity_score": 0, "emotional_control_score": 0,
    "boundary_strength_score": 0, "defensiveness_risk": 0, "escalation_risk": 0,
    "conversational_control_score": 0
  },
  "protection_conflicts": ["string"],
  "advisory_threshold_met": false,
  "is_approval": false,
  "is_review": false,
  "is_evidence": false
}
```

**Rule DC-11 — the filter has one owner and one field set.** The ten **serialized component keys**
are exactly `goal`, `emotion`, `clarity`, `brevity`, `boundary`, `defensiveness`, `control`,
`relevance`, `escalation`, `next_step`, in that order, and the seven derived figures are exactly
those of the filter document.

**Rule DC-11a — display labels are not JSON keys.** The factor names appear in prose, tables and
score formulas in upper case — `GOAL`, `NEXT_STEP` — because that is how the filter document
presents them to a reader. Those are **display labels**. The serialized keys are the lower-case
forms above, and `communication-control-filter.md` §7 owns them. An earlier revision of this
contract serialized the upper-case labels as keys while claiming exact structural identity with a
document that serializes lower-case ones: the claim of exactness and the schema disagreed, and the
schema comparison could not see it because it only ever looked at upper-case keys. The two JSON
blocks now carry identical key sets in identical order, and the validator compares them exactly
rather than by name-membership.
An earlier revision of this contract carried a **nine-field** object mixing four filter factors
with five risk measures and presented it as the filter's `scores`. That object was neither the
filter nor a risk model: it was a third rubric nobody owned, and a reviewer comparing it against
the filter would have found four names matching and five missing without being able to say which
document was wrong. The two are now separate namespaces, and the validator compares the component
names in this contract against the factor names in the filter document, both directions.

**Rule DC-12 — the diagnostic invents no competing rubric.** Anything that is not one of the ten
factors or one of the seven derived figures belongs in §4b, under its own names.

## 4b. `diagnostic_risks` — the separate risk namespace

```json
{
  "escalation_risk": 0,
  "relationship_risk": 0,
  "documentation_risk": 0,
  "legal_sensitivity": 0,
  "reputational_exposure": 0,
  "timing_risk": 0,
  "channel_risk": 0,
  "rubric_version": "diagnostic.risks@0.1",
  "is_approval": false,
  "is_review": false,
  "is_evidence": false
}
```

| Dimension | What it measures |
|---|---|
| `escalation_risk` | How likely this exchange is to move up the ladder given the record |
| `relationship_risk` | What the working relationship stands to lose |
| `documentation_risk` | What is exposed by the record being incomplete, or by creating one |
| `legal_sensitivity` | How close the exchange is to a legal position, admission or dispute |
| `reputational_exposure` | What becomes visible, and to whom, if the exchange is forwarded |
| `timing_risk` | What responding now, or later, costs |
| `channel_risk` | What the current medium is doing to the exchange |

All are `0`–`100`.

**Rule DC-13 — risk scores are `CALCULATION`, advisory, and never authority.** They inform the
posture decision. They do not set it, do not satisfy a review, and do not identify a gate. Like
the filter scores, they are never stored against a person.

**Rule DC-13a — `escalation_risk` appears in both namespaces and they are different numbers.**
The filter's `escalation_risk` is derived from the ESCALATION component of **one draft**
(`100 − ESCALATION × 10`). The diagnostic's `escalation_risk` is a property of **the exchange**.
They are not interchangeable, they are not compared, and neither is computed from the other. The
namespaces exist so that this is visible rather than a collision.

**Rule DC-14 — no score in either namespace becomes authority.** No component, no derived figure
and no risk dimension may satisfy a review, identify or exercise a Decision Right, select a Model
Profile, or be cited as evidence that a message is safe, accurate, lawful or approved. The three
`false` flags in each namespace are declared explicitly so that a consumer cannot read either
structure as something it is not.

## 5. Bounded pattern-label vocabulary

These are the **only** permitted labels for what an exchange is doing. The set is closed. A
diagnosis may not coin a new one.

| Label | Describes | Never means |
|---|---|---|
| `GENUINE_CLARIFICATION_NEEDED` | The material is objectively ambiguous on a point that matters | — |
| `POSSIBLE_MISUNDERSTANDING` | Two readings of the same text are both available | That anyone is confused as a person |
| `POSSIBLE_STRATEGIC_CONFUSION` | Confusion is asserted about a point previously stated clearly and dated | That the party is lying |
| `POSSIBLE_DEFLECTION` | The central question is unanswered while adjacent topics are answered | That the party is evasive by nature |
| `POSSIBLE_DELAY_TACTIC` | Successive turns add process steps without advancing the decision | That the party intends delay |
| `POSSIBLE_RESPONSIBILITY_AVOIDANCE` | Attribution is moved without addressing the substantive point | That the party is avoiding responsibility |
| `REOPENED_CLOSED_ISSUE` | A point recorded as closed on a stated date is raised again | Bad faith |
| `TOPIC_SHIFT` | The subject changes before the current issue is closed | Intent |
| `NON_MATERIAL_ACCUSATION` | An allegation that cannot change the outcome or the record | That it is untrue |
| `PRESSURE_WITHOUT_AUTHORITY` | A demand is made by someone the record does not show as the decision-maker | That the person is overreaching deliberately |

**Rule DC-15 — every label is hedged, observable and evidenced.** Each carries the observable
feature of the exchange it rests on, with a `source_ref`. A label with no observable basis is a
finding against the diagnosis, not a finding about the exchange
(`workflow-thread-diagnostics.md` S4).

**Rule DC-16 — labels describe exchanges, never people.** No label may be written as a property of
a person, restated as a characterisation, or aggregated across interactions into a profile of a
counterparty. The "Never means" column is normative.

**Rule DC-17 — prohibited vocabulary.** The diagnosis must not use, and must not paraphrase:
narcissism, gaslighting, manipulation, lying, bad faith, dishonesty, incompetence, instability,
personality, pathology, or any clinical term. Where a user supplies such a term, the diagnosis
records it as the user's characterisation, in quotation, and does not adopt it
(`role-card.md` limit 3; `methodology-card.md` S-1).

## 7. Hedging vocabulary

Permitted for anything inferred: `possible`, `appears to`, `may indicate`, `potential risk`,
`the exchange is structured such that`, `on the record as it stands`.

Prohibited for anything inferred: any unhedged assertion of intent, motive, character or state.

## 8. Non-Runtime Statement

This document is declarative architecture. It specifies no schema, API, parser, store,
orchestration, model routing or automation code, and binds no model, provider or runtime
technology. The JSON above is a contract shape, not a stored object.
