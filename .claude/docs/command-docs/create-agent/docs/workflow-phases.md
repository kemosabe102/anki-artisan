# Create-Agent Workflow Phases

*Detailed documentation for the 12-phase agent creation workflow*

---

## OODA Phase Mapping

| OODA Phase | Workflow Phases | Purpose | Gate |
|------------|-----------------|---------|------|
| OBSERVE | 1-2 | Parse input, detect duplicates | CQ >= 0.7 |
| ORIENT | 3-5 | Assess requirements, research gaps | CQ >= 0.85 |
| DECIDE | 6-7 | Design schema, generate definition | Self-score >= 70 |
| ACT | 8-12 | Test, validate, document, approve, finalize | All gates pass |

---

## Phase Overview

```text
PHASE 1: PARSE & VALIDATE [ReACT]
  |-- Parse definition file, validate structure
  
PHASE 2: DUPLICATE DETECTION [5 Whys]
  |-- Check for existing similar agents
  |-- HUMAN DECISION: If duplicate found

PHASE 3: REQUIREMENTS ASSESSMENT [Cynefin]
  |-- Classify problem complexity, calculate CQ
  |-- HUMAN DECISION: Approve research scope

PHASE 4: RESEARCH PLANNING [CAGEERF]
  |-- Create targeted research plan

PHASE 5: RESEARCH EXECUTION [ReACT]
  |-- Execute parallel research workers
  |-- GATE: CQ >= 0.85 (max 2 iterations)

PHASE 6: SCHEMA DESIGN [First Principles]
  |-- Design input/output JSON schema

PHASE 7: AGENT DEFINITION [CAGEERF]
  |-- Generate agent definition with self-evaluation
  |-- GATE: Self-score >= 70/100

PHASE 8: SIMULATION TESTING [Build-Measure-Learn] (NEW)
  |-- Generate test prompts, simulate execution
  |-- GATE: All 3 simulations pass

PHASE 9: QUALITY VALIDATION [DMAIC]
  |-- 5 parallel validators
  |-- GATE: template=100% AND aggregate>=70 AND no HIGH-severity

PHASE 10: DOCUMENTATION [SCAMPER]
  |-- Optimize and organize documentation

PHASE 11: REVIEW & APPROVAL [Disney Creative Strategy]
  |-- Multi-perspective review
  |-- HUMAN DECISION: approve | refine | cancel

PHASE 12: FINALIZATION [Pre-Mortem]
  |-- Write files, generate handoff
  |-- Rollback plan if failure
```

---

## Phase 1: PARSE & VALIDATE [ReACT]

**Purpose**: Extract structured information from user's agent definition file and validate all required sections are present.

**Agent(s)**: researcher-codebase

**Inputs**:
- Agent definition file path (from $ARGUMENTS)
- Template structure reference (`.claude/templates/agent-definition-input.template.md`)

**Process (ReACT Framework)**:
1. **THINK**: What sections does the agent definition template require?
   - Identify REQUIRED vs OPTIONAL sections
   - Prepare validation checklist
2. **ACT**: Parse the input file
   - Read file contents
   - Extract each section by header
   - Map to structured data
3. **OBSERVE**: Validate extracted data
   - Check REQUIRED sections present: Purpose, Capabilities, Tools
   - Verify section content is substantive (not placeholder)
   - Note any gaps or warnings
4. **REFINE**: Flag gaps and prepare for next phase
   - List missing REQUIRED sections (blocking)
   - List missing OPTIONAL sections (warning)
   - Calculate parse confidence score

**Outputs/Deliverables**:
```json
{
  "parsed_definition": {
    "name": "string",
    "domain": "string",
    "purpose": "string",
    "capabilities": ["string"],
    "tools": ["string"],
    "inputs": {},
    "outputs": {}
  },
  "validation_result": "PASS | FAIL",
  "missing_required": [],
  "missing_optional": [],
  "parse_confidence": 0.0-1.0
}
```

**Gate Condition**: 
- All REQUIRED sections present (Purpose, Capabilities, Tools)
- Parse confidence >= 0.7

**Error Handling**:
- If REQUIRED section missing: Return FAILURE with specific gaps, suggest template reference
- If file not found: Return FAILURE with path validation error
- If malformed markdown: Attempt recovery, flag sections that couldn't parse

**TodoWrite Checkpoint**:
```
Phase 1: PARSE & VALIDATE - [COMPLETE|IN_PROGRESS|BLOCKED]
  - Parsed: [agent-name]
  - Validation: [PASS|FAIL]
  - Gaps: [list or "none"]
```

---

## Phase 2: DUPLICATE DETECTION [5 Whys]

**Purpose**: Identify if a similar agent already exists to prevent ecosystem fragmentation and wasted effort.

**Agent(s)**: tech-debt-investigator

**Inputs**:
- Parsed definition from Phase 1
- Agent ecosystem: `.claude/agents/**/*.md`

**Process (5 Whys Framework)**:
1. **Why might this agent already exist?**
   - Search for exact name matches in `.claude/agents/`
   - Check for similar naming patterns (synonyms, abbreviations)
   
2. **Why would existing agents overlap?**
   - Compare capabilities list against existing agents
   - Calculate capability overlap percentage
   
3. **Why is the domain scope similar?**
   - Match domain boundaries (`.claude/**`, `packages/**`, etc.)
   - Identify agents with same domain + similar type
   
4. **Why would users call the wrong agent?**
   - Compare purpose statements for semantic similarity
   - Identify ambiguous differentiation
   
5. **Why should this be a separate agent vs enhancement?**
   - Assess if capabilities could extend existing agent
   - Evaluate complexity of enhancement vs new creation

**Outputs/Deliverables**:
```json
{
  "duplicate_check": {
    "exact_match": null | "agent-name",
    "similar_agents": [
      {
        "name": "string",
        "similarity_score": 0.0-1.0,
        "overlap_areas": ["capabilities", "domain", "purpose"],
        "recommendation": "DUPLICATE | SIMILAR | DISTINCT"
      }
    ],
    "highest_similarity": 0.0-1.0,
    "recommendation": "PROCEED | MERGE | RENAME | CANCEL"
  }
}
```

**Gate Condition**:
- No agent with similarity > 0.8 (or user override)
- If similarity 0.6-0.8: Warning presented, user decides

**Error Handling**:
- If exact duplicate found: Present options (Enhance existing, Rename new, Cancel)
- If high similarity (>0.8): HUMAN DECISION required before proceeding

**Human Decision Point**:
```text
Similar agent detected: code-quality (similarity: 0.82)

Overlap areas:
- Domain: packages/** (SAME)
- Capabilities: 3 of 5 overlap
- Purpose: Both analyze Python code quality

Options:
1. [E] Enhance existing - Add capabilities to code-quality
2. [R] Rename & differentiate - Proceed with clearer differentiation
3. [P] Proceed anyway - Create despite similarity (not recommended)
4. [C] Cancel - Abort agent creation

Choose [E/R/P/C]:
```

