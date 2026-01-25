# Usage Examples for /code-review Command

Complete workflow examples with expected output.

---

## Example 1: Basic Review (Uncommitted Changes)

```bash
/code-review --all
```

**Scenario**: Developer has modified 5 Python files, wants quality check before commit.

**Phase-by-Phase Execution**:

**Phase 0 - Pre-Flight**:
```
[PRE-FLIGHT] Checking tool availability...
  git: OK (version 2.43.0)
  semgrep: OK (version 1.56.0)
Tools available: [git, semgrep]
Warnings: []
```

**Phase 1 - File Discovery**:
```
[DISCOVER] git status --porcelain
  packages/core/loader.py (modified)
  packages/api/handlers.py (modified)
  packages/core/cache.py (modified)
  packages/auth/manager.py (modified)
  tests/test_loader.py (modified)
Files: 5 (5 Python)
```

**Phase 2 - Agent Routing**:
```
[ROUTE] Grouping files by language...
  Batch 1: 5 Python files -> python-code-reviewer
[ROUTE] Core agents: python-code-reviewer, tech-debt-investigator, sast-scanner
```

**Phase 3 - Multi-Agent Review**:
```
[REVIEW] Launching 3 agents in parallel...
  python-code-reviewer: 4 findings (1 High, 2 Medium, 1 Low)
  tech-debt-investigator: debt_score=34, TDR=0.15
  sast-scanner: 1 finding (Medium - hardcoded timeout)
Raw findings: 5
```

**Phase 4 - Confidence Investigation**:
```
[INVESTIGATE] 2 findings below 0.75 confidence threshold
  [MED-002] Confidence 0.72 -> Context7 (asyncio docs) -> 0.85
  [LOW-001] Confidence 0.68 -> Context7 (typing docs) -> 0.81
Research calls: Context7=2, Perplexity=0
```

**Phase 5 - Consolidation**:
```
[CONSOLIDATE] Deduplication check...
  1 duplicate removed (same issue from 2 agents)
Unique findings: 4
```

**Phase 6 - Report**:
```
Code Review Report
==================
Status: APPROVED_WITH_CONDITIONS

Summary:
- Files: 5 (5 Python)
- Findings: 4 (High: 1, Medium: 2, Low: 1)
- Investigation: 2 findings researched (Context7: 2)

HIGH (should fix):
[HIGH-001] Async function not awaited (packages/core/loader.py:67)
  Confidence: 0.88 | Agent: python-code-reviewer
  Fix: data = await fetch_data()
  Verify: rg -n 'fetch_data\(' packages/core/ | grep -v 'await'

MEDIUM (consider):
[MED-001] Missing input validation (packages/api/handlers.py:23)
  Confidence: 0.85 | Agent: python-code-reviewer
  Fix: Add Pydantic model validation
  Verify: pytest tests/api/test_handlers.py

[MED-002] Hardcoded timeout value (packages/core/cache.py:45)
  Confidence: 0.85 | Agent: sast-scanner
  Fix: CACHE_TIMEOUT_SECONDS = int(os.getenv("CACHE_TIMEOUT", 300))
  Verify: rg -n 'timeout\s*=' packages/core/

LOW (optional):
[LOW-001] Missing type hints (packages/auth/manager.py:12)
  Confidence: 0.81 | Agent: python-code-reviewer
  Fix: def authenticate(user: User, password: str) -> AuthResult:

Next Steps:
- Fix HIGH issue before commit
- Re-run: /code-review --all
```

---

## Example 2: Security-Focused Review

```bash
/code-review --all --focus=security
```

**Scenario**: Pre-commit security scan for authentication module changes.

**Phase-by-Phase Execution**:

**Phase 0 - Pre-Flight**:
```
[PRE-FLIGHT] Tools: git OK, semgrep OK
Focus mode: SECURITY (sast-scanner priority weighted)
```

**Phase 1 - File Discovery**:
```
[DISCOVER] git status --porcelain
  packages/auth/queries.py (modified)
  packages/auth/tokens.py (modified)
  packages/api/middleware.py (modified)
Files: 3 (3 Python)
```

**Phase 3 - Multi-Agent Review** (sast-scanner prioritized):
```
[REVIEW] Security focus: sast-scanner runs first with priority weighting
  sast-scanner: 2 Critical (SQL injection, hardcoded secret)
  python-code-reviewer: 1 High (input not sanitized)
  tech-debt-investigator: debt_score=28, TDR=0.12
Raw findings: 3
```

