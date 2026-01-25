# Risk Management Specialist Examples

Usage examples showing how the orchestrator delegates to risk-management-specialist.

## Contents

| Example | Description |
|---------|-------------|
| [delegation-examples.md](delegation-examples.md) | Orchestrator delegation patterns |

## Quick Example

```python
Task(risk-management-specialist,
  "Calculate position size for AAPL long entry at $175.00.
   Account equity: $100,000. Risk tolerance: 1%.")
```

## Expected Output Format

```json
{
  "status": "SUCCESS",
  "agent": "risk-management-specialist",
  "position_size": 180,
  "stop_price": 169.45,
  "risk_dollars": 999.00,
  "risk_pct": 0.999,
  "confidence": 0.95,
  "constraint_validation": {
    "buying_power": "PASS",
    "portfolio_heat": "PASS",
    "max_positions": "PASS"
  }
}
```
