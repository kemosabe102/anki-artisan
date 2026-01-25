---
name: prioritizing-impact-effort
description: Create and analyze Impact/Effort matrices for prioritizing technical debt remediation. Classifies findings into P1-P4 quadrants, calculates ROI using Principal/Interest framework, and generates sprint groupings. Use when planning remediation, backlog grooming, or release planning.
---

# Prioritizing Impact/Effort

> **Impact/Effort matrix methodology for prioritizing technical debt remediation.**

---

## When to Use This Skill

**Use For**: P1-P4 quadrant classification, priority scoring, ROI calculation, sprint groupings

**NOT For**: Initial debt detection, SQALE scoring, full investigation workflow

---

## Core Methodology

### P1-P4 Quadrant Classification

| Quadrant | Impact | Effort | Action |
|----------|--------|--------|--------|
| P1 Quick Wins | High (>=6) | Low (<=4) | Do immediately |
| P2 Strategic | High (>=6) | High (>4) | Plan and resource |
| P3 Defer | Low (<6) | High (>4) | Deprioritize |
| P4 Opportunistic | Low (<6) | Low (<=4) | Boy Scout Rule |

**Assignment Logic**:
```
if impact >= 6:
    quadrant = "P1" if effort <= 4 else "P2"
else:
    quadrant = "P4" if effort <= 4 else "P3"
```

---

## Priority Score Formula

### Ranking Calculation

```
priority_score = (impact_score x 2) - effort_score
```

**Ranges**:
- impact_score: 0-10
- effort_score: 0-10
- priority_score: -10 to +20

**Tiebreaker**: Higher churn files rank first

**P1 Validation**: Effort must be <4 hours for true quick wins

---

## ROI Calculation (Principal/Interest)

### Formula

```
ROI = (interest_per_sprint x expected_sprints) / principal
```

**Definitions**:
- **Principal**: One-time remediation cost (hours)
- **Interest**: Recurring maintenance burden per sprint if unfixed (hours)
- **expected_sprints**: Planning horizon (default: 6 sprints)

**Threshold**: ROI >2.0 = high priority

**Payback Period**:
```
payback_sprints = principal / interest_per_sprint
```

---

## Sprint Grouping Rules

| Sprint | Contents | Criteria |
|--------|----------|----------|
| Sprint 1 | P1_quick_wins + urgent hotspots | hotspot_score >7.0 |
| Sprint 2 | P2_strategic | Dependencies resolved |
| Sprint 3+ | Remaining P2 + P4_opportunistic | Normal priority |
| Backlog | P3_defer | Document only, exclude from sprints |

---

## Input/Output Contract

### Input
- `impact_score`: 0-10
- `effort_score`: 0-10
- `hotspot_score`: Optional, flags urgency
- `file_path`: For churn tiebreaker lookup

### Output
- `prioritized_items[]`: finding_id, quadrant, priority_score, roi, sprint_assignment
- `sprint_summary`: Per-sprint count and total_effort

---

## References

- **Quadrant Definitions**: [reference/quadrant-classification.md](reference/quadrant-classification.md)
- **Scoring Criteria**: [reference/scoring-criteria.md](reference/scoring-criteria.md)
- **ROI Calculation**: [reference/roi-calculation.md](reference/roi-calculation.md)
- **Sprint Grouping**: [reference/sprint-grouping.md](reference/sprint-grouping.md)
- **Shared Formulas**: `../tech-debt-shared/FORMULAS-DECIDE.md` (Priority, Impact/Effort, ROI formulas)
- **Definitions**: `../tech-debt-shared/DEFINITIONS.md`
- **Related Skill**: `scoring-sqale-methodology` for SQALE grades
- **Source Agent**: `.claude/agents/specialists/tech-debt-investigator/`

---

## Scripts

Executable scripts for automated analysis. Run via `uv run python`.

| Script | Purpose | CLI |
|--------|---------|-----|
| `scripts/calculate_roi.py` | ROI and NPV calculation | `--tdr-file <path> --team-budget <float> --target-tdr <float> --output-file <path>` |
| `scripts/prioritize_items.py` | Impact/Effort prioritization | `--hotspots-file <path> --output-file <path>` |

### Usage Example

```bash
uv run python .claude/skills/prioritizing-impact-effort/scripts/calculate_roi.py --tdr-file orient_output.json --team-budget 1800000 --target-tdr 10 --output-file roi_result.json

uv run python .claude/skills/prioritizing-impact-effort/scripts/prioritize_items.py --hotspots-file hotspots.json --output-file prioritized.json
```
