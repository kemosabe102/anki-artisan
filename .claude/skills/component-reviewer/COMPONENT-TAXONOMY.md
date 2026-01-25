# Component Taxonomy & Review Matrix

**Purpose**: Systematic categorization of codebase components for targeted, automated reviews

**Last Updated**: 2025-10-24

## Component Categories

### 1. Claude Code Ecosystem (.claude/\*\*)

#### 1.1 Agents (.claude/agents/\*.md)

**Description**: Sub-agent definitions with capabilities, tools, and domain boundaries

**Review Types**:

- **Agent Quality Review**: Capability assessment, prompt engineering quality, tool alignment
- **Agent Duplication Analysis**: Capability overlap detection, consolidation opportunities
- **Context Usage Analysis**: Token efficiency, progressive disclosure effectiveness
- **Domain Boundary Validation**: Scope clarity, anti-pattern detection

**Key Metrics**:

- Quality score (9-dimensional matrix from claude-code-ecosystem): Target ≥70%
- Token efficiency: Instructions <10K characters
- Tool-task alignment: >80% appropriate tool usage
- Domain clarity: Zero scope ambiguity

**Review Artifacts**:

- Capability overlap matrix
- Context usage breakdown
- Domain violation incidents
- Quality improvement recommendations

---

#### 1.2 Commands (.claude/commands/\*.md)

**Description**: Workflow automation implementations (slash commands)

**Review Types**:

- **Workflow Review**: Process efficiency, error handling, user experience
- **Integration Review**: Agent delegation patterns, tool usage, orchestration quality
- **Documentation Review**: Usage clarity, examples completeness, edge case coverage
- **Security Review**: Input validation, command injection prevention, privilege escalation risks

**Key Metrics**:

- Workflow efficiency: Steps to value ratio
- Error recovery: Graceful degradation present
- Documentation completeness: 100% parameters documented
- Security posture: OWASP LLM Top 10 compliance

**Review Artifacts**:

- Workflow bottleneck analysis
- Orchestration pattern adherence
- Documentation gaps
- Security vulnerability report

---

#### 1.3 Hooks (.claude/hooks/\*.py)

**Description**: Event-driven automation scripts (startup, validation, cleanup)

**Review Types**:

- **Code Review**: Python quality (Framework v2), performance, error handling
- **Security Review**: Command whitelist validation, path traversal prevention, OWASP compliance
- **Integration Review**: Event lifecycle correctness, side effect management
- **Performance Review**: Execution time <2s per hook, resource usage

**Key Metrics**:

- Code quality: 6-dimensional score (Framework v2): Target ≥4.0
- Security score: Zero critical vulnerabilities
- Performance: <2s execution, <50MB memory
- Reliability: >99% success rate

**Review Artifacts**:

- Code quality report (6 dimensions)
- Security vulnerability scan results
- Performance profiling data
- Error rate and failure modes

---

#### 1.4 Documentation (.claude/docs/\*\*)

**Description**: Agent standards, guides, schemas, orchestration patterns

**Review Types**:

- **Documentation Quality Review**: Clarity, completeness, accuracy, maintainability
- **Technical Accuracy Review**: Code examples validation, API correctness, version compatibility
- **Consistency Review**: Terminology alignment, format standardization, cross-references
- **Relevance Review**: Staleness detection, deprecation identification, update requirements

**Key Metrics**:

- Accuracy: 100% code examples executable
- Completeness: All critical paths documented
- Consistency: Zero terminology conflicts
- Freshness: <30 days since last validation

**Review Artifacts**:

- Broken link report
- Stale documentation list
- Terminology inconsistencies
- Missing cross-references

---

### 2. Main Codebase (packages/**, tests/**, src/\*\*)

#### 2.1 Core Infrastructure (packages/core/\*\*)

**Description**: Core business logic, domain models, shared utilities

**Review Types**:

- **Code Review**: Python Framework v2 (6 dimensions), architectural integrity
- **Tech Debt Analysis**: Complexity, duplication, missing tests, weak boundaries
- **Performance Review**: Async correctness, N+1 queries, resource efficiency
- **Security Review**: OWASP Top 10 (A01-A06), input validation, auth/authz

**Key Metrics**:

- Code quality: All 6 dimensions ≥4.0
- Test coverage: >80%
- Tech debt score: <0.3 (low risk)
- Security: Zero high/critical vulnerabilities

**Review Artifacts**:

- Multi-dimensional code quality report
- Tech debt hotspot graph
- Performance profiling results
- Security scan findings

---

#### 2.2 Data Connectors (packages/connectors/\*\*)

**Description**: External system integrations (APIs, databases, message queues)

**Review Types**:

