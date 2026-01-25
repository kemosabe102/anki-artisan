# CLAUDE.md Orchestrator Analysis Mode

When `CLAUDE.md` is specified, the command analyzes the **orchestrator configuration** as an "agent definition" with adapted evaluation criteria.

---

## What Changes

When analyzing CLAUDE.md instead of a sub-agent:

| Aspect | Sub-Agent Analysis | CLAUDE.md Analysis |
|--------|-------------------|-------------------|
| Structure | Frontmatter validation | Section organization, hierarchy, navigation |
| Schema | JSON schema compliance | OODA framework, formulas (ASC/DCS/CQ), rules |
| Integration | External references | Auto-loaded docs, path consistency |
| Prompt Quality | Agent prompt evaluation | System prompt (role, XML, chain-of-thought) |
| Token Threshold | ~2K tokens acceptable | ~10K tokens acceptable |

---

## Adapted Validations

### Skipped Validations (N/A for orchestrator)
- Frontmatter compliance (orchestrator config, not agent)
- Base-pattern extension (orchestrator IS the base)

### Active Validations
- Formula consistency (ASC/DCS/CQ definitions match usage)
- Threshold clarity (0.5, 0.85, etc. documented)
- Delegation rule completeness
- Safety controls (BANNED operations, ALWAYS directives)
- Progressive disclosure (critical info in first 100 lines?)


---

## Report Differences

| Standard Report Section | CLAUDE.md Adaptation |
|------------------------|---------------------|
| Maturity Assessment | Orchestrator Health Score |
| Integration Checklist | Reference Validation |
| (new section) | Safety Information Accessibility |

### Safety Information Accessibility

Additional validation for CLAUDE.md:
- BANNED operations line position (should be in first 50 lines)
- ALWAYS directives line position (should be in first 100 lines)
- Emergency protocols visibility
- Security hook references

---

## Example Usage

```bash
/analyze-agent CLAUDE.md
```

**Output includes**:
- Orchestrator quality score (0-100)
- Redundancy analysis (duplicated content)
- Token savings opportunities
- Structural recommendations
- Safety audit (BANNED/ALWAYS accessibility)
- Formula consistency check
- Reference validation

---

## Agent Delegation Adaptations

When delegating to the 4 agents for CLAUDE.md analysis:

### claude-code-ecosystem
- Skip frontmatter validation
- Focus on section organization and navigation
- Validate formula definitions (ASC/DCS/CQ)


### claude-code-ecosystem
- Evaluate as system prompt (not agent prompt)
- Check role clarity and mission statement
- Validate XML structure potential
- Assess chain-of-thought scaffolding

### documentation
- Higher token threshold (~10K acceptable)
- Focus on redundancy across sections
- Check auto-loaded doc efficiency
- Validate external reference patterns

### tech-debt-investigator
- Documentation debt focus
- Section organization debt
- Cross-reference maintenance burden
- Historical cruft detection
