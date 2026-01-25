# Git-GitHub Agent Documentation

**Purpose**: Externalized domain knowledge for the git-github agent

---

## Contents

| File | Description | When to Consult |
|------|-------------|-----------------|
| `filegrouper-heuristics.md` | 6 heuristics for semantic commit grouping | analyze_changes operation |
| `error-handling.md` | Error classification, retry patterns, circuit breaker | Any git/GitHub errors |
| `operation-workflows.md` | Detailed workflows for all 3 operations | Operation execution |
| `conventional-commits.md` | Commit message format reference | Generating commit messages |

---

## Quick Reference

### Operation -> Document Mapping

- **analyze_changes**: `filegrouper-heuristics.md`, `conventional-commits.md`
- **execute_commits**: `error-handling.md`, `conventional-commits.md`
- **monitor_ci**: `error-handling.md`, `operation-workflows.md`

---

## See Also

- **Main agent**: `../git-github.md`
- **Output examples**: `../examples/output-examples.md`
- **Schema**: `../schemas/git-github.schema.json`
- **External**: `.claude/docs/01-guides/github-integration-guide.md`
