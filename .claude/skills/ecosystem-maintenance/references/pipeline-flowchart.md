# 7-Stage Auto-Fix Pipeline Flowchart

Visual representation of the validation and auto-fix pipeline.

---

## Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           7-STAGE AUTO-FIX PIPELINE                         │
└─────────────────────────────────────────────────────────────────────────────┘

                                    ┌─────────┐
                                    │  START  │
                                    └────┬────┘
                                         │
                                         ▼
                    ┌────────────────────────────────────────┐
                    │           STAGE 1: DRY-RUN             │
                    │   Simulate operation without changes   │
                    └────────────────────┬───────────────────┘
                                         │
                              ┌──────────┴──────────┐
                              │   Simulation OK?    │
                              └──────────┬──────────┘
                                    │         │
                              YES   │         │ NO
                                    │         │
                                    ▼         ▼
                    ┌───────────────────┐   ┌───────────────────┐
                    │                   │   │  REPORT ISSUES    │
                    │                   │   │  Return FAILURE   │
                    └────────┬──────────┘   └───────────────────┘
                             │
                             ▼
                    ┌────────────────────────────────────────┐
                    │         STAGE 2: SMOKE TEST            │
                    │   Lightweight validation (paths,       │
                    │   links, syntax)                       │
                    └────────────────────┬───────────────────┘
                                         │
                              ┌──────────┴──────────┐
                              │   Issues Found?     │
                              └──────────┬──────────┘
                                    │         │
                               NO   │         │ YES
                                    │         │
                                    ▼         ▼
                    ┌───────────────────┐   ┌───────────────────┐
                    │   Skip to STAGE 4 │   │   FLAG ISSUES     │
                    │                   │   │   Continue        │
                    └────────┬──────────┘   └────────┬──────────┘
                             │                       │
                             │                       ▼
                             │      ┌────────────────────────────────────────┐
                             │      │         STAGE 3: AUTO-FIX              │
                             │      │   Automatic repair of known patterns   │
                             └─────►└────────────────────┬───────────────────┘
                                                         │
                                              ┌──────────┴──────────┐
                                              │  Fixes Applied?     │
                                              └──────────┬──────────┘
                                                    │         │
                                               YES  │         │ NO
                                                    │         │
                                                    ▼         │
                                    ┌───────────────────┐     │
                                    │   LOG FIXES       │     │
                                    └────────┬──────────┘     │
                                             │                │
                                             └───────┬────────┘
                                                     │
                                                     ▼
                    ┌────────────────────────────────────────┐
                    │          STAGE 4: VALIDATE             │
                    │   Full validation against standards    │
                    └────────────────────┬───────────────────┘
                                         │
                              ┌──────────┴──────────┐
                              │  Validation Pass?   │
                              └──────────┬──────────┘
                                    │         │
                              YES   │         │ NO
                                    │         │
                                    ▼         ▼
                    ┌───────────────────┐   ┌───────────────────┐
                    │                   │   │  RETRY < 3?       │
                    │                   │   │  ├─ YES: STAGE 3  │
                    │                   │   │  └─ NO: FAILURE   │
                    └────────┬──────────┘   └───────────────────┘
                             │
                             ▼
                    ┌────────────────────────────────────────┐
                    │           STAGE 5: APPLY               │
                    │   Execute file modifications           │
                    └────────────────────┬───────────────────┘
                                         │
                              ┌──────────┴──────────┐
                              │    Apply Success?   │
                              └──────────┬──────────┘
                                    │         │
                              YES   │         │ NO
                                    │         │
                                    ▼         ▼
                    ┌───────────────────┐   ┌───────────────────┐
                    │                   │   │  ROLLBACK         │
                    │                   │   │  Return FAILURE   │
                    └────────┬──────────┘   └───────────────────┘
                             │
                             ▼
                    ┌────────────────────────────────────────┐
                    │           STAGE 6: CHECK               │
                    │   Read-back verification               │
                    └────────────────────┬───────────────────┘
                                         │
                              ┌──────────┴──────────┐
                              │  Content Matches?   │
                              └──────────┬──────────┘
                                    │         │
                              YES   │         │ NO
                                    │         │
                                    ▼         ▼
                    ┌───────────────────┐   ┌───────────────────┐
                    │                   │   │  RETRY or         │
                    │                   │   │  ROLLBACK         │
                    └────────┬──────────┘   └───────────────────┘
                             │
                             ▼
                    ┌────────────────────────────────────────┐
                    │        STAGE 7: FINAL VERIFY           │
                    │   Integration testing                  │
                    └────────────────────┬───────────────────┘
                                         │
                              ┌──────────┴──────────┐
                              │  Integration OK?    │
                              └──────────┬──────────┘
                                    │         │
                              YES   │         │ NO
                                    │         │
                                    ▼         ▼
                    ┌───────────────────┐   ┌───────────────────┐
                    │     SUCCESS       │   │  REPORT           │
                    │  Return results   │   │  DEGRADATION      │
                    └───────────────────┘   └───────────────────┘
```

---

## Stage Transition Rules

| From Stage | To Stage | Condition |
|------------|----------|-----------|
| 1. DRY-RUN | 2. SMOKE | Simulation passes |
| 1. DRY-RUN | FAILURE | Simulation fails |
| 2. SMOKE | 3. AUTO-FIX | Issues detected |
| 2. SMOKE | 4. VALIDATE | No issues |
| 3. AUTO-FIX | 4. VALIDATE | Always (after logging) |
| 4. VALIDATE | 5. APPLY | Validation passes |
| 4. VALIDATE | 3. AUTO-FIX | Validation fails, retry < 3 |
| 4. VALIDATE | FAILURE | Validation fails, retry >= 3 |
| 5. APPLY | 6. CHECK | Apply succeeds |
| 5. APPLY | ROLLBACK | Apply fails |
| 6. CHECK | 7. VERIFY | Content matches |
| 6. CHECK | RETRY/ROLLBACK | Content mismatch |
| 7. VERIFY | SUCCESS | Integration OK |
| 7. VERIFY | DEGRADATION | Integration issues |

---

## Retry Behavior

```
Retry Counter: 0
    │
    ▼
VALIDATION FAILURE ──► Retry Counter++
    │
    ▼
┌───────────────────────────────┐
│  Retry Counter < 3?           │
│  ├─ YES: Go to STAGE 3        │
│  │       (AUTO-FIX)           │
│  └─ NO:  Return FAILURE       │
│          with attempts log    │
└───────────────────────────────┘
```

---

## Time Allocation per Stage

| Stage | Typical Duration | Max Duration |
|-------|------------------|--------------|
| DRY-RUN | <5s | 30s |
| SMOKE | <10s | 60s |
| AUTO-FIX | <30s | 120s |
| VALIDATE | <30s | 120s |
| APPLY | <10s | 60s |
| CHECK | <5s | 30s |
| VERIFY | <30s | 180s |
| **Total** | **<2 min** | **10 min** |

**Hard Limit**: 600 seconds (10 minutes) total pipeline time

---

## Pipeline State Preservation

At each stage, preserve:
- Current stage number
- Retry counter
- Applied fixes log
- Validation results
- File state snapshots (for rollback)

This enables resume-from-failure and debugging of pipeline issues.

