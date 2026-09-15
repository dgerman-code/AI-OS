# Request and Work Intent Model

Status: `PROPOSED` — Phase 15 architecture candidate
Version: 0.1

## 1. Two objects, and the distance between them

| Object | Is | Epistemic type |
|---|---|---|
| **Request** | What the user wrote, byte for byte, with who wrote it and when | `SOURCE` |
| **Work Intent** | The system's structured reading of it | `AI_SUGGESTION` |

**Rule RI-1 — the Request is a source and stays a source.** It is never edited, normalised,
summarised in place, or replaced by its interpretation. A source is cited, never promoted
(`knowledge/knowledge-state-model.md` §2). Where the user later clarifies, that is a **new**
Request linked to the first, not a correction of it.

**Rule RI-2 — the Work Intent is a reading, and the system says so.** It is `AI_SUGGESTION`: an
unadopted proposal. No acceptance, no confidence, no downstream use converts it into a
`FACT_CLAIM` about what the user wanted. The user confirming it does not convert it either — a
confirmed reading is a reading the user agreed with, recorded as such.

That distance is the whole point of separating the two. A system that overwrote the request with
its interpretation would have no way to notice it had misread, and no way to show the user what it
thought they said.

## 2. The Work Intent fields

Each is **inferred**, **stated by the user**, or explicitly `UNKNOWN`. There is no fourth state,
and absence is never silently treated as a default.

| # | Field | Values | Notes |
|---:|---|---|---|
| 1 | `objective` | free text \| `UNKNOWN` | What the user is trying to achieve, not what they asked for |
| 2 | `requested_outcome` | free text \| `UNKNOWN` | The deliverable as the user framed it |
| 3 | `primary_work_mode` | exactly one of `ACTION` · `ANALYSIS` · `ADVICE` · `DRAFTING` · `MONITORING` · `DECISION_SUPPORT` \| `UNKNOWN` | §3. Never a set |
| 4 | `secondary_work_modes` | a unique set of zero or more further modes from the same enum | §3. Never contains the primary; never `UNKNOWN` — an empty set is the absence |
| 5 | `entities` | list of references \| empty | Counterparties, projects, documents, instruments named or implied |
| 6 | `scope_candidates` | ordered list \| empty | Handed to the Context Resolver; never resolved here |
| 7 | `urgency` | free text \| `UNKNOWN` | Only where stated. Never inferred from tone |
| 8 | `deadline` | date \| `UNKNOWN` | Only where stated |
| 9 | `act_direction` | `INTERNAL` · `EXTERNAL` \| `UNKNOWN` | Does anything leave the entity? |
| 10 | `reversibility` | `REVERSIBLE` · `COSTLY_TO_REVERSE` · `IRREVERSIBLE` \| `UNKNOWN` | Of the **act**, not the artifact |
| 11 | `commitment_possible` | `YES` · `NO` \| `UNKNOWN` | Could this bind the entity? |
| 12 | `transmission_contemplated` | `YES` · `NO` \| `UNKNOWN` | Is sending, publishing or filing in view? |
| 13 | `execute_or_prepare` | `EXECUTE` · `PREPARE` · `RECOMMEND` \| `UNKNOWN` | §4 |
| 14 | `language` | language tag \| `UNKNOWN` | Where an output language matters |
| 15 | `audience` | free text \| `UNKNOWN` | Who receives the output |
| 16 | `channel` | `EMAIL` · `CHAT` · `MEETING` · `DOCUMENT` · `PUBLICATION` · `SUBMISSION` · `OTHER` \| `UNKNOWN` | |

**Rule RI-3 — `UNKNOWN` is a determinate finding, not a blank.** It says the question was asked and
the answer is not held. A field that was never considered is a defect in the interpreter, not an
`UNKNOWN`, and `governance-preflight.md` check G-2 fails a Work Intent with a missing field rather
than treating absence as `UNKNOWN`.

**Rule RI-4 — the four safety fields are never inferred permissively.** Fields 9, 10, 11 and 12
decide whether this request can cause something irreversible. Where the material does not settle
one, it is `UNKNOWN`, and `UNKNOWN` on any of the four routes to the conservative branch in
`work-classification-and-criticality.md` §5 — never to the convenient one. "Probably internal" is
`UNKNOWN`, not `INTERNAL`.

## 3. Work mode

