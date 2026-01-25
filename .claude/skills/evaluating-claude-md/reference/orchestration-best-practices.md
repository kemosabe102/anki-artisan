# Claude Code Orchestration Best Practices

## 1. Purpose and Philosophy

Orchestration is the art of **directing work without doing it all yourself**. In a well-architected Claude Code environment, the Main Agent (guided by `CLAUDE.md`) acts as a **Coordinator** or **Dispatcher**, not a worker.

### The "Read-Only Coordinator" Pattern

The most robust pattern for complex projects restricts the Main Agent’s scope:

- **Role**: Project Manager / Dispatcher
- **Permissions**: Read-Only (functionally restricted via instructions)
- **Primary Tool**: Sub-agent invocation (`/agents run ...`)
- **Goal**: Understand the user's intent just enough to pick the right specialist.

This prevents "Context Pollution"—where the main context window gets clogged with implementation details, making the agent "forget" high-level instructions.

---

## 2. The "One-Read" Rule for Context Gathering

To ensure the Main Agent remains a lightweight coordinator, strictly limit its reading behavior.

### The Guideline

> "If you need to read files to understand the request, perform **one** multi-file read operation. If that is insufficient, delegate the investigation to a sub-agent."

### Why this matters
- **Speed**: Prevents the Main Agent from spending 5 minutes reading 50 files.
- **Focus**: Forces the agent to identify *where* the problem is, rather than *what* the solution is.
- **Handoff**: The Main Agent passes the *file paths* to the sub-agent, which then does the deep reading in its own fresh context.

---

## 3. Tool Use Guidelines for Orchestrators

Define clear "lanes" for tool usage in your `CLAUDE.md`.

### 🔴 Forbidden / Restricted Tools (Main Agent)
- **Edit/Write**: NEVER edit files directly.
- **Test Execution**: NEVER run full test suites.
- **Bash**: AVOID complex commands (simple `ls` or `grep` is okay for discovery).

### 🟢 Allowed Tools (Main Agent)
- **Glob/LS**: To find *where* files are.
- **Read**: Strictly limited (see "One-Read Rule").
- **Agent Dispatch**: The primary method of solving problems.

### The Decision Matrix

| Task Type | Main Agent Action | Sub-Agent to Invoke |
| :--- | :--- | :--- |
| "Fix this bug" | Read error log → Locate file → **DELEGATE** | `implementer` |
| "How does auth work?" | Find auth folder → **DELEGATE** | `researcher` |
| "Update documentation" | **DELEGATE** | `docs-writer` |
| "Where is the user controller?" | `glob` search → Report path | (None, task complete) |

---

## 4. Designing the Orchestrator `CLAUDE.md`

To enforce this behavior, your `CLAUDE.md` needs specific "Orchestration Rules".

### Example `CLAUDE.md` Orchestration Section

```markdown
# Orchestration Rules (CRITICAL)

## Role: Read-Only Coordinator
You are the Project Coordinator. Your job is to route tasks to specialists.
**YOU DO NOT WRITE CODE.** You only read enough to delegate.

## Tool Use Strategy
1. **Discovery**: Use `ls` or `glob` to locate relevant files.
2. **Context**: You may perform **ONE** read operation (reading 1-5 key files) to understand the request.
3. **Delegation**: If the task requires writing code, deep analysis, or running tests, YOU MUST use a sub-agent.

## Sub-Agent Directory
- **Use `implementer`**: For writing code, fixing bugs, running tests.
- **Use `architect`**: For planning large features or refactors.
- **Use `security`**: For auditing code or dependencies.

## Anti-Patterns (DO NOT DO)
- Do not try to "fix it quickly" yourself.
- Do not read >10 files to "get context".
- Do not run the test suite yourself.
```

---

## 5. Handoff Patterns

### 5.1 The "Context-Rich Handoff"
When delegating, the Main Agent should pass three things:
1. **The Goal**: What needs to be done.
2. **The Map**: Which files are likely involved (found via `glob`).
3. **The Constraints**: Any specific user requirements.

**Prompt Example:**
> "I found the user controller at `src/controllers/user.ts`. It seems to have a bug in the login method. I am delegating to the `implementer` agent to fix it."

### 5.2 The "Plan-First Handoff"
For ambiguous requests, the Main Agent acts as a planner:
1. User: "Build a blog system."
2. Main Agent: "I see no blog system exists. I will run `architect` to design it."
3. `architect` returns: "We need models X, Y, Z."
4. Main Agent: "Great. I will now run `implementer` to build model X."

---

## 6. Checklist for Orchestration Readiness

Use this to verify your setup is ready for the Read-Only pattern:

- [ ] **`CLAUDE.md` explicitly forbids writing** in the System Role section.
- [ ] **Sub-agents exist** for all core "write" tasks (coding, docs, config).
- [ ] **Discovery tools** (glob, ls, grep) are encouraged over Reading tools.
- [ ] **One-Read Rule** is explicitly defined in `CLAUDE.md`.
- [ ] **Handoff instructions** tell the agent to pass file paths, not full file contents.
- [ ] **User expectations** are set: "I am the coordinator" is the first line of the agent's identity.
