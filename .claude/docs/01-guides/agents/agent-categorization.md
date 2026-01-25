---
title: "Agent Categorization Guide"
date: 2025-11-08
status: ACTIVE
tags: [agents, claude-docs]
---

## Agent Categorization Guide

**Purpose**: Organize agents by capability and use case for easy discovery
**Last Updated**: 2025-10-03

## Agent Categories Overview

```text
All Agents
├── Planning & Design (6 agents)
├── Implementation & Code (4 agents)
├── Testing & Quality (2 agents)
├── Review & Validation (4 agents)
├── Meta & Management (3 agents)
├── Analysis & Discovery (3 agents)
└── Domain Specialists (1 agent)
```

## Category 1: Planning & Design

**Purpose**: Create specifications, plans, and architectural designs

| Agent                     | Type             | Modifies Files | Primary Use                         |
| ------------------------- | ---------------- | -------------- | ----------------------------------- |

| **planning**         | Enhancer         | ✅ Yes         | Add business context to plans       |
| **architecture** | Enhancer         | ✅ Yes         | Add technical details to plans      |
| **planning**         | Reviewer         | ❌ No          | Validate specification quality      |
| **planning**          | Reviewer         | ❌ No          | Review business alignment           |
| **architecture**   | Reviewer         | ❌ No          | Review technical architecture       |

### When to Use

- Starting new feature → /spec command
- Creating plans → planning + architecture
- Validating quality → planning, planning, architecture

## Category 2: Implementation & Code

**Purpose**: Write, modify, and improve code

| Agent                       | Type     | Primary Use           | Key Strength          |
| --------------------------- | -------- | --------------------- | --------------------- |
| **development** | Creator  | Write new features    | Production code       |
| **debugger**                | Fixer    | Diagnose and fix bugs | Problem solving       |
| **development** | Improver | Clean up code         | Structure improvement |
| **handle-code-review**      | Handler  | Apply review feedback | Fix implementation    |

### When to Use

- New feature → development
- Bug fixing → debugger
- Code cleanup → development
- Address review → handle-code-review

## Category 3: Testing & Quality

**Purpose**: Ensure code quality through testing

| Agent             | Type           | Primary Use             | Coverage Focus    |
| ----------------- | -------------- | ----------------------- | ----------------- |
| **test-runner**   | Creator/Runner | Write and execute tests | Unit, integration |
| **test-reviewer** | Reviewer       | Review test quality     | Test coverage     |

### When to Use

- Need tests → test-runner
- Validate test quality → test-reviewer

## Category 4: Review & Validation

**Purpose**: Review without modification, provide feedback

| Agent                    | Type     | Reviews What           | Output             |
| ------------------------ | -------- | ---------------------- | ------------------ |
| **code-quality** | Reviewer | Code quality, security | Feedback report    |
| **planning**        | Reviewer | Specification quality  | Quality assessment |
| **planning**         | Reviewer | Business alignment     | Business report    |
| **architecture**  | Reviewer | Technical architecture | Technical report   |

### Key Characteristic

**ALL reviewers are READ-ONLY** - they cannot modify files

### When to Use

- PR review → code-quality
- Spec validation → planning
- Business check → planning
- Technical validation → architecture

## Category 5: Meta & Management

**Purpose**: Manage agents, workflows, and system configuration

| Agent               | Type        | Manages              | Special Purpose              |
| ------------------- | ----------- | -------------------- | ---------------------------- |
| **claude-code-ecosystem** | Manager     | Agent lifecycle      | Create/update agents         |
| **workflow**        | Coordinator | Workflow ecosystem   | Slash commands, automation   |
| **claude-code**     | Manager     | Claude configuration | .claude directory management |

### When to Use

- Create new agent → claude-code-ecosystem
- Workflow automation → workflow
- Claude config → claude-code

## Category 6: Analysis & Discovery

**Purpose**: Discover patterns, analyze components, generate inventories

| Agent                  | Type     | Analyzes                | Output Type         |
| ---------------------- | -------- | ----------------------- | ------------------- |
| **repository-analyst** | Analyzer | Repository components   | Component inventory |
| **feature-analyzer**   | Analyzer | Specification documents | Overlap analysis    |
| **tech-debt-investigator** | Analyzer | Codebase quality    | Technical debt report |

### When to Use

- Component inventory → repository-analyst
- Feature overlap detection → feature-analyzer
- Technical debt assessment → tech-debt-investigator

## Category 7: Domain Specialists

**Purpose**: Specialized domain expertise for specific data types, APIs, and integrations