| Mode | The user wants | Typical artifact |
|---|---|---|
| `ACTION` | Something done in the world | An act with an external effect |
| `ANALYSIS` | To understand something | An assessment |
| `ADVICE` | A recommendation they will act on | A recommendation with reasoning |
| `DRAFTING` | Text produced | A draft |
| `MONITORING` | To be told when something changes | A watch condition and a report |
| `DECISION_SUPPORT` | Material for a decision someone will make | A decision pack |

**Rule RI-12 — one primary mode, a set of secondary modes, and no free-form third form.**
A multi-part request is never represented as two primaries, as a compound value such as
`ANALYSIS_AND_DRAFTING`, or as prose the implementer has to re-parse. It is one
`primary_work_mode` — a single enum value **or** `UNKNOWN` — and a set of `secondary_work_modes`.
The derivation is deterministic:

**The derivation reads the Request and nothing else.** `WorkIntent` is produced at step 2 of the
planning sequence, before any `PlanStage` exists, so a rule that derived the primary mode from stage
dependency order would be reading an object that has not been built yet — and would make the
sequence circular. The tests below are applied **in order**, and the first that resolves wins:

| # | Test, over the Request text and the stated Work Intent fields only | Resolves the primary as |
|---:|---|---|
| 1 | The user **states a priority** — "first work out whether they are right, then draft a reply", "mainly I need the analysis" | The mode of the result they put first |
| 2 | The request names **exactly one end result** | The mode of that result |
| 3 | An **explicit execution verb** governs the request — send, file, submit, publish, post, pay, sign — and `transmission_contemplated` or `commitment_possible` is `YES` | `ACTION`. A consequential act leads whatever else is asked for |
| 4 | The request has one **direct grammatical target** and the rest is subordinate to it — "prepare a response *based on* whether they are right" | The mode of the main clause's object |
| 5 | None of the above resolves | **`UNKNOWN`** |

**The normative worked case.** *"Check whether they are right and prepare a response."* Two end
results, joined by *and*, with no stated priority, no single execution verb, and no subordinating
clause making one the object of the other. Test 1 does not resolve it — the user stated no priority.
Test 2 does not — there are two end results. Test 3 does not — *prepare* is not an execution verb,
and nothing is transmitted. Test 4 does not — neither result is grammatically subordinate to the
other. So test 5 applies:

| Field | Value |
|---|---|
| `primary_work_mode` | **`UNKNOWN`** |
| `secondary_work_modes` | **`{ANALYSIS, DRAFTING}`** — the complete applicable set |

`ANALYSIS` is **not** the answer here, and the reasons it might look like the answer are exactly the
ones this rule rejects: that the analysis comes first in the sentence, that it must happen before
the drafting can, or that it feels like the substantive core of the request. Sequence is not
priority, a dependency is not a primacy, and "feels central" is not a test. `exemplars.md` Example 2
is the same request and returns the same result.

**Rule RI-13 — the primary mode is derived upstream, or it is `UNKNOWN`.** It is never derived from
a `PlanStage`, a dependency order, a Workflow candidate, a Role requirement or anything else the
planner builds later, and it is never invented to avoid an `UNKNOWN`. Where test 5 is reached, the
primary is `UNKNOWN` and **every** applicable mode is carried in `secondary_work_modes` — the set is
complete, not a remainder after an arbitrary pick. Downstream consumers read `UNKNOWN` as what it is
(RI-3): a determinate finding that the request did not settle which result leads.

`secondary_work_modes` is a **set**: unordered, unique, possibly empty, and never containing the
primary — except where the primary is `UNKNOWN`, which names no mode and therefore excludes none.
Downstream logic that needs a single leading mode reads `primary_work_mode` and nothing else, so
there is no place where a reader has to decide which of several modes leads; where it reads
`UNKNOWN`, the honest answer is that no mode leads, and the conservative routing of WC-6 applies to
the consequences rather than to the mode.

**Rule RI-5 — the mode does not decide the gate.** A `DRAFTING` request whose draft is going to be
sent carries a transmission gate exactly as an `ACTION` request does. The mode describes the shape
of the work; fields 9–12 describe its consequences, and the consequences drive governance.

## 4. Execute, prepare, recommend

The single most consequential distinction in this model, and the one a user most often leaves
implicit.

| Value | Means | Planner behaviour |
|---|---|---|
| `EXECUTE` | The user wants the act performed | The plan must resolve every authority the act requires, and blocks where one is missing |
| `PREPARE` | The user wants it ready, not done — **stated**, never assumed | The plan stops before the transmitting act and says so explicitly |
| `RECOMMEND` | The user wants to know what to do | No act is planned at all |

