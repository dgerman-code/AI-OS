# Phase 11 — Claude remediation: scope qualifiers and identity contradictions

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-11-orchestrator`

Exact remediation baseline:
`f5a919ef408e9c340f9e405a10833d49d6ac1f5d`

This is a targeted validator remediation only.

Do NOT redesign Phase 11 architecture.
Do NOT modify substantive architecture semantics.
Do NOT touch Phase 1–10 semantic artifacts, Phase 8/9/10 validators, or Phase 9/10 approval records.
No runtime, SQL, migrations, deployment, API/SDK, queues, workers, scheduler, event bus, agents, RAG, credentials, IAM, secrets, or PR.
All Phase 11 architecture artifacts remain `PROPOSED`.

## Context

The latest independent human-approval re-audit on the exact baseline above reports that the fail-closed scope rule is materially improved, but two validator-enforcement gaps remain:

1. **Scope clause/qualifier parsing is incomplete.**
   These mechanism-free crossings incorrectly pass:
   - `A Phase 6 handoff is discussed — the run may cross a scope boundary.`
   - `The run may cross a scope boundary so a Phase 6 handoff can be recorded later.`
   - `The run would not cross a project boundary unless an operator requested it.`
   - `The run is forbidden to cross a project boundary except when an operator requests it.`
   - `The run never crosses a project boundary unless the operator asks.`

   The first two borrow a mechanism from a neighbouring clause because the current clause grammar does not recognise boundaries such as an em dash and `so`.
   The last three are **conditional permissions disguised by an apparent prohibition**. A prohibition qualified by `unless`, `except`, `except when`, or equivalent permission-restoring language must NOT be treated as an unconditional prohibition.

2. **Identity contradiction scans are not fail-closed.**
   Contradictory assertions such as:
   - `ROLE = AGENT INSTANCE`
   - `ROUTER = ORCHESTRATOR`

   can currently coexist with the required canonical denial text elsewhere in the corpus without causing validation failure.

The independent audit rated harness credibility `MEDIUM`. Human approval requires `HIGH`.

---

# BLOCKER 1 — FAIL-CLOSED SCOPE CLAUSE AND QUALIFIER PARSING

The scope invariant remains:

> A clause that asserts, permits or describes a scope crossing must name an approved Phase 6 / Phase 8 mechanism in that same crossing clause. Only an **unqualified prohibition attached to that same crossing predicate** may stand without a mechanism.

The key addition is **unqualified**.

A prohibition is not sufficient if later language in the same logical construction re-opens permission, for example:
- `unless ...`
- `except ...`
- `except when ...`
- `except if ...`
- `unless and until ...`
- or any other explicit exception/condition that converts the prohibition into a conditional permission.

## Required behavior

The following MUST REJECT without an approved mechanism in the crossing clause:

- `A Phase 6 handoff is discussed — the run may cross a scope boundary.`
- `The run may cross a scope boundary so a Phase 6 handoff can be recorded later.`
- `The run would not cross a project boundary unless an operator requested it.`
- `The run is forbidden to cross a project boundary except when an operator requests it.`
- `The run never crosses a project boundary unless the operator asks.`

Also add independent paraphrases beyond these exact strings, including at minimum:
- em dash / en dash / colon boundaries;
- `so`, `therefore`, `hence`, `provided that`, `if`, `unless`, `except`, `except when`, `except if`;
- a prohibition with an unrelated trailing clause that does **not** re-open crossing and therefore remains allowed;
- a prohibition followed by an explicit approved mechanism in a separate clause — the separate mechanism must NOT satisfy a conditional permission in the crossing clause;
- two crossings in one sentence with different qualification, proving treatment is per occurrence.

## Design requirement

Do NOT keep patching a flat list of clause separators without a semantic rule.

Refactor the scope reading so that, for each crossing occurrence, the validator determines a bounded **crossing construction** consisting of:
- the crossing predicate and its governing modal/negation;
- the local clause containing the crossing;
- any directly attached exception/condition that can alter whether crossing is permitted.

Then enforce:

1. If the crossing is an **unqualified prohibition** attached to the crossing predicate -> ALLOW without mechanism.
2. If the prohibition is qualified by an exception/condition that permits crossing in some case -> treat as permission/assertion and require an approved mechanism in the crossing construction.
3. Otherwise require the approved mechanism in the crossing construction itself.
4. A mechanism in a neighbouring clause or before/after an em-dash/colon/causal boundary does not count.
5. Unknown wording fails closed.

Prefer deterministic standard-library parsing/scanning. Do not introduce third-party NLP dependencies.

## Required self-guards

The validator must directly guard the rule, not only phrase examples.

At minimum self-guard:
- em dash is a boundary for mechanism borrowing;
- en dash is a boundary;
- `so`/`therefore`/`hence` starts a neighbouring consequence clause;
- `unless` qualifies a prohibition and destroys the unconditional-prohibition exemption;
- `except` / `except when` / `except if` do the same;
- a genuinely unconditional prohibition still ALLOWs without a mechanism;
- two crossing occurrences are evaluated independently;
- widening the mechanism search from crossing construction to sentence must fail the harness;
- removing conditional-qualification detection must fail the harness;
- weakening one crossing occurrence must not be hidden by another correct occurrence.

---

# BLOCKER 2 — IDENTITY CONTRADICTION DETECTION

The canonical Phase 11 identity model already states identities such as:

`ROLE != AGENT INSTANCE != MODEL != MODEL PROFILE != ROUTER != ORCHESTRATOR ...`

The validator must fail if normative Phase 11 content also contains a contradictory positive collapse assertion, even if the canonical denial remains elsewhere.

At minimum it must reject explicit normative assertions equivalent to:

- `ROLE = AGENT INSTANCE`
- `ROLE IS AGENT INSTANCE`
- `A Role is an Agent Instance`
- `ROUTER = ORCHESTRATOR`
- `The Router is the Orchestrator`
- `Router and Orchestrator are the same component`

Do not only check those two pairs. Use the existing load-bearing identity denials as the source of the contradiction pairs and guard them systematically where practical.

## Identity contradiction rule

A required denial being present is not enough.
The validator must also scan normative Phase 11 content for **positive collapse assertions** contradicting those denials.

The scan must distinguish:
- denial/contrast prose -> allowed;
- quoted/review specimen examples in explicitly permitted review-only specimen fences -> allowed only under the existing specimen governance;
- normative positive identity collapse -> reject.

Do NOT let one correct denial elsewhere cancel a contradictory positive assertion.

## Required identity probes

Negative probes must include at least:
- `ROLE = AGENT INSTANCE`
- `A Role is an Agent Instance.`
- `ROUTER = ORCHESTRATOR`
- `The Router is the Orchestrator.`
- `Router and Orchestrator are the same component.`
- at least two additional load-bearing identity collapses chosen from the 21-object chain.

Positive controls must include canonical inequality/denial language and benign descriptive references that do not collapse identities.

Controlled weakening must prove that removing the contradiction scan causes at least one committed harness check to fail without editing architecture documents.

---

# VALIDATION / REGRESSION

Re-run all prior Phase 11 suites, including:
- malformed/rendered-text grammar;
- Markdown/HTML/entity/comment handling;
- stale Decision Record wording and attached-negation logic;
- late review versus late Decision asymmetry;
- specimen fence boundaries;
- orchestrator authority;
- state machine;
- missing Decision Right continuation;
- retry/replay/idempotency/exactly-once;
- scope crossing prior suites;
- logs-as-evidence;
- Role/Agent and Router/Orchestrator identity separation;
- vacuity / `or True`.

Run:

```bash
python3 validation/phase_11_validation.py
python3 validation/phase_11_validation.py --verbose
python3 validation/phase_11_validation.py --json
python3 validation/phase_10_validation.py
python3 validation/phase_9_validation.py
python3 validation/phase_8_validation.py
```

Expected upstream only if independently reproduced:
- Phase 10: inherited `145/147` approval-record-only condition, unchanged;
- Phase 9: `277/277 PASS`;
- Phase 8: `119/119 PASS`.

If the Phase 11 check count changes, update only the Phase 11 self-check/review documentation that genuinely needs the new total.

Architecture content under `architecture/` and `orchestration/` must remain byte-for-byte unchanged. If fixing the validators requires architecture semantic changes, STOP and report instead of committing.

---

# FILES

Prefer changing only:
- `validation/phase_11_validation.py`
- `reviews/phase-11-late-decision-race-remediation.md`
- `reviews/phase-11-foundation-self-check.md` only if totals/group descriptions genuinely change.

No PR.

# COMMIT

Commit exactly:

`docs: remediate Phase 11 scope qualifiers and identity contradictions`

Push to:

`origin architecture/phase-11-orchestrator`

# RESPONSE

Return exactly sections A-I:

A. REMEDIATION SUMMARY
B. SCOPE CONSTRUCTION / QUALIFIER RULE
C. IDENTITY CONTRADICTION RULE
D. VALIDATOR REPAIR / CONTROLLED PROBES
E. VALIDATION
F. REGRESSION
G. FILES CHANGED
H. COMMIT / PUSH
I. NEXT STEP

Section I exactly:

`READY FOR FINAL PHASE 11 HUMAN-APPROVAL RE-AUDIT`
