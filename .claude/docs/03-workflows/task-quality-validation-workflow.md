---
title: "Task Quality Validation Workflow"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Task Quality Validation Workflow

**Purpose**: Comprehensive multi-agent validation with 3 core agents (always) + 0-2 dynamic agents (confidence-based) for generated task lists.

**Context**: Invoked by `/tasks` slash command in Step 6 after successful task generation.

**Timing**: ~2-5 minutes (parallel execution, 3-5 agents)

---

## Overview

**Validation Strategy**: Multi-Agent Confidence-Based Review

**Core Agents (ALWAYS run, 75% weight)**:

- **planning** (25%): Business alignment, value delivery, resource optimization
- **architecture** (25%): Technical completeness, production readiness, risk mitigation
- **tech-debt-investigator** (25%): Technical debt detection, duplicates, cleanup, coupling

**Dynamic Agents (0-2 agents selected, 25% weight split)**:

- **feature-analyzer**: Integration analysis (multi-component features)
- **test-runner**: Test coverage and quality (test-heavy features)
- **security-reviewer**: Security analysis (auth/authz/api features)

**Selection Criteria**: Dynamic agents included if confidence >0.8 based on feature signals

**Output**: Weighted validation score, aggregated findings, recommendation status, agent selection rationale

---

## Step 1: Launch Core + Dynamic Review Agents in Parallel

### Agent 1: planning (Business Alignment Review)

**Prompt Template**:

```json
{
  "task_id": "task-validation-tpm-001",
  "execution_timestamp": "${execution_timestamp}",
  "objective": "Evaluate business alignment, value delivery, and resource optimization of generated tasks",
  "input": {
    "review_type": "Task Quality Validation - Business Alignment",
    "feature_number": "${feature_synthesis.feature_number}",
    "feature_name": "${feature_synthesis.feature_name}",
    "feature_description": "${feature_synthesis.feature_description}",
    "task_files": [
      "tasks/phase-0/tasks.md",
      "tasks/phase-1/tasks.md",
      "tasks/phase-2/tasks.md"
    ],
    "context_files": [
      "${FEATURE_DIR}/README.md",
      "${FEATURE_DIR}/SPEC.md",
      "${discovered plan files}"
    ]
  },
  "instructions": "
**Review Type**: Task Quality Validation - Business Alignment

**Feature**: ${feature_synthesis.feature_number}-${feature_synthesis.feature_name}

**Objective**: Evaluate business alignment, value delivery, and resource optimization of generated tasks

**Task Files to Review**:
${FOR EACH success in success_results:}
- ${success.output_dir}/tasks.md (${success.tasks_created} tasks, ${success.sprint_points} points)
${END FOR}

**Context Files**:
${FOR EACH context_file in discovered_context_files:}
- ${context_file}
${END FOR}

**Validation Criteria**:
1. **Business Value Alignment** (35%)
   - Do tasks deliver meaningful business value?
   - Are high-impact features prioritized correctly?
   - Is scope appropriate for business goals?

2. **Resource Optimization** (25%)
   - Are tasks sized appropriately (not too large/small)?
   - Is sprint point distribution balanced?
   - Are there opportunities for parallelization?

3. **Stakeholder Communication** (20%)
   - Are review checkpoints defined clearly?
   - Is progress tracking feasible?
   - Are acceptance criteria business-understandable?

4. **Scope Management** (20%)
   - Are boundaries clearly defined?
   - Is scope creep prevented?
   - Are dependencies explicit?

**Output Format**:
Return a business review report with:
- Overall score (0.0-5.0)
- Critical issues (must-fix before implementation)
- High-priority improvements (should-fix)
- Medium/low recommendations (nice-to-have)
- Confidence score (0.0-1.0)
- Time impact estimates (hours saved/added)
"
}
```

**Template Expansion Note**:
The orchestrator expands `success_results` to a concrete array of file paths before invoking agents. Agents receive fully expanded JSON with no template variables.

**Example**:

- Input: success_results = [{output_dir: "tasks/phase-0"}, {output_dir: "tasks/phase-1"}]
- Expanded: task_files = ["tasks/phase-0/tasks.md", "tasks/phase-1/tasks.md"]

### Agent 2: architecture (Technical Validation)

**Prompt Template**:

```json
{
  "task_id": "task-validation-arch-001",
  "execution_timestamp": "${execution_timestamp}",
  "objective": "Evaluate technical soundness, production readiness, implementation quality",
  "input": {
    "review_type": "Task Quality Validation - Technical Validation",
    "feature_number": "${feature_synthesis.feature_number}",
    "feature_name": "${feature_synthesis.feature_name}",
    "task_files": [
      "tasks/phase-0/tasks.md",
      "tasks/phase-1/tasks.md",
      "tasks/phase-2/tasks.md"
    ],
    "context_files": [
      "${FEATURE_DIR}/README.md",
      "${FEATURE_DIR}/SPEC.md",
      "${discovered plan files}"
    ]
  },
  "instructions": "
**Review Type**: Task Quality Validation - Technical Validation

**Feature**: ${feature_synthesis.feature_number}-${feature_synthesis.feature_name}

**Objective**: Evaluate technical soundness, production readiness, implementation quality

**Task Files to Review**:
${FOR EACH success in success_results:}
- ${success.output_dir}/tasks.md (${success.tasks_created} tasks)
${END FOR}

**Context Files**:
${FOR EACH context_file in discovered_context_files:}
- ${context_file}
${END FOR}

**Validation Criteria**:
1. **Technical Completeness** (35%)
   - Are all technical requirements covered?
   - Are edge cases and error handling addressed?
   - Are performance considerations included?

2. **Implementation Quality** (25%)
   - Are tasks technically sound?
   - Are best practices followed?
   - Is code quality maintained?

3. **Production Readiness** (20%)
   - Are monitoring/observability tasks included?
   - Is security addressed?
   - Are deployment steps defined?

4. **Risk Mitigation** (20%)
   - Are technical risks identified?
   - Are mitigation strategies defined?
   - Are rollback plans included?

**Output Format**:
Return a technical validation report with:
- Overall score (0.0-5.0)
- Critical issues (must-fix before implementation)
- High-priority improvements (should-fix)
- Medium/low recommendations (nice-to-have)
- Confidence score (0.0-1.0)
- Time impact estimates (hours saved/added)
"
}
```

**Template Expansion**: Same as Agent 1 - orchestrator expands template variables before agent invocation.

### Agent 3: tech-debt-investigator (Technical Debt Detection) [CORE]

**Prompt Template**:

```json
{
  "task_id": "task-validation-tdi-001",
  "execution_timestamp": "${execution_timestamp}",
  "objective": "Detect technical debt, duplicates, cleanup gaps, and coupling issues in generated tasks",
  "input": {
    "review_type": "Task Quality Validation - Technical Debt Detection",
    "feature_number": "${feature_synthesis.feature_number}",
    "feature_name": "${feature_synthesis.feature_name}",
    "task_files": [
      "tasks/phase-0/tasks.md",
      "tasks/phase-1/tasks.md",
      "tasks/phase-2/tasks.md"
    ],
    "context_files": [
      "${FEATURE_DIR}/README.md",
      "${FEATURE_DIR}/SPEC.md",
      "${discovered plan files}"
    ]
  },
  "instructions": "
**Review Type**: Task Quality Validation - Technical Debt Detection

**Feature**: ${feature_synthesis.feature_number}-${feature_synthesis.feature_name}

**Objective**: Identify potential technical debt, duplicate functionality, cleanup gaps, and coupling issues

**Task Files to Review**:
${FOR EACH success in success_results:}
- ${success.output_dir}/tasks.md (${success.tasks_created} tasks, ${success.sprint_points} points)
${END FOR}

**Context Files**:
${FOR EACH context_file in discovered_context_files:}
- ${context_file}
${END FOR}

**Analysis Areas**:
1. **Duplicate Functionality Detection** (30%)
   - Are tasks introducing duplicate functionality?
   - Is existing functionality being reimplemented?
   - Can existing components be reused instead?

2. **Cleanup & Integration Completeness** (25%)
   - Are cleanup tasks included (temp files, deprecated code, old patterns)?
   - Is integration complete (no half-finished connections)?
   - Are migration paths complete (old → new transitions)?

3. **Coupling & Architectural Debt** (25%)
   - Are tasks introducing tight coupling between components?
   - Is separation of concerns maintained?
   - Are abstraction boundaries respected?

4. **Code Quality & Maintainability** (20%)
   - Are technical debt items addressed (not deferred indefinitely)?
   - Is code quality improvement planned alongside features?
   - Are refactoring opportunities identified?

**Output Format**:
Return a technical debt analysis report with:
- Overall score (0.0-5.0)
- Critical issues (must-fix before implementation - debt that will compound)
- High-priority improvements (should-fix - prevents future debt)
- Medium/low recommendations (nice-to-have - quality improvements)
- Confidence score (0.0-1.0)
- Time impact estimates (hours saved/added by addressing debt now vs later)
"
}
```

