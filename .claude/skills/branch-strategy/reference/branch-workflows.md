# Branch Workflows

Standard workflows for branch lifecycle management.

---

## Feature Branch Workflow

The primary workflow for new development.

### Lifecycle

```
1. CREATE    git checkout -b feature/user-auth main
2. DEVELOP   [make commits, push regularly]
3. SYNC      git fetch origin && git rebase origin/main
4. PR        gh pr create --base main
5. REVIEW    [address feedback, push updates]
6. MERGE     [PR merged via GitHub]
7. CLEANUP   git branch -d feature/user-auth
```

### Detailed Steps

#### 1. Create Feature Branch

```bash
# Ensure main is up-to-date
git checkout main
git pull origin main

# Create and switch to feature branch
git checkout -b feature/user-auth

# Push to remote (creates tracking)
git push -u origin feature/user-auth
```

#### 2. Develop on Branch

```bash
# Regular development cycle
git add <files>
git commit -m "feat(auth): add login endpoint"

# Push frequently (backup + collaboration)
git push
```

#### 3. Keep Branch Updated

```bash
# Fetch latest from remote
git fetch origin

# Rebase onto latest main (preferred over merge)
git rebase origin/main

# Force push if rebased (only your branch!)
git push --force-with-lease
```

**Why rebase?** Keeps history linear, easier to review.

#### 4. Create Pull Request

```bash
# Via GitHub CLI
gh pr create --base main --title "feat(auth): user authentication" --body "..."
```

#### 5-6. Review and Merge

Handled via GitHub PR interface. Squash merge recommended for clean history.

#### 7. Cleanup

```bash
# Switch away from feature branch
git checkout main
git pull origin main

# Delete local branch
git branch -d feature/user-auth

# Remote branch deleted automatically by GitHub (if configured)
```

---

## Hotfix Workflow

For urgent production fixes that cannot wait for normal release cycle.

### Lifecycle

```
1. CREATE    git checkout -b hotfix/critical-bug main
2. FIX       [minimal fix commits]
3. TEST      [verify fix works]
4. PR        gh pr create --base main
5. MERGE     [emergency merge to main]
6. BACKPORT  [merge fix to develop if exists]
7. TAG       git tag v1.2.1 (patch version bump)
```

### Key Differences from Feature

| Aspect | Feature Branch | Hotfix Branch |
|--------|----------------|---------------|
| Base | `main` or `develop` | Always `main` |
| Merge target | `develop` then `main` | `main` directly |
| Backport | Not needed | Must merge to `develop` |
| Tagging | No | Yes (patch version) |
| Review | Standard | Expedited |

---

## Release Branch Workflow

For preparing releases when using release branches.

### Lifecycle

```
1. CREATE    git checkout -b release/v1.3.0 develop
2. STABILIZE [bug fixes only, no features]
3. VERSION   [update version numbers, changelog]
4. TEST      [final QA]
5. MERGE     [merge to main AND develop]
6. TAG       git tag v1.3.0
7. CLEANUP   git branch -d release/v1.3.0
```

### Rules

- **No new features**: Only bug fixes allowed
- **Version bump**: Update version at creation
- **Dual merge**: Must merge to both main AND develop
- **Tag after merge**: Tag on main after merge

---

## Stash Workflow

For temporarily storing uncommitted changes during branch switches.

### When to Stash

1. **Switching branches** with uncommitted work
2. **Pulling changes** when local changes conflict
3. **Rebasing** when working directory is dirty

### Stash Commands

```bash
# Save current changes to stash
git stash push -m "WIP: user auth changes"

# List stashes
git stash list
# stash@{0}: On feature/user-auth: WIP: user auth changes

# Apply most recent stash (keeps stash)
git stash apply

# Apply and remove stash
git stash pop

# Apply specific stash
git stash apply stash@{1}

# Drop a stash
git stash drop stash@{0}

# Clear all stashes (destructive!)
git stash clear
```

### Stash Best Practices

1. **Always use message**: `git stash push -m "description"`
2. **Don't accumulate**: Apply or drop stashes promptly
3. **Check before clear**: `git stash list` before `git stash clear`

---

## Decision Tree: Which Workflow?

```
Is this an urgent production fix?
  YES -> Hotfix Workflow
  NO  -> Continue

Is this preparing a release?
  YES -> Release Branch Workflow
  NO  -> Continue

Is this new development?
  YES -> Feature Branch Workflow
  NO  -> Feature Branch Workflow (default)
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Create feature branch | `git checkout -b feature/name main` |
| Push with tracking | `git push -u origin feature/name` |
| Sync with main | `git fetch && git rebase origin/main` |
| Safe switch | `git stash && git checkout other && git stash pop` |
| Delete local | `git branch -d feature/name` |
| Delete remote | `git push origin --delete feature/name` |
