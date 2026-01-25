# Token Calculation Methodology

**Purpose**: Detailed formulas and accuracy ranges for token estimation in documentation optimization.

---

## Base Formula

```
estimated_tokens = character_count / 4
```

**Rationale**: Approximates GPT tokenization at character level.

**Accuracy**: +/-5% for individual sections (tested against tiktoken)

---

## Current State Calculation

**Input**: Section content (string)

**Process**:
1. Count total characters (including whitespace)
2. Divide by 4
3. Round to nearest integer

**Example**:
```
Section content: 1,024 characters
Estimated tokens: 1024 / 4 = 256 tokens
Actual range: 243-269 tokens (+/-5%)
```

---

## Optimized State Calculation

**Components**:
1. **Reference overhead**: 15-20 tokens per documentation reference
2. **Agent-specific remainder**: Content not covered by documentation
3. **Optimized total**: `reference_overhead + remainder`

**Formula**:
```
optimized_tokens = reference_overhead + (current_tokens × (1 - overlap_percentage))
```

**Conservative Approach**: Use 20 tokens for reference overhead (worst case)


**Example**:
```
Current: 1,000 characters = 250 tokens
Overlap: 0.85 (85% covered by documentation)
Reference overhead: 20 tokens (conservative)
Remainder: 250 × (1 - 0.85) = 37.5 tokens
Optimized: 20 + 37.5 = 57.5 ≈ 58 tokens
```

---

## Savings Calculation

**Formula**:
```
savings = current_tokens - optimized_tokens
```

**Percentage**:
```
savings_percentage = (savings / current_tokens) × 100
```

**Example**:
```
Current: 250 tokens
Optimized: 58 tokens
Savings: 250 - 58 = 192 tokens
Percentage: (192 / 250) × 100 = 76.8%
```

---

## Accuracy Ranges

**Individual Section**: +/-5%
- Based on: Character-to-token ratio variance
- Impact: Minor estimation error
- Mitigation: Use conservative reference overhead

**Total Savings**: +/-10-20%
- Based on: Implementation variance, actual reference formatting
- Impact: Moderate estimation error
- Mitigation: Always report accuracy range

**Sources of Variance**:
1. Tokenization differences (GPT vs actual)
2. Reference formatting choices (brief vs verbose)
3. Agent-specific content identification accuracy
4. Markdown formatting overhead


---

## Best Practices

**Always Include Accuracy Range**:
```markdown
Savings: 192 tokens (+/-19 tokens, 10% variance)
Range: 173-211 tokens
```

**Conservative Estimation**:
- Use 20 tokens for reference overhead (not 15)
- Round optimized tokens up
- Report lower bound of savings range

**Metadata Requirements**:
Every savings estimate must include:
1. Formula used
2. Overlap percentage
3. Reference overhead assumption
4. Accuracy range
5. Assumptions (e.g., "Assumes filename-only reference format")

---

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Optimistic reference overhead (10 tokens) | Overestimated savings | Use 20 tokens |
| Ignoring implementation variance | Disappointed stakeholders | Report +/-10-20% range |
| Rounding savings up | Inflated expectations | Round down or use midpoint |
| Missing accuracy metadata | Unclear confidence | Always include range |

---

## Validation

**Test against tiktoken** (when available):
```python
import tiktoken
encoder = tiktoken.get_encoding("cl100k_base")
actual_tokens = len(encoder.encode(section_content))
estimated_tokens = len(section_content) / 4
variance = abs(actual_tokens - estimated_tokens) / actual_tokens
# Expect: variance <= 0.05 (5%)
```
