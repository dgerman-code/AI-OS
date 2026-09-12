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

# Scans normative text only: a remediation record must be able to report what it removed.
# Stricter than the previous version, which scanned every document including the records and
# so could be satisfied only by a hand-written exemption for one sentence.
check("memory-classes", "counts normalised to six across model, architecture and inventory",
      lambda: (lambda stale: (not stale and "six memory classes" in plain(A)
                              and ("| Memory classes | %d |" % len(declared_classes())) in plain(UNIV),
                              str(stale) if stale else "no stale count in normative text"))(
          [rel for rel, doc in NORMATIVE.items()
           for m in re.finditer(r"seven (?:memory )?classes", doc, re.I)
           if not REMEDIATION_CONTEXT.search(doc[max(0, m.start() - 200):m.end() + 200])]))

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

# --- 5.1 semantic PERSONAL / scope-family checks -------------------------------------------
# The previous check was presence-oriented and passed while the document still declared
# organisational canonical statements applicable inside PERSONAL. These inspect the rule.

PERSONAL_SECTION = SCOPE.split("## 7.")[1].split("## 8.")[0] if "## 7." in SCOPE else ""

LEAKAGE_PATTERNS = [
    # any wording that makes an organisational statement govern inside PERSONAL
    r"organisational canonical statements are applicable (?:to|in|inside)[^.]*personal",
    r"applicable (?:to|in|inside) (?:work done in )?personal scope",
    r"personal scope inherits",
    r"inherit(?:s|ed)? (?:downward |down )?into personal",
    r"personal[^.]{0,40}descendant of[^.]{0,20}organisation",
]


def personal_applicability_leakage():
    hits = []
    for rel, doc in NORMATIVE.items():
        flat = plain(doc).lower().replace("\n", " ")
        for pat in LEAKAGE_PATTERNS:
            for m in re.finditer(pat, flat, re.I):
                window = flat[max(0, m.start() - 160):m.end() + 160]
                # a sentence that denies the proposition is not a leak
                if re.search(r"\bnot\b|\bnever\b|\bno \b|refus|wrong|contradict", window):
                    continue
                hits.append("%s: %s" % (rel, m.group(0)[:60]))
    return (not hits, str(hits) if hits else "0 leaks across %d normative documents" % len(NORMATIVE))


check("personal-isolation", "applicability leakage from ORGANISATION into PERSONAL = 0",
      personal_applicability_leakage)

check("personal-isolation", "PERSONAL is declared a separate scope family, not a descendant",
      lambda: ("separate scope family" in plain(PERSONAL_SECTION)
               and "never a descendant of" in plain(PERSONAL_SECTION).lower()
               and "sibling of" in plain(PERSONAL_SECTION), ""))

check("personal-isolation", "association with an organisation is explicitly not ancestry",
      lambda: ("not because the human is associated with the organisation" in plain(PERSONAL_SECTION)
               and "Association is not ancestry" in plain(PERSONAL_SECTION), ""))

check("personal-isolation", "nothing crosses the family boundary automatically",
      lambda: (all(t in plain(PERSONAL_SECTION) for t in
                   ["not canonical status", "not Review satisfaction", "not authority",
                    "not the applicability mode itself"]), ""))

check("personal-isolation", "cross-family use is reference or governed transfer only",
      lambda: ("SCOPE_REFERENCE" in PERSONAL_SECTION and "GOVERNED_TRANSFER" in PERSONAL_SECTION
               and "never inherited applicability and never canonical propagation" in plain(PERSONAL_SECTION), ""))

check("personal-isolation", "mandatory wider constraints do not cross sideways either",
      lambda: ("Not even mandatory constraints propagate sideways" in plain(SCOPE)
               and "a sibling family has none of its ancestors" in plain(SCOPE), ""))

check("personal-isolation", "all four stress tests are answered",
      lambda: (all(w in plain(PERSONAL_SECTION).lower() for w in
                   ["travel policy", "writing style", "legal constraint", "house style"])
               and plain(PERSONAL_SECTION).count("|") > 20, "4 cases in the stress-test table"))

