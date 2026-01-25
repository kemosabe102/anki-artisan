# Review Aggregation Logic

**Central reference for parsing and aggregating multi-agent review findings.**

**Last Updated**: 2025-10-06
**Applies To**: Orchestrators, /spec command, /plan command, review workflows

---

## Overview

This document establishes the **mandatory review aggregation protocol** for combining findings from multiple review agents (planning, planning, architecture) into actionable decisions. Enables automated quality gates and human-readable summaries.

### When to Use This Framework

**✅ Use review-aggregation-logic.md When**:

- Findings have **machine-readable JSON schemas** (planning, planning, architecture)
- Formal quality gate decisions required (SUCCESS/FAILURE status)
- Structured validation checklists with scoring
- Review lifecycle workflows (spec → plan → tasks)

**❌ Use synthesis-and-recommendation-framework.md Instead When**:

- Findings are **general multi-agent outputs** without formal schemas (researcher-\*, development, debugger)
- Multiple overlapping solutions need consolidation (similarity >0.7)
- Trade-off analysis and recommendation scoring needed
- Research or exploratory workflows

**Decision Rule**:

```
Multiple agent findings received:
  ↓
Do findings have machine-readable JSON schemas?
  ├─ YES → Use review-aggregation-logic.md (this document)
  └─ NO → Use synthesis-and-recommendation-framework.md
```

## Review Agent Ecosystem

### Agent Roles & Review Focus

| Agent                   | Review Type      | Focus Area                                          | Output Location                                                        |
| ----------------------- | ---------------- | --------------------------------------------------- | ---------------------------------------------------------------------- |
| **planning**       | Quality Review   | Requirements clarity, testability, WHAT/WHY vs HOW  | `docs/01-planning/specifications/XXX/review/spec-review-report.md`     |
| **planning**        | Business Review  | Pain point alignment, ROI, business value           | `docs/01-planning/specifications/XXX/review/business-review-report.md` |
| **architecture** | Technical Review | Architecture feasibility, tech choices, scalability | `docs/02-plans/XXX/review/technical-review-report.md`                  |

### Review Lifecycle

```yaml
workflow:
  spec_phase:
    - /spec command creates SPEC.md
    - planning validates quality
    - planning validates business alignment
    - orchestrator aggregates → decision: proceed to /plan or fix issues

  plan_phase:
    - planning creates PLAN.md
    - architecture validates technical feasibility
    - orchestrator aggregates → decision: proceed to /tasks or refine plan
```

## Machine-Readable Format

### JSON Structure Location

All review reports MUST include a **Machine-Readable Review Data** section near the end of the markdown file, formatted as:

````markdown
## Machine-Readable Review Data

**Purpose**: Structured output for orchestrator parsing and review aggregation

```json
{
  "status": "SUCCESS|FAILURE",
  "agent": "planning|planning|architecture",
  "task_id": "review-[timestamp]",
  "operation_type": "spec_quality_review|business_review|technical_review",
  "summary": "Brief summary",
  "validation_checklist": { ... },
  "success_evidence": { ... },
  "confidence": 0.0-1.0,
  "severity": "Minor|Major|Critical",
  "execution_timestamp": "ISO_8601_UTC"
}
```
````

````

### Parsing Strategy

**Step 1: Extract JSON Block**
```python
import re
import json

def extract_review_data(markdown_content: str) -> dict:
    """Extract machine-readable JSON from review report."""
    # Find the JSON code block after "Machine-Readable Review Data"
    pattern = r'## Machine-Readable Review Data.*?```json\n(.*?)\n```'
    match = re.search(pattern, markdown_content, re.DOTALL)

    if not match:
        raise ValueError("No machine-readable section found")

    json_str = match.group(1)
    return json.loads(json_str)
````

**Step 2: Validate Schema**

```python
def validate_review_schema(data: dict) -> bool:
    """Validate required fields present."""
    required_fields = ["status", "agent", "operation_type", "summary", "success_evidence"]
    return all(field in data for field in required_fields)
