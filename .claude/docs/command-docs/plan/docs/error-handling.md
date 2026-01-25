# Error Handling for /plan Command

Complete error scenarios and recovery strategies for the planning workflow.

---

## Phase 1: Input Validation Errors

### SPEC.md Not Found

**Symptoms:**
- File path doesn't exist
- File is empty or corrupted

**Recovery:**
```
1. Verify path is correct: ls {provided_path}
2. If not found: "SPEC.md not found at {path}. Please provide valid path or run /spec first."
3. If empty: "SPEC.md exists but is empty. Run /spec to generate specification."
```

### Invalid SPEC.md Structure

**Symptoms:**
- Missing required sections (Business Goals, Requirements, etc.)
- No FR-IDs defined
- Incomplete specification

**Recovery:**
```
1. Validate structure: Check for ## headers matching spec template
2. If missing sections: "SPEC.md is incomplete. Missing: {sections}. Run /spec to regenerate."
3. If no FR-IDs: "No FR-IDs found. Requirements must be tagged (e.g., FR-001)."
```

---

## Phase 2: SPEC Validation & Component Analysis Errors

### planning Fails

**Symptoms:**
- Agent returns error status or FAIL validation
- Missing required sections identified
- Completeness score < 70

**Recovery:**
```
1. Review planning issues[] output for specific problems
2. If missing sections: "SPEC.md incomplete. Missing: {sections}. Run /spec to regenerate."
3. If FR-ID format issues: "FR-IDs must follow FR-XXX pattern (e.g., FR-001)"
4. If completeness < 70: Suggest running /spec with enhanced context
```

### feature-analyzer Fails

**Symptoms:**
- Agent returns error status
- No components identified
- Timeout

**Recovery:**
```
1. Check SPEC.md complexity: Is it too large? (>500 lines)
2. Verify planning passed (feature-analyzer needs valid SPEC)
3. Retry with enhanced context: Add explicit domain hints
4. Fallback: Create single monolithic plan if spec is simple
```

### Ambiguous Component Boundaries

**Symptoms:**
- Overlapping requirements across components
- Unclear domain separation

**Recovery:**
```
1. Review feature-analyzer rationale and dependencies[]
2. Ask user for clarification on component boundaries
3. Merge ambiguous components if separation isn't clear
```

### Two-Agent Coordination Failure

**Symptoms:**
- One agent succeeds, other fails
- Inconsistent outputs between agents

**Recovery:**
```
1. If planning FAIL: Do not proceed with feature-analyzer output
2. If feature-analyzer FAIL but planning PASS: Retry feature-analyzer only
3. If outputs conflict: Prioritize planning validation status
```

---

## Phase 3: File Creation Errors

### Template Script Fails

**Symptoms:**
- `create-plan-from-template.py` returns error
- Files not created
- Permission denied

**Recovery:**
```
1. Check script exists: ls scripts/planning/create-plan-from-template.py
2. Check Python environment: uv run python --version
3. Check output directory permissions: ls -la {output_dir}
4. Create directory if missing: mkdir -p {output_dir}
5. Retry: uv run python scripts/planning/create-plan-from-template.py ...
```

---

## Phase 4: Enhancement Pipeline Errors

### planning Fails (Per File)

**Symptoms:**
- Business sections not populated
- Agent timeout
- Partial completion

**Recovery:**
```
1. Check which file failed (other pipelines should complete)
2. Verify SPEC.md is accessible
3. Retry single file: Task(planning, failed_file_path)
4. If repeated failure: Manual business section population
```


### architecture Fails (Per File)

**Symptoms:**
- Technical sections not populated
- Implementation Plan incomplete
- Placeholders remain

**Recovery:**
```
1. Check which file failed
2. Verify planning completed for this file first
3. Retry single file: Task(architecture, failed_file_path)
4. If Context7 unavailable: Use WebSearch for technical research
5. If repeated failure: Flag for manual technical review
```

### File Conflict Errors

**Symptoms:**
- "File was modified by another process"
- Merge conflicts in plan file

**Prevention:**
- This should NOT happen with parallel-by-file strategy
- If it does: Check that pipelines are truly separated by file

**Recovery:**
```
1. Stash current changes: git stash
2. Re-run enhancement pipeline for that file only
3. Verify no concurrent modifications
4. Apply stash if needed: git stash pop
```

**WARNING**: Do NOT use `git checkout {file}` - this is a BANNED operation that destroys uncommitted work. Use `git stash` instead to preserve changes.

---

## Phase 5: Task-Creator Readiness Errors

### FAIL Status

**Symptoms:**
- >5 placeholders in Implementation Plan
- <2 phases defined
- Missing Implementation Plan section entirely

**Recovery:**
```
1. Identify failing files from validation output
2. Re-run architecture with enhanced scope:
   Task(architecture, {
     plan_file_path: {failed_file},
     enhanced_scope: "implementation_detail"
   })
3. If still failing: Manual Implementation Plan population
```


---

## Phase 6: Architecture Review Errors

### Score Below Threshold

**Symptoms:**
- Architecture score < 3.5 (WARN)
- Architecture score < 3.0 (BLOCK)

**Recovery:**
```
Score 3.0-3.5 (WARN):
1. Review recommendations from architectureer
2. Present to user with option to proceed or refine
3. Document accepted technical debt

Score < 3.0 (BLOCK):
1. Review critical issues from architectureer
2. Address blocking issues before proceeding
3. Options:
   - Simplify architecture
   - Add missing components
   - Re-run spec phase for clearer requirements
```

### architectureer Agent Failure

**Symptoms:**
- Agent returns error status
- Timeout during validation
- Incomplete validation report

**Recovery:**
```
1. Check plan file count: Too many plans may cause timeout
2. Retry with subset: Validate plans in batches of 3-5
3. If repeated failure: Manual architecture review checklist
4. Verify Context7/research tools available for technical validation
```

### Integration Analysis Failures

**Symptoms:**
- Missing cross-component integrations
- Circular dependencies detected
- Unresolved external dependencies

**Recovery:**
```
1. Review integration_analysis output from architectureer
2. Missing integrations: Add integration points to affected plans
3. Circular dependencies: Refactor component boundaries
4. External dependencies: Document and validate availability
```

---

## General Recovery Strategies

### Skip Flags (HIGH RISK)

| Flag | Effect | Use When |
|------|--------|----------|
| `--mode=quick` | Skip human review | Trusted workflow, time-critical |
| `--skip-validation` | Skip Phase 1 | SPEC already validated manually |

### Manual Fallback

If automated workflow fails repeatedly:
1. Create plan files manually from template
2. Populate sections by reading SPEC.md
3. Skip to architectureer for validation
4. Document manual intervention
