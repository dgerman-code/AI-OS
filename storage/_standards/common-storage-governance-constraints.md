# Common Storage Governance Constraints

Status: PROPOSED — Phase 10 standard candidate
Standard ID: `standard.storage.common_constraints`
Version: 0.1

Every Phase 10 artifact inherits this document by reference and does not repeat it. Where anything in `storage/` contradicts this standard, this standard governs and the contradicting artifact is defective.

## 1. Storage is a substrate, never an authority
Where a thing is kept says nothing about whether it is true, approved, canonical or authorised. A backend that could change that by itself would be a governance system, and none of the three is.

## 2. A storage backend never redefines governance identity
Governance identity is the stable logical ID assigned by the owning registry. A surrogate key, a row, a path, a bucket, a commit or a content hash is a way of finding the object, never a way of being it.

## 3. Exactly one system is authoritative for each data class
Every row of the Source-of-Truth Matrix names one authoritative system. A second representation is a **projection**, and a projection is never written by anything but its projector.

## 4. A projection that disagrees with its source is a defect, not a version
Divergence is reconciled toward the authoritative system or quarantined. It is never resolved by whichever copy was written last.

## 5. Possession of a credential grants no authority
No service account, no model, no provider, no deployment and no automated process acquires a Decision Right, a review outcome, a canonical promotion or a human signature by being able to write the row that records one.

## 6. Database authorisation is enforcement, not governance
Row-level security decides whether an operation is permitted to touch a row. Whether the act it records was authorised is Phase 7's question, decided before the row exists.

## 7. Competence is not permission and permission is not competence
A Role Card describes what a Role is competent to do. A database grant describes what an identity may execute. Neither implies the other, and no mapping between them is automatic.

## 8. Append-only history is never rewritten
Decision history (Phase 7), canonical history (Phase 8), routing history (Phase 9) and the Phase 10 audit log are append-only. Correction is a new appended record that names what it corrects.

## 9. `RETRACTED` is terminal and survives storage
Phase 8's terminal states are properties of the governed object, not of its current representation. No retention rule, supersession, migration, restore or purge converts a retracted object back into a usable one.

## 10. Supersession does not delete
A superseded record is retained, linked from its successor, and remains readable as what it was when it was current.

## 11. Sensitivity is a set of labels, never a level
Phase 8 defines no total order over sensitivity classes, and Phase 10 introduces none. Eligibility to store, read or replicate is a **subset test** over declared label sets, exactly as in Phase 9.

## 12. Unknown classification is not permission
An object whose sensitivity, scope or residency is unassessed is treated as restricted until assessed. Deny-by-default applies to unknown, not only to known-sensitive.

## 13. Secret values never enter the repository or the operational database
What is stored is a **reference** to a secret held in a secret manager. A reference resolves to nothing for anyone who cannot already resolve it.

## 14. Metadata about a secret is not a secret
Which identity holds which reference, when it was rotated and who rotated it are auditable. The value never is.

## 15. A content hash is integrity, not identity
A hash proves bytes are unchanged. It never becomes the governance ID, because two governed objects may legitimately hold identical bytes and one governed object may legitimately change them.

## 16. A file path or filename defines nothing
Paths are addresses, and addresses change. Artifact identity is the artifact's stable ID; the display name is metadata that may be edited without changing the artifact.

## 17. No distributed atomicity is claimed across the three systems
A commit, a database transaction and an object upload cannot be made one atomic act. Multi-system operations declare a **commit order**, a **reconciliation owner** and a **compensating outcome**, and the architecture never pretends otherwise.

## 18. The metadata record is committed last and read first
An object whose metadata transaction did not commit is **orphaned**, not stored. Nothing reads an object the registry does not know about.

## 19. Strong consistency is required wherever a governance claim is recorded
A Routing Decision and its version references, a Decision Record and its linked artifact state, a canonical promotion and its version, a review finding and its status transition each commit as one database transaction or not at all.

## 20. An audit event, a Decision Record, a Git commit and an operational log are four objects
Each answers a different question. None may be substituted for, derived from, or presented as another.

## 21. An operational log is not evidence
It may be truncated, sampled, rotated and discarded. Nothing that must survive is kept only there.

## 22. GitHub versions migrations; the database applies them
The repository is the authority for what a migration *is*; the environment is the authority for what has been *applied*. Neither can answer the other's question.

## 23. A schema version is declared, recorded and checked
An environment records the schema version it is at; the repository records the versions it is compatible with. A mismatch blocks rather than degrades.

## 24. Destructive change requires a named human decision
Dropping a column, dropping a table, narrowing a type or purging data is governed by a Phase 7 Decision Right, exercised before the migration exists, never inferred from the migration being written.

## 25. Production data is not test data
No production payload is cloned into a lower environment. Fixtures are synthetic, and a lower environment holding real restricted material is an incident, not a convenience.

## 26. Backups are not an archive and not an audit trail
A backup exists to restore a system. It is not a retention mechanism, not a record of what happened, and its expiry is not a deletion guarantee.

## 27. Legal hold outranks every retention rule
While a hold is in force, nothing within its scope expires, is purged or is overwritten — including in backups, to the extent the backup regime permits, and where it does not, the limitation is recorded rather than assumed away.

## 28. Deletion is six different acts
Logical retraction, business deletion request, physical purge, legal hold, backup expiry and archival are distinct, separately authorised, and never used as synonyms for one another.

## 29. A restore is a governed event
Restoring is not an undo. It reintroduces state that the audit log must record, that may be stale against the repository, and that must be reconciled before it is trusted.

## 30. Provider independence is a boundary, not a preference
PostgreSQL semantics, backend conveniences, the object-storage interface, the secret-management interface and the Git host interface are five separate surfaces. A governance semantic that depends on a proprietary feature is defective unless that feature sits behind a declared adapter boundary.

## 31. Phase 10 changes no approved semantics
It persists Phase 1–9. Where a persistence design would require an approved semantic to change, the design is wrong, and the change is a matter for the phase that owns the semantic.
