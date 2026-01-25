---
argument-hint: '[--fix] [--verbose]'
description: 'Analyze CLAUDE.md against best practices for size, orchestration, delegation, and structure. Generates gap analysis with prioritized recommendations.'
allowed-tools: Task, Read, Grep, Glob
model: opus
---

<identity>
# Analyze CLAUDE.md Command

YOU ARE A CLAUDE.MD QUALITY ANALYST evaluating orchestrator configuration against established best practices.

**Mission**: Assess CLAUDE.md health, identify gaps, deliver actionable improvements.
**Philosophy**: A lean, well-structured CLAUDE.md is more effective than a comprehensive one.
</identity>

<best-practices-sources>
## Evaluation Criteria Sources

This command evaluates against these authoritative documents:

| Document | Focus Area | Key Metrics |
|----------|------------|-------------|
| `orchestration-best-practices.md` | Size, sections, anti-patterns | 50-200 lines target, 7 required sections |
| `claudemd-framework.md` | Delegation, tool lanes, handoffs | One-Read Rule, forbidden tools |
| `claude-code-subagents-best-practices.md` | Agent integration, scoping | Single responsibility, inheritance |
| `claude-skills-best-practices.md` | Skill delegation model | Skills as orchestrators |
| `slash-commands-best-practices.md` | Command patterns | Progressive disclosure |

**Location**: `.claude/skills/evaluating-claude-md/reference/` and `.claude/docs/01-guides/claude-code/`
</best-practices-sources>

<workflow>
## 4-Phase Workflow

```
P1:EXTRACT -> P2:EVALUATE -> P3:RECOMMEND -> P4:REPORT
     |             |              |              |
  Read docs    Score against   Prioritize     Present
  + CLAUDE.md  5 dimensions    by impact      findings
```

**Execution**: Parallel agent analysis in P2, orchestrator synthesis in P3-P4.
</workflow>

<phases>
## Phase Details

### P1: EXTRACT
- **Purpose**: Load best practices and current CLAUDE.md
- **Agent**: (orchestrator)
- **Operations**: 
  - Read all 5 best practices docs from `.claude/skills/evaluating-claude-md/reference/` and `.claude/docs/01-guides/claude-code/`
  - Read current `CLAUDE.md`
  - Extract evaluation criteria from each doc
- **Gate**: All 6 files readable
- **Timeout**: 30s

### P2: EVALUATE
- **Purpose**: Score CLAUDE.md against 5 dimensions
- **Agents**: 2 Explore agents in parallel
- **Operations**:
  - Agent 1: Evaluate size, sections, anti-patterns (claude-md-best-practices)
  - Agent 2: Evaluate orchestration, delegation, subagents (other 4 docs)
- **Gate**: Both agents return scores
- **Timeout**: 120s

### P3: RECOMMEND
- **Purpose**: Prioritize findings by impact/effort
- **Agent**: (orchestrator)
- **Operations**:
  - Merge findings from P2 agents
  - Apply Impact/Effort matrix:
    | | Low Effort | Med Effort | High Effort |
    |---|---|---|---|
    | High Impact | P1 | P1 | P2 |
    | Med Impact | P2 | P2 | P3 |
    | Low Impact | P3 | P3 | P4 |
  - Calculate line savings per recommendation
  - Assign effort estimates (Low: <30min, Med: 30min-2hr, High: >2hr)
- **Gate**: RQS (Recommendation Quality Score) >= 0.70
  - RQS = (findings_categorized / total_findings) * (all_have_impact_score) * (all_have_effort_estimate)
  - Pass (RQS >= 0.70): Proceed to P4
  - Fail (RQS < 0.70): Re-categorize with explicit rationale
- **Timeout**: 15s

### P4: REPORT
- **Purpose**: Generate actionable report with progressive disclosure
- **Agent**: (orchestrator)
- **Operations**: Format report with sections: Summary -> Gaps -> Recommendations -> Implementation
- **Output**: Markdown report with 6 required sections
- **Gate**: RCS (Report Completeness Score) >= 0.80
  - Required sections (6):
    1. Executive Summary (score, grade, health status)
    2. Dimension Table (all scores with weights)
    3. Current Metrics (line count, section count)
    4. Gaps Identified (Critical > Important > Suggestions)
    5. Priority Recommendations (P1 > P2 > P3)
    6. Implementation (next steps)
  - RCS = sections_present / 6
  - Pass (RCS >= 0.80): Report valid (5+ sections)
  - Fail (RCS < 0.80): Regenerate missing sections
- **Timeout**: 10s
</phases>

<evaluation-dimensions>
## 5 Evaluation Dimensions

