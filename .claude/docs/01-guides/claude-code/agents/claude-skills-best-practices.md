# Claude Skills Best Practices

## 1. Purpose and Philosophy

Claude Skills are **reusable, filesystem-backed capabilities** that extend what Claude can do in a project or workspace. A Skill is a small, well-structured bundle of:

- A core `SKILL.md` file with metadata and instructions
- Optional reference docs (markdown)
- Optional executable scripts

Good Skills behave like **power tools** for Claude:

- **Discoverable** – Claude can understand what they do and when to use them
- **Composable** – They fit into larger workflows and agent systems
- **Progressive** – They reveal detail only when needed, preserving context
- **Maintainable** – They are concise, testable, and easy to evolve

Think of a Skill as a **library-quality prompt + tool bundle** that Claude can reliably call on, rather than a one-off instruction.

---

## 2. File Size and Content Scope

### Keep `SKILL.md` concise

The **SKILL.md file should stay under 500 lines** for optimal performance. This is your core file that functions like a table of contents and overview.

Guidelines:

- Include only what Claude **cannot reasonably infer** from its pretraining or the surrounding project
- Avoid long background explanations or tutorials
- Prefer concrete code, procedures, and rules over prose essays

If your content exceeds this limit, split it into separate files using progressive disclosure patterns, loading additional content only when needed.

### Match specificity to task fragility

Use three levels of instruction detail (from the Anthropic guidance):

- **High freedom (text-based instructions)** – For robust, low-risk tasks
- **Medium freedom (pseudocode or scripts with parameters)** – For more fragile or constrained workflows
- **Low freedom (exact scripts/commands)** – For dangerous, high-stakes, or highly standardized operations

The more fragile or risky the task, the more concrete and prescriptive the instructions should be.

---

## 3. Documentation Coordination & Extraction

Claude Skills use a **filesystem-based architecture** that enables smart documentation extraction instead of stuffing everything into a single prompt.

### Basic structure

- `SKILL.md` – Core metadata and high-level instructions (< 500 lines)
- Additional files – Loaded progressively as needed

Example:

```text
skill-directory/
├── SKILL.md                 # Metadata + overview (loaded when triggered)
├── instructions.md          # Detailed workflows (loaded as needed)
├── parameters.md            # Configuration details (conditional)
├── examples/
│   ├── example1.md          # Task examples (progressive)
│   └── example2.md
└── troubleshooting.md       # Advanced help (on-demand)
```

### How Claude reads Skills

Claude:

- Sees only **name** and **description** of all Skills at startup
- Reads `SKILL.md` when a Skill becomes relevant
- Reads referenced files only when needed

This means:

- Start with `SKILL.md` as an **overview/table of contents**
- Point to detailed materials only when relevant
- Treat documentation as a **reference library**, not mandatory pre-loaded context

---

## 4. Progressive Disclosure in Skills

Progressive disclosure keeps your Skill powerful without blowing the context window. Design Skill content in three layers.

### 4.1 Step-by-step disclosure (procedural)

Break complex operations into **clear, sequential steps**. For particularly complex workflows, provide a checklist that Claude can copy into its response and check off as it progresses.

Example pattern inside `SKILL.md`:

```markdown
## Research synthesis workflow

Copy this checklist and track your progress:

Research Progress:
- [ ] Step 1: Read all source documents
- [ ] Step 2: Identify key themes
- [ ] Step 3: Cross-reference claims
- [ ] Step 4: Create structured summary
- [ ] Step 5: Verify citations

**Step 1: Read all source documents**
...
```

This helps both Claude and humans track progress through multi-step processes.

### 4.2 Conditional disclosure (by domain or feature)

Organize content so **only relevant domains are loaded**.

Example:

```text
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (campaigns, attribution)
```

And in `SKILL.md`:

```markdown
## Available datasets

**Finance** → [reference/finance.md](reference/finance.md)
**Sales**   → [reference/sales.md](reference/sales.md)
**Product** → [reference/product.md](reference/product.md)
**Marketing** → [reference/marketing.md](reference/marketing.md)
```

When the user asks about sales, Claude only needs to read `reference/sales.md`, not the entire reference tree.

### 4.3 Contextual disclosure (advanced docs & edge cases)

Show basic content in `SKILL.md`, and push specialized details to separate files that are only pulled in when needed.

Example:

```markdown
# DOCX Processing

## Creating documents
Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents
For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

Claude reads `REDLINING.md` or `OOXML.md` only when those topics are relevant.

---

## 5. Skill Structure: From Metadata to Capabilities

### YAML frontmatter

Every `SKILL.md` must start with at least:

```yaml
---
name: pdf-processing
description: >
  Extracts text and tables from PDF files, fills forms, and merges documents.
  Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---
