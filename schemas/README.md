# Schemas

> Machine-readable specifications for validation and type safety

---

## Overview

This directory contains JSON schemas that define the data contracts for the 12 Factor Agents implementation.

**Purpose**:
- **Validate context inputs** before agent execution
- **Type safety** for programmatic integrations
- **Documentation** of expected data structures
- **Tooling support** for IDE autocomplete and validation

---

## Files

### 1. `context-contract.json`

**JSON Schema** defining the input contract for agent runs.

**Usage**:
```bash
# Validate a context file against the schema
jsonschema -i my-context.json schemas/context-contract.json
```

**Key Fields**:
- `persona`: Persona identifier (must match file in `./personas/agents/`)
- `task`: Primary goal or problem statement
- `target_files`: Files to modify or inspect
- `constraints`: Operational constraints (performance, security, etc.)
- `verbosity`: Output level (brief/normal/detailed)
- `trace`: Enable observability traces
- `spec_version`: Expected spec version (e.g., "0.4.0")

**Current Version**: 0.4.0

---

### 2. `sample-context.json`

**Example context object** demonstrating a complete TDD task request.

**Example**:
```json
{
  "persona": "tdd-orchestrator",
  "task": "Add a failing test for user login rate limiting and implement the minimal fix.",
  "target_files": ["src/auth/", "tests/auth/login_rate_limit.test.ts"],
  "constraints": { "performance": "<10ms added p95", "security": "no logging of secrets" },
  "spec_version": "0.4.0"
}
```

**Usage**:
- Copy as template for new tasks
- Reference for programmatic agent invocation
- Testing schema validation

---

### 3. `sample-context.toon`

**TOON format** (Text-Oriented Object Notation) equivalent of `sample-context.json`.

**Purpose**:
- **Token efficiency**: TOON saves ~10-20% tokens vs JSON
- **Human-readable**: Line-oriented format for prompts
- **LLM-friendly**: Easier for models to parse in constrained contexts

**When to use**:
- Large context payloads (>1000 tokens)
- Token budget constraints
- Prompt engineering scenarios

See `implementations/factor-03-context-window/` for TOON conversion utilities.

---

### 4. `state-schema.json`

**JSON Schema** defining the agent state object structure (Factor 5: Unify Execution/Business State).

**Key Fields**:
- `messages`: Conversational history (exposed to LLM)
- `summary`: Context summary (exposed selectively)
- `context`: Scratchpad/session data (isolated by default)
- `tool_outputs`: Raw tool results (isolated, summarized for LLM)
- `images`: Binary/base64 data (isolated)
- `large_artifacts`: Code files, documents (isolated)

**Exposure Rules**:
- **Always to LLM**: `messages` (trimmed), `summary`
- **Selective to LLM**: `tool_outputs.summary`, `context.plan`
- **Never to LLM**: `images`, `large_artifacts` (unless requested)

See `implementations/factor-05-state-management/` for implementation details.

---

## Schema Validation

### Prerequisites

```bash
# Install jsonschema CLI (Python)
pip install jsonschema

# Or use Node.js validator
npm install -g ajv-cli
```

### Validation Examples

**Validate context object**:
```bash
jsonschema -i my-context.json schemas/context-contract.json
```

**Validate state object**:
```bash
jsonschema -i session-state.json schemas/state-schema.json
```

**Using ajv (Node.js)**:
```bash
ajv validate -s schemas/context-contract.json -d my-context.json
```

---

## Integration Examples

### Python

```python
import json
import jsonschema

# Load schema
with open('schemas/context-contract.json') as f:
    schema = json.load(f)

# Validate context
context = {
    "persona": "backend-architect",
    "task": "Design user authentication API",
    "spec_version": "0.4.0"
}

try:
    jsonschema.validate(instance=context, schema=schema)
    print("✅ Valid context")
except jsonschema.ValidationError as e:
    print(f"❌ Invalid: {e.message}")
```

### TypeScript

```typescript
import Ajv from 'ajv';
import schema from './schemas/context-contract.json';

const ajv = new Ajv();
const validate = ajv.compile(schema);

const context = {
  persona: 'backend-architect',
  task: 'Design user authentication API',
  spec_version: '0.4.0',
};

if (validate(context)) {
  console.log('✅ Valid context');
} else {
  console.log('❌ Invalid:', validate.errors);
}
```

---

## Schema Evolution

**Versioning**: Schemas follow semantic versioning aligned with `spec_version`.

**Breaking Changes** (major version):
- Removing required fields
- Changing field types
- Removing enum values

**Non-Breaking Changes** (minor version):
- Adding optional fields
- Adding enum values
- Expanding patterns

**See**: `CHANGELOG.md` for schema change history

---

## Best Practices

1. **Always validate** context before agent execution
2. **Use `spec_version`** field to ensure compatibility
3. **Check persona exists** in `./personas/agents/` before validation
4. **Extend constraints** object for project-specific requirements
5. **Use TOON** for large payloads (>1000 tokens)
6. **Archive state objects** to `.session-archive/` for audit trails

---

## References

- **Factor 3**: Context Window Management → `implementations/factor-03-context-window/`
- **Factor 5**: State Management → `implementations/factor-05-state-management/`
- **Persona Catalog**: `personas/PERSONA_CATALOG.md`
- **Master Spec**: `core/AGENTIC_GUIDE.md`

---

**Version**: 0.4.0
**Maintained By**: Context-Engineered 12 Factor Agents project
**License**: MIT
