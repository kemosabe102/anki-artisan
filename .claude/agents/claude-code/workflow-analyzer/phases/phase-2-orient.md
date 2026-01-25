# Phase 2: ORIENT - Analysis & Research

**OODA Stage**: ORIENT | **Time Allocation**: 25-30%

**Purpose**: Analyze step ordering, verify agent/skill existence, research patterns via Context7, calculate CQ score

**Deliverable**: Dependency validation, existence checks, pattern analysis, CQ assessment

---

## Workflow Steps

### Step 2.1: Topological Step Ordering Analysis

**Input**: Steps and dependencies from Phase 1

**Process**:
1. Build directed acyclic graph (DAG) from step dependencies
2. Perform topological sort to verify ordering
3. Detect cycles (circular dependencies)
4. Identify parallel-safe step groups

**Validation Rules**:
- Step N cannot depend on output of Step M where M > N
- Parallel steps must not share mutable state
- Gate steps must precede gated operations

**Output**: `{ ordering_valid: boolean, cycles: Cycle[], parallel_groups: Group[] }`

### Step 2.2: Agent Existence Verification

**Input**: `agents_referenced` from Phase 1

**Process**:
1. For each agent name:
   - Glob for `.claude/agents/**/{agent-name}.md`
   - Glob for `.claude/agents/**/{agent-name}/{agent-name}.md`
2. Load agent frontmatter if found
3. Extract declared tools
4. Compare agent tools with workflow requirements


**Output**: 
```json
{
  "agents": [
    {
      "name": "agent-name",
      "exists": true,
      "path": ".claude/agents/domain/agent-name.md",
      "tools": ["Read", "Write", "Grep"],
      "tools_sufficient": true
    }
  ],
  "missing_agents": ["unknown-agent"]
}
```

### Step 2.3: Skill Availability Check

**Input**: `skills_required` from Phase 1

**Process**:
1. For each skill reference:
   - Glob for `.claude/skills/{skill-name}/SKILL.md`
2. Verify skill file exists and readable
3. Check skill dependencies (nested skills)

**Output**: `{ skills_found: string[], skills_missing: string[] }`

### Step 2.4: Pattern Research via Context7

**Input**: Workflow patterns identified, similar commands

**Process**:
1. Identify workflow pattern type (linear, branching, parallel)
2. Research best practices for pattern via Context7 if needed
3. Compare against known good patterns from `workflow-patterns-checklist.md`
4. Note deviation from established patterns

**When to Research**:
- Novel workflow pattern not in local knowledge base
- Complex parallelization requirements
- Unusual error recovery needs

**Output**: `{ patterns_identified: Pattern[], best_practices: string[] }`


### Step 2.5: CQ Score Calculation

**Input**: All findings from Steps 2.1-2.4

**Process**:
Calculate Context Quality score:

| Factor | Weight | Calculation |
|--------|--------|-------------|
| Ordering clarity | 0.25 | 1.0 if DAG valid, 0.0 if cycles |
| Agent availability | 0.25 | found_agents / total_agents |
| Skill availability | 0.20 | found_skills / total_skills |
| Pattern alignment | 0.15 | deviation_score from best practices |
| Documentation | 0.15 | completeness of workflow description |

**Formula**: `CQ = SUM(factor_score x weight)`

**Output**: `{ cq_score: float, factors: object, gaps: string[] }`

---

## Exit Criteria

**CQ >= 0.85 required to proceed to DECIDE**

| Criterion | Weight | Check |
|-----------|--------|-------|
| Ordering analyzed | 0.25 | DAG built, cycles detected |
| Agents verified | 0.25 | All Task() targets checked |
| Skills checked | 0.25 | All Skill() references verified |
| CQ calculated | 0.25 | Score computed with factors |

**If CQ < 0.85**: Document gaps, determine if blocking or can proceed with assumptions.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping agent verification | ALWAYS check .claude/agents/ for each Task() |
| Missing skill dependencies | Check nested skill references |
| Ignoring implicit ordering | Analyze output->input data flow |
| Not calculating CQ | Required gate for DECIDE phase |

---

**Previous Phase**: [Phase 1: OBSERVE](phase-1-observe.md)
**Next Phase**: [Phase 3: DECIDE](phase-3-decide.md)
