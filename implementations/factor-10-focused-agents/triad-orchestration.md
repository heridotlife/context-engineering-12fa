# Triad Orchestration within Factor 10: Focused Agents

This note maps the triadic workflow (User → GPT-5 Codex → Claude Code Sonne 4.5) into the Factor 10 guidance on focused agents. It shows how to keep each persona narrow while coordinating the loop.

---

## Alignment to Factor 10 Principles

- **Narrow Intent Surface** – Each agent owns a distinct slice: the user sets mission intent, Codex plans/contextualizes, Claude executes. None of them attempt to do all three at once.
- **Explicit Handoffs** – Plans and briefs are stored in reproducible artefacts (`SESSION_LOG`, `/handoffs` files) so transitions stay auditable.
- **State Isolation** – Codex maintains the planning state, Claude works from the provided bundle, and any shared state lives in the repo (not hidden in prompts).
- **Lifecycle Hooks** – The cycle can pause after any stage; restarting just requires revalidating the latest artefacts, keeping agents focused on their entry criteria.

---

## Suggested Orchestration Flow

1. **Initialize Session**
   - User records the mission in `SESSION_LOG.md` (Task + Constraints).
   - Codex runs a quick context survey (repo state, open PRs, external references).

2. **Codex Planning Pass**
   - Draft the execution plan and context bundle.
   - Use `prompts/claude/triad-executor.md` as the canonical Claude prompt template.
   - Store any supplementary notes under `/handoffs/`.

3. **Claude Execution Pass**
   - Provide the bundle and plan; request structured reporting (summary, diffs, follow-up questions).
   - Claude performs the work, returning artefacts (code blocks, error logs, test results).

4. **Codex Review & Integration**
   - Evaluate Claude’s output against acceptance criteria and repo standards.
   - If accepted, merge into the codebase (commits, PR, documentation updates).
   - If revisions are required, annotate the SESSION_LOG and re-enter the loop with amended constraints.

5. **Session Closure**
   - Summarize outcomes, decisions, and next steps in `SESSION_LOG.md`.
   - Archive the handoff packet if long-term traceability is needed.

---

## Automation Hooks

- **Trigger** – Start when the user drops a new mission into `SESSION_LOG.md` or adds a `@triad` label in an issue tracker.
- **Codex Task Runner** – Script that gathers file diffs, context snippets, and populates the prompt template.
- **Claude Executor** – CLI wrapper that submits the prompt + context bundle and captures output to `/handoffs/claude_output.md`.
- **Verifier** – Optional test runner that Codex calls before closing the loop.

---

## Guardrails

- Keep the Claude prompt under token limits by aggressively summarizing context.
- Avoid giving Claude write access to sensitive files unless explicitly required.
- Always verify Claude’s output before merging—Factor 10 emphasises human or Codex oversight.
- Treat each session as independent; do not assume Claude retains history beyond the provided context.

---

By keeping responsibilities crisp and artefacts explicit, the triad slots neatly into Factor 10 while preserving observability, safety, and focus.
