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

HARD = ["REQUIRED_CAPABILITY", "REQUIRED_MODALITY", "REQUIRED_CONTEXT_CLASS", "REQUIRED_TOOL_USE",
        "REQUIRED_STRUCTURED_OUTPUT", "REQUIRED_DEPLOYMENT_CLASS",
        "REQUIRED_RESIDENCY_OR_JURISDICTION", "MAX_DATA_SENSITIVITY_ALLOWED",
        "PROVIDER_ALLOWED", "PROVIDER_PROHIBITED", "MODEL_ALLOWED", "MODEL_PROHIBITED",
        "MODEL_FAMILY_ALLOWED", "MODEL_FAMILY_PROHIBITED", "MINIMUM_REASONING_CLASS",
        "MINIMUM_RELIABILITY_CLASS", "MAX_COST_CLASS", "MAX_LATENCY_CLASS",
        "MINIMUM_CONTEXT_CAPACITY_CLASS", "MODEL_DIVERSITY_REQUIRED",
        "PROVIDER_DIVERSITY_REQUIRED", "HUMAN_SELECTION_REQUIRED", "NO_EXTERNAL_PROVIDER",
        "NO_TRAINING_ON_INPUT"]
missing_hard = [h for h in HARD if h not in CONS]
check("constraints", "every required constraint type defined",
      lambda: (not missing_hard, str(missing_hard) if missing_hard else "%d types" % len(HARD)))

check("constraints", "hard constraints filter, soft preferences rank",
      lambda: ("Hard eligibility constraint" in CONS and "Soft preference" in CONS
               and "Filters" in CONS and "Ranks" in CONS, ""))

