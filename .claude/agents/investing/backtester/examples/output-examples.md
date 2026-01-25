# Backtester Output Examples

> **Reference examples for backtester output formats across all modes.**

---

## Backtest Result Schema {#backtest-result}

Standard output structure for single_run and validation modes.

```json
{
  "status": "SUCCESS|FAILURE",
  "hypothesis_id": "HYP-001",
  "trial_number": 3,
  "trials_on_dataset": 12,
  
  "metrics": {
    "sharpe_raw": 0.85,
    "sharpe_deflated": 0.72,
    "deflation_factor": 0.85,
    "trade_count": 156,
    "max_drawdown": 0.18,
    "win_rate": 0.54,
    "profit_factor": 1.42,
    "oos_is_ratio": 0.65
  },
  
  "regime_context": {
    "detected_regime": "ELEVATED",
    "regime_factors": {
      "volatility": 0.65,
      "correlation": 0.45,
      "credit": 0.30,
      "sentiment": 0.55,
      "trend": "BELOW"
    },
    "threshold_adjustment": {
      "sharpe_multiplier": 0.83,
      "drawdown_multiplier": 1.20,
      "trade_count_multiplier": 0.80
    },
    "classification_confidence": 0.78
  },
  
  "validation_gates": {
    "trade_count": {"passed": true, "value": 156, "threshold": 100},
    "sharpe_raw": {"passed": true, "value": 0.85, "threshold": 0.5},
    "sharpe_deflated": {"passed": true, "value": 0.72, "threshold": 0.3},
    "max_drawdown": {"passed": true, "value": 0.18, "threshold": 0.25},
    "oos_is_ratio": {"passed": true, "value": 0.65, "threshold": 0.5}
  },
  
  "verdict": "DEPLOYABLE|NOT_DEPLOYABLE|NEEDS_REVIEW",
  "verdict_reasons": ["All gates passed", "Strong OOS performance"],
  "next_action": "walk_forward|holdout|deploy|failure_analyzer|archive",
  "failure_mode": null
}
```

---

## regime_test Output Example {#regime-test}

Output structure for cross-regime testing mode.

```json
{
  "status": "SUCCESS",
  "hypothesis_id": "HYP-001",
  "trial_number": 2,
  
  "metrics": {
    "sharpe_raw": 0.62,
    "sharpe_deflated": 0.57,
    "deflation_factor": 0.92,
    "trade_count": 142
  },
  
  "regime_context": {
    "detected_regime": "ELEVATED",
    "classification_confidence": 0.82
  },
  
  "regime_results": {
    "HIGH_RISK": {"sharpe_raw": 0.38, "trade_count": 28, "max_drawdown": -0.31},
    "ELEVATED": {"sharpe_raw": 0.55, "trade_count": 45, "max_drawdown": -0.22},
    "NORMAL": {"sharpe_raw": 0.72, "trade_count": 52, "max_drawdown": -0.15},
    "LOW_RISK": {"sharpe_raw": 0.81, "trade_count": 17, "max_drawdown": -0.09}
  },
  
  "regime_variance": 0.38,
  "regime_consistency": "PASS",
  
  "verdict": "NEEDS_REVIEW",
  "verdict_reasons": ["HIGH_RISK underperformance (Sharpe 0.38 vs threshold 0.20)", "Consider regime filter"],
  "next_action": "failure_analyzer",
  "failure_mode": "regime_mismatch"
}
```

---

## walk_forward Output Example {#walk-forward}

Output structure for rolling window validation mode.

```json
{
  "status": "SUCCESS",
  "hypothesis_id": "HYP-001",
  "trial_number": 3,
  
  "metrics": {
    "sharpe_raw": 0.78,
    "sharpe_deflated": 0.68,
    "deflation_factor": 0.87,
    "trade_count": 234,
    "oos_is_ratio": 0.72
  },
  
  "walk_forward_results": {
    "windows": [
      {
        "window_id": 1,
        "is_start": "2018-01-01", "is_end": "2019-06-30",
        "oos_start": "2019-07-01", "oos_end": "2019-12-31",
        "is_sharpe": 0.95, "oos_sharpe": 0.68, "oos_is_ratio": 0.72,
        "oos_regime": "NORMAL"
      },
      {
        "window_id": 2,
        "is_start": "2018-07-01", "is_end": "2020-01-31",
        "oos_start": "2020-02-01", "oos_end": "2020-07-31",
        "is_sharpe": 0.82, "oos_sharpe": 0.45, "oos_is_ratio": 0.55,
        "oos_regime": "HIGH_RISK"
      },
      {
        "window_id": 3,
        "is_start": "2019-01-01", "is_end": "2020-07-31",
        "oos_start": "2020-08-01", "oos_end": "2021-01-31",
        "is_sharpe": 0.88, "oos_sharpe": 0.71, "oos_is_ratio": 0.81,
        "oos_regime": "ELEVATED"
      }
    ],
    "aggregate_oos_is_ratio": 0.69,
    "consistency_score": 0.78,
    "regime_consistency": {
      "window_regimes": ["NORMAL", "HIGH_RISK", "ELEVATED"],
      "consistency_cv": 0.32,
      "regime_transitions": 2,
      "dominant_regime": "NORMAL"
    }
  },
  
  "verdict": "DEPLOYABLE",
  "verdict_reasons": ["All gates passed", "OOS/IS ratio 0.69 > 0.5", "Regime consistency CV 0.32 < 0.5"],
  "next_action": "holdout"
}
```

