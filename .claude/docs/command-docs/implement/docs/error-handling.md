# Error Handling for /implement Command

Complete error scenarios with recovery strategies and decision trees.

---

## Failure Categories

| Failure Type | Retry Strategy | Escalation | Examples |
|--------------|----------------|------------|----------|
| **Infrastructure Transient** | Exponential backoff (max 3) | After 3 failures | Network timeout, rate limit, file lock |
| **Infrastructure Permanent** | Immediate escalation | Immediate | Missing file, access denied, disk full |
| **Schema/Validation** | Immediate escalation | Immediate | TASKS.json malformed, invalid dependencies |
| **Agent Unavailable** | Retry 1x | After 1 retry | Agent not found, timeout |
| **Task Logic Failure** | Tasks: 1 retry, Reviews: 3 retries | After limit | Test failures, bugs, lint errors |

---

## Phase 1: Discovery Failures

### No tasks/ Directory

**Error**: `feature_dir/tasks/` does not exist

**Actions**:
1. Report error with expected path
2. Suggest: `/tasks {feature_dir}`
3. STOP workflow

**Recovery**: Run `/tasks` to generate TASKS.json, then retry `/implement`

### No TASKS.json Files

**Error**: No `*/TASKS.json` found in tasks/ directory

**Actions**:
1. Report empty directory
2. Suggest: `/tasks {feature_dir}`
3. STOP workflow

### Malformed JSON

**Error**: JSON parsing fails

**Actions**:
1. Report specific JSON error with line number
2. STOP workflow

**Recovery**: Manually fix JSON syntax or regenerate with `/tasks`

### Circular Dependencies

**Error**: Dependency graph has cycles

**Actions**:
1. Report cycle: `T005 → T008 → T012 → T005`
2. ESCALATE to user

**Recovery**: Edit TASKS.json to break cycle

---

## Phase 2: Validation Failures

### Schema Mismatch

**Error**: TASKS.json doesn't match implement.schema.json

**Actions**:
1. Report missing/invalid fields
2. STOP workflow

**Recovery**: Regenerate with `/tasks` (ensures schema compliance)

### Invalid Task IDs

**Error**: Dependencies reference non-existent task IDs

**Actions**:
1. Report: `T015 depends on T099 (not found)`
2. STOP workflow

### Broken Review Groups

**Error**: Review group references invalid task or missing files_in_scope

**Actions**:
1. Report specific issue
2. STOP workflow

---

## Phase 3: Execution Failures

### Regular Task Failure

**Retry Policy**: 1 retry (fail-fast)

**Flow**:
```
Task fails
  → Attempt 1: ❌ FAIL
  → Retry once
  → Attempt 2: ❌ FAIL
  → Mark task BLOCKED
  → Block dependent tasks
  → Continue with independent tasks
  → Report to user
```

**Time Budget**: 45 seconds to escalation

**Actions**:
1. Mark task as `blocked` with reason
2. Mark dependent tasks as `blocked` (cascade)
3. Continue executing independent tasks
4. Report blocked tasks in progress update

**User Options**:
```
❌ T009 ESCALATED after 1 retry (45s)
Actions: Blocked T010-T012 | Continuing with T013+

Options:
1. Fix manually: Check T008 output
2. Re-run: /implement {path}
3. Skip: --skip-tasks=T009,T010,T011,T012
```

### Review Checkpoint Failure

**Retry Policy**: 3 retries (quality-focused)

**Flow**:
```
Multi-agent review
  → Critical issues found
  → Iteration 1: Fix agent → Re-review → Still critical
  → Iteration 2: Fix agent → Re-review → Still critical
  → Iteration 3: Fix agent → Re-review → Still critical
  → Mark checkpoint BLOCKED
  → Block dependent tasks
  → Report to user
```

**Time Budget**: 2-6 minutes for retry loop

