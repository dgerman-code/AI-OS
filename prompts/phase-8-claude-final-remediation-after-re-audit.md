# Claude Code Prompt — Final Phase 8 Remediation After Re-Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-8-memory-canonical`
Current audited baseline: `4a20429c94e4c881a303a58b7fd62289a4131c26`
Phase 7 approval-record baseline: `c72ef0399b3c7c2f272711918803f7bc08c70084`

The final independent re-audit still returned **FAIL**.

This is a second, tightly bounded Phase 8 remediation pass. Fix only the remaining blockers and validation weaknesses identified by the re-audit. Do not redesign unrelated architecture.

Do NOT modify approved Phase 3–7 semantics.
Do NOT implement runtime, DB, API, UI, RAG, embeddings, model routing, agents, IAM, or storage.
Do NOT create a PR.
Do NOT mark Phase 8 APPROVED or CANONICAL.
All Phase 8 artifacts remain `PROPOSED`.

---

# 1. Remove organisational applicability leakage into PERSONAL

Re-audit finding:
`knowledge/scope-isolation-and-transfer.md` §7 still makes organisational canonical statements applicable inside the sibling `PERSONAL` branch, contradicting:
- approved scope graph;
- no-sideways-flow rule;
- governed-transfer rule;
- personal/organisational isolation rule.

Required fix:
- `PERSONAL` is a separate scope family and is **not a descendant of ORGANISATION**;
- no organisational canonical statement becomes applicable inside PERSONAL merely because the human is associated with the organisation;
- no PERSONAL item becomes applicable inside ORGANISATION by absorption;
- any intentional cross-family use requires explicit reference/import/governed transfer semantics already defined by Phase 8;
- no canonical status, Review satisfaction, authority, or applicability mode transfers across the PERSONAL/organisational-family boundary automatically;
- remove every wording that implies organisational canonical applicability inside PERSONAL;
- ensure all examples, templates, universe text, and validation match this.

Stress-test:
1. organisational travel policy visible to an employee's personal task;
2. user's preferred writing style used in an organisational deliverable;
3. organisational legal constraint relevant to a personal workflow;
4. personal preference used as organisational house style.

The architecture may permit **reference/use** where explicitly selected by task governance, but it must never call that inherited applicability or canonical propagation.

Report applicability leakage after fix: required `0`.

---

# 2. Normalize `APPROVED_STATUS_WITHDRAWAL` to the governance-state model

Re-audit finding:
`knowledge/canonical-promotion-governance.md` says `APPROVED_STATUS_WITHDRAWAL` returns the item to `REVIEWED` or `DRAFT`, while the state model permits withdrawal only to `RETRACTED`.

Resolve the contradiction at the semantic level.

Required design:
- never “rewind history” from APPROVED to an earlier state as if approval had not happened;
- an explicitly withdrawn/invalidated approval must preserve the fact that approval once existed;
- choose one coherent representation and use it everywhere.

Preferred architecture direction unless existing approved semantics force otherwise:
- `APPROVED` remains a historical governance state that occurred;
- withdrawal of an approval creates a new governed terminal/non-applicable state such as `RETRACTED` (or a specifically justified new distinct state if truly necessary);
- a replacement/revised claim enters a new lifecycle as a new linked item/version starting at `DRAFT` or another appropriate initial state;
- the original approved item is not relabelled back to `DRAFT`/`REVIEWED`;
- `decision.canonical_knowledge_status_change` acts on the existing governed state/effect, not on history rewriting.

If `RETRACTED` is used for both formerly APPROVED and formerly CANONICAL material, define the distinction through subject/effect metadata rather than ambiguous state names.

Update:
- knowledge-state model;
- canonical-promotion governance;
- common constraints;
- templates;
- universe;
- exemplars if affected;
- validation harness.

Required outcome: no contradictory permitted transition remains.

---

# 3. Correct active universe / inventory inconsistencies

Re-audit found live factual inconsistencies in `knowledge/master-knowledge-governance-universe.md`:
- still says **three-axis** where the model is now four-axis;
- says **28 inherited constraints** where the standard now contains 29;
- retains **“seven stores”** reasoning after the memory-class model was reduced to six classes.