---

## Failure Output Example {#failure-output}

Output structure when validation gates fail (NOT_DEPLOYABLE verdict).

```json
{
  "status": "SUCCESS",
  "hypothesis_id": "HYP-002",
  "trial_number": 4,
  
  "metrics": {
    "sharpe_raw": 0.42,
    "sharpe_deflated": 0.34,
    "deflation_factor": 0.82,
    "trade_count": 67,
    "oos_is_ratio": 0.38
  },
  
  "regime_context": {
    "detected_regime": "NORMAL",
    "threshold_adjustment": {
      "sharpe_multiplier": 1.0,
      "drawdown_multiplier": 1.0
    },
    "classification_confidence": 0.91
  },
  
  "validation_gates": {
    "trade_count": {"passed": false, "value": 67, "threshold": 100, "severity": "HARD"},
    "sharpe_deflated": {"passed": true, "value": 0.34, "threshold": 0.30, "severity": "HARD"},
    "oos_is_ratio": {"passed": false, "value": 0.38, "threshold": 0.50, "severity": "HARD"}
  },
  
  "verdict": "NOT_DEPLOYABLE",
  "verdict_reasons": [
    "HARD FAIL: Trade count 67 < 100 minimum",
    "HARD FAIL: OOS/IS ratio 0.38 < 0.50 (curve_fit indicator)"
  ],
  "next_action": "failure_analyzer",
  "failure_mode": "curve_fit"
}
```

---

## tier_test Output {#tier-test}

Output structure for progressive tier validation mode.

```json
{
  "status": "SUCCESS|FAILURE",
  "hypothesis_id": "HYP-001",
  "tier": 2,
  "trial_number": 3,
  
  "period_results": [
    {"period_id": "post_gfc_bull", "sharpe": 0.45, "dd": -0.22, "trades": 34},
    {"period_id": "gfc_bear", "sharpe": 0.22, "dd": -0.31, "trades": 18}
  ],
  
  "aggregated_metrics": {
    "sharpe_avg": 0.38,
    "sharpe_deflated": 0.33,
    "max_drawdown": -0.31,
    "total_trades": 87,
    "regime_cv": 0.42
  },
  
  "gate_results": {
    "sharpe": {"passed": true, "value": 0.38, "threshold": 0.30},
    "drawdown": {"passed": true, "value": -0.31, "threshold": -0.35}
  },
  
  "verdict": "PASS|FAIL",
  "next_tier": 3,
  "failure_mode": null
}
```

---

## capacity_test Output {#capacity-test}

Output structure for scalability testing mode.

```json
{
  "capacity_test_results": {
    "baseline_sharpe": 0.65,
    "scaled_results": [
      {"scale": 2, "capital": 200000, "sharpe": 0.62, "degradation_pct": 4.6},
      {"scale": 5, "capital": 500000, "sharpe": 0.55, "degradation_pct": 15.4},
      {"scale": 10, "capital": 1000000, "sharpe": 0.48, "degradation_pct": 26.2}
    ],
    "capacity_score": 73.8,
    "estimated_capacity_ceiling_usd": 750000,
    "verdict": "PASS"
  }
}
```

---

## dashboard Output {#dashboard}

Output structure for 6-dimension metrics dashboard generation.

```json
{
  "dashboard_path": "backtest-history/runs/{run_id}/dashboard.md",
  "scores": {
    "profitability": 75,
    "risk": 82,
    "consistency": 68,
    "robustness": 71,
    "capacity": 90,
    "efficiency": 77
  },
  "overall_score": 77.2,
  "grade": "B"
}
```

---

## aggregate Output {#aggregate}

Output structure for metric aggregation mode.

```json
{
  "avg_sharpe": 0.38,
  "dsr": 0.33,
  "worst_dd": -0.28,
  "total_trades": 87,
  "avg_win_rate": 0.42,
  "regime_cv": 0.32
}
```

---

## validate Output {#validate}

Output structure for gate validation mode.

```json
{
  "gate_passed": true,
  "failed_gate": null,
  "gate_results": [
    {"gate": "trade_count", "passed": true, "value": 87, "threshold": 50},
    {"gate": "sharpe", "passed": true, "value": 0.38, "threshold": 0.30}
  ]
}
```
