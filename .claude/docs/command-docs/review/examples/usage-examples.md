# Usage Examples for /review Command

Complete workflow examples with expected output.

---

## Example 1: Review Uncommitted Changes

```bash
/review --all
```

**Scenario**: Developer has modified 5 Python files, wants quality check before commit.

**Expected Flow**:
1. Discovers: 5 Python files from `git status`
2. Routes: code-quality, tech-debt-investigator, sast-scanner
3. Findings: 2 High, 3 Medium (all confidence >= 0.80)
4. Investigation: 1 finding researched with Context7 (0.72 -> 0.85)

**Expected Output**:
```
Code Review Report
==================
Status: APPROVED_WITH_CONDITIONS

Summary:
- Files: 5 (5 Python)
- Findings: 5 (High: 2, Medium: 3)
- Investigation: 1 finding researched (Context7: 1)

HIGH (should fix):
[HIGH-001] Async function not awaited (src/services/loader.py:67)
  Confidence: 0.88 | Verified: Context7 - FastAPI async patterns
  Fix: data = await fetch_data()
  Verify: rg -n 'fetch_data\(' | grep -v 'await'

[HIGH-002] Missing input validation (src/api/handlers.py:23)
  Confidence: 0.85
  Fix: Add Pydantic model validation
  Verify: pytest tests/api/test_handlers.py

MEDIUM (consider):
...

Next Steps:
- Fix HIGH issues before commit
- Re-run: /review --all
```

---

## Example 2: Security-Focused Review

```bash
/review --all --focus=security
```

**Scenario**: Pre-commit security scan for authentication module changes.

**Expected Flow**:
1. Discovers: 8 files from uncommitted changes
2. Routes: sast-scanner (primary), code-quality (security patterns)
3. Agents prioritize security rules (OWASP, secrets, injection)

**Expected Output**:
```
Code Review Report
==================
Status: CHANGES_REQUIRED

Summary:
- Files: 8 (8 Python)
- Findings: 3 (Critical: 1, High: 2)
- Focus: SECURITY

CRITICAL (must fix):
[CRIT-001] SQL Injection Vulnerability (src/api/routes.py:142)
  Confidence: 0.92 | Verified: Context7 + OWASP A01
  Problem: Raw SQL with string concatenation
  Fix: Use parameterized queries
  Verify: rg -n 'f"SELECT.*{' src/

HIGH (should fix):
[HIGH-001] Hardcoded API Key (src/config.py:15)
  Confidence: 0.95
  Fix: Move to environment variable
  Verify: rg -n 'api_key\s*=' src/

Security Notes:
- OWASP A01 (Injection): 1 finding
- OWASP A02 (Broken Auth): 0 findings
- Secrets detected: 1 hardcoded key
```


---

## Example 3: Feature Branch Review

```bash
/review --branch feature-auth --mode=comprehensive
```

**Scenario**: Technical lead reviews feature branch before merge to main.

**Expected Flow**:
1. Discovers: 15 files (8 Python, 5 Java, 2 TypeScript)
2. Routes: code-quality (8 files), reports gap for Java/TypeScript
3. Core agents only (no dynamic agents implemented yet)
4. Full investigation for all findings

**Expected Output**:
```
Code Review Report
==================
Status: APPROVED_WITH_CONDITIONS

Summary:
- Files: 15 (8 Python, 5 Java, 2 TypeScript)
- Findings: 12 (High: 3, Medium: 5, Low: 4)
- Comparison: feature-auth (45 commits) vs main
- Duration: ~3 minutes

Language Coverage:
- Python: REVIEWED (code-quality)
- Java: SKIPPED (no reviewer available)
- TypeScript: SKIPPED (no reviewer available)

HIGH (should fix):
[HIGH-001] SOLID Violation - Single Responsibility (src/auth/manager.py)
  Confidence: 0.87 | Agent: code-quality
  Problem: UserManager handles auth, logging, and email
  Fix: Extract EmailService and AuditLogger classes

Gaps Detected:
- Java: 5 files not reviewed
  Recommendation: Create java-code-reviewer (Priority: P1)
- TypeScript: 2 files not reviewed
  Recommendation: Create typescript-code-reviewer (Priority: P1)
```

---

## Example 4: Quick Mode vs Comprehensive

### Quick Mode
```bash
/review --all --mode=quick
```

