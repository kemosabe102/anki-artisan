# TDD Component Status Template

**File Location:** `.claude/workflows/TDD_STATUS.md`

Use this template to track progress on a component implementation.

---

## Component: [Component Name]

### Current Phase
- [ ] Phase 1: RED - Writing failing test
- [ ] Phase 2: GREEN - Making test pass
- [ ] Phase 3: REFACTOR - Improving code quality
- [ ] Phase 4: SELF-REVIEW - Quality verification
- [ ] Phase 5: COMMIT - Atomic commit

### Details
- **Test**: [test name or path]
- **Implementation**: [notes on what's being implemented]
- **Coverage**: [estimated or actual %]

### Time Tracking
- **Started**: [timestamp]
- **Current Duration**: [X minutes]
- **Phase Durations**: RED [X min] | GREEN [X min] | REFACTOR [X min]

---

## Example

```markdown
## Component: PasswordHasher

### Current Phase
- [x] Phase 1: RED - Writing failing test
- [x] Phase 2: GREEN - Making test pass
- [ ] Phase 3: REFACTOR - Improving code quality
- [ ] Phase 4: SELF-REVIEW - Quality verification
- [ ] Phase 5: COMMIT - Atomic commit

### Details
- **Test**: `tests/unit/test_password_hasher.py::test_hash_differs_from_input`
- **Implementation**: SHA256 hashing with UTF-8 encoding
- **Coverage**: 100%

### Time Tracking
- **Started**: 2025-01-15 10:30
- **Current Duration**: 25 minutes
- **Phase Durations**: RED 8 min | GREEN 12 min | REFACTOR 5 min
```
