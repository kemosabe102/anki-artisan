# OHLCV Data Quality Standards & Domain Knowledge

**Category**: domain-specific
**Domain**: Financial market data (OHLCV time-series)
**Confidence**: 0.95
**Last Updated**: 2025-11-14T00:00:00Z
**Agent**: market-data-specialist

---

## Overview

This documentation provides comprehensive OHLCV (Open, High, Low, Close, Volume) domain expertise for the market-data-specialist agent, covering industry-standard data quality validation, missing data handling strategies, and corporate actions adjustment methodologies.

**Key Concepts**:

- **OHLCV Data**: Time-series financial data representing price movements (Open, High, Low, Close) and trading activity (Volume) over discrete time intervals
- **Data Quality Standards**: FINRA Rule 6893 compliance requirements (timeliness, accuracy, integrity, completeness)
- **Corporate Actions**: Stock splits, dividends, and other events requiring retroactive price adjustments to maintain comparability

---

## Core Frameworks

### Framework 1: OHLCV Data Quality Standards

**Purpose**: Ensure financial data integrity through systematic validation of OHLCV time-series data against industry-standard consistency rules and format requirements.

**When to Use**:

- Before processing any OHLCV dataset (ingestion, transformation, analysis)
- After data retrieval from external sources (APIs, databases, files)
- During data pipeline validation (ETL, streaming, batch processing)
- Pre-delivery quality gates for downstream consumers

**Components**:

1. **Field Requirements (8 Critical Fields)**:
   - **Open**: Opening price for the time period
   - **High**: Highest price during the time period
   - **Low**: Lowest price during the time period
   - **Close**: Closing price for the time period
   - **Volume**: Number of shares/contracts traded
   - **Date/Timestamp**: ISO 8601 UTC timestamp (YYYY-MM-DDTHH:MM:SSZ)
   - **AdjClose**: Adjusted closing price (corporate actions applied)
   - **Ticker**: Stock symbol (1-5 uppercase characters, alphanumeric)

2. **Consistency Rules (7 Critical Validations)**:
   - **Rule 1**: High ≥ max(Open, Close) — High must be at least as large as both Open and Close
   - **Rule 2**: Low ≤ min(Open, Close) — Low must be at most as small as both Open and Close
   - **Rule 3**: High ≥ Low — High cannot be less than Low
   - **Rule 4**: Volume ≥ 0 — Volume cannot be negative
   - **Rule 5**: No negative prices — Open, High, Low, Close, AdjClose must all be ≥ 0
   - **Rule 6**: Chronological ordering — Timestamps must be strictly increasing
   - **Rule 7**: Valid ticker format — 1-5 uppercase alphanumeric characters

3. **Compliance Standards**:
   - **FINRA Rule 6893**: Market data integrity requirements (timeliness, accuracy, integrity, completeness)
   - **ISO 8601**: Timestamp format standard (UTC timezone, unambiguous representation)
   - **CRSP Standards**: Adjusted close methodology for corporate actions

**How to Apply**:

1. **Pre-Flight Validation**: Check all 8 fields present and non-null
2. **Type Validation**: Verify numeric types (float64) for prices/volume, datetime64 for timestamps, string for ticker
3. **Consistency Validation**: Apply all 7 rules sequentially, flag violations with row index and failed rule
4. **Format Validation**: Verify ISO 8601 timestamp format, uppercase ticker format
5. **Reporting**: Generate validation report with pass/fail status, violation counts, and detailed error list

**Validation Example**:

```python
# Example validation implementation (pseudo-code for AI readability)

def validate_ohlcv(df):
    """Validate OHLCV data against all 7 consistency rules."""
    violations = []

    # Rule 1: High >= max(Open, Close)
    violations.extend(df[df['High'] < df[['Open', 'Close']].max(axis=1)].index)

    # Rule 2: Low <= min(Open, Close)
    violations.extend(df[df['Low'] > df[['Open', 'Close']].min(axis=1)].index)

    # Rule 3: High >= Low
    violations.extend(df[df['High'] < df['Low']].index)

    # Rule 4: Volume >= 0
    violations.extend(df[df['Volume'] < 0].index)

    # Rule 5: No negative prices
    for col in ['Open', 'High', 'Low', 'Close', 'AdjClose']:
        violations.extend(df[df[col] < 0].index)

    # Rule 6: Chronological ordering
    violations.extend(df[df['Timestamp'].diff() <= pd.Timedelta(0)].index)

    # Rule 7: Valid ticker format
    violations.extend(df[~df['Ticker'].str.match(r'^[A-Z0-9]{1,5}$')].index)

    return {
        'status': 'PASS' if len(violations) == 0 else 'FAIL',
        'violations': list(set(violations)),
        'total_rows': len(df),
        'violation_rate': len(set(violations)) / len(df)
    }
```

