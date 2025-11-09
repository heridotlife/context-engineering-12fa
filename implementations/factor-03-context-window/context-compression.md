# Context Compression (Factor 3 Implementation)

> **Auto-summarization strategies to prevent token budget exhaustion**

---

## Overview

Contract: Agents must actively manage context size through automatic summarization, preventing token budget exhaustion while maintaining performance.

---

## Auto-Summarization

### Trigger

When context token utilization reaches **50%** of the token budget.

```python
if (current_tokens / token_budget) >= 0.50:
    trigger_auto_summarization()
```

### Strategy: "Simple" Summarization

LLM-based compression in a single pass:

1. **Extract conversational messages**
   - Exclude: System prompts, tool schemas, SESSION_LOG
   - Include: User/assistant message pairs, tool results

2. **Send to LLM with prompt**:
   ```
   Summarize the following conversation, preserving:
   - Key decisions made
   - Unresolved issues
   - Current task state
   Be concise.
   ```

3. **Replace oldest messages with summary**
   - Keep latest 2-3 messages intact (immediate context)
   - Insert summary as new message at beginning

4. **Log action to SESSION_LOG**:
   ```
   Summarized 8 messages → 1 summary (saved ~1,200 tokens)
   ```

---

## Protection Rules

**NEVER summarize:**
- System prompts or persona definitions
- Most recent 2-3 messages (preserve immediate context)
- SESSION_LOG.md content
- Active state checkpoints
- User-provided constraints or requirements

**Why**: These elements are critical for maintaining agent coherence and task continuity.

---

## Selective Tool Post-Processing

**Principle**: Compress token-heavy tool outputs immediately after retrieval; preserve small, structured results.

### Compress/Summarize

| Tool Type | Strategy | Example |
|-----------|----------|---------|
| **Web search results** | Keep title + snippet + URL only | Discard full HTML |
| **File reads** | If >500 lines: summary + line ranges | Discard full content unless needed |
| **Database queries** | Keep row count + sample rows | Discard full result set if >100 rows |
| **API responses** | Keep status + key fields | Discard verbose metadata |

### Preserve As-Is

| Data Type | Reason | Threshold |
|-----------|--------|-----------|
| **Tool errors** | Full error for debugging | Always keep |
| **Small results** | Already compact | <200 tokens |
| **Structured data** | Need for validation | JSON/YAML <500 tokens |
| **Debug verbosity** | User requested | `context.verbosity=debug` |

---

## Example: Before/After

### Before Compression (1,200 tokens)

```
User: Can you analyze the latest sales data?
Assistant: I'll fetch the sales data from the database.
Tool: database_query() → [1000 rows of data...]
Assistant: Here's the analysis: ...
User: What about Q3 specifically?
Assistant: Let me filter for Q3...
Tool: database_query(quarter=3) → [300 rows...]
Assistant: Q3 shows...
User: Compare to Q2?
Assistant: I'll fetch Q2 data...
```

### After Compression (400 tokens)

```
Summary: User requested sales analysis. Fetched full dataset (1000 rows),
analyzed Q3 (300 rows showing 15% growth), now comparing to Q2.

User: Compare to Q2?
Assistant: I'll fetch Q2 data...
```

**Savings**: 800 tokens (67% reduction)

---

## Implementation Pseudocode

```python
def auto_summarize(session):
    # Calculate utilization
    utilization = session["token_usage"]["total"] / session["token_usage"]["budget"]

    if utilization < 0.50:
        return  # No action needed

    # Extract messages (exclude recent 3)
    messages_to_summarize = session["messages"][:-3]
    recent_messages = session["messages"][-3:]

    # Generate summary
    summary_prompt = f"""
    Summarize this conversation, preserving key decisions,
    unresolved issues, and current task state. Be concise.

    {format_messages(messages_to_summarize)}
    """

    summary = llm_call(summary_prompt)

    # Replace old messages with summary
    session["messages"] = [
        {"role": "assistant", "content": f"[SUMMARY]: {summary}"}
    ] + recent_messages

    # Log action
    tokens_saved = count_tokens(messages_to_summarize) - count_tokens(summary)
    log_to_session_log(
        f"Summarized {len(messages_to_summarize)} messages → 1 summary "
        f"(saved ~{tokens_saved} tokens)"
    )

    return tokens_saved
```

---

## Best Practices

1. **Summarize early** (50% threshold) to avoid emergency trimming at 80%
2. **Preserve recent context** (latest 2-3 messages) for coherence
3. **Log all summarizations** to SESSION_LOG for auditability
4. **Compress tool outputs** immediately after retrieval
5. **Respect user verbosity preferences** (don't compress in debug mode)

---

## Monitoring

Track effectiveness in SESSION_LOG:

```markdown
## Token Usage @ 2025-11-09T10:35:22
- Pre-summarization: 4,200 / 8,000 (52.5%)
- Post-summarization: 2,800 / 8,000 (35%)
- Savings: 1,400 tokens (33% reduction)
```

---

**Version**: 0.4.0
**Factor**: 3.1 (Context Compression)
**Related**: `context-trimming.md`, `health-monitoring.md`
