# Shared Definitions: Tech Debt Domain

Common terms, thresholds, and normalization rules used across all formula files.

---

## Normalization Standards

All component scores normalize to **0.0-1.0 scale** before formula application.

**Capping Rule**: Values exceeding threshold cap at 1.0
```
normalized = min(actual / threshold, 1.0)
```

---

## Standard Thresholds

| Metric | Threshold | Source |
|--------|-----------|--------|
| Cyclomatic Complexity | 15 per function | SIG/ISO 25010 |
| Code Duplication | 5% of codebase | Industry standard |
| Unit Size | 30 LOC per method | SIG |
| Parameter Count | 4 per method | SIG |
| Churn (90-day) | 30 commits | Project calibration |
| Coupling | 10 external deps | Project calibration |

---

## Business Criticality Levels

| Level | Value | Examples |
|-------|-------|----------|
| Core | 1.0 | Authentication, payment, data integrity |
| Critical | 0.8 | API endpoints, core business logic |
| Support | 0.5 | Utilities, helpers, internal services |
| Utility | 0.2 | Scripts, one-off tools, dev utilities |

---

## Time Estimation Baselines

**Development Productivity**:
- Industry standard: 10 LOC/hour (0.1 LOC/minute)
- `development_hours = total_LOC / 10`

**Effort Estimates by Issue Category**:
| Category | Minutes | Hours |
|----------|---------|-------|
| Duplication block | 30 | 0.5 |
| Complex function | 45 | 0.75 |
| Security vulnerability | 60 | 1.0 |
| Missing test coverage | 20 | 0.33 |
| Missing documentation | 15 | 0.25 |
| Performance issue | 40 | 0.67 |

---

## Risk Level Classifications

**Cyclomatic Complexity Risk**:
| CC | Risk | Action |
|----|------|--------|
| 1-5 | LOW | OK |
| 6-10 | MODERATE | Watch |
| 11-15 | HIGH | Refactor soon |
| 16-20 | VERY_HIGH | Refactor now |
| >20 | CRITICAL | Urgent refactor |

**Hotspot Score Risk**:
| Score | Risk | Action |
|-------|------|--------|
| 0.00-0.30 | LOW | Monitor |
| 0.30-0.50 | MEDIUM | Next sprint |
| 0.50-0.75 | HIGH | This sprint |
| 0.75-1.00 | CRITICAL | Urgent refactor |

---

## Cross-References

- **FORMULAS-OBSERVE.md**: Uses thresholds for CC, churn, duplication
- **FORMULAS-ORIENT.md**: Uses criticality, risk classifications
- **FORMULAS-DECIDE.md**: Uses effort estimates, risk levels
