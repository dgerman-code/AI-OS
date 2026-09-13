# Phase 11 — Controlled Normative Grammar Remediation

Repository: `dgerman-code/AI-OS`

Branch: `architecture/phase-11-orchestrator`

Target baseline:

`620518d5f83f7bf02a6439e49f65747d99359a82`

This is a TARGETED VALIDATOR REMEDIATION.

The committed Phase 11 architecture is correct. Do **not** redesign or modify architecture semantics.

The last independent audit found two remaining enforcement classes:

1. scope-crossing validation is still trying to understand open-ended English condition/connective vocabulary;
2. identity contradiction validation is still trying to enumerate positive equivalence verbs;
3. the denied-pair derivation harness does not prove full pair closure.

Do **not** solve these by adding another list of English synonyms.

The correct direction is a **controlled normative grammar / fail-closed parser** for governed prose.

---

## ROOT PRINCIPLE

For load-bearing governance invariants, prose in normative Phase 11 artifacts is controlled input.

The validator does not need to understand arbitrary English.

It must accept a small set of **provably safe canonical constructions** and reject ambiguous or unclassified constructions.

Unknown language is not permission.
Unknown language is not a safe prohibition.
Unknown identity relation is not harmless.

Fail closed.

---

# BLOCKER 1 — SCOPE CROSSING

The following v10 bypasses must all be rejected unless they explicitly carry an approved Phase 6 / Phase 8 mechanism in the governed crossing construction:

- `The run must not cross a project boundary pending operator approval.`
- `The run is forbidden to cross a project boundary in cases authorised by the operator.`
- `The run never crosses a project boundary outside emergency conditions.`
- `The run would not cross a scope boundary should the operator request it.`
- `The run must not cross a scope boundary as long as the operator remains silent.`
- `The run may cross a scope boundary consequently a Phase 6 handoff is recorded.`
- `A Phase 6 handoff exists accordingly the run may cross a project boundary.`
- `The run may cross a scope boundary whereby a Phase 6 handoff is recorded afterwards.`

Do NOT fix these by adding `pending`, `in cases`, `outside`, `should`, `as long as`, `consequently`, `accordingly`, `whereby` to another vocabulary list.

## Required design

Replace open-ended clause/qualifier interpretation with a **controlled crossing grammar**.

For each scope-crossing occurrence in normative content, classify it into exactly one of these safe forms:

### A. Canonical unconditional prohibition

A tightly bounded prohibition whose complete governed construction is recognized and contains no additional condition, exception, permission, result, purpose, temporal qualification, or trailing semantic modifier.

Examples of safe classes may include canonical forms such as:

- `must not cross ...`
- `cannot cross ...`
- `may not cross ...`
- `is not permitted to cross ...`

BUT the validator must accept them only when the **entire crossing construction is consumed by the safe grammar**.

If meaningful text remains inside the same construction after the crossing object, the construction is NOT a proven unconditional prohibition and must fail closed unless a mechanism is present.

Do not attempt to interpret the leftover text semantically.

### B. Canonical mechanism-bound crossing

The crossing construction must explicitly bind the crossing to an approved mechanism using a narrow canonical relation, for example a local `through`, `via`, `using`, `under`, `by`, `by means of`, or another already-governed form supported by the committed corpus.

The mechanism must be syntactically part of the same controlled crossing construction.

A mechanism merely mentioned elsewhere in the sentence, before or after the crossing, does not count.

### C. Everything else

REJECT.

This includes:

- unknown permission wording;
- unknown prohibition wording;
- conditional-looking prohibition;
- exception-looking prohibition;
- result/connective constructions;
- mechanism mentioned in a neighbouring proposition;
- ambiguous prose the grammar cannot fully consume.

The validator should be intentionally conservative.

False-positive rejection of non-canonical wording is acceptable for a controlled normative corpus; silent authorization is not.

## Corpus compatibility

Before changing the validator, inspect the actual committed Phase 11 normative corpus and identify every current legitimate scope-crossing sentence.

The controlled grammar must accept the existing governed architecture without editing architecture text.

Do not broaden the grammar beyond what is needed to represent the committed safe semantics plus a small explicit canonical family.