**Source**: [FINRA Rule 6893](https://www.finra.org/rules-guidance/rulebooks/finra-rules/6893), [ISO 8601 Standard](https://www.iso.org/iso-8601-date-and-time-format.html)

---

### Framework 2: Missing Data Handling Strategies

**Purpose**: Apply time-series best practices for handling missing OHLCV data while preserving data integrity and avoiding look-ahead bias.

**When to Use**:

- Encountering NaN/null values in OHLCV datasets
- Dealing with trading halts, market closures, or gaps in data feeds
- Preparing data for downstream analysis requiring complete time-series
- Balancing data completeness vs. accuracy trade-offs

**Components**:

1. **Forward Fill (LOCF - Last Observation Carried Forward)** [PRIMARY]:
   - **Description**: Propagate previous valid value forward to fill gaps
   - **Use Case**: Non-trading days, temporary data feed outages
   - **Assumption**: Price/volume remains stable during gap period
   - **Limitation**: Can extend stale data too far; max gap threshold recommended (e.g., 5 bars)

2. **Backward Fill (NOCB - Next Observation Carried Backward)** [SECONDARY]:
   - **Description**: Propagate next valid value backward to fill gaps
   - **Use Case**: End-of-series gaps where forward fill unavailable
   - **Risk**: CREATES LOOK-AHEAD BIAS — use cautiously, only for non-predictive contexts
   - **Limitation**: Should NOT be used for trading strategies or backtesting

3. **Omission with Flagging** [CONSERVATIVE]:
   - **Description**: Leave NaN in place, add boolean flag column (e.g., 'is_missing')
   - **Use Case**: When no trading occurred (legitimate market closure)
   - **Benefit**: Preserves data integrity, allows downstream consumers to make informed decisions
   - **Implementation**: Add 'data_quality_flag' column with values: 'valid', 'forward_filled', 'missing'

4. **Linear Interpolation** [USE CAUTIOUSLY]:
   - **Description**: Fill gaps by linearly interpolating between surrounding valid values
   - **Use Case**: Very short gaps (1-2 bars) in high-frequency data
   - **Risk**: Introduces artificial data points, can create misleading patterns
   - **Limitation**: Should NOT be used for volume (volume interpolation is meaningless)

**How to Apply**:

1. **Gap Analysis**: Identify all NaN values, calculate gap sizes (consecutive missing bars)
2. **Strategy Selection**: Use decision tree (see below) to select appropriate strategy
3. **Application**: Apply selected strategy with metadata tracking (which rows were filled, using which method)
4. **Validation**: Verify no new consistency rule violations introduced (e.g., interpolation creating High < Low)
5. **Documentation**: Log all filling operations with timestamp, method, affected row indices

**Example Execution**:

```python
# Recommended missing data handling workflow

def handle_missing_data(df):
    """Apply tiered missing data strategy with metadata tracking."""
    df['data_quality_flag'] = 'valid'

    # Strategy 1: Forward fill for gaps <= 5 bars
    mask_small_gaps = df['Close'].isna() & (df['Close'].isna().groupby(df['Close'].notna().cumsum()).transform('size') <= 5)
    df.loc[mask_small_gaps, 'Close'] = df['Close'].fillna(method='ffill')
    df.loc[mask_small_gaps, 'data_quality_flag'] = 'forward_filled'

    # Strategy 2: Flag remaining gaps as missing
    df.loc[df['Close'].isna(), 'data_quality_flag'] = 'missing'

    return df
```

**Source**: [Time-Series Best Practices](https://otexts.com/fpp2/missing-outliers.html), Financial Data Quality Standards

---

### Framework 3: Corporate Actions Adjustment Calculations

**Purpose**: Maintain price comparability across time by retroactively adjusting historical prices for stock splits, dividends, and other corporate actions following CRSP standards.

**When to Use**:

- Calculating adjusted close prices (AdjClose field)
- Preparing data for backtesting trading strategies
- Creating price charts with historical comparability
- Generating returns calculations that account for corporate actions

**Components**:

1. **Stock Split Adjustment**:
   - **Formula**: `adjusted_price = price × (1 / split_ratio)`
   - **Example**: 2-for-1 split → split_ratio = 2 → adjusted_price = price × 0.5
   - **Direction**: Retroactive (adjust all prices BEFORE split date)
   - **Fields Affected**: Open, High, Low, Close (Volume adjusted inversely: volume × split_ratio)

2. **Dividend Adjustment**:
   - **Formula**: `adjusted_price = price × (1 - dividend / close_price_on_ex_date)`
   - **Example**: $1 dividend, $50 close → adjustment_factor = 1 - (1/50) = 0.98
   - **Direction**: Retroactive (adjust all prices BEFORE ex-dividend date)
   - **Fields Affected**: Open, High, Low, Close (Volume NOT adjusted)

3. **CRSP Adjustment Methodology**:
   - **Cumulative Adjustments**: Apply splits and dividends in chronological order, compounding adjustment factors
   - **Ex-Date vs. Record Date**: Use ex-dividend date (when stock trades without dividend), not record date
   - **Precision**: Maintain at least 6 decimal places during calculations to avoid rounding errors

**How to Apply**:

1. **Data Collection**: Gather all corporate actions with dates, types (split/dividend), and values
2. **Chronological Sort**: Order corporate actions from most recent to oldest
3. **Iterative Adjustment**: Start from most recent action, work backward:
   - For each action, identify all rows with timestamp < action_date
   - Apply adjustment formula to affected price fields
   - Maintain cumulative adjustment factor for audit trail
4. **Validation**: Verify no negative prices introduced, check High >= Low still holds
5. **Metadata**: Store original unadjusted prices in separate column for reference

**Validation Example**:

```python
# Corporate actions adjustment implementation

def apply_split_adjustment(df, split_date, split_ratio):
    """Apply stock split adjustment to historical prices."""
    mask = df['Timestamp'] < split_date

    # Adjust prices (divide by split ratio)
    for col in ['Open', 'High', 'Low', 'Close', 'AdjClose']:
        df.loc[mask, col] = df.loc[mask, col] / split_ratio

    # Adjust volume (multiply by split ratio)
    df.loc[mask, 'Volume'] = df.loc[mask, 'Volume'] * split_ratio

    # Track adjustment
    df.loc[mask, 'adjustment_factor'] = df.loc[mask, 'adjustment_factor'].fillna(1.0) / split_ratio

    return df

def apply_dividend_adjustment(df, ex_date, dividend_amount, close_price_on_ex_date):
    """Apply dividend adjustment to historical prices."""
    adjustment_factor = 1 - (dividend_amount / close_price_on_ex_date)
    mask = df['Timestamp'] < ex_date

    # Adjust prices (multiply by adjustment factor)
    for col in ['Open', 'High', 'Low', 'Close', 'AdjClose']:
        df.loc[mask, col] = df.loc[mask, col] * adjustment_factor

    # Track adjustment
    df.loc[mask, 'adjustment_factor'] = df.loc[mask, 'adjustment_factor'].fillna(1.0) * adjustment_factor

    return df
```

**Source**: [CRSP Adjustment Methodology](https://www.crsp.org/products/documentation/crsp-calculations), [StockCharts Technical Note](https://school.stockcharts.com/doku.php?id=data#adjustment_for_dividends_and_splits)

---

## Processes & Workflows

### Workflow 1: OHLCV Data Ingestion & Validation Pipeline

**Trigger Conditions**:

- New OHLCV data received from external source (API, file upload, database)
- Scheduled batch processing job (daily market data refresh)
- On-demand data retrieval for analysis or backtesting

**Steps**:

1. **Raw Data Acquisition**:
   - **Input**: Data source identifier (API endpoint, file path, database query)
   - **Output**: Raw DataFrame with timestamp, ticker, OHLCV fields
   - **Rationale**: Centralize data acquisition logic for consistency across sources

2. **Schema Validation**:
   - **Input**: Raw DataFrame
   - **Output**: Schema-validated DataFrame or validation error report
   - **Rationale**: Ensure all 8 critical fields present with correct data types before processing

3. **Consistency Rule Validation**:
   - **Input**: Schema-validated DataFrame
   - **Output**: Validation report with pass/fail status and violation details
   - **Rationale**: Detect data quality issues early, prevent downstream corruption

4. **Missing Data Handling**:
   - **Input**: Validated DataFrame with potential NaN values
   - **Output**: DataFrame with missing data strategy applied and metadata flags
   - **Rationale**: Ensure complete time-series for analysis while preserving integrity

5. **Corporate Actions Adjustment**:
   - **Input**: DataFrame + corporate actions event list
   - **Output**: DataFrame with AdjClose calculated and historical prices adjusted
   - **Rationale**: Maintain price comparability for accurate returns calculation

6. **Final Validation & Storage**:
   - **Input**: Fully processed DataFrame
   - **Output**: Storage confirmation + data quality report
   - **Rationale**: Verify no new violations introduced during processing, persist with audit trail

**Success Criteria**:

- ✅ All 7 consistency rules pass validation (100% compliance)
- ✅ Missing data rate < 5% OR all gaps handled with appropriate strategy
- ✅ Corporate actions applied correctly (audit trail verifiable)
- ✅ Timestamp format ISO 8601 UTC compliant
- ✅ Data quality metadata attached (flags, adjustment factors)

**Failure Handling**:

- If schema validation fails → Reject data, log error with source details, notify user
- If consistency validation fails → Quarantine data, generate violation report, escalate to manual review
- If missing data rate > 10% → Flag as low-quality dataset, require user approval before processing
- If corporate actions data missing → Skip adjustment step, flag AdjClose as unavailable

**Example Execution**:

```text
Input: CSV file with 252 rows (1 year daily data for AAPL)
Step 1: Load CSV → 252 rows, 8 columns
Step 2: Schema validation → PASS (all fields present, correct types)
Step 3: Consistency validation → FAIL (3 violations: rows 45, 87, 201 have High < Close)
Step 4: Data cleaning → Remove 3 invalid rows, apply forward fill for 2 NaN gaps
Step 5: Corporate actions → Apply 2-for-1 split on 2024-08-15, adjust 156 historical rows
Step 6: Final validation → PASS (249 rows, 100% compliance)
Output: Stored in database with data_quality_flag metadata
```

---

## Decision Trees

### Decision 1: Missing Data Strategy Selection

```
IF gap_size == 0 (no missing data)
  THEN no action required
  BECAUSE data is complete

ELSE IF gap_size <= 5 bars AND context == 'trading strategy'
  THEN apply forward fill (LOCF)
  BECAUSE small gaps likely due to non-trading days, forward fill preserves integrity without look-ahead bias

ELSE IF gap_size <= 5 bars AND context == 'exploratory analysis'
  THEN apply forward fill OR linear interpolation (prices only, NOT volume)
  BECAUSE analysis context allows slight smoothing, but volume interpolation is meaningless

ELSE IF gap_size > 5 bars AND gap_size <= 20 bars
  THEN omit with flagging (add 'is_missing' metadata)
  BECAUSE large gaps indicate data quality issues, better to preserve integrity than fabricate data

ELSE IF gap_size > 20 bars
  THEN escalate to user for manual decision
  BECAUSE dataset may be fundamentally incomplete, requires domain judgment

SPECIAL CASE: end-of-series gap AND no future data available
  THEN omit with flagging (DO NOT backward fill for predictive contexts)
  BECAUSE backward fill creates look-ahead bias, violates causality
```

**Example Scenarios**:

1. **Scenario**: 2-day gap in daily data, trading strategy context → **Decision**: Forward fill (LOCF)
2. **Scenario**: 15-day gap in daily data, exploratory analysis → **Decision**: Omit with flagging
3. **Scenario**: 1-bar gap in 5-minute data, visualization context → **Decision**: Linear interpolation (prices only)
4. **Scenario**: 30-day gap in daily data → **Decision**: Escalate to user, likely data source failure

---

### Decision 2: Data Quality Validation Threshold

```
IF validation_pass_rate >= 0.99 (99%+ compliance)
  THEN ACCEPT data, proceed to storage
  BECAUSE high-quality dataset, minor violations acceptable

ELSE IF validation_pass_rate >= 0.95 AND violation_type == 'timestamp_format'
  THEN ACCEPT with warning, apply timestamp normalization
  BECAUSE format issues are correctable, data integrity intact

ELSE IF validation_pass_rate >= 0.95 AND violation_type == 'price_consistency'
  THEN QUARANTINE data, flag for manual review
  BECAUSE price violations indicate fundamental data quality issues

ELSE IF validation_pass_rate < 0.95
  THEN REJECT data, log error, notify user
  BECAUSE low-quality dataset poses risk to downstream analysis

SPECIAL CASE: validation_pass_rate == 1.0 AND source == 'untrusted_api'
  THEN apply additional sanity checks (price range, volume outliers)
  BECAUSE perfect scores from untrusted sources may indicate synthetic/manipulated data
```

**Example Scenarios**:

1. **Scenario**: 98% pass rate, 5 timestamp format violations → **Decision**: ACCEPT with normalization
2. **Scenario**: 92% pass rate, 20 High < Close violations → **Decision**: REJECT dataset
3. **Scenario**: 100% pass rate from new API source → **Decision**: Apply outlier detection before acceptance

---

## Best Practices

### Practice 1: Always Validate Before Processing

**Principle**: Never trust external data sources — apply systematic validation at ingestion boundaries to prevent downstream corruption.

**Implementation**:

- Use schema validation as first gate (fail fast on missing/mistyped fields)
- Apply all 7 consistency rules sequentially, report ALL violations (not just first failure)
- Generate detailed validation reports with row indices and specific rule violations
- Implement validation as reusable function/module for consistency across pipelines

**Benefits**:

- ✅ Early detection of data quality issues (before expensive processing)
- ✅ Audit trail for compliance and debugging
- ✅ Prevents propagation of corrupt data to downstream systems

**Trade-offs**:

- ⚠️ Adds processing overhead (~5-10% latency for large datasets)
- ⚠️ May reject datasets with minor correctable issues (requires tuning thresholds)

**Example**:

```python
# Validation-first pipeline pattern

def ingest_ohlcv_data(source, config):
    """Ingest OHLCV data with mandatory validation gates."""
    # 1. Acquire raw data
    raw_df = fetch_data(source)

    # 2. Schema validation (GATE 1)
    schema_valid, schema_errors = validate_schema(raw_df)
    if not schema_valid:
        raise ValidationError(f"Schema validation failed: {schema_errors}")

    # 3. Consistency validation (GATE 2)
    consistency_report = validate_consistency_rules(raw_df)
    if consistency_report['pass_rate'] < config['min_pass_rate']:
        raise ValidationError(f"Consistency validation failed: {consistency_report}")

    # 4. Proceed with processing only after all gates passed
    return process_data(raw_df)
```

---

### Practice 2: Preserve Original Data with Adjustment Metadata

**Principle**: When applying corporate actions adjustments, maintain both original unadjusted prices and cumulative adjustment factors for auditability and flexibility.

**Implementation**:

- Store original prices in separate columns (e.g., 'Close_Unadjusted', 'Close_Adjusted')
- Track cumulative adjustment factor for each row (compounded splits and dividends)
- Include adjustment event metadata (date, type, value) in separate table linked by ticker
- Allow downstream consumers to choose adjusted vs. unadjusted data based on use case

**Benefits**:

- ✅ Audit trail for regulatory compliance
- ✅ Flexibility for different analysis contexts (some require unadjusted prices)
- ✅ Ability to revert or recalculate adjustments if corporate actions data corrected

**Trade-offs**:

- ⚠️ Increased storage requirements (~30% more space)
- ⚠️ Potential confusion for users unfamiliar with adjusted vs. unadjusted distinction

**Example**:

```python
# Dual-storage pattern for adjusted prices

def apply_adjustments_with_metadata(df, corporate_actions):
    """Apply adjustments while preserving original prices."""
    # Store original prices
    df['Close_Unadjusted'] = df['Close'].copy()
    df['adjustment_factor'] = 1.0

    # Apply adjustments iteratively
    for action in corporate_actions:
        if action['type'] == 'split':
            df = apply_split_adjustment(df, action['date'], action['ratio'])
        elif action['type'] == 'dividend':
            df = apply_dividend_adjustment(df, action['ex_date'], action['amount'], action['close_price'])

    # Calculate adjusted close
    df['Close_Adjusted'] = df['Close_Unadjusted'] * df['adjustment_factor']

    return df
```

---

### Practice 3: Use ISO 8601 UTC Timestamps Exclusively

**Principle**: Standardize all timestamps to ISO 8601 UTC format to avoid timezone ambiguity, daylight saving issues, and cross-system compatibility problems.

**Implementation**:

- Convert all incoming timestamps to UTC at ingestion boundary
- Store timestamps as ISO 8601 strings (YYYY-MM-DDTHH:MM:SSZ) or datetime64[ns, UTC] in pandas
- Include 'Z' suffix to explicitly indicate UTC timezone
- Reject data with ambiguous timezone information or local time without offset

**Benefits**:

- ✅ Eliminates timezone-related bugs (major source of financial data errors)
- ✅ Enables correct chronological sorting across markets in different timezones
- ✅ Compliance with international standards (ISO 8601)

**Trade-offs**:

- ⚠️ Requires timezone conversion logic at display layer for user-facing applications
- ⚠️ May lose original timezone information from source (requires separate metadata if needed)

**Example**:

```python
# Timestamp normalization pattern

def normalize_timestamps(df, timestamp_col='Timestamp'):
    """Convert all timestamps to ISO 8601 UTC."""
    # Parse timestamps with timezone awareness
    df[timestamp_col] = pd.to_datetime(df[timestamp_col], utc=True)

    # Verify UTC timezone
    if df[timestamp_col].dt.tz is None:
        raise ValueError("Timestamps must be timezone-aware")

    # Convert to ISO 8601 string representation
    df[timestamp_col + '_iso8601'] = df[timestamp_col].dt.strftime('%Y-%m-%dT%H:%M:%SZ')

    return df
```

---

## Anti-Patterns

### Anti-Pattern 1: Backward Fill for Predictive Contexts

**Problem**: Using backward fill (NOCB) to handle missing data in trading strategies or backtesting creates look-ahead bias, where future information influences past decisions.

**Detection**:

- 🔴 Missing data handling code uses `fillna(method='bfill')` or `shift(-1)` in strategy/backtest context
- 🔴 Data quality flags show 'backward_filled' values used in signal generation
- 🔴 Backtest results show unrealistic accuracy (perfect prediction of gaps)

**Consequences**:

- ❌ Trading strategy performance will be artificially inflated in backtests
- ❌ Live trading will fail catastrophically (future data not available in real-time)
- ❌ Violates causality principle (past cannot depend on future)

**Better Approach**:

```python
✅ Preferred Pattern (Forward Fill or Omit):
df['Close_filled'] = df['Close'].fillna(method='ffill')  # Use last known value
# OR
df = df.dropna(subset=['Close'])  # Omit missing data entirely

❌ Anti-Pattern (Backward Fill):
df['Close_filled'] = df['Close'].fillna(method='bfill')  # LOOK-AHEAD BIAS!
```

**Migration Strategy**:

1. Audit all existing data pipelines for `bfill`, `shift(-1)`, or backward-looking operations
2. Replace with forward fill (LOCF) or omission with flagging strategies
3. Re-run backtests with corrected data to establish realistic performance baselines
4. Add validation check to reject backward fill in strategy contexts

---

### Anti-Pattern 2: Volume Interpolation

**Problem**: Applying linear interpolation or other smoothing techniques to fill missing volume data creates artificial trading activity that never occurred.

**Detection**:

- 🔴 Missing data handling code applies interpolation to 'Volume' column
- 🔴 Volume values show unrealistic smoothness (no natural spikiness)
- 🔴 Volume sum across interpolated period doesn't match exchange-reported totals

**Consequences**:

- ❌ Volume-based indicators (VWAP, OBV, Volume MA) will produce incorrect signals
- ❌ Liquidity analysis will be fundamentally flawed
- ❌ Trading cost models will underestimate slippage/market impact

**Better Approach**:

```python
✅ Preferred Pattern (Forward Fill or Zero):
df['Volume_filled'] = df['Volume'].fillna(method='ffill')  # Carry forward last known volume
# OR (for non-trading days)
df['Volume_filled'] = df['Volume'].fillna(0)  # Zero volume on non-trading days

❌ Anti-Pattern (Interpolation):
df['Volume_filled'] = df['Volume'].interpolate(method='linear')  # CREATES FAKE TRADING ACTIVITY!
```

**Migration Strategy**:

1. Identify all pipelines applying interpolation to volume data
2. Replace with forward fill (conservative) or zero fill (for known non-trading days)
3. Add validation rule: volume must be integer (interpolation creates floats)
4. Document volume filling strategy in data quality metadata

---

### Anti-Pattern 3: Skipping Validation for "Trusted" Sources

**Problem**: Assuming data from reputable providers (Bloomberg, Reuters, exchanges) is always correct without validation can lead to silent data corruption.

**Detection**:

- 🔴 Pipeline code path bypasses validation for specific data sources
- 🔴 Configuration has 'skip_validation: true' flag for certain providers
- 🔴 Data quality reports show 100% pass rate with no variation over time

**Consequences**:

- ❌ Data quality issues go undetected until downstream systems fail
- ❌ No audit trail when errors are discovered (can't trace back to source)
- ❌ False confidence in data integrity leads to incorrect decisions

**Better Approach**:

```python
✅ Preferred Pattern (Always Validate):
def ingest_data(source):
    raw_df = fetch_from_provider(source)

    # Validate regardless of source reputation
    validation_report = validate_all_rules(raw_df)

    if not validation_report['passed']:
        log_error(f"Validation failed for {source}: {validation_report}")
        notify_data_quality_team(validation_report)

    return raw_df, validation_report

❌ Anti-Pattern (Skip Validation):
def ingest_data(source):
    raw_df = fetch_from_provider(source)

    if source in TRUSTED_PROVIDERS:
        return raw_df  # ASSUMES PERFECTION!
    else:
        return validate_all_rules(raw_df)
```

**Migration Strategy**:

1. Remove all 'skip_validation' flags and trusted provider bypass logic
2. Apply uniform validation to all data sources (no exceptions)
3. Tune validation thresholds based on historical source quality (relaxed for high-quality sources, strict for low-quality)
4. Monitor validation failures by source to identify problematic providers

---

## Integration Points

### Integration 1: Data Ingestion Pipeline (ETL)

**Relationship**: Market-data-specialist provides validation and quality assurance layer for upstream ETL processes.

**Coordination Pattern**:

- ETL extracts raw OHLCV data from sources → passes to market-data-specialist for validation
- Market-data-specialist returns validation report + cleaned data OR rejection notice
- ETL loads validated data into storage systems (databases, data lakes) with quality metadata

**Example Usage**:

```text
ETL Workflow:
1. Extract: Fetch OHLCV from API (yfinance, Alpha Vantage, proprietary feeds)
2. Validate: Call market-data-specialist validation suite
   - Input: Raw DataFrame
   - Output: ValidationReport(status='PASS', violations=[], cleaned_df=...)
3. Transform: Apply corporate actions adjustments, feature engineering
4. Load: Store in TimescaleDB with data_quality_flag metadata
```

**Dependencies**:

- **Upstream**: Data source APIs, file storage systems, message queues
- **Downstream**: Time-series databases (TimescaleDB, InfluxDB), data lakes (S3, GCS), ML pipelines

---

### Integration 2: Trading Strategy Backtesting Engine

**Relationship**: Market-data-specialist ensures backtesting accuracy by providing properly validated and adjusted OHLCV data.

**Coordination Pattern**:

- Backtesting engine requests historical data for specific ticker/date range
- Market-data-specialist retrieves data, applies validation and adjustments
- Returns adjusted close prices with quality flags for strategy evaluation
- Backtesting engine filters data based on quality flags (e.g., exclude 'missing' or 'low_confidence' bars)

**Example Usage**:

```text
Backtest Workflow:
1. Request: Strategy requests AAPL data 2020-2025, daily frequency
2. Retrieval: Market-data-specialist fetches from storage
3. Validation: Apply consistency rules, flag 3 gaps (data_quality_flag='forward_filled')
4. Adjustment: Apply 2 splits, 8 dividends → calculate AdjClose
5. Delivery: Return DataFrame with quality metadata
6. Execution: Strategy runs on AdjClose, filters out 'missing' bars
```

**Dependencies**:

- **Backtesting engine depends on**: Validated adjusted prices, quality flags, corporate actions metadata
- **Market-data-specialist depends on**: Corporate actions database, historical price storage

---

### Integration 3: Real-Time Market Data Streaming

**Relationship**: Market-data-specialist validates incoming real-time data streams for live trading systems.

**Coordination Pattern**:

- Streaming platform (Kafka, Kinesis) publishes real-time OHLCV bars
- Market-data-specialist consumer validates each incoming bar (low-latency validation)
- Publishes validated bars to downstream topic OR alerts on validation failures
- Monitoring system tracks validation pass rate in real-time

**Example Usage**:

```text
Streaming Workflow:
1. Producer: Exchange publishes 1-minute OHLCV bars to Kafka topic 'market-data-raw'
2. Validator: Market-data-specialist consumer subscribes to 'market-data-raw'
3. Processing: For each bar, apply lightweight validation (7 consistency rules, <10ms latency)
4. Decision: IF valid → publish to 'market-data-validated' | IF invalid → publish to 'market-data-alerts'
5. Monitoring: Track validation_pass_rate metric (alert if drops below 95%)
```

**Dependencies**:

- **Upstream**: Message broker (Kafka, Kinesis), exchange APIs
- **Downstream**: Live trading systems, monitoring dashboards, alerting services

---

## Validation & Quality Checks

### Check 1: Consistency Rules Compliance

**What to Validate**: All 7 OHLCV consistency rules applied to every row in dataset.

**Validation Method**:

1. Iterate through DataFrame, apply each rule as boolean mask
2. Collect row indices where rule violated
3. Calculate pass rate: (total_rows - violations) / total_rows

**Pass Criteria**: pass_rate ≥ 0.99 (99%+ compliance)
**Fail Criteria**: pass_rate < 0.95 OR any critical field missing

**Remediation**: If validation fails → quarantine data, generate detailed violation report with specific row indices and failed rules, escalate to manual review

---

### Check 2: Corporate Actions Adjustment Integrity

**What to Validate**: Adjusted close prices calculated correctly with audit trail for all corporate actions.

**Validation Method**:

1. Recalculate AdjClose independently using stored corporate actions events
2. Compare recalculated values to stored AdjClose (tolerance: 0.01%)
3. Verify adjustment_factor column matches expected cumulative adjustments
4. Check no negative prices introduced by adjustments

**Pass Criteria**: 100% of AdjClose values match recalculation within 0.01% tolerance
**Fail Criteria**: Any discrepancy > 0.01% OR negative adjusted prices

**Remediation**: If validation fails → recompute all adjustments from scratch, update stored AdjClose, log correction in audit table

---

### Check 3: Missing Data Strategy Metadata

**What to Validate**: All filled gaps documented with data_quality_flag metadata indicating fill strategy used.

**Validation Method**:

1. Identify all rows where original data had NaN values (compare to raw ingestion log)
2. Verify each filled row has data_quality_flag ∈ {'forward_filled', 'interpolated', 'backward_filled'}
3. Check no backward fills exist for predictive contexts (strategy/backtest data)
4. Validate gap sizes match documented thresholds (e.g., forward fill only for gaps ≤5)

**Pass Criteria**: 100% of filled gaps have metadata, no backward fills in predictive contexts
**Fail Criteria**: Any filled gap missing metadata OR backward fill detected in strategy data

**Remediation**: If validation fails → reprocess data with correct metadata attachment, audit existing datasets for compliance

---

## Common Pitfalls & Solutions

| Pitfall                                    | Detection                                          | Solution                                                      |
| ------------------------------------------ | -------------------------------------------------- | ------------------------------------------------------------- |
| Timezone inconsistency                     | Timestamps show different timezone offsets         | Standardize to ISO 8601 UTC at ingestion boundary             |
| Volume interpolation                       | Volume values are non-integer or unrealistically smooth | Use forward fill or zero fill, never interpolate volume       |
| Skipping validation for trusted sources    | 100% pass rate with no variance over time          | Apply validation to ALL sources regardless of reputation      |
| Backward fill in backtesting               | Unrealistic backtest accuracy                      | Use forward fill or omit missing data entirely                |
| Rounding errors in corporate actions       | Adjusted prices don't match reference data         | Use at least 6 decimal places in adjustment calculations      |
| Missing corporate actions data             | AdjClose doesn't match unadjusted Close            | Query corporate actions database, flag if unavailable         |
| Non-trading days counted as missing data   | High missing_data_rate for legitimate market closures | Identify market calendar, flag non-trading days separately    |
| Stale data from forward fill               | 20+ consecutive bars with identical values         | Set max gap threshold (e.g., 5 bars) for forward fill         |

---

## Tools & Resources

### Recommended Tools

1. **pandas**
   - **Purpose**: DataFrame manipulation, time-series analysis
   - **When to Use**: All OHLCV data processing tasks
   - **Documentation**: <https://pandas.pydata.org/docs/>

2. **yfinance**
   - **Purpose**: Historical OHLCV data retrieval from Yahoo Finance
   - **When to Use**: Backtesting, research, prototyping (NOT production trading)
   - **Documentation**: <https://github.com/ranaroussi/yfinance>

3. **pandas_market_calendars**
   - **Purpose**: Market trading calendar (identify non-trading days)
   - **When to Use**: Distinguishing missing data from market closures
   - **Documentation**: <https://github.com/rsheftel/pandas_market_calendars>

4. **Great Expectations**
   - **Purpose**: Data validation and quality monitoring
   - **When to Use**: Production data pipelines requiring comprehensive validation suites
   - **Documentation**: <https://docs.greatexpectations.io/>

### Learning Resources

1. **FINRA Rule 6893 - Market Data Integrity**: <https://www.finra.org/rules-guidance/rulebooks/finra-rules/6893>
   - **Topic**: Regulatory requirements for market data quality (timeliness, accuracy, integrity, completeness)
   - **Quality**: High (official regulatory source)

2. **CRSP Calculations Guide**: <https://www.crsp.org/products/documentation/crsp-calculations>
   - **Topic**: Standard methodology for corporate actions adjustments (splits, dividends)
   - **Quality**: High (industry-standard reference)

3. **ISO 8601 Date and Time Format**: <https://www.iso.org/iso-8601-date-and-time-format.html>
   - **Topic**: International standard for timestamp representation
   - **Quality**: High (official ISO standard)

4. **StockCharts Technical Notes - Data Adjustments**: <https://school.stockcharts.com/doku.php?id=data#adjustment_for_dividends_and_splits>
   - **Topic**: Practical guide to price adjustments with examples
   - **Quality**: Medium (educational resource, widely referenced)

---

## Glossary

- **OHLCV**: Open, High, Low, Close, Volume — standard format for financial time-series data
- **Adjusted Close (AdjClose)**: Closing price retroactively adjusted for corporate actions (splits, dividends) to maintain comparability
- **Corporate Actions**: Events affecting stock price/structure (splits, dividends, mergers, spin-offs)
- **FINRA Rule 6893**: Regulatory requirement for market data integrity (timeliness, accuracy, integrity, completeness)
- **ISO 8601**: International standard for date/time representation (YYYY-MM-DDTHH:MM:SSZ format)
- **LOCF (Last Observation Carried Forward)**: Forward fill strategy for missing data
- **NOCB (Next Observation Carried Backward)**: Backward fill strategy for missing data
- **Look-Ahead Bias**: Using future information to influence past decisions (fatal flaw in backtesting)
- **CRSP**: Center for Research in Security Prices — provider of high-quality financial data and adjustment methodologies
- **Ex-Dividend Date**: Date when stock trades without upcoming dividend (used for adjustment calculations)
- **Split Ratio**: Factor by which shares are multiplied in stock split (e.g., 2-for-1 split = ratio of 2)
- **Data Quality Flag**: Metadata indicating data processing applied (e.g., 'valid', 'forward_filled', 'missing')

---

## Sources & References

1. FINRA Rule 6893 - Market Data Integrity: <https://www.finra.org/rules-guidance/rulebooks/finra-rules/6893>
   - Accessed: 2025-11-14
   - Confidence: 0.98 (official regulatory source)

2. ISO 8601 Date and Time Format: <https://www.iso.org/iso-8601-date-and-time-format.html>
   - Accessed: 2025-11-14
   - Confidence: 0.99 (international standard)

3. CRSP Calculations Guide: <https://www.crsp.org/products/documentation/crsp-calculations>
   - Accessed: 2025-11-14
   - Confidence: 0.95 (industry-standard methodology)

4. StockCharts Technical Notes: <https://school.stockcharts.com/doku.php?id=data#adjustment_for_dividends_and_splits>
   - Accessed: 2025-11-14
   - Confidence: 0.85 (educational resource, widely referenced)

5. Time-Series Missing Data Handling: <https://otexts.com/fpp2/missing-outliers.html>
   - Accessed: 2025-11-14
   - Confidence: 0.90 (academic textbook reference)

---

## Changelog

- **2025-11-14**: Initial documentation created (confidence: 0.95) — OHLCV standards, missing data strategies, corporate actions adjustments based on research findings from researcher-external

---

## Related Documentation

- `.claude/agents/market-data-specialist.md`: Agent definition and capabilities
- `.claude/docs/guides/market-data-specialist/tool-usage-patterns.md`: Tool usage patterns for OHLCV processing
- `.claude/docs/guides/market-data-specialist/workflow-operations.md`: Workflow operations and delegation patterns
- `docs/00-project/SPEC.md`: System specification for gauntlet-agents project
