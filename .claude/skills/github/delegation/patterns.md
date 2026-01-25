# Delegation Patterns

**Purpose**: Task() templates for invoking GitHub skill operations

---

## Overview

This skill provides methodology for Task() delegation to implementation agents.
All operations execute via gh CLI or mcp__github__* tools.

---

## Standard Delegation Pattern

```
Task(github) with:
  operation: "<operation_name>"
  params: {
    # operation-specific parameters
  }
```

---

## Operation Templates

### monitor_ci

```
Task(github) with:
  operation: "monitor_ci"
  params: {
    branch: "main",           # Optional: branch to check
    commit_sha: null,         # Optional: specific commit
    run_id: null,             # Optional: specific run ID
    wait_for_completion: false
  }

Expected Output: {
  workflow_status: "completed",
  conclusion: "success" | "failure",
  uv_failure_detected: bool,
  recommended_actions: [...]
}
```

---

### create_pr

```
Task(github) with:
  operation: "create_pr"
  params: {
    title: "feat(auth): add OAuth support",
    body: "## Summary\n\n- Added OAuth2 flow\n\n## Test Plan\n\n- [ ] Manual testing",
    base: "main",
    head: "feature/oauth",
    draft: false
  }

Expected Output: {
  status: "SUCCESS",
  pr_number: 42,
  pr_url: "https://github.com/owner/repo/pull/42"
}
```

---

### list_prs

```
Task(github) with:
  operation: "list_prs"
  params: {
    state: "open",            # "open" | "closed" | "all"
    author: null,             # Optional: filter by author
    label: "bug",             # Optional: filter by label
    limit: 20
  }

Expected Output: {
  prs: [{number, title, state, author, url, ...}],
  total_count: number
}
```

---

### merge_pr

```
Task(github) with:
  operation: "merge_pr"
  params: {
    pr_number: 42,
    merge_method: "squash",   # "squash" | "merge" | "rebase"
    commit_title: null,       # Optional: custom title
    delete_branch: true
  }

Expected Output: {
  status: "SUCCESS",
  merged: true,
  sha: "abc1234...",
  branch_deleted: true
}
```

---

### create_issue

```
Task(github) with:
  operation: "create_issue"
  params: {
    title: "Bug: Login fails on Safari",
    body: "## Description\n\n...",
    labels: ["bug", "priority:high"],
    assignees: ["username"]
  }

Expected Output: {
  status: "SUCCESS",
  issue_number: 123,
  issue_url: "https://github.com/owner/repo/issues/123"
}
```

---

### list_issues

```
Task(github) with:
  operation: "list_issues"
  params: {
    state: "open",
    labels: ["bug"],
    assignee: "@me",
    limit: 30
  }

Expected Output: {
  issues: [{number, title, state, labels, ...}],
  total_count: number
}
```

---

### create_release

```
Task(github) with:
  operation: "create_release"
  params: {
    tag: "v1.3.0",            # Existing git tag
    title: "Version 1.3.0",
    body: "## Changes\n\n- Feature 1\n- Bug fix 2",
    draft: false,
    prerelease: false,
    generate_notes: false
  }

Expected Output: {
  status: "SUCCESS",
  release_id: 12345,
  release_url: "https://github.com/owner/repo/releases/tag/v1.3.0"
}
```

---

### trigger_workflow

```
Task(github) with:
  operation: "trigger_workflow"
  params: {
    workflow: "deploy.yml",
    ref: "main",
    inputs: {
      environment: "staging",
      debug: "true"
    }
  }

Expected Output: {
  status: "SUCCESS",
  run_id: "12345678901",
  run_url: "https://github.com/owner/repo/actions/runs/12345678901"
}
```

---

## Repository Identification

**MANDATORY**: Before any GitHub operation, identify the repository:

```
Pre-requisite step:
  AGENT_NAME=github git remote -v
  # Parse origin URL to extract owner/repo

Example:
  origin  git@github.com:owner/repo.git (fetch)
  -> owner = "owner"
  -> repo = "repo"
```

---

## Error Handling in Delegation

All delegations should handle failures:

```
Task(github) with:
  operation: "create_pr"
  params: { ... }

On SUCCESS:
  -> Return PR URL to user
  -> Proceed with next steps

On FAILURE:
  -> Check failure_details.error_classification
  -> If PERMANENT: Present recovery_suggestions to user
  -> If TRANSIENT: Retry was already attempted, present status
```

---

## Chaining Operations

### PR Creation Flow
```
1. Task(branch-strategy) with:
     operation: "get_remote_status"
   -> Verify branch is pushed

2. Task(github) with:
     operation: "create_pr"
   -> Create the PR

3. Task(github) with:
     operation: "monitor_ci"
     params: { branch: head_branch }
   -> Wait for CI results
```

### Release Flow
```
1. Task(tag-release) with:
     operation: "create_release_tag"
     params: { version: "v1.3.0" }
   -> Create git tag

2. Task(branch-strategy) with:
     operation: "push_tags"
   -> Push tag to remote

3. Task(github) with:
     operation: "create_release"
     params: { tag: "v1.3.0" }
   -> Create GitHub release
```

---

## Anti-Patterns

- Invoking GitHub operations without repository identification
- Skipping error handling for PERMANENT errors
- Creating releases without verifying tag exists
- Merging without checking CI status
- Chaining operations without checking previous success
