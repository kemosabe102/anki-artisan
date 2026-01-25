# Domain Heuristics Reference

Rules for simulating expert decisions in algorithm-specific test datasets.

---

## Heuristic Hierarchy

Apply heuristics in priority order for ground truth generation:

| Priority | Heuristic | Confidence | Description |
|----------|-----------|------------|-------------|
| 1 | Functional Cohesion | 0.90 | Files implementing same feature |
| 2 | Directory Proximity | 0.75 | Files in same directory |
| 3 | File Type Similarity | 0.65 | Files with same extension |
| 4 | Change Type Alignment | 0.60 | Files sharing commit type |
| 5 | Temporal Coupling | 0.55 | Files frequently changed together |

---

## Decision Algorithm

```python
def simulate_expert_grouping(files, commit_message, git_history):
    groups = []
    
    # Priority 1: Functional cohesion
    feature = extract_feature_from_message(commit_message)
    if feature:
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
                "confidence": 0.65
            })
            files = [f for f in files if f not in type_files]
    
    # Remaining files become singletons
    for file in files:
        groups.append({
            "id": f"SINGLETON_{sanitize(file.path)}",
            "files": [file],
            "heuristic": "ungrouped",
            "confidence": 0.50
        })
    
    return groups
```

---

## Confidence Scoring Rules

### High Confidence (0.85-1.0)
- Feature-based grouping with explicit commit message match
- All files in same directory with clear functional purpose
- Well-documented architectural pattern (models/, controllers/)

### Medium Confidence (0.70-0.84)
- Directory-based grouping with 3+ files
- File type grouping with strong convention (all tests)
- Change type alignment with supporting evidence

### Low Confidence (0.50-0.69)
- File type grouping with 2 files only
- Change type alignment without other evidence
- Fallback heuristics (temporal coupling, name similarity)

### Ambiguous (<0.50)
- Singletons (ungrouped files)
- Conflicting heuristics
- Missing context

---

## Commit Classification Heuristics

When commit type not explicitly specified:

| Type | Indicators |
|------|------------|
| feat | New files added, `lines_added > 100`, keywords: add, implement, introduce |
| fix | Small changes (`files <= 3`, `lines < 50`), keywords: fix, resolve, patch |
| refactor | High churn (`deleted/added > 0.8`), tests unchanged, keywords: refactor, cleanup |
| docs | Only .md files changed, keywords: docs, documentation, readme |
| test | Only test files changed, keywords: test, spec, coverage |
| style | Whitespace only, keywords: style, format, lint |

---

## Quality Thresholds

- Average confidence >= 0.70 across all scenarios
- < 10% scenarios flagged as ambiguous (< 0.50)
- 100% decisions have documented heuristic source
