# Branch Error Handling

Error patterns and recovery strategies for branch operations.

---

## Error Classification

| Category | Behavior | Example |
|----------|----------|---------|
| **PERMANENT** | Cannot retry, requires user action | Branch already exists |
| **SOFT** | Recoverable with additional params | Unmerged branch deletion |
| **TRANSIENT** | Retry may succeed | Network timeout |

---

## Common Errors

### Branch Already Exists

**Error Message**:
```
fatal: A branch named 'feature/user-auth' already exists.
```

**Category**: PERMANENT

**Cause**: Attempting to create a branch with a name that already exists locally.

**Recovery Options**:
1. Switch to existing branch: `git checkout feature/user-auth`
2. Use different name: `git checkout -b feature/user-auth-v2`
3. Delete existing first: `git branch -d feature/user-auth` (if safe)

**Structured Response**:
```json
{
  "status": "FAILURE",
  "error": "branch_already_exists",
  "branch": "feature/user-auth",
  "recovery_options": [
    "checkout_existing",
    "use_different_name",
    "delete_and_recreate"
  ]
}
```

---

### Cannot Delete Current Branch

**Error Message**:
```
error: Cannot delete branch 'feature/user-auth' checked out at '/path/to/repo'
```

**Category**: PERMANENT

**Cause**: Attempting to delete the branch you're currently on.

**Recovery**:
1. Switch to different branch first: `git checkout main`
2. Then delete: `git branch -d feature/user-auth`

**Structured Response**:
```json
{
  "status": "FAILURE",
  "error": "cannot_delete_current_branch",
  "branch": "feature/user-auth",
  "recovery": "switch_branch_first",
  "suggested_target": "main"
}
```

---

### Branch Not Fully Merged

**Error Message**:
```
error: The branch 'feature/user-auth' is not fully merged.
If you are sure you want to delete it, run 'git branch -D feature/user-auth'.
```

**Category**: SOFT

**Cause**: Branch has commits not present in its upstream or HEAD.

**Recovery Options**:
1. Force delete if sure: `git branch -D feature/user-auth`
2. Merge first: Merge to target branch before deleting
3. Check if already merged to different branch

**Structured Response**:
```json
{
  "status": "FAILURE",
  "error": "branch_not_merged",
  "branch": "feature/user-auth",
  "unmerged_commits": 3,
  "recovery_options": [
    {"action": "force_delete", "command": "git branch -D feature/user-auth"},
    {"action": "merge_first", "target": "main"}
  ],
  "requires_confirmation": true
}
```

---

### Tracking Branch Mismatch

**Error Message**:
```
Your branch and 'origin/feature/user-auth' have diverged,
and have 3 and 1 different commits each, respectively.
```

**Category**: SOFT

**Cause**: Local and remote branches have diverged (both have unique commits).

**Recovery Options**:
1. Rebase: `git pull --rebase` (preferred)
2. Merge: `git pull` (creates merge commit)
3. Force push: `git push --force-with-lease` (if remote should match local)

**Structured Response**:
```json
{
  "status": "WARNING",
  "error": "branches_diverged",
  "branch": "feature/user-auth",
  "tracking": "origin/feature/user-auth",
  "ahead": 3,
  "behind": 1,
  "recovery_options": [
    {"action": "pull_rebase", "recommended": true},
    {"action": "pull_merge"},
    {"action": "force_push", "warning": "May overwrite remote commits"}
  ]
}
```

---

### Remote Not Found

**Error Message**:
```
fatal: 'upstream' does not appear to be a git repository
fatal: Could not read from remote repository.
```

**Category**: PERMANENT

**Cause**: Remote name doesn't exist or is misconfigured.

**Recovery**:
1. List remotes: `git remote -v`
2. Add remote: `git remote add upstream <url>`
3. Fix URL: `git remote set-url origin <correct-url>`

**Structured Response**:
```json
{
  "status": "FAILURE",
  "error": "remote_not_found",
  "remote": "upstream",
  "available_remotes": ["origin"],
  "recovery": "verify_remote_config"
}
```

