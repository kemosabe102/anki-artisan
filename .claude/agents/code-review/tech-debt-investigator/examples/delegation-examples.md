# Delegation Examples

How the orchestrator invokes tech-debt-investigator for common scenarios.

---

## Scenario 1: Code Health Assessment

**User Request**: "Assess code health in packages/"

**Orchestrator Delegation**:
```markdown
Task(tech-debt-investigator,
  "Analyze technical debt in packages/. Calculate debt_score, TDR,
   identify hotspots, generate Impact/Effort matrix with remediation roadmap.")
```

**Context Metadata**:
```json
{
  "scope": {
    "directories": ["packages/"],
    "file_patterns": ["*.py"],
    "exclusions": ["**/test_*.py", "**/__pycache__/**"]
  }
}
```

---

## Scenario 2: Agent Documentation Debt

**User Request**: "Review agent quality for .claude/agents/"

**Orchestrator Delegation**:
```markdown
Task(tech-debt-investigator,
  "Analyze documentation debt in .claude/agents/**. Assess consistency,
   maintainability, schema compliance. Part of Agent Analysis Suite.")
```

**Context Metadata**:
```json
{
  "scope": {
    "directories": [".claude/agents/"],
    "file_patterns": ["*.md"],
    "analysis_type": "agent_debt"
  }
}
```

---

## Scenario 3: Pre-Release Quality Gate

**User Request**: "Run quality gate before release"

**Orchestrator Delegation**:
```markdown
Task(tech-debt-investigator,
  "Comprehensive 6-category debt analysis for packages/ and tests/.
   Apply SQALE grading. Flag any regressions vs baseline.
   Output pass/fail recommendation with evidence.")
```

**Context Metadata**:
```json
{
  "scope": {
    "directories": ["packages/", "tests/"],
    "file_patterns": ["*.py"]
  },
  "baseline": {
    "previous_debt_score": 42,
    "previous_tdr": 0.08,
    "run_timestamp": "2024-01-15T10:00:00Z"
  },
  "thresholds": {
    "max_debt_score": 50,
    "max_tdr": 0.10,
    "min_coverage": 80
  }
}
```

---

## Scenario 4: Hotspot Analysis (Post-Mortem)

**User Request**: "Find hotspots after production incident"

**Orchestrator Delegation**:
```markdown
Task(tech-debt-investigator,
  "Hotspot analysis for packages/api/. Correlate churn x complexity x defects.
   Focus on 3-month window. Identify ownership dispersion risks.")
```

**Context Metadata**:
```json
{
  "scope": {
    "directories": ["packages/api/"],
    "analysis_type": "historical"
  },
  "business": {
    "critical_modules": ["packages/api/auth.py", "packages/api/payments.py"],
    "incident_files": ["packages/api/handlers.py"]
  }
}
```

---

## Scenario 5: Iterative Run with Trend Analysis

**User Request**: "Compare debt to last sprint"

**Orchestrator Delegation**:
```markdown
Task(tech-debt-investigator,
  "Iterative debt analysis for packages/. Compare vs baseline.
   Calculate deltas, detect regressions, assess debt trajectory.")
```

**Context Metadata**:
```json
{
  "scope": {
    "directories": ["packages/"]
  },
  "baseline": {
    "previous_debt_score": 38,
    "previous_tdr": 0.07,
    "previous_coverage": 82,
    "run_timestamp": "2024-01-01T10:00:00Z"
  }
}
```

**Expected Output Includes**:
```json
{
  "trend_analysis": {
    "debt_score_delta": "+4",
    "tdr_delta": "+0.01",
    "coverage_delta": "-2%",
    "direction": "worsening",
    "regressions": ["coverage drop >5% threshold approaching"],
    "new_hotspots": ["packages/api/new_handler.py"]
  }
}
```

---

## Output Interpretation

### debt_score (0-100)
- 0-20: Excellent health
- 21-40: Good, manageable
- 41-60: Fair, attention needed
- 61-80: Poor, significant debt
- 81-100: Critical, immediate action

### SQALE Grade
- A (<5% TDR): Production-ready
- B (5-10%): Acceptable
- C (10-20%): Technical debt sprint recommended
- D (20-50%): Major refactoring needed
- E (>50%): Architecture review required

### Priority Quadrants
- **P1**: Fix this sprint (high impact, low effort)
- **P2**: Plan for next quarter (high impact, high effort)
- **P3**: Backlog (low impact, high effort)
- **P4**: Boy Scout Rule (low impact, low effort)
---

## Edge Case Scenarios

How tech-debt-investigator handles failure conditions, incomplete data, and ambiguous situations.

