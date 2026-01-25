---
name: documentation-optimization
description: >
  Optimizes documentation for token efficiency through reference deduplication, 
  content consolidation, and strategic externalization. Calculates token savings 
  with confidence scoring. Use when: "reduce doc tokens", "optimize references", 
  "trim redundancy", "consolidate docs", "token efficiency". 
  NOT for: validation (documentation-health), generation (documentation-synthesis).
---

# Documentation Optimization

> **Maximize token efficiency through strategic documentation reference optimization and content consolidation.**

---

## Core Methodology

Documentation optimization reduces token consumption through four evidence-based strategies:

1. **Reference Existing**: Replace inline content with references when overlap >=80%
2. **Extend Base**: Combine reference + agent-specific additions for 60-79% overlap
3. **Create New**: Recommend shared documentation when pattern appears across agents
4. **Keep Inline**: Retain content when confidence <0.70 or essential for workflow clarity

### Decision Framework

```
IF overlap >= 0.80 AND confidence >= 0.80:
    → reference_existing (highest priority)
ELSE IF overlap >= 0.60 AND confidence >= 0.70:
    → extend_base
ELSE IF overlap < 0.60 AND pattern_count >= 3 AND confidence >= 0.70:
    → create_new
ELSE:
    → keep_inline (no action)
```

---

## Token Estimation

**Reference**: [token-calculation.md](references/token-calculation.md)

**Quick Formula**: `tokens ≈ character_count / 4`

**Accuracy**: +/-5% for individual sections, +/-10-20% for total savings (implementation variance)

**Calculation Steps**:
1. **Current tokens**: Count characters in target section, divide by 4
2. **Reference overhead**: ~15-20 tokens per documentation reference
3. **Agent-specific remainder**: Content not covered by documentation
4. **Savings**: `current_tokens - (reference_overhead + remainder)`

**Conservative approach**: Always assume worst-case reference overhead to avoid overestimating savings.

**Example**:
```
Section: 1,000 characters = 250 tokens
Documentation covers: 95% of content
Reference overhead: 15 tokens
Agent-specific additions: 12 tokens (5% unique content)
Savings: 250 - (15 + 12) = 223 tokens
```

---

## Overlap Detection

**Reference**: [overlap-algorithm.md](references/overlap-algorithm.md)

**Three-Component Algorithm**:
```
overlap_score = (jaccard × 0.4) + (structural × 0.3) + (semantic × 0.3)
```

### Components

1. **Jaccard Similarity (40%)**: Word-level token overlap
   - Tokenize both texts (lowercase, remove punctuation)
   - Calculate: `|intersection| / |union|`
   - Captures literal content reuse

2. **Structural Similarity (30%)**: Organizational pattern matching
   - Compare section headers, bullet structures, table layouts
   - Identifies format-level alignment
   - Important for reference suitability

3. **Semantic Similarity (30%)**: Concept and intent alignment
   - Domain concepts (agent names, tool patterns, workflows)
   - Conceptual coverage assessment
   - Ensures meaningful content overlap, not just word matching

### Thresholds

| Overlap Range | Classification | Strategy Indication |
|---------------|----------------|---------------------|
| >= 0.80 | High | `reference_existing` candidate |
| 0.60 - 0.79 | Medium | `extend_base` candidate |
| < 0.60 | Low | `keep_inline` or `create_new` |

**Critical**: Overlap alone does not determine strategy. Confidence scoring (below) is required.

---

## Confidence Scoring

**Formula**:
```python
confidence = overlap_score + coverage_adjustment + clarity_adjustment
confidence = min(1.0, max(0.0, confidence))  # Clamp to [0.0, 1.0]
```

### Adjustments

**Coverage Adjustment** (does doc cover agent section concepts?):
- Complete coverage (>=95%): +0.05
- Good coverage (>=85%): +0.00
- Partial coverage (>=70%): -0.05
- Insufficient (<70%): -0.10

**Clarity Preservation** (will reference maintain workflow clarity?):
- Perfect (4/4 criteria met): +0.05
- Good (3/4 criteria met): +0.00
- Reduced (2/4 criteria): -0.05
- Unclear (<=1/4 criteria): -0.10

**Clarity Criteria** (4-point checklist):
1. Terminology remains clear
2. Examples still available
3. Context preserved
4. Completeness maintained

### Confidence Thresholds

| Confidence | Action | Rationale |
|------------|--------|-----------|
| >= 0.90 | Strong recommendation | High certainty, implement first |
| >= 0.80 | Recommend | Good confidence, include in report |
| >= 0.70 | Consider | Borderline, flag for review |
| < 0.70 | Keep inline | Insufficient confidence for change |

**Critical Rule**: Confidence <0.70 = always `keep_inline`, regardless of overlap score.

---

## Optimization Strategies

**Reference**: [optimization-strategies.md](references/optimization-strategies.md)

### 1. reference_existing

**When**: Overlap >=80%, confidence >=80%

**Action**: Replace inline content with filename-only reference

