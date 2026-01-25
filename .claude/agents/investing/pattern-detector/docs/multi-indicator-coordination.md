# Multi-Indicator Coordination Frameworks

## Overview

Systematic frameworks for combining multiple indicator signals into unified decisions using evidence theory, weighted voting, and consensus thresholds with confidence scoring.

## Core Frameworks

### 1. Dempster-Shafer Evidence Theory

**Purpose**: Combine evidence from multiple sources with explicit uncertainty representation

**When to Use**: High-stakes decisions, conflicting indicators, explicit confidence quantification required

**How to Apply**:

1. **Define Hypothesis Space**:
   - Θ = {BUY, SELL, HOLD}
   - Power set: 2^Θ (all possible combinations)

2. **Assign Basic Probability Assignments (BPA)**:
   - Each indicator provides BPA: m(A) for each subset A ⊆ Θ
   - Constraint: Σ m(A) = 1.0
   - Example: RSI oversold → m({BUY}) = 0.6, m({BUY, HOLD}) = 0.3, m(Θ) = 0.1

3. **Dempster's Combination Rule**:

   ```
   m₁₂(A) = [Σ m₁(B) × m₂(C)] / [1 - K]
            where B ∩ C = A

   K = Σ m₁(B) × m₂(C)  (conflict measure)
       where B ∩ C = ∅
   ```

4. **Decision Rule**:
   - Belief(BUY) = Σ m(A) for all A ⊆ {BUY}
   - Plausibility(BUY) = Σ m(A) for all A ∩ {BUY} ≠ ∅
   - Decide: argmax Belief(hypothesis)

**Example**:

```python
from pyds import MassFunction

def dempster_shafer_combine(indicator_signals):
    """
    indicator_signals: List[dict] where each dict is {hypothesis: mass}
    Example: [{'BUY': 0.6, 'HOLD': 0.3, 'BUY|HOLD|SELL': 0.1}, ...]
    """
    combined = MassFunction()

    for signal in indicator_signals:
        mf = MassFunction(signal)
        combined = combined & mf  # Dempster's rule

    # Extract belief for each hypothesis
    beliefs = {
        'BUY': combined.bel({'BUY'}),
        'SELL': combined.bel({'SELL'}),
        'HOLD': combined.bel({'HOLD'})
    }

    decision = max(beliefs, key=beliefs.get)
    confidence = beliefs[decision]

    return decision, confidence, combined.conflict()
```

**Confidence Scoring**:

- Confidence = Belief(decision) × (1 - K)
  - K (conflict) penalizes contradictory evidence
  - Low conflict (K < 0.2) → confidence near Belief value
  - High conflict (K > 0.5) → confidence heavily discounted

---

### 2. Weighted Voting Framework

**Purpose**: Simple, interpretable aggregation with explicit indicator importance weights

**When to Use**: Clear indicator hierarchy, performance-based weighting, fast computation required

**How to Apply**:

1. **Assign Indicator Weights**:
   - Based on historical accuracy: w_i = accuracy_i / Σ accuracy_j
   - Domain expertise: Trend indicators (0.4), Momentum (0.3), Volume (0.2), Volatility (0.1)
   - Constraint: Σ w_i = 1.0

2. **Collect Indicator Votes**:
   - Each indicator votes: {BUY: +1, SELL: -1, HOLD: 0}
   - Attach confidence: vote_i = direction × confidence_i

3. **Weighted Sum**:

   ```
   Score = Σ (w_i × vote_i × confidence_i)
   ```

4. **Decision Thresholds**:
   - BUY: Score > +0.5
   - SELL: Score < -0.5
   - HOLD: -0.5 ≤ Score ≤ +0.5

**Example**:

