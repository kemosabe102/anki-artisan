# Usage Examples

Complete usage scenarios for `/analyze-agent`.

---

## Example 1: Single Agent by Name

```bash
/analyze-agent researcher-external
```

**What happens**:
1. Resolves to `.claude/agents/research/researcher-external/researcher-external.md`
2. Launches 4 agents in parallel
3. Runs Claude Code validations
4. Synthesizes findings
5. Generates comprehensive report

**Expected output** (abbreviated):
```
Agent Analysis Report: researcher-external

Analysis Date: 2025-01-15T10:30:00Z
Overall Confidence: 0.92

## Executive Summary
researcher-external demonstrates strong prompt quality (Grade: A) with 
well-structured methodology sections. Key improvement opportunity: 
reduce token count by 15% through base-pattern inheritance.

## Overall Quality Score: 87/100
Grade: B

| Dimension | Score | Grade |
|-----------|-------|-------|
| Prompt Quality | 92 | A |
| Schema Design | 85 | B |

| Documentation | 78 | C |
| Integration | 90 | A |
| Methodology | PASS | - |

## Top 3 Findings (P1)
1. Missing base-pattern inheritance - 1,150 tokens recoverable
2. Verbose examples in methodology section - 230 tokens
3. Missing Quick Reference section

Token Savings: 1,380 tokens (15% reduction)
```

---

## Example 2: Single Agent by Path

```bash
/analyze-agent .claude/agents/dev-tools/debugger.md
```

**Use case**: When agent name is ambiguous or you want to analyze a specific file.

**Expected output**: Same format as Example 1, with path shown in report header.

---

## Example 3: CLAUDE.md Orchestrator Analysis

```bash
/analyze-agent CLAUDE.md
```

**What changes**:
- Adapted validations (see `docs/claude-md-mode.md`)
- Higher token threshold (~10K acceptable)
- Safety Information Accessibility audit
- Formula consistency check (ASC/DCS/CQ)


**Expected output** (abbreviated):
```
Orchestrator Analysis Report: CLAUDE.md

## Orchestrator Health Score: 82/100

## Safety Information Accessibility
- BANNED operations: Line 45 (GOOD - within first 50)
- ALWAYS directives: Line 89 (GOOD - within first 100)

## Formula Consistency
- ASC formula: CONSISTENT (3 definitions match)
- DCS formula: CONSISTENT (2 definitions match)
- CQ formula: WARNING (threshold 0.85 vs 0.8 in one location)

## Redundancy Analysis
- Duplicate content detected: 3 sections
- Token waste: ~450 tokens

## Recommendations
1. Consolidate duplicate delegation examples
2. Fix CQ threshold inconsistency
3. Move verbose examples to external docs
```

---

## Example 4: Ecosystem-Wide Audit

```bash
/analyze-agent --all
```

**Duration**: ~2-4 hours (depends on agent count)

**Process**:
1. Discovers all agents in `.claude/agents/`
2. Batches agents (5 in parallel)
3. Generates individual reports
4. Creates ecosystem summary


**Expected output** (abbreviated):
```
Ecosystem Analysis Summary

Agents Analyzed: 38
Total Duration: 2h 15m

## Overall Ecosystem Health
Average Quality Score: 79/100
Total Token Savings Opportunity: 12,450 tokens

## Quality Distribution
- Grade A (90-100): 8 agents
- Grade B (80-89): 15 agents
- Grade C (70-79): 10 agents
- Grade D (60-69): 4 agents
- Grade F (<60): 1 agent

## Top 5 Agents Needing Attention
1. legacy-parser (Score: 52) - Major restructuring needed
2. old-validator (Score: 63) - Missing integrations
3. temp-helper (Score: 67) - No schema defined
4. quick-fix (Score: 68) - Poor documentation
5. data-loader (Score: 71) - Token inefficiency

## Ecosystem-Wide Patterns
- 12 agents missing base-pattern inheritance
- 8 agents with duplicate methodology content
- 5 agents missing Quick Reference sections

## Recommended Actions
1. Apply base-pattern inheritance to 12 agents (~13,800 tokens saved)
2. Consolidate methodology content into shared docs
3. Add Quick Reference to 5 agents
```

---

## Common Scenarios

| Scenario | Command | Notes |
|----------|---------|-------|
| New agent validation | `/analyze-agent new-agent-name` | Run after /create-agent |
| Quarterly audit | `/analyze-agent --all` | Schedule quarterly |
| Pre-promotion check | `/analyze-agent agent-name` | Before v0.x -> v1.x |
| Token optimization | `/analyze-agent agent-name` | Focus on savings section |
