# Codebase Research Findings Template

**Use this template to report codebase research results**

---

## [Topic/Query]

**Research Type**: [ ] Needle Query  [ ] Open Investigation  [ ] Dependency Mapping

**Scope**: [files/modules searched]

---

## Executive Summary

[1-2 sentence summary of findings]

---

## Key Findings

### Finding 1: [Title]

**Location**: `path/to/file.py:line`

**Description**: [What was found]

**Code Reference**:
```python
# Relevant code snippet (signature + key logic only)
```

### Finding 2: [Title]

**Location**: `path/to/file.py:line`

**Description**: [What was found]

---

## File Map

| File | Purpose | Key Elements |
|------|---------|--------------|
| `path/to/file1.py` | [purpose] | `Class`, `function` |
| `path/to/file2.py` | [purpose] | `Class`, `function` |

---

## Dependency Graph

```
[Main Component]
├── imports → [Dependency 1]
├── imports → [Dependency 2]
└── used by → [Consumer 1]
```

---

## Patterns Identified

| Pattern | Location | Description |
|---------|----------|-------------|
| [Pattern Name] | `path/to/file.py` | [How it's used] |

---

## Gaps / Unknowns

- [ ] [Area that needs further investigation]
- [ ] [Missing information]

---

## Confidence Score

| Dimension | Weight | Score | Rationale |
|-----------|--------|-------|-----------|
| Domain | 0.4 | [0.0-1.0] | [Found relevant files?] |
| Pattern | 0.3 | [0.0-1.0] | [Understood patterns?] |
| Dependency | 0.2 | [0.0-1.0] | [Mapped relationships?] |
| Risk | 0.1 | [0.0-1.0] | [Identified edge cases?] |
| **CQ** | 1.0 | **[weighted avg]** | |

---

## Tool Usage Summary

| Tool | Calls | Files Processed |
|------|-------|-----------------|
| Glob | [n] | [patterns searched] |
| Grep | [n] | [patterns matched] |
| Read | [n] | [files read] |
| **Total** | **[n]** | |

---

## Escalation Recommendation

- [ ] **Sufficient** - CQ ≥ 0.85, proceed to decision
- [ ] **Escalate to library-research** - Need official API docs for [library]
- [ ] **Escalate to web-research** - Need community patterns for [topic]

---

## Next Steps

1. [Recommended action 1]
2. [Recommended action 2]
