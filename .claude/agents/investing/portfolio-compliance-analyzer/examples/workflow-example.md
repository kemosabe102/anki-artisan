# Workflow Example: Portfolio Compliance Analysis

**Purpose**: Complete example showing inputs, analysis flow, and output structure

---

## Sample Input

### IPS Document (JSON format)
```json
{
  "saa_targets": {
    "US_Equity": { "neutral": 0.40, "min": 0.35, "max": 0.45 },
    "Intl_Equity": { "neutral": 0.20, "min": 0.15, "max": 0.25 },
    "Fixed_Income": { "neutral": 0.30, "min": 0.25, "max": 0.35 },
    "Cash": { "neutral": 0.10, "min": 0.05, "max": 0.15 }
  },
  "risk_budget": {
    "max_drawdown_pct": 15,
    "vol_target_pct": 12,
    "var_limit": 5
  },
  "rebalancing_bands": {
    "US_Equity": 5,
    "Intl_Equity": 5,
    "Fixed_Income": 3,
    "Cash": 5
  },
  "investor_constraints": {
    "liquidity_min_pct": 5,
    "prohibited_securities": ["TOBACCO_ETF"],
    "concentration_limits": { "single_security": 10 }
  }
}
```

### Holdings Data (CSV format)
```csv
symbol,quantity,current_price,cost_basis,purchase_date,account_type
VTI,100,250.00,22000.00,2023-01-15,taxable
VXUS,50,60.00,3200.00,2023-03-20,taxable
BND,80,75.00,6200.00,2022-06-10,IRA
VMFXX,200,1.00,200.00,2024-01-01,taxable
```

---

## SUCCESS Output Example

```json
{
  "status": "SUCCESS",
  "agent": "portfolio-compliance-analyzer",
  "task_id": "pca-2025-001",
  "operation_type": "portfolio_compliance_analysis",
  "summary": "Portfolio shows 3.2% allocation drift from SAA targets. Recommended rebalancing trades will reduce drift to <1%. Identified $1,500 in tax-loss harvesting opportunities. No IPS violations flagged.",
  "confidence": 0.88,
  "execution_timestamp": "2025-01-15T14:30:00Z",
  "agent_specific_output": {
    "gap_analysis": {
      "current_allocation": {
        "US_Equity": 0.432,
        "Intl_Equity": 0.052,
        "Fixed_Income": 0.103,
        "Cash": 0.413
      },
      "target_allocation": {
        "US_Equity": 0.40,
        "Intl_Equity": 0.20,
        "Fixed_Income": 0.30,
        "Cash": 0.10
      },
      "allocation_drift": {
        "US_Equity": 0.032,
        "Intl_Equity": -0.148,
        "Fixed_Income": -0.197,
        "Cash": 0.313
      },
      "drift_severity": "EXCEEDS_TOLERANCE",
      "risk_metrics_comparison": {
        "current_volatility": 0.08,
        "target_volatility": 0.12,
        "current_drawdown": -0.02,
        "max_drawdown_limit": 0.15
      }
    },
    "rebalancing_recommendations": {
      "trades": [
        {
          "symbol": "VXUS",
          "action": "BUY",
          "quantity": 150,
          "lot_id": null,
          "rationale": "Increase Intl_Equity from 5.2% to 20% target"
        },
        {
          "symbol": "BND",
          "action": "BUY",
          "quantity": 200,
          "lot_id": null,
          "rationale": "Increase Fixed_Income from 10.3% to 30% target"
        }
      ],
      "expected_post_trade_allocation": {
        "US_Equity": 0.40,
        "Intl_Equity": 0.20,
        "Fixed_Income": 0.30,
        "Cash": 0.10
      }
    },
    "tax_optimization": {
      "harvest_opportunities": [
        {
          "symbol": "VXUS",
          "unrealized_loss": 200.00,
          "lot_id": "LOT-VXUS-001",
          "cost_basis": 3200.00,
          "current_value": 3000.00,
          "purchase_date": "2023-03-20",
          "replacement_candidates": ["IXUS", "VEU"]
        }
      ],
      "projected_tax_savings": 30.00,
      "wash_sale_warnings": []
    },
    "tactical_sleeve_adjustments": {
      "sleeve_status": {},
      "recommended_actions": []
    },
    "compliance_flags": {
      "risk_violations": [],
      "kill_switch_status": false,
      "constraint_violations": []
    },
    "summary_narrative": "Portfolio shows significant drift from SAA targets, primarily due to excess cash allocation. Rebalancing into international equity and fixed income recommended. One tax-loss harvesting opportunity identified in VXUS position. No compliance violations detected.",
    "analysis_metadata": {
      "analysis_date": "2025-01-15T14:30:00Z",
      "execution_time_seconds": 12.5,
      "holdings_count": 4,
      "confidence_score": 0.88
    }
  }
}
```

---

## FAILURE Output Example

```json
{
  "status": "FAILURE",
  "agent": "portfolio-compliance-analyzer",
  "task_id": "pca-2025-002",
  "operation_type": "portfolio_compliance_analysis",
  "summary": "Failed to parse IPS document. PDF appears to be scanned image without OCR text layer.",
  "confidence": 0.0,
  "execution_timestamp": "2025-01-15T14:35:00Z",
  "failure_details": {
    "failure_type": "IPS_PARSE_ERROR",
    "error_details": "PyPDF2 extracted 0 text characters. pdfplumber also returned empty text. PDF appears to be image-based without OCR layer.",
    "recovery_suggestions": [
      "Provide IPS in text-based format (markdown or JSON)",
      "Run OCR on PDF before uploading",
      "Manually transcribe IPS into JSON structure"
    ],
    "partial_results": {
      "ips_constraints": null
    },
    "validation_errors": [
      {
        "field_name": "ips_document",
        "expected_format": "PDF with searchable text or markdown/JSON",
        "actual_value": "PDF (5 pages, 0 text characters)",
        "validation_rule_violated": "IPS document must be machine-readable"
      }
    ]
  }
}
```

---

## Command Invocation

```bash
# Via slash command
/analyze-portfolio --ips data/ips.json --holdings data/holdings.csv --output reports/

# Direct Bash execution (with AGENT_NAME prefix)
AGENT_NAME=portfolio-compliance-analyzer python scripts/analyze_portfolio.py \
  --ips data/ips.json \
  --holdings data/holdings.csv \
  --mode comprehensive \
  --output reports/analysis_2025-01-15.json
```