```

## Aggregation Algorithms

### 1. Quality Gate Algorithm (Boolean Decision)

**Purpose**: Determine if reviews pass threshold for proceeding to next phase

**Decision Logic**:

```python
def should_proceed_to_next_phase(reviews: list[dict]) -> tuple[bool, str]:
    """
    Aggregate multiple review findings into proceed/block decision.

    Returns:
        (should_proceed, rationale)
    """
    # Rule 1: All reviews must have SUCCESS status
    all_success = all(r["status"] == "SUCCESS" for r in reviews)
    if not all_success:
        failed_agents = [r["agent"] for r in reviews if r["status"] == "FAILURE"]
        return False, f"Review failures: {', '.join(failed_agents)}"

    # Rule 2: Check severity of issues found
    critical_issues = [r for r in reviews if r.get("severity") == "Critical"]
    if critical_issues:
        agents = [r["agent"] for r in critical_issues]
        return False, f"Critical issues from: {', '.join(agents)}"

    # Rule 3: Check confidence levels (all must be > 0.7)
    low_confidence = [r for r in reviews if r.get("confidence", 1.0) < 0.7]
    if low_confidence:
        agents = [r["agent"] for r in low_confidence]
        return False, f"Low confidence from: {', '.join(agents)}"

    # Rule 4: Check quality thresholds (for planning)
    for review in reviews:
        if review["agent"] == "planning":
            qa = review["success_evidence"]["quality_assessment"]
            if qa["completeness_score"] < 0.7:
                return False, "Completeness score below threshold (0.7)"
            if qa["testability_score"] < 0.7:
                return False, "Testability score below threshold (0.7)"

    # All checks passed
    return True, "All reviews passed quality gates"
```

**Threshold Configuration**:

```yaml
quality_gates:
  completeness_score: 0.7
  testability_score: 0.7
  clarity_score: 0.6
  confidence_level: 0.7
  max_critical_issues: 0
  max_major_issues: 3
```

### 2. Recommendation Aggregation (Priority Sorting)

**Purpose**: Combine recommendations from multiple reviewers into prioritized action list

**Aggregation Logic**:

```python
def aggregate_recommendations(reviews: list[dict]) -> list[dict]:
    """
    Merge and prioritize recommendations from multiple reviewers.

    Returns sorted list of recommendations with agent attribution.
    """
    all_recommendations = []

    for review in reviews:
        findings = review["success_evidence"].get("review_findings", {})
        recommendations = findings.get("recommendations", [])

        for rec in recommendations:
            all_recommendations.append({
                "priority": rec["priority"],
                "category": rec["category"],
                "finding": rec["finding"],
                "recommendation": rec["recommendation"],
                "location": rec["location"],
                "reviewer": review["agent"],  # Attribution
                "severity": review.get("severity", "Minor")
            })

    # Priority order: Critical severity first, then High/Medium/Low priority
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    severity_order = {"Critical": 0, "Major": 1, "Minor": 2}

    return sorted(all_recommendations, key=lambda x: (
        severity_order.get(x["severity"], 3),
        priority_order.get(x["priority"], 4)
    ))
```

### 3. Quality Score Aggregation (Weighted Average)

**Purpose**: Combine quality scores from planning with business/technical assessments

**Weighted Scoring**:

```python
def aggregate_quality_scores(reviews: list[dict]) -> dict:
    """
    Calculate weighted aggregate quality scores.

    Returns overall quality assessment with component breakdown.
    """
    # Extract planning scores (if present)
    spec_review = next((r for r in reviews if r["agent"] == "planning"), None)
    if not spec_review:
        return {"error": "No planning found"}

    qa = spec_review["success_evidence"]["quality_assessment"]

    # Base scores from planning (70% weight)
    base_score = (
        qa["completeness_score"] * 0.3 +
        qa["testability_score"] * 0.3 +
        qa["clarity_score"] * 0.2 +
        qa["pain_point_alignment"] * 0.2
    ) * 0.7

    # Business alignment from planning (15% weight)
    pm_review = next((r for r in reviews if r["agent"] == "planning"), None)
    business_score = 0.0
    if pm_review:
        validation = pm_review["success_evidence"].get("validation_results", {})
        business_score = (
            float(validation.get("pain_point_aligned", False)) * 0.15
        )

    # Technical feasibility from architecture (15% weight)
    arch_review = next((r for r in reviews if r["agent"] == "architecture"), None)
    technical_score = 0.0
    if arch_review:
        validation = arch_review["success_evidence"].get("validation_results", {})
        technical_score = (
            float(validation.get("architecture_feasible", False)) * 0.15
        )

    overall_score = base_score + business_score + technical_score

    return {
        "overall_score": round(overall_score, 2),
        "grade": _score_to_grade(overall_score),
        "components": {
            "spec_quality": round(base_score / 0.7, 2),
            "business_alignment": round(business_score / 0.15, 2) if business_score > 0 else None,
            "technical_feasibility": round(technical_score / 0.15, 2) if technical_score > 0 else None
        }
    }

