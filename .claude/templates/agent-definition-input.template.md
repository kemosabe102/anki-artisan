# Agent Definition Input Template

**Purpose**: Use this template to define a new agent for the `/create-agent` command. Fill out all required sections completely to enable automatic agent generation with proper research, tool selection, and integration.

**📚 Need Help?** See **`docs/04-guides/agent-creation-guide.md`** for:

- Step-by-step instructions for filling out this template
- Complete examples (security-scanner, test-dataset-creator)
- Tips & best practices for agent design
- Command reference and workflow details

---

## 1. Basic Information

### Agent Name

**Format**: `[domain]-[action]` (e.g., `security-scanner`, `code-quality`, `development`)

**Name**: **\*\***\_\_\_**\*\***

**Naming Guidance**:

- **Domain Options**: security, spec, code, test, doc, research, git, config, deployment, monitoring, data, etc.
- **Action Options**: scanner, reviewer, implementer, enhancer, analyzer, runner, creator, validator, optimizer, monitor, etc.
- Use kebab-case (lowercase with hyphens)
- Be descriptive but concise

### Domain Scope

**Choose ONE that best fits** (determines which files/directories this agent operates on):

- [ ] `.claude/**` - Claude Code ecosystem (agents, commands, hooks, schemas)
- [ ] `packages/**` - Main codebase implementation (Python, scripts)
- [ ] `tests/**` - Test suite (unit tests, integration tests, test data)
- [ ] `docs/**` - Documentation and specifications
- [ ] `cross-domain` - Works across multiple directories (e.g., research, analysis)

**Selected**: **\*\***\_\_\_**\*\***

**Directory Boundaries** (if not cross-domain, specify exact paths this agent can access):

- Read access: **\*\***\_\_\_**\*\***
- Write access: **\*\***\_\_\_**\*\***
- Forbidden paths: **\*\***\_\_\_**\*\***

---

## 1A. Agent Directory Structure

### Automatic Directory Assignment

Based on your Domain Scope selection above, your agent will be created at:
- **Path**: `.claude/agents/{domain}/{{agent-name}}/`

**Domain Mapping**:
| Domain Scope Selection | Agent Directory |
|----------------------|-----------------|
| `.claude/**` | `.claude/agents/dev-tools/` |
| `packages/**` | `.claude/agents/dev-tools/` |
| `tests/**` | `.claude/agents/dev-tools/` |
| `docs/**` | `.claude/agents/dev-tools/` |
| Financial/trading focus | `.claude/agents/investing/` |
| Research/information gathering | `.claude/agents/research/` |
| Other (specify) | `.claude/agents/{custom}/` |

### Documentation Plan (`docs/`)

**Purpose**: Agent-specific knowledge, frameworks, and methodologies that live WITH the agent.

**Instructions**: List documentation files to create. These are AI-readable guides.

**Planned Documentation**:
```
docs/
├── _____.md - [Brief description]
├── _____.md - [Brief description]
└── _____.md - [Brief description (optional)]
```

**Leave blank** if unsure - the command will auto-generate from research.

### Examples Plan (`examples/`)

**Purpose**: Show orchestrator how to invoke this agent with realistic scenarios.

**Instructions**: List usage examples to include.

**Planned Examples**:
```
examples/
├── _____.md - [Scenario description]
├── _____.md - [Scenario description (optional)]
```

**Minimum**: At least 1 basic usage example recommended.

### Frameworks to Include

**Purpose**: List domain frameworks/methodologies to document in `docs/`.

**Frameworks** (optional):
1. **[Framework Name]** - [How agent uses it]
2. **[Framework Name]** - [How agent uses it]

---

### Agent Type

**Choose ONE that best describes the primary work pattern**:

- [ ] **Creator** - Generates new artifacts (code, docs, specs, tests)
- [ ] **Reviewer** - Validates existing artifacts for quality, standards, correctness
- [ ] **Enhancer** - Improves existing artifacts (refactoring, optimization, enrichment)
- [ ] **Runner** - Executes operations (tests, builds, deployments, commands)
- [ ] **Analyzer** - Investigates and reports findings (patterns, issues, metrics)
- [ ] **Planner** - Creates plans, strategies, research delegation

**Selected**: **\*\***\_\_\_**\*\***

---

## 2. Purpose & Description

### Orchestrator Description

**Instructions**: Write 1-3 sentences describing WHEN the orchestrator should call this agent. Focus on trigger conditions and context signals.

**Example**: "Performs static application security testing (SAST) on modified code using Semgrep to detect vulnerabilities before commit. Integrates with git workflow as a parallel quality gate alongside code-quality. Triggers automatically when files in packages/\*\* are modified."

**Your Description**:

```
[Write your description here - be specific about triggers, context, and integration points]
```

### Value Proposition

**Instructions**: Explain WHY this agent is needed (what problem does it solve? what gap does it fill?).

**Example**: "Existing code-quality focuses on style and best practices but doesn't catch security vulnerabilities. This agent adds OWASP-focused security scanning to prevent CVEs from reaching production."

**Your Value Proposition**:

```
[What unique value does this agent provide?]
```

---

## 3. Core Capabilities

**Instructions**: List 3-7 specific, actionable capabilities. Each should be a concrete task the agent performs.

**Format**: Use action verbs (analyzes, generates, validates, executes, detects, etc.)

**Examples**:

- ✅ GOOD: "Scans Python code for SQL injection vulnerabilities using Semgrep OWASP ruleset"
- ❌ BAD: "Handles security" (too vague)

**Your Capabilities**:

1. [Capability 1 - specific action with clear scope]
2. [Capability 2 - specific action with clear scope]
3. [Capability 3 - specific action with clear scope]
4. [Capability 4 - optional]
5. [Capability 5 - optional]
6. [Capability 6 - optional]
7. [Capability 7 - optional]

---

## 4. Input/Output Contract

### Expected Inputs

**Instructions**: Define what information the agent needs to do its work. Be specific about data types and validation requirements.

**Format**:

```
- **[input_field_name]**: [Description, data type, validation rules]
```

**Examples**:

```
- **files_to_scan**: List of absolute file paths (string[]) - must exist and be readable
- **scan_mode**: Enum ["fast", "comprehensive"] - determines ruleset selection
- **severity_threshold**: Enum ["critical", "high", "medium", "low"] - minimum severity to report
```

**Your Inputs**:

```
- **[input_1]**: [description, type, validation]
- **[input_2]**: [description, type, validation]
- **[input_3]**: [description, type, validation]
```

