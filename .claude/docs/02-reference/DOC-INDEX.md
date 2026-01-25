---
title: Documentation Index
date: 2025-01-12
status: ACTIVE
tags: [reference, documentation]
---

## Documentation Index

**Quick Links**: See `CLAUDE.md` Essential Docs section for Top 10 most-used documents

**Purpose**: Comprehensive categorized listing of all documentation across Claude Code ecosystem (`.claude/docs/**`) and Gauntlet Agents project (`docs/**`)

---

## 🏗️ Project Foundation

### Core Specifications

- **SPEC.md** (`docs/00-project/`) - Complete system design and core principles

- **COMPONENT_ALMANAC.md** (`docs/00-project/`) - **CHECK BEFORE NEW CODE** - Existing components and patterns

- **README.md** (`docs/00-project/`) - Project overview and getting started

### Operations & Planning

- **LIVING_SPRINT.md** (`docs/00-project/operations/`) - Current sprint status, active work, complexity tracking

- **PLANNING-GUIDE.md** (`docs/00-project/operations/`) - How to create specifications and plans

- **MATURITY-MATRIX.md** (`docs/00-project/strategy/`) - Component maturity scoring

### Templates

- **living-sprint-template.md** (`docs/00-project/templates/`) - Living sprint structure template

- **plan-template.md** (`docs/00-project/templates/`) - Implementation plan template

- **spec-template.md** (`docs/00-project/templates/`) - Specification document template

### Strategy & Analysis

- **customer-pain-points-external.md** (`docs/00-project/`) - External customer pain points analysis

- **customer-pain-points-internal.md** (`docs/00-project/`) - Internal developer pain points

- **critical-feedback-analysis-context.md** (`docs/00-project/`) - Feedback analysis context

- **roadmap-readiness-matrix.md** (`docs/00-project/`) - Roadmap planning readiness assessment

- **context-monitoring-investigation-report.md** (`docs/00-project/`) - Context monitoring research findings

### Roadmaps

- **Q2-Q3-2026.md** (`docs/00-project/roadmaps/active/`) - Active roadmap for Q2-Q3 2026

- **ROADMAP-Q4-2025-Q1-2026-COMBINED.md** (`docs/archive/roadmaps/`) - Previous combined roadmap (archived)

---

## 🎯 Architecture & Design

### System Architecture

- **ARCHITECTURE.md** (`docs/02-architecture/`) - System architecture, design patterns (Gauntlet system)

- **ARCHITECTURE.md** (`.claude/docs/`) - Agent architecture, design principles (Claude Code)

- **WORKFLOW.md** (`.claude/docs/`) - Workflow execution patterns

### Design Patterns

- **lightweight-error-budget.md** (`docs/02-architecture/design/`) - Error budget framework

- **mvp-documentation-summary.md** (`docs/02-architecture/design/`) - MVP documentation summary

- **reportwriter-boundaries.md** (`docs/02-architecture/design/`) - Report writer component boundaries

- **state-management-patterns.md** (`docs/03-implementation/components/`) - State management design patterns

### Architecture Decision Records (ADRs)

- **README.md** (`docs/02-architecture/decisions/`) - ADR index and overview

- **adr-template.md** (`docs/02-architecture/decisions/`) - ADR template

- **adr-001-llm-module-consolidation.md** - LLM module consolidation decision

- **adr-002-multi-api-fallback-strategy.md** - Multi-API fallback strategy

- **adr-003-resilient-data-provider-implementation.md** - Resilient data provider design

- **adr-004-dataconnector-protocol.md** - Data connector protocol

- **adr-005-company-profile-data-model.md** - Company profile data model

- **adr-005-local-production-environment.md** - Local production environment setup

- **adr-006-investment-thesis-synthesis-engine.md** - Investment thesis synthesis engine

- **adr-007-key-financial-ratios-architecture.md** - Financial ratios architecture

- **adr-009-quantitative-analysis-pipeline-consolidation.md** - Quantitative analysis pipeline

- **adr-010-advanced-agent-orchestration-architecture.md** - Advanced agent orchestration

### Research & Analysis

- **existing-components-audit.md** (`docs/02-architecture/research/`) - Existing components audit

---

## 🤖 Agent Development

### Core Agent Standards

- **orchestrator-workflow.md** (`.claude/docs/`) - Agent coordination, delegation patterns, maturity tracking

- **agent-capability-reference.md** (`.claude/docs/02-reference/`) - Comprehensive 30+ agent capability catalog, research patterns, delegation strategies (Progressive Disclosure Level 2)

- **agent-selection-protocol-reference.md** (`.claude/docs/02-reference/`) - Complete DCS methodology, multi-agent decisions, verification-first protocol, performance heuristics (Progressive Disclosure Level 2)

- **code-reuse-workflow-integration.md** (`.claude/docs/03-workflows/`) - Component Almanac workflow, extend vs replace matrices, cleanup task specs, ROI formulas (Progressive Disclosure Level 2)

- **agent-performance-reference.md** (`.claude/docs/02-reference/`) - Performance tiers (Fast/Medium/Slow), optimization results (planning, architecture), delegation strategy (Progressive Disclosure Level 2)

- **parallel-execution-protocol.md** (`.claude/docs/03-workflows/`) - Parallel vs sequential execution patterns, .claude/ constraints, scaling limits, performance metrics (Progressive Disclosure Level 2)

