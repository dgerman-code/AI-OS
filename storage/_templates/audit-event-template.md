# Audit Event Template

Status: PROPOSED — Phase 10 template candidate
Inherits: `standard.storage.common_constraints@0.1`

The 11 fields of `storage/audit-provenance-model.md` §2. **Append-only: this record is never updated and never deleted.**

1. **Event ID** — stable, unique, never reused
2. **Subject reference** — the governed object's stable logical ID and affected version
3. **Change class** — create · new version · transition · link · quarantine · hold · purge · rebuild · restore
4. **Previous version reference** — or explicitly none
5. **New version reference** — or explicitly none
6. **Reason / context** — in the owning phase's vocabulary where one exists
7. **Decision Record reference** — **required** for purge, hold release, destructive migration, restore and reclassification. For those classes, **absent is a failure, not a blank field**
8. **Provenance reference**
9. **Timestamps** — event time; effective time where it differs
10. **Identities** — **human identity reference** and **system / service identity**, as two separate fields
11. **Correlation reference** — links the events of one operation

*Optional where the deployment supports it:* **immutable event reference** — a chained digest over this event and its predecessor. Declared optional deliberately: an architecture must not assume a chain only some environments can produce.

## What this event is not
- **Not a Decision Record.** It records a change; the authority for the change is field 7 or does not exist.
- **Not a Git commit.** The repository records definitions; this records operations.
- **Not an operational log.** A log is rotated and discarded; this is retained and never deleted.
- **Not knowledge provenance.** Provenance is about content; this is about a record.
