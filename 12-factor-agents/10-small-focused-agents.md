# Factor 10: Small, Focused Agents

> **Source**: [HumanLayer 12 Factor Agents](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-10-small-focused-agents.md)

---

## Overview

**Core Principle**: Build many small, specialized agents instead of one large, general-purpose agent.

Small agents are:
- **Easier to prompt** - Narrow scope, clear instructions
- **Easier to test** - Limited functionality, focused test cases
- **More reliable** - Less ambiguity, better tool selection
- **More maintainable** - Isolate changes to specific domains

## The Anti-Pattern

❌ **God Agent**: One agent that does everything

```python
agent = Agent(
    prompt="You are an expert at everything: backend, frontend, DevOps, "
           "security, databases, mobile, ML, data science, design...",
    tools=[...hundreds of tools...]
)
```

Problems:
- Ambiguous tool selection (too many choices)
- Diluted expertise (jack of all trades, master of none)
- Hard to test (infinite combinations)
- Difficult to maintain (changes affect everything)

## The Pattern

✅ **Specialized Agents**: Many focused agents, each expert in one domain

```python
backend_agent = Agent(
    prompt="You are a backend architect specializing in API design",
    tools=["create_endpoint", "add_middleware", "setup_db"]
)

frontend_agent = Agent(
    prompt="You are a frontend developer specializing in React",
    tools=["create_component", "add_state", "style_element"]
)

security_agent = Agent(
    prompt="You are a security auditor specializing in vulnerabilities",
    tools=["scan_code", "check_auth", "review_permissions"]
)
```

---

## 🎯 Our Implementation

### Location

