# Google Gemini — Mode A Adapter

Start with `AI_OS_ENTRYPOINT.md`, then read `ai-os.yaml`. In interactive chat, follow `docs/CONVERSATIONAL_OPERATION_MODEL.md`.

Repository governance overrides this adapter. This file adds no provider-specific Role, Workflow, Skill, Review Profile or Decision Right semantics.

If the Gemini environment available to you can read this GitHub repository, use that capability to inspect the exact ref/commit supplied by the human. If write access is available and explicitly authorized, keep edits within the requested branch/scope. If repository access is unavailable, state that limitation and do not invent repository state.

Use FULL RESOLUTION for a new project/fresh baseline/material objective or evidence change; use FAST TASK RESOLUTION for ordinary follow-up work. Re-resolve the minimum sufficient Role set for each substantive request and treat Gemini conversation/workspace memory as non-canonical working context only.

Apply Workflow admissibility before reporting MATCH. Do not use `MATCH + execution_eligible=false` as a substitute for failed admissibility and do not silently modify a matched Workflow.

Default user-facing output to NORMAL MODE: direct answer, material recommendation, one best next step, and at most one targeted clarification question. Do not normally show raw JSON, SHA/ref, internal IDs or governance diagnostics. Use EXPLAIN or AUDIT mode only when requested.

Keep governed result structure compatible with `contracts/ai-result-envelope.schema.json`; raw envelope JSON is not a default user-facing artifact.
