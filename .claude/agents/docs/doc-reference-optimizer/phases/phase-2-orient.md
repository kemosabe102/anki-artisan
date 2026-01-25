# Phase 2: ORIENT - Documentation Discovery & Analysis

**OODA Stage**: ORIENT | **Time Allocation**: 25-30%

**Purpose**: Discover candidate documentation, calculate content overlap, rank optimization candidates

**Deliverable**: Ranked list of section-to-documentation matches with overlap scores

---

## Workflow Steps

### Step 2.1: Documentation Discovery

**Input**: Section names and keywords from Phase 1

**Process**:
1. Search documentation directory: `Glob(".claude/docs/**/*.md")`
2. Extract keywords from each agent section
3. Search for keyword matches: `Grep(section_keywords, path=".claude/docs/")`
4. Build candidate doc list per section

**Output**: Map of sections to candidate documentation files

### Step 2.2: Overlap Calculation (3-Component Algorithm)

**Input**: Section content + candidate doc content


**Process**:
1. **Jaccard Similarity (40%)**: Word-level overlap between section and doc
   - Tokenize both texts (lowercase, remove punctuation)
   - Calculate: `|intersection| / |union|`
2. **Structural Similarity (30%)**: Header/format pattern matching
   - Compare section headers, bullet structures, table layouts
   - Score based on structural element overlap
3. **Semantic Similarity (30%)**: Concept and intent alignment
   - Identify domain concepts (agent names, tool names, patterns)
   - Compare conceptual coverage

**Formula**: `overlap = (jaccard * 0.4) + (structural * 0.3) + (semantic * 0.3)`

**Output**: Overlap percentage per section-doc pair

### Step 2.3: Candidate Ranking

**Input**: All section-doc overlap scores

**Process**:
1. Filter candidates with overlap >= 0.60 (minimum threshold)
2. Sort by overlap percentage descending
3. Keep top 3 candidates per section
4. Flag high-overlap matches (>= 0.80) for reference strategy

**Output**: Ranked candidate list per section


### Step 2.4: Gap Detection (Optional)

**Input**: Sections with no high-overlap matches

**Process**:
1. Sample 2-3 related agents for pattern detection
2. Identify shared content patterns not in docs
3. Note potential new documentation opportunities

**Output**: Documentation gap candidates (for reporting only)

---

## Overlap Thresholds

| Overlap Range | Classification | Strategy Indication |
|---------------|----------------|---------------------|
| >= 0.80 | High | `reference_existing` candidate |
| 0.60 - 0.79 | Medium | `extend_base` candidate |
| < 0.60 | Low | `keep_inline` or `create_new` |

---

## Quick Checklist

Before advancing to Phase 3 (DECIDE):

- [ ] Documentation directory scanned
- [ ] All sections matched against candidates
- [ ] Overlap calculated using 3-component algorithm
- [ ] Candidates ranked by overlap score
- [ ] Gap detection completed (if applicable)


---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Full ecosystem scan | Limit to `.claude/docs/`, sample only 2-3 agents for gaps |
| Ignoring structural similarity | Format patterns matter for reference suitability |
| Single-candidate selection | Keep top 3 candidates for decision phase |
| Skipping low-overlap sections | Still record them for `keep_inline` justification |

---

## Exit Criteria

**CQ >= 0.85 required to proceed**

| Criterion | Weight | Check |
|-----------|--------|-------|
| Docs discovered | 0.25 | At least 1 doc file found |
| Overlap calculated | 0.30 | All sections have overlap scores |
| Candidates ranked | 0.25 | Top candidates identified per section |
| Thresholds applied | 0.20 | High/Medium/Low classified |

---

**Previous Phase**: [Phase 1: OBSERVE](phase-1-observe.md)
**Next Phase**: [Phase 3: DECIDE](phase-3-decide.md)
