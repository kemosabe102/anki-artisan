# Domain Heuristics for Ground Truth Generation

**Purpose**: Rules for simulating expert decisions in algorithm-specific test datasets

**Domain**: Algorithm validation test datasets

**Reference**: Used by `.claude/agents/dev-tools/test-dataset-creator/test-dataset-creator.md`

---

## FileGrouper Heuristics

### Purpose

Generate simulated expert file grouping decisions that reflect how a human developer would logically organize changed files in a commit.

### Heuristic Hierarchy

**Priority 1: Functional Cohesion** (highest weight)
- Files implementing the same feature or bugfix
- Related by explicit feature markers in commit message
- Example: `feat(auth): add OAuth2 support` → group all `auth/oauth2*` files

**Priority 2: Directory Proximity** (medium-high weight)
- Files in the same directory or subdirectory
- Assumes directory structure reflects logical modules
- Example: `packages/api/users/*` files form natural group

**Priority 3: File Type Similarity** (medium weight)
- Files with same extension or role (source, test, config)
- Example: All `.py` implementation files vs. all `.md` documentation

**Priority 4: Change Type Alignment** (medium-low weight)
- Files sharing same Conventional Commit type (feat, fix, refactor)
- Example: All `feat` files vs. all `fix` files

**Priority 5: Temporal Coupling** (low weight, from git history)
- Files frequently changed together in past commits
- Requires git log analysis: `AGENT_NAME=test-dataset-creator git log --follow --stat`

### Decision Algorithm

```python
def simulate_expert_grouping(files, commit_message, git_history):
    """
    Simulate expert file grouping using weighted heuristics.

    Returns: List[FileGroup] with confidence scores
    """
    groups = []

    # Step 1: Extract feature hints from commit message
    feature = extract_feature_from_message(commit_message)

    # Step 2: Apply heuristics in priority order
    if feature:
        # Priority 1: Functional cohesion
        feature_files = [f for f in files if feature in f.path]
        if feature_files:
            groups.append({
                "id": f"FEATURE_{feature.upper()}",
                "files": feature_files,
                "heuristic": "functional_cohesion",
                "confidence": 0.90,
                "rationale": f"All files related to {feature} feature"
            })
            files = [f for f in files if f not in feature_files]

    # Priority 2: Directory proximity
    directory_groups = group_by_directory(files, max_depth=2)
    for dir_name, dir_files in directory_groups.items():
        if len(dir_files) >= 2:
            groups.append({
                "id": f"DIR_{sanitize(dir_name)}",
                "files": dir_files,
                "heuristic": "directory_proximity",
                "confidence": 0.75,
                "rationale": f"Files in {dir_name} directory"
            })
            files = [f for f in files if f not in dir_files]

    # Priority 3: File type similarity
    type_groups = group_by_extension(files)
    for ext, type_files in type_groups.items():
        if len(type_files) >= 3:
            groups.append({
                "id": f"TYPE_{ext.upper()}",
                "files": type_files,
                "heuristic": "file_type_similarity",
                "confidence": 0.65,
                "rationale": f"All {ext} files"
            })
            files = [f for f in files if f not in type_files]

    # Priority 4: Change type alignment
    change_type_groups = group_by_change_type(files)
    for change_type, ct_files in change_type_groups.items():
        if len(ct_files) >= 2:
            groups.append({
                "id": f"CHANGETYPE_{change_type.upper()}",
                "files": ct_files,
                "heuristic": "change_type_alignment",
                "confidence": 0.60,
                "rationale": f"All {change_type} changes"
            })
            files = [f for f in files if f not in ct_files]

    # Remaining files become singletons (ungrouped edge case)
    for file in files:
        groups.append({
            "id": f"SINGLETON_{sanitize(file.path)}",
            "files": [file],
            "heuristic": "ungrouped",
            "confidence": 0.50,
            "rationale": "No clear grouping relationship found"
        })

    return groups
```

### Confidence Scoring Rules

**High Confidence (0.85-1.0)**:
- Feature-based grouping with explicit commit message match
- All files in same directory with clear functional purpose
- Well-documented architectural pattern (e.g., `models/`, `controllers/`)

