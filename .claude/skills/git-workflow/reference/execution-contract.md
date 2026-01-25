# Execution Contract Reference

**Purpose**: Explains WHY each step in the prepare workflow is mandatory.

---

## Contract Summary

| Step | Name | Why Mandatory? |
|------|------|----------------|
| 0 | CI Validation | Fail fast - don't waste time grouping broken code |
| 1 | Semantic Categorization | Domain isolation enables targeted review |
| 2 | File Grouping | Creates atomic, reversible commits |
| 3 | Quality Gates | Catches critical issues before merge |
| 4 | Present Summary | Human approval required before commit |

---

## Step Dependencies

```
Step 0 → Step 1 → Step 2 → Step 3 → Step 4
         │        │        │
         └── depends on ───┘
```

- Steps 1-2 cannot proceed if Step 0 fails (without `--skip-validation`)
- Step 4 cannot proceed if Step 3 is incomplete (without `--skip-quality`)
- Commit phase requires completed prepare phase

---

## Why This Order?

1. **CI first**: If tests fail, grouping is wasted effort
2. **Categorization before grouping**: Domain determines quality agents
3. **Quality gates before summary**: User sees final status
4. **Summary before commit**: Human-in-the-loop approval

---

## Contract Violations

A violation occurs when:
- Presenting summary without completing required steps
- Committing without prior prepare in session
- Skipping mandatory steps without explicit flags

---

## See Also

- Execution logic: `.claude/commands/git.md`
- SKILL reference: `../SKILL.md`
