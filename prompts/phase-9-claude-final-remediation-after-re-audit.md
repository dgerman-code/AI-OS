# Claude Code Prompt — Final Phase 9 Remediation After Re-Audit

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-9-model-registry-router`
Current audited remediation baseline: `69a119f59c8fc1687944ed27df594dc809aadf78`
Phase 8 approval-record baseline: `00fb92e1b2dd1209ee2f69550c5962158b881e3e`

The final independent Phase 9 re-audit still returned **FAIL**, but only a small number of tightly bounded blockers remain.

Fix only these remaining Phase 9 blockers and the validation gaps that allowed them through.

Do NOT redesign unrelated Phase 9 architecture.
Do NOT modify approved Phase 3–8 semantics.
Do NOT implement runtime, SDKs, API calls, secrets, DB, UI, RAG, agents, orchestration, queues, monitoring, evaluation service or deployment.
Do NOT create real vendor/model/provider/deployment profiles.
Do NOT create a PR.
Do NOT mark Phase 9 APPROVED or CANONICAL.
All Phase 9 artifacts remain `PROPOSED`.

---

# 1. Resolve Underlying Model Release vs Registry Profile Version contradiction

Re-audit finding:
The six-layer identity stack is good, but `models/model-lifecycle-and-versioning.md` §4 still says an underlying provider/model change becomes a Registry Profile Version change, contradicting the rule that one Model Profile describes one underlying release.

Required final semantics:

## 1.1 Immutable identity boundary

A **Model Profile identity is bound to one Underlying Model Release**.

Therefore:
- if the underlying model release changes materially, this is **not** merely a new Registry Profile Version;
- it requires a **new Model Profile identity** linked by `supersedes` / `superseded-by` or equivalent;
- a Registry Profile Version may change only the governed record about the **same underlying release**, e.g. metadata correction, new evidence, new limitation, refreshed evaluation, alias/mapping updates that do not change the underlying release identity.

## 1.2 Provider-side changes

Distinguish clearly:
- provider marketing alias rename -> Provider Offering Mapping update / alias update, same Model Profile if underlying release proven unchanged;
- provider contractual/data-handling change -> Provider/Deployment profile version change, not Model Profile identity change unless model behavior/release itself changed;
- provider backend behavior materially changes but exact release cannot be proven unchanged -> **new Model Profile identity or explicit unresolved identity conflict**, never silently a registry-profile-version bump;
- deployment configuration/residency change -> Deployment Profile version/new Deployment Profile as appropriate, not Model Profile release change;
- AI-OS metadata/evidence correction -> Registry Profile Version change only.

## 1.3 Historical reproducibility

Routing Decision must preserve:
- Model Profile stable ID;
- Registry Profile Version;
- Underlying Model Release identity;
- Provider Offering Mapping/version/reference;
- Provider Profile version;
- Deployment Profile version.

Search all Phase 9 normative files for any wording that says or implies that a changed underlying release remains the same Model Profile with only a Registry Profile Version increment. Remove the contradiction everywhere.

Re-adjudicate open question #1 only after the normative rule is consistent.

---

# 2. Remove invented Phase 6 / Phase 7 registry references from Exemplar 9

Re-audit finding:
Exemplar 9 references:
- nonexistent `decision.model_capability_threshold_exception`;
- nonexistent `review.software_security_change`.

This is a blocking cross-registry integrity defect.

## 2.1 Inspect approved upstream registries first

Read the approved Phase 6 Review universe/cards and Phase 7 Decision Rights universe/cards at or before the approved baselines.

Do NOT invent or rename IDs.

Determine whether an **existing approved** Decision Right actually covers the specific act of adjusting a model capability threshold for routing.

Determine whether an **existing approved** Review Profile is actually applicable to the exemplar.

## 2.2 Use an existing approved ID only if the semantics truly fit

Do not force-fit a broad Right just because its name sounds nearby.

For example, if `decision.exceptional_progression` exists upstream, inspect its approved semantics. Use it only if it legitimately authorises the exact bounded progression/exception effect required here and does not create authority beyond Phase 7.

If no approved Right currently covers this routing constraint exception, the architecture must say so explicitly.

## 2.3 Preferred safe outcome if no suitable approved Right exists

If no exact suitable Phase 7 Right exists:
- Exemplar 9 must **not execute the exception**;
- it should demonstrate the full pre-exception sequence up to the governance boundary;
- original candidate remains ineligible;
- exceptionability classification is checked;
- system discovers `NO_APPLICABLE_DECISION_RIGHT` / equivalent;
- Routing Decision outcome is `BLOCKED_FOR_ROUTING` or `ESCALATED_FOR_GOVERNANCE_DESIGN`;
- exemplar records that a future, explicitly carded Phase 7 Right would be required before an adjusted requirement context can exist;
- no fabricated Review Profile should be referenced;
- if review is needed conceptually but no approved profile matches, state `REVIEW_PROFILE_NOT_BOUND_IN_PHASE_9` / equivalent and keep it non-executable.

This is preferable to inventing upstream governance.

## 2.4 Architecture rule

Add a general cross-registry integrity rule:
- every `decision.*` reference in Phase 9 must resolve to an approved Phase 7 candidate/card or be explicitly labelled a **future/unresolved reference** that cannot be executed;
- every `review.*` reference must resolve to an approved Phase 6 profile/candidate or be explicitly non-executable/deferred;
- unresolved/future governance IDs must never appear as though already exercisable.

This rule must apply to templates, exemplars and Routing Decision records.

Re-adjudicate open question #10 after this correction.

---

# 3. Remove stale active reference to deleted privacy capability

Re-audit finding:
`capability.privacy_sensitive_suitability` was removed from the declared taxonomy but remains actively referenced in `models/model-capability-taxonomy.md` §4.

Required:
- remove all active normative references to this deleted capability ID;
- if historical/remediation text mentions it, mark it clearly historical only;
- privacy/data-handling eligibility must remain owned by Provider/Deployment evidence + routing constraints, not Model Capability;
- mechanically scan all active Phase 9 normative documents for the removed capability token and any alias/equivalent that recreates the same governance overlap.

Required active reference count after remediation: `0`.

---

# 4. Correct all stale active counts and inventory prose

Re-audit found 10 inventory inconsistencies.

At minimum correct:
- actual capability families = **23**;
- actual eligibility constraint IDs = **27**;
- actual preferences = **9**;
- actual common constraints = **43**;
- lifecycle states = **6**;
- evidence classes = **6**;
- templates = **5**;
- exemplars = **9**;
- Routing Act Requirements = **3**;
- Routing Decision required elements = **31**;
- fix any text saying 24 capability families, 24 or 22 hard constraints, 8 preferences, 33 common constraints;
- fix the heading/text `Two things this architecture cannot express` if it lists three things.

## 4.1 Derive counts where feasible

Do not hand-maintain numbers where the validation harness can derive them from authoritative tables/files.

The universe should either:
- state mechanically verified counts; or
- omit a brittle count if it adds no architectural value.

## 4.2 Scan all active normative prose

Search for stale numbers and obsolete terminology across:
- master architecture;
- taxonomy;
- universe;
- standards;
- templates;
- review/self-check files if they make active claims.

Historical audit/remediation records may preserve old counts only when clearly labelled historical.

Required active inventory inconsistency count after remediation: `0`.

---

# 5. Strengthen validation harness for the exact misses

Current harness `204/204 PASS` is still only MEDIUM credibility because it missed material semantic defects.

Add deterministic validation for all remaining classes of failure.

## 5.1 Cross-registry ID validation

Parse all Phase 9 active references matching `decision.*` and `review.*`.

For each:
- resolve against approved Phase 7 / Phase 6 registries/cards/candidate universes;
- PASS if the ID exists and the reference is semantically allowed;
- OR PASS if explicitly marked future/unresolved/non-executable and the surrounding semantics block execution;
- FAIL if an unknown ID is presented as exercisable/available.

Do not merely maintain a hand-written allowed list if authoritative upstream files can be parsed.

## 5.2 Model identity/version consistency

Add cross-file checks that fail if:
- one Model Profile is said to represent one underlying release in one place;
- but another place permits an underlying release change as only a Registry Profile Version increment.

Check all normative Phase 9 docs for equivalent contradictory wording.

## 5.3 Removed capability references

Derive declared capability IDs from the taxonomy and fail if any active normative Phase 9 file references an undeclared `capability.*` ID, unless explicitly marked historical/non-active.

This must catch `capability.privacy_sensitive_suitability`.

## 5.4 Inventory counts

Derive and cross-check:
- capability count;
- lifecycle primary-state count;
- eligibility constraint count;
- preference count;
- act-requirement count;
- common-constraint count;
- evidence-class count;
- template count;
- exemplar count;
- Routing Decision element count.

Fail on contradictory active prose/counts.

## 5.5 Heading/list cardinality

Add at least a bounded check for inventory text where a heading claims N items and the immediately governed list/table has a different count, especially the `Two things ...` / three-item defect.

## 5.6 Exemplar 9 governance integrity

Validation must fail if Exemplar 9:
- references a nonexistent approved Decision Right as exercisable;
- references a nonexistent Review Profile as though bound;
- marks a candidate eligible before a valid governance act;
- creates adjusted requirements without a real approved Right or an explicit non-executable future boundary;
- confuses model diversity with reviewer independence.

## 5.7 Keep existing strong checks

Preserve:
- Candidate Universe checks;
- multi-label sensitivity checks;
- residency checks;
- exceptionability checks;
- fallback ordering;
- act requirement separation;
- policy-owned preference order;
- Phase 3–8 regression checks;
- no runtime checks;
- all Phase 9 artifacts PROPOSED.

Do not preserve `204` cosmetically. Report actual deterministic total.

Run:
- Phase 9 harness normal/verbose/JSON;
- injected failure if practical;
- Phase 8 harness and preserve `119/119 PASS`.

Target credibility: HIGH.

---

# 6. Re-adjudicate open questions #1 and #10

The final re-audit still marked:
- #1 MUST RESOLVE BEFORE HUMAN APPROVAL;
- #10 MUST RESOLVE BEFORE HUMAN APPROVAL.

After fixes:

## Question 1 — Model Profile identity
Must be RESOLVED only if the release/profile-version rule is globally consistent and no runtime guess remains.

## Question 10 — fallback / degraded fallback / exception
Must be RESOLVED only if:
- ordinary fallback is executable under Phase 9 policy;
- governed exception path requires an actually applicable approved Phase 7 Right;
- absence of such Right blocks rather than invents governance;
- future right carding is explicitly a Phase 7 governance extension, not silently created by Phase 9.

Re-adjudicate all 17 questions for completeness, but do not disturb already-resolved semantics without cause.

---

# 7. Update remediation record

Update:
`reviews/phase-9-foundation-audit-remediation.md`

Add a clearly separated **Second Re-Audit Remediation** section with:
- exact remaining blockers;
- fixes;
- cross-registry integrity result;
- inventory correction result;
- validation total;
- open-question re-adjudication;
- Phase 8 validation result;
- explicit statement Phase 9 remains PROPOSED;
- external remote checks separate from offline harness.

Preserve the prior remediation history.

---

# 8. Regression boundary

Prove against `00fb92e1b2dd1209ee2f69550c5962158b881e3e`:
- Phase 3 approved Role changes = 0;
- Phase 4 Skills = 0;
- Phase 5 Workflows = 0;
- Phase 6 Handoff/Review = 0;
- Phase 7 Decisions = 0;
- Phase 8 Knowledge/Canonical semantics = 0;
- Phase 8 validator remains unchanged unless a strictly necessary tooling-only correction is found and explicitly justified;
- Phase 9 changes only its architecture/models/exemplars/validation/review evidence;
- no runtime implementation;
- no real vendor/model/provider/deployment profiles;
- no PR.

---

# 9. Commit / push

If and only if all remediation checks pass, commit exactly:

`docs: close remaining Phase 9 re-audit gaps`

Push to:

`origin architecture/phase-9-model-registry-router`

Do not create a PR.

---

# Required final output

Return exactly:

### A. FINAL REMEDIATION SUMMARY
Each remaining blocker and final status.

### B. MODEL IDENTITY / VERSIONING
Exact immutable release/profile rule; provider/backend/alias cases; identity ambiguity count after fix.

### C. CROSS-REGISTRY GOVERNANCE REFERENCES
All `decision.*` and `review.*` refs used by Phase 9; whether they resolve; Exemplar 9 final executable/blocked semantics.

### D. CAPABILITY TAXONOMY CLEANUP
Removed capability references; undeclared active capability-ref count.

### E. INVENTORY / COUNTS
Mechanically derived final counts; active inconsistency count.

### F. EXEMPLAR 9
Final sequence and why it no longer invents upstream governance.

### G. OPEN QUESTIONS
All 17 dispositions; highlight #1 and #10.

### H. VALIDATION
Exact command/result/count; cross-registry checks; identity checks; capability-ref checks; inventory checks; credibility self-assessment; Phase 8 harness result.

### I. REGRESSION
Phase 3–8 changes; Phase 9 status; runtime/profile/PR status.

### J. FILES CHANGED
Exact files and purpose.

### K. COMMIT / PUSH
Commit SHA, exact message, push result, remote HEAD, clean-tree status.

### L. NEXT STEP
Choose exactly one:
- READY FOR FINAL PHASE 9 APPROVAL RE-AUDIT
- NOT READY

Do not claim Phase 9 approval.