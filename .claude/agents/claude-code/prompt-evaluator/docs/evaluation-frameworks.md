# Prompt Evaluation Frameworks

**Purpose**: Comprehensive evaluation criteria for assessing Claude Code agent prompt quality

**Reference**: Used by `.claude/agents/dev-tools/prompt-evaluator/prompt-evaluator.md`

**Version**: 1.0

---

## Overview

This document contains the complete evaluation frameworks used by the prompt-evaluator agent. Each framework assesses a different dimension of prompt quality with specific scoring criteria and grading scales.

---

## Framework 1: Structural Quality (17 Criteria - Pass/Fail)

**Purpose**: Assess agent architecture and design patterns compliance

**Cross-Reference**: `creating-ai-readable-documentation-framework.md` for machine-parseable structure patterns

**Scoring**: Pass = 1 point, Fail = 0 points. Report: X/17 with evidence for each criterion.

### Single Responsibility & Boundaries (3 criteria)

1. **Single responsibility clearly defined**
   - **PASS**: Agent has one clear purpose stated in Role & Boundaries
   - **FAIL**: Multiple responsibilities or unclear scope

2. **Scope discipline (explicit boundaries documented)**
   - **PASS**: Boundaries section explicitly lists what agent does NOT do
   - **FAIL**: No boundaries documented or scope too broad

3. **Domain scope properly limited**
   - **PASS**: Domain restricted to specific directories/file types
   - **FAIL**: Cross-domain without justification or unlimited scope

### Schema & Pattern Compliance (4 criteria)

4. **Frontmatter compliance (Claude Code specification)**
   - **PASS**: Frontmatter contains ONLY officially documented Claude Code fields: name (required), description (required), tools, model, permissionMode, skills
   - **FAIL**: Invalid fields present (version, maturity, temperature, disallowedTools, status, tags) OR field values use incorrect format (e.g., tools/skills as YAML lists instead of comma-separated strings)
   - **ACCEPTED (Undocumented)**: `color` field - accepted by Claude Code but NOT in official Anthropic specification. Accepts CSS color name strings (red, blue, green, yellow, orange, purple, cyan, etc.). Do NOT flag as invalid - functional but undocumented.
   - **Evidence**: Check frontmatter lines 1-20 for field names and value formats
   - **Reference**: Claude Code agent specification, agent-creation-guide.md
   - **Note**: Undocumented fields that work (like `color`) should be flagged as "accepted/undocumented" not "invalid"

5. **Schema compliance (extends base-agent.schema.json)**
   - **PASS**: Agent references and extends base-agent.schema.json
   - **FAIL**: No schema reference or custom schema without inheritance

6. **Base pattern extension (inheritance for token savings)**
   - **PASS**: Agent extends base-agent-pattern.md with documented inherited sections
   - **FAIL**: Duplicates base pattern content or no extension reference

7. **Two-state model (SUCCESS/FAILURE)**
   - **PASS**: Explicitly documents SUCCESS and FAILURE response structures
   - **FAIL**: Missing state model or custom states without justification

### Tool & Workflow Architecture (3 criteria)

8. **Performance-first tool selection (appropriate tier)**
   - **PASS**: Tools match performance tier (Tier 1: Read/Grep, Tier 2: Edit, Tier 3: Write/Bash)
   - **FAIL**: Heavy tools for simple tasks or missing lighter alternatives

9. **Workflow structure (6 phases documented)**
   - **PASS**: Complete workflow with Analysis → Research → Todo → Implementation → Validation → Reflection
   - **FAIL**: Missing phases or workflow not documented

10. **File operation protocol compliance**
    - **PASS**: References file-operation-protocol.md and follows standards
    - **FAIL**: No protocol reference or violations (e.g., editing system files)

### Communication Quality (3 criteria)

11. **Tool descriptions (new team member standard)**
    - **PASS**: Tool usage explained clearly for someone unfamiliar with the codebase
    - **FAIL**: Vague descriptions or assumes prior knowledge

12. **Explicit context (no implicit assumptions)**
    - **PASS**: All decisions and context documented explicitly
    - **FAIL**: Relies on implicit knowledge or undocumented assumptions

13. **High-signal information (actionable outputs)**
    - **PASS**: All outputs include actionable next steps or specific findings
    - **FAIL**: Generic outputs or missing implementation guidance

### Integration Patterns (3 criteria)

