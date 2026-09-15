# GitHub Access Model

AI-OS Mode A should operate with least privilege. Access level is an operational permission, not governance authority.

## Recommended roles

### Owner / Admin

Use for the human repository owner or a very small number of trusted administrators.

Responsibilities may include repository settings, access control, rulesets/branch protection, final merge decisions and recovery actions.

Admin access does not replace the AI-OS Decision Rights model; repository administration and governance authority are separate concepts.

### Trusted Maintainer / Write

Use only for trusted humans who need to edit repository content regularly.

Recommended boundaries:

- work on dedicated branches;
- avoid direct writes to protected integration branches where possible;
- no self-approval of critical authored work;
- no silent promotion of proposed/canonical status;
- merge authority only where explicitly granted.

### Read-only collaborator

Recommended default for reviewers, auditors, domain experts who only need to inspect the repository, and most external participants.

Read-only users can inspect governed sources and approval records without being able to change repository state.

### External AI read-only integration

**Default recommended AI access.**

Grant only enough access to read the required repository content and resolve branch/ref/commit SHA. The AI should begin from `AI_OS_ENTRYPOINT.md` and `ai-os.yaml` and return results without modifying repository state.

Read-only AI access is preferred for research, planning, reviews, comparisons, due diligence and the final cold-start acceptance test.

### Temporary write-capable AI or human session

Use only for a specific, explicit task that actually requires repository edits.

Recommended controls:

- dedicated working branch;
- exact starting SHA recorded;
- minimum necessary repository permissions;
- explicit file/task scope;
- no direct default-branch write unless separately authorised;
- human review before integration;
- revoke or reduce write permission after the task where practical.

Write permission does not grant approval, Decision Right exercise, canonicalisation authority or permission to merge.

## Recommended branch / ruleset protections

Where supported by the repository/account configuration, consider protecting `main` and any stable approval/integration branches with controls such as:

- restrict direct updates;
- require pull requests or an equivalent reviewed integration path for ordinary changes;
- restrict force pushes;
- restrict branch deletion;
- require selected status/validation checks where reliable;
- limit bypass privileges to the repository owner or narrowly designated maintainers/apps;
- keep reviewer/external-AI credentials read-only;
- use separate credentials/integrations for automation rather than sharing a personal owner credential.

For maximum immutability of an archival branch, a lock/read-only rule may be appropriate if it fits the repository workflow.

These are **recommendations only**. Phase 18 does not claim that GitHub settings, rulesets or branch protections have actually been changed.

## Credential principle

Do not give an external AI a broad personal access token merely for convenience. Prefer a dedicated integration/app/token with the minimum permissions required for the session. For Mode A review/use, `Contents: Read` or equivalent repository-read capability is the intended default where the provider supports that model.

Provider capabilities vary. If read-only repository access cannot be enforced by a particular provider, treat that as an operational limitation and choose an access method that preserves least privilege.

## Governance boundary

GitHub permission answers **what an identity can technically change in the repository**. AI-OS governance answers **what the identity is authorised to decide or approve**. These must not be conflated.

A user with Write permission is not automatically a governance approver. An AI that can commit cannot self-approve the commit. An Admin may still need the applicable human governance decision before changing approved semantics.

## Recommended default

For normal Mode A use:

`Human owner/admin -> repository governance`

`External AI / reviewer -> read-only`

Temporarily elevate to scoped write access only when the human explicitly needs repository edits.