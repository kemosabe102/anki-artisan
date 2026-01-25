---
title: "Agent Parallelization Strategy"
date: 2025-11-08
status: ACTIVE
tags: [agents, claude-docs]
---
# Agent Parallelization Strategy

**Purpose**: Strategic guidance for when and how to delegate work to multiple agents in parallel

**Audience**: CLAUDE.md (orchestrator), researcher-lead (delegation planning)

**Scope**: Agent coordination and delegation strategy. For tool-level parallelization, see `tool-parallelization-patterns.md`

## Core Principle

**Independent Agents for Independent Tasks**

Launch multiple agents in parallel when tasks are truly independent with no sequential dependencies.

## When to Launch Parallel Agents

### Multiple Independent Files/Components

- **3-5 files**: Launch 3-5 agents (one per file)
- **6-10 files**: Launch 5 agents, then next 1-5 when complete
- **10+ files**: Process in batches of 5 agents maximum

**Example**:

```markdown
Task: Migrate 15 agent prompts

Batch 1 (5 agents):

- development: agent1.md
- development: agent2.md
- development: agent3.md
- development: agent4.md
- development: agent5.md
  Wait for completion

Batch 2 (5 agents):

- development: agent6.md through agent10.md
  Wait for completion

Batch 3 (5 agents):

- development: agent11.md through agent15.md
```

### Multi-Source Research

- **Different sources**: researcher-codebase + researcher-external in parallel
- **Different topics**: Multiple researcher-external agents for independent queries
- **Breadth-first exploration**: researcher-lead coordinates parallel workers

**Example**:

```markdown
Task: Research authentication best practices

Parallel delegation:

- researcher-codebase: "Analyze existing auth implementation"
- researcher-external: "Research OWASP authentication patterns 2025"
- researcher-external: "Get pydantic validation patterns for auth"

Result: 3 independent research streams, synthesize findings
```

### Independent Analysis Tasks

- **Different modules**: code-quality on separate components
- **Different features**: feature-analyzer on independent specifications
- **Different aspects**: architecture + planning on same plan (different concerns)

## When to NEVER Parallelize Agents

### Sequential Dependencies

- **Implementation pipeline**: Spec → Plan → Implementation (each depends on previous)
- **Interface contracts**: Define interface before implementations
- **Database migrations**: Order matters for schema changes
- **Build pipelines**: Build → Test → Deploy stages

**Example**:

```markdown
❌ Parallel (WRONG):

- /spec: Create spec
- planning: Create plan (needs spec first!)
- development: Implement feature (needs plan first!)

✅ Sequential (CORRECT):

1. /spec: Create spec → Complete
2. planning: Create plan → Complete
3. development: Implement feature
```

### Shared State Requirements

- **Same file modifications**: Multiple agents editing same file = conflicts
- **Integration points**: Components that must integrate consistently
- **Coordinated changes**: Refactoring across tightly coupled modules

---

## ⚠️ DEPRECATED SECTIONS BELOW

**Deprecation Notice**: The sections below ("Low-Value Tasks" and "When Direct Handling is Better") are deprecated as of 2025-10-31.

**Reason**: Delegation-first principle supersedes performance optimization. ALL tasks now go through agent selection with confidence scoring.

**Current Guidance**: See CLAUDE.md "Delegation Decision Framework" section for up-to-date decision process:

- Confidence ≥ 0.5 → Delegate to specialist
- Confidence < 0.5 → Orchestrator handles directly (signals agent gap)

**Historical Context**: These sections reflected earlier performance-focused thinking where "simple tasks = direct work faster". Experience showed that domain specialization provides greater quality benefits than marginal time savings.

---

### Low-Value Tasks

- **Simple single-file tasks**: Direct implementation faster than delegation
- **1-2 file analysis**: Overhead not worth complexity
- **Quick fixes**: Direct tool usage more efficient

## Scaling Rules (Orchestrator)

### Agent Batch Sizing

**Maximum Simultaneous Agents**: 5

- Prevents resource exhaustion
- Maintains reasonable coordination complexity
- Balances throughput with overhead

**Scaling Pattern**:

```markdown
1-2 files → Handle directly OR 1 agent
3-5 files → 3-5 agents (single batch)
6-10 files → 5 agents → Wait → 1-5 agents
11-15 files → 5 agents → Wait → 5 agents → Wait → 1-5 agents
16+ files → Question scope (too large?)
```

