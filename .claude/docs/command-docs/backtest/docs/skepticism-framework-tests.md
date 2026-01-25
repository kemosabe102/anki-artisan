# Skepticism-First Framework Integration Tests

Verification tests for the confidence scaling, watchlist routing, capacity testing, and Monte Carlo validation components.

---

## Test Suite Overview

| Category | Tests | Pass Criteria |
|----------|-------|---------------|
| Confidence Scaling | 4 | Position size scales with confidence |
| Watchlist Routing | 3 | Low confidence routes to watchlist |
| Capacity Testing | 3 | Sharpe degradation measured at scale |
| Monte Carlo Validation | 3 | p-value gates enforced |
| SNR Tracking | 3 | Degradation status calculated |

---

## 1. Confidence Scaling Tests

### Test 1.1: Standard Confidence Scaling
**Input**:
- Account equity: $100,000
- Base risk: 1%
- Pattern confidence: 0.75
- Entry price: $50
- Stop price: $48

**Expected**:
```
effective_risk_pct = 0.01 × 0.75 = 0.0075 (0.75%)
risk_dollars = $100,000 × 0.0075 = $750
position_size = $750 / $2 = 375 shares
```

**Pass**: Position size = 375 (not 500 which would be without scaling)

### Test 1.2: Maximum Confidence (0.95)
**Input**: Same as 1.1, but confidence = 0.95
**Expected**: Position size = 475 shares (not 500)
**Pass**: Scaling applied even at maximum confidence

### Test 1.3: Floor Confidence (0.50)
**Input**: Same as 1.1, but confidence = 0.50
**Expected**: Position size = 250 shares (minimum executable)
**Pass**: Floor confidence produces minimum position

### Test 1.4: Regime Multiplier Stacking
**Input**: Same as 1.1, plus regime_multiplier = 0.7 (HIGH volatility)
**Expected**:
```
position_size = 375 × 0.7 = 262 shares
```
**Pass**: Both multipliers applied multiplicatively


---

## 2. Watchlist Routing Tests

### Test 2.1: Below Floor Routing
**Input**:
- Pattern confidence: 0.45
- All other inputs valid

**Expected**:
```json
{
  "status": "WATCHLIST_ROUTED",
  "watchlist_routed": true,
  "position_size": null,
  "message": "Pattern confidence 0.45 below 0.5 floor. Routed to watchlist."
}
```

**Pass**: No position sizing calculated, status = WATCHLIST_ROUTED

### Test 2.2: Exactly At Floor
**Input**: Pattern confidence: 0.50

**Expected**: Position sizing proceeds (NOT routed to watchlist)

**Pass**: 0.50 is executable, not watchlist

### Test 2.3: Watchlist Entry Created
**Input**: Confidence 0.45 pattern detected

**Expected**: Watchlist entry with:
- status: "WATCHING"
- ttl_hours: 72
- pattern_confidence: 0.45

**Pass**: Watchlist schema validated, entry persisted

---

## 3. Capacity Testing Tests

### Test 3.1: Sharpe Degradation Detection
**Input**:
- Baseline capital: $100,000
- Baseline Sharpe: 0.65
- Scale factors: [2, 5, 10]

**Expected** (example):
```json
{
  "scaled_results": [
    {"scale": 2, "sharpe": 0.62, "degradation_pct": 4.6},
    {"scale": 5, "sharpe": 0.55, "degradation_pct": 15.4},
    {"scale": 10, "sharpe": 0.48, "degradation_pct": 26.2}
  ],
  "capacity_score": 73.8
}
```

**Pass**: Sharpe degrades at higher scales, degradation_pct calculated correctly


### Test 3.2: Tier 3 Soft Gate (70%)
**Input**: Capacity score = 68%

**Expected**: Verdict = "WARN" (soft gate, not fail)

**Pass**: Warning issued but validation continues

### Test 3.3: Tier 4 Hard Gate (75%)
**Input**: Capacity score = 72%

**Expected**: Verdict = "FAIL" at Tier 4

**Pass**: Validation fails if below 75% at Tier 4

---

## 4. Monte Carlo Validation Tests

### Test 4.1: Tier 4 Without Monte Carlo
**Input**:
- Tier: 4
- monte_carlo_pvalue: null (not run)

**Expected**:
```json
{
  "verdict": "FAIL",
  "failure_reason": "Monte Carlo validation required at Tier 4"
}
```

**Pass**: Validation fails with clear error message


### Test 4.2: p-value Above Threshold
**Input**:
- Tier: 4
- monte_carlo_pvalue: 0.08

**Expected**:
```json
{
  "verdict": "FAIL",
  "failure_reason": "Monte Carlo p-value 0.08 >= 0.05 threshold"
}
```

**Pass**: Fails due to insufficient statistical significance

### Test 4.3: p-value Below Threshold
**Input**:
- Tier: 4
- monte_carlo_pvalue: 0.03

**Expected**:
```json
{
  "verdict": "PASS",
  "monte_carlo": {
    "passed": true,
    "percentile": 97
  }
}
```

**Pass**: Validation passes with significance


---

## 5. SNR Tracking Tests

### Test 5.1: Degradation Detection
**Input**:
- Pattern: breakout
- SNR history: [1.2, 1.0, 0.9, 0.8, 0.7] (5 periods)

**Expected**:
```json
{
  "degradation_status": "DEGRADING",
  "degradation_signals": ["SNR < 1.0 for 3 consecutive periods"],
  "recommendation": "REDUCE_SIZING"
}
```

**Pass**: Status correctly identifies degradation

### Test 5.2: Critical Status
**Input**: SNR = 0.4 for 3+ periods

**Expected**: degradation_status = "CRITICAL", sizing_multiplier = 0.5

**Pass**: Critical threshold triggers half sizing

### Test 5.3: Sizing Multiplier Applied
**Input**:
- Base confidence: 0.80
- Degradation status: DEGRADING (multiplier 0.75)

**Expected**:
```
effective_confidence = 0.80 × 0.75 = 0.60
effective_risk_pct = 0.01 × 0.60 = 0.006 (0.6%)
```

**Pass**: SNR degradation multiplier stacks with confidence

---

## Test Execution

### Manual Verification
```bash
# Run individual test scenarios via Task delegations
Task(backtester, "MODE: capacity_test, hypothesis_id: TEST-001, ...")
Task(risk-management-specialist, "calculate_position_size, pattern_confidence: 0.75, ...")
```

### Automated Validation
Future: Add pytest fixtures for schema validation and formula verification.

---

## Success Criteria Summary

| Component | Key Test | Must Pass |
|-----------|----------|-----------|
| Confidence Scaling | 0.75 confidence → 0.75% risk | Yes |
| Watchlist Routing | 0.45 confidence → WATCHLIST_ROUTED | Yes |
| Capacity Testing | 10x scale → measurable degradation | Yes |
| Monte Carlo | Tier 4 without p-value → FAIL | Yes |
| SNR Tracking | SNR < 1.0 for 3 periods → DEGRADING | Yes |
