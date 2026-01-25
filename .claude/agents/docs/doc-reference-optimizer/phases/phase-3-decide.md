# Phase 3: DECIDE - Strategy Selection & Scoring

**OODA Stage**: DECIDE | **Time Allocation**: 15-20%

**Purpose**: Apply confidence scoring, select optimization strategy per section, calculate value scores

**Deliverable**: Strategy assignments with confidence and value scores for each optimization opportunity

---

## Workflow Steps

### Step 3.1: Confidence Scoring

**Input**: Ranked candidates from Phase 2

**Process**:
1. **Base Score**: Start with overlap percentage (0.0-1.0)
2. **Guide Coverage Adjustment**: +0.05 if doc covers >90% of section concepts
3. **Clarity Preservation Adjustment**: -0.10 if reference would obscure essential workflow
4. **Final**: Clamp to [0.0, 1.0]

**Formula**: `confidence = min(1.0, max(0.0, overlap + coverage_adj + clarity_adj))`

**Output**: Confidence score per section-doc pair

### Step 3.2: Strategy Selection

**Input**: Confidence scores + overlap thresholds


**Decision Matrix**:

| Overlap | Confidence | Strategy |
|---------|------------|----------|
| >= 0.80 | >= 0.80 | `reference_existing` - Replace with doc reference |
| >= 0.60 | >= 0.70 | `extend_base` - Reference + agent-specific additions |
| < 0.60 | >= 0.70 | `create_new` - Recommend new shared doc |
| Any | < 0.70 | `keep_inline` - Retain in agent prompt |

**Output**: Strategy assignment per section

### Step 3.3: Value Score Calculation

**Input**: Strategy, savings estimate, confidence, effort estimate

**Process**:
1. **Savings Estimate**: `current_tokens - (reference_overhead + agent_specific_remainder)`
   - Reference overhead: ~15 tokens per doc reference
   - Agent-specific remainder: content not covered by doc
2. **Effort Estimate** (1-5 scale):
   - `reference_existing`: 1 (simple replacement)
   - `extend_base`: 2 (reference + minor additions)
   - `create_new`: 4 (doc creation required)
   - `keep_inline`: 0 (no action)
3. **Value Score**: `(savings * confidence) / max(effort, 1)`

**Output**: Value score per optimization opportunity


### Step 3.4: Priority Ranking

**Input**: All opportunities with value scores

**Process**:
1. Sort by value score descending
2. Group by strategy type
3. Identify quick wins (high value, low effort)

**Output**: Prioritized opportunity list

---

## Confidence Thresholds

| Confidence | Action | Rationale |
|------------|--------|-----------|
| >= 0.90 | Strong recommendation | High certainty, implement first |
| >= 0.80 | Recommend | Good confidence, include in report |
| >= 0.70 | Consider | Borderline, flag for review |
| < 0.70 | Keep inline | Insufficient confidence for change |

---

## Quick Checklist

Before advancing to Phase 4 (ACT):

- [ ] Confidence scores calculated for all candidates
- [ ] Strategy assigned to each section
- [ ] Value scores computed
- [ ] Opportunities prioritized by value
- [ ] Quick wins identified


---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Ignoring clarity preservation | Essential workflows must stay readable |
| Overweighting savings | High savings + low confidence = bad recommendation |
| Skipping effort estimation | Value score requires effort denominator |
| Equal treatment of strategies | `reference_existing` always preferred over `create_new` |

---

## Exit Criteria

**All criteria must pass to proceed**

| Criterion | Weight | Check |
|-----------|--------|-------|
| Confidence scored | 0.30 | All candidates have confidence |
| Strategies assigned | 0.30 | Every section has strategy |
| Value calculated | 0.25 | Value scores computed |
| Priorities set | 0.15 | Opportunities ranked |

---

**Previous Phase**: [Phase 2: ORIENT](phase-2-orient.md)
**Next Phase**: [Phase 4: ACT](phase-4-act.md)