### Expected Outputs

#### On Success (Status: SUCCESS)

**Instructions**: Describe what the agent delivers when the operation completes successfully. Include structure, format, and key fields.

**Example**:

```
Security report (JSON) with:
- **findings**: Array of vulnerability objects (severity, confidence, location, remediation)
- **summary**: Aggregate counts by severity level
- **scan_metadata**: Files scanned, rules used, execution time
- **recommendations**: Prioritized action items for developer
```

**Your Success Output**:

```
[Describe structure, format, and key fields for successful execution]
```

#### On Failure (Status: FAILURE)

**Instructions**: Describe what information is provided when the operation fails. Include error categorization and recovery guidance.

**Example**:

```
Failure report (JSON) with:
- **failure_category**: Enum ["tool_error", "invalid_input", "file_access_error"]
- **error_details**: Specific error message and stack trace (if applicable)
- **recovery_suggestions**: Actionable steps to resolve the issue
- **partial_results**: Any findings collected before failure (optional)
```

**Your Failure Output**:

```
[Describe error structure, categorization, and recovery information]
```

---

## 5. Domain Knowledge & Expertise

### Required Frameworks/Standards

**Instructions**: List specific frameworks, methodologies, standards, or best practices this agent needs to understand. Be as specific as possible. If unknown, the command will research automatically.

**Examples**:

```
- OWASP Top 10 2021 (security vulnerabilities)
- Semgrep rule syntax and customization
- Python PEP 8 style guide (for code context understanding)
- Git pre-commit hook integration patterns
```

**Your Domain Knowledge** (optional - leave blank if unsure):

```
- [Framework/standard 1]
- [Framework/standard 2]
- [Framework/standard 3]
- [Framework/standard 4]
```

### Key Concepts & Terminology

**Instructions**: List domain-specific terms, jargon, or concepts the agent must understand.

**Examples**:

```
- Static Application Security Testing (SAST)
- Dynamic taint analysis
- False positive rate vs. false negative rate
- CVE (Common Vulnerabilities and Exposures)
```

**Your Key Concepts** (optional):

```
- [Concept 1]
- [Concept 2]
- [Concept 3]
```

---

## 5A. OODA Loop Integration

**Purpose**: Define how this agent participates in the orchestrator's OODA (Observe-Orient-Decide-Act) decision framework. This ensures proper context gathering, delegation, and execution patterns.

**Why This Matters**: The OODA loop is the orchestrator's core decision-making framework. Understanding how your agent fits into each phase prevents scope drift, ensures proper context gathering, and enables effective multi-agent coordination.

**Reference Framework**: `.claude/docs/00-core/ooda-loop-framework.md`

---

### OBSERVE Phase Contribution

**Question**: What does this agent observe/parse when the orchestrator calls it?

**Check all that apply**:

- [ ] Request parsing (extracts specific parameters from user input)
- [ ] Context assessment (evaluates available information quality)
- [ ] Complexity classification (simple vs multi-component vs architectural)
- [ ] File/directory scope identification
- [ ] Error condition detection
- [ ] Other: _______________

**Example (development agent)**:
- ✅ Request parsing (extracts error message, file path, reproduction steps)
- ✅ Context assessment (checks if stack trace available, logs accessible)
- ✅ Complexity classification (single-file bug vs multi-component integration issue)

**Your OBSERVE Contribution**:

```
[Describe what this agent observes/parses when invoked]
```

---

### ORIENT Phase Contribution

**Question**: How does this agent assess Context_Quality and gather necessary information?

**Context_Quality Formula**: (Domain × 0.40) + (Pattern × 0.30) + (Dependency × 0.20) + (Risk × 0.10)

**For each dimension, specify how this agent evaluates it**:

**Domain Familiarity (0.0-1.0)**:
- What domain knowledge does this agent need?
- How does it assess if it has sufficient domain understanding?

**Pattern Clarity (0.0-1.0)**:
- What existing patterns does this agent look for?
- Where does it check for reference implementations?

**Dependency Understanding (0.0-1.0)**:
- What integration points does this agent need to understand?
- How does it map dependencies and interfaces?

**Risk Awareness (0.0-1.0)**:
- What failure modes does this agent consider?
- How does it assess potential side effects?

**Your ORIENT Contribution**:

```
**Domain Familiarity**:
[How agent assesses domain understanding - e.g., "Checks Context7 for library docs, searches codebase for existing implementations"]

**Pattern Clarity**:
[How agent finds patterns - e.g., "Uses Grep to find similar test files, reviews existing fixtures for structure"]

**Dependency Understanding**:
[How agent maps dependencies - e.g., "Reads import statements, traces function calls, validates API contracts"]

**Risk Awareness**:
[How agent identifies risks - e.g., "Considers backward compatibility, data migration impacts, performance degradation"]
```

**Information Hierarchy** (Priority order for context sources):

1. **Primary source**: _______________
2. **Secondary source**: _______________
3. **Tertiary source**: _______________
4. **Fallback source**: _______________

**Example (development)**:
1. Primary: COMPONENT_ALMANAC.md (existing implementations)
2. Secondary: Similar files in same package (local patterns)
3. Tertiary: Context7 library docs (official API reference)
4. Fallback: research agent with web-research skill (community best practices)

**Context_Quality Threshold**:

- **Minimum threshold to proceed**: _______ (typically 0.5-0.7)
- **Action if below threshold**: Delegate to researcher-_____ OR escalate to user

---

### DECIDE Phase Contribution

**Question**: What decisions does this agent make, and what's the decision framework?

**Decision Framework**:

**Main Action** → **Follow-up Action** → **Checkpoint**

**Example (code-quality agent)**:
- Main Action: Execute test suite with pytest
- Follow-up Action: Categorize failures (assertion vs import vs timeout)
- Checkpoint: Validate all tests ran, check exit code, parse output

**Your Decision Framework**:

```
**Main Action**: [Primary task this agent performs]

**Follow-up Action**: [Secondary analysis, validation, or categorization]

**Checkpoint**: [How agent verifies decision quality before reporting]
```

**Agent Selection Confidence Ranges** (for this agent):

- **HIGH (0.7-1.0)**: [Conditions where this agent is best fit - e.g., "Files in packages/core/**, known bug patterns, stack trace available"]
- **MEDIUM (0.5-0.69)**: [Borderline conditions - e.g., "Files in packages/** but unfamiliar module, vague error description"]
- **LOW (<0.5)**: [When this agent is NOT suitable - e.g., "Files in docs/**, no error message, architectural changes"]

