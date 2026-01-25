# examples/ Directory

**Purpose**: Concrete usage patterns for loki-query-specialist

---

## Contents

| File | Purpose | Audience |
|------|---------|----------|
| `delegation-examples.md` | How orchestrator delegates to this agent | Orchestrator, other agents |
| `output-template.md` | Standard SUCCESS/FAILURE output formats | Agent validation |

---

## Quick Reference

### Orchestrator Delegation
```markdown
Task(loki-query-specialist,
  "Construct a query to extract error logs from the API service.
   Log sample: {json log example}
   Extraction goal: Count errors by status code over time")
```

### Expected Output
- Constructed LogQL query with test results
- Parser selection rationale with performance evidence
- Anti-pattern detection results (if issues found)
- Confidence score (0-1)

---

## See Also

- **Main agent**: `../loki-query-specialist.md`
- **Schema**: `../schemas/loki-query-specialist.schema.json`
- **Orchestrator patterns**: `.claude/docs/03-workflows/orchestrator-workflow.md`