**Phase 4 - Confidence Investigation**:
```
[INVESTIGATE] Critical findings ALWAYS investigated (regardless of confidence)
  [CRIT-001] SQL Injection (0.88)
    -> Context7 (SQLAlchemy parameterized queries) -> 0.92
    -> Perplexity (OWASP A03:2021 Injection) -> 0.94
  [CRIT-002] Hardcoded API Key (0.95)
    -> Context7 (python-dotenv secrets management) -> 0.96
    -> Perplexity (OWASP A07:2021 secrets) -> 0.97
Research calls: Context7=2, Perplexity=2
```

**Phase 6 - Report**:
```
Code Review Report
==================
Status: CHANGES_REQUIRED

Summary:
- Files: 3 (3 Python)
- Findings: 3 (Critical: 2, High: 1)
- Focus: SECURITY
- Investigation: 2 Critical findings researched (Context7: 2, Perplexity: 2)

CRITICAL (must fix):
[CRIT-001] SQL Injection Vulnerability (packages/auth/queries.py:42)
  Confidence: 0.94 | Verified: Context7 + OWASP A03:2021
  Problem: Raw SQL with f-string interpolation
  Code: f"SELECT * FROM users WHERE id = {user_id}"
  Fix: Use parameterized queries
  ```python
  result = db.execute(
      text("SELECT * FROM users WHERE id = :user_id"),
      {"user_id": user_id}
  )
  ```
  Verify: rg -n 'f"SELECT.*{' packages/auth/

[CRIT-002] Hardcoded API Key (packages/auth/tokens.py:15)
  Confidence: 0.97 | Verified: Context7 + OWASP A07:2021
  Problem: API key committed to source control
  Code: API_KEY = "sk-prod-abc123..."
  Fix: Move to environment variable
  ```python
  API_KEY = os.environ["API_KEY"]  # Set via .env or secrets manager
  ```
  Verify: rg -n 'api_key\s*=' packages/auth/ --ignore-case

Security Summary:
- OWASP A03 (Injection): 1 finding
- OWASP A07 (Secrets): 1 finding
- Secrets detected: 1 hardcoded key

Action Required: CRITICAL issues must be fixed before merge.
```

---

## Example 3: Branch Comparison

```bash
/code-review --branch feature/new-api
```

**Scenario**: Technical lead reviews feature branch before merge to main.

**Phase-by-Phase Execution**:

**Phase 1 - File Discovery**:
```
[DISCOVER] git diff --name-only main...feature/new-api
  packages/api/routes.py (added)
  packages/api/models.py (added)
  packages/api/handlers.py (modified)
  packages/core/service.py (modified)
  packages/core/cache.py (modified)
  packages/auth/middleware.py (modified)
  tests/api/test_routes.py (added)
  tests/api/test_handlers.py (modified)
  docs/api-reference.md (added)
Files: 9 (8 Python, 1 Markdown)
Commits: 12 commits ahead of main
```

**Phase 2 - Agent Routing**:
```
[ROUTE] Grouping files by language...
  Batch 1: packages/api/*.py (3 files) -> python-code-reviewer
  Batch 2: packages/core/*.py, packages/auth/*.py (3 files) -> python-code-reviewer
  Batch 3: tests/**/*.py (2 files) -> python-code-reviewer
[ROUTE] Markdown files: 1 (skipped - no reviewer)
[ROUTE] Total batches: 3 (max 5 files per batch)
```

**Phase 3 - Multi-Agent Review**:
```
[REVIEW] 3 batches x 3 core agents = 9 agent calls (parallel)
  Batch 1: 3 findings (1 High, 2 Medium)
  Batch 2: 2 findings (2 Medium)
  Batch 3: 1 finding (1 Low - missing test coverage)
  tech-debt-investigator (all files): debt_score=41, TDR=0.18
  sast-scanner (all files): 1 finding (Medium)
Raw findings: 7
```

**Phase 5 - Consolidation**:
```
[CONSOLIDATE] Synthesis triggered (3 overlapping findings > 0.7 similarity)
  Synthesized: 3 API validation findings -> 1 consolidated recommendation
Unique findings: 5
```