---

### ACT Phase Contribution

**Question**: What execution actions does this agent perform, and how does it iterate on failures?

**Execution Actions** (list tools + workflows):

1. **Tool 1**: _______ → **Purpose**: _______
2. **Tool 2**: _______ → **Purpose**: _______
3. **Tool 3**: _______ → **Purpose**: _______

**Example (security-scanner agent)**:
1. Bash → Execute Semgrep SAST scan on target files
2. Read → Load scanned files for context in report
3. Write → Generate security report JSON artifact
4. Grep → Search for related vulnerability patterns across codebase

**Your Execution Actions**:

```
1. **[Tool]**: [Purpose and usage pattern]
2. **[Tool]**: [Purpose and usage pattern]
3. **[Tool]**: [Purpose and usage pattern]
```

**Iteration Protocol**:

- **Confidence threshold for iteration**: _______ (default: <0.85 triggers retry)
- **Max iterations**: _______ (default: 3)
- **Iteration action**: Gather more context via _______ OR delegate to _______ OR escalate to user

**Example (development agent)**:
- Confidence <0.85: Return to ORIENT phase, gather additional logs/traces
- Max iterations: 3 debugging cycles
- Iteration action: If confidence still low after 3 cycles → escalate to user with findings

**Your Iteration Protocol**:

```
[Describe how agent iterates when confidence <0.85 or initial action fails]
```

---

**OODA Integration Checklist**:

- [ ] OBSERVE phase: Defined what agent parses/identifies
- [ ] ORIENT phase: Specified Context_Quality assessment approach
- [ ] ORIENT phase: Listed information hierarchy (4 priority levels)
- [ ] ORIENT phase: Set Context_Quality threshold for proceeding
- [ ] DECIDE phase: Documented decision framework (Main → Follow-up → Checkpoint)
- [ ] DECIDE phase: Specified Agent Selection Confidence ranges (HIGH/MEDIUM/LOW)
- [ ] ACT phase: Listed execution tools and workflows
- [ ] ACT phase: Defined iteration protocol (threshold, max iterations, action)

---

## 5B. Navigation Rules

**Purpose**: Define how this agent navigates information, makes decisions under uncertainty, and handles topics outside its domain scope. Navigation Rules prevent hallucination, boundary violations, and scope drift.

**Why This Matters**: Navigation Rules scored 0.35/1.0 (lowest technical score) in agent evaluation. Clear information hierarchy and limitation protocols are critical for preventing agents from operating outside their expertise.

**Reference Framework**: `.claude/docs/01-guides/infuse-framework-quick-ref.md` (N - Navigation Rules)

---

### Information Hierarchy

**Concept**: Like a research librarian - always check primary sources before secondary, always cite sources, never invent information.

**Define the priority order for information sources** (1 = highest authority):

**1. Primary Source** (authoritative, always trusted):
- **Source Type**: [Official docs / Schema files / SPEC.md / Test fixtures / etc.]
- **Location**: [File path or URL pattern]
- **Usage**: [When to consult this source]

**Example (development)**:
- Source Type: COMPONENT_ALMANAC.md
- Location: `docs/00-project/COMPONENT_ALMANAC.md`
- Usage: Check BEFORE creating any new code (prevents duplication)

**Your Primary Source**:

```
**Source Type**: _______
**Location**: _______
**Usage**: _______
```

**2. Secondary Source** (reliable but may need validation):
- **Source Type**: _______
- **Location**: _______
- **Usage**: _______

**Example (code-quality)**:
- Source Type: Existing test files in same package
- Location: `tests/{package_name}/test_*.py`
- Usage: Follow patterns for test structure, fixtures, assertions

**Your Secondary Source**:

```
**Source Type**: _______
**Location**: _______
**Usage**: _______
```

**3. Tertiary Source** (supplementary, cross-reference recommended):
- **Source Type**: _______
- **Location**: _______
- **Usage**: _______

**Example (library-research skill)**:
- Source Type: Context7 library documentation
- Location: Official package docs via Context7 API
- Usage: Understand library API, validate usage patterns

**Your Tertiary Source**:

```
**Source Type**: _______
**Location**: _______
**Usage**: _______
```

**4. Fallback Source** (last resort, use when others unavailable):
- **Source Type**: _______
- **Location**: _______
- **Usage**: _______

**Example (development)**:
- Source Type: research agent with web-research skill (community forums, GitHub issues)
- Location: WebSearch for specific error messages
- Usage: Only when official docs don't cover error, cross-reference multiple sources

**Your Fallback Source**:

```
**Source Type**: _______
**Location**: _______
**Usage**: _______
```

---

### Decision Protocol

**Structured workflow for making decisions under uncertainty**:

**Format**: Main Action → Follow-up Action → Checkpoint

**Example 1 (code-reviewer)**:
- **Main Action**: Scan modified files for style violations, security issues, test coverage
- **Follow-up Action**: Categorize findings by severity (blocking vs warning vs suggestion)
- **Checkpoint**: Validate all files reviewed, check exit code, ensure actionable feedback provided

**Example 2 (planning)**:
- **Main Action**: Read incomplete plan, identify [TODO] and [TBD] sections
- **Follow-up Action**: Research domain requirements via Context7 + web-research skill
- **Checkpoint**: Validate all TODO sections addressed, cross-reference with COMPONENT_ALMANAC.md for consistency

**Your Decision Protocol**:

```
**Main Action**: [Primary task this agent performs]

**Follow-up Action**: [Secondary analysis, validation, or categorization - what happens after main action?]

**Checkpoint**: [How agent verifies quality before reporting SUCCESS - validation criteria]
```

**Decision Tree Example** (for complex agents):

```
IF [condition 1] THEN [action A] ELSE [action B]
IF [condition 2] THEN [delegate to agent X] ELSE [handle directly]
IF [threshold exceeded] THEN [escalate to user] ELSE [proceed with confidence score]
```

**Your Decision Tree** (optional, for agents with complex branching logic):

```
[Document decision tree if agent has multiple execution paths based on conditions]
```

---

### Limitations Protocol

**How does this agent handle requests outside its domain scope?**

**Choose the appropriate limitation handling strategy**:

**Strategy 1: Acknowledge + Recommend Specialist**

- **When to use**: Request is valid but outside agent's domain
- **Response pattern**: "This is outside my domain scope ([domain]). Recommend delegating to [specialist_agent] for [specific_capability]."

