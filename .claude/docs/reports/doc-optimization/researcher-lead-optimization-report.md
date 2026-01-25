# Researcher-Lead Agent Optimization Report

**Date**: 2025-11-18
**Agent**: researcher-lead
**Analysis Type**: Token efficiency and documentation access audit
**Focus**: Planning vs execution role separation

---

## Executive Summary

**Current State**: 28,055 characters (~7,014 tokens)
**Optimized State**: ~18,500 characters (~4,625 tokens)
**Token Savings**: ~2,389 tokens (34% reduction)

**Key Finding**: Agent is well-designed for planning focus, but contains significant duplication with base-agent-pattern.md and excessive inline workflow details that belong in external guides.

---

## Token Analysis

### Current Token Distribution

| Section | Characters | Est. Tokens | Percentage |
|---------|-----------|-------------|------------|
| Frontmatter + Role & Boundaries | 2,500 | 625 | 9% |
| Schema Reference | 2,200 | 550 | 8% |
| Permissions & Protocols | 800 | 200 | 3% |
| Base Pattern Extension | 750 | 188 | 3% |
| Navigation Rules | 2,800 | 700 | 10% |
| Reasoning Approach | 600 | 150 | 2% |
| Core Workflow (Phases 1-6) | 9,200 | 2,300 | 33% |
| Delegation Patterns | 1,200 | 300 | 4% |
| Memory Management | 400 | 100 | 1% |
| Tool Usage | 500 | 125 | 2% |
| Compression & Output | 200 | 50 | 1% |
| Agent-Specific Knowledge | 6,905 | 1,726 | 25% |
| **TOTAL** | **28,055** | **7,014** | **100%** |

### Optimization Opportunities by Category

#### 1. Base Pattern Duplication (~900 tokens)
**Current**: Agent includes full navigation rules, decision protocol, limitations protocol, escalation path
**Issue**: These are generic patterns that belong in base-agent-pattern.md
**Solution**: Replace with "Extends base-agent-pattern.md (Navigation Rules)" + planning-specific overrides

**Sections to Remove**:
- Information Hierarchy (lines 220-247) - Generic pattern → 350 tokens
- Checkpoint Validation (lines 267-272) - Generic pattern → 100 tokens
- Limitations Protocol (lines 274-290) - Generic pattern → 250 tokens
- Escalation Path (lines 292-313) - Generic pattern → 200 tokens

**Savings**: ~900 tokens

#### 2. Workflow Duplication with External Guides (~800 tokens)
**Current**: Phases 1-6 contain extensive inline workflow details
**Issue**: Phase details duplicate content in planning-methodology.md, coordination-patterns.md, worker-allocation.md
**Solution**: Replace with concise phase summaries + references to external guides

**Sections to Compress**:
- Phase 1: Initial Planning (lines 367-382) - Duplicates planning-methodology.md → Reference only
- Phase 2: Task Decomposition (lines 416-426) - Duplicates coordination-patterns.md → Reference only
- Phase 3: Delegation Plan Creation (lines 428-481) - Duplicates coordination-patterns.md + worker-allocation.md → Reference only
- Phase 4: Plan Refinement (lines 504-525) - Generic validation → Compress to checklist
- Phase 6: Follow-Up Planning (lines 555-585) - Duplicates planning-methodology.md lines 386-468 → Reference only

**Savings**: ~800 tokens

#### 3. Pre-Flight Self-Check Redundancy (~300 tokens)
**Current**: Pre-Flight Self-Check appears TWICE (lines 384-414 and embedded in Phase workflow)
**Issue**: Exact duplication of 5-question checklist
**Solution**: Single reference in Core Workflow, remove duplicate

**Savings**: ~300 tokens

#### 4. Agent-Specific Knowledge Redundancy (~200 tokens)
**Current**: Lists 7 guides with full "when to consult" details
**Issue**: Some guidance is obvious (planning-methodology.md for planning tasks)
**Solution**: Compress to essential guides only, move details to guide frontmatter

