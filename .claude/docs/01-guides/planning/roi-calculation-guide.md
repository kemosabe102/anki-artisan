# ROI Calculation Guide - Hours-Based Approach

**Purpose**: Standardize ROI calculations using developer hours, not dollars
**Principle**: Conservative estimates in hours/month for individual developers
**Last Updated**: 2025-10-03

## Core Principle

**Express ROI in hours saved per month, not dollar values.**

Dollar values are reference-only with clear disclaimers.

## Calculation Framework

### Step 1: Identify Time-Consuming Activities

```
What tasks take significant time?
├── Manual processes
├── Repetitive work
├── Error-prone activities
├── Coordination overhead
└── Knowledge searching
```

### Step 2: Measure Current State

```
For each activity:
- Time per occurrence: X hours
- Frequency: N times per month
- People affected: M developers
- Current monthly time: X × N × M hours
```

### Step 3: Estimate Improved State

```
After implementation:
- Reduced time: Y hours (must be < X)
- Same frequency: N times
- Same or more people: M+ developers
- Future monthly time: Y × N × M hours
```

### Step 4: Calculate Raw Savings

```
Raw savings = Current time - Future time
            = (X × N × M) - (Y × N × M)
            = (X - Y) × N × M hours/month
```

### Step 5: Apply Conservative Factor

```
Conservative estimate = Raw savings × 0.7
(Accounts for learning curve, adoption rate, edge cases)
```

## Example Calculations

### Example 1: Development Environment Setup

```
Current State:
- Time: 4 hours per setup
- Frequency: 2 new developers/month
- Current total: 8 hours/month

Target State:
- Time: 30 minutes per setup
- Frequency: 2 new developers/month
- Target total: 1 hour/month

Raw Savings: 7 hours/month
Conservative: 4.9 hours/month (70%)
```

### Example 2: Code Review Process

```
Current State:
- Time: 3 days (24 hours) per PR
- Frequency: 4 PRs/month
- Current total: 96 hours/month

Target State:
- Time: 4 hours per PR
- Frequency: 4 PRs/month
- Target total: 16 hours/month

Raw Savings: 80 hours/month
Conservative: 56 hours/month (70%)
```

### Example 3: Bug Investigation

```
Current State:
- Time: 2 hours to identify root cause
- Frequency: 10 bugs/month
- Current total: 20 hours/month

Target State:
- Time: 15 minutes with better logs
- Frequency: 10 bugs/month
- Target total: 2.5 hours/month

Raw Savings: 17.5 hours/month
Conservative: 12.25 hours/month (70%)
```

## Conservative Estimation Rules

### ALWAYS Be Conservative ✅

- Use 70% confidence factor
- Round down, not up
- Account for learning time
- Assume gradual adoption
- Include edge cases

### NEVER Be Optimistic ❌

- Don't assume 100% adoption
- Don't ignore setup time
- Don't claim instant results
- Don't forget maintenance
- Don't use best-case scenarios

## ROI Presentation Template

### Correct Format ✅

```markdown
## ROI Analysis (Time-Based)

| Activity  | Current | Target | Saved    | Frequency | Monthly Hours Saved |
| --------- | ------- | ------ | -------- | --------- | ------------------- |
| PR Review | 24 hrs  | 4 hrs  | 20 hrs   | 4/month   | 80 hours            |
| Bug Fixes | 2 hrs   | 15 min | 1.75 hrs | 10/month  | 17.5 hours          |

**Total Monthly Time Savings:** 97.5 hours (raw)
**Conservative Estimate:** 68.25 hours/month (70% confidence)

_Note: Dollar values shown for reference only at assumed $100/hour rate_
_Actual value: 68.25 hours × $100 = ~$6,825/month (reference only)_
```

### Incorrect Format ❌

```markdown
## ROI Analysis

This will save $15,000 per month!

Developers will be 10x more productive!

We'll eliminate all bugs!
```

## Time Savings Categories

### High-Impact (>20 hours/month)

- Deployment automation
- Test automation
- Code generation
- Review streamlining

### Medium-Impact (5-20 hours/month)

- Documentation search
- Environment setup
- Debugging tools
- Build optimization

### Low-Impact (<5 hours/month)

- Linting automation
- Formatting tools
- Snippet management
- Shortcut optimization

## Validation Questions

Before claiming ROI, answer:

1. **Is the current time realistic?**
   - Based on actual measurements?
   - Includes all steps?
   - Accounts for variations?

2. **Is the target time achievable?**
   - Based on proven tools?
   - Tested in similar contexts?
   - Includes overhead?

3. **Is the frequency accurate?**
   - Based on historical data?
   - Accounts for seasonality?
   - Realistic for team size?

4. **Are people counts correct?**
   - Current team size?
   - Growth projections?
   - Actual users of feature?

## Common Pitfalls

### Pitfall 1: Claiming Dollar Values

❌ "Saves $10,000/month"
✅ "Saves 100 developer hours/month"

### Pitfall 2: Ignoring Learning Curve

❌ "Immediate 4x productivity"
✅ "After 1-month ramp-up, 2x efficiency"

### Pitfall 3: Perfect Adoption

❌ "All developers will use it"
✅ "Assuming 70% adoption rate"

### Pitfall 4: Best-Case Only

❌ "Reduces time from 4 hours to 0"
✅ "Reduces time from 4 hours to 30 minutes"

## Disclaimer Template

Always include this disclaimer:

```markdown
**ROI Disclaimer:**

- Measured in developer hours saved per month
- Conservative estimates with 70% confidence factor
- Dollar values ($100/hour) shown for reference only
- Actual savings depend on adoption and team size
- Includes learning curve and ramp-up time
```

## Quick Reference Formula

```
Monthly Hours Saved = Σ(Current_Time - Target_Time) × Frequency × 0.7

Where:
- Current_Time = Hours per task now
- Target_Time = Hours per task after improvement
- Frequency = Times per month task occurs
- 0.7 = Conservative factor
```

## Reporting Standards

### Monthly Report Format

```markdown
## October 2025 ROI Report

**Measured Improvements:**

- Setup time: 3.5 hours → 30 minutes (3 hrs saved × 2/month = 6 hrs/month)
- Debug time: 2 hours → 15 minutes (1.75 hrs saved × 10/month = 17.5 hrs/month)

**Total Measured Savings:** 23.5 hours/month
**Projected Annual:** 282 hours/year

**Adoption Metrics:**

- Current adoption: 65% of team
- Target adoption: 85% by Q2
```

### Avoid These Claims

- "Worth $X million annually"
- "Pays for itself in days"
- "10x ROI guaranteed"
- "Saves $X per developer"

## Audit Checklist

When reviewing ROI claims:

- [ ] Expressed in hours/month?
- [ ] Conservative factor applied?
- [ ] Dollar values marked as reference?
- [ ] Assumptions documented?
- [ ] Measurements realistic?
- [ ] Learning time included?
- [ ] Adoption rate stated?
- [ ] Maintenance considered?

---

**Remember**: We measure value in time saved, not dollars earned. Be conservative, be honest, be helpful.
