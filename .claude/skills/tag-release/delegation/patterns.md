# Delegation Patterns for Tag Release Skill

**Purpose**: Task() templates for delegating tag/release operations

---

## Skill Delegation Model

This skill provides **methodology** for Task() delegation. It does NOT execute git commands directly.

**What This Skill Does**:
- Provides operation definitions
- Guides SemVer version computation
- Defines release note formatting
- Specifies error handling patterns

**What Agents Do**:
- Execute actual git commands
- Return structured results
- Handle retries per skill guidance

---

## Standard Delegation Templates

### compute_next_version

```
Task(source-control) with:
  goal: "Compute next semantic version from commit history"
  operation: "compute_next_version"
  context: {
    current_version: "v1.2.3",  # Optional, auto-detect if omitted
    include_prerelease: false
  }
  expected_output: {
    current_version: "v1.2.3",
    next_version: "v1.3.0",
    bump_type: "minor",
    reason: "...",
    commits_analyzed: 15
  }
```


### create_release_tag

```
Task(source-control) with:
  goal: "Create annotated release tag"
  operation: "create_release_tag"
  context: {
    version: "v1.3.0",
    message: "Release v1.3.0\n\n## Features\n- ...",
    sign: false
  }
  expected_output: {
    status: "SUCCESS",
    tag: "v1.3.0",
    commit_sha: "abc1234567890"
  }
```

### list_tags

```
Task(source-control) with:
  goal: "List all version tags with metadata"
  operation: "list_tags"
  context: {
    pattern: "v*",
    limit: 20,
    sort: "version"
  }
  expected_output: {
    tags: [...],
    total_count: 15,
    latest: "v1.3.0"
  }
```

### delete_tag

```
Task(source-control) with:
  goal: "Delete release tag"
  operation: "delete_tag"
  context: {
    tag: "v1.3.0",
    delete_remote: false
  }
  expected_output: {
    status: "SUCCESS",
    deleted_local: true,
    deleted_remote: false
  }
```


### get_release_notes

```
Task(source-control) with:
  goal: "Generate release notes from commits"
  operation: "get_release_notes"
  context: {
    from_version: "v1.2.0",
    to_version: "HEAD"
  }
  expected_output: {
    from_version: "v1.2.0",
    to_version: "v1.3.0",
    notes: {
      breaking_changes: [...],
      features: [...],
      fixes: [...],
      other: [...]
    },
    markdown: "## v1.3.0\n\n..."
  }
```

---

## Orchestrator Workflow Pattern

Recommended orchestrator flow for release operations:

```
1. User requests "create a release"

2. Orchestrator delegates version computation:
   Task(source-control, operation="compute_next_version")
   
3. Agent returns suggested version with breakdown

4. Orchestrator presents to user:
   "Suggested version: v1.3.0 (minor bump)"
   "15 commits: 3 features, 5 fixes, 7 other"
   "Proceed? [y/n]"

5. If approved, orchestrator delegates:
   Task(source-control, operation="get_release_notes", from="v1.2.0")
   Task(source-control, operation="create_release_tag", version="v1.3.0")
   
6. Agent returns tag info and release notes

7. Orchestrator reports results to user
```

