---
argument-hint: '<spec-path> | [check|update|assess|advance] [--stage=MVP|Alpha|Beta|GA]'
description: 'Generate ROADMAP.md from project specs. Modes: generate, check, update, assess, advance.'
allowed-tools: Task, Read, Skill
model: sonnet
---

# Roadmap Command

*Thin orchestrator for roadmap operations*

---

## Your Role

You are a **thin orchestrator** that:
1. Parses user input to identify mode
2. Validates required inputs exist
3. Delegates to appropriate agent or skill
4. Returns results verbatim

**DO NOT** implement roadmap logic - that lives in agents/skills.

---

## Mode Detection

| User Says | Mode | Delegate To |
|-----------|------|-------------|
| `/roadmap path/to/SPEC.md` | generate | Task(roadmap-manager) |
| `/roadmap path/to/SPEC.md --stage=Beta` | generate-stage | Task(roadmap-manager) with stage constraint |
| `/roadmap check` | health | Task(roadmap-manager) |
| `/roadmap check --stage=Beta` | health-stage | Task(roadmap-manager) for specific stage |
| `/roadmap update` | update | Task(roadmap-manager) |
| `/roadmap update --stage=Beta` | update-stage | Task(roadmap-manager) for specific stage |
| `/roadmap assess` | assess | Skill(roadmap-lifecycle) |
| `/roadmap advance` | advance | Skill(roadmap-lifecycle) |
| `/roadmap advance --to=Beta` | advance-to | Skill(roadmap-lifecycle) with target |

**Stage Parameter**: Custom stage names supported (MVP, Alpha, Beta, GA, or custom)

**Roadmap Location**: `docs/00-project/roadmaps/ROADMAP-{STAGE}.md`

---

## Delegation Patterns

### Generate Mode

```
Task(subagent_type="roadmap-manager", prompt="""
Create roadmap from spec: {spec_path}
Stage: {stage or 'default'}

Use semantic extraction for features (FR-XXX IDs, P0/P1/P2 tags).
Apply ICE scoring per .claude/docs/00-core/orchestrator-thresholds.md#ice-score-thresholds.
Output to: docs/00-project/roadmaps/ROADMAP-{STAGE}.md
""")
```

### Check Mode

```
Task(subagent_type="roadmap-manager", prompt="""
Generate health metrics for roadmap ecosystem.
Stage filter: {stage or 'all'}
Validate: structure, ICE scores, success metrics, feature count per phase.
""")
```

### Update Mode

```
Task(subagent_type="roadmap-manager", prompt="""
Update roadmap status for stage: {stage or 'all'}
Scan for spec/plan/task files, auto-check boxes where files exist.
""")
```

### Assess/Advance Mode

```
Skill(skill="roadmap-lifecycle")
```

The skill handles stage assessment (OBSERVE phase) and transition planning (DECIDE/ACT phases).

---

## Error Handling

| Error | Action |
|-------|--------|
| Spec path not found | Return: "Spec not found at {path}. Create with: /spec --project 'name'" |
| Invalid mode | Return: "Unknown mode. Valid: generate, check, update, assess, advance" |
| Invalid --stage | Return: "Invalid stage format. Examples: MVP, Alpha, Beta, GA, or custom name" |
| Agent/skill fails | Return failure with agent's error message verbatim |

---

## Knowledge Base

| Resource | Path |
|----------|------|
| ICE Thresholds | .claude/docs/00-core/orchestrator-thresholds.md#ice-score-thresholds |
| ICE Examples | .claude/docs/command-docs/roadmap/docs/ice-scoring.md |
| roadmap-manager | .claude/agents/planning/roadmap-manager/roadmap-manager.md |
| roadmap-lifecycle | .claude/skills/roadmap-lifecycle/SKILL.md |
| Roadmap template | .claude/docs/command-docs/roadmap/templates/roadmap-template.md |
| Error handling | .claude/docs/command-docs/roadmap/docs/error-handling.md |

---

## Roadmap Item Format

Each roadmap item is **epic-level** (1-2 weeks of work):

```markdown
### B.1 [Epic Name] (ICE: XXX)
- **Scope**: High-level description
- **Outcome**: What success looks like
- **Spec**: [ ] To create → links to SPEC.md when done
- **Status**: [ ] Not started
```

**Design Decisions**:
- Items are **outcomes**, not tasks
- Each epic = 1 SPEC.md = 1-2 weeks of work
- No implementation details - those live in PLAN.json
- Update roadmap only for strategic changes

---

## Integration

**Upstream**: PROJECT-SPEC.md (locked, detailed product vision)

**Downstream**:
- For each roadmap item: `/spec "[epic name]"` creates feature spec
- Then: `/plan` → `/tasks` → `/implement`

**Stage Lifecycle**:
```
/roadmap assess        → Determine current stage
/roadmap generate --stage=X  → Create stage roadmap
/roadmap advance --to=Y → Plan stage transition
```
