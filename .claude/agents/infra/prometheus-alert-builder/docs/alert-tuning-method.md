# Prometheus Alert Tuning & Analysis Methodology

## Table of Contents
1. [Introduction](#introduction)
2. [Alert Tuning Workflow Overview](#alert-tuning-workflow-overview)
3. [Data Collection & Preparation](#data-collection--preparation)
4. [Firing Pattern Analysis](#firing-pattern-analysis)
5. [Incident-Alert Correlation](#incident-alert-correlation)
6. [Threshold Optimization](#threshold-optimization)
7. [Alert Consolidation & Deduplication](#alert-consolidation--deduplication)
8. [Safety Checks & Validation](#safety-checks--validation)
9. [Coverage Matrix Construction](#coverage-matrix-construction)
10. [Decision Framework](#decision-framework)
11. [Edge Case Handling](#edge-case-handling)
12. [Reporting & Documentation](#reporting--documentation)
13. [Real-World Case Studies](#real-world-case-studies)

---

## Introduction

This document provides a comprehensive, step-by-step methodology for analyzing and tuning Prometheus alerts in production environments. Unlike the reference documents that show **what** good and bad alerts look like, this guide teaches **how** to systematically improve existing alerting systems.

### Who This Is For

- SRE teams experiencing alert fatigue
- Platform engineers optimizing alerting systems
- On-call teams drowning in noise
- Anyone managing 50+ Prometheus alerts in production

### When to Use This Methodology

Apply this methodology when:
- Alert volume exceeds incident volume by 10x or more
- On-call teams report >20% false positive rate
- Monthly alert count growing faster than incidents
- Post-incident reviews reveal missed alerts
- Team requests "just turn off all the alerts"

### Expected Outcomes

After applying this methodology:
- **Alert volume reduction**: 80-95% decrease in total firings
- **Incident coverage**: Maintain 100% coverage of real incidents
- **False positive rate**: Reduce to <10%
- **Signal-to-noise ratio**: Improve from 1:50 to 1:5 or better
- **On-call satisfaction**: Measurable improvement in team morale

### Time Investment

- **First-time application**: 40-80 hours over 2-4 weeks
- **Subsequent iterations**: 8-16 hours quarterly
- **Maintenance**: 2-4 hours monthly

---

## Alert Tuning Workflow Overview

### The 7-Step Process

```
┌─────────────────────────────────────────────────────────┐
│ Step 1: Data Collection & Preparation                   │
│ • Gather 7+ days firing history                         │
│ • Collect incident data with timestamps                 │
│ • Extract metrics samples around incidents              │
│ • Normalize labels across datasets                      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Step 2: Firing Pattern Analysis                         │
│ • Detect flapping alerts                                │
│ • Identify temporal patterns                            │
│ • Analyze volume distribution                           │
│ • Find cardinality explosions                           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Step 3: Incident-Alert Correlation                      │
│ • Map firing times to incident windows                  │
│ • Identify coverage gaps                                │
│ • Detect redundant coverage                             │
│ • Find leading indicators                               │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Step 4: Threshold Optimization                          │
│ • Analyze metric distributions                          │
│ • Calculate appropriate thresholds                      │
│ • Size 'for' clauses correctly                          │
│ • Test threshold changes                                │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Step 5: Alert Consolidation                             │
│ • Identify redundant alert pairs                        │
│ • Calculate correlation coefficients                    │
│ • Merge redundant alerts safely                         │
│ • Create alert hierarchies                              │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Step 6: Safety Checks & Validation                      │
│ • Verify incident coverage maintained                   │
│ • Validate PromQL syntax                                │
│ • Test in non-production                                │
│ • Define rollback plan                                  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Step 7: Documentation & Deployment                      │
│ • Generate analysis report                              │
│ • Create coverage matrix                                │
│ • Document decisions                                    │
│ • Deploy with monitoring                                │
└─────────────────────────────────────────────────────────┘
```

### Prerequisites

Before starting, ensure you have:

1. **Firing History Data** (7-30 days recommended)
   - JSONL format with: alert_name, timestamp, labels, status
   - Minimum 1 week for pattern detection
   - More history = better trend analysis

2. **Incident Log** (matching time period)
   - Incident ID, start/end timestamps, severity
   - Affected services/components
   - Root cause (if known)

3. **Metrics Access**
   - Query access to Prometheus
   - Historical data retention matching firing history
   - Ability to run queries around incident times

4. **Service Catalog**
   - Service ownership mapping
   - Dependency graphs
   - SLO definitions (if available)

5. **Current Alert Rules**
   - Complete alert_rules.yaml files
   - Recording rules (if used)
   - Alertmanager configuration

### Success Criteria Definition

Before starting, agree on targets with stakeholders:

```yaml
success_criteria:
  alert_reduction:
    target: 90%  # Reduce total monthly firings by 90%
    minimum_acceptable: 80%
    
  incident_coverage:
    target: 100%  # Every incident must have covering alert
    minimum_acceptable: 95%  # May accept 5% gap for noise reduction
    
  false_positive_rate:
    target: "< 10%"  # <10% of alerts should be false positives
    maximum_acceptable: "20%"
    
  signal_to_noise:
    current: "1:50"  # 1 real incident per 50 alerts
    target: "1:5"    # 1 real incident per 5 alerts
    
  deployment_timeline:
    analysis_phase: 2_weeks
    testing_phase: 1_week
    gradual_rollout: 2_weeks
```

---

## Data Collection & Preparation

### Step 1: Gather Firing History

**Format**: JSONL (one JSON object per line)

**Required Fields**:
```json
{
  "alert_name": "HighCPUUsage",
  "timestamp": "2025-12-01T14:23:15Z",
  "status": "firing",
  "labels": {
    "instance": "web-01",
    "service": "api",
    "severity": "warning"
  },
  "annotations": {
    "summary": "High CPU on web-01"
  },
  "value": 92.5
}
```

**Collection Methods**:

**Method 1: From Alertmanager API**
```bash
# Get all alerts from last 7 days
curl -s 'http://alertmanager:9093/api/v2/alerts?active=true&silenced=false' \
  | jq -r '.[] | @json' > firing_history.jsonl

# For historical data, query Prometheus ALERTS metric
curl -s 'http://prometheus:9090/api/v1/query_range' \
  --data-urlencode 'query=ALERTS{alertstate="firing"}' \
  --data-urlencode 'start=2025-11-24T00:00:00Z' \
  --data-urlencode 'end=2025-12-01T00:00:00Z' \
  --data-urlencode 'step=1m' \
  | jq -r '.data.result[] | .values[] | @json' > firing_history.jsonl
```

**Method 2: From Notification Logs**
```python
# Parse from PagerDuty, Slack, or email logs
import json
from datetime import datetime

def parse_slack_webhooks(log_file):
    alerts = []
    with open(log_file) as f:
        for line in f:
            webhook_data = json.loads(line)
            # Extract alert info from webhook payload
            alert = {
                "alert_name": webhook_data["title"],
                "timestamp": webhook_data["timestamp"],
                "status": "firing",
                "labels": webhook_data["labels"],
                "annotations": webhook_data["annotations"]
            }
            alerts.append(alert)
    return alerts
```

### Step 2: Collect Incident Data

**Format**: JSON array

**Required Fields**:
```json
{
  "incidents": [
    {
      "incident_id": "INC-001",
      "start_time": "2025-12-01T14:23:00Z",
      "end_time": "2025-12-01T14:45:00Z",
      "severity": "P1",
      "affected_services": ["payment-api", "user-service"],
      "root_cause": "database_connection_pool_exhaustion",
      "user_impact": "15% of payment requests failed",
      "detection_method": "customer_report"
    }
  ]
}
```

**Collection Sources**:
- PagerDuty incident API
- Jira/ServiceNow tickets
- Post-incident review documents
- StatusPage incident history

**Python Example**:
```python
import requests
from datetime import datetime, timedelta

def fetch_pagerduty_incidents(api_key, days=7):
    headers = {
        "Authorization": f"Token token={api_key}",
        "Accept": "application/vnd.pagerduty+json;version=2"
    }
    
    since = (datetime.now() - timedelta(days=days)).isoformat()
    until = datetime.now().isoformat()
    
    url = f"https://api.pagerduty.com/incidents"
    params = {
        "since": since,
        "until": until,
        "statuses[]": ["triggered", "acknowledged", "resolved"]
    }
    
    response = requests.get(url, headers=headers, params=params)
    incidents = response.json()["incidents"]
    
    formatted = []
    for inc in incidents:
        formatted.append({
            "incident_id": inc["id"],
            "start_time": inc["created_at"],
            "end_time": inc.get("resolved_at", inc["last_status_change_at"]),
            "severity": inc["urgency"],  # or inc["priority"]["summary"]
            "affected_services": [inc["service"]["summary"]],
            "title": inc["title"]
        })
    
    return formatted
```

### Step 3: Extract Metrics Samples

**Purpose**: Understand metric behavior around incidents to inform threshold tuning.

**Collection Strategy**:

For each incident, collect metric samples:
- **Before incident**: -2 hours to incident start
- **During incident**: incident start to end
- **After incident**: incident end to +2 hours

**Python Example**:
```python
import requests
from datetime import datetime, timedelta

def get_metrics_around_incident(prometheus_url, incident, metric_name):
    """
    Collect metric samples around an incident timeframe.
    """
    start_time = datetime.fromisoformat(incident["start_time"].replace("Z", "+00:00"))
    end_time = datetime.fromisoformat(incident["end_time"].replace("Z", "+00:00"))
    
    # Extend window by 2 hours on each side
    query_start = (start_time - timedelta(hours=2)).isoformat()
    query_end = (end_time + timedelta(hours=2)).isoformat()
    
    # Query Prometheus
    response = requests.get(
        f"{prometheus_url}/api/v1/query_range",
        params={
            "query": metric_name,
            "start": query_start,
            "end": query_end,
            "step": "30s"
        }
    )
    
    samples = []
    for result in response.json()["data"]["result"]:
        labels = result["metric"]
        for timestamp, value in result["values"]:
            samples.append({
                "metric": metric_name,
                "labels": labels,
                "timestamp": datetime.fromtimestamp(timestamp).isoformat(),
                "value": float(value),
                "incident_id": incident["incident_id"],
                "incident_phase": classify_phase(timestamp, start_time, end_time)
            })
    
    return samples

def classify_phase(sample_time, incident_start, incident_end):
    """Classify if sample is before, during, or after incident."""
    if sample_time < incident_start.timestamp():
        return "before"
    elif sample_time <= incident_end.timestamp():
        return "during"
    else:
        return "after"
```

### Step 4: Label Normalization

**Problem**: Inconsistent label names/values prevent accurate correlation.

**Common Mismatches**:
```
Incident:         service: "payment-api"
Alert:            app: "payment-api"
Metric:           job: "payment-api"

Incident:         environment: "production"
Alert:            env: "prod"
Metric:           stage: "prod"
```

**Normalization Strategy**:

```python
def normalize_labels(data, label_mappings):
    """
    Normalize label names and values across datasets.
    
    label_mappings = {
        "service": ["app", "job", "application"],  # All map to "service"
        "environment": {
            "env": {"prod": "production", "stg": "staging"},
            "stage": {"prod": "production", "stg": "staging"}
        }
    }
    """
    normalized = data.copy()
    
    # Normalize label names
    for standard_name, alternatives in label_mappings.items():
        if isinstance(alternatives, list):
            for alt in alternatives:
                if alt in normalized.get("labels", {}):
                    normalized["labels"][standard_name] = normalized["labels"].pop(alt)
    
    # Normalize label values
    for label_name, value_mappings in label_mappings.items():
        if isinstance(value_mappings, dict):
            current_value = normalized.get("labels", {}).get(label_name)
            if current_value in value_mappings:
                normalized["labels"][label_name] = value_mappings[current_value]
    
    return normalized
```

**Create Normalization Map**:
```yaml
# normalization_config.yaml
label_mappings:
  service:
    aliases: [app, job, application, component]
  
  environment:
    aliases: [env, stage, tier]
    value_map:
      prod: production
      prd: production
      stg: staging
      stage: staging
      dev: development
  
  severity:
    value_map:
      page: critical
      crit: critical
      warn: warning
      info: information
```

### Step 5: Data Validation

**Validation Checklist**:

```python
def validate_data_quality(firing_history, incidents, metrics):
    """Run data quality checks before analysis."""
    
    issues = []
    
    # Check 1: Sufficient time coverage
    if len(firing_history) < 1000:
        issues.append("WARN: <1000 alert firings may not be sufficient for analysis")
    
    # Check 2: Incident coverage period matches firing history
    firing_start = min(f["timestamp"] for f in firing_history)
    firing_end = max(f["timestamp"] for f in firing_history)
    incident_start = min(i["start_time"] for i in incidents)
    incident_end = max(i["end_time"] for i in incidents)
    
    if incident_start < firing_start:
        issues.append(f"ERROR: Incidents before firing history ({incident_start} < {firing_start})")
    
    # Check 3: All incidents have affected services
    for inc in incidents:
        if not inc.get("affected_services"):
            issues.append(f"WARN: Incident {inc['incident_id']} missing affected_services")
    
    # Check 4: Label consistency
    all_service_labels = set()
    for alert in firing_history:
        if "service" in alert.get("labels", {}):
            all_service_labels.add(alert["labels"]["service"])
    
    incident_services = set()
    for inc in incidents:
        incident_services.update(inc.get("affected_services", []))
    
    unmapped = incident_services - all_service_labels
    if unmapped:
        issues.append(f"WARN: Services in incidents but not in alerts: {unmapped}")
    
    return issues
```

---

## Firing Pattern Analysis

### Flapping Detection

**Definition**: Alert fires and resolves repeatedly in a short time window, indicating instability.

**Detection Criteria**:
- 10+ fires within 1 hour window
- Average firing duration < 5 minutes
- Ratio of fires-to-resolution time > 5:1

**Python Implementation**:

```python
from datetime import datetime, timedelta
from collections import defaultdict

def detect_flapping_alerts(firing_history):
    """
    Identify alerts that fire/resolve repeatedly (flapping).
    """
    # Group firings by alert name
    alert_events = defaultdict(list)
    
    for event in firing_history:
        key = (event["alert_name"], frozenset(event["labels"].items()))
        alert_events[key].append({
            "timestamp": datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00")),
            "status": event["status"]
        })
    
    flapping_alerts = []
    
    for alert_key, events in alert_events.items():
        # Sort by timestamp
        events.sort(key=lambda x: x["timestamp"])
        
        # Sliding 1-hour window
        for i in range(len(events)):
            window_start = events[i]["timestamp"]
            window_end = window_start + timedelta(hours=1)
            
            # Count fires in window
            window_events = [
                e for e in events 
                if window_start <= e["timestamp"] <= window_end
            ]
            
            fire_count = sum(1 for e in window_events if e["status"] == "firing")
            resolve_count = sum(1 for e in window_events if e["status"] == "resolved")
            
            # Flapping if 10+ fires in 1 hour
            if fire_count >= 10:
                alert_name, labels = alert_key
                flapping_alerts.append({
                    "alert_name": alert_name,
                    "labels": dict(labels),
                    "window_start": window_start.isoformat(),
                    "fire_count": fire_count,
                    "resolve_count": resolve_count,
                    "pattern": "flapping"
                })
                break  # Only report once per alert
    
    return flapping_alerts

# Example usage
flapping = detect_flapping_alerts(firing_history)
print(f"Found {len(flapping)} flapping alerts:")
for alert in flapping:
    print(f"  {alert['alert_name']}: {alert['fire_count']} fires in 1 hour")
```

**Root Cause Analysis for Flapping**:

1. **Missing `for` Clause**
   ```yaml
   # Problem
   - alert: HighCPU
     expr: cpu > 80
     # No 'for' clause - fires on every spike
   
   # Solution
   - alert: HighCPU
     expr: cpu > 80
     for: 15m  # Wait 15 minutes before firing
   ```

2. **Threshold Too Sensitive**
   ```yaml
   # Problem: Metric oscillates around threshold
   # 79% → 81% → 79% → 81% (flapping)
   
   # Solution: Adjust threshold or add hysteresis
   - alert: HighCPU
     expr: cpu > 90  # Increase threshold
     for: 10m
   ```

3. **Using irate() in Expression**
   ```yaml
   # Problem: irate() only looks at last 2 points, very volatile
   - alert: HighTraffic
     expr: irate(requests[5m]) > 100
     for: 5m  # for clause ineffective with irate()
   
   # Solution: Use rate() instead
   - alert: HighTraffic
     expr: rate(requests[5m]) > 100
     for: 5m
   ```

**Remediation Decision Tree**:

```
Flapping Alert Detected
│
├─ Has 'for' clause?
│  ├─ No → Add 'for: 10m' (or longer based on metric)
│  └─ Yes → Continue to next check
│
├─ Duration < 2× scrape_interval?
│  ├─ Yes → Increase to at least 2× scrape_interval
│  └─ No → Continue to next check
│
├─ Using irate()?
│  ├─ Yes → Replace with rate()
│  └─ No → Continue to next check
│
├─ Metric oscillates around threshold?
│  ├─ Yes → Increase threshold OR add percentage buffer
│  └─ No → Check if legitimate flapping (unstable system)
│
└─ Review metric source and collection
```

### Temporal Pattern Analysis

**Purpose**: Identify time-based patterns (day/night, weekday/weekend, seasonality).

**Patterns to Detect**:

1. **Time-of-Day Pattern**
   - Alert fires only during business hours (9am-5pm)
   - Alert fires only at night (low traffic misinterpreted as error)

2. **Day-of-Week Pattern**
   - Alert fires only on weekends (different traffic profile)
   - Alert fires only on weekdays

3. **Regular Interval Pattern**
   - Alert fires every hour (cron job?)
   - Alert fires every 5 minutes (health check?)

**Detection Implementation**:

```python
import pandas as pd
from datetime import datetime

def analyze_temporal_patterns(firing_history):
    """
    Detect time-based patterns in alert firings.
    """
    # Convert to DataFrame
    df = pd.DataFrame(firing_history)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek
    df["is_weekend"] = df["day_of_week"].isin([5, 6])
    
    patterns = []
    
    # Group by alert name
    for alert_name in df["alert_name"].unique():
        alert_df = df[df["alert_name"] == alert_name]
        
        # Time-of-day pattern
        hourly_fires = alert_df.groupby("hour").size()
        business_hours_fires = hourly_fires[9:18].sum()
        off_hours_fires = hourly_fires.drop(range(9, 18)).sum()
        
        if business_hours_fires > 0.9 * len(alert_df):
            patterns.append({
                "alert_name": alert_name,
                "pattern": "business_hours_only",
                "description": f"{business_hours_fires/len(alert_df)*100:.0f}% of fires during 9am-5pm"
            })
        
        # Weekend pattern
        weekend_fires = alert_df[alert_df["is_weekend"]].shape
        weekday_fires = alert_df[~alert_df["is_weekend"]].shape
        
        if weekend_fires > 0.8 * len(alert_df):
            patterns.append({
                "alert_name": alert_name,
                "pattern": "weekend_only",
                "description": f"{weekend_fires/len(alert_df)*100:.0f}% of fires on weekends"
            })
        
        # Regular interval pattern (detect spikes at regular intervals)
        alert_df = alert_df.sort_values("timestamp")
        time_diffs = alert_df["timestamp"].diff().dt.total_seconds()
        
        # Check for regular intervals (within 10% variance)
        if len(time_diffs) > 10:
            median_diff = time_diffs.median()
            std_diff = time_diffs.std()
            
            if std_diff / median_diff < 0.1:  # Low variance
                patterns.append({
                    "alert_name": alert_name,
                    "pattern": "regular_interval",
                    "interval_seconds": median_diff,
                    "description": f"Fires every {median_diff/60:.0f} minutes"
                })
    
    return patterns
```

**Remediation Strategies**:

| Pattern | Root Cause | Solution |
|---------|-----------|----------|
| **Business hours only** | Traffic-based threshold doesn't account for off-hours | Use baseline comparison or time-of-day recording rules |
| **Night-only fires** | Absolute threshold too sensitive for low traffic | Add minimum traffic threshold |
| **Weekend spikes** | Different usage pattern | Separate alert rules for weekend vs weekday |
| **Regular 5-minute interval** | Health check or cron job | Exclude known maintenance windows |

**Example Fix for Time-of-Day Pattern**:

```yaml
# Before: Fires at night due to low traffic making percentage high
- alert: HighErrorRate
  expr: |
    (errors / requests) > 0.01
  # At night: 1 error / 10 requests = 10% (alert fires!)

# After: Add minimum traffic threshold
- alert: HighErrorRate
  expr: |
    (errors / requests) > 0.01
    and
    rate(requests[5m]) > 10  # Minimum 10 req/s
  # At night: 1 error / 10 requests, but < 10 req/s (no alert)
```

### Volume Analysis

**Purpose**: Identify alerts contributing most to noise.

**Metrics to Calculate**:
- Total fires per alert (7-day period)
- Fires per day average
- Percentage of total alert volume
- Fire duration (short = likely noise)

**Implementation**:

```python
def analyze_alert_volume(firing_history):
    """
    Calculate volume statistics for each alert.
    """
    alert_stats = defaultdict(lambda: {
        "total_fires": 0,
        "total_duration_seconds": 0,
        "avg_duration_seconds": 0,
        "fires_per_day": 0,
        "percentage_of_total": 0
    })
    
    total_fires = len(firing_history)
    
    # Group by alert name
    for event in firing_history:
        alert_name = event["alert_name"]
        alert_stats[alert_name]["total_fires"] += 1
    
    # Calculate percentages and averages
    time_span_days = 7  # Adjust based on your data
    
    results = []
    for alert_name, stats in alert_stats.items():
        stats["fires_per_day"] = stats["total_fires"] / time_span_days
        stats["percentage_of_total"] = (stats["total_fires"] / total_fires) * 100
        
        results.append({
            "alert_name": alert_name,
            **stats
        })
    
    # Sort by volume (highest first)
    results.sort(key=lambda x: x["total_fires"], reverse=True)
    
    return results

# Identify top noise contributors
volume_analysis = analyze_alert_volume(firing_history)
top_10_noisy = volume_analysis[:10]

print("Top 10 noisiest alerts:")
for alert in top_10_noisy:
    print(f"  {alert['alert_name']}: {alert['total_fires']} fires ({alert['percentage_of_total']:.1f}% of total)")
```

**Pareto Principle Check**:

Typically, 20% of alerts cause 80% of the noise.

```python
def calculate_pareto(volume_analysis):
    """
    Calculate cumulative percentage to find 80/20 split.
    """
    cumulative_pct = 0
    alert_count = 0
    
    for alert in volume_analysis:
        cumulative_pct += alert["percentage_of_total"]
        alert_count += 1
        
        if cumulative_pct >= 80:
            break
    
    return {
        "top_alert_count": alert_count,
        "total_alerts": len(volume_analysis),
        "percentage_of_alerts": (alert_count / len(volume_analysis)) * 100,
        "noise_contribution": cumulative_pct
    }

pareto = calculate_pareto(volume_analysis)
print(f"{pareto['top_alert_count']} alerts ({pareto['percentage_of_alerts']:.0f}%) cause {pareto['noise_contribution']:.0f}% of noise")
```

**Focus Areas**: Prioritize tuning the top 20% noisiest alerts for maximum impact.

### Cardinality Explosion Detection

**Definition**: Alert creates hundreds or thousands of instances due to high-cardinality labels.

**Detection**:

```python
def detect_cardinality_explosions(firing_history, threshold=100):
    """
    Identify alerts creating excessive instances.
    """
    # Group by alert name and count unique label combinations
    alert_instances = defaultdict(set)
    
    for event in firing_history:
        alert_name = event["alert_name"]
        # Create hashable key from labels
        label_key = frozenset(event["labels"].items())
        alert_instances[alert_name].add(label_key)
    
    explosions = []
    
    for alert_name, instances in alert_instances.items():
        instance_count = len(instances)
        
        if instance_count > threshold:
            # Identify which label is causing the explosion
            label_cardinality = defaultdict(set)
            
            for label_set in instances:
                for label_name, label_value in label_set:
                    label_cardinality[label_name].add(label_value)
            
            # Find high-cardinality labels
            high_card_labels = {
                label: len(values)
                for label, values in label_cardinality.items()
                if len(values) > 50
            }
            
            explosions.append({
                "alert_name": alert_name,
                "instance_count": instance_count,
                "high_cardinality_labels": high_card_labels
            })
    
    return explosions

# Detect cardinality issues
explosions = detect_cardinality_explosions(firing_history, threshold=100)
print(f"Found {len(explosions)} alerts with cardinality explosions:")
for exp in explosions:
    print(f"  {exp['alert_name']}: {exp['instance_count']} instances")
    for label, card in exp['high_cardinality_labels'].items():
        print(f"    - Label '{label}' has {card} unique values")
```

**Remediation**:

```yaml
# Problem: Per-pod alert creates 1000 instances
- alert: HighCPUPerPod
  expr: container_cpu_usage{pod=~".*"} > 0.9
  # With 1000 pods, creates 1000 separate alerts

# Solution 1: Aggregate by service
- alert: HighCPUByService
  expr: |
    avg by(service) (container_cpu_usage) > 0.8
  # Creates 1 alert per service instead

# Solution 2: Alert on percentage of pods affected
- alert: ServicePodsHighCPU
  expr: |
    (
      count(container_cpu_usage{service="myapp"} > 0.9) by (service)
      /
      count(container_cpu_usage{service="myapp"}) by (service)
    ) > 0.25
  # Alerts when >25% of pods high CPU
```

---

## Incident-Alert Correlation

### Correlation Methodology

**Goal**: Map each incident to the alerts that fired (or should have fired) during the incident window.

**Time Window Matching**:

```python
from datetime import datetime, timedelta

def correlate_alerts_to_incidents(firing_history, incidents, window_before=300, window_after=300):
    """
    Map alerts to incidents based on time windows.
    
    window_before: seconds before incident start to check for alerts (default 5 min)
    window_after: seconds after incident start to check for alerts (default 5 min)
    """
    correlations = []
    
    for incident in incidents:
        incident_start = datetime.fromisoformat(incident["start_time"].replace("Z", "+00:00"))
        incident_end = datetime.fromisoformat(incident["end_time"].replace("Z", "+00:00"))
        
        # Define correlation window
        window_start = incident_start - timedelta(seconds=window_before)
        window_end = incident_start + timedelta(seconds=window_after)
        
        # Find alerts that fired in this window
        matching_alerts = []
        
        for alert in firing_history:
            alert_time = datetime.fromisoformat(alert["timestamp"].replace("Z", "+00:00"))
            
            if window_start <= alert_time <= window_end:
                # Check if labels match incident
                if labels_match(alert["labels"], incident):
                    matching_alerts.append({
                        "alert_name": alert["alert_name"],
                        "timestamp": alert["timestamp"],
                        "time_before_incident": (incident_start - alert_time).total_seconds(),
                        "labels": alert["labels"]
                    })
        
        correlations.append({
            "incident_id": incident["incident_id"],
            "incident_start": incident["start_time"],
            "incident_severity": incident["severity"],
            "affected_services": incident["affected_services"],
            "matching_alerts": matching_alerts,
            "alert_count": len(matching_alerts)
        })
    
    return correlations

def labels_match(alert_labels, incident):
    """
    Check if alert labels match incident metadata.
    """
    # Check service match
    if "service" in alert_labels:
        if alert_labels["service"] in incident.get("affected_services", []):
            return True
    
    # Check environment match
    if "environment" in alert_labels:
        if alert_labels["environment"] == incident.get("environment", "production"):
            return True
    
    # Add more matching logic as needed
    return False
```

**Example Output**:

```json
{
  "incident_id": "INC-001",
  "incident_start": "2025-12-01T14:23:00Z",
  "incident_severity": "P1",
  "affected_services": ["payment-api"],
  "matching_alerts": [
    {
      "alert_name": "HighErrorRate",
      "timestamp": "2025-12-01T14:23:15Z",
      "time_before_incident": -15,
      "labels": {"service": "payment-api", "severity": "critical"}
    },
    {
      "alert_name": "HighCPU",
      "timestamp": "2025-12-01T14:20:00Z",
      "time_before_incident": 180,
      "labels": {"service": "payment-api", "severity": "warning"}
    }
  ],
  "alert_count": 2
}
```

### Coverage Analysis

**Coverage Types**:

1. **Direct Coverage**: Alert fires during incident window
2. **Leading Indicator**: Alert fires before incident (predictive)
3. **Lagging Indicator**: Alert fires after incident starts (too late but validates)
4. **No Coverage**: Incident with no alerts (gap!)

**Classification**:

```python
def classify_coverage(correlations):
    """
    Classify incident coverage by alert timing.
    """
    results = []
    
    for corr in correlations:
        if corr["alert_count"] == 0:
            coverage_type = "no_coverage"
            quality = "critical_gap"
        else:
            # Analyze timing
            timings = [a["time_before_incident"] for a in corr["matching_alerts"]]
            
            # Direct coverage: within 2 minutes of incident start
            direct = [t for t in timings if -120 <= t <= 120]
            # Leading: more than 2 min before
            leading = [t for t in timings if t < -120]
            # Lagging: more than 2 min after
            lagging = [t for t in timings if t > 120]
            
            if direct:
                coverage_type = "direct"
                quality = "good"
            elif leading:
                coverage_type = "leading_indicator"
                quality = "excellent"  # Caught it early!
            elif lagging:
                coverage_type = "lagging"
                quality = "poor"  # Too late
            else:
                coverage_type = "no_coverage"
                quality = "critical_gap"
        
        results.append({
            **corr,
            "coverage_type": coverage_type,
            "coverage_quality": quality
        })
    
    return results
```

### Gap Identification

**Finding Uncovered Incidents**:

```python
def identify_coverage_gaps(classified_coverage):
    """
    Find incidents without adequate alert coverage.
    """
    gaps = []
    
    for item in classified_coverage:
        if item["coverage_type"] == "no_coverage":
            gaps.append({
                "incident_id": item["incident_id"],
                "severity": item["incident_severity"],
                "affected_services": item["affected_services"],
                "recommendation": "Create new alert or tune existing alert to cover this scenario"
            })
    
    return gaps

# Identify gaps
gaps = identify_coverage_gaps(classified_coverage)
if gaps:
    print(f"Found {len(gaps)} incidents without alert coverage:")
    for gap in gaps:
        print(f"  {gap['incident_id']} ({gap['severity']}): {gap['affected_services']}")
```

**Creating Alerts for Gaps**:

When you find an uncovered incident:

1. **Review incident details**: What metric changed?
2. **Query metrics during incident**: What threshold would have caught it?
3. **Design new alert** or **tune existing alert**

Example:
```python
# Incident INC-001: Payment API database connection pool exhausted
# No alert fired

# Step 1: Query metrics during incident
metrics_during = get_metrics_around_incident(
    prometheus_url,
    incident,
    "db_connections_active / db_connections_max"
)

# Step 2: Analyze values
# Found: db connections reached 98% at incident start

# Step 3: Create alert
new_alert = """
- alert: DatabaseConnectionPoolNearLimit
  expr: |
    (db_connections_active / db_connections_max) * 100 > 85
  for: 10m
  labels:
    severity: warning
    team: database
  annotations:
    summary: "Database connection pool at {{ $value | humanizePercentage }}"
"""
```

### Redundancy Detection

**Finding Always-Together Alert Pairs**:

```python
def detect_redundant_alerts(correlations, threshold=0.9):
    """
    Identify alert pairs that always fire together.
    """
    from itertools import combinations
    
    # Build co-occurrence matrix
    alert_pairs = defaultdict(lambda: {"together": 0, "total": 0})
    
    for corr in correlations:
        alert_names = [a["alert_name"] for a in corr["matching_alerts"]]
        unique_alerts = set(alert_names)
        
        # For each pair of alerts
        for alert_a, alert_b in combinations(unique_alerts, 2):
            pair_key = tuple(sorted([alert_a, alert_b]))
            alert_pairs[pair_key]["together"] += 1
    
    # Count total occurrences of each alert
    alert_counts = defaultdict(int)
    for corr in correlations:
        for alert in corr["matching_alerts"]:
            alert_counts[alert["alert_name"]] += 1
    
    # Calculate correlation coefficient
    redundant_pairs = []
    
    for (alert_a, alert_b), counts in alert_pairs.items():
        together = counts["together"]
        total_a = alert_counts[alert_a]
        total_b = alert_counts[alert_b]
        
        # Correlation = together / min(total_a, total_b)
        correlation = together / min(total_a, total_b)
        
        if correlation >= threshold:
            redundant_pairs.append({
                "alert_a": alert_a,
                "alert_b": alert_b,
                "correlation": correlation,
                "together_count": together,
                "recommendation": "Consider consolidating these alerts"
            })
    
    return redundant_pairs
```

**Example Output**:
```python
{
  "alert_a": "HighCPU",
  "alert_b": "HighMemory",
  "correlation": 0.95,
  "together_count": 20,
  "recommendation": "95% correlation - consider consolidating into ResourceExhaustion alert"
}
```

---

## Threshold Optimization

### Metric Distribution Analysis

**Goal**: Find the threshold that separates "normal" from "incident" states.

**Statistical Approach**:

```python
import numpy as np
from scipy import stats

def analyze_metric_distribution(metrics_samples, incident_id=None):
    """
    Calculate statistical properties of metric during and outside incidents.
    """
    if incident_id:
        incident_samples = [s for s in metrics_samples if s["incident_id"] == incident_id]
        during = [s["value"] for s in incident_samples if s["incident_phase"] == "during"]
        before_after = [s["value"] for s in incident_samples if s["incident_phase"] in ["before", "after"]]
    else:
        during = []
        before_after = [s["value"] for s in metrics_samples]
    
    stats_during = {
        "mean": np.mean(during) if during else None,
        "median": np.median(during) if during else None,
        "p50": np.percentile(during, 50) if during else None,
        "p90": np.percentile(during, 90) if during else None,
        "p95": np.percentile(during, 95) if during else None,
        "p99": np.percentile(during, 99) if during else None,
        "std": np.std(during) if during else None
    }
    
    stats_normal = {
        "mean": np.mean(before_after) if before_after else None,
        "median": np.median(before_after) if before_after else None,
        "p50": np.percentile(before_after, 50) if before_after else None,
        "p90": np.percentile(before_after, 90) if before_after else None,
        "p95": np.percentile(before_after, 95) if before_after else None,
        "p99": np.percentile(before_after, 99) if before_after else None,
        "std": np.std(before_after) if before_after else None
    }
    
    # Find separation point
    if during and before_after:
        # Threshold = point where incident distribution starts
        proposed_threshold = min(during)  # Conservative
        # Or use statistical approach
        # threshold = normal_mean + 3 * normal_std
        
        return {
            "during_incident": stats_during,
            "normal_operation": stats_normal,
            "proposed_threshold": proposed_threshold,
            "current_max_normal": max(before_after),
            "current_min_incident": min(during),
            "separation_gap": min(during) - max(before_after)
        }
    
    return {"normal_operation": stats_normal}
```

**Visual Analysis**:

```python
import matplotlib.pyplot as plt

def visualize_threshold_separation(metrics_samples, incident_id):
    """
    Plot metric distribution to visualize threshold placement.
    """
    incident_samples = [s for s in metrics_samples if s["incident_id"] == incident_id]
    
    during = [s["value"] for s in incident_samples if s["incident_phase"] == "during"]
    before_after = [s["value"] for s in incident_samples if s["incident_phase"] in ["before", "after"]]
    
    plt.figure(figsize=(10, 6))
    
    # Plot histograms
    plt.hist(before_after, bins=50, alpha=0.5, label="Normal", color="green")
    plt.hist(during, bins=50, alpha=0.5, label="During Incident", color="red")
    
    # Show proposed threshold
    threshold = min(during) if during else np.mean(before_after) + 3 * np.std(before_after)
    plt.axvline(threshold, color="blue", linestyle="--", label=f"Proposed Threshold: {threshold:.2f}")
    
    plt.xlabel("Metric Value")
    plt.ylabel("Frequency")
    plt.title(f"Metric Distribution - Incident {incident_id}")
    plt.legend()
    plt.show()
```

### Threshold Determination Methods

**Method 1: Statistical (Mean + N×StdDev)**

```python
def calculate_statistical_threshold(normal_values, n_std=3):
    """
    Threshold = mean + N * standard_deviation
    
    Common values:
    - 2σ: catches ~95% of normal variation
    - 3σ: catches ~99.7% of normal variation (more conservative)
    """
    mean = np.mean(normal_values)
    std = np.std(normal_values)
    threshold = mean + (n_std * std)
    
    return {
        "threshold": threshold,
        "mean": mean,
        "std": std,
        "method": f"mean + {n_std}σ"
    }
```

**Method 2: Percentile-Based**

```python
def calculate_percentile_threshold(normal_values, percentile=95):
    """
    Threshold = Pth percentile of normal operation
    
    Common values:
    - P90: 10% of normal samples exceed (sensitive)
    - P95: 5% of normal samples exceed (balanced)
    - P99: 1% of normal samples exceed (conservative)
    """
    threshold = np.percentile(normal_values, percentile)
    
    return {
        "threshold": threshold,
        "percentile": percentile,
        "method": f"P{percentile}"
    }
```

**Method 3: SLO-Based**

```python
def calculate_slo_threshold(slo_target, burn_rate_multiplier):
    """
    For SLO-based alerts (error budget burn rate).
    
    Example: 99.9% SLO = 0.1% error budget
    14.4x burn rate = consuming 2% budget/hour
    """
    error_budget = 1 - slo_target
    threshold = error_budget * burn_rate_multiplier
    
    return {
        "threshold": threshold,
        "slo_target": slo_target,
        "error_budget": error_budget,
        "burn_rate": burn_rate_multiplier,
        "time_to_exhaustion_hours": 100 / (burn_rate_multiplier * 100 * error_budget)
    }

# Example
slo_threshold = calculate_slo_threshold(slo_target=0.999, burn_rate_multiplier=14.4)
# Result: threshold=0.00144 (0.144%), exhaustion in ~2 hours
```

**Method 4: Separation Point**

```python
def calculate_separation_threshold(normal_values, incident_values, buffer_pct=10):
    """
    Find the gap between normal and incident, add buffer.
    
    Best when there's clear separation between states.
    """
    max_normal = max(normal_values)
    min_incident = min(incident_values)
    
    if min_incident <= max_normal:
        # Overlap! No clean separation
        return {
            "threshold": None,
            "error": "No separation between normal and incident values",
            "max_normal": max_normal,
            "min_incident": min_incident
        }
    
    # Threshold in the gap, closer to incident side
    gap = min_incident - max_normal
    buffer = gap * (buffer_pct / 100)
    threshold = max_normal + buffer
    
    return {
        "threshold": threshold,
        "max_normal": max_normal,
        "min_incident": min_incident,
        "gap": gap,
        "buffer": buffer,
        "method": f"separation + {buffer_pct}% buffer"
    }
```

### For Clause Sizing

**Purpose**: Determine how long to wait before firing alert.

**Formula**:
```
for_duration = max(
    2 × scrape_interval,
    metric_oscillation_period,
    time_to_user_impact
)
```

**Implementation**:

```python
def calculate_for_clause_duration(metrics_samples, scrape_interval=30):
    """
    Determine appropriate 'for' duration based on metric behavior.
    """
    # Calculate time between value changes
    timestamps = [s["timestamp"] for s in metrics_samples]
    timestamps.sort()
    
    time_diffs = []
    for i in range(1, len(timestamps)):
        diff = (datetime.fromisoformat(timestamps[i]) - 
                datetime.fromisoformat(timestamps[i-1])).total_seconds()
        time_diffs.append(diff)
    
    # Oscillation period = typical time between up/down swings
    oscillation_period = np.median(time_diffs) if time_diffs else scrape_interval
    
    # Minimum: 2× scrape interval
    min_duration = 2 * scrape_interval
    
    # Recommended: 5× scrape interval or oscillation period, whichever is longer
    recommended_duration = max(min_duration, 5 * scrape_interval, oscillation_period)
    
    # Round to reasonable values (5m, 10m, 15m, 30m)
    reasonable_durations = [300, 600, 900, 1800]  # 5m, 10m, 15m, 30m
    final_duration = min(reasonable_durations, key=lambda x: abs(x - recommended_duration))
    
    return {
        "recommended_seconds": final_duration,
        "recommended_minutes": final_duration / 60,
        "reasoning": {
            "scrape_interval": scrape_interval,
            "oscillation_period": oscillation_period,
            "min_safe": min_duration
        }
    }
```

**Decision Matrix**:

| Metric Type | Volatility | Recommended For Duration |
|-------------|------------|--------------------------|
| **CPU** | High (spiky) | 10-15m |
| **Memory** | Low (gradual) | 5-10m |
| **Disk** | Very low | 30m |
| **Error rate** | Medium | 10m |
| **Latency** | High | 15m |
| **Network** | High | 10-15m |

---

## Alert Consolidation & Deduplication

### Redundancy Detection

**Correlation Coefficient Calculation**:

```python
def calculate_alert_correlation(firing_history, alert_a, alert_b):
    """
    Calculate how often two alerts fire together.
    
    Correlation = |A ∩ B| / min(|A|, |B|)
    Where:
    - |A ∩ B| = incidents where both fire
    - |A| = total incidents where A fires
    - |B| = total incidents where B fires
    """
    # Group firings by time window (1-minute buckets)
    from collections import defaultdict
    
    buckets_a = set()
    buckets_b = set()
    
    for event in firing_history:
        timestamp = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
        bucket = timestamp.replace(second=0, microsecond=0)  # Round to minute
        
        if event["alert_name"] == alert_a:
            buckets_a.add(bucket)
        elif event["alert_name"] == alert_b:
            buckets_b.add(bucket)
    
    # Calculate intersection
    intersection = buckets_a & buckets_b
    
    if not buckets_a or not buckets_b:
        return 0.0
    
    correlation = len(intersection) / min(len(buckets_a), len(buckets_b))
    
    return {
        "correlation": correlation,
        "alert_a_fires": len(buckets_a),
        "alert_b_fires": len(buckets_b),
        "together_fires": len(intersection)
    }
```

**Finding All Redundant Pairs**:

```python
def find_all_redundant_pairs(firing_history, correlation_threshold=0.8):
    """
    Find all alert pairs with correlation above threshold.
    """
    from itertools import combinations
    
    # Get unique alert names
    alert_names = set(event["alert_name"] for event in firing_history)
    
    redundant_pairs = []
    
    # Check all pairs
    for alert_a, alert_b in combinations(alert_names, 2):
        corr = calculate_alert_correlation(firing_history, alert_a, alert_b)
        
        if corr["correlation"] >= correlation_threshold:
            redundant_pairs.append({
                "alert_a": alert_a,
                "alert_b": alert_b,
                **corr
            })
    
    # Sort by correlation (highest first)
    redundant_pairs.sort(key=lambda x: x["correlation"], reverse=True)
    
    return redundant_pairs
```

### Consolidation Strategies

**Strategy 1: Merge into Composite Alert**

```yaml
# Before: Three separate alerts
- alert: HighCPU
  expr: cpu > 90
  for: 10m

- alert: HighMemory
  expr: memory > 90
  for: 10m

- alert: HighLoad
  expr: load > 8
  for: 10m

# After: One consolidated alert
- alert: ResourceExhaustion
  expr: |
    (cpu > 90 OR memory > 90 OR load > 8)
  for: 10m
  labels:
    severity: warning
    alert_type: resource
  annotations:
    summary: "Resource exhaustion on {{ $labels.instance }}"
    description: |
      Multiple resource metrics elevated:
      CPU: {{ query "cpu{instance='{{ $labels.instance }}'}" | first | value }}%
      Memory: {{ query "memory{instance='{{ $labels.instance }}'}" | first | value }}%
      Load: {{ query "load{instance='{{ $labels.instance }}'}" | first | value }}
```

**Strategy 2: Alert Hierarchy with Inhibition**

```yaml
# Keep separate alerts but use inhibition rules
alerts:
  - alert: NodeDown
    expr: up == 0
    for: 5m
    labels:
      severity: critical

  - alert: HighCPU
    expr: cpu > 90
    for: 10m
    labels:
      severity: warning

# In Alertmanager
inhibit_rules:
  - source_match:
      alertname: NodeDown
    target_match:
      alertname: HighCPU
    equal: ['instance']
# When NodeDown fires, suppress HighCPU for that instance
```

**Strategy 3: Promote Most Important, Demote Others**

```yaml
# Identify primary alert (user-facing symptom)
- alert: HighErrorRate  # PRIMARY - keep at critical
  expr: error_rate > 0.01
  labels:
    severity: critical
    alert_type: symptom

# Demote correlated cause alerts to info
- alert: DatabaseConnectionPoolFull  # SECONDARY - demote
  expr: db_connections > 95%
  labels:
    severity: info  # Changed from warning
    alert_type: cause
# Still fires, but doesn't page. Provides context.
```

### Consolidation Decision Matrix

| Correlation | Relationship | Action |
|-------------|-------------|--------|
| **> 95%** | Always together, same root cause | Merge into single alert |
| **80-95%** | Usually together | Consider merging OR use inhibition |
| **60-80%** | Often together | Use inhibition (parent → child) |
| **< 60%** | Sometimes together | Keep separate |

### Safe Consolidation Checklist

Before merging alerts:

- [ ] Correlation coefficient calculated (> 80%)
- [ ] Both alerts cover same incidents in historical data
- [ ] Merged expression includes OR logic for all conditions
- [ ] Annotations include details from both original alerts
- [ ] Coverage verified: all incidents still covered after merge
- [ ] Team approval obtained
- [ ] Rollback plan defined

---

## Safety Checks & Validation

### Pre-Removal Checklist

Before removing or significantly changing an alert:

```python
def safety_check_before_removal(alert_name, correlations, firing_history):
    """
    Perform safety checks before removing an alert.
    """
    checks = {
        "covers_incidents": False,
        "referenced_in_runbooks": None,  # Manual check required
        "firing_frequency": 0,
        "last_fired": None,
        "redundancy_confirmed": False,
        "team_approval": None  # Manual check required
    }
    
    # Check 1: Does it cover any incidents?
    for corr in correlations:
        alert_names = [a["alert_name"] for a in corr["matching_alerts"]]
        if alert_name in alert_names:
            checks["covers_incidents"] = True
            break
    
    # Check 2: Firing frequency
    alert_fires = [e for e in firing_history if e["alert_name"] == alert_name]
    checks["firing_frequency"] = len(alert_fires)
    
    if alert_fires:
        last_fire = max(alert_fires, key=lambda x: x["timestamp"])
        checks["last_fired"] = last_fire["timestamp"]
    
    # Check 3: Redundancy
    # (Requires running redundancy detection first)
    
    # Decision
    if checks["covers_incidents"]:
        checks["recommendation"] = "DO NOT REMOVE - covers incidents"
    elif checks["firing_frequency"] == 0:
        checks["recommendation"] = "SAFE TO REMOVE - never fires"
    elif checks["firing_frequency"] < 5:
        checks["recommendation"] = "LIKELY SAFE - fires rarely, check coverage"
    else:
        checks["recommendation"] = "INVESTIGATE - fires regularly, determine purpose"
    
    return checks
```

### PromQL Syntax Validation

**Using promtool**:

```bash
# Validate alert rules file
promtool check rules tuned_rules.yaml

# Test specific expression
promtool query instant http://prometheus:9090 \
  '(sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))) * 100'
```

**Python Validation Wrapper**:

```python
import subprocess
import json

def validate_promql_syntax(expression, prometheus_url):
    """
    Validate PromQL expression by querying Prometheus.
    """
    try:
        result = subprocess.run(
            [
                "promtool", "query", "instant",
                prometheus_url,
                expression
            ],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return {"valid": True, "message": "Syntax OK"}
        else:
            return {
                "valid": False,
                "error": result.stderr,
                "message": "Syntax error in PromQL"
            }
    except subprocess.TimeoutExpired:
        return {"valid": False, "error": "Query timeout"}
    except FileNotFoundError:
        return {"valid": False, "error": "promtool not found"}

# Validate all expressions in tuned rules
def validate_all_rules(rules_file, prometheus_url):
    """
    Validate all expressions in a rules file.
    """
    import yaml
    
    with open(rules_file) as f:
        rules = yaml.safe_load(f)
    
    results = []
    
    for group in rules.get("groups", []):
        for rule in group.get("rules", []):
            if "expr" in rule:
                validation = validate_promql_syntax(rule["expr"], prometheus_url)
                results.append({
                    "alert": rule.get("alert", rule.get("record")),
                    "valid": validation["valid"],
                    "error": validation.get("error")
                })
    
    return results
```

### Test in Non-Production

**Gradual Rollout Strategy**:

```yaml
# Phase 1: Deploy to staging (1 week)
environment: staging
monitoring:
  - alert_firing_rate
  - incident_coverage
  - false_positive_count

# Phase 2: Canary in production (10% of traffic, 1 week)
environment: production
canary_percentage: 10%
monitoring:
  - compare_old_vs_new_alerts
  - incident_coverage_maintained
  - on_call_feedback

# Phase 3: Gradual rollout (2 weeks)
week_1: 50%
week_2: 100%

# Rollback triggers
rollback_if:
  - incident_missed: true
  - false_positive_rate_increase: "> 50%"
  - on_call_complaints: "> 3"
```

### Coverage Verification

**Before and After Comparison**:

```python
def verify_coverage_maintained(incidents, original_correlations, tuned_correlations):
    """
    Verify that tuned alerts still cover all incidents.
    """
    comparison = []
    
    for incident in incidents:
        incident_id = incident["incident_id"]
        
        # Find coverage in original
        orig_corr = next((c for c in original_correlations if c["incident_id"] == incident_id), None)
        orig_covered = orig_corr["alert_count"] > 0 if orig_corr else False
        orig_alerts = [a["alert_name"] for a in orig_corr["matching_alerts"]] if orig_corr else []
        
        # Find coverage in tuned
        tuned_corr = next((c for c in tuned_correlations if c["incident_id"] == incident_id), None)
        tuned_covered = tuned_corr["alert_count"] > 0 if tuned_corr else False
        tuned_alerts = [a["alert_name"] for a in tuned_corr["matching_alerts"]] if tuned_corr else []
        
        # Determine status
        if not orig_covered and not tuned_covered:
            status = "no_coverage_before_or_after"
        elif orig_covered and tuned_covered:
            status = "coverage_maintained"
        elif orig_covered and not tuned_covered:
            status = "COVERAGE_LOST"  # CRITICAL!
        else:
            status = "coverage_gained"
        
        comparison.append({
            "incident_id": incident_id,
            "severity": incident["severity"],
            "original_covered": orig_covered,
            "tuned_covered": tuned_covered,
            "original_alerts": orig_alerts,
            "tuned_alerts": tuned_alerts,
            "status": status
        })
    
    # Summary
    coverage_lost = [c for c in comparison if c["status"] == "COVERAGE_LOST"]
    
    if coverage_lost:
        return {
            "safe_to_deploy": False,
            "coverage_lost_count": len(coverage_lost),
            "lost_incidents": coverage_lost,
            "message": "CRITICAL: Coverage lost for incidents"
        }
    else:
        return {
            "safe_to_deploy": True,
            "coverage_maintained": True,
            "message": "All incidents still covered"
        }
```

---

## Coverage Matrix Construction

### Matrix Schema

```json
{
  "coverage_matrix": {
    "generated_at": "2025-12-06T08:00:00Z",
    "time_period": "2025-11-24 to 2025-12-01",
    "incidents": [
      {
        "incident_id": "INC-001",
        "start_time": "2025-12-01T14:23:00Z",
        "end_time": "2025-12-01T14:45:00Z",
        "severity": "P1",
        "affected_services": ["payment-api"],
        "original_covering_alerts": ["HighErrorRate", "HighCPU", "HighMemory"],
        "tuned_covering_alerts": ["ErrorBudgetBurnRateFast", "ResourceExhaustion"],
        "coverage_maintained": true,
        "alert_reduction": {
          "before": 3,
          "after": 2,
          "reduction_pct": 33
        }
      }
    ],
    "uncovered_incidents": [],
    "coverage_percentage": 100.0,
    "total_incidents": 15,
    "covered_incidents": 15
  }
}
```

### Generation Implementation

```python
def generate_coverage_matrix(incidents, original_correlations, tuned_correlations):
    """
    Generate complete coverage matrix comparing original vs tuned.
    """
    matrix = {
        "generated_at": datetime.now().isoformat(),
        "incidents": [],
        "uncovered_incidents": [],
        "coverage_percentage": 0.0,
        "total_incidents": len(incidents),
        "covered_incidents": 0
    }
    
    for incident in incidents:
        incident_id = incident["incident_id"]
        
        # Get original coverage
        orig = next((c for c in original_correlations if c["incident_id"] == incident_id), None)
        orig_alerts = [a["alert_name"] for a in orig["matching_alerts"]] if orig else []
        
        # Get tuned coverage
        tuned = next((c for c in tuned_correlations if c["incident_id"] == incident_id), None)
        tuned_alerts = [a["alert_name"] for a in tuned["matching_alerts"]] if tuned else []
        
        # Build incident entry
        incident_entry = {
            "incident_id": incident_id,
            "start_time": incident["start_time"],
            "end_time": incident["end_time"],
            "severity": incident["severity"],
            "affected_services": incident["affected_services"],
            "original_covering_alerts": orig_alerts,
            "tuned_covering_alerts": tuned_alerts,
            "coverage_maintained": len(tuned_alerts) > 0,
            "alert_reduction": {
                "before": len(orig_alerts),
                "after": len(tuned_alerts),
                "reduction_pct": ((len(orig_alerts) - len(tuned_alerts)) / len(orig_alerts) * 100) if orig_alerts else 0
            }
        }
        
        matrix["incidents"].append(incident_entry)
        
        # Track coverage
        if len(tuned_alerts) > 0:
            matrix["covered_incidents"] += 1
        else:
            matrix["uncovered_incidents"].append(incident_id)
    
    # Calculate coverage percentage
    matrix["coverage_percentage"] = (matrix["covered_incidents"] / matrix["total_incidents"]) * 100
    
    return matrix

# Save to file
import json

coverage_matrix = generate_coverage_matrix(incidents, original_correlations, tuned_correlations)

with open("coverage_matrix.json", "w") as f:
    json.dump(coverage_matrix, f, indent=2)
```

---

## Decision Framework

### Decision Tree

```
For each alert:
│
├─ Covers ≥1 incident?
│  ├─ No
│  │  ├─ Fires frequently (>50/month)?
│  │  │  ├─ Yes → MODIFY (tune to reduce noise) or REMOVE if truly useless
│  │  │  └─ No → REMOVE (safe, low impact)
│  │  └─ Never fires?
│  │     └─ REMOVE (dead alert)
│  │
│  └─ Yes (covers incidents)
│     │
│     ├─ Correlation > 0.9 with another alert?
│     │  ├─ Yes
│     │  │  ├─ Both cover same incidents?
│     │  │  │  ├─ Yes → CONSOLIDATE (merge into one)
│     │  │  │  └─ No → KEEP BOTH (different coverage)
│     │  │  └─ One is parent-child relationship?
│     │  │     └─ CREATE INHIBITION RULE
│     │  │
│     │  └─ No (independent alert)
│     │     │
│     │     ├─ Signal/Noise ratio < 0.2 (firing 5x more than incidents)?
│     │     │  ├─ Yes → MODIFY
│     │     │  │  ├─ Flapping? → Add/increase 'for' clause
│     │     │  │  ├─ Threshold too sensitive? → Increase threshold
│     │     │  │  ├─ High cardinality? → Aggregate labels
│     │     │  │  └─ Time-of-day pattern? → Add traffic threshold
│     │     │  │
│     │     │  └─ No (good signal/noise) → KEEP
│     │     │
│     │     └─ Leading indicator (fires before incident)?
│     │        └─ KEEP (valuable early warning)
```

### KEEP Decision Criteria

Keep alert if:
- ✅ Covers ≥1 incident
- ✅ No redundant alternative exists
- ✅ Signal-to-noise ratio > 0.3 (1 incident per 3 firings or better)
- ✅ Required by SLO/compliance
- ✅ Leading indicator (fires before incident)
- ✅ Team explicitly requests to keep it

### MODIFY Decision Criteria

Modify alert if:
- ⚠️ Covers incidents but too noisy (signal/noise < 0.3)
- ⚠️ Threshold analysis shows better value exists
- ⚠️ Missing `for` clause causing flapping
- ⚠️ Wrong aggregation causing cardinality explosion
- ⚠️ Time-of-day pattern causing false positives

**Modification Types**:
1. **Adjust threshold**: Based on metric distribution analysis
2. **Add/tune `for` clause**: Based on oscillation period
3. **Aggregate labels**: Reduce cardinality
4. **Add minimum traffic threshold**: Prevent low-traffic false positives
5. **Split by environment**: Separate staging/prod thresholds

### REMOVE Decision Criteria

Remove alert if:
- ❌ No incident coverage
- ❌ Fully redundant with another alert (correlation > 95%)
- ❌ Service decommissioned
- ❌ Always false positive (0% accuracy)
- ❌ Never fires (dead alert)

**Safety Check Before Removal**:
```python
can_remove = (
    not covers_incidents and
    (never_fires or always_false_positive) and
    not required_by_compliance and
    team_approved_removal
)
```

### CONSOLIDATE Decision Criteria

Consolidate alerts if:
- 🔗 Correlation > 0.9 with other alert
- 🔗 Same root cause, different symptoms
- 🔗 Can merge without coverage loss
- 🔗 Both alerts cover exact same incidents

**Consolidation Safety Check**:
```python
can_consolidate = (
    correlation > 0.9 and
    set(incidents_a) == set(incidents_b) and
    team_approved_consolidation
)
```

---

## Edge Case Handling

This section provides detailed solutions for the 14 common edge cases in alert tuning.

### Edge Case 1: Flapping Alerts

**Symptoms**: 10+ fires in 1 hour, rapid fire/resolve cycles

**Root Causes**:
1. No `for` clause
2. Threshold at inflection point (metric oscillates around it)
3. Using `irate()` in expression

**Solution**:

```python
def fix_flapping_alert(alert_rule, metrics_samples):
    """
    Automatically suggest fix for flapping alert.
    """
    fixes = []
    
    # Check 1: Missing 'for' clause
    if "for" not in alert_rule or alert_rule["for"] == "0s":
        # Calculate appropriate duration
        for_duration = calculate_for_clause_duration(metrics_samples)
        fixes.append({
            "issue": "missing_for_clause",
            "fix": f"Add 'for: {for_duration['recommended_minutes']:.0f}m'",
            "new_for": f"{for_duration['recommended_minutes']:.0f}m"
        })
    
    # Check 2: Using irate()
    if "irate(" in alert_rule["expr"]:
        fixes.append({
            "issue": "using_irate",
            "fix": "Replace irate() with rate()",
            "new_expr": alert_rule["expr"].replace("irate(", "rate(")
        })
    
    # Check 3: Threshold oscillation
    # Analyze if metric oscillates around current threshold
    threshold = extract_threshold_from_expr(alert_rule["expr"])
    if threshold:
        values = [s["value"] for s in metrics_samples]
        crosses = sum(1 for i in range(1, len(values)) 
                     if (values[i-1] < threshold) != (values[i] < threshold))
        
        if crosses > len(values) * 0.3:  # More than 30% oscillation
            # Suggest new threshold
            dist_analysis = analyze_metric_distribution(metrics_samples)
            fixes.append({
                "issue": "threshold_oscillation",
                "fix": f"Increase threshold from {threshold} to {dist_analysis['proposed_threshold']}",
                "new_threshold": dist_analysis['proposed_threshold']
            })
    
    return fixes
```

**Example Before/After**:

```yaml
# BEFORE: Flapping
- alert: HighCPU
  expr: cpu > 80
  # Fires whenever CPU briefly spikes above 80%

# AFTER: Fixed
- alert: HighCPU
  expr: cpu > 85  # Increased threshold
  for: 10m       # Added time tolerance
  # Only fires when CPU sustained above 85% for 10 minutes
```

### Edge Case 2: Near-Miss Timing

**Symptoms**: Alert fires 2+ minutes AFTER incident starts

**Problem**: Threshold too conservative, misses early detection

**Solution**:

```python
def fix_late_firing_alert(alert_name, incidents, firing_history, metrics_samples):
    """
    Tune alert to fire earlier by analyzing incident start vs alert fire time.
    """
    # Find incidents where this alert fired late
    late_fires = []
    
    for incident in incidents:
        incident_start = datetime.fromisoformat(incident["start_time"].replace("Z", "+00:00"))
        
        # Find when alert fired for this incident
        alert_fires = [
            f for f in firing_history
            if f["alert_name"] == alert_name and
            labels_match(f["labels"], incident)
        ]
        
        if alert_fires:
            first_fire = min(alert_fires, key=lambda x: x["timestamp"])
            fire_time = datetime.fromisoformat(first_fire["timestamp"].replace("Z", "+00:00"))
            delay = (fire_time - incident_start).total_seconds()
            
            if delay > 120:  # More than 2 minutes late
                late_fires.append({
                    "incident_id": incident["incident_id"],
                    "delay_seconds": delay,
                    "fire_time": first_fire["timestamp"]
                })
    
    if not late_fires:
        return {"needs_tuning": False}
    
    # Analyze metrics at incident start to find better threshold
    avg_delay = np.mean([f["delay_seconds"] for f in late_fires])
    
    # Get metric values at incident start time
    incident_start_values = []
    for incident in incidents:
        incident_start = datetime.fromisoformat(incident["start_time"].replace("Z", "+00:00"))
        
        # Find metric value at incident start
        nearest_sample = min(
            metrics_samples,
            key=lambda s: abs(
                (datetime.fromisoformat(s["timestamp"].replace("Z", "+00:00")) - incident_start).total_seconds()
            )
        )
        incident_start_values.append(nearest_sample["value"])
    
    # New threshold = value at incident start (minus small buffer)
    proposed_threshold = min(incident_start_values) * 0.95  # 5% buffer
    
    return {
        "needs_tuning": True,
        "current_delay_avg": avg_delay,
        "late_fire_count": len(late_fires),
        "proposed_threshold": proposed_threshold,
        "reasoning": f"Alert currently fires {avg_delay:.0f}s after incidents. Lower threshold to catch earlier."
    }
```

**Example Before/After**:

```yaml
# BEFORE: Fires late
- alert: HighErrorRate
  expr: error_rate > 0.05  # 5%
  for: 5m
  # Incident starts when error rate hits 2%, but alert doesn't fire until 5%
  # Fires 3 minutes after incident starts

# AFTER: Tuned to fire earlier
- alert: HighErrorRate
  expr: error_rate > 0.02  # 2% (lowered threshold)
  for: 5m
  # Now fires when error rate hits 2%, catching incident at start
```

### Edge Case 3: Redundant Alerts

**Symptoms**: Two alerts always fire together (>90% correlation)

**Solution**: Consolidate into single alert

```python
def consolidate_redundant_alerts(alert_a, alert_b, correlation_data):
    """
    Merge two redundant alerts into one.
    """
    # Determine which alert is primary (more specific or symptom-based)
    if "error" in alert_a["alert"].lower() or "availability" in alert_a["alert"].lower():
        primary = alert_a
        secondary = alert_b
    else:
        primary = alert_b
        secondary = alert_a
    
    # Create consolidated alert
    consolidated = {
        "alert": f"{primary['alert']}Or{secondary['alert']}",
        "expr": f"({primary['expr']}) OR ({secondary['expr']})",
        "for": primary.get("for", secondary.get("for", "5m")),
        "labels": primary.get("labels", {}),
        "annotations": {
            "summary": f"{primary['annotations']['summary']} (consolidated with {secondary['alert']})",
            "description": f"""
            This alert fires when either condition is met:
            1. {primary['annotations'].get('description', primary['alert'])}
            2. {secondary['annotations'].get('description', secondary['alert'])}
            
            Consolidated from {primary['alert']} and {secondary['alert']} (correlation: {correlation_data['correlation']:.0%})
            """
        }
    }
    
    return {
        "consolidated_alert": consolidated,
        "removed_alerts": [alert_a["alert"], alert_b["alert"]],
        "justification": f"Correlation {correlation_data['correlation']:.0%}, always fire together"
    }
```

**Example Before/After**:

```yaml
# BEFORE: Two always-together alerts
- alert: HighCPU
  expr: cpu > 90
  for: 10m

- alert: HighMemory
  expr: memory > 90
  for: 10m

- alert: HighLoad
  expr: load > 8
  for: 10m

# Correlation: 95% - always fire together

# AFTER: Consolidated
- alert: ResourceExhaustion
  expr: (cpu > 90 OR memory > 90 OR load > 8)
  for: 10m
  labels:
    severity: warning
  annotations:
    summary: "Resource exhaustion on {{ $labels.instance }}"
    description: |
      Multiple resources are exhausted:
      CPU: {{ query "cpu{instance='{{ $labels.instance }}'}" | first | value }}%
      Memory: {{ query "memory{instance='{{ $labels.instance }}'}" | first | value }}%
      Load: {{ query "load{instance='{{ $labels.instance }}'}" | first | value }}
```

### Edge Case 4: High-Cardinality Explosion

**Symptoms**: Alert creates 100+ instances

**Solution**: Aggregate labels

```python
def fix_high_cardinality_alert(alert_rule, firing_history, cardinality_threshold=50):
    """
    Fix high-cardinality alert by suggesting aggregation.
    """
    # Find which labels cause high cardinality
    label_cardinality = defaultdict(set)
    
    for event in firing_history:
        if event["alert_name"] == alert_rule["alert"]:
            for label_name, label_value in event["labels"].items():
                label_cardinality[label_name].add(label_value)
    
    # Identify problem labels
    high_card_labels = {
        label: len(values)
        for label, values in label_cardinality.items()
        if len(values) > cardinality_threshold
    }
    
    if not high_card_labels:
        return {"needs_fix": False}
    
    # Suggest aggregation
    # Remove high-cardinality labels from query, aggregate by low-cardinality labels
    low_card_labels = [
        label for label in label_cardinality.keys()
        if label not in high_card_labels and len(label_cardinality[label]) < 20
    ]
    
    # Modify expression to aggregate
    # This is simplified - actual implementation would need PromQL parsing
    suggested_expr = alert_rule["expr"]
    
    if low_card_labels:
        # Add aggregation by low-cardinality labels
        aggregation_labels = ", ".join(low_card_labels)
        if "sum(" not in suggested_expr and "avg(" not in suggested_expr:
            suggested_expr = f"avg by({aggregation_labels}) ({suggested_expr})"
    
    return {
        "needs_fix": True,
        "high_cardinality_labels": high_card_labels,
        "suggested_aggregation_labels": low_card_labels,
        "original_expr": alert_rule["expr"],
        "suggested_expr": suggested_expr,
        "estimated_reduction": f"{len(high_card_labels[list(high_card_labels.keys())[0]])} → {len(low_card_labels)} instances"
    }
```

**Example Before/After**:

```yaml
# BEFORE: Per-pod alert (1000 pods = 1000 alerts)
- alert: HighCPU
  expr: container_cpu_usage{pod=~".*"} > 0.9
  # Creates separate alert for EVERY pod

# AFTER: Aggregate by service
- alert: HighCPUByService
  expr: |
    avg by(service, namespace) (container_cpu_usage) > 0.8
  # Creates one alert per service
  annotations:
    summary: "Service {{ $labels.service }} high CPU"
    description: |
      Average CPU: {{ $value | humanizePercentage }}
      Affected pods: {{ query "count(container_cpu_usage{service='{{ $labels.service }}'} > 0.9)" | first | value }}
```

### Edge Case 5: Missing `for` Clause

**Solution**: Calculate appropriate duration

```python
# Already covered in Flapping Alerts section
# Use calculate_for_clause_duration() function
```

### Edge Case 6: Threshold Too Sensitive

**Solution**: Analyze metric distribution

```python
# Already covered in Threshold Optimization section
# Use analyze_metric_distribution() and calculate_statistical_threshold()
```

### Edge Case 7: Broken Expression

**Symptoms**: PromQL syntax error, query returns no results

**Solution**:

```bash
# Validate syntax
promtool check rules alert_rules.yaml

# Test expression
promtool query instant http://prometheus:9090 'your_expression_here'
```

Common fixes:
1. **Missing closing parenthesis**: Count `(` and `)`
2. **Wrong label matcher**: `{label="value"}` not `{label=value}`
3. **Invalid function**: Check function name spelling
4. **Missing rate() on counter**: Counters must use `rate()` or `increase()`

### Edge Case 8: Orphan Alert

**Symptoms**: Alert for decommissioned service

**Solution**:

```python
def identify_orphan_alerts(alert_rules, service_catalog):
    """
    Find alerts for services that no longer exist.
    """
    active_services = set(service["name"] for service in service_catalog["services"])
    
    orphan_alerts = []
    
    for rule in alert_rules:
        # Extract service from labels or expression
        service = extract_service_from_alert(rule)
        
        if service and service not in active_services:
            orphan_alerts.append({
                "alert": rule["alert"],
                "service": service,
                "recommendation": "REMOVE - service decommissioned"
            })
    
    return orphan_alerts
```

### Edge Case 9: Indirect Correlation (Leading Indicator)

**Symptoms**: Alert fires 5 min before incident, not during

**Solution**: **KEEP the alert** - it's a valuable early warning!

```python
def identify_leading_indicators(correlations):
    """
    Find alerts that fire BEFORE incidents (leading indicators).
    """
    leading_indicators = []
    
    for corr in correlations:
        for alert in corr["matching_alerts"]:
            if alert["time_before_incident"] < -300:  # More than 5 min before
                leading_indicators.append({
                    "alert_name": alert["alert_name"],
                    "incident_id": corr["incident_id"],
                    "lead_time_seconds": abs(alert["time_before_incident"]),
                    "recommendation": "KEEP - valuable early warning"
                })
    
    return leading_indicators
```

### Edge Case 10: Split-Brain Alerts (Environment-Specific)

**Symptoms**: Same alert, different thresholds for staging vs prod

**Solution**: **Preserve** environment-specific logic

```yaml
# CORRECT: Different thresholds for different environments
- alert: HighErrorRate
  expr: |
    (error_rate{environment="production"} > 0.01)
    OR
    (error_rate{environment="staging"} > 0.05)
  for: 10m
  labels:
    severity: '{{ if eq $labels.environment "production" }}critical{{ else }}warning{{ end }}'
  # Production: 1% threshold, critical
  # Staging: 5% threshold, warning
```

### Edge Case 11: Composite Incident Coverage (OR Relationship)

**Symptoms**: Incident covered by alert A OR B, never both

**Solution**: **Keep both** alerts - they cover different scenarios

```python
def identify_or_relationships(correlations):
    """
    Find incidents covered by A OR B (not both).
    """
    or_relationships = []
    
    # Group incidents by covering alerts
    alert_coverage = defaultdict(list)
    
    for corr in correlations:
        for alert in corr["matching_alerts"]:
            alert_coverage[alert["alert_name"]].append(corr["incident_id"])
    
    # Find alert pairs where each covers different incidents
    for alert_a in alert_coverage:
        for alert_b in alert_coverage:
            if alert_a >= alert_b:  # Avoid duplicates
                continue
            
            incidents_a = set(alert_coverage[alert_a])
            incidents_b = set(alert_coverage[alert_b])
            
            # Check for OR relationship (little overlap)
            overlap = incidents_a & incidents_b
            if len(overlap) < 0.2 * min(len(incidents_a), len(incidents_b)):
                or_relationships.append({
                    "alert_a": alert_a,
                    "alert_b": alert_b,
                    "incidents_only_a": list(incidents_a - incidents_b),
                    "incidents_only_b": list(incidents_b - incidents_a),
                    "recommendation": "KEEP BOTH - cover different scenarios"
                })
    
    return or_relationships
```

### Edge Case 12: Night/Day Pattern

**Solution**: Add time-of-day logic or minimum traffic threshold

```yaml
# Solution 1: Time-of-day recording rule
recording_rules:
  - record: baseline:error_rate:hourly
    expr: |
      avg_over_time(
        (sum(rate(http_requests_total{status=~"5.."}[5m])) by (service) /
         sum(rate(http_requests_total[5m])) by (service))[1h:5m] offset 1w
      )

alerts:
  - alert: ErrorRateAboveBaseline
    expr: |
      (
        sum(rate(http_requests_total{status=~"5.."}[5m])) by (service) /
        sum(rate(http_requests_total[5m])) by (service)
      ) / baseline:error_rate:hourly > 2
    # Fires when error rate is 2x the baseline for this hour

# Solution 2: Minimum traffic threshold (simpler)
- alert: HighErrorRate
  expr: |
    (error_rate > 0.01)
    AND
    (request_rate > 10)  # Only when sufficient traffic
```

### Edge Case 13: Pending Never Firing

**Symptoms**: Alert stuck in "pending" state, never reaches "firing"

**Cause**: `for` clause too long, condition doesn't sustain

**Solution**:

```python
def fix_pending_alert(alert_rule, firing_history):
    """
    Detect and fix alerts that never fire (stuck pending).
    """
    # Check if alert appears in firing history
    fires = [e for e in firing_history if e["alert_name"] == alert_rule["alert"]]
    
    if len(fires) == 0:
        # Never fired - likely stuck pending
        current_for = parse_duration(alert_rule.get("for", "0s"))
        
        if current_for > 600:  # More than 10 minutes
            recommended_for = max(300, current_for // 2)  # Halve it, minimum 5m
            
            return {
                "issue": "never_fires_pending",
                "current_for": f"{current_for // 60}m",
                "recommended_for": f"{recommended_for // 60}m",
                "reasoning": "For clause too long, condition doesn't sustain"
            }
    
    return {"needs_fix": False}
```

### Edge Case 14: Label Mismatch

**Solution**: Normalize labels (covered in Data Preparation section)

---

## Reporting & Documentation

### Analysis Report Structure

Generate comprehensive report documenting all decisions:

```python
def generate_analysis_report(
    original_rules,
    tuned_rules,
    firing_history,
    incidents,
    correlations,
    decisions
):
    """
    Generate complete analysis report.
    """
    report = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "analysis_period": {
                "start": min(f["timestamp"] for f in firing_history),
                "end": max(f["timestamp"] for f in firing_history)
            },
            "analyst": "SRE Team",
            "tool_version": "1.0.0"
        },
        
        "executive_summary": {
            "original_alert_count": len(original_rules),
            "tuned_alert_count": len(tuned_rules),
            "removed_count": len([d for d in decisions if d["action"] == "REMOVE"]),
            "modified_count": len([d for d in decisions if d["action"] == "MODIFY"]),
            "consolidated_count": len([d for d in decisions if d["action"] == "CONSOLIDATE"]),
            "kept_count": len([d for d in decisions if d["action"] == "KEEP"]),
            
            "impact": {
                "original_monthly_firings": len(firing_history) * 30 / 7,  # Extrapolate to monthly
                "projected_monthly_firings": calculate_projected_firings(tuned_rules, firing_history),
                "reduction_percentage": None  # Calculate below
            },
            
            "coverage": {
                "total_incidents": len(incidents),
                "incidents_covered_before": len([c for c in correlations if c["alert_count"] > 0]),
                "incidents_covered_after": None,  # From coverage matrix
                "coverage_percentage": None
            }
        },
        
        "alerts": [],
        "consolidations": [],
        "coverage_gaps": [],
        "recommendations": []
    }
    
    # Calculate reduction percentage
    original_monthly = report["executive_summary"]["impact"]["original_monthly_firings"]
    projected_monthly = report["executive_summary"]["impact"]["projected_monthly_firings"]
    report["executive_summary"]["impact"]["reduction_percentage"] = \
        ((original_monthly - projected_monthly) / original_monthly) * 100
    
    # Add per-alert details
    for decision in decisions:
        alert_detail = {
            "alert_name": decision["alert_name"],
            "action": decision["action"],
            "reason": decision["reason"],
            "original_firings_7d": decision.get("original_firings", 0),
            "incidents_covered": decision.get("incidents_covered", []),
            "changes_made": decision.get("changes", []),
            "projected_firings_7d": decision.get("projected_firings", 0)
        }
        report["alerts"].append(alert_detail)
    
    return report

# Save report
import json

report = generate_analysis_report(...)
with open("analysis_report.json", "w") as f:
    json.dump(report, f, indent=2)
```

### Human-Readable Summary

Generate markdown summary for stakeholders:

```python
def generate_markdown_summary(report):
    """
    Generate human-readable markdown summary.
    """
    md = f"""
# Alert Tuning Analysis Report

**Generated**: {report["metadata"]["generated_at"]}
**Analysis Period**: {report["metadata"]["analysis_period"]["start"]} to {report["metadata"]["analysis_period"]["end"]}

## Executive Summary

### Alert Reduction
- **Original alert count**: {report["executive_summary"]["original_alert_count"]}
- **Tuned alert count**: {report["executive_summary"]["tuned_alert_count"]}
- **Reduction**: {report["executive_summary"]["removed_count"]} removed, {report["executive_summary"]["consolidated_count"]} consolidated

### Impact
- **Original monthly firings**: {report["executive_summary"]["impact"]["original_monthly_firings"]:.0f}
- **Projected monthly firings**: {report["executive_summary"]["impact"]["projected_monthly_firings"]:.0f}
- **Reduction**: {report["executive_summary"]["impact"]["reduction_percentage"]:.1f}%

### Coverage
- **Total incidents**: {report["executive_summary"]["coverage"]["total_incidents"]}
- **Coverage maintained**: {report["executive_summary"]["coverage"]["coverage_percentage"]:.1f}%

## Actions Taken

### Removed Alerts ({report["executive_summary"]["removed_count"]})
"""
    
    removed = [a for a in report["alerts"] if a["action"] == "REMOVE"]
    for alert in removed:
        md += f"\n- **{alert['alert_name']}**: {alert['reason']}"
    
    md += f"\n\n### Modified Alerts ({report['executive_summary']['modified_count']})\n"
    
    modified = [a for a in report["alerts"] if a["action"] == "MODIFY"]
    for alert in modified:
        md += f"\n- **{alert['alert_name']}**: {alert['reason']}\n"
        for change in alert.get("changes_made", []):
            md += f"  - {change}\n"
    
    md += f"\n\n### Consolidated Alerts ({report['executive_summary']['consolidated_count']})\n"
    
    for consol in report["consolidations"]:
        md += f"\n- **{consol['new_alert_name']}**: Merged {', '.join(consol['replaced_alerts'])}\n"
        md += f"  - Reason: {consol['reason']}\n"
    
    return md

# Save markdown summary
md_summary = generate_markdown_summary(report)
with open("analysis_summary.md", "w") as f:
    f.write(md_summary)
```

---

## Real-World Case Studies

### Case Study 1: E-Commerce Platform

**Starting Point**:
- 52 alert rules
- 2,800 alerts/month
- 40 real incidents/month
- Signal-to-noise: 1:70
- On-call team burnout

**Analysis Findings**:

```python
# Top 5 noisiest alerts (caused 65% of total noise)
noisy_alerts = [
    {"name": "HighCPU", "fires/month": 450, "incidents_covered": 3},
    {"name": "HighMemory", "fires/month": 380, "incidents_covered": 3},
    {"name": "DiskSpaceLow", "fires/month": 320, "incidents_covered": 2},
    {"name": "HighErrorRate", "fires/month": 280, "incidents_covered": 12},  # Good!
    {"name": "PodRestarting", "fires/month": 250, "incidents_covered": 1}
]

# Redundancy analysis
redundant_pairs = [
    {"alert_a": "HighCPU", "alert_b": "HighMemory", "correlation": 0.95},
    {"alert_a": "HighCPU", "alert_b": "HighLoad", "correlation": 0.92},
    {"alert_a": "DatabaseDown", "alert_b": "DatabaseConnectionPoolExhausted", "correlation": 0.88}
]

# Coverage gaps
gaps = [
    {"incident": "INC-023", "issue": "S3 bucket full", "current_alert": None},
    {"incident": "INC-031", "issue": "API rate limit hit", "current_alert": None}
]
```

**Tuning Actions**:

1. **Consolidated** 3 resource alerts into 1:
   ```yaml
   # Before: HighCPU, HighMemory, HighLoad (3 alerts, 1,150 fires/month)
   # After: ResourceExhaustion (1 alert, estimated 250 fires/month)
   - alert: ResourceExhaustion
     expr: (cpu > 90 OR memory > 90 OR load > 10)
     for: 15m  # Increased from 10m
   ```

2. **Tuned** DiskSpaceLow threshold:
   ```yaml
   # Before: < 20% free, no predictive
   # After: < 10% OR will fill in 4h
   - alert: DiskSpaceLow
     expr: |
       (disk_free_pct < 10)
       OR
       (predict_linear(disk_free_bytes[1h], 4*3600) < 0 AND disk_free_pct > 5)
     for: 30m  # Increased from 10m
   ```

3. **Fixed** PodRestarting cardinality:
   ```yaml
   # Before: Per-pod (250 fires, 1000 pod instances)
   # After: Aggregated by service (estimated 15 fires)
   - alert: ServicePodsRestarting
     expr: |
       (
         rate(kube_pod_container_status_restarts_total[15m]) by (service, namespace) > 0.1
       )
     for: 15m
   ```

4. **Created** 2 new alerts for gaps:
   ```yaml
   - alert: S3BucketNearQuota
     expr: s3_bucket_size / s3_bucket_quota > 0.9
     for: 1h
   
   - alert: APIRateLimitNearLimit
     expr: (api_requests / api_rate_limit) > 0.8
     for: 10m
   ```

**Results**:
- **Alert count**: 52 → 38 (27% reduction)
- **Monthly firings**: 2,800 → 285 (90% reduction)
- **Incident coverage**: 40/40 (100% maintained)
- **Signal-to-noise**: 1:70 → 1:7 (10x improvement)
- **On-call satisfaction**: 3.2/10 → 8.1/10

**Timeline**:
- Week 1-2: Analysis and tuning
- Week 3: Testing in staging
- Week 4-5: Gradual rollout (10% → 50% → 100%)
- Week 6+: Monitoring and iteration

---

### Case Study 2: SaaS Application (High Cardinality Problem)

**Starting Point**:
- 68 alert rules
- 5,200 alerts/month
- 35 real incidents/month
- **Major issue**: Per-user alerts creating cardinality explosion

**Problem Discovery**:

```python
cardinality_analysis = {
    "UserAPIErrorRate": {
        "instances": 2500,  # 2500 users with separate alerts!
        "fires/month": 1800,
        "incidents_covered": 3,
        "high_card_label": "user_id"
    },
    "UserQuotaExceeded": {
        "instances": 1200,
        "fires/month": 950,
        "incidents_covered": 1,
        "high_card_label": "user_id"
    }
}
```

**Tuning Actions**:

1. **Aggregated** per-user alerts to service-level:
   ```yaml
   # Before: Per-user
   - alert: UserAPIErrorRate
     expr: (user_api_errors / user_api_requests) > 0.1
     # 2500 user instances × 1800 fires = noise explosion
   
   # After: Service-level with percentage threshold
   - alert: UsersExperiencingAPIErrors
     expr: |
       (
         count(
           (user_api_errors / user_api_requests) > 0.1
         )
         /
         count(user_api_requests > 0)
       ) > 0.05  # Alert when >5% of active users have errors
     for: 15m
     annotations:
       summary: "{{ $value | humanizePercentage }} of users experiencing API errors"
       affected_users: "{{ query 'count((user_api_errors / user_api_requests) > 0.1)' | first | value }}"
   ```

2. **Created** recording rules for efficient aggregation:
   ```yaml
   recording_rules:
     - record: service:users_with_high_errors:count
       expr: count((user_api_errors / user_api_requests) > 0.1)
     
     - record: service:active_users:count
       expr: count(user_api_requests > 0)
     
     - record: service:users_error_percentage:ratio
       expr: |
         service:users_with_high_errors:count
         /
         service:active_users:count
   
   # Alert uses pre-computed recording rule
   alerts:
     - alert: UsersExperiencingAPIErrors
       expr: service:users_error_percentage:ratio > 0.05
       for: 15m
   ```

**Results**:
- **Alert instances**: 5,200 → 180 (97% reduction)
- **Prometheus memory usage**: 8GB → 2GB
- **Query performance**: 5-8s → <500ms
- **Incident coverage**: 35/35 (100% maintained)
- **Cardinality**: Eliminated per-user metrics in alerts

---

### Case Study 3: Microservices Infrastructure

**Starting Point**:
- 95 alert rules
- 4,500 alerts/month
- 45 real incidents/month
- **Major issue**: Redundant alerts for service dependencies

**Problem Discovery**:

```python
dependency_analysis = {
    "cascade_alerts": [
        {
            "root_cause": "DatabaseDown",
            "fires": 1,
            "triggers_downstream": [
                "APIErrorRate (15 fires)",
                "HighLatency (12 fires)",
                "QueueBacklog (8 fires)",
                "UserAuthFailures (10 fires)"
            ],
            "total_noise": 46  # 1 database issue = 46 alerts
        }
    ]
}
```

**Tuning Actions**:

1. **Implemented** inhibition rules to suppress cascading alerts:
   ```yaml
   # In Alertmanager
   inhibit_rules:
     # Database down inhibits application errors
     - source_match:
         alertname: DatabaseDown
       target_match_re:
         alertname: ".*ErrorRate|.*Latency|.*QueueBacklog"
       equal: ['database', 'cluster']
     
     # Service down inhibits instance alerts
     - source_match:
         alertname: ServiceDown
       target_match_re:
         alertname: ".*Instance.*"
       equal: ['service']
   ```

2. **Created** alert hierarchy (symptom → cause):
   ```yaml
   # Symptom alert (pages)
   - alert: UserFacingErrorRate
     expr: (public_api_errors / public_api_requests) > 0.01
     for: 5m
     labels:
       severity: critical
       alert_type: symptom
       pages: "true"
   
   # Cause alerts (don't page, provide context)
   - alert: DatabaseConnectionPoolExhausted
     expr: (db_connections_active / db_connections_max) > 0.95
     for: 5m
     labels:
       severity: warning
       alert_type: cause
       pages: "false"
   
   - alert: BackendAPIHighLatency
     expr: p99_latency > 5
     for: 10m
     labels:
       severity: warning
       alert_type: cause
       pages: "false"
   ```

3. **Consolidated** 15 redundant microservice alerts:
   ```yaml
   # Before: 15 separate "ServiceDown" alerts (one per microservice)
   # After: 1 alert with dynamic service label
   - alert: MicroserviceDown
     expr: avg by(service) (up{job=~"microservice-.*"}) < 0.5
     for: 5m
     labels:
       severity: critical
       team: "{{ $labels.service }}-team"
     annotations:
       summary: "Microservice {{ $labels.service }} is down"
       healthy_instances: "{{ query 'sum(up{job=\"microservice-{{ $labels.service }}\", state=\"ready\"})' | first | value }}"
       total_instances: "{{ query 'count(up{job=\"microservice-{{ $labels.service }}\"}' | first | value }}"
   ```

**Results**:
- **Alert count**: 95 → 52 (45% reduction)
- **Monthly firings**: 4,500 → 380 (92% reduction)
- **Cascade noise**: Database incident 1 → 46 alerts, now 1 → 3 alerts (93% reduction)
- **Incident coverage**: 45/45 (100%)
- **Mean time to acknowledge**: 8min → 2min (responders see clear root cause)

---

## Conclusion

This methodology provides a systematic approach to alert tuning that:

1. **Reduces noise** by 80-95% while maintaining 100% incident coverage
2. **Improves signal-to-noise ratio** from 1:50 to 1:5 or better
3. **Preserves safety** through rigorous coverage verification
4. **Scales** to organizations with 50-500+ alerts
5. **Documents** all decisions for future reference

**Key Success Factors**:
- Start with data collection (7+ days minimum)
- Focus on top 20% noisiest alerts first (Pareto principle)
- Always verify coverage before removing alerts
- Test in non-production before deploying
- Deploy gradually with monitoring
- Iterate quarterly as systems evolve

**Next Steps**:
1. Collect your firing history and incident data
2. Run the analysis scripts from this document
3. Start with the top 5 noisiest alerts
4. Document your decisions
5. Deploy gradually
6. Monitor and iterate

For additional resources, see:
- **Alert Rules Reference** (`alert-rules-ref.md`) - Examples of good and bad alerts
- **Alert Configuration Patterns** (`alert-config-patterns.md`) - Infrastructure configuration

---

**Document Version**: 1.0
**Last Updated**: 2025-12-06
**Maintainers**: SRE Team
**Feedback**: sre-team@example.com