# Usage Examples for /implement Command

Complete workflow scenarios with expected outputs.

---

## Example 1: Full Feature Implementation (Success Path)

### Command
```bash
/implement docs/01-planning/features/006-opentelemetry-monitoring-infrastructure/
```

### Phase 1: Discovery
```
📁 Discovering TASKS.json files...

Found 3 plans:
  001-infrastructure-foundation (29 tasks, 8 SP)
  002-telemetry-integration (22 tasks, 6 SP)
  003-dashboard-alerting (25 tasks, 5 SP)

Execution order: 001 → 002 → 003
```

### Phase 2: Validation
```
✅ Validation PASSED

Plans validated: 3
Total tasks: 76
Dependencies: Valid
Review groups: 14
```

### Phase 3: Execution (Progress Updates)
```
📊 Implementation Progress: 001-infrastructure-foundation
Phase 1: 🔄 T001-T006 in_progress | [development]
Status: 0/29 tasks | ETA: 18 min

---

📊 Implementation Progress: 001-infrastructure-foundation
Phase 1: ✅ T001-T006 complete | 🔍 T007 in_progress [code-quality]
Status: 6/29 tasks | Review checkpoint | ETA: 15 min

---

📊 Implementation Progress: 001-infrastructure-foundation
Phase 1: ✅ RG001 approved (1 iteration) | 🔄 T008-T012 in_progress
Status: 7/29 tasks | ETA: 12 min
```

### Phase 4: Completion Report
```markdown
## Implementation Complete: 006-opentelemetry-monitoring-infrastructure
**Plans**: 3 | **Tasks**: 76/76 (100%) | **Duration**: 46.5 hrs | **Status**: ✅

### Executive Summary
- 76 tasks completed (100% success)
- 14 review checkpoints passed
- 0 blocking issues

### Plan Breakdown
#### 001-infrastructure-foundation (8 SP) ✅
- Tasks: 29/29 (100%)
- Review Groups: 4/4 passed (RG001: 1 iter, RG003: 2 iter)
- Files Changed: 5 files (k8s/local/*.yaml)
- Duration: 17.5 hours

#### 002-telemetry-integration (6 SP) ✅
- Tasks: 22/22 (100%)
- Review Groups: 5/5 passed
- Files Changed: 8 files

#### 003-dashboard-alerting (5 SP) ✅
- Tasks: 25/25 (100%)
- Review Groups: 5/5 passed
- Files Changed: 12 files

### Implementation Metrics
**Review Performance**: 79% first attempt | 14% 1 retry | 7% 2 retries
**Agent Distribution**: implementer 53% | code-quality 12% | reviewer 18%

### Next Steps
1. ✅ Ready for /git commit
2. 🎯 Monitor metrics in Grafana
```

---

## Example 2: Task Failure with Fail-Fast

### Command
```bash
/implement docs/01-planning/features/006-opentelemetry-monitoring-infrastructure/
```

### Execution (Failure Occurs)
```
📊 Implementation Progress: 001-infrastructure-foundation
Phase 1: ✅ T001-T008 complete | 🔄 T009 in_progress [development]
Status: 8/29 tasks | ETA: 10 min

---

🔄 T009: in_progress → Attempt 1: ❌ FAIL
Error: PVC 'jaeger-storage' not found

Retrying once...

🔄 T009: Attempt 2: ❌ FAIL
Error: PVC 'jaeger-storage' not found (retry failed)

---

❌ T009 ESCALATED after 1 retry (45s)
Actions: Blocked T010-T012 (dependencies) | Continuing with T013+

Options:
1. Fix manually: Create PVC 'jaeger-storage'
2. Re-run: /implement docs/01-planning/features/006-opentelemetry/
3. Skip: --skip-tasks=T009,T010,T011,T012
```

### Continuing with Independent Tasks
```
📊 Implementation Progress: 001-infrastructure-foundation
Phase 1: ✅ T013-T015 complete | 🔄 T016 in_progress
Status: 12/29 tasks (4 blocked) | Continuing...
```

---

## Example 3: Review Checkpoint with Retry Loop

