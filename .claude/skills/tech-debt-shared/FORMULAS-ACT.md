# ACT Phase Formulas

Output formatting and report generation. Used during final report assembly.

**Skills Using This File**: `generating-debt-reports`

**Output Schema**: `.claude/agents/specialists/tech-debt-investigator/schemas/tech-debt-investigator.schema.json`

---

## 1. Trend Calculation

**Formula**:
```
trend_direction = ((current_tdr - baseline_tdr) / baseline_tdr) × 100
```

**Classification**:
| Trend % | Direction | Interpretation |
|---------|-----------|----------------|
| < -5% | IMPROVING | Debt decreasing faster than expected |
| -5% to +5% | STABLE | Debt within maintenance range |
| > +5% | DEGRADING | Debt accumulating, intervention needed |

**Example**:
```
Baseline TDR: 12%
Current TDR: 10%

trend = ((10 - 12) / 12) × 100 = -16.7%
Direction: IMPROVING
```

---

## 2. Executive Summary Template

```markdown
## Tech Debt Report: [Component/System Name]

**Assessment Date**: [YYYY-MM-DD]
**TDR**: [X.X]% (Grade: [A-E])
**SIG Rating**: [★★★★★]
**Trend**: [IMPROVING/STABLE/DEGRADING] ([±X.X]%)

### Top Hotspots
1. [file1.py] - Score: [0.XX] - [CRITICAL/HIGH/MEDIUM]
2. [file2.py] - Score: [0.XX] - [CRITICAL/HIGH/MEDIUM]
3. [file3.py] - Score: [0.XX] - [CRITICAL/HIGH/MEDIUM]

### ROI Recommendation
[APPROVE/DEFER/REJECT] - Break-even: [X] months
Estimated savings: $[X,XXX]/year
```

---

## Cross-References

- **FORMULAS-ORIENT.md**: TDR and grade calculations, SIG star ratings
- **FORMULAS-DECIDE.md**: ROI analysis, priority quadrants, sprint grouping
