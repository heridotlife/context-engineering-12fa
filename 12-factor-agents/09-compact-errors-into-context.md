# Factor 9: Compact Errors into Context Window

> **Source**: [HumanLayer 12 Factor Agents](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-09-compact-errors.md)

---

## Overview

This factor addresses how LLMs can **recover from tool failures** through error-driven learning. The core concept involves capturing error messages within the agent's context window so the model can adjust subsequent actions.

## Key Concept

Rather than terminating on first error, agents should:

1. **Capture errors** in the context window
2. **Allow LLM to read** the error message
3. **Let LLM adjust** subsequent tool calls based on error
4. **Continue execution** with updated strategy

This creates self-healing capability through error analysis.

## Implementation Pattern

### Event Thread with Errors

```python
# Maintain event thread that logs both success and failures
context = {
    "messages": [...],
    "events": [
        {"tool": "create_endpoint", "status": "success", "result": {...}},
        {"tool": "add_middleware", "status": "error", "error": "Missing redis connection"},
        {"tool": "setup_redis", "status": "success", "result": {...}},
        {"tool": "add_middleware", "status": "success", "result": {...}}  # Retry succeeded
    ]
}
```

When a tool fails, the error gets **formatted and appended** to the context rather than terminating execution. This enables the LLM to "read the error message and figure out what to change in a subsequent tool call."

## Error Handling with Limits

A practical enhancement introduces a **consecutive error counter**, typically capping retry attempts at around 3 before triggering escalation:

```python
if session["consecutive_errors"] >= 3:
    # Escalate to human or pause
    session.pause(reason="Error threshold exceeded")
```

As the documentation notes: **"Hitting some consecutive-error-threshold might be a great place to escalate to a human, whether by model decision or via deterministic takeover of the control flow."**

## Preventing Error Cycles

The guide warns that excessive error recovery can cause agents to "spin out and might repeat the same error over and over again." Solutions include:

- Restructuring error representation (more detail)
- Removing stale context (trim old errors)
- Implementing smaller, more focused agents

---

## 🎯 Our Implementation

### Location

**Full implementation** in:
- `implementations/factor-09-error-handling/` - Complete error compaction system
- `implementations/factor-03-context-window/context-trimming.md` - Error pruning strategies
- `core/AGENTIC_GUIDE.md` (§4) - Error handling protocol

### How It Works

We implement error compaction with three strategies:

#### 1. Error Capture & Formatting

```python
def handle_tool_error(session, tool_call, error):
    """Capture and format error for context"""

    # Extract relevant error info
    error_summary = {
        "tool": tool_call["tool"],
        "parameters": tool_call["parameters"],
        "error_type": type(error).__name__,
        "error_message": str(error),
        "timestamp": now(),
        "suggested_fix": infer_fix(error)  # Heuristic hints
    }

    # Compact representation (save tokens)
    compact_error = f"""
Tool: {error_summary['tool']} FAILED
Error: {error_summary['error_type']} - {error_summary['error_message'][:100]}
Hint: {error_summary['suggested_fix']}
"""

    # Add to context
    session.add_message({
        "role": "system",
        "content": compact_error
    })

    # Track consecutive errors
    session.consecutive_errors += 1

    # Log full error to SESSION_LOG (not in context)
    session.log_error(error_summary)

    return error_summary
```

#### 2. Error Recovery Loop

```python
def execute_with_error_recovery(session, step, max_retries=3):
    """Execute step with automatic error recovery"""

    for attempt in range(max_retries):
        try:
            # Attempt execution
            result = execute_tool(step["tool"], step["parameters"])

            # Success! Reset error counter
            session.consecutive_errors = 0
            return result

        except Exception as error:
            # Capture error in context
            error_summary = handle_tool_error(session, step, error)

            # Check if we should escalate
            if session.consecutive_errors >= max_retries:
                session.pause(
                    reason=f"Error threshold exceeded: {error_summary['error_message']}"
                )
                return {
                    "status": "paused",
                    "error": error_summary,
                    "action": "escalate_to_human"
                }

            # Let LLM see error and adjust
            adjusted_step = llm.adjust_after_error(
                original_step=step,
                error=error_summary,
                attempt=attempt + 1
            )

            # Log retry
            session.log(f"Retry {attempt + 1}/{max_retries} with adjusted parameters")

            # Next iteration will try adjusted step
            step = adjusted_step

    # Should never reach here (max_retries check above)
    return {"status": "failed", "error": "Max retries exceeded"}
```

