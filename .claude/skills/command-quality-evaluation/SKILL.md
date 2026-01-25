---
name: command-quality-evaluation
description: >
  11-criterion quality matrix for evaluating slash command definitions. Use when assessing
  command quality, conducting workflow audits, or validating command improvements.
  Trigger keywords: command quality, evaluate command, workflow audit, command validation.
---

# Command Quality Evaluation Skill

Systematic command evaluation using a weighted 11-criterion quality matrix for slash command workflows.

## Reference Documentation

- **Quality Matrix Rubric** -> [references/quality-matrix-rubric.md](references/quality-matrix-rubric.md)
- **Workflow Patterns Checklist** -> [references/workflow-patterns-checklist.md](references/workflow-patterns-checklist.md)
- **SCAMPER Workflow Optimization** -> [references/scamper-workflow-optimization.md](references/scamper-workflow-optimization.md)

---

## Quick Reference: Quality Matrix

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Workflow Correctness** | 0.15 | Steps in correct order, dependencies valid |
| **Frontmatter Compliance** | 0.12 | Valid YAML, required fields present |
| **Subagent Validity** | 0.12 | All Task() targets exist, have required tools |
| **Gate Coverage** | 0.10 | Critical decision points have gates |
| **Error Recovery** | 0.10 | Comprehensive error handling, retry policies |
| **Parallelization Safety** | 0.10 | Parallel operations are truly independent |
| **Skill References** | 0.08 | Referenced skills exist and accessible |
| **Tool Permissions** | 0.08 | Tools properly scoped (Bash with patterns) |
| **Documentation** | 0.08 | Anti-patterns, good patterns, examples |
| **Orchestrator Integration** | 0.05 | Trigger keywords, integration points |
| **State Management** | 0.02 | Checkpoint/resume support if multi-phase |

---

## Grade Calculation

**Formula**: Weighted sum of all criterion scores (each 0-5)

```
Quality_Score = SUM(Criterion_Score x Weight) for all 11 criteria
```

| Grade | Score Range | Description |
|-------|-------------|-------------|
| **A** | 4.5-5.0 | Production ready, excellent workflow orchestration |
| **B** | 3.5-4.4 | Good workflow, minor improvements needed |
| **C** | 2.5-3.4 | Acceptable, notable workflow issues |
| **D** | 1.5-2.4 | Poor workflow, significant improvements required |
| **F** | 0.0-1.4 | Failing, major redesign needed |

---

## Quality Gates

### Minimum Thresholds

| Context | Minimum Grade | Action if Below |
|---------|---------------|-----------------|
| Production deployment | B (3.5) | Block deployment |
| PR merge | C (2.5) | Require fixes |
| Draft/experimental | D (1.5) | Document gaps |

### Critical Failures (Auto-Fail)

- Workflow Correctness < 3: Steps out of order or missing dependencies
- Subagent Validity < 2: References non-existent agents
- Error Recovery < 2: No error handling defined

---

## Evaluation Workflow

### Step 1: Load Command Definition

```
Input: Command file path (.claude/commands/*.md)
Output: Parsed frontmatter, workflow sections, Task() patterns
```

### Step 2: Validate Frontmatter

Check required fields:
- `argument-hint`: Present and descriptive
- `description`: Present, <200 chars, includes trigger keywords
- `allowed-tools`: Present, minimal set
- `model`: Present (opus, sonnet, haiku)

### Step 3: Apply Quality Matrix

For each of the 11 criteria:
1. Review relevant command sections
2. Assign score (0-5) based on rubric
3. Document evidence for score

### Step 4: Calculate Weighted Score

```
Final_Score = (Workflow x 0.15) + (Frontmatter x 0.12) + 
              (Subagent x 0.12) + (Gates x 0.10) + 
              (Error x 0.10) + (Parallel x 0.10) + 
              (Skills x 0.08) + (Tools x 0.08) + 
              (Docs x 0.08) + (Integration x 0.05) + 
              (State x 0.02)
```

### Step 5: Generate Report

Output includes:
- Overall grade (A-F)
- Per-criterion scores with evidence
- Improvement recommendations
- Priority fixes (lowest-scoring criteria)

---

## Frontmatter Field Reference

| Field | Required | Valid Values |
|-------|----------|--------------|
| `argument-hint` | YES | String with placeholders (e.g., `<file-path>`) |
| `description` | YES | String <200 chars with trigger keywords |
| `allowed-tools` | YES | Comma-separated tool list |
| `model` | YES | `opus`, `sonnet`, `haiku` |

---

## Common Quality Issues

| Issue | Criterion Affected | Fix |
|-------|-------------------|-----|
| Steps out of order | Workflow Correctness | Add dependency annotations |
| Missing `model` field | Frontmatter Compliance | Add model selection |
| Task() to non-existent agent | Subagent Validity | Verify agent exists in .claude/agents/ |
| No error codes defined | Error Recovery | Add error handling section |
| Parallel Task() with dependencies | Parallelization Safety | Make sequential or remove dependency |
| Skill() without path | Skill References | Add valid skill path |
| Bash without patterns | Tool Permissions | Add allowed-command patterns |
| No examples section | Documentation | Add usage examples |
| No trigger keywords | Orchestrator Integration | Add keywords to description |
| Multi-phase without checkpoints | State Management | Add checkpoint/resume support |

---

## Workflow Validation Quick Checks

### Dependency Chain Validation

For each phase/step in the workflow:
1. Identify inputs required
2. Verify previous phase provides those inputs
3. Flag any gaps in the chain

### Parallel Safety Check

Tasks can run in parallel ONLY if:
- No shared state modification
- No file write conflicts
- No dependency on other parallel task output

### Gate Coverage Check

Every phase should have:
- Exit condition defined
- Timeout specified
- Failure handling

---

## Integration with Orchestrator

This skill provides evaluation capability for:
- Command quality audits
- Pre-merge validation gates
- Workflow improvement recommendations

Commands evaluated against this matrix:
- `.claude/commands/*.md` - All slash commands
- Workflow definitions in agent skills
