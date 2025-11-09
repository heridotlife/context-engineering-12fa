# Factor 11: Trigger from Anywhere, Meet Users Where They Are

> **Source**: [HumanLayer 12 Factor Agents](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-11-trigger-from-anywhere.md)

---

## Overview

Factor 11 emphasizes enabling agents to be **triggered from multiple communication channels** like Slack, email, SMS, webhooks, cron jobs, and events, with responses flowing through the same channels.

## Key Concepts

### 1. Meeting Users in Their Preferred Spaces

Build AI applications that integrate seamlessly into existing workflows, functioning as "real humans, or at the very least, digital coworkers."

Users shouldn't need to learn a new interface—agents should work where users already are:
- Slack channels
- Email threads
- CLI terminals
- GitHub PR comments
- Webhooks from monitoring systems

### 2. Outer Loop Agents

Allow **non-human triggers** (events, crons, outages) to initiate agents that can:
- Run for extended periods
- Make progress autonomously
- Escalate to humans at critical junctures

Examples:
- Daily report generation (cron)
- Incident response (monitoring alert)
- PR review (GitHub webhook)
- Deployment automation (CI/CD event)

### 3. High-Stakes Operations

With reliable human-in-the-loop capabilities (Factor 7), agents can safely access higher-risk functions:
- External communications (sending emails, Slack messages)
- Production data updates (database modifications)
- Financial transactions (payment processing)
- Infrastructure changes (deployments, scaling)

This creates **auditability** and **user confidence** in agent capabilities.

---

## 🎯 Our Implementation

### Location

Implemented via **platform-agnostic binding system** in:
- `CLAUDE.md` - Claude Code binding
- `GEMINI.md` - Google AI Studio binding
- `COPILOT.md` - GitHub Copilot binding
- `core/AGENTIC_GUIDE.md` (§6) - Platform binding protocol

### How It Works

We enable triggering from anywhere through platform-agnostic design:

#### Platform Bindings

```markdown
# CLAUDE.md (Claude Code binding)

> You are an agentic AI using the **12 Factor Agents** specification.
> Load and follow all operational rules from `core/AGENTIC_GUIDE.md`.

This file exists to bind the Claude CLI to the shared behavior contract.
```

```markdown
# GEMINI.md (Google AI Studio binding)

> You are an agentic AI using the **12 Factor Agents** specification.
> Load and follow all operational rules from `core/AGENTIC_GUIDE.md`.

This file exists to bind Google AI Studio to the shared behavior contract.
```

```markdown
# COPILOT.md (GitHub Copilot binding)

> You are an agentic AI using the **12 Factor Agents** specification.
> Load and follow all operational rules from `core/AGENTIC_GUIDE.md`.

This file exists to bind GitHub Copilot to the shared behavior contract.
```

#### Universal Trigger Interface

```python
class UniversalAgentTrigger:
    """Trigger agents from any source"""

    def __init__(self):
        self.triggers = {
            "cli": CLITrigger(),
            "slack": SlackTrigger(),
            "email": EmailTrigger(),
            "webhook": WebhookTrigger(),
            "github": GitHubTrigger(),
            "cron": CronTrigger(),
            "event": EventTrigger()
        }

    def handle_trigger(self, source: str, payload: dict):
        """Universal entry point for all triggers"""

        # Normalize payload
        normalized = self.normalize_payload(source, payload)

        # Extract task
        task = normalized["task"]
        context = normalized["context"]
        response_channel = normalized["response_channel"]

        # Launch agent
        session = self.supervisor.launch(
            persona=self.select_persona(task),
            task=task,
            context=context
        )

        # Route responses back to source
        session.set_response_handler(
            self.create_response_handler(source, response_channel)
        )

        return session
```

#### Channel-Specific Triggers

