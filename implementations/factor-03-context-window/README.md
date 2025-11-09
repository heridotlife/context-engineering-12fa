# Factor 3: Own Your Context Window (Implementation)

> **12FA Principle**: "At any given point, your input to an LLM is 'here's what happened so far, what's next.'"
>
> This directory implements HumanLayer's Factor 3 with production-ready context engineering tools.

---

## Overview

Factor 3 emphasizes **active context management** rather than passive accumulation. Our implementation provides:

1. **Context Compression** - Auto-summarization at 50% token threshold
2. **Context Trimming** - Proactive message pruning before LLM calls
3. **Context Isolation** - Separate exposed vs isolated state
4. **Health Monitoring** - Continuous context quality checks
5. **Temporal Awareness** - Date/time for version checks, timestamps
6. **Observability** - Token tracking and reasoning traces

---

## Implementation Files

| File | Purpose | When to Load |
|------|---------|--------------|
| `context-compression.md` | Auto-summarization strategies | Token usage > 50% |
| `context-trimming.md` | Message pruning rules | Before every LLM call |
| `context-isolation.md` | State schema (exposed/isolated) | Session init |
| `health-monitoring.md` | `context_health_check()` | Session init, before LLM calls |
| `temporal-awareness.md` | Date/time + **auto web search** for latest info | Session init, query parsing |
| `observability.md` | Token tracking, traces | On-demand (trace=true) |

---

## Quick Start

### Minimal Implementation

```python
# 1. Initialize session
session = {
    "session_date": get_local_date(),  # YYYY-MM-DD
    "session_timestamp": get_iso_timestamp(),  # ISO 8601
    "messages": [],
    "token_usage": {"input": 0, "output": 0, "total": 0, "budget": 8000}
}

# 2. Before each LLM call
context_health_check(session)  # Auto-trim/summarize if needed

# 3. After LLM call
session["token_usage"]["total"] += count_tokens(response)
log_to_session_log(session, response)
```

### Full Implementation

See individual files for detailed procedures:
- **Compression**: `context-compression.md` (§1-3)
- **Trimming**: `context-trimming.md` (§1-2)
- **Health Checks**: `health-monitoring.md` (§1-5)

---

## Token Efficiency

| Strategy | Trigger | Savings | Trade-off |
|----------|---------|---------|-----------|
| **Trimming** | Every LLM call | 20-40% | Lose old context |
| **Summarization** | 50% tokens | 30-60% | Lose detail |
| **Isolation** | Session init | 10-20% | Complexity |
| **Combined** | Proactive | 50-70% | Best practice |

---

## Original 12FA Reference

**Source**: https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-03-own-your-context-window.md

**Key Quote**:
> "Rather than relying solely on standard message formats, you should develop custom context structures tailored to your specific use case."

Our implementation provides those custom structures as reusable patterns.

---

**Version**: 0.4.0
**Factor**: 3 (Own Your Context Window)
**Status**: Production-ready
