---
title: "Planning Workflow Patterns"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Planning Workflow Patterns

**Purpose**: Complete planning lifecycle, optimization flows, and coordination protocols

**Auto-loaded**: No (on-demand reference from orchestrator-workflow.md)

---

## 7-Phase Development Lifecycle

**Complete workflow from specification to cleanup**:

### Phase 1: Specification Creation

**Command**: /spec

**Inputs**:
- User requirements (natural language or requirements file)
- Context7 research (automatic)

**Outputs**:
- `docs/01-planning/specifications/NNN-feature/SPEC.md` (complete specification)
- **Embedded Planning Recommendations** (50% planning overhead reduction)

**Fallback Agents**: None (/spec command is primary)

**Performance**: 2-3min with Context7 research

**Key Innovation**: Planning metadata embedded directly in SPEC eliminates separate planning research step

---

### Phase 2: Plan Creation (Business Context)

**Agent**: planning (Alpha, B+)

**Inputs**:
- SPEC.md (from Phase 1)
- Planning Recommendations (embedded in SPEC)

**Outputs**:
- `*-PLAN.md` files (one per component)
- Business context sections populated
- NFR specifications added

**Fallback Agents**: architecture (can add business context if needed)

**Performance**: 1.5-2min per plan

**Optimization**: Parallel enhancement for multi-component features (3-5x faster)

---

### Phase 3: Technical Architecture

**Agent**: architecture (Alpha, B+)

**Inputs**:
- `*-PLAN.md` files (from Phase 2)
- Component Almanac (code reuse analysis)

**Outputs**:
- Technical design sections populated
- Cleanup tasks generated (T9XX series)
- "Existing Code Analysis" section

**Fallback Agents**: architecture (validation only, generates Edit Plans for architecture)

**Performance**: 1.5-2min per plan

**Optimization**: Parallel enhancement for multiple plans

**Code Reuse Integration**: Identifies extension opportunities, generates cleanup tasks for replacements

---

### Phase 4: Implementation

**Agent**: development (MVP, C+)

**Inputs**:
- `*-PLAN.md` files (from Phase 3)
- Component Almanac (existing code)
- Task lists (optional)

**Outputs**:
- Feature code in `packages/**`
- Pre-flight validation complete

**Fallback Agents**:
- debugger (if implementation issues)
- architecture (complex architectural decisions)

**Performance**: Variable (depends on feature complexity)

---

### Phase 5: Testing & Validation

**Agent**: code-quality (Alpha, B+)

**Inputs**:
- Implementation code (from Phase 4)
- Existing test suites

**Outputs**:
- Test execution results
- Failure categorization (APPLICATION_BUG/TEST_BUG/ENVIRONMENT/FLAKY)
- Delegation to debugger/code-quality/code-quality

**Fallback Agents**:
- debugger (application bugs)
- code-quality (test bugs)
- code-quality (code quality issues)

**Performance**: 30s-2min depending on test suite size

---

### Phase 6: Quality Review

**Agent**: code-quality (Alpha, B+)

**Inputs**:
- Implementation code (from Phase 4)
- Test results (from Phase 5)

**Outputs**:
- Security validation
- Standards compliance check
- Code review report

**Fallback Agents**: None (code-quality is primary)

**Performance**: 1-2min

---

### Phase 7: Cleanup & Optimization

**Agent**: development (MVP, C+)

**Inputs**:
- Cleanup tasks (T9XX series from Phase 3)
- Implementation code

**Outputs**:
- Deprecated code removed
- Code structure organized
- Technical debt addressed

**Fallback Agents**: architecture (complex refactoring validation)

**Performance**: Variable (depends on cleanup scope)

---

## Optimized Planning Flow (3-5x Faster)

**Key Optimization**: Parallel enhancement + architecture validation + parallel task creation

### Standard Sequential Flow (Slow)

```
/spec → specification generation (2min)
  → /plan → planning (2min each × 3 = 6min)
  → architecture (2min each × 3 = 6min)
  → architecture (1.5min)
  → /tasks → planning (1min each × 3 = 3min)

Total: 19.5min
```

---

### Optimized Parallel Flow (Fast)

```
/spec → specification generation (SPEC.md + Planning Recommendations) (2min)
  ↓
/plan → [Parallel Enhancement]:
  ├─ planning: core-PLAN.md (2min)
  ├─ planning: analysis-PLAN.md (2min)
  └─ planning: integration-PLAN.md (2min)
  [Total: 2min instead of 6min]
  ↓
[Parallel Enhancement]:
  ├─ architecture: core-PLAN.md (2min)
  ├─ architecture: analysis-PLAN.md (2min)
  └─ architecture: integration-PLAN.md (2min)
  [Total: 2min instead of 6min]
  ↓
architecture: Validate reuse + cleanup (1.5min)
  ↓
/tasks → [Parallel Task Creation]:
  ├─ planning: core-PLAN.md (1min)
  ├─ planning: analysis-PLAN.md (1min)
  └─ planning: integration-PLAN.md (1min)
  [Total: 1min instead of 3min]

Total: 8.5min (2.3x faster)
```

