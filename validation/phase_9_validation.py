#!/usr/bin/env python3
"""Phase 9 Model Registry / Router architecture validation.

Architecture-validation tooling. Reads the repository's markdown and asserts properties of
it. Implements no part of AI-OS: no provider SDK, API call, credential, endpoint, scoring
function, storage or runtime.

Usage:
    python3 validation/phase_9_validation.py [--verbose] [--json]

Exit code 0 if every check passes, 1 otherwise.
"""

import json
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The Phase 8 human-approval record. Everything at or before it is upstream and immutable.
PHASE8_BASELINE = "00fb92e1b2dd1209ee2f69550c5962158b881e3e"

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
    diff = subprocess.run(["git", "diff", "--name-only", PHASE8_BASELINE, "HEAD", "--"] + paths,
                          cwd=REPO, capture_output=True, text=True)
    status = subprocess.run(["git", "status", "--porcelain", "--"] + paths,
                            cwd=REPO, capture_output=True, text=True)
    changed = [ln for ln in (diff.stdout + status.stdout).splitlines() if ln.strip()]
    return (not changed), changed


ARCH = "architecture/model-registry-router.md"
MODEL_FILES = discover("models")
EXEMPLARS = [f for f in MODEL_FILES if "/exemplars/" in f]
TEMPLATES = [f for f in MODEL_FILES if "/_templates/" in f]
STANDARD = "models/_standards/common-model-governance-constraints.md"
PHASE9_FILES = [ARCH] + MODEL_FILES + [f for f in discover("reviews") if "phase-9" in f]

DOCS = {rel: read(rel) for rel in PHASE9_FILES}
NORMATIVE = {rel: doc for rel, doc in DOCS.items() if not rel.startswith("reviews/")}
RECORDS = {rel: doc for rel, doc in DOCS.items() if rel.startswith("reviews/")}
REMEDIATION_CONTEXT = re.compile(
    r"remov|was removed|duplicat|deliberately not|Not built|no longer|replaced|refus|"
    r"defect|finding|audit|fixed|correct|no live|nowhere|is absent|absent from|"
    r"prohibit|never|not a|cannot|must not|refuses", re.I)

A = DOCS[ARCH]
CAP = DOCS["models/model-capability-taxonomy.md"]
LIFE = DOCS["models/model-lifecycle-and-versioning.md"]
CONS = DOCS["models/routing-constraint-model.md"]
PREC = DOCS["models/routing-precedence-and-fallback.md"]
DIV = DOCS["models/review-diversity-and-criticality.md"]
EVID = DOCS["models/evaluation-evidence-model.md"]
UNIV = DOCS["models/master-model-routing-universe.md"]
STD = DOCS[STANDARD]
TMPL = {os.path.basename(t): DOCS[t] for t in TEMPLATES}
ALL9 = "\n".join(DOCS.values())

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

SEPARATED = ["ROLE", "SKILL", "WORKFLOW", "HANDOFF", "REVIEW PROFILE", "DECISION RIGHT",
             "KNOWLEDGE", "MODEL PROFILE", "MODEL CAPABILITY", "ROUTING POLICY",
             "ROUTING DECISION", "PROVIDER", "ENDPOINT", "RUNTIME"]

check("identity", "full 14-object separation chain stated",
      lambda: (all(s in A for s in SEPARATED) and "!=" in A, "%d objects" % len(SEPARATED)))

DENIALS = ["MODEL != ROLE", "MODEL != AGENT INSTANCE", "MODEL != AUTHORITY",
           "MODEL != REVIEWER IDENTITY", "MODEL != KNOWLEDGE SOURCE BY DEFAULT",
           "MODEL != CANONICAL KNOWLEDGE", "ROUTER != ORCHESTRATOR",
           "ROUTING DECISION != DECISION RIGHT"]
missing_denials = [d for d in DENIALS if d not in plain(A)]
check("identity", "every required denial stated verbatim (incl. MODEL != PROVIDER != ENDPOINT)",
      lambda: (not missing_denials and "MODEL != PROVIDER != ENDPOINT" in plain(A),
               str(missing_denials) if missing_denials else "%d denials" % (len(DENIALS) + 1)))

check("identity", "MODEL != ROLE: a model is replaceable, a Role is a professional profile",
      lambda: ("replaceable execution capability" in plain(A)
               and "Roles are not staffed by models" in plain(A)
               and "A model is a replaceable execution capability" in plain(STD), ""))

check("identity", "MODEL != AUTHORITY: no model holds a Decision Right",
      lambda: ("A model holds no authority" in plain(STD)
               and "by being the thing that reached the gate" in plain(A), ""))

check("identity", "ROUTER != ORCHESTRATOR: router does not decide what work happens",
      lambda: ("A Router is not an Orchestrator" in plain(STD)
               and "in what order, by which Role" in plain(A), ""))

check("identity", "ROUTING DECISION != DECISION RIGHT: selection approves nothing",
      lambda: ("approves no work, accepts no risk, satisfies no review" in plain(A)
               and "A Routing Decision is not a Decision Record" in plain(STD)
               and "not a Decision Record" in plain(TMPL["routing-decision-template.md"]), ""))

check("identity", "model, provider and deployment are three separate objects",
      lambda: ("Model, provider and deployment are three objects" in plain(STD)
               and "one provider may expose many models" in plain(A), ""))

check("identity", "model output enters Phase 8 as AI_SUGGESTION with AI origin",
      lambda: ("AI_SUGGESTION" in A and "ORIGIN: AI_GENERATED" in A
               and "Model output enters Phase 8 as" in plain(STD), ""))

# =========================================================== capability / evidence

CAP_IDS = re.findall(r"\| `(capability\.[a-z_]+)` \|", CAP)
check("capability", "capability taxonomy defines a named, stable family set",
      lambda: (len(CAP_IDS) >= 20 and len(CAP_IDS) == len(set(CAP_IDS)),
               "%d families, all unique" % len(CAP_IDS)))

CLASSES = ["NOT_CLAIMED", "BASELINE", "STRONG", "SPECIALISED"]
check("capability", "four ordered capability claim classes",
      lambda: (all(re.search(r"\| `%s` \|" % c, CAP) for c in CLASSES), ", ".join(CLASSES)))

check("capability", "NOT_CLAIMED is not NOT_CAPABLE",
      lambda: ("NOT_CLAIMED is not NOT_CAPABLE" in plain(CAP)
               and "NOT_CLAIMED is not NOT_CAPABLE" in plain(STD), ""))

check("capability", "a capability claim is a claim, never a guarantee",
      lambda: ("A capability claim is a claim" in plain(CAP)
               and "never a guarantee of performance" in plain(STD), ""))

check("capability", "limitations narrow a claim; prohibited contexts override it",
      lambda: ("narrows" in CAP and "overrides" in CAP
               and "## Known Limitations" in TMPL["model-profile-template.md"]
               and "## Prohibited Contexts" in TMPL["model-profile-template.md"], ""))

EVCLASSES = ["PROVIDER_DECLARED", "EXTERNAL_BENCHMARK", "INTERNAL_EVALUATION",
             "HUMAN_EXPERT_ASSESSMENT", "OBSERVED_PRODUCTION", "KNOWN_LIMITATION_OR_INCIDENT"]
check("capability", "six distinct evidence classes, each with its weakness stated",
      lambda: (all(re.search(r"\| `%s` \|" % e, EVID) for e in EVCLASSES), "%d" % len(EVCLASSES)))

check("capability", "provider declaration is evidence, not proof",
      lambda: ("admissible and is not proof" in plain(EVID)
               and "Provider assertion is evidence of a provider assertion" in plain(STD), ""))

check("capability", "no benchmark score is authority",
      lambda: ("A benchmark score is not authority" in plain(EVID)
               and "No benchmark score is authority" in plain(STD), ""))

check("capability", "evidence classes never merge",
      lambda: ("Classes never merge" in plain(EVID)
               and "no quantity of weak evidence becomes strong evidence" in plain(EVID), ""))

check("capability", "no composite score exists and none may become routing authority",
      lambda: ("No composite score exists in this architecture" in plain(EVID)
               and "No composite score exists" in plain(STD)
               and "no ranking of models is expressible" in plain(STD), ""))

check("capability", "confidence never creates eligibility",
      lambda: ("Confidence never creates eligibility" in plain(EVID)
               and "Confidence does not create eligibility" in plain(STD), ""))

check("capability", "capability evidence is about a tool, never about the world",
      lambda: ("never knowledge about the world" in plain(EVID)
               and "never knowledge about the world" in plain(STD), ""))

check("capability", "freshness reuses Phase 8 rather than inventing states",
      lambda: ("PAST_REFRESH_INTERVAL" in EVID
               and all(v in EVID for v in ["CURRENT_FOR_USE", "STALE_BUT_USABLE",
                                           "STALE_AND_BLOCKING", "EXPIRED_FOR_USE"])
               and "No verdict is written back" in plain(EVID).replace("no verdict", "No verdict"), ""))

check("capability", "evaluation dimensions are separate, review-detection among them",
      lambda: ("review-detection quality" in EVID
               and "is not the ability to produce it" in plain(EVID), ""))

# =========================================================== constraints / precedence

ELIGIBILITY = ["REQUIRED_CAPABILITY", "REQUIRED_MODALITY", "REQUIRED_CONTEXT_CLASS",
               "REQUIRED_TOOL_USE", "REQUIRED_STRUCTURED_OUTPUT", "REQUIRED_DEPLOYMENT_CLASS",
               "REQUIRED_JURISDICTION", "SUPPORTED_SENSITIVITY_CLASSES",
               "REQUIRED_HANDLING_CONTROLS", "PROHIBITED_SENSITIVITY_CLASSES",
               "REQUIRED_DATA_HANDLING_POSTURE", "PROVIDER_ALLOWED", "PROVIDER_PROHIBITED",
               "MODEL_ALLOWED", "MODEL_PROHIBITED", "MODEL_FAMILY_ALLOWED",
               "MODEL_FAMILY_PROHIBITED", "MINIMUM_REASONING_CLASS",
               "MINIMUM_RELIABILITY_CLASS", "MINIMUM_CONTEXT_CAPACITY_CLASS",
               "MODEL_DIVERSITY_REQUIRED", "PROVIDER_DIVERSITY_REQUIRED",
               "NO_EXTERNAL_PROVIDER", "MAX_COST_CLASS", "MAX_LATENCY_CLASS",
               "LIFECYCLE_ROUTABLE", "AVAILABILITY_ELIGIBLE"]
ACT_REQUIREMENTS = ["HUMAN_SELECTION_REQUIRED", "HUMAN_ACKNOWLEDGEMENT_REQUIRED",
                    "GOVERNANCE_REVIEW_REQUIRED"]
EXCEPTIONABILITY = ["ABSOLUTELY_NON_WAIVABLE", "GOVERNED_EXCEPTION_POSSIBLE",
                    "OPERATOR_CONFIGURABLE_WITHIN_POLICY"]
missing_hard = [h for h in ELIGIBILITY if h not in CONS]
check("constraints", "every eligibility constraint type defined",
      lambda: (not missing_hard, str(missing_hard) if missing_hard
               else "%d types" % len(ELIGIBILITY)))


def eligibility_table_rows():
    """Parse the eligibility-constraint table, not the whole file."""
    block = CONS.split("## 2. Eligibility constraints")[1].split("### Three that are commonly misread")[0]
    rows = []
    for line in block.splitlines():
        if not line.startswith("|") or line.startswith("|---") or "Constraint |" in line:
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) == 3 and re.search(r"`[A-Z_]+`", cells[0]):
            rows.append((", ".join(re.findall(r"`([A-Z_]+)`", cells[0])), cells[1], "", cells[2]))
    return rows


# --- 14.15 act requirements are NOT in the eligibility-filter set
def act_requirements_not_filters():
    rows = [r[0] for r in eligibility_table_rows()]
    leaked = [a for a in ACT_REQUIREMENTS if a in rows]
    return (not leaked and all(a in CONS.split("## 7. Act requirements")[1]
                               for a in ACT_REQUIREMENTS),
            str(leaked) if leaked else "3 act requirements, none in the eligibility table")


check("constraints", "act requirements are a third kind, not eligibility filters",
      act_requirements_not_filters)