**Sections to Compress**:
- Lines 186-217: 7 guides with full consultation details
- Compress to 3 essential guides (planning-methodology.md, coordination-patterns.md, worker-allocation.md)
- Remove obvious timing ("every planning task") and extract details ("what to extract")

**Savings**: ~200 tokens

#### 5. Schema Embedding (~190 tokens)
**Current**: Full JSON schema examples embedded in agent (lines 80-136)
**Issue**: Schema already exists in researcher-lead.schema.json
**Solution**: Reference schema file, show only critical fields for quick reference

**Savings**: ~190 tokens

---

## Documentation Access Audit

### ✅ Appropriate Planning Documentation

| Guide | Purpose | Access Level | Planning-Relevant |
|-------|---------|--------------|-------------------|
| research-patterns.md | Delegation methodology, scaling rules | Loaded at startup | ✅ YES - Core framework |
| planning-methodology.md | Minimal scoping, 5-10 min workflow | On-demand | ✅ YES - Primary workflow |
| coordination-patterns.md | 4-component delegation structure | On-demand | ✅ YES - Delegation design |
| worker-allocation.md | Scaling formulas, worker count | On-demand | ✅ YES - Worker planning |
| delegation-examples.md | Complete delegation examples | On-demand | ✅ YES - Pattern reference |

### ⚠️ Potentially Execution-Oriented Documentation

| Guide | Current Access | Issue | Recommendation |
|-------|---------------|-------|----------------|
| tool-parallelization-patterns.md | Referenced (line 209) | Execution optimization, not planning | ✅ KEEP - Helps estimate worker parallelization |
| agent-parallelization-strategy.md | Referenced (line 213) | Execution coordination | ✅ KEEP - Informs delegation planning |

### ❌ Documentation Gaps (Not Found)

| Missing Guide | Purpose | Impact |
|---------------|---------|--------|
| None identified | - | No critical gaps |

**Assessment**: Documentation access is well-aligned with planning role. No execution-oriented documentation inappropriately loaded.

---

## Optimization Recommendations

### Priority 1: Remove Base Pattern Duplication (900 tokens)

**Action**: Replace lines 220-313 (Information Hierarchy, Decision Protocol, Checkpoint Validation, Limitations, Escalation) with:

```markdown
## Navigation Rules

**Extends**: `.claude/docs/01-guides/agents/base-agent-pattern.md` (Navigation Rules)

**Planning-Specific Navigation**:

1. **Primary Source**: Research query from orchestrator with Context_Quality metadata
2. **Secondary Source**: Research planning frameworks (coordination-patterns.md, worker-allocation.md, planning-methodology.md)
3. **Tertiary Source**: Quick reconnaissance (≤10 tool calls) for complexity assessment

**Planning-Specific Decision Path**:
1. Parse research query → Classify (breadth/depth/straightforward)
2. Apply Context_Quality → Determine worker allocation
3. Design 4-component delegations → Return plan to orchestrator

**Checkpoint Validation** (before outputting plan):
- All workers have 4 components? (YES → proceed | NO → complete delegations)
- Worker count ≤5? (YES → proceed | NO → prioritize and cap)
- Boundaries prevent scope creep? (YES → proceed | NO → add exclusions)
- Tool usage ≤10 calls? (YES → proceed | NO → STOP, you're researching not planning)
```

**Savings**: ~900 tokens

### Priority 2: Compress Workflow to References (800 tokens)

**Action**: Replace lines 367-585 (Phases 1-6) with:

```markdown
# Core Workflow: Research Planning

## Workflow Overview

**6-Phase Lifecycle** (PLANNING ONLY - NO EXECUTION):

1. **Analysis**: Parse query, classify type (breadth/depth/straightforward), assess complexity
   - **See**: `planning-methodology.md` (Phase 1: Minimal Scoping)

2. **Research**: Minimal reconnaissance (≤10 tool calls, 5-10 min max)
   - **See**: `planning-methodology.md` (Reconnaissance Patterns)

3. **Todo Creation**: Generate plan structure for complex multi-phase research
   - **See**: Todo Management Protocol (lines 338-365)

4. **Implementation**: Design 4-component delegations for each worker
   - **See**: `coordination-patterns.md` (4-Component Delegation Structure)
   - **See**: `worker-allocation.md` (Scaling Rules)

5. **Validation**: Verify delegation completeness, worker allocation, boundaries
   - **See**: `planning-methodology.md` (Minimal Scoping Checklist)

6. **Reflection**: Return plan to orchestrator (STOP - DO NOT EXECUTE)

## Pre-Flight Self-Check (MANDATORY before Phase 4)

**Before designing delegations, verify**:
1. Am I planning or executing? (✅ Planning = designing delegation plans)
2. How many tool calls? (✅ <10 calls = reconnaissance | ❌ >10 = research)
3. What am I creating? (✅ Delegation plans | ❌ Research findings)
4. Who executes? (✅ Workers via orchestrator | ❌ I execute)
5. Time spent? (✅ <10 min = scoping | ❌ >10 min = exceeded scope)

**Decision**: If ❌ to ANY question → STOP, return plan immediately

## Follow-Up Planning (Iteration Support)

**When Called**: Orchestrator detects gaps, provides `iteration_context`
**Process**: Analyze gap patterns → Design 1-3 targeted delegations → Return follow-up plan
**See**: `planning-methodology.md` (Follow-Up Planning section)
```

**Savings**: ~800 tokens

### Priority 3: Remove Pre-Flight Duplication (300 tokens)

**Action**: Remove duplicate Pre-Flight Self-Check (lines 384-414), keep single reference in Core Workflow

**Savings**: ~300 tokens

### Priority 4: Compress Agent-Specific Knowledge (200 tokens)

**Action**: Replace lines 186-217 with:

```markdown
### Agent-Specific Knowledge Requirements

**Beyond Base Pattern**:

1. `.claude/docs/00-core/research-patterns.md` (Loaded at startup)
   - Delegation methodology, scaling rules, 4-component structure, search strategies

2. `docs/04-guides/researcher-lead/planning-methodology.md`
   - Minimal scoping workflow (5-10 min max), reconnaissance patterns, pre-flight self-check

3. `docs/04-guides/researcher-lead/coordination-patterns.md`
   - 4-component delegation framework (objective/format/guidance/boundaries)

4. `docs/04-guides/researcher-lead/worker-allocation.md`
   - Context_Quality-based allocation formulas, complexity scaling, MAX_WORKERS limits

**Consult on-demand**: delegation-examples.md (pattern reference), tool-parallelization-patterns.md (efficiency), agent-parallelization-strategy.md (delegation planning)
```

**Savings**: ~200 tokens

### Priority 5: Compress Schema Embedding (190 tokens)

**Action**: Replace lines 80-136 with:

```markdown
### agent_specific_output (SUCCESS)

**Complete Structure**: See `.claude/docs/schemas/researcher-lead.schema.json`

**Key Fields**:
- `research_plan`: strategy, complexity, worker_allocation, delegation_plans[], execution_guidance
- `research_rationale`: Why this strategy was chosen
- `recommendations[]`: Execution suggestions for orchestrator

**Each delegation_plan contains**:
- worker_type, worker_id, specific_objective, output_format, tool_guidance, task_boundaries

**See schema file for**: Complete field definitions, validation rules, example payloads
```

**Savings**: ~190 tokens

---

## Optimized Token Breakdown

| Section | Current Tokens | Optimized Tokens | Savings |
|---------|---------------|------------------|---------|
| Navigation Rules | 700 | 150 | 550 |
| Core Workflow | 2,300 | 400 | 1,900 |
| Pre-Flight Check | 300 (duplicate) | 0 | 300 |
| Agent Knowledge | 1,726 | 500 | 1,226 |
| Schema Embedding | 550 | 150 | 400 |
| **Subtotal (Optimizations)** | **5,576** | **1,200** | **4,376** |
| **Other Sections (Unchanged)** | **1,438** | **1,438** | **0** |
| **TOTAL** | **7,014** | **2,638** | **4,376** |

