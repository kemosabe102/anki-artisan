# Context Optimization Domain Expertise

**Purpose**: Detailed methodologies for token estimation, redundancy detection, ROI calculation, and severity classification.

---

## Token Estimation Techniques

### Accurate Token Counting

```python
# Line-based estimation (quick but approximate)
estimated_tokens = line_count * 4.5

# Character-based estimation (more accurate)
estimated_tokens = character_count / 4

# Word-based estimation (good balance)
estimated_tokens = word_count * 1.3
```

**Recommended**: Line-based for quick scans, character-based for detailed analysis.

### When to Use Each Method

| Method | Speed | Accuracy | Use Case |
|--------|-------|----------|----------|
| Line-based | Fast | ±15% | Initial inventory, large file counts |
| Character-based | Medium | ±5% | Detailed analysis, final reports |
| Word-based | Medium | ±10% | Balanced approach, validation |

---

## Redundancy Detection Algorithm

```
1. Extract sections from all agents:
   - Knowledge Base Integration
   - Pre-Flight Checklist
   - Workflow Structure
   - Error Recovery
   - Parallel Execution
   - Validation Checklist

2. For each section type:
   - Calculate pairwise similarity (Jaccard index or edit distance)
   - Identify sections with >80% similarity
   - Count frequency of near-identical sections

3. Calculate redundancy rate:
   redundancy_rate = duplicated_tokens / total_tokens

4. Estimate consolidation savings:
   savings = duplicated_tokens - (1 * canonical_version_tokens + N * reference_tokens)
```

### Similarity Thresholds

| Similarity | Classification | Action |
|------------|---------------|--------|
| >90% | Near-identical | Consolidate immediately |
| 80-90% | High overlap | Strong consolidation candidate |
| 60-80% | Moderate overlap | Review for partial consolidation |
| <60% | Distinct | Keep separate |

---

## ROI Methodology

**Reference**: See `.claude/docs/01-guides/planning/roi-calculation-guide.md` for complete methodology.

**Token-Specific Adaptation**:
- Convert token savings to hours: `hours_equivalent = token_savings / 1000 * 0.1`
- Apply standard ROI formula from guide with token-based benefits
- Use conservative factor (0.7) per ecosystem standard

**Priority Thresholds** (aligned with ecosystem):
| Priority | ROI Threshold | Action |
|----------|---------------|--------|
| P1 | >=5.0x | Implement immediately |
| P2 | 2.0-4.9x | Schedule for next sprint |
| P3 | 1.0-1.9x | Backlog |
| P4 | <1.0x | Document only |

---

## Severity Classification

```yaml
critical: # Immediate action required
  - MCP tool bloat (>50K tokens)
  - Context overflow risk (>85% utilization)
  - Circular references

high: # Address within 1 week
  - Agent redundancy (>30% duplication)
  - Missing compression strategies
  - Orchestrator bloat (>5K tokens)

medium: # Address within 1 month
  - Structural inconsistencies
  - Verbose examples (>20% of agent)
  - Sub-optimal tool patterns

low: # Nice-to-have improvements
  - Minor duplication (<10%)
  - Style inconsistencies
  - Documentation gaps
```

---

## Context Quality Scoring

**Formula**: Context_Quality = (Section_Clarity × 0.4 + Redundancy_Analysis × 0.3 + Token_Density × 0.2 + Progressive_Disclosure_Compliance × 0.1)

### Dimension Definitions

| Dimension | Weight | Measurement |
|-----------|--------|-------------|
| Section Clarity | 0.4 | Clear headers, logical flow, scannable structure |
| Redundancy Analysis | 0.3 | Inverse of duplication rate (1 - redundancy_rate) |
| Token Density | 0.2 | Information per token (lower filler = higher score) |
| Progressive Disclosure | 0.1 | Compliance with 3-tier loading patterns |

### Health Score Interpretation

| Score | Grade | Status |
|-------|-------|--------|
| 90-100 | A | Excellent - minimal optimization needed |
| 80-89 | B | Good - minor improvements available |
| 70-79 | C | Fair - significant optimization potential |
| 60-69 | D | Poor - major restructuring recommended |
| <60 | F | Critical - immediate attention required |

---

## Token Density Analysis

### Filler Word Detection

Target: <5% filler words in agent definitions.

Common fillers to detect:
- "basically", "essentially", "actually", "really"
- "in order to" (use "to")
- "it is important to note that" (remove)
- "as mentioned above/below" (use direct reference)

### Active Voice Ratio

Target: >80% active voice.

```
Passive: "The file is read by the agent"
Active: "The agent reads the file"
```

### Example Bloat Detection

Target: ≤3 examples per concept, each <20 lines.

```
Bloat signals:
- >3 examples showing same pattern
- Examples >50 lines each
- Redundant examples across agents
```

---

**Usage**: Consult this guide when performing detailed optimization analysis calculations and prioritization decisions.
