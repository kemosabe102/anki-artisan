---
name: plan-presentation
description: >
  Use this skill when formatting validated plans as PLAN.json output.
  Generates summaries and next step instructions.
  Trigger keywords: plan output, format plan, PLAN.json, plan summary.
---

# Plan Presentation Skill

**Domain**: Planning  
**Responsibility**: Format and present plan generation results (Final step of /plan workflow)  
**Triggers**:
  - Plan ready for output
  - Generate PLAN.json file
  - Create plan summary report
  - Prepare for /tasks handoff

---

## Overview

Owns the methodology and operations for:
- Formatting PLAN.json machine-readable output
- Creating summary reports with metrics
- Providing next step instructions for /tasks workflow
- Validating output structure before delivery


**Does NOT own**:
- Plan generation logic (see `plan-generation` skill)
- Validation algorithms (see `generating-plans` skill)
- SPEC.md parsing (see `plan-intake` skill)
- Task generation (see /tasks command)

---

## Input Contract

### From plan-generation
- `plan` - Validated plan object with phases and features
- `validation_result` - Validation status with quality_score

### From plan-intake
- `output_dir` - Target directory for PLAN.json output
- `feature_name` - Name for filename generation

### From plan-risk-assessment
- `research_recommendations[]` - Array of risk recommendations with structure:
  - `step_id` - Identifier for the affected step
  - `step_description` - Human-readable step description
  - `priority` - MUST | SHOULD | COULD
  - `risk_factors[]` - List of identified risk factors
  - `topics[]` - Specific topics to research
  - `rationale` - Why this research is needed
- `summary` - Counts by priority: `{ must: N, should: N, could: N }`

---

## Output Contract

```json
{
  "status": "SUCCESS|FAILURE",
  "output_files": {
    "plan_json": "/path/to/feature/feature-name-PLAN.json"
  },
  "summary": {
    "project": "Feature Name",
    "total_features": 8,
    "total_phases": 3,
    "must_requirements": 4,
    "should_requirements": 3,
    "could_requirements": 1,
    "estimated_hours": 24,
    "quality_score": 0.87
  },
  "research_summary": {
    "must_count": 2,
    "should_count": 3,
    "could_count": 1,
    "estimated_research_hours": 4.5
  },
  "next_step": "/tasks /path/to/feature/feature-name-PLAN.json"
}
```

---

## Output Generation Pipeline

### Transformation Flow

```
Validated Plan Input
    |
+---------------------------------------------------------------+
| STEP 1: Input Validation                                       |
|   -> Verify plan object structure                              |
|   -> Confirm validation_result.valid == true                   |
|   -> Extract output_dir from intake                            |
+---------------------------------------------------------------+
    |
+---------------------------------------------------------------+
| STEP 2: Filename Resolution                                    |
|   -> Apply: filename_pattern algorithm                         |
|   -> Generate: {feature-name}-PLAN.json                        |
|   -> Resolve: absolute output path                             |
+---------------------------------------------------------------+
    |
+---------------------------------------------------------------+
| STEP 3: JSON Serialization                                     |
|   -> Apply: plan_to_json algorithm                             |
|   -> Pretty-print with 2-space indent                          |
|   -> Validate UTF-8 encoding                                   |
+---------------------------------------------------------------+
    |
+---------------------------------------------------------------+
| STEP 4: Summary Calculation                                    |
|   -> Count features by MoSCoW priority                         |
|   -> Sum estimated hours                                       |
|   -> Calculate phase count                                     |
|   -> Extract quality score                                     |
+---------------------------------------------------------------+
    |
+---------------------------------------------------------------+
| STEP 5: Next Step Generation                                   |
|   -> Format /tasks command with PLAN.json path                 |
|   -> Include execution hints                                   |
+---------------------------------------------------------------+
    |
+---------------------------------------------------------------+
| STEP 6: Output Assembly                                        |
|   -> Write PLAN.json to output_dir                             |
|   -> Construct response with summary                           |
|   -> Include next_step instruction                             |
+---------------------------------------------------------------+
    |
SUCCESS Response (or FAILURE if any step fails)
```

