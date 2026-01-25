# Phase 2: ORIENT - Research and Context Quality Assessment

**OODA Stage**: ORIENT | **Time Allocation**: 20-25%

**Purpose**: Research patterns via Context7/Perplexity, assess context quality, select thinking framework

**Deliverable**: Research synthesis, CQ score, framework selection, gap identification

---

## Research Strategy

### Step 2.1: Context7 Research (Primary)

**Input**: Operation type and context from Phase 1

**Process**:
1. Resolve library ID for Claude Code documentation
2. Query relevant topics based on operation
3. Extract patterns, best practices, constraints

**Context7 Query Matrix**:

| Operation | Topic Focus |
|-----------|-------------|
| `build_workflow` | Slash commands, hooks, agent patterns |
| `sync_ecosystem` | Document structure, cross-references |
| `create_command` | Command syntax, tool permissions, frontmatter |
| `create_automation` | Hook patterns, event triggers, validation |
| `pre_mortem` | Failure patterns, risk assessment |
| `analyze_failures` | Debugging patterns, root cause analysis |

**Output**: Extracted patterns with source references


### Step 2.2: Perplexity Research (Secondary)

**When**: CQ < 0.85 after Context7, or novel patterns needed

**Process**:
1. Formulate specific query about workflow patterns
2. Search for community best practices
3. Cross-reference with Context7 findings

**Cost Optimization**: Context7 FIRST (free) -> Perplexity SECOND (paid). Target ratio: 4:1.

**Output**: Community patterns with confidence scores

---

## Framework Selection

### Step 2.3: Select Thinking Framework

**Input**: Operation type from Phase 1

**Framework Matrix**:

| Operation | Framework | Application |
|-----------|-----------|-------------|
| `build_workflow` | CAGEERF | Context -> Analysis -> Goals -> Execution -> Evaluation -> Refinement -> Framework |
| `optimize_workflow` | SCAMPER | Substitute/Combine/Adapt/Modify/Put to use/Eliminate/Reverse |
| `analyze_bottlenecks` | 5 Whys + RCA | Symptom -> Why? (x5) -> Root Cause -> Fix |
| `sync_ecosystem` | ReACT | Think -> Act -> Observe -> Refine |
| `pre_mortem` | Pre-Mortem Analysis | Assume failure -> Brainstorm causes -> Prioritize -> Prevent |
| `analyze_failures` | 5 Whys + RCA | Gather evidence -> Why chain -> Root cause -> Recommendations |
| `create_command` | CAGEERF | Structured creation with validation |
| `create_automation` | CAGEERF | Structured hook development |

**Output**: Selected framework with application guidance


---

## Context Quality Assessment

### Step 2.4: Calculate CQ Score

**Formula**: CQ = Domain x 0.4 + Pattern x 0.3 + Dependency x 0.2 + Risk x 0.1

| Factor | Weight | Evaluation |
|--------|--------|------------|
| Domain Knowledge | 0.40 | Operation-specific patterns understood |
| Pattern Clarity | 0.30 | Best practices identified from research |
| Dependency Mapping | 0.20 | Integration points and prerequisites clear |
| Risk Awareness | 0.10 | Potential failure modes identified |

**CQ Gate**:
- CQ >= 0.85: Proceed to DECIDE
- CQ 0.70-0.84: One more research iteration
- CQ < 0.70: Escalate or gather more context

**Iteration Limit**: 3 research cycles before FAILURE

---

## Gap Analysis

### Step 2.5: Identify and Resolve Gaps

**Input**: Research findings and CQ assessment

**Process**:
1. List information gaps affecting CQ
2. Assess impact of each gap on execution
3. Plan resolution (research, clarification, assumption)

**Gap Categories**:
- **Blocking**: Cannot proceed without resolution
- **Degrading**: Can proceed but with reduced confidence
- **Acceptable**: Minor gaps with workarounds

**Output**: Gap register with resolution status


---

## Quick Checklist

Before advancing to Phase 3 (DECIDE):

- [ ] Context7 research completed for operation type
- [ ] Perplexity consulted if CQ < 0.85 after Context7
- [ ] Thinking framework selected
- [ ] CQ score >= 0.85
- [ ] Gaps identified with resolution plan

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping Context7 | Always research before building |
| Over-relying on Perplexity | Use Context7 first (free), Perplexity second (paid) |
| Ignoring CQ gate | Do not proceed below 0.85 without iteration |
| Wrong framework | Match framework to operation type |

---

## Exit Criteria

**CQ (Context Quality) >= 0.85 required to proceed**

| Criterion | Weight | Check |
|-----------|--------|-------|
| Research complete | 0.30 | Context7 + optional Perplexity |
| Framework selected | 0.20 | Matches operation type |
| CQ calculated | 0.25 | Score documented with factors |
| Gaps resolved | 0.15 | No blocking gaps remain |
| Patterns extracted | 0.10 | Best practices documented |

---

## Reference Documentation

- [00-core/frameworks/README.md](../../../../docs/00-core/frameworks/README.md) - Framework details
- [orchestrator-thresholds.md](../../../../docs/00-core/orchestrator-thresholds.md) - CQ thresholds
- [workflow-operations.md](../docs/workflow-operations.md) - Operation-specific research needs

---

**Previous Phase**: [Phase 1: OBSERVE](phase-1-observe.md)
**Next Phase**: [Phase 3: DECIDE](phase-3-decide.md)
