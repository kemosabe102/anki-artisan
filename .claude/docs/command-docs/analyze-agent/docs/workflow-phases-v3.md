# Workflow Phases (v3)

Comprehensive documentation for all 7 phases of the `/analyze-agent` command v3.

---

## Phase Flow Diagram

```
                                    ┌─────────────────────────────────────────────────────────────┐
                                    │                     /analyze-agent v3                        │
                                    └─────────────────────────────────────────────────────────────┘
                                                              │
                                                              ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 0: VALIDATE                                                                                        │
│ Framework: Cynefin | Executor: Orchestrator | Duration: <5s                                             │
│ ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                               │
│ │ Parse Args  │───►│ Resolve     │───►│ Validate    │───►│ Fuzzy Match │                               │
│ │ (mode)      │    │ Target Path │    │ Dependencies│    │ (typos)     │                               │
│ └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘                               │
└────────────────────────────────────────────────┬────────────────────────────────────────────────────────┘
                                                 │ GATE: Valid input?
                                    ┌────────────┴────────────┐
                                    │ YES                 NO  │
                                    ▼                         ▼
                            ┌───────────────┐         ┌────────────────────┐
                            │   Phase 1     │         │ ANALYZE_ERR_001-003│
                            └───────────────┘         │ (ABORT)            │
                                    │                 └────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: DISCOVER                                                                                        │
│ Framework: MECE | Executor: 4 Agents (parallel) | Duration: 2-5min | Timeout: 120s/agent, 180s total    │
│ ┌──────────────────────────────────────────────────────────────────────────────────────────────┐        │
│ │                           SINGLE MESSAGE - 4 PARALLEL Task() CALLS                           │        │
│ │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  ┌──────────────────────────┐   │        │
│ │  │ claude-code-ecosystem│  │claude-code-ecosystem│  │doc-ref-optim   │  │tech-debt-investigator   │   │        │
│ │  │ (Structure)    │  │(Prompt Quality)│  │(Token Effic.)  │  │(Documentation Debt)     │   │        │
│ │  └────────────────┘  └────────────────┘  └────────────────┘  └──────────────────────────┘   │        │
│ └──────────────────────────────────────────────────────────────────────────────────────────────┘        │
└────────────────────────────────────────────────┬────────────────────────────────────────────────────────┘
                                                 │
                                                 ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 2: COLLECT                                                                                         │
│ Framework: OODA-OBSERVE | Executor: Orchestrator | Duration: 30s-2min                                   │
│ ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                               │
│ │ Track Agent │───►│ Validate    │───►│ Calculate   │───►│ Handle      │                               │
│ │ Status      │    │ Schemas     │    │ Metrics     │    │ Failures    │                               │
│ └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘                               │
└────────────────────────────────────────────────┬────────────────────────────────────────────────────────┘
                                                 │ GATE: >=3 agents + avg_confidence >=0.7? (detailed spec; main command uses simplified ">=3 agents")
                                    ┌────────────┴────────────┐
                                    │ YES                 NO  │
                                    ▼                         ▼
                            ┌───────────────┐         ┌────────────────────┐
                            │   Phase 3     │         │ Retry (1x) or      │
                            └───────────────┘         │ ANALYZE_ERR_004    │
                                    │                 └────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 3: SYNTHESIZE                                                                                      │
│ Framework: Synthesis Framework | Executor: Orchestrator | Duration: 30s-1min                            │
│ ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                                                  │
│ │ Overlap     │───►│ Conflict    │───►│ Consolidate │                                                  │
│ │ Detection   │    │ Detection   │    │ & Dedupe    │                                                  │
│ └─────────────┘    └─────────────┘    └─────────────┘                                                  │
└────────────────────────────────────────────────┬────────────────────────────────────────────────────────┘
                                                 │
                                                 ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 4: PRE-MORTEM (NEW in v3)                                                                          │
│ Framework: Pre-Mortem | Executor: contingency-planner | Duration: 1-2min                                 │
│ ┌─────────────────────────────────────────────────────────────────────────────────────────────┐        │
│ │ "Assume this agent fails in production. What caused the failure?"                           │        │
│ │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐            │        │
│ │  │ Input Failures │  │ Execution Fail │  │ Output Failures│  │ Evolution Fail │            │        │
│ │  └────────────────┘  └────────────────┘  └────────────────┘  └────────────────┘            │        │
│ └─────────────────────────────────────────────────────────────────────────────────────────────┘        │
└────────────────────────────────────────────────┬────────────────────────────────────────────────────────┘
                                                 │
                                                 ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 5: RECOMMEND                                                                                       │
│ Framework: Impact/Effort Matrix | Executor: Orchestrator | Duration: 30s                                │
│ ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                               │
│ │ Score Each  │───►│ Assign      │───►│ Create      │───►│ Estimate    │                               │
│ │ Finding     │    │ Priority    │    │ Roadmap     │    │ Effort      │                               │
│ └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘                               │
└────────────────────────────────────────────────┬────────────────────────────────────────────────────────┘
                                                 │
                                                 ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 6: REPORT                                                                                          │
│ Framework: Progressive Disclosure | Executor: Orchestrator | Duration: 15s                              │
│ ┌─────────────────────────────────────────────────────────────────────────────────────────────┐        │
│ │ Validated Report (report.schema.json)                                                       │        │
│ │ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │        │
│ │ │Executive │ │Scores    │ │Findings  │ │Pre-Mortem│ │Token     │ │Roadmap   │ │Metadata  │ │        │
│ │ │Summary   │ │Dashboard │ │by Prior. │ │Risks     │ │Savings   │ │          │ │          │ │        │
│ │ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │        │
│ └─────────────────────────────────────────────────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 0: VALIDATE

**Purpose**: Fail fast on invalid inputs before expensive agent operations.

**Framework**: Cynefin (problem classification)

**Executor**: Orchestrator (no agent delegation - lightweight validation)

**Duration**: <5 seconds

### Operations

```
Step 1: PARSE $ARGUMENTS
├── Extract mode from command
│   ├── by-name: "debugger", "development"
│   ├── by-path: ".claude/agents/dev-tools/debugger/debugger.md"
│   ├── claude-md: "CLAUDE.md" or "--claude-md"
│   └── ecosystem: "--all" or "--ecosystem"
└── Validate mode is recognized

