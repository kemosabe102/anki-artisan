# Naming Conventions Reference

## Primary Rule: kebab-case

**Standard Format**: All lowercase, words separated by hyphens

### File Naming

**Pattern**: `^[a-z0-9]+(-[a-z0-9]+)*\.md$`

**Examples**:
```
✅ CORRECT:
- research-methodology.md
- python-framework-v2.md
- ci-cd-pipeline.md
- kubernetes-deployment-guide.md
- opentelemetry-integration.md

❌ INCORRECT:
- ResearchMethodology.md          # PascalCase
- research_methodology.md          # snake_case
- Research Methodology.md          # Spaces
- research-methodology-v2.0.md    # Decimal version
- research--methodology.md         # Double hyphen
```

### Directory Naming

**Pattern**: `^[a-z0-9]+(-[a-z0-9]+)*/$`

**Examples**:
```
✅ CORRECT:
- code-review/
- development-guides/
- infrastructure-docs/
- api-reference/

❌ INCORRECT:
- Code_Review/        # Underscore + PascalCase
- development guides/ # Space
- Infrastructure/     # PascalCase
- api_reference/      # snake_case
```

## Exceptions (Three Cases Only)

### Exception 1: Major Reference Documents

**Rule**: Use `SCREAMING_SNAKE_CASE.md` for top-level governance docs

**Location**: `00-project/` only

**Examples**:
```
✅ VALID EXCEPTIONS:
- SPEC.md
- COMPONENT_ALMANAC.md
- STRATEGIC_VISION.md
- ROADMAP-Q1-2026.md
- LIVING_SPRINT.md
- MATURITY_MATRIX.md

❌ INVALID (wrong location):
- 04-guides/DEVELOPMENT_GUIDE.md   # Not in 00-project/
- 02-architecture/DESIGN.md        # Not top-level governance
```

**Detection**: File in `00-project/` AND matches `^[A-Z]+(_[A-Z]+)*(-[A-Z0-9]+)*\.md$`

### Exception 2: Nested SPEC Files

**Rule**: Use `SPEC.md` inside numbered specification directories

**Location**: `01-planning/specifications/NNN-name/SPEC.md`

**Examples**:
```
✅ VALID:
- 01-planning/specifications/001-research-system/SPEC.md
- 01-planning/specifications/042-agent-framework/SPEC.md

❌ INVALID:
- 01-planning/specifications/research-system-spec.md   # Not SPEC.md
- 01-planning/features/001-new-agent/SPEC.md          # Wrong parent (features)
```

**Purpose**: Clearly identify formal specification documents

### Exception 3: Numbered Stage Files

**Rule**: Use `NN-TITLE.md` for sequential workflow stages

**Location**: `01-planning/features/NNN-name/` only

**Format**: `^[0-9]{2}-[A-Z]+\.md$`

**Examples**:
```
✅ VALID:
- 01-planning/features/001-new-agent/01-RESEARCH.md
- 01-planning/features/001-new-agent/02-PLAN.md
- 01-planning/features/001-new-agent/03-TASKS.md

❌ INVALID:
- 01-planning/features/001-new-agent/1-RESEARCH.md     # Single digit
- 01-planning/features/001-new-agent/01-research.md    # Lowercase
- 01-planning/specifications/001-spec/01-RESEARCH.md   # Wrong parent
```

**Purpose**: Indicate sequential execution order within feature workflow

## Numbered Directories

### Planning Specifications

**Format**: `NNN-kebab-case-description/`

**Pattern**: `^[0-9]{3}-[a-z0-9]+(-[a-z0-9]+)*/$`

**Examples**:
```
✅ CORRECT:
- 001-research-planner-agent/
- 042-secure-research-system/
- 100-kubernetes-deployment/

❌ INCORRECT:
- 1-research-planner/          # Not zero-padded
- 042_secure_research/         # Underscore
- 042-Secure-Research/         # PascalCase
```

### Architecture Decision Records (ADRs)

**Format**: `adr-NNN-kebab-case-description.md` (FILES, not directories)

**Pattern**: `^adr-[0-9]{3}-[a-z0-9]+(-[a-z0-9]+)*\.md$`