**Performance Gain**: 19.5min → 8.5min (56% time reduction)

---

## Quality-Enhanced Planning Flow (Optional Variant)

**When to Use**: High-stakes features requiring additional validation

### Flow with Pre-Enhancement Review

```
/spec → specification generation (2min)
  → planning: Quality check (30s)
  ↓
/plan → [Parallel Enhancement]:
  ├─ planning: core-PLAN.md (2min)
  ├─ planning: analysis-PLAN.md (2min)
  └─ planning: integration-PLAN.md (2min)
  [Total: 2min]
  ↓
[Parallel Review - Fast agents]:
  ├─ planning: Business review (30s)
  └─ planning: Quality review (30s)
  [Total: 30s]
  ↓
[Parallel Enhancement]:
  ├─ architecture: core-PLAN.md (2min)
  ├─ architecture: analysis-PLAN.md (2min)
  └─ architecture: integration-PLAN.md (2min)
  [Total: 2min]
  ↓
architecture: Technical validation (1.5min)
  ↓
/tasks → [Parallel Task Creation]:
  ├─ planning: core-PLAN.md (1min)
  ├─ planning: analysis-PLAN.md (1min)
  └─ planning: integration-PLAN.md (1min)
  [Total: 1min]

Total: 9min (fast agent reviews add minimal overhead)
```

**Trade-off**: 30s additional time for higher quality assurance

---

## Planning Phase Coordination Protocols

### Protocol 1: Spec-to-Plan Handoff

**Handoff Artifact**: SPEC.md with embedded Planning Recommendations

**planning Receives**:
- Business context guidance
- Component breakdown
- NFR requirements
- Integration points

**planning Populates**:
- Business Context section
- Success Metrics section
- NFR specifications

**Validation**: Check Planning Recommendations section exists in SPEC

---

### Protocol 2: Plan-to-Architecture Handoff

**Handoff Artifact**: *-PLAN.md with business context

**architecture Receives**:
- Business requirements
- Component structure
- NFR specifications

**architecture Populates**:
- Technical Design section
- API specifications
- Integration patterns
- Cleanup tasks (T9XX)

**Validation**: Check Technical Design section populated

---

### Protocol 3: Architecture-to-Implementation Handoff

**Handoff Artifact**: *-PLAN.md (complete)

**development Receives**:
- Technical design
- API specifications
- Integration patterns
- Cleanup tasks

**development Creates**:
- Implementation code
- Pre-flight validation results

**Validation**: Check code follows plan specifications

---

### Protocol 4: Implementation-to-Testing Handoff

**Handoff Artifact**: Implementation code + plan

**code-quality Receives**:
- Implementation code
- Test requirements (from plan)

**code-quality Provides**:
- Test results
- Failure categorization
- Delegation recommendations

**Validation**: Check test coverage meets plan requirements

---

## Workflow Diagrams

### Basic Planning Flow

```
Specification → Plan Enhancement → Architecture → Tasks
(/spec) → (planning) → (architecture) → (planning)
```

### Complete Development Flow

```
Specification → Planning → Architecture → Review → Tasks → Implementation → Testing → Quality → Cleanup
     ↓            ↓            ↓           ↓        ↓           ↓            ↓          ↓         ↓
/spec  plan-enh  arch-enh  arch-review  task-c  python-code-i  test-exec  py-code-r  py-code-i
```

### Parallel Optimization Flow

```
Specification (2min)
     ↓
[Plan Enhancement × 3 parallel] (2min total)
     ↓
[Architecture Enhancement × 3 parallel] (2min total)
     ↓
Architecture Review (1.5min)
     ↓
[Task Creation × 3 parallel] (1min total)

Total: 8.5min (vs 19.5min sequential)
```

---

## Key Performance Insights

**Bottlenecks Eliminated**:
1. **Planning Research**: Embedded in SPEC (50% overhead reduction)
2. **Sequential Enhancement**: Parallel processing (3-5x faster)
3. **Sequential Task Creation**: Parallel generation (3x faster)

**Remaining Bottlenecks**:
1. **architecture**: Cannot parallelize (validates cross-component integration)
2. **/spec command**: Cannot parallelize (single SPEC.md)

**Future Optimization Opportunities**:
- architecture: Incremental validation (per-component instead of full-system)
- /spec command: Component-level specs (parallel creation)

---

**This reference provides complete planning workflow patterns for orchestrator coordination and optimization.**
