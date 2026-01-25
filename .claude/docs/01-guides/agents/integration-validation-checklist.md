---
title: "Agent Integration Validation Checklist"
date: 2025-11-18
status: ACTIVE
tags: [agents, integration, validation, orchestration]
---

# Agent Integration Validation Checklist

**Purpose**: Validate agent integration with Claude Code orchestrator and ecosystem

**Audience**: claude-code-ecosystem, workflow agents, agent creators

**Scope**: Integration requirements for `.claude/agents/*.md` files with orchestrator-workflow.md, base-agent-pattern.md, CLAUDE.md

---

## Quick Reference

| **Requirement** | **Validation** | **Impact if Missing** |
|-----------------|----------------|----------------------|
| Frontmatter Compliance | 7 valid fields (name, description, tools, model, permissionMode, skills, color) | Agent won't load correctly in Claude Code |
| Base Pattern Extension | `**Extends**: base-agent-pattern.md` declaration | 1,150 token waste, duplication, inconsistency |
| Orchestrator Integration | Entry in orchestrator-workflow.md Agent Legend | Agent invisible to delegation logic |
| CLAUDE.md Entry | Row in Complete Agent List table | Agent not discoverable by users/orchestrator |
| Schema Reference | `.claude/docs/schemas/{agent-name}.schema.json` | Output validation fails, type safety lost |
| Pre-Flight Assessment | complexity_estimate, expected_changes, failure_tolerance | No risk assessment before execution |
| Two-Attempt Rule | Max 2 failures → escalate pattern | Infinite retry loops, wasted tokens |

**Validation Score**: Pass/Fail for each requirement → Overall: PASS (7/7) | PARTIAL (5-6/7) | FAIL (<5/7)

---

## 1. Frontmatter Compliance

**Requirement**: Agent definition must have valid frontmatter with 7 approved fields.

**Valid Fields**:
1. `name` (string, required) - Agent identifier matching filename
2. `description` (string, required) - One-line purpose description
3. `tools` (comma-separated string, optional) - Tool access list (Read, Write, Edit, Grep, Glob, Bash, Task, etc.)
4. `model` (string, optional) - opus (recommended) | sonnet | haiku | inherit
5. `permissionMode` (string, optional) - default | acceptEdits | bypassPermissions | plan | ignore
6. `skills` (comma-separated string, optional) - Skill references
7. `color` (string, optional) - UI color identifier

**Invalid Fields** (will cause errors):
- `agent_type`, `category`, `version`, `author`, `tags`, `status`, `priority`, custom fields

**Validation**:
```yaml
✅ GOOD:
---
name: researcher-external
description: Official library/framework documentation specialist via Context7 MCP
tools: mcp__context7__resolve-library-id, mcp__context7__get-library-docs, WebFetch
model: opus
permissionMode: default
---

❌ BAD:
---
name: researcher-external
description: Documentation specialist
agent_type: research  ← INVALID FIELD
category: research     ← INVALID FIELD
version: 1.0           ← INVALID FIELD
---
```

**Detection**:
- Parse frontmatter YAML
- Check for invalid fields (not in approved list)
- Verify required fields present (name, description)
- Validate field types (name/description are strings, tools is comma-separated string)

**Fix**: Remove invalid fields, ensure name + description present

**Reference**: `.claude/docs/01-guides/agents/agent-standards-extended.md` (Frontmatter Validation section)

---

## 2. Base Pattern Extension Declaration

**Requirement**: Agent must declare extension of base-agent-pattern.md if using inherited sections.

**Inherited Sections** (from base-agent-pattern.md):
- Knowledge Base Integration
- Pre-Flight Checklist
- Core Workflow
- Error Recovery
- Parallel Execution
- Validation Checklist

**Validation**:
```markdown
✅ GOOD:
**Extends**: .claude/docs/01-guides/agents/base-agent-pattern.md

**Inherited Sections**:
- Knowledge Base Integration
- Pre-Flight Checklist
- Core Workflow
- Error Recovery
- Parallel Execution
- Validation Checklist

## [Agent-Specific Content]
Domain-specific workflows...

❌ BAD:
## Knowledge Base Integration  ← Duplicated content instead of inherited
[... 45 lines of content identical to base-agent-pattern.md ...]
```

**Detection**:
- Check for `**Extends**: base-agent-pattern.md` declaration
- Compare agent content to base-agent-pattern.md (detect >80% duplication)
- Verify no duplication of 6 standard sections

**Fix**: Add extension declaration, remove duplicated sections, reference base pattern

