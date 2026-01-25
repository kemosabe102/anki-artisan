# Workflow Phases

Detailed documentation for each phase of the `/analyze-agent` command.

---

## Phase 1: 4-Agent Parallel Analysis

**Duration**: ~10-12 minutes (parallel execution)
**Pattern**: Multi-Agent Analysis Pattern (agent-analysis-suite-protocol.md)

Launch all 4 agents in a **single message** with 4 Task calls:

### Agent 1: claude-code-ecosystem
**Focus**: Structure, schema compliance, integration quality

**Evaluation Criteria**:
1. Frontmatter validation (7 valid fields, no invalid fields)
2. Schema quality (extends base-agent.schema.json, two-state model)
3. Integration compliance (orchestrator-workflow.md entry, CLAUDE.md entry)
4. Quality matrix (9 criteria, 0-5 scale)
5. Maturity level assessment (v0.x -> v1.x -> v2.x -> v3.x)

**Reference Guides**:
- `.claude/docs/01-guides/agents/integration-validation-checklist.md`
- `.claude/docs/01-guides/agents/schema-quality-criteria.md`
- `.claude/docs/01-guides/agents/agent-standards-extended.md`

### Agent 2: claude-code-ecosystem
**Focus**: Prompt quality across 6 frameworks + Anthropic best practices


**Evaluation Criteria**:
1. Structural Quality (16 criteria, Pass/Fail)
2. Anthropic Prompt Engineering (6 principles)
3. Token Optimization (15+ techniques, quantified savings)
4. Testing & Validation (risk-appropriate strategies)
5. Progressive Disclosure (4 factors, A-F grade)
6. Token Density (6 metrics, A-F grade)

**Reference Guides**:
- `.claude/docs/01-guides/agents/anthropic-prompt-standards.md`
- `.claude/docs/01-guides/agents/documentation-anti-patterns.md`

### Agent 3: documentation
**Focus**: Token efficiency and documentation optimization

**Evaluation Criteria**:
1. Base-agent-pattern inheritance (detect duplication, ~1,150 token savings)
2. Progressive disclosure compliance (2-level depth max, 80% essential visibility)
3. Anti-pattern detection (6 patterns)
4. External guide opportunities
5. Token density analysis (<100 tokens/concept = high)

**Reference Guides**:
- `.claude/docs/01-guides/agents/documentation-anti-patterns.md`
- `.claude/docs/01-guides/documentation/progressive-disclosure-validation-framework.md`
- `.claude/docs/01-guides/documentation/doc-optimization-methodology.md`

### Agent 4: tech-debt-investigator
**Focus**: Documentation debt using SQALE/SIG methodology


**Evaluation Criteria**:
1. Documentation debt score (0-100 scale)
2. Technical Debt Ratio (TDR = remediation_cost / development_cost)
3. SQALE grade (A-E) and SIG star rating (1-5)
4. 6-category breakdown
5. Impact/Effort matrix (P1-P4)

---

## Phase 2: Claude Code-Specific Validations

**Duration**: ~2-3 minutes
**Executor**: Orchestrator (after agents return)

### Validation 1: Methodology Appropriateness

**Reference**: `.claude/docs/00-core/frameworks/README.md`

**Steps**:
1. Identify agent domain (`.claude/**`, `packages/**`, `docs/**`, etc.)
2. Assess task complexity (Simple, Medium, High)
3. Determine primary OODA phase
4. Match to recommended methodology:
   - CAGEERF: Complex implementations
   - ReACT: Systematic problem-solving, debugging
   - 5W1H: Requirements gathering, documentation
   - SCAMPER: Optimization, enhancement
5. Generate PASS/PARTIAL/FAIL assessment

### Validation 2: Integration Checklist

**Reference**: `.claude/docs/01-guides/agents/integration-validation-checklist.md`


**7 Requirements**:
1. Frontmatter compliance (7 valid fields)
2. Base-pattern extension declaration
3. orchestrator-workflow.md entry
4. CLAUDE.md entry
5. Schema reference
6. Pre-flight assessment pattern
7. Two-attempt rule compliance

**Output**: PASS (7/7) | PARTIAL (5-6/7) | FAIL (<5/7)

---

## Phase 3: Synthesis & Recommendations

**Duration**: ~2-3 minutes
**Reference**: `.claude/docs/00-core/synthesis-and-recommendation-framework.md`

**Trigger**: If 3+ agents return findings with overlap >0.7 similarity

### Steps

1. **Overlap Detection**:
   - Similarity = (keyword_overlap x 0.4 + domain x 0.3 + location x 0.2 + agent_type x 0.1)
   - Identify findings >0.7 similarity (consolidate duplicates)

2. **Weighted Scoring**:
   - Priority = (Impact x 0.4 + Effort^-1 x 0.3 + Risk x 0.3)
   - Assign P1 (>0.7), P2 (0.5-0.7), P3 (0.3-0.5), P4 (<0.3)

3. **Conflict Resolution**:
   - If agents disagree, present trade-offs with weighted scoring
   - Orchestrator makes final recommendation based on domain fit


4. **Consolidation**:
   - Merge overlapping recommendations
   - Remove duplicates
   - Sequence by dependencies (P1 -> P2 -> P3)

---

## Phase 4: Comprehensive Report Generation

**Duration**: ~3-5 minutes

**Output Structure** (see `report-format.md` for full template):
- Executive Summary (2-3 sentences)
- Overall Quality Score (0-100)
- 5-Dimension Breakdown (Prompt, Schema, Documentation, Integration, Methodology)
- Top 3 Findings (P1 priority)
- Token Savings Opportunities
- Consolidated Recommendations (P1/P2/P3)
- Implementation Roadmap
- Maturity Assessment
- Confidence & Iteration Support

---

## Duration Summary

| Mode | Duration |
|------|----------|
| Single agent | ~15-20 minutes total |
| Ecosystem-wide (--all) | ~2-4 hours (batched) |

**Breakdown (single agent)**:
- Phase 1 (4 agents parallel): 10-12 min
- Phase 2 (validations): 2-3 min
- Phase 3 (synthesis): 2-3 min
- Phase 4 (report): 3-5 min