**Location**: `02-architecture/decisions/`

**Examples**:
```
✅ CORRECT:
- adr-001-llm-module-consolidation.md
- adr-042-postgres-timescaledb.md
- adr-100-kubernetes-orchestration.md

❌ INCORRECT:
- adr-1-llm-consolidation.md      # Not zero-padded
- ADR-001-consolidation.md        # Uppercase ADR
- 001-adr-consolidation.md        # Wrong prefix order
- adr-001/                        # Directory (should be file)
```

## Version Suffixes

**Format**: `-vN` (NOT `.0` or `_version`)

**Examples**:
```
✅ CORRECT:
- python-framework-v2.md
- api-spec-v3.md
- deployment-guide-v1.md

❌ INCORRECT:
- python-framework-v2.0.md        # Decimal version
- api-spec-version-3.md           # Spelled out
- deployment-guide_v1.md          # Underscore
- framework-2.md                  # No 'v' prefix
```

**Versioning Rules**:
- Increment version on MAJOR revision
- Keep old version in archive if needed for reference
- Only use versions when necessary (avoid v1 for initial docs)

## Compliance Detection

### Validation Regex Patterns

**Standard File**: `^[a-z0-9]+(-[a-z0-9]+)*\.md$`

**Standard Directory**: `^[a-z0-9]+(-[a-z0-9]+)*/$`

**Numbered Directory**: `^[0-9]{3}-[a-z0-9]+(-[a-z0-9]+)*/$`

**ADR File**: `^adr-[0-9]{3}-[a-z0-9]+(-[a-z0-9]+)*\.md$`

**Major Reference Doc**: `^[A-Z]+(_[A-Z]+)*(-[A-Z0-9]+)*\.md$`

**Stage File**: `^[0-9]{2}-[A-Z]+\.md$`

### Violation Indicators

**Automatic Rejection**:
- Contains spaces: `Research Methodology.md`
- Contains underscores (non-exception): `research_methodology.md`
- PascalCase (non-exception): `ResearchMethodology.md`
- camelCase: `researchMethodology.md`
- Multiple consecutive hyphens: `research--methodology.md`
- Missing .md extension: `research-methodology`
- Ends with hyphen: `research-methodology-.md`
- Starts with hyphen: `-research-methodology.md`

**Context-Dependent Violations**:
- SCREAMING_SNAKE_CASE outside `00-project/`: Misplaced exception
- `SPEC.md` outside numbered spec directory: Incorrect usage
- `NN-TITLE.md` outside feature directory: Wrong location
- Numbered directory with single digit: `1-name/` → should be `001-name/`

## Common Transformation Patterns

### From PascalCase

```
Python Code Review Framework v2.md
→ python-code-review-framework-v2.md
```

### From snake_case

```
ci_cd_pipeline_spec.md
→ ci-cd-pipeline-spec.md
```

### From Spaces

```
Kubernetes Workflows_ Kustomize.md
→ kubernetes-workflows-kustomize.md
```

### From Mixed

```
OpenTelemetry_Observability_Strategy.md
→ opentelemetry-observability-strategy.md
```

## Edge Cases

### Acronyms

**Rule**: Lowercase in kebab-case (except SCREAMING_SNAKE_CASE exceptions)

```
✅ CORRECT:
- ci-cd-pipeline.md
- api-reference.md
- llm-integration.md
- adr-001-llm-consolidation.md

❌ INCORRECT:
- CI-CD-pipeline.md
- API-reference.md
- LLM-integration.md
```

### Numbers in Names

**Rule**: Treat numbers as words, hyphenate if multi-part

```
✅ CORRECT:
- python-3-11-guide.md
- v2-migration-plan.md
- adr-001-consolidation.md

❌ INCORRECT:
- python311guide.md    # No hyphens between parts
- v2MigrationPlan.md   # PascalCase
```

### Special Characters

**Rule**: Remove or convert to hyphen

```
✅ CORRECT:
- test-and-validation.md
- before-after-analysis.md

❌ INCORRECT:
- test&validation.md
- before/after-analysis.md
- test+validation.md
```
