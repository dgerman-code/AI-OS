#!/usr/bin/env python3
"""Phase 10 Storage / Persistence architecture validation.

Architecture-validation tooling. Reads the repository's markdown and asserts properties of
it. Implements no part of AI-OS: no database, schema, migration, client, credential, bucket,
policy or runtime.

Usage:
    python3 validation/phase_10_validation.py [--verbose] [--json]

Exit code 0 if every check passes, 1 otherwise.
"""

import json
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The Phase 9 human-approval record. Everything at or before it is upstream and immutable.
PHASE9_BASELINE = "a94de435f0a47f9910d804029cc74bb7c995434a"

UPSTREAM_PATHS = {
    "Phase 3 Roles": ["roles/"],
    "Phase 4 Skills": ["skills/", "architecture/skill-registry-design.md",
                       "architecture/role-to-skill-mapping-rules.md"],
    "Phase 5 Workflows": ["workflows/", "architecture/workflow-registry-design.md"],
    "Phase 6 Handoff/Review": ["handoffs/", "architecture/handoff-review-registry-design.md",
                               "reviews/_standards/", "reviews/_templates/",
                               "reviews/master-review-profile-universe.md", "reviews/exemplars/"],
    "Phase 7 Decisions": ["decisions/", "architecture/decision-rights-registry-design.md"],
    "Phase 8 Knowledge": ["knowledge/", "architecture/memory-canonical-governance.md"],
    "Phase 9 Models/Routing": ["models/", "architecture/model-registry-router.md"],
    "Phase 9 approval record": ["reviews/phase-9-final-approval.md"],
    "Phase 8/9 validators": ["validation/phase_8_validation.py",
                             "validation/phase_9_validation.py"],
    "Inherited Phase 2/3 architecture": ["architecture/context-hierarchy.md",
                                         "architecture/project-criticality-policy.md",
                                         "architecture/registry-separation.md",
                                         "architecture/system-principles.md"],
}


