# Delegation Patterns

Exact Task() call syntax for all agent delegations in the /tasks command.

---

## Step 3: Feature Context Synthesis

**Agent**: researcher-codebase

```python
Task(
  subagent_type="researcher-codebase",
  description="Synthesize feature context",
  prompt="""
Analyze this feature directory and extract structured metadata for task generation.

**Feature Directory**: ${FEATURE_DIR}

**Context Files to Read**:
${list_of_context_files}

**Plan Files to Scan**:
${list_of_plan_files}

**Extract and Return JSON**:
{
  "feature_name": "Derived from directory name",
  "feature_number": "Extracted from directory name if present",
  "feature_description": "High-level summary (2-3 sentences)",
  "plan_structure": "sequential_phases | parallel_components | mixed",
  "plan_structure_rationale": "Why this structure?",
  "plans": [
    {
      "file": "relative/path/from/feature_dir",
      "name": "Human-readable name",
      "component_name": "sanitized-name-for-directory",
      "type": "foundation | core | enhancement | cleanup | integration",
      "estimated_tasks": 15,
      "depends_on": ["phase-0"] or [],
      "sprint_points": 8,
      "priority": "high | medium | low"
    }
  ],
  "confidence": 0.85
}

**Return**: JSON only (no markdown, no explanations outside JSON)
"""
)
```

---

## Step 4: Parallel Task Generation

**Agent**: planning (one per plan file)

**CRITICAL**: Launch ALL planning agents in SINGLE MESSAGE for parallel execution.

```python
# Generate shared timestamp ONCE
execution_timestamp = datetime.utcnow().isoformat() + "Z"

# For EACH plan, prepare input and call Task
for plan_index, plan in enumerate(feature_synthesis.plans):
    task_id_offset = plan_index * 100
    
    Task(
      subagent_type="planning",
      description=f"Generate tasks for {plan.component_name}",
      prompt=f"""
{{
  "task_id": "task-gen-{plan_index:03d}",
  "execution_timestamp": "{execution_timestamp}",
  "plan_file_path": "{FEATURE_DIR}/{plan.file}",
  "spec_file_path": "{FEATURE_DIR}/SPEC.md",
  "task_id_offset": {task_id_offset},
  "component_context": {{
    "component_name": "{plan.component_name}",
    "type": "{plan.type}",
    "depends_on": {plan.depends_on},
    "estimated_tasks": {plan.estimated_tasks},
    "sprint_points": {plan.sprint_points},
    "priority": "{plan.priority}"
  }},
  "feature_context": {{
    "feature_name": "{feature_synthesis.feature_name}",
    "feature_number": "{feature_synthesis.feature_number}",
    "feature_description": "{feature_synthesis.feature_description}",
    "plan_structure": "{feature_synthesis.plan_structure}"
  }},
  "output_dir": "{TASK_DIR}/{plan.component_name}/"
}}
"""
    )
```

**Example for 3 Plans**:
```markdown
# Single message with 3 Task calls
Task(planning, plan-0 JSON)
Task(planning, plan-1 JSON)
Task(planning, plan-2 JSON)
```

---

## Step 6: Quality Validation

**Core Agents (ALWAYS run)**:

```python
validation_input = {
  "feature_dir": FEATURE_DIR,
  "task_files": [f"{TASK_DIR}/{c}/TASKS.json" for c in components],
  "feature_metadata": feature_synthesis,
  "aggregated_metrics": {
    "total_tasks": total_tasks,
    "parallel_tasks": total_parallel,
    "sequential_tasks": total_sequential,
    "review_groups": total_review_groups
  }
}

# Core agents (ALWAYS - 75% weight total)
Task(
  subagent_type="planning",
  description="Validate business alignment",
  prompt=f"""
Validate task list for business alignment.

**Feature**: {feature_synthesis.feature_name}
**Tasks**: {total_tasks} tasks across {len(components)} components
**Task Files**: {validation_input['task_files']}

**Analyze**:
1. Business goals coverage from SPEC.md
2. User story completeness
3. Acceptance criteria clarity
4. Risk identification

**Return JSON**:
{{
  "score": 0.0-1.0,
  "critical_issues": [],
  "improvements": [],
  "confidence": 0.0-1.0
}}
"""
)

Task(
  subagent_type="architecture", 
  description="Validate technical design",
  prompt=f"""
Validate task list for technical correctness.

**Feature**: {feature_synthesis.feature_name}
**Plan Structure**: {feature_synthesis.plan_structure}
**Task Files**: {validation_input['task_files']}

**Analyze**:
1. Dependency correctness
2. Parallel execution opportunities
3. Review checkpoint placement
4. Agent assignment appropriateness

**Return JSON**:
{{
  "score": 0.0-1.0,
  "critical_issues": [],
  "improvements": [],
  "confidence": 0.0-1.0
}}
"""
)

Task(
  subagent_type="tech-debt-investigator",
  description="Assess task quality",
  prompt=f"""
Assess generated task quality.

**Feature**: {feature_synthesis.feature_name}
**Metrics**: {validation_input['aggregated_metrics']}
**Task Files**: {validation_input['task_files']}

**Analyze**:
1. Task granularity (too large/too small?)
2. Effort estimate reasonableness
3. Test coverage adequacy
4. Documentation task presence

**Return JSON**:
{{
  "score": 0.0-1.0,
  "debt_indicators": [],
  "improvements": [],
  "confidence": 0.0-1.0
}}
"""
)
```

**Dynamic Agents (if confidence >0.8)**:

```python
# Only if 3+ components
if len(components) >= 3:
    Task(
      subagent_type="feature-analyzer",
      description="Multi-component analysis",
      prompt=f"""
Analyze cross-component task relationships.

**Components**: {components}
**Task Files**: {validation_input['task_files']}

**Analyze**:
1. Cross-component dependencies
2. Integration task coverage
3. Component boundary clarity

**Return JSON**:
{{
  "score": 0.0-1.0,
  "issues": [],
  "confidence": 0.0-1.0
}}
"""
    )

# Only if test-heavy feature detected
if test_heavy_feature:
    Task(
      subagent_type="code-quality",
      description="Test task validation",
      prompt=f"""
Validate test-related tasks.

**Task Files**: {validation_input['task_files']}

**Analyze**:
1. Test task completeness
2. Test coverage gaps
3. Test dependency ordering

**Return JSON**:
{{
  "score": 0.0-1.0,
  "issues": [],
  "confidence": 0.0-1.0
}}
"""
    )
```

---

## Synthesis Algorithm

When collecting validation results:

```python
# Weight configuration
CORE_WEIGHT = 0.75  # Split among 3 core agents (0.25 each)
DYNAMIC_WEIGHT = 0.25  # Split among 0-2 dynamic agents

# Calculate weighted score
core_score = (
    technical_pm.score * 0.25 +
    architecture_review.score * 0.25 +
    tech_debt_investigator.score * 0.25
)

if dynamic_agents:
    dynamic_score = sum(a.score for a in dynamic_agents) / len(dynamic_agents)
    final_score = core_score + (dynamic_score * DYNAMIC_WEIGHT)
else:
    final_score = core_score / 0.75  # Normalize if no dynamic

# Determine status
if any(a.critical_issues for a in all_agents):
    status = "BLOCKED"
elif final_score < 0.7:
    status = "NEEDS_FIXES"
else:
    status = "APPROVED"
```
