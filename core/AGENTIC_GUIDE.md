# {{PROJECT_NAME}} Agentic Template

> Spec Metadata: `spec_version: 0.4.0` | `stability: experimental` | `license: MIT` | `framework: HumanLayer 12FA + Context Engineering`
> Mode: Markdown Knowledge Base (no vector/RAG dependency)

## 0. Placeholder Inventory
`{{PROJECT_NAME}}`, `{{PROJECT_STACK}}`, `{{STACK}}`, `{{MODEL}}`, `{{SECRET_KEY}}`, `{{DB_URL}}`, `{{KB_PATH}}`, `{{SESSION_ID}}`, `{{ISO_TIMESTAMP}}`, `{{ROLE}}`, `{{GOAL}}`, `{{CONSTRAINTS}}`, `{{SCHEMA_REF}}`, `{{MEMORY_SNIPPET}}`, `{{EVIDENCE_BLOCK}}`, `{{SCHEMA_NAME}}`, `{{SCHEMA_TITLE}}`, `{{ORCH_ID}}`, `{{RESEARCHER_ID}}`, `{{VERIFIER_ID}}`, `{{TTL_ORCH}}`, `{{TTL_RESEARCH}}`, `{{TTL_VERIFY}}`, `{{ORCH_INPUT_SCHEMA}}`, `{{ORCH_OUTPUT_SCHEMA}}`, `{{RESEARCH_INPUT_SCHEMA}}`, `{{RESEARCH_OUTPUT_SCHEMA}}`, `{{VERIFY_INPUT_SCHEMA}}`, `{{VERIFY_OUTPUT_SCHEMA}}`, `{{LOG_LEVEL}}`, `{{OTLP_ENDPOINT}}`, `{{MAX_RETRIES}}`, `{{MIN_EVIDENCE}}`, `{{MIN_CONFIDENCE}}`, `{{QUEUE_BACKEND}}`, `{{FRAMEWORK}}`, `{{LANGUAGE}}`.

## 0.1 Operational Prerequisites
1. Persona selected from `personas/PERSONA_CATALOG.md` (log adoption).
2. `templates/SESSION_LOG.md` instantiated (session header written).
3. Initial `context_health_check` performed (Factor 3 health monitoring).
4. Compliance checklist executed (`core/COMPLIANCE_CHECKLIST.md`).
5. All critical placeholders replaced before production run.

## 0.1.1 Persona System (Factor 10 Emphasis)
The persona library (86+ specialized agents) enables focused tool routing and prompt ownership.
### Selection Protocol (Mandatory Before Any Task)
1. Parse user task → classify dominant intent.
2. Match intent to catalog entry in `personas/PERSONA_CATALOG.md`.
3. Load persona file from `personas/agents/`.
4. Announce adoption explicitly in first response: `Persona: {{PERSONA_NAME}} adopted for {{TASK_ID}}`.
5. Stay in scope; switch only on explicit request or material task shift (log switch in SESSION_LOG).
6. Record persona, task objective, constraints in `SESSION_LOG.md`.

### Persona Compliance Checks
- Exactly one active persona at a time.
- Persona prompt loaded (hash recorded optionally).
- Tool set matches allowed persona capabilities.
- Health monitoring acknowledges persona context size.

### Example Persona Adoption Log Entry
```markdown
[PERSONA_ADOPTED] persona=backend-architect task="Design API" ts={{ISO_TIMESTAMP}}
```

## 0.2 Factor Cross-Link Reference
| Factor | Section Here | Directory Link |
|--------|--------------|----------------|
| 3 Context Window | 4 Context Engineering Layer | `implementations/factor-03-context-window/` |
| 5 State Management | Session Log Integration (§4 addendum) | `implementations/factor-05-state-management/` |
| 9 Error Compaction | Verifier Policy (Sections 3 & 5) | `implementations/factor-09-error-handling/` |
| 10 Focused Agents | Triadic Blueprint (Section 3) | `implementations/factor-10-focused-agents/` |
| 12 Stateless Reducer | Manifests + Externalized Memory | `templates/SESSION_LOG.md` |

