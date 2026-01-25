# Delegation Patterns for /create-agent Command

**CRITICAL**: Use these EXACT Task() call patterns. Every phase delegates to sub-agents.

---

## Phase-to-Framework Mapping

| Phase | Cognitive Task | Framework | Why |
|-------|---------------|-----------|-----|
| **1: Parse & Validate** | Parse files, check preconditions | **ReACT** | Hypothesis -> Act -> Observe -> Refine |
| **2: Requirements** | Assess information needs | **Confidence-Based** | Score requirements by importance |
| **3: Context Analysis** | Extract from user files | **Structured Extraction** | Map to requirements |
| **4: Research Gaps** | Plan and execute research | **CAGEERF** | Context -> Analysis -> Goals -> Execution |
| **5: Documentation** | Generate AI-readable docs | **Template-Driven** | Consistent structure |
| **6: Schema Design** | Define input/output contract | **Contract-First** | Validation before implementation |
| **7: Agent Definition** | Generate agent file | **Simulation-Driven** | Think from agent perspective |
| **8: Quality Validation** | Multi-dimensional assessment | **Quality Matrix** | 9-dimension scoring |
| **9: Review** | User approval | **Pre-Mortem** | Anticipate issues before finalization |
| **10: Finalization** | Write files, update integrations | **Build-Measure-Learn** | Execute -> Verify -> Document |

**See**: `.claude/docs/00-core/frameworks/README.md`

---

## Phase 1: Parse & Validate

### Task 1: Parse Agent Definition

```
Task(
  subagent_type="researcher-codebase",
  prompt="PARSE AGENT DEFINITION FILE and extract structured information.

    File: [agent-definition-file-path]

    Extract and validate:
    1. Agent name (check format: [domain]-[action])
    2. Domain scope (.claude/**, packages/**, docs/**, cross-domain)
    3. Purpose (1-2 sentence orchestrator description)
    4. Core capabilities (list)
    5. Expected inputs (schema hints)
    6. Expected outputs (schema hints)
    7. Domain knowledge references (if any)
    8. Tool requirements (if any)
    9. Additional context (if any)

    Return structured JSON with all extracted fields and validation notes."
)
```

### Task 2: Check for Duplicates

```
Task(
  subagent_type="tech-debt-investigator",
  prompt="CHECK FOR DUPLICATE AGENTS with overlapping capabilities.

    Proposed Agent Name: [name from definition file]
    Proposed Capabilities: [list from definition file]

    Search existing agents in .claude/agents/ for:
    1. Exact name match
    2. Similar name patterns
    3. Overlapping capabilities
    4. Domain overlap

    Return JSON with:
    - is_duplicate: boolean
    - similar_agents: [list with similarity scores]
    - overlap_analysis: string
    - recommendation: 'proceed' | 'rename' | 'merge_with_existing'"
)
```

---

## Phase 2: Assess Requirements

```
Task(
  subagent_type="context-readiness-assessor",
  prompt="ASSESS INFORMATION REQUIREMENTS for new agent creation.

    Agent Definition:
    - Name: [name]
    - Domain: [domain]
    - Purpose: [purpose]
    - Capabilities: [list]

    Determine what information this agent needs to know:
    1. Domain expertise required (frameworks, methodologies, standards)
    2. Technical concepts needed (patterns, algorithms, architectures)
    3. Processes/workflows agent will execute
    4. Tool usage patterns and best practices
    5. Integration points with other agents/systems

    For each information requirement, provide:
    - Topic name
    - Confidence score (0.0-1.0) indicating importance
    - Rationale for why this information is needed
    - Specificity level (broad topic vs. specific subtopic)

    Return structured JSON with categorized requirements and confidence scores."
)
```

---

## Phase 3: Analyze Context

**Only if --context-dir provided**

```
Task(
  subagent_type="researcher-codebase",
  prompt="ANALYZE USER-PROVIDED CONTEXT for agent creation.

    Context Directory: [context-dir-path]
    Information Requirements: [list from Phase 2]

    Extract from user-provided files:
    1. Frameworks mentioned (with descriptions)
    2. Processes/workflows described
    3. Tool requirements and usage patterns
    4. Domain-specific knowledge and terminology
    5. Best practices and standards
    6. Examples and code patterns

    Map each finding to information requirements from Phase 2:
    - Which requirements are fully covered?
    - Which are partially covered?
    - Which have no coverage?

    Return structured JSON with:
    - covered_requirements: [list with coverage scores]
    - extracted_frameworks: [list]
    - extracted_processes: [list]
    - gap_analysis: {requirement: coverage_score}"
)
```

---

## Phase 4: Research Gaps

### Task 1: Create Research Plan

