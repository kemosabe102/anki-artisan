---
name: evaluating-claude-md
description: >
  CLAUDE.md quality evaluation with parallel agent delegation. Assesses 
  orchestrator configuration across 7 dimensions (structure, context management, 
  agent config, phase quality, standards, validation, architecture). Produces 
  graded A-F report (70 points total).
  
  4-phase workflow: Load → Delegate 7 agents → Synthesize → Report.
  Trigger: "evaluate CLAUDE.md", "/analyze-claude-md"
  
  NOT for: Documentation ecosystem health (doc-librarian), individual agent 
  quality assessment (agent-quality-evaluation skill), feature/system SPEC.md 
  reviews (spec-reviewer), general documentation content creation.
---

# CLAUDE.md Quality Evaluation

**Framework**: 70 points across 7 dimensions (10 pts each)

## Quick Reference

| D# | Dimension | Agent | Focus |
|----|-----------|-------|-------|
| D1 | Structure | research | File size, identity, phases |
| D2 | Context Management | research | One-Read Rule, token budget |
| D3 | Agent Configuration | claude-code-ecosystem | Specialists, selection |
| D4 | Phase Quality | planning | OODA checklists, exit criteria |
| D5 | Quality Standards | code-quality | Code truth, approval gates |
| D6 | Practical Validation | research | Tested, readable, accessible |
| D7 | Agent Architecture | claude-code-ecosystem | Inheritance, parallelization |

---

## Phase 1: Load Context (Orchestrator)

You MUST complete these steps before Phase 2:

1. Read `CLAUDE.md` from project root
2. Count lines (target: <200)
3. Read `reference/dimension-rubrics.md` for scoring criteria
4. Proceed to Phase 2

---


## EXECUTE: Phase 2 Delegation (7 Parallel Agents)

**CRITICAL**: You MUST spawn these 7 agents in parallel using Task().
Do NOT evaluate dimensions yourself. Delegate to specialists.

### Delegation Contract

```json
{
  "phase": "P2_EVALUATE",
  "execution": "parallel",
  "max_agents": 7,
  "sync_point": "Wait for ALL agents to complete before Phase 3",
  "agents": [
    {
      "id": "D1",
      "dimension": "Structure",
      "agent_type": "research",
      "prompt": "Evaluate CLAUDE.md structure (D1). Read reference/dimension-rubrics.md#d1. Score: file size <200 lines (2pts), read-only coordinator stated (2pts), project identity (2pts), phases defined (2pts), agents listed (2pts). Return JSON: {dimension: 'D1', score: 0-10, criteria_met: [], findings: [], recommendations: []}",
      "input": "CLAUDE.md path + dimension-rubrics.md#d1",
      "output": "DimensionReport JSON"
    },
    {
      "id": "D2",
      "dimension": "Context Management",
      "agent_type": "research",
      "prompt": "Evaluate CLAUDE.md context management (D2). Read reference/dimension-rubrics.md#d2. Score: One-Read Rule (4pts), token budget strategy (3pts), anti-patterns listed (3pts). Return JSON: {dimension: 'D2', score: 0-10, criteria_met: [], findings: [], recommendations: []}",
      "input": "CLAUDE.md path + dimension-rubrics.md#d2",
      "output": "DimensionReport JSON"
    },
    {
      "id": "D3",
      "dimension": "Agent Configuration",
      "agent_type": "claude-code-ecosystem",
      "prompt": "Evaluate CLAUDE.md agent configuration (D3). Read reference/dimension-rubrics.md#d3. Score: research specialists (2pts), planning specialists (2pts), implementation specialists (2pts), selection guidance (2pts), capability descriptions (2pts). Return JSON: {dimension: 'D3', score: 0-10, criteria_met: [], findings: [], recommendations: []}",
      "input": "CLAUDE.md path + dimension-rubrics.md#d3",
      "output": "DimensionReport JSON"
    },
    {
      "id": "D4",
      "dimension": "Phase Quality",
      "agent_type": "planning",
      "prompt": "Evaluate CLAUDE.md phase quality (D4). Read reference/dimension-rubrics.md#d4. Score: OBSERVE checklist (2pts), ORIENT checklist (2pts), ACT checklist (2pts), exit criteria testable (2pts), handoff artifacts (2pts). Return JSON: {dimension: 'D4', score: 0-10, criteria_met: [], findings: [], recommendations: []}",
      "input": "CLAUDE.md path + dimension-rubrics.md#d4",
      "output": "DimensionReport JSON"
    },
    {
      "id": "D5",
      "dimension": "Quality Standards",
      "agent_type": "code-quality",
      "prompt": "Evaluate CLAUDE.md quality standards (D5). Read reference/dimension-rubrics.md#d5. Score: Code Truth requirement (3pts), Code Snippets requirement (3pts), human approval gates (2pts), blocker escalation (2pts). Return JSON: {dimension: 'D5', score: 0-10, criteria_met: [], findings: [], recommendations: []}",
      "input": "CLAUDE.md path + dimension-rubrics.md#d5",
      "output": "DimensionReport JSON"
    },
    {
      "id": "D6",
      "dimension": "Practical Validation",
      "agent_type": "research",
      "prompt": "Evaluate CLAUDE.md practical validation (D6). Read reference/dimension-rubrics.md#d6. Score: successfully tested (3pts), readable <2min (2pts), agent specs path (2pts), documentation map (2pts), rigor adjustment (1pt). Return JSON: {dimension: 'D6', score: 0-10, criteria_met: [], findings: [], recommendations: []}",
      "input": "CLAUDE.md path + dimension-rubrics.md#d6",
      "output": "DimensionReport JSON"
    },
    {
      "id": "D7",
      "dimension": "Agent Architecture",
      "agent_type": "claude-code-ecosystem",
      "prompt": "Evaluate CLAUDE.md agent architecture (D7). Read reference/dimension-rubrics.md#d7. Score: inheritance model (2pts), tool lane enforcement (2pts), handoff protocol (2pts), parallelization rules (2pts), context budget & recovery (2pts). Return JSON: {dimension: 'D7', score: 0-10, criteria_met: [], findings: [], recommendations: []}",
      "input": "CLAUDE.md path + dimension-rubrics.md#d7",
      "output": "DimensionReport JSON"
    }
  ]
}
```