**TodoWrite Checkpoint**:
```
Phase 2: DUPLICATE DETECTION - [COMPLETE|IN_PROGRESS|BLOCKED]
  - Highest similarity: [score] with [agent-name]
  - Recommendation: [PROCEED|MERGE|RENAME|CANCEL]
  - User decision: [if applicable]
```

---

## Phase 3: REQUIREMENTS ASSESSMENT [Cynefin]

**Purpose**: Classify the problem complexity and identify what domain knowledge, frameworks, and processes the agent needs.

**Agent(s)**: context-readiness-assessor

**Inputs**:
- Parsed definition from Phase 1
- Duplicate check results from Phase 2
- Existing agent patterns for comparison

**Process (Cynefin Framework)**:
1. **OBSERVE**: Gather problem characteristics
   - What domain does this agent operate in?
   - What expertise level is required?
   - What tools and integrations are needed?

2. **CLASSIFY** the problem type:
   - **SIMPLE**: Best practice exists, cause-effect clear
     - Example: File formatting agent (well-defined rules)
     - Strategy: Direct execution with existing patterns
   - **COMPLICATED**: Analysis needed, expertise required
     - Example: Code review agent (requires domain knowledge)
     - Strategy: Expert research, pattern discovery
   - **COMPLEX**: Unknowns, emergence likely
     - Example: AI behavior prediction agent (novel domain)
     - Strategy: Probe-sense-respond, extensive research
   - **CHAOTIC**: No patterns, crisis response
     - Example: Incident response agent (unpredictable scenarios)
     - Strategy: Act-sense-respond, build flexibility

3. **ASSESS** Context Quality dimensions:
   - Domain (0.0-1.0): Understanding of agent's problem space
   - Pattern (0.0-1.0): Existing patterns to follow
   - Dependency (0.0-1.0): Integration points clarity
   - Risk (0.0-1.0): Failure modes understood

**Outputs/Deliverables**:
```json
{
  "complexity_classification": "SIMPLE | COMPLICATED | COMPLEX | CHAOTIC",
  "context_quality": {
    "domain": 0.0-1.0,
    "pattern": 0.0-1.0,
    "dependency": 0.0-1.0,
    "risk": 0.0-1.0,
    "aggregate": 0.0-1.0
  },
  "information_requirements": [
    {
      "topic": "string",
      "priority": "HIGH | MEDIUM | LOW",
      "confidence": 0.0-1.0,
      "source_hint": "codebase | web | library"
    }
  ],
  "research_scope": "MINIMAL | STANDARD | EXTENSIVE"
}
```

**Gate Condition**:
- CQ >= 0.7 to proceed (lower threshold than implementation)
- If CQ < 0.7: Expand research scope, iterate

**Error Handling**:
- If classification unclear: Default to COMPLICATED (safe middle ground)
- If CQ extremely low (<0.5): Flag as high-risk, recommend user consultation

**Human Decision Point**:
```text
Requirements Assessment Complete

Complexity: COMPLICATED
Context Quality: 0.72

Research Scope Recommendation: STANDARD
- 3 research topics identified
- Estimated time: 5-8 minutes

Information Requirements:
1. [HIGH] Python profiling frameworks (confidence: 0.45)
2. [HIGH] Memory analysis patterns (confidence: 0.52)
3. [MEDIUM] Integration with existing debugger (confidence: 0.78)

Options:
1. [A] Accept scope - Proceed with STANDARD research
2. [E] Expand scope - Add topics or increase depth
3. [R] Reduce scope - Skip MEDIUM priority items
4. [S] Skip research - Use existing knowledge only (RISK)

Choose [A/E/R/S]:
```

**TodoWrite Checkpoint**:
```
Phase 3: REQUIREMENTS ASSESSMENT - [COMPLETE|IN_PROGRESS|BLOCKED]
  - Complexity: [classification]
  - CQ: [aggregate score]
  - Research scope: [MINIMAL|STANDARD|EXTENSIVE]
  - Topics: [count] identified
```

---

## Phase 4: RESEARCH PLANNING [CAGEERF]

**Purpose**: Create a targeted research plan with specific questions and worker assignments.

**Agent(s)**: researcher-lead

**Inputs**:
- Information requirements from Phase 3
- Research scope (MINIMAL/STANDARD/EXTENSIVE)
- User-approved topics

**Process (CAGEERF Framework)**:
1. **CONTEXT**: Understand what we're researching
   - Agent domain and purpose
   - Gaps identified in Phase 3
   - Existing knowledge baseline

2. **ANALYSIS**: Break down research needs
   - Categorize by source type (codebase/web/library)
   - Identify dependencies between topics
   - Estimate effort per topic

3. **GOALS**: Define success criteria
   - Target confidence per topic (>= 0.85)
   - Maximum iterations (2)
   - Time budget per worker

4. **EXECUTION**: Plan worker assignments
   - researcher-codebase: Internal patterns, existing agents
   - researcher-external: External frameworks, best practices, API documentation, library usage

5. **EVALUATION**: Define measurement criteria
   - How to assess research quality
   - When to iterate vs proceed
   - Confidence aggregation method

6. **REFINEMENT**: Build iteration strategy
   - Fallback questions if primary fails
   - Alternative sources per topic

7. **FRAMEWORK**: Structure the plan
   - Worker assignments with specific prompts
   - Parallelization strategy
   - Synthesis approach

**Outputs/Deliverables**:
```json
{
  "research_plan": {
    "workers": [
      {
        "agent": "researcher-codebase | researcher-external",
        "questions": ["string (max 3)"],
        "focus_areas": ["string"],
        "success_criteria": "string",
        "time_budget": "seconds"
      }
    ],
    "parallelization": "ALL_PARALLEL | SEQUENTIAL | PHASED",
    "synthesis_strategy": "MERGE | PRIORITIZE | DEDUPE",
    "max_workers": 5,
    "max_questions_per_worker": 3
  }
}
```

**Gate Condition**:
- Plan has <= 5 workers
- <= 3 questions per worker
- All HIGH priority topics covered

**Error Handling**:
- If too many topics: Prioritize by information requirement priority
- If no suitable source: Flag topic for user-provided context

**TodoWrite Checkpoint**:
```
Phase 4: RESEARCH PLANNING - [COMPLETE|IN_PROGRESS|BLOCKED]
  - Workers planned: [count]
  - Questions total: [count]
  - Parallelization: [strategy]
```

---

## Phase 5: RESEARCH EXECUTION [ReACT]

**Purpose**: Execute the research plan with parallel workers, iterating until confidence threshold met.

