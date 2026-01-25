---
argument-hint: '<feature-directory> [--resume] [--strict] [--skip-tests]'
description: 'Final integration review before PR. Reviews data flow boundaries between components. Outputs report + pass/fail gate. Sequential with checkpoints.'
allowed-tools: [Task, Bash, Read, Write, Glob, Grep, TodoRead, TodoWrite]
model: opus
---

# Integration Review Command

*Integration-focused pre-PR validation with sequential checkpoint support*

---

## Core Behavior

YOU ARE AN INTEGRATION REVIEW ORCHESTRATOR.

### How to Start
Parse $ARGUMENTS -> Detect pairs -> Loop reviews (with checkpoint) -> Synthesize -> Gate decision

### The Flow
```
/integration-review <dir> -> Detect Pairs -> Loop Review -> Checkpoint -> Synthesize -> Report + Gate
```

### Anti-Patterns (NEVER DO)
- Review component internals (that's what /code-review is for)
- Skip checkpoint saves (interruption loses progress)
- Report findings without integration evidence
- Proceed to /git after FAIL gate

### Good Patterns (ALWAYS DO)
- Focus on data flow boundaries, not component internals
- Save checkpoint after EACH pair review
- Display progress: `[N/total] Reviewing: A -> B...`
- Generate both markdown report AND JSON gate status

---

## Delegation Model

This command uses agents to perform work. Agents use their skills to complete the work.

**Agents used by this command**:
- `integration-boundary-reviewer` agent - Pair detection (MODE: detect) and pair review (MODE: review)
- `test-executor` agent - Integration test execution (Phase 4)

---

## Modes

| Flag | Mode | Action |
|------|------|--------|
| (none) | Fresh | Detect pairs, review all from scratch |
| `--resume` | Resume | Load checkpoint, continue from last pair |
| `--strict` | Strict | FAIL on any MEDIUM+ finding |
| `--skip-tests` | Fast | Skip integration test execution |

---

## Workflow Overview

```text
PHASE 0: ARGUMENT PARSING
  |-- Parse feature directory from $ARGUMENTS
  |-- Check flags: --resume, --strict, --skip-tests
  |-- Validate directory exists with PLAN.md or ARCHITECTURE.md
  |-- Output: {feature_dir, flags}

PHASE 1: CHECKPOINT CHECK
  |-- IF --resume flag:
  |     Load {feature_dir}/.integration-review-checkpoint.json
  |     Validate schema_version == "1.0"
  |     Verify checksum matches content hash
  |     IF checksum invalid:
  |       Error: "Checkpoint corrupted. Use --no-resume to restart fresh."
  |       ABORT workflow
  |     Skip to current_pair
  |-- ELSE:
  |     Continue to Phase 2

PHASE 2: PAIR DETECTION -> integration-boundary-reviewer agent (MODE: detect)
  |-- Timeout: 600000ms (10 min)
  |-- Task(integration-boundary-reviewer, "MODE: detect\nFeature: {feature_dir}")
  |-- Receive integration_pairs[]
  |-- **Pair Schema**:
  |     ```json
  |     {
  |       "id": "number",
  |       "upstream": "string (component name)",
  |       "downstream": "string (component name)",
  |       "upstream_file": "string (file path)",
  |       "downstream_file": "string (file path)",
  |       "data_flow_type": "direct | indirect",
  |       "confidence": "number (0.0-1.0)"
  |     }
  |     ```
  |-- Initialize checkpoint with pairs
  |-- Save checkpoint: status = IN_PROGRESS
  |-- Output: pairs[], checkpoint initialized

PHASE 2.5: ZERO PAIRS GATE
  |-- IF pairs.count == 0:
  |     Set gate_status = SKIPPED
  |     Generate INTEGRATION-REVIEW-REPORT.md with:
  |       "No integration pairs detected. Feature may be single-component."
  |     Generate INTEGRATION-REVIEW.json with gate_status: "SKIPPED"
  |     TERMINATE workflow (skip Phases 3-5)
  |-- ELSE:
  |     Continue to Phase 2.6
  |-- Output: gate_status (SKIPPED or continue)

PHASE 2.6: PROGRESS FILE INITIALIZATION
  |-- Create `{feature_dir}/.review-progress.md`
  |-- Initial content:
  |     # Integration Review Progress
  |     
  |     **Feature**: {feature_dir}
  |     **Started**: {timestamp}
  |     **Total Pairs**: {count}
  |     
  |     ---
  |     
  |     ## Pair Reviews
  |-- Output: progress file created

PHASE 3: SEQUENTIAL REVIEW LOOP -> integration-boundary-reviewer agent (MODE: review)
  |-- Timeout per pair: 300000ms (5 min)
  |-- FOR each pair NOT in reviewed_pairs:
  |     1. Display: "[{N}/{total}] Reviewing: {upstream} -> {downstream}..."
  |     2. Task(integration-boundary-reviewer, "MODE: review\nPair: {pair_json}")
  |     3. Receive pair_findings{}
  |     4. Add pair to reviewed_pairs
  |     5. Save findings to checkpoint
  |     6. Display: "OK {status}" or "WARNING {status} ({finding_count} findings)"
  |     7. Append to .review-progress.md:
  |        ### Pair {N}/{total}: {upstream} -> {downstream}
  |        **Reviewed**: {timestamp}
  |        **Status**: {status}
  |        **Findings**: {count} ({severity_breakdown})
  |        
  |     8. Save checkpoint
  |-- Output: all_findings[]

PHASE 4: INTEGRATION TEST EXECUTION (unless --skip-tests) -> test-executor agent
  |-- Timeout: 600000ms (10 min)
  |-- Discover: Glob("tests/integration/test_*.py")
  |-- IF no test files found:
  |     Warn: "No integration tests found at tests/integration/"
  |     Set test_results = {passed: 0, failed: 0, skipped: 0, missing: true}
  |     Continue to Phase 5 (missing tests do NOT fail gate)
  |-- ELSE:
  |     Run: Task(test-executor, "Run pytest tests/integration/ -v --tb=short")
  |     IF pytest execution fails (environment/runtime error, not test failures):
  |       Warn: "Test execution failed (environment issue)"
  |       Set test_results = {error: true, message: "..."}
  |       Continue to Phase 5 (execution errors do NOT fail gate)
  |     ELSE:
  |       Parse results for failures
  |       Output: test_results{passed, failed, skipped}

PHASE 5: SYNTHESIS & GATE DECISION
  |-- Aggregate findings by severity:
  |     Count CRITICAL, HIGH, MEDIUM, LOW
  |-- Append to .review-progress.md:
  |     ---
  |     
  |     ## Synthesis Complete
  |     **Completed**: {timestamp}
  |     **Gate Status**: {gate_status}
  |     **Findings Summary**: {critical}C/{high}H/{medium}M/{low}L
  |-- Apply gate criteria:
  |     - Any CRITICAL -> FAIL
  |     - 4+ HIGH -> FAIL  
  |     - --strict + any MEDIUM+ -> FAIL
  |     - Tests failed -> FAIL
  |     - 1-3 HIGH -> PASS_WITH_CONDITIONS
  |     - Otherwise -> PASS
  |-- Output: gate_status

PHASE 6: REPORT GENERATION
  |-- Validate output schema:
  |     - gate_status in [PASS, PASS_WITH_CONDITIONS, FAIL, SKIPPED]
  |     - blocked_commands is array
  |     - findings_summary contains critical, high, medium, low counts
  |-- IF validation fails:
  |     Set gate_status = "FAIL"
  |     Set blocking_reason = "Output schema validation failed: {details}"
  |-- Generate INTEGRATION-REVIEW-REPORT.md using template
  |-- Generate INTEGRATION-REVIEW.json with:
  |     - gate_status
  |     - blocked_commands: ["git"] if gate_status == "FAIL" else []
  |     - blocking_reason: summary of CRITICAL/HIGH findings if FAIL
  |-- Delete checkpoint (review complete)
  |-- Delete .review-progress.md (validation complete)
  |-- Display summary:
  |     "Gate: {status} - {critical}C/{high}H/{medium}M/{low}L"
  |-- IF gate_status == "FAIL":
  |     Display warning: "WARNING: BLOCKED: /git command should check this gate before proceeding"
```

---

## Agent Delegation

This command directly invokes agents via Task(). Agents do not delegate to other agents.

| Phase | Agent | Operation |
|-------|-------|-----------|
| 2 | integration-boundary-reviewer | MODE: detect - identify integration pairs |
| 3 | integration-boundary-reviewer | MODE: review - review single pair (per iteration) |
| 4 | test-executor | Integration test execution |

### Task Invocation Examples

**Detect Mode**:
```
Task(integration-boundary-reviewer, prompt="MODE: detect\nFeature: docs/00-project/alpha/phase-01", timeout_ms=600000)
```

**Review Mode**:
```
Task(integration-boundary-reviewer, prompt="MODE: review\nPair: {\"id\": 1, \"upstream\": \"Provider\", \"downstream\": \"Normalizer\", \"upstream_file\": \"...\", \"downstream_file\": \"...\"}", timeout_ms=300000)
```

---

## Checkpoint Management

### Checkpoint File
Location: `{feature_dir}/.integration-review-checkpoint.json`

```json
{
  "schema_version": "1.0",
  "checksum": "sha256:...",
  "feature": "alpha-phase-01",
  "started_at": "2025-12-17T10:00:00Z",
  "total_pairs": 8,
  "reviewed_pairs": [1, 2, 3],
  "current_pair": 4,
  "findings": {
    "1": {"status": "PASS", "findings": []},
    "2": {"status": "PASS", "findings": []},
    "3": {"status": "PASS_WITH_CONDITIONS", "findings": [...]}
  },
  "status": "IN_PROGRESS"
}
```

### Resume Behavior
1. Load checkpoint file
2. Skip pairs in `reviewed_pairs`
3. Start from `current_pair`
4. Merge new findings with existing

### Checkpoint Cleanup
On successful completion (all pairs reviewed):
- Generate final report
- Delete checkpoint file
- Checkpoint presence indicates incomplete review

---

## Gate Criteria

**Source of Truth**: `.claude/skills/integration-boundary-reviewer/reference/gate-criteria.md`

**Quick Reference**:
| Condition | Result |
|-----------|--------|
| Zero pairs detected | **SKIPPED** |
| Zero CRITICAL + Zero HIGH | **PASS** |
| Zero CRITICAL + 1-3 HIGH | **PASS_WITH_CONDITIONS** |
| Any CRITICAL or 4+ HIGH | **FAIL** |
| Integration tests fail | **FAIL** |
| `--strict` + any MEDIUM+ | **FAIL** |

See [gate-criteria.md](.claude/skills/integration-boundary-reviewer/reference/gate-criteria.md) for complete decision matrix.

---

## Gate Status Enum (Single Source of Truth)

All gate status references in this command use these values:

| Status | Meaning | Blocks /git |
|--------|---------|-------------|
| `PASS` | All checks passed | No |
| `PASS_WITH_CONDITIONS` | Minor issues, review recommended | No |
| `FAIL` | Critical/high issues found | Yes |
| `SKIPPED` | No integration pairs detected | No |

Referenced in: Phase 2.5, Phase 5, Phase 6, Gate Criteria table.

---

## Error Recovery

| Error | Recovery |
|-------|----------|
| Feature directory not found | Display error, suggest correct path |
| No PLAN.md or ARCHITECTURE.md | Suggest running `/plan` first |
| Zero pairs detected | SKIPPED gate (Phase 2.5) - generate report with empty findings |
| Agent timeout on pair | Retry 1x after 60s timeout, then mark INCOMPLETE, continue |
| Checkpoint corrupted | Offer to restart (`--no-resume`) |
| tests/integration/ not found | Warn, continue without test gate (tests marked MISSING) |
| pytest execution error | Warn, continue without test gate (tests marked ERROR) |

---

## Output Format

### Progress Display
```
Integration Review: docs/00-project/alpha/phase-01
======================================================

Detecting integration pairs...
Found 8 integration pairs.

[1/8] Reviewing: PerplexityProvider -> Normalizer... OK PASS
[2/8] Reviewing: Normalizer -> Deduplicator... OK PASS
[3/8] Reviewing: Deduplicator -> ThemeMatcher... WARNING PASS_WITH_CONDITIONS (1 MEDIUM)
[4/8] Reviewing: ThemeMatcher -> EntityLinker... OK PASS
[5/8] Reviewing: EntityLinker -> MentionAggregator... OK PASS
[6/8] Reviewing: MentionAggregator -> TickerProjector... WARNING PASS_WITH_CONDITIONS (1 HIGH)
[7/8] Reviewing: TickerProjector -> QualityGate... OK PASS
[8/8] Reviewing: QualityGate -> StorageBackend... OK PASS

Running integration tests...
Tests: 12 passed, 0 failed

=======================================================
Gate: PASS_WITH_CONDITIONS
Findings: 0 Critical, 1 High, 1 Medium, 0 Low
=======================================================

Action: Review HIGH finding before merge.
Report: docs/00-project/alpha/phase-01/INTEGRATION-REVIEW-REPORT.md
```

### Generated Files
- `{feature_dir}/INTEGRATION-REVIEW-REPORT.md` - Human-readable report
- `{feature_dir}/INTEGRATION-REVIEW.json` - Machine-readable, includes:
  - `gate_status`: PASS | PASS_WITH_CONDITIONS | FAIL | SKIPPED
  - `blocked_commands`: Array of commands blocked by FAIL (e.g., ["git"])
  - `blocking_reason`: Summary of blocking issues (if FAIL)


### Transient Files (deleted on completion)
- `{feature_dir}/.review-progress.md` - Cumulative progress document (validation proof during review)
- `{feature_dir}/.integration-review-checkpoint.json` - Resume state for interrupted reviews

---

## Structured Logging

Each phase emits structured log entries for observability:

| Phase | Log Entry |
|-------|-----------|
| 0 | `{"event": "phase_start", "phase": "argument_parsing", "feature_dir": "...", "flags": {...}}` |
| 2 | `{"event": "phase_complete", "phase": "pair_detection", "pairs_found": N, "duration_ms": M}` |
| 3 | `{"event": "pair_reviewed", "pair_id": N, "upstream": "...", "downstream": "...", "status": "...", "findings_count": N, "duration_ms": M}` |
| 4 | `{"event": "phase_complete", "phase": "test_execution", "passed": N, "failed": N, "skipped": N, "duration_ms": M}` |
| 5 | `{"event": "gate_decision", "gate_status": "...", "critical": N, "high": N, "medium": N, "low": N}` |
| 6 | `{"event": "workflow_complete", "gate_status": "...", "total_duration_ms": M, "report_path": "..."}` |

**Log Output**: Write to stderr to separate from user-facing progress display.

**Usage**: Enable with environment variable `INTEGRATION_REVIEW_LOGS=1` or flag `--verbose-logs`.

---

## Examples

### Example A: Fresh Review
```
User: /integration-review docs/00-project/alpha/phase-01

Phase 0: Parse args -> feature_dir = docs/00-project/alpha/phase-01
Phase 1: No --resume, skip checkpoint load
Phase 2: Detect 8 pairs from ARCHITECTURE.md
Phase 3: Review pairs 1-8 sequentially, checkpoint after each
Phase 4: Run pytest tests/integration/ -> 12 passed
Phase 5: 0 CRITICAL, 1 HIGH, 1 MEDIUM -> PASS_WITH_CONDITIONS
Phase 6: Generate report, delete checkpoint, display summary
```

### Example B: Resume Interrupted
```
User: /integration-review docs/00-project/alpha/phase-01 --resume

Phase 0: Parse args -> --resume flag set
Phase 1: Load checkpoint -> reviewed_pairs=[1,2,3], current_pair=4
Phase 2: Skip detection (pairs already known)
Phase 3: Review pairs 4-8 only
Phase 4-6: Normal completion
```

### Example C: Strict Mode
```
User: /integration-review docs/00-project/alpha/phase-01 --strict

Phases 0-4: Normal execution
Phase 5: Found 1 MEDIUM finding -> FAIL (strict mode)
Phase 6: Report shows FAIL with strict mode indicator
```

---

## Knowledge Base

- `.claude/skills/integration-boundary-reviewer/SKILL.md` - Skill reference
- `.claude/skills/integration-boundary-reviewer/reference/pair-detection-algorithm.md` - Detection details
- `.claude/skills/integration-boundary-reviewer/reference/integration-checklist.md` - Review criteria
- `.claude/skills/integration-boundary-reviewer/reference/gate-criteria.md` - Pass/fail thresholds
- `.claude/skills/integration-boundary-reviewer/templates/review-report.template.md` - Report template
- `.claude/skills/integration-boundary-reviewer/schemas/review-output.schema.json` - JSON schema
- `.claude/agents/code-review/integration-boundary-reviewer/integration-boundary-reviewer.md` - Agent definition

---

## Orchestrator Integration

**Trigger Keywords**: final review, integration review, pre-PR review, feature review

**Workflow Position**:
```
/spec -> /plan -> /tasks -> /implement -> /integration-review -> /git
```

**Integration Points**:
- **Upstream**: /implement completion
- **Downstream**: /git prepare (integration gate informs commit readiness)
- **Complement**: /code-review (component-level) vs /integration-review (integration-level)

**Anti-Patterns** (do NOT use /integration-review for):
- Component-level code review (use /code-review)
- Security scans (use /code-review --focus=security)
- Initial feature planning (use /spec, /plan)
