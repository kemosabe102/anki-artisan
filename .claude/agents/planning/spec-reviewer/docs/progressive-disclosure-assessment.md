# Progressive Disclosure Assessment for Specifications

**Purpose**: Evaluation checklist for SPEC.md progressive disclosure compliance

**Reference**: `docs/04-guides/documentation/progressive-disclosure-validation-framework.md`

---

## Evaluation Checklist

### 1. Essential Visibility

**Question**: Are core requirements (FR-IDs) visible in main overview?

| Check | Pass | Fail |
|-------|------|------|
| Core FR-XXX in Level 1 sections | Requirements visible without drilling | Buried in subsections |
| Success criteria in overview | Business goals upfront | Goals hidden in details |
| Frequently-referenced content | Easy to find | Requires navigation |

**Recommendation if Fail**: Move essential features to primary view

---

### 2. Hierarchical Structure

**Expected SPEC Structure**:

```
Level 0: Overview (Business case, problem statement)
Level 1: Core Requirements (FR-001 through FR-NNN) - ALWAYS VISIBLE
Level 2: Implementation Details (Component breakdowns)
Level 2: Advanced Topics (Edge cases, optimizations)
Level 2: References (External detailed specs)
```

| Check | Pass | Fail |
|-------|------|------|
| Overview first | Problem/solution upfront | Jumps to details |
| Core requirements prominent | FR-XXX in main body | Hidden or scattered |
| Details separated | Implementation in subsections | Mixed with requirements |

---

### 3. Document Size

| Metric | Target | Action |
|--------|--------|--------|
| Main SPEC.md | < 500 lines | PASS |
| Main SPEC.md | 500-800 lines | WARNING - consider extraction |
| Main SPEC.md | > 800 lines | FAIL - extract to reference docs |

**Extraction Target**: `docs/05-reference/[feature]-spec.md`

---

### 4. Information Scent

**Question**: Do headings provide clear navigation hints?

| Check | Pass | Fail |
|-------|------|------|
| Specific headings | "Authentication Flow Requirements" | "Advanced Features" |
| Preview hints | "This section covers X, Y, Z" | No context |
| Consistent labels | Same terms throughout | Terminology drift |

**Vague Labels to Flag**: "Miscellaneous", "Other", "Advanced", "Details", "Notes"

---

### 5. Depth Compliance

| Levels | Rating | Action |
|--------|--------|--------|
| 0-2 | PASS | Proper disclosure hierarchy |
| 3 | WARNING | Consider restructuring |
| 4+ | FAIL | Information architecture redesign needed |

**Recommendation if Fail**: Consolidate nested subsections or externalize to reference docs

---

## Report Template Section

Add to specification review reports:

```markdown
## Progressive Disclosure Compliance

**Score**: [X.XX] (Grade: [A/B/C/D/F])

| Dimension | Status | Notes |
|-----------|--------|-------|
| Essential Visibility | ✅/❌ | [Recommendation] |
| Hierarchical Structure | ✅/❌ | [Recommendation] |
| Document Size | [N] lines | Target: <500 |
| Information Scent | ✅/❌ | Vague labels: [list] |
| Depth Compliance | [N] levels | Max: 2 |

**Priority Recommendations**:
1. [Highest impact improvement]
2. [Secondary improvement]
3. [Tertiary improvement]
```

---

## Quick Reference

- [ ] Core requirements visible at Level 0-1?
- [ ] Proper Overview -> Requirements -> Details hierarchy?
- [ ] SPEC < 500 lines?
- [ ] Headings specific and descriptive?
- [ ] Maximum 2 disclosure levels?
