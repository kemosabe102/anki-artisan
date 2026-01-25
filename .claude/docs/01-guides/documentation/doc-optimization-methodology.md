# Documentation Optimization Methodology

**Purpose**: Detailed implementation guide for documentation agent analysis procedures, formulas, and decision frameworks.

**Audience**: Sub-agents implementing documentation logic, developers debugging optimization issues, users understanding recommendation rationale.

---

## Section Handling Protocol

### Section Name Normalization (Fuzzy Matching)

**Purpose**: Robust section identification despite minor variations in agent markdown.

**Rules**:

- **Case-insensitive matching**: "knowledge base" = "Knowledge Base"
- **Whitespace normalized**: "Pre-Flight" = "Pre- Flight"
- **Levenshtein distance ≤2** for standard section names (typo tolerance)
- **Example**: "Knowlege Base" (typo) still matches "Knowledge Base"

### Handling Missing Sections

**Agent lacks section** → Skip, note in report ("Section not found")

- **All 6 standard sections present** → Flag as "template compliant"
- **Missing >2 standard sections** → Flag as "non-standard structure"
- **Report structural compliance** in analysis_summary

### Agent-Specific Section Detection

**Any ## section not matching standard 6** → Classified as agent-specific

- Still analyzed for patterns and optimization opportunities
- Default categorization: "keep_inline" (unique capability)

### Malformed Markdown Handling

