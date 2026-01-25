---
name: agent-lifecycle-management
description: >
  Agent lifecycle operations for .claude/agents/**. Use when creating new agents,
  updating existing agents, or validating agent schema compliance.
  Trigger keywords: create agent, update agent, validate agent, agent schema, scaffolding.
---

# Agent Lifecycle Management

Lifecycle operations for Claude Code agents: creation, updates, and validation. Covers directory scaffolding, frontmatter compliance, schema generation, and CLAUDE.md table updates.

## Quick Reference

| Aspect | Pattern |
|--------|---------|
| Agent location | `.claude/agents/{domain}/{agent-name}/` |
| Valid frontmatter fields | 7 fields only (see [Schema](#valid-frontmatter-fields)) |
| Required directories | `docs/`, `examples/`, `schemas/` |
| Main file | `{agent-name}.md` |
| Schema file | `schemas/{agent-name}.schema.json` |
| Max file size | <500 lines for main agent file |
| Description limit | <200 characters |

---

## Table of Contents

1. [Operation Categories](#operation-categories)
2. [CREATE Workflow](#create-workflow)
3. [UPDATE Workflow](#update-workflow)
4. [VALIDATE Workflow](#validate-workflow)
5. [Valid Frontmatter Fields](#valid-frontmatter-fields)
6. [Directory Structure Template](#directory-structure-template)
7. [CLAUDE.md Update Protocol](#claudemd-update-protocol)
8. [Validation Checklist](#validation-checklist)

## Reference Documentation

- **Base Agent Pattern** -> [references/base-agent-pattern.md](references/base-agent-pattern.md)
- **Agent Schema** -> [references/agent-schema.json](references/agent-schema.json)

---

## 1. Operation Categories

| Category | Intent Signals | Action |
|----------|----------------|--------|
| **CREATE** | "create", "new", "build", "make" | Bootstrap directory -> Generate files |
| **UPDATE** | "update", "change", "improve", "fix" | Identify scope -> Apply changes -> Validate |
| **VALIDATE** | "validate", "check", "verify" | Run validation -> Report issues |

---

## 2. CREATE Workflow

### Step 2.1: Pre-Creation Validation

Before creating any agent:

1. **Check for duplicates**: Search existing agents for similar functionality
2. **Validate name**: Must be kebab-case, descriptive, unique
3. **Identify domain**: Match to existing domain category or justify new domain
4. **Define scope boundaries**: Document what the agent DOES and DOES NOT do

### Step 2.2: Directory Scaffolding

Create the standard directory structure:

```bash
mkdir -p .claude/agents/{domain}/{agent-name}/docs
mkdir -p .claude/agents/{domain}/{agent-name}/examples
mkdir -p .claude/agents/{domain}/{agent-name}/schemas
```

**Required Files**:
```
.claude/agents/{domain}/{agent-name}/
├── {agent-name}.md            # Main agent definition
├── docs/
│   ├── README.md              # Documentation index
│   ├── domain-expertise.md    # Domain-specific knowledge
│   └── frameworks.md          # Applied frameworks
├── examples/
│   ├── README.md              # Examples index
│   └── basic-usage.md         # Basic delegation examples
└── schemas/
    ├── README.md              # Schema documentation
    └── {agent-name}.schema.json  # Input/output contract
```

### Step 2.3: Main Agent File Generation

Generate `{agent-name}.md` with required structure:

```yaml
---
name: {agent-name}
description: '{<200 char description with trigger keywords and NOT-for cases}'
model: {opus|sonnet}
color: {color from agent-color-taxonomy.md}
tools: {comma-separated tool list}
---
```

**Agent body must**:
- Reference `base-agent-pattern.md` (inherit, don't duplicate)
- Include Core Behavior, Role & Boundaries, Quality Standards
- Define Error Recovery for domain-specific cases
- Stay under 500 lines (externalize to docs/)

### Step 2.4: Schema Generation

Create `schemas/{agent-name}.schema.json`:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "{Agent Name} Schema",
  "description": "Input/output contract for {agent-name}",
  "type": "object",
  "properties": {
    "input": {
      "type": "object",
      "properties": {
        "request_type": {"type": "string"},
        "context": {"type": "object"}
      },
      "required": ["request_type"]
    },
    "output": {
      "type": "object",
      "properties": {
        "status": {"enum": ["SUCCESS", "FAILURE", "PARTIAL"]},
        "result": {"type": "object"},
        "metadata": {"type": "object"}
      },
      "required": ["status"]
    }
  }
}
```

### Step 2.5: CLAUDE.md Registration

Add entry to CLAUDE.md Complete Agent List table (see [CLAUDE.md Update Protocol](#claudemd-update-protocol)).

---

## 3. UPDATE Workflow

### Step 3.1: Scope Identification

1. Read current agent definition
2. Identify update type:
   - **Frontmatter**: Fields, description, tools
   - **Behavior**: Workflows, boundaries, quality standards
   - **Documentation**: docs/, examples/, schemas/
3. Document scope boundaries for update

### Step 3.2: Apply Changes

| Update Type | Process |
|-------------|---------|
| Frontmatter | Validate field names, apply change, verify schema |
| Behavior | Edit agent.md sections, preserve structure |
| Documentation | Update specific doc file, maintain links |

### Step 3.3: Post-Update Validation

Run VALIDATE workflow after any update:
- Verify frontmatter compliance
- Check file size limits
- Confirm no duplicate content from base-agent-pattern.md
- Validate all internal links

---

## 4. VALIDATE Workflow

### Step 4.1: Frontmatter Validation

Check ONLY these 7 fields are present (no others):

| Field | Required | Validation |
|-------|----------|------------|
| `name` | Yes | kebab-case, matches filename |
| `description` | Yes | <200 chars, includes trigger keywords |
| `model` | No | `opus` or `sonnet` only |
| `color` | No | Valid color from taxonomy |
| `tools` | No | Comma-separated valid tool names |
| `permissionMode` | No | `default` or `permissive` |
| `skills` | No | Array of skill names |

**INVALID FIELDS** (reject if present):
- `version`, `maturity`, `temperature`, `context`, `date`, `status`, `tags`

### Step 4.2: Structural Validation

| Check | Requirement |
|-------|-------------|
| File size | <500 lines for main agent file |
| Directory structure | All required subdirs present |
| Schema file | `schemas/{agent-name}.schema.json` exists |
| Base pattern reference | Contains `**Extends**: base-agent-pattern.md` |
| No duplication | Does not copy base-agent-pattern.md content |

### Step 4.3: Validation Report

Return structured validation result:

```json
{
  "status": "PASS | FAIL",
  "agent": "{agent-name}",
  "checks": {
    "frontmatter": {"status": "PASS", "details": "7/7 fields valid"},
    "structure": {"status": "PASS", "details": "All directories present"},
    "schema": {"status": "PASS", "details": "Valid JSON schema"},
    "size": {"status": "PASS", "details": "342 lines"}
  },
  "issues": [],
  "recommendations": []
}
```

---

## 5. Valid Frontmatter Fields

**The 7 valid frontmatter fields**:

```yaml
---
name: agent-name                    # REQUIRED: kebab-case identifier
description: 'Short description'    # REQUIRED: <200 chars with triggers
model: opus                         # OPTIONAL: opus | sonnet
color: blue                         # OPTIONAL: from agent-color-taxonomy.md
tools: Read, Grep, Write           # OPTIONAL: comma-separated tools
permissionMode: default            # OPTIONAL: default | permissive
skills: [skill-1, skill-2]         # OPTIONAL: skill references
---
```

**Common Mistakes**:
- Using `version:` (not valid)
- Using `maturity:` (not valid)
- Using `temperature:` (not valid)
- Description over 200 characters
- Tools not comma-separated

See [references/agent-schema.json](references/agent-schema.json) for formal schema.

---

## 6. Directory Structure Template

Standard agent directory layout:

```
.claude/agents/{domain}/{agent-name}/
├── {agent-name}.md                 # Main definition (<500 lines)
├── phases/                         # OPTIONAL: OODA phase files
│   ├── phase-1-observe.md
│   ├── phase-2-orient.md
│   ├── phase-3-decide.md
│   └── phase-4-act.md
├── docs/
│   ├── README.md                   # Index with descriptions
│   ├── domain-expertise.md         # Domain knowledge
│   └── frameworks.md               # Applied frameworks
├── examples/
│   ├── README.md                   # Example index
│   ├── basic-usage.md              # Simple delegation
│   └── delegation-examples.md      # Complex patterns
└── schemas/
    ├── README.md                   # Schema documentation
    └── {agent-name}.schema.json    # I/O contract
```

**When to use phases/**:
- Agent has multi-step workflows with different delegation per phase
- Complex decision gates between phases
- Exit criteria that must be validated before advancing
- Agent prompt exceeds 200 lines

---

## 7. CLAUDE.md Update Protocol

### When to Update

Update CLAUDE.md Complete Agent List table for:
- CREATE: New agent added
- Major UPDATE: Scope or domain change

### Update Process

1. **Locate table**: Find "Complete Agent List" or equivalent agent registry
2. **Identify category**: Match agent to existing category section
3. **Format entry**:
   ```markdown
   | **{agent-name}** | {domain-scope} | {use-case-description} | {type} |
   ```
4. **Validate formatting**: Ensure table alignment preserved
5. **Fallback**: If write fails, provide manual update instructions

### Example Entry

```markdown
| **development** | Python implementation | Implement Python modules with testing | implementer |
```

---

## 8. Validation Checklist

### Pre-Operation
- [ ] Agent name is unique and kebab-case
- [ ] Domain category identified
- [ ] Scope boundaries documented

### CREATE Validation
- [ ] Directory structure created with all subdirs
- [ ] Main agent file generated with valid frontmatter
- [ ] Schema file created with proper JSON
- [ ] Base pattern referenced (not duplicated)
- [ ] File size under 500 lines
- [ ] CLAUDE.md updated

### UPDATE Validation
- [ ] Scope documented before changes
- [ ] Changes applied within scope
- [ ] Frontmatter remains valid
- [ ] Structure preserved
- [ ] All links functional

### VALIDATE Checks
- [ ] 7 valid frontmatter fields only
- [ ] No invalid fields present
- [ ] Description under 200 chars
- [ ] File under 500 lines
- [ ] Schema file present
- [ ] Base pattern referenced

---

## Error Recovery

| Error | Recovery |
|-------|----------|
| Invalid frontmatter field | List valid fields, show correct format |
| Agent too large | Externalize content to docs/ |
| Duplicate functionality | Suggest consolidation or differentiation |
| Schema validation fails | Show violation, suggest fix |
| CLAUDE.md update fails | Retry once, provide manual instructions |

---

## Anti-Patterns

### DO NOT
- Use invalid frontmatter fields (version, maturity, temperature)
- Duplicate base-agent-pattern.md content
- Exceed 500 lines in main agent file
- Skip schema generation
- Create agents without domain assignment

### DO
- Reference base-agent-pattern.md for common patterns
- Externalize domain content to docs/
- Include trigger keywords in description
- Follow kebab-case naming
- Validate before completion

---

## See Also

- [Base Agent Pattern](references/base-agent-pattern.md) - Inheritance source
- [Agent Schema](references/agent-schema.json) - Valid frontmatter fields
- `.claude/templates/agent.template.md` - Structural template
- `.claude/docs/01-guides/agents/agent-color-taxonomy.md` - Color assignment