#### 3. Error Pruning (Save Tokens)

```python
def prune_stale_errors(session):
    """Remove old/resolved errors from context to save tokens"""

    messages = session.messages
    pruned_messages = []

    for i, msg in enumerate(messages):
        # Is this an error message?
        if msg["role"] == "system" and "FAILED" in msg["content"]:
            # Was it followed by a successful retry?
            if i + 2 < len(messages):
                next_tool = messages[i + 2]
                if next_tool.get("status") == "success":
                    # Skip this error (resolved)
                    continue

        pruned_messages.append(msg)

    session.messages = pruned_messages
```

#### 4. Smart Error Formatting

```python
def infer_fix(error) -> str:
    """Provide context-aware hints based on error type"""

    error_type = type(error).__name__
    error_msg = str(error).lower()

    # Pattern matching for common errors
    if "connection" in error_msg or "refused" in error_msg:
        return "Check if service is running and connection string is correct"

    elif "authentication" in error_msg or "unauthorized" in error_msg:
        return "Verify credentials/tokens are valid and not expired"

    elif "not found" in error_msg or "404" in error_msg:
        return "Check if resource exists or path is correct"

    elif "timeout" in error_msg:
        return "Service may be slow, consider increasing timeout or checking load"

    elif "permission" in error_msg or "forbidden" in error_msg:
        return "Check if agent has necessary permissions for this action"

    elif error_type == "JSONDecodeError":
        return "Response may not be valid JSON, check API response format"

    else:
        return "Review error message and adjust parameters accordingly"
```

#### 5. Error Compaction in SESSION_LOG

```markdown
## Errors @ 14:35:12

### Error #1 (RECOVERED)
- Tool: add_middleware("rate_limiter")
- Error: ConnectionRefusedError - Redis connection refused
- Hint: Check if service is running
- Resolution: Ran setup_redis() successfully, then retried

### Error #2 (RECOVERED)
- Tool: create_endpoint(path="/api/v1/auth")
- Error: ValidationError - Missing required field 'handler'
- Hint: Review error message and adjust parameters
- Resolution: Added handler='authenticate', retry succeeded

### Error #3 (ESCALATED)
- Tool: deploy_to_production()
- Error: PermissionError - Insufficient permissions
- Hint: Check if agent has necessary permissions
- Resolution: PAUSED - Human approval required
- Consecutive errors: 3 → THRESHOLD EXCEEDED
```

### Token Savings

| Strategy | Before | After | Savings |
|----------|--------|-------|---------|
| **Compact formatting** | 250 tokens/error | 50 tokens/error | 80% |
| **Prune resolved errors** | N errors × 50 | Only active errors | 60-90% |
| **Smart hints** | Full stack traces | Actionable hints | 90% |
| **Combined** | 2500 tokens (10 errors) | 300 tokens (6 active) | 88% |

### Example: Error Recovery Flow

```python
# Attempt 1: FAIL
result = execute_tool("add_middleware", {"name": "rate_limiter"})
# Error: ConnectionRefusedError - Redis connection refused
# → Add to context: "Tool: add_middleware FAILED\nError: ConnectionRefusedError\nHint: Check if service is running"

# LLM sees error, adjusts strategy
adjusted = llm.adjust_after_error()
# → "Need to setup Redis first"

# Attempt 2: Setup dependency
result = execute_tool("setup_redis", {"host": "localhost"})
# → SUCCESS

# Attempt 3: Retry original (automatic)
result = execute_tool("add_middleware", {"name": "rate_limiter"})
# → SUCCESS

# Prune resolved error from context (save tokens)
prune_stale_errors(session)
```

---

## Related Factors

- **Factor 3**: Own Your Context Window (error compaction saves tokens)
- **Factor 5**: Unify Execution/Business State (log full errors to SESSION_LOG)
- **Factor 7**: Contact Humans with Tool Calls (escalate on error threshold)
- **Factor 8**: Own Your Control Flow (deterministic error handling)

---

**Version**: 0.4.0
**Status**: ✅ Fully implemented with error compaction + recovery
**See Also**: `implementations/factor-09-error-handling/`, `implementations/factor-03-context-window/`
