# Diversity Sampling Reference

Quantitative targets and scoring for test dataset diversity.

---

## Distribution Targets

### Change Type Distribution (20 scenarios)

| Type | Range | Count |
|------|-------|-------|
| feat | 20-30% | 4-6 |
| fix | 15-25% | 3-5 |
| refactor | 10-20% | 2-4 |
| docs | 5-15% | 1-3 |
| test | 5-15% | 1-3 |
| style | 0-10% | 0-2 |
| other (perf, ci, build, chore) | 15-25% | 3-5 |

### File Count Distribution

| Files Changed | Target | Count (20 scenarios) |
|---------------|--------|----------------------|
| 1-5 | 15% | 3 |
| 6-10 | 40% | 8 |
| 11-15 | 30% | 6 |
| 16-50+ | 15% | 3 |

---

## Diversity Score Calculation

```python
diversity_score = (
    change_type_entropy * 0.4 +
    file_count_distribution_score * 0.3 +
    edge_case_coverage_ratio * 0.3
)
```

### Component Calculations

**Change Type Entropy** (Shannon entropy normalized to 0-1):
```python
from math import log2
probabilities = [count/total for count in change_type_counts]
entropy = -sum(p * log2(p) for p in probabilities if p > 0)
max_entropy = log2(len(change_types))
change_type_entropy = entropy / max_entropy
```

**File Count Distribution Score** (Chi-squared goodness-of-fit):
```python
observed = [count_1_5, count_6_10, count_11_15, count_16_50]
expected = [0.15 * total, 0.40 * total, 0.30 * total, 0.15 * total]
chi2, _ = chisquare(observed, expected)
file_count_distribution_score = max(0, 1 - chi2 / 100)
```

**Edge Case Coverage Ratio**:
```python
edge_case_coverage_ratio = len(covered_edge_cases) / 7
```

---

## Quality Thresholds

| Score | Grade | Status |
|-------|-------|--------|
| >= 0.90 | Excellent | All targets met |
| 0.80-0.89 | Good | Minor gaps |
| 0.70-0.79 | Acceptable | Notable gaps |
| < 0.70 | Poor | Significant imbalance |

**Minimum Acceptable**: 0.80

---

## Stratified Sampling Strategy

### Phase 1: Initial Selection

```bash
# Select candidates from each change type stratum
git log --oneline --all -150 | grep "^[a-f0-9]\+ feat:" | head -5
git log --oneline --all -150 | grep "^[a-f0-9]\+ fix:" | head -4
```

### Phase 2: File Count Balancing

```bash
# Check file count per commit
git show --stat <commit-sha> | tail -1
```

### Phase 3: Edge Case Prioritization

```bash
# Renamed/deleted files
git log --diff-filter=R --diff-filter=D

# Mixed types
git log --oneline | grep -E "(feat|fix):"
```

### Phase 4: Iterative Refinement

1. Calculate diversity score after initial selection
2. Identify gaps (missing types, imbalance, edge cases)
3. Search for additional candidates
4. Recalculate score
5. Repeat until score >= 0.80 or candidates exhausted
