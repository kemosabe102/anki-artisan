# Example: Complex Library Research

**Scenario**: "Compare FastAPI and Flask routing approaches for our new API"

---

## Request Analysis

- **Type**: Multi-library comparison
- **Libraries**: FastAPI, Flask
- **Scope**: Routing patterns, decorators, parameters
- **Expected Tools**: Multiple resolve + get-library-docs calls

---

## Execution

### Phase 1: Resolve Libraries

**Step 1.1: Resolve FastAPI**

```
Tool: mcp__context7__resolve-library-id
libraryName: "FastAPI"
```

**Result**:
```json
{
  "library_id": "/tiangolo/fastapi",
  "trust_score": 9,
  "snippet_count": 723
}
```

**Step 1.2: Resolve Flask**

```
Tool: mcp__context7__resolve-library-id
libraryName: "Flask"
```

**Result**:
```json
{
  "library_id": "/pallets/flask",
  "trust_score": 9,
  "snippet_count": 456
}
```

**Assessment**: Both libraries have trust ≥ 7, adequate snippets → Proceed

### Phase 2: Gather Routing Documentation

**Step 2.1: FastAPI routing patterns**

```
Tool: mcp__context7__get-library-docs
context7CompatibleLibraryID: "/tiangolo/fastapi"
topic: "routing path decorators parameters"
mode: "code"
```

**Key Findings**:
- Decorator-based routing (`@app.get`, `@app.post`)
- Automatic request validation via type hints
- Path parameters with type conversion
- Query parameters with defaults
- Dependency injection system

**Step 2.2: Flask routing patterns**

```
Tool: mcp__context7__get-library-docs
context7CompatibleLibraryID: "/pallets/flask"
topic: "routing decorators url parameters"
mode: "code"
```

**Key Findings**:
- Decorator-based routing (`@app.route`)
- Manual request parsing via `request` object
- Path converters (`<int:id>`, `<string:name>`)
- No built-in validation
- Blueprint system for modularization

### Phase 3: Deep Dive on Differences

**Step 3.1: FastAPI async support**

```
Tool: mcp__context7__get-library-docs
context7CompatibleLibraryID: "/tiangolo/fastapi"
topic: "async await endpoints concurrency"
mode: "info"
```

**Step 3.2: Flask async support** (page 2 for more detail)

```
Tool: mcp__context7__get-library-docs
context7CompatibleLibraryID: "/pallets/flask"
topic: "async views flask 2.0"
mode: "info"
page: 1
```

---

## Findings Output

```markdown
## FastAPI vs Flask Routing Comparison

### Overview

| Aspect | FastAPI | Flask |
|--------|---------|-------|
| Routing Style | Type-annotated decorators | Traditional decorators |
| Validation | Automatic (Pydantic) | Manual |
| Async Support | Native | Flask 2.0+ (limited) |
| Documentation | Auto-generated OpenAPI | Manual |

### Routing Syntax Comparison

**FastAPI**:
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: int, include_email: bool = False):
    # user_id automatically validated as int
    # include_email is optional query parameter
    return {"user_id": user_id}
```

**Flask**:
```python
from flask import Flask, request

app = Flask(__name__)

@app.route("/users/<int:user_id>")
def get_user(user_id):
    include_email = request.args.get("include_email", False, type=bool)
    # Manual parameter extraction
    return {"user_id": user_id}
```

### Key Differences

| Feature | FastAPI | Flask |
|---------|---------|-------|
| Type validation | Automatic via type hints | Manual via converters |
| Query params | Function parameters | `request.args.get()` |
| Request body | Pydantic models | `request.json` |
| Response model | Type hints + models | Dict or Response |
| Async handlers | `async def` native | `async def` (Flask 2.0+) |
| OpenAPI docs | Automatic `/docs` | Requires flask-apispec |

### Recommendation Matrix

| Use Case | Recommendation | Rationale |
|----------|----------------|-----------|
| New API, type safety priority | FastAPI | Native validation, OpenAPI |
| Existing Flask codebase | Flask | Migration cost |
| High concurrency needs | FastAPI | Native async, better perf |
| Simple prototype | Flask | Less boilerplate |
| Team knows Flask | Flask | Learning curve |

### Confidence Scores

| Dimension | FastAPI | Flask | Rationale |
|-----------|---------|-------|-----------|
| Domain | 0.95 | 0.95 | Both well-documented |
| Pattern | 0.90 | 0.90 | Clear routing patterns |
| Dependency | 0.85 | 0.85 | Understood requirements |
| Risk | 0.80 | 0.85 | FastAPI newer, Flask mature |
| **CQ** | **0.90** | **0.90** | |
```

---

## Tool Calls Summary

| Tool | Calls | Purpose |
|------|-------|---------|
| resolve-library-id | 2 | FastAPI, Flask IDs |
| get-library-docs | 4 | Routing + async for each |
| **Total** | **6** | |

**Time**: ~25 seconds

---

## Escalation Check

- **Codebase research needed?** Yes, if checking existing patterns in project
- **Web research needed?** Only for production deployment comparisons
- **CQ ≥ 0.85?** Yes for both → Ready for decision