```

Best practices:

- **Name**
  - Lowercase letters, numbers, hyphens only
  - Prefer **gerund form**: `processing-pdfs`, `analyzing-spreadsheets`, `testing-code`
  - Avoid vague names like `helper`, `utils`, `documents`, `data`, `files`

- **Description**
  - Always written in **third person**
  - Include both **what** the Skill does and **when** to use it
  - Be specific and include key trigger terms

Good examples:

- `Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDFs, forms, or document extraction.`
- `Analyze Excel spreadsheets, create pivot tables, generate charts. Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files.`

### Body structure for `SKILL.md`

A practical pattern:

```markdown
---
name: bigquery-analysis
description: Analyze BigQuery datasets and generate SQL queries for finance, sales, product, and marketing domains.
---

# BigQuery Data Analysis

## Quick start

[Short, concrete example or command]

## Workflows

[Step-by-step procedures or checklists]

## Domains

[Links to domain-specific reference files]

## Utility scripts

[How and when to run scripts, with commands]

## Validation loops

[How to validate outputs and correct errors]

## Examples

[Curated input/output pairs]
```

This makes it easy to "lift" the Skill definition into a more structured agent capability later if needed.

---

## 6. Scripts and Supporting Resources

Skills can bundle **executable scripts** that run in Claude’s code execution environment.

### Separate instructions from implementation

- Keep **procedural logic and guidance** in markdown
- Put **heavy lifting** into scripts
- In `SKILL.md`, explain **when and how** to run scripts, not their full implementation

Example layout:

```text
pdf/
├── SKILL.md              # Main instructions (loaded when triggered)
├── FORMS.md              # Form-filling guide (loaded as needed)
├── reference.md          # API reference (loaded as needed)
├── examples.md           # Usage examples (loaded as needed)
└── scripts/
    ├── analyze_form.py   # Utility script (executed, not loaded)
    ├── fill_form.py      # Form filling script
    └── validate.py       # Validation script
```

In `SKILL.md`:

```markdown
## Utility scripts

**analyze_form.py** – Extract all form fields from PDF

```bash
python scripts/analyze_form.py input.pdf > fields.json
```

**validate.py** – Validate field mappings

```bash
python scripts/validate.py fields.json
```
```

### Prefer execution over introspection

Be explicit whether Claude should:

- **Execute** the script: `"Run scripts/analyze_form.py to extract fields"`
- Or **read** it as reference: `"Read scripts/analyze_form.py for the extraction algorithm"`

For most utility scripts, executing is more reliable and efficient than loading the entire file into context.

### Validation and safety loops

Use the "plan–validate–execute" pattern for complex or destructive operations:

1. Create a structured **plan file** (for example, `changes.json`)
2. Run a **validator script** on that file
3. Only if validation passes, **apply changes**
4. Optionally, run a **post-verify** step

This greatly reduces the risk of silent, large-scale errors.

---

## 7. Linking and Depth: How Many Levels is Too Many?

Claude may preview referenced files with partial reads (for example `head -100`). To ensure it still understands the whole shape of your docs:

- Keep references from `SKILL.md` **one level deep**
- Avoid deep chains like: `SKILL.md → advanced.md → details.md`

Bad:

```markdown
# SKILL.md
See [advanced.md](advanced.md)...

# advanced.md
See [details.md](details.md)...

# details.md
Here's the actual information...
```

Good:

```markdown
# SKILL.md

**Basic usage**: [instructions in SKILL.md]
**Advanced features**: See [advanced.md](advanced.md)
**API reference**: See [reference.md](reference.md)
**Examples**: See [examples.md](examples.md)
```

For long reference files (> 100 lines), include a **table of contents** at the top so Claude can see what’s inside even when only the first part is read.

---

## 8. Style, Consistency, and Output Formats

### Be consistent with terms

Pick one term for each concept and use it consistently across the Skill (for example, always "customer" not "user"/"client"/"account" interchangeably). This improves Claude’s ability to follow and apply rules correctly.

### Provide output templates

For strict outputs (APIs, structured reports), give templates:

```markdown
## Report structure

ALWAYS use this exact template structure:

```markdown
# [Analysis Title]

## Executive summary
[One-paragraph overview of key findings]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```
```

For more flexible outputs, present the template as guidance rather than a hard requirement.

### Use examples liberally

Provide input/output pairs for styles Claude must mimic (commit messages, ticket descriptions, email styles, etc.). Examples often communicate expectations far better than prose descriptions.

---

## 9. Evaluation-Driven Skill Development

Treat Skills like software components: **design, test, iterate**.

Recommended loop:

1. **Do the task once without a Skill** – Work with Claude interactively and note what you repeat
2. **Extract the reusable pattern** – Data sources, rules, naming conventions, safety checks
3. **Ask Claude to draft `SKILL.md`** – "Create a Skill that captures this pattern"
4. **Review for conciseness and structure** – Remove explanations Claude doesn’t need; organize into references
5. **Test with real tasks** – Use a fresh Claude instance with the Skill loaded
6. **Iterate based on observed failures** – Refine instructions, workflows, and references

You can even define evaluation cases (inputs, expected behavior) in a simple JSON or YAML format to guide manual or scripted testing.

---

## 10. Example: Complete Skill Directory

```text
mortgage-analyzer-skill/
├── SKILL.md                           # 300 lines max
│   ├── Overview
│   ├── Core capabilities
│   └── File references (not full content)
├── core_workflows/
│   ├── rate_analysis.md               # Loaded when analyzing rates
│   └── payment_calculation.md         # Loaded for payments
├── advanced_features/
│   ├── scenario_modeling.md           # Progressive - conditional
│   └── risk_assessment.md             # Progressive - conditional
├── scripts/
│   ├── calculate_amortization.py      # Called by workflows
│   └── validate_inputs.py             # Verification step
└── examples/
    ├── scenario1_first_time_buyer.md  # Reference examples
    └── scenario2_refinance.md
```

This structure ensures **SKILL.md stays lean**, **documentation is discoverable**, and **supporting resources load only when needed** — the same design philosophy as your slash commands and sub-agent best practices.

---

## 11. Skills Evaluation Checklist (360° Analysis)

Use this tiered checklist when creating or reviewing a Skill. Tiers indicate severity:

- **Tier 1 (Critical)**: Must pass — failures mean skill won't function correctly
- **Tier 2 (Required)**: Should pass — failures indicate significant quality issues  
- **Tier 3 (Best Practice)**: Recommended — improves effectiveness but not blocking

> **Sources**: Anthropic `skill-creator` skill, [Using Skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude), project standards

---

### Tier 1: Critical Requirements (Must Pass)

#### 1.1 YAML Frontmatter
- [ ] Contains ONLY `name` and `description` fields
- [ ] No `model`, `tools`, or other fields present

#### 1.2 Naming
- [ ] `name` is lowercase with hyphens only (no spaces, underscores, uppercase)
- [ ] `name` ≤64 characters
- [ ] Directory name matches skill name exactly

#### 1.3 Required Files
- [ ] SKILL.md exists in skill directory
- [ ] No "When to Use This Skill" section in SKILL.md body (belongs in description)

#### 1.4 Body Size
- [ ] SKILL.md body is under 500 lines

---

### Tier 2: Required Standards (Should Pass)

#### 2.1 Description Quality
- [ ] Description includes WHAT the skill does
- [ ] Description includes WHEN to use it (trigger conditions)
- [ ] Description written in third person
- [ ] Description under 1024 characters
- [ ] Includes trigger keywords users might say

#### 2.2 Naming Quality
- [ ] Uses gerund form (verb + -ing): `processing-pdfs` not `pdf-processor`
- [ ] Name is specific (not `helper`, `utils`, `data`, `files`, `documents`)

#### 2.3 Structure Compliance
- [ ] NO auxiliary files: README.md, CHANGELOG.md, INSTALLATION_GUIDE.md, etc.
- [ ] All referenced files exist within skill directory
- [ ] No broken references to non-existent files

#### 2.4 Architecture
- [ ] No Task() delegation patterns (skills don't orchestrate agents)
- [ ] No agent references (skills are self-contained capabilities)

---

### Tier 3: Best Practices (Recommended)

#### 3.1 Progressive Disclosure
- [ ] References from SKILL.md are ONE level deep only (no A.md → B.md → C.md chains)
- [ ] Reference files >100 lines have table of contents at top
- [ ] Domain/variant content split into separate files
- [ ] SKILL.md serves as overview/navigation hub

#### 3.2 Content Quality
- [ ] Uses imperative/infinitive form for instructions
- [ ] Only includes what Claude cannot reasonably infer
- [ ] Prefers concrete examples over verbose explanations
- [ ] Consistent terminology throughout (one term per concept)
- [ ] Output templates provided for strict format requirements

#### 3.3 Resource Organization
- [ ] `scripts/` contains executable code only (deterministic tasks)
- [ ] `references/` contains documentation loaded into context as needed
- [ ] `assets/` contains output files (templates, images — NOT loaded into context)
- [ ] No information duplicated between SKILL.md and reference files
- [ ] Scripts documented with when/how to run them

#### 3.4 Workflows
- [ ] Complex processes broken into clear steps or checklists
- [ ] Risky/destructive operations use plan–validate–execute pattern
- [ ] Examples illustrate style and edge cases
- [ ] Degrees of freedom match task fragility (low freedom = fragile tasks)

#### 3.5 Testing
- [ ] Skill tested on real tasks (not just theoretical review)
- [ ] Refined based on observed failures and inefficiencies
- [ ] Scripts tested and produce expected output

---

### Quick Evaluation Summary Template

```markdown
## Skill Evaluation: [skill-name]

