# Phase 1: OBSERVE - Context Gathering and Operation Identification

**OODA Stage**: OBSERVE | **Time Allocation**: 15-20%

**Purpose**: Parse request, identify operation type, validate inputs, gather context from ecosystem

**Deliverable**: Operation classification, input validation status, context inventory

---

## Pre-Flight Checklist

Before proceeding, verify:

- [ ] Request contains clear operation intent
- [ ] Required inputs present (context, execution_timestamp)
- [ ] Target files/workflows exist (if referencing existing artifacts)
- [ ] No conflicting operations in progress (check operation_id)

---

## Operation Identification

### Step 1.1: Parse Request

**Input**: User request or orchestrator delegation

**Process**:
1. Extract key verbs and nouns from request
2. Match against operation trigger words (see Mode Detection table)
3. Identify scope: single artifact vs. ecosystem-wide

**Mode Detection Table**:

| User Says | Operation | Input Requirements |
|-----------|-----------|-------------------|
| "build workflow", "create workflow" | `build_workflow` | workflow name, purpose, integration points |
| "sync", "synchronize" | `sync_ecosystem` | document list, operation_id, apply_mode |
| "optimize", "improve workflow" | `optimize_workflow` | workflow name, optimization goals |
| "create command", "slash command" | `create_command` | command name, purpose, tool permissions |
| "maintain registry", "update registry" | `maintain_registry` | registry scope, update type |
| "bottleneck", "friction" | `analyze_bottlenecks` | workflow scope, bottleneck indicators |
| "update docs", "documentation" | `update_documentation` | documentation scope, update type |
| "create hook", "automation" | `create_automation` | automation purpose, hook trigger |
| "pre-mortem", "what could go wrong" | `pre_mortem` | target artifact, scope, risk tolerance |
| "analyze failure", "why did this fail" | `analyze_failures` | failed artifact, symptoms, error logs |

**Output**: Identified operation type with confidence score


### Step 1.2: Validate Inputs

**Input**: Parsed request with operation type

**Process**:
1. Check required fields per operation (see schema)
2. Validate path formats (forward slashes, absolute paths)
3. Verify referenced files exist via Glob/Read
4. Check operation_id uniqueness for idempotency

**Validation Checks**:
- `execution_timestamp`: ISO 8601 UTC format
- `operation_id`: Valid ULID or UUID pattern
- `apply_mode`: `dry_run` or `commit`
- File paths: Forward slashes, within `.claude/**` or `docs/**`

**Output**: Validation status (PASS/FAIL with specific issues)

### Step 1.3: Gather Context

**Input**: Validated operation request

**Process**:
1. Read existing workflow/command/hook if modifying
2. Check ecosystem state (workflow registry, existing patterns)
3. Identify dependencies and integration points
4. List unclear items requiring clarification

**Context Sources by Operation**:

| Operation | Key Context Sources |
|-----------|---------------------|
| `build_workflow` | Existing workflows, command patterns, hook templates |
| `sync_ecosystem` | Target documents, cross-references, version history |
| `optimize_workflow` | Current workflow state, usage patterns, friction reports |
| `create_command` | Command registry, Claude Code patterns, tool permissions |
| `pre_mortem` | Target artifact, integration points, historical failures |
| `analyze_failures` | Error logs, execution traces, dependency health |

**Output**: Context inventory with completeness score

---

## Quick Checklist

Before advancing to Phase 2 (ORIENT):

- [ ] Operation type identified with >0.90 confidence
- [ ] All required inputs validated
- [ ] Referenced files/artifacts verified to exist
- [ ] Context gathered from relevant sources
- [ ] Unclear items documented

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Assuming operation type | Always match against Mode Detection table |
| Skipping path validation | Validate all paths before proceeding |
| Ignoring unclear items | Document and flag for resolution |
| Missing context sources | Check all relevant ecosystem files |

---

## Exit Criteria

**CQ (Context Quality) >= 0.70 required to proceed**


| Criterion | Weight | Check |
|-----------|--------|-------|
| Operation identified | 0.30 | Single operation type with confidence >0.90 |
| Inputs validated | 0.25 | All required fields present and valid |
| Files verified | 0.20 | Referenced artifacts exist |
| Context gathered | 0.15 | Key sources read and inventoried |
| Unclear items flagged | 0.10 | Ambiguities documented |

---

## Reference Documentation

- [workflow-operations.md](../docs/workflow-operations.md) - Complete operation definitions
- [workflow.schema.json](../schemas/workflow.schema.json) - Input validation contract
- [base-agent-pattern.md](../../../../docs/01-guides/agents/base-agent-pattern.md) - Inherited patterns

---

**Next Phase**: [Phase 2: ORIENT](phase-2-orient.md)
