# Stage Definitions

Detailed definitions for each stage in the 7-stage auto-fix pipeline.

---

## Stage 1: DRY-RUN

**Purpose**: Simulate the operation without making any file changes.

### Actions
- Parse all target files that would be modified
- Validate paths exist and are writable
- Check schema compliance of inputs
- Simulate transformations in memory
- Calculate expected diffs

### Pass Criteria
- All target paths are valid
- All target files exist (for modifications)
- Parent directories exist (for creates)
- No permission issues detected
- Simulation completes without errors

### Failure Handling
- Return FAILURE immediately
- Include specific simulation error details
- List which paths/files caused issues
- Suggest remediation steps

### Output
```json
{
  "stage": "DRY_RUN",
  "status": "PASS|FAIL",
  "simulated_changes": [
    {"path": "...", "action": "create|update|delete", "preview": "..."}
  ],
  "issues": []
}
```

---

## Stage 2: SMOKE TEST

**Purpose**: Lightweight validation of paths, links, and syntax.

### Actions
- Validate all file path formats (forward slashes, absolute)
- Check internal link references exist
- Verify markdown syntax validity
- Confirm cross-references resolve
- Check for obvious errors (missing brackets, etc.)

### Validation Checks

| Check | Validation | Severity |
|-------|------------|----------|
| Path Format | Forward slashes only | Warning |
| Path Absolute | Starts with `/` or `C:/` | Warning |
| Link Target | Referenced file exists | Warning |
| Markdown Syntax | Parses without error | Warning |
| Frontmatter | Valid YAML | Warning |

### Pass Criteria
- All checks pass OR only warnings (no errors)
- Warnings are logged for AUTO-FIX stage

