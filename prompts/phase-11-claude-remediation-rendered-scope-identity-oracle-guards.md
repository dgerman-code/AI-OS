# Phase 11 — Remediation: rendered scope discovery, guarded identity co-occurrence, and closure-oracle anti-vacuity

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-11-orchestrator`
Current baseline: `15e349fe20fcceb9c433bb3f509a7b7e64ddf11b`

This is a targeted validator-only remediation. Do not change Phase 11 architecture semantics. Do not edit `architecture/` or `orchestration/`.

The latest independent audit found exactly three remaining enforcement gaps:

1. Scope discovery still scans with `plain()` before detecting `cross`, so visible predicates split by supported rendering syntax are missed.
2. Guarded identity-pair co-occurrences are silently skipped when the relation is long, parenthetical, pronoun-bearing, or contains multiple content words.
3. The closure-oracle check can itself be disabled by replacing `denied_pair_closure()` with an unconditional successful return while the suite still passes.

Do not reopen the old paraphrase-enumeration strategy. Keep the controlled normative grammar.

## 1. Rendered scope discovery must use the same semantic text path

`crossing_spans()` / document discovery must search for scope-crossing predicates in rendered semantic text, not the limited `plain()` representation.

Required principle:

> Any syntax already supported by the rendered-text normalizer may alter presentation but may not hide a scope-crossing predicate from discovery.

At minimum these must be discovered and rejected unless the rendered result is canonical/governed:

- `The run may cr*oss* a project boundary.`
- `The run may c<!--x-->ross a project boundary.`
- equivalent inline-code / emphasis / HTML / entity splits where the rendered visible text contains `cross` or `crossing`

Use the existing `semantic_text()` reading path or a single shared semantic-reader helper. Do not create a second, weaker renderer for scope.

Add direct guards proving that:

- raw Markdown and rendered text map to the same crossing discovery result;
- formatting cannot erase or split the crossing predicate;
- weakening scope discovery back to `plain()` makes the harness fail.

## 2. Guarded identity co-occurrence must fail closed, not skip hard spans

The controlled identity contract is:

> If two guarded identity terms co-occur in the same normative predication, the span must prove an approved safe relation or explicit separation. If the validator cannot prove that, it is an offence.

The current implementation still skips spans because of maximum-gap/content-word heuristics. Remove silent skipping as an outcome.

Fresh audit examples that must be rejected:

- `A Role has exactly the same governance identity as an Agent Instance.`
- `A Role should be treated in all respects as an Agent Instance.`
- `A Role, for every operational purpose, constitutes an Agent Instance.`
- `A Role is functionally indistinguishable from an Agent Instance.`
- `A Role, which the runtime creates, is an Agent Instance.`
- `The Router and the Orchestrator, taken together, are one component.`

Do not add these phrases to an equivalence-word list. Instead change discovery so guarded-pair co-occurrence is conservatively identified first, then a narrow safe-grammar proves it benign. Unknown relation = offence.

Preserve legitimate committed relations such as explicit inequality/separation, possessive references, and the already measured safe relation vocabulary from the committed corpus.

Add guards for long spans, parentheticals, pronouns, relative clauses, coordinated subjects, Markdown/code formatting, and specimen fences.

## 3. Closure oracle must have independent anti-vacuity protection

The latest audit replaced:

`denied_pair_closure()`

with an immediate successful return and still got `158/158 PASS`.

Fix this structurally.

Do not rely on a generic text scan for `or True` or similar syntax.

There must be at least one independent registered check that does NOT call `denied_pair_closure()` and independently proves the full closure property from source denial chains using its own parsing/computation path.

For example:

- independent chain parser;
- independent `itertools.combinations` closure;
- direct comparison against the production denied-pair set;
- explicit longest-chain closure assertion;
- synthetic 4-term chain → exactly 6 pairs.

The key requirement is mutation resistance:

- replacing `denied_pair_closure()` with `return (True, "")` must make another registered check fail;
- weakening production pair derivation to adjacent pairs must fail;
- weakening the independent oracle must fail a separate guard;
- aliasing the oracle to production output must fail;
- deleting one of the two independent checks must be detectable by expected check/group inventory where practical.

Avoid circular verification where two checks call the same helper and therefore fail together.

## Controlled weakening requirements

Add and execute controlled mutations for at least:

1. scope discovery reverted to `plain()`;
2. rendered scope split by emphasis/comment ignored;
3. identity long-span co-occurrence skipped;
4. identity parenthetical co-occurrence skipped;
5. unknown guarded-pair relation treated as benign;
6. specimen fence suppresses identity contradiction;
7. production denied-pair builder reduced to adjacent pairs;
8. `denied_pair_closure()` replaced with immediate success;
9. independent closure checker replaced with immediate success;
10. independent oracle aliases production output;
11. identity document scan bypassed;
12. vacuous boolean mutation.

Every mutation must produce non-zero exit without editing architecture documents.

## Validation

Run:

```bash
python3 validation/phase_11_validation.py
python3 validation/phase_11_validation.py --verbose
python3 validation/phase_11_validation.py --json
python3 validation/phase_10_validation.py
python3 validation/phase_9_validation.py
python3 validation/phase_8_validation.py
```

Expected upstream, if unchanged:

- Phase 10: inherited `145/147` approval-record-only condition
- Phase 9: `277/277 PASS`
- Phase 8: `119/119 PASS`

Phase 11 total may increase if a new independent oracle guard is registered. Update self-check totals honestly.

## Constraints

Do not modify substantive Phase 1–10 architecture.
Do not modify Phase 8/9/10 validators.
Do not modify Phase 9/10 approval records.
Do not modify Phase 11 architecture semantics.
No runtime, SQL, migrations, Supabase deployment, API, SDK, queue, worker, scheduler, event bus, agent, RAG, credentials, IAM, secrets, or live assignments.
No PR.
All Phase 11 artifacts remain `PROPOSED`.

Prefer changing only:

- `validation/phase_11_validation.py`
- `reviews/phase-11-late-decision-race-remediation.md`
- `reviews/phase-11-foundation-self-check.md` if totals/descriptions change

If fixing this requires architecture semantics to change, STOP and report rather than committing.

## Commit

Commit exactly:

`docs: remediate Phase 11 rendered scope identity and oracle guards`

Push to:

`origin architecture/phase-11-orchestrator`

## Response

Return exactly sections A–I:

A. REMEDIATION SUMMARY
B. RENDERED SCOPE DISCOVERY RULE
C. GUARDED IDENTITY CO-OCCURRENCE RULE
D. CLOSURE-ORACLE ANTI-VACUITY RULE
E. CONTROLLED PROBES / WEAKENINGS
F. VALIDATION
G. REGRESSION / FILES CHANGED
H. COMMIT / PUSH
I. NEXT STEP

Section I exactly:

`READY FOR FINAL PHASE 11 HUMAN-APPROVAL RE-AUDIT`