**Medium Confidence (0.70-0.84)**:
- Directory-based grouping with 3+ files
- File type grouping with strong convention (e.g., all tests)
- Change type alignment with supporting evidence

**Low Confidence (0.50-0.69)**:
- File type grouping with 2 files only
- Change type alignment without other evidence
- Fallback heuristics (temporal coupling, file name similarity)

**Ambiguous (<0.50)**:
- Singletons (ungrouped files)
- Conflicting heuristics (multiple groupings equally valid)
- Missing context (no commit message, no directory structure)

---

## Commit Classification Heuristics

### Purpose

Determine Conventional Commit type when not explicitly specified in commit message.

### Heuristic Rules

**feat (Feature)**:
- New files added: `AGENT_NAME=test-dataset-creator git diff --name-status | grep "^A"`
- Significant new functionality: `lines_added > 100 && new_functions > 5`
- Keywords in message: "add", "implement", "introduce", "create"

**fix (Bug Fix)**:
- Small targeted changes: `files_changed <= 3 && lines_changed < 50`
- Keywords in message: "fix", "resolve", "correct", "repair", "patch"
- Test files include regression tests

**refactor (Code Refactoring)**:
- No behavioral changes (tests unchanged or minimal)
- High churn ratio: `lines_deleted / lines_added > 0.8`
- Keywords in message: "refactor", "restructure", "reorganize", "cleanup"

**docs (Documentation)**:
- Only documentation files changed: `all(f.endswith('.md') for f in files)`
- Keywords in message: "docs", "documentation", "readme", "guide"

**test (Testing)**:
- Only test files changed: `all('test' in f.path for f in files)`
- Keywords in message: "test", "spec", "coverage"

**style (Code Style)**:
- Whitespace/formatting only: `AGENT_NAME=test-dataset-creator git diff --ignore-all-space` shows no changes
- Keywords in message: "style", "format", "lint", "prettier"

### Confidence Scoring

```python
def classify_commit_type(files, commit_message, git_diff):
    """
    Classify commit type using heuristics.

    Returns: (commit_type, confidence)
    """
    scores = {
        "feat": 0.0,
        "fix": 0.0,
        "refactor": 0.0,
        "docs": 0.0,
        "test": 0.0,
        "style": 0.0
    }

    # Apply keyword matching (0.3 weight)
    keyword_scores = score_by_keywords(commit_message)
    for type, score in keyword_scores.items():
        scores[type] += score * 0.3

    # Apply file pattern matching (0.4 weight)
    file_scores = score_by_files(files)
    for type, score in file_scores.items():
        scores[type] += score * 0.4

    # Apply change metrics (0.3 weight)
    metric_scores = score_by_metrics(git_diff)
    for type, score in metric_scores.items():
        scores[type] += score * 0.3

    # Select highest scoring type
    best_type = max(scores, key=scores.get)
    confidence = scores[best_type]

    return best_type, confidence
```

---

## General Heuristic Principles

### When to Use Heuristics

**Recommended**:
- Algorithm test dataset generation (simulating expert decisions)
- Baseline ground truth for algorithm validation
- Exploratory analysis when ground truth unavailable

**Not Recommended**:
- Production algorithm implementation (use trained models or formal rules)
- Safety-critical systems (require verified ground truth)
- Legal/compliance applications (require auditable decisions)

### Heuristic Quality Assessment

**Validation Methods**:
1. **Precision**: Sample generated ground truth, manually verify correctness
2. **Consistency**: Run heuristics multiple times, check for identical results
3. **Coverage**: Ensure all edge cases have applicable heuristics
4. **Explainability**: All decisions must have documented rationale

**Quality Thresholds**:
- Average confidence ≥0.70 across all scenarios
- <10% of scenarios flagged as ambiguous (confidence <0.50)
- 100% of decisions have documented heuristic source

### Documenting Heuristic Sources

**Required Documentation**:
```json
{
  "ground_truth_methodology": {
    "heuristic_source": "docs/04-guides/test-dataset-creator/domain-heuristics.md",
    "algorithm_spec": "docs/01-planning/specifications/004-git-github-agent/SPEC.md",
    "expert_validation": false,
    "confidence_threshold": 0.70,
    "ambiguous_scenario_count": 2
  }
}
```

---

**Token Savings**: ~55 lines externalized from agent definition
