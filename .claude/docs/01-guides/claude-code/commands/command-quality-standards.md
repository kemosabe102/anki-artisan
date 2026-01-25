# Command Quality Standards

> Defines what makes a high-quality slash command based on patterns from exemplary implementations.

**Version**: 1.0  
**Last Updated**: 2025-01-04  
**Based On**: analyze-command.md, analyze-news.md, backtest.md, algo-strategy.md, integration-review.md, tasks.md

---

## Table of Contents

1. [Command Anatomy (Required Sections)](#1-command-anatomy-required-sections)
2. [Frontmatter Standards](#2-frontmatter-standards)
3. [Workflow Patterns](#3-workflow-patterns)
4. [Agent Delegation Patterns](#4-agent-delegation-patterns)
5. [Error Handling Standards](#5-error-handling-standards)
6. [Output Format Standards](#6-output-format-standards)
7. [Quality Scoring Rubric](#7-quality-scoring-rubric)
8. [Anti-Patterns Catalog](#8-anti-patterns-catalog)
9. [Command Types](#9-command-types)

---

## 1. Command Anatomy (Required Sections)

Every high-quality slash command MUST include these sections in order:

### 1.1 Required Sections Checklist

| Section | Purpose | Required | Example Command |
|---------|---------|----------|-----------------|
| **Frontmatter** | YAML metadata block | YES | All commands |
| **Identity/Role** | Define command's persona and mission | YES | analyze-command.md |
| **Modes Table** | Map inputs to behaviors | YES | algo-strategy.md |
| **Workflow Diagram** | Visual phase flow with gates | YES | analyze-news.md |
| **Phase Details** | Deep-dive each phase | RECOMMENDED | analyze-command.md |
| **Agent Delegation Matrix** | Agent-to-phase mapping | YES | integration-review.md |
| **Delegation Patterns** | Task() syntax examples | YES | analyze-news.md |
| **Gate Criteria** | Pass/fail conditions per phase | YES | integration-review.md |
| **Error Codes** | Taxonomy with recovery paths | YES | algo-strategy.md |
| **Output Templates** | Success/failure formats | YES | backtest.md |
| **Anti-Patterns** | What NOT to do | YES | analyze-command.md |
| **Good Patterns** | What to ALWAYS do | YES | backtest.md |
| **Knowledge Base** | Reference links | YES | All commands |
| **Integration** | Upstream/downstream workflow | RECOMMENDED | integration-review.md |

### 1.2 Section Order Template

```markdown
---
# Frontmatter (YAML)
---

# Command Name

*One-line description*

---

## Your Role / Core Behavior
## Modes
## Workflow (Phases with Gates)
## Phase Details (if complex)
## Agent Delegation Matrix
## Delegation Patterns
## Gate Criteria
## Error Codes
## Output Format
## Anti-Patterns (NEVER DO)
## Good Patterns (ALWAYS DO)
## Knowledge Base
## Integration / Orchestrator Integration
```

### 1.3 Exemplary Anatomy: analyze-command.md

```
Frontmatter: argument-hint, description, allowed-tools, model
Identity: <identity> block with mission and philosophy
Workflow: 9-phase diagram (P0-P8) with gates and timeouts
Modes: 4 modes (by name, by path, --all, --optimize)
Phases: Detailed breakdown with framework, agent, operations, gate, timeout
Delegation: Complete Task() syntax for each phase
Error Codes: 8 codes (ANALYZE_CMD_001-008) with recovery
Output: Two-state (SUCCESS/FAILURE) templates
Anti-Patterns: 10+ specific violations
Good Patterns: 10+ required behaviors
Knowledge Base: 6 reference links
```

---

## 2. Frontmatter Standards

Every command MUST begin with a YAML frontmatter block defining its metadata.

### 2.1 Required Fields

| Field | Required | Purpose | Format |
|-------|----------|---------|--------|
| `argument-hint` | YES | Show valid invocation syntax | `'<required> [optional] [--flags]'` |
| `description` | YES | Single sentence, action-oriented | Max 120 chars, imperative verb |
| `allowed-tools` | YES | Whitelist tools for command scope | Array or comma-separated |
| `model` | YES | Model selection for complexity | `opus`, `sonnet`, `haiku` |

### 2.2 Field Specifications

#### argument-hint
Shows users how to invoke the command correctly.

```yaml
# Simple command
argument-hint: '<feature-directory>'

# With optional flags
argument-hint: '<algorithm> <tier> [--dry-run] [--resume]'

# Multiple modes
argument-hint: '<command-name | command-path | --all | --optimize command-name>'

# Positional with defaults
argument-hint: '[YYYY-MM-DD] [category] [min-severity: 0-100]'
```

#### description
Single sentence describing what the command does. Use imperative verbs.

```yaml
# Good
description: 'Generate trading strategies using Hypothesis-Driven Development.'
description: 'Final integration review before PR. Reviews data flow boundaries.'
description: 'Comprehensive 9-phase command workflow analysis with pre-mortem.'

# Bad (too vague)
description: 'Helps with strategies'
description: 'Does review stuff'
```


#### allowed-tools
Whitelist of tools the command may use. Restricts scope for safety.

```yaml
# Read-only analysis
allowed-tools: [Task, Read, Glob, Grep]

# Full execution capability
allowed-tools: [Task, Bash, Read, Write, Glob, Grep, TodoRead, TodoWrite]

# Minimal delegation
allowed-tools: Task, Read
```

#### model
Select model based on command complexity:

| Model | Use Case | Examples |
|-------|----------|----------|
| `opus` | Complex multi-phase workflows, domain expertise | analyze-command, algo-strategy, backtest |
| `sonnet` | Simple delegation, thin orchestrators | tasks |
| `haiku` | Quick validation, simple transforms | (rarely used for commands) |

### 2.3 Complete Frontmatter Examples

**Multi-Phase Workflow (opus)**:
```yaml
---
argument-hint: '<command-name | command-path | --all | --optimize command-name>'
description: 'Comprehensive 9-phase command workflow analysis with pre-mortem.'
allowed-tools: Task, Read, Grep, Glob
model: opus
---
```

**Thin Orchestrator (sonnet)**:
```yaml
---
argument-hint: '[plan-json-path] [--phase=1-N]'
description: 'Generate machine-executable task list from PLAN.json.'
allowed-tools: Task, Read
model: sonnet
---
```

---

## 3. Workflow Patterns

Commands should follow structured phase-based execution with explicit gates.

### 3.1 Phase Naming Convention

Use `P0`, `P1`, `P2`... prefix for phases. Each phase has:
- **Name**: Descriptive action (VALIDATE, DISCOVER, COLLECT)
- **Framework**: Methodology applied (Cynefin, MECE, OODA)
- **Agent**: Who executes (orchestrator or specific agent)
- **Operations**: What happens
- **Gate**: Exit criteria
- **Timeout**: Maximum duration

### 3.2 Workflow Diagram Format

Use ASCII art for clarity. Show phases, operations, and gates inline.

**Example from analyze-news.md**:
```text
/analyze-news [date] [category] [min-severity]
|
+-- P0: ARGUMENT PARSING
|   +-- Parse date, category, severity
|   +-- Validate formats
|   +-- [GATE 0: ARGS] All arguments valid OR show usage
|
+-- P1: DATA RETRIEVAL
|   +-- Task(postgres-risk-searcher): Query events
|   +-- [GATE 1: DATA] events.count >= 1
|
+-- P2: HISTORICAL MATCHING
|   +-- Task(postgres-risk-searcher): Find similar past events
|   +-- [GATE 2: MATCHES] >= 1 match (soft gate)
```

### 3.3 Gate Types

| Gate Type | Behavior | Example |
|-----------|----------|---------|
| **HARD (Blocking)** | FAIL workflow if not met | "events.count >= 1" |
| **SOFT (Warning)** | Warn but continue | "historical_matches >= 1" |
| **HUMAN** | Requires user approval | "User approves report" |
| **AUTOMATED** | System validates | "Schema validation passes" |


### 3.4 Gate Criteria Table Format

Document all gates in a consolidated table:

```markdown
| Gate | Phase | Condition | Blocking | Recovery |
|------|-------|-----------|----------|----------|
| GATE 0 | P0 | Arguments valid | YES | Show usage |
| GATE 1 | P1 | events.count >= 1 | YES | Suggest different date |
| GATE 2 | P2 | matches >= 1 | NO | Widen confidence bands |
```

### 3.5 Checkpoint Support

For long-running commands, implement checkpoint management:

**Checkpoint Schema**:
```json
{
  "schema_version": "1.0",
  "checksum": "sha256:...",
  "feature": "feature-name",
  "started_at": "ISO8601",
  "total_items": 8,
  "completed_items": [1, 2, 3],
  "current_item": 4,
  "results": { ... },
  "status": "IN_PROGRESS"
}
```

**Resume Behavior**:
1. Load checkpoint file
2. Validate checksum (detect corruption)
3. Skip completed items
4. Continue from `current_item`

**Cleanup**: Delete checkpoint on successful completion.

### 3.6 Progress Display Format

Show users real-time progress:

```
[1/8] Reviewing: ComponentA -> ComponentB... OK PASS
[2/8] Reviewing: ComponentB -> ComponentC... WARNING (1 MEDIUM)
[3/8] Reviewing: ComponentC -> ComponentD... OK PASS
```

**Pattern**: `[{current}/{total}] {action}: {target}... {status} [{details}]`

---

## 4. Agent Delegation Patterns

Commands delegate work to agents. This section defines Task() syntax and patterns.

### 4.1 Task() Syntax

```
Task(agent-name,
  "MODE: {mode}
   {Required context}
   {Input parameters}
   
   Output: {expected_output_fields}
   BOUNDARIES: {what agent should NOT do}")
```

### 4.2 Required Task() Fields

| Field | Required | Purpose |
|-------|----------|---------|
| `agent-name` | YES | Target agent identifier |
| `MODE` | RECOMMENDED | Operation mode for multi-mode agents |
| `prompt` | YES | Instructions with context |
| `timeout_ms` | RECOMMENDED | Maximum execution time |
| `BOUNDARIES` | YES | Explicit scope limitations |

### 4.3 Timeout Recommendations

| Task Type | Recommended Timeout | Example |
|-----------|---------------------|---------|
| Validation/parsing | 60s (60000ms) | Pre-flight checks |
| Single file analysis | 120s | Code review |
| Multi-file analysis | 300s | Integration review |
| External tool execution | 600s | LEAN CLI backtest |
| Parallel agent launch | 180s total | 4 agents analyzing |


### 4.4 MODE Parameter Conventions

When agents support multiple operations, use MODE parameter:

```
Task(integration-boundary-reviewer, 
  "MODE: detect
   Feature: docs/00-project/alpha/phase-01")

Task(integration-boundary-reviewer,
  "MODE: review
   Pair: {pair_json}")

Task(backtester,
  "MODE: tier_test
   Algorithm: {algo}
   Period: post_gfc_bull")

Task(backtester,
  "MODE: aggregate
   Period results: [{...}]
   Tier: 2")
```

### 4.5 BOUNDARIES Statements

Every Task() MUST include explicit BOUNDARIES:

```
BOUNDARIES: Do NOT modify files. Do NOT evaluate prompt quality.
BOUNDARIES: Read-only queries. Do NOT modify data.
BOUNDARIES: Format only. Do NOT generate new analysis.
BOUNDARIES: Prediction only. Do NOT execute trades.
```

### 4.6 Parallel Launch Pattern

Launch multiple agents in a single message block:

**From analyze-command.md (P1)**:
```
Task(workflow-analyzer,
  "Analyze command at {path}. Evaluate workflow flow...
   BOUNDARIES: Do NOT modify files.")

Task(prompt-evaluator,
  "Evaluate command prompt at {path}...
   BOUNDARIES: Do NOT modify files.")

Task(tech-debt-investigator,
  "Assess maintainability debt...
   BOUNDARIES: Do NOT modify files.")

Task(agent-architect,
  "Validate command structure...
   BOUNDARIES: Do NOT modify files.")
```

**Rule**: Launch ALL parallel agents in ONE message. Do not launch sequentially.


### 4.7 Agent Delegation Matrix Format

Document agent-to-phase mapping:

```markdown
| Phase | Agent | Purpose | Timeout |
|-------|-------|---------|---------|
| P1 | strategy-builder | Pre-flight validation | 60s |
| P2 | backtester | Execute periods | 10min/period |
| P3 | backtester | Aggregate metrics | 60s |
| P4 | failure-analyzer | Classify failures | 60s |
```

### 4.8 Delegation Routing Matrix

For multi-outcome delegation, use routing matrix:

**From analyze-command.md (P7)**:
```markdown
| Finding Type | Primary Agent | Fallback Agent |
|--------------|---------------|----------------|
| Schema violations | agent-architect | - |
| Workflow gaps | agent-architect | workflow |
| Prompt issues | agent-architect | - |
| Documentation gaps | doc-librarian | agent-architect |
```

---

## 5. Error Handling Standards

Commands must define explicit error codes with recovery paths.

### 5.1 Error Code Taxonomy

Use prefix matching command name: `{COMMAND}_ERR_{NNN}`

| Command | Prefix | Example |
|---------|--------|---------|
| analyze-command | ANALYZE_CMD | ANALYZE_CMD_001 |
| analyze-news | NEWS_ERR | NEWS_ERR_001 |
| algo-strategy | ALGO_ERR | ALGO_ERR_001 |
| backtest | BACKTEST_ERR | BACKTEST_ERR_001 |
| integration-review | INTREV_ERR | INTREV_ERR_001 |

### 5.2 Error Categories

| Category | Code Range | Examples |
|----------|------------|----------|
| Input Validation | 001-009 | Invalid arguments, missing files |
| Dependency Errors | 010-019 | Agent unavailable, skill missing |
| Execution Errors | 020-029 | Timeout, partial failure |
| Validation Errors | 030-039 | Schema violation, gate failure |
| Integration Errors | 040-049 | External tool failure |

### 5.3 Error Table Format

```markdown
| Code | Phase | Description | Recovery |
|------|-------|-------------|----------|
| NEWS_ERR_001 | P0 | Invalid date format | Show YYYY-MM-DD format |
| NEWS_ERR_002 | P0 | Invalid category | Show valid categories |
| NEWS_ERR_003 | P1 | No events found | Suggest different date |
| NEWS_ERR_004 | P2 | No historical matches | Widen search (soft) |
```


### 5.4 Recovery Paths

Each error must have a recovery path:

| Recovery Type | When to Use | Example |
|---------------|-------------|---------|
| **Reprompt** | User input error | "Show expected format, ask for correction" |
| **Retry** | Transient failure | "Retry 1x after 30s delay" |
| **Fallback** | Degraded operation | "Use VIX-based fallback, flag uncertainty" |
| **Partial** | Some agents failed | "Report available findings, flag incomplete" |
| **Abort** | Critical failure | "Cannot proceed, escalate to user" |

### 5.5 Error Response Format

Standardize error output:

```markdown
ERROR: {ERROR_CODE}
Phase: P{N} - {phase_name}
Description: {error_description}

Details:
{specific_error_details}

Recovery:
{recovery_guidance}

Fallback:
{fallback_action_if_available}
```

### 5.6 Retry Strategies

| Error Type | Strategy | Max Retries |
|------------|----------|-------------|
| Agent timeout | Retry after 60s | 1 |
| Network error | Exponential backoff | 3 |
| Validation error | No retry (user input needed) | 0 |
| Partial agent failure | Continue with available | N/A |

---

## 6. Output Format Standards

Commands must produce consistent, predictable output.

### 6.1 Progress Display During Execution

Show real-time status for long-running operations:

```
Backtest: momentum_strategy Tier 2
==================================================
Hypothesis: HYP-20250104-abc123 (Trial 2/5)

[1/6] Testing: post_gfc_bull... OK Sharpe: 0.45
[2/6] Testing: gfc_bear... OK Sharpe: 0.22
[3/6] Testing: covid_crash... FAIL Sharpe: -0.15
[4/6] Testing: 2021_bull... OK Sharpe: 0.52
[5/6] Testing: 2022_bear... OK Sharpe: 0.18
[6/6] Testing: current... OK Sharpe: 0.33
==================================================
Gate: PASS
Action: Proceed to Tier 3
```

### 6.2 Two-State Output Pattern

Every command produces either SUCCESS or FAILURE output.

**SUCCESS Template Structure**:
```markdown
# {Command} Result: {target}
**Status**: SUCCESS
**Score/Gate**: {primary_metric}

## Summary
{executive_summary}

## Details
{structured_findings}

## Next Steps
1. {action_1}
2. {action_2}

## Generated Files
- {file_1}: {purpose}
- {file_2}: {purpose}
```


**FAILURE Template Structure**:
```markdown
# {Command} Failed

## Error
Code: {ERROR_CODE}
Phase: P{N} - {phase_name}

## Issue
{error_description}

## Details
{specific_details}

## Recovery Options
1. {option_1}
2. {option_2}

## Partial Results (if available)
{partial_data}
```

### 6.3 Generated Files Naming Conventions

| File Type | Naming Pattern | Example |
|-----------|----------------|---------|
| Report (human) | `{TYPE}-REPORT.md` | INTEGRATION-REVIEW-REPORT.md |
| Report (machine) | `{TYPE}.json` | INTEGRATION-REVIEW.json |
| Checkpoint | `.{type}-checkpoint.json` | .integration-review-checkpoint.json |
| Progress (transient) | `.{type}-progress.md` | .review-progress.md |
| Manifest | `run-manifest.json` | run-manifest.json |
| Verdict | `verdict.md` | verdict.md |

### 6.4 Machine-Readable Output Schema

JSON output must include standard fields:

```json
{
  "status": "SUCCESS | FAILURE",
  "gate_status": "PASS | PASS_WITH_CONDITIONS | FAIL | SKIPPED",
  "agent": "agent-name",
  "confidence": 0.92,
  "timestamp": "ISO8601",
  "blocked_commands": [],
  "blocking_reason": null,
  "output_files": ["file1.md", "file2.json"]
}
```

---

## 7. Quality Scoring Rubric

Score commands on a 0-100 scale across six categories.

### 7.1 Scoring Matrix

| Category | Weight | Criteria | Max Points |
|----------|--------|----------|------------|
| Structure Completeness | 20% | All required sections present | 20 |
| Workflow Clarity | 20% | Clear phases, gates, timeouts | 20 |
| Delegation Correctness | 20% | Proper Task() syntax, BOUNDARIES | 20 |
| Error Handling Coverage | 15% | Error codes, recovery paths | 15 |
| Documentation Completeness | 15% | Knowledge base, examples | 15 |
| Anti-Pattern Avoidance | 10% | No violations of banned patterns | 10 |

### 7.2 Structure Completeness (20 points)

| Criterion | Points | Requirement |
|-----------|--------|-------------|
| Frontmatter complete | 4 | All 4 required fields |
| Identity/Role section | 2 | Mission statement present |
| Modes table | 3 | Input-to-behavior mapping |
| Workflow diagram | 4 | ASCII phases with gates |
| Agent delegation matrix | 3 | Agent-to-phase mapping |
| Output templates | 2 | Success/failure formats |
| Knowledge base | 2 | Reference links present |

### 7.3 Workflow Clarity (20 points)

| Criterion | Points | Requirement |
|-----------|--------|-------------|
| Phase numbering (P0, P1...) | 3 | Consistent naming |
| Gate definitions | 4 | Each phase has exit criteria |
| Timeout specifications | 3 | Duration per phase/agent |
| Framework references | 2 | OODA, MECE, etc. applied |
| Sequential vs parallel | 3 | Execution order clear |
| Checkpoint support | 3 | Resume capability documented |
| Progress display | 2 | User feedback format |


### 7.4 Delegation Correctness (20 points)

| Criterion | Points | Requirement |
|-----------|--------|-------------|
| Task() syntax correct | 4 | Agent name, prompt, timeout |
| MODE parameter used | 3 | Multi-mode agents have MODE |
| BOUNDARIES present | 5 | Every Task() has explicit limits |
| Parallel launch pattern | 3 | Single message for parallel agents |
| Timeout recommendations | 3 | Appropriate per task type |
| Routing matrix | 2 | Multi-outcome delegation documented |

### 7.5 Error Handling Coverage (15 points)

| Criterion | Points | Requirement |
|-----------|--------|-------------|
| Error code taxonomy | 4 | {COMMAND}_ERR_{NNN} format |
| Error-to-phase mapping | 3 | Each error linked to phase |
| Recovery paths | 4 | Every error has recovery |
| Retry strategies | 2 | Timeout/failure handling |
| Partial results handling | 2 | Degraded operation documented |

### 7.6 Documentation Completeness (15 points)

| Criterion | Points | Requirement |
|-----------|--------|-------------|
| Knowledge base links | 3 | Related docs referenced |
| Usage examples | 4 | At least 2 examples |
| Integration points | 3 | Upstream/downstream documented |
| Trigger keywords | 2 | Orchestrator integration |
| Schema references | 3 | Input/output schemas linked |

### 7.7 Anti-Pattern Avoidance (10 points)

| Criterion | Points | Deduction For |
|-----------|--------|---------------|
| No direct execution | 4 | Command executes work instead of delegating |
| No missing gates | 3 | Phases without exit criteria |
| No sequential launches | 2 | Parallel agents launched sequentially |
| No missing error codes | 1 | Errors without recovery paths |


### 7.8 Grade Thresholds

| Score | Grade | Interpretation |
|-------|-------|----------------|
| 90-100 | A | Exemplary, use as reference |
| 80-89 | B | High quality, minor improvements |
| 70-79 | C | Acceptable, needs refinement |
| 60-69 | D | Below standard, significant gaps |
| <60 | F | Unacceptable, requires rewrite |

### 7.9 Example Scoring: analyze-command.md

```
Structure Completeness:     20/20 (all sections present)
Workflow Clarity:           19/20 (9 phases, gates, timeouts)
Delegation Correctness:     20/20 (parallel launch, BOUNDARIES)
Error Handling Coverage:    14/15 (8 error codes, recovery paths)
Documentation Completeness: 15/15 (knowledge base, examples)
Anti-Pattern Avoidance:     10/10 (no violations)
-------------------------------------------
Total:                      98/100 (Grade: A)
```

---

## 8. Anti-Patterns Catalog

Patterns that indicate poor command design.

### 8.1 Direct Execution (Critical)

**Anti-Pattern**: Command executes work instead of delegating.

```markdown
# BAD: Command does the work
## Workflow
1. Read files
2. Analyze content
3. Write report

# GOOD: Command delegates
## Workflow
1. Task(analyzer, "Analyze files...")
2. Task(reporter, "Generate report...")
```

**Source**: CLAUDE.md - "Orchestrator orchestrates. NEVER execute domain work directly."

### 8.2 Missing Gates Between Phases

**Anti-Pattern**: Phases proceed without validation.

```markdown
# BAD: No gate between phases
P1: Collect data
P2: Generate report

# GOOD: Explicit gate
P1: Collect data
    [GATE 1: DATA] events.count >= 1 OR abort
P2: Generate report
```

**Impact**: Downstream failures, wasted processing.

### 8.3 Sequential Agent Launches

**Anti-Pattern**: Parallel agents launched one at a time.

```markdown
# BAD: Sequential launches
Task(agent1, ...)
# Wait for result
Task(agent2, ...)
# Wait for result

# GOOD: Single message, parallel launch
Task(agent1, ...)
Task(agent2, ...)
Task(agent3, ...)
Task(agent4, ...)
# All launch simultaneously
```

**Impact**: 4x slower execution.


### 8.4 Missing Error Codes

**Anti-Pattern**: Errors without taxonomy or recovery.

```markdown
# BAD: Vague error handling
If something fails, show error message.

# GOOD: Explicit error codes
| Code | Phase | Description | Recovery |
|------|-------|-------------|----------|
| CMD_ERR_001 | P0 | Invalid input | Show format |
| CMD_ERR_002 | P1 | Agent timeout | Retry 1x |
```

### 8.5 Unclear Mode Distinctions

**Anti-Pattern**: Modes that overlap or confuse.

```markdown
# BAD: Overlapping modes
| Mode | Action |
|------|--------|
| analyze | Analyze the thing |
| review | Review the thing |
| check | Check the thing |

# GOOD: Distinct modes
| Mode | Action |
|------|--------|
| detect | Identify pairs (read-only) |
| review | Analyze single pair |
| report | Generate final output |
```

### 8.6 Missing BOUNDARIES

**Anti-Pattern**: Task() without scope limitations.

```markdown
# BAD: No boundaries
Task(agent, "Analyze and fix the code")

# GOOD: Explicit boundaries
Task(agent, "Analyze code structure.
   BOUNDARIES: Do NOT modify files. Analysis only.")
```

### 8.7 Skipping Validation Phases

**Anti-Pattern**: Jumping to execution without input validation.

```markdown
# BAD: No P0 validation
P1: Execute main workflow

# GOOD: Validate first
P0: ARGUMENT PARSING
    Validate inputs exist
    Check file format
    [GATE 0] All args valid
P1: Execute main workflow
```

**From backtest.md**: "Run backtests without hypothesis validation" is explicit anti-pattern.


### 8.8 Missing Checkpoint for Long Operations

**Anti-Pattern**: No resume capability for multi-phase workflows.

```markdown
# BAD: All-or-nothing execution
If interrupted, must restart from beginning.

# GOOD: Checkpoint after each phase
[3/8] Complete... CHECKPOINT SAVED
[4/8] Start... (can resume from here)
```

### 8.9 Reporting Without Confidence

**Anti-Pattern**: Claims without confidence scores.

```markdown
# BAD: Unqualified claims
The strategy will perform well.

# GOOD: Confidence-qualified claims
Impact prediction (confidence: 72%): -2.5% to -3.2%
Historical matches: 4 (high confidence requires >= 3)
```

### 8.10 Anti-Pattern Summary Table

| Anti-Pattern | Severity | Detection |
|--------------|----------|-----------|
| Direct execution | CRITICAL | No Task() in workflow |
| Missing gates | HIGH | Phases without [GATE] |
| Sequential launches | MEDIUM | Multiple Task() in separate messages |
| Missing error codes | HIGH | No {CMD}_ERR_NNN taxonomy |
| Unclear modes | MEDIUM | Overlapping mode descriptions |
| Missing BOUNDARIES | HIGH | Task() without scope limits |
| Skipping P0 | HIGH | No input validation phase |
| No checkpoints | MEDIUM | Long workflow, no resume |
| No confidence | LOW | Claims without scores |

---

## 9. Command Types

Commands fall into four architectural categories based on complexity and delegation patterns.

### 9.1 Thin Orchestrator

**Definition**: Validates input, delegates to single agent, returns output verbatim.

**Characteristics**:
- Minimal logic in command
- Single agent delegation
- No multi-phase workflow
- Uses `sonnet` model

**Example**: `/tasks`

```yaml
---
argument-hint: '[plan-json-path] [--phase=1-N]'
description: 'Generate machine-executable task list from PLAN.json.'
allowed-tools: Task, Read
model: sonnet
---
```

**Workflow**:
```
Parse arguments -> INPUT_GATE -> Task(task-creator) -> OUTPUT_GATE -> Return verbatim
```

**When to Use**:
- Simple delegation to a single domain agent
- Agent contains all business logic
- Command is thin wrapper

### 9.2 Multi-Phase Workflow

**Definition**: Complex orchestration with multiple phases, agents, and gates.

**Characteristics**:
- 5+ phases (P0-P4+)
- Multiple agents with different roles
- Parallel and sequential execution
- Checkpoint support for long operations
- Uses `opus` model


**Example**: `/analyze-command`

```yaml
---
argument-hint: '<command-name | --all | --optimize command-name>'
description: 'Comprehensive 9-phase command workflow analysis.'
allowed-tools: Task, Read, Grep, Glob
model: opus
---
```

**Workflow** (9 phases):
```
P0:VALIDATE -> P1:DISCOVER -> P2:COLLECT -> P3:SYNTHESIZE -> 
P4:PRE-MORTEM -> P5:RECOMMEND -> P6:REPORT -> P7:DELEGATION -> P8:SCAMPER
```

**Key Features**:
- 4 agents launched in parallel at P1
- Pre-mortem analysis at P4
- SCAMPER optimization at P8 (conditional)
- Human decision point at P6

**When to Use**:
- Complex analysis requiring multiple perspectives
- Synthesis of multiple agent outputs
- User approval gates

### 9.3 Domain Specialist

**Definition**: Deep domain logic with specialized agents and external tool integration.

**Characteristics**:
- Domain-specific validation gates
- External tool execution (LEAN CLI, databases)
- Hypothesis tracking / state management
- Domain formulas and calculations
- Uses `opus` model

**Example**: `/algo-strategy` and `/backtest`

```yaml
# algo-strategy
---
argument-hint: '<strategy description> | --from-doc <path>'
description: 'Generate trading strategies using HDD.'
allowed-tools: Task, Read, Glob, Grep, TodoWrite
model: opus
---

# backtest
---
argument-hint: '<algorithm> <tier> [--dry-run] [--resume]'
description: 'Progressive tier-based backtesting with HDD compliance.'
allowed-tools: [Task, Bash, Read, Write, Glob, Grep, TodoRead, TodoWrite]
model: opus
---
```


**Key Features**:
- Anti-overfit gates (param count < 10)
- Hypothesis formulation template
- Parameter locking before testing
- Trial tracking (max 5 per hypothesis)
- Deflated Sharpe Ratio at Tier 4
- External CLI execution (LEAN)

**When to Use**:
- Domain requires specialized methodology (HDD)
- External tool integration
- State tracking across sessions

### 9.4 Review/Validation

**Definition**: Gate-focused commands with checkpoint-enabled sequential reviews.

**Characteristics**:
- Sequential pair/item reviews
- Checkpoint after each review
- Gate criteria determine workflow outcome
- Blocks downstream commands on failure
- Uses `opus` model

**Example**: `/integration-review`

```yaml
---
argument-hint: '<feature-directory> [--resume] [--strict]'
description: 'Final integration review before PR.'
allowed-tools: [Task, Bash, Read, Write, Glob, Grep, TodoRead, TodoWrite]
model: opus
---
```

**Workflow**:
```
Parse args -> Checkpoint check -> Detect pairs -> 
Loop(review each pair, checkpoint) -> Run tests -> 
Synthesize findings -> Gate decision -> Report
```

**Key Features**:
- Pair detection via agent (MODE: detect)
- Sequential review loop with checkpoints
- Progress display per pair
- Gate criteria: CRITICAL/HIGH findings count
- Blocks `/git` on FAIL

**When to Use**:
- Pre-merge validation
- Sequential item review
- Gate-based workflow control


### 9.5 Command Type Selection Guide

| If Your Command... | Choose Type | Model |
|--------------------|-------------|-------|
| Wraps single agent | Thin Orchestrator | sonnet |
| Has 5+ phases with synthesis | Multi-Phase Workflow | opus |
| Requires external tools | Domain Specialist | opus |
| Has specialized methodology | Domain Specialist | opus |
| Reviews items sequentially | Review/Validation | opus |
| Gates downstream commands | Review/Validation | opus |

### 9.6 Type Comparison Matrix

| Aspect | Thin | Multi-Phase | Domain | Review |
|--------|------|-------------|--------|--------|
| Phases | 1-2 | 5+ | 4-8 | 5-7 |
| Agents | 1 | 3-5 | 2-4 | 2-3 |
| Parallel | No | Yes | Sometimes | No (sequential) |
| Checkpoints | No | Optional | Yes | Yes |
| Gates | 2 (in/out) | Per phase | Domain-specific | Severity-based |
| External Tools | No | No | Yes | Sometimes |
| State Tracking | No | No | Yes (hypothesis) | Yes (checkpoint) |

---

## Appendix: Quick Reference

### Required Frontmatter Fields
1. `argument-hint` - Invocation syntax
2. `description` - Single sentence purpose
3. `allowed-tools` - Tool whitelist
4. `model` - opus/sonnet/haiku

### Minimum Viable Command Sections
1. Frontmatter
2. Role/Identity
3. Modes table
4. Workflow diagram with gates
5. Agent delegation matrix
6. Error codes with recovery
7. Output templates (success/failure)
8. Anti-patterns and good patterns

### Quality Gate: Ready for Review
- [ ] All frontmatter fields present
- [ ] Every phase has explicit gate
- [ ] Every Task() has BOUNDARIES
- [ ] Error codes follow {CMD}_ERR_NNN format
- [ ] Recovery path for each error
- [ ] At least 2 usage examples
- [ ] Knowledge base links present

---

**Document Path**: `.claude/docs/01-guides/claude-code/commands/command-quality-standards.md`  
**Related**: `.claude/docs/01-guides/claude-code/commands/slash-commands-best-practices.md`  
**Schema**: `.claude/schemas/command.schema.json` (if exists)
