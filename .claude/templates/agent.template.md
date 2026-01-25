# Agent Template

> **⚠️ CRITICAL - REMOVE THIS HEADER WHEN CREATING ACTUAL AGENTS ⚠️**
>
> **Lines 1-9 (this entire header section) MUST BE DELETED when creating actual agent files.**
> **Agent files MUST start directly with the YAML frontmatter (`---` block).**
> **The "## Agent Definition Header" section marker must also be removed.**
>
> **Correct agent file structure:**
>
> ```
> ---
> name: agent-name
> description: ...
> model: ...
> color: ...
> tools: ...
> ---
>
> # Role & Boundaries
> ...
> ```

**Template Version:** 6.0 - Claude Code v2.0 Compliance Edition
**Target Token Count:** <15K tokens (optimized for Claude Code file operations)
**Last Updated:** 2025-11-21
**Incorporates:** Claude Code v2.0 frontmatter spec, cd command ban enforcement, Anthropic Multi-Agent Research System learnings

---

---

## Agent Definition Header

```yaml
---
name: agent-name # Use descriptive, groupable names (e.g., researcher-lead, researcher-external)
description: 'Brief description of agent purpose and capabilities - 1-2 sentences max, MUST be single-quoted string on ONE line'
model: opus # opus (recommended)|sonnet|haiku|inherit - opus for most agents
color: purple|blue|green|yellow|red # Visual identifier
tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch # Comma-separated string, NOT YAML list
permissionMode: default # default|acceptEdits|bypassPermissions|plan|ignore
skills: skill1, skill2  # Optional: Skills auto-loaded into agent context on start
---
```

**CRITICAL**: Both `tools` and `skills` must be comma-separated strings for Claude Code sub-agent compatibility.
**NOTE**: `permissionMode` values: `default` (standard permission checks), `acceptEdits` (auto-accept file edits), `bypassPermissions` (skip all checks - use with caution), `plan` (read-only mode), `ignore` (disabled agent).

> **Skills Field**
>
> Skills are **auto-loaded** into the subagent's context when it starts (not just available - actively injected).
> Use this to give agents domain-specific knowledge without bloating their prompt.
>
> **Project Skills** (from `.claude/skills/`):
> - `debugging-methodology` - 8-step debugging, 5 Whys, SCAMPER
> - `code-review-standards` - Blast radius, severity classification
> - `analyzing-code-complexity` - Cyclomatic complexity, detection patterns
> - `test-driven-development` - TDD workflow, test patterns
> - `python-implementation` - Python coding standards
> - See full list: `.claude/skills/` directory
>
> **Plugin Skills** (from MCP plugins):
> - `example-skills:docx` - Document creation/editing
> - `example-skills:pdf` - PDF handling
> - `example-skills:xlsx` - Excel file handling
>
> **Best Practice**: Load 1-3 skills max to avoid context bloat. Choose skills that provide domain knowledge the agent needs frequently.

> ⚠️ **CRITICAL: Description Field YAML Syntax**
>
> Claude Code does NOT parse YAML multi-line syntax (`|` pipe or `>` folded). Using these causes descriptions to load as ~11 tokens instead of full content.
>
> **❌ BROKEN**: `description: |` or `description: >` (multi-line)
> **✅ CORRECT**: `description: 'Single line, escape quotes with double single-quotes like it''s this'`

# Role & Boundaries

**[Agent Type] Scope**: [Define specific micro-scope and boundaries - what this agent does and does NOT do]

**Core Function**: [Single sentence describing primary responsibility]

**Capabilities**: [Bulleted list of what the agent can do]

**Artifacts**: [What outputs/artifacts the agent produces]

**Boundaries**: [What the agent should NOT do]

## Schema Reference

**Input/Output Contract**: `.claude/docs/shared/schemas/[agent-name].schema.json`

- **Extends**: `base-agent.schema.json` (two-state SUCCESS/FAILURE model)
- **Validation**: All outputs must validate against agent-specific schema
- **State Model**: Returns either SUCCESS with evidence or FAILURE with recovery guidance

## OODA Phase Structure (Recommended for Complex Agents)

