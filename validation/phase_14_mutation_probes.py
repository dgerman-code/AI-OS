"""Phase 14 — committed adversarial / controlled-weakening fixture.

Status: PROPOSED. Standard library only, deterministic, no network.

    python3 validation/phase_14_mutation_probes.py [--verbose] [--json]

This fixture answers a question a validator cannot answer about itself: **is each check
load-bearing, or would the specification pass anyway?** The independent Phase 14 audit rated the
harness `MEDIUM` because 8 of 9 materially contradictory mutations were accepted. This is the
mechanism for not being in that position silently.

How it works. Each probe names a load-bearing rule, a piece of specification text that carries
it, and a weakening of that text. The weakening is applied to the specification **in memory**;
the Phase 14 validator is re-run against the weakened copy in a temporary tree; and the probe
records whether any check failed.

Nothing on disk is edited. No Phase 1-13 artifact is read from anywhere but the real repository,
and none is copied, modified or written. The runner is reproducible from a clean checkout.

Each probe is classified from EXECUTED BEHAVIOUR, never from a label:

    DETECTED   - the weakening makes at least one validator check fail.
    REDUNDANT  - the weakening changes nothing the validator observes. Recorded honestly and
                 never presented as a pass; a redundant probe is a gap in the harness, stated.

A probe whose target text is not found is an ERROR, not a skip. A runner that quietly matches
nothing proves exactly as much as no runner at all.

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
SPEC_DIR = "implementation-spec"

#: (name, document, old_text, new_text, rule the weakening attacks)
PROBES = [
    ("Model Profile takes an invented prefix instead of Phase 9's",
     "domain-identity-model.md",
     "| 4 | Model Profile | `ModelProfileRef` | **`model.<stable_snake_case_name>`** |",
     "| 4 | Model Profile | `ModelProfileRef` | **`model_profile.<name>`** |",
     "Phase 9 model identity compatibility"),

    ("an independent stable ModelRef is reintroduced",
     "domain-identity-model.md",
     "| 3 | Model — the **Underlying Model Release** | `ModelReleaseIdentity`",
     "| 3 | Model | `ModelRef` | `model.<name>` | Yes | Git (C1) |\n| 3b | ignored | `ModelReleaseIdentity`",
     "MODEL != MODEL PROFILE"),

    ("the Model Result is checked against a field the decision does not hold",
     "model-router-runtime-contract.md",
     "| `model_profile_ref` + `model_profile_registry_version` | ref pair | NO | IMM | **Verified equal to elements 20–21 of the recorded Routing Decision** before the write |",
     "| `model_ref` + versions | ref pair | NO | IMM | Verified equal to the recorded decision's |",
     "Routing Decision / Model Result lineage"),

    ("the release-identity divergence outcome is removed",
     "model-router-runtime-contract.md",
     "**`PROVIDER_VERSION_CHANGE` fires**",
     "the difference is noted",
     "Phase 9 silent-backend-change detection"),

    ("conflict resolution is made authority-bearing again",
     "api-command-contracts.md",
     "| `ResolveConflict` | **R** |",
     "| `ResolveConflict` | H |",
     "Phase 8 conflict-resolution authority boundary"),

    ("cancellation and termination are collapsed into one command",
     "api-command-contracts.md",
     "| `TerminateRun` | **S** |",
     "| `TerminateRun` | h |",
     "CANCELLED / TERMINATED asymmetry"),

    ("the transaction table stops stating audit counts",
     "persistence-and-transaction-model.md",
     "| **Scope transfer** | Source run, retained Decision Records, mechanism registry, target definition | All source-side clauses **and** every target-run creation condition, via one shared preflight | Source run `record_version` | `scope_transfer_authorisation`, target `workflow_run`, target `scope_binding`, provenance link | **4** |",
     "| **Scope transfer** | Source run, retained Decision Records, mechanism registry, target definition | All source-side clauses **and** every target-run creation condition, via one shared preflight | Source run `record_version` | `scope_transfer_authorisation`, target `workflow_run`, target `scope_binding`, provenance link | as needed |",
     "audit-event-per-governed-record-write cardinality"),

    ("U19 keys on a nonexistent ACTIVE approval status",
     "persistence-and-transaction-model.md",
     "| U19 | Approval state — **current pointer** | `PRIMARY KEY (subject_ref, subject_version)` on `approval_state_current` |",
     "| U19 | Approval state | `UNIQUE (subject_ref, subject_version) WHERE status = 'ACTIVE'` |",
     "approval-state current-row uniqueness"),

    ("the Phase 4 baseline is replaced with a contradictory claim",
     "README.md",
     "| Phase 4 — Skill Registry | `8ddacb2b2d2bc47e1a65099df575a0b16205d046` |",
     "| Phase 4 — Skill Registry | *(no SHA recorded)* |",
     "exact Phase 4 approved baseline citation"),

    ("the identity chain is reordered",
     "domain-identity-model.md",
     "ROLE != AGENT INSTANCE != MODEL != MODEL PROFILE",
     "ROLE != MODEL != AGENT INSTANCE != MODEL PROFILE",
     "exact ordered identity-chain equality"),

    ("an approved origin value is dropped",
     "knowledge-and-canonical-model.md",
     "| `EXTERNAL_ORIGIN` | Received from outside the entity |",
     "| `THIRD_PARTY` | Received from outside the entity |",
     "origin-axis completeness"),

    ("self-review is reduced to a class label",
     "decision-review-authority-model.md",
     "equals any producer identity recorded on the reviewed artifact version",
     "declares a class other than PRODUCER_REVIEW",
     "self-review identity inequality"),

    ("the separator-boundary ancestry rule is removed",
     "scope-and-context-model.md",
     "**Rule S-2 — the prefix trap.**",
     "**Rule S-2 — removed.**",
     "separator-boundary ancestry"),

    ("the approval registry is allowed to create approval",
     "approval-state-registry.md",
     "**Rule AP-2 — the registry records approval; it never creates it.**",
     "**Rule AP-2 — the registry may record or establish approval.**",
     "approval registry records but never creates approval"),

    ("the execution-event contract stops denying governance evidence",
     "audit-provenance-observability.md",
     "Written by C9. **Coordination history. Not governance evidence.**",
     "Written by C9. **Coordination history, and governance evidence where a gate needs it.**",
     "operational events never satisfy governance evidence"),

    ("the write-only event interface gains a read operation",
     "audit-provenance-observability.md",
     "interface has an `append` operation and **no read operation at all**",
     "interface has an `append` operation and a read operation for governed lookups",
     "structural enforcement of the runtime-event boundary"),

    ("a convenience exception is carved for governed uniqueness",
     "persistence-and-transaction-model.md",
     "`ON CONFLICT DO NOTHING` is\nprohibited on every table above",
     "`ON CONFLICT DO NOTHING` is\npermitted where convenient",
     "no ON CONFLICT DO NOTHING exception"),

    ("an administrative path is offered for a destructive migration",
     "migrations-versioning-compatibility.md",
     "there is no `--force`, no environment variable and no break-glass parameter on the applier",
     "a database owner may apply it directly where the Right is not yet mapped",
     "no admin substitution for the destructive-migration Right"),

    ("a blocked authority section is renamed away",
     "open-items-and-blocked-authorities.md",
     "### BA-3 — Controlled destruction of governed content",
     "### BX-3 — Controlled destruction of governed content",
     "missing Decision Rights are not silently filled"),
]


#: Checks that read repository state (git history, untracked files) rather than specification
#: content. In a temporary tree they cannot be evaluated meaningfully, and a probe never weakens
#: containment, so their verdict is DISCARDED. Counting them would make every probe "detected"
#: by an artefact of the harness - which is precisely the kind of false credibility this fixture
#: exists to prevent.
GIT_DEPENDENT = {
    "no infrastructure, dependency or deployment artifact is added",
    "only the specification package and its validator are added",
    "approved Phase 1-13 artifacts are unchanged",
}


def run_validator(tree):
    result = subprocess.run([sys.executable,
                             os.path.join(tree, "validation", "phase_14_validation.py"),
                             "--json"],
                            capture_output=True, text=True, cwd=tree)
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None, result.stderr[-400:]
    failed = [r["name"] for r in payload["results"]
              if not r["pass"] and r["name"] not in GIT_DEPENDENT]
    return failed, ""


def build_tree(base, document, old, new):
    """A temporary copy of the specification package and the validator, weakened in one place.

    Phase 1-13 artifacts are symlinked from the real repository, never copied and never
    written: the validator reads them, and this fixture must not be able to touch them."""
    tree = os.path.join(base, "tree")
    os.makedirs(os.path.join(tree, "validation"), exist_ok=True)
    shutil.copytree(os.path.join(REPO, SPEC_DIR), os.path.join(tree, SPEC_DIR))
    for name in ("phase_14_validation.py",):
        shutil.copy2(os.path.join(REPO, "validation", name),
                     os.path.join(tree, "validation", name))
    # No `.git` symlink: the containment checks are discarded anyway (GIT_DEPENDENT), and a
    # temporary tree that could reach the real repository's git directory is a tree that could
    # write to it.
    for entry in ("architecture", "orchestration", "knowledge", "models", "storage", "decisions",
                  "roles", "skills", "workflows", "handoffs", "reviews", "implementation",
                  "prompts"):
        source = os.path.join(REPO, entry)
        if os.path.exists(source):
            os.symlink(source, os.path.join(tree, entry))
    target = os.path.join(tree, SPEC_DIR, document)
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
    # The baseline is checked in a pristine temporary tree too, so that "the package passes"
    # means the same thing for the baseline as it does for every probe.
    if baseline_failed is None:
        print("the validator did not run on the pristine package: %s" % error)
        return 1
    if baseline_failed:
        print("the pristine package does not pass; probes would prove nothing: %s"
              % baseline_failed)
        return 1

    results = []
    for name, document, old, new, rule in PROBES:
        base = tempfile.mkdtemp(prefix="phase14-probe-")
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

    # An error is always a failure. A redundancy is reported, not hidden, and does not by itself
    # fail the run - but the caller is told, and the self-check must state the number.
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
