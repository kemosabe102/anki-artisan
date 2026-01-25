# Workflow Analysis Domain Expertise

Domain knowledge for analyzing slash command workflows in Claude Code.

---

## Command Workflow Anatomy

### Standard Command Structure

```markdown
---
argument-hint: <placeholder>
description: Brief description with trigger keywords
allowed-tools: Tool1, Tool2, Tool3
model: opus|sonnet|haiku
---

# Command Name

## Phase 1: [Name]
### Step 1.1: [Action]
...

## Phase 2: [Name]
...
```

### Key Components

| Component | Purpose | Analysis Focus |
|-----------|---------|----------------|
| Frontmatter | Configuration | Field validation, tool permissions |
| Phases | Major workflow stages | Ordering, dependencies |
| Steps | Atomic operations | Sequential vs parallel |
| Gates | Decision points | Exit criteria, thresholds |
| Task() | Agent delegation | Agent existence, tool match |
| Skill() | Skill invocation | Skill availability |

---

## Workflow Patterns

### Linear Workflow
```
P1 -> P2 -> P3 -> Output
```
- Simple sequential execution
- Each phase depends on previous
- Easy to validate ordering


### Branching Workflow
```
P1 -> [Gate] -> P2a (if condition)
            -> P2b (else)
      -> P3
```
- Conditional execution paths
- Requires gate criteria
- Must handle both branches

### Parallel Workflow
```
P1 -> [P2a, P2b, P2c] (parallel) -> P3
```
- Multiple operations simultaneously
- Independence required
- Synchronization at join

### Hybrid Workflow
```
P1 -> [P2a, P2b] -> [Gate] -> P3a | P3b -> [P4a, P4b] -> P5
```
- Combination of patterns
- Most complex to analyze
- Highest optimization potential

---

## Dependency Types

### Explicit Dependencies
- Output of Step N used as input to Step M
- Clearly stated in workflow text
- Example: "Using results from Step 2.1..."

### Implicit Dependencies
- Shared file access
- Agent state assumptions
- Tool availability
- Example: File written in P1, read in P2

### Temporal Dependencies
- Order-dependent operations
- Setup/teardown relationships
- Example: "After validation completes..."

---

## Common Anti-Patterns

### 1. Circular Dependencies
**Symptom**: Step A depends on Step B which depends on Step A
**Detection**: DAG cycle detection
**Fix**: Restructure to break cycle

### 2. Unsafe Parallelization
**Symptom**: Parallel steps modify same resource
**Detection**: Shared state analysis
**Fix**: Serialize or use coordination


### 3. Missing Gates
**Symptom**: Decision points without criteria
**Detection**: Branch without condition
**Fix**: Add explicit gate with exit criteria

### 4. Orphaned Agents
**Symptom**: Task() to non-existent agent
**Detection**: Agent existence check
**Fix**: Create agent or use existing

### 5. Tool Permission Mismatch
**Symptom**: Agent lacks tools for delegated task
**Detection**: Compare agent tools to operation
**Fix**: Add tools or delegate to different agent

### 6. No Error Recovery
**Symptom**: No handling for failure cases
**Detection**: Missing error section
**Fix**: Add retry, fallback, escalation

---

## Validation Heuristics

### Ordering Validation
1. Build DAG from dependencies
2. Topological sort succeeds = valid ordering
3. Cycle detection = ordering violation

### Parallelization Check
1. Identify parallel groups
2. For each group, check:
   - No shared file writes
   - No output->input between parallel steps
   - No shared agent instance
3. Flag violations

### Gate Completeness
1. Identify decision points (if/else, gates)
2. Check exit criteria defined
3. Verify all branches have handling
4. Check timeout defined

### Agent Verification
1. Extract Task() targets
2. Glob for agent files
3. Parse agent frontmatter
4. Compare tools declared vs required

---

## Quality Indicators

### High-Quality Workflow Signs
- Clear phase separation
- Explicit dependencies documented
- Gates at every decision point
- Comprehensive error handling
- Appropriate parallelization

### Low-Quality Workflow Signs
- Monolithic single-phase
- Implicit dependencies
- Missing gates
- No error handling
- Over-parallelization or under-parallelization