---

### Edge Case 1: Empty Scope

**Scenario**: No files match the provided patterns (non-existent directory, overly restrictive glob).

**Example Input Context**:
```json
{
  "scope": {
    "directories": ["packages/nonexistent/"],
    "file_patterns": ["*.rs"]
  }
}
```

**Expected Agent Behavior**:
1. Detect zero matching files during scope resolution
2. Return structured failure (NOT empty results)
3. Provide actionable guidance for scope correction
4. Set `status: "failure"` with `failure_type: "empty_scope"`

**Example Output**:
```json
{
  "status": "failure",
  "failure_type": "empty_scope",
  "failure_details": {
    "message": "No files matched the provided scope",
    "scope_attempted": {
      "directories": ["packages/nonexistent/"],
      "file_patterns": ["*.rs"]
    },
    "diagnostics": {
      "directory_exists": false,
      "pattern_matches": 0
    },
    "guidance": [
      "Verify directory path exists: packages/nonexistent/",
      "Available directories in packages/: ['core/', 'api/', 'utils/']",
      "For Rust files, check if project uses .rs extension"
    ]
  },
  "confidence": 1.0
}
```

---

### Edge Case 2: Missing Git History

**Scenario**: Fresh repository with no commits, or shallow clone without history.

**Example Input Context**:
```json
{
  "scope": {
    "directories": ["src/"],
    "analysis_type": "historical"
  }
}
```

**Expected Agent Behavior**:
1. Attempt git log/blame operations
2. Detect missing or insufficient history
3. Skip historical metrics (churn, ownership, defect correlation)
4. Continue with static analysis only
5. Lower confidence score to reflect incomplete data
6. Document which metrics are unavailable

**Example Output**:
```json
{
  "status": "partial",
  "agent": "tech-debt-investigator",
  "confidence": 0.65,
  "agent_specific_output": {
    "debt_score": 34,
    "tdr": 0.06,
    "sqale_grade": "B",
    "metrics_available": {
      "static_analysis": true,
      "complexity": true,
      "coverage": true,
      "churn": false,
      "ownership": false,
      "defect_correlation": false
    },
    "limitations": [
      "Git history unavailable - churn analysis skipped",
      "Ownership dispersion cannot be calculated",
      "Defect density based on code smells only (no commit correlation)"
    ],
    "hotspots": {
      "note": "Ranked by complexity only (churn data unavailable)",
      "files": [
        {"path": "src/parser.py", "complexity": 42, "confidence": 0.6}
      ]
    }
  }
}
```

---

### Edge Case 3: Invalid Baseline Comparison

**Scenario**: Baseline was collected from different directories than current analysis scope.

**Example Input Context**:
```json
{
  "scope": {
    "directories": ["packages/api/"]
  },
  "baseline": {
    "previous_debt_score": 45,
    "previous_tdr": 0.09,
    "run_timestamp": "2024-01-10T10:00:00Z",
    "scope": {
      "directories": ["packages/core/"]
    }
  }
}
```

**Expected Agent Behavior**:
1. Detect scope mismatch between baseline and current analysis
2. Flag comparison as invalid
3. Return current-only analysis with explicit warning
4. Provide both datasets separately (no delta calculations)
5. Recommend corrective action

**Example Output**:
```json
{
  "status": "success",
  "confidence": 0.85,
  "warnings": [
    {
      "code": "BASELINE_SCOPE_MISMATCH",
      "severity": "high",
      "message": "Baseline scope (packages/core/) does not match current scope (packages/api/). Trend comparison invalid.",
      "recommendation": "Re-run baseline analysis on packages/api/ for valid comparison"
    }
  ],
  "agent_specific_output": {
    "debt_score": 38,
    "tdr": 0.07,
    "sqale_grade": "B",
    "trend_analysis": {
      "status": "invalid",
      "reason": "scope_mismatch",
      "current_scope": "packages/api/",
      "baseline_scope": "packages/core/",
      "deltas": null
    },
    "baseline_reference": {
      "note": "Provided for reference only - not comparable",
      "debt_score": 45,
      "tdr": 0.09
    }
  }
}
```

---

### Edge Case 4: Large Codebase Timeout

**Scenario**: Analysis scope exceeds practical limits (>100K LOC, thousands of files).

**Example Input Context**:
```json
{
  "scope": {
    "directories": ["/"],
    "file_patterns": ["*.py", "*.js", "*.ts"]
  }
}
```

