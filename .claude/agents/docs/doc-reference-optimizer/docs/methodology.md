# Documentation Optimization Methodology

**Purpose**: Detailed implementation guide for doc-reference-optimizer agent analysis procedures, formulas, and decision frameworks.

---

## Token Estimation

**Formula**: `character_count / 4` (+/-5% accuracy)

**Methodology**:
- Current tokens: Character-based estimation
- Optimized tokens: Reference overhead (~20-30 tokens) + agent-specific additions
- Savings: Difference between current and optimized
- Conservative approach: Assumes worst-case reference overhead

**Accuracy**: +/-10-20% for final savings (implementation variance)

---

## Overlap Detection

### Three-Component Algorithm

```
overlap = (jaccard x 0.4) + (structural x 0.3) + (semantic x 0.3)
```

**Jaccard Similarity**: Token-level intersection/union
**Structural Similarity**: Section organization, header patterns
**Semantic Similarity**: Meaning-level concept coverage (LLM-assessed)

### Thresholds
- **High match**: >=0.80
- **Medium match**: 0.60-0.79
- **Low match**: <0.60


---

## Confidence Scoring

### Calculation Formula

```python
def calculate_confidence(overlap, guide_coverage, clarity_preservation):
    base_confidence = overlap
    
    # Guide coverage adjustment (concept overlap %)
    if guide_coverage >= 0.95:    base_confidence += 0.05  # Complete
    elif guide_coverage >= 0.85:  base_confidence += 0.00  # Good
    elif guide_coverage >= 0.70:  base_confidence -= 0.05  # Partial
    else:                         base_confidence -= 0.10  # Insufficient
    
    # Clarity preservation (0-4 scale)
    if clarity_preservation == 4:   base_confidence += 0.05  # Perfect
    elif clarity_preservation == 3: base_confidence += 0.00  # Good
    elif clarity_preservation == 2: base_confidence -= 0.05  # Reduced
    else:                           base_confidence -= 0.10  # Unclear
    
    return min(base_confidence, 1.0)
```

### Clarity Preservation Criteria (4-point scale)
1. Terminology remains clear
2. Examples still available
3. Context preserved
4. Completeness maintained

### Confidence Thresholds
- **>=0.90**: Strong recommend
- **>=0.80**: Recommend
- **>=0.70**: Consider
- **<0.70**: Keep inline


---

## Value Score Thresholds

**Formula**: `(savings x confidence) / effort`

**Units**: Confidence-weighted tokens saved per minute of implementation effort

### Priority Levels
| Priority | Score | Interpretation |
|----------|-------|----------------|
| High | >50 | Implement immediately (>1 token/sec ROI) |
| Medium | 20-50 | Implement when available (0.3-1 token/sec) |
| Low | <20 | Defer or skip (<0.3 token/sec) |

### Example Calculations
- **High (118.75)**: reference_existing, 250 tokens, 0.95 conf, 2min effort
- **Medium (25.5)**: extend_base, 900 tokens, 0.85 conf, 30min effort
- **Low (4.2)**: create_new, 250 tokens, 0.75 conf, 45min effort

---

## Gap Detection

### Scope
- **Primary**: Target agent only (single-agent analysis)
- **Secondary**: 2-3 sampled related agents (opportunistic)
- **NOT in scope**: Full ecosystem scan (context-optimizer's role)

### Gap Identification Threshold
- Target + 2+ agents share pattern
- Total savings >=300 tokens across sampled agents
- Confidence >=0.70 that pattern is truly shared

### Sampling Strategy
- Maximum: 3-5 related agents
- Selection: Domain similarity, family membership, shared imports
- Performance: ~10-15s per sampled agent
