# Google Gemini — Mode A Adapter

Start with `AI_OS_ENTRYPOINT.md`, then read `ai-os.yaml`.

Repository governance overrides this adapter. This file adds no provider-specific Role, Workflow, Skill, Review Profile or Decision Right semantics.

If the Gemini environment available to you can read this GitHub repository, use that capability to inspect the exact ref/commit supplied by the human. If write access is available and explicitly authorized, keep edits within the requested branch/scope. If repository access is unavailable, state that limitation and do not invent repository state.

Do not treat Gemini conversation state, workspace memory or generated summaries as canonical AI-OS state. Return governed work using `contracts/ai-result-envelope.schema.json`.
