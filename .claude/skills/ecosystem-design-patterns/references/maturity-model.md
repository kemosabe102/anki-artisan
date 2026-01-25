# Skill Maturity Model

Lifecycle stages for skills from conception to deprecation.

---

## Stage Overview

```
sketch -> draft -> stable -> deprecated
   │        │        │           │
   │        │        │           └─> Archived or removed
   │        │        └─> Production use
   │        └─> Development complete
   └─> Initial concept
```

---

## Stage 1: Sketch

**Definition**: Initial idea captured, minimal content.

### Entry Criteria
- Identified need for skill
- Created SKILL.md stub

### Exit Criteria (to Draft)
- [ ] SKILL.md has complete structure
- [ ] Core methodology documented
- [ ] At least one reference file exists
- [ ] Frontmatter complete

### Allowed Actions
- Rapid iteration
- Major structural changes
- Incomplete sections acceptable

---

## Stage 2: Draft

**Definition**: Functionally complete but not validated.

### Entry Criteria
- All sections of SKILL.md populated
- Reference documentation complete
- Trigger keywords defined

### Exit Criteria (to Stable)
- [ ] Reviewed by domain expert
- [ ] Tested by at least one agent
- [ ] No broken references
- [ ] Under size limits (500 lines SKILL.md)
- [ ] Anti-patterns checklist passed

### Allowed Actions
- Content refinement
- Bug fixes
- Reference updates
- Minor structural changes

---

## Stage 3: Stable

**Definition**: Production-ready, validated, documented.

### Entry Criteria
- All draft exit criteria met
- Documented in skill registry
- At least 2 weeks in draft without major issues

### Exit Criteria (to Deprecated)
- [ ] Superseded by better skill
- [ ] Domain no longer relevant
- [ ] Consolidated into another skill

### Allowed Actions
- Bug fixes only
- Reference updates (non-breaking)
- Clarifications (no semantic changes)

### Change Control
Major changes require:
1. Create new draft version
2. Parallel run period
3. Migration path documented
4. Deprecate old version

---

## Stage 4: Deprecated

**Definition**: Superseded or obsolete, marked for removal.

### Entry Criteria
- Replacement skill exists (if superseded)
- Migration path documented
- Deprecation notice period (2 weeks minimum)

### Exit Criteria (Removal)
- [ ] No agents actively using skill
- [ ] Migration complete
- [ ] Archive copy preserved

### Deprecation Notice Template
```markdown
> **DEPRECATED**: This skill is deprecated as of YYYY-MM-DD.
> Use [new-skill-name](path/to/new-skill) instead.
> This skill will be removed on YYYY-MM-DD.
> See [migration guide](path/to/migration.md) for transition steps.
```

---

## Maintenance Schedule

| Stage | Review Frequency | Allowed Changes |
|-------|------------------|-----------------|
| sketch | Weekly | Any |
| draft | Bi-weekly | Content, structure |
| stable | Quarterly | Bug fixes, clarifications |
| deprecated | None | Deprecation notices only |

---

## Stage Transition Checklist

### Sketch -> Draft
- [ ] SKILL.md structure complete
- [ ] All sections have content
- [ ] References created
- [ ] Frontmatter updated

### Draft -> Stable
- [ ] Domain expert review
- [ ] Agent integration test
- [ ] Size limits verified
- [ ] Anti-patterns check passed
- [ ] Registry entry created

### Stable -> Deprecated
- [ ] Replacement identified (or N/A)
- [ ] Migration guide created
- [ ] Deprecation notice added
- [ ] Removal date set (min 2 weeks)
- [ ] Stakeholders notified

### Deprecated -> Removed
- [ ] Migration complete verified
- [ ] No active usage
- [ ] Archive copy saved
- [ ] Registry entry removed
