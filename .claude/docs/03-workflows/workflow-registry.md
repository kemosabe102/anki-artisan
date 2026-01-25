---
title: "Claude Code Workflow Capabilities Registry"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Claude Code Workflow Capabilities Registry

**Last Updated**: 2025-09-21
**Registry Version**: 1.0.0
**Total Workflows Tracked**: 8

## Overview

This registry tracks all Claude Code workflows, their capabilities, maturity levels, and integration points. Use this to discover available workflows, understand their strengths and limitations, and select the right workflow for your needs.

## Workflow Capabilities Matrix

### 🟢 **Production Ready (GA)**

#### **Feature Development Workflow** (v3.1)

- **Commands**: `/spec` → `/plan` → `/tasks` → `/implement`
- **Strong At**: Strategic feature delivery, Context7 integration, sub-agent coordination, regenerative development
- **Capabilities**: Complete SDLC support, deterministic outcomes, roadmap integration, maturity-aware planning
- **Integration Points**: planner-agent, development-agent, test-runner-agent, code-quality, living sprint
- **Documentation**: `.claude/commands/spec/spec.md`, `.claude/commands/plan.md`, `.claude/commands/tasks.md`
- **Maturity**: Full SDLC support with proven reliability in production use

#### **Git Workflow** (v3.0)

- **Commands**: `/git`
- **Strong At**: Automated commit messages, staged change analysis, conventional commit standards
- **Capabilities**: Smart commit message generation, change impact analysis, conventional commit compliance
- **Integration Points**: code-quality, living sprint progress tracking
- **Documentation**: `.claude/commands/git.md`
- **Maturity**: Production-ready with comprehensive change analysis capabilities

### 🟡 **Testing Ready (Beta)**

#### **Code Review Workflow** (v2.1)

- **Commands**: Manual workflow via `scripts/prepare-code-review.py`
- **Strong At**: Quality validation, multi-tier testing, automated feedback preparation
- **Capabilities**: Three-tier validation (lint/fast/full), AI review preparation, artifact generation
- **Integration Points**: All sub-agents, git workflow, validation hooks
- **Documentation**: `.claude/docs/WORKFLOW.md` (code review section)
- **Maturity**: Reliable for development, improving automation integration

#### **Startup Evaluation Workflow** (v2.0)

- **Commands**: Automatic via `.claude/hooks/startup-eval.py`
- **Strong At**: Context loading, developer onboarding, project status overview
- **Capabilities**: Async document loading, developer identity integration, workflow recommendations
- **Integration Points**: Living sprint, roadmaps, developer identity, project context
- **Documentation**: `.claude/hooks/startup-eval.py` (comprehensive inline documentation)
- **Maturity**: Good core functionality with opportunities for optimization

#### **Progress Tracking Workflow** (v1.8)

- **Commands**: Integrated with living sprint updates
- **Strong At**: Sprint progress tracking, roadmap integration, developer assignment
- **Capabilities**: Cross-document synchronization, progress automation, status reporting
- **Integration Points**: Living sprint, roadmaps, sub-agent completion tracking
- **Documentation**: `docs/00-project/LIVING_SPRINT.md`
- **Maturity**: Functional with manual oversight, automation improvements in progress

### 🔄 **Development Ready (Alpha)**

#### **Workflow Orchestration** (v1.5)

- **Commands**: Orchestrator coordination patterns
- **Strong At**: Sub-agent delegation, 2-attempt rule, escalation patterns
- **Capabilities**: Agent capability matrix, workflow state management, context continuity
- **Integration Points**: All sub-agents, workflow state tracking, human escalation
- **Documentation**: `.claude/docs/orchestrator-workflow.md`
- **Maturity**: Core patterns established, refinement for complex scenarios needed

#### **Hook Automation Workflow** (v1.2)

- **Commands**: Various hooks in `.claude/hooks/`
- **Strong At**: Validation automation, startup evaluation, progress tracking
- **Capabilities**: Pre/post tool validation, session automation, custom workflow controls
- **Integration Points**: Claude Code hook system, tool validation, workflow automation
- **Documentation**: Individual hook files with inline documentation
- **Maturity**: Basic automation working, expanding validation and control capabilities

### 🟠 **Concept Phase (MVP)**

#### **Cross-Document Synchronization** (v0.5)

- **Commands**: Manual workflow, automation in development
- **Strong At**: Document consistency checking, dependency tracking
- **Capabilities**: Basic consistency validation, manual synchronization procedures
- **Integration Points**: Living sprint, roadmaps, workflow documentation
- **Documentation**: Manual procedures in various workflow docs
- **Maturity**: Concept validation, needs automation development

## Workflow Integration Map

### Primary Integration Clusters

#### **Feature Development Cluster**

```
/spec ← → planner-agent
    ↓
/plan ← → planner-agent + Context7 research
    ↓
/tasks ← → planner-agent + task breakdown
    ↓
/implement ← → multiple sub-agents (development, test-runner, code-quality)
    ↓
Living Sprint Updates ← → Progress Tracking
```

#### **Quality Assurance Cluster**

```
Code Review Workflow ← → All Sub-Agents
    ↓
Git Workflow ← → Commit Generation
    ↓
Hook Automation ← → Validation Rules
    ↓
Progress Tracking ← → Status Updates
```