| Agent                     | Type               | Domain Scope                           | Primary Use                         |
| ------------------------- | ------------------ | -------------------------------------- | ----------------------------------- |
| **market-data-specialist** | Creator + Validator | packages/core/data/**, packages/connectors/market_data/** | OHLCV validation, API integration, Parquet optimization, SQLAlchemy models |
| **sentiment-nlp-specialist** | Creator + Validator | packages/core/nlp/**, packages/analysis/sentiment/** | Financial NLP, sentiment analysis, text processing, model integration |
| **pattern-detector** | Analyzer + Validator | packages/analysis/patterns/**, packages/core/technical_analysis/** | Technical pattern detection (Breakout, Pullback, PEAD, Divergence), confidence scoring, multi-pattern resolution |
| **risk-management-specialist** | Analyzer + Creator | packages/core/risk/**, packages/core/portfolio/** | Portfolio risk, position sizing (Van Tharp R-Multiple), stop-loss (Chandelier), circuit breakers, constraint enforcement |

### When to Use

- Market data validation → market-data-specialist
- Financial API integration → market-data-specialist
- Data compression optimization → market-data-specialist
- Time-series data modeling → market-data-specialist
- Sentiment analysis → sentiment-nlp-specialist
- Financial text processing → sentiment-nlp-specialist
- NLP model integration → sentiment-nlp-specialist
- News/earnings call analysis → sentiment-nlp-specialist
- Technical pattern detection → pattern-detector
- Breakout/pullback analysis → pattern-detector
- PEAD (post-earnings drift) detection → pattern-detector
- Divergence pattern detection → pattern-detector
- Multi-pattern conflict resolution → pattern-detector
- Position sizing calculation → risk-management-specialist
- Stop-loss placement (ATR-based) → risk-management-specialist
- Portfolio heat monitoring → risk-management-specialist
- Daily loss limits (circuit breakers) → risk-management-specialist
- Volatility regime detection → risk-management-specialist

## Performance Categories

### 🟢 Fast Agents (<30s startup)

Best for initial analysis and quick tasks:

- planning
- planning (after optimization)
- code-quality

### 🟡 Medium Agents (1-2min startup)

Good for focused modifications:

- planning
- architecture
- development

### 🔴 Heavy Agents (3+min startup)

Use sparingly, batch operations:

- (None currently after optimizations)

## Selection Decision Tree

```text
What do you need?
├── Planning/Design
│   ├── Create spec → /spec command
│   ├── Enhance plan → planning OR architecture
│   └── Review → planning OR planning OR architecture
├── Implementation
│   ├── New code → development
│   ├── Fix bugs → debugger
│   ├── Clean code → development
│   └── Apply feedback → handle-code-review
├── Testing
│   ├── Write tests → test-runner
│   └── Review tests → test-reviewer
└── Review Only
    ├── Code → code-quality
    ├── Specs → planning
    ├── Business → planning
    └── Technical → architecture
```

## Capability Matrix

### By Tool Access

| Capability           | Agents with Access                                                                               |
| -------------------- | ------------------------------------------------------------------------------------------------ |
| **Write/Edit Files** | development, planning, architecture, handle-code-review |
| **Read Only**        | All reviewers (planning, code-quality, planning, architecture)           |
| **Run Commands**     | test-runner, development, debugger                                                   |
| **Web Research**     | planning, architecture                                                 |

### By Workflow Phase

| Phase              | Primary Agents                       | Support Agents                    |
| ------------------ | ------------------------------------ | --------------------------------- |
| **Planning**       | /spec command                        | planning                     |
| **Design**         | planning, architecture | planning, architecture |
| **Implementation** | development              | debugger, development |
| **Testing**        | test-runner                          | test-reviewer                     |
| **Review**         | code-quality                 | handle-code-review                |

## Agent Interaction Patterns

### Sequential Pattern

```text
/spec command → planning → planning → architecture → development → test-runner → code-quality
```

### Review-Fix Pattern

```text
code-quality → handle-code-review → code-quality (verify)
```

### Enhancement Pattern

```text
planning (business) → architecture (technical) → planning (validate)
```

## Common Workflows

### Feature Development

1. /spec command - Create specification
2. planning - Add business context
3. architecture - Add technical details
4. development - Write code
5. test-runner - Create tests
6. code-quality - Review quality

### Bug Fix

1. debugger - Diagnose issue
2. development - Fix bug
3. test-runner - Add regression test
4. code-quality - Review fix

### Code Improvement

1. code-quality - Identify issues
2. development - Clean up code
3. test-runner - Ensure no regression
4. code-quality - Verify improvements

## Best Practices

### DO ✅

- Use reviewers for validation
- Use enhancers for modifications
- Check performance tier before delegation
- Batch operations for heavy agents
- Follow sequential workflows

### DON'T ❌

- Use reviewers to modify files
- Skip review phases
- Use heavy agents for simple tasks
- Mix review and modification in one agent
- Create duplicate agents

## Quick Reference Card

### Most Used Agents

1. **development** - Main coding agent
2. **/spec command** - Specification creation
3. **test-runner** - Test automation
4. **code-quality** - Quality gates
5. **debugger** - Problem solving

### By Frequency

- Daily: development, test-runner, code-quality
- Weekly: planning, architecture
- As needed: debugger, development
- Rarely: claude-code-ecosystem, workflow

---

**Remember**: Choose agents based on whether you need to READ (reviewer) or MODIFY (enhancer/development).
