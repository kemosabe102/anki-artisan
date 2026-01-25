# Diversity Sampling Methodology

**Purpose**: Quantitative targets and scoring for test dataset diversity

**Domain**: Algorithm validation test datasets

**Reference**: Used by `.claude/agents/dev-tools/test-dataset-creator/test-dataset-creator.md`

---

## Diversity Targets

### Change Type Distribution

**For FileGrouper and commit analysis algorithms**:

- **feat**: 20-30% (4-6 scenarios out of 20)
- **fix**: 15-25% (3-5 scenarios)
- **refactor**: 10-20% (2-4 scenarios)
- **docs**: 5-15% (1-3 scenarios)
- **test**: 5-15% (1-3 scenarios)
- **style**: 0-10% (0-2 scenarios)
- **Other types** (perf, ci, build, chore): 15-25% combined (3-5 scenarios)

### File Count Distribution

**Target ranges for realistic commit scenarios**:

- **1-5 files**: 15% (3 scenarios) - Small focused changes
- **6-10 files**: 40% (8 scenarios) - Medium complexity changes
- **11-15 files**: 30% (6 scenarios) - Large feature development
- **16-50 files**: 15% (3 scenarios) - Major refactoring or releases

### Edge Case Coverage

**7 Required Cases** (must have at least one scenario for each):

1. **mixed_change_types**: Single commit with multiple change types (e.g., feat + fix + docs)
2. **test_only_changes**: Commit modifying only test files (no application code)
3. **large_repository_50_files**: Commit with 50+ files changed (major refactoring)
4. **low_confidence_ambiguous**: Unclear grouping, multiple valid interpretations
5. **renamed_deleted_files**: Files with rename or delete operations
6. **ungrouped_files**: Files that don't fit into logical groups
7. **dependency_ordering**: Files with strict dependency relationships

## Diversity Score Calculation

### Formula

```python
diversity_score = (
    change_type_entropy * 0.4 +
    file_count_distribution_score * 0.3 +
    edge_case_coverage_ratio * 0.3
)
```

### Component Calculations

**Change Type Entropy**:
```python
# Shannon entropy normalized to 0-1
from math import log2
probabilities = [count/total for count in change_type_counts]
entropy = -sum(p * log2(p) for p in probabilities if p > 0)
max_entropy = log2(len(change_types))
change_type_entropy = entropy / max_entropy
```

**File Count Distribution Score**:
```python
# Chi-squared goodness-of-fit to target distribution
from scipy.stats import chisquare
observed = [count_1_5, count_6_10, count_11_15, count_16_50]
expected = [0.15 * total, 0.40 * total, 0.30 * total, 0.15 * total]
chi2, p_value = chisquare(observed, expected)
file_count_distribution_score = max(0, 1 - chi2 / 100)  # Normalize to 0-1
```

**Edge Case Coverage Ratio**:
```python
# Simple ratio of covered edge cases
edge_case_coverage_ratio = len(covered_edge_cases) / 7
```

### Quality Thresholds

- **Excellent (≥0.90)**: All targets met, balanced distribution
- **Good (0.80-0.89)**: Minor gaps in distribution or 1 missing edge case
- **Acceptable (0.70-0.79)**: Notable gaps, 2 missing edge cases
- **Poor (<0.70)**: Significant imbalance, 3+ missing edge cases

**Minimum Acceptable**: 0.80 (required for dataset approval)

## Sampling Strategy

### Stratified Sampling

**Phase 1: Initial Selection**
```bash
# Select candidates from each change type stratum
AGENT_NAME=test-dataset-creator git log --oneline --all -150 | grep "^[a-f0-9]\+ feat:" | head -5
AGENT_NAME=test-dataset-creator git log --oneline --all -150 | grep "^[a-f0-9]\+ fix:" | head -4
# ... repeat for other types
```

**Phase 2: File Count Balancing**
```bash
# Ensure file count distribution
AGENT_NAME=test-dataset-creator git show --stat <commit-sha> | tail -1  # Extract files changed
# Select commits to match target distribution
```

**Phase 3: Edge Case Prioritization**
```bash
# Identify and prioritize edge cases
AGENT_NAME=test-dataset-creator git log --diff-filter=R --diff-filter=D  # Renamed/deleted files
AGENT_NAME=test-dataset-creator git log --oneline | grep -E "(feat|fix):"  # Mixed types
```

### Iterative Refinement

1. Calculate diversity score after initial selection
2. Identify gaps (missing change types, file count imbalance, edge cases)
3. Search for additional candidates to fill gaps
4. Recalculate diversity score
5. Repeat until score ≥0.80 or candidates exhausted

---

**Token Savings**: ~60 lines externalized from agent definition
