# Agent Architect Delegation Examples

## Example 1: Create New Agent

**Orchestrator Request**:
```
Task(agent-architect,
  "Create a new agent for managing test datasets. The agent should:
   - Generate validation datasets from git history
   - Apply domain heuristics for simulated expert ground truth
   - Create Pydantic-validated JSON
   Purpose: Algorithm validation testing.")
```

**Expected Output**:
- New directory: `.claude/agents/dev-tools/test-dataset-creator/`
- Main definition file with streamlined structure
- Schema file extending base-agent.schema.json
- Documentation in docs/ subdirectory
- CLAUDE.md Complete Agent List updated

---

## Example 2: Evaluate Agent Quality

**Orchestrator Request**:
```
Task(agent-architect,
  "Evaluate the python-code-reviewer agent for quality compliance.
   Check: description-capability alignment, frontmatter validity,
   progressive disclosure compliance, framework alignment.")
```

**Expected Output**:
```json
{
  "status": "SUCCESS",
  "evaluation": {
    "overall_score": 4.2,
    "grade": "B",
    "criteria_scores": {
      "correctness": {"score": 4.5, "weight": 0.25},
      "description_alignment": {"score": 4.0, "weight": 0.10},
      ...
    }
  },
  "recommendations": {
    "priority_improvements": [
      "Reduce description length from 220 to <200 chars",
      "Add explicit NOT-for cases in description"
    ]
  }
}
```

---

## Example 3: Implement Feedback

**Orchestrator Request**:
```
Task(agent-architect,
  "Update the debugger agent to include circuit breaker pattern
   for repeated failures. Add max 3 retry attempts with exponential
   backoff before escalating to orchestrator.")
```

**Expected Output**:
- Agent definition updated in place
- Changes documented with rationale
- Self-evaluation applied post-change
- Version increment recommendation provided

---

## Example 4: Analyze Agent Idea

**Orchestrator Request**:
```
Task(agent-architect,
  "Analyze this agent idea: 'I want an agent that can automatically
   detect when our documentation is out of sync with the codebase
   and suggest updates.'
   
   Generate a structured proposal with confidence-scored recommendations.")
```

**Expected Output**:
- name_options: ["doc-sync-analyzer", "doc-drift-detector"] with confidence scores
- domain_scope: `.claude/docs/**`, `packages/**` (read), `.claude/docs/**` (write)
- agent_type: Analyzer (confidence 0.85)
- purpose_statement, capabilities, expected inputs/outputs
- tool_recommendations with rationale
- integration_points (coordinates with doc-librarian, researcher-codebase)

---

## When NOT to Use agent-architect

| Request | Correct Agent | Reason |
|---------|---------------|--------|
| "Fix the authentication bug" | debugger | Code debugging, not agent definition |
| "Review this PR for quality" | python-code-reviewer | Code review, not agent evaluation |
| "Update the SPEC.md" | /spec command | Specification management |
| "Create project documentation" | doc-librarian | Documentation, not agents |
