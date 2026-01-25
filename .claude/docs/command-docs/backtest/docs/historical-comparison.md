# Historical Backtest Comparison

**Version**: 1.0.0 | **Last Updated**: 2025-01-09

---

## Overview

The `--history N` flag enables comparison of the current backtest run against the last N historical runs. This feature helps identify performance trends, regression detection, and strategy evolution over time.

### Usage

```bash
/backtest dashboard --history 5    # Compare against last 5 runs
/backtest dashboard --history 10   # Compare against last 10 runs
```

### What It Does

1. Fetches the last N backtest results from QuantConnect Cloud
2. Normalizes API responses to match `dashboard.schema.json` structure
3. Calculates trend analysis across key metrics
4. Displays comparison in ASCII table format with delta highlighting

---

## QC Cloud API Integration

### Credentials Location

Credentials are stored in the Lean CLI configuration:

```
~/.lean/credentials
```

**Format**:
```json
{
  "user-id": "123456",
  "api-token": "your-api-token-here"
}
```

### API Endpoints

| Endpoint | Purpose | Method |
|----------|---------|--------|
| `/backtests/list` | Retrieve list of backtests for a project | GET |
| `/backtests/read` | Fetch detailed results for a specific backtest | GET |

### Reference Implementation

See `fetch_backtest_logs.py` pattern at:
`C:\Users\kemos\Repos\trendy-trader\quantconnect\scripts\fetch_backtest_logs.py`

**Key Functions**:

```python
def load_credentials():
    """Load QC credentials from lean config."""
    config_path = Path.home() / ".lean" / "credentials"
    with open(config_path, 'r') as f:
        creds = json.load(f)
    return creds.get('user-id', ''), creds.get('api-token', '')

def list_backtests(project_id: str, user_id: str, api_token: str):
    """List available backtests for a project."""
    url = f"{BASE_URL}/backtests/list"
    params = {'projectId': project_id}
    response = requests.get(url, params=params, 
                           auth=HTTPBasicAuth(user_id, api_token))
    return response.json()

def fetch_backtest(project_id: str, backtest_id: str, ...):
    """Fetch detailed backtest data."""
    url = f"{BASE_URL}/backtests/read"
    params = {'projectId': project_id, 'backtestId': backtest_id}
    response = requests.get(url, params=params, 
                           auth=HTTPBasicAuth(user_id, api_token))
    return response.json()
```

---

## Response Normalization

### QC API Response to Dashboard Schema Mapping

The QC API returns results in its own format. Normalize to `dashboard.schema.json`:

| QC API Field | Dashboard Schema Field | Transformation |
|--------------|------------------------|----------------|
| `statistics.sharpeRatio` | `dimensions.risk_adjusted.sharpe_ratio` | Direct map |
| `statistics.sortinoRatio` | `dimensions.risk_adjusted.sortino_ratio` | Direct map |
| `statistics.totalNetProfit` | `dimensions.profitability.total_return_pct` | Convert to % |
| `statistics.compoundingAnnualReturn` | `dimensions.profitability.cagr_pct` | Direct map |
| `statistics.drawdown` | `dimensions.downside_protection.max_drawdown_pct` | Absolute value |
| `statistics.winRate` | `dimensions.trade_quality.win_rate_pct` | Multiply by 100 |
| `statistics.totalTrades` | `dimensions.trade_quality.total_trades` | Direct map |
| `backtestId` | `run_id` | Truncate to 8 chars |
| `created` | `generated_at` | ISO 8601 format |

### Handling Missing Fields