Step 2: RESOLVE TARGET PATH
├── by-name: Glob(".claude/agents/**/{name}*.md") → resolve to full path
├── by-path: Verify file exists at path
├── claude-md: Use "CLAUDE.md" (project root)
└── --all: Glob(".claude/agents/**/*.md") → collect all agent files

Step 3: VALIDATE DEPENDENCIES
├── Required Agents (4):
│   ├── claude-code-ecosystem: .claude/agents/dev-tools/claude-code-ecosystem/claude-code-ecosystem.md
│   ├── claude-code-ecosystem: .claude/agents/dev-tools/claude-code-ecosystem/claude-code-ecosystem.md
│   ├── documentation: .claude/agents/dev-tools/documentation/documentation.md
│   └── tech-debt-investigator: .claude/agents/dev-tools/tech-debt-investigator/tech-debt-investigator.md
├── Required Scripts:
│   └── None (agents handle all analysis)
└── Required Docs:
    ├── synthesis-and-recommendation-framework.md
    ├── 00-core/frameworks/README.md
    └── report.schema.json

Step 4: FUZZY MATCHING (for typos)
├── If target not found exactly:
│   ├── Calculate Levenshtein distance to all agent names
│   ├── If distance <= 2: Suggest correction
│   └── Example: "debuger" → "Did you mean 'debugger'?"
└── User confirms or corrects
```

### Gate Decision

| Condition | Result | Error Code |
|-----------|--------|------------|
| Mode unrecognized | ABORT | ANALYZE_ERR_001 |
| Target path not found (no fuzzy match) | ABORT | ANALYZE_ERR_002 |
| Missing required dependency | ABORT | ANALYZE_ERR_003 |
| All valid | PROCEED to Phase 1 | - |

### Error Codes

| Code | Description | Recovery |
|------|-------------|----------|
| ANALYZE_ERR_001 | Invalid mode specified | Show valid modes: by-name, by-path, --claude-md, --all |
| ANALYZE_ERR_002 | Agent not found | Show fuzzy suggestions or list available agents |
| ANALYZE_ERR_003 | Missing dependency | List missing files, suggest installation/recovery |

---

## Phase 1: DISCOVER

**Purpose**: Gather comprehensive analysis data from 4 specialized perspectives using MECE coverage.

**Framework**: MECE (Mutually Exclusive, Collectively Exhaustive)

**Executor**: 4 Agents in parallel (single message with 4 Task() calls)

**Duration**: 2-5 minutes

**Timeout**: 120s per agent, 180s total phase timeout

### Agent Coverage Matrix

| Dimension | claude-code-ecosystem | claude-code-ecosystem | doc-ref-optimizer | tech-debt-inv |
|-----------|:---------------:|:----------------:|:-----------------:|:-------------:|
| Structure/Schema | PRIMARY | - | - | - |
| Prompt Quality | - | PRIMARY | SECONDARY | - |
| Token Efficiency | - | SECONDARY | PRIMARY | - |
| Documentation Debt | - | - | SECONDARY | PRIMARY |
| Integration | PRIMARY | - | - | SECONDARY |
| Methodology | SECONDARY | PRIMARY | - | - |

**MECE Guarantee**: Each dimension has exactly one PRIMARY owner. No gaps, no overlaps in primary responsibility.

### Launch Pattern

```python
# Single message with 4 parallel Task() calls
Task(claude-code-ecosystem, f"""
Analyze agent: {target_path}
Focus: Structure, schema compliance, integration quality
Return: JSON per claude-code-ecosystem.schema.json
""")

Task(claude-code-ecosystem, f"""
Analyze agent: {target_path}
Focus: Prompt quality across 6 frameworks + Anthropic best practices
Return: JSON per claude-code-ecosystem.schema.json
""")

Task(documentation, f"""
Analyze agent: {target_path}
Focus: Token efficiency, documentation optimization opportunities
Return: JSON per documentation.schema.json
""")

