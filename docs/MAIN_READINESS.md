# Main Integration State

This document records the integrated `main` state for the approved Phase 1–18 body of work and later narrowly governed remediations. Historical merge-readiness guidance is preserved only where it remains useful for future governed changes.

## Integrated baseline

The integrated `main` baseline includes the approved phase-level architecture, governance records, implementation specifications, reference implementation artifacts, Mode A entrypoint/manifest/adapters/result envelope, validation assets, Phase 18 completion documents and the validated Astra 6 targeted remediation.

The Phase 17 approval commit `352c2f056177e43f422b008042b7296799742958` is the approved ancestor from which Phase 18 completion work started. Phase 18 produced reviewed implementation baseline `eb8a64ec5e79589f7def3a96a740d004f59236f8` and explicit human approval commit `5ab13b4b99cc46e7b68bf370b0230e0af59daef4`. The first post-approval cold-start test was then recorded at that exact tested commit.

## What belongs in the integrated main package

The integrated package retains:

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

Mode B remains deferred. Provider API invocation, provider routing, billing, key management, retries/fallbacks, workers, queues, schedulers and production deployment infrastructure are not part of the current integrated Mode A package.

## Current integration evidence

Phase 18 is explicitly human-approved, the first post-approval cold-start test is recorded, Astra 6 remediation is integrated into `main`, and the read-only GitHub Actions validation suite has passed over the integrated remediation path. Future materially changed baselines should preserve history, rerun the applicable validators and repeat the cold-start procedure when the change affects provider-facing behaviour or discovery.

Repository protection remains a separate operational control. The verified active `AI-OS Main Protection` ruleset currently prevents branch deletion and non-fast-forward updates. It does not yet require pull requests or successful validation checks before every `main` update.

## Future merge strategy

For future governed changes, prefer history-preserving pull requests into `main`, preserve approval/remediation evidence, and avoid silently rebasing or squashing away governance history unless that evidence is preserved separately. If branches diverge materially, compare them explicitly and resolve conflicts conservatively; governed semantics and approval records take precedence over cosmetic or stale documentation.

## Default branch

`main` is the current integrated default branch. Future semantic changes should enter through governed change control and, operationally, should use pull requests with successful automated validation once the corresponding repository ruleset is strengthened. Integration into `main` does not itself grant production authority, canonicalise unrelated artifacts or exercise a human Decision Right.