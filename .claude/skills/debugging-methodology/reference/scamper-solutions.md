# SCAMPER Solution Generation

## Purpose

Generate multiple fix candidates using creative problem-solving framework.

---

## The 7 SCAMPER Techniques

| Letter | Technique | Question |
|--------|-----------|----------|
| **S** | Substitute | What can be replaced? |
| **C** | Combine | What can be merged? |
| **A** | Adapt | What can be borrowed from elsewhere? |
| **M** | Modify | What can be changed (bigger/smaller/different)? |
| **P** | Put to other use | Can this serve a different purpose? |
| **E** | Eliminate | What can be removed? |
| **R** | Reverse/Rearrange | What if we did the opposite? |

---

## Application to Debugging

For each root cause, apply relevant SCAMPER techniques:

### Substitute
- Replace problematic library with alternative
- Use different algorithm
- Swap data structure

### Combine
- Merge related operations to reduce state
- Combine validation steps
- Unify error handling

### Adapt
- Apply pattern from similar solved problem
- Borrow solution from another module
- Use established library for common issue

### Modify
- Adjust timing/threshold
- Change scope of operation
- Alter data format

### Put to Other Use
- Repurpose existing utility
- Use test infrastructure in production
- Apply monitoring data for diagnosis

### Eliminate
- Remove unnecessary complexity
- Delete dead code path
- Simplify configuration

### Reverse
- Process in opposite order
- Pull instead of push
- Fail-open instead of fail-closed

---

## Solution Ranking

After generating candidates, rank by:

| Criterion | Weight | Question |
|-----------|--------|----------|
| Minimality | 40% | Is this the smallest possible change? |
| Risk | 35% | What could go wrong? |
| Maintainability | 25% | Will future developers understand this? |

---

## Output Format

```json
{
  "candidates": [
    {
      "approach": "Substitute datetime.now() with datetime.utcnow()",
      "technique": "Substitute",
      "minimality": 0.9,
      "risk": 0.1,
      "maintainability": 0.9,
      "score": 0.85
    },
    {
      "approach": "Add timezone conversion layer",
      "technique": "Adapt",
      "minimality": 0.5,
      "risk": 0.3,
      "maintainability": 0.7,
      "score": 0.52
    }
  ],
  "recommended": "Substitute datetime.now() with datetime.utcnow()"
}
```
