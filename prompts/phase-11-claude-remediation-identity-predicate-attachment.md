# Phase 11 — Targeted Remediation: Identity Predicate Attachment

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-11-orchestrator`
Current audited baseline: `fdc337efb57e4b7b0233a1d6208d1f998f818d3f`

## Purpose

Apply one narrow remediation for the only remaining Phase 11 blocker from the latest independent audit: the identity-collapse validator does not bind separation/negation and proposition structure to the guarded pair’s actual positive identity predicate.

Do **not** redesign Phase 11 architecture. Do **not** expand this into a new NLP system. Do **not** modify `architecture/` or `orchestration/` unless an unavoidable architecture defect is found; if so, STOP and report instead of changing them.

The architecture is otherwise passing. The target is validator enforcement and harness credibility only.

## Audit finding to close

The following positive identity collapses currently evade detection and MUST be rejected:

- `A Role is not merely a label but is an Agent Instance.`
- `A Role remains temporary but is an Agent Instance.`
- `A Role is operational today and is an Agent Instance.`
- `The Router handles dispatch but is the Orchestrator.`
- `A Decision Right is documented and is a Decision Record.`

Root cause: an unrelated earlier negation, adjective, or coordinated predicate is being treated as sufficient evidence of separation or as a proposition break, even though the later predicate positively equates the guarded pair.

## Required rule

For every guarded identity pair co-occurring in a rendered normative proposition:

1. identify the predicate that actually relates the first guarded term to the second guarded term;
2. any separation/negation evidence must govern **that same predicate / pair relation**;
3. an earlier unrelated negation, adjective, property, or coordinated predicate MUST NOT suppress a later positive identity relation;
4. `but`, `and`, coordination, or an earlier predicate MUST NOT be treated as a safe proposition boundary when a later clause still positively predicates the second guarded term of the first;
5. if the actual relation between the guarded pair is not proven to be an allowed separation or approved safe relation, fail closed and report an offence.

Do not solve this by merely adding the five examples or a vocabulary of equivalent phrases. Fix predicate attachment / clause ownership structurally inside the existing controlled grammar.

## Required positive controls

The five audit examples above must be detected as collapses.

Add additional independent contrastive cases, including at minimum:

- unrelated negation before a later positive identity predicate;
- benign property before `but is <guarded-term>`;
- benign property before `and is <guarded-term>`;
- coordinated verb before a later identity copula;
- two guarded terms in genuinely separate propositions that must remain non-offences;
- explicit denial where the negation actually governs the identity predicate and must remain safe.

Examples of safe controls that should stay safe where semantically appropriate:

- `A Role is not an Agent Instance.`
- `The Router is distinct from the Orchestrator.`
- `A Role remains temporary, and the runtime creates an Agent Instance.`
- existing corpus relations already accepted by the controlled grammar.

## Harness requirements

Add negative controls / controlled weakenings proving the repaired logic is non-vacuous.

At minimum, mutations that MUST produce non-zero exit:

1. restore the current behaviour where any earlier negation suppresses the pair offence;
2. treat `but` as an unconditional safe boundary even when the later clause positively identifies the pair;
3. treat `and` as an unconditional safe boundary in the same way;
4. skip coordinated predicates before a later identity copula;
5. bypass the identity document scan;
6. vacuous boolean mutation (`or True` or equivalent).

Keep the existing rendered-text, scope, closure-oracle, stale-Decision, authority, state, retry, concurrency, provenance, and upstream regression guards intact.

## Validation expectations

Run:

- `python3 validation/phase_11_validation.py`
- `python3 validation/phase_11_validation.py --verbose`
- `python3 validation/phase_11_validation.py --json`
- `python3 validation/phase_10_validation.py`
- `python3 validation/phase_9_validation.py`
- `python3 validation/phase_8_validation.py`

Expected inherited upstream state remains:

- Phase 10: `145/147` due only to the known approval-record condition;
- Phase 9: `277/277 PASS`;
- Phase 8: `119/119 PASS`.

If Phase 11 total changes, update only the relevant Phase 11 review/self-check records accurately.

## Change scope

Preferred changed files only:

- `validation/phase_11_validation.py`
- `reviews/phase-11-late-decision-race-remediation.md`
- `reviews/phase-11-foundation-self-check.md` only if totals/group counts change

No PR.

Commit message:

`docs: remediate Phase 11 identity predicate attachment`

## Required final report

Return sections A–I:

A. REMEDIATION SUMMARY
B. IDENTITY PREDICATE-ATTACHMENT RULE
C. VALIDATOR REPAIR
D. CONTROLLED PROBES / WEAKENINGS
E. VALIDATION
F. REGRESSION
G. FILES CHANGED
H. COMMIT / PUSH
I. NEXT STEP

`I` should be `READY FOR FINAL PHASE 11 HUMAN-APPROVAL RE-AUDIT` only if all targeted findings are closed and the harness is again credibly fail-closed.
