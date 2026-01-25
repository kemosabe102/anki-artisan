# Repository Analyst Domain Knowledge

## YAML Frontmatter Parsing

### Required Fields by Component Type

**Agents** (`.claude/agents/*.md`):
- `name`: Agent identifier (required)
- `description`: Purpose and capabilities (required)
- `model`: sonnet|opus (required)
- `tools`: Comma-separated tool list (required)
- `color`: UI color code (optional)
- `ooda_phase`: OBSERVE|ORIENT|DECIDE|ACT (optional, infer if missing)

**Commands** (`.claude/commands/*.md`):
- `name`: Command identifier (required)
- `description`: Command purpose (required)

**Hooks** (`.claude/hooks/*.py`):
- Extract from Python docstring or module header

### Metadata Inference Rules

When optional fields are missing, infer from description keywords:

**OODA Phase Inference**:
- "discover", "analyze", "scan", "inspect" → OBSERVE
- "research", "investigate", "assess" → ORIENT  
- "plan", "design", "strategy", "decide" → DECIDE
- "implement", "execute", "deploy", "create" → ACT

**Domain Inference** (from agent name prefix):
- `agent-*`, `prompt-*` → `.claude/**`
- `python-*`, `debugger` → `packages/**`
- `doc-*`, `spec-*`, `plan-*` → `docs/**`
- `k8s-*`, `grafana-*` → `k8s/**`

---

## Component Taxonomies

### OODA Phase Distribution (Expected)
| Phase | Expected % | Purpose |
|-------|-----------|---------|
| OBSERVE | 20-25% | Discovery, analysis, scanning |
| ORIENT | 35-40% | Research, context gathering |
| DECIDE | 15-20% | Planning, strategy, design |
| ACT | 25-30% | Implementation, execution |

### Type Taxonomy
| Type | Keywords | Examples |
|------|----------|----------|
| Creator | create, generate, implement | python-code-implementer |
| Reviewer | review, validate, assess | python-code-reviewer, spec-reviewer |
| Enhancer | enhance, improve, optimize | plan-enhancer, architecture-enhancer |
| Runner | execute, run, deploy | test-executor, k8s-deployment |
| Analyzer | analyze, investigate, discover | feature-analyzer, repository-analyst |
| Planner | plan, strategy, roadmap | technical-pm, roadmap-manager |

### Maturity Levels
| Level | Version | Stability | Documentation |
|-------|---------|-----------|---------------|
| alpha | v0.x | Low | Minimal |
| beta | v1-2.x | Medium | Partial |
| stable | v3.x+ | High | Complete |
| GA | Production | Very High | Exhaustive |

---

## Naming Conventions

### File Naming Rules
| File Type | Convention | Pattern | Example |
|-----------|------------|---------|---------|
| Markdown | kebab-case | `^[a-z0-9-]+\.md$` | `agent-architect.md` |
| Python | snake_case | `^[a-z0-9_]+\.py$` | `validate_command.py` |

### Exceptions (Intentional Uppercase)
- `SPEC.md`, `COMPONENT_ALMANAC.md`, `CLAUDE.md`, `README.md`

---

## Standard Directory Structure

```
.claude/
├── agents/          # Agent definitions (*.md)
├── commands/        # Slash commands (*.md)
├── hooks/           # Lifecycle hooks (*.py)
├── skills/          # Skill definitions (*.md)
├── docs/            # Ecosystem documentation
└── templates/       # Component templates
```

### Exclusion Rules
Skip during discovery: `.venv/`, `__pycache__/`, `node_modules/`, `.git/`, `temp/`, `*.pyc`, `*.log`
