# Claude Code Sub-Agents Best Practices

## 1. Purpose and Philosophy

Claude Code sub-agents are **specialized, autonomous AI assistants** that the main Claude Code agent can delegate specific tasks to. Each sub-agent operates with:

- Its own **isolated context window** (preventing context pollution in the main conversation)
- A **custom system prompt** guiding specialized behavior
- **Scoped tool permissions** (what it can and cannot access)
- **Single, clear responsibility** (one domain or task type)

Sub-agents enable:

- **Context preservation** – Main agent stays focused while sub-agents handle complex research or tasks
- **Parallelization** – Multiple sub-agents work simultaneously on independent tasks
- **Specialized expertise** – Fine-tuned prompts for specific domains (security review, architecture, testing, etc.)
- **Reusability** – Once created, shared across projects and team members

---

## 2. File Size and Content Scope

### Keep sub-agent definitions lean and focused

- Each sub-agent file should be a **single, well-defined agent**, not a multi-mode tool.
- Sub-agent definitions (YAML frontmatter + markdown) typically range from **100–300 lines**.
- Avoid embedding entire codebases or massive reference docs in the agent file; instead, **reference key files or directories** that the agent should consult when needed.

### Practical guidelines

- **System prompt** should fit on 1–2 screens for easy review and iteration.
- **Tool list** should be explicit and minimal—only include tools the agent actually needs.
- **Description** should be action-oriented, clear about when to invoke this agent, and what outcome it produces.
- If a sub-agent definition grows beyond ~250 lines, reconsider whether its scope is too broad.

This keeps sub-agents maintainable and prevents them from becoming a dumping ground for vague responsibilities.

---

## 3. File Structure and Organization

### Directory-based agent namespacing
s
Store all sub-agent definitions in a dedicated directory, organized by role, phase, or domain:

```text
.claude/agents/
├── pm-spec.md           # Product spec & requirement gathering
├── architect-review.md  # Architecture & design validation
├── implementer.md       # Code implementation & testing
├── security-review.md   # Security & vulnerability analysis
├── code-reviewer.md     # Code quality & standards
└── docs-writer.md       # Documentation generation
```

Claude automatically discovers and invokes sub-agents from `.claude/agents/` (project scope) or `~/.claude/agents/` (user scope).

### Sub-agent file structure (Markdown with YAML frontmatter)

```markdown
---
name: architect-review
description: >
  Validates architectural designs against platform constraints.
  Use after a spec exists; produces an ADR and guardrails.
  Checks for performance, cost limits, and scalability.
model: claude-3-5-sonnet-20241022
tools:
  - read
  - glob
  - grep
  - bash
---

# Architect Review Agent

## Purpose

You are the architecture specialist. Your job is to:
1. Review the proposed design against known constraints
2. Identify potential performance, cost, or scalability issues
3. Produce an ADR (Architecture Decision Record) with guardrails
4. Ask clarifying questions if the design is ambiguous

## Key Responsibilities

- **Validate design**: Does it fit the platform constraints?
- **Assess impact**: Performance, cost, security, maintainability?
- **Produce ADR**: Document decisions and rationale
- **Set guardrails**: What must NOT be violated in implementation?

## Input Expected

You receive:
- A product specification or feature request
- Any existing architecture context
- Links to relevant codebase sections

## Output Definition of Done

Your response includes:
- [ ] Architecture Decision Record (ADR) file path or content
- [ ] List of guardrails (constraints the implementation must respect)
- [ ] Identified risks and mitigations
- [ ] Any clarifying questions (if design is incomplete)

## Ask-First Rules

**Stop and ask if:**
- The design implies a breaking change to public APIs
- Performance requirements are unclear
- The scalability limits are not defined
- Security or compliance implications are ambiguous

Do NOT proceed without clarification.

## References

See project root `CLAUDE.md` for platform constraints, performance budgets, and cost targets.
```

### Key components

1. **YAML Frontmatter**:
   - `name`: Unique identifier (used in invocation)
   - `description`: When to use this agent, what it produces (action-oriented)
   - `model`: Which Claude model to use (typically Sonnet for balance)
   - `tools`: Explicit list of allowed tools (read, write, bash, etc.)

