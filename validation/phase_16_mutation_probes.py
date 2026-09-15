"""Phase 16 — mutation probes for the planner-activation validator.

Status: PROPOSED. Standard library only, deterministic, no network.

    python3 validation/phase_16_mutation_probes.py [--verbose]

A validator that passes proves nothing on its own: it may be passing because it is not looking.
Each probe copies the Phase 16 package and its reference implementation into a throwaway
directory, breaks exactly one rule there, re-runs the validator against the copy, and expects it
to FAIL. A probe reported REDUNDANT means the validator did not notice the break, which is a
defect in the validator and not in the package.

The working tree is never mutated. Every probe runs against a copy under a temporary directory
that is removed afterwards.

This file is an ASSURANCE TOOL AND NEVER GOVERNANCE AUTHORITY.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
VALIDATOR = os.path.join(HERE, "phase_16_validation.py")

#: Copied into each throwaway root. The last three are read only by the containment checks.
COPY_PATHS = ("planner-activation", os.path.join("implementation", "phase-16"),
              "architecture", "planning", "implementation-spec")

PROBES = []


def probe(name, path, pattern, replacement, count=1):
    """Register a single-rule mutation. `path` is repo-relative; `pattern` is a regex."""
    PROBES.append({"name": name, "path": path, "pattern": pattern,
                   "replacement": replacement, "count": count})


# --------------------------------------------------------------- the twelve classes, broken

D = "domain.py"
P = "preflight.py"
H = "handoff.py"
S = "store.py"
R = "registries.py"


def impl(name):
    return os.path.join("implementation", "phase-16", name)


# C-1 COMPOSE executable without a basis
probe("a non-EXECUTABLE basis is allowed to produce a trigger", impl(H),
      r"if basis\.status is not BasisStatus\.EXECUTABLE:",
      "if False:")
probe("only the STALE status is checked, so a SUPERSEDED basis passes", impl(H),
      r"if basis\.status is not BasisStatus\.EXECUTABLE:",
      "if basis.status is BasisStatus.STALE:")

# C-2 the basis exercising authority
probe("ExecutionBasis.exercise() returns instead of refusing", impl(D),
      r'(def exercise\(self, \*_args, \*\*_kwargs\):\n\s*)raise GovernanceError\(',
      r"\1return None  # noqa\n        _unused = GovernanceError(")
probe("ExecutionBasis.satisfy_review() returns instead of refusing", impl(D),
      r'(def satisfy_review\(self, \*_args, \*\*_kwargs\):\n\s*)raise GovernanceError\(',
      r"\1return None  # noqa\n        _unused = GovernanceError(")
probe("is_approval is declared true on the basis", impl(D),
      r"is_approval: bool = False", "is_approval: bool = True")
probe("is_authority is declared true on the basis", impl(D),
      r"is_authority: bool = False", "is_authority: bool = True")
probe("a trigger declares itself an approval", impl(H),
      r"is_approval: bool = False", "is_approval: bool = True")
probe("a ReviewRequirement arrives already satisfied", impl(D),
      r"satisfied: bool = False", "satisfied: bool = True")
probe("a DecisionRequirement arrives already exercised", impl(D),
      r"exercised: bool = False", "exercised: bool = True")

# C-3 planner-created governed records
probe("preflight accepts a caller-supplied governed record", impl(P),
      r"if plan\.injected_governed_records:", "if False:")

# C-4 material change not invalidating the basis
probe("a material change leaves the live basis standing", impl(S),
      r"basis\.mark_stale\(\)", "pass")
probe("scope is dropped from the material fields, so a scope change is cosmetic", impl(D),
      r'MATERIAL_FIELDS = \(\n        "scope_ref", ', 'MATERIAL_FIELDS = (\n        ')
probe("the objective is dropped from the material fields", impl(D),
      r'"objective", "deliverables"', '"deliverables"')
probe("criticality is dropped from the material fields", impl(D),
      r'"criticality", "execution_mode"', '"execution_mode"')

# C-5 unapproved or stale Workflow under MATCH
probe("MATCH accepts any Workflow identity the planner names", impl(P),
      r"approved_workflows\(\)", "set(_ALL_STRINGS)")
probe("MATCH ignores the Workflow version", impl(P),
      r'plan\.workflow_ref\.partition\("@"\)', 'plan.workflow_ref.partition("#")')

# C-6 unregistered Role or Skill made assignable
probe("an unregistered Role is accepted for assignment", impl(P),
      r"elif role\.role_ref not in approved_roles", "elif False")
probe("an unregistered Skill is accepted for assignment", impl(P),
      r"(?m)^(\s*)if skill\.skill_ref not in ", r"\1if False and skill.skill_ref not in ")
probe("the registry view grows a write path", impl(R),
      r"(?m)\Z", "\n\ndef register_role(role_ref):\n    \"\"\"Silently widen the universe.\"\"\"\n    return role_ref\n")

# C-7 separation of duties
probe("author and final critical reviewer may be the same identity", impl(P),
      r"author_identity == reviewer_identity", "author_identity != reviewer_identity")

# C-8 clarification-required entering execution
probe("a blocking clarification no longer blocks", impl(P),
      r"if any\(c\.blocking for c in plan\.clarifications\):", "if False:")
probe("a blocking clarification issues a basis anyway", impl(P),
      r"PlannerState\.CLARIFICATION_REQUIRED, None,",
      "PlannerState.CLARIFICATION_REQUIRED, _draft_basis(plan),")

# C-9 duplicate request creating duplicate lineage
probe("a repeated trigger mints a second lineage", impl(S),
      r"if idempotency_key in self\._triggers:", "if False:")
probe("the idempotency key ignores the material planning version", impl(H),
      r'"%s\|%s\|%s" % \(plan\.scope_ref, plan\.request_id, plan\.material_digest\(\)\)',
      '"%s|%s" % (plan.scope_ref, plan.request_id)')
probe("re-issuing on unchanged inputs mints a second basis", impl(S),
      r"return previous                   # idempotent reuse", "pass  # idempotent reuse")

# C-10 Work Plan promoted to reusable Workflow
probe("a Work Plan may be rendered in the workflow identifier space", impl(D),
      r'if self\.work_plan_id\.startswith\("workflow\."\):', "if False:")
probe("a repeated pattern is emitted as APPROVED rather than PROPOSED", impl(S),
      r'"status": "PROPOSED",', '"status": "APPROVED",')
probe("a workflow candidate is declared matchable", impl(S),
      r'"is_matchable": False,', '"is_matchable": True,')
probe("the store grows a promotion path", impl(S),
      r"(?m)\Z", "\n\ndef promote_candidate(candidate):\n    candidate[\"status\"] = \"APPROVED\"\n    return candidate\n")

# C-11 caller-injected governed records in the handoff
probe("the trigger builder stops screening for governed records", impl(H),
      r"for field in FORBIDDEN_IN_TRIGGER:", "for field in ():")
probe("the forbidden list quietly loses the Review Instance", impl(H),
      r'"decision_record", "review_instance", ', '"decision_record", ')
probe("a planned spec may take work_item identity", impl(H),
      r'if not self\.spec_id\.startswith\("planned_work_item_spec\."\):', "if False:")
probe("the handoff invents its own command instead of the approved one", impl(H),
      r'command="CreateWorkflowRun",', 'command="ActivatePlanDirectly",')

# C-12 stale or mismatched scope or version lineage
probe("the builder stops comparing the basis digest to the plan", impl(H),
      r"if basis\.planning_digest != plan\.material_digest\(\):", "if False:")
probe("basis versioning reads the live basis, losing the lineage across a STALE one", impl(S),
      r"previous = self\.latest_basis\(basis\.request_id\)",
      "previous = self.live_basis(basis.request_id)")
probe("a new basis no longer records what it supersedes", impl(S),
      r"basis\.supersedes = previous\.ref", "basis.supersedes = None")
probe("the basis stops binding the implementation-spec version", impl(P),
      r"IMPLEMENTATION_SPEC_VERSION = \"phase-14@ba9e3fee\"",
      'IMPLEMENTATION_SPEC_VERSION = "unversioned"')

# --------------------------------------------------------------- prose, broken

def pkg(name):
    return os.path.join("planner-activation", name)


probe("the closure document claims PO-4 is closed outright", pkg("po-4-and-po-12-closure.md"),
      r"Neither is closed by this package alone",
      "Both obligations are closed by this package")
probe("the closure document drops its new open items", pkg("po-4-and-po-12-closure.md"),
      r"PO-16-E", "PO-16-Z")
probe("the closure document promises intake will accept", pkg("po-4-and-po-12-closure.md"),
      r"intake may accept", "intake will accept")
probe("the basis contract drops the declared false fields",
      pkg("execution-basis-contract.md"), r"is_authority", "is-authority-omitted")
probe("the README drops its unapproved banner", pkg("README.md"),
      r"\*\*Nothing in this package is approved\.\*\*", "This package is ready.")
probe("the README stops listing the self-check", pkg("README.md"),
      r"phase-16-self-check\.md", "phase-16-notes.md")
probe("a package document claims production readiness", pkg("README.md"),
      r"## 5\. Non-Runtime Statement", "## 5. This package is production-ready\n\nNon-Runtime Statement")
probe("the self-check drops its governance disclaimer", pkg("phase-16-self-check.md"),
      r"NEVER GOVERNANCE AUTHORITY", "an authoritative record")
probe("the idempotency document contradicts the store's lineage rule",
      pkg("idempotency-versioning-replay.md"), r"most recently issued", "currently live")
probe("the observability document loses the governed/operational split",
      pkg("observability-audit-provenance.md"), r"(?i)\bgoverned\b", "recorded", 0)


# --------------------------------------------------------------- runner


def build_root(tmp):
    root = os.path.join(tmp, "repo")
    os.makedirs(root)
    for rel in COPY_PATHS:
        src = os.path.join(REPO, rel)
        dst = os.path.join(root, rel)
        if os.path.isdir(src):
            shutil.copytree(src, dst,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return root


def run_validator(root):
    env = dict(os.environ)
    env["PHASE_16_REPO_ROOT"] = root
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run([sys.executable, VALIDATOR, "--json"], env=env,
                          capture_output=True, text=True)
    return proc


def main():
    verbose = "--verbose" in sys.argv

    baseline = run_validator(REPO)
    if baseline.returncode != 0:
        print("BASELINE IS NOT CLEAN - probes are meaningless until it is.")
        print(baseline.stdout[-2000:] or baseline.stderr[-2000:])
        return 2
    print("baseline: clean\n")

    caught, redundant = 0, []
    for entry in PROBES:
        with tempfile.TemporaryDirectory() as tmp:
            root = build_root(tmp)
            target = os.path.join(root, entry["path"])
            original = open(target, encoding="utf-8").read()
            mutated, n = re.subn(entry["pattern"], entry["replacement"], original,
                                 count=entry["count"], flags=re.MULTILINE)
            if n == 0:
                redundant.append((entry["name"], "PATTERN DID NOT MATCH - the probe is dead"))
                print("  DEAD       %s" % entry["name"])
                continue
            open(target, "w", encoding="utf-8").write(mutated)
            proc = run_validator(root)
            if proc.returncode != 0:
                caught += 1
                if verbose:
                    print("  CAUGHT     %s" % entry["name"])
            else:
                redundant.append((entry["name"], "validator still passed"))
                print("  REDUNDANT  %s" % entry["name"])

    total = len(PROBES)
    print("\n=== %d/%d CAUGHT ===" % (caught, total))
    if redundant:
        print("\nNot caught:")
        for name, why in redundant:
            print("  - %s (%s)" % (name, why))
    return 0 if caught == total else 1


if __name__ == "__main__":
    sys.exit(main())
