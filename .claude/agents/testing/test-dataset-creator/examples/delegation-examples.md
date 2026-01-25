# Delegation Examples

**Purpose**: How orchestrator delegates to test-dataset-creator

---

## Basic Dataset Generation

```python
Task(test-dataset-creator, prompt="""
Generate 20 FileGrouper test scenarios from gauntlet-agents git history.

Requirements:
- 20 scenarios covering all Conventional Commit types
- File count distribution: 1-5 (3), 6-10 (8), 11-15 (6), 16-50 (3)
- Edge cases: 7/7 required (mixed types, test-only, large repo, low confidence, renamed/deleted, ungrouped, dependencies)
- Ground truth: Simulated expert grouping using FileGrouper heuristics

Algorithm heuristics source: docs/01-planning/specifications/004-git-github-agent/filegrouper-heuristics.md

Output:
- tests/fixtures/filegrouper_scenarios.json
- tests/fixtures/filegrouper_ground_truth.json
""")
```

---

## Custom Algorithm Dataset

```python
Task(test-dataset-creator, prompt="""
Generate 30 commit classification test scenarios.

Requirements:
- 30 scenarios with diverse Conventional Commit types
- Focus on ambiguous commits (fix vs refactor, feat vs chore)
- Ground truth: Simulated expert classification using commit message + file patterns

Algorithm heuristics source: docs/01-planning/specifications/commit-classifier/SPEC.md

Output:
- tests/fixtures/commit_classification_scenarios.json
- tests/fixtures/commit_classification_ground_truth.json
""")
```

---

## Heuristic Extraction Only

```python
Task(test-dataset-creator, prompt="""
Extract heuristics from FileGrouper specification for ground truth generation.

Specification source: docs/01-planning/specifications/004-git-github-agent/SPEC.md
Algorithm code: packages/git_github/filegrouper.py (READ-ONLY)

Output: Structured heuristic rules document with:
- Priority-ordered heuristics
- Confidence scoring rules
- Edge case handling
""")
```

---

## Handling Partial Results

When orchestrator receives FAILURE with partial_results:

```python
# Option 1: Expand search
Task(test-dataset-creator, prompt="""
Continue previous dataset generation with expanded git history.

Previous results: tests/fixtures/filegrouper_scenarios.json (15 scenarios)
Missing edge cases: large_repository_50_files, dependency_ordering

Expand git log to last 500 commits (was 150).
Focus on finding missing edge cases.
""")

# Option 2: Manual scenario creation
# Orchestrator creates synthetic scenarios for missing edge cases
# Then re-validates with test-dataset-creator
```

---

## Multi-Agent Coordination

**Upstream**: researcher-codebase provides git history diversity analysis
**Downstream**: test-executor uses generated datasets for algorithm validation

```python
# Step 1: Research git history diversity
result = Task(researcher-codebase, prompt="Analyze git log diversity for test dataset generation...")

# Step 2: Generate datasets with context
Task(test-dataset-creator, prompt=f"""
Generate datasets using diversity analysis:
{result.diversity_summary}

Focus on underrepresented change types: {result.gaps}
""")

# Step 3: Run algorithm validation
Task(test-executor, prompt="Run FileGrouper against tests/fixtures/filegrouper_scenarios.json...")
```
