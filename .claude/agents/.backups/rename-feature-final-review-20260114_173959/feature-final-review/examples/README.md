# Feature Final Review Examples

## Overview

This directory contains delegation examples for the feature-final-review agent.

## Files

| File | Description |
|------|-------------|
| `delegation-examples.md` | Task() invocation examples for both modes |

## Quick Reference

### Detect Mode

```markdown
Task(integration-boundary-reviewer, prompt="MODE: detect
Feature: packages/alpha-phase-01/")
```

### Review Mode

```markdown
Task(integration-boundary-reviewer, prompt="MODE: review
Pair: {\"id\": 1, \"upstream\": \"Provider\", \"downstream\": \"Normalizer\", ...}")
```

See `delegation-examples.md` for complete examples with expected outputs.