### Failure Handling
- Flag all issues found
- Continue to AUTO-FIX stage (warnings don't block)
- Hard errors block progression

### Output
```json
{
  "stage": "SMOKE_TEST",
  "status": "PASS|WARN|FAIL",
  "issues_found": [
    {"type": "path_format", "severity": "warning", "location": "...", "detail": "..."}
  ],
  "fixable_issues": ["issue_ids that AUTO-FIX can handle"]
}
```

---

## Stage 3: AUTO-FIX

**Purpose**: Automatically repair known issue patterns.

### Auto-Fix Patterns

| Pattern | Detection | Fix |
|---------|-----------|-----|
| Backslash Paths | `\\` in path strings | Replace with `/` |
| Relative Paths | Path not starting with `/` or drive | Prepend absolute base |
| Missing Newline | No `\n` at EOF | Append `\n` |
| Broken Links | Link target 404 | Update to correct path |
| Duplicate IDs | Same identifier twice | Dedupe, keep latest |
| Stale Timestamp | Older than file mtime | Update to current |
| Trailing Whitespace | Spaces at EOL | Strip whitespace |

### Actions
- Iterate through fixable issues from SMOKE
- Apply pattern-matched fixes
- Log each fix with before/after
- Track fix count and types

### Pass Criteria
- All fixable issues addressed
- Fix log populated
- No new issues introduced

### Constraints
- Only fix known patterns
- Unknown issues passed to VALIDATE
- Maximum 3 retry attempts total

### Output
```json
{
  "stage": "AUTO_FIX",
  "status": "APPLIED|NO_ACTION",
  "fixes_applied": [
    {
      "issue_id": "...",
      "pattern": "backslash_path",
      "location": "file.md:25",
      "before": "path\\to\\file",
      "after": "path/to/file"
    }
  ],
  "unfixable_issues": ["issues that need manual intervention"]
}
```

---

## Stage 4: VALIDATE

**Purpose**: Full validation against ecosystem standards.

### Validation Categories

#### Path Validation
- All paths use forward slashes
- All paths are absolute
- All referenced files exist
- No circular references

#### Schema Validation
- Frontmatter conforms to schema
- Required fields present
- Field types correct
- Enum values valid

#### Content Validation
- Markdown renders correctly
- Code blocks have language tags
- Tables are well-formed
- Lists properly nested

#### Integration Validation
- Cross-references resolve
- Agent-skill bindings valid
- Command-hook links work
- Registry entries accurate

### Pass Criteria

| Category | Required Pass Rate |
|----------|-------------------|
| Path Validation | 100% |
| Schema Validation | 100% |
| Content Validation | 95% |
| Integration Validation | 100% |

### Failure Handling
- If retry_count < 3: Return to AUTO-FIX
- If retry_count >= 3: Return FAILURE
- Log all validation failures with detail

### Output
```json
{
  "stage": "VALIDATE",
  "status": "PASS|FAIL",
  "retry_count": 0,
  "validation_results": {
    "path": {"passed": 10, "failed": 0},
    "schema": {"passed": 5, "failed": 0},
    "content": {"passed": 20, "failed": 1},
    "integration": {"passed": 8, "failed": 0}
  },
  "failures": [
    {"category": "content", "check": "table_format", "location": "...", "detail": "..."}
  ]
}
```

---

## Stage 5: APPLY

**Purpose**: Execute file modifications.

### Actions
- Create backup of target files (in-memory)
- Execute file operations in dependency order
- Use appropriate tool per operation:
  - New file: `write_file`
  - Small edit (<5 lines): `edit_block`
  - Large edit (>5 lines): `write_file` with chunks
- Track each operation result

### Operation Order
1. Delete operations first
2. Create operations second
3. Update operations last
4. Respect dependency graph

### Pass Criteria
- All file operations succeed
- No partial writes
- File system consistent

### Failure Handling
- On first failure: halt immediately
- Rollback all changes made in this stage
- Return FAILURE with operation that failed

### Output
```json
{
  "stage": "APPLY",
  "status": "SUCCESS|ROLLBACK",
  "operations_completed": [
    {"path": "...", "action": "create", "bytes_written": 1234}
  ],
  "rollback_performed": false,
  "failed_operation": null
}
```

---

## Stage 6: CHECK

**Purpose**: Read-back verification of applied changes.

### Actions
- Read each modified file
- Compare content to expected result
- Verify no corruption or truncation
- Confirm file permissions intact
- Check file timestamps updated

### Verification Checks

| Check | Method | Tolerance |
|-------|--------|-----------|
| Content Match | SHA256 hash | Exact |
| File Size | Byte count | +/- 10 bytes |
| Line Count | wc -l equivalent | Exact |
| Permissions | Mode check | Exact |

### Pass Criteria
- All content matches expected
- No file corruption detected
- No truncation detected

### Failure Handling
- On mismatch: Retry write operation once
- On second failure: Rollback and FAILURE
- Log detailed comparison

### Output
```json
{
  "stage": "CHECK",
  "status": "VERIFIED|MISMATCH",
  "verifications": [
    {
      "path": "...",
      "expected_hash": "sha256:...",
      "actual_hash": "sha256:...",
      "match": true
    }
  ],
  "retry_attempted": false
}
```

---

## Stage 7: FINAL VERIFY

**Purpose**: Integration testing of the ecosystem.

### Actions
- Verify cross-document links still work
- Check registry consistency
- Validate agent-skill bindings
- Test command-hook integrations
- Run ecosystem health scan

### Integration Tests

| Test | Description | Severity |
|------|-------------|----------|
| Link Resolution | All internal links resolve | Critical |
| Registry Accuracy | All entries up-to-date | Major |
| Binding Validity | Agent-skill connections work | Major |
| Hook Execution | Hooks can be invoked | Minor |

### Pass Criteria
- All critical tests pass
- Major tests: 100% pass
- Minor tests: 90% pass

### Failure Handling
- Report degradation details
- Do NOT rollback (changes are committed)
- Flag for manual review

### Output
```json
{
  "stage": "FINAL_VERIFY",
  "status": "PASS|DEGRADATION",
  "integration_tests": {
    "link_resolution": {"passed": 50, "failed": 0},
    "registry_accuracy": {"passed": 10, "failed": 0},
    "binding_validity": {"passed": 20, "failed": 0},
    "hook_execution": {"passed": 5, "failed": 1}
  },
  "degradation_details": [],
  "recommendations": []
}
```

---

## Stage Summary Table

| Stage | Purpose | Blocks Pipeline | Auto-Retry |
|-------|---------|-----------------|------------|
| 1. DRY-RUN | Simulate | Yes | No |
| 2. SMOKE | Quick validate | No (warnings) | No |
| 3. AUTO-FIX | Repair known | No | Yes (3x) |
| 4. VALIDATE | Full check | Yes | Via AUTO-FIX |
| 5. APPLY | Execute | Yes | No |
| 6. CHECK | Read-back | Yes | Once |
| 7. VERIFY | Integration | No (report) | No |

---

## Common Failure Patterns

| Symptom | Likely Stage | Common Cause | Resolution |
|---------|--------------|--------------|------------|
| "Path not found" | DRY-RUN | Missing target file | Verify paths exist |
| "Invalid format" | SMOKE | Path format issues | Let AUTO-FIX repair |
| "Schema violation" | VALIDATE | Missing required field | Add field to content |
| "Write failed" | APPLY | Permission issue | Check file permissions |
| "Content mismatch" | CHECK | Partial write | Retry or chunk smaller |
| "Link broken" | VERIFY | Changed file location | Update references |

