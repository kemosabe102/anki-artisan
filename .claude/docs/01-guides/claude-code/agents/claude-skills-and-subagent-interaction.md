# Designing Claude Agents, Sub-Agents, Skills, and Tools: A Practical Guide

The most important design rules Anthropic emphasizes for agents and skills are:

- **Do not overcomplicate the system** – start with simple workflows and only add agent loops, sub-agents, and skills when they demonstrably improve outcomes.
- **Think like the model** – design tools/skills and prompts as if you were onboarding a junior engineer who must infer everything from the interface and examples.
- **Engineer the agent–computer interface (ACI)** – invest as much care in tool and skill design as in UI/UX, with progressive disclosure, clear schemas, and test-driven iteration.

The rest of this document turns those principles into a concrete reference you can reuse when designing agents, sub‑agents, skills, and tools.

***

## 1. When to Use Agents, Sub‑Agents, Skills, and Plain Tools

### 1.1 Workflows vs Agents

Anthropic draws a clear line between **workflows** and **agents**:

- **Workflows:**  
  - LLM + tools orchestrated by fixed code paths.  
  - Deterministic, easier to test, cheaper and faster.  
  - Good for: predictable pipelines (RAG, templateable transforms, “LLM in the middle” flows).

- **Agents:**  
  - LLM controls its own process in a loop, deciding which tools to use and how many steps to take.  
  - Good for: open‑ended tasks where step count and needed tools cannot be known ahead of time (complex coding tasks, multi‑stage research, computer-use agents).

**Guideline:** Start with workflows; only graduate to agents when you can show that fixed pipelines fail to meet requirements (accuracy, robustness, UX).

### 1.2 When to Introduce Sub‑Agents

Sub‑agents become useful when a single agent’s context window and responsibilities become unwieldy:

- **Use sub‑agents when:**  
  - You need **context isolation** for large, messy subtasks (e.g., research over many sources, deep codebase analysis).
  - You want **high compression**: sub‑agent consumes tens of thousands of tokens and returns a compressed plan/summary (1–2K tokens) back to the orchestrator.
  - Different subtasks benefit from **different tools, instructions, and memory** (e.g., “researcher” vs “planner” vs “executor”).
  - You want **parallel exploration** of multiple hypotheses or directions.

- **Avoid sub‑agents when:**  
  - The main agent can handle the task with a simple prompt chain or just a few tools.  
  - You are using sub‑agents primarily to “save tokens” rather than to **structure context and responsibilities**.

### 1.3 When to Use Skills vs “Raw” Tools

Skills are Anthropic’s mechanism for packaging procedural knowledge + resources; tools/MCP servers provide **capabilities** (APIs, filesystem, code exec).

- **Tools / MCP servers:**  
  - Represent concrete actions (e.g., call REST API, run SQL, read files, invoke script).
  - Should be **mechanically simple and deterministic**.  
  - Primary focus is on **clean interfaces and safety**.

- **Skills:**
  - Are **folders of instructions and resources** (markdown, code, reference docs) that agents discover and load via progressive disclosure.  
  - Teach the agent *how* to perform a workflow or domain-specific process.  
  - Can contain both:  
    - Instructional docs (checklists, style guides, SOPs).  
    - Code/scripts that are then used via tools.

**Agent perspective:**  
- Tools = “system calls” (eyes and hands).  
- Skills = “playbooks and manuals” that the agent selectively opens as needed.

***

## 2. Core Design Principles from Anthropic

### 2.1 Simplicity

- Start with the **simplest possible system** (single LLM call, maybe RAG).
- Add **prompt chaining**, routing, or parallelization when needed.
- Only then introduce **agents**, sub‑agents, Skills, or complex orchestrations when simpler structures cannot achieve the goal.

Indicators you are adding too much complexity:

- Many tools that are rarely used or poorly distinguishable by description.  
- Sub‑agents with overlapping roles and no clear accountability.  
- Hard‑to‑explain execution traces.

### 2.2 Transparency

- Make **planning steps explicit** in the prompt (e.g., “think, then act” pattern) and in the UI/logs.
- When using sub‑agents, emit a **clear ledger of tasks, delegation, and results** so humans can debug and audit.
- For long‑running agents, use checkpoints and expose intermediate thoughts or summaries where safe.

### 2.3 Agent–Computer Interface (ACI) Quality

