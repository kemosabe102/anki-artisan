# Delegation Examples

## Overview

Examples of how orchestrators delegate to crisis-stress-tester and how crisis-stress-tester delegates to other agents.

---

## Inbound Delegation (Orchestrator to Crisis-Stress-Tester)

### Example 1: Full Crisis Suite (P10 Workflow)

**Context**: algo-strategy command at P10 phase needs crisis validation.

```json
Task(crisis-stress-tester): {
  "hypothesis_id": "HYP-001-momentum-reversion",
  "mode": "full_crisis_suite",
  "strategy_spec": {
    "name": "momentum-reversion",
    "universe": "SP500",
    "entry_rules": [...],
    "exit_rules": [...],
    "position_sizing": "risk_parity"
  },
  "backtest_passed": true,
  "backtest_results": {
    "sharpe": 0.85,
    "max_dd": -22,
    "trade_count": 156
  },
  "request": "Execute full crisis stress test for deployment validation"
}
```

**Expected Response**:
```json
{
  "status": "SUCCESS",
  "hypothesis_id": "HYP-001-momentum-reversion",
  "overall_status": "CRISIS_PROOF",
  "overall_score": 72,
  
  "crisis_results": {
    "gfc_2008": {
      "max_dd": -35,
      "benchmark_dd": -57,
      "dd_ratio": 0.61,
      "recovery_days": 180,
      "period_sharpe": -0.15,
      "gate_status": "PASS"
    },
    "covid_2020": {
      "max_dd": -28,
      "benchmark_dd": -34,
      "dd_ratio": 0.82,
      "recovery_days": 45,
      "period_sharpe": 0.12,
      "gate_status": "PASS"
    },
    "rate_hike_2022": {
      "max_dd": -22,
      "benchmark_dd": -27,
      "dd_ratio": 0.81,
      "recovery_days": 120,
      "period_sharpe": 0.08,
      "gate_status": "PASS"
    }
  },
  
  "tail_metrics": {
    "var_95": -5.2,
    "var_99": -8.1,
    "cvar_99": -10.5,
    "max_consecutive_losses": 12
  },
  
  "verdict": "CRISIS_PROOF",
  "verdict_reasons": ["All hard gates passed", "Score 72 >= 70 threshold"],
  "next_action": "deploy",
  "recommendations": []
}
```

### Example 2: Failed Crisis Test

**Context**: Strategy fails 2008 crisis gate.

```json
Task(crisis-stress-tester): {
  "hypothesis_id": "HYP-002-leveraged-tech",
  "mode": "full_crisis_suite",
  "strategy_spec": {
    "name": "leveraged-tech",
    "leverage": 2.0,
    "universe": "QQQ_constituents"
  },
  "backtest_passed": true,
  "request": "Execute crisis stress test"
}
```

**Expected Response (FRAGILE)**:
```json
{
  "status": "SUCCESS",
  "hypothesis_id": "HYP-002-leveraged-tech",
  "overall_status": "FRAGILE",
  "overall_score": 28,
  
  "crisis_results": {
    "gfc_2008": {
      "max_dd": -78,
      "benchmark_dd": -57,
      "dd_ratio": 1.37,
      "recovery_days": 890,
      "period_sharpe": -0.85,
      "gate_status": "FAIL",
      "gate_reason": "DD -78% exceeds 2x benchmark (-114%)"
    },
    "covid_2020": {
      "max_dd": -52,
      "benchmark_dd": -34,
      "dd_ratio": 1.53,
      "recovery_days": 95,
      "period_sharpe": -0.42,
      "gate_status": "FAIL",
      "gate_reason": "DD -52% exceeds 50% threshold"
    },
    "rate_hike_2022": {
      "max_dd": -45,
      "benchmark_dd": -27,
      "dd_ratio": 1.67,
      "recovery_days": null,
      "period_sharpe": -0.38,
      "gate_status": "FAIL",
      "gate_reason": "DD -45% exceeds 30% AND Sharpe < 0"
    }
  },
  
  "verdict": "FRAGILE",
  "verdict_reasons": [
    "HARD FAIL: GFC 2008 - DD -78% exceeds 2x benchmark",
    "HARD FAIL: COVID 2020 - DD -52% exceeds 50%",
    "HARD FAIL: Rate Hike 2022 - Both conditions failed"
  ],
  "next_action": "reject",
  "recommendations": [
    "Reduce leverage from 2.0x to 1.0x",
    "Add volatility-based position sizing",
    "Consider hedging during high VIX periods",
    "Diversify beyond tech-heavy universe"
  ]
}
```

---

## Outbound Delegation (Crisis-Stress-Tester to Other Agents)

### To Backtester

```json
Task(backtester): {
  "hypothesis_id": "HYP-001",
  "mode": "single_run",
  "backtest_params": {
    "start_date": "2008-09-01",
    "end_date": "2009-03-31",
    "initial_capital": 100000
  },
  "strategy_spec": { ... },
  "request": "Execute GFC 2008 crisis period backtest"
}
```

### To Risk Management Specialist

```json
Task(risk-management-specialist): {
  "mode": "tail_analysis",
  "returns_data": [-0.02, -0.015, 0.01, -0.05, ...],
  "confidence_levels": [0.95, 0.99],
  "request": "Calculate VaR and CVaR for crisis period returns"
}
```

---

## Workflow Integration Example

### P10 Phase in algo-strategy --full

```
P9: backtester (normal market backtest) -> PASS
    |
    v
P10: crisis-stress-tester (crisis validation)
    |
    +-> GFC 2008 test -> Task(backtester, crisis_dates)
    +-> COVID 2020 test -> Task(backtester, crisis_dates)
    +-> Rate Hike 2022 test -> Task(backtester, crisis_dates)
    +-> Tail metrics -> Task(risk-management-specialist)
    |
    v
    Verdict: CRISIS_PROOF / VULNERABLE / FRAGILE
    |
    v
P11: (next phase if CRISIS_PROOF)
```