check("constraints", "act requirements change eligibility in neither direction",
      lambda: ("change eligibility in neither direction" in plain(STD)
               and "Three kinds of requirement, never confused" in plain(STD)
               and "never changes eligibility in either direction" in plain(CONS)
               and "None of these filters a candidate, and none changes eligibility" in plain(CONS)
               and "conditions on **finalisation**" in CONS
               and "None of these filters a candidate or changes eligibility in either direction"
               in plain(TMPL["routing-policy-template.md"]), ""))

# --- 14.11 every eligibility constraint carries an exceptionability class or derivation
def every_constraint_has_exceptionability():
    rows = eligibility_table_rows()
    if len(rows) < 20:
        return (False, "only %d rows parsed from the eligibility table" % len(rows))
    bad = [r[0] for r in rows
           if not (any(e in r[3] for e in EXCEPTIONABILITY) or "Derived from source" in r[3])]
    return (not bad, str(bad) if bad else "%d rows, all classified or derived" % len(rows))


check("exceptionability", "every eligibility constraint has an exceptionability class or derivation",
      every_constraint_has_exceptionability)

check("exceptionability", "three exceptionability classes defined",
      lambda: (all(re.search(r"\| \*\*`%s`\*\* \|" % e, CONS) for e in EXCEPTIONABILITY),
               ", ".join(EXCEPTIONABILITY)))

check("exceptionability", "class is derived from the source of the requirement",
      lambda: ("Deriving the class from the source" in CONS
               and "Exceptionability is a property of the source" in plain(STD), ""))

check("exceptionability", "legal, contractual, privileged and third-party sources are non-waivable",
      lambda: (lambda block: (all(("**`ABSOLUTELY_NON_WAIVABLE`**" in ln)
                                  for ln in block.splitlines()
                                  if re.search(r"Statute|contractual prohibition|PRIVILEGED. or .THIRD_PARTY", ln)),
                              "legal/contract/privilege rows non-waivable"))(
          CONS.split("### 5.2")[1].split("### 5.3")[0]))

check("exceptionability", "a Phase 7 Right cannot create legal authority",
      lambda: ("cannot create legal authority" in plain(CONS)
               and "cannot create legal authority" in plain(STD), ""))

check("exceptionability", "unknown exceptionability defaults to non-waivable",
      lambda: ("defaults to `ABSOLUTELY_NON_WAIVABLE`" in CONS
               and "unclassified constraint is non-waivable" in plain(STD), ""))

check("exceptionability", "human acknowledgement never changes eligibility",
      lambda: ("Human acknowledgement never changes eligibility" in plain(CONS)
               and "adjusts no requirement" in plain(CONS), ""))

check("exceptionability", "a named Right must cover the specific constraint class",
      lambda: ('"A Decision Right exists" is not a basis' in plain(CONS).replace("\u201c", '"').replace("\u201d", '"')
               or "a Decision Right exists\" is not a basis" in plain(CONS), ""))

check("constraints", "three kinds: eligibility filters, preferences rank, acts withhold",
      lambda: (all(k in CONS for k in ("ELIGIBILITY_CONSTRAINT", "PREFERENCE",
                                       "ROUTING_ACT_REQUIREMENT"))
               and "Filters" in CONS and "Ranks" in CONS and "No selection is final" in CONS, ""))

check("constraints", "a preference never overrides an eligibility constraint",
      lambda: ("preference may never override an eligibility constraint" in plain(CONS)
               and "Three kinds of requirement, never confused" in plain(STD)
               and "no accumulation of preferences" in plain(CONS).lower(), ""))

check("constraints", "ranking happens only inside the eligible set",
      lambda: ("Ranking happens only inside the eligible set" in plain(CONS), ""))

check("constraints", "no partial eligibility and no closest fit",
      lambda: ("There is no partial eligibility" in plain(CONS)
               and "There is no partial eligibility" in plain(STD)
               and "closest fit" in plain(CONS).lower(), ""))

check("constraints", "an unrecognised constraint blocks rather than being ignored",
      lambda: ("An unrecognised constraint blocks routing" in plain(STD)
               and "blocks routing" in plain(CONS), ""))

check("constraints", "sensitivity eligibility is a deployment property",
      lambda: ("property of the deployment, not of the model" in plain(CONS), ""))

check("constraints", "data-handling posture: unstated is not satisfied",
      lambda: ("unstated is not satisfied" in plain(CONS).lower()
               and "unstated is not satisfied" in plain(TMPL["deployment-profile-template.md"]).lower(), ""))

check("constraints", "an unrecognised requirement blocks routing",
      lambda: ("an unrecognised requirement blocks routing" in plain(CONS).lower()
               and "An unrecognised constraint blocks routing" in plain(STD), ""))

check("constraints", "conflicting eligibility constraints yield NO_ELIGIBLE_MODEL, not a compromise",
      lambda: ("NO_ELIGIBLE_MODEL" in CONS
               and "violates the fewest" in plain(CONS)
               and "There is no partial eligibility" in plain(CONS), ""))

STAGES = ["Legality and governance", "Sensitivity, handling and residency",
          "Required capability", "Independence and diversity", "Lifecycle and availability",
          "Preferences, in the policy's declared order", "Deterministic tie-break",
          "Act requirements"]
check("precedence", "nine precedence stages including universe binding at stage 0",
      lambda: (all(s in plain(PREC) for s in STAGES)
               and "Candidate universe binding" in plain(PREC), "%d stages" % (len(STAGES) + 1)))

check("precedence", "hard stages 1-5 globally fixed; stage 6 owned by the versioned policy",
      lambda: ("Stages 1-5 are globally fixed and cannot be reordered by any policy"
               in plain(PREC).replace("\u2013", "-")
               and "Stage 6 is owned by the versioned Routing Policy" in plain(PREC)
               and "This policy owns the order" in plain(TMPL["routing-policy-template.md"]), ""))

check("precedence", "no global hard-coded reliability-before-cost ordering survives",
      lambda: (lambda stale: (not stale, str(stale) if stale else "no fixed soft ordering"))(
          [rel for rel, doc in NORMATIVE.items()
           if re.search(r"reliability outranks (cheapness|cost)", doc, re.I)
           or "stage 7 sits **after** stage 6" in doc]))

check("precedence", "risk-required reliability is expressed as an eligibility constraint",
      lambda: ("MINIMUM_RELIABILITY_CLASS" in PREC
               and "a preference is always negotiable by definition" in plain(PREC), ""))

check("precedence", "each stage filters what the next sees; no ordering restores a candidate",
      lambda: ("Each stage filters the set the next stage sees" in plain(PREC)
               and "No preference ordering can restore an ineligible candidate" in plain(PREC), ""))

check("precedence", "cost and latency can never override governance requirements",
      lambda: ("never displaces a governance" in plain(CONS)
               and "Cost and latency never override governance" in plain(STD), ""))

check("precedence", "preferences are lexicographic, not weighted",
      lambda: ("lexicographic" in plain(PREC) and "not weighted" in plain(PREC)
               and "declared order, not weighted" in plain(CONS)
               and "none to tune" in plain(TMPL["routing-policy-template.md"]).lower(), ""))

check("precedence", "tie-break is deterministic and recorded, never random",
      lambda: ("deterministic and recorded" in plain(PREC) and "never random" in plain(PREC)
               and "select the same candidate" in plain(PREC), ""))

check("precedence", "cost may be an eligibility constraint only by declared task policy",
      lambda: ("preferences by default" in plain(CONS)
               and "the work costs more than the budget" in plain(CONS), ""))

# =========================================================== candidate universe

UNIVERSE_ELEMENTS = ["Registry state reference", "Universe definition version", "Inclusion rule",
                     "Routing scope", "Pre-filter exclusions", "Enumerated candidate set",
                     "Omission reasons", "Completeness result"]
check("candidate-universe", "Candidate Universe Definition names all required elements",
      lambda: (all(e in PREC for e in UNIVERSE_ELEMENTS), "%d elements" % len(UNIVERSE_ELEMENTS)))

check("candidate-universe", "universe is bound before any filtering",
      lambda: ("binds to a Candidate Universe Definition before any filtering or ranking occurs"
               in plain(PREC)
               and PREC.index("## 1. The candidate universe comes first")
               < PREC.index("## 2. Precedence"), "universe section precedes precedence section"))

def where_practical_removed():
    """The phrase survives only where it is quoted as the standard being rejected."""
    stale = []
    for rel, doc in NORMATIVE.items():
        for m in re.finditer(r"where practical", doc):
            window = doc[max(0, m.start() - 250):m.end() + 250]
            if re.search(r"is not a standard|does not meet it|replaced|first draft|audit", window, re.I):
                continue
            stale.append(rel)
    return (not stale, str(sorted(set(stale))) if stale else "only as the rejected standard")


check("candidate-universe", "'where practical' replaced by normative semantics",
      where_practical_removed)

check("candidate-universe", "registry state reference is deterministic, not a timestamp alone",
      lambda: ("Not a timestamp alone" in plain(PREC)
               and "does not reconstruct anything" in plain(PREC)
               and "reconstructs nothing" in plain(TMPL["routing-decision-template.md"]), ""))

check("candidate-universe", "pre-filter exclusion is distinguished from constraint exclusion",
      lambda: ("Outside the universe versus ineligible inside it" in plain(PREC)
               and "appears in neither list is the defect" in plain(PREC), ""))

check("candidate-universe", "availability does not remove a candidate from the universe",
      lambda: ("Availability does not remove a candidate from the universe" in plain(PREC)
               and "never made to disappear" in plain(TMPL["routing-decision-template.md"]), ""))

check("candidate-universe", "a load failure yields CANDIDATE_UNIVERSE_INCOMPLETE, never silent shrink",
      lambda: ("CANDIDATE_UNIVERSE_INCOMPLETE" in PREC
               and "must never silently shrink the universe" in plain(PREC)
               and "never silently shrinks the universe" in plain(STD), ""))

check("candidate-universe", "incomplete universe blocks or escalates per policy",
      lambda: ("**block**, or **escalate**" in PREC and "It never proceeds" in plain(PREC)
               and "`BLOCK` or `ESCALATE`" in TMPL["routing-policy-template.md"], ""))

check("candidate-universe", "routing decision template requires the universe elements",
      lambda: (all(x in TMPL["routing-decision-template.md"]
                   for x in ["Registry state reference", "Candidate Universe Definition version",
                             "Omission reasons", "Completeness result",
                             "CANDIDATE_UNIVERSE_COMPLETE"]), ""))

check("candidate-universe", "policy template declares the universe definition and its failure mode",
      lambda: ("## Candidate Universe Definition" in TMPL["routing-policy-template.md"]
               and "Availability pre-enumeration" in TMPL["routing-policy-template.md"], ""))

# =========================================================== sensitivity multi-label

def no_ordinal_sensitivity():
    """No scalar ceiling or ordinal comparison over Phase 8 sensitivity classes."""
    patterns = [r"MAX_DATA_SENSITIVITY_ALLOWED", r"maximum (approved )?(data )?sensitivity",
                r"sensitivity[^.]{0,40}at or above", r"at or above[^.]{0,40}sensitivity",
                r"highest[^.]{0,30}sensitivity class"]
    hits = []
    for rel, doc in NORMATIVE.items():
        for pat in patterns:
            for m in re.finditer(pat, doc, re.I):
                window = doc[max(0, m.start() - 250):m.end() + 250]
                if (REMEDIATION_CONTEXT.search(window) or "no total order" in window
                        or re.search(r"would have|ceiling test|first draft|rejected", window, re.I)):
                    continue
                hits.append("%s: %s" % (rel, m.group(0)[:40]))
    return (not hits, str(hits) if hits else "0 ordinal sensitivity constructs")


check("sensitivity", "no scalar maximum-sensitivity or ordinal comparison survives",
      no_ordinal_sensitivity)

check("sensitivity", "Phase 8's lack of a total order is stated and honoured",
      lambda: ("no total order" in plain(CONS) and "no total order" in plain(A)
               and "Sensitivity is a multi-label set test" in plain(STD), ""))

check("sensitivity", "eligibility is a subset test with obligations",
      lambda: ("subset test with obligations" in plain(CONS)
               and "every applicable sensitivity label is explicitly supported" in plain(CONS), ""))

check("sensitivity", "compound labels require every regime simultaneously",
      lambda: ("requires **both** regimes simultaneously" in CONS
               and "implies support for no other" in plain(CONS), ""))

