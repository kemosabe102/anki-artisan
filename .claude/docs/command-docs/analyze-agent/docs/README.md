# Analyze Agent Command Documentation

Supporting documentation for the `/analyze-agent` slash command.

## Files

| File | Purpose | When to Read |
|------|---------|--------------|
| `workflow-phases.md` | Detailed Phase 1-4 documentation | Understanding phase behavior, customizing analysis |
| `delegation-patterns.md` | Exact Task() call syntax for all 5 agents | Implementing delegation, debugging agent calls |
| `report-format.md` | Full report template (300+ lines) | Understanding output structure, customizing reports |
| `claude-md-mode.md` | CLAUDE.md orchestrator analysis mode | Analyzing orchestrator configuration |
| `pre-mortem-phase.md` | Phase 4 pre-mortem failure analysis | Predictive failure mode identification |
| `error-codes.md` | Error codes, recovery strategies, graceful degradation | Troubleshooting failures, understanding error handling |

## Quick Navigation

- **Need exact delegation syntax?** -> `delegation-patterns.md`
- **Understanding analysis phases?** -> `workflow-phases.md`
- **Customizing report output?** -> `report-format.md`
- **Analyzing CLAUDE.md?** -> `claude-md-mode.md`
- **Predictive failure analysis?** -> `pre-mortem-phase.md`
- **Troubleshooting errors?** -> `error-codes.md`

## Relationship to Main Command

The main `/analyze-agent` command file (`analyze-agent.md`) provides:
- Concise workflow overview
- Mode/argument reference
- Quick delegation syntax
- Error recovery table

These docs provide the **detailed implementation** referenced from the main file.
