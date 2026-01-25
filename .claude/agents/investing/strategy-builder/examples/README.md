# Strategy Builder Examples

## Delegation Examples

```markdown
# Full Build (NL -> Spec -> Code)
Task(strategy-builder, "Build a momentum strategy that buys SPY when 20-day EMA crosses above 50-day EMA, with 2% stop loss")

# Spec Only
Task(strategy-builder, "Convert to spec: Mean reversion on RSI < 30 for QQQ, exit at RSI > 50")

# Skeleton from Spec
Task(strategy-builder, "Generate QC skeleton for this spec: {existing_json_spec}")
```

## Example Conversions

See [strategy-examples.md](./strategy-examples.md) for complete NL -> JSON -> Python examples.