**Expected Agent Behavior**:
1. Estimate scope size before full analysis
2. If >100K LOC or >5000 files: chunk analysis
3. Process chunks sequentially, tracking progress
4. Report partial results with coverage gaps noted
5. Provide chunking metadata for resumption
6. Recommend scope reduction strategies

**Example Output**:
```json
{
  "status": "partial",
  "confidence": 0.70,
  "agent_specific_output": {
    "scope_analysis": {
      "total_files": 8234,
      "total_loc": 342000,
      "analyzed_files": 3500,
      "analyzed_loc": 145000,
      "coverage_percentage": 42.5
    },
    "chunking_metadata": {
      "chunks_completed": 2,
      "chunks_total": 5,
      "last_chunk_end": "packages/m*/",
      "resume_from": "packages/n*/"
    },
    "partial_results": {
      "debt_score": 52,
      "debt_score_confidence": 0.65,
      "note": "Score based on 42.5% of codebase",
      "tdr": 0.11,
      "sqale_grade": "C",
      "hotspots": [
        {"path": "packages/core/engine.py", "score": 89},
        {"path": "packages/api/handlers.py", "score": 76}
      ]
    },
    "coverage_gaps": [
      "packages/legacy/ - not analyzed",
      "packages/vendor/ - not analyzed",
      "tests/ - not analyzed"
    ],
    "recommendations": [
      "Re-run with narrower scope: packages/core/ and packages/api/",
      "Use exclusions: ['**/vendor/**', '**/legacy/**']",
      "For full analysis, increase timeout or run in background"
    ]
  }
}
```

---

### Edge Case 5: Conflicting Evidence

**Scenario**: Metrics disagree - e.g., high complexity but low defect density, or high churn but excellent test coverage.

**Example Input Context**:
```json
{
  "scope": {
    "directories": ["packages/crypto/"]
  },
  "business": {
    "critical_modules": ["packages/crypto/encryption.py"]
  }
}
```

**Analysis Finds**:
- Cyclomatic complexity: 85 (very high)
- Defect density: 0.02 (very low)
- Test coverage: 98%
- Code churn: High (50+ commits/month)

**Expected Agent Behavior**:
1. Detect conflicting signals between metrics
2. Document both perspectives without forcing resolution
3. Lower confidence score to reflect uncertainty
4. Note the conflict explicitly in output
5. Provide context-specific interpretation

**Example Output**:
```json
{
  "status": "success",
  "confidence": 0.72,
  "agent_specific_output": {
    "debt_score": 45,
    "debt_score_rationale": "Elevated due to complexity, moderated by low defect density",
    "conflicts_detected": [
      {
        "conflict_id": "COMPLEXITY_VS_DEFECTS",
        "metrics": {
          "cyclomatic_complexity": 85,
          "defect_density": 0.02
        },
        "interpretation": {
          "pessimistic": "High complexity is latent risk - defects may emerge under edge cases",
          "optimistic": "High test coverage (98%) catches issues; complexity is managed",
          "contextual": "Crypto modules often have unavoidable complexity for security correctness"
        },
        "recommendation": "Maintain high test coverage; consider extracting sub-algorithms to reduce per-function complexity"
      },
      {
        "conflict_id": "CHURN_VS_STABILITY",
        "metrics": {
          "monthly_churn": 52,
          "defect_rate": "low"
        },
        "interpretation": {
          "pessimistic": "High churn increases regression risk over time",
          "optimistic": "Active maintenance with strong test safety net",
          "contextual": "Security-critical code often requires frequent updates for CVEs"
        },
        "recommendation": "Monitor churn reasons; distinguish security patches from feature changes"
      }
    ],
    "hotspots": [
      {
        "path": "packages/crypto/encryption.py",
        "complexity": 85,
        "defect_density": 0.02,
        "churn": "high",
        "coverage": 98,
        "priority": "P2",
        "priority_rationale": "Flagged for complexity, but low defects and high coverage reduce urgency"
      }
    ],
    "summary": {
      "overall_assessment": "Mixed signals - code is complex but well-tested. Risk is latent rather than active.",
      "confidence_note": "Confidence reduced from 0.85 to 0.72 due to metric conflicts",
      "action": "Monitor, don't remediate urgently. Add complexity threshold alerts."
    }
  }
}
```

---

## Edge Case Handling Principles

1. **Fail Explicitly**: Return structured `failure` status with diagnostics, never empty results
2. **Degrade Gracefully**: When partial data available, continue with reduced confidence
3. **Document Limitations**: Always note which metrics are unavailable or unreliable
4. **Provide Guidance**: Include actionable recommendations for scope correction or retry
5. **Preserve Integrity**: Never fabricate missing data or force metric agreement