**CRITICAL**: Use exact phrase "CREATE A RESEARCH PLAN for"

```
Task(
  subagent_type="researcher-lead",
  prompt="CREATE A RESEARCH PLAN for agent creation information gaps.

    Agent Being Created: [name]
    Domain: [domain]

    Information Gaps (from Phase 3):
    [List of gaps with context]

    For each gap:
    1. Convert broad topic to 2-3 specific research queries
    2. Determine research strategy (breadth-first vs depth-first)
    3. Assign research source type (web, library docs, codebase patterns)
    4. Estimate worker count and parallel execution plan

    Focus on:
    - Frameworks and methodologies (structured approaches)
    - Processes and workflows (step-by-step procedures)
    - Best practices and standards (industry guidance)
    - Integration patterns (how this fits with existing systems)

    Return delegation_plans with worker assignments and specific prompts.
    DO NOT EXECUTE RESEARCH - ONLY CREATE THE PLAN."
)
```

### Task 2: Execute Research Workers

Spawn from plan (max 5 simultaneously):

```
Task(
  subagent_type="researcher-external",
  prompt="[Specific research query from plan]
    Focus on: [frameworks/processes/patterns]
    Sources: [recommended sources from plan]"
)

Task(
  subagent_type="researcher-external",
  prompt="[Specific library documentation query]
    Library: [library name]
    Topics: [specific API/patterns needed]"
)

Task(
  subagent_type="researcher-codebase",
  prompt="[Specific codebase pattern search]
    Pattern: [what to look for]
    Files: [scope]"
)
```

---

## Phase 5: Generate Documentation

For each category with findings (parallel, max 5):

```
Task(
  subagent_type="documentation",
  prompt="GENERATE AI-READABLE DOCUMENTATION from research findings.

    Category: [planning|development|testing|review|security|domain-specific]
    Agent Name: [agent-name]
    Template: .claude/templates/agent-documentation.template.md

    Research Findings:
    [Relevant findings for this category]

    Use the AI-readable documentation template to create:
    1. Overview (1-2 sentence summary)
    2. Core Frameworks (structured with Purpose/When to Use/How to Apply/Example)
    3. Processes & Workflows (step-by-step with rationale)
    4. Decision Trees (condition -> action mappings)
    5. Anti-Patterns (what to avoid with alternatives)
    6. Integration Points (how this connects to other components)

    Output file path: .claude/agents/{domain}/{agent-name}/docs/[category]-[topic].md

    Follow template structure exactly for AI readability.
    Include sources with URLs for provenance."
)
```

### Update Indices

```
Task(
  subagent_type="documentation",
  prompt="UPDATE DOCUMENTATION INDICES for new agent documentation.

    New Documentation Files:
    [List of generated files]

    Update:
    1. .claude/docs/DOC-INDEX.md (add entries under appropriate category)
    2. .claude/docs/01-guides/agents/agent-categorization.md (add agent to category)

    Maintain alphabetical ordering and consistent formatting."
)
```

---

## Phase 6: Design Schema

```
Task(
  subagent_type="claude-code-ecosystem",
  prompt="DESIGN INPUT/OUTPUT SCHEMA for new agent.

    Agent Definition:
    - Name: [name]
    - Capabilities: [list]
    - Expected Inputs: [from Phase 1 parsed definition]
    - Expected Outputs: [from Phase 1 parsed definition]

    Analyze capabilities to determine:
    1. Input structure:
       - Required fields (context, operation_type, etc.)
       - Optional parameters (flags, configuration)
       - Multiple operation types? (like claude-code-ecosystem: create, evaluate, update)

    2. Output structure:
       - SUCCESS state: What deliverables, changes, artifacts?
       - FAILURE state: What error types, recovery steps?
       - Metadata: confidence, sources, recommendations?

    Generate JSON Schema file that:
    - Extends base-agent.schema.json
    - Defines agent_specific_output structure
    - Defines failure_details structure
    - Includes descriptions for all fields
    - Validates against JSON Schema Draft 07

    Output file: .claude/agents/{domain}/{agent-name}/schemas/{agent-name}.schema.json"
)
```

---

## Phase 7: Create Agent Definition

