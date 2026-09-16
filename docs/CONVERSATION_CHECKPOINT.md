# Conversation Checkpoint Contract

Status: `PROPOSED` — Mode A continuity hardening
Version: 0.1

## Purpose

A Conversation Checkpoint is a compact, non-canonical continuity record for long-running chats. It exists so an external AI can resume work without pretending that provider memory is a durable audit system.

It is not canonical memory, evidence, a Review result, a Decision Record, an ExecutionBasis or authority.

## Minimum fields

A checkpoint should retain, when available:

- `scope_ref` — stable scope identity, not only a display name;
- `scope_label` — human-readable project/organisation/workstream name;
- `objective` — current working objective;
- `source_refs` — controlled project/evidence sources and versions used for the current working state;
- `governance_ref` — AI-OS ref/SHA last verified for governed work where pinning matters;
- `last_verification_point` — what was last revalidated and when/at which task boundary;
- `last_completed` — last completed working step or artifact;
- `unresolved_items` — material open questions, conflicts and blockers;
- `next_action` — current recommended next dependency/action;
- `material_change_flags` — known changes that require FULL rather than FAST resolution.

## Refresh rule

Refresh the checkpoint after a material project task, after new evidence is accepted into working context, after a human decision changes the working basis, after a material objective change, or before resuming work from stale/compacted context.

Do not refresh it by silently promoting an AI summary into evidence.

## Resume rule

A checkpoint may accelerate navigation, but the AI must revalidate any material item whose correctness depends on freshness, approval state, evidence version, criticality, Workflow admissibility, Review state or Decision Rights.

If `scope_ref` is absent or multiple projects share the same/similar label, the AI must clarify the intended scope before importing project-specific evidence.

## Audit truthfulness

If the original governed result, source references or retained checkpoint are no longer available, AUDIT MODE must state that the original audit trail is unavailable or incomplete. It must not reconstruct a confident historical provenance narrative from conversational memory alone.

A reconstructed summary may be offered only when clearly labelled as reconstruction.

## Retention

This contract does not mandate a new storage system. A checkpoint may be retained in an already authorised project record, conversation workspace, repository artifact or future service store according to the applicable storage/governance boundary.

Absence of durable retention is a disclosed limitation, not permission to invent retention.
