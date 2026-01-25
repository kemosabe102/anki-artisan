# Workflow Phases for /implement Command

Detailed documentation for each phase of the implementation workflow.

---

## Phase 1: Discovery (Automated)

**Purpose**: Discover TASKS.json files and build execution plan

**Orchestrator Actions**:
```
GIVEN: feature_dir = docs/01-planning/features/006-opentelemetry/

1. Check feature_dir/tasks/ exists → IF NOT: ERROR
2. Glob: feature_dir/tasks/*/TASKS.json
3. FOR EACH TASKS.json: Extract metadata, dependency_graph
4. Determine execution order (single plan immediate, multiple by dependency)
```

**Output**: `discovered_plans[]` with:
- component_name
- total_tasks
- sprint_points
- depends_on
- execution_order

**Duration**: <5 seconds for 10 plans

**Failures**:
- No tasks/ directory → Suggest `/tasks` → STOP
- No TASKS.json → Suggest `/tasks` → STOP
- Malformed JSON → Report errors → STOP
- Circular dependencies → Report cycle → ESCALATE

---

## Phase 2: Validation (Automated)

**Purpose**: Parse and validate TASKS.json structure

**Validation Checks**:
```
✓ Schema compliance (implement.schema.json v1.0)
✓ Required fields: meta, tasks_generated[], dependency_graph, review_groups[]
✓ Task IDs unique, no collisions
✓ Dependencies valid (all referenced task IDs exist)
✓ Review groups valid (review_task exists, files_in_scope defined)
✓ Agent assignments valid
```

**Output**: `validation_status` (PASS|FAIL)
- plans_validated count
- total_tasks count
- warnings list

**Duration**: <2 seconds for 100 tasks

**Failures**:
- Schema mismatch → Report → STOP
- Missing fields → Report → STOP
- Invalid task IDs → Report → STOP
- Broken dependencies → Report → STOP

**Recovery**: Regenerate with `/tasks` or manually fix TASKS.json

---

## Phase 3: Execution (Automated, Iterative)

**Purpose**: Execute tasks with dependency tracking and parallel processing

### Workflow State Tracking

The orchestrator maintains:
- Current plan being executed
- Tasks completed successfully
- Tasks currently in progress
- Tasks blocked by failures/dependencies
- Review groups that failed validation

### Execution Flow (per plan)

1. **Load Tasks & Dependencies**
   - Read TASKS.json
   - Parse task metadata and dependency graph
   - Sort topologically (dependencies first)

2. **Identify Ready Tasks**
   - Find tasks with all dependencies met
   - Separate parallel-eligible vs sequential-required
   - Apply file conflict detection

3. **Execute Parallel Batch**
   - Launch safe parallel tasks (max 5 agents)
   - Each agent works on different files
   - Wait for all to complete

4. **Execute Sequential Batch**
   - **Regular tasks**: Delegate → 1 retry → escalate
   - **Review checkpoints**: Multi-agent → 3 retries → escalate

5. **Update State**
   - Track completion (completed, blocked, in-progress)
   - Update IMPLEMENTATION_PROGRESS.md

6. **Continue Until Done**
   - Repeat until queue empty or all blocked

### File Conflict Detection

**Purpose**: Prevent parallel agents editing same file

**Process**:
1. Build file-to-task mapping for parallel batch
2. Identify conflicts (multiple tasks → same file)
3. Move conflicts to sequential batch

**Principle**: File safety over speed

### Progress Tracking (IMPLEMENTATION_PROGRESS.md)

**Location**: `{feature_dir}/IMPLEMENTATION_PROGRESS.md`

**Updates At**:
- First run: Create template
- Review group start: Update current status
- Review group completion: Add to completed section
- Review group blocked: Mark with reason
- Phase completion: Update phase status

**Key Sections**:
- Overall Progress (percentage)
- Completed Review Groups (with timestamps, iterations)
- Next Review Group
- Remaining Work
- Lessons Learned
- Quality Metrics
- Resume Instructions

---

## Phase 4: Completion Report (Automated)

**Purpose**: Present feature completion summary

**Report Template**:
```markdown
## Implementation Complete: [Feature Name]
**Plans**: N | **Tasks**: M/M (100%) | **Duration**: X hrs | **Status**: ✅

### Executive Summary
- M tasks completed (P% success)
- R review checkpoints passed
- B blocking issues resolved

### Plan Breakdown
#### 001-infrastructure-foundation (8 SP) ✅
- Tasks: 29/29 (100%)
- Review Groups: 4/4 passed (RG001: 1 iter, RG003: 2 iter)
- Files Changed: 5

### Implementation Metrics
**Review Performance**: 79% first attempt | 14% 1 retry | 7% 2 retries
**Agent Distribution**: implementer 53% | code-quality 12% | reviewer 18%

### Next Steps
1. ✅ Ready for /git commit
2. 🎯 Monitor in production
```

**Duration**: Instant (synthesis from tracked state)

---

## Phase Transitions

