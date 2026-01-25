# Workflow Phases

Detailed documentation for the 7-step task generation workflow.

---

## Step 1: Argument Parsing & Validation

**Purpose**: Validate user input and normalize paths.

**Input**: `$ARGUMENTS` (feature directory path)

**Process**:
```
GIVEN: FEATURE_DIR = [user provided path]

VALIDATE:
- Path exists and is a directory
- Path is within project workspace (docs/ or other approved location)
- Convert to absolute path for reliability

IF invalid:
  ERROR "Invalid directory: [path]"
  HINT: "Usage: /tasks path/to/feature/directory/"
  EXAMPLES:
    - /tasks docs/01-planning/features/005-regenerative-orchestration-system/
    - /tasks docs/01-planning/specifications/002-executable-task-system/
```

**Output**: Validated absolute path to FEATURE_DIR

---

## Step 2: Directory Discovery

**Purpose**: Intelligently discover plan and context files in any structure.

**Discovery Patterns**:

### Context Files (priority order)
1. SPEC.md, spec.md
2. README.md, readme.md  
3. RATIONALE.md, rationale.md
4. feature.md, FEATURE.md
5. Any *.md in root describing the feature

### Plan Files (flexible patterns)
1. `plans/**/*.md` - Any .md in plans/ subdirectory
2. `*plan*.md`, `*PLAN*.md` - Case-insensitive plan pattern
3. `phase-*.md`, `PHASE-*.md` - Phase-based structure
4. `component-*.md`, `COMPONENT-*.md` - Component-based structure

**Tools Used**:
- `Glob("*.md")` in FEATURE_DIR for context files
- `Glob("plans/**/*.md")` for plan subdirectory
- `Glob("**/*plan*.md", -i=true)` for plan pattern matches

**Output Structure**:
```json
{
  "feature_dir": "absolute/path/to/feature",
  "context_files": ["SPEC.md", "RATIONALE.md", "README.md"],
  "plan_files": [
    "plans/phase-0-operational-foundation.md",
    "plans/phase-1-ooda-framework.md"
  ],
  "task_dir": "absolute/path/to/feature/tasks"
}
```

---

## Step 3: Feature Context Synthesis

**Purpose**: Understand feature structure and extract metadata for intelligent task generation.

**Agent**: `researcher-codebase`

**Framework**: CAGEERF (Context → Analysis → Goals → Execution → Evaluation → Refinement → Framework)

**Expected Output**:
```json
{
  "feature_name": "regenerative-orchestration-system",
  "feature_number": "005",
  "feature_description": "High-level summary from context files",
  "plan_structure": "sequential_phases | parallel_components | mixed",
  "plans": [
    {
      "file": "plans/phase-0-foundation.md",
      "name": "Operational Foundation",
      "component_name": "phase-0-foundation",
      "type": "foundation | core | enhancement",
      "estimated_tasks": 15,
      "depends_on": [],
      "priority": "high"
    }
  ],
  "confidence": 0.85
}
```

**Fallback Strategy** (if synthesis fails or confidence < 0.5):
- feature_name: basename(feature_dir)
- plan_structure: "parallel_components" (safest default)
- All plans get type: "core", priority: "medium"

---

## Step 4: Parallel Task Generation

**Purpose**: Generate tasks for all plans simultaneously.

**Framework**: Cynefin (classify complexity domain → select appropriate strategy)

**Key Operations**:

### 1. Generate Shared Timestamp
```
execution_timestamp = ISO 8601 UTC format
Use once for all planning agents (consistency)
```

### 2. Calculate Task ID Offsets
```
Component 0: offset = 0   (T001-T099)
Component 1: offset = 100 (T101-T199)
Component 2: offset = 200 (T201-T299)
```

### 3. Prepare Task-Creator Inputs
For each plan, create input JSON with:
- task_id_offset
- component_context (name, type, dependencies)
- feature_context (name, description, structure)
- output_dir

### 4. Launch Parallel Agents
```markdown
PARALLEL EXECUTION (single message):
Task(planning, plan-0 input)
Task(planning, plan-1 input)
Task(planning, plan-2 input)

BENEFITS:
- 3-5x faster than sequential
- Each agent focuses on single plan
- Natural isolation via directories
```

**Output**: tasks.md + TASKS.json per component

---

## Step 5: Result Collection & Validation

**Purpose**: Aggregate results and validate success.

**Process**:
```
FOR EACH agent output:

IF SUCCESS:
  ✅ Extract: component_name, tasks_created, parallel_tasks, 
     sequential_tasks, review_groups, agent_distribution
  ✅ Verify: ${output_dir}/tasks.md exists
  ✅ Verify: ${output_dir}/TASKS.json exists

IF FAILURE:
  ❌ Extract: component_name, error_message, suggestions
  ❌ Store in failure_results
```

**Aggregated Metrics**:
- total_tasks = sum of tasks_created
- total_parallel = sum of parallel_tasks  
- total_sequential = sum of sequential_tasks
- agent_distribution = merged counts across components

---

## Step 6: Task Quality Validation

**Purpose**: Multi-agent review of generated tasks.

**Framework**: DMAIC (Define → Measure → Analyze → Improve → Control)

**Core Agents (ALWAYS - 75% weight)**:
| Agent | Focus | Weight |
|-------|-------|--------|
| planning | Business alignment | 25% |
| architecture | Technical design | 25% |
| tech-debt-investigator | Task quality | 25% |

**Dynamic Agents (0-2 if confidence >0.8 - 25% split)**:
| Agent | Trigger Condition |
|-------|-------------------|
| feature-analyzer | 3+ plan components |
| code-quality | Test-heavy feature |
| code-quality | Low test coverage in plans |

**Launch Pattern**:
```markdown
Single message with 3-5 Task calls:
Task(planning, validation_input)
Task(architecture, validation_input)
Task(tech-debt-investigator, validation_input)
Task(feature-analyzer, validation_input)  # if >0.8 confidence
```

**Synthesis**:
- If 3+ overlapping findings (similarity >0.7): Apply synthesis framework
- Calculate weighted validation score
- Determine: APPROVED | NEEDS_FIXES | BLOCKED

---

## Step 7: Present Results

**Purpose**: Clear summary with next steps.

**Template Selection**:
| Condition | Template |
|-----------|----------|
| Single plan | Single Plan Summary |
| Multiple plans, all success | Multi-Plan Summary |
| Partial success | Multi-Plan + Failures |
| All failed | Failure Report |

**Always Include**:
- Status indicator (✅ ⚠️ ❌)
- Task counts and distribution
- Output file locations
- Validation results (if Step 6 ran)
- Next steps guidance

**Quality Metrics**:
- Parallel execution potential (%)
- Review coverage (groups per tasks)
- Confidence scores
- Speedup factor (parallel vs sequential)
