# docs/ Directory

**Purpose**: Externalized domain knowledge for the postgres-schema-specialist agent

---

## Contents

| File | Description |
|------|-------------|
| `domain-expertise.md` | Workflow phases, retry logic, token budgets, integration points |

---

## Shared Documentation

Database knowledge shared with postgres-timescale-specialist:

| Shared Doc | Location | Contents |
|------------|----------|----------|
| Crash Prevention | `.claude/skills/database-optimization/reference/postgres-crash-prevention-patterns.md` | Patterns to avoid in schema design |

**Do NOT duplicate shared content here** - reference it from the main agent definition.

---

## See Also

- **Main agent**: `../postgres-schema-specialist.md`
- **Examples**: `../examples/delegation-examples.md`
- **Schema**: `../schemas/postgres-schema-specialist.schema.json`