**Agent(s)**: researcher-codebase, researcher-external (parallel)

**Inputs**:
- Research plan from Phase 4
- Context from Phase 3

**Process (ReACT Framework - per worker)**:
1. **THINK**: Form hypothesis based on research question
   - What do we expect to find?
   - What sources are most likely to help?
   - What would high-confidence answer look like?

2. **ACT**: Execute specific investigation
   - researcher-codebase: Grep patterns, read agent files, analyze structures
   - researcher-external: Search authoritative sources, gather best practices, query Context7, fetch API documentation

3. **OBSERVE**: Analyze results
   - Did we find relevant information?
   - What's the confidence level?
   - Are there gaps or contradictions?

4. **REFINE**: Update understanding, iterate if needed
   - If confidence < 0.85 AND iterations < 2: Refine query, retry
   - If confidence >= 0.85: Mark complete
   - If iterations exhausted: Proceed with best findings

**Outputs/Deliverables**:
```json
{
  "research_results": {
    "findings": [
      {
        "topic": "string",
        "content": "string",
        "confidence": 0.0-1.0,
        "sources": ["string"],
        "iterations_used": 1-2
      }
    ],
    "aggregate_confidence": 0.0-1.0,
    "gaps_remaining": ["string"],
    "frameworks_discovered": ["string"],
    "patterns_found": ["string"]
  }
}
```

**Gate Condition**:
- Aggregate CQ >= 0.85
- Maximum 2 iterations per topic
- All HIGH priority topics have findings

**Error Handling**:
- If worker fails: Retry once with refined query
- If topic has no findings after 2 iterations: Flag gap, proceed with warning
- If aggregate CQ < 0.85 after 2 rounds: Proceed with best findings, document risk

**Iteration Protocol**:
```text
Round 1: Execute all workers in parallel
  |-- Collect results
  |-- Calculate aggregate CQ
  |-- If CQ >= 0.85: PROCEED to Phase 6
  |-- If CQ < 0.85: Identify lowest-confidence topics

Round 2 (if needed): Targeted follow-up
  |-- Spawn 1-2 workers for gap topics only
  |-- Use refined queries based on Round 1 learnings
  |-- Collect results, recalculate CQ
  |-- PROCEED to Phase 6 (regardless of CQ, document gaps)
```

**TodoWrite Checkpoint**:
```
Phase 5: RESEARCH EXECUTION - [COMPLETE|IN_PROGRESS|BLOCKED]
  - Workers executed: [count]
  - Iterations: [1|2]
  - Aggregate CQ: [score]
  - Gaps: [list or "none"]
```

---

## Phase 6: SCHEMA DESIGN [First Principles]

**Purpose**: Design the input/output JSON schema by reasoning from fundamental requirements.

**Agent(s)**: claude-code-ecosystem

**Inputs**:
- Parsed definition from Phase 1
- Research findings from Phase 5
- Base schema: `.claude/agents/dev-tools/schemas/base-agent.schema.json`

**Process (First Principles Framework)**:
1. **IDENTIFY**: What is the schema problem at its most basic level?
   - What data does the agent receive?
   - What data does the agent produce?
   - What states can the agent be in?

2. **QUESTION**: What assumptions are being made?
   - Do we need all fields from base schema?
   - What's truly required vs nice-to-have?
   - What types best represent the data?

3. **DECOMPOSE**: Break down to fundamental truths
   - Input: context + parameters + operation_type
   - Output: status + deliverables + metadata
   - Failure: error_type + recovery_steps + context

4. **RECONSTRUCT**: Build schema from fundamentals
   - Start with absolute minimum viable schema
   - Add fields only with clear justification
   - Ensure each field has description and type

5. **VALIDATE**: Does the schema serve the agent's purpose?
   - Can all capabilities be expressed with this schema?
   - Are error cases properly represented?
   - Does it extend base-agent.schema.json correctly?

**Outputs/Deliverables**:
```json
{
  "schema": {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "agent-name Input/Output Schema",
    "allOf": [
      { "$ref": "base-agent.schema.json" }
    ],
    "properties": {
      "agent_specific_output": {
        "type": "object",
        "properties": {},
        "required": []
      },
      "failure_details": {
        "type": "object",
        "properties": {},
        "required": []
      }
    }
  },
  "validation_result": "VALID | INVALID",
  "schema_path": ".claude/agents/{domain}/{agent-name}/schemas/{agent-name}.schema.json"
}
```

**Gate Condition**:
- Schema validates against JSON Schema draft-07
- All required base-agent fields inherited
- agent_specific_output defined
- failure_details defined

**Error Handling**:
- If validation fails: Show specific errors, iterate on schema
- If base schema not found: Fail with clear error message
- If schema too complex (>50 properties): Warn and suggest simplification

**TodoWrite Checkpoint**:
```
Phase 6: SCHEMA DESIGN - [COMPLETE|IN_PROGRESS|BLOCKED]
  - Schema validation: [VALID|INVALID]
  - Properties defined: [count]
  - Path: [schema file path]
```

---

## Phase 7: AGENT DEFINITION [CAGEERF]

**Purpose**: Generate the complete agent definition file with mandatory self-evaluation before proceeding.

**Agent(s)**: claude-code-ecosystem

**Inputs**:
- Parsed definition from Phase 1
- Research findings from Phase 5
- Schema from Phase 6
- Template: `.claude/templates/agent.template.md`

**Process (CAGEERF Framework)**:
1. **CONTEXT**: Gather all inputs
   - User's original definition
   - Research findings and frameworks
   - Schema design
   - Similar agents for reference

2. **ANALYSIS**: Break down the agent structure
   - Map capabilities to workflow phases
   - Identify tool requirements per capability
   - Determine delegation patterns

3. **GOALS**: Define what success looks like
   - All 19 template sections populated
   - Orchestrator description clear and differentiating
   - Workflow executable by sub-agent

4. **EXECUTION**: Generate the definition
   - Apply template structure
   - Reference frameworks from research
   - Include tool usage patterns with rationale
   - Create clear error handling

5. **EVALUATION**: Self-score the generated agent (MANDATORY)
   - Score across 9 quality dimensions
   - Calculate aggregate score
   - Identify weakest areas

6. **REFINEMENT**: Improve if score < 70
   - Address lowest-scoring dimensions
   - Iterate until score >= 70 or max 2 iterations

7. **FRAMEWORK**: Finalize with OODA integration
   - Map workflow to OODA phases
   - Define gates and checkpoints

