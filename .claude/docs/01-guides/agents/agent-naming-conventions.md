---
title: "Agent Naming Conventions"
date: 2025-11-08
status: ACTIVE
tags: [agents, claude-docs]
---
# Agent Naming Conventions

**Purpose**: Standardize agent naming for clarity and discoverability
**Status**: Official naming standard for all Claude Code agents
**Effective**: 2025-10-03

## Naming Pattern

### Standard Format: `[domain]-[action]-[modifier]`

Examples:

- `planning` (domain: plan, action: enhancer)
- `code-quality` (domain: code, action: reviewer)
- `test-runner` (domain: test, action: runner)

## Suffix Standards

### Action Suffixes (Required)

| Suffix       | Purpose                   | Can Modify Files? | Examples                                                  |
| ------------ | ------------------------- | ----------------- | --------------------------------------------------------- |
| `-enhancer`  | Enhances/modifies content | ✅ Yes            | `planning`, `architecture` |
| `-reviewer`  | Reviews and validates     | ❌ No             | `code-quality`, `planning`                   |
| `-runner`    | Executes processes        | ✅ Yes            | `test-runner`                                             |
| `-handler`   | Handles external input    | ✅ Yes            | `review-response-handler`                                 |
| `-architect` | Designs and structures    | ✅ Yes            | `claude-code-ecosystem`                                         |
| `-analyzer`  | Analyzes without changing | ❌ No             | `complexity-analyzer`                                     |
| `-generator` | Creates new content       | ✅ Yes            | `task-generator`                                          |
| `-validator` | Validates correctness     | ❌ No             | `schema-validator`                                        |

### Domain Prefixes (Required)

| Prefix          | Domain              | Examples                                       |
| --------------- | ------------------- | ---------------------------------------------- |
| `spec-`         | Specifications      | `planning`                                |
| `code-`         | Code/implementation | `code-quality`                         |
| `test-`         | Testing             | `test-runner`                                  |
| `plan-`         | Planning            | `planning`                                |
| `architecture-` | Architecture/design | `architecture`, `architecture` |
| `tech-`         | Technical analysis  | `tech-debt-investigator`                       |
| `agent-`        | Agent management    | `claude-code-ecosystem`                              |
| `debug-`        | Debugging           | `debug-assistant`                              |
| `refactor-`     | Refactoring         | `refactor-assistant`                           |

## Naming Rules

### MUST Follow ✅

1. **Use lowercase with hyphens**: `planning` not `PlanEnhancer` or `plan_enhancer`
2. **Include action suffix**: Every agent must have a clear action suffix
3. **Domain before action**: `code-quality` not `reviewer-code`
4. **Be specific**: `architecture` not just `enhancer`
5. **Match capability**: Reviewers can't modify, enhancers can

### MUST Avoid ❌

1. **Generic names**: Not just `handler`, `processor`, `worker`
2. **Verb-only names**: Not `implement`, `debug`, `refactor`
3. **Unclear boundaries**: Not `code-helper`, `plan-assistant`
4. **Mixed capabilities**: Reviewers shouldn't have Write tools
5. **Duplicate purposes**: Check existing agents first

## Agent Categories

### Planning & Design


- `planning` - Reviews specification quality
- `planning` - Adds business context to plans
- `architecture` - Adds technical details
- `architecture` - Reviews technical architecture
- `planning` - Reviews business alignment

### Implementation & Code

- `development` - Implements features
- `code-quality` - Reviews code quality
- `refactor-assistant` - Refactors code
- `debug-assistant` - Debugs issues

### Testing & Validation

- `test-runner` - Creates and runs tests
- `test-reviewer` - Reviews test quality

### Meta & Management

- `claude-code-ecosystem` - Manages agent lifecycle
- `workflow-coordinator` - Manages workflows

## Tool Alignment

### Reviewers (Read-Only)

Should only have:

- Read, Grep, Glob
- WebSearch, WebFetch
- Context7 tools

Should NOT have:

- Write, Edit, MultiEdit
- Bash (unless read-only commands)
- File modification tools

### Enhancers/Handlers (Modifiers)

Can have:

- All read tools
- Write, Edit, MultiEdit
- Bash for execution
- Any needed modification tools

## Migration Guide

### Current → Recommended

| Current                   | Recommended               | Status        |
| ------------------------- | ------------------------- | ------------- |
| `development` | Keep as-is                | ✅ Good       |
| `debugger`                | `debug-assistant`         | Consider      |
| `development` | `refactor-assistant`      | Consider      |
| `handle-code-review`      | `review-response-handler` | Should change |
| `claude-code`             | `claude-config-manager`   | Consider      |

## Validation Checklist

Before creating a new agent:

- [ ] Check if agent already exists
- [ ] Follows `[domain]-[action]` pattern
- [ ] Action suffix matches capabilities
- [ ] Tools align with suffix (reviewers = read-only)
- [ ] Name is specific and clear
- [ ] No overlap with existing agents
- [ ] Description explains unique value

## Examples

### Good Names ✅

- `planning` - Clear domain and action
- `code-quality` - Obvious purpose
- `test-runner` - Specific function
- `architecture` - Detailed scope

### Bad Names ❌

- `helper` - Too generic
- `smart-agent` - Not descriptive
- `do-everything` - Too broad
- `processor` - Unclear purpose
- `claude` - Not specific

## Quick Reference

```
Creating agent? Use this checklist:

1. What domain? (spec, code, test, etc.)
2. What action? (enhance, review, run, etc.)
3. Name = [domain]-[action]
4. Can it modify files?
   - Yes → enhancer/runner/handler
   - No → reviewer/analyzer/validator
5. Tools match suffix?
   - Reviewer → Read-only tools
   - Enhancer → Modification tools
```

## Enforcement

### Automated Validation

Future hook will validate:

- Naming pattern compliance
- Tool-suffix alignment
- No duplicate purposes

### Manual Review

PR reviews should check:

- Clear agent boundaries
- No overlap with existing
- Follows conventions

---

**All new agents must follow these conventions. Existing agents should migrate gradually.**