- **planning-workflow-patterns.md** (`.claude/docs/03-workflows/`) - 7-phase development lifecycle, optimized planning flow, code reuse integration, coordination protocols (Progressive Disclosure Level 2)

- **agent-standards-extended.md** (`.claude/docs/`) - Comprehensive agent design standards

- **agent-standards-runtime.md** (`.claude/docs/`) - Runtime behavior and contracts

### Agent Patterns & Templates

- **base-agent-pattern.md** (`.claude/docs/01-guides/agents/`) - Standard agent structure

- **base-review-agent-pattern.md** (`.claude/docs/01-guides/agents/`) - Review agent template

- **agent-design-best-practices.md** (`.claude/docs/01-guides/agents/`) - Prompt engineering, tool selection

- **infuse-framework-quick-ref.md** (`.claude/docs/00-core/`) - INFUSE framework 30-second reference (Identity, Navigation, Flow, User Guidance, Signals, End Instructions) - **USE FOR ALL AGENT CREATION**

- **infuse-framework.md** (`.claude/docs/00-core/`) - Complete INFUSE methodology for structured agent prompt engineering with 6 components, academic validation, integration strategy, best practices

- **agent-optimization-lessons-learned.md** (`.claude/docs/01-guides/agents/`) - Practical optimization lessons

- **secure-agent-template.md** (`docs/04-guides/templates/`) - Security-focused agent template

### Agent Management

- **agent-naming-conventions.md** (`.claude/docs/01-guides/agents/`) - Agent naming standards

- **agent-categorization.md** (`.claude/docs/01-guides/agents/`) - Agent categorization system

- **agent-descriptions-update.md** (`.claude/docs/01-guides/agents/`) - Agent description maintenance

- **agent-parallelization-strategy.md** (`.claude/docs/01-guides/agents/`) - Multi-agent delegation patterns

### Agent-Specific Guides

#### repository-analyst

- **development-workflows.md** (`.claude/docs/guides/repository-analyst/`) - 5-phase discovery workflow (Discovery → Extract → Categorize → Validate → Generate), multi-format outputs, error recovery patterns

- **domain-knowledge.md** (`.claude/docs/guides/repository-analyst/`) - YAML frontmatter parsing, component categorization taxonomies (OODA/domain/type/maturity), repository organization standards

- **integration-patterns.md** (`.claude/docs/guides/repository-analyst/`) - Orchestrator delegation, multi-agent coordination (claude-code-ecosystem, documentation, context-optimizer), advisory role patterns

#### sentiment-nlp-specialist

- **domain-knowledge.md** (`.claude/docs/guides/sentiment-nlp-specialist/`) - Financial NLP domain expertise, sentiment analysis frameworks, text processing patterns

- **development-workflows.md** (`.claude/docs/guides/sentiment-nlp-specialist/`) - NLP pipeline development, model integration, validation workflows

- **testing-strategy.md** (`.claude/docs/guides/sentiment-nlp-specialist/`) - NLP testing frameworks, model validation, benchmark datasets

- **security-patterns.md** (`.claude/docs/guides/sentiment-nlp-specialist/`) - Text sanitization, prompt injection prevention, model security

#### pattern-detector

- **domain-knowledge-pattern-detection.md** (`.claude/docs/01-guides/pattern-detector/`) - Breakout, Pullback, PEAD, Divergence pattern frameworks, structure validation, volume confirmation

- **domain-knowledge-confidence-scoring.md** (`.claude/docs/01-guides/pattern-detector/`) - Evidence weighting methodology, multi-signal aggregation, threshold calibration

- **development-workflows-detector-implementation.md** (`.claude/docs/01-guides/pattern-detector/`) - 6-phase OODA loop implementation workflow, feature engineering, pattern matching, validation

- **development-workflows-multi-pattern-resolution.md** (`.claude/docs/01-guides/pattern-detector/`) - Conflict resolution framework, directional conflicts, weighted voting, pattern hierarchy

- **testing-edge-cases.md** (`.claude/docs/01-guides/pattern-detector/`) - Edge case taxonomy (missing data, extreme values, regime changes), testing strategies

- **testing-performance-optimization.md** (`.claude/docs/01-guides/pattern-detector/`) - Vectorization, caching, computational efficiency, profiling workflows

#### risk-management-specialist

- **position-sizing-methodology.md** (`.claude/docs/guides/risk-management-specialist/`) - Van Tharp R-Multiple position sizing, ATR-based Chandelier stops, portfolio heat management, fixed fractional methodology

- **chandelier-stop-methodology.md** (`.claude/docs/guides/risk-management-specialist/`) - ATR-based trailing stops, Chandelier exit calculation (long/short), parameter selection, lookback period optimization

- **circuit-breaker-pattern.md** (`.claude/docs/guides/risk-management-specialist/`) - Four-state circuit breaker (NORMAL/WARNING/CRITICAL/BREAKER), session-based resets, daily loss limits (-3% threshold), graduated risk controls

- **atr-integration-patterns.md** (`.claude/docs/guides/risk-management-specialist/`) - ATR delegation to technical-indicator-specialist, caching strategies, NaN handling, Wilder's smoothing methodology

- **volatility-regime-detection.md** (`.claude/docs/guides/risk-management-specialist/`) - Percentile-based regime classification (LOW/NORMAL/HIGH), risk adjustment multipliers, 252-day lookback windows (Post-MVP)

### Agent Research & Templates

- **agent-research-template.md** (`docs/04-guides/templates/`) - Research phase template

