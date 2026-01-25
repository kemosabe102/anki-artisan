---
argument-hint: '<command-name> [--type=thin|workflow|domain|review] [--template] [--validate <path>] [--resume] [--force]'
description: 'Guided wizard for creating high-quality slash commands. Validates against quality standards and generates skeleton with all required sections.'
allowed-tools: [Task, Read, Write, Glob, Grep, TodoWrite, AskUserQuestion]
model: opus
---

# Create Command

*Wizard-style guided creation of high-quality slash commands with quality validation*

---

## Core Behavior

YOU ARE A COMMAND CREATION WIZARD executing 6-phase structured command generation.

**Mission**: Guide users through creating well-structured slash commands that meet quality standards, validate against the quality rubric, and integrate into the Claude Code ecosystem.

**Philosophy**: Quality commands delegate work, never execute directly. Every command needs clear phases, gates, and error handling.

### How to Start
Parse $ARGUMENTS -> Determine mode (wizard|typed|template|validate) -> Execute appropriate workflow

### The Flow
```
User: /create-command my-command           -> Wizard mode (interactive)
User: /create-command my-cmd --type=thin  -> Typed mode (skip type selection)
User: /create-command --template          -> Output blank template only
User: /create-command --validate path.md  -> Score existing command
```

### Anti-Patterns (NEVER DO)
- Generate command without quality validation
- Skip requirements gathering (leads to incomplete commands)
- Create commands that execute work directly
- Use wrong archetype for use case

### Good Patterns (ALWAYS DO)
- Validate command name uniqueness before generation
- Ask clarifying questions via AskUserQuestion before generating
- Score against quality rubric (command-quality-standards.md)
- Provide actionable next steps
- Suggest /analyze-command for post-creation validation

---

## Modes

| User Says | Mode | Action |
|-----------|------|--------|
| `/create-command my-command` | wizard | Interactive guided creation |
| `/create-command my-command --type=thin` | typed | Create with specific archetype |
| `/create-command --template` | template | Output blank template only |
| `/create-command --validate path/cmd.md` | validate | Score existing command against standards |

---

## Workflow (6 Phases)

```text
/create-command <name> [flags]
|
+-- P0: ARGUMENT PARSING
|   +-- Parse command name from $ARGUMENTS
|   +-- Parse flags: --type, --template, --validate
|   +-- Validate name (kebab-case, no collisions)
|   +-- [GATE 0: ARGS] Name valid, no collision
|
+-- P1: TYPE SELECTION (if not provided)
|   +-- IF --validate: Skip to P5
|   +-- IF --template: Skip to P4 (blank template)
|   +-- IF --type provided: Use specified archetype
|   +-- ELSE: AskUserQuestion for archetype selection
|   +-- [GATE 1: TYPE] Archetype selected
|
+-- P2: REQUIREMENTS GATHERING
|   +-- Based on archetype, ask structured questions
|   +-- Capture: description, argument-hint, allowed-tools
|   +-- Capture: archetype-specific requirements
|   +-- [GATE 2: REQUIREMENTS] 7+ requirements captured
|
+-- P3: SKELETON GENERATION
|   +-- Select template based on archetype
|   +-- Populate all 14 sections with gathered data
|   +-- Generate error codes ({COMMAND}_ERR_001-005)
|   +-- [GATE 3: SKELETON] All sections present
|
+-- P4: QUALITY VALIDATION
|   +-- Score against command-quality-standards.md rubric
|   +-- Calculate: Structure, Workflow, Delegation, Errors, Docs, Anti-Patterns
|   +-- Report score breakdown and gaps
|   +-- [GATE 4: QUALITY] Score >= 60/100 (hard minimum) - use --force flag to bypass
|
+-- P5: OUTPUT
    +-- Write command to .claude/commands/{name}.md
    +-- Display summary with quality score
    +-- Provide next steps
    +-- [GATE 5: COMPLETE] File written successfully
```

---

## Phase Details

