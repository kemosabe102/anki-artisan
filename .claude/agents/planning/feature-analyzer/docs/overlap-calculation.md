# Overlap Calculation Protocol

## Framework Integration

This protocol integrates with **Phase 2 (ORIENT)** of the agent workflow.

**Primary Framework**: 5 Whys - Understand root cause of overlap
**Tool Sequence**: Read → Calculate → Perplexity (if unclear) → Gate Check

---

## Responsibility Overlap (Weighted Formula)

### Core Purpose Similarity (40% weight)
```
(shared_keywords / total_unique_keywords) × 0.40
```

**Directive Steps**:
1. Extract core purpose from each spec: `Read(spec_path)` → find "## Purpose" or first paragraph
2. Tokenize: Split on whitespace, remove stop words (the, a, an, of, for, with, to, in, and, or, is, are)
3. Calculate: `shared_keywords / total_unique_keywords`
4. Apply weight: `result × 0.40`
5. IF shared_keywords < 2 AND specs are in same domain → `mcp__perplexity__search("relationship between [feature A] and [feature B]")`

**Example Walkthrough**:
```
Feature A purpose: "Manage agent state checkpoints for recovery"
Feature B purpose: "Track agent execution state"

Tokens A: [manage, agent, state, checkpoints, recovery] = 5
Tokens B: [track, agent, execution, state] = 4
Shared: [agent, state] = 2
Total unique: [manage, agent, state, checkpoints, recovery, track, execution] = 7

Score: (2/7) × 0.40 = 0.114 (11.4% responsibility overlap)
```

---

### Entity Overlap (30% weight)
```
(shared_entities / total_unique_entities) × 0.30
```

**Directive Steps**:
1. Extract entities from each spec: `Grep("class |interface |schema:|hook:|type ")` in spec
2. Normalize names: lowercase, remove prefixes/suffixes
3. Calculate: `shared_entities / total_unique_entities`
4. Apply weight: `result × 0.30`

**Entity Categories**:
| Category | Pattern | Example |
|----------|---------|---------|
| Classes | `class [Name]` | `class StateManager` |
| Interfaces | `interface [Name]` | `interface ICheckpoint` |
| Schemas | `schema: [name]` | `schema: checkpoint.schema.json` |
| Hooks | `hook: [name]` | `hook: on_state_change` |
| Agents | `agent: [name]` | `agent: state-tracker` |

---

### Workflow Overlap (30% weight)
```
(shared_workflows / total_unique_workflows) × 0.30
```

**Directive Steps**:
1. Extract workflows from each spec: Look for "## User Journey", "## Process Flow", numbered steps
2. Identify workflow triggers, actions, outcomes
3. Calculate: `shared_workflows / total_unique_workflows`
4. Apply weight: `result × 0.30`

**Workflow Components**:
- **Trigger**: What initiates the workflow (user action, event, schedule)
- **Actions**: What the workflow does (CRUD, transform, notify)
- **Outcome**: What state changes result (created, updated, completed)


---

### Total Responsibility Overlap
```
Total = Purpose_Score + Entity_Score + Workflow_Score
```

---

## 5 Whys Analysis (Root Cause of Overlap)

After calculating raw percentages, apply 5 Whys to understand WHY overlap exists:

**Question Chain**:
1. WHY do these features share keywords? → Same problem domain OR coincidental terminology
2. WHY same problem domain? → Solving related problems OR same problem differently
3. WHY related problems? → Sequential dependency OR parallel alternatives
4. WHY sequential/parallel? → One provides foundation OR both compete
5. WHY foundation/compete? → REFACTOR (extract) OR SEPARATE (choose one)

**Decision Influence**:
| 5 Whys Conclusion | Overlap Adjustment | Decision Bias |
|-------------------|-------------------|---------------|
| Same problem, same solution | +10% to overlap | MERGE |
| Same problem, different solution | -10% to overlap | SEPARATE |
| Related problems, sequential | +5% to overlap | REFACTOR |
| Related problems, parallel | No adjustment | Use raw score |
| Coincidental terminology | -15% to overlap | SEPARATE |

---

## Requirement Overlap (Simple Count)
```
(duplicate_FRs / total_FRs_across_features) × 100%
```
- Count exact duplicates or 80%+ keyword match after normalization


---

## Infrastructure Overlap (Component-Based)
```
(shared_components / total_unique_components) × 100%
```
- List all hooks, schemas, agents, configs, dependencies

---

## Overall Overlap for Decision-Making
```
Overall = (Responsibility × 0.40) + (Requirement × 0.30) + (Infrastructure × 0.30)
```

