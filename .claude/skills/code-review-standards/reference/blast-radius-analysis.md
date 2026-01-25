# Blast Radius Analysis Reference

## Formula

```
Blast_Radius = (Afferent_Coupling × 0.50) + (Change_Frequency × 0.25) + (Business_Criticality × 0.25)
```

---

## Afferent Coupling (0.0-1.0)

Number of files that depend on this file.

### Measurement
```bash
# Count files importing this module
grep -r "from module import" --include="*.py" | wc -l
grep -r "import module" --include="*.py" | wc -l
```

### Scoring

| Importers | Score | Priority |
|-----------|-------|----------|
| 10+ | 1.0 | CRITICAL |
| 5-9 | 0.75 | HIGH |
| 2-4 | 0.50 | MEDIUM |
| 0-1 | 0.25 | LOW |

---

## Change Frequency (0.0-1.0)

How often this file changes.

### Measurement
```bash
# Count commits touching this file in last 90 days
git log --since="90 days ago" --oneline -- path/to/file.py | wc -l
```

### Scoring

| Commits (90d) | Score |
|---------------|-------|
| 20+ | 1.0 |
| 10-19 | 0.75 |
| 5-9 | 0.50 |
| 1-4 | 0.25 |
| 0 | 0.10 |

---

## Business Criticality (0.0-1.0)

Impact on business operations if this code fails.

### Scoring

| Characteristic | Score |
|----------------|-------|
| User-facing, auth, payment | 1.0 |
| Data processing, API endpoints | 0.75 |
| Internal services, utilities | 0.50 |
| Logging, monitoring | 0.25 |
| Tests, dev tools | 0.10 |

---

## Review Depth by Blast Radius

| Blast Radius | Review Depth | Rate Limits |
|--------------|--------------|-------------|
| CRITICAL (>0.8) | Full coverage, all severity levels | Bypass limits |
| HIGH (0.6-0.8) | Standard review | 3/5/5/2 |
| MEDIUM (0.4-0.6) | Major issues only | Skip Minor, Nit |
| LOW (<0.4) | Critical issues only | Critical only |

---

## Example Calculation

**File**: `packages/auth/token_validator.py`

```
Afferent: 12 files import this → Score: 1.0
Frequency: 8 commits in 90 days → Score: 0.50
Criticality: Auth module → Score: 1.0

Blast_Radius = (1.0 × 0.50) + (0.50 × 0.25) + (1.0 × 0.25)
             = 0.50 + 0.125 + 0.25
             = 0.875

Priority: CRITICAL → Full coverage review
```