check("sensitivity", "unknown support is not support",
      lambda: ("Unknown support is not support" in plain(CONS)
               and "unknown support is not support" in plain(STD).lower()
               and "Unknown support is not support" in plain(TMPL["deployment-profile-template.md"]), ""))

check("sensitivity", "prohibition wins over support",
      lambda: ("A prohibition wins over any support" in plain(CONS)
               and "Prohibition wins over support" in plain(TMPL["deployment-profile-template.md"]), ""))

check("sensitivity", "Phase 8's most-restrictive and non-relaxable rules are carried through",
      lambda: ("most restrictive handling applies" in plain(CONS)
               and "cannot be relaxed by an internal decision" in plain(CONS), ""))

check("sensitivity", "deployment template declares supported/prohibited sets and controls",
      lambda: (all(x in TMPL["deployment-profile-template.md"]
                   for x in ["SUPPORTED_SENSITIVITY_CLASSES", "PROHIBITED_SENSITIVITY_CLASSES",
                             "Handling controls per supported label", "Unassessed labels"]), ""))

# =========================================================== residency

RESIDENCY_FIELDS = ["Exact jurisdiction", "Region / residency class", "Allowed jurisdiction set",
                    "Prohibited jurisdiction set", "Cross-border processing", "UNKNOWN_RESIDENCY"]
check("residency", "residency semantics complete in the constraint model",
      lambda: (all(f in CONS for f in RESIDENCY_FIELDS), "%d fields" % len(RESIDENCY_FIELDS)))

check("residency", "deployment template carries the residency fields and evidence",
      lambda: (all(f in TMPL["deployment-profile-template.md"]
                   for f in ["Exact jurisdiction", "Region / residency class",
                             "Cross-border processing", "UNKNOWN_RESIDENCY",
                             "Evidence and review-by"]), ""))

check("residency", "UNKNOWN_RESIDENCY never satisfies a residency requirement",
      lambda: ("never satisfies a residency requirement" in plain(CONS)
               and "Never satisfies a residency requirement" in plain(TMPL["deployment-profile-template.md"])
               and "never satisfied" in plain(STD).lower(), ""))

check("residency", "prohibited outranks allowed",
      lambda: ("Prohibited outranks allowed" in plain(CONS)
               and "prohibited outranks allowed" in plain(STD).lower(), ""))

check("residency", "region class and exact jurisdiction need an explicit mapping",
      lambda: ("not interchangeable" in plain(CONS)
               and "explicit declared mapping" in plain(CONS), ""))

check("residency", "provider claims constrain but do not substitute for deployment evidence",
      lambda: ("do not substitute" in plain(CONS)
               and "never substitute for deployment-specific evidence"
               in plain(TMPL["deployment-profile-template.md"]), ""))

check("residency", "residency belongs to the deployment, not the model",
      lambda: ("belongs **primarily to the Deployment Profile**" in CONS
               and "Residency belongs to the deployment" in plain(STD), ""))

# =========================================================== data-handling ownership

check("posture", "data-handling posture has one authoritative reading",
      lambda: ("Effective deployment posture" in CONS
               and "Data-handling posture has one authoritative reading" in plain(STD)
               and "There is no second source of truth" in plain(CONS), ""))

check("posture", "Model Profile carries no data-handling posture",
      lambda: ("Data Handling — not recorded here" in TMPL["model-profile-template.md"]
               and "is a **defect**" in TMPL["model-profile-template.md"]
               and "**Nothing.**" in CONS.split("| **Model Profile** |")[1][:60], ""))

check("posture", "provider carries the default; deployment carries the effective posture",
      lambda: ("provider-level default and constraint" in plain(TMPL["provider-profile-template.md"])
               and "Effective Data-Handling Posture" in TMPL["deployment-profile-template.md"], ""))

check("posture", "a deployment may be more restrictive freely, less only if evidenced",
      lambda: ("more** restrictive" in CONS and "explicitly evidenced and permitted" in plain(CONS)
               and "provider-level constraint governs" in plain(TMPL["deployment-profile-template.md"]), ""))

# =========================================================== lifecycle

IDENTITY_LAYERS = ["Model Family", "Underlying Model Release", "Model Profile",
                   "Registry Profile Version", "Provider Offering Mapping", "Deployment Profile"]
check("identity-stack", "six identity-stack layers defined with no overlap",
      lambda: (all(l in LIFE for l in IDENTITY_LAYERS)
               and "The identity stack" in LIFE, "%d layers" % len(IDENTITY_LAYERS)))

check("identity-stack", "registry profile version is not the underlying model version",
      lambda: ("Registry profile version is not the underlying model version" in plain(LIFE)
               and "not the underlying model version" in plain(TMPL["model-profile-template.md"])
               and "Registry profile version is not the underlying model version" in plain(STD), ""))

check("identity-stack", "model profile template carries all four of its layers",
      lambda: (all(x in TMPL["model-profile-template.md"]
                   for x in ["Model Family:", "Underlying Model Release:", "Model Profile ID:",
                             "Registry Profile Version:"]), ""))

check("identity-stack", "provider offering mapping is a bounded mapping, not a registry object",
      lambda: ("Provider Offering Mappings" in TMPL["provider-profile-template.md"]
               and "not a registry object" in plain(TMPL["provider-profile-template.md"])
               and "Why Provider Offering is a mapping, not a seventh object" in LIFE, ""))

check("identity-stack", "materially different provider behaviour becomes a distinct Model Profile",
      lambda: ("distinct Model Profile" in LIFE
               and "belongs to a distinct Model Profile, not to this list"
               in plain(TMPL["model-profile-template.md"])
               and "never an ambiguous mapping" in plain(STD), ""))

check("identity-stack", "a marketing alias never defines identity",
      lambda: ("never defines Model Profile identity" in plain(LIFE)
               and "an alias never defines identity" in plain(TMPL["model-profile-template.md"]), ""))

check("identity-stack", "one profile may map to several provider/deployment combinations",
      lambda: ("may map to several provider/deployment combinations" in plain(LIFE)
               and "the same underlying release" in plain(LIFE), ""))

SIX_PART = ["Model Profile stable ID", "Registry Profile Version",
            "Underlying Model Release identity", "Provider Offering Mapping",
            "Provider Profile version", "Deployment Profile version"]
check("identity-stack", "routing decision preserves the full six-part reproducibility set",
      lambda: (lambda missing: (not missing, str(missing) if missing else "6 elements"))(
          [e for e in SIX_PART if e not in TMPL["routing-decision-template.md"]]))

check("identity-stack", "a silent provider backend change triggers review",
      lambda: ("silent provider backend change" in plain(LIFE).lower()
               and "silent backend change" in plain(TMPL["provider-profile-template.md"]).lower(), ""))

LIFECYCLE = ["CANDIDATE", "EVALUATING", "ELIGIBLE", "DEPRECATED", "SUSPENDED", "RETIRED"]


def declared_lifecycle_states():
    # Only the first table after the heading declares the states; the table after it
    # explains what was removed and must not be read as a declaration.
    block = LIFE.split("## 1. Lifecycle states")[1]
    first_table = re.search(r"\| State \|.*?\n\n", block, re.S)
    return sorted(set(re.findall(r"^\| `([A-Z_]+)` \|", first_table.group(0), re.M)))


check("lifecycle", "exactly six mutually exclusive primary lifecycle states",
      lambda: (declared_lifecycle_states() == sorted(LIFECYCLE),
               ", ".join(declared_lifecycle_states())))

check("lifecycle", "lifecycle exclusivity is explicit",
      lambda: ("Exactly one primary lifecycle state at a time" in plain(LIFE)
               and "two never coexist" in plain(LIFE)
               and "Exactly one primary lifecycle state at a time" in plain(STD), ""))

check("lifecycle", "PREFERRED and RESTRICTED are annotations, not states",
      lambda: ("PREFERRED" not in declared_lifecycle_states()
               and "RESTRICTED" not in declared_lifecycle_states()
               and "routing preference designation" in plain(LIFE)
               and "restriction annotation" in plain(LIFE)
               and "were removed" in LIFE.split("## 1. Lifecycle states")[1]
               and "Exactly one primary lifecycle state" in plain(LIFE), ""))

check("lifecycle", "annotations are orthogonal to the state and to each other",
      lambda: ("orthogonal to the state and to each other" in plain(LIFE)
               and "neither is a state" in plain(STD), ""))

check("lifecycle", "transition rules defined and RETIRED is terminal",
      lambda: ("### Transitions" in LIFE and "RETIRED` is terminal" in LIFE
               and "a new profile" in plain(LIFE), ""))

check("lifecycle", "no transition touches history",
      lambda: ("No transition touches history" in plain(LIFE), ""))

check("lifecycle", "lifecycle status is not task eligibility",
      lambda: ("Registry status is a gate, not a grant" in plain(LIFE)
               and "Lifecycle status is not task eligibility" in plain(STD), ""))

check("lifecycle", "a globally ELIGIBLE model can be prohibited for a specific task",
      lambda: ("can be prohibited for a particular task" in plain(LIFE), ""))

check("lifecycle", "deprecation excludes new routing and removes nothing",
      lambda: ("excludes a profile from new routing. It removes nothing" in plain(LIFE)
               and "Routing history is preserved through everything" in plain(STD), ""))

check("lifecycle", "historical decisions preserved through deprecation and incident",
      lambda: ("Preserved intact" in plain(LIFE)
               and "Historical Routing Decisions are preserved through every one of these" in plain(LIFE), ""))

check("lifecycle", "three versioned objects, all named by a Routing Decision",
      lambda: ("Model Profile version" in LIFE and "Routing Policy version" in LIFE
               and "A Routing Decision names all three, by version" in plain(LIFE), ""))

# =========================================================== fallback / exception

check("exception", "three distinct cases A/B/C defined",
      lambda: ("Ordinary eligible fallback" in PREC and "Exception-adjusted re-evaluation" in PREC
               and "Non-waivable constraint failure" in PREC, "A, B, C"))

check("exception", "a candidate is never eligible before the governing act",
      lambda: ("never called eligible before the governing act changes the applicable requirement set"
               in plain(PREC)
               and "never recorded as eligible" in plain(STD), ""))

check("exception", "case B records the original ineligibility and never rewrites it",
      lambda: ("the original ineligibility result" in plain(PREC)
               and "No part of the original routing history is rewritten" in plain(PREC)
               and "The original result is never overwritten" in plain(STD), ""))

check("exception", "case B requires the act before re-evaluation, in order",
      lambda: (plain(PREC).index("The candidate is ineligible")
               < plain(PREC).index("Eligibility is re-evaluated against the adjusted set"),
               "ineligibility recorded before re-evaluation"))

check("exception", "exception effect is bounded and expiring",
      lambda: ("bounded, expiring effect" in plain(PREC)
               and "bounded, expiring adjusted context" in plain(STD), ""))

check("exception", "ordinary degraded fallback is weaker only on a preference or permitted band",
      lambda: ("preference** or an **explicitly declared permitted degradation band**" in PREC
               and "never weaker on an eligibility constraint" in plain(PREC), ""))

check("exception", "acknowledgement is not the mechanism for a failed eligibility constraint",
      lambda: ("this is not a degraded fallback at all" in plain(PREC).lower()
               and "Operator acknowledgement is not sufficient and is not the mechanism" in plain(PREC), ""))

check("exception", "case C blocks with no acknowledgement, seniority or urgency changing it",
      lambda: ("no acknowledgement, seniority or urgency changes it" in plain(PREC), ""))

check("exception", "routing decision template records the full case-B chain",
      lambda: (all(x in plain(TMPL["routing-decision-template.md"])
                   for x in ["the original ineligibility result", "exceptionability class",
                             "adjusted constraint", "expiry", "re-evaluated"]), ""))

check("exception", "routing decision template names the anti-retrospective-justification rule",
      lambda: ("never recorded as eligible under the original policy"
               in plain(TMPL["routing-decision-template.md"])
               and "justification written afterwards" in plain(TMPL["routing-decision-template.md"]), ""))

# =========================================================== anti-lock-in

ID_FORMS = ["model.<stable_snake_case_name>", "provider.<stable_snake_case_name>",
            "deployment.<stable_snake_case_name>", "routing_policy.<stable_snake_case_name>"]
check("anti-lock-in", "stable internal identifier forms defined",
      lambda: (all(i in LIFE for i in ID_FORMS), "%d forms" % len(ID_FORMS)))

