# Slash Commands, Agents, and Skills Interaction Best Practices

The most important design rules for orchestrating slash commands, agents, and skills together are:

- **Clarity of responsibility** – Each layer (command, agent, skill) has a single, well-defined purpose
- **Explicit delegation** – When one component invokes another, the flow is transparent and imperative
- **Minimize indirection** – Avoid chains like "command → skill → skill → skill → execution"
- **Progressive loading** – Load context only when needed; let the filesystem be external memory

This document provides concrete patterns for designing slash commands that work well with agents and skills.

---

## 1. The Three-Layer Architecture: Command, Agent, Skill

### 1.1 Conceptual Model

The healthy architecture has three distinct layers, each with a clear role:

```
┌──────────────────────────────────────────────────────────┐
│ SLASH COMMAND (Entry Point)                              │
│ - User-facing interface                                  │
│ - Orchestrates workflow steps                            │
│ - Routes to agents and skills                            │
│ - Presents results to user                               │
└──────────────────────────────────────────────────────────┘
                           ↓
        ┌──────────────────┴──────────────────┐
        ↓                                      ↓
┌──────────────────────┐         ┌─────────────────────────┐
│ SUB-AGENTS (Workers) │         │ SKILLS (Reference Docs) │
│ - Specialized tasks  │         │ - Procedural knowledge  │
│ - Isolated context   │         │ - Reusable patterns     │
│ - Scoped tools       │         │ - Examples & templates  │
└──────────────────────┘         └─────────────────────────┘
```

### 1.2 Responsibility Mapping

| Layer | Responsibility | Invokes | Examples |
|-------|---|---|---|
| **Command** | Orchestration & routing | Agents (via Task()) | `/git`, `/analyze-code`, `/prepare-review` |
| **Agent** | Domain-specific execution | Skills (via Skill()) | `code-quality`, `security-review`, `implementer` |
| **Skill** | Reference & procedures | Nothing (agents read them) | `git-workflow`, `testing-patterns`, `security-guidelines` |

**Key principle**: Commands orchestrate. Agents execute. Skills inform.

---

## 2. When Commands Should Invoke Agents

### 2.1 Use Agents When

**Use `Task(agent-name)` from a slash command when:**

- The task requires **domain-specific expertise** beyond general reasoning
  - Example: `Task(security-review)` for code security analysis
- The work is **long-running** and you want **context isolation**
  - Example: `Task(researcher)` to explore a topic without polluting the main conversation
- The task has **narrow scope** and produces a **compressed output**
  - Example: `Task(linter-fixer)` returns structured fixes, not raw exploration
- You want **parallel execution** of independent tasks
  - Example: Simultaneously invoke `Task(code-quality)` and `Task(sast-scanner)`
- The agent has **specialized instructions** that differ from the main workflow
  - Example: `Task(implementer)` knows how to write code; `Task(test-fixer)` knows test patterns

**Example (good command):**

```markdown
# /git prepare

## Execution Path

1. Read git status/diff
2. Analyze file categories locally (command logic)
3. FOR EACH category:
   - Task(code-quality): Review code for issues
   - Task(sast-scanner): Check for security vulnerabilities
4. Aggregate results and present summary
```

### 2.2 Avoid Agents When

**Don't use Task() if:**

- The operation is **simple and deterministic**
  - Do: Parse user arguments directly in the command
  - Don't: Invoke a "parser-agent" for trivial parsing
- The task can be **completed with standard tools** (bash, file read/write)
  - Do: Use `Bash("git status")` directly in the command
  - Don't: Invoke `Task(git-analyzer)` to run `git status`
- You're **"delegating" to save tokens** rather than **isolating context**
  - Anti-pattern: Creating a sub-agent just to offload simple work
  - Better: Do the work in the command itself

### 2.3 Delegation Decision Tree

