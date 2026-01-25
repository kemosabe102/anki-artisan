---
name: github
description: >
  GitHub platform operations: PR management, issue tracking, CI monitoring via Actions,
  release publishing, and workflow dispatch. Uses gh CLI and mcp__github__* tools.
  NOT for commits/staging (source-control), branches (branch-strategy), or git tags (tag-release).
---

# GitHub Skill

**Domain**: Development  
**Responsibility**: GitHub platform operations (PRs, issues, Actions, releases)  
**Triggers**:
  - PR create/list/merge/review metadata
  - issue create/list/comment/close metadata
  - CI status monitoring metadata
  - GitHub release creation metadata
  - workflow dispatch metadata

---

## Overview

Owns the methodology and operations for:
- Pull Request lifecycle (create, list, review, merge)
- Issue management (create, list, comment, close)
- GitHub Actions CI monitoring and failure analysis
- GitHub Release publishing (not git tags)
- Workflow dispatch and trigger management
- GitHub API error handling and rate limiting

**Does NOT own**:
- Commits/staging (use source-control skill)
- Branch creation/switching/deletion (use branch-strategy skill)
- Git tags (use tag-release skill)
- Local git operations (use appropriate skill)
- Code modifications (use domain specialists)

---

## Tool Selection

| Tool | Use For |
|------|---------|
| gh CLI | Workflow runs, PR/issue operations, releases |
| mcp__github__create_pull_request | Create PRs with full body |
| mcp__github__list_pull_requests | List PRs with filters |
| mcp__github__get_pull_request | Get PR details |
| mcp__github__merge_pull_request | Merge PRs |
| mcp__github__create_issue | Create issues |
| mcp__github__list_issues | List issues with filters |
| mcp__github__get_issue | Get issue details |
| mcp__github__update_issue | Update issue (close, labels, etc.) |
| mcp__github__create_or_update_file | NOT for releases (use gh release) |

**Workflow Runs**: GitHub MCP does not provide workflow run tools - use gh run CLI.

---

## Core Operations

### monitor_ci

Monitors GitHub Actions workflow status with UV-aware failure analysis.

```
Input: {
  commit_sha: string,         # Optional: specific commit to check
  run_id: string,             # Optional: specific run ID
  branch: string,             # Optional: branch (default: current)
  wait_for_completion: bool   # Optional: poll until complete (default: false)
}
Output: {
  workflow_status: "queued" | "in_progress" | "completed",
  conclusion: "success" | "failure" | "cancelled" | "skipped" | null,
  workflow_runs: [{
    id: string,
    name: string,
    status: string,
    conclusion: string,
    started_at: string,
    completed_at: string,
    jobs: [{name, status, conclusion}]
  }],
  summary: string,
  recommended_actions: string[],
  uv_failure_detected: bool,
  uv_failure_type: string | null
}
Logic: gh run list/view -> parse failures -> detect UV patterns
```

**Workflow**:
1. Determine target (commit SHA, run ID, or branch)
2. Query GitHub Actions: `gh run list --limit 10 [--branch]`
3. View specific run: `gh run view <run-id>`
4. Get failed logs: `gh run view <run-id> --log-failed`
5. Parse failure details (job names, step names, error messages)
6. Identify UV failure patterns (see reference/ci-monitoring.md)
7. Generate recommendations
8. Return structured status report

See reference/ci-monitoring.md for UV failure patterns.

---

### create_pr

Creates a GitHub Pull Request.

```
Input: {
  title: string,              # Required: PR title
  body: string,               # Required: PR body (markdown)
  base: string,               # Optional: target branch (default: main)
  head: string,               # Optional: source branch (default: current)
  draft: bool                 # Optional: create as draft (default: false)
}
Output: {
  status: "SUCCESS" | "FAILURE",
  pr_number: number,
  pr_url: string,
  title: string,
  head: string,
  base: string
}
Logic: Validate branches exist -> create PR via MCP or gh CLI
```

**Workflow**:
1. Verify head branch has commits ahead of base
2. Verify head branch is pushed to remote
3. Create PR via `mcp__github__create_pull_request` or `gh pr create`
4. Return PR details

See reference/pr-management.md for PR templates.

---

### list_prs

Lists Pull Requests with optional filters.

