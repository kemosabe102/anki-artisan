# Review Methodology

Detailed OODA loop integration, review operating procedures, and quality gates for the technical-pm agent.

---

## OODA Loop Integration

### OBSERVE Phase: Input Discovery & Context Gathering

**Primary Actions**:
1. **File Discovery**: Use Glob to locate SPEC.md and plan files in specification directory
2. **Content Analysis**: Read all plan files to extract business context
3. **Framework Research**: Use Context7/WebSearch to gather business analysis methodologies
4. **Context Validation**: Verify all required inputs are accessible

**Information Sources**:
- Target plan files (SPEC.md, PLAN.md, component plans)
- Knowledge base frameworks (cost-analysis-framework.md, risk-assessment-matrix.md, quality-scoring-algorithms.md)
- Business value methodologies (ROI calculation, strategic alignment patterns)

**Context_Quality Assessment**:
- Formula: (Domain x 0.4) + (Pattern x 0.3) + (Dependency x 0.2) + (Risk x 0.1)
- Domain: Understanding of business review requirements and plan structure
- Pattern: Familiarity with business alignment patterns and NFR frameworks
- Dependency: Knowledge of framework integration requirements
- Risk: Awareness of business impact from incomplete analysis

**Quality Gate**: Context_Quality >= 0.5 required to proceed to ORIENT phase

---

### ORIENT Phase: Business Alignment Analysis

**Analysis Dimensions**:
1. **Business Goals Alignment**: Map plan components to SPEC.md business objectives (score 0.0-1.0)
2. **NFR Coverage Assessment**: Evaluate performance, security, operational requirements (low/medium/high)
3. **Requirements Traceability**: Calculate FR-ID coverage percentage and gap analysis
4. **Placeholder Census**: Identify and prioritize business placeholder patterns

**Framework Application**:
- Cost-benefit analysis validation against $100/month budget constraint
- Risk assessment using P x I x E scoring methodology
- Timeline realism evaluation using quality scoring algorithms
- Code reuse ROI calculation (development time savings)

**Pattern Recognition**:
- Business placeholder patterns (critical/important/nice-to-have)
- Missing business context indicators
- Strategic misalignment signals
- NFR coverage gaps

**Output**: Structured analysis findings ready for recommendation generation

---

### DECIDE Phase: Recommendation Prioritization

**Decision Criteria**:
1. **Business Impact Scoring**: Assess impact of each gap on business value delivery
2. **Priority Classification**: Categorize recommendations as P1 (critical), P2 (important), P3 (nice-to-have)
3. **Effort Estimation**: Calculate enhancement effort for each recommendation
4. **Risk Assessment**: Evaluate implementation risks and mitigation strategies

**Prioritization Formula**:
```
Priority = (Business_Impact x 0.5) + (Strategic_Alignment x 0.3) + (Feasibility x 0.2)
```

| Priority | Score Range | Description |
|----------|-------------|-------------|
| P1 (critical) | >= 0.75 | Blocks business value delivery |
| P2 (important) | 0.50-0.74 | Enhances business value |
| P3 (nice-to-have) | < 0.50 | Incremental improvements |

**Quality Thresholds**:
- Business goals alignment score: Target >= 0.75 (escalate if < 0.50)
- NFR coverage: Target "high" across all categories (escalate if "low")
- Traceability coverage: Target >= 70% FR-ID mapping (escalate if < 50%)

---

### ACT Phase: Report Generation & Handoff

**Deliverables**:
1. **Business Review Report**: Schema-compliant comprehensive analysis
2. **Business Edit Plan**: Actionable recommendations with patterns, replacements, priorities
3. **Zero Mutation Verification**: Confirm no files were modified during review

**Validation Protocol**:
- Schema validation against `schemas/technical-pm.schema.json`
- Framework integration checklist completion
- Recommendation quality verification (clarity, actionability, rationale)

**Handoff Preparation**:
- Format edit plans for enhancement agent consumption
- Document framework compliance findings
- Provide clear success criteria for enhancements

---

## Review Operating Procedures

### Phase 1: Input Analysis & Validation
1. Use Glob to discover plan files in specification directory
2. Use Read to analyze SPEC.md and all plan files
3. Verify all required inputs are available and accessible
4. Determine review scope based on available files and context

### Phase 2: Business Alignment Assessment
1. Extract business goals, user needs, success criteria from SPEC.md
2. Map plan components to business objectives
3. Identify missing business context or misaligned components
4. Calculate business goals alignment score (0.0-1.0)

### Phase 3: NFR Framework Evaluation
1. Evaluate performance, security, operational, integration requirements
2. Identify business risks from technical decisions
3. Rate NFR coverage as low/medium/high per category
4. Recommend risk mitigation strategies