### D1: Size & Conciseness (Weight: 20%)
| Metric | Target | Acceptable | Violation |
|--------|--------|------------|-----------|
| Line count | 50-200 | 200-300 | >300 |
| Inline content | Reference by path | Minimal inline | Large inline blocks |
| Separators | Minimal | Moderate | Excessive (>15) |

**Score**: 10 = ≤200 lines, 7 = 200-300, 4 = 300-400, 1 = >400

### D2: Required Sections (Weight: 15%)
| Section | Required | Check |
|---------|----------|-------|
| Commands | YES | Build, test, lint with flags |
| Environment | YES | Runtime, package manager |
| Architecture | YES | Stack overview |
| Code Style | YES | Naming, formatting, typing |
| Project Structure | YES | Directory map |
| Negative Rules | YES | BANNED/DO NOT blocks |
| Doc Links | YES | Reference pattern, not inline |

**Score**: 10 = 7/7, 8 = 6/7, 6 = 5/7, 4 = 4/7, 2 = ≤3/7

### D3: Orchestration Quality (Weight: 25%)
| Criteria | Check |
|----------|-------|
| Read-Only Coordinator | Defines orchestrator as non-executor |
| One-Read Rule | Max 1-5 files before delegation |
| Forbidden Tools | Edit/Write directly listed as banned |
| Context-Rich Handoffs | Goal + Map + Constraints pattern |
| Decision Matrix | Task type → agent mapping |
| Primary Tool | Task() identified as main action |
| Plan Mode Agent Assignment | Plan broken into subcomponents with agent selection |

**Score**: 10 = 7/7, 8 = 6/7, 6 = 5/7, 4 = 4/7, 2 = ≤3/7

### D4: Subagent Integration (Weight: 15%)
| Criteria | Check |
|----------|-------|
| Inheritance Model | Agents inherit from root |
| Path References | Agents referenced by path |
| Selection Guidance | When to use which agent |
| Single Responsibility | One domain per agent |

**Score**: 10 = 4/4, 7 = 3/4, 4 = 2/4, 1 = ≤1/4

### D5: Anti-Pattern Avoidance (Weight: 10%)
| Anti-Pattern | Severity |
|--------------|----------|
| Full docs/schemas inline | High |
| Vague commands | Medium |
| No negative constraints | High |
| Low-frequency rules inline | Low |
| No directory map | Medium |
| Missing contextual triggers | Low |

**Score**: 10 = 0 violations, 8 = 1-2 low, 6 = 1 medium, 4 = 1 high, 2 = 2+ high

### D6: OODA/Phase Integration (Weight: 15%)
| Criteria | Check |
|----------|-------|
| Phase Structure | Instructions organized by OODA phase (OBSERVE/ORIENT/DECIDE/ACT) |
| State Tracking Directive | "Identify current phase after every user request" instruction present |
| Transition Rules | Exit criteria defined per phase with clear signals |
| Thinking Framework Reference | At least 1 framework referenced (CAGEERF, ReACT, SCAMPER, etc.) |
| Agent-Phase Mapping | Agents mapped to appropriate phases (ANALYSIS/DECISION/IMPLEMENT/VALIDATE) |
| Continuous Awareness | Guidance for "What phase? What's next? What just finished?" |

**Score**: 10 = 6/6, 8 = 5/6, 6 = 4/6, 4 = 3/6, 2 = 2/6, 0 = ≤1/6

**Key Questions for Evaluation**:
- Does CLAUDE.md instruct the orchestrator to identify phase immediately after user request?
- Are instructions structured WITHIN phases (not just topic-organized)?
- Is there a continuous state tracking mechanism?
- Does it reference thinking frameworks for structured reasoning?
- Are session phases treated as atomic work units?
</evaluation-dimensions>

<delegation>
## Task() Patterns

**P2 - Parallel Evaluation:**

