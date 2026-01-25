# Phase 4: ACT - Execution & Report Generation

**OODA Stage**: ACT | **Time Allocation**: 40-50%

**Purpose**: Execute 7-dimension analysis, generate findings with evidence, calculate dimension scores, produce structured output

**Deliverable**: Complete analysis report with scores, violations, recommendations, and SCAMPER optimizations

---

## Workflow Steps

### Step 4.1: Dimension Scoring Execution

**Input**: Validation sequence from Phase 3

**Process**:
For each dimension in sequence, calculate score (0-100):

#### Workflow Correctness (Weight: 0.20)
| Score | Criteria |
|-------|----------|
| 100 | All steps ordered correctly, all dependencies valid |
| 75 | Minor ordering issues, no blocking dependencies |
| 50 | Some steps out of order, workarounds needed |
| 25 | Significant ordering problems |
| 0 | Circular dependencies or broken flow |

#### Parallelization Safety (Weight: 0.15)
| Score | Criteria |
|-------|----------|
| 100 | All parallel ops independent, no shared state |
| 75 | Mostly safe, minor shared read-only state |
| 50 | Some shared state, needs synchronization |
| 25 | Unsafe parallelization detected |
| 0 | Critical race conditions possible |


#### Gate Coverage (Weight: 0.15)
| Score | Criteria |
|-------|----------|
| 100 | All decision points have gates with exit criteria |
| 75 | Most gates defined, minor gaps |
| 50 | Partial gate coverage |
| 25 | Few gates, missing critical decision points |
| 0 | No gates defined |

#### Subagent Validation (Weight: 0.15)
| Score | Criteria |
|-------|----------|
| 100 | All agents exist with required tools |
| 75 | All exist, minor tool mismatches |
| 50 | Some agents missing non-critical tools |
| 25 | Missing agents but workarounds available |
| 0 | Critical agents missing |

#### Error Recovery (Weight: 0.15)
| Score | Criteria |
|-------|----------|
| 100 | Comprehensive error handling, retry policies, fallbacks |
| 75 | Good error handling, some gaps in edge cases |
| 50 | Basic error handling present |
| 25 | Minimal error handling |
| 0 | No error handling defined |

#### State Management (Weight: 0.10)
| Score | Criteria |
|-------|----------|
| 100 | Full checkpoint/resume for multi-phase |
| 75 | Checkpoints at major phases |
| 50 | Partial state persistence |
| 25 | Minimal state tracking |
| 0 | No state management (if multi-phase) |

#### Integration Alignment (Weight: 0.10)
| Score | Criteria |
|-------|----------|
| 100 | Proper trigger keywords, orchestrator integration |
| 75 | Good integration, minor gaps |
| 50 | Basic integration |
| 25 | Poor integration alignment |
| 0 | No integration consideration |


### Step 4.2: Evidence Collection

**Input**: Dimension scores, command content

**Process**:
For each score, collect supporting evidence:

```json
{
  "dimension": "Workflow Correctness",
  "score": 75,
  "evidence": [
    {
      "location": "## Phase 2, Step 3",
      "finding": "Step depends on output from Step 5",
      "severity": "medium"
    }
  ]
}
```

**Evidence Requirements**:
- Specific location (line, section, step)
- Clear finding description
- Severity classification (critical, high, medium, low)

### Step 4.3: Violation Cataloging

**Input**: Evidence with severity >= medium

**Process**:
1. Group findings by violation type
2. Assign violation codes
3. Link to dimension affected
4. Calculate fix priority

**Violation Code Format**: `WF-{dimension_abbrev}-{number}`
- WF-CORR-001: Workflow Correctness
- WF-PARA-001: Parallelization Safety
- WF-GATE-001: Gate Coverage
- WF-SUBV-001: Subagent Validation
- WF-ERRR-001: Error Recovery
- WF-STAT-001: State Management
- WF-INTG-001: Integration Alignment


### Step 4.4: Recommendation Generation

**Input**: Violations, dimension scores

**Process**:
For each violation, generate actionable recommendation:

```json
{
  "violation_code": "WF-PARA-001",
  "recommendation": "Move Task(agent-a) to sequential block before Task(agent-b)",
  "impact": "Eliminates race condition on shared config file",
  "effort": "low",
  "priority": 1
}
```

**Priority Calculation**:
- Priority 1: Critical violations + low effort
- Priority 2: High violations OR critical + high effort
- Priority 3: Medium violations
- Priority 4: Low violations

