---
name: generating-debt-reports
description: Generate structured technical debt reports following standardized schemas. Produces JSON output with debt scores, category ratings, matrices, and remediation plans. Supports trend analysis and stakeholder summaries. Use when finalizing tech debt analysis, creating quality gate reports, or tracking debt over time.
---

# Generating Debt Reports

Generate structured JSON reports for technical debt analysis with schema-compliant output, trend tracking, and stakeholder communication.

## When to Use This Skill

Use this skill when:
- Finalizing tech debt investigation output
- Creating quality gate reports for CI/CD
- Tracking debt metrics over time (baseline comparisons)
- Producing stakeholder-friendly summaries
- Validating report completeness before delivery

## Reference Documentation

**Detailed Guides** (read when relevant):
- **Output Schema** -> [reference/output-schema.md](reference/output-schema.md)
- **Trend Analysis** -> [reference/trend-analysis.md](reference/trend-analysis.md)
- **Stakeholder Summary** -> [reference/stakeholder-summary.md](reference/stakeholder-summary.md)

**Canonical Schema**:
- `.claude/agents/specialists/tech-debt-investigator/schemas/tech-debt-investigator.schema.json`

---

## Required Output Fields

| Field | Type | Description |
|-------|------|-------------|
| `debt_score` | number (0-100) | Composite score: Code Quality (40%) + Testing (20%) + Architecture (15%) + Docs (10%) + Infrastructure (10%) + Design (5%) |
| `debt_classification` | enum | Low (81-100), Moderate (61-80), High (41-60), Severe (0-40) |
| `category_ratings` | object | 6 categories with score (0-5), evidence array, remediation_hours |
| `quantitative_metrics` | object | complexity, duplication, coverage measurements |
| `impact_effort_matrix` | array | All findings with quadrant assignments (P1-P4) |
| `remediation_plan` | array | Prioritized actions with effort estimates and acceptance criteria |

## Optional Fields

| Field | When to Include | Purpose |
|-------|-----------------|---------|
| `tdr_ratio` | Always recommended | SQALE Technical Debt Ratio |
| `sqale_grade` | Always recommended | A-E maintainability grade |
| `historical_metrics` | Git analysis done | Churn, ownership, defect density |
| `hotspots` | Git analysis done | Files with high churn + complexity |
| `trend_analysis` | Baseline provided | Delta comparisons, regression detection |
| `stakeholder_summary` | Executive reporting | Plain-language health assessment |

---

## Input/Output Contract

**Input**: Scored data from tech debt investigation phases 1-3
- Category assessments with evidence
- Quantitative metrics
- Impact/effort quadrant assignments
- Sprint groupings and dependencies

**Output**: Schema-compliant JSON per `tech-debt-investigator.schema.json`
- All required fields populated
- Evidence arrays with `{path}:{line}` format
- Measurable acceptance criteria in remediation plan
- Trend analysis if baseline available

---

## Quick Checklist

Before marking report complete:

- [ ] All required JSON fields populated
- [ ] Evidence arrays contain `{path}:{line}` format strings
- [ ] Remediation plan has measurable acceptance criteria
- [ ] Trend analysis included if baseline provided
- [ ] Urgent hotspots (>7.0) prominently flagged
- [ ] Stakeholder summary uses plain language (if included)

---

## References

- **Shared Formulas**: `../tech-debt-shared/FORMULAS-ACT.md` (Output formatting formulas)
- **Definitions**: `../tech-debt-shared/DEFINITIONS.md`

## Related Skills

- `tech-debt-investigator` agent - Full investigation workflow
- `code-review-standards` - Code quality assessment patterns
- `reviewing-architecture` - Architecture debt analysis

---

## Scripts

Executable scripts for automated analysis. Run via `uv run python`.

| Script | Purpose | CLI |
|--------|---------|-----|
| `scripts/generate_report.py` | Final report aggregation | `--input-dir <path> --output-file <path> --repo-name <name> [--markdown]` |

### Usage Example

```bash
uv run python .claude/skills/generating-debt-reports/scripts/generate_report.py --input-dir ./analysis --output-file report.json --repo-name myproject

uv run python .claude/skills/generating-debt-reports/scripts/generate_report.py --input-dir ./analysis --output-file report.json --repo-name myproject --markdown
```