Task(tech-debt-investigator, f"""
Analyze agent: {target_path}
Focus: Documentation debt using SQALE/SIG methodology
Return: JSON per tech-debt-investigator.schema.json
""")
```

### Agent Output Schemas

#### claude-code-ecosystem Output
```json
{
  "status": "SUCCESS" | "FAILURE",
  "confidence": 0.0-1.0,
  "agent_specific_output": {
    "frontmatter_validation": {
      "valid_fields": ["name", "description", ...],
      "invalid_fields": [],
      "missing_required": []
    },
    "schema_quality": {
      "extends_base": true | false,
      "two_state_model": true | false,
      "criteria_scores": { /* 14 criteria, 0-100 each */ }
    },
    "integration_compliance": {
      "orchestrator_workflow_entry": true | false,
      "claude_md_entry": true | false,
      "schema_reference": true | false
    },
    "quality_matrix": { /* 9 criteria, 0-5 scale */ },
    "maturity_level": "v0.x MVP" | "v1.x Alpha" | "v2.x Beta" | "v3.x+ GA"
  }
}
```


#### claude-code-ecosystem Output
```json
{
  "status": "SUCCESS" | "FAILURE",
  "confidence": 0.0-1.0,
  "agent_specific_output": {
    "structural_quality": {
      "criteria_passed": 14,
      "criteria_total": 16,
      "failures": ["criterion_name", ...]
    },
    "anthropic_standards": {
      "clarity_directness": "PASS" | "PARTIAL" | "FAIL",
      "xml_structure": "PASS" | "PARTIAL" | "FAIL",
      "chain_of_thought": "PASS" | "PARTIAL" | "FAIL",
      "prefill_guidance": "PASS" | "PARTIAL" | "FAIL",
      "uncertainty_handling": "PASS" | "PARTIAL" | "FAIL",
      "context_management": "PASS" | "PARTIAL" | "FAIL"
    },
    "framework_scores": {
      "prompt_engineering": "A" | "B" | "C" | "D" | "F",
      "token_optimization": "A" | "B" | "C" | "D" | "F",
      "testing_strategy": "A" | "B" | "C" | "D" | "F",
      "progressive_disclosure": "A" | "B" | "C" | "D" | "F",
      "token_density": "A" | "B" | "C" | "D" | "F"
    }
  }
}
```

#### documentation Output
```json
{
  "status": "SUCCESS" | "FAILURE",
  "confidence": 0.0-1.0,
  "agent_specific_output": {
    "token_analysis": {
      "current_tokens": 2500,
      "optimized_potential": 1800,
      "savings_tokens": 700,
      "savings_percentage": 28.0
    },
    "base_pattern_inheritance": {
      "detected_duplication": true | false,
      "duplicated_sections": ["section_name", ...],
      "potential_savings": 1150
    },
    "anti_patterns": {
      "buried_essentials": { "count": 0, "examples": [] },
      "vague_labels": { "count": 0, "examples": [] },
      "excessive_depth": { "count": 0, "examples": [] },
      "content_duplication": { "count": 0, "tokens_wasted": 0 },
      "inline_verbose_examples": { "count": 0, "tokens_wasted": 0 },
      "missing_quick_reference": true | false
    },
    "progressive_disclosure": {
      "layering_grade": "A" | "B" | "C" | "D" | "F",
      "essential_visibility": 85.0,
      "information_scent": 80.0
    }
  }
}
```

#### tech-debt-investigator Output
```json
{
  "status": "SUCCESS" | "FAILURE",
  "confidence": 0.0-1.0,
  "agent_specific_output": {
    "debt_score": 25,
    "tdr": 0.12,
    "sqale_grade": "A" | "B" | "C" | "D" | "E",
    "sig_rating": 1-5,
    "category_breakdown": {
      "code_quality": 20,
      "testing": 30,
      "architecture": 15,
      "documentation": 40,
      "infrastructure": 10,
      "historical": 5
    },
    "hotspots": [
      { "location": "line:45-67", "severity": "HIGH", "category": "documentation" }
    ],
    "impact_effort_matrix": {
      "p1_quick_wins": 3,
      "p2_strategic": 5,
      "p3_defer": 8,
      "p4_opportunistic": 2
    }
  }
}
```

---

## Phase 2: COLLECT

**Purpose**: Aggregate results from Phase 1 agents, handle partial failures gracefully.

**Framework**: OODA - OBSERVE (collect without judgment)

**Executor**: Orchestrator

**Duration**: 30 seconds - 2 minutes

### Operations

```
Step 1: TRACK AGENT STATUS
├── For each of 4 agents, record:
│   ├── returned: Agent completed successfully
│   ├── timeout: Agent exceeded 120s limit
│   ├── error: Agent returned FAILURE status
│   └── low_confidence: Agent returned confidence < 0.5
└── Calculate: agents_successful = count(returned + low_confidence)

Step 2: VALIDATE OUTPUT SCHEMAS
├── For each returned agent:
│   ├── Parse JSON output
│   ├── Validate against agent's schema
│   ├── If invalid: Mark as "schema_error", exclude from synthesis
│   └── If valid: Add to findings pool
└── Log validation errors for debugging

