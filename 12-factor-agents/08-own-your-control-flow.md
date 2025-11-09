# Factor 8: Own Your Control Flow

> **Source**: [HumanLayer 12 Factor Agents](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-08-own-your-control-flow.md)

---

## Overview

This factor emphasizes building **custom control structures** tailored to your agent's specific needs rather than relying on generic frameworks.

Owning control flow enables agents to handle different scenarios appropriately with the right level of granularity.

## Key Concepts

### Different Operations Need Different Control

- **Synchronous operations** (like fetching data) → Return results directly to LLM for immediate processing
- **Asynchronous operations** (like human approval) → Pause execution and resume via webhooks
- **High-stakes actions** (like deployments) → Warrant human intervention **between tool selection and invocation**

### Critical Capability

**"We need to be able to interrupt a working agent and resume later, ESPECIALLY between the moment of tool selection and the moment of tool invocation"**

This granularity is essential for review and approval workflows. Without it, teams face an impossible choice:

- ❌ Pause indefinitely (can't review what hasn't been planned)
- ❌ Restrict agent capabilities (too limiting)
- ❌ Accept high-risk unsupervised actions (too dangerous)

## Implementation Opportunities

When you own control flow, you can incorporate:

- **Result summarization and caching** - Don't re-fetch data
- **LLM-based output validation** - Check responses before using them
- **Memory management strategies** - Decide what to keep/trim
- **Comprehensive logging and metrics** - Track every decision
- **Rate limiting** - Prevent API abuse
- **Durable pause/resume** - Stop and restart anywhere

---

## 🎯 Our Implementation

### Location

Implemented via **explicit execution protocol + health checks** in:
- `core/AGENTIC_GUIDE.md` (§9) - Execution footer protocol
- `implementations/factor-03-context-window/health-monitoring.md` - Health checks
- `implementations/factor-10-focused-agents/supervisor-pattern.md` - Multi-agent control flow

### How It Works

We own control flow through explicit execution protocols and health checks:

#### Execution Protocol (Deterministic)

```python
class AgentExecutor:
    """Deterministic control flow for agent execution"""

    def execute(self, task: str) -> Result:
        """Execute task with full control flow visibility"""

        # Step 1: Initialize
        session = self.initialize_session(task)
        self.log(f"Session initialized: {session.session_id}")

        # Step 2: Health check BEFORE execution
        health = self.context_health_check(session)
        if not health["ok"]:
            return self.handle_unhealthy_state(session, health)

        # Step 3: Plan (LLM call)
        plan = self.create_plan(session, task)
        self.log_to_session_log(session, "plan", plan)

        # Step 4: Validate plan
        if not self.validate_plan(plan):
            return self.escalate_invalid_plan(session, plan)

        # Step 5: Execute steps with control
        for step in plan["steps"]:
            # Health check before each step
            health = self.context_health_check(session)
            if not health["ok"]:
                session.pause(reason=f"Health check failed: {health['issue']}")
                return {"status": "paused", "reason": health["issue"]}

            # Execute step with full control
            result = self.execute_step_with_control(session, step)

            if result["needs_approval"]:
                # PAUSE between tool selection and invocation
                session.pause(reason="Human approval required")
                return {"status": "paused", "awaiting": "approval"}

            if result["error"]:
                # Error handling with limits
                if session.consecutive_errors >= 3:
                    session.pause(reason="Error threshold exceeded")
                    return {"status": "paused", "error": result["error"]}

            # Log and continue
            self.log_to_session_log(session, "step_complete", result)

        # Step 6: Finalize
        return self.finalize_session(session)
```

#### Tool Selection vs. Invocation Control

```python
def execute_step_with_control(self, session, step):
    """Control flow between tool SELECTION and INVOCATION"""

    # Phase 1: LLM selects tool (decision only, no execution)
    tool_selection = self.llm_select_tool(session, step)
    self.log(f"Tool selected: {tool_selection['tool']}")

    # Phase 2: Validate selection (deterministic)
    validation = self.validate_tool_selection(tool_selection, session)
    if not validation["valid"]:
        return {"error": validation["reason"], "needs_llm_retry": True}

    # Phase 3: Risk assessment (deterministic)
    risk = self.assess_tool_risk(tool_selection)
    self.log(f"Risk level: {risk['level']}")

    # Phase 4: DECISION POINT - Do we need approval?
    if risk["level"] in ["high", "critical"]:
        # Pause BEFORE invoking tool
        return {
            "status": "pending_approval",
            "tool": tool_selection,
            "risk": risk,
            "needs_approval": True
        }

    # Phase 5: Invoke tool (only after approval or low risk)
    result = self.invoke_tool(tool_selection)
    self.log(f"Tool invoked: {result['status']}")

    # Phase 6: Validate result (deterministic)
    if not self.validate_tool_result(result):
        return {"error": "Invalid tool result", "retry": True}

    # Phase 7: Summarize and cache (deterministic)
    summary = self.summarize_result(result)
    self.cache_result(tool_selection, summary)

    return {"status": "success", "result": summary}
```