14. **Four-component delegation (if orchestrator)**
    - **PASS**: Orchestrator agents delegate with objective/format/guidance/boundaries
    - **FAIL**: Incomplete delegation context or missing components
    - **N/A**: Not an orchestrator agent

15. **Query classification (if research agent)**
    - **PASS**: Research agents classify queries and apply appropriate strategies
    - **FAIL**: Single strategy for all queries or no classification
    - **N/A**: Not a research agent

16. **Parallel execution awareness**
    - **PASS**: Documents parallel execution support or serialization requirements
    - **FAIL**: No parallel execution guidance or conflicts possible

17. **Filename-only documentation references**
    - **PASS**: All doc references use filename only (e.g., `base-agent-pattern.md`, `thinking-frameworks-catalog.md`)
    - **FAIL**: Full paths used (e.g., `.claude/docs/01-guides/...`, `docs/04-guides/...`)
    - **Detection**: `Grep("[./]claude/docs/|docs/[0-9]+-", agent_path)` - any matches = FAIL
    - **Exception**: Glob patterns for directory scanning are acceptable (e.g., `Glob(".claude/docs/**/*.md")`)
    - **Rationale**: Filename-only allows AI to search for file; full paths break when docs reorganized

---

## Framework 2: Anthropic Prompt Engineering (9 Principles - Graded A-F)

**Purpose**: Assess adherence to Anthropic best practices for prompt engineering

**Scoring**: Grade each principle (0-5 scale), calculate weighted average, map to letter grade.

### Core Principles (5 criteria)

1. **Role assignment (clear agent identity and purpose)** (Weight: 1.2x)
   - **5**: Detailed role with specific expertise, boundaries, and context
   - **4**: Clear role with basic context
   - **3**: Role stated but lacking detail
   - **2**: Vague role definition
   - **1**: Role mentioned but unclear
   - **0**: No role assignment

2. **Clarity & directness (unambiguous instructions)** (Weight: 1.3x)
   - **5**: All instructions crystal clear, 0 unclear instructions
   - **4**: Mostly clear with 1-2 unclear instructions
   - **3**: Generally clear but 3-5 unclear instructions
   - **2**: 6-10 unclear instructions
   - **1**: 11+ unclear instructions (mostly ambiguous)
   - **0**: Completely unclear instructions

   **Calibration Examples**:
   ```markdown
   # Score 5 - Crystal Clear
   ## Workflow
   1. Read agent file with `Read(path)`
   2. Extract frontmatter fields: name, description, tools
   3. Validate each field against schema
   4. Output structured JSON with pass/fail per field
   ```
   *Why 5: Numbered steps, explicit tool calls, clear output format*

   ```markdown
   # Score 3 - Generally Clear (3-5 unclear)
   ## Workflow
   Load the agent file and check the frontmatter. Validate fields and report issues.
   ```
   *Why 3: Steps implied but not explicit, no tool invocations, "report issues" vague*

   ```markdown
   # Score 1 - Mostly Ambiguous (11+ unclear)
   ## Workflow
   Analyze the agent.
   ```
   *Why 1: No actionable detail, unclear what "analyze" means or outputs*

3. **Data-instruction separation (context vs directives)** (Weight: 1.1x)
   - **5**: Perfect separation using XML tags or clear sections
   - **4**: Good separation with minor mixing
   - **3**: Some separation but inconsistent
   - **2**: Data and instructions often mixed
   - **1**: Minimal separation
   - **0**: No separation

4. **Output formatting (structured JSON, XML tags)** (Weight: 1.0x)
   - **5**: Comprehensive structured output with examples
   - **4**: Good structure with clear format
   - **3**: Basic structure, some formatting
   - **2**: Minimal structure
   - **1**: Vague format requirements
   - **0**: No output formatting specified

5. **Step-by-step thinking (reasoning approach documented)** (Weight: 1.2x)
   - **5**: Detailed reasoning approach with OODA loop
   - **4**: Clear reasoning steps
   - **3**: Basic thinking approach mentioned
   - **2**: Minimal reasoning guidance
   - **1**: Vague reasoning expectations
   - **0**: No reasoning approach

### Advanced Patterns (4 criteria)

