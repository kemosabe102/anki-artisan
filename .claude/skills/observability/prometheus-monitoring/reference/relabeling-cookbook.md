# Prometheus Relabeling Cookbook

> Practical recipes for label manipulation in Prometheus scrape configurations.

---

## Table of Contents

1. [Overview](#overview)
2. [Actions Reference](#actions-reference)
3. [Configuration Structure](#configuration-structure)
4. [relabel_configs vs metric_relabel_configs](#relabel_configs-vs-metric_relabel_configs)
5. [Cookbook Recipes](#cookbook-recipes)
6. [Performance Considerations](#performance-considerations)
7. [Debugging Tips](#debugging-tips)

---

## Overview

Relabeling enables dynamic rewriting of label sets before scraping (targets) or after scraping (metrics):
- Filtering which targets to scrape
- Filtering which metrics to ingest
- Adding, modifying, or removing labels
- Extracting metadata into labels

---

## Actions Reference

| Action | Description | Required Fields |
|--------|-------------|-----------------|
| `replace` | Replace target_label using regex | `target_label` |
| `keep` | Keep targets where regex matches | `source_labels`, `regex` |
| `drop` | Drop targets where regex matches | `source_labels`, `regex` |
| `labelmap` | Copy label values based on name match | `regex` |
| `labeldrop` | Remove labels matching regex | `regex` |
| `labelkeep` | Keep only labels matching regex | `regex` |
| `hashmod` | Set target_label to hash mod modulus | `source_labels`, `modulus` |
| `lowercase` | Convert to lowercase | `source_labels`, `target_label` |
| `uppercase` | Convert to uppercase | `source_labels`, `target_label` |

---

## Configuration Structure

```yaml
- source_labels: [<label_name>, ...]
  separator: <string>           # Default: ;
  target_label: <label_name>
  regex: <regex>                # Default: (.*)
  modulus: <int>
  replacement: <string>         # Default: $1
  action: <action>              # Default: replace
```

---

## relabel_configs vs metric_relabel_configs

| Aspect | relabel_configs | metric_relabel_configs |
|--------|-----------------|------------------------|
| When | Before scraping | After scraping |
| Operates On | Target labels | Metric labels |
| Access to __meta_ | Yes | No |
| Affects Scrape | Yes | No |

```yaml
scrape_configs:
  - job_name: 'example'
    relabel_configs:      # BEFORE scrape
      - source_labels: [__meta_kubernetes_pod_label_app]
        target_label: app
    metric_relabel_configs:  # AFTER scrape
      - source_labels: [__name__]
        regex: 'go_.*'
        action: drop
```

---

## Cookbook Recipes

### 1. Adding Static Labels

```yaml
relabel_configs:
  - target_label: environment
    replacement: production
  - target_label: team
    replacement: platform
```

### 2. Renaming Labels

```yaml
relabel_configs:
  - source_labels: [old_label]
    target_label: new_label
  - regex: old_label
    action: labeldrop
```

### 3. Dropping High-Cardinality Labels

```yaml
metric_relabel_configs:
  - regex: '(request_id|trace_id|correlation_id)'
    action: labeldrop
```

### 4. Filtering Targets by Label

```yaml
relabel_configs:
  # Keep only enabled targets
  - source_labels: [__meta_kubernetes_pod_annotation_monitoring]
    regex: 'enabled'
    action: keep
  
  # Drop kube-system namespace
  - source_labels: [__meta_kubernetes_namespace]
    regex: 'kube-system'
    action: drop
```

### 5. Filtering Metrics by Name

```yaml
metric_relabel_configs:
  # Drop go_* metrics
  - source_labels: [__name__]
    regex: 'go_.*'
    action: drop
  
  # Keep only specific metrics
  - source_labels: [__name__]
    regex: '(http_requests_total|up)'
    action: keep
```

### 6. Extracting from __meta_ Labels

```yaml
relabel_configs:
  - sourceLabels: [__meta_kubernetes_pod_name]
    target_label: pod
  - source_labels: [__meta_kubernetes_namespace]
    target_label: namespace
  - source_labels: [__meta_kubernetes_pod_label_app]
    target_label: app
  # Copy all pod labels with prefix
  - regex: __meta_kubernetes_pod_label_(.+)
    action: labelmap
    replacement: pod_$1
```

### 7. Hashmod for Sharding

```yaml
relabel_configs:
  # Shard targets across 4 Prometheus instances
  - source_labels: [__address__]
    modulus: 4
    target_label: __tmp_hash
    action: hashmod
  # Instance 0 keeps hash % 4 == 0
  - source_labels: [__tmp_hash]
    regex: '0'
    action: keep
```

### 8. Label Case Transformation

```yaml
relabel_configs:
  - source_labels: [environment]
    target_label: environment
    action: lowercase
```

---

## Performance Considerations

### Ordering Matters

1. Place `drop` actions early
2. Place expensive regex after filtering
3. Use `labeldrop` before `labelkeep`

### Regex Performance

| Pattern | Performance |
|---------|-------------|
| `exact_match` | Fastest |
| `prefix_.*` | Fast |
| `.*_suffix` | Slower |
| `.*middle.*` | Slowest |

### Cardinality Control

```yaml
metric_relabel_configs:
  # Limit histogram buckets
  - source_labels: [__name__, le]
    regex: '(.*_bucket);(0\.1|1|10|\+Inf)'
    action: keep
```

---

## Debugging Tips

### 1. Use Prometheus UI

Navigate to `Status > Targets` to see labels before/after relabeling.

### 2. Test with promtool

```bash
promtool check config prometheus.yml
```

### 3. Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing `action: keep` | Add explicit action |
| Wrong regex escaping | Use `\.` for literal dots |
| Overwriting `__address__` | Use `__tmp_*` labels |

---

## Quick Reference

```yaml
# Add label
- target_label: env
  replacement: prod

# Copy label
- source_labels: [src]
  target_label: dst

# Regex extract
- source_labels: [__address__]
  regex: '(.+):\d+'
  target_label: host
  replacement: '$1'

# Keep matching
- source_labels: [label]
  regex: 'value'
  action: keep

# Drop matching
- source_labels: [__name__]
  regex: 'unwanted_.*'
  action: drop

# Drop label by name
- regex: 'high_cardinality_.*'
  action: labeldrop
```

---

**Source**: Prometheus Documentation via Context7