Required fix:
- make the universe reflect the actual current architecture exactly;
- do not preserve stale counts or rationale for historical convenience;
- where historical change matters, move it to remediation/history notes, not active normative inventory;
- verify all counts mechanically from the files where feasible.

Search for stale references across all Phase 8 files, including:
- `three-axis` / `three axes`;
- `seven classes` / `seven stores` / `7 classes`;
- `28 constraints`;
- old memory-class aliases;
- old freshness wording;
- old AI conversion wording.

Distinguish historical remediation text from active normative declarations.

---

# 4. Fix exemplar 2 and exemplar 3

## Exemplar 2 — Project assumption

Re-audit finding: still describes itself as proving a **three-axis model**.

Required fix:
- update it to the current four-axis model;
- preserve its substantive lesson: `ASSUMPTION + APPROVED` remains an assumption;
- include origin where relevant;
- do not alter its non-canonical status merely to match the model.

## Exemplar 3 — Financial calculation

Re-audit finding: declares `CALCULATION + CANONICAL` but lacks the mandatory applicability mode.

Required fix:
- add exactly one applicability mode appropriate to the exemplar;
- justify why that mode is correct for the financial calculation's scope/use;
- ensure no unintended descendant propagation occurs;
- preserve source-input versioning and re-derivation semantics.

All eight exemplars must pass after remediation.

---

# 5. Strengthen validation harness materially

Re-audit result:
`python3 validation/phase_8_validation.py` reports `95/95 PASS`, but credibility only **MEDIUM**.

Specific weaknesses to fix:

### 5.1 No-sideways-flow check
Current check is presence-oriented and did not detect the live ORGANISATION -> PERSONAL leakage.

Replace/add semantic checks that inspect the actual PERSONAL/ORGANISATION rules and fail if:
- organisational applicability is declared inside PERSONAL by inheritance/propagation;
- PERSONAL is treated as a descendant of ORGANISATION;
- cross-family canonical propagation is allowed without governed transfer/reference.

### 5.2 State-transition consistency
Add cross-file parsing/checks that compare:
- permitted governance-state transitions in `knowledge-state-model.md`;
- status-change effects in `canonical-promotion-governance.md`;
- common constraints;
- templates.

The harness must fail if one file says APPROVED withdrawal -> REVIEWED/DRAFT while the state model says only RETRACTED.

### 5.3 Universe/inventory consistency
Add deterministic checks for:
- four-axis wording;
- actual number of memory classes;
- actual number of inherited/common constraints;
- absence of stale normative “seven stores/classes” statements;
- current counts derived rather than hand-maintained where practical.

### 5.4 Canonical exemplar applicability
Current selector excludes canonical records lacking `Canonical ID`, allowing a canonical exemplar with no applicability mode to escape validation.

Fix discovery so **every exemplar whose governance state/status is CANONICAL** is validated for:
- exactly one applicability mode;
- allowed token;
- no missing applicability metadata.

Do not select based on presence of a field whose absence is itself the defect.

### 5.5 Remove vacuous checks
Re-audit found an implementation check containing `or True`.

Remove all unconditional-pass constructs, including:
- `or True`;
- equivalent tautologies;
- checks whose failure branch is unreachable;
- hard-coded PASS counters disconnected from content.

Search the whole validation harness for vacuous conditions.

### 5.6 PR detection
Current check only inspects local `.git/PULL_REQUEST`, which is not a credible open-PR test.

Because the validator is offline/local and must not require network:
- do **not** pretend it can prove remote PR count;
- reclassify local validator scope honestly: it may prove no PR artifact/action was created locally, but remote open-PR status must be independently checked by audit tooling/GitHub API;
- remove any claim that local Python alone proves remote PR count = 0;
- self-check/remediation record must distinguish local deterministic checks from external repository-state checks.

### 5.7 Validation count
Do not preserve `95` for cosmetic reasons.

