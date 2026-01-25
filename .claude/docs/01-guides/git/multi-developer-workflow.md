---
title: Multi-Developer Git Workflow Guide
description: Best practices for collaborative development on shared feature branches with automated git workflow support
tags: [git, workflow, collaboration, multi-developer]
last_updated: 2025-01-12
version: 1.0
date: 2025-01-12
status: ACTIVE
---

## Multi-Developer Git Workflow Guide

**Purpose**: Best practices for collaborative development on shared feature branches with automated git workflow support

**Last Updated**: 2025-01-12

---

## Table of Contents

1. [Overview](#overview)
2. [Core Principles](#core-principles)
3. [Workflow Patterns](#workflow-patterns)
4. [Pull Strategies](#pull-strategies)
5. [Staging Area Management](#staging-area-management)
6. [Conflict Prevention](#conflict-prevention)
7. [Conflict Resolution](#conflict-resolution)
8. [Command Reference](#command-reference)
9. [Anti-Patterns](#anti-patterns)

---

## Overview

**Scenario**: Multiple developers working on shared feature branches with:

- Regular commits throughout the day (not just end-of-day)
- Selective file commits (atomic changesets)
- Automated workflow via `/git prepare` and `/git commit`
- No local branch switching (single active branch per developer)

**Assumptions**:

- Feature branch already exists (created via GitHub PR or team lead)
- You are already checked out on the correct branch
- Remote repository has latest changes from other developers
- You want to commit only specific file groups, not all changes

---

## Core Principles

### 1. Pull Often, Push Incrementally

**Frequency**: Pull at start of each work session, before creating commits, and before pushing

**Why**: Reduces drift between local and remote branches, prevents conflicts

**Pattern**:

```bash
# Start of day
git pull --rebase

# Before /git prepare
git pull --rebase

# After /git commit (before push)
git pull --rebase
git push
```

### 2. Atomic Commits

**Definition**: One logical change per commit (single purpose, self-contained)

**Benefits**:

- Easier code review (reviewers understand single concept)
- Simpler conflict resolution (clear boundaries)
- Easier rollback (revert specific feature without breaking others)
- Better git history (clear narrative of project evolution)

**Examples**:

- ✅ GOOD: "feat(auth): add JWT token validation"
- ✅ GOOD: "fix(api): resolve null pointer in user endpoint"
- ❌ BAD: "updates" (vague, multi-purpose)
- ❌ BAD: "fix auth and update docs and refactor tests" (mixed concerns)

### 3. Clean Staging Area

**Rule**: Always unstage everything before selective commits

**Why**: Prevents accidental commits of unrelated files from previous operations

**Pattern**:

```bash
# Before committing specific group
git restore --staged .  # Unstage all files

# Then stage only intended files
git add file1.py file2.py
git commit -m "feat: specific change"
```

**Automated**: `/git commit` workflow automatically resets staging area before each commit group

### 4. Short-Lived Branches

**Recommendation**: Merge feature branches within 1-2 days

**Why**: Reduces conflicts, easier integration, faster feedback

**If long-running required**:

- Rebase on main daily: `git fetch origin && git rebase origin/main`
- Break large features into smaller sub-tasks
- Use feature toggles for incomplete features

---

## Workflow Patterns

### Pattern 1: Daily Development Workflow

**Morning (Start of Session)**:

```bash
# 1. Check current state
git status

# 2. Pull latest changes
git pull --rebase

# 3. Check for conflicts
# If conflicts, resolve them before starting work
```

**During Work (Regular Commits)**:

```bash
# 1. Make changes to files

# 2. Prepare commits (analyzes all changes, generates groups)
/git prepare

# 3. Review groups, select relevant ones
# Groups shown with files, change types, confidence scores

# 4. Commit selected groups only
/git commit --groups=1,3,5

# 5. Pull again (others may have pushed)
git pull --rebase

# 6. Push your commits
git push
```

**End of Day (Clean Up)**:

```bash
# 1. Commit any remaining work
/git prepare
/git commit

# 2. Pull and push
git pull --rebase
git push

# 3. Verify clean state
git status  # Should be "nothing to commit, working tree clean"
```

### Pattern 2: Selective Commit Workflow

**Scenario**: You have changes for Feature A (done) and Feature B (WIP), want to commit only Feature A

**Steps**:

```bash
# 1. Analyze all changes
/git prepare

# Output shows groups:
# Group 1: feat(feature-a) - Feature A implementation (5 files)
# Group 2: feat(feature-b) - Feature B WIP (3 files)
# Group 3: refactor(core) - Shared utilities (2 files)

# 2. Commit only Feature A
/git commit --groups=1

# Result: Feature A committed, Feature B remains uncommitted for later
```

**Benefits**:

- Feature A can be reviewed/merged independently
- Feature B remains local until complete
- Shared utilities (Group 3) can be committed separately

### Pattern 3: Collaborative Branch Workflow

**Scenario**: Developer A and B both work on `feature/auth-improvements`

**Developer A**:

```bash
# Morning
git pull --rebase

# Work on login flow
# ...

# Commit login changes
/git prepare
/git commit --groups=1  # Login flow group

# Pull (B may have pushed)
git pull --rebase

# Push
git push
```

**Developer B** (working simultaneously):

```bash
# Morning
git pull --rebase  # Gets A's earlier work

# Work on registration flow
# ...

# Before committing
git pull --rebase  # Gets A's login commit

# Commit registration changes
/git prepare
/git commit --groups=2  # Registration flow group

# Push
git push
```

**Key**: Frequent pulls keep both developers synchronized, reducing conflicts

---

## Pull Strategies

### Decision Matrix

| Situation | Command | Reason |
|-----------|---------|--------|
| **Start of work session** | `git pull --rebase` | Get latest changes, clean history |
| **Before `/git prepare`** | `git pull --rebase` | Ensure analyzing current state |
| **Before creating PR** | `git pull --rebase` | Clean history for review |
| **Shared branch (others working)** | `git pull --rebase` | Replay your commits on top |
| **Uncommitted changes exist** | `git stash && git pull --rebase && git stash pop` | Preserve WIP |
| **Complex conflicts expected** | `git pull` (merge) | Safer, preserves full context |
| **Uncertain** | `git fetch` then decide | Review changes before integrating |

### Rebase vs Merge

**Use `git pull --rebase` (recommended default)**:

- ✅ Creates linear history (easier to follow)
- ✅ Cleaner commit timeline
- ✅ Easier to review in PRs
- ✅ Standard for feature branches
- ⚠️ Requires resolving conflicts commit-by-commit

**Use `git pull` (merge) when**:

- Complex conflicts expected
- Working with junior developers (safer)
- Need full audit trail
- When in doubt (merging is safer)

### Auto-Stash Configuration

**What it does**: Automatically stashes uncommitted changes before pull, reapplies after

**Enable**:

```bash
git config --global rebase.autoStash true
```

**When to use**: Small, temporary changes only

**Warning**: For substantial work-in-progress, commit to branch instead (stash can be lost)

---

## Staging Area Management

### Unstaging Commands

**Modern (Git 2.23+)**:

```bash
# Unstage specific file (keeps modifications)
git restore --staged <file>

# Unstage all files
git restore --staged .
```

**Legacy (still works)**:

```bash
# Unstage specific file
git reset HEAD <file>

# Unstage all files
git reset HEAD
```

**Automated**: `/git commit` workflow automatically runs `git reset HEAD` before staging files for each commit group

### Selective Staging

**Interactive staging** (for manual commits):

```bash
git add -p <file>

# Options:
# y - stage this hunk
# n - skip this hunk
# s - split into smaller hunks
# e - manually edit hunk
```

**Use cases**:

- Separate unrelated changes in same file
- Create multiple logical commits from single file
- Review changes during staging

**Automated**: `/git prepare` uses FileGrouper to create logical groups automatically

### Pre-Commit Checklist

Before committing (manual or via `/git commit`):

1. ✅ `git status` - Verify which files staged
2. ✅ `git diff --staged` - Review exact changes
3. ✅ Unstage unrelated files if needed
4. ✅ Ensure only related changes together
5. ✅ Write descriptive commit message

---

## Conflict Prevention

### Communication Strategies

**Signal intentions**:

- "Refactoring auth module this afternoon" (Slack/Teams)
- "Working on API endpoints in services/api/" (GitHub issue comment)
- "Planning database migration for users table" (standup)

**Benefits**: Prevents hours of conflict resolution pain

### Code Organization

**Module ownership**:

- Clear boundaries (who owns which modules)
- Reduces overlapping work
- Easier to coordinate changes

**Shared files strategy**:

- Communicate before modifying shared utilities
- Break changes into smaller commits (easier to merge)
- Use import aliases to reduce coupling

### Frequency Patterns

**Pull frequency**: At minimum before each commit push, ideally multiple times per day

**Commit frequency**:

- Whenever logical unit complete (not just end-of-day)
- Small, atomic commits reduce conflict surface area
- Push regularly (don't hoard commits locally)

**Rebase frequency** (feature branch on main):

- Daily for active branches
- Before creating pull request
- After major merges to main

### Short-Lived Branches

**Target**: Merge within 1-2 days

**Benefits**:

- Single most effective conflict prevention technique
- Reduces drift between feature branch and main
- Enables parallel development without collisions

**Breaking down work**:

- Split large features into self-contained tasks
- Use feature toggles for incomplete features
- Incremental delivery reduces risk

---

## Conflict Resolution

### Identifying Conflicts

**After pull**:

```bash
git pull --rebase
# Output: CONFLICT (content): Merge conflict in <file>
# Automatic merge failed; fix conflicts and then commit the result.

# Check status
git status
# Shows "Unmerged paths" and conflicted files
```

### Resolution Workflow

**Step-by-step**:

```bash
# 1. Open conflicted files, look for markers
# <<<<<<< HEAD
# Your changes
# =======
# Remote changes
# >>>>>>> commit-sha

# 2. Edit files to resolve conflicts
# Keep your changes, remote changes, or combine both

# 3. Remove conflict markers (<<<, ===, >>>)

# 4. Stage resolved files
git add <resolved-files>

# 5. Continue rebase
git rebase --continue

# 6. Repeat for each conflicting commit
```

**Abort if too complex**:

```bash
git rebase --abort  # Return to pre-rebase state
git pull            # Use merge instead
```

### Conflict Resolution Tools

**Visual merge tools**:

```bash
git mergetool
```

**IDE integration**:

- VS Code: Built-in 3-way merge view
- IntelliJ: Advanced merge tool
- PyCharm: Side-by-side comparison

**Advanced commands**:

```bash
# Show commits causing conflict
git log --merge

# Show 3-way diff (original + both versions)
git config --global merge.conflictStyle diff3
```

### Rerere (Reuse Recorded Resolution)

**What it does**: Saves conflict resolutions, auto-applies to future conflicts

**Enable**:

```bash
git config --global rerere.enabled true
```

**Benefits**:

- If same conflict recurs during rebase, Git auto-resolves
- Saves time on repeated conflicts
- Useful for frequent rebase workflows

---

## Command Reference

### Daily Commands

```bash
# Start of session
git status                # Check current state
git pull --rebase         # Get latest changes

# During work
/git prepare              # Analyze all changes, generate groups
/git commit --groups=X,Y  # Commit specific groups
git pull --rebase         # Pull again before push
git push                  # Push commits

# Check state
git status                # Verify clean working directory
git log --oneline -5      # Review recent commits
```

### Staging Management

```bash
# Unstage files (modern)
git restore --staged .         # Unstage all
git restore --staged <file>    # Unstage specific file

# Unstage files (legacy)
git reset HEAD                 # Unstage all
git reset HEAD <file>          # Unstage specific file

# Review staging
git status                     # Show staged/unstaged files
git diff --staged              # Show staged changes
```

### Pull Strategies

```bash
# Rebase (cleaner history)
git pull --rebase
git pull --rebase --autostash  # With auto-stash

# Merge (safer)
git pull

# Fast-forward only (safest, requires explicit decision)
git config --global pull.ff only
```

### Conflict Resolution

```bash
# During rebase conflict
git status                     # Show conflicted files
# ... resolve conflicts ...
git add <resolved-files>       # Stage resolutions
git rebase --continue          # Continue rebase

# Abort if needed
git rebase --abort             # Return to pre-rebase state

# Visual tools
git mergetool                  # Launch merge tool
```

### Branch Maintenance

```bash
# Check divergence
git fetch
git status                     # Shows ahead/behind status

# Rebase on main
git fetch origin
git rebase origin/main

# Update feature branch
git pull --rebase              # From remote feature branch
```

### Recovery Commands

```bash
# View reflog (all HEAD movements)
git reflog

# Restore to previous state
git reset --hard <commit-sha>

# Recover lost commits
git reflog                     # Find commit SHA
git cherry-pick <commit-sha>   # Apply to current branch
```

---

## Anti-Patterns

### ❌ DON'T: Use git stash as primary workflow

**Problem**: Stash is temporary storage, can be lost, hard to manage

**Instead**: Commit work to branch (use `git commit --amend` if needed, or squash later)

### ❌ DON'T: Rebase public branches

**Problem**: Rewrites history others depend on, causes confusion and conflicts

**Instead**: Only rebase private feature branches before pushing

### ❌ DON'T: `git add .` blindly

**Problem**: Stages unrelated files, debug code, temporary changes

**Instead**: Use `/git prepare` to review groups, or `git add -p` for manual control

### ❌ DON'T: Mix file moves with logic changes

**Problem**: Conflicts become impossible to resolve (can't separate rename from modification)

**Instead**: Separate commits: first commit moves files, second commit modifies content

### ❌ DON'T: Long-running feature branches

**Problem**: Merge conflicts multiply over time, integration becomes painful

**Instead**: Merge within 1-2 days, or rebase on main daily

### ❌ DON'T: Push directly to main

**Problem**: Bypasses code review, breaks CI, no rollback safety

**Instead**: Use feature branches + pull requests

### ❌ DON'T: Force push without coordination

**Problem**: Overwrites others' work, destroys team's commits

**Instead**: Use `git push --force-with-lease` (checks remote state), coordinate with team

### ❌ DON'T: Ignore `.gitignore`

**Problem**: Build artifacts, logs, secrets in repository

**Instead**: Configure `.gitignore` properly, use `git check-ignore` to test

### ❌ DON'T: Generic commit messages

**Problem**: "fix stuff", "updates" provide no context

**Instead**: Use Conventional Commits format (generated automatically by `/git commit`)

### ❌ DON'T: Skip pulling before push

**Problem**: Diverged branches, rejected push, wasted time

**Instead**: Always pull before push (automated in `/git` workflow)

---

## Configuration Recommendations

### Essential Global Config

```bash
# Pull strategy (choose one)
git config --global pull.rebase true     # Cleaner history
# OR
git config --global pull.ff only         # Safest (forces explicit decision)

# Auto-stash (use cautiously)
git config --global rebase.autoStash true  # Only for small changes

# Conflict resolution helpers
git config --global rerere.enabled true              # Reuse resolutions
git config --global merge.conflictStyle diff3        # 3-way comparison

# Better diff algorithm
git config --global diff.algorithm histogram

# Colorful UI
git config --global color.ui auto
```

### Team Configuration

**Shared `.gitconfig` patterns** (document in README):

```bash
# Pull strategy (team standard)
pull.rebase = true

# Auto-stash (team preference)
rebase.autoStash = true

# Rerere (recommended for all)
rerere.enabled = true
```

---

## References

**Internal Documentation**:

- `.claude/commands/git.md` - Git workflow command definition
- `.claude/agents/source-control.md` - Git operations implementation
- `.claude/docs/01-guides/repository-standards.md` - Repository conventions

**External Resources**:

- [GitHub Docs: About Git Rebase](https://docs.github.com/en/get-started/using-git/about-git-rebase)
- [Atlassian: Merging vs Rebasing](https://www.atlassian.com/git/tutorials/merging-vs-rebasing)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Book: Rebasing](https://git-scm.com/book/en/v2/Git-Branching-Rebasing)

**Last Updated**: 2025-01-12
**Version**: 1.0
**Maintainers**: Development Team
