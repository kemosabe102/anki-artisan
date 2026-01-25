# Intent Analyzer Domain Expertise

Detailed reference for intent decomposition, clarity scoring, and task graph construction.

---

## Intent Clarity Scoring Rubric

### Calculation Method
```
intent_clarity = (specificity × 0.4) + (completeness × 0.3) + (actionability × 0.2) + (unambiguity × 0.1)
```

### Component Scoring (0.0-1.0 scale)

#### 1. Specificity (0.4 weight)
How precise are the action verbs and targets?
- **1.0**: Exact action + file path ("implement AuthService in packages/core/auth/service.py")
- **0.7**: Clear action + component ("add JWT authentication to auth service")
- **0.4**: Vague action + broad target ("improve the auth system")
- **0.0**: No specific action or target ("make it better")

#### 2. Completeness (0.3 weight)
Are all necessary details provided?
- **1.0**: All context present (what, where, how, constraints)
- **0.7**: Most context present (what, where, partial how)
- **0.4**: Minimal context (what only, vague where)
- **0.0**: Missing critical context

#### 3. Actionability (0.2 weight)
Can work begin immediately?
- **1.0**: Ready to execute (no clarification needed)
- **0.7**: Minor assumptions needed (reasonable defaults available)
- **0.4**: Significant assumptions required (multiple interpretations)
- **0.0**: Cannot proceed (multiple unknowns)

#### 4. Unambiguity (0.1 weight)
Is there only one interpretation?
- **1.0**: Single clear interpretation
- **0.7**: Primary interpretation obvious (minor alternatives)
- **0.4**: Multiple equally valid interpretations
- **0.0**: Completely ambiguous

### Threshold Rules
- **intent_clarity ≥ 0.7**: Proceed with analysis (sufficient clarity)
- **intent_clarity < 0.7**: Return FAILURE with clarification questions

### Example Calculations

**High Clarity Request**:
```
"Implement AuthService in packages/core/auth/service.py using JWT tokens"
- Specificity: 0.9 (exact file path + clear technology)
- Completeness: 0.8 (what + where + how, missing constraints)
- Actionability: 0.9 (ready to execute)
- Unambiguity: 1.0 (single interpretation)
- intent_clarity = (0.9×0.4) + (0.8×0.3) + (0.9×0.2) + (1.0×0.1) = 0.88 ✅ PROCEED
```

**Low Clarity Request**:
```
"Update the auth system"
- Specificity: 0.3 (vague action, broad target)
- Completeness: 0.2 (what only, no where/how)
- Actionability: 0.1 (cannot proceed without clarification)
- Unambiguity: 0.2 (fix? enhance? refactor?)
- intent_clarity = (0.3×0.4) + (0.2×0.3) + (0.1×0.2) + (0.2×0.1) = 0.22 ❌ CLARIFY
```

---

## Compression & Output Optimization

### Compression Principle
Transform verbose natural language requests into structured machine-readable task graphs.

**Target Compression Ratio**: 3:1-4:1 (input context tokens / output structure tokens)

### Example Compression

**INPUT (~44 tokens)**:
```
"I need to implement a new authentication service using JWT tokens. It should integrate
with the existing user database and provide login/logout endpoints. Make sure to add
comprehensive tests and update the API documentation. Also research best practices
for JWT security before implementing."
```

**OUTPUT (structured ~12 core action tokens)**:
```json
{
  "intents": [
    {"action": "research", "target": "JWT security best practices", "order": 1},
    {"action": "implement", "target": "AuthService with JWT", "order": 2, "depends_on": [1]},
    {"action": "test", "target": "AuthService", "order": 3, "depends_on": [2], "implicit": true},
    {"action": "document", "target": "API endpoints", "order": 4, "depends_on": [2], "implicit": true}
  ],
  "domain_scope": "packages/core/auth/",
  "entity_count": 3,
  "parallel_tasks": [],
  "sequential_tasks": [1, 2, 3, 4]
}

Compression Ratio: 44 input tokens / 12 core action tokens = 3.7:1 ✅
```

### Token Efficiency Techniques
- Use structured JSON over prose
- Eliminate redundant explanations
- Reference domain patterns by ID
- Compress dependencies into graph notation

---

## Action Verb Taxonomy

### Primary Categories
| Category | Verbs | Domain Scope |
|----------|-------|--------------|
| Implementation | implement, create, add, build | packages/**, .claude/** |
| Modification | update, fix, change, refactor | packages/**, tests/** |
| Analysis | research, analyze, explain, investigate | external, docs/** |
| Validation | test, review, verify, check | tests/**, packages/** |
| Documentation | document, write, describe | docs/** |

### Implicit Requirement Patterns
| Explicit Action | Implicit Requirement | Rationale |
|----------------|---------------------|-----------|
| implement | test | >80% coverage requirement per CLAUDE.md |
| API change | document | API docs must reflect current state |
| feature | test + document | Standard feature completeness |
| refactor | test | Verify behavior unchanged |

---

## Task Graph Construction

### Node Types
- **Explicit**: Directly stated in user request
- **Implicit**: Inferred from domain patterns
- **Blocking**: Must complete before dependents

### Edge Types
| Type | Description | Example |
|------|-------------|---------|
| sequential | Must complete in order | research → implement |
| parallel | Can execute simultaneously | test ∥ document |
| data_flow | Output feeds input | analyze → implement |
| hard | Strict dependency | N/A without completion |
| soft | Preferred but not required | docs before deploy |

### DAG Validation
Task graphs MUST be acyclic (directed acyclic graph). Circular dependencies indicate analysis error.

**Validation Steps**:
1. Topological sort attempt
2. If cycle detected → analysis error
3. If valid → determine parallel groups and critical path