**Self-Evaluation Scoring (MANDATORY)**:
```text
Dimension                    Weight    Score (0-5)
--------------------------------------------------
Purpose Clarity              0.15      [score]
Capability Completeness      0.15      [score]
Workflow Executability       0.15      [score]
Tool Appropriateness         0.10      [score]
Error Handling               0.10      [score]
Schema Alignment             0.10      [score]
Documentation Quality        0.10      [score]
Differentiation              0.10      [score]
Token Efficiency             0.05      [score]
--------------------------------------------------
Aggregate (weighted):                  [0-100]
```

**Outputs/Deliverables**:
```json
{
  "agent_definition": {
    "content": "markdown string",
    "path": ".claude/agents/{domain}/{agent-name}/{agent-name}.md",
    "sections_count": 19,
    "token_count": "number"
  },
  "self_evaluation": {
    "scores": {
      "purpose_clarity": 0-5,
      "capability_completeness": 0-5,
      "workflow_executability": 0-5,
      "tool_appropriateness": 0-5,
      "error_handling": 0-5,
      "schema_alignment": 0-5,
      "documentation_quality": 0-5,
      "differentiation": 0-5,
      "token_efficiency": 0-5
    },
    "aggregate_score": 0-100,
    "weakest_dimension": "string",
    "improvement_notes": "string"
  },
  "iterations_used": 1-2
}
```

**Gate Condition**:
- Self-evaluation score >= 70/100
- All 19 template sections present
- YAML frontmatter valid

**Error Handling**:
- If score < 70 after 2 iterations: Return to user for guidance
- If template section missing: Flag and attempt generation
- If token count > 5000: Warn about verbosity

**TodoWrite Checkpoint**:
```
Phase 7: AGENT DEFINITION - [COMPLETE|IN_PROGRESS|BLOCKED]
  - Self-score: [aggregate]/100
  - Iterations: [count]
  - Weakest: [dimension]
  - Token count: [count]
```

---

## Phase 8: SIMULATION TESTING [Build-Measure-Learn]

### Purpose
Catch non-working agents BEFORE quality validation by generating and executing test scenarios against the agent definition.

### Agent(s)
- **Primary**: `code-quality` (generates test scenarios)
- **Secondary**: Orchestrator (simulates/evaluates)
- **Future**: `claude-code-test-evaluator` (actual execution via DeepEval)

### Inputs
- Agent definition from Phase 7 (with self-score ≥70)
- Schema from Phase 6
- Research findings from Phase 5

### Process [Build-Measure-Learn]

#### BUILD: Generate Test Scenarios
Task(code-quality) generates 3-5 test scenarios:

| # | Type | Required | Purpose |
|---|------|----------|---------|
| 1 | Happy Path | YES | Basic capability verification |
| 2 | Edge Case | YES | Boundary condition handling |
| 3 | Error Handling | YES | Invalid input response |
| 4 | Tool Usage | NO | Verify declared tools used correctly |
| 5 | Performance | NO | Check execution within limits |

**Test Scenario Schema**:
```json
{
  "scenario_id": "TEST-001",
  "type": "happy_path|edge_case|error_handling|tool_usage|performance",
  "description": "Brief description of what this tests",
  "prompt": "Exact user prompt to test agent with",
  "context_files": ["optional/files/to/provide.md"],
  "expected_behavior": {
    "actions": ["What agent should do step by step"],
    "tools_used": ["Read", "Grep", "Task"],
    "output_contains": ["Key phrases expected in output"]
  },
  "success_criteria": [
    "Output matches expected schema",
    "No error status returned",
    "Completes within 60 seconds"
  ],
  "difficulty": "easy|medium|hard"
}
```

#### MEASURE: Evaluate Test Scenarios

**Current Implementation** (Mental Simulation):
Until DeepEval infrastructure is deployed, evaluation is performed by the Orchestrator:

1. For each test scenario:
   - Read the test prompt
   - Trace through agent workflow mentally
   - Verify workflow handles the input correctly
   - Check if expected tools would be invoked
   - Confirm output would match success criteria

2. Score each scenario:
   - **PASS**: Workflow logic handles scenario correctly
   - **PARTIAL**: Handles but with concerns
   - **FAIL**: Workflow cannot handle scenario

**Future Implementation** (With DeepEval):
When `docs/01-planning/specifications/015-deepeval-agent-evaluation/SPEC.md` is implemented:

1. Test scenarios converted to DeepEval test cases
2. `claude-code-test-evaluator` executes each test in Docker
3. Metrics captured via OpenTelemetry:
   - `agent_test_pass_rate` (target: ≥90%)
   - `agent_test_execution_time_seconds`
   - `agent_quality_score` (target: ≥0.75)
   - `agent_tool_calls_total`
   - `agent_token_usage`
4. Results exported to Prometheus for trend analysis
5. Grafana dashboard shows test results before approval

#### LEARN: Analyze Results & Iterate

**Decision Logic**:
```
IF all required tests (1-3) PASS:
    → Proceed to Phase 9
    → Optional test results inform but don't block

ELSE IF iteration_count < 2:
    → Return to Phase 7 with failure analysis
    → Provide: which tests failed, why, suggested fixes
    → claude-code-ecosystem revises definition

ELSE:
    → Escalate to user for decision
    → Options: override | manual fix | cancel
```

### Outputs/Deliverables
1. **Test Scenarios File**: `{agent-dir}/tests/scenarios.json`
   - Contains all 3-5 test scenarios in JSON format
   - Ready for future DeepEval execution
   
2. **Simulation Report**:
   ```json
   {
     "phase": 8,
     "status": "PASS|FAIL",
     "tests_run": 3,
     "tests_passed": 3,
     "tests_failed": 0,
     "iteration": 1,
     "details": [
       {"scenario_id": "TEST-001", "result": "PASS", "notes": "..."},
       {"scenario_id": "TEST-002", "result": "PASS", "notes": "..."},
       {"scenario_id": "TEST-003", "result": "PASS", "notes": "..."}
     ]
   }
   ```

### Gate Condition
- **Required**: All 3 required tests (happy path, edge case, error handling) must PASS
- **Optional**: Tests 4-5 inform quality but do not block
- **Iteration**: Max 2 returns to Phase 7 before escalation

### Error Handling
| Error | Recovery |
|-------|----------|
| Test generation fails | Retry with simpler scenarios |
| Happy path fails | Return to Phase 7: core workflow broken |
| Edge case fails | Return to Phase 7: boundary handling issue |
| Error handling fails | Return to Phase 7: missing error paths |
| All required pass but optional fail | Proceed with warnings in Phase 11 report |

### TodoWrite Checkpoint
```
Phase 8 complete: Simulation testing passed
- Tests generated: {count}
- Required tests: 3/3 PASS
- Optional tests: {X}/2 PASS
- Scenarios saved: {agent-dir}/tests/scenarios.json
- Ready for Phase 9: Quality Validation
```

