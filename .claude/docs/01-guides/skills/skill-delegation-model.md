# Skill Delegation Model

**Purpose**: Define how skills (slash commands) interact with agents and file operations.

---

## Core Principle

**Skills are orchestrators, not executors.** When a skill is invoked, it must delegate file operations via Task().

```
┌─────────────────────────────────────────────────────────────────┐
│  SKILL (Orchestrator)              AGENTS (via Task)            │
│  ────────────────────              ─────────────────            │
│  • Guide workflow                  • Edit/Write files           │
│  • Make decisions                  • Generate content           │
│  • Coordinate phases               • Create artifacts           │
│  • Synthesize outputs              • Run validations            │
└─────────────────────────────────────────────────────────────────┘
```

---

## File-Scoped Delegation

**Limit each Task() call to ONE file** for retryability and parallelization:

```python
# ❌ BAD: Too broad
Task(agent, "Write task.yaml, Dockerfile, solution.sh, and tests")

# ✅ GOOD: File-scoped, parallelizable
Task(agent, "Write task.yaml for [name]")   # ⚡ parallel
Task(agent, "Write Dockerfile for [name]")  # ⚡ parallel
Task(agent, "Write solution.sh for [name]") # 🔗 sequential (depends on above)
Task(agent, "Write tests for [name]")       # 🔗 sequential (depends on above)
```

**Benefits**:
- Retry individual files on failure
- Run independent files in parallel
- Clear agent responsibility
- Better error isolation

---

## What Skills DO Directly (No Task Required)

| Action | Allowed | Rationale |
|--------|---------|-----------|
| Read files for context | ✅ YES | Understanding before delegation |
| Run bash for validation | ✅ YES | Verification of outputs |
| Guide user decisions | ✅ YES | Orchestration responsibility |
| Synthesize agent outputs | ✅ YES | Coordination role |
| Track phase progress | ✅ YES | Workflow management |

---

## What Skills NEVER Do Directly

| Action | Delegate To |
|--------|-------------|
| Edit/Write files | Domain agent (development, workflow, etc.) |
| Generate content | Content-specific agent |
| Create artifacts | Domain agent |
| Run test suites | code-quality |

---

## One-Read Rule for Skills

Skills inherit the same constraints as the main orchestrator:

> **One-Read Rule**: You may perform ONE multi-file read (1-5 files max) for context.
> If insufficient, delegate investigation to `researcher-codebase`.

This prevents skills from consuming excessive context before delegation.

---

## Parallelization Strategy

| File Type | Parallel? | Rationale |
|-----------|-----------|-----------|
| Independent configs | ✅ YES | No dependencies |
| Source + tests | ❌ NO | Tests depend on source |
| Schema + migrations | ❌ NO | Migrations depend on schema |
| Docs for same feature | ✅ YES | Usually independent |

**Max parallel agents**: 5 (system limit)

---

**See also**: 
- `.claude/docs/01-guides/performance/tool-parallelization-patterns.md`
- `.claude/docs/03-workflows/orchestrator-workflow.md`
