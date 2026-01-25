# Architecture Review Agent Integration Guide

## Overview

This guide provides detailed integration specifications for the Architecture Review Agent within the regenerative SDLC orchestration system, including workflow coordination, parallel execution protocols, and human collaboration patterns.

## Workflow Integration

### Position in SDLC Workflow

```
SPEC.md → /plan (planner-agent) → Multiple PLAN.md files → **Architecture Review Agent** (parallel with Technical PM) → Validated PLAN.md files → /tasks
```

### Integration Points

#### 1. Pre-Review Trigger

**Orchestrator Role**: Main orchestrator agent detects completion of planning phase

```python
# Orchestrator integration pattern
if planner_result["status"] == "SUCCESS":
    # Trigger parallel execution
    arch_review_task = {
        "task_id": f"arch-review-{timestamp}",
        "operation_type": "architecture_review",
        "review_scope": {
            "specification_file": planner_result["source_spec"],
            "plan_files": planner_result["generated_plans"],
            "maturity_stage": project_context["maturity_stage"]
        }
    }

    # Launch architecture review in parallel with technical PM
    arch_review_future = launch_architecture_review(arch_review_task)
    tech_pm_future = launch_technical_pm(tech_pm_task)

    # Wait for both to complete
    arch_results, pm_results = await gather(arch_review_future, tech_pm_future)
```

#### 2. Parallel Execution Coordination

**Architecture Review Focus**: Technical excellence, quality gates, risk assessment
**Technical PM Focus**: Project execution, resource planning, timeline coordination

**Shared Context Exchange**:

```json
{
  "shared_assessment": {
    "integration_complexity": "moderate",
    "implementation_risk": "low",
    "resource_requirements": "standard_team",
    "timeline_impact": "none"
  }
}
```

#### 3. Post-Review Integration

**Quality Gate Decision**:

```python
def evaluate_quality_gate(arch_review, pm_review):
    """Determine if plans can proceed to task generation."""

    # Architecture quality gate
    arch_approved = (
        arch_review["overall_assessment"]["grade"] in ["A", "B"] and
        arch_review["overall_assessment"]["approval_status"] != "rejected"
    )

    # Project feasibility gate
    pm_approved = pm_review["feasibility"]["overall"] == "approved"

    # Combined decision
    if arch_approved and pm_approved:
        return "proceed_to_tasks"
    elif arch_review["overall_assessment"]["readiness_level"] == "needs_significant_enhancement":
        return "return_to_planning"
    else:
        return "human_review_required"
```

## Agent Input Specifications

### Standard Architecture Review Input

```json
{
  "task_id": "arch-review-20250120-143022",
  "operation_type": "architecture_review",
  "review_scope": {
    "specification_file": "docs/01-planning/specifications/user-auth/SPEC.md",
    "plan_files": [
      "docs/01-planning/specifications/user-auth/plans/auth-service-plan.md",
      "docs/01-planning/specifications/user-auth/plans/user-mgmt-plan.md"
    ],
    "maturity_stage": "MVP",
    "review_focus": ["architecture_soundness", "implementation_readiness", "production_readiness"]
  },
  "quality_requirements": {
    "minimum_overall_score": 3.5,
    "required_grade": "B",
    "mandatory_criteria": ["architecture_soundness", "implementation_readiness"],
    "critical_risk_tolerance": "low"
  },
  "research_requirements": {
    "context7_research": true,
    "research_topics": ["OAuth2 architecture patterns", "FastAPI authentication"],
    "pattern_validation": ["Clean Architecture", "Hexagonal Architecture"],
    "token_budget": 5000
  }
}
```

### Enhanced Review with Auto-Enhancement

```json
{
  "task_id": "arch-review-enhanced-20250120-143022",
  "operation_type": "architecture_review",
  "review_scope": {
    "specification_file": "docs/01-planning/specifications/payment-processing/SPEC.md",
    "plan_files": ["docs/01-planning/specifications/payment-processing/plans/payment-plan.md"],
    "maturity_stage": "Growth",
    "review_focus": ["production_readiness", "performance_optimization", "risk_mitigation"]
  },
  "enhancement_mode": {
    "auto_enhance": true,
    "enhancement_priority": "high_impact",
    "preserve_structure": true
  },
  "integration_context": {
    "performance_targets": {
      "response_time_slo": "95th percentile < 200ms",
      "throughput_target": "1000 requests/second",
      "availability_target": "99.9%"
    },
    "deployment_constraints": [
      "Must support cloud deployment",
      "PCI DSS compliance required",
      "Multi-region deployment capability"
    ]
  }
}
```

## Agent Output Processing

### Success Output Handling