Anthropic explicitly advocates treating tool and skill design as HCI for agents:

- Design tools as if for a **junior developer**; they must be obvious from names, descriptions, and examples.  
- Provide **robust documentation**: usage examples, edge cases, failure modes, expected formats.
- Iterate based on **observed mistakes** in real runs; optimize tools and skills more than you optimize the main prompt.

***

## 3. Skill Design: Progressive Disclosure and Structure

### 3.1 Progressive Disclosure

Progressive disclosure is the key pattern that makes Skills scalable:

- **Level 1: Metadata (always in system prompt)**  
  - `name`: machine‑friendly identifier (often hyphen/kebab-case).  
  - `description`: short, specific description of when the skill should be used.  
  - This is what Claude uses to decide *if* a skill is relevant.

- **Level 2: SKILL.md body**  
  - Loaded only when the agent decides the skill might help.  
  - Contains top‑level instructions, high‑level workflow, and links to deeper references.

- **Level 3+: Linked files and resources**  
  - Skill references extra markdown and scripts (`reference.md`, `forms.md`, `workflow/*.md`, etc.).  
  - Agent uses filesystem tools (e.g., `Read`, `Bash`) to load specific documents on demand.

Design implications:

- **Keep Level 1 and 2 tight.** Move rare or specialized subflows into deeper files.  
- Use the filesystem as **unbounded context**: store large docs, examples, and code; pay tokens only when reading them.

### 3.2 Anatomy of a Skill

Per Anthropic’s Agent Skills spec and docs:

- **Directory structure (conceptual):**

  - `skill-name/`  
    - `SKILL.md` (required; YAML frontmatter + body)  
    - Additional markdown: `reference.md`, `forms.md`, `checklists/*.md`  
    - Code: scripts, helpers, test harnesses (Python, shell, etc.)

- **YAML frontmatter (minimal fields):**
  - `name`: must match directory name and be unique.  
  - `description`: short, concrete trigger description (“Use this skill when …”).  
  - Optional other metadata (version, tags, etc.).

- **SKILL.md body:**
  - Overview and high‑level purpose.  
  - A copyable **procedure/checklist** for the agent.  
  - Links (“When doing X, read `forms.md` first”).  
  - Any invariants or safety checks (“Never send PII externally”, “Always confirm with the user before executing destructive actions”).

### 3.3 Authoring Best Practices

From Anthropic’s skill docs and posts:

- **Start with evaluation:**  
  - Run the agent on real tasks; identify concrete pain points or failures; build Skills only for gaps that recur.

- **Structure for scale:**  
  - As SKILL.md grows, **split** by mutually exclusive contexts (e.g., “editing vs drafting” docs, “forms vs general PDFs”).  
  - Keep the main SKILL.md lean; push specifics to referenced files.

- **Think from Claude’s perspective:**  
  - Monitor how the agent actually uses the skill; watch for:  
    - Over‑activation (skill triggered too often).  
    - Under‑activation (skill rarely used even when relevant).  
    - Mis‑navigation (reading unrelated files).

- **Iterate with Claude:**  
  - While using the system, ask the agent to **capture its best patterns/mistakes** into the skill files themselves.  
  - Ask it to propose better structure (“Propose a checklist for this skill based on the last 10 tasks”).

- **Security and safety:**  
  - Audit code and instructions in any third‑party skill, especially networked code or dependencies.
  - Treat skills from untrusted sources like untrusted plugins or shell scripts.

***

## 4. Tool Design Best Practices (from the Agent’s Perspective)

Anthropic’s “Prompt engineering your tools” guidance is directly about how agents should perceive and use tools.

### 4.1 Choose LLM‑Friendly Formats

Tools should be **easy for an LLM to call correctly**:

- Avoid formats that require the model to:  
  - Count large line numbers or diff offsets.  
  - Heavily escape code strings.  
  - Maintain exact character counts.

- Prefer:  
  - Whole‑file rewrites over diffs when possible.  
  - Code in markdown instead of embedded JSON strings.  
  - Natural structures that look like documentation the model has seen online.

### 4.2 Parameter and Schema Design

- **Intuitive names:**  
  - Parameter names should be descriptive and role‑revealing (`file_path`, `query`, `max_results`, `dry_run`) rather than generic (`arg1`, `content`).

