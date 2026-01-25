# Edge Case Scenarios

**Purpose**: Detailed definitions of 7 required edge cases for test dataset diversity

**Domain**: Algorithm validation test datasets

**Reference**: Used by `.claude/agents/dev-tools/test-dataset-creator/test-dataset-creator.md`

---

## Required Edge Cases (7/7 Coverage)

### 1. Mixed Change Types

**Definition**: Single commit containing multiple Conventional Commit types

**Real-World Examples**:
- `feat(api): add user endpoint + fix(auth): resolve token expiry bug`
- `refactor(db): optimize queries + docs: update API documentation`
- `test: add integration tests + ci: enable coverage reports`

**Algorithmic Challenge**:
- File grouping algorithms must handle heterogeneous change types
- Commit classification cannot rely on single-type assumption
- Group prioritization requires multi-criteria scoring

**Ground Truth Heuristic**:
```python
# Separate by change type prefix, create distinct groups
groups = []
for change_type in ["feat", "fix", "refactor", "docs", "test"]:
    type_files = [f for f in files if f.change_type == change_type]
    if type_files:
        groups.append({"type": change_type, "files": type_files})
```

**Identification in Git History**:
```bash
AGENT_NAME=test-dataset-creator git log --oneline --all -150 | grep -E "(feat|fix).*\+(fix|docs|test)"
```

---

### 2. Test-Only Changes

**Definition**: Commit modifying exclusively test files, no application code

**Real-World Examples**:
- `test: add missing unit tests for auth module`
- `test: improve test coverage for payment processor`
- `ci: update test fixtures for new API version`

**Algorithmic Challenge**:
- Traditional grouping by feature may fail (no feature code changed)
- Code-test coupling analysis produces empty results
- Commit impact assessment requires special handling

**Ground Truth Heuristic**:
```python
# Group by test module or feature under test
if all(file.path.startswith("tests/") for file in files):
    # Extract feature from test path: tests/unit/auth/ -> auth
    feature = extract_feature_from_test_path(files[0].path)
    groups = [{"feature": feature, "type": "test", "files": files}]
```

**Identification in Git History**:
```bash
AGENT_NAME=test-dataset-creator git log --name-only --all -150 | awk '/^commit/,/^$/ {if (/^tests\//) print}'
```

---

### 3. Large Repository (50+ Files)

**Definition**: Commit changing 50 or more files simultaneously

**Real-World Examples**:
- Version bumps (`chore: update dependencies to v2.0`)
- Mass refactoring (`refactor: rename API endpoints across project`)
- Code formatting (`style: apply black formatter to all Python files`)

**Algorithmic Challenge**:
- Naive file grouping produces unmanageable group sizes
- Performance degrades with O(n²) pairwise comparisons
- Must identify "umbrella changes" vs. feature groups

**Ground Truth Heuristic**:
```python
# Detect bulk operations, create logical umbrella group
if len(files) > 50:
    if is_dependency_update(files):
        groups = [{"type": "dependency_update", "files": files}]
    elif is_mass_refactoring(files):
        groups = [{"type": "mass_refactoring", "files": files}]
    else:
        # Fall back to directory-based grouping
        groups = group_by_directory(files, max_group_size=10)
```

**Identification in Git History**:
```bash
AGENT_NAME=test-dataset-creator git log --stat --all -150 | awk '/files changed/ && $1 >= 50 {print}'
```

---

### 4. Low Confidence / Ambiguous

**Definition**: Scenarios with multiple valid grouping interpretations, no clear "correct" answer

**Edge Case Threshold**: Confidence <0.70 triggers edge case tagging (must have at least ONE scenario below this threshold for edge case coverage)

**Confidence Ranges** (system-wide):
- **High confidence**: 0.85-1.0 (feature-based grouping with explicit match)
- **Medium confidence**: 0.70-0.84 (directory-based grouping with 3+ files)
- **Low confidence**: 0.50-0.69 (fallback heuristics, temporal coupling) → **TAG AS EDGE CASE**
- **Ambiguous**: <0.50 (conflicting heuristics, no clear winner) → **ALWAYS TAG AS EDGE CASE**

**Real-World Examples**:
- Unrelated files bundled in single commit (poor commit hygiene)
- Feature spanning multiple domains (cross-cutting concern)
- Experimental code with unclear purpose

**Algorithmic Challenge**:
- Cannot rely on single heuristic for grouping
- Must generate confidence scores and alternative groupings
- Ground truth requires expert judgment simulation

**Ground Truth Heuristic**:
```python
# Constant for edge case threshold (matches system requirement: ≥0.70 average confidence)
LOW_CONFIDENCE_THRESHOLD = 0.70

# Generate multiple plausible groupings with confidence scores
groupings = [
    {"groups": group_by_directory(files), "confidence": 0.65},
    {"groups": group_by_change_type(files), "confidence": 0.60},
    {"groups": group_by_file_extension(files), "confidence": 0.55}
]
# Select highest confidence, flag as ambiguous if < threshold
best_grouping = max(groupings, key=lambda g: g["confidence"])
if best_grouping["confidence"] < LOW_CONFIDENCE_THRESHOLD:
    best_grouping["flags"] = ["low_confidence", "ambiguous"]
```

