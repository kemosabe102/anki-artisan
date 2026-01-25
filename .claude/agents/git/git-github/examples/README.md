# Git-GitHub Agent Examples

**Purpose**: Output examples and usage patterns for the git-github agent

---

## Contents

| File | Description |
|------|-------------|
| `output-examples.md` | JSON output schemas for all 3 operations |

---

## Quick Usage

### Orchestrator Delegation Pattern

```
Task(git-github, "Analyze changes and group for commits")
Task(git-github, "Execute commits for groups 1-3")
Task(git-github, "Check CI status for commit abc123")
```

---

## See Also

- **Main agent**: `../git-github.md`
- **Schema**: `../schemas/git-github.schema.json`
- **Workflows**: `../docs/operation-workflows.md`
