# Context-Engineered 12 Factor Agents

> Production-ready AI agents implementing [HumanLayer's 12 Factor Agents](https://github.com/humanlayer/12-factor-agents) with context engineering extensions.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE.md)
[![Spec Version](https://img.shields.io/badge/spec-0.4.0-green.svg)](CHANGELOG.md)
[![12FA Compliant](https://img.shields.io/badge/12FA-compliant-brightgreen.svg)](https://www.humanlayer.dev/12-factor-agents)

---

## What is This?

A **reusable template** for building reliable, production-ready AI agents that combines:

1. **[12 Factor Agents](https://github.com/humanlayer/12-factor-agents)** (HumanLayer) - Proven principles for LLM applications
2. **Context Engineering** - Active context window management (Factor 3 implementation)
3. **Rich Persona System** - 88 specialized agent personas (Factor 10 extension)
4. **Multi-Agent Orchestration** - Supervisor pattern with clean handoffs

---

## Quick Start

### 1. For AI Agents (Claude, Gemini, Copilot)

```bash
# Clone/copy this template into your project
git clone https://github.com/yourusername/context-engineering-12fa.git

# Your AI will automatically load:
# 1. CLAUDE.md → core/AGENTIC_GUIDE.md
# 2. Select persona from personas/PERSONA_CATALOG.md
# 3. Initialize SESSION_LOG.md from templates/
# 4. Execute following 12 Factor Agents principles
```

### 2. Customize for Your Project

```bash
# Update project-specific settings in core/AGENTIC_GUIDE.md:
- Language/Framework
- Build commands
- Test commands
- Common operations

# Add custom personas to personas/agents/ (optional)
# Extend implementations/ with project-specific patterns
```

---

## Architecture

### 📂 Directory Structure

```
context-engineering-12fa/
├── README.md                          # This file
├── CLAUDE.md                          # Runtime binding (→ core/AGENTIC_GUIDE.md)
├── CHANGELOG.md                       # Version history
│
├── core/                              # Core specifications
│   ├── AGENTIC_GUIDE.md              # 🎯 Master spec (start here)
│   └── COMPLIANCE_CHECKLIST.md       # Validation rules
│
├── 12-factor-agents/                  # 12FA reference
│   └── README.md                      # Maps our work to 12FA factors
│
├── implementations/                   # Our 12FA implementations
│   ├── factor-03-context-window/     # ⭐ Context engineering
│   ├── factor-05-state-management/   # SESSION_LOG system
│   ├── factor-09-error-handling/     # Error compaction
│   └── factor-10-focused-agents/     # ⭐ Multi-agent orchestration
│
├── personas/                          # Persona catalog
│   ├── PERSONA_CATALOG.md            # ⭐ Persona selection guide
│   └── agents/                        # 88 specialized persona files
│
├── templates/                         # Reusable templates
│   └── SESSION_LOG.md                # Session scratchpad template
│
├── schemas/                           # Machine-readable specs
└── .session-archive/                  # Session artifacts (gitignored)
```

---

## How We Implement 12 Factor Agents

| # | Factor | Our Implementation | Load Cost |
|:-:|:-------|:-------------------|:----------|
| **1** | Natural Language → Tool Calls | Persona-based routing | ~200 tokens |
| **2** | Own Your Prompts | 88 persona prompts | ~300 tokens |
| **3** | 🌟 **Own Your Context Window** | **Full implementation** | ~3,000 tokens |
| **4** | Tools = Structured Outputs | Standard JSON | ~100 tokens |
| **5** | 🌟 **Unify Execution/Business State** | **SESSION_LOG.md** | ~1,000 tokens |
| **6** | Launch/Pause/Resume | Multi-agent supervisor | ~800 tokens |
| **7** | Contact Humans via Tools | Human-in-loop | ~200 tokens |
| **8** | Own Your Control Flow | Execution footer | ~400 tokens |
| **9** | 🌟 **Compact Errors into Context** | Error compaction | ~600 tokens |
| **10** | 🌟 **Small, Focused Agents** | **88 personas** | ~1,500 tokens |
| **11** | Trigger from Anywhere | Platform-agnostic | ~100 tokens |
| **12** | Stateless Reducer | Externalized state | ~200 tokens |

**Typical Load**: ~2,500 tokens (core + 1 persona)
**Full Load**: ~8,400 tokens (all implementations)

---

## Key Features

### ⭐ Factor 3: Context Engineering

Production-ready context window management:
- **Auto-Summarization**: Trigger at 50% token usage
- **Proactive Trimming**: Before every LLM call
- **Health Monitoring**: Continuous context quality checks

**Location**: `implementations/factor-03-context-window/`

### ⭐ Factor 10: Rich Persona System

88 specialized agent personas vs. HumanLayer's 5:

**Backend**: backend-architect, api-documenter, graphql-architect
**Frontend**: frontend-developer, ui-ux-designer, mobile-developer
**Languages**: python-pro, typescript-pro, rust-pro, golang-pro
**Operations**: performance-engineer, security-auditor
**Data/ML**: data-engineer, ml-engineer, mlops-engineer

**Location**: `personas/agents/`

### ⭐ Multi-Agent Orchestration

Supervisor pattern with clean context handoffs for parallel/sequential task execution.

**Location**: `implementations/factor-10-focused-agents/`

---

## License

MIT License

### Attribution

- **12 Factor Agents**: HumanLayer (https://github.com/humanlayer/12-factor-agents)
- **Persona Library**: Adapted from wshobson/agents (MIT)

---

**spec_version**: 0.4.0 | **base_framework**: HumanLayer 12 Factor Agents
