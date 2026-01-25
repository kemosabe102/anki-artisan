# Orchestrator Essential Documentation Index

**Purpose**: Quick reference to critical documentation for orchestration decisions

**Auto-loaded**: Via startup-eval.py hook (in memory, not sent per-message)

**Usage**: Reference these docs when making delegation, architecture, or workflow decisions

---

## Project Core (Top 3 Priority)

### 1. SPEC.md - System Design
**Path**: `docs/00-project/SPEC.md`
**Purpose**: Complete system architecture, business case, technical requirements
**When to Check**: Understanding project goals, feature requirements, NFRs
**Key Sections**: Business Framework, Component Catalog, FR-IDs, Success Metrics

### 2. COMPONENT_ALMANAC.md - Existing Components
**Path**: `docs/00-project/COMPONENT_ALMANAC.md`
**Purpose**: **CHECK BEFORE NEW CODE** - Avoid duplication, discover existing functionality
**When to Check**: BEFORE creating new features, BEFORE proposing new implementations
**Key Sections**: Core Infrastructure, Data Pipeline, Agent Catalog, Utility Functions

### 3. LIVING_SPRINT.md - Current Sprint Status
**Path**: `docs/00-project/operations/LIVING_SPRINT.md`
**Purpose**: Active tasks, priorities, blockers, sprint velocity
**When to Check**: Understanding current work, prioritizing new requests, resource allocation
**Key Sections**: Sprint Goals, In-Progress Tasks, Blocked Items, Velocity Metrics

---

## Orchestration Core

### 4. orchestrator-workflow.md - Agent Coordination & Delegation Patterns
**Path**: `.claude/docs/03-workflows/orchestrator-workflow.md`
**Purpose**: Complete agent catalog (32+ agents), domain boundaries, OODA phase mapping, delegation patterns
**When to Check**: Agent selection decisions, multi-agent coordination, understanding agent capabilities
**Key Sections**: Agent Legend (maturity grades, domains), Multi-agent patterns, Parallel execution, Synthesis triggers

### 5. agent-standards-extended.md - Comprehensive Agent Design Standards
**Path**: `.claude/docs/01-guides/agents/agent-standards-extended.md`
**Purpose**: Universal agent requirements, quality criteria, integration guidelines
**When to Check**: Creating new agents, reviewing agent quality, validating agent outputs
**Key Sections**: Base-agent pattern, Quality matrix, Schema requirements, Frontmatter standards

---

## Research & Context Gathering

### 6. research-patterns.md - Research Delegation Strategies
**Path**: `.claude/docs/00-core/research-patterns.md`
**Purpose**: When to research, which researcher-* agent to use, context quality thresholds
**When to Check**: Context_Quality <0.5, unfamiliar domains, complex multi-source research
**Key Sections**: researcher-lead protocol, Context7-first patterns, Perplexity escalation, Worker allocation

### 7. research-tool-selection-protocol.md - Cost-Optimized Research
**Path**: `.claude/docs/01-guides/research/research-tool-selection-protocol.md`
**Purpose**: Context7 vs Perplexity decision matrix, cost tracking, target ratios (4:1)
**When to Check**: Library/framework errors, research tool selection, cost optimization
**Key Sections**: Context7-first protocol, Perplexity escalation triggers, Integration status, Monitoring metrics

---

## Performance & Efficiency

### 8. tool-parallelization-patterns.md - Read/Grep/Write Efficiency
**Path**: `.claude/docs/01-guides/performance/tool-parallelization-patterns.md`
**Purpose**: When to parallelize tool calls, batch delegation, read/write patterns
**When to Check**: Multi-file operations, codebase exploration, performance optimization
**Key Sections**: Parallel for reads, Sequential for writes, Batch delegation (5 files max per agent), Research worker limits

---

## File Operations & Workflows

### 9. file-operation-protocol.md - File Editing Protocol & Rate Limiting
**Path**: `.claude/docs/01-guides/file-ops/file-operation-protocol.md`
**Purpose**: Desktop Commander usage, rate limiting, Windows path handling
**When to Check**: File editing tasks, tool failures, platform-specific issues
**Key Sections**: Desktop Commander Protocol (edit_block, write_file), Rate limiting, Temp directory standards

### 10. multi-developer-workflow.md - Git Collaboration Patterns
**Path**: `.claude/docs/01-guides/git/multi-developer-workflow.md`
**Purpose**: Pull-before-push, conflict resolution, /git prepare automation, remote sync
**When to Check**: Git operations, multi-developer scenarios, merge conflicts
**Key Sections**: Pull patterns, Automated checks (/git prepare), Conflict resolution, Divergence detection

### 11. safety-protocols.md - Git Data Loss Prevention
**Path**: `.claude/docs/01-guides/git/safety-protocols.md`
**Purpose**: Banned git commands (reset --hard, clean -fd), safe alternatives, permission protocol
**When to Check**: Git operations, user requests to discard work, data safety validation
**Key Sections**: Banned operations, Safe alternatives, Permission protocol, Security hooks

