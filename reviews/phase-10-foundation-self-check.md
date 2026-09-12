# Phase 10 — GitHub / Supabase / Storage Foundation Self-Check

Status: PROPOSED — READY FOR INDEPENDENT PHASE 10 FOUNDATION AUDIT

Branch: `architecture/phase-10-github-supabase-storage`
Start baseline: Phase 9 human-approval record `a94de435f0a47f9910d804029cc74bb7c995434a`
Approved Phase 9 architecture baseline: `a13fee667859bb8983d4f6a1f902f18fee0af083`

This is a **self**-check by the producing pass. Under Phase 6's vocabulary it is `PRODUCER_REVIEW` — internal quality control, which cannot satisfy an independent review requirement. It carries no results of its own; it points at the harness that produces them.

## Running the check

```
python3 validation/phase_10_validation.py
```

Python 3 standard library and `git` only. No network, no third-party packages, no writes. Deterministic; exit code 0 on pass, non-zero on any failure. `--verbose` prints each check's evidence; `--json` emits machine-readable results. Conventions are in `validation/README.md`.

**Current result: `=== 143/143 PASS ===`.** Normal, `--verbose` and `--json` modes all report the same total. The harness asserts that this document states the total and the group counts the suite actually emits, so a stale number here is a failure rather than a cosmetic slip.

**Scope boundary.** These 143 are **offline, deterministic checks over committed content**. Remote repository state — open pull requests, branch protection, review state — and the configuration of any database, bucket or forge are **not provable offline and are not claimed**. Phase 10 is unusual in that its subject is infrastructure; the temptation to assert that infrastructure is configured correctly is exactly what §5.3 and §4 of the migration document refuse.

| Group | Checks | Covers |
|---|---:|---|
| `identity` | 5 | The nine-object chain verbatim; every adjacent denial with its own consequence; seven identity facets; a backend may not redefine identity |
| `source-of-truth` | 8 | The matrix parsed as 21 rows × 9 columns; **no row with two masters**; every row carries a conflict rule; secrets never replicated; every required class present; definitions in the repository, operational records in the database |
| `data-domains` | 7 | Ten domains with write authority, lifecycle owner and audit posture; the boundary test; the bounded runtime domain; append-only has no operation to grant; `RETRACTED` terminal across every storage act; unclassified mutability defaults immutable |
| `versioning` | 9 | Five identifier kinds; surrogate key never a governance identity; six version planes; one stated rule for mutation/new object/supersession; lineage cycles detected; **historical references are recorded values, not pointers** |
| `consistency` | 5 | Six boundaries parsed; the four governance claims strong; **the two-system boundary declared non-atomic rather than pretending**; declared commit order and named compensating pattern |
| `artifact` | 8 | 22 fields; path defines nothing; new-version-only bytes; four hash uses with identity excluded; abstract algorithm; purge leaves a tombstone |
| `sensitivity` | 6 | **No scalar ceiling anywhere in Phase 10**; labels as a set; superset test with per-label obligations; Phase 9's test reused unmodified; unknown denies; metadata central where payload is not |
| `access-control` | 10 | Seven dimensions; enforcement ≠ authority; three authority collapses denied individually; no Right from a grant; no authority from a credential; absent-not-withheld operations; deny-by-default; two identity fields; portable vs backend |
| `audit` | 7 | Five histories kept apart; 11 event fields; Decision Record reference required for authority-bearing classes; append-only correction; **an unenforceable immutability claim recorded as a gap**; log is not evidence |
| `github` | 6 | Definitions and architecture history; approval is a record, not a tag; architecture vs tooling vs code; migrations versioned without becoming the database; **branch protection stated as requirement, not claimed as configured**; the never-commit list |
| `secrets` | 7 | Values never in repository or database; references inert; rotation ≠ revocation; environment-specific; metadata auditable without exposure; credential ≠ governance identity in both directions; no vendor mandated |
| `migration` | 9 | Nine governance elements; destructive migrations may not declare a rollback; a named Right before the migration exists; mismatch blocks; two authorities apart; three environments; **no downward cloning**; forward-only promotion; architecture vs configuration |
| `backup` | 10 | Backup ≠ archive ≠ audit; recovery classes instead of invented numbers; **no concrete RPO/RTO anywhere**; six deletion acts; legal hold outranks retention and its gaps recorded; supersession is none of the six; purge leaves a tombstone; restore governed and reconciled; backups unreachable with live credentials; retention as classes |
| `failure-modes` | 6 | Fifteen modes × five columns; every outcome from the fixed vocabulary; every required case; **a dangling reference is never repointed**; silently continuing is never an outcome; no failure relaxes a constraint |
| `anti-lock-in` | 3 | Five adapter boundaries; no governance semantic on a backend-specific feature; the current backend named as current |
| `templates` | 4 | Three templates, all `PROPOSED`, all inheriting the standard; contiguous numbering; no secret value in any template |
| `exemplars` | 8 | Five on disk, `PROPOSED` and synthetic; each states what it proves; the migration exemplar **blocks rather than inventing a Right**; the partial-failure exemplar refuses to adopt the orphan |
| `regression` | 20 | Phases 3–9 unchanged against the Phase 9 approval baseline; the Phase 9 approval record untouched; the Phase 8 and Phase 9 validators untouched; all `PROPOSED`; no runtime, schema, client or policy; **no secret-shaped string anywhere**; harness read-only and non-vacuous; no claim about remote PR state |
| `inventory` | 5 | Every count derived from a parsed source; the master inventory table reconciled; prose counts reconciled; heading-versus-list cardinality; and that this document's total and group counts are the ones the suite emits |

