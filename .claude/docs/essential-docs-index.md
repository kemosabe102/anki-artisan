# Essential Documentation Index

**Purpose**: Quick reference for orchestrator to find key Claude Code framework documentation.

**Last Updated**: 2025-12-03

---

## Core Frameworks

| File Path | Description | When to Reference |
|-----------|-------------|-------------------|
| `.claude/docs/00-core/ooda-loop-framework.md` | OODA loop decision framework with Context_Quality formulas | Before any task assessment, calculating confidence scores |
| `.claude/docs/00-core/infuse-framework.md` | Comprehensive integration framework | Complex multi-component implementations |
| `.claude/docs/00-core/infuse-framework-quick-ref.md` | Quick reference for INFUSE framework | Fast lookup during implementation |
| `.claude/docs/00-core/research-patterns.md` | Research methodology patterns | When Context_Quality < 0.5, need investigation |
| `.claude/docs/00-core/error-classification-framework.md` | Error categorization and handling | Debugging, failure analysis |
| `.claude/docs/00-core/code-reuse-framework.md` | Code reuse patterns and guidelines | Avoiding duplication, DRY principles |
| `.claude/docs/00-core/technical-debt-frameworks.md` | Technical debt identification and management | Code quality assessment, refactoring decisions |
| `.claude/docs/00-core/development-pytest-framework.md` | Pytest testing patterns | Writing and organizing tests |
| `.claude/docs/00-core/frameworks/README.md` | Complete catalog of thinking frameworks (5 Whys, ReACT, SCAMPER, etc.) | Selecting appropriate reasoning approach for task type |

---

## Agent Guides

| File Path | Description | When to Reference |
|-----------|-------------|-------------------|
| `.claude/docs/01-guides/agents/agent-selection-guide.md` | Domain-first agent selection framework | Choosing which agent for a task |
| `.claude/docs/01-guides/agents/agent-creation-guide.md` | Step-by-step agent creation process | Building new agents |
| `.claude/docs/01-guides/agents/base-agent-pattern.md` | Foundation pattern all agents inherit | Understanding agent structure |
| `.claude/docs/01-guides/agents/base-review-agent-pattern.md` | Pattern for review-type agents | Creating review agents |
| `.claude/docs/01-guides/agents/agent-standards-runtime.md` | Runtime standards auto-loaded at session start | Quick reference for agent behavior |
| `.claude/docs/01-guides/agents/agent-standards-extended.md` | Comprehensive design standards | Deep dive into agent requirements |
| `.claude/docs/01-guides/agents/golden-agent-standards.md` | Excellence criteria for agents | Quality assessment, agent improvement |
| `.claude/docs/01-guides/agents/agent-design-best-practices.md` | Design guidelines and patterns | Agent design decisions |
| `.claude/docs/01-guides/agents/agent-naming-conventions.md` | Naming standards for agents | Creating new agents, renaming |
| `.claude/docs/01-guides/agents/agent-parallelization-strategy.md` | Concurrent execution patterns | Multi-agent coordination |
| `.claude/docs/01-guides/agents/anthropic-prompt-standards.md` | Anthropic prompt engineering standards | Writing agent prompts |
| `.claude/docs/01-guides/agents/agent-categorization.md` | Agent classification system | Understanding agent types |

---

## Workflow Guides

| File Path | Description | When to Reference |
|-----------|-------------|-------------------|
| `.claude/docs/01-guides/file-ops/file-operation-protocol.md` | **CANONICAL** - Complete file operation guide | Any file read/write/edit operation |
| `.claude/docs/01-guides/git/safety-protocols.md` | Git safety rules and banned operations | Before any git operation |
| `.claude/docs/01-guides/git/multi-developer-workflow.md` | Multi-developer git patterns | Collaborative development |
| `.claude/docs/01-guides/commit-message-guide.md` | Commit message conventions | Writing commit messages |
| `.claude/docs/01-guides/testing/testing-failure-categorization.md` | Test failure analysis patterns | Debugging failed tests |
| `.claude/docs/01-guides/testing/testing-flaky-detection.md` | Flaky test identification | Intermittent test failures |
| `.claude/docs/01-guides/review/review-aggregation-logic.md` | Multi-agent review synthesis | Combining review feedback |
| `.claude/docs/01-guides/review/spec-review-guidelines.md` | Specification review standards | Reviewing specs and requirements |
| `.claude/docs/01-guides/delegation-verification-protocol.md` | Agent delegation validation | Verifying agent handoffs |
| `.claude/docs/01-guides/retry-strategies.md` | Error recovery patterns | Handling failures, retries |
| `.claude/docs/01-guides/circuit-breaker-pattern.md` | Fault tolerance patterns | Preventing cascade failures |
| `.claude/docs/01-guides/workflows/todo-management-protocol.md` | Todo tracking guidelines | Task progress management |
| `.claude/docs/01-guides/workflows/automation-guidelines.md` | Automation patterns | Setting up automated workflows |

