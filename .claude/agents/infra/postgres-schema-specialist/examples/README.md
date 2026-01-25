# examples/ Directory

**Purpose**: Concrete usage patterns showing how this agent is called and what it produces

---

## Contents

| File | Purpose | Audience |
|------|---------|----------|
| `delegation-examples.md` | How orchestrator delegates to this agent | Orchestrator, other agents |

---

## Quick Reference

### Trigger This Agent When
- New table/schema design needed
- Database migrations required
- TimescaleDB hypertable setup
- Index strategy design (structure, not optimization)
- Constraint design (CHECK, UNIQUE, FK)
- Backup/recovery strategy planning

### Don't Use This Agent For
- Query creation → `postgres-timescale-specialist`
- Query optimization → `postgres-timescale-specialist`
- EXPLAIN ANALYZE → `postgres-timescale-specialist`
- Production deployment → `k8s-deployment`
- Application code → `python-code-implementer`

---

## See Also

- **Main agent**: `../postgres-schema-specialist.md`
- **Domain expertise**: `../docs/domain-expertise.md`
- **Schema**: `../schemas/postgres-schema-specialist.schema.json`
