# Factor 2: Own Your Prompts

> **Source**: [HumanLayer 12 Factor Agents](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-02-own-your-prompts.md)

---

## Overview

This factor advocates for maintaining direct control over prompt engineering rather than relying on framework abstractions.

## Core Argument

The factor contrasts two approaches:

**Black Box Frameworks**: Some tools hide prompt complexity behind high-level abstractions (role, goal, personality parameters), making tuning and reverse-engineering difficult.

**Owned Prompts**: Treat prompts as first-class code with full visibility and control.

## Key Benefits

The document identifies five advantages to owning your prompts:

1. **Full Control** - Write precise instructions without abstraction layers
2. **Testing and Evals** - Create comprehensive tests like any codebase
3. **Iteration** - Rapidly adjust based on production performance
4. **Transparency** - Know exactly what instructions guide the agent
5. **Role Hacking** - Leverage non-standard API uses for advanced techniques

## Practical Implementation

Your prompts are the primary interface between your application logic and the LLM, making control essential for production-grade agents.

---

## 🎯 Our Implementation

### Location

Implemented via **persona-specific prompts** in:
- `personas/agents/` - 86 specialized persona files with tailored prompts
- `core/AGENTIC_GUIDE.md` - Master execution protocol
- `implementations/factor-10-focused-agents/` - Persona system architecture

### How It Works

Instead of generic prompts, each persona has a custom-tailored system prompt:

```markdown
# personas/agents/backend-architect.md

## Role & Expertise
Expert backend architect specializing in scalable API design, microservices
architecture, and distributed systems...

## Core Competencies
- REST/GraphQL/gRPC API design
- Event-driven architectures
- Service mesh patterns
- Database design & optimization

## Operational Constraints
- Always consider scalability implications
- Prefer standard patterns over clever tricks
- Document architectural decisions
```

### Advantages

1. **Domain-specific instructions**: Each persona has prompts optimized for its domain
2. **Version control**: All prompts stored as markdown files in git
3. **A/B testing**: Easy to test prompt variations per persona
4. **Transparency**: Full visibility into what each agent is instructed to do
5. **Rapid iteration**: Update prompts without framework changes

### Example: Prompt Specialization

| Persona | Prompt Focus | Key Instructions |
|---------|--------------|------------------|
| `backend-architect` | API design, scalability | "Always consider distributed system implications" |
| `security-auditor` | Security, compliance | "Enumerate all attack surfaces before proposing solutions" |
| `python-pro` | Python best practices | "Use type hints, follow PEP 8, prefer standard library" |
| `frontend-developer` | React, accessibility | "Ensure ARIA labels, test with screen readers" |

### Testing & Iteration

```bash
# Test persona prompt changes
pytest tests/personas/test_backend_architect.py

# Compare prompt versions
git diff personas/agents/backend-architect.md

# Roll back if needed
git checkout HEAD~1 personas/agents/backend-architect.md
```

---

## Related Factors

- **Factor 1**: Natural Language to Tool Calls (persona selection uses these prompts)
- **Factor 10**: Small, Focused Agents (each focused agent has its own prompt)
- **Factor 11**: Trigger from Anywhere (platform bindings load prompts consistently)

---

**Version**: 0.4.0
**Status**: ✅ Fully implemented via 86 persona-specific prompts
**See Also**: `personas/PERSONA_CATALOG.md`, `implementations/factor-10-focused-agents/`