6. **Example usage (few-shot demonstrations)** (Weight: 1.0x)
   - **5**: 3+ examples covering edge cases and error scenarios
   - **4**: 2-3 examples for common scenarios
   - **3**: 1-2 basic examples provided
   - **2**: 1 minimal example lacking detail
   - **1**: Example present but incorrect or misleading
   - **0**: No examples

   **Calibration Examples**:
   ```markdown
   # Score 5 - Comprehensive Examples
   ### Example 1: Standard File Analysis
   Input: `path/to/agent.md`
   Output: `{"status": "SUCCESS", "score": 14/16}`

   ### Example 2: Missing Schema (Error Case)
   Input: `path/to/incomplete-agent.md`
   Output: `{"status": "FAILURE", "error": "schema_missing"}`

   ### Example 3: Edge Case - Large Agent
   Input: `path/to/large-agent.md` (>500 lines)
   Output: `{"status": "SUCCESS", "warnings": ["size_exceeded"]}`
   ```
   *Why 5: Multiple scenarios including success, error, and edge case*

   ```markdown
   # Score 3 - Basic Example
   ### Example
   Run evaluation on an agent file to get quality score.
   ```
   *Why 3: Shows intent but no concrete input/output format*

7. **Hallucination prevention (fact-checking, confidence scoring)** (Weight: 1.1x)
   - **5**: 3+ mechanisms: confidence scoring + evidence citations + validation steps
   - **4**: 2 prevention mechanisms implemented
   - **3**: 1 mechanism (e.g., "cite sources" instruction)
   - **2**: Prevention mentioned but not actionable
   - **1**: Vague guidance ("be accurate")
   - **0**: No hallucination prevention

   **Calibration Examples**:
   ```markdown
   # Score 5 - Comprehensive Prevention
   ## Validation Rules
   - Include confidence score (0.0-1.0) for all recommendations
   - Cite file:line for every finding
   - If confidence <0.7, state "UNVERIFIED" and explain gap
   ```
   *Why 5: Quantified confidence, evidence requirement, uncertainty handling*

   ```markdown
   # Score 2 - Minimal Prevention
   ## Guidelines
   Make sure your analysis is accurate.
   ```
   *Why 2: Intent present but no actionable mechanism*

8. **XML tag structure (consistent use for sections)** (Weight: 0.9x)
   - **5**: Consistent XML tags throughout with clear hierarchy
   - **4**: Good XML usage with minor inconsistencies
   - **3**: Some XML tags used
   - **2**: Minimal XML structure
   - **1**: Inconsistent XML usage
   - **0**: No XML tags

9. **Layered complexity (progressive detail levels)** (Weight: 1.0x)
   - **5**: Perfect progressive disclosure from essential to detailed
   - **4**: Good layering with clear hierarchy
   - **3**: Some layering present
   - **2**: Minimal layering
   - **1**: Poor organization
   - **0**: No layered complexity

### Grading Scale

- **A (4.5-5.0)**: Excellent implementation, follows all best practices
- **B (3.5-4.4)**: Good implementation, minor improvements possible
- **C (2.5-3.4)**: Acceptable, notable gaps in best practices
- **D (1.5-2.4)**: Poor implementation, significant improvements required
- **F (0.0-1.4)**: Failing to meet standards, major redesign needed

### Calculation Formula

```
Weighted_Average = (Σ (Score × Weight)) / (Σ Weights)
Letter_Grade = Map(Weighted_Average, Grading_Scale)
```

---

## Framework 3: Token Optimization (Quantitative Analysis)

**Purpose**: Identify and quantify token savings opportunities

**Data Source**: `scripts/calculate_tokens.py` output (run at evaluation start)

### Available Data from Token Counting

- Total tokens (accurate count using tiktoken)
- Line count (for progressive disclosure compliance)
- Character count (for size analysis)
- Tokens per line (density metric)
- Per-file breakdown (for batch processing)

### Optimization Techniques (15+ Methods)

**Technique 1: Base pattern inheritance** (~1,150 tokens)
- **When to apply**: Agent not extending base-agent-pattern.md
- **Savings**: ~1,150 tokens (Knowledge Base + Pre-Flight + Core Workflow)
- **Effort**: Low (add reference section)

**Technique 2: Documentation references** (100-300 tokens per section)
- **When to apply**: Inline documentation >50 lines
- **Savings**: 100-300 tokens per externalized section
- **Effort**: Low (create external doc + reference)

**Technique 3: Compression targets** (10:1 ratios for verbose sections)
- **When to apply**: Verbose explanations, redundant wording
- **Savings**: 10:1 compression ratio for prose
- **Effort**: Medium (rewrite for clarity and brevity)

**Technique 4: Tool description optimization** (50-150 tokens)
- **When to apply**: Redundant tool descriptions, low-signal content
- **Savings**: 50-150 tokens per tool section
- **Effort**: Low (edit descriptions)