```python
def normalize_qc_response(qc_data: dict) -> dict:
    """Map QC API response to dashboard schema with defaults."""
    stats = qc_data.get('statistics', {})
    
    return {
        'run_id': qc_data.get('backtestId', 'unknown')[:8],
        'generated_at': qc_data.get('created', datetime.now().isoformat()),
        'dimensions': {
            'risk_adjusted': {
                'sharpe_ratio': stats.get('sharpeRatio', 0.0),
                'sortino_ratio': stats.get('sortinoRatio', 0.0),
            },
            'downside_protection': {
                'max_drawdown_pct': abs(stats.get('drawdown', 0.0)),
            },
            'trade_quality': {
                'win_rate_pct': stats.get('winRate', 0.0) * 100,
                'total_trades': stats.get('totalTrades', 0),
            }
        },
        'verdict': 'PASS' if stats.get('sharpeRatio', 0) > 1.0 else 'FAIL'
    }
```

**Graceful Default Values**:
- Numeric fields: `0.0` or `0`
- String fields: `'unknown'` or empty string
- Enum fields: Conservative default (e.g., `'FAIL'`)

---

## Trend Analysis Calculation

### Comparison Logic

Compare current run against the last N runs to identify trends:

```python
def calculate_trend_analysis(current: dict, historical: list[dict]) -> dict:
    """Calculate trend analysis comparing current to historical runs."""
    
    # Extract metric series
    sharpes = [h['dimensions']['risk_adjusted']['sharpe_ratio'] for h in historical]
    max_dds = [h['dimensions']['downside_protection']['max_drawdown_pct'] for h in historical]
    win_rates = [h['dimensions']['trade_quality']['win_rate_pct'] for h in historical]
    
    current_sharpe = current['dimensions']['risk_adjusted']['sharpe_ratio']
    current_dd = current['dimensions']['downside_protection']['max_drawdown_pct']
    current_wr = current['dimensions']['trade_quality']['win_rate_pct']
    
    return {
        'sharpe_trend': classify_trend(current_sharpe, sharpes),
        'drawdown_trend': classify_trend(current_dd, max_dds, lower_is_better=True),
        'win_rate_trend': classify_trend(current_wr, win_rates),
        'consistency_score': calculate_consistency(historical)
    }
```

### Delta Calculation

| Metric | Delta Formula | Interpretation |
|--------|---------------|----------------|
| `sharpe_delta` | `current - avg(historical)` | Positive = improvement |
| `max_dd_delta` | `avg(historical) - current` | Positive = improvement (lower DD) |
| `win_rate_delta` | `current - avg(historical)` | Positive = improvement |

### Trend Classification

```python
def classify_trend(current: float, historical: list[float], 
                   lower_is_better: bool = False) -> str:
    """Classify trend as improving, stable, or declining."""
    if len(historical) < 2:
        return 'stable'
    
    avg = sum(historical) / len(historical)
    delta_pct = ((current - avg) / abs(avg)) * 100 if avg != 0 else 0
    
    if lower_is_better:
        delta_pct = -delta_pct
    
    if delta_pct > 10:
        return 'improving'
    elif delta_pct < -10:
        return 'declining'
    else:
        return 'stable'
```

### Consistency Score

Measures how stable metrics are across runs (0.0 to 1.0):

```python
def calculate_consistency(historical: list[dict]) -> float:
    """Calculate consistency score based on metric stability."""
    sharpes = [h['dimensions']['risk_adjusted']['sharpe_ratio'] for h in historical]
    
    if len(sharpes) < 2:
        return 1.0
    
    std_dev = statistics.stdev(sharpes)
    mean = statistics.mean(sharpes)
    cv = std_dev / abs(mean) if mean != 0 else 0  # Coefficient of variation
    
    # Convert CV to 0-1 score (lower CV = higher consistency)
    return max(0, min(1, 1 - cv))
```

---

## Display Format

### ASCII Table Output