- **agent-design-template.md** (`docs/04-guides/templates/`) - Design phase template

- **agent2agent_protocol_and_self_optimizing_prompts.md** (`docs/04-guides/domain/agents/`) - Agent communication protocols

- **Anthropic Multi-Agent Research System.md** (`docs/04-guides/domain/agents/`) - Anthropic research patterns

- **Agents vs. Workflows Research Plan\_.md** (`docs/04-guides/domain/agents/`) - Agents vs workflows comparison

### Context & Prompt Engineering

- **Context Management in AI Agents.md** (`docs/04-guides/domain/agents/`) - Context management strategies

- **Context-Management-Best-Practices.md** (`docs/04-guides/domain/agents/`) - Context best practices

- **Context-Optimization-Analysis-Report.md** (`docs/04-guides/domain/agents/`) - Context optimization analysis

- **prompt-engineering-research-analysis.md** (`docs/04-guides/domain/agents/`) - Prompt engineering research

- **prompt-engineering-lifecycle-analysis.md** (`docs/04-guides/domain/agents/`) - Prompt lifecycle management

- **prompt-engineering-standards-and-practices.md** (`docs/04-guides/domain/agents/`) - Prompt standards

### Agent Reports & Analysis

- **../archive/research/2025/01-january/2025-01-09-agent-best-practices-research.md** (`.claude/docs/01-guides/agents/`) - Agent best practices research

- **../archive/research/2025/01-january/2025-01-25-agent-performance-optimization-plan.md** (`.claude/docs/01-guides/`) - Performance optimization plan

- **2025-09-21-164500-claude-code-ecosystem-workflow-improvements.md** (`.claude/docs/03-workflows/`) - Agent architect improvements

- **2025-09-21-workflow-agent-creation-report.md** (`.claude/docs/03-workflows/`) - Workflow agent creation

- **architecture-agent-creation-report.md** (`.claude/docs/05-reports/`) - Architecture review agent creation

- **architecture-creation-report.md** (`.claude/docs/05-reports/`) - Architecture enhancer creation

---

## 🔍 Research & Analysis

### Research Patterns

- **research-patterns.md** (`.claude/docs/00-core/`) - Research delegation strategies

- **research-methodology.md** (`.claude/docs/01-guides/research/`) - Research best practices

---

## 🏗️ Infrastructure & Deployment

### Deployment

- **deployment-release-handoff.md** (`.claude/docs/01-guides/infrastructure/deployment/`) - Kubernetes deployment handoff guide

- **deployment-release-quality-evaluation.md** (`.claude/docs/01-guides/infrastructure/deployment/`) - K8s deployment quality checklist

### Observability

- **monitoring.md** (`.claude/docs/01-guides/infrastructure/observability/`) - Monitoring strategy and patterns

- **opentelemetry-instrumentation.md** ⚠️ (`.claude/docs/01-guides/infrastructure/observability/`) - Complete OpenTelemetry Python SDK guide (referenced by 3 agents)

- **telemetry-disambiguation.md** ⚠️ (`.claude/docs/01-guides/infrastructure/observability/`) - When to use OpenTelemetry SDK vs telemetrygen (referenced by 3 agents)

- **telemetrygen-usage.md** ⚠️ (`.claude/docs/01-guides/infrastructure/observability/`) - telemetrygen CLI and K8s Job patterns (referenced by 2 agents)

- **grafana-provisioning-sidecar.md** (`.claude/docs/01-guides/infrastructure/observability/`) - Grafana sidecar pattern

- **grafana-dashboard-builder-quality-evaluation.md** (`.claude/docs/01-guides/infrastructure/observability/`) - Dashboard quality checklist

- **intent-to-metric-mapping.md** (`.claude/docs/01-guides/infrastructure/observability/`) - Convert monitoring intents to metrics

- **prometheus-api-patterns.md** (`.claude/docs/01-guides/infrastructure/observability/`) - Prometheus API usage patterns

---

### MCP Integration

- **mcp-agent-optimization.md** (`.claude/docs/`) - Context7 token optimization, agent patterns

- **integration-guide.md** (`docs/03-implementation/integrations/mcp/`) - Project setup, authentication

- **Building Subscription-Based MCP Servers - Architecture, Orchestration, and Best Practices.md** (`docs/04-guides/domain/`) - MCP server design

### Technical Research

- **planning-research-guides.md** (`.claude/docs/01-guides/research/`) - Technical PM research patterns

- **researcher-web-optimization-spec.md** (`docs/01-planning/custom/`) - Researcher-web optimization specification [deprecated - see researcher-external]

---

## ⚡ Performance & Parallelization

### Tool & Agent Parallelization

- **tool-parallelization-patterns.md** (`.claude/docs/01-guides/performance/`) - Read/Grep/Write efficiency

- **agent-parallelization-strategy.md** (`.claude/docs/01-guides/agents/`) - Multi-agent delegation patterns

- **parallel-execution-patterns.md** (`.claude/docs/01-guides/performance/`) - General parallel execution strategies

### Error Handling & Resilience

- **error-classification-framework.md** (`.claude/docs/00-core/`) - Error categorization system (retryable vs permanent, severity scoring)

- **circuit-breaker-pattern.md** (`.claude/docs/01-guides/`) - Circuit breaker implementation for service protection

- **retry-strategies.md** (`.claude/docs/01-guides/`) - Exponential backoff, jitter, retry budgets

