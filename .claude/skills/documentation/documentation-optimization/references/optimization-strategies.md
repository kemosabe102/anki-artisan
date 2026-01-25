# Optimization Strategies

**Purpose**: Detailed guidance on when and how to apply each documentation optimization strategy.

---

## Strategy 1: reference_existing

**When to Use**:
- Overlap >=0.80 (high content match)
- Confidence >=0.80 (high certainty)
- Documentation already exists
- Section is not critical workflow step

**Decision Criteria**:
```
IF overlap >= 0.80 AND confidence >= 0.80 AND doc_exists:
    → reference_existing
```

**Implementation**:
1. Identify exact documentation file
2. Replace entire section with filename-only reference
3. Remove inline content completely

**Reference Format**:
```markdown
## Section Name
See filename.md
```

**Example - Before (250 tokens)**:
```markdown
## Error Recovery

When analysis fails:
1. Check file permissions
2. Verify file format (YAML frontmatter required)
3. Validate schema structure
4. Retry with error logging enabled

Common errors:
- FileNotFoundError: Check path, use absolute paths
- YAMLError: Validate frontmatter syntax
- SchemaValidationError: Compare against schema.json
```

**Example - After (15 tokens)**:
```markdown
## Error Recovery
See error-recovery-protocol.md
```

**Savings**: 235 tokens (94% reduction)

**Effort**: 1-2 minutes (simple text replacement)


**Typical Savings Range**: 200-500 tokens per section

**Risk Level**: Low (documentation already validated)

**Prerequisites**:
- Documentation file exists and is accessible
- Content coverage >=90%
- No agent-specific customizations required

---

## Strategy 2: extend_base

**When to Use**:
- Overlap 0.60-0.79 (medium content match)
- Confidence >=0.70
- Documentation covers base concepts
- Agent has specific customizations/additions

**Decision Criteria**:
```
IF overlap >= 0.60 AND overlap < 0.80 AND confidence >= 0.70 AND has_agent_specific_content:
    → extend_base
```

**Implementation**:
1. Reference shared documentation for base concepts
2. Add "Agent-specific:" section below reference
3. Include only unique content not in documentation

**Format**:
```markdown
## Section Name
Base: filename.md

Agent-specific adaptations:
- [unique point 1]
- [unique point 2]
```

**Example - Before (900 tokens)**:
```markdown
## Phase Workflow

The OODA loop (Observe, Orient, Decide, Act) provides a structured decision-making framework:

**OBSERVE**: Gather information about current state
- Read files for context
- Parse user request
- Identify key entities
- Extract requirements

**ORIENT**: Analyze information and assess situation
- Calculate confidence scores
- Identify knowledge gaps
- Determine readiness thresholds
- Match to decision criteria

**DECIDE**: Select action based on analysis
- Choose optimization strategy
- Prioritize recommendations
- Calculate value scores

**ACT**: Execute decisions
- Generate reports
- Validate outputs
- Document results

For this agent, apply these phase-specific adaptations:
- OBSERVE: Include schema validation during file read
- ORIENT: Use domain-specific threshold (overlap >=0.80 for references)
- DECIDE: Apply confidence scoring with clarity preservation
- ACT: Generate JSON output per schema requirements
```

**Example - After (80 tokens)**:
```markdown
## Phase Workflow
Base: ooda-workflow.md

Agent-specific adaptations:
- OBSERVE: Include schema validation during file read
- ORIENT: Use overlap >=0.80 threshold for reference candidates
- DECIDE: Apply confidence scoring with clarity preservation criteria
- ACT: Generate JSON output per schema requirements
```

**Savings**: 820 tokens (91% reduction)

**Effort**: 2-5 minutes (identify unique content, restructure)

**Typical Savings Range**: 300-800 tokens per section

**Risk Level**: Medium (requires accurate identification of unique content)

**Prerequisites**:
- Documentation covers 60-80% of section content
- Agent-specific additions are clearly identifiable
- Reference + additions maintain clarity

---

## Strategy 3: create_new


**When to Use**:
- Overlap <0.60 (no existing documentation match)
- Pattern appears in 3+ agents
- Total savings potential >=300 tokens across agents
- Confidence >=0.70 that pattern is shared

**Decision Criteria**:
```
IF overlap < 0.60 AND pattern_count >= 3 AND total_savings >= 300 AND confidence >= 0.70:
    → create_new (recommend only, do not create)
```

**Implementation** (RECOMMENDATION ONLY):
1. Identify shared pattern across multiple agents
2. Calculate total savings potential
3. Recommend documentation location and content outline
4. Delegate creation to claude-code-ecosystem

