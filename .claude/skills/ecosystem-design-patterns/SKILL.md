---
name: ecosystem-design-patterns
description: >
  Architecture guidance for Claude Code ecosystem growth. Use when deciding whether
  to create an agent vs skill, evaluating skill cohesion, or planning ecosystem changes.
  Trigger keywords: agent vs skill, design patterns, architecture, ecosystem, cohesion.
---

# Ecosystem Design Patterns Skill

Architecture guidance for Claude Code ecosystem growth and sustainable scaling.

## Quick Reference

| Decision | Use Agent | Use Skill |
|----------|-----------|-----------|
| Complex multi-phase workflow | YES | NO |
| Reusable knowledge/methodology | NO | YES |
| Domain ownership required | YES | NO |
| Cross-cutting concern | NO | YES |
| Needs persistent state | YES | NO |
| Pure orchestration logic | NO | YES |
| File modification patterns | YES | NO |
| Decision frameworks | NO | YES |

---

## Reference Documentation

- **Agent vs Skill Decision Tree** -> [references/decision-tree.md](references/decision-tree.md)
- **Skill Maturity Model** -> [references/maturity-model.md](references/maturity-model.md)

---

## 1. Agent vs Skill Decision Tree

### When to Create an Agent

Create an agent when:

1. **Domain Ownership Required**: The capability needs to own files, lifecycle, or state
2. **Complex Multi-Phase Workflow**: Work spans multiple distinct phases with dependencies
3. **Persistent Identity Needed**: The capability needs to maintain context across sessions
4. **File Modification Is Primary**: The capability's main job is editing/creating files

### When to Create a Skill

Create a skill when:

1. **Reusable Methodology**: The capability is knowledge that multiple agents can use
2. **Cross-Cutting Concern**: Applies across domains (debugging, validation, research)
3. **Decision Framework**: Provides structured thinking patterns, not file operations
4. **Guidance Over Execution**: Teaches HOW to do something vs DOING it

---

## 2. Skill Cohesion Rules

### Size Constraints

| Metric | Limit | Rationale |
|--------|-------|-----------|
| SKILL.md lines | 500 max | Prevents context bloat |
| Reference files | 5-7 max | Focused domain |
| Total skill size | 2000 lines max | Manageable scope |

### Single Responsibility Principle

Each skill must answer ONE question:
- **Good**: "How do I debug using scientific method?" (debugging-methodology)
- **Bad**: "How do I debug, test, and deploy?" (too broad)

### Cohesion Checklist

- [ ] All content relates to single domain
- [ ] No overlapping responsibility with existing skills
- [ ] Can explain skill purpose in one sentence
- [ ] Reference files support main SKILL.md, not tangential topics

---

## 3. Dependency Mapping Patterns

### Allowed Dependencies

| Dependency Type | Allowed | Example |
|-----------------|---------|---------|
| Skill -> Reference doc | YES | SKILL.md -> references/pattern.md |
| Skill -> External guide | YES | SKILL.md -> .claude/docs/guide.md |
| Skill -> Skill | CAUTION | Only for composable patterns |
| Agent -> Skill | YES | Agent uses skill for methodology |
| Skill -> Agent | NO | Skills must not delegate to agents |

### Circular Dependency Detection

NEVER create cycles:
- skill-A -> skill-B -> skill-A (FORBIDDEN)
- skill-A -> agent-X -> skill-A (FORBIDDEN)

---

## 4. Anti-Patterns

### Overly Broad Skills

**Anti-Pattern**: Single skill covering multiple unrelated domains.

**Example**:
```
# BAD: development-skill
- Python implementation patterns
- Database optimization
- Kubernetes deployment
- Git workflow
```

**Fix**: Split into focused skills per domain.

### Circular Dependencies

**Anti-Pattern**: Skill A references Skill B which references Skill A.

**Detection**: Before adding dependency, trace path back to source.

**Fix**: Extract shared content to common reference document.

### Skill-as-Agent

**Anti-Pattern**: Skill that tries to own files or execute operations.

**Symptoms**:
- Skill contains "Edit file X" instructions
- Skill references specific file paths to modify
- Skill has "execution" or "implementation" phases

**Fix**: Convert to agent if file ownership needed, or clarify skill as guidance-only.

### Empty Abstraction

**Anti-Pattern**: Skill that adds indirection without value.

**Symptoms**:
- Skill just links to other documents
- Content could fit in a README
- No unique methodology or framework

**Fix**: Merge into parent skill or convert to reference document.

---

## 5. Skill Maturity Model

### Stage Definitions

| Stage | Description | Criteria |
|-------|-------------|----------|
| **sketch** | Initial idea, incomplete | Has SKILL.md stub only |
| **draft** | Functional but untested | Complete content, no validation |
| **stable** | Production-ready | Validated, documented, reviewed |
| **deprecated** | Superseded or obsolete | Marked for removal |

### Stage Indicators

Add to SKILL.md frontmatter:

```yaml
maturity: stable  # sketch | draft | stable | deprecated
deprecated-by: new-skill-name  # if deprecated
```

See [references/maturity-model.md](references/maturity-model.md) for detailed criteria.

---

## 6. Ecosystem Growth Guidelines

### Before Creating New Skill

1. Search existing skills for overlap
2. Check if agent already covers domain
3. Validate single-responsibility fit
4. Estimate maintenance burden

### Skill Naming Convention

- Use gerund form: `debugging-methodology`, `validating-specifications`
- Hyphenated lowercase
- Descriptive but concise (2-4 words)

### Directory Structure

```
.claude/skills/{skill-name}/
├── SKILL.md              # Main skill document (required)
├── references/           # Supporting documentation
│   ├── pattern-a.md
│   └── pattern-b.md
└── templates/            # Optional: reusable templates
    └── report.template.md
```

---

## Validation Checklist

Before marking skill as stable:

- [ ] SKILL.md under 500 lines
- [ ] Single responsibility verified
- [ ] No circular dependencies
- [ ] All references exist and valid
- [ ] Frontmatter complete (name, description, maturity)
- [ ] Trigger keywords documented
- [ ] Quick reference table present
- [ ] Anti-patterns avoided
- [ ] Tested by at least one agent
