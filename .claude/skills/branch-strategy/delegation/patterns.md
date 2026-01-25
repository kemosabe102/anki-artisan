# Delegation Patterns

Task() templates for delegating branch operations to the source-control agent.

---

## Core Principle

**This skill provides methodology; agents execute.**

The branch-strategy skill:
- Defines operations and validation rules
- Provides naming convention enforcement
- Guides error recovery
- Interprets results

The source-control agent:
- Executes git commands
- Returns structured results
- Handles low-level errors

---

## Task() Templates

### list_branches

```python
Task(source-control) with:
  goal: "List all branches with tracking information"
  operation: "list_branches"
  params: {
    "include_remote": true
  }
  expected_output: {
    "local": ["main", "feature/user-auth", ...],
    "remote": ["origin/main", ...],
    "tracking": {...},
    "current": "feature/user-auth"
  }
```

**Orchestrator Usage**:
```
I need to see all branches including remote tracking info.

Task(source-control):
- Operation: list_branches
- Include remote: yes
```

---

### create_branch

```python
Task(source-control) with:
  goal: "Create new branch with naming validation"
  operation: "create_branch"
  params: {
    "name": "feature/user-authentication",
    "base": "main",
    "track_remote": false
  }
  pre_validation: "branch-strategy naming conventions"
  expected_output: {
    "branch": "feature/user-authentication",
    "base": "main",
    "created": true
  }
```

**Orchestrator Usage**:
```
Create a feature branch for user authentication based on main.

Pre-check: Validate "feature/user-authentication" against naming conventions
  -> PASS: Matches pattern feature/*

Task(source-control):
- Operation: create_branch
- Name: feature/user-authentication
- Base: main
```

---

### switch_branch

```python
Task(source-control) with:
  goal: "Safely switch to target branch"
  operation: "switch_branch"
  params: {
    "branch": "main",
    "stash_if_dirty": true
  }
  expected_output: {
    "switched_to": "main",
    "stashed": true,
    "stash_ref": "stash@{0}"
  }
```

**Orchestrator Usage**:
```
Switch to main branch, preserving any uncommitted work.

Task(source-control):
- Operation: switch_branch
- Target: main
- Stash if dirty: yes

Post-action: Report if stash was created
```

---

### delete_branch

```python
Task(source-control) with:
  goal: "Delete branch with safety checks"
  operation: "delete_branch"
  params: {
    "branch": "feature/old-feature",
    "force": false,
    "delete_remote": false
  }
  pre_checks: [
    "Not current branch",
    "Merged status (unless force=true)"
  ]
  expected_output: {
    "deleted": "feature/old-feature",
    "was_merged": true
  }
```

**Orchestrator Usage**:
```
Delete the old feature branch (already merged).

Pre-check: Verify not on feature/old-feature
  -> PASS: Currently on main

Task(source-control):
- Operation: delete_branch
- Branch: feature/old-feature
- Force: no (branch should be merged)
```

---

### fetch_remote

```python
Task(source-control) with:
  goal: "Fetch remote updates and report changes"
  operation: "fetch_remote"
  params: {
    "remote": "origin",
    "prune": true
  }
  expected_output: {
    "remote": "origin",
    "fetched_branches": [...],
    "pruned_refs": [...]
  }
```

**Orchestrator Usage**:
```
Fetch latest from origin and clean up stale refs.

Task(source-control):
- Operation: fetch_remote
- Remote: origin
- Prune: yes

Post-action: Report new branches and pruned refs to user
```

---

### get_remote_status

```python
Task(source-control) with:
  goal: "Check sync status with remote"
  operation: "get_remote_status"
  params: {
    "branch": "feature/user-auth"  # Optional, defaults to current
  }
  expected_output: {
    "branch": "feature/user-auth",
    "tracking": "origin/feature/user-auth",
    "ahead": 3,
    "behind": 1,
    "needs_sync": true,
    "sync_suggestion": "pull_rebase_recommended"
  }
```

**Orchestrator Usage**:
```
Check if current branch is in sync with remote.

Task(source-control):
- Operation: get_remote_status
- Branch: (current)

Post-action: Interpret results and suggest action
  -> "You are 3 commits ahead and 1 behind. Recommend: git pull --rebase"
```

---

## Composite Patterns

### Safe Branch Switch (Full)

```
1. Task(source-control): get_remote_status (check current branch)
2. If dirty: Task(source-control): switch_branch with stash_if_dirty=true
3. Task(source-control): fetch_remote (ensure target is fresh)
4. Task(source-control): switch_branch to target
5. Report: Switched from X to Y, stash created: yes/no
```

### Create Feature Branch (Full)

```
1. Validate name against naming conventions
   -> If invalid: Return error with suggestions
2. Task(source-control): fetch_remote (get latest)
3. Task(source-control): create_branch with base=main
4. Task(source-control): push with track_remote=true (optional)
5. Report: Created feature/X from main, tracking origin/feature/X
```

### Pre-PR Sync

```
1. Task(source-control): fetch_remote
2. Task(source-control): get_remote_status
3. If behind main: 
   - Task(source-control): rebase onto origin/main
   - Task(source-control): push --force-with-lease
4. Report: Branch is ready for PR (in sync with main)
```

---

## Error Handling in Delegation

When agent returns error, skill interprets:

```python
def handle_delegation_result(result: dict) -> dict:
    """Process agent result through skill lens."""
    if result["status"] == "SUCCESS":
        return result
    
    # Apply skill-level error handling
    error = result.get("error")
    
    if error == "branch_already_exists":
        return {
            "status": "FAILURE",
            "error": error,
            "recovery": "See reference/error-handling.md",
            "user_options": [
                "Switch to existing branch",
                "Use different name",
                "Delete existing and recreate"
            ]
        }
    
    # Default: Pass through with skill context
    return {
        "status": "FAILURE",
        "error": error,
        "skill_context": "branch-strategy",
        "reference": "reference/error-handling.md"
    }
```

---

## Quick Reference

| Operation | Agent | Key Params |
|-----------|-------|------------|
| list_branches | source-control | include_remote |
| create_branch | source-control | name, base, track_remote |
| switch_branch | source-control | branch, stash_if_dirty |
| delete_branch | source-control | branch, force, delete_remote |
| fetch_remote | source-control | remote, prune |
| get_remote_status | source-control | branch |
