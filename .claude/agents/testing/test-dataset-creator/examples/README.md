# examples/ Directory

**Purpose**: Concrete usage patterns showing how this agent is called and what it produces

---

## Contents

| File | Purpose | Audience |
|------|---------|----------|
| `filegrouper-example.md` | Complete worked example with SUCCESS/FAILURE outputs | Orchestrator, developers |
| `delegation-examples.md` | How orchestrator delegates dataset generation | Orchestrator |

---

## Quick Delegation Template

```python
Task(test-dataset-creator, prompt="""
Generate [N] [algorithm-name] test scenarios from [repository] git history.

Requirements:
- Diversity targets: change types, file counts (see diversity-sampling.md)
- Edge cases: 7/7 required (see edge-cases.md)
- Ground truth: Simulated expert decisions using [algorithm] heuristics

Algorithm heuristics source: [path/to/specs]
Output: [dataset-file-paths]
""")
```

---

## Expected Outputs

**SUCCESS**: Dataset files + diversity metrics + quality grade (A-F)

**FAILURE**: Partial results + specific gaps + recovery suggestions