### Prerequisites

- **Required Input**: Validated plan object from plan-generation
- **Required Data**: validation_result with quality_score >= 0.70
- **Required Path**: output_dir from plan-intake

---

## JSON Serialization

### Filename Pattern Algorithm

```
FUNCTION resolve_output_filename(feature_name: str, output_dir: str) -> str:
  """
  Generate PLAN.json filename from feature name.
  
  Pattern: {feature-name}-PLAN.json
  
  Examples:
    feature_name="User Authentication" -> "user-authentication-PLAN.json"
    feature_name="api-gateway" -> "api-gateway-PLAN.json"
    feature_name="My Feature v2" -> "my-feature-v2-PLAN.json"
  """
  
  # Normalize feature name to kebab-case
  normalized = feature_name.lower()
  normalized = re.sub(r'[^a-z0-9]+', '-', normalized)
  normalized = normalized.strip('-')
  
  # Construct filename
  filename = f"{normalized}-PLAN.json"
  
  # Resolve absolute path
  output_path = os.path.join(output_dir, filename)
  output_path = output_path.replace('\\', '/')  # Normalize slashes
  
  RETURN output_path
```

### Plan-to-JSON Algorithm

```python
def serialize_plan_to_json(plan: dict, metadata: dict) -> str:
    """
    Serialize validated plan to JSON format.
    
    Args:
        plan: Validated plan object from plan-generation
        metadata: Generation metadata (timestamps, source, etc.)
        
    Returns:
        JSON string with 2-space indentation, UTF-8 encoded
    """
    
    output_structure = {
        "metadata": {
            "version": "1.0.0",
            "generated_at": metadata.get("generated_at", datetime.utcnow().isoformat() + "Z"),
            "spec_source": metadata.get("spec_source", ""),
            "complexity_classification": metadata.get("complexity_classification", "COMPLICATED"),
            "quality_score": metadata.get("quality_score", 0.0)
        },
        "project": plan.get("project", "Unknown Project"),
        "description": plan.get("description", ""),
        "phases": plan.get("phases", {}),
        "summary": plan.get("summary", {}),
        "validation": {
            "algorithms_applied": metadata.get("algorithms_applied", []),
            "gate_results": metadata.get("validation_results", {})
        }
    }
    
    # Serialize with pretty-printing
    json_output = json.dumps(
        output_structure,
        indent=2,
        ensure_ascii=False,  # Allow UTF-8 characters
        sort_keys=False      # Preserve insertion order
    )
    
    return json_output
```


### JSON Schema Validation

```
VALIDATE json_output against schema:
  - metadata.version: string, required
  - metadata.generated_at: ISO-8601 string, required
  - metadata.spec_source: string, required
  - metadata.complexity_classification: enum[SIMPLE|COMPLICATED|COMPLEX|CHAOTIC]
  - metadata.quality_score: number 0.0-1.0, required
  - project: string, required
  - description: string, optional
  - phases: object with phase_N keys, required
  - phases.phase_N.name: string, required
  - phases.phase_N.duration_weeks: integer >= 1, required
  - phases.phase_N.features: array, required
  - summary: object, required
  - validation.algorithms_applied: array of strings, required
  - validation.gate_results: object, required
```

### UTF-8 Encoding Validation

```
FUNCTION validate_utf8_encoding(json_string: str) -> bool:
  """Ensure JSON output is valid UTF-8."""
  TRY:
    encoded = json_string.encode('utf-8')
    decoded = encoded.decode('utf-8')
    RETURN decoded == json_string
  EXCEPT UnicodeError:
    RETURN False
```

---

## Summary Generation

### Summary Calculation Algorithm