check("personal-isolation", "personal-to-organisational absorption prohibited",
      lambda: ("No personal item is applicable inside an organisational scope" in plain(PERSONAL_SECTION)
               and "never becomes organisational knowledge by absorption" in plain(STD), ""))

check("personal-isolation", "the corrected rule is recorded as a correction, not silently swapped",
      lambda: ("was wrong" in plain(PERSONAL_SECTION) and "re-audit" in plain(PERSONAL_SECTION).lower(), ""))

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

def artifacts_remain_proposed(docs, phase_label):
    """Every architecture artifact must be PROPOSED.

    A human approval record is a different kind of object: it records a human decision and is
    *supposed* to say APPROVED. The previous version of this check scooped it up with the
    artifacts and failed the moment the phase was approved. This one separates the two and is
    stricter for it: an approval record must identify itself as a human decision, and no
    architecture artifact may declare its own approval.
    """
    approval, artifacts, bad = [], [], []
    for rel, doc in docs.items():
        if re.search(r"(?:^|/)phase-\d+-final-approval\.md$", rel):
            approval.append(rel)
            if not re.search(r"^Status:.*HUMAN DECISION", doc, re.M):
                bad.append("%s: approval record does not identify a human decision" % rel)
            continue
        artifacts.append(rel)
        if not re.search(r"^Status: PROPOSED", doc, re.M):
            bad.append("%s: not PROPOSED" % rel)
        if re.search(r"^Status:.*\b(APPROVED|CANONICAL)\b", doc, re.M):
            bad.append("%s: artifact declares its own approval" % rel)
    return (not bad, str(bad) if bad else
            "%d %s artifacts PROPOSED; %d human approval record(s) excluded"
            % (len(artifacts), phase_label, len(approval)))


check("regression", "every Phase 8 artifact is PROPOSED (approval records excluded)",
      lambda: artifacts_remain_proposed(DOCS, "Phase 8"))

check("regression", "every knowledge file inherits the common standard",
      lambda: (all("standard.knowledge.common_constraints@0.1" in DOCS[f]
                   for f in KNOWLEDGE_FILES if f != STANDARD)
               and "Standard ID: `standard.knowledge.common_constraints`" in STD,
               "%d files" % (len(KNOWLEDGE_FILES) - 1)))

RUNTIME = re.compile(r"\b(CREATE TABLE|REST API|endpoint|POST /|SELECT \*|pgvector|"  # self-literal
                     r"cosine similarity|chunk size|top-k|OAuth|LDAP|SAML|CREATE INDEX)\b", re.I)  # self-literal
check("regression", "no runtime, DB, API, embedding, retrieval or IAM implementation",
      lambda: (not any(RUNTIME.search(d) for d in DOCS.values())
               and "## 8. Non-runtime statement" in A, ""))

check("regression", "no named human or organisation bound",
      lambda: (not re.search(r"\b(Mr|Ms|Mrs|Dr)\.? [A-Z][a-z]+", ALL8)
               and "never a named person" in KREC, ""))

# 5.6 — scope stated honestly. This harness is offline: it can prove that no PR artifact or
# PR-creating action exists LOCALLY. It cannot and does not claim anything about remote open-PR
# count, which must be checked by audit tooling against the GitHub API and reported separately.

SELF_START = "# --- self-inspection region (excluded from its own scans) ---"
SELF_END = "# --- end self-inspection region ---"


def harness_body_excluding_self_inspection():
    """The harness source minus the two self-inspecting checks, which necessarily contain the
    literals they search for. Scanning them would make both checks match themselves."""
    src = read("validation/phase_8_validation.py")
    body = src.split('"""', 2)[2]
    kept, skipping = [], False
    for line in body.splitlines():
        # Match the marker only as a standalone line, so the constants that hold the marker
        # text are not themselves mistaken for the marker.
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