```
Input: {
  state: string,              # Optional: "open" | "closed" | "all" (default: "open")
  author: string,             # Optional: filter by author
  label: string,              # Optional: filter by label
  limit: number               # Optional: max results (default: 30)
}
Output: {
  prs: [{
    number: number,
    title: string,
    state: string,
    author: string,
    created_at: string,
    updated_at: string,
    url: string,
    labels: string[],
    draft: bool
  }],
  total_count: number
}
Logic: mcp__github__list_pull_requests or gh pr list
```

---

### merge_pr

Merges a Pull Request.

```
Input: {
  pr_number: number,          # Required: PR number
  merge_method: string,       # Optional: "merge" | "squash" | "rebase" (default: "squash")
  commit_title: string,       # Optional: custom merge commit title
  delete_branch: bool         # Optional: delete head branch after merge (default: true)
}
Output: {
  status: "SUCCESS" | "FAILURE",
  merged: bool,
  sha: string,
  message: string,
  branch_deleted: bool
}
Logic: Check mergeable -> merge via MCP -> optionally delete branch
```

**Pre-Merge Checks**:
- PR is open
- PR is mergeable (no conflicts)
- Required status checks pass
- Required reviews approved

---

### create_issue

Creates a GitHub Issue.

```
Input: {
  title: string,              # Required: issue title
  body: string,               # Required: issue body (markdown)
  labels: string[],           # Optional: labels to apply
  assignees: string[]         # Optional: users to assign
}
Output: {
  status: "SUCCESS" | "FAILURE",
  issue_number: number,
  issue_url: string,
  title: string
}
Logic: mcp__github__create_issue
```

See reference/issue-management.md for issue templates.

---

### list_issues

Lists Issues with optional filters.

```
Input: {
  state: string,              # Optional: "open" | "closed" | "all" (default: "open")
  labels: string[],           # Optional: filter by labels
  assignee: string,           # Optional: filter by assignee
  limit: number               # Optional: max results (default: 30)
}
Output: {
  issues: [{
    number: number,
    title: string,
    state: string,
    author: string,
    created_at: string,
    labels: string[],
    assignees: string[],
    url: string
  }],
  total_count: number
}
Logic: mcp__github__list_issues or gh issue list
```

---

### create_release

Creates a GitHub Release (platform release, NOT git tag).

```
Input: {
  tag: string,                # Required: existing git tag (e.g., "v1.3.0")
  title: string,              # Optional: release title (default: tag name)
  body: string,               # Optional: release notes (markdown)
  draft: bool,                # Optional: create as draft (default: false)
  prerelease: bool,           # Optional: mark as prerelease (default: false)
  generate_notes: bool        # Optional: auto-generate notes (default: false)
}
Output: {
  status: "SUCCESS" | "FAILURE",
  release_id: number,
  release_url: string,
  tag: string,
  title: string,
  draft: bool,
  prerelease: bool
}
Logic: Verify tag exists -> gh release create
```

**Workflow**:
1. Verify git tag exists: `git tag -l {tag}`
2. Create release: `gh release create {tag} --title "{title}" --notes "{body}"`
3. Optionally use `--generate-notes` for auto-generated notes
4. Return release details

See reference/release-management.md for release workflows.

---

### trigger_workflow

Manually triggers a GitHub Actions workflow.

```
Input: {
  workflow: string,           # Required: workflow file name or ID
  ref: string,                # Optional: branch/tag to run on (default: main)
  inputs: object              # Optional: workflow inputs (key-value pairs)
}
Output: {
  status: "SUCCESS" | "FAILURE",
  run_id: string,
  workflow: string,
  ref: string,
  run_url: string
}
Logic: gh workflow run -> return run ID
```

**Workflow**:
1. Verify workflow exists: `gh workflow list`
2. Trigger workflow: `gh workflow run {workflow} --ref {ref} -f input1=value1`
3. Get run ID from output or query: `gh run list --workflow={workflow} --limit 1`
4. Return run details

See reference/actions-workflows.md for workflow patterns.

---

## Error Handling

See reference/error-handling.md

### HTTP Error Classification

