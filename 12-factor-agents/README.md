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

> Each factor includes HumanLayer's original content plus our implementation notes showing how we extend and apply the principles.

| # | Factor | Local File | HumanLayer Source | Our Implementation |
|:-:|:-------|:-----------|:------------------|:-------------------|
| 1 | **Natural Language to Tool Calls** | [01-natural-language-to-tool-calls.md](01-natural-language-to-tool-calls.md) | [View](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-01-natural-language-to-tool-calls.md) | Persona-based tool routing |
| 2 | **Own Your Prompts** | [02-own-your-prompts.md](02-own-your-prompts.md) | [View](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-02-own-your-prompts.md) | 86 persona-specific prompts in `personas/agents/` |
| 3 | **Own Your Context Window** | [03-own-your-context-window.md](03-own-your-context-window.md) | [View](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-03-own-your-context-window.md) | ✅ **Full implementation** in `implementations/factor-03-context-window/` |
| 4 | **Tools Are Just Structured Outputs** | [04-tools-are-structured-outputs.md](04-tools-are-structured-outputs.md) | [View](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-04-tools-are-structured-outputs.md) | Standard JSON tool outputs |
| 5 | **Unify Execution State and Business State** | [05-unify-execution-and-business-state.md](05-unify-execution-and-business-state.md) | [View](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-05-unify-execution-state.md) | ✅ **SESSION_LOG.md** in `implementations/factor-05-state-management/` |
| 6 | **Launch/Pause/Resume** | [06-launch-pause-resume.md](06-launch-pause-resume.md) | [View](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-06-launch-pause-resume.md) | Multi-agent supervisor pattern |
| 7 | **Contact Humans with Tool Calls** | [07-contact-humans-with-tool-calls.md](07-contact-humans-with-tool-calls.md) | [View](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-07-contact-humans-with-tools.md) | Human-in-loop via tool escalation |
| 8 | **Own Your Control Flow** | [08-own-your-control-flow.md](08-own-your-control-flow.md) | [View](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-08-own-your-control-flow.md) | Explicit execution footer + health checks |
| 9 | **Compact Errors Into Context** | [09-compact-errors-into-context.md](09-compact-errors-into-context.md) | [View](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-09-compact-errors.md) | ✅ **Error compaction** in `implementations/factor-09-error-handling/` |
| 10 | **Small, Focused Agents** | [10-small-focused-agents.md](10-small-focused-agents.md) | [View](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-10-small-focused-agents.md) | ✅ **86 personas** + multi-agent in `implementations/factor-10-focused-agents/` |
| 11 | **Trigger from Anywhere** | [11-trigger-from-anywhere.md](11-trigger-from-anywhere.md) | [View](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-11-trigger-from-anywhere.md) | Platform-agnostic (Claude, Gemini, Copilot) |
| 12 | **Stateless Reducer** | [12-stateless-reducer.md](12-stateless-reducer.md) | [View](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-12-make-your-agent-a-stateless-reducer.md) | Stateless design with externalized SESSION_LOG |

---

## How We Extend 12FA

1. **Rich Persona System** (Factor 10): 86 specialized agents vs. HumanLayer's 5
2. **Context Engineering** (Factor 3): Auto-compression, trimming, health monitoring, **temporal awareness + auto web search**
3. **State Management** (Factor 5): Structured SESSION_LOG with checkpoints
4. **Multi-Agent Orchestration** (Factor 10): Supervisor pattern with context handoffs
5. **Observability** (Factor 8): Token tracking, reasoning traces, health checks
6. **Temporal Awareness** (Factor 3): Automatic web search for latest versions/security/releases

---

## Usage

### Reading Factor Documentation

Each factor file (01-12.md) contains:
1. **HumanLayer's original principle** - The core concept from 12 Factor Agents
2. **Implementation examples** - Code patterns and best practices
3. **🎯 Our Implementation section** - How we apply it in this project
4. **Related factors** - Cross-references to related principles

### When to Load Factor Files

- **Designing new features**: Reference factor principles for architecture decisions
- **Debugging issues**: Check factor compliance to diagnose problems
- **Onboarding**: Understand architecture decisions and patterns
- **Learning**: Study HumanLayer's principles + our practical extensions

### Quick Navigation

- Start with `core/AGENTIC_GUIDE.md` for the master spec
- Browse local factor files (01-12.md) for detailed principles
- Check `implementations/` for production-ready implementations
- Reference HumanLayer's originals via "HumanLayer Source" links for latest updates

---

**Version**: 0.4.0 (aligned with HumanLayer 12FA)
**Last Updated**: 2025-11-09
