# Factor 1: Natural Language to Tool Calls

> **Source**: [HumanLayer 12 Factor Agents](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-01-natural-language-to-tool-calls.md)

---

## Overview

This foundational pattern converts natural language requests into structured tool calls, enabling agents to reason about tasks and execute them programmatically.

## Core Concept

The pattern translates informal user requests—such as:

> "can you create a payment link for $750 to Terri for sponsoring the february AI tinkerers meetup?"

Into structured JSON objects describing specific API calls with properly formatted parameters.

## Example Transformation

**Input** (Natural Language):
```
"Create a payment link for $750 to Terri for the February AI Tinkerers meetup"
```

**Output** (Structured Tool Call):
```json
{
  "function": "create_payment_link",
  "parameters": {
    "amount": 750,
    "currency": "USD",
    "customer": "Terri",
    "product_id": "ai_tinkerers_sponsorship",
    "memo": "February AI Tinkerers meetup sponsorship"
  }
}
```

## Implementation Pattern

The workflow involves three steps:

1. **LLM processes** natural language and returns structured output
2. **Deterministic code** evaluates the function type
3. **Appropriate handler** executes based on the identified function

### Example Code

```python
def handle_natural_language(user_input: str):
    # Step 1: LLM converts to structured tool call
    tool_call = llm.parse(user_input, output_format="tool_call")

    # Step 2: Route based on function name
    if tool_call["function"] == "create_payment_link":
        return create_payment_link(**tool_call["parameters"])
    elif tool_call["function"] == "send_email":
        return send_email(**tool_call["parameters"])
    else:
        return handle_unknown_function(tool_call)
```

## Key Note

This factor deliberately excludes the loop-back step where agents receive API results and return final responses to users. This sequencing is intentionally deferred to subsequent factors, allowing implementers to choose which additional patterns suit their needs.

---

## 🎯 Our Implementation

### Location

Implemented via **persona-based tool routing** in:
- `personas/PERSONA_CATALOG.md` - Persona selection based on user intent
- `personas/agents/` - 86 specialized personas with tool mappings

### How It Works

Instead of a single generic agent, we use specialized personas that understand domain-specific tool calls:

```
User: "Create a REST API endpoint for user authentication"

Agent:
1. Classifies intent: "implement backend feature"
2. Selects persona: "backend-architect"
3. Loads persona from personas/agents/backend-architect.md
4. Persona has domain knowledge of:
   - Backend tools (FastAPI, Django, Express)
   - Auth patterns (JWT, OAuth, sessions)
   - Security tools (bcrypt, rate limiting)
5. Converts request to structured actions
```

### Advantages

1. **Domain expertise**: Each persona understands its domain's tools
2. **Better accuracy**: Narrow scope → better tool selection
3. **Extensible**: Add new personas = add new tool domains
4. **Type safety**: Persona defines expected tool signatures

### Example Personas & Their Tools

| Persona | Domain | Key Tools |
|---------|--------|-----------|
| `backend-architect` | Backend APIs | `create_endpoint`, `add_middleware`, `setup_db` |
| `frontend-developer` | UI Components | `create_component`, `add_state`, `style_element` |
| `security-auditor` | Security | `scan_vulnerabilities`, `check_auth`, `review_permissions` |
| `data-engineer` | Data Pipelines | `create_pipeline`, `add_transform`, `setup_warehouse` |

### Configuration

Each persona defines its tool interface in the persona file:

```markdown
# personas/agents/backend-architect.md

## Available Tools
- create_rest_endpoint(method, path, handler)
- add_authentication(type, provider)
- setup_database(engine, connection_string)
- add_middleware(name, config)
```

---

## Related Factors

- **Factor 2**: Own Your Prompts (persona prompts define tool usage)
- **Factor 4**: Tools Are Just Structured Outputs (JSON tool definitions)
- **Factor 10**: Small, Focused Agents (each persona is focused)

---

**Version**: 0.4.0
**Status**: ✅ Fully implemented via persona system
**See Also**: `personas/PERSONA_CATALOG.md`, `core/AGENTIC_GUIDE.md`
