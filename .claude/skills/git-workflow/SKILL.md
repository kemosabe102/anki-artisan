---
name: git-workflow
description: >
  Reference guide for the two-phase git workflow: PREPARE and COMMIT.
  This skill is REFERENCE-ONLY. Execution logic lives in .claude/commands/git.md.
  Do NOT call this skill directly - use /git command instead.
---

# Git Workflow (Reference Guide)

**This skill is reference-only. It explains WHY each step exists.**

**Execution logic**: `.claude/commands/git.md`

---

## Overview

The git workflow has two phases:

| Phase | Purpose |
|-------|---------|
| **PREPARE** | Analyze changes → Group into commits → Run quality gates → Present summary |
| **COMMIT** | Execute commits for user-selected groups |

**Invocation**: `/git prepare` or `/git commit <groups>`

---

## Why This Workflow Exists

### Problem: Ad-hoc Commits
Without structure, commits become:
- Too large (10+ unrelated files)
- Poorly categorized (mixing features/fixes/docs)
- Missing quality validation
- Hard to review and revert

### Solution: Structured Two-Phase Approach
1. **PREPARE phase** forces analysis before commit
2. **Quality gates** catch issues before they reach main
3. **Semantic grouping** creates atomic, reviewable commits
4. **Self-healing** fixes common issues automatically

---

## Execution Contract (Reference)

The prepare workflow enforces this contract:

| Step | Purpose | Skip Flag | Why Mandatory? |
|------|---------|-----------|----------------|
| 0 | CI Validation | `--skip-validation` | Fail fast - don't group broken code |
| 1 | Semantic Categorization | None | Ensure domain isolation |
| 2 | File Grouping | None | Create atomic commits |
| 3 | Quality Gates | `--skip-quality` | Prevent critical issues |
| 4 | Present Summary | None | User must approve |

**Why Step 0 is blocking**: If CI fails, grouping is wasted work. Fix issues first.

**Why Steps 1-2 cannot be skipped**: Without grouping, there's nothing to commit.

---

## Self-Healing Design (Reference)

### Why Automatic Repair?
Most CI failures are fixable:
- 80%+ of lint errors are auto-fixable by ruff
- Many test failures are fixture/mock issues
- Self-healing saves developer time

### Why Confidence Decay?
As we attempt more repairs, we're increasingly likely to introduce new bugs:
- **Attempt 1** (0.85): High confidence - aggressive auto-fix
- **Attempt 2** (0.70): Medium - more conservative  
- **Attempt 3** (0.55): Low - report fixable issues only

### Why Escalate ENVIRONMENT?
Environment issues (missing dependencies, network, permissions) cannot be fixed programmatically. Immediate escalation prevents wasted repair attempts.

---

## Semantic Categories (Reference)

### Why 9 Categories?
Each category has different:
- Quality gate agents
- Security concerns
- Review focus areas

| Category | Why Separate? |
|----------|---------------|
| database | SQL injection risk, migration safety |
| api | Auth bypass, input validation |
| ui | XSS, accessibility |
| config | Secrets exposure |
| tests | Coverage, flakiness |
| docs | Link validation |
| infrastructure | Manifest validity |
| claude_code | Agent quality, schema compliance |
| code | General code quality |

### Why Never Mix Categories?
- Different reviewers for different domains
- Easier to revert specific changes
- Cleaner git history

---

## FileGrouper Heuristics (Reference)

### Why These 7 Heuristics?

| Heuristic | Why? |
|-----------|------|
| Semantic Categorization | Domain experts review domain code |
| Change Type Separation | Never mix feat/fix/docs - confuses reviewers |
| UV Dependency Management | Isolate dependency changes from app code |
| Test-Implementation Pairing | Keep test with code for context |
| Dependency Ordering | Foundation commits enable dependent commits |
| Functional Coupling | Related code should be reviewed together |
| Directory Scope | Fallback when no other signal |

### Conflict Resolution
Higher confidence wins. Change Type Separation (1.0) beats Test-Implementation Pairing (0.90).

---

## Quality Gates Design (Reference)

### Why Agent Matrix?
Different file types need different expertise:
- Python code → code-quality, sast-scanner
- Agent definitions → claude-code-ecosystem, architecture
- Infrastructure → deployment-release, sast-scanner

### Why Universal + Dynamic Agents?
- **Universal** (always run): Baseline quality for all code
- **Dynamic** (category-based): Specialized checks for specific domains

### Why Parallel Execution?
- Quality gates are independent per group
- Parallel reduces total review time
- Max 5 agents prevents resource exhaustion

---

## Status Classification (Reference)

### Why Three Statuses?

| Status | Meaning | User Action |
|--------|---------|-------------|
| READY_TO_COMMIT | No issues, safe to commit | Can commit immediately |
| NEEDS_REVIEW | Minor issues, likely OK | Should review before commit |
| BLOCKED | Critical issues | Must fix before commit |

### Why Default Threshold 0.80?
- Below 0.70: Too many uncertain groupings
- Above 0.90: Too strict for normal development
- 0.80: Good balance of quality and velocity

---

## Commit Message Format (Reference)

### Why Conventional Commits?
- Automated changelog generation
- Semantic versioning automation
- Clear commit history

### Format
```
<type>(<scope>): <description>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Types
- `feat`: New feature (minor version bump)
- `fix`: Bug fix (patch version bump)
- `refactor`: Code restructuring (no version bump)
- `test`: Test changes
- `docs`: Documentation
- `style`: Formatting
- `perf`: Performance
- `ci`: CI/CD
- `build`: Build system
- `chore`: Maintenance
- `revert`: Revert commit

---

## Safety Constraints (Reference)

### Why Forbidden Operations?

| Operation | Why Forbidden? |
|-----------|----------------|
| `git reset --hard` | Loses uncommitted work permanently |
| `git clean -fd` | Deletes untracked files permanently |
| `git checkout -- <file>` | Loses changes without stash |
| `git push --force` | Rewrites history, breaks collaborators |

### Why BLOCKED Groups Excluded from "commit all"?
BLOCKED groups have critical issues. Including them in "all" would commit known problems. User must explicitly `--force` to override.

---

## Reference Files

Detailed documentation:
- **Workflow contract**: `reference/execution-contract.md`
- **Agent matrix**: `reference/agent-matrix.md`
- **Category guidelines**: `reference/category-guidelines.md`
- **FileGrouper heuristics**: `.claude/skills/source-control/reference/fileGrouper-heuristics.md`
- **Command execution**: `.claude/commands/git.md`
