# Slash Command Conversion Task

**Source Command**: [PASTE COMMAND NAME HERE, e.g., "review", "spec", "plan"]
**Source Path**: `.claude/commands/[COMMAND-NAME].md`

## Instructions

Convert the legacy flat-file slash command definition to the NEW streamlined directory-based structure, following the `/git` command reference implementation.

### Target Structure (~100-200 lines main file)

```
.claude/commands/{command-name}/
├── {command-name}.md           # Main definition (STREAMLINED)
├── docs/
│   ├── README.md               # Overview of supporting docs
│   ├── workflow-phases.md      # Detailed phase documentation (if multi-phase)
│   ├── delegation-patterns.md  # Agent delegation with exact Task() syntax
│   ├── error-handling.md       # Error scenarios and recovery
│   └── {domain-specific}.md    # Domain-specific details
├── examples/
│   ├── README.md               # Overview of examples
│   └── usage-examples.md       # Complete usage scenarios
└── schemas/
    ├── README.md               # Schema documentation
    └── {command}.schema.json   # Output schema (if applicable)
```

### Main Command File Template (~100-200 lines)

```markdown
---
argument-hint: '[arguments with options]'
description: '{1-2 sentence description with trigger keywords. Use for: X. NOT for: Y.}'
allowed-tools: {comma-separated tool list}
model: {sonnet|opus}
---

# {Command Name} Command

*{One-line philosophy/purpose}*

---

## Core Behavior

YOU ARE A {ROLE} ORCHESTRATOR.

### How to Start
Parse $ARGUMENTS -> {initial action} -> {workflow}

### The Flow
User: /{command} {args} -> Step 1 -> Step 2 -> Step 3 -> Result

### Anti-Patterns (NEVER DO)
- {3-5 items with rationale}

### Good Patterns (ALWAYS DO)
- {3-5 items}

---

## Modes

| User Says | Mode | Action |
|-----------|------|--------|
| `/{command}` or `/{command} {default}` | {Default} | {Default action} |
| `/{command} {variant}` | {Variant} | {Variant action} |
| `--{flag}` | {Flag mode} | {Flag effect} |

---

## Workflow Overview

```text
PHASE 1: {NAME} [{Framework}] -> {Agent or Action}
  |-- {Brief description}
  |-- Output: {What this phase produces}

PHASE 2: {NAME} [{Framework}] -> {Agent or Action}
  |-- {Brief description}
  |-- Output: {What this phase produces}

[Continue for all phases...]

HUMAN DECISION (if applicable)
  |-- {What user decides}
  |-- Options: {choices}
```

**Framework Reference**: `.claude/docs/00-core/frameworks/README.md`

---

## Critical Safety Constraints (if applicable)

### SAFE Operations
- {Safe commands/actions}

### FORBIDDEN Operations
- {Dangerous commands/actions}

**Core Principle**: {Safety philosophy}

---

## Agent Delegation

| Phase | Agent | Operation |
|-------|-------|-----------|
| 1 | {agent-name} | {operation_type} |
| 2 | {agent-name} | {operation_type} |
| ... | ... | ... |

---

## Delegation Instructions (MANDATORY)

**Quick Reference**:
- Phase 1: `Task({agent}, {operation})`
- Phase 2: `Task({agent}, {operation})`
- ...

**Full Task() syntax with exact prompts**: `docs/delegation-patterns.md`

---

## Error Recovery (Quick Reference)

| Error Type | Recovery |
|------------|----------|
| {Error 1} | {Recovery strategy} |
| {Error 2} | {Recovery strategy} |
| ... | ... |

**See**: `docs/error-handling.md` for detailed recovery patterns

---

## Output Format

### Success Output
```text
{Example successful output format}
```

### Error Output
```text
{Example error output format}
```

---

## Knowledge Base

- `docs/workflow-phases.md` - Detailed phase documentation
- `docs/delegation-patterns.md` - **EXACT Task() call syntax**
- `docs/error-handling.md` - Complete error recovery patterns
- `examples/usage-examples.md` - Full workflow examples

---

## Orchestrator Integration

**Trigger Keywords**: {keywords that trigger this command}

**Delegation Pattern**:
```
User: "{natural language request}"
Claude Code (OBSERVE): Parse request -> Identify /{command} trigger
Claude Code (ORIENT): {What context is gathered}
Claude Code (DECIDE): ASC = X.XX -> Delegate to /{command}
Claude Code (ACT): SlashCommand(command="/{command} {args}")
```

**Integration Points**:
- Upstream: {What triggers this command}
- Downstream: {What this command leads to}
```

