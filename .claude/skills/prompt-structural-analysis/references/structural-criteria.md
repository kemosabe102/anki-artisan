# Structural Criteria Reference

**Purpose**: Complete 16-criterion structural validation checklist for agent prompts

**Version**: 1.0

---

## Scoring

**Pass** = 1 point, **Fail** = 0 points

**Report Format**: X/16 with file:line evidence for each criterion

---

## Category 1: Single Responsibility & Boundaries (3 criteria)

### Criterion 1: Single Responsibility
- **PASS**: Agent has one clear purpose stated in Role & Boundaries
- **FAIL**: Multiple responsibilities or unclear scope
- **Evidence**: Check for "Role & Boundaries" section with single verb/purpose

### Criterion 2: Scope Discipline
- **PASS**: Boundaries section explicitly lists what agent does NOT do
- **FAIL**: No boundaries documented or scope too broad
- **Evidence**: Look for "NOT for:", "Boundaries:", explicit exclusions

### Criterion 3: Domain Scope Limits
- **PASS**: Domain restricted to specific directories/file types
- **FAIL**: Cross-domain without justification or unlimited scope
- **Evidence**: Check for path restrictions, file type limits

---

## Category 2: Schema & Pattern Compliance (4 criteria)

### Criterion 4: Frontmatter Compliance
- **PASS**: Frontmatter contains ONLY officially documented Claude Code fields:
  - `name` (required)
  - `description` (required)
  - `tools`, `model`, `permissionMode`, `skills` (optional)
- **FAIL**: Invalid fields present (version, maturity, temperature, disallowedTools, status, tags) OR incorrect format
- **ACCEPTED (Undocumented)**: `color` field - functional but not in official spec
- **Evidence**: Check frontmatter lines 1-20 for field names and value formats

### Criterion 5: Schema Compliance
- **PASS**: Agent references and extends base-agent.schema.json
- **FAIL**: No schema reference or custom schema without inheritance
- **Evidence**: Search for "schema" references in document

### Criterion 6: Base Pattern Extension
- **PASS**: Agent extends base-agent-pattern.md with documented inherited sections
- **FAIL**: Duplicates base pattern content or no extension reference
- **Evidence**: Look for "Extends:", "Base Agent Pattern Extension"

### Criterion 7: Two-State Model
- **PASS**: Explicitly documents SUCCESS and FAILURE response structures
- **FAIL**: Missing state model or custom states without justification
- **Evidence**: Search for SUCCESS/FAILURE documentation

---

## Category 3: Tool & Workflow Architecture (3 criteria)

### Criterion 8: Performance-First Tool Selection
- **PASS**: Tools match performance tier:
  - Tier 1: Read, Grep (lightweight)
  - Tier 2: Edit (medium)
  - Tier 3: Write, Bash (heavy)
- **FAIL**: Heavy tools for simple tasks or missing lighter alternatives
- **Evidence**: Check `tools:` frontmatter against agent purpose

### Criterion 9: Workflow Structure
- **PASS**: Complete workflow with phases:
  - Analysis -> Research -> Todo -> Implementation -> Validation -> Reflection
- **FAIL**: Missing phases or workflow not documented
- **Evidence**: Look for "Workflow", "Phase", numbered steps

### Criterion 10: File Operation Protocol
- **PASS**: References file-operation-protocol.md and follows standards
- **FAIL**: No protocol reference or violations (e.g., editing system files)
- **Evidence**: Search for file operation guidance

---

## Category 4: Communication Quality (3 criteria)

### Criterion 11: Tool Descriptions
- **PASS**: Tool usage explained clearly for someone unfamiliar with codebase
- **FAIL**: Vague descriptions or assumes prior knowledge
- **Evidence**: Evaluate tool documentation clarity

### Criterion 12: Explicit Context
- **PASS**: All decisions and context documented explicitly
- **FAIL**: Relies on implicit knowledge or undocumented assumptions
- **Evidence**: Check for "when to use", decision criteria

### Criterion 13: High-Signal Information
- **PASS**: All outputs include actionable next steps or specific findings
- **FAIL**: Generic outputs or missing implementation guidance
- **Evidence**: Review output format specifications

---

## Category 5: Integration Patterns (3 criteria)

### Criterion 14: Four-Component Delegation (Orchestrators)
- **PASS**: Orchestrator agents delegate with objective/format/guidance/boundaries
- **FAIL**: Incomplete delegation context or missing components
- **N/A**: Not an orchestrator agent
- **Evidence**: Check delegation patterns if orchestrator role

### Criterion 15: Query Classification (Research Agents)
- **PASS**: Research agents classify queries and apply appropriate strategies
- **FAIL**: Single strategy for all queries or no classification
- **N/A**: Not a research agent
- **Evidence**: Look for query type handling

### Criterion 16: Parallel Execution Awareness
- **PASS**: Documents parallel execution support or serialization requirements
- **FAIL**: No parallel execution guidance or conflicts possible
- **Evidence**: Search for "parallel", "concurrent", serialization notes

---

## Scoring Summary

| Category | Criteria | Max Points |
|----------|----------|------------|
| Single Responsibility & Boundaries | 1-3 | 3 |
| Schema & Pattern Compliance | 4-7 | 4 |
| Tool & Workflow Architecture | 8-10 | 3 |
| Communication Quality | 11-13 | 3 |
| Integration Patterns | 14-16 | 3 |
| **Total** | | **16** |

**Note**: Criteria 14-15 may be N/A based on agent type. Score as N/A (not counted) rather than FAIL.
