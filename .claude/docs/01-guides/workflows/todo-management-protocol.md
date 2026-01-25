# Todo Management Protocol

**Purpose**: Standardized todo/task tracking for agent workflows
**Last Updated**: 2025-11-21
**Applies To**: All agents with multi-step operations (3+ steps)

---

## When to Use

**Triggers**:
- Tasks with **3+ distinct steps**
- Operations with **potential blocking dependencies**
- Workflows requiring **progress tracking for orchestrator**
- Complex operations spanning **multiple files or domains**

**Don't Use For**:
- Simple 1-2 step operations
- Fully automated sequential workflows with no branches
- Read-only analysis with no state changes

---

## Todo Structure

```json
{
  "todo_items": [
    {
      "id": "step_1",
      "description": "Clear, actionable step description",
      "completion_criteria": "Specific validation criteria (what defines 'done')",
      "dependencies": ["prerequisite_step_ids"],
      "status": "pending|in_progress|blocked|completed",
      "blocking_issue": "Description if status=blocked (why can't proceed)"
    }
  ],
  "unclear_items": [
    {
      "id": "unclear_1",
      "description": "Ambiguous requirement or missing context",
      "impact": "How this affects workflow execution",
      "resolution_needed": "Specific information or clarification required"
    }
  ]
}
```

---

## Status Lifecycle

```
pending → in_progress → completed
   ↓
blocked (with blocking_issue) → pending (after unblock)
```

**Status Definitions**:
- **pending**: Ready to start, dependencies met
- **in_progress**: Currently executing
- **blocked**: Cannot proceed, awaiting external input/fix
- **completed**: Validation criteria met, step finished

---

## Creation Timing

**Phase**: During **Analysis** phase, after task breakdown

**Process**:
1. Parse user request and context
2. Break down into discrete steps (each with clear completion criteria)
3. Identify dependencies between steps
4. Detect unclear items that may block progress
5. Generate todo structure
6. Return in Analysis phase output

---

## Completion Criteria

Each todo item MUST have **specific, measurable completion criteria**:

✅ **Good Criteria**:
- "File `packages/auth/jwt.py` created with 3 functions (generate, validate, decode)"
- "All 15 TODO comments resolved or converted to GitHub issues"
- "Test coverage ≥80% for new authentication module"

❌ **Bad Criteria**:
- "Implement authentication" (too vague)
- "Fix bugs" (unmeasurable)
- "Make it better" (subjective)

---

## Unclear Items Handling

**Purpose**: Track ambiguities that may require clarification or research

**When to Add**:
- Requirements unclear or conflicting
- Missing critical context (integration points, dependencies)
- Multiple valid interpretations possible
- External dependencies with unknown status

**Resolution Process**:
1. Document unclear item during Analysis
2. Attempt resolution during Research phase (consult guides, Context7, etc.)
3. If resolvable: Remove from unclear_items, proceed with assumption documented
4. If unresolvable: Return FAILURE with unclear items in output, escalate to orchestrator

---

## Example Workflows

### Example 1: Simple Implementation (3 steps)

```json
{
  "todo_items": [
    {
      "id": "step_1",
      "description": "Read existing authentication patterns in packages/auth/",
      "completion_criteria": "3+ existing auth files read, pattern analysis complete",
      "dependencies": [],
      "status": "completed"
    },
    {
      "id": "step_2",
      "description": "Implement JWT token generation function",
      "completion_criteria": "Function generate_jwt() created, unit test passing",
      "dependencies": ["step_1"],
      "status": "in_progress"
    },
    {
      "id": "step_3",
      "description": "Validate implementation against security standards",
      "completion_criteria": "SAST scan passed, no vulnerabilities found",
      "dependencies": ["step_2"],
      "status": "pending"
    }
  ],
  "unclear_items": []
}
```

### Example 2: Complex Workflow with Blocking

```json
{
  "todo_items": [
    {
      "id": "step_1",
      "description": "Research library API compatibility",
      "completion_criteria": "Context7 search complete, compatibility matrix documented",
      "dependencies": [],
      "status": "completed"
    },
    {
      "id": "step_2",
      "description": "Implement database migration",
      "completion_criteria": "Migration file created, tested on dev database",
      "dependencies": ["step_1"],
      "status": "blocked",
      "blocking_issue": "Dev database credentials unavailable (unclear_1)"
    },
    {
      "id": "step_3",
      "description": "Update ORM models",
      "completion_criteria": "5 models updated, schema validated",
      "dependencies": ["step_2"],
      "status": "pending"
    }
  ],
  "unclear_items": [
    {
      "id": "unclear_1",
      "description": "Development database connection string not found in .env or config",
      "impact": "Cannot test migration (step_2 blocked)",
      "resolution_needed": "Database credentials or permission to create local test DB"
    }
  ]
}
```

---

## Integration with Workflows

**Analysis Phase**:
- Generate todo structure
- Identify unclear items
- Output in analysis_results

**Implementation Phase**:
- Update todo status (pending → in_progress → completed)
- Document blocking issues
- Attempt unclear item resolution

**Validation Phase**:
- Verify all todos completed or properly escalated
- Check completion criteria met
- Include todo summary in SUCCESS/FAILURE output

**Reflection Phase**:
- Analyze todo accuracy (were estimates correct?)
- Document lessons learned about task breakdown
- Recommend process improvements

---

## Best Practices

1. **Granular steps**: Each todo = 1 discrete action with clear outcome
2. **Explicit dependencies**: Document all prerequisites to enable parallel execution
3. **Measurable criteria**: Avoid subjective or vague completion criteria
4. **Early unclear detection**: Flag ambiguities during Analysis, not Implementation
5. **Status hygiene**: Update status immediately (don't batch updates)
6. **Blocking transparency**: Document blocking issues clearly for orchestrator escalation

---

**Reference**: Used by all agents extending base-agent-pattern.md in Analysis → Research → Todo → Implementation → Validation → Reflection workflow