**Example (development handling docs/** file)**:
- "This file is in docs/**, outside my domain (packages/**). Recommend delegating to documentation for documentation structure or using the /spec command for specification content."

**Strategy 2: Report Gap + Suggest Sources**

- **When to use**: Agent lacks information/context to proceed
- **Response pattern**: "Insufficient [context/information] to [perform_action]. Recommend researching [specific_sources] or consulting [specific_files]."

**Example (development missing stack trace)**:
- "Insufficient error context to diagnose issue. Recommend: (1) Reproduce error with verbose logging, (2) Capture full stack trace, (3) Provide environment details (Python version, package versions)."

**Strategy 3: State Assumptions + Confidence**

- **When to use**: Agent can proceed but with uncertainty
- **Response pattern**: "Assuming [assumption] based on [evidence]. Confidence: [0.0-1.0]. Recommend validating [specific_aspect] before proceeding."

**Example (code-quality without complete spec)**:
- "Assuming input validation requirements based on type hints in function signature. Confidence: 0.65. Recommend validating edge cases with domain expert or reviewing SPEC.md Section X for complete requirements."

**Your Limitations Protocol**:

```
**Primary Strategy**: [Strategy 1/2/3 from above]

**Example Limitation Scenario**: [Describe specific case where agent hits limitation]

**Agent Response**: [How agent handles this scenario - exact wording/pattern]
```

**Escalation Path** (when agent cannot proceed):

1. **First attempt**: [What agent tries first - e.g., "Check COMPONENT_ALMANAC.md for similar component"]
2. **Second attempt**: [Fallback - e.g., "Delegate to research agent with codebase-research skill for pattern discovery"]
3. **Final escalation**: [Last resort - e.g., "Report to orchestrator with gap analysis, recommend user clarification"]

---

**Navigation Rules Checklist**:

- [ ] Information Hierarchy: Defined 4 priority levels (Primary → Secondary → Tertiary → Fallback)
- [ ] Decision Protocol: Documented Main → Follow-up → Checkpoint workflow
- [ ] Decision Protocol: Optional decision tree for complex branching logic
- [ ] Limitations Protocol: Selected handling strategy (Acknowledge/Report/Assume)
- [ ] Limitations Protocol: Provided example limitation scenario with agent response
- [ ] Escalation Path: Defined 3-step escalation (attempt 1 → attempt 2 → final escalation)

---

## 6. Tool Requirements

**Instructions**: If you know which Claude Code tools this agent needs, list them with confidence scores (0.0-1.0) and rationale. Otherwise, leave blank and the command will recommend automatically.

**Available Tools**: Read, Write, Edit, Glob, Grep, Bash, WebFetch, Task

**Format**:

```
- **[Tool Name]** (confidence: [0.0-1.0], rationale: [why needed])
```

**Examples**:

```
- **Bash** (confidence: 1.0, rationale: Required to execute Semgrep CLI commands and parse JSON output)
- **Read** (confidence: 1.0, rationale: Must read code files to provide context in security reports)
- **Grep** (confidence: 0.8, rationale: Search for related vulnerability patterns across codebase for context)
- **Write** (confidence: 0.9, rationale: Generate security report artifacts in docs/ for review)
```

**Your Tool Requirements** (optional - leave blank if unsure):

```
- **[Tool 1]** (confidence: [0.0-1.0], rationale: [why])
- **[Tool 2]** (confidence: [0.0-1.0], rationale: [why])
- **[Tool 3]** (confidence: [0.0-1.0], rationale: [why])
```

**Tool Selection Guidance**:

- **Read** - Reading files, checking existence, gathering context
- **Write** - Creating new files, generating reports, writing artifacts
- **Edit** - Modifying existing files (prefer over Write for updates)
- **Glob** - Finding files by pattern (_.py, \*\*/_.json, etc.)
- **Grep** - Searching file contents with regex patterns
- **Bash** - Executing shell commands (use sparingly, security risk)
- **WebFetch** - Fetching external documentation or resources
- **Task** - Delegating to other agents (for orchestrators/planners only)

### Disallowed Tools (OPTIONAL)

**Purpose**: Explicitly block specific tools for security or scope control. Use when you want to prevent the agent from using certain tools even if they might otherwise be available.

**When to Use**:
- Security constraints (e.g., read-only agents should block Write, Edit, Bash)
- Scope limitations (e.g., research agents should block file modification)
- Policy enforcement (e.g., workers should not delegate via Task tool)

**Format**:

```
**Disallowed Tools** (optional - leave blank if no restrictions):

- **[Tool Name]** - [Why this tool should be blocked]

Examples:
- **Bash** - Read-only agent should not execute commands
- **Write** - Reviewer agent should not modify files
- **Task** - Worker agent should not delegate to other agents
- **WebFetch** - Internal-only agent should not access external resources
```

**Anti-Patterns to Avoid**:
- ❌ Blocking tools "just in case" without security rationale
- ❌ Blocking Task tool for coordinator agents (defeats delegation)
- ❌ Over-restricting tools before testing agent capabilities
- ✅ Start permissive with runtime monitoring, add `disallowedTools` based on observed misuse patterns or security audits (principle: restrict based on evidence, not assumption)

**Your Disallowed Tools** (optional):

```
- **[Tool 1]** - [Reason for blocking]
- **[Tool 2]** - [Reason for blocking]
```

### File Operations (If Agent Modifies Files)

**Protocol Reference**: `.claude/docs/01-guides/file-ops/file-operation-protocol.md`

**Tool Selection**: ALWAYS use Desktop Commander for file modifications.

**Example Workflow**:
```python
# 1. Read file
content = Read("path/to/file.py")

# 2. Edit with Desktop Commander
mcp__desktop-commander__edit_block(
    file_path="path/to/file.py",
    old_string="old text to replace",
    new_string="new replacement text"
)
```

**Common Scenarios**:
- Surgical edits: `mcp__desktop-commander__edit_block` - precise string replacement
- Full file writes: `mcp__desktop-commander__write_file` - chunk into 25-30 lines per call

**See**: `.claude/docs/01-guides/file-ops/file-operation-protocol.md` for complete protocol

### Bash Command Standards (MANDATORY)

**AGENT_NAME Prefix**: ALL Bash commands MUST start with agent name from frontmatter

```bash
AGENT_NAME={{{{agent-name}}}} [command]
```

**Why Required**:
- Command traceability in multi-agent workflows
- Audit logging and debugging
- Security hook enforcement (enables bypass configuration)

