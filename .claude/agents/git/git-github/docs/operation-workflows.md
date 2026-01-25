# Operation Workflows

**Purpose**: Detailed workflows for the 3 git-github operations

---

## Operation 1: analyze_changes

**Purpose**: Analyze git changes and return intelligent file groups
**Risk Level**: Low (read-only)

### What It Does
- Run `git status` and `git diff` to discover changes
- Apply FileGrouper heuristics to group related files
- Generate Conventional Commit messages for each group
- Calculate grouping confidence scores
- Return structured groups to orchestrator

### What It Does NOT Do
- NO commits
- NO quality gates
- NO branch creation
- NO delegation to other agents

### Workflow

1. **Check remote state** (multi-developer safety):
   ```bash
   AGENT_NAME=git-github git fetch origin
   AGENT_NAME=git-github git rev-parse --abbrev-ref @{upstream}
   AGENT_NAME=git-github git rev-list --left-right --count HEAD...@{upstream}
   ```

2. **Discover changes**:
   ```bash
   AGENT_NAME=git-github git status --porcelain
   AGENT_NAME=git-github git diff --stat
   ```

3. **Apply FileGrouper heuristics** (see `filegrouper-heuristics.md`)

4. **Generate Conventional Commit messages** (see `conventional-commits.md`)

5. **Calculate confidence scores**

6. **Return structured groups with remote sync status**

### Input Schema

```json
{
  "operation_type": "analyze_changes",
  "include_context": true  // optional: include git blame/log context
}
```

### Output Fields

- `current_branch`: Current git branch
- `modified_files`, `new_files`, `deleted_files`: File counts
- `commit_groups[]`: Array of grouped files with messages and confidence
- `grouping_summary`: Statistics (total files, groups, avg confidence)
- `remote_sync_status`: Ahead/behind counts, sync recommendation

---

## Operation 2: execute_commits

**Purpose**: Execute git commits for specific groups
**Risk Level**: HIGH (permanently modifies git history)

### What It Does
- Receive groups to commit from orchestrator
- Execute `git add` + `git commit` for each group sequentially
- Use provided commit messages
- Return commit SHAs
- Handle git errors gracefully

### What It Does NOT Do
- NO automatic pushing to remote
- NO branch creation or switching
- NO quality gates or validation
- NO delegation to other agents

### Workflow

1. **Check remote state**:
   ```bash
   AGENT_NAME=git-github git fetch origin
   AGENT_NAME=git-github git status -sb
   ```
   - If remote ahead: Show warning, recommend pull

2. **Validate files exist and are modified**

3. **For each group** (sequential execution):
   ```bash
   # Reset staging area (non-destructive)
   AGENT_NAME=git-github git reset HEAD
   
   # Stage files
   AGENT_NAME=git-github git add file1 file2 ...
   
   # Commit with heredoc
   AGENT_NAME=git-github git commit -F- <<'EOF'
   feat(scope): subject line
   
   Body text here.
   
   Footer here.
   EOF
   
   # Capture SHA
   AGENT_NAME=git-github git rev-parse HEAD
   ```

4. **Return summary with all commit SHAs and remote sync status**

### Input Schema

```json
{
  "operation_type": "execute_commits",
  "groups_to_commit": [
    {
      "group_id": "group_1",
      "files": ["file1.py", "file2.py"],
      "message": "feat(scope): complete commit message with footer"
    }
  ]
}
```

### Output Fields (Success)

- `committed_groups[]`: Array with group_id, commit_sha, message, files_committed
- `summary`: Counts (requested, committed, failed, total_files)
- `remote_sync_status`: Ahead/behind counts, push recommendation

### Output Fields (Failure)

- `failure_type`: git_command_error, merge_conflict, etc.
- `partial_commits[]`: Commits created before failure
- `failed_group`: Group ID that caused failure
- `recovery_suggestions[]`: Actionable recovery steps

---

## Operation 3: monitor_ci

**Purpose**: Check GitHub Actions workflow status
**Risk Level**: Low (read-only)

### Hybrid Implementation

- **GitHub CLI** (`gh run` commands): Workflow monitoring
- **GitHub MCP**: Issues, PRs, repository operations

GitHub MCP server doesn't provide workflow run tools, so CLI is required.

### What It Does
- Query workflow status via GitHub CLI
- Parse failure details (job names, step names, errors)
- Identify UV-specific failure patterns
- Generate actionable recommendations
- Return structured status report

### What It Does NOT Do
- NO automatic fixes
- NO re-running workflows
- NO PR creation
- NO delegation to other agents

### Workflow

1. **Determine target** (commit SHA, run ID, or branch)

2. **Query GitHub Actions**:
   ```bash
   # List recent runs
   AGENT_NAME=git-github gh run list --limit 10 [--branch main]
   
   # View specific run
   AGENT_NAME=git-github gh run view <run-id>
   
   # Get failed logs
   AGENT_NAME=git-github gh run view <run-id> --log-failed
   ```

3. **Parse failure details** (job names, step names, error messages)

4. **Identify UV failure patterns** (6 common patterns):
   - UV sync failures
   - Command not found
   - Lockfile conflicts
   - Venv issues
   - Python execution errors
   - Test failures

5. **Generate recommendations** (including Context7 research if novel pattern)

6. **Return structured status report**

### Input Schema

```json
{
  "operation_type": "monitor_ci",
  "commit_sha": "abc123",       // optional: specific commit
  "run_id": "7891234567",       // optional: specific run
  "branch": "feature/branch",   // optional: defaults to current
  "wait_for_completion": false  // optional: poll until complete
}
```

### Output Fields (Success)

- `workflow_status`: queued | in_progress | completed
- `conclusion`: success | failure | cancelled | etc.
- `workflow_runs[]`: Run details with jobs, durations
- `summary`: Human-readable summary
- `recommended_actions[]`: Next steps (for failures)

---

## UV CI Failure Patterns

Quick reference for 6 common UV patterns in GitHub Actions:

| Pattern | Symptom | Recommendation |
|---------|---------|----------------|
| UV sync failure | "No matching distribution" | Check pyproject.toml constraints |
| Command not found | "uv: command not found" | Verify UV install step in workflow |
| Lockfile conflict | "Lock file out of sync" | Regenerate with `uv lock` |
| Venv issues | "No module named..." | Check venv activation in workflow |
| Python execution | "Python version mismatch" | Verify python-version in workflow |
| Test failures | pytest errors | Delegate to debugger agent |

**Detailed troubleshooting**: See `.claude/docs/01-guides/github-integration-guide.md`