**Report Format**:
```markdown
## Gap Identified: [Pattern Name]

**Pattern Found In**:
- agent-1 (250 tokens)
- agent-2 (300 tokens)
- agent-3 (200 tokens)
- agent-4 (150 tokens)

**Total Savings Potential**: 900 tokens (after doc creation)

**Recommended Documentation**:
- Location: .claude/docs/01-guides/[category]/[pattern-name].md
- Content Outline:
  1. Pattern overview
  2. Common use cases
  3. Implementation examples
  4. Best practices

**Next Steps**: Delegate to claude-code-ecosystem for documentation creation
```

**Savings**: 500-1,500 tokens total (across all agents, after implementation)

**Effort**: 4-8 minutes analysis + 30-60 minutes documentation creation (delegated)

**Typical Savings Range**: 100-400 tokens per agent (after doc created)

**Risk Level**: High (requires new documentation creation, validation, adoption)


**Prerequisites**:
- Pattern confirmed across 3+ agents via sampling
- Shared content clearly defined
- No existing documentation covers this pattern
- Value score justifies creation effort

**Important**: This strategy is RECOMMENDATION ONLY. Do not create documentation files. Delegate to claude-code-ecosystem.

---

## Strategy 4: keep_inline

**When to Use**:
- Confidence <0.70 (insufficient certainty for change)
- Essential workflow content (clarity critical)
- Agent-specific decision matrix or checklist
- Implementation complexity exceeds value

**Decision Criteria**:
```
IF confidence < 0.70 OR is_essential_workflow OR value_score < 5:
    → keep_inline (no action)
```

**Implementation**: No changes required

**Report Format**:
```markdown
## Keep Inline: [Section Name]

**Rationale**: [one of below]
- Confidence below threshold (0.65 < 0.70)
- Essential workflow step, critical for clarity
- Agent-specific decision matrix
- Low value score (3.2 < 5.0)

**Current Tokens**: 300
**Savings**: 0 (no optimization)
```

**Savings**: 0 tokens

**Effort**: 0 minutes

**Risk Level**: None (status quo maintained)

**Examples of Keep Inline Content**:
- Agent-specific OODA phase adaptations with custom thresholds
- Domain-specific decision matrices
- Critical workflow checklists unique to agent
- Error recovery procedures with agent-specific tools
- Custom validation criteria


---

## Strategy Selection Decision Tree

```
START
  |
  ├─ Does documentation exist with overlap >=0.80 AND confidence >=0.80?
  |    YES → reference_existing
  |    NO ↓
  |
  ├─ Does documentation exist with overlap >=0.60 AND confidence >=0.70?
  |    YES → extend_base
  |    NO ↓
  |
  ├─ Pattern appears in 3+ agents AND total savings >=300 tokens AND confidence >=0.70?
  |    YES → create_new (recommend only)
  |    NO ↓
  |
  └─ keep_inline (no action)
```

---

## Effort Estimation Guide

| Strategy | Typical Effort | Effort Score | Notes |
|----------|----------------|--------------|-------|
| reference_existing | 1-2 min | 1 | Simple text replacement |
| extend_base | 2-5 min | 2 | Identify unique content, restructure |
| create_new | 30-60 min | 4 | Includes documentation creation (delegated) |
| keep_inline | 0 min | 0 | No action required |

**Effort Score Usage**: Denominator in value score calculation: `(savings × confidence) / effort`

---

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Using reference_existing for 70% overlap | Incomplete coverage, broken workflows | Require >=80% overlap |
| Skipping agent-specific content in extend_base | Loss of critical customizations | Always identify unique content |
| Creating docs instead of recommending | Scope violation | Recommend only, delegate to claude-code-ecosystem |
| Not justifying keep_inline | Unclear why optimization skipped | Always provide rationale |
| Using full paths in references | Verbose, brittle | Filename-only: `workflow.md` not `.claude/docs/workflow.md` |


---

## Strategy Prioritization

**Always prioritize in this order** (when multiple opportunities exist):

1. **reference_existing**: Highest confidence, lowest effort, immediate savings
2. **extend_base**: Medium effort, good savings, maintains customization
3. **create_new**: High effort, deferred savings, requires creation
4. **keep_inline**: Last resort, used when other strategies not viable

**Use value scores to rank within each strategy tier.**

---

## Validation Checklist

Before recommending any strategy:

**reference_existing**:
- [ ] Overlap >=0.80
- [ ] Confidence >=0.80
- [ ] Documentation file exists and accessible
- [ ] Coverage >=90% of section content
- [ ] Reference preserves clarity

**extend_base**:
- [ ] Overlap 0.60-0.79
- [ ] Confidence >=0.70
- [ ] Agent-specific content clearly identified
- [ ] Base doc + additions maintain completeness
- [ ] Unique content <=40% of section

**create_new**:
- [ ] Pattern confirmed in 3+ agents
- [ ] Total savings >=300 tokens
- [ ] Confidence >=0.70
- [ ] No existing doc covers pattern
- [ ] Value score justifies creation effort

**keep_inline**:
- [ ] Rationale documented (low confidence OR essential workflow OR low value)
- [ ] No viable alternative strategy
