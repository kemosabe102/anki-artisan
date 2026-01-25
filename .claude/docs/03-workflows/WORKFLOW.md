---
title: "Gauntlet Agents: Daily Workflow & Git Process"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Gauntlet Agents: Daily Workflow & Git Process

---

This document contains all daily development workflow, code review processes, git procedures, and detailed Global Workflow Enforcement protocols for the Gauntlet Agents project.

## Global Workflow Enforcement [DETAILED IMPLEMENTATION]

### Context7 Standards Authority & Phase Gate System

**UPDATED 2025-10-07**: Context7 usage follows a **phased approach** based on development stage.

#### Context7 Phased Approach

**Planning Phase**:

- **When**: Creating PLAN.md files from SPEC.md
- **Usage**: Heavy Context7 usage for library patterns, architecture choices
- **Agents**: planning, architecture
- **Goal**: Validate technical decisions against official documentation

**Task Creation Phase**:

- **When**: Generating tasks.md from PLAN.md
- **Usage**: Heavy Context7 usage for implementation patterns
- **Agents**: planning
- **Goal**: Ensure tasks follow library best practices

**Implementation Phase**:

- **When**: Implementing tasks, fixing bugs
- **Usage**: Context7 for clarification when needed
- **Agents**: development, debugger, development
- **Goal**: Resolve unclear patterns, verify API usage

**Documentation Search Priority**:

1. **Context7 FIRST** (official docs, latest versions via mcp**context7**\*)
2. **Web search SECOND** (if not in Context7, use WebSearch)
3. **Fallback**: Official website documentation directly

**Rules:**

- Context7 overrides project docs (create "Doc Update Proposal" if conflicts)
- IF standards conflict → **STOP** with "Standards Conflict Note"
- IF Context7 unreachable/insufficient → Use `WebSearch` for current best practices, then official upstream docs, mark `standards_fallback=true`

#### 1a. Spec-Kit Enhanced Planning (MANDATORY FOR FEATURES)

**Apply spec-kit clarity techniques to all feature development:**

**CRITICAL: Existing Component Discovery (MANDATORY FIRST STEP)**

- **Before ANY implementation planning**: Search existing codebase for related functionality
- **Search patterns**: Use `Grep`, `Glob`, and `Read` tools to find existing implementations:
  - Search for similar feature names, keywords, and functionality
  - Check `packages/core/` for shared utilities and existing modules
  - Look in `services/`, `workers/`, `domain/models/` for related components
  - Review existing tests in `tests/` for similar functionality patterns
- **Documentation review**: Check existing feature plans, architecture docs, and SPEC.md
- **Prevent duplication**: Build on existing components rather than creating from scratch
- **Flag conflicts**: If similar functionality exists, clarify integration vs replacement approach

**Planning Framework:**

- **Use Templates**: Apply `docs/00-project/templates/plan-template.md` for structured planning
- **Constitution Check**: Validate architectural compliance before implementation:
  - ✅ Single LLM Agent Pattern (ReportWriterAgent for narrative only)
  - ✅ Pydantic Type Safety (all data structures validated)
  - ✅ Fact Traceability (all outputs traceable to source data)
  - ✅ Code-First Workers (deterministic logic in Python functions)
- **[NEEDS CLARIFICATION] Markers**: Flag ambiguous requirements for human review
- **Test-First Approach**: Define acceptance criteria before coding begins
- **Strategic Separation**: Clear what/why (business goals) vs how (technical) vs when (timeline)

#### 2. Phase Gate Enforcement

**MANDATORY SEQUENCE:** Research → Plan → Approval → Implement → Test → Review

**Key Gates:** Context7 research first, present findings to human, wait for explicit approval before any implementation  
**Violation Response:** STOP, re-sync Context7, fix issues before advancing phases

#### 3. Progress State Tracking

Maintain: **current_phase** | **steps_completed** | **open_blockers** | **standards_refs[]**

