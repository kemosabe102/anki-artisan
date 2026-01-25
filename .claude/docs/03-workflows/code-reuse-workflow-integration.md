---
title: "Code Reuse Workflow Integration"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Code Reuse Workflow Integration

**Purpose**: Complete code reuse strategy, decision matrices, and cleanup protocols

**Auto-loaded**: No (on-demand reference from orchestrator-workflow.md)

---

## Quick Decision Rule

**Always check Component Almanac before creating new components**

**Decision Hierarchy**: Extend > Modify > Replace > Create New

---

## Core Workflow Trigger

### Planning Phase Integration

```
Planning Phase Entry:
  ├─ Check Component Almanac (docs/00-project/COMPONENT_ALMANAC.md)
  ├─ Apply decision matrix: >50% overlap → Extend | No overlap → Create New
  ├─ Generate cleanup tasks (T9XX) for every replacement
  └─ Validate >50% time savings threshold
```

**Key Principle**: Code reuse must save >50% time to justify vs new implementation

---

## Decision Matrix: Extend vs Replace

### When to Extend (Preferred)

**Criteria** (ANY of these triggers extension):
- Existing component covers >50% of requirements
- Core functionality matches, needs additional features
- Architecture aligns with new requirements
- Extension effort < 50% of new implementation

**Time Savings**: 60-80% (good option)

**Example**:
```
Requirement: Enhanced BaseService with caching
Existing: BaseService (covers 70% - lifecycle, logging, error handling)
Decision: EXTEND (add caching mixin)
Savings: 70% (only implement caching, reuse lifecycle/logging/errors)
```

---

### When to Replace (Avoid Unless Necessary)

**Criteria** (ALL must be true to justify):
- Existing component fundamentally incompatible (NOT just missing features)
- Extension would introduce significant complexity or anti-patterns
- Replacement effort < existing component maintenance cost + extension effort
- Replacement includes cleanup tasks (T9XX series)

**Time Savings**: Often negative (requires cleanup, expensive)

**Example**:
```
Requirement: Async BaseService
Existing: Sync BaseService (incompatible with async/await)
Decision: REPLACE (async requires fundamental redesign)
Cleanup: Generate T9XX tasks to migrate all sync services
Savings: Negative initially, positive long-term after migration
```

---

### When to Create New (Last Resort)

**Criteria** (ONLY if):
- No existing component covers >20% of requirements
- Extension/modification would be forced and unnatural
- Component Almanac check shows no related components

**Time Savings**: 0% (baseline)

**Example**:
```
Requirement: WebSocket handler
Existing: HTTP request handlers only (<10% overlap)
Decision: CREATE NEW (fundamentally different protocol)
Savings: 0% (no reuse opportunity)
```

---

## Time Savings Thresholds

**Quantitative Guidelines**:

| Decision | Overlap | Time Savings | When to Use |
|----------|---------|--------------|-------------|
| **Reuse** | 80-100% | 80-95% | Exact match, no changes needed |
| **Extend** | 50-79% | 60-80% | Core matches, add features |
| **Modify** | 30-49% | 40-60% | Partial match, adapt existing |
| **Replace** | N/A | Often negative | Incompatible architecture, includes cleanup |
| **Create New** | 0-29% | 0% | No existing component applies |

**Critical Threshold**: Must save >50% to justify new implementation

**Example Calculation**:
```
New Feature Estimate: 8 hours
Existing Component: 6 hours equivalent functionality
Extension Effort: 2 hours
Time Savings: (6 / 8) × 100% = 75% ✅ (Extend is justified)

Alternative - Create New: 8 hours
Time Savings: 0% ❌ (Would waste existing 6 hours of work)
```

---

## Key Integration Points

### Plan-Enhancer Integration

**Responsibility**: Identify reuse opportunities, flag replacements

**Actions**:
1. Read Component Almanac during plan enhancement
2. Identify existing components with >50% overlap
3. Recommend extension strategy in Business Context section
4. Flag replacement decisions for architecture review

**Output Section**: "Existing Code Analysis" in *-PLAN.md

---

### Architecture-Enhancer Integration