**Technique 5: Example consolidation** (100-500 tokens)
- **When to apply**: Exhaustive example lists (>5 examples)
- **Savings**: 100-500 tokens
- **Effort**: Low (select representative samples)

**Technique 6-15**: See `optimization-calculations.md` for complete list including workflow compression, redundant section removal, termination rules, context offloading, MCP efficiency, parallel execution references, error handling compression, validation checklist optimization, research pattern references, and tool coordination patterns.

### Quantification Formula

```
Current_Tokens = Token_Count (from scripts/calculate_tokens.py)
Optimization_Potential = Σ (Applicable_Technique_Savings)
Optimization_Percentage = (Optimization_Potential / Current_Tokens) × 100
Priority_Ranking = Savings × Effort⁻¹ (high savings, low effort = top priority)
```

---

## Framework 4: Testing & Validation (Risk-Based Strategy)

**Purpose**: Match testing approach to agent risk level

### Risk Level Classification

| Level | Tools | Examples | Risk Score |
|-------|-------|----------|------------|
| CRITICAL | Write + Bash + External APIs | python-code-implementer, k8s-deployment | 1.0 |
| HIGH | Write OR Bash OR External APIs | agent-architect, debugger, researcher-external | 0.75 |
| MEDIUM | Edit + Read + Complex logic | doc-librarian, architecture-enhancer | 0.5 |
| LOW | Read-only + simple operations | prompt-evaluator, researcher-codebase | 0.25 |

### Testing Strategy by Risk Level

| Risk | Required Testing | Coverage Target |
|------|-----------------|-----------------|
| CRITICAL | Schema + Regression + Adversarial + CI/CD + Manual QA | >80% |
| HIGH | Schema + Regression + Quality Matrix + Integration | >60% |
| MEDIUM | Schema + Quality Matrix + LLM-as-judge | >40% |
| LOW | Quality Matrix + Schema + Spot checks | >20% |

### Recommended Testing Frameworks

- **Pydantic**: Schema validation (all risk levels)
- **G-Eval**: LLM-as-judge evaluation (MEDIUM/LOW)
- **PromptBench**: Adversarial testing (CRITICAL/HIGH)
- **pytest**: Unit and integration testing (all levels)

---

## Framework 5: Progressive Disclosure Quality

**Purpose**: Assess agent definition organization for optimal context window usage

### Evaluation Criteria (4 Factors)

| Factor | Weight | Target | Pass/Partial/Fail |
|--------|--------|--------|-------------------|
| Semantic Description | 0.25 | <200 chars, keyword-rich | 1.0 / 0.5 / 0.0 |
| Hierarchical Structure | 0.30 | 5 sections in order | 1.0 / 0.5 / 0.0 |
| Size Compliance | 0.25 | <500 lines | Score formula below |
| Context Efficiency | 0.20 | External refs, no bloat | 1.0 / 0.5 / 0.0 |

**Size Score Formula**: `max(0.0, 1.0 - ((Line_Count - 500) / 500))`

**Overall Formula**:
```
PD_Score = (Semantic × 0.25) + (Hierarchical × 0.30) + (Size × 0.25) + (Efficiency × 0.20)
```

**Grading**: A (0.85-1.0), B (0.70-0.84), C (0.50-0.69), D (0.30-0.49), F (0.00-0.29)

### Calibration Examples - Semantic Description

**Pass (1.0)**: `"Python code reviewer for packages/. Static analysis, style enforcement, security scanning. NOT for: tests, docs, non-Python files."` (168 chars, keywords: Python, reviewer, static analysis, security)

**Partial (0.5)**: `"Reviews code and provides feedback on quality."` (46 chars but lacks trigger keywords, no NOT-for boundary)

**Fail (0.0)**: `"A helpful agent for code stuff."` (vague, no domain keywords, no boundaries)

### Calibration Examples - Hierarchical Structure

**Pass (1.0)**: Agent has sections in order: Role & Boundaries > Core Behavior > Workflow > Error Handling > Output Schema

**Partial (0.5)**: Has 4/5 sections OR sections present but disordered

**Fail (0.0)**: Missing 2+ required sections OR flat structure with no hierarchy

---

## Framework 6: Token Density Quality

**Purpose**: Assess prompt efficiency using advanced token optimization techniques

**Cross-Reference**: `creating-ai-readable-documentation-framework.md` for AI-readability patterns (machine-parseable structure, front-loaded keywords, explicit relationships)