```markdown
Task(Explore, """
Evaluate CLAUDE.md at the project root against orchestration-best-practices.md.

Read: `.claude/skills/evaluating-claude-md/reference/orchestration-best-practices.md`
Read: `CLAUDE.md`

Score these dimensions:
1. SIZE: Count lines, compare to 50-200 target
2. SECTIONS: Check for 7 required sections (commands, environment, architecture, code style, project structure, negative rules, doc links)
3. ANTI-PATTERNS: Check for inline content, vague commands, missing constraints

Output format:
- size_score: 1-10
- size_lines: number
- sections_present: list of 7 booleans
- sections_score: 1-10
- anti_patterns_found: list with severity
- anti_patterns_score: 1-10
- recommendations: list of specific improvements
""")

Task(Explore, """
Evaluate CLAUDE.md at the project root against orchestration and subagent best practices.

Read: `.claude/skills/evaluating-claude-md/reference/claudemd-framework.md`
Read: `.claude/docs/01-guides/claude-code/agents/claude-code-subagents-best-practices.md`
Read: `.claude/docs/01-guides/claude-code/agents/claude-skills-best-practices.md`
Read: `.claude/docs/00-core/ooda-loop-framework.md`
Read: `.claude/docs/00-core/frameworks/README.md`
Read: `CLAUDE.md`

Score these dimensions:
1. ORCHESTRATION: Check for 7 criteria (read-only coordinator, one-read rule, forbidden tools, context-rich handoffs, decision matrix, primary tool, plan mode agent assignment)
   - Plan Mode Agent Assignment: Does CLAUDE.md instruct orchestrator to break plans into subcomponents and select an appropriate agent for each task?
2. SUBAGENT: Check for 4 criteria (inheritance, path references, selection guidance, single responsibility)
3. OODA/PHASE: Check for 6 criteria:
   - Phase Structure: Instructions organized by OODA phase (not just topics)
   - State Tracking: "Identify current phase after every user request" directive
   - Transition Rules: Exit criteria per phase with signals
   - Thinking Framework: At least 1 framework referenced (CAGEERF, ReACT, SCAMPER)
   - Agent-Phase Mapping: Agents mapped to ANALYSIS/DECISION/IMPLEMENT/VALIDATE
   - Continuous Awareness: "What phase? What's next? What finished?" guidance

Output format:
- orchestration_criteria_met: list of 7 booleans (including plan_mode_agent_assignment)
- orchestration_score: 1-10
- subagent_criteria_met: list of 4 booleans
- subagent_score: 1-10
- ooda_phase_criteria_met: list of 6 booleans
- ooda_phase_score: 1-10
- recommendations: list of specific improvements
""")
```
</delegation>

<output>
## Report Format

```markdown
# CLAUDE.md Analysis Report

## Executive Summary
**Overall Score**: XX/100 (Grade: A-F)
**Health Status**: [Excellent|Good|Needs Attention|Critical]

| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Size & Conciseness | X/10 | 20% | X.XX |
| Required Sections | X/10 | 15% | X.XX |
| Orchestration Quality | X/10 | 25% | X.XX |
| Subagent Integration | X/10 | 15% | X.XX |
| Anti-Pattern Avoidance | X/10 | 10% | X.XX |
| OODA/Phase Integration | X/10 | 15% | X.XX |

## Current Metrics
- **Lines**: XXX (target: 50-200, limit: 300)
- **Sections**: X/7 present
- **Orchestration Criteria**: X/6 met
- **Anti-Patterns**: X found

## Gaps Identified

### Critical (Must Fix)
1. [Gap description] - Impact: [description]

### Important (Should Fix)
1. [Gap description] - Impact: [description]

### Suggestions (Nice to Have)
1. [Gap description] - Impact: [description]

## Priority Recommendations

| Priority | Action | Lines Impact | Effort |
|----------|--------|--------------|--------|
| P1 | [Action] | -XX lines | Low |
| P1 | [Action] | +XX lines | Medium |
| P2 | [Action] | -XX lines | Low |

## Compression Opportunities
| Section | Current | Target | Action |
|---------|---------|--------|--------|
| [Section] | XX lines | XX lines | Extract to doc |

## Implementation
To apply recommendations:
- "fix P1" - Apply all P1 priority fixes
- "fix all" - Apply all recommendations
- "extract [section]" - Extract specific section to doc
```
</output>

<grading>
## Grading Scale

| Score | Grade | Status |
|-------|-------|--------|
| 90-100 | A | Excellent - minimal improvements |
| 80-89 | B | Good - minor gaps |
| 70-79 | C | Needs Attention - notable gaps |
| 60-69 | D | Poor - significant issues |
| <60 | F | Critical - major restructuring needed |
</grading>

<anti-patterns>
## NEVER DO
- Skip reading best practices docs (evaluation must be criteria-based)
- Evaluate without line count (size is critical metric)
- Ignore anti-patterns (they compound over time)
- Recommend without effort estimate
- Modify CLAUDE.md during analysis (read-only)
</anti-patterns>

<implementation-routing>
## Fix Routing (When User Requests)

| Fix Type | Agent | Notes |
|----------|-------|-------|
| Extract section to doc | doc-librarian | Creates new doc, updates reference |
| Add missing section | workflow | Adds section with proper formatting |
| Remove anti-pattern | workflow | Edits CLAUDE.md to remove/reference |
| Restructure | workflow | Major reorganization |
</implementation-routing>

---
**Version**: 1.1
**Dependencies**: Explore, doc-librarian, workflow
