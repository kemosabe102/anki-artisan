# Create Agent Command Documentation

Supporting documentation for the `/create-agent` slash command.

## Files

| File | Purpose | When to Read |
|------|---------|--------------|
| `workflow-phases.md` | Detailed documentation for each of the 10 workflow phases | Understanding phase behavior, customizing workflow |
| `delegation-patterns.md` | Exact Task() call syntax for agent delegation | Implementing phases, debugging delegation |
| `error-handling.md` | Error scenarios with recovery strategies | Handling failures, understanding error recovery |
| `interactive-mode.md` | 5-phase interactive workflow for idea-to-definition | Using --create-definition flag |

## Quick Navigation

- **Need exact delegation syntax?** -> `delegation-patterns.md`
- **Understanding a specific phase?** -> `workflow-phases.md`
- **Debugging failures?** -> `error-handling.md`
- **Using interactive mode?** -> `interactive-mode.md`

## Relationship to Main Command

The main `/create-agent` command file (`create-agent.md`) provides:
- Concise workflow overview
- Mode/argument reference
- Quick error recovery table

These docs provide the **detailed implementation** referenced from the main file.

## External References

These shared resources are NOT moved here (used by other commands/agents):
- `.claude/templates/agent-definition-input.template.md` - Input template
- `.claude/templates/agent-scaffold/` - Directory structure template
- `.claude/docs/01-guides/interactive-agent-definition-workflow.md` - Shared workflow guide