### Scoring Dimensions (6 Metrics)

| Dimension | Weight | Target | Scoring |
|-----------|--------|--------|---------|
| Filler Word Density | 0.15 | <5% | 1.0 if <5%, 0.5 if 5-10%, 0.0 if >10% |
| Active Voice Ratio | 0.20 | >80% | 1.0 if >80%, 0.5 if 60-80%, 0.0 if <60% |
| Structured Data Usage | 0.15 | Lists > Prose | Optimized/Mixed/Verbose |
| XML Tag Efficiency | 0.15 | >30% savings | 1.0 if >40%, 0.5 if 30-40%, 0.0 if <30% |
| Example Efficiency | 0.20 | ≤3, <20% tokens | Combined count + ratio score |
| Reference Inheritance | 0.15 | >60% reuse | 1.0 if >60%, 0.5 if 40-60%, 0.0 if <40% |

**Overall Formula**:
```
TD_Score = (Filler × 0.15) + (Active × 0.20) + (Structured × 0.15) + (XML × 0.15) + (Examples × 0.20) + (Inheritance × 0.15)
```

**Grading**: A (0.85-1.0), B (0.70-0.84), C (0.50-0.69), D (0.30-0.49), F (0.00-0.29)

### Calibration Examples - Filler Word Density

**Pass (<5%)**:
```markdown
Read file. Extract fields. Validate schema. Return JSON.
```
*0% filler - direct imperative instructions*

**Partial (5-10%)**:
```markdown
You should read the file. Then you need to extract fields. Please validate the schema.
```
*~8% filler - "you should", "you need to", "please" add no information*

**Fail (>10%)**:
```markdown
In order to properly analyze the file, you will need to carefully read through it. After that, you should then proceed to extract the relevant fields.
```
*~15% filler - "in order to", "properly", "carefully", "after that", "proceed to"*

### Calibration Examples - Active Voice Ratio

**Pass (>80% active)**:
```markdown
The agent reads the file, validates fields, and outputs JSON.
```
*100% active voice*

**Fail (<60% active)**:
```markdown
The file is read by the agent. Fields are validated. JSON is output.
```
*100% passive voice - harder to parse, less direct*

---

## Framework 7: Framework Alignment (Phase-Aware Evaluation)

**Purpose**: Validate agent uses appropriate thinking framework(s) for its domain AND applies them deliberately throughout workflow phases

**Reference**: `00-core/frameworks/README.md` for complete framework-agent mappings

### Assessment Process (4 Steps)

1. **Domain Identification**: Determine agent's primary category
   | Category | Examples | Primary Framework Expected |
   |----------|----------|---------------------------|
   | Research | researcher-*, context-readiness-assessor | ReACT |
   | Implementation | python-code-implementer, test-creator | CAGEERF or Build-Measure-Learn |
   | Analysis/Review | python-code-reviewer, prompt-evaluator | ReACT + DMAIC |
   | Planning | plan-enhancer, task-creator | CAGEERF or OKR |
   | Debugging | debugger, root-cause-identifier | ReACT + 5 Whys |
   | Optimization | doc-reference-optimizer, context-optimizer | SCAMPER + DMAIC |
   | Agent Lifecycle | agent-architect | CAGEERF + SCAMPER |

2. **Framework Detection**: Find all framework references in agent definition
   - Grep for: OODA, ReACT, CAGEERF, 5 Whys, SCAMPER, DMAIC, Pre-Mortem, Cynefin, Build-Measure-Learn, First Principles, OKR, Disney Creative Strategy
   - Note: Mention alone is insufficient (Grade C or below)

3. **Integration Depth Analysis**: Score how deeply framework is applied
   - Count total workflow phases/steps
   - For each phase, check for:
     - Framework phase terminology (e.g., OBSERVE/ORIENT/DECIDE/ACT for OODA)
     - Explicit deliverables per phase (→ Output: ...)
     - Framework-aligned decision points
   - Calculate: `integration_depth = phases_with_framework / total_phases`

4. **Phase-Framework Alignment**: Verify each workflow phase uses appropriate framework
   | OODA Phase | Recommended Frameworks | Purpose |
   |------------|----------------------|---------|
   | OBSERVE | Cynefin, OKR, 5W1H | Problem classification, goal definition |
   | ORIENT | ReACT, 5 Whys, CAGEERF, First Principles | Analysis, root cause, context building |
   | DECIDE | SCAMPER, Pre-Mortem, Cynefin | Alternative generation, risk assessment |
   | ACT | Build-Measure-Learn, DMAIC, Disney Creative Strategy | Execution, validation, quality control |

