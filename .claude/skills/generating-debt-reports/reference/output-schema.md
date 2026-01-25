# Output Schema Reference

Complete field specifications for technical debt report JSON output.

**Canonical Schema**: `.claude/agents/specialists/tech-debt-investigator/schemas/tech-debt-investigator.schema.json`

---

## Required Fields

### debt_score

| Property | Value |
|----------|-------|
| Type | number |
| Range | 0-100 |
| Meaning | 0 = severe debt, 100 = excellent health |

**Composite Formula**:
```
debt_score = Sum(category_weight x category_score)

Category Weights:
- Code Quality: 40%
- Testing: 20%
- Architecture: 15%
- Documentation: 10%
- Infrastructure: 10%
- Design/UI: 5%
```

---

### debt_classification

| Classification | Score Range | Interpretation |
|----------------|-------------|----------------|
| Low | 81-100 | Minimal debt, healthy codebase |
| Moderate | 61-80 | Manageable debt, monitor closely |
| High | 41-60 | Significant debt, plan remediation |
| Severe | 0-40 | Critical debt, immediate action |

---

### category_ratings

Object with 6 categories. Each category requires:

| Field | Type | Description |
|-------|------|-------------|
| `score` | number (0-5) | SIG star rating |
| `evidence` | array[string] | File:line references |
| `remediation_hours` | number | Hours to fix all issues |

**Required Categories**:
- `code_quality` - Complexity, duplication, violations
- `architecture` - Coupling, cohesion, dependencies
- `testing` - Coverage, flakiness, missing tests
- `documentation` - Missing docs, outdated READMEs
- `infrastructure` - Deprecated APIs, outdated deps

**Optional Category**:
- `design_ui` - UX patterns, accessibility

**Star Rating Scale** (SIG-inspired):
| Stars | Percentile | Interpretation |
|-------|------------|----------------|
| 5 | Top 5% | Exceptional |
| 4 | Top 30% | Above average |
| 3 | Average | Industry median |
| 2 | Below 30% | Below average |
| 1 | Bottom 5% | Critical |

---

### quantitative_metrics

Required sub-objects:

**cyclomatic_complexity**:
| Field | Type | Description |
|-------|------|-------------|
| `average` | number | Average across all functions |
| `max` | number | Highest complexity function |
| `high_complexity_count` | integer | Functions with complexity >10 |
| `critical_complexity_count` | integer | Functions with complexity >20 (optional) |

**code_duplication**:
| Field | Type | Description |
|-------|------|-------------|
| `percentage` | number (0-100) | % duplicated lines (target: <5%) |
| `duplicate_block_count` | integer | Number of duplicate blocks |
| `largest_duplicate_loc` | integer | Lines in largest block (optional) |

**test_coverage**:
| Field | Type | Description |
|-------|------|-------------|
| `line_coverage_pct` | number (0-100) | % lines covered (target: >80%) |
| `function_coverage_pct` | number (0-100) | % functions with tests |
| `untested_critical_paths` | array[string] | Critical modules without tests (optional) |

---

### impact_effort_matrix

Array of debt items with quadrant classification.

**Required Fields per Item**:
| Field | Type | Description |
|-------|------|-------------|
| `debt_item_id` | string | Unique identifier |
| `description` | string | Brief issue description |
| `category` | enum | One of 6 debt categories |
| `impact_score` | number (0-10) | Business/technical impact |
| `effort_score` | number (0-10) | Remediation effort |
| `priority_quadrant` | enum | P1_quick_wins, P2_strategic, P3_defer, P4_opportunistic |
| `principal_cost_hours` | number | Hours to fix now |

**Optional Fields**:
| Field | Type | Description |
|-------|------|-------------|
| `interest_cost_per_sprint` | number | Ongoing cost if unfixed |
| `is_hotspot` | boolean | True if high churn + complexity |
| `evidence` | array[string] | File:line references |

**Quadrant Logic**:
| Quadrant | Impact | Effort | Action |
|----------|--------|--------|--------|
| P1_quick_wins | High (>6) | Low (<4) | Do immediately |
| P2_strategic | High (>6) | High (>6) | Plan and resource |
| P3_defer | Low (<4) | High (>6) | Deprioritize |
| P4_opportunistic | Low (<4) | Low (<4) | Boy Scout Rule |

---

### remediation_plan

Array of prioritized remediation actions.

**Required Fields per Action**:
| Field | Type | Description |
|-------|------|-------------|
| `priority_order` | integer | Execution order (1 = highest) |
| `debt_item_ids` | array[string] | References to matrix items |
| `action` | string | Specific remediation description |
| `estimated_effort_hours` | number | Total effort for action |
| `acceptance_criteria` | array[string] | Testable completion checks |

**Optional Fields**:
| Field | Type | Description |
|-------|------|-------------|
| `expected_debt_score_improvement` | number | Predicted score increase |

**Acceptance Criteria Examples**:
- "Complexity <10 for all functions in module"
- "Test coverage >80% for payment service"
- "Zero critical CVEs in dependencies"
- "All public APIs have docstrings"

---

## Optional Fields

### tdr_ratio

Technical Debt Ratio per SQALE methodology.

```
TDR = remediation_cost / development_cost
```

| Range | SQALE Grade | Interpretation |
|-------|-------------|----------------|
| <5% | A | Excellent |
| 5-10% | B | Good |
| 10-20% | C | Fair |
| 20-50% | D | Poor |
| >50% | E | Critical |

---

### historical_metrics

Git-based behavioral analysis (requires repository access).

**code_churn**: High-frequency change files
**ownership_dispersion**: Files with fragmented ownership
**defect_density**: Bug concentration metrics

---

### hotspots

Array of critical files: high churn + high complexity + high defects.

| Field | Type | Description |
|-------|------|-------------|
| `file_path` | string | Path to hotspot file |
| `hotspot_score` | number (0-10) | Composite score |
| `priority` | enum | P1-P4 assignment |

**Hotspot Score Formula**:
```
hotspot_score = churn x complexity x defects x business_criticality
Threshold: >7.0 = urgent attention required
```

---

## Evidence Format

All evidence arrays must use `{path}:{line}` format:

```json
"evidence": [
  "packages/core/auth.py:45",
  "packages/core/auth.py:89",
  "packages/utils/helpers.py:23"
]
```

This enables direct navigation to findings in IDE/editor.
