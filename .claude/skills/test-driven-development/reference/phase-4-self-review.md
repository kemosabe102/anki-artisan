# Phase 2D: Chunk Self-Review

**Goal:** Review this chunk before committing to ensure it's production-ready.

---

## Activities

### 1. Review the diff for this chunk only

```bash
git diff feature/your-feature-name...main -- <files in this chunk>
```

### 2. Mental walkthrough

- Step through the code with different inputs
- What happens with valid input? Invalid input? Boundary values?
- Are error messages helpful?

### 3. Edge case check

- Empty/null inputs?
- Very large inputs?
- Negative numbers (if applicable)?
- Special characters (if applicable)?

### 4. Cleanup check

- Any `console.log()` left in code?
- Any commented-out code?
- Any `TODO` or `FIXME` comments?
- Any test debug code (`.only`, `.skip`)?

### 5. Test coverage check

Run tests with coverage report:

```bash
npm test -- --coverage  # JavaScript
pytest --cov            # Python
```

- Are all new lines covered by tests?

---

## Definition of Done (Commit when)

- [ ] Chunk implements ONE coherent piece of functionality
- [ ] ALL tests for this chunk PASS
- [ ] Code follows team conventions (naming, style, structure)
- [ ] No debug code, console.logs, or commented-out code remains
- [ ] Edge cases for this chunk are tested and handled
- [ ] Variable/function names are consistent and descriptive
- [ ] Test coverage is >80% for this chunk
- [ ] No `.only` or `.skip` in test files
- [ ] You can write a clear commit message explaining this chunk

---

## Time Investment

5-10 minutes per chunk

---

## Related Skills to Invoke

- **code-review-standards** (final checklist)
- **test-naming-conventions** (if team has specific patterns)
