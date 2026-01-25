# Feature Analyzer Domain Expertise

## Thinking Framework Integration

Each phase maps to specific thinking frameworks for structured analysis:

| Phase | Primary Framework | Secondary Framework | Purpose |
|-------|-------------------|---------------------|---------|
| 1. Inventory | ReACT | - | Systematic evidence gathering |
| 2. Overlap | 5 Whys | - | Root cause of overlap |
| 3. Conflicts | Cynefin | 5 Whys | Complexity classification |
| 4. Synergies | SCAMPER | - | Enhancement opportunities |
| 5. Decision | Decision Matrix | Pre-Mortem | Quantified choice + risk |
| 6. Integration | CAGEERF | - | Structured implementation |
| 7. Validation | Pre-Mortem | Cynefin | Failure anticipation |

---

## 7-Phase Methodology

### Phase 1: Inventory (Responsibility Mapping)

- Extract core responsibility (single-sentence purpose) from each feature
- Identify primary entities (classes, modules, data structures)
- Map primary workflows (user journeys, process flows, integration points)
- Document success metrics (quantitative targets, validation approaches)

**Framework: ReACT (Reasoning and Acting)**
- **Reason**: "What information do I need to compare these features?"
- **Act**: Execute Glob to find specs, Read to extract data
- **Observe**: Record core responsibility, entities, workflows, metrics
- **Iterate**: If missing data, reason about where to find it

**Tool Sequence**:
1. `Glob("docs/01-planning/specifications/**/*.md")` - Find specs
2. `Read(spec_path)` - Extract structured data
3. Build inventory object with all extracted fields

### Phase 2: Overlap Detection

- Calculate responsibility overlap % (weighted semantic similarity)
- Identify duplicate requirements (exact or near-exact matches)
- Detect shared infrastructure needs (hooks, schemas, agents, configs)

**Framework: 5 Whys (Root Cause Analysis)**
- WHY do these features share keywords? - Same domain
- WHY same domain? - Solving related problems
- WHY related problems? - Could be merged OR layered
- WHY layered? - One provides foundation for other
- WHY foundation? - REFACTOR recommendation

**Tool Sequence**:
1. Extract keywords from core responsibility
2. Calculate Jaccard similarity
3. IF domain terms unclear - `mcp__perplexity__search("definition [term]")`
4. Apply 5 Whys to understand overlap cause

### Phase 3: Conflicts (Competing Objectives)

- Detect opposing requirements (Feature A requires X, Feature B forbids X)
- Identify circular dependencies (A needs B, B needs A)
- Find resource contention, timeline conflicts
- Document conflict severity (low/medium/high/critical)

**Framework: Cynefin (Complexity Classification)**
- **Simple**: One feature clearly supersedes other - Choose one
- **Complicated**: Expert analysis needed - Detailed comparison
- **Complex**: Emergent behavior - Probe with partial implementation
- **Chaotic**: Immediate action needed - Stabilize first

**Conflict Classification**:
| Type | Cynefin Domain | Resolution |
|------|----------------|------------|
| Resource contention | Complicated | Prioritization matrix |
| Circular dependency | Complex | Break cycle, probe |
| Opposing requirements | Complex | Stakeholder input |
| Timeline conflict | Simple | Sequence features |

### Phase 4: Synergies (Complementarity Assessment)

- Detect sequential dependencies (Feature A - Feature B pipeline)
- Identify amplification effects (Feature A makes B more effective)
- Map foundation layers (one provides infrastructure for other)

**Framework: SCAMPER (Creative Enhancement)**
- **S**ubstitute: Can Feature A replace parts of Feature B?
- **C**ombine: Can A + B create new capability?
- **A**dapt: Can A's approach work for B's problem?
- **M**odify: Can A enhance B's effectiveness?
- **P**ut to other use: Can combined feature serve new use case?
- **E**liminate: What can be removed if merged?
- **R**everse: What if B provided foundation for A instead?

**Tool Sequence**:
1. For each SCAMPER question, evaluate applicability
2. Score synergy potential (0-10)
3. IF unfamiliar enhancement pattern - `mcp__perplexity__search("best practices [enhancement type]")`

### Phase 5: Decision (Integration Strategy)

Apply decision matrix with tie-breakers. See `overlap-calculation.md` for formulas.

**Framework: Decision Matrix + Pre-Mortem**

