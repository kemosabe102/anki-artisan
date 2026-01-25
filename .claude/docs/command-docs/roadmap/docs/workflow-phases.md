# Workflow Phases

Detailed documentation for each phase of the `/roadmap` command workflow.

---

## Phase 1: Discovery (Automated)

**Tools Used**: Glob, Read

**Duration**: <5 seconds

**Actions**:
1. Use Glob to find all roadmap files:
   - `docs/00-project/roadmaps/active/*.md`
   - `docs/00-project/roadmaps/archive/*.md`
   - `docs/00-project/operations/LIVING_SPRINT.md`
   - `docs/00-project/SPRINT-ROADMAP.md`
2. Count discovered files
3. Verify at least one roadmap exists

**Output**: List of roadmap file paths

**Human Involvement**: NONE

**Success Criteria**:
- At least 1 roadmap file discovered
- All files readable (no permission errors)

**Failure Criteria**:
- No roadmap files found (empty directory)
- Permission issues (cannot read files)
- Invalid paths


---

## Phase 2: Multi-Agent Health Analysis (Parallel)

**Delegation Strategy**: Launch 3 specialized agents in parallel (single message, 3 Task tool calls)

**Duration**: ~30-40 seconds (parallel execution)

**Human Involvement**: NONE

### Agent 1: planning
- **Analyzes**: Sprint compliance, Freshness, Completeness
- **Input**: Roadmap files list + dimension requirements
- **Output**: Health scores (0.0-1.0) + specific issues found
- **Schema**: See `.claude/agents/dev-tools/planning/planning.md`

### Agent 2: documentation
- **Analyzes**: Cross-reference integrity, Progressive disclosure
- **Input**: Roadmap files list + validation requirements
- **Output**: Link validation report + files exceeding 500 lines
- **Schema**: See `.claude/agents/dev-tools/documentation/documentation.md`

### Agent 3: context-optimizer
- **Analyzes**: Token density, AI-readability
- **Input**: Roadmap files list + token analysis request
- **Output**: Filler ratio, passive voice %, optimization opportunities
- **Schema**: See `.claude/agents/dev-tools/context-optimizer/context-optimizer.md`

### Success/Failure Criteria

| Scenario | Status | Action |
|----------|--------|--------|
| All 3 agents succeed | SUCCESS | Continue to Phase 3 |
| 1-2 agents succeed | PARTIAL | Report partial results, continue |
| All 3 agents fail | FAILURE | Escalate to human |
| Agent timeout (>2min) | TIMEOUT | Treat as failure, continue with others |


---

## Phase 3: Synthesis & Aggregation (Automated)

**Duration**: ~10 seconds

**Human Involvement**: NONE

### Orchestrator Actions

1. **Aggregate Results**: Collect outputs from 3 agents

2. **Calculate Weighted Health Score**:
   ```
   Overall = (CrossRefIntegrity x 0.20) + (ProgDisclosure x 0.25) +
             (SprintCompliance x 0.15) + (Completeness x 0.10) +
             (Freshness x 0.10) + (TokenDensity x 0.20)
   ```

3. **Apply Synthesis** (if >0.7 similarity overlap):
   - Consolidate duplicate recommendations
   - Score by `(impact x confidence) / effort`
   - Present unified recommendation with agent attribution

4. **Rank Top 5**: Sort by ROI (score improvement per hour)

### Synthesis Rules

- **Overlap Detection**: Similarity >0.7 triggers synthesis
  - Example: documentation "Fix 41 broken links" + planning "Update cross-references" -> consolidated
- **Weighted Formula**: `ROI = (Score Improvement / Effort Hours) x Confidence`
- **Attribution**: Always cite contributing agents

**Reference**: `.claude/docs/01-guides/synthesis-and-recommendation-framework.md`


---

## Phase 4: Present Results (Report)

**Duration**: <5 seconds

**Human Involvement**: REVIEW

### Dashboard Components

1. **Overall Score**: Letter grade (A-F) with numeric value
2. **6 Dimension Scores**: Each with status indicator
3. **Cross-Reference Summary**: Total, valid %, broken links with line numbers
4. **Top 5 Actions**: Ranked by ROI with impact/effort/confidence
5. **Next Steps**: Recommended follow-up commands

### Letter Grade Scale

| Score Range | Grade |
|-------------|-------|
| 0.90-1.00 | A |
| 0.80-0.89 | B |
| 0.70-0.79 | C |
| 0.60-0.69 | D |
| 0.00-0.59 | F |

---

## Performance Targets

| Phase | Target Duration | Notes |
|-------|-----------------|-------|
| Phase 1 (Discovery) | <5 seconds | Glob + Read |
| Phase 2 (Analysis) | ~30-40 seconds | 3 agents in parallel |
| Phase 3 (Synthesis) | ~10 seconds | Aggregation + ranking |
| Phase 4 (Present) | <5 seconds | Dashboard generation |
| **Total Check Mode** | ~1 minute | vs ~1.5 minutes sequential |

### Mode-Specific Timing

| Mode | Duration | Agent Count |
|------|----------|-------------|
| Check | ~1 minute | 3 (parallel) |
| Update | ~20-30 seconds | 1 (planning) |
| Optimize | ~30-45 seconds | 1 (context-optimizer) |