### Task() Delegation Example
```
Task(code-quality, "
  GENERATE TEST SCENARIOS for agent: {agent-name}
  
  Agent Definition: {path-to-definition}
  Agent Schema: {path-to-schema}
  
  Generate 3 REQUIRED test scenarios:
  1. Happy path - basic capability
  2. Edge case - boundary condition
  3. Error handling - invalid input
  
  And 2 OPTIONAL test scenarios:
  4. Tool usage verification
  5. Performance boundary
  
  Output format: JSON array of test scenarios per schema.
  Save to: {agent-dir}/tests/scenarios.json
")
```

---

## Phase 9: QUALITY VALIDATION [DMAIC]

**Purpose**: Run comprehensive quality validation across multiple dimensions with parallel validators.

**Agent(s)**: claude-code-ecosystem, claude-code-ecosystem, documentation, context-optimizer (parallel)

**Inputs**:
- Agent definition from Phase 7
- Schema from Phase 6
- Documentation generated
- Simulation results from Phase 8

**Process (DMAIC Framework)**:

### DEFINE: Establish validation scope
- Template compliance (19 sections)
- Documentation health (links, naming)
- Prompt quality (anti-patterns)
- Context efficiency (tokens)
- Quality matrix (9 dimensions)

### MEASURE: Run 5 parallel validators

| Validator | Agent | Metrics |
|-----------|-------|---------|
| Template Compliance | claude-code-ecosystem | Section count, YAML validity, base patterns |
| Documentation Health | documentation | Link validity, naming conventions, organization |
| Prompt Quality | claude-code-ecosystem | Anti-pattern count, clarity score, specificity |
| Context Optimization | context-optimizer | Token count, redundancy, efficiency |
| Quality Matrix | claude-code-ecosystem | 9-dimension scoring (0-100) |

### ANALYZE: Aggregate results
```text
Synthesis Formula:
aggregate = min(template_compliance, 
  0.30 * prompt_quality + 
  0.20 * doc_health + 
  0.20 * context_optimization + 
  0.30 * quality_matrix)

Gate: template = 100% AND aggregate >= 70 AND no HIGH-severity issues
```

### IMPROVE: Address issues if gate fails
- Categorize issues by severity (HIGH/MEDIUM/LOW)
- HIGH: Must fix before proceeding
- MEDIUM: Should fix, can proceed with warning
- LOW: Nice to fix, document for later

### CONTROL: Document validation results
- Store scores for future reference
- Create improvement backlog
- Set baseline for agent quality

**Outputs/Deliverables**:
```json
{
  "validation_results": {
    "template_compliance": {
      "score": 100,
      "sections_present": 19,
      "sections_required": 19,
      "issues": []
    },
    "documentation_health": {
      "score": 0-100,
      "links_valid": "number",
      "links_broken": "number",
      "naming_compliant": true | false
    },
    "prompt_quality": {
      "score": 0-100,
      "anti_patterns": [],
      "severity_counts": {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    },
    "context_optimization": {
      "score": 0-100,
      "token_count": "number",
      "redundancy_areas": [],
      "efficiency_rating": "OPTIMAL | ACCEPTABLE | VERBOSE"
    },
    "quality_matrix": {
      "score": 0-100,
      "dimension_scores": {},
      "weakest_dimensions": []
    }
  },
  "aggregate_score": 0-100,
  "gate_result": "PASS | CONDITIONAL_PASS | FAIL",
  "blocking_issues": [],
  "warnings": []
}
```

**Gate Condition**:
- **PASS** (proceed to Phase 10):
  - Template compliance: 100%
  - Aggregate score: >= 70
  - No HIGH-severity issues
  
- **CONDITIONAL PASS** (proceed with warnings):
  - Template compliance: 100%
  - Aggregate score: 60-69
  - No HIGH-severity, some MEDIUM-severity
  
- **FAIL** (return to Phase 7):
  - Template compliance: < 100%
  - Aggregate score: < 60
  - Any HIGH-severity issues

**Error Handling**:
- If validation times out: Retry individual validator
- If scores inconsistent: Re-run conflicting validators
- If max iterations (3) reached: Return to Phase 7 with detailed feedback

**TodoWrite Checkpoint**:
```
Phase 9: QUALITY VALIDATION - [COMPLETE|IN_PROGRESS|BLOCKED]
  - Template: [score]%
  - Aggregate: [score]/100
  - Gate: [PASS|CONDITIONAL_PASS|FAIL]
  - HIGH issues: [count]
```

---

## Phase 10: DOCUMENTATION [SCAMPER]

**Purpose**: Optimize and organize all agent documentation for clarity and efficiency.

**Agent(s)**: documentation

**Inputs**:
- Agent definition from Phase 7
- Research findings from Phase 5
- Validation results from Phase 9

**Process (SCAMPER Framework)**:

1. **SUBSTITUTE**: Replace verbose explanations with concise ones
   - Long paragraphs -> Bullet points
   - Repetitive examples -> Single canonical example
   - Prose workflows -> Tables/diagrams

2. **COMBINE**: Merge related documentation
   - Consolidate overlapping sections
   - Link related docs instead of duplicating
   - Create unified index

3. **ADAPT**: Apply patterns from successful agents
   - Copy structure from high-quality agents
   - Adapt naming conventions
   - Follow established organizational patterns

4. **MODIFY**: Adjust for the agent's specific needs
   - Customize examples for domain
   - Adjust detail level per audience
   - Optimize for AI-readability

5. **PUT TO OTHER USES**: Consider documentation reuse
   - Create snippets for CLAUDE.md updates
   - Generate orchestrator integration text
   - Prepare handoff summary content

6. **ELIMINATE**: Remove unnecessary content
   - Delete placeholder text
   - Remove redundant examples
   - Strip verbose explanations

7. **REVERSE**: Consider alternative organization
   - Task-based vs feature-based structure
   - Reference-first vs tutorial-first
   - Flat vs hierarchical

**Documentation Structure**:
```
.claude/agents/{domain}/{agent-name}/
├── {agent-name}.md              # Core definition
├── docs/
│   ├── README.md               # Overview and quick start
│   ├── domain-expertise.md     # Frameworks and methodologies
│   └── [topic-specific].md     # Additional knowledge
├── examples/
│   ├── README.md               # Examples index
│   ├── delegation-examples.md  # How to call this agent
│   └── output-template.md      # Sample outputs
└── schemas/
    ├── README.md               # Schema documentation
    └── {agent-name}.schema.json
```

**Outputs/Deliverables**:
```json
{
  "documentation": {
    "files_created": ["string"],
    "files_updated": ["string"],
    "total_files": "number",
    "total_tokens": "number"
  },
  "optimization_applied": {
    "substitutions": "number",
    "combinations": "number",
    "eliminations": "number",
    "token_reduction": "percentage"
  },
  "link_validation": {
    "internal_links": "number",
    "external_links": "number",
    "broken_links": []
  },
  "naming_compliance": {
    "kebab_case_compliant": true | false,
    "violations": []
  }
}
```

