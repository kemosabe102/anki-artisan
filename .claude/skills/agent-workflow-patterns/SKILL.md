---
name: agent-workflow-patterns
description: >
  7-pattern structural evaluation for agent definitions. Checks for mandatory workflow
  patterns: Mode Detection, OODA Workflow, Mode-Specific Sections, Anti-Patterns,
  Ask-First Rules, Output Structure, Role & Boundaries.
  Trigger keywords: workflow patterns, agent patterns, structural evaluation, pattern check.
---

# Agent Workflow Patterns Skill

Evaluate agents for 7 mandatory workflow patterns that ensure production readiness and consistent behavior.

## Reference Documentation

- **Pattern Rubrics** -> [reference/pattern-rubrics.md](reference/pattern-rubrics.md)
- **Evaluation Examples** -> [reference/evaluation-examples.md](reference/evaluation-examples.md)

---

## Quick Reference: 7 Mandatory Patterns

| P# | Pattern | Points | Key Criteria |
|----|---------|--------|--------------|
| P1 | **Mode Detection Table** | 10 | Table exists, Keywords → Skill mapping, Each mode → action |
| P2 | **OODA Workflow** | 10 | All 4 phases, 3-4 bullets per phase, ORIENT has skill invocation |
| P3 | **Mode-Specific Sections** | 10 | Section per mode, Step 1 = Skill invocation, Tool specification |
| P4 | **Anti-Patterns** | 10 | 4-6 explicit "NEVER DO", Includes phase-skipping prohibition |
| P5 | **Ask-First Rules** | 10 | 3-5 measurable conditions, Prevents runaway execution |
| P6 | **Output Structure** | 10 | SUCCESS + FAILURE templates, Confidence score, Recovery suggestion |
| P7 | **Role & Boundaries** | 10 | "Your Job" explicit, "Boundaries/NOT for" explicit, Output format |

**Total**: 70 points

---

## Grading Scale

| Score | Grade | Status |
|-------|-------|--------|
| 63-70 | A | All patterns present, production-ready |
| 56-62 | B | Most patterns present, minor gaps |
| 49-55 | C | Core patterns present, notable gaps |
| 42-48 | D | Missing key patterns, needs work |
| <42   | F | Missing multiple patterns, major revision |

**Pattern Status**: ✅ Pass (8-10) | ⚠️ Partial (4-7) | ❌ Missing (<4)

---

## Evaluation Workflow

### Step 1: Load Agent Definition

```
Input: Agent file path (.claude/agents/**/*.md)
Output: Parsed content, section headers identified
```

### Step 2: Check Each Pattern

For each of 7 patterns:
1. Search for pattern indicators (headers, tables, keywords)
2. Validate structure matches criteria
3. Score based on rubric (0-10)
4. Document evidence (quotes, line numbers)

### Step 3: Calculate Score

```
Total_Score = P1 + P2 + P3 + P4 + P5 + P6 + P7  (max 70)
Grade = map_to_grade(Total_Score)
```

### Step 4: Generate Report

Output includes:
- Overall grade (A-F)
- Per-pattern scores with evidence
- Missing patterns highlighted
- Improvement recommendations

---

## Pattern Evaluation Criteria (Inline Reference)

### P1: Mode Detection Table (10 pts)

**What to look for**: A markdown table mapping trigger keywords to skills/actions.

| Criteria | Points | Check |
|----------|--------|-------|
| Table exists with Mode column | 3 | `## Mode Detection` or similar header + table |
| Trigger Keywords column present | 3 | Keywords are specific, not vague |
| Primary Skill/Action column | 2 | Each mode maps to exactly one skill/action |
| Keywords are actionable | 2 | Not generic like "complex" or "general" |

**Example structure**:
```markdown
| Mode | Trigger Keywords | Primary Skill |
|------|------------------|---------------|
| `codebase` | "find code", "pattern" | codebase-research |
```

---

### P2: OODA Workflow (10 pts)

**What to look for**: All 4 OODA phases documented with concrete steps.

| Criteria | Points | Check |
|----------|--------|-------|
| OBSERVE phase present | 2 | Has section with parsing/input steps |
| ORIENT phase present | 3 | Has skill invocation, context loading |
| DECIDE phase present | 2 | Has planning/strategy steps |
| ACT phase present | 3 | Has execution steps, output generation |

**Required in ORIENT**: Explicit skill invocation instruction.

---

### P3: Mode-Specific Sections (10 pts)

**What to look for**: Dedicated section for each mode with step-by-step workflow.

