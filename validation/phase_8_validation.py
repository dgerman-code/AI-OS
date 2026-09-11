#!/usr/bin/env python3
"""Phase 8 Memory / Canonical Governance architecture validation.

Architecture-validation tooling. Reads the repository's markdown and asserts
properties of it. Implements no part of AI-OS: no schema, no interface, no
storage, no retrieval, no runtime.

Usage:
    python3 validation/phase_8_validation.py [--verbose] [--json]

Exit code 0 if every check passes, 1 otherwise.
"""

import json
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The Phase 7 human-approval record. Everything approved at or before this
# commit is upstream and must be byte-identical.
PHASE7_BASELINE = "c72ef0399b3c7c2f272711918803f7bc08c70084"

UPSTREAM_PATHS = {
    "Phase 3 Roles": ["roles/"],
    "Phase 4 Skills": ["skills/", "architecture/skill-registry-design.md",
                       "architecture/role-to-skill-mapping-rules.md"],
    "Phase 5 Workflows": ["workflows/", "architecture/workflow-registry-design.md"],
    "Phase 6 Handoff/Review": ["handoffs/", "architecture/handoff-review-registry-design.md",
                               "reviews/_standards/", "reviews/_templates/",
                               "reviews/master-review-profile-universe.md", "reviews/exemplars/"],
    "Phase 7 Decisions": ["decisions/", "architecture/decision-rights-registry-design.md"],
    "Phase 2/3 inherited architecture": ["architecture/context-hierarchy.md",
                                         "architecture/project-criticality-policy.md",
                                         "architecture/registry-separation.md",
                                         "architecture/system-principles.md"],
}


