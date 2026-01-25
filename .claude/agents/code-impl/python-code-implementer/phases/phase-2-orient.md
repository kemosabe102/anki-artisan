# Phase 2: ORIENT - Context Assessment & Research

**OODA Stage**: ORIENT | **Time Allocation**: 20-25%

**Purpose**: Assess context quality, declare scope boundaries, identify gaps, research library patterns

**Deliverable**: CQ score, declared scope, research results, gap resolution plan

---

## Workflow Steps

### Step 2.1: Scope Boundary Declaration

**Trigger**: Before ANY file modification planning

**Process**:
1. Based on Phase 1 analysis, explicitly declare scope
2. Separate files into modify vs read-only categories
3. Document rationale for scope decisions

**Output**:
```json
{
  "declared_scope": {
    "files_to_modify": ["packages/api/auth.py", "tests/unit/test_auth.py"],
    "files_read_only": ["packages/core/base.py"],
    "rationale": "Auth feature requires auth.py changes and new tests"
  }
}
```

**HALT Condition**: Attempting to modify undeclared file -> FAILURE with `scope_boundary_violation`


---

### Step 2.2: CQ Assessment

**When**: After scope declaration

**Process**:
1. Evaluate context quality across four dimensions
2. Calculate weighted CQ score
3. Determine if research is needed

**CQ Calculation**:
| Dimension | Weight | Check |
|-----------|--------|-------|
| Domain knowledge | 0.40 | Familiar with target module patterns |
| Pattern clarity | 0.30 | Existing code provides clear examples |
| Dependency map | 0.20 | All imports/interfaces understood |
| Risk assessment | 0.10 | Edge cases and failure modes identified |

**CQ Thresholds**:
- CQ >= 0.85: Proceed to Phase 3 (DECIDE)
- CQ 0.70-0.84: Light research (1 Context7 query)
- CQ < 0.70: Deep research required (see Step 2.3)

---

### Step 2.3: Research Tool Selection (Cost-Optimized)

**When**: CQ < 0.85

**Priority Order** (exhaust free options before paid):

| Priority | Tool | Use When | Cost |
|----------|------|----------|------|
| 1st | `mcp__context7__*` | Library/framework docs, API references | Free |
| 2nd | `Read` local docs | Project-specific patterns, existing code | Free |
| 3rd | `mcp__perplexity__search` | Context7 insufficient (trust <7) | Paid |
| 4th | `mcp__perplexity__reason` | Complex trade-off analysis | Paid |

**Rule**: Target ratio 4:1 (Context7:Perplexity)

**Context7 Evaluation Protocol**:
1. Query Context7 for library patterns (max 2 attempts)
2. Assess trust score (1-10)
3. If trust < 7 -> supplement with Perplexity
4. If still < 0.85 after 3 iterations -> HALT with `insufficient_context`

---

### Step 2.4: Gap Detection & Resolution

**Process**:
1. Identify knowledge gaps from Phase 1 analysis
2. Map gaps to research sources
3. Execute targeted research
4. Re-calculate CQ after research

**Gap Categories**:
| Gap Type | Resolution Source |
|----------|-------------------|
| Library API unknown | Context7 |
| Project pattern unclear | Read existing code |
| Best practice needed | Perplexity search |
| Architecture question | Read docs/ or escalate |

---

## Quick Checklist

Before advancing to Phase 3 (DECIDE):

- [ ] Scope boundary explicitly declared
- [ ] CQ calculated and documented
- [ ] Research completed (if CQ < 0.85)
- [ ] All gaps identified with resolution plan
- [ ] CQ >= 0.85 achieved OR research exhausted

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping scope declaration | ALWAYS declare files_to_modify before proceeding |
| Using Perplexity before Context7 | Exhaust free options first (4:1 ratio) |
| Proceeding with CQ < 0.70 | Must research until CQ >= 0.85 or HALT |
| Expanding scope mid-implementation | Return to ORIENT, re-declare scope |

---

## Exit Criteria

**CQ >= 0.85 required to proceed**

| Criterion | Weight | Check |
|-----------|--------|-------|
| Scope declared | 0.25 | `declared_scope` object populated |
| CQ sufficient | 0.30 | CQ >= 0.85 |
| Gaps resolved | 0.25 | All identified gaps have resolution |
| Research complete | 0.20 | Context7/Perplexity queries exhausted or satisfied |

---

## Reference Documentation

- coding-guidelines.md - Prevention patterns
- COMPONENT_ALMANAC.md - Existing components
- research-patterns.md - Context7-first protocol

---

**Previous Phase**: [Phase 1: OBSERVE](phase-1-observe.md)
**Next Phase**: [Phase 3: DECIDE](phase-3-decide.md)
