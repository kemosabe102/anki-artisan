# Task Generation Workflow Phases

Complete 6-phase workflow for generating executable task lists from PLAN.md files.

## Phase 1: Analysis & Input Validation

**Purpose**: Parse context and verify inputs

**Steps**:
1. Parse context from orchestrator input
2. Verify plan_file_path and spec_file_path accessibility
3. Assess plan complexity (simple, moderate, complex)
4. Identify unclear plan sections or missing requirements
5. Initialize tracking counters (task count, agent assignments, parallel flags)

**Output**: Validated inputs, complexity assessment, initial counters

### PLAN.md Structure Specification

#### Required Sections (>=3 must be present)

| Section | Canonical Header | Fuzzy Matches | Purpose |
|---------|------------------|---------------|---------|
| Implementation Plan | `## Implementation Plan` | "Implementation", "Plan", "Phases" | Main work items |
| Technical Debt | `## Technical Debt` | "Debt", "Cleanup", "Refactoring" | Cleanup tasks |
| Dependencies | `## Dependencies` | "Requirements", "Prerequisites" | Task dependencies |
| Architecture | `## Architecture` | "Design", "Structure", "Components" | System design |
| Testing | `## Testing` | "Test Plan", "Quality", "Validation" | Test requirements |

#### Section Detection Algorithm

```python
def detect_section(header_text):
    """Detect canonical section from header text using exact + fuzzy matching."""
    canonical_headers = [
        "Implementation Plan", "Technical Debt", "Dependencies", 
        "Architecture", "Testing"
    ]
    fuzzy_patterns = {
        "Implementation Plan": ["implement", "plan", "phase"],
        "Technical Debt": ["debt", "cleanup", "refactor"],
        "Dependencies": ["depend", "require", "prerequisite"],
        "Architecture": ["design", "structure", "component"],
        "Testing": ["test", "quality", "validation"],
    }
    
    # Exact match first (case-insensitive)
    for canonical in canonical_headers:
        if canonical.lower() == header_text.lower().strip("# "):
            return canonical
    
    # Fuzzy match (case-insensitive, partial)
    for canonical, patterns in fuzzy_patterns.items():
        if any(p in header_text.lower() for p in patterns):
            return canonical
    
    return None  # Unknown section
```

#### Validation Rules

| Rule | Threshold | Action if Failed |
|------|-----------|------------------|
| Min sections | >=3 of 5 | FAILURE: missing_plan_sections |
| Section has content | >0 lines after header | WARNING: log empty section |
| Nested headers | ## or ### only | IGNORE: skip deeper nesting |

### Malformed Input Handling

| Issue | Detection | Recovery |
|-------|-----------|----------|
| No ## headers | Grep for `^##` returns empty | FAILURE: parse_error |
| YAML frontmatter error | Parse exception | FAILURE: parse_error |
| Empty file | Size = 0 | FAILURE: plan_not_found |
| Binary file | Contains null bytes | FAILURE: parse_error |
| Missing sections | <3 detected | FAILURE: missing_plan_sections |

**Error Codes Reference**:
- `parse_error`: File format invalid, cannot proceed
- `plan_not_found`: File missing or empty
- `missing_plan_sections`: Fewer than 3 required sections detected

---

## Phase 2: Research & Template Loading

**Purpose**: Gather patterns and templates

**Steps**:
1. Load task template from `docs/00-project/templates/task-template.md`
2. Load feature structure guide for directory patterns
3. Review existing task files for similar components (pattern matching)
4. Query Context7 for task generation best practices (if needed)
5. Synthesize research into task generation strategy

**Output**: Loaded templates, identified patterns, generation strategy

---

## Phase 3: Todo Creation

**Purpose**: Create processing todo items

**Steps**:
1. Generate todo items for each plan section:
   - Technical Debt & Cleanup Tasks (T9XX series)
   - Tech Debt Investigation (T8XX series)
   - Implementation Plan (T001+ series)