- **Integration Review**: Protocol compliance, error handling, retry logic, circuit breakers
- **Reliability Review**: Resilience patterns, timeout management, graceful degradation
- **Performance Review**: Connection pooling, batch operations, caching strategy
- **Observability Review**: Logging quality, metrics emission, tracing coverage

**Key Metrics**:

- Reliability: >99.9% success rate
- Performance: p95 latency <100ms
- Error handling: 100% failure modes covered
- Observability: All external calls traced

**Review Artifacts**:

- Integration quality scorecard
- Resilience pattern compliance
- Performance benchmark results
- Observability coverage map

---

#### 2.3 API Layer (packages/api/\*\*)

**Description**: HTTP APIs, GraphQL endpoints, WebSocket handlers

**Review Types**:

- **API Design Review**: RESTful principles, endpoint consistency, versioning strategy
- **Security Review**: Auth/authz, rate limiting, input validation, OWASP API Top 10
- **Performance Review**: Response times, payload sizes, caching headers
- **Documentation Review**: OpenAPI spec accuracy, example completeness

**Key Metrics**:

- Design quality: RESTful maturity level ≥3
- Security: Zero API vulnerabilities
- Performance: p95 <200ms
- Documentation: 100% endpoints documented

**Review Artifacts**:

- API design assessment
- Security vulnerability report
- Performance profiling data
- Documentation completeness check

---

#### 2.4 Testing Infrastructure (tests/\*\*)

**Description**: Unit tests, integration tests, test fixtures, test utilities

**Review Types**:

- **Test Quality Review**: Coverage, assertion strength, fixture design, mock alignment
- **Test Performance Review**: Execution speed, resource usage, parallelization
- **Test Reliability Review**: Flakiness detection, determinism, isolation
- **Test Maintainability Review**: DRY violations, fixture reuse, test data management

**Key Metrics**:

- Coverage: >80% line, >70% branch
- Quality: Strong assertions (no bare assertions)
- Performance: <5min full suite
- Reliability: Zero flaky tests

**Review Artifacts**:

- Coverage report with gaps
- Flaky test identification
- Performance bottleneck analysis
- Maintainability improvement suggestions

---

### 3. Documentation (docs/\*\*)

#### 3.1 Specifications (docs/01-planning/specifications/\*\*)

**Description**: Feature specifications following SDD methodology

**Review Types**:

- **Specification Quality Review**: Completeness, testability, clarity, ambiguity detection
- **Business Alignment Review**: Pain point coverage, ROI validation, success metrics
- **Technical Feasibility Review**: Architecture soundness, dependency analysis, risk assessment
- **Traceability Review**: FR-ID consistency, component mapping, task coverage

**Key Metrics**:

- Quality score: ≥0.7 (planning grading)
- Business alignment: ≥0.4 pain point score
- Technical readiness: ≥0.75 plan quality
- Traceability: 100% FR-ID → component → task

**Review Artifacts**:

- Specification quality report (A-F grade)
- Business alignment scorecard
- Technical feasibility assessment
- Traceability coverage matrix

---

#### 3.2 Plans (docs/02-planning/\*\*)

**Description**: Implementation plans with technical/business details

**Review Types**:

- **Plan Quality Review**: Implementation readiness, resource allocation, timeline realism
- **Architecture Review**: Technical soundness, pattern compliance, production readiness
- **Integration Review**: Cross-plan consistency, interface design, dependency management
- **Risk Review**: Risk identification, mitigation strategies, contingency plans

**Key Metrics**:

- Plan quality: ≥0.75 (quality gate)
- Architecture: All criteria ≥4.0
- Integration: Zero conflicts
- Risk coverage: All identified risks have mitigation

**Review Artifacts**:

- Plan quality assessment
- Architecture scoring report
- Integration conflict matrix
- Risk mitigation completeness

---

#### 3.3 Guides (docs/04-guides/\*\*)

**Description**: Development guides, process documentation, best practices

**Review Types**:

- **Documentation Quality Review**: Clarity, accuracy, completeness, usability
- **Process Review**: Workflow efficiency, bottleneck identification, improvement opportunities
- **Consistency Review**: Cross-guide alignment, terminology standardization
- **Adoption Review**: Usage tracking, pain point feedback, update frequency

**Key Metrics**:

- Accuracy: 100% procedures validated
- Completeness: All workflows documented
- Consistency: Zero conflicts
- Adoption: >80% team following guides

**Review Artifacts**:

- Documentation quality scorecard
- Process bottleneck analysis
- Terminology consistency report
- Adoption metrics and feedback

---

### 4. Scripts & Automation (scripts/\*\*)

#### 4.1 Build & Validation Scripts

