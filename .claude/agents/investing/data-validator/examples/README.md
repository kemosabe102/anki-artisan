# Data Validator - Examples

## Overview

This directory contains example outputs from the data-validator agent to illustrate usage patterns and expected results.

## Example Index

| Example | Description | Score |
|---------|-------------|-------|
| [full-audit-example.md](full-audit-example.md) | Complete quality audit with all dimensions passing | 85 (B) |
| [gap-detection-example.md](gap-detection-example.md) | Audit with gaps detected and recommendations | 62 (D) |

## Quick Start

**Input** (minimal):
```json
{}
```
Uses today's date.

**Input** (with date):
```json
{
  "date": "2026-01-04"
}
```

## Expected Output Structure

```json
{
  "status": "SUCCESS",
  "audit_date": "2026-01-04",
  "data_quality_score": 85,
  "grade": "B",
  "category_coverage": { ... },
  "events_audited": 12,
  "breakdown": {
    "category_score": 16,
    "confidence_score": 18,
    "source_score": 15,
    "severity_score": 20,
    "escalation_score": 16
  },
  "recommendations": [ ... ]
}
```
