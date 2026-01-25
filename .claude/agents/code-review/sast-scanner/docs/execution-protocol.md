# SAST Execution Protocol

**Purpose**: Step-by-step scan workflow, Semgrep CLI commands, and error handling

---

## Version Requirements

**Minimum Semgrep Version**: 1.140.0

Pin version in project dependencies:
```bash
# In pyproject.toml or UV dependencies
semgrep>=1.140.0,<2.0.0
```

**Rationale**: Ensures consistent JSON output format and ruleset compatibility.

---

## Execution Steps

### Step 1: Validate Environment

```bash
AGENT_NAME=sast-scanner semgrep --version
```

**Exit Conditions**:
- Success → Continue to Step 2
- Command not found → Return FAILURE (missing_dependency)

### Step 2: Build Scan Command

```bash
AGENT_NAME=sast-scanner semgrep \
  --config=p/security-audit \
  --config=p/python \
  --config=p/secrets \
  --baseline-commit=HEAD \
  --json \
  --quiet \
  <file1> <file2> <file3>
```

**Ruleset Selection**:
- Always: `p/security-audit`, `p/secrets`
- Python projects: `p/python`
- Framework detected: `p/django` | `p/flask` | `p/fastapi`

### Step 3: Execute Scan

```bash
output=$(AGENT_NAME=sast-scanner semgrep <args> 2>&1)
exit_code=$?
```

**Exit Code Interpretation**:
| Code | Meaning | Action |
|------|---------|--------|
| 0 | Clean scan | Continue |
| 1 | Findings found | Continue (expected) |
| >1 | Error | Return FAILURE |

### Step 4: Parse JSON Output

Extract from Semgrep JSON:
- `results[]` - Array of findings
- `results[].check_id` - Rule identifier
- `results[].path` - File path
- `results[].start.line` / `.col` - Location
- `results[].extra.severity` - ERROR/WARNING/INFO
- `results[].extra.metadata.owasp` - OWASP category
- `results[].extra.metadata.cwe` - CWE identifier
- `results[].extra.message` - Finding description

---

## Scope Validation

**Post-Scan Assertion**:
```python
assert scan_summary.total_files_scanned == len(input.files), \
    f"Scope reduction: {len(input.files) - scan_summary.total_files_scanned} files skipped"
```

If files are skipped due to `.semgrepignore` or other filters, log warning with list of skipped files.

---

### Step 5: Map Findings to Groups

```
FOR each finding in results:
  file = finding.path
  FOR each group in commit_groups:
    IF file in group.files:
      IF finding.severity == "ERROR":
        group.blocking_issues.append(finding)
      ELSE:
        group.warnings.append(finding)
```

### Step 6: Determine Group Status

```
FOR each group in commit_groups:
  IF len(group.blocking_issues) > 0:
    group.security_status = "CHANGES_REQUIRED"
  ELSE IF len(group.warnings) > 0:
    group.security_status = "APPROVED_WITH_WARNINGS"
  ELSE:
    group.security_status = "APPROVED"
```

### Step 7: Return Results

Return JSON matching schema with:
- `status`: "SUCCESS"
- `scan_summary`: files scanned, duration, findings by severity
- `group_results`: security_status per group
- `recommendations`: actionable next steps

---

## Error Handling

### Missing Dependency

```json
{
  "status": "FAILURE",
  "failure_details": {
    "failure_type": "missing_dependency",
    "reasons": ["Semgrep CLI not found"],
    "recovery_suggestions": [
      {"approach": "Install Semgrep", "rationale": "Run: uv run pip install semgrep"}
    ]
  }
}
```

### Scan Error

```json
{
  "status": "FAILURE",
  "failure_details": {
    "failure_type": "scan_error",
    "reasons": ["Semgrep scan failed with exit code 2"],
    "scan_attempted": {
      "files": ["file1.py"],
      "exit_code": 2,
      "stderr": "error message"
    }
  }
}
```

### Parse Error

```json
{
  "status": "FAILURE",
  "failure_details": {
    "failure_type": "parse_error",
    "reasons": ["Semgrep output not valid JSON"],
    "recovery_suggestions": [
      {"approach": "Verify --json flag", "rationale": "Check Semgrep command syntax"}
    ]
  }
}
```

### Timeout

```json
{
  "status": "FAILURE",
  "failure_details": {
    "failure_type": "timeout",
    "reasons": ["Scan exceeded 120 second timeout"],
    "recovery_suggestions": [
      {"approach": "Reduce file count", "rationale": "Split into smaller batches"}
    ]
  }
}
```

---

## Performance Constraints

| File Count | Target Duration | Strategy |
|------------|-----------------|----------|
| 1-10 | <10 seconds | Single scan |
| 11-50 | <30 seconds | Single scan |
| 50+ | <60 seconds | Consider batching |

**Optimization**:
- Use `--baseline-commit=HEAD` for diff-aware scanning
- Scan only modified files, not entire codebase
- Filter by severity threshold if needed

---

## Quick Reference

- Timeout: 120 seconds (Bash)
- Rulesets: p/security-audit + p/python + p/secrets (minimum)
- Exit codes: 0=clean, 1=findings, >1=error
