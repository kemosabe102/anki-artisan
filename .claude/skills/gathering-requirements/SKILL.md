---
name: gathering-requirements
description: >
  Use this skill when starting from scratch: gathering requirements,
  writing user stories, conducting stakeholder discovery, or defining
  acceptance criteria. Entry point for new features without existing specs.
  Output feeds to validating-specifications for SPEC.md quality check.
  NOT for: validating existing specs (use validating-specifications),
  stakeholder communication (use managing-stakeholder-engagement).
  Keywords: requirements, user story, discovery, INVEST, acceptance criteria.
---

# Gathering Requirements

*Requirements elicitation, user story writing, and discovery techniques*

---

## Contents

1. [When This Skill Applies](#when-this-skill-applies)
2. [Elicitation Techniques](#elicitation-techniques)
3. [User Story Format](#user-story-format)
4. [INVEST Criteria](#invest-criteria)
5. [Acceptance Criteria Patterns](#acceptance-criteria-patterns)
6. [Scope Boundary Definition](#scope-boundary-definition)
7. [Prioritization Frameworks](#prioritization-frameworks)
8. [Handoff to validating-specifications](#handoff-to-validating-specifications)
9. [Relationship to Other Skills](#relationship-to-other-skills)
10. [Anti-Patterns](#anti-patterns-never-do)
11. [Quick Reference](#quick-reference)

---

## When This Skill Applies

### Use This Skill When

- Starting a new feature from scratch (no existing SPEC.md)
- Stakeholder has a problem but no documented requirements
- Discovery phase for new product area
- Converting informal requests to formal specifications

### Skip Ahead When

| Situation | Skip To |
|-----------|---------|
| SPEC.md already exists | `validating-specifications` |
| Clear requirements, need architecture | `reviewing-architecture` |
| Requirements validated, need tasks | `generating-tasks` |

---

## Elicitation Techniques

### Stakeholder Interviews

**Question Templates by Category**:

| Category | Questions |
|----------|-----------|
| **Problem** | "What problem are you trying to solve?" "What happens if we don't solve this?" |
| **Current State** | "How do you handle this today?" "What's painful about the current process?" |
| **Success** | "How will you know this is successful?" "What metrics matter?" |
| **Constraints** | "What must not change?" "What are the technical/business limits?" |
| **Priority** | "If we could only deliver one thing, what would it be?" |

### Jobs-to-Be-Done Framework

```
When [situation], I want to [motivation], so I can [expected outcome].
```

**Example**:
> When I'm reviewing a pull request, I want to see test coverage changes, so I can ensure quality isn't regressing.

### User Journey Mapping

| Stage | User Action | Pain Points | Opportunities |
|-------|-------------|-------------|---------------|
| Awareness | Discovers need | Unclear where to start | Onboarding flow |
| Consideration | Evaluates options | Too many choices | Guided selection |
| Decision | Chooses solution | Fear of wrong choice | Easy reversal |
| Use | Executes task | Friction points | Streamlined flow |
| Retention | Returns/recommends | Forgetting how | Quick actions |

### Feature Workshop Facilitation

**Workshop Structure (2 hours)**:

| Segment | Duration | Activity |
|---------|----------|----------|
| Context setting | 15 min | Problem statement, goals |
| Diverge | 30 min | Brainstorm solutions (silent, then share) |
| Cluster | 15 min | Group related ideas |
| Prioritize | 20 min | Dot voting on clusters |
| Converge | 30 min | Define top 3 features |
| Wrap-up | 10 min | Next steps, owners |

---

## User Story Format

### Standard Format

```
As a [user type],
I want [goal/action],
So that [benefit/value].
```

### Examples

**Good**:
> As a developer, I want to see failed test output in my PR comment, so that I can fix issues without leaving GitHub.

**Bad** (too vague):
> As a user, I want the system to be faster.

**Bad** (solution-focused):
> As a developer, I want a Redis cache, so queries are faster.

### User Story Sizing Guide

| Size | Description | Action |
|------|-------------|--------|
| **Small** | Single clear outcome | Ready for sprint |
| **Medium** | 2-3 related outcomes | May need breakdown |
| **Large** | Multiple workflows | Split into smaller stories |
| **Epic** | Entire feature area | Decompose into stories |

---

## INVEST Criteria

User stories must meet INVEST criteria before sprint planning:

| Criterion | Question | Fix If Not |
|-----------|----------|------------|
| **I**ndependent | Can be delivered without other stories? | Remove dependencies or bundle |
| **N**egotiable | Is scope flexible within the story? | Avoid over-specification |
| **V**aluable | Delivers value to user/business? | Reframe or reject |
| **E**stimable | Can team estimate effort? | Add spike, clarify scope |
| **S**mall | Fits in single sprint? | Split into smaller stories |
| **T**estable | Has clear pass/fail criteria? | Add acceptance criteria |

### INVEST Checklist

```markdown
## Story: [Title]

- [ ] **Independent**: No blocking dependencies
- [ ] **Negotiable**: Scope can adjust within story
- [ ] **Valuable**: Clear user/business value
- [ ] **Estimable**: Team can estimate (pointed)
- [ ] **Small**: Fits in one sprint
- [ ] **Testable**: Acceptance criteria defined
```


---

## Acceptance Criteria Patterns

### Given-When-Then (Gherkin)

```gherkin
Given [precondition/context]
When [action/trigger]
Then [expected outcome]
```

**Example**:
```gherkin
Given I am logged in as an admin
When I click "Delete User" and confirm
Then the user is removed and I see a success message
```

### Checklist Format

```markdown
## Acceptance Criteria

- [ ] Form validates email format before submission
- [ ] Error message displays below invalid field
- [ ] Submit button disabled until form is valid
- [ ] Success redirects to dashboard
```

### Criteria Categories

| Category | Examples |
|----------|----------|
| **Functional** | "User can filter by date range" |
| **Performance** | "Page loads in <2 seconds" |
| **Security** | "Passwords are hashed with bcrypt" |
| **Accessibility** | "Form is keyboard navigable" |
| **Error Handling** | "Invalid input shows specific message" |

---

## Scope Boundary Definition

### In-Scope vs Out-of-Scope Template

```markdown
## Scope: [Feature Name]

### In Scope
- [Specific capability 1]
- [Specific capability 2]
- [Specific capability 3]

### Out of Scope (Explicitly Excluded)
- [Capability NOT included]
- [Future consideration]

### Deferred (Future Phase)
- [Capability for later]
```

### Boundary Questions

| Question | Purpose |
|----------|---------|
| "What's the minimum to solve the problem?" | Find MVP |
| "What could we add later?" | Identify deferrals |
| "What should we never do?" | Set hard boundaries |
| "What's assumed to already exist?" | Identify dependencies |

### Scope Creep Warning Signs

| Signal | Action |
|--------|--------|
| "While we're at it..." | Capture separately, evaluate priority |
| "Can we also..." | Document as enhancement, not requirement |
| "It would be nice if..." | Add to backlog, not current scope |
| Stakeholder keeps adding | Revisit scope agreement |

---

## Prioritization Frameworks

### MoSCoW Method

| Category | Meaning | Guidance |
|----------|---------|----------|
| **M**ust Have | Critical, non-negotiable | ≤60% of effort |
| **S**hould Have | Important, workarounds exist | ~20% of effort |
| **C**ould Have | Nice to have | ~15% of effort |
| **W**on't Have | Explicitly excluded | Documented, not this release |

### Kano Model

| Feature Type | Absence | Presence | Example |
|--------------|---------|----------|---------|
| **Basic** | Dissatisfied | Neutral | Login works |
| **Performance** | Dissatisfied | Satisfied | Fast loading |
| **Excitement** | Neutral | Delighted | Unexpected shortcut |

### Value vs Effort Matrix

| Quadrant | Value | Effort | Action |
|----------|-------|--------|--------|
| Quick Wins | High | Low | Do first |
| Major Projects | High | High | Plan carefully |
| Fill-ins | Low | Low | If time permits |
| Time Sinks | Low | High | Avoid |

---

## Handoff to validating-specifications

### Pre-Handoff Checklist

Before passing to `validating-specifications`:

- [ ] User stories written with INVEST compliance
- [ ] Acceptance criteria for each story
- [ ] Scope boundaries defined (in/out/deferred)
- [ ] Prioritization applied (MoSCoW or similar)
- [ ] Stakeholder sign-off obtained

### SPEC.md Draft Structure

Create initial SPEC.md with:

```markdown
# [Feature Name] Specification

## 1. The "Why"
[Problem statement from discovery]

## 2. User Story
[Primary user story in standard format]

## 3. Acceptance Criteria
[Given-When-Then or checklist format]

## 4. Out of Scope
[Explicit exclusions]

## 5. Constraints
[Technical/business limitations]

## 6. ICE Score
- Impact: [1-10] - [rationale]
- Confidence: [1-10] - [rationale]
- Ease: [1-10] - [rationale]
- **Total**: [I × C × E]
```

---

## Relationship to Other Skills

| Skill | Relationship |
|-------|--------------|
| `validating-specifications` | This skill CREATES requirements; validating-specifications CHECKS quality |
| `managing-stakeholder-engagement` | Stakeholder skill identifies WHO to talk to; this skill defines WHAT to ask |
| `feature-design-workflow` | Architectural design happens AFTER requirements are gathered |
| `estimating-and-tracking` | Estimation happens AFTER requirements are clarified |

---

## Anti-Patterns (NEVER DO)

| Anti-Pattern | Why Problematic | Correct Approach |
|--------------|-----------------|------------------|
| Solution-first thinking | Skips problem definition | Start with "Why" before "How" |
| Forgetting the "why" | Requirements without context | Always document problem statement |
| Accepting vague requests | Leads to scope creep | Clarify with specific questions |
| Single stakeholder view | Misses perspectives | Interview multiple stakeholders |
| Gold plating | Adds unrequested features | Stick to validated requirements |
| Skipping prioritization | Everything seems urgent | Apply MoSCoW or similar |
| Oral-only requirements | No accountability, drift | Document and get sign-off |

---

## Quick Reference

### User Story Format

```
As a [who], I want [what], so that [why].
```

### INVEST Checklist

- **I**ndependent
- **N**egotiable
- **V**aluable
- **E**stimable
- **S**mall
- **T**estable

### Given-When-Then

```
Given [context]
When [action]
Then [outcome]
```

### MoSCoW Distribution

- Must: ≤60%
- Should: ~20%
- Could: ~15%
- Won't: Documented

### Key Questions

1. What problem are you solving?
2. How do you handle this today?
3. How will you measure success?
4. What are the constraints?
5. What's the minimum viable solution?

---

## Thinking Frameworks

When facing requirements challenges, these frameworks guide systematic problem-solving.

**Full Catalog**: [Thinking Frameworks README](../../docs/00-core/frameworks/README.md)

**Most Relevant for Requirements Gathering**:

| Framework | When to Use |
|-----------|-------------|
| [5 Whys](../../docs/00-core/frameworks/analysis.md) | Root cause discovery, finding real problems |
| [First Principles](../../docs/00-core/frameworks/creative.md) | Breaking assumptions, finding core needs |

> **Selection Tip**: problem discovery→5 Whys, assumption breaking→First Principles
