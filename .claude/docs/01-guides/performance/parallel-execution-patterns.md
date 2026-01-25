# Parallel Execution Patterns Guide

**Purpose**: Guidance for when and how to use parallel vs sequential execution in multi-agent orchestration

**Referenced by**: CLAUDE.md (orchestrator), researcher-lead, all agents (via template)

## Core Principle

**Parallel for Reads, Sequential for Writes**

The fundamental rule that drives 90% of parallel execution decisions.

## When to ALWAYS Parallelize

### Read Operations

- **Multiple file reads** - Different Read tool calls on different files
- **Search operations** - Multiple Grep/Glob patterns simultaneously
- **Analysis tasks** - Multiple agents reviewing different files
- **Research streams** - Independent information gathering
- **Validation tasks** - Independent checks without dependencies

**Pattern**:

```markdown
Single message with multiple Tool calls:

- Read(file1.py)
- Read(file2.py)
- Read(file3.py)

All execute simultaneously, collect results when complete
```

**Benefits**:

- 3-5x faster for multi-file analysis
- Better resource utilization
- No file conflicts (read-only)
- Scales to 10+ files without timeout

### Independent Agent Tasks

- **researcher-codebase** + **researcher-external** - Different sources
- **Multiple plan files** - Different planning agents
- **Component implementations** - Different development agents on different files
- **Parallel reviews** - code-quality on different modules

## When to NEVER Parallelize

### Write Operations

- **File modifications** - Write, Edit, MultiEdit tools
- **Same file edits** - Multiple agents modifying same file
- **.claude/ directory** - File locking issues prevent concurrent modifications
- **Git operations** - Commits, pushes must be sequential

**Why**: File system conflicts, data corruption, lost changes

### Dependency Chains

- **Sequential workflows** - Output of agent A feeds input of agent B
- **Shared context requirements** - Multiple agents need same information
- **Tight coupling** - One task depends on result of another

**Example**:

```markdown
❌ Parallel:

- Agent A: Analyze architecture
- Agent B: Implement based on architecture (needs A's output)

✅ Sequential:

1. Agent A completes architecture analysis
2. Agent B receives results and implements
```

### Coding Tasks

Most coding involves fewer parallelizable components than research:

- Code files have interdependencies
- Shared interfaces and contracts
- Integration requirements

**Exception**: Completely independent modules/services can be parallel

## Anthropic Research Patterns

### Optimal Use Cases

**Breadth-First Queries** - Multiple independent directions:

- ✅ "Identify board members of all S&P 500 tech companies" (100+ parallel subtasks)
- ✅ "Analyze authentication across 50 microservices" (50 parallel analyses)

**Information Exceeding Context** - Multiple 200k contexts:

- ✅ Large-scale codebase analysis (split across workers)
- ✅ Multi-source research (web + docs + code in parallel)

**Complex Tool Interfaces** - Different tool sets:

- ✅ Codebase tools (Grep/Read) + Web tools (WebSearch/WebFetch) in parallel

### Anti-Patterns

**Domains with Tight Dependencies**:

- ❌ Most implementation tasks (interfaces depend on contracts)
- ❌ Database migrations (order matters)
- ❌ Build pipelines (sequential stages)

**Resource Misallocation**:

- ❌ 50 agents for simple query (use scaling rules: 1/3-5/10+)
- ❌ Parallel when 1 agent sufficient
- ❌ Excessive updates between agents

**Shared Context Requirements**:

- ❌ All agents need same full codebase context
- ❌ State must be consistent across agents
- ❌ Real-time coordination needed

## Implementation Patterns

### Pattern 1: Parallel Tool Calls

**Use**: Independent read/search operations

```markdown
Single response with multiple tool calls:
<tool_calls>
<Read file="src/auth.py"/>
<Read file="src/user.py"/>
<Grep pattern="class.*Auth" path="src/"/>
</tool_calls>
```

### Pattern 2: Parallel Agent Deployment

**Use**: Independent research/analysis tasks

```markdown
Single message with multiple Task calls:
<tool_calls>
<Task agent="researcher-codebase" task="analyze auth"/>
<Task agent="researcher-external" task="research best practices"/>
<Task agent="researcher-codebase" task="analyze user management"/>
</tool_calls>
```

### Pattern 3: Sequential Phases with Parallel Steps

**Use**: Complex workflows with internal parallelization

```markdown
Phase 1: Research (parallel agents)
→ Wait for all
Phase 2: Synthesis (single lead agent)
→ Complete
Phase 3: Implementation (parallel workers if independent)
```

### Pattern 4: .claude/ Sequential Constraint

**Special Case**: `.claude/` directory requires sequential execution

```markdown
❌ Parallel:

- claude-code-ecosystem: Create agent-a.md
- claude-code-ecosystem: Create agent-b.md

✅ Sequential:

1. Create agent-a.md
2. Wait for completion
3. Create agent-b.md
```

**Reason**: File watcher/locking prevents concurrent `.claude/` modifications

## Performance Benefits

### Measured Improvements

- **90% time reduction** for complex multi-source research
- **3-5x faster** for multi-component analysis
- **No timeout concerns** when scaling to 10+ components
- **Better resource utilization** vs sequential bottlenecks

### Token Economics

- **Parallel agents**: Each gets independent 200k context
- **Token usage**: 15x more than chat (4x for single agent)
- **Value justification**: Use for high-value tasks only

**Performance Variance**: Token usage explains 80% of performance differences

## Decision Matrix

| Scenario                | Parallel? | Rationale                            |
| ----------------------- | --------- | ------------------------------------ |
| Read 5 files            | ✅ Yes    | Independent reads, no conflicts      |
| Modify 5 files          | ❌ No     | Write conflicts, sequential required |
| Research web + codebase | ✅ Yes    | Different sources, independent       |
| Implement feature A → B | ❌ No     | B depends on A's interface           |
| Analyze 10 services     | ✅ Yes    | Independent microservices            |
| Update .claude/ files   | ❌ No     | File locking constraint              |
| Review 3 PRs            | ✅ Yes    | Independent reviews                  |
| Build → Test → Deploy   | ❌ No     | Sequential pipeline stages           |

## Orchestrator Guidance

### For CLAUDE.md (Main Orchestrator)

**Research Delegation**:

- Simple research: Handle directly
- Complex research: Delegate to researcher-lead (coordinates parallel workers)

**General Orchestration**:

- **Always check**: Read or write operation?
- **Reads**: Parallelize when >1 independent operation
- **Writes**: Always sequential
- **Mixed**: Parallel reads, then sequential writes

### For Sub-Agents

**Workers (sonnet)**:

- Execute tools in parallel when independent (3+ tools)
- Return compressed results to lead
- No worker-to-worker coordination

**Orchestrators (sonnet)**:

- Deploy workers in parallel for independent subtasks
- Single message with multiple Task calls
- Wait for all before synthesis

## Validation Checklist

**Before Parallelizing**:

- [ ] Operations are truly independent
- [ ] No write operations involved
- [ ] Not modifying .claude/ directory
- [ ] No sequential dependencies
- [ ] Resource usage justified (high-value task)

**Parallel Execution**:

- [ ] Single message with multiple tool/Task calls
- [ ] Each operation has independent context
- [ ] Failure handling for partial results
- [ ] Clear what to do when all complete

---

**Key Insight**: Start with sequential, parallelize proven-independent operations. The performance gains (up to 90%) justify the complexity for high-value, truly independent tasks.