```
Should I invoke Task(agent)?

├─ Is the task NARROW and WELL-SCOPED?
│  ├─ YES → Consider Task()
│  └─ NO → Do it in the command
│
├─ Does it need SPECIALIZED EXPERTISE?
│  ├─ YES → Use Task()
│  └─ NO → Do it in the command
│
├─ Will it produce COMPRESSED OUTPUT?
│  ├─ YES → Use Task() (isolate context)
│  └─ NO → Do it in the command (no benefit)
│
├─ Can it run in PARALLEL with other tasks?
│  ├─ YES → Use Task() (parallelization benefit)
│  └─ NO → Do it in the command (sequential anyway)
│
└─ Use Task() only if ≥2 of above are YES
```

---

## 3. When Agents Should Use Skills

### 3.1 Skill Discovery and Usage

**Agents should use skills when:**

- The skill **explicitly teaches how to accomplish the task**
  - `Skill(testing-patterns)` when writing tests
  - `Skill(security-guidelines)` when reviewing code for vulnerabilities

- The skill is **referenced in the agent's system prompt**
  - The agent knows the skill exists and when to consult it

- The skill provides **procedural knowledge** that reduces errors
  - Checklists, step-by-step workflows, examples

**Agents should NOT use skills when:**

- They can accomplish the task **without additional instructions**
- The skill is **reference only** but the agent doesn't need it for the specific task
- Using the skill **increases rather than decreases** context size

### 3.2 Skill Loading Pattern (from Agent's Perspective)

Agents follow a natural progression:

1. **Metadata check** (metadata is always available)
   - Is this skill relevant to my task?
   - Does the description match what I need to do?

2. **If relevant, load SKILL.md** (decision made)
   - Read the overview and core instructions
   - Understand the workflow structure

3. **If needed, load referenced files** (progressive)
   - Read specific sections (checklists, examples, guardrails)
   - Only when those sections are relevant

4. **Execute based on skill guidance** (action taken)
   - Follow the procedures defined in SKILL.md
   - Return results to orchestrator

**Example:**

Agent (code-quality) receives task to review API code:
1. Metadata: "Does security-guidelines apply?" → YES
2. Load SKILL.md: Read overview of API security checks
3. Load reference/api-security.md: Read specific API vulnerability patterns
4. Execute: Run security checks based on patterns
5. Return: Structured security report

---

## 4. Command → Agent Delegation Protocol

### 4.1 Imperative Delegation (The Right Way)

Slash commands should **clearly state** when and how they invoke agents. Use imperative language and structured delegation contracts.

**Pattern: Explicit Task Invocation**

```markdown
# /analyze-code

## Execution

1. Parse user input for code location
2. Read the code file
3. **Execute in parallel:**
   
   Task(code-quality):
   """
   Review the following code for quality issues:
   [code content]
   
   Return: JSON with {status, issues[], confidence}
   """
   
   Task(sast-scanner):
   """
   Analyze the following code for security vulnerabilities:
   [code content]
   
   Return: JSON with {vulnerabilities[], severity_scores[]}
   """

4. Aggregate results from both agents
5. Present combined report to user
```

**Key elements:**
- `Task(agent-name)` is explicit and clear
- Prompt to the agent is specific and includes input data
- Expected output format is defined (JSON schema)
- Parallelization is obvious (`in parallel:`)
- Results aggregation step is clear

### 4.2 Anti-Pattern: Indirect Delegation (The Wrong Way)

**Avoid:**

```markdown
# /analyze-code [BAD EXAMPLE]

Invoke Skill(code-analysis) which will route to agents as needed.
```

**Problems:**
- Doesn't say which agents are invoked
- Doesn't explain HOW they're invoked
- Makes the orchestrator's flow opaque
- Skill is responsible for orchestration (wrong layer)

### 4.3 Multi-Agent Orchestration Pattern

When a command needs to orchestrate many agents, structure it with clear phases:

```markdown
# /prepare-pr

## Phase 1: Code Analysis (Parallel)

Execute all agents simultaneously:

- Task(code-quality): "Review code..."
- Task(sast-scanner): "Check security..."
- Task(test-coverage): "Verify tests..."

Results schema:
{
  "code_quality": {...},
  "security": {...},
  "testing": {...}
}

## Phase 2: Synthesis (Orchestrator)

Aggregate Phase 1 results:
- Count issues by severity
- Determine overall status (PASS, WARN, FAIL)
- Extract top recommendations

## Phase 3: Present (Orchestrator)

Output: Structured PR readiness report
```

