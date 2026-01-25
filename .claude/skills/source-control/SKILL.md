# Source Control Skill

**Domain**: Development  
**Responsibility**: Commit workflows, file grouping, staging operations  
**Triggers**:
  - analyze_changes metadata
  - staging workflow metadata
  - Conventional Commits metadata

---

## Overview

Owns the methodology and operations for:
- Analyzing file changes and grouping them semantically
- Staging files by logical group
- Generating commits following Conventional Commits standard
- Executing batch or single commits
- Handling staging-related errors

**Does NOT own**:
- Branch management (use branch-strategy skill)
- Tagging/releases (use tag-release skill)
- GitHub operations (use github skill)
- Push to remote (orchestrator decision)

---

## Core Operations

### categorize_files

Categorizes modified files by semantic domain before grouping.

```
Input: List of file paths from git status
Output: {
  categorized_files: {
    "database": ["migrations/001.sql", "models/user.py"],
    "api": ["routes/auth.py"],
    "ui": ["components/Button.tsx"],
    "config": ["pyproject.toml", ".env.example"],
    "tests": ["tests/test_auth.py"],
    "docs": ["docs/README.md"],
    "infrastructure": ["k8s/deployment.yaml"],
    "claude_code": [".claude/agents/dev.md"],
    "code": ["utils/helpers.py"]  // Fallback
  },
  category_counts: { ... }
}
```

**Detection Priority** (highest first):
1. claude_code (95): `.claude/agents/**`, `.claude/skills/**`, `.claude/commands/**`, `.claude/hooks/**`
2. database (100): `migrations/`, `models/`, `schema/`, `*.sql`, sqlalchemy imports
3. api (90): `routes/`, `handlers/`, `api/`, `controllers/`, FastAPI/Flask imports
4. ui (85): `components/`, `pages/`, `views/`, `*.tsx`, `*.jsx`, `*.css`, `*.scss`
5. config (80): `config/`, `settings/`, `*.env*`, `*.yaml`, `*.toml`, `pyproject.toml`
6. tests (75): `tests/`, `test_*.py`, `*_test.py`, `*.spec.*`
7. docs (70): `docs/`, `*.md`, `README*`, `CHANGELOG*`
8. infrastructure (65): `k8s/`, `terraform/`, `docker/`, `.github/`, `Dockerfile*`, `*.tf`
9. code (0): Fallback for unmatched files

---

### analyze_changes

Analyzes modified/staged files and groups them semantically using FileGrouper heuristics.


```
Input: List of modified/staged files from git status
Output: {
  commit_groups: [{
    group_id: string,
    category: string,  // From categorize_files
    files: string[],
    suggested_message: string,
    change_type: string,
    confidence: number
  }],
  grouping_summary: {
    total_files: number,
    total_groups: number,
    average_confidence: number
  }
}
Logic: Apply 7 FileGrouper heuristics in priority order (Semantic Categorization first)
```

**Workflow**:
1. Run `git status --porcelain` to discover changes
2. Run `git diff --stat` for change context
3. Apply FileGrouper heuristics (see reference/fileGrouper-heuristics.md)
4. Generate Conventional Commit messages per group
5. Calculate confidence scores
6. Return structured groups

**Confidence Thresholds**:
| Score | Classification | Action |
|-------|----------------|--------|
| 0.90+ | High | Auto-group recommended |
| 0.80-0.89 | Medium | `needs_review: true` flag |
| 0.75-0.79 | Low | `needs_confirmation: true` flag |
| <0.75 | Very low | Return FAILURE |

---

### stage_group

Stages files belonging to a specific commit group.


```
Input: group_id or list of file paths
Output: {
  status: "SUCCESS" | "FAILURE",
  staged_files: string[]
}
Logic: git add for specified files
```

**Workflow**:
1. Validate files exist and are modified
2. Execute `git add {files}`
3. Return staging report

**Notes**: Always use absolute paths. Validates file existence before staging.

---

### get_group_diff

Returns the unified diff for currently staged files.

```
Input: none (operates on staging area)
Output: {
  status: "SUCCESS",
  diff: string,
  files: string[],
  stats: { insertions: number, deletions: number }
}
Logic: git diff --cached
```

**Workflow**:
1. Run `git diff --cached --stat` for overview
2. Run `git diff --cached` for full diff
3. Return structured diff output

---

### unstage_all

Clears the staging area without modifying working directory.


```
Input: none
Output: { status: "SUCCESS" }
Logic: git reset HEAD
```

**Notes**: Non-destructive operation. Safe to call before staging new groups.