**Rule RI-6 — ambiguity between `EXECUTE` and `PREPARE` on an irreversible act is material, and it
blocks.** It is not resolved by inference, by convenience, or by asking the model what it thinks. It
is a clarification under `clarification-policy.md` class **C4**, and it follows CL-2 exactly: the
plan sits in `AWAITING_CLARIFICATION`, and where the question is unanswerable or unavailable the
plan becomes **`BLOCKED`**.

There is **no default to `PREPARE`**. An earlier version of this rule said the plan "degrades to
`PREPARE`" where clarification was unavailable, which contradicted CL-2 and was wrong in the way
that matters: `PREPARE` is not a neutral fallback, it is a **different act from the one the user
asked for**, chosen by the system without being told. Substituting it silently is the scope change
UX-5 and FE-1 forbid, and doing it under the name of safety makes it harder to notice.

Where the user afterwards asks for preparation only, that is a **new linked `Request`** and a
revised `WorkIntent` (RI-1) — a thing the user decided, recorded as such. It is never the automatic
destination of a blocked plan. **The safe direction is the one that does less, and doing less than
was asked is still a decision the user makes.**

"Send them confirmation that we accept the terms" is the canonical case. The verb is `EXECUTE`, the
act may be a contractual commitment, and the correct planner behaviour is neither to send nor to
quietly draft: it is to resolve the applicable Decision Right and block on its absence
(`exemplars.md` Example 4).

## 5. What the interpreter may not do

**Rule RI-7 — no field is populated from what would be convenient.** An inference must be supported
by something in the request or in resolved context. Where it is not, the field is `UNKNOWN`.

**Rule RI-8 — no psychological or motive inference.** The interpreter reads what was asked. It does
not model why, does not attribute states of mind to the user or to third parties, and does not
record tone as a fact about anyone.

**Rule RI-9 — the interpreter creates no governed record.** It produces a `Request` and a
`WorkIntent`. It creates no knowledge item, no Decision Record, no Review Instance, no Work Item and
no run.

**Rule RI-10 — verbatim material is carried, not paraphrased.** Where the request encloses material
— a pasted email, a clause, a figure — that material is carried as `SOURCE` at full fidelity and
referenced by location. A paraphrase of evidence is not evidence.

## 6. Relationship to knowledge typing

| Thing | Type |
|---|---|
| The request text, and anything pasted into it | `SOURCE` |
| An extraction from that text, bound to its location | `EVIDENCE` |
| An assertion the extraction supports | `FACT_CLAIM`, **new and linked** |
| The Work Intent, and every inferred field | `AI_SUGGESTION` |
| A field the user stated explicitly | `FACT_CLAIM` about what was requested, linked to the request |
| A field neither stated nor safely inferable | `UNKNOWN` |

**Rule RI-11 — nothing is converted.** There is no `SOURCE` → `FACT_CLAIM` transition and no
`AI_SUGGESTION` → anything transition. A supported assertion is a **new linked item** with its own
basis (`knowledge/knowledge-state-model.md` §2a). The planner needing a fact to be true is not a
basis.

## 7. Worked field derivation

For "Send them confirmation that we accept the terms":

| Field | Value | Basis |
|---|---|---|
| `objective` | Communicate acceptance of terms to a counterparty | Inferred from the verb and object |
| `primary_work_mode` | `ACTION` | "Send" |
| `secondary_work_modes` | empty | Nothing else is requested |
| `entities` | "them" → `UNKNOWN`; "the terms" → `UNKNOWN` | **Neither resolves.** Two unresolved entities on a committing act |
| `act_direction` | `EXTERNAL` | "Send them" |
| `reversibility` | `IRREVERSIBLE` | Acceptance of terms is not retractable by the sender |
| `commitment_possible` | `YES` | "We accept" is the language of commitment |
| `transmission_contemplated` | `YES` | "Send" |
| `execute_or_prepare` | `EXECUTE` | Stated |

Nine fields, and the two `UNKNOWN`s are the ones that matter: the planner does not know **who** or
**which terms**. `clarification-policy.md` classifies both as material, and
`governance-preflight.md` blocks regardless, because an `EXECUTE` + `IRREVERSIBLE` +
`commitment_possible = YES` request requires a resolved Decision Right before anything is planned.

## 8. Non-Runtime Statement

This document is declarative architecture. It specifies no parser, classifier, model, prompt,
schema, API or storage mechanism, and binds no provider or runtime technology.
