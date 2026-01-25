# Delegation Patterns (v3)

Exact Task() call syntax for all 5 agents in the `/analyze-agent` command.

---

## Overview

**CRITICAL**: Launch all 4 Phase 1 agents in a **single message** with 4 Task calls (parallel execution).

Phase 2 (contingency-planner) runs sequentially AFTER Phase 1 merging.

---

## Variable Substitution

Variables used in Task() calls:

| Variable | Description | Example |
|----------|-------------|---------|
| `{resolved_path}` | Full absolute path to target agent | `C:/Users/.../agents/debugger/debugger.md` |
| `{merged_findings_summary}` | JSON summary from Phase 3 merge | `{"critical_count": 2, "findings": [...]}` |
| `{agent_name}` | Name of target agent (from frontmatter) | `debugger` |

---

## Parallel Launch Pattern (Phase 1)

**CRITICAL**: All 4 Discovery agents MUST be launched in a SINGLE message.

```xml
<parallel-launch>
Task(claude-code-ecosystem, "...")
Task(claude-code-ecosystem, "...")
Task(documentation, "...")
Task(tech-debt-investigator, "...")
</parallel-launch>
```

This enables parallel execution. Sequential launches waste time.

---

## Complete Task() Syntax

### 1. claude-code-ecosystem Task()

```markdown
Task(claude-code-ecosystem, "
  Analyze agent at {resolved_path} for structure and integration.
  
  EVALUATE:
  1. 9-criterion quality matrix:
     - Identity clarity (name, description, purpose)
     - Workflow definition (phases, gates, transitions)
     - Tool specification (allowed-tools, usage patterns)
     - Error handling (codes, recovery, fallbacks)
     - Output schema (SUCCESS/FAILURE states)
     - Integration points (upstream/downstream)
     - Documentation references (knowledge base)
     - Anti-patterns (NEVER DO list)
     - Good patterns (ALWAYS DO list)
  
  2. Frontmatter validation:
     - Required: name, description, allowed-tools
     - Optional: model, argument-hint
  
  3. Schema compliance:
     - Extends base-agent.schema.json
     - agent_specific_output defined
     - failure_details defined
  
  4. Integration requirements (7 checks):
     - Trigger keywords defined
     - Upstream dependencies documented
     - Downstream consumers documented
     - CLAUDE.md compatibility
     - Orchestrator delegation pattern
     - Error propagation
     - Output consumption
  
  OUTPUT JSON:
  {
    structure_score: 0-100,
    criteria_scores: {criterion_name: 0-100},
    frontmatter_valid: bool,
    frontmatter_issues: [string],
    schema_compliant: bool,
    schema_issues: [string],
    integration_status: PASS|PARTIAL|FAIL,
    integration_checks: {check_name: bool},
    findings: [{
      severity: CRITICAL|HIGH|MEDIUM|LOW,
      location: string (file:line),
      issue: string,
      recommendation: string,
      effort: LOW|MEDIUM|HIGH
    }],
    confidence: 0.0-1.0
  }
")
```

---

### 2. claude-code-ecosystem Task()

```markdown
Task(claude-code-ecosystem, "
  Evaluate agent at {resolved_path} across 7 quality frameworks.
  
  FRAMEWORKS:
  F1: Structural Quality (16 criteria)
      - Identity section, workflow section, delegation section
      - Error handling, output states, anti-patterns
  
  F2: Prompt Engineering
      - Clarity, specificity, examples
      - Hallucination prevention, constraints
      - XML structure for AI parsing
  
  F3: Token Optimization
      - Current token count
      - Redundancy detection
      - Compression opportunities
      - Reference vs inline balance
  
  F4: Testing Strategy
      - Testability of workflow
      - Validation checkpoints
      - Edge case coverage
  
  F5: Progressive Disclosure
      - Information hierarchy
      - Critical info frontloading
      - Detail depth appropriate
  
  F6: Token Density
      - Filler word ratio
      - Passive voice usage
      - Information per token
  
  F7: Framework Alignment
      - OODA integration
      - Thinking framework usage
      - Phase methodology mapping
  
  DETECT anti-patterns:
  - Full path doc references
  - Truncated examples
  - Missing schema reference
  - No termination rules
  - Decorative content
  
  OUTPUT JSON:
  {
    overall_grade: A|B|C|D|F,
    overall_score: 0-100,
    framework_scores: {
      F1_structural: 0-100,
      F2_engineering: 0-100,
      F3_token: 0-100,
      F4_testing: 0-100,
      F5_disclosure: 0-100,
      F6_density: 0-100,
      F7_alignment: 0-100
    },
    anti_patterns: [{
      name: string,
      location: string,
      severity: CRITICAL|HIGH|MEDIUM|LOW,
      tokens_wasted: int
    }],
    findings: [{
      severity: CRITICAL|HIGH|MEDIUM|LOW,
      location: string,
      issue: string,
      recommendation: string,
      effort: LOW|MEDIUM|HIGH
    }],
    confidence: 0.0-1.0
  }
")
```

