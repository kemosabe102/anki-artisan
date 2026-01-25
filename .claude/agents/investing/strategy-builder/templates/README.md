# Strategy Builder Templates

Reference documentation for QC Python template placeholders.

## Templates

| Template | Strategy Type | Description |
|----------|---------------|-------------|
| `momentum-template.py` | Momentum/Trend | Trend-following with breakout entry |
| `mean-reversion-template.py` | Mean-Reversion | RSI oversold/overbought signals |
| `event-driven-template.py` | Event-Driven | News/earnings event reactions |
| `multi-factor-template.py` | Multi-Factor | Combined scoring factors |

## Placeholder Dictionary

All templates support the following placeholders for customization:

### Core Placeholders

| Placeholder | Location | Purpose |
|-------------|----------|---------|
| `{{UNIVERSE}}` | `initialize()` | Symbol selection logic |
| `{{ENTRY_CONDITIONS}}` | `_check_entry()` | Entry signal criteria |
| `{{EXIT_CONDITIONS}}` | `_check_exit()` | Exit signal criteria |
| `{{POSITION_SIZE}}` | `_execute_entry()` | Base position sizing logic |
| `{{RISK_PARAMS}}` | `initialize()` | Risk parameter values |

### Regime-Adaptive Placeholders (NEW)

| Placeholder | Location | Purpose |
|-------------|----------|---------|
| `{{REGIME_CONDITIONS}}` | `_update_regime_multiplier()` | Custom regime detection logic |

**Default Regime Logic**: SPY above/below 200-day SMA
- Above 200 DMA: `regime_multiplier = 1.0` (full position)
- Below 200 DMA: `regime_multiplier = 0.5` (half position)

### Event-Driven Specific

| Placeholder | Location | Purpose |
|-------------|----------|---------|
| `{{EVENT_CONDITIONS}}` | `_event_signal()` docstring | Event detection description |
| `{{EVENT_SIGNAL_LOGIC}}` | `_event_signal()` | Custom event detection code |

## Position Sizing Formula

All templates use regime-adaptive position sizing:

```python
base_shares = int(risk_dollars / stop_distance)
shares = int(base_shares * self.regime_multiplier)
```

This ensures position size adjusts based on market regime while maintaining risk management.

## Usage

1. Select template matching strategy type
2. Replace placeholders with strategy-specific logic
3. Customize `{{REGIME_CONDITIONS}}` for regime detection
4. Test with backtester across all market regimes

## See Also

- `../strategy-builder.md` - Agent documentation
- `../schemas/strategy-builder.schema.json` - JSON specification schema
- `../examples/` - Complete strategy examples
