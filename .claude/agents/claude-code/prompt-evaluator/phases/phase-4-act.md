# Phase 4: ACT - Report Generation & Output Validation

**OODA Stage**: ACT | **Time Allocation**: 15-20%

**Purpose**: Generate structured report, validate against schema, support batch evaluation

**Deliverable**: Validated JSON report per schema, batch processing workflow

---

## Workflow Steps

### Step 4.1: Report Assembly

**Input**: Scores, evidence, recommendations from Phases 1-3

**Process**:
1. Assemble JSON structure per `schemas/prompt-evaluator.schema.json`:
   - `agent_path`: Input path
   - `baseline_tokens`: From Phase 1
   - `framework_scores`: All 7 normalized scores with evidence
   - `overall_grade`: Letter grade A-F
   - `overall_score`: Numeric 0-5
   - `anti_patterns`: Detected patterns with severity
   - `recommendations`: Prioritized list with scores
   - `incomplete_dimensions`: Any gaps
   - `confidence`: Overall confidence score

**Output**: Complete JSON report structure


### Step 4.2: Output Validation

**Input**: Assembled JSON report

**Process**:
1. Validate against `schemas/prompt-evaluator.schema.json`
2. Verify all required fields present:
   - [ ] `agent_path` (string)
   - [ ] `baseline_tokens` (integer)
   - [ ] `framework_scores` (object with 7 keys)
   - [ ] `overall_grade` (A|B|C|D|F)
   - [ ] `overall_score` (number 0-5)
   - [ ] `recommendations` (array)
   - [ ] `confidence` (number 0-1)
3. Check evidence citations: all findings must have `file:line` format

**Output**: Validation pass/fail with any schema errors

### Step 4.3: Report Presentation

**Input**: Validated JSON report

**Process**:
1. Format summary section:
   - Overall grade with score
   - Token baseline and potential savings
   - Top 3 priority recommendations
2. Format detailed sections:
   - Per-framework scores with evidence
   - Anti-pattern findings with fix guidance
   - Full recommendation list

**Output**: Formatted evaluation report for user


---

## Batch Evaluation Workflow

**Trigger**: Multiple agent paths provided or `*.md` glob pattern

**Process**:
1. `Glob(".claude/agents/**/*.md")` - Collect all agent files
2. For each agent:
   - Run Phases 1-4 (OBSERVE -> ORIENT -> DECIDE -> ACT)
   - Capture individual report
   - Estimate ~20s per agent
3. Aggregate results:
   - Sort by overall_grade
   - Identify common anti-patterns across agents
   - Calculate fleet-wide statistics

**Output**: Individual reports + summary table

```
| Agent | Grade | Tokens | Top Issue |
|-------|-------|--------|-----------|
| agent-a.md | B | 2,400 | Missing schema |
| agent-b.md | C | 4,100 | Tool bloat |
```

---

## Quick Checklist

Before returning results:

- [ ] JSON validates against schema
- [ ] All findings have file:line citations
- [ ] Recommendations quantified with priority scores
- [ ] Confidence score reflects any gaps
- [ ] Summary formatted for user consumption

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Invalid JSON structure | Validate against schema before return |
| Missing citations | Every finding needs file:line evidence |
| Generic recommendations | Include token savings or priority score |
| No confidence reporting | Always include confidence, note incomplete_dimensions |

---

**Previous Phase**: [Phase 3: DECIDE](phase-3-decide.md)
**Complete**: Return to [prompt-evaluator.md](../prompt-evaluator.md)