```
PHASE 1 (Discovery)
    ↓ SUCCESS: discovered_plans[] populated
    ↓ FAILURE: No tasks → Suggest /tasks → STOP
    
PHASE 2 (Validation)
    ↓ SUCCESS: validation_status = PASS
    ↓ FAILURE: Schema errors → Report → STOP

PHASE 3 (Execution)
    ↓ SUCCESS: All tasks completed
    ↓ PARTIAL: Some blocked → Report → Continue independent
    ↓ FAILURE: All blocked → Escalate

PHASE 4 (Report)
    ↓ Always reached (even with partial success)
    ↓ Shows completion status and next steps
```

---

## State Persistence Architecture

### Dual-File Approach

The `/implement` command uses two files for state persistence, each optimized for different consumers:

| File | Purpose | Format | Consumer |
|------|---------|--------|----------|
| `IMPLEMENTATION_STATE.json` | Machine-parseable execution state | JSON | Orchestrator (resume logic) |
| `IMPLEMENTATION_PROGRESS.md` | Human-readable progress report | Markdown | Developers (visibility) |

**Why Two Files?**
- **Separation of Concerns**: Machine parsing requires predictable structure; human visibility requires readable prose
- **Reliability**: JSON parsing is deterministic; Markdown parsing is fragile (regex-dependent, whitespace-sensitive)
- **Independence**: Updates to human-readable sections cannot corrupt machine state

### When to Write Each File

| Event | IMPLEMENTATION_STATE.json | IMPLEMENTATION_PROGRESS.md |
|-------|---------------------------|----------------------------|
| Execution starts | CREATE (meta, empty tasks) | CREATE (template) |
| Task completes | UPDATE (task status, checksums) | - |
| Task fails | UPDATE (error_details, blocked_by) | - |
| Review checkpoint starts | UPDATE (review_group status) | UPDATE (current status) |
| Review iteration completes | UPDATE (fix_history, iteration++) | UPDATE (iteration count) |
| Review group passes | UPDATE (status=passed) | UPDATE (add to completed) |
| Review group escalates | UPDATE (unresolved_issues) | UPDATE (mark blocked) |
| Phase completes | UPDATE (current_phase, statistics) | UPDATE (phase status) |
| Execution completes | UPDATE (status=completed) | UPDATE (final report) |

**Write Frequency**:
- `IMPLEMENTATION_STATE.json`: After EVERY task completion (ensures resume can recover from any point)
- `IMPLEMENTATION_PROGRESS.md`: At review checkpoints only (reduces I/O, human-visible changes)

### Resume Logic Using IMPLEMENTATION_STATE.json

```
ON /implement --resume:
1. READ IMPLEMENTATION_STATE.json
   - IF NOT EXISTS: ERROR "No state to resume from"
   - IF schema_version mismatch: WARN + attempt migration

2. VALIDATE file checksums
   FOR EACH file in file_checksums:
     current_checksum = SHA256(file)
     IF current_checksum != stored_checksum:
       CONFLICT DETECTED
       - IF file was modified by completed task: WARN (external modification)
       - IF file was modified by in_progress task: RECOVER (re-execute task)

3. RECONSTRUCT execution state
   - pending_tasks = tasks WHERE status IN (pending, in_progress)
   - blocked_tasks = tasks WHERE status = blocked
   - active_review = review_groups WHERE status = in_progress

4. DETERMINE resume point
   - IF active_review EXISTS: Resume from review checkpoint (iteration N)
   - ELSE: Resume from first pending task

5. INCREMENT meta.resume_count
6. CONTINUE execution from resume point
```

### Checksum-Based Conflict Detection

**Purpose**: Detect external file modifications between sessions that could cause inconsistencies.

**Process**:
1. Before task execution: Record `checksum_before` (SHA-256)
2. After task completion: Record `checksum_after` (SHA-256)
3. On resume: Compare stored `checksum_after` with current file checksum

**Conflict Resolution**:

| Scenario | Detection | Resolution |
|----------|-----------|------------|
| No change | stored == current | Continue normally |
| External edit to completed task's file | stored != current | WARN user, continue (trust external edit) |
| External edit to in-progress task's file | stored != current | Re-execute task (state was incomplete) |
| File deleted | file not found | Re-execute task that created it |

### Oscillation Prevention

The `fix_history` array in review groups tracks which issues were addressed by which agent in each iteration. This enables detection of "fix oscillation" where:
- Iteration 1: Agent A fixes issue X
- Iteration 2: Agent B introduces issue X again while fixing Y
- Iteration 3: Agent A fixes issue X again...

**Detection**: If same issue appears in 2+ iterations, escalate immediately (don't retry).

### Schema Reference

See `schemas/implementation-state.schema.json` for complete field definitions.

**Key Sections**:
- `meta`: Execution metadata (phase, status, timestamps, resume_count)
- `tasks`: Per-task state map (status, checksums, error_details)
- `review_groups`: Per-review-group state (iteration, fix_history, unresolved_issues)
- `blocked_cascade`: Dependency blocking graph (root_blockers, cascade_map)
- `file_checksums`: Current checksums for conflict detection
- `statistics`: Aggregated metrics for completion report

---

## Context Budget by Phase

| Phase | Context Usage |
|-------|---------------|
| Discovery | 1-2k tokens |
| Validation | 1-2k tokens |
| Execution | 10-15k tokens |
| Completion | 5-8k tokens |
| **Total** | **17-27k (8-14%)** |

**Target**: <20k tokens (10% of 200k)