```python
def calculate_plan_summary(plan: dict) -> dict:
    """
    Calculate summary metrics from validated plan.
    
    Returns:
        {
            "project": str,
            "total_features": int,
            "total_phases": int,
            "must_requirements": int,
            "should_requirements": int,
            "could_requirements": int,
            "estimated_hours": float,
            "quality_score": float
        }
    """
    
    summary = {
        "project": plan.get("project", "Unknown"),
        "total_features": 0,
        "total_phases": 0,
        "must_requirements": 0,
        "should_requirements": 0,
        "could_requirements": 0,
        "estimated_hours": 0.0,
        "quality_score": 0.0
    }
    
    phases = plan.get("phases", {})
    summary["total_phases"] = len(phases)
    
    for phase_key, phase_data in phases.items():
        features = phase_data.get("features", [])
        
        for feature in features:
            summary["total_features"] += 1
            
            # Count by MoSCoW priority
            priority = feature.get("priority", "").lower()
            if priority == "must":
                summary["must_requirements"] += 1
            elif priority == "should":
                summary["should_requirements"] += 1
            elif priority == "could":
                summary["could_requirements"] += 1
            
            # Sum estimated hours
            hours = feature.get("estimated_hours", 0.0)
            summary["estimated_hours"] += hours
    
    # Round hours to 1 decimal place
    summary["estimated_hours"] = round(summary["estimated_hours"], 1)
    
    return summary
```


### Summary Display Template

```markdown
## Plan Generation Summary

| Metric | Value |
|--------|-------|
| Project | {project} |
| Total Features | {total_features} |
| Total Phases | {total_phases} |
| Estimated Hours | {estimated_hours} |
| Quality Score | {quality_score} |

### MoSCoW Distribution

| Priority | Count | Percentage |
|----------|-------|------------|
| Must | {must_requirements} | {must_pct}% |
| Should | {should_requirements} | {should_pct}% |
| Could | {could_requirements} | {could_pct}% |

### Phase Breakdown

| Phase | Features | Hours | Priority Focus |
|-------|----------|-------|----------------|
| Phase 1 | {p1_features} | {p1_hours} | {p1_focus} |
| Phase 2 | {p2_features} | {p2_hours} | {p2_focus} |
| Phase 3 | {p3_features} | {p3_hours} | {p3_focus} |
```

---

## Research Recommendations Display

### Visual Distinction Markers

| Priority | Marker | Meaning |
|----------|--------|---------|
| MUST | ⛔ | Critical - Blocks implementation until resolved |
| SHOULD | ⚠️ | Important - Recommended before implementation |
| COULD | ℹ️ | Optional - Nice to have, can proceed without |

### Research Summary Statistics

Display at the top of Research Recommendations section:

```markdown
**Research Summary**: {must_count} MUST | {should_count} SHOULD | {could_count} COULD items
**Estimated Research Time**: {estimated_research_hours} hours
```

**Time Estimation Formula**:
- MUST topics: 1.5 hours per topic (thorough investigation required)
- SHOULD topics: 1.0 hour per topic (standard research depth)
- COULD topics: 0.5 hours per topic (quick verification)

### Research Recommendations Template

```markdown
## Research Recommendations

**Research Summary**: {must_count} MUST | {should_count} SHOULD | {could_count} COULD items
**Estimated Research Time**: {estimated_research_hours} hours

### MUST Research (Required Before Implementation)

⛔ **{step_id}**: {step_description}
   - **Risk Factors**: {risk_factor_1}, {risk_factor_2}
   - **Topics to Research**:
     - [ ] {topic_1}
     - [ ] {topic_2}
   - **Rationale**: {rationale}

⛔ **{step_id}**: {step_description}
   - **Risk Factors**: {risk_factors}
   - **Topics to Research**:
     - [ ] {topic}
   - **Rationale**: {rationale}

### SHOULD Research (Recommended)

⚠️ **{step_id}**: {step_description}
   - **Risk Factors**: {risk_factors}
   - **Topics to Research**:
     - [ ] {topic}
   - **Rationale**: {rationale}

### COULD Research (Optional)

ℹ️ **{step_id}**: {step_description}
   - **Topics**: {topics}
```

### Conditional Rendering

When no research recommendations exist:

```markdown
## Research Recommendations

✅ No high-risk items identified. Proceed with implementation.
```

When only SHOULD/COULD exist (no blockers):

```markdown
## Research Recommendations

**Research Summary**: 0 MUST | {should_count} SHOULD | {could_count} COULD items
**Estimated Research Time**: {estimated_research_hours} hours

✅ No blocking research required. Optional research items listed below.

### SHOULD Research (Recommended)
...

### COULD Research (Optional)
...
```

### Research Recommendation Rendering Algorithm

```python
def render_research_recommendations(recommendations: list, summary: dict) -> str:
    """
    Render research recommendations with visual distinction.
    
    Args:
        recommendations: List of research recommendation objects
        summary: { must: int, should: int, could: int }
        
    Returns:
        Formatted markdown string
    """
    
    # Handle empty case
    if not recommendations or (summary.get('must', 0) + summary.get('should', 0) + summary.get('could', 0) == 0):
        return """## Research Recommendations

✅ No high-risk items identified. Proceed with implementation.
"""
    
    # Calculate estimated time
    must_count = summary.get('must', 0)
    should_count = summary.get('should', 0)
    could_count = summary.get('could', 0)
    
    # Count topics per priority for time estimation
    must_topics = sum(len(r.get('topics', [])) for r in recommendations if r.get('priority') == 'MUST')
    should_topics = sum(len(r.get('topics', [])) for r in recommendations if r.get('priority') == 'SHOULD')
    could_topics = sum(len(r.get('topics', [])) for r in recommendations if r.get('priority') == 'COULD')
    
    estimated_hours = (must_topics * 1.5) + (should_topics * 1.0) + (could_topics * 0.5)
    
    # Build output
    output = [f"""## Research Recommendations

**Research Summary**: {must_count} MUST | {should_count} SHOULD | {could_count} COULD items
**Estimated Research Time**: {estimated_hours:.1f} hours
"""]
    
    # No blockers message if applicable
    if must_count == 0 and (should_count > 0 or could_count > 0):
        output.append("\n✅ No blocking research required. Optional research items listed below.\n")
    
    # Group by priority
    priority_groups = {
        'MUST': [r for r in recommendations if r.get('priority') == 'MUST'],
        'SHOULD': [r for r in recommendations if r.get('priority') == 'SHOULD'],
        'COULD': [r for r in recommendations if r.get('priority') == 'COULD']
    }
    
    markers = {'MUST': '⛔', 'SHOULD': '⚠️', 'COULD': 'ℹ️'}
    headers = {
        'MUST': '### MUST Research (Required Before Implementation)',
        'SHOULD': '### SHOULD Research (Recommended)', 
        'COULD': '### COULD Research (Optional)'
    }
    
    for priority in ['MUST', 'SHOULD', 'COULD']:
        items = priority_groups[priority]
        if not items:
            continue
            
        output.append(f"\n{headers[priority]}\n")
        
        for item in items:
            marker = markers[priority]
            step_id = item.get('step_id', 'Unknown')
            step_desc = item.get('step_description', '')
            risk_factors = ', '.join(item.get('risk_factors', []))
            topics = item.get('topics', [])
            rationale = item.get('rationale', '')
            
            output.append(f"\n{marker} **{step_id}**: {step_desc}")
            output.append(f"   - **Risk Factors**: {risk_factors}")
            output.append("   - **Topics to Research**:")
            for topic in topics:
                output.append(f"     - [ ] {topic}")
            output.append(f"   - **Rationale**: {rationale}\n")
    
    return '\n'.join(output)
```

---

## Next Step Instructions

### Command Format Generation

```python
def generate_next_step(plan_json_path: str) -> str:
    """
    Generate the /tasks command for the next workflow step.
    
    Args:
        plan_json_path: Absolute path to generated PLAN.json
        
    Returns:
        Formatted command string for /tasks invocation
    """
    
    # Normalize path (forward slashes)
    normalized_path = plan_json_path.replace('\\', '/')
    
    # Generate command
    next_step = f"/tasks {normalized_path}"
    
    return next_step
```

