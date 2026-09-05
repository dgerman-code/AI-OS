# Claude Code Prompt — Phase 3 Remediation After Codex Audit

Status: WORKING EXECUTION INSTRUCTION — NOT CANONICAL

Repository: `dgerman-code/AI-OS`
Branch: `architecture/phase-3-role-registry`

You are applying the minimum remediation required by the independent Codex Phase 3 audit.

Do not redesign the architecture.
Do not add first-class roles.
Do not mark Phase 3 APPROVED or CANONICAL.
Do not create Review Profile Registry or Decision Rights Register yet.
Do not change the €50m project-criticality policy.

Read first:
- `roles/master-role-universe.md`
- `roles/_templates/role-card-template.md`
- `roles/_standards/common-role-constraints.md`
- `architecture/registry-separation.md`
- `architecture/project-criticality-policy.md`
- all current Role Cards

Then apply the following changes exactly, unless a repository-wide search proves a referenced ID is used differently than stated. If so, stop and report before changing that item.

## 1. Fix HIGH finding B1 — external API / integration contract publication

File:
`roles/digital-product-software-data/solution-architect.md`

For `artifact.integration_contract_specification`:
- change `Independent Review Required` to `yes where external parties consume the contract`;
- change `Decision Right Reference` from `none` to `decision.api_contract_publication`.

In `## Human Decision Gates` add `decision.api_contract_publication`.

Do not change the Solution Architect professional scope.

## 2. Fix HIGH finding B2 — lender-facing coverage-gap submission

File:
`roles/economics-finance-transaction/insurance-risk-transfer-specialist.md`

For `artifact.coverage_gap_analysis`:
- change `Decision Right Reference` from `none` to `decision.lender_engagement`.

In `## Human Decision Gates` add `decision.lender_engagement`.

Keep the existing independent review requirement for lender-facing use.

## 3. Normalize Role ID now, before downstream registries exist

Rename:
`role.sales_business_development`
→
`role.sales_business_development_specialist`

Update the Identity field in:
`roles/strategy-business/sales-business-development-specialist.md`

Update every repository reference to the old Role ID, including at minimum the Adjacent / Boundary Role references in Marketing / Growth and Customer / CRM.

Do not rename the file or Role Name.

After replacement, repository-wide search for `role.sales_business_development` must return zero exact old-ID references.

## 4. Normalize Review Profile IDs

Apply these mappings repository-wide across Role Cards only:

- `review.independent_financial_model_review` → `review.financial_model`
- `review.technical` → `review.engineering_technical`
- `review.commercial` → `review.commercial_structure`

Do not alter:
- `review.factual_evidence`
- `review.financial_evidence`
- `review.evidence_integrity_provenance`
- `review.commercial_claims`
- `review.architecture`
- `review.data_architecture`

Do not create review profile files yet.

## 5. Normalize Decision Rights IDs

Apply these mappings repository-wide across Role Cards only:

- `decision.production_change` → `decision.production_release`
- `decision.eu_application_submission` → `decision.granting_authority_submission`
- `decision.budget_commitment` → `decision.budget_approval`
- `decision.production_release_scope` → `decision.release_scope_approval`
- `decision.emergency_change` → `decision.emergency_production_change`
- `decision.assessment_approval` → `decision.learning_assessment_approval`

Do not merge materially distinct IDs such as:
- `decision.production_infrastructure_change`
- `decision.production_database_migration`
- `decision.security_risk_acceptance`
- `decision.risk_acceptance`
- `decision.canonical_knowledge_promotion`
- `decision.canonical_knowledge_status_change`

## 6. Remove the overly broad Project / Delivery Lead catch-all decision right

File:
`roles/portfolio-programme-project/project-delivery-lead.md`

The role explicitly Does Not Own external submission, publication, deployment, filing or binding commitment. Therefore the integrated package itself must remain an internal delivery artifact; the actual external act belongs to the consuming workflow / specialist role and its specific human Decision Right.

For `artifact.integrated_delivery_package`:
- change `Decision Right Reference` from `decision.external_submission_or_commitment` to `none; external act must resolve to the consuming workflow's specific decision.<id>`;
- change `Transmitting Act` to `none; external transmission is a downstream workflow act`;
- change `Reversibility after Transmitting Act` to `REVERSIBLE while retained as an internal package; downstream external act has its own reversibility classification`.

In `## Human Decision Gates`:
- remove `decision.external_submission_or_commitment`;
- after repository-wide decision normalization, retain `decision.workflow_scope_approval` and `decision.production_release` only where applicable;
- add a sentence that any external submission / publication / deployment / filing / binding commitment must resolve to the specific decision right owned by the consuming workflow and may not use a generic catch-all.

