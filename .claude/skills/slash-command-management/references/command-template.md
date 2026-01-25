# Slash Command Template

*Use this template when creating new Claude Code slash commands*

## Minimal Template

For simple commands with limited scope:

```markdown
---
argument-hint: '<required-arg> [--optional-flag]'
description: 'Brief description of what this command does and when to use it.'
allowed-tools: [Task, Read, Glob]
---

# Command Name

*One-line tagline*

## Core Behavior

Parse $ARGUMENTS -> Execute -> Output

## Modes

| User Says | Mode | Action |
|-----------|------|--------|
| `/command <arg>` | Default | [Default behavior] |

## Output Format

### On Success
[Expected output]

### On Failure
[Expected failure output]
```

---

## Standard Template

For typical workflow commands:

```markdown
---
argument-hint: '<positional> [optional] [--flag=value]'
description: 'Purpose statement. Use for: X, Y. NOT for: Z.'
allowed-tools: [Task, Read, Glob, Grep, Bash(git:*)]
model: opus
---

# Command Name

*Tagline describing the command purpose*

---

## Core Behavior

YOU ARE A [ROLE] ORCHESTRATOR.

### How to Start
Parse $ARGUMENTS -> [Step 2] -> [Step N] -> Output

### The Flow
User: /command <args> -> [Phase 1] -> [Phase 2] -> Result

### Anti-Patterns (NEVER DO)
- [Action to avoid with explanation]
- [Another action to avoid]

### Good Patterns (ALWAYS DO)
- [Required behavior with rationale]
- [Another required behavior]

---

## Modes

| User Says | Mode | Action |
|-----------|------|--------|
| `/command <arg>` | Default | [Default behavior] |
| `--flag` | Flag Mode | [Flag-specific behavior] |
| `--mode=quick` | Quick | [Quick mode behavior] |

---

## Workflow Overview

```text
PHASE 1: [NAME] -> [Tools/Agents]
  |-- [Step description]
  |-- Output: [expected output]

PHASE 2: [NAME] -> [Tools/Agents]
  |-- [Step description]
  |-- Output: [expected output]
```

---

## Agent Delegation

| Phase | Agent | Operation |
|-------|-------|-----------|
| 1 | [agent-name] | [what it does] |
| 2 | [agent-name] | [what it does] |

---

## Error Recovery

| Error Type | Recovery |
|------------|----------|
| [Error case] | [Recovery action] |
| [Another error] | [Recovery action] |

---

## Output Format

### On Success
```text
[Expected success output format]
```

### On Failure
```text
[Expected failure output format]
```

---

## Knowledge Base

- [Link to detailed docs]
- [Link to examples]

---

## Orchestrator Integration

**Trigger Keywords**: keyword1, keyword2, keyword3

**Integration Points**:
- **Upstream**: [commands/workflows that precede this]
- **Downstream**: [commands/workflows that follow this]
```



---

## Comprehensive Template

For complex orchestration commands (like `/implement`, `/review`, `/create-agent`):

```markdown
---
argument-hint: '<source> [--focus=security|performance|all] [--mode=quick|comprehensive] [--output=path]'
description: 'Detailed purpose. Use for: A, B, C. NOT for: X, Y (use [alternative] instead).'
allowed-tools: [Task, Bash, Read, Write, Glob, Grep, mcp__context7__*, mcp__perplexity__*]
model: opus
---

# Command Name

*Tagline with key differentiator*

---

## Core Behavior

YOU ARE A [ROLE] ORCHESTRATOR.

### How to Start
Parse $ARGUMENTS -> Discover -> Route -> Investigate -> Generate

### The Flow
User: /command <source> -> Discovery -> Routing -> Parallel Execution -> Consolidation -> Report

### Anti-Patterns (NEVER DO)
- [Critical anti-pattern with consequence]
- [Security-related anti-pattern]
- [Performance anti-pattern]
- [Delegation anti-pattern]

### Good Patterns (ALWAYS DO)
- [Best practice with rationale]
- [Quality pattern]
- [Research pattern - Context7 first, Perplexity second]
- [Delegation pattern]

---

## Modes

| User Says | Mode | Action |
|-----------|------|--------|
| `/command <arg>` | Default | Full workflow |
| `--mode=quick` | Quick | Reduced scope, faster |
| `--mode=comprehensive` | Full | Complete analysis |
| `--focus=security` | Focus | Prioritize security agents |
| `--dry-run` | Preview | Show plan without executing |

---

## Workflow Overview

```text
PHASE 0: PRE-FLIGHT VALIDATION
  |-- Check required tools availability
  |-- Validate prerequisites
  |-- Output: {tools_available, warnings}