- **Clear descriptions:**  
  - Describe semantics, not just types. E.g., “Absolute path to the file in the repo root; must start with `/workspace/`.”

- **Poka‑yoke (error‑proofing):**  
  - Make wrong usage difficult:  
    - Require absolute paths instead of relative when path confusion is common.  
    - Split one ambiguous tool into two unambiguous ones (`read_file` vs `write_file`).  
    - Use enums where possible.

- **Use examples and edge cases:**  
  - For complex tools, show **valid and invalid** calls with full JSON payloads.  
  - Encode subtle rules (e.g., correlation of optional parameters) via examples.

### 4.3 Tool Use Control (tool_choice and strict tools)

Claude’s API allows fine‑grained control over when tools must or must not be used:

- `tool_choice = "auto"`: default; agent can decide to call tools or not.  
- `tool_choice = { "type": "any" }`: agent must call one of the tools at least once.  
- **Strict tool use** with schemas: enforce well‑formed arguments and catch malformed calls early.

Agent‑design implications:

- Use **auto** for general assistant agents that should be trusted to decide.  
- Use **any + strict** when building a sub‑agent whose very purpose is to call a particular tool (e.g., “SQL executor agent”).

### 4.4 Testing and Iteration

- Run a **large suite of prompts** through your agent using each tool; inspect:  
  - Incorrect/non‑minimal tool calls.  
  - Missing required parameters.  
  - Confusion between similar tools.  
- Fix by adjusting descriptions, parameter names, examples, or even splitting/merging tools.

***

## 5. Designing Agent–Skill–Tool Interaction

Now, from the agent’s perspective, what does a healthy interaction pattern look like?

### 5.1 Baseline Agent Loop

A typical Claude agent with tools and skills follows this cycle:

1. **Interpret task** from user message + system prompt + skill metadata (names/descriptions).  
2. **Decide if a skill is relevant** (using Level‑1 metadata); if so, read SKILL.md.  
3. **If needed, load deeper skill references** (other markdown files, examples).  
4. **Plan** a sequence of steps (possibly visible to user).  
5. **Call tools** (code exec, filesystem, MCP servers, Skills tool, etc.) as needed.  
6. **Incorporate tool results**, update plan, and iterate.  
7. **Produce final answer**, optionally writing new artifacts (files, reports, etc.).

Design goal: make each of those steps **obvious and ergonomic** for the agent.

### 5.2 Sub‑Agent Pattern (Orchestrator–Worker)

Anthropic’s own multi‑agent research system uses a **lead agent + sub‑agents** design.

- **Lead agent (orchestrator):**  
  - Receives the user request.  
  - Plans the decomposition into subtasks.  
  - Spawns worker agents (sub‑agents) with focused instructions and tools.  
  - Aggregates sub‑agent outputs into final answer.

- **Sub‑agents:**  
  - Operate with their **own context windows** (context isolation).  
  - Often run in parallel, exploring different aspects of the task.  
  - Return compressed artifacts (summaries, lists, plans, structured results) rather than raw trajectories.

Design tips:

- Sub‑agents should be **domain‑specialized** (“researcher”, “planner”, “fact‑checker”, “code modifier”).  
- Each sub‑agent should have:
  - Its own system prompt describing role and tools.  
  - Well‑scoped tools and Skills.  
  - A clearly defined **return schema**, often enforced by constrained decoding or a “submit_results” tool.

### 5.3 Context Management Strategies

From Anthropic and related context‑engineering work:

- **Reduce context:**  
  - Summarize long histories into short “working memory” before passing to sub‑agents.  
  - Use Skills/filesystem as external memory; read only what's necessary.

- **Offload context:**  
  - Store raw artifacts in files (logs, code, documents).  
  - Give agents tools to read specific files instead of keeping everything in the chat history.

- **Isolate context:**  
  - Use sub‑agents for discrete tasks with independent context windows.  
  - Route specialized tasks to agents whose history is **only about that task**, avoiding cross‑pollution.

Concrete pattern:

- Planner agent maintains a **task ledger** (structured list of work items).  
- For each item, it may spin up a sub‑agent with:
  - A short description of the task.  
  - Pointers (paths/URLs) to relevant materials.  
  - Expected output schema.  
- Sub‑agent explores widely, then writes a **summary artifact** for the planner to ingest.

***