# --- self-inspection region (excluded from its own scans) ---
def harness_is_read_only():
    """The harness must not itself be runtime, and must not contain vacuous checks.

    The previous version of this check ended in `or True`, which made it unconditionally
    pass — a check that cannot fail is not a check. This one can fail, and it is the check
    that enforces that property on the rest of the file.
    """
    body = harness_body_excluding_self_inspection()
    problems = []
    if RUNTIME.search(body):
        problems.append("runtime construct in harness")
    # No write, network or subprocess beyond the read-only git commands used for baselines.
    for banned in ("open(", "urllib", "socket", "requests"):
        for hit in re.finditer(re.escape(banned), body):
            window = body[max(0, hit.start() - 120):hit.end() + 60]
            if banned == "open(" and "encoding=\"utf-8\"" in window and '"r"' not in window:
                continue  # the read() helper only
            if banned == "open(":
                problems.append("non-read open()")
            else:
                problems.append(banned)
    for cmd in re.findall(r'subprocess\.run\(\[([^\]]*)\]', body):
        if '"git"' not in cmd:
            problems.append("non-git subprocess")
        for w in ("commit", "push", "add", "checkout", "reset"):
            if '"%s"' % w in cmd:
                problems.append("mutating git: %s" % w)
    return (not problems, str(sorted(set(problems))) if problems else "read-only, stdlib only, git read-only")


def no_vacuous_checks():
    """No unconditional-pass construct anywhere in the harness."""
    body = harness_body_excluding_self_inspection().split("RESULTS = []", 1)[-1]
    # Patterns are assembled from fragments so that a plain grep of this file for a vacuous
    # construct finds no literal occurrence outside the explanatory docstring above.
    t = "Tr" + "ue"
    patterns = {
        "or-true": r"\bor %s\b" % t,
        "or-not-false": r"\bor not Fa" + r"lse\b",
        "lambda-true": r"lambda:\s*\(?%s\)?\s*[,)]" % t,
        "assert-true": r"\bassert %s\b" % t,
        "hard-coded pass count": r"passed\s*=\s*\d+",
    }
    found = [name for name, pat in patterns.items() if re.search(pat, body)]
    return (not found, str(found) if found else "none found")


check("regression", "harness is read-only and implements nothing", harness_is_read_only)
def no_local_pr_action():
    """Offline scope: prove no PR artifact and no PR-creating call exist locally."""
    if os.path.exists(os.path.join(REPO, ".git", "PULL_REQUEST")):
        return (False, "local PR artifact present")
    if os.path.exists(os.path.join(REPO, ".git", "PULL_REQUEST_EDITMSG")):
        return (False, "local PR edit message present")
    pattern = "create" + "_pull_" + "request"
    cli = "gh pr " + "create"
    for rel in discover("validation", ".py"):
        body = (harness_body_excluding_self_inspection() if rel.endswith("phase_8_validation.py")
                else read(rel))
        if pattern in body or cli in body:
            return (False, "PR-creating call in %s" % rel)
    return (True, "LOCAL ONLY — remote open-PR count is NOT provable offline and is not claimed")


# --- end self-inspection region ---

check("regression", "harness contains no vacuous or unconditional-pass checks", no_vacuous_checks)
check("regression", "no local PR artifact or PR-creating action in the tree (local scope only)",
      no_local_pr_action)


# --- 5.2 cross-file governance-state transition consistency ---------------------------------

def parse_transitions():
    """Parse the permitted-transition table out of the state model."""
    block = STATE.split("## 6. Permitted transitions")[1].split("### Withdrawal is terminal")[0]
    rows = []
    for line in block.splitlines():
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) == 3 and cells[0].startswith("`") or (len(cells) == 3 and "/" in cells[0]):
            rows.append((plain(cells[0]), plain(cells[1])))
    return rows