check("constraints", "a soft preference never overrides a hard constraint",
      lambda: ("A soft preference may never override a hard constraint" in plain(CONS)
               and "A soft preference never overrides a hard constraint" in plain(STD)
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

check("constraints", "MAX_DATA_SENSITIVITY_ALLOWED is a deployment property",
      lambda: ("property of the deployment, not of the model" in plain(CONS), ""))

check("constraints", "NO_TRAINING_ON_INPUT: unstated is not satisfied",
      lambda: ("Unstated is not satisfied" in plain(CONS)
               and "unstated is not satisfied" in plain(TMPL["deployment-profile-template.md"]).lower(), ""))

check("constraints", "HUMAN_SELECTION_REQUIRED is an act, not a filter",
      lambda: ("is not a filter" in plain(CONS) and "requires is a human act" in plain(CONS), ""))

check("constraints", "conflicting hard constraints yield NO_ELIGIBLE_MODEL, not a compromise",
      lambda: ("NO_ELIGIBLE_MODEL" in CONS
               and "fewest constraints" in plain(CONS), ""))

STAGES = ["Legality and governance", "Sensitivity, privacy and residency",
          "Required capability", "Independence and diversity", "Lifecycle and availability",
          "Quality and reliability preference", "Latency and cost preference",
          "Deterministic tie-break"]
check("precedence", "eight ordered precedence stages, hard before soft",
      lambda: (all(s in plain(PREC) for s in STAGES)
               and "Stages 1-5 are hard and cannot be reordered" in plain(PREC).replace("–", "-"),
               "%d stages" % len(STAGES)))

check("precedence", "each stage filters what the next sees",
      lambda: ("Each stage filters the set the next stage sees" in plain(PREC)
               and "can never restore what an earlier one excluded" in plain(PREC), ""))

check("precedence", "cost and latency can never override governance requirements",
      lambda: ("can never override legality, confidentiality, residency, required capability, "
               "review independence, or a criticality requirement" in plain(PREC)
               and "Cost and latency never override governance" in plain(STD), ""))

check("precedence", "reliability preference is ordered before cost preference",
      lambda: (plain(PREC).index("Quality and reliability preference")
               < plain(PREC).index("Latency and cost preference"), "stage 6 before stage 7"))

check("precedence", "preferences are ordered, not weighted",
      lambda: ("A preference states a direction, not a weight" in plain(CONS)
               and "Ordered, not weighted" in plain(TMPL["routing-policy-template.md"]), ""))

check("precedence", "tie-break is deterministic and recorded, never random",
      lambda: ("deterministic and recorded" in plain(PREC)
               and "never random" in plain(PREC)
               and "select the same candidate" in plain(PREC), ""))

check("precedence", "cost may be hard only by declared task policy, and never relaxes others",
      lambda: ("preferences by default" in plain(CONS)
               and "never displaces a governance" in plain(CONS)
               and "the work costs more than the budget" in plain(CONS), ""))

# =========================================================== lifecycle

LIFECYCLE = ["CANDIDATE", "EVALUATING", "ELIGIBLE", "PREFERRED", "RESTRICTED",
             "DEPRECATED", "SUSPENDED", "RETIRED"]
check("lifecycle", "eight lifecycle states defined",
      lambda: (all(re.search(r"\| `%s` \|" % s, LIFE) for s in LIFECYCLE), "%d" % len(LIFECYCLE)))

check("lifecycle", "lifecycle status is not task eligibility",
      lambda: ("Registry status is a gate, not a grant" in plain(LIFE)
               and "Lifecycle status is not task eligibility" in plain(STD), ""))

check("lifecycle", "a globally ELIGIBLE model can be prohibited for a specific task",
      lambda: ("can be prohibited for a particular task" in plain(LIFE), ""))

check("lifecycle", "a PREFERRED model is not mandatory",
      lambda: ("A PREFERRED model is not mandatory" in plain(LIFE)
               and "is not mandatory where policy disqualifies it" in plain(STD), ""))

check("lifecycle", "deprecation excludes new routing and removes nothing",
      lambda: ("excludes a profile from new routing. It removes nothing" in plain(LIFE)
               and "Routing history is preserved through everything" in plain(STD), ""))

check("lifecycle", "historical Routing Decisions preserved through deprecation and incident",
      lambda: ("Preserved intact" in plain(LIFE)
               and "Historical Routing Decisions are preserved through every one of these"
               in plain(LIFE), ""))

check("lifecycle", "three versioned objects, all named by a Routing Decision",
      lambda: ("Model Profile version" in LIFE and "Routing Policy version" in LIFE
               and "A Routing Decision names all three, by version" in plain(LIFE), ""))

check("lifecycle", "a provider version change is a profile version change",
      lambda: ("provider version change is a profile version change" in plain(LIFE), ""))

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

check("fallback", "a fallback satisfies every hard constraint or is not a fallback",
      lambda: ("satisfies every hard constraint or it is not a fallback" in plain(PREC), ""))

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

check("fallback", "material degraded fallback at Decision-Grade needs a Phase 7 exception",
      lambda: ("governed exception under an upstream Phase 7 Decision Right" in plain(PREC)
               and "Operator acknowledgement is not sufficient" in plain(PREC), ""))

# =========================================================== human control

check("human", "human may select, require, prohibit, accept degraded, or block",
      lambda: (all(w in plain(A) for w in ["select", "require", "prohibit",
                                           "accept a declared degraded fallback", "block"]), ""))

check("human", "human cannot make an ineligible model eligible where law/privacy forbids",
      lambda: ("make an ineligible model eligible" in plain(A)
               and "no role, seniority or urgency reaches that" in plain(A)
               and "Human override cannot reach a mandatory constraint" in plain(STD), ""))

check("human", "human cannot waive mandatory review independence without a Decision Right",
      lambda: ("waive mandatory review independence" in plain(A)
               and "a routing choice is not one" in plain(A), ""))

check("human", "human cannot make output true or canonical, nor rewrite routing history",
      lambda: ("make output true or canonical" in plain(A)
               and "rewrite routing history" in plain(A), ""))

check("human", "operator choice and governed exception are distinguished",
      lambda: ("Ordinary operator choice and a governed exception are different acts" in plain(A)
               and "it is either a governed exception" in plain(A).lower(), ""))

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
                      ("model profile version", "profile version**"),
                      ("candidate set", "Candidate set considered"),
                      ("per-candidate eligibility", "Eligibility result per candidate"),
                      ("selection reason", "Reason for selection"),
                      ("fallback candidates", "Declared fallback candidates"),
                      ("diversity prior", "named prior Routing Decision"),
                      ("availability at selection", "at selection time"),
                      ("human involvement", "Human selection, requirement or prohibition"),
                      ("block outcome", "BLOCKED_FOR_ROUTING"),
                      ("audit history", "append-only")]:
    check("decision-record", "routing decision records %s" % label,
          (lambda n=needle: (n in TMPL["routing-decision-template.md"], "")))

check("decision-record", "degraded selection must name dimension, acknowledgement and exception",
      lambda: ("the dimension on which it is weaker, the acknowledgement, and the Phase 7 "
               "exception reference" in plain(TMPL["routing-decision-template.md"]), ""))

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
    "privacy-restricted-deployment.md": "property of the",
    "vision-requirement-excludes-text-only.md": "hard constraint",
    "provider-outage-equivalent-fallback.md": "never a reason to relax",
    "no-eligible-model-block.md": "correct outcome",
    "deprecated-model-history-preserved.md": "removes nothing",
    "degraded-fallback-governed-exception.md": "governed Phase 7 exception",
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
