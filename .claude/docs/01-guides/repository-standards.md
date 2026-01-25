---
title: "Repository Standards & Git Workflow"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---

## Repository Standards & Git Workflow

**Purpose**: Git workflow standards, branch naming, commit conventions, and PR process for Gauntlet Agents

**Audience**: All contributors, orchestrator, agents performing git operations

**Quick Reference**: Branch first, validate, then commit

---

## Branch Naming (MANDATORY)

- `feature/NNN-description` - New features
- `bugfix/NNN-description` - Bug fixes
- `system/description` - Config changes
- `docs/description` - Documentation

**Examples**:

- `feature/042-add-portfolio-analyzer`
- `bugfix/128-fix-token-counting`
- `system/update-security-hooks`
- `docs/improve-agent-guide`

---

## Commit Message Format

**Structure**: `type: brief description` (longer explanation optional)

**Types**:

- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation only
- `refactor` - Code restructuring (no behavior change)
- `test` - Test additions or fixes
- `chore` - Build process, dependencies, tooling

**Examples**:

- `feat: add Context_Quality scoring to ORIENT phase`
- `fix: resolve path normalization on Windows`
- `docs: add progressive disclosure to agent-creation-guide`
- `refactor: extract validation logic to separate module`

---

## Git Workflow (CRITICAL)

**Golden Rule**: NEVER run git commands automatically after making changes

**Process**:

1. Create feature branch: `git checkout -b feature/NNN-description`
2. Make changes
3. Run tests: `uv run pytest`
4. **Validation** (choose one):
   - `/git prepare` - Agent-driven, comprehensive (includes linting, type checking, tests, security)
   - `scripts/prepare-code-review.py --fast` - Script-only, faster (validation without agents)
5. Stage files: `git add path/to/file.py` (only after validation PASS)
6. Commit: `git commit -m "type: description"`
7. Create PR: `gh pr create`

**Permission Protocol**:

- ✅ ALWAYS ask user permission before `git add`, `git commit`, or `git push`
- ❌ NEVER run git commands automatically
- Exception: User explicitly says "commit this" or "push this"

---

### Multi-Developer Workflow

When working on shared branches with other developers:

**Daily Pattern**:

1. **Start of session**: `git pull --rebase`
2. **Before commits**: `/git prepare` (includes automatic remote check)
3. **After commits**: `git pull --rebase` before push
4. **If diverged**: Follow conflict resolution patterns

**Key Principles**:

- **Pull often**: Reduces conflicts (at least before each commit/push)
- **Commit atomically**: Single logical change per commit
- **Push regularly**: Don't hoard commits locally
- **Communicate**: Signal intentions to team (avoid simultaneous edits)

**Automated Support**:

- `/git prepare` automatically checks remote branch state
- Divergence warnings displayed with recommendations
- Staging area automatically reset before each commit group
- No manual staging area cleanup required

**Conflict Resolution**:

```bash
# If pull shows conflicts
git status                    # Check conflicted files
# ... resolve conflicts in editor ...
git add <resolved-files>      # Stage resolutions
git rebase --continue         # Continue rebase

# If too complex
git rebase --abort            # Return to pre-rebase state
git pull                      # Use merge instead of rebase
```

**Complete Guide**: See `.claude/docs/01-guides/git/multi-developer-workflow.md` for:

- Pull strategies (rebase vs merge decision matrix)
- Conflict prevention techniques
- Staging area management
- Command reference
- Anti-patterns to avoid

---

## Pre-Commit Validation Options

### Option 1: `/git prepare` (Recommended)

- **What**: Agent-driven comprehensive validation
- **Runs**: Linting (ruff), type checking (mypy), unit tests (pytest), security scans
- **When**: Complex changes, multiple files, before important commits
- **See**: `.claude/commands/git.md` for complete workflow

### Option 2: `scripts/prepare-code-review.py --fast`

- **What**: Script-only validation (no agents)
- **Runs**: Linting, type checking, unit tests, security checks
- **When**: Quick validation, simple changes, faster iteration
- **Output**: Pass/fail with error details

---

## PR Process

**7-Step Workflow**:

1. **Branch from main**: Create feature branch
2. **Make changes**: Implement feature/fix
3. **Run tests**: Verify tests pass locally
4. **Validate**: Use `/git prepare` or `prepare-code-review.py --fast`
5. **Create PR**: `gh pr create` with descriptive title and summary
6. **Address feedback**: Respond to code review comments
7. **Squash & merge**: Clean up commit history on merge

**PR Title Format**: Same as commit messages (`type: description`)

**PR Description**:

- **Summary**: 1-3 bullet points explaining changes
- **Test plan**: How to verify the changes
- **Context**: Links to related issues/specs if applicable

---

## References

- **Complete Git Command Reference**: `.claude/commands/git.md`
- **Security Validation**: `.claude/hooks/security/validate_command.py`
- **Pre-commit Script**: `scripts/prepare-code-review.py`

---

**Last Updated**: 2025-11-05
