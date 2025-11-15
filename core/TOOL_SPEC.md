# Tool Specification Template (YAML)

Use this template to declare tools available to agents. External runtimes should ingest these definitions and enforce schemas/permissions.

```yaml
id: {{TOOL_ID}}
name: {{HUMAN_NAME}}
description: {{WHAT_IT_DOES}}
inputs:
  type: object
  required: [{{REQ_FIELDS}}]
  properties:
    {{FIELD_NAME}}:
      type: string
      description: {{FIELD_DESC}}
outputs:
  type: object
  required: [ok]
  properties:
    ok:
      type: boolean
    data:
      type: object
      additionalProperties: true
    meta:
      type: object
      additionalProperties: true
safety:
  rate_limit: {{N_PER_MIN}}
  pii_allowed: false
permissions:
  allowed_roles: [orchestrator, researcher, verifier]
```