check("anti-lock-in", "IDs exclude marketing names, versions, prices, dates, regions",
      lambda: ("must not contain a marketing name, a version number, a price, a date, a region "
               "code" in plain(LIFE), ""))

check("anti-lock-in", "a rename is an alias addition, never an identity change",
      lambda: ("A rename is an alias addition, never an identity change" in plain(LIFE)
               and "A rename is an alias, never an identity change" in plain(STD), ""))

check("anti-lock-in", "no routing constraint is expressed against an alias",
      lambda: ("no routing constraint is ever expressed against an alias" in plain(LIFE)
               and "no constraint is ever expressed against an alias"
               in plain(TMPL["model-profile-template.md"]), ""))

check("anti-lock-in", "upper architecture may not name a model or provider",
      lambda: ("Upper architecture names no vendor" in plain(STD)
               and "No Role says" in plain(LIFE), ""))

check("anti-lock-in", "model pinning is exceptional, owned and expiring",
      lambda: ("Model pinning is exceptional and governed" in plain(STD)
               and "An unexpiring pin is lock-in acquired one task at a time" in plain(LIFE)
               and "An unexpiring pin is defective"
               in plain(TMPL["routing-policy-template.md"]), ""))


def no_vendor_names():
    """No real provider or product name anywhere in Phase 9 normative text or exemplars."""
    vendors = [r"\bOpenAI\b", r"\bGPT-?\d", r"\bAnthropic\b", r"\bClaude\b", r"\bGemini\b",
               r"\bLlama\b", r"\bMistral\b", r"\bCohere\b", r"\bBedrock\b", r"\bAzure\b",
               r"\bVertex\b", r"\bOllama\b", r"\bDeepSeek\b", r"\bQwen\b", r"\bGrok\b"]
    hits = []
    for rel, doc in DOCS.items():
        for pat in vendors:
            if re.search(pat, doc):
                hits.append("%s: %s" % (rel, pat))
    return (not hits, str(hits) if hits else "0 vendor names across %d files" % len(DOCS))


check("anti-lock-in", "no real vendor or product name appears anywhere in Phase 9", no_vendor_names)

check("anti-lock-in", "exemplars declare themselves synthetic and claim nothing about real models",
      lambda: (all("No claim is made about any real model or provider" in plain(DOCS[e])
                   for e in EXEMPLARS), "%d exemplars" % len(EXEMPLARS)))

# =========================================================== diversity / criticality

DIVVALS = ["SAME_MODEL_ALLOWED", "DIFFERENT_MODEL_VERSION_REQUIRED",
           "DIFFERENT_MODEL_FAMILY_REQUIRED", "DIFFERENT_PROVIDER_REQUIRED",
           "HUMAN_ONLY_REVIEW_REQUIRED", "MODEL_DIVERSITY_NOT_APPLICABLE"]
check("diversity", "six model diversity policy values defined",
      lambda: (all(re.search(r"\| `%s` \|" % d, DIV) for d in DIVVALS), "%d" % len(DIVVALS)))

check("diversity", "reviewer independence is not model diversity",
      lambda: ("REVIEWER / REVIEW PROFILE INDEPENDENCE != MODEL DIVERSITY" in plain(DIV)
               and "Reviewer independence is not model diversity" in plain(STD), ""))

check("diversity", "all four independence/diversity combinations shown as possible",
      lambda: ("Model-homogeneous" in DIV and "Model-diverse" in DIV
               and "model-diverse and not independent at all" in plain(DIV), ""))

check("diversity", "Phase 9 adds no Phase 6 independence class and changes no review status",
      lambda: ("adds no independence class" in plain(DIV)
               and "adds no independence class and changes no review status" in plain(STD)
               and "Phase 9 changes nothing in Phase 6" in plain(DIV), ""))

check("diversity", "different-provider review is never a default",
      lambda: ("is never a default" in plain(DIV)
               and "Different-provider review is never a default" in plain(STD), ""))

check("diversity", "diversity is evaluated against a named prior selection, else blocks",
      lambda: ("named prior Routing Decision" in plain(DIV)
               and "unsatisfiable, and routing blocks" in plain(DIV)
               and "evaluated against a named prior selection" in plain(STD), ""))

check("diversity", "criticality reuses Phase 3 bands without redefining them",
      lambda: ("architecture/project-criticality-policy.md" in DIV
               and "used, not redefined" in plain(DIV), ""))

check("diversity", "criticality grants no authority and makes no output true",
      lambda: ("It does not grant a model authority" in plain(DIV)
               and "It does not make output true" in plain(DIV)
               and "Criticality raises rigour, not authority or truth" in plain(STD), ""))

check("diversity", "largest model is not equated with best model",
      lambda: ('does not mean "the largest model"' in plain(DIV).replace("“", '"').replace("”", '"')
               and "no model is globally strongest" in plain(DIV), ""))

check("diversity", "family diversity at Decision-Grade is expected, not a blanket rule",
      lambda: ('"Expected value", not blanket rule' in plain(DIV).replace("“", '"').replace("”", '"'), ""))

# =========================================================== fallback / availability

AVAIL = ["AVAILABLE", "DEGRADED", "UNAVAILABLE", "UNKNOWN_AVAILABILITY"]
check("fallback", "four availability classes defined",
      lambda: (all(re.search(r"\| `%s` \|" % a, PREC) for a in AVAIL), "%d" % len(AVAIL)))

check("fallback", "availability is not capability",
      lambda: ("Availability is not capability" in plain(PREC)
               and "Availability is not capability" in plain(STD), ""))

check("fallback", "UNKNOWN_AVAILABILITY is never silently treated as AVAILABLE at high criticality",
      lambda: ("never silently treated as" in plain(PREC)
               and "not eligible" in plain(PREC)
               and "never silently treated as" in plain(STD), ""))

FBKINDS = ["EQUIVALENT_FALLBACK", "DEGRADED_FALLBACK", "PROHIBITED_FALLBACK",
           "HUMAN_SELECTION_FALLBACK", "BLOCK"]
check("fallback", "five fallback outcomes defined",
      lambda: (all(re.search(r"\| `%s` \|" % f, PREC) for f in FBKINDS), "%d" % len(FBKINDS)))

check("fallback", "a fallback satisfies every eligibility constraint or is not a fallback",
      lambda: ("satisfies every eligibility constraint or it is not a fallback" in plain(PREC)
               and "is never called eligible" in plain(PREC), ""))

check("fallback", "no silent degradation; degraded fallback names the weaker dimension",
      lambda: ("No silent degradation" in plain(PREC) and "No silent degradation" in plain(STD)
               and "names the dimension on which it is weaker" in plain(PREC), ""))

check("fallback", "degradation does not compound: each fallback assessed against the original",
      lambda: ("never against the previous fallback" in plain(PREC)
               and "never against the previous fallback" in plain(STD), ""))

check("fallback", "outage is never a reason to relax a constraint",
      lambda: ("never a reason to relax a constraint" in plain(PREC)
               and "an outage is never a reason to relax a constraint" in plain(STD), ""))

check("fallback", "no eligible candidate yields NO_ELIGIBLE_MODEL / BLOCKED_FOR_ROUTING",
      lambda: ("NO_ELIGIBLE_MODEL" in PREC and "BLOCKED_FOR_ROUTING" in PREC
               and 'There is no "best available"' in plain(PREC).replace("“", '"').replace("”", '"')
               and "Where nothing is eligible, routing blocks" in plain(STD), ""))

check("fallback", "blocking is stated as a legitimate outcome, not a router failure",
      lambda: ("is a correct result, not a failure of the router" in plain(PREC), ""))

check("fallback", "a weaker eligibility constraint is case B, not a degraded fallback",
      lambda: ("it is case B of" in plain(PREC)
               and "Operator acknowledgement is not sufficient and is not the mechanism" in plain(PREC), ""))

# =========================================================== human control

check("human", "human may select, require, prohibit, accept degraded, or block",
      lambda: (all(w in plain(A) for w in ["select", "require", "prohibit",
                                           "accept a declared degraded fallback", "block"]), ""))

check("human", "human cannot make an ineligible model eligible by any act of their own",
      lambda: ("make an ineligible model eligible by any act of their own" in plain(A)
               and "no exception path exists at all" in plain(A)
               and "Human override cannot reach a mandatory constraint" in plain(STD), ""))

check("human", "no routing act waives reviewer independence, with or without a Decision Right",
      lambda: ("waive reviewer independence by any routing act" in plain(A)
               and "no routing choice or model-diversity adjustment touches it" in plain(A)
               and "never touches reviewer independence" in plain(STD).lower(), ""))

check("human", "human cannot make output true or canonical, nor rewrite routing history",
      lambda: ("make output true or canonical" in plain(A)
               and "rewrite routing history" in plain(A), ""))

check("human", "operator choice, acknowledgement and governed exception are three acts",
      lambda: ("Three different acts, kept apart" in plain(A)
               and "Adjusts no requirement" in plain(A)
               and "re-evaluated against it" in plain(A)
               and "never called eligible under the original policy" in plain(A), ""))

# =========================================================== privacy / Phase 8 integration

check("privacy", "Phase 8 sensitivity classes used, not redefined",
      lambda: ("used, not redefined" in plain(A)
               and "PERSONAL_DATA" in TMPL["deployment-profile-template.md"], ""))

check("privacy", "sensitivity classification never names a provider",
      lambda: ("A sensitivity classification never names a provider" in plain(A), ""))

check("privacy", "provider suitability is explicit policy and evidence, never inferred",
      lambda: ("never inferred from reputation, scale, or the absence of a known incident"
               in plain(A), ""))

check("privacy", "routing never moves knowledge across a scope boundary",
      lambda: ("never moves knowledge across a scope boundary" in plain(A)
               and "Selecting a deployment never moves knowledge across a scope boundary"
               in plain(STD), ""))

check("privacy", "PERSONAL / organisational separation explicitly untouched",
      lambda: ("PERSONAL / organisational separation is untouched" in plain(A)
               and "knowledge/scope-isolation-and-transfer.md" in A, ""))

check("privacy", "routing changes no canonicality and no visibility",
      lambda: ("Routing changes no canonicality and no visibility" in plain(A)
               and "Routing changes nothing about knowledge" in plain(STD), ""))

check("privacy", "no IAM, identity or access-control mechanism designed",
      lambda: ("No identity, permission or access-control mechanism is designed here" in plain(A), ""))

# =========================================================== routing decision record

check("decision-record", "routing decision template enumerates its required elements",
      lambda: (len(re.findall(r"^\| \d+ \|", TMPL["routing-decision-template.md"], re.M)) >= 20,
               "%d elements" % len(re.findall(r"^\| \d+ \|",
                                              TMPL["routing-decision-template.md"], re.M))))

for label, needle in [("policy version", "routing_policy.<id>` **and policy version**"),
                      ("model profile stable id and registry version", "Registry Profile Version"),
                      ("candidate set", "Enumerated candidate set"),
                      ("per-candidate eligibility", "Eligibility result per enumerated candidate"),
                      ("selection reason", "Reason for selection"),
                      ("fallback candidates", "Declared fallback candidates"),
                      ("diversity prior", "named prior Routing Decision"),
                      ("availability at selection", "Availability class per candidate at evaluation time"),
                      ("human involvement", "Act requirements"),
                      ("block outcome", "BLOCKED_FOR_ROUTING"),
                      ("audit history", "append-only")]:
    check("decision-record", "routing decision records %s" % label,
          (lambda n=needle: (n in TMPL["routing-decision-template.md"], "")))

check("decision-record", "degraded selection names its dimension; exception chain is separate",
      lambda: ("the dimension on which it is weaker, and the acknowledgement"
               in plain(TMPL["routing-decision-template.md"])
               and "the full case-B chain" in plain(TMPL["routing-decision-template.md"]), ""))

check("decision-record", "a degraded fallback recorded as ordinary selection is a defect",
      lambda: ("is a defect in the record" in plain(TMPL["routing-decision-template.md"]), ""))

check("decision-record", "routing decisions are not editable; corrections are new linked records",
      lambda: ("not editable" in plain(TMPL["routing-decision-template.md"])
               and "new linked decision" in plain(TMPL["routing-decision-template.md"]), ""))

