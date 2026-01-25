# Invocation Examples

Practical examples of skill invocations across different scenarios.

---

## Table of Contents

1. [Simple Invocations](#simple-invocations)
2. [Structured Invocations](#structured-invocations)
3. [Chained Invocations](#chained-invocations)
4. [Error Recovery Examples](#error-recovery-examples)

---

## Simple Invocations

### Code Review

**User Request**:
```
Review this Python function for issues:

def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)
```

**Skill Activated**: `code-quality`

**Response**:
```markdown
## Review Report: get_user function

**Status**: FAIL

### Critical Issues

1. **SQL Injection Vulnerability**
   - **Confidence**: 0.98
   - **Line**: 2
   - **Problem**: Direct string interpolation in SQL query
   
   **Current code**:
   ```python
   query = f"SELECT * FROM users WHERE id = {user_id}"
   ```
   
   **Required fix**:
   ```python
   query = "SELECT * FROM users WHERE id = %s"
   return db.execute(query, (user_id,))
   ```

**Recommendation**: REQUEST CHANGES - Critical security fix required
```

---

### Debugging

**User Request**:
```
Debug why this test is failing intermittently:
test_async_handler sometimes passes, sometimes fails with timeout
```

**Skill Activated**: `debugging-methodology`

**Response**:
```markdown
## Debug Report: test_async_handler

### Hypothesis
Race condition in async task scheduling

### Evidence
1. Failure rate: ~30% (non-deterministic)
2. Occurs more on slower CI machines
3. Timeout suggests resource contention

### Root Cause Analysis (5 Whys)
1. Why timeout? -> Async task not completing
2. Why not completing? -> Awaiting lock held by another task
3. Why lock held? -> Tasks sharing mutable state
4. Why sharing state? -> Global variable used
5. Why global? -> Design oversight

### Recommendation
- Add asyncio.Lock around shared state access
- Isolate test fixtures to prevent state bleeding
```

---

## Structured Invocations

### Full Context Request

**User Request**:
```markdown
## Skill Request: code-quality

### Context
- **Files**: packages/core/auth/handler.py
- **Objective**: Pre-merge security review
- **Constraints**: Must pass before release v2.1

### Input
[contents of handler.py]

### Expected Output
Security-focused review with severity ratings
```

**Response**:
```json
{
  "skill": "code-quality",
  "status": "SUCCESS",
  "confidence": 0.94,
  "findings": [
    {
      "severity": "HIGH",
      "type": "security",
      "issue": "JWT token not validated for expiry",
      "line": 45,
      "fix": "Add exp claim validation"
    },
    {
      "severity": "MEDIUM",
      "type": "security",
      "issue": "Missing rate limiting on auth endpoint",
      "line": 12,
      "fix": "Add rate limiter decorator"
    }
  ],
  "recommendation": "APPROVE_WITH_CHANGES",
  "blocking_issues": 1
}
```

---

### Multi-File Analysis

**User Request**:
```markdown
## Skill Request: codebase-research

### Context
- **Scope**: packages/core/
- **Objective**: Understand authentication flow
- **Constraints**: Focus on OAuth integration

### Questions
1. Where is OAuth configured?
2. How are tokens refreshed?
3. What happens on auth failure?
```

**Response**:
```markdown
## Research Report: Authentication Flow

### OAuth Configuration
- **Location**: `packages/core/auth/oauth.py`
- **Provider**: Auth0
- **Scopes**: read:users, write:users, admin

### Token Refresh Flow
```
1. Client -> /auth/refresh (POST)
2. Handler validates refresh_token
3. If valid: Issue new access_token (15min TTL)
4. If invalid: Return 401, redirect to /login
```

### Auth Failure Handling
- **401**: Token expired -> Client refreshes
- **403**: Insufficient scope -> Redirect to permission request
- **429**: Rate limited -> Exponential backoff

### Key Files
| File | Purpose |
|------|---------|
| `oauth.py` | OAuth provider configuration |
| `middleware.py` | Request authentication |
| `refresh.py` | Token refresh logic |
```

---

## Chained Invocations

### Code Review Pipeline

**Workflow**:
```
1. codebase-research -> Gather context
2. code-quality -> Analyze code
3. code-review-standards -> Validate compliance
```

**Step 1 Output** (codebase-research):
```json
{
  "context": {
    "module": "auth",
    "related_files": ["handler.py", "middleware.py"],
    "patterns_used": ["decorator-based auth", "JWT tokens"]
  }
}
```

**Step 2 Input** (code-quality):
```markdown
## Context from codebase-research
Module: auth
Patterns: decorator-based auth, JWT tokens

## Files to Review
- handler.py
- middleware.py
```

**Step 2 Output**:
```json
{
  "issues": [
    {"file": "handler.py", "severity": "HIGH", "issue": "..."},
    {"file": "middleware.py", "severity": "LOW", "issue": "..."}
  ]
}
```

**Step 3 Input** (code-review-standards):
```markdown
## Review Results
- 1 HIGH severity issue
- 1 LOW severity issue

## Validate Against
- Project security standards
- Python style guide
```

**Final Output**:
```markdown
## Pipeline Complete

### Summary
- Files analyzed: 2
- Issues found: 2 (1 blocking)
- Compliance: 85%

### Blocking Issues
1. handler.py: JWT expiry not validated

### Recommendations
1. Fix JWT validation before merge
2. Add missing docstrings (non-blocking)

### Decision
BLOCK MERGE until HIGH severity resolved
```

---

## Error Recovery Examples

### Missing Input Recovery

**User Request**:
```
Review this code
```

**Skill Response**:
```json
{
  "skill": "code-quality",
  "status": "FAILURE",
  "error": {
    "code": "INPUT_MISSING",
    "message": "No code provided for review",
    "recovery": "Please provide code block or file path"
  },
  "prompt": "Share the code you want reviewed, either as:\n- Code block in message\n- File path: `packages/module/file.py`"
}
```

---

### Partial Success Recovery

**User Request**:
```
Review all Python files in packages/core/
```

**Skill Response** (5 files, 2 failed):
```markdown
## Partial Result: code-quality

**Status**: PARTIAL (3/5 files)
**Confidence**: 0.87

### Completed Analysis
| File | Status | Issues |
|------|--------|--------|
| auth.py | OK | 0 |
| handler.py | WARN | 2 |
| utils.py | OK | 0 |

### Failed Files
| File | Error | Recovery |
|------|-------|----------|
| legacy.py | Syntax error line 42 | Fix syntax, retry |
| binary.pyc | Not source code | Skip (expected) |

### Actionable Findings
1. handler.py:23 - Unused import
2. handler.py:45 - Missing type hint

### Next Steps
1. Fix legacy.py syntax error
2. Re-run: "Review packages/core/legacy.py"
```

---

### Timeout Recovery

**User Request**:
```
Analyze entire codebase for security issues
```

**Skill Response** (timeout after 60s):
```json
{
  "skill": "code-quality",
  "status": "TIMEOUT",
  "partial_results": {
    "files_analyzed": 45,
    "files_remaining": 128,
    "issues_found": 12
  },
  "recovery": {
    "strategy": "chunk",
    "suggestion": "Analyze one package at a time",
    "commands": [
      "Review packages/core/ for security",
      "Review packages/api/ for security",
      "Review packages/utils/ for security"
    ]
  }
}
```

---

## Integration Patterns

### Agent Delegating to Skill

```python
# In agent workflow
"""
Step 3: Code Quality Check

Invoke code-quality skill with:
- Files: {changed_files}
- Focus: Security + Performance
- Threshold: No HIGH severity issues

If skill returns FAILURE or HIGH issues:
  -> Block workflow, report to user
Else:
  -> Continue to Step 4
"""
```

### Skill Composition in Slash Command

```markdown
# /review command

1. Run `codebase-research` to understand context
2. Run `code-quality` on changed files
3. Run `code-review-standards` for compliance
4. Aggregate results into unified report
```

---

## See Also

- [Error Handling Patterns](error-handling.md)
- [SKILL.md](../SKILL.md) - Main skill documentation
