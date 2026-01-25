# Review Command Documentation

Supporting documentation for the `/review` slash command.

## Files

| File | Purpose | When to Read |
|------|---------|--------------|
| `workflow-phases.md` | Detailed documentation for each of the 6 workflow phases | Understanding phase behavior, customizing workflow |
| `delegation-patterns.md` | Exact Task() call syntax for agent delegation | Implementing phases, debugging delegation |
| `error-handling.md` | Error scenarios with recovery strategies | Handling failures, understanding error recovery |
| `confidence-investigation.md` | Phase 4 confidence-driven research protocol | Understanding investigation flow, tuning thresholds |
| `finding-schema.md` | Complete finding structure documentation | Understanding output format, extending schema |

## Quick Navigation

- **Need exact delegation syntax?** -> `delegation-patterns.md`
- **Understanding confidence research?** -> `confidence-investigation.md`
- **Debugging failures?** -> `error-handling.md`
- **Understanding output format?** -> `finding-schema.md`

## Relationship to Main Command

The main `/review` command file (`review.md`) provides:
- Concise workflow overview
- Mode/argument reference
- Quick error recovery table
- Agent delegation summary

These docs provide the **detailed implementation** referenced from the main file.
