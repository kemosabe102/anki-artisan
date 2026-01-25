# Test Dataset Creator Workflow Details

**Purpose**: Detailed phase-by-phase workflow execution for dataset generation

**Domain**: Algorithm validation test datasets

**Reference**: Used by `.claude/agents/dev-tools/test-dataset-creator/test-dataset-creator.md`

---

## Dataset Generation Workflow Phases

### Phase 1: Analysis (30 seconds)

**Objective**: Parse requirements and assess complexity

**Actions**:
- Parse dataset requirements from orchestrator input
- Extract targets: scenario count, diversity metrics (≥0.80), edge case coverage (7/7)
- Assess complexity: simple git mining (20 scenarios from recent commits) vs. complex (50+ scenarios requiring deep history search)
- Identify unclear requirements or missing heuristics
- Plan git history search strategy (commit range, branch scope, time window)

**Todo Creation for Complex Generation**:

```markdown
- [ ] Mine git history for candidate commits (diversity sampling)
- [ ] Generate scenarios from candidates (prioritize edge cases)
- [ ] Extract algorithm heuristics from specs/code (READ-ONLY)
- [ ] Simulate expert ground truth using heuristics
- [ ] Create scenario JSON with Pydantic validation
- [ ] Create ground truth JSON with Pydantic validation
- [ ] Validate diversity metrics (≥0.80) and edge case coverage (7/7)
- [ ] Generate metadata report with quality grading
```

**Complexity Assessment Criteria**:
- **Simple** (<10 scenarios, recent git history, well-documented heuristics): 10-15 min
- **Medium** (20-30 scenarios, diverse change types, documented heuristics): 20-25 min
- **Complex** (50+ scenarios, all edge cases, ambiguous heuristics): 30 min (max time-box)

---

### Phase 2: Research (2-3 minutes)

**Objective**: Mine git history and extract algorithm heuristics

**Git History Mining Strategy**:

```bash
# Step 1: Extract diverse commits with stat information
AGENT_NAME=test-dataset-creator git log --oneline --stat -150 > /tmp/git_history.txt

# Step 2: Filter by Conventional Commit types
AGENT_NAME=test-dataset-creator grep -E 'feat|fix|refactor|docs|test|style|perf|ci|build|chore' /tmp/git_history.txt | head -50

# Step 3: Analyze file count distribution per commit
AGENT_NAME=test-dataset-creator git log --stat -150 --format="%H" | while read sha; do
  files=$(git show --stat $sha | tail -1 | awk '{print $1}')
  echo "$sha: $files files"
done

# Step 4: Identify edge case candidates
AGENT_NAME=test-dataset-creator git log --diff-filter=R --diff-filter=D --name-status -150  # Renamed/deleted files
AGENT_NAME=test-dataset-creator git log --stat -150 | awk '/files changed/ && $1 >= 50'  # Large repo scenarios
```

**Heuristic Extraction Process**:

1. **Read algorithm specification docs** for decision logic
   - Location: `docs/01-planning/specifications/**/SPEC.md`
   - Extract: Decision criteria, grouping rules, priority formulas
   - Example: FileGrouper uses functional cohesion > directory proximity > file type similarity

2. **Grep algorithm code** for heuristic patterns (READ-ONLY)
   - Location: `packages/**/`, `tests/algorithms/**/`
   - Search patterns: Decision points, scoring formulas, edge case handling
   - Example: `grep -rn "def calculate_priority" packages/git_github/filegrouper.py`

3. **Document heuristic rules** for ground truth simulation
   - Create priority-ordered list of heuristics
   - Define confidence scoring for each heuristic
   - Map heuristics to edge case scenarios

**Delegation to Other Agents**:

When research exceeds time budget (>3 min), delegate to specialist agents:

- **researcher-codebase**: "Analyze git log output, identify 20 diverse commit SHAs covering all change types (feat, fix, refactor, etc.), varying file counts (1-5, 6-10, 11-15, 16-50), prioritize edge cases if present (mixed types, test-only, large repos, renamed/deleted files)"

