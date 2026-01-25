# Overlap Detection Algorithm

**Purpose**: 3-component algorithm for calculating content overlap between agent sections and documentation.

---

## Overview

**Formula**:
```
overlap_score = (jaccard × 0.4) + (structural × 0.3) + (semantic × 0.3)
```

**Output**: Score in range [0.0, 1.0] representing content overlap percentage

**Thresholds**:
- **High**: >=0.80 (reference_existing candidate)
- **Medium**: 0.60-0.79 (extend_base candidate)
- **Low**: <0.60 (keep_inline or create_new)

---

## Component 1: Jaccard Similarity (40% weight)

**Purpose**: Measure literal word-level overlap

**Algorithm**:
1. Tokenize both texts:
   - Convert to lowercase
   - Remove punctuation
   - Split on whitespace
   - Create word sets
2. Calculate intersection: Words present in both texts
3. Calculate union: All unique words across both texts
4. Score: `|intersection| / |union|`

**Example**:
```
Section words: {agent, workflow, phase, observe, orient, decide, act, error}
Doc words: {workflow, phase, observe, orient, decide, act, process, step}

Intersection: {workflow, phase, observe, orient, decide, act} = 6 words
Union: {agent, workflow, phase, observe, orient, decide, act, error, process, step} = 10 words
Jaccard: 6 / 10 = 0.60
```

**Why 40% weight**: Captures direct content reuse, most reliable indicator


---

## Component 2: Structural Similarity (30% weight)

**Purpose**: Measure organizational pattern alignment

**Elements Compared**:
1. **Header hierarchy**: H1, H2, H3 structure
2. **List patterns**: Bullet points, numbered lists, checklists
3. **Table presence**: Column count, row patterns
4. **Code blocks**: Presence and formatting
5. **Section order**: Sequential pattern matching

**Scoring**:
```
structural_score = matched_elements / total_elements
```

**Example**:
```
Section structure:
- H2: Phase Workflow
- Bulleted list (4 items)
- Table (3 columns, 5 rows)
- Code block

Doc structure:
- H2: Workflow Phases
- Bulleted list (4 items)
- Table (3 columns, 8 rows)
- No code block

Matched: 3 / 4 = 0.75
```

**Why 30% weight**: Format alignment indicates reference suitability

---

## Component 3: Semantic Similarity (30% weight)

**Purpose**: Measure concept-level alignment beyond literal words

**Concept Categories**:
1. **Domain entities**: Agent names, tool names, component names
2. **Action patterns**: Workflow verbs, process descriptions
3. **Decision criteria**: Thresholds, conditions, rules
4. **Examples**: Use cases, scenarios, code samples


**Assessment Method** (LLM-based):
```
For each concept category:
1. Extract concepts from section
2. Extract concepts from doc
3. Calculate concept coverage: matched_concepts / section_concepts
4. Average across categories
```

**Example**:
```
Section concepts:
- Domain: [orchestrator, researcher, development]
- Actions: [delegate, analyze, verify]
- Criteria: [CQ>=0.85, ASC>=0.80]

Doc concepts:
- Domain: [orchestrator, agent, specialist]
- Actions: [delegate, coordinate, spawn]
- Criteria: [CQ>=0.85, confidence threshold]

Coverage:
- Domain: 1/3 matched (orchestrator) = 0.33
- Actions: 1/3 matched (delegate) = 0.33
- Criteria: 1/2 matched (CQ>=0.85) = 0.50
Average: (0.33 + 0.33 + 0.50) / 3 = 0.39
```

**Why 30% weight**: Captures meaning-level overlap, prevents false positives from word matching alone

---

## Combined Calculation

**Example - High Overlap**:
```
Jaccard: 0.85 (high word overlap)
Structural: 0.90 (similar organization)
Semantic: 0.80 (aligned concepts)

Overlap = (0.85 × 0.4) + (0.90 × 0.3) + (0.80 × 0.3)
        = 0.34 + 0.27 + 0.24
        = 0.85 (HIGH - reference_existing candidate)
```

**Example - Medium Overlap**:
```
Jaccard: 0.70 (moderate word overlap)
Structural: 0.60 (some format differences)
Semantic: 0.65 (partial concept coverage)

Overlap = (0.70 × 0.4) + (0.60 × 0.3) + (0.65 × 0.3)
        = 0.28 + 0.18 + 0.195
        = 0.655 ≈ 0.66 (MEDIUM - extend_base candidate)
```


**Example - Low Overlap**:
```
Jaccard: 0.40 (low word overlap)
Structural: 0.30 (different formats)
Semantic: 0.35 (minimal concept alignment)

Overlap = (0.40 × 0.4) + (0.30 × 0.3) + (0.35 × 0.3)
        = 0.16 + 0.09 + 0.105
        = 0.355 ≈ 0.36 (LOW - keep_inline or create_new)
```

---

## Implementation Notes

**Performance Optimization**:
- Cache tokenized word sets for reuse
- Limit semantic analysis to top 20 concepts per category
- Skip structural comparison if Jaccard <0.30 (optimization)

**Edge Cases**:
- Empty sections: Return 0.0 overlap
- Missing documentation: Return 0.0 overlap
- Identical content: Return 1.0 overlap

**Validation**:
Test against known pairs:
- Duplicate content → expect ≥0.95
- Completely unrelated → expect ≤0.20
- Partial match (60-70% shared) → expect 0.60-0.75

---

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Word matching only | False positives | Use all 3 components |
| Ignoring structure | Reference format mismatches | Check header/list alignment |
| Skipping semantic analysis | Misses concept-level reuse | Extract domain concepts |
| Equal weights | Overvalues less reliable signals | Use 40/30/30 weighting |

---

## Threshold Justification

**>=0.80 (High)**: Sufficient overlap for direct reference replacement
- Jaccard typically >=0.75
- Structural alignment strong
- Concept coverage >=85%

**0.60-0.79 (Medium)**: Partial overlap, needs extension strategy
- Jaccard typically 0.55-0.75
- Some structural differences
- Concept coverage 60-80%

**<0.60 (Low)**: Insufficient overlap for reference
- Jaccard typically <0.55
- Format may differ significantly
- Concept coverage <60%
