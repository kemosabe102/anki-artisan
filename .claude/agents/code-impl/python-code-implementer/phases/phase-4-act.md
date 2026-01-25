# Phase 4: ACT - Implementation & Validation

**OODA Stage**: ACT | **Time Allocation**: 50-55%

**Purpose**: Execute TDD workflow, implement code, validate with defensive checks, self-review

**Deliverable**: Implemented code, passing tests, security verification, self-review evidence

---

## Workflow Steps

### Step 4.1: TDD Workflow Execution

**Trigger**: Before ANY production code modification

**Protocol** (from Enforcement Gates):
1. If `tests_needed: true` from Phase 1:
   - Create test file FIRST with failing test for expected behavior
   - Run test: `AGENT_NAME=python-code-implementer uv run pytest <test_file> -v`
   - Confirm it fails (proves test is meaningful)
2. Implement production code to pass tests
3. Run full test suite to verify pass

**Evidence Required**:
```json
{
  "tdd_evidence": {
    "existing_tests_found": ["tests/unit/test_auth.py:45-67"],
    "tests_created": ["tests/unit/test_new_feature.py"],
    "pre_impl_test_run": "1 failed (expected)",
    "post_impl_test_run": "5 passed in 0.3s"
  }
}
```

**HALT Conditions**:
- `tdd_evidence` missing -> `failure_type: "tdd_gate_violation"`
- `post_impl_test_run` shows failures -> `failure_type: "tests_failing"`

**Extended Reference**: For comprehensive TDD methodology including feature chunking, 
Definition of Done checklists, and anti-pattern avoidance, see:
`.claude/skills/test-driven-development/SKILL.md`

---

### Step 4.2: Security Pre-Flight (MANDATORY)

**Cross-Reference**: coding-guidelines.md for full pattern details

**Address ALL items with evidence**:

| Pattern | Verification | Evidence Format |
|---------|--------------|-----------------|
| Path Validation | `pathlib.Path.resolve()` + `.relative_to()` | Line numbers OR "N/A: no user paths" |
| Subprocess Safety | NO `shell=True`; use list args | Line numbers OR "N/A: no subprocess" |
| Regex Safety | No nested quantifiers; compile at module level | Line numbers OR "N/A: no regex" |
| Input Validation | Whitelist before file paths, SQL params | Line numbers OR "N/A: no external input" |
| Secret Handling | No hardcoded credentials | "Verified: no secrets" |
| Mutable Defaults | No `[]`, `{}`, `set()` defaults; use `None` | Grep result OR "N/A: no default args" |
| Empty Collections | Check `.empty` or `len()` before aggregation | Line numbers OR "N/A: no collection processing" |

**HALT Condition**: Any pattern not addressed -> `failure_type: "security_preflight_incomplete"`

---

### Step 4.3: Defensive Programming Gate

**Trigger**: Before returning implementation results

**Verification Protocol**:

1. **DP-02: No Mutable Defaults**
   - Grep for `=[]`, `={}`, `=set()` in function signatures
   - Fix with `None` sentinel pattern if found

2. **DP-03: No Bare Exception Catching**
   - No bare `except Exception:` without re-raise
   - Specific exceptions only

3. **DP-10: Input Validation at Entry Points**
   - Public functions validate inputs
   - Internal functions may skip (document as "N/A: internal function")

**Evidence Required**:
```json
{
  "defensive_checks": {
    "mutable_defaults": "none found" | "lines X, Y fixed",
    "exception_handling": "specific exceptions only" | "lines X, Y use Exception with re-raise",
    "input_validation": "validated at lines X, Y" | "N/A: internal function"
  }
}
```

**HALT Condition**: Mutable default found and not fixed -> `failure_type: "mutable_default_violation"`

---

### Step 4.4: Self-Review Checklist (MANDATORY EVIDENCE)

**Trigger**: Before returning results

**Complexity-Based Evidence Depth**:
| Complexity | Criteria | Evidence Depth |
|------------|----------|----------------|
| Simple | Single file, <20 lines | Brief (1 sentence per category) |
| Moderate | 2-3 files, 20-100 lines | Standard (specific line references) |
| Complex | 4+ files, >100 lines | Detailed (rationale + line refs + test mapping) |

**Required Categories**:

| Category | Evidence Required |
|----------|-------------------|
| Correctness | "Verified by test: `test_<name>` at line X" OR "Manual assertion: [check]" |
| Readability | "Functions <20 lines, clear names, docstrings where non-obvious" |
| Maintainability | "No magic numbers, constants extracted, single responsibility" |
| Security | Reference security_verification output from Step 4.2 |
| Performance | "Regex compiled: [Y/N/NA], generators used: [Y/N/NA], no N+1 queries" |
| Standards | "Linter: [clean/N warnings], Type hints: [complete/partial]" |
| Defensive | "DP-02: [status], DP-03: [status], DP-10: [status]" |

**HALT Condition**: Any category lacks specific evidence -> `failure_type: "self_review_incomplete"`

---

### Step 4.5: File Operations

**Tool Selection** (use available tools based on environment):
| Operation | Built-in Tool | MCP Equivalent | Note |
|-----------|---------------|----------------|------|
| Read files | `Read` | `mcp__desktop-commander__read_file` | Prefer over Bash cat |
| Search content | `Grep` | `mcp__desktop-commander__start_search` | Prefer over Bash grep |
| Find files | `Glob` | `mcp__desktop-commander__list_directory` | Prefer over Bash find |
| Edit existing | `Edit` | `mcp__desktop-commander__edit_block` | Surgical replacements |
| Write new | `Write` | `mcp__desktop-commander__write_file` | Chunk ≤30 lines |
| Run tests | `Bash` | - | `AGENT_NAME=python-code-implementer uv run pytest` |
| Run linter | `Bash` | - | `AGENT_NAME=python-code-implementer uv run ruff check` |

**Chunking**: All file modifications should be ≤30 lines per operation (writes AND edits).

**Execution Order**:
1. Test files (if TDD creating new tests)
2. Production files (sequential, one at a time)
3. Lint/format after writes
4. Final test run to verify

---

## Quick Checklist

Before marking complete:

- [ ] TDD evidence captured (tests created/found, pre/post run results)
- [ ] Security pre-flight ALL items addressed
- [ ] Defensive programming gate passed
- [ ] Self-review ALL categories with evidence
- [ ] Linter clean, tests passing
- [ ] Output schema complete

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Implementing before tests | TDD: write failing test FIRST |
| Skipping security items | Address ALL 7 patterns with evidence |
| Generic self-review | Provide specific line references |
| Mutable defaults | Use `None` sentinel, not `[]` or `{}` |
| Bare except blocks | Use specific exceptions only |

---

## Exit Criteria

**All criteria must pass to complete**

| Criterion | Weight | Check |
|-----------|--------|-------|
| TDD complete | 0.25 | `tdd_evidence` populated, tests passing |
| Security verified | 0.20 | All 7 patterns addressed |
| Defensive gate | 0.15 | DP-02, DP-03, DP-10 verified |
| Self-review | 0.25 | All 7 categories with evidence |
| Linter clean | 0.15 | No errors from ruff check |

---

## Reference Documentation

- coding-guidelines.md - Security patterns (canonical source)
- defensive-programming-guide.md - DP-01 to DP-12 checklist
- file-operation-protocol.md - File operations

---

**Previous Phase**: [Phase 3: DECIDE](phase-3-decide.md)
**Complete**: Return to [python-code-implementer.md](../python-code-implementer.md)
