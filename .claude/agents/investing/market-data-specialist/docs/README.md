# Market Data Specialist - Documentation

Domain expertise documentation for the market-data-specialist agent.

## Contents

| Document | Purpose | When to Consult |
|----------|---------|-----------------|
| [domain-knowledge.md](domain-knowledge.md) | OHLCV standards, missing data strategies, corporate actions | OHLCV validation, data quality assessment |
| [storage-optimization.md](storage-optimization.md) | Parquet compression, partitioning, SQLAlchemy patterns | Storage optimization, model design |
| [development-workflows.md](development-workflows.md) | DataConnector protocol, circuit breaker, fallback chains | API connector implementation |

## Quick Reference

### OHLCV Validation (8 Fields, 7 Rules)
**Fields**: Open, High, Low, Close, Volume, Timestamp, AdjClose, Ticker
**Rules**: High≥max(O,C), Low≤min(O,C), High≥Low, Volume≥0, Prices≥0, Chronological, Valid ticker

### Compression Codecs
| Workload | Codec | Ratio | Speed |
|----------|-------|-------|-------|
| Real-time | Snappy | 48% | Fast |
| Production | ZSTD-1 | 66% | Balanced |
| Archival | ZSTD-19 | 71% | Slow |

### API Provider Rate Limits
| Provider | Free Tier | Paid Tier |
|----------|-----------|-----------|
| Alpaca | 200/min | 1000/min |
| Polygon | 5/min | Unlimited |
| Yahoo | ~60/min | N/A |