#### **Developer Experience Cluster**

```
Startup Evaluation → Project Context Loading
    ↓
Workflow Orchestration → Sub-Agent Coordination
    ↓
Progress Tracking → Developer Status
    ↓
Cross-Document Sync → Consistency Maintenance
```

### Dependencies and Prerequisites

#### **High-Level Dependencies**

- **Feature Development** depends on: planner-agent, Context7 integration, living sprint
- **Code Review** depends on: validation hooks, git workflow, sub-agent coordination
- **Progress Tracking** depends on: living sprint, roadmap integration, developer identity
- **Startup Evaluation** depends on: project documentation, developer configuration

#### **Shared Components**

- **Sub-Agent System**: Used by feature development, code review, workflow orchestration
- **Living Sprint**: Used by progress tracking, feature development, startup evaluation
- **Context7 Integration**: Used by feature development, research workflows
- **Validation Hooks**: Used by code review, automation workflows

## Workflow Selection Guide

### By Use Case

#### **Starting New Feature Development**

1. **Ready for Implementation**: Use `/spec roadmap:next` → select ready item → `/plan` → `/tasks` → `/implement`
2. **Custom Feature**: Use `/spec "feature description"` → follow planning workflow
3. **Planning Required**: Use `/spec roadmap:planning-item` → complete planning first

#### **Daily Development Tasks**

1. **Code Review Preparation**: Use `scripts/prepare-code-review.py --stage-changes`
2. **Progress Updates**: Update living sprint manually, automation in development
3. **Status Overview**: Automatic startup evaluation provides current status

#### **Workflow Optimization**

1. **Bottleneck Analysis**: Manual analysis, workflow agent development in progress
2. **Documentation Updates**: Manual updates, cross-document sync in development
3. **Automation Setup**: Hook development for validation and progress tracking

### By Maturity Requirements

#### **Production Use (GA Required)**

- Feature development workflow
- Git workflow with conventional commits
- Basic code review validation

#### **Development Use (Beta Acceptable)**

- Code review workflow for quality gates
- Startup evaluation for developer onboarding
- Progress tracking with manual oversight

#### **Experimental Use (Alpha/MVP)**

- Workflow orchestration patterns
- Hook automation development
- Cross-document synchronization

## Missing Workflows & Development Priorities

### High Priority Development Needs

#### **Automated Progress Tracking** (Target: Beta)

- **Gap**: Manual living sprint updates after sub-agent completion
- **Solution**: Hook-based automation for progress updates
- **Impact**: Reduced manual overhead, consistent progress tracking

#### **Workflow Discovery System** (Target: Alpha)

- **Gap**: No systematic workflow discovery for new developers
- **Solution**: Interactive workflow recommendation system
- **Impact**: Improved developer onboarding and workflow adoption

#### **Cross-Document Synchronization** (Target: Beta)

- **Gap**: Manual consistency checking across workflow documents
- **Solution**: Automated synchronization and validation system
- **Impact**: Reduced documentation drift, improved consistency

### Medium Priority Enhancements

#### **Advanced Hook Automation** (Target: Alpha)

- **Gap**: Limited validation and automation capabilities
- **Solution**: Comprehensive hook framework for workflow automation
- **Impact**: Improved workflow reliability and validation

#### **Workflow Performance Analytics** (Target: MVP)

- **Gap**: No metrics on workflow efficiency and bottlenecks
- **Solution**: Performance tracking and analysis system
- **Impact**: Data-driven workflow optimization

## Deprecation Schedule

### Planned Deprecations

#### **Manual Progress Tracking** (Deprecate: Q1 2026)

- **Replacement**: Automated progress tracking workflow
- **Migration Path**: Gradual automation rollout with manual fallback
- **Reason**: Reduces manual overhead and improves consistency

#### **Manual Cross-Document Updates** (Deprecate: Q4 2025)

- **Replacement**: Automated synchronization workflow
- **Migration Path**: Automated validation with manual review
- **Reason**: Eliminates documentation drift and inconsistencies

### Legacy Workflow Support

#### **Command Evolution**

- **Current Commands**: Maintain backward compatibility during transitions
- **New Patterns**: Introduce new workflows alongside existing ones
- **Migration Support**: Provide clear migration paths and documentation

## Quality Metrics

### Workflow Reliability Metrics

- **Feature Development**: 95% successful completion rate
- **Git Workflow**: 100% conventional commit compliance
- **Code Review**: 90% issue detection rate
- **Startup Evaluation**: <10 second load time target

### Documentation Quality Metrics

- **Coverage**: 100% of GA workflows fully documented
- **Accuracy**: Monthly validation against actual workflow behavior
- **Usability**: Developer feedback integration for improvements
- **Discoverability**: Clear workflow selection guidance

### Integration Health Metrics

- **Dependency Tracking**: All workflow dependencies mapped and validated
- **Cross-Document Consistency**: Automated validation of document synchronization
- **Version Compatibility**: Backward compatibility maintained across workflow updates

---

**This registry provides comprehensive tracking of Claude Code workflow capabilities, enabling informed workflow selection and systematic improvement of the workflow ecosystem.**