| Code | Error | Category | Recovery |
|------|-------|----------|----------|
| 401 | Unauthorized | PERMANENT | Re-authenticate: `gh auth login` |
| 403 | Forbidden | PERMANENT | Check token permissions |
| 404 | Not Found | PERMANENT | Verify owner/repo via `git remote -v` |
| 422 | Validation Failed | PERMANENT | Check parameters, fix request |
| 429 | Rate Limited | TRANSIENT | Honor Retry-After header |
| 500 | Server Error | TRANSIENT | Retry with backoff |
| 502 | Bad Gateway | TRANSIENT | Retry with backoff |
| 503 | Service Unavailable | TRANSIENT | Retry with backoff |
| 504 | Gateway Timeout | TRANSIENT | Retry with backoff |

### Retry Configuration

```
TRANSIENT errors (429, 5xx):
  max_retries: 3
  backoff: exponential with jitter (5s, 10s, 20s)
  circuit_breaker: 5 consecutive failures -> 60s wait

PERMANENT errors (401, 403, 404, 422):
  max_retries: 0
  action: Return FAILURE with recovery suggestions
```

### Circuit Breaker

```
CLOSED (normal) --[5 failures]--> OPEN (blocked)
OPEN --[60s wait]--> HALF-OPEN (testing)
HALF-OPEN --[3 successes]--> CLOSED
HALF-OPEN --[1 failure]--> OPEN
```

---

## Delegation Patterns

See delegation/patterns.md

### Standard Delegation

```
Task(github) with:
  operation: "monitor_ci" | "create_pr" | "merge_pr" | ...
  params: { ... }
```

### Repository Identification

**MANDATORY**: Always identify repository before GitHub operations:
```bash
AGENT_NAME=github git remote -v
# Extract owner/repo from origin URL
```

---

## Bash Command Format

All gh commands use AGENT_NAME prefix for logging:

```bash
AGENT_NAME=github gh run list --limit 10
AGENT_NAME=github gh run view 12345 --log-failed
AGENT_NAME=github gh pr create --title "feat: add feature" --body "..."
AGENT_NAME=github gh pr merge 42 --squash --delete-branch
AGENT_NAME=github gh issue create --title "Bug: ..." --body "..."
AGENT_NAME=github gh release create v1.3.0 --title "v1.3.0" --notes "..."
AGENT_NAME=github gh workflow run ci.yml --ref main
```

---

## Safety Constraints

### SAFE Operations
- `gh run list` / `gh run view` (read-only)
- `gh pr list` / `gh pr view` (read-only)
- `gh issue list` / `gh issue view` (read-only)
- `gh release list` / `gh release view` (read-only)
- `gh workflow list` (read-only)

### REQUIRES CONFIRMATION
- `gh pr merge` (modifies repository)
- `gh pr close` (modifies PR state)
- `gh issue close` (modifies issue state)
- `gh release delete` (removes release)
- `gh workflow run` (triggers execution)

### FORBIDDEN (This Skill)
- Direct git commits (use source-control skill)
- Branch operations (use branch-strategy skill)
- Git tag creation (use tag-release skill)
- Force push operations

---

## Examples

See examples/usage-examples.md

### Quick Start
```
User: "Check CI status"
Skill: monitor_ci() -> status report with recommendations

User: "Create a PR for this branch"
Skill: create_pr(title, body) -> PR URL

User: "Merge PR #42"
Skill: merge_pr(42, squash) -> merge confirmation

User: "Create a GitHub release for v1.3.0"
Skill: create_release("v1.3.0", title, notes) -> release URL
```

---

## Thinking Frameworks

When facing complex GitHub challenges:

**Full Catalog**: See .claude/docs/00-core/frameworks/README.md

**Most Relevant for GitHub Operations**:

| Framework | When to Use |
|-----------|-------------|
| ReACT | Diagnosing CI failures, tracing workflow issues |
| Pre-Mortem | Assessing risks before merging to main |

> **Selection Tip**: CI failures -> ReACT, risky merges -> Pre-Mortem

---

## References

| File | Purpose |
|------|---------|
| reference/ci-monitoring.md | UV failure patterns, Actions monitoring |
| reference/pr-management.md | PR templates, review workflows |
| reference/issue-management.md | Issue templates, labeling |
| reference/release-management.md | GitHub release workflows |
| reference/actions-workflows.md | Workflow dispatch, triggers |
| reference/error-handling.md | GitHub-specific error patterns |
| delegation/patterns.md | Task() delegation templates |
| examples/usage-examples.md | End-to-end workflow examples |
