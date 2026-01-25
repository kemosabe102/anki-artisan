---
title: "Command & Tool Discovery Guide"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Command & Tool Discovery Guide

**Purpose**: Help users discover available commands and tools for their tasks

**Audience**: Orchestrator (Claude Code primary agent)

---

## Discovery Protocol (3 Steps)

### 1. Check Available Commands First

- Review the SlashCommand tool's "Available Commands" list in the tool description
- Match user's intent to command capabilities
- Commands cover: /spec, /plan, /tasks, /implement, /git, /validate, /file-ops, /create-agent, /optimize-claude-md, /analyze-portfolio

### 2. If Command Exists - Reference it directly

- "You can use the `/[command-name]` command for this"
- Provide brief usage: "For example: `/spec feature-description` to create a specification"

### 3. If No Command Exists - Describe the approach

- "There isn't a dedicated command for this, but here's how I would approach it:"
- List the agents/tools involved: "I would use [agent-name] to [action], then [agent-name] for [action]"
- Explain the workflow: "The process would be: [step 1] → [step 2] → [step 3]"
- Optionally suggest: "This might be a good candidate for a new command if you do it frequently"

---

## Examples

### Example 1 - Command Exists

**User**: "How can I create a feature specification?"

**Response**: "You can use the `/spec` command for this. Run `/spec feature-description` or `/spec file:path/to/requirements.txt` to create a comprehensive specification with GitHub spec-kit integration. See `.claude/commands/spec/spec.md` for more options like `next` to show roadmap items."

### Example 2 - No Command

**User**: "How can I analyze circular dependencies in the codebase?"

**Response**: "There isn't a dedicated command for this, but here's how I would approach it:
1. Use researcher-codebase agent to map import relationships across packages/**
2. Use tech-debt-investigator to identify coupling hotspots
3. Generate a dependency graph with recommendations

The workflow would take ~5-10 minutes. If you do this frequently, we could create a `/analyze-dependencies` command for it."

### Example 3 - Partial Command Match

**User**: "How do I commit my changes with proper validation?"

**Response**: "You can use the `/git` command which handles validation, analysis, review, and commits with intelligent grouping. Run `/git prepare` to validate without committing, or `/git commit` to validate and commit. Use `--skip-validation` flag if you've already validated manually. See `.claude/commands/git.md` for all options."

### Example 4 - Multi-Step Workflow

**User**: "How do I create a new feature from scratch?"

**Response**: "Here's the complete workflow:
1. Use `/spec [description]` to create specification
2. Use `/plan [spec-file-path]` to generate implementation plan
3. Use `/tasks [feature-directory]` to break down into executable tasks
4. Use `/implement [feature-directory]` to execute tasks with self-correcting reviews
5. Use `/git commit` to validate and commit changes

Total time: ~30-60 min depending on feature complexity. Each command has detailed options - add `--help` for details."

### Example 5 - Agent Delegation Pattern

**User**: "How can I optimize the performance of my Python code?"

**Response**: "There isn't a dedicated command for Python performance optimization, but here's the agent delegation approach:
1. Use code-quality to identify performance bottlenecks (profiling analysis)
2. Use researcher-external to research Python performance best practices for identified patterns
3. Use development to apply optimizations
4. Use code-quality to validate performance improvements don't break functionality

Estimated time: 1-2 hours. If you do performance optimization regularly, we could create a `/optimize-performance` command."

### Example 6 - Research-Heavy Task

**User**: "What's the best way to implement caching in my system?"

**Response**: "This requires research before implementation:
1. Use researcher-lead to create research plan (cache strategies, libraries, patterns)
2. Coordinate researcher-external (industry patterns, specific library docs), researcher-codebase (existing patterns)
3. Use planning + architecture to validate approach against system design
4. Use development to implement recommended caching layer

Research phase: ~15-20 min | Implementation: ~1-2 hours. No dedicated command exists yet, but the workflow is repeatable."

### Example 7 - Validation & Quality Gates

**User**: "How can I ensure my code meets all quality standards before committing?"

**Response**: "You have two options:

**Option 1 - `/git prepare` (Comprehensive, Agent-Driven)**:
- Runs: linting, type checking, unit tests, security scanning
- Includes: code-quality analysis, code-quality validation, multi-agent quality gates
- Time: 3-5 min
- Best for: Final validation before PR creation

**Option 2 - `scripts/prepare-code-review.py --fast` (Fast, Script-Only)**:
- Runs: linting, type checking, unit tests only
- No agent analysis or artifact generation
- Time: 30-60 seconds
- Best for: Quick pre-commit validation during development

Both enforce PASS/FAIL gates. Choose based on your workflow stage."

### Example 8 - Debugging Workflow

**User**: "My tests are failing - how do I debug them?"

**Response**: "Use the debugging workflow:
1. Use code-quality to run tests and categorize failures (APPLICATION_BUG/TEST_BUG/ENVIRONMENT/FLAKY)
2. Based on failure category:
   - APPLICATION_BUG → Delegates to debugger (hypothesis-driven debugging)
   - TEST_BUG → Delegates to code-quality (test fix)
   - ENVIRONMENT → Provides setup guidance
   - FLAKY → Recommends re-run or test stability improvements
3. Debugger uses scientific method: reproduce → hypothesis → experiment → 5 Whys → minimal fix → verify

No dedicated command, but code-quality automatically delegates to the right specialist based on failure type."

---

## Key Principles

1. **Always check for existing tools before proposing manual workflows** - Tool discovery is part of being a helpful orchestrator
2. **Provide usage examples** - Show command syntax with realistic parameters
3. **Estimate time** - Help users understand workflow duration
4. **Suggest command creation** - If pattern repeats, recommend automation
5. **Multi-agent transparency** - Explain which agents will be involved and why
6. **Options comparison** - When multiple approaches exist, present trade-offs (speed vs thoroughness)

---

## Example Guidelines for CLAUDE.md

When adding new examples to CLAUDE.md, compress to 2-3 lines maximum. Format:

```
User: "[question]" → Response: "[brief answer with command/approach]"
```

Detailed examples belong in this guide (command-discovery-guide.md), not in CLAUDE.md.
