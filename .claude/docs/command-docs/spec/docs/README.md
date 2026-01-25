# Spec Command Documentation

Supporting documentation for the `/spec` slash command.

## Files

| File | Purpose | When to Read |
|------|---------|--------------|
| `workflow-phases.md` | Detailed 14-phase workflow documentation | Understanding phase behavior, debugging flow |
| `delegation-patterns.md` | Exact Task() call syntax for agent delegation | Implementing delegation, debugging agents |
| `error-handling.md` | Error scenarios with recovery strategies | Handling failures, understanding recovery |
| `guide-file-processing.md` | Guide file extraction patterns | Processing `file:path` inputs |

## Quick Navigation

- **Need exact delegation syntax?** → `delegation-patterns.md`
- **Understanding a specific phase?** → `workflow-phases.md`
- **Debugging failures?** → `error-handling.md`
- **Processing guide files?** → `guide-file-processing.md`

## Relationship to Main Command

The main `/spec` command file (`spec.md`) provides:
- Concise workflow overview
- Mode/argument reference
- Quick error recovery table
- Agent delegation summary

These docs provide the **detailed implementation** referenced from the main file.