Step 3: CALCULATE COLLECTION METRICS
├── collection_rate = agents_successful / 4
├── avg_confidence = mean(agent.confidence for successful agents)
├── schema_valid_rate = valid_schemas / agents_successful
└── total_findings = sum(findings from all valid agents)

Step 4: HANDLE PARTIAL FAILURES
├── Decision tree based on agents_successful:
│   ├── 4/4: Full analysis (optimal)
│   ├── 3/4: Note gap in report, continue with available data
│   ├── 2/4: Retry failed agents once (30s timeout)
│   │   ├── If retry succeeds: Continue
│   │   └── If retry fails: ANALYZE_ERR_004
│   └── <2/4: ANALYZE_ERR_004 (insufficient data)
└── Document which agents failed and why
```

### Partial Failure Handling Matrix

| Agents Returned | Action | Report Impact |
|-----------------|--------|---------------|
| 4/4 | Full analysis | Complete coverage |
| 3/4 | Note gap, continue | "Note: {agent} unavailable" in report |
| 2/4 | Retry once | If still 2/4 after retry → ANALYZE_ERR_004 |
| 1/4 or 0/4 | ABORT | ANALYZE_ERR_004 |

### Gate Decision

| Condition | Result |
|-----------|--------|
| agents_successful >= 3 AND avg_confidence >= 0.7 | PROCEED to Phase 3 |
| agents_successful == 2 | RETRY failed agents (1x) |
| After retry: still < 3 agents OR avg_confidence < 0.7 | ANALYZE_ERR_004 |

### Collection Metrics Output

```json
{
  "collection_summary": {
    "agents_launched": 4,
    "agents_returned": 4,
    "agents_timeout": 0,
    "agents_error": 0,
    "avg_confidence": 0.85,
    "total_findings": 23,
    "schema_valid_rate": 1.0
  },
  "agent_status": {
    "claude-code-ecosystem": { "status": "returned", "confidence": 0.88, "findings_count": 7 },
    "claude-code-ecosystem": { "status": "returned", "confidence": 0.82, "findings_count": 6 },
    "documentation": { "status": "returned", "confidence": 0.85, "findings_count": 5 },
    "tech-debt-investigator": { "status": "returned", "confidence": 0.84, "findings_count": 5 }
  }
}
```

---

## Phase 3: SYNTHESIZE

**Purpose**: Merge findings from multiple agents, resolve conflicts, eliminate duplicates.

**Framework**: Synthesis Framework (from `.claude/docs/00-core/synthesis-and-recommendation-framework.md`)

**Executor**: Orchestrator

**Duration**: 30 seconds - 1 minute

### Operations

```
Step 1: OVERLAP DETECTION
├── For each pair of findings:
│   ├── Calculate similarity using 3 methods:
│   │   ├── Jaccard: keyword overlap / union
│   │   ├── Structural: same file location?
│   │   └── Semantic: same problem domain?
│   ├── Combined similarity = (Jaccard × 0.4) + (Structural × 0.3) + (Semantic × 0.3)
│   └── Group findings with similarity > threshold
└── Output: overlap_groups[]

Step 2: CONFLICT DETECTION
├── Within each overlap group:
│   ├── Check for contradictory recommendations
│   │   ├── Example: Agent A says "add validation", Agent B says "remove validation"
│   │   └── Detect: opposite action verbs on same target
│   ├── If conflict found:
│   │   ├── Record both perspectives
│   │   └── Generate trade-off analysis
│   └── If no conflict: Mark as "consensus"
└── Output: conflicts[], consensus_findings[]

