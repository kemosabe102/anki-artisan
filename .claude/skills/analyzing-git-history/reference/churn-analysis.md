# Churn Analysis Reference

Git commands and patterns for measuring code churn and identifying high-volatility files.

---

## High-Churn Files (3-Month Window)

**Command**:
```bash
git log --since="3 months ago" --name-only --format="" | sort | uniq -c | sort -rn | head -20
```

**Output Format**:
```
  45 packages/core/auth.py
  38 packages/api/handlers.py
  32 packages/connectors/redis.py
```

**Interpretation**:
- Column 1: Number of commits touching this file
- Column 2: File path
- Top 20 files by commit count = potential hotspots

---

## Recurrent Churn (Month-Over-Month)

Files changed across multiple consecutive months indicate chronic instability.

**Command**:
```bash
for month in {0..2}; do
  git log --since="$month months ago" --until="$((month+1)) months ago" --name-only --format="" | sort -u
done | sort | uniq -c | awk '$1 >= 3'
```

**Interpretation**:
- Files appearing in 3+ consecutive months = recurrent churn
- Indicates ongoing instability or scope creep
- Prioritize for refactoring or architectural review

---

## Defect Density Correlation

Correlate file changes with bug-related commits.

**Command**:
```bash
# Find bug-related commits in 6-month window
git log --grep="BUG-\|fixes #\|fix:\|hotfix" --since="6 months ago" --name-only --format="" | sort | uniq -c | sort -rn
```

**Alternative (case-insensitive)**:
```bash
git log -i --grep="bug\|fix\|defect\|issue" --since="6 months ago" --name-only --format="" | sort | uniq -c | sort -rn
```

**Defect Ratio Calculation**:
```
defect_ratio = bug_commits / total_commits
```

Where:
- `bug_commits`: Commits matching bug patterns for this file
- `total_commits`: All commits for this file in the window


---

## Churn Normalization

Normalize churn counts to 0.0-1.0 scale for hotspot calculation.

**Formula**:
```
normalized_churn = file_commits / max_commits_in_window
```

**Example**:
```
File A: 45 commits
File B: 30 commits
Max in window: 50 commits

normalized_churn_A = 45 / 50 = 0.90
normalized_churn_B = 30 / 50 = 0.60
```

---

## Thresholds

| Churn Level | Normalized Range | Action |
|-------------|------------------|--------|
| Critical | >= 0.80 | Immediate review |
| High | 0.50 - 0.79 | Schedule stabilization |
| Moderate | 0.25 - 0.49 | Monitor |
| Low | < 0.25 | No action |

---

## Related

- [Hotspot Formula](hotspot-formula.md) - Uses normalized churn in scoring
- [Ownership Analysis](ownership.md) - Combine with churn for full picture
