# Claude Code Workflows: Developer Usage Guide

**Last Updated**: 2025-09-21
**Guide Version**: 1.0.0

## Quick Start

**New to Claude Code Workflows?** Start here for immediate productivity.

### Essential Commands (5-Second Reference)

```bash
/spec roadmap:next          # See top development candidates
/spec "feature description" # Start custom feature development
/plan                         # Generate technical implementation plan
/tasks                        # Break down plan into executable tasks
/implement                    # Execute tasks with sub-agent coordination
```

### Daily Workflow Pattern

1. **Morning**: Review startup evaluation for current status and recommendations
2. **Development**: Use `/spec` → `/plan` → `/tasks` → `/implement` cycle
3. **Before Commits**: Run `scripts/prepare-code-review.py --stage-changes`
4. **End of Day**: Update living sprint progress (automation in development)

## Workflow Discovery by Scenario

### 🚀 **Starting New Feature Development**

#### **Scenario 1: Ready Roadmap Items**

```bash
# See what's ready for immediate development
/spec roadmap:next

# Expected output: Top 3 ready items + 2 planning items
# Choose from ✅ READY items for immediate specification work
```

#### **Scenario 2: Custom Feature Development**

```bash
# Start custom feature specification
/spec "Create user authentication system with OAuth2"

# Follow the guided specification process
# Context7 research will be integrated automatically
```

#### **Scenario 3: Planning Phase Items**

```bash
# Work on items that need planning first
/spec roadmap:ROADMAP-PLAN-001

# Note: Planning items require planner agent work before implementation
```

### 🔧 **Daily Development Tasks**

#### **Code Review Preparation**

```bash
# Default mode (fast validation - 2 minutes)
uv run python scripts/prepare-code-review.py --stage-changes

# Full validation (includes integration tests - 5 minutes)
uv run python scripts/prepare-code-review.py --full --stage-changes

# Quick linting only (30 seconds)
uv run python scripts/prepare-code-review.py --lint-only --stage-changes
```

#### **Progress Tracking**

```bash
# Manual living sprint updates (automation in development)
# Edit: docs/00-project/LIVING_SPRINT.md
# Add completed tasks and update current focus
```

#### **Status Overview**

```bash
# Automatic startup evaluation provides:
# - Current project status
# - Active tasks and recent completions
# - Workflow recommendations
# - Quick start commands
```

### 🔍 **Troubleshooting and Analysis**

#### **Workflow Issues**

```bash
# Check workflow orchestration status
# Review: .claude/docs/orchestrator-workflow.md
# Apply 2-attempt rule for sub-agent issues
```

#### **Integration Problems**

```bash
# Validate workflow integration
# Check: .claude/docs/workflows/workflow-integration-map.md
# Review dependency matrix and data flow analysis
```

#### **Performance Optimization**

```bash
# Analyze workflow bottlenecks (manual analysis)
# Future: workflow agent will provide automated bottleneck analysis
```

## Workflow Selection Guide

### By Development Phase

#### **Feature Planning Phase**

- **Primary**: `/spec` command with roadmap integration
- **Supporting**: Context7 research, existing component discovery
- **Output**: Complete feature specification with technical planning
- **Next Step**: `/plan` command for detailed technical design

#### **Technical Design Phase**

- **Primary**: `/plan` command for implementation planning
- **Supporting**: Architecture compliance, Context7 pattern research
- **Output**: Technical plan with implementation phases
- **Next Step**: `/tasks` command for executable breakdown

#### **Implementation Phase**

- **Primary**: `/tasks` → `/implement` workflow
- **Supporting**: Sub-agent coordination, progress tracking
- **Output**: Working feature with test coverage
- **Next Step**: Code review workflow

#### **Quality Assurance Phase**

- **Primary**: Code review workflow with multi-tier validation
- **Supporting**: Git workflow, conventional commit generation
- **Output**: Quality-validated changes ready for merge
- **Next Step**: Living sprint progress updates

### By Experience Level

#### **New Developers**

1. **Start Here**: Run `/spec roadmap:next` to see development candidates
2. **Choose Ready Items**: Select from ✅ READY items for immediate work
3. **Follow Guided Process**: Use `/plan` → `/tasks` → `/implement` sequence
4. **Use Default Code Review**: `scripts/prepare-code-review.py --stage-changes`

#### **Experienced Developers**

1. **Custom Features**: Use `/spec "description"` for custom development
2. **Complex Planning**: Work with 🟡 PLANNING items to make them ready
3. **Advanced Code Review**: Use `--full` mode for integration testing
4. **Workflow Optimization**: Review workflow registry for advanced patterns

#### **Team Leads**

1. **Roadmap Management**: Coordinate roadmap readiness and developer assignments
2. **Workflow Coordination**: Use orchestrator patterns for complex coordination
3. **Quality Standards**: Establish code review standards and automation
4. **Process Improvement**: Analyze workflow bottlenecks and optimization opportunities

## Command Reference

### Core Development Commands

#### `/spec` - Feature Specification

```markdown
# Basic usage

/spec "feature description"

# Roadmap integration

/spec roadmap:next # Show top candidates
/spec roadmap:ROADMAP-ID # Specific roadmap item
/spec roadmap:title-substring # Fuzzy match
/spec roadmap:recent # Recent roadmap updates
```

**What it does**: Creates comprehensive feature specification using planner-agent with GitHub spec-kit integration and regenerative development patterns.

**Output**: Complete feature specification in `docs/01-planning/specifications/` with:

- Business goals and context
- Technical architecture
- Success criteria and acceptance tests
- Implementation phases and constraints

#### `/plan` - Technical Implementation Planning

```markdown
# Generate technical plan from approved specification

/plan [implementation details / constraints]
```

