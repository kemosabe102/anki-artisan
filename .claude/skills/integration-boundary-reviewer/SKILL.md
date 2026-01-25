---
name: integration-boundary-reviewer
description: >
  Final integration review for features before PR submission. Reviews data flow
  boundaries between components, contract alignment, error propagation, and edge
  case handling. Use when /implement completes and before /git. Trigger keywords:
  integration review, final review, pre-PR review, component integration, data flow.
allowed-tools: Task, Read, Glob, Grep, Bash(pytest:*)
---

# Feature Final Review

**Purpose**: Systematic review of integration points between feature components before PR submission.

**Use Cases**:
- Pre-PR integration validation
- Data flow boundary review
- Contract alignment verification
- Error propagation analysis
- Integration test coverage check

## Quick Start

### Full Feature Review
```
/integration-review docs/00-project/alpha/phase-01
```

### Resume Interrupted Review
```
/integration-review docs/00-project/alpha/phase-01 --resume
```

### Strict Mode (Block on MEDIUM+)
```
/integration-review docs/00-project/alpha/phase-01 --strict
```

---

## Workflow Overview

```
/integration-review (command)
        │
        ├──► integration-boundary-reviewer agent (MODE: detect)
        │         └──► Returns: integration_pairs[]
        │
        └──► LOOP: For each pair (with checkpoint)
                  │
                  └──► integration-boundary-reviewer agent (MODE: review)
                            └──► Returns: pair_findings
                            └──► Save checkpoint after each
                  │
        └──► Synthesize → Report + Gate Decision
```

**Position in Development Workflow**:
```
/spec → /plan → /tasks → /implement → /integration-review → /git
```

---

## Reference Documentation

| Document | Purpose |
|----------|---------|
| [pair-detection-algorithm.md](reference/pair-detection-algorithm.md) | How integration pairs are identified |
| [integration-checklist.md](reference/integration-checklist.md) | Per-pair review criteria |
| [gate-criteria.md](reference/gate-criteria.md) | Pass/fail thresholds |

---

## Input/Output Contract

### Input
- **Required**: Feature directory path containing PLAN.md or ARCHITECTURE.md
- **Optional Flags**:
  - `--resume`: Continue from checkpoint
  - `--strict`: Block on MEDIUM+ severity
  - `--skip-tests`: Skip integration test execution

### Output
- `INTEGRATION-REVIEW-REPORT.md` - Human-readable report
- `INTEGRATION-REVIEW.json` - Machine-readable gate status

---

## Agent Delegation

The skill orchestrates the `integration-boundary-reviewer` agent in two modes:

### MODE: detect
Identifies integration pairs from the feature.

```
Task(integration-boundary-reviewer, prompt="MODE: detect\nFeature: {feature_dir}")
```

Returns: List of integration pairs with confidence scores.

### MODE: review
Reviews a single integration pair using 4 parallel delegates:

```
Task(integration-boundary-reviewer, prompt="MODE: review\nPair: {pair_json}")
```

The agent spawns 4 parallel reviewers:
1. `python-code-reviewer` - Interface contract review
2. `architecture-reviewer` - Layer alignment validation
3. `test-executor` - Integration test coverage check
4. `reliability-reviewer` - Four Hats reliability analysis (NEW)

Returns: Findings for that pair with severity classification.

---

## Checkpoint Management

### Checkpoint File
Location: `{feature_dir}/.integration-review-checkpoint.json`

```json
{
  "feature": "alpha-phase-01",
  "started_at": "2025-12-17T10:00:00Z",
  "total_pairs": 8,
  "reviewed_pairs": [1, 2, 3],
  "current_pair": 4,
  "findings": {},
  "status": "IN_PROGRESS"
}
```

### Resume Behavior
- `--resume` flag loads existing checkpoint
- Skips already-reviewed pairs
- Continues from `current_pair`
- On completion, checkpoint is deleted

---

## Progress Tracking

During review execution, a cumulative progress file is maintained:

**Location**: `{feature_dir}/.review-progress.md`

**Purpose**: 
- Provides real-time validation proof that each pair was reviewed
- Documents findings as they are discovered
- Deleted on successful completion (final proof is in INTEGRATION-REVIEW-REPORT.md)

**Contents**:
- Header with feature info and timestamp
- Per-pair review results (status, findings count, severity breakdown)
- Synthesis summary with gate decision

