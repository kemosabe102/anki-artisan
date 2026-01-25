# Severity Classification Reference

## Decision Tree

```
                    ┌─────────────────────────────────────┐
                    │ Confidence >= 0.90?                 │
                    └─────────────────────────────────────┘
                               │
              ┌────────────────┴────────────────┐
              │ YES                             │ NO
              ▼                                 ▼
┌─────────────────────────────┐    ┌─────────────────────────────┐
│ Security/Data Risk?         │    │ Confidence >= 0.70?         │
└─────────────────────────────┘    └─────────────────────────────┘
         │                                    │
    ┌────┴────┐                    ┌──────────┴──────────┐
    │YES      │NO                  │YES                  │NO
    ▼         ▼                    ▼                     ▼
CRITICAL    MAJOR          ┌──────────────────┐   ┌──────────────┐
                           │ Public API?      │   │ Style only?  │
                           └──────────────────┘   └──────────────┘
                                  │                      │
                           ┌──────┴──────┐         ┌────┴────┐
                           │YES          │NO       │YES      │NO
                           ▼             ▼         ▼         ▼
                         MAJOR        MINOR       NIT    DO NOT
                                                        REPORT
```

---

## Severity Definitions

### CRITICAL (Max 3 per review)
- Security vulnerabilities (SQL injection, XSS, auth bypass)
- Data corruption or loss risk
- Production stability threats
- Confidence >= 0.90 required

### MAJOR (Max 5 per review)
- Logic errors affecting correctness
- API contract violations
- Performance issues (>100ms regression)
- Confidence >= 0.70 required for public APIs
- Confidence >= 0.90 for internal code

### MINOR (Max 5 per review)
- Code quality issues
- Missing error handling (non-critical paths)
- Documentation gaps
- Confidence 0.70-0.89 for internal code

### NIT (Max 2 per review)
- Style inconsistencies
- Naming suggestions
- Optional improvements
- Any confidence level

---

## Risk Categories

### Security Risks
- SQL injection patterns
- Authentication bypass
- Authorization failures
- Data exposure
- Path traversal

### Data Integrity Risks
- Silent data corruption
- Race conditions on writes
- Missing transaction boundaries
- Incorrect aggregations

### Stability Risks
- Unhandled exceptions in critical paths
- Resource leaks
- Infinite loops
- Deadlock potential

---

## Examples

| Finding | Confidence | Risk | Severity |
|---------|------------|------|----------|
| SQL string concatenation | 0.92 | Security | CRITICAL |
| Missing null check on API response | 0.85 | Stability | MAJOR |
| Inefficient loop in background job | 0.78 | Performance | MINOR |
| Variable name `x` instead of `count` | 0.95 | Style | NIT |
| Possible race condition | 0.55 | Data | DO NOT REPORT |
