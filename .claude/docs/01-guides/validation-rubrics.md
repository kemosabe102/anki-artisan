---
title: "Validation Rubrics Guide"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Validation Rubrics Guide

## Pain Point Alignment Rubric (0-3 Scale)

### **Score 3: APPROVE** - Direct P1 Impact

- Directly addresses P1 pain point with clear impact measurement
- Customer-facing improvement with quantifiable benefits
- Aligns with top customer complaints and feedback

### **Score 2: APPROVE** - P2/P3 or Secondary P1 Impact

- Addresses P2/P3 pain point directly
- OR provides secondary impact on P1 pain point
- Clear customer value proposition

### **Score 1: NEEDS_REFINEMENT** - Technical Enabler

- Indirect technical enabler that supports pain point resolution
- Infrastructure or foundation work that enables future pain point fixes
- Requires justification of pain point connection

### **Score 0: REJECT** - No Pain Point Connection

- No clear connection to documented customer pain points
- Purely internal or technical work without customer impact justification
- Should be deferred or justified through different criteria

## Decision Framework

- **≥2**: **APPROVE** - Proceed with implementation
- **=1**: **NEEDS_REFINEMENT** - Clarify pain point connection
- **0**: **REJECT** - Defer or provide pain point justification

## Maturity Gate Assessment

### **MVP Stage**

- **Complexity**: Low only (≤3 major components, proven patterns)
- **Unknowns**: Minimal unknowns, well-understood domain
- **Risk**: Prefer safe, tested approaches

### **Alpha Stage**

- **Complexity**: Moderate (some new integration, limited unknowns)
- **Unknowns**: Some research required, manageable scope
- **Risk**: Accept moderate risk for validated benefits

### **Beta/GA Stage**

- **Complexity**: High complexity acceptable (new patterns, multiple unknowns)
- **Unknowns**: Significant research and experimentation allowed
- **Risk**: Higher risk acceptable for strategic initiatives

## Maturity Assessment Actions

- **Appropriate**: Complexity matches current stage, proceed
- **Too Complex**: Recommend deferral to later stage or scope reduction
- **Too Simple**: Consider accelerating or bundling with other work

## Rationale Coverage KPI

### **Formula**

```
rationale_coverage = plan_sections_with_decisions / total_plan_sections
```

### **Qualifying Section**

Plan section (§) must have:

- At least one Decision Snapshot with `id` referencing the section
- At least one `context_used` entry that is pinned (commit hash or research reference)

### **Minimum Threshold**

- **≥0.8** (80% of plan sections must have traceable decisions)
- **Quality Gate**: Block planning if coverage falls below threshold