**Template Expansion Note**: Same as Agent 1 and 2.

**Why Always Core**: Even simple CRUD can introduce duplicates, skip cleanup, or create coupling. Tech debt detection is valuable for ALL changes.

---

### Agent 4 (Dynamic): feature-analyzer (Integration Analysis) [IF CONFIDENCE >0.8]

**Selection Criteria**: Multi-component features with dependencies or integration points

**Confidence Calculation**:

```python
domain_fit = 0.3 + (component_count * 0.15) + (has_dependencies * 0.35) + (integration_points * 0.2)
confidence = domain_fit * 0.6 + 0.3 * 0.4  # Unique value = 0.3 (moderate, overlaps with tech-debt)
# Include if confidence >0.8 (typically 2+ components OR dependencies + integration points)
```

**Prompt Template**:

```json
{
  "task_id": "task-validation-fa-001",
  "execution_timestamp": "${execution_timestamp}",
  "objective": "Analyze cross-task dependencies, overlaps, conflicts, sequencing optimization",
  "input": {
    "review_type": "Task Quality Validation - Integration & Overlap Analysis",
    "feature_number": "${feature_synthesis.feature_number}",
    "feature_name": "${feature_synthesis.feature_name}",
    "task_files": [
      "tasks/phase-0/tasks.md",
      "tasks/phase-1/tasks.md",
      "tasks/phase-2/tasks.md"
    ],
    "context_files": [
      "${FEATURE_DIR}/README.md",
      "${FEATURE_DIR}/SPEC.md",
      "${discovered plan files}"
    ]
  },
  "instructions": "
**Review Type**: Task Quality Validation - Integration & Overlap Analysis

**Feature**: ${feature_synthesis.feature_number}-${feature_synthesis.feature_name}

**Objective**: Analyze cross-task dependencies, overlaps, conflicts, sequencing optimization

**Task Files to Review**:
${FOR EACH success in success_results:}
- ${success.output_dir}/tasks.md (${success.tasks_created} tasks)
${END FOR}

**Context Files**:
${FOR EACH context_file in discovered_context_files:}
- ${context_file}
${END FOR}

**Analysis Areas**:
1. **Dependency Validation** (30%)
   - Are dependencies correctly identified?
   - Is dependency order logical and correct?
   - Are circular dependencies avoided?

2. **Overlap & Duplication Detection** (25%)
   - Are there duplicate tasks?
   - Do tasks overlap in scope?
   - Can tasks be consolidated?

3. **Gap Identification** (25%)
   - Are there missing integration points?
   - Are there gaps in the task flow?
   - Are handoffs between components clear?

4. **Sequencing Optimization** (20%)
   - Can more tasks run in parallel?
   - Is critical path optimized?
   - Are bottlenecks identified?

**Output Format**:
Return an integration analysis report with:
- Overall score (0.0-1.0 for integration health)
- Critical issues (must-fix before implementation)
- High-priority improvements (should-fix)
- Medium/low recommendations (nice-to-have)
- Dependency graph or visualization
- Confidence score (0.0-1.0)
- Time impact estimates (hours saved/added)
"
}
```

**Template Expansion**: Same as Agent 1 and 2.

---

### Agent 5 (Dynamic): test-runner (Test Coverage Analysis) [IF CONFIDENCE >0.8]

**Selection Criteria**: Test-heavy features with high complexity or quality requirements

**Confidence Calculation**:

```python
test_complexity_map = {"high": 0.9, "medium": 0.7, "low": 0.5}
domain_fit = test_complexity_map[test_complexity]
confidence = domain_fit * 0.6 + 0.35 * 0.4  # Unique value = 0.35 (moderate overlap)
# Include if confidence >0.8 (typically "high" test complexity OR "medium" + other signals)
```