**Token Impact**: ~1,150 tokens saved per agent through inheritance

**Reference**: `.claude/docs/01-guides/agents/base-agent-pattern.md`

---

## 3. Orchestrator Workflow Integration

**Requirement**: Agent must be listed in orchestrator-workflow.md Agent Legend with domain boundaries.

**Required Information**:
- Agent name
- Primary domain (file paths: `.claude/**`, `packages/**`, `docs/**`, etc.)
- Maturity level (v0.x MVP, v1.x Alpha, v2.x Beta, v3.x+ GA)
- OODA phase specialization (OBSERVE, ORIENT, DECIDE, ACT percentages)
- Capabilities summary (1-2 sentences)

**Validation**:
```markdown
✅ GOOD (in orchestrator-workflow.md):
| **Agent** | **Domain** | **Maturity** | **OODA** | **Capabilities** |
|-----------|------------|--------------|----------|------------------|
| researcher-external | External research | v2.0 Beta | 0/85/10/5 | Context7 + Perplexity unified, auto-routes, 15:1 compression |

❌ BAD:
Agent exists in .claude/agents/ but NOT in orchestrator-workflow.md Agent Legend
→ Invisible to delegation logic, won't be selected by agent selection frameworks
```

**Detection**:
- Parse orchestrator-workflow.md Agent Legend table
- Check if agent name appears in legend
- Verify domain boundaries match agent's actual scope

**Fix**: Add row to Agent Legend table with domain, maturity, OODA, capabilities

**Reference**: `.claude/docs/03-workflows/orchestrator-workflow.md` (Agent Legend section)

---

## 4. CLAUDE.md Entry

**Requirement**: Agent must appear in CLAUDE.md Complete Agent List table for user discoverability.

**Required Information**:
- Agent name
- One-line description
- Primary use cases (when to use this agent)

**Validation**:
```markdown
✅ GOOD (in CLAUDE.md):
**Domain Specialists**: market-data-specialist (...) | researcher-external (official library/framework documentation + web research via Context7/Perplexity) | ...

❌ BAD:
Agent exists but NOT mentioned in CLAUDE.md
→ Users don't know agent exists, orchestrator might not select it
```

**Detection**:
- Search CLAUDE.md for agent name
- Verify description matches agent's frontmatter description
- Check agent listed in appropriate category (Discovery, Domain Specialists, Analysis & Quality, Utility, etc.)

**Fix**: Add agent to CLAUDE.md in appropriate category with description and use cases

**Reference**: `CLAUDE.md` (Agent Quick Reference section)

---

## 5. Schema Reference

**Requirement**: Agent must reference output schema extending base-agent.schema.json.

**Schema Structure**:
```json
{
  "$schema": "http://json-schema.org/draft/2020-12/schema#",
  "title": "{Agent Name} Output",
  "allOf": [
    {"$ref": ".claude/docs/schemas/base-agent.schema.json"},
    {
      "properties": {
        "agent_specific_output": {
          "type": "object",
          "description": "Agent-specific output structure",
          "properties": {
            // Agent-specific fields
          }
        }
      }
    }
  ]
}
```

**Validation**:
```markdown
✅ GOOD (in agent definition):
**Output Schema**: .claude/agents/research/researcher-external/schemas/researcher-external.schema.json

**Two-State Model**:
- SUCCESS: agent_specific_output contains findings, compression_stats
- FAILURE: failure_details contains error information

❌ BAD:
No schema reference, or schema doesn't extend base-agent.schema.json
```

**Detection**:
- Check for schema file reference in agent definition
- Verify schema file exists at `.claude/docs/schemas/{agent-name}.schema.json`
- Parse schema JSON, verify allOf with base-agent.schema.json reference
- Validate two-state model (SUCCESS/FAILURE conditional requirements)

**Fix**: Create schema file, reference in agent definition, ensure base schema extension

**Reference**: `.claude/docs/schemas/base-agent.schema.json`, `.claude/docs/01-guides/agents/schema-quality-criteria.md`

---

## 6. Pre-Flight Assessment Pattern

**Requirement**: Agent workflow must include pre-flight assessment before execution.

**Required Assessments**:
- **complexity_estimate** (low/medium/high) - Task complexity evaluation
- **expected_changes** (file count, line estimates) - Scope prediction
- **failure_tolerance** (strict/moderate/flexible) - Risk tolerance
- **research_needs** (yes/no + scope) - Whether research needed before action

