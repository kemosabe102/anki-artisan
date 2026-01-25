# Storage Optimization & Compression

**Category**: performance
**Domain**: Market data storage, time-series data compression, partitioning strategies
**Confidence**: 0.92
**Last Updated**: 2025-11-14T00:00:00Z
**Agent**: market-data-specialist

---

## Overview

This documentation covers storage optimization strategies for financial time-series data, including Parquet compression codec selection, partitioning strategies, SQLAlchemy model patterns, and API rate limiting. Proper storage optimization enables 70% compression targets while maintaining query performance and ensuring reliable data ingestion.

**Key Concepts**:

- **Parquet Compression Codec**: Algorithm used to compress columnar data (Snappy, LZ4, Gzip, ZSTD) - trade-off between compression ratio, read/write speed, and CPU usage
- **Partitioning Strategy**: Directory structure organization (date-based, ticker-based, hybrid) - impacts query pruning efficiency and I/O reduction
- **Exponential Backoff**: Retry pattern for transient API failures - prevents thundering herd, respects rate limits, maximizes success rate
- **Composite Primary Key**: Database indexing strategy for time-series data - ensures uniqueness and query performance on (date, ticker) combinations

---

## Core Frameworks

### Framework 1: Parquet Compression Codec Selection

**Purpose**: Select optimal compression codec to achieve 70% compression target while balancing read/write performance for financial time-series data ingestion and querying.

**When to Use**:

- Real-time data ingestion requiring fast writes (market data feeds, tick data)
- Cold storage archival with infrequent access (historical research datasets)
- Balanced production workloads with mixed read/write patterns (daily OHLCV data)

**Components**:

1. **Codec Options**: Snappy (fast), LZ4 (fastest), Gzip (maximum compression), ZSTD (balanced)
2. **Performance Metrics**: Compression ratio, write throughput (MB/s), read throughput (MB/s), CPU usage
3. **Trade-off Analysis**: Real-time vs archival, storage cost vs query performance

**How to Apply**:

1. Identify workload pattern (real-time ingestion, batch processing, archival storage)
2. Select codec using decision tree (see Decision Trees section)
3. Configure PyArrow writer with chosen codec and compression level
4. Validate compression ratio meets 70% target using sample data
5. Benchmark read/write performance against requirements

**Example from Codebase**:

```python
import pyarrow.parquet as pq
import pyarrow as pa

# ZSTD level 1 - RECOMMENDED for balanced production workloads
table = pa.Table.from_pandas(df)
pq.write_table(
    table,
    'market_data.parquet',
    compression='ZSTD',
    compression_level=1,  # 66% reduction, balanced performance
    use_dictionary=True,  # Enables dictionary encoding for repeated values
    write_statistics=True  # Enables query pruning
)

# Snappy - RECOMMENDED for real-time ingestion
pq.write_table(
    table,
    'realtime_ticks.parquet',
    compression='SNAPPY',  # 48% reduction, fastest read/write
    use_dictionary=True
)

# ZSTD level 19 - RECOMMENDED for cold storage
pq.write_table(
    table,
    'historical_archive.parquet',
    compression='ZSTD',
    compression_level=19,  # 71% reduction, slow writes (105 MB/s)
    use_dictionary=True
)
```text

**Performance Comparison**:

| Codec       | Compression Ratio | Write Speed | Read Speed  | Use Case              |
|-------------|-------------------|-------------|-------------|-----------------------|
| Snappy      | 48%               | Fast        | 2100 MB/s   | Real-time ingestion   |
| LZ4         | 52%               | Fastest     | 3850 MB/s   | Streaming data        |
| Gzip        | 64%               | Slow        | 300 MB/s    | Legacy compatibility  |
| ZSTD level 1| 66%               | Balanced    | 1400 MB/s   | **Production default**|
| ZSTD level 19| 71%              | Slowest     | 400 MB/s    | Cold storage          |