check("decision-record", "routing reproducibility claimed; output reproducibility not claimed",
      lambda: ("Routing reproducibility" in A and "Model-output reproducibility" in A
               and "Not claimed, not achievable" in plain(A)
               and "Routing reproducibility only" in plain(STD), ""))

# =========================================================== templates

check("templates", "five templates present and discovered on disk",
      lambda: (len(TEMPLATES) == 5, "%d: %s" % (len(TEMPLATES),
                                                sorted(os.path.basename(t) for t in TEMPLATES))))

check("templates", "every template carries a non-runtime statement",
      lambda: (all("## Non-Runtime Statement" in TMPL[t] for t in TMPL), "%d" % len(TMPL)))

check("templates", "deployment template forbids URLs, credentials and infrastructure detail",
      lambda: ("No URL, hostname, credential, key, region code, infrastructure configuration or "
               "network detail" in plain(TMPL["deployment-profile-template.md"]), ""))

check("templates", "model profile uses semantic bands, never prices or measured latencies",
      lambda: ("No prices, rates, token costs or measured latencies"
               in plain(TMPL["model-profile-template.md"])
               and all(b in TMPL["model-profile-template.md"]
                       for b in ["COST_LOW", "COST_PREMIUM", "LATENCY_INTERACTIVE", "LATENCY_BATCH"]), ""))

check("templates", "provider template records concentration and substitutability",
      lambda: ("Concentration and Substitutability" in TMPL["provider-profile-template.md"]
               and "is a concentration, not a control"
               in plain(TMPL["provider-profile-template.md"]), ""))

check("templates", "routing policy template declares out-of-scope authority",
      lambda: ("## Out-of-Scope Authority" in TMPL["routing-policy-template.md"]
               and "A blank section is a defect" in plain(TMPL["routing-policy-template.md"]), ""))

check("templates", "every Phase 9 file inherits the common standard",
      lambda: (lambda missing: (not missing, str(missing) if missing
                                else "%d files" % (len(MODEL_FILES) - 1)))(
          [f for f in MODEL_FILES if f != STANDARD
           and "standard.model.common_constraints@0.1" not in DOCS[f]]))


def constraint_numbers():
    return [int(n) for n in re.findall(r"^## (\d+)\. ", STD, re.M)]


check("templates", "standard numbering is contiguous from 1 and matches the inventory",
      lambda: (constraint_numbers() == list(range(1, len(constraint_numbers()) + 1))
               and ("| Enforceable constraints | %d |" % len(constraint_numbers())) in plain(UNIV),
               "%d constraints" % len(constraint_numbers())))

# =========================================================== exemplars

check("exemplars", "at least eight exemplars discovered on disk",
      lambda: (len(EXEMPLARS) >= 8, "%d: %s" % (len(EXEMPLARS),
                                                [os.path.basename(e) for e in EXEMPLARS])))

check("exemplars", "every exemplar remains PROPOSED",
      lambda: (all("Status: PROPOSED" in DOCS[e] for e in EXEMPLARS), ""))

EXEMPLAR_PROOFS = {
    "routine-drafting-low-cost.md": "already-filtered set",
    "high-criticality-reasoning.md": "not the same as",
    "independent-assurance-family-diversity.md": "two controls",
    "privacy-restricted-deployment.md": "multi-label subset test",
    "vision-requirement-excludes-text-only.md": "ABSOLUTELY_NON_WAIVABLE",
    "provider-outage-equivalent-fallback.md": "never a reason to relax",
    "no-eligible-model-block.md": "correct outcome",
    "deprecated-model-history-preserved.md": "removes nothing",
    "degraded-fallback-governed-exception.md": "never called eligible",
}
for fname, needle in EXEMPLAR_PROOFS.items():
    check("exemplars", "exemplar %s states what it proves" % fname.replace(".md", ""),
          (lambda f=fname, n=needle: ("models/exemplars/" + f in DOCS
                                      and n in plain(DOCS["models/exemplars/" + f]), "")))

# Stricter: case-insensitive on the phrase (the previous version matched case and missed the
# sentence it was written for), AND requires the exemplar to refuse both partial-eligibility
# formulations, name the block outcome, and state the unsatisfiable combination.
def block_exemplar_refuses_closest_fit():
    doc = plain(DOCS["models/exemplars/no-eligible-model-block.md"])
    low = doc.lower()
    needed = {
        "fewest-violations refused": "fewest violations" in low,
        "closest refused": "closest" in low,
        "no partial eligibility": "no partial eligibility" in low,
        "block outcome named": "BLOCKED_FOR_ROUTING" in doc and "NO_ELIGIBLE_MODEL" in doc,
        "unsatisfiable combination named": "unsatisfiable" in low,
        "not a router failure": "not the router failing" in low,
    }
    missing = [k for k, ok in needed.items() if not ok]
    return (not missing, str(missing) if missing else "all %d properties present" % len(needed))


check("exemplars", "block exemplar refuses closest-fit and names the unsatisfiable combination",
      block_exemplar_refuses_closest_fit)

check("exemplars", "outage exemplar shows the available-but-prohibited route refused",
      lambda: ("PROHIBITED_FALLBACK"
               in DOCS["models/exemplars/provider-outage-equivalent-fallback.md"], ""))

check("exemplars", "history exemplar preserves profile and policy versions",
      lambda: (all(t in DOCS["models/exemplars/deprecated-model-history-preserved.md"]
                   for t in ["v2", "v3", "Intact"]), ""))

# =========================================================== regression / hygiene