**Gate Condition**:
- All internal links valid
- Kebab-case naming compliant
- README.md present in each directory
- No broken references

**Error Handling**:
- If link broken: Attempt auto-fix, flag if unable
- If naming violation: Auto-rename with user confirmation
- If missing README: Generate minimal version

**TodoWrite Checkpoint**:
```
Phase 10: DOCUMENTATION - [COMPLETE|IN_PROGRESS|BLOCKED]
  - Files created: [count]
  - Token reduction: [percentage]
  - Links valid: [all|count broken]
  - Naming: [compliant|violations]
```

---

## Phase 11: REVIEW & APPROVAL [Disney Creative Strategy]

**Purpose**: Multi-perspective review before final approval, ensuring the agent meets vision, practicality, and risk requirements.

**Agent(s)**: planning + Human

**Inputs**:
- Complete agent definition
- All documentation
- Validation results from Phase 9
- Simulation results from Phase 8

**Process (Disney Creative Strategy Framework)**:

### DREAMER: Vision Alignment Check
*"Does this inspire? Is it elegant?"*

Questions to evaluate:
- Does the agent fulfill the original vision?
- Would stakeholders be proud of this agent?
- Is the design elegant and cohesive?
- Does it differentiate clearly from existing agents?

Output:
```json
{
  "vision_verdict": "PASS | NEEDS_WORK",
  "vision_score": 0-5,
  "note": "string"
}
```

### REALIST: Practicality Check
*"Can this actually work?"*

Questions to evaluate:
- Are all tools available and appropriate?
- Can the workflow execute with current infrastructure?
- Are dependencies resolvable?
- Is the scope achievable?

Output:
```json
{
  "practicality_verdict": "PASS | NEEDS_WORK",
  "practicality_score": 0-5,
  "note": "string"
}
```

### CRITIC: Risk Check
*"What could go wrong?"*

Questions to evaluate:
- What are the failure modes?
- What assumptions are risky?
- What's missing from the design?
- What could cause confusion with other agents?

Output:
```json
{
  "risk_verdict": "PASS | NEEDS_WORK",
  "risk_score": 0-5,
  "risks_identified": ["string"],
  "note": "string"
}
```

### CONSOLIDATED: Present to User

Generate comprehensive summary for human review:

```text
# Agent Review: [agent-name]

## Summary
- Domain: [domain]
- Type: [type]
- Quality Score: [aggregate]/100

## Three-Lens Validation
| Lens | Verdict | Score | Notes |
|------|---------|-------|-------|
| Dreamer (Vision) | PASS/NEEDS_WORK | X/5 | [note] |
| Realist (Practical) | PASS/NEEDS_WORK | X/5 | [note] |
| Critic (Risk) | PASS/NEEDS_WORK | X/5 | [note] |

## Capabilities
1. [capability 1]
2. [capability 2]
...

## Files to be Created
- .claude/agents/{domain}/{agent-name}/{agent-name}.md
- .claude/agents/{domain}/{agent-name}/schemas/{agent-name}.schema.json
- .claude/agents/{domain}/{agent-name}/docs/*.md

## Risks & Mitigations
- [risk 1]: [mitigation]
- [risk 2]: [mitigation]

## Decision Required
```

**Outputs/Deliverables**:
```json
{
  "review_summary": {
    "dreamer": {"verdict": "PASS", "score": 4, "note": "string"},
    "realist": {"verdict": "PASS", "score": 5, "note": "string"},
    "critic": {"verdict": "NEEDS_WORK", "score": 3, "note": "string"}
  },
  "overall_verdict": "PASS | NEEDS_WORK",
  "consolidated_score": 0-15,
  "top_suggestion": "string",
  "user_decision": "approve | refine | cancel"
}
```

**Human Decision Point**:
```text
Options:
1. [A] Approve - Proceed to finalization
2. [R] Refine - Return to Phase 7 with specific feedback
3. [C] Cancel - Abort agent creation

If Refine, specify:
- Which dimension needs work (vision/practicality/risk)
- Specific changes requested

Choose [A/R/C]:
```

**Gate Condition**:
- User explicitly selects "Approve"
- If "Refine": Return to Phase 7 with feedback, max 2 refinement cycles
- If "Cancel": Clean up artifacts, exit workflow

**Error Handling**:
- If review times out: Save state, allow resume
- If user unclear: Request clarification
- If max refinements reached: Force decision (approve/cancel)

**TodoWrite Checkpoint**:
```
Phase 11: REVIEW & APPROVAL - [COMPLETE|IN_PROGRESS|BLOCKED]
  - Dreamer: [verdict]
  - Realist: [verdict]
  - Critic: [verdict]
  - User decision: [approve|refine|cancel|pending]
```

---

## Phase 12: FINALIZATION [Pre-Mortem]

**Purpose**: Write all files with proactive failure prevention and generate handoff documentation.

**Agent(s)**: claude-code-ecosystem, planning

**Inputs**:
- Approved agent definition
- All documentation
- Schema
- User approval from Phase 11

**Process (Pre-Mortem Framework)**:

### ASSUME FAILURE
*"It's 6 months from now and this agent completely failed to work."*

Brainstorm potential causes:
1. **File System Failures**
   - Write permissions denied
   - Path conflicts
   - Disk space issues

2. **Integration Failures**
   - CLAUDE.md not updated
   - Agent not discoverable
   - Schema not linked

3. **Runtime Failures**
   - Missing dependencies
   - Tool access issues
   - Context too large

4. **Human Failures**
   - User forgets to restart
   - Misconfigured handoff
   - Incomplete documentation

### PREVENT NOW
For each failure mode, implement prevention:

| Failure Mode | Prevention | Verification |
|--------------|------------|--------------|
| Write denied | Check permissions before write | Pre-flight validation |
| Path conflict | Verify no existing files (or --overwrite) | Glob check |
| Missing integration | Auto-update CLAUDE.md, orchestrator-workflow.md | Post-write verification |
| User forgets restart | Bold reminder in handoff | Handoff template |
| Incomplete docs | Validate all READMEs exist | File count check |

### EXECUTE WRITES
Write files in order with verification:

1. **Create directory structure**
   ```
   .claude/agents/{domain}/{agent-name}/
   ├── docs/
   ├── examples/
   └── schemas/
   ```

2. **Write schema file**
   - Path: `schemas/{agent-name}.schema.json`
   - Verify: JSON valid, refs resolved

3. **Write documentation files**
   - Path: `docs/*.md`
   - Verify: Links valid, naming compliant

4. **Write examples**
   - Path: `examples/*.md`
   - Verify: Code blocks valid

