# Analyze Agent Schemas

JSON schemas for `/analyze-agent` command outputs.

## Files

| File | Purpose |
|------|---------|
| `report.schema.json` | Analysis report output structure |

## Usage

The schema defines the structure of the analysis report output, enabling:
- Validation of report completeness
- Integration with automation tools
- Consistent report parsing

## Schema Highlights

- **Overall score**: 0-100 with grade mapping
- **5 dimensions**: Prompt, Schema, Documentation, Integration, Methodology
- **Findings**: P1/P2/P3 priority with impact/effort scores
- **Token savings**: Quantified opportunities with strategies
- **Maturity**: v0.x through v3.x assessment
