---
name: slash-command-management
description: >
  Slash command creation and management for Claude Code. Use when creating new
  commands, updating command behavior, or managing the command registry.
  Trigger keywords: slash command, create command, /command, command registry.
---

# Slash Command Management Skill

*Create, validate, and maintain Claude Code slash commands with proper integration*

## Quick Start

| Task | Action |
|------|--------|
| Create new command | Parse requirements -> Design frontmatter -> Build command body -> Validate |
| Update existing command | Read current -> Identify changes -> Apply with validation |
| Registry operations | Discover commands -> Update registry -> Verify consistency |

---

## Command File Structure

### Location
All slash commands live in `.claude/commands/`:
```
.claude/commands/
├── spec.md           # Specification generation
├── plan.md           # Planning from specs
├── tasks.md          # Task generation from plans
├── implement.md      # Task execution orchestration
├── review.md         # Multi-agent code review
├── git.md            # Git workflow operations
├── create-agent.md   # Agent creation workflow
├── analyze-agent.md  # Agent analysis
└── [custom].md       # Custom commands
```

### Naming Convention
- **Format**: `kebab-case.md`
- **Length**: 2-25 characters
- **Characters**: lowercase letters, numbers, hyphens only
- **Examples**: `git.md`, `create-agent.md`, `analyze-claude-md.md`

---

## Command Frontmatter Format

### Required Fields

```yaml
---
argument-hint: '<positional> [optional] [--flag=value]'
description: 'Single sentence describing purpose, use cases, and anti-use cases.'
allowed-tools: [Task, Read, Glob, Bash(pattern:*)]
model: opus
---
```

### Field Specifications

| Field | Required | Description |
|-------|----------|-------------|
| `argument-hint` | Yes | Shows usage pattern in command help |
| `description` | Yes | Concise purpose + when to use/not use |
| `allowed-tools` | Yes | List of permitted tool invocations |
| `model` | No | Model selection (opus, sonnet, haiku) |

### Argument Hint Syntax

```
<required>     - Required positional argument
[optional]     - Optional positional argument
--flag         - Boolean flag
--flag=value   - Flag with value
--flag=a|b|c   - Flag with enumerated values
```

**Examples**:
```yaml
# Simple
argument-hint: '<feature description>'

# Complex
argument-hint: '[spec-file-path] [--phase=N]'

# Full featured
argument-hint: '<source> [--focus=security|performance|quality|all] [--mode=quick|comprehensive]'
```


### Tool Permissions

**Standard Patterns**:
```yaml
# Read-only command
allowed-tools: [Read, Glob, Grep]

# Delegation-focused command (RECOMMENDED)
allowed-tools: [Task, Read, Glob, Bash(git:*)]

# Implementation command
allowed-tools: [Task, Read, Write, Edit, Glob, Grep, Bash(uv:*)]

# Research command
allowed-tools: [Task, Read, Glob, mcp__context7__*, mcp__perplexity__*]
```

**Bash Restrictions**:
```yaml
# Pattern: Bash(prefix:*)
Bash(git:*)      # Only git commands
Bash(uv:*)       # Only uv commands
Bash(kubectl:*)  # Only kubectl commands
Bash(ls:*)       # Only ls commands
```

---

## Command Body Structure

### Standard Sections

```markdown
# Command Name

*One-line tagline describing the command*

---

## Core Behavior

YOU ARE A [ROLE] ORCHESTRATOR.

### How to Start
Parse $ARGUMENTS -> [Step 2] -> [Step N] -> Output

### The Flow
User: /command <args> -> [Phase 1] -> [Phase 2] -> Result

### Anti-Patterns (NEVER DO)
- [Action to avoid]
- [Another action to avoid]

### Good Patterns (ALWAYS DO)
- [Required behavior]
- [Another required behavior]

---

## Modes

| User Says | Mode | Action |
|-----------|------|--------|
| `/command <arg>` | Default | [Default behavior] |
| `--flag` | Flag Mode | [Flag-specific behavior] |

---

## Workflow Overview

[ASCII diagram or structured flow]

---

## Agent Delegation

| Phase | Agent | Operation |
|-------|-------|-----------|
| 1 | [agent-name] | [what it does] |
| 2 | [agent-name] | [what it does] |

---

## Error Recovery

| Error Type | Recovery |
|------------|----------|
| [Error case] | [Recovery action] |

---

## Output Format

### On Success
[Expected output format]

### On Failure
[Expected failure format]

---

## Knowledge Base

- [Link to detailed docs]
- [Link to examples]
- [Link to schemas]

---

## Orchestrator Integration

**Trigger Keywords**: [keywords that invoke this command]
**Integration Points**: [upstream/downstream connections]
```


---

## Command Creation Workflow

### OODA-Aligned Process

```
OBSERVE: Parse requirements, check existing commands
    |
ORIENT: Research patterns via Context7, assess complexity
    |
DECIDE: Select template, plan command structure
    |
ACT: Create command file, validate, update registry
```

### Phase 1: OBSERVE (Analysis)
1. Parse command requirements from user request
2. Check for existing similar commands in `.claude/commands/`
3. Identify tool permissions needed
4. Assess complexity (simple/moderate/complex)

### Phase 2: ORIENT (Research)
1. Research Claude Code command patterns via Context7
2. Review similar command implementations
3. Calculate CQ (Context Quality) score
4. Gate: CQ >= 0.85 before proceeding

### Phase 3: DECIDE (Planning)
1. Select appropriate template (minimal/standard/comprehensive)
2. Define frontmatter fields
3. Plan command body sections
4. Identify knowledge base requirements

