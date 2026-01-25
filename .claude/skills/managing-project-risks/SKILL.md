---
name: managing-project-risks
description: >
  Use this skill for ONGOING risk management: maintaining risk registers,
  tracking risk status, planning mitigations, and reviewing risks at
  sprint boundaries. Extends assessing-business-alignment's initial P×I×E
  scoring with continuous monitoring and mitigation tracking.
  NOT for: initial business risk assessment (use assessing-business-alignment),
  contingency planning (use contingency-planner agent for complex scenarios).
  Keywords: risk register, risk tracking, mitigation, technical debt as risk.
---

# Managing Project Risks

*Ongoing risk identification, tracking, and mitigation throughout project lifecycle*

## Contents

- [Risk Identification Techniques](#risk-identification-techniques)
- [5 Risk Categories](#5-risk-categories)
- [P×I×E Scoring Formula](#pie-scoring-formula)
- [Risk Register Template](#risk-register-template)
- [Mitigation Strategy Patterns](#mitigation-strategy-patterns)
- [Risk Review Cadence](#risk-review-cadence)
- [Technical Debt as Risk](#technical-debt-as-risk)
- [Risk Trigger Conditions](#risk-trigger-conditions)
- [Escalation Thresholds](#escalation-thresholds)
- [Integration with Other Skills](#integration-with-other-skills)
- [Anti-Patterns](#anti-patterns-never-do)
- [Quick Reference](#quick-reference)

---

## Risk Identification Techniques

### Pre-Mortem Analysis

**When**: Sprint planning, milestone kickoffs, new feature starts

| Step | Action | Output |
|------|--------|--------|
| 1 | Assume the project has failed | Failure scenario |
| 2 | List all possible causes | Cause inventory |
| 3 | Prioritize by likelihood | Sorted risk list |
| 4 | Develop preventive measures | Mitigation plan |

### Assumption Testing

| Step | Action |
|------|--------|
| 1 | List all assumptions made in plans |
| 2 | Rate each: Confidence (1-5), Impact if wrong (1-5) |
| 3 | Low confidence + High impact = Risk |
| 4 | Convert assumptions to risks with mitigations |

### SWOT for Technical Decisions

| Quadrant | Focus | Risk Implications |
|----------|-------|-------------------|
| **Strengths** | What we do well | Over-reliance risks |
| **Weaknesses** | Known gaps | Capability risks |
| **Opportunities** | Could exploit | Scope creep risks |
| **Threats** | External factors | Environmental risks |

---

## 5 Risk Categories

| # | Category | Examples | Detection Signals |
|---|----------|----------|-------------------|
| 1 | **Scope** | Creep, unclear boundaries, gold-plating | "Just one more feature", expanding requirements |
| 2 | **Requirements** | Missing, incomplete, conflicting specs | Frequent clarification requests, blocked tasks |
| 3 | **Market** | Competitor moves, timing pressure | External news, stakeholder urgency |
| 4 | **Resource** | Team availability, skill gaps, turnover | Vacation schedules, knowledge silos |
| 5 | **Technical** | Integration complexity, dependencies, debt | Build failures, increasing bug rates |

### Category-Specific Monitoring

| Category | Primary Indicator | Frequency |
|----------|-------------------|-----------|
| Scope | Requirements change count | Per sprint |
| Requirements | Blocked task count | Daily |
| Market | Competitor activity | Weekly |
| Resource | Team capacity % | Per sprint |
| Technical | Build/test stability | Daily |

---

## P×I×E Scoring Formula

**Formula**: `Risk Score = Probability × Impact × Exposure`

### Factor Definitions

| Factor | Scale | Description |
|--------|-------|-------------|
| **Probability (P)** | 0.1-1.0 | Likelihood of occurrence |
| **Impact (I)** | 1-5 | Severity if risk materializes |
| **Exposure (E)** | 0.1-1.0 | Duration/breadth of vulnerability |

### Probability Scale

| P Value | Label | Criteria |
|---------|-------|----------|
| 0.1-0.2 | Rare | <10% chance, exceptional circumstances |
| 0.3-0.4 | Unlikely | 10-30% chance, not expected |
| 0.5-0.6 | Possible | 30-60% chance, could occur |
| 0.7-0.8 | Likely | 60-80% chance, expected to occur |
| 0.9-1.0 | Almost Certain | >80% chance, will occur unless mitigated |

### Impact Scale

| I Value | Label | Criteria |
|---------|-------|----------|
| 1 | Minimal | Minor inconvenience, easily absorbed |
| 2 | Low | Noticeable impact, workarounds exist |
| 3 | Moderate | Significant impact, requires response |
| 4 | High | Major impact, timeline/budget affected |
| 5 | Critical | Project failure, unrecoverable |

### Exposure Scale

| E Value | Label | Criteria |
|---------|-------|----------|
| 0.1-0.2 | Limited | Affects single component, short window |
| 0.3-0.4 | Contained | Affects module, bounded timeframe |
| 0.5-0.6 | Moderate | Affects multiple areas, medium duration |
| 0.7-0.8 | Broad | Cross-cutting impact, extended period |
| 0.9-1.0 | Pervasive | System-wide, entire project duration |

### Score Interpretation

| Score Range | Priority | Action Required |
|-------------|----------|-----------------|
| 0.0-0.5 | Low | Monitor, no active mitigation |
| 0.5-1.5 | Medium | Plan mitigation, implement when convenient |
| 1.5-2.5 | High | Prioritize mitigation, active tracking |
| 2.5-5.0 | Critical | Immediate mitigation, escalate to stakeholders |

---

## Risk Register Template

### Register Structure

| Field | Description | Required |
|-------|-------------|----------|
| **ID** | Unique identifier (RSK-###) | ✓ |
| **Category** | Scope/Requirements/Market/Resource/Technical | ✓ |
| **Description** | Clear risk statement | ✓ |
| **P×I×E Score** | Calculated priority | ✓ |
| **Mitigation** | Strategy and actions | ✓ |
| **Owner** | Accountable person | ✓ |
| **Status** | Open/Mitigating/Resolved/Accepted | ✓ |
| **Trigger** | Conditions that activate risk | Optional |
| **Last Updated** | Date of last review | ✓ |

### Example Entry

```markdown
| Field | Value |
|-------|-------|
| ID | RSK-007 |
| Category | Technical |
| Description | Third-party API rate limits may block data ingestion at scale |
| P×I×E | 0.7 × 4 × 0.6 = 1.68 (HIGH) |
| Mitigation | Implement caching layer, negotiate higher limits, build fallback |
| Owner | @data-team-lead |
| Status | Mitigating |
| Trigger | API errors > 5% of requests |
| Last Updated | 2025-01-15 |
```

---

## Mitigation Strategy Patterns

### Four Response Strategies

| Strategy | When to Use | Example |
|----------|-------------|---------|
| **Accept** | Low score, cost > benefit | "Monitor but don't act on minor UI inconsistencies" |
| **Avoid** | Can eliminate root cause | "Use proven library instead of custom implementation" |
| **Transfer** | Someone else can handle | "Purchase insurance, outsource to specialist" |
| **Mitigate** | Reduce P, I, or E | "Add redundancy, create fallback, buffer timeline" |

### Mitigation Action Template

```markdown
## Mitigation: [Risk ID]
**Strategy**: [Accept/Avoid/Transfer/Mitigate]
**Actions**:
1. [Specific action with owner]
2. [Specific action with owner]
**Success Criteria**: [How we know it worked]
**Review Date**: [When to reassess]
```

---

## Risk Review Cadence

### Standard Review Schedule

| Event | Frequency | Focus | Participants |
|-------|-----------|-------|--------------|
| **Daily Standup** | Daily | Blockers, triggered risks | Team |
| **Sprint Planning** | Per sprint | New risks, capacity impact | Team + PO |
| **Sprint Review** | Per sprint | Materialized risks, lessons | Stakeholders |
| **Milestone Gate** | Per milestone | Critical risks, go/no-go | Leadership |
| **Post-Incident** | As needed | Root cause, prevention | Affected teams |

### Review Actions Checklist

- [ ] Review all OPEN risks for status changes
- [ ] Check TRIGGER conditions against current metrics
- [ ] Update P×I×E scores based on new information
- [ ] Close RESOLVED risks with resolution summary
- [ ] Identify new risks from recent work
- [ ] Verify mitigation actions are progressing

---

## Technical Debt as Risk

### Debt-to-Risk Conversion

Technical debt creates risk when it:
- Slows future development (Resource risk)
- Creates fragile code paths (Technical risk)
- Accumulates interest (compound impact over time)

### Debt Tracking Formula

```
Debt_Risk_Score = Debt_Size × Accumulation_Rate × Time_Exposure

Where:
- Debt_Size: Estimated hours to fix (normalized 1-5)
- Accumulation_Rate: How fast interest compounds (0.1-1.0)
- Time_Exposure: Sprints until addressed (0.1-1.0)
```

### Debt Categories

| Type | Description | Risk Escalation |
|------|-------------|-----------------|
| **Deliberate** | Conscious trade-off, documented | Low - planned repayment |
| **Accidental** | Discovered later, unknown scope | Medium - needs investigation |
| **Bit Rot** | Gradual degradation | Medium - compounds silently |
| **Outdated** | Dependencies, patterns obsolete | High - security implications |

### Repayment Strategy

| Approach | When to Use |
|----------|-------------|
| **Incremental** | Allocate 10-20% per sprint to debt |
| **Dedicated Sprint** | Debt blocking major features |
| **Big Bang** | Debt causing incidents, must stop |

---

## Risk Trigger Conditions

### What Triggers Are

Triggers are observable conditions that indicate a risk is materializing.

### Trigger Examples by Category

| Category | Trigger Condition | Action When Triggered |
|----------|-------------------|----------------------|
| Scope | Requirements changes > 3/sprint | Freeze scope, stakeholder review |
| Requirements | Blocked tasks > 20% | Escalate to PO for clarification |
| Market | Competitor launch announcement | Strategy review session |
| Resource | Key person availability < 50% | Knowledge transfer, backup plan |
| Technical | Build failures > 2/day | Stop new work, stabilization focus |

### Trigger Monitoring

```markdown
## Trigger: [Risk ID]
**Condition**: [Measurable threshold]
**Data Source**: [Where to check]
**Check Frequency**: [How often]
**Response Plan**: [Immediate actions]
```

---

## Escalation Thresholds

### When to Escalate

| Condition | Escalation Level | Action |
|-----------|------------------|--------|
| Risk score > 2.5 | Team Lead | Immediate mitigation planning |
| Risk score > 3.5 | Project Manager | Stakeholder notification |
| Risk score > 4.0 | Leadership | Go/no-go decision required |
| Risk materialized | Incident Owner | Activate response plan |
| Mitigation failing | Original Owner + 1 | Reassess strategy |

### Escalation Communication Template

```markdown
## Risk Escalation: [Risk ID]
**Current Score**: [P×I×E calculation]
**Previous Score**: [If changed]
**Trigger Activated**: [Yes/No + details]
**Immediate Impact**: [What's affected now]
**Recommended Action**: [What needs to happen]
**Decision Needed By**: [Date/time]
```

---

## Integration with Other Skills

| Skill | Integration Point |
|-------|-------------------|
| `assessing-business-alignment` | Initial P×I×E scoring during plan review |
| `managing-roadmaps` | Risk status feeds sprint capacity decisions |
| `roadmap-lifecycle` | Critical risks affect stage gate assessments |
| `facilitating-retrospectives` | Retrospectives surface new risks |
| `managing-stakeholder-engagement` | Risk escalations use communication channels |

### Handoff Patterns

| From | To | Trigger |
|------|----|---------| 
| `assessing-business-alignment` | This skill | Initial risks identified in plan review |
| This skill | `contingency-planner` agent | Complex failure modes need deep analysis |
| This skill | `roadmap-lifecycle` | Risk findings affect stage readiness |
| `facilitating-retrospectives` | This skill | New risks surfaced in retro |

---

## Anti-Patterns (NEVER DO)

| Anti-Pattern | Why Problematic | Correct Approach |
|--------------|-----------------|------------------|
| Set-and-forget risks | Risks evolve, stale data useless | Review every sprint |
| Score without evidence | Gut feelings unreliable | Use measurable triggers |
| All risks same priority | Everything urgent = nothing urgent | P×I×E scoring required |
| No owner assigned | Diffusion of responsibility | Every risk has one owner |
| Mitigation without deadline | Actions never complete | Time-bound mitigation plans |
| Ignore low-score risks | They can escalate | Monitor, review periodically |
| Skip post-incident review | Miss prevention opportunities | Always conduct retrospective |
| Technical debt not tracked | Hidden risk accumulation | Track as Technical category |

---

## Quick Reference

```
P×I×E Formula:
  Risk_Score = Probability × Impact × Exposure
  P: 0.1-1.0 (likelihood)
  I: 1-5 (severity)
  E: 0.1-1.0 (vulnerability window)

Score Thresholds:
  0.0-0.5  = Low (monitor)
  0.5-1.5  = Medium (plan mitigation)
  1.5-2.5  = High (prioritize)
  2.5-5.0  = Critical (immediate action)

5 Categories: Scope | Requirements | Market | Resource | Technical

4 Response Strategies: Accept | Avoid | Transfer | Mitigate

Review Cadence:
  Daily     = Blockers, triggered risks
  Sprint    = New risks, capacity impact
  Milestone = Critical risks, go/no-go
  Incident  = Root cause, prevention

Escalation:
  Score > 2.5 = Team Lead
  Score > 3.5 = Project Manager
  Score > 4.0 = Leadership
  Materialized = Incident response

Risk Register Fields:
  ID | Category | Description | P×I×E | Mitigation | Owner | Status | Trigger
```

---

## Thinking Frameworks

**Full Catalog**: `.claude/docs/00-core/frameworks/README.md`

**Most Relevant for Risk Management**:

| Framework | When to Use |
|-----------|-------------|
| [Pre-Mortem](../../docs/00-core/frameworks/strategy.md) | Identifying risks before they occur |
| [5 Whys](../../docs/00-core/frameworks/analysis.md) | Root cause analysis for materialized risks |
| [SWOT](../../docs/00-core/frameworks/analysis.md) | Structured risk identification |

> **Selection Tip**: identification→Pre-Mortem/SWOT, analysis→5 Whys, mitigation→SCAMPER
