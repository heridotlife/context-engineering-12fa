# Factor 4: Tools Are Just Structured Outputs

> **Source**: [HumanLayer 12 Factor Agents](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-04-tools-are-structured-outputs.md)

---

## Overview

Tools are fundamentally "just structured output from your LLM that triggers deterministic code." Rather than complex implementations, tools involve three simple steps:

1. An LLM outputs structured JSON
2. Deterministic code executes the appropriate action
3. Results feed back into context

## Core Concept

### The Pattern

```python
# Step 1: LLM outputs JSON
tool_call = {
    "intent": "create_payment_link",
    "parameters": {
        "amount": 750,
        "customer": "Terri",
        "memo": "February AI Tinkerers sponsorship"
    }
}

# Step 2: Deterministic routing
if tool_call["intent"] == "create_payment_link":
    result = create_payment_link(**tool_call["parameters"])
elif tool_call["intent"] == "wait_for_a_while":
    result = wait_for_a_while(**tool_call["parameters"])

# Step 3: Feed result back to context
context.append({"role": "tool", "content": result})
```

## Important Distinction

**"The LLM decides what to do, but your code controls how it's done."**

This separation means you have flexibility in implementation—an LLM's tool selection doesn't mandate executing a specific function identically each time. You can:

- Add validation layers
- Implement retry logic
- Route to different backends based on context
- Mock tools in testing
- Add observability hooks

## Plain Prompting vs. Tool Calling vs. JSON Mode

The document references debates about different approaches. The key insight: tools are just one way to get structured output from LLMs. Choose based on your needs:

- **Plain prompting**: Simple, but less reliable structure
- **Tool calling**: Native LLM support, good for function dispatch
- **JSON mode**: Guaranteed valid JSON, good for complex schemas

This factor combines with Factor 8 (own your control flow) to give you maximum flexibility.

---

## 🎯 Our Implementation

### Location

Implemented via **standard JSON tool contracts** in:
- `personas/agents/*.md` - Each persona defines its tool interface
- `schemas/` - JSON schemas for tool validation
- `core/AGENTIC_GUIDE.md` (§1) - Tool routing via personas

### How It Works

We use structured JSON outputs with persona-specific tool definitions:

#### Tool Definition (Persona Level)

```markdown
# personas/agents/backend-architect.md

## Available Tools

### create_rest_endpoint
Creates a new REST API endpoint with proper routing and handlers.

**Input Schema**:
```json
{
  "tool": "create_rest_endpoint",
  "parameters": {
    "method": "GET|POST|PUT|DELETE|PATCH",
    "path": "/api/v1/resource",
    "handler": "function_name",
    "auth_required": true,
    "rate_limit": "100/hour"
  }
}
```

**Output Schema**:
```json
{
  "status": "success|error",
  "endpoint_created": "/api/v1/resource",
  "file_modified": "src/routes/api.py:42",
  "tests_created": ["tests/test_api.py:15"]
}
```
```

#### Deterministic Routing

```python
def execute_tool_call(tool_call, persona):
    """Route tool calls to appropriate handlers"""

    # Validate against persona's tool schema
    validate_tool_schema(tool_call, persona)

    # Deterministic routing based on tool name
    tool_handlers = {
        "create_rest_endpoint": handle_create_endpoint,
        "add_authentication": handle_add_auth,
        "setup_database": handle_setup_db,
        "add_middleware": handle_add_middleware
    }

    handler = tool_handlers.get(tool_call["tool"])
    if not handler:
        return {"status": "error", "message": f"Unknown tool: {tool_call['tool']}"}

    # Execute with observability
    start_time = time.time()
    try:
        result = handler(**tool_call["parameters"])
        log_tool_success(tool_call, result, time.time() - start_time)
        return result
    except Exception as e:
        log_tool_error(tool_call, e, time.time() - start_time)
        return {"status": "error", "message": str(e)}
```

#### Validation & Testing

```python
# schemas/tool-contract.json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["tool", "parameters"],
  "properties": {
    "tool": {
      "type": "string",
      "description": "Tool identifier"
    },
    "parameters": {
      "type": "object",
      "description": "Tool-specific parameters"
    }
  }
}

# Validation
import jsonschema

def validate_tool_schema(tool_call, persona):
    # Load persona's tool schema
    schema = load_schema(f"personas/{persona}/tools.json")

    # Validate
    try:
        jsonschema.validate(instance=tool_call, schema=schema)
    except jsonschema.ValidationError as e:
        raise ToolValidationError(f"Invalid tool call: {e.message}")
```

### Advantages

1. **Flexibility**: LLM suggests, code controls execution
2. **Testing**: Mock any tool handler in tests
3. **Observability**: Log every tool call with timing/results
4. **Validation**: Schema validation before execution
5. **Personas**: Each persona has its own tool catalog

### Example: Same Tool, Different Execution

```python
# LLM always outputs same structure
tool_call = {"tool": "create_payment_link", "parameters": {...}}

# But execution varies by context
def create_payment_link(**params):
    if environment == "test":
        return mock_payment_link(**params)
    elif environment == "staging":
        return sandbox_payment_link(**params)
    else:
        return stripe.create_payment_link(**params)
```

---

## Related Factors

- **Factor 1**: Natural Language to Tool Calls (persona routing to tools)
- **Factor 2**: Own Your Prompts (personas define tool instructions)
- **Factor 8**: Own Your Control Flow (deterministic tool routing)

---

**Version**: 0.4.0
**Status**: ✅ Implemented via standard JSON contracts + persona tool catalogs
**See Also**: `schemas/tool-contract.json`, `personas/agents/`
