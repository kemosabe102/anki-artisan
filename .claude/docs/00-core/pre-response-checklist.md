---
title: "Pre-Response Checklist"
date: 2025-11-26
status: ACTIVE
auto-load: true
tags: [orchestrator, checklist, claude-docs]
---

# Pre-Response Checklist

**Purpose**: Validate before EVERY response. Silent self-check, not shown to user.

## Phase Awareness

- [ ] **Phase Identified**: ANALYSIS | DECISION | IMPLEMENT | VALIDATE
- [ ] **Loop Correct**: Using appropriate OODA loop for phase
  - ANALYSIS: OBSERVE <-> ORIENT (gather context, explore options)
  - DECISION: ORIENT <-> DECIDE (plan, assign agents)
  - IMPLEMENT: DECIDE <-> ACT (execute tasks)
  - VALIDATE: ACT <-> OBSERVE (verify quality)
- [ ] **Transition Check**: Exit criteria met? Consider phase transition (see table below)

## Context Quality

- [ ] **CQ Threshold**:
  - IMPLEMENT phase: CQ >= 0.85 required
  - Other phases: CQ >= 0.70 acceptable
- [ ] **Gaps Explicit**: Unknown areas acknowledged
- [ ] **Research Triggered**: If CQ < threshold -> delegate to researcher-*

## Agent Selection (if delegating)

- [ ] **Phase-Appropriate**: Agents match current phase (see Quick Reference)
- [ ] **ASC >= 0.5**: Confidence calculated for each agent
- [ ] **Parallelization**: Independent tasks launched together (max 5 agents)

## User Guidance

- [ ] **Next Steps Clear**: User knows what happens next
- [ ] **Decision Points**: Surfaced choices user needs to make
- [ ] **Progress Visible**: TodoWrite updated if multi-step

## Response Quality

- [ ] **Evidence Provided**: Citations, confidence scores where relevant
- [ ] **Uncertainty Acknowledged**: Gaps/assumptions stated
- [ ] **Actionable**: User can act on response

---

## Phase Transition Signals

| From -> To | User Signals | Orchestrator Action |
|------------|--------------|---------------------|
| ANALYSIS -> DECISION | "Let's do X", "I want to...", requirements concrete | Propose approach, agent assignments |
| DECISION -> IMPLEMENT | "Go ahead", "Approved", plan accepted | Begin execution, track with TodoWrite |
| IMPLEMENT -> VALIDATE | Tasks complete, code written | Run reviews, tests, verification |
| VALIDATE -> (complete) | All checks pass, user satisfied | Summarize, offer commit |
| Any -> ANALYSIS | "Wait", "What about...", new questions | Return to exploration |

---

## Quick Reference: Agents by Phase

| Phase | Primary Agents | Purpose |
|-------|---------------|---------|
| ANALYSIS | researcher-*, context-readiness-assessor | Gather context, explore options |
| DECISION | planning, planning, feature-analyzer | Plan, break down, assign |
| IMPLEMENT | development, claude-code-ecosystem, debugger, code-quality | Execute tasks |
| VALIDATE | code-quality, code-quality, sast-scanner, tech-debt-investigator | Verify quality |

**Full agent list**: `orchestrator-workflow.md` (Agent Legend section)

---

## Anti-Patterns (Quick Check)

| Bad | Good |
|-----|------|
| Implementing during ANALYSIS | Delegate to researcher-* first |
| Skipping ORIENT (CQ < 0.85) | Research until CQ >= 0.85 |
| Direct execution when agent exists | Always delegate if ASC >= 0.5 |
| Vague "working on it" responses | Concrete next steps with agents |

---

**This checklist is internal validation. Do not include checklist items in user responses.**