### Context & Token Management

- **context-monitoring-guide.md** (`.claude/docs/01-guides/`) - Complete context monitoring with token usage tracking and hook configuration

- **doc-optimization-methodology.md** (`.claude/docs/01-guides/documentation/`) - Documentation optimization methodology

### File Operations

- **file-operation-protocol.md** (`.claude/docs/01-guides/file-ops/`) - **CANONICAL FILE OPERATIONS GUIDE** - Complete file operation protocol with decision trees, script usage, troubleshooting, flags reference, and platform-specific guidance (consolidates all file-ops documentation)

- **file-ops-script-guide.md** (`.claude/docs/01-guides/file-ops/`) - ⚠️ **DEPRECATED** (2025-11-18) - Use file-operation-protocol.md instead

- **file-ops-flags.md** (`.claude/docs/02-reference/`) - ⚠️ **DEPRECATED** (2025-11-18) - Use file-operation-protocol.md instead

- **file-ops-platform-issues.md** (`.claude/docs/02-reference/`) - ⚠️ **DEPRECATED** (2025-11-18) - Use file-operation-protocol.md instead

---

## 📋 Planning & Development

### Spec-Driven Development

- **spec-driven-development.md** (`docs/04-guides/development/`) - SDD methodology and workflow

- **planning-phase-workflow.md** (`docs/04-guides/development/`) - Planning phase execution

- **implementation-phase-workflow.md** (`docs/04-guides/development/`) - Implementation phase execution

- **development-workflow.md** (`docs/04-guides/development/`) - General development workflow

### Delegation & Orchestration

- **proactive-research-workflow.md** (`docs/04-guides/development/`) - Auto-delegation triggers

- **orchestrator-delegation.md** (`docs/04-guides/development/`) - Orchestrator delegation patterns

- **confidence-based-delegation-framework.md** (`docs/01-planning/custom/`) - DCS scoring framework

- **ooda-loop-framework.md** (`.claude/docs/00-core/`) - Complete OODA Loop methodology (Observe-Orient-Decide-Act), Context_Quality assessment, gate definitions, research depth scoping

- **orchestrator-refinement-plan-v4.5.md** (`docs/01-planning/custom/`) - Orchestrator refinement plan

### Planning Frameworks

- **strategic-planning-relationships.md** (`.claude/docs/01-guides/planning/`) - Planning workflows

- **feature-artifact-structure.md** (`.claude/docs/01-guides/`) - Spec/plan/task organization

- **development-sequencing-guide.md** (`.claude/docs/01-guides/planning/`) - Development sequencing strategies

- **cost-analysis-framework.md** (`.claude/docs/00-core/`) - Cost analysis methodology

- **risk-assessment-matrix.md** (`.claude/docs/01-guides/planning/`) - Risk assessment framework

- **roi-calculation-guide.md** (`.claude/docs/01-guides/planning/`) - ROI calculation methodology

- **technical-debt-frameworks.md** (`.claude/docs/00-core/`) - SQALE/SIG methodologies, TDR calculation, debt scoring, hotspot detection, principal vs interest analysis

- **code-reuse-framework.md** (`.claude/docs/00-core/`) - Code reuse strategies

### Feature Specifications

- **001-regenerative-system/SPEC.md** (`docs/01-planning/specifications/`) - Regenerative system specification

- **002-executable-task-system/SPEC.md** (`docs/01-planning/specifications/`) - Executable task system specification

- **003-multi-agent-research/SPEC.md** (`docs/01-planning/specifications/`) - Multi-agent research specification

- **012-regenerative-sdlc/SPEC.md** (`docs/01-planning/specifications/`) - Regenerative SDLC specification

### Feature Planning (Active)

- **005-regenerative-orchestration-system/README.md** (`docs/01-planning/features/`) - Feature 005 overview

- **005-regenerative-orchestration-system/RATIONALE.md** - Feature rationale and goals

- **005-regenerative-orchestration-system/plans/phase-1-ooda-framework.md** - Phase 1 OODA implementation plan

- **005-regenerative-orchestration-system/plans/phase-2-workflows-../01-guides/infrastructure/observability/monitoring.md** - Phase 2 workflows and monitoring

- **005-regenerative-orchestration-system/plans/phase-3-learning-system.md** - Phase 3 learning system

- **006-opentelemetry-monitoring-infrastructure/README.md** - OpenTelemetry monitoring feature

- **006-opentelemetry-monitoring-infrastructure/plans/001-infrastructure-foundation-PLAN.md** - Infrastructure foundation plan

- **006-opentelemetry-monitoring-infrastructure/plans/002-validation-testing-PLAN.md** - Validation testing plan

- **006-opentelemetry-monitoring-infrastructure/plans/003-claude-code-monitoring-PLAN.md** - Claude Code monitoring plan

- **007-claude-sdk-migration/README.md** - Claude SDK migration feature

- **007-claude-sdk-migration/plans/001-provider-integration-PLAN.md** - Provider integration plan

- **007-claude-sdk-migration/plans/002-validation-testing-PLAN.md** - Validation testing plan

- **007-claude-sdk-migration/plans/003-canary-rollout-PLAN.md** - Canary rollout plan

- **007-claude-sdk-migration/plans/004-gemini-deprecation-PLAN.md** - Gemini deprecation plan

- **007-claude-sdk-migration/plans/005-cost-optimization-PLAN.md** - Cost optimization plan

