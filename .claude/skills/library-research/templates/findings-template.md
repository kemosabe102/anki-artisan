# Library Research Findings Template

**Use this template to report library research results**

---

## [Library Name] Research

**Library ID**: `/org/project`
**Trust Score**: X/10
**Snippet Count**: XXX
**Research Type**: [ ] API Lookup  [ ] Pattern Research  [ ] Comparison

---

## Executive Summary

[1-2 sentence summary of findings]

---

## Library Overview

| Attribute | Value |
|-----------|-------|
| Library | [name] |
| Context7 ID | [/org/project] |
| Version Researched | [version] |
| Trust Score | [X/10] |
| Documentation Quality | [Excellent/Good/Adequate] |

---

## API Reference

### [Function/Class Name]

**Signature**:
```python
def function_name(param1: Type1, param2: Type2 = default) -> ReturnType:
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `param1` | Type1 | Yes | [description] |
| `param2` | Type2 | No | [description] |

**Returns**: [description]

**Example**:
```python
# Usage example from official docs
result = function_name(value1, param2=value2)
```

---

## Usage Patterns

### Pattern 1: [Name]

**When to Use**: [scenario description]

```python
# Code example
```

### Pattern 2: [Name]

**When to Use**: [scenario description]

```python
# Code example
```

---

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| [option1] | [type] | [default] | [description] |
| [option2] | [type] | [default] | [description] |

---

## Version Considerations

| Version | Notes |
|---------|-------|
| v2.x | [current patterns] |
| v1.x | [deprecated patterns, migration notes] |

**Breaking Changes**: [list any relevant breaking changes]

---

## Integration Requirements

| Dependency | Version | Purpose |
|------------|---------|---------|
| [dep1] | [version] | [purpose] |
| [dep2] | [version] | [purpose] |

---

## Confidence Score

| Dimension | Weight | Score | Rationale |
|-----------|--------|-------|-----------|
| Domain | 0.4 | [0.0-1.0] | [Library indexed? Trust score?] |
| Pattern | 0.3 | [0.0-1.0] | [Patterns match use case?] |
| Dependency | 0.2 | [0.0-1.0] | [Version compatibility?] |
| Risk | 0.1 | [0.0-1.0] | [Deprecated? Security?] |
| **CQ** | 1.0 | **[weighted avg]** | |

---

## Tool Usage Summary

| Tool | Calls | Topics Queried |
|------|-------|----------------|
| resolve-library-id | [n] | [libraries resolved] |
| get-library-docs | [n] | [topics queried] |
| **Total** | **[n]** | |

---

## Source Citations

All findings from Context7 official documentation:
- Source: `/org/project` Context7 index
- Trust Score: X/10
- Last Updated: [if known]

---

## Escalation Recommendation

- [ ] **Sufficient** - CQ ≥ 0.85, official docs comprehensive
- [ ] **Escalate to web-research** - Need community patterns for [topic]
- [ ] **Escalate to codebase-research** - Need to check existing usage in project

---

## Next Steps

1. [Recommended action 1]
2. [Recommended action 2]
