# Frameworks: Architecture Enhancement Methodology

Detailed methodology documentation for architecture enhancement operations.

---

## Context7 MCP Integration

### Purpose
Access authoritative, version-specific library/framework documentation for architecture patterns and design principles.

### When to Use Context7
- Researching official framework design patterns (FastAPI architecture, Django app structure)
- Validating technology choices against official documentation
- Extracting architectural guidelines from framework documentation
- Version-specific architecture patterns (migration guides, breaking changes)

### Usage Pattern

```python
# 1. Resolve framework documentation
library_info = resolve_library_id("FastAPI")

# 2. Get architecture patterns documentation
docs = get_library_docs(
    library_info["library_id"],
    topic="project structure dependency injection architecture",
    tokens=8000  # Deep dive for comprehensive guidance
)

# 3. Extract and apply patterns
patterns = extract_architecture_patterns(docs)
```

### Token Optimization Strategies

| Strategy | Example | Impact |
|----------|---------|--------|
| Topic Specificity | "FastAPI auto_instrumentation setup" vs "FastAPI instrumentation" | 3k vs 15k+ tokens |
| Progressive Research | Multiple 2k queries vs single 8k dump | Better focus |
| Question-Driven | "how to handle timeout errors" vs "error handling" | Targeted results |


### Token Allocation Guide

| Depth | Tokens | Use Case |
|-------|--------|----------|
| Basic | 2,000 | Quick validation, simple patterns |
| Standard | 5,000 | Default research depth |
| Deep | 8,000 | Comprehensive architectural guidance |

### Research Areas
- **Architectural Patterns**: Proven patterns for system type and requirements
- **Technology Validation**: Compatibility and best practices
- **Implementation Patterns**: Code organization, project structure
- **Integration Patterns**: Service communication, API design
- **Security Patterns**: Authentication, authorization, data protection
- **Performance Patterns**: Scalability, caching, optimization

---

## Progressive Disclosure for Technical Content

### Three-Level Structure

**Level 1 (Always Visible)**:
- Architecture patterns and rationale
- Technology stack choices
- Integration points and dependencies
- High-level component design

**Level 2 (Progressive Disclosure)**:
- Detailed implementation steps
- Edge cases and error handling
- Performance optimization strategies
- Advanced configuration options

**External (Separate Files)**:
- Detailed API specifications
- Comprehensive schema definitions
- Complex architecture diagrams
- Technology-specific implementation guides


### Placeholder Replacement with Progressive Disclosure

**Before (Placeholder)**:
```markdown
## Technical Architecture
[Architecture Placeholder]
```

**After (Progressive Disclosure)**:
```markdown
## Technical Architecture (Essential - Level 1)

**Architecture Pattern**: Layered architecture with clean separation
- Presentation Layer: FastAPI REST endpoints
- Business Logic Layer: Pydantic AI agents with tool orchestration
- Data Layer: PostgreSQL with async SQLAlchemy

**Technology Stack**:
- **Language**: Python 3.13
- **Framework**: FastAPI (async), Pydantic AI
- **Storage**: PostgreSQL 16, Redis 7
- **Observability**: OpenTelemetry, Grafana, Prometheus

**Detailed Specifications**: See external references:
- API Documentation: `docs/05-reference/[feature]-api-spec.md`
- Data Models: `docs/05-reference/[feature]-schemas.md`

## Implementation Details (Progressive - Level 2)
[Detailed component designs move here]
```

### 500-Line Guideline
- Keep main PLAN.md technical sections concise
- If technical content >300 lines, externalize:
  - Detailed API specs → `docs/05-reference/[feature]-api.md`
  - Schemas → `docs/05-reference/[feature]-schemas.md`
  - Architecture diagrams → `docs/05-reference/[feature]-architecture.md`

---


## OODA Loop for Architecture Decisions

### Observe
- What placeholders exist in the plan?
- What Context7 research is needed?
- What existing components are in Component Almanac?

### Orient
- Best architecture patterns for this system type?
- Update beliefs based on Context7 research
- Identify reuse opportunities (extend vs replace vs create)

### Decide
- Select specific technologies with clear justification
- Choose architecture patterns with rationale
- Determine integration approach

### Act
- Populate plan sections with researched content
- Evaluate results against quality standards
- Iterate if placeholders remain

---

## Anti-Patterns for Technical Content

1. **Burying Architecture Decisions**
   - Do NOT hide technology choices in nested sections
   - Place architecture patterns and tech stack in Level 1

2. **Vague Technical Labels**
   - BAD: "System Component", "Technical Details"
   - GOOD: "Event Processing Pipeline (Redis Streams)", "REST API Layer (FastAPI)"

3. **Inline API Specifications**
   - BAD: 200+ lines of API endpoint definitions in PLAN.md
   - GOOD: API overview in plan + complete spec in `docs/05-reference/`

4. **Generic Placeholders Left Behind**
   - NEVER leave `[TBD]`, `[TODO]`, or `[Placeholder]`
   - ALWAYS replace with concrete, research-backed content
