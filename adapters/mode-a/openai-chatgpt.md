# OpenAI ChatGPT — Mode A Adapter

Start with `AI_OS_ENTRYPOINT.md`, then read `ai-os.yaml`. In interactive chat, follow `docs/CONVERSATIONAL_OPERATION_MODEL.md`.

Repository governance overrides this adapter. This file adds no provider-specific Role, Workflow, Skill, Review Profile or Decision Right semantics.

If the ChatGPT environment available to you can access the GitHub repository, use that repository access to read the exact ref/commit supplied by the human. If write access is available and explicitly authorized, limit changes to the requested branch/scope. If repository access is unavailable, state that limitation rather than pretending to have read AI-OS.

For a new project, fresh baseline or material objective/evidence change, perform FULL RESOLUTION. For ordinary follow-up questions, use FAST TASK RESOLUTION and re-resolve only the minimum sufficient Role set for the current task.

If the conversation detours to an unrelated topic and later clearly returns to an established project/workstream, resume that working context without forcing the human to repeat the project history. Treat ChatGPT memory/project context/conversation history as non-canonical working context only.

Before reporting a Workflow MATCH, apply the admissibility rules. Do not report `MATCH + execution_eligible=false` merely because a Workflow is the best semantic fit. Do not silently add Roles/stages/reviews/gates to a matched Workflow; re-resolve or use governed COMPOSE where eligible.

Default to NORMAL MODE: provide the useful answer, material recommendation, one best next step, and at most one targeted clarification question. Do not normally show repository-reading narration, exact SHA/ref, internal Role IDs, Skill mechanics, Workflow diagnostics, Review/Decision Right mechanics or raw result-envelope JSON.

Use EXPLAIN MODE when the human asks why, which specialists were used or how AI-OS reached the answer. Use AUDIT MODE when the human explicitly asks for provenance, exact SHA/ref, governance/validation detail or the structured result envelope.

Keep governed result structure compatible with `contracts/ai-result-envelope.schema.json`, but do not display the raw envelope by default.
