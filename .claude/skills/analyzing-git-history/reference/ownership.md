# Ownership Analysis Reference

Git commands and patterns for measuring code ownership and identifying dispersed-ownership files.

---

## Contributors Per File

**Command**:
```bash
git shortlog -sn --since="6 months ago" -- <file>
```

**Output Format**:
```
    25  Alice Developer
    15  Bob Engineer
     8  Charlie Coder
     2  Diana Dev
```

**Interpretation**:
- Column 1: Commit count by author
- Column 2: Author name
- Sorted by contribution (highest first)

---

## Ownership Dispersion

Files with many contributors and no clear owner have higher defect risk.

**Dispersion Metric**:
```
dispersion = 1 - (top_owner_commits / total_commits)
```

**Example**:
```
File: packages/core/auth.py
- Total commits: 50
- Top owner (Alice): 25 commits
- Top owner percentage: 25/50 = 0.50 (50%)
- Dispersion: 1 - 0.50 = 0.50

Interpretation: 50% dispersion = moderate risk
```

---

## Top Owner Percentage Calculation

**Formula**:
```
top_owner_pct = max_contributor_commits / total_file_commits
```

**Batch Command** (all files in directory):
```bash
for file in $(git ls-files "packages/core/*.py"); do
  total=$(git log --oneline --since="6 months ago" -- "$file" | wc -l)
  top=$(git shortlog -sn --since="6 months ago" -- "$file" | head -1 | awk '{print $1}')
  if [ "$total" -gt 0 ]; then
    pct=$(echo "scale=2; $top / $total" | bc)
    echo "$pct $file"
  fi
done | sort -n
```

---

## Risk Thresholds

| Top Owner % | Dispersion | Risk Level | Recommendation |
|-------------|------------|------------|----------------|
| >= 70% | <= 0.30 | Low | Clear ownership |
| 50-69% | 0.31-0.50 | Moderate | Monitor |
| 30-49% | 0.51-0.70 | High | Assign owner |
| < 30% | > 0.70 | Critical | Urgent: assign owner |


**Research Basis**: Files with <30% top owner have 2-3x higher defect rates (Microsoft Research, 2011).

---

## Contributor Count Analysis

**Command** (count unique contributors):
```bash
git shortlog -sn --since="6 months ago" -- <file> | wc -l
```

**Risk by Contributor Count**:

| Contributors | Risk Factor | Notes |
|--------------|-------------|-------|
| 1-2 | Low | Clear ownership, possible bus factor risk |
| 3-5 | Moderate | Healthy collaboration |
| 6-10 | Elevated | Consider splitting file |
| > 10 | High | File likely too large/complex |

---

## Combining Ownership with Churn

High churn + dispersed ownership = highest risk combination.

**Combined Risk Matrix**:

| | Low Churn | High Churn |
|---|-----------|------------|
| **Clear Owner** | Low risk | Moderate - owner may be overwhelmed |
| **Dispersed** | Moderate - ownership unclear | Critical - unstable and unowned |

---

## Related

- [Churn Analysis](churn-analysis.md) - Combine with ownership metrics
- [Hotspot Formula](hotspot-formula.md) - Ownership informs criticality scoring
