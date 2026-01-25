# Tool Parallelization Patterns

**Purpose**: Universal guidance for efficient tool usage - when to execute tools in parallel vs sequential

**Audience**: Read-only research agents (researcher-codebase, researcher-external), orchestrator for direct tool usage

**Scope**: Tool-level execution patterns only. For agent delegation strategy, see `agent-parallelization-strategy.md`

## Core Principle

**Parallel for Reads, Sequential for Writes**

The fundamental rule that drives 90% of tool parallelization decisions.

## When to ALWAYS Parallelize

### Multiple Independent Reads

- **Different files**: `Read(file1.py)` + `Read(file2.py)` + `Read(file3.py)`
- **Search operations**: `Grep(pattern1)` + `Grep(pattern2)` + `Glob("**/*.py")`
- **Independent research**: `WebFetch(url1)` + `WebFetch(url2)` + `WebSearch(query)`
- **Validation checks**: Multiple Grep operations with different patterns

**Pattern**:

```markdown
Single message with multiple tool calls:
<tool_calls>
<Read file_path="src/auth.py"/>
<Read file_path="src/user.py"/>
<Grep pattern="class.*Auth" path="src/"/>
</tool_calls>

All execute simultaneously, results collected when complete
```

**Benefits**:

- **3-5x faster** for multi-file analysis
- **Better resource utilization** vs sequential bottlenecks
- **No file conflicts** (read-only operations)
- **Scales well** to 10+ tool calls without timeout

### Discovery Phase Pattern (Research Agents)

**Common Research Pattern**:

```markdown
Round 1 - Discovery (parallel):

- Glob("\*_/_.py") # Get project structure
- Grep(pattern, head_limit=20) # Find initial matches
- Grep(pattern, output_mode="count") # Count occurrences

Round 2 - Mapping (parallel):

- Read(top_file_1.py) # Read top matches
- Read(top_file_2.py)
- Read(top_file_3.py)

Round 3 - Validation (parallel):

- Grep(pattern, glob="\*_/test_.py") # Find tests
- Grep(pattern, output_mode="content", -A=2, -B=2) # Usage examples
```

## When to NEVER Parallelize

### Write Operations

- **File modifications**: Write, Edit, MultiEdit tools
- **Git operations**: Any git commands (commits, pushes, etc.)
- **.claude/ directory modifications**: File locking prevents concurrent writes

**Why**: File system conflicts, data corruption, lost changes

**Example**:

```markdown
❌ Parallel:

- Edit(file.py, old="foo", new="bar")
- Edit(file.py, old="baz", new="qux")

✅ Sequential:

1. Edit(file.py, old="foo", new="bar")
2. Wait for completion
3. Edit(file.py, old="baz", new="qux")
```

### Dependent Operations

- **Sequential workflows**: Output of tool A feeds input of tool B
- **Conditional execution**: If tool A succeeds, then tool B
- **Shared state requirements**: Multiple tools need consistent state

**Example**:

```markdown
❌ Parallel:

- Grep("class UserModel") # Find definition
- Read(result_file) # Read file found by Grep

✅ Sequential:

1. Grep("class UserModel") → identifies src/user.py
2. Read(src/user.py) → reads the identified file
```

## File System Constraints

### .claude/ Directory - Sequential Only

**Rule**: All `.claude/` directory operations MUST be sequential

```markdown
❌ Parallel:

- Write(.claude/agents/agent-a.md)
- Write(.claude/agents/agent-b.md)

✅ Sequential:

1. Write(.claude/agents/agent-a.md)
2. Wait for completion
3. Write(.claude/agents/agent-b.md)
```

**Reason**: File watcher and mandatory file locking prevent concurrent modifications

### Write Operations on Different Files

**Rule**: Even different files should be written sequentially to prevent conflicts

```markdown
❌ Parallel:

- Write(src/file1.py, content=...)
- Write(src/file2.py, content=...)

✅ Sequential:

1. Write(src/file1.py, content=...)
2. Write(src/file2.py, content=...)
```

**Reason**: File system locks, git tracking, and import dependencies

## Decision Matrix

| Tool Operation | Multiple Targets     | Parallel? | Rationale                                |
| -------------- | -------------------- | --------- | ---------------------------------------- |
| Read           | 5 different files    | ✅ Yes    | Independent reads, no conflicts          |
| Grep           | 3 different patterns | ✅ Yes    | Independent searches                     |
| Glob           | Multiple patterns    | ✅ Yes    | Independent file discovery               |
| WebFetch       | Different URLs       | ✅ Yes    | Independent external requests            |
| WebSearch      | Different queries    | ✅ Yes    | Independent searches                     |
| Write          | Any files            | ❌ No     | Write conflicts, sequential required     |
| Edit           | Same file            | ❌ No     | Data corruption risk                     |
| Edit           | Different files      | ❌ No     | Import dependencies, git tracking        |
| Bash           | Any commands         | ❌ No     | State dependencies, sequential execution |

