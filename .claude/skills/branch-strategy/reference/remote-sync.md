# Remote Synchronization

Patterns for keeping local and remote branches synchronized.

---

## Core Operations

### Fetch

Downloads refs and objects from remote without modifying local branches.

```bash
# Fetch from default remote (origin)
git fetch

# Fetch from specific remote
git fetch origin

# Fetch and prune stale tracking refs
git fetch --prune

# Fetch all remotes
git fetch --all
```

**When to fetch**:
- Before checking ahead/behind status
- Before creating branches from remote
- Before rebasing onto remote branch
- Regularly during collaboration

### Pull

Fetches AND merges remote changes into current branch.

```bash
# Pull with merge (default)
git pull

# Pull with rebase (preferred for feature branches)
git pull --rebase

# Pull specific branch
git pull origin main
```

**Pull vs Pull --rebase**:

| Scenario | Use | Reason |
|----------|-----|--------|
| Feature branch | `--rebase` | Keeps linear history |
| Shared branch | merge (default) | Preserves collaboration history |
| main/develop | Either | Team preference |

### Push

Uploads local commits to remote.

```bash
# Push current branch
git push

# Push and set upstream tracking
git push -u origin feature/user-auth

# Push specific branch
git push origin feature/user-auth

# Force push with safety (after rebase)
git push --force-with-lease
```

---

## Ahead/Behind Tracking

Understanding sync status between local and remote branches.

### Check Status

```bash
# Quick status (shows ahead/behind)
git status

# Detailed count
git rev-list --left-right --count HEAD...@{upstream}
# Output: 3    1
# Meaning: 3 commits ahead, 1 commit behind

# Verbose branch info
git branch -vv
# * feature/auth abc1234 [origin/feature/auth: ahead 3, behind 1] commit message
```

### Status Interpretations

| Ahead | Behind | Status | Action |
|-------|--------|--------|--------|
| 0 | 0 | In sync | No action needed |
| N | 0 | Ahead | Push recommended |
| 0 | N | Behind | Pull recommended |
| N | M | Diverged | Pull --rebase then push |

### Sync Suggestions Logic

```python
def suggest_sync_action(ahead: int, behind: int) -> str:
    """Suggest sync action based on ahead/behind counts."""
    if ahead == 0 and behind == 0:
        return "in_sync"
    elif ahead > 0 and behind == 0:
        return "push_recommended"
    elif ahead == 0 and behind > 0:
        return "pull_recommended"
    else:  # Both ahead and behind
        return "pull_rebase_then_push"
```

---

## Tracking Branches

Setting up and managing tracking relationships.

### Set Upstream

```bash
# During push
git push -u origin feature/user-auth

# Manually set upstream
git branch --set-upstream-to=origin/feature/user-auth

# Shorthand
git branch -u origin/feature/user-auth
```

### View Tracking

```bash
# Show tracking for all branches
git branch -vv

# Show tracking for current branch
git rev-parse --abbrev-ref --symbolic-full-name @{upstream}
```

### Remove Tracking

```bash
# Unset upstream
git branch --unset-upstream
```

---

## Force Push Safety

When and how to safely force push.

### When Force Push is Needed

1. After rebasing a branch
2. After amending commits
3. After squashing commits

### Safe Force Push

```bash
# ALWAYS use --force-with-lease instead of --force
git push --force-with-lease

# This will FAIL if remote has commits you don't have
# Protects against overwriting others' work
```

### Force Push Rules

| Rule | Reason |
|------|--------|
| Only on your own branches | Never force push shared branches |
| Use `--force-with-lease` | Prevents overwriting others' commits |
| Never on main/master | Protected branches should block this |
| Communicate with team | Warn if others might be working on branch |

---

## Common Sync Scenarios

### Scenario 1: Start of Day Sync

```bash
# Fetch all updates
git fetch --all --prune

# Check status of current branch
git status

# If behind, pull with rebase
git pull --rebase
```

### Scenario 2: Before Creating PR

```bash
# Fetch latest main
git fetch origin main

# Rebase onto main
git rebase origin/main

# Force push (if needed)
git push --force-with-lease
```

### Scenario 3: Diverged Branch

```bash
# Fetch to see current state
git fetch

# Check ahead/behind
git rev-list --left-right --count HEAD...@{upstream}

# Pull with rebase to integrate remote changes
git pull --rebase

# Resolve any conflicts, then continue
git rebase --continue

# Push updated branch
git push --force-with-lease
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Fetch all | `git fetch --all --prune` |
| Check sync status | `git status` or `git branch -vv` |
| Pull with rebase | `git pull --rebase` |
| Push with tracking | `git push -u origin branch` |
| Safe force push | `git push --force-with-lease` |
| Set upstream | `git branch -u origin/branch` |
| Ahead/behind count | `git rev-list --left-right --count HEAD...@{u}` |
