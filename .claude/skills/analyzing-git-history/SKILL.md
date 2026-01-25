---
name: analyzing-git-history
description: Collect and analyze git-based code metrics including code churn, ownership dispersion, recurrent changes, and defect correlation. Use when identifying hotspots, post-mortem analysis, ownership analysis, or churn detection.
---

# Analyzing Git History

**Purpose**: Extract actionable insights from git history to identify code hotspots, ownership patterns, and defect-prone areas for tech debt prioritization.

## Quick Reference

| Analysis Type | Command | Details |
|---------------|---------|---------|
| High-churn files | `git log --since="3 months ago" --name-only --format="" \| sort \| uniq -c \| sort -rn` | [churn-analysis.md](reference/churn-analysis.md) |
| Ownership | `git shortlog -sn --since="6 months ago" -- <file>` | [ownership.md](reference/ownership.md) |
| Hotspot score | `churn x complexity x defects x criticality` | [hotspot-formula.md](reference/hotspot-formula.md) |

## Use Cases

- **Hotspot Detection**: Identify files with high churn that need stabilization
- **Post-Mortem Analysis**: Trace defect patterns to root causes
- **Ownership Analysis**: Find files with dispersed ownership (higher defect risk)
- **Churn Detection**: Track month-over-month change patterns

---

## Input/Output Contract

### Input

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `scope` | string | Yes | File path, directory, or glob pattern |
| `window` | string | No | Time window (default: "3 months") |
| `analysis_type` | enum | No | `churn`, `ownership`, `hotspot`, `all` (default: `all`) |

### Output

```json
{
  "scope": "packages/core/",
  "window": "3 months",
  "churn_analysis": {
    "high_churn_files": [
      {"path": "auth.py", "commits": 45, "normalized_churn": 0.8}
    ]
  },
  "ownership_analysis": {
    "dispersed_ownership": [
      {"path": "auth.py", "contributors": 5, "top_owner_pct": 0.35}
    ]
  },
  "hotspot_scores": [
    {"path": "auth.py", "score": 7.2, "urgency": "high"}
  ]
}
```

---

## Delegation Model

**This skill guides analysis. File operations require Task() delegation.**

| Operation | Delegate To | Direct Action |
|-----------|-------------|---------------|
| Run git commands | `Task(source-control)` | Never |
| Read complexity metrics | `Task(tech-debt-investigator)` | Never |
| Generate reports | `Task(documentation)` | Never |


---

## Reference Documentation

- **Churn Analysis**: [reference/churn-analysis.md](reference/churn-analysis.md)
- **Ownership Metrics**: [reference/ownership.md](reference/ownership.md)
- **Hotspot Formula**: [reference/hotspot-formula.md](reference/hotspot-formula.md)

## Cross-References

- **Shared Formulas**: `../tech-debt-shared/FORMULAS-OBSERVE.md` (churn, hotspot formulas)
- **Definitions**: `../tech-debt-shared/DEFINITIONS.md`
- **Tech Debt Agent**: `.claude/agents/specialists/tech-debt-investigator/`
- **Related Skills**:
  - `scoring-sqale-methodology` - Uses hotspot data for SQALE scoring
  - `prioritizing-impact-effort` - Combines hotspot scores with effort estimates
  - `generating-debt-reports` - Assembles git metrics into reports

---

## Version History

- **v1.0.0** (2025-12-13): Initial release
  - Churn analysis with 3-month window
  - Ownership dispersion metrics
  - Hotspot score calculation
  - Defect correlation via commit message parsing

---

## Scripts

Executable scripts for automated analysis. Run via `uv run python`.

| Script | Purpose | CLI |
|--------|---------|-----|
| `scripts/git_churn.py` | Git commit history analysis | `--repo-path <path> --output-file <path> [--days <int>] [--branch <name>]` |
| `scripts/calculate_hotspots.py` | Weighted hotspot score calculation | `--complexity-file <path> --churn-file <path> --output-file <path>` |

### Usage Example

```bash
uv run python .claude/skills/analyzing-git-history/scripts/git_churn.py --repo-path /path/to/repo --output-file churn.json --days 90 --branch main

uv run python .claude/skills/analyzing-git-history/scripts/calculate_hotspots.py --complexity-file complexity.json --churn-file churn.json --output-file hotspots.json
```
