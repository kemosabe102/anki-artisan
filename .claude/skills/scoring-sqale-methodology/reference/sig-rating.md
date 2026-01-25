# SIG Rating Reference

Software Improvement Group (SIG) Maintainability Model for star ratings.

---

## Important Distinction

> **SIG and SQALE are DIFFERENT systems.**
>
> - **SQALE**: Ratio-based (TDR = remediation/development cost)
> - **SIG**: Percentile-based (ranking against industry benchmarks)
>
> A codebase can have a good SQALE grade but poor SIG rating (or vice versa).

---

## Star Rating System

SIG ratings are based on percentile ranking against industry benchmarks:

| Stars | Percentile | Interpretation |
|-------|------------|----------------|
| 5 | Top 5% | Exceptional maintainability |
| 4 | Top 30% | Above average |
| 3 | Average | Industry median |
| 2 | Below 30% | Below average |
| 1 | Bottom 5% | Critical concerns |

**Note**: Percentiles are based on SIG's proprietary benchmark database of analyzed systems.

---


## Low-Risk Thresholds

To achieve 4-5 star ratings, codebases must meet these thresholds:

| Metric | Threshold | Measurement |
|--------|-----------|-------------|
| Volume | <66 KLOC per component | Lines of code |
| Complexity | <15 per method | Cyclomatic complexity |
| Duplication | <5% of code | Clone detection |
| Unit Size | <15 LOC per method | Method length |
| Unit Interfacing | <4 parameters | Parameter count |

**All thresholds must be met** for top-tier ratings.

---

## Maintainability Characteristics

SIG evaluates 8 quality characteristics:

| Characteristic | Description | Weight |
|----------------|-------------|--------|
| Analyzability | Ease of diagnosis | High |
| Changeability | Ease of modification | High |
| Stability | Risk of unintended effects | Medium |
| Testability | Ease of testing | Medium |
| Modularity | Component independence | Medium |
| Reusability | Potential for reuse | Low |
| Security | Vulnerability surface | High |
| Performance | Efficiency characteristics | Medium |


---

## Simplified Star Assignment

Without access to SIG benchmarks, approximate ratings using thresholds:

### 5 Stars (Exceptional)
- All low-risk thresholds met
- No critical/high severity issues
- Test coverage >90%
- Documentation complete

### 4 Stars (Above Average)
- Most low-risk thresholds met (4/5)
- No critical issues, <5 high severity
- Test coverage >80%
- Core documentation present

### 3 Stars (Average)
- Half of low-risk thresholds met
- <3 critical issues
- Test coverage >60%
- README and API docs present

### 2 Stars (Below Average)
- Few thresholds met (1-2/5)
- Multiple critical issues
- Test coverage 40-60%
- Minimal documentation

### 1 Star (Critical)
- No thresholds met
- Numerous critical issues
- Test coverage <40%
- Documentation absent or severely outdated

---

## Mapping SIG to SQALE

| SIG Stars | Approximate SQALE Grade | TDR Equivalent |
|-----------|------------------------|----------------|
| 5 | A | <5% |
| 4 | A-B | 5-8% |
| 3 | B-C | 8-15% |
| 2 | C-D | 15-35% |
| 1 | D-E | >35% |

**Caution**: This mapping is approximate. Systems measure different qualities.
