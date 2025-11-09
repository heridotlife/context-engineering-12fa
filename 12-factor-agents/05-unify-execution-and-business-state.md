# Factor 5: Unify Execution and Business State

> **Source**: [HumanLayer 12 Factor Agents](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-05-unify-execution-state.md)

---

## Overview

**Core Principle**: Store execution state (agent progress, context, decisions) alongside business state (domain data, entities, relationships) in a single unified source of truth.

## The Problem

Traditional approaches separate:
- **Execution state**: Stored in orchestrator/framework (agent memory, conversation history)
- **Business state**: Stored in application database (users, orders, inventory)

This separation causes:
- State synchronization issues
- Difficult debugging (can't replay agent decisions)
- Poor observability (execution state is opaque)
- Resume failures (execution state lost between sessions)

## The Solution

**Single Source of Truth**: Store both execution and business state together, making the entire agent run inspectable, replayable, and resumable.

### Example Structure

```python
{
    # Business state
    "order_id": "123",
    "customer": "Alice",
    "items": [...],
    "total": 150.00,

    # Execution state
    "agent_session_id": "abc-def",
    "current_step": "awaiting_payment",
    "decisions_made": [
        {"step": "validate_cart", "decision": "approved", "reasoning": "..."},
        {"step": "check_inventory", "decision": "in_stock", "reasoning": "..."}
    ],
    "next_action": "send_payment_link",
    "context_summary": "Customer wants express shipping..."
}
```

---

## 🎯 Our Implementation

### Location

**Full implementation** in:
- `implementations/factor-05-state-management/` - Complete state management system
- `templates/SESSION_LOG.md` - Session state template
- `schemas/state-schema.json` - Unified state schema

### How It Works

We implement unified state through the **SESSION_LOG.md** system:

#### SESSION_LOG.md Structure

```markdown
## Session: [id] @ [timestamp]
session_date: 2025-11-09
persona: backend-architect
model: claude-sonnet-4-5
context_budget: 8000 tokens

## Task (Business Context)
User request: "Create a REST API endpoint for user authentication"
Project: my-app-backend
Language: Python 3.12 + FastAPI

## Plan (Execution State)
1. ✅ Design endpoint schema (POST /api/v1/auth/login)
2. ✅ Implement authentication logic with JWT
3. ⏳ Add rate limiting middleware
4. ⏸️ Write integration tests

## Reasoning (Execution Decisions)
- Decision: Use JWT over sessions → reasoning: API needs to scale horizontally
- Constraint: Token budget at 45% → action: trim old context
- Tool selection: FastAPI + python-jose → reasoning: project already uses FastAPI

## Tool Calls (Execution + Results)
1. create_endpoint(method="POST", path="/api/v1/auth/login")
   → SUCCESS: Created in src/routes/auth.py:15

2. add_middleware(name="rate_limiter", config={"limit": "10/minute"})
   → ERROR: Missing redis connection

3. setup_redis(host="localhost", port=6379)
   → SUCCESS: Redis configured in config/redis.py:8

## Token Usage @ 14:32:18 (Execution Metrics)
- LLM Call #3: input=420, output=180, total=600
- Cumulative: 2,450 / 8,000 (30.6%)

## Health Check @ 14:32:19 (Execution Health)
- Token utilization: 30.6% ✅
- Message count: 8 messages ✅
- Compression needed: NO
- Action taken: None
```

#### State Schema

```json
// schemas/state-schema.json
{
  "session": {
    "session_id": "uuid",
    "session_date": "YYYY-MM-DD",
    "session_timestamp": "ISO 8601",
    "persona": "persona-name",
    "model": "model-id"
  },

  "business_context": {
    "task": "user request text",
    "project": "project name",
    "language": "tech stack",
    "artifacts": ["files created/modified"]
  },

  "execution_state": {
    "plan": [
      {"step": "description", "status": "pending|in_progress|completed|paused"}
    ],
    "decisions": [
      {"decision": "what", "reasoning": "why", "timestamp": "when"}
    ],
    "tool_calls": [
      {"tool": "name", "params": {}, "result": {}, "timestamp": "when"}
    ]
  },

  "execution_metrics": {
    "token_usage": {"input": 0, "output": 0, "total": 0, "budget": 8000},
    "health_checks": [
      {"timestamp": "when", "utilization": 0.3, "action": "none"}
    ]
  }
}
```

#### Unified State Access

```python
class SessionState:
    """Unified interface to both execution and business state"""

    def __init__(self, session_log_path):
        self.session_log = self.load_session_log(session_log_path)

    # Business state accessors
    def get_task(self) -> str:
        return self.session_log["business_context"]["task"]

    def get_artifacts(self) -> List[str]:
        return self.session_log["business_context"]["artifacts"]

    # Execution state accessors
    def get_current_step(self) -> Dict:
        plan = self.session_log["execution_state"]["plan"]
        return next((s for s in plan if s["status"] == "in_progress"), None)

    def get_decisions(self) -> List[Dict]:
        return self.session_log["execution_state"]["decisions"]

    def get_tool_history(self) -> List[Dict]:
        return self.session_log["execution_state"]["tool_calls"]

    # Unified operations
    def add_decision(self, decision: str, reasoning: str):
        """Record both execution decision and business impact"""
        self.session_log["execution_state"]["decisions"].append({
            "decision": decision,
            "reasoning": reasoning,
            "timestamp": now()
        })
        self.save()

    def complete_step(self, step: str, artifacts: List[str]):
        """Update both execution progress and business artifacts"""
        # Update execution state
        for s in self.session_log["execution_state"]["plan"]:
            if s["step"] == step:
                s["status"] = "completed"

        # Update business state
        self.session_log["business_context"]["artifacts"].extend(artifacts)
        self.save()

    def save(self):
        """Persist unified state"""
        write_session_log(self.session_log)
```

### Advantages

1. **Single source of truth**: Both execution and business state in one place
2. **Full observability**: See exactly what agent decided and why
3. **Replayability**: Reconstruct entire session from SESSION_LOG
4. **Resumability**: Pause/resume with complete state
5. **Debuggability**: Inspect decisions, tool calls, reasoning
6. **Auditability**: Complete audit trail for compliance

### Lifecycle Management

```python
# Initialize session (create unified state)
session = create_session_log(task="Create auth endpoint")

# During execution (update unified state)
session.add_decision("Use JWT", "Need horizontal scaling")
session.complete_step("design_schema", artifacts=["schema.json"])

# Pause (state persisted automatically)
session.pause(reason="Waiting for human approval")

# Resume (load unified state)
session = load_session_log(session_id="abc-def")
session.resume()

# Archive (move to long-term storage)
archive_session_log(session_id="abc-def", dest=".session-archive/")
```

---

## Related Factors

- **Factor 3**: Own Your Context Window (SESSION_LOG stores context state)
- **Factor 6**: Launch/Pause/Resume (unified state enables resume)
- **Factor 12**: Stateless Reducer (SESSION_LOG is externalized state)

---

**Version**: 0.4.0
**Status**: ✅ Fully implemented via SESSION_LOG.md system
**See Also**: `implementations/factor-05-state-management/`, `templates/SESSION_LOG.md`
