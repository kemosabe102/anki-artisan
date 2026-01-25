---
title: "Agent Analysis Suite Protocol"
date: 2025-11-12
status: ACTIVE
tags: [workflow, multi-agent, analysis, quality-assurance]
---

**Purpose**: Standard workflow for analyzing agent definitions, prompt quality, and documentation efficiency using coordinated multi-agent analysis.

**Quick Reference**: Launch 4 core agents in parallel → Synthesize findings → Deliver consolidated recommendations

---

## Table of Contents

1. [When to Use](#when-to-use)
2. [Standard Suite Composition](#standard-suite-composition)
3. [Launch Pattern](#launch-pattern)
4. [Output Synthesis](#output-synthesis)
5. [Expected Outputs](#expected-outputs)
6. [Benefits](#benefits)
7. [Example Scenarios](#example-scenarios)
8. [Related Documentation](#related-documentation)

---

## When to Use

Use the Agent Analysis Suite Protocol when:

- **Agent Quality Assessment**: Evaluating agent definition quality, structure, and compliance
- **Prompt Optimization**: Identifying prompt engineering improvements and anti-patterns
- **Documentation Reviews**: Assessing documentation efficiency and token density
- **Agent Ecosystem Health**: Conducting regular health checks on agent definitions
- **Pre-Release Validation**: Ensuring new agents meet quality standards before deployment
- **Technical Debt Assessment**: Identifying documentation debt and maintenance burden
- **Performance Optimization**: Finding opportunities to reduce token usage and improve efficiency

**Decision Criteria**:

- Task involves agent definition analysis → Use this protocol
- Task requires multi-perspective quality assessment → Use this protocol
- Task is focused on single code file bug fix → Use debugger instead
- Task is about implementation in packages/** → Use development instead

---

## Standard Suite Composition

### Core Analysis Agents (Always Include)

These 4 agents provide comprehensive 360° analysis and should be launched in EVERY agent analysis task:

#### 1. claude-code-ecosystem

**Domain**: Agent definition structure, schema compliance, lifecycle assessment
**Focus**:

- Agent definition structure validation
- Schema compliance checking
- Lifecycle phase implementation
- Base pattern adherence
- Identity and scope clarity
- Workflow structure assessment

**Output**: Structure quality score, schema violations, lifecycle gaps, improvement recommendations

#### 2. claude-code-ecosystem

**Domain**: Prompt quality across 6 frameworks, anti-pattern detection, optimization opportunities
**Focus**:

- Prompt clarity and specificity
- Instruction completeness
- Anti-pattern detection (vagueness, ambiguity, conflicting instructions)
- Role definition quality
- Context provision effectiveness
- Output format specification

**Output**: Prompt quality score (0-100), framework-specific grades, anti-patterns detected, optimization opportunities

**6 Evaluation Frameworks**:

1. Clarity & Specificity
2. Instruction Completeness
3. Context Provision
4. Output Format Specification
5. Anti-Pattern Detection
6. Role Definition Quality

#### 3. documentation

**Domain**: Token efficiency, verbose content analysis, documentation reference opportunities
**Focus**:

- Token density analysis (tokens per meaningful unit)
- Verbose content detection
- Documentation reference extraction opportunities
- Redundant content identification
- Compression strategies
- Reference link optimization

**Output**: Token savings estimate, verbose sections identified, reference extraction opportunities, compression recommendations

**Token Density Thresholds**:

- High quality: <100 tokens per concept
- Acceptable: 100-150 tokens per concept
- Verbose: >150 tokens per concept

#### 4. tech-debt-investigator

**Domain**: Documentation debt, consistency scoring, maintainability assessment
**Focus**:

- Documentation debt calculation (SQALE methodology)
- Consistency scoring across sections
- Maintainability assessment
- Technical debt ratio (TDR)
- SQALE grade (A-E)
- SIG star rating (1-5)
- Remediation effort estimation

**Output**: debt_score (0-100), TDR, SQALE grade, SIG rating, 6-category breakdown, remediation roadmap

**6 Debt Categories**:

1. Code Quality (not applicable for agent docs, but framework checks structural quality)
2. Architecture (agent structure and organization)
3. Testing (validation and quality assurance references)
4. Documentation (completeness, clarity, accuracy)
5. Infrastructure (tool integration, hook references)
6. Design/UI (presentation, formatting, readability)

---

### Optional Analysis Agents (Include When Relevant)

Launch these agents when specific analysis needs arise:

#### 5. context-optimizer

**When to Use**: Ecosystem-wide analysis when reviewing multiple agents or CLAUDE.md
**Focus**:

- Cross-agent consistency
- Ecosystem-wide patterns
- CLAUDE.md optimization
- Token budget management
- Context window efficiency
- Reference extraction at scale

**Output**: Ecosystem health score, cross-agent issues, CLAUDE.md optimization opportunities

**Trigger Conditions**:

- Analyzing 3+ agents simultaneously
- CLAUDE.md optimization task
- Cross-agent consistency review
- Token budget exceeding thresholds

#### 6. documentation

**When to Use**: Link health, documentation standards compliance, organization validation
**Focus**:

- Link health validation (internal and external)
- Documentation structure compliance
- Naming convention enforcement (kebab-case.md)
- Cross-reference integrity
- Organization compliance (docs/DOCS-MANAGEMENT.md)
- Orphan detection

**Output**: Link health score, broken links report, naming violations, organization compliance assessment

**Trigger Conditions**:

- Agent references external documentation
- Link validation needed
- Documentation structure concerns
- File organization review

#### 7. code-quality

**When to Use**: If agent has associated Python tools or validation scripts
**Focus**:

- Python code quality standards
- Type hint compliance
- Security vulnerability detection
- Testing coverage
- Style guide adherence (Ruff)
- Performance optimization

**Output**: Code quality score, violations detected, security issues, performance recommendations

**Trigger Conditions**:

- Agent includes Python tools (scripts/file_ops.py, hooks, etc.)
- Validation logic implementation
- Security-critical operations
- Performance concerns

---

## Launch Pattern

### Critical Rule: Single Message, Multiple Task Calls

**MANDATORY**: Launch all core agents in a SINGLE orchestrator message with multiple Task tool calls.

**Why Parallel Execution**:

- **Speed**: ~10 minutes for complete analysis vs 40+ minutes sequential
- **Independence**: Agent analyses are independent (no dependencies)
- **Resource Efficiency**: Optimal Claude Code parallel execution
- **Consistent Context**: All agents work from same starting state

### Example Orchestrator Pattern

```markdown
User Request: "Analyze debugger agent quality"

Orchestrator Response:
"Launching Agent Analysis Suite for debugger agent..."

[Single message with 4 Task calls in parallel]

Task(claude-code-ecosystem,
  "Analyze agent definition structure and schema compliance for .claude/agents/debugger.md.
   Focus: Base pattern adherence, lifecycle implementation, schema validation.")

Task(claude-code-ecosystem,
  "Evaluate prompt quality for .claude/agents/debugger.md across 6 frameworks.
   Focus: Clarity, completeness, anti-patterns, role definition.")

Task(documentation,
  "Analyze token efficiency for .claude/agents/debugger.md.
   Focus: Verbose content, reference extraction opportunities, compression strategies.")

Task(tech-debt-investigator,
  "Assess documentation debt for .claude/agents/debugger.md using SQALE methodology.
   Focus: Consistency, maintainability, TDR calculation, remediation priorities.")
```

### Parallel Execution Rules

**Maximum Agents**:

- Core suite: 4 agents (always)
- With optionals: 5-7 agents (when triggered)
- Absolute maximum: 7 agents (optimal for synthesis)

**Single Message Structure**:

```markdown
[Opening context statement]

Task(agent-1, "specific instruction...")
Task(agent-2, "specific instruction...")
Task(agent-3, "specific instruction...")
Task(agent-4, "specific instruction...")
[optional: Task(agent-5, "specific instruction...")]

"Synthesizing results using synthesis-and-recommendation-framework.md after completion."
```

**Task Instruction Format**:

- Agent name from Quick Matrix or agent-selection-guide.md
- Specific file path(s) to analyze
- Focus areas for this agent's domain
- Expected output format reference (agent schema)

---

## Output Synthesis

After all agents complete, orchestrator applies synthesis protocol:

### Step 1: Aggregate Findings

**Process**:

1. Collect all agent outputs (SUCCESS/FAILURE status)
2. Extract findings, scores, recommendations from agent_specific_output
3. Detect overlapping findings (similarity >0.7 threshold)
4. Group related recommendations by category

**Overlap Detection**:

- Same issue identified by 2+ agents → HIGH PRIORITY (cross-domain concern)
- Similar recommendations from 2+ agents → VALIDATE and consolidate
- Conflicting recommendations → ANALYZE trade-offs and present options

**Categories**:

- Structural issues (claude-code-ecosystem)
- Prompt quality issues (claude-code-ecosystem)
- Token efficiency opportunities (documentation)
- Documentation debt (tech-debt-investigator)
- Cross-cutting concerns (multiple agents)

### Step 2: Apply Synthesis Framework

**Reference**: `.claude/docs/00-core/synthesis-and-recommendation-framework.md`

**Trigger Condition**: 3+ agents return findings with overlap >0.7

**Synthesis Process**:

1. **Detect Overlaps**: Identify similar findings across agents (Jaccard similarity >0.7)
2. **Score Solutions**: Weight recommendations by (Impact × 0.4) + (Effort × 0.3) + (Risk × 0.2) + (Coverage × 0.1)
3. **Consolidate Recommendations**: Merge similar recommendations, resolve conflicts
4. **Prioritize Actions**: P1 (critical, immediate), P2 (strategic, planned), P3 (defer, opportunistic)
5. **Generate Roadmap**: Sequenced implementation plan with effort estimates

**Weighted Scoring Formula**:

```text
Recommendation_Score = (Impact × 0.4) + (Effort × 0.3) + (Risk × 0.2) + (Coverage × 0.1)

Where:
- Impact: 0.0-1.0 (how much improvement expected)
- Effort: 1.0-0.0 (inverse scale: low effort = high score)
- Risk: 1.0-0.0 (inverse scale: low risk = high score)
- Coverage: 0.0-1.0 (how many issues addressed)
```

### Step 3: Consolidated Recommendations

**Priority Levels**:

**P1 - Critical (Immediate Action)**:

- Blocking issues (schema violations, broken references)
- High impact + low effort (quick wins)
- Security or stability concerns
- Must-fix before deployment

**P2 - Strategic (Planned)**:

- Medium-high impact + medium effort
- Architectural improvements
- Significant token savings (>500 tokens)
- Quality enhancements

**P3 - Defer (Opportunistic)**:

- Low-medium impact + high effort
- Nice-to-have improvements
- Minor optimizations (<100 tokens saved)
- Future considerations

**Format**:

```markdown
## Priority Recommendations

### P1 - Critical (Complete within 1 sprint)
1. [Issue]: [Description]
   - Impact: High | Effort: 2-4h | Affected: [sections]
   - Recommendation: [Specific action]
   - Rationale: [Why priority 1]

### P2 - Strategic (Plan for next 2-3 sprints)
2. [Issue]: [Description]
   - Impact: Medium | Effort: 4-8h | Affected: [sections]
   - Recommendation: [Specific action]
   - Rationale: [Why priority 2]

### P3 - Defer (Backlog)
3. [Issue]: [Description]
   - Impact: Low | Effort: 8-16h | Affected: [sections]
   - Recommendation: [Specific action]
   - Rationale: [Why deferred]
```

### Step 4: Actionable Next Steps

**Delivery Format**:

1. **Executive Summary** (2-3 sentences)
2. **Overall Quality Score** (0-100 weighted average)
3. **Top 3 Findings** (highest priority issues)
4. **Consolidated Recommendations** (P1/P2/P3 breakdown)
5. **Implementation Roadmap** (sequenced actions with dependencies)
6. **Estimated Effort** (total hours across all recommendations)

---

## Expected Outputs

### Individual Agent Outputs

Each agent returns structured output conforming to their schema:

**claude-code-ecosystem**:

```json
{
  "status": "SUCCESS",
  "agent": "claude-code-ecosystem",
  "confidence": 0.92,
  "agent_specific_output": {
    "structure_quality_score": 85,
    "schema_compliance": "PASS",
    "lifecycle_gaps": ["Missing ORIENT phase example"],
    "base_pattern_adherence": 0.90,
    "recommendations": [...]
  }
}
```

**claude-code-ecosystem**:

```json
{
  "status": "SUCCESS",
  "agent": "claude-code-ecosystem",
  "confidence": 0.88,
  "agent_specific_output": {
    "prompt_quality_score": 78,
    "framework_grades": {
      "clarity": "B+",
      "completeness": "A-",
      "context_provision": "B",
      ...
    },
    "anti_patterns": ["Vague constraint in section X"],
    "optimization_opportunities": [...]
  }
}
```

**documentation**:

```json
{
  "status": "SUCCESS",
  "agent": "documentation",
  "confidence": 0.85,
  "agent_specific_output": {
    "current_token_count": 3200,
    "token_savings_estimate": 450,
    "verbose_sections": ["Tool Usage Patterns (250 tokens redundant)"],
    "reference_extraction_opportunities": [...],
    "compression_recommendations": [...]
  }
}
```

**tech-debt-investigator**:

```json
{
  "status": "SUCCESS",
  "agent": "tech-debt-investigator",
  "confidence": 0.90,
  "agent_specific_output": {
    "debt_score": 58,
    "tdr": 0.12,
    "sqale_grade": "C",
    "sig_rating": 3,
    "category_breakdown": {
      "architecture": 65,
      "documentation": 52,
      "testing": 70,
      ...
    },
    "hotspots": [...],
    "remediation_roadmap": [...]
  }
}
```

### Synthesized Output Format

```markdown
# Agent Analysis Report: [Agent Name]

**Analysis Date**: 2025-11-12
**Agents Involved**: claude-code-ecosystem, claude-code-ecosystem, documentation, tech-debt-investigator
**Analysis Duration**: ~10 minutes

---

## Executive Summary

[2-3 sentence overview of findings]

**Overall Quality Score**: 82/100 (Grade: B+)

**Key Findings**:
- [Finding 1] - Priority: P1, Impact: High
- [Finding 2] - Priority: P1, Impact: Medium
- [Finding 3] - Priority: P2, Impact: Medium

---

## Detailed Analysis

### 1. Structure & Compliance (claude-code-ecosystem)
- **Quality Score**: 85/100
- **Schema Compliance**: PASS
- **Base Pattern Adherence**: 90%
- **Key Issues**:
  - Missing ORIENT phase example (P1)
  - Incomplete tool selection guidance (P2)

### 2. Prompt Quality (claude-code-ecosystem)
- **Quality Score**: 78/100
- **Framework Grades**: A- (Completeness), B+ (Clarity), B (Context)
- **Anti-Patterns Detected**: 2 (vague constraints, ambiguous examples)
- **Key Issues**:
  - Vague constraint in Tool Usage section (P1)
  - Missing role definition clarity (P2)

### 3. Token Efficiency (documentation)
- **Current Tokens**: 3,200
- **Savings Estimate**: 450 tokens (14% reduction)
- **Verbose Sections**: 3 identified
- **Key Opportunities**:
  - Extract 250 tokens from Tool Usage Patterns to reference doc (P1)
  - Compress 200 tokens in examples using reference links (P2)

### 4. Technical Debt (tech-debt-investigator)
- **Debt Score**: 58/100
- **TDR**: 0.12 (12% of content is debt)
- **SQALE Grade**: C
- **SIG Rating**: 3 stars
- **Key Issues**:
  - Documentation inconsistency (P1)
  - Missing validation examples (P2)
  - Outdated workflow references (P2)

---

## Consolidated Recommendations

### P1 - Critical (Complete within 1 sprint - 6-8 hours)

1. **Fix vague constraint in Tool Usage section**
   - Impact: High | Effort: 2h | Affected: Tool Usage Patterns section
   - Recommendation: Add specific thresholds and examples for tool selection
   - Rationale: Causes ambiguity in agent decision-making, identified by 2 agents

2. **Extract verbose Tool Usage Patterns content to reference doc**
   - Impact: High | Effort: 3h | Affected: Tool Usage section
   - Recommendation: Create tool-selection-reference.md, reduce inline content to 50 tokens
   - Rationale: 250 token savings, improves readability, identified by documentation

3. **Add missing ORIENT phase example**
   - Impact: Medium | Effort: 1-2h | Affected: Workflow section
   - Recommendation: Include concrete ORIENT example with Context_Quality calculation
   - Rationale: ORIENT is 44% of OODA loop, missing example creates gaps

### P2 - Strategic (Plan for next 2-3 sprints - 8-12 hours)

4. **Improve role definition clarity**
   - Impact: Medium | Effort: 4h | Affected: Identity section
   - Recommendation: Expand role definition with concrete boundaries and examples
   - Rationale: Moderate prompt quality impact, identified by claude-code-ecosystem

5. **Compress examples using reference links**
   - Impact: Medium | Effort: 3h | Affected: Multiple sections
   - Recommendation: Replace inline examples with references to examples repository
   - Rationale: 200 token savings, improves maintainability

6. **Update outdated workflow references**
   - Impact: Medium | Effort: 2h | Affected: Workflow section
   - Recommendation: Update references to match current workflow standards
   - Rationale: Documentation debt reduction, consistency improvement

### P3 - Defer (Backlog - 4-6 hours)

7. **Add advanced validation examples**
   - Impact: Low | Effort: 4h | Affected: Validation section
   - Recommendation: Create comprehensive validation example set
   - Rationale: Nice-to-have for edge cases, not blocking current usage

---

## Implementation Roadmap

**Sprint 1** (6-8 hours):
1. Fix vague constraint (2h) → Prerequisite: None
2. Extract verbose content (3h) → Prerequisite: Create reference doc
3. Add ORIENT example (2h) → Prerequisite: None

**Sprint 2** (8-12 hours):
4. Improve role definition (4h) → Prerequisite: None
5. Compress examples (3h) → Prerequisite: Examples repository exists
6. Update workflow references (2h) → Prerequisite: Workflow standards finalized

**Backlog** (Future):
7. Add advanced validation examples (4h) → Prerequisite: Core examples complete

**Total Estimated Effort**: 18-26 hours across 3 sprints

---

## Metrics Summary

| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| Quality Score | 82/100 | 90/100 | +8 points |
| Token Count | 3,200 | 2,750 | -450 tokens (14%) |
| Debt Score | 58/100 | 75/100 | +17 points |
| TDR | 0.12 | 0.08 | -0.04 (33% reduction) |
| SQALE Grade | C | B | +1 grade |
| Prompt Quality | 78/100 | 85/100 | +7 points |

---

## Next Steps

1. **Immediate Actions** (P1):
   - Assign P1 recommendations to sprint planning
   - Create tool-selection-reference.md for content extraction
   - Schedule review session for vague constraint fixes

2. **Planning Actions** (P2):
   - Add P2 recommendations to product backlog
   - Verify examples repository exists for compression work
   - Confirm workflow standards are finalized

3. **Monitoring**:
   - Re-run Agent Analysis Suite in 2 sprints to measure progress
   - Track token count reduction vs 450 target
   - Monitor debt score improvement vs 75 target

---

## Appendix: Agent-Specific Details

[Optional: Include full agent outputs for reference]

### claude-code-ecosystem Full Output
[...]

### claude-code-ecosystem Full Output
[...]

### documentation Full Output
[...]

### tech-debt-investigator Full Output
[...]
```

---

## Benefits

### 1. Comprehensive 360° Analysis

- **Structure**: Agent definition quality and compliance (claude-code-ecosystem)
- **Quality**: Prompt engineering and clarity (claude-code-ecosystem)
- **Efficiency**: Token density and optimization (documentation)
- **Maintainability**: Technical debt and consistency (tech-debt-investigator)

**Result**: No blind spots, all quality dimensions covered in single pass

### 2. Multi-Framework Evaluation

**6 Prompt Evaluation Frameworks** (claude-code-ecosystem):

1. Clarity & Specificity
2. Instruction Completeness
3. Context Provision
4. Output Format Specification
5. Anti-Pattern Detection
6. Role Definition Quality

**SQALE/SIG Technical Debt** (tech-debt-investigator):

- SQALE methodology for debt quantification
- SIG star rating for benchmarking
- 6-category debt breakdown

**Token Density Analysis** (documentation):

- Tokens per concept measurement
- Reference extraction opportunities
- Compression technique recommendations

**Result**: Deep, multi-perspective quality assessment using established frameworks

### 3. Parallel Execution Speed

**Sequential Approach**: 40+ minutes

- claude-code-ecosystem: 10 min
- claude-code-ecosystem: 12 min
- documentation: 8 min
- tech-debt-investigator: 10 min
- Total: 40 min

**Parallel Approach**: ~10 minutes

- All 4 agents execute simultaneously
- Orchestrator synthesis: 2-3 min
- Total: ~12 min

**Speedup**: 3-4x faster than sequential execution

### 4. Consistent Methodology

**Standard Suite Benefits**:

- Same agents for all agent reviews → comparable results
- Repeatable process → consistent quality bar
- Baseline metrics → track improvements over time
- Cross-agent benchmarking → identify outliers

**Example**:

- Agent A: Quality 85/100, Tokens 2500, Debt 45
- Agent B: Quality 72/100, Tokens 3800, Debt 68
- Agent C: Quality 90/100, Tokens 2200, Debt 38
→ Clear visibility into which agents need attention

### 5. Prioritized Actionability

**P1/P2/P3 Framework**:

- P1 (Critical): Immediate action, high ROI
- P2 (Strategic): Planned improvement, medium ROI
- P3 (Defer): Backlog, low priority

**Impact/Effort Matrix**:

```text
High Impact + Low Effort → P1 (Quick Wins)
High Impact + High Effort → P2 (Strategic)
Low Impact + Low Effort → P3 (Opportunistic)
Low Impact + High Effort → Avoid (unless strategic necessity)
```

**Result**: Clear roadmap, no ambiguity about what to do next

### 6. Cross-Agent Overlap Detection

**High-Priority Signal**:

- Issue found by 2+ agents → Cross-domain concern → P1 priority
- Similar recommendations from multiple agents → Validate and consolidate
- Conflicting recommendations → Trade-off analysis required

**Example**:

- claude-code-ecosystem: "Tool selection guidance unclear"
- claude-code-ecosystem: "Vague constraint in Tool Usage section"
→ OVERLAP >0.7 → Escalate to P1 → Consolidate: "Fix tool selection clarity"

### 7. Quantifiable Improvements

**Measurable Outcomes**:

- Token savings: Absolute count + percentage reduction
- Quality score: Before/after comparison (0-100 scale)
- Debt metrics: TDR, SQALE grade, SIG rating
- Effort estimates: Hours per recommendation, sprint capacity planning

**Result**: Objective progress tracking, ROI visibility, stakeholder communication

---

## Example Scenarios

### Scenario 1: New Agent Pre-Deployment Review

**Context**: New agent "api-integrator" created, needs validation before deployment

**Orchestrator Action**:

```markdown
User: "Review api-integrator agent before we deploy it"

Orchestrator:
"Launching Agent Analysis Suite for pre-deployment validation..."

Task(claude-code-ecosystem,
  "Validate .claude/agents/api-integrator.md structure and schema compliance.
   Check: Base pattern adherence, lifecycle completeness, boundary enforcement.")

Task(claude-code-ecosystem,
  "Evaluate prompt quality for api-integrator across 6 frameworks.
   Focus: API-specific instructions, error handling clarity, security guidance.")

Task(documentation,
  "Analyze token efficiency for api-integrator. Target: <3000 tokens.
   Identify: Verbose API examples, reference extraction opportunities.")

Task(tech-debt-investigator,
  "Pre-deployment debt scan for api-integrator. Block if: TDR >0.15 or debt_score <60.
   Focus: Documentation completeness, testing references, security compliance.")

"Synthesizing results. Deployment blocked if any P1 critical issues found."
```

**Expected Output**:

- Quality score with P1 blockers flagged
- Token count vs 3000 target
- Deployment recommendation (PASS/FAIL)
- P1 fixes required before deployment

### Scenario 2: Quarterly Agent Health Audit

**Context**: Quarterly review of all production agents, prioritize improvement work

**Orchestrator Action**:

```markdown
User: "Run health audit on all agents, generate improvement roadmap"

Orchestrator:
"Launching Agent Analysis Suite for quarterly health audit (32 agents)..."

[For each agent, launch 4-agent suite in parallel]
[Aggregate results across all agents]
[Generate comparative report + roadmap]

"Synthesis:
- 5 agents with P1 issues (quality <70)
- 12 agents with token optimization opportunities (>500 savings)
- 8 agents with high debt (TDR >0.15)
- Roadmap: 40h effort to address P1s, 80h for P2s"
```

**Expected Output**:

- Comparative quality dashboard (all 32 agents)
- Top 10 improvement priorities (sorted by ROI)
- Effort estimate for next quarter (sprints required)
- Trend analysis vs previous quarter

### Scenario 3: Agent Optimization Sprint

**Context**: Sprint dedicated to improving existing agent quality

**Orchestrator Action**:

```markdown
User: "Analyze debugger, development, and code-quality. Which needs most improvement?"

Orchestrator:
"Launching Agent Analysis Suite for comparative analysis (3 agents)..."

[Launch 4-agent suite for each agent in parallel = 12 total agents]
[Compare results across 3 target agents]
[Rank by improvement opportunity (Impact × Effort⁻¹)]

"Synthesis:
1. development: Quality 72, 650 tokens savings, Debt 68 → HIGH PRIORITY
2. code-quality: Quality 78, 380 tokens savings, Debt 55 → MEDIUM PRIORITY
3. debugger: Quality 85, 150 tokens savings, Debt 42 → LOW PRIORITY

Recommendation: Focus sprint on development (8-10h effort, highest ROI)"
```

**Expected Output**:

- Comparative analysis across 3 agents
- Ranked improvement opportunities
- Sprint capacity planning recommendation
- Effort estimates per agent

### Scenario 4: Post-Implementation Validation

**Context**: Agent improvements completed, validate quality improvement

**Orchestrator Action**:

```markdown
User: "Re-analyze planning after optimizations. Compare to baseline from 2025-10-15."

Orchestrator:
"Launching Agent Analysis Suite for post-implementation validation..."

Task(claude-code-ecosystem, "Validate planning improvements vs baseline...")
Task(claude-code-ecosystem, "Measure prompt quality improvement vs baseline...")
Task(documentation, "Calculate token savings achieved vs 450 target...")
Task(tech-debt-investigator, "Assess debt reduction vs TDR 0.12 baseline...")

"Comparing to baseline from docs/01-planning/reports/2025-10-15-planning-analysis.md"
```

**Expected Output**:

- Before/after comparison (quality, tokens, debt)
- Target achievement (goals met vs missed)
- Regression detection (any quality degradation)
- Next iteration recommendations

### Scenario 5: Incident Post-Mortem

**Context**: Agent produced low-quality output, investigate root cause

**Orchestrator Action**:

```markdown
User: "Researcher-lead failed task #42 with vague research questions. Investigate why."

Orchestrator:
"Launching Agent Analysis Suite for incident post-mortem on researcher-lead..."

Task(claude-code-ecosystem,
  "Analyze researcher-lead structure. Focus: Research question generation guidance.")

Task(claude-code-ecosystem,
  "Evaluate researcher-lead prompt. Focus: Specificity in research planning section.")

Task(documentation,
  "Check researcher-lead for verbose/unclear instructions causing misunderstanding.")

Task(tech-debt-investigator,
  "Assess researcher-lead documentation debt. Focus: Examples, validation, edge cases.")

"Root cause analysis: Identify prompt deficiencies causing vague research questions."
```

**Expected Output**:

- Root cause identification (which agent sections failed)
- Specific prompt deficiencies causing issue
- Remediation recommendations (P1 fixes to prevent recurrence)
- Validation strategy to test fixes

---

## Related Documentation

### Core Frameworks

- **Multi-Agent Synthesis**: `.claude/docs/00-core/synthesis-and-recommendation-framework.md` - Overlap detection, weighted scoring, conflict resolution
- **OODA Loop**: `.claude/docs/00-core/ooda-loop-framework.md` - OBSERVE/ORIENT/DECIDE/ACT workflow integration
- **Technical Debt**: `.claude/docs/00-core/technical-debt-frameworks.md` - SQALE/SIG methodologies, TDR calculation

### Workflow Patterns

- **Orchestrator Workflow**: `.claude/docs/03-workflows/orchestrator-workflow.md` - Agent selection, delegation patterns, parallel execution
- **Planning Workflow**: `.claude/docs/03-workflows/planning-workflow-patterns.md` - Multi-phase workflows, optimization strategies
- **Validation Workflow**: `.claude/docs/03-workflows/validation-workflows.md` - Quality gates, acceptance criteria

### Agent Standards

- **Agent Standards Extended**: `.claude/docs/01-guides/agents/agent-standards-extended.md` - Comprehensive agent design standards, lifecycle, output formats
- **Agent Selection Guide**: `.claude/docs/01-guides/agents/agent-selection-guide.md` - 7 frameworks for agent selection, Quick Matrix
- **Base Agent Pattern**: `.claude/docs/01-guides/agents/base-agent-pattern.md` - Universal agent structure and inheritance

### Performance & Efficiency

- **Tool Parallelization**: `.claude/docs/01-guides/performance/tool-parallelization-patterns.md` - Parallel execution limits, batching strategies
- **Token Density**: `docs/04-guides/documentation/token-density-techniques.md` - Compression techniques, reference extraction

### Agent-Specific Documentation

- **claude-code-ecosystem**: `.claude/agents/claude-code-ecosystem.md` - Agent definition analysis specialist
- **claude-code-ecosystem**: `.claude/agents/claude-code-ecosystem.md` - Prompt quality assessment frameworks
- **documentation**: `.claude/agents/documentation.md` - Token efficiency and reference extraction
- **tech-debt-investigator**: `.claude/agents/tech-debt-investigator.md` - SQALE/SIG debt analysis

### Quality Assurance

- **Code Review Guidelines**: `docs/04-guides/code-review/coding-guidelines.md` - Code quality standards
- **Documentation Standards**: `docs/DOCS-MANAGEMENT.md` - Documentation structure and naming conventions
- **Schema Validation**: `.claude/docs/schemas/*.schema.json` - Output validation contracts

---

## Quick Reference Card

```yaml
# Agent Analysis Suite Quick Reference

trigger:
  - Agent quality assessment
  - Prompt optimization
  - Documentation review
  - Pre-deployment validation
  - Quarterly health audit

core_agents:
  - claude-code-ecosystem         # Structure & compliance
  - claude-code-ecosystem        # Prompt quality (6 frameworks)
  - documentation # Token efficiency
  - tech-debt-investigator  # Documentation debt (SQALE/SIG)

optional_agents:
  - context-optimizer       # If 3+ agents or CLAUDE.md
  - documentation          # If link validation needed
  - code-quality   # If Python tools present

launch_pattern: "Single message, 4 Task calls in parallel"

synthesis_trigger: "3+ agents with overlap >0.7"

expected_duration: "~10 minutes (parallel) vs 40+ min (sequential)"

output_format:
  - Executive summary (2-3 sentences)
  - Overall quality score (0-100)
  - Top 3 findings (P1 priority)
  - Consolidated recommendations (P1/P2/P3)
  - Implementation roadmap (sprint planning)
  - Effort estimates (hours)

benefits:
  - 360° comprehensive analysis
  - 6+ evaluation frameworks
  - 3-4x faster than sequential
  - Consistent methodology
  - Prioritized actionability
  - Quantifiable improvements

metrics:
  - Quality score: 0-100 (target: 85+)
  - Token count: current vs target
  - Debt score: 0-100 (target: 70+)
  - TDR: ratio (target: <0.10)
  - SQALE grade: A-E (target: B+)
  - SIG rating: 1-5 stars (target: 4+)
```

---

## Validation Checklist

Before launching Agent Analysis Suite:

**Pre-Flight**:

- [ ] Target agent file path confirmed (`.claude/agents/*.md`)
- [ ] Core 4 agents available (claude-code-ecosystem, claude-code-ecosystem, documentation, tech-debt-investigator)
- [ ] Optional agents evaluated (context-optimizer, documentation, code-quality)
- [ ] Baseline data available (if comparative analysis)
- [ ] Synthesis framework reference loaded (`.claude/docs/00-core/synthesis-and-recommendation-framework.md`)

**Launch**:

- [ ] Single message with multiple Task calls (not sequential)
- [ ] Each agent receives specific instructions and file path
- [ ] Parallel execution confirmed (no dependencies between agents)
- [ ] Maximum 7 agents total (4 core + 3 optional)

**Post-Completion**:

- [ ] All agents returned SUCCESS or documented FAILURE reasons
- [ ] Overlap detection performed (similarity >0.7)
- [ ] Synthesis framework applied (if 3+ agents with overlap)
- [ ] Consolidated recommendations prioritized (P1/P2/P3)
- [ ] Implementation roadmap generated with effort estimates
- [ ] Metrics summary included (quality, tokens, debt)

**Delivery**:

- [ ] Executive summary clear and actionable (2-3 sentences)
- [ ] Overall quality score calculated (weighted average)
- [ ] Top 3 findings highlighted (highest priority)
- [ ] Next steps documented (immediate actions + planning)
- [ ] Report saved to appropriate location (docs/01-planning/reports/ or agent-specific directory)

---

**Protocol Version**: 1.0
**Last Updated**: 2025-11-12
**Maintained By**: Orchestrator + Agent Analysis Suite
**Review Frequency**: Quarterly or when agent standards updated
