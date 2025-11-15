# Compliance Checklist (Placeholder)

> Ensures agents align with context-engineering + 12FA operational rules.

## Required Before Execution
- Persona selected (`personas/PERSONA_CATALOG.md`)
- Session initialized (`templates/SESSION_LOG.md` created)
- Context health check performed
- Placeholder values replaced in manifests

## Validation Steps
1. Verify manifests schema compliance
2. Confirm environment variables loaded (.env)
3. Check markdown KB path exists (`{{KB_PATH}}`)
4. Ensure logging sink configured
5. Run schema validation tests

## Remediation
- Missing persona → halt & request selection
- Failed health check → trim/summarize then re-run
- KB path missing → create directory & add README.md

## Logging Format
```markdown
[COMPLIANCE] status=ok missing=[] ts={{ISO_TIMESTAMP}}
```
