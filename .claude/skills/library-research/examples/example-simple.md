# Example: Simple Library Research

**Scenario**: "How do I use React's useState hook?"

---

## Request Analysis

- **Type**: API reference lookup
- **Library**: React
- **Scope**: Single hook documentation
- **Expected Tools**: resolve-library-id → get-library-docs

---

## Execution

### Step 1: Resolve library ID

```
Tool: mcp__context7__resolve-library-id
libraryName: "React"
```

**Result**:
```json
{
  "library_id": "/facebook/react",
  "trust_score": 9,
  "snippet_count": 823
}
```

**Assessment**: Trust 9 ≥ 7 ✓, Snippets 823 ≥ 100 ✓ → Proceed

### Step 2: Fetch hook documentation

```
Tool: mcp__context7__get-library-docs
context7CompatibleLibraryID: "/facebook/react"
topic: "useState hook usage examples"
mode: "code"
page: 1
```

**Result**: ~4k tokens of useState documentation including:
- Function signature
- Basic usage examples
- Update function behavior
- Lazy initialization
- Common patterns

---

## Findings Output

```markdown
## React useState Hook

**Library**: React (`/facebook/react`)
**Trust Score**: 9/10
**Documentation Source**: Official React docs

### API Signature

```typescript
const [state, setState] = useState<T>(initialState: T | (() => T)): [T, Dispatch<SetStateAction<T>>]
```

### Basic Usage

```jsx
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

### Key Behaviors

1. **Initial State**: Evaluated only on first render
2. **Lazy Initialization**: Pass function for expensive computation
3. **Batching**: Multiple setState calls batched in event handlers
4. **Identity**: setState with same value skips re-render (Object.is)

### Common Patterns

| Pattern | Example |
|---------|---------|
| Simple value | `useState(0)` |
| Object state | `useState({ name: '', age: 0 })` |
| Lazy init | `useState(() => expensiveComputation())` |
| Functional update | `setCount(prev => prev + 1)` |

**Confidence**: 0.95 (official documentation, comprehensive coverage)
```

---

## Tool Calls Summary

| Tool | Calls | Purpose |
|------|-------|---------|
| resolve-library-id | 1 | Get React library ID |
| get-library-docs | 1 | Fetch useState docs |
| **Total** | **2** | |

**Time**: ~8 seconds