## 6. Concrete Patterns You Can Reuse

This section gives patterns you can copy into your own designs.

### 6.1 Pattern: Simple Skill‑Aware Single Agent

Use when you want a single agent that automatically uses domain Skills when relevant.

- System prompt:
  - High‑level role.  
  - Instruction to:  
    - Consider Skill metadata when deciding how to complete tasks.  
    - Load SKILL.md only when the skill seems relevant.  
    - Follow the skill’s checklists and safety rules.

- Skill design:
  - Clear descriptions (“Use this skill when working with PDFs that need form filling”).
  - Checklists and examples in SKILL.md + deeper files.  
  - Optional scripts as tools (e.g., “extract_form_fields.py”).

- Tools:
  - Filesystem read/write.  
  - Code execution.  
  - Possibly MCP‑backed tools.

### 6.2 Pattern: Planner + Skill‑Using Worker Sub‑Agent

Use when tasks are long‑running and you want an explicit “planner” and “executor”.

- **Planner agent:**
  - Tools: none or minimal (maybe read/write ledger file).  
  - Responsibilities:  
    - Interpret user goal.  
    - Break into subtasks (task ledger).  
    - Decide which sub‑agent type or Skill applies to each subtask.

- **Worker sub‑agent:**
  - Tools: full set (Skills, filesystem, code execution, MCP).  
  - Instructions:  
    - Treat the assigned task as your *only* goal.  
    - For each step, consider relevant Skills; load them progressively.  
    - Record key decisions in a summary for the planner.

This matches patterns described by Anthropic and other multi‑agent orchestration guides.

### 6.3 Pattern: Research Sub‑Agent for High‑Compression Exploration

Used by Anthropic’s research system and others:

- Sub‑agent:
  - Tools: web search, document retrieval, Skills for synthesis.  
  - Large thinking budget (tokens).  
  - Output: a structured research memo or JSON summary (1–2K tokens).

- Orchestrator:
  - Uses the memo to update plan and inform next decisions.  
  - Never needs to ingest the entire research trajectory.

This is ideal when you are building a “researcher for your main agent” in your own system.

***

## 7. Security, Safety, and Governance

Agents + Skills + tools create new security surfaces.

Key practices:

- **Trust model:**
  - Only install Skills and MCP servers from trusted sources.  
  - Audit code and instructions, especially network calls or shell commands.

- **Prompt‑injection and data‑exfiltration:**
  - Treat external data (web pages, PDFs, emails) as potentially adversarial; do not blindly follow instructions in them.  
  - Consider guardrail prompts or separate “safety agents” for critical environments.

- **Least privilege:**
  - Limit tools and Skills per agent to what’s necessary.  
  - Use separate sandboxes for higher‑risk capabilities (e.g., code execution, file system).

- **Monitoring and logging:**
  - Log tool calls, skill usage, and sub‑agent delegations.  
  - Review logs periodically, especially for sensitive environments.

***

## 8. Practical Design Checklist (For Your Own Projects)

When designing a new agent + skills + tools setup, walk through this abbreviated checklist:

1. **Do you really need an agent?**  
   - Try single‑call + RAG first.  
   - Consider prompt chaining / routing before going full agent.

2. **Is sub‑agent complexity justified?**  
   - Are there clear context‑isolation needs?  
   - Will sub‑agents produce high‑compression outputs that justify overhead?

3. **Are skills scoped and structured via progressive disclosure?**  
   - Clear `name` and `description` that make it obvious *when* to use each skill.
   - SKILL.md small and acts as “table of contents”, deeper files for specifics.  
   - Checklists and workflows captured as explicit steps.

4. **Are tools designed for the model’s ergonomics?**  
   - Human‑readable parameter names and descriptions.  
   - Examples for complex tools.  
   - Formats that minimize diff/escaping complexity.

5. **Is the agent–sub‑agent protocol explicit?**  
   - Planner clearly defines subtask scope and expected output schema.  
   - Sub‑agents have clear role prompts and limited toolsets.

6. **Have you tested on real tasks and iterated?**  
   - Capture failure modes: wrong tool choice, skill misuse, context bloat.  
   - Adjust skill metadata, tool docs, or architecture accordingly.

7. **Are safety and governance covered?**  
   - Skills and MCP servers from trusted sources only.  
   - Sandboxed execution and least‑privilege access.
