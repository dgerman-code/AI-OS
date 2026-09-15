# Anthropic Claude — Mode A Adapter

Start with `AI_OS_ENTRYPOINT.md`, then read `ai-os.yaml`.

Repository governance overrides this adapter. This file adds no provider-specific Role, Workflow, Skill, Review Profile or Decision Right semantics.

If the Claude environment available to you can read this GitHub repository, use that capability to inspect the supplied ref/commit. If it can write and the human explicitly authorizes changes, keep them within the requested branch/scope. If GitHub access is not available, say so and do not invent repository state.

Do not treat Claude project memory, conversation context or generated summaries as canonical AI-OS state. Return governed work using `contracts/ai-result-envelope.schema.json`.
