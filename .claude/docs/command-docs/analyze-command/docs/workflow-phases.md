# Workflow Phases

Detailed documentation for each phase of the `/analyze-command` command.

**Version**: 1.0.0 | **Last Updated**: 2025-12-21

---

## Phase Overview

The `/analyze-command` workflow consists of 9 phases (P0-P8):

| Phase | Name | Execution | Duration | Framework |
|-------|------|-----------|----------|-----------|
| P0 | Input Validation | Sequential | 5-10s | Guard Clauses |
| P1 | Parallel Analysis | Parallel (4 agents) | 8-12min | Multi-Agent |
| P2 | Orchestrator Validation | Sequential | 1-2min | Checklist |
| P3 | Synthesis | Sequential | 2-3min | Weighted Merge |
| P4 | Pre-Mortem | Sequential | 1-2min | Gary Klein |
| P5 | Scoring | Sequential | 30s | Weighted Average |
| P6 | Report Generation | Sequential | 2-3min | Template |
| P7 | Delegation Routing | Conditional | Variable | Decision Matrix |
| P8 | SCAMPER Optimization | Optional | 3-5min | SCAMPER |

**Execution Rules**:
- P0-P6: MANDATORY sequential execution
- P7: Conditional based on findings
- P8: Optional (triggered by `--optimize` flag or score < 70)

---

## Phase 0: Input Validation

**Duration**: 5-10 seconds
**Pattern**: Guard Clause Validation

### Gate Criteria

| Check | Pass Condition | Fail Action |
|-------|----------------|-------------|
| Path exists | Command file found at path | ERROR: `COMMAND_NOT_FOUND` |
| File extension | `.md` extension | ERROR: `INVALID_EXTENSION` |
| Frontmatter present | YAML frontmatter detected | ERROR: `MISSING_FRONTMATTER` |
| Scope valid | Path within `.claude/commands/` | ERROR: `OUT_OF_SCOPE` |

### Timeout

- **Hard limit**: 30 seconds
- **Retry**: None (input validation is deterministic)

### Output

```json
{
  "phase": "P0_INPUT_VALIDATION",
  "status": "PASS|FAIL",
  "resolved_path": "absolute/path/to/command.md",
  "command_name": "git",
  "errors": []
}
```

---

## Phase 1: 4-Agent Parallel Analysis

**Duration**: 8-12 minutes (parallel execution)
**Pattern**: Multi-Agent Analysis Protocol

### Agent Assignments

Launch all 4 agents in a **single message** with 4 Task calls:

#### Agent 1: claude-code-ecosystem (Structure)
**Focus**: Command structure, workflow phases, delegation patterns

**Evaluation Criteria**:
1. Frontmatter validation (name, description, argument-hint)
2. Workflow phase definition (phases listed, gates defined)
3. Delegation pattern completeness (Task() calls documented)
4. Error handling coverage (error codes, recovery strategies)
5. Output state definition (SUCCESS/FAILURE states)
6. Integration points (upstream/downstream commands)
7. Quality matrix (9 criteria, 0-5 scale)

#### Agent 2: claude-code-ecosystem (Prompt Quality)
**Focus**: Prompt quality across frameworks

**Evaluation Criteria**:
1. Structural Quality (16 criteria)
2. Prompt Engineering (6 principles)
3. Token Optimization (15+ techniques)
4. Testing Strategy (risk-appropriate)
5. Progressive Disclosure (4 factors, A-F grade)
6. Token Density (6 metrics, A-F grade)
7. Framework Alignment (OODA, thinking frameworks)

#### Agent 3: documentation
**Focus**: Token efficiency and documentation optimization

**Evaluation Criteria**:
1. Token count by section
2. Redundancy detection (inline vs external)
3. Compression opportunities
4. Reference vs inline decisions
5. Anti-pattern detection (6 types)

#### Agent 4: tech-debt-investigator
**Focus**: Documentation debt using SQALE/SIG methodology

**Evaluation Criteria**:
1. Documentation debt score (0-100)
2. Technical Debt Ratio (TDR)
3. SQALE grade (A-E) and SIG rating (1-5)
4. 6-category breakdown
5. Dependency risk assessment
6. Knowledge debt detection

### Timeout

- **Per agent**: 180 seconds
- **Total phase**: 300 seconds (agents run in parallel)
- **Retry**: 1 attempt per agent, then skip with note

---

## Phase 2: Orchestrator Validation

**Duration**: 1-2 minutes
**Pattern**: Checklist Validation

### Validation Checks

| Check | Description | Weight |
|-------|-------------|--------|
| Workflow completeness | All phases have gates and outputs | 20% |
| Delegation coverage | All complexity delegated to agents | 20% |
| Error handling | All error codes have recovery | 15% |
| OODA alignment | Phases map to OODA loop | 15% |
| Integration points | Upstream/downstream documented | 15% |
| Schema compliance | Output matches schema | 15% |

### Gate Criteria

- **PASS**: All checks pass (100%)
- **PARTIAL**: 5-6 checks pass (70-99%)
- **FAIL**: <5 checks pass (<70%)

### Timeout

- **Hard limit**: 120 seconds
- **No retry** (deterministic validation)

---

## Phase 3: Synthesis

**Duration**: 2-3 minutes
**Pattern**: Weighted Merge with Conflict Resolution

### Process

1. **Overlap Detection**:
   ```
   Similarity = (keyword_overlap x 0.4) + (domain x 0.3) + (location x 0.2) + (agent_type x 0.1)
   ```
   - Findings with similarity > 0.7 are consolidated