### P0: ARGUMENT PARSING
- **Purpose**: Fail-fast on invalid inputs
- **Framework**: Cynefin (classify complexity)
- **Agent**: (orchestrator)
- **Operations**:
  - Parse command name from $ARGUMENTS (first positional)
  - Extract flags: `--type`, `--template`, `--validate`, `--resume`, `--force`
  - Validate command name format (kebab-case, 3-50 chars)
  - Check for collisions via `Glob(".claude/commands/*.md")`
  - Check for existing checkpoint via `Glob("temp/create-command/{name}.checkpoint.json")`
  - IF checkpoint exists AND no --resume: Prompt user to continue or restart
  - IF --resume AND checkpoint exists: Load checkpoint, skip to P3
  - IF --resume AND no checkpoint: Error CREATE_CMD_010
- **Gate**: Name valid AND no existing command with same name
- **Timeout**: 10s

### P1: TYPE SELECTION
- **Purpose**: Determine command archetype for template selection
- **Framework**: Cynefin (domain classification)
- **Agent**: (orchestrator via AskUserQuestion)
- **Operations**:
  - IF `--validate` mode: Skip to P5 (validation only)
  - IF `--template` mode: Skip to P4 (blank template)
  - IF `--type` flag provided: Use specified archetype
  - ELSE: Present 4 archetypes via AskUserQuestion:
    1. **Thin Orchestrator**: Single agent delegation, minimal phases
    2. **Multi-Phase Workflow**: 5+ phases, parallel agents, gates
    3. **Domain Specialist**: External tools, state tracking, domain logic
    4. **Review/Validation**: Sequential reviews, checkpoints, gate criteria
- **Gate**: Archetype selected (1 of 4)
- **Timeout**: User-dependent (interactive)

### P2: REQUIREMENTS GATHERING (Interactive)
- **Purpose**: Collect all information needed for skeleton generation
- **Framework**: 5W1H (structured questioning)
- **Agent**: (orchestrator via AskUserQuestion)
- **Operations**: Ask questions based on archetype:

**All Types** (required):
- What does this command do? (-> description, max 120 chars)
- What arguments does it accept? (-> argument-hint)
- Which tools does it need? (-> allowed-tools selection)

**Thin Orchestrator** (additional):
- Which agent does it delegate to?
- What input validation is needed?
- What output format?

**Multi-Phase Workflow** (additional):
- How many phases? (suggest 3-7)
- What agents are involved per phase?
- Which phases can run in parallel?
- What gates exist between phases?

**Domain Specialist** (additional):
- What external tools/services are used?
- What state needs to be tracked?
- What domain-specific validation?

**Review/Validation** (additional):
- What is being reviewed?
- What are the gate criteria (PASS/FAIL)?
- Does it need checkpoint support?

- Write checkpoint to `temp/create-command/{name}.checkpoint.json` (atomic)
- **Gate**: 7+ requirements captured
- **Timeout**: User-dependent (interactive)

### P3: SKELETON GENERATION
- **Purpose**: Generate complete command file from template + requirements
- **Framework**: CAGEERF (structured generation)
- **Agent**: (orchestrator)
- **Operations**:
  1. Select template based on archetype
  2. Populate frontmatter (all 4 required fields)
  3. Generate Identity/Role section
  4. Create Modes table from requirements
  5. Build Workflow diagram with phases and gates
  6. Create Agent Delegation matrix with Task() examples
  7. Generate error codes: `{COMMAND}_ERR_001` through `{COMMAND}_ERR_005` minimum
  8. Create Output templates (success/failure)
  9. Add Anti-patterns section (archetype-specific)
  10. Add Good patterns section (archetype-specific)
  11. Add Knowledge Base with placeholders
- **Gate**: All 14 required sections present
- **Timeout**: 30s

### P4: QUALITY VALIDATION
- **Purpose**: Score against quality rubric before output
- **Framework**: DMAIC (measure, analyze)
- **Agent**: (orchestrator)
- **Operations**:
  1. Score Structure Completeness (20 pts)
  2. Score Workflow Clarity (20 pts)
  3. Score Delegation Correctness (20 pts)
  4. Score Error Handling Coverage (15 pts)
  5. Score Documentation Completeness (15 pts)
  6. Score Anti-Pattern Avoidance (10 pts)
  7. Calculate total (0-100)
  8. Report category breakdown and specific gaps
