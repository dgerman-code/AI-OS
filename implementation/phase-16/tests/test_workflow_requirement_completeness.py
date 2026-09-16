"""Regression tests for Astra-6 F1: MATCH cannot omit Workflow requirements."""

import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import registries
from domain import (
    BlockReason, Criticality, ExecutionMode, PlannerOutput, PlannerState, WorkMode,
)
from preflight import run_preflight
from workflow_contract import workflow_contract


class TestWorkflowRequirementCompleteness(unittest.TestCase):

    def _empty_match(self, workflow_id):
        version = registries.approved_workflows()[workflow_id]
        return PlannerOutput(
            request_id="request.workflow-omission",
            request_text="Run the selected Workflow.",
            intent_id="intent.workflow-omission",
            scope_ref="scope.project.alpha",
            scope_ancestry=("scope.org.root", "scope.project.alpha"),
            objective="Test Workflow completeness",
            deliverables=("governed work",),
            primary_work_mode=WorkMode.ANALYSIS,
            secondary_work_modes=(),
            criticality=Criticality.ROUTINE,
            execution_mode=ExecutionMode.MATCH,
            workflow_ref="%s@%s" % (workflow_id, version),
            role_requirements=(),
            skill_requirements=(),
            review_requirements=(),
            decision_requirements=(),
            evidence_requirements=(),
        )

    def test_project_readiness_empty_requirements_fail_closed(self):
        workflow_id = "workflow.project_development_readiness"
        self.assertIn(workflow_id, registries.approved_workflows())
        contract = workflow_contract(workflow_id)
        self.assertTrue(contract.mandatory_roles)
        self.assertTrue(contract.required_evidence)

        result = run_preflight(self._empty_match(workflow_id))
        self.assertIs(result.state, PlannerState.BLOCKED)
        self.assertIsNone(result.basis)
        self.assertIn(BlockReason.BASIS_NOT_EXECUTABLE, result.reasons)
        self.assertTrue(any("omits mandatory Workflow Role" in item for item in result.detail))

    def test_valid_workflow_identity_is_not_requirement_completeness(self):
        workflow_id = "workflow.project_development_readiness"
        result = run_preflight(self._empty_match(workflow_id))
        self.assertFalse(result.executable)
        self.assertTrue(any(
            reason in result.reasons
            for reason in (
                BlockReason.BASIS_NOT_EXECUTABLE,
                BlockReason.REVIEW_UNRESOLVED,
                BlockReason.NO_APPLICABLE_DECISION_RIGHT,
                BlockReason.EVIDENCE_UNSATISFIED,
                BlockReason.UNREGISTERED_CAPABILITY,
            )
        ))


if __name__ == "__main__":
    unittest.main()