2. Define completion criteria for each processing step
3. Track dependencies between todo items
4. Document unclear plan elements requiring resolution

**Output**: Todo list with dependencies and completion criteria


---

## Phase 4: Implementation - Task Generation

**Purpose**: Generate all tasks with proper sequencing

**Reference**: `docs/00-project/templates/task-template.md`

### 4.1 File Operation Type Detection (MANDATORY)

**Purpose**: Determine [C]/[M]/[D] operation type for each task

**Process**:
```
FOR each task T with file_path F:
  1. Check if F exists using Glob("**/F") or file system check
  2. IF F exists AND task modifies content → operation = [M]
  3. IF F not exists → operation = [C]
  4. IF task description contains "remove", "delete", "deprecate" → operation = [D]
  5. Add operation to task prefix: "T001 [C] Create..." or "T002 [M] Update..."
```

**Validation Rules**:

| Operation | Prerequisite Check | If Fails |
|-----------|-------------------|----------|
| [C] Create | Parent directory exists? | Add mkdir task as dependency |
| [M] Modify | File exists? | Change to [C] or flag error |
| [D] Delete | File exists? | Skip task (already deleted) or flag warning |

**Output**: Each task annotated with [C], [M], or [D] operation type

### 4.2 Process Technical Debt & Cleanup Tasks
- Extract from "Technical Debt & Cleanup Tasks" section
- Generate T9XX series tasks with [C] flag
- Detect operation type per 4.1 (cleanup often involves [M] or [D])
- Assign to python-code-implementer based on complexity
- Mark blocking vs post-implementation cleanup

### 4.3 Process Tech Debt Investigation & Dependency Detection
- Extract from plan flags or complexity indicators
- Generate T8XX series tasks with [I] flag
- Assign to tech-debt-investigator
- Document investigation scope

**Dependency Detection Algorithm** (apply to ALL tasks):

```
FOR each task T:
  1. Extract file_path from task description
  2. Scan PLAN.md description for explicit dependency keywords:
     - "after X" → add explicit dependency on task X
     - "requires X" → add explicit dependency
     - "once X is complete" → add explicit dependency
     - "depends on" → add explicit dependency
  3. Check target file for import statements (if file exists):
     - "import X" or "from X import" → add import-chain dependency
  4. Match against dependency taxonomy:
     - test_*.py mirrors *.py → test-impl dependency
     - config/settings references → setup-config dependency
     - Model/Schema/dataclass usage → model-service dependency
     - endpoint/route/API calls → api-client dependency
     - migrate/schema/DDL operations → migration-schema dependency
  5. Add to T.dependencies[] with dependency_type field
```

**Dependency Types Reference**:

| Type | Pattern | Detection |
|------|---------|-----------|
| import-chain | Module A imports Module B | import statements |
| test-impl | Test requires implementation | test file mirrors source |
| setup-config | Config must exist before use | config/settings keywords |
| model-service | Service uses model | Model/Schema/dataclass |
| api-client | Client calls API | endpoint/route/API |
| migration-schema | Migration before model | migrate/schema/DDL |

