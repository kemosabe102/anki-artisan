---
title: "Agent Quality Taxonomy"
date: 2025-11-30
status: ACTIVE
auto-load: agent-analysis
tags: [agents, quality, evaluation, claude-docs]
---

# Agent Quality Taxonomy

**Purpose**: Unified quality dimensions for agent evaluation - canonical reference for claude-code-ecosystem, claude-code-ecosystem, and tech-debt-investigator

**Auto-Load**: This document is automatically loaded when analyzing agents (triggers: "evaluate agent", "agent quality", "analyze agent", "prompt quality")

---

## Quick Reference: 10 Quality Dimensions

| # | Dimension | Primary Evaluator | Weight | Key Criteria |
|---|-----------|-------------------|--------|--------------|
| 1 | Structural Integrity | claude-code-ecosystem F1 | 0.15 | 17 checkpoints, frontmatter, schema |
| 2 | Prompt Engineering | claude-code-ecosystem F2 | 0.15 | 9 Anthropic principles |
| 3 | Token Efficiency | claude-code-ecosystem F3,F5,F6 | 0.10 | <500 lines, base pattern inheritance |
| 4 | Framework Integration | claude-code-ecosystem F7 | 0.10 | Phase-framework mapping, integration depth |
| 5 | Correctness | claude-code-ecosystem | 0.15 | Task accuracy, external validation |
| 6 | Scope Discipline | Both | 0.10 | Clear boundaries, single responsibility |
| 7 | Tool Quality | claude-code-ecosystem | 0.05 | Appropriate selection, clear descriptions |
| 8 | Reliability | claude-code-ecosystem | 0.05 | Stable performance, error recovery |
| 9 | Safety/Compliance | claude-code-ecosystem | 0.10 | Proper refusals, security boundaries |
| 10 | Maintainability | Both | 0.05 | AI-readability, modularity, clarity |

**Total Weight**: 1.00


---

## Dimension Details

### 1. Structural Integrity (0.15)

**Measured by**: claude-code-ecosystem Framework 1 (17 criteria)

**Key Checkpoints**:
- Single responsibility defined
- Scope boundaries documented (what agent does NOT do)
- Frontmatter uses only valid fields (name, description, tools, model, color)
- Extends base-agent-pattern.md
- Schema reference exists
- Two-state model (SUCCESS/FAILURE)
- File operation protocol compliance
- **Filename-only doc references** (NEW - criterion 17)

**Scoring**: Pass/Fail per criterion -> X/17 -> Grade

---

### 2. Prompt Engineering (0.15)

**Measured by**: claude-code-ecosystem Framework 2 (9 principles)

**Key Principles** (weighted):
1. Role assignment (1.2x) - Clear identity and purpose
2. Clarity & directness (1.3x) - Unambiguous instructions
3. Data-instruction separation (1.1x) - Context vs directives
4. Output formatting (1.0x) - Structured JSON, XML tags
5. Step-by-step thinking (1.2x) - OODA/reasoning approach
6. Example usage (1.0x) - Few-shot demonstrations
7. Hallucination prevention (1.1x) - Confidence scoring, evidence
8. XML tag structure (0.9x) - Consistent hierarchy
9. Layered complexity (1.0x) - Progressive disclosure

**Scoring**: 0-5 per principle -> Weighted average -> A-F grade

---

### 3. Token Efficiency (0.10)

**Measured by**: claude-code-ecosystem Frameworks 3, 5, 6

**Key Metrics**:
- Total tokens (baseline from calculate_tokens.py)
- Line count (<500 target)
- Description length (<200 chars)
- Base pattern inheritance (~1,150 token savings)
- Filler word density (<5%)
- Active voice ratio (>80%)
- Reference reuse (>60%)

**Scoring**: Quantified savings + efficiency ratios -> A-F grade

---
### 4. Framework Integration (0.10) [ENHANCED]

**Measured by**: claude-code-ecosystem Framework 7 (phase-aware)

**Reference**: `00-core/frameworks/README.md`

**Key Requirements**:
- Primary framework matches agent domain
- Framework applied throughout workflow (not just mentioned)
- Each OODA phase has appropriate framework assigned
- Explicit deliverables per phase (-> Output: ...)

**Phase-Framework Mapping**:
| OODA Phase | Recommended Frameworks |
|------------|----------------------|
| OBSERVE | Cynefin, OKR, 5W1H |
| ORIENT | ReACT, 5 Whys, CAGEERF, First Principles |
| DECIDE | SCAMPER, Pre-Mortem |
| ACT | Build-Measure-Learn, DMAIC, Disney Creative Strategy |