- **Gate**: Score >= 60/100 (hard minimum) - use --force flag to bypass
- **Timeout**: 15s

### P5: OUTPUT
- **Purpose**: Write command file and provide summary
- **Framework**: Progressive Disclosure
- **Agent**: (orchestrator)
- **Operations**:
  1. IF `--validate` mode: Output validation report only (no file write)
  2. IF `--template` mode: Output blank template to console only
  3. ELSE: Write command to `.claude/commands/{command-name}.md`
  4. Display summary: quality score, sections created, gaps
  5. Provide next steps: fill TODOs, create agents if needed
  6. Suggest `/analyze-command` for post-creation validation
  7. Delete checkpoint file on success
- **Gate**: File written successfully (or report displayed for validate/template modes)
- **Timeout**: 10s

---

## Agent Delegation Matrix

| Phase | Agent | Purpose | Timeout |
|-------|-------|---------|---------|
| P0 | orchestrator | Parse arguments, validate name | 10s |
| P1 | orchestrator (AskUserQuestion) | Type selection | interactive |
| P2 | orchestrator (AskUserQuestion) | Requirements gathering | interactive |
| P3 | orchestrator | Skeleton generation | 30s |
| P4 | orchestrator | Quality scoring | 15s |
| P5 | orchestrator | File output | 10s |

**Note**: This command is a thin orchestrator that uses AskUserQuestion for interactivity rather than delegating to sub-agents. The complexity lies in the structured generation, not multi-agent coordination.

### Delegation Syntax Reference (for commands that delegate)

**Standard Pattern** (from analyze-command.md):
```
Task(agent-architect,
  "Validate command structure at {path}.
   Check: frontmatter compliance, schema adherence, section organization.
   Output: structure_score (0-100), schema_violations[], recommendations[]
   BOUNDARIES: Do NOT modify files. Do NOT evaluate prompt quality.")
```

**With Timeout** (for long-running tasks):
```
Task(strategy-builder, 
  prompt="MODE: validate\nAlgorithm: {algo}\nCheck: param_count < 10", 
  timeout_ms=60000)
```

**Key Elements**:
- `BOUNDARIES:` - Prevent agent scope creep
- `MODE:` - Specify sub-task for multi-mode agents  
- `Output:` - Explicit return schema
- `timeout_ms` - 30s (git) to 600s (backtest)

---

## Validation Mode (--validate)

When validating an existing command:

```text
/create-command --validate .claude/commands/my-command.md
|
+-- Read command file
+-- Parse all sections
+-- Score against 6-category rubric
+-- Output detailed report
```

**Validation Output**:
- Overall score (0-100)
- Category breakdown with point values
- Specific gaps identified
- Prioritized recommendations

---

## Checkpoint Support

For long wizard sessions, state is saved after P2 (requirements gathering).

**Checkpoint Location**: `temp/create-command/{command-name}.checkpoint.json`

**Schema**:
```json
{
  "schema_version": "1.0",
  "checksum": "sha256:...",
  "command_name": "my-command",
  "archetype": "multi-phase",
  "phase": 2,
  "requirements": {
    "description": "...",
    "argument_hint": "...",
    "allowed_tools": [...],
    "archetype_specific": {...}
  },
  "timestamp": "2026-01-04T12:00:00Z"
}
```

**Resume Behavior**:
- `--resume` + checkpoint exists -> Load state, continue from P3
- `--resume` + no checkpoint -> Error CREATE_CMD_010
- No flags + checkpoint exists -> Prompt user (continue/restart)
- Checkpoint deleted on successful P5 completion

**Atomic Write Pattern**:
1. Serialize to JSON
2. Write to `.tmp` file
3. Validate JSON parseable
4. Atomic rename to final path

---

## Templates (by Archetype)

### Thin Orchestrator Template
- **Phases**: 3 (Parse -> Delegate -> Return)
- **Agents**: 1 (single delegation target)
- **Workflow**: Simple linear flow
- **Gates**: 2 (INPUT_GATE, OUTPUT_GATE)
- **Model**: sonnet