```
Task(
  subagent_type="claude-code-ecosystem",
  prompt="CREATE NEW AGENT DEFINITION using template and simulation-driven development.

    Agent Requirements:
    - Name: [name]
    - Domain: [domain]
    - Purpose: [purpose]
    - Capabilities: [list from Phase 1]

    Documentation References (generated in Phase 5):
    [List all .claude/agents/{domain}/{agent-name}/docs/*.md files]

    Schema File: .claude/agents/{domain}/{agent-name}/schemas/{agent-name}.schema.json

    Tool Recommendations (with confidence and rationale):
    [Orchestrator-provided recommendations]
    - Read (confidence: 1.0, rationale: All agents need to read files)
    - Write (confidence: 0.9, rationale: Agent creates X files)
    - Bash (confidence: 0.6, rationale: May need to execute Y commands)

    Instructions:
    1. Use simulation-driven development (think from agent's perspective)
    2. Apply .claude/templates/agent.template.md structure
    3. Apply base pattern inheritance (reference base-agent-pattern.md)
    4. Reference frameworks from documentation in appropriate sections
    5. Include tool usage patterns with rationale
    6. Create clear orchestrator description (1-2 sentences, when to call)
    7. Follow all template requirements (YAML frontmatter, section ordering, etc.)

    Output: .claude/agents/{domain}/{agent-name}/{agent-name}.md"
)
```

---

## Phase 8: Quality Validation (5 Parallel Tasks)

### Validator 1: Template Compliance

```
Task(
  subagent_type="claude-code-ecosystem",
  prompt="VALIDATE TEMPLATE COMPLIANCE for new agent.

    Agent File: .claude/agents/{domain}/{agent-name}/{agent-name}.md
    Template: .claude/templates/agent.template.md (or agent-scaffold/ structure)

    Check:
    1. YAML frontmatter on line 1 (not lines 1-22 warnings)
    2. Tools field is comma-separated string (not YAML list)
    3. All 19 sections present in correct order
    4. Base pattern references included
    5. Schema reference included
    6. File operation protocol referenced

    Return validation report with pass/fail per check."
)
```

### Validator 2: Documentation Health

```
Task(
  subagent_type="documentation",
  prompt="VALIDATE DOCUMENTATION HEALTH for new agent.

    Agent File: .claude/agents/{domain}/{agent-name}/{agent-name}.md
    Generated Docs: .claude/agents/{domain}/{agent-name}/docs/*.md (from Phase 5)
    Schema File: .claude/agents/{domain}/{agent-name}/schemas/{agent-name}.schema.json

    Check:
    1. Documentation structure (all Phase 5 files exist)
    2. Internal link integrity (all markdown links resolve)
    3. Cross-reference validity (references to guides are correct)
    4. Naming conventions (kebab-case.md standard)
    5. Organization compliance (DOCS-MANAGEMENT.md rules)

    Return health report with:
    - health_score (0-100)
    - broken_links: [list]
    - missing_files: [list]
    - naming_violations: [list]
    - organization_issues: [list]
    - recommendations: [list]"
)
```

### Validator 3: Prompt Quality

```
Task(
  subagent_type="claude-code-ecosystem",
  prompt="EVALUATE PROMPT QUALITY for new agent.

    Agent File: .claude/agents/{domain}/{agent-name}/{agent-name}.md
    Schema File: .claude/agents/{domain}/{agent-name}/schemas/{agent-name}.schema.json

    Evaluate across 4 frameworks:
    1. Structural Quality: Clarity, modularity, reasonable length
    2. Prompt Engineering: Best practices, implicit context handling
    3. Token Optimization: Redundancy, compression opportunities
    4. Testing Strategy: Validation approach, quality gates

    Return evaluation report with:
    - framework_scores: {structural, engineering, tokens, testing}
    - anti_patterns: [list with severity: high/medium/low]
    - optimization_opportunities: [list with quantified impact]
    - improvement_roadmap: [prioritized recommendations]
    - confidence_scores: [0.0-1.0 per recommendation]"
)
```

### Validator 4: Context Optimization

```
Task(
  subagent_type="context-optimizer",
  prompt="ANALYZE CONTEXT USAGE for new agent.

    Agent File: .claude/agents/{domain}/{agent-name}/{agent-name}.md
    Generated Docs: .claude/agents/{domain}/{agent-name}/docs/*.md
    Template: .claude/templates/agent-scaffold/ (directory-based structure)
    Base Pattern: .claude/docs/01-guides/agents/base-agent-pattern.md

    Analyze:
    1. Current token count for agent definition
    2. Redundancy with base-agent-pattern.md
    3. Redundancy with generated documentation
    4. Documentation reference opportunities
    5. Optimization potential with ROI

    Return optimization report with:
    - current_tokens: number
    - optimized_tokens: number (if recommendations applied)
    - potential_savings: number
    - redundancy_analysis: [list with overlap percentages]
    - reference_opportunities: [list with token savings]
    - optimization_roadmap: [prioritized by ROI]"
)
```

### Validator 5: Quality Matrix

