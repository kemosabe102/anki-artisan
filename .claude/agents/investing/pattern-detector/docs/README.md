# Pattern Detector Documentation

Supporting documentation for the pattern-detector agent.

| Document | Purpose |
|----------|---------|
| `pattern-detection.md` | 4 classical pattern frameworks (breakout, pullback, PEAD, divergence) with confidence scoring formulas and code examples |
| `multi-indicator-coordination.md` | Dempster-Shafer evidence theory, Weighted Voting, Consensus threshold frameworks for signal combination |
| `error-recovery.md` | Decision trees for retry/fail/partial, validation checkpoints, edge case handling, performance optimization |
| `talib-integration.md` | TA-Lib CDL pattern functions, pandas-ta fallback strategy, vectorization patterns for large datasets |
| `architecture-integration.md` | DataConnector protocol, OODA loop implementation, Fact object mapping, output schema design |

## Quick Reference

**Pattern Selection by Regime**:
- Trending (ADX >25): breakout, pullback, hidden_divergence
- Ranging (ADX <20): regular_divergence, support_resistance
- Volatile (ATR >80th pct): pead

**Confidence Scoring Range**: 0.4 (base) to 0.95 (max with all confirmations)

**Delegation Boundaries**:
- Indicator computation -> `technical-indicator-specialist`
- Sentiment analysis -> `sentiment-nlp-specialist`
