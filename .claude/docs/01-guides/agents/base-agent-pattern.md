---
title: "Base Agent Pattern (Universal Template)"
date: 2025-11-08
status: ACTIVE
tags: [agents, claude-docs]
---
# Base Agent Pattern (Universal Template)

**Purpose:** Common sections shared across all Claude Code agents to reduce duplication and ensure consistency
**Usage:** Agents reference this file with `**Extends**: .claude/docs/guides/base-agent-pattern.md`
**Version:** 1.0 - Context Optimization Edition
**Created:** 2025-10-10

---

## Overview

This guide establishes the universal baseline for all Claude Code agents. It contains 6 core patterns that appear in 15+ agents, representing ~1,225 tokens of common content per agent.

**Token Savings:** ~25,080 tokens across 22 agents (1,140 tokens saved per agent × 22 agents)

**Extension Mechanism:** Agents include only their specialized content, referencing this base pattern for common infrastructure.

---

## Standard Sections

### 1. Knowledge Base Integration

**Common Pattern (~100-150 tokens):**

````markdown
## Knowledge Base Integration

**Always Loaded at Startup:**

- This agent definition
- `CLAUDE.md` for project context
- `.claude/docs/01-guides/agents/agent-standards-runtime.md` (auto-loaded - universal baseline)

**Working Directory Awareness:**

- **Repository root**: `C:/Users/kemos/Repos/gauntlet-agents/` (agents always start here)
- **CRITICAL Architecture**: Claude Code resets `cwd` between bash calls - `cd` commands DO NOT PERSIST
- **Why `cd` Fails**: Each bash invocation starts fresh from repository root. Commands like `cd tests && pytest unit/` will run `cd` successfully but then pytest runs from root (not tests/) because cwd was reset.

**Path Rules by Tool Type**:

**Bash Commands** (cwd resets between calls):

- ✅ **CORRECT**: Use absolute paths
  ```bash
  uv run pytest C:/Users/kemos/Repos/gauntlet-agents/tests/unit/
  ```
````

- ❌ **WRONG**: Standalone `cd` or relative paths
  ```bash
  cd tests && uv run pytest unit/  # cwd resets, pytest runs from root
  ```

**AGENT_NAME Prefix (MANDATORY)**:
```bash
# ✅ CORRECT: Prefix all Bash commands with agent name
AGENT_NAME=debugger uv run pytest tests/unit/test_auth.py

# ❌ WRONG: Missing prefix
uv run pytest tests/unit/test_auth.py
```

**Source**: Use agent name from YAML frontmatter (`name:` field, line 2)

**Why**: Command traceability for multi-agent workflows and audit logging

**Validation**: Security hooks will enforce this requirement (implementation pending)

**Tool Calls** (Read/Write/Edit/Grep/Glob - maintain context):

- ✅ **CORRECT**: Relative paths from root
  ```python
  Read("docs/guides/file.md")
  Grep(pattern="test", path="tests/unit/")
  ```
- ✅ **ALSO CORRECT**: Absolute paths
  ```python
  Read("C:/Users/kemos/Repos/gauntlet-agents/docs/guides/file.md")
  ```

**Context Gathering Hierarchy (when uncertain):**

1. Search `.claude/docs/guides/` for domain guidance
2. Check `docs/04-guides/` for user documentation
3. Query MCP servers (Context7) for library/framework patterns
4. Web search for latest best practices if above insufficient
5. Document new patterns discovered for future reference

**MCP Resources**: Context7 for library documentation, WebFetch for current practices
**Workflow Integration**: `.claude/docs/orchestrator-workflow.md` (coordination patterns)

````

**How to Override:**
Agents add only agent-specific knowledge requirements:

```markdown
**Extends**: base-agent-pattern.md

**Additional Knowledge:**
- [Agent-specific guide] (`.claude/docs/guides/domain/specific-guide.md`)
  - When to consult: [specific scenarios]
  - What to extract: [key information needed]
````

**Example Override (development agent):**

```markdown
**Required Guide Consultations:**

1. Coding Guidelines (`docs/04-guides/code-review/coding-guidelines.md`)
   - When to consult: Every implementation task (MANDATORY first step)
   - What to extract: Pre-flight validation patterns, anti-pattern prevention

