# Code Review Schemas

Schema definitions for the `/code-review` command workflow.

## Files

| Schema | Purpose |
|--------|---------|
| `code-review-checkpoint.schema.json` | Checkpointing state for the 7-phase workflow |
| `code-review.schema.json` | Finding structure with severity, confidence, and conflict resolution |

## Schema Versions

- **Current**: 1.0.0
- **JSON Schema Draft**: draft-07

## Usage

### Checkpoint Schema
Used to persist workflow state between phases. Enables:
- Resume after interruption
- Phase-by-phase progress tracking
- Tool availability detection

### Finding Schema
Defines the structure for code review findings:
- Severity levels: Critical, High, Medium, Low, Nit
- Categories: Security, Performance, Quality, Design, Maintainability
- Confidence scoring (0.0-1.0)
- Conflict resolution for multi-agent severity disputes
