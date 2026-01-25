# Delegation Examples

How the orchestrator invokes python-code-reviewer.

## Standard Code Review

```markdown
Task(python-code-reviewer,
  "Review code changes in current branch. Focus on principle-driven
   feedback with ranked findings (Critical/Major/Minor/Nits).
   Validate findings against Context7 library docs.")
```

## Targeted File Review

```markdown
Task(python-code-reviewer,
  "Review packages/core/auth/validator.py for security patterns
   and type safety. Focus on OWASP Top 10 compliance.")
```

## Pre-Merge Quality Gate

```markdown
Task(python-code-reviewer,
  "Perform quality gate check for PR #123. Must have zero Critical
   findings and ≤2 Major findings to pass. Output review_passed: true/false.")
```

## Multi-Agent Coordination

When used with other agents:

```markdown
# Parallel review pattern
Task(python-code-reviewer, "Review code quality and correctness")
Task(sast-scanner, "Scan for security vulnerabilities")
Task(test-executor, "Run test suite and verify coverage")

# Orchestrator synthesizes results for final verdict
```

## Context Requirements

When delegating, include:
- **Branch/PR context**: Which changes to review
- **Focus areas**: Security, performance, type safety, etc.
- **Quality gates**: Pass/fail criteria if applicable
- **Scope limits**: Specific files or directories

## Expected Output

Agent returns structured JSON per `schemas/python-code-reviewer.schema.json`:

```json
{
  "status": "SUCCESS",
  "agent": "python-code-reviewer",
  "confidence": 0.92,
  "agent_specific_output": {
    "review_verdict": "Changes Requested",
    "review_passed": false,
    "artifact_scope": {
      "files_reviewed": ["packages/core/auth/validator.py"]
    },
    "review_findings": [...],
    "recommendations": {...},
    "rate_limit_compliance": {
      "critical_count": 2,
      "major_count": 3,
      "minor_count": 0,
      "nit_count": 1
    }
  }
}
```