- **researcher-external**: Only if complex library pattern research needed (e.g., "Find pytest fixture patterns for dataset validation")

- **python-code-implementer**: Only if complex JSON transformation logic needed (rarely - most datasets use simple Pydantic models)

- **debugger**: Only if JSON validation failures occur during development

**Research Outputs**:
- List of 50-150 candidate commit SHAs
- Diversity assessment: change type distribution, file count spread, edge case presence
- Algorithm heuristics: decision rules, confidence thresholds, edge case handling
- Missing gaps: unavailable edge cases, insufficient diversity, unclear heuristics

---

### Phase 3: Todo Creation

**When to Use**: Dataset generation with 3+ distinct phases or potential blocking dependencies

**Structure**: Each todo item includes completion criteria and blocking dependency tracking (see Todo Management Protocol in agent definition)

**Standard Todo Breakdown for 20-Scenario Dataset**:

1. **Mine git history** for candidate commits (50-150 candidates)
   - Completion criteria: 50+ commits covering all change types, varying file counts
   - Dependencies: None (first step)
   - Estimated time: 1-2 minutes

2. **Apply diversity sampling** to select N scenarios (e.g., 20)
   - Completion criteria: 20 commits with diversity score ≥0.80, balanced change type distribution
   - Dependencies: Step 1 (requires candidate list)
   - Estimated time: 2-3 minutes

3. **Extract commit details** for each selected commit
   - Completion criteria: Files changed, lines added/deleted, change types extracted for all 20 scenarios
   - Dependencies: Step 2 (requires selected commits)
   - Estimated time: 2-3 minutes

4. **Load algorithm heuristics** from specs/code (READ-ONLY)
   - Completion criteria: Decision rules documented, confidence thresholds defined
   - Dependencies: None (can parallelize with Steps 1-3)
   - Estimated time: 2-3 minutes

5. **Simulate expert ground truth** using heuristics
   - Completion criteria: Expert decision generated for all 20 scenarios, confidence ≥0.70 average
   - Dependencies: Steps 3 and 4 (requires commit details AND heuristics)
   - Estimated time: 3-5 minutes

6. **Create scenario JSON file** with Pydantic validation
   - Completion criteria: tests/fixtures/scenarios.json created, schema validated
   - Dependencies: Step 3 (requires scenario objects)
   - Estimated time: 1 minute

7. **Create ground truth JSON file** with Pydantic validation
   - Completion criteria: tests/fixtures/ground_truth.json created, schema validated
   - Dependencies: Step 5 (requires ground truth objects)
   - Estimated time: 1 minute

8. **Validate diversity metrics** against targets
   - Completion criteria: Diversity score ≥0.80 confirmed, change type/file count distributions match targets
   - Dependencies: Step 6 (requires scenario dataset)
   - Estimated time: 30 seconds

9. **Validate edge case coverage** (7/7 required)
   - Completion criteria: All 7 edge cases present with at least 1 scenario each
   - Dependencies: Step 6 (requires scenario dataset with edge_case_tags)
   - Estimated time: 30 seconds

10. **Generate metadata report** with quality grading
    - Completion criteria: Quality score calculated, grade assigned (A-F), methodology documented
    - Dependencies: Steps 8 and 9 (requires validation results)
    - Estimated time: 1 minute

**Total Estimated Time**: 15-25 minutes for standard 20-scenario dataset

---

### Phase 4: Implementation (3-5 minutes)

**Detailed execution steps with code examples**

#### Step 1: Git History Mining

```bash
# Extract commit metadata for diverse scenarios
AGENT_NAME=test-dataset-creator git log --format="%H|%s|%an|%ad" --stat -150 > /tmp/git_history.txt

# Optional: Delegate to researcher-codebase for diversity sampling
# Input: git_history.txt, diversity targets from diversity-sampling.md
# Output: 20 commit SHAs with diversity justification
```

#### Step 2: Scenario Generation

For each selected commit SHA:

1. **Extract commit details**:
   ```bash
   AGENT_NAME=test-dataset-creator git show --stat <commit-sha> > /tmp/commit_<sha>.txt
   ```