## What the harness does not prove

Stated first, because Phase 10's subject makes the gap wider than in earlier phases:

- **Nothing about live infrastructure.** No Supabase project, database, bucket, policy, account or secret was connected to, created, inspected or configured. The harness reads markdown.
- **Nothing about the forge.** Whether branch protection, required reviews or history protection are enabled is not observable from inside the repository and is **not claimed**.
- **Nothing about whether the architecture is right.** It checks that the documents agree with each other and with their own parsed tables. Internal consistency is not correctness.
- **Nothing an independent reviewer could not disagree with.** It is a `PRODUCER_REVIEW`.

## Open architecture questions — all 13 adjudicated

| # | Question | Disposition | The rule, or the reason for deferral |
|---:|---|---|---|
| 1 | GitHub or the database as source of truth for registry definitions? | **RESOLVED IN FOUNDATION** | **GitHub.** A registry definition is a governed document with a review history, and the repository already provides attributable authorship, reviewable diffs, immutable history and an approval naming a commit. Reproducing that in the database would rebuild a worse version of it |
| 2 | Are approved registry definitions mirrored into the database or authored there? | **RESOLVED IN FOUNDATION** | **Mirrored, as a read-only projection rebuilt from an approved baseline.** The mirror is never the target of a governed write; an application that writes to it has committed the defect the matrix exists to prevent. The mirror exists for querying and referential integrity, which is what the repository is bad at |
| 3 | Object storage provider abstraction | **RESOLVED IN FOUNDATION** | One of five adapter boundaries. Portable: bucket/prefix/key addressing, object versioning, immutability retention, encryption at rest. Vendor-specific: lifecycle, event and replication features, which no governance semantic may depend on |
| 4 | Are files mutable or new-version-only? | **RESOLVED IN FOUNDATION** | **New-version-only.** Bytes are never mutated in place, because a governed record may cite an artifact version and in-place mutation would silently change what that record said. An editing surface may hold working state; the artifact is the committed version |
| 5 | Database temporal / version strategy | **RESOLVED IN FOUNDATION** | Record versions within a logical object, monotonic and immutable once written; prior versions retained and linked; append-only in `decision`, `audit`, `knowledge` canonical history and `routing`. Effective time is recorded separately from event time where they differ |
| 6 | Audit log immutability mechanism boundary | **SAFE TO DEFER WITH EXPLICIT RULE** | The **requirement** is fixed: no update and no delete operation exists to grant. Where the backend can enforce this structurally it must; where it can only enforce it by permission, **the limitation is recorded rather than assumed away**. The optional chained event digest is declared optional precisely because only some environments can produce it |
| 7 | Retention versus legal hold | **RESOLVED IN FOUNDATION** | Six distinct acts, never synonyms. Legal hold outranks every retention rule; where the backup regime cannot honour a hold inside existing copies, that is recorded as a known gap rather than described as satisfied |
| 8 | Environment data cloning | **RESOLVED IN FOUNDATION** | **Production data is never cloned downward.** A lower environment holding real restricted material is an incident. Where a production-shaped dataset is genuinely needed, the path is a narrowly scoped, time-bounded, separately authorised extraction with labels preserved and the environment treated as production for its duration — which is expensive, and is meant to be |
| 9 | Migration rollback versus forward-fix | **RESOLVED IN FOUNDATION** | Non-destructive migrations may declare a rollback. **Destructive migrations may not** — the data is gone, and a script that pretends otherwise is the most dangerous artifact in the repository. Destructive change is corrected by forward fix, decided before the migration rather than after the failure |
| 10 | Where does backend-specific RLS end and portable authorisation begin? | **RESOLVED IN FOUNDATION** | Portable: the seven dimensions and their evaluation, deny-by-default for sensitive **and unknown**, and the operations that are absent rather than withheld. Backend-specific: the policy language and how session context reaches it. The test is whether the architecture above remains expressible if the mechanism changes |
| 11 | Private and sensitive source documents | **RESOLVED IN FOUNDATION** | Metadata may be held centrally; the payload does not follow it. Storage eligibility is a **superset test** on the location's approved label set, with unknown support treated as no support. Where no location is eligible the outcome is a recorded **BLOCK**, and an outage never makes a non-compliant location acceptable |
| 12 | Recovery from database / object divergence | **RESOLVED IN FOUNDATION** | A bidirectional reconciliation sweep. Records without objects are quarantined and escalated; objects without records are quarantined and expired, **never adopted by a later record**. Neither direction is repaired by inventing the missing half |
| 13 | Schema compatibility with the Phase 11 orchestrator | **PHASE 11+** | The `runtime_meta` domain is **reserved and bounded** now — correlation metadata only, never payloads, never governance outcomes, and citable by nothing. Phase 11 owns what goes in it. Reserving the boundary without designing the contents is the point: a domain invented later gets bolted onto whichever table was nearest |