### Review Iteration 1
```
🔍 Review Checkpoint: RG003 (API Authentication)
Files: src/api/auth.py, tests/api/test_auth.py

Launching multi-agent review...
- code-quality: analyzing...
- architectureer: analyzing...
- tech-debt-investigator: analyzing...
- sast-scanner: analyzing... (dynamic: security component)

Review complete. Synthesizing findings...

❌ Critical Issues Found (2):
1. [SECURITY] SQL injection vulnerability in query_user() (Line 45)
2. [TEST] test_login_flow assertion error

🔧 Applying fixes (Iteration 1/3)...
- Delegating security fix to development
- Delegating test fix to debugger
```

### Review Iteration 2
```
🔍 Re-reviewing RG003 (Iteration 2/3)...

Launching multi-agent review...

Review complete. Synthesizing findings...

❌ Critical Issues Found (1):
1. [SECURITY] Remaining injection vector in update_user() (Line 78)

🔧 Applying fixes (Iteration 2/3)...
```

### Review Iteration 3 (Success)
```
🔍 Re-reviewing RG003 (Iteration 3/3)...

Launching multi-agent review...

Review complete. Synthesizing findings...

✅ RG003 APPROVED (3 iterations)

Critical issues: 0 (resolved)
High-priority: 2 (documented for follow-up)
Future improvements: 4 (captured in tech debt)

Unblocking dependent tasks: T024, T025, T026
```

---

## Example 4: Dry Run (Preview)

### Command
```bash
/implement docs/01-planning/features/006-opentelemetry/ --dry-run
```

### Output
```
🔍 DRY RUN: Execution Preview

## Discovery
Plans found: 3
  001-infrastructure-foundation (29 tasks)
  002-telemetry-integration (22 tasks)
  003-dashboard-alerting (25 tasks)

## Validation
Schema: Valid
Dependencies: Valid
Review groups: 14

## Execution Plan
Execution order: 001 → 002 → 003

Plan 001 (29 tasks):
  Parallel batch 1: T001, T002, T003, T004 (no conflicts)
  Sequential: T005, T006
  Review checkpoint: T007 (RG001)
  Parallel batch 2: T008, T009, T010
  ...

Estimated duration: 46-48 hours
Review checkpoints: 14

⚠️ NO CHANGES MADE - This was a dry run
To execute: /implement docs/01-planning/features/006-opentelemetry/
```

---

## Example 5: Resume from Checkpoint

### Previous Run (Interrupted)
```
Session interrupted at T045/76 (59% complete)
IMPLEMENTATION_PROGRESS.md saved
```

### Resume Command
```bash
/implement docs/01-planning/features/006-opentelemetry/ --resume
```

### Output
```
📂 Resuming from checkpoint...

Reading IMPLEMENTATION_PROGRESS.md...
Last completed: RG008 (T001-T044)
Next pending: RG009 (T045-T052)

Skipping completed review groups: RG001-RG008
Starting at: T045

📊 Implementation Progress: 002-telemetry-integration
Phase 2: 🔄 T045-T048 in_progress [development]
Status: 44/76 tasks | Resuming...
```

---

## Example 6: Single Plan Execution

### Command
```bash
/implement docs/01-planning/features/006-opentelemetry/ --plan=002
```

### Output
```
📁 Discovering TASKS.json files...

Filtering for plan: 002-telemetry-integration

Found 1 plan:
  002-telemetry-integration (22 tasks, 6 SP)

## Execution
[Proceeds with only plan 002]
```

---

## Example 7: Skip Specific Tasks

### Command
```bash
/implement docs/01-planning/features/006-opentelemetry/ --skip-tasks=T009,T010,T011,T012
```

### Output
```
📁 Discovering TASKS.json files...

⚠️ Skipping tasks: T009, T010, T011, T012

Found 3 plans:
  001-infrastructure-foundation (25 tasks after skip)
  002-telemetry-integration (22 tasks)
  003-dashboard-alerting (25 tasks)

Total: 72 tasks (4 skipped)

[Proceeds without skipped tasks]
```
