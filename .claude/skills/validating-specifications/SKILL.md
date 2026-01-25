---
name: validating-specifications
description: >
  Use this skill when validating SPEC.md quality, checking WHAT/WHY vs HOW boundaries, 
  scoring 5 quality dimensions, or assessing ICE scores. Trigger keywords: spec review, 
  specification quality, HOW detection, progressive disclosure, vague terms.
---

# Validating Specifications

*5-dimension quality validation with WHAT/WHY vs HOW boundary enforcement*

## Contents

- [5D Quality Scoring Framework](#5d-quality-scoring-framework)
- [Overall Grade Calculation](#overall-grade-calculation)
- [HOW Detection Patterns](#how-detection-patterns)
- [ICE Score Validation](#ice-score-validation)
- [Vague Term Index](#vague-term-index)
- [Review Checklist](#review-checklist)
- [Anti-Patterns](#anti-patterns-never-do)
- [Quick Reference](#quick-reference)

---

## 5D Quality Scoring Framework

### 1. Completeness Score (0-1.0)

| Component | Weight | Criteria |
|-----------|--------|----------|
| Functional requirements | 0.30 | All FR-XXX present and clear |
| Non-functional requirements | 0.20 | NFR specs with measurable targets |
| Acceptance scenarios | 0.20 | Clear pass/fail criteria |
| Planning Recommendations | 0.15 | Section present (from /spec command) |
| Technical architecture | 0.15 | Component breakdown defined |

### 2. Testability Score (0-1.0)

| Component | Weight | Criteria |
|-----------|--------|----------|
| Measurable criteria | 0.40 | Requirements have quantifiable metrics |
| Verifiable scenarios | 0.30 | Acceptance tests can be automated |
| Quantifiable success | 0.30 | Success metrics are numeric/observable |

### 3. Clarity Score (0-1.0)

| Component | Weight | Criteria |
|-----------|--------|----------|
| Unambiguous language | 0.40 | No vague terms (see Vague Term Index) |
| Defined terms | 0.30 | Technical terms explained |
| Consistent references | 0.30 | Internal links valid, terminology consistent |

### 4. Ambiguity Index (0-10)

| Score | Rating | Description |
|-------|--------|-------------|
| 0-2 | Excellent | Clear, precise language throughout |
| 3-5 | Acceptable | Minor ambiguities, easily resolved |
| 6-8 | Significant | Multiple unclear requirements |
| 9-10 | Critical | Pervasive ambiguity, needs rewrite |

### 5. Progressive Disclosure Score (0-1.0)

| Component | Weight | Criteria |
|-----------|--------|----------|
| Visibility | 0.25 | Core requirements in main overview |
| Structure | 0.25 | Proper hierarchy (Overview -> Core -> Details) |
| Size | 0.20 | Main SPEC <500 lines |
| Scent | 0.15 | Descriptive headings, preview hints |
| Depth | 0.15 | Maximum 2 disclosure levels |

---

## Overall Grade Calculation

### Formula

```
Overall_Score = (Completeness × 0.25) + (Testability × 0.25) + 
                (Clarity × 0.25) + ((10 - Ambiguity) / 10 × 0.15) + 
                (Progressive_Disclosure × 0.10)
```

### Grade Mapping

| Grade | Score Range | Description |
|-------|-------------|-------------|
| A | 0.90 - 1.00 | Excellent - ready for implementation |
| B | 0.80 - 0.89 | Good - minor improvements recommended |
| C | 0.70 - 0.79 | Acceptable - several issues to address |
| D | 0.60 - 0.69 | Poor - significant rework needed |
| F | < 0.60 | Failing - major rewrite required |

---

## HOW Detection Patterns

### What to Scan For

SPECs define WHAT (requirements) and WHY (rationale), NOT HOW (implementation).

| Pattern Type | Examples | Action |
|--------------|----------|--------|
| Code blocks | ```python, ```javascript | FLAG |
| Function signatures | `def function_name()`, `function()` | FLAG |
| Class definitions | `class ClassName`, interface declarations | FLAG |
| Algorithm keywords | "use binary search", "implement using" | FLAG |
| Data structures | "use a hash map", "store in array" | FLAG |
| Library specifics | "use pandas DataFrame", "import numpy" | FLAG |

### Exceptions (Allowed in SPEC)

| Context | Why Allowed |
|---------|-------------|
| Constraints section | "Must NOT use external libraries" is a constraint |
| Out of Scope section | "Will not implement caching" is scoping |
| Quoted negative examples | Showing what not to do |
| Interface contracts | API signatures as requirements (not implementation) |

### Severity Escalation

| Violations | Severity | Action |
|------------|----------|--------|
| 0 | PASS | Proceed to grade calculation |
| 1-2 | WARNING | Flag locations, continue with note |
| 3+ | CRITICAL | Recommend REJECTION |

---

## ICE Score Validation

ICE Score prioritizes specifications based on Impact, Confidence, and Ease.

### Formula

```
ICE Score = Impact × Confidence × Ease
```

### Validation Criteria

| Check | Criteria |
|-------|----------|
| Formula | Impact × Confidence × Ease = Total |
| Range | Each factor 1-10, Total 1-1000 |
| Threshold | Total < 200 = WARN (recommend backlog) |
| Rationale | Each factor has 1-sentence justification |

### Score Interpretation

> **Canonical Source**: `.claude/docs/00-core/orchestrator-thresholds.md#ice-score-thresholds`

See canonical thresholds for priority classification and phase assignment.

---

## Vague Term Index

Flag these terms in User Story and Acceptance Criteria sections:

| Term | Why Vague | Better Alternative |
|------|-----------|-------------------|
| "improve" | No measurable target | "reduce latency by 50%" |
| "enhance" | No measurable target | "add support for X feature" |
| "optimize" | No measurable target | "process 1000 items/second" |
| "better" | Comparative without baseline | "score 90% vs current 75%" |
| "faster" | No specific metric | "complete in <2 seconds" |
| "more efficient" | No specific metric | "reduce memory usage by 30%" |
| "user-friendly" | Subjective | "complete task in 3 clicks" |
| "seamless" | Subjective | "zero manual intervention required" |
| "robust" | Undefined scope | "handle 1000 concurrent users" |
| "scalable" | No target scale | "support 10x current load" |

---

## Review Checklist

### Quick Reference (All Reviews)

- [ ] All FR-XXX requirements present?
- [ ] NFRs have measurable targets?
- [ ] Acceptance scenarios verifiable?
- [ ] No vague terms used?
- [ ] Technical terms defined?
- [ ] Cross-references consistent?
- [ ] SPEC < 500 lines?
- [ ] Proper heading hierarchy?

### Lean Spec Sections (6 Required)

- [ ] 1. The "Why" - Problem statement and context
- [ ] 2. User Story - Who, what, why format
- [ ] 3. Acceptance Criteria - Observable behaviors
- [ ] 4. Out of Scope - Explicit exclusions
- [ ] 5. Constraints - Technical/business limitations
- [ ] 6. ICE Score - Impact × Confidence × Ease

### HOW Detection Checklist

- [ ] Run pattern scan on entire SPEC
- [ ] Check code blocks are in allowed sections only
- [ ] Verify no function/class definitions outside constraints
- [ ] Confirm algorithm keywords have proper context

---

## Anti-Patterns (NEVER DO)

| Anti-Pattern | Why Problematic | Correct Approach |
|--------------|-----------------|------------------|
| Modifying SPEC.md files | Reviewer is read-only | Report findings only |
| Suggesting implementation details | Violates WHAT/WHY vs HOW boundary | Focus on requirements clarity |
| Accepting SPECs with ICE < 200 without override | Low priority work | Flag for user decision |
| Skipping HOW Detection scan | Boundary enforcement is mandatory | Run on every review |
| Reviewing non-SPEC files | Out of scope | Reject with explanation |
| Vague feedback without line references | Not actionable | Cite specific locations |

---

## Quick Reference

```
SPEC Quality = 5 Dimensions + HOW-Free + ICE Valid

Dimensions (weights):
  - Completeness (0.25): FR + NFR + Acceptance + Planning + Architecture
  - Testability (0.25): Measurable + Verifiable + Quantifiable
  - Clarity (0.25): Unambiguous + Defined + Consistent
  - Ambiguity (0.15): Score 0-10, inverted in formula
  - Progressive Disclosure (0.10): Visibility + Structure + Size + Scent + Depth

Grade Scale:
  A: 0.90+  B: 0.80-0.89  C: 0.70-0.79  D: 0.60-0.69  F: <0.60

HOW Detection:
  0 violations = PASS | 1-2 = WARNING | 3+ = CRITICAL

ICE Score:
  Total = Impact × Confidence × Ease (each 1-10, total 1-1000)
  Threshold: <200 = WARN

Vague Terms to Flag:
  improve, enhance, optimize, better, faster, 
  more efficient, user-friendly, seamless, robust, scalable
```

---

## Thinking Frameworks

When facing validation challenges, these frameworks guide systematic assessment.

**Full Catalog**: `.claude/docs/00-core/frameworks/README.md`

**Most Relevant for Specification Validation**:

| Framework | When to Use |
|-----------|-------------|
| [Pre-Mortem](../../docs/00-core/frameworks/strategy.md) | Predicting spec quality issues before review |
| [SCAMPER](../../docs/00-core/frameworks/problem-solving.md) | Improving specification clarity |

> **Selection Tip**: quality prediction→Pre-Mortem, clarity improvement→SCAMPER