| Criteria | Points | Check |
|----------|--------|-------|
| Section per mode declared in P1 | 4 | Headers like `## Codebase Mode` |
| Step 1 is skill invocation | 3 | "Invoke: Skill(X)" pattern |
| Tools specified per step | 2 | `Glob`, `Grep`, `Read` etc. |
| Return format specified | 1 | JSON structure or output template |

---

### P4: Anti-Patterns Section (10 pts)

**What to look for**: Explicit "NEVER DO" list with 4-6 items.

| Criteria | Points | Check |
|----------|--------|-------|
| Section header exists | 2 | `## Anti-Patterns` or `## NEVER DO` |
| 4-6 explicit behaviors listed | 4 | Bulleted list of prohibited actions |
| Forbids skipping skill invocation | 2 | "Never return without invoking skill" |
| Forbids skipping OODA phases | 2 | "Never skip OBSERVE/ORIENT" |

---

### P5: Ask-First Rules (10 pts)

**What to look for**: Conditions that require stopping and asking for clarification.

| Criteria | Points | Check |
|----------|--------|-------|
| Section header exists | 2 | `## Ask-First Rules` or `## Stop Conditions` |
| 3-5 specific conditions listed | 4 | Not vague, has thresholds |
| Conditions are measurable | 2 | Numbers, counts, specific triggers |
| Prevents runaway execution | 2 | Max iterations, scope limits |

**Example conditions**: "Scope exceeds 10 files", "Confidence < 0.50 after 3 rounds"

---

### P6: Output Structure (10 pts)

**What to look for**: Structured JSON templates for SUCCESS and FAILURE.

| Criteria | Points | Check |
|----------|--------|-------|
| SUCCESS template exists | 3 | JSON with status, agent, output fields |
| FAILURE template exists | 3 | JSON with failure_type, recovery fields |
| Confidence score included | 2 | Number 0.0-1.0 in output |
| Recovery suggestion in FAILURE | 2 | Actionable next step |

**Example structure**:
```json
{
  "status": "SUCCESS",
  "agent": "agent-name",
  "confidence": 0.88,
  "agent_specific_output": { ... }
}
```

---

### P7: Role & Boundaries (10 pts)

**What to look for**: Explicit scope definition with what agent does and doesn't do.

| Criteria | Points | Check |
|----------|--------|-------|
| "Your Job" or purpose explicit | 3 | Clear capability statement |
| "Boundaries" or "NOT for" explicit | 4 | What agent does NOT do |
| Output format specified | 3 | JSON, Markdown, specific schema |

**Example structure**:
```markdown
| Aspect | Details |
|--------|---------|
| **Your Job** | Execute research, compress findings |
| **Boundaries** | NO code modifications, NO file writes |
| **Output Format** | JSON with confidence and citations |
```

---

## Output Schema

### SUCCESS Response

```json
{
  "status": "SUCCESS",
  "agent": "agent-workflow-patterns",
  "confidence": 0.85,
  "agent_specific_output": {
    "total_score": 58,
    "grade": "B",
    "pattern_scores": {
      "P1_mode_detection": 8,
      "P2_ooda_workflow": 10,
      "P3_mode_sections": 7,
      "P4_anti_patterns": 9,
      "P5_ask_first": 6,
      "P6_output_structure": 10,
      "P7_role_boundaries": 8
    },
    "missing_patterns": ["P5 partial: only 2 conditions listed"],
    "recommendations": [
      "Add 2 more measurable ask-first conditions",
      "Expand mode-specific sections with tool specifications"
    ]
  }
}
```

### FAILURE Response

```json
{
  "status": "FAILURE",
  "agent": "agent-workflow-patterns",
  "agent_specific_output": {
    "failure_type": "agent_not_found",
    "attempted_path": ".claude/agents/nonexistent.md",
    "recovery_suggestion": "Verify agent path. Use Glob to find available agents."
  }
}
```

---

## Integration Notes

- **Used by**: `/analyze-agent` command (P1:DISCOVER phase)
- **Weight**: 20% of overall analyze-agent score
- **Enforcement**: Advisory only (surfaced in recommendations)
- **Delegation**: claude-code-ecosystem agent invokes this skill

---

## Common Issues

| Issue | Pattern Affected | Typical Score Loss |
|-------|------------------|-------------------|
| No mode detection table | P1 | -10 |
| Missing ORIENT phase | P2 | -3 to -5 |
| Anti-patterns section missing | P4 | -10 |
| No FAILURE output template | P6 | -5 |
| Vague boundaries | P7 | -4 to -7 |