**Example**:
```markdown
Before (250 tokens):
## Error Recovery
[detailed error handling procedures...]

After (15 tokens):
## Error Recovery
See error-recovery-protocol.md
```

**Effort**: 1 (minutes) - simple text replacement

**Typical Savings**: 200-500 tokens per section

---

### 2. extend_base

**When**: Overlap 60-79%, confidence >=70%

**Action**: Reference shared documentation + agent-specific additions

**Example**:
```markdown
Before (400 tokens):
## Phase Workflow
[OODA description, phase definitions, general process...]
[agent-specific phase adaptations...]

After (80 tokens):
## Phase Workflow
Base: ooda-workflow.md

Agent-specific adaptations:
- OBSERVE: Include schema validation
- DECIDE: Use domain-specific thresholds
```

**Effort**: 2 (minutes) - identify unique content, restructure

**Typical Savings**: 300-800 tokens per section


---

### 3. create_new

**When**: Overlap <60%, pattern appears across 3+ agents, confidence >=70%

**Action**: Recommend new shared documentation (do not create directly)

**Example**:
```markdown
Opportunity: "Agent Selection Protocol"
- Found in 5 agents with 150-300 token variations
- Total savings potential: 750-1,200 tokens
- Recommendation: Create .claude/docs/01-guides/agents/selection-protocol.md
```

**Effort**: 4 (minutes) - requires documentation creation by claude-code-ecosystem

**Typical Savings**: 500-1,500 tokens across multiple agents

**Note**: This strategy identifies gaps, does not create documentation.

---

### 4. keep_inline

**When**: Confidence <70% OR essential workflow content

**Action**: No change, retain content in agent prompt

**Rationale**:
- Low overlap with existing docs
- Agent-specific workflow critical for clarity
- Reference would obscure essential context
- Implementation complexity exceeds value

**Example**:
```markdown
Keep inline: Agent-specific OODA adaptations
Keep inline: Custom validation checklists
Keep inline: Domain-specific decision matrices
```

**Effort**: 0 - no action required

**Savings**: 0 tokens

---

## Value Score Calculation

**Formula**: `value_score = (savings × confidence) / effort`

**Units**: Confidence-weighted tokens saved per minute of effort


### Priority Levels

| Priority | Score | Interpretation | Action |
|----------|-------|----------------|--------|
| High | >50 | >1 token/sec ROI | Implement immediately |
| Medium | 20-50 | 0.3-1 token/sec | Implement when available |
| Low | <20 | <0.3 token/sec | Defer or skip |

### Example Calculations

**High Priority (118.75)**:
- Strategy: reference_existing
- Savings: 250 tokens
- Confidence: 0.95
- Effort: 2 minutes
- Calculation: (250 × 0.95) / 2 = 118.75

**Medium Priority (25.5)**:
- Strategy: extend_base
- Savings: 900 tokens
- Confidence: 0.85
- Effort: 30 minutes
- Calculation: (900 × 0.85) / 30 = 25.5

**Low Priority (4.2)**:
- Strategy: create_new
- Savings: 250 tokens
- Confidence: 0.75
- Effort: 45 minutes
- Calculation: (250 × 0.75) / 45 = 4.2

**Interpretation**: Always prioritize by value score, not raw savings. A 250-token savings with 2-minute effort beats a 900-token savings with 30-minute effort.

---

## Gap Detection

**Purpose**: Identify shared patterns not yet in documentation


**Scope**: Target agent + 2-3 sampled related agents (NOT full ecosystem scan)

**Trigger Criteria**:
- Same pattern appears in target + 2+ related agents
- Total savings potential >=300 tokens across sampled agents
- Confidence >=0.70 that pattern is truly shared

**Sampling Strategy**:
- Maximum: 3-5 related agents
- Selection criteria: Domain similarity, agent family membership, shared tool usage
- Performance budget: ~10-15 seconds per sampled agent

**Example**:
```
Pattern detected: "Agent Selection Protocol"
- Found in: orchestrator, context-optimizer, claude-code-ecosystem, documentation
- Individual savings: 150-300 tokens per agent
- Total potential: 600-1,200 tokens
- Recommendation: Create shared documentation
- Strategy: create_new
```

**Note**: Gap detection is opportunistic, not exhaustive. Full ecosystem scans are context-optimizer's responsibility.

---

## Workflow Integration

**Phase 1 - Analysis Request**:
1. Receive target agent or documentation set
2. Parse sections, estimate baseline tokens
3. Extract keywords for documentation search

**Phase 2 - Discovery**:
1. Search `.claude/docs/**/*.md` for candidate matches
2. Calculate overlap using 3-component algorithm
3. Rank candidates by overlap score


**Phase 3 - Decision**:
1. Calculate confidence scores (overlap + adjustments)
2. Apply decision matrix for strategy selection
3. Calculate value scores for prioritization
4. Rank opportunities by value score

**Phase 4 - Reporting**:
1. Generate structured optimization report
2. Include: savings estimates, confidence scores, strategy assignments
3. Provide: priority ranking, implementation guidance
4. Document: metadata (accuracy ranges, assumptions)

