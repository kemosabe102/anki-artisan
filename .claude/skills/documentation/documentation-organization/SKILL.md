---
name: documentation-organization
description: >
  Enforces documentation structure, naming conventions (kebab-case), and three-tier 
  safety model. Validates directory hierarchy and compliance with DOCS-MANAGEMENT.md rules.
  Use when: "organize docs", "fix naming", "restructure docs", "tier compliance", 
  "directory rules", "kebab-case". 
  NOT for: content validation (documentation-health), token analysis (documentation-optimization).
---

# Documentation Organization

## Overview

This skill enforces the lifecycle-based documentation structure defined in DOCS-MANAGEMENT.md. It validates directory hierarchy (00-project through 06-archive), naming conventions (kebab-case), and organizational compliance across `docs/**` and `.claude/docs/**`.

**Core Principle**: Documentation follows predictable paths from planning → architecture → implementation → guides → reference → archive.

## When to Use This Skill

**Invoke for**:
- Reorganizing documentation after structural changes
- Validating compliance with DOCS-MANAGEMENT.md
- Enforcing kebab-case naming across doc trees
- Auditing directory structure correctness
- Moving documents through lifecycle stages (planning → archive)

**NOT for**:
- Content quality checks (use `documentation-health`)
- Token/context optimization (use `documentation-optimization`)
- Creating new content (use `/spec` command or `researcher-lead`)
- Git operations (orchestrator handles)

## Directory Structure Rules

### Standard Hierarchy

```
docs/
├── 00-project/          # Project governance (SPEC.md, COMPONENT_ALMANAC.md, roadmaps)
├── 01-planning/         # Active planning (specifications/, features/, custom/)
├── 02-architecture/     # Architecture decisions (ADRs, design docs)
├── 03-implementation/   # Implementation artifacts (components/, infrastructure/)
├── 04-guides/           # How-to guides (development/, domain/, templates/)
├── 05-reference/        # Look-up info (api/, schemas/, glossary.md)
└── 06-archive/          # Historical documents (roadmaps/, projects/, planning/)

.claude/docs/
├── 00-core/             # Orchestrator rules, frameworks, thresholds
├── 01-guides/           # Agent selection, file ops, skills
├── 02-patterns/         # Reusable patterns (base-agent, etc.)
└── 03-workflows/        # Orchestration workflows
```

### Lifecycle Flow

Documents progress through stages. This is the EXPECTED path:

```
User Need → 00-project/ (strategic alignment)
         → 01-planning/ (specification/feature plan)
         → 02-architecture/ (ADRs for design decisions)
         → 03-implementation/ (technical details)
         → 04-guides/ (extract reusable patterns)
         → 05-reference/ (formalize into lookup docs)
         → 06-archive/ (when obsolete/superseded)
```

### Placement Decision Logic

**Quick Decision Tree**:

1. **Strategic/Governance?** → `00-project/` (SPEC.md, roadmaps, COMPONENT_ALMANAC.md)
2. **Planning New Feature?** → `01-planning/specifications/` (large) or `features/` (small)
3. **Architecture Decision?** → `02-architecture/decisions/adr-NNN-*.md`
4. **Implementation Detail?** → `03-implementation/components/` or `infrastructure/`
5. **How-To Guide?** → `04-guides/development/`, `domain/`, or `templates/`
6. **Reference Lookup?** → `05-reference/api/`, `schemas/`, or `glossary.md`
7. **No Longer Active?** → `06-archive/` with appropriate subdirectory

**Validation Rules**:
- ONE spec per numbered directory in `01-planning/specifications/`
- ADRs MUST use `adr-NNN-name.md` format (files, not directories)
- Templates go in `04-guides/templates/` (NOT scattered across directories)
- Archive MUST preserve git history (`git mv` required)

## Naming Conventions

### Primary Rule: kebab-case

**Standard Format**: `kebab-case.md` for files, `kebab-case/` for directories

**Examples**:
```
✅ CORRECT:
- python-framework-v2.md
- ci-cd-spec.md
- kubernetes-workflows.md
- 001-research-planner-agent/

❌ INCORRECT:
- Python Code Review Framework v2.md
- ci_cd_spec.md (snake_case)
- OpenTelemetry_Strategy.md (PascalCase + underscore)
- Kubernetes Workflows_ Kustomize.md (spaces + underscore)
```

### Exceptions (Three Cases Only)

1. **Major Reference Docs**: `SCREAMING_SNAKE_CASE.md`
   - Examples: `SPEC.md`, `COMPONENT_ALMANAC.md`, `STRATEGIC_VISION.md`
   - Use case: Top-level project governance documents in `00-project/`

