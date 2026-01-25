# Debugger Agent Schemas

This directory contains the JSON schema contract for the debugger agent.

## Contents

| File | Purpose |
|------|---------|
| `debugger.schema.json` | Input/output contract for all debugger operations |

## Schema Overview

The debugger schema extends `base-agent.schema.json` and supports three operation types:

- **debug**: Standard hypothesis-driven debugging with RCA
- **validate_pre_commit**: Autonomous pre-commit validation with retry loop
- **fix_failing_tests**: Per-test OODA fix cycle

See the schema file for complete input/output specifications.
