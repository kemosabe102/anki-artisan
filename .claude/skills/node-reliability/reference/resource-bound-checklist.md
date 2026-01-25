# Resource Bound Checklist

**Source**: `.claude/docs/01-guides/review/system-node-reliability.md`

## Memory Safety

### RB-001: Bounded Allocations
- **Check**: No unbounded allocations based on user input
- **Severity**: CRITICAL
- **Evidence**: List/dict creation from external input
- **Pass**: Explicit size limits, pagination
- **Fail**: `[x for x in user_input]` without limit

### RB-002: Streaming Large Data
- **Check**: Large datasets processed incrementally
- **Severity**: HIGH
- **Evidence**: Generators, chunked processing
- **Pass**: yield-based iteration, batch processing
- **Fail**: Loading entire dataset into memory

## Algorithmic Complexity

### RB-003: Linear Complexity
- **Check**: No hidden O(n²) or worse
- **Severity**: MEDIUM
- **Evidence**: Nested loops, repeated list operations
- **Pass**: O(n) or O(n log n) algorithms
- **Fail**: Nested iteration over same collection

### RB-004: Recursion Depth
- **Check**: Recursive calls have depth limits
- **Severity**: HIGH
- **Evidence**: Recursive functions, tree traversal
- **Pass**: Explicit depth limit or iterative alternative
- **Fail**: Unbounded recursion possible

## Regex Safety

### RB-005: ReDoS Prevention
- **Check**: Regex patterns are safe from catastrophic backtracking
- **Severity**: HIGH
- **Evidence**: Complex regex with nested quantifiers
- **Pass**: Simple patterns, timeout on regex operations
- **Fail**: `(a+)+b` style vulnerable patterns