2. **Nested SPEC Files**: `SPEC.md` inside numbered directories
   - Format: `01-planning/specifications/NNN-name/SPEC.md`
   - Use case: Formal specification documents within feature directories

3. **Numbered Stage Files**: `NN-TITLE.md` inside feature directories
   - Format: `01-RESEARCH.md`, `02-PLAN.md`, `03-TASKS.md`
   - Use case: Sequential workflow stages in `01-planning/features/NNN-name/`

### Numbered Directories

**Format**: `NNN-kebab-case-description/`

- `NNN`: Zero-padded 3-digit number (001, 002, 003, ...)
- Use for: Planning specifications, features, ADRs (file format)
- Examples: `001-research-planner/`, `adr-042-llm-consolidation.md`

**Versioning**: Use `-vN` suffix (NOT `.0` or `_version`)
- Correct: `document-name-v2.md`
- Incorrect: `document-name-v2.0.md`, `document-name_version_2.md`

### Compliance Detection

**Kebab-Case Pattern**: `^[a-z0-9]+(-[a-z0-9]+)*\.md$` (files)

**Directory Pattern**: `^[a-z0-9]+(-[a-z0-9]+)*/$` OR `^[0-9]{3}-[a-z0-9]+(-[a-z0-9]+)*/$`

**Violation Indicators**:
- Contains uppercase letters (except SCREAMING_SNAKE_CASE exceptions)
- Contains underscores (except SCREAMING_SNAKE_CASE exceptions)
- Contains spaces
- Missing .md extension
- Multiple consecutive hyphens (`--`)

## Three-Tier Safety Model

### Tier 0: Read-Only Validation (Default)

**Capabilities**: Scan, analyze, report violations

**Safe Operations**:
- Directory structure validation
- Naming convention checks
- Cross-reference integrity analysis
- Lifecycle stage detection
- Orphan document identification
- Compliance scoring (0-100)

**Triggers**: "check", "audit", "validate", "scan", "analyze"

**Output**: Structured report with violations categorized by severity

### Tier 1: Safe Automated Fixes

**Capabilities**: Tier 0 + non-destructive automated corrections

**Safe Operations**:
- Fix broken internal links (update paths)
- Rename files to kebab-case (preserve git history via orchestrator)
- Update cross-references after moves
- Add missing frontmatter
- Fix relative path format

**Prohibited**:
- File deletion
- Directory restructuring
- Content modifications
- Moving files across lifecycle stages

**Triggers**: "fix links", "correct naming", "update references"

**Verification Required**: Read-back confirmation for all edits

### Tier 2: Supervised Restructuring

**Capabilities**: Tier 1 + structural changes with user approval

**Operations Requiring Approval**:
- Move files between lifecycle directories (01-planning → 06-archive)
- Merge duplicate documents
- Restructure directory hierarchy
- Archive completed work
- Delete orphaned files

**Triggers**: "restructure", "reorganize", "move files", "migrate", "archive"

**Approval Protocol**:
1. Present proposed changes with impact analysis
2. Wait for explicit user confirmation
3. Execute changes with rollback plan
4. Verify all cross-references updated

**Tier 3: Manual-Only (Not Automated)**

Operations that MUST be done by user or orchestrator:
- Git operations (`git mv`, `git rm`)
- Deleting directories
- Major reorganizations (>20 files)
- Changes to `00-project/SPEC.md` or `COMPONENT_ALMANAC.md`

### Tier Selection Logic

**Decision Matrix**:

| User Request Contains | Selected Tier | Rationale |
|-----------------------|---------------|-----------|
| "check", "health", "audit" | Tier 0 | Read-only keywords |
| "fix", "correct", "repair" | Tier 1 | Safe modification keywords |
| "restructure", "reorganize", "move" | Tier 2 | Supervised keywords |
| "delete", "remove", "purge" | Escalate to user | Destructive operation |

**Ambiguity Handling**:
- Multiple tier keywords → Use HIGHEST tier
- No clear tier keyword → Default to Tier 0, ask for clarification
- Explicit tier requested → Use that tier

## Reorganization Workflow

### Phase 1: Assessment (Tier 0)

**Steps**:
1. Glob target scope: `docs/**/*.md`, `.claude/docs/**/*.md`
2. Validate directory structure against standard hierarchy
3. Check naming compliance (kebab-case vs exceptions)
4. Detect misplaced documents (wrong lifecycle stage)
5. Identify orphans (no cross-references)
6. Calculate compliance score