```python
class SlackTrigger:
    """Trigger agent from Slack"""

    def handle_mention(self, event):
        """Handle @agent mentions in Slack"""

        return {
            "task": event["text"].replace(f"<@{BOT_ID}>", "").strip(),
            "context": {
                "channel": event["channel"],
                "user": event["user"],
                "thread_ts": event.get("thread_ts", event["ts"])
            },
            "response_channel": {
                "type": "slack",
                "channel": event["channel"],
                "thread": event.get("thread_ts", event["ts"])
            }
        }

class GitHubTrigger:
    """Trigger agent from GitHub events"""

    def handle_pr_comment(self, event):
        """Handle PR comment triggers"""

        if "/agent" not in event["comment"]["body"]:
            return None

        # Extract command after /agent
        command = event["comment"]["body"].split("/agent", 1)[1].strip()

        return {
            "task": command,
            "context": {
                "repo": event["repository"]["full_name"],
                "pr_number": event["pull_request"]["number"],
                "author": event["comment"]["user"]["login"],
                "pr_diff": fetch_pr_diff(event["pull_request"]["url"])
            },
            "response_channel": {
                "type": "github",
                "repo": event["repository"]["full_name"],
                "issue_number": event["pull_request"]["number"]
            }
        }

class CronTrigger:
    """Trigger agent on schedule"""

    def handle_schedule(self, schedule_config):
        """Handle scheduled triggers"""

        return {
            "task": schedule_config["task"],
            "context": {
                "schedule": schedule_config["cron"],
                "last_run": schedule_config.get("last_run"),
                "trigger_type": "scheduled"
            },
            "response_channel": {
                "type": "webhook",
                "url": schedule_config["result_webhook"]
            }
        }
```

#### Response Routing

```python
def create_response_handler(source: str, response_channel: dict):
    """Create handler to route responses back to trigger source"""

    if response_channel["type"] == "slack":
        def handler(message):
            slack_client.chat_postMessage(
                channel=response_channel["channel"],
                thread_ts=response_channel["thread"],
                text=message
            )
        return handler

    elif response_channel["type"] == "github":
        def handler(message):
            github_client.create_issue_comment(
                repo=response_channel["repo"],
                issue_number=response_channel["issue_number"],
                body=message
            )
        return handler

    elif response_channel["type"] == "email":
        def handler(message):
            send_email(
                to=response_channel["recipient"],
                subject=f"Re: {response_channel['subject']}",
                body=message,
                in_reply_to=response_channel["message_id"]
            )
        return handler

    elif response_channel["type"] == "webhook":
        def handler(message):
            requests.post(
                response_channel["url"],
                json={"message": message}
            )
        return handler

    else:
        # Default: CLI output
        def handler(message):
            print(message)
        return handler
```

### Example Triggers

#### 1. Slack: "@agent review this PR"

```python
# User posts in Slack: "@agent review PR #123"

# Slack event received
event = {
    "text": "<@U12345> review PR #123",
    "channel": "C789",
    "user": "U456",
    "ts": "1234567890.123456"
}

# Trigger agent
session = trigger.handle_trigger("slack", event)

# Agent responds in Slack thread
session.post_message("Reviewing PR #123...")
session.post_message("Found 3 issues: ...")
```

#### 2. GitHub: PR comment "/agent optimize performance"

```python
# User comments on PR: "/agent optimize performance"

# GitHub webhook received
webhook = {
    "action": "created",
    "comment": {"body": "/agent optimize performance"},
    "pull_request": {"number": 123, ...}
}

# Trigger agent
session = trigger.handle_trigger("github", webhook)

# Agent responds as PR comment
session.post_comment("Analyzing performance bottlenecks...")
session.post_comment("Optimized: [list of changes]")
```

#### 3. Cron: Daily security scan

```python
# Scheduled task: "0 9 * * * security scan"

# Cron trigger fires at 9am daily
schedule = {
    "task": "Run security scan on production codebase",
    "cron": "0 9 * * *",
    "result_webhook": "https://api.example.com/security-reports"
}

# Trigger agent
session = trigger.handle_trigger("cron", schedule)

# Agent posts report to webhook
session.post_result({"vulnerabilities": [...], "severity": "low"})
```

### Platform-Agnostic Benefits

1. **Write once, run anywhere**: Same agent spec works across all platforms
2. **User choice**: Users trigger via their preferred tool
3. **Consistent behavior**: Same prompts, same personas, same quality
4. **Easy migration**: Switch platforms without rewriting agents
5. **Multi-channel**: Respond where triggered (Slack → Slack, GitHub → GitHub)

---

## Related Factors

- **Factor 6**: Launch/Pause/Resume (launch from any trigger)
- **Factor 7**: Contact Humans with Tool Calls (respond via any channel)
- **Factor 12**: Stateless Reducer (platform-agnostic state)

---

**Version**: 0.4.0
**Status**: ✅ Implemented via platform bindings (Claude, Gemini, Copilot)
**See Also**: `CLAUDE.md`, `GEMINI.md`, `COPILOT.md`, `core/AGENTIC_GUIDE.md` (§6)
