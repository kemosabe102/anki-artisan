---
name: branch-strategy
description: >
  Branch lifecycle management: creation, switching, deletion, naming conventions,
  and remote synchronization. Use for branch operations, fetch/pull status,
  tracking info, and safe branch switching with stash management.
---

# Branch Strategy Skill

**Domain**: Development  
**Responsibility**: Branch lifecycle, naming conventions, remote synchronization  
**Triggers**:
  - list_branches metadata
  - create_branch metadata
  - switch_branch metadata
  - remote sync metadata
  - branch naming validation

---

## Overview

Owns the methodology and operations for:
- Creating branches with proper naming conventions
- Switching branches safely (with stash if needed)
- Deleting branches with safety checks
- Listing branches with tracking info
- Remote synchronization (fetch, ahead/behind tracking)
- Stash management for safe branch switching

**Does NOT own**:
- Commits (see source-control skill)
- Tagging/releases (see tag-release skill)
- Pull requests (see github skill)
- Code modifications (see domain specialists)

---

## Core Operations

### list_branches

```
Input: { include_remote: boolean (default: true) }
Output: {
  local: ["main", "feature/user-auth", ...],
  remote: ["origin/main", "origin/develop", ...],
  tracking: {
    "feature/user-auth": "origin/feature/user-auth",
    ...
  },
  current: "feature/user-auth"
}
Logic: git branch -a with tracking info extraction
```

**Delegation**: `Task(source-control)` with operation: list_branches

### create_branch

```
Input: {
  name: string,           # Required: branch name (validated against conventions)
  base: string,           # Optional: base branch (default: current branch)
  track_remote: boolean   # Optional: set up remote tracking (default: false)
}
Output: {
  branch: "feature/user-auth",
  base: "main",
  tracking_suggested: true,
  validation: { passed: true, convention: "feature/*" }
}
Logic: Validate name -> git checkout -b <name> [base]
```

**Naming Validation**: See [reference/naming-conventions.md](reference/naming-conventions.md)

**Delegation**: `Task(source-control)` with operation: create_branch

### switch_branch

```
Input: {
  branch: string,         # Required: target branch
  stash_if_dirty: boolean # Optional: auto-stash uncommitted changes (default: true)
}
Output: {
  switched_to: "feature/user-auth",
  stashed: true,
  stash_ref: "stash@{0}",
  tracking: "origin/feature/user-auth"
}
Logic: Check dirty state -> stash if needed -> git checkout <branch>
```

**Safety**: Will NOT lose uncommitted work. Stash is automatic unless disabled.

**Delegation**: `Task(source-control)` with operation: switch_branch

### delete_branch

```
Input: {
  branch: string,         # Required: branch to delete
  force: boolean,         # Optional: force delete unmerged branch (default: false)
  delete_remote: boolean  # Optional: also delete from remote (default: false)
}
Output: {
  deleted: "feature/old-branch",
  was_merged: true,
  remote_deleted: false,
  warnings: []
}
Logic: Check not current -> check merged status -> git branch -d/-D
```

**Safety Checks**:
- Cannot delete current branch (switch first)
- Warns if branch has unmerged commits (requires `force: true`)
- Remote deletion requires explicit `delete_remote: true`

**Delegation**: `Task(source-control)` with operation: delete_branch

### fetch_remote

```
Input: {
  remote: string,         # Optional: remote name (default: "origin")
  prune: boolean          # Optional: remove stale tracking refs (default: true)
}
Output: {
  remote: "origin",
  fetched_branches: ["feature/new-api", "fix/login-bug"],
  pruned_refs: ["origin/feature/old-removed"],
  new_tags: []
}
Logic: git fetch [remote] [--prune]
```

**Report Changes**: Always report what changed (new branches, pruned refs).

**Delegation**: `Task(source-control)` with operation: fetch_remote

### get_remote_status

```
Input: {
  branch: string          # Optional: branch to check (default: current branch)
}
Output: {
  branch: "feature/user-auth",
  tracking: "origin/feature/user-auth",
  ahead: 3,
  behind: 1,
  needs_sync: true,
  sync_suggestion: "pull --rebase recommended"
}
Logic: git rev-list --left-right --count HEAD...@{u}
```