**Output**: Assessment report with violation counts and severity levels

### Phase 2: Planning (Tier 1/2)

**Steps**:
1. Categorize violations by fix type (rename, move, link update)
2. Estimate effort (number of files affected)
3. Identify dependencies (cross-references that will break)
4. Generate fix plan with rollback strategy
5. Present to user if Tier 2 operations required

**Output**: Structured fix plan with before/after state

### Phase 3: Execution (Tier 1/2)

**Tier 1 Automated**:
- Rename files: Use orchestrator delegation (git mv required)
- Fix links: Use `mcp__desktop-commander__edit_block` on each file
- Update references: Sequential edits with read-back verification

**Tier 2 Supervised**:
- Present change → Wait for approval → Execute → Verify
- Use `git mv` via orchestrator for all file moves
- Update all cross-references in single transaction
- Log all changes with file:line details

### Phase 4: Verification

**Mandatory Checks**:
- [ ] All renamed files read back correctly
- [ ] No new broken links introduced
- [ ] Cross-references bidirectional (A→B, B→A both valid)
- [ ] Compliance score improved (before/after comparison)
- [ ] Git history preserved for all moves

**Rollback Criteria**: If ANY check fails, revert all changes in that phase

## Compliance Scoring

### Scoring Formula

**Overall Score** = (Directory × 0.3) + (Naming × 0.3) + (Lifecycle × 0.25) + (Links × 0.15)

**Component Scores** (0-100 each):

1. **Directory Structure** (30%):
   - Valid top-level directories: +10 each (max 70)
   - No invalid directories: +30
   - Calculation: `(valid_dirs / total_dirs) × 70 + (no_invalid ? 30 : 0)`

2. **Naming Compliance** (30%):
   - Files matching kebab-case: +1 each
   - Valid exceptions (SCREAMING_SNAKE_CASE): +1 each
   - Calculation: `(compliant_files / total_files) × 100`

3. **Lifecycle Placement** (25%):
   - Documents in correct stage: +1 each
   - Misplaced documents: -2 each
   - Calculation: `max(0, (correct_placement / total_docs) × 100)`

4. **Cross-Reference Health** (15%):
   - Valid internal links: +1 each
   - Broken links: -2 each
   - Calculation: `max(0, (valid_links / total_links) × 100)`

### Grade Mapping

| Score Range | Grade | Health Status | Action Required |
|-------------|-------|---------------|-----------------|
| 90-100 | A | Excellent | Routine maintenance only |
| 80-89 | B | Good | Minor fixes (Tier 1) |
| 70-79 | C | Fair | Systematic cleanup (Tier 1) |
| 60-69 | D | Poor | Restructuring needed (Tier 2) |
| 0-59 | F | Critical | Major reorganization (Tier 2 + user) |

**Actionable Threshold**: Score < 80 triggers automatic fix recommendations

## Common Violations & Fixes

### Violation: Incorrect Naming

**Detection**: File/directory contains spaces, underscores, or PascalCase (non-exception)

**Tier 1 Fix**:
```markdown
Before: Python Code Review Framework v2.md
After:  python-code-review-framework-v2.md

Before: ci_cd_spec.md
After:  ci-cd-spec.md
```

**Process**: Delegate rename to orchestrator (requires git mv)

### Violation: Misplaced Document

**Detection**: Document in wrong lifecycle stage

**Examples**:
- Completed spec still in `01-planning/` → Should be in `06-archive/projects/`
- How-to guide in `03-implementation/` → Should be in `04-guides/development/`
- ADR in wrong format → Should use `adr-NNN-name.md` in `02-architecture/decisions/`

**Tier 2 Fix**: Present proposed move, get approval, execute via orchestrator

### Violation: Broken Internal Link

**Detection**: Link target does not exist at specified path

**Tier 1 Fix**:
```markdown
Before: See [SPEC.md](SPEC.md)  # Relative to current file
After:  See [SPEC.md](00-project/SPEC.md)  # Relative to docs root

Before: See [ADR](02-architecture/decisions/adr-001.md)  # File moved
After:  See [ADR](02-architecture/decisions/adr-042-llm-consolidation.md)  # Updated
```

**Process**: Update link path using `mcp__desktop-commander__edit_block`

### Violation: Single-File Directory

**Detection**: Directory contains only one .md file (no subdirectories)

**Example**:
```
docs/orchestrator/
└── pain-point-validation.md  # Orphan in single-file directory
```

**Tier 2 Fix**: Move to appropriate category (e.g., `04-guides/templates/`)

