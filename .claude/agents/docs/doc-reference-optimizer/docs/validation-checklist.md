# Validation Checklist

**Purpose**: Quality gates for doc-reference-optimizer analysis and output.

**Extends**: `base-agent-pattern.md` (Validation Checklist)

---

## Pre-Analysis Validation

- [ ] Agent file readable and parseable (valid markdown structure)
- [ ] Frontmatter contains name field for identification
- [ ] Agent size >3,000 tokens (optimization threshold)

---

## Analysis Quality Validation

- [ ] Token calculations use character-based methodology (chars/4 formula)
- [ ] Overlap percentages >80% for `reference_existing` recommendations
- [ ] Confidence scores include `guide_coverage` and `clarity_preservation` factors
- [ ] All optimization opportunities include `savings_metadata` with accuracy ranges

---

## Recommendation Validation

- [ ] Value scores calculated: `(savings x confidence) / effort`
- [ ] Strategies prioritized by value score (>50 = High, 20-50 = Medium, <20 = Low)
- [ ] Essential workflows marked for inline retention (not externalized)
- [ ] Specific file:line references provided for all recommendations


---

## Output Quality Validation

- [ ] `agent_specific_output` includes all required fields:
  - analysis_summary
  - optimization_opportunities
  - documentation_gaps
  - agent_specific_content
- [ ] SUCCESS status with complete `savings_metadata`
- [ ] OR FAILURE status with recovery suggestions and partial results
- [ ] Confidence score >=0.70 for final report (or marked as low-confidence)

---

## Documentation Gap Validation (if performed)

- [ ] Sampling limited to 2-3 related agents (not ecosystem-wide scan)
- [ ] Gap descriptions specify affected agents count
- [ ] Estimated savings include confidence ranges (+/-10%)
- [ ] Recommended path follows existing documentation structure

---

## Final Output Check

- [ ] JSON structure valid per schema
- [ ] All required meta-flags present (status, agent, confidence, execution_timestamp)
- [ ] Summary accurately reflects analysis findings
- [ ] No sensitive information in output
