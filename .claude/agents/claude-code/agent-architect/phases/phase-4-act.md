# Phase 4: ACT - Execution & Validation

**OODA Stage**: ACT | **Time Allocation**: 50-55%

**Purpose**: Execute approved operation, validate outputs, update CLAUDE.md, complete handoff

**Deliverable**: Completed agent operation with validation evidence

---

## Workflow Steps

### Step 4.1: Directory Structure Creation (CREATE only)

**Input**: Approved agent design, domain assignment

**Process**:
1. Verify parent directory exists via Glob
2. Create base directory: `.claude/agents/{domain}/{agent-name}/`
3. Create subdirectories: `docs/`, `examples/`, `schemas/`
4. Copy scaffold README files from `.claude/templates/agent-scaffold/`

**Output Structure**:
```
.claude/agents/{domain}/{agent-name}/
├── {agent-name}.md
├── docs/
│   ├── README.md
│   ├── domain-expertise.md
│   └── frameworks.md
├── examples/
│   ├── README.md
│   └── basic-usage.md
└── schemas/
    ├── README.md
    └── {agent-name}.schema.json
```


### Step 4.2: File Generation

**Input**: Agent design, template structure

**Process by Operation**:

**CREATE**:
1. Generate `{agent-name}.md` following `agent.template.md` structure
2. Apply frontmatter with valid fields only
3. Reference `base-agent-pattern.md` (inherit, don't duplicate)
4. Generate schema extending `base-agent.schema.json`
5. Populate docs/ with domain-expertise.md, frameworks.md
6. Create examples/ with basic-usage.md

**UPDATE**:
1. Read current agent definition
2. Apply scoped changes
3. Preserve structure and formatting
4. Update version/maturity if applicable

**ANALYZE**:
1. Load agent definition
2. Apply quality matrix
3. Generate evaluation report with scores

**Output**: Generated/updated files

### Step 4.3: Schema Validation

**Input**: Generated agent files

**Process**:
1. Validate frontmatter against spec (7 valid fields only)
2. Validate schema against JSON Schema spec
3. Check description length (<200 chars)
4. Validate description YAML syntax:
   - MUST be single-quoted string on one line: `description: 'text here'`
   - REJECT if uses pipe (`|`) or folded (`>`) multi-line syntax
   - REJECT if description spans multiple lines
   - Error: "Description must be single-quoted string on one line, not YAML multi-line syntax (| or >)"
5. Verify file size (<500 lines for main agent file)
6. Confirm all required sections present

**Output**: Validation results (PASS/FAIL with details)


### Step 4.4: CLAUDE.md Update (CREATE/major UPDATE)

**Input**: New or significantly updated agent

**Process**:
1. Read CLAUDE.md to locate Complete Agent List table
2. Identify correct category section
3. Add/update row: `| **agent-name** | domain-scope | use-case-description | type |`
4. Validate formatting preserved
5. If write fails, provide manual update instructions

**Output**: CLAUDE.md updated or manual fallback provided

### Step 4.5: Completion & Handoff

**Input**: All validated outputs

**Process**:
1. Compile completion evidence:
   - Files created/modified
   - Validation results
   - Quality scores (if ANALYZE)
   - CLAUDE.md update status
2. Generate structured output per schema
3. Include recommendations for next steps

**Output**: Completion report with evidence

---

## Exit Criteria

**All criteria must pass to complete**

| Criterion | Weight | Check |
|-----------|--------|-------|
| Execution complete | 0.30 | All files created/modified |
| Validation passed | 0.30 | Schema, frontmatter valid |
| CLAUDE.md updated | 0.20 | Table entry exists (if required) |
| Evidence documented | 0.20 | Completion report ready |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping validation | ALWAYS validate before completion |
| Forgetting CLAUDE.md | Update Complete Agent List for CREATE |
| Invalid frontmatter | Use ONLY 7 valid fields |
| No evidence | Document specific files and validation results |

---

**Previous Phase**: [Phase 3: DECIDE](phase-3-decide.md)
**Complete**: Return to [agent-architect.md](../agent-architect.md)
