# Phase 4: ACT - Report Generation & Output

**OODA Stage**: ACT | **Time Allocation**: 30-35%

**Purpose**: Generate structured optimization report, format recommendations, validate output against schema

**Deliverable**: Complete optimization report in JSON format per schema specification

---

## Workflow Steps

### Step 4.1: Analysis Summary Generation

**Input**: All phase outputs (baseline, overlaps, strategies, scores)

**Process**:
1. Compile summary statistics:
   - `current_token_count`: Total baseline tokens
   - `optimized_token_count`: Projected after all optimizations
   - `potential_savings`: Sum of all recommended savings
   - `compression_ratio`: `(savings / current) * 100%`
   - `sections_analyzed`: Count of sections processed

**Output**: `analysis_summary` object

### Step 4.2: Opportunity Formatting

**Input**: Prioritized opportunities from Phase 3


**Process**:
1. Format each opportunity per schema:
   - `section`: Section name
   - `current_location`: File path with line numbers
   - `current_tokens`: Pre-optimization count
   - `optimization_strategy`: Selected strategy
   - `documentation_match`: Path, section, overlap details
   - `optimized_tokens`: Post-optimization estimate
   - `savings`: Token reduction
   - `savings_metadata`: Type, accuracy, methodology, conservative flag
   - `confidence`: Score from Phase 3
   - `recommendation`: Actionable text

**Output**: `optimization_opportunities` array sorted by value score DESC

### Step 4.3: Gap Documentation

**Input**: Identified documentation gaps from Phase 2

**Process**:
1. Format gap entries:
   - `gap_description`: What's missing
   - `content_pattern`: Pattern that should be documented
   - `affected_agents`: List of agents sharing pattern
   - `total_savings`: Potential ecosystem-wide savings
   - `suggested_doc_path`: Recommended new doc location
   - `confidence`: Gap identification confidence

**Output**: `documentation_gaps` array (may be empty)


### Step 4.4: Keep-Inline Documentation

**Input**: Sections with `keep_inline` strategy

**Process**:
1. Document retention rationale:
   - `section`: Section name
   - `tokens`: Current token count
   - `keep_reason`: Why inline retention is recommended

**Output**: `agent_specific_content` array

### Step 4.5: Output Validation

**Input**: Complete report structure

**Process**:
1. Validate against `schemas/doc-reference-optimizer.schema.json`
2. Check required fields present
3. Verify data types and enums
4. Ensure confidence values in [0, 1] range

**Output**: Validated JSON report or validation warnings

### Step 4.6: Report Writing (Optional)

**Input**: Validated report, orchestrator request

**Process**:
1. If report writing requested:
   - Write to `.claude/docs/reports/doc-optimization/{agent_name}-{timestamp}.json`
2. Return report in response

**Output**: Written report path (if applicable) + JSON response


---

## Output Format

**Success Response Structure**:
```json
{
  "status": "SUCCESS",
  "agent": "doc-reference-optimizer",
  "confidence": 0.85,
  "execution_timestamp": "2024-01-15T10:30:00Z",
  "agent_specific_output": {
    "analysis_summary": { ... },
    "optimization_opportunities": [ ... ],
    "documentation_gaps": [ ... ],
    "agent_specific_content": [ ... ]
  }
}
```

**No Opportunities Response**:
```json
{
  "status": "SUCCESS",
  "agent_specific_output": {
    "analysis_summary": { "potential_savings": 0 },
    "optimization_opportunities": []
  },
  "summary": "All sections optimized or agent-specific"
}
```

---

## Quick Checklist

Before returning results:

- [ ] Analysis summary complete with all metrics
- [ ] Opportunities formatted per schema
- [ ] Gaps documented (if any)
- [ ] Keep-inline sections justified
- [ ] Output validated against schema
- [ ] Report written (if requested)

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing savings_metadata | Always include methodology and accuracy |
| Full paths in doc references | Use filename-only for portability |
| Skipping validation | Always validate before returning |
| Unsorted opportunities | Sort by value score DESC |

---

## Exit Criteria

**All criteria must pass to complete**

| Criterion | Weight | Check |
|-----------|--------|-------|
| Summary complete | 0.25 | All metrics calculated |
| Opportunities formatted | 0.30 | Schema-compliant entries |
| Validation passed | 0.25 | No schema errors |
| Response structured | 0.20 | SUCCESS/FAILURE with required fields |

---

**Previous Phase**: [Phase 3: DECIDE](phase-3-decide.md)
**Complete**: Return to [doc-reference-optimizer.md](../doc-reference-optimizer.md)
