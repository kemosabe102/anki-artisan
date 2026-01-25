# Common Documentation References

**Purpose**: Links to shared documentation that applies to library-research skill

---

## Core Framework References

| Document | Purpose | Key Sections |
|----------|---------|--------------|
| [Context7 Usage Guide](/docs/shared/mcp/context7-usage-guide.md) | Complete Context7 reference | Tool usage, best practices, examples |
| [Orchestrator Thresholds](/.claude/docs/00-core/orchestrator-thresholds.md) | CQ formulas, confidence scoring | CQ calculation, thresholds |
| [OODA Loop Framework](/.claude/docs/00-core/ooda-loop-framework.md) | Phase-based methodology | OBSERVE, ORIENT phases |
| [Research Patterns](/.claude/docs/00-core/research-patterns.md) | General research methodology | Compression, source quality |
| [Research Skill Escalation](/.claude/docs/01-guides/research/research-skill-escalation.md) | Cross-skill handoffs | Codebase → Library → Web chain |

---

## Context7 Quick Reference

From context7-usage-guide.md:

### Tool Selection

| Tool | Purpose |
|------|---------|
| `resolve-library-id` | Match library name → Context7 ID |
| `get-library-docs` | Fetch documentation with topic filtering |

### Quality Thresholds

| Metric | Threshold | Action |
|--------|-----------|--------|
| Trust Score | ≥ 7 | Proceed with Context7 |
| Trust Score | < 7 | Escalate to web-research |
| Snippet Count | ≥ 100 | Adequate coverage |

### Mode Selection

| Mode | Use For |
|------|---------|
| `code` | API references, code examples |
| `info` | Conceptual guides, architecture |

---

## CQ Formula (Library Research)

From orchestrator-thresholds.md:

```
CQ = Domain×0.4 + Pattern×0.3 + Dependency×0.2 + Risk×0.1
```

**Library-specific scoring:**
- **Domain (0.4)**: Found relevant library? Trust score adequate?
- **Pattern (0.3)**: Retrieved API patterns? Examples match use case?
- **Dependency (0.2)**: Version compatibility? Integration requirements?
- **Risk (0.1)**: Deprecated methods? Breaking changes? Security advisories?

---

## Compression Guidelines

From research-patterns.md:

| Content Type | Compression Ratio | Method |
|--------------|-------------------|--------|
| API signatures | 2:1 | Extract signature + description |
| Code examples | 3:1 | Key pattern only, remove boilerplate |
| Configuration | 4:1 | Required options only |
| Changelog | 10:1 | Breaking changes only |

---

## Escalation Triggers

From research-skill-escalation.md:

**Escalate to web-research when:**
- Library not in Context7 index (trust score N/A)
- Trust score < 7 (insufficient documentation quality)
- Need community patterns not in official docs
- Need production deployment patterns
- Need comparative analysis across projects

**Escalate to codebase-research when:**
- Need to see how library is currently used in project
- Need to check existing integration patterns
- Need to verify version compatibility with project