### Next Step Display Template

Include this in every plan presentation output:

```markdown
## Next Steps

### Execute Task Generation

To generate implementation tasks from this plan:

```
/tasks {plan_json_path}
```

### Alternative Options

**Generate tasks for specific phase:**
```
/tasks {plan_json_path} --phase=1
```

**Preview without writing files:**
```
/tasks {plan_json_path} --dry-run
```

### What Happens Next

1. `/tasks` parses the PLAN.json file
2. Converts features to actionable tasks with TDD pairing
3. Assigns agents to each task based on domain
4. Generates `tasks.md` and `TASKS.json` for `/implement`
```

---

## File Location Resolution

### Output Path Determination

```
FUNCTION resolve_output_path(intake_result: dict, feature_name: str) -> str:
  """
  Determine where to write PLAN.json based on intake discovery.
  
  Priority:
    1. output_dir from intake (discovered from SPEC.md location)
    2. feature_dir from intake (parent of SPEC.md)
    3. Same directory as SPEC.md
  """
  
  # Primary: Use output_dir from intake
  IF intake_result.get("output_dir"):
    output_dir = intake_result["output_dir"]
  
  # Fallback: Use feature_dir
  ELIF intake_result.get("feature_dir"):
    output_dir = intake_result["feature_dir"]
  
  # Last resort: Extract from spec_path
  ELSE:
    spec_path = intake_result.get("spec_path", "")
    output_dir = os.path.dirname(spec_path)
  
  # Normalize path
  output_dir = output_dir.replace('\\', '/')
  
  # Generate filename
  filename = resolve_output_filename(feature_name, output_dir)
  
  RETURN filename
```

### Directory Structure Patterns

**Pattern A: PLAN.json alongside SPEC.md**
```
feature/
  SPEC.md          <- Input
  feature-PLAN.json <- Output (same directory)
```

**Pattern B: Separate plans directory**
```
feature/
  specs/
    SPEC.md        <- Input
  plans/
    feature-PLAN.json <- Output (plans/ subdir)
```

**Pattern C: Docs planning directory**
```
docs/01-planning/
  feature-name/
    SPEC.md             <- Input
    feature-name-PLAN.json <- Output (same directory)
```

---

## Output Contract

### Success Response Schema

```json
{
  "status": "SUCCESS",
  "output_files": {
    "plan_json": "/absolute/path/to/feature-name-PLAN.json"
  },
  "summary": {
    "project": "Feature Name",
    "total_features": 8,
    "total_phases": 3,
    "must_requirements": 4,
    "should_requirements": 3,
    "could_requirements": 1,
    "estimated_hours": 24.5,
    "quality_score": 0.87
  },
  "next_step": "/tasks /absolute/path/to/feature-name-PLAN.json",
  "metadata": {
    "generated_at": "2025-12-17T10:30:00Z",
    "spec_source": "/path/to/SPEC.md",
    "complexity_classification": "COMPLICATED"
  }
}
```

### Failure Response Schema

```json
{
  "status": "FAILURE",
  "error": {
    "code": "SERIALIZATION_FAILED|WRITE_FAILED|VALIDATION_FAILED",
    "message": "Human-readable error description",
    "details": {}
  },
  "partial_output": null,
  "recovery_actions": [
    "Check output directory permissions",
    "Verify plan structure is complete"
  ]
}
```


### Error Codes

| Code | Trigger | Recovery |
|------|---------|----------|
| `SERIALIZATION_FAILED` | JSON encoding error | Check plan structure for invalid types |
| `WRITE_FAILED` | Cannot write to output directory | Verify directory exists and is writable |
| `VALIDATION_FAILED` | Plan validation score < 0.70 | Address validation warnings before presentation |
| `INVALID_INPUT` | Missing required plan fields | Ensure plan-generation completed successfully |
| `PATH_RESOLUTION_FAILED` | Cannot determine output path | Verify intake provided valid output_dir |

