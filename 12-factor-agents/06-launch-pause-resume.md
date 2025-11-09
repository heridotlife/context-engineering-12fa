# Factor 6: Launch/Pause/Resume with Simple APIs

> **Source**: [HumanLayer 12 Factor Agents](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-06-launch-pause-resume.md)

---

## Overview

Agents should operate like standard programs with straightforward lifecycle management. This factor emphasizes simple, predictable APIs for controlling agent execution.

## Core Capabilities

### 1. Launch

Users, applications, pipelines, and other agents should be able to launch agents through uncomplicated APIs:

```python
# Simple launch API
agent = Agent(persona="backend-architect")
session = agent.start(task="Create auth endpoint")
```

### 2. Pause

Agents and their deterministic orchestration code should support pausing during lengthy operations:

```python
# Pause during long-running task
session.pause(reason="Awaiting human approval")

# Pause with context preservation
session.pause(
    reason="External dependency (Redis setup)",
    resume_condition="webhook: redis_ready"
)
```

### 3. Resume

External triggers (like webhooks) should enable resuming agent execution from its previous state:

```python
# Resume from webhook
session = Session.load(session_id="abc-def")
session.resume(trigger="webhook", data={"redis_url": "redis://..."})

# Resume with updated context
session.resume(
    additional_context="User approved the deployment"
)
```

## Important Constraint

**Critical Limitation**: Many AI orchestrators don't allow pause/resume functionality **between the moment a tool is selected and when it's executed**.

This limitation means you can't easily:
- Review a tool call before execution
- Request human approval mid-execution
- Inject additional context after tool selection

This connects to Factor 7 (human contact) and Factor 8 (control flow).

---

## 🎯 Our Implementation

### Location

Implemented via **multi-agent supervisor pattern** in:
- `implementations/factor-10-focused-agents/supervisor-pattern.md` - Orchestration system
- `implementations/factor-05-state-management/` - SESSION_LOG persistence
- `core/AGENTIC_GUIDE.md` (§4) - Multi-agent lifecycle

### How It Works

We implement launch/pause/resume through the supervisor pattern:

#### Launch API

```python
class AgentSupervisor:
    """Orchestrates agent lifecycle"""

    def launch(self, persona: str, task: str, **kwargs) -> AgentSession:
        """Launch a new agent session"""

        # Create session with unified state
        session = AgentSession(
            session_id=generate_id(),
            session_date=get_local_date(),
            persona=persona,
            task=task,
            status="running"
        )

        # Initialize SESSION_LOG
        session.init_session_log()

        # Load persona
        agent = self.load_persona(persona)

        # Start execution
        session.agent = agent
        self.active_sessions[session.session_id] = session

        log(f"Launched {persona} agent: {session.session_id}")
        return session
```

#### Pause API

```python
def pause(self, session_id: str, reason: str, **kwargs):
    """Pause agent execution with state preservation"""

    session = self.active_sessions[session_id]

    # Save current state to SESSION_LOG
    session.save_checkpoint(
        reason=reason,
        current_step=session.get_current_step(),
        context_snapshot=session.get_context(),
        **kwargs
    )

    # Update status
    session.status = "paused"
    session.pause_reason = reason
    session.pause_timestamp = now()

    # Move to paused sessions
    self.paused_sessions[session_id] = session
    del self.active_sessions[session_id]

    log(f"Paused session {session_id}: {reason}")

    return {
        "status": "paused",
        "session_id": session_id,
        "resume_token": session.generate_resume_token()
    }
```

#### Resume API

```python
def resume(self, session_id: str, trigger: str, **kwargs):
    """Resume paused agent execution"""

    # Load session from paused state
    session = self.paused_sessions.get(session_id)
    if not session:
        # Try loading from disk
        session = AgentSession.load_from_log(session_id)

    # Restore checkpoint
    session.restore_checkpoint()

    # Add resume context
    session.add_context(
        f"Resuming after pause: {session.pause_reason}",
        trigger=trigger,
        **kwargs
    )

    # Update status
    session.status = "running"
    session.resume_timestamp = now()

    # Move to active sessions
    self.active_sessions[session_id] = session
    if session_id in self.paused_sessions:
        del self.paused_sessions[session_id]

    log(f"Resumed session {session_id} via {trigger}")

    # Continue execution from checkpoint
    return session.continue_execution()
```

### Multi-Agent Orchestration

```python
class MultiAgentSupervisor(AgentSupervisor):
    """Orchestrates multiple agents with pause/resume"""

    def execute_multi_agent_task(self, task: str):
        """Execute task across multiple agents"""

        # Launch coordinator
        coordinator = self.launch("project-coordinator", task)

        # Break down task
        subtasks = coordinator.plan_subtasks(task)

        # Launch sub-agents in parallel
        sub_sessions = []
        for subtask in subtasks:
            persona = self.select_persona_for_subtask(subtask)
            session = self.launch(persona, subtask["description"])
            sub_sessions.append(session)

        # Wait for completion or pause
        while not all(s.is_complete() for s in sub_sessions):
            for session in sub_sessions:
                if session.needs_human_input():
                    # Pause and wait for input
                    self.pause(
                        session.session_id,
                        reason="Human approval required",
                        resume_condition="webhook: approval_received"
                    )
                elif session.has_error():
                    # Pause for investigation
                    self.pause(
                        session.session_id,
                        reason=f"Error: {session.get_error()}",
                        resume_condition="manual"
                    )

        # Consolidate results
        return coordinator.consolidate_results(sub_sessions)
```

### Pause/Resume Triggers

```python
# Pause triggers
def check_pause_conditions(session):
    """Determine if session should pause"""

    if session.needs_human_approval():
        return "human_approval_required"

    if session.waiting_for_external_event():
        return "external_dependency"

    if session.hit_error_threshold():
        return "error_threshold_exceeded"

    if session.context_budget_exceeded():
        return "context_budget_exceeded"

    return None

# Resume triggers
RESUME_TRIGGERS = {
    "webhook": lambda data: data.get("event") == "approval_received",
    "manual": lambda data: True,  # Always allow manual resume
    "cron": lambda data: check_schedule(data["schedule"]),
    "event": lambda data: check_event_condition(data["condition"])
}
```

### State Persistence

```markdown
## Session: abc-def @ 2025-11-09T14:30:00Z
session_date: 2025-11-09
persona: backend-architect
status: paused

## Pause Checkpoint @ 14:35:12
reason: Awaiting human approval for database schema changes
current_step: 3/5 (create_database_migration)
resume_condition: webhook: schema_approved

## Context Snapshot
- Task: Create user authentication system
- Progress: 60% complete
- Artifacts: [auth.py, models.py, migrations/001_create_users.py]
- Decisions: [Use JWT, Hash with bcrypt, Add rate limiting]

## Resume Instructions
When resuming:
1. Verify schema approval in webhook data
2. Apply approved schema changes
3. Continue with step 4: Write integration tests
```

---

## Related Factors

- **Factor 5**: Unify Execution/Business State (unified state enables resume)
- **Factor 7**: Contact Humans with Tool Calls (human approval triggers pause)
- **Factor 8**: Own Your Control Flow (control when to pause/resume)
- **Factor 10**: Small, Focused Agents (each agent has independent lifecycle)

---

**Version**: 0.4.0
**Status**: ✅ Implemented via multi-agent supervisor pattern
**See Also**: `implementations/factor-10-focused-agents/supervisor-pattern.md`
