---
name: analyzing-code-complexity
description: Measure and analyze code complexity metrics including cyclomatic complexity, nesting depth, function length, and code duplication. Use when assessing code maintainability, identifying refactoring candidates, detecting code smells, or performing tech debt analysis.
---

# Code Complexity Analysis Skill

Systematic complexity measurement for tech debt assessment and refactoring prioritization.

## Reference Documentation

- **Thresholds** -> [reference/thresholds.md](reference/thresholds.md)
- **Detection Patterns** -> [reference/detection-patterns.md](reference/detection-patterns.md)
- **Duplication Analysis** -> [reference/duplication.md](reference/duplication.md)

---

## Quick Reference: Complexity Thresholds

| Metric | Threshold | Risk Level |
|--------|-----------|------------|
| Cyclomatic Complexity | >10 | High risk, refactor required |
| Function Length | >50 lines | Needs refactoring |
| Nesting Depth | >3 levels | Code smell |
| Code Duplication | >5% | Technical debt |

**SIG Low-Risk Benchmarks** (Software Improvement Group):

| Metric | Low-Risk Threshold |
|--------|-------------------|
| Complexity | <15 per function |
| Unit Size | <15 LOC per function |
| Parameters | <4 per function |

---

## Input/Output Contract

### Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| scope | Yes | File path, directory, or glob pattern |
| metrics | No | Subset: `complexity`, `length`, `nesting`, `duplication` |
| format | No | Output format: `summary`, `detailed`, `json` |

### Output

```json
{
  "scope": "<analyzed-scope>",
  "summary": {
    "total_functions": 0,
    "high_complexity": 0,
    "needs_refactoring": 0,
    "code_smells": 0,
    "duplication_pct": 0.0
  },
  "findings": [
    {
      "file": "<path>",
      "function": "<name>",
      "metric": "<metric-type>",
      "value": 0,
      "threshold": 0,
      "severity": "HIGH|MEDIUM|LOW"
    }
  ],
  "recommendations": []
}
```

---

## Analysis Workflow

1. **Scope Identification**: Parse target files/directories
2. **Metric Collection**: Run detection patterns (see [reference/detection-patterns.md](reference/detection-patterns.md))
3. **Threshold Comparison**: Flag violations per [reference/thresholds.md](reference/thresholds.md)
4. **Duplication Scan**: Identify duplicates per [reference/duplication.md](reference/duplication.md)
5. **Prioritization**: Rank by severity and blast radius
6. **Report Generation**: Output findings in requested format

---

## Severity Classification

| Severity | Criteria |
|----------|----------|
| HIGH | Complexity >15 OR nesting >4 OR duplication >10% |
| MEDIUM | Complexity 10-15 OR length 50-100 OR duplication 5-10% |
| LOW | Approaching thresholds (within 20%) |

---

## References

- **Shared Formulas**: `../tech-debt-shared/FORMULAS-OBSERVE.md` (CC, churn, duplication formulas)
- **Definitions**: `../tech-debt-shared/DEFINITIONS.md`

## Related Components

- **Agent**: `tech-debt-investigator` - Full debt analysis
- **Skill**: `code-review-standards` - Finding validation

---

## Scripts

Executable scripts for automated analysis. Run via `uv run python`.

| Script | Purpose | CLI |
|--------|---------|-----|
| `scripts/measure_complexity.py` | Cyclomatic complexity analysis using Radon | `--repo-path <path> [--output-file <path>] [--language python]` |
| `scripts/detect_duplication.py` | Code duplication detection using Pylint | `--repo-path <path> [--output-file <path>] [--min-lines <int>]` |

### Usage Example

```bash
uv run python .claude/skills/analyzing-code-complexity/scripts/measure_complexity.py --repo-path /path/to/repo --output-file complexity.json

uv run python .claude/skills/analyzing-code-complexity/scripts/detect_duplication.py --repo-path /path/to/repo --output-file duplication.json
```