**Decision Matrix**:
| Factor | Weight | MERGE Score | SEPARATE Score | REFACTOR Score |
|--------|--------|-------------|----------------|----------------|
| Overlap % | 0.40 | >70: 10 | <30: 10 | 30-70: 10 |
| Synergy strength | 0.25 | High: 10 | Low: 10 | Medium: 10 |
| Conflict severity | 0.20 | Low: 10 | High: 10 | Medium: 10 |
| Maintainability | 0.15 | Single team: 10 | Distinct teams: 10 | Shared foundation: 10 |

**Pre-Mortem** (apply to chosen decision):
- "It's 6 months later. The [MERGE/SEPARATE/REFACTOR] failed. Why?"
- Identify top 3 failure modes
- Add mitigations to recommendation

**Tool Sequence**:
1. Calculate weighted scores
2. `mcp__perplexity__reason("risks of [decision] for [feature types]")`
3. Apply Pre-Mortem to validate

### Phase 6: Integration (Architecture Definition)

- **If Merged**: Combined scope, phased implementation, unified success criteria
- **If Separated**: Interface contracts, dependency order, shared infrastructure
- **If Refactored**: Shared foundation extraction, feature separation phases

**Framework: CAGEERF (Structured Output)**
- **C**ontext: What problem does this integration solve?
- **A**nalysis: What did overlap/conflict/synergy analysis reveal?
- **G**oals: What must the integration achieve?
- **E**xecution: Step-by-step implementation plan
- **E**valuation: How will success be measured?
- **R**efinement: What might need adjustment?
- **F**ramework: What patterns/structures to use?

**Output Structure** (per strategy):
- MERGE: Combined spec with unified requirements, single timeline
- SEPARATE: Interface contracts, dependency graph, parallel timelines
- REFACTOR: Foundation layer spec + dependent feature specs

### Phase 7: Validation (Architecture Alignment)

Check against 5 system goals + 4 architecture constraints. See `architecture-constraints.md`.

**Framework: Pre-Mortem + Architecture Constraints**

**Pre-Mortem Validation**:
1. Assume recommendation fails - List 5 ways it could fail
2. For each failure mode, check if current recommendation addresses it
3. Add unaddressed failure modes to risks array

**Cynefin Re-check**:
- Has complexity classification changed during analysis?
- Are we applying appropriate resolution strategy?

**Architecture Alignment**:
- Check 4 constraints from `architecture-constraints.md`
- Validate against 5 system goals from SPEC.md

---

## Feature Relationship Patterns

| Type | Description | Recommendation |
|------|-------------|----------------|
| Type 1: Foundational + Application | One provides infrastructure, other builds on it | REFACTOR (extract foundation) |
| Type 2: Competing Alternatives | Both solve same problem differently | SEPARATE (choose one) |
| Type 3: Complementary Layers | Different abstraction levels | REFACTOR (layered architecture) |
| Type 4: Independent Modules | No shared infrastructure | SEPARATE (parallel development) |


---

## Feature Quality Criteria (Phase 1 Validation)

Features should have:
- Clear problem statement with quantified pain points
- Bounded scope (explicit IN/OUT, <=70 functional requirements)
- Measurable success criteria (baseline + target metrics)
- Integration clarity (dependencies, shared infrastructure, interfaces)

---

## Rate Limits (Finding Prioritization)

Per feature comparison:
- <=3 Critical Conflicts (competing objectives, circular dependencies)
- <=5 Major Overlaps (>70% overlap areas)
- <=5 Minor Synergies (complementary opportunities)
- <=2 Open Questions (missing context, unclear boundaries)

**When exceeded**: Rank by impact, keep top N, summarize remainder in appendix.

---


## External Research Integration

**When to Use Perplexity**:
| Situation | Tool | Query Pattern |
|-----------|------|---------------|
| Unknown domain terms | `mcp__perplexity__search` | "definition of [term] in [context]" |
| Best practice validation | `mcp__perplexity__reason` | "best practices for [decision] in [domain]" |
| Risk identification | `mcp__perplexity__reason` | "common failures when [action] with [features]" |
| Architecture patterns | `mcp__perplexity__search` | "[pattern type] architecture pattern examples" |

**Query Templates**:
- Overlap: "What are common reasons for feature overlap in [domain]?"
- Conflict: "How to resolve [conflict type] between software features?"
- Synergy: "Best practices for combining [feature type A] with [feature type B]"
- Decision: "When should features be merged vs separated in [context]?"
