---
name: operational-reliability
description: >
  Operator and Historian reliability review for observability and maintainability.
  Evaluates observability (log quality, metric exposure, configurability) and
  maintainability (cognitive load, dependency hygiene). Use for: operational readiness
  validation. Trigger keywords: operational reliability, observability, logs, metrics,
  maintainability, cognitive load.
allowed-tools: Read, Glob, Grep
---

# Operational Reliability Skill

**Purpose**: Systematic checklist for evaluating operational readiness (Operator + Historian hats).

**Use Cases**:
- Log quality assessment
- Metric exposure validation
- Kill switch / feature flag verification
- Cognitive load evaluation
- Dependency hygiene check

## Source Documents

This skill derives its checklists from:
- `.claude/docs/01-guides/review/operational-edge-reliability.md`

---

## Checklist Categories

### 1. Observability (Operator Hat)

| Check | Severity | Evidence Pattern |
|-------|----------|------------------|
| Logs explain "why" not just "what" | MEDIUM | Look for context values in log statements |
| New features expose metrics | LOW | Check for metric registration, counters |
| Hardcoded values moved to config | MEDIUM | Look for magic numbers, feature flags |

### 2. Maintainability (Historian Hat)

| Check | Severity | Evidence Pattern |
|-------|----------|------------------|
| Cognitive load acceptable (readable in one pass) | LOW | Count nesting levels, function length |
| Dependency hygiene (minimal imports) | LOW | Check import count, external deps |


---

## Four Hats Context

This skill covers two hats from the Four Hats methodology:

| Hat | Focus | Checks |
|-----|-------|--------|
| **Operator** | Can we understand production? | Logs, metrics, configurability |
| **Historian** | Will this be maintainable? | Cognitive load, dependencies |

---

## Reference Files

- `reference/observability-checklist.md` - Operator hat checks
- `reference/maintainability-checklist.md` - Historian hat checks

## Related Skills

- `edge-reliability` - Graph Theorist hat (edge boundaries)
- `node-reliability` - Lawyer hat (node contracts)
