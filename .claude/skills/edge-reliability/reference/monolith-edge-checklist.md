# Monolith Edge Reliability Checklist

**Source**: `.claude/docs/01-guides/review/monolith-edge-reliability.md`

## Transactional Edge (The "Logical Lock")

### TX-001: Sandwich Rule
- **Check**: Transaction is the "meat" not the "bread"
- **Severity**: HIGH
- **Evidence**: @Transactional scope, context manager usage
- **Pass**: Transaction wraps only DB ops, not external calls
- **Fail**: Transaction spans HTTP calls, file I/O

### TX-002: No External Calls in Transaction
- **Check**: HTTP/gRPC calls are outside transaction boundary
- **Severity**: CRITICAL
- **Evidence**: Look for requests.* or httpx.* inside @Transactional
- **Pass**: External calls before/after transaction
- **Fail**: External call inside transaction block

### TX-003: Deadlock Prevention
- **Check**: Component update ordering is consistent
- **Severity**: CRITICAL
- **Evidence**: Lock acquisition order, table update order
- **Pass**: Documented ordering, consistent across codebase
- **Fail**: Inconsistent ordering, potential circular waits

## Shared Resource Edge (The "Starvation" Edge)

### SR-001: Thread Pool Isolation
- **Check**: Separate thread pools for different concerns
- **Severity**: HIGH
- **Evidence**: ThreadPoolExecutor instances, pool configuration
- **Pass**: CPU-bound and I/O-bound work in separate pools
- **Fail**: Single shared pool for all work

### SR-002: Memory Bounds
- **Check**: No unbounded data loads
- **Severity**: HIGH
- **Evidence**: findAll(), SELECT * without LIMIT
- **Pass**: Pagination, streaming, or explicit limits
- **Fail**: Unbounded queries loading full tables

### SR-003: Cache Eviction
- **Check**: Static caches have eviction policy
- **Severity**: MEDIUM
- **Evidence**: @lru_cache maxsize, TTL configuration
- **Pass**: Explicit maxsize or TTL
- **Fail**: Unbounded cache growth

## Coupling Edge (The "Side Effect" Edge)

### CE-001: Defensive Copying
- **Check**: Mutable objects are copied at boundaries
- **Severity**: MEDIUM
- **Evidence**: copy.deepcopy, .copy(), immutable types
- **Pass**: Defensive copy or immutable return
- **Fail**: Mutable object passed by reference

### CE-002: Side Effect Isolation
- **Check**: Pure reads have no side effects
- **Severity**: HIGH
- **Evidence**: GET methods modifying state
- **Pass**: Read operations are idempotent
- **Fail**: Read methods mutate state

### CE-003: ThreadLocal/Singleton Hygiene
- **Check**: No polluted global state
- **Severity**: MEDIUM
- **Evidence**: threading.local(), module-level singletons
- **Pass**: Proper cleanup, request-scoped state
- **Fail**: State leaks between requests
