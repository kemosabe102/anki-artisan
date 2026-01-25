# SAST Scanner Delegation Examples

**Purpose**: How orchestrator delegates to sast-scanner and expected outputs

---

## Git Workflow Phase 3 Integration

The sast-scanner runs in parallel with python-code-reviewer and tech-debt-investigator during Phase 3 quality gates.

```
PHASE 3: QUALITY GATES (Automated, Parallel)
├─ [python-code-reviewer] → code quality assessment
├─ [tech-debt-investigator] → tech debt analysis
└─ [sast-scanner] → security vulnerability detection ← THIS AGENT
```

---

## Orchestrator Delegation Pattern

```javascript
// Phase 3: Spawn 3 agents in parallel (single message)
Task(python-code-reviewer, { files: all_files });
Task(tech-debt-investigator, { files: all_files });
Task(sast-scanner, { files: all_files, groups: commit_groups });

// Orchestrator waits for all 3 to complete (~1 minute parallel)
// Then merges results and presents in Phase 4
```

---

## Input Example

```json
{
  "operation": "scan_files",
  "files": [
    "packages/core/auth/validators.py",
    "packages/api/handlers.py",
    "tests/test_auth.py"
  ],
  "commit_groups": [
    {
      "group_id": "group_1",
      "files": ["packages/core/auth/validators.py"],
      "change_type": "feat",
      "scope": "auth"
    },
    {
      "group_id": "group_2",
      "files": ["packages/api/handlers.py", "tests/test_auth.py"],
      "change_type": "refactor",
      "scope": "api"
    }
  ],
  "baseline_commit": "HEAD",
  "severity_threshold": "ERROR",
  "execution_timestamp": "2025-10-17T10:00:00Z"
}
```

---

## Output Examples

### Scenario 1: Clean Code (All Groups APPROVED)

```json
{
  "status": "SUCCESS",
  "agent": "sast-scanner",
  "confidence": 0.92,
  "execution_timestamp": "2025-10-17T10:00:08Z",
  "summary": "Scanned 3 files, no security issues found",
  "agent_specific_output": {
    "scan_summary": {
      "total_files_scanned": 3,
      "scan_duration_seconds": 5.2,
      "findings_by_severity": {},
      "semgrep_version": "1.140.0",
      "rulesets_used": ["p/security-audit", "p/python", "p/secrets"]
    },
    "group_results": [
      {
        "group_id": "group_1",
        "security_status": "APPROVED",
        "blocking_issues": [],
        "warnings": []
      },
      {
        "group_id": "group_2",
        "security_status": "APPROVED",
        "blocking_issues": [],
        "warnings": []
      }
    ]
  },
  "recommendations": ["All groups approved - no security issues detected"]
}
```

### Scenario 2: Non-Blocking Warnings (APPROVED_WITH_WARNINGS)

```json
{
  "status": "SUCCESS",
  "agent": "sast-scanner",
  "confidence": 0.92,
  "summary": "Scanned 3 files, found 1 WARNING severity finding",
  "agent_specific_output": {
    "scan_summary": {
      "total_files_scanned": 3,
      "findings_by_severity": { "WARNING": 1 }
    },
    "group_results": [
      {
        "group_id": "group_2",
        "security_status": "APPROVED_WITH_WARNINGS",
        "blocking_issues": [],
        "warnings": [
          {
            "check_id": "python.flask.security.xss.audit.template-autoescape-off",
            "path": "packages/api/handlers.py",
            "line": 145,
            "column": 20,
            "severity": "WARNING",
            "message": "Template autoescape is disabled - potential XSS risk",
            "owasp": "A03:2021 - Injection",
            "cwe": "CWE-79",
            "confidence": "MEDIUM",
            "remediation": "Enable autoescape in template configuration"
          }
        ]
      }
    ]
  },
  "recommendations": ["Review 1 WARNING severity finding (non-blocking)"]
}
```

### Scenario 3: Blocking Issues (CHANGES_REQUIRED)

```json
{
  "status": "SUCCESS",
  "agent": "sast-scanner",
  "confidence": 0.92,
  "summary": "Scanned 3 files, found 2 ERROR severity findings in 1 group",
  "agent_specific_output": {
    "scan_summary": {
      "total_files_scanned": 3,
      "findings_by_severity": { "ERROR": 2, "WARNING": 1 }
    },
    "group_results": [
      {
        "group_id": "group_1",
        "security_status": "CHANGES_REQUIRED",
        "blocking_issues": [
          {
            "check_id": "python.django.security.injection.sql-injection",
            "path": "packages/core/auth/validators.py",
            "line": 67,
            "column": 8,
            "severity": "ERROR",
            "message": "User input passed to SQL query without parameterization",
            "owasp": "A03:2021 - Injection",
            "cwe": "CWE-89",
            "confidence": "HIGH",
            "remediation": "Use parameterized queries or ORM methods"
          },
          {
            "check_id": "python.lang.security.audit.hardcoded-password",
            "path": "packages/core/auth/validators.py",
            "line": 23,
            "column": 12,
            "severity": "ERROR",
            "message": "Hardcoded password detected",
            "owasp": "A02:2021 - Cryptographic Failures",
            "cwe": "CWE-798",
            "confidence": "HIGH",
            "remediation": "Use environment variables or secrets management"
          }
        ],
        "warnings": []
      }
    ]
  },
  "recommendations": [
    "Fix 2 ERROR severity security issues in group_1 before committing",
    "SQL injection at validators.py:67 - use parameterized queries",
    "Hardcoded password at validators.py:23 - use environment variables"
  ]
}
```

### Scenario 4: Mixed Groups

```json
{
  "status": "SUCCESS",
  "agent": "sast-scanner",
  "summary": "Scanned 3 files across 2 groups with mixed results",
  "agent_specific_output": {
    "group_results": [
      {
        "group_id": "group_1",
        "security_status": "CHANGES_REQUIRED",
        "blocking_issues": [{ "severity": "ERROR", "message": "SQL injection" }],
        "warnings": []
      },
      {
        "group_id": "group_2",
        "security_status": "APPROVED",
        "blocking_issues": [],
        "warnings": []
      }
    ]
  },
  "recommendations": [
    "group_1: BLOCKED - fix ERROR severity issues before commit",
    "group_2: APPROVED - ready to commit"
  ]
}
```

---

## Phase 4 Presentation (Orchestrator Merges Results)

```
Group 1: feat(auth) - JWT authentication ❌ BLOCKED
  Code Quality: ✅ APPROVED
  Tech Debt: ✅ NONE
  Security: ❌ CHANGES_REQUIRED
    Blocking Issues:
    - SQL injection in validators.py:67 (ERROR)
    - Hardcoded password in validators.py:23 (ERROR)
  Files: 1 file

Group 2: refactor(api) - Handler cleanup ✅ READY
  Code Quality: ✅ APPROVED
  Tech Debt: ✅ NONE
  Security: ⚠️ APPROVED_WITH_WARNINGS
    Warnings:
    - XSS risk in handlers.py:145 (WARNING)
  Files: 2 files
```

---

## Quick Reference

| Security Status | Meaning | Blocks Commit |
|-----------------|---------|---------------|
| APPROVED | No issues | NO |
| APPROVED_WITH_WARNINGS | Non-blocking warnings | NO |
| CHANGES_REQUIRED | ERROR severity found | YES |