**Missing header levels** → Capture content until next ##
**Mixed header symbols (#, \*, -)** → Normalize to #
**No headers found** → Treat entire file as one section
**Report parsing warnings** in analysis notes

---

## Token Savings Calculations

### ALL SAVINGS ARE ESTIMATES, NOT GUARANTEES

Token savings calculations use conservative methodology with **±10-20% accuracy**. Actual savings may vary based on:

- Implementation approach (how reference is written)
- Agent-specific overrides added
- Reference overhead (link text length)
- Validation by claude-code-ecosystem during implementation

### Calculation Methodology

**Current tokens**: Character-based estimation (÷4)
**Optimized tokens**: Reference overhead (~20-30 tokens) + agent-specific additions
**Savings**: Difference between current and optimized
**Conservative approach**: Assumes worst-case reference overhead, typical override length

---

## Value Score Thresholds

### Threshold Rationale

**>50**: High ROI, implement immediately (saves >1 token per second of work)
**20-50**: Moderate ROI, implement when time available (saves 0.3-1 token/sec)
**<20**: Low ROI, defer or skip unless strategic value (saves <0.3 token/sec)

### Units Definition

**Value Score Units**: Confidence-weighted tokens saved per minute of implementation effort

**Formula**:

```python
value_score = (savings × confidence) / effort
```

### Example Calculations

- **High Priority** (>50): reference_existing with 250 tokens, confidence 0.95, 2min effort = (250 × 0.95) / 2 = **118.75**
- **Medium Priority** (20-50): extend_base with 900 tokens, confidence 0.85, 30min effort = (900 × 0.85) / 30 = **25.5**
- **Low Priority** (<20): create_new with 250 tokens, confidence 0.75, 45min effort = (250 × 0.75) / 45 = **4.2**

---

## Overlap Detection

### Semantic Similarity (Meaning-Level, Agent-Performed)

**Purpose**: Agent analysis using LLM reasoning (automated, no human review required).

**Algorithm**:

```python
def semantic_similarity(section_a, section_b):
    # Agent analysis using LLM reasoning (automated, no human review):
    # Step 1: Extract concepts (technical terms, patterns, domain concepts)
    # Step 2: Calculate coverage (guide_concepts ∩ agent_concepts / agent_concepts)
    # Step 3: Test clarity preservation (would reference maintain readability?)
    # Step 4: Check example equivalence (guide demonstrates same patterns?)
    return 0.0-1.0  # Agent's automated judgment
```

**Implementation Notes**:

- **Step 1**: Use LLM to extract key concepts from both agent section and guide section
- **Step 2**: Calculate set intersection and divide by agent concepts (coverage percentage)
- **Step 3**: Agent evaluates if replacing content with reference maintains understanding
- **Step 4**: Agent checks if guide provides equivalent examples and illustrations

**No External Systems**: Agent performs all semantic analysis using built-in LLM reasoning capabilities.

---

## Confidence Scoring

### All Assessments Performed by Agent

The agent autonomously evaluates `guide_coverage` and `clarity_preservation` using its LLM reasoning capabilities (**no external systems or human judgment required**).

### Confidence Calculation

```python
def calculate_confidence(overlap, guide_coverage, clarity_preservation, agent_count):
    base_confidence = overlap

    # Adjust for guide coverage (agent calculates concept overlap %)
    # Agent compares: guide_concepts ∩ agent_concepts / agent_concepts
    if guide_coverage >= 0.95:  # Complete (≥95% concept coverage)
        base_confidence += 0.05
    elif guide_coverage >= 0.85:  # Good (85-94%)
        base_confidence += 0.00  # No adjustment
    elif guide_coverage >= 0.70:  # Partial (70-84%)
        base_confidence -= 0.05
    else:  # Insufficient (<70%)
        base_confidence -= 0.10

    # Adjust for clarity preservation (agent evaluates readability)
    # Agent assesses 4 criteria: terminology, examples, context, completeness
    if clarity_preservation == 4:  # Perfect (all 4 criteria met)
        base_confidence += 0.05
    elif clarity_preservation == 3:  # Good (3 of 4)
        base_confidence += 0.00  # No adjustment
    elif clarity_preservation == 2:  # Reduced (2 of 4)
        base_confidence -= 0.05
    else:  # Unclear (<2 of 4)
        base_confidence -= 0.10

    # Adjust for ecosystem pattern (3+ agents)
    if agent_count >= 3:
        base_confidence += 0.05

    return min(base_confidence, 1.0)
```

### Input Definitions (Agent-Calculated)

#### guide_coverage (0.0-1.0)

**Definition**: Percentage of agent concepts covered by guide

**Agent Calculation**:

- Agent extracts concepts from both texts using LLM reasoning
- Calculates: (shared concepts) / (total agent concepts)
- **Example**: Agent needs [auth, validation, error handling], guide covers [auth, validation] → 0.67 coverage

#### clarity_preservation (0-4 scale)

**Definition**: Readability assessment if reference replaces content

**Agent Evaluation**: 4 criteria using LLM judgment:

1. **Terminology remains clear** (technical terms not lost)
2. **Examples still available** (guide provides equivalent illustrations)
3. **Context preserved** (reader understands without original text)
4. **Completeness maintained** (no critical nuances lost)

**Example**: If all 4 true → score 4 (perfect), if 2 true → score 2 (reduced)

### Confidence Thresholds

- **≥ 0.90**: Strong recommend (high match, clear benefit)
- **≥ 0.80**: Recommend (good match, likely beneficial)
- **≥ 0.70**: Consider (acceptable match, review needed)
- **< 0.70**: Keep inline (insufficient match, not worth change)

---

## Gap Detection

### Scope Clarification: Single Agent Analysis, Not Ecosystem Scan

**PRIMARY**: Analyze only target agent (one agent at a time)
**SECONDARY**: Opportunistic gap detection for related patterns
**NOT IN SCOPE**: Comprehensive 22-agent scan (context-optimizer's role)

### When Gap Detection Triggers

1. **Agent Family Pattern**: Sample 2-3 family members (e.g., researcher-\* agents)
2. **Explicit Cross-Reference**: Read agents mentioned in target agent
3. **Shared Documentation Import**: Search for other agents importing same guide

### Sampling Strategy

**Maximum sample**: 3-5 related agents
**Selection criteria**: Domain similarity, family membership, shared imports
**Performance impact**: ~10-15s additional per sampled agent

### Gap Identification Threshold

- Target agent + 2+ sampled agents share pattern = potential gap
- Total savings ≥ 300 tokens across sampled agents
- Confidence ≥ 0.70 that pattern is truly shared

### Output Clarification

**Note**: "Found in sampled agents - not exhaustive ecosystem scan"
**Recommendation**: "Consider context-optimizer for comprehensive analysis"

### Gap Identification Pattern

```yaml
steps:
  1_collect_common_patterns:
    - For each section across all agents
    - Group by similarity (overlap > 60%)
    - Count occurrences

  2_identify_gaps:
    - Pattern appears in 3+ agents
    - No existing guide covers pattern
    - Total savings ≥ 300 tokens across agents

  3_recommend_new_guide:
    - Document affected agents
    - Describe content pattern
    - Suggest documentation path
    - Calculate total savings
```

---

## Formula Validation

**Note**: All formulas in this methodology guide should be validated through empirical testing. See `tests/unit/test_doc_optimizer_formulas.py` for validation results.

**Expected Validation Coverage**:

- Token estimation: ±5% accuracy (tested on 50+ agent files)
- Overlap weights: 40/30/30 split optimized via ablation study
- Confidence adjustments: Calibrated to historical accuracy data
- Value thresholds: Based on ROI analysis (effort vs savings)

---

**This methodology guide provides the detailed implementation logic for the documentation agent, including all formulas, thresholds, and decision frameworks extracted from the agent prompt for reference and validation purposes.**