for label, paths in UPSTREAM_PATHS.items():
    check("regression", "%s unchanged since Phase 8 baseline" % label,
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


check("regression", "every Phase 9 artifact is PROPOSED (approval records excluded)",
      lambda: artifacts_remain_proposed(DOCS, "Phase 9"))

RUNTIME = re.compile(  # self-literal
    r"\b(import openai|import anthropic|api[_-]?key|bearer token|CREATE TABLE|REST API|"  # self-literal
    r"POST /|https?://|SELECT \*|OAuth|LDAP|SAML|pip install|npm install)\b", re.I)  # self-literal
check("regression", "no provider SDK, API call, credential, endpoint or runtime construct",
      lambda: (lambda hits: (not hits, str(hits) if hits else "0 across %d files" % len(DOCS)))(
          [rel for rel, doc in DOCS.items() if RUNTIME.search(doc)]))

check("regression", "non-runtime statement present in architecture and enumerated",
      lambda: ("## 8. Non-runtime statement" in A
               and all(w in A for w in ["provider SDK", "credential", "billing integration",
                                        "latency probe", "failover service", "evaluation service",
                                        "agent orchestration", "queue", "dashboard",
                                        "telemetry pipeline"]), ""))

check("regression", "no model, provider or deployment profile instance was created",
      lambda: (not any(re.search(r"^- Model Profile ID: `model\.", DOCS[f], re.M)
                       for f in MODEL_FILES if "_templates" not in f)
               and "No Model Profile, Provider Profile or Deployment Profile is created"
               in plain(UNIV), "profiles are populated by a later governed pass"))

check("regression", "no named human or organisation bound",
      lambda: (not re.search(r"\b(Mr|Ms|Mrs|Dr)\.? [A-Z][a-z]+", ALL9)
               and "never a named person" in plain(TMPL["routing-policy-template.md"]), ""))


SELF_START = "# --- self-inspection region (excluded from its own scans) ---"
SELF_END = "# --- end self-inspection region ---"


def harness_body_excluding_self_inspection():
    """The harness source minus the self-inspecting checks, which necessarily contain the
    literals they search for. Markers are matched as standalone lines so the constants that
    hold the marker text are not mistaken for the markers."""
    src = read("validation/phase_9_validation.py")
    body = src.split('"""', 2)[2]
    kept, skipping = [], False
    for line in body.splitlines():
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
    """The harness must not itself be runtime. This check can fail."""
    body = harness_body_excluding_self_inspection()
    problems = []
    if RUNTIME.search(body):
        problems.append("runtime construct in harness")
    for banned in ("urllib", "socket", "requests"):
        if banned in body:
            problems.append(banned)
    for cmd in re.findall(r"subprocess\.run\(\[([^\]]*)\]", body):
        if '"git"' not in cmd:
            problems.append("non-git subprocess")
        for w in ("commit", "push", "add", "checkout", "reset"):
            if '"%s"' % w in cmd:
                problems.append("mutating git: %s" % w)
    return (not problems, str(sorted(set(problems))) if problems
            else "read-only, stdlib only, git read-only")


def no_vacuous_checks():
    """No unconditional-pass construct anywhere. Patterns are assembled from fragments so a
    plain grep of this file finds no literal occurrence outside this docstring."""
    body = harness_body_excluding_self_inspection().split("RESULTS = []", 1)[-1]
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


def no_local_pr_action():
    """Offline scope: proves no PR artifact and no PR-creating call exist LOCALLY."""
    if os.path.exists(os.path.join(REPO, ".git", "PULL_REQUEST")):
        return (False, "local PR artifact present")
    pattern = "create" + "_pull_" + "request"
    cli = "gh pr " + "create"
    for rel in discover("validation", ".py"):
        body = (harness_body_excluding_self_inspection()
                if rel.endswith("phase_9_validation.py") else read(rel))
        if pattern in body or cli in body:
            return (False, "PR-creating call in %s" % rel)
    return (True, "LOCAL ONLY - remote open-PR state is NOT provable offline and is not claimed")


# --- end self-inspection region ---

check("regression", "harness is read-only and implements nothing", harness_is_read_only)
check("regression", "harness contains no vacuous or unconditional-pass checks", no_vacuous_checks)
check("regression", "no local PR artifact or PR-creating action (local scope only)",
      no_local_pr_action)


# =========================================================== cross-registry references
# The re-audit found the harness did not validate referenced Review/Decision IDs against the
# approved registries. Exemplar 9 cited two objects that do not exist and passed 204 checks.

def approved_ids(pattern, *paths):
    found = set()
    for rel in paths:
        for root, _d, files in os.walk(os.path.join(REPO, rel)):
            for name in sorted(files):
                if name.endswith(".md"):
                    found |= set(re.findall(pattern,
                                            read(os.path.relpath(os.path.join(root, name), REPO))))
    return found


APPROVED_REVIEWS = approved_ids(r"`(review\.[a-z_]+)`", "reviews")
APPROVED_DECISIONS = approved_ids(r"`(decision\.[a-z_]+)`", "decisions")
# Decision Rights that are actually CARDED, which is what "a valid Right" means.
CARDED_DECISIONS = set()
for _rel in discover("decisions/exemplars"):
    _m = re.search(r"^- Decision ID: \*?\*?`(decision\.[a-z_]+)`", read(_rel), re.M)
    if _m:
        CARDED_DECISIONS.add(_m.group(1))


def unresolved_cross_registry_refs():
    """Every review.<id> and decision.<id> in Phase 9 must exist in the approved registries."""
    bad = []
    for rel, doc in DOCS.items():
        for token in set(re.findall(r"`(review\.[a-z_]+)`", doc)):
            if token not in APPROVED_REVIEWS:
                bad.append("%s: %s" % (rel, token))
        for token in set(re.findall(r"`(decision\.[a-z_]+)`", doc)):
            if token not in APPROVED_DECISIONS:
                bad.append("%s: %s" % (rel, token))
    return (not bad, str(sorted(set(bad))) if bad
            else "0 unresolved across %d files (%d approved reviews, %d approved decisions)"
            % (len(DOCS), len(APPROVED_REVIEWS), len(APPROVED_DECISIONS)))


check("cross-registry", "every review.<id> and decision.<id> resolves to an approved registry object",
      unresolved_cross_registry_refs)

check("cross-registry", "approved registries were actually found, so the check is not vacuous",
      lambda: (len(APPROVED_REVIEWS) >= 20 and len(CARDED_DECISIONS) == 8,
               "%d review IDs, %d carded Decision Rights" % (len(APPROVED_REVIEWS),
                                                             len(CARDED_DECISIONS))))


def exception_paths_cite_carded_rights():
    """A governed exception must name a CARDED Right, or state that none exists and block."""
    problems = []
    for rel in EXEMPLARS:
        doc = DOCS[rel]
        if "GOVERNED_EXCEPTION_POSSIBLE" not in doc and "governed exception" not in doc.lower():
            continue
        cited = set(re.findall(r"`(decision\.[a-z_]+)`", doc))
        uncarded = cited - CARDED_DECISIONS
        claims_exception_taken = re.search(r"adjusted (routing )?context (was )?creat|"
                                           r"eligible under the adjusted context", doc, re.I)
        if uncarded:
            problems.append("%s cites uncarded %s" % (os.path.basename(rel), sorted(uncarded)))
        if claims_exception_taken and not re.search(r"BLOCKED_FOR_ROUTING", doc):
            problems.append("%s exercises an exception without a blocking alternative recorded"
                            % os.path.basename(rel))
    return (not problems, str(problems) if problems
            else "exception paths cite only carded Rights or block")


check("cross-registry", "exception paths cite only carded Decision Rights",
      exception_paths_cite_carded_rights)

check("cross-registry", "no approved Phase 7 Right covers a routing constraint class, and that is stated",
      lambda: ("None of them covers a model-capability threshold"
               in plain(DOCS["models/exemplars/degraded-fallback-governed-exception.md"])
               and "BLOCKED_FOR_ROUTING"
               in DOCS["models/exemplars/degraded-fallback-governed-exception.md"], ""))

# =========================================================== identity / version consistency

def no_release_change_as_version_bump():
    """A changed underlying release must never be absorbed into a registry profile version."""
    bad = []
    for rel, doc in NORMATIVE.items():
        for m in re.finditer(r"provider version change is a profile version change", doc, re.I):
            window = doc[max(0, m.start() - 300):m.end() + 300]
            if REMEDIATION_CONTEXT.search(window):
                continue
            bad.append(rel)
    return (not bad and "never absorbs a change of the underlying release" in plain(LIFE)
            and "A different Model Profile" in LIFE.split("### A changed underlying release")[1],
            str(sorted(set(bad))) if bad else "release change yields a distinct profile")


check("identity-stack", "a changed underlying release is a distinct profile, never a version bump",
      no_release_change_as_version_bump)

check("identity-stack", "uncertainty about a release change defaults to the safe reading",
      lambda: ("Treated as a changed release" in LIFE
               and "SUSPENDED` pending that evidence" in LIFE, ""))

check("identity-stack", "PROVIDER_VERSION_CHANGE fires an identity review, not a version bump",
      lambda: ("fires an identity review, not a version bump" in plain(LIFE), ""))

# =========================================================== derived inventory counts
# The re-audit found stale counts in active prose. These derive every count from the files.


def declared_capabilities():
    return sorted(set(re.findall(r"^\| `(capability\.[a-z_]+)` \|", CAP, re.M)))


def counted(label, actual, *docs):
    """The stated number must equal the derived one, wherever it is stated."""
    stale = []
    for name, doc in docs:
        for m in re.finditer(r"(\d+)[- ]%s" % label, doc):
            if int(m.group(1)) != actual:
                stale.append("%s: %s-%s (actual %d)" % (name, m.group(1), label, actual))
    return stale


check("inventory", "capability count consistent everywhere it is stated",
      lambda: (lambda stale: (not stale and len(declared_capabilities()) == 23,
                              str(stale) if stale else "%d families" % len(declared_capabilities())))(
          counted("family", len(declared_capabilities()), ("arch", A), ("uni", UNIV), ("cap", CAP))
          + counted("capability families", len(declared_capabilities()),
                    ("arch", A), ("uni", UNIV), ("cap", CAP))))

check("inventory", "no stale twenty-four-dimension prose survives",
      lambda: (lambda stale: (not stale, str(stale) if stale else "0 stale word-form counts"))(
          [rel for rel, doc in NORMATIVE.items()
           if re.search(r"twenty-four dimensions|twenty-four families", doc, re.I)]))

check("inventory", "eligibility-constraint count in the universe matches the parsed table",
      lambda: (lambda n: (("| Eligibility constraints | **%d** |" % n) in UNIV,
                          "%d parsed" % n))(len({t for r in eligibility_table_rows()
                                                 for t in r[0].split(", ") if t})))

check("inventory", "preference count in the universe matches the parsed table",
      lambda: (lambda n: (("| Preferences | **%d**" % n) in UNIV, "%d parsed" % n))(
          len(re.findall(r"^\| `PREFER_[A-Z_]+` \|",
                         CONS.split("## 6. Preferences")[1].split("### When cost")[0], re.M))))

check("inventory", "constraint count in the artifact table matches the standard",
      lambda: (lambda n: (("| %d inherited rules |" % n) in UNIV, "%d rules" % n))(
          len(re.findall(r"^## (\d+)\. ", STD, re.M))))

check("inventory", "no stale 'hard and soft' constraint summary survives",
      lambda: (lambda stale: (not stale, str(stale) if stale else "0 stale summaries"))(
          [rel for rel, doc in NORMATIVE.items()
           if re.search(r"\d+ hard and \d+ soft", doc)]))

check("inventory", "the inexpressible list matches its own heading count",
      lambda: (lambda heading, items: (heading == items,
                                       "heading says %d, lists %d" % (heading, items)))(
          {"Two": 2, "Three": 3, "Four": 4}[
              re.search(r"## 4\. (\w+) things this architecture cannot express", UNIV).group(1)],
          len(re.findall(r"^\d+\. \*\*",
                         UNIV.split("cannot express")[1].split("## 5.")[0], re.M))))

check("inventory", "no removed capability token is referenced outside its removal note",
      lambda: (lambda bad: (not bad, str(bad) if bad else "0 live references"))(
          [rel for rel, doc in NORMATIVE.items()
           for m in re.finditer(r"capability\.privacy_sensitive_suitability", doc)
           if not REMEDIATION_CONTEXT.search(doc[max(0, m.start() - 400):m.end() + 400])]))


# =========================================================== §1.2 provider-side cases

PROVIDER_CASES = ["Provider marketing alias rename",
                  "Provider contractual or data-handling change",
                  "Provider backend behaviour materially changes",
                  "Deployment configuration or residency change",
                  "AI-OS metadata or evidence correction"]
check("identity-stack", "all five provider-side change cases distinguished",
      lambda: (lambda missing: (not missing, str(missing) if missing
                                else "%d cases" % len(PROVIDER_CASES)))(
          [c for c in PROVIDER_CASES if c not in LIFE]))

check("identity-stack", "unprovable sameness yields a new identity or a recorded conflict",
      lambda: ("identity conflict" in plain(LIFE).lower()
               and "Never silently a registry-profile-version bump" in plain(LIFE)
               and "Unprovable sameness is not sameness" in plain(LIFE), ""))

check("identity-stack", "the identity rule is in the standard, not only the model doc",
      lambda: ("A Model Profile identity is bound to one underlying release" in plain(STD)
               and "never a version increment" in plain(STD), ""))

# =========================================================== §2.4 cross-registry integrity rule

check("cross-registry", "the cross-registry integrity rule is normative in architecture and standard",
      lambda: ("Cross-registry governance references" in A
               and "FUTURE_GOVERNANCE_REFERENCE" in A and "FUTURE_GOVERNANCE_REFERENCE" in STD
               and "never appears as though exercisable" in plain(A), ""))

check("cross-registry", "the rule reaches templates and Routing Decision records",
      lambda: ("Cross-Registry Governance References" in TMPL["routing-decision-template.md"]
               and "REVIEW_PROFILE_NOT_BOUND_IN_PHASE_9"
               in TMPL["routing-decision-template.md"], ""))

check("cross-registry", "carding a Right is stated to be a Phase 7 act, never a Phase 9 one",
      lambda: ("carding a right is a phase 7 act" in plain(STD).lower()
               and "never something phase 9 performs, implies or assumes" in plain(A).lower(), ""))

# =========================================================== §5.6 exemplar 9 governance integrity

EX9 = "models/exemplars/degraded-fallback-governed-exception.md"


def exemplar9_governance_integrity():
    doc = DOCS[EX9]
    flat = plain(doc)
    problems = []
    # 1. no unresolved Right or Profile presented as exercisable
    for token in set(re.findall(r"`(decision\.[a-z_]+|review\.[a-z_]+)`", doc)):
        if token.startswith("decision.") and token not in APPROVED_DECISIONS:
            problems.append("unresolved %s" % token)
        if token.startswith("review.") and token not in APPROVED_REVIEWS:
            problems.append("unresolved %s" % token)
    # 2. reaches the governance boundary and records it
    if "NO_APPLICABLE_DECISION_RIGHT" not in doc:
        problems.append("no NO_APPLICABLE_DECISION_RIGHT outcome")
    if "BLOCKED_FOR_ROUTING" not in doc:
        problems.append("no blocking outcome")
    # 3. never marks a candidate eligible
    if re.search(r"^\| `model\.[a-z_]+`[^|]*\| \*\*Yes\*\*", doc, re.M):
        problems.append("a candidate is marked eligible")
    # 4. creates no adjusted requirement context
    if re.search(r"adjusted (routing )?context (is|was) creat", doc, re.I):
        problems.append("creates an adjusted context without an approved Right")
    # 5. does not confuse diversity with reviewer independence
    if not re.search(r"two controls", flat, re.I):
        problems.append("does not separate diversity from reviewer independence")
    if re.search(r"(waiv|drop|reduc)[a-z]* .{0,40}diversity .{0,40}waiv.{0,20}independence", flat, re.I):
        problems.append("conflates diversity with reviewer independence")
    # 6. future carding is a Phase 7 act
    if "Phase 7 governance extension" not in doc:
        problems.append("does not state that carding is a Phase 7 extension")
    return (not problems, str(problems) if problems
            else "all six governance-integrity properties hold")


check("cross-registry", "exemplar 9 governance integrity", exemplar9_governance_integrity)

# =========================================================== §5.3 undeclared capability references

def undeclared_capability_refs():
    """Derive declared capability IDs from the taxonomy; fail on any active undeclared use."""
    declared = set(declared_capabilities())
    bad = []
    for rel, doc in NORMATIVE.items():
        for m in re.finditer(r"`(capability\.[a-z_]+)`", doc):
            token = m.group(1)
            if token in declared:
                continue
            window = doc[max(0, m.start() - 400):m.end() + 400]
            if REMEDIATION_CONTEXT.search(window):
                continue
            bad.append("%s: %s" % (rel, token))
    return (not bad and len(declared) == 23,
            str(sorted(set(bad))) if bad
            else "0 undeclared active refs against %d declared families" % len(declared))


check("inventory", "no undeclared capability.<id> is actively referenced",
      undeclared_capability_refs)

# =========================================================== §5.4 derived count cross-checks

def act_requirement_count():
    block_ = CONS.split("## 7. Act requirements")[1].split("## 8.")[0]
    return len(re.findall(r"^\| `([A-Z_]+)` \|", block_, re.M))


def evidence_class_count():
    block_ = EVID.split("## 2. Evidence classes")[1].split("### Rules")[0]
    return len(re.findall(r"^\| `([A-Z_]+)` \|", block_, re.M))


def routing_decision_elements():
    return len(re.findall(r"^\| \d+ \|", TMPL["routing-decision-template.md"], re.M))


DERIVED = {
    "capability families": (len(declared_capabilities()), 23),
    "primary lifecycle states": (len(declared_lifecycle_states()), 6),
    "eligibility constraints": (len({t for r in eligibility_table_rows()
                                     for t in r[0].split(", ") if t}), 27),
    "preferences": (len(re.findall(r"^\| `PREFER_[A-Z_]+` \|",
                                   CONS.split("## 6. Preferences")[1].split("### When cost")[0],
                                   re.M)), 9),
    "act requirements": (act_requirement_count(), 3),
    "common constraints": (len(re.findall(r"^## (\d+)\. ", STD, re.M)), 45),
    "evidence classes": (evidence_class_count(), 6),
    "templates": (len(TEMPLATES), 5),
    "exemplars": (len(EXEMPLARS), 9),
    "routing decision elements": (routing_decision_elements(), 35),
}
for _label, (_actual, _expected) in DERIVED.items():
    check("inventory", "derived count matches expectation: %s" % _label,
          (lambda a=_actual, e=_expected, l=_label: (a == e, "%s = %d (expected %d)" % (l, a, e))))


def stale_numbers_in_active_prose():
    """Any stated count contradicting a derived one, in active normative prose."""
    patterns = {
        r"(\d+)[- ]capability famil": DERIVED["capability families"][0],
        r"(\d+)[- ]famil(?:y|ies) taxonomy": DERIVED["capability families"][0],
        r"(\d+) inherited rules": DERIVED["common constraints"][0],
        r"(\d+) eligibility constraints": DERIVED["eligibility constraints"][0],
        r"(\d+) preferences": DERIVED["preferences"][0],
        r"(\d+) act requirements": DERIVED["act requirements"][0],
        r"(\d+) lifecycle states": DERIVED["primary lifecycle states"][0],
        r"(\d+) evidence classes": DERIVED["evidence classes"][0],
    }
    bad = []
    for rel, doc in NORMATIVE.items():
        for pat, actual in patterns.items():
            for m in re.finditer(pat, doc):
                if int(m.group(1)) != actual:
                    window = doc[max(0, m.start() - 250):m.end() + 250]
                    if REMEDIATION_CONTEXT.search(window):
                        continue
                    bad.append("%s: %s (actual %d)" % (rel, m.group(0), actual))
    return (not bad, str(sorted(set(bad))) if bad else "0 stale counts in active prose")


check("inventory", "no stale count contradicts a derived one in active prose",
      stale_numbers_in_active_prose)


def heading_list_cardinality():
    """A heading claiming N items must govern a list of N."""
    words = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6,
             "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10}
    bad = []
    for rel, doc in NORMATIVE.items():
        for m in re.finditer(r"^#{2,3} (?:\d+\.?\w?\. )?(%s) ([a-z][^\n]*)$"
                             % "|".join(words), doc, re.M):
            claimed = words[m.group(1)]
            body = doc[m.end():]
            body = body.split("\n## ")[0].split("\n### ")[0]
            numbered = len(re.findall(r"^\d+\. ", body, re.M))
            # Table rows only: skip the header row and the |---| separator, which are not items.
            rows = [ln for ln in body.splitlines()
                    if ln.startswith("| ") and not re.match(r"^\|[\s:-]+\|", ln)]
            table_items = max(0, len(rows) - 1) if rows else 0
            items = numbered or table_items
            if items and items != claimed:
                bad.append("%s: '%s %s' governs %d" % (rel, m.group(1), m.group(2)[:40], items))
    return (not bad, str(bad) if bad else "headings match their lists")


check("inventory", "a heading claiming N items governs a list of N",
      heading_list_cardinality)


# =========================================================== final conformance cleanup
# The approval re-audit found defects that a 239/239 PASS had not caught: exemplars carrying
# a prose approximation of the Candidate Universe Definition rather than its mandatory
# elements, a declared candidate count disagreeing with the candidates actually assessed,
# stage-6 preferences described as stage 7, and stale counts in the producer self-check —
# which the count scans had excluded from their own scope. These close each of those.

SELF_CHECK = "reviews/phase-9-foundation-self-check.md"
SELF = DOCS[SELF_CHECK]

# The current producer self-check is an *active* description of the architecture, not a
# historical record, so it is scanned with the normative files rather than exempted.
ACTIVE = dict(NORMATIVE)
ACTIVE[SELF_CHECK] = SELF

CUD_ELEMENTS = ["Registry state reference", "Universe definition version", "Inclusion rule",
                "Routing scope", "Pre-filter exclusions", "Enumerated candidate set",
                "Omission reasons", "Completeness result", "Behaviour if incomplete"]


def universe_block(doc):
    """The exemplar's bound Candidate Universe Definition, or None if it has none."""
    m = re.search(r"^## Candidate universe\s*$", doc, re.M)
    if m is None:
        return None
    return doc[m.end():].split("\n## ")[0]


def assessed_candidates(doc):
    """Rows of every candidate-assessment table: a table whose header carries 'Eligible?'."""
    rows, in_table = 0, False
    for line in doc.splitlines():
        if line.startswith("|") and "Eligible?" in line:
            in_table = True
            continue
        if not in_table:
            continue
        if re.match(r"^\|[\s:|-]+\|\s*$", line):     # the |---|---| separator is not a row
            continue
        if line.startswith("|"):
            rows += 1
        else:
            in_table = False
    return rows


def declared_candidates(block):
    m = re.search(r"Enumerated candidate set \| (\d+)", plain(block))
    return int(m.group(1)) if m else None


def exemplar_universe_conformance(rel):
    doc = DOCS[rel]
    block = universe_block(doc)
    if block is None:
        return (False, "no '## Candidate universe' section: the definition is not bound at all")
    flat = plain(block)
    missing = [e for e in CUD_ELEMENTS if e not in flat]
    if not re.search(r"CANDIDATE_UNIVERSE_(COMPLETE|INCOMPLETE)", block):
        missing.append("completeness verdict token")
    if not re.search(r"(?i)\b(BLOCK|ESCALATE)", flat):
        missing.append("declared behaviour on an incomplete universe")
    return (not missing,
            "missing: %s" % missing if missing else "all %d mandatory elements bound"
            % len(CUD_ELEMENTS))


def exemplar_candidate_cardinality(rel):
    doc = DOCS[rel]
    block = universe_block(doc)
    if block is None:
        return (False, "no candidate universe to declare a cardinality")
    declared = declared_candidates(block)
    assessed = assessed_candidates(doc)
    if declared is None:
        return (False, "no declared enumerated cardinality")
    return (declared == assessed,
            "declared %d, assessed %d" % (declared, assessed))


for _rel in EXEMPLARS:
    _name = os.path.basename(_rel).replace(".md", "")
    check("candidate-universe", "exemplar %s binds every mandatory universe element" % _name,
          (lambda r=_rel: exemplar_universe_conformance(r)))
    check("candidate-universe", "exemplar %s enumerates exactly what it assesses" % _name,
          (lambda r=_rel: exemplar_candidate_cardinality(r)))

check("candidate-universe", "no exemplar drops an unavailable candidate from its universe",
      lambda: (lambda bad: (not bad, str(bad) if bad else "availability is evaluated, never pre-filtered"))(
          [os.path.basename(e) for e in EXEMPLARS
           if "UNAVAILABLE" in DOCS[e]
           and "Availability pre-enumeration: no" not in plain(universe_block(DOCS[e]) or "")]))

# --------------------------------------------------------- stage numbering

STAGE_MAP = {
    1: "Legality and governance",
    2: "Sensitivity, handling and residency",
    3: "Required capability, modality, context and tooling",
    4: "Independence and diversity",
    5: "Lifecycle and availability",
    6: "Preferences, in the policy's declared order",
    7: "Deterministic tie-break",
    8: "Act requirements",
}


def normative_stage_map():
    found = {}
    for m in re.finditer(r"^\| *(\d+) \| \*\*([^*]+)\*\*", PREC, re.M):
        found[int(m.group(1))] = m.group(2).strip()
    wrong = ["stage %d is '%s', expected '%s'" % (n, found.get(n), t)
             for n, t in STAGE_MAP.items()
             if not (found.get(n) or "").startswith(t)]
    return (not wrong, str(wrong) if wrong
            else "stages 1-5 fixed filtering, 6 preferences, 7 tie-break, 8 act requirements")


check("precedence", "normative stage map is 1-5 filtering, 6 preferences, 7 tie-break",
      normative_stage_map)


def no_preference_claimed_at_stage_seven():
    """Stage 7 is the deterministic tie-break. A sentence placing a preference there is the
    defect the re-audit found; a sentence that says stage 7 *is* the tie-break is not."""
    bad = []
    for rel, doc in ACTIVE.items():
        flat = plain(doc)
        for m in re.finditer(r"(?i)stage 7", flat):
            # Bound the sentence to its own line: a markdown table row is not prose that
            # continues into the row above it.
            line_start = flat.rfind("\n", 0, m.start()) + 1
            line_end = flat.find("\n", m.end())
            line = flat[line_start:line_end if line_end != -1 else len(flat)]
            rel_start = max(0, line.rfind(".", 0, m.start() - line_start) + 1)
            rel_end = line.find(".", m.end() - line_start)
            sentence = line[rel_start:rel_end if rel_end != -1 else len(line)]
            if re.search(r"(?i)tie-break", sentence):
                continue
            if re.search(r"(?i)\b(cost|latency|preference|PREFER_[A-Z_]+)\b", sentence):
                bad.append("%s: %s" % (rel, sentence.strip()[:110]))
    return (not bad, str(bad) if bad else "no preference is placed at stage 7")


check("precedence", "no active text places a cost or latency preference at stage 7",
      no_preference_claimed_at_stage_seven)

# --------------------------------------------------------- derived counts, self-check included


def negative_evidence_dimensions():
    block_ = EVID.split("## 2a. Applicability of negative evidence")[1].split("### Rules")[0]
    rows = [ln for ln in block_.splitlines()
            if ln.startswith("| ") and not re.match(r"^\|[\s:|-]+\|\s*$", ln)]
    return max(0, len(rows) - 1)


DERIVED["negative-evidence applicability dimensions"] = (negative_evidence_dimensions(), 8)
check("inventory", "derived count matches expectation: negative-evidence dimensions",
      lambda: (negative_evidence_dimensions() == 8,
               "%d dimensions parsed from the authoritative table" % negative_evidence_dimensions()))

WORD_NUM = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
            "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
            "twenty-three": 23, "twenty-four": 24, "twenty-five": 25,
            "thirty-one": 31, "thirty-five": 35, "forty-three": 43, "forty-five": 45}


