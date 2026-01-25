# Repository Analyst Integration Patterns

## Orchestrator Delegation

### Trigger Conditions
- "Generate component inventory"
- "Check if agent X exists" (pre-creation validation)
- "Show documentation coverage" (audit baseline)
- "Analyze ecosystem gaps"

### Delegation Context
```json
{
  "context": "Generate full component inventory",
  "output_format": "json",
  "scope": {
    "include_agents": true,
    "include_commands": true,
    "include_hooks": true,
    "include_skills": true
  }
}
```

---

## Downstream Consumers

### agent-architect (Pre-Creation Validation)
**Flow**: agent-architect → repository-analyst → similarity check → recommendation
**Use Case**: Before creating new agent, check for duplicates
**Output**: Top 5 matches with similarity scores (0.0-1.0)
**Recommendation**: CREATE_NEW | EXTEND_EXISTING | MERGE_WITH

### doc-librarian (Documentation Audit)
**Flow**: doc-librarian → repository-analyst → inventory → coverage analysis
**Use Case**: Validate documentation completeness
**Output**: Component inventory as baseline for coverage calculation

### context-optimizer (Ecosystem Analysis)
**Flow**: context-optimizer → repository-analyst → statistics → gap analysis
**Use Case**: OODA phase distribution, domain coverage
**Output**: Distribution percentages for ecosystem optimization

---

## Authority Hierarchy

Repository-analyst provides **advisory** recommendations only:
1. **User** - Final authority
2. **Domain specialist** (agent-architect, doc-librarian) - Decision authority
3. **repository-analyst** - Advisory data provider

---

## Data Flow Patterns

### Direct Pass-Through
```
orchestrator → repository-analyst → JSON inventory → downstream agent
```

### Cached Inventory
```
repository-analyst → .claude/docs/reports/inventory.json
downstream agents → read from cache (TTL: 1 hour)
```

### Cache Refresh Triggers
- Component file created/modified/deleted
- User explicit request ("refresh inventory")
- Cache TTL expiration (1 hour)
