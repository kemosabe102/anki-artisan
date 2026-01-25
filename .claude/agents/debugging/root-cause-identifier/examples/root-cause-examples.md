# Root Cause Analysis Examples

Example outputs demonstrating 5 Whys and SCAMPER application.

---

## Example 1: API Performance Degradation

### Input
```json
{
  "task_id": "RCA-001",
  "problem_statement": {
    "symptom": "API response times increased from 200ms to 3s over the past week",
    "context": "No code deployments in the past 2 weeks, traffic levels stable"
  },
  "evidence_available": {
    "logs": ["Slow query warnings appearing in database logs"],
    "code_references": ["packages/api/src/handlers/orders.py"]
  }
}
```

### Output (SUCCESS)
```json
{
  "status": "SUCCESS",
  "agent": "root-cause-identifier",
  "task_id": "RCA-001",
  "operation_type": "analyze_root_cause",
  "summary": "Root cause: Database index fragmentation from continuous writes without maintenance. Top recommendation: Implement automated index maintenance schedule.",
  "confidence": 0.85,
  "agent_specific_output": {
    "five_whys_chain": [
      {
        "level": 1,
        "question": "Why did API response times increase from 200ms to 3s?",
        "answer": "Database queries are taking 10x longer than baseline",
        "evidence": [
          {"type": "metric", "description": "Query p95 latency increased from 50ms to 500ms", "source": "database metrics dashboard"}
        ],
        "confidence": 0.95
      },
      {
        "level": 2,
        "question": "Why are database queries taking 10x longer?",
        "answer": "Index scans are being replaced by sequential scans",
        "evidence": [
          {"type": "log", "description": "EXPLAIN plans show Seq Scan instead of Index Scan", "source": "slow query log analysis"}
        ],
        "confidence": 0.90
      },
      {
        "level": 3,
        "question": "Why are indexes not being used effectively?",
        "answer": "Index fragmentation has reached 85%, causing planner to prefer sequential scans",
        "evidence": [
          {"type": "metric", "description": "pg_stat_user_indexes shows fragmentation at 85%", "source": "database stats query"}
        ],
        "confidence": 0.88
      },
      {
        "level": 4,
        "question": "Why has index fragmentation reached 85%?",
        "answer": "High volume of updates/deletes without index maintenance",
        "evidence": [
          {"type": "metric", "description": "50K updates/day on orders table, no REINDEX in 6 months", "source": "pg_stat_activity history"},
          {"type": "documentation", "description": "No scheduled maintenance in runbooks", "source": "ops runbook review"}
        ],
        "confidence": 0.85
      },
      {
        "level": 5,
        "question": "Why is there no index maintenance scheduled?",
        "answer": "Index maintenance was never configured in production setup",
        "evidence": [
          {"type": "documentation", "description": "Production setup checklist missing index maintenance step", "source": "infrastructure docs"}
        ],
        "confidence": 0.80
      }
    ],
    "root_cause": {
      "description": "Database index maintenance was never configured in production, leading to progressive fragmentation from high write volume",
      "actionable": true,
      "circular_check_passed": true,
      "category": "process",
      "recurrence_risk": "high"
    },
    "scamper_recommendations": [
      {
        "id": "R1",
        "scamper_lens": "Substitute",
        "description": "Replace manual index maintenance with automated pg_cron job for weekly REINDEX",
        "prevents_recurrence_by": "Automatically maintains indexes regardless of operator awareness",
        "effort_estimate": "low",
        "impact_estimate": "high",
        "priority": 1
      },
      {
        "id": "R2",
        "scamper_lens": "Adapt",
        "description": "Adapt monitoring from staging that includes index health alerts",
        "prevents_recurrence_by": "Provides early warning before fragmentation impacts performance",
        "effort_estimate": "low",
        "impact_estimate": "medium",
        "priority": 2
      },
      {
        "id": "R3",
        "scamper_lens": "Modify",
        "description": "Modify production setup checklist to include index maintenance configuration",
        "prevents_recurrence_by": "Ensures future deployments include maintenance from day one",
        "effort_estimate": "low",
        "impact_estimate": "medium",
        "priority": 3
      }
    ],
    "analysis_metadata": {
      "evidence_quality": "strong",
      "alternative_root_causes_considered": [
        {"description": "Increased data volume", "ruled_out_because": "Traffic levels confirmed stable, table size growth minimal"},
        {"description": "Hardware degradation", "ruled_out_because": "No hardware alerts, other databases on same host performing normally"}
      ],
      "assumptions_made": ["Database statistics are accurate", "No concurrent schema changes"]
    }
  }
}
```

---

## Example 2: Recurring Test Failures (Insufficient Evidence)

### Input
```json
{
  "task_id": "RCA-002",
  "problem_statement": {
    "symptom": "Unit tests fail randomly in CI but pass locally"
  }
}
```


### Output (FAILURE - Insufficient Evidence)
```json
{
  "status": "FAILURE",
  "agent": "root-cause-identifier",
  "task_id": "RCA-002",
  "operation_type": "analyze_root_cause",
  "summary": "Unable to complete root cause analysis due to insufficient evidence. Need CI logs and test output.",
  "confidence": 0.3,
  "failure_details": {
    "failure_type": "insufficient_evidence",
    "reasons": [
      "No CI logs provided to analyze failure patterns",
      "No specific test names or error messages available",
      "Cannot determine if failures are consistent or truly random"
    ],
    "partial_analysis": {
      "whys_completed": 1,
      "last_answer": "Tests fail in CI environment but not locally",
      "blocking_point": "Cannot determine why CI environment differs without logs"
    },
    "evidence_gaps": [
      {"gap": "CI build logs from failing runs", "investigation_path": "Export logs from last 5 failing CI runs"},
      {"gap": "Specific test names that fail", "investigation_path": "Run pytest with -v flag in CI"},
      {"gap": "Environment differences", "investigation_path": "Compare CI vs local Python version, dependencies"}
    ],
    "recovery_suggestions": [
      "Gather CI logs from recent failing builds",
      "Identify which specific tests fail (names, not just count)",
      "Document environment differences between local and CI",
      "Check if failures correlate with specific times or conditions"
    ]
  }
}
```