## 0.3 Legacy Tool Name Mapping
| Legacy Label | New Manifest Tool ID | Notes |
|--------------|----------------------|-------|
| WebSearch | `web_search` | External search / freshness |
| VectorRetrieve | `md_lookup` | Markdown KB section scan |
| ValidateSchema | `schema_validate` | JSON Schema validation |
| CrossCheck | `cross_check` | Secondary evidence verification |
| EvidenceAggregate | `aggregate_results` | Orchestrator consolidation |
| DispatchAgent | `dispatch_agent` | Orchestrator task routing |
| PlanTasks | `plan_tasks` | Task decomposition |
| FactConsistency | `fact_consistency` | Consistency check vs sources |

## 0.4 Session Log Integration (Factor 5)
Embed after each major turn:
```
## Turn {{TURN_ID}} @ {{ISO_TIMESTAMP}}
persona: {{ROLE}}
task: {{TASK_ID}}
plan: [ .. steps .. ]
tools_used: [ {"name":"md_lookup","sections":3}, ... ]
health: {"token_util": "38%", "messages": 12}
summary: "...compressed context..."
```
Compression triggers when utilization >50%; trimming at >80%.

## 0.5 Execution Footer (Condensed Protocol)
**Upon loader start execute these phases in order:**
1. Load Modules: factor-03 (context), persona catalog (if none selected), compliance checklist (if validation requested).
2. Initialize Session: set `session_date`, `session_timestamp`; create `SESSION_LOG.md` from template.
3. Persona Selection: apply selection protocol; log adoption.
4. Freshness & Search: detect temporal keywords ("latest", "CVE", version) → trigger `web_search` if model cutoff stale.
5. Planning: orchestrator generates multi-step plan; store under `plan` in session log.
6. Execution Loop: apply triadic dispatch → researcher → verifier → orchestrator aggregate.
7. Health Monitoring: run `context_health_check` before each LLM turn; apply summarization / trimming.
8. Completion: verifier passes; orchestrator outputs final artifact; archive session to `.session-archive/`.

### Execution Log Example Lines
```markdown
[INIT] session_id={{SESSION_ID}} date={{session_date}} ts={{ISO_TIMESTAMP}}
[PLAN] steps=["scan repos","design schema","generate manifests"]
[DISPATCH] task_id={{TASK_ID}} to=researcher envelope_id={{UUID}}
[VERIFY] status=pass sources=5 confidence=0.92
[COMPLETE] task_id={{TASK_ID}} duration=142s
```


## 1. Project Overview (Short)
{{PROJECT_NAME}} applies the 12-Factor Agent methodology plus a triadic (orchestrator–researcher–verifier) pattern and a context engineering layer (Markdown KB + memory + structured prompts) atop {{PROJECT_STACK}} / {{STACK}}. This template provides minimal manifests, schemas, and integration notes using placeholders for rapid customization.

## 2. 12-Factor Agent Mapping
| # | Factor | Definition | Application to {{PROJECT_NAME}} | TODO (with placeholders) |
|:-:|:-------|:-----------|:-------------------------------|:-------------------------|
| 1 | Codebase | Single authoritative spec + manifests | Keep agent specs in `agents/` folder | Create `agents/orchestrator.yaml` {{MODEL}} |
| 2 | Config | Settings externalized via env | Use `.env` for {{SECRET_KEY}}, {{DB_URL}} | Add `dotenv` loader in runtime |
| 3 | Dependencies | Explicit, pinned modules | Lock model/tool SDK versions | Generate `requirements.txt` / `package.json` {{STACK}} |
| 4 | Context | Deliberate window + compression | Implement memory TTL + Markdown section selection | Add KB scanning helper {{MODEL}} |
| 5 | Build-Release-Run | Separate spec from execution | Spec YAML consumed by external runtime | Provide external loader (out of scope here) |
| 6 | Processes | Stateless agents; external state | Read-only markdown KB + simple cache | Define `{{KB_PATH}}` folder |
| 7 | Port Binding | Expose via API / CLI | Wrap orchestrator as HTTP endpoint | Build `server.{ext}` using {{FRAMEWORK}} |
| 8 | Concurrency | Multi-agent orchestration | Orchestrator fans tasks to researcher | Implement task queue {{QUEUE_BACKEND}} |
| 9 | Disposability | Fast start/stop; clean teardown | On exit flush memory + logs | Add shutdown hook {{STACK}} |
|10 | Dev/Prod Parity | Align local & prod infra | Same KB folder structure & env names | Mirror `.env.example` to deployment templates |
|11 | Logs | Event stream; treat as append-only | JSON logs for each agent turn | Configure logger level via {{LOG_LEVEL}} |
|12 | Admin Tasks | Run ops scripts as agents | Use verifier role for audits | Add `scripts/audit_context.{ext}` |

