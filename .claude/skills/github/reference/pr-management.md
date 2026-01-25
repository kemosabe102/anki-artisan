# PR Management Reference

**Purpose**: Pull Request lifecycle management - create, review, merge workflows

---

## Overview

Pull Request operations in this skill:
- create_pr: Create new PRs with templates
- list_prs: Query PRs with filters
- merge_pr: Merge PRs with method selection

---

## PR Creation

### Via MCP Tool
```
mcp__github__create_pull_request
  owner: string     # Repository owner
  repo: string      # Repository name
  title: string     # PR title
  body: string      # PR description (markdown)
  head: string      # Source branch
  base: string      # Target branch (default: main)
```

### Via gh CLI
```bash
AGENT_NAME=github gh pr create \
  --title "feat(scope): description" \
  --body "## Summary\n\n- Change 1\n- Change 2\n\n## Test Plan\n\n- [ ] Test case 1" \
  --base main \
  --head feature/my-feature
```

---

## PR Body Template

```markdown
## Summary

<\!-- Brief description of what this PR does -->

## Changes

- Change 1
- Change 2

## Test Plan

- [ ] Test case 1
- [ ] Test case 2

## Related Issues

Closes #123
```

---

## PR Listing

### Via MCP Tool
```
mcp__github__list_pull_requests
  owner: string
  repo: string
  state: "open" | "closed" | "all"
```

### Via gh CLI
```bash
# List open PRs
AGENT_NAME=github gh pr list

# List with filters
AGENT_NAME=github gh pr list --state open --author @me
AGENT_NAME=github gh pr list --label bug --limit 10

# Show PR details
AGENT_NAME=github gh pr view 42
```

---

## PR Merging

### Merge Methods

| Method | Command | Use When |
|--------|---------|----------|
| squash | `--squash` | Feature branches, clean history |
| merge | `--merge` | Preserve all commits |
| rebase | `--rebase` | Linear history, few commits |

### Via MCP Tool
```
mcp__github__merge_pull_request
  owner: string
  repo: string
  pull_number: number
  merge_method: "squash" | "merge" | "rebase"
```

### Via gh CLI
```bash
# Squash merge (recommended)
AGENT_NAME=github gh pr merge 42 --squash --delete-branch

# Merge with custom commit title
AGENT_NAME=github gh pr merge 42 --squash \
  --subject "feat(auth): add OAuth support (#42)"

# Auto-merge when checks pass
AGENT_NAME=github gh pr merge 42 --auto --squash
```

---

## Pre-Merge Validation

**MANDATORY checks before merge_pr**:

1. **PR is open**: Cannot merge closed PRs
2. **No conflicts**: Mergeable state must be "clean"
3. **Status checks pass**: All required checks green
4. **Reviews approved**: If required, approvals present

```bash
# Check PR status
AGENT_NAME=github gh pr view 42 --json state,mergeable,statusCheckRollup,reviews
```

---

## PR Review

### Approve PR
```bash
AGENT_NAME=github gh pr review 42 --approve
```

### Request Changes
```bash
AGENT_NAME=github gh pr review 42 --request-changes --body "Please fix..."
```

### Comment
```bash
AGENT_NAME=github gh pr review 42 --comment --body "LGTM with minor suggestions"
```

---

## Common Patterns

### Create PR from Current Branch
```bash
# Ensure branch is pushed
AGENT_NAME=github git push -u origin HEAD

# Create PR
AGENT_NAME=github gh pr create --fill
```

### Draft PR
```bash
AGENT_NAME=github gh pr create --draft --title "WIP: feature" --body "..."

# Mark ready when complete
AGENT_NAME=github gh pr ready 42
```

---

## Error Scenarios

| Error | Cause | Recovery |
|-------|-------|----------|
| "No commits between..." | Head same as base | Push commits to head branch |
| "Cannot merge" | Conflicts exist | Resolve conflicts locally |
| "Required status check..." | CI failing | Fix CI failures |
| "Review required" | No approvals | Request review |
