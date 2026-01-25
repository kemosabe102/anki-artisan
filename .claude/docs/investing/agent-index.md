---
title: Investing Agents Index
date: 2025-01-09
status: active
tags: [agents, investing, algo-strategy, trading]
---

# Investing Agents Index

> Comprehensive reference for all investing domain agents and their workflow integration.

---

## Agent Categories

| Category | Agents | Purpose |
|----------|--------|---------|
| Data & Validation | market-data-specialist, data-validator, universe-selector | Data quality, availability, universe validation |
| Analysis | pattern-detector, technical-indicator-specialist, news-impact-analyzer | Pattern recognition, technical analysis, news impact |
| Risk & Execution | risk-management-specialist, execution-modeler | Position sizing, regime classification, execution costs |
| Strategy | strategy-builder, backtester | Strategy generation, backtesting |
| Validation | sensitivity-tester, crisis-stress-tester | Parameter sensitivity, stress testing |
| Compliance | portfolio-compliance-analyzer | IPS compliance, rebalancing |
| Sentiment | sentiment-nlp-specialist | NLP-based sentiment analysis |

---

## Agent Details

### Data & Validation Agents

#### market-data-specialist

**Purpose**: Validate OHLCV data availability and quality for backtesting.

| Attribute | Value |
|-----------|-------|
| Location | `.claude/agents/investing/market-data-specialist/` |
| Phases | P3 (parallel), P12 (parallel) |
| Workflow | Classic + Full |

**Capabilities**:
- OHLCV gap detection
- Volume data validation
- Indicator dependency checks
- Data confidence scoring

**Integration Points**:
- Provides `data_confidence_score` to P12 gate
- Parallel execution with risk-management-specialist in P3

---

#### data-validator

**Purpose**: Comprehensive data quality auditing and gap detection.

| Attribute | Value |
|-----------|-------|
| Location | `.claude/agents/investing/data-validator/` |
| Phases | Pre-workflow |
| Workflow | On-demand |

**Capabilities**:
- Quality metrics calculation
- Category-based requirements validation
- Gap detection with severity classification

---

#### universe-selector

**Purpose**: Validate investment universe for survivor bias and liquidity.

| Attribute | Value |
|-----------|-------|
| Location | `.claude/agents/investing/universe-selector/` |
| Phases | P3 |
| Workflow | Full only |

**Capabilities**:
- Survivor bias detection (delisted, M&A, symbol changes)
- Liquidity threshold validation (volume, dollar volume, spread)
- Sector concentration analysis
- Universe quality scoring (0-1)

**Gates Owned**:
- SURVIVOR_BIAS_CHECK: universe_quality_score >= 0.7

**Samir Varma Integration**:
- Ensures realistic execution assumptions
- Flags illiquid symbols that create unrealistic backtests

---

### Analysis Agents

#### pattern-detector

**Purpose**: Identify chart patterns and candlestick formations.

| Attribute | Value |
|-----------|-------|
| Location | `.claude/agents/investing/pattern-detector/` |
| Phases | On-demand |
| Workflow | Strategy development |

**Capabilities**:
- TA-Lib pattern integration
- Multi-indicator coordination
- Error recovery patterns

---

#### technical-indicator-specialist

**Purpose**: Calculate and validate technical indicators.

| Attribute | Value |
|-----------|-------|
| Location | `.claude/agents/investing/technical-indicator-specialist/` |
| Phases | On-demand |
| Workflow | Strategy development |

**Capabilities**:
- Edge case methodology
- Warmup period calculation
- Indicator dependency mapping

---

#### news-impact-analyzer

**Purpose**: Analyze news events and their market impact.

| Attribute | Value |
|-----------|-------|
| Location | `.claude/agents/investing/news-impact-analyzer/` |
| Phases | On-demand |
| Workflow | Event-driven strategies |

**Capabilities**:
- Impact formula calculation
- Regime classification
- Scenario generation
- Escalation patterns

---

### Risk & Execution Agents

#### risk-management-specialist

**Purpose**: Position sizing, regime classification, and circuit breaker configuration.

| Attribute | Value |
|-----------|-------|
| Location | `.claude/agents/investing/risk-management-specialist/` |
| Phases | P3 (parallel), P6, P8 |
| Workflow | Classic + Full |

**Capabilities**:
- Volatility regime classification (ATR percentile)
- Trend regime classification (200DMA position)
- Position sizing methods (fixed, volatility_scaled, kelly, regime_adjusted)
- Circuit breaker configuration
- 5-factor regime model

**Gates Owned**:
- SIZING_METHOD_VALID
- REGIME_ADJUSTMENT_CONFIGURED
- REGIME_CLASSIFICATION_COMPLETE
- CIRCUIT_BREAKERS_CONFIGURED

**Samir Varma Integration**:
- 200DMA risk asymmetry (67%/33% return split)
- CDAP framework (context-aware drawdown)
- 5-factor regime model (Volatility, Correlation, Trend, Credit, Sentiment)

---

#### execution-modeler

**Purpose**: Model execution costs, slippage, and market impact.

| Attribute | Value |
|-----------|-------|
| Location | `.claude/agents/investing/execution-modeler/` |
| Phases | P7 |
| Workflow | Full only |

