# Modular Template Architecture (Template-Only)

This guide defines a decoupled structure for agentic systems consuming this repository. It focuses on separation of concerns without prescribing a language/runtime.

## Components (Conceptual)
- Agent Core: Orchestration and planning (external runtime)
- Tools: Uniform, documented capabilities defined via tool specs (YAML)
- Memory: Short-term (session) + long-term (curated) policies
- Prompts: Structured templates (system, instructions, history, output)
- Context: Markdown KB lookups to enrich prompts

## Interfaces
- Tool Spec: see `core/TOOL_SPEC.md`
- Prompt Templates: `prompts/base_prompts/`
- Manifests: `manifests/*.yaml` for roles, tools, policies
- KB: `kb/*.md` content, headers for sectioning

## Extensibility
- Add tools by creating new tool specs and referencing them in agent manifests
- Swap memory policy by editing `AGENTIC_GUIDE.md` memory section
- Provide task-specific prompts via `prompts/examples/`

## Flow (High-Level)
1. Load manifests and select persona
2. Build prompt from templates: <BACKGROUND> + <INSTRUCTIONS> + Tool Guidance + <CONTEXT> + <MEMORY>
3. Enrich with KB sections from `kb/`
4. Generate → Validate → Verify → Log → Iterate

## Best Practices
- Keep prompts declarative and templated
- Treat tools as structured outputs with schemas
- Log every turn with token/health summaries
- Periodically curate long-term memory in markdown
