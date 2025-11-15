# Prompt Templates (Structured)

These templates segment context into clear sections to improve parsing and token efficiency. They are markdown with placeholders like `{{PLACEHOLDER}}` and tag-like blocks.

## Sections
- <BACKGROUND>: Static or project-specific knowledge
- <INSTRUCTIONS>: Concrete task directives and constraints
- ## Tool Guidance: Allowed tools and usage notes
- ## Output Format: Expected structure (JSON or Markdown)
- <CONTEXT>: Conversation history or relevant excerpts
- <MEMORY>: Key long-term facts / decisions

Consumers should fill placeholders and optionally remove unused sections before sending to the LLM.
