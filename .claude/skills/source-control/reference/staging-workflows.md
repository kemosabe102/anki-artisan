# Staging Workflows

**Purpose**: Detailed workflows for staging and commit operations

---

## Stage-Diff-Review-Commit Cycle

The standard workflow for committing changes:

```
1. analyze_changes -> Get file groups
2. stage_group -> Stage one group
3. get_group_diff -> Review staged changes
4. execute_single_commit -> Commit if approved
5. Repeat for remaining groups
```

**Alternative (batch)**: Use `execute_commits` to process all groups sequentially.

---

## analyze_changes Workflow

**Purpose**: Analyze git changes and return intelligent file groups
**Risk Level**: Low (read-only)

### Step 1: Check Remote State (Multi-Developer Safety)

```bash
AGENT_NAME=source-control git fetch origin
AGENT_NAME=source-control git rev-parse --abbrev-ref @{upstream}
AGENT_NAME=source-control git rev-list --left-right --count HEAD...@{upstream}
```

### Step 2: Discover Changes


```bash
AGENT_NAME=source-control git status --porcelain
AGENT_NAME=source-control git diff --stat
```

### Step 3: Apply FileGrouper Heuristics

See fileGrouper-heuristics.md for the 6 heuristics.

### Step 4: Generate Conventional Commit Messages

See conventional-commits.md for format.

### Step 5: Calculate Confidence Scores

### Step 6: Return Structured Groups with Remote Sync Status

**Output Fields**:
- `current_branch`: Current git branch
- `modified_files`, `new_files`, `deleted_files`: File counts
- `commit_groups[]`: Array of grouped files with messages and confidence
- `grouping_summary`: Statistics (total files, groups, avg confidence)
- `remote_sync_status`: Ahead/behind counts, sync recommendation

---

## execute_commits Workflow

**Purpose**: Execute git commits for specific groups
**Risk Level**: HIGH (permanently modifies git history)

### Step 1: Check Remote State


```bash
AGENT_NAME=source-control git fetch origin
AGENT_NAME=source-control git status -sb
```

- If remote ahead: Show warning, recommend pull

### Step 2: Validate Files Exist and Are Modified

### Step 3: For Each Group (Sequential Execution)

```bash
# Reset staging area (non-destructive)
AGENT_NAME=source-control git reset HEAD

# Stage files
AGENT_NAME=source-control git add file1 file2 ...

# Commit with heredoc
AGENT_NAME=source-control git commit -F- <<'EOF'
feat(scope): subject line

Body text here.

Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF

# Capture SHA
AGENT_NAME=source-control git rev-parse HEAD
```

### Step 4: Return Summary with All Commit SHAs and Remote Sync Status

---

## Pre-Commit Validation Checklist


**MANDATORY** checks before ANY git commit operation:

### Hard Checks (Failure = Abort)

- [ ] **Branch State**: Not detached HEAD, not mid-rebase/merge (`git status` shows clean state)
- [ ] **Rebase/Merge Check**: No `.git/rebase-merge` or `.git/MERGE_HEAD` present
- [ ] **Files Exist**: All files in commit group exist and show as modified/added/deleted in `git status`
- [ ] **Staging Clean Start**: Run `git reset HEAD` before staging (non-destructive, clears prior staging)

### Soft Checks (Warning, Proceed)

- [ ] **Main Branch Warning**: If on `main`/`master` -> Log: "Warning: Committing directly to main branch"
- [ ] **Remote Behind**: If remote is ahead -> Log: "Warning: Remote has commits not in local. Consider `git pull --rebase` first"

### Protected Branch Check (Configurable Blocker)

- [ ] **Protected Patterns**: If branch matches `release/*`, `prod`, `production` -> Return FAILURE requiring explicit confirmation

### Validation Failure Response

**If ANY hard check fails**:
```json
{
  "status": "FAILURE",
  "failure_details": {
    "failure_type": "pre_commit_validation_failed",
    "failed_checks": ["branch_state", "files_exist"],
    "recovery_suggestions": ["Resolve detached HEAD with 'git checkout <branch>'", "..."]
  }
}
```

Do NOT attempt commit. Return immediately with recovery suggestions.


---

## Iterative Review Workflow

For orchestrator-controlled commit loops:

### stage_group

**Input**: List of files to stage
**Action**: `git add {files}`
**Output**:
```json
{
  "status": "SUCCESS",
  "staged_files": ["path/to/file1.py", "path/to/file2.py"]
}
```
**Notes**: Use absolute paths. Validates files exist before staging.

### unstage_all

**Input**: None
**Action**: `git reset HEAD`
**Output**:
```json
{
  "status": "SUCCESS"
}
```
**Notes**: Non-destructive operation. Clears staging area without touching working directory.

### get_group_diff

**Input**: None (operates on currently staged files)
**Action**: `git diff --cached`
**Output**:
```json
{
  "status": "SUCCESS",
  "diff": "diff --git a/file.py b/file.py\n...",
  "files": ["path/to/file.py"],
  "stats": {"insertions": 42, "deletions": 10}
}
```
**Notes**: Returns empty diff if nothing staged.


### execute_single_commit

**Input**: Commit message (Conventional Commits format)
**Action**:
1. Verify files are staged (`git diff --cached --name-only`)
2. Run pre-commit validation (same as execute_commits)
3. Create commit with message
4. Return commit hash

**Output**:
```json
{
  "status": "SUCCESS",
  "commit_hash": "abc1234",
  "message": "feat(auth): add login endpoint",
  "files_committed": ["packages/auth/login.py"]
}
```

**Risk**: HIGH - requires pre-commit validation passed. Inherits ALL safety checks from execute_commits.

---

## Group-Based Staging Rules

1. **Never mix groups** in a single commit
2. **Clear staging area** before staging new group (`git reset HEAD`)
3. **Validate group integrity** before commit
4. **Sequential execution** - commit groups one at a time
5. **Capture SHA** after each successful commit
