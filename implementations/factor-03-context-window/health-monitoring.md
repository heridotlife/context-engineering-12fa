# Context Health Monitoring (Factor 3 Implementation)

> **Continuous context quality checks and remediation**

---

## Overview

Contract: Agents must monitor context health and take remediation actions when thresholds are exceeded.

---

## Health Metrics

### 1. Token Utilization
- **Calculation**: `(current_tokens / token_budget) * 100`
- **Thresholds**:
  - 50% (WARN): Trigger auto-summarization
  - 80% (CRITICAL): Force trim oldest messages
- **Frequency**: Check before every LLM call

### 2. Message Count
- **Threshold**: >20 messages → Consider summarization
- **Action**: Trim if >30 messages regardless of token count

### 3. Contradiction Detection
- Check for conflicting instructions in context
- Example: "Use Python" vs "Use Node.js" in same session
- Action: Request user clarification

### 4. Staleness
- Check if context references outdated information
- Example: "As of 2023" when session_date is 2025
- Action: Note potential staleness in SESSION_LOG

### 5. Completeness
- Verify required fields present (persona, task, session_id)
- Action: Request missing information before proceeding

---

## Health Check Frequency

- **Session Init**: Full health check at start
- **Before LLM Calls**: Token utilization check
- **After Tool-Heavy Operations**: After 3+ consecutive tool calls
- **On-Demand**: When user requests health check or trace

---

## Remediation Actions

| Threshold | Condition | Action | Log Entry |
|-----------|-----------|--------|-----------|
| 50% | Token utilization | Trigger summarization | "Health check: 50% tokens → Summarized" |
| 80% | Token utilization | Force trim messages | "Health check: 80% tokens → Force trim" |
| >20 msgs | Message count | Consider summarization | "Health check: 22 messages → Summarized" |
| >30 msgs | Message count | Force trim regardless of tokens | "Health check: 32 messages → Force trim" |
| Conflict | Contradictions detected | Request user clarification | "Health check: Conflict detected → Clarify" |
| Missing | Required field absent | Block execution until provided | "Health check: Missing persona → Request" |

---

## Implementation

```python
def context_health_check(state):
    """Run comprehensive health check and take remediation actions."""

    # Calculate metrics
    token_percent = (state.token_usage.total / state.token_usage.budget) * 100
    message_count = len(state.messages)

    # Token utilization checks
    if token_percent >= 80:
        trim_messages(state, force=True)
        log("Health check: 80% tokens → Force trim")
    elif token_percent >= 50:
        summarize_context(state)
        log("Health check: 50% tokens → Summarized")

    # Message count checks
    if message_count > 30:
        trim_messages(state, force=True)
        log("Health check: >30 messages → Force trim")
    elif message_count > 20:
        summarize_context(state)
        log("Health check: >20 messages → Consider summarization")

    # Contradiction detection
    conflicts = detect_contradictions(state)
    if conflicts:
        log(f"Health check: Conflicts detected → {conflicts}")
        request_user_clarification(conflicts)

    # Completeness check
    required_fields = ["persona", "task", "session_id"]
    missing = [f for f in required_fields if f not in state]
    if missing:
        log(f"Health check: Missing fields → {missing}")
        raise MissingContextError(missing)

    # Staleness check (basic)
    check_date_references(state)

    return {
        "status": "healthy" if token_percent < 50 else "warning",
        "token_utilization": token_percent,
        "message_count": message_count,
        "conflicts": conflicts,
        "missing_fields": missing
    }
```

---

## Logging Format

```markdown
## Health Check @ 2025-11-09T10:35:22

- **Token utilization**: 52% (WARN) → Triggered summarization
- **Message count**: 18 messages
- **Contradictions**: None detected
- **Staleness**: None detected
- **Completeness**: All required fields present
- **Action taken**: Summarized 12 messages → 1 summary (saved ~1,100 tokens)
- **New utilization**: 38% (healthy)
```

---

**Version**: 0.4.0
**Factor**: 3.5 (Health Monitoring)
**Related**: `context-compression.md`, `context-trimming.md`