**Note**: Actual savings ~2,389 tokens due to overhead from reference text and section headers.

---

## Documentation Relevance Assessment

### Planning vs Execution Separation

**✅ STRENGTHS**:
1. Agent clearly defines "PLANNER, not RESEARCHER" role (line 13)
2. Critical boundaries prevent execution (lines 37-65)
3. Pre-flight self-check enforces planning focus (5 questions)
4. Documentation focuses on delegation design, not research execution

**⚠️ IMPROVEMENT AREAS**:
1. Workflow phases could be more concise (currently 2,300 tokens, mostly duplication)
2. Navigation Rules are generic (not planning-specific) - should inherit from base pattern
3. Some guide references have obvious timing ("every planning task") - compress

**❌ NO EXECUTION-ORIENTED CONTENT FOUND**:
- No implementation details for research execution
- No synthesis methodologies (orchestrator responsibility)
- No worker result processing (orchestrator handles)

---

## Implementation Strategy

### Phase 1: Base Pattern Migration (900 tokens)
1. Review base-agent-pattern.md for navigation/decision/escalation patterns
2. Replace generic content with "Extends base-agent-pattern.md" references
3. Add only planning-specific decision paths and checkpoints

### Phase 2: Workflow Compression (800 tokens)
1. Create concise workflow overview with external guide references
2. Preserve Pre-Flight Self-Check (critical boundary enforcement)
3. Remove duplicated phase details (already in planning-methodology.md)

### Phase 3: Knowledge & Schema Cleanup (390 tokens)
1. Compress agent-specific knowledge to essential guides only
2. Replace embedded schema with reference + key fields summary
3. Move detailed consultation guidance to guide frontmatter

### Phase 4: Validation
1. Verify agent still loads correctly (session restart required)
2. Test delegation planning workflow (create research plan)
3. Confirm external guides accessible and complete

---

## Risk Assessment

**Low Risk Optimizations** (2,189 tokens):
- Remove base pattern duplication (generic content)
- Remove pre-flight check duplication (exact copy)
- Compress schema embedding (reference existing file)

**Medium Risk Optimizations** (200 tokens):
- Compress agent-specific knowledge (ensure critical guides retained)

**High Risk Optimizations** (800 tokens):
- Compress workflow phases (verify external guides have complete details)
- **Mitigation**: Validate delegation-examples.md, planning-methodology.md, coordination-patterns.md contain all workflow details before compressing

**Overall Risk**: MEDIUM
- **Concern**: Workflow compression assumes external guides are complete and accessible
- **Mitigation**: Read all 4 external guides to verify completeness before optimization
- **Rollback**: Keep current version as researcher-lead.md.backup

---

## Related Optimizations

**Ecosystem Impact**:
1. **researcher-codebase**: Likely similar base pattern duplication (~700 tokens)
2. **researcher-web**: Likely similar base pattern duplication (~700 tokens)
3. **researcher-library**: Likely similar base pattern duplication (~700 tokens)

**Recommendation**: Apply similar optimization pattern to all researcher-* agents after validating researcher-lead optimization.

---

## Conclusion

**Optimization Potential**: 34% size reduction (7,014 → 4,625 tokens)
**Primary Gains**: Base pattern migration (900 tokens) + workflow compression (800 tokens)
**Role Clarity**: Agent is appropriately focused on planning, but contains excessive duplication
**Documentation Access**: Well-aligned with planning role, no execution-oriented guides

**Recommendation**: PROCEED with optimization in 4 phases, validating external guide completeness before workflow compression.

---

**Generated**: 2025-11-18
**Agent**: documentation
**Confidence**: 0.88 (High confidence in base pattern duplication, medium confidence in workflow compression safety)