---

### 3. documentation Task()

```markdown
Task(documentation, "
  Analyze agent at {resolved_path} for token efficiency.
  
  ANALYZE:
  1. Token count by section
     - Frontmatter, identity, workflow, delegation, errors, output
  
  2. Redundancy detection
     - Inline content duplicating external docs
     - Repeated patterns within file
     - Cross-file duplication
  
  3. Compression opportunities
     - Sections reducible by 50%+
     - Content convertible to references
     - Verbose patterns to compress
  
  4. Reference vs inline decisions
     - What should be referenced (details)
     - What should be inlined (critical execution)
  
  5. Anti-pattern detection (6 types)
     - Full path references
     - Duplicate content
     - Verbose explanations
     - Decorative elements
     - Outdated references
     - Missing references
  
  OUTPUT JSON:
  {
    current_tokens: int,
    token_breakdown: {section_name: int},
    optimized_tokens: int,
    savings_percentage: float,
    redundancy_map: [{
      inline_location: string,
      external_doc: string,
      overlap_percentage: float,
      tokens_wasted: int
    }],
    compression_opportunities: [{
      section: string,
      current_tokens: int,
      potential_tokens: int,
      strategy: string
    }],
    anti_patterns: [{
      type: string,
      location: string,
      tokens_wasted: int,
      fix: string
    }],
    findings: [{
      severity: CRITICAL|HIGH|MEDIUM|LOW,
      location: string,
      issue: string,
      recommendation: string,
      effort: LOW|MEDIUM|HIGH
    }],
    confidence: 0.0-1.0
  }
")
```

---

### 4. tech-debt-investigator Task()

```markdown
Task(tech-debt-investigator, "
  Assess documentation debt for agent at {resolved_path}.
  
  APPLY METHODOLOGIES:
  1. SQALE (6 categories, weighted)
     - Code Quality (40%)
     - Architecture (15%)
     - Testing (20%)
     - Documentation (10%)
     - Infrastructure (10%)
     - Design (5%)
  
  2. SIG Maintainability Model
     - Volume, complexity, duplication, unit size
  
  3. Dependency Risk Assessment
     - Direct dependencies (agents, docs, scripts)
     - Stability rating per dependency
     - Risk level per dependency
  
  4. Knowledge Debt Detection
     - Stale references
     - Outdated patterns
     - Version drift
     - Broken links
  
  5. Hotspot Analysis
     - Churn × Complexity scoring
     - High-change areas
  
  OUTPUT JSON:
  {
    debt_score: 0-100,
    debt_classification: Low|Moderate|High|Critical,
    tdr_ratio: float,
    sqale_grade: A|B|C|D|E,
    sig_stars: 1-5,
    category_breakdown: {
      code_quality: {score: 0-5, issues: []},
      architecture: {score: 0-5, issues: []},
      testing: {score: 0-5, issues: []},
      documentation: {score: 0-5, issues: []},
      infrastructure: {score: 0-5, issues: []},
      design: {score: 0-5, issues: []}
    },
    dependencies: [{
      name: string,
      type: agent|doc|script,
      path: string,
      stability: HIGH|MEDIUM|LOW,
      risk_level: HIGH|MEDIUM|LOW
    }],
    knowledge_debt: [{
      type: stale|outdated|drift|broken,
      location: string,
      description: string
    }],
    hotspots: [{
      location: string,
      churn_score: float,
      complexity_score: float,
      combined_score: float
    }],
    findings: [{
      severity: CRITICAL|HIGH|MEDIUM|LOW,
      location: string,
      issue: string,
      recommendation: string,
      effort: LOW|MEDIUM|HIGH
    }],
    confidence: 0.0-1.0
  }
")
```