#### 4. Structured Output Discipline

All agents MUST return JSON per role schema; on mismatch, re-emit once, then STOP with "Blocked: invalid output format".

#### 5. Supervisor Agent (Gatekeeper)

On phase completion, validate agent's JSON against schema and acceptance checks.
IF invalid or checks fail → ROUTE to: planner (missing scope), debugger (test failures), development (gaps)
ELSE → advance phase and persist to run_state.json

#### 6. Persistence (Audit Trail) & Timestamp Coordination

**ORCHESTRATOR TIMESTAMP AUTHORITY:**

- **Orchestrator MUST generate single execution_timestamp** at workflow start in ISO 8601 UTC format
- **ALL sub-agent delegations MUST include execution_timestamp** parameter
- **Sub-agents MUST use orchestrator timestamp** for all reports, logs, and persistence
- **NEVER allow sub-agents to generate their own timestamps** - ensures chronological consistency

#### 7. Context7 Freshness Policy

Force Context7 re-sync when: (a) >120 min since last sync, (b) library version changes, (c) standards conflict
Record `checked_at` and lib versions in Standards Sync Log

#### 8. Global Error Protocol

```
IF encounter (missing info | conflicting standards | failing checks):
  1) Log issue with evidence
  2) Re-run Context7 search with refined keywords
  3) IF Context7 insufficient → Use WebSearch for "[library/pattern] best practices [current year]"
  4) Apply documented pattern from Context7/WebSearch or ask clarification
  5) IF still unresolved → STOP with canonical blocked payload:
     {"status":"blocked","reason":"missing_info|conflict|failed_check","owner":"planner|debugger|human","next_step":"..."}
```

## Code Review Preparation [MANDATORY]

### 🎯 DEFAULT BEHAVIOR: FAST MODE (~2 minutes)

**When you run the script without specifying a mode, it automatically uses `--fast` (linting + unit tests).**

```bash
# Just run this - automatically uses --fast mode:
uv run python scripts/prepare-code-review.py --stage-changes
```

### 📊 THREE-TIER VALIDATION SYSTEM

**Only use other modes when specifically needed:**

#### ⚡ **LINT-ONLY: Quick Formatting (~30 seconds)**

```bash
# For quick formatting fixes only - no tests
uv run python scripts/prepare-code-review.py --lint-only --stage-changes
```

**Use when:** Just fixing formatting/linting issues, very minor changes

#### 🏃 **FAST: Default Mode (~2 minutes)** ⭐

```bash
# This is the DEFAULT when no mode is specified
uv run python scripts/prepare-code-review.py --stage-changes
# Explicitly using --fast does the same thing:
uv run python scripts/prepare-code-review.py --fast --stage-changes
```

**Use when:** Normal development, most code changes, daily commits (AUTOMATICALLY SELECTED BY DEFAULT)

#### 🐌 **FULL: Complete CI Validation (~5 minutes)**

```bash
# Complete validation including integration tests - matches CI exactly
uv run python scripts/prepare-code-review.py --full --stage-changes
```

**Use when:** ONLY for integration test changes, major architectural changes, or before pushing to main

### 🎯 **SIMPLIFIED WORKFLOW**

```bash
# For 95% of development - just use the default:
uv run python scripts/prepare-code-review.py --stage-changes

# Only use --full when you've changed integration tests or major architecture:
uv run python scripts/prepare-code-review.py --full --stage-changes
```

### 📊 **PERFORMANCE CHARACTERISTICS**

| Mode          | Time  | What It Runs                     | Best For                          |
| ------------- | ----- | -------------------------------- | --------------------------------- |
| `--lint-only` | ~30s  | Linting + Formatting only        | Quick iterations, fixing linting  |
| `--fast`      | ~2min | + Unit tests (no integration)    | Normal development, daily commits |
| `--full`      | ~5min | + Integration tests (matches CI) | Before push, major changes        |