### Phase 4: Traceability Analysis
1. Count functional requirement identifiers (FR-IDs) in plans
2. Verify requirement traceability to business goals
3. Calculate percentage of traced requirements
4. List unmapped or poorly traced requirements

### Phase 5: Placeholder Census & Prioritization
1. Identify business placeholder patterns across files
2. Count placeholders by file and priority category
3. Evaluate business impact of each placeholder category
4. Classify as critical/important/nice-to-have

### Phase 6: Report Generation
1. Generate Business Review Report conforming to schema
2. Create Business Edit Plan for enhancement agents
3. Verify reports conform to `schemas/technical-pm.schema.json`
4. Confirm zero files were modified during review

---

## Success/Failure Criteria

### SUCCESS Status Requirements

All of the following must be true:
- [ ] Business Review Report generated and schema-valid
- [ ] Business Edit Plan created for enhancement agents
- [ ] Zero file mutations verified
- [ ] All analysis dimensions completed (alignment, NFR, traceability, placeholders)
- [ ] Clear, actionable recommendations with rationale provided
- [ ] Framework integration validated:
  - [ ] Cost-benefit validates against $100/month constraint
  - [ ] Risk assessments use P x I x E scoring
  - [ ] Timeline realism assessed
  - [ ] Framework references cited

### FAILURE Status Indicators

Return FAILURE if ANY of these occur:
- Required input files (SPEC.md or plan files) missing or unreadable
- Business Review Report generation fails or schema validation fails
- Any file mutation attempt detected
- Critical analysis steps skipped or incomplete
- Recommendations lack sufficient detail or rationale

---

## Escalation Path

### Priority 1 (Immediate - Blocks Progress)
- Missing critical input files (SPEC.md not found)
- File mutation attempt detected (security violation)
- Schema validation failure after retry
- Business alignment score < 0.30 (severe misalignment)

### Priority 2 (High - Requires Attention)
- Business goals alignment score < 0.50
- NFR coverage "low" across 3+ categories
- Traceability coverage < 50%
- Budget overruns > 150% of $100/month constraint

### Priority 3 (Medium - Advisory)
- Context_Quality < 0.5 with missing framework guides
- Timeline realism concerns (complexity vs estimation mismatch > 40%)
- Code reuse opportunities with > 50% development time savings
- Progressive disclosure violations in plan structure

### Escalation Format
```json
{
  "escalation_level": "P1|P2|P3",
  "trigger": "Brief description",
  "business_impact": "Impact if unresolved",
  "recommended_action": "Specific action for orchestrator",
  "context": {
    "affected_files": ["list"],
    "metrics": {"alignment_score": 0.0-1.0, "traceability_coverage": "0-100%"}
  }
}
```

---

## Edge Cases & Handling

### Missing SPEC.md
**Detection**: `Glob("**/SPEC.md")` returns empty
**Action**: FAILURE with `failure_type: missing_spec`
**Guidance**: "Cannot proceed without SPEC.md. Ensure specification exists at `docs/01-planning/specifications/XXX-feature/SPEC.md`"

### Partial PLAN Files
**Detection**: PLAN file exists but missing required sections (Business Goals, NFRs, FR-IDs)
**Action**: WARN, proceed with reduced scoring
**Report**: Flag missing sections, calculate partial scores, note limitations in output

### Conflicting Business Goals
**Detection**: Multiple goals contradict (e.g., "minimize cost" vs "maximize features")
**Action**: Flag for human review
**Report**: List conflicts with evidence, do NOT resolve - escalate with P2 priority

### No NFR Section in SPEC
**Detection**: SPEC lacks explicit NFR definitions
**Action**: Derive from industry standards via `mcp__perplexity__search`
**Report**: Note "NFRs derived from industry standards" with source citations, flag as P2 for explicit definition

### Budget Undefined
**Detection**: No cost/budget constraints in SPEC or PLAN files
**Action**: Skip cost-benefit analysis, note limitation
**Report**: "Cost-benefit analysis skipped - no budget constraints defined. Recommend defining $X/month operational limit."

### Multiple SPECs in Path
**Detection**: `Glob` returns 2+ SPEC.md files
**Action**: Review ALL specs, aggregate findings
**Report**: Separate analysis per SPEC, combined recommendations, note potential scope conflicts

### Empty Plan Files
**Detection**: PLAN file exists but is empty or <10 lines
**Action**: FAILURE with specific file list
**Report**: `failure_type: validation_error`, list empty files, suggest orchestrator verify file generation

### Plan Count Exceeds Threshold
**Detection**: >10 PLAN files discovered
**Action**: WARN about extended review time, proceed
**Report**: Estimated review time = plan_count x 5 min SLO, recommend batching if >20 files
