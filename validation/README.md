# AI-OS Architecture Validation

Status: PROPOSED — architecture-validation tooling

This directory holds **repeatable architecture validation harnesses**. They read the repository's markdown architecture and assert properties of it.

They are **not runtime implementation**. They implement no part of AI-OS, define no schema, expose no interface, and are never a dependency of anything the architecture describes. They exist so that a claim like "all checks pass" is reproducible by anyone with the repository, rather than asserted in prose — which is the defect the Phase 8 independent audit identified in the first Phase 8 self-check.

## Running

```
python3 validation/phase_8_validation.py
```

Requires Python 3 and `git` on PATH. No third-party packages, no network. Exit code 0 when every check passes, 1 otherwise. Output is deterministic: one `PASS`/`FAIL` line per check, then a total.

Options:

```
python3 validation/phase_8_validation.py --verbose   # also print each check's evidence
python3 validation/phase_8_validation.py --json      # machine-readable results
```

## Scope boundary — what a local harness can and cannot prove

This harness is **offline and read-only**. It runs no network call, writes no file, and runs `git` only for read commands.

| Provable here | Not provable here |
|---|---|
| Every property of the repository's committed content | The remote repository's open pull-request count |
| Diffs against an approved baseline commit | Branch protection, review state, or anything held only by the forge |
| That no PR artifact or PR-creating call exists **locally** | That no PR exists **remotely** |

The PR check states this in its own evidence line. **A local Python script cannot prove a remote open-PR count, and this one does not claim to** — that is an external check, performed against the GitHub API by audit tooling and reported separately from the deterministic count.

## Conventions

- **Discover, do not enumerate.** Files are found by walking the tree, so a new artifact is covered automatically and cannot pass by being absent from a hand-written list.
- **Prefer semantic checks.** Where a property can be tested by parsing structure or cross-referencing two documents, that is done instead of matching a string.
- **No vacuous checks.** No `or True`, no tautology, no unreachable failure branch, no hard-coded pass counter. One check enforces this on the rest of the file, and the two self-inspecting checks exclude their own source so they cannot match their own literals.
- **Never weaken a check to make it pass.** A wrong check is replaced with a stricter correct one, and the replacement is recorded in the relevant review record.