### 🔧 **ADVANCED OPTIONS**

```bash
# Legacy flags (still supported)
uv run python scripts/prepare-code-review.py --skip-tests        # Skip all tests
uv run python scripts/prepare-code-review.py --skip-cli          # Skip CLI tests
uv run python scripts/prepare-code-review.py --skip-ai-review    # Skip AI prompt

# Deployment validation (for infrastructure changes)
uv run python scripts/prepare-code-review.py --deployment-validation

# Default behavior (no flag = --fast mode)
uv run python scripts/prepare-code-review.py --stage-changes     # Uses --fast by default
```

**Pipeline includes:**

1. ✅ **Intelligent staging** (optional) - Auto-detects relevant files to stage
2. ✅ **Tier-based validation** - Optimized for development speed vs confidence
3. ✅ **Diff report generation** - Comprehensive change report for review
4. ✅ **AI review prompt** - Ready-to-submit prompt for AI code reviewer

**Critical rule:** The three-tier system prevents "passes locally, fails in CI" by ensuring `--full` matches CI exactly.

## Common Development Commands

### Running Tests

```bash
# Primary: Use test runner script (with uv run - see UV setup above)
uv run python scripts/testing/run_tests.py unit        # Unit tests only
uv run python scripts/testing/run_tests.py integration # Integration tests
uv run python scripts/testing/run_tests.py e2e         # End-to-end tests
uv run python scripts/testing/run_tests.py coverage    # Full coverage report

# For single files or debugging:
pytest tests/test_specific_file.py -v
pytest -k "test_function_name"
```

### Running Applications

```bash
# API development server
uvicorn services.api.main:app --reload

# CLI workflow (with uv run - see UV setup above)
python cli/main.py "Apple Inc"
```

## Deployment Validation [FOR INFRASTRUCTURE CHANGES]

**Standalone usage:**

```bash
# Basic validation (auto-skips if no deployment)
uv run python scripts/deployment/validate_deployment.py --port-forward

# Full deployment cycle
uv run python scripts/deployment/validate_deployment.py --deploy --cleanup
```

**Code review integration:**

- Add `--deployment-validation` flag for API/infrastructure changes
- Auto port-forwarding, non-blocking (warnings only)
- Use for: API endpoints, K8s configs, database changes
- Skip for: pure business logic, UI work

## Git Workflow [Context7-Guided Standards]

**Integrated with Enhanced Development Workflow:**
Git operations follow the Context7-guided development workflow (Phases 1-6) with LIVING_SPRINT.md integration.

**Daily Implementation Pattern:**

```bash
# CONTEXT7-GUIDED WORKFLOW (Use This!)
# [Phase 5: Implementation] - After completing Phases 1-4 planning and approval
uv run python scripts/prepare-code-review.py --stage-changes  # Complete code review preparation
# For infrastructure/API changes, add: --deployment-validation

# Commit with Context7-guided message format and LIVING_SPRINT.md update
git commit -m "type(scope): description

Update LIVING_SPRINT.md: Mark chunk X completed, advance to next todo item

Context7 sources: library/pattern references used"
git push origin main                         # Push to remote

# ALTERNATIVE: Manual staging control for debugging
git status                                   # Check what changed
git add feature1_files...                    # Stage specific files
git add docs/00-project/LIVING_SPRINT.md     # ALWAYS include sprint progress
uv run python scripts/prepare-code-review.py # Run pipeline on staged files
# [PAUSE] Human reviews artifacts and approves changes
git commit -m "type(scope): description"    # Commit approved changes with sprint update
```

**Context7-Guided Commit Standards:**
Following GitLab/GitHub industry standards researched via Context7:

**📖 Complete Guide:** `.claude/docs/01-guides/commit-message-guide.md` (templates, scopes, examples)

