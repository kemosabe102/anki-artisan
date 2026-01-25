---
title: "Code Reuse Framework"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Code Reuse Framework

**Purpose**: Decision framework for reusing, extending, or replacing existing code to prevent duplication and reduce technical debt.

**Last Updated**: 2025-10-03

---

## Table of Contents

1. [Core Principles](#core-principles)
2. [Build vs Extend vs Replace Decision Tree](#build-vs-extend-vs-replace-decision-tree)
3. [Integration Pattern Library](#integration-pattern-library)
4. [Cleanup Task Prioritization](#cleanup-task-prioritization)
5. [Time Savings Calculation](#time-savings-calculation)
6. [Examples: Good vs Bad Code Reuse](#examples-good-vs-bad-code-reuse)

---

## Core Principles

### 1. **Prefer Extend Over Create**

- **Default Assumption**: Existing code can be extended
- **Burden of Proof**: New implementation requires strong justification
- **Extension Methods**: Inheritance, composition, plugins, decorators, mixins
- **Validation**: Check Component Almanac before any new implementation

### 2. **Prefer Modify Over Replace**

- **Incremental Enhancement**: Add functionality to existing code when possible
- **Replacement Threshold**: Only when modification creates unacceptable technical debt
- **Risk Consideration**: Replacement carries migration and stability risks

### 3. **Mandatory Cleanup for Replacements**

- **Every Replacement**: Generates cleanup tasks (T9XX series)
- **Complete Removal**: Old code, tests, documentation, dependencies
- **Validation**: Cleanup tasks must be verified before feature completion

### 4. **Component Almanac as Source of Truth**

- **Always Check**: `docs/00-project/COMPONENT_ALMANAC.md` before planning
- **Living Document**: Update almanac when creating truly new components
- **Search First**: Use Grep/Glob to find similar functionality before building

---

## Build vs Extend vs Replace Decision Tree

```
┌─────────────────────────────────────┐
│ Need new functionality?             │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ Does Component Almanac have similar functionality?  │
└──────────────┬─────────────────┬────────────────────┘
               │                 │
           YES │                 │ NO
               ▼                 ▼
    ┌──────────────────┐  ┌────────────────────┐
    │ Can it be used   │  │ Search codebase    │
    │ as-is?           │  │ with Grep/Glob     │
    └────┬────────┬────┘  └─────┬──────────────┘
         │        │              │
     YES │        │ NO       Found similar?
         ▼        ▼              │
    ┌─────────┐  ┌─────────────────────────┐
    │ REUSE   │  │ Can it be extended?      │
    │ AS-IS   │  │ (inheritance/composition)│
    └─────────┘  └────┬───────────┬─────────┘
                      │           │
                  YES │           │ NO
                      ▼           ▼
              ┌────────────┐  ┌──────────────────────┐
              │ EXTEND     │  │ Extension creates    │
              │ EXISTING   │  │ unacceptable         │
              └────────────┘  │ coupling/debt?       │
                              └────┬────────┬────────┘
                                   │        │
                               YES │        │ NO → EXTEND anyway
                                   ▼        │
                          ┌──────────────────┐
                          │ REPLACE with     │
                          │ cleanup tasks    │
                          └──────────────────┘

If NO similar functionality found anywhere → BUILD NEW (rare case)
```

---

## Integration Pattern Library

### Pattern 1: Direct Reuse (No Modification)

**When**: Existing component meets all requirements
**Approach**:

```python
# Simply import and use
from packages.core.connectors.protocol import DataConnector
from packages.core.resilience import with_resilience

# Use existing functionality directly
connector = DataConnector()
result = await with_resilience(connector.fetch_data)()
```

**Time Saved**: 100% of build time

### Pattern 2: Extension via Inheritance

**When**: Need to add behavior while keeping base functionality
**Approach**:

```python
# Extend existing base class
from packages.core.connectors.base import BaseConnector

class EnhancedConnector(BaseConnector):
    """Extends BaseConnector with new capabilities."""

    async def fetch_with_retry(self, max_retries: int = 3):
        # New functionality builds on base
        return await super().fetch_data()
```

**Time Saved**: 60-80% of build time
**Cleanup**: None (additive change)

### Pattern 3: Extension via Composition

**When**: Need to combine multiple existing components
**Approach**:

```python
# Compose existing components
from packages.core.caching import CacheDecorator
from packages.core.connectors import HttpConnector

class ComposedService:
    def __init__(self):
        self.connector = HttpConnector()
        self.cache = CacheDecorator()

    async def get_data(self, key: str):
        # Leverage both existing components
        cached = await self.cache.get(key)
        if cached:
            return cached
        data = await self.connector.fetch(key)
        await self.cache.set(key, data)
        return data
```

**Time Saved**: 70-90% of build time
**Cleanup**: None (additive change)

### Pattern 4: Extension via Plugin/Decorator

**When**: Need to add cross-cutting concerns
**Approach**:

```python
# Use existing decorator pattern
from packages.core.observability import with_metrics

@with_metrics(operation="data_fetch")
async def fetch_data(source: str):
    # Your logic here, metrics added by decorator
    pass
```

**Time Saved**: 80-95% of build time
**Cleanup**: None (additive change)

### Pattern 5: Replacement with Migration

**When**: Existing component fundamentally incompatible
**Approach**:

```python
# Old component (to be removed)
# from packages.legacy.old_connector import OldConnector  # DELETE

# New component (replacement)
from packages.core.connectors import ModernConnector

# Migration helper (temporary)
def migrate_from_old_connector():
    """Migrate data from OldConnector to ModernConnector."""
    # Migration logic
    pass
```

**Time Saved**: 0-20% of build time (expensive)
**Cleanup Required**:

- Remove old component files
- Update all imports
- Update tests
- Remove old documentation
- Clean up dependencies

---

## Cleanup Task Prioritization

### Priority Assignment Matrix

| Scenario                                    | Priority | When to Execute       | Rationale                           |
| ------------------------------------------- | -------- | --------------------- | ----------------------------------- |
| **Replaced code blocks new functionality**  | P1       | Before implementation | Old code conflicts with new design  |
| **Security vulnerability in replaced code** | P1       | Immediately           | Risk to production                  |
| **Replaced code with active usage**         | P2       | During sprint         | Prevent confusion, reduce tech debt |
| **Deprecated but working code**             | P2       | This sprint           | Controlled removal with migration   |
| **Dead code with no dependencies**          | P3       | Backlog               | Low risk, low urgency               |
| **Documentation cleanup**                   | P3       | After code cleanup    | Verify code removed first           |

### Cleanup Task Template

```markdown
## T9XX: [Cleanup Task Name] [C]

**Priority**: P1/P2/P3
**Obsolete Component**: `path/to/old_component.py`
**Replacement**: `path/to/new_component.py`
**Estimated Effort**: X hours

### Cleanup Checklist

- [ ] Remove old component file: `old_component.py`
- [ ] Update imports in dependent files (use Grep to find)
- [ ] Remove tests for old component
- [ ] Update documentation references
- [ ] Remove unused dependencies from requirements
- [ ] Verify no runtime references remain
- [ ] Update Component Almanac

### Validation

- [ ] All tests pass after removal
- [ ] No import errors in codebase
- [ ] grep for old component name returns zero results
```

---

## Time Savings Calculation

### Formula Reference

**Reuse Savings** = (Hours to Build New) - (Hours to Integrate Existing)

**Extension Savings** = (Hours to Build New) - (Hours to Extend + Migration Hours)

**Replacement Savings** = (Maintenance Hours Saved Over Lifetime) - (Migration Hours + Cleanup Hours)

### Decision Threshold

- **Reuse/Extension must save >50% development hours** to justify new implementation
- If reuse/extension saves <50%, **must build new and add to Component Almanac**

### Example Calculation

**Scenario**: Need data caching functionality

| Approach             | Build Hours | Integration Hours | Extend Hours | Cleanup Hours | Total Hours | Time Saved    |
| -------------------- | ----------- | ----------------- | ------------ | ------------- | ----------- | ------------- |
| **Build New**        | 16          | 0                 | 0            | 0             | 16          | 0% (baseline) |
| **Reuse Existing**   | 0           | 2                 | 0            | 0             | 2           | **87.5%** ✅  |
| **Extend Existing**  | 0           | 0                 | 6            | 0             | 6           | **62.5%** ✅  |
| **Replace Existing** | 12          | 0                 | 0            | 8             | 20          | **-25%** ❌   |

**Decision**: Use existing cache decorator (87.5% time savings)

---

## Examples: Good vs Bad Code Reuse

### ✅ Good Example: Extending Resilience Patterns

**Requirement**: Add circuit breaker to existing retry logic

**Good Approach** (Extend):

```python
from packages.core.resilience import with_resilience, ResilienceConfig

# Extend existing resilience with circuit breaker
config = ResilienceConfig(
    max_retries=3,
    circuit_breaker_threshold=5,  # New parameter
    circuit_breaker_timeout=60
)

@with_resilience(config=config)
async def fetch_data():
    # Existing resilience + new circuit breaker
    pass
```

**Why Good**:

- Reuses proven resilience infrastructure
- Adds functionality via configuration
- No code duplication
- No cleanup needed
- Time savings: ~70%

**Bad Approach** (Build New):

```python
# DON'T DO THIS - Duplicates existing resilience
class MyCircuitBreaker:
    def __init__(self):
        self.retry_count = 0  # Already exists in with_resilience!
        self.failures = 0

    async def execute(self, func):
        for attempt in range(3):  # Duplicates retry logic!
            try:
                return await func()
            except Exception:
                self.failures += 1
                # ... reinventing the wheel
```

**Why Bad**:

- Duplicates existing retry logic
- Doesn't leverage proven patterns
- Creates maintenance burden
- No integration with existing observability
- Time wasted: ~16 hours

---

### ✅ Good Example: Replacing with Cleanup

**Requirement**: Replace legacy sync HTTP client with async version

**Good Approach** (Replace with Cleanup):

```python
# 1. Create new async connector (inheriting from BaseConnector)
from packages.core.connectors.base import BaseConnector

class AsyncHttpConnector(BaseConnector):
    async def fetch_data(self, url: str):
        # New async implementation
        pass

# 2. Create cleanup tasks in PLAN.md:
# - T901 [C P1]: Remove packages/legacy/sync_http.py
# - T902 [C P1]: Update 12 import statements
# - T903 [C P2]: Remove sync_http tests
# - T904 [C P3]: Update documentation
```

**Why Good**:

- Replacement is justified (sync → async architectural change)
- Comprehensive cleanup tasks generated
- Migration path clear
- Technical debt reduced
- Old code fully removed

**Bad Approach** (Replace without Cleanup):

```python
# Create new async connector
class AsyncHttpConnector:
    async def fetch_data(self, url: str):
        pass

# ... but leave old sync_http.py in codebase
# ... leave old tests
# ... leave old documentation
# ❌ Technical debt accumulates!
```

**Why Bad**:

- Old code creates confusion
- Maintenance burden doubled
- No clarity on which to use
- Tests conflict
- Documentation misleading

---

## Integration with Planning Workflow

### During Planning (/plan command)

1. **planning**: Checks Component Almanac, flags reuse opportunities
2. **architecture**: Populates "Existing Code Analysis" section
3. **architecture**: Scores code reuse effectiveness (15% weight)

### During Task Creation (/tasks command)

1. Parse "Technical Debt & Cleanup Tasks" section
2. Generate T9XX cleanup tasks
3. Generate T8XX tech debt investigation tasks
4. Order: P1 cleanup → implementation → P2/P3 cleanup

### During Implementation

1. **development agent**: Follows existing component patterns
2. **development agent**: Extracts reusable patterns to shared modules
3. **test-runner agent**: Validates cleanup (no old references)

---

## Quick Reference Checklist

**Before Planning**:

- [ ] Read Component Almanac
- [ ] Search codebase with Grep/Glob
- [ ] Identify reuse/extend/replace opportunities

**During Planning**:

- [ ] Complete "Existing Code Analysis" section
- [ ] Document extend vs create decision rationale
- [ ] Generate cleanup tasks for replacements
- [ ] Calculate time savings

**During Task Creation**:

- [ ] Create T9XX cleanup tasks from PLAN
- [ ] Create T8XX investigation tasks if needed
- [ ] Order cleanup before/after implementation correctly

**During Implementation**:

- [ ] Use existing patterns and components
- [ ] Execute cleanup tasks
- [ ] Verify no old code remains (grep check)
- [ ] Update Component Almanac if built new

---

**This framework ensures systematic code reuse, prevents duplication, and maintains a clean, maintainable codebase.**
