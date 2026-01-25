# Slash Commands Best Practices

## 1. Purpose and Philosophy

Slash commands are **reusable, named prompts or actions** that users can invoke quickly using a leading `/` followed by a command name and optional arguments. They are ideal for:

- Frequently repeated tasks
- Opinionated workflows
- Team-wide conventions and utilities

Good slash command design aims for:

- **Speed** – minimize typing and cognitive load
- **Clarity** – clear names, arguments, and results
- **Safety** – predictable, reversible where possible

---

## 2. File Size and Content Scope

### Keep each command small and focused

- Treat each command file (Markdown, TOML, or code-backed definition) as a **single-purpose tool**.
- Prefer **multiple small commands** over one giant, multi-mode command.
- Avoid embedding large reference docs directly in a command file; instead, **link out** or reference secondary files.

### Practical guidelines

- Command description + body should typically fit on **one screenful** in your editor for easy scanning.
- If a command definition exceeds ~150–200 lines of text or logic, strongly consider **splitting it** into:
  - A core command
  - One or more subcommands or helper commands
  - External docs or scripts

This keeps commands easier to maintain, reason about, and reuse.

---

## 3. Command Organization & Documentation Coordination

### Directory-based namespacing

Organize commands in a dedicated directory, grouped by domain or feature area:

```text
commands/
├── project/
│   ├── init.md
│   ├── status.md
│   └── deploy.md
├── code/
│   ├── refactor-function.md
│   └── add-tests.md
└── docs/
    ├── summarize-file.md
    └── propose-edits.md
```

- Subdirectories become **namespaces** (e.g., `/project:init`, `/code:refactor-function`).
- Keep naming **consistent and action-oriented**: `deploy`, `fix-imports`, `generate-report`.

### Co-locating documentation

Use a layered documentation strategy:

- **Inline, minimal description** in the command file for quick discovery
- **Short usage notes** or examples near the top
- **Deep documentation** in separate, referenced files

Example layout:

```text
commands/
├── project/
│   ├── deploy.md            # Slash command definition & primary instructions
│   ├── deploy-checklist.md  # Detailed checklist (referenced from deploy.md)
│   └── deploy-troubleshooting.md
└── shared/
    └── environments.md      # Shared environment docs
```

In `deploy.md`, reference the others instead of inlining everything:

```markdown
# /project:deploy

Deploys the current service to the selected environment.

See:
- `project/deploy-checklist.md` for the full pre-deploy checklist.
- `project/deploy-troubleshooting.md` for failure modes.
- `shared/environments.md` for environment details.
```

This keeps the command definition compact while still giving the model access to richer docs when needed.

---

## 4. Progressive Disclosure for Slash Commands

Progressive disclosure means **only exposing detail when it’s needed**, to reduce clutter and cognitive load. For slash commands, design disclosure in three layers:

### 4.1 Step-by-step disclosure (procedural)

Use commands to guide users through multi-step workflows instead of dumping everything into one massive operation.

Patterns:

- One command per major step: `/project:init`, `/project:plan`, `/project:implement`, `/project:review`.
- Each command:
  - States its **current step and goal**.
  - Summarizes **what was done previously** (if relevant).
  - Clearly lists the **next actions**.

This mirrors multi-step UI flows but in command form.

### 4.2 Conditional disclosure (arguments & subcommands)

Use arguments and subcommands to reveal complexity only when the user opts into it.

Examples:

- Subcommands:
  - `/db:backup` – simple/default behavior
  - `/db:backup full` – reveals and applies additional constraints
  - `/db:backup dry-run` – explains what would happen without executing

- Flags or modes (depending on your platform):
  - `mode=quick` vs `mode=full`
  - `level=basic` vs `level=advanced`

The default invocation should be **safe, simple, and common**; advanced behavior is opt‑in.

### 4.3 Contextual disclosure (docs & references)

Reference deeper documentation only when the complexity warrants it:

- In the command body, add a short “Learn more” or “Advanced usage” section at the bottom.
- Point to:
  - Additional markdown files for advanced scenarios
  - Checklists for risky operations
  - Troubleshooting guides

Example tail section in a command file:

```markdown
---

## Advanced usage

- For blue/green and canary deployment patterns, see `project/deploy-advanced.md`.
- For rollback playbooks, see `project/rollback.md`.
```

