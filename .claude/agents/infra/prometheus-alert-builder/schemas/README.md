# Prometheus Alert Builder - Schemas

Input/output contract definitions.

## Contents

| Document | Purpose |
|----------|---------|
| [prometheus-alert-builder.schema.json](./prometheus-alert-builder.schema.json) | Full input/output schema for alert operations |

## Operation Types

- `construct_alert` - Build new alert rule from intent
- `validate_alert` - Check existing alert against anti-patterns
- `tune_alert` - Optimize noisy/flapping alert
