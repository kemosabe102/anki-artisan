# Context7 Tool Patterns

**Purpose**: Tool-specific patterns for Context7 MCP integration

---

## Tool Overview

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `mcp__context7__resolve-library-id` | Match library name → Context7 ID | Always first (unless ID known) |
| `mcp__context7__get-library-docs` | Fetch documentation by topic | After resolving library ID |

---

## resolve-library-id Patterns

### Basic Resolution

```
Tool: mcp__context7__resolve-library-id
Parameter: libraryName = "Pydantic"

Response:
- library_id: "/pydantic/pydantic"
- trust_score: 9
- snippet_count: 542
```

### Quality Thresholds

| Metric | Threshold | Action |
|--------|-----------|--------|
| Trust Score ≥ 7 | Proceed | Use Context7 documentation |
| Trust Score < 7 | Escalate | Delegate to web-research |
| Snippet Count ≥ 100 | Adequate | Full topic coverage likely |
| Snippet Count < 100 | Sparse | May need supplementary research |

### Common Library IDs

| Library | Context7 ID | Trust | Snippets |
|---------|-------------|-------|----------|
| Pydantic | `/pydantic/pydantic` | 9 | 542 |
| FastAPI | `/tiangolo/fastapi` | 9 | 723 |
| SQLAlchemy | `/sqlalchemy/sqlalchemy` | 9 | 890 |
| pytest | `/pytest-dev/pytest` | 9 | 456 |
| Pandas | `/pandas-dev/pandas` | 9 | 1200+ |
| React | `/facebook/react` | 9 | 800+ |
| Next.js | `/vercel/next.js` | 9 | 650 |

### Skip Resolution When

- User provides exact `/org/project` format
- Library ID cached from previous call in session
- Using version-specific ID: `/vercel/next.js/v14.3.0`

---

## get-library-docs Patterns

### Parameter Reference

| Parameter | Type | Default | Purpose |
|-----------|------|---------|---------|
| `context7CompatibleLibraryID` | string | required | From resolve-library-id |
| `topic` | string | optional | Focus documentation (CRITICAL) |
| `mode` | enum | "code" | "code" for API, "info" for concepts |
| `page` | integer | 1 | Pagination (1-10) |

### Mode Selection

| Mode | Use When | Returns |
|------|----------|---------|
| `code` | Need API signatures, examples | Code snippets, function docs |
| `info` | Need concepts, architecture | Narrative guides, explanations |

**Default to `code`** - most research needs API references.

### Topic Formulation (CRITICAL for Token Efficiency)

**Principle**: Specific topics = smaller responses = faster research

| Specificity | Example Topic | Response Size |
|-------------|---------------|---------------|
| ❌ Vague | "validation" | ~30k tokens |
| ⚠️ Generic | "field validation" | ~15k tokens |
| ✅ Specific | "async field validators v2" | ~5k tokens |
| ✅ Precise | "field_validator decorator async" | ~3k tokens |

### Topic Patterns by Research Type

**API Lookup** (function/class reference):
```
topic = "{class_name} {method_name}"
topic = "{decorator_name} decorator usage"
topic = "{function_name} parameters"
```

**Pattern Research** (how to do X):
```
topic = "{concept} patterns examples"
topic = "async {operation} best practices"
topic = "{feature} configuration options"
```

**Error Resolution** (debugging):
```
topic = "{ErrorName} causes solutions"
topic = "{feature} troubleshooting"
topic = "{behavior} edge cases"
```

**Version-Specific**:
```
topic = "{feature} v2 migration"
topic = "{feature} breaking changes v1 v2"
topic = "{deprecated_feature} replacement"
```

---

## Pagination Strategy

### When to Paginate

| Scenario | Strategy |
|----------|----------|
| First query insufficient | Increment page, same topic |
| Need broader coverage | Broaden topic, page=1 |
| Exploring related topics | New topic, page=1 |

### Progressive Research Pattern

```
# Round 1: Quick validation (2k tokens equivalent)
get-library-docs(id, topic="specific feature", page=1)

# Round 2: If insufficient, same topic, next page
get-library-docs(id, topic="specific feature", page=2)

# Round 3: If still insufficient, broaden topic
get-library-docs(id, topic="feature category examples", page=1)
```

### Page Limits

- Maximum: `page=10`
- Typical sufficient: `page=1-3`
- If page=3 insufficient → broaden topic instead

---

## Multi-Library Comparison

### Pattern: Compare Two Libraries

```
# Step 1: Resolve both libraries
lib1_id = resolve-library-id("FastAPI")
lib2_id = resolve-library-id("Flask")

# Step 2: Query same topic from each
fastapi_docs = get-library-docs(lib1_id, topic="routing decorators")
flask_docs = get-library-docs(lib2_id, topic="routing decorators")

# Step 3: Synthesize comparison
```

### Comparison Topics

| Comparison Type | Topic Pattern |
|-----------------|---------------|
| API Style | "{feature} syntax examples" |
| Performance | "{operation} performance async" |
| Configuration | "{feature} configuration options" |
| Migration | "{lib1} to {lib2} migration" |

---

## Error Handling

### Common Issues

| Error | Cause | Resolution |
|-------|-------|------------|
| Library not found | Not in Context7 index | Escalate to web-research |
| Low snippet count | Sparse documentation | Supplement with web-research |
| Topic too broad | Generic topic | Narrow topic, add qualifiers |
| Empty response | Topic mismatch | Try alternative topic wording |

### Fallback Chain

```
1. Context7 (specific topic)
   ↓ if insufficient
2. Context7 (broader topic)
   ↓ if still insufficient  
3. Context7 (related topic)
   ↓ if library not indexed
4. Escalate to web-research
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| No topic parameter | Returns 30k+ tokens | Always specify topic |
| Re-resolving known IDs | Wastes API calls | Cache library IDs |
| Starting at page=5 | Misses relevant content | Start page=1, increment |
| "documentation" as topic | Too vague | Use specific feature name |
| Parallel library queries | May hit rate limits | Sequential queries |
