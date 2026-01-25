# Agent Matrix Reference

**Purpose**: Explains WHY different agents review different file categories.

---

## Universal Agents (Always Run)

| Agent | Purpose | Why Universal? |
|-------|---------|----------------|
| `tech-debt-investigator` | Code health, complexity | All code can accumulate debt |
| `documentation` | Link validation, structure | All code benefits from doc checks |

---

## Category-Specific Agents

| Category | Agents | Why These Agents? |
|----------|--------|-------------------|
| database | `code-quality` | SQL injection, migration safety |
| api | `code-quality`, `sast-scanner` | Auth bypass, input validation, API security |
| ui | `code-quality` | XSS, accessibility, component quality |
| config | `sast-scanner` | Secrets exposure, invalid syntax |
| tests | `code-quality` | Coverage, flaky tests, test quality |
| docs | `planning` | Completeness, broken links (SPEC patterns only) |
| infrastructure | `deployment-release`, `sast-scanner` | Manifest validity, security config |
| claude_code | `claude-code-ecosystem`, `architecture` | Agent quality, schema compliance |
| code | `code-quality` | General code quality |

---

## Why This Matrix?

### Domain Expertise
Different file types need different expertise:
- Python API code → needs security review
- Agent definitions → needs ecosystem review
- K8s manifests → needs deployment review

### Risk-Based Selection
Higher-risk categories get more agents:
- `api`: 2 security-focused agents
- `infrastructure`: 2 deployment-focused agents
- `docs`: Only planning (lower risk)

### Efficiency
- Universal agents provide baseline coverage
- Dynamic agents add targeted checks
- Max 5 agents per group prevents review fatigue

---

## Execution Model

```python
def get_agents(category):
    UNIVERSAL = ["tech-debt-investigator", "documentation"]
    DYNAMIC = {
        "api": ["code-quality", "sast-scanner"],
        "database": ["code-quality"],
        # ... other mappings
    }
    return UNIVERSAL + DYNAMIC.get(category, ["code-quality"])
```

---

## See Also

- Execution logic: `.claude/commands/git.md`
- SKILL reference: `../SKILL.md`