```python
def weighted_voting(indicator_signals, weights):
    """
    indicator_signals: List[tuple] = [(direction, confidence), ...]
        direction: +1 (BUY), -1 (SELL), 0 (HOLD)
        confidence: 0.0-1.0
    weights: List[float] matching indicator_signals length
    """
    assert len(indicator_signals) == len(weights)
    assert abs(sum(weights) - 1.0) < 1e-6, "Weights must sum to 1.0"

    weighted_score = sum(
        w * direction * confidence
        for (direction, confidence), w in zip(indicator_signals, weights)
    )

    if weighted_score > 0.5:
        decision = 'BUY'
    elif weighted_score < -0.5:
        decision = 'SELL'
    else:
        decision = 'HOLD'

    # Confidence is absolute weighted score normalized to [0,1]
    confidence = min(1.0, abs(weighted_score))

    return decision, confidence, weighted_score
```

**Confidence Scoring**:

- Confidence = |weighted_score| / max_possible_score
- max_possible_score = Σ w_i (if all indicators vote same direction with confidence=1.0)
- Adjust for agreement: confidence × (fraction_agreeing)^0.5

---

### 3. Consensus Threshold Framework

**Purpose**: Require minimum agreement across indicators before action

**When to Use**: Risk-averse strategies, false positive reduction, high-conviction signals only

**How to Apply**:

1. **Define Consensus Threshold**:
   - Minimum fraction of indicators agreeing: τ (default 0.6-0.7)
   - Minimum average confidence: c_min (default 0.5)

2. **Collect Indicator Decisions**:
   - Each indicator: (decision, confidence)
   - Group by decision type

3. **Calculate Consensus Metrics**:

   ```
   Agreement_Fraction = count(decision_i == majority_decision) / total_indicators
   Avg_Confidence = mean(confidence_i for decision_i == majority_decision)
   ```

4. **Decision Rule**:

   ```
   IF Agreement_Fraction ≥ τ AND Avg_Confidence ≥ c_min:
       RETURN majority_decision
   ELSE:
       RETURN HOLD (no consensus)
   ```

**Example**:

```python
from collections import Counter

def consensus_threshold(indicator_signals, agreement_threshold=0.7, confidence_threshold=0.5):
    """
    indicator_signals: List[tuple] = [(decision, confidence), ...]
        decision: 'BUY', 'SELL', 'HOLD'
        confidence: 0.0-1.0
    """
    decisions = [dec for dec, _ in indicator_signals]
    confidences = [conf for _, conf in indicator_signals]

    # Find majority decision
    decision_counts = Counter(decisions)
    majority_decision, majority_count = decision_counts.most_common(1)

    agreement_fraction = majority_count / len(decisions)

    # Calculate average confidence for majority voters
    majority_confidences = [
        conf for dec, conf in indicator_signals if dec == majority_decision
    ]
    avg_confidence = sum(majority_confidences) / len(majority_confidences)

    # Apply thresholds
    if agreement_fraction >= agreement_threshold and avg_confidence >= confidence_threshold:
        return majority_decision, avg_confidence
    else:
        return 'HOLD', 0.0  # No consensus
```

**Confidence Scoring**:

- Confidence = avg_confidence × agreement_fraction
- Penalty for near-threshold: If agreement within 0.1 of threshold, multiply by 0.8

---

## Signal Conflict Resolution

### Hierarchical Priority Strategy

**When to Use**: Established indicator reliability hierarchy, trending vs ranging regimes

**Process**:

1. Rank indicators by domain relevance:
   - Trending regime: Trend indicators (ADX, MA) > Momentum (RSI) > Oscillators (Stochastic)
   - Ranging regime: Oscillators > Volume > Trend indicators

2. If top 2 tiers agree → high confidence (0.85+)
3. If top tier conflicts with lower → follow top tier, moderate confidence (0.6-0.7)
4. If same tier conflicts → apply weighted voting among conflicting tier

**Example**:

```python
def hierarchical_priority(indicator_signals, regime='trending'):
    """
    indicator_signals: Dict[str, tuple] = {indicator_name: (decision, confidence)}
    regime: 'trending' or 'ranging'
    """
    # Define hierarchy
    if regime == 'trending':
        tier1 = ['adx', 'ema_cross', 'supertrend']
        tier2 = ['rsi', 'macd']
        tier3 = ['stochastic', 'cci']
    else:  # ranging
        tier1 = ['rsi', 'stochastic', 'bbands']
        tier2 = ['volume_profile', 'obv']
        tier3 = ['adx', 'ema_cross']

    def get_tier_consensus(tier_indicators):
        tier_signals = [indicator_signals[ind] for ind in tier_indicators if ind in indicator_signals]
        if not tier_signals:
            return None, 0.0
        decisions = [dec for dec, _ in tier_signals]
        majority = Counter(decisions).most_common(1)
        agreement = decisions.count(majority) / len(decisions)
        avg_conf = sum(conf for dec, conf in tier_signals if dec == majority) / decisions.count(majority)
        return majority, avg_conf * agreement

    # Try tier 1 first
    tier1_decision, tier1_conf = get_tier_consensus(tier1)
    if tier1_conf > 0.6:
        return tier1_decision, tier1_conf

    # Fallback to tier 2
    tier2_decision, tier2_conf = get_tier_consensus(tier2)
    if tier2_conf > 0.5:
        return tier2_decision, tier2_conf * 0.85  # Discount for lower tier

    # Last resort: tier 3 or HOLD
    tier3_decision, tier3_conf = get_tier_consensus(tier3)
    return tier3_decision if tier3_conf > 0.4 else 'HOLD', tier3_conf * 0.7
```

---

### Conflict Penalty Approach

**When to Use**: No clear hierarchy, equal weighting desired, explicit conflict measurement

**Process**:

1. Calculate pairwise conflicts:

   ```
   Conflict_Score = Σ (|vote_i - vote_j| × w_i × w_j) for all pairs (i,j)
   ```

   - vote_i ∈ {-1, 0, +1} for SELL, HOLD, BUY

2. Penalize final confidence:

   ```
   Adjusted_Confidence = Base_Confidence × (1 - Conflict_Score / Max_Conflict)
   ```

3. If conflict > 0.5 → force HOLD decision

**Example**:

```python
def conflict_penalty(indicator_signals, weights):
    """
    indicator_signals: List[tuple] = [(direction, confidence), ...]
        direction: +1 (BUY), -1 (SELL), 0 (HOLD)
    weights: List[float]
    """
    n = len(indicator_signals)
    conflict_score = 0.0

    # Calculate pairwise conflicts
    for i in range(n):
        for j in range(i + 1, n):
            vote_i, _ = indicator_signals[i]
            vote_j, _ = indicator_signals[j]
            conflict_score += abs(vote_i - vote_j) * weights[i] * weights[j]

    # Max possible conflict (all indicators maximally disagree)
    max_conflict = sum(weights[i] * weights[j] for i in range(n) for j in range(i+1, n)) * 2  # max |vote_i - vote_j| = 2

    # Get base decision via weighted voting
    base_decision, base_confidence, _ = weighted_voting(indicator_signals, weights)

    # Apply penalty
    conflict_penalty = conflict_score / max_conflict
    adjusted_confidence = base_confidence * (1 - conflict_penalty)

    # Force HOLD if high conflict
    if conflict_penalty > 0.5:
        return 'HOLD', adjusted_confidence * 0.5

    return base_decision, adjusted_confidence
```

---

### Time-Weighted Consensus

**When to Use**: Fast-moving markets, recent signals more reliable, indicator lag differences

**Process**:

1. Assign time-decay weights:

   ```
   w_time(t) = e^(-λ × Δt)
   ```

   - Δt = bars since signal generated
   - λ = decay rate (default 0.1 for 10-bar half-life)

2. Combine with indicator weights:

   ```
   w_total = w_indicator × w_time
   ```

3. Apply weighted voting with time-adjusted weights

**Example**:

```python
import numpy as np

def time_weighted_consensus(indicator_signals, indicator_weights, signal_ages, decay_rate=0.1):
    """
    indicator_signals: List[tuple] = [(direction, confidence), ...]
    indicator_weights: List[float]
    signal_ages: List[int] = bars since signal generated
    decay_rate: lambda for exponential decay
    """
    # Calculate time weights
    time_weights = np.exp(-decay_rate * np.array(signal_ages))

    # Combine weights
    total_weights = np.array(indicator_weights) * time_weights
    total_weights /= total_weights.sum()  # Renormalize

    # Apply weighted voting
    return weighted_voting(indicator_signals, total_weights.tolist())
```

---

## Edge Case Handling

### Missing Data Strategy

**Problem**: Indicator cannot compute (insufficient history, data gap)

**Solutions**:

1. **Graceful Degradation**:
   - Exclude missing indicators from voting
   - Renormalize weights among available indicators
   - Flag reduced confidence: `confidence × sqrt(available_indicators / total_indicators)`

2. **Imputation** (use cautiously):
   - Forward-fill for short gaps (< 3 bars)
   - Mean/median for longer gaps with confidence penalty (0.7x)
   - Never impute for volatility/volume indicators

**Example**:

```python
def handle_missing_indicators(indicator_signals, weights):
    """Remove None values and renormalize weights"""
    valid_signals = [(sig, w) for sig, w in zip(indicator_signals, weights) if sig is not None]

    if not valid_signals:
        return 'HOLD', 0.0

    valid_signals_list, valid_weights = zip(*valid_signals)
    valid_weights = np.array(valid_weights)
    valid_weights /= valid_weights.sum()

    decision, confidence, _ = weighted_voting(valid_signals_list, valid_weights.tolist())

    # Penalize for missing data
    availability_ratio = len(valid_signals) / len(indicator_signals)
    adjusted_confidence = confidence * np.sqrt(availability_ratio)

    return decision, adjusted_confidence
```

---

### Outlier Detection

**Problem**: Single indicator produces extreme value (data error, flash crash)

**Solutions**:

1. **Z-Score Filtering**:
   - Calculate z-score for each indicator's confidence vs historical distribution
   - If |z| > 3.0 → flag as outlier, reduce weight by 0.5x

2. **MAD (Median Absolute Deviation)**:
   - More robust to outliers than standard deviation
   - Threshold: |x - median| / MAD > 3.5

**Example**:

```python
def detect_outliers(indicator_confidences, historical_confidences, method='zscore'):
    """
    indicator_confidences: List[float] - current confidence values
    historical_confidences: List[List[float]] - historical values per indicator
    """
    outlier_flags = []

    for i, current_conf in enumerate(indicator_confidences):
        historical = historical_confidences[i]

        if method == 'zscore':
            mean = np.mean(historical)
            std = np.std(historical)
            z_score = abs(current_conf - mean) / (std + 1e-9)
            is_outlier = z_score > 3.0

        elif method == 'mad':
            median = np.median(historical)
            mad = np.median(np.abs(historical - median))
            score = abs(current_conf - median) / (mad + 1e-9)
            is_outlier = score > 3.5

        outlier_flags.append(is_outlier)

    return outlier_flags
```

---

### Regime Change Detection

**Problem**: Coordination framework optimized for one regime fails in another

**Solutions**:

1. **Regime Classification**:
   - Trending: ADX > 25
   - Ranging: ADX < 20, Bollinger Band width < 20th percentile
   - Volatile: ATR > 80th percentile

2. **Adaptive Weighting**:
   - Switch weight profiles based on regime
   - Use hierarchical priority strategy with regime-specific tiers

3. **Framework Selection**:
   - Trending → Weighted Voting (clear signals)
   - Ranging → Consensus Threshold (reduce false breakouts)
   - Volatile → Dempster-Shafer (explicit uncertainty)

**Example**:

