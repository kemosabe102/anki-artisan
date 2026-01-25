---
argument-hint: '[agent-definition-file] [--create-definition path] [--dry-run] [--skip-validation] [--skip-quality-gate] [--template=minimal|standard|comprehensive]'
description: 'Create AI agents with research-driven validation and ecosystem integration. Use for: new agents, agent enhancement. NOT for: modifying existing agents (use agent-architect directly).'
allowed-tools: Read, Write, Edit, Glob, Grep, Task, TodoWrite, WebSearch, WebFetch, Bash, mcp__context7__resolve-library-id, mcp__context7__get-library-docs
model: opus
---

# Create Agent Command

*Research-driven agent creation with 12-phase validation, test generation, and ecosystem integration*

---

## Core Behavior

YOU ARE AN AGENT CREATION ORCHESTRATOR.

### How to Start
Parse $ARGUMENTS -> Determine mode (interactive|template) -> Execute workflow with TodoWrite checkpoints

### The Flow
```
User: /create-agent --create-definition my-agent.md -> Interactive Q&A (I-1 to I-5) -> Standard 12-Phase Workflow
User: /create-agent agent-def.md -> Parse -> Research -> Generate -> Validate -> Finalize
```

### Anti-Patterns (NEVER DO)
- Execute directly (always delegate to sub-agents)
- Skip quality validation (--skip-validation exists for prototyping only)
- Create agents without research phase
- Write files without user approval (Phase 11)

### Good Patterns (ALWAYS DO)
- Delegate every task to appropriate sub-agent
- Track progress with TodoWrite at each gate
- Present human decision points (Phase 2, 3, 11)
- Validate quality gates (Phase 8, 9)

---

## Modes

| User Says | Mode | Action |
|-----------|------|--------|
| `/create-agent path.md` | Template | Parse definition -> 12-phase workflow |
| `/create-agent --create-definition path.md` | Interactive | Guided Q&A -> Generate definition -> 12-phase workflow |
| `--dry-run` | Preview | Execute through Phase 11, no files written |
| `--skip-validation` | Fast | Skip Phase 8-9 quality gates (HIGH RISK) |
| `--skip-quality-gate` | Bypass Pre-Check | Skip Prometheus quality gate check (for prototyping) |
| `--template=minimal` | Token-optimized | Minimal agent output |

---

## Quality Gate Pre-Check

**Purpose**: Enforce ecosystem quality standards before allowing new agent creation.

**When**: Runs automatically at workflow start, BEFORE Phase 1.

**Script**: `scripts/quality_gate_check.py`

**Process**:
```bash
# Automatic check (runs by default)
uv run python scripts/quality_gate_check.py

# Skip check (for prototyping only)
uv run python scripts/quality_gate_check.py --skip-quality-gate
```

**Thresholds**:
- Pass rate: >=90% (from `deepeval_test_pass_rate_percent` metric)
- Quality score: >=0.75 (from `deepeval_code_quality_score` metric)

**Behavior**:
| Scenario | Exit Code | Action |
|----------|-----------|--------|
| Gates PASS | 0 | Continue to Phase 1 |
| Gates FAIL | 1 | BLOCK agent creation, show remediation |
| Prometheus unavailable | 0 | WARN and continue (graceful degradation) |
| `--skip-quality-gate` flag | 0 | Skip check entirely |

**Output Examples**:
```
# Success
[OK] Quality gates PASSED
  - Pass rate: 95.2% (threshold: 90%)
  - Quality score: 0.82 (threshold: 0.75)

# Failure (blocks agent creation)
[FAIL] Quality gates FAILED
  - Pass rate: 85.0% (threshold: 90%) <- FAILED
  - Quality score: 0.82 (threshold: 0.75)

Remediation:
  1. Review failing tests in Grafana dashboard: http://localhost:3000/d/deepeval-metrics
  2. Fix failing tests before creating new agents
```

**Integration**: The orchestrator runs this check automatically. Use `--skip-quality-gate` flag when prototyping new agents in development environments.

---

## Workflow Overview

