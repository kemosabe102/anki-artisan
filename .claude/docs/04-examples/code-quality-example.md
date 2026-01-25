# Example 2: Code Quality Improvements

**Scenario**: Multiple agents review authentication code

## Agent Findings

```yaml
code-quality:
  - 'Extract authentication logic into separate service'
  - 'Add input validation for credentials'

tech-debt-investigator:
  - 'High coupling between auth and routes'
  - 'Duplicate password validation in 3 places'

development:
  - 'Consolidate validation into shared module'
  - 'Use dependency injection for auth service'
```

## Overlap Detection

```yaml
OverlapGroup 1:
  problem: 'Authentication architecture'
  findings: [code-quality "extract service", development "use DI"]

OverlapGroup 2:
  problem: 'Validation duplication'
  findings:
    [
      code-quality "add validation",
      tech-debt "duplicate validation",
      development "consolidate",
    ]
```

## Synthesis Output

```markdown
## Problem 1: Authentication Architecture

### Recommendation: ✅ Extract Auth Service (No DI Yet)

**Score**: 1.40 vs 0.60

- Extract to service: Impact 4/5, Effort 2/5, Risk Low
- Add DI: Impact 3/5, Effort 4/5, Risk Medium
- **Rationale**: Service extraction provides 80% of benefits without DI complexity

---

## Problem 2: Validation Duplication

### Recommendation: ✅ Consolidate with Pydantic Models

**Score**: 1.50 vs 0.30 vs 0.40

- Pydantic models: Impact 5/5, Effort 2/5, Risk Low (already in use)
- Shared module: Impact 4/5, Effort 4/5, Risk Medium (new abstraction)
- Generic validators: Impact 3/5, Effort 3/5, Risk Medium (overengineered)
- **Rationale**: Pydantic already in codebase, eliminates duplication with minimal effort
```