**Full implementation + major extension** in:
- `personas/agents/` - **86 specialized agent personas** (vs. HumanLayer's 5)
- `personas/PERSONA_CATALOG.md` - Persona selection guide
- `implementations/factor-10-focused-agents/` - Multi-agent orchestration
- `core/AGENTIC_GUIDE.md` (§4) - Multi-agent protocol

### How It Works

We extend Factor 10 dramatically with a rich persona system:

#### 86 Specialized Personas

| Category | Count | Examples |
|----------|-------|----------|
| **Backend** | 12 | backend-architect, api-documenter, graphql-architect, fastapi-pro |
| **Frontend/Mobile** | 8 | frontend-developer, mobile-developer, ui-ux-designer, flutter-expert |
| **Languages** | 15 | python-pro, typescript-pro, rust-pro, golang-pro, java-pro, ruby-pro |
| **Operations** | 10 | devops-troubleshooter, performance-engineer, security-auditor |
| **Data/ML** | 8 | data-engineer, data-scientist, ml-engineer, mlops-engineer |
| **Security** | 6 | security-auditor, backend-security-coder, frontend-security-coder |
| **Testing** | 5 | test-automator, debugger, performance-engineer |
| **Specialized** | 22 | blockchain-developer, payment-integration, legal-advisor, seo-* |

#### Persona Selection Protocol

```python
def select_persona(task: str) -> str:
    """Match task to most appropriate persona"""

    # Parse task intent
    intent = classify_intent(task)

    # Intent → Persona mapping (from PERSONA_CATALOG.md)
    intent_map = {
        "implement_backend": ["backend-architect", "fastapi-pro", "django-pro"],
        "implement_frontend": ["frontend-developer", "mobile-developer"],
        "implement_api": ["backend-architect", "api-documenter"],
        "implement_graphql": ["graphql-architect"],
        "security_audit": ["security-auditor"],
        "performance_optimization": ["performance-engineer"],
        "database_design": ["database-admin", "database-optimizer"],
        "test_automation": ["test-automator"],
        "debug_error": ["debugger", "error-detective"]
    }

    # Select most specific persona
    personas = intent_map.get(intent, ["general-purpose"])

    # Refine based on tech stack
    if "Python" in task:
        personas = [p for p in personas if "python" in p or "django" in p or "fastapi" in p]
    elif "TypeScript" in task:
        personas = [p for p in personas if "typescript" in p or "frontend" in p]

    # Return most specific match
    return personas[0]
```

#### Multi-Agent Orchestration

```python
class MultiAgentSupervisor:
    """Orchestrate multiple specialized agents"""

    def execute_complex_task(self, task: str):
        """Break down task and assign to appropriate agents"""

        # Analyze task complexity
        complexity = analyze_task_complexity(task)

        if complexity == "simple":
            # Single persona sufficient
            persona = select_persona(task)
            return self.execute_single_agent(persona, task)

        else:
            # Multi-agent needed
            subtasks = decompose_task(task)

            # Assign personas to subtasks
            agent_assignments = []
            for subtask in subtasks:
                persona = select_persona(subtask["description"])
                agent_assignments.append({
                    "subtask": subtask,
                    "persona": persona,
                    "dependencies": subtask.get("dependencies", [])
                })

            # Execute in dependency order
            return self.execute_multi_agent(agent_assignments)

    def execute_multi_agent(self, assignments):
        """Execute with context handoffs"""

        results = {}
        sessions = {}

        for assignment in assignments:
            # Wait for dependencies
            self.wait_for_dependencies(assignment["dependencies"], results)

            # Create context handoff
            context = self.create_handoff_context(
                task=assignment["subtask"],
                persona=assignment["persona"],
                dependency_results=results
            )

            # Launch sub-agent
            session = self.launch_agent(
                persona=assignment["persona"],
                context=context
            )

            # Track session
            sessions[assignment["subtask"]["id"]] = session
            results[assignment["subtask"]["id"]] = session.result

        return self.consolidate_results(sessions, results)
```

#### Context Handoff (Minimal)

```python
def create_handoff_context(task, persona, dependency_results):
    """Create minimal context for sub-agent"""

    return {
        # Task info (what to do)
        "task": task["description"],
        "objective": task["objective"],

        # Relevant state only (not full SESSION_LOG)
        "artifacts": [
            r["artifacts"] for r in dependency_results.values()
        ],
        "decisions": [
            r["key_decisions"] for r in dependency_results.values()
        ],

        # References (don't copy full content)
        "refs": {
            "parent_session": get_session_log_path(),
            "dependency_sessions": [
                r["session_id"] for r in dependency_results.values()
            ]
        }
    }
```

### Example: Multi-Agent Task

```python
# User: "Build a REST API with authentication, tests, and deployment"

# Supervisor analyzes
task_breakdown = [
    {
        "id": "t1",
        "description": "Design and implement REST API endpoints",
        "persona": "backend-architect",
        "dependencies": []
    },
    {
        "id": "t2",
        "description": "Add JWT authentication",
        "persona": "security-auditor",
        "dependencies": ["t1"]
    },
    {
        "id": "t3",
        "description": "Write integration tests",
        "persona": "test-automator",
        "dependencies": ["t1", "t2"]
    },
    {
        "id": "t4",
        "description": "Set up CI/CD pipeline",
        "persona": "deployment-engineer",
        "dependencies": ["t3"]
    }
]

# Execute in order with handoffs
results = supervisor.execute_multi_agent(task_breakdown)

# Each agent:
# - Gets minimal context (task + refs)
# - Works in its domain only
# - Returns focused result
# - No knowledge of other agents' internals
```

### Advantages Over HumanLayer's Approach

| Aspect | HumanLayer (5 personas) | Ours (86 personas) |
|--------|-------------------------|-------------------|
| **Specificity** | General categories | Deep specialization |
| **Tool selection** | Many tools/agent | Focused toolset |
| **Prompt length** | Long, generic | Short, specific |
| **Extensibility** | Add manually | Template-driven |
| **Language support** | Limited | 15+ languages |

### When to Use Multi-Agent

✅ **Use multi-agent when:**
- Task spans multiple domains (backend + frontend + tests)
- Parallel work possible (independent subtasks)
- Single persona insufficient (needs multiple expertise areas)

❌ **Stay single-agent when:**
- Narrow task (one persona sufficient)
- Token budget tight (<4000 tokens)
- Sequential work (no parallelism benefit)

---

## Related Factors

- **Factor 1**: Natural Language to Tool Calls (persona selection)
- **Factor 2**: Own Your Prompts (each persona has custom prompt)
- **Factor 5**: Unify Execution/Business State (each agent has SESSION_LOG)
- **Factor 6**: Launch/Pause/Resume (each agent lifecycle independent)

---

**Version**: 0.4.0
**Status**: ✅ **Major extension** - 86 personas vs. HumanLayer's 5
**See Also**: `personas/PERSONA_CATALOG.md`, `implementations/factor-10-focused-agents/`
