# Example: Alpha Phase 01 Integration Review

**Feature**: Theme, Attention & Sentiment Engine (Alpha Phase 01)
**Components**: Data providers, document processing, attention scoring, ticker projection

---

## Command Execution

```bash
/integration-review docs/00-project/alpha/phase-01
```

---

## Phase 2: Detect Output

```json
{
  "feature": "alpha-phase-01",
  "total_pairs": 8,
  "pairs": [
    {
      "id": 1,
      "upstream": "PerplexityProvider",
      "downstream": "Normalizer",
      "upstream_file": "packages/news_sentiment/providers/perplexity_provider.py",
      "downstream_file": "packages/attention/processing/normalizer.py",
      "data_flow_type": "direct",
      "confidence": 0.95,
      "evidence": ["ARCHITECTURE.md line 23", "import in normalizer.py:5"]
    },
    {
      "id": 2,
      "upstream": "Normalizer",
      "downstream": "Deduplicator",
      "upstream_file": "packages/attention/processing/normalizer.py",
      "downstream_file": "packages/attention/processing/deduplicator.py",
      "data_flow_type": "direct",
      "confidence": 0.92,
      "evidence": ["Same package", "Sequential task dependency"]
    },
    {
      "id": 3,
      "upstream": "Deduplicator",
      "downstream": "ThemeMatcher",
      "upstream_file": "packages/attention/processing/deduplicator.py",
      "downstream_file": "packages/attention/processing/theme_matcher.py",
      "data_flow_type": "direct",
      "confidence": 0.90,
      "evidence": ["Pipeline pattern in engine.py"]
    },
    {
      "id": 4,
      "upstream": "ThemeMatcher",
      "downstream": "EntityLinker",
      "upstream_file": "packages/attention/processing/theme_matcher.py",
      "downstream_file": "packages/attention/entity/linker.py",
      "data_flow_type": "direct",
      "confidence": 0.88,
      "evidence": ["EnrichedDocument type flows through"]
    },
    {
      "id": 5,
      "upstream": "EntityLinker",
      "downstream": "MentionAggregator",
      "upstream_file": "packages/attention/entity/linker.py",
      "downstream_file": "packages/attention/processing/mention_aggregator.py",
      "data_flow_type": "direct",
      "confidence": 0.92,
      "evidence": ["Explicit data flow in architecture"]
    },
    {
      "id": 6,
      "upstream": "MentionAggregator",
      "downstream": "TickerProjector",
      "upstream_file": "packages/attention/processing/mention_aggregator.py",
      "downstream_file": "packages/attention/scoring/ticker_projection.py",
      "data_flow_type": "direct",
      "confidence": 0.94,
      "evidence": ["MentionCounts → TickerProjection"]
    },
    {
      "id": 7,
      "upstream": "TickerProjector",
      "downstream": "QualityGate",
      "upstream_file": "packages/attention/scoring/ticker_projection.py",
      "downstream_file": "packages/attention/scoring/quality_gate.py",
      "data_flow_type": "direct",
      "confidence": 0.96,
      "evidence": ["5-filter validation documented"]
    },
    {
      "id": 8,
      "upstream": "QualityGate",
      "downstream": "TimescaleStorage",
      "upstream_file": "packages/attention/scoring/quality_gate.py",
      "downstream_file": "packages/attention/storage/timescale.py",
      "data_flow_type": "storage",
      "confidence": 0.90,
      "evidence": ["Persistence layer in architecture"]
    }
  ]
}
```

---

## Phase 3: Review Loop Progress

