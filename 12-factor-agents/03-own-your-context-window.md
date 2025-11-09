# Factor 3: Own Your Context Window

> **Source**: [HumanLayer 12 Factor Agents](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-03-own-your-context-window.md)

---

## Overview

**Core Principle**: "At any given point, your input to an LLM is 'here's what happened so far, what's next.'"

Factor 3 emphasizes **active context management** rather than passive accumulation. Rather than relying solely on standard message formats, you should develop custom context structures tailored to your specific use case.

## Key Concepts

### Context as a Resource

The context window is a finite, precious resource that requires active management:

- **Don't just append** - Actively curate what goes in
- **Summarize strategically** - Compress old context while preserving critical information
- **Prioritize relevance** - Keep recent and important context, trim the rest

### Custom Context Structures

Standard message arrays (`[{role, content}]`) aren't always sufficient. Consider custom structures:

- Separate "working memory" from "long-term memory"
- Maintain structured state (not just text)
- Use hierarchical context (summary → details)

---

## 🎯 Our Implementation

### Location

**Full production implementation** in:
- `implementations/factor-03-context-window/` - Complete context engineering suite
- `core/AGENTIC_GUIDE.md` (§2) - Context engineering requirements

### How It Works

We implement Factor 3 with six integrated strategies:

#### 1. Context Compression (`context-compression.md`)

Auto-summarization triggered at 50% token threshold:

```python
def auto_summarize(session):
    if session["token_usage"]["total"] > session["token_budget"] * 0.5:
        # Summarize messages older than 10 turns
        old_messages = session["messages"][:-10]
        summary = llm.summarize(old_messages)
        session["messages"] = [{"role": "system", "content": summary}] + session["messages"][-10:]
```

#### 2. Context Trimming (`context-trimming.md`)

Proactive pruning before every LLM call:

```python
def trim_context(messages):
    # Keep system prompt + last 2-3 user/assistant turns
    return [messages[0]] + messages[-6:]  # Keep last 3 exchanges
```

#### 3. Context Isolation (`context-isolation.md`)

Separate exposed vs isolated state:

```python
{
    "messages": [],           # Exposed to LLM
    "context": {              # Isolated scratchpad
        "session_date": "2025-11-09",
        "persona": "backend-architect",
        "token_usage": {...}
    },
    "tool_outputs": {...},    # Isolated: raw + summaries
    "images": [],             # Isolated: binary data
}
```

#### 4. Health Monitoring (`health-monitoring.md`)

Continuous quality checks:

```python
def context_health_check(session):
    """Run before each LLM call"""
    checks = {
        "token_utilization": calculate_usage(session),
        "message_count": len(session["messages"]),
        "compression_needed": should_compress(session),
        "trim_recommended": should_trim(session)
    }

    if checks["compression_needed"]:
        auto_summarize(session)
    if checks["trim_recommended"]:
        session["messages"] = trim_context(session["messages"])

    return checks
```

#### 5. Temporal Awareness (`temporal-awareness.md`)

Date/time for version checks + **auto web search**:

```python
def initialize_session():
    session = {
        "session_date": get_local_date(),      # "2025-11-09"
        "session_timestamp": get_iso_timestamp(),  # ISO 8601
        "model_knowledge_cutoff": "2025-01-01"
    }
    return session

def should_trigger_web_search(query, session):
    """Detect if web search needed for freshness"""
    latest_keywords = ["latest", "newest", "current", "recent"]
    version_keywords = ["version", "release", "update"]
    security_keywords = ["CVE", "vulnerability", "security"]

    # Trigger search if query needs fresh data
    return any(kw in query.lower() for kw in
               latest_keywords + version_keywords + security_keywords)
```

#### 6. Observability (`observability.md`)

Token tracking and reasoning traces:

```python
def log_llm_call(session, request, response):
    session["token_usage"]["input"] += count_tokens(request)
    session["token_usage"]["output"] += count_tokens(response)
    session["token_usage"]["total"] = (
        session["token_usage"]["input"] +
        session["token_usage"]["output"]
    )

    log_to_session_log(session, {
        "timestamp": now(),
        "tokens": session["token_usage"],
        "utilization": session["token_usage"]["total"] / session["token_budget"]
    })
```

### Token Efficiency Results

| Strategy | Trigger | Savings | Trade-off |
|----------|---------|---------|-----------|
| **Trimming** | Every LLM call | 20-40% | Lose old context |
| **Summarization** | 50% tokens | 30-60% | Lose detail |
| **Isolation** | Session init | 10-20% | Complexity |
| **Combined** | Proactive | 50-70% | Best practice |

### Minimal Integration

```python
# 1. Initialize session
session = {
    "session_date": get_local_date(),
    "session_timestamp": get_iso_timestamp(),
    "messages": [],
    "token_usage": {"input": 0, "output": 0, "total": 0, "budget": 8000}
}

# 2. Before each LLM call
context_health_check(session)  # Auto-trim/summarize if needed

# 3. After LLM call
session["token_usage"]["total"] += count_tokens(response)
log_to_session_log(session, response)
```

---

## Related Factors

- **Factor 5**: Unify Execution/Business State (SESSION_LOG stores context state)
- **Factor 9**: Compact Errors into Context (error compaction saves tokens)
- **Factor 12**: Stateless Reducer (externalized state enables isolation)

---

**Version**: 0.4.0
**Status**: ✅ Production-ready full implementation
**See Also**: `implementations/factor-03-context-window/` for detailed procedures
