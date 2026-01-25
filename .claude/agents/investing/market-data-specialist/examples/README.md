# Market Data Specialist - Examples

Example delegations and output templates for orchestrator reference.

## Contents

| Example | Purpose |
|---------|---------|
| [delegation-examples.md](delegation-examples.md) | How orchestrator invokes this agent |

## Quick Delegation Patterns

### OHLCV Validation
```
Task(market-data-specialist, "Validate OHLCV data in data/ohlcv/AAPL_2024.parquet. 
Apply 8-field schema and 7 consistency rules. Quality threshold: 0.95.")
```

### API Connector Implementation
```
Task(market-data-specialist, "Implement Alpaca connector following DataConnector protocol.
Include circuit breaker (5 failures, 60s reset) and fallback to Polygon.")
```

### Parquet Compression
```
Task(market-data-specialist, "Optimize Parquet storage for data/market/. 
Target 70% compression. Benchmark snappy vs zstd. Apply hybrid partitioning (date/ticker).")
```

### SQLAlchemy Model
```
Task(market-data-specialist, "Design SQLAlchemy ORM model for daily OHLCV data.
Composite index on (ticker, trade_date). NO database DDL - ORM only.")
```
