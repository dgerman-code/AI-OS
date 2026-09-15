# OpenAI ChatGPT — Mode A Adapter

Start with `AI_OS_ENTRYPOINT.md`, then read `ai-os.yaml`.

Repository governance overrides this adapter. This file adds no provider-specific Role, Workflow, Skill, Review Profile or Decision Right semantics.

If the ChatGPT environment available to you can access the GitHub repository, use that repository access to read the exact ref/commit supplied by the human. If write access is available and explicitly authorized, limit changes to the requested branch/scope. If repository access is unavailable, state that limitation rather than pretending to have read AI-OS.

Do not treat ChatGPT memory, project context or conversation history as canonical AI-OS state. Return governed work using `contracts/ai-result-envelope.schema.json`.
