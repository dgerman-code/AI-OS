# Phase 12 — MVP Foundation

Repository: `dgerman-code/AI-OS`

Branch: `implementation/phase-12-mvp`

Base approval commit: `b8fba92e03a4bc29c8f1bb4d894fb9efb45586cb`

Human-approved Phase 11 architecture baseline: `b4cc549680c87e465931b5c4a6825e34f3c3ced6`

## Objective

Begin Phase 12 as the first controlled implementation phase of AI-OS.

This is **not** permission to build the whole production platform. The objective is to produce a minimal, inspectable, provider-independent MVP foundation that proves the approved Phase 1–11 governance model can be represented and executed without collapsing its boundaries.

Do not create a pull request.

## Governing rule

Implementation must conform to the approved architecture. Do not redesign earlier phases from implementation convenience.

Preserve these separations exactly:

`ROLE != AGENT INSTANCE != MODEL != MODEL PROFILE != ROUTER != ORCHESTRATOR != WORKFLOW != WORKFLOW RUN != TASK != HANDOFF != REVIEW PROFILE != REVIEW INSTANCE != DECISION RIGHT != DECISION RECORD != KNOWLEDGE != CANONICAL RECORD != ARTIFACT != STORAGE RECORD != RUNTIME EVENT != CREDENTIAL != HUMAN AUTHORITY`

Also preserve:

- approval is never inferred;
- model output is never authority;
- router is not orchestrator;
- RLS / credentials / service identities are not governance authority;
- operational logs are not governance evidence;
- AI suggestion is not canonical knowledge;
- missing Decision Right blocks;
- timeout is not approval;
- recovery cannot weaken governance;
- cross-scope movement requires an approved Phase 6 / Phase 8 mechanism;
- human authority remains explicit.

## Important Phase 11 approval condition

Phase 11 was explicitly approved by human decision with validator hardening deferred.

The approval record is:

`reviews/phase-11-final-approval.md`

Do not falsify the assurance history. The final Phase 11 independent audit remained `FAIL`, harness credibility remained `MEDIUM`, and the architecture was nevertheless approved by explicit human decision because the remaining findings were confined to natural-language validator attachment edge cases.

Treat these as a Phase 12 assurance backlog, not as a reason to reopen Phase 11 architecture:

1. same-subject pronoun attachment after controlled connectors, e.g. `... but it is ...`;
2. contrastive forms such as `although` / `though` where earlier negation must not hide a later identity collapse;
3. false positives for genuinely new bare/proper-name subjects after coordinators;
4. eventual restoration of HIGH harness credibility.

Do not enter another endless NLP-regex expansion cycle. If hardening cannot be made structurally reliable with a bounded grammar, record the limitation and keep the approved invariant enforced at structured-data/runtime boundaries instead.

## Phase 12 scope

Work in two explicit tracks.

### Track A — MVP implementation foundation

Build only the minimum executable/reference implementation required to demonstrate the approved control model.

Create a small implementation layer with explicit typed/domain objects for, at minimum:

- Workflow Definition reference
- Workflow Run
- Task / Work Item / Attempt
- Assignment
- Agent Instance
- Review Instance
- Decision Request / Decision Record reference
- Model Invocation Request
- Routing Decision reference
- Gate state
- Execution Event
- Scope binding
- Human Intervention record

Names may be refined only if they preserve the approved identities and terminology.

The MVP should be able to execute one synthetic workflow locally/in-memory or through an equally non-production reference adapter and demonstrate:

1. run creation from a governed workflow definition;
2. explicit scope binding;
3. stage activation;
4. executor assignment without granting new authority;
5. router request creation distinct from routing decision;
6. model result recorded as AI-generated/suggested output rather than approval;
7. review request and review result as separate governed objects;
8. Decision Right absence causing BLOCKED / AUTHORITY_ABSENT rather than continuation;
9. a human decision record satisfying a gate only where the required right exists;
10. retry behavior that respects the approved retry class;
11. append-only execution events;
12. terminal completion only when governance posture permits it.

A second synthetic case must prove a prohibited path cannot continue, such as missing Decision Right, scope mismatch, failed independent review, or unresolved governance gate.

### Track B — implementation assurance

Add implementation-level checks that directly enforce the approved identities and governance contracts using structured objects rather than natural-language interpretation where possible.

Validator hardening from Phase 11 may be improved, but Phase 12 assurance should primarily shift critical invariants into deterministic structured checks, schema/type checks, state-transition checks, and executable tests.

Examples:

- Role ID cannot be used where Agent Instance ID is required;
- Model Profile cannot satisfy Review Instance or Decision Record fields;
- Router output cannot set gate state directly;
- missing Decision Right cannot transition to approved/continuing state;
- human-only decisions require explicit human authority reference;
- cross-scope transition requires an approved transfer/handoff reference;
- a model result cannot mutate canonical state directly;
- terminal completion requires permitted governance posture;
- retries cannot replay a non-replayable governed act automatically;
- execution event history is append-only in the reference implementation.

## Implementation constraints

Prefer the smallest standard-library or low-dependency implementation that makes the semantics explicit.