### Decision Thresholds
| Overall Overlap | Decision |
|-----------------|----------|
| >70% | MERGE |
| <30% | SEPARATE |
| 30-70% | REFACTOR |

### Tie-Breaker Zones
- **28-32%** (separate/refactor boundary)
- **68-72%** (refactor/merge boundary)

### Tie-Breaker Priority
1. **Synergy Strength** (highest): Measurable synergy → bias MERGE/REFACTOR
2. **Implementation Cost**: Shared infrastructure >50% → bias MERGE/REFACTOR
3. **Maintainability** (lowest): Distinct teams → bias SEPARATE

---

## Phase Gate (BLOCKING)

**Before proceeding to Phase 3 (Conflicts)**:

| Check | Threshold | On Fail |
|-------|-----------|---------|
| Responsibility calculated | Score exists | FAILURE: Cannot compare |
| Entity calculated | Score exists OR documented as N/A | WARN: Reduced confidence |
| Workflow calculated | Score exists OR documented as N/A | WARN: Reduced confidence |
| At least 2 dimensions complete | 2/3 scored | FAILURE: Insufficient data |
| 5 Whys applied | Root cause documented | WARN: Proceed with note |


**Confidence Reduction**:
- Missing 1 dimension: confidence -= 0.15
- Missing 2 dimensions: confidence -= 0.30 (minimum 0.50)
- 5 Whys not applied: confidence -= 0.05

---

## External Research (When Needed)

**Trigger Conditions**:
- Unknown domain terms in either spec
- Shared keywords < 2 despite apparent relationship
- Overlap calculation yields unexpected result (e.g., clearly related features show <20%)

**Query Templates**:
- Term clarification: `mcp__perplexity__search("what is [term] in [domain] software")`
- Relationship discovery: `mcp__perplexity__search("relationship between [feature type A] and [feature type B]")`
- Pattern matching: `mcp__perplexity__reason("are [feature A] and [feature B] typically separate or combined in [domain]")`

**Result Integration**:
- IF Perplexity reveals hidden relationship → adjust overlap +10-15%
- IF Perplexity reveals they solve different problems → adjust overlap -10-15%
- Document adjustment in rationale

---

## Confidence Based on Data Quality

| Data Completeness | Confidence Range |
|-------------------|------------------|
| All 3 dimensions calculated | 0.90-1.00 |
| 2 dimensions complete, 1 missing | 0.70-0.89 |
| 1 dimension complete, 2 estimated | <0.70 (flag as Open Question) |


---

## Complete Worked Example

**Input**: Compare `checkpoint-management.md` and `state-persistence.md`

### Step 1: Responsibility Overlap (40% weight)
```
A: "Enable recovery of agent state through checkpoint creation and restoration"
B: "Persist agent state to durable storage for session continuity"

Tokens A: [enable, recovery, agent, state, checkpoint, creation, restoration] = 7
Tokens B: [persist, agent, state, durable, storage, session, continuity] = 7
Shared: [agent, state] = 2
Unique: 12

Score: (2/12) × 0.40 = 0.067 (6.7%)
```

### Step 2: Entity Overlap (30% weight)
```
A entities: StateCheckpoint, CheckpointManager, checkpoint.schema.json, on_checkpoint_created
B entities: StateStore, PersistenceManager, state.schema.json, on_state_saved

Shared: None (different names, but...)
After normalization: StateCheckpoint ≈ StateStore (both manage state)

Score: (1/7) × 0.30 = 0.043 (4.3%)
```

### Step 3: Workflow Overlap (30% weight)
```
A workflows: [user triggers save → create checkpoint → store snapshot → confirm]
B workflows: [state changes → serialize state → write to storage → confirm]

Shared pattern: [trigger → process state → store → confirm]

Score: (3/8) × 0.30 = 0.113 (11.3%)
```

### Step 4: 5 Whys Analysis
```
WHY share "state"? → Both manage agent state
WHY both manage state? → Different aspects: snapshots vs continuous
WHY different aspects? → Checkpoint = discrete, Persistence = continuous
WHY discrete vs continuous? → Different use cases (recovery vs continuity)
WHY different use cases? → REFACTOR: extract shared StateManager, keep separate features
```

### Step 5: Total Calculation
```
Raw: 6.7% + 4.3% + 11.3% = 22.3%
5 Whys adjustment: +5% (related problems, sequential)
Final: 27.3%

Decision: SEPARATE (< 30% threshold, but near boundary)
Tie-breaker check: 27.3% is NOT in 28-32% zone
Confidence: 0.78 (Medium-High) - all 3 dimensions calculated
```