---

## 5. Extracting Documentation into Structures & Capabilities

Design your slash command files so that they **read like structured prompts**, not ad-hoc text blobs.

### Recommended command file structure (Markdown-based)

```markdown
# /namespace:command-name

## Purpose

One or two sentences describing what this command does and when to use it.

## Inputs

- `<arg1>`: Required. Short description.
- `<arg2>`: Optional. Short description.

## Behavior

1. Step-by-step description of what the command should do.
2. Any constraints or invariants that must be respected.
3. How to handle ambiguous or partial inputs.

## Output

- What the command should return or modify (files, messages, summaries, etc.).

## Examples

- Example 1: Short example invocation and expected behavior.
- Example 2: Edge case.

## References

- `path/to/related-doc.md`
- `path/to/checklist.md`
```

This structure makes it easy for a tool or model to:

- Parse **what the command is for** (Purpose)
- Understand **how to call it** (Inputs)
- Follow **how to execute it** (Behavior)
- Format **results consistently** (Output)
- Discover **supporting docs** (References)

### Turning command files into capabilities

If you later want to convert a slash command into a more powerful skill or tool, the above structure maps cleanly into:

- Metadata (name, description, scope)
- Input schema (arguments/options)
- Execution plan (behavior steps)
- Example library (examples)
- Linked knowledge base (references)

Designing commands this way from the start makes them future‑proof.

---

## 6. Scripts, Tools, and Integration

Slash commands often orchestrate **external scripts or programs**. To keep things clean and maintainable:

### Separate orchestration from implementation

- Let the slash command define **what** should happen.
- Put heavy logic in separate scripts or services that define **how** it happens.

Example layout:

```text
commands/
├── project/
│   └── deploy.md              # High-level instructions & prompts
scripts/
├── deploy.sh                  # Implements the actual steps
└── check-env.sh
```

In `deploy.md`, describe when and how to call the scripts, not their entire content:

```markdown
## Behavior

1. Validate environment using `scripts/check-env.sh`.
2. Run `scripts/deploy.sh <environment>`.
3. Summarize the deployment results and highlight any warnings.
```

### Handling side effects safely

- Prefer **dry-run modes** for dangerous operations (deletes, migrations, production changes).
- Encourage confirmation steps in risky commands, e.g.:
  - First run `/project:deploy plan`.
  - Then `/project:deploy apply` only after review.

### Reuse shared scripts

Organize shared logic:

```text
scripts/
├── git/
│   ├── ensure-clean-tree.sh
│   └── create-tag.sh
├── ci/
│   └── run-pipeline.sh
└── env/
    └── load-vars.sh
```

Reference these from multiple commands instead of duplicating behavior.

---

## 7. Naming, Arguments, and UX

### Command naming

- Use **verbs**: `summarize-file`, `fix-imports`, `run-tests`.
- Keep names **short but specific**.
- Use `kebab-case` or the naming convention of your platform.
- Avoid overly generic names like `do`, `task`, `misc`.

### Argument design

- Use **descriptive placeholders**: `<file-path>`, `<branch>`, `<ticket-id>`.
- Show all key arguments in the command help/description.
- Default optional arguments sensibly.
- Validate arguments where the platform allows.

### Response behavior

- Be **deterministic and clear** about what happens on each run.
- Provide:
  - A brief summary at the top.
  - Details or logs below.
  - Any next recommended commands ("Next: /project:deploy-verify").

---

## 8. Example: Complete Slash Command Suite Layout

```text
.slash-commands/
├── project/
│   ├── init.md
│   ├── status.md
│   ├── plan-release.md
│   ├── deploy.md
│   └── rollback.md
├── code/
│   ├── refactor-function.md
│   ├── add-tests.md
│   └── format-project.md
├── docs/
│   ├── summarize-file.md
│   └── propose-edits.md
└── shared-docs/
    ├── environments.md
    ├── deploy-checklist.md
    └── troubleshooting.md

scripts/
├── project/
│   ├── deploy.sh
│   ├── rollback.sh
│   └── verify.sh
└── utils/
    ├── ensure-clean-tree.sh
    └── notify-chat.sh
```

This structure supports:

