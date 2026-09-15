"""Communication specialist package — committed controlled-weakening fixture.

Status: PROPOSED. Standard library only, deterministic, no network.

    python3 validation/communication_package_probes.py [--verbose] [--json]

This fixture answers a question the package validator cannot answer about itself: **is each
check load-bearing, or would the package pass anyway?** The independent review of baseline
`81623de` found six defects that the package's own self-check had reported as clean. This is the
mechanism for not being in that position silently.

Each probe names a rule, a piece of package text that carries it, and a weakening of that text.
The weakening is applied **in memory** to a temporary copy; the package validator is re-run
against the copy; the probe records whether any check failed.

Nothing on disk is edited. Classification is from EXECUTED BEHAVIOUR, never from a label:

    DETECTED   - the weakening makes at least one validator check fail.
    REDUNDANT  - the weakening changes nothing the validator observes. Recorded honestly and
                 never presented as a pass; a redundant probe is a gap in the harness, stated.

A probe whose target text is not found is an ERROR, not a skip.

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
PKG_REL = os.path.join("proposals", "communication-difficult-conversations-specialist")
VALIDATOR = "communication_package_validation.py"

#: (name, document, old_text, new_text, rule the weakening attacks)
PROBES = [
    ("the deprecated FACT label returns as an active epistemic type",
     "workflow-thread-diagnostics.md",
     "a `FACT_CLAIM` only where `EVIDENCE` bound to the record supports it, and the record stays `SOURCE` (RC-4); everything else",
     "`FACT` only where directly stated; everything else",
     "Phase 8 epistemic vocabulary"),

    ("a SOURCE-to-claim epistemic mutation is reintroduced",
     "skill-pack.md",
     "- States the pack may support deriving: `EVIDENCE` bound to a location in the record, and a\n  **new linked** `FACT_CLAIM` supported by it;",
     "- States the pack may support deriving: `SOURCE` → `FACT_CLAIM` for directly stated claims;",
     "a source is cited, never promoted"),

    ("the no-mutation rule is removed from the Role Card",
     "role-card.md",
     "**Rule RC-4 — nothing is converted; a claim is a new linked item.**",
     "**Rule RC-4 — claims are derived from the record.**",
     "a claim is a new linked item"),

    ("the review trigger loses a condition",
     "role-card.md",
     "| RC-5.2 | The draft **carries or reformulates** a substantive conclusion owned by another Role |",
     "",
     "one review trigger, four conditions"),

    ("a workflow states a narrower review trigger than RC-5",
     "workflow-refusal.md",
     "- **Mandatory at:** high and critical bands, **and at any band where an RC-5 condition holds** (`role-card.md` RC-5)",
     "- **Mandatory at:** required only where stakes are high or critical",
     "no document states a narrower trigger"),

    ("the Review Profile restates its own trigger instead of referencing RC-5",
     "review-profile-communication-strategy.md",
     "| **RC-5.2** the draft carries or reformulates another Role's substantive conclusion | Regardless of stakes |",
     "| Carrying another Role's conclusion | Only where stakes are high or critical |",
     "one review trigger, referenced not restated"),

    ("a read-only diagnosis is made to report AUTHORITY_ABSENT",
     "workflow-thread-diagnostics.md",
     "`human_gate_status: NOT_APPLICABLE` with `human_gate_reason: NO_EXTERNAL_ACT_CONTEMPLATED` —\n  **never** `AUTHORITY_ABSENT`, which would claim an authority is missing where none is required\n  (DC-7, DC-7a)",
     "diagnostic records `human_gate_status: AUTHORITY_ABSENT` because no Decision Right resolves",
     "no external act, no gate"),

    ("NOT_APPLICABLE is allowed to travel to a later workflow",
     "conversation-diagnostics-contract.md",
     "**Rule DC-7a — `NOT_APPLICABLE` never travels.**",
     "**Rule DC-7a — `NOT_APPLICABLE` is inherited by any workflow the diagnostic feeds.**",
     "a later workflow resolves its own gate"),

    ("the diagnostic filter namespace loses a factor",
     "conversation-diagnostics-contract.md",
     '"defensiveness": 0, "control": 0, "relevance": 0, "escalation": 0, "next_step": 0',
     '"defensiveness": 0, "control": 0, "relevance": 0, "escalation": 0',
     "the filter has one field set"),

    ("the diagnostic filter namespace invents a factor",
     "conversation-diagnostics-contract.md",
     '"goal": 0, "emotion": 0, "clarity": 0, "brevity": 0, "boundary": 0,',
     '"goal": 0, "emotion": 0, "clarity": 0, "brevity": 0, "boundary": 0, "tone": 0,',
     "the diagnostic invents no competing rubric"),

    ("the risk namespace reuses a filter factor name",
     "conversation-diagnostics-contract.md",
     '  "legal_sensitivity": 0,\n  "reputational_exposure": 0,',
     '  "legal_sensitivity": 0,\n  "clarity": 0,\n  "reputational_exposure": 0,',
     "two namespaces, no collision"),

    ("a filter score is allowed to satisfy a review",
     "communication-control-filter.md",
     "**Rule CF-9 — the filter is not a reviewer.**",
     "**Rule CF-9 — the filter score satisfies a review where it meets the threshold.**",
     "no score satisfies a review"),

    ("the routing score is allowed to select a model",
     "trigger-routing-spec.md",
     "**Rule TR-8 — the Orchestrator routes; the Router selects models.**",
     "**Rule TR-8 — the score selects a Model Profile directly where it is high.**",
     "routing never selects a model"),

    ("TA-7 is again assumed outside the approved Right because it is private",
     "decision-right-gap-analysis.md",
     "Four elements, and no fifth. There is **no** element requiring the audience to be the public,",
     "A private letter is outside the Right because it is neither published nor generally available. There is an element requiring the audience to be the public,",
     "the approved subject, read as written"),

    ("the withdrawn candidate Right is presented as available again",
     "decision-right-gap-analysis.md",
     "| **TA-7** | **`decision.external_publication`** | **Carded** | **Covered.** See §5 |",
     "| **TA-7** | `decision.external_high_stakes_communication_send` | Candidate | The applicable candidate Right applies to this act |",
     "no candidate Right is available"),

    ("the Role is allowed to improve another Role's conclusion",
     "role-card.md",
     "**Rule RC-1 — phrasing may change, conclusions may not.**",
     "**Rule RC-1 — the Role may amend a supplied conclusion where the wording is unclear.**",
     "expression may change, the conclusion may not"),

    ("a compatibility alias is presented as the canonical identity",
     "README.md",
     "**Rule CP-2 — the alias is a migration aid, not an identity.**",
     "**Rule CP-2 — naming.** Fisher Mode is the product name for this capability.",
     "no alias becomes canonical"),

    ("a prompt-assembly layer is allowed to widen a higher one",
     "runtime-prompt-assembly.md",
     "| 7 | Adjacent specialist findings | conclusions supplied by owning Roles, at their versions | **No** |",
     "| 7 | Adjacent specialist findings | conclusions supplied by owning Roles, at their versions | **Yes** |",
     "narrowing only"),

    ("a candidate Skill is treated as registered",
     "skill-pack.md",
     "**Rule SP-1 — a candidate skill is not a skill.**",
     "**Rule SP-1 — candidate skills activate with the pack.**",
     "a candidate Skill is non-activatable"),

    ("the governance note decides OG-2 on its own authority",
     "governance-decision-note.md",
     "No Role is created,\nregistered or approved here.",
     "Option A is adopted here and the Role is registered by this package.",
     "the package decides no governance item for itself"),

    # ---- OG-1 applied: one canonical identifier per object -------------------------------
    ("a dotted identifier survives in an active workflow card",
     "workflow-refusal.md",
     "- Workflow ID: `workflow.communication_refusal@0.1`",
     "- Workflow ID: `workflow.communication.refusal@0.1`",
     "no dotted identifier survives"),

    ("a dotted identifier survives in the skill pack",
     "skill-pack.md",
     "- Pack ID: `skill_pack.communication_difficult_conversations@0.1`",
     "- Pack ID: `pack.communication.difficult_conversations@0.1`",
     "no dotted identifier survives"),

    ("the methodology reverts to the prompt-fixed identifier",
     "methodology-card.md",
     "Methodology ID: `method.communication_calm_direct_control@0.1`",
     "Methodology ID: `method.communication.calm_direct_control@0.1`",
     "no dotted identifier survives"),

    ("a second canonical identity is restored beside a primary ID",
     "workflow-meeting-preparation.md",
     "- Workflow ID: `workflow.communication_meeting_preparation@0.1`",
     "- Workflow ID: `workflow.communication_meeting_preparation@0.1`\n- Registry-normalised alternative (open item **OG-1**): `workflow.meeting_preparation@0.1`",
     "exactly one canonical identifier per object"),

    ("the historical identifiers stop being disclaimed",
     "README.md",
     "The IDs below were fixed by the commissioning prompt and are **not** identities. They resolve to\nnothing, may not be used in any reference, mapping, workflow, evaluation fixture or validator\nassertion, and are recorded here so that the originating text remains traceable.",
     "The IDs below were fixed by the commissioning prompt and remain valid alternatives for any\nreference, mapping, workflow, evaluation fixture or validator assertion.",
     "a historical alias never becomes a second identity"),

    # ---- OG-2 applied: a candidate Professional Delivery Role ----------------------------
    ("the Role is demoted back to a specialisation",
     "self-check.md",
     "| A new Role being created where a specialisation would do | **OG-2 — decided by a human authority**, Professional Delivery Role. See below | Decided; the Role is still a candidate and still unregistered |",
     "| A new Role being created where a specialisation would do | The capability is only a specialisation attached to existing Roles | Resolved |",
     "the capability is a candidate Professional Delivery Role"),

    ("the Role Card drops the Role Type the decision settled",
     "role-card.md",
     "- Role Type: **Professional Delivery Role** — candidate, per the OG-2 human decision above",
     "- Role Type: Specialisation attached to existing Roles",
     "the capability is a candidate Professional Delivery Role"),

    ("the candidate Role is described as registered by the decision",
     "role-card.md",
     "The decision settles the\n> *modelling question only*. It does not register the Role, approve it, activate it, make it\n> assignable, or change the approved Role universe, which remains **59 approved Roles**.",
     "The decision registers the Role and approves it for assignment, taking the approved Role\n> universe to 60.",
     "a human decision on modelling registers nothing"),

    ("the candidate mapping is presented as a Phase 4 mapping record",
     "role-skill-mapping-candidates.md",
     "> **This is a proposal surface, not a mapping record.**",
     "> **This is the authoritative Phase 4 mapping record for this Role.**",
     "no candidate mapping authorises activation"),

    ("candidate Skills are presented as activatable",
     "role-skill-mapping-candidates.md",
     "**None of these exists.** Each is a candidate under OG-5 and requires Skill Registry change control\nbefore it can be activated for any Role.",
     "Each of these is available for activation once the Role is assigned.",
     "a candidate Skill is unavailable"),

    ("the human decision record is read as approving the package",
     "self-check.md",
     "are recorded here as decided. The rest are recorded, not resolved: each requires a governance\ndecision this package must not make for itself.",
     "are recorded here as decided, and the human decision therefore approves the package and\nactivates the capability.",
     "the human decision record approves only OG-1 and OG-2"),

    # ---- V1 blocker closures, each attacked in a second location -------------------------
    ("the Review Profile restores the public/otherwise Right split",
     "review-profile-communication-strategy.md",
     "That resolution does not branch on publicity: **any release\nof a content item outside the entity under the entity's name resolves\n`decision.external_publication`**",
     "In practice that is `decision.external_publication` for public content, and the applicable\nsubmission, disclosure, transmission or commitment Right otherwise",
     "external release never branches on publicity"),

    ("the diagnostic workflow drops its review obligation again",
     "workflow-thread-diagnostics.md",
     "**Rule TD-2 — producing nothing transmissible removes the gate, not the review.**",
     "**Rule TD-2 — no review is required because nothing is transmissible.**",
     "RC-5 decides review applicability, not transmission"),

    ("the non-response branch skips the required-review stage again",
     "workflow-difficult-interaction-response.md",
     "**S10 is never skipped by this branch.**",
     "S6–S10 are skipped by this branch.",
     "no branch skips a review RC-5 triggered"),

    ("a Decision Right is allowed to cure an unsatisfied review again",
     "workflow-formal-escalation.md",
     "**None may support\na `COMPLETE` or `COMPLETE_WITH_OPEN_ITEMS` exit.**",
     "None may support a `COMPLETE` or `COMPLETE_WITH_OPEN_ITEMS` exit unless a named external\nhuman Decision Right permits progression with the unsatisfied review left open.",
     "authority never cures review satisfaction"),

    ("the diagnostic serializes the display labels as JSON keys again",
     "conversation-diagnostics-contract.md",
     '    "goal": 0, "emotion": 0, "clarity": 0, "brevity": 0, "boundary": 0,\n    "defensiveness": 0, "control": 0, "relevance": 0, "escalation": 0, "next_step": 0',
     '    "GOAL": 0, "EMOTION": 0, "CLARITY": 0, "BREVITY": 0, "BOUNDARY": 0,\n    "DEFENSIVENESS": 0, "CONTROL": 0, "RELEVANCE": 0, "ESCALATION": 0, "NEXT_STEP": 0',
     "the two serialized schemas are exactly identical"),

    ("the two derived blocks are allowed to disagree",
     "conversation-diagnostics-contract.md",
     '    "boundary_strength_score": 0, "defensiveness_risk": 0, "escalation_risk": 0,\n    "conversational_control_score": 0',
     '    "boundary_strength_score": 0, "defensiveness_risk": 0, "escalation_risk": 0',
     "the derived objects agree exactly"),

    ("a package artifact is promoted out of PROPOSED",
     "self-check.md",
     "Status: `PROPOSED`",
     "Status: `APPROVED`",
     "every artifact remains PROPOSED"),
]

#: Checks that read repository state (git history, untracked files) rather than package content.
#: In a temporary tree they cannot be evaluated meaningfully, and a probe never weakens
#: containment, so their verdict is DISCARDED. Counting them would make every probe "detected"
#: by an artefact of the harness - the false credibility this fixture exists to prevent.
GIT_DEPENDENT = {
    "no approved Phase 1-13 artifact is changed",
    "no Phase 14 file is changed",
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
    """A temporary copy of the package and its validator, with one weakening applied.

    The real `decisions/` tree is symlinked read-only so the validator can resolve approved
    Decision Right identifiers. `.git` is deliberately NOT linked: the containment checks are
    discarded anyway, and a probe must never be able to touch repository state."""
    tree = os.path.join(base, "tree")
    os.makedirs(os.path.join(tree, "validation"))
    os.makedirs(os.path.join(tree, os.path.dirname(PKG_REL)))
    shutil.copytree(os.path.join(REPO, PKG_REL), os.path.join(tree, PKG_REL))
    shutil.copy2(os.path.join(REPO, "validation", VALIDATOR),
                 os.path.join(tree, "validation", VALIDATOR))
    os.symlink(os.path.join(REPO, "decisions"), os.path.join(tree, "decisions"))

    target = os.path.join(tree, PKG_REL, document)
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
        base = tempfile.mkdtemp(prefix="commpkg-probe-")
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
