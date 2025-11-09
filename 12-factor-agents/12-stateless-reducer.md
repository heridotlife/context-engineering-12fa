# Factor 12: Make Your Agent a Stateless Reducer

> **Source**: [HumanLayer 12 Factor Agents](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-12-make-your-agent-a-stateless-reducer.md)

---

## Overview

**Core Principle**: Design agents as **stateless reducers** that take current state as input and produce new state as output, without maintaining internal state.

```python
# Stateless reducer pattern
new_state = agent(current_state, action)
```

This is directly inspired by functional programming (especially Redux) where reducers are pure functions:
- **Same input** → **Same output** (deterministic)
- **No side effects** (state externalized)
- **Easy to test** (provide state, check result)
- **Easy to debug** (inspect state at any point)

## The Anti-Pattern

❌ **Stateful Agent**: Agent maintains internal state

```python
class StatefulAgent:
    def __init__(self):
        self.conversation_history = []
        self.context = {}
        self.decisions = []
        self.tool_results = {}

    def execute(self, user_input):
        # Modifies internal state
        self.conversation_history.append(user_input)
        result = self.llm.call(self.conversation_history)
        self.decisions.append(result.decision)
        return result
```

Problems:
- **Opaque state**: Can't inspect internal variables
- **Hard to resume**: State lost between sessions
- **Hard to debug**: Can't reproduce issues (state unknown)
- **Hard to test**: Must mock entire object lifecycle

## The Pattern

✅ **Stateless Reducer**: Pure function with externalized state

```python
def agent_reducer(state: dict, action: dict) -> dict:
    """Pure function: state + action → new state"""

    # Read current state
    messages = state["messages"]
    context = state["context"]

    # Process action
    if action["type"] == "user_input":
        messages.append({"role": "user", "content": action["input"]})

        # Call LLM (only I/O side effect)
        response = llm.call(messages)

        messages.append({"role": "assistant", "content": response})

    # Return new state (don't modify input)
    return {
        **state,
        "messages": messages,
        "last_action": action["type"],
        "timestamp": now()
    }
```

Benefits:
- **Transparent state**: All state visible and inspectable
- **Easy to resume**: Just load last state
- **Easy to debug**: Replay any state + action
- **Easy to test**: `assert agent_reducer(state, action) == expected_state`

---

## 🎯 Our Implementation

### Location

Implemented via **externalized SESSION_LOG** in:
- `templates/SESSION_LOG.md` - External state storage
- `implementations/factor-05-state-management/` - State management system
- `core/AGENTIC_GUIDE.md` (§3, §12) - Stateless design

### How It Works

We implement stateless design by externalizing all state to SESSION_LOG.md:

#### Stateless Agent Interface

```python
class StatelessAgent:
    """Agent as pure reducer function"""

    def __init__(self, persona: str):
        # Only configuration (no state!)
        self.persona = load_persona(persona)
        self.model = self.persona["model"]

    def execute(self, session_log_path: str, action: dict) -> dict:
        """Pure reducer: (session_log, action) → new session_log"""

        # Load state from external storage
        state = self.load_session_log(session_log_path)

        # Process action
        new_state = self.reduce(state, action)

        # Save state to external storage
        self.save_session_log(session_log_path, new_state)

        # Return result (don't keep state!)
        return new_state["result"]

    def reduce(self, state: dict, action: dict) -> dict:
        """Pure function: no internal state modification"""

        if action["type"] == "user_request":
            return self.handle_user_request(state, action)

        elif action["type"] == "tool_call":
            return self.handle_tool_call(state, action)

        elif action["type"] == "error":
            return self.handle_error(state, action)

        return state
```

#### External State Storage

```python
# All state stored in SESSION_LOG.md (external file)

def load_session_log(path: str) -> dict:
    """Load state from external storage"""

    with open(path) as f:
        content = f.read()

    # Parse SESSION_LOG.md structure
    return {
        "session_id": extract_session_id(content),
        "persona": extract_persona(content),
        "task": extract_task(content),
        "plan": extract_plan(content),
        "decisions": extract_decisions(content),
        "tool_calls": extract_tool_calls(content),
        "token_usage": extract_token_usage(content),
        "health_checks": extract_health_checks(content)
    }

def save_session_log(path: str, state: dict):
    """Save state to external storage"""

    content = format_session_log(state)

    with open(path, "w") as f:
        f.write(content)
```

#### Pure Reducer Functions

