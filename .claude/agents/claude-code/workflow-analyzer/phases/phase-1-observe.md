# Phase 1: OBSERVE - Context Gathering

**OODA Stage**: OBSERVE | **Time Allocation**: 15-20%

**Purpose**: Parse command definition, extract workflow steps, identify subagent references, catalog skill dependencies, map tool usage

**Deliverable**: Parsed command structure, dependency graph, initial findings

---

## Pre-Flight Checklist

Before ANY analysis:

- [ ] Command file path validated
- [ ] Command file readable
- [ ] Frontmatter extracted
- [ ] Workflow steps identified
- [ ] Task() patterns cataloged
- [ ] Skill() references listed
- [ ] Tool declarations noted

---

## Workflow Steps

### Step 1.1: Command File Loading

**Input**: Command file path (e.g., `.claude/commands/analyze-agent.md`)

**Process**:
1. Validate path exists via Glob
2. Read command file contents
3. Parse YAML frontmatter
4. Extract body content

**Output**: `{ path: string, frontmatter: object, body: string }`


### Step 1.2: Frontmatter Validation

**Input**: Extracted frontmatter

**Process**:
1. Check required fields:
   - `argument-hint`: Present and descriptive
   - `description`: Present, <200 chars, trigger keywords
   - `allowed-tools`: Present, minimal set
   - `model`: Present (opus, sonnet, haiku)
2. Flag missing/invalid fields

**Output**: `{ valid: boolean, issues: string[] }`

### Step 1.3: Workflow Step Extraction

**Input**: Command body content

**Process**:
1. Identify phase/step markers (## Phase, ### Step)
2. Extract numbered workflow steps
3. Identify conditional branches (if/else, gates)
4. Map step dependencies (explicit and implicit)

**Output**: `{ steps: Step[], phases: Phase[], branches: Branch[] }`

### Step 1.4: Task() Pattern Cataloging

**Input**: Command body content

**Process**:
1. Regex scan for `Task(agent-name, ...)` patterns
2. Extract agent names referenced
3. Note context (parallel vs sequential grouping)
4. Record delegation parameters

**Pattern**: `Task\(([a-z-]+),\s*["'](.+?)["']\)`

**Output**: `{ task_calls: TaskCall[], agents_referenced: string[] }`


### Step 1.5: Skill Reference Cataloging

**Input**: Command body content

**Process**:
1. Scan for `Skill()` or skill reference patterns
2. Extract skill names/paths
3. Note required vs optional skills
4. Map skill to workflow phase

**Output**: `{ skill_refs: SkillRef[], skills_required: string[] }`

### Step 1.6: Tool Usage Mapping

**Input**: Frontmatter `allowed-tools`, body content

**Process**:
1. Parse `allowed-tools` declaration
2. Scan body for tool usage patterns
3. Compare declared vs used tools
4. Flag undeclared tool usage

**Output**: `{ tools_declared: string[], tools_used: string[], discrepancies: string[] }`

---

## Exit Criteria

**All criteria must pass to proceed to ORIENT**

| Criterion | Weight | Check |
|-----------|--------|-------|
| File loaded | 0.25 | Command file accessible and parsed |
| Frontmatter valid | 0.25 | Required fields present |
| Steps extracted | 0.25 | Workflow structure identified |
| Dependencies mapped | 0.25 | Task/Skill/Tool references cataloged |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing frontmatter check | ALWAYS validate frontmatter first |
| Ignoring implicit dependencies | Look for output->input chains |
| Skipping skill references | Scan for both Skill() and skill mentions |
| Missing parallel groupings | Check for "in parallel" language |

---

**Next Phase**: [Phase 2: ORIENT](phase-2-orient.md)