Do not add production infrastructure yet unless strictly required by an already approved contract.

Specifically, do **not** introduce without separate justification and review:

- production Supabase configuration;
- live database migrations;
- deployed APIs;
- cloud queues/workers;
- schedulers/event buses;
- provider SDK coupling in governance objects;
- secrets or credentials;
- live LLM calls;
- production IAM;
- RAG/embeddings;
- autonomous agents;
- background daemons;
- deployment configuration.

Use adapters/interfaces for external mechanisms where needed. A fake/stub/in-memory implementation is preferred for MVP proof.

## Required outputs

Create a coherent Phase 12 implementation package, not scattered experimental files.

At minimum produce:

1. `implementation/phase-12/README.md` — scope, non-scope, architecture mapping, how to run.
2. `implementation/phase-12/domain.py` or equivalent — explicit domain objects / enums / references.
3. `implementation/phase-12/orchestrator.py` or equivalent — minimal coordinator implementing approved semantics only.
4. `implementation/phase-12/adapters.py` or equivalent — provider/runtime boundaries with in-memory stubs.
5. `implementation/phase-12/examples/` — at least one successful governed workflow and one blocked workflow.
6. `implementation/phase-12/tests/` — deterministic tests for architecture invariants and state transitions.
7. `validation/phase_12_validation.py` — deterministic Phase 12 validator for package structure, forbidden dependencies/claims, and required assurance properties.
8. `reviews/phase-12-foundation-self-check.md` — producer self-check with exact test/validator results and known limitations.

If a different file split is materially cleaner, use it, but preserve the responsibilities above and explain the mapping.

## Required implementation behavior

The reference orchestrator may coordinate only. It must not:

- infer or manufacture approval;
- act as reviewer;
- act as Decision Right holder;
- accept risk;
- canonicalise knowledge by itself;
- relax routing constraints;
- substitute a model for a human gate;
- silently cross scopes;
- rewrite historical records;
- automatically retry non-replayable governed acts;
- treat operational success as governance completion.

Every state transition must be explicit and testable.

Prefer pure functions/state-transition functions where practical so invariants are inspectable.

## Tests required before completion

At minimum test:

- valid Workflow → Workflow Run creation;
- identity-type separation;
- scope bind and scope mismatch block;
- narrowing sub-run allowed, widening rejected;
- assignment does not grant review/decision authority;
- Router Request != Routing Decision;
- routing block remains a block;
- model output cannot satisfy review/decision/human gate;
- missing Decision Right blocks;
- timeout does not approve;
- late Review Result behavior remains distinct from late Decision Record behavior;
- retryable versus non-retryable governed acts;
- append-only event history;
- completion denied while WAITING/BLOCKED/governance-unclear;
- successful completion only after all required governed conditions are satisfied;
- structured identity-collapse attempts fail;
- Phase 11 deferred validator cases are either structurally covered or explicitly documented as text-layer limitations.

Add mutation/non-vacuity tests where they provide real value, but do not recreate an infinite natural-language fuzzing project.

## Regression gates

Run and report:

- Phase 12 tests;
- `validation/phase_12_validation.py` in default, verbose and JSON modes if supported;
- Phase 11 validator;
- Phase 10 validator;
- Phase 9 validator;
- Phase 8 validator.

Do not silently repair inherited Phase 10 approval-record validator behavior from Phase 12.

## Status and governance

All new Phase 12 implementation artifacts must begin as `PROPOSED` or implementation-equivalent non-approved status where status metadata exists.

Do not alter any prior human approval record.

Do not change approved Phase 1–11 semantics without stopping and reporting the conflict before implementation.

If implementation reveals an architectural contradiction, STOP and return a conflict report rather than changing the architecture to make the code easier.

## Final report format

Return exactly these sections:

### A. IMPLEMENTATION SUMMARY
What was built and why.

### B. ARCHITECTURE-TO-CODE MAPPING
Map Phase 11 identities/invariants to implementation objects and checks.

### C. MVP EXECUTION MODEL
Explain the executable/reference flow end to end.

### D. GOVERNANCE ENFORCEMENT
Show how authority, scope, review, decision, routing, retry and completion rules are enforced.

### E. DEFERRED VALIDATOR HARDENING
State what was structurally solved, what remains text-layer only, and why this does not alter approved architecture.

### F. TESTS / VALIDATION
Exact commands, counts and results.

### G. REGRESSION
Phase 11/10/9/8 results and any inherited known conditions.

### H. FILES CHANGED
Complete list.

### I. KNOWN LIMITATIONS
No hidden TODOs. Distinguish MVP limitation from architecture defect.

### J. COMMIT / PUSH
Commit SHA, message, branch, clean-tree confirmation, no PR.

### K. NEXT STEP
Return one of:

- `READY FOR INDEPENDENT PHASE 12 MVP AUDIT`
- `STOPPED — ARCHITECTURE CONFLICT FOUND`
- `STOPPED — IMPLEMENTATION BLOCKER FOUND`

## Commit

If all required work is complete and green, commit and push to `implementation/phase-12-mvp` with a message similar to:

`feat: add Phase 12 MVP foundation`

Do not create a PR.