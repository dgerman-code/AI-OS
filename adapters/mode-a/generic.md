# Generic Mode A Adapter

Start with `AI_OS_ENTRYPOINT.md`, then read `ai-os.yaml`. In interactive chat, follow `docs/CONVERSATIONAL_OPERATION_MODEL.md`.

This adapter changes no AI-OS semantics. Repository rules override this file.

If your AI environment can read GitHub, use that capability to read the repository at the supplied ref/commit. If it can also write, write only when the human task explicitly permits it and prefer a dedicated working branch.

For ordinary follow-up conversation use FAST TASK RESOLUTION rather than re-running a full bootstrap. Re-resolve the minimum sufficient Role set for each substantive request, resume clear prior project context after unrelated detours, and keep conversation state non-canonical.

Apply Workflow admissibility before reporting MATCH. Do not use `MATCH + execution_eligible=false` as a substitute for failed admissibility and do not silently modify a matched Workflow.

Default user-facing output to NORMAL MODE: answer directly, give material guidance, recommend one best next step, and avoid raw JSON, SHA/ref, internal IDs and governance/debug detail unless requested. Use EXPLAIN or AUDIT mode only when the human asks for that level of detail.

Do not infer governance approval, authority, Skill eligibility or canonical status from this adapter or from provider memory. Keep governed result structure compatible with `contracts/ai-result-envelope.schema.json`; raw envelope JSON is not a default user-facing artifact.