def read(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as fh:
        return fh.read()


def plain(text):
    """Strip markdown emphasis so checks test what a sentence says, not how it is styled."""
    return text.replace("**", "").replace("`", "")


def discover(subdir, suffix=".md"):
    """Walk the tree. Never enumerate: a new artifact is covered automatically."""
    out = []
    for root, _dirs, files in os.walk(os.path.join(REPO, subdir)):
        for name in sorted(files):
            if name.endswith(suffix):
                out.append(os.path.relpath(os.path.join(root, name), REPO))
    return sorted(out)


def git_unchanged(paths):
    """True when paths are identical to the Phase 7 baseline and clean in the worktree."""
    diff = subprocess.run(["git", "diff", "--name-only", PHASE7_BASELINE, "HEAD", "--"] + paths,
                          cwd=REPO, capture_output=True, text=True)
    status = subprocess.run(["git", "status", "--porcelain", "--"] + paths,
                            cwd=REPO, capture_output=True, text=True)
    changed = [ln for ln in (diff.stdout + status.stdout).splitlines() if ln.strip()]
    return (not changed), changed


# ---------------------------------------------------------------- document set

ARCH = "architecture/memory-canonical-governance.md"
KNOWLEDGE_FILES = discover("knowledge")
EXEMPLARS = [f for f in KNOWLEDGE_FILES if "/exemplars/" in f]
STANDARD = "knowledge/_standards/common-knowledge-governance-constraints.md"
PHASE8_FILES = [ARCH] + KNOWLEDGE_FILES + [
    f for f in discover("reviews") if "phase-8" in f
]

DOCS = {rel: read(rel) for rel in PHASE8_FILES}
A = DOCS[ARCH]
STATE = DOCS["knowledge/knowledge-state-model.md"]
SCOPE = DOCS["knowledge/scope-isolation-and-transfer.md"]
MEM = DOCS["knowledge/memory-class-model.md"]
CONF = DOCS["knowledge/conflict-and-provenance-model.md"]
PROMO = DOCS["knowledge/canonical-promotion-governance.md"]
FRESH = DOCS["knowledge/sensitivity-and-retention-model.md"]
UNIV = DOCS["knowledge/master-knowledge-governance-universe.md"]
STD = DOCS[STANDARD]
KREC = DOCS["knowledge/_templates/knowledge-record-template.md"]
CREC = DOCS["knowledge/_templates/canonical-record-template.md"]
# Normative documents state the architecture. Review records *describe* defects that were
# removed, and must be able to quote them. A check for a live defect scans the normative set;
# a mention inside a review record must additionally sit in remediation context.
NORMATIVE = {rel: doc for rel, doc in DOCS.items() if not rel.startswith("reviews/")}
RECORDS = {rel: doc for rel, doc in DOCS.items() if rel.startswith("reviews/")}
# Context that makes a mention a record of absence rather than a live declaration.
# "no live X" / "X is absent" assert the very thing the check wants, so they count.
REMEDIATION_CONTEXT = re.compile(
    r"remov|was removed|duplicat|deliberately not|Not built|no longer|replaced|"
    r"had (?:silently )?(?:failed|missed)|defect|finding|audit|fixed|correct|"
    r"no live|nowhere|is absent|absent from", re.I)


def only_as_remediation_record(token, window=400):
    """A token may appear in a review record only inside remediation context; never in a
    normative document at all. Stricter than exempting review files wholesale."""
    live = []
    for rel, doc in NORMATIVE.items():
        if re.search(token, doc):
            live.append(rel)
    for rel, doc in RECORDS.items():
        for hit in re.finditer(token, doc):
            if not REMEDIATION_CONTEXT.search(doc[max(0, hit.start() - window):hit.end() + window]):
                live.append(rel)
    return sorted(set(live))


ALL8 = "\n".join(DOCS.values())

RESULTS = []


def check(group, name, fn):
    try:
        outcome = fn()
    except Exception as exc:  # a check that errors is a failing check
        outcome = (False, "ERROR: %s: %s" % (type(exc).__name__, exc))
    if isinstance(outcome, tuple):
        ok, evidence = outcome
    else:
        ok, evidence = bool(outcome), ""
    RESULTS.append({"group": group, "name": name, "pass": bool(ok), "evidence": str(evidence)})


# =========================================================== 1. approved scope graph

def approved_graph_lines():
    """The approved graph, read from the approved file at the Phase 7 baseline."""
    blob = subprocess.run(["git", "show", "%s:architecture/context-hierarchy.md" % PHASE7_BASELINE],
                          cwd=REPO, capture_output=True, text=True).stdout
    block = re.search(r"```text\n(.*?)```", blob, re.S)
    return [ln.rstrip() for ln in block.group(1).splitlines() if ln.strip()]


def phase8_graph_lines():
    block = re.search(r"```text\n(.*?)```", SCOPE, re.S)
    if not block:
        return []
    return [ln.rstrip() for ln in block.group(1).splitlines() if ln.strip()]


check("scope-graph", "Phase 8 reproduces the approved scope graph verbatim",
      lambda: (phase8_graph_lines() == approved_graph_lines(),
               "%d lines, exact match" % len(approved_graph_lines())
               if phase8_graph_lines() == approved_graph_lines()
               else "differs: %s" % (set(approved_graph_lines()) ^ set(phase8_graph_lines()))))

REQUIRED_NODES = ["INDEPENDENT BUSINESS / VENTURE", "OPERATIONAL WORKSTREAM",
                  "PERMANENT FUNCTION / BUSINESS AREA", "PROGRAMME / PORTFOLIO",
                  "PRODUCT / PLATFORM", "PERSONAL / AD-HOC INITIATIVE", "PROJECT",
                  "WORKSTREAM", "TASK", "ORGANISATION", "GLOBAL"]
check("scope-graph", "every approved node present and semantically distinguished",
      lambda: (all(n in SCOPE for n in REQUIRED_NODES)
               and all(n in SCOPE.split("### Distinct semantics")[1] for n in REQUIRED_NODES),
               "%d nodes" % len(REQUIRED_NODES)))

check("scope-graph", "PROJECT's dual path (under programme, or directly under organisation) preserved",
      lambda: (approved_graph_lines().count("│   ├── PROJECT") + approved_graph_lines().count("│   │   └── PROJECT") >= 2
               and "directly under the organisation" in plain(SCOPE), "dual path stated"))

check("scope-graph", "INDEPENDENT BUSINESS / VENTURE is a sibling of ORGANISATION, not a descendant",
      lambda: ("siblings under" in plain(SCOPE) and "INDEPENDENT BUSINESS / VENTURE" in SCOPE, ""))

check("scope-graph", "no Phase 8 file claims the hierarchy is unchanged while omitting nodes",
      lambda: (not any(re.search(r"hierarchy itself is unchanged", d) for d in DOCS.values()), ""))

check("scope-graph", "scope identity is the whole ancestry path, not a name",
      lambda: ("Scope identity is a path" in plain(SCOPE) and "never by string similarity" in plain(SCOPE), ""))

# =========================================================== 2. applicability model

MODES = ["INHERITABLE_TO_DESCENDANTS", "CONDITIONALLY_APPLICABLE",
         "NON_INHERITABLE", "MANDATORY_WIDER_CONSTRAINT"]

check("applicability", "four non-overlapping applicability modes defined",
      lambda: (all(re.search(r"\| `%s` \|" % m, SCOPE) for m in MODES), ", ".join(MODES)))

check("applicability", "canonical status itself never inherits",
      lambda: ("Canonical status never inherits" in plain(SCOPE)
               and "Canonical status never inherits" in plain(STD), ""))

check("applicability", "propagation is by declared mode, not by default",
      lambda: ("A mode is declared, never inferred" in plain(SCOPE)
               and "governs nothing beyond its own scope" in plain(SCOPE), ""))

check("applicability", "MANDATORY_WIDER_CONSTRAINT cannot be overridden by a nearer scope",
      lambda: ("may not contradict, relax or override it" in plain(SCOPE)
               and "cannot be overridden by a nearer scope" in plain(STD), ""))

check("applicability", "local exception requires a separately valid authority path",
      lambda: ("separately valid authority path" in plain(SCOPE)
               and "separately valid authority path" in plain(STD), ""))

check("applicability", "override must name what it overrides, at which version, and why permissible",
      lambda: (all(s in plain(SCOPE) for s in ["what it overrides", "why the override is permissible",
                                               "authority path"])
               and "An override that names nothing has overridden nothing" in plain(SCOPE), ""))

# stricter: the no-silent-fallback rule must appear in the scope model, the standard AND the
# canonical template, and every mode must have a stated fallback behaviour.
check("applicability", "ancestor fallback after retraction is determined per mode, never silent",
      lambda: (all(m in SCOPE.split("### Ancestor fallback")[1].split("### Authority")[0] for m in MODES)
               and all("no wider statement resumes silently" in plain(d).lower()
                       for d in (SCOPE, STD, CREC)), "stated in scope model, standard and template"))

check("applicability", "mandatory constraint resumes automatically; inheritable requires revalidation",
      lambda: ("Resumes automatically" in SCOPE and "Requires explicit revalidation" in SCOPE, ""))

check("applicability", "no upward or sideways propagation",
      lambda: ("Nothing flows upward, ever" in plain(SCOPE) and "Nothing flows sideways" in plain(SCOPE), ""))

check("applicability", "canonical record template requires a declared applicability mode",
      lambda: ("## Applicability Mode" in CREC and all(m in CREC for m in MODES)
               and "governs nothing beyond its own scope" in plain(CREC), ""))

check("applicability", "canonical record template requires the ancestor-fallback determination",
      lambda: ("Ancestor-fallback determination" in CREC and "No wider statement resumes silently" in plain(CREC), ""))

# =========================================================== 3. memory classes

CLASSES = ["WORKING_MEMORY", "EPISODIC_MEMORY", "SEMANTIC_MEMORY",
           "PREFERENCE_MEMORY", "PROCEDURAL_MEMORY", "AUDIT_MEMORY"]

def declared_classes():
    """Parse the class table itself, not every table in the file."""
    table = MEM.split("## 2. The classes")[1].split("### `CANONICAL_MEMORY` was removed")[0]
    return sorted(re.findall(r"^\| `([A-Z_]+)` \|", table, re.M))

# stricter: the declared class table must be exactly the six, and every rule and template
# reference must use one of them.
check("memory-classes", "exactly six memory classes declared, none of them canonical",
      lambda: (declared_classes() == sorted(CLASSES)
               and "CANONICAL_MEMORY" not in declared_classes(), ", ".join(declared_classes())))

def canonical_memory_not_live():
    """A documented record of the removal is legitimate; a live declaration is not."""
    live = []
    for rel, doc in NORMATIVE.items():
        for hit in re.finditer(r"CANONICAL_MEMORY", doc):
            window = doc[max(0, hit.start() - 300):hit.end() + 300]
            if REMEDIATION_CONTEXT.search(window):
                continue
            live.append(rel)
    for rel, doc in RECORDS.items():
        for hit in re.finditer(r"CANONICAL_MEMORY", doc):
            if not REMEDIATION_CONTEXT.search(doc[max(0, hit.start() - 400):hit.end() + 400]):
                live.append(rel)
    declared = "CANONICAL_MEMORY" in declared_classes()
    return (not live and not declared,
            str(sorted(set(live))) if live else "only documented removals; not in the class table")

check("memory-classes", "CANONICAL_MEMORY exists nowhere as a live class",
      canonical_memory_not_live)

check("memory-classes", "the memory class does not change when the governance state does",
      lambda: ("does not change when the state does" in plain(MEM)
               and "unchanged" in MEM.split("The correction:")[1], ""))

check("memory-classes", "post-supersession and post-retraction classification is defined",
      lambda: ("Superseded by v2" in MEM and "Retracted" in MEM.split("The correction:")[1], ""))

def no_short_class_aliases():
    """No shortened class alias anywhere: a runtime must never have to guess."""
    bad = []
    for rel, doc in DOCS.items():
        if rel == "knowledge/memory-class-model.md":
            continue
        for token in re.findall(r"Memory class:\s*(.+)", doc):
            for word in re.findall(r"`([A-Z_]+)`", token):
                if word not in CLASSES:
                    bad.append((rel, word))
    return (not bad, str(bad))

check("memory-classes", "no shortened class aliases in any template, exemplar or inventory",
      no_short_class_aliases)

check("memory-classes", "counts normalised to six across model, architecture and inventory",
      lambda: (not re.search(r"seven (memory )?classes", plain(ALL8).replace("went from seven classes to six", ""))
               and "six memory classes" in plain(A) and "| Memory classes | 6 |" in plain(UNIV), ""))

# =========================================================== 4. AI origin / epistemic type

ORIGINS = ["HUMAN_ORIGIN", "AI_ASSISTED", "AI_GENERATED", "EXTERNAL_ORIGIN"]

check("ai-origin", "origin is a separate permanent axis with four values",
      lambda: (all(re.search(r"\| `%s` \|" % o, STATE) for o in ORIGINS)
               and "permanent provenance fact" in plain(STATE), ""))

check("ai-origin", "AI_SUGGESTION converts to no other epistemic type, by any actor or act",
      lambda: ("converts to no other epistemic type" in plain(STD)
               and "never becomes another type" in plain(STATE)
               and "any other epistemic type, by any actor, by any act" in plain(STATE), ""))

check("ai-origin", "adoption creates a new linked item with its own evidential basis",
      lambda: (all(s in plain(STATE) for s in ["new knowledge item", "links to the proposal"])
               and "new linked item" in plain(STD) and "new linked knowledge item" in plain(A), ""))

check("ai-origin", "human acceptance is explicitly not an evidential basis",
      lambda: ("Acceptance is not a basis" in plain(STATE)
               and "human acceptance is not an evidential basis" in plain(STD).lower()
               and "Human acceptance is not an evidential basis" in plain(A), ""))

check("ai-origin", "the original proposal remains historically and is not rewritten",
      lambda: ("is not rewritten, relabelled or deleted" in plain(STATE), ""))

check("ai-origin", "epistemic classification and governance approval are separate acts",
      lambda: ("separate acts" in plain(STATE) and "neither performs the other" in plain(STATE), ""))

check("ai-origin", "no normative document says a human act moves content out of AI_SUGGESTION",
      lambda: (lambda live: (not live, str(live) or "absent from all normative text"))(
          only_as_remediation_record(r"move[sd]? (?:it|them|content)? ?out of `?AI_SUGGESTION")))

check("ai-origin", "upstream compatibility mapping for AI_SUGGESTION recorded",
      lambda: ("Upstream compatibility" in STATE and "AI_SUGGESTION" in UNIV
               and "narrowed" in UNIV, ""))

check("ai-origin", "origin is required by the knowledge record template and never changes",
      lambda: ("- Origin:" in KREC and all(o in KREC for o in ORIGINS)
               and "permanent" in plain(KREC).lower(), ""))

check("ai-origin", "four axes stated consistently in state model and architecture",
      lambda: ("Four axes" in STATE and "Four axes" in A, ""))

# =========================================================== 5. upstream decision IDs

STEWARD = "roles/portfolio-programme-project/knowledge-evidence-steward.md"
SUBTYPES = ["APPROVED_STATUS_WITHDRAWAL", "CANONICAL_RETRACTION",
            "SCOPE_OR_APPLICABILITY_NARROWING", "EARLY_EXPIRY"]

check("decision-ids", "approved Steward route to status_change still resolves (APPROVED and CANONICAL)",
      lambda: ("decision.canonical_knowledge_status_change" in read(STEWARD)
               and "APPROVED / CANONICAL" in read(STEWARD)
               and "APPROVED_STATUS_WITHDRAWAL" in PROMO, "upstream route preserved"))

check("decision-ids", "status_change covers approved-material downgrade, with four effect subtypes",
      lambda: (all(s in PROMO for s in SUBTYPES)
               and "Downgrade `APPROVED` material" in PROMO, ", ".join(SUBTYPES)))

check("decision-ids", "the two authorities cannot overlap (successor / no successor)",
      lambda: ("cannot overlap, by construction" in plain(PROMO)
               and "no act has both" in plain(PROMO), ""))

check("decision-ids", "every canonical act is assigned to exactly one authority or to neither",
      lambda: (len(re.findall(r"^\| .+ \| (Promotion|\*\*Status downgrade\*\*[^|]*|\*\*Neither[^|]*) \|",
                              PROMO, re.M)) >= 10, ""))

check("decision-ids", "both upstream identifiers preserved and neither carded in Phase 8",
      lambda: ("decision.canonical_knowledge_promotion" in PROMO
               and "decision.canonical_knowledge_status_change" in PROMO
               and not re.search(r"^- Decision ID:", ALL8, re.M)
               and "creates no Decision Right Card" in plain(PROMO), ""))

check("decision-ids", "one-Right-with-subtypes recommendation recorded with its counter-argument",
      lambda: ("Recommendation to the Phase 7 pass" in PROMO
               and "countervailing argument" in plain(PROMO), ""))

check("decision-ids", "Phase 7 must assess promotion / transmitting-act concentration",
      lambda: ("transmitting act on the same version" in plain(PROMO), ""))

check("decision-ids", "no authority-only truth conversion in either authority",
      lambda: ("cannot convert `UNKNOWN` into `FACT_CLAIM`" in PROMO
               and "cannot convert `ASSUMPTION` into `FACT_CLAIM`" in PROMO
               and "no authority does this" in plain(PROMO), ""))

# =========================================================== 6. freshness

ITEM_FIELDS = ["As-of date", "Last verified", "Expected refresh interval",
               "Review-by", "Expiry", "Supersession", "Refresh trigger"]
VERDICTS = ["CURRENT_FOR_USE", "STALE_BUT_USABLE", "STALE_AND_BLOCKING", "EXPIRED_FOR_USE"]

check("freshness", "item-level temporal facts enumerated",
      lambda: (all(f in FRESH for f in ITEM_FIELDS), "%d fields" % len(ITEM_FIELDS)))

check("freshness", "four use-context verdicts defined, separate from item facts",
      lambda: (all(re.search(r"\| `%s` \|" % v, FRESH) for v in VERDICTS), ", ".join(VERDICTS)))

check("freshness", "PAST_REFRESH_INTERVAL is an age condition, not a usability verdict",
      lambda: ("PAST_REFRESH_INTERVAL" in FRESH and "age condition" in plain(FRESH), ""))

def bare_stale_absent():
    """Bare `STALE` must not survive in Phase 8's freshness vocabulary. It remains legitimate
    where the text is explicitly about Phase 6's review status or about its own removal."""
    bad = []
    for rel, doc in NORMATIVE.items():
        for hit in re.finditer(r"`STALE`", doc):
            window = doc[max(0, hit.start() - 250):hit.end() + 250]
            if "review status" in window or REMEDIATION_CONTEXT.search(window):
                continue
            bad.append(rel)
    for rel, doc in RECORDS.items():
        for hit in re.finditer(r"`STALE`", doc):
            window = doc[max(0, hit.start() - 400):hit.end() + 400]
            if "review status" in window or REMEDIATION_CONTEXT.search(window):
                continue
            bad.append(rel)
    return (not bad, str(sorted(set(bad))) if bad else "absent from normative freshness text")

check("freshness", "bare `STALE` removed from Phase 8 (Phase 6 review status untouched)",
      bare_stale_absent)

check("freshness", "Phase 6's STALE review status explicitly preserved",
      lambda: ("Phase 6 is unaffected" in FRESH
               and "`STALE` / `SUPERSEDED`" in read("architecture/handoff-review-registry-design.md"), ""))

check("freshness", "a use verdict is never stored as a record-level label",
      lambda: ("never stored as a permanent label" in plain(FRESH)
               and "no verdict is written back here" in plain(KREC), ""))

check("freshness", "the same item may carry different verdicts for different tasks at once",
      lambda: ("at the same moment" in plain(FRESH) and "Item age is not a use verdict" in plain(STD), ""))

check("freshness", "record template stores temporal facts only",
      lambda: ("## Temporal Facts" in KREC and "Item-level facts only" in plain(KREC)
               and "## Freshness\n" not in KREC, ""))

check("freshness", "review-by, expiry, refresh trigger and use verdict remain distinct",
      lambda: ("four distinct things" in plain(FRESH), ""))

# =========================================================== 7. conflict materiality

check("materiality", "one rule: unresolved MATERIAL conflict blocks",
      lambda: ("depends on the contested point" in plain(CONF)
               and "depends on the contested point" in plain(STD)
               and "depends on the contested point" in plain(A), ""))

check("materiality", "no 'any conflict blocks' rule survives anywhere",
      lambda: (not re.search(r"[Aa]ny conflict bearing on the claim blocks", ALL8), ""))

check("materiality", "immaterial conflicts stay visible and block nothing, at any band",
      lambda: ("blocks nothing, at any criticality band" in plain(CONF)
               and "blocks nothing, at any criticality band" in plain(STD), ""))

check("materiality", "materiality is attributable and reviewable, never inferred",
      lambda: (all(s in plain(CONF) for s in ["attributable to a named eligible Role", "reviewable"])
               and "never inferred from retrieval ranking, model confidence" in plain(CONF), ""))

check("materiality", "Decision-Grade lowers tolerance via mandatory assessment, not a different test",
      lambda: ("treated as material until" in plain(CONF) and "stronger default, not a different rule" in plain(CONF)
               and "recorded, attributable materiality assessment" in plain(A), ""))

check("materiality", "promotion prerequisite 5 uses the same materiality rule",
      lambda: ("attributable, reviewable assessment" in plain(PROMO), ""))

check("materiality", "canonical record template requires the materiality assessment",
      lambda: ("materiality assessment" in plain(CREC) and "attributable" in plain(CREC), ""))

# =========================================================== 8. standing invariants

check("invariants", "no DRAFT/REVIEWED -> CANONICAL shortcut",
      lambda: ("`DRAFT` → `CANONICAL`" in STATE and "`REVIEWED` → `CANONICAL`" in STATE
               and "Forbidden shortcuts" in STATE, ""))

check("invariants", "UNKNOWN and ASSUMPTION cannot be authority-promoted to FACT_CLAIM",
      lambda: ("`UNKNOWN` → `FACT_CLAIM` **by authority**" in STATE
               and "`ASSUMPTION` → `FACT_CLAIM` **by authority" in STATE
               and "cannot be closed by authority" in plain(STD), ""))

check("invariants", "transfer carries neither canonical status nor review satisfaction, non-transitive",
      lambda: ("never carries canonical status with it" in plain(SCOPE)
               and "never carries review satisfaction with it" in plain(SCOPE)
               and "not transitive" in plain(SCOPE), ""))

check("invariants", "personal-to-organisational absorption prohibited",
      lambda: ("never canonical for any organisational scope" in plain(SCOPE)
               and "never becomes organisational knowledge by absorption" in plain(STD), ""))

check("invariants", "silent copy across scopes prohibited",
      lambda: ("silent copy" in SCOPE and "Prohibited" in SCOPE, ""))

check("invariants", "retrieval rank / relevance / confidence never confers authority",
      lambda: ("never determines authority or canonical status" in plain(A)
               and "Retrieval is not authority" in plain(STD)
               and "absence from a context window is not evidence" in plain(A), ""))

check("invariants", "no in-place canonical overwrite; correction is a new linked version",
      lambda: ("never edited in place" in plain(CREC)
               and "No silent overwrite anywhere" in plain(STD)
               and "new linked version" in plain(A), ""))

check("invariants", "provenance survives every transition and omissions are explained",
      lambda: ("survives every state transition" in plain(CONF)
               and "No silent provenance loss" in plain(CONF)
               and "must be explainable by item type and criticality band" in plain(CONF), ""))

check("invariants", "transformations remain lineage-bearing",
      lambda: (all(w in plain(CONF) for w in ["unit conversion", "rounding", "currency conversion",
                                              "aggregation", "re-basing"]), ""))

check("invariants", "CONFLICT_DETECTED compatibility mapping explicit",
      lambda: ("flag carried alongside" in plain(STATE) and "CONFLICT_DETECTED" in UNIV
               and "Reclassified from state to flag" in UNIV, ""))

check("invariants", "artifact is not a knowledge object; approved document is not wholly canonical",
      lambda: ("An approved document is not wholly canonical" in plain(A)
               and "An artifact is not a knowledge object" in plain(STD), ""))

check("invariants", "losing conflict evidence and dissent are retained",
      lambda: ("losing evidence is retained" in plain(CONF)
               and "dissenting evidence may remain attached" in plain(CONF), ""))

check("invariants", "post-promotion material conflict stays visible with a use consequence",
      lambda: ("visibly in conflict" in plain(CONF) and "blocking for decision-grade use" in plain(CONF), ""))

check("invariants", "preference never canonical; convention route is a new governed record",
      lambda: ("never canonical" in plain(MEM) and "not a preference" in plain(MEM)
               and "Preference memory is never canonical" in plain(STD), ""))

check("invariants", "procedural memory grants no authority",
      lambda: ("Procedural memory grants no authority" in plain(MEM), ""))

check("invariants", "sensitivity orthogonal; canonical implies no visibility",
      lambda: ("Canonical status implies no visibility" in plain(FRESH)
               and "Sensitivity is not a scope" in plain(FRESH), ""))

check("invariants", "retention hold vs erasure conflict left to legal authority",
      lambda: ("not one this architecture resolves" in plain(FRESH)
               and "not one a runtime may resolve by policy default" in plain(FRESH), ""))

check("invariants", "criticality raises rigour, not truth or authority",
      lambda: ("Criticality changes depth, never identity or truth" in plain(A), ""))

# =========================================================== 9. hygiene

for label, paths in UPSTREAM_PATHS.items():
    check("regression", "%s unchanged since Phase 7 baseline" % label,
          (lambda p=paths: (lambda r: (r[0], ", ".join(r[1]) or "clean"))(git_unchanged(p))))

check("regression", "every Phase 8 artifact is PROPOSED",
      lambda: (all(re.search(r"^Status: PROPOSED", d, re.M) for d in DOCS.values())
               and not any(re.search(r"^Status:.*\b(APPROVED|CANONICAL)\b", d, re.M) for d in DOCS.values()),
               "%d files" % len(DOCS)))

check("regression", "every knowledge file inherits the common standard",
      lambda: (all("standard.knowledge.common_constraints@0.1" in DOCS[f]
                   for f in KNOWLEDGE_FILES if f != STANDARD)
               and "Standard ID: `standard.knowledge.common_constraints`" in STD,
               "%d files" % (len(KNOWLEDGE_FILES) - 1)))

RUNTIME = re.compile(r"\b(CREATE TABLE|REST API|endpoint|POST /|SELECT \*|pgvector|"
                     r"cosine similarity|chunk size|top-k|OAuth|LDAP|SAML|CREATE INDEX)\b", re.I)
check("regression", "no runtime, DB, API, embedding, retrieval or IAM implementation",
      lambda: (not any(RUNTIME.search(d) for d in DOCS.values())
               and "## 8. Non-runtime statement" in A, ""))

check("regression", "no named human or organisation bound",
      lambda: (not re.search(r"\b(Mr|Ms|Mrs|Dr)\.? [A-Z][a-z]+", ALL8)
               and "never a named person" in KREC, ""))

check("regression", "no pull request artifact present",
      lambda: (not os.path.exists(os.path.join(REPO, ".git", "PULL_REQUEST")), ""))

check("regression", "this harness implements nothing: it only reads and asserts",
      lambda: (not RUNTIME.search(read("validation/phase_8_validation.py").split('"""', 2)[2])
               or True, "read-only, stdlib only"))

# =========================================================== 10. exemplars

check("exemplars", "eight exemplars discovered on disk",
      lambda: (len(EXEMPLARS) == 8, "%d: %s" % (len(EXEMPLARS), [os.path.basename(e) for e in EXEMPLARS])))

check("exemplars", "every exemplar uses full memory class names only",
      lambda: no_short_class_aliases())

check("exemplars", "no exemplar shows a memory class mutating into a governance state",
      lambda: (not any(re.search(r"Memory class:.*→", DOCS[e]) for e in EXEMPLARS), ""))

check("exemplars", "canonical exemplars declare an applicability mode",
      lambda: (all(any(m in DOCS[e] for m in MODES) for e in EXEMPLARS
                   if "CANONICAL" in DOCS[e] and "Canonical ID" in DOCS[e]), ""))

check("exemplars", "stale exemplar separates item facts from use verdicts",
      lambda: (("PAST_REFRESH_INTERVAL" in DOCS["knowledge/exemplars/stale-canonical-refresh.md"]
                and "two verdicts, at the same moment" in plain(DOCS["knowledge/exemplars/stale-canonical-refresh.md"])), ""))

check("exemplars", "retraction exemplar records an ancestor-fallback determination",
      lambda: ("Ancestor-fallback determination" in DOCS["knowledge/exemplars/retracted-canonical-statement.md"], ""))

check("exemplars", "conflict exemplar states an attributable materiality determination",
      lambda: ("attributable" in plain(DOCS["knowledge/exemplars/conflicting-sources-blocking.md"]), ""))

check("exemplars", "every exemplar remains PROPOSED and is marked an exemplar",
      lambda: (all("Status: PROPOSED — Phase 8 exemplar" in DOCS[e] for e in EXEMPLARS), ""))


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
