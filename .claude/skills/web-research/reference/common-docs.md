# Common Documentation - Web Research Skill

**Version**: 1.0.0 | **Last Updated**: 2025-12-13

---

## Overview

This document provides links to shared documentation used by the web-research skill.

---

## Perplexity MCP Usage

**Location:** `docs/shared/mcp/perplexity-mcp-usage-guide.md`

**Contents:**
- Perplexity MCP server configuration
- Tool API reference (`search`, `reason`, `deep_research`)
- Cost optimization strategies (4:1 Context7:Perplexity ratio)
- Error handling and retry patterns
- Rate limiting and quota management

**When to Reference:**
- Implementing Perplexity tool calls
- Debugging MCP connection issues
- Understanding cost implications
- Query parameter tuning

---

## Orchestrator Thresholds

**Location:** `.claude/docs/00-core/orchestrator-thresholds.md`

**Contents:**
- CQ (Context Quality) formula and thresholds
- ASC (Agent Selection Confidence) calculations
- Research depth decision matrix
- Escalation trigger values

**When to Reference:**
- Determining research depth (CQ < 0.5 = deep research)
- Calculating confidence scores for findings
- Deciding when to escalate to user
- Multi-source validation requirements

---

## Research Patterns

**Location:** `.claude/docs/00-core/research-patterns.md`

**Contents:**
- Progressive depth pattern (search → reason → deep_research)
- Parallel validation pattern (multi-source cross-reference)
- Hypothesis-driven research workflow
- Synthesis and reporting guidelines

**When to Reference:**
- Planning multi-phase research tasks
- Structuring complex investigations
- Synthesizing findings from multiple sources
- Reporting research outcomes

---

## Related Skill Documentation

### Web-Research Skill-Specific Docs

- `reference/tool-patterns.md` - Perplexity/WebSearch/WebFetch tool selection
- `reference/source-authority.md` - Domain scoring and credibility assessment
- `examples/example-simple.md` - Simple fact-finding scenario
- `examples/example-complex.md` - Multi-phase deep research scenario
- `templates/findings-template.md` - Output format for research findings

---

## External References

### Perplexity API Documentation

**URL:** https://docs.perplexity.ai/
**Use For:** Official API reference, model capabilities, rate limits

### Context7 (Library Research)

**Usage:** Via `researcher-external` agent (Context7 MCP integration)
**Priority:** Use Context7 FIRST (free) before Perplexity (paid)
**Ratio Target:** 4:1 Context7:Perplexity queries

---

## Usage Guidelines

**When to Consult Shared Docs:**
1. Before implementing new research workflows (check `research-patterns.md`)
2. When encountering Perplexity errors (see `perplexity-mcp-usage-guide.md`)
3. When calculating confidence scores (use formulas from `orchestrator-thresholds.md`)
4. For cost optimization strategies (follow 4:1 ratio in `perplexity-mcp-usage-guide.md`)

**Document Updates:**
- Shared docs are maintained by orchestrator/core agents
- Skill-specific docs (this directory) maintained by web-research skill users
- Report broken links or outdated content via `.claude/docs/00-core/escalation-protocol.md`

---

## Quick Reference Map

```
Query Optimization ──> tool-patterns.md (this skill)
Source Validation ──> source-authority.md (this skill)
Perplexity API ──────> docs/shared/mcp/perplexity-mcp-usage-guide.md
CQ Calculations ─────> .claude/docs/00-core/orchestrator-thresholds.md
Research Workflow ───> .claude/docs/00-core/research-patterns.md
```
