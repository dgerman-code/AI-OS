# Claude Code Prompt — Final Four Phase 4 Prose Fixes

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-4-skill-registry`
Expected current branch state before this prompt commit: `edb9c93732312de35e050b9751cf5377b4f20250`

The final independent re-audit returned:
- FINAL VERDICT: FAIL
- RETIRED TAXONOMY: PASS
- PACK CARD CONSISTENCY: PASS
- DUPLICATE ACTIVATION: PASS
- COMPATIBILITY / AUTHORITY: PASS
- HUMAN APPROVAL: READY AFTER LISTED CHANGES

Only four stale prose/statistical statements remain. This is a **narrow prose reconciliation only**.

Do not alter Phase 3 Role Cards.
Do not alter mapping relationships, triggers, alternative sets, prohibitions or allowlists.
Do not add/remove/rename Skills, Specialisations or Packs.
Do not create new cards.
Do not start another normalization wave.
Do not change authority boundaries.
Do not create a PR.
Do not mark Phase 4 APPROVED or CANONICAL.

## Files to inspect

Primary target:
- `skills/mappings/wave-2-domain-completion-role-skill-mapping.md`

Also inspect for consistency only:
- `reviews/phase-4-wave-3-cross-domain-normalization.md`
- `reviews/phase-4-final-audit-remediation.md`
- `skills/master-skill-universe.md`

## Apply exactly these four fixes

### 1. Cross-role summary
Replace every active/stated current-value occurrence in the Wave 2 mapping file that still reports:
- 92 single-role IDs
- 263 used IDs
- 35.0%

with the audited current values:
- 93 single-role positive-use IDs
- 264 positive-use IDs
- 35.2%

Historical references may remain only if clearly labeled as historical and paired with the correct historical baseline. Do not leave an ambiguous unlabeled 92/263/35.0 statement.

### 2. Insurance / Risk Transfer sparse-core prose
Where current prose says the Insurance / Risk Transfer Specialist core is three, correct it to the actual current mapping count: **2 REQUIRED_CORE entries**.

If a sentence refers to a historical pre-merge count of three, label it explicitly as historical and state the current core is two.

Do not change the actual relationship block.

### 3. Software QA sparse-core prose
Where current prose says the Software QA / Test Automation Specialist core is two, correct it to the actual current mapping count: **3 REQUIRED_CORE entries**.

If a sentence refers to the earlier state with two, label it explicitly as historical / superseded by Wave 3 and state the current core is three.

Do not change the actual relationship block.

### 4. Specialisation count wording
Where Wave 3 / Wave 2 prose says “all 34 remaining active Specialisations” or otherwise risks presenting 34 as the universe count, clarify:
- 41 = active Specialisations in the Master Skill Universe
- 38 = Specialisation IDs in positive use across mappings (if that statistic is stated)
- 34 = the subset reviewed in that specific Wave 3 classification exercise / direct Wave 2 context, not the active universe total

Use wording that cannot be read as saying the active universe has 34 Specialisations.

## Validation

After editing, independently recompute / verify:

1. Wave 2 mapping total remains 676.
2. Relationship distribution remains 188 CORE / 230 RFC / 192 OPTIONAL / 56 ALTERNATIVE / 10 PROHIBITED.
3. Combined Wave 1 + Wave 2 total remains 823.
4. Positive-use IDs remain 264.
5. Single-role positive-use IDs remain 93 = 35.2%.
6. Insurance / Risk Transfer current REQUIRED_CORE count is 2 and prose says 2.
7. Software QA current REQUIRED_CORE count is 3 and prose says 3.
8. Active universe Specialisations remain 41.
9. No prose states or implies 34 is the active universe Specialisation count.
10. No mapping relationship line changed.
11. No trigger changed.
12. No allowlist changed.
13. Phase 3 Role Cards unchanged.
14. No Skill / Specialisation / Pack Card added or removed.
15. Retired taxonomy cleanup remains intact.
16. Pack Card reconciliation remains intact.
17. Duplicate activation evidence remains 20 / 14 / 10 / 36 / 56.
18. Compatibility remains 0 testable conflicts / 0 orphan allowlist entries.
19. All Phase 4 artifacts remain PROPOSED.
20. No PR created.

If any validation fails, stop and report rather than making broader changes.

## Commit / Push

If all 20 checks pass:

Commit exactly:
`docs: reconcile final Phase 4 prose statistics`

Push to:
`origin architecture/phase-4-skill-registry`

Do not create a PR.

## Required output

Return exactly:

### A. FOUR FIXES APPLIED
Describe the four prose/statistical corrections.

### B. MAPPING IMMUTABILITY
Confirm relationships/triggers/allowlists unchanged.

### C. STATISTICAL RECHECK
Report 676 / 823 / 264 / 93 / 35.2% and core counts 2 / 3.

### D. SPECIALISATION COUNT CLARIFICATION
Report 41 active universe Specialisations and explain what 34 refers to.

### E. REGRESSION CHECK
Retired taxonomy / Pack cards / duplicate activation / compatibility / authority.

### F. VALIDATION
Checks 1–20 PASS / FAIL.

### G. COMMIT / PUSH
Commit SHA and push result.

### H. NEXT STEP
Choose exactly:
- READY FOR HUMAN APPROVAL OF PHASE 4
- NOT READY

Do not claim approval itself.