### Violation: Duplicate Documents

**Detection**: Multiple docs with similar names or overlapping content

**Example**:
```
docs/00-project/HIGH-LEVEL-PLAN-AND-CONTEXT.md
docs/00-project/STRATEGIC_VISION.md
docs/00-project/IMPLEMENTATION-PLAN-SECURE-RESEARCH-SYSTEM.md
```

**Tier 2 Fix**: Consolidate into single authoritative document, archive others

## Scope Validation

**Allowed**: `docs/**/*.md`, `.claude/docs/**/*.md`, specific subdirectories
**Rejected**: Path traversal (`../`), absolute paths, `node_modules/`, `.git/`, `__pycache__/`

**Invalid Scope**: FAIL immediately with `invalid_scope` error, suggest corrected pattern

## Integration with DOCS-MANAGEMENT.md

**This skill enforces rules defined in**: `docs/DOCS-MANAGEMENT.md`

**Authoritative Source**: DOCS-MANAGEMENT.md is the single source of truth for:
- Directory structure hierarchy
- Lifecycle stage definitions
- Naming convention exceptions
- Placement decision trees
- Maintenance schedules

**Sync Protocol**:
- When DOCS-MANAGEMENT.md updates → Re-validate organization rules
- When conflicts arise → DOCS-MANAGEMENT.md takes precedence
- When new patterns emerge → Update DOCS-MANAGEMENT.md first, then skill

**Reference Hierarchy**:
1. DOCS-MANAGEMENT.md (canonical rules)
2. This skill (enforcement logic)
3. `documentation` agent (execution)

## Anti-Patterns

**NEVER**:
- Modify file content (structure/metadata only)
- Delete files without explicit user approval
- Perform git operations directly (delegate to orchestrator)
- Edit outside `docs/**` or `.claude/docs/**` scope
- Make parallel edits to the same file
- Skip read-back verification after edits
- Ignore DOCS-MANAGEMENT.md rules

**ALWAYS**:
- Read before Edit (mandatory verification)
- Sequential file operations with read-back confirmation
- Classify violations by severity (critical/high/medium/low)
- Provide actionable recommendations with effort estimates
- Document coverage percentage for partial scans
- Preserve git history for all moves (use `git mv` via orchestrator)
- Use kebab-case for all new files/directories (unless valid exception)

## Quick Reference

### Decision Matrix: Document Placement

| Document Type | Target Directory | Format |
|---------------|------------------|--------|
| System spec | `00-project/SPEC.md` | SCREAMING_SNAKE_CASE.md |
| Component inventory | `00-project/COMPONENT_ALMANAC.md` | SCREAMING_SNAKE_CASE.md |
| Quarterly roadmap | `00-project/roadmaps/active/` | `QN-YYYY.md` |
| Large feature spec | `01-planning/specifications/NNN-name/` | `SPEC.md` inside |
| Small feature plan | `01-planning/features/NNN-name/` | `01-RESEARCH.md`, `02-PLAN.md`, `03-TASKS.md` |
| Architecture decision | `02-architecture/decisions/` | `adr-NNN-name.md` |
| Component spec | `03-implementation/components/` | `kebab-case.md` |
| Infrastructure guide | `03-implementation/infrastructure/` | `kebab-case.md` |
| Development workflow | `04-guides/development/` | `kebab-case.md` |
| Domain knowledge | `04-guides/domain/` | `kebab-case.md` |
| Reusable template | `04-guides/templates/` | `kebab-case.md` |
| API reference | `05-reference/api/` | `kebab-case.md` |
| Data schema | `05-reference/schemas/` | `kebab-case.md` |
| Completed work | `06-archive/projects/` | Preserve original name |

### Naming Exceptions Checklist

- [ ] Is this a top-level governance doc in `00-project/`? → SCREAMING_SNAKE_CASE.md
- [ ] Is this a SPEC.md inside a numbered directory? → Keep as `SPEC.md`
- [ ] Is this a numbered stage file in features/? → `NN-TITLE.md`
- [ ] None of the above? → `kebab-case.md`

## Resources

### references/

This skill includes detailed reference documentation:

- **naming-conventions.md**: Complete kebab-case rules, exception patterns, version suffixes
- **directory-structure.md**: Standard hierarchy, lifecycle flow, valid subdirectories
- **tier-safety-rules.md**: Detailed tier capabilities, operation matrices, approval workflows

All references are loaded into context to inform validation and enforcement logic.

### scripts/ and assets/

Not applicable for this skill. Organization enforcement is analysis-based, not execution-based.
