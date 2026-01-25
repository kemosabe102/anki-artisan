# Component Reviewer Skill

**Automated codebase component review system with CI integration and GitHub issue creation**

## Overview

The Component Reviewer Skill provides systematic, automated reviews of your codebase components using specialized review agents. It supports:

- **Random component selection** for weekly reviews
- **Targeted reviews** for specific components or categories
- **Multi-agent analysis** using the 3 core + dynamic agents pattern
- **Automated GitHub issue creation** for findings
- **CI integration** with auto-fix capability for critical issues
- **Comprehensive review types**: code quality, tech debt, security, performance, documentation, agent quality, context efficiency, and more

## Quick Start

### 1. Installation

Copy this Skill to your project:

```bash
# From repository root
mkdir -p .claude/skills/component-reviewer
cp -r path/to/component-reviewer/* .claude/skills/component-reviewer/
```

The Skill is now available to Claude Code and will be automatically discovered.

### 2. Test the Skill

Ask Claude to review components:

```
Review 3 random components this week
```

Claude will automatically use the component-reviewer Skill and:

1. Select 3 components using weighted random algorithm
2. Identify applicable review types
3. Delegate to appropriate review agents
4. Synthesize findings
5. Report results

### 3. Set Up CI (Optional)

To enable weekly automated reviews with GitHub issue creation:

```bash
# Copy workflow to your repository
mkdir -p .github/workflows
cp .claude/skills/component-reviewer/ci-workflow.yml .github/workflows/component-review.yml

# Commit and push
git add .github/workflows/component-review.yml
git commit -m "feat: add weekly component review CI workflow"
git push
```

**Requirements**:

- GitHub repository with Actions enabled
- `ANTHROPIC_API_KEY` secret configured in repository settings
- Anthropic Claude Code CI integration installed

## Usage

### Interactive Usage (Claude Code)

#### Random Component Review

```
Review 3 random components and create issues for findings
```

#### Targeted Category Review

```
Review all agents for quality and context efficiency
```

#### Specific Component Review

```
Review packages/core/auth/login.py for security and performance
```

#### Security Audit

```
Perform security audit on API layer and hooks
```

#### Tech Debt Analysis

```
Analyze tech debt in core infrastructure
```

### CI Usage (GitHub Actions)

#### Weekly Scheduled Review

The CI workflow runs automatically every Monday at 10:00 AM UTC.

**Manual Trigger**:

```bash
# Trigger via GitHub CLI
gh workflow run component-review.yml

# With custom parameters
gh workflow run component-review.yml \
  -f component_count=5 \
  -f target_component=agents \
  -f review_types=security,tech_debt
```

**GitHub UI**:

1. Go to Actions tab
2. Select "Weekly Component Review" workflow
3. Click "Run workflow"
4. Configure parameters (optional)
5. Click "Run workflow"

### Script Usage (Standalone)

```bash
# Select 3 random components
uv run python .claude/skills/component-reviewer/component_selector.py

# Select 5 random components
uv run python .claude/skills/component-reviewer/component_selector.py --count 5

# Select all agents
uv run python .claude/skills/component-reviewer/component_selector.py --category agents

# Output as JSON
uv run python .claude/skills/component-reviewer/component_selector.py --format json
```

## Component Categories

The Skill organizes your codebase into 14 component categories:

### Claude Code Ecosystem

1. **agents** (.claude/agents/\*.md) - Sub-agent definitions
2. **commands** (.claude/commands/\*.md) - Workflow automation
3. **hooks** (.claude/hooks/\*.py) - Event-driven scripts
4. **claude_docs** (.claude/docs/\*\*) - Agent standards and guides

### Main Codebase

5. **core_infrastructure** (packages/core/\*\*) - Business logic
6. **data_connectors** (packages/connectors/\*\*) - External integrations
7. **api_layer** (packages/api/\*\*) - HTTP/GraphQL endpoints
8. **tests** (tests/\*\*) - Test infrastructure

### Documentation

9. **specifications** (docs/01-planning/specifications/\*\*) - Feature specs
10. **plans** (docs/02-planning/\*\*) - Implementation plans
11. **guides** (docs/04-guides/\*\*) - Process documentation

### Infrastructure

12. **scripts** (scripts/\*\*) - Automation scripts
13. **ci_workflows** (.github/workflows/\*\*) - CI/CD workflows
14. **dependencies** (pyproject.toml, uv.lock) - Dependency management

**Full taxonomy**: See [COMPONENT-TAXONOMY.md](COMPONENT-TAXONOMY.md)