def _score_to_grade(score: float) -> str:
    """Convert numeric score to letter grade."""
    if score >= 0.9: return "A"
    if score >= 0.8: return "B"
    if score >= 0.7: return "C"
    if score >= 0.6: return "D"
    return "F"
```

## Conflict Resolution

### Scenario 1: Reviewers Disagree on Readiness

**Example**: planning says "READY", planning says "CONDITIONAL"

**Resolution Strategy**:

```python
def resolve_readiness_conflict(reviews: list[dict]) -> str:
    """
    Conservative conflict resolution: require unanimous approval.

    Returns: "READY" | "CONDITIONAL" | "NOT READY"
    """
    statuses = []
    for review in reviews:
        # Extract verdict from human-readable section or validation_results
        validation = review["success_evidence"].get("validation_results", {})
        if validation.get("quality_threshold_met", False):
            statuses.append("READY")
        elif review.get("severity") == "Critical":
            statuses.append("NOT READY")
        else:
            statuses.append("CONDITIONAL")

    # Conservative approach: worst case wins
    if "NOT READY" in statuses:
        return "NOT READY"
    if "CONDITIONAL" in statuses:
        return "CONDITIONAL"
    return "READY"
```

**Decision Tree**:

```yaml
conflict_resolution:
  all_ready: 'Proceed to next phase'
  any_not_ready: 'Block and require fixes'
  any_conditional: 'Proceed with caution, address critical issues'
  mixed_ready_conditional: 'Treat as CONDITIONAL'
```

### Scenario 2: Conflicting Recommendations

**Example**: planning says "Add ROI section", architecture says "ROI not needed for architecture"

**Resolution Strategy**:

```python
def deduplicate_recommendations(recommendations: list[dict]) -> list[dict]:
    """
    Remove contradictory or redundant recommendations.

    Strategy:
    1. Group by location (same section/requirement)
    2. Prioritize by reviewer expertise
    3. Keep highest priority if conflict
    """
    grouped = {}
    for rec in recommendations:
        key = rec["location"]
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(rec)

    # Reviewer expertise priority (for conflicts)
    expertise_priority = {
        "planning": {"requirements", "testability", "clarity", "structure"},
        "planning": {"business", "roi", "pain_points"},
        "architecture": {"architecture", "scalability", "performance", "security"}
    }

    deduplicated = []
    for location, recs in grouped.items():
        if len(recs) == 1:
            deduplicated.append(recs[0])
        else:
            # Pick recommendation from most relevant expert
            best_rec = max(recs, key=lambda r: (
                r["category"] in expertise_priority.get(r["reviewer"], set()),
                {"High": 3, "Medium": 2, "Low": 1}.get(r["priority"], 0)
            ))
            deduplicated.append(best_rec)

    return deduplicated
```

## Orchestrator Integration

### Workflow Integration Points

**1. /spec Command (Post-Enhancement)**

```python
def spec_review_workflow(spec_path: str) -> dict:
    """
    Execute multi-agent spec review and aggregate findings.
    """
    # Step 1: Launch review agents in parallel
    reviews = parallel_execute([
        Task("planning", f"Review {spec_path}"),
        Task("planning", f"Review {spec_path}")
    ])

    # Step 2: Parse machine-readable sections
    parsed_reviews = [extract_review_data(r.output) for r in reviews]

    # Step 3: Aggregate findings
    proceed, rationale = should_proceed_to_next_phase(parsed_reviews)
    recommendations = aggregate_recommendations(parsed_reviews)
    quality_scores = aggregate_quality_scores(parsed_reviews)

    # Step 4: Generate summary report
    return {
        "proceed_to_plan": proceed,
        "rationale": rationale,
        "quality_scores": quality_scores,
        "recommendations": recommendations[:10],  # Top 10
        "review_paths": [r["agent"] for r in parsed_reviews]
    }