```python
def regime_adaptive_coordination(indicator_signals, weights, adx, atr_percentile, bb_width_percentile):
    """Select coordination framework based on market regime"""

    # Classify regime
    if adx > 25:
        regime = 'trending'
        framework = 'weighted_voting'
    elif adx < 20 and bb_width_percentile < 20:
        regime = 'ranging'
        framework = 'consensus_threshold'
    elif atr_percentile > 80:
        regime = 'volatile'
        framework = 'dempster_shafer'
    else:
        regime = 'transitional'
        framework = 'weighted_voting'  # Default

    # Apply selected framework
    if framework == 'weighted_voting':
        return weighted_voting(indicator_signals, weights)
    elif framework == 'consensus_threshold':
        return consensus_threshold(indicator_signals)
    elif framework == 'dempster_shafer':
        return dempster_shafer_combine(indicator_signals)
```

---

## Anti-Patterns

### 1. Equal Weighting Assumption

**Problem**: Treating all indicators equally ignores performance differences
**Alternative**: Use historical accuracy to derive weights, or domain hierarchy (trend > momentum > oscillators)

### 2. Ignoring Indicator Lag

**Problem**: Slow indicators (long-period MA) conflict with fast indicators (RSI) due to time lag
**Alternative**: Apply time-weighted consensus, or separate fast/slow indicator groups

### 3. Over-Reliance on Consensus

**Problem**: Requiring 100% agreement misses valid minority signals
**Alternative**: Use 60-70% threshold, allow high-confidence minority overrides in hierarchical priority

### 4. Static Regime Assumptions

**Problem**: Using trending-optimized weights in ranging markets
**Alternative**: Regime detection with adaptive framework selection

### 5. Ignoring Conflict Metrics

**Problem**: High confidence despite indicator disagreement
**Alternative**: Calculate conflict explicitly (Dempster K, pairwise conflict score), penalize confidence

---

## Integration Points

### Pattern Detection Framework

- Receives multi-pattern signals (breakout, pullback, divergence)
- Coordinates pattern confidence scores into unified decision
- See: `domain-knowledge-pattern-detection.md`

### TA-Lib Integration

- Indicator outputs feed coordination frameworks
- Handles missing indicator gracefully (see Missing Data Strategy)
- See: `development-talib-integration.md`

### Fact Object Output

- Coordination decision → Fact.category ('BUY', 'SELL', 'HOLD')
- Final confidence → Fact.confidence
- Framework metadata → Fact.metadata (conflict score, regime, contributing indicators)

### Error Recovery

- Validation checkpoints before/after coordination
- Partial results if subset of indicators fail
- See: `development-error-recovery.md`

---

## Sources

1. **Shafer, Glenn** (1976). _A Mathematical Theory of Evidence_. Princeton University Press. ISBN: 978-0691100425
   - Dempster-Shafer theory, belief functions, evidence combination

2. **Sentz, Kari & Ferson, Scott** (2002). "Combination of Evidence in Dempster-Shafer Theory". SAND 2002-0835, Sandia National Laboratories.
   - Practical implementation, conflict handling

3. **Kuncheva, Ludmila I.** (2004). _Combining Pattern Classifiers: Methods and Algorithms_. Wiley. ISBN: 978-0471210788
   - Weighted voting, consensus methods, ensemble learning

4. **Dietterich, Thomas G.** (2000). "Ensemble Methods in Machine Learning". _Multiple Classifier Systems_, LNCS 1857, 1-15.
   - Framework comparison, error correlation

5. **Murphy, John J.** (1999). _Technical Analysis of the Financial Markets_. New York Institute of Finance. ISBN: 978-0735200661
   - Multi-indicator strategies, confirmation techniques

6. **Aronson, David R.** (2006). _Evidence-Based Technical Analysis_. Wiley. ISBN: 978-0470008744
   - Statistical validation, indicator weighting, regime analysis

7. **pyds Library Documentation** (2024). <https://github.com/reineking/pyds>
   - Dempster-Shafer implementation in Python

---

**Version**: 1.0
**Last Updated**: 2025-11-16
**Agent**: pattern-detector