### Multi-Phase Workflow Template
- **Phases**: 5-7 (P0-P6 with complex flow)
- **Agents**: 3-5 (parallel where possible)
- **Workflow**: Full diagram with branches
- **Gates**: Per-phase exit criteria
- **Model**: opus

### Domain Specialist Template
- **Phases**: 4-8 (domain-specific stages)
- **Agents**: 2-4 (specialized agents)
- **Workflow**: State tracking, external tools
- **Gates**: Domain validation criteria
- **Model**: opus

### Review/Validation Template
- **Phases**: 5-7 (Detect -> Loop -> Synthesize -> Gate)
- **Agents**: 2-3 (reviewers, synthesizer)
- **Workflow**: Sequential with checkpoints
- **Gates**: Severity-based criteria
- **Model**: opus

---

## Error Codes

| Code | Phase | Description | Recovery |
|------|-------|-------------|----------|
| CREATE_CMD_001 | P0 | Invalid command name format | Show naming rules: kebab-case, 3-50 chars, alphanumeric + hyphens |
| CREATE_CMD_002 | P0 | Command name collision | Suggest alternative: `{name}-v2`, `{name}-enhanced`, or different name |
| CREATE_CMD_003 | P1 | Type selection failed | Show 4 archetype options with descriptions |
| CREATE_CMD_004 | P2 | Requirements incomplete | List missing requirements, re-prompt for specific items |
| CREATE_CMD_005 | P4 | Quality score below threshold | Show gaps to fix, offer to proceed with acknowledgment |
| CREATE_CMD_006 | P5 | File write failed | Check permissions, verify path, retry once |
| CREATE_CMD_007 | P5 (validate) | Command file not found | Show available commands via Glob |
| CREATE_CMD_008 | P5 (validate) | Command file parse error | Show parsing issue, suggest manual review |
| CREATE_CMD_009 | P4 | Quality score below 60 (hard minimum) | Fix gaps or use --force flag |
| CREATE_CMD_010 | P0 | --resume flag but no checkpoint found | Start fresh without --resume |
| CREATE_CMD_011 | P0 | Checkpoint corrupted (checksum mismatch) | Delete checkpoint, start fresh |

---

## Output Format

### Success (Wizard/Typed Mode)
```text
Command Created: /my-command
Quality Score: 82/100

Sections Generated:
[x] Frontmatter (4/4 fields)
[x] Identity/Role
[x] Modes table
[x] Workflow (5 phases, 4 gates)
[x] Agent Delegation (2 agents)
[x] Error codes (5 defined)
[x] Output templates
[x] Anti-patterns
[x] Knowledge Base

Location: .claude/commands/my-command.md

Next Steps:
1. Review generated content for accuracy
2. Fill in [TODO] placeholders with specific details
3. Create referenced agents (if any are new)
4. Test with /analyze-command my-command
```

### Success (Template Mode)
```text
Blank Command Template (Multi-Phase Workflow)
==============================================
Copy the template below and customize for your use case.

---
argument-hint: '<required-arg> [optional-arg] [--flag]'
description: 'Single sentence describing what command does.'
allowed-tools: [Task, Read, Glob, Grep]
model: opus
---

# Command Name

*One-line description*

...
[Full template output]
```

### Success (Validate Mode)
```text
Command Validation: /existing-command
Overall Score: 65/100 (Below threshold)

Category Breakdown:
- Structure:       18/20 (missing Knowledge Base)
- Workflow:        15/20 (gates unclear)
- Delegation:      12/20 (no Task() examples)
- Error Handling:  10/15 (only 3 error codes)
- Documentation:    5/15 (sparse descriptions)
- Anti-Patterns:    5/10 (direct execution detected)

Recommendations:
1. Add Knowledge Base section with skill/schema links
2. Add gate criteria to workflow phases
3. Add Task() invocation examples to delegation section
4. Define 5+ error codes with recovery paths
5. Refactor to delegate instead of direct execution
```

### Failure
```text
Command Creation Failed

Error: CREATE_CMD_002
Phase: P0 - ARGUMENT PARSING
Description: Command name collision detected

Details:
  Requested: my-command
  Existing:  .claude/commands/my-command.md

Recovery Options:
1. Use different name: /create-command my-command-v2
2. Use --validate to check existing: /create-command --validate .claude/commands/my-command.md
3. Delete existing command first (manual)
```

