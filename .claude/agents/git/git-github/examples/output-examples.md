# Output Examples

**Purpose**: JSON output examples for all 3 git-github operations

---

## Example 1: analyze_changes (Success)

**Scenario**: Agent creation with multiple file types

**Git Status**:
```
M  .claude/agents/git-github.md
M  .claude/agents/dev-tools/schemas/git-github.schema.json
M  CLAUDE.md
A  docs/00-project/SECURITY.md
A  scripts/generate_filegrouper_dataset.py
```

**Output**:
```json
{
  "status": "SUCCESS",
  "agent": "git-github",
  "operation_type": "analyze_changes",
  "summary": "Grouped 5 files into 2 semantic commits with 0.83 avg confidence",
  "confidence": 0.83,
  "execution_timestamp": "2025-01-10T12:34:56Z",
  "agent_specific_output": {
    "current_branch": "main",
    "modified_files": 3,
    "new_files": 2,
    "deleted_files": 0,
    "commit_groups": [
      {
        "group_id": "group_1",
        "files": [
          ".claude/agents/git-github.md",
          ".claude/agents/dev-tools/schemas/git-github.schema.json"
        ],
        "change_type": "feat",
        "scope": "agent-git-github",
        "message": "feat(agent-git-github): redesign as three-operation worker agent",
        "grouping_rationale": "Test-impl pairing (0.90): Schema validates agent operations",
        "grouping_confidence": 0.90,
        "heuristics_applied": ["test_impl_pairing", "directory_scope"]
      },
      {
        "group_id": "group_2",
        "files": [
          "CLAUDE.md",
          "docs/00-project/SECURITY.md",
          "scripts/generate_filegrouper_dataset.py"
        ],
        "change_type": "docs",
        "scope": "project",
        "message": "docs(project): add security assessment and FileGrouper validation script",
        "grouping_rationale": "Functional coupling (0.75): Documentation + supporting tooling",
        "grouping_confidence": 0.75,
        "heuristics_applied": ["functional_coupling", "directory_scope"]
      }
    ],
    "grouping_summary": {
      "total_files": 5,
      "total_groups": 2,
      "average_confidence": 0.825,
      "high_confidence_groups": 1,
      "medium_confidence_groups": 1,
      "low_confidence_groups": 0
    },
    "remote_sync_status": {
      "remote_branch": "origin/main",
      "branch_diverged": true,
      "ahead": 0,
      "behind": 1,
      "last_fetch": "2025-01-10T12:34:00Z",
      "recommendation": "git pull --rebase before committing"
    }
  }
}
```

---

## Example 2: execute_commits (Success)

**Scenario**: Committing a single group

**Input**:
```json
{
  "operation_type": "execute_commits",
  "groups_to_commit": [
    {
      "group_id": "group_1",
      "files": [
        ".claude/agents/git-github.md",
        ".claude/agents/dev-tools/schemas/git-github.schema.json"
      ],
      "message": "feat(agent-git-github): redesign as three-operation worker agent\n\n- analyze_changes: intelligent file grouping\n- execute_commits: selective commit execution\n- monitor_ci: GitHub Actions monitoring\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\n\nCo-Authored-By: Claude <noreply@anthropic.com>"
    }
  ]
}
```

**Output**:
```json
{
  "status": "SUCCESS",
  "agent": "git-github",
  "operation_type": "execute_commits",
  "summary": "Successfully committed 1 group (2 files)",
  "confidence": 1.0,
  "execution_timestamp": "2025-01-10T12:35:22Z",
  "agent_specific_output": {
    "committed_groups": [
      {
        "group_id": "group_1",
        "commit_sha": "a1b2c3d4e5f6",
        "message": "feat(agent-git-github): redesign as three-operation worker agent",
        "files_committed": 2,
        "timestamp": "2025-01-10T12:35:15Z"
      }
    ],
    "summary": {
      "requested": 1,
      "committed": 1,
      "failed": 0,
      "total_files": 2
    },
    "remote_sync_status": {
      "branch_diverged": true,
      "ahead": 1,
      "behind": 0,
      "recommendation": "Ready to push with 'git push origin main'"
    }
  }
}
```

---

## Example 3: execute_commits (Failure - Merge Conflict)

**Scenario**: Commit fails due to merge conflict

