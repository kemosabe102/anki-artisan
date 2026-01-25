---
name: agent-skill-integration
description: >
  Communication protocol between agents and skills. Use when defining how agents
  invoke skills, understanding request/response formats, or debugging skill invocations.
  Trigger keywords: skill invocation, Skill(), invoke skill, skill protocol, skill discovery.
---

# Agent-Skill Integration Protocol

Communication protocol for agent-to-skill interactions. Defines invocation patterns, request/response formats, error handling, and discovery mechanisms.

## Quick Reference

| Aspect | Pattern |
|--------|---------|
| Invocation syntax | `Skill(skill-name)` |
| Discovery | Metadata-based (name + description in frontmatter) |
| Output format | Structured JSON preferred, free-form for guidance |
| Validation gate | CQ >= 0.85 before skill application |
| Tool permissions | `allowed-tools` frontmatter field |
| Max context load | 500 lines per SKILL.md |

---

## Table of Contents

1. [Invocation Patterns](#invocation-patterns)
2. [Request Format](#request-format)
3. [Response Format](#response-format)
4. [Output Expectations](#output-expectations)
5. [Error Handling](#error-handling)
6. [Skill Discovery](#skill-discovery)
7. [Tool Permission Model](#tool-permission-model)
8. [Validation Checklist](#validation-checklist)

## Reference Documentation

- **Invocation Examples** -> [references/invocation-examples.md](references/invocation-examples.md)
- **Error Handling** -> [references/error-handling.md](references/error-handling.md)

---

## 1. Invocation Patterns

### Model-Invoked Skills

Skills are **model-invoked** - Claude autonomously decides when to use them based on context and the skill's description. This differs from slash commands which are user-invoked.

**Invocation Flow**:
```
User Request -> Claude Reads Description -> Relevance Check -> Load SKILL.md -> Execute
```

### Explicit Invocation (Agent Context)

Within agent workflows, skills can be explicitly referenced:

```python
# Pattern 1: Direct skill reference in agent prompt
"Apply the code-quality skill to analyze this file"

# Pattern 2: Skill composition
"Use debugging-methodology skill, then apply code-quality"

# Pattern 3: Conditional skill application
"If code changes detected, invoke code-review-standards skill"
```

### Implicit Invocation (Trigger Keywords)

Claude automatically invokes skills when requests match description keywords:

| Request Pattern | Triggers Skill |
|-----------------|----------------|
| "review this Python code" | `code-quality` |
| "debug this issue" | `debugging-methodology` |
| "help me understand this library" | `library-research` |

---

## 2. Request Format

### Minimal Request

The simplest skill invocation requires only relevant context:

```markdown
User: Review this function for security issues
[code block]
```

### Structured Request

For complex invocations, provide structured context:

```markdown
## Skill Request: [skill-name]

### Context
- **Files**: [list of relevant files]
- **Objective**: [what needs to be accomplished]
- **Constraints**: [any limitations or requirements]

### Input
[primary content for skill to process]

### Expected Output
[format or structure expected]
```

### Request Fields

| Field | Required | Description |
|-------|----------|-------------|
| Context | Yes | Background information for skill execution |
| Input | Yes | Primary content to process |
| Objective | Recommended | Clear statement of goal |
| Constraints | Optional | Limitations, deadlines, requirements |
| Output Format | Optional | Expected response structure |

---

## 3. Response Format

### Standard Response Structure

Skills return responses in consistent format:

```markdown
## Skill Response: [skill-name]

### Status
[SUCCESS | PARTIAL | FAILURE]

### Summary
[1-2 sentence overview]

### Findings
[detailed results]

### Recommendations
[actionable next steps]
```

### Structured JSON Response

For programmatic consumption:

```json
{
  "skill": "skill-name",
  "status": "SUCCESS",
  "confidence": 0.92,
  "findings": [...],
  "recommendations": [...],
  "metadata": {
    "execution_time": "2.3s",
    "files_analyzed": 5
  }
}
```

---

## 4. Output Expectations

### Output Types by Skill Category

| Skill Category | Expected Output | Format |
|----------------|-----------------|--------|
| Analysis | Findings + recommendations | Markdown report |
| Validation | Pass/Fail + issues | Structured checklist |
| Generation | Artifacts | Code/config files |
| Research | Synthesis | Markdown with citations |

### Confidence Scores

Include confidence when making claims:

```markdown
**Finding**: SQL injection vulnerability detected
**Confidence**: 0.95 (high - direct evidence in code)
**Evidence**: Line 42 uses string concatenation for query
```

### Progressive Output

For long-running skills, provide incremental updates:

```markdown
## Progress: [skill-name]

- [x] Step 1: File discovery (12 files found)
- [x] Step 2: Initial analysis (3 issues identified)
- [ ] Step 3: Deep inspection (in progress...)
- [ ] Step 4: Report generation
```

---

## 5. Error Handling

### Error Categories

| Category | Code | Recovery Action |
|----------|------|-----------------|
| Missing Input | `INPUT_MISSING` | Request required fields |
| Invalid Format | `FORMAT_INVALID` | Provide format example |
| Skill Not Found | `SKILL_NOT_FOUND` | List available skills |
| Execution Failure | `EXEC_FAILED` | Retry with reduced scope |
| Timeout | `TIMEOUT` | Break into smaller chunks |

### Error Response Format

```json
{
  "skill": "skill-name",
  "status": "FAILURE",
  "error": {
    "code": "INPUT_MISSING",
    "message": "Required field 'files' not provided",
    "recovery": "Provide list of files to analyze"
  }
}
```

### Graceful Degradation

When full execution fails, provide partial results:

```markdown
## Partial Result: [skill-name]

**Status**: PARTIAL (2/5 files analyzed)

**Completed**:
- file1.py: No issues found
- file2.py: 2 warnings

**Failed**:
- file3.py: Parse error (invalid syntax)
- file4.py: Access denied
- file5.py: Timeout

**Recommendation**: Fix syntax in file3.py and retry
```

See [references/error-handling.md](references/error-handling.md) for complete error handling patterns.

---

## 6. Skill Discovery

### Metadata-Based Discovery

Claude discovers skills through YAML frontmatter:

```yaml
---
name: skill-name
description: >
  What this skill does. When to use it.
  Trigger keywords: keyword1, keyword2, keyword3.
---
```

### Discovery Locations

| Location | Scope | Priority |
|----------|-------|----------|
| `~/.claude/skills/` | Personal (all projects) | 1 (highest) |
| `.claude/skills/` | Project (shared via git) | 2 |
| Plugin `skills/` | Plugin-bundled | 3 |

### Listing Available Skills

Request skill inventory:

```
User: What skills are available?
Claude: [Lists all discovered skills with descriptions]
```

### Description Best Practices

**Effective description** (enables discovery):
```yaml
description: >
  Analyzes Python code for security vulnerabilities, performance issues,
  and style compliance. Use when reviewing Python files, validating changes
  before commit, or auditing code quality. Trigger keywords: review python,
  code audit, security check, python lint.
```

**Ineffective description** (poor discovery):
```yaml
description: Helps with code
```

---

## 7. Tool Permission Model

### The `allowed-tools` Field

Restrict which tools a skill can use:

```yaml
---
name: safe-analyzer
description: Read-only code analysis skill
allowed-tools: Read, Grep, Glob
---
```

### Permission Levels

| Level | Tools | Use Case |
|-------|-------|----------|
| Read-only | `Read, Grep, Glob` | Analysis, review |
| Read-write | `Read, Grep, Glob, Edit, Write` | Implementation |
| Full | (no restriction) | Complex workflows |

### Tool Categories

**Safe (read-only)**:
- `Read` - File contents
- `Grep` - Pattern search
- `Glob` - File discovery

**Modifying (require caution)**:
- `Edit` - Surgical file changes
- `Write` - File creation/overwrite

**Privileged (restrict carefully)**:
- `Bash` - Shell commands
- `Task` - Sub-agent delegation

### Inheritance Rules

1. Skills inherit CLAUDE.md restrictions
2. `allowed-tools` further restricts (never expands)
3. Project-level tools override personal skills

---

## 8. Integration with Agent Workflows

### Agent-to-Skill Communication

Agents invoke skills for specialized capabilities:

```
Agent Request -> Skill Execution -> Structured Response -> Agent Integration
```

### Delegation Pattern

```python
# Agent delegates to skill
"Apply debugging-methodology skill to investigate test failure"

# Skill returns structured findings
{
  "root_cause": "Race condition in async handler",
  "evidence": ["log excerpt", "stack trace"],
  "fix_recommendation": "Add mutex lock"
}

# Agent integrates into workflow
"Based on debugging-methodology findings, implementing fix..."
```

### Skill Composition

Chain multiple skills for complex tasks:

```markdown
## Workflow: Code Review Pipeline

1. **codebase-research** -> Understand context
2. **code-quality** -> Identify issues
3. **debugging-methodology** -> Investigate failures
4. **code-review-standards** -> Validate compliance
```

---

## Validation Checklist

Before invoking a skill, verify:

### Pre-Invocation
- [ ] Skill exists (check `.claude/skills/` or `~/.claude/skills/`)
- [ ] Description matches intended use case
- [ ] Required input available (files, context, objective)
- [ ] Tool permissions sufficient for task

### During Execution
- [ ] Monitor for progress updates
- [ ] Check for partial results on timeout
- [ ] Validate output format matches expectations

### Post-Invocation
- [ ] Response status is SUCCESS or acceptable PARTIAL
- [ ] Confidence scores meet threshold (>= 0.85 for critical decisions)
- [ ] Recommendations are actionable
- [ ] No unhandled errors

### Integration Validation
- [ ] Skill output integrates into agent workflow
- [ ] Results can be verified independently
- [ ] Error recovery path defined

---

## Anti-Patterns

### DO NOT

| Anti-Pattern | Why | Instead |
|--------------|-----|---------|
| Invoke skill without context | Poor results | Provide objective + constraints |
| Ignore partial results | Lose valuable data | Process available findings |
| Skip confidence checks | Unreliable decisions | Verify scores >= threshold |
| Chain > 5 skills | Context bloat | Break into phases |
| Bypass tool restrictions | Security risk | Request permission escalation |

### DO

| Pattern | Benefit |
|---------|---------|
| Provide structured input | Consistent results |
| Check skill availability first | Avoid missing skill errors |
| Handle errors gracefully | Robust workflows |
| Use progressive disclosure | Efficient context use |
| Validate output before use | Catch issues early |

---

## See Also

- [Skill Delegation Model](../../docs/01-guides/skills/skill-delegation-model.md)
- [Claude Skills Best Practices](../../docs/01-guides/claude-code/claude-skills-best-practices.md)
- [Agent Skills Guide](../../docs/01-guides/agent-skills.md)
