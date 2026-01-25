# Phase 2: ORIENT - Framework Application & Evidence Collection

**OODA Stage**: ORIENT | **Time Allocation**: 50-55%

**Purpose**: Apply 7 evaluation frameworks, collect file:line evidence, detect anti-patterns

**Deliverable**: Framework scores (7), evidence citations, anti-pattern findings

---

## Workflow Steps

### Step 2.1: Structural Quality (Framework 1)

**Input**: Agent file path, loaded criteria (16 items)

**Process**:
1. `Read(agent_path, limit=20)` - Extract frontmatter
2. `Grep("^tools:", agent_path)` - Verify tools field exists
3. `Grep("schema:", agent_path)` - Check schema reference
4. `Grep("base-agent-pattern", agent_path)` - Verify base pattern extension
5. For each of 16 criteria: cite evidence as `file:line` or mark FAIL

**Output**: `{pass_count}/16` with evidence citations

### Step 2.2: Prompt Engineering Principles (Framework 2)

**Input**: Full agent file content


**Process**:
1. `Read(agent_path)` - Full file for analysis
2. Score each of 9 principles (0-5) using rubric in `docs/evaluation-frameworks.md`
3. Apply weights per principle
4. Calculate: `Weighted_Average = (Sum(Score x Weight)) / Sum(Weights)`

**Output**: Grade A-F with weighted_score

### Step 2.3: Token Optimization (Framework 3)

**Input**: Baseline token count from Phase 1

**Process**:
1. Scan agent content for each of 15+ optimization techniques
2. For each technique found: calculate potential token savings
3. Aggregate: `potential_savings = sum(technique_savings)`

**Output**: `{current_tokens}` vs `{potential_tokens}` with technique breakdown

### Step 2.4: Testing & Validation Strategy (Framework 4)

**Input**: Agent tools field, description

**Process**:
1. Classify risk level: CRITICAL (file writes) / HIGH (external APIs) / MEDIUM (analysis) / LOW (read-only)
2. `Grep("test|validation|schema", agent_path)` - Find testing references
3. Compare current approach against required strategy for risk level

**Output**: `{current_approach}` vs `{required_approach}` with gaps


### Step 2.5: Progressive Disclosure (Framework 5)

**Input**: Full agent file content

**Process**:
1. Check description length from frontmatter: target `<200 chars`
2. Verify hierarchical structure: 5 sections in expected order
3. Count total lines
4. Calculate: `PD_Score = (Semantic x 0.25) + (Hierarchical x 0.30) + (Size x 0.25) + (Efficiency x 0.20)`

**Output**: Grade A-F with component scores

### Step 2.6: Token Density (Framework 6)

**Input**: Full agent file content

**Process**:
1. `Grep("just|very|really|quite|simply", agent_path)` - Count filler words
2. Compare active voice ratio: `"do|make|create|run"` vs `"is|are|was|were"`
3. Check XML tag usage, example count, reference inheritance
4. Calculate: `TD_Score = Sum(dimension x weight)`

**Output**: Grade A-F with dimension breakdown

### Step 2.7: Framework Alignment (Framework 7)

**Input**: Agent description, 00-core/frameworks/README.md

**Process**:
1. Identify agent domain: research/implementation/analysis/planning/debugging/optimization
2. `Grep("OODA|ReACT|5 Whys|CAGEERF|SCAMPER|DMAIC", agent_path)` - Find framework references
3. Count workflow phases, check framework terminology application (not just mention)
4. Calculate: `integration_depth = phases_with_framework_applied / total_phases`

**Output**: Grade A-F with integration_depth score


### Step 2.8: Anti-Pattern Detection

**Input**: Full agent file content, anti-patterns.md catalog

**Process**:
1. For each category (Performance, Schema/Compliance, Operational, Security):
   - Run Grep patterns from catalog
   - Classify severity: CRITICAL / HIGH / MEDIUM / LOW
   - Cite locations: `file:line`
2. Aggregate findings with fix guidance

**Output**: Anti-pattern report with severity and locations

---

## Quick Checklist

Before advancing to Phase 3 (DECIDE):

- [ ] All 7 frameworks applied (or noted in incomplete_dimensions)
- [ ] Every finding has file:line citation
- [ ] Anti-patterns detected with severity classification
- [ ] Confidence score assigned per framework
- [ ] Evidence documented for each score

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Generic findings | Always cite specific file:line evidence |
| Missing frameworks | Apply all 7 sequentially, note gaps |
| Subjective scoring | Use rubric from evaluation-frameworks.md |
| Ignoring anti-patterns | Run full catalog scan regardless of framework scores |

---

**Previous Phase**: [Phase 1: OBSERVE](phase-1-observe.md)
**Next Phase**: [Phase 3: DECIDE](phase-3-decide.md)