Step 3: CONSOLIDATION & DEDUPLICATION
├── For each overlap group:
│   ├── Merge duplicate findings (keep highest-confidence version)
│   ├── Combine evidence from all sources
│   ├── Attribute to all contributing agents
│   └── Calculate consolidated confidence = max(agent_confidences)
└── Output: merged_findings[]
```

### Overlap Thresholds

| Similarity Score | Action | Rationale |
|------------------|--------|-----------|
| > 0.9 | Merge (identical) | Same finding, different words |
| 0.7 - 0.9 | Merge (similar) | Related findings, combine evidence |
| 0.5 - 0.69 | Link (related) | Keep separate but cross-reference |
| < 0.5 | Separate | Distinct findings |

### Conflict Resolution Protocol

When agents disagree:

1. **Domain Weight**: Prefer agent with PRIMARY ownership of dimension
   - Schema issue? Trust claude-code-ecosystem over claude-code-ecosystem
   - Token issue? Trust documentation over tech-debt-investigator

2. **Confidence Weight**: Higher confidence agent gets priority (if domain equal)

3. **Trade-off Presentation**: If unresolvable, present both with pros/cons
   ```markdown
   **Conflict**: Methodology recommendation
   - claude-code-ecosystem recommends: CAGEERF (comprehensive coverage)
   - claude-code-ecosystem recommends: ReACT (iterative refinement)
   
   **Trade-off**:
   - CAGEERF: Better for complex multi-component agents
   - ReACT: Better for debugging/investigation agents
   
   **Recommendation**: User decision based on agent's primary use case
   ```

### Synthesis Output

```json
{
  "synthesis_summary": {
    "total_raw_findings": 23,
    "overlap_groups": 5,
    "merged_findings": 18,
    "conflicts_detected": 1,
    "consensus_findings": 17
  },
  "merged_findings": [
    {
      "id": "MF-001",
      "title": "Missing base-pattern extension",
      "sources": ["claude-code-ecosystem", "documentation"],
      "consolidated_confidence": 0.92,
      "similarity_score": 0.87,
      "evidence": ["line:1-5 missing extends declaration", "duplicated error recovery ~200 tokens"]
    }
  ],
  "conflicts": [
    {
      "id": "CF-001",
      "dimension": "methodology",
      "agents": ["claude-code-ecosystem", "claude-code-ecosystem"],
      "positions": { "claude-code-ecosystem": "CAGEERF", "claude-code-ecosystem": "ReACT" },
      "trade_off": "CAGEERF for complex agents, ReACT for investigation agents",
      "resolution": "user_decision"
    }
  ],
  "overlaps": [
    {
      "group_id": "OG-001",
      "findings": ["F-003", "F-012"],
      "similarity": 0.87,
      "action": "merged"
    }
  ]
}
```

---

## Phase 4: PRE-MORTEM (NEW in v3)

**Purpose**: Predict how the agent might fail in production before it happens.

**Framework**: Pre-Mortem (assume failure, brainstorm causes, prevent now)

**Executor**: contingency-planner

> **Note**: root-cause-identifier may be added as optional secondary agent in future versions for complex agents requiring deeper failure analysis.

**Duration**: 1-2 minutes

### Conceptual Foundation

> "It's 6 months from now. This agent has completely failed in production. What caused the failure?"

This inverted thinking surfaces risks that optimistic forward-looking analysis misses.

### Failure Categories

The Pre-Mortem systematically explores 5 failure categories:

#### 1. Input Failures
How the agent fails to handle incoming requests correctly.

| Failure Mode | Description | Detection Signal |
|--------------|-------------|------------------|
| Ambiguous intent | Agent misinterprets user request | Low accuracy on edge cases |
| Missing context | Required information not provided | "I don't have enough information" responses |
| Invalid format | Input doesn't match expected schema | Parse errors, validation failures |
| Scope creep | Request exceeds agent boundaries | Attempts to call forbidden tools |

#### 2. Execution Failures
How the agent fails during its core workflow.

| Failure Mode | Description | Detection Signal |
|--------------|-------------|------------------|
| Tool unavailable | Required tool not accessible | Tool call errors |
| Infinite loop | Agent doesn't converge | Timeout, token exhaustion |
| Wrong methodology | Applies inappropriate framework | Poor quality output |
| Resource exhaustion | Exceeds token/time limits | Truncated responses |

#### 3. Output Failures
How the agent produces incorrect or unusable results.

| Failure Mode | Description | Detection Signal |
|--------------|-------------|------------------|
| Schema violation | Output doesn't match contract | Validation errors downstream |
| Low confidence | Agent uncertain but proceeds | confidence < 0.7 in output |
| Hallucination | Fabricated information | Unverifiable claims |
| Incomplete | Missing required fields | Null/undefined in required fields |

#### 4. Integration Failures
How the agent fails to work within the larger system.

| Failure Mode | Description | Detection Signal |
|--------------|-------------|------------------|
| Orchestrator mismatch | Not recognized by orchestrator | Agent not selected when appropriate |
| Handoff failure | Delegation to/from fails | Broken agent chains |
| State corruption | Modifies shared state incorrectly | Inconsistent system state |
| Version drift | Incompatible with updated dependencies | Breaking changes |

#### 5. Evolution Failures
How the agent fails to remain effective over time.

| Failure Mode | Description | Detection Signal |
|--------------|-------------|------------------|
| Knowledge decay | Information becomes outdated | Incorrect recommendations |
| Pattern obsolescence | Recommended patterns deprecated | Tech debt accumulation |
| Capability gap | New requirements not supported | Feature requests pile up |
| Maintenance burden | Too complex to update safely | Fear of changes |


### Pre-Mortem Process

```
Step 1: CONTEXT GATHERING
├── Read agent definition (already done in Phase 1)
├── Extract: tools, boundaries, workflow steps
├── Identify: dependencies, integration points
└── Note: complexity indicators (lines, sections, tool count)

Step 2: FAILURE MODE ENUMERATION
├── For each of 5 categories:
│   ├── Generate 2-4 plausible failure modes
│   ├── Score: probability (0.0-1.0)
│   ├── Score: impact (0.0-1.0)
│   └── Calculate: risk_score = probability × impact
└── Total: 10-20 failure modes identified

Step 3: CRITICAL RISK IDENTIFICATION
├── Filter: risk_score >= 0.5 (critical threshold)
├── Rank by risk_score descending
├── Top 3-5 become "critical_risks"
└── Each critical risk gets:
    ├── Prevention strategy
    ├── Detection mechanism
    └── Recovery plan