```bash
# Commit message template (dynamic based on change type)
<type>(scope): <description>

[optional body with Context7 source references]
[optional LIVING_SPRINT.md progress update]

[optional footer: Closes #123, Breaking-change: details]
```

**Commit types:** feat, fix, refactor, test, docs, style, perf, ci
**Project scopes:** agents, core, orchestrator, planner, api, cli, workers, scripts, deployment, docs, etc.

**Feature Impact Analysis and Staging:**

- **Export all changes** to `code-review-diff.txt` before staging anything
- **Human analyzes complete feature impact** including:
  - Files implementing the feature (follows approved Phase 3 design)
  - Tests for the feature (Context7-guided testing patterns)
  - Dependencies that this feature relies on
  - Dependents that rely on this feature
  - Related configuration or documentation changes
  - **LIVING_SPRINT.md progress updates** (MANDATORY)
- **Stage and commit by complete chunks** - atomic units from Phase 1 breakdown
- **Each commit represents one working chunk** with todo list progress

**Critical habits:**

- Export diffs to review file before staging or committing
- Check `git status` before and after operations
- Keep commits atomic (one logical change per commit)
- **Always include LIVING_SPRINT.md updates** in commits
- Reference Context7 sources in commit messages when applicable
- Don't assume repository state - always check first

## Spec-Driven Development (SDD) Workflow [MANDATORY]

### SDD Command Interface

Following GitHub spec-kit methodology with Gauntlet Agents specializations:

**`/spec` - Feature Specification Creation**

- **Sub-Agent:** `planner-agent`
- **Output:** Complete feature specification using `plan-template.md`
- **Includes:** Context7 research, Constitutional Check, [NEEDS CLARIFICATION] markers

**`/plan` - Technical Implementation Planning**

- **Sub-Agent:** `planner-agent`
- **Input:** Approved feature specification
- **Output:** Detailed technical plan with Context7 patterns and architectural compliance

**`/tasks` - Executable Task List Generation**

- **Sub-Agent:** `planner-agent`
- **Input:** Approved technical plan
- **Output:** Sequential task list with sub-agent assignments using `task-template.md`

**`/implement` - Sub-Agent Task Execution**

- **Execution:** Main agent orchestrates specialized sub-agents per task list
- **Process:** Task-by-task execution with LIVING_SPRINT.md integration
- **Coordination:** Main agent coordinates all sub-agent interactions (never sub-agent-to-sub-agent)

### 7-Phase SDD Workflow Process

**🚨 CRITICAL RULE: FOLLOW COMPLETE SDD WORKFLOW**

**Common Violations to Avoid:**

- Starting implementation without completing specify → plan → tasks phases
- Skipping human approval gates after each planning phase
- Bypassing sub-agent coordination in implementation phase

**Enforcement:** ANY attempt to implement without completing SDD workflow violates protocol.

### Phase 1: `/spec` - Feature Specification [PLANNING]

**Command:** Use `planner-agent` with feature brief  
**Objective:** Create comprehensive feature specification using spec-kit methodology

**Process:**

1. **Main Agent** launches `planner-agent` with specification requirements
2. **Planner Agent** creates feature document using `plan-template.md`:
   - Context7 research for relevant libraries/patterns
   - Constitutional Check architectural compliance
   - [NEEDS CLARIFICATION] markers for ambiguities
   - Test-first acceptance criteria with golden set examples
   - Success metrics and Definition of Done

**Output:** `docs/feature-plans/[feature-name].md` with complete specification  
**Pause Point:** Human reviews and approves specification before proceeding

### Phase 2: `/plan` - Technical Implementation Planning [PLANNING]

**Command:** Use `planner-agent` with approved specification  
**Objective:** Generate detailed technical plan with Context7 validation

**Process:**

1. **Main Agent** launches `planner-agent` with approved specification
2. **Planner Agent** enhances specification with:
   - Detailed technical architecture section
   - Context7-researched implementation patterns
   - Integration points and dependencies analysis
   - Testing strategy with specific frameworks
   - Implementation phases with clear sequencing

