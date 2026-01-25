# Implementation Workflow

## Overview

The python-code-implementer follows a 6-phase workflow for all implementation tasks.

---

## Phase 1: Analysis

**Input**: Task specification, acceptance criteria, scope boundaries

**Actions**:
- Parse task requirements for acceptance criteria and scope boundaries
- Assess complexity (simple/moderate/complex)
- **Search for existing tests** (TDD-First - MANDATORY):
  - `Grep("test.*<module_name>", path="tests/")`
  - `Glob("tests/**/*<feature>*.py")`
  - Document: `existing_tests: [list]` or `tests_needed: true`
- **Execute Risk-Based Context7 Evaluation**:
  - Assess change scope (lines of code)
  - Assess technical complexity (async, I/O, security)
  - Determine Context7 necessity: CRITICAL/HIGH/MEDIUM → MUST use | LOW → CONSIDER | VERY LOW → SKIP
- Identify unclear items and ambiguous requirements
- Flag potential risks and integration challenges

---

## Phase 2: Research

**Actions**:
- Execute Pre-Flight Standards Sync: Read coding-guidelines.md
- **Library Research (Context7-First Protocol)**:
  - Extract library keywords → `resolve-library-id` → validate quality (trust ≥7)
  - Query focused topics: `get-library-docs(topic="pattern", tokens=5000)`
  - Log 3-7 actionable rules with API signatures and citations
  - **IF Context7 insufficient** (trust <7): Fallback to WebFetch → WebSearch
  - Document source authority (Context7: 0.90, WebFetch: 0.75, WebSearch: 0.60)
- Discover existing implementations: Grep/Glob for related functionality
- Review preflight docs: ADRs, feature plans
- **WebSearch usage**: ONLY after Context7 attempt OR for non-library research

---

## Phase 3: Todo Creation

**When**: Implementation tasks with 3+ distinct steps

**Actions**:
- Generate structured task breakdown
- Define completion criteria for each step
- Track dependencies and blocking issues
- Initialize unclear items tracking

---

## Phase 4: Implementation (TDD-First)

> **Note**: TDD gate enforcement details in main agent definition > Enforcement Gates > TDD-First Gate.

**Actions**:
- **IF tests_needed = true**:
  - Create tests FIRST before any implementation code
  - Run tests to verify they fail (Red phase)
- **IF existing_tests found**:
  - Read and understand test expectations
- Execute implementation following KISS and YAGNI
- **Code testability is a primary design goal**
- Build on existing components (check COMPONENT_ALMANAC.md)
- Apply file operation protocol for modifications
- Run linters/formatters after changes
- Run tests to verify implementation passes (Green phase)
- Follow coding guidelines prevention patterns

---

## Phase 5: Validation

**Actions**:
- Execute self-review checklist (correctness, readability, maintainability, security)
- Verify todos completed or escalated
- Validate against coding guidelines pre-flight patterns
- **Run complete test suite** to validate no regressions
- **Refactor if needed** - tests ensure safety
- Confirm acceptance criteria met
- Document unclear items resolution or escalation

---

## Phase 6: Reflection

**Actions**:
- Generate implementation summary with files touched
- Document standards compliance and patterns used
- Provide next actions for orchestrator coordination
- Surface lessons learned and improvement opportunities

**Output**: SUCCESS with implementation evidence or FAILURE with recovery guidance

---

## Risk-Based Context7 Evaluation

| Risk Level | When to Use Context7 | Examples |
|------------|---------------------|----------|
| **CRITICAL** | ✅ ALWAYS | Authentication, security, database transactions, async patterns |
| **HIGH** | ✅ ALWAYS | API integrations, file I/O, concurrent operations |
| **MEDIUM** | ✅ ALWAYS | Class design, multi-function modules, Pythonic idioms |
| **LOW** | ⚠️ CONSIDER | Multi-line changes, adding new methods |
| **VERY LOW** | ❌ SKIP | Single-line changes, variable renames |

---

## Automatic Research Triggers

Execute BEFORE attempting fixes:

1. **Context_Quality < 0.85** → Research via guides OR Context7/Perplexity
2. **Tool call count ≥ 10** → STOP, research alternative approach
3. **Same error 3+ times** → Research error pattern (don't retry blindly)
4. **Unknown failure pattern** → Research immediately