---

### Conversion Rules

1. **ELIMINATE** these legacy sections (move to `docs/` if essential):
   - Multi-page workflow phase descriptions (>50 lines per phase)
   - Verbose "Implementation Roadmap" sections
   - Extensive code examples (>20 lines each)
   - Detailed schema definitions (move to `schemas/`)
   - Long "Error Handling" sections with many scenarios
   - Full "Finding Schema" or "Output Schema" definitions
   - Complete "Report Structure" templates (>50 lines)
   - "Integration Points" with extensive CI/CD details

2. **PRESERVE** (distill to essence):
   - Frontmatter (argument-hint, description, allowed-tools, model)
   - Core workflow phases (as concise overview)
   - Key anti-patterns and good patterns
   - Mode/argument variations (in Modes table)
   - Agent delegation summary (in table format)
   - Error recovery quick reference (in table format)

3. **CREATE SUPPORTING FILES** (if content exceeds limits):
   - `docs/workflow-phases.md` - Detailed phase-by-phase documentation
   - `docs/delegation-patterns.md` - Exact Task() call syntax with prompts
   - `docs/error-handling.md` - Complete error scenarios and recovery
   - `docs/{domain}.md` - Domain-specific details (e.g., ci-integration.md)
   - `examples/usage-examples.md` - Full workflow examples with expected output
   - `schemas/{command}.schema.json` - Output/finding schemas

4. **TARGET SIZE**: Main command file ~100-200 lines (not 500+)

5. **DOCUMENTATION DEDUPLICATION**:
   - If content is referenced by ONLY this command → MOVE to command's `docs/`
   - If content is used by MULTIPLE commands → KEEP in shared location, REFERENCE via link
   - If content is generic (frameworks, patterns) → LINK to `.claude/docs/01-guides/`

---

### Quality Check After Conversion

- [ ] Main file <200 lines
- [ ] Description <200 chars with trigger keywords
- [ ] Frontmatter uses ONLY valid fields (argument-hint, description, allowed-tools, model)
- [ ] Core Behavior captures essence in ~30 lines
- [ ] Modes table covers all argument variations
- [ ] Workflow Overview is concise (10-20 lines total)
- [ ] Agent Delegation table is complete
- [ ] Error Recovery is quick-reference format (table)
- [ ] Verbose content moved to `docs/` subdirectory
- [ ] All `docs/` files have README.md
- [ ] Schema files exist if command has structured output

---

### Reference Implementation

See `.claude/commands/git/git.md` as the reference implementation:
- ~200 lines main file
- Clear structure with modes table
- Concise workflow overview
- Agent delegation table
- Links to detailed docs in subdirectory

---

## Execute Conversion

1. Read the source command file completely
2. Identify which sections exceed target size
3. Extract essential elements per the structure above
4. Create streamlined main command file
5. Move verbose content to appropriate `docs/` files
6. Create `examples/` with usage scenarios
7. Create `schemas/` if command has structured output
8. Validate against the quality checklist
9. Report what was created and what was moved

---

## Post-Conversion Cleanup

After conversion is complete:
1. **DELETE** the original flat file (`.claude/commands/{command}.md`)
2. **VERIFY** all internal links work
3. **TEST** command still functions correctly
4. **UPDATE** any references to old path in other files