2. **Markdown Content**:
   - Purpose and role
   - Key responsibilities
   - Input expectations
   - Output definition of done (checklist)
   - Ask-first rules (when to stop and ask before proceeding)
   - References to shared docs

---

## 4. Progressive Disclosure for Sub-Agents

Progressive disclosure for sub-agents means **structuring workflows so complexity and context appear only when needed**. Design disclosure in three layers:

### 4.1 Step-by-step workflow disclosure (procedural)

Break multi-step workflows into sequential sub-agent invocations, each handling one phase:

**Common pipeline:**
1. **PM Spec** → Gathers requirements, writes spec, asks clarifying questions, sets status `READY_FOR_ARCH`
2. **Architect Review** → Validates design, produces ADR, sets status `READY_FOR_IMPL`
3. **Implementer** → Writes code, runs tests, produces summary, sets status `READY_FOR_REVIEW`
4. **Code Reviewer** → Security & quality review, provides feedback, sets status `APPROVED` or `NEEDS_REVISION`

Each sub-agent receives:
- The **current state** (what's been done so far)
- The **next objective** (what THIS phase should produce)
- A **handoff rule** (what triggers the next phase)

**Result**: Complex workflows become a series of focused, isolated tasks rather than one massive operation.

### 4.2 Conditional disclosure (specialized sub-agents for specific scenarios)

Create specialized sub-agents only for specific, well-defined scenarios. Don't create an agent for every possible task.

**Example triggers for conditional sub-agent invocation:**

- "This code has security implications; use the security-review subagent to analyze it."
- "Before implementing, use the architect-review subagent to validate this approach."
- "After implementing, use a test-verification subagent to check coverage and quality."

Conditional invocation means:
- The main agent decides **if and when** to delegate, not the user.
- The main agent keeps higher-level decision-making.
- Sub-agents remain focused, lightweight, and easy to reason about.

### 4.3 Contextual disclosure (shared docs & guardrails)

Reference deeper documentation only in the sub-agent's prompt when it needs to consult it:

```markdown
## References

When making design decisions, consult:
- Root `CLAUDE.md`: Platform constraints, performance budgets, cost targets
- `docs/architecture/patterns.md`: Approved architectural patterns
- `docs/security/guidelines.md`: Security requirements and checklist
```

This prevents bloating the sub-agent definition with massive inline docs. Instead, the agent is **empowered to read** these files as needed.

---

## 5. Single-Responsibility Design

### The core principle

**Give each sub-agent ONE clear goal, ONE clear input, and ONE clear output.**

#### Bad:

```markdown
---
name: general-helper
description: Does code stuff, reviews things, maybe writes docs
---
```

Too vague. Claude won't know when to use it or what to expect.

#### Good:

```markdown
---
name: security-review
description: >
  Performs a security-focused code review.
  Use after implementation; identifies vulnerabilities and compliance gaps.
  Produces a security report and list of required fixes.
---
```

Crystal clear: when to use, what it does, what you get.

### Single responsibility in practice

- **One goal per agent** – "validate architecture", "perform security review", "write unit tests"
- **One input type** – What kind of artifact does it expect? (code, spec, design doc)
- **One output type** – What does it produce? (ADR, test file, security report)
- **Narrow tool scope** – Only include tools it actually needs

Example scoping:

```yaml
# PM Spec Agent
tools:
  - read         # Read existing specs
  - write        # Write the new spec
  - grep         # Search for related requirements

# Implementer Agent
tools:
  - read
  - write
  - bash         # Run tests and linting
  - grep

# Security Review Agent
tools:
  - read         # Review code only
  # No write, bash, or dangerous tools
```

---

## 6. Designing Handoffs and State Management

### Explicit handoff rules

Workflows break down when handoff rules are vague. Make them explicit:

```markdown
## Definition of Done (DoD)

Before handing off to the next stage:
- [ ] Spec includes all acceptance criteria
- [ ] At least 3 clarifying questions answered
- [ ] Estimate (T-shirt size) provided
- [ ] Status file updated to READY_FOR_ARCH

Next agent: Use `architect-review` subagent on `features/use-case-presets`
```

### Status tracking file

Maintain a `WORKFLOW_STATUS.md` or similar at the repo root:

```markdown
# Feature: Use-Case Presets

## Timeline

| Phase | Owner | Status | Date | Notes |
|-------|-------|--------|------|-------|
| Spec | @pm-spec | ✅ READY_FOR_ARCH | 2025-12-05 | Added 3 clarifying answers |
| Architecture | @architect | ⏳ IN_PROGRESS | 2025-12-05 | Reviewing design patterns |
| Implementation | @implementer | ⏹️ BLOCKED | — | Waiting on architecture |
| Security Review | @security-review | ⏹️ BLOCKED | — | Waiting on implementation |
| Code Review | @code-reviewer | ⏹️ BLOCKED | — | Waiting on implementation |

## Key Decisions

- Using event-driven pattern for real-time updates
- Database: PostgreSQL (constraint per performance budget)
- API: REST; GraphQL deferred to phase 2

## Open Questions

1. Should presets be user-scoped or team-scoped?
   - **Answer**: Team-scoped, with future user override option
```

### Human approval gates

Don't chain all sub-agents automatically. Use **explicit, visible handoffs**:

**Pattern:**
```
Sub-agent output includes: "Next: Use the implementer subagent on feature/xyz"
Main agent displays this.
Human scans the handoff suggestion and approves.
User runs the next sub-agent explicitly.
```

This prevents:
- Runaway agent chains
- Loss of human oversight
- Accumulating errors across stages
- Wasted sub-agent invocations

---

## 7. Sub-Agent Configuration Best Practices

### Clear, action-oriented descriptions

```yaml
# ❌ Vague
description: Helps with code

# ✅ Clear
description: >
  Performs test-driven development verification.
  Use after unit tests are written; verifies tests are not overfitted to the implementation.
  Suggests additional test cases and edge cases to cover.
```

### Explicit tool lists

```yaml
# ❌ Over-broad
tools: ALL

# ✅ Explicit (security review agent)
tools:
  - read         # Read code to analyze
  # NO write, bash, or other mutation tools
```

### Model selection

```yaml
# For fast, simple tasks
model: claude-3-5-haiku-20241022

# For complex reasoning (architecture, security)
model: claude-3-5-sonnet-20241022

# For deep analysis (rarely needed)
model: claude-3-opus-20250805
```

---

## 8. Iterative Refinement of Sub-Agents

When a sub-agent performs poorly:

1. **Document the failure** – What did it do vs. what should it have done?
2. **Provide context** – Share the failed output and expected result
3. **Ask Claude to refine the prompt** – Pass the sub-agent `.md` file to Claude and ask for suggestions
4. **Update and version control** – Commit the refined definition

Example refinement loop:

```markdown
# Feedback on architect-review subagent

The agent neglected to check our performance budget constraint.
It should have reviewed `CLAUDE.md` first for cost limits.

Can you suggest updates to the architect-review.md system prompt
to ensure it always checks performance budgets before finalizing the ADR?
```

Claude will analyze the `.md` file and suggest precise changes to the prompt.

---

## 9. CLAUDE.md Integration with Sub-Agents

Sub-agents inherit the root **CLAUDE.md** context (project constraints, architecture, coding standards). Use hierarchical CLAUDE.md files:

```text
.claude/
├── CLAUDE.md              # Project-level context (all agents read this)
├── CLAUDE-backend.md      # Backend-specific overrides
├── CLAUDE-frontend.md     # Frontend-specific overrides
└── agents/
    ├── architect.md
    ├── security-review.md
    └── implementer.md
```

**How it works:**
- All agents read the root `CLAUDE.md`
- More specific files override general ones
- Keeps root context lean; domain-specific details live in specialized files

---

## 10. Example: Complete Sub-Agent Suite for a Typical Workflow

```text
.claude/
├── CLAUDE.md              # Project context
├── agents/
│   ├── pm-spec.md
│   ├── architect-review.md
│   ├── implementer.md
│   ├── security-review.md
│   ├── code-reviewer.md
│   └── docs-writer.md
└── shared-docs/
    ├── performance-budget.md
    ├── security-checklist.md
    ├── code-standards.md
    └── architecture-patterns.md

WORKFLOW_STATUS.md        # Track feature progress across phases
```

### Typical invocation sequence

```
User: Help me implement the new notification system

Main Claude Code agent:
1. Asks for high-level requirements
2. Invokes /agents pm-spec for detailed spec
   ↓ [Agent produces spec + clarifying questions]
3. Waits for user approval
4. Invokes /agents architect-review
   ↓ [Agent produces ADR + guardrails]
5. Waits for user approval
6. Invokes /agents implementer
   ↓ [Agent writes code + tests]
7. Invokes /agents security-review (in parallel or sequentially)
   ↓ [Agent produces security report]
8. Waits for user approval
9. Invokes /agents code-reviewer
   ↓ [Agent produces review feedback]
10. Main agent creates PR with summary
```

---

## 11. Common Patterns and Pitfalls

### ✅ Best Practices

- **Start with Claude-generated agents** – Use `/agents` command; Claude scaffolds a solid foundation
- **Single responsibility** – One goal, one input, one output per agent
- **Explicit handoffs** – Use checklists and status files, not vague prose
- **Narrow tool scope** – Only allow tools the agent needs
- **Version control agents** – Track `.md` file changes like code
- **Human approval gates** – Don't auto-chain; make handoffs visible
- **Pause, resume, branch** – Add status flags like `ON_HOLD`, `BLOCKED`, or `-a`/`-b` splits
- **Ask-first rules** – Bake "ask before proceeding" into prompts for risky decisions

### ❌ Pitfalls

- **Too broad a scope** – "Do everything related to features" – breaks predictability
- **Hidden handoffs** – Auto-chaining agents without user visibility
- **Over-documentation** – Embedding 500 lines of reference docs in the agent definition
- **Tool sprawl** – Giving agents access to tools they don't need
- **No approval gates** – Letting agents make irreversible decisions without human oversight
- **Vague descriptions** – "Helps with stuff" – Claude can't decide when to invoke
- **Combining roles** – One agent trying to be PM + Architect + Implementer

---

## 12. Parallel vs. Sequential Execution

### When to parallelize

Use parallel sub-agent invocation for **independent tasks**:

```
Security Review (analyzes code) ──┐
                                  ├─→ Merge results
Code Quality Review (checks style)┘
```

The main agent can invoke both simultaneously:

```
Task("Security review of payment.ts", [...])
Task("Code quality review of payment.ts", [...])
# Wait for both to complete
```

### When to sequence

Use sequential invocation for **dependent tasks**:

```
PM Spec → [requires spec]
         ↓
       Architect → [requires architecture]
                 ↓
               Implementer → [requires guardrails]
                           ↓
                    Security Review
```

---

## 13. Tips for Production Use

### Bake decisions into prompts

```markdown
## Guardrails (Do NOT violate)

1. All database changes must include a migration
2. Any public API change requires a breaking-version bump
3. Performance must stay within 100ms SLA
```

### Test agents with dry runs

Before deploying a new sub-agent definition:
1. Invoke it on a sample task
2. Review the output carefully
3. Iterate on the prompt if needed
4. Commit only after validation

### Monitor agent quality

Track:
- How often agents ask clarifying questions (should be common)
- How often their output requires rework (should be rare)
- Which agents get invoked most (indicates core workflow)
- Which agents underutilized (may be poorly scoped)

### Document your agent suite

Maintain a **AGENTS.md** at the repo root:

```markdown
# Sub-Agents Directory

## pm-spec
Gathers requirements and writes product specifications.
**Use when**: Starting a new feature or enhancement
**Output**: Spec document + clarifying questions
**Time**: 5–15 min

## architect-review
Validates architectural designs against constraints.
**Use when**: Design phase is complete
**Output**: ADR + guardrails
**Time**: 10–20 min

## implementer
Writes code and tests based on ADR.
**Use when**: Architecture is approved
**Output**: Code + passing tests + summary
**Time**: 30–60 min
```

This makes it easy for team members to understand the agent ecosystem at a glance.

---

## Conclusion

Claude Code sub-agents are most powerful when:

1. **Each has a single, clear responsibility**
2. **Handoffs are explicit and tracked**
3. **Tool scope is narrow and intentional**
4. **Workflows are sequential with human approval gates**
5. **Agent definitions are treated like code** (versioned, refined, tested)
6. **Context is shared through CLAUDE.md**, not embedded in each agent

By following these principles, you can build reliable, maintainable, parallelizable workflows that blend AI autonomy with human oversight.