## 3. Triadic / Multi-Agent Blueprint
### Roles
- Orchestrator: Plans tasks, decomposes goals, routes messages, consolidates outputs.
- Researcher: Executes retrieval, analysis, tool/RAG queries; returns structured evidence.
- Verifier: Validates schemas, checks factual consistency, enforces policies & guardrails.

### Message Schema (Envelope)
```json
{
  "envelope_id": "{{UUID}}",
  "from": "{{AGENT_ROLE}}",
  "to": "{{TARGET_AGENT}}",
  "task": {
    "id": "{{TASK_ID}}",
    "input": "...",
    "schema": "{{SCHEMA_PATH}}"
  },
  "policy": {
    "max_steps": 5,
    "verify_required": true
  }
}
```

### Coordination Rules
1. Orchestrator emits task envelopes → researcher.
2. Researcher returns `data_bundle` + `evidence_list` conforming to {{SCHEMA_PATH}}.
3. Verifier validates: schema conformity, provenance count >= {{MIN_EVIDENCE}}, optional cross-check via secondary RAG query.
4. Failure → orchestrator issues `revision_request` with delta instructions.
5. Completion → orchestrator aggregates verified outputs → final response.
6. Supervisor Scaling (Optional): For broader tasks, integrate additional focused personas using pattern in `implementations/factor-10-focused-agents/supervisor-pattern.md`.

## 4. Context Engineering Layer
### Markdown Knowledge Base Strategy
- KB Path: `{{KB_PATH}}` (e.g. `kb/` directory of `.md` files).
- Flow: user query → normalize → scan markdown headers (lines starting with `#`) and paragraphs → score by keyword frequency + recency → collect top N sections → optional summarization → generation.
- Section Identification: `file.md#Heading-Slug` reference stored with snippet.
- Caching: key=`mkb:{{HASH(query)}}` TTL configurable (default none).

### Memory Policy
- Short-Term: in-process map (key=`st:{{SESSION_ID}}`) storing recent KB snippets + summaries.
- Long-Term (Optional): curated summaries appended to `kb/session-insights.md` for human review.
- Eviction: drop oldest snippet if >50 or token utilization threshold exceeded.

### Prompt Template Pattern
```
SYSTEM: You are {{ROLE}}.
GOAL: {{GOAL}}
CONSTRAINTS: {{CONSTRAINTS}}
SCHEMA: {{SCHEMA_REF}}
MEMORY_SUMMARY: {{MEMORY_SNIPPET}}
EVIDENCE: {{EVIDENCE_BLOCK}}
```

### Example JSON Schema (`{{SCHEMA_NAME}}.json`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "{{SCHEMA_TITLE}}",
  "type": "object",
  "required": ["summary", "items", "sources"],
  "properties": {
    "summary": {"type": "string", "maxLength": 2000},
    "items": {
      "type": "array",
      "items": {"type": "object", "required": ["id", "text"], "properties": {"id": {"type": "string"}, "text": {"type": "string"}}}
    },
    "sources": {
      "type": "array",
      "items": {"type": "object", "required": ["url", "confidence"], "properties": {"url": {"type": "string"}, "confidence": {"type": "number", "minimum": 0, "maximum": 1}}}
    },
    "meta": {"type": "object", "additionalProperties": true}
  }
}
```

### 4.1 Session Log Addendum
Log KB lookups under `## KB Access` then append context summary under `## Reasoning`. Error compaction (Factor 9) appends an `## Errors` section with structured fields: `{ "error_type": "ValidationError", "affected_field": "items[2].id", "remediation": "Regenerate item IDs" }`.

