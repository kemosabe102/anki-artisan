# 5 Whys Root Cause Analysis

## Purpose

Drill past symptoms to find the fundamental, actionable root cause.

---

## Process

1. Start with the observed problem
2. Ask "Why did this happen?"
3. Answer with evidence-based statement
4. Repeat until reaching actionable root cause
5. Stop when further "why" leads to organizational/external factors

---

## Example

**Problem**: User login fails intermittently

```
Why #1: Why does login fail?
→ Because JWT token validation returns false

Why #2: Why does token validation return false?
→ Because token appears expired

Why #3: Why does token appear expired?
→ Because server time differs from token issuer time

Why #4: Why do times differ?
→ Because server uses local timezone, issuer uses UTC

Why #5: Why does server use local timezone?
→ Because datetime.now() was used instead of datetime.utcnow()

ROOT CAUSE: Timezone handling inconsistency in token validation
ACTIONABLE FIX: Use UTC consistently in auth module
```

---

## Rules

| Rule | Description |
|------|-------------|
| Stay evidence-based | Each answer must have supporting evidence |
| Avoid blame | Focus on systems, not people |
| Stop at actionable | When you can fix it, you've found the root |
| Document chain | Full chain is valuable for future reference |

---

## Anti-Patterns

- **Stopping at symptom**: "Token validation fails" is not root cause
- **Guessing**: Every answer needs evidence
- **Going too deep**: "Why was the developer hired?" is too far
- **Multiple branches**: Focus on one path at a time

---

## Output Format

```json
{
  "five_whys": [
    "Login fails because JWT validation returns false",
    "Validation fails because token appears expired",
    "Token appears expired because of time difference",
    "Times differ because server uses local timezone",
    "Local timezone used because datetime.now() instead of utcnow()"
  ],
  "root_cause": "Timezone handling inconsistency",
  "actionable_fix": "Use UTC consistently in datetime operations"
}
```
