# Template Usage Guidance (No Runtime Code)

This repository now serves purely as a markdown + YAML template layer for agentic AI systems. All execution/runtime logic must be provided by the consuming platform.

## Included Artifacts
- `core/AGENTIC_GUIDE.md` – Master specification & operational protocols
- `core/COMPLIANCE_CHECKLIST.md` – Pre-execution validation list
- `manifests/` – Agent role YAML skeletons (edit placeholders)
- `schemas/` – Example JSON schemas for outputs (optional)
- `kb/` – Knowledge base markdown documents (user-maintained)
- `templates/SESSION_LOG.md` – Session log template
- `personas/` – Persona catalog & persona files

## Excluded (Removed) Runtime Components
- Python loader / tool registry / runner scripts
- Dependency specification (`requirements.txt`)

## How to Integrate Externally
1. Copy or mount this directory into your application under `.agentic/`.
2. Parse YAML manifests using your platform's preferred language.
3. Implement a markdown section lookup tool analogous to `md_lookup` described in the guide (keyword scoring over headers & paragraphs).
4. Enforce compliance by reading `core/COMPLIANCE_CHECKLIST.md` before agent activation.
5. Use `schemas/` for structured output validation where applicable.
6. Maintain session logs with `templates/SESSION_LOG.md` structure.

## Placeholder Replacement Workflow
1. Perform a search for `{{` patterns.
2. Replace global project identifiers (`{{PROJECT_NAME}}`, `{{KB_PATH}}`, etc.).
3. Review manifests for model/tool keys.

## Minimal External Loader Pseudocode (Language-Agnostic)
```
load_env()
manifests = read_yaml_dir("manifests/")
persona = select_persona(user_task, catalog)
kb_sections = index_markdown("kb/")
session_log = init_session_log(template_path)
while task_open:
  plan = plan_tasks(user_task)
  sections = lookup(kb_sections, plan.keywords)
  draft = model.generate(context=compress(sections))
  validated = validate(draft, schemas.summary)
  if validated: break
finalize(session_log, draft)
```

## Updating the KB
- Add or modify markdown files under `kb/`.
- Prefer descriptive headings for improved lookup accuracy.
- Optionally maintain `kb/session-insights.md` as a curated knowledge evolution record.

## Versioning
Update `spec_version` in `AGENTIC_GUIDE.md` and record changes in `CHANGELOG.md` when structural template changes are made.

## Compliance Quick Checklist Snapshot
```
Persona Selected? YES/NO
Placeholders Replaced? YES/NO
KB Path Exists? YES/NO
Session Log Initialized? YES/NO
Health Check Performed? YES/NO
```

## Notes
Runtime execution intentionally out of scope; this keeps the repository lightweight, portable, and language-agnostic.
