# Strategy Builder Documentation

Navigation index for the strategy-builder agent documentation.

## Quick Reference

| Document | Purpose |
|----------|---------|
| [../strategy-builder.md](../strategy-builder.md) | Main agent prompt & modes |
| [../schemas/strategy-builder.schema.json](../schemas/strategy-builder.schema.json) | JSON specification schema |
| [../templates/README.md](../templates/README.md) | Template placeholder dictionary |
| [../examples/strategy-examples.md](../examples/strategy-examples.md) | Complete NL→JSON→Python examples |

## Local Documentation

| Document | Purpose |
|----------|---------|
| [development_guide.md](development_guide.md) | Development workflow & practices |
| [iteration_framework.md](iteration_framework.md) | Strategy iteration methodology |

## Templates

| Template | Strategy Type | Use When |
|----------|---------------|----------|
| `momentum-template.py` | Trend-following | Breakout, momentum continuation |
| `mean-reversion-template.py` | Mean-reversion | RSI oversold, Bollinger band reversals |
| `event-driven-template.py` | Event-driven | Earnings, news events |
| `multi-factor-template.py` | Multi-factor | Combined scoring strategies |

## Key Concepts

### 9-Field JSON Schema

Every strategy specification requires:
1. **strategy_name** - Unique identifier
2. **strategy_type** - momentum, mean_reversion, event_driven, multi_factor
3. **universe** - Symbol selection
4. **entry** - Entry conditions
5. **exit** - Exit conditions
6. **position_sizing** - Size calculation method
7. **risk_management** - Portfolio-level limits
8. **timeframe** - Trading frequency
9. **regime_filters** - Market regime detection (REQUIRED)

**Note**: `strategy_name` and `strategy_type` are agent-determined from classification; users specify the remaining 7 elements.

### Enforcement Gates

| Gate | Requirement |
|------|-------------|
| ALGO_GATE_001 | `regime_filters` must be specified |
| ALGO_GATE_002 | `position_sizing` must be specified |
| ALGO_GATE_003 | `timeframe` must be specified |


## Modes

| Mode | Output |
|------|--------|
| `full_build` | JSON spec + Python skeleton |
| `spec_only` | JSON spec only |
| `skeleton_only` | Python skeleton from existing spec |
| `classify_only` | Strategy type classification |
| `hdd_validate` | Hypothesis validation |
| `hypothesis_only` | Hypothesis formulation |
| `submit_to_backtest` | Route to backtester |
| `validate` | Validate spec against schema |

## See Also

- `.claude/skills/strategy-specification/SKILL.md` - 7-element framework details
- `.claude/skills/hypothesis-formulation/SKILL.md` - Cause-Effect-Why format
- `.claude/commands/backtest.md` - Backtest orchestration
