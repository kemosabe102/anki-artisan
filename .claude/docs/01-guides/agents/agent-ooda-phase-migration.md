# Agent OODA Phase Migration Guide

**Purpose**: Transform agents from "OODA in prompts" to "prompts in OODA"

**Outcome**: Standardized phase-based structure enabling testability, consistency, and reduced prompt sizes

---

## Overview

### Current State vs Target State

| Aspect | Inline OODA (Before) | Phase-Based (After) |
|--------|---------------------|---------------------|
| Structure | OODA embedded in agent.md | OODA workflow in phases/ directory |
| Agent file size | 300-800 lines | <150 lines |
| Testability | Difficult - monolithic | Isolated per-phase testing |
| Maintenance | Update entire file | Update specific phase |
| Reusability | Copy/paste sections | Reference phase templates |

### Benefits

- **Standardization**: All agents follow identical phase structure
- **Testability**: Each phase independently verifiable
- **Consistency**: Shared exit criteria weights across agents
- **Reduced Prompt Size**: Agent.md focused on identity, phases loaded as needed
- **Discoverability**: Clear phase boundaries aid debugging

---

## When to Migrate

### Migration Criteria (migrate if 3+ apply)

- [ ] Agent has multi-step workflows with distinct OBSERVE/ORIENT/DECIDE/ACT phases
- [ ] Different delegation patterns per phase
- [ ] Complex decision gates between phases (CQ thresholds, approval gates)
- [ ] Agent prompt exceeds 200 lines
- [ ] Exit criteria vary by workflow stage
- [ ] Frequently updated sections could be isolated

### When NOT to Migrate

- Single-purpose agents (<100 lines)
- Agents with no clear phase boundaries (simple input/output transformation)
- Agents where all phases use identical delegation patterns
- Stable agents rarely requiring updates

---

## Automated Migration

### Command Syntax

```bash
/analyze-agent --migrate {agent-name}
```

### What It Does

1. **Creates** `phases/` directory in agent location
2. **Extracts** OODA content into 4 phase files
3. **Refactors** agent.md to hybrid model (<150 lines)
4. **Updates** description with triggers, boundaries, method summary
5. **Validates** structure against scaffold templates

### Example Usage

```bash
# Migrate debugger agent
/analyze-agent --migrate debugger

# Output:
# Created: .claude/agents/dev-tools/debugger/phases/
#   - phase-1-observe.md (context gathering)
#   - phase-2-orient.md (error analysis)
#   - phase-3-decide.md (fix strategy)
#   - phase-4-act.md (implementation)
# Refactored: debugger.md (412 -> 127 lines)
# Validation: PASSED
```

---

## Manual Migration Steps

### Step 1: Create phases/ Directory

```bash
mkdir -p .claude/agents/{domain}/{agent-name}/phases
```

### Step 2: Create phase-1-observe.md

**Extract**: Pre-flight checks, context gathering, input validation, initial delegation

**Template**: `.claude/templates/agent-scaffold/phases/phase-1-observe.template.md`