## Review Types

The Skill supports 15+ review types, automatically selected based on component category:

| Review Type                    | Description                              | Primary Agents                                  |
| ------------------------------ | ---------------------------------------- | ----------------------------------------------- |
| **Agent Quality Review**       | Capability assessment, prompt quality    | claude-code-ecosystem, claude-code-ecosystem               |
| **Agent Duplication Analysis** | Capability overlap detection             | feature-analyzer, tech-debt-investigator        |
| **Context Usage Analysis**     | Token efficiency, progressive disclosure | documentation, context-optimizer      |
| **Code Review**                | Python quality (6 dimensions)            | code-quality, test-runner               |
| **Tech Debt Analysis**         | Complexity, duplication, weak boundaries | tech-debt-investigator, development |
| **Security Review**            | OWASP compliance, vulnerability scanning | code-quality, sast-scanner              |
| **Performance Review**         | Async correctness, N+1 queries           | debugger, code-quality                  |
| **API Design Review**          | RESTful principles, versioning           | architecture                             |
| **Test Quality Review**        | Coverage, assertions, fixtures           | test-runner, code-quality               |
| **Workflow Review**            | Process efficiency, error handling       | architecture, planning               |
| **Documentation Review**       | Clarity, completeness, accuracy          | documentation, planning                    |
| **Integration Review**         | Protocol compliance, resilience          | architecture, researcher-codebase        |
| **Reliability Review**         | Error handling, graceful degradation     | debugger, architecture                   |
| **Observability Review**       | Logging, metrics, tracing                | code-quality, researcher-external       |
| **Specification Quality**      | Completeness, testability, clarity       | planning, planning                     |

