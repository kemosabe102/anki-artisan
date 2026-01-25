---
name: plan-intake
description: >
  Use this skill when parsing /plan command arguments and validating 
  SPEC.md files. Validates existence, extracts metadata.
  Trigger keywords: parse plan args, spec validation, directory discovery.
---

# Plan Intake

*Parse /plan command arguments and discover feature directories for plan generation*

## Contents

- [Argument Parsing Protocol](#argument-parsing-protocol)
- [Directory Discovery Algorithm](#directory-discovery-algorithm)
- [Input Validation Gates](#input-validation-gates)
- [SPEC Metadata Extraction](#spec-metadata-extraction)
- [Output Contract](#output-contract)
- [Anti-Patterns](#anti-patterns-never-do)
- [Quick Reference](#quick-reference)

---

## Argument Parsing Protocol

Parse `/plan path/to/SPEC.md --phase=N` arguments into structured intake data.

### Argument Structure

```
/plan <positional-path> [--phase=N]

Components:
  <positional-path>  : Required. Path to SPEC.md file (absolute or relative)
  --phase=N          : Optional. Phase number to filter (integer >= 1)
```

### Parsing Algorithm

```python
def parse_plan_arguments(raw_args: str) -> dict:
    """
    Parse /plan command arguments.
    
    Args:
        raw_args: Raw argument string from command invocation
        
    Returns:
        {
            "spec_path": str,      # Normalized absolute path
            "phase": int | None,   # Phase number if provided
            "raw_input": str       # Original input for debugging
        }
    """
    tokens = raw_args.strip().split()
    
    result = {
        "spec_path": None,
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
        elif not token.startswith("--") and result["spec_path"] is None:
            result["spec_path"] = normalize_path(token)
    
    if result["spec_path"] is None:
        raise ValueError("Missing required: path to SPEC.md")
    
    return result
```

### Path Normalization Rules

| Input Pattern | Normalized Output |
|---------------|-------------------|
| `SPEC.md` | `{cwd}/SPEC.md` |
| `./docs/SPEC.md` | `{cwd}/docs/SPEC.md` |
| `docs/feature/SPEC.md` | `{cwd}/docs/feature/SPEC.md` |
| `/absolute/path/SPEC.md` | `/absolute/path/SPEC.md` |
| `C:\Windows\path\SPEC.md` | `C:/Windows/path/SPEC.md` |

**Key Rules**:
- Always convert to forward slashes
- Always resolve to absolute path
- Preserve case on case-sensitive filesystems

---

## Directory Discovery Algorithm

Determine feature directory and output location from the validated spec path.

### Discovery Process

```
INPUT: spec_path (absolute path to SPEC.md)

STEP 1: Extract Feature Directory
  feature_dir = parent_directory(spec_path)
  
  IF spec_path ends with /specs/*.md:
    # Spec is in a specs/ subdirectory
    feature_dir = parent_directory(parent_directory(spec_path))

STEP 2: Determine Output Directory
  output_dir = feature_dir
  
  IF directory_exists(feature_dir + "/plans"):
    output_dir = feature_dir + "/plans"
  ELIF file_exists(feature_dir + "/PLAN.md"):
    output_dir = feature_dir  # Plans live alongside SPEC.md
  ELSE:
    output_dir = feature_dir  # Default: same directory as SPEC.md

STEP 3: Validate Structure
  ASSERT: directory_exists(feature_dir)
  ASSERT: file_exists(spec_path)
  
OUTPUT: {
  "feature_dir": feature_dir,
  "output_dir": output_dir,
  "spec_location": "root" | "specs_subdir"
}
```

### Directory Structure Patterns

**Pattern A: Spec at Feature Root**
```
feature/
  SPEC.md          <- spec_path
  PLAN.md          <- output_dir (same directory)
  PLAN.json
```

**Pattern B: Spec in Subdirectory**
```
feature/
  specs/
    SPEC.md        <- spec_path
  plans/
    PLAN.md        <- output_dir
    PLAN.json
```

**Pattern C: Phase-Specific Specs**
```
feature/
  SPEC-phase-1.md  <- spec_path (with --phase=1)
  SPEC-phase-2.md
  PLAN-phase-1.md  <- output (same directory)
```

---

## Input Validation Gates

All gates are BLOCKING. Failure prevents plan generation.

### Gate 1: Path Existence

```
VALIDATE file_exists(spec_path):
  IF NOT exists:
    ERROR: "SPEC_NOT_FOUND"
    MESSAGE: "Spec file not found at: {spec_path}"
    HINT: "Check file path. Use: ls {parent_dir} to see available files"
    SUGGEST: "/spec {feature_path} for creating SPEC.md"
```

### Gate 2: File Extension

```
VALIDATE spec_path ends with .md:
  IF NOT .md extension:
    ERROR: "INVALID_FILE_TYPE"
    MESSAGE: "Expected .md file, got: {extension}"
    HINT: "Spec files must be Markdown (.md)"
```

### Gate 3: Required Sections

**Reference**: SPEC.md must contain at least 3 of 5 core sections for valid plan generation.

```
VALIDATE spec has >= 3 of 5 required sections:
  Required sections:
    - Functional Requirements (or: FR-, Requirements)
    - Context (or: Background, Overview, Problem Statement)
    - User Scenarios (or: Use Cases, Stories, User Stories)
    - Technical Constraints (or: TC-, Constraints, Platform)
    - Non-Functional Requirements (or: NFR-, Performance, Quality)
    
  IF section_count < 3:
    ERROR: "INSUFFICIENT_SPEC_STRUCTURE"
    MESSAGE: "Spec missing required sections. Found: {found_sections}"
    HINT: "Spec needs at least 3 of: Functional Requirements, Context, User Scenarios, Technical Constraints, Non-Functional Requirements"
    SUGGEST: "/spec {feature_path} to regenerate SPEC.md"
```

### FR Table Detection (Gate 3 Sub-validation)

```
FUNCTION detect_fr_table(spec_content):
  fr_entries = []
  in_table = False
  has_fr_ids = False
  has_moscow = False
  
  FOR line IN spec_content:
    IF '|' IN line AND ('FR-' IN line OR 'MUST' IN line.upper()):
      in_table = True
      IF 'FR-' IN line:
        has_fr_ids = True
        fr = parse_fr_row(line)
        IF fr:
          fr_entries.append(fr)
      IF any(kw IN line.upper() FOR kw IN ['MUST', 'SHOULD', 'COULD', "WON'T"]):
        has_moscow = True
    ELSE IF in_table AND not line.strip().startswith('|'):
      in_table = False
  
  RETURN {
    "fr_count": len(fr_entries),
    "has_fr_ids": has_fr_ids,
    "has_moscow": has_moscow,
    "entries": fr_entries
  }
```

### Gate 4: Phase Validity (if --phase provided)

```
IF phase is not None:
  VALIDATE phase is reasonable:
    # SPEC.md doesn't have explicit phases like PLAN.md
    # Phase flag indicates which phase of implementation to generate
    
    IF phase < 1:
      ERROR: "INVALID_PHASE"
      MESSAGE: "Phase must be >= 1, got: {phase}"
      HINT: "Phase numbers start at 1"
    
    IF phase > 4:
      ERROR: "INVALID_PHASE"
      MESSAGE: "Phase {phase} exceeds maximum (4). Most projects have 1-4 phases"
      HINT: "Valid phase range: 1-4"
```

### Gate 5: Output Directory Writable

```
VALIDATE can_write(output_dir):
  IF NOT writable:
    ERROR: "OUTPUT_NOT_WRITABLE"
    MESSAGE: "Cannot write to output directory: {output_dir}"
    HINT: "Check permissions or specify different output location"
```

---

## SPEC Metadata Extraction

Extract structured metadata from validated SPEC.md for downstream plan generation.

### Extraction Algorithm

```python
def extract_spec_metadata(spec_path: str, spec_content: str) -> dict:
    """
    Extract metadata from SPEC.md content.
    
    Returns:
        {
            "feature_name": str,
            "has_fr_ids": bool,
            "has_moscow": bool,
            "has_ice_score": bool,
            "fr_count": int,
            "sections_found": list[str],
            "estimated_complexity": "simple" | "complicated" | "complex" | "chaotic"
        }
    """
    metadata = {
        "feature_name": extract_feature_name(spec_path, spec_content),
        "has_fr_ids": False,
        "has_moscow": False,
        "has_ice_score": False,
        "fr_count": 0,
        "sections_found": [],
        "estimated_complexity": "complicated"
    }
    
    # Detect sections
    metadata["sections_found"] = detect_sections(spec_content)
    
    # Detect FR table structure
    fr_analysis = detect_fr_table(spec_content)
    metadata["has_fr_ids"] = fr_analysis["has_fr_ids"]
    metadata["has_moscow"] = fr_analysis["has_moscow"]
    metadata["fr_count"] = fr_analysis["fr_count"]
    
    # Check for ICE Score
    metadata["has_ice_score"] = "ice" in spec_content.lower() and \
                                 any(x in spec_content.lower() for x in ["impact", "confidence", "ease"])
    
    # Estimate complexity based on FR count (Cynefin domains)
    if metadata["fr_count"] <= 5:
        metadata["estimated_complexity"] = "simple"
    elif metadata["fr_count"] <= 15:
        metadata["estimated_complexity"] = "complicated"
    elif metadata["fr_count"] <= 30:
        metadata["estimated_complexity"] = "complex"
    else:
        metadata["estimated_complexity"] = "chaotic"
    
    return metadata
```

### Section Detection Algorithm

```python
def detect_sections(spec_content: str) -> list[str]:
    """
    Detect which required sections are present in SPEC.md.
    
    Returns list of canonical section names found.
    """
    sections_found = []
    content_lower = spec_content.lower()
    
    # Section patterns with fuzzy matching
    section_patterns = {
        "Functional Requirements": ["functional requirements", "fr-", "## requirements"],
        "Context": ["context", "background", "overview", "problem statement", "the why"],
        "User Scenarios": ["user scenario", "use case", "user story", "stories"],
        "Technical Constraints": ["technical constraint", "tc-", "constraint", "platform"],
        "Non-Functional Requirements": ["non-functional", "nfr-", "performance", "quality attributes"]
    }
    
    for canonical, patterns in section_patterns.items():
        for pattern in patterns:
            if pattern in content_lower:
                if canonical not in sections_found:
                    sections_found.append(canonical)
                break
    
    return sections_found
```

### Feature Name Extraction

```
Priority order for feature name:
  1. YAML frontmatter: feature_name or name field
  2. First H1 heading: "# Feature Name"
  3. Directory name: basename(feature_dir)
  4. Spec filename: SPEC-{feature-name}.md -> feature-name
```

```python
def extract_feature_name(spec_path: str, spec_content: str) -> str:
    """Extract feature name from spec path or content."""
    
    # Priority 1: YAML frontmatter
    if spec_content.startswith("---"):
        yaml_end = spec_content.find("---", 3)
        if yaml_end > 0:
            frontmatter = spec_content[3:yaml_end]
            for line in frontmatter.split("\n"):
                if line.startswith("feature_name:") or line.startswith("name:"):
                    return line.split(":", 1)[1].strip().strip('"\'')
    
    # Priority 2: First H1 heading
    for line in spec_content.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    
    # Priority 3: Directory name
    parent_dir = os.path.dirname(spec_path)
    dir_name = os.path.basename(parent_dir)
    if dir_name and dir_name not in ["specs", "specifications"]:
        return dir_name
    
    # Priority 4: Filename pattern
    filename = os.path.basename(spec_path)
    if filename.startswith("SPEC-"):
        return filename[5:-3]  # Remove "SPEC-" and ".md"
    
    return "unknown-feature"
```

---

## Output Contract

Successful intake produces this structured output for downstream plan generation.

### Success Output Schema

```json
{
  "status": "SUCCESS",
  "spec_path": "/absolute/path/to/SPEC.md",
  "phase_filter": 1,
  "feature_dir": "/absolute/path/to/feature",
  "output_dir": "/absolute/path/to/feature",
  "spec_metadata": {
    "feature_name": "my-feature",
    "has_fr_ids": true,
    "has_moscow": true,
    "has_ice_score": true,
    "fr_count": 8,
    "sections_found": ["Context", "Functional Requirements", "Non-Functional Requirements", "User Scenarios"],
    "estimated_complexity": "complicated"
  }
}
```

### Failure Output Schema

```json
{
  "status": "FAILURE",
  "error_code": "SPEC_NOT_FOUND | MISSING_FR_IDS | INVALID_PHASE | INSUFFICIENT_SPEC_STRUCTURE | INVALID_FILE_TYPE | OUTPUT_NOT_WRITABLE",
  "message": "Human-readable error description",
  "hint": "Actionable suggestion for resolution",
  "suggest": "/spec path/to/feature for creating SPEC.md",
  "context": {
    "spec_path": "/attempted/path",
    "phase": 3,
    "raw_input": "original user input"
  }
}
```

### Error Code Reference

| Error Code | Trigger | Resolution |
|------------|---------|------------|
| `SPEC_NOT_FOUND` | File does not exist at path | Verify path, create spec with /spec |
| `INVALID_FILE_TYPE` | File is not .md extension | Provide path to Markdown file |
| `INSUFFICIENT_SPEC_STRUCTURE` | <3 required sections found | Regenerate spec with required sections |
| `MISSING_FR_IDS` | No FR-XXX identifiers in FR table | Add FR IDs to requirements table |
| `INVALID_PHASE` | Phase <1 or >4 | Use phase 1-4 |
| `OUTPUT_NOT_WRITABLE` | Cannot write to output directory | Check permissions |

### Phase-Filtered Output

When `--phase=N` is provided:

```json
{
  "status": "SUCCESS",
  "spec_path": "/absolute/path/to/SPEC.md",
  "phase_filter": 2,
  "feature_dir": "/absolute/path/to/feature",
  "output_dir": "/absolute/path/to/feature",
  "spec_metadata": {
    "feature_name": "my-feature",
    "has_fr_ids": true,
    "has_moscow": true,
    "has_ice_score": false,
    "fr_count": 12,
    "sections_found": ["Context", "Functional Requirements", "Technical Constraints"],
    "estimated_complexity": "complicated",
    "phase_filter_applied": 2
  }
}
```

---

## Anti-Patterns (NEVER DO)

| Anti-Pattern | Why It Fails | Correct Approach |
|--------------|--------------|------------------|
| Skip path validation | File not found errors downstream | Always validate existence first |
| Assume relative paths | CWD varies between tool calls | Always normalize to absolute |
| Hardcode output location | Breaks different project structures | Discover from spec location |
| Ignore --phase flag | Generates all phases when user wants subset | Parse and filter appropriately |
| Return partial metadata | Downstream agents fail | Validate all gates before success |
| Use backslashes in paths | Cross-platform incompatibility | Always use forward slashes |
| Execute plan generation | Intake only parses, does not generate | Delegate generation to generating-plans |
| Modify spec file | Intake is read-only | Never write to input files |
| Skip FR table analysis | Missing critical plan inputs | Always extract FR metadata |
| Accept specs without FR-IDs | Plan generation requires FR mapping | Enforce FR-XXX format in table |

---

## Quick Reference

```
ARGUMENT FORMAT:
  /plan <path> [--phase=N]

PARSING:
  path     : Required, first non-flag token, normalize to absolute
  --phase  : Optional, integer 1-4, filters plan to single phase

DIRECTORY DISCOVERY:
  feature_dir = parent(spec_path) or parent(parent(spec_path)) if in specs/
  output_dir  = feature_dir (default) or feature_dir/plans (if exists)

VALIDATION GATES (all blocking):
  1. Path exists
  2. File is .md
  3. Has >= 3 required sections (FR, Context, User Scenarios, TC, NFR)
  4. Phase valid (if --phase provided): 1-4
  5. Output writable

REQUIRED SECTIONS (>=3 must be present):
  - Functional Requirements (FR-, Requirements)
  - Context (Background, Overview, Problem Statement)
  - User Scenarios (Use Cases, Stories)
  - Technical Constraints (TC-, Constraints, Platform)
  - Non-Functional Requirements (NFR-, Performance, Quality)

FR TABLE REQUIREMENTS:
  - Has FR-XXX identifiers
  - Preferably has MoSCoW (Must/Should/Could/Won't)
  - Preferably has ICE Score

OUTPUT CONTRACT:
  SUCCESS: { status, spec_path, phase_filter, feature_dir, output_dir, spec_metadata }
  FAILURE: { status, error_code, message, hint, suggest, context }

METADATA EXTRACTION:
  - feature_name: frontmatter > H1 > directory > filename
  - has_fr_ids: FR-XXX format present
  - has_moscow: MUST/SHOULD/COULD/WON'T present
  - has_ice_score: Impact/Confidence/Ease present
  - fr_count: Number of FR entries
  - sections_found: List of detected sections
  - estimated_complexity: simple|complicated|complex|chaotic (Cynefin)

COMPLEXITY ESTIMATION (Cynefin):
  FR count 1-5:   simple
  FR count 6-15:  complicated
  FR count 16-30: complex
  FR count >30:   chaotic
  
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
| [generating-plans](../generating-plans/SKILL.md) | Consumes intake output, generates PLAN.json |
| [validating-specifications](../validating-specifications/SKILL.md) | SPEC.md quality validation |
| [codebase-research](../codebase-research/SKILL.md) | Directory discovery patterns |
| [task-intake](../task-intake/SKILL.md) | Parallel intake skill for /tasks command |

### Command Documentation

| Document | Purpose |
|----------|---------|
| [/plan command](../../commands/plan.md) | Parent command specification |
| [/spec command](../../commands/spec.md) | SPEC.md creation command |

---

## Thinking Frameworks

**Full Catalog**: [Thinking Frameworks README](../../docs/00-core/frameworks/README.md)

**Most Relevant for Plan Intake**:

| Framework | When to Use |
|-----------|-------------|
| [ReACT](../../docs/00-core/frameworks/analysis.md) | Path resolution, iterative validation |
| [Pre-Mortem](../../docs/00-core/frameworks/strategy.md) | Anticipating parsing edge cases |
| [Cynefin](../../docs/00-core/frameworks/analysis.md) | Complexity estimation from FR count |

> **Selection Tip**: path issues -> ReACT, edge cases -> Pre-Mortem, complexity -> Cynefin
