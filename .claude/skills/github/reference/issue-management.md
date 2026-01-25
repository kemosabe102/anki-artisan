# Issue Management Reference

**Purpose**: GitHub Issue lifecycle - create, list, comment, close workflows

---

## Overview

Issue operations in this skill:
- create_issue: Create issues with templates
- list_issues: Query issues with filters
- Comment and close operations

---

## Issue Creation

### Via MCP Tool
```
mcp__github__create_issue
  owner: string      # Repository owner
  repo: string       # Repository name
  title: string      # Issue title
  body: string       # Issue body (markdown)
  labels: string[]   # Optional labels
  assignees: string[] # Optional assignees
```

### Via gh CLI
```bash
AGENT_NAME=github gh issue create \
  --title "Bug: Login fails on Safari" \
  --body "## Description\n\nLogin button unresponsive on Safari 17.\n\n## Steps to Reproduce\n\n1. Open Safari\n2. Click login\n\n## Expected\n\nLogin modal appears" \
  --label bug,high-priority \
  --assignee username
```

---

## Issue Body Templates

### Bug Report
```markdown
## Description

<\!-- Clear description of the bug -->

## Steps to Reproduce

1. Step 1
2. Step 2
3. Step 3

## Expected Behavior

<\!-- What should happen -->

## Actual Behavior

<\!-- What actually happens -->

## Environment

- OS: [e.g., macOS 14.2]
- Browser: [e.g., Safari 17]
- Version: [e.g., 1.2.3]
```

### Feature Request
```markdown
## Summary

<\!-- Brief description of the feature -->

## Problem Statement

<\!-- What problem does this solve? -->

## Proposed Solution

<\!-- How should it work? -->

## Alternatives Considered

<\!-- Other approaches considered -->

## Additional Context

<\!-- Any other relevant information -->
```

---

## Issue Listing

### Via MCP Tool
```
mcp__github__list_issues
  owner: string
  repo: string
  state: "open" | "closed" | "all"
```

### Via gh CLI
```bash
# List open issues
AGENT_NAME=github gh issue list

# List with filters
AGENT_NAME=github gh issue list --state open --label bug
AGENT_NAME=github gh issue list --assignee @me --limit 20

# Search issues
AGENT_NAME=github gh issue list --search "login in:title"

# Show issue details
AGENT_NAME=github gh issue view 123
```

---

## Issue Updates

### Close Issue
```bash
AGENT_NAME=github gh issue close 123

# Close with comment
AGENT_NAME=github gh issue close 123 --comment "Fixed in #456"

# Close as not planned
AGENT_NAME=github gh issue close 123 --reason "not planned"
```

### Reopen Issue
```bash
AGENT_NAME=github gh issue reopen 123
```

### Add Comment
```bash
AGENT_NAME=github gh issue comment 123 --body "Investigation update: ..."
```

### Edit Issue
```bash
# Add labels
AGENT_NAME=github gh issue edit 123 --add-label "priority:high"

# Assign user
AGENT_NAME=github gh issue edit 123 --add-assignee username

# Update title
AGENT_NAME=github gh issue edit 123 --title "Updated title"
```

---

## Label Conventions

| Label | Color | Use For |
|-------|-------|---------|
| bug | red | Bug reports |
| feature | green | Feature requests |
| enhancement | blue | Improvements |
| documentation | purple | Doc updates |
| help-wanted | yellow | Community help |
| good-first-issue | green | Beginner friendly |
| priority:high | red | Urgent issues |
| priority:low | gray | Lower priority |

---

## Linking Issues to PRs

### Auto-Close on Merge

Include in PR body:
```markdown
Closes #123
Fixes #456
Resolves #789
```

### Reference Without Closing
```markdown
Related to #123
See also #456
```

---

## Error Scenarios

| Error | Cause | Recovery |
|-------|-------|----------|
| "Issue not found" | Wrong number/repo | Verify issue exists |
| "Cannot edit" | No permissions | Check repo access |
| "Label not found" | Label does not exist | Create label first |
| "User not found" | Invalid assignee | Verify username |
