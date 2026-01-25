# Backtester Agent Phases

This directory contains the OODA-aligned phase documentation for the backtester agent.

## Phase Structure

| Phase | File | Purpose | Time Allocation |
|-------|------|---------|-----------------|
| OBSERVE | [phase-1-observe.md](phase-1-observe.md) | HDD enforcement, hypothesis validation, input validation | 10-15% |
| ORIENT | [phase-2-orient.md](phase-2-orient.md) | Environment verification, config loading, path validation | 15-20% |
| DECIDE | [phase-3-decide.md](phase-3-decide.md) | Mode detection, timeout configuration, gate setup | 10-15% |
| ACT | [phase-4-act.md](phase-4-act.md) | Execution, aggregation, gate evaluation, verdict routing | 55-65% |

## Flow

```
Backtest Request
    │
    ▼
┌─────────┐   Missing hypothesis_id   ┌─────────┐
│ OBSERVE │ ─────────────────────────│  HALT   │
└────┬────┘                          └─────────┘
     │ HDD compliant
     ▼
┌─────────┐   Environment invalid    ┌─────────┐
│ ORIENT  │ ─────────────────────────│ FAILURE │
└────┬────┘                          └─────────┘
     │ Config loaded
     ▼
┌─────────┐
│ DECIDE  │ ─── Mode selected, gates configured
└────┬────┘
     │
     ▼
┌─────────┐   Gate failure           ┌──────────────────┐
│   ACT   │ ─────────────────────────│ failure-analyzer │
└────┬────┘                          └──────────────────┘
     │
     ▼
┌───────────────────────────────────┐
│ DEPLOYABLE / NOT_DEPLOYABLE      │
└───────────────────────────────────┘
```

## Key Gates and Thresholds

See [gate-thresholds.md](../docs/gate-thresholds.md) for complete threshold definitions.

| Gate | Phase | Action if Failed |
|------|-------|------------------|
| hypothesis_id required | OBSERVE | HALT immediately |
| trial_number <= 5 | OBSERVE | HALT (max trials exceeded) |
| Environment verified | ORIENT | FAILURE with diagnostics |
| Mode detected | DECIDE | Default to single_run |
| Statistical gates | ACT | Route to failure-analyzer |

## Related Resources

- Main agent: [../backtester.md](../backtester.md)
- Output examples: [../examples/output-examples.md](../examples/output-examples.md)
- Schema: [../schemas/backtester.schema.json](../schemas/backtester.schema.json)
