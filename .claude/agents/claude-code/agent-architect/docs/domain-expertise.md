# Agent Architect Domain Expertise

## Operations Reference

### 1. Agent Creation (`create_agent`)

**Input**: Agent requirements, research context, design constraints

**Process**:
1. **Directory Bootstrapping** (30 sec):
   - Determine domain from agent scope (dev-tools/investing/research/etc.)
   - Create base directory: `.claude/agents/{domain}/{agent-name}/`
   - Create subdirectories: `docs/`, `examples/`, `schemas/`
   - Copy scaffold README files from `.claude/templates/agent-scaffold/`

2. **Simulation** - Think from agent's perspective, identify needs
3. **Research** - Best practices from template and guides
4. **Framework Selection** - Identify appropriate thinking framework(s)
5. **Design** - Specification aligned with template structure
6. **Validation** - Component standards, template compliance
7. **Evaluation** - Apply quality matrix, self-improvement loop
8. **Integration** - Schema validation, workflow integration

**Output Structure**:
```
.claude/agents/{domain}/{agent-name}/
├── {agent-name}.md           # Main agent definition
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

### 2. Agent Evaluation (`evaluate_agent`)

**Input**: Agent file path, evaluation fixtures, external validation data

**Process**:
1. Load agent → Parse frontmatter
2. Apply quality matrix evaluation (9 criteria)
3. Calculate weighted grades
4. Generate recommendations
5. Version assessment
6. Self-improvement suggestions

**Description-Capability Alignment Evaluation**:
Validate against Description Delegation Checklist:
1. ✅ Clear trigger condition ("Use proactively when...", "MUST BE USED for...")
2. ✅ Proactive delegation signal (encourages auto-delegation)
3. ✅ Domain keywords for semantic matching
4. ✅ Action-oriented language (present tense verbs)
5. ✅ Role/expertise declaration

**Score 0-5**:
- 5: All 5 delegation criteria met
- 4: 4/5 criteria met
- 3: 3/5 criteria met
- 2: 2/5 criteria met
- 1: 1/5 criteria met
- 0: Description unusable for delegation

### 3. Feedback Implementation (`implement_feedback`)

**Input**: Target agent name and clear feedback description
**Process**: Feedback analysis → Change planning → Apply changes immediately → Validation → Documentation

### 4. Agent Updates (`update_agent`)

**Input**: Agent name, update specifications, version strategy
**Process**: Backup → Change application → Template compliance → Component validation → Version management → Workflow synchronization


### 5. Design Guide Creation (`create_design_guide`)

**Input**: Design guide requirements, observed practices, target audience
**Process**: Practice analysis → Pattern documentation → Guide structure → Integration

### 6. Workflow Validation (`validate_workflow`)

**Input**: Workflow validation specifications, agent change list
**Process**: Agent legend validation → Capability analysis → Maturity calculation → Discrepancy detection

### 7. Maturity Update (`update_maturity`)

**Input**: Agent name, new maturity version, rationale
**Process**: Maturity assessment → Impact analysis → Workflow update → Validation

### 8. Agent Idea Analysis (`analyze_agent_idea`)

**Purpose**: Analyze user's rough agent idea and generate structured proposal with confidence-scored recommendations.

**Process**:
1. **Parse User Intent** - Extract problem domain, work type, mentioned tools
2. **Domain Research** - Check COMPONENT_ALMANAC.md, search codebase
3. **Generate Proposal** - Name options, domain scope, type, purpose, capabilities, inputs, outputs, knowledge areas, tools, integration points

**Quality Gate**: Confidence ≥0.50 for all sections to proceed

### 9. Agent Definition Generation (`generate_agent_definition`)

**Purpose**: Generate complete agent definition file from refined requirements.

**Process**:
1. **Load Template** - Read `agent-definition-input.template.md`
2. **Fill All 14 Sections** - Basic info through additional context
3. **Validate Completeness** - All sections filled, follows structure
4. **Write File** - Output to specified path

### 10. Populate Agent Subdirectories (`populate_subdirectories`)

**Purpose**: Populate docs/, examples/, schemas/ for new agent directory.

**Process**:
1. **Populate schemas/** - Generate schema extending base-agent.schema.json
2. **Populate docs/** - Generate domain-expertise.md, frameworks.md, README.md
3. **Populate examples/** - Generate basic-usage.md, additional examples
4. **Validate Structure** - Verify all files exist, links correct

---

## Valid Frontmatter Fields (Claude Code Specification)

**ONLY these fields are allowed**:
- **name** (required): Unique identifier using lowercase letters and hyphens
- **description** (required): Natural language description of purpose
- **tools** (optional): Comma-separated list of specific tools
- **model** (optional): opus (recommended), sonnet, haiku, or 'inherit'
- **permissionMode** (optional): default, acceptEdits, bypassPermissions, plan, ignore
- **skills** (optional): Comma-separated list of skill names
- **color** (optional): Visual identifier (purple, blue, green, etc.)

**INVALID fields** (will cause errors):
- ❌ `version`, `maturity`, `temperature`, `disallowedTools`, `status`, `tags`

---

## CLAUDE.md Update Protocol

**When to Update**: EVERY agent creation, significant capability change, or domain scope modification

**Location**: `CLAUDE.md` Complete Agent List table

**Update Process**:
1. Read CLAUDE.md to locate the Complete Agent List table
2. Identify correct category section
3. Add new row: `| **agent-name** | domain-scope | use-case-description | type |`
4. Validate formatting preserved

---

## Documentation Reference Standard

**CRITICAL**: Use filename-only references (NOT full paths).

**Why**: Documentation locations change frequently. Claude Code can search entire repository for filename.

**Examples**:
- ❌ WRONG: `.claude/docs/00-core/infuse-framework-quick-ref.md`
- ✅ CORRECT: `infuse-framework-quick-ref.md`

**Exception**: Use relative paths ONLY for schemas or when filename collisions exist.
