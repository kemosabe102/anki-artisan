# Claude Schemas

This directory contains JSON Schema definitions for validation and structure enforcement across the Claude Code ecosystem.

## Schemas

| Schema | Purpose |
|--------|---------|
| `terminal-bench-checkpoint.schema.json` | Phase-based checkpoint tracking for terminal-bench workflow |

## Schema: terminal-bench-checkpoint

Tracks workflow state across the terminal-bench task creation pipeline.

### Phases

| Phase | Description |
|-------|-------------|
| `DISCOVERY` | Idea selection and concept hardening |
| `SPECIFICATION` | TB-SPEC document creation |
| `PLANNING` | TB-PLAN document creation |
| `IMPLEMENTATION` | File creation (instruction.md, task.toml, Dockerfile, solve.sh, tests/) |
| `VALIDATION` | CI, oracle, agent, and LLMAJ validation |
| `SUBMISSION` | Final packaging and submission |
| `COMPLETE` | Workflow finished |

### Gates

| Gate | Checkpoint |
|------|------------|
| `G1` | Discovery complete |
| `G1.5` | Specification complete |
| `G1.75` | Planning complete |
| `G2` | Implementation complete |
| `G3` | Validation complete |

### File Status Tracking

Each implementation file tracks:
- `status`: `not_started` | `pending` | `approved`
- `iterations`: Number of revision cycles
- `approved_at`: Timestamp of approval

## Usage

Schemas in this directory are used for:
- Validating checkpoint files during workflow execution
- Ensuring consistent data structures across agents
- Providing IDE autocompletion and validation

## Schema Standards

- All schemas follow JSON Schema draft-07
- Required fields are explicitly listed
- Enum values are used for constrained string fields
- Definitions are used for reusable structures (`fileStatus`, `gate`)
