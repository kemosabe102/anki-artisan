# docs/ Directory

**Purpose**: Externalized domain knowledge for the postgres-timescale-specialist agent

---

## Contents

| File | Description |
|------|-------------|
| `domain-expertise.md` | Workflow phases, retry logic, token budgets, integration points |

---

## Shared Documentation

Most database knowledge is in **shared locations** (used by multiple agents):

| Shared Doc | Location | Contents |
|------------|----------|----------|
| Query Optimization | `.claude/skills/postgres-timescaledb/reference/timescaledb-query-optimization.md` | Chunk exclusion, fixed dates, caching |
| Crash Prevention | `.claude/skills/database-optimization/reference/postgres-crash-prevention-patterns.md` | Crash-prone queries, safe alternatives |

**Do NOT duplicate shared content here** - reference it from the main agent definition.

---

## See Also

- **Main agent**: `../postgres-timescale-specialist.md`
- **Examples**: `../examples/delegation-examples.md`
- **Schema**: `.claude/docs/schemas/postgres-timescale-specialist.schema.json`
