# Human Intervention Record Template

Status: PROPOSED — Phase 11 template candidate
Inherits: `standard.orchestration.common_constraints@0.1`

**Append-only: never updated, never deleted.** An intervention that was wrong is followed by another naming it.

1. **Intervention ID** — `intervention.<id>`, stable, unique, never reused
2. **Run and position** — `run.<id>`, stage or activity instance
3. **Human identity reference** — the person. **Not the account, and not the system identity**
4. **System identity** — what executed the change. A separate field, always
5. **Act** — resume · pause · cancel · reassign · approve a permitted operational exception · supply evidence or request rework
6. **Reason** — in governed vocabulary where one exists
7. **Authority reference** — the Decision Record. **Required for "approve a permitted operational exception"; absent is a failure for that act, not a blank field**
8. **Bounded effect** — exactly what changes, and nothing beyond it
9. **Expiry** — where the effect is time-bounded
10. **Timestamps** — act time; effective time where they differ
11. **Resulting state** — the run's four axes, before and after

## What this record is not
- **Not authority.** The ability to perform an action is not authority to authorise one
- **Not a review**, and never satisfies a review gate
- **Not a Decision Record.** Field 7 references one or the act required none
- **Not a way past a stop condition** that still holds
