---
name: scoring-sqale-methodology
description: Apply SQALE methodology for technical debt scoring. Calculates Technical Debt Ratio (TDR), assigns grades A-E, applies 6-category weighted taxonomy, and produces SIG star ratings. Use when scoring tech debt, quality gates, or comparing codebases.
---

# SQALE Methodology for Technical Debt Scoring

> **Industry-standard framework for quantifying and grading technical debt.**

---

## When to Use This Skill

**Trigger Keywords**: "tech debt score", "TDR", "SQALE grade", "debt ratio", "quality gate", "SIG rating", "maintainability score"

**Use For**:
- Calculating Technical Debt Ratio (TDR) percentages
- Assigning SQALE grades (A-E) to codebases or components
- Applying 6-category weighted taxonomy for composite scoring
- Generating SIG star ratings for maintainability benchmarking
- Quality gate decisions (pass/fail thresholds)

**NOT For**:
- Finding debt items (use `tech-debt-investigator` agent)
- Prioritizing remediation (use `prioritizing-impact-effort` skill)
- Git history analysis (use `analyzing-git-history` skill)

---

## Methodology Overview

### SQALE (Software Quality Assessment based on Lifecycle Expectations)

SQALE provides a standardized method to measure technical debt as a ratio of remediation cost to development cost. Originally developed by DNV GL, it focuses on the economics of quality.

**Key Concept**: Technical debt is the gap between the current state and an ideal state, measured in remediation effort.

### SIG Maintainability Model (Software Improvement Group)

SIG provides percentile-based star ratings (1-5) by benchmarking against industry data. Unlike SQALE's ratio-based approach, SIG ranks codebases against peers.

**Key Difference**: SQALE measures absolute debt ratio; SIG measures relative maintainability.

---

## Quick Reference: TDR to Grade Mapping

| Grade | TDR Range | Interpretation | Action Required |
|-------|-----------|----------------|-----------------|
| **A** | <5% | Excellent | Maintain current practices |
| **B** | 5-10% | Good | Monitor, minor fixes |
| **C** | 10-20% | Fair | Plan remediation sprint |
| **D** | 20-50% | Poor | Prioritize debt reduction |
| **E** | >50% | Critical | Emergency intervention |

---

## Category Weights (6-Category Taxonomy)

| Category | Weight | Focus Areas |
|----------|--------|-------------|
| Code Quality | 40% | Complexity, duplication, violations |
| Testing | 20% | Coverage, flakiness, missing tests |
| Architecture | 15% | Coupling, cohesion, dependencies |
| Documentation | 10% | Missing docs, outdated READMEs |
| Infrastructure | 10% | Deprecated APIs, outdated deps |
| Design | 5% | UX patterns, accessibility |

**Composite Formula**: `debt_score = SUM(category_weight x category_score)`

---

## Input/Output Contract

### Required Inputs

| Input | Type | Source |
|-------|------|--------|
| remediation_cost | hours | Issue analysis or estimation |
| development_cost | hours | LOC/10 (industry standard) |
| category_scores | 0-100 each | Per-category analysis |

### Outputs

| Output | Type | Description |
|--------|------|-------------|
| TDR | percentage | Technical Debt Ratio |
| sqale_grade | A-E | SQALE quality grade |
| debt_score | 0-100 | Weighted composite score |
| sig_stars | 1-5 | SIG maintainability rating |

---

## Scoring Workflow

### Step 1: Calculate TDR
```
TDR = (remediation_cost / development_cost) x 100
```

### Step 2: Assign SQALE Grade
Map TDR percentage to A-E grade using threshold table.

### Step 3: Calculate Composite Debt Score
Apply 6-category weights to individual category scores.

### Step 4: Determine SIG Rating (Optional)
Benchmark against low-risk thresholds for star assignment.

---

## References

- **TDR Calculation Details**: [reference/tdr-calculation.md](reference/tdr-calculation.md)
- **Category Taxonomy**: [reference/category-taxonomy.md](reference/category-taxonomy.md)
- **SIG Rating Model**: [reference/sig-rating.md](reference/sig-rating.md)
- **Shared Formulas**: `../tech-debt-shared/FORMULAS-ORIENT.md` (Hotspot, TDR, SIG, composite formulas)
- **Definitions**: `../tech-debt-shared/DEFINITIONS.md`
- **Source Agent**: `.claude/agents/specialists/tech-debt-investigator/`

---

## Scripts

Executable scripts for automated analysis. Run via `uv run python`.

| Script | Purpose | CLI |
|--------|---------|-----|
| `scripts/calculate_tdr.py` | Technical Debt Ratio calculation | `--loc <int> --output-file <path> [--complexity-file <path>] [--duplication-file <path>] [--coverage-file <path>]` |
| `scripts/calculate_sig.py` | SIG Star Rating conversion | `--tdr-file <path> --output-file <path>` |

### Usage Example

```bash
uv run python .claude/skills/scoring-sqale-methodology/scripts/calculate_tdr.py --complexity-file complexity.json --duplication-file duplication.json --loc 10000 --output-file tdr_results.json

uv run python .claude/skills/scoring-sqale-methodology/scripts/calculate_sig.py --tdr-file tdr_results.json --output-file sig_rating.json
```