**Validation**:
```markdown
✅ GOOD:
## Pre-Flight Assessment

Before execution, evaluate:

1. **Complexity**: Analyze task scope (component count, dependencies, unknowns)
   - Low (<0.3): Single component, clear pattern
   - Medium (0.3-0.7): Multiple components, some unknowns
   - High (>0.7): Cross-domain, significant unknowns

2. **Expected Changes**: Estimate file modifications
   - Files: Count expected edits
   - Lines: Rough magnitude (10s, 100s, 1000s)

3. **Failure Tolerance**: Assess risk level
   - Strict: Critical path, must succeed
   - Moderate: Important but recoverable
   - Flexible: Experimental, iteration expected

4. **Research Needs**: Determine if research required before implementation
   - Context7 for library patterns
   - WebSearch for industry standards
   - Codebase grep for existing patterns

❌ BAD:
No pre-flight assessment - agent jumps straight to implementation
```

**Detection**:
- Search agent definition for "Pre-Flight" or "Assessment" section
- Verify complexity, expected_changes, failure_tolerance, research_needs mentioned
- Check that workflow includes assessment step BEFORE action

**Fix**: Add Pre-Flight Assessment section to workflow, include 4 required assessments

**Reference**: `.claude/docs/01-guides/agents/base-agent-pattern.md` (Pre-Flight Checklist)

---

## 7. Two-Attempt Rule Compliance

**Requirement**: Agent must implement max 2 failures → escalate pattern (prevent infinite retries).

**Pattern**:
```markdown
✅ GOOD:
## Error Recovery

**Two-Attempt Rule**: Maximum 2 failures per operation → escalate to orchestrator

1. **First Failure**: Analyze error, adjust approach, retry
2. **Second Failure**: Return FAILURE status with detailed failure_details, escalate

**No Infinite Retries**: After 2 attempts, orchestrator decides next action (different agent, user intervention, abandon)

**Failure Details Required**:
- failure_type (validation_error, tool_failure, constraint_violation, etc.)
- reasons (list of specific failure causes)
- recovery_suggestions (actionable next steps for orchestrator)

❌ BAD:
while not success:
    try_again()  ← Infinite retry loop, no escalation
```

**Detection**:
- Search for "Two-Attempt" or "max 2" or "escalate" in agent definition
- Verify agent doesn't implement infinite retry loops
- Check failure_details schema includes failure_type, reasons, recovery_suggestions

**Fix**: Add Two-Attempt Rule to Error Recovery section, implement escalation pattern

**Reference**: `.claude/docs/01-guides/agents/agent-standards-extended.md` (Two-Attempt Rule section)

---

## Validation Workflow

**For claude-code-ecosystem during agent creation/review**:

1. **Parse Frontmatter**: Check 7 valid fields, no invalid fields
2. **Check Base Extension**: Verify `**Extends**: base-agent-pattern.md` if using inherited sections
3. **Validate Orchestrator Entry**: Search orchestrator-workflow.md for agent name
4. **Validate CLAUDE.md Entry**: Search CLAUDE.md for agent name in appropriate category
5. **Check Schema**: Verify schema file exists, extends base-agent.schema.json
6. **Validate Pre-Flight**: Check for Pre-Flight Assessment section with 4 required assessments
7. **Check Two-Attempt Rule**: Verify Error Recovery includes max 2 failures → escalate

**Scoring**:
- PASS: 7/7 requirements met
- PARTIAL: 5-6/7 requirements met (acceptable for v0.x MVP, must fix for v1.x+)
- FAIL: <5/7 requirements met (block agent deployment)

---

## Integration with Agent Analysis

**claude-code-ecosystem.md** runs this checklist during:
- Agent creation (new agent validation)
- Agent review (existing agent audit)
- Quality matrix evaluation (Integration criterion)

**claude-code-ecosystem.md** validates integration aspects:
- Frontmatter compliance (structural quality)
- Schema reference (structural quality)

**tech-debt-investigator.md** identifies integration debt:
- Missing base-pattern extension (duplication debt)
- Orphaned agents (not in orchestrator-workflow.md or CLAUDE.md)

**See Also**:
- `.claude/docs/01-guides/agents/agent-standards-extended.md` - Universal requirements
- `.claude/docs/03-workflows/orchestrator-workflow.md` - Agent Legend and delegation patterns
- `CLAUDE.md` - Complete Agent List and discovery
- `.claude/docs/01-guides/agents/base-agent-pattern.md` - Inheritance model

---

**Version**: 1.0
**Source**: Agent standards extended + orchestrator workflow patterns + base-agent pattern
