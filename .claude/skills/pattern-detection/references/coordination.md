# Multi-Indicator Coordination Reference

Tiered fallback strategy for combining indicator signals based on conflict level.

---

## Tiered Fallback Strategy

```
                   K < 0.3?
                  /        \
               YES          NO
                |            |
        Dempster-Shafer   K < 0.5?
                         /      \
                      YES        NO
                       |          |
              Weighted Voting   Consensus
```

---

## Tier 1: Dempster-Shafer (K < 0.3)

**When**: Low conflict between indicators

**Process**:
1. Assign BPA per indicator (see dempster-shafer.md)
2. Apply Dempster's combination rule
3. Decision = argmax(Belief)
4. Confidence = Belief(decision) * (1 - K)

**Advantages**:
- Mathematically rigorous evidence combination
- Explicit uncertainty quantification
- Handles partial evidence

---

## Tier 2: Weighted Voting (K 0.3-0.5)

**When**: Moderate conflict, need interpretable aggregation

### Weight Assignment

| Method | Description |
|--------|-------------|
| Historical accuracy | w_i = accuracy_i / Sum(accuracy_j) |
| Domain hierarchy | Trend (0.4), Momentum (0.3), Volume (0.2), Volatility (0.1) |

### Voting Process

```python
def weighted_voting(signals, weights):
    """
    signals: List[(direction, confidence)]
        direction: +1 (BUY), -1 (SELL), 0 (HOLD)
    weights: List[float] summing to 1.0
    """
    score = sum(w * dir * conf for (dir, conf), w in zip(signals, weights))
    
    if score > 0.5: return 'BUY', abs(score)
    if score < -0.5: return 'SELL', abs(score)
    return 'HOLD', 0.0
```

### Decision Thresholds

| Score | Decision |
|-------|----------|
| > +0.5 | BUY |
| < -0.5 | SELL |
| -0.5 to +0.5 | HOLD |

---

## Tier 3: Consensus Threshold (K > 0.5)

**When**: High conflict, require agreement before action

### Consensus Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| tau | 0.6-0.7 | Minimum agreement fraction |
| c_min | 0.5 | Minimum average confidence |

### Consensus Process

```python
def consensus_threshold(signals, tau=0.7, c_min=0.5):
    """
    signals: List[(decision, confidence)]
    """
    decisions = [d for d, _ in signals]
    majority = Counter(decisions).most_common(1)[0][0]
    
    agreement = decisions.count(majority) / len(decisions)
    avg_conf = mean([c for d, c in signals if d == majority])
    
    if agreement >= tau and avg_conf >= c_min:
        return majority, avg_conf * agreement
    return 'HOLD', 0.0
```

---

## Framework Selection by Regime

| Regime | Primary Framework | Rationale |
|--------|-------------------|-----------|
| Trending | Weighted Voting | Clear signals, weight trend indicators higher |
| Ranging | Consensus Threshold | Reduce false breakouts, require agreement |
| Volatile | Dempster-Shafer | Explicit uncertainty handling |

---

## Conflict Resolution Strategies

### Hierarchical Priority

**Process**:
1. Rank indicators by domain relevance
2. If top 2 tiers agree -> high confidence (0.85+)
3. If top tier conflicts with lower -> follow top tier, moderate confidence (0.6-0.7)

**Tier Assignment**:

| Regime | Tier 1 | Tier 2 | Tier 3 |
|--------|--------|--------|--------|
| Trending | ADX, EMA_cross, Supertrend | RSI, MACD | Stochastic, CCI |
| Ranging | RSI, Stochastic, BBands | Volume_profile, OBV | ADX, EMA_cross |

### Conflict Penalty

```
Adjusted_Confidence = Base_Confidence * (1 - Conflict_Score / Max_Conflict)
```

If conflict > 0.5 -> force HOLD decision

---

## Missing Data Handling

### Graceful Degradation

1. Exclude missing indicators from voting
2. Renormalize weights: `new_weights = old_weights / sum(available_weights)`
3. Apply coverage penalty: `confidence * sqrt(available / total)`

### Example

```python
def handle_missing(signals, weights):
    valid = [(s, w) for s, w in zip(signals, weights) if s is not None]
    if not valid:
        return 'HOLD', 0.0
    
    signals_valid, weights_valid = zip(*valid)
    weights_norm = [w / sum(weights_valid) for w in weights_valid]
    
    decision, conf = weighted_voting(signals_valid, weights_norm)
    coverage = len(valid) / len(signals)
    return decision, conf * sqrt(coverage)
```

---

## Output Structure

```json
{
  "decision": "BUY",
  "confidence": 0.72,
  "coordination_method": "weighted_voting",
  "K_conflict": 0.35,
  "contributing_indicators": ["ADX", "RSI", "Volume"],
  "fallback_triggered": true,
  "fallback_reason": "K > 0.3"
}
```
