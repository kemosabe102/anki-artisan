# Phase 4: ACT - Output Generation

**OODA Stage**: ACT | **Time Allocation**: 50-55%

**Purpose**: Generate structured JSON output, remediation roadmap, trend analysis

**Deliverable**: Complete analysis report per schema specification

---

## Workflow Steps

### Step 4.1: JSON Output Generation

**Input**: All scored data from Phases 1-3

**Process**:
1. Assemble required fields per `schemas/tech-debt-investigator.schema.json`:
   - `debt_score` (0-100)
   - `debt_classification` (Low/Moderate/High/Severe)
   - `category_ratings` (6 categories with scores, evidence, hours)
   - `quantitative_metrics` (complexity, duplication, coverage)
   - `impact_effort_matrix` (all findings with quadrants)
   - `remediation_plan` (prioritized actions)
2. Include optional fields when relevant:
   - `tdr_ratio`, `sqale_grade` (always recommended)
   - `historical_metrics`, `hotspots` (when git analysis done)
   - `trend_analysis` (when baseline provided)

**Output**: Schema-compliant JSON structure

### Step 4.2: Remediation Roadmap

**Input**: Sprint groupings, dependency graph

**Process**:
1. For each sprint, create remediation entries:
   - `priority_order`: 1, 2, 3...
   - `debt_item_ids`: references to matrix items
   - `action`: specific remediation description
   - `estimated_effort_hours`: sum of item efforts
   - `acceptance_criteria`: testable completion checks
2. Include quick-win items first
3. Ensure acceptance criteria are measurable

**Output**: `remediation_plan` array with actionable steps

### Step 4.3: Trend Analysis (Iterative Mode)

**Input**: Current scores, baseline scores (if provided)

**Process**:
1. Calculate delta for each metric:
   - `debt_score` change (+/- points)
   - `tdr_ratio` change
   - Per-category score changes
2. Identify regressions (metrics getting worse)
3. Flag improvements and their causes
4. Project trend direction

**Output**: `trend_analysis` object with deltas and projections

### Step 4.3.5: Trend Confidence Assessment

**Input**: Current scores, baseline scores, baseline metadata

**Process**:
1. Calculate confidence factors:
   - `baseline_recency`: Recent (<7 days) = 1.0, Moderate (7-30 days) = 0.8, Old (>30 days) = 0.5
   - `sample_size`: ≥20 findings = 1.0, 10-19 = 0.8, <10 = 0.5
   - `delta_magnitude`: |delta| > 10% = 1.0, 5-10% = 0.7, <5% = 0.4

2. Calculate trend confidence:
   ```
   confidence = baseline_recency × sample_size × delta_magnitude
   ```

3. Apply alert thresholds:

   | Confidence | Delta Direction | Alert Level |
   |------------|-----------------|-------------|
   | ≥0.7 | Worsening | **ALERT** - Regression confirmed |
   | 0.4-0.7 | Worsening | **WARNING** - Possible regression |
   | <0.4 | Any | **INFO** - Insufficient confidence |
   | ≥0.7 | Improving | **SUCCESS** - Improvement confirmed |

4. Add interpretation to output:
   ```json
   {
     "trend_analysis": {
       "confidence": 0.85,
       "alert_level": "ALERT",
       "interpretation": "Regression confirmed (85% confidence). TDR increased 8% since last sprint."
     }
   }
   ```

**Output**: `trend_analysis` with confidence score and calibrated alerts

### Step 4.4: Urgent Hotspot Flagging

**Input**: Hotspot scores from Phase 2

**Process**:
1. Extract all items with hotspot score >7.0
2. Add prominent warning flags
3. Include in executive summary
4. Recommend immediate attention

**Output**: Urgent hotspot section with visibility flags

### Step 4.5: Report Persistence (Optional)

**Input**: Complete analysis output

**Process**:
1. Write JSON to `temp/tech-debt-investigator/{timestamp}.json`
2. Update baseline reference for future comparisons
3. Document analysis coverage and limitations

**Output**: Persisted report for iterative mode baseline

---

## Quick Checklist

Before marking complete:

- [ ] All required JSON fields populated
- [ ] Evidence arrays contain `{path}:{line}` format strings
- [ ] Remediation plan has measurable acceptance criteria
- [ ] Trend analysis included if baseline provided
- [ ] Urgent hotspots (>7.0) prominently flagged

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing required fields | Validate against schema before output |
| Vague acceptance criteria | Make all criteria testable/measurable |
| No evidence references | Every finding needs file:line location |
| Skipping trend analysis | Always calculate if baseline available |

---

## Exit Criteria

**All criteria must pass to complete**

| Criterion | Weight | Check |
|-----------|--------|-------|
| Schema compliance | 0.30 | All required fields present |
| Evidence complete | 0.25 | All findings have file:line refs |
| Plan actionable | 0.25 | Acceptance criteria measurable |
| Hotspots flagged | 0.10 | >7.0 items prominently marked |
| Report ready | 0.10 | JSON output valid and complete |

---

**Previous Phase**: [Phase 3: DECIDE](phase-3-decide.md)
**Complete**: Return to [tech-debt-investigator.md](../tech-debt-investigator.md)