**Description**: Build automation, validation tools, code quality scripts

**Review Types**:

- **Code Review**: Python Framework v2, error handling, portability
- **Reliability Review**: Edge case handling, failure modes, recovery logic
- **Performance Review**: Execution speed, resource efficiency, parallel execution
- **Usability Review**: CLI design, help text, error messages

**Key Metrics**:

- Code quality: All dimensions ≥4.0
- Reliability: >99% success rate
- Performance: Fast feedback (<2min for common operations)
- Usability: Clear error messages, helpful output

**Review Artifacts**:

- Code quality report
- Reliability test results
- Performance benchmarks
- Usability assessment

---

### 5. Infrastructure & Config

#### 5.1 CI/CD Workflows (.github/workflows/\*\*)

**Description**: GitHub Actions workflows for testing, validation, deployment

**Review Types**:

- **Workflow Review**: Efficiency, parallelization, caching strategy
- **Security Review**: Secret handling, permission scoping, supply chain security
- **Reliability Review**: Flakiness, timeout management, retry logic
- **Cost Review**: Execution time, runner usage, optimization opportunities

**Key Metrics**:

- Efficiency: Optimal parallelization
- Security: Zero secrets in logs
- Reliability: <5% failure rate
- Cost: Execution time trending down

**Review Artifacts**:

- Workflow efficiency analysis
- Security scan results
- Reliability metrics
- Cost optimization recommendations

---

#### 5.2 Environment & Dependencies (pyproject.toml, .env.example, etc.)

**Description**: Dependency management, environment configuration, build settings

**Review Types**:

- **Dependency Review**: Version currency, vulnerability scanning, unused dependencies
- **Configuration Review**: Completeness, documentation, sensible defaults
- **Security Review**: Dependency vulnerabilities, secret management, secure defaults
- **Maintainability Review**: Lock file hygiene, update frequency, breaking changes

**Key Metrics**:

- Currency: Dependencies <6 months old
- Security: Zero vulnerabilities
- Completeness: All required config documented
- Maintainability: Regular updates

**Review Artifacts**:

- Dependency vulnerability scan
- Configuration completeness check
- Security assessment
- Update recommendations

---

## Component Selection Strategy

### Random Selection Algorithm

```python
import random
from typing import List, Dict

# Weight components by review priority (higher = more frequent reviews)
COMPONENT_WEIGHTS = {
    "agents": 1.5,           # Higher priority - core to system
    "commands": 1.2,         # Medium-high - user-facing
    "hooks": 1.0,            # Medium - security-critical
    "core_infrastructure": 1.5,  # High - business logic
    "data_connectors": 1.3,  # Medium-high - reliability critical
    "api_layer": 1.4,        # High - security surface
    "tests": 1.0,            # Medium - quality foundation
    "specifications": 0.8,   # Medium-low - less frequently changed
    "plans": 0.7,            # Lower - stable after completion
    "ci_workflows": 1.1,     # Medium - cost/reliability
}

def select_weekly_components(count: int = 3) -> List[str]:
    """Select components for weekly review using weighted random selection"""
    components = list(COMPONENT_WEIGHTS.keys())
    weights = list(COMPONENT_WEIGHTS.values())
    return random.choices(components, weights=weights, k=count)
```

### Review Scheduling

- **Weekly**: 3 randomly selected components
- **Monthly**: Full category rotation (all components reviewed once)
- **Quarterly**: Comprehensive system-wide review
- **Ad-hoc**: Triggered by code changes in component

---

## Review Type to Agent Mapping Matrix

| Review Type                    | Primary Agent(s)                           | Support Agents                      | Confidence Threshold |
| ------------------------------ | ------------------------------------------ | ----------------------------------- | -------------------- |
| **Agent Quality Review**       | claude-code-ecosystem, claude-code-ecosystem          | researcher-codebase                 | ≥0.8                 |
| **Agent Duplication Analysis** | feature-analyzer                           | tech-debt-investigator              | ≥0.8                 |
| **Context Usage Analysis**     | documentation, context-optimizer | researcher-codebase                 | ≥0.7                 |
| **Domain Boundary Validation** | claude-code-ecosystem                            | tech-debt-investigator              | ≥0.9                 |
| **Workflow Review**            | architecture, planning          | tech-debt-investigator              | ≥0.8                 |
| **Integration Review**         | architecture                        | researcher-codebase                 | ≥0.8                 |
| **Documentation Review**       | documentation, planning               | researcher-codebase                 | ≥0.7                 |
| **Security Review**            | code-quality, sast-scanner         | researcher-external (OWASP)         | ≥0.9                 |
| **Code Review (Python)**       | code-quality                       | test-runner, tech-debt-investigator | ≥0.9                 |
| **Tech Debt Analysis**         | tech-debt-investigator                     | development             | ≥0.9                 |
| **Performance Review**         | debugger, code-quality             | researcher-external                 | ≥0.8                 |
| **Test Quality Review**        | test-runner                                | code-quality                | ≥0.8                 |
| **API Design Review**          | architecture                        | researcher-external                 | ≥0.8                 |
| **Reliability Review**         | debugger, architecture              | researcher-codebase                 | ≥0.8                 |
| **Observability Review**       | code-quality                       | researcher-external                 | ≥0.7                 |

