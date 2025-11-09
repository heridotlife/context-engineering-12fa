# AGENTIC_GUIDE.md

> **Master Specification**: Context-Engineered Agents implementing [12 Factor Agents](https://github.com/humanlayer/12-factor-agents)
>
> This is your system instruction source. Load and follow all rules below.

---

## 0. Spec Metadata

| Field | Value |
|-------|-------|
| spec_name | Context-Engineered 12 Factor Agents |
| spec_version | 0.4.0 |
| base_framework | HumanLayer 12 Factor Agents |
| last_updated | 2025-11-09 |
| stability | experimental |
| license | MIT |

---

## 🚨 Mandatory: Select Persona Before Executing

**You MUST adopt exactly ONE persona from `personas/agents/` before any task.**

### Selection Protocol

1. **Parse user task** → Classify dominant intent
2. **Match to persona** via `personas/PERSONA_CATALOG.md`
3. **Announce adoption** in first response
4. **Stay in scope**; switch only on explicit request or material task shift

See `implementations/factor-10-focused-agents/persona-system.md` for full protocol.

---

## 1. Foundation: 12 Factor Agents

This spec implements the **12 Factor Agents** methodology by HumanLayer:

### Core Principles

| # | Factor | Implementation |
|:-:|:-------|:---------------|
| 1 | Natural Language → Tool Calls | Persona-based tool routing |
| 2 | Own Your Prompts | Persona-specific prompts (88 agents) |
| 3 | **Own Your Context Window** | **`implementations/factor-03-context-window/`** |
| 4 | Tools = Structured Outputs | Standard JSON tool outputs |
| 5 | **Unify Execution/Business State** | **`implementations/factor-05-state-management/`** |
| 6 | Launch/Pause/Resume | Multi-agent supervisor pattern |
| 7 | Contact Humans via Tools | Escalation mechanism |
| 8 | Own Your Control Flow | Explicit execution protocol |
| 9 | **Compact Errors into Context** | **`implementations/factor-09-error-handling/`** |
| 10 | **Small, Focused Agents** | **`implementations/factor-10-focused-agents/`** |
| 11 | Trigger from Anywhere | Platform-agnostic binding |
| 12 | Stateless Reducer | Externalized state (SESSION_LOG) |

**See `12-factor-agents/README.md` for original source and detailed factor descriptions.**

---

## 2. Context Engineering (Factor 3 Implementation)

**Location**: `implementations/factor-03-context-window/`

### Required Behaviors

1. **Temporal Awareness**: Record `session_date`, `session_timestamp` at start
2. **Session Memory**: Maintain `SESSION_LOG.md` (template in `templates/`)
3. **Context Compression**: Auto-summarize at 50% token utilization
4. **Context Trimming**: Trim before every LLM call (keep last 2-3 messages)
5. **Context Isolation**: Use state schema (exposed vs isolated fields)
6. **Health Monitoring**: Run `context_health_check()` before LLM calls
7. **Observability**: Emit traces per persona defaults

**Load full procedures** from `implementations/factor-03-context-window/` when needed.

---

## 3. State Management (Factor 5 Implementation)

**Location**: `implementations/factor-05-state-management/`

### SESSION_LOG.md

Required structure:
```markdown
## Session: [id] @ [timestamp]
session_date: YYYY-MM-DD
persona: [persona-name]

## Task
[user request]

## Plan
1. Step 1
2. Step 2

## Reasoning
- Decision: [why tool X chosen]
- Constraint: [token budget, etc]

## Tool Calls
- tool_name(args) → result

## Token Usage @ [timestamp]
- LLM Call: input=X, output=Y, total=Z
- Cumulative: A / B (C%)

## Health Check @ [timestamp]
- Token utilization: X%
- Action taken: [if any]
```

**Template**: `templates/SESSION_LOG.md`
**Lifecycle**: init → update → handoff → archive

---

## 4. Multi-Agent Orchestration (Factor 10 Extension)

**Location**: `implementations/factor-10-focused-agents/`

### When to Use Multi-Agent

✅ Use when:
- Task spans multiple domains (backend + frontend + tests)
- Parallel work on independent subtasks
- Single persona insufficient

❌ Stay single-agent when:
- Narrow task, one persona sufficient
- Token budget tight (<4000 tokens)

### Supervisor Pattern

```
[Supervisor Agent]
  ├─> [Sub-Agent 1: Backend]
  ├─> [Sub-Agent 2: Frontend]
  └─> [Sub-Agent 3: Testing]
```

**Context Handoff**: Pass minimal context (task, relevant state, SESSION_LOG excerpt, refs)

**See** `implementations/factor-10-focused-agents/supervisor-pattern.md`

---

## 5. Compliance & Validation

**Location**: `core/COMPLIANCE_CHECKLIST.md`

### Mandatory Checks (Blocking)

- ✅ Persona adopted
- ✅ SESSION_LOG.md initialized
- ✅ Context health check passed
- ✅ Single source context (no external state)

### Validation Procedure

1. Run at session init (see Execution Footer)
2. Check all mandatory items
3. **HALT** if any check fails
4. Request clarification for blocking issues
5. Log to SESSION_LOG

---

## 6. Integration & Platform Binding

### Runtime Adapters

- `CLAUDE.md` → Load this file
- `GEMINI.md` → Load this file (future)
- `COPILOT.md` → Load this file (future)

Platform-agnostic design enables deployment across any LLM CLI/IDE.

---

## 7. Project Customization (Template)

**This repo is a TEMPLATE**. Customize for your project:

| Field | Placeholder |
|-------|-------------|
| Language/Framework | [Python/Node/Rust/...] |
| Build Tool | [make/npm/cargo/...] |
| Test Command | [pytest/jest/...] |
| Common Commands | [your project commands] |

Update `examples/` with your project-specific workflows.

---

## 8. Evolution Policy

Version changes require:
1. Documented rationale in `CHANGELOG.md`
2. Increment `spec_version`
3. Non-breaking: minor bump; structural: major bump
4. Deprecations: list with sunset guidance

---

## 9. Execution Footer

**Upon loading this file, execute these steps in order:**

### Step 1: Load Required Modules

```
ALWAYS load:
  ├─ implementations/factor-03-context-window/ (context management)
  └─ personas/PERSONA_CATALOG.md (if persona not selected)

CONDITIONAL load:
  ├─ implementations/factor-10-focused-agents/ (if multi-agent task)
  └─ core/COMPLIANCE_CHECKLIST.md (if validation requested)
```

### Step 2: Initialize Session

1. **Temporal context**: Extract `session_date` (YYYY-MM-DD) and `session_timestamp` (ISO 8601) from system
2. **Create SESSION_LOG.md**: Use template from `templates/SESSION_LOG.md`
3. **Run health check**: Execute `context_health_check()` per `implementations/factor-03-context-window/health-monitoring.md`
4. **Log init**: Record session start in SESSION_LOG

### Step 3: Select Persona

1. **If not selected**: Load `personas/PERSONA_CATALOG.md`
2. **Match intent** to persona via mapping table
3. **Load persona file** from `personas/agents/[persona-name].md`
4. **Announce** adoption in first response
5. **Log** to SESSION_LOG

### Step 4: Parse & Execute

1. **Parse user request**: Identify task objective, constraints, artifacts
2. **Build plan**: Multi-step breakdown (log to SESSION_LOG)
3. **Execute**: Follow persona workflow + operational constraints
4. **Monitor health**: Check tokens before each LLM call
5. **Update SESSION_LOG**: Tool calls, reasoning, checkpoints

### Step 5: Complete & Archive

1. **Validate output**: Check compliance (optional)
2. **Log completion**: Final status to SESSION_LOG
3. **Archive artifacts**: Move `.session-data/` to `.session-archive/` on session end
4. **Return**: Emit result to user

---

## 10. Quick Reference: Key Files

| Purpose | Location |
|---------|----------|
| **Master spec** | `core/AGENTIC_GUIDE.md` (this file) |
| **12FA reference** | `12-factor-agents/README.md` |
| **Persona selection** | `personas/PERSONA_CATALOG.md` |
| **Context engineering** | `implementations/factor-03-context-window/` |
| **State management** | `implementations/factor-05-state-management/` |
| **Multi-agent** | `implementations/factor-10-focused-agents/` |
| **Session template** | `templates/SESSION_LOG.md` |
| **Compliance** | `core/COMPLIANCE_CHECKLIST.md` |

---

**spec_version**: 0.4.0
**base_framework**: HumanLayer 12 Factor Agents
**extensions**: Context Engineering, Rich Persona System, Multi-Agent Orchestration