**Required Sections**:
- Purpose & Deliverable
- Pre-Flight Checklist (from agent's existing pre-flight)
- Workflow Steps (numbered 1.1, 1.2, etc.)
- Exit Criteria table with CQ weights
- Navigation to Phase 2

### Step 3: Create phase-2-orient.md

**Extract**: Analysis logic, pattern matching, quality assessment, options evaluation

**Template**: `.claude/templates/agent-scaffold/phases/phase-2-orient.template.md`

**Required Sections**:
- Analysis methodology
- Agent delegation table
- Decision matrices
- Gap detection logic
- Exit Criteria (CQ >= 0.85 typically)

### Step 4: Create phase-3-decide.md

**Extract**: Planning, risk assessment, strategy selection, approval gates

**Template**: `.claude/templates/agent-scaffold/phases/phase-3-decide.template.md`

**Required Sections**:
- Risk assessment criteria
- Strategy selection matrix
- Approval gate conditions
- Rollback planning

### Step 5: Create phase-4-act.md

**Extract**: Execution steps, delegation patterns, validation, completion criteria

**Template**: `.claude/templates/agent-scaffold/phases/phase-4-act.template.md`

**Required Sections**:
- Execution workflow
- Agent delegation (implementation agents)
- Validation checklist
- Completion criteria

### Step 6: Refactor agent.md

**Add** Phase Workflows section:
```markdown
## Phase Workflows

Detailed OODA phase instructions in `phases/` directory:

| Phase | File | Purpose |
|-------|------|---------|
| OBSERVE | [phase-1-observe.md](phases/phase-1-observe.md) | Context gathering, validation |
| ORIENT | [phase-2-orient.md](phases/phase-2-orient.md) | Analysis, pattern matching |
| DECIDE | [phase-3-decide.md](phases/phase-3-decide.md) | Planning, risk assessment |
| ACT | [phase-4-act.md](phases/phase-4-act.md) | Execution, delegation |
```

**Remove**: All migrated OODA content (should reduce to <150 lines)

### Step 7: Update Description

**Before**:
```yaml
description: 'Code review specialist for Python codebases'
```

**After**:
```yaml
description: 'Code review specialist for Python. Use for: security audits, performance review, style checks. NOT for: implementation, test writing, documentation. Method: OODA phases with severity-based findings.'
```

---

## Content Routing Matrix

| Content Type | Destination | Example |
|--------------|-------------|---------|
| Pre-flight checks | phase-1-observe.md | Input validation, file existence |
| Context gathering | phase-1-observe.md | Loading dependencies, reading configs |
| Analysis logic | phase-2-orient.md | Pattern detection, quality scoring |
| Pattern matching | phase-2-orient.md | Matching against known issues |
| Options evaluation | phase-2-orient.md | Comparing approaches |
| Planning steps | phase-3-decide.md | Execution order, dependencies |
| Risk assessment | phase-3-decide.md | Impact analysis, rollback plans |
| Approval gates | phase-3-decide.md | User confirmation triggers |
| Execution workflow | phase-4-act.md | File modifications, commands |
| Delegation patterns | phase-4-act.md | Task() calls to other agents |
| Identity/tone | agent.md (retained) | Core Behavior section |
| Tool permissions | agent.md (retained) | YAML frontmatter |
| Boundaries | agent.md (retained) | Role & Boundaries section |
| Error recovery | agent.md (retained) | Recovery patterns |

---

## Before/After Example

### Before (Inline OODA - 380 lines)

```markdown
---
name: example-agent
description: 'Example agent for demonstration'
---

# Example Agent

## Core Behavior
[20 lines]

## OBSERVE Phase
[80 lines of observation logic, checklists, delegation]

## ORIENT Phase  
[90 lines of analysis, pattern matching, matrices]

## DECIDE Phase
[70 lines of planning, risk assessment]

## ACT Phase
[85 lines of execution, validation]

## Quality Standards
[15 lines]

## Error Recovery
[20 lines]
```

### After (Phase-Based - 95 lines + 4 phase files)

**agent.md** (95 lines):
```markdown
---
name: example-agent
description: 'Example agent. Use for: X, Y. NOT for: A, B. Method: OODA with quality gates.'
---

# Example Agent

## Core Behavior
[20 lines - unchanged]

## Phase Workflows

| Phase | File | Purpose |
|-------|------|---------|
| OBSERVE | [phase-1-observe.md](phases/phase-1-observe.md) | Context, validation |
| ORIENT | [phase-2-orient.md](phases/phase-2-orient.md) | Analysis, patterns |
| DECIDE | [phase-3-decide.md](phases/phase-3-decide.md) | Planning, risks |
| ACT | [phase-4-act.md](phases/phase-4-act.md) | Execution |

## Quality Standards
[15 lines - unchanged]

## Error Recovery
[20 lines - unchanged]
```

**phases/** (4 files, ~80-100 lines each):
- phase-1-observe.md - Observation workflow
- phase-2-orient.md - Analysis workflow  
- phase-3-decide.md - Planning workflow
- phase-4-act.md - Execution workflow

### Reference Implementations

- `claude-code-ecosystem` - Full 4-phase migration with delegation tables
- `claude-code-ecosystem` - Evaluation-focused phase structure
- `tech-debt-investigator` - Investigation-focused phases

---

## Validation Checklist

After migration, verify:

### Structure
- [ ] `phases/` directory exists with 4 files
- [ ] Each phase file follows template structure
- [ ] Phase files have Previous/Next navigation links

### Phase Files
- [ ] Each has: Purpose, Deliverable, Workflow Steps, Checklist, Exit Criteria
- [ ] Exit Criteria include CQ weight tables
- [ ] Agent delegation tables specify execution mode (parallel/sequential)
- [ ] Common Mistakes section present

### Agent.md
- [ ] <150 lines after migration
- [ ] Phase Workflows section with table linking all 4 phases
- [ ] No duplicated content from phases/
- [ ] YAML description updated with "Use for:", "NOT for:", method summary

### Functionality
- [ ] Agent functionality preserved (no breaking changes)
- [ ] All original capabilities documented in phases
- [ ] Error recovery patterns retained in agent.md

---

## Templates Reference

**Location**: `.claude/templates/agent-scaffold/phases/`

| Template | Purpose |
|----------|---------|
| `phase-1-observe.template.md` | Context gathering, pre-flight |
| `phase-2-orient.template.md` | Analysis, pattern matching |
| `phase-3-decide.template.md` | Planning, risk assessment |
| `phase-4-act.template.md` | Execution, validation |
| `README.md` | Phase directory documentation |

---

## See Also

- [Agent Migration Guide](agent-migration-guide.md) - Flat-to-directory migration
- [Base Agent Pattern](base-agent-pattern.md) - Inherited patterns
- [Agent Design Best Practices](agent-design-best-practices.md) - Quality standards
- [Thinking Frameworks Catalog](../../00-core/frameworks/README.md) - OODA methodology

---

**Document Version**: 1.0  
**Last Updated**: 2025-12-08
