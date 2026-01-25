# Agent Creation Guide

**Purpose**: Complete guide for creating new agents using agent.template.md v6.0
**Last Updated**: 2025-11-21
**Template Version**: 6.0

---

## Quick Start (5 Steps)

1. **Copy template**:
   ```bash
   cp .claude/templates/agent.template.md .claude/agents/[domain]/[agent-name].md
   ```

2. **Delete header**: Remove lines 1-22 (entire warning block + "## Agent Definition Header" marker)

3. **Fill frontmatter**: Update YAML fields
   - `name`: Descriptive agent name (e.g., security-scanner)
   - `description`: 1-2 sentences describing purpose
   - `model`: opus (recommended) | sonnet | haiku | inherit
   - `color`: purple|blue|green|yellow|red
   - `tools`: Comma-separated string (NOT YAML list)
   - `permissionMode`: default|acceptEdits|bypassPermissions|plan|ignore
   - `skills`: Comma-separated skill names or empty `""`

4. **Replace placeholders**:
   - All `[bracketed content]`
   - All `{{agent-name}}` occurrences (Bash examples)

5. **Validate**:
   ```bash
   uv run python scripts/validate_agent_file.py .claude/agents/[domain]/[agent-name].md
   ```

---

## Detailed Creation Process

### Step 1: Choose Domain Directory

**Directory Structure**:
```
.claude/agents/
├── dev-tools/        # Agents for .claude/** management
├── research/         # Research and analysis agents
├── implementation/   # Code implementation agents
├── review/           # Code review and validation agents
└── orchestration/    # Multi-agent coordination agents
```

**Naming Convention**: `[function]-[specialization].md`
- ✅ Good: `security-scanner.md`, `researcher-external.md`, `code-quality.md`
- ❌ Bad: `agent1.md`, `helper.md`, `new_agent.md`

---

### Step 2: Fill Frontmatter

**Example**:
```yaml
---
name: security-scanner
description: SAST analysis for Python code with vulnerability detection and security report generation
model: opus
color: red
tools: Read, Grep, Bash
permissionMode: default
skills: ""
---
```

**Field Requirements**:
- **name** (REQUIRED): Lowercase with hyphens, no spaces
- **description** (REQUIRED): 90-110 tokens (360-440 characters)

> ⚠️ **CRITICAL: YAML Syntax for Description Field**
>
> Claude Code does NOT correctly parse YAML multi-line syntax (`|` pipe or `>` folded block). Using these causes descriptions to load as ~11 tokens instead of the full content, breaking agent selection.
>
> **❌ BROKEN - Do NOT use**:
> ```yaml
> description: |
>   Multi-line description text here.
>   Second line of description.
>
> description: >
>   Folded block syntax also broken.
>   Same parsing issue as pipe.
> ```
>
> **✅ CORRECT - Use single-quoted strings**:
> ```yaml
> description: 'Single line description. All content on one line. Escape internal quotes by doubling them like this: it''s working.'
> ```
>
> **Rules**:
> 1. Always use single-quoted strings for `description`
> 2. Keep entire description on ONE line (no line breaks)
> 3. Escape single quotes by doubling: `'` → `''`
> 4. Avoid special characters: use `->` not `→`, use `x` not `×`
- **model**: Default `opus` (recommended for most agents), `sonnet` for simpler tasks, `haiku` for speed, `inherit` to use parent's model
- **color**: Visual identifier (red for security, blue for research, green for implementation, etc.)
- **tools**: Only include tools agent will use (comma-separated string)
- **permissionMode**: Usually `default`, use `acceptEdits` for autonomous file operations
- **skills**: Leave `""` unless agent auto-loads specific skills

---

### Step 3: Replace Placeholders

**Bracketed Content** `[like this]`:
- Role & Boundaries: `[Agent Type]`, `[Core Function]`, `[Capabilities]`
- Workflow Operations: `[Primary Operation Workflow]`, `[operation_name]`
- All section-specific placeholders

**Agent Name Placeholders** `{{agent-name}}`:
- Find: `{{agent-name}}`
- Replace with: Actual `name` value from frontmatter
- **Example**: `AGENT_NAME={{agent-name}}` → `AGENT_NAME=security-scanner`

**Validation**: Search entire file for `{{agent-name}}` - must be ZERO results before finalizing.

