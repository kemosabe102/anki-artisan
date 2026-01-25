# Git Workflow Phases

Detailed documentation for each phase of the `/git` command workflow.

---

## Phase 1: Validation (Automated)

**Delegate to:** `[debugger]` agent - `validate_pre_commit` operation

**Action:** Run `prepare-code-review.py` script

- Linting checks (ruff check)
- Formatting checks (ruff format)
- Unit tests on modified files
- Auto-fix any fixable issues

**Output:** PASS/FAIL with details
- PASS: Proceeds to Phase 2
- FAIL: Stops workflow, reports blockers to user

**Human involvement:** NONE (unless validation fails)

**Duration:** ~2 minutes

### Validation Output Schema

```json
{
  "status": "SUCCESS" | "FAILURE",
  "agent_specific_output": {
    "validation_status": "PASS" | "FAIL",
    "fixes_applied": [
      {"type": "linting", "files": [...], "description": "..."},
      {"type": "test_failure", "files": [...], "description": "..."}
    ],
    "iteration_count": 1-3,
    "duration_seconds": X
  },
  "failure_details": {
    "blockers": [...],
    "delegation_needed": "development" | "none"
  }
}
```

---

## Phase 2: File Grouping (Automated)

**Delegate to:** `[source-control]` agent - `analyze_changes` operation

**Action:** Parse git status, apply FileGrouper heuristics

- Identify all modified/untracked files via `git status --porcelain`
- Apply heuristics: test-implementation pairing, functional coupling, directory scope
- Generate commit groups with Conventional Commits messages
- Calculate grouping confidence scores

**Output:** Commit groups with:
- Files list per group
- Change type (feat/fix/refactor/docs/test/style/chore)
- Scope (directory or module)
- Proposed commit message
- Grouping confidence (0.0-1.0)
- Grouping rationale

**UV Package Manager Awareness**: pyproject.toml + uv.lock grouped together (confidence: 0.95)

**Human involvement:** NONE

**Duration:** <5 seconds for 50 files + fetch time (~1-2 seconds)

**Remote Sync**: Automatically checks remote branch for new commits

### Grouping Output Schema

```json
{
  "commit_groups": [
    {
      "group_id": "group_1",
      "files": [...],
      "change_type": "feat",
      "scope": "agents",
      "message": "feat(agents): core agent schema & standards",
      "grouping_confidence": 0.90,
      "grouping_rationale": "Directory scope + functional coupling"
    }
  ],
  "grouping_summary": {
    "total_files": 24,
    "total_groups": 7,
    "average_confidence": 0.85
  }
}
```

---

## Phase 3: Iterative Review + Commit Loop

**CRITICAL**: This phase processes ONE GROUP AT A TIME with human decision at each group.

### Why Iterative Processing?

| Benefit | Explanation |
|---------|-------------|
| Focused review | Review 5-10 files per group vs 50+ files at once |
| Immediate feedback | See quality results and commit immediately |
| Granular control | Approve, reject, or edit each group independently |
| Resume capability | Pause workflow, fix issues, resume with `/git continue` |
| Better agent perf | Agents work better with smaller, cohesive changesets |

### Iterative Loop Workflow

```
FOR EACH group in commit_groups:
  STEP A: Stage group files
    - git reset HEAD (clear prior staging)
    - git add {group.files}
  
  STEP B: Quality Gates (PARALLEL)
    - tech-debt-investigator
    - sast-scanner
    - code-quality (ALWAYS - full code review)
  
  STEP C: Present Human Checkpoint
    - Show group summary, files, quality results
    - Show findings with severity
    - Present decision options
  
  STEP D: Human Decision
    [A] Approve & commit -> STEP E
    [R] Reject -> Skip group, continue to next
    [V] View diff -> Show diff, return to decision
    [E] Edit -> PAUSE workflow, user fixes, resume with /git continue
    [Q] Quit -> Exit loop, show summary
  
  STEP E: Commit (if approved)
    - Task(source-control, execute_single_commit)
    - Record commit hash
  
  STEP F: Unstage & Continue
    - git reset HEAD
    - Continue to next group
END FOR
```

### Human Decision Checkpoint Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GROUP {N} OF {TOTAL}: {commit_message}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Files ({count}):
  {status} {filepath}
  ...

Quality: {APPROVED|CHANGES_REQUIRED|BLOCKED}
  - Tech Debt: {status} (score: {N})
  - Security: {status} ({N} issues)
  - Code Review: {status}

{if findings}
Findings ({count}):
  [{severity}] {description}
           File: {filepath}:{line}
           Fix: {suggestion}
{end if}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DECISION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[A] Approve & commit    [R] Reject (skip)    [V] View diff
[E] Edit (pause workflow, fix issues, resume with /git continue)
[Q] Quit (keep remaining groups uncommitted)

{if blocked}
⚠️ This group has blocking issues. Fix issues [E] or reject [R].
{end if}

