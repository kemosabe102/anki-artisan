# Common Documentation References

**Purpose**: Links to shared documentation that applies to codebase-research skill

---

## Core Framework References

| Document | Purpose | Key Sections |
|----------|---------|--------------|
| [Orchestrator Thresholds](/.claude/docs/00-core/orchestrator-thresholds.md) | CQ formulas, confidence scoring | CQ calculation, thresholds |
| [OODA Loop Framework](/.claude/docs/00-core/ooda-loop-framework.md) | Phase-based methodology | OBSERVE, ORIENT phases |
| [Research Patterns](/.claude/docs/00-core/research-patterns.md) | General research methodology | Compression, source quality |
| [Research Skill Escalation](/.claude/docs/01-guides/research/research-skill-escalation.md) | Cross-skill handoffs | Codebase → Library → Web chain |

---

## Tool-Specific References

| Document | Purpose | Relevance |
|----------|---------|-----------|
| [File Operation Protocol](/.claude/docs/01-guides/file-ops/file-operation-protocol.md) | Read/Write best practices | Read chunking strategies |
| [Tool Selection Guide](/.claude/docs/01-guides/tool-selection-guide.md) | When to use which tool | Glob vs Grep vs Read |
| [Desktop Commander Best Practices](/.claude/docs/01-guides/integration/desktop-commander-best-practices.md) | MCP file operations | Advanced file reading |
| [Tool Parallelization Patterns](/.claude/docs/01-guides/performance/tool-parallelization-patterns.md) | Parallel tool execution | Parallel reads, sequential writes |

---

## CQ Formula (Codebase Research)

From orchestrator-thresholds.md:

```
CQ = Domain×0.4 + Pattern×0.3 + Dependency×0.2 + Risk×0.1
```

**Codebase-specific scoring:**
- **Domain (0.4)**: Found relevant files? Understanding of module structure?
- **Pattern (0.3)**: Identified coding patterns, conventions, idioms?
- **Dependency (0.2)**: Mapped imports, function calls, class hierarchies?
- **Risk (0.1)**: Identified edge cases, error handling, security concerns?

---

## Compression Guidelines

From research-patterns.md (lines 190-206):

| Content Type | Compression Ratio | Method |
|--------------|-------------------|--------|
| Code snippets | 3:1 | Extract signature + key logic |
| File lists | 10:1 | Group by pattern/purpose |
| Function chains | 5:1 | Call graph summary |
| Error patterns | 2:1 | Categorize by type |

---

## Escalation Triggers

From research-skill-escalation.md:

**Escalate to library-research when:**
- Need official API documentation for external library
- Version-specific behavior questions
- Library best practices not in codebase

**Escalate to web-research when:**
- Community patterns not in official docs
- Production deployment patterns
- Comparative analysis across projects
