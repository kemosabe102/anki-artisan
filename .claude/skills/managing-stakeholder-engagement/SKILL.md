---
name: managing-stakeholder-engagement
description: >
  Use this skill when identifying stakeholders, planning communications, 
  managing expectations, or preparing status updates. Covers RACI matrices,
  communication cadences, stakeholder mapping, and escalation protocols.
  Runs THROUGHOUT all project phases (parallel activity, not sequential).
  NOT for: business goal alignment (use assessing-business-alignment),
  requirements gathering (use gathering-requirements).
  Keywords: stakeholder, RACI, status update, demo planning, escalation.
---

# Managing Stakeholder Engagement

*Communication planning, expectation management, and stakeholder mapping throughout the project lifecycle*

---

## Contents

1. [Stakeholder Identification Matrix](#stakeholder-identification-matrix)
2. [RACI Framework](#raci-framework)
3. [Communication Cadence Planning](#communication-cadence-planning)
4. [Status Report Templates](#status-report-templates)
5. [Demo & Review Preparation](#demo--review-preparation)
6. [Expectation Management](#expectation-management)
7. [Escalation Protocols](#escalation-protocols)
8. [Relationship to Other Skills](#relationship-to-other-skills)
9. [Anti-Patterns](#anti-patterns-never-do)
10. [Quick Reference](#quick-reference)

---

## Stakeholder Identification Matrix

### Power/Interest Grid

Classify stakeholders by their power to influence and their interest level:

| Quadrant | Power | Interest | Strategy |
|----------|-------|----------|----------|
| **Manage Closely** | High | High | Regular 1:1s, involve in decisions |
| **Keep Satisfied** | High | Low | Periodic updates, consult on major changes |
| **Keep Informed** | Low | High | Regular broadcasts, invite to demos |
| **Monitor** | Low | Low | Minimal engagement, on-demand updates |

### Stakeholder Categories

| Category | Typical Roles | Primary Concern |
|----------|---------------|-----------------|
| **Sponsors** | Executives, budget owners | ROI, strategic alignment |
| **Users** | End users, customers | Usability, functionality |
| **Technical** | Architects, ops teams | Feasibility, integration |
| **Regulatory** | Compliance, legal | Risk, audit requirements |

### Identification Checklist

- [ ] Who approves budget/resources?
- [ ] Who will use the deliverable?
- [ ] Who must integrate with this work?
- [ ] Who has veto power?
- [ ] Who will maintain this long-term?

---

## RACI Framework

**R**esponsible • **A**ccountable • **C**onsulted • **I**nformed

### RACI Template

| Decision/Task | Sponsor | PM | Tech Lead | Dev Team | Stakeholder |
|---------------|---------|-----|-----------|----------|-------------|
| Requirements approval | A | R | C | I | C |
| Architecture decisions | I | C | A | R | I |
| Sprint priorities | A | R | C | I | C |
| Release approval | A | R | C | I | I |
| Incident response | I | C | A | R | I |


### RACI Rules

1. **One A per row**: Only one person is Accountable
2. **A implies R**: The Accountable person can also be Responsible
3. **Minimize C**: Too many Consulted slows decisions
4. **I is passive**: Informed parties receive updates, not asked

---

## Communication Cadence Planning

### Cadence Matrix

| Stakeholder Type | Frequency | Channel | Content Level |
|------------------|-----------|---------|---------------|
| Sponsors (High Power) | Weekly | 1:1 meeting | Executive summary |
| Product Owners | Daily/standup | Slack + meetings | Detailed status |
| Tech Stakeholders | Weekly | Email + meetings | Technical details |
| End Users | Milestone | Demo sessions | Feature previews |
| Executives | Monthly | Written report | KPIs + highlights |

### Event Triggers (Beyond Regular Cadence)

| Event | Notify | Within | Channel |
|-------|--------|--------|---------|
| Major blocker | Sponsor + PM | 4 hours | Direct message |
| Scope change | All RACI "C" | 24 hours | Email |
| Milestone complete | All "I" | 48 hours | Broadcast |
| Risk materialized | Sponsor | Immediate | Call/urgent msg |
| Release scheduled | All stakeholders | 1 week prior | Email |

---

## Status Report Templates

### Executive Summary (Weekly)

```markdown
## Status: [Project Name] - Week of [Date]

**Overall Health**: 🟢 On Track | 🟡 At Risk | 🔴 Blocked

### Key Accomplishments
- [Accomplishment 1]
- [Accomplishment 2]

### Next Week Focus
- [Priority 1]
- [Priority 2]

### Risks & Blockers
| Risk | Impact | Mitigation | Owner |
|------|--------|------------|-------|
| [Risk] | [H/M/L] | [Action] | [Name] |

### Metrics
- Sprint velocity: X points
- Completion: X% of planned scope
```

### Technical Status (Weekly)

```markdown
## Technical Status: [Sprint/Week]

### Completed
- [PR/Feature]: [Brief description]

### In Progress
- [Task]: [% complete, blockers]

### Architecture Decisions
- [ADR-XXX]: [Decision summary]

### Technical Debt
- Added: [description]
- Paid down: [description]
```

---

## Demo & Review Preparation

### Pre-Demo Checklist

- [ ] Environment verified working (test all demo paths)
- [ ] Backup demo recording prepared (in case of failures)
- [ ] Stakeholder calendar confirmed
- [ ] Demo script written with timing estimates
- [ ] Feedback capture mechanism ready (form/doc)
- [ ] Known limitations documented (avoid surprises)

### Demo Structure (30 min)

| Segment | Duration | Content |
|---------|----------|---------|
| Context | 3 min | Why we built this, problem solved |
| Demo | 15 min | Live walkthrough of features |
| Comparison | 5 min | Before/after, metrics improvement |
| Q&A | 5 min | Stakeholder questions |
| Next Steps | 2 min | Upcoming work, feedback process |

### Feedback Capture Template

```markdown
## Demo Feedback: [Feature Name] - [Date]

### Attendees
- [Name, Role]

### Positive Feedback
- [What worked well]

### Concerns/Questions
- [Issue raised] → [Response/Action]

### Change Requests
| Request | Priority | Decision |
|---------|----------|----------|
| [Request] | [H/M/L] | [Accept/Defer/Reject] |

### Action Items
- [ ] [Action] - Owner - Due date
```

---

## Expectation Management

### Setting Expectations Framework

| Stage | Expectation to Set | Communication |
|-------|-------------------|---------------|
| **Kickoff** | Scope boundaries, timeline ranges | Written + verbal |
| **Planning** | Sprint goals, known risks | Sprint planning doc |
| **Execution** | Progress pace, blockers | Daily/weekly updates |
| **Delivery** | What's included/excluded | Release notes |

### Under-Promise, Over-Deliver Patterns

1. **Buffer estimates**: Add 20-30% contingency, communicate lower bound
2. **Scope clarity**: Explicitly state what's NOT included
3. **Risk transparency**: Surface risks early, before they're problems
4. **Progress honesty**: Report actual status, not aspirational

### Difficult Conversation Framework

When delivering bad news:

1. **Lead with facts**: "We discovered X during testing"
2. **Explain impact**: "This means Y for the timeline"
3. **Present options**: "We can do A, B, or C"
4. **Recommend**: "I recommend B because..."
5. **Commit**: "I'll update you by [date] on progress"

---

## Escalation Protocols

### Escalation Triggers

| Trigger | Escalate To | Timeframe |
|---------|-------------|-----------|
| Blocker >24h unresolved | Tech Lead | Same day |
| Scope creep >20% | PM + Sponsor | Within 24h |
| Resource conflict | PM | Same day |
| Stakeholder unresponsive >48h | Their manager | Within 48h |
| Critical defect in production | Incident commander | Immediate |

### Escalation Communication Template

```markdown
## Escalation: [Issue Title]

**Severity**: [Critical/High/Medium]
**Date**: [When identified]
**Escalated By**: [Name]
**Escalated To**: [Name]

### Issue Summary
[1-2 sentences describing the problem]

### Impact
- [Business impact]
- [Timeline impact]
- [Resource impact]

### Attempted Resolution
- [Action 1] → [Result]
- [Action 2] → [Result]

### Request
[Specific ask: decision needed, resource, unblocking action]

### Deadline for Decision
[Date/time by which decision is needed]
```

### Conflict Resolution Steps

1. **Direct conversation**: Try to resolve 1:1 first
2. **Facilitate discussion**: Bring parties together with neutral facilitator
3. **Escalate with documentation**: If unresolved, escalate with written history
4. **Decision authority**: Designated decision-maker makes final call

---

## Relationship to Other Skills

| Skill | Relationship |
|-------|--------------|
| `gathering-requirements` | Stakeholder engagement identifies WHO to interview; gathering-requirements defines WHAT to ask |
| `assessing-business-alignment` | Business alignment validates strategic fit; stakeholder engagement manages ongoing communication |
| `managing-roadmaps` | Roadmap updates trigger stakeholder communications at milestones |
| `facilitating-retrospectives` | Retrospective insights may require stakeholder communication about process changes |

---

## Anti-Patterns (NEVER DO)

| Anti-Pattern | Why Problematic | Correct Approach |
|--------------|-----------------|------------------|
| Stakeholder bypass | Breeds distrust, causes misalignment | Always include appropriate stakeholders |
| Over-communication | Causes notification fatigue | Follow cadence matrix, be concise |
| Under-communication | Stakeholders feel uninformed | Proactive updates, especially on risks |
| Surprise delivery | Stakeholders unprepared for changes | Demo early and often, get feedback |
| Blame-shifting | Damages relationships | Focus on solutions, not fault |
| Promising without checking | Creates false expectations | Always verify before committing |

---

## Quick Reference

### Communication Frequency

| Stakeholder | Minimum Cadence |
|-------------|-----------------|
| Sponsor | Weekly 1:1 |
| Product Owner | Daily standup |
| Tech Lead | Daily async |
| End Users | Per milestone |
| Executives | Monthly report |

### RACI Quick Rules

- One "A" per decision
- "C" slows things down—minimize
- "I" is passive notification

### Escalation Thresholds

- Blocker: 24h → escalate
- Scope creep: >20% → escalate
- Unresponsive: 48h → escalate

### Key Templates

1. Executive Status Report (weekly)
2. Demo Feedback Capture
3. Escalation Communication
4. RACI Matrix

---

## Thinking Frameworks

When facing stakeholder challenges, these frameworks guide systematic problem-solving.

**Full Catalog**: [Thinking Frameworks README](../../docs/00-core/frameworks/README.md)

**Most Relevant for Stakeholder Engagement**:

| Framework | When to Use |
|-----------|-------------|
| [Eisenhower Matrix](../../docs/00-core/frameworks/problem-solving.md) | Prioritizing communications by urgency/importance |
| [5W1H](../../docs/00-core/frameworks/analysis.md) | Structuring stakeholder discovery |

> **Selection Tip**: prioritization→Eisenhower, discovery→5W1H
