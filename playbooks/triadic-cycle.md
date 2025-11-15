# Triadic Agentic Cycle Playbook

> Operational guide for running the "user ↔ GPT-5 Codex ↔ Claude Code Sonne 4.5" collaboration loop inside the 12 Factor Agent stack.

---

## Purpose

This playbook turns the triadic concept into a repeatable workflow that fits the existing context-engineering conventions. Use it whenever execution duties are split across three roles:

- **User (Mission Owner)** – defines intent, constraints, and acceptance criteria.
- **GPT-5 Codex (Context Planner)** – decomposes the task, assembles context packets, and prepares the execution brief.
- **Claude Code Sonne 4.5 (Execution Agent)** – performs coding / tool actions based on the prepared packet and returns results for review.

The loop is intentionally lightweight so it can run inside a single repository, a shared SESSION_LOG, or an automated supervisor.

---

## High-Level Cycle

| Stage | Owner | Required Inputs | Outputs | Definition of Done |
|-------|-------|-----------------|---------|--------------------|
| **1. Brief** | User | Problem statement, constraints, success criteria | `mission.md` or SESSION_LOG Task section | All stakeholders agree on scope and blockers |
| **2. Plan** | GPT-5 Codex | Approved brief, current repo context, latest state checks | `plan.md`, `context_bundle.json`, Claude prompt draft | Tasks sequenced, dependencies noted, guardrails captured |
| **3. Execute** | Claude Code Sonne 4.5 | Plan packet + execution prompt + relevant files | Code changes, command output, interim notes | All planned steps attempted, deviations documented |
| **4. Review** | GPT-5 Codex (with User) | Execution artefacts, SESSION_LOG updates | Acceptance decision, follow-up tasks, retrospectives | Changes validated, next cycle (if any) queued |

---

## Stage Checklists

### 1. Brief (User)
- [ ] Clarify **what** needs to happen and **why it matters**.
- [ ] State non-negotiable constraints (tools, deadlines, coding standards).
- [ ] Flag freshness needs ("requires latest version", "needs web search").
- [ ] Confirm artefacts to produce (PR, report, dataset, etc.).
- [ ] Log the brief in `SESSION_LOG.md` under **Task**.

### 2. Plan (GPT-5 Codex)
- [ ] Run `context_health_check()` before stepping through large context.
- [ ] Identify persona alignment and note it in SESSION_LOG.
- [ ] Create a numbered plan with explicit owners (Claude vs User follow-up).
- [ ] Prepare `context_bundle.json` or equivalent (file paths, snippets, command history, references).
- [ ] Draft the Claude executor prompt using `prompts/claude/triad-executor.md` as the schema.
- [ ] Record plan + handoff artefacts under **Plan** and **State Checkpoints** in SESSION_LOG.

### 3. Execute (Claude Code Sonne 4.5)
- [ ] Receive the handoff packet (plan, context bundle, guardrails).
- [ ] Follow the plan sequentially, acknowledging deviations immediately.
- [ ] Capture tool outputs, errors, and decisions inline with the response template.
- [ ] Send a structured report back (summary, detailed log, diff or code blocks, open questions).
- [ ] Update the SESSION_LOG **Tool Calls** and **Token Usage** sections if automated; otherwise attach Claude’s transcript.

### 4. Review (GPT-5 Codex + User)
- [ ] Validate outputs against acceptance criteria and repository standards.
- [ ] Run tests / linting as required and note results.
- [ ] Decide: **Accept**, **Request revisions**, or **Escalate**.
- [ ] Summarize learnings / blockers in SESSION_LOG **Notes**.
- [ ] If more work is needed, start a fresh cycle with a refined brief.

---

## Artefact Naming

The workflow intentionally keeps artefacts simple:

- `/handoffs/mission.md` – optional archive of the brief.
- `/handoffs/plan.md` – Codex plan (mirrors SESSION_LOG plan section).
- `/handoffs/context_bundle.json` – machine-readable context (paths, config, environment).
- `/handoffs/claude_prompt.txt` – final prompt supplied to Claude.
- `/handoffs/claude_output.md` – Claude’s raw output for traceability.

*Create the `handoffs/` folder on demand; do not commit secrets or oversized files.*

---

## When to Use vs. Skip

Use the triadic cycle when:
- Execution requires a separate model (e.g., Claude) for tooling or licensing reasons.
- Tasks span multiple toolchains where Codex plans and Claude acts (e.g., Codex lacks external access).
- You want auditable handoffs for compliance, safety, or review.

Skip or simplify when:
- The task is trivial and can be handled entirely by one agent.
- There is no need for a second model (Claude) because GPT-5 Codex has sufficient capabilities.
- Context size is tiny and the overhead outweighs the benefits.

---

## Tips

- Reuse past handoff packets to accelerate recurring tasks.
- Keep context bundles lean (< 8 KB) to avoid Claude prompt bloat.
- If Claude identifies missing information, feed the updates back into the plan and rerun Stage 3.
- Archive completed packets in `.session-archive/` for audit trails.
- Consider automating the handoff creation with a small script once the process feels stable.
