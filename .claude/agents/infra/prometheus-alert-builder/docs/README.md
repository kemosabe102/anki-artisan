# Prometheus Alert Builder - Documentation

Domain expertise for Prometheus alert rule construction, validation, and tuning.

## Contents

| Document | Purpose |
|----------|---------|
| [alert-rules-ref.md](./alert-rules-ref.md) | 50+ anti-patterns, 30+ best practices, side-by-side comparisons |
| [alert-config-patterns.md](./alert-config-patterns.md) | 8 core patterns: Multi-tier severity, SLO burn rate, symptom+cause, predictive, Alertmanager config |
| [alert-tuning-method.md](./alert-tuning-method.md) | 7-step methodology for tuning noisy alerts, firing pattern analysis, threshold optimization |

## Quick Reference

### Alert Threshold Guidelines
| Metric Type | Warning | Critical | For Clause |
|-------------|---------|----------|------------|
| CPU | >85% | >95% | 10-15m |
| Memory | >85% | >95% | 10m |
| Disk | <20% free | <10% free | 30m |
| Error rate | >1% | >5% | 10m |
| P99 latency | >1s | >3s | 15m |

### Anti-Pattern Quick Checks
- ❌ Missing `for` clause
- ❌ Using `irate()` in alerts
- ❌ High-cardinality labels ($value, request_id)
- ❌ Absolute thresholds
- ❌ Missing severity labels
- ❌ No annotations

## Related Agents

For PromQL query construction (dashboards, recording rules), see: `promql-query-builder` agent
