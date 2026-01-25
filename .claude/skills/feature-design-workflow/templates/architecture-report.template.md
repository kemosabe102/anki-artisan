# Architecture & Design Report

> **Feature**: [Feature Name]
> **Author**: [Name]
> **Date**: [YYYY-MM-DD]
> **Status**: Draft | Review | Approved
> **Prerequisite**: Problem Statement & Requirements Report

---

## 1. Architecture Overview

**High-Level Summary**:
[2-3 sentences describing the architectural approach and key design decisions]

```
[ASCII architecture diagram showing major components and data flow]

     +-----------+      +-----------+      +-----------+
     | Component |----->| Component |----->| Component |
     |     A     |      |     B     |      |     C     |
     +-----------+      +-----------+      +-----------+
           |                  |
           v                  v
     +-----------+      +-----------+
     | Storage   |      | External  |
     +-----------+      +-----------+
```

---

## 2. Sub-Problems Breakdown

```
Top-Level Problem: [Main problem statement]
│
├─ Sub-Problem 1: [Name]
│  ├─ [Sub-task 1.1]
│  ├─ [Sub-task 1.2]
│  └─ [Sub-task 1.3]
│
├─ Sub-Problem 2: [Name]
│  ├─ [Sub-task 2.1]
│  └─ [Sub-task 2.2]
│
└─ Sub-Problem 3: [Name]
   ├─ [Sub-task 3.1]
   └─ [Sub-task 3.2]
```

---

## 3. Approach Evaluation Matrix

### Sub-Problem 1: [Name]

| Approach | Implementation | Pros | Cons | Recommended |
|----------|---------------|------|------|-------------|
| Option A | [How] | [Benefits] | [Drawbacks] | [ ] |
| Option B | [How] | [Benefits] | [Drawbacks] | [x] |
| Option C | [How] | [Benefits] | [Drawbacks] | [ ] |

**Decision**: [Selected approach] because [rationale]

### Sub-Problem 2: [Name]

| Approach | Implementation | Pros | Cons | Recommended |
|----------|---------------|------|------|-------------|
| Option A | [How] | [Benefits] | [Drawbacks] | [x] |
| Option B | [How] | [Benefits] | [Drawbacks] | [ ] |

**Decision**: [Selected approach] because [rationale]


---

## 4. Selected Design Patterns

| Pattern | Purpose | Benefit | Trade-off |
|---------|---------|---------|-----------|
| [e.g., Strategy] | [Why used] | [Value added] | [Cost/complexity] |
| [e.g., Circuit Breaker] | [Why used] | [Value added] | [Cost/complexity] |
| [e.g., Repository] | [Why used] | [Value added] | [Cost/complexity] |

---

## 5. Data Structures & Interfaces

### Core Data Classes
```python
@dataclass
class [EntityName]:
    field_1: type  # Description
    field_2: type  # Description
```

### Interfaces/Contracts
```python
class [InterfaceName](ABC):
    @abstractmethod
    def method_name(self, param: Type) -> ReturnType:
        """Description of contract"""
        pass
```


---

## 6. Architecture Decision Record (ADR)

### ADR-001: [Decision Title]

| Field | Value |
|-------|-------|
| **Status** | Proposed / Accepted / Deprecated |
| **Context** | [Why this decision is needed] |
| **Decision** | [What was decided] |
| **Rationale** | [Why this option was chosen] |
| **Alternatives** | [What else was considered] |
| **Consequences** | (+) [Benefit 1], (+) [Benefit 2], (-) [Trade-off 1] |

---

## 7. Implementation Roadmap

| Phase | Tasks | Dependencies | Estimate |
|-------|-------|--------------|----------|
| 1. Foundation | [Schema, data classes] | None | [X days] |
| 2. Core Logic | [Main implementation] | Phase 1 | [X days] |
| 3. Integration | [External services] | Phase 2 | [X days] |
| 4. Observability | [Logging, metrics] | Phase 2 | [X days] |
| 5. Testing | [Full test suite] | Phase 3 | [X days] |

---

**Phase 2 Checklist**:
- [ ] Problem decomposed into independent sub-problems
- [ ] 2-3 approaches evaluated per sub-problem
- [ ] Pros/cons documented for each approach
- [ ] Design patterns identified with trade-offs
- [ ] Data classes and interfaces defined
- [ ] Implementation sequenced by dependency
- [ ] Effort estimated per phase