**Output:** Enhanced feature document with complete technical plan  
**Pause Point:** Human reviews and approves technical approach before proceeding

### Phase 3: `/tasks` - Task List Generation [PLANNING]

**Command:** Use `planner-agent` with approved technical plan  
**Objective:** Generate executable task list with sub-agent assignments

**Process:**

1. **Main Agent** launches `planner-agent` with approved technical plan
2. **Planner Agent** creates task breakdown using `task-template.md`:
   - Sequential task list derived from implementation phases
   - Sub-agent assignments per task type (test-runner, development, debugger, etc.)
   - Parallel task identification with [P] flags
   - Preflight documentation requirements per task
   - Context7 research topics per task
   - Existing codebase search keywords per task

**Output:** Complete task list in LIVING_SPRINT.md format  
**Pause Point:** Human reviews task breakdown and sequencing before proceeding

### Phase 4: `/implement` - Sub-Agent Task Execution [IMPLEMENTATION]

**Command:** Main agent coordinates sub-agents per task list  
**Objective:** Execute tasks using specialized sub-agents with systematic coordination

**Process:**

```
FOR EACH TASK in approved task list:
  1. Main Agent loads task context (preflight docs, Context7 topics)
  2. Main Agent launches appropriate sub-agent with complete task context:
     - test-runner-agent: Unit tests, integration tests, validation
     - development-agent: Core implementation, Pydantic models, workers
     - debugger: Test failures, integration issues, performance
     - code-quality: Security, best practices, architecture compliance
     - development: Code structure, modularization, optimization
  3. Sub-Agent executes task following mcp-agent-optimization.md guidelines
  4. Main Agent validates task completion
  5. Main Agent updates LIVING_SPRINT.md progress
  6. Main Agent proceeds to next task
```

**Integration Points:**

- Code review preparation after each implementation task
- Context7 compliance validation by each sub-agent
- LIVING_SPRINT.md progress tracking throughout

### Phase 5: Collaborative Code Review [VALIDATION]

**Objective:** Human review of complete implementation with automated feedback resolution

**Process:**

1. **Main Agent** runs code review preparation and presents implementation summary
2. **Human** reviews comprehensive analysis
3. **IF feedback required:** Main Agent launches `handle-code-review` agent
4. **Code Review Agent** addresses feedback systematically using sub-agents as needed
5. **Main Agent** validates all feedback resolved and integration successful

### Phase 6: Feature Integration & Validation [VALIDATION]

**Objective:** End-to-end feature validation and integration testing

**Process:**

1. **Main Agent** launches `test-runner-agent` for comprehensive integration validation
2. **Integration testing** with full system context and realistic data
3. **Performance validation** against SLO requirements if applicable
4. **Documentation updates** for user-facing changes or API modifications

### Phase 7: Feature Completion & Sprint Advancement [COMPLETION]

**Objective:** Mark feature complete and advance to next feature

**Process:**

1. **Definition of Done validation** against original specification acceptance criteria
2. **LIVING_SPRINT.md final update** - mark feature complete with summary
3. **Success metrics validation** where measurable outcomes were defined
4. **Strategic impact assessment** - how feature advances product vision per SPEC.md
5. **Next feature identification** from current sprint backlog or active roadmap

## Human Interaction Patterns [MANDATORY]

### During Planning and Architecture

**Feature implementation bookends:**

- **Beginning of feature:** Present current state and proposed next steps
- **End of feature:** Summarize what was accomplished and identify next priorities based on:
  - `docs/00-project/SPEC.md` - System requirements and business goals
  - `docs/00-project/ROADMAP-*.md` - Quarterly roadmaps and strategic milestones
  - `docs/00-project/LIVING_SPRINT.md` - Current state and immediate next steps

### During Development