def claims_against(pattern, actual, label):
    """Every active digit-or-word claim matching `pattern` must equal the derived value."""
    bad = []
    for rel, doc in ACTIVE.items():
        for m in re.finditer(pattern, doc, re.I):
            token = m.group(1).lower()
            stated = int(token) if token.isdigit() else WORD_NUM.get(token)
            if stated is None or stated == actual:
                continue
            window = doc[max(0, m.start() - 250):m.end() + 250]
            if REMEDIATION_CONTEXT.search(window):
                continue
            bad.append("%s: '%s' (actual %d)" % (rel, m.group(0).strip(), actual))
    return (not bad, str(sorted(set(bad))) if bad
            else "%d: every active claim agrees" % actual)


NUM = r"(\d+|[a-z]+(?:-[a-z]+)?)"

check("inventory", "every active Routing Decision element claim matches the template",
      lambda: (lambda bad: (not bad, str(bad) if bad
                            else "%d elements: every active claim agrees"
                            % routing_decision_elements()))(
          [("%s: %s" % (rel, ln.strip()[:90]))
           for rel, doc in ACTIVE.items() for ln in doc.splitlines()
           if re.search(r"(?i)routing decision element|decision-record", ln)
           for mm in re.finditer(r"(\d+) elements", ln)
           if int(mm.group(1)) != routing_decision_elements()]))

check("inventory", "every active capability-family claim matches the taxonomy",
      lambda: claims_against(NUM + r"[- ]capability famil", len(declared_capabilities()),
                             "capability families"))

check("inventory", "every active negative-evidence dimension claim matches its table",
      lambda: claims_against(NUM + r" dimensions, each recorded", negative_evidence_dimensions(),
                             "negative-evidence dimensions"))

check("inventory", "every active common-constraint claim matches the standard",
      lambda: claims_against(
          NUM + r" (?:inherited rules|contiguous constraints|enforceable constraints)",
          DERIVED["common constraints"][0], "common constraints"))

check("inventory", "every active exemplar-count claim matches the files on disk",
      lambda: claims_against(NUM + r"(?: worked)? exemplars?\b", len(EXEMPLARS), "exemplars"))

check("inventory", "the self-check carries no scalar sensitivity ceiling language",
      lambda: (lambda hits: (not hits, str(hits) if hits else "0 scalar constructs"))(
          [m.group(0) for m in re.finditer(
              r"(?i)maximum (approved )?(data )?sensitivity|highest[^.]{0,30}sensitivity class|"
              r"sensitivity[^.]{0,40}at or above", SELF)]))

# --------------------------------------------------------- historical reproducibility identity

REPRO_PARTS = ["Model Profile stable ID", "Registry Profile Version",
               "Underlying Model Release identity", "Provider Offering Mapping",
               "Provider Profile version", "Deployment Profile version"]


def historical_decision_identity(rel):
    """An exemplar recording a decision made in the past must carry the six-part set for it."""
    flat = plain(DOCS[rel])
    missing = [p for p in REPRO_PARTS if p not in flat]
    return (not missing, "missing: %s" % missing if missing
            else "all %d reproducibility parts recorded" % len(REPRO_PARTS))


