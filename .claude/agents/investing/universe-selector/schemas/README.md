# Universe Selector Schemas

## Schema Location

The canonical schema for universe-selector is located at the project level:

**Source of Truth**: `.claude/schemas/universe-selector.schema.json`

This agent does NOT maintain a local schema copy to avoid divergence. All schema updates should be made to the project-level file.

## Schema Contract

See `.claude/schemas/universe-selector.schema.json` for:
- Input validation (symbols, date_range, thresholds, asset_classes)
- Output contract (status, gates, validated_symbols, excluded_symbols, metadata)
- Gate definitions and quality score formula
