# Context Optimizer Delegation Examples

**Purpose**: Examples of analysis outputs and targeting modes for orchestrator delegation.

---

## Example Output Structure

```markdown
# Context Optimization Analysis Report

## Executive Summary

- Total tokens analyzed: 55,723
- Optimization potential: 25,000 tokens (45%)
- Critical findings: 2
- High-priority recommendations: 4

## Findings

### F1: MCP Tool Bloat (CRITICAL)

- **Location**: .claude/settings.json
- **Tokens Wasted**: 60,000
- **Description**: Loading 70+ tools, using only 12
- **Impact**: 39.5% of context consumed before work begins

### F2: Agent Redundancy (HIGH)

- **Location**: .claude/agents/*.md
- **Tokens Wasted**: 8,836 (17% of agent definitions)
- **Description**: Common sections duplicated across 18-20 agents

## Recommendations

### R1: MCP Tool Reduction (P1)

- **Savings**: 60,000 tokens (75% overhead reduction)
- **Effort**: 1 hour (config change)
- **Risk**: 0.1 (very low)
- **ROI**: 10.4x
- **Steps**:
  1. Audit actual tool usage
  2. Create selective tool config
  3. Update .claude/settings.json

## Implementation Plan

### Phase 1: Quick Wins (Week 1)
- R1: MCP tool reduction (60K savings)

### Phase 2: Consolidation (Week 2)
- R3: Base agent pattern creation (9K savings)
```

---

## Targeting Mode Examples

### Example 1: Single Agent Quick Feedback

**Use Case**: Quick feedback on newly created agent (2-3 min)

**Delegation**:
```
Task(context-optimizer, "Analyze context usage for context-optimizer agent. 
Provide token count, top findings, and quick wins.")
```

**Input**:
```json
{
  "scope": "agents",
  "target_agents": ["context-optimizer"],
  "depth": "quick"
}
```

**Expected Output**:
```markdown
## Executive Summary

- Selected agents: 1 (context-optimizer)
- Targeting mode: specific
- Total tokens analyzed: 3,425
- Optimization potential: 380 tokens (11%)
- Duration: ~2-3 minutes

## Findings

### F1: Verbose Examples Section (MEDIUM)
- Location: context-optimizer.md
- Tokens: 215 (6% of agent)
- Description: Example section could be condensed

## Recommendations

### R1: Consolidate Examples (P2)
- Savings: 150 tokens
- Effort: 15 minutes
- ROI: 2.5x
```

---

### Example 2: Pattern-Based Group Analysis

**Use Case**: Analyze all researcher agents for consistency (8-10 min)

**Delegation**:
```
Task(context-optimizer, "Analyze all researcher-* agents for consistency 
and redundancy. Identify consolidation opportunities.")
```

**Input**:
```json
{
  "scope": "agents",
  "target_agents": "researcher-*",
  "depth": "standard"
}
```

**Expected Output**:
```markdown
## Executive Summary

- Selected agents: 3 (researcher-lead, researcher-codebase, researcher-external)
- Targeting mode: pattern
- Total tokens analyzed: 12,840
- Optimization potential: 2,150 tokens (17%)

## Findings

### F1: Duplicated Workflow Sections (HIGH)
- Location: All 4 researcher agents
- Tokens: 1,680 (13% duplication)
- Description: Phase 1-3 workflow structure near-identical

## Recommendations

### R1: Extract Common Researcher Workflow (P1)
- Savings: 1,500 tokens
- Effort: 1.5 hours
- ROI: 4.2x
```

---

### Example 3: Ecosystem-Wide Comprehensive Review

**Use Case**: Full ecosystem optimization (60-85 min)

**Delegation**:
```
Task(context-optimizer, "Perform comprehensive ecosystem analysis. 
Analyze all agents, CLAUDE.md, and MCP configuration. 
Generate full optimization roadmap with phased implementation plan.")
```

**Input**:
```json
{
  "scope": "full",
  "target_agents": "all",
  "depth": "comprehensive"
}
```

---

## Targeting Mode Comparison

| Mode | Input | Agents | Sampling | Duration | Use Case |
|------|-------|--------|----------|----------|----------|
| **all** | `"all"` | All in ecosystem | Yes (5-10) | 60-85 min | Comprehensive review |
| **specific** | `["a1", "a2"]` | 2-10 specific | NO | 2-10 min | Targeted feedback |
| **pattern** | `"researcher-*"` | Glob matched | IF >10 | 8-20 min | Group consistency |

**Key Insight**: Targeted analysis provides 6-28x faster feedback for focused tasks.

---

## Agent Analysis Suite Integration

When analyzing 3+ agents simultaneously, context-optimizer can be included in the Agent Analysis Suite:

```
# Launch in parallel with other analysis agents
Task(agent-architect, "Evaluate structure compliance...")
Task(prompt-evaluator, "Assess prompt quality...")
Task(context-optimizer, "Analyze token usage across [agent list]...")
Task(doc-reference-optimizer, "Check reference efficiency...")
```

**See**: `agent-analysis-suite-protocol.md` for complete suite workflow.

---

**Usage**: Reference these examples when delegating to context-optimizer or understanding output formats.
