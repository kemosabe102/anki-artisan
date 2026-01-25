# Error Handling

Complete error scenarios and recovery strategies for the /tasks command.

---

## Step 1: Argument Parsing Errors

### Invalid Path
```
ERROR: "Invalid directory: [path]"

CAUSE: Path doesn't exist or isn't a directory

RECOVERY:
1. Show usage examples
2. Suggest valid paths

OUTPUT:
"Usage: /tasks path/to/feature/directory/

Examples:
  - /tasks docs/01-planning/features/005-regenerative-orchestration-system/
  - /tasks docs/01-planning/specifications/002-executable-task-system/"
```

### Path Outside Workspace
```
ERROR: "Path outside allowed workspace"

CAUSE: Path is outside docs/ or approved locations

RECOVERY:
1. Show allowed directories
2. Suggest moving files

OUTPUT:
"Feature directories should be in:
  - docs/01-planning/features/
  - docs/01-planning/specifications/"
```

---

## Step 2: Discovery Errors

### No Plan Files Found
```
ERROR: "No plan files discovered in ${FEATURE_DIR}"

CAUSE: No files matching plan patterns

RECOVERY:
1. List expected patterns
2. Suggest creating plan files

OUTPUT:
"Expected files matching:
  - plans/**/*.md
  - *plan*.md (case-insensitive)
  - phase-*.md
  - component-*.md

Suggestion: Create at least one plan file describing implementation steps"
```

### No Context Files Found
```
WARNING: "No feature context files found (SPEC.md, README.md, etc.)"

CAUSE: Missing context documentation

ACTION: Continue with plans only

OUTPUT:
"Will generate tasks from plan files only.
Quality impact: Tasks may lack broader feature context."
```

---

## Step 3: Synthesis Errors

### Synthesis Agent Fails
```
ERROR: researcher-codebase returns error or timeout

RECOVERY: Use fallback extraction

FALLBACK:
feature_name = basename(FEATURE_DIR)
feature_number = extract leading digits if present
feature_description = "Tasks generated from ${plan_count} plan files"
plan_structure = "parallel_components"  # Safest default
plans = map files to simple metadata:
  - file: relative path
  - name: filename without extension
  - component_name: sanitized filename
  - type: "core"
  - estimated_tasks: 15
  - depends_on: []
  - priority: "medium"
```

### Low Confidence Synthesis
```
WARNING: Synthesis confidence < 0.7

ACTION: 
1. Continue with synthesis results
2. Log warning for user
3. Suggest manual review of feature_metadata

OUTPUT:
"Feature synthesis confidence: 0.65
Recommend reviewing plan relationships before implementation."
```

---

## Step 4: Task Generation Errors

### Single Agent Failure
```
ERROR: One planning agent fails

RECOVERY:
1. Continue with successful agents
2. Report partial success
3. Provide failure details

OUTPUT:
"⚠️ Partial Success (2/3 plans succeeded)

Failed Plans:
- phase-2-integration.md
  Error: Invalid plan format - missing ## Implementation section
  Suggestion: Add implementation section with concrete steps"
```

### All Agents Fail
```
ERROR: All planning agents fail

RECOVERY:
1. Detailed error report per plan
2. Common issue detection
3. Recovery suggestions

OUTPUT:
"❌ Task Generation Failed

All 3 plans failed with similar errors:
- Common Issue: Plans missing required sections

For each plan, ensure:
1. ## Implementation section exists
2. Concrete steps with effort estimates
3. Clear dependencies between steps

Retry: Fix plan files and run /tasks again"
```

### Task ID Collision
```
ERROR: Duplicate task IDs detected

CAUSE: Offset calculation error or manual task file edits

RECOVERY:
1. Re-run with fresh offsets
2. Or manually renumber conflicting tasks

PREVENTION: 
- Always use calculated offsets (index * 100)
- Don't manually edit TASKS.json task IDs
```

---

## Step 5: Collection Errors

### Missing Output Files
```
ERROR: tasks.md or TASKS.json not found for successful agent

RECOVERY:
1. Mark as failure
2. Re-run single agent

OUTPUT:
"Agent reported success but output files missing.
Re-running task generation for: phase-0-foundation"
```

### Invalid TASKS.json
```
ERROR: TASKS.json fails schema validation

RECOVERY:
1. Log validation errors
2. Attempt auto-fix
3. Fall back to tasks.md parsing

OUTPUT:
"TASKS.json has schema errors:
- Missing 'dependencies' field on task T003
- Invalid 'effort' value on task T007

Attempting auto-repair..."
```

---

## Step 6: Validation Errors

### Validation Agent Timeout
```
ERROR: One validation agent times out

RECOVERY:
1. Continue with available results
2. Reduce weight for missing agent
3. Note incomplete validation

OUTPUT:
"Validation partial (2/3 core agents responded)
planning: timed out
Confidence reduced: 0.72 → 0.65"
```

### Critical Issues Detected
```
STATUS: BLOCKED

CAUSE: Validation found blocking issues

RECOVERY:
1. List critical issues
2. Suggest fixes
3. Don't proceed to /implement until resolved

OUTPUT:
"Validation Status: BLOCKED

Critical Issues (must fix):
1. Missing test tasks for auth module
2. Circular dependency: T003 → T007 → T003
3. No error handling tasks defined

Fix these issues before running /implement"
```

### High Priority Improvements
```
STATUS: APPROVED with suggestions

CAUSE: Validation found non-blocking improvements

ACTION: Present but don't block

OUTPUT:
"Validation Status: APPROVED (92%)

Suggested Improvements:
1. Consider adding performance test tasks
2. Documentation tasks could be more specific
3. Consider splitting large task T015

These are optional - proceed with /implement when ready"
```

---

## Graceful Degradation Philosophy

### Priority Order
1. **Continue if possible** - Partial results better than none
2. **Use fallbacks** - Simple extraction when synthesis fails
3. **Report clearly** - User knows what succeeded/failed
4. **Suggest recovery** - Actionable next steps

### Decision Matrix

| Scenario | Severity | Action |
|----------|----------|--------|
| No context files | Low | Continue, warn |
| 1 of N plans fail | Medium | Partial success |
| Synthesis fails | Medium | Use fallback |
| All plans fail | High | Error report |
| Validation blocks | High | List fixes, block |
| Critical issues | High | Require fixes |

### User Guidance Principles
- Clear error messages (what went wrong)
- Actionable suggestions (how to fix)
- Examples of correct usage
- Recovery paths (next steps)
