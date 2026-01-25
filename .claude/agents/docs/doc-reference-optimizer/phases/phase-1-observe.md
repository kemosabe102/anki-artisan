# Phase 1: OBSERVE - Target Agent Analysis

**OODA Stage**: OBSERVE | **Time Allocation**: 15-20%

**Purpose**: Load target agent, establish baseline token count, extract all sections for analysis

**Deliverable**: Parsed agent structure with token estimates per section

---

## Workflow Steps

### Step 1.1: Target Agent Loading

**Input**: Agent name or path from orchestrator task

**Process**:
1. Locate agent file: `Glob(".claude/agents/**/{agent_name}*.md")`
2. Read complete agent file: `Read(agent_path)`
3. Validate file structure (frontmatter + body)

**Output**: Raw agent content with file path confirmed

### Step 1.2: Frontmatter Extraction

**Input**: Raw agent content


**Process**:
1. Parse YAML frontmatter (between `---` delimiters)
2. Extract: name, description, model, tools
3. Handle malformed YAML: skip frontmatter, note in warnings

**Output**: Structured frontmatter data or warning flag

### Step 1.3: Section Extraction

**Input**: Agent body content (after frontmatter)

**Process**:
1. Split on H2 headers (`## Section Name`)
2. Extract section names and content boundaries
3. Record line numbers for each section

**Output**: Array of sections with names, content, line ranges

### Step 1.4: Baseline Token Estimation

**Input**: Extracted sections

**Process**:
1. Calculate tokens per section: `characters / 4`
2. Sum total agent tokens
3. Record per-section token counts

**Output**: Token baseline with per-section breakdown


---

## Quick Checklist

Before advancing to Phase 2 (ORIENT):

- [ ] Target agent file located and readable
- [ ] Frontmatter parsed (or warning noted)
- [ ] All sections extracted with line numbers
- [ ] Baseline token count calculated (total + per-section)
- [ ] Section boundaries validated (no overlaps)

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping frontmatter validation | Always attempt parse, note errors in warnings |
| Counting headers in token estimate | Include all content (headers contribute to tokens) |
| Missing nested sections | Handle H3/H4 as part of parent H2 section |
| Incorrect line number tracking | Use 1-indexed line numbers consistent with Read tool |

---

## Exit Criteria

**All criteria must pass to proceed**

| Criterion | Weight | Check |
|-----------|--------|-------|
| Agent file loaded | 0.30 | Read tool returns content |
| Sections extracted | 0.30 | At least 1 section identified |
| Token baseline set | 0.25 | Total > 0 with per-section breakdown |
| Structure validated | 0.15 | No parsing errors (warnings acceptable) |

---

**Next Phase**: [Phase 2: ORIENT](phase-2-orient.md)