Step 4: RESILIENCE SCORING
├── resilience_score = 1.0 - (mean(top_5_risk_scores))
├── Interpretation:
│   ├── 0.8-1.0: Highly resilient
│   ├── 0.6-0.79: Moderately resilient
│   ├── 0.4-0.59: Vulnerable
│   └── <0.4: High risk
└── Factor into overall quality score

Step 5: CROSS-REFERENCE WITH PHASE 3
├── For each critical risk:
│   ├── Check if existing finding addresses it
│   │   ├── YES: Link finding to risk as mitigation
│   │   └── NO: Create new P1/P2 recommendation
│   └── Update finding priority if risk is critical
└── Ensures pre-mortem insights become actionable
```

### Pre-Mortem Output

```json
{
  "pre_mortem_summary": {
    "failure_modes_identified": 15,
    "critical_risks": 4,
    "resilience_score": 0.72,
    "resilience_assessment": "Moderately resilient"
  },
  "failure_modes": [
    {
      "id": "FM-001",
      "category": "input_failures",
      "mode": "Ambiguous methodology selection",
      "description": "Agent receives task matching multiple methodologies, selects wrong one",
      "probability": 0.6,
      "impact": 0.7,
      "risk_score": 0.42,
      "is_critical": false
    },
    {
      "id": "FM-002",
      "category": "execution_failures",
      "mode": "Infinite research loop",
      "description": "Agent keeps researching without reaching confidence threshold",
      "probability": 0.4,
      "impact": 0.9,
      "risk_score": 0.36,
      "is_critical": false
    }
  ],
  "critical_risks": [
    {
      "id": "CR-001",
      "failure_mode_id": "FM-007",
      "title": "Schema validation bypass",
      "risk_score": 0.63,
      "prevention": "Add explicit schema validation step before output",
      "detection": "Monitor for downstream parse errors",
      "recovery": "Return to last valid state, request human review",
      "linked_findings": ["MF-003", "MF-012"]
    }
  ],
  "phase3_cross_reference": {
    "risks_with_existing_mitigation": 2,
    "new_recommendations_created": 2,
    "findings_priority_upgraded": 1
  }
}
```

---

## Phase 5: RECOMMEND

**Purpose**: Score and prioritize all recommendations using Impact/Effort analysis.

**Framework**: Impact/Effort Matrix (Eisenhower-style quadrant prioritization)

**Executor**: Orchestrator

**Duration**: ~30 seconds

### Operations

```
Step 1: SCORE EACH FINDING
├── For each merged finding from Phase 3 + new findings from Phase 4:
│   ├── Impact Score (1-5):
│   │   ├── 5: Critical - blocks agent from functioning
│   │   ├── 4: High - significantly degrades quality
│   │   ├── 3: Medium - noticeable improvement opportunity
│   │   ├── 2: Low - minor enhancement
│   │   └── 1: Minimal - cosmetic/polish
│   ├── Effort Score (1-5):
│   │   ├── 5: Very High - >2 days, architectural changes
│   │   ├── 4: High - 1-2 days, multiple files
│   │   ├── 3: Medium - 2-4 hours, single file complex
│   │   ├── 2: Low - 30min-2hours, straightforward
│   │   └── 1: Minimal - <30min, simple edit
│   └── Calculate: priority_score = impact / effort
└── Sort findings by priority_score descending

Step 2: ASSIGN PRIORITY QUADRANT
├── Based on Impact (High/Low) × Effort (High/Low):
│   ├── P1 (Quick Wins): High Impact + Low Effort
│   │   └── priority_score >= 2.0
│   ├── P2 (Strategic): High Impact + High Effort
│   │   └── priority_score 1.0-1.99, impact >= 4
│   ├── P3 (Backlog): Low Impact + Low Effort
│   │   └── priority_score 1.0-1.99, impact < 4
│   └── P4 (Reconsider): Low Impact + High Effort
│       └── priority_score < 1.0
└── Assign each finding to exactly one quadrant

Step 3: CREATE IMPLEMENTATION ROADMAP
├── Sprint 1 (Immediate): All P1 findings
│   └── Sequence by dependencies (if A requires B, do B first)
├── Sprint 2 (Short-term): P2 findings
│   └── Group by theme (all schema fixes together, etc.)
├── Sprint 3 (Long-term): P3 findings
│   └── Optional backlog items
└── Parking Lot: P4 findings
    └── Reconsider if context changes

