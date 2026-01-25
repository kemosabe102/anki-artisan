---
title: "Orchestrator Workflow"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Orchestrator Workflow

**Purpose**: Quick orchestration patterns reference | **Auto-loaded**: Throughout session

---

## Quick Reference

**OODA**: OBSERVE (parse) → ORIENT (Context_Quality: Domain×0.4+Pattern×0.3+Dependency×0.2+Risk×0.1) → DECIDE (select agents) → ACT (execute+verify)

**Domain→Agent**: `.claude/agents/**`→claude-code-ecosystem | `docs/**/SPEC.md`→planning | `packages/**`→development/debugger/code-quality | `tests/**`→code-quality/code-quality | Research→researcher-lead+workers

**Performance**: Fast(<30s): planning, planning | Medium(1-2min): planning, architecture

**Rules**: ALWAYS respect domains, ORIENT before DECIDE | NEVER parallel `.claude/**` (locking)

---

## Agent Selection

<agent_selection>
  <extract>Paths→Domains</extract>
  <framework_80>Domain clear→Framework: Domain-first|Work type|Disambiguation</framework_80>
  <dcs_20>Unclear→DCS calculation</dcs_20>
</agent_selection>

**Reference**: `agent-selection-protocol-reference.md`

---

## Parallel Execution

**Rule**: Parallel for independent, sequential for `.claude/**`

✅ **Parallel** (3-5x): Multiple files (different dirs) | Research | Multi-agent analysis
❌ **Sequential**: `.claude/**` mods (locking) | Dependencies

**Limits**: MAX 5 file mods, MAX 5 research, 3-10 review

**Reference**: `parallel-execution-protocol.md`

---

## Agent Capabilities

**Orchestrator**:
- **Claude Code orchestrator** - Primary coordination + .claude directory manager (Role 2). OODA: 5/44/20/31 (ORIENT-heavy). Delegates domain-specific .claude operations to specialists (claude-code-ecosystem for agents/**, workflow for commands/hooks/**, documentation for docs/**), executes general .claude/** operations directly.

**Top 10**: development (C+), code-quality (B+), debugger (A-), researcher-codebase (A-), planning (B+), architecture (B+), code-quality (B+), planning (A), architecture (B+), planning (B+)

**Domain Specialists**:

- market-data-specialist (v1.0, A) - Market data domain specialist for OHLCV validation, API integration (Alpaca/Polygon/Yahoo), Parquet compression optimization, SQLAlchemy data model design. Delegates database administration to infrastructure agents.
- sentiment-nlp-specialist (v0.1, MVP) - Financial NLP specialist for FinBERT sentiment analysis, zS/zΔS normalization, burst detection, theme extraction from news/earnings. OODA Phase: ORIENT (44% - sentiment pattern discovery, statistical validation).

**Reference**: `agent-capability-reference.md` (32+ agents)

---

## Utility Agents

**context-optimizer** (`/optimize-claude-md`): CLAUDE.md optimization using token budget control and reference extraction

**source-control** (`/git`): Git/GitHub operations - analyze_changes (file grouping), execute_commits (Conventional Commits), monitor_ci (GitHub Actions)

**feature-analyzer** (`/tasks`): Feature specification comparison with overlap analysis, used for multi-component validation

---

## Workflow Patterns

**7-Phase**: Spec→Plan→Architecture→Implementation→Testing→Review→Cleanup

**Optimized** (3-5x): Parallel enhancement→Architecture review→Parallel tasks

**Reference**: `planning-workflow-patterns.md`

---

## Code Reuse

**Rule**: Component Almanac→Extend>Modify>Replace>Create

**Thresholds**: Reuse:80-95% | Extension:60-80% | Replacement:negative | **>50% savings required**

**Reference**: `code-reuse-workflow-integration.md`

---

## Delegation & Verification

**6-Step**: PRE-DELEGATION→INITIAL ATTEMPT→VERIFICATION→ANALYSIS→SECOND ATTEMPT→ESCALATION

**Reference**: `delegation-verification-protocol.md`

---

## Result Synthesis

**Trigger**: 3+ findings, overlap >0.7 → Apply `synthesis-and-recommendation-framework.md`

**Reference**: `.claude/docs/00-core/synthesis-and-recommendation-framework.md`

---

## Performance

**Wins**: planning: 70% (5min→<30s) | architecture: 70% (review-only)

**Rule**: Fast first (feedback)→Medium (mods)

**Reference**: `performance-optimization-case-studies.md`

---

## References

**Workflow**: agent-capability-reference.md | agent-performance-reference.md | agent-selection-protocol-reference.md | parallel-execution-protocol.md | planning-workflow-patterns.md | code-reuse-workflow-integration.md | delegation-verification-protocol.md | performance-optimization-case-studies.md

**Frameworks**: .claude/docs/01-guides/agents/agent-selection-guide.md | .claude/docs/00-core/ooda-loop-framework.md | .claude/docs/00-core/synthesis-and-recommendation-framework.md

---

**Quick-reference for orchestrator sub-agent coordination.**