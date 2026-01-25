# docs/ Directory

**Purpose**: Externalized domain knowledge for test dataset generation

---

## Contents

| File | Purpose | When to Consult |
|------|---------|-----------------|
| `diversity-sampling.md` | Quantitative targets and scoring methodology | ALL dataset generation (mandatory) |
| `domain-heuristics.md` | Rules for simulating expert decisions | Ground truth generation |
| `edge-cases.md` | 7 required edge case definitions | Planning edge case coverage |
| `workflow-details.md` | Phase-by-phase execution guide | Complex dataset generation |
| `validation-schemas.md` | Pydantic model definitions | JSON file creation |

---

## Quick Reference

**Diversity Score Formula**:
```
diversity_score = (change_type_entropy * 0.4) + (file_count_distribution * 0.3) + (edge_case_coverage * 0.3)
```

**Required Edge Cases** (7/7):
1. mixed_change_types
2. test_only_changes
3. large_repository_50_files
4. low_confidence_ambiguous
5. renamed_deleted_files
6. ungrouped_files
7. dependency_ordering

**Heuristic Priority Order**:
1. Functional cohesion (0.90 confidence)
2. Directory proximity (0.75 confidence)
3. File type similarity (0.65 confidence)
4. Change type alignment (0.60 confidence)
5. Ungrouped/singleton (0.50 confidence)