---

## Anti-Patterns (NEVER DO)

### Generation Anti-Patterns
- **Skip requirements gathering** - Leads to incomplete, low-quality commands
- **Generate without quality validation** - Outputs substandard commands
- **Create commands that execute directly** - Violates orchestrator pattern
- **Use wrong archetype** - Thin orchestrator for complex workflow = bad design
- **Skip P0 validation** - Invalid names cause downstream issues

### Template Anti-Patterns
- **Missing frontmatter fields** - Commands won't load properly
- **Phases without gates** - No quality control between phases
- **Task() without BOUNDARIES** - Agents may exceed scope
- **Error codes without recovery** - Users stuck on failures

---

## Good Patterns (ALWAYS DO)

### Process Patterns
- **Validate command name uniqueness** - Check via Glob before generation
- **Ask clarifying questions** - Use AskUserQuestion to gather requirements
- **Score against quality rubric** - Always validate before output
- **Provide actionable next steps** - Guide user on what to do after creation
- **Suggest post-creation validation** - Recommend /analyze-command

### Template Patterns
- **Include all 4 frontmatter fields** - argument-hint, description, allowed-tools, model
- **Add gates after every phase** - Enforce quality control
- **Provide Task() examples** - Show exact delegation syntax
- **Define 5+ error codes** - Cover input, execution, validation errors
- **Include BOUNDARIES in all Task()** - Explicit scope limitations

### Quality Patterns
- **Structure Completeness first** - All sections before content quality
- **Generate archetype-appropriate templates** - Match complexity to use case
- **Include Anti-Patterns section** - Prevent common mistakes
- **Link to Knowledge Base** - Reference standards and related docs

---

## Quality Scoring Rubric

Apply the 6-category quality rubric when validating (P4 or --validate mode).

**See**: `.claude/docs/01-guides/claude-code/commands/command-quality-standards.md` Section 7

**Grade Thresholds**:
| Score | Grade | Action |
|-------|-------|--------|
| 90-100 | A | Exemplary |
| 80-89 | B | High quality |
| 70-79 | C | Acceptable |
| 60-69 | D | Below standard, requires --force |
| <60 | F | Rejected, fix required |

---

## Knowledge Base

**Primary Reference**:
- `.claude/docs/01-guides/claude-code/commands/command-quality-standards.md` - Quality standards and scoring rubric

**Related Commands**:
- `/analyze-command` - Post-creation command analysis and validation
- `/create-agent` - Agent creation wizard (similar pattern)

**Related Agents**:
- `agent-architect` - Agent/command structure validation
- `workflow-analyzer` - Workflow flow analysis
- `doc-librarian` - Documentation generation

**Templates & Examples**:
- `.claude/commands/tasks.md` - Thin orchestrator example
- `.claude/commands/analyze-command.md` - Multi-phase workflow example
- `.claude/commands/backtest.md` - Domain specialist example
- `.claude/commands/integration-review.md` - Review/validation example

---

## Orchestrator Integration

**Trigger Keywords**: create command, new command, build command, slash command, command wizard

**Delegation Pattern**:
```
User: "Create a new slash command for code formatting"
Orchestrator (OBSERVE): Parse request -> Identify /create-command trigger
Orchestrator (ORIENT): Command creation intent clear
Orchestrator (DECIDE): ASC = 0.92 -> Delegate to /create-command
Orchestrator (ACT): SlashCommand(command="/create-command code-formatter")
```

**Integration Points**:
- Upstream: User requirements, existing command patterns
- Downstream: `.claude/commands/{name}.md`, `/analyze-command` validation

---

## Boundaries

**IN SCOPE**:
- Create new command files in `.claude/commands/`
- Validate existing commands (--validate mode)
- Output blank templates (--template mode)

**OUT OF SCOPE**:
- Modify existing commands (use agent-architect directly)
- Modify quality standards document
- Create agents (use /create-agent)
- Execute the created command

---

**Version**: 1.0
**Dependencies**: command-quality-standards.md