---

## 5. Skill Design for Agent Usage

### 5.1 Skill Structure That Agents Love

**Design skills with agents as the primary consumer.** This changes how you structure documentation.

#### 5.1a Metadata Must Be Precise

```yaml
---
name: security-code-review
description: >
  Analyzes code for security vulnerabilities, injection attacks, authentication bypass, 
  and data exposure. Use when reviewing user-facing code, API endpoints, database code, 
  or authentication handlers for security issues.
---
```

**Why this matters to agents:**
- Clear trigger terms ("injection", "authentication", "vulnerability")
- Specific context ("user-facing code", "API endpoints")
- Agent can decide in 1 second if skill is relevant

#### 5.1b SKILL.md Should Be a Checklist, Not a Tutorial

Instead of explaining concepts, **give the agent a procedure to follow:**

```markdown
---
name: security-code-review
description: ...
---

# Security Code Review

## Quick Checklist

Run through these checks for all code:

- [ ] Input validation: All user inputs validated and sanitized
- [ ] Authentication: Proper auth checks before access
- [ ] Authorization: Role/permission checks enforced
- [ ] Secrets: No hardcoded credentials or API keys
- [ ] SQL injection: Parameterized queries used everywhere
- [ ] XSS: Output properly escaped for context
- [ ] CORS: Origin restrictions configured
- [ ] Rate limiting: API endpoints have rate limits

## Per-Category Deep Dives

- **API Endpoints** → [reference/api-security.md](reference/api-security.md)
- **Database Code** → [reference/database-security.md](reference/database-security.md)
- **Authentication** → [reference/auth-security.md](reference/auth-security.md)

## Examples

See [examples/](examples/) for real code patterns and vulnerabilities.
```

**Why:**
- Agents can run the checklist in parallel
- SKILL.md is lightweight (~100 lines)
- Detailed sections loaded only when needed
- Agent can reference specific sections: "Check database-security.md for SQL injection patterns"

### 5.2 Skills as Reference, Not Orchestrators

**Critical rule: Skills must NEVER orchestrate other components.**

```markdown
❌ ANTI-PATTERN (Skill orchestrating agents):

# SKILL.md (security-review)

## Execution

Task(secrets-scanner): "Find secrets..."
Task(dependency-checker): "Check dependencies..."
```

**Why this is wrong:**
- Skills are passive; agents are active
- Orchestration belongs in commands, not skills
- Creates indirection and hard-to-debug flows

**Correct pattern:**

```markdown
✅ CORRECT (Skill as reference, agent or command orchestrates):

# SKILL.md (security-review)

## Scanning Approach

When reviewing code for security, check:

1. **Secrets** – Hardcoded credentials, API keys
2. **Dependencies** – Vulnerable package versions
3. **Input** – Validation and sanitization
...

## When to Use Specialized Agents

- **Secrets scanning** → Delegate to `secrets-scanner` agent
- **Dependency analysis** → Delegate to `dependency-checker` agent
```

The skill **describes** what to check and **suggests** delegation; the agent or command **makes the decision**.

---

## 6. Progressive Disclosure in Commands

### 6.1 Layered Command Documentation

Commands should reveal complexity progressively, just like skills:

```markdown
# /git prepare

Quick summary, examples, and links.

## Examples

### Basic (common case)
\`\`\`
/git prepare
\`\`\`
Runs: CI validation → File grouping → Quality gates → Summary

### Fast (skip validation)
\`\`\`
/git prepare --skip-validation
\`\`\`
Runs: File grouping → Quality gates → Summary

### Advanced Reference
For full details on workflow phases, see `SKILL.md`.
For quality gate agent matrix, see `SKILL.md` > Agent Matrix section.
```

**Benefits:**
- Users see simplicity first
- Complex options are discoverable but not required
- Power users can dive deep without cluttering the main documentation

### 6.2 Conditional Command Sections

Commands may have different execution paths based on context:

```markdown
# /code-review

## When reviewing Python code

- Task(python-linter): Check style and imports
- Task(type-checker): Verify type hints
- Task(security-review): Check for vulnerabilities

## When reviewing API code

- Task(api-reviewer): Check endpoint structure
- Task(security-review): Check auth/authz
- Task(documentation): Check API documentation

## When reviewing CLI code

- Task(cli-reviewer): Check argument parsing
- Task(error-handling): Check error messages
```

This makes clear that the agent set **depends on context** (language, code type, etc.).

---

## 7. State Management Across Command-Agent-Skill Layers

### 7.1 State Ownership

**Be explicit about where state lives:**

| State | Owned By | Used By | Shared Via |
|-------|----------|---------|-----------|
| User input, flags | Command | Agents (passed in Task prompt) | Prompt text |
| Task results | Agent | Command (orchestrator) | Return JSON |
| Workflow progress | Command | Display/logging | Files or memory |
| Skill content | Skill (filesystem) | Agents (read on-demand) | Filesystem |

**Example:**

```markdown
# /git prepare --strict --ci-tier=lint-only

## Command receives:
- flags: ["--strict", "--ci-tier=lint-only"]

## Command passes to agents:
Task(development, """
Run CI validation with tier: lint-only
...""")

## Command receives from agents:
{
  "ci_status": "PASS" | "FAIL",
  "errors": [...]
}

## Command maintains:
- workflow_state.validation_completed = true
- workflow_state.ci_tier = "lint-only"
- workflow_state.threshold_mode = "strict"
```

### 7.2 State File Pattern

For stateful commands (like `/git prepare` followed by `/git commit`), use a session state file:

```text
.claude/
├── commands/
│   └── git.md
└── state/
    └── git-workflow-state.json  # Stores prepare phase results
```

File contents:

```json
{
  "prepared_at": "2025-12-14T10:30:00Z",
  "groups": [
    {
      "group_id": 1,
      "files": ["src/api.py", "tests/test_api.py"],
      "status": "READY_TO_COMMIT",
      "quality_results": {...}
    }
  ],
  "workflow_status": {
    "validation_completed": true,
    "grouping_completed": true,
    "quality_gates_completed": true
  }
}
```

**Advantages:**
- State persists across command invocations (session-scoped)
- Easy to debug ("What did prepare actually produce?")
- Clear contract between phases

---

## 8. Common Patterns and Anti-Patterns

### 8.1 ✅ Best Practices

#### Pattern 1: Command as Orchestrator, Agents as Workers

```markdown
# /deploy-release

1. Parse version argument
2. Task(release-validator): "Check if release is ready..."
3. Task(deployment): "Deploy to production..."
4. Task(smoke-tests): "Run post-deploy verification..."
5. Aggregate results
6. Present deployment report
```

**Why:** Clear command flow, agents have scoped responsibilities.

#### Pattern 2: Skills as Shared Knowledge

```markdown
# Agent in security-review

When you need to check authentication patterns:
Load Skill(auth-security-guidelines) and review the authentication checklist.

When you need to check for injection attacks:
Load Skill(injection-prevention) and apply the patterns.
```

**Why:** Skills are consulted on-demand; agent decides relevance.

#### Pattern 3: Progressive Disclosure in Commands

```markdown
# /analyze-code

## Basic
\`\`\`
/analyze-code <file>
\`\`\`

## Full (with detailed options)
\`\`\`
/analyze-code <file> --deep --categories=security,performance
\`\`\`

See Advanced Usage section for:
- Custom agent routing
- Threshold configuration
- Report formatting
```

**Why:** Keeps common cases simple; advanced options available.

### 8.2 ❌ Anti-Patterns to Avoid

#### Anti-Pattern 1: Skill-to-Skill Orchestration

```markdown
# ❌ BAD: Skill calling skills

/command → Skill(workflow-orchestrator)
         → Skill(categorization)
         → Skill(validation)
         → Skill(reporting)
```

**Problem:** Indirection obscures execution flow. Skill is trying to be an orchestrator.

**Fix:** Commands orchestrate; skills inform agents.

---

#### Anti-Pattern 2: Hidden Agent Invocation