### When Direct Handling is Better

- **1 file tasks**: Use tools directly (Read, Edit, etc.)
- **Simple queries**: Direct search faster than agent delegation
- **Quick validation**: Direct tool calls sufficient

## Anthropic Research Patterns

### Optimal Use Cases for Parallel Agents

**Breadth-First Exploration**:

- ✅ "Analyze authentication across 50 microservices" (50 parallel analyses)
- ✅ "Research design patterns for 10 different domains" (10 parallel researchers)
- ✅ "Review 15 SPEC files for consistency" (batched reviews)

**Large-Scale Information Gathering**:

- ✅ Multi-source research (web + docs + codebase in parallel)
- ✅ Comprehensive codebase analysis (split by module/package)
- ✅ Independent feature analysis (parallel feature-analyzer agents)

**Complex Tool Interfaces**:

- ✅ Different tool sets per agent (codebase tools vs web tools)
- ✅ Specialized research domains (researcher-external auto-routes based on query)

### Anti-Patterns (Don't Do This)

**Excessive Parallelization**:

- ❌ 50 agents for simple query (use 1 agent with tool parallelization)
- ❌ Parallel when 1 agent sufficient (overhead > benefit)
- ❌ Fine-grained splitting (each agent < 30 seconds work)

**Tight Dependencies**:

- ❌ Most implementation tasks (interfaces depend on contracts)
- ❌ Coordinated refactoring (changes must be consistent)
- ❌ Sequential workflows (output A → input B)

**Shared Context Requirements**:

- ❌ All agents need same full codebase context (wasteful)
- ❌ State must be consistent across agents (coordination overhead)
- ❌ Real-time coordination needed (sequential better)

## researcher-lead Delegation Planning

**Role**: Creates parallel execution plans for orchestrator to execute

### Creating Delegation Plans

**Four-Component Structure**:

1. **Overall Objective**: Clear research goal
2. **Worker Tasks**: 3-5 specific tasks for parallel workers
3. **Synthesis Approach**: How to combine findings
4. **Success Criteria**: When research is complete

**Example Delegation Plan**:

```markdown
Overall Objective: Research JSON schema validation patterns

Worker Tasks (parallel):

1. researcher-codebase: "Find all JSON schema usage in src/"
2. researcher-external: "Get pydantic JSON schema patterns"
3. researcher-external: "Research JSON Schema 2020-12 best practices"
4. researcher-codebase: "Analyze test patterns for schema validation"

Synthesis Approach:

- Combine codebase patterns with library best practices
- Identify gaps between current implementation and standards
- Recommend migration path if needed

Success Criteria:

- Current usage patterns documented
- Best practices identified with sources
- Migration recommendations (if applicable)
```

### Bite-Sized Component Strategy

**Principle**: Break large research into parallel-executable chunks

**Good Decomposition**:

- Each task: 1-3 minutes work
- Independent findings
- Clear boundaries
- Minimal overlap

**Example**:

```markdown
Large Task: "Understand authentication system"

❌ Poor decomposition:

- Task 1: "Research everything about auth"
  (Too broad, not parallelizable)

✅ Good decomposition:

- Task 1: "Find all authentication entry points (login, OAuth, API keys)"
- Task 2: "Analyze session management implementation"
- Task 3: "Review test coverage for auth modules"
- Task 4: "Research industry best practices (OWASP, NIST)"

Result: 4 parallel workers, ~3x faster than sequential
```

### Parallel Execution Recommendations

**researcher-lead should recommend**:

1. Number of workers (typically 3-5)
2. Task assignments per worker
3. Expected completion time
4. How to synthesize findings

**researcher-lead does NOT**:

