# Evaluation Examples

Good vs bad examples for 7 mandatory agent workflow patterns.

---

## P1: Mode Detection Table

### GOOD Example

```markdown
| Mode | Trigger Keywords | Entry Condition |
|------|------------------|-----------------|
| ANALYZE | "review", "check", "audit", "assess" | Default entry point |
| FIX | "fix", "repair", "resolve", "correct" | Issue identified |
| GENERATE | "create", "generate", "write", "produce" | Template/output needed |
| VALIDATE | "verify", "confirm", "test", "ensure" | Post-action check |
```

### BAD Example

```markdown
The agent detects modes based on what the user wants.
- Analysis mode: when analyzing
- Fix mode: when fixing things
- Other modes as needed
```

**Why BAD**: No specific keywords, vague conditions, missing table structure.

---

## P2: OODA Workflow (All 4 Phases)

### GOOD Example

```markdown
## OODA Workflow

### OBSERVE
- Parse user request for task type and scope
- Glob for relevant files: `**/*.py`, `**/*.md`
- Read configuration files for context

### ORIENT
- Calculate complexity score (files * avg_lines / 1000)
- Identify dependencies and blockers
- Assess risk: LOW (<10 files), MEDIUM (10-50), HIGH (>50)

### DECIDE
- Select tools based on task type
- Plan execution order (parallel vs sequential)
- Set success criteria and rollback triggers

### ACT
- Execute plan via tool calls
- Track progress with TodoWrite
- Validate outputs against criteria
```

### BAD Example

```markdown
## Workflow
1. Look at the request
2. Figure out what to do
3. Do it
4. Check if it worked
```

**Why BAD**: Missing OODA labels, no specific actions, no tools or criteria.

---

## P3: Mode-Specific Sections

### GOOD Example

```markdown
## Mode: ANALYZE

**Entry**: Default mode, triggered by audit/review requests
**Tools**: Read, Grep, Glob (read-only)
**Output**: Analysis report with findings and severity

### Workflow
1. Scope validation (reject paths outside boundary)
2. File discovery via Glob
3. Pattern matching via Grep
4. Severity classification (P1-P4)

## Mode: FIX

**Entry**: From ANALYZE when issues found, or direct "fix" request
**Tools**: edit_block, write_file (with approval gate)
**Output**: Modified files with change summary

### Workflow
1. Confirm fix scope with user (if >5 files)
2. Apply changes smallest-to-largest
3. Validate each change before proceeding
```

### BAD Example

```markdown
## How It Works
The agent analyzes things and fixes them when needed.
It uses various tools depending on the situation.
```

**Why BAD**: No mode separation, no entry/exit criteria, no tool restrictions.

---

## P4: Anti-Patterns Section

### GOOD Example

```markdown
## Anti-Patterns

| Pattern | Why It Fails | Correct Approach |
|---------|--------------|------------------|
| Editing without reading | Blind changes cause regressions | Read target file first |
| Skipping validation | Silent failures propagate | Always run post-edit checks |
| Unbounded scope | Context overflow, slow execution | Limit to 10 files per batch |
| Direct git commands | Security hooks may block | Use source-control agent |
```

### BAD Example

```markdown
## Things to Avoid
- Don't do bad things
- Be careful with files
- Make sure it works
```

**Why BAD**: No specific patterns, no explanations, no correct alternatives.

---

## P5: Ask-First Rules

### GOOD Example

```markdown
## Ask-First Rules

**STOP and ask user ONLY if:**

| Condition | Why | Example Prompt |
|-----------|-----|----------------|
| Destructive operation | Irreversible | "Delete 15 files? [y/n]" |
| Scope > 20 files | Resource intensive | "Found 47 files. Proceed?" |
| Confidence < 0.70 | Uncertain outcome | "Ambiguous request. Did you mean X or Y?" |
| Cross-boundary access | Security | "This requires access to /etc. Approve?" |

**Proceed WITHOUT asking for:**
- Read-only operations
- Single-file edits within scope
- Standard formatting/linting
```

### BAD Example

```markdown
## Asking Permission
Ask the user before doing anything important.
Use your judgment about what's important.
```

**Why BAD**: No specific conditions, subjective criteria, no proceed-without list.

---

## P6: Output Structure (SUCCESS/FAILURE JSON)

### GOOD Example

```markdown
## Output Format

All operations return structured JSON:

### Success
```json
{
  "status": "SUCCESS",
  "mode": "ANALYZE",
  "findings": [
    {"file": "src/main.py", "line": 42, "severity": "P2", "message": "Unused import"}
  ],
  "metrics": {"files_scanned": 15, "issues_found": 3, "duration_ms": 1200}
}
```

### Failure
```json
{
  "status": "FAILURE",
  "mode": "FIX",
  "error": "Permission denied: /etc/config.yml",
  "partial_results": {"files_fixed": 2, "files_failed": 1},
  "recovery": "Run with elevated permissions or exclude /etc/"
}
```
```

### BAD Example

```markdown
## Output
Returns results of the operation.
Success means it worked, failure means it didn't.
```

**Why BAD**: No schema, no examples, no error handling structure.

---

## P7: Role & Boundaries

### GOOD Example

```markdown
## Role & Boundaries

| Aspect | In Scope | Out of Scope |
|--------|----------|--------------|
| **Files** | `src/**`, `tests/**` | `node_modules/`, `.git/` |
| **Operations** | Read, Lint, Format, Test | Deploy, Publish, Delete |
| **Decisions** | Code style, test coverage | Architecture, dependencies |

### Escalation Triggers
- Request involves production deployment → Escalate to `deployment` agent
- Request requires new dependency → Escalate to `dependency-manager`
- Request outside file scope → Reject with explanation

### Integration Points
- **Upstream**: Receives tasks from `orchestrator`, `code-quality`
- **Downstream**: Delegates to `test-runner`, `formatter`
```

### BAD Example

```markdown
## What This Agent Does
This agent helps with code stuff.
It works on files in the project.
Ask another agent if you need something else.
```

**Why BAD**: No specific boundaries, no scope table, no escalation criteria.

---

## Summary Checklist

| Pattern | Key Elements |
|---------|--------------|
| P1 | Table with keywords + conditions |
| P2 | Four labeled OODA phases with actions |
| P3 | Separate sections per mode with tools |
| P4 | Table: pattern / why fails / correct |
| P5 | Conditions table + proceed-without list |
| P6 | JSON schema for SUCCESS and FAILURE |
| P7 | Scope table + escalation + integration |