**Edge Case Tagging Rules**:
- **At least ONE scenario** with confidence <0.70 required for edge case coverage
- **Not all** low-confidence scenarios need tagging (only representative examples)
- **Target**: 1-3 low-confidence scenarios per dataset (enough for algorithm validation)

**Identification in Git History**:
```bash
# Look for commits with diverse file paths and types
AGENT_NAME=test-dataset-creator git log --name-only --all -150 | awk '/^commit/,/^$/ {if (/\.py$|\.md$|\.yaml$/) print}'
```

---

### 5. Renamed/Deleted Files

**Definition**: Commits containing file rename or delete operations (not just modifications)

**Real-World Examples**:
- `refactor: rename auth.py -> authentication.py`
- `chore: remove deprecated API endpoints`
- `refactor: reorganize project structure (move files)`

**Algorithmic Challenge**:
- File similarity detection must track renames (not just paths)
- Deleted files have no current content for analysis
- Git diff format differs for renames (`R100`) vs. modifications (`M`)

**Ground Truth Heuristic**:
```python
# Track file identity through renames, group deletions by purpose
for file in files:
    if file.operation == "rename":
        # Group with related files in new location
        target_group = find_group_by_directory(file.new_path)
        target_group.files.append(file)
    elif file.operation == "delete":
        # Group by deletion reason (deprecated, refactored, obsolete)
        deletion_reason = infer_deletion_reason(file.path, commit_message)
        deletion_group = find_or_create_group(deletion_reason)
        deletion_group.files.append(file)
```

**Identification in Git History**:
```bash
AGENT_NAME=test-dataset-creator git log --diff-filter=R --diff-filter=D --name-status --all -150
```

---

### 6. Ungrouped Files

**Definition**: Files that don't fit into any logical group (singletons)

**Real-World Examples**:
- One-off configuration changes (`chore: update .gitignore`)
- Isolated bug fixes (`fix: resolve typo in README`)
- Standalone utility scripts (`feat: add backup script`)

**Algorithmic Challenge**:
- Forced grouping produces meaningless clusters
- Must recognize when "no group" is the correct answer
- Singleton handling affects overall grouping metrics

**Ground Truth Heuristic**:
```python
# Allow singletons when grouping confidence < threshold
groups = []
for file in files:
    best_group = find_best_group(file, existing_groups)
    if best_group and best_group.confidence > 0.70:
        best_group.files.append(file)
    else:
        # Create singleton group
        groups.append({"type": "singleton", "files": [file]})
```

**Identification in Git History**:
```bash
# Find commits with 1-2 files, diverse paths
AGENT_NAME=test-dataset-creator git log --stat --all -150 | awk '/1 file changed|2 files changed/ {print}'
```

---

### 7. Dependency Ordering

**Definition**: Files with strict dependency relationships requiring ordered processing

**Real-World Examples**:
- Database migrations (`001_create_users.sql` → `002_add_auth.sql`)
- Module initialization (`__init__.py` must precede submodules)
- Build system changes (`Makefile` → dependent scripts)

**Algorithmic Challenge**:
- Topological sorting required for correct processing order
- Circular dependencies must be detected and flagged
- Parallel processing assumptions invalid

**Ground Truth Heuristic**:
```python
# Build dependency graph, perform topological sort
dependency_graph = build_dependency_graph(files)
if has_cycle(dependency_graph):
    groups = [{"type": "circular_dependency", "files": files, "error": True}]
else:
    sorted_files = topological_sort(dependency_graph)
    groups = [{"type": "ordered", "files": sorted_files, "must_preserve_order": True}]
```

**Identification in Git History**:
```bash
# Find commits with migration files or __init__.py changes
AGENT_NAME=test-dataset-creator git log --name-only --all -150 | grep -E "(migrations/|__init__\.py)"
```

---

## Coverage Validation

### Validation Checklist

```python
edge_cases_required = [
    "mixed_change_types",
    "test_only_changes",
    "large_repository_50_files",
    "low_confidence_ambiguous",
    "renamed_deleted_files",
    "ungrouped_files",
    "dependency_ordering"
]

def validate_edge_case_coverage(scenarios):
    covered = set()
    for scenario in scenarios:
        covered.update(scenario.edge_case_tags)

    missing = set(edge_cases_required) - covered
    coverage_ratio = len(covered) / len(edge_cases_required)

    return {
        "covered": list(covered),
        "missing": list(missing),
        "coverage_ratio": coverage_ratio,
        "passed": coverage_ratio == 1.0
    }
```

### Quality Thresholds

- **Required**: 7/7 edge cases covered (100%)
- **Each edge case**: At least 1 scenario (can have multiple)
- **Realistic scenarios**: Edge cases must be mined from real git history (not synthetic)
- **Ground truth quality**: Expert decisions must have confidence ≥0.70 or be flagged as "low_confidence"

---

**Token Savings**: ~45 lines externalized from agent definition
