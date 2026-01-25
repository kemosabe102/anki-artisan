# Pattern Detector Examples

Usage examples demonstrating orchestrator delegation patterns for the pattern-detector agent.

| Example | Description |
|---------|-------------|
| `delegation-examples.md` | How orchestrator invokes pattern-detector for detection, validation, and explanation workflows |

## Quick Example

```markdown
Task(pattern-detector,
  "Detect breakout and pullback patterns for AAPL 1d timeframe.
   Data source: packages/core/data/outputs/AAPL_1d_ohlcv.parquet.
   Detection sensitivity: balanced.")
```