**No authority, privacy or independence ambiguity is deferred.** Questions 1, 2, 8, 10, 11 and 12 all touch those concerns and are resolved in the foundation; only 6 defers a *mechanism* behind a fixed requirement, and only 13 is a scope boundary.

## Where this foundation is most likely to be wrong

Recorded for the audit rather than left to be discovered. In Phase 9 the audit found five HIGH findings and none was on the equivalent list, which is the honest measure of how much weight to put on what follows.

1. **The registry-mirror decision is the load-bearing one, and it is arguable.** Authoring definitions in the repository and projecting them into the database buys governance and costs latency and operational complexity: every definition change needs a rebuild, and the window during which the mirror is stale is real. An organisation that finds the rebuild painful will be tempted to write to the mirror, which is precisely the defect the matrix names.
2. **The ten-domain boundary test is a judgement.** "One write authority, one lifecycle owner, one audit posture" is defensible and will be argued, particularly around `execution` and `review`, which share more than the test admits.
3. **The audit-immutability gap is stated, not closed.** Where a backend enforces append-only only by permission, an identity with the wrong grant can still delete history. Recording the limitation is more honest than claiming immutability, and it is not the same as having it.
4. **Legal hold inside backups is a known gap.** Most backup regimes cannot selectively preserve or purge within existing copies. The architecture says so rather than asserting a guarantee, and an organisation with a real hold obligation will find the gap matters.
5. **No concrete recovery objective exists.** Recovery classes without numbers are honest and are also not yet operable. Somebody has to supply the numbers with evidence, and until they do, "point-in-time recovery is expected" is an expectation.
6. **The exemplars are synthetic, and the migration exemplar blocks.** Exemplar 5 reaches `NO_APPLICABLE_DECISION_RIGHT` because no approved Phase 7 Right covers destructive schema change — which is accurate today and means the most common real operation in this phase has no governed path yet.

## Standing statement

Every Phase 10 artifact is `PROPOSED`. Nothing is APPROVED or CANONICAL. No Supabase project, database, table, bucket, policy, service account, credential or secret was created, connected to, inspected or configured. No migration exists and none was run. No API, SDK, orchestrator, queue, retrieval system or agent was implemented. No Decision Right was created, no Role gained authority, no review status was set or changed, no knowledge was promoted, and no approved Phase 1–9 artifact was modified. This record does not claim human approval and is not an independent audit.
