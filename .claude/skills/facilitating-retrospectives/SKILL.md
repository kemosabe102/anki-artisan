---
name: facilitating-retrospectives
description: >
  Use this skill when facilitating retrospectives (sprint or milestone),
  capturing lessons learned, tracking action items, or driving continuous
  improvement. Covers multiple formats (Start/Stop/Continue, 4Ls, Sailboat).
  Feeds insights back to managing-roadmaps for process optimization.
  NOT for: incident post-mortems (use root-cause-identifier agent),
  risk identification (use managing-project-risks).
  Keywords: retrospective, lessons learned, action items, continuous improvement.
---

# Facilitating Retrospectives

*Structured reflection and continuous improvement through team retrospectives*

## Contents

- [When to Run Retrospectives](#when-to-run-retrospectives)
- [Retrospective Formats](#retrospective-formats)
- [Facilitation Checklist](#facilitation-checklist)
- [Action Item Template](#action-item-template)
- [Improvement Velocity Tracking](#improvement-velocity-tracking)
- [Lessons Learned Archive](#lessons-learned-archive)
- [Integration with Other Skills](#integration-with-other-skills)
- [Anti-Patterns](#anti-patterns-never-do)
- [Quick Reference](#quick-reference)

---

## When to Run Retrospectives

### Retrospective Types

| Type | Frequency | Duration | Focus |
|------|-----------|----------|-------|
| **Sprint Retro** | End of each sprint | 30-60 min | Recent work, immediate improvements |
| **Milestone Retro** | Major deliverable complete | 60-90 min | Broader patterns, strategic insights |
| **Stage Retro** | MVP→Alpha→Beta→GA transitions | 90-120 min | Phase learnings, next phase prep |
| **Project Retro** | Project completion | 2-3 hours | Full lifecycle, organizational learning |
| **Ad-hoc** | After incidents/pivots | 30-45 min | Specific event, targeted learnings |

### When NOT to Run Retrospectives

| Situation | Alternative |
|-----------|-------------|
| Active incident | Use incident response process first |
| Team conflict | Address conflict directly first |
| Major scope change announced | Wait for clarity |
| Team exhausted/demoralized | Short check-in, defer full retro |

---

## Retrospective Formats

### Format 1: Start/Stop/Continue (Simple, Quick)

| Column | Question | Example Items |
|--------|----------|---------------|
| **Start** | What should we begin doing? | "Start daily standups", "Start code reviews" |
| **Stop** | What should we stop doing? | "Stop long meetings", "Stop skipping tests" |
| **Continue** | What's working well? | "Continue pair programming", "Continue weekly demos" |

**Best for**: Regular sprint retros, time-constrained sessions

### Format 2: 4Ls (Comprehensive)

| Column | Question | Focus |
|--------|----------|-------|
| **Liked** | What did you enjoy? | Celebrate successes |
| **Learned** | What did you discover? | Capture knowledge |
| **Lacked** | What was missing? | Identify gaps |
| **Longed For** | What do you wish for? | Future aspirations |

**Best for**: Milestone retros, team morale check

### Format 3: Sailboat (Visual, Engaging)

| Element | Represents | Question |
|---------|------------|----------|
| **Wind** | Helping forces | What pushed us forward? |
| **Anchor** | Hindering forces | What held us back? |
| **Rocks** | Risks ahead | What could hurt us? |
| **Island** | Goal/destination | Where are we heading? |

**Best for**: Visual teams, engagement when energy is low

### Format 4: What Went Well / What Could Improve

| Column | Focus |
|--------|-------|
| **Went Well** | Successes, wins, positive experiences |
| **Could Improve** | Challenges, friction, opportunities |

**Best for**: New teams, straightforward situations

### Format Selection Guide

| Situation | Recommended Format |
|-----------|-------------------|
| Short on time | Start/Stop/Continue |
| Low team energy | Sailboat (visual engagement) |
| First retro together | What Went Well / Could Improve |
| Milestone complete | 4Ls (comprehensive) |
| Recurring issues | Mad/Sad/Glad + targeted analysis |

---

## Facilitation Checklist

### Before the Retrospective

- [ ] Schedule with adequate notice (48h+ for sprint, 1 week for milestone)
- [ ] Choose format appropriate to context
- [ ] Prepare materials (board, stickies, timer)
- [ ] Review previous retro action items
- [ ] Send pre-work if needed (gather data, reflect)

### During the Retrospective

- [ ] Set the stage (purpose, psychological safety reminder)
- [ ] Timebox each phase (gather: 10-15min, discuss: 20-30min, decide: 10-15min)
- [ ] Ensure equal participation (round-robin, dot voting)
- [ ] Focus on behaviors/processes, not individuals
- [ ] Capture action items with owners and deadlines
- [ ] Summarize decisions and commitments

### After the Retrospective

- [ ] Document outcomes within 24 hours
- [ ] Share summary with team and stakeholders
- [ ] Add action items to backlog/task system
- [ ] Track action completion in next retro
- [ ] Archive lessons learned

### Psychological Safety Reminders

| Principle | How to Reinforce |
|-----------|------------------|
| **No blame** | "We focus on systems, not individuals" |
| **Confidentiality** | "What's said here stays here" |
| **Honesty** | "We need truth to improve" |
| **Respect** | "All perspectives are valid" |

---

## Action Item Template

### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| **Problem** | Issue identified in retro | "Deployments take too long" |
| **Action** | Specific improvement step | "Automate staging deploy pipeline" |
| **Owner** | Single accountable person | @deploy-lead |
| **Deadline** | Target completion date | 2025-02-01 |
| **Status** | Open/In Progress/Done/Dropped | Open |

### Action Item Quality Criteria

- [ ] **Specific**: Clear, unambiguous action
- [ ] **Measurable**: Know when it's done
- [ ] **Achievable**: Can complete in 1-2 sprints
- [ ] **Relevant**: Addresses identified problem
- [ ] **Time-bound**: Has a deadline

---

## Improvement Velocity Tracking

### Metrics to Track

| Metric | Formula | Target |
|--------|---------|--------|
| **Completion Rate** | Actions completed / Actions created | ≥70% |
| **Cycle Time** | Days from creation to completion | <14 days |
| **Recurrence Rate** | Same issues appearing again | <20% |
| **Participation** | Team members contributing items | 100% |

### Velocity Dashboard

```markdown
## Retro Health: Sprint [N]

| Metric | This Sprint | Trend |
|--------|-------------|-------|
| Actions Created | 5 | → |
| Actions Completed | 4 | ↑ |
| Completion Rate | 80% | ↑ |
| Recurring Issues | 1 | ↓ |
| Avg Cycle Time | 10 days | ↓ |
```

### Warning Signs

| Indicator | Signal | Response |
|-----------|--------|----------|
| Completion < 50% | Too many actions, unclear owners | Reduce scope, clarify ownership |
| Same issues 3+ times | Actions not addressing root cause | Deeper analysis, escalate |
| Participation < 70% | Disengagement, safety concerns | 1:1s, format change |

---

## Lessons Learned Archive

### Archive Structure

```markdown
## Lesson: [Title]
**Date**: [When learned]
**Context**: [Sprint/Milestone/Project]
**Category**: [Process/Technical/Communication/Planning]

### What Happened
[Brief description of situation]

### What We Learned
[Key insight or discovery]

### Applied Changes
[How we changed based on learning]

### Tags
[searchable keywords]
```

### Archive Best Practices

| Practice | Rationale |
|----------|-----------|
| Archive within 1 week | Details fade quickly |
| Use consistent categories | Enables pattern analysis |
| Include both success & failure | Learn from both |
| Reference in onboarding | Transfer knowledge to new members |
| Review quarterly | Surface cross-project patterns |

---

## Integration with Other Skills

| Skill | Integration Point |
|-------|-------------------|
| `managing-roadmaps` | Process optimizations feed capacity planning |
| `managing-project-risks` | New risks surface during retrospectives |
| `managing-stakeholder-engagement` | Communication improvements identified |
| `estimating-and-tracking` | Estimation accuracy feedback loop |

### Handoff Patterns

| From | To | Trigger |
|------|----|---------| 
| This skill | `managing-project-risks` | Risk identified in retro |
| This skill | `managing-roadmaps` | Process change affects capacity |
| `root-cause-identifier` agent | This skill | Post-incident retro needed |

---

## Anti-Patterns (NEVER DO)

| Anti-Pattern | Why Problematic | Correct Approach |
|--------------|-----------------|------------------|
| Blame individuals | Destroys psychological safety | Focus on systems and processes |
| No follow-up on actions | Creates cynicism, wastes time | Track and review every sprint |
| Same format every time | Engagement drops | Rotate formats |
| Skip when busy | Problems compound | Short retro > no retro |
| Too many action items | Nothing gets done | Max 3-5 actions per retro |
| Only negative focus | Demoralizing | Balance with celebrations |
| Manager dominates | Suppresses honest feedback | Facilitate, don't lead |
| No documentation | Lessons lost | Archive within 1 week |

---

## Quick Reference

```
Retrospective Timing:
  Sprint   = End of sprint (30-60 min)
  Milestone = Major deliverable (60-90 min)
  Stage    = MVP→Alpha→Beta→GA (90-120 min)
  Project  = Completion (2-3 hours)

Formats:
  Start/Stop/Continue = Quick, simple
  4Ls                 = Comprehensive (Liked/Learned/Lacked/Longed)
  Sailboat            = Visual (Wind/Anchor/Rocks/Island)
  WWW/CI              = Straightforward (Went Well / Could Improve)

Facilitation Flow:
  1. Set stage (5 min)  = Purpose, safety
  2. Gather (10-15 min) = Individual input
  3. Discuss (20-30 min)= Group analysis
  4. Decide (10-15 min) = Action items

Action Item Fields:
  Problem | Action | Owner | Deadline | Status

Metrics:
  Completion Rate ≥70% | Cycle Time <14d | Recurrence <20%
```

---

## Thinking Frameworks

**Full Catalog**: `.claude/docs/00-core/frameworks/README.md`

**Most Relevant for Retrospectives**:

| Framework | When to Use |
|-----------|-------------|
| [5 Whys](../../docs/00-core/frameworks/analysis.md) | Drilling into recurring issues |
| [SCAMPER](../../docs/00-core/frameworks/problem-solving.md) | Generating improvement ideas |

> **Selection Tip**: recurring issues→5 Whys, improvement ideas→SCAMPER