---

### 5. contingency-planner Task() (Phase 2 - Sequential)

```markdown
Task(contingency-planner, "
  Conduct pre-mortem analysis for agent at {resolved_path}.
  
  CONTEXT from Phase 1-3:
  {merged_findings_summary}
  
  ASSUME: This agent will fail in production. Brainstorm WHY.
  
  ANALYZE failure modes using schema-aligned failure_type values:
  
  Technical failure_type enum (from contingency-planner.schema.json):
  - agent_timeout, schema_validation_fail, resource_exhaustion
  - boundary_violation, dependency_failure, tool_error
  - context_insufficient, rate_limit_exceeded, permission_denied, data_corruption
  
  Map to conceptual categories for analysis:
  - INPUT: context_insufficient, schema_validation_fail, data_corruption
  - EXECUTION: agent_timeout, resource_exhaustion, tool_error, rate_limit_exceeded
  - OUTPUT: schema_validation_fail, data_corruption
  - INTEGRATION: dependency_failure, boundary_violation
  - EVOLUTION: context_insufficient (stale patterns), dependency_failure (upstream changes)
  
  Brainstorm questions per category:
  
  1. INPUT (context_insufficient, schema_validation_fail, data_corruption)
     - What invalid inputs cause problems?
     - What edge cases aren't handled?
     - What format assumptions might be wrong?
  
  2. EXECUTION (agent_timeout, resource_exhaustion, tool_error, rate_limit_exceeded)
     - What could cause hangs or timeouts?
     - What external dependencies might fail?
     - What resource limits might be hit?
  
  3. OUTPUT (schema_validation_fail, data_corruption)
     - What wrong outputs could be produced?
     - What would cause misleading recommendations?
     - What schema violations are possible?
  
  4. INTEGRATION (dependency_failure, boundary_violation)
     - What breaks if output changes?
     - Who consumes this agent's output?
     - What upstream changes could break this?
  
  5. EVOLUTION (context_insufficient, dependency_failure)
     - What will make this stale in 6 months?
     - What ecosystem changes could invalidate assumptions?
     - What maintenance burden is being created?
  
  FOR EACH failure mode provide:
  - ID: FM-{failure_type}-{NUMBER}
  - Description
  - Likelihood: HIGH/MEDIUM/LOW
  - Impact: HIGH/MEDIUM/LOW
  - Root Cause
  - Prevention Strategy
  - Detection Method
  
  OUTPUT JSON:
  {
    failure_modes: [{
      id: string,
      failure_type: "agent_timeout|schema_validation_fail|resource_exhaustion|boundary_violation|dependency_failure|tool_error|context_insufficient|rate_limit_exceeded|permission_denied|data_corruption",
      conceptual_category: "INPUT|EXECUTION|OUTPUT|INTEGRATION|EVOLUTION",
      description: string,
      likelihood: HIGH|MEDIUM|LOW,
      impact: HIGH|MEDIUM|LOW,
      root_cause: string,
      prevention: string,
      detection: string
    }],
    risk_matrix: {
      critical: [ids],
      high: [ids],
      medium: [ids],
      low: [ids]
    },
    resilience_score: 0.0-1.0,
    top_3_risks: [{id, mitigation_priority}],
    confidence: 0.0-1.0
  }
")
```

---

## Execution Flow Summary

```
Phase 1: PARALLEL (single message)
├── claude-code-ecosystem      → structure_score, integration_status
├── claude-code-ecosystem     → overall_grade, framework_scores
├── documentation → current_tokens, savings_percentage
└── tech-debt-investigator  → debt_score, sqale_grade

Phase 2: MERGE
└── Consolidate all findings into merged_findings_summary

Phase 3: SEQUENTIAL (after merge)
└── contingency-planner  → failure_modes, resilience_score
```

---

## Notes

- **No truncation**: All Task() calls above are COMPLETE - copy verbatim
- **JSON comments**: Output schemas use simplified notation; actual output is valid JSON
- **Variable resolution**: Orchestrator replaces `{variables}` before delegation
- **Confidence threshold**: Agents with confidence < 0.7 trigger re-analysis
