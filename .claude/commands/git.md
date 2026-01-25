---
argument-hint: '[prepare] [commit <groups>] [--skip-validation] [--skip-quality]'
description: 'Two-phase git workflow: prepare analyzes and presents summary, commit executes selected groups.'
allowed-tools: Task, Bash(git:*), Bash(gh:*), Read, Grep
model: opus
---

# /git Command

Two-phase git workflow that analyzes changes, groups files by category, runs quality gates, and commits selected groups.

## Usage

| User Says | Action |
|-----------|--------|
| `/git` or `/git prepare` | Run prepare workflow |
| `/git prepare --skip-validation` | Skip CI validation step |
| `/git prepare --skip-quality` | Skip quality gates |
| `/git commit all` | Commit all READY_TO_COMMIT groups |
| `/git commit 1-3` | Commit groups 1 through 3 |
| `/git commit 1,3,5` | Commit specific groups |

## Prerequisites

- Working directory must have uncommitted changes (staged or unstaged)
- Git repository must be initialized
- Not in merge/rebase conflict state

## Phase 1: PREPARE Execution

Execute when user runs `/git` or `/git prepare`:

1. **Collect Changes**:
   ```bash
   git status
   git diff --name-only
   git diff --cached --name-only
   ```

2. **Validation** (skippable with `--skip-validation`):
   
   **[GATE 2: VALIDATION]** - CI must pass before grouping
   
   ```
   IF --skip-validation flag provided:
     SKIP gate → proceed to Step 3
   ELSE:
     Task(debugger): """
       Operation: validate_pre_commit
       
       Validate changes before commit using:
         scripts/prepare-code-review.py --fast
       
       Max iterations: 3
       Auto-fix: linting, formatting, simple test failures
       Document any unfixable issues.
       
       Return schema:
       {
         "status": "SUCCESS|FAILURE",
         "agent_specific_output": {
           "validation_status": "PASS|FAIL",
           "fixes_applied": [...],
           "iteration_count": 1-3
         }
       }
     """
   ```
   
   **Gate Conditions:**
   - **PASS** (status=SUCCESS): Proceed to Step 3 (Grouping)
   - **FAIL** (status=FAILURE): 
     - Display `failure_details.unfixable_issues` to user
     - Display `failure_details.recovery_suggestions`
     - Suggest: "Use `--skip-validation` to bypass if issues are acceptable"
     - **BLOCK** - Do NOT proceed to Step 3
   
   **Timeout**: 120s (debugger manages internal retry loop)

3. **Grouping**:
   ```
   Task(git-github, operation="analyze_changes"): "Categorize and group files by domain"
   ```
   - Groups files by: api, core, tests, docs, config, agents, workflows

4. **Quality Gates** (skippable with `--skip-quality`):
   ```
   FOR EACH group:
     Task(python-code-reviewer): "Review files for quality issues"
   ```
   - Sets status: READY_TO_COMMIT (score >= 0.85), NEEDS_REVIEW (0.70-0.84), BLOCKED (< 0.70)

5. **Present Summary**: Display summary table to user and await selection

## Phase 2: COMMIT Execution

Execute when user runs `/git commit <groups>`:

1. **Parse Group Selection**:
   - `all`: All groups with status READY_TO_COMMIT
   - `1-3`: Groups 1 through 3 (range)
   - `1,3,5`: Specific groups (comma-separated)

2. **Execute Commits**:
   ```
   FOR EACH selected group:
     Task(git-github, operation="execute_commits"): "Create commit with conventional message"
   ```
   - Generates conventional commit message (feat/fix/docs/test/refactor)
   - Stages files for the group
   - Creates commit

3. **Present Results**: Display commit results table

## Output Formats

### Prepare Summary Table

| # | Category | Files | Status | Quality Score |
|---|----------|-------|--------|---------------|
| 1 | api | 3 | READY_TO_COMMIT | 0.92 |
| 2 | tests | 2 | NEEDS_REVIEW | 0.78 |
| 3 | docs | 1 | READY_TO_COMMIT | 0.95 |

**Status Legend**:
- `READY_TO_COMMIT`: Quality score >= 0.85, no blockers
- `NEEDS_REVIEW`: Quality score 0.70-0.84, minor issues
- `BLOCKED`: Quality score < 0.70, must resolve before commit

### Commit Results

```
Commit Group 1 committed: abc123f - feat(api): add user endpoint
Commit Group 2 committed: def456a - test(api): add user endpoint tests
Skipped Group 3 skipped (BLOCKED)
```

## Error Handling

| Error | Recovery |
|-------|----------|
| CI validation fails | Display unfixable issues + recovery suggestions, BLOCK workflow, suggest `--skip-validation` |
| Agent timeout (>60s) | Skip agent, mark group NEEDS_REVIEW |
| git command fails | Report error, suggest manual resolution |
| No changes to commit | Report "Working tree clean" |
| Group status BLOCKED | Skip group, report reason |
| Invalid group selection | Report valid range, prompt for correction |

## Timeouts

| Operation | Timeout | Fallback |
|-----------|---------|----------|
| CI validation | 120s | Skip, warn user |
| Quality gate (per agent) | 60s | Skip agent, mark NEEDS_REVIEW |
| Total prepare | 300s | Present partial results |

## Delegation Rule

ALL operations delegate to sub-agents:
- Validation: `Task(debugger)`
- Grouping: `Task(git-github)`
- Quality: `Task(python-code-reviewer)`
- Commits: `Task(git-github)`

## Skill Reference

See `.claude/skills/git-workflow/` for supporting documentation:

- `reference/execution-contract.md` - Contract between command and agents
- `reference/agent-matrix.md` - Agent responsibilities and capabilities
- `reference/category-guidelines.md` - File categorization rules

## Safety

**SAFE**: git status, diff, log, add, commit, fetch, reset HEAD

**FORBIDDEN**: git reset --hard, clean -fd, checkout --, stash drop