```

**2. /plan Command (Post-Planning)**

```python
def plan_review_workflow(plan_path: str) -> dict:
    """
    Execute architecture review and validate technical feasibility.
    """
    # Step 1: Launch architecture agent
    review = execute_agent("architecture", f"Review {plan_path}")

    # Step 2: Parse machine-readable section
    parsed_review = extract_review_data(review.output)

    # Step 3: Check technical feasibility
    validation = parsed_review["success_evidence"]["validation_results"]
    proceed = validation.get("architecture_feasible", False)

    return {
        "proceed_to_tasks": proceed,
        "rationale": parsed_review["summary"],
        "recommendations": parsed_review["success_evidence"]["review_findings"]["recommendations"]
    }
```

### Human-Readable Summary Generation

**Purpose**: Convert aggregated review data into user-friendly summary

**Template**:

```python
def generate_summary_report(aggregation_result: dict) -> str:
    """
    Generate human-readable summary from aggregated review findings.
    """
    proceed = aggregation_result["proceed_to_plan"]
    rationale = aggregation_result["rationale"]
    quality = aggregation_result["quality_scores"]
    recommendations = aggregation_result["recommendations"]

    summary = f"""
# Review Aggregation Summary

## Overall Assessment
- **Decision**: {'✅ PROCEED' if proceed else '❌ BLOCKED'}
- **Rationale**: {rationale}
- **Quality Score**: {quality['overall_score']} ({quality['grade']})

## Quality Breakdown
- **Spec Quality**: {quality['components']['spec_quality']}
- **Business Alignment**: {quality['components']['business_alignment'] or 'N/A'}
- **Technical Feasibility**: {quality['components']['technical_feasibility'] or 'N/A'}

## Top Recommendations
"""

    for i, rec in enumerate(recommendations[:5], 1):
        summary += f"""
{i}. **[{rec['priority']}]** ({rec['reviewer']}) - {rec['category']}
   - **Finding**: {rec['finding']}
   - **Recommendation**: {rec['recommendation']}
   - **Location**: {rec['location']}
"""

    return summary
```

## Validation Checklist

**Before aggregating reviews**:

- [ ] All expected review agents have completed (planning mandatory)
- [ ] Machine-readable JSON sections parsed successfully
- [ ] Schema validation passed for all review outputs
- [ ] No JSON parsing errors or malformed data

**After aggregation**:

- [ ] Quality gates evaluated (proceed/block decision made)
- [ ] Recommendations deduplicated and prioritized
- [ ] Conflicts resolved using documented strategy
- [ ] Summary report generated for user
- [ ] Aggregation results logged for audit trail

## Best Practices

1. **Always parse machine-readable section** - Don't rely on human-readable text alone
2. **Validate JSON schema** - Ensure all required fields present before aggregation
3. **Use conservative conflict resolution** - Block on critical issues, warn on major issues
4. **Attribute recommendations to reviewers** - Enable users to understand source of feedback
5. **Log aggregation decisions** - Create audit trail for quality gate decisions
6. **Provide actionable next steps** - Always include "what to do next" in summary

## Error Handling

### Missing Machine-Readable Section

```python
def handle_missing_section(review_path: str) -> dict:
    """
    Graceful degradation when review lacks machine-readable data.
    """
    return {
        "status": "FAILURE",
        "agent": "unknown",
        "error": "Review report missing machine-readable section",
        "recovery": "Re-run review agent or parse human-readable content manually"
    }
```

### Malformed JSON

```python
def handle_json_error(review_path: str, error: str) -> dict:
    """
    Handle JSON parsing failures gracefully.
    """
    return {
        "status": "FAILURE",
        "agent": "unknown",
        "error": f"JSON parsing failed: {error}",
        "recovery": "Check review report for syntax errors in JSON block"
    }
```

---

**References**:

- Review Template: `.claude/templates/spec-review-template.md`
- Agent Schemas: `.claude/docs/schemas/*-reviewer.schema.json`
- Orchestrator Workflow: `.claude/docs/orchestrator-workflow.md`

**Questions or Issues**:
If aggregation logic is insufficient for a specific workflow, document the gap and propose an extension in workflow-specific documentation.