### Step 4.5: SCAMPER Optimization (OPTIMIZE mode only)

**Input**: Complete analysis, dimension scores

**Process**:
Apply 7 SCAMPER techniques per `scamper-workflow-optimization.md`:

1. **Substitute**: Identify replaceable agents/phases
2. **Combine**: Find mergeable phases
3. **Adapt**: Note patterns from successful commands
4. **Modify**: Scale/threshold adjustments
5. **Put to other use**: Extension opportunities
6. **Eliminate**: Removable complexity
7. **Reverse**: Reordering for efficiency

**Output Format**:
```json
{
  "technique": "Combine",
  "candidate": "Merge Phase 2 and Phase 3 validation",
  "minimality": 0.8,
  "risk": 0.2,
  "maintainability": 0.9,
  "score": 0.84
}
```


### Step 4.6: Workflow Diagram Generation

**Input**: Extracted phases, gates, Task() calls from OBSERVE phase

**Process**:
Generate abbreviated workflow diagram data:

1. **Extract command invocation** from frontmatter argument-hint
2. **Identify phases** from:
   - Numbered headings (## Phase N, ### Step N, P0:, etc.)
   - Named sections (VALIDATE, DISCOVER, BUILD, etc.)
3. **Extract operations per phase**:
   - Key actions described
   - Task() delegations with agent names
   - Human interaction points (WAIT, user approval, etc.)
4. **Map gates** to phases:
   - Gate IDs (G1, G2, etc.) or confidence thresholds
   - Exit criteria text
   - Human vs automated classification
5. **Identify parallelization**:
   - Phases with "parallel", "concurrent", "single message" markers
   - Multiple Task() calls in same phase

**Output Format**:
```json
{
  "workflow_diagram": {
    "command_invocation": "/analyze-command <name|path|--all>",
    "phases": [
      {
        "id": "P0",
        "name": "VALIDATE",
        "operations": ["Parse arguments", "Verify command exists"],
        "delegations": [],
        "is_parallel": false
      },
      {
        "id": "P1",
        "name": "DISCOVER",
        "operations": ["Launch 4 analysis agents"],
        "delegations": [
          {"agent": "workflow-analyzer", "output": "workflow_score"},
          {"agent": "prompt-evaluator", "output": "prompt_score"},
          {"agent": "tech-debt-investigator", "output": "debt_score"},
          {"agent": "agent-architect", "output": "structure_score"}
        ],
        "is_parallel": true
      }
    ],
    "gates": [
      {"id": "P0->P1", "after_phase": "P0", "criteria": "Command file readable", "type": "automated"},
      {"id": "P2->P3", "after_phase": "P2", "criteria": ">=3 agents returned, confidence>=0.75", "type": "automated"}
    ],
    "summary": {
      "total_gates": 5,
      "human_gates": 1,
      "automated_gates": 4,
      "parallel_phases": 1
    }
  }
}
```

**Diagram Extraction Patterns**:
| Pattern | Extracts |
|---------|----------|
| `## Phase N:` or `### Step N:` | Phase identifier |
| `Task(agent_name,` | Delegation |
| `GATE`, `[GN]`, `User approves` | Gate |
| `parallel`, `concurrent` | Parallelization |
| `WAIT`, `human`, `approval` | Human interaction |


### Step 4.7: Final Report Generation

**Input**: All scores, evidence, violations, recommendations, SCAMPER, workflow_diagram

**Process**:
1. Calculate final workflow_score:
   `workflow_score = SUM(dimension_score x weight)`
2. Assign grade based on score
3. Compile structured output per schema
4. Include summary and next steps
5. Include workflow_diagram for visual report

**Output**: Complete JSON report per `workflow-analyzer.schema.json`

---

## Exit Criteria

**All criteria must pass to complete**

| Criterion | Weight | Check |
|-----------|--------|-------|
| All dimensions scored | 0.30 | 7 dimension scores calculated |
| Evidence documented | 0.25 | Findings linked to locations |
| Violations cataloged | 0.20 | All issues coded and prioritized |
| Report generated | 0.25 | Output validates against schema |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Scores without evidence | ALWAYS link score to specific findings |
| Missing violation codes | Use standard WF-XXX-NNN format |
| Unprioritized recommendations | Calculate priority from severity+effort |
| SCAMPER without mode check | Only in OPTIMIZE mode |

---

**Previous Phase**: [Phase 3: DECIDE](phase-3-decide.md)
**Complete**: Return to [workflow-analyzer.md](../workflow-analyzer.md)