### Quality Thresholds

| Score Range | Grade | Presentation Action |
|-------------|-------|---------------------|
| >= 0.85 | PASS | Full presentation with SUCCESS status |
| 0.70 - 0.84 | WARN | Present with warnings in summary |
| < 0.70 | FAIL | Return FAILURE, do not write PLAN.json |

---

## Anti-Patterns (NEVER DO)

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|----------------|------------------|
| Write PLAN.json before validation passes | May output invalid/incomplete plan | Verify quality_score >= 0.70 first |
| Skip summary calculation | User cannot assess plan quality | Always include summary metrics |
| Output without next_step | User unsure how to proceed | Include /tasks command |
| Use relative paths in output | Breaks cross-directory execution | Always use absolute paths |
| Single-number hour estimates | Hides estimation uncertainty | Include total with breakdown by phase |
| Hardcode output filename | Ignores feature naming | Use filename_pattern algorithm |
| Skip UTF-8 validation | May corrupt non-ASCII content | Always validate encoding |
| Present plan without MoSCoW counts | User cannot assess priority balance | Include must/should/could breakdown |
| Minify JSON output | Human-unreadable for debugging | Always pretty-print with 2-space indent |
| Write to input directory blindly | May overwrite existing files | Resolve output_dir from intake |
| Return partial output on failure | Downstream expects complete output | Either SUCCESS or FAILURE, never partial |
| Skip quality_score in summary | User cannot gauge plan reliability | Always include quality_score |

### Output Anti-Patterns

```
# WRONG: Missing output_files
{
  "status": "SUCCESS",
  "summary": {...}
  // No output_files!
}

# WRONG: Relative path in output_files
{
  "status": "SUCCESS",
  "output_files": {
    "plan_json": "./feature-PLAN.json"  // WRONG: relative path
  }
}

# WRONG: Missing next_step
{
  "status": "SUCCESS",
  "output_files": {...},
  "summary": {...}
  // No next_step instruction!
}

# CORRECT: All required fields present
{
  "status": "SUCCESS",
  "output_files": {
    "plan_json": "/absolute/path/to/feature-PLAN.json"
  },
  "summary": {
    "project": "Feature Name",
    "total_features": 8,
    "total_phases": 3,
    "must_requirements": 4,
    "should_requirements": 3,
    "could_requirements": 1,
    "estimated_hours": 24.5,
    "quality_score": 0.87
  },
  "next_step": "/tasks /absolute/path/to/feature-PLAN.json"
}
```

---

## Quick Reference