**Development workflow with Context7-guided touchpoints:**

**Follows Enhanced Development Workflow (Phases 1A-6):**

1. **Phases 1A-4 Planning [MULTIPLE PAUSE POINTS]:**
   - **Phase 1A:** Present feature definition document for review and approval
   - **Phase 2:** Present completed feature document with Context7 technical plan added
   - **Phase 3:** Collaborative review of complete feature document (definition + technical plan)
   - **Phase 4:** Refine feature document based on feedback until approved

2. **Phase 5 Test-First Implementation:**
   - **Write tests first** based on acceptance criteria from approved feature document
   - **Validate test patterns** against Context7-researched testing frameworks
   - **Implement minimal code** to make tests pass (following TDD red-green-refactor cycle)
   - **Apply Context7 patterns** documented in technical plan during refactor phase
   - **Verify Constitution compliance** throughout implementation
   - **Run pre-commit validation** (see Code Review section for commands)
   - **Fix any issues** until all validations pass

3. **Code review preparation [PAUSE POINT]:**
   - Run `git diff > code-review-diff.txt` to export changes
   - Present to human with:
     - **Feature document adherence** - Implementation matches approved technical plan
     - **Context7 pattern usage** - Which researched patterns from feature document were applied
     - **Test coverage** - Following testing strategies from feature document
     - **LIVING_SPRINT.md progress** - Todo item advancement
     - Questions or concerns about the implementation

4. **Code review resolution:**
   - **[MANDATORY] Log ALL feedback** in `docs/04-guides/code-review/feedback-log.md` using standard format
   - **For each issue raised:** Validate with Context7 before implementing
     - Check if the suggested approach aligns with library best practices
     - Verify if current implementation already follows documentation
     - Compare against approved feature document technical plan
     - Propose alternatives if suggestion conflicts with researched standards
   - **For questions:** Provide clear, reasoned responses with Context7 sources
   - **For suggestions:** Evaluate against project goals and Context7 guidance
   - Run validation again after changes

5. **Final approval and commit:**
   - Confirm all issues addressed per Context7 standards
   - Ensure all questions answered with source references
   - **Update LIVING_SPRINT.md** with chunk completion status
   - Get explicit approval before proceeding to commit
   - **Phase 6:** Loop back to next chunk following same process

**Critical principle:** Follow Global Workflow Enforcement Context7 validation during code review.

### During Code Review

**Receiving and incorporating feedback:**

- Human code review feedback takes precedence over automated suggestions
- Ask clarifying questions when feedback conflicts with existing architecture
- Validate suggestions against official documentation using Context7 when appropriate
- Propose alternatives when direct implementation isn't feasible
- Confirm understanding before making major architectural changes

**Goal:** Collaborative development that respects human oversight while maintaining development efficiency.

## Context7 Integration

**Complete Guide**: `docs/04-guides/mcp-integration-guide.md` (AUTHORITY: Context7 Usage & Token Optimization)

**Quick Reference**:

- **Standard research**: 5000 tokens (default)
- **Basic validation**: 2000 tokens (quick checks)
- **Deep analysis**: 8000 tokens (comprehensive)
- **Topic specificity**: Use specific topics to reduce response size (15k+ → 3k)

**Dynamic Token Allocation**:

```
Research Depth  | Base Tokens | With Topic Filter
----------------|-------------|-------------------
Quick lookup    | 2,000       | 1,500
Standard query  | 5,000       | 3,000
Deep dive       | 8,000       | 5,000
```

**Emergency Context Management**: See `docs/04-guides/mcp-integration-guide.md` for >100k token research patterns with Memory tool

**Documentation Search Priority** (UPDATED 2025-10-07):

1. **Context7 FIRST** - Official docs, latest versions (via researcher-external agent)
2. **Web search SECOND** - If not in Context7 (via researcher-external agent, auto-routes)
3. **Fallback**: Official website documentation directly