PHASE 1: DISCOVERY -> Glob + Read
  |-- Discover target files/resources
  |-- Filter exclusions
  |-- Output: discovered_items[]

PHASE 2: ROUTING -> Task(coordinator-agent)
  |-- Group by category
  |-- Batch (max N items)
  |-- Select agents
  |-- Output: batches[] with assigned agents

PHASE 3: EXECUTION -> 3 core + 0-2 dynamic (parallel)
  |-- Core agents: [agent1, agent2, agent3]
  |-- Dynamic: Select via Agent Selection Framework (confidence > 0.8)
  |-- Output: raw_results[]

PHASE 4: INVESTIGATION [CRITICAL]
  |-- Validate findings
  |-- Research via Context7/Perplexity
  |-- Output: validated_results[]

PHASE 5: CONSOLIDATION -> Dedupe + Synthesis
  |-- Deduplicate results
  |-- Synthesize insights
  |-- Output: consolidated_results[]

PHASE 6: REPORT GENERATION
  |-- Format output
  |-- Include verification commands
  |-- Output: final_report
```

---

## Agent Delegation

| Phase | Agent | Operation | Retry |
|-------|-------|-----------|-------|
| 0 | (orchestrator) | Pre-flight checks | 0 |
| 1 | (orchestrator) | File discovery | 0 |
| 2 | [coordinator] | Batching/routing | 1 |
| 3 | [worker-agents] | Parallel execution | 1 |
| 4 | (orchestrator) | Context7/Perplexity research | 2 |
| 5 | (orchestrator) | Consolidation | 0 |
| 6 | (orchestrator) | Report generation | 0 |

**Task() Syntax**:
```
Task([agent-name], "[detailed prompt with context]")
```

---

## Quality Gates

| Gate | Threshold | Action on Failure |
|------|-----------|-------------------|
| Pre-flight | All required tools | ABORT |
| Discovery | >0 items found | ABORT with guidance |
| Execution | >80% success | CONTINUE with warnings |
| Investigation | Confidence >=0.75 | Escalate or downgrade |

---

## Error Recovery

| Error Type | Retry | Recovery |
|------------|-------|----------|
| Pre-flight failure | 0 | Show requirements, STOP |
| Discovery empty | 0 | Suggest alternatives |
| Agent failure | 1 | Mark partial, continue |
| Research timeout | 2 | Degrade gracefully |
| Consolidation conflict | 0 | Manual review |

---

## Output Format

### Success
```text
[Command Name] Complete
=======================
Status: [STATUS]

Summary:
- Items: N processed
- Results: N findings (Critical: X, High: Y)
- Investigation: N researched (Context7: X, Perplexity: Y)

[CATEGORY 1] (highest priority):
[ITEM-001] Title (location)
  Confidence: 0.XX | Verified: [source]
  Action: [recommended action]
  Verify: [verification command]

[CATEGORY 2]:
...

Open Questions (needs manual review):
[OQ-001] Description (confidence: 0.XX)
  Research inconclusive - manual review required
```

### Failure
```text
[Command Name] Failed
=====================
Phase: [failed phase]
Error: [error type]

Partial Results:
- [what was completed]

Recovery Options:
1. [option 1]
2. [option 2]
```

---

## State Management

```python
command_state = {
    "phase": "current_phase",
    "items_processed": [],
    "results": [],
    "errors": [],
    "started_at": "timestamp",
    "checkpoints": []
}
```

---

## Knowledge Base

- `docs/workflow-phases.md` - Detailed phase documentation
- `docs/delegation-patterns.md` - Task() call syntax
- `docs/error-handling.md` - Error recovery patterns
- `examples/usage-examples.md` - Full workflow examples
- `schemas/[command].schema.json` - Input/output schema

---

## Orchestrator Integration

**Trigger Keywords**: keyword1, keyword2, keyword3, keyword4

**Delegation Pattern**:
```
User: "[natural language request]"
Claude Code (OBSERVE): Parse request -> Identify /command trigger
Claude Code (ORIENT): [Context assessment]
Claude Code (DECIDE): ASC = 0.XX -> Delegate to /command
Claude Code (ACT): SlashCommand(command="/command [args]")
```

**Integration Points**:
- **Upstream**: [preceding commands/workflows]
- **Downstream**: [following commands/workflows]
- **Parallel**: [commands that can run alongside]

**Anti-Patterns** (do NOT use /command for):
- [Inappropriate use case 1]
- [Inappropriate use case 2]
```