**Full review matrix**: See [COMPONENT-TAXONOMY.md](COMPONENT-TAXONOMY.md#review-type-to-agent-mapping-matrix)

## Agent Selection

The Skill uses the **Multi-Agent Analysis Pattern** (3 core + 0-2 dynamic agents):

### Core Agents (Always 3)

1. **tech-debt-investigator** (always included)
2. **Domain specialist #1** (based on component)
3. **Domain specialist #2** (based on review type)

### Dynamic Agents (Confidence >0.8)

- Additional agents included when confidence score >0.8
- Calculated as: `(domain_fit × 0.6) + (unique_value × 0.3) + (cost_efficiency × 0.1)`

### Example: Reviewing Agents

**Component**: `.claude/agents/code-quality.md`

**Review Types**: Agent Quality, Context Usage, Domain Boundary

**Selected Agents**:

- **Core**: tech-debt-investigator, claude-code-ecosystem, claude-code-ecosystem
- **Dynamic**: documentation (confidence 0.85 for token optimization)
- **Total**: 4 agents

**Delegation**:

```python
# Spawned in parallel (single message, multiple Task calls)
Task(agent="tech-debt-investigator", prompt="Analyze code-quality.md for tech debt...")
Task(agent="claude-code-ecosystem", prompt="Review code-quality.md quality...")
Task(agent="claude-code-ecosystem", prompt="Evaluate code-quality.md prompts...")
Task(agent="documentation", prompt="Analyze context usage...")
```

## GitHub Issue Creation

The Skill automatically creates GitHub issues for all findings:

### Critical Issues (Auto-Fix)

- **Labels**: `type:bug`, `priority:critical`, `auto-fix`
- **Behavior**: Triggers Claude Code CI for automated fix
- **CI Process**:
  1. Read issue details
  2. Analyze current code
  3. Apply fix
  4. Run validation (tests, linting)
  5. Create PR if tests pass
  6. Comment on issue if tests fail

### High Priority Issues

- **Labels**: `priority:high`, `needs:triage`
- **Behavior**: Assigned to component owner
- **Action Required**: Manual review and fix

### Medium Priority Issues

- **Labels**: `priority:medium`, `type:tech-debt`
- **Behavior**: Batched into tech debt backlog
- **Action Required**: Prioritized in sprint planning

### Low Priority Issues

- **Labels**: `priority:low`, `enhancement`
- **Behavior**: Added to quarterly review backlog
- **Action Required**: Reviewed quarterly

**Issue Template Example**:

```markdown
# [CRITICAL] Excessive token usage in code-quality agent

**Component**: .claude/agents/code-quality.md
**Review Type**: Context Usage Analysis
**Agent**: documentation
**Auto-Fixable**: Yes

## Description

Agent instructions exceed 10K characters (12,543 characters), reducing context
availability for actual code review work. Recommend refactoring to use
progressive disclosure pattern.

## Evidence

- Current size: 12,543 characters
- Threshold: 10,000 characters
- Efficiency score: 0.65 (target: >0.80)

## Recommended Fix

1. Extract verbose content to separate documentation files
2. Replace with concise references
3. Update schema to reflect changes

## Expected Impact

- 30% token reduction (3,763 characters saved)
- Improved context availability for code review
- Faster agent loading

---

_Generated by component-reviewer Skill_
_Review Date: 2025-10-24T10:30:00Z_
```

## CI Workflow Details

### Weekly Schedule

- **Runs**: Every Monday at 10:00 AM UTC
- **Selects**: 3 random components (weighted by priority)
- **Agents**: 3-5 per component (multi-agent pattern)
- **Duration**: ~10-15 minutes total
- **Output**: GitHub issues + summary report

### Manual Trigger

- **Available**: Via GitHub Actions UI or CLI
- **Parameters**:
  - `component_count`: Number of components (default: 3)
  - `target_component`: Specific category (optional)
  - `review_types`: Comma-separated types (optional)

### Auto-Fix Process

1. **Issue Created**: With `auto-fix` label
2. **Webhook Triggered**: CI job starts
3. **Fix Applied**: Claude attempts automated fix
4. **Validation**: Tests, linting, type checking
5. **PR Created**: If validation passes
6. **Human Review**: Approve and merge PR

### Notifications

Configure notifications by uncommenting the notification step in `ci-workflow.yml`:

```yaml
# Slack example
- name: Send Slack Notification
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
    payload: |
      {
        "text": "Weekly Component Review Complete",
        "blocks": [...]
      }
```

## Output and Artifacts

### Review Reports

- **Location**: `docs/04-guides/component-review-YYYY-MM-DD.md`
- **Content**:
  - Components reviewed
  - Agents used
  - Findings by severity
  - Quality metrics
  - Recommendations

### Review Data

- **Location**: `.claude/debug/review-YYYY-MM-DD.json`
- **Format**: Structured JSON
- **Content**:
  - Complete findings
  - Agent outputs
  - Metrics and scores
  - Evidence and references

### GitHub Issues

- **Labels**: Severity-based (`critical`, `high`, `medium`, `low`)
- **Assignees**: Component owners (if configured)
- **Projects**: Added to relevant project boards (if configured)
- **Milestones**: Linked to current sprint (if configured)

### CI Artifacts

- **Retention**: 90 days
- **Content**: Review reports + JSON data
- **Download**: From GitHub Actions run page

## Configuration

### Component Weights

Adjust review frequency by modifying weights in `component_selector.py`:

```python
COMPONENT_WEIGHTS = {
    "agents": 1.5,           # Review more frequently
    "core_infrastructure": 1.5,  # High priority
    "tests": 1.0,            # Medium priority
    "guides": 0.7,           # Review less frequently
}
```

Higher weights = more frequent selection in random reviews.

### Review Thresholds

Adjust quality gates in component reviews:

- **Code Quality**: Default ≥4.0 (all dimensions)
- **Test Coverage**: Default >80%
- **Security**: Zero critical/high vulnerabilities
- **Tech Debt Score**: Default <0.3

Modify in agent delegation prompts for stricter/looser standards.

### Agent Confidence

Adjust confidence threshold for dynamic agents:

```python
# In SKILL.md instructions
# Current: Include dynamic agents if confidence >0.8
# Stricter: Change to >0.85 (fewer dynamic agents)
# Looser: Change to >0.75 (more dynamic agents)
```

## Success Metrics

Track these metrics to measure review system effectiveness:

### Coverage Metrics

- ✅ All components reviewed monthly: 100%
- ✅ High-priority components reviewed weekly: 100%
- ✅ Random selection distribution: Matches weights

### Quality Metrics

- ✅ False positive rate: <10%
- ✅ Finding validation rate: >90%
- ✅ Issue actionability: >85%

### Impact Metrics

- ✅ Critical issues auto-fixed: 50%+
- ✅ Median time to issue creation: <24 hours
- ✅ Tech debt reduction: 30% over 6 months

### Efficiency Metrics

- ✅ Review time per component: <10 minutes
- ✅ Result synthesis time: <5 minutes
- ✅ Issue creation time: <2 minutes

## Troubleshooting

### Issue: Skill Not Recognized

**Symptom**: Claude doesn't use the component-reviewer Skill

**Solutions**:

1. Verify Skill location: `.claude/skills/component-reviewer/SKILL.md`
2. Check YAML frontmatter syntax (valid YAML)
3. Restart Claude Code session
4. Verify description field contains relevant keywords

### Issue: Too Many False Positives

**Symptom**: Review agents finding issues that aren't real

**Solutions**:

1. Increase confidence threshold for dynamic agents (0.8 → 0.85)
2. Add validation step before issue creation
3. Update review guidelines with false positive patterns
4. Review feedback log for common patterns

### Issue: Auto-Fix Failures

**Symptom**: Critical issues not being fixed automatically

**Solutions**:

1. Check if issue is truly auto-fixable (clear fix path)
2. Improve fix recommendations in findings
3. Add more context to issue description
4. Manual fix + update auto-fix patterns

### Issue: Reviews Taking Too Long

**Symptom**: Reviews exceeding time budgets

**Solutions**:

1. Reduce component count (3 → 2)
2. Skip performance profiling for low-risk components
3. Batch similar components together
4. Ensure parallel agent spawning (max 5)

### Issue: CI Workflow Fails

**Symptom**: GitHub Actions workflow fails

**Solutions**:

1. Check `ANTHROPIC_API_KEY` secret is configured
2. Verify Claude Code CI integration is installed
3. Check workflow permissions (contents, issues, PRs)
4. Review workflow logs for specific errors

## Examples

### Example 1: Weekly Random Review

**Request**:

```
Review 3 random components this week
```

**Execution**:

1. **Components Selected**:
   - `.claude/agents/code-quality.md` (agents, weight 1.5)
   - `packages/connectors/redis_connector.py` (data_connectors, weight 1.3)
   - `tests/unit/test_file_grouper.py` (tests, weight 1.0)

2. **Review Types**:
   - Agents: Agent Quality, Context Usage, Domain Boundary
   - Connectors: Integration, Reliability, Performance, Observability
   - Tests: Test Quality, Performance, Reliability

3. **Agents**: 10 total (batched in 2 groups of 5)

4. **Findings**: 15 total (2 critical, 5 high, 6 medium, 2 low)

5. **Issues Created**:
   - 2 critical (auto-fix triggered)
   - 5 high (assigned)
   - 6 medium (batched)
   - 2 low (quarterly backlog)

### Example 2: Security Audit

**Request**:

```
Perform security audit on API layer and hooks
```

**Execution**:

1. **Components**: All files in `packages/api/**/*.py` + `.claude/hooks/**/*.py`

2. **Review Type**: Security Review (OWASP)

3. **Agents**: tech-debt-investigator, code-quality, sast-scanner, researcher-external

4. **Scan**: OWASP Top 10 + LLM Top 10 + input validation

5. **Findings**: Security vulnerabilities by severity

6. **Issues**: Immediate creation for critical/high

### Example 3: Agent Quality Assessment

**Request**:

```
Review all agents for quality and context efficiency
```

**Execution**:

1. **Components**: All 25 agents in `.claude/agents/`

2. **Review Types**: Agent Quality, Context Usage, Domain Boundary

3. **Agents**: tech-debt-investigator, claude-code-ecosystem, claude-code-ecosystem, documentation

4. **Output**:
   - Agent quality matrix (all agents scored)
   - Context optimization opportunities
   - Capability duplication report
   - Domain boundary validation

5. **Artifacts**:
   - `docs/04-guides/agent-quality-report-2025-10-24.md`
   - Issues for agents scoring <0.7

## References

- **Component Taxonomy**: [COMPONENT-TAXONOMY.md](COMPONENT-TAXONOMY.md)
- **Skill Definition**: [SKILL.md](SKILL.md)
- **CI Workflow**: [ci-workflow.yml](ci-workflow.yml)
- **Component Selector**: [component_selector.py](component_selector.py)

## Contributing

To improve the component-reviewer Skill:

1. Add new component categories in `COMPONENT_TAXONOMY.md`
2. Define review types and agent mappings
3. Update `component_selector.py` with new paths/patterns
4. Test with manual reviews before adding to CI
5. Document changes in this README

## License

Part of Gauntlet Agents project - see repository LICENSE file.

## Support

For issues or questions:

- Create GitHub issue with label `component:skill-component-reviewer`
- Include: Request, expected behavior, actual behavior, logs
- Tag relevant team members

---

**Version**: 1.0.0
**Last Updated**: 2025-10-24
**Maintainer**: Gauntlet Agents Team