---

## Quality Standards

**Token Accuracy**: +/-5% for sections, +/-10-20% for total (implementation variance)

**Overlap Threshold**: >=80% required for `reference_existing` strategy

**Confidence Minimum**: >=0.70 for any optimization action

**Value Score**: Always include in recommendations for prioritization

**Savings Metadata**: Every recommendation must include accuracy range

**Conservative Estimation**: Assume worst-case reference overhead (15-20 tokens)

---

## Anti-Patterns

**DO NOT**:
- Create documentation files (recommend only, delegate to claude-code-ecosystem)
- Perform full ecosystem scans (context-optimizer's role)
- Use full paths for references (filename-only: `error-protocol.md` not `.claude/docs/00-core/error-protocol.md`)
- Skip savings metadata in recommendations
- Recommend optimization with confidence <0.70
- Ignore clarity preservation for essential workflows


**ALWAYS DO**:
- Use filename-only references for documentation
- Include confidence scores (0.0-1.0) for every recommendation
- Calculate value scores: (savings × confidence) / effort
- Mark essential workflows for inline retention (keep_inline strategy)
- Sample 2-3 related agents for gap detection (not full scan)
- Provide accuracy ranges in savings estimates
- Apply 3-component overlap algorithm consistently

---

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Full ecosystem scan | Performance degradation, scope creep | Limit to target + 2-3 samples |
| Ignoring structural similarity | False positives in overlap | Use 3-component algorithm |
| Single-candidate selection | Missed opportunities | Keep top 3 per section |
| Skipping clarity check | Broken workflows after optimization | Apply 4-point clarity criteria |
| Overweighting raw savings | Low-value high-effort recommendations | Use value score prioritization |
| Creating documentation | Scope violation | Recommend only, delegate creation |

---

## Example Analysis Output

```markdown
## Optimization Report: agent-example

### Summary
- Baseline: 2,500 tokens
- Optimized: 1,750 tokens
- Savings: 750 tokens (30% reduction)
- Confidence: 0.85 (high)

### Recommendations (Priority Ranked)

**1. Reference Error Recovery Section** (value: 118.75, HIGH)
- Strategy: reference_existing
- Current: 250 tokens
- Optimized: 15 tokens
- Savings: 235 tokens
- Confidence: 0.95
- Effort: 2 minutes
- Overlap: 0.92 (high)
- Action: Replace with "See error-recovery-protocol.md"

**2. Consolidate Phase Workflow** (value: 25.5, MEDIUM)
- Strategy: extend_base
- Current: 900 tokens
- Optimized: 80 tokens
- Savings: 820 tokens
- Confidence: 0.85
- Effort: 30 minutes
- Overlap: 0.75 (medium)
- Action: Reference ooda-workflow.md + agent-specific adaptations

**3. Keep Agent Selection Matrix Inline** (value: 0, KEEP)
- Strategy: keep_inline
- Current: 300 tokens
- Savings: 0 tokens
- Confidence: 0.65 (below threshold)
- Overlap: 0.50 (low)
- Rationale: Agent-specific decision matrix, essential for workflow clarity
```

---

## Reference Documentation

- **[token-calculation.md](references/token-calculation.md)**: Token estimation formulas, accuracy ranges, calculation methodology
- **[overlap-algorithm.md](references/overlap-algorithm.md)**: 3-component detection algorithm, thresholds, implementation details
- **[optimization-strategies.md](references/optimization-strategies.md)**: Strategy selection criteria, when to use each approach, effort estimates

---

## When to Use This Skill

**Use when**:
- "Reduce documentation tokens"
- "Optimize agent prompt references"
- "Consolidate redundant content"
- "Find documentation overlap"
- "Calculate token savings"
- "Improve token efficiency"
- "Identify reference opportunities"

**NOT for**:
- Documentation validation (use documentation-health skill)
- Documentation generation (use documentation-synthesis skill)
- Full ecosystem optimization (use context-optimizer agent)
- Creating new documentation files (delegate to claude-code-ecosystem)

---

## Performance Expectations

**Single Agent Analysis**: 30-60 seconds
- Phase 1 (OBSERVE): 5-10s (file read, section extraction)
- Phase 2 (ORIENT): 15-25s (doc discovery, overlap calculation)
- Phase 3 (DECIDE): 5-10s (confidence scoring, strategy selection)
- Phase 4 (ACT): 5-15s (report generation)

**With Gap Detection**: +10-15s per sampled agent (2-3 agents max)

**Output Size**: 1,500-3,000 tokens (structured report)

---

## Success Criteria

**Analysis Complete When**:
- All sections analyzed for overlap
- Strategies assigned with confidence scores
- Value scores calculated for prioritization
- Savings estimates include accuracy ranges
- Report follows schema format

**High-Quality Output Includes**:
- Priority-ranked recommendations (value score sorted)
- Conservative savings estimates (worst-case overhead)
- Clear implementation guidance per strategy
- Metadata: accuracy, assumptions, thresholds applied
- Gap detection results (if applicable)
