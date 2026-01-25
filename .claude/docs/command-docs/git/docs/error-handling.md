# Error Handling & Recovery

Complete error recovery patterns for the `/git` command workflow.

---

## A. Validation Failures (Phase 1)

**Scenario:** Linting errors, formatting issues, test failures detected

**Orchestrator Action:** Stop workflow, report failures with details

**Example Output:**
```text
Validation FAILED

Linting Issues:
- tests/test_auth.py:23 - unused import 'os'
- packages/core/auth.py:145 - line too long (92 > 88 characters)

Test Failures:
- tests/test_auth.py::test_jwt_validation - AssertionError: Expected valid=True
- tests/test_user.py::test_create_user - ValidationError: email format invalid

Workflow STOPPED. Cannot proceed to file grouping until validation passes.
```

### Recovery Options

1. **Auto-Fix + Retry (Automated - RECOMMENDED):**
   - Orchestrator automatically delegates test failures to `[debugger]` agent
   - Debugger fixes issues, re-runs validation (validate_pre_commit)
   - Iterates until PASS (max 3 attempts)
   - If PASS after fixes: Continue to Phase 2 automatically
   - If FAIL after 3 attempts: Escalate to user (option 2)

2. **Manual Fix + Retry:**
   ```bash
   # Fix issues manually
   # Then re-run validation
   /git prepare
   ```

3. **Delegate to Debugger (for persistent failures):**
   - User explicitly requests: "Fix those test failures"
   - Claude delegates to `[debugger]` agent
   - After fixes, re-run `/git prepare`

4. **Skip Validation (NOT RECOMMENDED - HIGH RISK):**
   ```bash
   /git prepare --skip-validation
   ```
   - **Risk:** May commit code with test failures, linting issues
   - **Use only for:** Emergency commits, experimental branches

**When to Use Each Option:**
- **Auto-fix:** Default (orchestrator handles automatically)
- **Manual fix:** Simple issues you can fix faster manually
- **Debugger:** Complex test failures needing hypothesis-driven debugging
- **Skip validation:** ONLY for emergency commits (accept risk)

---

## B. File Grouping Failures (Phase 2)

**Scenario:** Git status fails, FileGrouper logic errors, repository issues

**Orchestrator Action:** Stop workflow, report error details

**Example Output:**
```text
File Grouping FAILED

Error: git status command failed
Details: fatal: not a git repository (or any of the parent directories): .git

Workflow STOPPED. Cannot proceed to quality gates.
```

### Recovery Options

1. **Check Git Repository Status:**
   ```bash
   git status
   # If not a git repo: git init
   # If corrupted: investigate .git directory
   ```

2. **Manual Git Commands (Fallback):**
   ```bash
   # If FileGrouper fails, use manual git workflow:
   git add file1.py file2.py
   git commit -m "feat(module): description"
   ```

3. **Report Bug (if FileGrouper logic error):**
   - If error indicates FileGrouper bug (e.g., "KeyError: 'change_type'")
   - Report issue with full error details
   - Use manual git commands as workaround

**Common Causes:**
- Not in a git repository (fatal: not a git repository)
- Git command not available (git: command not found)
- FileGrouper internal error (rare - indicates bug)

---

## C. Quality Gate Failures (Phase 3)

**Scenario:** Blocking code review issues, critical tech debt, security vulnerabilities

**Orchestrator Action:** Mark affected groups as BLOCKED, continue to Phase 4 with partial results

**Example Output:**
```text
Quality Gates: PARTIAL PASS (3 groups blocked, 4 groups approved)

Group 1: feat(auth) - JWT authentication [BLOCKED]
  Quality: CHANGES_REQUIRED
    Blocking Issues:
    - Security: Hard-coded secret key in auth.py:45 (CRITICAL)
    - Correctness: Missing null check in login handler (HIGH)
  Tech Debt: INTRODUCED (debt_delta: +12)
  Files: 5 files

Group 2: refactor(api) - Standardize endpoints [APPROVED]
  Quality: APPROVED
  Tech Debt: REDUCED (debt_delta: -8)
  Files: 8 files

Summary:
- 4 groups approved (ready to commit)
- 3 groups blocked (must fix before commit)
- Blocking issues: 2 CRITICAL, 1 HIGH, 1 MEDIUM

Next Steps:
- To commit approved groups only: /git commit --groups=2,4,5,6,7
- To fix blocked groups: Address issues, re-run /git prepare
```

### Recovery Options

