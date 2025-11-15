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

> **📋 For detailed instructions, see [INSTALLATION.md](INSTALLATION.md)**

### 1. Copy to Your Project

**Essential files** (must copy):

```bash
# Option A: Copy everything to .agentic/ subdirectory (recommended)
cd your-project/
cp -r /path/to/context-engineering-12fa/.agentic

# Option B: Copy to project root
cd your-project/
cp -r /path/to/context-engineering-12fa/{core,implementations,personas,templates} .
cp /path/to/context-engineering-12fa/CLAUDE.md .  # Or GEMINI.md or COPILOT.md
```

**Minimal installation** (5 directories + 1 file):
```
your-project/
├── CLAUDE.md              ← Platform binding (choose one)
├── core/                  ← Master spec
├── implementations/       ← 12FA implementations
├── personas/              ← 88 agent personas
├── prompts/               ← Structured prompt templates + examples
└── templates/             ← SESSION_LOG template
```

**Optional but recommended**:
```
your-project/
├── schemas/               ← Validation schemas
└── 12-factor-agents/      ← Reference docs
```

### 2. Customize for Your Project

Edit `core/AGENTIC_GUIDE.md` section 7:

```markdown
## 7. Project Customization

| Field | Your Value |
|-------|------------|
| Language/Framework | Python 3.12 + FastAPI |
| Build Tool | uv + ruff |
| Test Command | pytest tests/ |
| Common Commands | make dev, make test |
```

**Optional**: Add custom personas to `personas/agents/`

Add structured prompt templates:
- Fill `prompts/base_prompts/system.tpl.md` with your Background, Tools, Output format
- Create task-specific templates under `prompts/examples/`

### 3. Verify Installation

```bash
# Check AI can load the spec
# For Claude Code:
claude --help  # Should see CLAUDE.md loaded

# Verify directory structure
ls core/AGENTIC_GUIDE.md
ls personas/PERSONA_CATALOG.md
ls templates/SESSION_LOG.md
```

---

## Installation Guide

### What to Copy

#### ✅ **REQUIRED** (Core functionality)

| Path | Size | Purpose | Required? |
|------|------|---------|-----------|
| `CLAUDE.md` (or `GEMINI.md` / `COPILOT.md`) | 2 KB | Platform binding | ✅ **YES** (pick one) |
| `core/` | 36 KB | Master spec + design decisions | ✅ **YES** |
| `implementations/` | 20 KB | 12FA factor implementations | ✅ **YES** |
| `personas/` | 748 KB | Persona catalog + 86 agent files | ✅ **YES** |
| `templates/` | 4 KB | SESSION_LOG template | ✅ **YES** |

**Total required**: ~810 KB (~95 files)

#### 📦 **OPTIONAL** (Recommended)

| Path | Size | Purpose | Optional? |
|------|------|---------|-----------|
| `schemas/` | 28 KB | Validation schemas (5 files) | ⚠️ Recommended |
| `12-factor-agents/` | 3 KB | 12FA reference docs | ⚠️ Recommended |

**Total optional**: ~31 KB (~6 files)

#### ❌ **DO NOT COPY** (Template-specific)

| Path | Reason |
|------|--------|
| `README.md` | This is the template's README, not yours |
| `CHANGELOG.md` | Template version history |
| `MIGRATION_SUMMARY.md` | Template migration docs |
| `AGENTIC_GUIDE.md.old` | Backup file |
| `SESSION_LOG.md` (root) | Active session file (use template from `templates/`) |
| `.git/` | Template git history |
| `scripts/` | Template maintenance scripts |
| `examples/` | Empty placeholder (add your own) |

---

### Installation Methods

#### Method 1: Subdirectory Install (Recommended)

Keep agent specs isolated in `.agentic/` subdirectory:

```bash
cd your-project/

# Copy essential files
mkdir -p .agentic
cp -r /path/to/template/core .agentic/
cp -r /path/to/template/implementations .agentic/
cp -r /path/to/template/personas .agentic/
cp -r /path/to/template/templates .agentic/
cp /path/to/template/CLAUDE.md .agentic/

# Optional: Copy schemas
cp -r /path/to/template/schemas .agentic/

# Create platform binding at root
ln -s .agentic/CLAUDE.md CLAUDE.md
# Or copy: cp .agentic/CLAUDE.md .
```

**Result**:
```
your-project/
├── CLAUDE.md → .agentic/CLAUDE.md
├── .agentic/
│   ├── core/
│   ├── implementations/
│   ├── personas/
│   ├── templates/
│   └── schemas/
├── src/
└── tests/
```

**Pros**: Clean separation, easy updates, portable
**Cons**: One extra directory level

---

#### Method 2: Root Install (Simple)

Copy directly to project root:

```bash
cd your-project/

# Copy essential files
cp -r /path/to/template/core .
cp -r /path/to/template/implementations .
cp -r /path/to/template/personas .
cp -r /path/to/template/templates .
cp /path/to/template/CLAUDE.md .

# Optional
cp -r /path/to/template/schemas .
```

**Result**:
```
your-project/
├── CLAUDE.md
├── core/
├── implementations/
├── personas/
├── templates/
├── schemas/
├── src/
└── tests/
```

**Pros**: Simpler structure, direct access
**Cons**: Mixes template with your code

---

#### Method 3: Git Submodule (Advanced)

Keep template as submodule for easy updates:

```bash
cd your-project/
git submodule add https://github.com/yourusername/context-engineering-12fa.git .agentic
git submodule update --init --recursive

# Create binding at root
ln -s .agentic/CLAUDE.md CLAUDE.md
```

**Update template**:
```bash
cd .agentic
git pull origin main
cd ..
git commit -am "Update .agentic submodule"
```

**Pros**: Easy updates, version control
**Cons**: More complex setup, requires git

---

### Post-Installation

#### 1. Update Project Settings

Edit `core/AGENTIC_GUIDE.md` section 7:

```markdown
## 7. Project Customization

| Field | Value |
|-------|-------|
| Language/Framework | [Your stack: Python/Node/Rust/etc] |
| Build Tool | [Your tool: npm/cargo/make/etc] |
| Test Command | [Your command: pytest/jest/etc] |
| Common Commands | [Your commands] |
```

#### 2. Verify Installation

```bash
# Check core files exist
ls core/AGENTIC_GUIDE.md
ls personas/PERSONA_CATALOG.md
ls templates/SESSION_LOG.md
ls prompts/base_prompts/system.tpl.md

# Check platform binding
cat CLAUDE.md | grep "core/AGENTIC_GUIDE.md"

# Test with AI
# For Claude Code: Open project, AI should load CLAUDE.md automatically
```

#### 3. Optional: Add .gitignore

```bash
# Add to your .gitignore
echo ".session-archive/" >> .gitignore
echo "SESSION_LOG.md" >> .gitignore  # Active session logs
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
- **🌐 Temporal Awareness + Auto Web Search**: Detect outdated knowledge, trigger web search for latest versions/security/releases

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
