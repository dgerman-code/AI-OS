# Main Readiness

This document describes how the approved Phase 1–17 body of work should be consolidated into a stable main-ready repository state. It does not itself merge, promote, or change the default branch.

## Integrated baseline

The intended integrated system baseline includes the approved phase-level architecture, governance records, implementation specifications, reference implementation artifacts, Mode A entrypoint/manifest/adapters/result envelope, validation assets, and the Phase 18 completion documents that describe how to use and protect the repository.

The Phase 17 approval commit `352c2f056177e43f422b008042b7296799742958` is the approved ancestor from which Phase 18 completion work starts. Phase 18 should produce one reviewed completion SHA before any main consolidation decision.

## What belongs in the main-ready package

The main-ready package should retain:

- architecture and governance sources for Phases 1–17;
- Role, Skill, Workflow, Review Profile, Decision Right and Model registry sources with their actual recorded statuses unchanged;
- historical phase approval records under `reviews/`;
- Phase 14 implementation specifications;
- Phase 15 planning architecture;
- Phase 16 planner-activation reference implementation and assurance artifacts;
- Phase 17 Mode A entrypoint, manifest, connection guide, result envelope, provider-neutral adapters and validator;
- Phase 18 system status, operational/access guidance, completion validator and post-approval cold-start test plan.

These files may coexist with `PROPOSED` artifacts. Inclusion in the repository does not silently promote them.

## What remains historical, proposed or deferred

Historical prompts, audits, remediation records and self-checks remain useful evidence and should not be rewritten merely for cosmetic consolidation.

Artifacts explicitly marked `PROPOSED` remain proposed unless a separate governed approval changes that state. This is especially important for individual Skill cards and other child artifacts whose phase-level architecture was approved without blanket per-card promotion.

Mode B remains deferred. Provider API invocation, provider routing, billing, key management, retries/fallbacks, workers, queues, schedulers and production deployment infrastructure are not part of the current main-ready Mode A package.

## Can history be consolidated safely?

Yes, provided consolidation is history-preserving and semantic changes are avoided. The current work has been developed as an additive chain with explicit human approval records. A safe consolidation should preserve the complete approved content and approval evidence rather than cherry-picking only attractive final files and losing governance history.

Before changing the default branch or merging into `main`, verify all of the following:

1. Phase 18 has an explicit human approval record naming its exact reviewed completion baseline.
2. The completion validator and Phase 17 Mode A validator both pass on that exact baseline.
3. The Phase 18 independent final review reports no blocker.
4. The diff from the approved Phase 17 ancestor contains only expected Phase 18 completion/onboarding changes and no accidental upstream semantic rewrite.
5. Repository protection and least-privilege decisions are agreed separately; documentation alone must not be mistaken for configured settings.
6. The post-approval external cold-start test plan is ready; the test itself may occur immediately after consolidation or before default-branch switch, according to the human decision.
7. No unresolved conflict would overwrite historical approval records.

## Recommended merge strategy

Preferred strategy: **preserve the Phase 18 completion branch ancestry and integrate it into `main` with a normal history-preserving merge after human approval**. Avoid a squash that erases the approval/remediation history unless a separate archival mechanism first preserves all governance evidence.

If `main` has diverged materially, perform an explicit comparison and resolve conflicts conservatively. Governance records and approved semantics should win over cosmetic or stale root documentation. Do not silently rebase historical approval commits in a way that changes their meaning.

## Default-branch decision

Do not change the default branch merely because Phase 18 passes review. The human owner should first confirm:

- the exact Phase 18 approval SHA;
- desired repository access protections;
- whether the cold-start test is to run before or immediately after main integration;
- whether `main` contains unrelated changes needing reconciliation.

Phase 18 documents readiness. It does not itself merge, open a PR, or change the default branch.