**Prompt Focus**: Test coverage completeness, test quality, validation strategies, quality gates

---

### Agent 6 (Dynamic): security-reviewer (Security Analysis) [IF CONFIDENCE >0.8]

**Selection Criteria**: Security-critical features (auth, authz, API operations, data sensitivity)

**Confidence Calculation**:

```python
domain_fit = 1.0 if security_critical else 0.4
confidence = domain_fit * 0.6 + 0.4 * 0.4  # Unique value = 0.4 (high uniqueness)
# Include if confidence >0.8 (security_critical must be True)
```

**Prompt Focus**: Security analysis for auth/authz, input validation, secrets handling, API security

---

### Parallel Execution Pattern

**Launch 3 core + 0-2 dynamic agents in SINGLE MESSAGE**:

```markdown
# Core agents (ALWAYS)

Task(subagent_type='planning', prompt=[agent-1 input JSON])
Task(subagent_type='architecture', prompt=[agent-2 input JSON])
Task(subagent_type='tech-debt-investigator', prompt=[agent-3 input JSON])

# Dynamic agents (IF confidence >0.8)

Task(subagent_type='feature-analyzer', prompt=[agent-4 input JSON]) # If selected
Task(subagent_type='test-runner', prompt=[agent-5 input JSON]) # If selected
```

**Benefits**:

- 3-5 reviews run simultaneously (depending on feature complexity)
- Tailored validation: Simple features get 3 core agents, complex features get up to 5 total
- Results available in ~2-5 minutes total
- Comprehensive validation from all perspectives
- No sequential delay

---

## Step 2: Collect and Synthesize Validation Results

### Result Extraction

```python
# Extract findings from each agent
FOR EACH agent_output in [tpm_result, arch_result, fa_result]:

  IF status == "SUCCESS":
    Extract:
      - overall_score (normalize to 0.0-5.0 for tpm/arch, 0.0-1.0 for fa)
      - critical_issues[] (must-fix)
      - high_priority_improvements[] (should-fix)
      - medium_low_recommendations[] (nice-to-have)
      - confidence (0.0-1.0)
      - time_impact {hours_added, hours_saved, net_hours}

  ELSE IF status == "FAILURE":
    WARN "Validation agent ${agent} failed - proceeding with partial validation"
    LOWER overall_validation_confidence by 33%
```

### Result Synthesis Methodology

**Apply multi-reviewer synthesis logic** from `.claude/docs/guides/review-aggregation-logic.md`:

1. **Extract findings** from each agent (critical/high/medium/low issues)
2. **Aggregate issues** using UNION + promotion rules:
   - Issue flagged by ANY agent as critical → CRITICAL
   - Issue flagged by 2+ agents as high → HIGH
   - Issue flagged by 3 agents as medium → HIGH
3. **Calculate weighted validation scores**:
   - **Core agents (75% weight)**:
     - validation_score_core = (tpm.score × 0.25) + (arch.score × 0.25) + (tech_debt.score × 0.25)
   - **Dynamic agents (25% weight split)**:
     - dynamic_weight = 0.25 / len(dynamic_agents) if dynamic_agents else 0
     - validation_score_dynamic = sum(agent.score \* dynamic_weight for agent in dynamic_agents)
     - Note: feature-analyzer score on 0-1 scale, normalize to 0-5 before weighting
   - **Total**: validation_score = validation_score_core + validation_score_dynamic
4. **Compute time impact metrics**:
   - Aggregate enhancement_effort across all issues
   - Aggregate time_savings across all improvements
   - Calculate net_impact = time_savings - enhancement_effort

**For complete aggregation algorithms**: See review-aggregation-logic.md

### Validation Confidence Calculation

**Calculate aggregate confidence** across all validation agents:

```python
# Core agents (75% weight)
core_confidence = (
    tpm.confidence * 0.25 +
    arch.confidence * 0.25 +
    tech_debt.confidence * 0.25
)

# Dynamic agents (25% weight split)
dynamic_weight = 0.25 / len(dynamic_agents) if dynamic_agents else 0
dynamic_confidence = sum(agent.confidence * dynamic_weight for agent in dynamic_agents)

# Total confidence
validation_confidence = core_confidence + dynamic_confidence
```