---

## Example 3: Deployment Failure Pattern

### Input
```json
{
  "task_id": "RCA-003",
  "problem_statement": {
    "symptom": "Kubernetes deployments fail 30% of the time with OOMKilled",
    "context": "Started after adding new feature for PDF generation",
    "timeline": [
      {"timestamp": "2024-01-15", "event": "PDF feature merged"},
      {"timestamp": "2024-01-16", "event": "First OOMKilled observed"},
      {"timestamp": "2024-01-20", "event": "Failures reaching 30% of deployments"}
    ]
  },
  "evidence_available": {
    "logs": ["kubectl describe pod shows OOMKilled exit code 137"],
    "code_references": ["packages/reports/src/pdf_generator.py"],
    "previous_occurrences": [{"date": "2023-06", "resolution": "Increased memory limits"}]
  }
}
```

### Output (SUCCESS)
```json
{
  "status": "SUCCESS",
  "agent": "root-cause-identifier",
  "task_id": "RCA-003",
  "operation_type": "analyze_root_cause",
  "summary": "Root cause: PDF generation loads entire document into memory without streaming. Top recommendation: Implement streaming PDF generation.",
  "confidence": 0.88,
  "agent_specific_output": {
    "five_whys_chain": [
      {
        "level": 1,
        "question": "Why are pods being OOMKilled during deployment?",
        "answer": "Memory usage spikes above 512Mi limit during PDF generation",
        "evidence": [
          {"type": "metric", "description": "Memory peaks at 650Mi during PDF jobs", "source": "Prometheus metrics"},
          {"type": "log", "description": "Exit code 137 (OOMKilled)", "source": "kubectl describe pod"}
        ],
        "confidence": 0.95
      },
      {
        "level": 2,
        "question": "Why does memory spike during PDF generation?",
        "answer": "PDF generator loads entire document into memory before rendering",
        "evidence": [
          {"type": "code", "description": "pdf_generator.py line 45: doc.load_all_pages()", "source": "code review"}
        ],
        "confidence": 0.90
      },
      {
        "level": 3,
        "question": "Why does the generator load all pages into memory?",
        "answer": "Implementation uses non-streaming library approach",
        "evidence": [
          {"type": "code", "description": "Using ReportLab Canvas without streaming", "source": "pdf_generator.py imports"}
        ],
        "confidence": 0.85
      },
      {
        "level": 4,
        "question": "Why was non-streaming approach chosen?",
        "answer": "Original implementation for small reports, not designed for large PDFs",
        "evidence": [
          {"type": "documentation", "description": "Original spec: 'Reports under 10 pages'", "source": "feature spec"},
          {"type": "pattern", "description": "New feature generates 50+ page reports", "source": "product requirements"}
        ],
        "confidence": 0.82
      },
      {
        "level": 5,
        "question": "Why wasn't memory impact assessed for large PDFs?",
        "answer": "No performance testing for memory-intensive operations in CI",
        "evidence": [
          {"type": "documentation", "description": "CI only runs unit tests, no memory profiling", "source": "CI config review"}
        ],
        "confidence": 0.78
      }
    ],
    "root_cause": {
      "description": "PDF generation implementation uses non-streaming approach unsuitable for large documents, and no memory profiling in CI caught the issue",
      "actionable": true,
      "circular_check_passed": true,
      "category": "design",
      "recurrence_risk": "high"
    },
    "scamper_recommendations": [
      {
        "id": "R1",
        "scamper_lens": "Substitute",
        "description": "Replace non-streaming PDF generation with streaming approach using ReportLab's streaming Canvas",
        "prevents_recurrence_by": "Limits memory to single page at a time regardless of document size",
        "effort_estimate": "medium",
        "impact_estimate": "high",
        "priority": 1
      },
      {
        "id": "R2",
        "scamper_lens": "Modify",
        "description": "Increase memory limits to 1Gi as temporary mitigation while implementing R1",
        "prevents_recurrence_by": "Provides headroom for current implementation",
        "effort_estimate": "low",
        "impact_estimate": "medium",
        "priority": 2
      },
      {
        "id": "R3",
        "scamper_lens": "Adapt",
        "description": "Add memory profiling tests similar to existing performance test suite",
        "prevents_recurrence_by": "Catches memory regressions before production deployment",
        "effort_estimate": "medium",
        "impact_estimate": "high",
        "priority": 3
      },
      {
        "id": "R4",
        "scamper_lens": "Eliminate",
        "description": "Remove synchronous PDF generation, use async job queue for large reports",
        "prevents_recurrence_by": "Moves memory-intensive work out of request path",
        "effort_estimate": "high",
        "impact_estimate": "high",
        "priority": 4
      }
    ],
    "analysis_metadata": {
      "evidence_quality": "strong",
      "alternative_root_causes_considered": [
        {"description": "Memory leak in application", "ruled_out_because": "Memory returns to baseline after PDF job completes"},
        {"description": "Container resource contention", "ruled_out_because": "Failures only occur during PDF generation, not other operations"}
      ],
      "assumptions_made": ["Prometheus metrics are accurate", "OOMKilled correlates with PDF jobs"]
    }
  }
}
```