Step 4: CALCULATE EFFORT ESTIMATES
├── For each sprint:
│   ├── Sum effort scores → estimate hours
│   │   ├── Effort 1 = 15 min
│   │   ├── Effort 2 = 1 hour
│   │   ├── Effort 3 = 3 hours
│   │   ├── Effort 4 = 1 day (8 hours)
│   │   └── Effort 5 = 2.5 days (20 hours)
│   └── Add 20% buffer for unknowns
└── Total estimated hours for full remediation
```

### Priority Quadrant Definitions

| Priority | Impact | Effort | Action | Typical Count |
|----------|--------|--------|--------|---------------|
| **P1** | High (4-5) | Low (1-2) | Do Now - Quick wins with high ROI | 3-5 |
| **P2** | High (4-5) | High (3-5) | Plan Next - Strategic investments | 5-10 |
| **P3** | Low (1-3) | Low (1-2) | Backlog - Nice to have when time permits | Unlimited |
| **P4** | Low (1-3) | High (3-5) | Reconsider - Usually not worth the effort | 0-2 |

### Target Distribution

A healthy agent analysis should produce:
- **P1**: 3-5 findings (focused quick wins)
- **P2**: 5-10 findings (strategic roadmap)
- **P3**: Variable (opportunity backlog)
- **P4**: 0-2 findings (if more, agent may have fundamental issues)

If P4 count > 5: Flag as "architecture review recommended"


### Recommendation Output

```json
{
  "recommendation_summary": {
    "total_recommendations": 18,
    "p1_count": 4,
    "p2_count": 7,
    "p3_count": 6,
    "p4_count": 1,
    "total_effort_hours": 12.5,
    "expected_quality_improvement": "+15 points"
  },
  "prioritized_findings": [
    {
      "id": "MF-001",
      "title": "Add base-pattern extension",
      "impact": 5,
      "effort": 1,
      "priority_score": 5.0,
      "priority": "P1",
      "sprint": 1,
      "effort_hours": 0.25,
      "dependencies": []
    },
    {
      "id": "MF-003",
      "title": "Implement schema validation",
      "impact": 4,
      "effort": 3,
      "priority_score": 1.33,
      "priority": "P2",
      "sprint": 2,
      "effort_hours": 3.0,
      "dependencies": ["MF-001"]
    }
  ],
  "roadmap": {
    "sprint_1": {
      "theme": "Quick Wins",
      "findings": ["MF-001", "MF-005", "MF-008", "MF-012"],
      "effort_hours": 2.5,
      "expected_impact": "+8 points"
    },
    "sprint_2": {
      "theme": "Strategic Improvements",
      "findings": ["MF-003", "MF-004", "MF-006", "MF-009", "MF-011", "MF-015", "MF-017"],
      "effort_hours": 8.0,
      "expected_impact": "+5 points"
    },
    "sprint_3": {
      "theme": "Polish & Enhancement",
      "findings": ["MF-002", "MF-007", "MF-010", "MF-013", "MF-014", "MF-016"],
      "effort_hours": 2.0,
      "expected_impact": "+2 points"
    },
    "parking_lot": {
      "findings": ["MF-018"],
      "reason": "Low impact relative to high effort"
    }
  }
}
```

---

## Phase 6: REPORT

**Purpose**: Generate validated, structured deliverables following Progressive Disclosure principles.

**Framework**: Progressive Disclosure (most important information first, details on demand)

**Executor**: Orchestrator

**Duration**: ~15 seconds

### Report Sections

The report follows Progressive Disclosure with 3 levels:

#### Level 1: Executive View (5 lines)
What a busy stakeholder needs in 30 seconds.

```markdown
# Agent Analysis Report: {agent-name}

