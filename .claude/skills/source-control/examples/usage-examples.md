# Source Control Skill Usage Examples

**Purpose**: End-to-end workflow examples showing analyze_changes -> execute_commits flow

---

## Example 1: Simple Feature Commit

### Scenario

User modified 3 files for a new authentication feature:
- `packages/auth/login.py` (new feature code)
- `packages/auth/test_login.py` (tests)
- `docs/auth.md` (documentation)

### Step 1: analyze_changes

**Input**: Git working directory with modifications

**Output**:
```json
{
  "status": "SUCCESS",
  "current_branch": "feature/auth-login",
  "commit_groups": [
    {
      "group_id": "group_1",
      "files": ["packages/auth/login.py"],
      "suggested_message": "feat(auth): add login endpoint",
      "change_type": "feat",
      "confidence": 0.92
    },
    {
      "group_id": "group_2",
      "files": ["packages/auth/test_login.py"],
      "suggested_message": "test(auth): add login endpoint tests",
      "change_type": "test",
      "confidence": 0.90
    },
    {
      "group_id": "group_3",
      "files": ["docs/auth.md"],
      "suggested_message": "docs(auth): document login endpoint",
      "change_type": "docs",
      "confidence": 0.95
    }
  ],
  "grouping_summary": {
    "total_files": 3,
    "total_groups": 3,
    "average_confidence": 0.92
  }
}
```


**Rationale**: Change Type Separation (1.0) splits feat/test/docs despite functional relationship.

### Step 2: execute_commits

**Input**:
```json
{
  "groups_to_commit": [
    {
      "group_id": "group_1",
      "files": ["packages/auth/login.py"],
      "message": "feat(auth): add login endpoint\n\nGenerated with [Claude Code](https://claude.com/claude-code)\n\nCo-Authored-By: Claude <noreply@anthropic.com>"
    },
    {
      "group_id": "group_2",
      "files": ["packages/auth/test_login.py"],
      "message": "test(auth): add login endpoint tests\n\nGenerated with [Claude Code](https://claude.com/claude-code)\n\nCo-Authored-By: Claude <noreply@anthropic.com>"
    },
    {
      "group_id": "group_3",
      "files": ["docs/auth.md"],
      "message": "docs(auth): document login endpoint\n\nGenerated with [Claude Code](https://claude.com/claude-code)\n\nCo-Authored-By: Claude <noreply@anthropic.com>"
    }
  ]
}
```

**Output**:
```json
{
  "status": "SUCCESS",
  "committed_groups": [
    {"group_id": "group_1", "commit_sha": "abc1234", "message": "feat(auth): add login endpoint", "files_committed": ["packages/auth/login.py"]},
    {"group_id": "group_2", "commit_sha": "def5678", "message": "test(auth): add login endpoint tests", "files_committed": ["packages/auth/test_login.py"]},
    {"group_id": "group_3", "commit_sha": "ghi9012", "message": "docs(auth): document login endpoint", "files_committed": ["docs/auth.md"]}
  ],
  "summary": {
    "requested": 3,
    "committed": 3,
    "failed": 0
  }
}
```

---


## Example 2: UV Dependency Update

### Scenario

User updated dependencies:
- `pyproject.toml` (added new dependency)
- `uv.lock` (regenerated)
- `packages/core/utils.py` (uses new dependency)

### analyze_changes Output

```json
{
  "status": "SUCCESS",
  "commit_groups": [
    {
      "group_id": "group_1",
      "files": ["pyproject.toml", "uv.lock"],
      "suggested_message": "build(deps): add httpx dependency",
      "change_type": "build",
      "confidence": 0.95
    },
    {
      "group_id": "group_2",
      "files": ["packages/core/utils.py"],
      "suggested_message": "feat(core): add HTTP client utility",
      "change_type": "feat",
      "confidence": 0.88
    }
  ],
  "grouping_summary": {
    "total_files": 3,
    "total_groups": 2,
    "average_confidence": 0.92
  }
}
```

**Rationale**: UV Dependency Management (0.95) groups pyproject.toml + uv.lock together, separate from application code.

---


## Example 3: Iterative Review Workflow

### Scenario

Orchestrator wants to review each group before committing.

### Step 1: analyze_changes

Returns groups as shown above.

### Step 2: stage_group (Group 1)

**Input**: `files: ["packages/auth/login.py"]`

**Output**:
```json
{
  "status": "SUCCESS",
  "staged_files": ["packages/auth/login.py"]
}
```

### Step 3: get_group_diff

**Output**:
```json
{
  "status": "SUCCESS",
  "diff": "diff --git a/packages/auth/login.py b/packages/auth/login.py\n+def login(username, password):\n+    ...",
  "files": ["packages/auth/login.py"],
  "stats": {"insertions": 45, "deletions": 0}
}
```

### Step 4: User Reviews and Approves

### Step 5: execute_single_commit

**Input**: `message: "feat(auth): add login endpoint\n\n..."`

**Output**:
```json
{
  "status": "SUCCESS",
  "commit_sha": "abc1234",
  "message": "feat(auth): add login endpoint",
  "files_committed": ["packages/auth/login.py"]
}
```

### Step 6: Repeat for Remaining Groups

---


## Example 4: Partial Failure Recovery

### Scenario

Batch commit fails on group 3 due to pre-commit hook.

### execute_commits Output

```json
{
  "status": "PARTIAL",
  "committed_groups": [
    {"group_id": "group_1", "commit_sha": "abc1234", "message": "feat(auth): add login", "files_committed": ["login.py"]},
    {"group_id": "group_2", "commit_sha": "def5678", "message": "test(auth): add tests", "files_committed": ["test_login.py"]}
  ],
  "failure_details": {
    "failure_type": "pre_commit_hook_failure",
    "failed_group": "group_3",
    "error_classification": "PERMANENT",
    "last_error": "Linting failed: docs/auth.md:15 line too long",
    "recovery_suggestions": [
      "Groups 1-2 committed successfully",
      "Fix linting error in docs/auth.md line 15",
      "Re-stage and commit group_3 separately"
    ]
  },
  "summary": {
    "requested": 3,
    "committed": 2,
    "failed": 1
  }
}
```

### Recovery

1. User fixes linting error in `docs/auth.md`
2. Re-run with only group_3:
   ```json
   {
     "groups_to_commit": [
       {"group_id": "group_3", "files": ["docs/auth.md"], "message": "docs(auth): document login endpoint\n\n..."}
     ]
   }
   ```

---

## Example 5: Low Confidence Grouping

### Scenario

Files have ambiguous relationships, confidence below threshold.

### analyze_changes Output

```json
{
  "status": "SUCCESS",
  "commit_groups": [
    {
      "group_id": "group_1",
      "files": ["utils.py", "helpers.py", "common.py"],
      "suggested_message": "refactor(core): update utility modules",
      "change_type": "refactor",
      "confidence": 0.72,
      "needs_confirmation": true
    }
  ],
  "grouping_summary": {
    "total_files": 3,
    "total_groups": 1,
    "average_confidence": 0.72
  }
}
```

### Orchestrator Response

Because confidence < 0.75, orchestrator should:
1. Present grouping to user with warning
2. Ask for explicit confirmation or manual regrouping
3. Do NOT auto-proceed with execute_commits
