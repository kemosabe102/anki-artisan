# Orchestrator Delegation Examples

## 1. Position Sizing (Standard)

**Request**:
```python
Task(risk-management-specialist,
  "Calculate position size for AAPL long entry at $175.00.
   Account equity: $100,000. Risk tolerance: 1%.")
```

**Response**:
```json
{
  "status": "SUCCESS",
  "position_size": 180,
  "stop_price": 169.45,
  "stop_distance": 5.55,
  "risk_dollars": 999.00,
  "risk_pct": 0.999,
  "atr_value": 1.85,
  "confidence": 0.95,
  "rationale": "ATR-based Chandelier stop at 3.0x multiplier"
}
```

---

## 2. Portfolio Heat Assessment

**Request**:
```python
Task(risk-management-specialist,
  "Assess portfolio heat before adding new position.
   Account equity: $500,000.
   Open positions: 12 positions totaling $32,500 risk.
   New position risk: $5,000.")
```

**Response**:
```json
{
  "status": "SUCCESS",
  "current_heat_pct": 6.5,
  "projected_heat_pct": 7.5,
  "margin_to_limit": 2.5,
  "threshold": 10.0,
  "heat_status": "PASS",
  "confidence": 0.98
}
```

---

## 3. Circuit Breaker State Check

**Request**:
```python
Task(risk-management-specialist,
  "Check circuit breaker state.
   Starting equity: $100,000.
   Current P&L: -$1,800.")
```

**Response**:
```json
{
  "status": "SUCCESS",
  "state": "WARNING",
  "loss_pct": -1.8,
  "position_sizing_multiplier": 0.5,
  "restrictions": [],
  "buffer_to_next_threshold": 0.3,
  "confidence": 1.0
}
```

---

## 4. Position Sizing with Constraint Failure

**Request**:
```python
Task(risk-management-specialist,
  "Calculate position size for NVDA long at $480.
   Account equity: $50,000. Risk: 1%.
   Current portfolio heat: 9.5%.")
```

**Response**:
```json
{
  "status": "FAILURE",
  "constraint_violations": ["portfolio_heat"],
  "current_heat": 9.5,
  "projected_heat": 10.5,
  "limit": 10.0,
  "remediation": "Close 1 position to free 0.5% heat capacity",
  "confidence": 0.95
}
```

---

## 5. ATR Fallback Scenario

**Request**:
```python
Task(risk-management-specialist,
  "Calculate position size for XYZ entry at $25.00.
   Account equity: $100,000. Risk: 1%.")
```

**Response** (ATR unavailable):
```json
{
  "status": "SUCCESS",
  "position_size": 200,
  "stop_price": 24.50,
  "stop_distance": 0.50,
  "risk_dollars": 1000.00,
  "fallback_used": true,
  "fallback_reason": "ATR unavailable after 2 retries",
  "fallback_method": "2% fixed stop",
  "confidence": 0.70,
  "warning": "Using fixed stop - verify with manual analysis"
}
```

---

## 6. Market Regime Classification

**Request**:
```python
Task(risk-management-specialist,
  "Classify market regime for SPY.
   ATR lookback: 22, Trend lookback: 200, Percentile window: 252.")
```

**Response**:
```json
{
  "status": "SUCCESS",
  "regime_classification": {
    "volatility_regime": "NORMAL",
    "atr_percentile": 52.3,
    "trend_filter": "above_200dma",
    "position_multiplier": 1.0,
    "stop_multiplier": 3.0
  },
  "confidence": 0.92,
  "rationale": "ATR at 52nd percentile (NORMAL range 25-75), price above 200DMA indicating bullish regime"
}
```

### Integration with Strategy Builder

When strategy-builder needs regime context for adaptive sizing:

```python
Task(risk-management-specialist,
  "Classify regime for AAPL before applying momentum strategy filters.
   Include position and stop multipliers for sizing adjustment.")
```

Use the returned `position_multiplier` (0.7x-1.2x) and `stop_multiplier` (2.5x-4.0x ATR) to adjust position sizing based on current market conditions.

---

## Common Delegation Patterns

### With Explicit Stop
```python
Task(risk-management-specialist,
  "Calculate position size.
   Entry: $50.00, Stop: $47.50, Account: $100,000, Risk: 1%")
```

### With ATR Delegation
```python
Task(risk-management-specialist,
  "Calculate position size with ATR-based stop.
   Symbol: AAPL, Entry: $175.00, Account: $100,000")
```

### Heat Check Before Entry
```python
Task(risk-management-specialist,
  "Can I add a $1,000 risk position?
   Current heat: 8.5%, Limit: 10%")
```
