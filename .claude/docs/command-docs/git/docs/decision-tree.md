# Complete Decision Tree

Visual decision flowcharts for all phases of the `/git` command.

---

## Master Decision Tree

```text
User: /git prepare
|
+--------------------------------------------------+
| PHASE 1: VALIDATION                               |
+--------------------------------------------------+
|-- PASS -> Continue to Phase 2
|-- FAIL -> STOP
    |-- Option 1: Auto-fix (orchestrator delegates to debugger automatically)
    |   |-- IF PASS after fixes -> Continue to Phase 2
    |   |-- IF FAIL after 3 attempts -> Option 2
    |-- Option 2: Fix manually -> /git prepare (retry)
    |-- Option 3: Delegate to debugger -> /git prepare (retry)
    |-- Option 4: --skip-validation (HIGH RISK - emergency only)

+--------------------------------------------------+
| PHASE 2: FILE GROUPING                            |
+--------------------------------------------------+
|-- SUCCESS -> Continue to Phase 3
|-- FAILURE -> STOP
    |-- Option 1: Check git repository status (git status)
    |-- Option 2: Manual git commands (fallback)
    |-- Option 3: Report bug if FileGrouper error

+--------------------------------------------------+
| PHASE 3: QUALITY GATES                            |
+--------------------------------------------------+
|-- ALL APPROVED -> Continue to Phase 4 (commit all)
|-- SOME BLOCKED -> Continue to Phase 4 (partial commit available)
|   |-- Option 1: /git commit --groups=<approved> (partial)
|   |-- Option 2: Fix issues -> /git prepare (retry all)
|   |-- Option 3: --skip-quality (HIGH RISK - experimental only)
|-- ALL BLOCKED -> STOP
    |-- Option 1: Fix blocking issues -> /git prepare (retry)
    |-- Option 2: --skip-quality (HIGH RISK - NOT RECOMMENDED)

+--------------------------------------------------+
| PHASE 4: PRESENT RESULTS (HUMAN DECISION)         |
+--------------------------------------------------+
|-- Option 1: /git commit (all groups)
|-- Option 2: /git commit --groups=1,2,3 (specific groups)
|-- Option 3: Fix first -> /git prepare (retry)
|-- Option 4: Cancel (no commit)

+--------------------------------------------------+
| PHASE 5: EXECUTE COMMITS                          |
+--------------------------------------------------+
|-- SUCCESS -> Ready to push
|-- FAILURE -> STOP
    |-- Option 1: Resolve conflicts -> /git commit (retry)
    |-- Option 2: Manual git commands (fallback)
    |-- Option 3: Reset and start over (git reset --soft HEAD~1)
    |-- Option 4: Skip failed group -> /git commit --groups=<remaining>
```

---

## Quality Gate Decision Tree

```text
Quality gates run
|
ALL APPROVED -> Continue to Phase 4 (commit all)
|
SOME BLOCKED -> Decision Point:
  |-- Are approved groups independent? YES -> Partial commit
  |   |-- /git commit --groups=<approved>
  |-- Are blocked issues quick fixes? YES -> Fix + retry
  |   |-- Fix -> /git prepare -> /git commit
  |-- Complex fixes needed? YES -> Fix first, commit later
      |-- Fix -> /git prepare (re-analyzes everything)
|
ALL BLOCKED -> MUST FIX
  |-- Fix blocking issues -> /git prepare -> /git commit
```

---

## Autonomous Recovery Decision Tree

```text
Phase fails
|
Is failure recoverable automatically?
|-- YES (validation/quality) -> Orchestrator attempts fix
|   |-- Delegate to debugger/development
|   |-- Re-run failed phase
|   |-- Iterate (max 3 attempts)
|   |-- IF SUCCESS -> Continue workflow
|   |-- IF FAIL after 3 -> Escalate to user
|-- NO (git errors, permissions) -> Escalate immediately
    |-- Report error details
    |-- Suggest recovery options
    |-- Wait for user action
```

---

## Skip Flag Decision Tree

```text
User wants to skip a phase
|
Which phase?
|-- Validation (--skip-validation)
|   |-- Is this an emergency? YES -> Proceed with caution
|   |-- Is this experimental branch? YES -> Acceptable risk
|   |-- Is this main/production? NO -> Do not skip
|-- Quality Gates (--skip-quality)
    |-- Is this experimental branch? YES -> Acceptable risk
    |-- Are you prototyping? YES -> Acceptable risk
    |-- Is this production code? NO -> Do not skip

Risk Assessment:
- --skip-validation: May commit failing tests, linting issues
- --skip-quality: May commit security vulnerabilities, critical bugs
- Both flags: Maximum risk - use only in emergencies
```

---

## Commit Selection Decision Tree

```text
Phase 4 presents N groups
|
How many groups approved?
|-- ALL approved -> /git commit (commit all)
|-- SOME approved, SOME blocked
|   |-- Are approved independent? YES -> Partial commit
|   |   |-- /git commit --groups=<approved>
|   |   |-- Fix blocked later
|   |-- Are approved dependent on blocked? NO partial commit
|       |-- Fix all first -> /git prepare
|-- NONE approved -> Must fix all
    |-- Address all blocking issues
    |-- /git prepare (retry)
```
