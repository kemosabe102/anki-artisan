# Code Review Command Documentation

Supporting documentation for the `/code-review` slash command.

## Files

| File | Purpose | When to Read |
|------|---------|--------------|
| `workflow-phases.md` | Detailed 7-phase documentation (P0-P6) with checkpoints | Understanding phase behavior, customizing workflow |
| `delegation-patterns.md` | Exact Task() call syntax for agent delegation | Implementing phases, debugging delegation |
| `finding-schema.md` | Complete finding structure with source_agent and conflict resolution | Understanding output format, extending schema |
| `error-handling.md` | Error scenarios with checkpoint recovery | Handling failures, resuming from failed phases |
| `confidence-investigation.md` | Phase 4 research via researcher agents | Understanding investigation delegation |

## Quick Navigation

- **Need exact delegation syntax?** -> `delegation-patterns.md`
- **Understanding confidence research?** -> `confidence-investigation.md`
- **Debugging failures or resuming?** -> `error-handling.md`
- **Understanding output format?** -> `finding-schema.md`
- **Phase-by-phase breakdown?** -> `workflow-phases.md`

## Key Differences from /review

| Aspect | /review | /code-review |
|--------|---------|--------------|
| Phase 0 | Direct tool check | HYBRID: direct git, delegate semgrep check |
| Phase 1 | Direct git commands | Delegate to git-github agent |
| Phase 4 | Direct MCP tool calls | Delegate to researcher-external |
| Checkpoints | None | Write after each phase |
| Conflicts | None | Severity conflict resolution in Phase 5 |

## Relationship to Main Command

The main `/code-review` command file (`code-review.md`) provides:
- Concise workflow overview
- Mode/argument reference
- Quick error recovery table
- Agent delegation summary

These docs provide the **detailed implementation** referenced from the main file.