```markdown
# ❌ BAD: Agent invocation not visible

/command → Processes data
         → [Implicitly invokes agents somehow]
         → Returns results
```

**Problem:** User/reviewer can't see which agents were involved or how they were called.

**Fix:** Explicitly state all Task() calls and their expected outputs.

---

#### Anti-Pattern 3: Over-Invocation of Agents

```markdown
# ❌ BAD: Invoking agents for trivial tasks

Task(input-parser): "Parse the user's input..."
Task(file-reader): "Read this file..."
Task(json-formatter): "Format this JSON..."
```

**Problem:** Overhead exceeds benefit. These are deterministic tasks the command can handle.

**Fix:** Use agents for domain expertise or context isolation, not trivial operations.

---

#### Anti-Pattern 4: Vague Skill Descriptions

```yaml
# ❌ BAD: Too generic

name: helper
description: Helps with code tasks
```

**Problem:** Agent can't decide when to use the skill.

**Fix:** Be specific about what and when.

```yaml
# ✅ GOOD: Specific trigger and purpose

name: python-import-organizer
description: >
  Analyzes Python imports and reorganizes them according to PEP 8.
  Use when code has tangled imports, missing imports, or unused imports.
```

---

## 9. Reference Architecture: Command → Agent → Skill Flow

### 9.1 Full Example: /code-quality Command

```markdown
# /code-quality <file>

## Command Execution

1. Read the file
2. Detect language and category
3. Select agents based on language/category
4. Task(code-quality): "Review code..."
5. Aggregate results
6. Present report

---

## Agent: code-quality

When analyzing code:

1. Check if Skill(code-quality-guidelines) applies
2. Load SKILL.md if relevant
3. Review against checklist
4. For language-specific patterns:
   - Python code → Load reference/python-patterns.md
   - API code → Load reference/api-patterns.md
   - Database code → Load reference/database-patterns.md
5. Return structured report

---

## Skill: code-quality-guidelines

SKILL.md contains:
- Quick checklist (complexity, naming, tests)
- Links to reference/

reference/ contains:
- python-patterns.md (Python-specific)
- api-patterns.md (API endpoints)
- database-patterns.md (DB code)
- examples/ (real code samples)
```

**Flow visualization:**

```
User: /code-quality myfile.py
        ↓
    Command reads file
        ↓
    Detects Python + API code
        ↓
    Task(code-quality): "Review..."
        ↓
    Agent checks Skill(code-quality-guidelines)
        ↓
    Agent loads SKILL.md → reference/python-patterns.md
        ↓
    Agent loads reference/api-patterns.md (relevant)
        ↓
    Agent returns structured report
        ↓
    Command displays report to user
```

---

## 10. Design Checklist for Command-Agent-Skill Systems

When designing a new slash command that uses agents and skills:

### Command Design

- [ ] Purpose is clear: "This command does X" (single responsibility)
- [ ] Entry point is obvious: "User invokes with `/command-name args`"
- [ ] Execution flow is explicit: Steps are listed with no hidden agents
- [ ] Each Task() call is imperative: `Task(agent, "prompt with expected output schema")`
- [ ] Agent results are aggregated: Command shows "Here's what agents returned"
- [ ] Output schema is defined: "Results are formatted as: ..."

### Agent Design (if used)

- [ ] Single responsibility: One domain or expertise area
- [ ] Skill references are explicit: "When doing X, consult Skill(Y)"
- [ ] Tool scope is narrow: Only tools actually needed
- [ ] Output schema matches command expectations: Structured JSON/markdown
- [ ] Error handling is clear: "If I can't do this, return {error: ...}"

### Skill Design (if used)

- [ ] Metadata is precise: Trigger terms and context are clear
- [ ] SKILL.md is lean: ~100-200 lines, acts as overview
- [ ] References are one level deep: No A → B → C chains
- [ ] Content is procedural: Checklists, examples, not essays
- [ ] Progressive disclosure: Complex sections are in separate files

### Integration