**Agent Name Source**: Use exact `name:` value from YAML frontmatter (line 2 of agent file)

**Examples**:
```bash
AGENT_NAME={{{{agent-name}}}} pytest tests/ -v
AGENT_NAME={{{{agent-name}}}} uv run python scripts/prepare-code-review.py --fast
AGENT_NAME={{{{agent-name}}}} semgrep --config=auto packages/
```

**Non-Compliance**: Agents without AGENT_NAME prefix may have commands blocked or untraced in audit logs.

---

## 6A. Skills Configuration

### Auto-Loaded Skills

**Purpose**: Skills are domain knowledge bundles **auto-loaded** into the agent's context on start. They provide frameworks, patterns, and methodologies without bloating the agent prompt.

**Instructions**: Select skills that provide knowledge this agent needs frequently. Limit to 1-3 skills to avoid context bloat.

**Selected Skills** (comma-separated):

**___________**

**Available Project Skills** (`.claude/skills/`):

| Skill | Purpose | Good For |
|-------|---------|----------|
| `debugging-methodology` | 8-step debugging, 5 Whys RCA, SCAMPER | Debuggers, fixers |
| `code-review-standards` | Severity classification, blast radius | Code reviewers |
| `test-driven-development` | TDD workflow, test patterns | Test creators |
| `python-implementation` | Python coding standards | Python implementers |
| `analyzing-code-complexity` | Cyclomatic complexity detection | Code analyzers |
| `codebase-research` | Tool patterns, finding templates | Researchers |

**Plugin Skills** (from MCP plugins):
- `example-skills:docx` - Document creation/editing
- `example-skills:pdf` - PDF handling
- `example-skills:xlsx` - Excel file handling

**Rationale for Selection**: ___________

---

## 7. Integration & Workflow

### Integration Points

**Instructions**: Describe how this agent fits into existing workflows, which agents it coordinates with, and any dependencies.

**Examples**:

```
- Runs in parallel with code-quality during pre-commit validation
- Triggered by source-control agent when files in packages/** are modified
- Failure blocks commit (validation gate) - escalates to development if issues found
- Success allows commit to proceed - reports sent to monitoring dashboard
```

**Your Integration Points** (optional):

```
[Describe workflow integration, agent coordination, and dependencies]
```

### Trigger Conditions

**Instructions**: Define when the orchestrator should invoke this agent.

**Examples**:

```
- ANY file in packages/** modified (auto-trigger)
- User runs /security command (manual trigger)
- Pre-commit hook validation phase (workflow trigger)
- Severity threshold: Run for all commits touching auth/security code
```

**Your Trigger Conditions**:

```
[When should orchestrator call this agent?]
```

### Performance Requirements

**Instructions**: Specify any time, token, or resource constraints.

**Examples**:

```
- Execution time: <60 seconds for typical changeset (5-10 files)
- Token budget: <50K tokens for scan + report generation
- Parallelization: Can run in parallel with other quality gates
- Failure tolerance: Must complete even if some files unreadable
```

**Your Performance Requirements** (optional):

```
[Time, token, or resource constraints]
```

---

## 8. Quality & Validation

### Success Criteria

**Instructions**: Define what "success" looks like for this agent. How do you measure quality of outputs?

**Examples**:

```
- All requested files scanned successfully
- Report contains actionable findings with remediation steps
- Confidence scores provided for each finding (0.0-1.0)
- False positive rate <10% based on manual review
- No critical vulnerabilities missed (measured against known CVE database)
```

**Your Success Criteria**:

```
[How do you measure quality and success?]
```

### Validation Checks

**Instructions**: List specific checks the agent should perform before reporting SUCCESS.

**Examples**:

```
- [ ] All input files exist and are readable
- [ ] Semgrep execution completed without errors
- [ ] Report validates against security-scanner.schema.json
- [ ] All findings include severity, confidence, and remediation
- [ ] No secrets or credentials exposed in report outputs
```

**Your Validation Checks**:

```
- [ ] [Validation check 1]
- [ ] [Validation check 2]
- [ ] [Validation check 3]
```

---

## 9. Edge Cases & Error Handling

### Known Edge Cases

**Instructions**: List scenarios where the agent might struggle or fail. This helps the command design better error handling.

**Examples**:

```
- Binary files in scan path (should skip gracefully)
- Files too large for Semgrep (>10MB - warn and skip)
- Network-dependent rules (may fail in offline mode)
- Mixed Python 2/3 codebases (different syntax rules)
```

**Your Edge Cases** (optional):

```
[Scenarios where agent might fail or behave unexpectedly]
```

### Error Recovery Strategy

**Instructions**: Describe how the agent should handle failures.

**Examples**:

```
- File access error → Skip file, log warning, continue scanning others
- Semgrep crash → Retry once, then fail with diagnostic info
- Rule parsing error → Fall back to default OWASP ruleset
- Timeout → Return partial results with timeout warning
```

**Your Error Recovery** (optional):

```
[How should agent handle failures and recover?]
```

---

## 9A. Signals & Adaptation

**Purpose**: Define how this agent adapts communication style and approach based on user emotional/behavioral cues. This section is REQUIRED for user-facing agents, OPTIONAL for worker agents.

**Why This Matters**: Signals & Adaptation scored 0.10/1.0 (lowest overall score) in agent evaluation. User-facing agents need emotional intelligence to detect confusion, frustration, enthusiasm, and overwhelm, then adapt responses accordingly.

**Reference Framework**: `.claude/docs/01-guides/orchestration/orchestrator-signal-response-library.md` (30+ user state patterns with adaptive response templates)

---

### User-Facing Check

**Is this agent user-facing?**

- [ ] **YES** - Agent interacts directly with users (complete this section)
- [ ] **NO** - Agent is a worker/backend processor (skip this section)

**Examples**:
- ✅ User-facing: orchestrator, planning (clarification dialogs), architecture (clarification dialogs)
- ❌ Worker agents: code-quality (runs tests), security-scanner (SAST analysis), file-ops (utility)

**Your Agent Classification**: _______

**If NO (worker agent)**: Skip to Section 10. Additional Context.

**If YES (user-facing agent)**: Complete the signal-response pairs below.

---

### Signal-Response Pairs (Minimum 4 Required)

**Instructions**: For each user emotional/behavioral state, define:
1. **Signal**: Observable cues in user communication
2. **Response Pattern**: How agent adapts (verbosity, tone, approach)

