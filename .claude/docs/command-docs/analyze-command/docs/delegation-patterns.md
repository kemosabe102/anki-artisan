# Delegation Patterns

Exact Task() call syntax for the `/analyze-command` workflow.

**Version**: 1.0.0 | **Last Updated**: 2025-12-21

---

## Overview

**CRITICAL**: Launch all 4 Phase 1 agents in a **single message** with 4 Task calls (parallel execution).

Phase 4 (contingency-planner) runs sequentially AFTER Phase 3 synthesis.
Phase 8 (SCAMPER) runs optionally after Phase 6 report generation.

---

## Variable Substitution

| Variable | Description | Example |
|----------|-------------|---------|
| `{resolved_path}` | Full absolute path to command | `C:/.../.claude/commands/git.md` |
| `{command_name}` | Name of command (from frontmatter) | `git` |
| `{merged_findings_summary}` | JSON summary from P3 | `{"critical_count": 2, ...}` |
| `{phase1_scores}` | Aggregated P1 scores | `{"workflow": 85, ...}` |

---

## P1: Parallel Launch Pattern

**CRITICAL**: All 4 agents MUST be launched in a SINGLE message.

```xml
<parallel-launch>
Task(claude-code-ecosystem, "Structure analysis...")
Task(claude-code-ecosystem, "Prompt quality analysis...")
Task(documentation, "Token efficiency analysis...")
Task(tech-debt-investigator, "Debt analysis...")
</parallel-launch>
```

---

## P1 Agent 1: Structure Analysis

