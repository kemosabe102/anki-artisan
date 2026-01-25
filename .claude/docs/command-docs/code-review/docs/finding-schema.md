# Finding Schema Documentation

Complete structure for code review findings with source tracking and conflict resolution.

---

## Finding Object Structure

```json
{
  "finding_id": "CRIT-001",
  "severity": "Critical",
  "category": "Security",
  "location": "src/api/routes.py:142",
  "message": "SQL injection vulnerability in query builder",
  "confidence": 0.92,
  "source_agent": "sast-scanner",
  "confidence_sources": [
    "researcher-external: SQLAlchemy Security Best Practices (trust: 9/10)",
    "researcher-external: OWASP A01:2021 SQL Injection Prevention"
  ],
  "problem": "Raw SQL query with string concatenation allows arbitrary SQL execution",
  "principle": "Python Security Patterns - SQL Injection Prevention",
  "verification_commands": [
    "rg -n 'f\\\"SELECT.*WHERE.*{' src/",
    "pytest tests/security/test_sql_injection.py"
  ],
  "recommendation": "Use parameterized queries: text('SELECT * FROM users WHERE id = :user_id')",
  "investigation_trail": {
    "initial_confidence": 0.75,
    "researcher_library_result": "Validated against SQLAlchemy docs, increased to 0.85",
    "researcher_web_result": "Confirmed with OWASP A01, final confidence 0.92",
    "final_confidence": 0.92
  },
  "conflict_resolution": null,
  "impact": 10,
  "effort": 4,
  "risk_multiplier": 1.2,
  "change_multiplier": 1.0,
  "priority_score": 1.25,
  "remediation_time_days": 10,
  "cvss_score": 9.1
}
```


---

## Field Definitions

### Core Fields

| Field | Type | Description |
|-------|------|-------------|
| `finding_id` | string | Unique identifier (e.g., CRIT-001, HIGH-003) |
| `severity` | enum | Critical, High, Medium, Low, Nit |
| `category` | string | Security, Performance, Quality, Design, Maintainability |
| `location` | string | File path and line number (file.py:line) |
| `message` | string | Clear, concise description of the issue |
| `confidence` | float | 0.0-1.0, final confidence after investigation |

### Source Tracking Fields

| Field | Type | Description |
|-------|------|-------------|
| `source_agent` | string | Agent that originally reported this finding |
| `confidence_sources` | array | List of research sources that validated the finding |
| `investigation_trail` | object | Research history (initial, library, web, final) |

### Conflict Resolution Object

When multiple agents report the same issue with different severities:

```json
{
  "conflict_resolution": {
    "conflicting_agents": ["python-code-reviewer", "sast-scanner"],
    "severities_reported": ["Medium", "High"],
    "resolution_strategy": "security_precedence",
    "final_severity": "High",
    "rationale": "Security agent (sast-scanner) rated higher; security takes precedence"
  }
}
```


| Field | Type | Description |
|-------|------|-------------|
| `conflicting_agents` | array | Agents that reported conflicting severities |
| `severities_reported` | array | Each agent's reported severity |
| `resolution_strategy` | enum | `security_precedence`, `higher_confidence`, `highest_severity` |
| `final_severity` | string | Resolved severity after conflict resolution |
| `rationale` | string | Explanation of resolution decision |

### Resolution Strategies

| Strategy | When Applied | Rule |
|----------|--------------|------|
| `security_precedence` | Security agent vs quality agent | Security agent severity wins |
| `higher_confidence` | Same domain, different confidence | Higher confidence agent wins |
| `highest_severity` | Tie or equal confidence | Use most conservative (highest) severity |

---

### Investigation Fields

| Field | Type | Description |
|-------|------|-------------|
| `problem` | string | Detailed explanation of what's wrong |
| `principle` | string | Reference to coding standard or guideline |

### Actionability Fields

| Field | Type | Description |
|-------|------|-------------|
| `verification_commands` | array | Deterministic commands to verify the issue |
| `recommendation` | string | Specific fix with code example if applicable |
| `remediation_time_days` | int | Estimated time to fix based on severity |


### Prioritization Fields

| Field | Type | Description |
|-------|------|-------------|
| `impact` | int | 1-10, severity of user/system harm |
| `effort` | int | 1-10, complexity to fix |
| `risk_multiplier` | float | 1.0-2.0, risk of introducing bugs |
| `change_multiplier` | float | 1.0-1.5, scope of change required |
| `priority_score` | float | Calculated: (Impact * 0.6) / (Effort * Risk * Change) |
| `cvss_score` | float | CVSS severity score (security findings only) |

---

## Severity Definitions

| Severity | Impact | Examples |
|----------|--------|----------|
| **Critical** | System failure, security breach, data loss | SQL injection, auth bypass, data exposure |
| **High** | Significant breakage, user-facing bugs | Async not awaited, null pointer, race condition |
| **Medium** | Non-core issues, performance degradation | N+1 queries, missing validation, code duplication |
| **Low** | Aesthetic, minimal impact | Magic numbers, unclear naming, missing docs |
| **Nit** | Stylistic preferences | Variable naming style, formatting |

---

## Confidence Thresholds by Severity

| Severity | Minimum Confidence | Investigation Required |
|----------|-------------------|------------------------|
| Critical | 0.90 | ALWAYS researcher-external |
| High | 0.80 | researcher-external if < 0.90 |
| Medium | 0.75 | researcher-external if < 0.85 |
| Low | 0.70 | Optional |
| Nit | 0.60 | None |

---

## Priority Score Calculation

```python
priority_score = (impact * 0.6) / (effort * risk_multiplier * change_multiplier)

# Example: SQL Injection
# Impact: 10 (security breach)
# Effort: 4 (use parameterized queries)
# Risk: 1.2 (low risk with proper testing)
# Change: 1.0 (localized change)
# Score: (10 * 0.6) / (4 * 1.2 * 1.0) = 1.25 -> CRITICAL PRIORITY
```