>
```

### End-of-Loop Summary Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ITERATIVE REVIEW COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Results:
  Committed: N groups (M files)
  Rejected:  N groups (M files)
  Skipped:   N groups (M files)

Commits created:
  1. {hash} {message}
  ...

{if rejected or skipped}
Uncommitted groups remain. To re-review: /git prepare
{end if}

To push: git push
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Quality Agents (Per-Group, Parallel)

| Agent | Scope | Purpose |
|-------|-------|---------|
| tech-debt-investigator | group.files | Technical debt analysis |
| sast-scanner | group.files | Security vulnerability scan |
| code-quality | group.files | Full code review (ALWAYS runs) |

**Duration:** ~30-60 seconds per group (agents run in parallel)

### Per-Group Quality Output Schema

```json
{
  "group_id": "group_1",
  "quality_results": {
    "tech_debt": {"score": 0.85, "issues": [...]},
    "security": {"vulnerabilities": [], "status": "PASS"},
    "code_review": {"status": "APPROVED", "suggestions": [...]}
  },
  "overall_status": "APPROVED|CHANGES_REQUIRED|BLOCKED",
  "blocking_issues": [],
  "findings": [
    {
      "severity": "HIGH|MEDIUM|LOW",
      "description": "...",
      "file": "path/to/file.py",
      "line": 42,
      "suggestion": "..."
    }
  ]
}
```


**Human involvement:** REQUIRED - User decides at each group checkpoint

---

## State Management

The orchestrator maintains state throughout the iterative review loop:

### Tracked State

| State Variable | Description |
|----------------|-------------|
| `groups[]` | Array of commit groups with status |
| `groups[].status` | `pending` \| `approved` \| `rejected` \| `committed` |
| `current_group_index` | Index of group being reviewed |
| `quality_results{}` | Quality gate results keyed by group_id |
| `committed_hashes[]` | Array of commit hashes created |
| `paused_at_group` | Group index when workflow paused (for `/git continue`) |

### State Transitions

```
pending -> (quality gates) -> presenting
presenting -> [A] -> committed
presenting -> [R] -> rejected
presenting -> [E] -> paused (user editing)
presenting -> [Q] -> (exit loop)
paused -> (/git continue) -> pending (re-run quality gates)
```


---

## /git continue Mode

**Purpose:** Resume workflow after user pauses to fix issues

### Resume Workflow

1. User selects `[E] Edit` at a checkpoint
2. Workflow pauses, records `paused_at_group` index
3. User makes code changes to fix issues
4. User runs `/git continue`
5. Workflow resumes from `paused_at_group`:
   - Re-stages group files
   - Re-runs quality gates (to verify fixes)
   - Presents checkpoint again with updated results
6. User can now approve, reject, edit again, or quit

### Continue Command Schema

```json
{
  "command": "/git continue",
  "action": "resume_iterative_review",
  "resume_from": "paused_at_group",
  "steps": [
    "git reset HEAD",
    "git add {paused_group.files}",
    "run_quality_gates(paused_group)",
    "present_checkpoint(paused_group)"
  ]
}
```

---

## Multi-Developer Support

**Purpose**: Handle scenarios where multiple developers work on same branch

**Remote Sync Checks**:
- **Phase 2 (analyze_changes)**: Automatic `git fetch origin` checks remote state
- **Phase 3 (per-group commit)**: Pre-commit remote check before each commit

**Workflow Pattern**:
```bash
# Start of session
git pull --rebase

# Analyze changes (includes remote check)
/git prepare
# Output shows: "Remote has 1 new commit"

# Pull before iterative review
git pull --rebase

# Run iterative review (approves/commits each group)
/git review

# Push all commits
git push
```

**Divergence Detection**:
- **Ahead**: You have local commits not pushed to remote
- **Behind**: Remote has commits you don't have locally
- **Diverged**: Both ahead and behind (requires rebase or merge)

---

## Implementation Notes

### Critical Rules

1. **NEVER automatically push** - only if user explicitly requests
2. **NEVER create PRs in main workflow** - separate operation
3. **NEVER switch branches** - operate on current branch only
4. **ALWAYS run quality gates** per group (unless --skip-quality flag)
5. **ALWAYS get human approval** at each group checkpoint
6. **NEVER commit secrets** (.env files, credentials, API keys)

### Performance Targets

| Phase | Target Duration |
|-------|-----------------|
| Validation | ~2 minutes |
| Grouping | <5 seconds |
| Per-group quality gates | ~30-60 seconds |
| Human decision | (user time) |
| Per-group commit | <2 seconds |
| **Total per group** | ~1-2 minutes + user time |

### Agent Delegation Pattern

```text
Claude Code (orchestrator)
|-- [debugger] validate_pre_commit
|   |-- IF FAIL -> retry with fixes -> re-run (max 3 attempts)
|-- [source-control] analyze_changes
|-- FOR EACH group:
|   |-- [source-control] stage_group
|   |-- PARALLEL: [tech-debt-investigator], [sast-scanner], [code-quality]
|   |-- Present checkpoint -> HUMAN DECISION
|   |   |-- [A] Approve -> [source-control] execute_single_commit
|   |   |-- [R] Reject -> skip, continue
|   |   |-- [V] View diff -> show diff, return to decision
|   |   |-- [E] Edit -> pause, await /git continue
|   |   |-- [Q] Quit -> exit loop, show summary
|   |-- [source-control] unstage_all
|-- Show end-of-loop summary
```

### Decision Flow Diagram

```
┌─────────────────┐
│  Stage Group    │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Quality Gates   │ (parallel: tech-debt, sast, code-review)
└────────┬────────┘
         ▼
┌─────────────────┐
│   Checkpoint    │◄──────────────────────────────┐
└────────┬────────┘                               │
         ▼                                        │
    ┌────────┐                                    │
    │Decision│                                    │
    └───┬────┘                                    │
        │                                         │
   ┌────┼────┬────────┬────────┐                  │
   ▼    ▼    ▼        ▼        ▼                  │
  [A]  [R]  [V]      [E]      [Q]                 │
   │    │    │        │        │                  │
   ▼    ▼    │        ▼        ▼                  │
Commit Skip  │     Pause    Exit Loop             │
   │    │    │        │        │                  │
   ▼    ▼    └────────┼────────┘                  │
   │    │             │                           │
   └────┴─────────────┼───────────────────────────┘
         │            │                 (next group)
         │      /git continue
         │            │
         └────────────┘
```