```
================================================================================
                         HISTORICAL COMPARISON (Last 5 Runs)
================================================================================

 Run ID   | Date       | Sharpe | Max DD  | Win Rate | Verdict
----------|------------|--------|---------|----------|----------
 40764ce7 | 2025-01-08 |  1.45  |  12.3%  |   58.2%  |   PASS
 3f8a2b1c | 2025-01-07 |  1.38  |  14.1%  |   55.8%  |   PASS
 2e9c4d5f | 2025-01-05 |  1.22  |  15.8%  |   52.4%  |   PASS
 1d7b3e6a | 2025-01-03 |  0.95  |  18.2%  |   48.9%  |   FAIL
 0c6a2f8b | 2025-01-01 |  1.08  |  16.5%  |   51.2%  |   PASS

--------------------------------------------------------------------------------
 CURRENT  | 2025-01-09 |  1.52  |  11.8%  |   59.5%  |   PASS
--------------------------------------------------------------------------------

TREND ANALYSIS:
  Sharpe Ratio:   IMPROVING (+18.3% vs avg)
  Max Drawdown:   IMPROVING (-23.1% vs avg)
  Win Rate:       IMPROVING (+11.5% vs avg)
  Consistency:    0.82 (HIGH)

================================================================================
```

### Highlighting Significant Changes

Changes exceeding 10% delta are highlighted:

| Delta Range | Display | Color (if terminal supports) |
|-------------|---------|------------------------------|
| > +10% | `[+]` prefix | Green |
| < -10% | `[-]` prefix | Red |
| -10% to +10% | `[=]` prefix | Yellow/Default |

**Example with highlighting**:
```
  Sharpe Ratio:   [+] IMPROVING (+18.3% vs avg)
  Max Drawdown:   [+] IMPROVING (-23.1% vs avg)
  Win Rate:       [+] IMPROVING (+11.5% vs avg)
  Total Trades:   [=] STABLE (+2.1% vs avg)
```

---

## Error Handling

### Missing Credentials

**Symptom**: `FileNotFoundError` when loading credentials

**Resolution**:
```
ERROR: QC credentials not found at ~/.lean/credentials

To fix:
1. Install Lean CLI: pip install lean
2. Login: lean login
3. Retry the command
```

### API Timeout

**Symptom**: Request takes >30 seconds or times out

**Resolution**:
```python
try:
    response = requests.get(url, params=params, 
                           auth=auth, timeout=30)
except requests.Timeout:
    logger.warning("QC API timeout - skipping historical comparison")
    return {'error': 'api_timeout', 'compared_count': 0}
```

**User Message**:
```
WARNING: Historical comparison unavailable (API timeout)
         Proceeding with current run analysis only.
```

### Insufficient Historical Data

**Symptom**: Fewer than N runs available

**Resolution**:
```python
def fetch_historical(n: int) -> list[dict]:
    backtests = list_backtests(project_id, user_id, api_token)
    available = len(backtests)
    
    if available < n:
        logger.info(f"Requested {n} runs, only {available} available")
    
    return backtests[:min(n, available)]
```

**User Message**:
```
NOTE: Requested 10 historical runs, found 3.
      Comparison based on available data.
```

### API Authentication Failure

**Symptom**: 401 Unauthorized response

**Resolution**:
```
ERROR: QC API authentication failed

To fix:
1. Verify credentials: cat ~/.lean/credentials
2. Re-authenticate: lean login --user-id YOUR_ID --api-token YOUR_TOKEN
3. Check token expiration in QC dashboard
```

---

## Schema Reference

Historical comparison data follows `dashboard.schema.json` structure:

```json
{
  "historical_comparison": {
    "compared_count": 5,
    "runs": [
      {
        "run_id": "40764ce7",
        "date": "2025-01-08T14:32:00Z",
        "sharpe_ratio": 1.45,
        "max_drawdown_pct": 12.3,
        "verdict": "PASS"
      }
    ],
    "trend_analysis": {
      "sharpe_trend": "improving",
      "drawdown_trend": "improving",
      "consistency_score": 0.82
    }
  }
}
```

See: `schemas/dashboard.schema.json` for complete schema definition.

---

## Related Documentation

- [Gate Thresholds](./gate-thresholds.md) - Threshold values for PASS/FAIL verdicts
- [Metrics Reference](./metrics-reference.md) - Full metric definitions
- [Workflow Phases](./workflow-phases.md) - Backtest command phases
