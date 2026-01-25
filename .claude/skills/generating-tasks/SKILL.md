---
name: generating-tasks
description: >
  Use this skill when transforming PLAN.json into executable task lists, applying TDD pairing 
  (T###T/T###I), assigning agents via domain-first matrix, or calculating effort estimates. 
  Trigger keywords: generate tasks, task creation, TDD enforcement, agent assignment, TASKS.json.
---

# Generating Tasks

*Transform implementation plans into executable task lists with TDD enforcement and parallel optimization*

## Contents

- [T-ID Numbering Convention](#t-id-numbering-convention)
- [TDD Pairing Algorithm](#tdd-pairing-algorithm)
- [2-Tier Agent Assignment Matrix](#2-tier-agent-assignment-matrix)
- [Dependency Detection](#dependency-detection)
- [Parallel Eligibility Rules](#parallel-eligibility-rules)
- [Review Checkpoint Insertion Algorithm](#review-checkpoint-insertion-algorithm)
- [Effort Estimation Model](#effort-estimation-model)
- [Quality Score Formula](#quality-score-formula)
- [Validation Gates](#validation-gates)
- [PLAN.json Schema Extraction](#planjson-schema-extraction)
- [Output Format](#output-format)
- [Anti-Patterns](#anti-patterns-never-do)
- [Quick Reference](#quick-reference)

---

## T-ID Numbering Convention

Task IDs follow a structured numbering system with TDD suffixes for implementation tasks.


| Category | ID Range | Suffix | Example |
|----------|----------|--------|---------|
| Cleanup/Debt | T9XX | - | T901 Remove deprecated code |
| Investigation | T8XX | - | T801 Investigate auth module |
| **Test Tasks** | T0XX-T4XX | `T` | T001T Write tests for calculate_metrics |
| **Implementation Tasks** | T0XX-T4XX | `I` | T001I Implement calculate_metrics |
| **Standalone Tasks** | T5XX-T7XX | - | T501 Update documentation |

**Key Rules**:
- T###T suffix = Test task (must precede matching implementation)
- T###I suffix = Implementation task (must have matching test task)
- T5XX-T7XX = Standalone tasks (docs, config) - no TDD pairing required
- T8XX = Investigation tasks - analysis without code changes
- T9XX = Cleanup/debt tasks - existing code modifications

---

## TDD Pairing Algorithm

**Scope**: All implementation tasks targeting `packages/**` or `scripts/**`

```
FOR each implementation_item in plan.implementation_section:
  
  IF file_path matches (packages/** OR scripts/**):
    # TDD Pairing Required
    1. Generate base_id = next_available_id()  # e.g., T001
    2. Create test_task:
       - id: base_id + "T"                     # e.g., T001T
       - file: tests/unit/test_{module}.py
       - agent: code-quality
       - action: "Write tests for {scope}"
    3. Create impl_task:
       - id: base_id + "I"                     # e.g., T001I
       - file: packages/**/...
       - agent: development
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
- Cleanup/refactoring tasks -> T9XX range
- Investigation tasks -> T8XX range
```

**TDD Pairing Rules Summary**:

| Rule | Description |
|------|-------------|
| Pair Requirement | Every T###I MUST have corresponding T###T |
| Order Enforcement | T###T MUST precede T###I in execution order |
| Shared Base ID | Test and impl share same base ID (T001T, T001I) |
| Dependency Link | T###I.depends_on MUST include T###T |
| Standalone Range | Tasks without tests use T5XX-T7XX |

---

## 2-Tier Agent Assignment Matrix

**Agent assignment uses domain-first thinking**: file location -> domain -> specialist

### Assignment Algorithm

```
FOR each task:
  1. Extract file_path from task description
  2. Tier 1 Check (0.95 confidence):
     FOR pattern IN Tier1_Matrix ORDER BY pattern_length DESC:
       IF file_path MATCHES pattern:
         RETURN { agent: Tier1_Matrix[pattern], confidence: 0.95, tier: 1 }
  3. Tier 2 Fallback (0.80 confidence):
     parent_dir = extract_parent_directory(file_path)
     FOR dir IN Tier2_Matrix:
       IF parent_dir STARTS_WITH dir:
         RETURN { agent: Tier2_Matrix[dir], confidence: 0.80, tier: 2 }
  4. No Match (0.50 confidence):
     RETURN { agent: null, confidence: 0.50, flag: "MANUAL_REVIEW" }
```

**Specificity Rule**: Longer/more-specific patterns win.
- `.claude/agents/**/*.md` (20 chars) beats `**/*.md` (6 chars)

### Tier 1: File Type Override (0.95 confidence)

| File Pattern | Agent | Rationale |
|--------------|-------|-----------|
| `.claude/agents/**/*.md` | claude-code-ecosystem | Agent definitions |
| `.claude/commands/**/*.md` | workflow | Command definitions |
| `.claude/hooks/**/*.py` | workflow | Hook implementations |
| `**/schemas/*.json` | claude-code-ecosystem | Schema definitions |
| `docs/**/*.md` | documentation | Documentation files |
| `tests/**/*.py` (create) | code-quality | Test file creation |
| `tests/**/*.py` (run) | code-quality | Test execution |

### Tier 2: Domain Match (0.80 confidence)

| Directory | Domain | Primary Agent | Fallback |
|-----------|--------|---------------|----------|
| `packages/**/*.py` | Core implementation | development | debugger |
| `scripts/**/*.py` | Utility scripts | development | - |
| `k8s/**/*.yaml` | Kubernetes | deployment-release | - |
| `.claude/docs/**/*.md` | Agent docs | claude-code-ecosystem | documentation |

### Disambiguation Rules

| Ambiguous Pattern | Resolution |
|-------------------|------------|
| `.claude/docs/**/*.md` | claude-code-ecosystem (ecosystem docs) |
| `docs/**/*.md` (NOT .claude) | documentation (project docs) |
| `tests/**/*.py` with "create" | code-quality (creation) |
| `tests/**/*.py` with "run/execute" | code-quality (execution) |

---

## Dependency Detection

### Dependency Types

| Type | Pattern | Detection |
|------|---------|-----------|
| import-chain | Module A imports Module B | import statements |
| test-impl | Test requires implementation | test file mirrors source |
| setup-config | Config must exist before use | config/settings keywords |
| model-service | Service uses model | Model/Schema/dataclass |
| api-client | Client calls API | endpoint/route/API |
| migration-schema | Migration before model | migrate/schema/DDL |

### Detection Algorithm

```
FOR each task T:
  1. Extract file_path from task description
  2. Scan PLAN.json feature descriptions for explicit dependency keywords:
     - "after X" -> add explicit dependency on task X
     - "requires X" -> add explicit dependency
     - "once X is complete" -> add explicit dependency
     - "depends on" -> add explicit dependency
  3. Check target file for import statements (if file exists):
     - "import X" or "from X import" -> add import-chain dependency
  4. Match against dependency taxonomy:
     - test_*.py mirrors *.py -> test-impl dependency
     - config/settings references -> setup-config dependency
     - Model/Schema/dataclass usage -> model-service dependency
     - endpoint/route/API calls -> api-client dependency
     - migrate/schema/DDL operations -> migration-schema dependency
  5. Add to T.dependencies[] with dependency_type field
```

---

## Parallel Eligibility Rules

**[P] flag indicates task can run in parallel with others in same batch**

### Parallel [P] Allowed (ALL must be true)

- [ ] Different target files (no file overlap)
- [ ] No import-chain dependency between tasks
- [ ] No explicit dependency keywords in description
- [ ] Different modules (no shared parent directory)
- [ ] Not a test-impl pairing (test and its implementation)

### Sequential Required (ANY triggers sequential)

- [ ] Same target file
- [ ] import-chain detected between tasks
- [ ] Explicit "after", "requires", "depends on" keywords
- [ ] test-impl pairing (test must precede implementation)
- [ ] setup-config dependency (config before consumer)
- [ ] model-service dependency (model before service)

**Max per parallel group**: 3-5 tasks

---

## Review Checkpoint Insertion Algorithm

**Purpose**: Automatically insert review checkpoints after implementation batches and at component integration boundaries.

### Review Checkpoint Types

| Type | ID Pattern | Trigger | Agent |
|------|------------|---------|-------|
| `code_review` | RC###C | Every 5 implementation tasks | python-code-reviewer |
| `integration_review` | RC###I | Component boundary crossing | integration-boundary-reviewer |
| `final_review` | RC###F | End of task list | integration-boundary-reviewer |

### Insertion Detection Algorithm

```
current_batch = []
component_stack = []
previous_component = None
previous_agent_domain = None

FOR each task T in generated_tasks ORDER BY order:
  
  # Track implementation tasks for code review checkpoints
  IF T.task_type == "implementation" AND T.id MATCHES /T\d{3}I/:
    current_component = extract_component(T.file_path)
    current_agent_domain = extract_agent_domain(T.agent)
    
    # Semantic boundary detection (replaces naive counter)
    semantic_boundary = (
      current_component != previous_component OR         # Component change
      current_agent_domain != previous_agent_domain OR   # Agent domain shift  
      len(current_batch) >= MAX_REVIEW_BATCH_SIZE        # Prevent runaway (10)
    )
    
    # Insert checkpoint at semantic boundary (min 3 tasks)
    IF semantic_boundary AND len(current_batch) >= MIN_REVIEW_BATCH_SIZE:
      review_id = generate_review_id("C")  # e.g., RC001C
      insert_code_review_checkpoint(
        review_id=review_id,
        task_range=get_task_range(current_batch),
        files_in_scope=collect_files_from_batch(current_batch),
        component_name=previous_component,
        blocks_tasks=get_next_n_tasks(T, 5)
      )
      current_batch = []
    
    # Add current task to batch
    current_batch.append(T)
    previous_component = current_component
    previous_agent_domain = current_agent_domain
    
    # Integration Review Checkpoint (component boundary)
    IF current_component != component_stack[-1]:
      IF len(component_stack) >= 2:  # At least 2 components involved
        review_id = generate_review_id("I")  # e.g., RC001I
        insert_integration_review_checkpoint(
          review_id=review_id,
          upstream_component=component_stack[-1],
          downstream_component=current_component,
          blocks_tasks=get_tasks_in_component(current_component)
        )
      component_stack.append(current_component)

# Handle remaining batch at end
IF len(current_batch) > 0:
  insert_code_review_checkpoint(
    review_id=generate_review_id("C"),
    task_range=get_task_range(current_batch),
    files_in_scope=collect_files_from_batch(current_batch),
    component_name=previous_component
  )

# Final Review Checkpoint (at end of task list)
insert_final_review_checkpoint(
  review_id=generate_review_id("F"),
  deferred_findings=accumulated_deferred_findings,
  scope="full_integration"
)
```

### Semantic Boundary Detection Rules

Semantic boundaries replace the naive counter-based approach with intelligent grouping based on logical code cohesion.

#### Boundary Conditions

A semantic boundary is detected when ANY of these conditions is true:

| Condition | Detection Method | Example |
|-----------|------------------|---------|
| **Component change** | `extract_component(current_file) != previous_component` | `packages/auth/` -> `packages/users/` |
| **Agent domain shift** | `extract_agent_domain(current_agent) != previous_domain` | `development` -> `code-quality` |
| **Max batch size** | `len(current_batch) >= MAX_REVIEW_BATCH_SIZE` | 10 tasks accumulated |

#### Component Change Detection

Uses the existing `extract_component()` function:

```
# Component extracted from file path
packages/auth/service.py     -> "auth"
packages/users/models.py     -> "users"
tests/unit/test_auth_*.py    -> "auth"
```

#### Agent Domain Shift Detection

Compares the `task.agent` field to identify domain transitions:

```
extract_agent_domain(agent):
  IF agent IN ["python-code-implementer", "debugger"]:
    RETURN "development"
  IF agent IN ["python-code-reviewer", "test-creator", "test-executor"]:
    RETURN "quality"
  IF agent IN ["doc-librarian", "documentation"]:
    RETURN "documentation"
  IF agent IN ["architecture-reviewer", "tech-debt-investigator"]:
    RETURN "architecture"
  RETURN "general"
```

#### Batch Size Constraints

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `MIN_REVIEW_BATCH_SIZE` | 3 | Minimum tasks before checkpoint allowed |
| `MAX_REVIEW_BATCH_SIZE` | 10 | Force checkpoint regardless of boundaries |

#### Examples of Semantic Boundaries

```
# Example 1: Component boundary (auth -> users)
T001I: packages/auth/service.py      [batch: auth]
T002I: packages/auth/models.py       [batch: auth]
T003I: packages/users/service.py     <- BOUNDARY (component change)
                                        -> Insert checkpoint for auth batch

# Example 2: Agent domain shift
T004I: agent=python-code-implementer [batch: dev domain]
T005I: agent=python-code-implementer [batch: dev domain]
T006I: agent=architecture-reviewer   <- BOUNDARY (domain shift)
                                        -> Insert checkpoint for dev batch

# Example 3: Max batch size reached
T007I-T016I: 10 tasks in same component <- BOUNDARY (max size)
                                          -> Insert checkpoint even if same component
```

### Review Group Structure

Each checkpoint generates a review_group entry with multi-reviewer support:

```json
{
  "group_id": "RG001",
  "review_type": "code_review",
  "reviewers": [
    {
      "agent": "python-code-reviewer",
      "focus": ["pythonic_idioms", "type_safety", "error_handling"],
      "weight": 0.40
    },
    {
      "agent": "architecture-reviewer",
      "focus": ["solid_principles", "oop_design", "layering"],
      "weight": 0.35
    },
    {
      "agent": "tech-debt-investigator",
      "focus": ["sqale_score", "complexity", "duplication"],
      "weight": 0.25
    }
  ],
  "execution_mode": "parallel",
  "aggregation": {
    "strategy": "weighted_severity",
    "dedup_threshold": 0.85,
    "conflict_resolution": "highest_severity_wins"
  },
  "component_name": "auth",
  "task_range": "T001-T005",
  "files_in_scope": ["packages/auth/service.py", "packages/auth/models.py"],
  "retry_enabled": true,
  "max_iterations": 3,
  "fix_agents": {
    "test_failures": "debugger",
    "pattern_violations": "python-code-implementer",
    "security_vulnerabilities": "python-code-implementer",
    "performance_issues": "python-code-implementer",
    "integration_breakage": "debugger"
  },
  "success_criteria": {
    "zero_critical": true,
    "max_high": 3,
    "test_coverage": ">= 80%"
  },
  "blocks_tasks": ["T007", "T008", "T009", "T010", "T011"]
}
```

#### Multi-Reviewer Schema Fields

| Field | Type | Description |
|-------|------|-------------|
| `reviewers` | array | List of reviewer agents with focus areas and weights |
| `reviewers[].agent` | string | Agent name from agent pool |
| `reviewers[].focus` | array | Specific review areas for this agent |
| `reviewers[].weight` | float | Weight for aggregated severity scoring (must sum to 1.0) |
| `execution_mode` | string | `parallel` (all reviewers run simultaneously) or `sequential` |
| `aggregation.strategy` | string | `weighted_severity`, `unanimous`, or `majority` |
| `aggregation.dedup_threshold` | float | Similarity threshold for deduplicating findings (0.0-1.0) |
| `aggregation.conflict_resolution` | string | How to resolve conflicting severities |

#### Backward Compatibility

The old single-agent format is still supported for backward compatibility:

```json
{
  "group_id": "RG001",
  "review_type": "code_review",
  "review_task": "T006",
  "...": "..."
}
```

When `reviewers` array is absent, the system uses `review_task` to identify a single reviewer agent.

### Fix-Then-Proceed Workflow

After each review checkpoint completes:

```
IF findings.critical > 0 OR findings.high > 0:
  1. Generate FIX TASK: "Fix CRITICAL/HIGH findings from {review_id}"
     - Agent: Determined by fix_agents map based on issue type
     - Blocks: All tasks in blocks_tasks array
  2. Execute fix task
  3. Re-run review checkpoint (max 3 iterations)
  4. IF still failing after 3 iterations: ESCALATE to user

MEDIUM/LOW/NIT findings:
  1. Add to deferred_findings[] accumulator
  2. Continue to next tasks (not blocking)
  3. Review ALL deferred findings at final_review checkpoint
```

### Deferred Findings Tracking

```json
{
  "deferred_findings": [
    {
      "from_checkpoint": "RC001C",
      "severity": "MEDIUM",
      "finding_id": "F001",
      "description": "Consider extracting duplicate validation logic",
      "file_path": "packages/auth/service.py",
      "deferred_at": "2025-01-02T10:30:00Z"
    }
  ],
  "final_review_required": true
}
```

### Threshold Configuration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `MIN_REVIEW_BATCH_SIZE` | 3 | Avoid over-reviewing small changes |
| `MAX_REVIEW_BATCH_SIZE` | 10 | Prevent runaway batches without review |
| `SEMANTIC_GROUPING_ENABLED` | true | Toggle semantic vs counter-based |
| `INTEGRATION_REVIEW_TRIGGER` | Component boundary | Catches contract mismatches at handoff points |
| `MAX_BLOCKED_TASKS` | 5 | Limits blast radius of failed review |
| `MAX_REVIEW_ITERATIONS` | 3 | Prevents infinite fix loops |

### Component Extraction Rules

```
extract_component(file_path):
  # Pattern: packages/{component}/...
  IF file_path MATCHES "packages/([^/]+)/":
    RETURN match.group(1)
  
  # Pattern: tests/unit/test_{component}...
  IF file_path MATCHES "tests/unit/test_([^_]+)":
    RETURN match.group(1)
  
  # Fallback: parent directory
  RETURN file_path.parent.name
```

### Summary Rules

| Condition | Action |
|-----------|--------|
| Semantic boundary + batch >= 3 | Insert code_review checkpoint with 3 parallel reviewers |
| Component boundary crossing | Insert integration_review checkpoint |
| End of task list | Insert final_review checkpoint |
| CRITICAL/HIGH finding | Generate fix task, block downstream, re-review |
| MEDIUM/LOW/NIT finding | Add to deferred_findings, continue |

**Semantic Boundaries** (any triggers checkpoint):
- Component change (`packages/auth/` -> `packages/users/`)
- Agent domain shift (`development` -> `quality`)
- Max batch size reached (10 tasks)

---

## Effort Estimation Model

**Reference**: [Effort Estimation Model Details](references/effort-estimation.md)

**Quick Summary**:
- BASE_MINUTES=3, REVIEW_MINUTES=5, ORCHESTRATION_BASE=5
- Per-task complexity: LOC(0.30) + Deps(0.25) + Familiarity(0.25) + Integration(0.20)
- Wall clock = execution + reviews + orchestration

---

## Quality Score Formula

**Calculate after task generation to validate quality**:

```
quality_score = (
  specificity_score x 0.30 +    # All 4 anatomy components present
  agent_match_score x 0.30 +    # Tier 1/2 match with confidence
  tdd_compliance x 0.20 +       # All T###I have T###T pairs
  parallel_optimization x 0.20  # % of tasks marked [P] correctly
)
```

### Dimension Scoring

| Dimension | Score Method |
|-----------|--------------|
| Specificity | 1.0 if all 4 components, -0.25 per missing component |
| Agent Match | avg(task.agent_confidence) across all tasks |
| TDD Compliance | valid_pairs / total_impl_tasks |
| Parallel Optimization | correctly_flagged / eligible_for_parallel |

### Thresholds

| Score | Grade | Action |
|-------|-------|--------|
| >=0.85 | PASS | Output ready for /implement |
| 0.70-0.84 | WARN | Output with warnings, suggest review |
| <0.70 | FAIL | Regenerate with feedback |

---

## Validation Gates

**All gates are BLOCKING - failure prevents output generation**

### Gate 1: Task Anatomy (per-task)

```
FOR each task:
  ASSERT has ACTION_VERB (Create|Modify|Delete|Add|Update|Remove|Implement|Fix)
  ASSERT has SCOPE (what component/module)
  ASSERT has FILE_PATH (absolute or relative path)
  ASSERT has ACCEPTANCE_CRITERIA (testable condition)
```

**Task Anatomy Formula**:
```
TASK = T-ID + [OPERATION] + [PARALLEL] + ACTION_VERB + SCOPE + FILE_PATH + ACCEPTANCE_CRITERIA

Example: "T003 [C] [P] Create MetricResult dataclass in packages/metrics/models.py; pydantic validation succeeds"
```

### Gate 2: TDD Compliance (post-generation)

```
FOR each T###I task:
  ASSERT matching T###T exists
  ASSERT T###T.order < T###I.order
  ASSERT T###T IN T###I.depends_on
```

### Gate 3: Dependency Acyclicity (post-generation)

```
graph = build_dependency_graph(tasks)
IF detect_cycle(graph):
  FAILURE with cycle path and suggested break point
```

### Gate 4: Agent Coverage (per-task)

```
FOR each task:
  ASSERT task.agent IN valid_agent_list OR task.agent_confidence < 0.50
```

---

## PLAN.json Schema Extraction

### Required JSON Keys

| JSON Path | Required | Maps To |
|-----------|----------|---------|
| `phases.phase_N.features[]` | Yes | Implementation items |
| `summary.critical_path` | Yes | Dependencies |
| `metadata.complexity_classification` | Yes | Architecture/complexity |
| `phases.phase_N.features[].acceptance_criteria` | Yes | Testing criteria |

### Schema Extraction Algorithm

```python
def extract_from_json(plan_json):
    required_keys = ["phases", "summary", "metadata"]

    # Validate required top-level keys
    for key in required_keys:
        if key not in plan_json:
            return None  # Missing required key

    # Extract implementation items from phases
    implementation_items = []
    for phase_key, phase in plan_json.get("phases", {}).items():
        for feature in phase.get("features", []):
            implementation_items.append(feature)

    return {
        "implementation_items": implementation_items,
        "dependencies": plan_json.get("summary", {}).get("critical_path", []),
        "complexity": plan_json.get("metadata", {}).get("complexity_classification"),
        "phase_count": len(plan_json.get("phases", {}))
    }
```

### Validation Rules

| Rule | Threshold | Action if Failed |
|------|-----------|------------------|
| Required keys | phases, summary, metadata present | FAILURE: missing_required_keys |
| Features exist | phases contains >=1 feature | WARNING: log empty phases |
| Acceptance criteria | each feature has acceptance_criteria | WARNING: log missing criteria |

---

## Output Format

### tasks.md Structure

```markdown
# Tasks: [Feature Name]

## Summary
- **Total Tasks**: X
- **Parallel Batches**: Y
- **Estimated Time**: Z min

## Task List

### Batch 1 (Parallel)
- T001T [C] [P] Write tests for AuthService in tests/unit/test_auth.py
- T002T [C] [P] Write tests for UserModel in tests/unit/test_user.py

### Batch 2 (Sequential - depends on Batch 1)
- T001I [C] Implement AuthService in packages/auth/service.py
- T002I [C] Implement UserModel in packages/models/user.py

### Review Checkpoint 1
Components: auth, models | Complexity: moderate | Coverage: unit
```

### TASKS.json Schema

```json
{
  "metadata": {
    "feature": "feature-name",
    "generated_at": "ISO-8601",
    "plan_source": "path/to/PLAN.json",
    "quality_score": 0.85
  },
  "tasks": [
    {
      "id": "T001T",
      "operation": "C",
      "parallel": true,
      "action": "Write tests for AuthService",
      "file_path": "tests/unit/test_auth.py",
      "agent": "code-quality",
      "agent_confidence": 0.95,
      "depends_on": [],
      "acceptance_criteria": "All test cases pass"
    }
  ],
  "effort": {
    "total_tasks": 15,
    "parallel_batches": 4,
    "estimated_wall_clock": "25-35 min"
  }
}
```

---

## Anti-Patterns (NEVER DO)

- Keyword-only agent matching ("create" -> development is WRONG)
- Implementation tasks without preceding test tasks (TDD violation)
- Parallel flags on tasks with shared state or same file
- Executing tasks (planning only generates)
- Sub-agent delegation from within task generation
- Sequential sum estimation ("15 tasks x 30 min = 7.5 hours" - ignores parallelism)
- Single-number estimates without breakdown transparency
- Assigning agents without file path analysis
- Missing acceptance criteria on tasks
- Circular dependencies without resolution

---

## Quick Reference

```
T-ID Ranges:
  T0XX-T4XX + T suffix = Test tasks (TDD)
  T0XX-T4XX + I suffix = Implementation tasks (TDD)
  T5XX-T7XX = Standalone (docs, config)
  T8XX = Investigation
  T9XX = Cleanup/debt

TDD Rule: T###T.order < T###I.order (test before impl)

Agent Assignment:
  Tier 1 (0.95): File pattern match
  Tier 2 (0.80): Directory/domain match
  No Match (0.50): Flag for manual review

Parallel [P] Requirements:
  - Different files
  - No import-chain
  - No explicit dependency
  - Different modules
  - Not test-impl pair

Quality Score:
  Specificity(0.30) + AgentMatch(0.30) + TDD(0.20) + Parallel(0.20)
  >= 0.85 = PASS | 0.70-0.84 = WARN | < 0.70 = FAIL

Task Anatomy:
  T-ID + [C/M/D] + [P]? + ACTION + SCOPE + FILE + CRITERIA
```

---

## Thinking Frameworks

**Full Catalog**: [Thinking Frameworks README](../../docs/00-core/frameworks/README.md)

**Most Relevant for Task Generation**:

| Framework | When to Use |
|-----------|-------------|
| [CAGEERF](../../docs/00-core/frameworks/planning.md) | Multi-phase task breakdown |
| [Systems Thinking](../../docs/00-core/frameworks/analysis.md) | Dependency analysis |
| [Pre-Mortem](../../docs/00-core/frameworks/strategy.md) | Validation before output |

> **Selection Tip**: task breakdown->CAGEERF, dependencies->Systems, validation->Pre-Mortem
