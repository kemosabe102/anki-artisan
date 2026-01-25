---
name: task-intake
description: >
  Use this skill when parsing /tasks command arguments and discovering 
  feature directories. Validates PLAN.md existence, extracts --phase flag,
  determines output location. Trigger keywords: parse tasks args, plan file 
  validation, task directory discovery, phase extraction.
---

# Task Intake

*Parse /tasks command arguments and discover feature directories for task generation*

## Contents

- [Argument Parsing Protocol](#argument-parsing-protocol)
- [Directory Discovery Algorithm](#directory-discovery-algorithm)
- [Input Validation Gates](#input-validation-gates)
- [Plan Metadata Extraction](#plan-metadata-extraction)
- [Output Contract](#output-contract)
- [Anti-Patterns](#anti-patterns-never-do)
- [Quick Reference](#quick-reference)

---

## Argument Parsing Protocol

Parse `/tasks path/to/PLAN.md --phase=N` arguments into structured intake data.

### Argument Structure

```
/tasks <positional-path> [--phase=N]

Components:
  <positional-path>  : Required. Path to PLAN.md file (absolute or relative)
  --phase=N          : Optional. Phase number to filter (integer >= 1)
```

### Parsing Algorithm

```python
def parse_tasks_arguments(raw_args: str) -> dict:
    """
    Parse /tasks command arguments.
    
    Args:
        raw_args: Raw argument string from command invocation
        
    Returns:
        {
            "plan_path": str,      # Normalized absolute path
            "phase": int | None,   # Phase number if provided
            "raw_input": str       # Original input for debugging
        }
    """
    tokens = raw_args.strip().split()
    
    result = {
        "plan_path": None,
        "phase": None,
        "raw_input": raw_args
    }
    
    for token in tokens:
        # Phase flag detection
        if token.startswith("--phase="):
            phase_value = token.split("=", 1)[1]
            if phase_value.isdigit() and int(phase_value) >= 1:
                result["phase"] = int(phase_value)
            else:
                raise ValueError(f"Invalid phase value: {phase_value}")
        
        # Positional path (first non-flag token)
        elif not token.startswith("--") and result["plan_path"] is None:
            result["plan_path"] = normalize_path(token)
    
    if result["plan_path"] is None:
        raise ValueError("Missing required: path to PLAN.md")
    
    return result
```

### Path Normalization Rules

| Input Pattern | Normalized Output |
|---------------|-------------------|
| `PLAN.md` | `{cwd}/PLAN.md` |
| `./docs/PLAN.md` | `{cwd}/docs/PLAN.md` |
| `docs/feature/PLAN.md` | `{cwd}/docs/feature/PLAN.md` |
| `/absolute/path/PLAN.md` | `/absolute/path/PLAN.md` |
| `C:\Windows\path\PLAN.md` | `C:/Windows/path/PLAN.md` |

**Key Rules**:
- Always convert to forward slashes
- Always resolve to absolute path
- Preserve case on case-sensitive filesystems

---

## Directory Discovery Algorithm

Determine feature directory and output location from the validated plan path.

### Discovery Process

```
INPUT: plan_path (absolute path to PLAN.md)

STEP 1: Extract Feature Directory
  feature_dir = parent_directory(plan_path)
  
  IF plan_path ends with /plans/*.md:
    # Plan is in a plans/ subdirectory
    feature_dir = parent_directory(parent_directory(plan_path))

STEP 2: Determine Output Directory
  output_dir = feature_dir + "/tasks"
  
  IF directory_exists(feature_dir + "/tasks"):
    output_dir = feature_dir + "/tasks"
  ELIF file_exists(feature_dir + "/TASKS.md"):
    output_dir = feature_dir  # Tasks live alongside PLAN.md
  ELSE:
    output_dir = feature_dir + "/tasks"  # Default: create tasks/ subdirectory

STEP 3: Validate Structure
  ASSERT: directory_exists(feature_dir)
  ASSERT: file_exists(plan_path)
  
OUTPUT: {
  "feature_dir": feature_dir,
  "output_dir": output_dir,
  "plan_location": "root" | "plans_subdir"
}
```

### Directory Structure Patterns

**Pattern A: Plan at Feature Root**
```
feature/
  PLAN.md          <- plan_path
  SPEC.md
  tasks/           <- output_dir
    TASKS.md
```

**Pattern B: Plan in Subdirectory**
```
feature/
  SPEC.md
  plans/
    phase-1-PLAN.md   <- plan_path
    phase-2-PLAN.md
  tasks/              <- output_dir
    phase-1-TASKS.md
```

**Pattern C: Phase-Specific Plans**
```
feature/
  PLAN-phase-1.md     <- plan_path (with --phase=1)
  PLAN-phase-2.md
  TASKS-phase-1.md    <- output (same directory)
```

---

## Input Validation Gates

All gates are BLOCKING. Failure prevents task generation.

### Gate 1: Path Existence

```
VALIDATE file_exists(plan_path):
  IF NOT exists:
    ERROR: "PLAN_NOT_FOUND"
    MESSAGE: "Plan file not found at: {plan_path}"
    HINT: "Check file path. Use: ls {parent_dir} to see available files"
    SUGGEST: "Create plan first: /plan {spec_path}"
```

### Gate 2: File Extension

```
VALIDATE plan_path ends with .md:
  IF NOT .md extension:
    ERROR: "INVALID_FILE_TYPE"
    MESSAGE: "Expected .md file, got: {extension}"
    HINT: "Plan files must be Markdown (.md)"
```

### Gate 3: Required Sections

**Reference**: See [generating-tasks skill](../generating-tasks/SKILL.md#planmd-section-detection) for full Section Detection Algorithm.

```
VALIDATE plan has >= 3 of 5 required sections:
  Required sections:
    - Implementation Plan (or: Implementation, Plan, Phases)
    - Technical Debt (or: Debt, Cleanup, Refactoring)
    - Dependencies (or: Requirements, Prerequisites)
    - Architecture (or: Design, Structure, Components)
    - Testing (or: Test Plan, Quality, Validation)
    
  IF section_count < 3:
    ERROR: "INSUFFICIENT_PLAN_STRUCTURE"
    MESSAGE: "Plan missing required sections. Found: {found_sections}"
    HINT: "Plan needs at least 3 of: Implementation, Dependencies, Architecture, Testing, Technical Debt"
    SUGGEST: "Regenerate plan: /plan {spec_path}"
```

### Gate 4: Phase Validity (if --phase provided)

```
IF phase is not None:
  VALIDATE phase exists in plan:
    phases_found = extract_phases(plan_content)
    
    IF phase > len(phases_found) OR phase < 1:
      ERROR: "INVALID_PHASE"
      MESSAGE: "Phase {phase} not found. Plan has phases: 1-{max_phase}"
      HINT: "Available phases: {list(phases_found)}"
```

### Gate 5: Feature Directory Writable

```
VALIDATE can_write(output_dir):
  IF NOT writable:
    ERROR: "OUTPUT_NOT_WRITABLE"
    MESSAGE: "Cannot write to output directory: {output_dir}"
    HINT: "Check permissions or specify different output location"
```

---

## Plan Metadata Extraction

Extract structured metadata from validated PLAN.md for downstream processing.

### Extraction Algorithm

```python
def extract_plan_metadata(plan_path: str, plan_content: str) -> dict:
    """
    Extract metadata from PLAN.md content.
    
    Returns:
        {
            "feature_name": str,
            "phases": list[dict],
            "total_phases": int,
            "has_acceptance_criteria": bool,
            "has_solution_design": bool,
            "estimated_complexity": "low" | "medium" | "high"
        }
    """
    metadata = {
        "feature_name": extract_feature_name(plan_path, plan_content),
        "phases": [],
        "total_phases": 0,
        "has_acceptance_criteria": False,
        "has_solution_design": False,
        "estimated_complexity": "medium"
    }
    
    # Extract phases
    phase_pattern = r"##\s*Phase\s*(\d+)[:\s]*(.+?)(?=##\s*Phase|\Z)"
    for match in re.finditer(phase_pattern, plan_content, re.DOTALL):
        phase_num = int(match.group(1))
        phase_content = match.group(2)
        
        metadata["phases"].append({
            "number": phase_num,
            "has_criteria": "acceptance" in phase_content.lower(),
            "has_tasks": bool(re.search(r"[-*]\s+\[", phase_content))
        })
    
    metadata["total_phases"] = len(metadata["phases"])
    
    # Check for key sections
    metadata["has_acceptance_criteria"] = "acceptance criteria" in plan_content.lower()
    metadata["has_solution_design"] = "solution design" in plan_content.lower()
    
    # Estimate complexity
    if metadata["total_phases"] > 5:
        metadata["estimated_complexity"] = "high"
    elif metadata["total_phases"] <= 2:
        metadata["estimated_complexity"] = "low"
    
    return metadata
```

### Feature Name Extraction

```
Priority order for feature name:
  1. YAML frontmatter: feature_name or name field
  2. First H1 heading: "# Feature Name"
  3. Directory name: basename(feature_dir)
  4. Plan filename: PLAN-{feature-name}.md -> feature-name
```

---

## Output Contract

Successful intake produces this structured output for downstream task generation.

### Success Output Schema

```json
{
  "status": "SUCCESS",
  "plan_path": "/absolute/path/to/PLAN.md",
  "phase": null,
  "feature_dir": "/absolute/path/to/feature",
  "output_dir": "/absolute/path/to/feature/tasks",
  "plan_metadata": {
    "feature_name": "my-feature",
    "phases": [
      {"number": 1, "has_criteria": true, "has_tasks": true},
      {"number": 2, "has_criteria": true, "has_tasks": false}
    ],
    "total_phases": 2,
    "has_acceptance_criteria": true,
    "has_solution_design": true,
    "estimated_complexity": "medium"
  }
}
```

### Failure Output Schema

```json
{
  "status": "FAILURE",
  "error_code": "PLAN_NOT_FOUND | INVALID_PHASE | INSUFFICIENT_PLAN_STRUCTURE | ...",
  "message": "Human-readable error description",
  "hint": "Actionable suggestion for resolution",
  "suggest": "Recommended command to fix the issue",
  "context": {
    "plan_path": "/attempted/path",
    "phase": 3,
    "raw_input": "original user input"
  }
}
```

### Phase-Filtered Output

When `--phase=N` is provided:

```json
{
  "status": "SUCCESS",
  "plan_path": "/absolute/path/to/PLAN.md",
  "phase": 2,
  "feature_dir": "/absolute/path/to/feature",
  "output_dir": "/absolute/path/to/feature/tasks",
  "plan_metadata": {
    "feature_name": "my-feature",
    "phases": [
      {"number": 2, "has_criteria": true, "has_tasks": true}
    ],
    "total_phases": 5,
    "filtered_to_phase": 2,
    "has_acceptance_criteria": true,
    "has_solution_design": true,
    "estimated_complexity": "medium"
  }
}
```

---

## Anti-Patterns (NEVER DO)

| Anti-Pattern | Why It Fails | Correct Approach |
|--------------|--------------|------------------|
| Skip path validation | File not found errors downstream | Always validate existence first |
| Assume relative paths | CWD varies between tool calls | Always normalize to absolute |
| Hardcode output location | Breaks different project structures | Discover from plan location |
| Ignore --phase flag | Generates all tasks when user wants subset | Parse and filter appropriately |
| Return partial metadata | Downstream agents fail | Validate all gates before success |
| Use backslashes in paths | Cross-platform incompatibility | Always use forward slashes |
| Execute task generation | Intake only parses, does not generate | Delegate generation to generating-tasks |
| Modify plan file | Intake is read-only | Never write to input files |

---

## Quick Reference

```
ARGUMENT FORMAT:
  /tasks <path> [--phase=N]

PARSING:
  path     : Required, first non-flag token, normalize to absolute
  --phase  : Optional, integer >= 1, filters to single phase

DIRECTORY DISCOVERY:
  feature_dir = parent(plan_path) or parent(parent(plan_path)) if in plans/
  output_dir  = feature_dir/tasks (default) or alongside plan (if pattern exists)

VALIDATION GATES (all blocking):
  1. Path exists
  2. File is .md
  3. Has >= 3 required sections (see generating-tasks skill)
  4. Phase exists (if --phase provided)
  5. Output writable

OUTPUT CONTRACT:
  SUCCESS: { status, plan_path, phase, feature_dir, output_dir, plan_metadata }
  FAILURE: { status, error_code, message, hint, suggest, context }

SECTION DETECTION:
  Reference: generating-tasks skill -> PLAN.md Section Detection
  
PATH NORMALIZATION:
  - Forward slashes only
  - Absolute paths only
  - Preserve filesystem case
```

---

## Cross-References

### Related Skills

| Skill | Relationship |
|-------|--------------|
| [generating-tasks](../generating-tasks/SKILL.md) | Consumes intake output, provides Section Detection Algorithm |
| [codebase-research](../codebase-research/SKILL.md) | Directory discovery patterns |
| [validating-specifications](../validating-specifications/SKILL.md) | Validation gate patterns |

### Command Documentation

| Document | Purpose |
|----------|---------|
| [/tasks command](../../commands/tasks.md) | Parent command specification |
| [Workflow Phases](../../docs/command-docs/tasks/docs/workflow-phases.md) | Full 7-step workflow |

---

## Thinking Frameworks

**Full Catalog**: [Thinking Frameworks README](../../docs/00-core/frameworks/README.md)

**Most Relevant for Task Intake**:

| Framework | When to Use |
|-----------|-------------|
| [ReACT](../../docs/00-core/frameworks/analysis.md) | Path resolution, iterative validation |
| [Pre-Mortem](../../docs/00-core/frameworks/strategy.md) | Anticipating parsing edge cases |

> **Selection Tip**: path issues -> ReACT, edge cases -> Pre-Mortem