### Scoring Rubric

| Grade | Integration Depth | Framework Match | Criteria |
|-------|------------------|-----------------|----------|
| **A** | ≥0.75 | Optimal | Framework applied in 4+ workflow steps with explicit phase deliverables |
| **B** | 0.50-0.74 | Good | Framework applied in 2-3 steps, minor gaps |
| **C** | 0.25-0.49 | Acceptable | Framework mentioned, applied to 1 step only |
| **D** | <0.25 | Mismatch | Framework mentioned but never applied in workflow OR wrong framework |
| **F** | 0.0 | Missing | No framework when domain requires one OR completely wrong choice |

### Calibration Examples

**Grade A - Full Integration (integration_depth = 0.80)**:
```markdown
## Domain: Tech Debt Investigation Agent
## Frameworks: DMAIC (primary) + 5 Whys (secondary)
## Workflow (OODA-Structured):

### OBSERVE Phase (Cynefin)
1. Classify problem complexity (Simple/Complicated/Complex)
→ Output: problem_classification, approach_strategy

### ORIENT Phase (DMAIC: Define + Measure + Analyze)
2. DEFINE: Scope boundaries, success criteria
3. MEASURE: Collect baseline metrics (LOC, complexity, coverage)
4. ANALYZE: Apply 5 Whys for root cause on hotspots
→ Output: baseline_metrics, root_causes[], hotspots[]

### DECIDE Phase (Pre-Mortem)
5. Prioritize by Impact/Effort matrix
6. Pre-mortem: "If remediation fails, why?"
→ Output: prioritized_items[], risk_mitigations[]

### ACT Phase (DMAIC: Improve + Control)
7. Generate remediation plan with acceptance criteria
8. Define monitoring controls
→ Output: remediation_plan, control_metrics
```
*Why A: 4 OODA phases mapped, 3 frameworks applied (DMAIC, 5 Whys, Pre-Mortem), explicit deliverables per phase*

**Grade C - Loosely Applied (integration_depth = 0.25)**:
```markdown
## Domain: Tech Debt Agent
## Framework: DMAIC
## Workflow:
1. Read files in scope
2. Calculate metrics
3. Generate report
```
*Why C: DMAIC mentioned but not applied - steps don't follow Define/Measure/Analyze/Improve/Control structure*

**Grade F - Wrong Framework**:
```markdown
## Domain: Debugging Agent
## Framework: OKR (goal-setting)
## Workflow:
1. Set objectives
2. Define key results
3. Track progress
```
*Why F: OKR is for goal-setting, not debugging - should use ReACT + 5 Whys*

### Framework Phase Coverage Checklist

For Grade A, verify agent has frameworks mapped to workflow phases:

- [ ] **OBSERVE phase** has classification or goal-setting framework (Cynefin, OKR, 5W1H)
- [ ] **ORIENT phase** has analysis framework (ReACT, 5 Whys, CAGEERF, First Principles)
- [ ] **DECIDE phase** has decision/risk framework (SCAMPER, Pre-Mortem)
- [ ] **ACT phase** has execution/validation framework (Build-Measure-Learn, DMAIC, Disney)
- [ ] Each phase has explicit deliverables (→ Output: ...)
- [ ] Primary framework matches agent domain per `thinking-frameworks-catalog.md`

---

## Overall Grade Calibration

### Grade A Example (Score >=4.5)
- 17/17 structural criteria pass
- Clear action sequences with explicit tool invocations
- Comprehensive error handling (3+ error types with recovery)
- Schema compliance validated with examples
- 0 unclear instructions

### Grade C Example (Score 2.5-3.49)
- 11-13/17 structural criteria pass
- Workflow described but not step-by-step (3-5 unclear instructions)
- Basic error handling (1 generic catch-all)
- Schema exists but validation not demonstrated
- Some filler words (5-10% density)

### Grade F Example (Score <1.5)
- <9/17 structural criteria pass
- No clear workflow (11+ unclear instructions)
- No error handling
- Missing schema reference
- >10% filler word density
- Passive voice dominant (<60% active)

---

## Integration Notes

- All 7 frameworks applied for comprehensive evaluation (`focus=all`)
- Selective framework application for focused evaluation
- Evidence citations required for all findings (file:line references)
- Quantified impact for all recommendations
- Confidence scoring per framework (0.0-1.0)
