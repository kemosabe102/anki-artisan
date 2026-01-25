# Market Data Specialist - Delegation Examples

## Example 1: OHLCV Validation

**Orchestrator Input:**
```markdown
Task(market-data-specialist, 
  "Validate OHLCV data in data/raw/AAPL_daily_2024.csv.
   Apply all consistency rules. Quality threshold: 0.95.
   Quarantine invalid records to temp/market-data-specialist/quarantine/")
```

**Expected Output:**
```json
{
  "status": "SUCCESS",
  "agent": "market-data-specialist",
  "operation_type": "validate_ohlcv",
  "summary": "Validated 252 OHLCV records for AAPL. Quality score: 0.988 (3 minor violations quarantined).",
  "confidence": 0.95,
  "agent_specific_output": {
    "validated_dataset": {
      "total_records": 252,
      "valid_records": 249,
      "invalid_records": 3,
      "data_quality_score": 0.988,
      "date_range": {"start": "2024-01-02", "end": "2024-12-31"},
      "symbols": ["AAPL"]
    },
    "validation_results": {
      "consistency_checks_passed": ["high_gte_low", "volume_gte_zero", "chronological", "valid_ticker"],
      "consistency_checks_failed": [
        {"rule": "high_gte_close", "violation_count": 3, "sample_records": [...]}
      ]
    }
  }
}
```

---

## Example 2: API Connector Implementation

**Orchestrator Input:**
```markdown
Task(market-data-specialist,
  "Implement DataConnector for Polygon API.
   Follow protocol (fetch, health_check methods).
   Add circuit breaker: 5 failure threshold, 60s reset, 3 success threshold.
   Integrate with MultiAPIOrchestrator fallback chain.")
```

**Expected Output:**
```json
{
  "status": "SUCCESS",
  "agent": "market-data-specialist",
  "operation_type": "implement_connector",
  "summary": "Implemented PolygonConnector with circuit breaker. Protocol compliant, tested with mock responses.",
  "confidence": 0.92,
  "agent_specific_output": {
    "api_metrics": {
      "provider_used": "polygon",
      "fallback_attempts": 0,
      "response_time_ms": 145.3,
      "rate_limit_remaining": 995
    },
    "files_created": [
      "packages/connectors/market_data/polygon_connector.py"
    ]
  }
}
```

---

## Example 3: Parquet Compression Optimization

**Orchestrator Input:**
```markdown
Task(market-data-specialist,
  "Optimize Parquet storage for data/ohlcv/ directory.
   Target compression ratio: 0.70.
   Benchmark all codecs (snappy, gzip, lz4, zstd).
   Apply hybrid partitioning (year/month/ticker).
   Output to data/ohlcv_optimized/")
```

**Expected Output:**
```json
{
  "status": "SUCCESS",
  "agent": "market-data-specialist",
  "operation_type": "compress_dataset",
  "summary": "Achieved 68% compression using ZSTD level 1. Created 156 partitioned files.",
  "confidence": 0.90,
  "agent_specific_output": {
    "compression_metrics": {
      "compression_ratio": 0.68,
      "codec_used": "zstd",
      "file_size_before": 524288000,
      "file_size_after": 167772160,
      "space_saved_mb": 340.0
    },
    "parquet_files": [
      {"path": "data/ohlcv_optimized/year=2024/month=01/ticker=AAPL/part-0.parquet", "partition_key": "2024/01/AAPL", "row_count": 21, "file_size_bytes": 8192}
    ]
  }
}
```

---

## Example 4: SQLAlchemy Model Design

**Orchestrator Input:**
```markdown
Task(market-data-specialist,
  "Design SQLAlchemy ORM model for daily OHLCV data.
   Include composite primary key (trade_date, ticker).
   Add indexes for common query patterns (ticker-first, date-first).
   Define relationship to CompanyInfo table.
   Output to packages/core/data/models/ohlcv.py")
```

**Expected Output:**
```json
{
  "status": "SUCCESS",
  "agent": "market-data-specialist",
  "operation_type": "create_data_models",
  "summary": "Created DailyOHLCV model with composite PK and dual indexes. ORM only, no DDL.",
  "confidence": 0.95,
  "agent_specific_output": {
    "data_models_created": [
      {
        "model_name": "DailyOHLCV",
        "file_path": "packages/core/data/models/ohlcv.py",
        "table_name": "daily_ohlcv",
        "fields_count": 7
      }
    ]
  }
}
```

---

## Example 5: Failure Scenario - Data Quality Below Threshold

**Orchestrator Input:**
```markdown
Task(market-data-specialist,
  "Validate OHLCV data in data/raw/corrupted_feed.csv. Quality threshold: 0.95.")
```

**Expected Output:**
```json
{
  "status": "FAILURE",
  "agent": "market-data-specialist",
  "operation_type": "validate_ohlcv",
  "summary": "Data quality score 0.72 below threshold 0.95. 28% of records have consistency violations.",
  "confidence": 0.88,
  "failure_details": {
    "failure_type": "data_quality_failure",
    "reasons": [
      "Quality score 0.72 below threshold 0.95",
      "142 records violate High >= Close rule",
      "23 records have negative volume"
    ],
    "invalid_records": [
      {"record_index": 45, "violation_type": "consistency_violation", "violation_details": "High (150.50) < Close (152.30)"}
    ],
    "consistency_violations": [
      {"rule": "high_gte_close", "affected_records": 142, "severity": "critical"}
    ],
    "recovery_guidance": [
      "Quarantine invalid records for manual review",
      "Contact data provider about feed quality",
      "Consider lower quality threshold if data source is best available"
    ],
    "quarantine_path": "temp/market-data-specialist/quarantine/corrupted_feed_2024-01-15/"
  }
}
```

---

## Delegation Best Practices

1. **Specify quality thresholds** - Default is 0.95, adjust for data source reliability
2. **Include output paths** - Where to write Parquet files, models, quarantine data
3. **Mention fallback chain** - If implementing connectors, specify provider order
4. **Clarify ORM vs DDL** - Always emphasize "NO database DDL" for model design
5. **Check output observability** - Ensure execution_time_ms and api_calls are populated