**What it does**: Executes implementation planning workflow using planner-agent with extended thinking for architecture and tradeoffs.

**Output**: Detailed technical plan with:

- Implementation phases
- Architecture decisions
- Task breakdown preparation
- Risk assessment and mitigation

#### `/tasks` - Executable Task Generation

```markdown
# Generate task breakdown from technical plan

/tasks [additional tasking context]
```

**What it does**: Generates actionable, dependency-ordered task list using planner-agent with extended thinking for dependency graphing.

**Output**: Complete task list with:

- Numbered tasks (T001, T002, ...)
- Dependency ordering
- Parallel execution guidance
- Sub-agent assignments

### Supporting Commands

#### Code Review Commands

```bash
# Three-tier validation system
scripts/prepare-code-review.py --lint-only    # Quick (30s)
scripts/prepare-code-review.py                # Default/Fast (2min)
scripts/prepare-code-review.py --full         # Complete (5min)
```

#### Manual Workflow Commands

```bash
# Living sprint management (manual)
# Edit: docs/00-project/LIVING_SPRINT.md

# Workflow registry consultation
# View: .claude/docs/workflows/workflow-registry.md

# Integration troubleshooting
# View: .claude/docs/workflows/workflow-integration-map.md
```

## Best Practices

### Workflow Execution

#### **Feature Development Best Practices**

1. **Always start with `/spec`** - Even for small features, specification prevents scope creep
2. **Use roadmap integration** - `/spec roadmap:next` provides vetted, ready items
3. **Follow complete cycle** - Don't skip planning phases for complex features
4. **Leverage Context7 research** - Automatic best practices integration during specification

#### **Code Review Best Practices**

1. **Use appropriate validation tier** - Default mode for daily development, full mode for integration changes
2. **Stage changes intelligently** - Let script auto-detect or stage specific chunks
3. **Review all artifacts** - Check diff reports, AI review prompts, and summary documents
4. **Address feedback systematically** - Use handle-code-review agent for complex feedback

#### **Progress Tracking Best Practices**

1. **Update living sprint regularly** - Mark completed tasks and advance focus
2. **Maintain roadmap synchronization** - Keep roadmap items aligned with sprint progress
3. **Use developer identity** - Configure for personalized workflow experience
4. **Document blockers clearly** - Enable effective troubleshooting and resolution

### Efficiency Tips

#### **Time Management**

- **Morning Status**: Startup evaluation provides complete context in <10 seconds
- **Command Discovery**: Use `/spec roadmap:next` instead of manual roadmap review
- **Validation Speed**: Use default code review mode (2min) for 95% of development
- **Batch Processing**: Group related tasks for parallel execution where marked [P]

#### **Quality Management**

- **Specification First**: Always create specification before implementation
- **Context7 Integration**: Leverage automatic best practices research
- **Validation Gates**: Don't skip code review workflow for any changes
- **Documentation Sync**: Keep living sprint current for team coordination

#### **Collaboration**

- **Clear Handoffs**: Use structured output for orchestrator coordination
- **Progress Visibility**: Living sprint provides team progress transparency
- **Quality Standards**: Consistent code review workflow for all team members
- **Knowledge Sharing**: Document workflow patterns for team adoption

## Troubleshooting Guide

### Common Issues and Solutions

#### **Feature Specification Issues**

**Problem**: `/spec` command returns planning items instead of ready items
**Solution**: Use `/spec roadmap:next` to see readiness levels, work on planning items first

**Problem**: Specification lacks technical detail
**Solution**: Ensure planner-agent has Context7 research completed, review technical plan section

**Problem**: Specification too complex for MVP stage
**Solution**: Use maturity-aware planning, distinguish core vs optional features

#### **Planning and Task Issues**

**Problem**: Technical plan lacks implementation detail
**Solution**: Review architecture compliance, ensure Context7 patterns integrated

**Problem**: Task breakdown has unclear dependencies
**Solution**: Review dependency ordering logic, mark parallel tasks with [P]

**Problem**: Tasks too large or too small
**Solution**: Adjust granularity based on sub-agent capabilities and execution time

#### **Integration Issues**

**Problem**: Sub-agent coordination failures
**Solution**: Apply 2-attempt rule, escalate to human after second failure

**Problem**: Cross-document inconsistencies
**Solution**: Manual validation procedures, automated sync in development

**Problem**: Progress tracking delays
**Solution**: Manual living sprint updates, automation development in progress

### Performance Optimization

#### **Workflow Speed**

- Use default code review mode for daily development
- Leverage parallel task execution where marked [P]
- Configure developer identity for personalized startup experience
- Use roadmap integration instead of custom feature descriptions when possible

#### **Quality Improvement**

- Always complete specification phase before implementation
- Use full code review mode for integration and architectural changes
- Maintain living sprint currency for effective coordination
- Apply Context7 research findings systematically

## What's Coming Next

### Planned Workflow Enhancements

#### **Q4 2025**

- **Automated Progress Tracking**: Hook-based living sprint updates after sub-agent completion
- **Cross-Document Synchronization**: Automated consistency validation and updates
- **Workflow Performance Analytics**: Bottleneck analysis and optimization recommendations

#### **Q1 2026**

- **Enhanced Discovery System**: Interactive workflow recommendation based on context
- **Advanced Hook Automation**: Comprehensive validation and quality gate automation
- **Integration Health Monitoring**: Real-time integration status and failure detection

#### **Q2 2026**

- **Workflow Customization**: Team-specific workflow patterns and templates
- **Advanced Analytics**: Predictive workflow optimization and performance insights
- **Ecosystem Integration**: Enhanced integration with external development tools

---

**This guide provides comprehensive guidance for effective Claude Code workflow usage, enabling developers to maximize productivity while maintaining high quality standards.**
