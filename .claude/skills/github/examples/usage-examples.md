# Usage Examples

**Purpose**: End-to-end workflow examples for GitHub skill operations

---

## Example 1: Check CI Status

### User Request
```
"Check if CI is passing on main"
```

### Skill Execution

**Step 1**: Identify repository
```bash
AGENT_NAME=github git remote -v
# origin  git@github.com:owner/repo.git (fetch)
```

**Step 2**: Query CI status
```bash
AGENT_NAME=github gh run list --branch main --limit 5
```

**Output**:
```
STATUS  TITLE                WORKFLOW  BRANCH  EVENT  ID          ELAPSED  AGE
X       feat: add login      CI        main    push   1234567890  2m30s    5m
```

**Step 3**: Get failure details
```bash
AGENT_NAME=github gh run view 1234567890 --log-failed
```

**Step 4**: Detect UV pattern and return
```json
{
  "status": "SUCCESS",
  "workflow_status": "completed",
  "conclusion": "failure",
  "summary": "CI failed: UV sync failure detected",
  "uv_failure_detected": true,
  "uv_failure_type": "sync_failure",
  "recommended_actions": [
    "Check pyproject.toml version constraints",
    "Run uv lock locally to regenerate lockfile"
  ]
}
```

---

## Example 2: Create Pull Request

### User Request
```
"Create a PR for my feature branch"
```

### Skill Execution

**Step 1**: Get current branch and remote status
```bash
AGENT_NAME=github git branch --show-current
# feature/user-auth

AGENT_NAME=github git rev-list --left-right --count main...HEAD
# 0       3  (3 commits ahead)
```

**Step 2**: Verify branch is pushed
```bash
AGENT_NAME=github git push -u origin HEAD
```

**Step 3**: Create PR
```bash
AGENT_NAME=github gh pr create \
  --title "feat(auth): add user authentication" \
  --body "## Summary

- Added login endpoint
- Added JWT token validation
- Added password hashing

## Test Plan

- [ ] Manual login test
- [ ] Unit tests pass

---

Generated with [Claude Code](https://claude.com/claude-code)" \
  --base main
```

**Output**:
```json
{
  "status": "SUCCESS",
  "pr_number": 42,
  "pr_url": "https://github.com/owner/repo/pull/42",
  "title": "feat(auth): add user authentication",
  "head": "feature/user-auth",
  "base": "main"
}
```

---

## Example 3: Merge PR After Review

### User Request
```
"Merge PR #42"
```

### Skill Execution

**Step 1**: Check PR status
```bash
AGENT_NAME=github gh pr view 42 --json state,mergeable,statusCheckRollup
```

**Output**: `{"state":"OPEN","mergeable":"MERGEABLE","statusCheckRollup":[{"conclusion":"SUCCESS"}]}`

**Step 2**: Merge with squash
```bash
AGENT_NAME=github gh pr merge 42 --squash --delete-branch
```

**Output**:
```json
{
  "status": "SUCCESS",
  "merged": true,
  "sha": "abc1234def5678...",
  "message": "Squash merged PR #42",
  "branch_deleted": true
}
```

---

## Example 4: Create Bug Issue

### User Request
```
"Create an issue for the Safari login bug"
```

### Skill Execution

```bash
AGENT_NAME=github gh issue create \
  --title "Bug: Login button unresponsive on Safari 17" \
  --body "## Description

The login button does not respond to clicks on Safari 17.

## Steps to Reproduce

1. Open Safari 17 on macOS
2. Navigate to login page
3. Click the Login button

## Expected Behavior

Login modal should appear.

## Actual Behavior

Nothing happens. No console errors.

## Environment

- Browser: Safari 17.2
- OS: macOS 14.2
- Version: 1.2.3" \
  --label bug,high-priority
```

**Output**:
```json
{
  "status": "SUCCESS",
  "issue_number": 123,
  "issue_url": "https://github.com/owner/repo/issues/123",
  "title": "Bug: Login button unresponsive on Safari 17"
}
```

---

## Example 5: Create GitHub Release

### User Request
```
"Create a GitHub release for v1.3.0"
```

### Skill Execution

**Step 1**: Verify tag exists
```bash
AGENT_NAME=github git tag -l v1.3.0
# v1.3.0
```

**Step 2**: Create release with auto-generated notes
```bash
AGENT_NAME=github gh release create v1.3.0 \
  --title "v1.3.0" \
  --generate-notes
```

**Output**:
```json
{
  "status": "SUCCESS",
  "release_id": 12345678,
  "release_url": "https://github.com/owner/repo/releases/tag/v1.3.0",
  "tag": "v1.3.0",
  "title": "v1.3.0",
  "draft": false,
  "prerelease": false
}
```

---

## Example 6: Trigger Deploy Workflow

### User Request
```
"Deploy to staging"
```

### Skill Execution

**Step 1**: Trigger workflow
```bash
AGENT_NAME=github gh workflow run deploy.yml \
  --ref main \
  -f environment=staging
```

**Step 2**: Get run ID
```bash
AGENT_NAME=github gh run list --workflow deploy.yml --limit 1 --json databaseId
# [{"databaseId":9876543210}]
```

**Step 3**: Return status
```json
{
  "status": "SUCCESS",
  "run_id": "9876543210",
  "workflow": "deploy.yml",
  "ref": "main",
  "run_url": "https://github.com/owner/repo/actions/runs/9876543210"
}
```

---

## Example 7: CI Failure with UV Detection

### Scenario
CI failed with UV lockfile error

### monitor_ci Output
```json
{
  "status": "SUCCESS",
  "workflow_status": "completed",
  "conclusion": "failure",
  "workflow_runs": [{
    "id": "1111111111",
    "name": "CI",
    "status": "completed",
    "conclusion": "failure",
    "jobs": [{
      "name": "test",
      "status": "completed",
      "conclusion": "failure"
    }]
  }],
  "summary": "CI failed in job test: UV lockfile out of sync",
  "recommended_actions": [
    "Run uv lock locally to regenerate lockfile",
    "Commit and push uv.lock",
    "Ensure UV version matches between local and CI"
  ],
  "uv_failure_detected": true,
  "uv_failure_type": "lockfile_conflict"
}
```

---

## Example 8: Error Recovery - 403 Forbidden

### Scenario
User tries to merge PR but lacks permissions

### Skill Execution
```bash
AGENT_NAME=github gh pr merge 42 --squash
# Error: Must have push access to repository
```

### Error Response
```json
{
  "status": "FAILURE",
  "failure_details": {
    "failure_type": "github_api_error",
    "error_code": 403,
    "error_message": "Must have push access to repository",
    "error_classification": "PERMANENT",
    "retry_attempted": false,
    "recovery_suggestions": [
      "Verify your token has repo scope: gh auth status",
      "Check you have write access to this repository",
      "For organization repos, verify SSO authorization"
    ]
  }
}
```

---

## Common Patterns

### Full PR Workflow
```
1. Create feature branch (branch-strategy skill)
2. Make changes (domain specialists)
3. Commit changes (source-control skill)
4. Push branch (branch-strategy skill)
5. Create PR (github skill)
6. Monitor CI (github skill)
7. Merge PR (github skill)
```

### Release Workflow
```
1. Compute next version (tag-release skill)
2. Create git tag (tag-release skill)
3. Push tag (branch-strategy skill)
4. Create GitHub release (github skill)
```
