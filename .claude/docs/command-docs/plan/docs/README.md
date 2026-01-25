# Plan Command Documentation

Supporting documentation for the `/plan` slash command.

## Files

| File | Purpose | When to Read |
|------|---------|--------------|
| `workflow-phases.md` | Detailed documentation for each of the 7 workflow phases | Understanding phase behavior, customizing workflow |
| `delegation-patterns.md` | Exact Task() call syntax for agent delegation | Implementing phases, debugging delegation |
| `error-handling.md` | Error scenarios with recovery strategies | Handling failures, understanding error recovery |

## Quick Navigation

- **Need exact delegation syntax?** → `delegation-patterns.md`
- **Understanding a specific phase?** → `workflow-phases.md`
- **Debugging failures?** → `error-handling.md`

## Relationship to Main Command

The main `/plan` command file (`plan.md`) provides:
- Concise workflow overview
- Mode/argument reference
- Quick error recovery table
- Quality gate thresholds

These docs provide the **detailed implementation** referenced from the main file.