```markdown
Task(claude-code-ecosystem, "
  Analyze command at {resolved_path} for structure and workflow.
  
  EVALUATE:
  1. Workflow phase definition:
     - Phases clearly defined (P0, P1, P2, etc.)
     - Gate criteria for each phase
     - Phase dependencies documented
     - Timeout values specified
  
  2. Delegation pattern completeness:
     - Task() syntax documented
     - Agent assignments clear
     - Boundaries defined (what NOT to do)
     - Parallelization opportunities identified
  
  3. Error handling coverage:
     - Error codes defined
     - Recovery strategies documented
     - Fallback paths specified
     - Escalation triggers defined
  
  4. Output state definition:
     - SUCCESS state schema
     - FAILURE state schema
     - Partial success handling
     - Timeout handling
  
  5. Integration points:
     - Upstream commands (what triggers this)
     - Downstream commands (what this triggers)
     - Agent dependencies
     - Skill dependencies
  
  6. Quality matrix (9 criteria, 0-5 scale):
     - Workflow clarity
     - Delegation completeness
     - Error coverage
     - Output definition
     - Integration documentation
     - OODA alignment
     - Progressive disclosure
     - Token efficiency
     - Maintainability
  
  OUTPUT JSON:
  {
    workflow_score: 0-100,
    delegation_score: 0-100,
    error_handling_score: 0-100,
    output_score: 0-100,
    integration_score: 0-100,
    quality_matrix: {criterion: 0-5},
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

## P1 Agent 2: Prompt Quality Analysis

```markdown
Task(claude-code-ecosystem, "
  Evaluate command at {resolved_path} for prompt quality.
  
  FRAMEWORKS:
  F1: Structural Quality (16 criteria)
      - Clear purpose statement
      - Defined phases
      - Explicit boundaries
      - Error handling
      - Output specification
  
  F2: Prompt Engineering (6 principles)
      - Clarity of instructions
      - Specificity of requirements
      - Examples provided
      - Constraint definition
      - Hallucination prevention
      - XML structure for parsing
  
  F3: Token Optimization
      - Current token count
      - Redundancy detection
      - Compression opportunities
      - Reference vs inline balance
  
  F4: Testing Strategy
      - Workflow testability
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

## P1 Agent 3: Token Efficiency Analysis

```markdown
Task(documentation, "
  Analyze command at {resolved_path} for token efficiency.
  
  ANALYZE:
  1. Token count by section:
     - Frontmatter
     - Purpose/overview
     - Workflow phases
     - Delegation patterns
     - Error handling
     - Output specification
  
  2. Redundancy detection:
     - Inline content duplicating docs
     - Repeated patterns within file
     - Cross-file duplication
  
  3. Compression opportunities:
     - Sections reducible by 50%+
     - Content convertible to references
     - Verbose patterns to compress
  
  4. Reference vs inline decisions:
     - What should be referenced (details)
     - What should be inlined (critical execution)
  
  5. Anti-pattern detection (6 types):
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

## P1 Agent 4: Debt Analysis

```markdown
Task(tech-debt-investigator, "
  Assess documentation debt for command at {resolved_path}.
  
  APPLY METHODOLOGIES:
  1. SQALE (6 categories, weighted):
     - Code Quality (40%)
     - Architecture (15%)
     - Testing (20%)
     - Documentation (10%)
     - Infrastructure (10%)
     - Design (5%)
  
  2. SIG Maintainability Model:
     - Volume, complexity, duplication, unit size
  
  3. Dependency Risk Assessment:
     - Agent dependencies
     - Skill dependencies
     - Doc dependencies
     - Stability rating per dependency
  
  4. Knowledge Debt Detection:
     - Stale references
     - Outdated patterns
     - Version drift
     - Broken links
  
  5. Hotspot Analysis:
     - Churn x Complexity scoring
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
      type: agent|skill|doc,
      path: string,
      stability: HIGH|MEDIUM|LOW,
      risk_level: HIGH|MEDIUM|LOW
    }],
    knowledge_debt: [{
      type: stale|outdated|drift|broken,
      location: string,
      description: string
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

## P4: Pre-Mortem Analysis

```markdown
Task(contingency-planner, "
  Conduct pre-mortem analysis for command at {resolved_path}.
  
  CONTEXT from Phase 1-3:
  {merged_findings_summary}
  
  ASSUME: This command will fail in production. Brainstorm WHY.
  
  ANALYZE 5 failure categories:
  
  1. INPUT FAILURES:
     - Invalid arguments (missing, malformed)
     - Missing files (paths don't exist)
     - Malformed paths (Windows vs Unix)
     - Encoding issues (non-UTF8)
  
  2. EXECUTION FAILURES:
     - Agent timeout (agents don't respond)
     - Tool unavailable (MCP tools missing)
     - Skill not found (skill dependencies)
     - Resource exhaustion (memory, API limits)
  
  3. WORKFLOW FAILURES:
     - Step ordering errors (phase dependency violations)
     - Parallelization conflicts (race conditions)
     - Missing gates (no validation between phases)
     - Timeout cascade (one timeout triggers others)
  
  4. OUTPUT FAILURES:
     - Schema violations (output doesn't match schema)
     - Truncated output (incomplete results)
     - Wrong format (unexpected structure)
     - Missing fields (required fields absent)
  
  5. INTEGRATION FAILURES:
     - Orchestrator mismatch (command not registered)
     - Registry inconsistency (metadata out of sync)
     - Version drift (dependencies updated)
     - Permission issues (scope violations)
  
  FOR EACH failure mode provide:
  - failure_id: FM-{category}-{number}
  - description: What fails
  - likelihood: LOW|MEDIUM|HIGH
  - impact: LOW|MEDIUM|HIGH
  - root_cause: Why it happens
  - prevention: How to prevent
  - detection: How to detect early
  
  OUTPUT JSON:
  {
    failure_modes: [{
      failure_id: string,
      category: INPUT|EXECUTION|WORKFLOW|OUTPUT|INTEGRATION,
      description: string,
      likelihood: LOW|MEDIUM|HIGH,
      impact: LOW|MEDIUM|HIGH,
      risk_score: 0.0-1.0,
      root_cause: string,
      prevention: string,
      detection: string
    }],
    risk_matrix: {
      critical: [failure_ids],
      high: [failure_ids],
      medium: [failure_ids],
      low: [failure_ids]
    },
    resilience_score: 0.0-1.0,
    top_3_risks: [{
      failure_id: string,
      mitigation_priority: P1|P2|P3
    }],
    confidence: 0.0-1.0
  }
")
```

---

## P7: Delegation Routing Matrix

| Finding Type | Target Agent | Trigger Condition |
|--------------|--------------|-------------------|
| Workflow issues | `workflow` | workflow_score < 70 |
| Delegation gaps | `claude-code-ecosystem` | delegation_score < 70 |
| Token bloat | `doc-reference-optimizer` | savings_percentage > 30% |
| Integration failures | `claude-code-ecosystem` | integration_score < 60 |
| Knowledge debt | `doc-librarian` | debt_classification == Critical |
| Schema violations | `spec-reviewer` | schema issues detected |

### Delegation Prompt Template

```markdown
Task({target_agent}, "
  Address findings from command analysis of {command_name}.
  
  FINDING:
  {finding_summary}
  
  CONTEXT:
  Command path: {resolved_path}
  Current score: {dimension_score}
  
  SCOPE:
  - Focus ONLY on the identified issue
  - Do NOT modify other sections
  - Preserve existing structure
  
  DELIVERABLE:
  - Specific changes to resolve finding
  - Verification that fix doesn't break other areas
  
  BOUNDARIES:
  - Do NOT refactor unrelated sections
  - Do NOT change command scope
  - Do NOT modify frontmatter (except if finding is about frontmatter)
")
```

---

## P8: SCAMPER Optimization

```markdown
Task(claude-code-ecosystem, "
  Apply SCAMPER optimization to command at {resolved_path}.
  
  CONTEXT:
  Current score: {overall_score}
  Phase 1 scores: {phase1_scores}
  
  APPLY 7 SCAMPER TECHNIQUES:
  
  1. SUBSTITUTE:
     - What workflow phases could be replaced?
     - What delegation patterns could be swapped?
     - What error handling could be simplified?
  
  2. COMBINE:
     - What phases could be merged?
     - What delegation calls could be batched?
     - What error codes could be consolidated?
  
  3. ADAPT:
     - What patterns from other commands apply?
     - What industry best practices fit?
     - What OODA patterns should be adopted?
  
  4. MODIFY:
     - What could be enlarged or reduced?
     - What could be more/less detailed?
     - What flow could change?
  
  5. PUT TO OTHER USES:
     - What components could be reused?
     - What could become a shared skill?
     - What could be extracted to a template?
  
  6. ELIMINATE:
     - What redundancy can be removed?
     - What complexity is unnecessary?
     - What phases could be skipped?
  
  7. REVERSE:
     - What order could be changed?
     - What dependencies could be inverted?
     - What could be parallelized?
  
  SCORING (per recommendation):
  - Minimality: 40% (does it reduce complexity?)
  - Risk: 35% (what's the implementation risk?)
  - Maintainability: 25% (does it improve long-term maintenance?)
  
  OUTPUT JSON:
  {
    recommendations: [{
      technique: S|C|A|M|P|E|R,
      title: string,
      description: string,
      current_state: string,
      proposed_change: string,
      minimality_score: 0.0-1.0,
      risk_score: 0.0-1.0,
      maintainability_score: 0.0-1.0,
      composite_score: 0.0-1.0,
      effort: LOW|MEDIUM|HIGH,
      impact: LOW|MEDIUM|HIGH
    }],
    summary: {
      total_recommendations: int,
      high_value: int,
      quick_wins: int,
      estimated_score_improvement: int
    },
    confidence: 0.0-1.0
  }
")
```

---

## Execution Flow Summary

```
P0: INPUT VALIDATION (Sequential)
└── Validate path, extension, frontmatter

P1: PARALLEL ANALYSIS (Single message, 4 agents)
├── claude-code-ecosystem  → workflow_score, delegation_score
├── claude-code-ecosystem  → overall_grade, framework_scores
├── documentation          → current_tokens, savings_percentage
└── tech-debt-investigator → debt_score, sqale_grade

P2: ORCHESTRATOR VALIDATION (Sequential)
└── 6 validation checks

P3: SYNTHESIS (Sequential after P1+P2)
└── Merge all findings into merged_findings_summary

P4: PRE-MORTEM (Sequential after P3)
└── contingency-planner → failure_modes, resilience_score

P5: SCORING (Sequential)
└── Calculate overall_score, grade

P6: REPORT GENERATION (Sequential)
└── Generate final report

P7: DELEGATION ROUTING (Conditional)
└── Route findings to fix agents (if needed)

P8: SCAMPER OPTIMIZATION (Optional)
└── claude-code-ecosystem → optimization recommendations
```

---

## Notes

- **No truncation**: All Task() calls above are COMPLETE - copy verbatim
- **JSON comments**: Output schemas use simplified notation
- **Variable resolution**: Orchestrator replaces `{variables}` before delegation
- **Confidence threshold**: Agents with confidence < 0.7 trigger re-analysis