HISTORICAL_EXEMPLARS = [e for e in EXEMPLARS
                        if re.search(r"(?i)the historical decision", DOCS[e])]
check("decision-record", "a historical exemplar decision exists to check",
      lambda: (len(HISTORICAL_EXEMPLARS) >= 1,
               str([os.path.basename(e) for e in HISTORICAL_EXEMPLARS])))
for _rel in HISTORICAL_EXEMPLARS:
    check("decision-record",
          "historical decision in %s keeps the six-part identity set"
          % os.path.basename(_rel).replace(".md", ""),
          (lambda r=_rel: historical_decision_identity(r)))


# =========================================================== structured count reconciliation
# The human-approval re-audit found the previous count checks syntax- and location-sensitive:
# they matched prose shapes like "23 capability families" and so passed unchanged while the
# master inventory *table* said 24, while `| Routing Decision elements | **31** |` was wrong,
# and while a bolded `**eight**` reverted to `**seven**`. The layer below reconciles every
# active current claim against a parsed authoritative source instead: structured table cells
# are read as cells, and prose is read after markdown emphasis is stripped, so `**eight**`,
# `eight` and `8` are one claim rather than three shapes to enumerate.

AUTHORITATIVE = {
    "capability families": len(declared_capabilities()),
    "eligibility constraints": len({t for r in eligibility_table_rows()
                                    for t in r[0].split(", ") if t}),
    "preferences": len(re.findall(r"^\| `PREFER_[A-Z_]+` \|",
                                  CONS.split("## 6. Preferences")[1].split("### When cost")[0],
                                  re.M)),
    "routing act requirements": act_requirement_count(),
    "primary lifecycle states": len(declared_lifecycle_states()),
    "evidence classes": evidence_class_count(),
    "negative-evidence applicability dimensions": negative_evidence_dimensions(),
    "common governance constraints": len(re.findall(r"^## (\d+)\. ", STD, re.M)),
    "templates": len(TEMPLATES),
    "exemplars": len(EXEMPLARS),
    "Routing Decision elements": routing_decision_elements(),
}

# Every quantity must come from a parsed file, never from a literal in this dictionary.
check("inventory", "every authoritative count is derived from a parsed source, not a constant",
      lambda: (all(isinstance(v, int) and v > 0 for v in AUTHORITATIVE.values())
               and len(AUTHORITATIVE) == 11,
               ", ".join("%s=%d" % kv for kv in sorted(AUTHORITATIVE.items()))))


def master_inventory_rows():
    """The master universe's vocabulary table, read as table cells rather than as prose."""
    body = UNIV.split("| Vocabulary | Members | Owner document |")[1]
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


# Master-table label -> authoritative quantity. A label that stops resolving is itself a
# failure: the check must never pass because it found nothing to compare.
MASTER_LABELS = {
    "Capability families": "capability families",
    "Evidence classes": "evidence classes",
    "Negative-evidence applicability dimensions": "negative-evidence applicability dimensions",
    "Primary lifecycle states": "primary lifecycle states",
    "Eligibility constraints": "eligibility constraints",
    "Act requirements": "routing act requirements",
    "Preferences": "preferences",
    "Routing Decision elements": "Routing Decision elements",
    "Enforceable constraints": "common governance constraints",
}


def master_inventory_reconciled():
    rows = master_inventory_rows()
    missing = [lbl for lbl in MASTER_LABELS if lbl not in rows]
    if missing:
        return (False, "master inventory rows not found, so nothing was compared: %s" % missing)
    wrong = ["%s states %d, authoritative %d" % (lbl, rows[lbl], AUTHORITATIVE[key])
             for lbl, key in MASTER_LABELS.items() if rows[lbl] != AUTHORITATIVE[key]]
    return (not wrong, str(wrong) if wrong
            else "%d master inventory rows reconciled against parsed sources" % len(MASTER_LABELS))


check("inventory", "master universe inventory table reconciles with every parsed source",
      master_inventory_reconciled)


def master_file_counts_reconciled():
    """The artifact table's `models/_templates/` x 5 and `models/exemplars/` x 9 rows."""
    found = {}
    for m in re.finditer(r"`models/(_templates|exemplars)/` × (\d+)", UNIV):
        found[m.group(1)] = int(m.group(2))
    expected = {"_templates": AUTHORITATIVE["templates"], "exemplars": AUTHORITATIVE["exemplars"]}
    missing = [k for k in expected if k not in found]
    if missing:
        return (False, "artifact rows not found, so nothing was compared: %s" % missing)
    wrong = ["%s states %d, on disk %d" % (k, found[k], expected[k])
             for k in expected if found[k] != expected[k]]
    return (not wrong, str(wrong) if wrong else "templates=%d, exemplars=%d on disk"
            % (expected["_templates"], expected["exemplars"]))


check("inventory", "master universe artifact counts reconcile with the files on disk",
      master_file_counts_reconciled)

# --------------------------------------------------------- prose claims, markup-normalised

NUMBER_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
    "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
    "twenty": 20, "twenty-one": 21, "twenty-two": 22, "twenty-three": 23, "twenty-four": 24,
    "twenty-five": 25, "twenty-six": 26, "twenty-seven": 27, "twenty-eight": 28,
    "thirty-one": 31, "thirty-four": 34, "thirty-five": 35, "thirty-six": 36,
    "forty-three": 43, "forty-four": 44, "forty-five": 45, "forty-six": 46,
}


def as_number(token):
    token = token.strip().lower()
    if token.isdigit():
        return int(token)
    return NUMBER_WORDS.get(token)


# Each pattern captures the quantity token immediately before a phrase that can only be a
# current claim about that quantity. Run over plain() text, so emphasis cannot hide a claim.
PROSE_CLAIMS = [
    (r"(\S+)[- ]capability famil(?:y|ies)", "capability families"),
    (r"(\S+)[- ]famil(?:y|ies) taxonomy", "capability families"),
    (r"(\S+) families;", "capability families"),
    (r"(\S+) eligibility constraints", "eligibility constraints"),
    (r"(\S+) preferences", "preferences"),
    (r"(\S+) (?:routing )?act requirements", "routing act requirements"),
    (r"(\S+) (?:primary )?lifecycle states", "primary lifecycle states"),
    (r"(\S+) (?:distinct )?evidence classes", "evidence classes"),
    (r"(?:on|assessed on) (\S+) (?:recorded )?dimensions", "negative-evidence applicability dimensions"),
    (r"(\S+) (?:applicability )?dimensions, each recorded",
     "negative-evidence applicability dimensions"),
    (r"(\S+) (?:inherited rules|contiguous constraints|enforceable constraints|"
     r"common governance constraints)", "common governance constraints"),
    (r"(\S+) Routing Decision elements", "Routing Decision elements"),
    (r"(\S+) elements;", "Routing Decision elements"),
    (r"(\S+) templates;", "templates"),
    (r"(\S+) exemplars\b", "exemplars"),
]


def prose_claims_reconciled():
    bad = []
    for rel, doc in ACTIVE.items():
        flat = plain(doc)
        for pattern, key in PROSE_CLAIMS:
            for m in re.finditer(pattern, flat):
                stated = as_number(m.group(1))
                if stated is None or stated == AUTHORITATIVE[key]:
                    continue
                window = flat[max(0, m.start() - 250):m.end() + 250]
                if REMEDIATION_CONTEXT.search(window):
                    continue
                bad.append("%s: '%s' (%s is %d)"
                           % (rel, m.group(0).strip(), key, AUTHORITATIVE[key]))
    return (not bad, str(sorted(set(bad))) if bad
            else "%d quantities reconciled across %d active documents"
            % (len(AUTHORITATIVE), len(ACTIVE)))


check("inventory", "every active prose count reconciles with its parsed source",
      prose_claims_reconciled)

# --------------------------------------------------------- self-check own cardinalities


def self_check_condition_cardinality():
    """'The prompt's N conditions' must govern a table of N conditions."""
    m = re.search(r"The prompt's (\S+) conditions", plain(SELF))
    if m is None:
        return (False, "no condition-count claim found to check")
    stated = as_number(m.group(1))
    block = SELF.split("## Producer self-check threshold")[1].split("\n## ")[0]
    rows = [ln for ln in block.splitlines()
            if ln.startswith("| ") and not re.match(r"^\|[\s:|-]+\|\s*$", ln)]
    actual = max(0, len(rows) - 1)          # the header row is not a condition
    return (stated == actual, "claims %s, table has %d" % (m.group(1), actual))


check("inventory", "the self-check's stated condition count governs its own table",
      self_check_condition_cardinality)


def self_check_question_cardinality():
    m = re.search(r"Open architecture questions — all (\S+) adjudicated", plain(SELF))
    if m is None:
        return (False, "no open-question count claim found to check")
    stated = as_number(m.group(1))
    block = SELF.split("## Open architecture questions")[1].split("\n## ")[0]
    actual = len(re.findall(r"^\| *\*{0,2}\d+\*{0,2} \|", block, re.M))
    return (stated == actual, "claims %s, table has %d" % (m.group(1), actual))


check("inventory", "the self-check's stated open-question count governs its own table",
      self_check_question_cardinality)


# --- these two checks must stay last: they count the suite, themselves included ---
# The group counts and the total are frozen here, BEFORE either check appends its own result,
# so both describe the same finished suite. Each check below re-derives what the registry will
# hold and fails if this freeze has drifted, so adding a check elsewhere can never leave these
# two silently describing a suite that no longer exists.
_PENDING_FINAL_CHECKS = 2                                              # self-literal
_PENDING_FINAL_GROUP = "inventory"                                     # self-literal


def _freeze_final_counts():
    groups = {}
    for r in RESULTS:
        groups[r["group"]] = groups.get(r["group"], 0) + 1
    groups[_PENDING_FINAL_GROUP] = groups.get(_PENDING_FINAL_GROUP, 0) + _PENDING_FINAL_CHECKS
    return groups, sum(groups.values())


FINAL_GROUPS, FINAL_TOTAL = _freeze_final_counts()


def self_check_group_counts_are_current():
    """Every per-group count stated in the current self-check must equal the number of checks
    this harness actually emits for that group. Derived from the result registry, never from a
    duplicated table."""
    if len(RESULTS) + _PENDING_FINAL_CHECKS != FINAL_TOTAL:
        return (False, "the frozen suite shape has drifted: registry holds %d, frozen %d"
                % (len(RESULTS) + _PENDING_FINAL_CHECKS, FINAL_TOTAL))
    stated = {m.group(1): int(m.group(2))
              for m in re.finditer(r"^\| `([a-z-]+)` \| (\d+) \|", SELF, re.M)}
    if not stated:
        return (False, "no per-group counts found in the self-check, so nothing was compared")
    unknown = sorted(g for g in stated if g not in FINAL_GROUPS)
    wrong = ["%s states %d, suite emits %d" % (g, n, FINAL_GROUPS[g])
             for g, n in sorted(stated.items()) if g in FINAL_GROUPS and n != FINAL_GROUPS[g]]
    absent = sorted(g for g in FINAL_GROUPS if g not in stated)
    problems = wrong + (["no such group: %s" % unknown] if unknown else []) \
        + (["group not stated at all: %s" % absent] if absent else [])
    return (not problems, str(problems) if problems
            else "all %d groups reconciled against the result registry" % len(FINAL_GROUPS))


check("inventory", "the self-check's per-group counts match the groups the suite emits",
      self_check_group_counts_are_current)


def self_check_total_is_current():
    """The producer self-check may not state a total the suite does not actually produce.
    Prior-pass totals (141, 204, 219, 239) are history and belong in the history sentence,
    never in a fraction presented as a result."""
    expected = FINAL_TOTAL
    if len(RESULTS) + 1 != FINAL_TOTAL:
        return (False, "the frozen suite shape has drifted: registry holds %d, frozen %d"
                % (len(RESULTS) + 1, FINAL_TOTAL))
    stated = [(int(m.group(1)), int(m.group(2)))
              for m in re.finditer(r"\b(\d{2,4})/(\d{2,4})\b", SELF)]
    bad = ["%d/%d" % f for f in stated if f != (expected, expected)]
    return (not bad and bool(stated),
            "stale or absent totals: %s (suite is %d/%d)" % (bad, expected, expected)
            if bad or not stated else "self-check states %d/%d and nothing else" % (expected, expected))


check("inventory", "the producer self-check states the suite's actual current total",
      self_check_total_is_current)


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
