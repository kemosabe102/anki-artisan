# Implement Command Documentation

Supporting documentation for the `/implement` slash command.

## Files

| File | Purpose | When to Read |
|------|---------|--------------|
| `workflow-phases.md` | Detailed documentation for each of the 4 workflow phases | Understanding phase behavior, debugging execution |
| `delegation-patterns.md` | Exact Task() call syntax for agent delegation | Implementing agents, debugging delegation |
| `error-handling.md` | Error scenarios with recovery strategies | Handling failures, understanding retry policy |
| `review-framework.md` | Multi-agent review checkpoint framework | Understanding quality gates, review selection |

## Quick Navigation

- **Need exact delegation syntax?** → `delegation-patterns.md`
- **Understanding a specific phase?** → `workflow-phases.md`
- **Debugging failures?** → `error-handling.md`
- **How review checkpoints work?** → `review-framework.md`

## Relationship to Main Command

The main `/implement` command file (`implement.md`) provides:
- Concise workflow overview
- Mode/argument reference
- Quick error recovery table
- Agent delegation summary

These docs provide the **detailed implementation** referenced from the main file.

## Key Concepts

### Orchestrator Philosophy
- **Delegates 95%** of work to specialized agents
- **Stays <10%** of context budget (~20k tokens)
- **Pure coordination** - never implements, tests, or reviews directly

### Retry Policy
- **Regular tasks**: 1 retry (fail-fast)
- **Review checkpoints**: 3 retries (quality-focused)
- **Infrastructure**: Exponential backoff (max 3)

### Progress Tracking
- IMPLEMENTATION_PROGRESS.md at feature root
- Review group granularity (not individual tasks)
- Resume capability from last completed group
