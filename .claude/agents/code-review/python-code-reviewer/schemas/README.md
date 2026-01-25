# Python Code Reviewer Schemas

## Contents

| File | Purpose |
|------|---------|
| `python-code-reviewer.schema.json` | Agent output schema (extends base-agent.schema.json) |

## Schema Overview

The schema defines two output states:

### Success Output
- `review_verdict`: "OK" or "Changes Requested"
- `review_passed`: Boolean pass/fail
- `artifact_scope`: Files reviewed, surfaces affected
- `review_findings`: Array of findings with severity, confidence, gate evidence
- `recommendations`: Should-do, optional/later, tests, security, performance
- `context7_research_summary`: Libraries researched, validation results
- `rate_limit_compliance`: Counts per severity (enforces limits)

### Failure Output
- `failure_type`: Enum of known failure modes
- `reasons`: Array of failure reasons
- `research_attempted`: What was tried before failure
- `partial_results`: Any results gathered before failure
- `recovery_suggestions`: How to resolve the failure

## Base Schema Reference

Extends: `../../schemas/base-agent.schema.json`