```python
def process_architecture_review_success(result):
    """Process successful architecture review results."""

    assessment = result["operation_result"]["overall_assessment"]
    recommendations = result["recommendations"]

    # Quality gate decision
    if assessment["approval_status"] == "approved":
        # Proceed to task generation
        return {
            "decision": "proceed",
            "validated_plans": result["operation_result"]["plans_reviewed"],
            "quality_score": assessment["overall_score"],
            "enhancements_applied": result["operation_result"].get("enhancement_results", {})
        }

    elif assessment["approval_status"] == "approved_with_conditions":
        # Human review required for conditions
        return {
            "decision": "human_review",
            "conditions": [r for r in recommendations if r["priority"] in ["critical", "high"]],
            "quality_concerns": [r["risk"] for r in result["operation_result"]["risk_analysis"]["identified_risks"]]
        }

    else:  # rejected
        # Return to planning with specific feedback
        return {
            "decision": "return_to_planning",
            "feedback": [r["description"] for r in recommendations if r["priority"] == "critical"],
            "required_improvements": assessment["readiness_level"]
        }
```

### Error and Clarification Handling

```python
def handle_architecture_review_blocked(result):
    """Handle blocked architecture review scenarios."""

    if result["status"] == "NEEDS_CLARIFICATION":
        # Route clarification requests appropriately
        missing_info = result["missing"]

        if "specification details" in str(missing_info):
            return {
                "action": "request_spec_enhancement",
                "specific_requests": result["proposed_next_steps"]
            }
        elif "plan architectural detail" in str(missing_info):
            return {
                "action": "request_plan_enhancement",
                "enhancement_requests": result["reasons"]
            }
        else:
            return {
                "action": "human_escalation",
                "escalation_reason": "Unknown information requirements"
            }

    elif result["status"] == "ERROR":
        # Handle different error scenarios
        error_context = result.get("error_context", {})

        if error_context.get("operation_phase") == "research":
            return {
                "action": "retry_with_fallback",
                "fallback_mode": "web_search_only"
            }
        else:
            return {
                "action": "error_escalation",
                "error_details": result["message"]
            }
```

## Human Collaboration Protocols

### Review Presentation Format

When presenting architecture review results to humans:

```markdown
# Architecture Review Results

## Overall Assessment

- **Quality Score**: 4.2/5.0 (Grade: B)
- **Readiness Level**: Implementation Ready with Improvements
- **Approval Status**: Approved with Conditions

## Critical Findings

### High Priority Issues (2)

1. **Database Scaling Strategy Missing**
   - Risk: Performance bottleneck under load
   - Recommendation: Add read replicas and caching layer
   - Implementation Effort: Medium

2. **Authentication Integration Unclear**
   - Risk: Security vulnerability in session management
   - Recommendation: Define explicit OAuth2 flow with PKCE
   - Implementation Effort: Low

### Research-Backed Recommendations (5)

- Clean Architecture pattern validation: ✅ Compliant
- Performance optimization patterns: ⚠️ Needs improvement
- Security compliance: ✅ Meets standards

## Next Actions Required

1. **Before Implementation**: Address database scaling strategy
2. **During Implementation**: Monitor authentication integration points
3. **Post Implementation**: Validate performance SLOs

## Human Decision Points

- **Accept recommendations and proceed**: Quality gate passed with noted improvements
- **Request additional review**: If concerns about specific recommendations
- **Return to planning**: Only if fundamental architectural changes needed
```

### Human Feedback Integration

```python
def integrate_human_feedback(review_result, human_feedback):
    """Integrate human feedback into architecture review process."""

    feedback_items = human_feedback["feedback_items"]

    for item in feedback_items:
        if item["type"] == "recommendation_modification":
            # Update specific recommendation
            rec_id = item["recommendation_id"]
            modification = item["modification"]

            # Apply modification to recommendation
            update_recommendation(review_result, rec_id, modification)

        elif item["type"] == "risk_acceptance":
            # Mark risk as accepted with rationale
            risk_id = item["risk_id"]
            acceptance_rationale = item["rationale"]

            # Update risk status
            mark_risk_accepted(review_result, risk_id, acceptance_rationale)

        elif item["type"] == "additional_requirement":
            # Add new requirement for consideration
            new_requirement = item["requirement"]

            # Schedule follow-up review
            schedule_follow_up_review(new_requirement)

    # Return updated decision
    return evaluate_updated_quality_gate(review_result)
```

## Performance Optimization

### Parallel Processing Patterns

```python
async def parallel_quality_assessment(plans):
    """Assess multiple plans in parallel for efficiency."""

    # Create assessment tasks
    assessment_tasks = []
    for plan in plans:
        task = assess_individual_plan(plan)
        assessment_tasks.append(task)

    # Execute in parallel
    individual_assessments = await gather(*assessment_tasks)

    # Perform integration assessment
    integration_assessment = await assess_plan_integration(plans, individual_assessments)

    return combine_assessments(individual_assessments, integration_assessment)

async def optimized_research_workflow(research_topics):
    """Optimize Context7 research with batching and caching."""

    # Batch similar queries
    batched_queries = batch_research_topics(research_topics)

    # Execute with token optimization
    research_results = []
    for batch in batched_queries:
        result = await execute_research_batch(batch, token_budget=5000)
        research_results.extend(result)

    return consolidate_research_findings(research_results)
```

