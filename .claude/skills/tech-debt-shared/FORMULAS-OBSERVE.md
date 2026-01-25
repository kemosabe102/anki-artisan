# OBSERVE Phase Formulas

Data collection formulas for code analysis and git history. Used during evidence gathering.

**Skills Using This File**: `analyzing-code-complexity`, `analyzing-git-history`

---

## 1. Cyclomatic Complexity (CC)

**Formula**:
```
CC = 1 + decision_points
```

**Decision Points** (each adds +1):
- `if` statements
- `else if` / `elif` clauses
- `for` loops
- `while` loops
- `do-while` loops
- `case` statements (in switch)
- `catch` blocks
- Ternary operators (`?:`)

**Logical Operators** (weighted at 0.5 each):
- `&&` (AND)
- `||` (OR)

**Risk Classification**:
| CC | Risk | Test Cases Needed | Action |
|----|------|-------------------|--------|
| 1-5 | LOW | 1-5 | OK, simple to test |
| 6-10 | MODERATE | 6-10 | Manageable |
| 11-15 | HIGH | 11-15 | Difficult to test |
| 16-20 | VERY_HIGH | 16-20 | Error-prone |
| >20 | CRITICAL | >20 | Unmaintainable |

**Example**:
```python
def get_grade(score):      # Base: 1
    if score >= 90:        # +1
        return 'A'
    elif score >= 80:      # +1
        return 'B'
    elif score >= 70:      # +1
        return 'C'
    else:
        return 'F'
# CC = 1 + 3 = 4 (LOW risk)
```

---

## 2. Git Churn Analysis

**Churn Score** (normalized):
```
churn_normalized = min(commits_90d / 30, 1.0)
```

**Parameters**:
| Metric | Calculation | Window |
|--------|-------------|--------|
| Commit count | Total commits touching file | 90 days |
| Lines changed | Added + deleted lines | 90 days |
| Unique authors | Distinct committers | 90 days |

**Bug-Related Commits**:
```
defect_ratio = bug_commits / total_commits
```
Identify bug commits by message patterns: `fix`, `bug`, `issue #`, `hotfix`

**High Churn Threshold**: >30 commits in 90 days = highly volatile file

---

## 3. Duplication Detection

**Duplication Percentage**:
```
duplication_pct = (duplicated_lines / total_lines) × 100
```

**Detection Thresholds**:
| Block Size | Action |
|------------|--------|
| <6 lines | Ignore (too small) |
| 6-15 lines | Flag for review |
| >15 lines | Definite refactoring target |

**Healthy Threshold**: <5% duplication = acceptable

---

## 4. File Coupling

**Coupling Score** (normalized):
```
coupling_normalized = min(external_deps / 10, 1.0)
```

**External Dependencies Include**:
- Import statements (other modules)
- Class inheritance chains
- Function calls to external modules
- Shared global state access

**High Coupling Threshold**: >10 external dependencies

---

## Output Contract (OBSERVE Phase)

```json
{
  "complexity_findings": [
    {"file": "path/to/file.py", "function": "name", "cc": 12, "risk": "HIGH"}
  ],
  "churn_files": [
    {"file": "path/to/file.py", "commits": 25, "authors": 4, "defect_ratio": 0.3}
  ],
  "duplication": {
    "total_pct": 4.2,
    "blocks": [{"files": ["a.py", "b.py"], "lines": 15}]
  },
  "coupling": [
    {"file": "path/to/file.py", "external_deps": 8}
  ]
}
```

---

## Cross-References

- **DEFINITIONS.md**: Threshold values, normalization rules
- **FORMULAS-ORIENT.md**: Consumes these metrics for scoring
