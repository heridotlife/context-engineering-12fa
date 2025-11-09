# Temporal Awareness (Factor 3 Implementation)

> **Date/time awareness for version checks, dependency updates, and automatic web search triggers**

---

## Overview

Contract: Agents must be aware of current date/time to make informed decisions about:
- **Version checks** (is this dependency outdated?)
- **Dependency updates** (what's the latest version?)
- **Knowledge freshness** (is my training data current?)
- **Web search triggers** (when to search for latest info)

---

## Core Capabilities

### 1. Session Date/Time Recording

At session initialization, record:

```markdown
session_date: 2025-11-09           # Local system date (YYYY-MM-DD)
session_timestamp: 2025-11-09T10:30:00-05:00  # ISO 8601 with timezone
session_timezone: America/New_York  # Timezone identifier
model_knowledge_cutoff: 2025-01     # Model training cutoff
```

**Source**: Injected by runtime environment (Claude, Gemini, Copilot)

---

### 2. Knowledge Freshness Detection

**Trigger web search when**:

| Scenario | Detection | Action |
|----------|-----------|--------|
| **Dependency version** | User asks "latest version of X" | ✅ Web search: "X latest version 2025" |
| **Recent release** | Topic mentions dates ≥ model cutoff | ✅ Web search: "X release notes 2025" |
| **Breaking changes** | Major version bump (2.x → 3.x) | ✅ Web search: "X v3 migration guide" |
| **Security advisory** | CVE or vulnerability mention | ✅ Web search: "X CVE 2025" |
| **Best practices** | User asks "current best practice" | ✅ Web search: "X best practices 2025" |
| **Framework updates** | Framework name + "update/latest" | ✅ Web search: "framework latest 2025" |

**Example**:
```
User: "What's the latest version of React?"
Agent:
  1. Checks: session_date (2025-11-09) vs model_knowledge_cutoff (2025-01)
  2. Triggers: WebSearch("React latest version November 2025")
  3. Returns: "React 19.x (released Oct 2025) is the latest..."
```

---

### 3. Automatic Web Search Protocol

#### When to Search

```python
def should_trigger_web_search(query, session_date, model_cutoff):
    """Determine if web search is needed for freshness."""

    # Patterns that indicate need for latest info
    latest_keywords = [
        "latest", "newest", "current", "recent",
        "up to date", "as of", "2025", "2024"
    ]

    version_keywords = [
        "version", "release", "update", "upgrade",
        "migration", "changelog", "breaking change"
    ]

    security_keywords = [
        "vulnerability", "CVE", "security", "patch",
        "exploit", "advisory"
    ]

    # Check if query mentions recent dates
    query_mentions_recent_date = parse_date_from_query(query) >= model_cutoff

    # Check if query asks for latest info
    asks_for_latest = any(keyword in query.lower() for keyword in latest_keywords)

    # Check if version-related
    version_related = any(keyword in query.lower() for keyword in version_keywords)

    # Check if security-related
    security_related = any(keyword in query.lower() for keyword in security_keywords)

    return (
        query_mentions_recent_date or
        asks_for_latest or
        (version_related and not has_recent_cached_data(query)) or
        security_related
    )
```

#### Search Query Construction

```python
def construct_search_query(user_query, session_date):
    """Build optimal search query with temporal context."""

    # Extract key terms
    key_terms = extract_entities(user_query)

    # Add temporal qualifier if not present
    year = session_date.split('-')[0]  # "2025-11-09" → "2025"
    month = get_month_name(session_date)  # "November"

    if "latest" in user_query.lower():
        # "latest React version" → "React latest version November 2025"
        return f"{key_terms} latest {month} {year}"
    elif "version" in user_query.lower():
        # "React version" → "React version 2025"
        return f"{key_terms} {year}"
    elif "migration" in user_query.lower():
        # "migrate to X" → "X migration guide 2025"
        return f"{key_terms} migration guide {year}"
    else:
        # Generic: add year for freshness
        return f"{key_terms} {year}"
```

---

## Implementation: Auto Web Search

### Integration with AGENTIC_GUIDE.md

Add to **Execution Footer** (Step 4: Parse & Execute):

```markdown
### Step 4: Parse & Execute

1. **Parse user request**: Identify task objective, constraints, artifacts
2. **Check knowledge freshness**: If query requires latest info:
   - Compare session_date with model_knowledge_cutoff
   - If gap > 2 months OR query mentions "latest/current": Trigger web search
   - Log: "Knowledge may be outdated, searching web for latest info..."
3. **Execute web search** (if triggered):
   - Construct search query with temporal context
   - Execute WebSearch tool
   - Integrate results into response
4. **Build plan**: Multi-step breakdown (log to SESSION_LOG)
5. **Execute**: Follow persona workflow + operational constraints
6. **Monitor health**: Check tokens before each LLM call
7. **Update SESSION_LOG**: Tool calls, reasoning, checkpoints
```

---

## Usage Patterns

### Pattern 1: Dependency Version Check

```markdown
User: "What version of FastAPI should I use?"

Agent:
1. Detects: version-related query
2. Calculates: session_date (2025-11-09) - model_cutoff (2025-01) = 10 months
3. Triggers: WebSearch("FastAPI latest stable version November 2025")
4. Response: "FastAPI 0.115.0 (Nov 2025) is the latest stable version.
             Key changes since 0.110: [from search results]"
```

### Pattern 2: Framework Migration

```markdown
User: "How do I migrate from Next.js 14 to 15?"

Agent:
1. Detects: migration query
2. Triggers: WebSearch("Next.js 15 migration guide 2025")
3. Response: "Next.js 15 released in Oct 2025. Migration steps: [from search]"
```

### Pattern 3: Security Advisories

```markdown
User: "Are there any security issues with Express 4.x?"

Agent:
1. Detects: security-related query
2. Triggers: WebSearch("Express 4.x security vulnerabilities CVE 2025")
3. Response: "Latest advisories as of Nov 2025: [from search]"
```

### Pattern 4: Best Practices

```markdown
User: "What's the current best practice for React state management?"

Agent:
1. Detects: "current best practice" (temporal qualifier)
2. Triggers: WebSearch("React state management best practices 2025")
3. Response: "As of 2025, the recommended approaches are: [from search]"
```

---

## Configuration

### Enable/Disable Web Search

In `core/AGENTIC_GUIDE.md` or context object:

```json
{
  "temporal_awareness": {
    "enabled": true,
    "auto_web_search": true,
    "freshness_threshold_months": 2,
    "search_triggers": [
      "latest", "newest", "current", "version",
      "migration", "security", "CVE", "best practice"
    ]
  }
}
```

### Model Knowledge Cutoff

Set in context or detect automatically:

```python
# From environment/context
model_cutoff = context.get("model_knowledge_cutoff", "2025-01")

# Or detect from model metadata
if model_name == "claude-sonnet-4-5":
    model_cutoff = "2025-01"  # January 2025
elif model_name == "gpt-4o":
    model_cutoff = "2024-10"  # October 2024
```

---

## Logging

All web searches logged to SESSION_LOG:

```markdown
## Temporal Awareness @ 2025-11-09T10:35:22

- **Session date**: 2025-11-09
- **Model cutoff**: 2025-01
- **Gap**: 10 months
- **Web search triggered**: YES
- **Query**: "FastAPI latest version November 2025"
- **Reason**: User asked for "latest version" (gap > 2 months)
- **Results integrated**: YES
- **Cache TTL**: 24 hours
```

---

## Caching Strategy

**Prevent redundant searches**:

```python
web_search_cache = {
    "FastAPI latest version": {
        "results": "0.115.0",
        "fetched_at": "2025-11-09T10:30:00",
        "ttl": 86400  # 24 hours
    }
}

def execute_web_search(query):
    cache_key = query.lower().strip()
    cached = web_search_cache.get(cache_key)

    if cached and not is_expired(cached["fetched_at"], cached["ttl"]):
        log("Using cached web search result")
        return cached["results"]

    # Execute fresh search
    results = WebSearch(query)
    web_search_cache[cache_key] = {
        "results": results,
        "fetched_at": now(),
        "ttl": 86400
    }
    return results
```

---

## Best Practices

1. **Always prefer web search** for:
   - Dependency versions ("latest X", "X version")
   - Security advisories (CVE, vulnerabilities)
   - Recent releases (< 6 months old)
   - Breaking changes (major version bumps)

2. **Don't trigger search** for:
   - Fundamental concepts (unchanged over time)
   - Historical information (events before cutoff)
   - Project-specific code (not public)
   - User's own dependencies (check package.json instead)

3. **Combine sources**:
   - Model knowledge (fundamentals, architecture)
   - Web search (versions, releases, advisories)
   - User's codebase (current state)

4. **Be transparent**:
   - State when using web search: "Let me check the latest..."
   - Cite sources: "According to [source] as of [date]..."
   - Note uncertainty: "My training data is from Jan 2025, searching for latest..."

---

## Example Integration

### In core/AGENTIC_GUIDE.md

Add to **Section 2: Context Engineering**:

```markdown
### 7. Temporal Awareness & Web Search

**Automatic freshness detection**:
- Track session_date vs model_knowledge_cutoff
- Trigger WebSearch for queries requiring latest info
- Cache results (TTL: 24 hours)

**Search triggers**:
- "latest/newest/current" keywords
- Version/dependency queries
- Security advisories (CVE)
- Gap > 2 months from model cutoff

**See**: `implementations/factor-03-context-window/temporal-awareness.md`
```

---

## Testing

```python
def test_temporal_awareness():
    # Scenario 1: Latest version query
    query = "What's the latest version of React?"
    assert should_trigger_web_search(query, "2025-11-09", "2025-01") == True

    # Scenario 2: Historical query
    query = "How does React work?"
    assert should_trigger_web_search(query, "2025-11-09", "2025-01") == False

    # Scenario 3: Security query
    query = "Are there CVEs for Express?"
    assert should_trigger_web_search(query, "2025-11-09", "2025-01") == True

    # Scenario 4: Migration query
    query = "Migrate from Vue 2 to Vue 3"
    assert should_trigger_web_search(query, "2025-11-09", "2025-01") == True
```

---

**Version**: 0.4.0
**Factor**: 3.6 (Temporal Awareness + Web Search)
**Status**: Production-ready
**Related**: `context-compression.md`, `health-monitoring.md`