2. Component Almanac (`docs/00-project/COMPONENT_ALMANAC.md`)
   - When to consult: Before any implementation work
   - What to extract: Existing components to prevent duplication
```

---

### 2. Pre-Flight Checklist

**Common Pattern (~200-250 tokens):**

```markdown
## Pre-Flight Checklist

**Comprehensive Task Assessment** (mandatory for all operations):

1. **Schema Loading**: Verify agent-specific schema accessibility and validation rules
2. **Task Analysis**: Parse context for operation type, complexity, scope boundaries
3. **Research Planning**: Identify information gaps and research strategy
4. **Todo Creation**: Generate structured task breakdown (when 3+ steps required)
5. **Ambiguity Detection**: Flag unclear requirements, missing context, conflicting constraints
6. **Workflow Selection**: Choose appropriate lifecycle workflow based on task characteristics
7. **Resource Verification**: Confirm tool permissions, file access, external dependencies
8. **Unclear Items Tracking**: Initialize tracking for ambiguous elements throughout process
9. **Hermeneutic Orient Assessment**: Apply iterative part-whole understanding before execution
   - Fore-having: What is the total context (task environment, constraints, dependencies)?
   - Fore-sight: Which specific aspect am I examining, and why?
   - Fore-conception: What is my preliminary understanding of this task?
   - Iterate: Move between examining specific details and broader context
     * How do task details challenge my whole-view?
     * How does revised whole-view change detail interpretation?
     * Continue until understanding stabilizes or confidence ≥ 0.85
   - Keep practical: Ensure answers are concrete and actionable
```

**How to Override:**
Agents add specialized pre-flight validations:

```markdown
**Extends**: base-agent-pattern.md (Pre-Flight Checklist)

**Agent-Specific Validations:** 9. [Domain-specific validation]: [Description of specialized check] 10. [Tool-specific verification]: [Specialized resource check]
```

**Example Override (debugger agent):**

```markdown
**Agent-Specific Validations:** 9. **Hypothesis Formation**: Identify testable hypothesis before any code changes 10. **Experiment Design**: Plan non-invasive experiment strategy for validation 11. **Evidence Collection**: Confirm ability to capture debugging artifacts
```

---

### 3. Core Workflow Structure

**Common Pattern (~150-200 tokens):**

```markdown
## Core Workflow Structure

**Agent as Class, Workflows as Methods** - Execute structured 6-phase lifecycles:

**Analysis → Research → Todo Creation → Implementation → Validation → Reflection**

Each workflow specifies:

- **Input Requirements**: Expected context, dependencies, validation criteria
- **Process Phases**: Detailed step-by-step execution with unclear items handling
- **Output Format**: SUCCESS/FAILURE alignment with base-agent.schema.json
- **Integration Points**: Handoffs to orchestrator and other agents

### Workflow Phases (Standard Pattern)

1. **Analysis**: Parse context, assess complexity, identify unclear items
2. **Research**: [Agent-specific research methodology and sources]
3. **Todo Creation**: Generate structured task breakdown with dependencies
4. **Implementation**: Execute tasks with file operation protocol compliance
5. **Validation**: Verify completion against criteria, handle unclear items
6. **Reflection**: Generate lessons learned and improvement recommendations
```

**How to Override:**
Agents customize phase 2 (Research) and phase 4 (Implementation) for their domain:

```markdown
**Extends**: base-agent-pattern.md (Core Workflow Structure)

**Agent-Specific Workflow Customization:**

- **Research Phase**: [Domain-specific research approach]
- **Implementation Phase**: [Specialized execution methodology]
```

**Example Override (researcher-codebase agent):**

```markdown
**Research Phase Customization:**

- Three-phase search strategy: Discovery (5s) → Mapping (10s) → Validation (5s)
- Progressive narrowing: Broad → Narrow → Precise → Deep
- Termination rules: Stop at "good enough" (confidence > 0.85, found > 10 files)

**Implementation Phase Customization:**

