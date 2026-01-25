---
argument-hint: '[spec-file-path] [--phase=N]'
description: 'Generate implementation plan in JSON format from SPEC.md. Uses feature_plan structure with phases, features, steps, and acceptance criteria. Outputs PLAN.json ready for /tasks.'
allowed-tools: Task, Read
model: sonnet
---

# Plan Command

*Delegate plan generation to plan-creator agent*

---

## Your Role

You are a **thin orchestrator** that:
1. Receives user request with spec path and optional --phase flag
2. Validates the path exists (quick check)
3. Delegates to plan-creator agent
4. Returns results

**DO NOT** implement plan generation logic - that lives in plan-creator agent and its skills.

---

## Workflow

```
PHASE 1: OBSERVE
  |
  v
Parse arguments (path, --phase flag)
  |
  v
Read SPEC.md metadata (title, section count)
  |
  v
INPUT_GATE: path exists AND file readable AND extension is .md
  |-- FAIL: Return error with specific gate failure
  |-- PASS: Continue to ORIENT
  |
  v
PHASE 2: ORIENT
  |
  v
Classify complexity (Simple: <10 FRs, Complex: >=10 FRs)
  |
  v
PHASE 3: DECIDE
  |
  v
Select timeout (Simple: 120s, Complex: 180s)
  |
  v
PHASE 4: ACT
  |
  v
Task(plan-creator, prompt="Generate implementation plan from SPEC.md at {spec_path}. Phase filter: {phase}", timeout_ms=<calculated>)
  |
  v
OUTPUT_GATE: status in [SUCCESS, FAILURE] AND valid schema
  |-- FAIL: Return error with validation details
  |-- PASS: Continue to DELIVER
  |
  v
PHASE 5: DELIVER
  |
  v
Return plan-creator output with quality attestation
```

---

## Agent Delegation

| Agent | Purpose |
|-------|---------|
| plan-creator | Complete plan generation workflow using skills |

---

## Error Handling

| Error | Action |
|-------|--------|
| Spec path doesn't exist | Return error with suggestion to check path |
| plan-creator fails | Return failure with plan-creator's error message |
| Invalid --phase value | Return error with valid phase range |

---

## Output

Return plan-creator output verbatim. Do not add additional formatting.

---

## Knowledge Base

| Resource | Path |
|----------|------|
| plan-creator agent | `.claude/agents/planning/plan-creator/plan-creator.md` |
| plan-intake skill | `.claude/skills/plan-intake/SKILL.md` |
| plan-generation skill | `.claude/skills/plan-generation/SKILL.md` |
| generating-plans skill | `.claude/skills/generating-plans/SKILL.md` |
| Output schema | `.claude/agents/planning/plan-creator/schemas/plan-creator.schema.json` |

---

## Orchestrator Integration

**Trigger Keywords**: generate plan, create plan, implementation plan, plan from spec, spec to plan

**Delegation Pattern**:
```
User: "Create an implementation plan from the auth spec"
Claude Code (OBSERVE): Parse request -> Identify /plan trigger
Claude Code (ORIENT): SPEC.md exists, has FR sections, CQ = 0.87
Claude Code (DECIDE): ASC = 0.91 -> Delegate to /plan
Claude Code (ACT): SlashCommand(command="/plan docs/01-planning/auth/SPEC.md")
```

**Integration Points**:
- Upstream: /spec (creates SPEC.md)
- Downstream: /tasks (generates executable tasks from PLAN.json)

---

## Edge Cases

### Empty SPEC.md
**Scenario**: SPEC file exists but has no content or only frontmatter
**Behavior**: plan-creator returns error with message "SPEC file contains no functional requirements"
**User Action**: Add at least one FR section to SPEC.md

### Missing Required Sections
**Scenario**: SPEC exists but lacks Problem Statement, Functional Requirements, or Non-Functional Requirements
**Behavior**: plan-intake validates minimum sections (>=3 required)
**User Action**: Ensure SPEC has at least 3 sections with content

### Invalid --phase Value
**Scenario**: User provides --phase=0 or --phase=99
**Behavior**: Return error "Phase must be between 1 and N where N is the number of phases in SPEC"
**User Action**: Check SPEC.md for valid phase numbers

### SPEC with Unresolved Placeholders
**Scenario**: SPEC contains [TODO], [TBD], or [PLACEHOLDER] markers
**Behavior**: Plan generates but includes warnings in output
**User Action**: Resolve placeholders before production use

### Large SPEC Files (>1000 lines)
**Scenario**: Very large SPEC file may cause context limits
**Behavior**: plan-intake truncates to first 5000 lines with warning
**User Action**: Split SPEC into smaller focused documents

---

## Output Examples

### Success
```
Plan generated successfully

Output: docs/01-planning/my-feature/PLAN.json
Quality Score: 0.87 (Grade A)
Features: 3 | Steps: 12 | Phases: 2

Research Recommendations:
MUST: 2 items (auth, external API)
SHOULD: 3 items
COULD: 1 item
```

### Failure
```
Plan generation failed

Error: SPEC_VALIDATION_FAILED
Details: Missing required section: Non-Functional Requirements
Action: Add NFR section to SPEC.md (see docs/templates/SPEC-template.md)
```

---

## Phase Flag Usage

### Filter by Phase
```bash
/plan path/to/SPEC.md --phase=1
```
Generates plan for Phase 1 features only.

### No Phase Filter (Default)
```bash
/plan path/to/SPEC.md
```
Generates plan for all phases.

### Multiple Phases
Not supported. Run command multiple times:
```bash
/plan path/to/SPEC.md --phase=1
/plan path/to/SPEC.md --phase=2
```