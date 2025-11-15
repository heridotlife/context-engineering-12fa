# Handoffs Packet

This directory stores the temporary artefacts exchanged between GPT-5 Codex (planning) and Claude Code Sonne 4.5 (execution).

> Do not commit secrets, large binaries, or sensitive data. Treat this folder as a working area and archive finished packets to `.session-archive/` if they need to persist.

## Workflow

1. **mission.md** – User-authored brief with intent, constraints, and acceptance criteria.
2. **plan.md** – GPT-5 Codex plan and step-by-step execution guide.
3. **context_bundle.json** – Machine-readable context (files, snippets, commands).
4. **claude_prompt.txt** – Final assembled prompt payload for Claude.
5. **claude_output.md** – Claude’s structured response with actions, artefacts, and open issues.

Use the provided templates below when drafting new packets.
