# Agent Capability Reference

**Purpose**: Complete catalog of 32+ agents across 6 domains with maturity grades, capabilities, and integration patterns

**Last Updated**: 2025-10-26

**Auto-loaded**: No (on-demand reference from orchestrator-workflow.md)

---

## Quick Lookup Index

**By Domain**:
- Research: researcher-lead, researcher-codebase, researcher-external
- Planning: planning, planning, architecture, architecture, planning
- Code/Testing: development, development, code-quality, code-quality, code-quality
- Documentation: documentation, documentation
- Infrastructure: deployment-release
- Git/GitHub: source-control

**By Performance Tier**:
- Fast (<30s): planning, planning
- Medium (1-2min): planning, architecture, architecture
- Slow (3+min): None after optimizations

**By Maturity**:
- GA (3.5+): None yet
- Beta (2.5-3.5): None yet
- Alpha (1.5-2.5): planning, architecture, code-quality, code-quality, code-quality
- MVP (0-1.5): development, development

---

## Overall Workflow Maturity

**Current Status**: Alpha (1.67) - Production Testing Ready with Test Architecture Enhancement

### Maturity Calculation

```
Critical Agent Average: (1.0 + 1.2 + 1.3 + 0.8 + 0.9 + 1.1) / 6 = 1.05
Support Agent Average: (1.0 + 1.0 + 0.7 + 1.0 + 1.0 + 0.6 + 1.0 + 1.0 + 1.0) / 9 = 0.92
Overall Maturity = (1.05 + 0.92) × 0.85 = 1.97 × 0.85 = 1.67 (Alpha)
```

### Maturity Stages

- **MVP (0-1.5)**: Development environment testing ready, manual oversight required
- **Alpha (1.5-2.5)**: Production testing ready, monitoring required
- **Beta (2.5-3.5)**: Production candidate, standard development workflow
- **GA (3.5+)**: Production ready, critical business workflows

---

## Critical Agents (Primary Workflow - 80% Weight)

| Agent | Maturity | Grade | Capabilities | Strong At | Limitations |
|-------|----------|-------|--------------|-----------|-------------|

| **planning** | v1.2 (Alpha) | A | Business alignment review and structured reporting | Business context review, NFR assessment, requirements traceability analysis, structured report generation | **PERFORMANCE OPTIMIZED**: Now 7 tools (Read+Grep+Research only) - zero file mutations |
| **architecture** | v1.3 (Alpha) | B+ | Technical architecture analysis and structured reporting | Technical analysis, production readiness assessment, Technical Review Reports + Edit Plans | **PERFORMANCE OPTIMIZED**: Now 6 tools (Read+Grep+Research only) - zero file mutations |
| **development** | v0.8 (MVP) | C+ | Code implementation, technical execution | Feature development, API integration | Complex architectural decisions |
| **code-quality** | v1.0 (Alpha) | B+ | Test execution, failure categorization, delegation routing | Multi-framework test running (pytest/jest/go test), 12-heuristic failure classification, delegation to development/code-quality/code-quality | Test creation (use code-quality), application bug fixing (use development) |
| **code-quality** | v1.1 (Alpha) | B+ | Quality gates, security validation, standards compliance | Code standards, security review | Performance optimization |

---

## Support Agents (Secondary Impact - 20% Weight)

| Agent | Maturity | Grade | Capabilities | Strong At | Limitations |
|-------|----------|-------|--------------|-----------|-------------|
| **architecture** | v1.0 (Alpha) | B+ | Technical architecture enhancement, Context7 research, placeholder replacement | Technical content population, research-backed decisions, file modification | Large-scale integration analysis |
| **planning** | v1.0 (Alpha) | B+ | Specification quality assessment, peer validation review | Quality scoring, ambiguity detection, improvement recommendations | Complex multi-spec validation, cross-specification consistency |
| **development** | v0.7 (MVP) | C | Problem diagnosis, troubleshooting | Error analysis, systematic debugging | Complex integration issues |
| **code-quality** | v1.0 (Alpha) | A- | Test generation, coverage analysis, AAA pattern enforcement | Unit test creation, pytest fixtures, Context7 research for testing patterns | Test execution (use code-quality), application bug fixing (use development) |
| **development** | v0.6 (MVP) | C- | Code organization, cleanup, optimization | Structure improvement, cleanup | Large-scale architectural changes |
| **claude-code-ecosystem** | v1.0 (Alpha) | B | Agent lifecycle management, evaluation | Agent creation, quality assessment | Complex workflow coordination |
| **context-optimizer** | v1.0 (Alpha) | B | Context analysis, optimization planning | Targeted/group/ecosystem token analysis, redundancy detection, flexible scope optimization | Analysis only, no modifications |
| **deployment-release** | v1.0 (Alpha) | B+ | Kubernetes deployment orchestration, pod troubleshooting, manifest management | Script-driven Kustomize workflows, event-driven troubleshooting, rollback strategies | Multi-cluster environments, cloud provider integrations |

---

## Research Agents

| Agent | Maturity | Grade | Domain | Capabilities |
|-------|----------|-------|--------|--------------|
| **researcher-lead** | v1.0 (Alpha) | A | Coordination | Research orchestration, multi-source coordination, complex information synthesis |
| **researcher-codebase** | v1.0 (Alpha) | A- | Code analysis | Pattern discovery (10:1 compression), architecture investigation, codebase exploration |
| **researcher-external** | v1.0 (Alpha) | A | External | Unified external research (Context7 library docs + Perplexity web search), auto-routes based on query type, source quality assessment, SSRF-protected (15:1 compression ratio, <15s performance) |