1. **Iterative Fix Loop (RECOMMENDED):**
   ```text
   Fix blocking issues manually -> Re-run /git prepare
   -> Workflow re-analyzes and re-reviews all files
   -> If PASS: All groups approved, proceed to commit
   -> If still FAIL: Repeat until resolved
   ```

2. **Partial Commit Strategy:**
   ```bash
   # Commit approved groups only
   /git commit --groups=2,4,5,6,7
   
   # Fix blocked groups separately
   # ... make fixes ...
   
   # Re-run prepare for remaining files
   /git prepare
   
   # Commit fixed groups
   /git commit
   ```

3. **Skip Quality Gates (HIGH RISK):**
   ```bash
   /git prepare --skip-quality
   ```
   - **Risk:** May commit security vulnerabilities, critical issues
   - **Use only for:** Experimental branches, quick prototyping (NOT production)

**When to Use Each Option:**
- **Iterative fix:** Best practice (fix all issues before any commit)
- **Partial commit:** When approved groups are independent of blocked groups
- **Skip quality:** ONLY for non-critical branches (never main/production)

---

## D. Commit Execution Failures (Phase 5)

**Scenario:** Git errors, merge conflicts, file not staged, commit hook failures

**Orchestrator Action:** Report failure, suggest recovery steps

**Example Output:**
```text
Commit Execution FAILED

Group 2 of 7 failed:
Group: refactor(api) - Standardize endpoints

Error: git commit failed
Details: error: Your local changes to the following files would be overwritten by merge:
  packages/api/routes.py
Please commit your changes or stash them before you merge.

Successful commits before failure:
1. feat(agents): core agent schema & standards (abc123)

Failed at group 2. Remaining groups not attempted.
```

### Recovery Options

1. **Resolve Conflicts + Retry:**
   ```bash
   # Check conflict status
   git status
   
   # Resolve conflicts manually
   # Edit conflicting files
   
   # Re-run commit (continues from where it failed)
   /git commit
   ```

2. **Manual Git Commands (Fallback):**
   ```bash
   # If automated commit consistently fails:
   git add packages/api/routes.py
   git commit -m "refactor(api): standardize endpoints"
   
   # Continue with remaining groups manually or via /git commit
   ```

3. **Reset and Start Over:**
   ```bash
   # If commit state is corrupted:
   git reset --soft HEAD~1  # Undo last commit (if any)
   git status               # Verify state
   
   /git prepare             # Re-analyze from clean state
   /git commit
   ```

4. **Skip Failed Group:**
   ```bash
   # Commit remaining groups without failed group
   /git commit --groups=1,3,4,5,6,7
   
   # Fix failed group separately
   ```

**Common Causes:**
- **Merge conflicts:** Another commit modified same files
- **File not found:** File deleted between prepare and commit
- **Commit hook failure:** Pre-commit hook rejected commit
- **Permission issues:** No write access to repository

---

## Error Recovery Patterns

### Pattern 1: Iterative Fix Loop (Most Common)

**Use For:** Validation failures, quality gate failures

**Workflow:**
```text
/git prepare
|
FAIL (validation or quality gates)
|
Fix issues manually OR delegate to debugger
|
/git prepare (re-run full workflow)
|
PASS -> Continue to commit
```

### Pattern 2: Partial Commit Strategy

**Use For:** Quality gate failures with independent approved groups

**Workflow:**
```text
/git prepare
|
SOME BLOCKED (approved groups available)
|
/git commit --groups=<approved>
|
Fix blocked groups
|
/git prepare (only blocked groups re-analyzed)
|
/git commit
```

### Pattern 3: Manual Fallback

**Use For:** FileGrouper failures, persistent commit failures

**Workflow:**
```text
/git prepare
|
FAIL (grouping or commit execution)
|
Manual git commands (traditional workflow)
|
git add <files>
git commit -m "message"
git push
```

### Pattern 4: Escalation Path

**When to Report Bugs vs User Errors:**

**User Errors (Fix Yourself):**
- Validation failures (linting, tests) -> Fix code
- Quality gate failures (code review issues) -> Improve code
- Not in git repository -> Run `git init`
- Merge conflicts -> Resolve conflicts

**FileGrouper Bugs (Report to Maintainers):**
- FileGrouper crashes with stack trace
- FileGrouper produces invalid commit groups (e.g., mixed change types)
- FileGrouper confidence calculation errors

**Git-GitHub Agent Bugs (Report to Maintainers):**
- `analyze_changes` operation fails with internal error
- `execute_commits` operation creates malformed commits
- Agent returns invalid JSON schema

**How to Report:**
1. Capture full error message and stack trace
2. Provide git status output
3. Provide list of modified files
4. Include reproduction steps