2. **Parse files changed**, lines added/deleted, change type:
   ```python
   # Parse git show output
   files_section = extract_files_from_git_show(commit_output)
   for line in files_section:
       file_path, stats = parse_file_line(line)
       # Example: "packages/auth.py | 42 +++++++---"
       change = FileChange(
           file_path=file_path,
           change_type=infer_change_type(commit_message, file_path),
           lines_added=extract_additions(stats),
           lines_deleted=extract_deletions(stats)
       )
   ```

3. **Create scenario object** with Pydantic validation:
   ```python
   scenario = CommitScenario(
       scenario_id=f"SCENARIO-{index:03d}",
       commit_sha=sha,
       commit_message=commit_msg,
       files=file_changes,
       edge_case_tags=identify_edge_cases(file_changes, commit_msg)
   )
   ```

4. **Tag edge cases** (mixed types, test-only, large repo, etc.):
   ```python
   def identify_edge_cases(files, commit_msg):
       tags = []
       change_types = set(f.change_type for f in files)
       if len(change_types) > 1:
           tags.append("mixed_change_types")
       if all(is_test_file(f.file_path) for f in files):
           tags.append("test_only_changes")
       if len(files) >= 50:
           tags.append("large_repository_50_files")
       if any(f.operation in ["rename", "delete"] for f in files):
           tags.append("renamed_deleted_files")
       # ... check other edge cases
       return tags
   ```

#### Step 3: Ground Truth Simulation

**Reference**: See `docs/04-guides/test-dataset-creator/domain-heuristics.md` for complete heuristic algorithms

Apply algorithm heuristics to each scenario:

1. **Load heuristic rules** from algorithm specs/code (READ-ONLY)
   ```python
   # Read heuristics from specification
   heuristics = load_heuristics_from_spec("docs/01-planning/specifications/004-git-github-agent/SPEC.md")
   # Or from algorithm code (READ-ONLY)
   heuristic_code = Read("packages/git_github/filegrouper.py")
   ```

2. **Simulate expert decision** using domain heuristics
   ```python
   # Example: FileGrouper heuristics
   groups = simulate_expert_grouping(
       files=scenario.files,
       commit_message=scenario.commit_message,
       heuristics=heuristics
   )
   # Applies: functional cohesion > directory proximity > file type > change type
   ```

3. **Calculate confidence score** based on heuristic priority
   - High confidence (0.85-1.0): Feature-based grouping with explicit commit message match
   - Medium confidence (0.70-0.84): Directory-based grouping with 3+ files
   - Low confidence (0.50-0.69): Fallback heuristics (temporal coupling, file name similarity)

4. **Document rationale** for expert decision
   ```python
   rationale = f"Applied {heuristic_name} heuristic: {explanation}"
   # Example: "Applied functional_cohesion heuristic: All files related to OAuth2 feature based on commit message and file paths"
   ```

5. **Create ground truth object** with Pydantic validation
   ```python
   ground_truth = ExpertGroundTruth(
       scenario_id=scenario.scenario_id,
       expert_decision={"groups": groups},
       confidence=calculated_confidence,
       rationale=rationale
   )
   ```

#### Step 4: JSON File Creation

**Reference**: See `docs/04-guides/test-dataset-creator/validation-schemas.md` for complete Pydantic models

```python
# Create scenario dataset
scenario_dataset = TestDataset(
    scenario_count=len(scenarios),
    scenarios=scenarios
)

# Create ground truth dataset
ground_truth_dataset = GroundTruthDataset(
    ground_truth_count=len(ground_truths),
    ground_truths=ground_truths
)

# Write validated JSON files
Write("tests/fixtures/scenarios.json", scenario_dataset.model_dump_json(indent=2))
Write("tests/fixtures/ground_truth.json", ground_truth_dataset.model_dump_json(indent=2))

# Read-back verification
Read("tests/fixtures/scenarios.json")  # Verify file written correctly
```

---

### Phase 5: Validation (1 minute)

