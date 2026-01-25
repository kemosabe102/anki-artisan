# Error Handling for Source Control Operations

**Purpose**: Error classification framework and retry patterns for git staging/commit operations

**MANDATORY**: Classify errors BEFORE retrying any git command.

---

## Error Classification Overview

| Category | Retry? | Max Attempts | Action |
|----------|--------|--------------|--------|
| PERMANENT | No | 0 | Return FAILURE with recovery suggestions |
| TRANSIENT | Yes | 3 | Exponential backoff, then FAILURE |
| FATAL | No | 0 | Escalate to orchestrator immediately |

---

## Git Command Errors

### PERMANENT (No Retry)

| Error Pattern | Example Message | Recovery Suggestion |
|---------------|-----------------|---------------------|
| Merge conflict | "Merge conflict in CLAUDE.md" | Resolve conflict manually, run git status |
| Pre-commit hook failure | "Linting failed", "Tests failed" | Fix issues, re-stage files |
| Invalid commit format | "commit-msg hook rejected" | Fix commit message format |
| Detached HEAD + uncommitted | "HEAD detached at..." | Create branch or stash changes |
| Files not modified | "nothing to commit" | Verify file status with git status |
| Invalid file path | "pathspec did not match" | Check file exists and path is correct |


### TRANSIENT (Retry with Backoff)

| Error Pattern | Example Message | Backoff |
|---------------|-----------------|---------|
| Lock file busy | ".git/index.lock already exists" | 1s, 2s, 4s |
| Network timeout | "Connection timeout", "EOF" | 2s, 4s, 8s |
| File system delay | "Temporary file error" | 1s, 2s, 4s |
| SSH key timeout | "git-agent not responding" | 2s, 4s, 8s |

### FATAL (Escalate Immediately)

| Error Pattern | Example Message | Action |
|---------------|-----------------|--------|
| Repository corruption | "Cannot recover objects" | Escalate to orchestrator |
| Force push blocked | "protected branch" | Escalate - never override |
| Pack file corruption | "Invalid pack file" | Escalate to orchestrator |

---

## Retry Configuration

### Git Commands (add, commit, reset)

```
max_retries: 3
backoff: exponential (1s, 2s, 4s)
retry_on: lock file issues ONLY
no_retry: merge conflicts, hook failures, validation errors
```

### FileGrouper Operations (git status, git diff)


```
max_retries: 2
backoff: linear (2s, 4s)
retry_on: concurrent operation conflicts
no_retry: repository corruption, invalid repository
```

---

## Failure Output Schema

When returning FAILURE, always include error classification context:

```json
{
  "status": "FAILURE",
  "operation": "execute_commits",
  "failure_details": {
    "failure_type": "git_transient_error",
    "error_classification": "TRANSIENT",
    "retry_attempts": 3,
    "last_error": "fatal: Unable to create '.git/index.lock'",
    "recovery_suggestions": [
      "Lock file persisted after 3 retries",
      "Check for concurrent git operations: ps aux | grep git",
      "Manually remove stale lock: rm -f .git/index.lock (CAUTION)"
    ]
  }
}
```

---

## Partial Failure Handling

When `execute_commits` fails mid-batch:

```json
{
  "status": "PARTIAL",
  "failure_details": {
    "failure_type": "git_command_error",
    "failed_group": "group_3"
  },
  "partial_commits": [
    {"group_id": "group_1", "commit_sha": "abc123", "message": "..."},
    {"group_id": "group_2", "commit_sha": "def456", "message": "..."}
  ],
  "recovery_suggestions": [
    "Groups 1-2 committed successfully",
    "Resolve issue with group_3, then retry remaining groups"
  ]
}
```


---

## Anti-Patterns

- Retrying PERMANENT errors (merge conflicts, validation failures)
- Skipping error classification
- Retrying without backoff (causes thundering herd)
- Continuing after FATAL errors
- Not providing recovery suggestions

---

## Common Recovery Paths

### Lock File Stuck

```bash
# Check for git processes
ps aux | grep git

# If no processes, remove stale lock
rm -f .git/index.lock
```

### Detached HEAD

```bash
# Create branch from current state
git checkout -b recovery-branch

# Or return to existing branch (loses uncommitted)
git checkout main
```

### Mid-Rebase State

```bash
# Check state
ls .git/rebase-merge

# Abort rebase
git rebase --abort
```

### Pre-Commit Hook Failure

1. Review hook output for specific failures
2. Fix code issues (lint, tests, etc.)
3. Re-stage affected files
4. Retry commit