## 5. Minimal Agent Manifests
### `orchestrator.yaml`
```yaml
id: {{ORCH_ID}}
role: orchestrator
model: {{MODEL}}
allowed_tools:
  - plan_tasks
  - dispatch_agent
  - aggregate_results
memory_policy:
  ttl_hours: {{TTL_ORCH}}
input_schema: {{ORCH_INPUT_SCHEMA}}
output_schema: {{ORCH_OUTPUT_SCHEMA}}
logging:
  level: {{LOG_LEVEL}}
  sink: file
```

### `researcher.yaml`
```yaml
id: {{RESEARCHER_ID}}
role: researcher
model: {{MODEL}}
allowed_tools:
  - md_lookup
  - web_search
  - parse_document
  - classify
memory_policy:
  ttl_hours: {{TTL_RESEARCH}}
input_schema: {{RESEARCH_INPUT_SCHEMA}}
output_schema: {{RESEARCH_OUTPUT_SCHEMA}}
knowledge_base:
  path: {{KB_PATH}}
  max_sections: {{MAX_SECTIONS}}
```

### `verifier.yaml`
```yaml
id: {{VERIFIER_ID}}
role: verifier
model: {{MODEL}}
allowed_tools:
  - schema_validate
  - cross_check
  - fact_consistency
memory_policy:
  ttl_hours: {{TTL_VERIFY}}
input_schema: {{VERIFY_INPUT_SCHEMA}}
output_schema: {{VERIFY_OUTPUT_SCHEMA}}
policy:
  min_confidence: {{MIN_CONFIDENCE}}
  require_sources: true
```

## 6. Integration Notes for {{PROJECT_STACK}}
- Runtime Placement: `src/agents/{{LANGUAGE}}/` (loader: `loader.{ext}`, server: `server.{ext}`).
- Environment Variables: define in `.env`; load early (`load_env()` before agent construction); examples: `MODEL_API_KEY={{SECRET_KEY}}`, `VECTOR_DB_URL={{DB_URL}}`.
- Markdown KB: external runtime implements scanner that loads headings & sections from `{{KB_PATH}}`.
- Tool Wiring: implement adapters in `src/tools/` each exporting a `run(payload) -> {"result":...,"cost":...}`.
- Logging & Tracing: structured JSON to `logs/agent.jsonl` + optional OTLP exporter (`{{OTLP_ENDPOINT}}`).
- Error Handling: verifier triggers remediation path; orchestrator retries with `retry_count` < {{MAX_RETRIES}}.
- Multi-Agent Reference: See `implementations/factor-10-focused-agents/supervisor-pattern.md` for scaling beyond triad.
-- Observability: Connect OTLP exporter if {{OTLP_ENDPOINT}} set; otherwise file-only.

## 7. TODO Checklist
1. Replace all placeholders ({{PROJECT_NAME}}, {{MODEL}}, {{KB_PATH}}, {{DB_URL}}, etc.).
2. Create markdown KB directory `{{KB_PATH}}` with initial docs.
3. Implement `src/agents/loader.{ext}` to parse YAML manifests.
4. Write tool adapters (`md_lookup`, `web_search`, `schema_validate`).
5. Add JSON Schemas to `schemas/` matching `{{ORCH_OUTPUT_SCHEMA}}`, etc.
6. Set up `.env` with {{SECRET_KEY}}, {{DB_URL}}, {{LOG_LEVEL}}.
7. Add KB indexing helper (optional precomputed heading map).
8. Implement caching layer (optional) for KB lookups.
9. Add tests for manifest parsing, md_lookup scoring & schema validation.
10. Connect tracing exporter if using {{OTLP_ENDPOINT}}.

---

Template generated. Replace all {{PLACEHOLDER}} values.