**Score**: {0-100} ({A-F}) | **Resilience**: {0.0-1.0} | **Debt**: {SQALE grade}
**Top Issue**: {P1 #1 title}
**Quick Win**: {Highest priority_score recommendation}
**Effort**: {total_hours}h to reach {target_score}
```

#### Level 2: Scores Dashboard (4-dimension radar)
Visual quality breakdown for quick assessment.

```
Dimension Scores (0-100):
┌─────────────────────────────────────┐
│         Prompt Quality: 85 (B)      │
│                   ╱╲                │
│                  ╱  ╲               │
│   Integration   ╱    ╲  Schema     │
│      78 (C)    ╱      ╲   82 (B)   │
│               ╱        ╲           │
│              ╱──────────╲          │
│             Documentation: 71 (C)   │
└─────────────────────────────────────┘

Methodology: PASS (ReACT appropriate for debugging agent)
Resilience: 0.72 (Moderately resilient)
```

#### Level 3: Detailed Findings
Full analysis for implementers.

1. **Findings by Priority** (P1 → P2 → P3 → P4)
   - Each finding: title, source, impact, effort, evidence, recommendation
   
2. **Pre-Mortem Risks**
   - Critical risks with prevention/detection/recovery
   - Resilience score breakdown
   
3. **Token Optimization**
   - Current vs potential token count
   - Top 3 savings opportunities with strategies
   
4. **Implementation Roadmap**
   - Sprint breakdown with effort estimates
   - Dependency sequencing
   
5. **Maturity Assessment**
   - Current level, target level, progression criteria
   
6. **Metadata**
   - Analysis timestamp, agents used, confidence scores
   - Synthesis summary (overlaps, conflicts)


### Schema Validation

Before output, validate against `report.schema.json`:

```json
{
  "required": [
    "agent_name",
    "analysis_date", 
    "overall_score",
    "dimensions",
    "findings"
  ],
  "properties": {
    "overall_score": {
      "required": ["score", "grade"],
      "properties": {
        "score": { "type": "integer", "minimum": 0, "maximum": 100 },
        "grade": { "enum": ["A", "B", "C", "D", "F"] }
      }
    },
    "dimensions": {
      "required": ["prompt_quality", "schema_design", "documentation", "integration", "methodology"]
    },
    "pre_mortem": {
      "required": ["resilience_score", "critical_risks"],
      "properties": {
        "resilience_score": { "type": "number", "minimum": 0, "maximum": 1 }
      }
    }
  }
}
```

**Validation Rules**:
- All required fields must be present
- Scores must be within valid ranges
- Enums must use allowed values
- If validation fails: Log error, attempt repair, if still fails → ANALYZE_ERR_005

### Report Generation Process

```
Step 1: ASSEMBLE DATA
├── Collect from all previous phases:
│   ├── Phase 2: Agent outputs, collection metrics
│   ├── Phase 3: Merged findings, conflicts, overlaps
│   ├── Phase 4: Pre-mortem risks, resilience score
│   └── Phase 5: Prioritized recommendations, roadmap
└── Verify completeness

Step 2: CALCULATE OVERALL SCORE
├── Weighted average of dimensions:
│   ├── prompt_quality × 0.25
│   ├── schema_design × 0.20
│   ├── documentation × 0.20
│   ├── integration × 0.20
│   └── resilience × 0.15 (from pre-mortem)
├── Apply methodology modifier:
│   ├── PASS: +0 points
│   ├── PARTIAL: -5 points
│   └── FAIL: -10 points
└── Final score = weighted_avg + modifier

Step 3: ASSIGN GRADE
├── A: 90-100 (Excellent)
├── B: 80-89 (Good)
├── C: 70-79 (Acceptable)
├── D: 60-69 (Needs Improvement)
└── F: <60 (Poor)

Step 4: VALIDATE SCHEMA
├── Run JSON schema validation
├── If errors:
│   ├── Attempt auto-repair (fill defaults, fix types)
│   └── Re-validate
└── If still fails: ANALYZE_ERR_005

Step 5: FORMAT OUTPUT
├── Generate Markdown report
├── Include all 3 progressive disclosure levels
└── Append post-analysis action prompts
```

### Post-Analysis Actions

After report generation, offer:

```markdown
---

## Next Steps

1. **Apply P1 recommendations?** (auto-fix quick wins)
2. **Generate implementation tasks?** (create TODO items)
3. **Analyze another agent?** (continue audit)
4. **Run ecosystem-wide audit?** (if single agent analyzed)
5. **Deep dive on specific dimension?** (expand analysis)
```

---

## Error Codes Reference

| Code | Phase | Description | Recovery |
|------|-------|-------------|----------|
| ANALYZE_ERR_001 | 0 | Invalid mode specified | Show valid modes |
| ANALYZE_ERR_002 | 0 | Agent not found | Fuzzy match suggestions |
| ANALYZE_ERR_003 | 0 | Missing dependency | List missing, suggest install |
| ANALYZE_ERR_004 | 2 | Insufficient agent data (<3 agents or avg_conf <0.7) | Retry failed agents |
| ANALYZE_ERR_005 | 3 | Synthesis failure (irreconcilable conflicts) | Present raw findings |
| ANALYZE_ERR_006 | 6 | Report schema validation failed | Auto-repair attempt |

---

## Duration Summary

| Phase | Duration | Executor |
|-------|----------|----------|
| Phase 0: VALIDATE | <5s | Orchestrator |
| Phase 1: DISCOVER | 2-5min | 4 Agents (parallel) |
| Phase 2: COLLECT | 30s-2min | Orchestrator |
| Phase 3: SYNTHESIZE | 30s-1min | Orchestrator |
| Phase 4: PRE-MORTEM | 1-2min | contingency-planner |
| Phase 5: RECOMMEND | ~30s | Orchestrator |
| Phase 6: REPORT | ~15s | Orchestrator |
| **Total (single agent)** | **5-12min** | - |

**Ecosystem Mode (--all)**:
- Batch size: 5 agents per batch
- Batch interval: 30s cooldown
- Total for 20 agents: ~45-60 minutes

---

## Framework Summary

| Phase | Framework | Purpose |
|-------|-----------|---------|
| 0: VALIDATE | Cynefin | Classify problem complexity, fail fast |
| 1: DISCOVER | MECE | Ensure complete, non-overlapping coverage |
| 2: COLLECT | OODA-OBSERVE | Gather data without judgment |
| 3: SYNTHESIZE | Synthesis Framework | Merge findings, resolve conflicts |
| 4: PRE-MORTEM | Pre-Mortem | Anticipate failures before they happen |
| 5: RECOMMEND | Impact/Effort Matrix | Prioritize by ROI |
| 6: REPORT | Progressive Disclosure | Present information at right depth |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v3.0 | 2025-11-30 | Added Phase 4 (Pre-Mortem), 7-phase workflow |
| v2.0 | 2025-11-15 | Added synthesis framework, 4-phase workflow |
| v1.0 | 2025-10-20 | Initial 4-agent parallel analysis |

---

**See Also**:
- `report-format.md` - Full report template
- `report.schema.json` - JSON schema for validation
- `delegation-patterns.md` - Agent delegation examples
- `claude-md-mode.md` - Special handling for CLAUDE.md analysis
