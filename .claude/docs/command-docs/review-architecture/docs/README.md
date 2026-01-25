# Review Architecture Command Documentation

Supporting documentation for the `/review-architecture` slash command.

## Overview

The `/review-architecture` command provides comprehensive 9-phase architecture review with stage-appropriate quality gates (MVP/Alpha/Beta/RC/GA). It applies TOGAF, SOLID, NFR, and ARB frameworks progressively based on detected project maturity.

## Files

| File | Purpose | When to Read |
|------|---------|--------------|
| `workflow-phases.md` | Detailed P0-P8 phase documentation | Understanding phase behavior, gate conditions |
| `framework-integration.md` | 5-framework integration guide | Applying TOGAF, SOLID, NFR, ARB, ICE |
| `../examples/usage-examples.md` | Usage patterns with expected outputs | Learning command options |
| `../schemas/review-architecture.schema.json` | Output schema definition | Understanding report structure |

## Quick Navigation

- **Understanding analysis phases?** -> `workflow-phases.md`
- **Framework application rules?** -> `framework-integration.md`
- **Command usage patterns?** -> `../examples/usage-examples.md`
- **Output structure?** -> `../schemas/review-architecture.schema.json`


## Quick Start

```bash
# Basic directory review
/review-architecture packages/core/

# Stage-specific review
/review-architecture --stage Beta packages/core/

# Full codebase with ADR generation
/review-architecture --all --generate-adrs

# Comprehensive report level
/review-architecture --report-level comprehensive
```

## Workflow Summary

```
P0:VALIDATE -> P1:EXPLORE -> P2:COLLECT -> P3:SYNTHESIZE -> P4:PRE-MORTEM -> P5:RECOMMEND -> P6:REPORT -> P7:DELEGATION -> P8:ADR-GENERATE
     |             |              |              |               |               |             |              |               |
  Cynefin      MECE+3agents   OODA-OBSERVE   Synthesis      Pre-Mortem     ICE Priority   Progressive    OODA-ACT      ADR Templates
  fail-fast    parallel       gather+stage   multi-frame    contingency    scoring        disclosure     delegate      generation
```

**Mandatory Phases**: P0-P6 (always executed in sequence)
**Conditional Phases**: P7 (user requests implementation), P8 (--generate-adrs flag)

## Related References

- Main command: `.claude/commands/review-architecture.md`
- Architecture reviewer agent: `.claude/agents/architecture/architecture-reviewer/architecture-reviewer.md`
- Stage policies: `.claude/docs/01-guides/architecture/architecture-review-stage-policies.md`
- Scoring rubric: `.claude/docs/01-guides/architecture/architecture-review-scoring-rubric.md`
- Frameworks catalog: `.claude/docs/00-core/frameworks/README.md`