---

### execute_commits

Executes commits for multiple groups sequentially.

```
Input: {
  groups_to_commit: [{
    group_id: string,
    files: string[],
    message: string  // Full Conventional Commit message
  }]
}
Output: {
  status: "SUCCESS" | "PARTIAL" | "FAILURE",
  committed_groups: [{
    group_id: string,
    commit_sha: string,
    message: string,
    files_committed: string[]
  }],
  summary: {
    requested: number,
    committed: number,
    failed: number
  }
}
Logic: Sequential stage + commit for each group
```

**Workflow** (per group):
1. Clear staging area: `git reset HEAD`
2. Stage group files: `git add {files}`
3. Commit with heredoc: `git commit -F- <<'EOF' ... EOF`
4. Capture SHA: `git rev-parse HEAD`


**Pre-Commit Validation** (MANDATORY):
- Branch not detached HEAD
- No rebase/merge in progress
- All files exist and are modified
- Clear staging before each group

See reference/staging-workflows.md for detailed workflow.

---

### execute_single_commit

Commits currently staged files with provided message.

```
Input: {
  message: string  // Full Conventional Commit message
}
Output: {
  status: "SUCCESS" | "FAILURE",
  commit_sha: string,
  message: string,
  files_committed: string[]
}
Logic: Commit staged files
```

**Workflow**:
1. Verify files are staged: `git diff --cached --name-only`
2. Run pre-commit validation
3. Create commit with message
4. Return commit hash

**Notes**: Inherits ALL safety checks from execute_commits.

---

## Key Methodologies

### FileGrouper Heuristics

[See reference/fileGrouper-heuristics.md]


7 heuristics applied in priority order:

0. **Semantic Categorization** (2.0) - Categorize by domain FIRST
1. **Change Type Separation** (1.0) - NEVER mix commit types
2. **UV Dependency Management** (0.95) - Isolate pyproject.toml + uv.lock
3. **Test-Implementation Pairing** (0.90) - Group test + impl together
4. **Dependency Ordering** (0.85) - Respect import order
5. **Functional Coupling** (0.80) - Group related features
6. **Directory Scope** (0.75) - Fallback for remaining files

### Conventional Commits

[See reference/conventional-commits.md]

Format: `<type>(<scope>): <subject>`

Types: feat, fix, refactor, test, docs, build, style, chore, ci, perf, revert, wip

**Footer Required**:
```
Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Staging Workflows

[See reference/staging-workflows.md]

- Stage -> diff -> review -> commit cycle
- Group-based staging (don't mix groups)
- Error recovery patterns
- Pre-commit validation checklist

---

## Error Handling

[See reference/error-handling.md]


### Error Categories

| Category | Retry? | Action |
|----------|--------|--------|
| PERMANENT | No | Return FAILURE with recovery suggestions |
| TRANSIENT | Yes (3x) | Exponential backoff, then FAILURE |

### Common Staging Errors

| Error | Classification | Recovery |
|-------|---------------|----------|
| Lock file busy | TRANSIENT | Retry 1s, 2s, 4s backoff |
| Merge conflict | PERMANENT | Resolve conflict manually |
| Pre-commit hook failure | PERMANENT | Fix issues, re-stage |
| Detached HEAD | PERMANENT | Create branch or checkout |
| Files not modified | PERMANENT | Verify file status |

---

## Delegation Patterns

[See delegation/patterns.md]

This skill provides methodology for Task() delegation to implementation agents.

### Standard Delegation

```
Task(git-workflow) with:
  - operation: "analyze_changes" | "execute_commits"
  - files: [...] (for execute)
  - groups: [...] (for execute)
```

---

## Quality Gates

- FileGrouper confidence >= 0.75 for grouping
- Conventional Commits format enforced
- Pre-commit validation passed
- Error classification before ANY retry


---

## Bash Command Format

All git commands use AGENT_NAME prefix for logging:

```bash
AGENT_NAME=source-control git status --porcelain
AGENT_NAME=source-control git add {files}
AGENT_NAME=source-control git commit -F- <<'EOF'
{message}
EOF
AGENT_NAME=source-control git reset HEAD
```

---

## References

| File | Purpose |
|------|---------|
| reference/fileGrouper-heuristics.md | 7 heuristics with examples |
| reference/conventional-commits.md | Commit format standard |
| reference/staging-workflows.md | Detailed stage/commit workflows |
| reference/error-handling.md | Error classification patterns |
| delegation/patterns.md | Task() delegation templates |
| examples/usage-examples.md | End-to-end workflow examples |