**Source**: PyArrow documentation (<https://arrow.apache.org/docs/python/parquet.html>), Uber engineering blog benchmarks

---

### Framework 2: Partitioning Strategy

**Purpose**: Organize Parquet files into directory structures that enable efficient query pruning and minimize I/O for common access patterns (temporal queries, ticker-specific analysis).

**When to Use**:

- Large datasets (>1GB per file or >100K rows) requiring query optimization
- Time-range queries (e.g., "all tickers for 2023-Q1")
- Single-ticker analysis (e.g., "AAPL historical data")
- Multi-dimensional slicing (e.g., "tech sector stocks for last month")

**Components**:

1. **Partition Keys**: Columns used for directory structure (year, month, day, ticker, sector)
2. **Partition Granularity**: Level of subdivision (daily, monthly, yearly)
3. **Query Pruning**: Metadata-based file skipping - reduces I/O by 80-95%

**How to Apply**:

1. Analyze query patterns (temporal range queries, ticker-specific queries, both)
2. Select partitioning strategy using decision tree (see Decision Trees section)
3. Configure PyArrow writer with partition columns
4. Create partitioned dataset directory structure
5. Query using dataset API with filters for automatic pruning

**Example from Codebase**:

```python
import pyarrow.parquet as pq
import pyarrow.dataset as ds

# Date-based partitioning (efficient for temporal queries)
pq.write_to_dataset(
    table,
    root_path='market_data/',
    partition_cols=['year', 'month', 'day'],
    compression='ZSTD',
    compression_level=1,
    existing_data_behavior='overwrite_or_ignore'
)
# Directory structure: market_data/year=2023/month=01/day=15/data.parquet

# Ticker-based partitioning (efficient for single-ticker queries)
pq.write_to_dataset(
    table,
    root_path='market_data/',
    partition_cols=['ticker'],
    compression='ZSTD',
    compression_level=1
)
# Directory structure: market_data/ticker=AAPL/data.parquet

# Hybrid partitioning (date→ticker) - RECOMMENDED
pq.write_to_dataset(
    table,
    root_path='market_data/',
    partition_cols=['year', 'month', 'ticker'],
    compression='ZSTD',
    compression_level=1
)
# Directory structure: market_data/year=2023/month=01/ticker=AAPL/data.parquet

# Query with automatic partition pruning
dataset = ds.dataset('market_data/', format='parquet', partitioning='hive')
filtered = dataset.filter(
    (ds.field('year') == 2023) &
    (ds.field('month') == 1) &
    (ds.field('ticker') == 'AAPL')
)
result = filtered.to_table().to_pandas()
# Only reads 1 file instead of all files - 99%+ I/O reduction
```text

**Partitioning Performance**:

| Strategy        | Temporal Query I/O | Ticker Query I/O | Hybrid Query I/O | Recommended For           |
|-----------------|--------------------|-----------------|--------------------|---------------------------|
| Date-based      | 80-95% reduction   | No pruning      | 80-95% reduction   | Time-range analysis       |
| Ticker-based    | No pruning         | 99% reduction   | 50% reduction      | Single-ticker analysis    |
| Hybrid (date→ticker) | 80-95% reduction | 99% reduction | 99% reduction      | **Production default**    |

**Source**: PyArrow partitioning documentation (<https://arrow.apache.org/docs/python/dataset.html>)

---

### Framework 3: SQLAlchemy Time-Series Model Patterns

**Purpose**: Design SQLAlchemy ORM models for financial time-series data with optimized indexing, composite primary keys, and relationship patterns for efficient querying.

**When to Use**:

- Defining database schemas for market data (OHLCV, ticks, fundamentals)
- Creating relationships between time-series and metadata tables
- Optimizing query performance on date and ticker columns

**Components**:

1. **Composite Primary Key**: (trade_date, ticker) uniqueness constraint
2. **Index Strategy**: Equality columns first (ticker), then range columns (date)
3. **Foreign Key Relationships**: Ticker → company_info, sector → sector_metadata
4. **Column Types**: Date (not DateTime for daily data), Numeric (precision for prices)

**How to Apply**:

1. Define model with composite primary key on (date, ticker)
2. Add indexes with equality columns first (ticker before date)
3. Create foreign key relationships for metadata lookups
4. Use appropriate column types (Date for daily, DateTime for intraday)
5. Add constraints for data validation (price > 0, volume >= 0)

**Example from Codebase**:

```python
from sqlalchemy import Column, String, Date, Numeric, BigInteger, Index, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class DailyOHLCV(Base):
    __tablename__ = 'daily_ohlcv'

    # Composite primary key - order matters for index efficiency
    trade_date = Column(Date, primary_key=True, nullable=False)
    ticker = Column(String(10), primary_key=True, nullable=False)

    # Price columns - use Numeric for precision (avoid Float)
    open = Column(Numeric(10, 2), nullable=False)
    high = Column(Numeric(10, 2), nullable=False)
    low = Column(Numeric(10, 2), nullable=False)
    close = Column(Numeric(10, 2), nullable=False)
    volume = Column(BigInteger, nullable=False)

    # Foreign key relationship to metadata table
    # ticker references company_info.ticker for joins
    company = relationship("CompanyInfo", back_populates="daily_data")

    # Index strategy: equality columns first (ticker), then range columns (date)
    # Supports queries: WHERE ticker = 'AAPL' AND trade_date BETWEEN ...
    __table_args__ = (
        Index('idx_ticker_date', 'ticker', 'trade_date'),
        Index('idx_date_ticker', 'trade_date', 'ticker'),  # Alternative for date-first queries
    )

class CompanyInfo(Base):
    __tablename__ = 'company_info'

    ticker = Column(String(10), primary_key=True)
    name = Column(String(100), nullable=False)
    sector = Column(String(50))
    market_cap = Column(BigInteger)

    # Reverse relationship to daily data
    daily_data = relationship("DailyOHLCV", back_populates="company")
```text

**Query Optimization Examples**:

```python
from sqlalchemy import select, and_
from datetime import date

# Efficient query using composite index
query = select(DailyOHLCV).where(
    and_(
        DailyOHLCV.ticker == 'AAPL',
        DailyOHLCV.trade_date >= date(2023, 1, 1),
        DailyOHLCV.trade_date <= date(2023, 12, 31)
    )
)
# Uses idx_ticker_date index - seeks to ticker='AAPL', scans date range

# Join with metadata using foreign key relationship
query = select(DailyOHLCV, CompanyInfo).join(
    CompanyInfo, DailyOHLCV.ticker == CompanyInfo.ticker
).where(CompanyInfo.sector == 'Technology')
# Uses relationship for efficient join
```text

**Source**: SQLAlchemy 2.0 documentation (<https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html>)

---

### Framework 4: API Rate Limiting & Exponential Backoff

**Purpose**: Implement robust retry logic with exponential backoff to handle transient API failures and respect provider rate limits during data ingestion.

**When to Use**:

- Fetching data from external APIs (Alpaca, Polygon, Yahoo Finance)
- Handling transient network failures (timeouts, connection errors)
- Respecting rate limits (requests per minute quotas)
- Avoiding thundering herd on service recovery

**Components**:

1. **Rate Limit Configuration**: max_requests_per_minute, max_retries, timeout
2. **Exponential Backoff Formula**: wait_time = min(max_backoff, base_delay × 2^retry_attempt)
3. **Jitter**: Random delay (0-1000ms) to prevent synchronized retries
4. **Retry Conditions**: Transient errors (429, 500, 502, 503, 504, network timeout) vs permanent errors (401, 403, 404)

**How to Apply**:

1. Configure rate limits per provider (Alpaca 200/min, Polygon 5/min, Yahoo 1-2/sec)
2. Set exponential backoff parameters (base_delay=1s, max_retries=3-5, max_backoff=20-60s)
3. Add jitter to prevent thundering herd (random 0-1000ms)
4. Classify errors (retry on transient, skip on permanent)
5. Log retry attempts for monitoring and debugging

**Example from Codebase**:

```python
import time
import random
import requests
from typing import Optional

class MarketDataAPI:
    def __init__(
        self,
        provider: str,
        api_key: str,
        max_requests_per_minute: int = 200,
        max_retries: int = 5,
        base_delay: float = 1.0,
        max_backoff: float = 60.0
    ):
        self.provider = provider
        self.api_key = api_key
        self.max_requests_per_minute = max_requests_per_minute
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_backoff = max_backoff

        # Provider-specific rate limits
        self.rate_limits = {
            'alpaca_free': 200,
            'alpaca_paid': 1000,
            'polygon_free': 5,
            'polygon_paid': 10000,
            'yahoo': 60  # ~1-2 req/sec = 60-120 req/min
        }

    def fetch_with_retry(self, url: str, params: dict) -> Optional[dict]:
        """Fetch data with exponential backoff retry logic."""
        for attempt in range(self.max_retries):
            try:
                response = requests.get(
                    url,
                    params=params,
                    headers={'Authorization': f'Bearer {self.api_key}'},
                    timeout=10
                )

                # Success case
                if response.status_code == 200:
                    return response.json()

                # Rate limit hit - use Retry-After header if available
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 0))
                    wait_time = retry_after if retry_after > 0 else self._calculate_backoff(attempt)
                    print(f"Rate limit hit. Retrying after {wait_time}s (attempt {attempt + 1}/{self.max_retries})")
                    time.sleep(wait_time)
                    continue

                # Transient server errors - retry with backoff
                if response.status_code in [500, 502, 503, 504]:
                    wait_time = self._calculate_backoff(attempt)
                    print(f"Server error {response.status_code}. Retrying after {wait_time}s (attempt {attempt + 1}/{self.max_retries})")
                    time.sleep(wait_time)
                    continue

                # Permanent errors - don't retry
                if response.status_code in [401, 403, 404]:
                    print(f"Permanent error {response.status_code}. Skipping.")
                    return None

                # Unknown error - retry with backoff
                wait_time = self._calculate_backoff(attempt)
                print(f"Unknown error {response.status_code}. Retrying after {wait_time}s")
                time.sleep(wait_time)

            except requests.exceptions.Timeout:
                wait_time = self._calculate_backoff(attempt)
                print(f"Timeout. Retrying after {wait_time}s (attempt {attempt + 1}/{self.max_retries})")
                time.sleep(wait_time)

            except requests.exceptions.ConnectionError:
                wait_time = self._calculate_backoff(attempt)
                print(f"Connection error. Retrying after {wait_time}s (attempt {attempt + 1}/{self.max_retries})")
                time.sleep(wait_time)

        print(f"Max retries ({self.max_retries}) exceeded. Giving up.")
        return None

    def _calculate_backoff(self, attempt: int) -> float:
        """Calculate exponential backoff with jitter."""
        # Exponential backoff: base_delay × 2^attempt
        backoff = min(self.max_backoff, self.base_delay * (2 ** attempt))

        # Add jitter (0-1000ms) to prevent thundering herd
        jitter = random.uniform(0, 1)

        return backoff + jitter

# Usage example
api = MarketDataAPI(
    provider='alpaca_free',
    api_key='your_api_key',
    max_requests_per_minute=200,
    max_retries=5,
    base_delay=1.0,
    max_backoff=60.0
)

data = api.fetch_with_retry(
    url='https://data.alpaca.markets/v2/stocks/AAPL/bars',
    params={'start': '2023-01-01', 'end': '2023-12-31', 'timeframe': '1Day'}
)
```text

**Provider Rate Limits**:

| Provider       | Free Tier     | Paid Tier      | Recommended Config                        |
|----------------|---------------|----------------|-------------------------------------------|
| Alpaca         | 200 req/min   | 1000 req/min   | base_delay=1s, max_retries=5, max_backoff=60s |
| Polygon        | 5 req/min     | Unlimited      | base_delay=2s, max_retries=3, max_backoff=30s |
| Yahoo Finance  | ~60-120 req/min (unofficial) | N/A | base_delay=1s, max_retries=3, max_backoff=20s |

**Source**: Alpaca API documentation (<https://alpaca.markets/docs/api-references/market-data-api/>), Polygon API documentation (<https://polygon.io/docs/stocks/getting-started>), AWS retry guidance (<https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/>)

---

## Decision Trees

### Decision 1: Compression Codec Selection

```text
IF workload == 'real-time ingestion' (low latency writes, market data feeds)
  THEN use Snappy compression
  BECAUSE fastest read/write performance (48% compression, 2100 MB/s read)

ELSE IF workload == 'balanced production' (mixed read/write, daily OHLCV)
  THEN use ZSTD level 1 compression
  BECAUSE best balance of compression ratio (66%) and performance (1400 MB/s read)

ELSE IF workload == 'cold storage archival' (infrequent access, historical research)
  THEN use ZSTD level 19 compression
  BECAUSE maximum compression ratio (71%), exceeds 70% target

ELSE IF workload == 'streaming data' (high throughput, log aggregation)
  THEN use LZ4 compression
  BECAUSE fastest read throughput (3850 MB/s), low CPU usage

ELSE
  THEN use ZSTD level 1 compression (default)
  BECAUSE safe default for unknown workloads, meets 70% target
```text

**Example Scenarios**:

1. **Scenario**: Ingesting tick data from Alpaca WebSocket (100K ticks/sec) → **Decision**: Snappy (prioritize write speed)
2. **Scenario**: Daily batch processing of OHLCV data (1M rows/day) → **Decision**: ZSTD level 1 (balanced compression + performance)
3. **Scenario**: Archiving 10 years of historical data (10GB total, accessed monthly) → **Decision**: ZSTD level 19 (maximize compression)

---

### Decision 2: Partitioning Strategy Selection

```text
IF query_pattern == 'time-range queries only' (e.g., "all stocks for Q1 2023")
  THEN use date-based partitioning (year/month/day)
  BECAUSE 80-95% I/O reduction via partition pruning on date filters

ELSE IF query_pattern == 'single-ticker queries only' (e.g., "AAPL historical data")
  THEN use ticker-based partitioning (ticker/)
  BECAUSE 99% I/O reduction via partition pruning on ticker filters

ELSE IF query_pattern == 'mixed queries' (time-range + ticker filters)
  THEN use hybrid partitioning (year/month/ticker)
  BECAUSE supports both query patterns with 99% I/O reduction

ELSE IF dataset_size < 1GB
  THEN use no partitioning (single file)
  BECAUSE partitioning overhead not justified for small datasets

ELSE
  THEN use hybrid partitioning (year/month/ticker)
  BECAUSE safe default for production workloads, supports all query patterns
```text

**Example Scenarios**:

1. **Scenario**: Backtesting system querying all stocks for specific date ranges → **Decision**: Date-based partitioning
2. **Scenario**: Portfolio tracking querying AAPL, MSFT, GOOGL individually → **Decision**: Ticker-based partitioning
3. **Scenario**: Research platform with mixed temporal and ticker queries → **Decision**: Hybrid partitioning (recommended)

---

### Decision 3: API Retry Strategy

```text
IF error_code in [429] (rate limit)
  THEN retry with exponential backoff + respect Retry-After header
  BECAUSE rate limits are transient, provider specifies wait time

ELSE IF error_code in [500, 502, 503, 504] (server errors)
  THEN retry with exponential backoff (max 5 attempts)
  BECAUSE server errors are usually transient, likely to succeed on retry

ELSE IF error_type in [Timeout, ConnectionError] (network issues)
  THEN retry with exponential backoff (max 3 attempts)
  BECAUSE network issues are transient, but may indicate provider outage

ELSE IF error_code in [401, 403] (authentication/authorization)
  THEN skip retry, log error, return None
  BECAUSE authentication errors are permanent, require API key fix

ELSE IF error_code in [404] (not found)
  THEN skip retry, log warning, return None
  BECAUSE data not available (e.g., delisted ticker), retry won't help

ELSE
  THEN retry once with short backoff (1s), then skip
  BECAUSE unknown errors are unpredictable, limit retry attempts
```text

**Example Scenarios**:

1. **Scenario**: Alpaca returns 429 with Retry-After: 30 → **Decision**: Wait 30s, retry (respects provider guidance)
2. **Scenario**: Polygon returns 503 (service unavailable) → **Decision**: Exponential backoff (1s, 2s, 4s, 8s, 16s)
3. **Scenario**: Yahoo Finance returns 404 for delisted ticker → **Decision**: Skip retry, log warning, continue to next ticker

---

## Anti-Patterns

### Anti-Pattern 1: Using Gzip for Real-Time Ingestion

**Problem**: Gzip has slow write performance (105 MB/s) compared to Snappy (2100 MB/s read), causing bottlenecks in real-time data pipelines.

**Detection**:

- 🔴 High CPU usage during writes (>80%)
- 🔴 Write latency >100ms for small batches (<1000 rows)
- 🔴 Growing backlog of unprocessed market data

**Consequences**:

- ❌ Missed market data during high-volume periods (market open, earnings)
- ❌ Delayed signal generation in trading systems
- ❌ Increased infrastructure costs (more workers to handle backlog)

**Better Approach**:

```python
✅ Preferred Pattern (Snappy for real-time):
pq.write_table(
    table,
    'realtime_ticks.parquet',
    compression='SNAPPY',  # Fast writes, 48% compression
    use_dictionary=True
)

❌ Anti-Pattern (Gzip for real-time):
pq.write_table(
    table,
    'realtime_ticks.parquet',
    compression='GZIP',  # Slow writes, 64% compression
    compression_level=9   # Even slower (maximum compression)
)
```text

**Migration Strategy**:

1. Benchmark current write throughput (rows/sec, MB/s)
2. Switch to Snappy compression for real-time data paths
3. Use ZSTD level 1 for batch processing (balanced performance)
4. Reserve Gzip/ZSTD-19 for cold storage archival only

---

### Anti-Pattern 2: Single Partition for Large Datasets

**Problem**: No partitioning on large datasets (>1GB, >100K rows) forces full table scans, negating Parquet's query pruning benefits.

**Detection**:

- 🔴 All queries read entire dataset regardless of filters
- 🔴 Query latency proportional to dataset size (O(n))
- 🔴 Single large Parquet file (>1GB)

**Consequences**:

- ❌ Slow query performance (10-100x slower than partitioned)
- ❌ High I/O costs in cloud environments (AWS S3 GET requests)
- ❌ Poor scalability as dataset grows

**Better Approach**:

```python
✅ Preferred Pattern (Hybrid partitioning):
pq.write_to_dataset(
    table,
    root_path='market_data/',
    partition_cols=['year', 'month', 'ticker'],  # Enables query pruning
    compression='ZSTD',
    compression_level=1
)

# Query with automatic partition pruning
dataset = ds.dataset('market_data/', format='parquet', partitioning='hive')
filtered = dataset.filter(
    (ds.field('year') == 2023) &
    (ds.field('ticker') == 'AAPL')
)
result = filtered.to_table()  # Only reads relevant partitions (99% I/O reduction)

❌ Anti-Pattern (No partitioning):
pq.write_table(
    table,
    'market_data.parquet',  # Single file, no pruning
    compression='ZSTD'
)

# Query reads entire file
df = pd.read_parquet('market_data.parquet')
filtered = df[(df['year'] == 2023) & (df['ticker'] == 'AAPL')]  # Post-filtering after full read
```text

**Migration Strategy**:

1. Analyze query patterns (temporal, ticker-specific, mixed)
2. Implement hybrid partitioning (year/month/ticker) for new data
3. Backfill historical data with partitioning (batch job)
4. Update query code to use dataset API with filters

---

### Anti-Pattern 3: Retry on All Errors Without Classification

**Problem**: Retrying on permanent errors (401, 403, 404) wastes API quota and delays failure detection. Retrying indefinitely on rate limits causes cascading failures.

**Detection**:

- 🔴 Logs show retry attempts on 401/403/404 errors
- 🔴 API quota exhausted due to repeated failed requests
- 🔴 Exponential backoff delays exceed several minutes

**Consequences**:

- ❌ Wasted API quota on requests guaranteed to fail
- ❌ Slow failure detection (wait for max retries before reporting)
- ❌ Cascading failures if retry delays accumulate

**Better Approach**:

```python
✅ Preferred Pattern (Classify errors before retry):
def fetch_with_retry(url: str, params: dict) -> Optional[dict]:
    for attempt in range(max_retries):
        response = requests.get(url, params=params, timeout=10)

        # Success
        if response.status_code == 200:
            return response.json()

        # Transient errors - retry with backoff
        if response.status_code in [429, 500, 502, 503, 504]:
            time.sleep(calculate_backoff(attempt))
            continue

        # Permanent errors - fail fast, don't retry
        if response.status_code in [401, 403, 404]:
            print(f"Permanent error {response.status_code}. Skipping.")
            return None

    return None

❌ Anti-Pattern (Retry on all errors):
def fetch_with_retry(url: str, params: dict) -> Optional[dict]:
    for attempt in range(max_retries):
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            return response.json()

        # Retry on ALL errors (wastes API quota on 401/403/404)
        time.sleep(calculate_backoff(attempt))

    return None
```text

**Migration Strategy**:

1. Add error classification logic (transient vs permanent)
2. Fail fast on permanent errors (401, 403, 404)
3. Implement exponential backoff with jitter for transient errors
4. Add monitoring/alerting for permanent error rates

---

## Best Practices

### Practice 1: Use Dictionary Encoding for Low-Cardinality Columns

**Principle**: Parquet dictionary encoding replaces repeated values (ticker symbols, sector names) with integer references, dramatically reducing storage and improving compression ratios.

**Implementation**:

- Enable `use_dictionary=True` in PyArrow writer (enabled by default)
- Dictionary encoding most effective for columns with <1000 unique values
- Combine with ZSTD compression for maximum benefit

**Benefits**:

- ✅ 20-40% additional compression on top of codec compression
- ✅ Faster queries due to smaller file sizes
- ✅ Lower memory usage during query execution

**Trade-offs**:

- ⚠️ Slightly slower writes due to dictionary construction
- ⚠️ Less effective for high-cardinality columns (>10K unique values)

**Example**:

```python
import pyarrow as pa
import pyarrow.parquet as pq

# Create table with low-cardinality columns (ticker, sector)
table = pa.Table.from_pandas(df)

# Enable dictionary encoding (default behavior)
pq.write_table(
    table,
    'market_data.parquet',
    compression='ZSTD',
    use_dictionary=True,  # Enables dictionary encoding for all columns
    compression_level=1
)

# Verify dictionary encoding
metadata = pq.read_metadata('market_data.parquet')
print(metadata.row_group(0).column(0).encodings)
# Output: [Encoding.RLE_DICTIONARY, Encoding.PLAIN]
```text

---

### Practice 2: Write Parquet Statistics for Query Pruning

**Principle**: Parquet file statistics (min/max/null_count per column) enable query engines to skip entire row groups without reading data, dramatically improving query performance.

**Implementation**:

- Enable `write_statistics=True` in PyArrow writer
- Statistics written at row group level (default 1M rows per group)
- Query engines use statistics for predicate pushdown

**Benefits**:

- ✅ 10-100x faster queries via row group skipping
- ✅ Lower I/O costs in cloud environments
- ✅ Reduced memory usage during query execution

**Trade-offs**:

- ⚠️ Slightly larger file sizes (~1-2% overhead)
- ⚠️ Minimal write performance impact

**Example**:

```python
# Write with statistics enabled
pq.write_table(
    table,
    'market_data.parquet',
    compression='ZSTD',
    write_statistics=True,  # Enables min/max/null_count statistics
    row_group_size=1000000  # 1M rows per group (default)
)

# Query with automatic row group pruning
import pyarrow.dataset as ds

dataset = ds.dataset('market_data.parquet', format='parquet')
# Filter uses statistics to skip row groups where trade_date < 2023-06-01
filtered = dataset.filter(ds.field('trade_date') >= '2023-06-01')
result = filtered.to_table()
# Row groups with max(trade_date) < 2023-06-01 are skipped entirely
```text

---

### Practice 3: Respect Provider Rate Limits with Token Bucket

**Principle**: Use token bucket algorithm to enforce rate limits proactively, preventing 429 errors and ensuring smooth data ingestion without manual backoff logic.

**Implementation**:

- Track requests per time window (minute, second)
- Sleep if quota exhausted before making request
- Reset quota at window boundary

**Benefits**:

- ✅ Prevents 429 errors and retry overhead
- ✅ Predictable throughput (no bursty traffic)
- ✅ Lower latency (no backoff delays)

**Trade-offs**:

- ⚠️ Slightly lower peak throughput (enforced limit)
- ⚠️ Requires accurate rate limit configuration

**Example**:

```python
import time
from collections import deque

class TokenBucket:
    def __init__(self, rate: int, per_seconds: float = 60.0):
        """
        rate: Maximum requests per time window
        per_seconds: Time window in seconds (default 60s = 1 minute)
        """
        self.rate = rate
        self.per_seconds = per_seconds
        self.allowance = rate
        self.last_check = time.time()
        self.requests = deque()

    def consume(self, tokens: int = 1) -> None:
        """Block until tokens available, then consume."""
        current = time.time()

        # Remove requests outside time window
        while self.requests and self.requests[0] < current - self.per_seconds:
            self.requests.popleft()

        # If quota exhausted, sleep until oldest request expires
        if len(self.requests) >= self.rate:
            sleep_time = self.per_seconds - (current - self.requests[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
                current = time.time()
                self.requests.popleft()

        # Consume token
        self.requests.append(current)

# Usage
bucket = TokenBucket(rate=200, per_seconds=60)  # 200 requests per minute

for ticker in tickers:
    bucket.consume()  # Block if quota exhausted
    data = fetch_ticker_data(ticker)
```text

---

## Common Pitfalls & Solutions

| Pitfall                                      | Detection                                      | Solution                                          |
|----------------------------------------------|------------------------------------------------|---------------------------------------------------|
| Large Parquet files (>1GB) slow queries      | Single file in directory, query latency >10s   | Implement partitioning (year/month/ticker)        |
| High CPU usage during compression            | CPU >80% during writes, slow throughput        | Switch to Snappy/LZ4 for real-time, ZSTD-1 for batch |
| 429 rate limit errors                        | Frequent 429 in logs, exponential backoff      | Implement token bucket, reduce request rate       |
| Repeated 401/403 errors                      | Retry attempts on auth errors, wasted quota    | Classify errors, fail fast on permanent errors    |
| Poor query performance despite partitioning  | All partitions read, no pruning                | Verify filters use partition columns, check statistics |
| Slow writes with dictionary encoding         | Write latency >100ms, high-cardinality columns | Disable dictionary for high-cardinality (>10K unique) |

---

## Tools & Resources

### Recommended Tools

1. **PyArrow**
   - **Purpose**: Parquet reading/writing, compression, partitioning
   - **When to Use**: All Parquet operations, dataset API for queries
   - **Documentation**: <https://arrow.apache.org/docs/python/parquet.html>

2. **SQLAlchemy 2.0**
   - **Purpose**: ORM for time-series data models, relationship mapping
   - **When to Use**: Defining database schemas, querying with ORM
   - **Documentation**: <https://docs.sqlalchemy.org/en/20/>

3. **requests + tenacity**
   - **Purpose**: HTTP requests with retry logic, exponential backoff
   - **When to Use**: API data ingestion, external service calls
   - **Documentation**: <https://requests.readthedocs.io/>, <https://tenacity.readthedocs.io/>

### Learning Resources

1. **Uber Engineering Blog - Parquet Benchmarks**: <https://eng.uber.com/parquet-cost-efficiency-big-data/>
   - **Topic**: Compression codec performance comparison
   - **Quality**: High

2. **AWS Architecture Blog - Exponential Backoff and Jitter**: <https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/>
   - **Topic**: Retry strategies, jitter formulas
   - **Quality**: High

3. **Alpaca API Documentation**: <https://alpaca.markets/docs/api-references/market-data-api/>
   - **Topic**: Rate limits, authentication, data formats
   - **Quality**: High

4. **Polygon API Documentation**: <https://polygon.io/docs/stocks/getting-started>
   - **Topic**: Rate limits, data schemas, WebSocket feeds
   - **Quality**: High

---

## Glossary

- **Compression Ratio**: Percentage reduction in file size after compression (e.g., 70% = 100MB → 30MB)
- **Partition Pruning**: Query optimization that skips entire files/row groups based on metadata, reducing I/O
- **Composite Primary Key**: Database constraint using multiple columns (e.g., date + ticker) to ensure uniqueness
- **Exponential Backoff**: Retry strategy where wait time doubles on each attempt (1s, 2s, 4s, 8s, ...)
- **Jitter**: Random delay added to retry wait time to prevent thundering herd (synchronized retries)
- **Token Bucket**: Rate limiting algorithm that allows bursts up to quota, then enforces steady rate
- **Row Group**: Parquet file subdivision (~1M rows) with independent statistics and compression
- **Dictionary Encoding**: Compression technique replacing repeated values with integer references
- **Hive Partitioning**: Directory naming convention (key=value/) for partition metadata

---

## Sources & References

1. PyArrow Parquet Documentation: <https://arrow.apache.org/docs/python/parquet.html>
   - Accessed: 2025-11-14
   - Confidence: 0.95

2. PyArrow Dataset Documentation: <https://arrow.apache.org/docs/python/dataset.html>
   - Accessed: 2025-11-14
   - Confidence: 0.95

3. SQLAlchemy 2.0 ORM Documentation: <https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html>
   - Accessed: 2025-11-14
   - Confidence: 0.95

4. Uber Engineering Blog - Parquet Benchmarks: <https://eng.uber.com/parquet-cost-efficiency-big-data/>
   - Accessed: 2025-11-14
   - Confidence: 0.90

5. AWS Architecture Blog - Exponential Backoff: <https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/>
   - Accessed: 2025-11-14
   - Confidence: 0.95

6. Alpaca API Documentation: <https://alpaca.markets/docs/api-references/market-data-api/>
   - Accessed: 2025-11-14
   - Confidence: 0.90

7. Polygon API Documentation: <https://polygon.io/docs/stocks/getting-started>
   - Accessed: 2025-11-14
   - Confidence: 0.90

---

## Changelog

- **2025-11-14**: Initial documentation created (confidence: 0.92)
  - Added Parquet compression codec selection framework with performance benchmarks
  - Added partitioning strategy framework with I/O reduction metrics
  - Added SQLAlchemy time-series model patterns with indexing strategies
  - Added API rate limiting and exponential backoff framework with provider limits
  - Added decision trees for codec selection, partitioning, and retry strategies
  - Added anti-patterns: Gzip for real-time, single partition for large datasets, retry on all errors
  - Added best practices: dictionary encoding, statistics, token bucket rate limiting

---

## Related Documentation

- `.claude/docs/guides/market-data-specialist/api-integration.md`: API provider integration patterns, authentication, error handling
- `.claude/docs/guides/market-data-specialist/data-quality.md`: Validation rules, outlier detection, completeness checks
- `.claude/agents/market-data-specialist.md`: Agent definition, responsibilities, workflow