### 4.4 Process Implementation Tasks
- Extract from "Implementation Plan" section
- Generate T001+ series with TDD pairing (see 4.4.1 TDD Pairing Algorithm)
- Apply agent assignment logic (domain-first thinking)
- Apply TDD enforcement via structural pairing (T###T before T###I)
- Apply parallel execution flags ([P] for independent operations)
- Group tasks into review groups (every 5-8 tasks)
- Generate progress checkpoints at milestones
- Order by dependency priority

### 4.4.1 TDD Pairing Algorithm

**Scope**: All implementation tasks targeting `packages/**` or `scripts/**`

```
FOR each implementation_item in plan.implementation_section:
  
  IF file_path matches (packages/** OR scripts/**):
    # TDD Pairing Required
    1. Generate base_id = next_available_id()  # e.g., T001
    2. Create test_task:
       - id: base_id + "T"                     # e.g., T001T
       - file: tests/unit/test_{module}.py
       - agent: test-creator
       - action: "Write tests for {scope}"
    3. Create impl_task:
       - id: base_id + "I"                     # e.g., T001I
       - file: packages/**/...
       - agent: python-code-implementer
       - action: "Implement {scope}"
    4. Set dependency:
       - impl_task.depends_on = [test_task.id]  # T001I depends on T001T
    5. Set order:
       - test_task.order = n
       - impl_task.order = n + 1               # T###T always before T###I
    6. Append [test_task, impl_task] to task_list
  
  ELSE IF file_path matches (docs/** OR .claude/** OR config files):
    # Standalone Task (no pairing)
    1. Generate standalone_id in T5XX-T7XX range
    2. Create task without T/I suffix
    3. Append to task_list

EXCEPTIONS (no TDD pairing needed):
- Documentation tasks (docs/**) -> T5XX range
- Config/setup tasks (*.yaml, *.json, *.toml) -> T6XX range
- Cleanup/refactoring tasks -> T9XX range (existing)
- Investigation tasks -> T8XX range (existing)
```

**Validation Gate**: After algorithm completes, verify all T###I tasks have matching T###T

### 4.5 Generate Output Files
- Create tasks.md using task template structure
- Create TASKS.json with machine-readable metadata
- Write to component-specific directory

**Output**: Complete task list with all metadata

---

## Phase 5: Validation

**Purpose**: Verify task quality and completeness

**Checks**:
- [ ] All tasks have file operation type [C]/[M]/[D]
- [ ] [C] tasks have parent directory validation (mkdir dependency if needed)
- [ ] [M] tasks reference existing files (verified via Glob)
- [ ] [D] tasks have deprecation/migration plan
- [ ] All tasks have agent assignments
- [ ] All tasks have clear file paths
- [ ] Parallel flags applied correctly
- [ ] Task numbering follows T###T/T###I convention
- [ ] TDD pairing complete (every T###I has matching T###T)
- [ ] TDD order enforced (T###T.order < T###I.order)
- [ ] TDD dependency linked (T###I.depends_on includes T###T)
- [ ] Standalone tasks use T5XX-T7XX range
- [ ] Dependencies properly ordered
- [ ] Review checkpoints every 5-8 tasks
- [ ] Component metadata provided for reviews

**Final Steps**:
1. Generate sprint metadata
2. Calculate confidence score
3. Document any validation failures

**Output**: Validated tasks, sprint metadata, confidence score


---

## Phase 6: Reflection

**Purpose**: Document lessons and improvements

**Steps**:
1. Document lessons learned from plan processing
2. Identify improvement opportunities for task generation
3. Record unclear items and resolution attempts
4. Generate recommendations for plan quality improvements

**Output**: Lessons learned, improvement recommendations

---

## Agent Selection Quick Reference

**See**: `task-creator.md` "Agent Assignment Algorithm" section for complete matrix and decision tree.

**Quick Reference**:
- Tier 1 (0.95): File pattern match (most specific wins)
- Tier 2 (0.80): Directory/domain match
- No Match (0.50): Flag for manual review

---

## Review Checkpoint Generation

**Frequency**: Every 5-8 implementation tasks

**Component Metadata** (for orchestrator multi-agent selection):
- Component type (model, service, api, integration, infrastructure)
- Complexity (simple, moderate, complex)
- Security sensitivity (public-facing, auth-related, data-handling, internal-only)
- Test coverage expectations (unit, integration, system)
- Integration scope (single-component, cross-component, system-wide)

**Orchestrator selects agents at runtime**: 3 core + 0-2 dynamic based on metadata.

---

## Parallel Execution Eligibility

**See**: `task-creator.md` → "Parallel Execution Rules" section for complete eligibility checklist.

**Quick Reference** (ALL must be true for [P] flag):
1. Different target files
2. No import-chain dependency
3. No explicit depends_on relationship
4. Different parent modules
5. Not a test-impl pair

**Sequential Required**: Test before impl, config before use, migration before schema, shared resource access