#### Health Monitoring Loop

```python
def context_health_check(self, session) -> dict:
    """Check context health before operations"""

    checks = {
        "token_utilization": self.calculate_token_usage(session),
        "message_count": len(session.messages),
        "consecutive_errors": session.consecutive_errors,
        "time_since_start": now() - session.start_time
    }

    # Token budget exceeded?
    if checks["token_utilization"] > 0.8:
        return {
            "ok": False,
            "issue": "token_budget_exceeded",
            "action": "compress_context"
        }

    # Too many errors?
    if checks["consecutive_errors"] >= 3:
        return {
            "ok": False,
            "issue": "error_threshold",
            "action": "escalate_to_human"
        }

    # Session too long?
    if checks["time_since_start"] > 3600:  # 1 hour
        return {
            "ok": False,
            "issue": "session_timeout",
            "action": "checkpoint_and_resume"
        }

    return {"ok": True, "checks": checks}
```

#### Rate Limiting & Caching

```python
class RateLimitedExecutor(AgentExecutor):
    """Add rate limiting to control flow"""

    def __init__(self):
        super().__init__()
        self.rate_limiter = RateLimiter()
        self.cache = ResultCache()

    def execute_step_with_control(self, session, step):
        # Check rate limits
        if not self.rate_limiter.allow(session.user_id):
            session.pause(reason="Rate limit exceeded")
            return {"status": "paused", "reason": "rate_limit"}

        # Check cache first
        cache_key = self.generate_cache_key(step)
        if cached := self.cache.get(cache_key):
            self.log(f"Cache hit: {cache_key}")
            return {"status": "success", "result": cached, "cached": True}

        # Execute with rate limiting
        with self.rate_limiter.acquire(session.user_id):
            result = super().execute_step_with_control(session, step)

        # Cache result
        if result["status"] == "success":
            self.cache.set(cache_key, result["result"], ttl=3600)

        return result
```

#### Execution Footer (Always Run)

```python
# From core/AGENTIC_GUIDE.md §9: Execution Footer

"""
Upon loading AGENTIC_GUIDE.md, execute these steps in order:

Step 1: Load Required Modules
Step 2: Initialize Session
  - Extract session_date and session_timestamp
  - Create SESSION_LOG.md
  - Run context_health_check()
Step 3: Select Persona
Step 4: Parse & Execute
  - Parse user request
  - Build plan
  - Execute with health monitoring
  - Update SESSION_LOG
Step 5: Complete & Archive
"""
```

### Advantages

1. **Full visibility**: See every decision point
2. **Granular control**: Pause between tool selection and invocation
3. **Health monitoring**: Continuous checks prevent failures
4. **Deterministic routing**: Predictable, testable behavior
5. **Custom strategies**: Caching, rate limiting, validation

### Example: High-Stakes Operation

```python
# User: "Deploy to production"

# Step 1: LLM selects tool
tool = llm.select_tool()  # → "deploy_to_production"

# Step 2: Risk assessment
risk = assess_risk(tool)  # → "critical"

# Step 3: PAUSE before invocation
session.pause(reason="Critical operation requires approval")
notify_human({
    "action": "deploy_to_production",
    "risk": "critical",
    "options": ["approve", "reject", "modify"]
})

# Step 4: Human approves
# (webhook received)

# Step 5: NOW invoke tool
result = invoke_tool("deploy_to_production")
```

---

## Related Factors

- **Factor 3**: Own Your Context Window (health checks part of control flow)
- **Factor 5**: Unify Execution/Business State (log all control flow decisions)
- **Factor 6**: Launch/Pause/Resume (pause is part of control flow)
- **Factor 7**: Contact Humans with Tool Calls (escalation in control flow)

---

**Version**: 0.4.0
**Status**: ✅ Implemented via execution protocol + health monitoring
**See Also**: `core/AGENTIC_GUIDE.md` (§9), `implementations/factor-03-context-window/health-monitoring.md`
