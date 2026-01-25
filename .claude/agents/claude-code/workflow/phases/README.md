# Workflow Agent Phases

This directory contains the OODA-aligned phase documentation for the workflow agent.

## Phase Structure

| Phase | File | Purpose | Time Allocation |
|-------|------|---------|-----------------|
| OBSERVE | [phase-1-observe.md](phase-1-observe.md) | Context gathering, operation identification, input validation | 15-20% |
| ORIENT | [phase-2-orient.md](phase-2-orient.md) | Research via Context7/Perplexity, CQ assessment, framework selection | 20-25% |
| DECIDE | [phase-3-decide.md](phase-3-decide.md) | Planning, mode selection, risk assessment, todo creation | 10-15% |
| ACT | [phase-4-act.md](phase-4-act.md) | Execution, 7-stage validation, output generation | 50-55% |

## Flow

```
User Request
    │
    ▼
┌─────────┐     CQ < 0.70     ┌─────────┐
│ OBSERVE │ ───────────────── │ ESCALATE│
└────┬────┘                   └─────────┘
     │ CQ >= 0.70
     ▼
┌─────────┐     CQ < 0.85     ┌──────────┐
│ ORIENT  │ ◄──────────────── │ RESEARCH │
└────┬────┘     (iterate)     └──────────┘
     │ CQ >= 0.85
     ▼
┌─────────┐
│ DECIDE  │ ─── Plan approved
└────┬────┘
     │
     ▼
┌─────────┐     Validation     ┌─────────┐
│  ACT    │ ───────────────── │ AUTO-FIX│
└────┬────┘     failure        └────┬────┘
     │                              │
     │ ◄────────────────────────────┘
     │          (retry x3)
     ▼
┌─────────────────┐
│ SUCCESS/FAILURE │
└─────────────────┘
```

## Key Gates

| Gate | Threshold | Action if Failed |
|------|-----------|------------------|
| CQ after OBSERVE | >= 0.70 | Escalate to user |
| CQ after ORIENT | >= 0.85 | Iterate research (max 3 cycles) |
| Validation in ACT | All checks pass | Auto-fix (max 3 retries) |
| Operation timeout | 600 seconds | FAILURE with partial results |

## Related Resources

- Main agent: [../workflow.md](../workflow.md)
- Operations: [../docs/workflow-operations.md](../docs/workflow-operations.md)
- Schema: [../schemas/workflow.schema.json](../schemas/workflow.schema.json)