def read(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as fh:
        return fh.read()


def plain(text):
    """Strip markdown emphasis: checks test what a sentence says, not how it is styled."""
    return text.replace("**", "").replace("`", "")


def discover(subdir, suffix=".md"):
    """Walk the tree. Never enumerate: a new artifact is covered automatically and cannot
    pass by being absent from a hand-written list."""
    out = []
    for root, _dirs, files in os.walk(os.path.join(REPO, subdir)):
        for name in sorted(files):
            if name.endswith(suffix):
                out.append(os.path.relpath(os.path.join(root, name), REPO))
    return sorted(out)


def git_unchanged(paths):
    diff = subprocess.run(["git", "diff", "--name-only", PHASE9_BASELINE, "HEAD", "--"] + paths,
                          cwd=REPO, capture_output=True, text=True)
    status = subprocess.run(["git", "status", "--porcelain", "--"] + paths,
                            cwd=REPO, capture_output=True, text=True)
    changed = [ln for ln in (diff.stdout + status.stdout).splitlines() if ln.strip()]
    return (not changed), changed


ARCH = "architecture/storage-persistence-architecture.md"
STORAGE_FILES = discover("storage")
EXEMPLARS = [f for f in STORAGE_FILES if "/exemplars/" in f]
TEMPLATES = [f for f in STORAGE_FILES if "/_templates/" in f]
STANDARD = "storage/_standards/common-storage-governance-constraints.md"
PHASE10_FILES = ([ARCH] + STORAGE_FILES
                 + [f for f in discover("reviews") if "phase-10" in f])

DOCS = {rel: read(rel) for rel in PHASE10_FILES}
NORMATIVE = {rel: doc for rel, doc in DOCS.items() if not rel.startswith("reviews/")}
# A denial marker suppresses a scan hit ONLY on the hit's own line. An earlier version of
# this harness used a +/-250-character window, which a controlled failure probe proved was
# far too wide: prose about what the architecture refuses is dense with denial words, so an
# injected schema-definition statement and an injected scalar sensitivity field both passed.
# Line scope is the fix, and it is strictly narrower than what it replaces.
DENIAL_MARKER = re.compile(
    r"\bnever\b|\bno\b|\bnot\b|\bcannot\b|must not|prohibit|refus|forbid|"
    r"would have|rejected|instead of|rather than|defect", re.I)
REMEDIATION_CONTEXT = DENIAL_MARKER


def line_of(text, index):
    """The single line containing `index` - the only context a denial marker may reach."""
    start = text.rfind("\n", 0, index) + 1
    end = text.find("\n", index)
    return text[start:end if end != -1 else len(text)]

A = DOCS[ARCH]
SOT = DOCS["storage/source-of-truth-matrix.md"]
DOM = DOCS["storage/data-domain-model.md"]
VER = DOCS["storage/versioning-and-lineage.md"]
ART = DOCS["storage/artifact-object-model.md"]
ACL = DOCS["storage/access-control-and-rls-boundary.md"]
AUD = DOCS["storage/audit-provenance-model.md"]
MIG = DOCS["storage/migration-and-environment-governance.md"]
BAK = DOCS["storage/backup-retention-recovery.md"]
FAIL = DOCS["storage/failure-modes.md"]
SEC = DOCS["storage/secrets-and-credentials.md"]
STD = DOCS[STANDARD]
TMPL = {os.path.basename(t): DOCS[t] for t in TEMPLATES}
ALL10 = "\n".join(DOCS.values())

RESULTS = []


def check(group, name, fn):
    try:
        outcome = fn()
    except Exception as exc:
        outcome = (False, "ERROR: %s: %s" % (type(exc).__name__, exc))
    if isinstance(outcome, tuple):
        ok, evidence = outcome
    else:
        ok, evidence = bool(outcome), ""
    RESULTS.append({"group": group, "name": name, "pass": bool(ok), "evidence": str(evidence)})


# =========================================================== identity separation

SEPARATED = ["REPOSITORY OBJECT", "DATABASE RECORD", "FILE OBJECT", "ARTIFACT",
             "CANONICAL RECORD", "DECISION RECORD", "RUNTIME EVENT", "SECRET", "CREDENTIAL"]

check("identity", "full nine-object separation chain stated verbatim",
      lambda: (" != ".join(SEPARATED) in plain(A), "%d objects" % len(SEPARATED)))


def denial_table_complete():
    """Each adjacent pair must be denied individually, not only inside the chain."""
    flat = plain(A)
    missing = []
    for i in range(len(SEPARATED) - 1):
        pair = "%s != %s" % (SEPARATED[i], SEPARATED[i + 1])
        if flat.count(pair) < 2:          # once in the chain, once as its own denial row
            missing.append(pair)
    return (not missing, str(missing) if missing
            else "%d pairwise denials each stated with its consequence" % (len(SEPARATED) - 1))


check("identity", "every adjacent denial is stated with its own consequence", denial_table_complete)

FACETS = ["Logical object identity", "Storage location", "Version identity", "Content hash",
          "Mutable metadata", "Immutable audit/history record",
          "Runtime instance / event identity"]
check("identity", "seven identity facets are separately recorded",
      lambda: (all(f in plain(A) for f in FACETS), "%d facets" % len(FACETS)))

check("identity", "a storage backend may not redefine governance identity",
      lambda: ("A storage backend never redefines governance identity" in plain(STD)
               and "never a way of being it" in plain(STD), ""))

check("identity", "upstream separations are preserved, not restated as new",
      lambda: (all(s in plain(A) for s in ["ROUTER != ORCHESTRATOR"])
               and "No Role Card, Skill Card or Workflow is modified" in plain(A), ""))

# =========================================================== source-of-truth matrix

SYSTEMS = ["GITHUB", "DB", "OBJECT", "SECRETS", "NONE"]


def sot_rows():
    """Parse the matrix into rows of cells. Never a string scan: the whole point is structure."""
    body = SOT.split("## 1. The matrix")[1].split("## 2.")[0]
    rows = []
    for line in body.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 9 or re.match(r"^[\s:|-]+$", line.strip().strip("|")):
            continue
        if cells[0] == "#":
            continue
        rows.append(cells)
    return rows


check("source-of-truth", "the matrix parses into rows with every required column",
      lambda: (lambda r: (len(r) == 21 and all(len(x) == 9 for x in r),
                          "%d rows x %d columns" % (len(r), len(r[0]) if r else 0)))(sot_rows()))


def no_dual_master():
    """Exactly one authoritative system per row. A row naming two is the defect this exists for."""
    bad = []
    for cells in sot_rows():
        auth = plain(cells[2])
        named = [s for s in SYSTEMS if re.search(r"\b%s\b" % s, auth)]
        if len(named) != 1:
            # Row 20 declares a split by item; it must say so explicitly and still name a rule.
            if "Split, stated per item" in auth and "no single configuration item is authoritative in two places" in plain(SOT):
                continue
            bad.append("row %s: authoritative = %s" % (cells[0], named or auth[:40]))
    return (not bad, str(bad) if bad else "every row names exactly one authoritative system")


check("source-of-truth", "no row has two masters", no_dual_master)


def every_row_has_a_conflict_rule():
    bad = [cells[0] for cells in sot_rows() if len(plain(cells[8]).strip()) < 10]
    return (not bad, "rows without a conflict rule: %s" % bad if bad
            else "all %d rows carry a conflict resolution rule" % len(sot_rows()))


check("source-of-truth", "every row carries a conflict resolution rule",
      every_row_has_a_conflict_rule)


def secrets_never_replicated():
    for cells in sot_rows():
        if "Secrets and credentials" in cells[1]:
            return ("Never replicated" in cells[4] and "SECRETS" in plain(cells[2])
                    and "Reference only" in plain(cells[3]),
                    "replication cell: %s" % plain(cells[4]))
    return (False, "no secrets row found, so nothing was checked")


check("source-of-truth", "the secrets row is authoritative elsewhere and never replicated",
      secrets_never_replicated)


REQUIRED_CLASSES = ["Role Registry", "Skill Registry", "Review Profile Registry",
                    "Workflow Registry", "Decision Rights Register", "Knowledge / Canonical",
                    "Model Registry", "Routing Policies", "Routing Decisions",
                    "Handoff records", "Review instances", "Decision Records", "Memory items",
                    "Source / evidence metadata", "Runtime logs", "Secrets and credentials",
                    "Configuration", "backups"]
check("source-of-truth", "every required data class appears as a row",
      lambda: (lambda missing: (not missing, str(missing) if missing
                                else "%d required classes present" % len(REQUIRED_CLASSES)))(
          [c for c in REQUIRED_CLASSES
           if not any(c.lower() in cells[1].lower() for cells in sot_rows())]))

check("source-of-truth", "a projection is never the target of a governed write",
      lambda: ("is never written by anything but its projector" in plain(SOT)
               and "never the target of a governed write" in plain(SOT)
               and "A projection that disagrees with its source is a defect, not a version"
               in plain(STD), ""))

check("source-of-truth", "registry definitions are authoritative in the repository",
      lambda: (lambda rows: (all("GITHUB" in plain(c[2]) for c in rows
                                 if "Registry (definitions)" in c[1]) and len(rows) >= 4,
                             "%d definition rows" % len(rows)))(
          [c for c in sot_rows() if "Registry (definitions)" in c[1]]))

check("source-of-truth", "operational governance records are authoritative in the database",
      lambda: (lambda rows: (all(plain(c[2]).strip() == "DB" for c in rows), str(
          [(c[0], plain(c[2])) for c in rows])))(
          [c for c in sot_rows()
           if c[1] in ("Routing Decisions", "Decision Records", "Handoff records")]))

# =========================================================== data domains


def domain_rows():
    body = DOM.split("## 2. The ten domains")[1].split("### 2.1")[0]
    return [ln for ln in body.splitlines()
            if ln.startswith("| ") and not re.match(r"^\|[\s:|-]+\|\s*$", ln)][1:]


check("data-domains", "ten domains, each with write authority, lifecycle owner and audit posture",
      lambda: (lambda rows: (len(rows) == 10 and all(len(r.strip().strip("|").split("|")) == 6
                                                     for r in rows), "%d domains" % len(rows)))(
          domain_rows()))

check("data-domains", "a domain boundary requires one write authority, owner and audit posture",
      lambda: ("three things coincide" in plain(DOM)
               and "one write authority, one lifecycle owner, and one audit posture" in plain(DOM),
               ""))

check("data-domains", "the runtime-metadata domain is bounded and cannot be cited as a reason",
      lambda: ("nothing in any other domain may cite it as a reason" in plain(DOM).lower()
               and "never payloads" in plain(DOM) and "not evidence" in plain(DOM), ""))

check("data-domains", "append-only domains have no update or delete operation to grant",
      lambda: ("no update and no delete operation to grant" in plain(AUD)
               and "not as a policy, as an absence of the operation" in plain(VER), ""))

check("data-domains", "soft delete is never used on decision, audit, canonical or routing history",
      lambda: ("it is never used on" in plain(DOM).lower()
               and "There is no hard delete of a governed record" in plain(DOM), ""))

check("data-domains", "RETRACTED remains terminal across every storage act",
      lambda: ("RETRACTED` is terminal" in DOM
               and "no supersession, restore, migration, reclassification or retention action"
               in plain(DOM)
               and "re-applies the retraction before the object is readable" in plain(DOM), ""))

check("data-domains", "unclassified mutability defaults to immutable",
      lambda: ("immutable by default" in plain(DOM)
               and "Unclassified mutability is the same defect as unclassified sensitivity"
               in plain(DOM), ""))

# =========================================================== identity / versioning / lineage

ID_KINDS = ["Stable logical ID", "Internal surrogate key", "Version identifier",
            "Storage object identifier", "External provider identifier"]
check("versioning", "five identifier kinds are distinguished",
      lambda: (all(k in plain(VER) for k in ID_KINDS), "%d kinds" % len(ID_KINDS)))

check("versioning", "a surrogate key is never a governance identity",
      lambda: ("A surrogate key is not a governance identity by implication" in plain(VER)
               and "never quoted in a governed record" in plain(VER).lower(), ""))

check("versioning", "stable IDs are namespaced, unique and never reused",
      lambda: ("is never reused" in plain(VER)
               and "A duplicate is a failure" in plain(VER)
               and "never stripped" in plain(VER), ""))

PLANES = ["Git commit", "Registry version", "Database record version", "Object version",
          "Snapshot version", "Schema version"]
check("versioning", "six version planes with their own increment authority",
      lambda: (all(p in plain(VER) for p in PLANES), "%d planes" % len(PLANES)))

check("versioning", "mutation, new object and supersession are decided by one stated rule",
      lambda: ("Could a governed record that already exists have relied on the thing you are "
               "about to change?" in plain(VER), ""))

check("versioning", "append-only and immutability scopes are both named",
      lambda: ("Where append-only is mandatory" in plain(VER)
               and "Where immutability is mandatory" in plain(VER), ""))

check("versioning", "lineage cycles are a detected defect, not tolerated",
      lambda: ("is a defect and is detected rather than tolerated" in plain(VER)
               and "may not form a cycle either" in plain(VER), ""))

check("versioning", "historical references are recorded values, never pointers to current state",
      lambda: ("stores its references as recorded values" in plain(VER)
               and "what was it then" in plain(VER)
               and "silently substitutes current values for recorded ones is a defect"
               in plain(VER), ""))

check("versioning", "the reproducibility rule reaches the master architecture",
      lambda: ("as literal recorded values" in plain(A)
               and "any join to current state is an enrichment, never the record" in plain(A), ""))

# =========================================================== consistency / transactions


def consistency_rows():
    body = VER.split("## 5. Six consistency boundaries")[1].split("## 6.")[0]
    return [ln for ln in body.splitlines()
            if ln.startswith("| ") and not re.match(r"^\|[\s:|-]+\|\s*$", ln)][1:]


check("consistency", "six consistency boundaries, each with a stated requirement",
      lambda: (lambda r: (len(r) == 6, "%d boundaries" % len(r)))(consistency_rows()))


def strong_where_a_claim_is_recorded():
    """The four governance-claim operations must be strong; the two-system one must not claim to be."""
    rows = consistency_rows()
    problems = []
    for r in rows:
        cells = [plain(c).strip() for c in r.strip().strip("|").split("|")]
        subject, mode = cells[1], cells[2]
        if "artifact metadata" in subject.lower():
            if "Not atomic" not in mode:
                problems.append("the two-system boundary claims atomicity: %s" % mode)
        elif not mode.startswith("Strong"):
            problems.append("%s is %s" % (subject[:40], mode))
    return (not problems, str(problems) if problems
            else "four governance claims strong; the cross-system boundary declared non-atomic")


check("consistency", "governance claims commit strongly; the cross-system one does not pretend to",
      strong_where_a_claim_is_recorded)

check("consistency", "no distributed atomicity is claimed across the three systems",
      lambda: ("No distributed atomicity is claimed across the three systems" in plain(STD)
               and "no amount of design makes them one act" in plain(VER), ""))

check("consistency", "a declared commit order and a named compensating pattern exist",
      lambda: ("Declared commit order" in plain(VER)
               and "reconciliation sweep" in plain(VER)
               and "Neither direction is repaired by inventing the missing half" in plain(VER), ""))

check("consistency", "the metadata record commits last and is read first",
      lambda: ("The metadata record is committed last and read first" in plain(STD)
               and "orphaned" in plain(STD).lower()
               and "never adopted by a later record" in plain(VER), ""))

# =========================================================== artifact / object model


def artifact_fields():
    body = ART.split("## 2. The artifact record")[1].split("## 3.")[0]
    return [ln for ln in body.splitlines() if re.match(r"^\| \d+ \|", ln)]


check("artifact", "the artifact record carries twenty-two numbered fields",
      lambda: (lambda n: (n == 22, "%d fields" % n))(len(artifact_fields())))

REQUIRED_ARTIFACT_FIELDS = ["Artifact stable ID", "Storage location reference", "Display name",
                            "Media type", "Size", "Content hash", "Encryption state", "Scope",
                            "Sensitivity labels", "Residency constraints", "Provenance",
                            "Producer", "Creation time", "Retention class", "Legal hold",
                            "Immutable snapshot flag", "Supersedes", "Governance links",
                            "Lifecycle status"]
check("artifact", "every required artifact field is present",
      lambda: (lambda missing: (not missing, str(missing) if missing
                                else "%d required fields" % len(REQUIRED_ARTIFACT_FIELDS)))(
          [f for f in REQUIRED_ARTIFACT_FIELDS if f not in plain(ART)]))

check("artifact", "a path or filename never defines artifact identity",
      lambda: ("A file path or filename never defines artifact identity" in plain(ART)
               and "A file path or filename defines nothing" in plain(STD), ""))

check("artifact", "object bytes are new-version-only, never mutated in place",
      lambda: ("Object bytes are never mutated in place" in plain(ART)
               and "in-place mutation would silently change what that record said"
               in plain(ART), ""))


def four_hash_uses():
    body = ART.split("## 4. Four uses of a hash")[1].split("## 5.")[0]
    rows = [ln for ln in body.splitlines()
            if ln.startswith("| ") and not re.match(r"^\|[\s:|-]+\|\s*$", ln)][1:]
    return (len(rows) == 4 and "A hash is not the ID" in plain(body),
            "%d uses, identity explicitly excluded" % len(rows))


check("artifact", "four hash uses kept apart and identity is not one of them", four_hash_uses)

check("artifact", "a content hash never becomes the governance ID",
      lambda: ("A content hash is integrity, not identity" in plain(STD)
               and "never becomes the governance ID" in plain(STD), ""))

check("artifact", "the hash algorithm is abstract, with the identifier stored alongside",
      lambda: ("collision-resistant cryptographic digest" in plain(ART)
               and "algorithm identifier stored alongside every digest" in plain(ART), ""))

check("artifact", "a purge leaves a tombstone and the audit history",
      lambda: ("Tombstone retained" in plain(ART)
               and "never removes the artifact's audit history" in plain(ART), ""))

# =========================================================== sensitivity


def no_ordinal_sensitivity():
    """No scalar ceiling or ordinal comparison over Phase 8 sensitivity classes."""
    patterns = [r"MAX_DATA_SENSITIVITY", r"maximum (approved )?(data )?sensitivity",
                r"sensitivity[^.]{0,40}at or above", r"at or above[^.]{0,40}sensitivity",
                r"highest[^.]{0,30}sensitivity", r"sensitivity (level|ceiling|score|rank)"]
    hits = []
    for rel, doc in DOCS.items():
        flat = plain(doc)
        for pat in patterns:
            for m in re.finditer(pat, flat, re.I):
                if DENIAL_MARKER.search(line_of(flat, m.start())):
                    continue
                hits.append("%s: %s" % (rel, m.group(0)))
    return (not hits, str(sorted(set(hits))) if hits else "0 ordinal sensitivity constructs")


check("sensitivity", "no scalar sensitivity ceiling is introduced anywhere in Phase 10",
      no_ordinal_sensitivity)

check("sensitivity", "sensitivity is persisted as a set of labels",
      lambda: ("Sensitivity is a set of labels, never a level" in plain(STD)
               and "a set of phase 8 classes" in plain(DOM).lower()
               and "Sensitivity labels: a set" in plain(TMPL["storage-record-template.md"]), ""))

check("sensitivity", "storage eligibility is a superset test with obligations per label",
      lambda: ("superset" in plain(ART).lower()
               and "unknown support is not support" in plain(ART).lower()
               and "No ceiling, no ordering" in plain(ART), ""))

check("sensitivity", "the subset test is reused from Phase 9 rather than redefined",
      lambda: ("the Phase 9 subset test applied to storage" in plain(ART)
               and "without modification" in plain(ART), ""))

check("sensitivity", "unknown classification denies by default",
      lambda: ("Unknown classification is not permission" in plain(STD)
               and "Unknown classification denies by default" in plain(ACL)
               and "Unassessed is not" in plain(ACL), ""))

check("sensitivity", "metadata may be central where the payload may not follow",
      lambda: ("Where payloads may not go" in plain(ART)
               and "may not follow it automatically" in plain(ART), ""))

# =========================================================== access control / RLS


def acl_dimension_rows():
    body = ACL.split("## 2. Seven access dimensions")[1].split("## 3.")[0]
    return [ln for ln in body.splitlines() if re.match(r"^\| \d+ \|", ln)]


check("access-control", "seven access dimensions are defined",
      lambda: (lambda n: (n == 7, "%d dimensions" % n))(len(acl_dimension_rows())))

check("access-control", "database authorisation is enforcement, never governance authority",
      lambda: ("Database authorisation is enforcement, not governance" in plain(STD)
               and "It never decides whether the act that operation records was authorised"
               in plain(ACL), ""))

ACL_DENIALS = ["Role Card competence != database permission",
               "Decision Right holder eligibility != database role",
               "Human signatory authority != service account capability"]
check("access-control", "the three authority collapses are denied individually",
      lambda: (lambda missing: (not missing, str(missing) if missing else "3 denials"))(
          [d for d in ACL_DENIALS if d not in plain(ACL)]))

check("access-control", "no Decision Right collapses into a grant or a policy",
      lambda: ("Possession of a credential grants no authority" in plain(STD)
               and "A Right is never created by a database write" in plain(SOT)
               and "no column, grant, policy or service account promotes anything"
               in plain(DOCS["storage/exemplars/canonical-record-version-linkage.md"]).lower(), ""))

check("access-control", "a model or provider gains no authority from a credential",
      lambda: ("gains no authority by holding a credential" in plain(ACL)
               and "Phase 9 already denies that capability confers authority" in plain(ACL), ""))

check("access-control", "operations that no policy may grant are absent, not withheld",
      lambda: ("Operations that no policy may grant" in plain(ACL)
               and "These are absent capabilities, not withheld ones" in plain(ACL), ""))

check("access-control", "deny-by-default covers sensitive domains and unknown classification",
      lambda: ("Deny by default, including for unknown" in plain(ACL)
               and "deny by default" in plain(ACL).lower(), ""))

check("access-control", "governed records name the human act and the system identity separately",
      lambda: ("Two fields, never one" in plain(ACL)
               and "two separate fields" in plain(TMPL["audit-event-template.md"]), ""))

check("access-control", "portable authorisation is separated from the backend mechanism",
      lambda: ("Where portable authorisation ends and the backend begins" in plain(ACL)
               and "must remain expressible if the mechanism changes" in plain(ACL), ""))

check("access-control", "no live policy, role, account or grant is created",
      lambda: ("defines no policy, creates no role, grants no permission, names no account"
               in plain(ACL), ""))

# =========================================================== audit / provenance

HISTORIES = ["Operational log", "Audit event", "Decision Record", "Knowledge provenance",
             "Git commit history"]
check("audit", "four operational histories plus the repository's are kept apart",
      lambda: (all(h in plain(AUD) for h in HISTORIES)
               and "An audit event is not a Decision Record, is not a Git commit, and is not "
               "an operational log" in plain(AUD), "%d histories" % len(HISTORIES)))


def audit_event_fields():
    body = AUD.split("## 2. The audit event")[1].split("## 3.")[0]
    return [ln for ln in body.splitlines() if re.match(r"^\| \d+ \|", ln)]


check("audit", "the audit event carries eleven numbered fields",
      lambda: (lambda n: (n == 11, "%d fields" % n))(len(audit_event_fields())))

check("audit", "a Decision Record reference is required for authority-bearing change classes",
      lambda: ("absent is a failure for those classes, not a blank field" in plain(AUD).lower()
               and "absent is a failure, not a blank field"
               in plain(TMPL["audit-event-template.md"]).lower(), ""))

check("audit", "the audit log is append-only and a correction is an appended event",
      lambda: ("Correction is an appended event" in plain(AUD)
               and "the original stands" in plain(AUD).lower(), ""))

check("audit", "an unenforceable immutability claim is recorded as a gap, not asserted",
      lambda: ("the limitation is recorded rather than assumed away" in plain(AUD)
               and "claims immutability it cannot produce is worse" in plain(AUD), ""))

check("audit", "an operational log is never evidence",
      lambda: ("An operational log is not evidence" in plain(STD)
               and "nothing that must survive lives only here" in plain(AUD), ""))

check("audit", "provenance and audit are not derived from one another",
      lambda: ("Provenance is not audit" in plain(AUD)
               and "neither is derived from the other" in plain(AUD), ""))

# =========================================================== GitHub boundary

check("github", "GitHub is authoritative for definitions and architecture history",
      lambda: ("authoritative for definitions" in plain(A)
               and "never what happened at" in plain(A), ""))

check("github", "approval is a committed record, not a movable tag",
      lambda: ("a tag is movable and an approval is not" in plain(A), ""))

check("github", "architecture, tooling and executable code are separated",
      lambda: ("Architecture versus executable code" in plain(A)
               and "implements no part of the system" in plain(A), ""))

check("github", "the repository versions migrations without becoming the operational database",
      lambda: ("GitHub versions migrations; the database applies them" in plain(STD)
               and "does not hold, mirror or reconstruct the operational database" in plain(A)
               and "compatibility declaration" in plain(A).lower(), ""))

check("github", "branch protection is stated as a requirement and not claimed as configured",
      lambda: ("Branch protection is a requirement, not an observation" in plain(A)
               and "not claimed anywhere in Phase 10" in plain(A)
               and "asserts nothing about the forge" in plain(A), ""))

check("github", "what must never be committed is listed specifically",
      lambda: (all(t in plain(A) for t in ["Secret values", "private keys",
                                           "raw sensitive source payloads", "database dump"]),
               ""))

# =========================================================== secrets

check("secrets", "secret values never enter the repository or the database",
      lambda: ("Secret values never enter the repository or the operational database"
               in plain(STD)
               and "Values never enter the repository or the operational database"
               in plain(SEC), ""))

check("secrets", "a reference is stored and is inert",
      lambda: ("secret reference" in plain(SEC).lower()
               and "It is inert: it authorises nothing" in plain(SEC), ""))

check("secrets", "rotation and revocation are separate acts and compromise needs both",
      lambda: ("Compromise requires both" in plain(SEC), ""))

check("secrets", "secrets are environment-specific and never shared",
      lambda: ("No secret is shared across environments" in plain(SEC), ""))

check("secrets", "secret metadata is auditable without exposing the value",
      lambda: ("Metadata about a secret is not a secret" in plain(STD)
               and "The value never is" in plain(STD), ""))

check("secrets", "runtime credential and governance identity are separated in both directions",
      lambda: ("Neither implies the other, in either direction" in plain(SEC)
               and "gains no authority by possessing credentials" in plain(SEC), ""))

check("secrets", "no secrets vendor is mandated",
      lambda: ("no specific vendor is mandated here" in plain(SEC), ""))

# =========================================================== migration / environments

MIGRATION_ELEMENTS = ["Migration ID and version", "Forward migration",
                      "Rollback versus forward-fix", "Compatibility window", "Data backfill",
                      "Destructive-change control", "Migration evidence",
                      "Schema version recording", "History immutability"]
check("migration", "every migration governance element is defined",
      lambda: (lambda missing: (not missing, str(missing) if missing
                                else "%d elements" % len(MIGRATION_ELEMENTS)))(
          [e for e in MIGRATION_ELEMENTS if e not in plain(MIG)]))

check("migration", "destructive migrations may not declare a rollback",
      lambda: ("Destructive migrations may not" in plain(MIG)
               and "corrected by forward fix" in plain(MIG).lower(), ""))

check("migration", "destructive change requires a named Right exercised beforehand",
      lambda: ("Destructive change requires a named human decision" in plain(STD)
               and "never inferred from the migration being written" in plain(STD)
               and "before the migration is written" in plain(MIG).lower(), ""))

check("migration", "schema version mismatch blocks rather than degrades",
      lambda: ("blocks on mismatch rather than degrading" in plain(MIG)
               and "A mismatch blocks rather than degrades" in plain(STD), ""))

check("migration", "the two migration authorities are kept apart",
      lambda: ("The repository is the authority for what a migration is. The environment is "
               "the authority for what has been applied." in plain(MIG)
               and "Neither can answer the other's question" in plain(MIG), ""))

check("migration", "three environments with separated data, credentials and storage",
      lambda: (all(e in plain(MIG) for e in ["Development", "Test / staging", "Production"])
               and "Storage separation" in plain(MIG)
               and "makes environment separation a naming convention" in plain(MIG), ""))

check("migration", "production data is never cloned into a lower environment",
      lambda: ("Production data is not test data" in plain(STD)
               and "Production data is never cloned downward" in plain(MIG)
               and "is an incident" in plain(MIG), ""))

check("migration", "the promotion path is forward-only and a hotfix is not an exception",
      lambda: ("forward only" in plain(MIG).lower()
               and "a hotfix is not an exception" in plain(MIG).lower(), ""))

check("migration", "architecture is separated from unobservable configuration",
      lambda: ("What is architecture and what is configuration" in plain(MIG)
               and "makes no claim about the current configuration" in plain(MIG), ""))

# =========================================================== backup / retention / recovery

check("backup", "a backup is neither an archive nor an audit trail",
      lambda: ("Backups are not an archive and not an audit trail" in plain(STD)
               and "A backup is not an archive and not an audit trail" in plain(BAK)
               and "its expiry is not a deletion guarantee" in plain(BAK), ""))

RECOVERY_CLASSES = ["RECOVERY_CRITICAL", "RECOVERY_STANDARD", "RECOVERY_DERIVABLE",
                    "RECOVERY_TRANSIENT"]
check("backup", "recovery classes replace invented RPO/RTO numbers",
      lambda: (all(c in BAK for c in RECOVERY_CLASSES)
               and "No RPO or RTO number appears in Phase 10" in plain(BAK),
               "%d classes" % len(RECOVERY_CLASSES)))


def no_invented_recovery_numbers():
    """A concrete RPO/RTO figure anywhere in Phase 10 is the defect this prevents."""
    hits = []
    for rel, doc in DOCS.items():
        for m in re.finditer(r"(?i)\b(RPO|RTO)\b[^.\n]{0,40}?(\d+)\s*(minute|hour|second|day)",
                             plain(doc)):
            hits.append("%s: %s" % (rel, m.group(0)))
    return (not hits, str(hits) if hits else "no concrete recovery objective invented")


check("backup", "no concrete recovery objective is invented", no_invented_recovery_numbers)


def deletion_acts():
    body = BAK.split("## 4. Six distinct acts")[1].split("### 4.1")[0]
    return [ln for ln in body.splitlines() if re.match(r"^\| \d+ \|", ln)]


check("backup", "six deletion-adjacent acts are distinguished",
      lambda: (lambda n: (n == 6, "%d acts" % n))(len(deletion_acts())))

check("backup", "legal hold outranks every retention rule and its gaps are recorded",
      lambda: ("Legal hold outranks every retention rule" in plain(STD)
               and "the limitation is recorded" in plain(STD)
               and "recorded as a known gap" in plain(BAK), ""))

check("backup", "supersession is none of the six acts",
      lambda: ("Supersession is none of the six" in plain(BAK)
               and "does not disappear because its current representation was superseded"
               in plain(BAK), ""))

check("backup", "a purge leaves a tombstone and remains answerable",
      lambda: ("What a purge never removes" in plain(BAK)
               and "an audit of the purge becomes impossible" in plain(BAK), ""))

check("backup", "a restore is authorised, audited, reconciled and re-applies terminal states",
      lambda: ("A restore is not an undo" in plain(BAK)
               and "re-retracted" in plain(BAK)
               and "Restore testing" in plain(BAK), ""))

check("backup", "backups are not reachable with the credentials that write live data",
      lambda: ("cannot" in plain(BAK).lower()
               and "a copy reachable with the same credential is not a backup" in plain(BAK), ""))

check("backup", "retention windows are policy classes, never literal dates in a record",
      lambda: ("never a literal embedded in a record" in plain(BAK)
               and "a named class, never a literal date"
               in plain(TMPL["artifact-record-template.md"]), ""))

# =========================================================== failure modes


def failure_rows():
    body = FAIL.split("| # | Failure |")[1].split("## The two rules")[0]
    return [ln for ln in body.splitlines() if re.match(r"^\| \d+ \|", ln)]


check("failure-modes", "fifteen failure modes, each with a detection and an outcome",
      lambda: (lambda r: (len(r) == 15 and all(len(x.strip().strip("|").split("|")) == 5
                                               for x in r), "%d modes" % len(r)))(failure_rows()))

OUTCOMES = ["BLOCK", "RETRY", "RECONCILE", "ESCALATE", "QUARANTINE", "RESTORE", "HUMAN REVIEW"]


def every_mode_has_a_declared_outcome():
    bad = []
    for row in failure_rows():
        cells = [plain(c).strip() for c in row.strip().strip("|").split("|")]
        if not any(o in cells[3] for o in OUTCOMES):
            bad.append("mode %s outcome cell: %s" % (cells[0], cells[3][:40]))
    return (not bad, str(bad) if bad
            else "all %d modes carry an outcome from the fixed vocabulary" % len(failure_rows()))


check("failure-modes", "every mode's outcome comes from the fixed vocabulary",
      every_mode_has_a_declared_outcome)

REQUIRED_MODES = ["Database unavailable", "metadata transaction fails", "object upload fails",
                  "Content hash mismatch", "Object missing", "Stale schema version",
                  "Dangling cross-registry reference", "Duplicate stable ID",
                  "Conflicting version write", "Incomplete migration", "stale backup",
                  "Storage provider outage", "Secret compromise",
                  "Access-control misconfiguration", "public exposure"]
check("failure-modes", "every required failure case is modelled",
      lambda: (lambda missing: (not missing, str(missing) if missing
                                else "%d required cases" % len(REQUIRED_MODES)))(
          [m for m in REQUIRED_MODES if m.lower() not in plain(FAIL).lower()]))

check("failure-modes", "a dangling reference is never repointed at a current equivalent",
      lambda: ("Never repointed at a current equivalent" in plain(FAIL)
               and "Repointing a dangling reference at" in plain(DOM), ""))

check("failure-modes", "silently continuing is never an outcome",
      lambda: ("What is never an outcome" in plain(FAIL)
               and "Silently continuing" in plain(FAIL)
               and "converts a detectable failure into an undetectable one" in plain(FAIL), ""))

check("failure-modes", "no failure relaxes a constraint",
      lambda: ("No failure relaxes a constraint" in plain(FAIL)
               and "Phase 9 established this for routing" in plain(FAIL), ""))

# =========================================================== anti-lock-in


def adapter_rows():
    body = A.split("## 8. Anti-lock-in: five adapter boundaries")[1].split("## 9.")[0]
    return [ln for ln in body.splitlines()
            if ln.startswith("| ") and not re.match(r"^\|[\s:|-]+\|\s*$", ln)][1:]


check("anti-lock-in", "five adapter boundaries, each splitting portable from vendor-specific",
      lambda: (lambda r: (len(r) == 5 and all(len(x.strip().strip("|").split("|")) == 3
                                              for x in r), "%d boundaries" % len(r)))(
          adapter_rows()))

check("anti-lock-in", "no governance semantic depends on a backend-specific feature",
      lambda: ("No governance semantic in Phases 1-10 depends on a Supabase-specific feature"
               in plain(A).replace("–", "-")
               and "Provider independence is a boundary, not a preference" in plain(STD), ""))

check("anti-lock-in", "the current backend is named as current, not as architecture",
      lambda: ("Supabase is the current PostgreSQL and object-storage implementation"
               in plain(A), ""))

# =========================================================== templates and exemplars

check("templates", "three templates are present and remain PROPOSED",
      lambda: (len(TEMPLATES) == 3 and all("Status: PROPOSED" in DOCS[t] for t in TEMPLATES),
               "%d: %s" % (len(TEMPLATES), [os.path.basename(t) for t in TEMPLATES])))

check("templates", "every template inherits the standard",
      lambda: (all("standard.storage.common_constraints" in DOCS[t] for t in TEMPLATES), ""))

check("templates", "the standard's numbering is contiguous from 1",
      lambda: (lambda nums: (nums == list(range(1, len(nums) + 1)),
                             "%d contiguous rules" % len(nums)))(
          [int(n) for n in re.findall(r"^## (\d+)\. ", STD, re.M)]))

check("templates", "no template records a secret value or a credential",
      lambda: (all("Never a key, never a secret value" in plain(TMPL["artifact-record-template.md"])
                   for _ in [0])
               and "holds no secret value and no credential"
               in plain(TMPL["storage-record-template.md"]).lower(), ""))

check("exemplars", "five exemplars on disk, each PROPOSED and synthetic",
      lambda: (len(EXEMPLARS) == 5
               and all("Status: PROPOSED" in DOCS[e] for e in EXEMPLARS)
               and all("synthetic" in plain(DOCS[e]).lower() for e in EXEMPLARS),
               "%d: %s" % (len(EXEMPLARS), [os.path.basename(e) for e in EXEMPLARS])))

EXEMPLAR_PROOFS = {
    "artifact-metadata-and-object-reference.md": "the path is an address",
    "canonical-record-version-linkage.md": "storing the record is not what promoted it",
    "cross-system-partial-failure.md": "neither half is ever completed by inventing the other",
    "restricted-multi-label-storage.md": "not a comparison against a ceiling",
    "schema-migration-governance.md": "authorised before it exists",
}
for _fname, _needle in EXEMPLAR_PROOFS.items():
    check("exemplars", "exemplar %s states what it proves" % _fname.replace(".md", ""),
          (lambda f=_fname, n=_needle: ("storage/exemplars/" + f in DOCS
                                        and n in plain(DOCS["storage/exemplars/" + f]), "")))

check("exemplars", "the migration exemplar blocks rather than inventing a Decision Right",
      lambda: (lambda d: ("NO_APPLICABLE_DECISION_RIGHT" in d
                          and "was not written" in plain(d)
                          and "is a Phase 7 act" in plain(d), ""))(
          DOCS["storage/exemplars/schema-migration-governance.md"]))

check("exemplars", "the partial-failure exemplar refuses to adopt the orphan",
      lambda: (lambda d: ("never adopted by a later record" in plain(d)
                          and "No distributed transaction was attempted" in plain(d), ""))(
          DOCS["storage/exemplars/cross-system-partial-failure.md"]))

# =========================================================== regression / hygiene

for _label, _paths in UPSTREAM_PATHS.items():
    check("regression", "%s unchanged since the Phase 9 approval baseline" % _label,
          (lambda p=_paths: (lambda r: (r[0], ", ".join(r[1]) or "clean"))(git_unchanged(p))))

check("regression", "every Phase 10 artifact remains PROPOSED",
      lambda: (lambda bad: (not bad, str(bad) if bad
                            else "%d artifacts, all PROPOSED" % len(DOCS)))(
          [rel for rel, doc in DOCS.items()
           if not re.search(r"^Status: (\*\*)?PROPOSED", doc, re.M)]))

check("regression", "no Phase 10 artifact claims APPROVED or CANONICAL status",
      lambda: (lambda bad: (not bad, str(bad) if bad else "0 approval claims"))(
          [rel for rel, doc in DOCS.items()
           if re.search(r"Status:[^\n]*\b(APPROVED|CANONICAL)\b", doc)]))

# --- self-inspection region (excluded from its own scans) ---
RUNTIME = re.compile(  # self-literal
    r"\b(import psycopg|import asyncpg|supabase\.create|createClient|"  # self-literal
    r"CREATE TABLE|ALTER TABLE|DROP TABLE|INSERT INTO|SELECT \*|"  # self-literal
    r"CREATE POLICY|GRANT ALL|api[_-]?key|bearer token|POST /|https?://|"  # self-literal
    r"service_role|anon key|pip install|npm install)\b", re.I)  # self-literal
SECRET_SHAPES = re.compile(  # self-literal
    r"(?:BEGIN [A-Z ]*PRIVATE KEY|"  # self-literal
    r"postgres(?:ql)?://[^\s]+:[^\s]+@|"  # self-literal
    r"\b(?:password|passwd|secret|token)\s*[:=]\s*['\"][^'\"\s]{8,})", re.I)  # self-literal
SELF_START = "# --- self-inspection region (excluded from its own scans) ---"
SELF_END = "# --- end self-inspection region ---"
# --- end self-inspection region ---


def harness_body():
    """This file minus the region that holds the patterns, so a scan cannot match its own text."""
    kept, skipping = [], False
    for line in read("validation/phase_10_validation.py").splitlines():
        if line.strip() == SELF_START:
            skipping = True
            continue
        if line.strip() == SELF_END:
            skipping = False
            continue
        if skipping or line.rstrip().endswith("# self-literal"):
            continue
        kept.append(line)
    return "\n".join(kept)


def no_runtime_implementation():
    hits = []
    # No suppression: these are executable constructs, not vocabulary. An architecture
    # document has no legitimate reason to contain one, denied or otherwise.  # self-literal
    for rel, doc in DOCS.items():
        for m in RUNTIME.finditer(doc):
            hits.append("%s: %s" % (rel, m.group(0)))
    for m in RUNTIME.finditer(harness_body()):
        hits.append("harness: %s" % m.group(0))
    return (not hits, str(sorted(set(hits))) if hits else "0 runtime constructs")


check("regression", "no runtime, schema, client or policy implementation is introduced",
      no_runtime_implementation)


def no_committed_secret():
    hits = []
    for rel, doc in DOCS.items():
        for m in SECRET_SHAPES.finditer(doc):
            hits.append("%s: %s" % (rel, m.group(0)[:40]))
    for m in SECRET_SHAPES.finditer(harness_body()):
        hits.append("harness: %s" % m.group(0)[:40])
    return (not hits, str(hits) if hits else "0 secret-shaped strings in any Phase 10 artifact")


check("regression", "no secret, key or credential shape appears in any artifact",
      no_committed_secret)


def no_vacuous_checks():
    """A check that cannot fail is worse than a missing one: it reports confidence."""
    t = "Tr" + "ue"
    patterns = {"or-true": r"\bor %s\b" % t,
                "or-not-false": r"\bor not Fa" + r"lse\b",
                "lambda-true": r"lambda:\s*\(?%s\)?\s*[,)]" % t,
                "assert-true": r"\bassert %s\b" % t,
                "hard-coded pass count": r"passed\s*=\s*\d+"}
    body = harness_body()
    found = [label for label, pat in patterns.items() if re.search(pat, body)]
    return (not found, str(found) if found else "0 vacuous constructs across %d patterns"
            % len(patterns))


check("regression", "harness contains no vacuous or unconditional-pass checks", no_vacuous_checks)


def harness_is_read_only():
    body = harness_body()
    writes = re.findall(r"open\([^)]*['\"][wa]['\"]", body) + re.findall(r"\bos\.remove\b", body)
    gitcmds = set(re.findall(r'"git", "(\w+)"', body))
    return (not writes and gitcmds <= {"diff", "status", "log", "rev-parse"},
            "writes=%d, git verbs=%s" % (len(writes), sorted(gitcmds)))


check("regression", "harness writes nothing and runs only read-only git", harness_is_read_only)


def no_local_pr_action():
    """Honest scope: a local script cannot prove a remote open-PR count and does not claim to."""
    body = harness_body()
    claims_remote = re.search(r"(?i)no open (pull request|pr)s? (exist|remain)", body)
    return (claims_remote is None,
            "LOCAL ONLY - remote open-PR state is NOT provable offline and is not claimed")


check("regression", "the harness makes no claim about remote pull-request state", no_local_pr_action)

check("regression", "the Phase 9 approval record is untouched",
      lambda: (lambda r: (r[0], ", ".join(r[1]) or "clean"))(
          git_unchanged(["reviews/phase-9-final-approval.md"])))

check("regression", "no Phase 10 artifact modifies an approved upstream separation",
      lambda: (lambda bad: (not bad, str(bad) if bad else "0 redefinitions"))(
          [rel for rel, doc in NORMATIVE.items()
           for m in re.finditer(r"(?i)(redefin|supersed|replac)\w*\s+(the\s+)?phase\s+[1-9]\b",
                                plain(doc))
           if not DENIAL_MARKER.search(line_of(plain(doc), m.start()))]))

check("regression", "Phase 10 states that it changes no approved semantics",
      lambda: ("Phase 10 changes no approved semantics" in plain(STD)
               and "It adds no governance semantics" in plain(A), ""))

# =========================================================== derived inventory


def inventory_rows():
    body = A.split("| Vocabulary | Members | Owner document |")[1]
    rows = {}
    for line in body.splitlines():
        if not line.startswith("|"):
            if rows:
                break
            continue
        cells = [plain(c).strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        m = re.match(r"(\d+)", cells[1])
        if m:
            rows[cells[0]] = int(m.group(1))
    return rows


AUTHORITATIVE = {
    "Identity denials": len(SEPARATED),
    "Identity facets": len(FACETS),
    "Source-of-truth rows": len(sot_rows()),
    "Data domains": len(domain_rows()),
    "Identifier kinds": len(ID_KINDS),
    "Version planes": len(PLANES),
    "Artifact record fields": len(artifact_fields()),
    "Access dimensions": len(acl_dimension_rows()),
    "Audit event fields": len(audit_event_fields()),
    "Consistency boundaries": len(consistency_rows()),
    "Deletion acts": len(deletion_acts()),
    "Failure modes": len(failure_rows()),
    "Adapter boundaries": len(adapter_rows()),
    "Common storage constraints": len(re.findall(r"^## (\d+)\. ", STD, re.M)),
    "Templates": len(TEMPLATES),
    "Exemplars": len(EXEMPLARS),
}

check("inventory", "every authoritative count is derived from a parsed source",
      lambda: (all(isinstance(v, int) and v > 0 for v in AUTHORITATIVE.values()),
               ", ".join("%s=%d" % kv for kv in sorted(AUTHORITATIVE.items()))))


def inventory_reconciled():
    rows = inventory_rows()
    missing = [k for k in AUTHORITATIVE if k not in rows]
    if missing:
        return (False, "inventory rows not found, so nothing was compared: %s" % missing)
    wrong = ["%s states %d, authoritative %d" % (k, rows[k], AUTHORITATIVE[k])
             for k in AUTHORITATIVE if rows[k] != AUTHORITATIVE[k]]
    return (not wrong, str(wrong) if wrong
            else "%d inventory rows reconciled against parsed sources" % len(AUTHORITATIVE))


check("inventory", "the master inventory table reconciles with every parsed source",
      inventory_reconciled)

NUMBER_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
                "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
                "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
                "nineteen": 19, "twenty": 20, "twenty-one": 21, "twenty-two": 22,
                "twenty-three": 23, "thirty": 30, "thirty-one": 31}


def as_number(token):
    token = token.strip().lower()
    return int(token) if token.isdigit() else NUMBER_WORDS.get(token)


PROSE_CLAIMS = [
    (r"(\S+) identity facets", "Identity facets"),
    (r"(\S+) access dimensions", "Access dimensions"),
    (r"(\S+) numbered fields", None),
    (r"(\S+) failure modes", "Failure modes"),
    (r"(\S+) adapter boundaries", "Adapter boundaries"),
    (r"(\S+) consistency boundaries", "Consistency boundaries"),
    (r"(\S+) identifier kinds", "Identifier kinds"),
    (r"(\S+) version planes", "Version planes"),
    (r"(\S+) distinct acts", "Deletion acts"),
    (r"(\S+) domains", "Data domains"),
    (r"(\S+) exemplars", "Exemplars"),
    (r"(\S+) templates", "Templates"),
]


def prose_counts_reconciled():
    bad = []
    for rel, doc in DOCS.items():
        flat = plain(doc)
        for pattern, key in PROSE_CLAIMS:
            if key is None:
                continue
            for m in re.finditer(pattern, flat, re.I):
                stated = as_number(m.group(1))
                if stated is None or stated == AUTHORITATIVE[key]:
                    continue
                bad.append("%s: '%s' (%s is %d)"
                           % (rel, m.group(0).strip(), key, AUTHORITATIVE[key]))
    return (not bad, str(sorted(set(bad))) if bad
            else "%d quantities reconciled across %d documents" % (len(AUTHORITATIVE), len(DOCS)))


check("inventory", "every prose count reconciles with its parsed source", prose_counts_reconciled)


def heading_list_cardinality():
    words = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7,
             "Eight": 8, "Nine": 9, "Ten": 10, "Eleven": 11, "Fifteen": 15}
    bad = []
    for rel, doc in DOCS.items():
        for m in re.finditer(r"^#{2,3} (?:\d+\.?\w?\. )?(%s) ([a-z][^\n]*)$"
                             % "|".join(words), doc, re.M):
            claimed = words[m.group(1)]
            body = doc[m.end():].split("\n## ")[0].split("\n### ")[0]
            numbered = len(re.findall(r"^\d+\. ", body, re.M))
            rows = [ln for ln in body.splitlines()
                    if ln.startswith("| ") and not re.match(r"^\|[\s:|-]+\|\s*$", ln)]
            table_items = max(0, len(rows) - 1) if rows else 0
            items = numbered or table_items
            if items and items != claimed:
                bad.append("%s: '%s %s' governs %d" % (rel, m.group(1), m.group(2)[:40], items))
    return (not bad, str(bad) if bad else "headings match their lists")


