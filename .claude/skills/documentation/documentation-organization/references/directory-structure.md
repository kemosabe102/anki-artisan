# Directory Structure Reference

## Standard Hierarchy

### Main Documentation Tree (`docs/`)

```
docs/
├── 00-project/          # Project governance & strategy
├── 01-planning/         # Active planning work
├── 02-architecture/     # Architecture decisions & design
├── 03-implementation/   # Implementation artifacts
├── 04-guides/           # How-to guides & best practices
├── 05-reference/        # Look-up information
└── 06-archive/          # Historical documents
```

### Claude Documentation Tree (`.claude/docs/`)

```
.claude/docs/
├── 00-core/             # Orchestrator rules, frameworks, thresholds
├── 01-guides/           # Agent selection, file ops, skills
├── 02-patterns/         # Reusable patterns (base-agent, etc.)
└── 03-workflows/        # Orchestration workflows
```

## Lifecycle Stages

### Visual Flow

```
User Need/Feature Idea
    ↓
00-project/ ────────────► Strategic alignment check
    ↓                     (Is this on roadmap? Does component exist?)
01-planning/ ───────────► Create specification or feature plan
    ↓                     (specifications/ for large, features/ for small)
02-architecture/ ───────► Design decisions via ADRs
    ↓                     (Technology selection, structural changes)
03-implementation/ ─────► Implementation details & artifacts
    ↓                     (Component specs, infrastructure, integrations)
04-guides/ ─────────────► Extract reusable patterns & how-tos
    ↓                     (Workflows, domain knowledge, templates)
05-reference/ ──────────► Formalize into reference documentation
    ↓                     (API docs, schemas, glossary)
06-archive/ ────────────► When obsolete or superseded
                          (Preserve with git history)
```

### Stage Definitions

| Stage | Purpose | Typical Lifetime | Move Trigger |
|-------|---------|------------------|--------------|
| 00-project | Governance & strategy | Permanent | Never (update in place) |
| 01-planning | Active planning | Days to weeks | Implementation complete |
| 02-architecture | Design decisions | Permanent | Superseded by new ADR |
| 03-implementation | Technical details | Months to years | Component deprecated |
| 04-guides | Reusable workflows | Years | Process obsolete |
| 05-reference | Lookup information | Years | API version deprecated |
| 06-archive | Historical record | Permanent | N/A (final destination) |

## Directory Details

### 00-project/ - Project Governance

**Purpose**: Single source of truth for project-level decisions

**Structure**:
```
00-project/
├── SPEC.md                      # System requirements & architecture
├── COMPONENT_ALMANAC.md         # Component inventory (CHECK BEFORE NEW CODE)
├── roadmaps/
│   ├── active/                  # Current planning horizons (QN-YYYY.md)
│   └── archive/                 # Completed roadmaps
├── strategy/                    # Strategic documents
│   ├── STRATEGIC_VISION.md
│   ├── MATURITY_MATRIX.md
│   └── SECURITY.md
├── operations/                  # Day-to-day operations
│   ├── LIVING_SPRINT.md         # Current sprint (updated daily/weekly)
│   └── PLANNING_GUIDE.md
└── templates/                   # Project-level templates
```

**Allowed Files**:
- Major docs: `SCREAMING_SNAKE_CASE.md`
- Roadmaps: `QN-YYYY.md` (e.g., Q1-2026.md)
- Others: `kebab-case.md`

**Prohibited**:
- Implementation details (→ 03-implementation/)
- Feature-specific plans (→ 01-planning/)
- How-to guides (→ 04-guides/)

### 01-planning/ - Active Planning Work

**Purpose**: All active planning artifacts organized by methodology

**Structure**:
```
01-planning/
├── specifications/              # SDD-style heavyweight specs
│   ├── NNN-descriptive-name/
│   │   ├── SPEC.md             # Main specification
│   │   ├── research/           # Research findings
│   │   ├── plans/              # Implementation plans
│   │   └── review/             # Review artifacts
│   └── template.md
├── features/                    # Lightweight feature plans
│   ├── NNN-descriptive-name/
│   │   ├── 01-RESEARCH.md      # Research phase
│   │   ├── 02-PLAN.md          # Planning phase
│   │   └── 03-TASKS.md         # Task breakdown
│   └── template.md
└── custom/                      # Custom workflows & frameworks
    └── kebab-case.md
```

**Planning Type Selection**:

| Type | Use When | Effort | Examples |
|------|----------|--------|----------|
| specifications/ | Large features, cross-cutting, formal review | 3+ sprints | Multi-agent systems, SDLC frameworks |
| features/ | Small-medium features, clear scope | 1-2 sprints | New agent, integration, enhancement |
| custom/ | Frameworks, methodologies, reusable patterns | Variable | Delegation patterns, workflows |