---

## Development Methodologies

### 12. spec-driven-development.md - SDD Methodology & Workflow
**Path**: `docs/04-guides/development/spec-driven-development.md`
**Purpose**: SPEC → PLAN → TASKS → Implement workflow, regenerative development, SDD mode
**When to Check**: Feature planning, architecture decisions, roadmap-to-implementation flow
**Key Sections**: SDD phases, /spec command, /plan command, /tasks command integration

### 13. confidence-based-delegation-framework.md - Agent Selection Confidence (ASC/DCS)
**Path**: `docs/01-planning/custom/confidence-based-delegation-framework.md`
**Purpose**: ASC formula (Domain×0.6 + WorkType×0.3 + TrackRecord×0.1), DCS methodology, threshold validation
**When to Check**: Complex delegation decisions, novel domains, PATH 3 scenarios
**Key Sections**: ASC vs DCS, 4-dimension DCS scoring, Decision trees, Validation results (28/28 tests)

---

## Infrastructure & Observability

### 14. infrastructure guides - Observability Stack
**Path**: `.claude/docs/01-guides/infrastructure/**`
**Purpose**: OpenTelemetry, Prometheus, Grafana, Loki, K8s deployment, telemetry patterns
**When to Check**: Infrastructure tasks, observability requests, monitoring setup
**Key Sections**:
- `prometheus-setup.md`: Prometheus config, exporters, scraping
- `grafana-dashboards.md`: Dashboard creation, query patterns
- `loki-integration.md`: LogQL queries, log aggregation
- `deployment-release.md`: Kubernetes orchestration, Kustomize workflows

---

## Workflow Examples (Real-World Patterns)

### 15. workflow examples - Agent Coordination Patterns
**Path**: `.claude/docs/04-examples/**`
**Purpose**: Real-world multi-agent coordination, async validation, architecture reviews, code quality workflows
**When to Check**: Learning orchestration patterns, replicating successful workflows, troubleshooting coordination issues
**Key Sections**:
- `agent-coordination-example.md`: 3 core + 2 dynamic agents pattern
- `async-validation-workflow.md`: Parallel validation with synthesis
- `architecture-example.md`: Multi-phase architecture review
- `code-quality-workflow.md`: Self-correcting review loops

---

## Complete Documentation Catalog

### DOC-INDEX.md - 213+ Categorized Docs
**Path**: `.claude/docs/02-reference/DOC-INDEX.md`
**Purpose**: Comprehensive index of ALL documentation across categories
**When to Check**: Finding specific guides, exploring available documentation, comprehensive searches
**Categories**: Architecture, Performance, Security, Planning, Review, Operations, Testing, Infrastructure, Research, Agents, Workflows

---

## Quick Reference Table

| **Need** | **Doc** | **Path** |
|----------|---------|----------|
| Avoid duplication | COMPONENT_ALMANAC.md | docs/00-project/ |
| Understand goals | SPEC.md | docs/00-project/ |
| Agent selection | orchestrator-workflow.md | .claude/docs/03-workflows/ |
| Research strategy | research-patterns.md | .claude/docs/00-core/ |
| File operations | file-operation-protocol.md | .claude/docs/01-guides/file-ops/ |
| Git safety | safety-protocols.md | .claude/docs/01-guides/git/ |
| Performance | tool-parallelization-patterns.md | .claude/docs/01-guides/performance/ |
| Confidence scoring | confidence-based-delegation-framework.md | docs/01-planning/custom/ |
| Infrastructure | infrastructure/** | .claude/docs/01-guides/infrastructure/ |
| Complete catalog | DOC-INDEX.md | .claude/docs/02-reference/ |

---

## Usage Patterns

### Before Creating New Code
1. Check COMPONENT_ALMANAC.md (avoid duplication)
2. Check SPEC.md (align with requirements)
3. Check relevant workflow examples (learn patterns)

### Before Delegating to Agent
1. Check orchestrator-workflow.md (agent capabilities, domain boundaries)
2. Calculate confidence (ASC/DCS frameworks)
3. Check research-patterns.md if Context_Quality <0.5

### Before Git Operations
1. Check safety-protocols.md (banned commands)
2. Check multi-developer-workflow.md (pull-before-push)
3. Use /git prepare (automated validation)

### Before Performance-Critical Tasks
1. Check tool-parallelization-patterns.md (parallel vs sequential)
2. Check file-operation-protocol.md (batch patterns)
3. Consider batch delegation (5 files max per agent)

---

**Last Updated**: 2025-11-21
**Maintained By**: Orchestrator + documentation
**Auto-loaded**: Via startup-eval.py hook
**Format**: Living index (updated as new docs added)
