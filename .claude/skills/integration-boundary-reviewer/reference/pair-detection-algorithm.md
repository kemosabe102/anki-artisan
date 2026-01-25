# Pair Detection Algorithm

**Purpose**: Identify integration pairs from a feature using data flow adjacency.

---

## Overview

Integration pairs are identified by analyzing where data flows from one component to another. A pair consists of:
- **Upstream**: Component that produces output
- **Downstream**: Component that consumes that output

---

## Detection Sources (Weighted)

| Source | Weight | Description |
|--------|--------|-------------|
| Documentation | 0.40 | Explicit data flow diagrams in ARCHITECTURE.md |
| Import Graph | 0.25 | Actual code import dependencies |
| Type Annotations | 0.20 | Output/input type matching |
| Task Dependencies | 0.15 | Sequential task relationships |

### Confidence Formula
```
pair_confidence = (doc_evidence × 0.40) + (import_evidence × 0.25) 
                + (type_evidence × 0.20) + (task_evidence × 0.15)
```

---

## Source 1: Documentation Analysis (0.40)

### What to Parse
- `ARCHITECTURE.md` - Primary source
- `PLAN.md` - Phase dependencies
- `README.md` - Component descriptions

### Pattern Recognition
```
# ASCII flow diagrams
Provider → Normalizer → Deduplicator

# Mermaid diagrams
graph LR
    A[Provider] --> B[Normalizer]
    B --> C[Deduplicator]

# Bullet lists
- Data flows from Provider to Normalizer
- Normalizer output feeds Deduplicator
```

### Scoring
- Explicit arrow notation: 1.0
- Described in text: 0.7
- Implied by section order: 0.4

---

## Source 2: Import Graph Analysis (0.25)

### Discovery Commands
```bash
# Find cross-package imports
Grep "from packages\." --type py {feature_dir}

# Build import map
Grep "from packages\.attention import" --type py packages/
Grep "from packages\.news_sentiment import" --type py packages/
```

### What Indicates Integration
- Cross-package imports (different top-level packages)
- Import of data models/schemas from another module
- Import of service/provider classes

### Scoring
- Direct import of class/function: 1.0
- Import of types only: 0.6
- No import relationship: 0.0

---

## Source 3: Type Annotation Inference (0.20)

### Contract Matching
```python
# Upstream output
class Provider:
    def fetch(self) -> list[RawDocument]:
        ...

# Downstream input  
class Normalizer:
    def process(self, docs: list[RawDocument]) -> list[CleanDocument]:
        ...
```

When `Provider.fetch()` returns `list[RawDocument]` and `Normalizer.process()` accepts `list[RawDocument]`, this indicates integration.

### Discovery Commands
```bash
# Find return types
Grep "def.*\).*->.*:" --type py {upstream_file}

# Find parameter types
Grep "def.*\(.*:.*\):" --type py {downstream_file}
```

### Scoring
- Exact type match: 1.0
- Compatible types (subclass, Protocol): 0.8
- Same base type: 0.5
- No type info available: 0.0

---

## Source 4: Task Dependencies (0.15)

### TASKS.md Patterns
```markdown
- T001: Implement Provider (packages/news_sentiment/providers/)
- T002: Implement Normalizer (packages/attention/processing/) [depends: T001]
```

### TASKS.json Structure
```json
{
  "tasks": [
    {"id": "T001", "component": "Provider", "dependencies": []},
    {"id": "T002", "component": "Normalizer", "dependencies": ["T001"]}
  ]
}
```

### Scoring
- Explicit `depends` relationship: 1.0
- Sequential task order: 0.5
- Same phase, different components: 0.3

---

## Pair Ordering

Pairs are ordered by:
1. **Data flow sequence** - Earlier in pipeline comes first
2. **Confidence score** - Higher confidence pairs first (within same sequence position)
3. **Criticality** - More critical integrations (auth, data persistence) first

---

## Filtering

### Include Pairs When
- Confidence ≥ 0.50
- Both components exist in codebase
- Data flow direction is determinable

### Exclude Pairs When
- Confidence < 0.50
- Components are in same file (not integration)
- Relationship is purely type-only (no runtime data flow)

---

## Output Format

```json
{
  "id": 1,
  "upstream": "PerplexityProvider",
  "downstream": "Normalizer",
  "upstream_file": "packages/news_sentiment/providers/perplexity_provider.py",
  "downstream_file": "packages/attention/processing/normalizer.py",
  "data_flow_type": "direct",
  "confidence": 0.92,
  "evidence": [
    "ARCHITECTURE.md line 45: 'Provider → Normalizer'",
    "normalizer.py:12: 'from packages.news_sentiment.providers import PerplexityProvider'"
  ]
}
```

### Data Flow Types
- `direct`: Synchronous function call
- `event`: Async event/message passing
- `storage`: Via database/file persistence
- `api`: Via HTTP/REST interface