---

## Gate Criteria

| Condition | Result |
|-----------|--------|
| Zero CRITICAL + Zero HIGH | **PASS** |
| Zero CRITICAL + ≤3 HIGH with action plan | **PASS_WITH_CONDITIONS** |
| Any CRITICAL or 4+ HIGH | **FAIL** |
| Integration tests fail | **FAIL** |
| `--strict` mode + any MEDIUM+ | **FAIL** |

---

## Severity Classification

| Severity | Criteria | Examples |
|----------|----------|----------|
| **CRITICAL** | Contract mismatch causing runtime error | Type mismatch, missing required field |
| **HIGH** | Potential data loss or silent failure | Null not handled, exception swallowed |
| **MEDIUM** | Suboptimal integration pattern | Missing error context, partial handling |
| **LOW** | Style or performance suggestion | Verbose error messages, unnecessary copies |

---

## Example: Alpha Phase 01

### Detect Output
```
Pair 1: PerplexityProvider → Normalizer
Pair 2: Normalizer → Deduplicator
Pair 3: Deduplicator → ThemeMatcher
Pair 4: ThemeMatcher → EntityLinker
Pair 5: EntityLinker → MentionAggregator
Pair 6: MentionAggregator → TickerProjector
Pair 7: TickerProjector → QualityGate
Pair 8: QualityGate → StorageBackend
```

### Review Loop Progress
```
[1/8] Reviewing: PerplexityProvider → Normalizer... ✓ PASS
[2/8] Reviewing: Normalizer → Deduplicator... ✓ PASS
[3/8] Reviewing: Deduplicator → ThemeMatcher... ⚠ PASS_WITH_CONDITIONS (1 MEDIUM)
[4/8] Reviewing: ThemeMatcher → EntityLinker... ✓ PASS
[5/8] Reviewing: EntityLinker → MentionAggregator... ✓ PASS
[6/8] Reviewing: MentionAggregator → TickerProjector... ⚠ PASS_WITH_CONDITIONS (1 HIGH)
[7/8] Reviewing: TickerProjector → QualityGate... ✓ PASS
[8/8] Reviewing: QualityGate → StorageBackend... ✓ PASS

─────────────────────────────────────
Gate: PASS_WITH_CONDITIONS
- 0 CRITICAL, 1 HIGH, 1 MEDIUM, 0 LOW
- Action required: Fix HIGH finding before merge
─────────────────────────────────────
```

---

## Error Recovery

| Error | Recovery |
|-------|----------|
| Feature directory not found | Return error with path guidance |
| No PLAN.md or ARCHITECTURE.md | Suggest running `/plan` first |
| Zero pairs detected | Warn feature may be single-component |
| Agent timeout | Retry 1x, then mark pair as INCOMPLETE |
| Checkpoint corrupted | Offer to restart from beginning |

---

## Best Practices

### When to Run
- After `/implement` completes successfully
- Before creating PR with `/git`
- After significant refactoring of integration points

### Interpreting Results
- **PASS**: Safe to proceed to `/git`
- **PASS_WITH_CONDITIONS**: Review HIGH findings, fix or document
- **FAIL**: Must fix CRITICAL/HIGH findings before PR

### Handling Findings
1. CRITICAL: Fix immediately - these cause runtime failures
2. HIGH: Fix or document with justification
3. MEDIUM: Fix if time permits, or add to tech debt
4. LOW: Optional - consider for future cleanup

---

## Related Skills & Agents

| Resource | Purpose |
|----------|---------|
| `python-code-reviewer` agent | Component-level code review |
| `architecture-reviewer` agent | Layer and design validation |
| `test-executor` agent | Test execution and coverage |
| `reliability-reviewer` agent | Four Hats reliability analysis |
| `edge-reliability` skill | Graph Theorist edge checks |
| `node-reliability` skill | Lawyer node checks |
| `operational-reliability` skill | Operator + Historian checks |
| `component-reviewer` skill | Automated component reviews |
| `feature-design-workflow` skill | Feature planning workflow |

---

## Version History

- **v1.0.0** (2025-12-17): Initial release
  - Two-mode agent (detect + review)
  - Data flow adjacency pair detection
  - Sequential checkpoint support
  - Integration with /integration-review command
