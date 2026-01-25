# Dempster-Shafer Evidence Theory Reference

Framework for combining evidence from multiple indicator sources with explicit uncertainty quantification.

---

## When to Use

- High-stakes decisions requiring explicit confidence
- Conflicting indicators
- Need to quantify uncertainty vs ignorance

---

## Core Concepts

### Hypothesis Space
```
Theta = {BUY, SELL, HOLD}
Power set: 2^Theta (all possible combinations)
```

### Basic Probability Assignment (BPA)

Each indicator provides a mass function m(A) for each subset A of Theta.

**Constraints**:
- m({}) = 0 (empty set has zero mass)
- Sum of all m(A) = 1.0

**Example: RSI Oversold**
```
m({BUY}) = 0.6        # Strong evidence for BUY
m({BUY, HOLD}) = 0.3  # Partial evidence (could be BUY or HOLD)
m(Theta) = 0.1        # Remaining uncertainty
```

### BPA Assignment Guidelines

| Indicator State | BPA Assignment |
|-----------------|----------------|
| RSI < 30 (oversold) | m({BUY}) = 0.6, m({BUY,HOLD}) = 0.3, m(Theta) = 0.1 |
| RSI > 70 (overbought) | m({SELL}) = 0.6, m({SELL,HOLD}) = 0.3, m(Theta) = 0.1 |
| ADX > 25 + uptrend | m({BUY}) = 0.5, m({BUY,HOLD}) = 0.3, m(Theta) = 0.2 |
| ADX > 25 + downtrend | m({SELL}) = 0.5, m({SELL,HOLD}) = 0.3, m(Theta) = 0.2 |
| Volume spike + breakout | m({BUY}) = 0.4, m(Theta) = 0.6 |

---

## Dempster's Combination Rule

Combines two mass functions m1 and m2:

```
m12(A) = [Sum m1(B) * m2(C)] / [1 - K]
         where B AND C = A

K = Sum m1(B) * m2(C)
    where B AND C = {} (conflict measure)
```

### K-Conflict Metric

| K Value | Interpretation | Action |
|---------|----------------|--------|
| K < 0.2 | Low conflict | DS combination reliable |
| 0.2-0.3 | Moderate conflict | DS combination acceptable |
| 0.3-0.5 | High conflict | Consider fallback to Weighted Voting |
| K > 0.5 | Very high conflict | Use Consensus method |

### Combination Example

**Indicator 1 (RSI oversold)**:
- m1({BUY}) = 0.6, m1({BUY,HOLD}) = 0.3, m1(Theta) = 0.1

**Indicator 2 (ADX uptrend)**:
- m2({BUY}) = 0.5, m2({BUY,HOLD}) = 0.3, m2(Theta) = 0.2

**Combination**:
```
Conflict K = m1({BUY}) * 0 + ... (calculate all empty intersections)

m12({BUY}) = [m1({BUY})*m2({BUY}) + m1({BUY})*m2({BUY,HOLD}) + ...] / (1-K)
```

---

## Belief and Plausibility

### Belief (Lower Bound)
```
Bel(A) = Sum m(B) for all B subset of A
```
- Minimum support for hypothesis

### Plausibility (Upper Bound)
```
Pl(A) = Sum m(B) for all B intersecting A
```
- Maximum possible support

### Decision Rule
```
Decision = argmax Belief(hypothesis)
Confidence = Belief(decision) * (1 - K)
```

---

## Python Implementation

```python
from pyds import MassFunction

def dempster_shafer_combine(indicator_bpas):
    """
    indicator_bpas: List[dict] - BPA for each indicator
    Returns: (decision, confidence, K_conflict)
    """
    combined = MassFunction()
    
    for bpa in indicator_bpas:
        mf = MassFunction(bpa)
        combined = combined & mf  # Dempster's rule
    
    beliefs = {
        'BUY': combined.bel({'BUY'}),
        'SELL': combined.bel({'SELL'}),
        'HOLD': combined.bel({'HOLD'})
    }
    
    decision = max(beliefs, key=beliefs.get)
    K = combined.conflict()
    confidence = beliefs[decision] * (1 - K)
    
    return decision, confidence, K
```

---

## Anti-Patterns

| Anti-Pattern | Why Wrong | Correct Approach |
|--------------|-----------|------------------|
| Ignoring K > 0.5 | False confidence from conflicting evidence | Fall back to Consensus |
| Equal BPA for all indicators | Loses domain knowledge | Weight by indicator reliability |
| Using DS for >5 indicators | Computational complexity, diminishing returns | Use Weighted Voting |
