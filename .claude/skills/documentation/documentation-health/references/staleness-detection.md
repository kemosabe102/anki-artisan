# Staleness Detection

## Overview

Staleness measures documentation relevance through file age and reference freshness analysis.

---

## File Age Thresholds

### Age Categories

Based on last modified timestamp:

| Category | Age Range | Interpretation | Action Required |
|----------|-----------|----------------|-----------------|
| `fresh` | 0-30 days | Recently updated | None |
| `recent` | 31-90 days | Current documentation | Monitor |
| `aging` | 91-180 days | Approaching staleness | Review soon |
| `stale` | 181-365 days | May contain outdated info | Review recommended |
| `outdated` | >365 days | Likely needs updates | Urgent review |

### Age Calculation

**Method**: File system last modified timestamp

**Command** (example):
```bash
stat -c %Y filename.md  # Unix/Linux (seconds since epoch)
git log -1 --format=%ct filename.md  # Git last commit time
```

**Conversion**:
```
age_days = (current_timestamp - file_modified_timestamp) / 86400
```

**Note**: Use file system timestamp (not git commit time) for files modified but not committed

---

## Reference Freshness Analysis

### Outbound Link Age Distribution

**Process**:
1. Extract all internal links from file
2. Get age category for each linked file
3. Calculate distribution:
   ```
   fresh_links = count(links to fresh files)
   recent_links = count(links to recent files)
   aging_links = count(links to aging files)
   stale_links = count(links to stale files)
   outdated_links = count(links to outdated files)
   total_links = sum of all above
   ```

### Staleness Score Formula

```
staleness_score = (stale_links + 2 × outdated_links) / total_links
```

**Rationale**: Outdated links weighted 2× because they indicate more severe freshness issues

**Range**: 0.0 (all links fresh) to 2.0 (all links outdated)

**Interpretation**:
- 0.0-0.3: Fresh references (healthy)
- 0.31-0.5: Mixed references (monitor)
- 0.51-0.8: Stale references (review needed)
- 0.81-2.0: Outdated references (urgent)

### Example Calculation

**File**: `guide.md` (120 days old, category: `aging`)

**Outbound links**:
- `intro.md` (15 days old, fresh)
- `setup.md` (45 days old, recent)
- `legacy.md` (200 days old, stale)
- `old-api.md` (400 days old, outdated)

**Calculation**:
```
stale_links = 1
outdated_links = 1
total_links = 4

staleness_score = (1 + 2×1) / 4 = 3/4 = 0.75
```

**Result**: Score 0.75 = "Stale references" (review needed)

---

## Staleness Alert Criteria

### Alert Trigger Conditions

File flagged as stale if **ANY** condition met:

1. **Age threshold**: `file_age > 180 days`
2. **Reference threshold**: `staleness_score > 0.5`
3. **Combined threshold**: `file_age > 90 days AND staleness_score > 0.3`

### Alert Severity Levels

| Severity | Criteria | Recommended Action |
|----------|----------|-------------------|
| **Low** | Age 91-180 days, score <0.3 | Schedule review in next quarter |
| **Medium** | Age 181-365 days OR score 0.5-0.8 | Review within 30 days |
| **High** | Age >365 days OR score >0.8 | Review within 7 days |
| **Critical** | Age >730 days AND score >0.8 | Immediate review or archive |

### Alert Output Format

```json
{
  "file": "docs/legacy-guide.md",
  "age_days": 420,
  "age_category": "outdated",
  "staleness_score": 0.83,
  "severity": "high",
  "recommendation": "Review within 7 days - mostly outdated references",
  "link_distribution": {
    "fresh": 0,
    "recent": 1,
    "aging": 2,
    "stale": 3,
    "outdated": 6
  }
}
```

---

## False Positive Handling

### Exceptions

**Stable documentation** (exempt from staleness alerts):
- Architecture decision records (ADRs) - historical by design
- Changelogs - dated content expected
- Legacy guides explicitly marked as archived
- API versioned documentation (e.g., `v1-api.md`)

**Configuration**:
Define exceptions in `DOCS-MANAGEMENT.md`:
```yaml
staleness_exceptions:
  - pattern: "docs/adr/*.md"
    reason: "ADRs are historical records"
  - pattern: "docs/changelog.md"
    reason: "Dated content expected"
```

### Bidirectional Reference Check

**Enhancement**: Reduce false positives by checking if old files are still actively referenced

**Process**:
1. Identify file as potentially stale (age >180 days)
2. Count incoming references from fresh/recent files
3. If `incoming_fresh_refs > 3`, reduce severity by one level

**Rationale**: Frequently referenced old files may still be relevant

---

## Staleness Trend Analysis

### Historical Tracking

**Metric**: Track staleness score over time

**Method**:
1. Calculate staleness score for each file
2. Store with timestamp in trend database
3. Compare current score to previous scan (e.g., 30 days ago)

**Output**:
```json
{
  "file": "docs/guide.md",
  "current_staleness": 0.65,
  "previous_staleness": 0.45,
  "trend": "worsening",
  "delta": 0.20
}
```

**Alerts**:
- Trend "worsening" + delta >0.3 → High priority review
- Trend "improving" → Lower priority

---

## Remediation Recommendations

### Based on Staleness Score

| Score Range | Recommendation | Estimated Effort |
|-------------|----------------|------------------|
| 0.0-0.3 | No action needed | N/A |
| 0.31-0.5 | Review outbound links, update if needed | 15-30 min |
| 0.51-0.8 | Comprehensive review, update content and links | 1-2 hours |
| 0.81-2.0 | Major rewrite or archive recommended | 4+ hours |

### Based on File Age

| Age Category | Recommendation | Estimated Effort |
|--------------|----------------|------------------|
| fresh/recent | No action needed | N/A |
| aging | Light review, verify accuracy | 15-30 min |
| stale | Thorough review, update examples | 1-2 hours |
| outdated | Rewrite, archive, or delete | 4+ hours |

---

## Integration with Health Score

### Staleness Contribution

Staleness violations contribute to health score as **medium** severity:

**Calculation**:
```
stale_violations = count(files with staleness_score > 0.5 OR age > 180 days)
penalty_points = stale_violations × 2
```

**Example**:
- 5 files with staleness issues
- Penalty: 5 × 2 = 10 points
- Health score impact: -10

---

## Quick Reference

**Age Thresholds**:
- Fresh: <30 days
- Recent: 31-90 days
- Aging: 91-180 days
- Stale: 181-365 days
- Outdated: >365 days

**Staleness Score Formula**:
```
(stale_links + 2 × outdated_links) / total_links
```

**Alert Trigger**:
- Age >180 days, OR
- Staleness score >0.5, OR
- Age >90 days AND score >0.3

**Severity**:
- Low: Age 91-180, score <0.3
- Medium: Age 181-365 OR score 0.5-0.8
- High: Age >365 OR score >0.8
- Critical: Age >730 AND score >0.8