### Caching Strategy

```python
class ArchitectureReviewCache:
    """Cache pattern validation and research results."""

    def __init__(self):
        self.pattern_cache = {}
        self.research_cache = {}
        self.ttl = 3600  # 1 hour cache

    def get_pattern_validation(self, pattern_key):
        """Get cached pattern validation result."""
        if pattern_key in self.pattern_cache:
            cached_result, timestamp = self.pattern_cache[pattern_key]
            if time.time() - timestamp < self.ttl:
                return cached_result
        return None

    def cache_pattern_validation(self, pattern_key, result):
        """Cache pattern validation result."""
        self.pattern_cache[pattern_key] = (result, time.time())

    def get_research_result(self, research_query):
        """Get cached research result."""
        query_hash = hash(research_query)
        if query_hash in self.research_cache:
            cached_result, timestamp = self.research_cache[query_hash]
            if time.time() - timestamp < self.ttl:
                return cached_result
        return None
```

## Error Handling and Recovery

### Research Service Failures

```python
def handle_research_failures(research_requirements):
    """Handle Context7 or research service failures gracefully."""

    try:
        # Primary: Context7 research
        context7_results = perform_context7_research(research_requirements)
        return context7_results

    except Context7ServiceError:
        # Fallback: WebSearch with targeted queries
        web_search_queries = convert_to_web_queries(research_requirements)
        web_results = perform_web_research(web_search_queries)

        # Mark as fallback research
        web_results["research_method"] = "web_search_fallback"
        web_results["confidence_adjustment"] = -0.1  # Slightly lower confidence

        return web_results

    except Exception as e:
        # Minimal research mode - use built-in patterns only
        return {
            "research_method": "builtin_patterns_only",
            "confidence_adjustment": -0.2,
            "patterns_validated": get_builtin_patterns(),
            "research_note": f"External research unavailable: {str(e)}"
        }
```

### Plan File Processing Errors

```python
def robust_plan_processing(plan_files):
    """Process plan files with error recovery."""

    successfully_processed = []
    failed_files = []

    for plan_file in plan_files:
        try:
            plan_content = load_and_parse_plan(plan_file)
            validate_plan_structure(plan_content)
            successfully_processed.append((plan_file, plan_content))

        except FileNotFoundError:
            failed_files.append({
                "file": plan_file,
                "error": "File not found",
                "recovery": "Request plan regeneration"
            })

        except PlanStructureError as e:
            failed_files.append({
                "file": plan_file,
                "error": f"Invalid structure: {str(e)}",
                "recovery": "Request plan format correction"
            })

    if not successfully_processed:
        raise ReviewBlockedError("No valid plan files available for review")

    if failed_files:
        # Log warnings but continue with available plans
        log_plan_processing_warnings(failed_files)

    return successfully_processed, failed_files
```

## Monitoring and Observability

### Review Performance Metrics

```python
class ArchitectureReviewMetrics:
    """Collect and report architecture review performance metrics."""

    def __init__(self):
        self.review_times = []
        self.quality_scores = []
        self.recommendation_counts = []
        self.research_times = []

    def record_review_completion(self, review_time, quality_score, rec_count):
        """Record completion metrics."""
        self.review_times.append(review_time)
        self.quality_scores.append(quality_score)
        self.recommendation_counts.append(rec_count)

    def record_research_performance(self, research_time, success_rate):
        """Record research performance."""
        self.research_times.append(research_time)

    def get_slo_compliance(self):
        """Calculate SLO compliance rates."""
        return {
            "review_time_slo": len([t for t in self.review_times if t <= 600]) / len(self.review_times),  # 10 minutes
            "avg_quality_score": sum(self.quality_scores) / len(self.quality_scores),
            "avg_research_time": sum(self.research_times) / len(self.research_times)
        }
```

---

## Examples

**For detailed usage scenarios and complete workflow examples**, see:

- **`.claude/docs/04-examples/architecture-examples.md`** - 5 complete scenarios including:
  - Standard feature architecture review with quality scoring
  - Critical architecture review with auto-enhancement
  - Multi-plan integration assessment
  - Blocked review handling (insufficient detail)
  - Quality gate failure (return to planning)

**These examples demonstrate input/output contracts, orchestrator integration patterns, and quality gate decision logic in production contexts.**

---

**This integration guide ensures seamless coordination of the Architecture Review Agent within the regenerative SDLC workflow, providing clear protocols for orchestrator integration, human collaboration, and performance optimization.**