**Apply confidence thresholds**:

- validation_confidence ≥ 0.85: HIGH confidence, full trust in validation
- validation_confidence 0.70-0.84: MEDIUM confidence, acceptable validation
- validation_confidence < 0.70: LOW confidence, validation incomplete

**Low Confidence Handling**:

```
IF validation_confidence < 0.70:
  WARN "Validation confidence below threshold - results may be incomplete"
  IF validation_confidence < 0.50:
    recommendation_status = "APPROVED WITH CAVEATS (LOW CONFIDENCE)"
  ELSE:
    ADD caveat to recommendation_status
```

**Partial Agent Failure**:

```python
IF successful_core_agents < 3:
  # Core agents failed - critical validation missing
  core_confidence *= (successful_core_agents / 3.0)
  WARN "Partial core validation only - {failed_core_agents} core agent(s) failed"

IF successful_dynamic_agents < len(expected_dynamic_agents):
  # Dynamic agents failed - reduce dynamic contribution
  dynamic_confidence *= (successful_dynamic_agents / len(expected_dynamic_agents))
  INFO "Partial dynamic validation - proceeding with {successful_dynamic_agents} dynamic agents"

# Recalculate total
validation_confidence = core_confidence + dynamic_confidence
```

---

## Step 3: Present Validation Summary

### Validation Summary Template

```markdown
---

## Task Quality Validation Results

**Overall Validation Score**: ${validation_score * 100}% (${validation_confidence_level})
**Validation Confidence**: ${validation_confidence * 100}%

**Validation Agents Selected** (confidence-based):
- ✓ planning (CORE) - Business Alignment
- ✓ architecture (CORE) - Technical Validation
- ✓ tech-debt-investigator (CORE) - Technical Debt Detection
${IF dynamic_agents_selected:}
${FOR EACH agent in dynamic_agents_selected:}
- ✓ ${agent.type} (${agent.confidence}) - ${agent.description} [HIGH CONFIDENCE]
${END FOR}
${END IF}

**Review Scores**:
- Business Alignment (planning): ${tpm.overall_score}/5.0 (${tpm.confidence * 100}% confidence)
- Technical Quality (architecture): ${arch.overall_score}/5.0 (${arch.confidence * 100}% confidence)
- Technical Debt (tech-debt-investigator): ${tech_debt.overall_score}/5.0 (${tech_debt.confidence * 100}% confidence)
${IF dynamic_agents_selected:}
${FOR EACH agent in dynamic_agents_selected:}
- ${agent.description} (${agent.type}): ${agent.overall_score}/${agent.scale} (${agent.confidence * 100}% confidence)
${END FOR}
${END IF}

${IF critical_issues.length > 0:}
### Critical Issues (${critical_issues.length}) - Must Fix Before Implementation

${FOR EACH issue in critical_issues:}
**${issue.title}** [${issue.source_agent}]
- **Impact**: ${issue.impact}
- **Recommendation**: ${issue.recommendation}
- **Effort**: ${issue.time_impact.hours_added} hours
- **Tasks Affected**: ${issue.affected_tasks[]}
${END FOR}

**Total Critical Enhancement Effort**: ${SUM(critical.hours_added)} hours

${END IF}

${IF high_priority.length > 0:}
### High-Priority Improvements (${high_priority.length}) - Should Fix

${FOR EACH issue in high_priority:}
**${issue.title}** [${issue.source_agent}]
- **Impact**: ${issue.impact}
- **Recommendation**: ${issue.recommendation}
- **Time Savings**: ${issue.time_impact.hours_saved} hours
- **Tasks Affected**: ${issue.affected_tasks[]}
${END FOR}

**Total High-Priority Time Savings**: ${SUM(high_priority.hours_saved)} hours

${END IF}

### Impact Summary
- **New/Modified Tasks Needed**: ${total_new_tasks}
- **Enhancement Effort**: ${total_effort_added} hours
- **Time Savings from Optimizations**: ${total_time_saved} hours
- **Net Impact**: ${net_impact} hours (${impact_percentage}% of sprint)

**Overall Recommendation**: ${recommendation_status}

${IF recommendation_status == "APPROVED WITH CRITICAL ENHANCEMENTS":}
⚠️ **Action Required**: Fix ${critical_issues.length} critical issues before implementation
   Would you like me to implement these fixes automatically?
${ELSE IF recommendation_status == "APPROVED WITH RECOMMENDED IMPROVEMENTS":}
✅ **Ready for Implementation** - Optional improvements available (${high_priority.length} items)
   Would you like me to implement these improvements?
${ELSE:}
✅ **Ready for Implementation** - High quality task list, no critical issues
${END IF}

---
```

