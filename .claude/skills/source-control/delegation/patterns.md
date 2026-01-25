# Delegation Patterns for Source Control Skill

**Purpose**: Task() templates for delegating source control operations

---

## Skill Delegation Model

This skill provides **methodology** for Task() delegation. It does NOT execute git commands directly.

**What This Skill Does**:
- Provides operation definitions
- Guides decision-making (FileGrouper heuristics)
- Defines output schemas
- Specifies error handling patterns

**What Agents Do**:
- Execute actual git commands
- Return structured results
- Handle retries per skill guidance

---

## Standard Delegation Templates

### analyze_changes

```
Task(git-workflow) with:
  goal: "Analyze current changes and return semantic file groups"
  operation: "analyze_changes"
  context: {
    include_context: true  // Include git blame/log context
  }
  expected_output: {
    commit_groups: [...],
    grouping_summary: {...},
    remote_sync_status: {...}
  }
```


### execute_commits (Batch)

```
Task(git-workflow) with:
  goal: "Commit file groups with provided messages"
  operation: "execute_commits"
  context: {
    groups_to_commit: [
      {
        group_id: "group_1",
        files: ["path/to/file1.py", "path/to/file2.py"],
        message: "feat(auth): add login endpoint\n\nGenerated with..."
      },
      {
        group_id: "group_2",
        files: ["path/to/test_file.py"],
        message: "test(auth): add login tests\n\nGenerated with..."
      }
    ]
  }
  expected_output: {
    status: "SUCCESS",
    committed_groups: [...],
    summary: {...}
  }
```

### execute_single_commit

```
Task(git-workflow) with:
  goal: "Commit currently staged files"
  operation: "execute_single_commit"
  context: {
    message: "feat(scope): subject line\n\nBody\n\nGenerated with..."
  }
  expected_output: {
    status: "SUCCESS",
    commit_sha: "...",
    files_committed: [...]
  }
```


### stage_group

```
Task(git-workflow) with:
  goal: "Stage files for review"
  operation: "stage_group"
  context: {
    files: ["path/to/file1.py", "path/to/file2.py"]
  }
  expected_output: {
    status: "SUCCESS",
    staged_files: [...]
  }
```

### get_group_diff

```
Task(git-workflow) with:
  goal: "Get diff for staged files"
  operation: "get_group_diff"
  expected_output: {
    status: "SUCCESS",
    diff: "...",
    stats: {...}
  }
```

### unstage_all

```
Task(git-workflow) with:
  goal: "Clear staging area"
  operation: "unstage_all"
  expected_output: {
    status: "SUCCESS"
  }
```

---

## Orchestrator Workflow Pattern


Recommended orchestrator flow for commit operations:

```
1. Orchestrator receives user request to commit changes

2. Orchestrator delegates:
   Task(git-workflow, operation="analyze_changes")
   
3. Agent returns groups with confidence scores

4. Orchestrator evaluates confidence:
   - >= 0.90: Proceed automatically
   - 0.80-0.89: Present to user, proceed if approved
   - 0.75-0.79: Require explicit user confirmation
   - < 0.75: Reject, suggest manual review

5. If approved, orchestrator delegates:
   Task(git-workflow, operation="execute_commits", groups=[...])
   
6. Agent returns commit SHAs

7. Orchestrator reports results to user
```

---

## Error Handling in Delegation

When agent returns FAILURE:

```
1. Check error_classification
2. If TRANSIENT: Agent already retried 3x, escalate to user
3. If PERMANENT: Present recovery_suggestions to user
4. If FATAL: Escalate immediately, do not retry
```

---

## Confidence-Based Routing

| Confidence | Orchestrator Action |
|------------|---------------------|
| >= 0.90 | Auto-proceed with execute_commits |
| 0.80-0.89 | Show groups, ask "Proceed?" |
| 0.75-0.79 | Show groups, require explicit "Yes" |
| < 0.75 | "Grouping uncertain, please review manually" |