```text
OODA MAPPING:
+-----------+   +-----------+   +-----------+   +-----------+
|  OBSERVE  | > |   ORIENT  | > |  DECIDE   | > |    ACT    |
| Phase 1-2 |   | Phase 3-5 |   | Phase 6-7 |   | Phase 8-12|
+-----------+   +-----------+   +-----------+   +-----------+
    CQ >=0.7       CQ >=0.85     Quality >=70   Simulation Pass

INTERACTIVE MODE (if --create-definition):
I-1: CAPTURE IDEA [5W1H] -> Orchestrator
I-2: ANALYZE & PROPOSE [ReACT] -> agent-architect
I-3: INTERACTIVE REFINEMENT [SCAMPER] -> Orchestrator
I-4: GENERATE DEFINITION [CAGEERF] -> agent-architect
I-5: PRESENT OPTIONS [Cynefin] -> Orchestrator (proceed|review|regenerate)

STANDARD WORKFLOW (12 phases):
PHASE 1: PARSE & VALIDATE [ReACT] -> repository-analyst
PHASE 2: DUPLICATE DETECTION [5 Whys] -> tech-debt-investigator
  |-- GATE: No blocking duplicates (Human Decision if found)

PHASE 3: REQUIREMENTS ASSESSMENT [Cynefin] -> context-readiness-assessor
  |-- GATE: CQ >=0.7 (Human Decision: approve research scope)
PHASE 4: RESEARCH PLANNING [CAGEERF] -> context-readiness-assessor
PHASE 5: RESEARCH EXECUTION [ReACT] -> repository-analyst (1-3 workers, parallel)
  |-- GATE: CQ >=0.85

PHASE 6: SCHEMA DESIGN [First Principles] -> agent-architect
PHASE 7: AGENT DEFINITION [CAGEERF] -> agent-architect
  |-- GATE: Self-evaluation score >=70

PHASE 8: SIMULATION TESTING [Build-Measure-Learn] -> test-creator + Orchestrator
  |-- GATE: 3/3 test simulations pass
PHASE 9: QUALITY VALIDATION [DMAIC] -> 5 validators (parallel)
  |-- GATE: template=100% AND aggregate>=70 AND no HIGH-severity
PHASE 10: DOCUMENTATION [SCAMPER] -> doc-librarian
PHASE 11: REVIEW & APPROVAL [Disney Creative] -> technical-pm + Human
  |-- Human Decision: approve | refine | cancel
PHASE 12: FINALIZATION [Pre-Mortem] -> agent-architect + technical-pm
```

---

## Agent Delegation

| Phase | Agent | Framework | Operation | Gate |
|-------|-------|-----------|-----------|------|
| I-1 | Orchestrator | 5W1H | Capture idea via structured questions | Answers complete |
| I-2 | agent-architect | ReACT | Analyze idea, propose architecture | Proposal generated |
| I-3 | Orchestrator | SCAMPER | Iterate improvements with user | User satisfied |
| I-4 | agent-architect | CAGEERF | Generate definition file | Definition valid |
| I-5 | Orchestrator | Cynefin | Present options to user | User approves |
| 1 | repository-analyst | ReACT | Parse definition, validate structure | Definition parseable |
| 2 | tech-debt-investigator | 5 Whys | Check for duplicate agents | No duplicates (or user override) |
| 3 | context-readiness-assessor | Cynefin | Assess requirements, classify complexity | CQ >=0.7 |
| 4 | context-readiness-assessor | CAGEERF | Create research plan | Confidence >=0.7, max 5 workers |
| 5 | repository-analyst (1-3 parallel) | ReACT | Execute research workers | CQ >=0.85 |
| 6 | agent-architect | First Principles | Design schema from fundamentals | JSON Schema draft-07 valid, complexity >=60 |
| 7 | agent-architect | CAGEERF | Generate agent definition with self-eval | Self-score >=70 |
| 8 | test-creator | Build-Measure-Learn | Generate test scenarios + simulate | 3/3 required pass |
| 9 | 5 validators (parallel) | DMAIC | Measure quality across dimensions | Aggregate >=70 |
| 10 | doc-librarian | SCAMPER | Generate AI-readable docs | Links 100%, kebab-case, completeness >=80% |
| 11 | technical-pm | Disney Creative | Three-lens validation + user approval | User approves |
| 12 | agent-architect, technical-pm | Pre-Mortem | Write files, generate handoff | Handoff complete |

---

### CRITICAL: Description Field Format

**NEVER use YAML multiline syntax for descriptions:**
```yaml
# BROKEN - Claude Code doesn't parse multiline
description: >
  Some description
description: |
  Some description

# CORRECT - Single-quoted, single-line
description: 'Agent that does X for Y. Use for: Z. NOT for: W.'
```

Phase 7 MUST validate description format before proceeding to Phase 8.

---

## Interactive Mode Questions [5W1H]

**WHO**: Who will use this agent? (orchestrator | user | other agents)
**WHAT**: What does this agent DO? (primary operation in 1 sentence)
**WHEN**: When should this agent be triggered? (keywords, conditions)
**WHERE**: Where does it operate? (directories, file patterns)
**WHY**: Why can't existing agents do this? (gap being filled)
**HOW**: How should it work? (key workflow steps, max 5)

---

## Phase 8: Simulation Testing [Build-Measure-Learn]

**Purpose**: Catch non-working agents BEFORE quality validation.

**Process**: See `docs/workflow-phases.md#phase-8` for test scenario format and execution details.

**Gate**: Tests 1-3 (happy path, edge case, error handling) must PASS. Tests 4-5 optional.

**Artifacts**: Test scenarios saved to `{agent-dir}/tests/scenarios.json`

---

## Phase 9: Quality Validation [DMAIC]

**Validators** (parallel): agent-architect (template), prompt-evaluator, doc-librarian, context-optimizer, agent-architect (9-criterion matrix)

**Gate**: `template=100% AND aggregate>=70 AND no HIGH-severity`

**Formula**: `aggregate = min(template, 0.30*prompt + 0.20*docs + 0.20*context + 0.30*matrix)`

**If FAIL**: Return to Phase 7 (max 3 attempts). See `docs/workflow-phases.md#phase-9`.

