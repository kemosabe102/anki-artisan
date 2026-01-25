# Context7 Integration Guide

## 3-Round Search Strategy

### Round 1 - Discovery (<3 seconds)

**Goal**: Resolve library and validate quality

**Tool**: `resolve-library-id`

**Process**:
1. Call `resolve-library-id("library-name")`
2. Check returned metadata: trust_score, snippet_count
3. Validate quality thresholds

**Quality Checks**:
- Primary: `trust_score >= 7 AND snippet_count >= 100`
- Exception: `trust_score >= 9 AND snippet_count >= 80` (highly authoritative sources)

**Termination**: quality_pass = false -> Return FAILURE immediately

**Example**:
```
resolve-library-id("Pydantic") 
-> "/pydantic/pydantic" (trust: 9, snippets: 542)
-> quality_pass = true
```

---

### Round 2 - Mapping (<8 seconds)

**Goal**: Retrieve focused documentation and extract patterns

**Tool**: `get-library-docs`

**Token Allocation** (progressive):
- 2000: Quick lookup (single API, simple question)
- 5000: Standard depth (topic exploration)
- 8000: Deep dive (complex patterns, multiple APIs)

**Topic Specificity**: Use 2-4 word phrases for focused results
- Good: "async validation", "model serialization", "field validators"
- Bad: "documentation", "everything", "how to use"

**Compression Target**: 15,000 tokens retrieved -> 1,000 tokens returned (15:1)

**Termination**: confidence >= 0.90 AND api_signatures.length > 0

**Example**:
```
get-library-docs("/pydantic/pydantic", topic="async validation", tokens=5000)
-> Extract: API signatures, patterns, 1-2 code examples
-> Compress: 15,000 -> 1,000 tokens
```

---

### Round 3 - Validation (<4 seconds)

**Conditions**: ONLY IF confidence < 0.90 OR version ambiguity detected

**Options**:
1. **Additional Context7 query** (8000 tokens) - deeper dive on specific sub-topic
2. **WebFetch supplement** - official library URL for gaps

**When to Use WebFetch**:
- Confidence 0.70-0.89 (partial coverage)
- Context7 missing specific version details
- Need cross-reference for accuracy

**Termination**: confidence >= 0.90 OR 3 rounds exhausted

---

## Tool Reference

### resolve-library-id

**Purpose**: Match library names to Context7-compatible IDs

**Input**: Library name string (e.g., "Pydantic", "FastAPI", "SQLAlchemy")

**Output**: Library metadata including:
- `library_id`: Context7-compatible path (e.g., "/pydantic/pydantic")
- `trust_score`: 0-10 quality indicator
- `snippet_count`: Number of code snippets available

**Quality Thresholds**:
```python
quality_pass = (
    (trust_score >= 7 AND snippet_count >= 100) OR
    (trust_score >= 9 AND snippet_count >= 80)
)
```

---

### get-library-docs

**Purpose**: Retrieve version-specific documentation with topic focusing

**Parameters**:
- `library_id`: From resolve-library-id (required)
- `topic`: 2-4 word focus phrase (recommended)
- `tokens`: Token budget (2000/5000/8000)

**Token Strategy**:
| Scenario | Tokens | Use Case |
|----------|--------|----------|
| Quick | 2000 | Single API lookup |
| Standard | 5000 | Topic exploration |
| Deep | 8000 | Complex patterns |

---

### WebFetch (Supplementary)

**Purpose**: Supplement Context7 when coverage gaps exist

**Authority Level**: 0.75 (supporting, not authoritative)

**When to Use**:
- Context7 confidence 0.70-0.89
- Version-specific details missing
- Cross-reference needed

**When NOT to Use**:
- As primary source (Context7 first)
- For community/unofficial content (delegate to researcher-web)

---

## Rate Limiting & Retry

**Detection**:
- HTTP 429 Too Many Requests
- MCP timeout >10 seconds
- MCP error indicating rate limit

**Retry Strategy**:
```
attempt_1: Execute immediately
attempt_2: Wait 2s + random(0-1s)
attempt_3: Wait 4s + random(0-2s)

max_retries = 2 (total 3 attempts)
```

**When NOT to Retry**:
- Library not found (permanent)
- Trust score below threshold (quality issue)
- Invalid library ID format (malformed request)

---

## Termination Rules

**Stop When ANY Condition is True**:

1. **Sufficient Findings**: `api_signatures.length > 0 AND confidence >= 0.90 AND code_examples.length >= 1`
2. **Quality Threshold Not Met**: `trust_score < 7 OR snippet_count < 100` -> FAILURE
3. **Library Not Found**: resolve-library-id returns no matches -> FAILURE
4. **Iteration Limit**: `context7_queries > 3` -> Diminishing returns

**"Good Enough" Criteria**:
- Good (0.90): Official docs + 2 examples + API signatures -> STOP
- Acceptable (0.80): Official docs + patterns (no examples) -> Continue if time permits
- Insufficient (<0.80): Missing key information -> Continue or populate iteration_support
