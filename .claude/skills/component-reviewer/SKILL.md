---
name: component-reviewer
description: Automated codebase component review system for Python code, agents, workflows, documentation, and infrastructure. Use when performing code reviews, tech debt analysis, agent quality assessment, or system health checks. Supports random component selection for weekly CI jobs and targeted reviews.
allowed-tools: Read, Grep, Glob, Task, Bash, WebFetch, Write
---

# Component Reviewer

**Purpose**: Systematic, automated review of codebase components with agent-driven analysis and GitHub issue creation.

**Use Cases**:

- Weekly automated component reviews (CI job)
- Targeted reviews after major changes
- Tech debt analysis and prioritization
- Agent quality assessments
- Documentation health checks
- Security audits

## Quick Start

### Random Component Review (Weekly CI)

```
Review 3 random components this week and create GitHub issues for findings
```

### Targeted Component Review

```
Review all agents for quality and context efficiency
```

### Specific Review Type

```
Perform tech debt analysis on core infrastructure
```

---

## Instructions

### 1. Component Selection

**Random Selection** (for weekly CI jobs):

1. Use weighted random algorithm from [COMPONENT-TAXONOMY.md](COMPONENT-TAXONOMY.md#component-selection-strategy)
2. Default: 3 components per week
3. Weights favor high-impact areas (agents: 1.5x, api_layer: 1.4x, core_infrastructure: 1.5x)

**Targeted Selection** (user-specified):

1. User specifies component category (e.g., "agents", "commands", "core infrastructure")
2. Select all items in that category
3. Apply appropriate review types from taxonomy

**Component Categories** (see [COMPONENT-TAXONOMY.md](COMPONENT-TAXONOMY.md#component-categories)):

- **Claude Code Ecosystem**: agents, commands, hooks, documentation
- **Main Codebase**: core infrastructure, data connectors, API layer, testing
- **Documentation**: specifications, plans, guides
- **Scripts & Automation**: build scripts, validation tools
- **Infrastructure**: CI/CD workflows, dependencies

---

### 2. Review Type Identification

For each selected component, identify applicable review types from the [Review Type to Agent Mapping Matrix](COMPONENT-TAXONOMY.md#review-type-to-agent-mapping-matrix).

**Common Review Types by Component**:

| Component           | Review Types                                                          |
| ------------------- | --------------------------------------------------------------------- |
| Agents              | Agent Quality, Duplication Analysis, Context Usage, Domain Boundary   |
| Commands            | Workflow, Integration, Documentation, Security                        |
| Hooks               | Code Review, Security, Integration, Performance                       |
| Core Infrastructure | Code Review, Tech Debt, Performance, Security                         |
| API Layer           | API Design, Security, Performance, Documentation                      |
| Tests               | Test Quality, Performance, Reliability, Maintainability               |
| Specifications      | Spec Quality, Business Alignment, Technical Feasibility, Traceability |
| CI/CD               | Workflow, Security, Reliability, Cost                                 |

---

### 3. Agent Selection & Delegation

**Use Multi-Agent Analysis Pattern** (3 core + 0-2 dynamic agents):

#### Core Agent Selection (Always 3)

1. **tech-debt-investigator** (always included)
2. **Domain specialist #1** (based on component type):
   - Agents → claude-code-ecosystem
   - Code → code-quality
   - Docs → documentation
   - Tests → test-runner
   - Workflows → architecture
3. **Domain specialist #2** (based on review type):
   - Security → sast-scanner
   - Performance → debugger
   - Integration → architecture
   - Quality → planning

#### Dynamic Agent Selection (Confidence >0.8)

```
Confidence = (domain_fit × 0.6) + (unique_value × 0.3) + (cost_efficiency × 0.1)
```

**Example**: Reviewing agents with context usage analysis:

- **Core**: tech-debt-investigator, claude-code-ecosystem, claude-code-ecosystem
- **Dynamic**: documentation (confidence 0.85 for token optimization)
- **Total**: 4 agents

**Delegation Pattern**:

```
Task(agent="tech-debt-investigator", prompt="[specific scope]")
Task(agent="claude-code-ecosystem", prompt="[specific scope]")
Task(agent="claude-code-ecosystem", prompt="[specific scope]")
Task(agent="documentation", prompt="[specific scope]")
```

**Spawn all agents in parallel** (single message with multiple Task calls) for efficiency.

---

### 4. Review Execution

Each agent produces **structured output** containing:

**Required Fields**:

- Component path
- Review type
- Findings (issues, severity, evidence, recommendations)
- Metrics (quality scores, performance data)
- Summary statistics

**Severity Levels**:

- **Critical**: Security vulnerabilities, system-breaking issues (auto-fix via CI)
- **High**: Major quality/performance/reliability issues (create issue immediately)
- **Medium**: Tech debt, minor quality issues (batch into backlog)
- **Low**: Suggestions, enhancements (quarterly review)

**Quality Gates** (from [Quality Scoring Algorithms](COMPONENT-TAXONOMY.md#quality-assessment-frameworks)):

- SPEC Quality: ≥0.7
- PLAN Quality: ≥0.75
- Code Quality: All dimensions ≥4.0
- Test Coverage: >80%
- Security: Zero critical/high vulnerabilities

---

### 5. Result Synthesis

**Consolidate agent outputs**:

1. Merge findings from all agents
2. Deduplicate overlapping issues
3. Apply quality gates to determine pass/fail
4. Prioritize findings by severity + impact
5. Identify auto-fixable issues (critical severity + clear fix path)

**Output Structure** (see [Output Schema](COMPONENT-TAXONOMY.md#output-schema)):

```json
{
  "component": "component-category",
  "review_date": "2025-10-24",
  "agents_used": ["agent1", "agent2", "agent3"],
  "findings": [...],
  "metrics": {...},
  "summary": {
    "total_findings": 10,
    "by_severity": {"critical": 1, "high": 3, "medium": 4, "low": 2},
    "auto_fixable": 1
  },
  "recommendations": [...]
}
```

---

### 6. GitHub Issue Creation

**For each finding, create appropriate GitHub issue**:

#### Critical Issues (Auto-Fix via CI)

1. Create issue with label `type:bug`, `priority:critical`, `auto-fix`
2. Trigger Claude Code CI workflow (see [CI Integration](#ci-integration-workflow))
3. CI job attempts automated fix
4. PR created with fix + test validation
5. Link PR to issue

**Issue Template**:

```markdown
# [CRITICAL] {Finding Title}

**Component**: {component_path}
**Review Type**: {review_type}
**Agent**: {agent_name}
**Auto-Fixable**: Yes

## Description

{description}

## Evidence

{evidence}

## Recommended Fix

{recommendation}

## Expected Impact

{expected_improvement}

---

_Generated by component-reviewer Skill_
_Review Date: {timestamp}_
```

#### High/Medium Issues (Manual Review)

1. Create issue with appropriate labels:
   - High: `priority:high`, `needs:triage`
   - Medium: `priority:medium`, `type:tech-debt`
2. Include detailed findings and recommendations
3. Assign to appropriate team member (based on component ownership)

#### Low Issues (Batched)

1. Create quarterly tech debt issue
2. Aggregate low-priority findings
3. Prioritize using composite scoring

---

### 7. CI Integration Workflow

**Weekly CI Job** (.github/workflows/component-review.yml):

```yaml
name: Weekly Component Review

on:
  schedule:
    - cron: '0 10 * * 1' # Every Monday at 10 AM
  workflow_dispatch: # Manual trigger

jobs:
  component-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Component Review
        uses: anthropics/claude-code-ci@v1
        with:
          prompt: |
            Review 3 random components this week using the component-reviewer Skill.
            Create GitHub issues for all findings.
            For critical issues, attempt automated fixes.

      - name: Summary
        run: |
          echo "Component review complete"
          echo "See issues created: https://github.com/${{ github.repository }}/issues"
```

**Auto-Fix Process**:

1. Critical issue created with `auto-fix` label
2. Webhook triggers Claude Code CI job
3. CI job scope:
   - Read issue details (component, finding, recommendation)
   - Analyze current code
   - Apply fix following recommendation
   - Run validation (tests, linting, security scan)
   - If tests pass: Create PR
   - If tests fail: Add comment to issue with diagnosis
4. PR created with:
   - Fix implementation
   - Test validation results
   - Link to original issue
   - Request human review

---

## Review Examples

### Example 1: Weekly Random Review

**User Request**:

```
Review 3 random components this week
```

**Execution**:

1. **Select Components** (weighted random):
   - agents (weight 1.5) → `.claude/agents/code-quality.md`
   - data_connectors (weight 1.3) → `packages/connectors/redis_connector.py`
   - tests (weight 1.0) → `tests/unit/test_file_grouper.py`

2. **Identify Review Types**:
   - Agents: Agent Quality, Context Usage, Domain Boundary
   - Data Connectors: Integration, Reliability, Performance, Observability
   - Tests: Test Quality, Performance, Reliability

3. **Select Agents** (3 core + dynamic per component):
   - Component 1 (agents): tech-debt-investigator, claude-code-ecosystem, claude-code-ecosystem, documentation (4 total)
   - Component 2 (connectors): tech-debt-investigator, code-quality, debugger (3 total)
   - Component 3 (tests): tech-debt-investigator, test-runner, code-quality (3 total)

4. **Execute Reviews** (spawn all 10 agents in parallel - note: max 5 at a time, so batch in 2 groups)

5. **Synthesize Results**:
   - Total findings: 15 (2 critical, 5 high, 6 medium, 2 low)
   - Auto-fixable: 2 critical issues

6. **Create Issues**:
   - 2 critical (with auto-fix trigger)
   - 5 high (assigned to component owners)
   - 6 medium (batched into tech debt issue)
   - 2 low (added to quarterly backlog)

---

### Example 2: Targeted Agent Review

**User Request**:

```
Review all agents for quality and context efficiency
```

**Execution**:

1. **Select Components**: All files in `.claude/agents/*.md` (25 agents)

2. **Review Type**: Agent Quality, Context Usage, Domain Boundary

3. **Select Agents**:
   - Core: tech-debt-investigator, claude-code-ecosystem, claude-code-ecosystem
   - Dynamic: documentation (confidence 0.85 for context analysis)

4. **Execute Reviews**: Process agents in batches of 5, spawning 4 review agents per batch

5. **Synthesize Results**:
   - Generate agent quality matrix (all agents scored)
   - Identify context optimization opportunities
   - Detect capability duplication
   - Validate domain boundaries

6. **Create Report** + Issues:
   - Summary report: `docs/04-guides/agent-quality-report-2025-10-24.md`
   - Issues for agents scoring <0.7 quality
   - Recommendations for context optimization

---

### Example 3: Security Audit

**User Request**:

```
Perform security audit on API layer and hooks
```

**Execution**:

1. **Select Components**:
   - `packages/api/**/*.py`
   - `.claude/hooks/**/*.py`

2. **Review Type**: Security Review (OWASP compliance)

3. **Select Agents**:
   - Core: tech-debt-investigator, code-quality, sast-scanner
   - Dynamic: researcher-external (OWASP patterns, confidence 0.9)

4. **Execute Reviews**: Spawn all 4 agents in parallel

5. **Security Scan**:
   - OWASP Top 10 check (A01-A10)
   - OWASP LLM Top 10 check (LLM01, LLM02, LLM06)
   - Input validation review
   - Auth/authz verification
   - Command injection prevention

6. **Critical Findings**:
   - Any critical/high vulnerabilities → immediate issues + auto-fix
   - Medium/low → batched security hardening issue

---

## Best Practices

### For Weekly CI Reviews

1. **Consistent Scheduling**: Run every Monday at 10 AM to maintain rhythm
2. **Random Selection**: Use weighted algorithm to prioritize high-impact components
3. **Issue Management**: Auto-fix critical issues, triage high/medium, batch low
4. **Team Communication**: Post summary in Slack/Discord after each review
5. **Trend Tracking**: Monitor quality metrics over time, celebrate improvements

### For Targeted Reviews

1. **Trigger on Major Changes**: Review affected components after significant PRs
2. **Pre-Release Audits**: Full system review before production deployments
3. **Security Focus**: Monthly security audits on external-facing components
4. **Documentation Sync**: Review docs after major feature releases

### For Agent Delegation

1. **Parallel Execution**: Always spawn agents in parallel (max 5) for speed
2. **Confidence Thresholds**: Only include dynamic agents with >0.8 confidence
3. **Result Validation**: Verify findings before creating issues (reduce false positives)
4. **Progressive Detail**: Start with high-level review, deep-dive on issues found

### For Issue Management

1. **Clear Titles**: Use format `[SEVERITY] Component: Brief Description`
2. **Evidence-Based**: Always include code snippets, metrics, reproduction steps
3. **Actionable Recommendations**: Specific fix guidance, not vague suggestions
4. **Effort Estimates**: Include time estimate for fixing (helps prioritization)
5. **Follow-Up**: Link related issues, track patterns across components

---

## Success Metrics

**Coverage** (Target):

- All components reviewed monthly (100%)
- High-priority components reviewed weekly (agents, core, API)

**Quality** (Target):

- False positive rate <10%
- Finding validation rate >90%

**Impact** (Target):

- 50% of critical issues auto-fixed
- Median time to issue <24 hours
- 30% tech debt reduction in 6 months

**Efficiency** (Target):

- Review time <10 minutes per component
- Result synthesis <5 minutes
- Issue creation <2 minutes

---

## Troubleshooting

### Issue: Too Many False Positives

**Symptom**: Review agents finding issues that aren't real problems

> **Framework**: [5 Whys](../../docs/00-core/frameworks/analysis.md) - Ask "why" repeatedly to find root cause of false positive patterns

**Solutions**:

1. Increase confidence threshold for dynamic agents (0.8 → 0.85)
2. Add validation step: researcher-codebase verifies findings before issue creation
3. Update review guidelines with false positive patterns (see [Feedback Log](COMPONENT-TAXONOMY.md#review-process-patterns--feedback-log))

### Issue: Auto-Fix Failures

**Symptom**: Critical issues not being fixed automatically by CI

> **Framework**: [DMAIC](../../docs/00-core/frameworks/structured-execution.md) - Define→Measure→Analyze→Improve→Control for process optimization

**Solutions**:

1. Check if issue is truly auto-fixable (clear fix path, deterministic)
2. Improve fix recommendations in review findings
3. Add more context to issue description
4. Manual fix + update auto-fix patterns for future

### Issue: Review Taking Too Long

**Symptom**: Reviews exceeding time budgets

**Solutions**:

1. Reduce number of components per review (3 → 2)
2. Use faster review types (skip performance profiling for low-risk components)
3. Batch similar components together
4. Parallelize more aggressively (ensure max 5 agents used)

### Issue: Low Adoption of Findings

**Symptom**: Issues created but not addressed

> **Framework**: [Pre-Mortem](../../docs/00-core/frameworks/strategy.md) - Identify adoption barriers before they cause abandonment

**Solutions**:

1. Improve issue prioritization (focus on high-impact)
2. Better effort estimates (make fixes seem achievable)
3. Celebrate wins (highlight completed improvements)
4. Regular triage meetings (weekly team review)

---

## References

- **Component Taxonomy**: [COMPONENT-TAXONOMY.md](COMPONENT-TAXONOMY.md) - Complete component categorization and review matrix
- **Python Code Review Framework**: `docs/04-guides/code-review/Python Code Review Framework v2.md`
- **Multi-Agent Analysis Pattern**: `.claude/docs/orchestrator-workflow.md`
- **Quality Scoring Algorithms**: `.claude/docs/guides/validation/quality-scoring-algorithms.md`
- **Agent Architect**: `.claude/agents/claude-code-ecosystem.md` - For agent quality reviews
- **Tech Debt Investigator**: `.claude/agents/tech-debt-investigator.md` - For debt analysis

---

## Thinking Frameworks

When facing complex review challenges, these frameworks guide systematic problem-solving.

**Full Catalog**: [Thinking Frameworks README](../../docs/00-core/frameworks/README.md)

**Most Relevant for Component Review**:

| Framework | When to Use |
|-----------|-------------|
| [Pre-Mortem](../../docs/00-core/frameworks/strategy.md) | Identifying risks before component changes |
| [DMAIC](../../docs/00-core/frameworks/structured-execution.md) | Process optimization, reducing defects |
| [5 Whys](../../docs/00-core/frameworks/analysis.md) | Root cause analysis for false positives |

> **Selection Tip**: risk assessment->Pre-Mortem, process improvement->DMAIC, root cause->5 Whys

---

## Version History

- **v1.0.0** (2025-10-24): Initial release
  - Component taxonomy with 5 major categories
  - Review type to agent mapping matrix
  - CI integration workflow
  - GitHub issue creation automation
  - Auto-fix capability for critical issues