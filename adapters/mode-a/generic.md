# Generic Mode A Adapter

Start with `AI_OS_ENTRYPOINT.md`, then read `ai-os.yaml`.

This adapter changes no AI-OS semantics. Repository rules override this file.

If your AI environment can read GitHub, use that capability to read the repository at the supplied ref/commit. If it can also write, write only when the human task explicitly permits it and prefer a dedicated working branch.

Do not infer governance approval, authority, Skill eligibility or canonical status from this adapter or from provider memory. Return governed work using `contracts/ai-result-envelope.schema.json`.