**Characteristics**:
- 3 core agents only (no dynamic)
- Minimal investigation (Context7 only for < 0.75)
- Duration: ~30 seconds

### Comprehensive Mode (default)
```bash
/review --all --mode=comprehensive
```

**Characteristics**:
- 3 core + 0-2 dynamic agents
- Full investigation (Context7 -> Perplexity -> Escalate)
- Duration: ~2-5 minutes

---

## Example 5: Specific Files Review

```bash
/review --files src/auth.py src/api/handlers.py tests/test_auth.py
```

**Scenario**: Developer wants review of specific files only.

**Expected Output**:
```
Code Review Report
==================
Status: APPROVED

Summary:
- Files: 3 (3 Python)
- Findings: 2 (Medium: 1, Low: 1)

MEDIUM (consider):
[MED-001] Missing test for error path (tests/test_auth.py)
  Confidence: 0.78
  Fix: Add test for invalid credentials scenario

LOW (optional):
[LOW-001] Magic number (src/auth.py:45)
  Confidence: 0.75
  Fix: SESSION_TIMEOUT_SECONDS = 3600  # 1 hour
```


---

## Example 6: Investigation Trail

**Scenario**: Finding with low initial confidence goes through full research pipeline.

**Initial Finding**:
```json
{
  "finding_id": "MED-001",
  "severity": "Medium",
  "message": "Potential memory leak in cache manager",
  "confidence": 0.62,
  "location": "src/cache/manager.py:89"
}
```

**Investigation Process**:

1. **Context7 Research** (confidence < 0.75):
   - Library: "cachetools"
   - Topic: "memory management TTL cache"
   - Result: Docs mention weak references for memory management
   - Confidence: 0.62 -> 0.71

2. **Perplexity Escalation** (still < 0.75):
   - Query: "Python TTLCache memory leak patterns"
   - Sources: Real Python, Stack Overflow (3 answers), GitHub issues
   - Result: Moderate consensus - depends on object lifecycle
   - Confidence: 0.71 -> 0.74

3. **User Escalation** (< 0.75 after research):
   - Moved to "Open Questions"
   - Manual review recommended

**Final Output**:
```
Open Questions (needs manual review):
[OQ-001] Potential memory leak in cache manager (confidence: 0.74)
  Location: src/cache/manager.py:89
  
  Investigation Trail:
  - Initial: 0.62
  - Context7 (cachetools docs): +0.09 -> 0.71
  - Perplexity (3 sources): +0.03 -> 0.74
  
  Research Summary:
  - Official docs mention weak references but unclear on TTL interaction
  - Community sources have conflicting opinions
  - GitHub issues show similar reports but no confirmed fix
  
  Recommendation:
  - Profile memory usage under load
  - Review object lifecycle in cache usage
  - DO NOT assume this is a bug without testing
```

---

## Example 7: Conflict Resolution

**Scenario**: Two agents provide contradictory recommendations.

**Agent 1 (code-quality)**:
- Finding: SQL injection vulnerability (Critical, confidence 0.88)
- Recommendation: Use parameterized queries with SQLAlchemy ORM
- Impact: HIGH (security fix required)
- Effort: MEDIUM (4 hours)

**Agent 2 (tech-debt-investigator)**:
- Finding: Direct SQL creates maintenance debt (Medium, confidence 0.75)
- Recommendation: Migrate to repository pattern with ORM abstraction
- Impact: MEDIUM (improves maintainability)
- Effort: HIGH (12 hours)

**Resolution via Weighted Scoring**:
```
Agent 1: Score = 0.90 / (4 * 0.20) = 1.125
Agent 2: Score = 0.60 / (12 * 0.50) = 0.100
```

**Final Output**:
```
CRITICAL (must fix):
[CRIT-001] SQL Injection Vulnerability (src/api/handlers.py:87)
  Confidence: 0.92
  
  Primary Fix (Score: 1.125 - IMMEDIATE):
  Use parameterized queries:
  ```python
  result = db.query("SELECT * FROM users WHERE id = :user_id", {"user_id": user_id})
  ```
  
  Long-Term Enhancement (Score: 0.100 - DEFERRED):
  Consider repository pattern refactor in future sprint.
  Tracked as: TD-2024-Q4-007
  
  Conflict Resolution:
  Agent 1's tactical fix (4 hours) provides immediate security value.
  Agent 2's strategic refactor (12 hours) is valuable but deferred.
```
