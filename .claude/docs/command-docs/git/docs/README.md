# Git Command Documentation

Supporting documentation for the `/git` slash command.

## Files

| File | Purpose | When to Read |
|------|---------|--------------|
| `workflow-phases.md` | Detailed documentation for each of the 5 workflow phases | Understanding phase behavior, customizing workflow |
| `delegation-patterns.md` | Exact Task() call syntax for agent delegation | Implementing new phases, debugging delegation |
| `error-handling.md` | Error scenarios with recovery strategies | Handling failures, understanding error recovery |
| `decision-tree.md` | Visual decision flowcharts | Understanding branching logic |
| `ci-integration.md` | CI/CD workflow integration patterns | Setting up automated workflows |

## Quick Navigation

- **Need exact delegation syntax?** → `delegation-patterns.md`
- **Understanding a specific phase?** → `workflow-phases.md`
- **Debugging failures?** → `error-handling.md`
- **Setting up CI/CD?** → `ci-integration.md`

## Relationship to Main Command

The main `/git` command file (`git.md`) provides:
- Concise workflow overview
- Mode/argument reference
- Quick error recovery table

These docs provide the **detailed implementation** referenced from the main file.
