# SOLID Principles Validation Checklist

> Validate design quality using the 5 core object-oriented design principles.

---

## Overview

SOLID is an acronym for five design principles that promote maintainable, extensible software:

| Principle | Full Name | Core Question |
|-----------|-----------|---------------|
| **S** | Single Responsibility | One reason to change? |
| **O** | Open/Closed | Extend without modify? |
| **L** | Liskov Substitution | Subclasses substitutable? |
| **I** | Interface Segregation | Focused interfaces? |
| **D** | Dependency Inversion | Depend on abstractions? |

---

## Single Responsibility Principle (SRP)

> "A class should have only one reason to change."

### Assessment Questions

1. Does each class/module have a single, well-defined purpose?
2. Can you describe the responsibility in one sentence without "and"?
3. Would a change in one area require changes in unrelated areas?
4. Are there classes doing formatting AND calculation AND persistence?
5. Is there clear separation between business logic and infrastructure?


### Scoring Rubric

| Score | Criteria |
|-------|----------|
| 5 | All classes have single responsibility, clear boundaries |
| 4 | Most classes well-focused, minor violations |
| 3 | Some classes have multiple responsibilities |
| 2 | Many classes with blurred responsibilities |
| 1 | No clear separation of concerns |

### Evidence Requirements

- Class/module size metrics (LOC, method count)
- Cohesion analysis (LCOM metrics)
- Change coupling analysis (files changed together)

### Common Violations

- God classes with 1000+ lines
- Service classes doing validation, persistence, and notification
- Controllers containing business logic

---

## Open/Closed Principle (OCP)

> "Software entities should be open for extension but closed for modification."

### Assessment Questions

1. Can new features be added without modifying existing code?
2. Are there strategy/plugin patterns for varying behavior?
3. Do you need to edit switch statements to add new cases?
4. Is behavior configured via composition rather than inheritance?
5. Are extension points clearly defined?


### Scoring Rubric

| Score | Criteria |
|-------|----------|
| 5 | Clear extension points, behavior via composition |
| 4 | Most variation handled via extension |
| 3 | Mix of extension and modification patterns |
| 2 | New features require significant code changes |
| 1 | Every change requires modifying core classes |

### Evidence Requirements

- Presence of strategy/factory patterns
- Plugin architecture documentation
- Change history showing extension vs modification

### Common Violations

- Giant switch/if-else chains for type handling
- Hardcoded behavior instead of configurable strategies
- No abstraction layers for varying implementations

---

## Liskov Substitution Principle (LSP)

> "Subtypes must be substitutable for their base types."

### Assessment Questions

1. Can derived classes be used wherever base class is expected?
2. Do subclasses honor base class contracts (pre/post conditions)?
3. Are there subclasses that throw "not implemented" exceptions?
4. Do subclasses strengthen preconditions or weaken postconditions?
5. Is inheritance used for code reuse rather than substitutability?


### Scoring Rubric

| Score | Criteria |
|-------|----------|
| 5 | All subclasses fully substitutable, contracts honored |
| 4 | Minor edge cases, well-documented |
| 3 | Some violations, workarounds in place |
| 2 | Inheritance hierarchy causes runtime errors |
| 1 | Widespread substitution failures |

### Evidence Requirements

- Type hierarchy analysis
- Contract documentation (pre/post conditions)
- Runtime exception patterns in subclasses

### Common Violations

- Square extending Rectangle (classic example)
- NotImplementedException in subclass methods
- Type checking before method calls (instanceof)

---

## Interface Segregation Principle (ISP)

> "Clients should not be forced to depend on interfaces they do not use."

### Assessment Questions

1. Are interfaces focused on specific client needs?
2. Do implementing classes have unused interface methods?
3. Are there "fat" interfaces with 10+ methods?
4. Can interfaces be split into smaller, cohesive units?
5. Do clients depend only on methods they actually use?


### Scoring Rubric

| Score | Criteria |
|-------|----------|
| 5 | Small, focused interfaces tailored to clients |
| 4 | Most interfaces well-scoped |
| 3 | Some fat interfaces, but functional |
| 2 | Interfaces force unnecessary dependencies |
| 1 | Monolithic interfaces throughout |

### Evidence Requirements

- Interface method counts
- Unused method implementations
- Client dependency analysis

### Common Violations

- IRepository with 20 methods when clients need 3
- Forcing implementers to stub unused methods
- One interface for all service operations

---

## Dependency Inversion Principle (DIP)

> "Depend on abstractions, not concretions."

### Assessment Questions

1. Do high-level modules depend on abstractions?
2. Are concrete implementations injected rather than instantiated?
3. Is there a dependency injection container/framework?
4. Can implementations be swapped without changing callers?
5. Are external dependencies (DB, API) behind interfaces?


### Scoring Rubric

| Score | Criteria |
|-------|----------|
| 5 | Full DI, all externals abstracted |
| 4 | DI used, most dependencies injectable |
| 3 | Partial DI, some hard dependencies |
| 2 | Minimal abstraction, tight coupling |
| 1 | Direct instantiation throughout |

### Evidence Requirements

- DI container configuration
- Interface definitions for external services
- Constructor injection patterns

### Common Violations

- `new ConcreteClass()` inside business logic
- Static method calls to infrastructure
- No interfaces for repositories/services

---

## Stage Application

### MVP Stage (SRP + DIP Only)

Focus on foundational principles:

| Principle | Required | Minimum Score |
|-----------|----------|---------------|
| SRP | Yes | 3.0 |
| OCP | No | - |
| LSP | No | - |
| ISP | No | - |
| DIP | Yes | 3.0 |

**Rationale**: Speed is priority; ensure basic structure for future extension.


### Alpha+ Stage (Full 5 Principles)

All principles required:

| Principle | Required | Minimum Score |
|-----------|----------|---------------|
| SRP | Yes | 3.5 |
| OCP | Yes | 3.5 |
| LSP | Yes | 3.5 |
| ISP | Yes | 3.5 |
| DIP | Yes | 3.5 |

### Beta/RC/GA Progression

| Stage | Minimum Average | Any Single Principle Min |
|-------|-----------------|-------------------------|
| Beta | 4.0 | 3.5 |
| RC | 4.2 | 4.0 |
| GA | 4.5 | 4.0 |

---

## Aggregate Scoring

### Formula

```
SOLID_Score = (SRP + OCP + LSP + ISP + DIP) / 5
```

### MVP Formula (Reduced Scope)

```
SOLID_Score_MVP = (SRP + DIP) / 2
```


---

## Assessment Template

```markdown
## SOLID Principles Assessment

**Project**: [name]
**Date**: [date]
**Stage**: [MVP/Alpha/Beta/RC/GA]

### Principle Scores

| Principle | Score | Confidence | Key Findings |
|-----------|-------|------------|--------------|
| SRP | X/5 | HIGH/MED/LOW | [notes] |
| OCP | X/5 | HIGH/MED/LOW | [notes] |
| LSP | X/5 | HIGH/MED/LOW | [notes] |
| ISP | X/5 | HIGH/MED/LOW | [notes] |
| DIP | X/5 | HIGH/MED/LOW | [notes] |

### Aggregate Score: X.X/5

### Stage Readiness: [PASS/WARN/FAIL]

### Top Violations
1. [violation 1 with location]
2. [violation 2 with location]
3. [violation 3 with location]

### Recommendations
1. [priority 1]
2. [priority 2]
3. [priority 3]
```
