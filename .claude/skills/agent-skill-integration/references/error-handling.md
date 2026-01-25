# Error Handling Patterns

Comprehensive error handling for skill invocations, including detection, recovery, and prevention strategies.

---

## Table of Contents

1. [Error Categories](#error-categories)
2. [Error Response Format](#error-response-format)
3. [Recovery Strategies](#recovery-strategies)
4. [Prevention Patterns](#prevention-patterns)
5. [Escalation Protocol](#escalation-protocol)

---

## Error Categories

### Category Reference

| Code | Category | Severity | Auto-Recoverable |
|------|----------|----------|------------------|
| `INPUT_MISSING` | Missing required input | Medium | Yes |
| `INPUT_INVALID` | Malformed input | Medium | Yes |
| `SKILL_NOT_FOUND` | Skill doesn't exist | High | No |
| `PERMISSION_DENIED` | Tool access blocked | High | No |
| `EXEC_FAILED` | Runtime failure | Medium | Partial |
| `TIMEOUT` | Operation exceeded limit | Medium | Yes |
| `PARTIAL_FAILURE` | Some operations failed | Low | Yes |
| `DEPENDENCY_MISSING` | Required skill/tool unavailable | High | No |

---

### INPUT_MISSING

**When**: Required fields not provided in request.

**Detection**:
```python
if not request.get("files") and not request.get("code"):
    raise SkillError("INPUT_MISSING", "No code or files provided")
```

**Response**:
```json
{
  "status": "FAILURE",
  "error": {
    "code": "INPUT_MISSING",
    "field": "files",
    "message": "Required field 'files' not provided",
    "recovery": "Provide file paths or code block"
  }
}
```

**Recovery**: Prompt user for missing input with clear examples.

---

### INPUT_INVALID

**When**: Input provided but malformed or incorrect type.

**Detection**:
```python
if not isinstance(request.get("confidence_threshold"), (int, float)):
    raise SkillError("INPUT_INVALID", "confidence_threshold must be number")
```

**Response**:
```json
{
  "status": "FAILURE",
  "error": {
    "code": "INPUT_INVALID",
    "field": "confidence_threshold",
    "received": "high",
    "expected": "number between 0 and 1",
    "example": 0.85
  }
}
```

**Recovery**: Show correct format with example.

---

### SKILL_NOT_FOUND

**When**: Requested skill doesn't exist in any discovery location.

**Detection**:
```python
skill_paths = [
    "~/.claude/skills/{name}/SKILL.md",
    ".claude/skills/{name}/SKILL.md"
]
if not any(path.exists() for path in skill_paths):
    raise SkillError("SKILL_NOT_FOUND", f"Skill '{name}' not found")
```

**Response**:
```json
{
  "status": "FAILURE",
  "error": {
    "code": "SKILL_NOT_FOUND",
    "skill": "code-optimizer",
    "searched": [
      "~/.claude/skills/code-optimizer/",
      ".claude/skills/code-optimizer/"
    ],
    "similar": ["code-quality", "code-review-standards"],
    "recovery": "Use one of the similar skills or create the skill"
  }
}
```

**Recovery**: Suggest similar skills or creation instructions.

---

### PERMISSION_DENIED

**When**: Skill attempts to use tool not in `allowed-tools`.

**Detection**:
```python
allowed = skill.frontmatter.get("allowed-tools", [])
if "Edit" not in allowed and operation == "edit":
    raise SkillError("PERMISSION_DENIED", "Edit tool not permitted")
```

**Response**:
```json
{
  "status": "FAILURE",
  "error": {
    "code": "PERMISSION_DENIED",
    "tool": "Edit",
    "skill": "safe-analyzer",
    "allowed": ["Read", "Grep", "Glob"],
    "recovery": "Use a skill with Edit permission or request escalation"
  }
}
```

**Recovery**: Suggest alternative skill or escalation path.

---

### EXEC_FAILED

**When**: Skill execution encounters runtime error.

**Common Causes**:
- File not found during analysis
- Parse error in target code
- Network failure for external resources
- Memory exhaustion on large files

**Response**:
```json
{
  "status": "FAILURE",
  "error": {
    "code": "EXEC_FAILED",
    "phase": "analysis",
    "message": "Failed to parse packages/legacy/old_module.py",
    "details": "SyntaxError: invalid syntax at line 42",
    "partial_results": {
      "files_completed": 3,
      "files_failed": 1
    },
    "recovery": "Fix syntax error or exclude file from analysis"
  }
}
```

**Recovery**: Return partial results, suggest fix for failed items.

---

### TIMEOUT

**When**: Operation exceeds time limit (default: 60s).

**Response**:
```json
{
  "status": "TIMEOUT",
  "error": {
    "code": "TIMEOUT",
    "limit_seconds": 60,
    "elapsed_seconds": 60.2,
    "progress": {
      "completed": 45,
      "total": 128,
      "percentage": 35
    },
    "partial_results": {...},
    "recovery": {
      "strategy": "chunk",
      "suggested_chunks": [
        "packages/core/",
        "packages/api/",
        "packages/utils/"
      ]
    }
  }
}
```

**Recovery**: Break into smaller operations, return partial results.

---

## Error Response Format

### Standard Error Structure

```json
{
  "skill": "skill-name",
  "status": "FAILURE",
  "timestamp": "2025-01-15T10:30:00Z",
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description",
    "details": "Technical details for debugging",
    "recovery": "Suggested action to resolve",
    "documentation": "link/to/relevant/docs"
  },
  "partial_results": null,
  "context": {
    "request_id": "abc123",
    "files_affected": []
  }
}
```

### Error with Partial Results

```json
{
  "skill": "code-quality",
  "status": "PARTIAL",
  "error": {
    "code": "PARTIAL_FAILURE",
    "failed_items": [
      {"file": "legacy.py", "reason": "Syntax error"},
      {"file": "binary.pyc", "reason": "Not source code"}
    ]
  },
  "partial_results": {
    "successful_files": ["auth.py", "handler.py", "utils.py"],
    "issues_found": 5,
    "analysis": {...}
  }
}
```

---

## Recovery Strategies

### Strategy 1: Retry with Reduced Scope

**When**: TIMEOUT or EXEC_FAILED on large operations.

**Pattern**:
```markdown
1. Identify failed/incomplete items
2. Isolate working subset
3. Retry failed items individually
4. Aggregate results
```

**Example**:
```
Original: "Review all 128 files"
Timeout after 45 files

Recovery:
1. Accept results for 45 completed files
2. Chunk remaining 83 files into groups of 20
3. Process: "Review files 46-65", "Review files 66-85", etc.
4. Merge all results
```

---

### Strategy 2: Input Correction

**When**: INPUT_MISSING or INPUT_INVALID.

**Pattern**:
```markdown
1. Identify missing/invalid field
2. Show expected format with example
3. Request corrected input
4. Validate before retry
```

**Example**:
```markdown
## Input Correction Required

**Error**: confidence_threshold must be a number

**You provided**: "high"

**Expected format**: Number between 0 and 1

**Example**:
```json
{
  "confidence_threshold": 0.85
}
```

Please provide the corrected value.
```

---

### Strategy 3: Alternative Skill

**When**: SKILL_NOT_FOUND or PERMISSION_DENIED.

**Pattern**:
```markdown
1. Identify user intent
2. Find skills with matching capabilities
3. Suggest alternatives with trade-offs
```

**Example**:
```markdown
## Skill Not Available

**Requested**: code-optimizer (not found)

**Similar skills available**:

| Skill | Match | Trade-off |
|-------|-------|-----------|
| code-quality | 70% | Review only, no auto-fix |
| code-review-standards | 50% | Style focus, not performance |

**Recommendation**: Use code-quality for analysis, 
then manually apply optimizations from recommendations.
```

---

### Strategy 4: Graceful Degradation

**When**: Partial results available despite errors.

**Pattern**:
```markdown
1. Complete what's possible
2. Document failures with reasons
3. Provide actionable partial results
4. Suggest manual completion for failed items
```

**Example**:
```markdown
## Partial Analysis Complete

### Successfully Analyzed (3/5 files)
- auth.py: 2 issues found
- handler.py: 0 issues
- utils.py: 1 issue

### Failed Analysis (2/5 files)
| File | Reason | Manual Action |
|------|--------|---------------|
| legacy.py | Syntax error line 42 | Fix syntax, retry |
| config.pyc | Binary file | N/A (expected) |

### Current Findings (from successful files)
[detailed analysis of 3 files...]

### Next Steps
1. Fix legacy.py syntax error
2. Run: "Review packages/core/legacy.py"
3. Merge results manually
```

---

## Prevention Patterns

### Pre-Validation

Validate inputs before skill execution:

```python
def validate_request(request):
    errors = []
    
    # Check required fields
    if not request.get("files") and not request.get("code"):
        errors.append(("INPUT_MISSING", "files or code required"))
    
    # Check field types
    if "confidence" in request:
        if not isinstance(request["confidence"], (int, float)):
            errors.append(("INPUT_INVALID", "confidence must be number"))
        elif not 0 <= request["confidence"] <= 1:
            errors.append(("INPUT_INVALID", "confidence must be 0-1"))
    
    # Check file existence
    for file in request.get("files", []):
        if not Path(file).exists():
            errors.append(("FILE_NOT_FOUND", f"{file} does not exist"))
    
    return errors
```

### Timeout Prevention

Estimate operation time before execution:

```python
def estimate_time(files):
    # ~2 seconds per file for code review
    estimated = len(files) * 2
    
    if estimated > 60:  # timeout threshold
        return {
            "warning": "Operation may timeout",
            "estimated_time": estimated,
            "suggestion": f"Consider chunking into {estimated // 50 + 1} batches"
        }
    return None
```

### Permission Check

Verify tool permissions before attempting operations:

```python
def check_permissions(skill, required_tools):
    allowed = set(skill.allowed_tools or [])
    required = set(required_tools)
    
    missing = required - allowed
    if missing:
        return {
            "error": "PERMISSION_DENIED",
            "missing_tools": list(missing),
            "suggestion": f"Use skill with {missing} permission"
        }
    return None
```

---

## Escalation Protocol

### When to Escalate

| Condition | Escalation Level |
|-----------|------------------|
| 3+ retries failed | User notification |
| PERMISSION_DENIED | User approval required |
| SKILL_NOT_FOUND (critical) | User decision |
| Data loss risk | IMMEDIATE user confirmation |

### Escalation Format

```markdown
## Escalation Required

**Skill**: code-quality
**Error**: PERMISSION_DENIED
**Attempts**: 3

### Situation
Skill requires Edit permission to apply auto-fixes,
but is restricted to read-only tools.

### Options

1. **Use read-only mode** (recommended)
   - Get analysis without auto-fix
   - Manually apply recommended changes
   
2. **Use different skill**
   - `python-implementation` has Edit permission
   - May have different review criteria

3. **Override restriction** (requires confirmation)
   - Temporarily grant Edit permission
   - Higher risk, proceed with caution

### Your Decision
Please choose option 1, 2, or 3.
```

---

## Error Logging

### Log Format

```json
{
  "timestamp": "2025-01-15T10:30:00Z",
  "skill": "code-quality",
  "error_code": "EXEC_FAILED",
  "request_hash": "abc123",
  "context": {
    "files": ["auth.py", "handler.py"],
    "phase": "analysis"
  },
  "recovery_attempted": true,
  "recovery_success": false,
  "escalated": true
}
```

### Retention

- Error logs: 7 days
- Recovery attempts: 24 hours
- Escalations: 30 days

---

## See Also

- [Invocation Examples](invocation-examples.md)
- [SKILL.md](../SKILL.md) - Main skill documentation
- [Escalation Protocol](../../../docs/00-core/escalation-protocol.md)
