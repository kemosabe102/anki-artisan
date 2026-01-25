# Feature Final Review Documentation

## Overview

The integration-boundary-reviewer agent specializes in **integration boundary review** - analyzing data flow between components rather than component internals.

## Two Modes

| Mode | Purpose | Input | Output |
|------|---------|-------|--------|
| **detect** | Discover integration pairs via data flow adjacency | Feature directory path | `integration_pairs[]` array |
| **review** | Deep review of single pair for contract/error/edge issues | Integration pair JSON | `pair_findings{}` object |

## Mode Selection

- **Detect mode**: Use when you have a feature directory and need to identify all integration points
- **Review mode**: Use when you have a specific pair and need detailed findings

## Integration Checklist Categories

| Category | Check Focus | Severity if Failed |
|----------|-------------|-------------------|
| Contract Alignment | Output type A == Input type B | CRITICAL |
| Schema Compatibility | Field names match, types compatible | HIGH |
| Null/Optional Handling | A returns None -> B handles None | HIGH |
| Error Propagation | A raises X -> B catches OR propagates | MEDIUM |
| Edge Cases | Empty list, zero values, boundaries | MEDIUM |
| Performance | No N+1 queries, no unbounded loops | LOW |

## Gate Criteria

| Result | Condition |
|--------|-----------|
| PASS | Zero findings |
| PASS_WITH_CONDITIONS | Zero CRITICAL and <=3 HIGH |
| FAIL | Any CRITICAL or 4+ HIGH |
| SKIPPED | Zero pairs detected |

## Skill References

This agent uses the following skill files for detailed workflows:

| Skill File | Purpose |
|------------|---------|
| `.claude/skills/integration-boundary-reviewer/SKILL.md` | Main skill with workflow |
| `.claude/skills/integration-boundary-reviewer/reference/pair-detection-algorithm.md` | Detection algorithm details |
| `.claude/skills/integration-boundary-reviewer/reference/integration-checklist.md` | Per-pair checklist items |
| `.claude/skills/integration-boundary-reviewer/reference/gate-criteria.md` | Pass/fail thresholds |
| `.claude/skills/integration-boundary-reviewer/schemas/review-output.schema.json` | Skill output schema |

## Related Agents

| Agent | Relationship |
|-------|--------------|
| `python-code-reviewer` | Delegate for interface contract review |
| `architecture-reviewer` | Delegate for layer alignment validation |
| `test-executor` | Delegate for integration test coverage |
| `reliability-reviewer` | Delegate for Four Hats reliability analysis |