- [ ] No skill-to-skill calls: Only agents read skills
- [ ] No hidden agent invocation: All Task() calls are visible
- [ ] State is explicit: Where does state live? How is it shared?
- [ ] Error paths are clear: What happens if an agent fails?
- [ ] Parallelization is obvious: Which agents run together? Which sequentially?

---

## 11. Common Questions and Answers

### Q: Should my command call an agent or a skill?

**A:** Depends on whether you need **execution** or **reference**.

- **Call an agent** (`Task()`) if you need the agent to actually DO something and produce output
- **Call a skill** (`Skill()` from within an agent) if you need guidance/procedures/examples

Commands invoke agents. Agents consult skills.

### Q: How many agents should I invoke from one command?

**A:** There's no hard limit, but start with **one agent per domain**. 

- 1 agent: Very focused command
- 2-4 agents: Common for multi-phase workflows (validate, review, execute, report)
- 5+ agents: Might indicate the workflow is too complex for a single command

**Rule of thumb:** If you need >5 agents, consider breaking the command into phases (e.g., `/prepare` then `/commit` instead of `/prepare-and-commit`).

### Q: Can a command invoke the same agent multiple times?

**A:** Yes, and it's often the right choice.

```markdown
# /format-and-test

1. Task(code-formatter): "Format the code..."
2. Task(test-runner): "Run tests..."
3. Task(code-formatter): "Format test files..." (same agent, different input)
4. Aggregate results
```

This is fine because the agent has a clear, reusable responsibility.

### Q: Should I create one big skill or multiple small skills?

**A:** Prefer **multiple small, focused skills** over one large skill.

- ✅ `security-review-api`, `security-review-database`, `security-review-general`
- ❌ `security-review-everything` (too broad, agents don't know which parts are relevant)

Each skill should answer: "When would you use this?"

### Q: How do I test a command-agent-skill system?

**A:** Test at each layer:

1. **Command**: Test argument parsing and orchestration
   - "When I run `/git prepare --strict`, does it pass `--strict` correctly to agents?"
2. **Agent**: Test with real tasks
   - "When security-review agent reviews this code, does it catch the vulnerability?"
3. **Skill**: Test that agents can find and use it
   - "When an agent needs API security guidance, can it load api-patterns.md?"

---

## 12. Evolution and Iteration

### 12.1 When to Refactor Command → Agent → Skill

**Refactor a command into an agent when:**
- The command has grown to >500 lines
- Multiple sub-commands have different flows
- You need to run the same logic in parallel with other agents

**Refactor an agent's guidance into a skill when:**
- Multiple agents need the same procedures/guidelines
- The agent frequently reads the same reference documentation
- The guidelines are domain-specific and stable

### 12.2 Version Control

Track changes to your command-agent-skill system in version control:

```bash
git add .claude/commands/git.md
git add .claude/agents/code-quality.md
git add .claude/skills/code-quality-guidelines/SKILL.md
git commit -m "refactor: consolidate git workflow command"
```

Each file is a versioned artifact, just like code.

### 12.3 Documentation and Runbooks

Maintain a README that explains the system:

```markdown
# Claude Code Orchestration

## Commands

- `/git prepare` – Analyze and group staged changes
- `/git commit <groups>` – Commit selected groups
- `/code-review <file>` – Comprehensive code review

## Agents

- `code-quality` – General code quality review
- `security-review` – Security-focused code analysis
- `test-coverage` – Test coverage verification

## Skills

- `code-quality-guidelines` – Code quality procedures
- `security-review-patterns` – Security review checklists
- `testing-best-practices` – Testing guidelines
```

This makes the system navigable for others on your team.

---

## Summary

**Key Principles:**

1. **Commands orchestrate** – They decide what gets done and in what order
2. **Agents execute** – They do the actual work with domain expertise
3. **Skills inform** – They provide procedures, examples, and guidelines
4. **Minimize indirection** – Avoid command → skill → skill → execution chains
5. **Be explicit** – All Task() calls are visible; no hidden invocations
6. **Isolate context** – Each agent has its own context window; use for high-compression work
7. **Load progressively** – Only load what's needed; use filesystem as external memory

**Design for clarity, not cleverness. If someone reading your command file can't immediately understand the execution flow, refactor.**