---

## Planning Agents

| Agent | Maturity | Grade | Domain | Capabilities |
|-------|----------|-------|--------|--------------|

| **planning** | v1.0 (Alpha) | B+ | Specifications | Quality assessment, peer validation review, ambiguity detection |
| **planning** | v1.0 (Alpha) | B+ | Plans | Business context enhancement, NFR specification |
| **architecture** | v1.0 (Alpha) | B+ | Plans | Technical architecture design, cleanup task generation |
| **architecture** | v1.3 (Alpha) | B+ | Validation | Technical validation, integration analysis, production readiness assessment |
| **planning** | v1.2 (Alpha) | A | Review | Business alignment review, requirements traceability analysis, structured reporting |

---

## Code & Testing Agents

| Agent | Maturity | Grade | Domain | Capabilities |
|-------|----------|-------|--------|--------------|
| **development** | v0.8 (MVP) | C+ | Implementation | Feature development, API integration, code organization |
| **development** | v0.7 (MVP) | C | Debugging | Hypothesis-driven debugging, error analysis, systematic troubleshooting |
| **code-quality** | v1.0 (Alpha) | A- | Testing | Test generation, coverage analysis, AAA pattern enforcement, pytest fixtures |
| **code-quality** | v1.0 (Alpha) | B+ | Testing | Multi-framework test running, 12-heuristic failure classification, delegation routing |
| **code-quality** | v1.1 (Alpha) | B+ | Quality | Standards compliance, security validation, code review |

---

## Documentation Agents

| Agent | Maturity | Grade | Domain | Capabilities |
|-------|----------|-------|--------|--------------|
| **documentation** | v1.0 (Alpha) | B | Organization | Documentation health checks, link validation, naming compliance |
| **documentation** | v1.0 (Alpha) | B | Optimization | Token density analysis, progressive disclosure, reference externalization |

---

## Infrastructure Agents

| Agent | Maturity | Grade | Domain | Capabilities |
|-------|----------|-------|--------|--------------|
| **deployment-release** | v1.0 (Alpha) | B+ | Kubernetes | Script-driven Kustomize workflows, pod troubleshooting, manifest management, rollback strategies |

---

## Git & GitHub Agents

| Agent | Maturity | Grade | Domain | Capabilities |
|-------|----------|-------|--------|--------------|
| **source-control** | v1.0 (Alpha) | B+ | Git | Intelligent file grouping, commit execution, CI monitoring, Conventional Commits |

---

## Top 10 Most-Used Agents

**Quick Reference for Common Tasks**:

| Agent | Domain | Primary Use | Performance |
|-------|--------|-------------|-------------|
| **development** | packages/** | Feature implementation with pre-flight validation | Medium |
| **development** | packages/**, tests/** | Bug fixing, hypothesis-driven debugging | Medium |
| **code-quality** | tests/** | Test execution, failure categorization, delegation routing | Fast |

| **researcher-codebase** | All sources | Codebase pattern discovery (10:1 compression) | Fast |
| **researcher-external** | External | Best practices, industry patterns, library docs (SSRF-protected) | Medium |
| **planning** | docs/** plans | Business context enhancement | Medium |
| **architecture** | docs/** plans | Technical design addition | Medium |
| **planning** | docs/**/tasks/** | Task list generation from plans | Fast |
| **source-control** | Git/GitHub | Commit automation, CI monitoring | Fast |

---

## Sub-Agent Coordination Patterns

**Sub-Agents as Specialized Tools** (orchestrator delegates to these):


- **planning**: Business alignment review, NFR assessment, requirements traceability, structured reporting
- **architecture**: Technical validation, integration analysis, production readiness, quality gates
- **development**: Code implementation, technical execution
- **code-quality**: Test execution, validation, quality assurance
- **code-quality**: Test generation, coverage analysis, AAA pattern enforcement
- **code-quality**: Quality gates, security, standards compliance
- **development**: Problem diagnosis, troubleshooting
- **development**: Code organization, refactoring, cleanup
- **claude-code-ecosystem**: Agent lifecycle, prompt engineering
- **researcher-lead**: Research orchestration, multi-source coordination, complex information synthesis
- **researcher-codebase**: Code analysis, pattern discovery, architecture investigation
- **researcher-external**: Unified external research (Context7 library docs + Perplexity web search), auto-routes based on query type, best practices discovery, source quality assessment
- **deployment-release**: Kubernetes deployment orchestration, pod troubleshooting, manifest management, script-driven Kustomize workflows

**Coordination Rules**:
- Only orchestrator delegates to sub-agents
- Sub-agents cannot call other sub-agents
- All sub-agent communication flows through orchestrator
- Orchestrator maintains context and state across sub-agent interactions
- **Orchestrator launches multiple sub-agents in parallel** when no file conflicts exist
- **Parallel execution recommended** for independent file processing (plan enhancement, task generation)

---

## Key Invocation Patterns

### Researcher-Lead Protocol

**✅ CORRECT Pattern**:
```
Task(agent="researcher-lead", prompt="CREATE A RESEARCH PLAN for [objective]")
→ researcher-lead returns delegation plan
→ Orchestrator spawns workers in parallel
```

**❌ WRONG Pattern**:
```
Task(agent="researcher-lead", prompt="Investigate [objective]")
→ researcher-lead executes research (99.4k tokens, 3m 53s)
```

**Key Insight**: researcher-lead is a coordinator, not an executor. Use it to plan research, then spawn workers yourself.

---

**This reference provides complete agent catalog for orchestrator decision-making and delegation planning.**
