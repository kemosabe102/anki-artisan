# Invariant Core Checklist

**Source**: `.claude/docs/01-guides/review/system-node-reliability.md`

## Precondition Validation

### IC-001: Fail Fast
- **Check**: Input validation fails immediately
- **Severity**: HIGH
- **Evidence**: Guard clauses, early returns, assertion statements
- **Pass**: Invalid input rejected before processing begins
- **Fail**: Validation mixed with business logic

### IC-002: Input Sanitization
- **Check**: External input is validated at boundary
- **Severity**: HIGH
- **Evidence**: Pydantic models, validation decorators
- **Pass**: Type and value validation on all inputs
- **Fail**: Raw input passed to business logic

## Postcondition Guarantees

### IC-003: Return Value Contracts
- **Check**: Methods honor their return type promises
- **Severity**: MEDIUM
- **Evidence**: Type hints, return statements
- **Pass**: Never null when typed as non-optional, empty list not None
- **Fail**: Returns None when type says otherwise

### IC-004: Exception Documentation
- **Check**: Raised exceptions are documented
- **Severity**: LOW
- **Evidence**: Docstrings, type annotations (raises)
- **Pass**: All exception types documented
- **Fail**: Undocumented exceptions possible

## Class Invariants

### IC-005: No Half-Broken States
- **Check**: Object is always in valid state after construction
- **Severity**: HIGH
- **Evidence**: Constructor validation, property setters
- **Pass**: Invalid state impossible (e.g., startDate <= endDate)
- **Fail**: Partial initialization allowed

### IC-006: Consistent State After Operations
- **Check**: Methods leave object in valid state
- **Severity**: HIGH
- **Evidence**: State mutation patterns
- **Pass**: All public methods maintain invariants
- **Fail**: Method can leave object inconsistent