check("inventory", "a heading claiming N items governs a list of N", heading_list_cardinality)


# --- this check must stay last: it counts the suite, itself included ---
_PENDING_FINAL_CHECKS = 1                                              # self-literal


def _freeze_final_counts():
    groups = {}
    for r in RESULTS:
        groups[r["group"]] = groups.get(r["group"], 0) + 1
    groups["inventory"] = groups.get("inventory", 0) + _PENDING_FINAL_CHECKS
    return groups, sum(groups.values())


FINAL_GROUPS, FINAL_TOTAL = _freeze_final_counts()

SELF_CHECK = "reviews/phase-10-foundation-self-check.md"


def self_check_is_current():
    """The producer self-check may not state a total or a group count the suite does not produce."""
    if len(RESULTS) + 1 != FINAL_TOTAL:
        return (False, "the frozen suite shape has drifted: registry holds %d, frozen %d"
                % (len(RESULTS) + 1, FINAL_TOTAL))
    if SELF_CHECK not in DOCS:
        return (False, "no producer self-check found, so nothing was compared")
    doc = DOCS[SELF_CHECK]
    problems = []
    totals = [(int(a), int(b)) for a, b in re.findall(r"\b(\d{2,4})/(\d{2,4})\b", doc)]
    if not totals:
        problems.append("the self-check states no total")
    problems += ["stale total %d/%d" % f for f in totals if f != (FINAL_TOTAL, FINAL_TOTAL)]
    stated = {m.group(1): int(m.group(2))
              for m in re.finditer(r"^\| `([a-z-]+)` \| (\d+) \|", doc, re.M)}
    if not stated:
        problems.append("the self-check states no per-group counts")
    problems += ["%s states %d, suite emits %d" % (g, n, FINAL_GROUPS[g])
                 for g, n in sorted(stated.items())
                 if g in FINAL_GROUPS and n != FINAL_GROUPS[g]]
    problems += ["no such group: %s" % g for g in sorted(stated) if g not in FINAL_GROUPS]
    problems += ["group not stated: %s" % g for g in sorted(FINAL_GROUPS) if g not in stated]
    return (not problems, str(problems) if problems
            else "%d/%d and all %d group counts reconcile with the result registry"
            % (FINAL_TOTAL, FINAL_TOTAL, len(FINAL_GROUPS)))


check("inventory", "the producer self-check states the suite's actual totals", self_check_is_current)


def main():
    verbose = "--verbose" in sys.argv
    as_json = "--json" in sys.argv
    passed = sum(1 for r in RESULTS if r["pass"])
    if as_json:
        print(json.dumps({"total": len(RESULTS), "passed": passed, "results": RESULTS}, indent=2))
    else:
        group = None
        for r in RESULTS:
            if r["group"] != group:
                group = r["group"]
                print("\n[%s]" % group)
            print("  %s  %s" % ("PASS" if r["pass"] else "FAIL", r["name"]))
            if (verbose or not r["pass"]) and r["evidence"]:
                print("        %s" % r["evidence"])
        print("\n=== %d/%d PASS ===" % (passed, len(RESULTS)))
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