**Phase 6 - Report**:
```
Code Review Report
==================
Status: APPROVED_WITH_CONDITIONS

Summary:
- Files: 9 (8 Python, 1 Markdown)
- Findings: 5 (High: 1, Medium: 3, Low: 1)
- Comparison: feature/new-api (12 commits) vs main
- Duration: 2m 34s

Language Coverage:
- Python: REVIEWED (python-code-reviewer)
- Markdown: SKIPPED (no reviewer available)

HIGH (should fix):
[HIGH-001] Missing error handling in API route (packages/api/routes.py:45)
  Confidence: 0.87 | Agent: python-code-reviewer
  Fix: Add try/except with proper HTTP error responses
  Verify: pytest tests/api/test_routes.py -k "test_error"

MEDIUM (consider):
[MED-001] API Validation (SYNTHESIZED from 3 findings)
  Confidence: 0.85 | Agents: python-code-reviewer (x3)
  Locations: routes.py:23, handlers.py:45, models.py:12
  Fix: Implement consistent Pydantic validation across all endpoints
  Verify: rg -n 'def.*request' packages/api/ | head -20

Next Steps:
- Address HIGH issue before merge
- Consider MEDIUM recommendations
- Re-run after fixes: /code-review --branch feature/new-api
```

---

## Example 4: Resume from Checkpoint (Phase 4 Failure Recovery)

**Scenario**: Review failed during Phase 4 (Confidence Investigation) due to Context7 rate limit. User wants to resume without re-running earlier phases.

**Initial Run (Failed)**:
```bash
/code-review --all --mode=comprehensive
```

**Failure Output**:
```
Code Review - INTERRUPTED
=========================
Status: CHECKPOINT_SAVED

Progress:
- Phase 0: COMPLETE (pre-flight passed)
- Phase 1: COMPLETE (8 files discovered)
- Phase 2: COMPLETE (2 batches routed)
- Phase 3: COMPLETE (6 raw findings)
- Phase 4: FAILED at finding 3/6
  Error: Context7 rate limit exceeded (429)
  Checkpoint: .claude/temp/code-review/checkpoint-2024-01-15-1423.json

Checkpoint Contents:
{
  "phase": 4,
  "finding_index": 3,
  "completed_findings": [
    {"id": "HIGH-001", "confidence": 0.92, "investigated": true},
    {"id": "MED-001", "confidence": 0.85, "investigated": true}
  ],
  "pending_findings": [
    {"id": "MED-002", "confidence": 0.71, "investigated": false},
    {"id": "MED-003", "confidence": 0.68, "investigated": false},
    {"id": "LOW-001", "confidence": 0.72, "investigated": false},
    {"id": "LOW-002", "confidence": 0.65, "investigated": false}
  ],
  "raw_findings": [...],
  "files_reviewed": [...]
}

Resume Command:
  /code-review --resume .claude/temp/code-review/checkpoint-2024-01-15-1423.json
```

**Resume Run**:
```bash
/code-review --resume .claude/temp/code-review/checkpoint-2024-01-15-1423.json
```

**Resume Output**:
```
Code Review - RESUMING
======================
Checkpoint: checkpoint-2024-01-15-1423.json
Resume from: Phase 4, finding 3/6

[RESUME] Skipping Phase 0-3 (already complete)
[RESUME] Phase 4: 4 findings remaining

[INVESTIGATE] Retrying with fallback strategy (Perplexity first)
  [MED-002] Confidence 0.71 -> Perplexity -> 0.83
  [MED-003] Confidence 0.68 -> Perplexity -> 0.79
  [LOW-001] Confidence 0.72 -> Perplexity -> 0.80
  [LOW-002] Confidence 0.65 -> Perplexity -> 0.52 (escalated)
Research calls: Context7=0 (skipped), Perplexity=4

[CONSOLIDATE] Phase 5 running...
[REPORT] Phase 6 generating...

Code Review Report
==================
Status: APPROVED_WITH_CONDITIONS

Summary:
- Files: 8 (8 Python)
- Findings: 5 (High: 1, Medium: 3, Low: 1)
- Resumed from checkpoint (Phase 4)

Open Questions (needs manual review):
[OQ-001] Potential memory leak in cache (confidence: 0.52)
  Location: packages/core/cache.py:89
  Research inconclusive - manual profiling recommended
```

---

## Example 5: Severity Conflict Resolution