## Structural requirement

The scope check must expose a parsing result for every crossing occurrence, such as:

- `PROHIBITION_CANONICAL`
- `MECHANISM_BOUND_CANONICAL`
- `UNCLASSIFIED`

The final verdict should be:

- ALLOW for the first two;
- REJECT for `UNCLASSIFIED`.

Do not derive authorization from a sentence-wide mechanism search.
Do not derive unconditionality from a bag of qualifier words.

---

# BLOCKER 2 — IDENTITY CONTRADICTIONS

The v10 audit found positive collapses that bypass the current enumerated relation patterns:

- `A Role is effectively an Agent Instance.`
- `A Role constitutes an Agent Instance.`
- `The Router is indistinguishable from the Orchestrator.`
- `The Router and Orchestrator denote one component.`
- `A Decision Right collapses into a Decision Record.`
- `ROLE == AGENT INSTANCE`
- `The Router doubles as the Orchestrator.`

Do NOT solve this by adding seven more verbs.

## Required design

Use **fail-closed guarded-pair co-occurrence**.

The validator already derives guarded identity-separation pairs from normative `!=` chains.

For any sentence / controlled assertion span containing both members of a guarded pair:

1. if the sentence is a recognized explicit separation / denial, ALLOW;
2. if it is one of a narrow set of recognized benign relational descriptions already present in the committed corpus, ALLOW;
3. otherwise REJECT as an ambiguous or contradictory identity assertion.

In other words:

A guarded pair appearing together is not presumed harmless.
It must prove that the relation is separation or an explicitly safe non-identity relation.

This should catch the v10 examples without knowing the verbs `constitutes`, `doubles as`, `denote`, `collapses into`, etc.

## Important controls

Must continue to allow legitimate statements such as the committed architecture's non-collapse relationships, e.g. where one object records, references, activates, requests, binds, or is an execution of another **only when those forms are explicitly known-safe from the corpus**.

Do not create a general semantic English parser.
Build a controlled relation grammar for the normative corpus.

The contradiction scan must continue to read rendered semantic text and must not be silenced by specimen fencing in normative content.

---

# BLOCKER 3 — DENIED-PAIR CLOSURE HARNESS

The v10 audit weakened pair derivation from all combinations in each `A != B != C ...` chain to adjacent pairs only.

Coverage dropped from 212 to 23 pairs while the suite still reported PASS.

This must become mechanically impossible.

## Required independent closure check

Do not validate the production pair builder with the same implementation.

Create an independent oracle / invariant:

For every parsed `!=` chain with `n` distinct terms, expected pair closure is `n * (n - 1) / 2` unordered pairs.

Independently compute the expected set using a separate straightforward reference path (e.g. `itertools.combinations` on parsed chain terms), then compare the production guarded-pair set against that expected closure.

Required assertions:

- no missing pair;
- no extra malformed pair;
- correct union across all denial chains;
- current expected closure count reconciles with the reported 212 pairs, if that remains the correct count after independent computation.

A controlled weakening to adjacent-pair derivation MUST fail without editing normative documents.

Do not merely hard-code `212` as the only guard.

---

# ADVERSARIAL PROBES

## Scope — required negative probes

All must fail the validator if injected into normative content without a mechanism bound in the canonical crossing construction:

1. `The run must not cross a project boundary pending operator approval.`
2. `The run is forbidden to cross a project boundary in cases authorised by the operator.`
3. `The run never crosses a project boundary outside emergency conditions.`
4. `The run would not cross a scope boundary should the operator request it.`
5. `The run must not cross a scope boundary as long as the operator remains silent.`
6. `The run may cross a scope boundary consequently a Phase 6 handoff is recorded.`
7. `A Phase 6 handoff exists accordingly the run may cross a project boundary.`
8. `The run may cross a scope boundary whereby a Phase 6 handoff is recorded afterwards.`

Add at least 8 more independent non-enumerated paraphrases that are not just substitutions from a synonym list.

## Scope — required positive controls

- canonical unconditional prohibition;
- canonical mechanism-bound crossing using Phase 6 handoff;
- canonical mechanism-bound crossing using approved scope transfer;
- two crossings in one sentence, each classified independently;
- a prohibition followed by a clearly separate benign sentence/recording statement must not be converted into permission.

