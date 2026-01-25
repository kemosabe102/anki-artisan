---
name: agent-quality-evaluation
description: >
  9-criterion quality matrix for evaluating agent definitions. Use when assessing
  agent quality, conducting agent audits, or validating agent improvements.
  Trigger keywords: agent quality, evaluate agent, quality matrix, agent audit.
---

# Agent Quality Evaluation Skill

Systematic agent evaluation using a weighted 9-criterion quality matrix with simulation-driven assessment.

## Reference Documentation

- **Quality Matrix Rubric** -> [references/quality-matrix-rubric.md](references/quality-matrix-rubric.md)

---

## Quick Reference: Quality Matrix

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Correctness** | 0.25 | Task accuracy, external validation |
| **Format Fidelity** | 0.15 | Schema adherence, machine-parseable outputs |
| **Description-Capability Alignment** | 0.10 | Frontmatter accurately reflects capabilities |
| **Scope Discipline** | 0.10 | Avoids role drift, clear boundaries |
| **Tool Use Quality** | 0.10 | Appropriate tool selection/usage |
| **Reliability** | 0.10 | Stable performance across contexts |
| **Safety/Compliance** | 0.10 | No prohibited content, proper refusals |
| **Maintainability** | 0.10 | Prompt clarity, modularity, <500 lines |
| **Efficiency+Observability** | 0.05 | Cost optimization, structured logging |

---

## Grade Calculation

**Formula**: Weighted sum of all criterion scores (each 0-5)

```
Quality_Score = SUM(Criterion_Score x Weight) for all 9 criteria
```

| Grade | Score Range | Description |
|-------|-------------|-------------|
| **A** | 4.5-5.0 | Production ready, excellent performance |
| **B** | 3.5-4.4 | Good performance, minor improvements needed |
| **C** | 2.5-3.4 | Acceptable performance, notable issues |
| **D** | 1.5-2.4 | Poor performance, significant improvements required |
| **F** | 0.0-1.4 | Failing performance, major redesign needed |

---

## Simulation-Driven Development

### Core Principle

Think from the target agent's perspective BEFORE evaluation or creation.

### Process

1. **Perspective Shift**: What does this agent need to accomplish its goals?
2. **Tool Requirements**: Which tools are essential? What descriptions do they need?
3. **Work Phases**: Map out decision points and execution stages
4. **Failure Modes**: Identify edge cases and potential failures

### Tool Description Standards (Anthropic Best Practice)

- Write as if explaining to new team member
- Make implicit context explicit (query formats, terminology)
- Use unambiguous parameter names (`user_id` vs `user`)
- Disclose destructive changes or open-world access
- Include examples where helpful

---

## Framework Pattern Matching

Match agent type to appropriate framework:

| Agent Category | Primary Framework | When to Use |
|----------------|------------------|-------------|
| Research agents | ReACT | Iterative investigation loops |
| Implementation agents | CAGEERF | Complex multi-component tasks |
| Analysis/Review agents | 5W1H + DMAIC | Systematic analysis + measurement |
| Planning agents | CAGEERF + OKR | Comprehensive planning + goals |
| Debugging agents | ReACT + 5 Whys | Hypothesis-driven + root cause |
| Optimization agents | SCAMPER + DMAIC | Creative enhancement + process |
| Agent lifecycle | CAGEERF + SCAMPER | Design + enhancement |

---

## Description-Capability Alignment Checklist

Validate agent descriptions against these 5 delegation criteria:

| # | Criterion | Check |
|---|-----------|-------|
| 1 | **Clear trigger condition** | "Use proactively when...", "MUST BE USED for..." |
| 2 | **Proactive delegation signal** | Encourages auto-delegation |
| 3 | **Domain keywords** | Enables semantic matching |
| 4 | **Action-oriented language** | Present tense verbs |
| 5 | **Role/expertise declaration** | Clear capability statement |

**Scoring**:
- 5/5 criteria = Score 5
- 4/5 criteria = Score 4
- 3/5 criteria = Score 3
- 2/5 criteria = Score 2
- 1/5 criteria = Score 1
- Unusable = Score 0

---

## Evaluation Workflow

### Step 1: Load Agent Definition

```
Input: Agent file path
Output: Parsed frontmatter, content sections
```

### Step 2: Apply Quality Matrix

For each of the 9 criteria:
1. Review relevant agent sections
2. Assign score (0-5) based on rubric
3. Document evidence for score

### Step 3: Calculate Weighted Score

```
Final_Score = (Correctness x 0.25) + (Format x 0.15) + 
              (Description x 0.10) + (Scope x 0.10) + 
              (Tools x 0.10) + (Reliability x 0.10) + 
              (Safety x 0.10) + (Maintainability x 0.10) + 
              (Efficiency x 0.05)
```

### Step 4: Generate Report

Output includes:
- Overall grade (A-F)
- Per-criterion scores with evidence
- Improvement recommendations
- Priority fixes (lowest-scoring criteria)

---

## Quality Gates

### Minimum Thresholds

| Context | Minimum Grade | Action if Below |
|---------|---------------|-----------------|
| Production deployment | B (3.5) | Block deployment |
| PR merge | C (2.5) | Require fixes |
| Draft/experimental | D (1.5) | Document gaps |

### Critical Failures (Auto-Fail)

- Safety/Compliance score < 3: Immediate remediation required
- Correctness score < 2: Cannot be used in production
- Scope Discipline < 2: Risk of role drift

---

## Maturity Stages

Agent maturity correlates with quality scores:

| Maturity | Version | Expected Grade | Production Use |
|----------|---------|----------------|----------------|
| MVP | v0.x | C-D | Development only |
| Alpha | v1.x | B-C | Testing ready |
| Beta | v2.x | A-B | Production candidate |
| GA | v3.x+ | A | Production ready |

---

## AI-Readability Assessment

Part of Maintainability criterion. Agent prompts should follow:

- Structured headers (scannable)
- Explicit instructions (no ambiguity)
- Front-loaded key information
- Consistent formatting patterns
- Clear section boundaries

Reference: `creating-ai-readable-documentation-framework.md`

---

## Common Quality Issues

| Issue | Criterion Affected | Fix |
|-------|-------------------|-----|
| Vague description | Description-Capability | Add trigger keywords, use cases |
| Missing boundaries | Scope Discipline | Define explicit NOT-for cases |
| Tool sprawl | Tool Use Quality | Remove unused tools, justify each |
| Prompt > 500 lines | Maintainability | Externalize to docs/ |
| No error handling | Reliability | Add Error Recovery section |
| Hardcoded paths | Maintainability | Use relative references |

---

## Integration with Agent Architect

This skill provides evaluation capability for:
- `evaluate_agent` operation
- Quality gate checks during `create_agent`
- Improvement recommendations in `update_agent`

The claude-code-ecosystem agent uses this quality matrix as its primary evaluation framework.