**Scenario**: Two agents provide contradictory recommendations for the same code location. The orchestrator must resolve the conflict using weighted scoring.

**Code Under Review** (packages/api/handlers.py:87):
```python
def get_user(user_id: str):
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    return db.execute(query)
```

**Conflicting Agent Findings**:

**Agent 1: sast-scanner**
```json
{
  "finding_id": "CRIT-001",
  "severity": "Critical",
  "message": "SQL Injection vulnerability - user input directly interpolated",
  "confidence": 0.92,
  "recommendation": "Use parameterized queries immediately",
  "impact": "HIGH",
  "effort": "LOW (2 hours)"
}
```

**Agent 2: tech-debt-investigator**
```json
{
  "finding_id": "TD-001",
  "severity": "Medium",
  "message": "Direct SQL creates maintenance debt - violates repository pattern",
  "confidence": 0.78,
  "recommendation": "Migrate to repository pattern with ORM abstraction",
  "impact": "MEDIUM",
  "effort": "HIGH (12 hours)"
}
```

**Conflict Resolution Process**:

**Step 1: Detect Overlap**
```
[CONSOLIDATE] Overlap detected: CRIT-001 and TD-001
  Location match: packages/api/handlers.py:87
  Semantic similarity: 0.82 (> 0.70 threshold)
  Conflict type: SEVERITY_MISMATCH + RECOMMENDATION_DIVERGENCE
```

**Step 2: Calculate Weighted Scores**

Formula: `Score = (Severity_Weight * Confidence) / (Effort_Hours * Effort_Multiplier)`

| Factor | Agent 1 (sast-scanner) | Agent 2 (tech-debt) |
|--------|------------------------|---------------------|
| Severity Weight | 1.0 (Critical) | 0.6 (Medium) |
| Confidence | 0.92 | 0.78 |
| Effort Hours | 2 | 12 |
| Effort Multiplier | 0.20 (LOW) | 0.50 (HIGH) |
| **Final Score** | (1.0 * 0.92) / (2 * 0.20) = **2.30** | (0.6 * 0.78) / (12 * 0.50) = **0.078** |

**Step 3: Resolution Decision**
```
[RESOLVE] Agent 1 score (2.30) >> Agent 2 score (0.078)
  Winner: sast-scanner (CRIT-001)
  Action: Report as CRITICAL with immediate fix
  Deferred: tech-debt recommendation tracked separately
```

**Final Report Output**:
```
Code Review Report
==================
Status: CHANGES_REQUIRED

CRITICAL (must fix):
[CRIT-001] SQL Injection Vulnerability (packages/api/handlers.py:87)
  Confidence: 0.92 | Agent: sast-scanner
  
  Primary Fix (Score: 2.30 - IMMEDIATE):
  Use parameterized queries:
  ```python
  def get_user(user_id: str):
      query = text("SELECT * FROM users WHERE id = :user_id")
      return db.execute(query, {"user_id": user_id})
  ```
  Effort: 2 hours
  Verify: rg -n 'f"SELECT.*{' packages/api/
  
  Long-Term Enhancement (Score: 0.078 - DEFERRED):
  Consider repository pattern refactor in future sprint.
  Tracked as: TD-2024-Q1-042
  
  Conflict Resolution Notes:
  - sast-scanner: Immediate security fix (2h) - HIGH priority
  - tech-debt-investigator: Strategic refactor (12h) - DEFERRED
  - Decision: Security trumps architectural preference
  - Both recommendations are valid; sequencing matters
```

---

## Conflict Resolution Reference

### Severity Weights
| Severity | Weight |
|----------|--------|
| Critical | 1.0 |
| High | 0.8 |
| Medium | 0.6 |
| Low | 0.4 |
| Nit | 0.2 |

### Effort Multipliers
| Effort Level | Multiplier | Typical Hours |
|--------------|------------|---------------|
| LOW | 0.20 | 1-4 hours |
| MEDIUM | 0.35 | 4-8 hours |
| HIGH | 0.50 | 8+ hours |

### Resolution Rules
1. **Score difference > 10x**: Clear winner, loser is DEFERRED
2. **Score difference 2-10x**: Winner is PRIMARY, loser is ALTERNATIVE
3. **Score difference < 2x**: Both reported, user decides
4. **Security always wins**: If one finding is security-related, it takes priority regardless of score
