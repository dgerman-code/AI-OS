# Role Folder Conventions

Status: PROPOSED — Phase 3 repository convention
Version: 0.1

## Purpose
Fix how Role Card folders are named so that repeated generation does not produce competing slug variants for the same capability domain.

## Rule

- Role folders use stable kebab-case capability-domain slugs.
- A folder slug may be a shortened but unambiguous form of the Master Role Universe domain name.
- Canonical semantic classification is the Role Card `Capability Domain` field and the Master Role Universe, not the folder slug.
- Existing slugs, including `strategy-business`, `legal-compliance`, `project-development-technical-commercial` and `knowledge-documentation-disclosure`, are accepted and should not be renamed merely for textual symmetry.

## Consequence

A folder slug is an addressing convenience. It carries no authority over classification, and a shortened slug does not narrow the domain it holds. Where a slug and a `Capability Domain` value appear to disagree, the `Capability Domain` field and the Master Role Universe govern.

## Change control

Adding a new folder slug for a capability domain that does not yet have one is a normal Phase 3 generation act. Renaming an existing slug is not: it breaks existing paths and requires architecture review and human approval.