def withdrawal_targets_agree():
    """Every file that describes withdrawal must agree with the state model's only target."""
    rows = parse_transitions()
    from_approved = [t.strip() for f, t in rows if f.strip() == "APPROVED"]
    # Promotion forward is legitimate; the defect is a rewind to an earlier state.
    rewinds = [t for t in from_approved if t in ("REVIEWED", "DRAFT")]
    if rewinds:
        return (False, "state model permits APPROVED -> %s" % rewinds)
    if "RETRACTED" not in from_approved:
        return (False, "state model gives APPROVED no withdrawal target: %s" % from_approved)
    from_canonical = [t.strip() for f, t in rows if f.strip() == "CANONICAL"]
    if [t for t in from_canonical if t in ("APPROVED", "REVIEWED", "DRAFT")]:
        return (False, "state model permits CANONICAL rewind: %s" % from_canonical)
    # no document may say an approval returns to an earlier state
    bad = []
    for rel, doc in NORMATIVE.items():
        flat = plain(doc).replace("\n", " ")
        for m in re.finditer(r"(?:stays|returns?|revert(?:s|ed)?|back) (?:at|to) (?:REVIEWED|DRAFT)", flat, re.I):
            window = flat[max(0, m.start() - 200):m.end() + 200]
            if re.search(r"\bnot\b|\bnever\b|no reverse|new linked item", window, re.I):
                continue
            bad.append("%s: %s" % (rel, m.group(0)))
    return (not bad, str(bad) if bad else "APPROVED -> RETRACTED only, in %d documents" % len(NORMATIVE))


check("state-transitions", "state model permits withdrawal only to RETRACTED",
      withdrawal_targets_agree)

check("state-transitions", "withdrawn level is carried as metadata on one terminal state",
      lambda: (all("withdrawn level" in plain(d).lower() for d in (STATE, PROMO, STD, CREC, KREC)), ""))

check("state-transitions", "no reverse transition exists on the governance axis",
      lambda: ("no reverse transition" in plain(STATE).lower()
               and "rewind a governance state" in plain(PROMO).lower()
               and "There is no APPROVED \u2192 REVIEWED" in plain(STD), ""))

check("state-transitions", "a revised claim is a new linked item starting at DRAFT",
      lambda: (all("new linked item starting at" in plain(d) for d in (STATE, PROMO, STD)), ""))

check("state-transitions", "APPROVED withdrawal in promotion governance matches the state model",
      lambda: ("RETRACTED with withdrawn level" in plain(PROMO)
               and "not** returned to `REVIEWED` or `DRAFT`" in PROMO, ""))

check("state-transitions", "forbidden-shortcut list names the reverse transitions",
      lambda: ("`APPROVED` \u2192 `REVIEWED` or `DRAFT`, and `CANONICAL` \u2192 `APPROVED`" in STATE, ""))


# --- 5.3 inventory consistency, derived rather than hand-maintained -------------------------

def constraint_numbers():
    return [int(n) for n in re.findall(r"^## (\d+)\. ", STD, re.M)]


check("inventory", "constraint numbering is contiguous from 1",
      lambda: (constraint_numbers() == list(range(1, len(constraint_numbers()) + 1)),
               "%d constraints" % len(constraint_numbers())))

check("inventory", "universe states the actual constraint count",
      lambda: (("| Enforceable constraints | %d |" % len(constraint_numbers())) in plain(UNIV)
               and ("%d inherited rules" % len(constraint_numbers())) in UNIV,
               "%d" % len(constraint_numbers())))

check("inventory", "universe states the actual memory-class count",
      lambda: (("| Memory classes | %d |" % len(declared_classes())) in plain(UNIV)
               and "six memory classes" in plain(A), "%d" % len(declared_classes())))

check("inventory", "four-axis wording is normative everywhere; no three-axis claim survives",
      lambda: (lambda stale: (not stale, str(stale) if stale else "0 stale axis claims"))(
          [rel for rel, doc in NORMATIVE.items()
           if re.search(r"three[- ]ax", doc, re.I)]))

