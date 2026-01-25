# PromQL Query Builder - Documentation

Domain expertise for PromQL query construction.

## Contents

| Document | Purpose |
|----------|---------|
| [query-construction-patterns.md](./query-construction-patterns.md) | Recording rules criteria, rate interval selection, time-period comparison patterns |
| [signal-detection-guide.md](./signal-detection-guide.md) | Label selection strategies, cardinality management, reduction techniques |

## Quick Reference

### Recording Rule Thresholds
- **Complexity**: >3 operators
- **Execution**: >500ms
- **Frequency**: >10 requests/min
- **Cardinality**: >100 time series

### Rate Interval Guidelines
- **Minimum**: 4x scrape_interval
- **Standard**: 5m (dashboard queries)
- **Extended**: 1h+ (trend analysis)
- **Grafana**: `$__rate_interval`

### Cardinality Thresholds
- **Safe**: <10 label combinations/metric
- **Warning**: 10-100 combinations
- **Critical**: >100 combinations
- **Alert**: >10K total series

## Related Agents

For Prometheus alerting (alert rules, validation, tuning), see: `prometheus-alert-builder` agent
