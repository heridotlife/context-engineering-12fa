# Changelog

All notable changes to this repository will be documented in this file. Adheres to Keep a Changelog format (simplified) and semantic-ish versioning while experimental.

## [0.2.3] - 2025-11-09
### Changed
- Removed deprecated `./personas/` directory; all personas now sourced exclusively from `./agents/`.
- Updated `AGENTIC_GUIDE.md` persona section to "Pick the Right Persona" table; eliminated local core fallback references.
- Bumped spec_version to 0.2.3.

### Updated
- `schemas/context-contract.json` persona description now requires match in `./agents/` only; updated example `spec_version`.

### Removed
- Local persona template files (developer, reviewer, planner, integrator, maintainer).

## [Unreleased]
### Added
- `schemas/sample-context.toon` as a TOON-formatted example of the context payload.
- **Temporal Awareness (Date/Time Access)** section in `AGENTIC_GUIDE.md` under Operational Constraints, documenting how agents detect and use system date/time.
- Updated Execution Footer in `AGENTIC_GUIDE.md` to initialize and record session date/time at start.
- **Session Memory Management (SESSION_LOG.md)** section with structured scratchpad pattern (Task, Plan, Reasoning, Tool Calls, State Checkpoints, Token Usage, Health Check, Trace).
- **Context Compression & Trimming** section with auto-summarization (50% threshold), trimming (before every LLM call), and selective tool post-processing.
- **Context Isolation (State Management)** section with exposed vs isolated state schema and best practices.
- **Context Health Monitoring** section with metrics (token utilization, message count, contradictions, staleness, completeness) and remediation actions.
- **Multi-Agent Architecture** section with supervisor pattern, context handoffs, parallel execution, and when-to-use guidance.
- **Observability & Tracing** section with token tracking (on-demand), reasoning traces (persona-dependent), verbosity levels, privacy filtering, and export formats.
- `SESSION_LOG.md` template file for session-scoped state and reasoning.
- `SPEC_CLARIFICATIONS.md` documenting all 10 implementation decisions with best practices research.

### Changed
- Temporal Awareness section now prioritizes **local system date/time** over UTC for user-facing operations (version checks, dependency updates, changelog entries, file timestamps).
- Added explicit use cases and timezone priority guidance to Temporal Awareness section.
- README TOON section now references agent procedure (no external script).
- **Bumped spec_version to 0.3.0** (major capability additions).
- Execution Footer now includes 8 steps: temporal context, SESSION_LOG init, health check, persona selection, task parsing, execution, output, archival.
- Updated README with v0.3.0 features: Session Management, Context Health, Multi-Agent Workflows, Observability.

### Removed
- Deprecated `scripts/json_to_toon.py` (replaced by documented agent-native conversion workflow in `AGENTIC_GUIDE.md`).

### Documentation
- Added "Agent‑native TOON Conversion & Validation" section to `AGENTIC_GUIDE.md`.
- All new sections aligned with 12-Factor Agent principles and Context Engineering best practices from LangChain, Anthropic, and LangGraph.

## [0.2.3] - 2025-11-09
### Added
- Integrated specialized persona catalog via `./agents/` and documented selection rules in `AGENTIC_GUIDE.md`.
- Starter JSON Schema `schemas/context-contract.json` for validating context inputs.
- This `CHANGELOG.md` file.

### Changed
- Bumped `spec_version` in `AGENTIC_GUIDE.md` to 0.2.2 and added links to `./agents/`.
- Clarified persona activation flow and extended-vs-core persona guidance.

## [0.2.1] - 2025-11-09
### Added
- Table of Contents and cleaned structure in `AGENTIC_GUIDE.md`.
- Core fallback personas: `./personas/developer.md`, `reviewer.md`, `planner.md`, `integrator.md`, `maintainer.md`.

### Changed
- Refined 12FA table with objectives and compliance signals.

## [0.2.0] - 2025-11-09
### Added
- Initial persona-activation model and lifecycle framing.

