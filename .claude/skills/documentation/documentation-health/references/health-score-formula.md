# Health Score Formula

## Calculation Methodology

### Base Formula

```
health_score = 100 - penalty_total
```

Where `penalty_total` is the sum of weighted violations:

```
penalty_total = (
  critical_violations × 10 +
  high_violations × 5 +
  medium_violations × 2 +
  low_violations × 1
)
```

### Floor and Ceiling

- **Maximum**: 100 (perfect health)
- **Minimum**: 0 (negative scores not allowed)

### Severity Weights Rationale

| Severity | Weight | Rationale |
|----------|--------|-----------|
| Critical | 10 | Broken links in root docs block onboarding |
| High | 5 | Broken links in active docs disrupt workflows |
| Medium | 2 | Orphans/naming issues reduce discoverability |
| Low | 1 | Minor issues with minimal impact |

## Severity Classification Rules

### Critical Violations

**Definition**: Issues that block primary documentation access

**Examples**:
- Broken link in `README.md`
- Broken link in `docs/index.md`
- Broken link in navigation file (e.g., `SUMMARY.md`)
- Missing required file referenced from root

**Weight**: 10 points per violation

**Impact**: Single critical violation drops score by 10%

### High Violations

**Definition**: Issues in actively maintained documentation

**Criteria**:
- Broken link in file modified <90 days ago
- Missing cross-reference in core guides
- Broken link with >5 incoming references (high traffic)

**Weight**: 5 points per violation

**Impact**: Two high violations drop score by 10%

### Medium Violations

**Definition**: Quality issues that reduce documentation usability

**Examples**:
- Orphaned file (zero incoming references)
- Naming convention violation (non-kebab-case)
- Stale reference (links to file >180 days old)
- Missing metadata (frontmatter)

**Weight**: 2 points per violation

**Impact**: Five medium violations drop score by 10%

### Low Violations

**Definition**: Minor cosmetic or optional quality issues

**Examples**:
- External link not validated (marked `external_unchecked`)
- Minor formatting inconsistency
- Optional section missing
- Recommended (not required) metadata absent

**Weight**: 1 point per violation

**Impact**: Ten low violations drop score by 10%

## Grading Scale

| Score Range | Grade | Quality Level | Interpretation |
|-------------|-------|---------------|----------------|
| 90-100 | A | Excellent | Production-ready, minimal issues |
| 75-89 | B | Good | Solid quality, minor improvements needed |
| 60-74 | C | Fair | Functional but needs attention |
| 40-59 | D | Poor | Significant issues present |
| 0-39 | F | Critical | Urgent remediation required |

## Coverage Adjustment

**Formula**:
```
adjusted_score = health_score × coverage_percentage
```

**Rationale**: Partial scans should not show inflated scores

**Example**:
- Health score: 90
- Coverage: 50% (scanned 25 of 50 files)
- Adjusted score: 45 (displays as "90 [50% coverage]")

**Reporting**: Always display both raw score and coverage percentage

## Score Interpretation Guidelines

### Score 90-100 (Grade A)
**Characteristics**:
- All root documentation links valid
- <2 broken links in active docs
- No critical violations
- Minimal technical debt

**Actions**:
- Maintain current quality
- Monitor for regressions

### Score 75-89 (Grade B)
**Characteristics**:
- Minor broken links in secondary docs
- Some orphaned files
- No critical violations
- Manageable technical debt

**Actions**:
- Fix high-severity issues
- Plan cleanup for medium-severity items

### Score 60-74 (Grade C)
**Characteristics**:
- Multiple broken links in active docs
- Significant orphan files
- Possible 1 critical violation
- Growing technical debt

**Actions**:
- Address critical and high violations immediately
- Schedule comprehensive cleanup

### Score 40-59 (Grade D)
**Characteristics**:
- Many broken links across documentation
- Poor organization (many orphans)
- Multiple critical violations
- High technical debt

**Actions**:
- Emergency remediation required
- Block new documentation work until fixed

### Score 0-39 (Grade F)
**Characteristics**:
- Systemic link failures
- Documentation largely unmaintained
- Critical paths broken
- Extreme technical debt

**Actions**:
- Documentation rebuild likely needed
- Consider archiving and restarting

## Example Calculations

### Example 1: Healthy Documentation

**Violations**:
- Critical: 0
- High: 1 (broken link in recent guide)
- Medium: 3 (2 orphans, 1 naming violation)
- Low: 5 (5 external links unchecked)

**Calculation**:
```
penalty_total = (0×10) + (1×5) + (3×2) + (5×1)
              = 0 + 5 + 6 + 5
              = 16

health_score = 100 - 16 = 84
grade = B (Good)
```

### Example 2: Degraded Documentation

**Violations**:
- Critical: 2 (README.md broken links)
- High: 5 (active doc broken links)
- Medium: 10 (orphans and naming)
- Low: 8 (unchecked externals)

**Calculation**:
```
penalty_total = (2×10) + (5×5) + (10×2) + (8×1)
              = 20 + 25 + 20 + 8
              = 73

health_score = 100 - 73 = 27
grade = F (Critical)
```

### Example 3: Perfect Score

**Violations**:
- Critical: 0
- High: 0
- Medium: 0
- Low: 0

**Calculation**:
```
penalty_total = 0
health_score = 100
grade = A (Excellent)
```
