# Parallel Execution Protocol

**Purpose**: Complete parallelization patterns, scaling limits, and execution strategies

**Auto-loaded**: No (on-demand reference from orchestrator-workflow.md)

---

## Core Principle

**Quick Rule**: Parallel for reads, sequential for writes. ALWAYS sequential for `.claude/**` directory.

---

## When to Parallelize

### ✅ Parallel Execution (3-5x faster)

**Safe Patterns**:

**1. Multiple Files in Different Directories**
```python
# Different directories, no conflicts:
Task(agent="planning", prompt="Enhance docs/plans/core-PLAN.md")
Task(agent="planning", prompt="Enhance docs/plans/analysis-PLAN.md")
Task(agent="planning", prompt="Enhance docs/plans/integration-PLAN.md")
# Result: 2min instead of 6min (3x faster)
```

**2. Independent Research Tasks**
```python
# Read-only, no file conflicts:
Task(agent="researcher-external", prompt="Research OAuth2 best practices")
Task(agent="researcher-codebase", prompt="Find auth patterns in packages/auth/**")
Task(agent="researcher-external", prompt="FastAPI auth documentation")
# Result: 1.5min instead of 4.5min (3x faster)
```

**3. Multi-Agent Analysis**
```python
# Independent analysis, different perspectives:
Task(agent="code-quality", prompt="Security review of auth module")
Task(agent="code-quality", prompt="Run auth test suite")
Task(agent="tech-debt-investigator", prompt="Analyze auth coupling")
# Result: 2min instead of 6min (3x faster)
```

---

## When to Use Sequential

### ❌ Sequential Execution (MANDATORY)

**Unsafe Patterns** (MUST serialize):

**1. Any Modifications to `.claude/**` Directory** (CRITICAL)
```python
# File locking on Windows - 99% Edit failure rate if parallel:
Task(agent="claude-code-ecosystem", prompt="Update .claude/agents/debugger.md")
# WAIT for completion before:
Task(agent="claude-code-ecosystem", prompt="Update .claude/agents/code-quality.md")
```

**Why**: Windows file locking in `.claude/` directory causes Edit tool failures

**2. Single File Modifications by Multiple Agents**
```python
# Same file, conflicting edits:
Task(agent="planning", prompt="Add business context to core-PLAN.md")
# WAIT before:
Task(agent="architecture", prompt="Add technical design to core-PLAN.md")
```

**3. Agent Dependencies** (Output of A feeds into B)
```python
# Sequential required:
Task(agent="/spec", prompt="Create SPEC.md")
# WAIT for SPEC.md to exist before:
Task(agent="planning", prompt="Create PLAN.md from SPEC.md")
```

---

## Agent Scaling Limits

**Context-Specific Constraints**:

### File Modification Agents: MAX 5

**Reason**: Approval management, file system constraints, Edit tool rate limiting

**Example**:
```python
# MAX 5 parallel file modifications:
Task(agent="planning", prompt="Enhance plan1.md")
Task(agent="planning", prompt="Enhance plan2.md")
Task(agent="planning", prompt="Enhance plan3.md")
Task(agent="planning", prompt="Enhance plan4.md")
Task(agent="planning", prompt="Enhance plan5.md")
# DO NOT exceed 5 concurrent file modification agents
```

---

### Research Workers: MAX 5

**Reason**: Read-only operations, parallel safe, but token/API rate limits

**Example**:
```python
# MAX 5 parallel research workers:
Task(agent="researcher-codebase", prompt="Pattern 1")
Task(agent="researcher-codebase", prompt="Pattern 2")
Task(agent="researcher-external", prompt="Best practice 1")
Task(agent="researcher-external", prompt="Best practice 2")
Task(agent="researcher-external", prompt="Library docs")
# Optimal parallelization
```

---

### Review Agents: 3-5 Optimal, MAX 10

**Reason**: Diminishing returns beyond 5, MAX 10 for comprehensive validation

**Example**:
```python
# 3 core agents (always included):
Task(agent="planning", prompt="Business review")
Task(agent="architecture", prompt="Technical review")
Task(agent="tech-debt-investigator", prompt="Debt analysis")

# +2 dynamic agents (confidence >0.8):
Task(agent="code-quality", prompt="Security review")
Task(agent="code-quality", prompt="Test validation")

# Total: 5 agents (optimal)
```

---

### Practical Limit: 15-20 Agents Total

**Composition**:
- 5 file modification agents
- 5 research workers
- 10 review agents
- **Total**: Up to 20 agents in single workflow

**Performance**: Linear scaling within limits

