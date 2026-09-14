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
  "facts": [{ "claim": "string", "source_ref": "string" }],
  "assumptions": ["string"],
  "emotional_triggers": ["string"],
  "power_context": "string | UNKNOWN",
  "boundary_issues": ["string"],
  "possible_deflection": ["string"],
  "possible_strategic_confusion": ["string"],
  "unnecessary_arguments": ["string"],
  "issue_classification": [
    { "issue": "string", "classification": "RESPOND | CLARIFY | REDIRECT | IGNORE | DOCUMENT | ESCALATE",
      "reason": "string", "materiality": "MATERIAL | NON_MATERIAL" }
  ],
  "what_requires_response": ["string"],
  "what_does_not_require_response": ["string"],
  "position_changing_facts": [{ "claim": "string", "source_ref": "string", "effect": "string" }],
  "escalation_risk": 0,
  "relationship_risk": 0,
  "documentation_risk": 0,
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
  "required_adjacent_review": ["role-or-review-id"],
  "human_gate_required": true,
  "human_gate_reference": "decision-id | AUTHORITY_ABSENT",
  "scores": {
    "clarity": 0, "brevity": 0, "emotional_control": 0, "boundary_strength": 0,
    "escalation_risk": 0, "defensiveness_risk": 0, "conversational_control": 0,
    "relationship_risk": 0, "documentation_risk": 0
  },
  "knowledge_states": {
    "conversation": "SOURCE",
    "facts": "FACT",
    "assumptions": "ASSUMPTION",
    "pattern_labels": "AI_SUGGESTION",
    "diagnostic": "DRAFT"
  }
}
```

**Rule DC-4 — `facts` carries provenance per entry.** A claim with no `source_ref` is not a fact
and belongs in `assumptions`.

**Rule DC-5 — `position_changing_facts` is surfaced before any drafting.** Where it is non-empty,
the diagnosis is escalated to the substantive owning Role and `recommended_response` stays `null`
until the position is re-derived (`role-card.md` RC-3).

**Rule DC-6 — `non_response_considered` is never omitted.** Silence and delay are options that must
be evaluated, and the reasoning is recorded whether or not they are chosen
(`methodology-card.md` P-12).

**Rule DC-7 — `human_gate_reference` admits exactly two kinds of value.** A concrete `decision.<id>`,
or the literal `AUTHORITY_ABSENT`. It is never `null`, never "TBD", and never a description of a
category of authority. An unresolved gate is a **blocked** state with a name, not an empty field.

**Rule DC-8 — the diagnostic transmits nothing.** It is `DRAFT`, and producing it exercises no
Right, satisfies no review and sends no message.

## 4. Minimal output contract

For a simple rewriting task where a full diagnosis is not warranted, the output is the improved
text plus the minimum useful note:

```json
{
  "improved_text": "string",
  "note": "string",
  "changes_made": ["string"],
  "protections_preserved": ["string"],
  "escalated_to_full_diagnostic": false
}
```

**Rule DC-9 — the minimal contract escalates itself.** Where a "just make it firmer" request turns
out to carry an H condition of `trigger-routing-spec.md` §5, a position-changing fact, or a
material boundary issue, `escalated_to_full_diagnostic` is set `true` and the full contract of §3
is produced instead. The minimal shape is a convenience for simple cases, never a way around the
review and gate path.

**Rule DC-10 — `protections_preserved` is not optional.** Every rewrite records which material
refusals, deadlines, conditions, reservations and evidence points survived it. A rewrite that
cannot list them has not checked (`communication-control-filter.md` CF-8).

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

**Rule DC-11 — every label is hedged, observable and evidenced.** Each carries the observable
feature of the exchange it rests on, with a `source_ref`. A label with no observable basis is a
finding against the diagnosis, not a finding about the exchange
(`workflow-thread-diagnostics.md` S4).

**Rule DC-12 — labels describe exchanges, never people.** No label may be written as a property of
a person, restated as a characterisation, or aggregated across interactions into a profile of a
counterparty. The "Never means" column is normative.

**Rule DC-13 — prohibited vocabulary.** The diagnosis must not use, and must not paraphrase:
narcissism, gaslighting, manipulation, lying, bad faith, dishonesty, incompetence, instability,
personality, pathology, or any clinical term. Where a user supplies such a term, the diagnosis
records it as the user's characterisation, in quotation, and does not adopt it
(`role-card.md` limit 3; `methodology-card.md` S-1).

## 6. Risk dimensions

| Dimension | What it measures | Scale |
|---|---|---|
| `escalation_risk` | How likely this exchange is to move up the ladder given the record | `0`–`100` |
| `relationship_risk` | What the working relationship stands to lose | `0`–`100` |
| `documentation_risk` | What is exposed by the record being incomplete, or by creating one | `0`–`100` |

**Rule DC-14 — risk scores are `CALCULATION`, advisory, and never authority.** They inform the
posture decision. They do not set it, do not satisfy a review, and do not identify a gate. Like the
filter scores, they are never stored against a person.

## 7. Hedging vocabulary

Permitted for anything inferred: `possible`, `appears to`, `may indicate`, `potential risk`,
`the exchange is structured such that`, `on the record as it stands`.

Prohibited for anything inferred: any unhedged assertion of intent, motive, character or state.

## 8. Non-Runtime Statement

This document is declarative architecture. It specifies no schema, API, parser, store,
orchestration, model routing or automation code, and binds no model, provider or runtime
technology. The JSON above is a contract shape, not a stored object.