### Feature Reference Materials

- **005-regenerative-orchestration-system/reference/context-quality-formula.md** - Context quality calculation

- **005-regenerative-orchestration-system/reference/dcs-formula-components.md** - DCS formula components

- **005-regenerative-orchestration-system/reference/ooda-phase-definitions.md** - OODA phase definitions

- **005-regenerative-orchestration-system/reference/agent-ooda-mapping.md** - Agent-to-OODA mapping

- **005-regenerative-orchestration-system/reference/operational-reliability-patterns.md** - Reliability patterns

- **005-regenerative-orchestration-system/reference/simplicity-ladder-specification.md** - Simplicity ladder framework

- **005-regenerative-orchestration-system/reference/workflow-patterns.md** - Workflow patterns reference

- **005-regenerative-orchestration-system/reference/agent-testing-roadmap.md** - Agent testing roadmap

- **006-opentelemetry-monitoring-infrastructure/reference/current-deployment-analysis.md** - Current deployment state

- **007-claude-sdk-migration/reference/research-findings.md** - SDK migration research

- **007-claude-sdk-migration/reference/cost-analysis.md** - Migration cost analysis

- **007-claude-sdk-migration/roadmap/post-mvp-enhancements.md** - Post-MVP enhancement roadmap

---

## 🔧 Tools & Workflows

### Tool Design

- **tool-design-patterns.md** (`.claude/docs/01-guides/tools/`) - Tool architecture and design

- **AI Agent Tool Design and Agent-Tool Interactions.md** (`.claude/docs/01-guides/`) - Tool interaction patterns

### Workflow Management

- **agent-analysis-suite-protocol.md** (`.claude/docs/03-workflows/`) - Standard workflow for multi-agent analysis using 4 core agents (claude-code-ecosystem, claude-code-ecosystem, documentation, tech-debt-investigator) with parallel launch patterns and synthesis methodology

- **automation-guidelines.md** (`.claude/docs/03-workflows/`) - Automation best practices

- **developer-usage-guide.md** (`.claude/docs/03-workflows/`) - Developer workflow guide

- **rollback-strategy.md** (`.claude/docs/03-workflows/`) - Workflow rollback strategies

- **tech-debt-delegation-guide.md** (`.claude/docs/03-workflows/`) - Complete guide for delegating to tech-debt-investigator with 5 delegation patterns, context metadata templates, output interpretation (debt_score, TDR, SQALE, SIG), and best practices

- **workflow-integration-map.md** (`.claude/docs/03-workflows/`) - Workflow integration mapping

- **workflow-patterns.md** (`.claude/docs/03-workflows/`) - Common workflow templates

- **workflow-registry.md** (`.claude/docs/03-workflows/`) - Available workflows catalog

### Documentation Management

- **documentation-context-loading.md** (`.claude/docs/01-guides/documentation/`) - Documentation loading strategies

- **doc-update-strategy.md** (`.claude/docs/01-guides/documentation/`) - Documentation update approach

- **doc-health-synthesis-framework-2025-10-31.md** (`.claude/docs/00-core/`) - Documentation health assessment methodology, orphan rate analysis, link health scoring, progressive disclosure validation

- **DOCS-MANAGEMENT.md** (`docs/`) - Documentation management guidelines

### Plugin Distribution & Marketplace

- **marketplace-setup.md** (`docs/04-guides/marketplace/`) - Private marketplace setup and configuration

- **plugin-repository-setup.md** (`docs/04-guides/marketplace/`) - Plugin repository structure and setup guide

### Git & GitHub

- **commit-message-guide.md** (`.claude/docs/01-guides/`) - Commit message standards

- **branch-management.md** (`docs/04-guides/claude-code/`) - Branch management strategies

---

## 👥 Review & Quality

### Review Workflows

- **planning-procedures.md** (`.claude/docs/01-guides/review/`) - Business alignment review

- **planning-usage-guide.md** (`.claude/docs/01-guides/review/`) - Technical PM usage patterns

- **architecture-integration-guide.md** (`.claude/docs/01-guides/architecture/`) - Technical validation

- **architecture-integration-enhancement.md** (`.claude/docs/01-guides/architecture/`) - Architecture review enhancements

- **spec-review-guidelines.md** (`.claude/docs/01-guides/review/`) - Specification quality review

- **review-aggregation-logic.md** (`.claude/docs/01-guides/review/`) - Multi-reviewer synthesis (formal reviews with JSON schemas)

- **synthesis-and-recommendation-framework.md** (`.claude/docs/00-core/`) - Consolidate overlapping multi-agent findings into prioritized recommendations (overlap detection, trade-off scoring, impact/effort analysis)

### Architecture Review Framework

- **architecture-success-criteria.md** (`.claude/docs/01-guides/architecture/`) - Architecture review success metrics

- **architecture-traceability-guide.md** (`.claude/docs/01-guides/architecture/`) - Traceability requirements

- **architecture-stage-policies.md** (`.claude/docs/01-guides/architecture/`) - Stage-specific policies

- **architecture-scoring-rubric.md** (`.claude/docs/01-guides/architecture/`) - Scoring rubric

- **architecture-slo-sli-framework.md** (`.claude/docs/00-core/`) - SLO/SLI framework

- **architecture-examples.md** (`.claude/docs/01-guides/architecture/`) - Review examples

### Code Review Standards

