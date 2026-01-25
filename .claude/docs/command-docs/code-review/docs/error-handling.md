# Error Handling for /code-review Command

Complete error scenarios, recovery strategies, and checkpoint-based resume.

---

## Checkpoint Recovery System

### Checkpoint Structure

```json
{
  "command": "code-review",
  "session_id": "uuid-here",
  "last_completed_phase": 2,
  "timestamp": "2025-01-15T10:30:00Z",
  "state": {
    "files": [],
    "batches": [],
    "tools_available": {}
  }
}
```

**Location**: `temp/code-review/{session_id}/checkpoint.json`

### Resume from Failed Phase

**Detection**:
```
On /code-review start:
  1. Check for existing checkpoint in temp/code-review/
  2. If found AND < 24h old:
     - Display: "Found incomplete review from {timestamp}"
     - Prompt: "Resume from Phase {N}? [Y/n]"
  3. If user confirms: Load state, start at Phase {N+1}
  4. If user declines: Delete checkpoint, start fresh
```


### Stale Checkpoint Handling

**Threshold**: 24 hours

```
If checkpoint.timestamp > 24h old:
  - Display: "Stale checkpoint found (from {timestamp})"
  - Display: "Context may have changed. Starting fresh review."
  - Action: Delete stale checkpoint, start from Phase 0
```

---

## Empty Input Set

**Scenario**: No files to review after filtering.

**Output**:
```
WARNING: No files to review

Source: /code-review --all
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

**Scenario**: Invalid source flag or multiple flags.


**Output**:
```
ERROR: Invalid command usage

Error: Multiple source flags provided (--all and --branch)

Correct Usage:
/code-review <source> [options]

Source (choose ONE):
- --files <file1> <file2> ...
- --branch <branch-name>
- --commit <commit-hash>
- --all

Examples:
/code-review --all
/code-review --branch feature-auth --focus=security
/code-review --files src/auth.py tests/test_auth.py
```

---

## Phase-Specific Failures

### Phase 0: Tool Check Failure

**Git Missing (BLOCKING)**:
```
ERROR: Git not found in PATH.
Cannot discover files for review.
Please install git: https://git-scm.com/downloads

Checkpoint: None (Phase 0 blocks without checkpoint)
Recovery: Install git, re-run command
```

**Semgrep Check Delegation Failure**:
```
WARNING: Could not verify semgrep availability

Agent git-github failed to check semgrep.
Assuming unavailable - security scan will be skipped.

Continuing with reduced agent set...
```


### Phase 1: File Discovery Failure

```
ERROR: File discovery failed

Agent: git-github
Error: Git repository not found in current directory

Recovery:
1. Verify you are in a git repository: `git status`
2. If in submodule, navigate to parent
3. Re-run: /code-review {args}

Checkpoint: Phase 0 complete, resume from Phase 1
```

### Phase 3: Agent Failure

```
WARNING: Partial Review Complete

Review Status: PARTIAL SUCCESS (2 of 3 agents succeeded)

Successful Agents:
- python-code-reviewer: 12 findings
- tech-debt-investigator: Debt score 34

Failed Agents:
- sast-scanner: Task timeout
  - Error: "Agent did not respond within 60s"
  - Recovery: Re-run with --retry-failed flag

Partial Results:
- Review continues with available findings
- Security scan incomplete
- Recommendations based on 2 of 3 agents

Checkpoint: Phase 3 partial, can resume sast-scanner only
```


### Phase 4: Research Failure

```
WARNING: Investigation partially complete

researcher-external: 4/6 calls succeeded (1 API error)

Fallback Applied:
- Findings researched via library only
- Confidence capped at 0.85 (no web validation)

Affected Findings:
- HIGH-003: Confidence 0.82 (would be 0.90 with web research)

Checkpoint: Phase 4 complete with degraded confidence
```

---

## Investigation API Failures

### Retry Logic

```
researcher-external failure:
  - Retry: 3 attempts (delays: 1s, 2s, 4s)
  - Fallback: Use agent confidence only (cap 0.50)
```

### Error Recovery Matrix

| Error | Recovery Strategy | Confidence Impact |
|-------|------------------|-------------------|
| researcher-external timeout | Retry with backoff | -0.05 |
| Library not found | Skip library research | -0.10 |
| researcher-external exhausted | Cap confidence at 0.75 | -0.15 |
| Both agents failed | Cap confidence at 0.50 | -0.25 |
| Network connectivity loss | Mark for manual review | -0.30 |


### Graceful Degradation

```json
{
  "status": "PARTIAL_SUCCESS",
  "confidence_boost": 0.08,
  "investigation_trail": [
    "researcher-external: SUCCESS - Validated against SQLAlchemy docs",
    "researcher-external: FAILED after 2 retries (API timeout)",
    "Final confidence: 0.78 (library only, capped)"
  ],
  "fallback_used": true,
  "manual_validation_recommended": true
}
```

---

## Branch/Commit Not Found

**Invalid Branch**:
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
- Use remote: `git fetch && git checkout origin/feature-xyz`
```

**Invalid Commit**:
```
ERROR: Commit not found

Commit: abc123xyz
Error: Commit 'abc123xyz' not found in repository

Suggestions:
- Check commit hash: `git log --oneline -20`
- Ensure commit exists locally (may need `git fetch`)
- Use full commit hash if abbreviated is ambiguous
```

---

## Cleanup on Success

On successful Phase 6 completion:
1. Delete checkpoint file
2. Preserve report in `temp/code-review/{session_id}/report.md`
3. Log session summary to `temp/code-review/history.log`

On failure:
1. Preserve checkpoint for resume
2. Log failure details
3. Display resume instructions