### Agent Selection Rules

**Multi-Agent Pattern** (3 core + 0-2 dynamic):

- **Core agents**: Always included (tech-debt-investigator + 2 domain-specific)
- **Dynamic agents**: Included if confidence >0.8

**Confidence Formula**:

```
Confidence = (domain_fit × 0.6) + (unique_value × 0.3) + (cost_efficiency × 0.1)
```

**Delegation Pattern**:

- Spawn agents in parallel (max 5 total)
- Synthesize results in orchestrator
- Generate consolidated findings

---

## Review Execution Workflow

### Phase 1: Component Selection

1. Select component(s) using weighted random algorithm
2. Identify applicable review types from taxonomy
3. Map review types to agents using matrix
4. Calculate agent selection confidence

### Phase 2: Agent Delegation

1. Spawn review agents in parallel (max 5)
2. Each agent produces structured output:
   - Findings (issues, recommendations)
   - Metrics (quality scores, performance data)
   - Artifacts (reports, graphs, checklists)

### Phase 3: Result Synthesis

1. Orchestrator consolidates agent outputs
2. Apply quality gates and thresholds
3. Identify critical issues requiring immediate action
4. Generate improvement recommendations

### Phase 4: Issue Creation

1. Create GitHub issues for findings:
   - **Critical**: Auto-create PR with fix (Claude Code CI)
   - **High**: Create issue with reproduction steps
   - **Medium**: Batch into tech debt issue
   - **Low**: Add to quarterly review backlog

### Phase 5: CI Integration

1. Critical issues trigger Claude Code CI job
2. Claude attempts automated fix
3. PR created with changes + test validation
4. Human review + merge

---

## Output Schema

### Review Finding Schema

```json
{
  "component": "agents",
  "component_path": ".claude/agents/code-quality.md",
  "review_type": "Agent Quality Review",
  "agent": "claude-code-ecosystem",
  "timestamp": "2025-10-24T10:30:00Z",
  "findings": [
    {
      "id": "FIND-001",
      "severity": "high",
      "category": "Context Efficiency",
      "title": "Excessive token usage in instructions",
      "description": "Agent instructions exceed 10K characters, reducing context availability",
      "evidence": {
        "current_size": 12543,
        "threshold": 10000,
        "efficiency_score": 0.65
      },
      "recommendation": {
        "action": "Refactor instructions using progressive disclosure",
        "expected_improvement": "30% token reduction",
        "estimated_effort": "2-3 hours"
      },
      "auto_fixable": false
    }
  ],
  "metrics": {
    "quality_score": 0.72,
    "token_efficiency": 0.65,
    "domain_clarity": 0.95,
    "tool_alignment": 0.88
  },
  "summary": {
    "total_findings": 5,
    "critical": 0,
    "high": 2,
    "medium": 2,
    "low": 1
  },
  "recommendations": [
    "Refactor verbose instructions",
    "Add progressive disclosure links",
    "Update schema for efficiency"
  ]
}
```

---

## Success Metrics

**Coverage**:

- All components reviewed at least monthly
- 100% of critical components reviewed weekly

**Quality**:

- > 90% of findings validated (not false positives)
- <10% false positive rate

**Impact**:

- 50% of critical issues auto-fixed via CI
- <24 hour median time to issue creation
- 30% reduction in tech debt over 6 months

**Efficiency**:

- <10 minutes per component review
- <5 minutes result synthesis
- <2 minutes issue creation

---

## References

- **Python Code Review Framework v2**: `docs/04-guides/code-review/Python Code Review Framework v2.md`
- **Base Review Agent Pattern**: `.claude/docs/guides/base-review-agent-pattern.md`
- **Quality Scoring Algorithms**: `.claude/docs/guides/validation/quality-scoring-algorithms.md`
- **Architecture Review Rubric**: `.claude/docs/guides/architecture-scoring-rubric.md`
- **Tech Debt Investigation**: `.claude/agents/tech-debt-investigator.md`
- **Multi-Agent Analysis Pattern**: `.claude/docs/orchestrator-workflow.md`
