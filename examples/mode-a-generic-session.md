# Mode A Generic Session Example

This example shows an external AI using AI-OS from GitHub without provider-specific governance.

## User request

> Prepare an initial investment-readiness assessment for a municipal infrastructure project and identify what is missing before it can be shown to banks or IFIs.

## External AI discovery

The AI first reads `AI_OS_ENTRYPOINT.md` and `ai-os.yaml`, then pins the repository state it actually used.

It resolves the applicable project scope and checks the repository sources for approved Roles, Workflow options, review requirements and Decision Rights. It distinguishes Skill applicability from individual Skill approval and does not treat a Skill card as execution eligibility.

If a required approval, source document or authority record is unavailable, it records that as a blocker or ambiguity rather than guessing.

## Example governed result envelope

```json
{
  "request_id": "request.example.investment-readiness-001",
  "task_id": null,
  "repository": "dgerman-code/AI-OS",
  "source_ref": "implementation/phase-17-github-mode-a",
  "source_commit_sha": null,
  "scope": "PROJECT: example municipal infrastructure project",
  "roles": [
    {
      "role_ref": "role.project_development_lead",
      "approval_state": "UNKNOWN",
      "source": "roles/master-role-universe.md"
    }
  ],
  "skill_requirements": [
    {
      "skill_ref": "skill.example_financial_assessment",
      "applicability": "UNKNOWN",
      "individual_approval": "UNKNOWN",
      "eligibility": "UNKNOWN",
      "source": null
    }
  ],
  "workflow": {
    "mode": "UNRESOLVED",
    "reference": null,
    "execution_eligible": null
  },
  "review_requirements": [],
  "decision_right_requirements": [],
  "evidence": [
    "AI_OS_ENTRYPOINT.md",
    "ai-os.yaml",
    "roles/master-role-universe.md",
    "workflows/master-workflow-universe.md"
  ],
  "assumptions": [],
  "unresolved_ambiguities": [
    "Exact commit SHA has not yet been resolved; this result is unpinned.",
    "Project evidence package has not yet been supplied.",
    "Role/Skill/workflow eligibility must be resolved from governed records before execution."
  ],
  "proposed_changes": [],
  "output_artifacts": [
    "Proposed investment-readiness gap analysis after required evidence is available"
  ],
  "authority_status": "NO_AUTHORITY_EXERCISED",
  "status": "CLARIFICATION_REQUIRED"
}
```

The important behavior is the refusal to invent approval, eligibility or authority. The AI can still explain what it needs next, but it does not silently convert its own analysis into canonical AI-OS state or a human decision.
