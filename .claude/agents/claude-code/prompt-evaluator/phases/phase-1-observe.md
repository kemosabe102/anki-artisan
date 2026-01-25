# Phase 1: OBSERVE - Pre-Flight & Baseline Collection

**OODA Stage**: OBSERVE | **Time Allocation**: 15-20%

**Purpose**: Validate agent exists, gather baselines, load evaluation frameworks

**Deliverable**: Validated agent path, token count baseline, loaded framework criteria

---

## Workflow Steps

### Step 1.1: Pre-Flight Validation

**Input**: Agent file path from user request

**Process**:
1. `Glob("{agent_path}")` - Verify agent file exists
2. `Glob("scripts/calculate_tokens.py")` - Verify token counter script exists
3. `Read(agent_path, limit=20)` - Extract frontmatter, check schema reference
4. If schema referenced: `Glob("{agent_dir}/schemas/*.json")` - Verify schema exists

**Output**: Pre-flight validation report with pass/fail per check


### Step 1.2: Token Count Baseline

**Input**: Validated agent path

**Process**:
1. `Bash("AGENT_NAME=prompt-evaluator uv run python scripts/calculate_tokens.py {agent_path} --format=json")`
2. Parse `summary.total_tokens` as baseline
3. Store for Framework 3 (Token Optimization) comparison

**Output**: `baseline_tokens` integer, confidence 1.0 (or 0.3 if using line heuristic)

**Error Handling**: If script times out, use `line_count x 10` heuristic with confidence: 0.3

### Step 1.3: Framework Loading

**Input**: None (uses known paths)

**Process**:
1. `Read("docs/evaluation-frameworks.md")` - Load 7 framework criteria
2. `Read("docs/anti-patterns.md")` - Load anti-pattern catalog
3. `Read("docs/optimization-calculations.md")` - Load priority formulas
4. `Read("00-core/frameworks/README.md")` - Load domain-framework mappings

**Output**: Loaded criteria for all 7 evaluation frameworks


---

## Quick Checklist

Before advancing to Phase 2 (ORIENT):

- [ ] Agent file exists and is readable
- [ ] Token counter script accessible
- [ ] Baseline token count captured
- [ ] Evaluation framework docs loaded
- [ ] Schema/docs references validated (if present)

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping token baseline | Always run calculate_tokens.py first |
| Assuming docs exist | Validate each referenced file with Glob |
| Proceeding without frameworks | Load all 7 framework criteria before evaluation |
| Ignoring missing schema | Note in `incomplete_dimensions`, reduce confidence |

---

## Exit Criteria

**All pre-flight checks must pass (or be noted) to proceed**

| Criterion | Weight | Check |
|-----------|--------|-------|
| Agent file exists | 0.30 | Glob returns path |
| Token baseline captured | 0.25 | Non-zero token count |
| Framework docs loaded | 0.25 | All 4 doc files readable |
| References validated | 0.10 | Schema/docs exist if referenced |
| Pre-flight report ready | 0.10 | Pass/fail documented |

---

**Next Phase**: [Phase 2: ORIENT](phase-2-orient.md)
