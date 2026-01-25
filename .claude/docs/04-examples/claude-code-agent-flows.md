# Claude Code Agent Execution Examples

## Success Flow Example

**Task**: Update agent model from `sonnet` to `sonnet` for complex reasoning tasks

**Flow**:

1. **Research**: Load `.claude/agents/planner-agent.md`, WebFetch model config documentation
2. **Plan**: Update model field, validate tool set compatibility, check existing patterns
3. **Patch**: Edit `.claude/agents/planner-agent.md` model field `sonnet → sonnet`
4. **Validate**: Schema check passes, security validation passes, performance acceptable
5. **Deliver**: Return SUCCESS with summary and detailed report

**Output**:

```json
{
  "status": "SUCCESS",
  "agent": "claude-code-agent",
  "task_id": "update-planner-model",
  "summary": "Updated planner-agent model from sonnet to sonnet for enhanced reasoning capability",
  "report_path": ".claude/docs/reports/2025-09-20-163000-claude-code-agent-update-planner-model.md",
  "changes": [{ "path": ".claude/agents/planner-agent.md", "action": "update" }],
  "recommendations": ["Monitor token usage increase", "Consider performance impact"],
  "validation_proposal": [
    "Verify model field changed from 'sonnet' to 'sonnet' in planner-agent.md",
    "Check agent still has compatible tools for sonnet model",
    "Test planner-agent functionality with sonnet model before commit",
    "Monitor token consumption in next few uses"
  ],
  "sources": ["https://docs.claude.com/en/docs/claude-code/model-config"],
  "confidence": 0.95,
  "severity": "Minor"
}
```

## Clarification Flow Example

**Task**: "Create new output style" with insufficient parameters

**Flow**:

1. **Research**: Load output style documentation, check existing patterns
2. **Plan**: Identify missing required parameters (style name, renderers, use cases)
3. **Block**: Cannot proceed without essential information

**Output**:

```json
{
  "status": "NEEDS_CLARIFICATION",
  "agent": "claude-code-agent",
  "task_id": "create-output-style",
  "reasons": ["Insufficient parameters for output style creation"],
  "missing": ["style_name", "target_renderers", "use_case_description", "model_selection"],
  "proposed_next_steps": [
    "Specify unique style name (kebab-case)",
    "Define target use case (planner/development/reviewer)",
    "Choose appropriate model (sonnet/sonnet)",
    "Provide example interaction pattern"
  ],
  "sources": ["https://docs.claude.com/en/docs/claude-code/model-config"],
  "confidence": 0.2,
  "severity": "Major"
}
```