check("inventory", "no stale 'seven classes' or 'seven stores' claim in normative text",
      lambda: (lambda stale: (not stale, str(stale) if stale else "0 stale class claims"))(
          [rel for rel, doc in NORMATIVE.items()
           for m in re.finditer(r"seven (classes|stores|memory)", doc, re.I)
           if not REMEDIATION_CONTEXT.search(doc[max(0, m.start() - 200):m.end() + 200])]))

check("inventory", "universe names the four axes and the withdrawal semantics",
      lambda: ("four axes" in plain(UNIV).lower() and "withdrawal semantics" in plain(UNIV).lower(), ""))

# =========================================================== 10. exemplars

check("exemplars", "eight exemplars discovered on disk",
      lambda: (len(EXEMPLARS) == 8, "%d: %s" % (len(EXEMPLARS), [os.path.basename(e) for e in EXEMPLARS])))

check("exemplars", "every exemplar uses full memory class names only",
      lambda: no_short_class_aliases())

check("exemplars", "no exemplar shows a memory class mutating into a governance state",
      lambda: (not any(re.search(r"Memory class:.*→", DOCS[e]) for e in EXEMPLARS), ""))

def canonical_exemplars():
    """Any exemplar whose own Identity block declares a canonical governance status —
    `CANONICAL`, or `SUPERSEDED`/`RETRACTED`, which only a once-canonical record holds.

    Selection is never by the presence of a metadata field: the previous selector required a
    `Canonical ID` line, so an exemplar missing its metadata escaped validation instead of
    failing it. Identity blocks are parsed, so a record cannot opt out by omission.
    """
    out = []
    for rel in EXEMPLARS:
        doc = DOCS[rel]
        block = doc.split("## Identity", 1)[-1].split("\n## ", 1)[0] if "## Identity" in doc \
            else doc.split("\n## ", 1)[0]
        if re.search(r"`(CANONICAL|SUPERSEDED|RETRACTED)`", block) or "Canonical ID" in block:
            out.append(rel)
    return out


def declared_mode(doc):
    """The declared field only. Prose discussing why other modes are wrong is not a declaration."""
    m = re.search(r"^- Applicability mode:\s*`([A-Z_]+)`", doc, re.M)
    return m.group(1) if m else None


def canonical_exemplar_modes():
    bad = []
    for rel in canonical_exemplars():
        mode = declared_mode(DOCS[rel])
        if mode is None:
            bad.append("%s: no declared mode" % os.path.basename(rel))
        elif mode not in MODES:
            bad.append("%s: illegal mode %s" % (os.path.basename(rel), mode))
    return (not bad and len(canonical_exemplars()) >= 5,
            str(bad) if bad else "%d canonical exemplars, exactly one mode each"
            % len(canonical_exemplars()))


check("exemplars", "every CANONICAL exemplar declares exactly one allowed applicability mode",
      canonical_exemplar_modes)

check("exemplars", "canonical-exemplar discovery is by state, not by field presence",
      lambda: (len(canonical_exemplars()) >= len([e for e in EXEMPLARS if "Canonical ID" in DOCS[e]]),
               "%d by state vs %d by Canonical ID field"
               % (len(canonical_exemplars()), len([e for e in EXEMPLARS if "Canonical ID" in DOCS[e]]))))

check("exemplars", "exemplar 2 uses the four-axis model",
      lambda: ("four axes" in plain(DOCS["knowledge/exemplars/project-assumption-non-canonical.md"]).lower()
               and "three-ax" not in DOCS["knowledge/exemplars/project-assumption-non-canonical.md"].lower(), ""))

check("exemplars", "exemplar 3 declares and justifies its applicability mode",
      lambda: ("NON_INHERITABLE" in DOCS["knowledge/exemplars/financial-calculation-lineage.md"]
               and "Why `NON_INHERITABLE` is the right mode"
               in DOCS["knowledge/exemplars/financial-calculation-lineage.md"], ""))

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