Repository-wide search for `decision.external_submission_or_commitment` must return zero references after this change.

Do NOT replace it with another generic catch-all ID.

## 7. Template-label conformance cleanup

In these two reference cards only:
- `roles/portfolio-programme-project/knowledge-evidence-steward.md`
- `roles/strategy-business/sales-business-development-specialist.md`

Change the Minimum Input Knowledge State label to the exact template label:
`Decision-grade output minimum:`

Preserve the existing substantive text after the label.

Do not weaken the current requirements.

## 8. Capability Domain conformance cleanup

File:
`roles/portfolio-programme-project/knowledge-evidence-steward.md`

Change:
`Capability Domain: Portfolio / Programme / Project Governance / Knowledge Governance`

to:
`Capability Domain: Portfolio / Programme / Project Governance`

Do not change the role's purpose or knowledge-governance scope. This is classification conformance to Master Role Universe only.

## 9. Product scope decision clarification

File:
`roles/digital-product-software-data/product-manager-business-analyst.md`

After mapping `decision.production_release_scope` → `decision.release_scope_approval`, preserve both:
- `decision.product_scope_approval` for approval of the product / feature requirements scope;
- `decision.release_scope_approval` for approval of which already-defined scope enters a specific release.

Make the distinction explicit in the relevant artifact descriptions / Decision Right references if necessary, without changing professional scope.

Do not collapse the two rights.

## 10. Folder slug rule documentation

Create:
`architecture/role-folder-conventions.md`

Status must be PROPOSED.

Document only this rule:
- Role folders use stable kebab-case capability-domain slugs.
- A folder slug may be a shortened but unambiguous form of the Master Role Universe domain name.
- Canonical semantic classification is the Role Card `Capability Domain` field and the Master Role Universe, not the folder slug.
- Existing slugs, including `strategy-business`, `legal-compliance`, `project-development-technical-commercial`, and `knowledge-documentation-disclosure`, are accepted and should not be renamed merely for textual symmetry.

No database or implementation design.

## 11. Adjacency asymmetry

Do NOT attempt to make all Adjacent / Boundary Role references symmetric.

Only validate:
- zero dangling `role.<id>` references;
- zero self-references;
- the Sales / BD ID rename has been propagated.

Adjacency remains advisory and optional; workflow binding does not depend on reciprocal adjacency.

## Required validation after changes

Run a repository-wide audit and report:

1. 59 approved roles / 59 Role Cards / 59 unique Role IDs.
2. Zero references to:
   - `role.sales_business_development` (old exact ID)
   - `review.independent_financial_model_review`
   - `review.technical`
   - `review.commercial`
   - `decision.production_change`
   - `decision.eu_application_submission`
   - `decision.budget_commitment`
   - `decision.production_release_scope`
   - `decision.emergency_change`
   - `decision.assessment_approval`
   - `decision.external_submission_or_commitment`
3. Confirm `solution-architect.md` external integration contract publication is gated by `decision.api_contract_publication`.
4. Confirm `insurance-risk-transfer-specialist.md` lender-facing coverage-gap submission is gated by `decision.lender_engagement`.
5. Re-run all 17 Role Card conformance checks.
6. Re-run the safety rule across all artifact interfaces:
   external transmitting act + COSTLY_TO_REVERSE / IRREVERSIBLE => explicit specific `decision.<id>` gate.
   The Project / Delivery Lead integrated package is excluded from this rule only because its transmitting act is now explicitly `none`; any real external act occurs downstream.
7. Confirm every Role Card remains `PROPOSED`.
8. Confirm no Review Profile Registry / Decision Rights Register was created.

## Commit and push

If all mandatory validation passes:

Commit message:
`docs: remediate Phase 3 role registry after independent audit`

Push to:
`origin architecture/phase-3-role-registry`

Do not create a PR.

## Required final output

### A. CHANGES APPLIED
List changed files and concise change per file.

### B. ID NORMALIZATION
Report old → new mappings and zero-old-reference confirmation.

### C. HIGH FINDINGS
- B1: RESOLVED / NOT RESOLVED
- B2: RESOLVED / NOT RESOLVED

### D. CONFORMANCE
Report 17/17 status and artifact safety-gate status.

### E. COMMIT / PUSH
Commit SHA and remote push status.

### F. REMAINING NON-BLOCKING ITEMS
Only genuine items still requiring architecture or human review.

Do not mark Phase 3 complete or approved.