```
PLAN PRESENTATION PROTOCOL:

  Input Contract:
    {
      plan: validated plan object from plan-generation,
      validation_result: { valid: bool, quality_score: float, gate_results: {} },
      output_dir: string (from plan-intake),
      research_recommendations: [] (from plan-risk-assessment),
      research_summary: { must: int, should: int, could: int }
    }

  Pipeline Steps (in order):
    1. Input Validation   -> Verify plan + validation_result
    2. Filename Resolution -> {feature-name}-PLAN.json
    3. JSON Serialization  -> Pretty-print, 2-space indent, UTF-8
    4. Summary Calculation -> Count features, hours, MoSCoW distribution
    5. Research Rendering  -> Format recommendations with visual markers
    6. Next Step Generation -> /tasks {plan_json_path}
    7. Output Assembly     -> Write file, construct response

  Filename Pattern:
    {feature-name}-PLAN.json
    
    Examples:
      "User Authentication" -> "user-authentication-PLAN.json"
      "api-gateway" -> "api-gateway-PLAN.json"
      "My Feature v2" -> "my-feature-v2-PLAN.json"

  JSON Structure:
    {
      "metadata": { version, generated_at, spec_source, complexity, quality_score },
      "project": string,
      "description": string,
      "phases": { phase_N: { name, duration_weeks, features[] } },
      "summary": { total_features, estimated_hours, critical_path, gates },
      "validation": { algorithms_applied[], gate_results{} }
    }

  Summary Metrics:
    - project: Feature name
    - total_features: Count of all features across phases
    - total_phases: Number of phases (1-4)
    - must_requirements: Count of Must priority features
    - should_requirements: Count of Should priority features
    - could_requirements: Count of Could priority features
    - estimated_hours: Sum of feature.estimated_hours
    - quality_score: From validation_result (0.0-1.0)

  Quality Thresholds:
    >= 0.85  -> PASS (present with SUCCESS)
    0.70-0.84 -> WARN (present with warnings)
    < 0.70   -> FAIL (return FAILURE, no output)

  Next Step Format:
    /tasks /absolute/path/to/feature-name-PLAN.json

  Research Recommendation Display:
    Visual Markers:
      MUST  -> ⛔ (blocks implementation)
      SHOULD -> ⚠️ (recommended before implementation)
      COULD -> ℹ️ (optional, nice to have)
    
    Time Estimation:
      MUST topics: 1.5 hours each
      SHOULD topics: 1.0 hour each
      COULD topics: 0.5 hours each
    
    Empty Case:
      "✅ No high-risk items identified. Proceed with implementation."

  Output Contract:
    SUCCESS: {
      status: "SUCCESS",
      output_files: { plan_json: "/path/to/feature-PLAN.json" },
      summary: { project, total_features, total_phases, must/should/could, hours, score },
      research_summary: { must_count, should_count, could_count, estimated_research_hours },
      next_step: "/tasks /path/to/feature-PLAN.json"
    }
    FAILURE: {
      status: "FAILURE",
      error: { code, message, details },
      recovery_actions: []
    }

  File Location Resolution:
    1. output_dir from intake (primary)
    2. feature_dir from intake (fallback)
    3. dirname(spec_path) (last resort)

  Path Rules:
    - Always forward slashes
    - Always absolute paths
    - Normalize from intake result
```

---

## Handoff Checklist

Before presenting output to user, verify:

- [ ] PLAN.json file written to expected location
- [ ] Quality score >= 0.70 (or FAIL if below)
- [ ] All MoSCoW priorities counted accurately
- [ ] Estimated hours summed correctly
- [ ] Research recommendations rendered with correct visual markers
- [ ] Research time estimation calculated (MUST: 1.5h, SHOULD: 1.0h, COULD: 0.5h per topic)
- [ ] Empty research case displays success message
- [ ] Phase count matches actual phases
- [ ] Next step command includes absolute path
- [ ] JSON is valid and UTF-8 encoded
- [ ] Summary includes all required metrics

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [plan-generation](../plan-generation/SKILL.md) | Upstream - provides validated plan object |
| [plan-intake](../plan-intake/SKILL.md) | Upstream - provides output_dir and feature context |
| [generating-plans](../generating-plans/SKILL.md) | Source of validation algorithms and quality scoring |
| [task-intake](../task-intake/SKILL.md) | Downstream - consumes PLAN.json for task generation |
| [task-presentation](../task-presentation/SKILL.md) | Parallel - similar presentation pattern for tasks |

---

## Cross-References

- **Plan Generation**: [plan-generation/SKILL.md](../plan-generation/SKILL.md)
- **Plan Intake**: [plan-intake/SKILL.md](../plan-intake/SKILL.md)
- **Task Generation**: [generating-tasks/SKILL.md](../generating-tasks/SKILL.md)
- **Thinking Frameworks**: [../../docs/00-core/frameworks/README.md](../../docs/00-core/frameworks/README.md)

---

## Thinking Frameworks

**Full Catalog**: [Thinking Frameworks README](../../docs/00-core/frameworks/README.md)

**Most Relevant for Plan Presentation**:

| Framework | When to Use |
|-----------|-------------|
| [Pre-Mortem](../../docs/00-core/frameworks/strategy.md) | Validate output before delivery |
| [SCAMPER](../../docs/00-core/frameworks/creative.md) | Optimize summary presentation |

> **Selection Tip**: output validation -> Pre-Mortem, presentation optimization -> SCAMPER
