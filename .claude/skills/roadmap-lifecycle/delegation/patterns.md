# Delegation Patterns

Task() templates for roadmap-lifecycle skill operations.

---

## ASSESS Operation Patterns

### 1. Gather Project Artifacts

**Agent**: `researcher-codebase` (can run in parallel)

```python
Task(
    subagent_type="researcher-codebase",
    prompt="""Assess project maturity by gathering key artifacts.

    **Search for these artifact categories:**

    1. **Project Definition**
       - PROJECT-SPEC.md or equivalent
       - README.md with project description
       - Architecture documentation

    2. **Roadmap & Planning**
       - ROADMAP.md or release plans
       - Sprint/iteration documentation
       - Feature backlogs

    3. **Testing Infrastructure**
       - pytest.ini, pyproject.toml test config
       - tests/ directory structure
       - Coverage reports (.coverage, htmlcov/)

    4. **CI/CD & Deployment**
       - .github/workflows/ or CI configs
       - Dockerfile, docker-compose.yml
       - k8s/ or deployment manifests

    5. **Observability**
       - Logging configuration
       - Metrics/monitoring setup
       - Alert definitions

    6. **Security**
       - Security scan configs (semgrep, bandit)
       - .env.example (secrets management)
       - Auth/authz implementations

    7. **Documentation**
       - docs/ directory structure
       - API documentation
       - Runbooks/playbooks

    **Output Format:**
    ```json
    {
        "artifacts_found": [
            {"category": "...", "path": "...", "exists": true/false}
        ],
        "maturity_indicators": {
            "testing": {"coverage_percent": N, "has_integration": bool},
            "deployment": {"has_ci": bool, "has_cd": bool, "environments": [...]},
            "observability": {"has_logging": bool, "has_metrics": bool},
            "security": {"has_scans": bool, "secrets_managed": bool},
            "documentation": {"has_api_docs": bool, "has_runbooks": bool}
        },
        "confidence": 0.0-1.0
    }
    ```"""
)
```


### 2. Validate Stage Gates

**Agent**: `architectureer` (can run in parallel)

```python
Task(
    subagent_type="architectureer",
    prompt="""Validate project against {stage} stage quality gates.

    **Context:**
    - Detected stage: {detected_stage}
    - Project artifacts: {artifact_paths}
    - Maturity indicators: {maturity_indicators}

    **Validate against stage requirements from:**
    - `.claude/skills/roadmap-lifecycle/stages/{stage}-stage.md`
    - `.claude/docs/01-guides/architecture/architecture-stage-policies.md`

    **Score each dimension (1-10):**
    1. Architecture
    2. Data & Migrations
    3. Observability
    4. Testing
    5. Release & Deployment
    6. Security
    7. Capacity & Cost
    8. Documentation
    9. LLM Integration (if applicable)

    **Output Format:**
    ```json
    {
        "stage_validated": true/false,
        "overall_score": N.N,
        "dimension_scores": {
            "architecture": N,
            "data_migrations": N,
            ...
        },
        "gate_violations": [
            {"dimension": "...", "required": N, "actual": N, "gap": "..."}
        ],
        "recommendations": ["..."]
    }
    ```"""
)
```

---

## GENERATE Operation Patterns

### 3. Create/Update Roadmap

**Agent**: `planning` (sequential - depends on assessment)

```python
Task(
    subagent_type="planning",
    prompt="""Create stage-aware roadmap for {project_name}.

    **Context:**
    - Current stage: {current_stage}
    - Stage definition: `.claude/skills/roadmap-lifecycle/stages/{current_stage}-stage.md`
    - Project spec: {project_spec_path}
    - Assessment results: {assessment_summary}

    **Requirements:**
    1. Apply stage-specific quality thresholds
    2. Include stage exit criteria as phase success gates
    3. Defer features inappropriate for current stage
    4. Mark stage transition milestones clearly
    5. Use ICE scoring aligned with stage context

    **Stage Constraints for {current_stage}:**
    {stage_constraints}

    **Output:** Updated ROADMAP.md at `docs/00-project/roadmaps/`"""
)
```

---

## ADVANCE Operation Patterns

### 4. Generate Transition Tasks

**Agent**: `planning` (sequential - depends on gap analysis)

```python
Task(
    subagent_type="planning",
    prompt="""Generate transition tasks from {current_stage} to {next_stage}.

    **Context:**
    - Exit criteria for {current_stage}: {exit_criteria}
    - Entry criteria for {next_stage}: {entry_criteria}
    - Current completion status: {completion_status}
    - Identified gaps: {gaps}

    **For each gap, generate:**
    1. Task description (actionable, specific)
    2. Acceptance criteria (testable)
    3. Effort estimate (S/M/L, not time)
    4. Dependencies (other tasks, external)
    5. Recommended agent for implementation

    **Group into work streams (max 5):**
    - Infrastructure/Deployment
    - Testing/Quality
    - Security/Compliance
    - Documentation/Process
    - Feature Completion

    **Output Format:** Transition checklist using template at
    `templates/transition-checklist.template.md`"""
)
```

---

## Parallel vs Sequential Guide

| Pattern | Parallel? | Reason |
|---------|-----------|--------|
| Gather artifacts | Yes | Read-only exploration |
| Validate stage gates | Yes | Independent analysis |
| Create roadmap | No | Depends on assessment |
| Generate tasks | No | Depends on gap analysis |


---

## Error Handling Patterns

### Artifact Not Found

```python
# If researcher-codebase returns empty artifacts
if not artifacts_found:
    # Ask user for project location
    AskUserQuestion(
        "I couldn't find standard project artifacts. "
        "Please provide the path to your project's main documentation."
    )
```

### Stage Ambiguous

```python
# If score falls on boundary (e.g., 3.4-3.5)
if score_is_ambiguous:
    # Present options to user
    AskUserQuestion(
        f"Your score ({score}) is on the boundary between {stage1} and {stage2}. "
        "Which stage better describes your current situation?",
        options=[stage1, stage2]
    )
```

### Gate Violation

```python
# If stage gate validation fails
if gate_violations:
    # Show gaps and suggest remediation
    for violation in gate_violations:
        print(f"Gap: {violation.dimension} requires {violation.required}, "
              f"currently at {violation.actual}")
    # Offer to run Advance operation
    AskUserQuestion("Would you like to generate tasks to address these gaps?")
```