**Sync Suggestions**:
- `ahead > 0, behind = 0`: "push recommended"
- `ahead = 0, behind > 0`: "pull recommended"  
- `ahead > 0, behind > 0`: "pull --rebase recommended"

**Delegation**: `Task(source-control)` with operation: get_remote_status

---

## Key Methodologies

### Naming Conventions
[See reference/naming-conventions.md](reference/naming-conventions.md)

| Prefix | Purpose | Example |
|--------|---------|---------|
| `feature/*` | New functionality | `feature/user-authentication` |
| `fix/*` | Bug fixes | `fix/login-timeout` |
| `refactor/*` | Code restructuring | `refactor/api-client` |
| `docs/*` | Documentation only | `docs/api-reference` |
| `test/*` | Test additions/fixes | `test/auth-integration` |
| `chore/*` | Maintenance tasks | `chore/update-deps` |

**Format**: `<prefix>/<kebab-case-description>`

### Branch Workflows
[See reference/branch-workflows.md](reference/branch-workflows.md)

- Feature branch lifecycle (create -> develop -> PR -> merge -> delete)
- Hotfix patterns (branch from main, merge to main + develop)
- Release branch handling

### Remote Synchronization
[See reference/remote-sync.md](reference/remote-sync.md)

- Fetch before status checks
- Pull vs pull --rebase decisions
- Push patterns and force-push warnings

---

## Error Handling

[See reference/error-handling.md](reference/error-handling.md)

| Error | Category | Recovery |
|-------|----------|----------|
| "Branch already exists" | PERMANENT | Suggest different name or checkout existing |
| "Cannot delete current branch" | PERMANENT | Switch to different branch first |
| "Branch not fully merged" | SOFT | Warn user, require `force: true` |
| "Tracking branch mismatch" | SOFT | Suggest `git branch --set-upstream-to` |
| "Ahead/behind conflicts" | SOFT | Recommend pull --rebase |
| "Remote not found" | PERMANENT | Verify remote exists with `git remote -v` |
| "Uncommitted changes" | SOFT | Auto-stash or prompt user |

---

## Delegation Patterns

[See delegation/patterns.md](delegation/patterns.md)

All operations delegate to `source-control` agent. This skill provides:
- Operation definitions and validation rules
- Naming convention enforcement
- Error recovery guidance
- Output interpretation

**Example Delegation**:
```
Task(source-control) with:
  operation: create_branch
  params: { name: "feature/user-auth", base: "main" }
```

---

## Safety Constraints

### SAFE Operations
- `git branch -a` (list branches)
- `git fetch` (download refs)
- `git checkout <branch>` (switch branches)
- `git stash` / `git stash pop` (temporary storage)
- `git branch -d` (safe delete - checks merged status)

### REQUIRES CONFIRMATION
- `git branch -D` (force delete - may lose work)
- `git push origin --delete` (remote deletion)
- `git push --force` (rewrite remote history)

### FORBIDDEN (This Skill)
- `git reset --hard` (use source-control skill)
- `git clean -fd` (destructive)
- Direct commits (use source-control skill)

---

## Examples

[See examples/usage-examples.md](examples/usage-examples.md)

### Quick Start
```
User: "create a branch for the login feature"
Skill: Validate name -> create_branch("feature/login", base="main")

User: "switch to main"
Skill: Check dirty -> stash if needed -> switch_branch("main")

User: "am I up to date with remote?"
Skill: fetch_remote() -> get_remote_status()
```

---

## Thinking Frameworks

When facing complex branch strategy challenges:

**Full Catalog**: [Thinking Frameworks README](../../docs/00-core/frameworks/README.md)

**Most Relevant for Branch Strategy**:

| Framework | When to Use |
|-----------|-------------|
| [ReACT](../../docs/00-core/frameworks/analysis.md) | Diagnosing sync conflicts, tracing branch history |
| [Pre-Mortem](../../docs/00-core/frameworks/strategy.md) | Assessing risks before force operations |

> **Selection Tip**: sync issues -> ReACT, destructive operations -> Pre-Mortem
