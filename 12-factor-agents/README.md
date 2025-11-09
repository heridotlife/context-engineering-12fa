# 12 Factor Agents (Reference)

> This directory references the **original 12 Factor Agents specification** by HumanLayer.
> Our implementation in `../implementations/` extends and implements these principles.

---

## Original Source

**Repository**: https://github.com/humanlayer/12-factor-agents
**Website**: https://www.humanlayer.dev/12-factor-agents
**License**: MIT (HumanLayer)

---

## The 12 Factors

| # | Factor | Our Implementation |
|:-:|:-------|:-------------------|
| 1 | [Natural Language to Tool Calls](01-natural-language-to-tool-calls.md) | Persona-based tool routing |
| 2 | [Own Your Prompts](02-own-your-prompts.md) | Persona-specific prompts in `personas/agents/` |
| 3 | [Own Your Context Window](03-own-your-context-window.md) | **Full implementation** in `implementations/factor-03-context-window/` |
| 4 | [Tools Are Just Structured Outputs](04-tools-structured-outputs.md) | Standard JSON tool outputs |
| 5 | [Unify Execution State and Business State](05-unify-execution-business-state.md) | **SESSION_LOG.md** in `implementations/factor-05-state-management/` |
| 6 | [Launch/Pause/Resume](06-launch-pause-resume.md) | Multi-agent supervisor pattern |
| 7 | [Contact Humans with Tool Calls](07-contact-humans-tool-calls.md) | Human-in-loop via tool escalation |
| 8 | [Own Your Control Flow](08-own-your-control-flow.md) | Explicit execution footer + health checks |
| 9 | [Compact Errors Into Context](09-compact-errors-context.md) | **Error compaction** in `implementations/factor-09-error-handling/` |
| 10 | [Small, Focused Agents](10-small-focused-agents.md) | **88 personas** + multi-agent in `implementations/factor-10-focused-agents/` |
| 11 | [Trigger from Anywhere](11-trigger-from-anywhere.md) | Platform-agnostic (Claude, Gemini, Copilot) |
| 12 | [Stateless Reducer](12-stateless-reducer.md) | Stateless design with externalized SESSION_LOG |

---

## How We Extend 12FA

1. **Rich Persona System** (Factor 10): 88 specialized agents vs. HumanLayer's 5
2. **Context Engineering** (Factor 3): Auto-compression, trimming, health monitoring
3. **State Management** (Factor 5): Structured SESSION_LOG with checkpoints
4. **Multi-Agent Orchestration** (Factor 10): Supervisor pattern with context handoffs
5. **Observability** (Factor 8): Token tracking, reasoning traces, health checks

---

## Usage

Load the appropriate factor file when:
- **Designing new features**: Reference factor principles
- **Debugging issues**: Check factor compliance
- **Onboarding**: Understand architecture decisions

**Always start with** `core/AGENTIC_GUIDE.md` for the master spec.

---

**Version**: 0.4.0 (aligned with HumanLayer 12FA)
**Last Updated**: 2025-11-09