**Required Patterns** (customize for your agent's domain):

---

#### Signal 1: Confusion → Simplification

**User Signal** (how you detect confusion):
- [ ] Multiple rephrased questions about same concept
- [ ] "I don't understand..."
- [ ] "Can you clarify...?"
- [ ] Long silence after complex explanation
- [ ] Other: _______

**Example Signal**:
- User: "I don't understand the Context_Quality formula"

**Agent Response Pattern** (how you adapt):

```
[Describe how agent simplifies when detecting confusion]

Example (orchestrator):
"Let me simplify. Context_Quality = 4 questions: (1) Do I know this tech? (2) Are there examples? (3) Are dependencies clear? (4) What could go wrong? Score <0.5 = 'I should research first.'"
```

**Your Confusion Response**:

```
**Signal Detection**: [How you identify user is confused]

**Response Adaptation**: [How you simplify - shorter sentences, analogies, concrete examples]
```

---

#### Signal 2: Frustration → Empathy + Systematic Breakdown

**User Signal** (how you detect frustration):
- [ ] Shortened responses ("OK...", "Fine.")
- [ ] All caps or exclamation marks
- [ ] "This is too complicated"
- [ ] "Just do it yourself"
- [ ] Other: _______

**Example Signal**:
- User: "I just want to fix one line, why all this process?"

**Agent Response Pattern** (how you adapt):

```
[Describe how agent acknowledges frustration and provides systematic path forward]

Example (orchestrator):
"I hear you. Quick answer: Git tracks changes, so quality matters even for 1 line. BUT I can fast-track:
1. Tell me the file + change
2. I delegate to domain specialist (they validate + fix)
3. Usually <2 min total

Sound good? Or would you prefer I just handle it directly this time?"
```

**Your Frustration Response**:

```
**Signal Detection**: [How you identify user is frustrated]

**Response Adaptation**: [Acknowledge feeling, offer fast path, give user control/choice]
```

---

#### Signal 3: Enthusiasm → Depth Enhancement

**User Signal** (how you detect enthusiasm):
- [ ] Detailed follow-up questions
- [ ] "This is awesome! Tell me more..."
- [ ] "What about edge case X?"
- [ ] "Can I see the framework source?"
- [ ] Other: _______

**Example Signal**:
- User: "This is great! How does multi-agent synthesis work?"

**Agent Response Pattern** (how you adapt):

```
[Describe how agent provides deeper technical detail when user is enthusiastic]

Example (orchestrator):
"Great question! Synthesis triggers when 3+ agents return findings with >0.7 similarity overlap.

Process:
1. **Detect overlaps**: Semantic matching identifies duplicate findings
2. **Score solutions**: Apply weighted validation formula (Framework 5)
3. **Consolidate**: Present ranked recommendations with confidence scores

Want to see the complete synthesis-and-recommendation-framework.md?"
```

**Your Enthusiasm Response**:

```
**Signal Detection**: [How you identify user is enthusiastic/curious]

**Response Adaptation**: [Provide technical depth, edge cases, framework citations, offer more resources]
```

---

#### Signal 4: Overwhelm → Chunking

**User Signal** (how you detect overwhelm):
- [ ] "Too much information..."
- [ ] "Where do I even start?"
- [ ] Long silence after complex explanation
- [ ] "I don't have time to read all this"
- [ ] Other: _______

**Example Signal**:
- User: "This 990-line CLAUDE.md is overwhelming"

**Agent Response Pattern** (how you adapt):

```
[Describe how agent breaks information into manageable chunks]

Example (orchestrator):
"Totally fair - it's 990+ lines. Let's chunk it. **Start with one thing**: OODA Loop (lines 78-140).

Master that first (4 phases: Observe → Orient → Decide → Act). Everything else builds on OODA.

Read just that section (takes ~5 min), then come back. Sound manageable?"
```

**Your Overwhelm Response**:

```
**Signal Detection**: [How you identify user is overwhelmed]

**Response Adaptation**: [Break into chunks, suggest starting point, offer manageable next step]
```

---

#### Optional Signal 5: Expert-Level → Technical Depth

**User Signal** (how you detect expertise):
- [ ] Uses technical jargon correctly
- [ ] References framework concepts
- [ ] "Skip the explanation, I know X"
- [ ] Detailed edge case questions
- [ ] Other: _______

**Example Signal**:
- User: "What's the Context_Quality dimension weighting rationale?"

**Agent Response Pattern** (how you adapt):

```
[Describe how agent provides advanced technical detail for expert users]

Example (orchestrator):
"Good question. Weights are empirically tuned based on OODA failure analysis:
- **Domain (0.4)**: Highest weight because tech unfamiliarity causes 60% of implementation rework
- **Pattern (0.3)**: Second because 40% of bugs stem from reinventing existing patterns
- **Dependency (0.2)**: Integration issues cause 25% of refactors
- **Risk (0.1)**: Lowest because risk assessment improves with research, not upfront perfect knowledge

Weights derived from 200+ orchestrator decision retrospectives."
```

**Your Expert-Level Response** (optional):

```
**Signal Detection**: [How you identify user is expert-level]

**Response Adaptation**: [Provide formulas, rationale, trade-offs, academic references]
```

---

### Adaptation Rules

**Verbosity Adjustment Protocol**:

**Confusion / Overwhelm Detected** → Reduce verbosity:
- Shorter sentences (10-15 words max)
- Simple analogies instead of technical terms
- Break into bullet points
- Avoid jargon

**Enthusiasm / Expert-Level Detected** → Increase verbosity:
- Technical depth and edge cases
- Framework citations and references
- Trade-off discussions
- Formula derivations

**Standard (default)** → Moderate verbosity:
- Clear explanations with examples
- Balanced technical detail
- Confidence scores where appropriate

**Your Verbosity Rules**:

```
**Low Verbosity** (confusion/overwhelm): [Describe simplified approach]

**High Verbosity** (enthusiasm/expert): [Describe detailed approach]

**Standard Verbosity** (default): [Describe balanced approach]
```

---

### Escalation Protocol

**When user remains confused after multiple clarification attempts**:

**After 2 failed clarifications**:
- [ ] Try alternative explanation format (analogy, diagram, example)
- [ ] Ask: "Would it help if I explained this differently?"
- [ ] Offer: "Would you like me to just handle this for now, and we can revisit later?"

**After 3 failed clarifications**:
- [ ] Acknowledge: "This might not be clicking. That's ok."
- [ ] Offer choice: "(A) I handle this directly without framework, (B) You tell me exactly what to do. Your preference?"
- [ ] Escalate to different agent if domain mismatch suspected

**Your Escalation Protocol**:

```
**After 2 failed clarifications**: [What does agent try - alternative format, ask for feedback, offer to simplify]

**After 3 failed clarifications**: [How does agent acknowledge limitation, offer choice, escalate if needed]
```

---

**Signals & Adaptation Checklist**:

- [ ] User-Facing Check: Determined if agent needs this section (YES/NO)
- [ ] Signal 1 (Confusion → Simplification): Defined detection + response pattern
- [ ] Signal 2 (Frustration → Empathy): Defined detection + response pattern
- [ ] Signal 3 (Enthusiasm → Depth): Defined detection + response pattern
- [ ] Signal 4 (Overwhelm → Chunking): Defined detection + response pattern
- [ ] Optional Signal 5 (Expert → Technical): Defined detection + response pattern (if applicable)
- [ ] Verbosity Adjustment: Documented low/high/standard verbosity rules
- [ ] Escalation Protocol: Defined 2-clarification and 3-clarification escalation paths

---

## 10. Additional Context

### Security Considerations

**Instructions**: Any security-specific requirements or constraints?

**Examples**:

```
- Never expose file contents in reports (paths and line numbers only)
- Sanitize all user-provided inputs (file paths, regex patterns)
- Do not execute untrusted code during analysis
- Report storage must be readable only by authorized users
```

**Your Security Considerations** (optional):

```
[Security requirements, constraints, or concerns]
```

### Future Extensibility

**Instructions**: How might this agent evolve? What features might be added later?

**Examples**:

```
- Support for additional languages (JavaScript, Go, Rust)
- Custom rule authoring interface for project-specific patterns
- Integration with external vulnerability databases (CVE, NVD)
- Automated fix generation for common vulnerabilities
```

**Your Future Plans** (optional):

```
[Potential enhancements or extensions]
```

### Related Agents

**Instructions**: List existing agents this new agent is similar to, complements, or replaces.

**Examples**:

```
- Similar to: code-quality (both validate code quality)
- Complements: test-runner (security + correctness gates)
- Replaces: N/A (new capability)
```

**Your Related Agents** (optional):

```
[Similar, complementary, or superseded agents]
```

---

## 11. Model & Configuration

### Recommended Model

**Instructions**: Choose the Claude model based on task complexity.

- [ ] **sonnet** - Fast, efficient worker agent (simple, well-defined tasks)
- [ ] **sonnet** - Hybrid reasoning agent (complex decisions, multi-step workflows)

**Selected**: **\*\***\_\_\_**\*\***

**Selection Guidance**:

- Use **sonnet** (worker) for: Scanning, parsing, formatting, validation, simple analysis
- Use **sonnet** (hybrid) for: Planning, research, complex debugging, multi-agent coordination

### Color Identifier

**Instructions**: Choose a visual color for this agent (helps distinguish in logs/UI).

**Options**: `purple`, `blue`, `green`, `yellow`, `red`

**Selected**: **\*\***\_\_\_**\*\***

**Color Conventions**:

- **purple** - Research/analysis agents
- **blue** - Implementation/creation agents
- **green** - Validation/quality agents
- **yellow** - Warning/monitoring agents
- **red** - Critical/security agents

---

## 12. Completion Checklist

**Before submitting this template, verify**:

- [ ] Agent name follows `[domain]-[action]` format (kebab-case)
- [ ] Domain scope selected (`.claude/**`, `packages/**`, `docs/**`, `tests/**`, or `cross-domain`)
- [ ] Agent type selected (Creator, Reviewer, Enhancer, Runner, Analyzer, Planner)
- [ ] Orchestrator description written (1-3 sentences with trigger conditions)
- [ ] Core capabilities listed (3-7 specific, actionable items)
- [ ] Input/output contract defined (structure, types, validation)
- [ ] Success criteria and validation checks specified
- [ ] Model selected (sonnet or sonnet based on complexity)
- [ ] Color identifier chosen (purple, blue, green, yellow, red)

**Directory Structure Planning (Section 1A)**:
- [ ] Domain directory determined
- [ ] Documentation files planned (at least outline)
- [ ] At least 1 usage example planned
- [ ] Relevant frameworks identified

**Optional but recommended**:

- [ ] Domain knowledge specified (frameworks, standards, concepts)
- [ ] Tool requirements listed (with confidence and rationale)
- [ ] Integration points described (workflow, triggers, dependencies)
- [ ] Edge cases and error recovery documented
- [ ] Security considerations noted
- [ ] Future extensibility plans outlined

**OODA Loop & INFUSE Framework Compliance (Phase 1 Enhancements)**:

- [ ] **OODA Loop Integration (Section 5A)**: All 4 phases addressed
  - [ ] OBSERVE phase: Defined what agent parses/identifies
  - [ ] ORIENT phase: Specified Context_Quality assessment approach (4 dimensions)
  - [ ] ORIENT phase: Listed information hierarchy (4 priority levels)
  - [ ] ORIENT phase: Set Context_Quality threshold for proceeding
  - [ ] DECIDE phase: Documented decision framework (Main → Follow-up → Checkpoint)
  - [ ] DECIDE phase: Specified Agent Selection Confidence ranges (HIGH/MEDIUM/LOW)
  - [ ] ACT phase: Listed execution tools and workflows
  - [ ] ACT phase: Defined iteration protocol (threshold, max iterations, action)

- [ ] **Navigation Rules (Section 5B)**: Information hierarchy and limitation protocols defined
  - [ ] Information Hierarchy: Defined 4 priority levels (Primary → Secondary → Tertiary → Fallback)
  - [ ] Decision Protocol: Documented Main → Follow-up → Checkpoint workflow
  - [ ] Limitations Protocol: Selected handling strategy (Acknowledge/Report/Assume)
  - [ ] Limitations Protocol: Provided example limitation scenario with agent response
  - [ ] Escalation Path: Defined 3-step escalation (attempt 1 → attempt 2 → final escalation)

- [ ] **Signals & Adaptation (Section 9A)**: User-facing agents have emotional intelligence
  - [ ] User-Facing Check: Determined if agent needs this section (YES/NO)
  - [ ] IF YES: Signal 1 (Confusion → Simplification) defined
  - [ ] IF YES: Signal 2 (Frustration → Empathy) defined
  - [ ] IF YES: Signal 3 (Enthusiasm → Depth) defined
  - [ ] IF YES: Signal 4 (Overwhelm → Chunking) defined
  - [ ] IF YES: Verbosity Adjustment rules documented
  - [ ] IF YES: Escalation Protocol defined (2-clarification and 3-clarification paths)
  - [ ] IF NO: Confirmed as worker agent, section skipped appropriately

---

## 13. Usage Instructions

### How to Use This Template

1. **Fill Out Template**:
   - Save this template to a new file: `my-agent-definition.md`
   - Complete all required sections (marked with "**\*\***\_\_\_**\*\***")
   - Fill optional sections where you have knowledge

2. **Run Create Command**:

   ```bash
   /create-agent path/to/my-agent-definition.md
   ```

3. **Optional Flags**:

   ```bash
   # Provide additional context/documentation
   /create-agent my-agent-definition.md --context-dir=docs/security/

   # Preview without creating files (dry-run mode)
   /create-agent my-agent-definition.md --dry-run

   # Skip quality checks for rapid prototyping
   /create-agent my-agent-definition.md --skip-validation

   # Control template size (minimal, standard, comprehensive)
   /create-agent my-agent-definition.md --template=minimal
   ```

4. **What Happens Next**:
   - Command validates your input for completeness
   - **Creates agent directory**: `.claude/agents/{domain}/{{agent-name}}/`
   - **Creates subdirectories**: `docs/`, `examples/`, `schemas/`
   - Researches domain knowledge (if not provided)
   - Populates all directories with generated content
   - Provides usage examples and testing guidance

**Reference Template**: See `.claude/templates/agent-scaffold/` for directory structure.

5. **Review & Refine**:
   - Review generated agent definition
   - Test with sample inputs
   - Iterate and refine based on results

### Template Flags Explained

**`--context-dir=path/`**:

- Provides additional documentation for research
- Useful for domain-specific context (security policies, coding standards, etc.)
- Example: `--context-dir=docs/04-guides/security/`

**`--dry-run`**:

- Preview agent definition without creating files
- Validates input and shows research plan
- Safe for experimentation

**`--skip-validation`**:

- Bypasses quality checks (not recommended for production)
- Faster iteration during prototyping
- Use when you trust your input completely

**`--template=minimal|standard|comprehensive`**:

- **minimal**: ~8K tokens (core functionality only)
- **standard**: ~12K tokens (balanced, recommended)
- **comprehensive**: ~15K tokens (full documentation and examples)
- Controls agent definition verbosity

---

## 14. Examples

### Example 1: Security Scanner Agent

```markdown
## 1. Basic Information

Name: security-scanner
Domain Scope: packages/\*\* (main codebase)
Agent Type: Analyzer

## 2. Purpose & Description

Orchestrator Description:
"Performs static application security testing (SAST) on modified code using Semgrep to detect OWASP Top 10 vulnerabilities before commit. Integrates with git workflow as a parallel quality gate alongside code-quality. Triggers automatically when files in packages/\*\* are modified."

Value Proposition:
"Existing code-quality focuses on style and best practices but doesn't catch security vulnerabilities. This agent adds OWASP-focused security scanning to prevent CVEs from reaching production."

## 3. Core Capabilities

1. Scans Python code for SQL injection vulnerabilities using Semgrep OWASP ruleset
2. Detects insecure deserialization patterns and command injection risks
3. Validates authentication/authorization implementation against OWASP guidelines
4. Generates security reports with severity scoring and remediation steps
5. Integrates with pre-commit workflow as validation gate

## 4. Input/Output Contract

Expected Inputs:

- **files_to_scan**: List of absolute file paths (string[]) - must exist and be readable
- **scan_mode**: Enum ["fast", "comprehensive"] - determines ruleset selection
- **severity_threshold**: Enum ["critical", "high", "medium", "low"] - minimum severity to report

Expected Outputs (Success):
Security report (JSON) with:

- **findings**: Array of vulnerability objects (severity, confidence, location, remediation)
- **summary**: Aggregate counts by severity level
- **scan_metadata**: Files scanned, rules used, execution time

Expected Outputs (Failure):

- **failure_category**: Enum ["tool_error", "invalid_input", "file_access_error"]
- **error_details**: Specific error message and stack trace
- **recovery_suggestions**: Actionable steps to resolve issue
```

### Example 2: Test Dataset Creator Agent

```markdown
## 1. Basic Information

Name: test-dataset-creator
Domain Scope: tests/\*\* (test suite)
Agent Type: Creator

## 2. Purpose & Description

Orchestrator Description:
"Generates comprehensive test datasets for algorithm validation based on specification requirements. Parses SPEC.md files to extract input/output examples, edge cases, and validation criteria, then creates structured JSON test data files in tests/fixtures/."

Value Proposition:
"Manual test data creation is time-consuming and error-prone. This agent automates dataset generation from specifications, ensuring comprehensive coverage of edge cases and validation requirements."

## 3. Core Capabilities

1. Parses SPEC.md files to extract algorithm requirements and validation criteria
2. Generates synthetic test data covering happy path, edge cases, and error scenarios
3. Creates structured JSON fixtures with expected outputs for validation
4. Validates generated datasets against schema definitions
5. Documents test data provenance and generation methodology

## 4. Input/Output Contract

Expected Inputs:

- **spec_file_path**: Absolute path to SPEC.md file (string)
- **dataset_size**: Number of test cases to generate (integer, 10-1000)
- **coverage_mode**: Enum ["edge_cases", "comprehensive", "performance"]

Expected Outputs (Success):

- **dataset_file_path**: Path to generated JSON fixture file
- **test_case_count**: Number of cases generated (integer)
- **coverage_report**: Categories covered (dict with counts)

Expected Outputs (Failure):

- **failure_category**: Enum ["spec_parsing_error", "generation_error", "validation_error"]
- **error_details**: Specific error with line numbers
- **partial_results**: Any test cases generated before failure
```

---

## Support & Questions

**Need Help?**

- **📚 COMPREHENSIVE GUIDE**: `docs/04-guides/agent-creation-guide.md` (step-by-step instructions, examples, tips)
- Check `.claude/templates/agent.template.md` for full agent structure reference
- See existing agents in `.claude/agents/` for inspiration (30+ examples)
- Ask orchestrator: "How do I create an agent for [use case]?"

**Template Issues?**

- Report template problems to claude-code-ecosystem
- Suggest improvements via pull request
- Check `.claude/docs/changelog.md` for recent updates

---

**Template Version**: 1.0.0
**Last Updated**: 2025-10-22
**Compatible With**: Claude Code v1.0.111+, Template v5.0