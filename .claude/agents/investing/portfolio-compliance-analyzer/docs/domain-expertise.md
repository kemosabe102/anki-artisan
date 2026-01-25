# Domain Expertise: Portfolio Compliance Analysis

**Purpose**: Detailed calculation methods, IPS parsing rules, and financial domain knowledge

---

## 1. IPS Parsing & Constraint Extraction

### Required IPS Sections

| Section | Fields | Example |
|---------|--------|---------|
| **SAA Targets** | asset_class, neutral_weight, min_weight, max_weight | US Equity: 40% (35%-45%) |
| **Risk Budget** | max_drawdown_pct, vol_target_pct, var_limit | Max DD: 15%, Vol: 12%, VaR: 5% |
| **Rebalancing Bands** | asset_class, tolerance_pct | Equity: +/-5%, Bonds: +/-3% |
| **Tactical Sleeves** | name, activation_rules, max_allocation_pct | Momentum: 10% max |
| **Investor Constraints** | liquidity_min, prohibited_securities, concentration_limits | 5% cash min, no tobacco |

### Parsing Strategy

1. **PDF**: Use PyPDF2 first, fallback to pdfplumber if text extraction fails
2. **Markdown/JSON**: Direct parsing with validation against schema
3. **Ambiguity Handling**: Flag qualitative terms ("moderate risk") for user clarification

---

## 2. Portfolio Metrics Calculation

### Allocation Weights
```
weight_i = (quantity_i × price_i) / total_portfolio_value
```

### Volatility (Annualized)
```
vol = std_dev(daily_returns) × sqrt(252)
```

### Value at Risk (VaR) Methods

| Method | Formula | When to Use |
|--------|---------|-------------|
| **Parametric** | `VaR = μ - z × σ` (z=1.645 for 95%) | Normal distributions, quick estimate |
| **Historical Simulation** | Sort returns, take percentile | Non-normal distributions |
| **Monte Carlo** | Simulate 10,000+ paths | Complex portfolios, fat tails |

### Euler Decomposition (Risk Contribution)
```
RC_i = w_i × MCTR_i
MCTR_i = (Σ × w)_i / σ_portfolio
```
Where: RC = Risk Contribution, MCTR = Marginal Contribution to Total Risk, Σ = covariance matrix

### Correlation Matrix Construction

**Ledoit-Wolf Shrinkage** (default): `sklearn.covariance.LedoitWolf()`
- Stabilizes eigenvalues for small sample sizes
- Prevents singular matrices

**EWMA** (time-varying): `pandas.ewm(span=60).cov()`
- More responsive to recent volatility changes

---

## 3. Gap Analysis

### Drift Classification

| Severity | Condition | Action |
|----------|-----------|--------|
| `WITHIN_BANDS` | abs(drift) <= tolerance | No action required |
| `APPROACHING_LIMIT` | tolerance × 0.8 < abs(drift) <= tolerance | Monitor closely |
| `EXCEEDS_TOLERANCE` | abs(drift) > tolerance | Rebalancing recommended |

### Risk Violation Flags

- **MAX_DRAWDOWN**: current_drawdown > max_drawdown_pct
- **VOLATILITY_TARGET**: portfolio_vol > vol_target_pct × 1.1 (10% buffer)
- **VAR_LIMIT**: var_estimate > var_limit
- **CONCENTRATION**: single_position_weight > concentration_limit

---

## 4. Rebalancing Optimization

### CVXPY Formulation
```python
import cvxpy as cp

x = cp.Variable(n_assets)  # New weights
objective = cp.Minimize(
    cp.quad_form(x, cov_matrix) +           # Minimize variance
    gamma * cp.sum_squares(x - target)       # Track SAA targets
)
constraints = [
    cp.sum(x) == 1,                          # Fully invested
    x >= min_weights,                        # IPS minimums
    x <= max_weights,                        # IPS maximums
    cp.abs(x - current) <= max_turnover      # Transaction cost limit
]
prob = cp.Problem(objective, constraints)
```

### Lot Selection Strategies

| Strategy | Logic | Tax Impact |
|----------|-------|------------|
| **HIFO** | Sell highest cost basis first | Minimize gains / Maximize losses |
| **LIFO** | Sell most recent purchases | May trigger STCG |
| **Specific ID** | Select specific lots | Maximum control |
| **FIFO** | Sell oldest first | Often default, may not optimize |

---

## 5. Tax-Loss Harvesting

### Wash-Sale Rule (61-Day Window)

**Rule**: Cannot claim loss if "substantially identical" security purchased within:
- 30 days BEFORE the sale
- Sale date
- 30 days AFTER the sale

**Substantially Identical**: Same security, options on same security, convertibles. Different share classes (e.g., GOOG vs GOOGL) may qualify.

**Cross-Account**: Applies across ALL accounts (taxable, IRA, 401k, spouse accounts)

### Replacement Candidate Selection

1. Find securities with correlation < 0.85 to harvested position
2. Verify not substantially identical (different issuer, different index)
3. Confirm no purchase within 61-day window in any account

### Tax Savings Calculation

```
projected_savings = unrealized_loss × marginal_tax_rate

# 2024 LTCG rates (held > 1 year)
# 0% (income < $47,025 single / $94,050 MFJ)
# 15% (income < $518,900 single / $583,750 MFJ)
# 20% (income >= above)
# +3.8% NIIT if AGI > $200,000 single / $250,000 MFJ

# STCG (held <= 1 year): Ordinary income rates (up to 37%)
```

---

## 6. Tactical Sleeve Management

### Activation Triggers (IPS-Defined)
- Market volatility threshold (e.g., VIX > 25)
- Momentum signals (e.g., 200-day MA crossover)
- Macroeconomic indicators (e.g., yield curve inversion)

### Risk Contribution Analysis

Use Euler decomposition to measure sleeve impact:
```
sleeve_RC = Σ(position_RC) for positions in sleeve
sleeve_RC_pct = sleeve_RC / total_portfolio_RC × 100
```

### Recommended Actions

| Status | Trigger Met | Current vs Target RC | Action |
|--------|-------------|---------------------|--------|
| INACTIVE | Yes | N/A | ACTIVATE to target size |
| ACTIVE | No | Within 20% | No action |
| ACTIVE | No | >20% deviation | RESIZE or DEACTIVATE |
| ACTIVE | Yes | >20% deviation | RESIZE to target |

---

## 7. Compliance Validation

### Kill-Switch Conditions
- Portfolio drawdown exceeds emergency threshold (e.g., -25%)
- Single-day loss exceeds limit (e.g., -5%)
- Requires immediate user notification and manual review

### Concentration Limits
- Single security: typically 5-10% max
- Single sector: typically 25-30% max
- Single issuer (bonds): typically 5% max

### Prohibited Securities
- User-defined exclusions (ESG, ethical, legal restrictions)
- Check against holdings list, flag any matches

---

## Quick Reference: Key Formulas

| Metric | Formula |
|--------|---------|
| Weight | `value_i / total_value` |
| Drift | `current_weight - target_weight` |
| VaR (95%) | `μ - 1.645 × σ` |
| Risk Contribution | `w_i × (Σw)_i / σ_p` |
| Tax Savings | `loss × marginal_rate` |
