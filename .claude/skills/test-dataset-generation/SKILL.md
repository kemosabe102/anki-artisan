---
name: test-dataset-generation
description: >
  Generate algorithm validation test datasets by mining git history, applying domain heuristics
  for simulated expert ground truth, and creating Pydantic-validated JSON. Diversity score >=0.80,
  7/7 edge cases required. Use for: generate test data, create fixtures, validation datasets,
  ground truth generation, test scenario creation. NOT for: running tests (test-execution skill),
  writing test code (test-generation skill), algorithm implementation.
---

# Test Dataset Generation Skill

Transform git history into diverse test scenarios with simulated expert ground truth.

## Reference Documentation

- **Diversity Sampling** -> [references/diversity-sampling.md](references/diversity-sampling.md)
- **Domain Heuristics** -> [references/domain-heuristics.md](references/domain-heuristics.md)
- **Edge Cases** -> [references/edge-cases.md](references/edge-cases.md)

---

## Quality Targets

| Metric | Threshold | Description |
|--------|-----------|-------------|
| Diversity Score | >= 0.80 | change_type_entropy*0.4 + file_count_dist*0.3 + edge_case_coverage*0.3 |
| Edge Cases | 7/7 | All 7 required edge case types covered |
| Confidence | >= 0.70 avg | Ground truth confidence average |
| Quality Grade | A-F | A(>=0.90), B(0.75-0.89), C(0.60-0.74), D(0.40-0.59), F(<0.40) |

---

## Workflow: Dataset Generation

### Phase 1: Requirements Analysis

1. Parse request for:
   - Scenario count target (default: 20)
   - Diversity requirements (default: >= 0.80)
   - Edge case requirements (default: 7/7)
2. Assess git history availability
3. Plan sampling strategy

### Phase 2: Git History Mining

```bash
# Extract commits with stat information
git log --oneline --stat -150 > candidates.txt

# Filter by Conventional Commit types
git log --oneline -150 | grep -E "^[a-f0-9]+ (feat|fix|refactor|docs|test):"

# Find edge case candidates
git log --diff-filter=R --diff-filter=D --name-status -150  # Renamed/deleted
git log --stat -150 | awk '/files changed/ && $1 >= 50'      # Large repos
```

### Phase 3: Diversity Sampling

Apply stratified sampling to select scenarios:

**Change Type Distribution**:
- feat: 20-30% | fix: 15-25% | refactor: 10-20%
- docs: 5-15% | test: 5-15% | other: 15-25%

**File Count Distribution**:
- 1-5 files: 15% | 6-10 files: 40%
- 11-15 files: 30% | 16-50+ files: 15%

### Phase 4: Ground Truth Simulation

Apply heuristics in priority order:
1. **Functional Cohesion** (0.90 confidence) - Feature-based grouping
2. **Directory Proximity** (0.75 confidence) - Same directory
3. **File Type Similarity** (0.65 confidence) - Same extension
4. **Change Type Alignment** (0.60 confidence) - Same commit type
5. **Ungrouped** (0.50 confidence) - No clear relationship

### Phase 5: Validation

- [ ] Scenario count meets target
- [ ] Diversity score >= 0.80
- [ ] Edge cases: 7/7 covered
- [ ] Ground truth confidence >= 0.70 average
- [ ] JSON schema validation passed

---

## Pydantic Schemas

### FileChange

```python
class FileChange(BaseModel):
    file_path: str
    change_type: str  # feat, fix, refactor, docs, test, etc.
    lines_added: int = Field(ge=0)
    lines_deleted: int = Field(ge=0)
```

### CommitScenario

```python
class CommitScenario(BaseModel):
    scenario_id: str = Field(pattern=r"^SCENARIO-\d{3}$")
    commit_sha: str = Field(min_length=7, max_length=40)
    commit_message: str
    files: list[FileChange]
    edge_case_tags: list[str] = []
```

### ExpertGroundTruth

```python
class ExpertGroundTruth(BaseModel):
    scenario_id: str = Field(pattern=r"^SCENARIO-\d{3}$")
    expert_decision: dict  # Algorithm-specific (e.g., file groupings)
    confidence: float = Field(ge=0.0, le=1.0)
    rationale: str = Field(min_length=10)
```

---

## Edge Case Tags

All datasets must include at least one scenario for each:

| Tag | Description |
|-----|-------------|
| `mixed_change_types` | Commit with multiple change types |
| `test_only_changes` | Only test files modified |
| `large_repository_50_files` | 50+ files changed |
| `low_confidence_ambiguous` | Confidence < 0.70, multiple valid interpretations |
| `renamed_deleted_files` | File rename or delete operations |
| `ungrouped_files` | Files with no logical grouping |
| `dependency_ordering` | Files with strict dependency relationships |

---

## Output Files

| File | Purpose |
|------|---------|
| `tests/fixtures/scenarios.json` | Test scenarios with file changes |
| `tests/fixtures/ground_truth.json` | Simulated expert decisions |
| `tests/fixtures/metadata.json` | Diversity metrics, quality grade |

---

## Error Recovery

| Issue | Recovery |
|-------|----------|
| Diversity < 0.80 | Expand git log range (150 -> 500 commits) |
| Missing edge cases | Search older history/branches |
| Schema validation fails | Return FAILURE with Pydantic errors |
| Ambiguous ground truth | Use conservative heuristic, flag low_confidence |

---

## Anti-Patterns

- Modifying algorithm code (READ-ONLY for heuristics)
- Creating synthetic data without real git commits
- Skipping diversity validation
- Generating datasets without edge case coverage
- Running tests or executing algorithms

---

## Output Format

### SUCCESS

```json
{
  "status": "SUCCESS",
  "confidence": 0.92,
  "summary": "Generated 20 scenarios, diversity 0.88, 7/7 edge cases, grade B",
  "datasets_created": ["scenarios.json", "ground_truth.json"],
  "diversity_metrics": {
    "change_type_entropy": 0.85,
    "file_count_distribution": 0.90,
    "edge_case_coverage": 1.0,
    "overall": 0.88
  },
  "quality_grade": "B"
}
```

### FAILURE

```json
{
  "status": "FAILURE",
  "failure_type": "insufficient_diversity",
  "reasons": ["Only 5/7 edge cases found", "Diversity score 0.72"],
  "recovery_suggestions": ["Expand git log to 500 commits", "Search feature branches"],
  "partial_results": {"scenarios_found": 15}
}
```