**Integration Depth Scoring**:
- >=0.75 phases with framework = Grade A
- 0.50-0.74 = Grade B
- 0.25-0.49 = Grade C
- <0.25 or mismatch = Grade D/F

---

### 5. Correctness (0.15)

**Measured by**: claude-code-ecosystem 9-criterion matrix

**Key Criteria**:
- Task accuracy for primary use case
- Output matches documented format
- External validation passing
- Edge cases handled appropriately

**Scoring**: 0-5 scale with evidence requirements

---

### 6. Scope Discipline (0.10)

**Measured by**: Both evaluators

**Key Criteria**:
- Single responsibility principle enforced
- Boundaries section explicitly lists exclusions
- NOT-for cases in description
- Domain restricted to specific directories/file types
- No cross-domain without justification

**Scoring**: Pass/Fail checkpoints + qualitative assessment

---

### 7. Tool Quality (0.05)

**Measured by**: claude-code-ecosystem

**Key Criteria**:
- Appropriate tool tier selection (Tier 1: Read/Grep, Tier 2: Edit, Tier 3: Write/Bash)
- Tool descriptions clear for new team members
- No tool bloat (unused heavy tools)
- Tool usage demonstrated in workflow

**Scoring**: 0-5 scale

---

### 8. Reliability (0.05)

**Measured by**: claude-code-ecosystem

**Key Criteria**:
- Stable performance across contexts
- Error recovery documented
- FAILURE response structure defined
- Graceful degradation patterns
- Retry logic for transient failures

**Scoring**: 0-5 scale

---

### 9. Safety/Compliance (0.10)

**Measured by**: claude-code-ecosystem

**Key Criteria**:
- No prohibited content generation
- Proper refusals for out-of-scope
- Security boundaries documented
- Input validation for Bash commands
- Domain whitelist for external URLs

**Scoring**: 0-5 scale (Critical violations = automatic 0)

---

### 10. Maintainability (0.05)

**Measured by**: Both evaluators

**Key Criteria**:
- AI-readability patterns (from `creating-ai-readable-documentation-framework.md`):
  - Structured headers with scannable format
  - Front-loaded key information
  - Explicit instructions over implicit context
  - Tables over prose where applicable
- Modularity (externalized docs for >50 line sections)
- Clear naming conventions
- Reasonable length (<500 lines agent file)

**Scoring**: 0-5 scale

---

## Overall Grade Calculation

```
Overall = (D1 x 0.15) + (D2 x 0.15) + (D3 x 0.10) + (D4 x 0.10) + 
          (D5 x 0.15) + (D6 x 0.10) + (D7 x 0.05) + (D8 x 0.05) + 
          (D9 x 0.10) + (D10 x 0.05)

Grade Mapping:
- A: 4.5-5.0 (Production ready)
- B: 3.5-4.4 (Good, minor improvements)
- C: 2.5-3.4 (Acceptable, notable gaps)
- D: 1.5-2.4 (Poor, significant work needed)
- F: <1.5 (Failing, major redesign)
```

---

## Cross-Reference Resolution

When evaluators report conflicting assessments:

| claude-code-ecosystem Term | claude-code-ecosystem Term | Canonical Definition |
|---------------------|----------------------|---------------------|
| Format Fidelity | Structural Quality F1 | Use F1's 17 criteria |
| Maintainability | Token Density + Progressive Disclosure | Combine F5, F6 + AI-readability |
| Correctness | (implicit in all) | Use claude-code-ecosystem definition |
| Scope Discipline | Structural criteria 2-3 | Merge into unified checklist |

---

## Integration with Analysis Workflow

When spawning agent analysis (e.g., `/analyze-agent`):

1. **Auto-load this taxonomy** for consistent dimension definitions
2. **Auto-load `thinking-frameworks-catalog.md`** for framework validation
3. Spawn evaluators in parallel:
   - claude-code-ecosystem (dimensions 1-4, 6, 10)
   - claude-code-ecosystem (dimensions 5, 7-9)
   - documentation (token efficiency deep-dive)
   - tech-debt-investigator (maintainability debt)
4. Synthesize results using weights above
5. Report unified grade with per-dimension breakdown

---

## References

- `thinking-frameworks-catalog.md` - Framework-to-agent mappings
- `base-agent-pattern.md` - Agent design standards
- `evaluation-frameworks.md` - claude-code-ecosystem criteria details
- `frameworks.md` - claude-code-ecosystem 9-criterion matrix
- `creating-ai-readable-documentation-framework.md` - AI-readability patterns

---

**Version**: 1.0
**Last Updated**: 2025-11-30