```
Feature Final Review: docs/00-project/alpha/phase-01
══════════════════════════════════════════════════════

Detecting integration pairs...
Found 8 integration pairs.

[1/8] Reviewing: PerplexityProvider → Normalizer... ✓ PASS
      Contract: RawDocument → RawDocument ✓
      Error handling: RateLimitError documented ✓
      Tests: test_integration_providers.py ✓

[2/8] Reviewing: Normalizer → Deduplicator... ✓ PASS
      Contract: RawDocument → RawDocument | None ✓
      Null handling: None = filtered out ✓
      Tests: test_processing_pipeline.py ✓

[3/8] Reviewing: Deduplicator → ThemeMatcher... ⚠ PASS_WITH_CONDITIONS (1 MEDIUM)
      Contract: RawDocument → EnrichedDocument ✓
      Finding: Missing error context in transformation
      Tests: test_processing_pipeline.py (PARTIAL)

[4/8] Reviewing: ThemeMatcher → EntityLinker... ✓ PASS
      Contract: EnrichedDocument → EnrichedDocument ✓
      Type safety: Theme list validated ✓
      Tests: test_entity_linking.py ✓

[5/8] Reviewing: EntityLinker → MentionAggregator... ✓ PASS
      Contract: EnrichedDocument → MentionCounts ✓
      Aggregation: entity_mentions grouped correctly ✓
      Tests: test_mention_aggregation.py ✓

[6/8] Reviewing: MentionAggregator → TickerProjector... ⚠ PASS_WITH_CONDITIONS (1 HIGH)
      Contract: MentionCounts → TickerProjection ✓
      Finding: InsufficientDataError not caught
      Tests: test_ticker_projection.py (PARTIAL - missing error scenarios)

[7/8] Reviewing: TickerProjector → QualityGate... ✓ PASS
      Contract: TickerProjection → TickerProjection (validated) ✓
      5-filter validation: All filters present ✓
      Tests: test_quality_gate.py ✓

[8/8] Reviewing: QualityGate → TimescaleStorage... ✓ PASS
      Contract: TickerProjection → write_ticker_attention() ✓
      Transaction handling: Batch commits ✓
      Tests: test_storage_integration.py ✓

Running integration tests...
pytest tests/integration/ -v --tb=short
Tests: 47 passed, 0 failed, 3 skipped

═══════════════════════════════════════════════════════
Gate: PASS_WITH_CONDITIONS
Findings: 0 Critical, 1 High, 1 Medium, 0 Low
═══════════════════════════════════════════════════════
```

---

## Sample Findings

### HIGH Finding (Pair 6)

```json
{
  "id": "INT-001",
  "category": "error_propagation",
  "severity": "HIGH",
  "confidence": 0.87,
  "pair_id": 6,
  "upstream": "MentionAggregator",
  "downstream": "TickerProjector",
  "issue": "InsufficientDataError from MentionAggregator not caught in TickerProjector",
  "evidence": "mention_aggregator.py:78 raises InsufficientDataError when len(mentions) < MIN_MENTIONS. ticker_projection.py:34 calls aggregator.aggregate() without try/except.",
  "recommendation": "Add try/except in TickerProjector.project() to handle InsufficientDataError, either by returning empty projection or logging and continuing with degraded data."
}
```

### MEDIUM Finding (Pair 3)

```json
{
  "id": "INT-002",
  "category": "error_propagation",
  "severity": "MEDIUM",
  "confidence": 0.82,
  "pair_id": 3,
  "upstream": "Deduplicator",
  "downstream": "ThemeMatcher",
  "issue": "Error context lost when Deduplicator filters document",
  "evidence": "deduplicator.py:45 returns None for duplicates without logging. theme_matcher.py:23 silently skips None values. No audit trail of filtered documents.",
  "recommendation": "Log filtered document IDs at DEBUG level in Deduplicator for troubleshooting. Consider emitting a DuplicateFiltered event for observability."
}
```

---

## Generated Report (INTEGRATION-REVIEW-REPORT.md)

