---
title: "Gauntlet Agents: Commit Message Guide"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Gauntlet Agents: Commit Message Guide

A lightweight, practical approach to consistent commit messages for our financial research system development.

## Template Structure

```
<type>(scope): <description>

[optional body with Context7 source references]
[optional LIVING_SPRINT.md progress update]

[optional footer: Closes #123, Breaking-change: details]
```

## Commit Types

Based on GitLab/GitHub industry standards:

- **feat**: New feature implementation
- **fix**: Bug fix or correction
- **refactor**: Code restructuring without behavior change
- **test**: Test additions or improvements
- **docs**: Documentation updates
- **style**: Code formatting, no logic changes
- **perf**: Performance improvements
- **ci**: CI/CD pipeline changes

## Project-Specific Scopes

Use these scopes to identify the component area being changed:

### Core System Components

- **agents**: Agent configuration files (`.claude/agents/*.md`)
- **commands**: Slash command definitions (`.claude/commands/*.md`)
- **hooks**: Automation hook scripts (`.claude/hooks/*.py`)
- **orchestrator**: Main orchestrator logic and coordination
- **planner**: Planning agent and SDD workflow
- **claude-code**: Claude Code platform integration

### Application Components

- **core**: Core packages and shared utilities (`packages/core/`)
- **api**: API service endpoints (`services/api/`)
- **cli**: Command-line interface (`cli/`)
- **workers**: Financial research workers (`workers/`)
- **models**: Data models and schemas (`domain/models/`)
- **connectors**: External API integrations (`packages/core/connectors/`)

### Development & Operations

- **scripts**: Development and deployment scripts (`scripts/`)
- **deployment**: Kubernetes configs and deployment (`deployment/`)
- **tests**: Test suites and testing infrastructure
- **ci**: CI/CD pipelines and automation
- **monitoring**: Observability and metrics (`scripts/monitoring/`)

### Documentation & Planning

- **docs**: Project documentation (`docs/`)
- **specs**: Feature specifications (`docs/01-planning/specifications/`)
- **plans**: Implementation plans and roadmaps
- **guides**: Development guides and standards

## Examples

### Feature Development

```
feat(core): Add financial data validation pipeline

Implement comprehensive validation for SEC filing data including:
- Schema validation using Pydantic models
- Data quality checks for missing fields
- Business rule validation for financial ratios

Context7 sources: pydantic/pydantic validation patterns
Update LIVING_SPRINT.md: Mark data validation chunk completed

Closes #142
```

### Agent Configuration

```
feat(agents): Add market analysis agent configuration

New specialized agent for equity market analysis with:
- Technical analysis capabilities
- Market sentiment processing
- Risk assessment workflows

Uses sonnet model for efficient execution
```

### Bug Fixes

```
fix(connectors): Handle SEC API rate limit errors

Add exponential backoff retry logic to SEC connector:
- Detect 429 rate limit responses
- Implement jittered exponential backoff
- Log retry attempts for monitoring

Context7 sources: requests retry patterns
```

### Documentation

```
docs(guides): Update agent coordination patterns

Clarify sub-agent delegation protocols:
- Main agent coordination requirements
- Context passing standards
- Error handling patterns

Addresses feedback from code review #156
```

### Infrastructure

```
ci(deployment): Add Kubernetes health check validation

Enhance deployment pipeline with:
- Pod readiness probe validation
- Service endpoint connectivity tests
- Database migration verification

Update LIVING_SPRINT.md: Infrastructure reliability chunk completed
```

### Testing

```
test(workers): Add integration tests for earnings analysis

Comprehensive test suite for earnings worker:
- Mock external API responses
- Test data transformation pipeline
- Validate output schema compliance

Context7 sources: pytest integration testing patterns
```

### Performance

```
perf(api): Optimize financial report generation

Reduce report generation time from 45s to 12s:
- Implement concurrent data fetching
- Add response caching layer
- Optimize database queries

Closes #203, improves SLO compliance
```

### Refactoring

```
refactor(orchestrator): Extract phase validation logic

Improve code organization by:
- Moving phase gate logic to dedicated module
- Standardizing validation interfaces
- Reducing orchestrator complexity

No functional changes, improves maintainability
```

## Context7 Integration

When commit includes research-based decisions, reference Context7 sources:

```
feat(connectors): Implement OpenAI streaming responses

Add streaming support for real-time analysis:
- Async iterator pattern for token streaming
- Error handling for connection drops
- Backpressure management

Context7 sources: openai/openai-python streaming patterns
WebSearch fallback: OpenAI streaming best practices 2025
```

## LIVING_SPRINT.md Updates

Always include sprint progress updates for feature work:

```
feat(core): Complete risk assessment calculation engine

Implementation includes:
- Monte Carlo simulation for portfolio risk
- VaR calculation with multiple confidence levels
- Stress testing scenarios

Update LIVING_SPRINT.md: Mark risk engine chunk completed, advance to reporting integration
Context7 sources: numpy/scipy statistical computing patterns

Closes #178
```

## Best Practices

### Keep It Focused

- One logical change per commit
- Atomic commits that don't break functionality
- Clear, actionable descriptions

### Be Specific

- Avoid vague terms like "fix stuff" or "update code"
- Include specific components changed
- Mention key implementation details

### Reference Standards

- Include Context7 sources when using researched patterns
- Reference issues/PRs for traceability
- Note breaking changes explicitly

### Sprint Integration

- Always update LIVING_SPRINT.md for feature work
- Mark completed chunks and advance todo items
- Connect commits to sprint progress

## Usage with Scripts

Our code review preparation script automatically stages relevant files:

```bash
# The script will help you identify the right scope and files
uv run python scripts/prepare-code-review.py --stage-changes

# Then commit using this guide's patterns
git commit -m "feat(api): Add real-time market data streaming

Implement WebSocket endpoint for live market updates:
- Real-time price feeds from multiple exchanges
- Client subscription management
- Rate limiting and connection handling

Update LIVING_SPRINT.md: Complete real-time data chunk
Context7 sources: fastapi/fastapi WebSocket patterns"
```

This guide ensures consistent, informative commit messages that support our Context7-guided development workflow and sprint tracking requirements.
