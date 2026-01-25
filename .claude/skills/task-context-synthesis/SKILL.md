---
name: task-context-synthesis
description: >
  Use this skill when building context for task generation from PLAN.md 
  and related feature artifacts. Synthesizes SPEC.md requirements, identifies
  existing patterns, maps implementation items. Trigger keywords: task context,
  feature synthesis, plan context building, implementation item extraction.
---

# Task Context Synthesis

*Build comprehensive context for task generation by extracting implementation items, classifying complexity, and discovering codebase patterns.*

## Contents

- [Context Building Protocol](#context-building-protocol)
- [Plan Section Extraction](#plan-section-extraction)
- [Implementation Item Detection](#implementation-item-detection)
- [Complexity Classification](#complexity-classification)
- [Codebase Pattern Discovery](#codebase-pattern-discovery)
- [Output Contract](#output-contract)
- [Anti-Patterns](#anti-patterns-never-do)
- [Quick Reference](#quick-reference)

---

## Context Building Protocol

**Framework Alignment**: CAGEERF (Context -> Analysis -> Goals -> Execution -> Evaluation -> Refinement -> Framework)

### Phase 1: Context Gathering (CAGEERF-C)

```
1. LOCATE source artifacts:
   - PLAN.md (primary source)
   - SPEC.md (requirements reference)
   - docs/00-project/COMPONENT_ALMANAC.md (existing components)
   
2. VALIDATE artifact presence:
   - PLAN.md MUST exist (FAILURE if missing)
   - SPEC.md OPTIONAL (warn if missing)
   - COMPONENT_ALMANAC.md RECOMMENDED (warn if missing)

3. EXTRACT metadata:
   - Feature name from PLAN.md title
   - Status (PLANNED/IN_PROGRESS/COMPLETE)
   - Sprint points and priority
   - Last updated timestamp
```


### Phase 2: Analysis (CAGEERF-A)

```
1. PARSE PLAN.md sections (see Plan Section Extraction)
2. DETECT implementation items (see Implementation Item Detection)
3. CLASSIFY overall complexity (see Complexity Classification)
4. DISCOVER codebase patterns (see Codebase Pattern Discovery)
```

### Phase 3: Goals Definition (CAGEERF-G)

```
1. MAP implementation items to task categories:
   - Code tasks (packages/**, scripts/**)
   - Test tasks (tests/**)
   - Documentation tasks (docs/**)
   - Configuration tasks (*.yaml, *.json, *.toml)
   
2. IDENTIFY dependencies between items
3. DETERMINE parallel vs sequential execution eligibility
```

---

## Plan Section Extraction

### Required Sections (>=3 must be present for valid PLAN.md)

| Section | Canonical Header | Fuzzy Matches | Priority |
|---------|------------------|---------------|----------|
| Implementation Plan | `## Implementation Plan` | "Implementation", "Plan", "Phases" | Critical |
| Technical Debt | `## Technical Debt` | "Debt", "Cleanup", "Refactoring" | High |
| Dependencies | `## Dependencies` | "Requirements", "Prerequisites" | High |
| Architecture | `## Architecture` | "Design", "Structure", "Components" | Medium |
| Testing | `## Testing` | "Test Plan", "Quality", "Validation" | Medium |

### Extraction Algorithm

```python
def extract_plan_sections(plan_content: str) -> dict[str, str]:
    """Extract recognized sections from PLAN.md content."""
    sections = {}
    current_section = None
    current_content = []
    
    for line in plan_content.split('\n'):
        if line.startswith('## '):
            # Save previous section
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            
            # Detect new section
            header = line.strip('# ').strip()
            current_section = detect_section_type(header)
            current_content = []
        elif current_section:
            current_content.append(line)
    
    # Save final section
    if current_section:
        sections[current_section] = '\n'.join(current_content)
    
    return sections
```


### Section Validation Rules

| Rule | Threshold | Action if Failed |
|------|-----------|------------------|
| Min sections | >=3 of 5 | FAILURE: `missing_plan_sections` |
| Section has content | >0 lines after header | WARNING: log empty section |
| Nested headers | ## or ### only | IGNORE: skip deeper nesting |

---

## Implementation Item Detection

### Item Sources in PLAN.md

| Source Location | Item Type | Detection Pattern |
|-----------------|-----------|-------------------|
| `## Implementation Plan` | Phase tasks | Numbered lists, task descriptions |
| `## Technical Debt` | Cleanup items | Checkboxes, file references |
| `## Architecture` | Component items | Code blocks, file paths |
| `## Dependencies` | Prerequisite items | Bullet lists, package names |

### Detection Algorithm

```
FOR each section in extracted_sections:
  
  1. SCAN for file path patterns:
     - Absolute: `/path/to/file.py`
     - Relative: `packages/core/module.py`
     - Glob: `tests/**/*.py`
  
  2. SCAN for action verbs:
     - Create: "create", "add", "new", "implement"
     - Modify: "update", "change", "refactor", "fix"
     - Delete: "remove", "delete", "deprecate"
  
  3. SCAN for component references:
     - Class names: PascalCase patterns
     - Function names: snake_case patterns
     - Module names: dotted paths (e.g., `packages.core.auth`)
  
  4. BUILD implementation_item:
     {
       "source_section": section_name,
       "action": detected_verb,
       "target_path": file_path or null,
       "component": component_name or null,
       "description": extracted_text,
       "line_number": source_line
     }
  
  5. APPEND to implementation_items[]
```

### Item Categorization

| Category | File Pattern | Agent Assignment |
|----------|--------------|------------------|
| Code | `packages/**/*.py`, `scripts/**/*.py` | development |
| Test | `tests/**/*.py` | code-quality |
| Documentation | `docs/**/*.md`, `.claude/**/*.md` | documentation |
| Configuration | `*.yaml`, `*.json`, `*.toml` | development |
| Agent/Workflow | `.claude/agents/**`, `.claude/commands/**` | workflow |



---

## Complexity Classification

**Reference**: See [generating-tasks skill](../generating-tasks/SKILL.md) for task-level complexity and TDD pairing rules.

### Feature-Level Complexity Thresholds

| Complexity | Implementation Items | File Count | Dependencies | Sprint Points |
|------------|---------------------|------------|--------------|---------------|
| SIMPLE | 1-5 items | 1-3 files | 0-2 deps | 1-8 points |
| MODERATE | 6-15 items | 4-10 files | 3-5 deps | 13-21 points |
| COMPLEX | 16+ items | 11+ files | 6+ deps | 34+ points |

### Classification Algorithm

```python
def classify_complexity(
    implementation_items: list[dict],
    file_patterns: dict,
    dependencies: list[str]
) -> str:
    """Classify feature complexity based on extracted context."""
    
    item_count = len(implementation_items)
    file_count = len(file_patterns.get("source_dirs", [])) + \
                 len(file_patterns.get("test_dirs", []))
    dep_count = len(dependencies)
    
    # Score each dimension
    item_score = 1 if item_count <= 5 else (2 if item_count <= 15 else 3)
    file_score = 1 if file_count <= 3 else (2 if file_count <= 10 else 3)
    dep_score = 1 if dep_count <= 2 else (2 if dep_count <= 5 else 3)
    
    # Weighted average (items most important)
    weighted_score = (item_score * 0.5) + (file_score * 0.3) + (dep_score * 0.2)
    
    if weighted_score <= 1.3:
        return "SIMPLE"
    elif weighted_score <= 2.3:
        return "MODERATE"
    else:
        return "COMPLEX"
```

### Complexity Implications

| Complexity | Review Frequency | Parallel Limit | TDD Enforcement |
|------------|------------------|----------------|-----------------|
| SIMPLE | Every 10 tasks | 5 parallel | Standard |
| MODERATE | Every 5 tasks | 3 parallel | Strict |
| COMPLEX | Every 3 tasks | 2 parallel | Mandatory review |



---

## Codebase Pattern Discovery

### Discovery Protocol

```
1. CHECK COMPONENT_ALMANAC.md first:
   - Grep for component names from implementation items
   - If found: Note existing location, DO NOT recreate
   - If not found: Mark as NEW component

2. SCAN existing file patterns:
   - Source directories: packages/**/
   - Test directories: tests/unit/, tests/integration/
   - Documentation: docs/**/

3. DETECT naming conventions:
   - Module naming: snake_case.py
   - Class naming: PascalCase
   - Test naming: test_*.py, *_test.py

4. IDENTIFY import patterns:
   - Absolute imports: from packages.core import X
   - Relative imports: from .module import X
   - Third-party imports: Group separately
```

### Pattern Output Structure

```json
{
  "file_patterns": {
    "source_dirs": ["packages/core/", "packages/agents/"],
    "test_dirs": ["tests/unit/", "tests/integration/"],
    "doc_dirs": ["docs/00-project/", ".claude/docs/"]
  },
  "naming_conventions": {
    "modules": "snake_case",
    "classes": "PascalCase",
    "tests": "test_*.py"
  },
  "import_style": "absolute",
  "existing_modules": [
    {
      "name": "AuthService",
      "location": "packages/core/auth/service.py",
      "almanac_entry": true
    }
  ]
}
```

### COMPONENT_ALMANAC.md Integration

**CRITICAL**: Always check COMPONENT_ALMANAC.md before flagging new components.

```
FOR each detected_component in implementation_items:
  1. SEARCH COMPONENT_ALMANAC.md for component name
  2. IF found:
     - existing_modules.append({
         name: component,
         location: almanac_path,
         almanac_entry: true
       })
     - FLAG: "REUSE existing component"
  3. IF not found:
     - existing_modules.append({
         name: component,
         location: null,
         almanac_entry: false
       })
     - FLAG: "NEW component - add to COMPONENT_ALMANAC.md after creation"
```



---

## Output Contract

### Success Response

```json
{
  "status": "SUCCESS",
  "implementation_items": [
    {
      "source_section": "Implementation Plan",
      "action": "create",
      "target_path": "packages/core/auth/validator.py",
      "component": "AuthValidator",
      "description": "Create token validation service",
      "line_number": 45
    }
  ],
  "complexity": "SIMPLE|MODERATE|COMPLEX",
  "file_patterns": {
    "source_dirs": ["packages/core/", "packages/agents/"],
    "test_dirs": ["tests/unit/", "tests/integration/"],
    "doc_dirs": ["docs/00-project/", ".claude/docs/"]
  },
  "existing_modules": [
    {
      "name": "BaseService",
      "location": "packages/core/base.py",
      "almanac_entry": true
    }
  ],
  "review_frequency": 5,
  "metadata": {
    "feature_name": "Auth Token Validation",
    "plan_source": "docs/01-planning/specifications/auth-validation/PLAN.md",
    "sections_found": ["Implementation Plan", "Architecture", "Testing"],
    "synthesis_timestamp": "2025-01-15T10:30:00Z"
  }
}
```

### Failure Response

```json
{
  "status": "FAILURE",
  "error_code": "MISSING_PLAN_SECTIONS",
  "error_message": "PLAN.md missing required sections: Implementation Plan, Dependencies",
  "sections_found": ["Architecture"],
  "sections_required": 3,
  "recovery_action": "Add Implementation Plan and Dependencies sections to PLAN.md"
}
```

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | string | Yes | SUCCESS or FAILURE |
| `implementation_items` | array | On success | Extracted items from PLAN.md |
| `complexity` | string | On success | SIMPLE, MODERATE, or COMPLEX |
| `file_patterns` | object | On success | Discovered codebase patterns |
| `existing_modules` | array | On success | Components found in COMPONENT_ALMANAC |
| `review_frequency` | number | On success | Tasks between review checkpoints |
| `error_code` | string | On failure | Machine-readable error identifier |
| `recovery_action` | string | On failure | Suggested fix for the error |



---

## Anti-Patterns (NEVER DO)

### Context Building Anti-Patterns

- **Skip COMPONENT_ALMANAC check** - Always verify existing components before flagging new ones
- **Ignore PLAN.md section validation** - Missing sections indicate incomplete planning
- **Hardcode file patterns** - Discover patterns from actual codebase structure
- **Assume complexity** - Calculate complexity from extracted metrics

### Output Anti-Patterns

- **Return partial results on FAILURE** - Either SUCCESS with full context or FAILURE with recovery action
- **Omit existing_modules** - Even if empty, include the field
- **Set review_frequency without complexity** - Review frequency depends on complexity classification

### Integration Anti-Patterns

- **Generate tasks directly** - This skill builds context only; delegate to `generating-tasks` skill
- **Modify files** - Context synthesis is read-only; no file modifications
- **Execute code** - Analysis only; no code execution or test runs

---

## Thinking Frameworks

**Full Catalog**: [Thinking Frameworks README](../../docs/00-core/frameworks/README.md)

**Most Relevant for Context Synthesis**:

| Framework | When to Use |
|-----------|-------------|
| [CAGEERF](../../docs/00-core/frameworks/planning.md) | Full context building workflow |
| [Systems Thinking](../../docs/00-core/frameworks/analysis.md) | Dependency and pattern analysis |
| [Pre-Mortem](../../docs/00-core/frameworks/strategy.md) | Validate context completeness before output |

> **Selection Tip**: context building -> CAGEERF, dependencies -> Systems, validation -> Pre-Mortem



---

## Quick Reference

```
CONTEXT BUILDING FLOW:
  1. Locate: PLAN.md (required), SPEC.md (optional), COMPONENT_ALMANAC.md (recommended)
  2. Extract: Parse sections, detect items, identify file paths
  3. Classify: Calculate complexity from items, files, dependencies
  4. Discover: Scan codebase for patterns, check almanac for existing modules
  5. Output: Return synthesis result with all context for task generation

COMPLEXITY THRESHOLDS:
  SIMPLE:   1-5 items,   1-3 files,  0-2 deps  -> review every 10 tasks
  MODERATE: 6-15 items,  4-10 files, 3-5 deps  -> review every 5 tasks
  COMPLEX:  16+ items,   11+ files,  6+ deps   -> review every 3 tasks

REQUIRED PLAN.md SECTIONS (>=3 of 5):
  - Implementation Plan (Critical)
  - Technical Debt (High)
  - Dependencies (High)
  - Architecture (Medium)
  - Testing (Medium)

OUTPUT CONTRACT:
  SUCCESS: implementation_items[] + complexity + file_patterns + existing_modules + review_frequency
  FAILURE: error_code + error_message + recovery_action

ALWAYS CHECK:
  - COMPONENT_ALMANAC.md before flagging new components
  - Section count >= 3 for valid PLAN.md
  - File paths match detected patterns

NEXT STEP:
  Pass context to generating-tasks skill for task list creation
```

---

## Cross-References

### Related Skills

| Skill | Relationship |
|-------|--------------|
| [generating-tasks](../generating-tasks/SKILL.md) | Receives context output, generates task list |
| [codebase-research](../codebase-research/SKILL.md) | Pattern discovery methodology |
| [feature-design-workflow](../feature-design-workflow/SKILL.md) | Upstream workflow (PLAN.md creation) |

### Shared Documentation

| Document | Purpose |
|----------|---------|
| [COMPONENT_ALMANAC.md](../../../docs/00-project/COMPONENT_ALMANAC.md) | Existing component registry |
| [Thinking Frameworks](../../docs/00-core/frameworks/README.md) | CAGEERF and analysis frameworks |
| [Agent Selection Guide](../../docs/01-guides/agents/agent-selection-guide.md) | Agent assignment reference |