### Tier 1 (Critical): [PASS/FAIL]
- YAML fields: [✅/❌]
- Naming: [✅/❌]  
- Required files: [✅/❌]
- Body size: [✅/❌] ([X] lines)

### Tier 2 (Required): [PASS/FAIL]
- Description quality: [✅/❌]
- Naming quality: [✅/❌]
- Structure compliance: [✅/❌]
- Architecture: [✅/❌]

### Tier 3 (Best Practice): [X/Y passing]
- Progressive disclosure: [✅/❌]
- Content quality: [✅/❌]
- Resource organization: [✅/❌]
- Workflows: [✅/❌]
- Testing: [✅/❌]

**Overall**: [PASS/NEEDS WORK/FAIL]
**Priority Issues**: [list blocking issues]
```

---

## 10. Delegation Contracts for Multi-Agent Skills

When a skill needs to coordinate multiple sub-agents for parallel work, use **delegation contracts** to ensure proper execution.

### 10.1 The Delegation Problem

Skills that describe agent spawning as documentation templates may not be executed. The orchestrator reads the patterns but doesn't act on them.

**Solution**: Use imperative headers and structured contracts that signal execution intent.

### 10.2 Imperative Headers

Use `## EXECUTE:` headers to signal delegation zones:

| Header | Meaning |
|--------|---------|
| `## EXECUTE:` | Parse and execute this now (spawn agents) |
| `## REFERENCE:` | Read for context only |
| `## DELEGATION:` | Defines agent spawning (parseable contract) |

**Example:**
```markdown
## EXECUTE: Phase 2 Delegation

**CRITICAL**: You MUST spawn these agents in parallel.
Do NOT perform this work yourself.
```

### 10.3 Delegation Contract Schema

Include a structured contract that the orchestrator can parse:

```json
{
  "phase": "P2_EVALUATE",
  "execution": "parallel",
  "max_agents": 5,
  "sync_point": "Wait for ALL agents before proceeding",
  "agents": [
    {
      "id": "A1",
      "dimension": "Structure",
      "agent_type": "researcher-codebase",
      "prompt": "Evaluate X against Y criteria. Return JSON: {...}",
      "input": "file paths or context",
      "output": "expected JSON schema"
    },
    {
      "id": "A2",
      "dimension": "Quality",
      "agent_type": "code-quality",
      "prompt": "Review Z for standards. Return JSON: {...}",
      "input": "file paths or context",
      "output": "expected JSON schema"
    }
  ]
}
```

### 10.4 Contract Fields

| Field | Required | Description |
|-------|----------|-------------|
| `phase` | Yes | Phase identifier (e.g., "P2_EVALUATE") |
| `execution` | Yes | "parallel" or "sequential" |
| `max_agents` | No | Limit on concurrent agents (default: 5) |
| `sync_point` | Yes | When to proceed to next phase |
| `agents` | Yes | Array of agent specifications |
| `agents[].id` | Yes | Unique identifier for this agent |
| `agents[].agent_type` | Yes | Sub-agent type to spawn |
| `agents[].prompt` | Yes | Task description for the agent |
| `agents[].input` | No | What context to pass |
| `agents[].output` | No | Expected return format |

### 10.5 Execution Instructions

After the contract, include explicit instructions:

```markdown
### How to Execute This Contract

For each agent in the contract above, call:

Task(agent_type, """
Goal: [prompt from contract]
Map: [input files]
Constraints: Return structured JSON only.
""")

Launch all agents in a SINGLE message with multiple Task() calls.
Wait for all agents before proceeding to next phase.
```

### 10.6 Anti-Patterns

**NEVER:**
- Put delegation contracts in XML tags (`<delegation>`) - treated as formatting
- Omit the `## EXECUTE:` header - may be skipped
- Describe agents without imperative language - treated as documentation
- Put contracts in the command file - belongs in SKILL.md

**ALWAYS:**
- Use `## EXECUTE:` to signal delegation zones
- Include structured JSON contract
- Add explicit "You MUST spawn" instructions
- Define sync points between phases