**Quality Validation Checks**:

**Reference**: See `docs/04-guides/test-dataset-creator/diversity-sampling.md` for diversity score calculation

- [ ] **Scenario count** meets target (e.g., 20 scenarios)
- [ ] **Change type distribution** matches targets:
  - feat: 20-30%, fix: 15-25%, refactor: 10-20%, docs: 5-15%, test: 5-15%, other: 15-25%
- [ ] **File count distribution** matches targets:
  - 1-5 files: 15%, 6-10 files: 40%, 11-15 files: 30%, 16-50+ files: 15%
- [ ] **Edge case coverage** complete (7/7 required):
  - mixed_change_types, test_only_changes, large_repository_50_files, low_confidence_ambiguous, renamed_deleted_files, ungrouped_files, dependency_ordering
- [ ] **Ground truth exists** for all scenarios (scenario_count == ground_truth_count)
- [ ] **Ground truth confidence** ≥0.70 average (or flagged as low-confidence edge case)
- [ ] **JSON schema validation** passed (Pydantic validation successful)
- [ ] **No duplicate commit SHAs** in scenario dataset
- [ ] **Diversity score** ≥0.80 (calculated using formula from diversity-sampling.md)

**Diversity Score Calculation**:

```python
diversity_score = (
    change_type_entropy * 0.4 +
    file_count_distribution_score * 0.3 +
    edge_case_coverage_ratio * 0.3
)
# Target: ≥0.80
```

**Validation Outcomes**:
- **All checks pass**: Proceed to Phase 6 (Reflection)
- **Diversity score <0.80**: Expand git log range (attempt 2) or report gap
- **Edge cases <7/7**: Search older commits (attempt 2) or flag missing cases
- **Schema validation fails**: Fix Pydantic errors, retry validation
- **Confidence <0.70 average**: Refine heuristics or flag low-confidence scenarios

---

### Phase 6: Reflection (30 seconds)

**Objective**: Document methodology and identify improvements

**Documentation Tasks**:
- Document dataset generation methodology (git log range, diversity strategy, heuristic sources)
- Record heuristics used for ground truth simulation (priority order, confidence thresholds)
- Identify gaps in git history diversity (missing edge cases, insufficient change type representation)
- Suggest manual scenario creation if needed (specific edge cases unavailable in git history)
- Generate lessons learned for future dataset generation (better heuristics, expanded search ranges)

**Output Format**:

SUCCESS with dataset files:
```json
{
  "status": "SUCCESS",
  "datasets_created": [...],
  "diversity_metrics": {...},
  "quality_validation": {...},
  "generation_methodology": {...}
}
```

FAILURE with recovery guidance:
```json
{
  "status": "FAILURE",
  "failure_type": "insufficient_diversity",
  "reasons": [...],
  "recovery_suggestions": [...],
  "partial_results": {...}
}
```

Per `base-agent.schema.json` two-state model.

---

## Heuristic Extraction Workflow

**Input Requirements**: Algorithm specification file path or code file path

### Phase 1: Analysis
- Parse algorithm specs for decision logic
- Identify decision points and scoring formulas

### Phase 2: Research
- Grep algorithm code for heuristic patterns (READ-ONLY)
- Search for: priority calculations, grouping rules, confidence scoring

### Phase 3: Todo Creation
- Structured heuristic documentation plan
- List all decision rules to extract

### Phase 4: Implementation
- Extract and document heuristic rules
- Create priority-ordered heuristic list
- Define confidence scoring for each heuristic

### Phase 5: Validation
- Verify heuristic completeness (all decision paths covered)
- Ensure clarity (no ambiguous rules)
- Test heuristics on sample scenarios

### Phase 6: Reflection
- Document heuristic extraction methodology
- Identify missing or unclear heuristics
- Suggest improvements to algorithm documentation

**Output Format**: Structured heuristic rules document for ground truth simulation (see `docs/04-guides/test-dataset-creator/domain-heuristics.md` for examples)

---

**Token Savings**: ~150 lines externalized from agent definition
