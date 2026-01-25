# Universe Selector Documentation

Documentation for the universe-selector agent.

## Contents

| Document | Purpose |
|----------|---------|
| [domain-expertise.md](domain-expertise.md) | Survivor bias patterns, sector classification |
| [validation-rules.md](validation-rules.md) | Gate thresholds, scoring formulas |

## Quick Links

- **Schema**: `../schemas/universe-selector.schema.json`
- **Examples**: `../examples/`
- **Agent Definition**: `../universe-selector.md`

## Integration Points

- **Upstream**: `/algo-strategy` command (P1-P3 Definition Layer)
- **Downstream**: `strategy-builder`, `backtester`
- **Peer Delegation**: `market-data-specialist` (OHLCV validation)
