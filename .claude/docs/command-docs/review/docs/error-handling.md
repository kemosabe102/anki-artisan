# Error Handling for /review Command

Complete error scenarios and recovery strategies.

---

## Empty Input Set

**Scenario**: No files to review after filtering.

**Output**:
```
WARNING: No files to review

Source: /review --all
Discovered: 0 files after filtering

Possible Causes:
- No uncommitted changes in repository
- All changes are in excluded directories (.claude/, docs/)
- All files are binary or generated

Suggestions:
- Run `git status` to verify repository state
- Check if changes are staged but not committed
- Use `--files` to specify files explicitly
```

---

## Invalid Input

**Scenario**: User provides invalid source flag or multiple flags.

**Output**:
```
ERROR: Invalid command usage

Error: Multiple source flags provided (--all and --branch)

Correct Usage:
/review <source> [options]

Source (choose ONE):
- --files <file1> <file2> ...
- --branch <branch-name>
- --commit <commit-hash>
- --all

Examples:
/review --all
/review --branch feature-auth --focus=security
/review --files src/auth.py tests/test_auth.py
```

---

## Permission Issues

**Scenario**: Cannot access git repository or write output.

**Output**:
```
ERROR: Permission Error

Error: Cannot access git repository

Diagnostics:
- Current directory: /home/user/project
- Git repository: Not detected
- Permissions: Read-only

Recovery Steps:
1. Verify you are in a git repository: `git status`
2. Check file permissions: `ls -la .git`
3. Ensure you have read access to git repository
4. If in submodule, navigate to parent repository
```

---

## Partial Agent Failures

**Scenario**: Some agents fail, others succeed.

**Output**:
```
WARNING: Partial Review Complete

Review Status: PARTIAL SUCCESS (2 of 3 agents succeeded)

Successful Agents:
- code-quality: 12 findings
- tech-debt-investigator: Debt score 0.73

Failed Agents:
- sast-scanner: Tool execution failed
  - Error: "Bandit not installed"
  - Recovery: `pip install bandit`
  - Re-run: `/review --all` after installation

Partial Results:
- Review continues with available findings
- Security scan incomplete (install Bandit for full coverage)
- Recommendations based on 2 of 3 agents

Next Steps:
1. Review partial findings above
2. Install missing tools (Bandit)
3. Re-run full review: `/review --all`
```


---

## Investigation API Failures

**Scenario**: Context7 or Perplexity APIs fail during confidence investigation.

### Retry Logic (Exponential Backoff)

1. **Context7 failure**: Retry max 3 times (delays: 1s, 2s, 4s)
2. **Perplexity failure**: Retry max 2 times (delays: 2s, 4s)
3. **Both failed**: Degrade gracefully

### Error Recovery Matrix

| Error | Recovery Strategy | Confidence Impact | User Notification |
|-------|------------------|-------------------|-------------------|
| Context7 rate limit | Wait + retry -> Fallback to Perplexity | -0.05 | "Context7 temporarily unavailable, using Perplexity" |
| Context7 library not found | Skip Context7 -> Perplexity only | -0.10 | "No official docs found for [library], using community sources" |
| Perplexity timeout | Mark finding as MEDIUM confidence | -0.15 | "Deep research incomplete, recommendation based on agent analysis" |
| Both APIs offline | Degrade to agent confidence only | -0.25 (cap at 0.50) | "External research unavailable, findings require manual validation" |
| Network connectivity loss | Retry once -> Fail gracefully | -0.30 (cap at 0.45) | "Cannot reach research APIs, review incomplete" |

### Graceful Degradation Example

```json
{
  "status": "PARTIAL_SUCCESS",
  "confidence_boost": 0.08,
  "investigation_trail": [
    "Context7: FAILED after 3 retries (rate limit exceeded)",
    "Perplexity: SUCCESS - Validated against OWASP A01 documentation",
    "Final confidence: 0.78 (initial 0.70 + Perplexity boost 0.08)"
  ],
  "fallback_used": true,
  "manual_validation_recommended": false
}
```

**No Infinite Retries**: Max 5 total API calls (3 Context7 + 2 Perplexity). After limit, mark finding confidence and proceed.

---

## Language Not Supported

**Scenario**: Files in language without available reviewer.

**Output**:
```
WARNING: Language Gap Detected

Unsupported Languages:
- Java: 3 files (src/api/*.java)
- TypeScript: 2 files (src/ui/*.ts)

Available Reviewers:
- Python: code-quality (confidence: 0.95)

Actions Taken:
- Python files: Full review completed
- Java/TypeScript: SKIPPED (no reviewer available)

Recommendations:
- Create java-code-reviewer agent (Priority: P1)
- Create typescript-code-reviewer agent (Priority: P1)
- Use `/create-agent` command to add language support
```

---

## Branch/Commit Not Found

**Scenario**: User specifies non-existent branch or commit.

**Output for Invalid Branch**:
```
ERROR: Branch not found

Branch: feature-xyz
Error: Branch 'feature-xyz' does not exist

Available Branches:
- main
- feature-auth
- feature-api

Suggestions:
- Check branch name spelling
- List all branches: `git branch -a`
- Use remote branch: `git fetch && git checkout origin/feature-xyz`
```

**Output for Invalid Commit**:
```
ERROR: Commit not found

Commit: abc123xyz
Error: Commit 'abc123xyz' not found in repository

Suggestions:
- Check commit hash: `git log --oneline -20`
- Ensure commit exists locally (may need `git fetch`)
- Use full commit hash if abbreviated hash is ambiguous
```