5. **Write agent definition**
   - Path: `{agent-name}.md`
   - Verify: Template complete, YAML valid

6. **Update integration points**
   - CLAUDE.md delegation table (if applicable)
   - orchestrator-workflow.md agent list
   - agent-categorization.md

### GENERATE HANDOFF
Create comprehensive handoff document:

```markdown
# Agent Creation Complete: [agent-name]

## Files Created
- [x] .claude/agents/{domain}/{agent-name}/{agent-name}.md
- [x] .claude/agents/{domain}/{agent-name}/schemas/{agent-name}.schema.json
- [x] .claude/agents/{domain}/{agent-name}/docs/README.md
- [x] .claude/agents/{domain}/{agent-name}/docs/domain-expertise.md
- [x] .claude/agents/{domain}/{agent-name}/examples/README.md
- [x] .claude/agents/{domain}/{agent-name}/examples/delegation-examples.md

## Integrations Updated
- [x] Agent directory structure created
- [ ] CLAUDE.md (manual update recommended)
- [ ] orchestrator-workflow.md (manual update recommended)

## Quality Metrics
- Quality Score: [score]/100
- Template Compliance: PASS
- Schema Validation: PASS
- Simulation Tests: 3/3 PASS

## CRITICAL: Next Steps
1. **RESTART Claude Code session** (required for new agent recognition)
2. Test agent with sample task:
   ```
   Task(subagent_type="[agent-name]", prompt="[sample prompt]")
   ```
3. Monitor first few executions for issues
4. Iterate on agent definition if needed

## Usage Example
[Include delegation example from examples/delegation-examples.md]

## Rollback Instructions
If issues arise, rollback with:
```bash
git checkout -- .claude/agents/{domain}/{agent-name}/
```
```

**Outputs/Deliverables**:
```json
{
  "files_written": [
    {
      "path": "string",
      "status": "SUCCESS | FAILED",
      "verification": "PASSED | FAILED"
    }
  ],
  "integrations_updated": [
    {
      "file": "string",
      "change": "string",
      "status": "SUCCESS | SKIPPED | FAILED"
    }
  ],
  "handoff": {
    "content": "markdown string",
    "displayed": true
  },
  "rollback_command": "string",
  "overall_status": "SUCCESS | PARTIAL | FAILED"
}
```

**Gate Condition**:
- All files written successfully
- Handoff document complete
- User has clear next steps

**Error Handling**:
- If write fails: Attempt rollback via git checkout
- If partial failure: Document what succeeded, what failed
- If rollback fails: Provide manual cleanup instructions

**Rollback Protocol**:
```bash
# If any write fails, restore previous state
git checkout -- .claude/agents/{domain}/{agent-name}/

# If directory was new (not overwrite), remove it
rm -rf .claude/agents/{domain}/{agent-name}/
```

**TodoWrite Checkpoint**:
```
Phase 12: FINALIZATION - [COMPLETE|IN_PROGRESS|BLOCKED]
  - Files written: [count]/[total]
  - Integrations: [count] updated
  - Handoff: [generated|pending]
  - Status: [SUCCESS|PARTIAL|FAILED]
```

---

## Interactive Mode Phases (I-1 through I-5)

When using `--create-definition` flag, the workflow begins with 5 interactive phases before proceeding to the standard 12-phase workflow.

---

### Phase I-1: CAPTURE IDEA

**Purpose**: Extract core agent concept from user in 2-3 sentences.

**Agent(s)**: Orchestrator (direct interaction)

**Process**:
1. Present "What, How, When" framework prompt
2. Collect user's agent idea description
3. Validate response has sufficient detail (>20 words, 2+ framework elements)
4. If vague: Re-prompt with guidance (max 3 attempts)

**Prompt Template**:
```text
Describe your agent idea in 2-3 sentences:

Use the "What, How, When" framework:
- WHAT problem does this agent solve?
- HOW does it accomplish this (key actions)?
- WHEN should it be called instead of other agents?

Example:
"An agent that analyzes Python code for performance bottlenecks
by profiling function execution times and memory usage. Call it
when optimizing slow code paths after functionality is correct."
```

**Gate**: User provides substantive description meeting criteria

**TodoWrite Checkpoint**:
```
Phase I-1: CAPTURE IDEA - [COMPLETE|IN_PROGRESS]
  - Idea captured: [yes|no]
  - Attempts: [count]/3
```

---

### Phase I-2: ANALYZE & PROPOSE [CAGEERF]

**Purpose**: Transform informal idea into structured proposal with confidence-scored recommendations.

**Agent(s)**: claude-code-ecosystem (analyze_agent_idea operation)

**Process**:
1. Analyze user's idea text
2. Generate 10 structured sections with confidence scores:
   - Agent Name Options (2-3 choices)
   - Domain Scope
   - Agent Type
   - Purpose Statement
   - Core Capabilities (4-6)
   - Expected Inputs
   - Expected Outputs
   - Domain Knowledge Areas
   - Tool Recommendations
   - Integration Points

**Output**: Structured proposal with confidence scores (0.0-1.0) per recommendation

**Gate**: Analysis complete with all 10 sections populated

**TodoWrite Checkpoint**:
```
Phase I-2: ANALYZE & PROPOSE - [COMPLETE|IN_PROGRESS]
  - Sections: [count]/10
  - Avg confidence: [score]
```

---

### Phase I-3: INTERACTIVE REFINEMENT

**Purpose**: Walk through proposal with user Q&A, allowing customization.

**Agent(s)**: Orchestrator (direct interaction)

**Process**:
1. Present name options with confidence scores, collect choice
2. Confirm domain and type, allow override
3. Present purpose statement, allow refinement
4. Present capabilities list with [A]ccept/[R]emove/[E]dit/[+]Add options
5. Confirm tools and integrations
6. Allow return to previous sections if needed

**Interaction Pattern**:
```text
Recommended agent names:
1. python-performance-analyzer (confidence: 0.92)
2. code-profiler (confidence: 0.78)
3. perf-bottleneck-finder (confidence: 0.71)

Choose [1/2/3] or provide custom name:
```

**Gate**: User confirms all sections

**TodoWrite Checkpoint**:
```
Phase I-3: INTERACTIVE REFINEMENT - [COMPLETE|IN_PROGRESS]
  - Name: [selected]
  - Domain: [confirmed]
  - Capabilities: [count] confirmed
```

---

### Phase I-4: GENERATE DEFINITION

**Purpose**: Create complete agent definition file from refined requirements.

**Agent(s)**: claude-code-ecosystem (generate_agent_definition operation)

**Process**:
1. Compile all refined requirements
2. Apply template structure (`.claude/templates/agent-definition-input.template.md`)
3. Generate definition file at specified path
4. Validate format and completeness

**Output**: Agent definition file ready for standard workflow

