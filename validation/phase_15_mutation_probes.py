"""Phase 15 — committed controlled-weakening fixture.

Status: PROPOSED. Standard library only, deterministic, no network.

    python3 validation/phase_15_mutation_probes.py [--verbose] [--json]

This fixture answers a question the Phase 15 validator cannot answer about itself: **is each check
load-bearing, or would the architecture pass anyway?**

Each probe names a rule, a piece of Phase 15 text that carries it, and a weakening of that text.
The weakening is applied **in memory** to a temporary copy; the validator is re-run against the
copy; the probe records whether any check failed.

Nothing on disk is edited. No approved Phase 1-13 artifact is copied or modified. Classification is
from EXECUTED BEHAVIOUR, never from a label:

    DETECTED   - the weakening makes at least one validator check fail.
    REDUNDANT  - the weakening changes nothing the validator observes. Recorded honestly and never
                 presented as a pass; a redundant probe is a gap in the harness, stated.

A probe whose target text is not found is an ERROR, not a skip. A runner that quietly matched
nothing would prove exactly as much as no runner at all.

This fixture is an assurance tool and NEVER GOVERNANCE AUTHORITY.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
ARCH = os.path.join("planning", "intent-work-planning-architecture.md")
VALIDATOR = "phase_15_validation.py"

#: (name, document path relative to the repo root, old_text, new_text, rule attacked)
PROBES = [
    # ---- identity separation ------------------------------------------------------------
    ("a Work Plan is allowed to become a Workflow",
     ARCH,
     "**Rule PL-3 — a Work Plan never acquires Workflow identity.**",
     "**Rule PL-3 — a Work Plan is registered as a Workflow once validated.**",
     "Work Plan != Workflow"),

    ("the composed plan section drops its non-Workflow rule",
     "planning/workflow-matching-and-composition.md",
     "**Rule MC-14 — it is not a Workflow, at any point, by any route.**",
     "**Rule MC-14 — a validated plan is written back to the workflow registry.**",
     "a composed plan stays instance-level"),

    ("the identity chain loses its tail",
     ARCH,
     "> `REQUEST != INTENT != WORK PLAN != PLANNED WORK ITEM SPEC != WORKFLOW != WORKFLOW RUN != TASK !=`",
     "> `REQUEST != INTENT != WORK PLAN != PLANNED WORK ITEM SPEC != WORKFLOW != WORKFLOW RUN !=`",
     "the extended identity chain"),

    ("the identity chain is reordered so a Work Plan follows a Workflow",
     ARCH,
     "> `REQUEST != INTENT != WORK PLAN != PLANNED WORK ITEM SPEC != WORKFLOW != WORKFLOW RUN != TASK !=`",
     "> `REQUEST != INTENT != WORKFLOW != WORK PLAN != PLANNED WORK ITEM SPEC != WORKFLOW RUN != TASK !=`",
     "the chain is ordered, not a set"),

    ("a candidate suggestion is allowed to self-register",
     "planning/workflow-candidate-learning-boundary.md",
     "**Rule WL-4 — self-approval is impossible by construction, not by policy.**",
     "**Rule WL-4 — a suggestion is registered automatically once three plans agree.**",
     "no self-registration"),

    ("the registry-write prohibition is removed",
     "planning/workflow-candidate-learning-boundary.md",
     "**Rule WL-2 — the system never writes to a governed registry.**",
     "**Rule WL-2 — the system writes accepted patterns to the workflow registry.**",
     "no registry mutation"),

    # ---- authority ----------------------------------------------------------------------
    ("the planner is allowed to exercise a Decision Right",
     "planning/governance-preflight.md",
     "**Rule GP-9 — it never exercises a Right.**",
     "**Rule GP-9 — the planner exercises the Right where the holder is unambiguous.**",
     "the planner exercises no authority"),

    ("a missing Decision Right stops blocking",
     "planning/failure-and-escalation-model.md",
     "| F-8 | `NO_APPLICABLE_DECISION_RIGHT` | **BLOCK** + escalate | GP-4. There is no alternative branch |",
     "| F-8 | `NO_APPLICABLE_DECISION_RIGHT` | **WARN** and continue | The user can decide later |",
     "a missing Right fails closed"),

    ("business necessity becomes an authority",
     "planning/governance-preflight.md",
     "**Rule GP-5 — business necessity is not an authority.**",
     "**Rule GP-5 — urgency may stand in for an unavailable holder.**",
     "necessity is not authority"),

    ("preflight is allowed to satisfy a review",
     "planning/governance-preflight.md",
     "**Rule GP-8 — it never satisfies a review.**",
     "**Rule GP-8 — preflight satisfies the review where the plan carries its evidence.**",
     "planning satisfies no review"),

    ("the act-posture set loses its blocked posture",
     "planning/governance-preflight.md",
     "| `BLOCKED_FROM_TRANSMISSION` | An act is contemplated and no applicable Right resolves |",
     "",
     "five act postures, including blocked"),

    # ---- model boundary -----------------------------------------------------------------
    ("the trigger envelope is allowed to name a model",
     "planning/orchestrator-handoff-contract.md",
     "**Rule HO-4 — the envelope carries no Model Profile, provider or routing decision.**",
     "**Rule HO-4 — the envelope names the Model Profile the planner selects.**",
     "model selection is Phase 9's"),

    ("a work item is allowed to bind a model",
     "planning/orchestrator-handoff-contract.md",
     "**Rule HO-8 — a spec names no model.**",
     "**Rule HO-8 — a spec names the model that will execute it.**",
     "no model binding in planning"),

    # ---- confidence ---------------------------------------------------------------------
    ("confidence is allowed to grant permission",
     "planning/work-plan-object-model.md",
     "**Rule OM-14 — low confidence may trigger work; high confidence never grants permission.**",
     "**Rule OM-14 — high confidence permits the planner to proceed without clarification.**",
     "confidence is never authority"),

    ("the confidences are aggregated into one number",
     "planning/work-plan-object-model.md",
     "**Rule OM-12 — there is no overall confidence.**",
     "**Rule OM-12 — an overall confidence is the mean of the six.**",
     "six confidences, never aggregated"),

    ("a confidence model omits authority resolution",
     "planning/work-plan-object-model.md",
     "| `authority_resolution` | How sure the Right identification is |",
     "",
     "six separate confidences"),

    # ---- scope --------------------------------------------------------------------------
    ("the scope boundary may be crossed on a good guess",
     "planning/context-scope-resolution.md",
     "**Rule CS-4 — never cross a boundary by guess.**",
     "**Rule CS-4 — the resolver may move between adjacent scopes where similarity is high.**",
     "no boundary crossed by inference"),

    ("prefix matching becomes ancestry",
     "planning/context-scope-resolution.md",
     "**Rule CS-5 — string proximity is not ancestry.**",
     "**Rule CS-5 — a shared scope-path prefix establishes ancestry.**",
     "a scope path is a structured identity"),

    ("material scope ambiguity may be resolved by confidence",
     "planning/context-scope-resolution.md",
     "**Rule CS-7 — material scope ambiguity is always clarified, whatever the confidence.**",
     "**Rule CS-7 — material scope ambiguity is resolved by the highest-confidence candidate.**",
     "scope ambiguity clarifies, never computes"),

    ("the planner records scope entitlement as granted",
     "planning/context-scope-resolution.md",
     "**Rule CS-11 — `entitlement_status` has one permitted value at planning time.**",
     "**Rule CS-11 — `entitlement_status` is `GRANTED` where the originator's default scope matches.**",
     "resolving a scope is not entitlement"),

    # ---- constraints over scores --------------------------------------------------------
    ("a similarity score is allowed to override a constraint",
     "planning/workflow-matching-and-composition.md",
     "**Rule MC-4 — a score never overrides a constraint.**",
     "**Rule MC-4 — a sufficiently high fit score may relax a precondition.**",
     "constraints outrank scores"),

    ("an inadmissible candidate is merely ranked down",
     "planning/workflow-matching-and-composition.md",
     "**Rule MC-3 — inadmissible is not low-scoring.**",
     "**Rule MC-3 — an inadmissible candidate is ranked below admissible ones.**",
     "admissibility gates, it does not rank"),

    # ---- floors and knowledge -----------------------------------------------------------
    ("criticality is allowed to be lowered",
     "planning/work-classification-and-criticality.md",
     "**Rule WC-2 — criticality raises and never lowers.**",
     "**Rule WC-2 — the planner lowers the band where the user reports the work is routine.**",
     "criticality only rises"),

    ("planner output is allowed to become a fact claim",
     "planning/work-plan-object-model.md",
     "**Rule OM-9 — planner output is `AI_SUGGESTION` and stays there.**",
     "**Rule OM-9 — the planner promotes an inference to `FACT_CLAIM` where confidence is high.**",
     "no epistemic conversion in planning"),

    # ---- handoff ------------------------------------------------------------------------
    ("a plan is allowed to hand off without passing preflight",
     "planning/orchestrator-handoff-contract.md",
     "**Rule HO-2 — the handoff happens only on a passing preflight.**",
     "**Rule HO-2 — a plan with non-blocking findings may hand off provisionally.**",
     "handoff requires a validated path"),

    ("the planner becomes a second orchestrator",
     ARCH,
     "**Rule PL-1 — the planner is not a second Orchestrator.**",
     "**Rule PL-1 — the planner creates the run and activates the first stage.**",
     "no second orchestrator"),

    # ---- user experience ----------------------------------------------------------------
    ("the user is required to choose a Workflow",
     "planning/clarification-policy.md",
     "**Rule CL-4 — never ask the user to choose an internal object.**",
     "**Rule CL-4 — where matching is ambiguous the user must select the Workflow.**",
     "internal identifiers stay hidden"),

    ("a blocking clarification is allowed a default",
     "planning/clarification-policy.md",
     "**Rule CL-15 — `default_if_unanswered` on a blocking class is a validation failure.**",
     "**Rule CL-15 — a blocking clarification falls back to its default after a timeout.**",
     "C4 and C5 block, without a default"),

    # ---- the five remediated blockers, re-attacked ---------------------------------------
    ("a runtime Work Item is created before any run exists",
     "planning/work-plan-object-model.md",
     "Phase 15 writes before any run exists, so it cannot own one, cannot pre-create one, and",
     "Phase 15 creates the runtime Work Item for each validated stage, and",
     "PLANNED WORK ITEM SPEC != WORK ITEM"),

    ("the exemplar reinstates the singular multi-valued work_mode",
     "planning/exemplars.md",
     "| `primary_work_mode` | `DRAFTING` |",
     "| `work_mode` | `DRAFTING` and `ANALYSIS` |",
     "one primary mode, a set of secondaries"),

    ("preflight stops requiring the load-bearing determination",
     "planning/governance-preflight.md",
     "every unavailable Role records `load_bearing` **and** `load_bearing_basis` (LB-3)",
     "the planner judges whether the gap matters",
     "F-5 and F-6 have one deterministic disposition"),

    ("a preflight check may hold one stage and release the rest",
     "planning/governance-preflight.md",
     "no check holds one stage while releasing another, and no check",
     "a check may hold one stage while releasing another, and a check may",
     "no partial handoff, no stage progression"),

    ("the self-check keeps a stale open-item count",
     "planning/phase-15-self-check.md",
     "- **Eleven open items** (PO-1",
     "- **Ten open items** (PO-1",
     "stated counts are the package's own counts"),

    # ---- the twelve classes that escaped the independent review, in second locations -----
    ("a repeated pattern auto-registers as an approved Workflow",
     "planning/exemplars.md",
     "**Nothing else happens.** The suggestion is not matched against (WL-3), does not influence any plan,",
     "**What happens next.** The recurring pattern auto-registers as an approved Workflow, is matched against thereafter,",
     "no repeated pattern reaches the registry"),

    ("high confidence skips the C4 question, in an exemplar rather than the policy",
     "planning/exemplars.md",
     "That single question is asked; nothing else is.",
     "Where semantic confidence is high the C4 question is skipped.",
     "C4 blocks regardless of confidence"),

    ("a sibling scope is chosen by name proximity, in an exemplar",
     "planning/exemplars.md",
     "**`ScopeResolution`:** if two municipal projects are live, **`AMBIGUOUS_SCOPE`** — clarify and",
     "**`ScopeResolution`:** if two municipal projects are live, the closest project name determines the scope, and",
     "ancestry never comes from a name"),

    ("an unavailable Role's conclusion passes to the closest available Role",
     "planning/role-skill-requirement-inference.md",
     "What the planner must **not** do is assign the drafting to whichever Role sounds closest and call",
     "Where the owning Role is unavailable, the closest available Role covers the conclusion and calls",
     "never substitute a capability"),

    ("the unapproved communication capability is treated as approved",
     "planning/exemplars.md",
     "| *communication strategy* | — | **No approved Role owns this at the Phase 13 baseline** |",
     "| *communication strategy* | The response strategy | The candidate communication specialist is approved for this |",
     "a candidate capability is absent"),

    ("a ReviewRequirement is satisfied inside the plan",
     "planning/exemplars.md",
     "S5  independent review         review.data_protection  +  review.grant_compliance",
     "S5  the ReviewRequirement is satisfied by the planner and counts as the review",
     "a requirement is never its own satisfaction"),

    ("a DecisionRequirement is exercised by the planner",
     "planning/exemplars.md",
     "under its name. Neither is exercised by the planner.",
     "under its name. Each DecisionRequirement is exercised by the planner once resolved.",
     "a Right is exercised by a human, during the run"),

    ("planning provenance becomes governance evidence",
     "planning/orchestrator-handoff-contract.md",
     "the system understood. It is not evidence for anything the run concludes, and a run may not cite it",
     "the system understood. The planning provenance is governance evidence for what the run concludes, and a run may cite it",
     "a planning record is never evidence"),

    ("a confirmed reading is promoted to a FACT_CLAIM, in the typing table",
     "planning/request-intent-model.md",
     "| The Work Intent, and every inferred field | `AI_SUGGESTION` |",
     "| The Work Intent, once the user confirms it | `AI_SUGGESTION` becomes `FACT_CLAIM` |",
     "no epistemic promotion"),

    ("the planned work item spec names the model that will execute it",
     "planning/orchestrator-handoff-contract.md",
     "| `PlannedWorkItemSpec` records of §3 | Confidence values as decision inputs |",
     "| `PlannedWorkItemSpec` records of §3, each of which names the model profile to execute it | Confidence values as decision inputs |",
     "no planning object selects a model"),

    ("the planner performs the intake checks in advance",
     "planning/orchestrator-handoff-contract.md",
     "Built to make the Orchestrator's seven intake checks answerable",
     "Built so that the planner performs the Orchestrator's seven intake checks in advance",
     "intake checks are made answerable, never performed"),

    ("COMPOSE is declared to satisfy intake check 1",
     ARCH,
     "which is **not a Workflow definition**, so whether it is admissible at all is the Orchestrator's to decide and is open as PO-4 |",
     "which a validated plan satisfies directly, so COMPOSE needs nothing further |",
     "PO-4 stays explicit and fail-closed"),
]

#: Checks that read repository state (git history, untracked files) rather than package content.
#: In a temporary tree they cannot be evaluated meaningfully, and a probe never weakens
#: containment, so their verdict is DISCARDED. Counting them would make every probe "detected" by
#: an artefact of the harness - precisely the false credibility this fixture exists to prevent.
GIT_DEPENDENT = {
    "no approved Phase 1-13 artifact is changed",
    "no Phase 14 file is changed",
    "no runtime or infrastructure artifact is added",
}


def run_validator(tree):
    """Returns (failed check names, error) with git-dependent verdicts discarded."""
    script = os.path.join(tree, "validation", VALIDATOR)
    try:
        result = subprocess.run([sys.executable, script, "--json"],
                                cwd=tree, capture_output=True, text=True, timeout=180)
    except Exception as exc:                                   # noqa: BLE001
        return None, "%s: %s" % (type(exc).__name__, exc)
    if not result.stdout.strip():
        return None, (result.stderr or "no output")[:400]
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None, (result.stdout or result.stderr)[:400]
    return ([r["name"] for r in payload["results"]
             if not r["pass"] and r["name"] not in GIT_DEPENDENT], None)


def build_tree(base, document, old, new):
    """A temporary copy of the Phase 15 package and its validator, with one weakening applied.

    The approved registry directories are symlinked so the identifier-resolution check can run
    against real approved architecture. They are never written to. `.git` is deliberately NOT
    linked: the containment checks are discarded anyway, and a probe must never be able to reach
    repository state."""
    tree = os.path.join(base, "tree")
    os.makedirs(os.path.join(tree, "validation"))
    shutil.copytree(os.path.join(REPO, "planning"), os.path.join(tree, "planning"))
    shutil.copy2(os.path.join(REPO, "validation", VALIDATOR),
                 os.path.join(tree, "validation", VALIDATOR))
    for registry in ("roles", "skills", "reviews", "decisions", "workflows"):
        os.symlink(os.path.join(REPO, registry), os.path.join(tree, registry))

    target = os.path.join(tree, document)
    with open(target, encoding="utf-8") as handle:
        body = handle.read()
    if old not in body:
        raise AssertionError("weakening text not found in %s: %r" % (document, old[:70]))
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(body.replace(old, new, 1))
    return tree


def main():
    verbose = "--verbose" in sys.argv
    as_json = "--json" in sys.argv

    baseline_failed, error = run_validator(REPO)
    if baseline_failed is None:
        print("the validator did not run on the pristine package: %s" % error)
        return 1
    if baseline_failed:
        print("the pristine package does not pass; probes would prove nothing: %s"
              % baseline_failed)
        return 1

    results = []
    for name, document, old, new, rule in PROBES:
        base = tempfile.mkdtemp(prefix="phase15-probe-")
        try:
            tree = build_tree(base, document, old, new)
            failed, error = run_validator(tree)
            if failed is None:
                results.append({"probe": name, "rule": rule, "classification": "ERROR",
                                "detail": error})
                continue
            results.append({
                "probe": name, "rule": rule,
                "classification": "DETECTED" if failed else "REDUNDANT",
                "detected_by": failed[:3],
            })
        finally:
            shutil.rmtree(base, ignore_errors=True)

    detected = [r for r in results if r["classification"] == "DETECTED"]
    redundant = [r for r in results if r["classification"] == "REDUNDANT"]
    errors = [r for r in results if r["classification"] == "ERROR"]

    if as_json:
        print(json.dumps({"total": len(results), "detected": len(detected),
                          "redundant": len(redundant), "errors": len(errors),
                          "results": results}, indent=2))
    else:
        for r in results:
            print("  %-10s %s" % (r["classification"], r["probe"]))
            if r["classification"] == "DETECTED" and verbose:
                print("             caught by: %s" % "; ".join(r["detected_by"]))
            if r["classification"] == "REDUNDANT":
                print("             NOT CAUGHT - the validator does not observe this rule")
            if r["classification"] == "ERROR":
                print("             %s" % r["detail"][:200])
        print("\n=== %d probes: %d DETECTED, %d REDUNDANT, %d ERROR ==="
              % (len(results), len(detected), len(redundant), len(errors)))

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
