"""B5 regression: three outcomes of the assurance layer must stay distinct.

    expected refusal exception   -> the refusal check passes semantically
    genuine semantic mismatch    -> validator status FAIL
    unexpected RuntimeError      -> validator status RUNNER_ERROR, harness outcome RUNNER_ERROR

The third case is the defect the final independent review found. `refuses()` ended in a bare
`except Exception -> (False, "wrong exception ...")`, so a `RuntimeError` raised by the call it
was wrapping came back as an ordinary failed check: the validator reported `status: FAIL`, exit
1, and the mutation harness counted a crash as a DETECTION. These tests drive the real validator
and the real mutation classifier against throwaway copies, so a regression shows up as the wrong
status rather than as prose that stopped being true.

Nothing here modifies the working tree. Every mutation is applied inside a temporary directory.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
IMPL = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(IMPL))
sys.path.insert(0, IMPL)
sys.path.insert(0, os.path.join(REPO, "validation"))

from domain import ActivationError, GovernanceError                       # noqa: E402

#: The same set the mutation harness copies. Anything omitted makes the fixture lie rather than
#: fail loudly, so it is imported from the harness instead of restated.
import phase_16_mutation_probes as harness                                # noqa: E402
import _planner_activation_validator_core as core                         # noqa: E402

RUNTIME_FAULT = 'raise RuntimeError("b5 regression: deliberate unexpected fault")'


def build_copy(tmp):
    root = os.path.join(tmp, "repo")
    os.makedirs(root)
    for rel in harness.COPY_PATHS:
        shutil.copytree(os.path.join(REPO, rel), os.path.join(root, rel),
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return root


def run_validator(root):
    env = dict(os.environ)
    env["PHASE_16_REPO_ROOT"] = root
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        [sys.executable, os.path.join(REPO, "validation", "phase_16_validation.py"), "--json"],
        env=env, capture_output=True, text=True, cwd=root)
    try:
        return json.loads(proc.stdout), proc.returncode
    except ValueError:
        return None, proc.returncode


def edit(root, relative, old, new):
    path = os.path.join(root, relative)
    with open(path, encoding="utf-8") as handle:
        body = handle.read()
    assert old in body, "fixture anchor not found in %s" % relative
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(body.replace(old, new, 1))


class RefusalHelperContract(unittest.TestCase):
    """Case 1 and the helper's own three-way behaviour, in-process."""

    def test_an_expected_refusal_exception_is_semantic_success(self):
        def raises_governance():
            raise GovernanceError("a rule refused")

        ok, evidence = core.refuses(raises_governance, GovernanceError)
        self.assertTrue(ok)
        self.assertIn("GovernanceError", evidence)

    def test_a_returned_value_instead_of_a_refusal_is_semantic_failure(self):
        ok, evidence = core.refuses(lambda: "no refusal at all", GovernanceError)
        self.assertFalse(ok)
        self.assertIn("returned instead of refusing", evidence)

    def test_a_wrong_but_ordinary_domain_exception_stays_a_semantic_failure(self):
        def raises_activation():
            raise ActivationError("a different refusal than the one asserted")

        ok, evidence = core.refuses(raises_activation, GovernanceError)
        self.assertFalse(ok, "an implementation regression must not hide as infrastructure")
        self.assertIn("wrong exception ActivationError", evidence)

    def test_an_unexpected_runtime_fault_escapes_rather_than_being_absorbed(self):
        def raises_runtime():
            raise RuntimeError("b5 regression: deliberate unexpected fault")

        with self.assertRaises(RuntimeError):
            core.refuses(raises_runtime, GovernanceError)

    def test_an_infrastructure_exception_the_caller_asserts_is_not_infrastructure(self):
        """A check may legitimately assert that an OSError is raised, and that must work."""
        def raises_os_error():
            raise OSError("an expected refusal for this check")

        ok, _evidence = core.refuses(raises_os_error, OSError)
        self.assertTrue(ok)
        self.assertFalse(core.is_infrastructure_fault(OSError("x"), (OSError,)))
        self.assertTrue(core.is_infrastructure_fault(OSError("x"), (GovernanceError,)))


class ValidatorClassification(unittest.TestCase):
    """Cases 2 and 3, driving the real validator against throwaway copies."""

    def test_a_pristine_copy_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            report, code = run_validator(build_copy(tmp))
        self.assertIsNotNone(report, "the pristine copy produced no JSON")
        self.assertEqual(report["status"], "PASS", report.get("failed"))
        self.assertEqual(report["passed"], report["total"])
        self.assertEqual(report["runner_errors"], [])
        self.assertEqual(code, 0)

    def test_a_genuine_semantic_mismatch_is_FAIL_not_RUNNER_ERROR(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = build_copy(tmp)
            # An ordinary rule removed: the basis stops refusing to exercise a Decision Right.
            # The refusal check sees a RETURN where it asserted a raise, which is a finding.
            edit(root, os.path.join("implementation", "phase-16", "domain.py"),
                 "    def exercise(self, *_args, **_kwargs):\n        raise GovernanceError(",
                 "    def exercise(self, *_args, **_kwargs):\n        return None\n"
                 "        raise GovernanceError(")
            report, code = run_validator(root)
        self.assertIsNotNone(report)
        self.assertEqual(report["status"], "FAIL", report.get("runner_errors"))
        self.assertEqual(report["runner_errors"], [])
        self.assertLess(report["passed"], report["total"])
        self.assertEqual(code, 1)

    def test_a_runtime_fault_through_the_refusal_helper_is_RUNNER_ERROR(self):
        """The exact attack the independent review reproduced."""
        with tempfile.TemporaryDirectory() as tmp:
            root = build_copy(tmp)
            # `exercise()` is reached ONLY through `refuses()`, so this fault can only arrive
            # by the helper path. Before the fix it came back as status FAIL, exit 1.
            edit(root, os.path.join("implementation", "phase-16", "domain.py"),
                 "    def exercise(self, *_args, **_kwargs):\n        raise GovernanceError(",
                 "    def exercise(self, *_args, **_kwargs):\n        %s\n"
                 "        raise GovernanceError(" % RUNTIME_FAULT)
            report, code = run_validator(root)
            self.assertIsNotNone(report)
            self.assertEqual(report["status"], "RUNNER_ERROR", report.get("failed"))
            self.assertTrue(report["runner_errors"])
            self.assertIn("RuntimeError", report["runner_errors"][0])
            self.assertEqual(code, 2)

            # And the mutation classifier must agree, because that is where the miscount was.
            outcome, detail = harness.classify(root)
            self.assertEqual(outcome, harness.RUNNER_ERROR, detail)
            self.assertNotEqual(outcome, harness.DETECTED)

    def test_the_harness_registers_a_refusal_helper_runtime_probe_expecting_RUNNER_ERROR(self):
        matching = [p for p in harness.PROBES
                    if "refusal helper" in p["name"] and p["expect"] == harness.RUNNER_ERROR]
        self.assertTrue(matching, "no probe asserts the refusal-helper runtime path")
        # The two earlier runtime paths are retained, not replaced by this one.
        runtime_probes = [p for p in harness.PROBES if p["expect"] == harness.RUNNER_ERROR]
        self.assertGreaterEqual(len(runtime_probes), 3, [p["name"] for p in runtime_probes])


if __name__ == "__main__":                                       # pragma: no cover
    unittest.main()