---

## Step 4: Decision Logic

**Recommendation Status Determination**:

```python
IF critical_issues.length > 0:
  recommendation_status = "APPROVED WITH CRITICAL ENHANCEMENTS"
  action = "Present critical issues, offer to implement fixes"

ELSE IF high_priority.length > 3 OR net_impact > (total_sprint_points * 0.10):
  recommendation_status = "APPROVED WITH RECOMMENDED IMPROVEMENTS"
  action = "Present improvements, offer to implement"

ELSE:
  recommendation_status = "APPROVED - READY FOR IMPLEMENTATION"
  action = "Proceed directly to final summary"
```

---

## Error Handling

### Partial Validation Failure

```python
IF any_core_agent_failed:
  successful_core_agents = COUNT(core agents with status == "SUCCESS")
  WARN f"Partial core validation only ({successful_core_agents}/3 core agents succeeded)"
  core_confidence *= (successful_core_agents / 3)

IF any_dynamic_agent_failed:
  successful_dynamic_agents = COUNT(dynamic agents with status == "SUCCESS")
  INFO f"Partial dynamic validation ({successful_dynamic_agents}/{len(expected_dynamic_agents)} dynamic agents succeeded)"
  dynamic_confidence *= (successful_dynamic_agents / len(expected_dynamic_agents))

  # Recalculate total
  validation_confidence = core_confidence + dynamic_confidence

  IF successful_agents == 0:
    ERROR "Validation step failed - proceeding with tasks as-is"
    WARN "Tasks generated but not validated - use with caution"
    SKIP validation summary, proceed to final summary
```

### Complete Validation Failure

```
IF all 3 agents failed:
  ERROR "Task quality validation failed - all agents returned errors"
  WARN "Tasks generated but UNVALIDATED - manual review recommended"
  SKIP Step 6 entirely, proceed to Step 7 (Present Results)
```

---

## Optional: Save Validation Report

```markdown
IF validation executed successfully:
validation_report_path = "${task_dir}/../review/task-quality-validation.md"

Write consolidated validation report with: - All 3 agent outputs (full details) - Aggregated findings - Impact analysis - Recommendation status - Timestamp and metadata

REFERENCE in final summary:
"Detailed validation report: ${validation_report_path}"
```

---

## Integration with /tasks Command

**Invocation Point**: Step 6 of `/tasks` command (after Step 5 Result Collection completes)

**Inputs Required**:

- `success_results[]`: Array of successful task generation outputs
- `feature_synthesis`: Feature metadata from Step 3
- `discovered_context_files[]`: Context files found in Step 2
- `execution_timestamp`: Shared timestamp from Step 4

**Outputs Returned**:

- `validation_score`: Weighted aggregate score (0.0-1.0)
- `validation_confidence`: Aggregate confidence (0.0-1.0)
- `recommendation_status`: APPROVED / APPROVED WITH CRITICAL ENHANCEMENTS / APPROVED WITH RECOMMENDED IMPROVEMENTS
- `critical_issues[]`: Must-fix issues
- `high_priority[]`: Should-fix improvements
- `validation_report_path`: Optional saved report location

**Graceful Degradation**:

- IF validation fails: Continue with tasks as-is, warn user
- IF partial validation: Lower confidence, warn about missing perspectives
- IF low confidence: Add caveats to recommendation status

---

## Performance Characteristics

**Execution Time**: 2-5 minutes (parallel)
**Token Usage**: 15-30k tokens total (3 agents × 5-10k each)
**Scalability**: Works for 1-10+ task files (agents handle Read operations efficiently)

---

**This workflow ensures comprehensive task quality validation across business, technical, and integration dimensions with graceful failure handling and actionable recommendations.**