### How to Execute This Contract

For each agent in the contract above, call:

```
Task(agent_type, """
Goal: [prompt from contract]
Map: CLAUDE.md, .claude/skills/evaluating-claude-md/reference/dimension-rubrics.md
Constraints: Return structured JSON only. No prose. Include evidence quotes.
""")
```

Launch all 7 agents in a SINGLE message with multiple Task() calls.

---

## Phase 3: Synthesis (Orchestrator)

After ALL 7 agents return, you MUST:

1. Collect dimension scores from each agent's JSON output
2. Calculate total: `sum(D1...D7)` out of 70
3. Assign grade: A (63-70), B (56-62), C (49-55), D (42-48), F (<42)
4. Extract top findings and recommendations
5. Proceed to Phase 4

---

## Phase 4: Report (Orchestrator)

Generate final report with:

1. **Executive Summary**: Score, grade, health status
2. **Dimension Table**: All 7 scores with pass/warn/fail status
3. **Gaps Identified**: Critical > Important > Suggestions
4. **Recommendations**: Prioritized by impact/effort (P1 > P2 > P3)

Output format: Markdown (default) or JSON if requested.

---


## Grading Scale

| Score | Grade | Status |
|-------|-------|--------|
| 63-70 | A | Production-ready |
| 56-62 | B | Strong, minor fixes |
| 49-55 | C | Good foundation |
| 42-48 | D | Needs work |
| <42 | F | Major revision |

**Dimension Status**: ✅ Pass (>=8) | ⚠️ Warn (5-7) | ❌ Fail (<5)

---

## Reference Files

- `reference/dimension-rubrics.md` - D1-D7 scoring criteria
- `reference/output-schema.md` - JSON output contract
- `reference/scoring-methodology.md` - How to apply rubrics

---

## Anti-Patterns (NEVER DO)

- Evaluate dimensions yourself instead of delegating
- Skip agents or run fewer than 7
- Return prose instead of structured JSON
- Score without evidence quotes
- Ignore the delegation contract