**Numbered Directory Rules**:
- Format: `NNN-kebab-case-description/` (001-, 002-, 003-, ...)
- Sequential numbering within each subdirectory
- Never reuse numbers (even after archival)

**Lifecycle Exit**:
- When implementation complete → Move to `06-archive/projects/`
- Preserve git history with `git mv`

### 02-architecture/ - Architecture Decisions

**Purpose**: Record significant architectural decisions

**Structure**:
```
02-architecture/
├── ARCHITECTURE.md              # System architecture overview
├── decisions/                   # Architecture Decision Records
│   ├── adr-NNN-descriptive.md  # Individual ADRs
│   └── template.md
├── design/                      # Design documents
│   └── component-design.md
└── research/                    # Architecture exploration
    └── pattern-research.md
```

**ADR Naming**: `adr-NNN-descriptive-name.md` (FILES, not directories)

**ADR Lifecycle**:
1. Create with status "Proposed"
2. Link from relevant spec in `01-planning/`
3. Update to "Accepted" after approval
4. When superseded: Update to "Superseded", add pointer to new ADR
5. Never delete superseded ADRs (preserve history)

**When to Create ADR**:
- Technology selection (framework, library, service)
- Structural changes (module organization, boundaries)
- Cross-cutting patterns (error handling, observability)
- Integration approaches

### 03-implementation/ - Implementation Artifacts

**Purpose**: Detailed implementation specifications and operational docs

**Structure**:
```
03-implementation/
├── components/                  # Component-level specs
│   └── kebab-case.md
├── infrastructure/              # DevOps & deployment
│   ├── ci-cd/
│   ├── observability/
│   └── caching/
└── integrations/                # External integrations
    ├── ollama/
    ├── mcp/
    └── examples/
```

**Content Types**:
- Component specifications (data models, APIs)
- Infrastructure setup guides
- Integration implementation details
- Configuration documentation

**Prohibited**:
- How-to workflows (→ 04-guides/)
- Reference material (→ 05-reference/)
- Planning documents (→ 01-planning/)

### 04-guides/ - How-To Guides

**Purpose**: Reusable guidance extracted from implementation experience

**Structure**:
```
04-guides/
├── development/                 # Development workflows
├── code-review/                 # Review frameworks
├── domain/                      # Domain knowledge
├── claude-code/                 # Claude Code specific
├── kubernetes/                  # Kubernetes workflows
├── personas/                    # Role-specific guides
└── templates/                   # Reusable templates
```

**Guide Criteria**:
- ✅ Reusable across multiple features
- ✅ Teaches "how to" do something
- ✅ Based on actual experience
- ❌ Not feature-specific implementation details

**Template Consolidation**:
- All reusable templates → `04-guides/templates/`
- Planning templates → `00-project/templates/`
- ADR template → `02-architecture/decisions/template.md`

### 05-reference/ - Reference Documentation

**Purpose**: Look-up information for APIs, schemas, and terminology

**Structure**:
```
05-reference/
├── glossary.md                  # Project terminology
├── api/                         # API documentation
│   └── kebab-case.md
└── schemas/                     # Data schemas & contracts
    └── kebab-case.md
```

**Content Types**:
- API documentation (generated or manual)
- JSON/YAML schemas
- Glossary terms
- Quick reference sheets

**Key Distinction**:
- **Guides** (04-guides/): "How to do X" (procedural)
- **Reference** (05-reference/): "What is X?" (definitional)

### 06-archive/ - Historical Documents

**Purpose**: Preserve completed/obsolete documents without clutter

**Structure**:
```
06-archive/
├── roadmaps/                    # Completed roadmaps
├── projects/                    # Completed project artifacts
├── planning/                    # Old planning documents
└── deprecated/                  # Obsolete documents
```

**When to Archive**:
- ✅ Document no longer actively referenced
- ✅ Information is historical/reference only
- ✅ Superseded by newer documentation
- ❌ Still actively used for decisions

**Archival Process**:
1. Move document to appropriate archive subdirectory
2. Add archive note at top with date and reason
3. Update cross-references if needed
4. Preserve git history (use `git mv` via orchestrator)

## Placement Decision Tree

**Quick Decision Logic**:

```
Is this document about...

├─ PROJECT GOVERNANCE?
│  ├─ Roadmap/strategic vision? → 00-project/roadmaps/ or /strategy/
│  ├─ Current sprint tracking? → 00-project/operations/LIVING_SPRINT.md
│  ├─ System specification? → 00-project/SPEC.md
│  └─ Component inventory? → 00-project/COMPONENT_ALMANAC.md
│
├─ PLANNING NEW FEATURE/SYSTEM?
│  ├─ Large, formal spec? → 01-planning/specifications/NNN-name/
│  ├─ Small feature? → 01-planning/features/NNN-name/
│  └─ Custom workflow? → 01-planning/custom/
│
├─ ARCHITECTURE DECISION?
│  ├─ ADR? → 02-architecture/decisions/adr-NNN-*.md
│  ├─ Design doc? → 02-architecture/design/
│  └─ Research? → 02-architecture/research/
│
├─ IMPLEMENTATION DETAIL?
│  ├─ Component spec? → 03-implementation/components/
│  ├─ Infrastructure/DevOps? → 03-implementation/infrastructure/
│  └─ Integration? → 03-implementation/integrations/
│
├─ HOW-TO GUIDE?
│  ├─ Development workflow? → 04-guides/development/
│  ├─ Code review? → 04-guides/code-review/
│  ├─ Domain knowledge? → 04-guides/domain/
│  └─ Reusable template? → 04-guides/templates/
│
├─ REFERENCE INFORMATION?
│  ├─ API docs? → 05-reference/api/
│  ├─ Schemas? → 05-reference/schemas/
│  └─ Glossary? → 05-reference/glossary.md
│
└─ NO LONGER ACTIVE?
   ├─ Completed roadmap? → 06-archive/roadmaps/
   ├─ Completed project? → 06-archive/projects/
   └─ Obsolete? → 06-archive/deprecated/
```

## Validation Rules

### Directory Existence

**Required Directories** (must exist):
- `docs/00-project/`
- `docs/01-planning/`
- `docs/02-architecture/`

**Optional Directories** (may exist):
- All other numbered directories (03-06)
- Subdirectories within allowed directories

**Prohibited Directories**:
- `docs/07-*` or higher (invalid lifecycle stage)
- Directories outside `docs/` or `.claude/docs/`
- Directories with spaces or invalid characters
- Single-file directories (orphans)

### File Placement

**Per-Directory Rules**:

| Directory | Allowed Files | Prohibited Files |
|-----------|---------------|------------------|
| `00-project/` | SCREAMING_SNAKE_CASE.md, QN-YYYY.md, kebab-case.md | Feature specs, implementation details |
| `01-planning/specifications/NNN-*/` | SPEC.md, kebab-case.md | Standalone specs outside numbered dirs |
| `01-planning/features/NNN-*/` | NN-TITLE.md, kebab-case.md | SPEC.md (reserved for specifications) |
| `02-architecture/decisions/` | adr-NNN-name.md, template.md | Other file patterns |
| `03-implementation/` | kebab-case.md only | SCREAMING_SNAKE_CASE, workflows |
| `04-guides/` | kebab-case.md only | Implementation details |
| `05-reference/` | kebab-case.md, glossary.md | How-to workflows |
| `06-archive/` | Any (preserve original names) | New documents (archive only) |

### Cross-Directory Constraints

**One Spec Per Directory**:
- Each `01-planning/specifications/NNN-*/` contains exactly ONE `SPEC.md`
- Multiple supporting files allowed (research/, plans/, review/)

**ADRs Are Files, Not Directories**:
- `adr-NNN-name.md` (correct)
- `adr-NNN-name/` (incorrect)

**Templates Consolidated**:
- Reusable templates → `04-guides/templates/`
- Domain templates scattered across directories → Violation

## Common Violations

### Single-File Directories

**Problem**: Directory contains only one .md file

```
❌ INCORRECT:
docs/orchestrator/
└── pain-point-validation.md
```

**Solution**: Move to appropriate category

```
✅ CORRECT:
docs/04-guides/templates/
├── pain-point-validation.md
└── other-templates.md
```

### Mixed Document Types

**Problem**: Different planning types in same directory

```
❌ INCORRECT:
01-planning/
├── 001-feature-spec/SPEC.md     # Heavyweight spec
├── quick-plan.md                # Lightweight plan
└── research-notes.md            # Research artifact
```

**Solution**: Use appropriate subdirectories

```
✅ CORRECT:
01-planning/
├── specifications/001-feature-spec/SPEC.md
├── features/002-quick-plan/02-PLAN.md
└── custom/research-notes.md
```

### Invalid Lifecycle Stage

**Problem**: Directory number > 06 or < 00

```
❌ INCORRECT:
docs/07-future/
docs/99-misc/
```

**Solution**: Use existing lifecycle stages (00-06 only)

### Misplaced Implementation Details

**Problem**: How-to guide in implementation directory

```
❌ INCORRECT:
docs/03-implementation/infrastructure/kubernetes-deployment-workflow.md
```

**Solution**: Move to guides

```
✅ CORRECT:
docs/04-guides/kubernetes/deployment-workflow.md
```
