# Workflow Patterns Checklist

Comprehensive validation checklists for slash command workflows.

---

## 1. Frontmatter Validation Checklist

### Required Fields

| Field | Check | Pass Criteria |
|-------|-------|---------------|
| `argument-hint` | [ ] Present | Non-empty string with placeholders |
| `description` | [ ] Present | <200 chars, includes trigger keywords |
| `allowed-tools` | [ ] Present | Comma-separated, valid tool names |
| `model` | [ ] Present | One of: opus, sonnet, haiku |

### Field Quality Checks

| Check | Validation |
|-------|------------|
| [ ] argument-hint uses angle brackets | `<file-path>`, `<agent-name>` |
| [ ] argument-hint shows optional args | `[--flag]`, `| option` |
| [ ] description starts with verb | "Analyze", "Create", "Validate" |
| [ ] description includes use case | "Use for...", "When..." |
| [ ] allowed-tools is minimal | Only tools actually used |
| [ ] model matches complexity | opus for complex, sonnet for standard |

### YAML Syntax Validation

| Check | Validation |
|-------|------------|
| [ ] Valid YAML syntax | No parsing errors |
| [ ] Proper quoting | Strings with special chars quoted |
| [ ] Consistent indentation | 2 spaces, no tabs |
| [ ] No trailing spaces | Clean line endings |

---

## 2. Workflow Structure Checklist

### Phase Definition

| Check | Validation |
|-------|------------|
| [ ] Phases clearly numbered | P0, P1, P2... or Step 1, 2, 3... |
| [ ] Phase purposes defined | Each phase has stated goal |
| [ ] Dependencies explicit | "After P1 completes..." |
| [ ] No circular dependencies | Directed acyclic graph |

### Phase Components

For each phase, verify:

| Component | Check | Example |
|-----------|-------|---------|
| Purpose | [ ] Stated | "Validate inputs" |
| Agent | [ ] Assigned | "(orchestrator)" or "agent-name" |
| Operations | [ ] Listed | "Parse arguments, verify path" |
| Gate | [ ] Defined | "Agent file readable" |
| Timeout | [ ] Specified | "5s", "120s" |

### Workflow Flow Validation

| Check | Validation |
|-------|------------|
| [ ] Entry point clear | First phase identified |
| [ ] Exit point clear | Final phase identified |
| [ ] All paths lead to exit | No orphan phases |
| [ ] Conditional branches documented | "If X, then Y" |
| [ ] Human decision points marked | User approval gates |

---

## 3. Subagent Validation Checklist

### Task() Syntax

| Check | Validation |
|-------|------------|
| [ ] Agent name valid | Exists in .claude/agents/ |
| [ ] Prompt provided | Non-empty instruction string |
| [ ] Boundaries specified | "Do NOT...", "ONLY..." |
| [ ] Output format defined | Expected return structure |

### Agent Capability Verification

For each Task() call:

| Check | Validation |
|-------|------------|
| [ ] Agent has required tools | Check agent's allowed-tools |
| [ ] Task within agent scope | Matches agent description |
| [ ] No conflicting delegations | Same file not modified by multiple |

### Parallel Task() Validation

| Check | Validation |
|-------|------------|
| [ ] All parallel tasks independent | No shared state |
| [ ] No write conflicts | Different files or READ-ONLY |
| [ ] Sync point defined | "Wait for ALL agents" |
| [ ] Partial failure handling | ">= N agents required" |

---

## 4. Integration Checklist

### Orchestrator Integration

| Check | Validation |
|-------|------------|
| [ ] Trigger keywords in description | Semantic matching support |
| [ ] Invocation pattern documented | How to call the command |
| [ ] Arguments well-documented | Each arg explained |
| [ ] Output format specified | What user receives |

### Error Integration

| Check | Validation |
|-------|------------|
| [ ] Error codes defined | Named error constants |
| [ ] Recovery actions specified | What to do on each error |
| [ ] User escalation path | When to ask user |
| [ ] Partial result handling | What to return on failure |

### Documentation Integration

| Check | Validation |
|-------|------------|
| [ ] Anti-patterns section | NEVER DO list |
| [ ] Good patterns section | ALWAYS DO list |
| [ ] Examples provided | At least 1 usage example |
| [ ] References linked | Related docs |

---

## 5. State Management Checklist

### For Multi-Phase Commands (>3 phases)

| Check | Validation |
|-------|------------|
| [ ] Checkpoint mechanism | State saved between phases |
| [ ] Resume capability | Can continue from checkpoint |
| [ ] State format defined | What is persisted |
| [ ] Cleanup on completion | State removed when done |

### State Persistence

| Check | Validation |
|-------|------------|
| [ ] TodoWrite used | Progress tracking |
| [ ] Phase status tracked | pending/in_progress/completed |
| [ ] Failure state captured | What failed and why |
| [ ] Recovery path documented | How to resume |

---

## Quick Validation Summary

### Must Pass (Critical)

- [ ] All 4 frontmatter fields present
- [ ] All Task() targets exist in .claude/agents/
- [ ] Workflow phases in correct order
- [ ] Error handling defined

### Should Pass (Important)

- [ ] Gates defined for each phase
- [ ] Parallel tasks verified independent
- [ ] Documentation sections complete
- [ ] Trigger keywords present

### Nice to Have (Enhancement)

- [ ] State management for long workflows
- [ ] Examples for edge cases
- [ ] Performance considerations documented

---

## Checklist Usage

1. **Pre-Creation**: Review checklist before writing command
2. **During Review**: Validate each section systematically
3. **Post-Update**: Re-validate after modifications
4. **Audit**: Use for periodic quality checks
