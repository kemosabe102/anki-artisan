# Effort Estimation Model

*Reference document for wall-clock time estimation in parallel task execution*

**Parent**: [Generating Tasks SKILL](SKILL.md)

---

## Key Insight

Tasks execute in PARALLEL via sub-agents. Estimate wall-clock time, not sequential sum.

---

## Time Constants

| Constant | Value | Rationale |
|----------|-------|-----------|
| BASE_MINUTES | 3 min | Median sub-agent task execution |
| REVIEW_MINUTES | 5 min | Per review checkpoint |
| ORCHESTRATION_BASE | 5 min | Initial context + final synthesis |

---

## Per-Task Complexity Score (1-5 scale)

| Factor | Weight | Score 1 | Score 3 | Score 5 |
|--------|--------|---------|---------|---------|
| LOC Estimate | 0.30 | <20 lines | 50-100 lines | >200 lines |
| Dependencies | 0.25 | 0-1 deps | 2-3 deps | 4+ deps |
| Domain Familiarity | 0.25 | Existing pattern | Similar pattern | New pattern |
| Integration Points | 0.20 | Isolated | 1-2 integrations | 3+ integrations |

**Formula**:
```
task_complexity = (LOC x 0.30) + (deps x 0.25) + (familiarity x 0.25) + (integration x 0.20)
```


---

## Critical Path Calculation

```
parallel_batches = group_by_dependencies(tasks)

FOR each batch in parallel_batches:
  batch_time = max(task.complexity for task in batch) x BASE_MINUTES
  
total_execution_time = sum(batch_time for batch in parallel_batches)
review_overhead = review_groups x REVIEW_MINUTES
orchestration_overhead = ORCHESTRATION_BASE + (task_count x 0.5)

wall_clock_time = total_execution_time + review_overhead + orchestration_overhead
```

---

## Output Format

```json
{
  "effort": {
    "total_tasks": 15,
    "parallel_batches": 4,
    "critical_path_tasks": 6,
    "estimated_wall_clock": "25-35 min",
    "confidence": 0.80,
    "breakdown": {
      "execution": "15-20 min",
      "reviews": "10-15 min", 
      "orchestration": "5 min"
    }
  }
}
```

---

## Anti-Patterns

- Sequential sum estimation ("15 tasks x 30 min = 7.5 hours" - ignores parallelism)
- Single-number estimates without breakdown transparency
- Ignoring review checkpoints in time calculation
- Not accounting for orchestration overhead