- **python-code-review-checklist.md** (`docs/04-guides/code-review/`) - Quick-reference checklist for Python code reviews (PRIMARY ENTRY POINT)

- **python-security-patterns.md** (`docs/04-guides/code-review/`) - Security patterns for path traversal, command injection, ReDoS mitigation

- **python-exception-handling.md** (`docs/04-guides/code-review/`) - Exception handling best practices and resource management

- **python-testing-standards.md** (`docs/04-guides/code-review/`) - Testing standards with AAA pattern and security tests

- **python-type-safety.md** (`docs/04-guides/code-review/`) - Type hints requirements and Pydantic usage

- **python-performance-patterns.md** (`docs/04-guides/code-review/`) - Performance optimization patterns

- **Code Testability.md** (`docs/04-guides/code-review/`) - Code testability guidelines

- **coding-guidelines.md** (`docs/04-guides/code-review/`) - General coding standards

- **oop-design-patterns-code-review.md** (`docs/04-guides/code-review/`) - OOP design patterns, SOLID principles, anti-patterns

- **Dependency Injection & Principles of Modular Design.md** (`docs/04-guides/code-review/`) - DI and modularity

- **Dynamic Programming Best Practices Guide.md** (`docs/04-guides/code-review/`) - Dynamic programming patterns

- **feedback-log.md** (`docs/04-guides/code-review/`) - Code review feedback log

### Validation & Quality

- **validation-rubrics.md** (`.claude/docs/01-guides/review/`) - Validation rubrics framework

- **quality-scoring-algorithms.md** (`.claude/docs/01-guides/`) - Quality scoring algorithms

- **review-troubleshooting-framework.md** (`.claude/docs/00-core/`) - Review failure diagnosis, root cause analysis, remediation patterns, quality gate troubleshooting

- **task-quality-validation-workflow.md** (`.claude/docs/03-workflows/`) - Task quality validation

- **../05-reports/refactoring-validation-summary.md** (`.claude/docs/01-guides/review/`) - Refactoring validation summary

### Task Management

- **task-quality-validation-workflow.md** (`.claude/docs/03-workflows/`) - Task validation workflow

- **pain-point-validation-guide.md** (`docs/04-guides/templates/`) - Pain point validation methodology

---

## 🧪 Testing

### Test Architecture

- **code-quality guides** (`.claude/docs/01-guides/testing/`) - Test execution specialist
  - `README.md` - Guide overview and quick reference (0.92 confidence)

  - `development-pytest-framework.md` - pytest execution, exit codes, output formats

  - `testing-failure-categorization.md` - 12-heuristic automated failure classification

  - `testing-flaky-detection.md` - N-run validation, indicator detection, quarantine strategies

  - `development-delegation-patterns.md` - Multi-agent coordination and delegation routing

### Test Agent Documentation

- `code-quality.md` (`.claude/agents/`) - Execution + categorization + delegation specialist

- `code-quality.md` (`.claude/agents/`) - Test generation + coverage analysis specialist

- `test-runner.md` (`.claude/agents/`) - [DEPRECATED] Historical reference only

### Schema Documentation

- `code-quality.schema.json` (`.claude/docs/schemas/`) - Test execution output contract

- `code-quality.schema.json` (`.claude/docs/schemas/`) - Test generation output contract

---

## 🔐 Security & Compliance

### Security Policies

- **README.md** (`.claude/docs/security/`) - Security overview and policies
- **tool-security-best-practices.md** (`.claude/docs/01-guides/security/`) - OWASP-compliant security patterns for production tool implementations (8 patterns, OWASP Top 10 2021 + LLM 2025 mappings, 1200+ lines)
- **allowed-domains.md** (`.claude/docs/security/`) - WebFetch/WebSearch whitelist

- **allowed-domains.md** (`.claude/docs/`) - Duplicate/legacy allowed domains reference

---

## 🛠️ Operations & Troubleshooting

### Setup & Configuration

- **SETUP.md** (`.claude/docs/`) - Initial setup and configuration

- **SETUP-GUIDE.md** (`docs/03-implementation/infrastructure/`) - Infrastructure setup guide

- **LOCAL-DEPLOYMENT-STRATEGY.md** (`docs/03-implementation/infrastructure/`) - Local deployment strategy

- **KUBERNETES.md** (`.claude/docs/`) - Deployment and infrastructure

- **Kubernetes Workflows\_ Kustomize & Troubleshooting.md** (`docs/04-guides/kubernetes/`) - Kubernetes operational guide

- **kubernetes-troubleshooting.md** (`docs/03-implementation/infrastructure/ci-cd/`) - Kubernetes troubleshooting

### Session Management

- **session-management.md** (`docs/04-guides/claude-code/`) - Claude Code session management

- **../archive/research/2025/09-september/2025-09-22-startup-data-loading-investigation.md** (`.claude/docs/01-guides/`) - Startup data loading investigation

### Troubleshooting & Best Practices

- **troubleshooting-guide.md** (`docs/04-guides/claude-code/`) - General troubleshooting guide

- **best-practices-checklist.md** (`docs/04-guides/claude-code/`) - Best practices checklist

- **agent-duplication-issues.md** (`docs/04-guides/claude-code/`) - Agent duplication troubleshooting

- **codebase-navigation-guide.md** (`docs/04-guides/claude-code/`) - Codebase navigation patterns

- **README.md** (`docs/04-guides/claude-code/`) - Claude Code operational overview

### Observability & Monitoring

