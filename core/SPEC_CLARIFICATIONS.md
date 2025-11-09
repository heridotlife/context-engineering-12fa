# Spec Clarifications: 12-Factor Agents & Context Engineering Alignment

**Date**: 2025-11-09  
**Status**: Awaiting Responses  
**Purpose**: Clarify design decisions to ensure full compliance with [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) and [Context Engineering](https://blog.langchain.com/context-engineering-for-agents/) principles.

---

## Review Summary

### ✅ Strong Alignment Areas
- Mandatory persona selection with clear protocol
- 12-Factor Agent table covering all factors
- Single codebase (AGENTIC_GUIDE.md) with adapters
- Context lifecycle (input → processing → output)
- Stateless design with externalized state
- Temporal awareness for date/time operations

### ⚠️ Areas Requiring Clarification
The following 10 topics need design decisions to complete the spec.

---

## 1. Memory Management (Write/Select Context)

### Background
- **12FA & Context Engineering emphasize**:
  - **Scratchpads**: Session-scoped notes/state for task execution
  - **Long-term memories**: Cross-session persistence (user preferences, learned patterns, facts)
  - **Memory types**: Episodic (examples), Procedural (instructions), Semantic (facts)
  - **Selection mechanisms**: Embeddings, knowledge graphs for relevant memory retrieval

### Current State
- Section 2, Factor 3: "No hidden persistent state. All memory must be externalized."
- Section 5: Temporal awareness for session date/time
- No explicit scratchpad or long-term memory guidance

### Questions

**Q1.1**: Should agents maintain a **scratchpad** (session-scoped state object) during task execution?
- Examples: Task plan, intermediate results, notes for later steps
- Storage: In-memory state object, temp file, or other?

**Your Answer**:
```
YES, use markdown file SESSION_LOG.md to store, help me define the structure and lifecycle best practices.
```

**✅ Best Practice Research** (Anthropic multi-agent system):
```
SESSION_LOG.md Structure:
---
session_date: 2025-11-09
session_timestamp: 2025-11-09T10:30:00-05:00
persona: [adopted-persona-name]
spec_version: 0.2.3

## Task Context
[User request summary]

## Plan
- [ ] Step 1: [description]
- [ ] Step 2: [description]

## Reasoning & Decisions
### [Timestamp] - [Step/Tool Name]
- Context: [what info was available]
- Analysis: [key reasoning points]
- Decision: [action taken]
- Rationale: [why this approach]

## Tool Calls & Results
### [Tool Name] @ [Timestamp]
Input: [tool args]
Output: [summary of result, full details isolated elsewhere if token-heavy]
Next Action: [what this enables]

## Progress Checkpoints
- [x] Checkpoint 1: [milestone] @ [timestamp]
- [ ] Checkpoint 2: [next milestone]

## Context Health
- Token count: [approximate]
- Key facts retained: [list critical info]
- Summary needed: [yes/no]
---

Lifecycle:
1. Initialize on session start (Execution Footer step 1)
2. Update after each significant node/tool call (not every token)
3. Save summaries to SESSION_LOG before spawning sub-agents
4. Archive SESSION_LOG.md → logs/session-[date]-[thread-id].md on session end
5. Use "think" tool pattern: log complex reasoning before tool calls
```

**Q1.2**: Should agents support **long-term memory** across sessions?
- Examples: User preferences, interaction history, learned facts
- Use cases: Personalization, avoiding repeated questions, context continuity

**Your Answer**:
```
LATER 
```

**Q1.3**: If long-term memory is supported, how should agents **select relevant memories**?

**Your Answer**:
```
Mechanism: knowledge-graph or file-based or combination of both
```

---

## 2. Context Compression (Token Management)

### Background
- **Context Engineering emphasizes**:
  - **Summarization**: LLM-based compression of agent trajectories
  - **Trimming**: Heuristic-based removal of old/irrelevant context
  - **Post-processing**: Compress token-heavy tool outputs

### Current State
- Section 8 (12FA): "Adapt to smaller or larger reasoning budgets"
- No explicit when/how to compress context

### Questions

**Q2.1**: Should agents **auto-summarize** when approaching token limits?

**Your Answer**:
```
YES

- Trigger threshold 50%
- Summarization strategy simple
- What to summarize first reasoning or fact 
```

**✅ Best Practice Research** (LangGraph/Anthropic):
```
Recommended Auto-Summarization Config:
- Trigger threshold: 50-80% of model's context window (50% is conservative, safe choice)
- Summarization strategy: "simple" = single-pass LLM summarization
  - Alternative: "recursive" (for very long contexts) or "hierarchical" (multi-level)
- What to summarize first: 
  1. Reasoning traces (verbose, can be compressed heavily)
  2. Tool outputs (keep result facts, drop verbose logs)
  3. Old human/AI message pairs (preserve facts, condense conversational filler)
  - PROTECT from summarization: Latest 2-3 message pairs, active tool results, current plan

Implementation:
- Use `SummarizationNode` pattern (LangGraph) or equivalent
- Store summary in state.context["summary"] field
- On next summarization, use existing summary as context for incremental update
- Token counter: count_tokens_approximately or model-specific counter
```

**Q2.2**: Should agents **trim old context** using heuristics?
- Examples: Remove messages older than N turns, drop duplicates, prune verbose outputs

**Your Answer**:
```
YES

- Trimming rules: remove old message
- What's protected from trimming: reasoning result and fact
- Frequency of trim operations: get from best practices guideline
```

**✅ Best Practice Research** (LangGraph trim_messages):
```
Recommended Trimming Config:
- Trimming rules:
  * "last" strategy: Keep last N tokens (most common)
  * Remove messages older than last 2-3 human/AI pairs
  * Drop duplicate tool outputs (same tool+args called multiple times)
  
- What's protected from trimming:
  * Latest 2 message pairs (human question + AI response)
  * System message (always retained)
  * Active tool call results
  * Reasoning conclusions/decisions
  * Key facts explicitly marked for retention
  
- Frequency of trim operations:
  * Before every LLM call (via pre_model_hook or state_modifier)
  * Triggered when message count > threshold (e.g., >10 messages OR >50% tokens)
  * Common pattern: Check token count, trim if needed, then invoke LLM
  
- Parameters (LangGraph trim_messages):
  * strategy: "last" (keep most recent)
  * max_tokens: 384-512 (leave headroom for response)
  * start_on: "human" (ensure context starts with user input)
  * end_on: ("human", "tool") (ensure complete thought)
```

**Q2.3**: Should agents **post-process token-heavy tool calls**?
- Examples: Summarize search results, compress file contents, extract key data

**Your Answer**:
```
SELECTIVE, refer to best practices
```

**✅ Best Practice Research** (Anthropic/LangGraph):
```
Selective Post-Processing Rules:
- Tool types requiring compression:
  * Web search/scraping: Summarize top N results (e.g., top 5), extract key facts
  * File read operations: Summarize if >1000 tokens; preserve structure (headers, key sections)
  * Database queries: Keep schema + sample rows; summarize large result sets
  * Code analysis: Extract signatures, docstrings, key logic; omit boilerplate
  * API responses: Keep status + essential fields; drop verbose metadata
  
- Tool types to preserve as-is:
  * Calculator/math results (small, precise)
  * Direct database writes/updates (confirmation only)
  * Small JSON payloads (<500 tokens)
  * User-facing outputs (preserve fidelity)
  
- Compression approach:
  * LLM-based: "Summarize these search results, preserving key facts and sources"
  * Heuristic: Truncate to first N tokens + "... (truncated)"
  * Structured extraction: Extract named entities, dates, key metrics
  
- Preserve original:
  * Store full output in state.tool_outputs[tool_name]
  * Pass summary to LLM context
  * Agent can request full output if needed via state access
```

---

## 3. Context Isolation (Multi-agent & State)

### Background
- **Context Engineering patterns**:
  - **Multi-agent**: Split tasks across sub-agents with isolated contexts
  - **State objects**: Isolate token-heavy objects from LLM (images, large data)
  - **Sandboxes**: Execute tools in isolated environments

### Current State
- Section 6 (12FA): "Handle concurrent prompts without state collision"
- No multi-agent orchestration or state isolation guidance

### Questions

**Q3.1**: Should the spec support **multi-agent workflows**?
- Examples: Planner agent delegates to specialist agents (coder, reviewer, tester)

**Your Answer**:
```
YES

- Orchestration pattern (supervisor/swarm/hierarchical): supervisor
- Context handoff mechanism: necessary context only
- Sub-agent coordination: yes
```

**Q3.2**: Should agents use a **state object schema** to isolate context?
- Examples: `state.messages` (to LLM), `state.images` (isolated), `state.tool_outputs` (selective)

**Your Answer**:
```
YES, get detail from best practices
```

**✅ Best Practice Research** (LangGraph State Management):
```
Recommended State Schema:
{
  "messages": [],              # Always exposed to LLM (trimmed/summarized)
  "llm_input_messages": [],    # Optional: pre-processed messages for LLM
  "summary": "",               # Context summary (exposed selectively)
  "context": {                 # Scratchpad/session data (isolated by default)
    "session_date": "2025-11-09",
    "session_timestamp": "...",
    "persona": "...",
    "plan": [],
    "summary": {}              # RunningSummary object
  },
  "tool_outputs": {},          # Isolated: {tool_name: {raw: ..., summary: ...}}
  "images": [],                # Isolated: binary/base64 data
  "large_artifacts": {},       # Isolated: code files, documents
  "ui": [],                    # UI messages (for generative UI patterns)
  "errors": []                 # Error log (isolated)
}

Exposure Rules:
- Always to LLM: messages (trimmed), summary (if present)
- Selective to LLM: tool_outputs.summary, context.plan
- Never to LLM: images (unless explicitly requested), large_artifacts (unless requested), errors (summarized only)
- State fields use reducers: messages (add_messages), context (merge), tool_outputs (merge)
```

**Q3.3**: Should tool execution be **sandboxed** (isolated from LLM context)?

**Your Answer**:
```
YES

- Sandbox mechanism file-based
- What outputs to expose to LLM: text
```

---

## 4. Tool Selection (RAG over Tools)

### Background
- **Context Engineering recommends**:
  - **RAG over tool descriptions**: When agents have many tools, retrieve only relevant ones
  - **Dynamic selection**: Reduces confusion, improves accuracy 3x per recent research

### Current State
- Persona selection implies available tools
- No explicit tool selection/filtering mechanism

### Questions

**Q4.1**: Do agents have access to a **large tool library** requiring filtering?

**Your Answer**:
```
YES

If YES, specify:
- Approx. number of tools: 30
```

**Q4.2**: Should tool descriptions be **embedded/retrieved dynamically**?

**Your Answer**:
```
PERSONA-FIXED
```

**Q4.3**: Should personas define a **fixed tool set**, or support dynamic expansion?

**Your Answer**:
```
HYBRID

Details:
- Persona tool assignment approach: predefine, update only if necessary
- Can agents request additional tools mid-task?: yes
```

---

## 5. Build/Test/Commit Workflow

### Background
- **12FA spec (CLAUDE.md) emphasizes**:
  - "BUILD AND TEST: Run your build and test commands after changes"
  - "COMMIT FREQUENTLY: Every 5-10 minutes for meaningful progress"

### Current State
- Section 9: "Common Commands (Placeholders)" - documentation-only
- No explicit build/test/commit discipline in operational constraints

### Questions

**Q5.1**: Should agents **auto-run tests** after code changes?

**Your Answer**:
```
YES

If YES/OPTIONAL, specify:
- When to run tests after task completion
- Test command discovery (package.json/Makefile/detect): define placeholder that can be adjusted later on
- Behavior on test failure (block/rollback/report): report the error message
```

**Q5.2**: Should agents **auto-commit** progress periodically?

**Your Answer**:
```
NO
```

**Q5.3**: What's the policy if **tests fail**?

**Your Answer**:
```
REQUEST-HELP

Details:
- Max retry attempts: 3
- Escalation procedure: Show error message or ask clarification
```

---

## 6. Compliance Checklist Enforcement

### Background
- **12FA spec says**: "DO NOT PROCEED WITHOUT SELECTING A PERSONA" (strong enforcement)

### Current State
- Section 6: Compliance Checklist marked "(Optional Emission)"
- Section 10: "If persona adoption is omitted, the first corrective action is to adopt one"

### Questions

**Q6.1**: Should compliance checks be **mandatory** (not optional)?

**Your Answer**:
```
YES

If YES, specify:
- Which checks are blocking: persona 
```

**Q6.2**: Should agents **refuse to execute** until persona is adopted + compliance confirmed?

**Your Answer**:
```
YES
```

---

## 7. Context Health & Validation

### Background
- **Context Engineering warns about**:
  - **Context Poisoning**: Hallucinations in context
  - **Context Confusion**: Superfluous context influencing responses
  - **Context Clash**: Conflicting information
  - **Context Distraction**: Context overwhelming training

### Current State
- Section 1: "Context Boundary Respect"
- Section 5: "Rejects out-of-scope or unsafe escalation"
- No explicit corrupted context detection

### Questions

**Q7.1**: Should agents **validate context integrity** before processing?
- Examples: Detect contradictions, check schema compliance, identify hallucinations

**Your Answer**:
```
YES

- Validation checks to perform: Detect contradictions and identify hallucinations
- When to validate (startup/per-step/on-demand): on-demand
- Action on validation failure: clarify to user
```

**Q7.2**: What should happen if context contains **conflicting instructions**?

**Your Answer**:
```
REQUEST-CLARIFICATION
```

**Q7.3**: Should there be a **"context health check"** step in the execution footer?

**Your Answer**:
```
YES

If YES, specify:
- Health metrics to track: 
- Frequency of health checks: 
- Remediation actions: 
```

**✅ Best Practice Research** (Context Engineering principles):
```
Context Health Metrics:
- Token utilization: current_tokens / max_tokens (warn at >50%, critical at >80%)
- Message count: total messages in state (baseline vs current)
- Contradiction detection: Check for conflicting instructions/facts (simple heuristic or LLM-based)
- Staleness: Age of oldest message (warn if >N turns without summarization)
- Completeness: Required context fields present (persona, task, constraints)

Frequency:
- On session init (Execution Footer)
- Before LLM calls (via pre_model_hook)
- After tool-heavy operations (3+ tool calls in sequence)
- On demand (user/agent can request health check)

Remediation Actions:
- Token >50%: Trigger summarization
- Token >80%: Force trim + summarize
- Contradiction detected: Request user clarification, log conflict in SESSION_LOG
- Staleness: Summarize old messages, archive to long-term memory
- Missing required field: Halt execution, request clarification

Implementation:
- Add context_health_check() function called in Execution Footer (step 1.5)
- Returns: {status: "healthy"|"warning"|"critical", metrics: {...}, recommendations: [...]}
- Log health status to SESSION_LOG
```

---

## 8. Project Context Customization

### Background
- **12FA spec says**: "CUSTOMIZE THIS SECTION FOR YOUR PROJECT" for:
  - Language/Framework, Build Tool, Testing, Architecture, File Structure, Common Commands

### Current State
- Section 7: "Placeholders" - marked "N/A (spec only)"
- Section 9: "Placeholders" - commands not filled

### Questions

**Q8.1**: Is this repo meant to be a **template** that users customize per-project?

**Your Answer**:
```
TEMPLATE

Details:
- If TEMPLATE, how should users customize (manual/script/guided)?: fill-in placeholder that will be specific for the project, users agentic ai tools will need to update the placeholder
```

**Q8.2**: Should there be a **setup script** to fill placeholders?
- Examples: `init-project.sh` prompts for language, framework, commands

**Your Answer**:
```
NO
```

**Q8.3**: Should the guide remain **project-agnostic** or include common stack examples?

**Your Answer**:
```
AGNOSTIC
```

---

## 9. TOON Format Validation

### Background
- **Context Engineering emphasizes**:
  - **Round-trip validation**: JSON → TOON → JSON to verify parity
  - **Schema validation**: Before/after conversion

### Current State
- Agent-native TOON conversion documented
- Round-trip validation marked "if the user requests"

### Questions

**Q9.1**: Should **round-trip validation** be mandatory for TOON conversion?

**Your Answer**:
```
YES
```

**Q9.2**: Should agents **always validate against schema** before converting to TOON?

**Your Answer**:
```
BEST-EFFORT

Details:
- Schema location (context-contract.json): 
- Proceed if schema missing?: 
```

**✅ Best Practice Research**:
```
Best-Effort Validation Approach:
- Schema location: schemas/context-contract.json (if present in project)
- Validation steps:
  1. Check if schema file exists
  2. If yes: Validate JSON structure, required fields, types
  3. If validation fails: Log warnings, proceed with noted issues
  4. If schema missing: Perform basic structure check (has persona, task, spec_version)
  
- Proceed if schema missing: YES
  * Log: "Schema not found, using basic validation"
  * Check minimal requirements: persona field, task/context field present
  * Warn if spec_version missing or outdated
  
- Validation failures:
  * Missing required field: ERROR, request clarification
  * Type mismatch: WARNING, attempt coercion (e.g., string→array)
  * Unknown fields: INFO, preserve in TOON (may be extension)
```

**Q9.3**: Should TOON be **default** or **opt-in** for large payloads?

**Your Answer**:
```
AUTO-DETECT

If AUTO-DETECT, specify:
- Threshold for auto-TOON (token count/size): 
- User notification/override: 
```

**✅ Best Practice Research** (token efficiency):
```
Auto-Detect Thresholds:
- Token count threshold: >1000 tokens (approx 750-800 words)
- File size threshold: >4KB for JSON payload
- Rationale: TOON saves ~10-20% tokens for typical structured data

Auto-Detect Logic:
1. Count tokens in JSON payload (use count_tokens_approximately)
2. If >1000 tokens:
   - Convert to TOON
   - Validate round-trip (JSON → TOON → JSON)
   - If round-trip succeeds: Use TOON
   - If fails: Log warning, use JSON
3. If ≤1000 tokens: Use JSON (overhead of TOON not justified)

User Notification:
- Log: "Payload size: 1234 tokens, using TOON format for efficiency"
- Add metadata to SESSION_LOG: format_used: "TOON", token_savings: ~200
- User override: Allow force_format: "JSON"|"TOON" in context config

Implementation:
- Add format_decision() function in context ingestion
- Returns: {format: "JSON"|"TOON", reason: "...", token_count: N}
```

---

## 10. Observability & Tracing

### Background
- **Context Engineering & 12FA emphasize**:
  - **Token tracking**: Per step, per tool call, cumulative
  - **Reasoning traces**: For debugging and transparency
  - **Metadata**: Step count, artifact types, timing

### Current State
- Section 5 (12FA): "Logging & Trace" - maintain interpretable trace
- Section 3: "Prepare observability metadata (optional)"

### Questions

**Q10.1**: Should agents **emit token counts** per step/tool call?

**Your Answer**:
```
ON-DEMAND

If YES/ON-DEMAND, specify:
- Output format (JSON/log/structured): 
- Granularity (per-step/per-tool/cumulative): 
- Where to emit (stdout/file/external): 
```

**✅ Best Practice Research** (LangSmith/observability):
```
On-Demand Token Tracking Config:
- Output format: STRUCTURED-MARKDOWN (human-readable + parseable)
  * Alternative: JSON for external tools (LangSmith, custom dashboards)
  
- Granularity:
  * Per-LLM-call: Input tokens, output tokens, total
  * Per-tool-call: Estimate tokens in tool args + result
  * Per-step/node: Cumulative tokens for that graph node
  * Session cumulative: Running total across all operations
  
- Where to emit:
  * stdout: Only if trace=true or verbosity=debug in context
  * file: Append to SESSION_LOG under "## Token Usage" section
  * external: Send to LangSmith/observability platform if configured
  
- Trigger:
  * Always track internally (state.context["token_usage"])
  * Emit only when:
    - trace=true in context
    - token_budget constraint present
    - Health check detects token >50%
    - Session end summary
    
- Format example:
  ```
  ## Token Usage @ 2025-11-09T10:35:22
  - LLM Call (agent node): input=234, output=156, total=390
  - Tool Call (search): ~180 tokens
  - Cumulative: 1,245 / 8,000 (15.6%)
  ```
```

**Q10.2**: Should **reasoning traces** be on by default or opt-in?

**Your Answer**:
```
PERSONA-DEPENDENT

Details:
- Trace verbosity levels: 
- Privacy/security filtering: 
```

**✅ Best Practice Research** (Anthropic "think" tool):
```
PERSONA-DEPENDENT Config:

Default Behavior by Persona Type:
- Developer/debugging personas: trace=true by default
- Production/end-user personas: trace=false by default
- Audit/compliance personas: trace=true with full logs

Override Mechanism:
- context.trace = true/false (explicit override)
- context.verbosity = "debug"|"info"|"warn"|"error" (granular)
- Environment variable: AGENT_TRACE=1 (session-level)
- Per-tool override: tool_call(..., trace=true)

Verbosity Levels:
1. silent (trace=false, verbosity=error):
   - Only final results and errors
   
2. normal (trace=false, verbosity=info):
   - Results, errors, warnings
   - Health check alerts (>50%)
   
3. verbose (trace=true, verbosity=info):
   - + Tool calls and results
   - + State transitions
   - + Token usage on health checks
   
4. debug (trace=true, verbosity=debug):
   - + Internal reasoning (scratchpad content)
   - + All LLM calls (input/output)
   - + Token counts per operation
   - + Validation steps

Privacy/Security Filtering:
- Auto-redact: API keys, passwords, tokens, PII (email, phone, SSN)
- Sanitize file paths: Replace /home/user with $HOME
- Mask sensitive params: tool_call(api_key="***")
- Log redactions: "[REDACTED: api_key]" to preserve trace structure

Emit Location:
- silent/normal: stdout (results only)
- verbose: stdout + SESSION_LOG.md ("## Trace" section)
- debug: stdout + SESSION_LOG.md + optional external (LangSmith)

Best Practice:
- Let persona defaults guide (developer=verbose, production=normal)
- Enable debug only for development or compliance review
- Always apply privacy filtering regardless of level
- Log errors always, regardless of verbosity
```

**Q10.3**: What **format** for observability data?

**Your Answer**:
```
STRUCTURED-MARKDOWN
```

**✅ Best Practice Research** (LangSmith/LangGraph observability):
```
STRUCTURED-MARKDOWN Format Spec:

Primary: SESSION_LOG.md
- Human-readable for quick review
- Parseable for tooling (grep, scripts)
- Persistent across session (append-only)
- Version controlled with code

Structure:
```markdown
## Session: [session_id] @ [timestamp]

### Task
[Original user request]

### Plan
1. Step 1
2. Step 2

### Reasoning
- Decision: Use tool X because Y
- Constraint: Token budget = 8000

### Tool Calls
- `tool_name(args)` → result (tokens: 234)

### State Checkpoints
- After step 2: [checkpoint_id]

### Token Usage @ [timestamp]
- LLM Call (node): input=234, output=156, total=390
- Cumulative: 1,245 / 8,000 (15.6%)

### Health Check @ [timestamp]
- Token utilization: 50% (WARN)
- Action: Triggered summarization

### Trace (if enabled)
- [timestamp] [level] Message
- [timestamp] DEBUG LLM call: {...}
```

Alternative: JSON for External Tools
If context.export_format = "json":
```json
{
  "session_id": "abc123",
  "timestamp": "2025-11-09T10:35:22Z",
  "task": "...",
  "plan": ["step1", "step2"],
  "tool_calls": [
    {"tool": "search", "args": {...}, "result": {...}, "tokens": 234}
  ],
  "token_usage": {
    "input": 1245,
    "output": 890,
    "total": 2135,
    "budget": 8000,
    "utilization": 0.267
  },
  "health_checks": [
    {"timestamp": "...", "metric": "token_utilization", "value": 0.5, "level": "WARN"}
  ],
  "trace": [...]
}
```

Export to external observability:
- LangSmith: Auto-export if LANGCHAIN_API_KEY present
- Custom webhook: POST JSON to context.observability_endpoint
- File export: Write JSON to .observability/session-{id}.json

Best Practice:
- Default: STRUCTURED-MARKDOWN in SESSION_LOG.md
- Enable JSON export for dashboards/monitoring
- Use markdown for human debugging
- Archive JSON for compliance/audit trails
```

---

## Next Steps

1. **Fill in your answers** in the placeholders above
2. **Save this file** with your responses
3. I'll update `AGENTIC_GUIDE.md`, `README.md`, and create any new supporting files based on your decisions
4. If any answers require new schemas, examples, or scripts, I'll generate those as well

---

## Additional Notes / Context

This project will be template that can be copy paste to any existing project to easily using agentic AI with 12 factor agent and context engineering concept. The goals is to create reusable framework across agentic AI.