**When to use phases/**: Agent has distinct OBSERVE → ORIENT → DECIDE → ACT workflows with different delegation patterns per phase.

**Hybrid Model**: Core identity stays in agent.md, phase-specific workflows in phases/ directory.

### Directory Structure with Phases

```
{{agent-name}}/
├── {{agent-name}}.md      # Core: identity, tools, boundaries (<150 lines)
├── phases/                 # Phase-specific workflows
│   ├── phase-1-observe.md  # Context gathering, pre-flight
│   ├── phase-2-orient.md   # Analysis, pattern matching
│   ├── phase-3-decide.md   # Planning, risk assessment
│   └── phase-4-act.md      # Execution, validation
├── docs/                   # Domain knowledge
├── examples/               # Usage patterns
└── schemas/                # Validation contracts
```

### What Stays in agent.md (Core)

- YAML frontmatter (name, description, tools, model, color)
- Core Behavior section (identity, tone, anti-patterns, good patterns)
- Role & Boundaries table
- Quality Standards
- Knowledge Base references
- Error Recovery patterns
- Technical Details

### What Goes in phases/ (Workflows)

- Detailed workflow steps with numbered sub-steps
- Agent delegation tables per phase
- Phase-specific checklists
- Exit criteria with CQ weights
- Common mistakes per phase

### Description Requirements

Agent descriptions MUST include trigger phrases and boundaries:

```yaml
description: 'Domain specialist for scope/**. Method summary here. Use for: "trigger phrase 1", "trigger phrase 2". NOT for: boundary 1 (use other-agent), boundary 2.'
```

**Example**:
```yaml
description: 'Hypothesis-driven debugging specialist for packages/**, tests/**. Uses 8-step scientific method with evidence-before-edits. Use for: "debug", "failing test", "RCA". NOT for: architectural changes (use architectureer), refactoring (use development).'
```

### Migration

Use `/analyze-agent --migrate {{agent-name}}` to automatically restructure an existing agent into phase-based format.

**Templates**: See `.claude/templates/agent-scaffold/phases/` for phase templates.

## Permissions

**✅ READ ANYWHERE**: [Define read permissions - typically .claude/** or specific directories]

**✅ WRITE WITHOUT APPROVAL**:

- [Specific directories/file patterns where agent can write freely]
- [Document any workflow-specific write permissions]

**❌ FORBIDDEN**:

- [Explicitly list forbidden operations and directories]
- System files or configurations
- Git operations (orchestrator handles commits)

## File Operation Protocol

**Protocol Reference**: `.claude/docs/01-guides/file-ops/file-operation-protocol.md`

### Bash Command Standards (MANDATORY)

**AGENT_NAME Prefix**: ALL Bash commands MUST start with agent name from frontmatter

```bash
# Template pattern ({{agent-name}} is replaced during agent creation)
AGENT_NAME={{agent-name}} <command>

# Example for this agent (name: {{agent-name}})
AGENT_NAME={{agent-name}} uv run pytest tests/
```

**Why Required**:
- Command traceability in multi-agent workflows
- Audit logging and debugging
- Security hook enforcement

**Agent Name Source**: Use exact `name:` value from YAML frontmatter (line 2 of agent file)

**Enforcement**: Security hooks will validate AGENT_NAME presence (implementation pending)

### Banned Commands (Security Enforcement)

**❌ NEVER use cd commands**: `cd`, `pushd`, `popd`
- **Reason**: Claude Code resets working directory between EVERY bash call - cd commands DO NOT PERSIST
- **Instead**: Use absolute paths for ALL file operations
- **Security hooks**: Will BLOCK cd commands automatically (configured in .claude/settings.json)
- **See**: `.claude/docs/01-guides/agents/agent-standards-runtime.md` for complete rationale

**Examples**:
```bash
# ❌ WRONG (cd does not persist)
AGENT_NAME={{agent-name}} cd /path && pytest tests/

# ✅ CORRECT (absolute path)
AGENT_NAME={{agent-name}} pytest /c/Users/kemos/Repos/gauntlet-agents/tests/
```

## Base Agent Pattern Extension (RECOMMENDED)

**This agent EXTENDS**: `.claude/docs/01-guides/agents/base-agent-pattern.md` (OPTIONAL - use for token optimization)

**Specialized Focus**: [Agent's unique capability and domain - what makes this agent different]

**Agent-Specific Capabilities**:

- [Unique capability 1 not covered by base pattern]
- [Unique capability 2 specific to this agent]
- [Unique capability 3 differentiating this agent]

**Inherited from Base Pattern** (when using base pattern extension):

- Knowledge Base Integration (context gathering hierarchy)
- Pre-Flight Checklist (comprehensive task assessment)
- Core Workflow Structure (6-phase lifecycle)
- Error Recovery Patterns (retry logic, graceful degradation)
- Parallel Execution Awareness (when to parallelize/serialize)
- Validation Checklist (lifecycle, core requirements, quality assurance)

**Token Savings**: Using base pattern reduces agent size by ~1,150 tokens through inheritance of common sections

# Reasoning Approach

**Simulation-Driven Development (For Agent Creation):**

- **Think from the agent's perspective** before creation
- Simulate what the agent needs to accomplish its goals
- Consider tool requirements, frameworks, work phases
- Identify potential failure modes and edge cases

**Decision-Making Process:**

- Evaluate multiple approaches before acting
- Consider tool appropriateness and cost implications
- Document rationale for non-obvious decisions
- Maintain internal reasoning separate from external outputs

**Reasoning Style:** [explicit|concise|minimal]

<!-- Future: thinking_budget: [low|medium|high] when Claude Code supports extended thinking -->

**OODA Loop Framework:**

1. **Observe** - What information is available? What tools can be used?
2. **Orient** - What's the best approach given constraints? Update beliefs based on learnings
3. **Decide** - Select specific tools/actions with clear justification
4. **Act** - Execute tools, evaluate results, repeat or conclude

**Output Structure:**

- Structured JSON with confidence scores
- Clear rationale fields for key decisions
- Alternative approaches considered (when applicable)
- Fallback strategies documented

# Knowledge Base Integration

**Always Loaded at Startup:**

- This agent definition
- `CLAUDE.md` for project context
- `.claude/docs/01-guides/agents/agent-standards-runtime.md` (auto-loaded - universal baseline)
- [Domain-specific guides from .claude/docs/01-guides/]

**Required Guide Consultations:**

```markdown
1. [Guide Name] (`.claude/docs/01-guides/path/to/guide.md`)
   - When to consult: [specific scenarios]
   - What to extract: [key information needed]

2. [Another Guide] (`docs/04-guides/domain/guide.md`)
   - When to consult: [specific scenarios]
   - What to extract: [key information needed]
```

**Context Gathering Hierarchy (when uncertain):**

1. Search `.claude/docs/01-guides/` for domain guidance
2. Check `docs/04-guides/` for user documentation
3. Query MCP servers (Context7, etc.)
4. Web search if above insufficient
5. Update/create documentation for knowledge gaps

**MCP Resources**: Context7 docs, WebFetch patterns when available
**Workflow Integration**: `.claude/docs/orchestrator-workflow.md` (coordination patterns)

# Pre-Flight Checklist

**Comprehensive Task Assessment** (mandatory for all operations):

1. **Schema Loading**: Verify agent-specific schema accessibility and validation rules
2. **Task Analysis**: Parse context for operation type, complexity, scope boundaries
3. **Research Planning**: Identify information gaps and research strategy
4. **Todo Creation**: Generate structured task breakdown (when 3+ steps required)
5. **Ambiguity Detection**: Flag unclear requirements, missing context, conflicting constraints
6. **Workflow Selection**: Choose appropriate lifecycle workflow based on task characteristics
7. **Resource Verification**: Confirm tool permissions, file access, external dependencies
8. **Unclear Items Tracking**: Initialize tracking for ambiguous elements throughout process

# Operating Mode: Workflow-Based Execution

**Agent as Class, Workflows as Methods** - Execute structured 6-phase lifecycles:

## Core Workflow Structure

**Analysis → Research → Todo Creation → Implementation → Validation → Reflection**

Each workflow specifies:

- **Input Requirements**: Expected context, dependencies, validation criteria
- **Process Phases**: Detailed step-by-step execution with unclear items handling
- **Output Format**: SUCCESS/FAILURE alignment with base-agent.schema.json
- **Integration Points**: Handoffs to orchestrator and other agents

# Tool Usage Patterns

**Tool Selection Heuristics:**

- Examine all available tools before deciding
- Match tool usage to task intent
- Prefer specialized tools over generic ones
- Consider token costs and response sizes

**Tool Description Quality (When Creating/Documenting Tools):**

- Write as if explaining to new team member
- Make implicit context explicit (query formats, terminology)
- Use unambiguous parameter names (`user_id` vs `user`)
- Disclose destructive changes or open-world access

**Tool Response Optimization:**

- Return high-signal information only
- Prioritize contextual relevance over flexibility
- Use semantic fields (name, type) over technical IDs (uuid, mime_type)
- Implement filtering/pagination for large responses

**Tool Coordination:**

- Use tools in parallel when operations are independent (3+ tools)
- Sequential for dependencies where output feeds next input
- Document tool chain rationale

**Agent-Specific Constraints:**

- **Path Validation**: [Specific path validation rules for this agent]
- **Schema Validation**: [Output schema requirements]
- **Research Tools**: [Which research tools and when to use them]
- **File Operation Protocol**: Mandatory pre-flight assessment for all file operations

# Parallel Execution Awareness

**When to Parallelize:**

- Read operations (Read, Grep, Glob)
- Independent research tasks
- Analysis of different files
- Validation tasks without dependencies

**When NOT to Parallelize:**

- Write operations (Write, Edit, MultiEdit)
- Tasks with tight dependencies
- Operations requiring shared context
- Sequential workflows where output feeds next step

**Implementation Pattern:**

```markdown
For orchestrators: Launch multiple agents in single message with multiple Task calls
For workers: Use multiple tools in parallel when operations are independent
```

# Error Recovery Patterns

**Retry Logic:**

- Retry failed tool calls with exponential backoff
- Maximum 3 retries before escalating
- Log failure patterns for analysis

**Checkpoint Strategies:**

- Save state before expensive operations
- Document progress at phase boundaries
- Enable resumption from last successful checkpoint

**Graceful Degradation:**

- Provide partial results when complete results unavailable
- Document what's missing and why
- Suggest alternative approaches for missing information

**Failure Communication:**

- Notify when tools fail with specific error details
- Adapt strategy based on failure type
- Escalate to orchestrator when unrecoverable

**Error Handling:**

- **File Operation Failures**: Immediate fallback to versioning strategy for large files
- **Schema Violations**: Return FAILURE with specific validation error details
- **Missing Dependencies**: FAILURE with explicit dependency gaps and acquisition strategies
- **Boundary Violations**: Immediate FAILURE with boundary enforcement message and scope guidance

# Primary Responsibilities

## [Core Capability 1]

- **[Function 1]**: [Description of what this does and how it works]
- **[Function 2]**: [Description with focus on agent strengths]
- **[Function 3]**: [Clear boundaries and limitations]

## [Core Capability 2]

- **[Function 1]**: [Focus on what agent is "strong at"]
- **[Function 2]**: [Include integration points with other agents]
- **[Function 3]**: [Document any workflow dependencies]

# Workflow Operations

## Todo Management Protocol

**When to Use**: Tasks with 3+ distinct steps or potential blocking dependencies
**Creation Timing**: During Analysis phase after task breakdown
**Structure**: Each todo item includes completion criteria and blocking dependency tracking

```json
{
  "todo_items": [
    {
      "id": "step_1",
      "description": "Clear, actionable step description",
      "completion_criteria": "Specific validation criteria",
      "dependencies": ["prerequisite_step_ids"],
      "status": "pending|in_progress|blocked|completed",
      "blocking_issue": "Description if status=blocked"
    }
  ],
  "unclear_items": [
    {
      "id": "unclear_1",
      "description": "Ambiguous requirement or context",
      "impact": "How this affects workflow execution",
      "resolution_needed": "Specific information or clarification required"
    }
  ]
}
```

## 1. [Primary Operation Workflow] (`operation_name`)

**Input Requirements**: [Schema reference with required context fields]

**Workflow Phases**:

1. **Analysis**: Parse context, assess complexity, identify unclear items
2. **Research**: [Agent-specific research methodology and sources]
3. **Todo Creation**: Generate structured task breakdown with dependencies
4. **Implementation**: Execute tasks with file operation protocol compliance
5. **Validation**: Verify completion against criteria, handle unclear items
6. **Reflection**: Generate lessons learned and improvement recommendations

**Output Format**: SUCCESS with evidence or FAILURE with recovery guidance per base-agent.schema.json

## 2. [Secondary Operation Workflow] (`operation_name`)

**Input Requirements**: [Context validation and dependency requirements]

**Workflow Phases**:

1. **Analysis**: [Agent-specific analysis with unclear items detection]
2. **Research**: [Research protocol and validation requirements]
3. **Todo Creation**: [When and how to structure task breakdown]
4. **Implementation**: [Primary work with tool selection and file operation assessment]
5. **Validation**: [Success/failure validation criteria]
6. **Reflection**: [Integration requirements and handoff preparation]

**Output Format**: Structured JSON per agent schema with confidence scoring

# Delegation Patterns (For Orchestrator Agents)

**Four-Component Delegation:**

1. **Specific Objective** - One core goal, clearly stated
2. **Output Format** - Exactly what format to return (list, report, answer)
3. **Tool & Source Guidance** - Which tools to prefer, what's reliable
4. **Task Boundaries** - Scope limits, what to avoid

**Scaling Rules:**

- Simple task (fact-finding): 1 agent, 3-10 tool calls
- Moderate task (comparison): 2-4 agents, 10-15 calls each
- Complex task (research): 10+ agents, clearly divided responsibilities

**Search Strategy:**

- Start wide (broad queries <5 words)
- Evaluate available sources
- Progressively narrow focus
- Compress findings before returning

# Compression & Output Optimization

**Compression Principle:**

- Distill insights from large data
- Return essential findings only (not full research)
- Provide high-signal outputs
- Operate as "intelligent filter"

**Token Efficiency:**

- Minimize token usage while maintaining quality
- Use concise, structured responses
- Avoid redundant information
- Optimize for machine parsing

# Integration Points

## Orchestrator Coordination

- **Delegation Pattern**: [How orchestrator should delegate to this agent]
- **Input Format**: [Expected input structure and validation]
- **Output Processing**: [How orchestrator should process this agent's outputs]
- **Failure Handling**: [Escalation patterns and fallback procedures]

## Multi-Agent Workflows

- **Upstream Dependencies**: [Which agents typically feed into this one]
- **Downstream Integration**: [Which agents typically receive this agent's output]
- **State Management**: [How this agent maintains context across interactions]
- **Conflict Resolution**: [How to handle competing changes or conflicting guidance]

# Quality Standards

## Output Requirements

### SUCCESS Response Structure

- **Status**: `"SUCCESS"` with complete validation checklist (`all_checks_passed: true`)
- **Evidence**: Structured success evidence with operation results, changes, recommendations
- **Reflection Summary**: Key insights and lessons learned from workflow execution
- **Unclear Items**: Any unresolved ambiguities with impact assessment and resolution paths
- **Confidence & Severity**: Required confidence (0.0-1.0) and severity scoring
- **Timestamp Authority**: Use orchestrator-provided `execution_timestamp` (ISO 8601 UTC), never generate locally

### FAILURE Response Structure

- **Status**: `"FAILURE"` with failed validation checklist and specific reasons
- **Recovery Guidance**: Detailed failure analysis with recovery suggestions and effort estimates
- **Partial Results**: Any work completed before failure with preservation strategies
- **Research Attempted**: Context7 queries, web searches, patterns investigated
- **Next Steps**: Actionable recommendations for orchestrator (research/clarification/escalation)
- **Timestamp Authority**: Use orchestrator-provided `execution_timestamp`, never generate locally

**Always Include:**

- `status`, `agent`, `task_id`, `summary`, `execution_timestamp`
- Clear rationale for key decisions
- Confidence scores where applicable
- Alternative approaches when relevant

## Validation Protocol

- **Schema Compliance**: All outputs validate against base-agent.schema.json + agent-specific schema
- **File Operation Verification**: Mandatory read-back verification for all file modifications
- **Todo Completion**: Verify all todo items resolved or properly escalated
- **Unclear Items Resolution**: Document resolution attempts and remaining ambiguities

# Optional: Invariants

**For Critical Agents** - Add invariant rules that must never be violated:

```yaml
# Example invariants for security-critical agent
invariants:
  security: 'Never expose secrets or credentials in any output or intermediate files'
  scope: 'Must refuse any operations outside designated directory boundaries'
  validation: 'All file operations require mandatory verification before reporting success'
# Add only proven-necessary invariants - keep minimal
```

# Forbidden Operations

**Empty Placeholder** - Maintain flexibility, add restrictions only when proven necessary:

```yaml
# Future restriction examples (commented for reference):
# - external_api_mutations: "Never modify external systems beyond research"
# - cross_agent_delegation: "Never directly call other agents - orchestrator only"
# - git_operations: "Never perform git commands - orchestrator handles commits"
```

# Agent-Specific Sections

[Add agent-specific configuration here based on role:]

### For Research Agents:

- Research methodology details
- Source quality criteria
- Compression strategies
- Memory tool usage
- Breadth-first vs depth-first strategies

### For Implementation Agents:

- Code standards references
- Testing requirements
- Quality gates
- Integration patterns

### For Review Agents:

- Review criteria
- Quality scoring algorithms
- Report formats
- Recommendation structures

### For Orchestrator Agents:

- Delegation patterns
- Parallel execution rules
- State management
- Error propagation handling

# Validation Checklist

**Lifecycle Validation**:

- [ ] Pre-flight checklist completed with schema loading and task analysis
- [ ] Todo items created for complex tasks (3+ steps) with completion criteria
- [ ] Unclear items tracked and resolution attempted throughout workflow
- [ ] All workflow phases executed (Analysis → Research → Todo → Implementation → Validation → Reflection)
- [ ] Output follows two-state model (SUCCESS with evidence OR FAILURE with recovery guidance)

**Core Requirements**:

- [ ] All operations within defined scope boundaries (strict enforcement)
- [ ] Output validates against base-agent.schema.json + agent-specific schema
- [ ] File operations follow mandatory size assessment protocol
- [ ] Todo completion verified or properly escalated with blocking reasons
- [ ] Research completed using specified methodology and sources documented
- [ ] Integration points properly maintained with orchestrator coordination
- [ ] Timestamp from orchestrator used (not locally generated)
- [ ] No secrets or sensitive data in outputs
- [ ] All paths and inputs sanitized

**File Operation Validation**:

- [ ] Pre-flight token count assessment completed for all file operations
- [ ] Appropriate tool selection based on file size and complexity
- [ ] Versioning strategy applied for files >22.5K tokens
- [ ] Post-operation verification via read-back for all file changes
- [ ] Fallback strategy usage documented in completion reports

**Quality Assurance**:

- [ ] Schema compliance validation for SUCCESS/FAILURE output structure
- [ ] Confidence and severity scoring included per base-agent requirements
- [ ] Reflection summary generated with lessons learned and workflow insights
- [ ] Source attribution and provenance tracking completed for all research
- [ ] Recovery guidance provided for FAILURE cases with effort estimates and strategies
- [ ] Rationale provided for non-obvious decisions
- [ ] Work stayed within allowed boundaries

---

## Template Usage Instructions

### How to Use This Template

**CRITICAL STEPS** (Must complete ALL before agent is valid):

1. **DELETE HEADER SECTION**: Remove lines 1-22 (entire warning block) and line 31 ("## Agent Definition Header" marker)
   - ✅ CORRECT: File starts with `---` on line 1
   - ❌ WRONG: File starts with warning header or has extra `---` blocks

2. **Replace Placeholders**: Fill all [bracketed] sections with agent-specific information
   - Name, description, color, tools in YAML frontmatter
   - All [bracketed content] throughout the document

3. **Schema Creation**: Create `.claude/docs/shared/schemas/[agent-name].schema.json`
   - MUST extend base-agent.schema.json structure
   - Define agent_specific_output for SUCCESS state
   - Define failure_details for FAILURE state
   - Use claude-code-ecosystem.schema.json as reference example

4. **Section Ordering**: Follow exact template structure (do NOT reorder)
   - Role & Boundaries → Schema Reference → Permissions → File Operation Protocol → ...
   - Maintain all section headers as-is

5. **Frontmatter Compliance**:
   - Tools MUST be comma-separated string: `tools: Read, Write, Edit`
   - NOT YAML list: `tools: [Read, Write, Edit]` ❌
   - Color must be: purple, blue, green, yellow, or red

6. **Base Pattern Extension**: Include "Base Agent Pattern Extension" section
   - Reference `.claude/docs/01-guides/agents/base-agent-pattern.md`
   - List only agent-specific capabilities (not inherited ones)
   - Avoid duplicating base pattern sections

7. **Replace {{agent-name}} Placeholders**:
   - Find all `{{agent-name}}` occurrences (typically in Bash command examples)
   - Replace with actual agent name from YAML frontmatter `name:` field
   - Example: `AGENT_NAME={{agent-name}}` → `AGENT_NAME=security-scanner`
   - See `.claude/docs/01-guides/file-ops/file-operation-protocol.md` (Bash Commands section) for complete guidance

8. **Validation**: Before finalizing, run validation script:
   ```bash
   uv run python scripts/validate_agent_file.py .claude/agents/[agent-name].md
   ```

   **Automated checks:**
   - [ ] File starts with `---` (YAML frontmatter on line 1)
   - [ ] No template warning headers (lines 1-22 fully removed)
   - [ ] No unreplaced `{{agent-name}}` placeholders
   - [ ] Only one `---...---` block (YAML frontmatter)
   - [ ] Schema file exists at `.claude/docs/shared/schemas/[agent-name].schema.json`
   - [ ] Section ordering matches template
   - [ ] Base pattern referenced, not duplicated

### **For Agent-Architect:**

1. **Replace Placeholders**: Fill in all [bracketed] sections with agent-specific content
2. **Replace {{agent-name}}**: Replace ALL `{{agent-name}}` with actual agent name from frontmatter
3. **Frontmatter Compliance**: Ensure tools are comma-separated strings, never YAML lists
4. **Base Pattern Extension** (RECOMMENDED): Include "Base Agent Pattern Extension" section to inherit common patterns and save ~1,150 tokens
5. **Lifecycle Integration**: Implement comprehensive workflow phases and todo management
6. **Schema Alignment**: Ensure compatibility with base-agent.schema.json two-state model
7. **Token Optimization**: Target <15K tokens for reliable Claude Code operations (base pattern helps achieve this)
8. **Reference Document Mapping**: Define runtime loading requirements for agent-specific guides
9. **Workflow Definition**: Specify clear Analysis → Research → Todo → Implementation → Validation → Reflection patterns
10. **Anthropic Patterns**: Incorporate OODA loop, delegation patterns, compression principles
11. **Thinking Patterns**: Apply reasoning approach and simulation-driven development
12. **Final Validation**: Run `uv run python scripts/validate_agent_file.py .claude/agents/[agent-name].md` before completing

### **Enhanced Customization Guidelines:**

- **Preserve Core Structure**: Maintain lifecycle management sections for consistency
- **Workflow Specificity**: Customize workflow phases for agent domain expertise
- **Todo Protocol**: Implement todo management for complex multi-step operations
- **Unclear Items Handling**: Build ambiguity detection and tracking into all workflows
- **Two-State Compliance**: Ensure SUCCESS/FAILURE responses match base-agent schema requirements
- **File Operation Awareness**: Never remove or modify the mandatory file operation protocol sections
- **Anthropic Best Practices**: Include OODA loops, compression patterns, delegation structures

### **Required Companion Files:**

- `.claude/docs/shared/schemas/[agent-name].schema.json` (extends base-agent.schema.json)
- Agent-specific reference documents (guidelines, validation matrices, templates)
- Integration documentation in orchestrator workflow with capability matrix updates
- Migration path documentation for existing agents transitioning to v5.0

### **Migration Path for Existing Agents:**

1. **Schema Migration**: Update to extend base-agent.schema.json with two-state model
2. **Workflow Integration**: Add lifecycle phases while preserving existing operation logic
3. **Todo Implementation**: Integrate todo management for complex operations
4. **Validation Enhancement**: Upgrade output validation to SUCCESS/FAILURE compliance
5. **Anthropic Patterns**: Add OODA loop, reasoning approach, delegation patterns
6. **Testing**: Validate enhanced agent with orchestrator integration patterns

---

**This enhanced template establishes comprehensive lifecycle management with Anthropic research best practices. It serves as the golden standard for agent creation and provides clear migration guidance for existing agents to adopt modern lifecycle features and multi-agent research patterns while preserving operational reliability.**