```python
def handle_user_request(state: dict, action: dict) -> dict:
    """Pure function: process user request"""

    # Don't modify input state
    new_state = {**state}

    # Add request to history
    new_state["messages"] = [
        *state["messages"],
        {"role": "user", "content": action["request"]}
    ]

    # Create plan (LLM call is only I/O)
    plan = llm.create_plan(
        persona=state["persona"],
        task=action["request"],
        context=state["messages"]
    )

    new_state["plan"] = plan
    new_state["status"] = "planning_complete"

    return new_state

def handle_tool_call(state: dict, action: dict) -> dict:
    """Pure function: execute tool call"""

    new_state = {**state}

    # Execute tool (I/O side effect only)
    result = execute_tool(action["tool"], action["parameters"])

    # Update state
    new_state["tool_calls"] = [
        *state["tool_calls"],
        {
            "tool": action["tool"],
            "parameters": action["parameters"],
            "result": result,
            "timestamp": now()
        }
    ]

    # Update token usage
    new_state["token_usage"]["total"] += count_tokens(result)

    return new_state
```

#### Replay & Debugging

```python
def replay_session(session_log_path: str, up_to_step: int = None):
    """Replay session from external state"""

    # Load initial state
    state = load_session_log(session_log_path)

    # Extract all actions
    actions = extract_actions_from_log(state)

    # Replay actions one by one
    current_state = create_initial_state()

    for i, action in enumerate(actions):
        if up_to_step and i >= up_to_step:
            break

        print(f"Step {i+1}: {action['type']}")
        current_state = agent.reduce(current_state, action)

    return current_state

# Debug specific step
state_at_step_5 = replay_session("SESSION_LOG.md", up_to_step=5)
print(f"State at step 5: {state_at_step_5}")
```

#### Testing

```python
def test_agent_reducer():
    """Test as pure function"""

    # Arrange: Create test state
    state = {
        "session_id": "test-123",
        "persona": "backend-architect",
        "messages": [],
        "tool_calls": [],
        "token_usage": {"total": 0}
    }

    action = {
        "type": "tool_call",
        "tool": "create_endpoint",
        "parameters": {"method": "POST", "path": "/api/auth"}
    }

    # Act: Call reducer
    new_state = agent.reduce(state, action)

    # Assert: Check new state
    assert len(new_state["tool_calls"]) == 1
    assert new_state["tool_calls"][0]["tool"] == "create_endpoint"
    assert new_state["token_usage"]["total"] > 0

    # Original state unchanged (pure function)
    assert len(state["tool_calls"]) == 0
```

#### Resume from Checkpoint

```python
def resume_session(session_log_path: str, additional_context: str = None):
    """Resume from external state"""

    # Load last state
    state = load_session_log(session_log_path)

    # Verify can resume
    if state["status"] != "paused":
        raise ValueError("Can only resume paused sessions")

    # Add resume context
    if additional_context:
        state["messages"].append({
            "role": "system",
            "content": f"Resuming: {additional_context}"
        })

    # Continue execution (stateless)
    new_state = agent.execute(session_log_path, {
        "type": "resume",
        "context": additional_context
    })

    return new_state
```

### Advantages

1. **Transparent state**: Everything in SESSION_LOG.md
2. **Easy resume**: Just load file and continue
3. **Full replay**: Reconstruct session from log
4. **Deterministic**: Same state + action = same result
5. **Testable**: Pure functions, no mocking needed
6. **Debuggable**: Inspect state at any point
7. **Platform-agnostic**: State is just a file

### Example: Complete Stateless Flow

```python
# 1. Initialize (create external state)
session_log = create_session_log("backend-task")

# 2. Execute (stateless)
agent = StatelessAgent(persona="backend-architect")
result = agent.execute(session_log, {
    "type": "user_request",
    "request": "Create auth endpoint"
})

# 3. Pause (state already external)
# No need to save—state is in SESSION_LOG.md!

# 4. Resume (load external state)
result = agent.execute(session_log, {
    "type": "resume"
})

# 5. Debug (replay from external state)
state_at_error = replay_session(session_log, up_to_step=5)
print(f"State when error occurred: {state_at_error}")
```

---

## Related Factors

- **Factor 3**: Own Your Context Window (context is part of external state)
- **Factor 5**: Unify Execution/Business State (SESSION_LOG is external state)
- **Factor 6**: Launch/Pause/Resume (external state enables resume)
- **Factor 11**: Trigger from Anywhere (stateless = platform-agnostic)

---

**Version**: 0.4.0
**Status**: ✅ Fully implemented via externalized SESSION_LOG
**See Also**: `templates/SESSION_LOG.md`, `implementations/factor-05-state-management/`