- **OpenTelemetry-Observability-Strategy.md** (`docs/03-implementation/infrastructure/observability/`) - OpenTelemetry strategy

- **E2E-TEST-PLAN.md** (`docs/03-implementation/infrastructure/`) - End-to-end testing plan

#### Observability Stack Troubleshooting Guides

- **jaeger-troubleshooting.md** (`docs/04-guides/observability/`) - Jaeger v2 configuration, ConfigMap mounting, Badger storage, OTLP receivers, trace persistence issues

- **otel-collector-troubleshooting.md** (`docs/04-guides/observability/`) - Memory limiter, batch processor, GOMEMLIMIT tuning, failure modes, debugging tools

- **prometheus-troubleshooting.md** (`docs/04-guides/observability/`) - Storage retention, PersistentVolume configuration, scrape targets, capacity planning

- **grafana-troubleshooting.md** (`docs/04-guides/observability/`) - Data source provisioning (Prometheus/Jaeger), connection troubleshooting, dashboard persistence

#### PromQL Query Construction & Optimization

- **query-construction-patterns.md** (`docs/04-guides/promql-query-builder/`) - PromQL query patterns, cardinality management, recording rules
  - **Label Cardinality Management**: Prevent metric explosion, cardinality thresholds, low vs high-cardinality labels
  - **Recording Rules**: Pre-computed queries, naming conventions, evaluation intervals, complexity triggers
  - **Time-Period Comparisons**: Offset patterns (1h, 24h, 7d, 30d), percentage change calculations, missing data handling
  - **Workflows**: Cardinality audit & remediation, recording rule creation & deployment, time-period comparison alerts
  - **Best Practices**: Route templates, reusable aggregations, naming conventions, missing data strategies
  - **Anti-Patterns**: High-cardinality labels, over-optimization with recording rules, hardcoded offset durations

- **signal-detection-guide.md** (`docs/04-guides/promql-query-builder/`) - Signal detection via label refinement & cardinality management
  - **Label Selection Framework**: Cardinality count, boundedness check, business value assessment
  - **Cardinality Thresholds**: Production capacity limits (1-2M series), per-metric targets (<10K), RAM requirements
  - **Reduction Techniques**: Aggregation, filtering (topk/bottomk), label replacement, recording rules, histogram bucket pruning
  - **Workflows**: Pre-production metric validation, production cardinality investigation
  - **Decision Trees**: Label retention vs removal, cardinality reduction technique selection
  - **Anti-Patterns**: Unbounded identifiers, temporal labels, excessive histogram buckets
  - **Integration**: Grafana dashboards, alerting rules, recording rules management

### Timestamp & Rate Limiting

- **orchestrator-timestamp-management.md** (`.claude/docs/01-guides/orchestration/`) - Timestamp management patterns

- **timestamp-system-implementation-plan.md** (`.claude/docs/01-guides/`) - Timestamp system implementation

- **../archive/research/2025/09-september/2025-09-20-rate-limiting-investigation.md** (`.claude/docs/01-guides/`) - Rate limiting investigation

- **../archive/research/2025/01-january/2025-01-20-intelligent-rate-limiting-redesign.md** (`.claude/docs/01-guides/`) - Rate limiting redesign

---

## 📚 Additional Resources

### Personas

- **tpm.md** (`docs/04-guides/personas/`) - Technical PM persona

- **architect.md** (`docs/04-guides/personas/`) - Architect persona

- **code-reviewer.md** (`docs/04-guides/personas/`) - Code reviewer persona

### Examples & Templates

- **roadmap-item-template.md** (`.claude/docs/cleanup/`) - Roadmap item template

- **claude-code-agent-flows.md** (`.claude/docs/01-guides/`) - Agent flow examples



### Domain Knowledge

- **Piotroski F-Score Implementation Guide.md** (`docs/04-guides/domain/`) - Financial analysis implementation

- **Agentic Investment Thesis Architecture Report.md** (`docs/04-guides/`) - Investment thesis architecture

- **CONNECTOR_DESIGN.md** (`docs/04-guides/`) - Connector design patterns

- **MULTI_PROVIDER_DEVELOPMENT_WORKFLOW.md** (`docs/04-guides/`) - Multi-provider workflow

- **prompt-template-enhancements.md** (`docs/04-guides/`) - Prompt template enhancements

### Component Specifications

- **DCF-MODEL-TOOL-SPEC.md** (`docs/03-implementation/components/`) - DCF model tool specification

- **QUAL-CONNECTORS.md** (`docs/03-implementation/components/`) - Qualitative connectors specification

- **domain-models-summary.md** (`docs/03-implementation/components/`) - Domain models summary

- **TECH-DEBT-BACKLOG.md** (`docs/03-implementation/components/`) - Technical debt backlog

### Integration Guides

- **ollama-integration-summary.md** (`docs/03-implementation/integrations/ollama/`) - Ollama integration overview

- **ollama-platform-guide.md** (`docs/03-implementation/integrations/ollama/`) - Ollama platform guide

- **ollama-integration-plan.md** (`docs/03-implementation/integrations/ollama/`) - Ollama integration plan

- **ollama-semantic-validation.md** (`docs/03-implementation/integrations/ollama/`) - Semantic validation with Ollama

- **golden-set-validation.md** (`docs/03-implementation/integrations/ollama/`) - Golden set validation approach

- **validation-infrastructure-plan.md** (`docs/03-implementation/integrations/`) - General validation infrastructure

