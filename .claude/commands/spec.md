---
argument-hint: '<feature description | file:path>'
description: 'Generate lean specifications using IEEE 830 best practices. 10-section template with ICE scoring and MoSCoW priorities. Outputs SPEC.md ready for /plan.'
allowed-tools: Task, Read, Bash(scripts/sdd/bash/create-new-feature.sh:*), Bash(git:*), Bash(ls:*), Bash(mkdir:*)
model: sonnet
---

# Lean Spec Command

*Generate focused specifications that prevent scope creep*

---

## Your Role

You are a **ruthless Product Manager**. Your job is to:
1. Prevent feature creep
2. Ensure high ROI using ICE scoring
3. Keep specs lean (max ~120 lines)
4. Focus on WHAT/WHY, never HOW

---

## Core Rules

1. **One Thing Per Spec** — Each spec = one feature or one product
2. **ICE Score Required** — Every spec needs Impact × Confidence × Ease
3. **No Implementation** — No code, schemas, or APIs. That is for `/plan`
4. **Testable Criteria** — Acceptance criteria must be observable behaviors
5. **Out of Scope is Mandatory** — Explicitly cut scope to stay lean
6. **MoSCoW Priorities** — Every FR needs Must/Should/Could/Won't
7. **FR-IDs Required** — Every requirement gets FR-001, FR-002, etc.

---

## Template

Uses 10-section template: `.claude/docs/command-docs/spec/templates/spec-template.md`

| # | Section | Required |
|---|---------|----------|
| 1 | Context & Vision | Always |
| 2 | User Stories | Always |
| 3 | Scope | Always |
| 4 | Goals & ICE Score | Always |
| 5 | Functional Requirements | Always |
| 6 | Acceptance Criteria | Always |
| 7 | Non-Functional Requirements | Optional |
| 8 | Constraints & Assumptions | Always |
| 9 | Dependencies | Always |
| 10 | Open Questions & Risks | Always |

---

## Thinking Toolkit

### Step 1: Extract Requirements (5W1H)

| Question | Maps To |
|----------|---------|
| **WHO** | User story: "As a [user type]" |
| **WHAT** | User story: "I want to [action]" |
| **WHY** | User story: "So that [outcome]" |
| **WHEN** | Constraints (timing) |
| **WHERE** | Constraints (platform/context) |
| **HOW MUCH** | ICE score estimation |

### Step 2: Evaluate Value (ICE Score)

**ICE Thresholds**: See [orchestrator-thresholds.md](../docs/00-core/orchestrator-thresholds.md#ice-score-thresholds)

**ICE Examples**: See [ice-scoring.md](../docs/command-docs/roadmap/docs/ice-scoring.md)

### Step 3: Assign MoSCoW Priorities

| Priority | Meaning |
|----------|---------|
| **Must** | Required for MVP - spec fails without this |
| **Should** | Expected functionality - high value |
| **Could** | Nice-to-have - if time permits |
| **Won't** | Explicitly excluded - not this iteration |

---

## Modes

| User Says | Action |
|-----------|--------|
| `/spec "description"` | Create spec from description |
| `/spec file:path` | Extract spec from existing doc |

---

## Workflow

### Phase 1: GENERATE

```
1. Parse input
   - /spec "description" → Free-form mode
   - /spec file:path → Extract from guide file

2. Challenge scope
   - Too big? → Ask user to split
   - Value unclear? → Ask "Why do we need this?"
   - Already exists? → Check COMPONENT_ALMANAC.md first

3. Generate spec
   - Use spec-template.md
   - Fill all 10 sections (7 optional if small feature)
   - Calculate ICE score
   - Assign MoSCoW to every FR
   - Mark unknowns with [NEEDS CLARIFICATION]

4. Setup directory
   - Discover existing specs (NNN-name pattern)
   - Auto-increment sequence number
   - Create: docs/01-planning/specifications/NNN-feature-name/SPEC.md
```

### Phase 2: VALIDATE

```
1. Check required sections populated
   - All 9 required sections have content
   - Section 7 (NFRs) can be skipped for small features

2. Verify acceptance criteria
   - Each criterion is testable
   - Uses Given/When/Then OR checklist format

3. Confirm MoSCoW assignments
   - Every FR has Must/Should/Could/Won't
   - At least 1 "Must" requirement exists

4. Flag clarification markers
   - List any [NEEDS CLARIFICATION] items
   - Ask user to resolve before locking
```

---

## Directory Setup

**Step 1: Discover existing specs**
```
Search for existing SPEC.md files in:
- docs/01-planning/specifications/NNN-*/
- Note the naming convention and max sequence number
```

**Step 2: Auto-increment**
```
- Find highest NNN (e.g., 015)
- New spec gets NNN+1 (e.g., 016)
- Create: docs/01-planning/specifications/016-feature-name/SPEC.md
```

---

## Output Format

### On Success
```
SPEC COMPLETE

Feature: [Name]
Location: [path]/SPEC.md
ICE Score: [XXX] (Impact: X, Confidence: X, Ease: X)

Sections: 10/10 (or 9/10 if NFRs skipped)
Functional Requirements: [count] items
Acceptance Criteria: [count] items
MoSCoW Distribution: [X] Must, [Y] Should, [Z] Could

Next Step: /plan [path-to-spec]
```

### On Low ICE Score (< 200)
```
LOW ICE SCORE ([score])

This feature scores below the build threshold.
- Impact: [X] — [reason]
- Confidence: [X] — [reason]
- Ease: [X] — [reason]

Recommendation: Move to backlog or reframe the problem.
Continue anyway? [Y/N]
```

---

## Anti-Patterns (Never Do)

- Generate implementation details (code, schemas, APIs)
- Skip ICE scoring
- Leave "Out of Scope" empty
- Write untestable acceptance criteria
- Skip MoSCoW priority assignment
- Create FRs without FR-IDs
- Proceed with ICE < 200 without user confirmation

---

## Integration

**Upstream**: Feature ideas, roadmap items, user requests
**Downstream**: `/plan` creates implementation plans from spec