**Responsibility**: Generate cleanup tasks, populate technical reuse strategy

**Actions**:
1. Review Component Almanac analysis from planning
2. Generate cleanup tasks (T9XX series) for replacements
3. Populate "Existing Code Analysis" section with technical details
4. Specify extension points and integration patterns

**Output**: T9XX tasks in *-PLAN.md + technical integration guidance

---

### Architecture-Review Integration

**Responsibility**: Validate code reuse (15% weight) + cleanup completeness (7% weight)

**Scoring Criteria**:

**Code Reuse (15% weight)**:
- 15%: Extension strategy with >50% reuse
- 10%: Modification with 30-50% reuse
- 5%: Create new with <30% reuse but justified
- 0%: Create new without Component Almanac check

**Cleanup Completeness (7% weight)**:
- 7%: All replacements have T9XX cleanup tasks
- 4%: Partial cleanup tasks
- 0%: Replacement without cleanup tasks

**Critical Flag**: "Reinventing the Wheel" if >50% overlap ignored

---

### /tasks Command Integration

**Responsibility**: Generate T9XX (cleanup) and T8XX (tech debt) task series

**Task Series**:

**T9XX - Cleanup Tasks** (for replacements):
```
T900: Remove deprecated ComponentA
T901: Migrate consumers to ComponentB
T902: Update documentation
T903: Update tests
```

**T8XX - Tech Debt Investigation** (for modifications):
```
T800: Investigate coupling in ModuleX
T801: Analyze extension impact
T802: Document technical debt
```

**Integration**: Automatically generated when architecture identifies replacements

---

## Cost-Benefit Calculation Formulas

### Formula 1: Extension ROI

```
Extension ROI = (Reuse_Hours / New_Implementation_Hours) × 100%

Example:
New Feature: 8 hours
Existing Reuse: 6 hours
Extension: 2 hours
ROI = (6 / 8) × 100% = 75% savings ✅
```

---

### Formula 2: Replacement Cost

```
Replacement Cost = New_Implementation + Cleanup + Migration

Example:
New Implementation: 10 hours
Cleanup Tasks (T9XX): 5 hours
Migration Effort: 15 hours
Total Cost: 30 hours

Existing Modification Cost: 12 hours
Decision: MODIFY (30h replacement >> 12h modification) ❌
```

---

### Formula 3: Technical Debt Burden

```
Tech Debt Burden = Maintenance_Cost_Per_Year × Expected_Lifetime

Example:
Maintenance: 2 hours/year
Lifetime: 5 years
Burden: 10 hours

If Replacement Saves: 5 hours/year maintenance
ROI: (5 × 5) - 30 = -5 hours (still negative, but improving)
Year 6+: Positive ROI
```

---

## Phase-by-Phase Integration Steps

### Phase 1: Specification (/spec command)

**Actions**:
- Review Component Almanac for related components
- Include reuse opportunities in Planning Recommendations
- Flag potential replacements for planning investigation

**Output**: Planning Recommendations with reuse guidance

---

### Phase 2: Plan Enhancement (planning)

**Actions**:
- Deep-dive Component Almanac analysis
- Identify >50% overlap components
- Recommend extension/modification strategy
- Document in "Existing Code Analysis" section

**Output**: "Existing Code Analysis" in *-PLAN.md

---

### Phase 3: Architecture Design (architecture)

**Actions**:
- Review planning's reuse recommendations
- Generate T9XX cleanup tasks for replacements
- Populate technical integration patterns
- Specify extension points

**Output**: Technical Design + T9XX tasks in *-PLAN.md

---

### Phase 4: Architecture Validation (architecture)

**Actions**:
- Validate code reuse strategy (15% weight)
- Validate cleanup completeness (7% weight)
- Flag "Reinventing the Wheel" anti-pattern if >50% overlap ignored
- Generate Technical Review Report with reuse assessment

**Output**: Technical Review Report with reuse validation

---

### Phase 5: Task Generation (/tasks command)

**Actions**:
- Extract T9XX cleanup tasks from architecture output
- Generate T8XX tech debt investigation tasks for modifications
- Create implementation task breakdown

**Output**: Complete task list with cleanup integration