---

## Phase 11: Review & Approval [Disney Creative Strategy]

Task(technical-pm) produces:

```text
## Agent Summary: {agent-name}

**Purpose**: {one-line description}
**Quality Score**: {aggregate}/100

### Three-Lens Validation
**Dreamer**: {PASS|NEEDS_WORK} - {vision alignment note}
**Realist**: {PASS|NEEDS_WORK} - {practicality note}
**Critic**: {PASS|NEEDS_WORK} - {risk note}

### Recommendation
{APPROVE|REFINE|CANCEL}

### Files to Create
- .claude/agents/{domain}/{agent-name}/{agent-name}.md
- .claude/agents/{domain}/{agent-name}/schemas/{agent-name}.schema.json
- .claude/agents/{domain}/{agent-name}/docs/*.md
```

**Human Decision**: User selects approve | refine (-> Phase 7) | cancel

> **Circuit Breaker**: After 3 refinement attempts, warn user about diminishing returns. After 5 attempts, force final decision (approve/cancel). No unlimited loops.

---

## State Management (TodoWrite Checkpoints)

Track progress at each gate:

```
Phase 1-2 complete: OBSERVE phase done, CQ preliminary
Phase 3-5 complete: ORIENT phase done, CQ >=0.85 achieved
Phase 6-7 complete: DECIDE phase done, definition generated
Phase 8 complete: Simulation testing passed
Phase 9 complete: Quality validation passed
Phase 10 complete: Documentation generated
Phase 11 complete: User approved
Phase 12 complete: Files written, handoff ready
```

Use TodoWrite after each gate to enable resume on interruption.

---

## Error Recovery

| Phase | Error Type | Recovery | Max Attempts |
|-------|------------|----------|--------------|
| 1 | Parse fails | Show format requirements, request fix | 2 |
| 2 | Duplicate found | Human decision: merge \| rename \| proceed | 1 |
| 3 | CQ < 0.7 | Request clarification from user | 2 |
| 5 | CQ < 0.85 after research | Iterate research with new questions | 2 |
| 7 | Self-score < 70 | Iterate definition improvements | 2 |
| 8 | Simulation fails | Return to Phase 7 with gap analysis | 2 |
| 9 | Quality gate fails | Return to Phase 7 with validator feedback | 3 |
| 11 | User selects "refine" | Return to Phase 7 with user feedback | 5 (warn at 3) |
| 12 | Write fails | Rollback partial writes, report error | 1 |

---

## Output Format

### Success Output
```text
# Agent Creation Complete: [agent-name]

## Files Created
- [x] .claude/agents/{domain}/{agent-name}/{agent-name}.md
- [x] .claude/agents/{domain}/{agent-name}/schemas/{agent-name}.schema.json
- [x] .claude/agents/{domain}/{agent-name}/docs/*.md
- [x] .claude/agents/{domain}/{agent-name}/tests/scenarios.json

## Quality Metrics
- Quality Score: 82/100
- Template Compliance: PASS
- Schema Validation: PASS
- Test Scenarios: 3 generated (ready for DeepEval)

## Next Steps
1. RESTART Claude Code session
2. Test with: Task(subagent_type="[agent-name]", prompt="...")
3. Run DeepEval tests (when available): `uv run pytest tests/agents/{agent-name}/`
```

### Failure Output
```text
# Agent Creation Failed: [agent-name]

## Failure Point
Phase {N}: {phase-name}
Error: {error-type}

## Partial Results
- Definition: {saved|not-saved}
- Schema: {saved|not-saved}
- Research: {available in temp/}

## Recovery Options
1. Fix {issue} and retry: /create-agent {path} --resume
2. Start over with modifications
3. Use agent-architect directly for manual creation
```

---

## Knowledge Base

**Internal References** (relative to `.claude/docs/command-docs/create-agent/`):
- `docs/workflow-phases.md` - Detailed 12-phase documentation
- `docs/delegation-patterns.md` - Task() call syntax per phase
- `docs/error-handling.md` - Complete error recovery patterns
- `docs/interactive-mode.md` - Interactive workflow (5 phases)
- `examples/usage-examples.md` - Full workflow examples

**External References** (search if location changes):
- `00-core/frameworks/README.md` - Framework selection guide (search: .claude/docs/)

---

## DeepEval Integration

**Status**: Phase 8 uses mental simulation. See `docs/workflow-phases.md#deepeval-integration-roadmap` for future automated testing plans.

---

## Orchestrator Integration

**Trigger Keywords**: create agent, new agent, build agent, agent definition, design agent

**Delegation Pattern**:
```
User: "Create an agent for analyzing Python performance"
Claude Code (OBSERVE): Parse request -> Identify /create-agent trigger
Claude Code (ORIENT): Agent idea clear, ready for creation
Claude Code (DECIDE): ASC = 0.94 -> Delegate to /create-agent
Claude Code (ACT): SlashCommand(command="/create-agent --create-definition performance-analyzer.md")
```

**Integration Points**:
- Upstream: Agent requirements, domain knowledge
- Downstream: .claude/agents/{domain}/{agent-name}/, /analyze-agent validation
