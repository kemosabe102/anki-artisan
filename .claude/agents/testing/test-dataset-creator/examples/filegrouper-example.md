# FileGrouper Dataset Generation Example

**Purpose**: Complete worked example of generating FileGrouper test scenarios from git history with simulated expert grouping.

**Domain**: Algorithm validation test datasets

**Reference**: Used by `.claude/agents/dev-tools/test-dataset-creator/test-dataset-creator.md`

---

## Example 1: FileGrouper Dataset Generation (SUCCESS)

### Input

```json
{
  "specific_objective": "Generate 20 FileGrouper test scenarios from gauntlet-agents git history with simulated expert grouping",
  "output_format": {
    "dataset_files": [
      "tests/fixtures/filegrouper_scenarios.json",
      "tests/fixtures/filegrouper_ground_truth.json"
    ],
    "metadata": {
      "scenario_count": 20,
      "diversity_metrics": {
        "change_types": { "feat": 5, "fix": 4, "refactor": 3 },
        "file_counts": { "1-5": 3, "6-10": 8, "11-15": 6, "16+": 3 },
        "edge_cases": [
          "mixed_types",
          "test_only",
          "large_repo",
          "low_confidence",
          "renamed_deleted",
          "ungrouped",
          "dependencies"
        ]
      }
    }
  },
  "tool_guidance": {
    "git_history_mining": "Use Bash(git log --stat) to extract real commit diffs",
    "codebase_analysis": "Use researcher-codebase for file relationship discovery",
    "simulation_approach": "Apply FileGrouper heuristics to generate expert-like grouping"
  },
  "task_boundaries": {
    "scope": "Test dataset generation only, no FileGrouper implementation",
    "exclusions": ["Modifying FileGrouper code", "Running actual algorithm"],
    "termination": "20 diverse scenarios OR git history exhausted OR 30 min elapsed"
  }
}
```

### Output (SUCCESS)

```json
{
  "status": "SUCCESS",
  "agent": "test-dataset-creator",
  "confidence": 0.92,
  "summary": "Generated 20 FileGrouper test scenarios with 7/7 edge cases covered, diversity score 0.88, quality grade B",
  "agent_specific_output": {
    "datasets_created": [
      {
        "file_path": "tests/fixtures/filegrouper_scenarios.json",
        "record_count": 20,
        "schema_version": "1.0",
        "validation_status": "passed"
      },
      {
        "file_path": "tests/fixtures/filegrouper_ground_truth.json",
        "record_count": 20,
        "schema_version": "1.0",
        "validation_status": "passed"
      }
    ],
    "diversity_metrics": {
      "change_types_distribution": {
        "feat": 5,
        "fix": 4,
        "refactor": 3,
        "docs": 2,
        "test": 2,
        "style": 1,
        "build": 1,
        "chore": 2
      },
      "file_count_distribution": {
        "1-5_files": 3,
        "6-10_files": 8,
        "11-15_files": 6,
        "16-50_files": 3
      },
      "edge_cases_covered": [
        "mixed_change_types",
        "test_only_changes",
        "large_repository_50_files",
        "low_confidence_ambiguous",
        "renamed_deleted_files",
        "ungrouped_files",
        "dependency_ordering"
      ]
    },
    "quality_validation": {
      "scenarios_with_ground_truth": 20,
      "edge_case_coverage": "7/7 required",
      "diversity_score": 0.88,
      "quality_grade": "B",
      "git_commits_analyzed": 150
    },
    "generation_methodology": {
      "git_log_range": "last 150 commits",
      "diversity_sampling_strategy": "stratified by change type and file count",
      "heuristic_source": "docs/01-planning/specifications/004-git-github-agent/filegrouper-heuristics.md",
      "ground_truth_simulation": "Applied FileGrouper grouping heuristics with confidence scoring"
    }
  }
}
```

## Example 2: Insufficient Diversity (FAILURE)

### Output (FAILURE)

```json
{
  "status": "FAILURE",
  "agent": "test-dataset-creator",
  "confidence": 0.65,
  "summary": "Insufficient diversity in git history, only 15/20 scenarios generated with 5/7 edge cases",
  "failure_details": {
    "failure_type": "insufficient_diversity",
    "reasons": [
      "Git history lacks sufficient 'refactor' type commits (found 2, need 3+)",
      "No large repository scenarios (50+ files) found in recent commits",
      "Missing 'dependency_ordering' edge case in available commits"
    ],
    "recovery_suggestions": [
      "Expand git log search to last 500 commits (currently 150)",
      "Create 2 synthetic large repository scenarios manually",
      "Lower diversity requirements to match available commit patterns"
    ],
    "partial_results": {
      "scenarios_generated": 15,
      "scenarios_file": "tests/fixtures/filegrouper_scenarios.json",
      "ground_truth_file": "tests/fixtures/filegrouper_ground_truth.json",
      "missing_edge_cases": ["large_repository_50_files", "dependency_ordering"],
      "diversity_score": 0.72
    }
  }
}
```

## Orchestrator Delegation Pattern

```python
# Orchestrator delegates dataset generation
Task(test-dataset-creator, prompt="""
Generate 20 FileGrouper test scenarios from gauntlet-agents git history.

Requirements:
- 20 scenarios covering all 12 Conventional Commit types
- File count distribution: 1-5 (3), 6-10 (8), 11-15 (6), 16-50 (3)
- Edge cases: mixed types, test-only, large repo, low confidence, renamed/deleted, ungrouped, dependencies
- Ground truth: Simulated expert grouping using FileGrouper heuristics

Algorithm heuristics source: docs/01-planning/specifications/004-git-github-agent/filegrouper-heuristics.md

Output:
- tests/fixtures/filegrouper_scenarios.json
- tests/fixtures/filegrouper_ground_truth.json
""")
```

---

**Token Savings**: ~141 lines externalized from agent definition