- **Redis-Cache-Integration-Technical-Plan.md** (`docs/03-implementation/infrastructure/caching/`) - Redis cache integration

### Implementation Guides

- **../01-guides/integration/implementer-assist-io.md** (`.claude/docs/01-guides/`) - Implementer assistance patterns

- **IMPLEMENTATION_SUMMARY.md** (`.claude/docs/01-guides/implementation/`) - Implementation summary

- **implement-error-recovery.md** (`docs/04-guides/development/`) - Error recovery implementation

### Schema Documentation

- **specify-output-schema.md** (`.claude/docs/schemas/`) - Output schema specification

### CI/CD

- **ci-cd-spec.md** (`docs/03-implementation/infrastructure/ci-cd/`) - CI/CD specification

### Claude Code System Reports

- **../archive/research/2025/09-september/2025-09-20-report-structure-update.md** (`.claude/docs/05-reports/`) - Report structure update

- **../archive/research/2025/09-september/2025-09-20-claude-code-ecosystem-schema-consolidation.md** (`.claude/docs/01-guides/`) - Schema consolidation

- **../archive/research/2025/01-january/2025-01-27-design-guide-and-permissions.md** (`.claude/docs/01-guides/architecture/`) - Design guide and permissions

- **../archive/research/2025/09-september/2025-09-20-simplify-feedback-implementation.md** (`.claude/docs/01-guides/`) - Feedback simplification

- **../archive/research/2025/09-september/2025-09-20-tool-guidelines-git-simplification.md** (`.claude/docs/01-guides/`) - Tool guidelines update

- **../archive/research/2025/09-september/2025-09-20-timestamp-management-standardization.md** (`.claude/docs/01-guides/`) - Timestamp standardization

### README Files

- **README.md** (`.claude/docs/01-guides/`) - Guides directory overview

- **README.md** (`docs/01-planning/`) - Planning directory overview

- **README.md** (`docs/01-planning/features/archive/`) - Archived features overview

---

## 📂 Archive & Legacy

### Archived Features (Reference Only)

- **004-ooda-orchestration-system/** (`docs/06-archive/completed-projects/`) - OODA orchestration (ARCHIVED, superseded by 005)

- **004-collaboration-framework-improvements/** (`docs/01-planning/features/archive/`) - Collaboration improvements (superseded)

- **004-integration-analysis/** (`docs/01-planning/features/archive/`) - Integration analysis (superseded)

### Legacy Plans

- **legacy-plans/** (`docs/archive/planning-old/`) - Historical project plans

- **completed/** (`docs/archive/planning-old/legacy-plans/`) - Completed legacy plans

- **001-simplification-mvp.md** - Simplification MVP (completed)

- **002-report-maturation.md** - Report maturation (completed)

- **003-advanced-investor-analysis.md** - Advanced investor analysis (completed)

- **004-bulletproof-development-foundation.md** - Development foundation (completed)

- **005-mcp-tools-discovery-spike.md** - MCP tools discovery (completed)

- **006-local-production-deployment.md** - Local production deployment (completed)

- **007-claude-actions-integration.md** - Claude actions integration (completed)

- **007-moat-assessment-framework.md** - Moat assessment framework (completed)

- **008-advanced-frameworks-preparation.md** - Advanced frameworks preparation (completed)

- **010-opentelemetry-foundation.md** - OpenTelemetry foundation (completed)

- **010-piotroski-details-enhancement.md** - Piotroski details enhancement (completed)

- **011-claude-md-refactor.md** - CLAUDE.md refactor (completed)

### Legacy Documentation

- **claude-code-best-practices/** (`docs/04-guides/legacy/`) - Legacy Claude Code best practices (superseded by current standards)

- **PROJECT_PLAN-2024-08.md** (`docs/archive/planning-old/`) - August 2024 project plan (archived)

- **temp-files/** (`docs/archive/deprecated/`) - Deprecated temporary files

- **organization/** (`docs/archive/deprecated/`) - Deprecated organization docs

---

## 🗂️ Documentation Organization

### Directory Structure Overview

```text

docs/

├── 00-project/          # Project foundation (SPEC, almanac, operations)

├── 01-planning/         # Feature planning, specifications, custom plans

├── 02-architecture/     # System architecture, ADRs, design patterns

├── 03-implementation/   # Components, infrastructure, integrations

├── 04-guides/           # Development guides, code review, domain knowledge

├── 05-guides/           # Personas, templates, Claude Code operational guides

└── archive/             # Deprecated and historical documentation



.claude/docs/

├── guides/              # Agent development, workflows, operations

├── examples/            # Templates and examples

├── workflows/           # Workflow patterns and automation

├── schemas/             # Schema specifications

├── security/            # Security policies and whitelists

├── hooks/               # Hook documentation

└── reports/             # System reports and analyses

```

### Navigation Tips

1. **New to project?** Start with `docs/00-project/SPEC.md` and `COMPONENT_ALMANAC.md`

2. **Building a feature?** Check `docs/04-guides/development/spec-driven-development.md`

3. **Creating an agent?** Review `.claude/docs/01-guides/agents/base-agent-pattern.md`

4. **Need a review?** See `.claude/docs/01-guides/` review-specific guides

5. **Troubleshooting?** Check `docs/04-guides/claude-code/troubleshooting-guide.md`

---

**Maintenance**: This index should be updated when new documentation is added or reorganized. Last updated: 2025-10-18