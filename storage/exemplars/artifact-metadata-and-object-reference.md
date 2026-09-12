# Exemplar 1 — An artifact, its bytes, and why they are two things

Status: PROPOSED — Phase 10 exemplar storage record
Inherits: `standard.storage.common_constraints@0.1`

**Illustrative and synthetic.** All identifiers are architecture placeholders. No real project, document, bucket or person is referenced, and no secret appears.

**Proves:** that artifact identity lives in the record, the bytes live in object storage, and the path is an address that can change without the artifact changing.

## The artifact

| Field | Value |
|---|---|
| Artifact stable ID | `artifact.appraisal_model_v2` |
| Record version | 3 |
| Storage location | `bkt.governed.eu` / `project-alpha/appraisal/` / `obj.7f3c9a` @ object version 2 |
| Display name | `Appraisal model (final).xlsx` |
| Media type | spreadsheet |
| Size | 418 KiB |
| Content hash | `digest-alg-a`:`c41f…8e2` |
| Encryption state | encrypted at rest; key reference class `env.production.governed` |
| Scope | `project.alpha` |
| Sensitivity labels | {`CONFIDENTIAL`, `PERSONAL_DATA`} |
| Residency | allowed jurisdictions: two named; cross-border `FORBIDDEN` |
| Provenance | derived from `source.hr_extract_2026_03`; origin `HUMAN_AUTHORED` with `AI_SUGGESTION` sections marked |
| Producer | human identity reference `person.ref.014` |
| Retention class | `retention.project_records` |
| Legal hold | absent |
| Snapshot flag | absent |
| Supersedes | `artifact.appraisal_model_v2` record version 2 |
| Status | current |

## What changed between record versions 2 and 3

**The file was moved.** Its prefix changed from `project-alpha/drafts/` to `project-alpha/appraisal/` when the draft was finalised.

| | Version 2 | Version 3 |
|---|---|---|
| Artifact stable ID | `artifact.appraisal_model_v2` | **Unchanged** |
| Storage location | `project-alpha/drafts/` … | **Changed** |
| Content hash | `c41f…8e2` | **Unchanged** |
| Display name | `Appraisal model (draft 4).xlsx` | Changed |

**Nothing governed changed.** A Decision Record citing `artifact.appraisal_model_v2` still resolves, because it cited the artifact and not the path. Had the path been the identity — the ordinary shortcut — that citation would now be broken by a rename that changed no content at all.

## The storage eligibility test

The location `bkt.governed.eu` is approved for {`INTERNAL`, `CONFIDENTIAL`, `PERSONAL_DATA`, `TRADE_SECRET`}. The artifact carries {`CONFIDENTIAL`, `PERSONAL_DATA`}.

**Approved ⊇ carried, so the location is eligible.** This is a **subset test**, exactly as in Phase 9 §3, and not a comparison: `PERSONAL_DATA` is not "above" `CONFIDENTIAL`, because Phase 8 orders neither. A location approved for `PERSONAL_DATA` alone would be **ineligible** here, and would look like the stricter option under any ceiling model.

## What this record does not do

It does not make the appraisal correct, approved or canonical. The spreadsheet is a file with governance metadata attached; **it becomes evidence when something cites it as evidence, and canonical only through Phase 8's promotion path** — neither of which is a storage act.
