# Phase 2: ORIENT - Simulation & Quality Analysis

**OODA Stage**: ORIENT | **Time Allocation**: 20-25%

**Purpose**: Apply simulation-driven development, evaluate against quality matrix, identify patterns and gaps

**Deliverable**: Design approach, quality assessment, pattern identification, gap analysis

---

## Workflow Steps

### Step 2.1: Simulation-Driven Development

**Input**: Request details, loaded knowledge base

**Process**:
1. **Perspective Shift**: Think FROM the target agent's viewpoint
2. **Needs Identification**: What does this agent need to accomplish its goals?
3. **Tool Requirements**: Which tools are essential? What descriptions do they need?
4. **Work Phases**: Map out decision points and execution stages
5. **Failure Modes**: Identify edge cases and potential failures

**Output**: Agent mental model with needs, tools, phases, failure modes

### Step 2.2: Quality Matrix Application

**Input**: Agent design or existing agent definition

**Process**:
Apply 9-criterion weighted evaluation:

| Criterion | Weight | Score 0-5 |
|-----------|--------|-----------|
| **Correctness** | 0.25 | Task accuracy, external validation |
| **Format Fidelity** | 0.15 | Schema adherence, machine-parseable outputs |
| **Description-Capability Alignment** | 0.10 | Frontmatter reflects capabilities |
| **Scope Discipline** | 0.10 | Avoids role drift, clear boundaries |
| **Tool Use Quality** | 0.10 | Appropriate tool selection/usage |
| **Reliability** | 0.10 | Stable performance across contexts |
| **Safety/Compliance** | 0.10 | No prohibited content, proper refusals |
| **Maintainability** | 0.10 | Prompt clarity, AI-readability, <500 lines |
| **Efficiency+Observability** | 0.05 | Cost optimization, structured logging |

**Grade Calculation**: Weighted sum -> A(4.5-5.0), B(3.5-4.4), C(2.5-3.4), D(1.5-2.4), F(0-1.4)

**Output**: Quality score, grade, per-criterion scores

### Step 2.3: Pattern Identification

**Input**: Agent requirements, template structure

**Process**:
1. Match agent type to framework selection matrix:
   | Agent Category | Primary Framework |
   |----------------|-------------------|
   | Research | ReACT |
   | Implementation | CAGEERF |
   | Analysis/Review | 5W1H + DMAIC |
   | Planning | CAGEERF + OKR |
   | Debugging | ReACT + 5 Whys |
   | Optimization | SCAMPER + DMAIC |


2. Identify similar existing agents for pattern reuse
3. Check `base-agent-pattern.md` for inheritable sections

**Output**: Selected frameworks, similar agents, inheritance plan

### Step 2.4: Gap Detection

**Input**: Current understanding, template requirements

**Process**:
1. Compare design against `agent.template.md` structure
2. Identify missing sections or incomplete information
3. Check frontmatter against valid fields only:
   - `name`, `description`, `tools`, `model`, `permissionMode`, `skills`, `color`
4. Verify description YAML syntax compliance:
   - Single-quoted string format required: `description: 'text'`
   - Multi-line syntax forbidden (| pipe, > folded block)
   - Flag as CRITICAL gap if multi-line detected
5. Verify description meets delegation checklist (5 criteria)
6. Assess if Tier 3 loading needed (COMPONENT_ALMANAC.md)

**Output**: Gap list with resolution requirements

---

## Exit Criteria

**CQ >= 0.85 required to proceed to DECIDE**

| Criterion | Weight | Check |
|-----------|--------|-------|
| Simulation complete | 0.30 | Agent perspective documented |
| Quality assessed | 0.25 | All 9 criteria scored |
| Patterns identified | 0.25 | Frameworks and inheritance selected |
| Gaps resolved | 0.20 | No blocking gaps remain |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping simulation | ALWAYS think from agent's perspective first |
| Using invalid frontmatter | Only use 7 valid fields |
| Ignoring quality matrix | Apply ALL 9 criteria |
| Missing pattern check | Check existing agents for reuse |

---

## Reference Documentation

- `docs/frameworks.md` - Quality framework details
- `agent-quality-taxonomy.md` - Evaluation criteria
- `description-delegation-checklist.md` - Description requirements

---

**Previous Phase**: [Phase 1: OBSERVE](phase-1-observe.md)
**Next Phase**: [Phase 3: DECIDE](phase-3-decide.md)