```
Task(
  subagent_type="claude-code-ecosystem",
  prompt="EVALUATE AGENT QUALITY using 9-dimensional matrix.

    Agent File: .claude/agents/{domain}/{agent-name}/{agent-name}.md

    Score each dimension (0-5 scale):
    1. Role clarity and boundary definition
    2. Schema integration quality
    3. Reasoning approach sophistication
    4. Tool usage appropriateness
    5. Error recovery completeness
    6. Output optimization
    7. Integration point clarity
    8. Documentation references
    9. Validation coverage

    Calculate weighted score: (sum x weights) / 45 x 100

    Return quality report with scores and recommendations."
)
```

---

## Phase 9: Generate Summary

```
Task(
  subagent_type="planning",
  prompt="GENERATE EXECUTIVE SUMMARY for agent review.

    Agent File: .claude/agents/{domain}/{agent-name}/{agent-name}.md
    Quality Report: [from Phase 8]
    Documentation: [list of doc files from .claude/agents/{domain}/{agent-name}/docs/]
    Schema: .claude/agents/{domain}/{agent-name}/schemas/{agent-name}.schema.json

    Create user-friendly summary:
    1. Agent name and type (Creator/Reviewer/Enhancer/etc.)
    2. Orchestrator description (when to call this agent)
    3. Core capabilities with confidence scores
    4. Tools assigned with rationale
    5. Documentation created (count of frameworks/processes)
    6. Quality score and key strengths
    7. Recommendations for improvement (if any)

    Format for clarity with sections."
)
```

### Apply Refinements (if user requests)

```
Task(
  subagent_type="claude-code-ecosystem",
  prompt="APPLY USER REFINEMENTS to agent definition.

    Agent File: .claude/agents/{domain}/{agent-name}/{agent-name}.md

    User Feedback:
    [Specific refinements requested]

    Apply changes while maintaining:
    - Template compliance
    - Base pattern inheritance
    - Documentation references
    - Quality standards

    Return updated agent file."
)
```

---

## Phase 10: Update Integrations

```
Task(
  subagent_type="claude-code-ecosystem",
  prompt="UPDATE INTEGRATION POINTS for new agent.

    Agent Name: [name]
    Agent File: .claude/agents/{domain}/{agent-name}/{agent-name}.md
    Agent Type: [Creator/Reviewer/etc.]
    Domain: [domain]

    Update:
    1. CLAUDE.md delegation table (lines 639-666)
       - Add row with agent, domain scope, use case, type
    2. .claude/docs/orchestrator-workflow.md agent legend
       - Add entry with description
    3. .claude/docs/01-guides/agents/agent-categorization.md
       - Add to appropriate category
    4. .claude/docs/DOC-INDEX.md (if not already updated)

    Maintain alphabetical ordering and consistent formatting.
    Return list of files updated."
)
```

### Generate Handoff

```
Task(
  subagent_type="planning",
  prompt="GENERATE HANDOFF SUMMARY for agent creation completion.

    Agent Name: [name]
    Files Created: [list]
    Files Updated: [list]
    Quality Score: [score]

    Create summary with:
    1. Files Created section (with paths)
    2. Integrations Updated section (with files)
    3. Quality Metrics section (scores, validations)
    4. Next Steps section (restart session, test agent, monitor)
    5. Usage Example (how orchestrator calls this agent)

    Format with clear sections, actionable next steps."
)
```

---

## Agent Assignment Summary

| Phase | Task | Agent | Rationale |
|-------|------|-------|-----------|
| 1 | Parse definition | researcher-codebase | File analysis |
| 1 | Validate preconditions | Orchestrator (inline) | .claude/ directory checks |
| 1 | Check duplicates | tech-debt-investigator | Duplicate detection |
| 2 | Assess requirements | context-readiness-assessor | Context needs |
| 3 | Analyze context | researcher-codebase | File analysis |
| 4 | Create plan | researcher-lead | Research planning |
| 4 | Execute research | researcher-*/multiple | Parallel research |
| 5 | Generate docs | documentation | Documentation org |
| 5 | Update indices | documentation | Index maintenance |
| 6 | Design schema | claude-code-ecosystem | Schema creation |
| 7 | Create agent | claude-code-ecosystem | Agent generation |
| 8 | Validate template | claude-code-ecosystem | Template validation |
| 8 | Validate documentation | documentation | Documentation health |
| 8 | Evaluate prompt quality | claude-code-ecosystem | Prompt engineering analysis |
| 8 | Analyze context usage | context-optimizer | Token budget analysis |
| 8 | Quality evaluation | claude-code-ecosystem | Quality matrix |
| 9 | Generate summary | planning | Executive summary |
| 9 | Apply refinements | claude-code-ecosystem | Feedback application |
| 10 | Update integrations | claude-code-ecosystem | Integration updates |
| 10 | Generate handoff | planning | User documentation |