---

### Step 4: Create Schema File

**Path**: `.claude/docs/schemas/[agent-name].schema.json`

**Template Structure**:
```json
{
  "$schema": "http://json-schema.org/draft/2020-12/schema#",
  "title": "[Agent Name] Output Schema",
  "description": "[Agent purpose and output structure]",
  "allOf": [
    {"$ref": "../shared/schemas/base-agent.schema.json"},
    {
      "if": {"properties": {"status": {"const": "SUCCESS"}}},
      "then": {
        "required": ["agent_specific_output"],
        "properties": {
          "agent_specific_output": {
            "type": "object",
            "description": "[Agent-specific success output]",
            "required": ["field1", "field2"],
            "properties": {
              "field1": {"type": "string", "description": "..."},
              "field2": {"type": "array", "items": {"type": "string"}}
            }
          }
        }
      },
      "else": {
        "if": {"properties": {"status": {"const": "FAILURE"}}},
        "then": {
          "required": ["failure_details"],
          "properties": {
            "failure_details": {
              "type": "object",
              "required": ["failure_type", "reasons"],
              "properties": {
                "failure_type": {"type": "string"},
                "reasons": {"type": "array", "items": {"type": "string"}},
                "recovery_suggestions": {"type": "array", "items": {"type": "string"}}
              }
            }
          }
        }
      }
    }
  ]
}
```

**Reference Example**: `.claude/docs/schemas/claude-code-ecosystem.schema.json`

---

### Step 5: Validation Script Usage

```bash
# Basic validation
uv run python scripts/validate_agent_file.py .claude/agents/security/scanner.md

# Expected output:
✅ PASS: Frontmatter valid (7/7 fields)
✅ PASS: No template headers found
✅ PASS: All placeholders replaced
✅ PASS: Schema exists at .claude/docs/schemas/scanner.schema.json
⚠️  WARN: Section "Workflow Operations" uses h4 headings (recommend h3 max)
✅ PASS: Base pattern extension present

Overall: PASS (6/6 critical checks, 1 warning)
```

**Validation Checks**:
1. File starts with `---` (YAML frontmatter on line 1)
2. No template warning headers (lines 1-22 fully removed)
3. No unreplaced `{{agent-name}}` placeholders
4. AGENT_NAME prefix uses actual agent name from frontmatter
5. Only one `---...---` block (YAML frontmatter)
6. Schema file exists at `.claude/docs/schemas/[agent-name].schema.json`
7. Section ordering matches template
8. Base pattern referenced, not duplicated

---

## Post-Creation Integration (MANDATORY)

See template lines 713-768 for complete integration steps:

1. **Update orchestrator-workflow.md Agent Legend**: Add agent to capability matrix
2. **Update CLAUDE.md Complete Agent List**: Add agent to appropriate category
3. **Test orchestrator discovery**: Restart session (new agents only), verify delegation works

**Session Restart Requirements**:
- **NEW agents**: Session restart REQUIRED for Claude Code recognition
- **Modified existing agents**: No restart needed

---

## Troubleshooting

### Common Errors

**Error**: `Frontmatter validation failed: invalid field 'disallowedTools'`
- **Cause**: Template v5.0 frontmatter used
- **Fix**: Use template v6.0, field removed

**Error**: `Unreplaced placeholder found: {{agent-name}}`
- **Cause**: Missed placeholder replacement
- **Fix**: Search entire file for `{{agent-name}}`, replace all with actual name

**Error**: `Schema file not found`
- **Cause**: Schema not created or wrong path
- **Fix**: Create `.claude/docs/schemas/[agent-name].schema.json`

**Error**: `Agent not found in orchestrator-workflow.md`
- **Cause**: Post-creation integration not completed
- **Fix**: Add agent to Agent Legend table

---

## Best Practices

1. **Test agent creation**: Create 1-2 test agents before production use
2. **Validation first**: Run validation script before integration
3. **Small iterations**: Fill one section at a time, validate frequently
4. **Reference existing agents**: Look at similar agents for patterns
5. **Token optimization**: Target <15K tokens per agent (use base pattern extension)

---

**Questions**: Reference agent.template.md v6.0 or consult `.claude/docs/01-guides/agents/integration-validation-checklist.md`