- Execute the parallel workers (orchestrator does this)
- Coordinate worker-to-worker communication (no inter-agent messaging)
- Make orchestration decisions (orchestrator's role)

## Performance Benefits

### Measured Improvements

- **90% time reduction** for complex multi-source research
- **3-5x faster** for multi-component analysis (3-5 agents)
- **Linear scaling** up to 5 agents (diminishing returns beyond)
- **No timeout concerns** when properly decomposed

### Token Economics

**Cost Model**:

- **Single agent**: ~4x tokens vs direct chat
- **Parallel agents**: Each gets independent 200k context
- **Total cost**: Linear with agent count (5 agents = 20x tokens)

**Value Justification**:

- Use for high-value research tasks only
- Time savings (90%) must justify token cost (20x)
- Prefer direct tool usage for simple tasks

**Performance Variance**:

- Token usage explains 80% of performance differences
- Well-decomposed tasks see better parallelization benefits
- Poorly decomposed tasks waste tokens on coordination

## Delegation Patterns

### Pattern 1: Parallel Research Workers

```markdown
researcher-lead creates plan with 4 tasks

Orchestrator executes:
<tool_calls>
<Task agent="researcher-codebase" task="Task 1"/>
<Task agent="researcher-external" task="Task 2"/>
<Task agent="researcher-external" task="Task 3"/>
<Task agent="researcher-codebase" task="Task 4"/>
</tool_calls>

All workers execute in parallel
Orchestrator synthesizes findings when complete
```

### Pattern 2: Batched Implementation

```markdown
10 files need modification

Orchestrator executes:
Batch 1:
<tool_calls>
<Task agent="development" task="Modify file1.py"/>
<Task agent="development" task="Modify file2.py"/>
<Task agent="development" task="Modify file3.py"/>
<Task agent="development" task="Modify file4.py"/>
<Task agent="development" task="Modify file5.py"/>
</tool_calls>

Wait for completion

Batch 2:
<tool_calls>
<Task agent="development" task="Modify file6.py"/>
... (remaining 5 files)
</tool_calls>
```

### Pattern 3: Sequential Phases with Internal Parallelization

```markdown
Phase 1: Research (parallel agents)
→ researcher-lead creates 5-worker plan
→ Orchestrator launches 5 workers in parallel
→ Wait for all workers

Phase 2: Synthesis (single orchestrator)
→ Combine findings from all workers
→ Identify patterns and recommendations

Phase 3: Implementation (parallel agents if independent)
→ Launch development agents for independent components
→ Batched if >5 components
```

## Special Constraints

### .claude/ Directory

- **Rule**: Sequential only, even for different files
- **Reason**: File watcher and locking prevent concurrent modifications
- **Strategy**: Batch agent operations on .claude/ files sequentially

### Integration Points

- **Rule**: Define contracts first, then parallel implementations
- **Pattern**: Sequential contract definition → Parallel implementations
- **Reason**: Implementations depend on stable interfaces

## Decision Matrix

| Scenario                      | Parallel Agents?                    | Rationale                    |
| ----------------------------- | ----------------------------------- | ---------------------------- |
| 5 independent files to modify | ✅ Yes (5 developments) | Independent, no shared state |
| Research web + codebase       | ✅ Yes (2 researchers)              | Different sources            |
| Spec → Plan → Implementation  | ❌ No                               | Sequential dependencies      |
| 10 microservices analysis     | ✅ Yes (5+5 batches)                | Independent services         |
| Same file modifications       | ❌ No                               | State conflicts              |
| 3 SPEC reviews                | ✅ Yes (3 plannings)           | Independent documents        |
| Refactor tightly coupled code | ❌ No                               | Coordination required        |
| Update 8 .claude/ agents      | ❌ No                               | .claude/ constraint          |

## Validation Checklist

**Before Launching Parallel Agents**:

- [ ] Tasks are truly independent (no sequential dependencies)
- [ ] No shared state modifications (different files/components)
- [ ] Not modifying .claude/ directory (requires sequential)
- [ ] Task size justifies agent overhead (>30 seconds per agent)
- [ ] Clear synthesis strategy for combining results
- [ ] Batch size ≤ 5 agents simultaneously

**During Execution**:

- [ ] Single message with multiple Task calls
- [ ] Each agent has independent task specification
- [ ] Failure handling for partial results
- [ ] Clear what to do when all agents complete

**After Completion**:

- [ ] Synthesize findings from all agents
- [ ] Identify conflicting recommendations (if any)
- [ ] Document rationale for final decisions

---

**Key Insight**: Parallel agent execution is expensive (20x tokens for 5 agents) but valuable (3-5x faster). Use for high-value tasks with truly independent work. When in doubt, start sequential and parallelize proven-independent operations.
