# Usage Examples

Complete workflow examples for the `/git` command.

---

## Example 1: Full Workflow

Standard end-to-end workflow with all phases.

```bash
User: /git

# Step 1-4: Prepare (validation + grouping + quality gates)
Claude: [Executes workflow]

Output:
Pre-commit analysis complete

Validation: PASSED
- 5 linting errors auto-fixed
- All tests passing (190 passed, 1 skipped)

File Grouping: 7 groups identified
- Average confidence: 0.85

Quality Gates: PASSED
- No blocking issues
- 3 suggestions for group_1 (non-blocking)

Commit Groups Ready:

Group 1: feat(agents) - Core agent schema & standards
  Files: 2 files | Confidence: 0.90
  Quality: APPROVED_WITH_SUGGESTIONS

Group 2: refactor(agents) - Standardize agent definitions
  Files: 8 files | Confidence: 0.85
  Quality: APPROVED
  
... (5 more groups)

Next Steps:
- To commit all: /git commit
- To commit specific: /git commit --groups=1,2,3

User: /git commit

# Step 5: Execute commits
Claude: [Creates 7 commits]

Output:
7 commits created successfully

1. feat(agents): core agent schema & standards (abc123)
   Files: 2 files committed

2. refactor(agents): standardize agent definitions (def456)
   Files: 8 files committed

... (5 more)

Total: 7 commits, 24 files committed
Ready to push with `git push`

User: git push
# User manually pushes (or can ask Claude to push)
```

---

## Example 2: Selective Commit

Committing only specific groups while skipping others.

```bash
User: /git

# Presents 7 groups, user notices group 3 has suggestions they want to address

Output:
...
Group 3: feat(api) - New endpoint handlers
  Quality: APPROVED_WITH_SUGGESTIONS
  Suggestions:
  - Consider adding input validation
  - Missing docstrings on 2 functions
...
User: /git commit --groups=1,2,4,5,6,7

# Commits 6 groups, skips group 3
Claude: [Creates 6 commits]

Output:
6 commits created successfully
(Group 3 skipped as requested)

# User fixes group 3 manually
User: [Adds docstrings and validation to API handlers]

User: /git prepare

# Re-analyzes, finds 1 new group (the fixed files)
Output:
1 group ready to commit

Group 1: feat(api) - New endpoint handlers (updated)
  Quality: APPROVED
  Files: 3 files

User: /git commit
# Commits the fixed group
```

---

## Example 3: CI Failure Recovery

Handling CI failures after pushing.

```bash
User: git push

# ... CI runs ...

User: Check CI status

Claude: [Delegates to source-control monitor_ci]

Output:
CI Status: FAILED

Failed Jobs:
- run-tests (1m 35s)
  3 test failures detected

Test Failures:
1. tests/test_auth.py::test_jwt_validation
2. tests/test_auth.py::test_token_expiry  
3. tests/test_user.py::test_create_user

User: Fix those test failures

Claude: [Delegates to debugger, analyzes and fixes tests]

Output:
Fixed 3 test failures:
- test_jwt_validation: Fixed assertion logic
- test_token_expiry: Added missing 'exp' key handling
- test_create_user: Corrected email validation

User: /git prepare

Output:
Validation: PASSED
1 group ready (fix commits)

User: /git commit

Output:
1 commit created: fix(tests): resolve CI test failures

User: git push

User: Monitor CI

Claude: [Watches CI run]

Output:
CI Status: PASSED
All checks successful!
```

---

## Example 4: Validation Failure Recovery

Handling validation failures during prepare.

```bash
User: /git prepare

Output:
Validation FAILED

Linting Issues:
- packages/core/auth.py:145 - line too long (92 > 88)

Test Failures:
- tests/test_auth.py::test_jwt_validation - AssertionError

# Orchestrator auto-delegates to debugger (attempt 1 of 3)
Claude: [Debugger fixes issues, re-runs validation]

Output:
Auto-fix attempt 1: PASSED
- Fixed line length issue
- Fixed test assertion

Continuing to Phase 2...

# Workflow continues normally
```

---

## Example 5: Partial Quality Gate Pass

Handling blocked groups with approved groups.

```bash
User: /git prepare

Output:
Quality Gates: PARTIAL (2 blocked, 5 approved)

Group 1: feat(auth) - JWT authentication [BLOCKED]
  Blocking Issues:
  - Security: Hard-coded secret key (CRITICAL)

Group 2: refactor(api) - Standardize endpoints [APPROVED]
Group 3: feat(user) - User profile [BLOCKED]
  Blocking Issues:
  - Testing: No tests for new endpoint
Group 4-7: [APPROVED]

User: /git commit --groups=2,4,5,6,7

Output:
5 commits created successfully
(Groups 1, 3 skipped - blocked)

# User fixes blocked groups
User: [Removes hard-coded secret, adds tests]

User: /git prepare
# Only the previously blocked files are re-analyzed

User: /git commit
# Commits the now-approved groups
```
