# Frameworks Reference: Root Cause Identifier

Detailed reference for the 5 Whys and SCAMPER frameworks used by root-cause-identifier.

---

## 5 Whys Framework

### Origin & Purpose
Developed by Sakichi Toyoda for Toyota's manufacturing process. The technique asks "Why?" iteratively to peel away symptom layers and reveal root causes.

### Core Principles

1. **Start with observable facts**: Begin with a clear, specific symptom
2. **One question at a time**: Each level addresses one "why"
3. **Evidence-based answers**: Every answer must have supporting evidence
4. **Avoid assumptions**: Challenge each answer with "How do we know?"
5. **Stop at actionable**: Continue until you reach something that can be fixed

### When to Use
- Incident investigation
- Bug root cause analysis
- Process failure analysis
- Recurring issue investigation
- Post-mortem analysis

### When NOT to Use
- Multiple unrelated root causes (use fishbone diagram instead)
- Statistical process variation (use statistical analysis)
- Broad exploratory research (use other research methods)

### Common Pitfalls

| Pitfall | Description | Prevention |
|---------|-------------|------------|
| Stopping too early | Accepting symptom as root cause | Ask "Can we fix this directly?" |
| Going too deep | Reaching philosophical causes | Stop when actionable |
| Single path bias | Missing alternative causes | Document alternatives |
| Assumption injection | Answers without evidence | Require evidence for each |
| Circular reasoning | Root leads back to symptom | Validate non-circularity |


### Example Application

**Symptom**: API returns 500 errors intermittently

```
Why 1: Why is the API returning 500 errors?
→ Database queries are timing out
Evidence: Error logs show "QueryTimeoutException" at 30s threshold

Why 2: Why are database queries timing out?
→ Query execution time exceeds 30s during peak hours
Evidence: Query metrics show p99 latency of 45s between 2-4pm

Why 3: Why is query execution slow during peak hours?
→ Full table scans on orders table
Evidence: EXPLAIN shows sequential scan, no index used

Why 4: Why are full table scans occurring?
→ Missing index on customer_id column used in WHERE clause
Evidence: Schema shows no index, query uses customer_id filter

Why 5: Why is the index missing?
→ Migration for index was never deployed to production
Evidence: Migration exists in code but not in prod schema

Root Cause: Index migration deployment was missed
Category: process (deployment procedure gap)
Actionable: Yes - deploy the migration
Non-circular: Yes - deploying index doesn't cause 500 errors
```

---

## SCAMPER Framework

### Origin & Purpose
Developed by Bob Eberle based on Alex Osborn's brainstorming questions. Originally for creative ideation, adapted here for generating improvement recommendations.

### The Seven Lenses

#### S - Substitute
**Question**: What can we replace to prevent recurrence?
**Applications**:
- Replace manual process with automation
- Substitute error-prone component with robust alternative
- Replace synchronous with asynchronous processing
- Substitute in-house solution with proven library

#### C - Combine
**Question**: What can we merge to reduce failure points?
**Applications**:
- Combine validation steps into single check
- Merge related services to reduce integration points
- Combine monitoring and alerting into unified system
- Merge duplicate code paths


#### A - Adapt
**Question**: What can we borrow from other solutions?
**Applications**:
- Adapt retry patterns from similar service
- Borrow circuit breaker pattern from resilient system
- Apply caching strategy from high-traffic component
- Adapt testing approach from more stable module

#### M - Modify
**Question**: What can we change in scale, frequency, or process?
**Applications**:
- Increase monitoring frequency
- Scale timeout thresholds
- Modify batch sizes
- Change deployment frequency
- Adjust resource allocation

#### P - Put to Other Use
**Question**: Can existing tools or patterns solve this?
**Applications**:
- Use existing circuit breaker for new service
- Apply existing validation framework
- Leverage existing monitoring infrastructure
- Repurpose existing error handling patterns

#### E - Eliminate
**Question**: What can we remove to simplify?
**Applications**:
- Remove unnecessary dependencies
- Eliminate redundant processing steps
- Remove legacy compatibility code
- Eliminate manual approval bottlenecks

#### R - Reverse/Rearrange
**Question**: Can we reorder steps to prevent failure?
**Applications**:
- Move validation earlier in pipeline
- Rearrange deployment order
- Reverse dependency direction
- Reorder initialization sequence

### Recommendation Quality Criteria

| Criterion | Description |
|-----------|-------------|
| Root cause linkage | Directly addresses identified root cause |
| Recurrence prevention | Prevents issue from happening again |
| Feasibility | Can be implemented with available resources |
| Impact/Effort ratio | Benefit justifies implementation cost |
| Side effects | Minimal negative impact on other systems |

### Effort Estimation Guide

| Level | Characteristics |
|-------|-----------------|
| Low | <1 day, single file/component, no dependencies |
| Medium | 1-5 days, multiple files, some coordination |
| High | >5 days, cross-system, significant coordination |

### Impact Estimation Guide

| Level | Characteristics |
|-------|-----------------|
| Low | Reduces but doesn't eliminate recurrence risk |
| Medium | Significantly reduces recurrence probability |
| High | Eliminates root cause, prevents all recurrence |
