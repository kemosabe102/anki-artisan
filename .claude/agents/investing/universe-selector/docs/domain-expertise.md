# Domain Expertise: Universe Selection

## Survivor Bias Detection

### What is Survivor Bias?
Survivor bias occurs when backtests only include securities that "survived" to the present day, excluding those that were delisted, acquired, or went bankrupt. This systematically overstates historical returns.

### Detection Patterns

| Event Type | Detection Signal | Example |
|------------|------------------|---------|
| **Delisting** | Symbol no longer trades | Enron (ENE) - delisted 2001 |
| **Acquisition** | Merged into another entity | LinkedIn (LNKD) → Microsoft 2016 |
| **Bankruptcy** | Chapter 7/11 filing | Lehman Brothers (LEH) - 2008 |
| **Going Private** | Taken private by PE | Dell (DELL) - 2013 |
| **Ticker Change** | Same company, new symbol | Google (GOOG) → Alphabet (GOOGL) |

### Point-in-Time Validation
Always validate universe composition AS OF the backtest start date, not current date.

```
# WRONG: Use current S&P 500 constituents for 2010 backtest
# CORRECT: Use S&P 500 constituents as of 2010-01-01
```

## Sector Classification (GICS)

### 11 GICS Sectors
1. **Technology** (45) - Software, Hardware, Semiconductors
2. **Healthcare** (35) - Pharma, Biotech, Medical Devices
3. **Financials** (40) - Banks, Insurance, Asset Management
4. **Consumer Discretionary** (25) - Retail, Autos, Leisure
5. **Consumer Staples** (30) - Food, Beverages, Household
6. **Industrials** (20) - Aerospace, Machinery, Transport
7. **Energy** (10) - Oil & Gas, Equipment
8. **Materials** (15) - Chemicals, Metals, Mining
9. **Real Estate** (60) - REITs, Real Estate Services
10. **Utilities** (55) - Electric, Gas, Water
11. **Communication Services** (50) - Telecom, Media, Entertainment

### Concentration Risk Thresholds

| Concentration | Risk Level | Action |
|---------------|------------|--------|
| < 25% | LOW | No action |
| 25-40% | MODERATE | Monitor |
| > 40% | HIGH | WARN (SECTOR_BALANCED gate) |
| > 60% | CRITICAL | Recommend diversification |

## Liquidity Screening

### Average Daily Volume (ADV)
- **Institutional threshold**: $10M+ ADV
- **Retail threshold**: $1M+ ADV (default)
- **Micro-cap allowance**: $100K+ ADV (with warning)

### Market Capitalization
- **Large-cap**: > $10B
- **Mid-cap**: $2B - $10B
- **Small-cap**: $300M - $2B
- **Micro-cap**: < $300M (requires explicit flag)

### Why Liquidity Matters
1. **Slippage**: Illiquid securities have higher execution costs
2. **Capacity**: Strategy capacity limited by universe liquidity
3. **Realism**: Paper gains may not be realizable in practice
