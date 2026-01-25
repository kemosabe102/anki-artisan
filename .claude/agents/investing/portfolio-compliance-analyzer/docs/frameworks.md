# Frameworks: Portfolio Compliance Analysis

**Purpose**: Methodologies and workflow patterns for portfolio analysis

---

## 1. OODA Loop Framework

**Observe → Orient → Decide → Act**

| Phase | Portfolio Analysis Application |
|-------|-------------------------------|
| **Observe** | Parse IPS constraints, load holdings data, assess market data availability |
| **Orient** | Identify analysis mode, select calculation methods (VaR approach, correlation), understand tax jurisdiction |
| **Decide** | Choose optimization approach, tax strategies, determine compliance flags |
| **Act** | Execute calculations, validate results, generate recommendations with XAI rationale |

---

## 2. 8-Phase Workflow

**Sequential execution - each phase depends on previous**

### Phase 1: Parse IPS
- Extract SAA table (neutral/min/max weights)
- Extract risk budget (max_drawdown, vol_target, VaR_limit)
- Extract rebalancing bands (tolerance percentages)
- Extract tactical sleeves (activation rules, max allocation)
- Extract investor constraints (prohibited securities, liquidity, concentration)

### Phase 2: Calculate Metrics
- Compute allocation weights per asset class
- Calculate volatility (annualized)
- Calculate current drawdown from peak
- Estimate VaR (parametric default, Monte Carlo if complex)
- Build correlation matrix (Ledoit-Wolf shrinkage)

### Phase 3: Gap Analysis
- Compare current weights vs SAA targets
- Calculate percentage point deviations
- Classify drift severity (WITHIN_BANDS / APPROACHING_LIMIT / EXCEEDS_TOLERANCE)
- Compare risk metrics vs IPS constraints

### Phase 4: Rebalancing
- Run CVXPY optimization with IPS constraints
- Generate trade list (BUY/SELL with quantities)
- Apply tax-aware lot selection (HIFO/LIFO/Specific ID)
- Rank trades by impact on allocation alignment

### Phase 5: Tax Optimization
- Identify unrealized losses (lot-level)
- Validate 61-day wash-sale window across ALL accounts
- Find replacement candidates (correlation < 0.85)
- Calculate projected tax savings

### Phase 6: Tactical Sleeves
- Evaluate activation trigger conditions
- Calculate current risk contribution (Euler decomposition)
- Generate ACTIVATE/DEACTIVATE/RESIZE recommendations

### Phase 7: Compliance Validation
- Check risk violations (drawdown, volatility, VaR, concentration)
- Evaluate kill-switch status
- Validate investor constraints (prohibited securities, liquidity)

### Phase 8: Generate Report
- Construct agent_specific_output JSON
- Validate against schema
- Generate executive summary (3-5 sentences)
- Write JSON + markdown reports


---

## 3. Error Recovery Patterns

### Retry Logic

| Error Type | Retry Strategy | Max Attempts |
|------------|----------------|--------------|
| PDF parse failure | Switch parser (PyPDF2 ↔ pdfplumber) | 2 |
| Numerical precision | Increase precision (float64 → float128) | 1 |
| Solver timeout | Increase max_iter, relax tolerances | 2 |

### Checkpoint Strategy

Save intermediate state after each successful phase:
1. `checkpoint_ips.json` - After Phase 1
2. `checkpoint_metrics.json` - After Phase 2
3. `checkpoint_trades.json` - After Phase 4

### Graceful Degradation

| Missing Data | Behavior |
|--------------|----------|
| Partial market data | Continue with available data, lower confidence, populate `data_requirements` |
| IPS section unreadable | Parse available sections, flag missing in `partial_results` |
| Calculation failure | Skip failed module, return `partial_results` with diagnostic info |

### Failure Communication

Return FAILURE with:
- `failure_type`: Enum (IPS_PARSE_ERROR, HOLDINGS_DATA_INVALID, MARKET_DATA_UNAVAILABLE, CALCULATION_ERROR, INSUFFICIENT_DATA, CONSTRAINT_VALIDATION_ERROR)
- `error_details`: Specific line numbers or field names
- `recovery_suggestions`: Actionable remediation steps
- `partial_results`: Successfully completed sections

---

## 4. Simulation-Driven Development

**Think from the portfolio manager's perspective:**

1. **IPS as Invariants** - Constraints are non-negotiable rules, not suggestions
2. **Trade-off Simulation** - Balance transaction costs vs tracking error vs tax impact
3. **Regulatory Awareness** - Wash-sale rules, fiduciary obligations, XAI requirements
4. **Edge Cases** - Singular correlation matrices, zero-weight classes, extreme drawdowns

---

## Quick Reference: Phase Dependencies

```
IPS → Metrics → Gap → Rebalancing → Tax → Sleeves → Compliance → Report
 1  →    2    →  3  →      4      →  5  →    6    →     7      →   8
```

**Cannot parallelize**: Each phase depends on outputs from previous phase.
