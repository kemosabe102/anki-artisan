# Phase 1: ASSESS - Stage Determination

**OODA Phase**: OBSERVE
**Operation**: Assess
**Purpose**: Determine current project stage via 9-dimension maturity scoring

---

## Overview

The Assess operation analyzes project artifacts and scores against the 9-dimension maturity framework to determine the current lifecycle stage (MVP, Alpha, Beta, or GA).

**Input**: Project path or current working directory
**Output**: Stage Assessment Report (see `templates/stage-assessment.template.md`)

---

## Workflow Steps

### Step 1.1: Gather Project Artifacts

**Delegate to**: `researcher-codebase`
**Execution**: Parallel (can run alongside Step 1.2 prep)

**Artifacts to locate**:

| Category | Files to Find | Maturity Signal |
|----------|---------------|-----------------|
| Project Definition | PROJECT-SPEC.md, README.md | Basic project structure |
| Roadmap | ROADMAP.md, release docs | Planning maturity |
| Testing | pytest.ini, tests/, .coverage | Quality assurance |
| CI/CD | .github/workflows/, Dockerfile | Deployment maturity |
| Observability | logging config, metrics setup | Operations readiness |
| Security | security scans, .env.example | Security posture |
| Documentation | docs/, API docs, runbooks | Knowledge management |

**Expected Output**:
```json
{
    "artifacts_found": [...],
    "maturity_indicators": {...},
    "confidence": 0.0-1.0
}
```

See [delegation/patterns.md](../delegation/patterns.md) for full Task() template.

---

### Step 1.2: Score Maturity Dimensions

**Delegate to**: `architectureer`
**Execution**: Parallel (after artifacts gathered)

**Dimensions to score (1-10)**:

| # | Dimension | Source | Key Evidence |
|---|-----------|--------|--------------|
| 1 | Architecture | Code structure | Module boundaries, patterns |
| 2 | Data & Migrations | DB setup | Schema versioning, migrations |
| 3 | Observability | Logging/metrics | Structured logs, dashboards |
| 4 | Testing | Test suite | Coverage %, test types |
| 5 | Release & Deployment | CI/CD | Pipeline, environments |
| 6 | Security | Security config | Auth, scans, secrets mgmt |
| 7 | Capacity & Cost | Infrastructure | Scaling config, cost tracking |
| 8 | Documentation | Docs | README, API docs, runbooks |
| 9 | LLM Integration | AI components | Model usage, prompts |

**Scoring Guidelines**:
- 1-3: MVP level (basic, manual, minimal)
- 4-5: Alpha level (structured, automated basics)
- 6-8: Beta level (comprehensive, resilient)
- 9-10: GA level (production-grade, continuous)

---

### Step 1.3: Map Score to Stage

**Logic** (no delegation - skill performs):

```python
def determine_stage(overall_score: float) -> str:
    if overall_score < 3.5:
        return "MVP"
    elif overall_score < 5.5:
        return "Alpha"
    elif overall_score < 8.0:
        return "Beta"
    else:
        return "GA"
```

**Stage Thresholds**:

| Stage | Score Range | Quality Minimum |
|-------|-------------|-----------------|
| MVP | 1.0 - 3.4 | 3.5 overall |
| Alpha | 3.5 - 5.4 | 3.7 overall |
| Beta | 5.5 - 7.9 | 3.8 overall |
| GA | 8.0 - 10.0 | 4.2 overall |

---

### Step 1.4: Validate Stage Gates

**Delegate to**: `architectureer` (with stage parameter)
**Execution**: Sequential (after stage determined)

**Validate**:
1. Overall score meets stage minimum
2. Critical dimension scores meet thresholds
3. Risk levels within tolerance
4. Required validations completed

**Stage Gate Sources**:
- `stages/{stage}-stage.md` - Stage-specific criteria
- `architecture-stage-policies.md` - Quality thresholds

---

### Step 1.5: Identify Gaps to Next Stage

**Logic** (no delegation - skill calculates):

For each dimension:
```python
gap = next_stage_target - current_score
if gap > 0:
    gaps.append({
        "dimension": dimension,
        "current": current_score,
        "target": next_stage_target,
        "gap": gap,
        "priority": "critical" if gap > 2 else "recommended"
    })
```

---

### Step 1.6: Generate Assessment Report

**Output**: Stage Assessment Report

Use template: `templates/stage-assessment.template.md`

Fill placeholders with:
- Project metadata
- Dimension scores
- Gate validation results
- Gaps to next stage
- Recommendations

---

### Step 1.7: User Confirmation

**Required**: User must confirm or override detected stage

**Present to user**:
```
Assessment complete:
- Detected Stage: {stage}
- Overall Score: {score}/10
- Confidence: {confidence}%

Does this match your understanding? (Yes / Override to different stage)
```

---

## Quick Checklist

- [ ] Project artifacts gathered
- [ ] All 9 dimensions scored
- [ ] Stage determined from score
- [ ] Stage gates validated
- [ ] Gaps to next stage identified
- [ ] Assessment report generated
- [ ] User confirmation obtained

---

## Exit Criteria

- Assessment report generated with all sections complete
- User confirms or overrides stage determination
- Gaps documented for potential Advance operation

---

## Error Handling

| Error | Recovery |
|-------|----------|
| No artifacts found | Ask user for project location |
| Score on boundary | Present both stages, let user choose |
| Gate validation fails | Show violations, suggest remediation |
| Low confidence (<70%) | Flag to user, request additional context |

---

## Next Phase

After Assess completes, user can:
- **Generate**: Create stage-aware roadmap -> [phase-2-generate.md](phase-2-generate.md)
- **Advance**: Plan transition to next stage -> [phase-3-advance.md](phase-3-advance.md)