**Actions**:
1. Each iteration: Fix → Re-review (same multi-agent)
2. After 3 iterations: Mark dependents BLOCKED
3. Report with full context of what was tried

### File Conflict During Parallel Execution

**Error**: Multiple tasks targeting same file detected

**Actions**:
1. Move conflicting tasks to sequential batch
2. Continue with safe parallel tasks
3. Log conflict detection in progress

**Prevention**: File conflict detection runs BEFORE parallel execution

### Agent Unavailable

**Error**: Agent times out or not found

**Actions**:
1. Retry once
2. If still unavailable: Mark task blocked
3. Continue with independent tasks

---

## Error Recovery Decision Tree

```
Task/Checkpoint Fails
│
├─ Infrastructure Transient?
│   └─ YES → Exponential backoff (2s → 4s → 8s)
│       └─ Still fails after 3? → ESCALATE
│
├─ Infrastructure Permanent?
│   └─ YES → Immediate ESCALATE
│
├─ Schema/Validation?
│   └─ YES → Report errors → STOP
│
├─ Agent Unavailable?
│   └─ YES → Retry 1x → ESCALATE if still unavailable
│
└─ Task Logic Failure?
    ├─ Regular task?
    │   └─ Retry 1x (fail-fast) → ESCALATE
    │
    └─ Review checkpoint?
        └─ Fix agent → Re-review (max 3x) → ESCALATE
```

---

## Retry Policy Rationale

### Regular Tasks: 1 Retry (Fail-Fast)

**Why**: Fast feedback, avoid cascading delays

**Example**:
```
T009: File not found
  → Retry → Still not found
  → Mark blocked (45s total)
  → Continue with T013+
```

### Review Checkpoints: 3 Retries (Quality-Focused)

**Why**: Quality gates worth deeper investment; fix agents resolve most issues

**Example**:
```
RG003: Linting errors
  → Fix agent applies fixes
  → Re-review → New pattern violation
  → Fix agent applies fixes
  → Re-review → PASS (2 min total)
```

### Infrastructure: Exponential Backoff

**Why**: Transient issues (network, rate limits) resolve with time

**Example**:
```
API timeout
  → Wait 2s → Retry → Timeout
  → Wait 4s → Retry → Success
```

---

## Escalation Reports

### Task Escalation Format

```markdown
❌ TASK ESCALATED: T009

**Task**: Update Jaeger deployment
**Agent**: development
**Attempts**: 2 (1 retry)
**Duration**: 45s
**Error**: PVC 'jaeger-storage' not found

**Blocked Dependents**: T010, T011, T012

**Recovery Options**:
1. Create missing PVC manually
2. Skip tasks: --skip-tasks=T009,T010,T011,T012
3. Re-run after fix: /implement {path}
```

### Review Escalation Format

```markdown
❌ REVIEW ESCALATED: RG003

**Component**: API Authentication
**Files**: src/api/auth.py, tests/api/test_auth.py
**Iterations**: 3 (max reached)

**Unresolved Critical Issues**:
1. [SECURITY] SQL injection in query_user()
2. [TEST] test_login_flow fails: AssertionError

**Attempted Fixes**:
- Iteration 1: Applied parameterized queries
- Iteration 2: Fixed assertion in test
- Iteration 3: Addressed remaining injection vector

**Blocked Dependents**: T024, T025, T026

**Next Steps**:
1. Manual review of auth.py security
2. Skip: --skip-tasks=T024,T025,T026
```

---

## Command-Line Recovery Options

| Option | When to Use | Example |
|--------|-------------|---------|
| `--skip-tasks=T001,T002` | Known blocking tasks | `/implement path --skip-tasks=T009,T010` |
| `--skip-phase=N` | Skip entire phase | `/implement path --skip-phase=1` |
| `--skip-validation` | After manual JSON fix | `/implement path --skip-validation` |
| `--resume` | Continue from checkpoint | `/implement path --resume` |