**Output**:
```json
{
  "status": "FAILURE",
  "agent": "git-github",
  "operation_type": "execute_commits",
  "summary": "Failed to commit group_2: merge conflict detected",
  "confidence": 0.0,
  "execution_timestamp": "2025-01-10T12:36:00Z",
  "failure_details": {
    "failure_type": "merge_conflict",
    "error_classification": "PERMANENT",
    "retry_attempts": 0,
    "reasons": [
      "Merge conflict in CLAUDE.md",
      "Commit aborted"
    ],
    "git_error": "error: Merge conflict in CLAUDE.md\nfatal: commit aborted",
    "partial_commits": [
      {
        "group_id": "group_1",
        "commit_sha": "a1b2c3d4e5f6",
        "message": "feat(agent-git-github): redesign as three-operation worker agent"
      }
    ],
    "failed_group": "group_2",
    "recovery_suggestions": [
      "Resolve merge conflict in CLAUDE.md",
      "Run 'git status' to see conflict markers",
      "Edit file to resolve conflicts",
      "Run 'git add CLAUDE.md' after resolution",
      "Re-run execute_commits for remaining groups"
    ]
  }
}
```

---

## Example 4: monitor_ci (Success - All Checks Passed)

**Scenario**: CI completed successfully

**Output**:
```json
{
  "status": "SUCCESS",
  "agent": "git-github",
  "operation_type": "monitor_ci",
  "summary": "All checks passed for commit a1b2c3d4e5f6 (4.5 minutes)",
  "confidence": 1.0,
  "execution_timestamp": "2025-01-10T12:40:00Z",
  "agent_specific_output": {
    "workflow_status": "completed",
    "conclusion": "success",
    "workflow_runs": [
      {
        "run_id": "7891234567",
        "workflow_name": "CI/CD Pipeline",
        "status": "completed",
        "conclusion": "success",
        "commit_sha": "a1b2c3d4e5f6",
        "branch": "main",
        "duration_minutes": 4.5,
        "started_at": "2025-01-10T12:35:30Z",
        "completed_at": "2025-01-10T12:40:00Z",
        "jobs": [
          { "name": "lint", "conclusion": "success", "duration_seconds": 45 },
          { "name": "test", "conclusion": "success", "duration_seconds": 120 },
          { "name": "build", "conclusion": "success", "duration_seconds": 90 }
        ]
      }
    ],
    "summary": "All checks passed for commit a1b2c3d4e5f6"
  }
}
```

---

## Example 5: monitor_ci (Failure - Test Failures)

**Scenario**: CI failed with pytest errors

**Output**:
```json
{
  "status": "SUCCESS",
  "agent": "git-github",
  "operation_type": "monitor_ci",
  "summary": "CI failed: 2 test failures in pytest step",
  "confidence": 1.0,
  "execution_timestamp": "2025-01-10T12:40:00Z",
  "agent_specific_output": {
    "workflow_status": "completed",
    "conclusion": "failure",
    "workflow_runs": [
      {
        "run_id": "7891234567",
        "workflow_name": "CI/CD Pipeline",
        "status": "completed",
        "conclusion": "failure",
        "commit_sha": "a1b2c3d4e5f6",
        "branch": "main",
        "duration_minutes": 3.2,
        "failed_jobs": [
          {
            "name": "test",
            "conclusion": "failure",
            "failed_step": "Run pytest",
            "duration_seconds": 95,
            "error_summary": "2 tests failed",
            "error_details": [
              "FAILED tests/agents/test_git_github.py::test_analyze_changes - AssertionError",
              "FAILED tests/agents/test_git_github.py::test_execute_commits - TypeError"
            ],
            "affected_files": ["tests/agents/test_git_github.py"]
          }
        ]
      }
    ],
    "summary": "CI failed: 2 test failures in pytest step",
    "recommended_actions": [
      "Delegate to debugger agent for test_analyze_changes (AssertionError)",
      "Delegate to debugger agent for test_execute_commits (TypeError)",
      "Run 'gh run view 7891234567 --log' for full logs",
      "Re-run CI after fixes"
    ]
  }
}
```

---

## Example 6: monitor_ci (Failure - Circuit Breaker Open)

**Scenario**: GitHub API experiencing outage

**Output**:
```json
{
  "status": "FAILURE",
  "agent": "git-github",
  "operation_type": "monitor_ci",
  "summary": "GitHub CLI circuit breaker OPEN (5 consecutive 5xx errors)",
  "confidence": 0.0,
  "execution_timestamp": "2025-01-10T12:45:00Z",
  "failure_details": {
    "failure_type": "circuit_breaker_open",
    "error_classification": "TRANSIENT",
    "circuit_breaker_state": "OPEN",
    "wait_duration_seconds": 60,
    "consecutive_failures": 5,
    "last_error": "503 Service Unavailable",
    "affected_operation": "gh_run_view",
    "recovery_suggestions": [
      "GitHub CLI experiencing outage (5 consecutive 5xx errors)",
      "Circuit breaker OPEN for 60 seconds",
      "Check status: https://www.githubstatus.com/",
      "Will retry automatically after wait period",
      "Alternative: Use GitHub web UI for urgent checks"
    ]
  }
}
```