2. **Weighted Scoring**:
   ```
   Priority = (Impact x 0.4) + (Effort^-1 x 0.3) + (Risk x 0.3)
   ```
   - P1: > 0.7
   - P2: 0.5 - 0.7
   - P3: 0.3 - 0.5
   - P4: < 0.3

3. **Conflict Resolution**:
   - If agents disagree, present trade-offs
   - Orchestrator makes final recommendation based on domain fit

4. **Consolidation**:
   - Merge overlapping recommendations
   - Remove duplicates
   - Sequence by dependencies (P1 -> P2 -> P3)

### Gate Criteria

- Phase completes when all findings merged
- No minimum threshold (empty findings = healthy command)

### Timeout

- **Hard limit**: 180 seconds
- **Fallback**: Return unmerged findings with `synthesis_failed: true`

---

## Phase 4: Pre-Mortem

**Duration**: 1-2 minutes
**Pattern**: Gary Klein Pre-Mortem Technique

### Purpose

Predict how the command might fail in production by assuming failure has already occurred.

### Agent

**Primary**: `contingency-planner`

See `pre-mortem-phase.md` for complete details including:
- 5 failure categories for commands
- Task() syntax
- Resilience score calculation

### Gate Criteria

- Output contains at least 3 failure modes
- Resilience score calculated
- All failure modes have detection methods

### Timeout

- **Hard limit**: 120 seconds
- **Fallback**: Skip phase, note in report

---

## Phase 5: Scoring

**Duration**: 30 seconds
**Pattern**: Weighted Average Calculation

### Score Formula

```
overall_score = (
  workflow_score x 0.25 +
  delegation_score x 0.20 +
  error_handling_score x 0.15 +
  documentation_score x 0.15 +
  integration_score x 0.10 +
  token_efficiency_score x 0.10 +
  resilience_score x 0.05
)
```

### 7 Dimensions

| Dimension | Weight | Source |
|-----------|--------|--------|
| Workflow Quality | 25% | P1 (claude-code-ecosystem) |
| Delegation Patterns | 20% | P1 (claude-code-ecosystem) |
| Error Handling | 15% | P1 (claude-code-ecosystem) |
| Documentation Quality | 15% | P1 (documentation) |
| Integration Points | 10% | P2 (orchestrator) |
| Token Efficiency | 10% | P1 (documentation) |
| Resilience | 5% | P4 (contingency-planner) |

### Grade Mapping

| Score Range | Grade | Assessment |
|-------------|-------|------------|
| 90-100 | A | Excellent |
| 80-89 | B | Good |
| 70-79 | C | Acceptable |
| 60-69 | D | Needs Improvement |
| 0-59 | F | Poor |

### Timeout

- **Hard limit**: 30 seconds (calculation only)

---

## Phase 6: Report Generation

**Duration**: 2-3 minutes
**Pattern**: Template-Based Generation

### Report Structure

1. Executive Summary (2-3 sentences)
2. Overall Score and Grade
3. 7-Dimension Breakdown
4. Top 3 Findings (P1 priority)
5. Resilience Assessment
6. Recommendations (P1/P2/P3)
7. Implementation Roadmap
8. Confidence and Limitations

### Output Format

JSON conforming to `command-analysis.schema.json`

### Timeout

- **Hard limit**: 180 seconds
- **Fallback**: Generate minimal report with available data

---

## Phase 7: Delegation Routing

**Duration**: Variable
**Pattern**: Conditional Execution

### Trigger Conditions

| Condition | Action |
|-----------|--------|
| Critical findings (P1) exist | Route to appropriate fix agent |
| Score < 60 | Recommend immediate remediation |
| Integration failures | Route to ecosystem validator |
| Token bloat > 30% | Route to doc-reference-optimizer |

### Routing Matrix

See `delegation-patterns.md` for complete routing matrix.

### Timeout

- **Per delegation**: 300 seconds
- **Retry**: 1 attempt, then escalate to user

---

## Phase 8: SCAMPER Optimization

**Duration**: 3-5 minutes
**Pattern**: SCAMPER Framework

### Trigger Conditions

- Explicit: `--optimize` flag passed
- Implicit: Overall score < 70

### Process

Apply 7 SCAMPER techniques to command workflow:
1. **Substitute**: Replace inefficient patterns
2. **Combine**: Merge redundant phases
3. **Adapt**: Apply patterns from high-scoring commands
4. **Modify**: Adjust workflow structure
5. **Put to other uses**: Repurpose reusable components
6. **Eliminate**: Remove unnecessary complexity
7. **Reverse**: Restructure phase dependencies

See `scamper-optimization.md` for complete details.

### Timeout

- **Hard limit**: 300 seconds
- **Fallback**: Skip optimization, note in report

---

## Duration Summary

| Mode | Total Duration |
|------|----------------|
| Standard analysis | 15-20 minutes |
| With optimization (P8) | 20-25 minutes |
| Quick mode (`--quick`) | 8-12 minutes |

**Phase Breakdown (standard)**:
- P0: 5-10s
- P1: 8-12min (parallel)
- P2: 1-2min
- P3: 2-3min
- P4: 1-2min
- P5: 30s
- P6: 2-3min
- P7: Variable (conditional)

---

## Error Recovery

| Phase | Error | Recovery |
|-------|-------|----------|
| P0 | Invalid path | FAIL immediately, clear error message |
| P1 | Agent timeout | Retry once, then skip agent with note |
| P2 | Validation timeout | Use partial results |
| P3 | Merge conflict | Present both perspectives |
| P4 | Pre-mortem timeout | Skip phase, note in report |
| P5 | Calculation error | Use fallback weights |
| P6 | Template error | Generate minimal report |
| P7 | Delegation failure | Escalate to user |
| P8 | Optimization timeout | Skip, note in report |