```markdown
# Integration Review Report

**Feature**: alpha-phase-01
**Review Date**: 2025-12-17T10:30:00Z
**Status**: PASS_WITH_CONDITIONS

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Integration Pairs Reviewed | 8 |
| Total Findings | 2 |
| Critical | 0 |
| High | 1 |
| Medium | 1 |
| Low | 0 |
| Gate Result | **PASS_WITH_CONDITIONS** |
| Blocking Issues | 0 |

---

## Integration Pairs Reviewed

| # | Upstream | Downstream | Data Flow | Status |
|---|----------|------------|-----------|--------|
| 1 | PerplexityProvider | Normalizer | direct | PASS |
| 2 | Normalizer | Deduplicator | direct | PASS |
| 3 | Deduplicator | ThemeMatcher | direct | PASS_WITH_CONDITIONS |
| 4 | ThemeMatcher | EntityLinker | direct | PASS |
| 5 | EntityLinker | MentionAggregator | direct | PASS |
| 6 | MentionAggregator | TickerProjector | direct | PASS_WITH_CONDITIONS |
| 7 | TickerProjector | QualityGate | direct | PASS |
| 8 | QualityGate | TimescaleStorage | storage | PASS |

---

## Findings by Severity

### CRITICAL (Blocking)

> None found ✓

### HIGH (Should Fix)

**[INT-001] error_propagation: MentionAggregator → TickerProjector**
- **Issue**: InsufficientDataError not caught
- **Evidence**: `mention_aggregator.py:78, ticker_projection.py:34`
- **Recommendation**: Add try/except for InsufficientDataError
- **Confidence**: 0.87

### MEDIUM (Advisory)

**[INT-002] error_propagation: Deduplicator → ThemeMatcher**
- **Issue**: Error context lost when filtering duplicates
- **Evidence**: `deduplicator.py:45, theme_matcher.py:23`
- **Recommendation**: Log filtered document IDs at DEBUG level

---

## Gate Decision

**Result**: PASS_WITH_CONDITIONS

**Criteria Applied**:
- [x] Zero CRITICAL findings
- [x] HIGH findings ≤3 (found: 1)
- [x] Integration tests pass

**Action Required**:
1. Review HIGH finding INT-001 (error propagation)
2. Document justification in PR or fix before merge

---

*Generated by integration-boundary-reviewer skill*
*Review Duration: 4m 23s*
```

---

## Generated JSON (INTEGRATION-REVIEW.json)

```json
{
  "feature": "alpha-phase-01",
  "date": "2025-12-17T10:30:00Z",
  "gate_status": "PASS_WITH_CONDITIONS",
  "total_pairs": 8,
  "findings": {
    "total": 2,
    "critical": 0,
    "high": 1,
    "medium": 1,
    "low": 0
  },
  "pairs": [
    {"id": 1, "upstream": "PerplexityProvider", "downstream": "Normalizer", "status": "PASS"},
    {"id": 2, "upstream": "Normalizer", "downstream": "Deduplicator", "status": "PASS"},
    {"id": 3, "upstream": "Deduplicator", "downstream": "ThemeMatcher", "status": "PASS_WITH_CONDITIONS"},
    {"id": 4, "upstream": "ThemeMatcher", "downstream": "EntityLinker", "status": "PASS"},
    {"id": 5, "upstream": "EntityLinker", "downstream": "MentionAggregator", "status": "PASS"},
    {"id": 6, "upstream": "MentionAggregator", "downstream": "TickerProjector", "status": "PASS_WITH_CONDITIONS"},
    {"id": 7, "upstream": "TickerProjector", "downstream": "QualityGate", "status": "PASS"},
    {"id": 8, "upstream": "QualityGate", "downstream": "TimescaleStorage", "status": "PASS"}
  ],
  "blocking_issues": [],
  "test_coverage": {
    "covered_pairs": 8,
    "total_pairs": 8,
    "percentage": 100,
    "tests_passed": true
  },
  "execution_time_seconds": 263,
  "checkpoint_used": false
}
```

---

## Resume Example

If review is interrupted at pair 4:

```bash
# Checkpoint saved at pair 4
/integration-review docs/00-project/alpha/phase-01 --resume

# Output:
Resuming from checkpoint...
Reviewed: 3/8 pairs
Continuing from pair 4: ThemeMatcher → EntityLinker

[4/8] Reviewing: ThemeMatcher → EntityLinker... ✓ PASS
[5/8] Reviewing: EntityLinker → MentionAggregator... ✓ PASS
...
```