- **Small, focused command files** for each task
- **Namespaced commands** via directories
- **Progressive disclosure** through referenced docs and advanced commands
- **Separation of concerns** between command definitions and implementation scripts

Designing slash commands this way makes them easy for humans to read, for tools to parse, and for large language models to execute reliably as part of larger workflows.

---

## 9. Multi-Agent Delegation in Slash Commands

When a slash command needs to spawn multiple sub-agents for parallel work, follow this pattern to ensure proper execution rather than inline evaluation.

### 9.1 The Command-to-Delegation Problem

Commands that embed `Task()` patterns directly are often interpreted as **documentation templates** rather than **executable directives**. The orchestrator may read the patterns but not execute them.

**Problem Pattern (Avoid):**
```markdown
<delegation>
## Task() Patterns

Task(researcher-codebase, """...""")  # Treated as documentation
Task(code-quality, """...""")         # Not actually executed
</delegation>
```

**Solution**: Separate the command (entry point) from the skill (execution logic).

### 9.2 Architecture: Command → Skill → Agents

```
Slash Command (entry point)
    ↓ "Load skill and follow Phase X"
Skill SKILL.md (delegation contract)
    ├─ Phase 1: Load context (orchestrator)
    ├─ Phase 2: EXECUTE delegation (spawn agents)
    └─ Phase 3+: Synthesis (orchestrator)
```

**Rules:**
1. **Commands** describe what happens and point to the skill
2. **Skills** own the delegation contract and execution logic
3. **Delegation contracts** use imperative language and structured format

### 9.3 Command Responsibility (Entry Point)

The command file should:
- Tell the orchestrator which skill to load
- Tell the orchestrator which phase(s) to execute
- Explicitly state: "Do NOT perform X yourself - delegate"
- NOT embed the delegation logic itself

**Good Command Structure:**
```markdown
# /my-command

## EXECUTION PATH

### Step 1: Load Skill
Skill(my-skill-name)

### Step 2: Execute Phase 1
[Instructions for orchestrator]

### Step 3: EXECUTE Phase 2 Delegation
**CRITICAL**: Follow the delegation contract in SKILL.md.
You MUST spawn Task() for each agent. Do NOT perform this work yourself.

### Step 4: Synthesis
[Instructions for collecting results]
```

### 9.4 Skill Responsibility (Delegation Contract)

The skill SKILL.md should contain an `## EXECUTE:` section with:
- Imperative header signaling execution zone
- Structured agent specifications (JSON or table)
- Clear input/output contracts
- Sync points for parallel execution

**Good Skill Structure:**
```markdown
## EXECUTE: Phase 2 Delegation

**CRITICAL**: You MUST spawn these agents in parallel.
Do NOT perform this work yourself.

### Delegation Contract
{
  "execution": "parallel",
  "sync_point": "Wait for ALL agents before Phase 3",
  "agents": [
    {"id": "A1", "agent_type": "researcher-codebase", "prompt": "..."},
    {"id": "A2", "agent_type": "code-quality", "prompt": "..."}
  ]
}
```

### 9.5 Imperative Headers for Execution Zones

Use these header conventions to signal intent:

| Header | Meaning |
|--------|---------|
| `## EXECUTE:` | "Parse and execute this now" |
| `## REFERENCE:` | "Read this for context only" |
| `## DELEGATION:` | "This defines agent spawning" |

Avoid XML tags (`<delegation>`, `<phases>`) which may be treated as formatting.

### 9.6 Example: Multi-Agent Analysis Command

**Command (`/analyze-thing.md`):**
```markdown
# /analyze-thing

## EXECUTION PATH

1. Load skill: `Skill(analyzing-thing)`
2. Execute Phase 1: Read target files
3. **EXECUTE Phase 2**: Follow delegation contract
   - Spawn all agents from the contract
   - Do NOT analyze yourself
4. Collect results, synthesize report
```

**Skill (`SKILL.md`):**
```markdown
## EXECUTE: Phase 2 Delegation

You MUST spawn these 3 agents in parallel:

| Agent | Type | Focus |
|-------|------|-------|
| A1 | researcher-codebase | Structure |
| A2 | code-quality | Standards |
| A3 | planning | Design |

Launch all in a SINGLE message with multiple Task() calls.
```

This pattern ensures the orchestrator treats delegation as imperative instructions, not documentation.
