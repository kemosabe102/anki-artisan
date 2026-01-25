# Delegation Examples for {{Agent Name}}

**Purpose**: Show orchestrator and other agents how to delegate tasks to this agent

**Standard Delegation Patterns**: See `.claude/docs/03-workflows/orchestrator-workflow.md` for generic Task() syntax and multi-agent coordination patterns. This file documents agent-SPECIFIC delegation.

---

## When to Delegate to This Agent

### Trigger Conditions

Delegate to `{{agent-name}}` when:
- {{Condition 1 - e.g., "User requests code review for Python files"}}
- {{Condition 2 - e.g., "Security vulnerabilities need assessment"}}
- {{Condition 3 - e.g., "Pre-commit quality gate required"}}

### NOT This Agent

Do NOT delegate when:
- {{Exclusion 1 - e.g., "Implementation needed"}} → Use `{{alternative-agent - e.g., development}}` instead
- {{Exclusion 2 - e.g., "Test creation needed"}} → Use `{{alternative-agent - e.g., code-quality}}` instead
- {{Exclusion 3 - e.g., "Debugging required"}} → Use `debugger` instead

---

## Basic Delegation Pattern

### Example (from code-quality)

**Orchestrator says**:
```
Task(code-quality, "Review packages/auth/oauth.py for security vulnerabilities. Focus on token handling, session management, and input validation.")
```

### Template

**Orchestrator says**:
```
Task({{agent-name}}, "{{Clear objective statement - be specific about files, focus areas, and expected output}}")
```

**Agent receives**:
- Task objective
- Implicit context from conversation

**Agent returns** (success example):
```json
{
  "status": "SUCCESS",
  "agent": "code-quality",
  "confidence": 0.87,
  "agent_specific_output": {
    "files_reviewed": ["packages/auth/oauth.py"],
    "findings": [
      {"severity": "HIGH", "line": 42, "issue": "SQL injection risk"}
    ],
    "summary": "1 critical, 2 minor issues found"
  }
}
```

**Agent returns** (template):
```json
{
  "status": "SUCCESS",
  "agent": "{{agent-name}}",
  "confidence": 0.9,
  "agent_specific_output": {
    "{{output_field_1}}": "{{value}}",
    "{{output_field_2}}": "{{value}}"
  }
}
```

---

## Complex Delegation Pattern

### Task with Context

**Orchestrator says**:
```
Task({{agent-name}}, "{{Objective}}.
Context: {{relevant background}}.
Constraints: {{limitations or requirements}}.
Output format: {{specific format request}}.")
```

**Required context fields**:
- `{{field_1}}`: {{Description}}
- `{{field_2}}`: {{Description}}
- `{{field_3}}`: {{Description}} (optional)

**Agent returns** (success example):
```json
{
  "status": "SUCCESS",
  "agent": "code-quality",
  "confidence": 0.85,
  "agent_specific_output": {
    "files_reviewed": ["packages/auth/oauth.py", "packages/auth/session.py"],
    "findings": [
      {"severity": "HIGH", "line": 42, "issue": "SQL injection risk in query builder"},
      {"severity": "MEDIUM", "line": 78, "issue": "Session timeout too long (24h)"},
      {"severity": "LOW", "line": 95, "issue": "Magic number should be constant"}
    ],
    "recommendations": [
      "Use parameterized queries",
      "Reduce session timeout to 1h",
      "Extract timeout values to config"
    ]
  }
}
```

**Agent returns** (template):
```json
{
  "status": "SUCCESS",
  "agent": "{{agent-name}}",
  "confidence": 0.85,
  "agent_specific_output": {
    "{{primary_output}}": { ... },
    "{{secondary_output}}": [ ... ],
    "recommendations": [ ... ]
  }
}
```

**Agent returns** (failure example):
```json
{
  "status": "FAILURE",
  "agent": "code-quality",
  "confidence": 0.3,
  "failure_details": {
    "failure_type": "insufficient_context",
    "reasons": ["File not found: packages/auth/oauth.py", "No Python files in specified path"],
    "recovery_suggestions": ["Verify file path exists", "Check if path uses correct case sensitivity"]
  }
}
```

**Agent returns** (failure template):
```json
{
  "status": "FAILURE",
  "agent": "{{agent-name}}",
  "confidence": 0.3,
  "failure_details": {
    "failure_type": "{{failure_category}}",
    "reasons": ["{{reason_1}}", "{{reason_2}}"],
    "recovery_suggestions": ["{{suggestion_1}}", "{{suggestion_2}}"]
  }
}
```

---

## Context Metadata (Required for Complex Tasks)

When delegating complex tasks, include structured context:

### Example Context Block

```yaml
context:
  files_to_analyze:
    - packages/auth/oauth.py
    - packages/auth/session.py
  focus_areas:
    - security
    - performance
  constraints:
    - no_breaking_changes: true
    - max_suggestions: 10
  prior_context:
    - "User reported slow login times"
    - "Previous review found SQL injection risk"
```

### Template Context Block

```yaml
context:
  {{context_field_1 - e.g., files_to_analyze}}:
    - {{value}}
  {{context_field_2 - e.g., focus_areas}}:
    - {{value}}
  constraints:
    {{constraint_1}}: {{value}}
  prior_context:
    - "{{relevant background from conversation}}"
```

**Required Fields** (agent-specific):
- `{{field_1 - e.g., files_to_analyze}}`: {{Description - e.g., "List of file paths to process"}}
- `{{field_2 - e.g., focus_areas}}`: {{Description - e.g., "Aspects to prioritize"}}
- `{{field_3}}`: {{Description}} (optional)

---

## Multi-Agent Coordination

### Upstream Agents (provide input to this agent)

| Agent | Provides | Example |
|-------|----------|---------|
| `{{agent-1}}` | {{What they provide}} | {{Brief example}} |
| `{{agent-2}}` | {{What they provide}} | {{Brief example}} |

### Downstream Agents (consume this agent's output)

| Agent | Uses | For |
|-------|------|-----|
| `{{agent-3}}` | {{Which output field}} | {{Purpose}} |
| `{{agent-4}}` | {{Which output field}} | {{Purpose}} |

### Parallel Execution Pattern

```
Launch in parallel:
- Task({{agent-name}}, "{{task_1}}")
- Task({{other-agent}}, "{{task_2}}")
- Task({{another-agent}}, "{{task_3}}")

Synthesize results when all complete.
```

---

## Error Handling

### Retry Conditions

Retry delegation when:
- `confidence < 0.5` with refined context
- `failure_type: "insufficient_context"` with additional information

### Escalation Conditions

Escalate to user when:
- 2+ retries failed
- `failure_type: "{{unrecoverable_type}}"`
- Agent explicitly requests escalation

---

## Examples by Mode

### Mode: {{mode_1}}

**Delegation**:
```
Task({{agent-name}}, "{{mode_1 specific task description}}")
```

**Expected output structure**:
```yaml
{{mode_1_output_structure}}
```

### Mode: {{mode_2}}

**Delegation**:
```
Task({{agent-name}}, "{{mode_2 specific task description}}")
```

**Expected output structure**:
```yaml
{{mode_2_output_structure}}
```
