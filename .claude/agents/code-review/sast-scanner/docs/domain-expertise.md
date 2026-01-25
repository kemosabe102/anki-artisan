# SAST Domain Expertise

**Purpose**: OWASP Top 10 coverage, CWE patterns, Semgrep ruleset details, and severity classification

---

## OWASP Top 10 2021 Coverage

| Category | Description | Common CWEs | Python Patterns |
|----------|-------------|-------------|-----------------|
| A01:2021 | Broken Access Control | CWE-200, CWE-284 | Missing auth decorators, IDOR |
| A02:2021 | Cryptographic Failures | CWE-327, CWE-798 | Weak algorithms, hardcoded secrets |
| A03:2021 | Injection | CWE-79, CWE-89 | SQL injection, XSS, command injection |
| A04:2021 | Insecure Design | CWE-209, CWE-502 | Deserialization, error exposure |
| A05:2021 | Security Misconfiguration | CWE-16, CWE-611 | Debug enabled, XXE |
| A06:2021 | Vulnerable Components | CWE-1104 | Outdated dependencies |
| A07:2021 | Auth Failures | CWE-287, CWE-384 | Weak passwords, session fixation |
| A08:2021 | Data Integrity Failures | CWE-502, CWE-829 | Unsafe deserialization |
| A09:2021 | Logging Failures | CWE-778 | Insufficient logging |
| A10:2021 | SSRF | CWE-918 | Server-side request forgery |

---

## CWE Quick Reference

| CWE | Name | Severity | Semgrep Rule Pattern |
|-----|------|----------|---------------------|
| CWE-79 | XSS | ERROR | `python.flask.security.xss.*` |
| CWE-89 | SQL Injection | ERROR | `python.django.security.injection.sql-*` |
| CWE-327 | Weak Crypto | WARNING | `python.cryptography.security.*` |
| CWE-502 | Deserialization | ERROR | `python.lang.security.deserialization.*` |
| CWE-798 | Hardcoded Credentials | ERROR | `python.lang.security.audit.hardcoded-*` |
| CWE-918 | SSRF | ERROR | `python.requests.security.ssrf.*` |

---

## Semgrep Rulesets

### Primary Rulesets (Always Used)

| Ruleset | Purpose | Finding Types |
|---------|---------|---------------|
| `p/security-audit` | Comprehensive security | All OWASP categories |
| `p/secrets` | Credential detection | API keys, passwords, tokens |

### Framework-Specific Rulesets

| Ruleset | When to Use | Patterns |
|---------|-------------|----------|
| `p/python` | All Python projects | Language-specific vulnerabilities |
| `p/django` | Django detected | ORM injection, CSRF, auth bypass |
| `p/flask` | Flask detected | XSS, session issues, debug mode |
| `p/fastapi` | FastAPI detected | Async issues, Pydantic validation |

### Framework Detection

Detect framework by checking imports in scanned files:
- `from django` or `import django` → Add `p/django`
- `from flask` or `import flask` → Add `p/flask`
- `from fastapi` or `import fastapi` → Add `p/fastapi`

---

## Severity Classification

| Level | Impact | Blocks Commit | Example |
|-------|--------|---------------|---------|
| ERROR | Critical vulnerability | YES | SQL injection, hardcoded secrets |
| WARNING | Potential risk | NO | Weak crypto, missing validation |
| INFO | Best practice | NO | Code style, defensive patterns |

### Status Determination Logic

```
IF group has any ERROR severity findings:
  security_status = "CHANGES_REQUIRED"
ELSE IF group has WARNING or INFO findings:
  security_status = "APPROVED_WITH_WARNINGS"  
ELSE:
  security_status = "APPROVED"
```

---

## Confidence Scoring

| Metric | Value | Rationale |
|--------|-------|-----------|
| scan_execution | 1.0 | Semgrep is deterministic |
| finding_accuracy | 0.92 | Semgrep false positive rate ~8% |
| owasp_mapping | 0.95 | Metadata from Semgrep rules is authoritative |

---

## Quick Reference

- **OWASP Reference**: https://owasp.org/Top10/
- **CWE Database**: https://cwe.mitre.org/
- **Semgrep Docs**: https://semgrep.dev/docs
- **Semgrep Registry**: https://semgrep.dev/r
