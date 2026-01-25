# Context Readiness Assessor - Examples

## Overview

This directory contains example scenarios demonstrating context-readiness-assessor behavior.

## Files

| File | Purpose |
|------|---------|
| `assessment-examples.md` | 3 scenarios: immediate PASS, 1-iteration PASS, BLOCKED after 3 iterations |

## Example Summary

| Scenario | Baseline CQ | Final CQ | Iterations | Outcome |
|----------|-------------|----------|------------|---------|
| JWT Auth (familiar domain) | 0.835 | 0.835 | 0 | PASS |
| Redis Caching (novel) | 0.410 | 0.650 | 1 | PASS |
| Vague "improve system" | 0.115 | 0.115 | 3 | BLOCKED |

## Delegation Pattern

Orchestrator invokes this agent after intent-analyzer (OBSERVE phase):

```
Task(context-readiness-assessor, {
  "task_description": "...",
  "domain_scope": ["packages/...", "tests/..."],
  "requirements": { "explicit": [...], "implicit": [...] }
})
```
