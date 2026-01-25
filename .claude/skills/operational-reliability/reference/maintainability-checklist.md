# Maintainability Checklist (Historian Hat)

**Source**: `.claude/docs/01-guides/review/operational-edge-reliability.md`

## Cognitive Load

### MT-001: Single-Read Comprehension
- **Check**: Code readable in one pass
- **Severity**: LOW
- **Evidence**: Function length, nesting depth
- **Pass**: Function fits on screen, clear flow
- **Fail**: Requires multiple reads to understand

### MT-002: No Clever Code
- **Check**: Obvious over clever
- **Severity**: LOW
- **Evidence**: Complex one-liners, obscure patterns
- **Pass**: Straightforward implementation
- **Fail**: "Clever" code requiring explanation

### MT-003: Naming Clarity
- **Check**: Names reveal intent
- **Severity**: LOW
- **Evidence**: Variable and function names
- **Pass**: `calculate_total_price` not `calc`
- **Fail**: Abbreviations, single letters

## Dependency Hygiene

### MT-004: Minimal Imports
- **Check**: Only necessary dependencies imported
- **Severity**: LOW
- **Evidence**: Import statements count
- **Pass**: Focused imports, no unused deps
- **Fail**: Kitchen-sink imports

### MT-005: Dependency Weight
- **Check**: Heavy dependencies justified
- **Severity**: LOW
- **Evidence**: requirements.txt, transitive deps
- **Pass**: Dependencies proportional to value
- **Fail**: Large library for small feature

## Long-Term Maintainability

### MT-006: Test Coverage
- **Check**: Changed code has tests
- **Severity**: MEDIUM
- **Evidence**: Test files, coverage report
- **Pass**: New logic has corresponding tests
- **Fail**: Untested changes

### MT-007: Documentation Currency
- **Check**: Docs match implementation
- **Severity**: LOW
- **Evidence**: Docstrings, README, comments
- **Pass**: Documentation accurate
- **Fail**: Stale or missing documentation
