# Factor 7: Contact Humans with Tool Calls

> **Source**: [HumanLayer 12 Factor Agents](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-07-contact-humans-with-tools.md)

---

## Overview

This factor addresses how agents should request human input. The key recommendation: have LLMs **"always output JSON"** with natural language intents like `request_human_input` rather than relying on the initial token choice between plaintext and structured data.

## The Problem

The first token LLMs generate carries significant weight—either starting plaintext content or denoting structured data. This creates ambiguity:

- If LLM starts with plaintext, it's committed to unstructured output
- If LLM starts with JSON, it must provide structured data
- Mixing modes mid-response is unreliable

## The Solution

**Always output JSON with declared intents**, including human contact as a tool call:

```python
{
    "intent": "request_human_input",
    "question": "Should I proceed with database migration?",
    "context": "Migration will modify 3 tables affecting 150K rows",
    "urgency": "high",
    "response_format": "approval|rejection|modification",
    "webhook": "https://api.example.com/agent/abc-def/resume"
}
```

## Implementation Pattern

### RequestHumanInput Tool

```python
class RequestHumanInput:
    question: str           # What to ask
    context: str            # Why asking
    urgency: str            # low|medium|high|critical
    response_format: str    # Expected response type
    options: List[str]      # Optional: multiple choice
    webhook: str            # Where to send response
```

### Webhook Pattern

```python
@app.post("/agent/{session_id}/resume")
async def handle_human_response(session_id: str, response: dict):
    """Receive human input and resume agent"""

    # Load paused session
    session = load_session(session_id)

    # Add human response to context
    session.add_context({
        "role": "human",
        "response": response["answer"],
        "timestamp": now()
    })

    # Resume execution
    return session.resume()
```

---

## 🎯 Our Implementation

### Location

Implemented via **tool escalation mechanism** in:
- `personas/agents/*.md` - Each persona defines escalation tools
- `implementations/factor-06-launch-pause-resume/` - Pause/resume for human input
- `core/AGENTIC_GUIDE.md` (§1) - Human-in-loop protocol

### How It Works

We implement human contact as a standard tool with escalation levels:

#### Tool Definition

```python
# Available to all personas
ESCALATION_TOOLS = {
    "request_human_approval": {
        "description": "Request human approval for high-stakes actions",
        "parameters": {
            "action": "What needs approval",
            "risk_level": "low|medium|high|critical",
            "context": "Why approval needed",
            "options": ["approve", "reject", "modify"]
        },
        "behavior": "pause_and_wait"
    },

    "request_human_clarification": {
        "description": "Ask human for clarification on ambiguous requirements",
        "parameters": {
            "question": "What needs clarification",
            "current_understanding": "Agent's current interpretation",
            "alternatives": ["option1", "option2", ...]
        },
        "behavior": "pause_and_wait"
    },

    "notify_human": {
        "description": "Inform human of important event (non-blocking)",
        "parameters": {
            "event": "What happened",
            "severity": "info|warning|error",
            "details": "Additional context"
        },
        "behavior": "continue_execution"
    }
}
```

#### Escalation Flow

```python
def handle_escalation_tool(tool_call, session):
    """Handle human contact tools"""

    if tool_call["tool"] == "request_human_approval":
        # Pause session
        session.pause(reason="Human approval required")

        # Create notification
        notification = create_notification(
            type="approval_request",
            question=tool_call["parameters"]["action"],
            risk_level=tool_call["parameters"]["risk_level"],
            context=tool_call["parameters"]["context"],
            session_id=session.session_id
        )

        # Send to user's preferred channel
        send_notification(notification, channels=["slack", "email"])

        # Log to SESSION_LOG
        session.log_escalation({
            "tool": "request_human_approval",
            "timestamp": now(),
            "status": "awaiting_response"
        })

        return {
            "status": "paused",
            "message": "Awaiting human approval",
            "resume_webhook": f"/agent/{session.session_id}/resume"
        }

    elif tool_call["tool"] == "notify_human":
        # Non-blocking notification
        notification = create_notification(
            type="info",
            event=tool_call["parameters"]["event"],
            severity=tool_call["parameters"]["severity"]
        )

        send_notification(notification)

        # Continue execution
        return {
            "status": "notified",
            "message": "Human notified, continuing execution"
        }
```

#### Multi-Channel Delivery

```python
def send_notification(notification, channels):
    """Deliver notification via multiple channels"""

    for channel in channels:
        if channel == "slack":
            send_slack_message(
                text=notification["question"],
                attachments=[
                    {
                        "text": notification["context"],
                        "actions": [
                            {"text": "Approve", "value": "approve"},
                            {"text": "Reject", "value": "reject"}
                        ]
                    }
                ]
            )

        elif channel == "email":
            send_email(
                subject=f"Agent Approval Required: {notification['question']}",
                body=format_email(notification),
                reply_webhook=notification["resume_webhook"]
            )

        elif channel == "cli":
            # For Claude Code, print to console
            print(f"\n🔔 HUMAN INPUT REQUIRED")
            print(f"Question: {notification['question']}")
            print(f"Context: {notification['context']}")
            print(f"Options: {notification['options']}")
```

#### Response Handling

```python
@app.post("/agent/{session_id}/resume")
async def receive_human_response(session_id: str, response: dict):
    """Handle human response and resume agent"""

    session = load_session(session_id)

    # Validate response
    if response["action"] not in session.escalation["options"]:
        return {"error": "Invalid response option"}

    # Add to context
    session.add_context({
        "role": "human",
        "action": response["action"],
        "reasoning": response.get("reasoning", ""),
        "timestamp": now()
    })

    # Log resolution
    session.log_escalation_resolution({
        "response": response["action"],
        "duration": now() - session.pause_timestamp
    })

    # Resume execution
    return session.resume(
        additional_context=f"Human response: {response['action']}"
    )
```

### Advantages

1. **Always structured**: Every output is JSON, including human requests
2. **Multi-channel**: Deliver via Slack, email, CLI, webhooks
3. **Non-blocking option**: Info notifications don't pause execution
4. **Full audit trail**: All escalations logged in SESSION_LOG
5. **Coordinated workflows**: Multiple agents can escalate to same human

### Example: High-Stakes Action

```python
# Agent detects high-risk operation
if risk_level == "high":
    result = agent.call_tool({
        "tool": "request_human_approval",
        "parameters": {
            "action": "Delete production database table 'users'",
            "risk_level": "critical",
            "context": "User requested cleanup of test data, but 'users' table contains 150K production records",
            "options": ["abort", "modify_to_test_table", "proceed_with_backup"]
        }
    })

    # Agent paused, waiting for human
    # SESSION_LOG shows: "Awaiting human approval (critical risk)"

# Human responds via Slack
# → "modify_to_test_table"

# Agent resumes with human decision
agent.execute_action("delete_table", table="test_users")  # Modified action
```

---

## Related Factors

- **Factor 4**: Tools Are Structured Outputs (human contact is a tool)
- **Factor 6**: Launch/Pause/Resume (escalation triggers pause)
- **Factor 8**: Own Your Control Flow (decide when to escalate)
- **Factor 11**: Trigger from Anywhere (respond via any channel)

---

**Version**: 0.4.0
**Status**: ✅ Implemented via tool escalation + multi-channel notifications
**See Also**: `implementations/factor-10-focused-agents/`, `core/AGENTIC_GUIDE.md`