### Phase 4: ACT (Execute + Validate)
1. Create command file with proper structure
2. Run 7-stage validation pipeline
3. Update command registry (if applicable)
4. Verify Claude Code compliance

---

## Validation Protocol

### 7-Stage Pipeline

| Stage | Check | Action on Failure |
|-------|-------|-------------------|
| 1. DRY-RUN | Simulate creation | Report issues |
| 2. SMOKE | Frontmatter syntax | Auto-fix YAML |
| 3. AUTO-FIX | Common patterns | Apply known fixes |
| 4. VALIDATE | Schema compliance | Report violations |
| 5. APPLY | Write file | Retry once |
| 6. CHECK | Read-back verify | Report mismatch |
| 7. FINAL | Integration test | Manual review |

### Frontmatter Validation

```python
def validate_frontmatter(content: str) -> ValidationResult:
    """Validate command frontmatter structure."""
    required_fields = ['argument-hint', 'description', 'allowed-tools']
    optional_fields = ['model']
    
    # Check YAML syntax
    # Verify required fields present
    # Validate tool permission patterns
    # Return ValidationResult
```

### Common Validation Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `missing_argument_hint` | No argument-hint field | Add argument-hint to frontmatter |
| `invalid_tool_pattern` | Bash without prefix | Use `Bash(prefix:*)` pattern |
| `description_too_long` | >200 characters | Shorten to single sentence |
| `invalid_model` | Unknown model value | Use opus, sonnet, or haiku |


---

## Command Registry Management

### Registry Location
Command registry tracks all available commands:
- **Primary**: `.claude/docs/03-workflows/workflow-registry.md`
- **Discovery**: Glob `.claude/commands/*.md`

### Registry Update Protocol

1. **Discover**: Scan `.claude/commands/` for all `.md` files
2. **Parse**: Extract frontmatter from each command
3. **Compare**: Check against current registry entries
4. **Update**: Add new, update changed, deprecate removed
5. **Validate**: Verify registry consistency

### Registry Entry Structure

```yaml
command_name:
  version: "1.0"
  status: GA | Beta | Alpha | Deprecated
  description: "Command purpose"
  trigger_keywords: ["keyword1", "keyword2"]
  integration_points:
    upstream: ["/spec", "/plan"]
    downstream: ["/implement", "/git"]
  maturity_metrics:
    reliability: 95%
    documentation: complete
```

---

## Best Practices

### Command Design Principles

1. **Single Responsibility**: Each command does ONE thing well
2. **Delegation First**: Orchestrate sub-agents, never execute directly
3. **Explicit Modes**: Clear mode detection via argument patterns
4. **Graceful Degradation**: Handle missing dependencies gracefully
5. **Progress Visibility**: Report status during long operations

### Naming Guidelines

| Pattern | Example | Use For |
|---------|---------|---------|
| `verb.md` | `review.md` | Action commands |
| `verb-noun.md` | `create-agent.md` | Specific actions |
| `analyze-*.md` | `analyze-agent.md` | Analysis commands |

### Documentation Requirements

Every command MUST have:
- [ ] Clear description in frontmatter
- [ ] Anti-patterns section (NEVER DO)
- [ ] Good patterns section (ALWAYS DO)
- [ ] Error recovery table
- [ ] Output format examples
- [ ] Orchestrator integration notes

---

## Skill-Command Integration

### When to Use Skill vs Command

| Use Case | Artifact | Reason |
|----------|----------|--------|
| User-invokable action | Command | Direct `/command` invocation |
| Agent capability | Skill | Referenced by agent prompts |
| Reusable pattern | Skill | Shared across multiple agents |
| Workflow entry point | Command | Clear user interface |

### Command Invoking Skills

Commands can reference skills for specialized behavior:

```markdown
# /git Command

This command invokes the **git-workflow** skill.

## Usage
Invoke the `git-workflow` skill and follow its instructions.

## Skill Reference
See `.claude/skills/git-workflow/SKILL.md` for complete documentation.
```


---

## Error Recovery

| Error Type | Detection | Recovery |
|------------|-----------|----------|
| Invalid frontmatter | YAML parse error | Show syntax, request fix |
| Missing required field | Schema validation | Add field with default |
| Invalid tool pattern | Pattern matching | Suggest correct syntax |
| Duplicate command | Name collision | Rename or merge |
| Orphaned command | Registry sync | Add to registry or remove |

---

## Anti-Patterns (NEVER DO)

- Create commands without frontmatter validation
- Use bare `Bash` without prefix restriction
- Skip the description field
- Create commands that duplicate existing functionality
- Write commands that execute code directly (always delegate)
- Ignore the registry update step

## Good Patterns (ALWAYS DO)

- Research via Context7 before designing new commands
- Use DRY-RUN mode for first-time command creation
- Read-back verify after file modifications
- Update registry after command changes
- Include error recovery patterns
- Document orchestrator integration points

---

## References

| Resource | Purpose |
|----------|---------|
| [Command Template](references/command-template.md) | Template for new commands |
| [Registry Format](references/registry-format.md) | Command registry structure |
| [Workflow Operations](../../agents/claude-code/workflow/docs/workflow-operations.md) | Operation definitions |

---

## Thinking Frameworks

**Most Relevant for Command Management**:

| Framework | When to Use |
|-----------|-------------|
| CAGEERF | Complex command design (Context->Analysis->Goals->Execute->Evaluate->Refine) |
| Pre-Mortem | Identifying command failure modes before deployment |
| ReACT | Debugging command issues (Reason->Act->Observe->Refine) |

**Full Catalog**: `.claude/docs/00-core/frameworks/README.md`