---

### Uncommitted Changes Blocking Switch

**Error Message**:
```
error: Your local changes to the following files would be overwritten by checkout:
        path/to/file.py
Please commit your changes or stash them before you switch branches.
```

**Category**: SOFT

**Cause**: Uncommitted changes conflict with target branch.

**Recovery Options**:
1. Stash changes: `git stash push -m "WIP"` then switch
2. Commit first: `git add . && git commit -m "WIP"`
3. Discard changes: `git checkout -- .` (DESTRUCTIVE)

**Structured Response**:
```json
{
  "status": "FAILURE",
  "error": "uncommitted_changes_blocking",
  "conflicting_files": ["path/to/file.py"],
  "recovery_options": [
    {"action": "stash", "command": "git stash push -m 'WIP'", "recommended": true},
    {"action": "commit", "command": "git commit -am 'WIP'"},
    {"action": "discard", "command": "git checkout -- .", "warning": "DESTRUCTIVE"}
  ]
}
```

---

### No Tracking Information

**Error Message**:
```
There is no tracking information for the current branch.
Please specify which branch you want to merge with.
```

**Category**: SOFT

**Cause**: Local branch has no upstream tracking configured.

**Recovery**:
1. Set upstream: `git branch -u origin/feature/user-auth`
2. Push with tracking: `git push -u origin feature/user-auth`

**Structured Response**:
```json
{
  "status": "WARNING",
  "error": "no_tracking_info",
  "branch": "feature/user-auth",
  "recovery": "set_upstream",
  "suggested_command": "git branch -u origin/feature/user-auth"
}
```

---

### Branch Does Not Exist

**Error Message**:
```
error: pathspec 'feature/nonexistent' did not match any file(s) known to git
```

**Category**: PERMANENT

**Cause**: Trying to checkout a branch that doesn't exist locally or remotely.

**Recovery**:
1. List available branches: `git branch -a`
2. Fetch to get remote branches: `git fetch --all`
3. Create the branch: `git checkout -b feature/nonexistent`

**Structured Response**:
```json
{
  "status": "FAILURE",
  "error": "branch_not_found",
  "branch": "feature/nonexistent",
  "available_local": ["main", "develop"],
  "recovery_options": [
    {"action": "fetch_remote", "command": "git fetch --all"},
    {"action": "create_branch", "command": "git checkout -b feature/nonexistent"}
  ]
}
```

---

## Error Quick Reference

| Error | Category | Quick Fix |
|-------|----------|-----------|
| Branch already exists | PERMANENT | Checkout existing or use different name |
| Cannot delete current | PERMANENT | Switch to different branch first |
| Not fully merged | SOFT | Force delete with `-D` or merge first |
| Branches diverged | SOFT | `git pull --rebase` |
| Remote not found | PERMANENT | Check `git remote -v` |
| Uncommitted changes | SOFT | Stash or commit first |
| No tracking info | SOFT | Set upstream with `-u` |
| Branch not found | PERMANENT | Fetch or create branch |

---

## Error Detection Patterns

```python
ERROR_PATTERNS = {
    "branch_already_exists": r"A branch named '(.+)' already exists",
    "cannot_delete_current": r"Cannot delete branch '(.+)' checked out",
    "not_fully_merged": r"branch '(.+)' is not fully merged",
    "branches_diverged": r"have diverged.*?(\d+) and (\d+) different commits",
    "remote_not_found": r"'(.+)' does not appear to be a git repository",
    "uncommitted_changes": r"Your local changes.*would be overwritten",
    "no_tracking_info": r"no tracking information for the current branch",
    "branch_not_found": r"pathspec '(.+)' did not match any",
}

def classify_error(stderr: str) -> dict:
    """Classify git error from stderr output."""
    import re
    for error_type, pattern in ERROR_PATTERNS.items():
        match = re.search(pattern, stderr)
        if match:
            return {
                "error": error_type,
                "match": match.groups(),
                "category": get_category(error_type)
            }
    return {"error": "unknown", "raw": stderr}
```