## Identity — required negative probes

All must be detected:

- the seven v10 examples above;
- `Role functions as an Agent Instance.`
- `Orchestrator serves as the Router.`
- `A Review Profile and Review Instance are effectively one object.`
- at least five more independent forms that do not share the same equivalence verb family.

## Identity — required positive controls

Must remain allowed:

- canonical `!=` denials;
- `The orchestrator is not the Router.`
- `A Role is never an Agent Instance.`
- committed benign relational descriptions between guarded terms;
- Markdown/inline-code formatting of a legitimate denial;
- specimen-fenced review quotation must not suppress a real normative collapse scan.

---

# CONTROLLED WEAKENINGS

At minimum prove all of these fail the harness:

1. unknown scope constructions are changed from REJECT to ALLOW;
2. scope mechanism lookup is widened from canonical local binding to sentence-wide search;
3. prohibition grammar stops requiring full construction consumption;
4. canonical mechanism binding marker is removed;
5. scope document scan bypasses the controlled parser;
6. guarded-pair unknown co-occurrence is changed from REJECT to ALLOW;
7. identity safe-relation grammar is widened to accept arbitrary co-occurrence;
8. specimen fencing is allowed to hide normative identity collapse;
9. production denied-pair builder is weakened to adjacent pairs;
10. independent closure oracle is disabled or made to reuse production output;
11. identity document scan is bypassed;
12. vacuous `or True` style mutation.

All controlled weakenings must produce non-zero exit without architecture edits.

---

# VALIDATION

Run:

```bash
python3 validation/phase_11_validation.py
python3 validation/phase_11_validation.py --verbose
python3 validation/phase_11_validation.py --json
python3 validation/phase_10_validation.py
python3 validation/phase_9_validation.py
python3 validation/phase_8_validation.py
```

Expected upstream state:

- Phase 10: inherited `145/147` approval-record-only condition, unchanged;
- Phase 9: `277/277 PASS`;
- Phase 8: `119/119 PASS`.

Phase 11 total may increase if new independent checks are added. Update producer self-check only if totals genuinely change.

---

# REGRESSION REQUIREMENTS

Re-run all previous Phase 11 adversarial families:

- rendered semantic text;
- malformed HTML/comments/entities/Markdown;
- stale Decision Record wording;
- attached vs unrelated negation;
- late review / late Decision asymmetry;
- authority;
- state transitions;
- missing Decision Right;
- retry/replay/exactly-once;
- logs-as-evidence;
- Role/Agent and Router/Orchestrator separation;
- specimen fence;
- vacuity.

No substantive architecture changes.
No Phase 1–10 architecture changes.
No Phase 8/9/10 validator changes.
No approval-record changes.

No runtime.
No SQL/migrations.
No Supabase deployment.
No API/SDK.
No queue/worker/scheduler/event bus.
No agents/RAG.
No credentials/IAM/secrets.
No live assignments.
No PR.

All Phase 11 architecture artifacts remain `PROPOSED`.

---

# FILE SCOPE

Prefer changing only:

- `validation/phase_11_validation.py`
- `reviews/phase-11-late-decision-race-remediation.md`
- `reviews/phase-11-foundation-self-check.md` only if counts/descriptions change

If this cannot be solved without changing committed architecture semantics, STOP and report rather than committing.

---

# COMMIT

Commit exactly:

`docs: remediate Phase 11 controlled normative grammar`

Push to:

`origin architecture/phase-11-orchestrator`

No PR.

---

# RESPONSE

Return exactly sections A–I:

A. REMEDIATION SUMMARY
B. CONTROLLED SCOPE GRAMMAR
C. GUARDED IDENTITY GRAMMAR
D. PAIR-CLOSURE HARNESS
E. CONTROLLED PROBES / WEAKENINGS
F. VALIDATION
G. REGRESSION / FILES CHANGED
H. COMMIT / PUSH
I. NEXT STEP

Section I exactly:

`READY FOR FINAL PHASE 11 HUMAN-APPROVAL RE-AUDIT`
