# Shared Schema Directory

This directory contains schema files that are **shared across multiple agents or plugins**.

## Shared Schemas (9 files)

### Core Agent Schemas
- **base-agent.schema.json** - Base schema extended by all agent schemas
- **failure-tracking-memory.schema.json** - Failure tracking and learning patterns
- **implement-orchestrator-state.schema.json** - Orchestrator state management

### Planning & Decision Schemas
- **decisions.schema.json** - Decision tracking and rationale
- **dependency-manifest.schema.json** - Component dependency tracking
- **planning-package.schema.json** - Planning package structure
- **spec-review-output.schema.json** - Specification review outputs
- **state-transitions.schema.json** - State machine transitions
- **sow.schema.json** - Statement of Work structure

## Plugin-Specific Schemas

Agent-specific schemas are now located in their respective plugin directories:

- **dev-tools**: `.claude/agents/dev-tools/schemas/` (31 agent schemas)
- **research**: `.claude/agents/research/schemas/` (5 agent schemas)
- **investing**: `.claude/agents/investing/schemas/` (6 agent schemas)

## Schema Organization Principles

1. **Shared schemas** go here when used by multiple plugins or agents
2. **Agent-specific schemas** go in `{plugin}/schemas/` directory
3. **Base schema** is always shared (all agents extend it)
4. **Domain-specific schemas** stay with their domain agents