## Practical Examples

### ✅ Good: Parallel Discovery

```markdown
Research Agent Task: "Analyze authentication patterns"

Parallel tool execution:

1. Glob("\*_/auth_.py")
2. Grep("class.\*Auth", output_mode="count")
3. Grep("@requires_auth", output_mode="files_with_matches")
4. Grep("def login", output_mode="content", -n=true)

Result: 4 tools execute simultaneously, ~4x faster
```

### ✅ Good: Parallel Multi-File Analysis

```markdown
Code Review Task: "Review authentication modules"

Parallel tool execution:

1. Read(src/auth/login.py)
2. Read(src/auth/session.py)
3. Read(src/auth/tokens.py)
4. Read(tests/test_auth.py)

Result: All files loaded simultaneously
```

### ❌ Bad: Parallel Writes

```markdown
Implementation Task: "Create authentication system"

❌ Parallel (WRONG):

1. Write(src/auth.py, content=auth_code)
2. Write(tests/test_auth.py, content=test_code)

✅ Sequential (CORRECT):

1. Write(src/auth.py, content=auth_code)
2. Wait for completion
3. Write(tests/test_auth.py, content=test_code)
```

### ❌ Bad: Dependent Tool Sequence

```markdown
Research Task: "Find and analyze UserModel"

❌ Parallel (WRONG):

1. Grep("class UserModel") # Returns: src/models/user.py:45
2. Read(src/models/user.py) # Needs result from step 1

✅ Sequential (CORRECT):

1. Grep("class UserModel") → Result: src/models/user.py:45
2. Read(src/models/user.py) → Analyze the class
```

## Performance Considerations

### When Parallelization Pays Off

- **3+ independent read operations**: 3-5x speedup
- **10+ file analysis**: Scales linearly, no timeout concerns
- **Multi-source research**: Web + codebase in parallel

### When Sequential is Fine

- **1-2 operations**: Overhead not worth complexity
- **Tight dependencies**: Sequential is clearer and safer
- **Write operations**: Always sequential for safety

### Token Cost Awareness

- Each tool call consumes tokens (input + output)
- Parallel execution doesn't change token cost
- Benefit is **time savings**, not token savings

## Validation Checklist

**Before Parallelizing Tools**:

- [ ] Operations are truly independent (no data dependencies)
- [ ] All operations are read-only (no Write/Edit/MultiEdit)
- [ ] Not modifying .claude/ directory (requires sequential)
- [ ] No sequential logic dependencies (if-then chains)
- [ ] Results can be collected independently

**Parallel Execution**:

- [ ] Single message with multiple tool calls
- [ ] Each tool call has independent parameters
- [ ] Clear what to do when all tools complete
- [ ] Failure handling for partial results

---

**Key Insight**: The "parallel for reads, sequential for writes" principle handles 90% of decisions. When in doubt, start sequential and parallelize when proven independent.

---

## Batch Delegation for Multi-File Workflows

**When to Use**: Tasks requiring >5 file changes across agent delegations

**Core Principle**: Prevent single-agent bottlenecks by splitting work across multiple parallel agents (max 3-5 files per agent).

### Scaling Rules

| File Count | Strategy | Agent Count | Files per Agent |
|------------|----------|-------------|-----------------|
| 1-3 files | Single agent | 1 | 1-3 |
| 4-5 files | Single agent (upper limit) | 1 | 4-5 |
| 6-10 files | Parallel batch | 2 | 5 each |
| 11-20 files | Parallel batch | 4 | 5 each |
| 21+ files | Parallel batch | 5+ | max 5 each |

### Examples

**Small Scale** (8 files):

- Batch 1-2: claude-code-ecosystem (4 files each)
- Launch: 2 parallel Task calls

**Medium Scale** (15 files):

- Batch 1-3: development (5 files each)
- Launch: 3 parallel Task calls

**Large Scale** (32 files):

- Batch 1-7: development (4-5 files each)
- Launch: 7 parallel Task calls

### Benefits

1. **Prevents Token Overflow**: Each agent handles 5K-15K tokens instead of 40K+ sequential
2. **Faster Execution**: 7 parallel agents complete in ~10 min vs 70 min sequential
3. **Failure Isolation**: One batch failure doesn't block other batches
4. **Better Resource Utilization**: Maximizes parallel execution capabilities

### When NOT to Batch

- **Sequential dependencies**: File B depends on File A changes
- **Cross-file refactoring**: Import paths, class references span batches
- **Schema migrations**: Database changes require specific order
- **Git operations**: Commits should be atomic, not batched

### Validation

After batch completion:

1. Verify all agents returned SUCCESS
2. Check for partial failures (some batches complete, some fail)
3. Validate cross-batch consistency (no conflicting changes)
4. Run integration tests across all modified files

---

**See Also**:

- `CLAUDE.md` lines 127-142 (batch delegation principle)
- `docs/01-planning/custom/agent-selection-consolidation-p2-summary.md` (32-agent batch validation results)
