# Market Data Specialist - Schemas

JSON Schema definitions for market-data-specialist agent input/output contracts.

## Contents

| Schema | Purpose |
|--------|---------|
| [market-data-specialist.schema.json](market-data-specialist.schema.json) | Agent input/output contract |

## Schema Overview

The schema extends the base agent pattern with domain-specific output fields:

### Operation Types
- `validate_ohlcv` - OHLCV data validation with quality scoring
- `implement_connector` - DataConnector implementation
- `compress_dataset` - Parquet compression optimization
- `create_data_models` - SQLAlchemy ORM model design

### Key Output Fields
- `validated_dataset` - Validation results with quality_score
- `compression_metrics` - Compression ratio, space savings
- `api_metrics` - Provider latency, rate limits
- `data_models_created` - ORM model metadata

### Failure Details
- `failure_type` - Category (data_quality_failure, api_error, timeout)
- `invalid_records` - Sample of problematic data
- `consistency_violations` - Rule violations with severity
- `recovery_guidance` - Suggested remediation steps
