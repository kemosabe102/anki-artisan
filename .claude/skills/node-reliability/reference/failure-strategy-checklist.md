# Failure Strategy Checklist

**Source**: `.claude/docs/01-guides/review/system-node-reliability.md`

## Exception Hierarchy

### FS-001: Typed Exceptions
- **Check**: Specific exception types used
- **Severity**: MEDIUM
- **Evidence**: Custom exception classes
- **Pass**: `PaymentDeclinedException` not `RuntimeException`
- **Fail**: Generic Exception for all errors

### FS-002: Exception Context
- **Check**: Error messages include relevant values
- **Severity**: LOW
- **Evidence**: Exception message content
- **Pass**: `f"User {user_id} not found"` with context
- **Fail**: `"User not found"` without ID

## Atomic Failure

### FS-003: All-or-Nothing Operations
- **Check**: Partial failure doesn't leave dirty state
- **Severity**: HIGH
- **Evidence**: Multi-step operations, transactions
- **Pass**: Rollback on failure, cleanup in finally
- **Fail**: Partial updates persist on error

### FS-004: Resource Cleanup
- **Check**: Resources released on all paths
- **Severity**: HIGH
- **Evidence**: File handles, connections, locks
- **Pass**: Context managers, try/finally
- **Fail**: Resources leak on exception

## Error Propagation

### FS-005: Exception Chain Preservation
- **Check**: Original exception context preserved
- **Severity**: MEDIUM
- **Evidence**: `raise X from e` pattern
- **Pass**: Chained exceptions maintain stack
- **Fail**: `raise X` losing original context
