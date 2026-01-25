# Sprint Grouping

Rules for assigning prioritized findings to sprints in remediation planning.

---

## Sprint Assignment Rules

| Sprint | Contents | Selection Criteria |
|--------|----------|-------------------|
| Sprint 1 | P1_quick_wins + urgent hotspots | Quick wins AND hotspot_score >7.0 |
| Sprint 2 | P2_strategic (dependencies resolved) | High impact, dependencies unblocked |
| Sprint 3+ | Remaining P2 + P4_opportunistic | Normal priority order |
| Backlog | P3_defer | Document only, exclude from sprints |

---

## Sprint 1: Quick Wins + Urgent

### Inclusion Criteria

Items qualify for Sprint 1 if:

1. **P1 Quick Wins**: Impact >=6 AND Effort <=4
2. **Urgent Hotspots**: hotspot_score >7.0 (regardless of quadrant)

### Capacity Planning

```
sprint_1_hours = sum(effort_hours for item in sprint_1_items)
max_capacity = team_size x hours_per_sprint x 0.3  # 30% for debt
```

If sprint_1_hours > max_capacity:
1. Prioritize by priority_score (highest first)
2. Move overflow to Sprint 2
3. Never move urgent hotspots (>7.0) out of Sprint 1

### Validation Checklist

- [ ] All P1 items have effort <4 hours
- [ ] Urgent hotspots (>7.0) included
- [ ] Total effort within sprint capacity
- [ ] No dependencies on unresolved items

---

## Sprint 2: Strategic Items

### Inclusion Criteria

Items qualify for Sprint 2 if:

1. **P2 Strategic**: Impact >=6 AND Effort >4
2. **Overflow from Sprint 1**: When capacity exceeded
3. **Dependencies resolved**: No blockers from Sprint 1

### Dependency Resolution

Before including P2 item, verify:
```
for dependency in item.dependencies:
    if dependency.sprint > current_sprint:
        move dependency to current_sprint OR
        defer item to dependency.sprint + 1
```

### Capacity Planning

P2 items often require dedicated capacity:
- Allocate 40-60% of debt budget to single P2 item
- Avoid splitting large items across sprints
- Consider pairing for complex refactoring

---

## Sprint 3+: Remaining Work

### Inclusion Criteria

1. **Remaining P2**: Items not fit in Sprint 2
2. **P4 Opportunistic**: Low impact, low effort items
3. **Deferred Sprint 1/2**: Capacity overflow

### Ordering

```
priority_order = sorted(items, key=lambda x: x.priority_score, reverse=True)
```

Apply P4 items when:
- Touching related code (Boy Scout Rule)
- Capacity available after P2 items
- Developer preference for variety

---

## Backlog: P3 Defer

### Handling P3 Items

P3 items (Low Impact, High Effort) should:

1. **Document**: Record in tech debt backlog
2. **Exclude**: Do NOT allocate sprint capacity
3. **Review**: Reassess quarterly for priority changes
4. **Promote**: Move to P2 if circumstances change

### Circumstances for Promotion

| Trigger | Action |
|---------|--------|
| New dependency | Reassess impact score |
| Security advisory | Reassess to P1/P2 |
| Performance regression | Reassess impact |
| Team capacity increase | Consider for inclusion |

---

## Assignment Algorithm

```python
def assign_sprints(findings: list) -> dict:
    """Assign findings to sprints based on quadrant and priority."""
    sprints = {"Sprint 1": [], "Sprint 2": [], "Sprint 3": [], "Backlog": []}
    
    # Sort by priority score descending
    sorted_findings = sorted(findings, key=lambda x: x.priority_score, reverse=True)
    
    for finding in sorted_findings:
        if finding.quadrant == "P3_defer":
            sprints["Backlog"].append(finding)
        elif finding.quadrant == "P1_quick_wins" or finding.hotspot_score > 7.0:
            sprints["Sprint 1"].append(finding)
        elif finding.quadrant == "P2_strategic":
            sprints["Sprint 2"].append(finding)
        else:  # P4_opportunistic
            sprints["Sprint 3"].append(finding)
    
    return sprints
```

---

## Common Mistakes

| Mistake | Impact | Prevention |
|---------|--------|------------|
| P2 items in Sprint 1 | Overcommitment | Sprint 1 is P1 + urgent hotspots only |
| Missing dependencies | Sprint failures | Check file references for shared modules |
| No capacity planning | Burnout | Calculate hours vs available capacity |
| Ignoring hotspot override | Delayed critical fixes | hotspot >7.0 always in Sprint 1 |
| P3 in active sprints | Wasted capacity | P3 goes to Backlog only |

---

## Output Format

### Sprint Summary

```json
{
  "sprints": {
    "Sprint 1": {
      "items": ["finding_id_1", "finding_id_2"],
      "total_effort_hours": 12,
      "quadrant_breakdown": {"P1": 3, "urgent_hotspot": 1}
    },
    "Sprint 2": {
      "items": ["finding_id_3"],
      "total_effort_hours": 40,
      "quadrant_breakdown": {"P2": 1}
    }
  },
  "backlog": {
    "items": ["finding_id_4"],
    "reason": "P3_defer - low ROI"
  }
}
```

---

## Cross-References

- **Quadrant Definitions**: [quadrant-classification.md](quadrant-classification.md)
- **Priority Formula**: [scoring-criteria.md](scoring-criteria.md)
- **Phase 3 DECIDE**: `.claude/agents/specialists/tech-debt-investigator/phases/phase-3-decide.md`