- Execute codebase analysis using Glob/Grep/Read patterns
- Apply intelligent compression (10:1 minimum ratio)
- Return compressed findings with confidence scores
```

---

### OODA Phase Files (Optional Extension)

For complex agents with distinct OODA workflows, externalize phase details to a `phases/` directory.

**When to Use Phases**:
- Agent has multi-step workflows with different delegation per phase
- Complex decision gates between phases
- Exit criteria that must be validated before advancing
- Agent prompt exceeds 200 lines

**Phase Reference Pattern** (add to agent.md):

```markdown
## Phase Workflows

**Detailed Phase Documentation**: See `phases/` directory

| Phase | File | Purpose |
|-------|------|---------|
| OBSERVE | phases/phase-1-observe.md | Context gathering, pre-flight checks |
| ORIENT | phases/phase-2-orient.md | Analysis, synthesis, option evaluation |
| DECIDE | phases/phase-3-decide.md | Planning, risk assessment, approval |
| ACT | phases/phase-4-act.md | Execution, delegation, validation |
```

**Hybrid Model**:
- Core agent.md retains: identity, tools, boundaries, error recovery (<150 lines)
- Phase files contain: detailed steps, delegation tables, checklists, exit criteria

**Migration**: Use `/analyze-agent --migrate agent-name` for automated restructuring.

**Templates**: `.claude/templates/agent-scaffold/phases/*.template.md`

---

### 4. Error Recovery Patterns

**Common Pattern (~200-250 tokens):**

```markdown
## Error Recovery Patterns

**Retry Logic:**

- Retry failed tool calls with exponential backoff
- Maximum 3 retries before escalating to orchestrator
- Log failure patterns for analysis and pattern detection

**Checkpoint Strategies:**

- Save state before expensive operations (file modifications, large analyses)
- Document progress at phase boundaries (discovery complete, implementation ready)
- Enable resumption from last successful checkpoint on failure

**Graceful Degradation:**

- Provide partial results when complete results unavailable
- Document what's missing and why (blocked dependencies, unclear requirements)
- Suggest alternative approaches for missing information

**Failure Communication:**

- Return FAILURE status with specific error details and recovery guidance
- Adapt strategy based on failure type (file operation failure → versioning fallback)
- Escalate to orchestrator when unrecoverable (conflicting standards, missing dependencies)

**Error Handling:**

- **File Operation Failures**: Desktop Commander is the ONLY tool for file modifications.
  - Use `mcp__desktop-commander__edit_block` for surgical replacements
  - Use `mcp__desktop-commander__write_file` for full file writes
  - If Desktop Commander fails → ESCALATE to orchestrator (no fallback chain)
  - **CRITICAL**: NEVER use sed, awk, echo, or cat for file editing - these are BANNED
  - See `.claude/docs/01-guides/file-ops/file-operation-protocol.md` for complete Desktop Commander protocol
- **Schema Violations**: Return FAILURE with specific validation error details
- **Missing Dependencies**: FAILURE with explicit dependency gaps and acquisition strategies
- **Boundary Violations**: Immediate FAILURE with boundary enforcement message and scope guidance
```

**How to Override:**
Agents add domain-specific error handling strategies:

```markdown
**Extends**: base-agent-pattern.md (Error Recovery Patterns)

**Agent-Specific Error Handling:**

- [Domain-specific failure mode]: [Specialized recovery strategy]
- [Tool-specific error]: [Fallback approach for domain tools]
```

**Example Override (test-runner agent):**

```markdown
**Agent-Specific Error Handling:**

- **Test Framework Failures**: Switch to alternative test runner if primary fails
- **Environment Errors**: Document missing dependencies with installation commands
- **Timeout Failures**: Retry with increased timeout, fallback to subset testing
```

### Advanced Error Handling Frameworks

**For specialized agents with external service integrations, high-volume operations, or complex error scenarios, consult:**

#### Error Classification

- **error-classification-framework.md** (`.claude/docs/guides/`)
  - When to use: Before ANY retry decision on failed operations
  - Purpose: Classify errors as TRANSIENT (retryable), PERMANENT (requires fix), or FATAL (escalate)
  - Key principle: Only retry TRANSIENT errors
  - Examples: Kubernetes immutability errors (PERMANENT), network timeouts (TRANSIENT)

#### Circuit Breaker Protection

- **circuit-breaker-pattern.md** (`.claude/docs/guides/`)
  - When to use: External service integrations (WebFetch, MCP servers, kubectl operations)
  - Purpose: Prevent cascading failures through automatic fail-fast
  - Key principle: After 3 consecutive failures on same operation → stop trying, escalate
  - Configuration: 50% threshold, 10 min calls, 60s wait duration

#### Retry Strategies

- **retry-strategies.md** (`.claude/docs/guides/`)
  - When to use: Implementing retry logic for transient failures
  - Purpose: Exponential backoff with jitter, retry budgets
  - Key principle: 3 attempts max per-request, 10% retry ratio per-client
  - Pattern: Base 1-2s, max 20-60s, full jitter (AWS recommendation)

**When to Consult Advanced Frameworks**:

- External service integrations → Circuit breakers for API protection
- High-volume operations → Retry budgets to prevent cascading failures
- Kubernetes operations → Error classification (immutability vs transient)
- Complex error handling → Formal error taxonomy and decision trees

**Integration with OODA Loop**:

- **OBSERVE**: Detect error from operation
- **ORIENT**: Consult error-classification-framework.md to classify error
- **DECIDE**: Use classification to decide retry (TRANSIENT), escalate (PERMANENT), or circuit break (repeated failures)
- **ACT**: Execute retry with exponential backoff, or return FAILURE with recovery guidance

---

### 5. Parallel Execution Awareness

**Common Pattern (~150-200 tokens):**

````markdown
## Parallel Execution Awareness

**When to Parallelize:**

- Read operations (Read, Grep, Glob on different files)
- Independent research tasks (Context7 queries, WebSearch)
- Analysis of different components or files
- Validation tasks without dependencies

**When NOT to Parallelize:**

- Write operations (Write, Edit, MultiEdit on same or related files)
- Tasks with tight dependencies (output feeds next input)
- Operations requiring shared context (sequential implementation steps)
- File modifications in same module or package

**Implementation Pattern:**

```markdown
For orchestrators: Launch multiple agents in single message with multiple Task calls
For workers: Use multiple tools in parallel when operations are independent
Sequential: Operations with dependencies or shared state modifications
```
````

````

**How to Override:**
Agents specify domain-specific parallelization constraints:

```markdown
**Extends**: base-agent-pattern.md (Parallel Execution Awareness)

**Agent-Specific Parallelization:**
- [Domain-specific parallel pattern]: [When and how to parallelize in domain]
- [Tool-specific constraints]: [Limitations for domain tools]
````

**Example Override (source-control agent):**

```markdown
**Agent-Specific Parallelization:**

- **Git Status Checks**: Parallelize multiple repository status queries
- **PR Reviews**: Sequential only (git state changes between operations)
- **Commit Preparation**: Sequential for file staging and commit operations
```

---

### 6. Validation Checklist

**Common Pattern (~300-400 tokens):**

```markdown
## Validation Checklist

**Lifecycle Validation**:

- [ ] Pre-flight checklist completed with schema loading and task analysis
- [ ] Todo items created for complex tasks (3+ steps) with completion criteria
- [ ] Unclear items tracked and resolution attempted throughout workflow
- [ ] All workflow phases executed (Analysis → Research → Todo → Implementation → Validation → Reflection)
- [ ] Output follows two-state model (SUCCESS with evidence OR FAILURE with recovery guidance)

**Core Requirements**:

- [ ] All operations within defined scope boundaries (strict enforcement)
- [ ] Output validates against base-agent.schema.json + agent-specific schema
- [ ] File operations follow mandatory size assessment protocol (22.5K threshold)
- [ ] Todo completion verified or properly escalated with blocking reasons
- [ ] Research completed using specified methodology and sources documented
- [ ] Integration points properly maintained with orchestrator coordination
- [ ] Timestamp from orchestrator used (not locally generated)
- [ ] No secrets or sensitive data in outputs
- [ ] All paths and inputs sanitized

**File Operation Validation**:

- [ ] Pre-flight token count assessment completed for all file operations
- [ ] Appropriate tool selection based on file size and complexity
- [ ] Versioning strategy applied for files >22.5K tokens
- [ ] Post-operation verification via read-back for all file changes
- [ ] Fallback strategy usage documented in completion reports
- [ ] BANNED commands NOT used (no sed, awk, echo >, cat << EOF for file editing)
- [ ] Desktop Commander used for all file modifications (edit_block or write_file)

**Quality Assurance**:

- [ ] Schema compliance validation for SUCCESS/FAILURE output structure
- [ ] Confidence and severity scoring included per base-agent requirements
- [ ] Reflection summary generated with lessons learned and workflow insights
- [ ] Source attribution and provenance tracking completed for all research
- [ ] Recovery guidance provided for FAILURE cases with effort estimates and strategies
- [ ] Rationale provided for non-obvious decisions
- [ ] Work stayed within allowed boundaries
```

**How to Override:**
Agents add domain-specific validation criteria:

```markdown
**Extends**: base-agent-pattern.md (Validation Checklist)

**Agent-Specific Validation**:

- [ ] [Domain validation criterion]: [Specific check for domain]
- [ ] [Tool validation]: [Verification for domain tools]
- [ ] [Quality standard]: [Domain quality requirements]
```

**Example Override (planning agent):**

```markdown
**Agent-Specific Validation**:

- [ ] Quality scores calculated for all dimensions (completeness, testability, clarity)
- [ ] HOW vs WHAT/WHY boundary enforcement completed
- [ ] Review report generated with template structure compliance
- [ ] No modifications to source SPEC files (read-only enforcement)
```

---

---

## Extension Mechanism

### How Agents Use This Base Pattern

**Step 1: Reference the Base Pattern**

```markdown
## Base Agent Pattern Extension

**This agent EXTENDS**: `.claude/docs/guides/base-agent-pattern.md`

**Specialized Focus**: [Agent's unique capability and domain]

**Agent-Specific Capabilities**:

- [Unique capability 1 not covered by base pattern]
- [Unique capability 2 specific to this agent]
- [Unique capability 3 differentiating this agent]

**Inherited from Base Pattern**:

- Knowledge Base Integration (context gathering hierarchy)
- Pre-Flight Checklist (comprehensive task assessment)
- Core Workflow Structure (6-phase lifecycle)
- Error Recovery Patterns (retry logic, graceful degradation)
- Parallel Execution Awareness (when to parallelize/serialize)
- Validation Checklist (lifecycle, core requirements, quality assurance)
```

**Step 2: Add Only Agent-Specific Content**

```markdown
## [Agent-Specific Section Name]

[Content unique to this agent that doesn't exist in base pattern]
```

**Step 3: Override Base Sections When Necessary**

```markdown
**Extends**: base-agent-pattern.md ([Section Name])

**Agent-Specific Additions:**

- [Specialized content for this agent]
```

**See**: `.claude/docs/guides/agent-migration-guide.md` for complete migration examples (before/after comparisons with token savings)

---

**Token Impact**: ~1,140 tokens saved per agent through inheritance (see agent-migration-guide.md for calculation details)

---

**Migration**: See `.claude/docs/guides/agent-migration-guide.md` for 4-phase migration process, checklist, and examples

---

## Best Practices

**Usage**: All new agents inherit base pattern | Override only for domain-specific needs | Never weaken core requirements

**See**: .claude/docs/guides/agent-migration-guide.md for complete best practices, pitfalls, and documentation standards

---

 

---

## Related Documentation

- **Agent Template**: `.claude/templates/agent.template.md` (incorporates base pattern)
- **Review Agent Pattern**: `.claude/docs/guides/base-review-agent-pattern.md` (specialized base)
- **File Operation Protocol**: `.claude/docs/01-guides/file-ops/file-operation-protocol.md` (MANDATORY - Desktop Commander protocol)
- **Agent Standards Runtime**: `.claude/docs/01-guides/agents/agent-standards-runtime.md` (minimal auto-loaded)
- **Orchestrator Workflow**: `.claude/docs/orchestrator-workflow.md` (coordination patterns)

---

**This base agent pattern establishes the universal foundation for all Claude Code agents, reducing duplication by ~26,000 tokens across the ecosystem while ensuring consistency, maintainability, and clear agent focus on unique capabilities.**