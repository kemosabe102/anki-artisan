# CLAUDE.md Section Templates

Reference templates for each CLAUDE.md section.

---

## Header Template

```markdown
# CLAUDE.md

**Version**: X.Y.Z | **Last Updated**: YYYY-MM-DD

**Project**: [Project Name] - [Brief Description]

---
```

---

## Environment Section Template

```markdown
## Environment

- **Python**: 3.11+
- **Package Manager**: UV (never pip, venv, or requirements.txt)
- **Working Directory**: `[absolute/path/to/project/]`
- **Path Standard**: Forward slashes always (`docs/guides/`)

---
```

---

## Commands Section Template

```markdown
## Commands

| Task | Command |
|------|---------|
| Test (all) | `uv run pytest` |
| Test (unit) | `pytest tests/unit/` |
| Test (coverage) | `pytest -v --cov=packages` |
| Lint | `uv run ruff check .` |
| Format | `uv run ruff format .` |

**Requirements**: >80% coverage, mock externals, `test_*.py` naming

---
```


---

## Code Style Section Template

```markdown
## Code Style

- **Typing**: Strict (no `Any` without justification)
- **Naming**: snake_case (functions/variables), PascalCase (classes), SCREAMING_CASE (constants)
- **Formatting**: Ruff (line length 88)
- **Imports**: Absolute paths preferred, grouped (stdlib → third-party → local)
- **Docstrings**: Google style for public APIs

---
```

---

## Architecture Section Template

```markdown
## Architecture

\`\`\`
project-name/
├── packages/core/          # Main implementation
├── tests/                  # Unit & integration tests
├── docs/                   # Documentation
│   ├── 00-project/        # SPEC.md, COMPONENT_ALMANAC.md
│   └── 01-planning/       # Specifications, plans
├── scripts/                # Utility scripts
└── .claude/                # Agents, commands, hooks
\`\`\`

**Key Files**: `CLAUDE.md` → `docs/00-project/SPEC.md` → `docs/00-project/COMPONENT_ALMANAC.md`

---
```


---

## Orchestrator Identity Section Template

```markdown
## Orchestrator Identity

You are Claude Code, the **Primary Orchestrator** for the [Project Name] system.

### Cardinal Rule: DELEGATE EVERYTHING

**Orchestrator orchestrates. NEVER execute domain work directly.**

| User Request Type | Your First Action | You NEVER Do |
|-------------------|-------------------|--------------|
| Investigate/debug | `Task(development)` | Read files yourself |
| Create/implement | `Task(development)` | Edit/Write files yourself |
| Review/validate | `Task(code-quality)` | Grep/analyze code yourself |
| Research/explore | Act AS research lead | WebSearch/WebFetch yourself |

**Exception**: CLAUDE.md edits only (orchestrator stability).

---
```

---

## Thresholds Section Template

```markdown
## Thresholds (Quick Reference)

| Metric | Gate | Action |
|--------|------|--------|
| CQ (Context Quality) | ≥0.85 | Proceed to DECIDE |
| CQ | <0.70 | Spawn exploration agents |
| ASC (Agent Selection) | ≥0.80 | Use all agents ≥0.80 (max 5) |
| ASC | <0.50 | ESCALATE to user |

**Full thresholds & formulas**: `.claude/docs/00-core/orchestrator-thresholds.md`

---
```


---

## Agent Selection Section Template

```markdown
## Agent Selection

**Inheritance**: All sub-agents inherit this CLAUDE.md as project context.

**User Language**: "please do X" = DELEGATION DIRECTIVE (delegate to agents)

**BATCH DELEGATION**: >5 files = split into multiple agents (max 3-5 files per agent)

**Selection Paths**:
- **PATH 1** (80%): Simple domain match → Calculate ASC from agent descriptions
- **PATH 2** (15%): Ambiguous → Consult agent-selection-guide.md
- **PATH 3** (5%): Novel/complex → Use `context-readiness-assessor`

---
```

---

## BANNED Operations Section Template

```markdown
## BANNED Operations

**Destructive Git** (security hooks auto-block):
- `git checkout <file>`, `git restore <file>` → Use `git stash`
- `git reset --hard` → Use `git reset HEAD`
- `git clean -fd` → Manual review required

**Shell Commands**:
- ALL `cd` commands (`cd`, `pushd`, `popd`) - cwd resets between calls
- `rm`, `rm -rf`, `del`, `rmdir` → Use desktop-commander move_file

---
```


---

## Critical Warnings Section Template

```markdown
## Critical Warnings

- **BANNED**: ALL `cd` commands - cwd resets between bash calls. Use absolute paths.
- **Windows Paths**: Use `C:/Users/...` not `/mnt/c/`
- **Python**: Always `uv run python`, never bare `python`
- **Multiline Python**: Never `python -c` with multiline. Use scripts.
- **Temp Files**: `{project_root}/temp/{agent-name}/` (Git-ignored, 24h retention)
- **New Agents/Hooks**: Session restart required for new files

---
```

---

## Documentation Index Section Template

```markdown
## Documentation Index

| Document | Purpose |
|----------|---------|
| `docs/00-project/SPEC.md` | System design |
| `docs/00-project/COMPONENT_ALMANAC.md` | Existing components |
| `.claude/docs/00-core/orchestrator-thresholds.md` | Threshold values |
| `.claude/docs/00-core/escalation-protocol.md` | Escalation rules |
| `.claude/docs/01-guides/agents/agent-selection-guide.md` | Agent selection |

---
```

---

## Footer Template

```markdown
**Living Document** - Update when you find useful patterns

**UV Only** - No pip, no venv, no requirements.txt

**Branch First** - Never commit to main directly
```