**Example Workflow**:
```
ORIENT phase (parallel):
  ├─ 5 research workers (1.5min)
  └─ 3 review agents (2min)

DECIDE phase (sequential):
  └─ 1 hypothesis-former (30s)

ACT phase (parallel):
  └─ 5 file modification agents (2min)

Total: ~4min instead of 15min sequential (3.75x faster)
```

---

## Performance Metrics

### Linear Scaling

**Formula**: `Total Time = max(agent_time) for parallel work`

**Example**:
```
Sequential: 5 agents × 2min = 10min
Parallel: max(2min, 2min, 2min, 2min, 2min) = 2min
Speedup: 5x faster
```

---

### Concurrent Capacity

**Limits**:
- Tool call parallelization: Claude Code handles scheduling
- API rate limits: Auto-throttling by platform
- File system: Windows locking constraints for `.claude/**`

---

## Complete Use Cases

### Use Case 1: Multi-Component Feature Planning

**Scenario**: Create plans for 3-component feature

**Sequential Approach** (slow):
```
/spec: Create SPEC.md (2min)
→ planning: core-PLAN.md (2min)
→ planning: analysis-PLAN.md (2min)
→ planning: integration-PLAN.md (2min)
Total: 8min
```

**Parallel Approach** (fast):
```
/spec: Create SPEC.md (2min)
→ [Parallel launch after SPEC exists]:
  ├─ planning: core-PLAN.md (2min)
  ├─ planning: analysis-PLAN.md (2min)
  └─ planning: integration-PLAN.md (2min)
Total: 4min (2x faster)
```

---

### Use Case 2: Multi-Agent Research

**Scenario**: Research authentication patterns

**Sequential Approach** (slow):
```
researcher-external: OAuth2 best practices (2min)
→ researcher-codebase: Existing auth patterns (1.5min)
→ researcher-external: FastAPI auth docs (1min)
Total: 4.5min
```

**Parallel Approach** (fast):
```
[Parallel launch]:
  ├─ researcher-external: OAuth2 best practices (2min)
  ├─ researcher-codebase: Existing auth patterns (1.5min)
  └─ researcher-external: FastAPI auth docs (1min)
Total: 2min (max of parallel times) (2.25x faster)
```

---

### Use Case 3: Multi-Agent Validation

**Scenario**: Validate feature implementation

**Parallel Approach** (optimal):
```
[Parallel launch - 3 core + 2 dynamic]:
  ├─ planning: Business review (30s)
  ├─ architecture: Technical review (1.5min)
  ├─ tech-debt-investigator: Debt analysis (1min)
  ├─ code-quality: Security review (1.5min)
  └─ code-quality: Test validation (1min)
Total: 1.5min (max of parallel times)
```

---

## Orchestrator Implementation Pattern

### Pre-Flight Check

**Before parallel launch**:
```python
# 1. Count pending modification agents
modification_agents = count_pending_edits()

# 2. Enforce limits
if modification_agents >= 5:
    # Serialize remaining agents
    queue_for_sequential_execution()
else:
    # Safe to parallelize
    launch_parallel()

# 3. Special case: .claude/** directory
if any(path.startswith('.claude/') for path in target_paths):
    # ALWAYS serialize .claude/** modifications
    force_sequential_execution()
```

---

### Launch Pattern

**Single message with multiple Task calls**:
```python
# Orchestrator launches all in one message:
# Launch 3 agents simultaneously in single response
Task(agent="planning", prompt="Enhance core-PLAN.md")
Task(agent="planning", prompt="Enhance analysis-PLAN.md")
Task(agent="planning", prompt="Enhance integration-PLAN.md")
```

---

### Completion Handling

**After parallel execution**:
```python
# 1. Collect all agent outputs
results = [agent1_output, agent2_output, agent3_output]

# 2. Verify all succeeded
for result in results:
    if result.status == "FAILURE":
        handle_failure(result)

# 3. Synthesize if overlap detected
if detect_overlap(results, threshold=0.7):
    apply_synthesis_framework()

# 4. Present consolidated findings
return synthesized_recommendations
```

---

## Critical Rules Summary

**ALWAYS Parallel**:
- Multiple files in different directories ✅
- Independent research tasks ✅
- Multi-agent analysis (no file conflicts) ✅

**ALWAYS Sequential**:
- `.claude/**` directory modifications ❌ (file locking)
- Single file by multiple agents ❌ (conflicts)
- Agent dependencies (A → B) ❌ (ordering)

**Scaling Limits**:
- File modifications: MAX 5
- Research workers: MAX 5
- Review agents: 3-5 optimal, MAX 10
- Total: 15-20 practical limit

---

**This protocol provides complete parallelization guidance for orchestrator execution optimization.**
