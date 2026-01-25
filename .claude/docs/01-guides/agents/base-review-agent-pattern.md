---
title: "Base Review Agent Pattern"
date: 2025-11-08
status: ACTIVE
tags: [agents, claude-docs]
---
# Base Review Agent Pattern

**Shared foundation for all specification review agents.**

## Purpose

This pattern establishes common infrastructure for review agents (planning, planning, architecture) to reduce duplication and ensure consistent review methodology.

## Inheritance Model

Review agents EXTEND this base pattern by:

1. Referencing this guide in their "Base Review Agent Pattern" section
2. Declaring their specialized review focus
3. Adding agent-specific review criteria and schemas
4. Inheriting all workflow, error recovery, and validation patterns

## Knowledge Base Integration

**Always Loaded at Startup**:

- Agent definition file
- `CLAUDE.md` for project context
- `.claude/docs/01-guides/agents/agent-standards-runtime.md` (auto-loaded)

**Required Guide Consultations**:

```markdown
1. Review Guidelines (`.claude/docs/guides/spec-review-guidelines.md` or equivalent)
   - When to consult: Every review operation
   - What to extract: Quality criteria, scoring methodology, review standards

2. Review Template (`.claude/templates/spec-review-template.md` or `.claude/docs/templates/business-review-template.md`)
   - When to consult: When generating review reports
   - What to extract: Report structure, required sections, formatting standards
```

**Context Gathering Hierarchy**:

1. Check review guidelines for review standards
2. Review report template for format
3. Examine reference specifications for examples
4. Update guides when new review patterns discovered

## Pre-Flight Checklist

**Comprehensive Task Assessment** (mandatory for all review operations):

1. **Schema Loading**: Verify agent schema accessibility and validation rules
2. **Task Analysis**: Parse SPEC/PLAN file path, review focus, validation thresholds
3. **Research Planning**: Identify guidelines/templates needed for review
4. **Todo Creation**: Generate structured review breakdown (when file >5K tokens)
5. **Ambiguity Detection**: Flag unclear sections, missing specifications
6. **Workflow Selection**: Choose comprehensive or focused review workflow
7. **Resource Verification**: Confirm Read/Write permissions, review/ directory access
8. **Unclear Items Tracking**: Initialize tracking for ambiguous elements

## Core Workflow Structure

**Agent as Class, Workflows as Methods** - Execute structured 6-phase lifecycles:

**Analysis → Research → Todo Creation → Implementation → Validation → Reflection**

### Workflow Phases (Standard Pattern)

1. **Analysis**: Parse file structure, assess complexity, identify unclear sections
2. **Research**: Load review guidelines and template, reference examples
3. **Todo Creation**: Generate review checklist for each major section
4. **Implementation**: Execute quality assessment across all dimensions
5. **Validation**: Verify all metrics calculated, unclear items documented
6. **Reflection**: Generate lessons learned, improvement recommendations

## Todo Management Protocol

**When to Use**: Files >5K tokens or complex multi-section reviews
**Creation Timing**: During Analysis phase after structure assessment
**Structure**: Each todo item includes completion criteria and review dependencies

```json
{
  "todo_items": [
    {
      "id": "review_requirements",
      "description": "Assess functional and non-functional requirements completeness",
      "completion_criteria": "All FR/NFR items evaluated with quality scores",
      "dependencies": [],
      "status": "pending|in_progress|completed"
    }
  ],
  "unclear_items": [
    {
      "id": "unclear_nfr_1",
      "description": "Performance requirements missing quantifiable metrics",
      "impact": "Cannot assess testability of NFR-002",
      "resolution_needed": "Specific performance targets (latency, throughput)"
    }
  ]
}
```

## Error Recovery Patterns

**Retry Logic**:

- Retry Read operations on temporary file access failures
- Maximum 2 retries before returning FAILURE
- No retries for Write operations (report generation)

**Graceful Degradation**:

- Provide partial review when sections unreadable
- Document missing sections in unclear_items
- Suggest manual review for problematic sections

**Failure Communication**:

- Return FAILURE with specific file access errors
- Provide recovery suggestions for structure issues
- Escalate to orchestrator for missing files

**Error Handling**:

- **File Operation Failures**: FAILURE with file path and access error details
- **Schema Violations**: FAILURE with validation error specifics
- **Missing File**: FAILURE with recovery suggestion to verify path
- **Invalid Structure**: FAILURE with structure issues documented

## Validation Checklist

**Lifecycle Validation**:

- [ ] Pre-flight checklist completed with schema loading and path validation
- [ ] Todo items created for complex reviews (file >5K tokens)
- [ ] Unclear items tracked for ambiguous sections
- [ ] All workflow phases executed (Analysis → Research → Todo → Implementation → Validation → Reflection)
- [ ] Output follows two-state model (SUCCESS with review report OR FAILURE with recovery guidance)

**Core Requirements**:

- [ ] All operations within defined scope boundaries (usually `docs/01-planning/specifications/**`)
- [ ] Output validates against agent-specific schema
- [ ] File operations follow token assessment protocol
- [ ] Quality scores calculated for all dimensions
- [ ] Review report generated with template structure
- [ ] Integration points maintained with orchestrator
- [ ] Timestamp from orchestrator used (not locally generated)
- [ ] No modifications to source files (read-only enforcement for review agents)

**File Operation Validation**:

- [ ] Pre-flight token count assessment for file reads
- [ ] Read tool used appropriately for file access
- [ ] Write tool used for review report generation
- [ ] No post-operation verification needed (write-only reports)

**Quality Assurance**:

- [ ] Schema compliance validated for SUCCESS/FAILURE structure
- [ ] Confidence and severity scoring included
- [ ] Reflection summary generated with review insights
- [ ] Source attribution for quality standards and scoring methodology
- [ ] Recovery guidance provided for FAILURE cases
- [ ] Rationale provided for quality grades and priority assignments
- [ ] Work stayed within read-only/write-review boundaries

## Agent-Specific Customization Points

Review agents customize the base pattern by providing:

### 1. Review Focus

- **planning**: Quality, completeness, HOW vs WHAT/WHY enforcement
- **planning**: Business alignment, ROI validation, pain point coverage
- **architecture**: Technical constraints, NFR reasonableness, platform justification

### 2. Schema Definitions

- Each agent defines their unique output schemas (Review Report + Edit Plan)
- Schemas extend base-agent.schema.json two-state model

### 3. Review Criteria

- Domain-specific evaluation metrics
- Agent-specific quality scoring algorithms
- Specialized detection logic (e.g., HOW avoidance for planning)

### 4. Output Requirements

- Report format variations
- Required sections unique to review type
- Compliance assessment frameworks

---

**This base pattern provides the common infrastructure for all review agents, reducing duplication and ensuring consistent review methodology across the specification validation workflow.**