**Gate**: File created, all required sections populated

**TodoWrite Checkpoint**:
```
Phase I-4: GENERATE DEFINITION - [COMPLETE|IN_PROGRESS]
  - File: [path]
  - Sections: [count]
  - Valid: [yes|no]
```

---

### Phase I-5: PRESENT OPTIONS

**Purpose**: Offer next steps to user after definition generation.

**Agent(s)**: Orchestrator (direct interaction)

**Process**:
1. Show preview (first 30 lines of generated file)
2. Present options:
   - [P] Proceed immediately to 12-phase workflow
   - [R] Review first (exit, user reviews, runs /create-agent later)
   - [G] Regenerate (return to I-3 with different answers)
3. Execute based on user choice

**Options Handling**:
- **Proceed**: Continue to Phase 1 of standard workflow
- **Review**: Save file, exit command, user manually reviews
- **Regenerate**: Return to Phase I-3 with previous answers as defaults

**Gate**: User makes explicit choice

**TodoWrite Checkpoint**:
```
Phase I-5: PRESENT OPTIONS - [COMPLETE|IN_PROGRESS]
  - Choice: [P|R|G]
  - Proceeding to: [Phase 1|Exit|Phase I-3]
```

---

## Phase Iteration Limits

| Phase | Max Iterations | On Exceed | Rationale |
|-------|---------------|-----------|-----------|
| 5 (Research) | 2 | Proceed with best CQ, warn user | Diminishing returns on research |
| 7 (Definition) | 2 | Return to user for guidance | Self-improvement has limits |
| 8 (Simulation) | 2 | Return to Phase 7 with gaps | Tests reveal fundamental issues |
| 9 (Validation) | 3 | Return to Phase 7 with feedback | Quality gates must be met |

### Iteration Flow Diagram

```
Phase 5 (Research):
  Iteration 1 -> CQ >= 0.85? -> YES -> Phase 6
                             -> NO  -> Iteration 2
  Iteration 2 -> Proceed regardless (document gaps)

Phase 7 (Definition):
  Iteration 1 -> Score >= 70? -> YES -> Phase 8
                              -> NO  -> Iteration 2
  Iteration 2 -> Score >= 70? -> YES -> Phase 8
                              -> NO  -> Return to USER

Phase 8 (Simulation):
  Iteration 1 -> All PASS? -> YES -> Phase 9
                           -> NO  -> Return to Phase 7 with gaps
  (After Phase 7 fix)
  Iteration 2 -> All PASS? -> YES -> Phase 9
                           -> NO  -> Return to USER

Phase 9 (Validation):
  Iteration 1 -> Gate PASS? -> YES -> Phase 10
                            -> NO  -> Fix and retry
  Iteration 2 -> Gate PASS? -> YES -> Phase 10
                            -> NO  -> Fix and retry
  Iteration 3 -> Gate PASS? -> YES -> Phase 10
                            -> NO  -> Return to Phase 7
```

---

## Phase Dependencies

```
                    [Interactive Mode]
                    I-1 -> I-2 -> I-3 -> I-4 -> I-5
                                                 |
                                                 v
[Standard Workflow] --------------------------> Phase 1
                                                 |
Phase 1 (Parse) -----> Phase 2 (Duplicates)     |
                              |                  |
                              v                  |
                       Phase 3 (Requirements) <--+
                              |
                              v
                       Phase 4 (Research Plan)
                              |
                              v
                       Phase 5 (Research Exec) <---+
                              |                    |
                              v                    |
                       Phase 6 (Schema)            |
                              |                    |
                              v                    |
                  +---> Phase 7 (Definition) ------+
                  |           |                    |
                  |           v                    |
                  |    Phase 8 (Simulation) -------+
                  |           |
                  |           v
                  +--- Phase 9 (Validation)
                              |
                              v
                       Phase 10 (Documentation)
                              |
                              v
                       Phase 11 (Review) <---------+
                              |                    |
                              v                    |
                       Phase 12 (Finalize) --------+
                                        (if refine requested)
```

---

## TodoWrite Master Template

Use this template at workflow start:

```
Agent Creation: [agent-name]
Mode: [Template | Interactive]
Started: [timestamp]

Interactive Phases (if applicable):
- [ ] I-1: Capture idea
- [ ] I-2: Analyze & propose
- [ ] I-3: Interactive refinement
- [ ] I-4: Generate definition
- [ ] I-5: Present options

Standard Phases:
- [ ] Phase 1: Parse & validate
- [ ] Phase 2: Duplicate detection
- [ ] Phase 3: Requirements assessment
- [ ] Phase 4: Research planning
- [ ] Phase 5: Research execution
- [ ] Phase 6: Schema design
- [ ] Phase 7: Agent definition
- [ ] Phase 8: Simulation testing
- [ ] Phase 9: Quality validation
- [ ] Phase 10: Documentation
- [ ] Phase 11: Review & approval
- [ ] Phase 12: Finalization

Current Phase: [phase]
Blockers: [none | description]
```

---

## Related Documentation

- **Command Reference**: `.claude/commands/create-agent.md`
- **Delegation Patterns**: `.claude/docs/command-docs/create-agent/docs/delegation-patterns.md`
- **Error Handling**: `.claude/docs/command-docs/create-agent/docs/error-handling.md`
- **Interactive Mode Details**: `.claude/docs/command-docs/create-agent/docs/interactive-mode.md`
- **Usage Examples**: `.claude/docs/command-docs/create-agent/examples/usage-examples.md`
- **Thinking Frameworks**: `.claude/docs/00-core/frameworks/README.md`
- **Agent Template**: `.claude/templates/agent.template.md`
- **Definition Input Template**: `.claude/templates/agent-definition-input.template.md`

---

## DeepEval Integration Roadmap

**Current State**: Phase 8 uses mental simulation for test validation.

**Dependency**: `docs/01-planning/specifications/015-deepeval-agent-evaluation/SPEC.md`

**Integration Timeline**:
1. **Now**: Test scenarios generated and saved as JSON artifacts
2. **Post-DeepEval MVP**: Scenarios become executable via `claude-code-test-evaluator`
3. **Post-DeepEval Full**: CI/CD gates, regression detection, trend analysis

**Test Artifact Flow**:
```
create-agent Phase 8
    ↓ generates
scenarios.json
    ↓ consumed by
DeepEval test runner
    ↓ metrics to
Prometheus/Grafana
    ↓ enables
Automated quality gates
```

---

**Version**: 2.0
**Last Updated**: 2025-11-30
**Change Log**:
- v2.0 - Complete rewrite for 12-phase workflow with OODA mapping, thinking frameworks per phase, simulation testing (Phase 8), enhanced gates and checkpoints
- v1.0 - Original 10-phase workflow documentation