---

### Phase 6: Implementation (development)

**Actions**:
- Follow extension strategy from architecture
- Execute T9XX cleanup tasks in order
- Integrate with existing components per Technical Design

**Output**: Implementation code + completed cleanup

---

### Phase 7: Cleanup Validation (architecture)

**Actions**:
- Verify all T9XX cleanup tasks completed
- Validate deprecated code removed
- Check migration completeness

**Output**: Cleanup validation report

---

## Critical Anti-Pattern: Reinventing the Wheel

**Definition**: Creating new components when existing components cover >50% functionality

**Detection** (architecture):
```
Check Component Almanac:
  ├─ Existing component overlap >50%?
  │   ├─ YES → Check if extension/modification considered
  │   │   ├─ NO → FLAG: "Reinventing the Wheel" (CRITICAL)
  │   │   └─ YES → Validate justification for replacement
  │   └─ NO → Approve new component
```

**Impact**: Wasted implementation time, duplicated maintenance, technical debt accumulation

**Resolution**:
1. Identify overlap percentage (Component Almanac)
2. Calculate extension effort vs new implementation
3. If extension saves >50%, recommend extension strategy
4. If replacement justified, generate T9XX cleanup tasks

---

## Agent Responsibilities by Phase

| Phase | Agent | Reuse Responsibility |
|-------|-------|---------------------|
| **Specification** | /spec command | Initial Component Almanac review, flag reuse opportunities |
| **Plan Enhancement** | planning | Deep reuse analysis, recommend extension/modification, document in "Existing Code Analysis" |
| **Architecture Design** | architecture | Generate T9XX cleanup tasks, technical integration patterns |
| **Architecture Validation** | architecture | Validate reuse (15%) + cleanup (7%), flag "Reinventing the Wheel" |
| **Task Generation** | /tasks command | Extract T9XX/T8XX tasks, generate task breakdown |
| **Implementation** | development | Execute extension strategy, complete T9XX cleanup |
| **Cleanup Validation** | architecture | Verify T9XX completion, deprecated code removal |

---

## Complete Workflow Example

**Scenario**: Implement caching for API service

### Step 1: Component Almanac Check
```
Existing: BaseService (covers lifecycle, logging, errors = 70%)
Requirement: CachedAPIService (BaseService + caching + API client)
Overlap: 70% (BaseService functionality)
Decision: EXTEND (add caching + API client to BaseService)
```

---

### Step 2: planning Analysis
```
"Existing Code Analysis":
- BaseService covers lifecycle, logging, error handling (70%)
- Extension required: Caching mixin (20%), API client mixin (10%)
- Recommendation: Extend BaseService with mixin architecture
- Time Savings: 70% vs new implementation
```

---

### Step 3: architecture Design
```
Technical Design:
- CachingMixin: Redis-backed cache with TTL
- APIClientMixin: httpx async client with retry logic
- Integration: Multiple inheritance pattern
- Extension Points: cache_key(), cache_ttl() overrides

No T9XX tasks (extension, not replacement)
```

---

### Step 4: architecture Validation
```
Code Reuse Score: 15/15 (extension with 70% reuse)
Cleanup Score: N/A (no replacement)
Overall: APPROVED
```

---

### Step 5: Implementation
```python
# Extend BaseService
class CachedAPIService(CachingMixin, APIClientMixin, BaseService):
    cache_ttl = 300  # Override cache TTL
    # Only implement API-specific logic (30%)
    # Reuse BaseService lifecycle, logging, errors (70%)
```

---

## Summary: Decision Quick Reference

**Check Component Almanac** → **Calculate Overlap** → **Apply Decision Matrix**:

- **>80% overlap** → REUSE (80-95% savings)
- **50-79% overlap** → EXTEND (60-80% savings)
- **30-49% overlap** → MODIFY (40-60% savings)
- **<30% overlap** → CREATE NEW (0% savings, justified)
- **Replacement** → Generate T9XX cleanup tasks (often negative savings)

**Critical Rule**: Must save >50% to justify new implementation over extension

---

**This reference provides complete code reuse workflow integration for orchestrator coordination and architecture validation.**