After adding/removing checks:
- report the actual deterministic check count;
- run with `--verbose` and normal mode;
- if JSON mode exists, verify it reports the same total;
- exit non-zero on any failure.

The harness credibility target is **HIGH**.

---

# 6. Re-adjudicate open questions 2, 3, 4

The re-audit still marked questions #2, #3, #4 as MUST RESOLVE BEFORE HUMAN APPROVAL.

After fixes above, independently determine whether each is now actually resolved:

2. Can one canonical subject have multiple simultaneously valid scoped statements?
- Must explicitly cover PERSONAL isolation and scope-family boundaries.

3. How is canonicality/applicability inherited across scopes, if at all?
- Canonical status must remain non-inherited;
- applicability modes must exclude sideways PERSONAL leakage.

4. How do `decision.canonical_knowledge_promotion` and `decision.canonical_knowledge_status_change` normalize?
- Must now include a state-transition-consistent APPROVED withdrawal semantics.

Do not mark RESOLVED merely because text exists.

---

# 7. Full regression recheck

After fixes, re-run all important Phase 8 invariants:
- scope graph exact vs approved baseline;
- PERSONAL isolation;
- no upward/sideways leakage;
- explicit applicability mode;
- mandatory wider constraints non-overridable;
- no canonical memory-class duplication;
- four-axis model everywhere normative;
- AI adoption creates new linked item;
- no epistemic type conversion by authority;
- canonical status-change ID preserves APPROVED and CANONICAL upstream meaning;
- governance-state transitions internally consistent;
- freshness item facts vs use verdicts separated;
- materiality rule consistent;
- conflict/provenance intact;
- sensitivity orthogonal;
- artifact != knowledge;
- retrieval != authority;
- all canonical exemplars have applicability mode;
- all Phase 8 artifacts remain PROPOSED;
- Phase 3–7 approved files/semantics unchanged;
- no runtime implementation.

Also externally verify with GitHub state where available:
- open PR count;
- branch HEAD after push.

Do not fold external repository checks into the offline validation count unless they are actually executed.

---

# 8. Remediation record update

Update:
`reviews/phase-8-foundation-audit-remediation.md`

Add a clearly separated **Second Re-Audit Remediation** section containing:
- remaining findings from the second independent audit;
- exact fixes;
- validation changes;
- final deterministic validation command and count;
- external checks performed separately;
- explicit statement Phase 8 remains PROPOSED.

Do not erase the first remediation history.

---

# 9. Commit / push

If and only if all checks pass, commit exactly:

`docs: close remaining Phase 8 re-audit gaps`

Push to:

`origin architecture/phase-8-memory-canonical`

Do not create a PR.

---

# Required final output

Return exactly:

### A. FINAL REMEDIATION SUMMARY
Each remaining blocker and final status.

### B. PERSONAL / SCOPE ISOLATION
Exact corrected rule; leakage count after fix.

### C. GOVERNANCE-STATE WITHDRAWAL MODEL
Exact APPROVED withdrawal transition/effect and why it preserves history.

### D. UNIVERSE / INVENTORY CONSISTENCY
Four-axis status, constraint count, memory-class count, stale-reference scan result.

### E. EXEMPLARS
All eight PASS/FAIL; explicitly call out exemplar 2 and 3 fixes.

### F. VALIDATION HARNESS
Files changed; exact command; exact deterministic PASS/FAIL count; vacuous checks removed; semantic checks added; local-vs-external verification boundary.

### G. OPEN QUESTIONS
All 12 dispositions; highlight #2, #3, #4.

### H. REGRESSION
Phase 3–7 changes; Phase 8 status; runtime status.

### I. EXTERNAL REPOSITORY CHECKS
Branch HEAD, push result, clean tree, open PR status if checked through GitHub/remote tooling.

### J. FILES CHANGED
Exact files and purpose.

### K. COMMIT / PUSH
Commit SHA, exact message, push result, remote HEAD.

### L. NEXT STEP
Choose exactly one:
- READY FOR FINAL PHASE 8 APPROVAL RE-AUDIT
- NOT READY

Do not claim Phase 8 approval.