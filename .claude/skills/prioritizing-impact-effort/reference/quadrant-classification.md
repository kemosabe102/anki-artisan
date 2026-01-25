# Quadrant Classification

Impact/Effort matrix quadrant definitions for technical debt prioritization.

---

## P1-P4 Quadrant Matrix

| Quadrant | Impact | Effort | Action | Timeline |
|----------|--------|--------|--------|----------|
| P1 Quick Wins | High (>=6) | Low (<=4) | Do immediately | Sprint 1 |
| P2 Strategic | High (>=6) | High (>4) | Plan and resource | Sprint 2+ |
| P3 Defer | Low (<6) | High (>4) | Deprioritize | Backlog only |
| P4 Opportunistic | Low (<6) | Low (<=4) | Boy Scout Rule | When convenient |

---

## Quadrant Descriptions

### P1: Quick Wins (High Impact, Low Effort)

**Characteristics**:
- High business value or risk reduction
- Can be completed in <4 hours
- No complex dependencies
- Clear implementation path

**Examples**:
- Security vulnerability with simple fix
- Missing input validation on critical endpoint
- Performance hotspot with obvious optimization
- Critical bug with localized fix

**Action**: Execute immediately in Sprint 1.

### P2: Strategic (High Impact, High Effort)

**Characteristics**:
- Significant business value
- Requires substantial investment (>1 week)
- May have dependencies or require coordination
- Needs proper planning and resourcing

**Examples**:
- Major architectural refactoring
- Database schema migration
- Legacy system replacement
- Cross-cutting security overhaul

**Action**: Plan thoroughly, allocate dedicated resources, schedule for Sprint 2+.

### P3: Defer (Low Impact, High Effort)

**Characteristics**:
- Limited business value
- High implementation cost
- Often "nice to have" improvements
- ROI typically <1.0

**Examples**:
- Complete rewrite of working legacy code
- Cosmetic refactoring of stable modules
- Migrating to new framework for style preference

**Action**: Document for future consideration. Do NOT allocate sprint capacity.

### P4: Opportunistic (Low Impact, Low Effort)

**Characteristics**:
- Minor improvements
- Quick to implement
- Low risk
- Good for developer morale

**Examples**:
- Code style cleanup
- Minor documentation updates
- Renaming for clarity
- Adding logging statements

**Action**: Apply "Boy Scout Rule" - fix when touching related code.

---

## Assignment Algorithm

```python
def assign_quadrant(impact: float, effort: float) -> str:
    """Assign finding to P1-P4 quadrant."""
    if impact >= 6:
        return "P1_quick_wins" if effort <= 4 else "P2_strategic"
    else:
        return "P4_opportunistic" if effort <= 4 else "P3_defer"
```

---

## Urgency Override

Hotspot score >7.0 overrides normal quadrant assignment:

| Hotspot Score | Override Behavior |
|---------------|-------------------|
| >7.0 | Force into Sprint 1 regardless of quadrant |
| 5.0-7.0 | Consider for Sprint 1 if capacity allows |
| <5.0 | Normal quadrant-based assignment |

---

## Cross-References

- **Priority Score Formula**: See SKILL.md
- **Hotspot Calculation**: `.claude/skills/tech-debt-shared/FORMULAS.md` section 1
- **Sprint Grouping**: [sprint-grouping.md](sprint-grouping.md)