**Capabilities**:
- Slippage estimation (based on trade size vs ADV)
- Market impact modeling (square-root model)
- Viability threshold validation
- +50% slippage stress scenarios

**Gates Owned**:
- SLIPPAGE_SENSITIVITY_PASS: Sharpe after costs > 0.5 AND stress viable

**Thresholds**:
- Slippage: < 50 bps
- Market impact (liquid): < 20 bps
- Total execution cost: < 30% of expected alpha

---

### Strategy Agents

#### strategy-builder

**Purpose**: Generate JSON specifications and QC Python skeletons.

| Attribute | Value |
|-----------|-------|
| Location | `.claude/agents/investing/strategy-builder/` |
| Phases | P4 (classic), P13 (full) |
| Workflow | Classic + Full |

**Capabilities**:
- JSON spec generation from hypothesis bundle
- QC Python skeleton generation
- Locked parameter enforcement
- Position sizing config integration (full mode)

---

#### backtester

**Purpose**: Execute HDD-compliant backtests with proper configuration.

| Attribute | Value |
|-----------|-------|
| Location | `.claude/agents/investing/backtester/` |
| Phases | P9 |
| Workflow | Full only |

**Capabilities**:
- Sharpe ratio calculation
- Trade count validation
- Win rate, profit factor, max drawdown metrics
- Calmar ratio calculation
- Deflated Sharpe adjustment

**Gates Owned**:
- SHARPE_MINIMUM: >= 0.5
- TRADE_COUNT_MINIMUM: >= 100

---

### Validation Agents

#### sensitivity-tester

**Purpose**: Parameter sensitivity analysis and walk-forward validation.

| Attribute | Value |
|-----------|-------|
| Location | `.claude/agents/investing/sensitivity-tester/` |
| Phases | P10 |
| Workflow | Full only |

**Capabilities**:
- +/-10% parameter perturbation noise test
- 5-fold walk-forward validation
- Fragile parameter identification
- Cliff-edge detection

**Gates Owned**:
- NOISE_ROBUST: Sharpe degrades < 30% under noise
- WALK_FORWARD_VALID: OOS Sharpe > 50% of IS

**Samir Varma Integration**:
- Stress-testing patterns methodology
- Avoid overfitting through noise injection

---

#### crisis-stress-tester

**Purpose**: Test strategy against historical market crises.

| Attribute | Value |
|-----------|-------|
| Location | `.claude/agents/investing/crisis-stress-tester/` |
| Phases | P11 |
| Workflow | Full only |

**Capabilities**:
- Historical crisis period testing
- Tail risk metrics (VaR 95%, VaR 99%, CVaR 99%)
- Crisis survivability assessment
- Recommendations for regime filters

**Crisis Periods**:
| Crisis | Period | Benchmark DD |
|--------|--------|--------------|
| GFC 2008 | Oct 2008 - Mar 2009 | -56.8% |
| COVID 2020 | Feb 2020 - Mar 2020 | -33.9% |
| Rate Hike 2022 | Jan 2022 - Oct 2022 | -25.4% |

**Gates Owned**:
- CRISIS_2008: DD < 2x benchmark DD
- CRISIS_2020: DD < 50%
- CRISIS_2022: Sharpe > 0 OR DD < 30%

---

### Compliance & Sentiment Agents

#### portfolio-compliance-analyzer

**Purpose**: IPS compliance checking and rebalancing recommendations.

| Attribute | Value |
|-----------|-------|
| Location | `.claude/agents/investing/portfolio-compliance-analyzer/` |
| Phases | On-demand |
| Workflow | Portfolio management |

**Capabilities**:
- IPS compliance validation
- Tax optimization suggestions
- Rebalancing recommendations
- Calculation standards enforcement

---

#### sentiment-nlp-specialist

**Purpose**: NLP-based sentiment analysis of market text.

| Attribute | Value |
|-----------|-------|
| Location | `.claude/agents/investing/sentiment-nlp-specialist/` |
| Phases | On-demand |
| Workflow | Sentiment-based strategies |

**Capabilities**:
- Text sentiment extraction
- Security pattern detection
- Sentiment regime classification

---

## Phase Mapping Summary

| Phase | Agents | Mode |
|-------|--------|------|
| P1 | - | Full |
| P2 | - | Full |
| P3 | universe-selector, market-data-specialist (parallel), risk-management-specialist (parallel) | Full |
| P4 | - | Both |
| P5 | - | Both |
| P6 | risk-management-specialist | Full |
| P7 | execution-modeler | Full |
| P8 | risk-management-specialist | Full |
| P9 | backtester | Full |
| P10 | sensitivity-tester | Full |
| P11 | crisis-stress-tester | Full |
| P12 | market-data-specialist (parallel) | Both |
| P13 | strategy-builder | Both |
| P14 | - | Both |
| P15 | - | Both |
| P16 | - | Full |
| P17 | - | Full |

---

## References

- Workflow Overview: `.claude/docs/investing/algo-strategy-workflow.md`
- Quick Reference: `.claude/docs/investing/algo-strategy-quick-ref.md`
- Samir Varma: `.claude/docs/investing/samir/samir-varma-insights.md`
