# Phase 4: ACT - Execution and Validation

**OODA Stage**: ACT | **Time Allocation**: 50-55%

**Purpose**: Execute planned tasks, validate outputs, apply auto-fix pipeline, generate final output

**Deliverable**: Completed operation with SUCCESS/FAILURE status, validation evidence, provenance

---

## 7-Stage Auto-Fix Pipeline

All file-modifying operations pass through this validation pipeline:

| Stage | Action | On Failure |
|-------|--------|------------|
| 1. DRY-RUN | Simulate operation without file changes | Report simulation issues |
| 2. SMOKE TEST | Lightweight validation (paths, links, syntax) | Flag issues, continue |
| 3. AUTO-FIX | Automatic repair of known patterns | Log fixes applied |
| 4. VALIDATE | Full validation against Claude Code standards | Block if critical |
| 5. APPLY | Execute file modifications | Rollback on error |
| 6. CHECK | Read-back verification | Retry or rollback |
| 7. FINAL VERIFY | Integration testing | Report degradation |

**Retry Limit**: 3 attempts per validation failure before FAILURE status


---

## Execution Steps

### Step 4.1: Execute Tasks

**Input**: Approved plan from Phase 3

**Process**:
1. Execute tasks in dependency order
2. Use appropriate file operation tool (edit_block for surgical, write_file for new)
3. Mark each task complete after execution
4. Halt on blocking errors

**File Operation Selection**:

| Scenario | Tool | Rationale |
|----------|------|-----------|
| New file | `mcp__desktop-commander__write_file` | Create from scratch |
| Small edit (<5 lines) | `mcp__desktop-commander__edit_block` | Surgical precision |
| Large edit (>5 lines) | `mcp__desktop-commander__write_file` | Chunk writes |
| Multiple edits same file | Sequential `edit_block` | Maintain consistency |

**Output**: Executed tasks with status

### Step 4.2: Validate Outputs

**Input**: Modified files/artifacts

**Validation Checks**:
- Path normalization compliance (forward slashes, absolute paths)
- File reference accuracy (all referenced files exist)
- Link verification (internal documentation links resolve)
- Markdown syntax validation
- Claude Code alignment (slash command syntax, agent references)
- Schema compliance (output validates against workflow.schema.json)

**Output**: Validation report with pass/fail per check


### Step 4.3: Apply Auto-Fix (if needed)

**Input**: Validation failures

**Auto-Fix Patterns**:

| Issue | Auto-Fix |
|-------|----------|
| Backslash paths | Convert to forward slashes |
| Relative paths | Convert to absolute |
| Missing newlines | Add trailing newline |
| Broken internal links | Update to correct path |

**Output**: Fixed artifacts with fix log

### Step 4.4: Read-Back Verification

**Input**: Modified files

**Process**:
1. Read each modified file
2. Verify content matches intent
3. Check for corruption or truncation
4. Confirm file permissions intact

**Output**: Read-back confirmation

---

## Output Generation

### Step 4.5: Generate Final Output

**SUCCESS Output Structure**:
```json
{
  "status": "SUCCESS",
  "agent": "workflow",
  "task_id": "ulid-or-uuid",
  "operation_type": "build_workflow",
  "summary": "Created new slash command /analyze with hook integration",
  "validation_checklist": {
    "checks_performed": ["path_validation", "syntax_check", "integration_test"],
    "all_checks_passed": true,
    "check_details": [...]
  },
  "success_evidence": {
    "operation_result": {...},
    "provenance": {
      "operation_id": "01HXYZ...",
      "inputs_hash": "sha256...",
      "apply_mode": "commit",
      "processing_time_ms": 1234
    },
    "validation_results": {...},
    "changes": [{"path": "...", "action": "create", "summary": "..."}],
    "next_actions": ["Run session restart to load new command"]
  },
  "confidence": 0.95,
  "severity": "Minor",
  "execution_timestamp": "2024-01-15T10:30:00Z"
}
```

**FAILURE Output Structure**:
```json
{
  "status": "FAILURE",
  "agent": "workflow",
  "task_id": "ulid-or-uuid",
  "operation_type": "build_workflow",
  "summary": "Failed to create slash command due to missing tool permissions",
  "validation_checklist": {
    "checks_performed": ["path_validation", "syntax_check"],
    "all_checks_passed": false,
    "failed_checks": [{"check_name": "tool_permissions", "status": "failed", "reason": "..."}]
  },
  "failure_details": {
    "failure_type": "validation_error",
    "reasons": ["Tool X not in allowed list"],
    "missing": ["Tool X permission"],
    "proposed_next_steps": ["Add Tool X to allowed_tools in frontmatter"],
    "recovery_suggestions": [...]
  },
  "confidence": 0.85,
  "severity": "Major",
  "execution_timestamp": "2024-01-15T10:30:00Z"
}
```

---

## Quick Checklist

Before marking complete:

- [ ] All planned tasks executed
- [ ] 7-stage validation pipeline passed
- [ ] Read-back verification confirmed
- [ ] Output matches schema
- [ ] Provenance documented
- [ ] Next actions listed

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping validation | Always run 7-stage pipeline |
| Parallel file edits | Execute file modifications sequentially |
| No read-back | Verify every write operation |
| Missing provenance | Always include operation_id, inputs_hash |
| Incomplete output | Use full SUCCESS/FAILURE structure |

---

## Termination Rules

- **Operation timeout**: 600 seconds maximum
- **Auto-fix retry limit**: 3 attempts per validation failure
- **CQ iteration limit**: 3 research cycles before FAILURE

---

## Exit Criteria

**All criteria must pass to return SUCCESS**

| Criterion | Weight | Check |
|-----------|--------|-------|
| Tasks executed | 0.25 | All planned steps finished |
| Validation passed | 0.30 | 7-stage pipeline green |
| Read-back confirmed | 0.15 | All writes verified |
| Schema compliant | 0.15 | Output validates |
| Provenance complete | 0.10 | operation_id, hash, timestamp |
| Next actions listed | 0.05 | Actionable follow-ups |

---

## Reference Documentation

- [workflow.schema.json](../schemas/workflow.schema.json) - Output schema contract
- [workflow-operations.md](../docs/workflow-operations.md) - Operation-specific validation
- [file-operation-protocol.md](../../../../docs/01-guides/file-ops/file-operation-protocol.md) - File ops

---

**Previous Phase**: [Phase 3: DECIDE](phase-3-decide.md)
**Complete**: Return to [workflow.md](../workflow.md)