---

## Infrastructure & Integration

| File Path | Description | When to Reference |
|-----------|-------------|-------------------|
| `.claude/docs/01-guides/infrastructure/observability/monitoring.md` | Monitoring setup guide | Setting up observability |
| `.claude/docs/01-guides/infrastructure/observability/opentelemetry-instrumentation.md` | OpenTelemetry patterns | Tracing, metrics instrumentation |
| `.claude/docs/01-guides/infrastructure/observability/prometheus-api-patterns.md` | Prometheus API usage | Metrics queries |
| `.claude/docs/01-guides/infrastructure/observability/grafana-provisioning-sidecar.md` | Grafana dashboard setup | Dashboard provisioning |
| `.claude/docs/01-guides/infrastructure/deployment/deployment-release-handoff.md` | Kubernetes deployment guide | K8s deployments |
| `.claude/docs/01-guides/integration/mcp.md` | MCP integration guide | Model Context Protocol usage |
| `.claude/docs/01-guides/integration/github-actions.md` | GitHub Actions patterns | CI/CD workflows |

---

## Reference Documentation

| File Path | Description | When to Reference |
|-----------|-------------|-------------------|
| `.claude/docs/02-reference/ARCHITECTURE.md` | Architecture reference | System design decisions |
| `.claude/docs/02-reference/DOC-INDEX.md` | Documentation index | Finding documentation |
| `.claude/docs/02-reference/agent-capability-reference.md` | Agent capabilities matrix | Understanding agent abilities |
| `.claude/docs/02-reference/agent-selection-protocol-reference.md` | Agent selection protocol | Detailed selection rules |
| `.claude/docs/02-reference/implementation-reference.md` | Implementation patterns | Coding standards, patterns |
| `.claude/docs/02-reference/hooks-reference.md` | Hooks system reference | Hook configuration |
| `.claude/docs/02-reference/cli-reference.md` | CLI commands reference | Command line usage |
| `.claude/docs/02-reference/allowed-domains.md` | Allowed external domains | External API access |

---

## Quick Lookup by Task Type

### Starting a New Feature
1. Check project SPEC/README for requirements
2. `.claude/docs/00-core/ooda-loop-framework.md` - Assess context quality
3. `.claude/docs/01-guides/agents/agent-selection-guide.md` - Select appropriate agents

### Debugging Issues
1. `.claude/docs/00-core/error-classification-framework.md` - Classify the error
2. `.claude/docs/00-core/frameworks/README.md` - Select 5 Whys or ReACT
3. `.claude/docs/01-guides/testing/testing-failure-categorization.md` - If test-related

### File Operations
1. `.claude/docs/01-guides/file-ops/file-operation-protocol.md` - **Always read first**
2. `.claude/docs/01-guides/git/safety-protocols.md` - Before any git operations

### Agent Development
1. `.claude/docs/01-guides/agents/agent-creation-guide.md` - Creation process
2. `.claude/docs/01-guides/agents/base-agent-pattern.md` - Foundation pattern
3. `.claude/docs/01-guides/agents/golden-agent-standards.md` - Quality criteria

---

## Document Categories

- **00-core/**: Foundational frameworks (OODA, INFUSE, error handling)
- **01-guides/**: How-to guides organized by topic
- **02-reference/**: Reference documentation and specifications
- **04-examples/**: Example implementations and patterns
- **05-reports/**: Analysis reports and findings
- **archive/**: Historical documentation (rarely needed)

---

## Project-Specific Documentation

For project-specific documentation (specs, architecture, domain logic), see:
- `docs/ESSENTIAL-DOCS.md` - Project-specific essential documentation index
- `docs/README.md` - Project documentation overview
- `CLAUDE.md` - Project orchestration and workflow instructions

---

*This index is maintained by documentation. Report missing or outdated entries.*
