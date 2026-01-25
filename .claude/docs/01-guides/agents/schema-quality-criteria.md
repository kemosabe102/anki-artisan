---
title: "Schema Quality Evaluation Criteria"
date: 2025-11-18
status: ACTIVE
tags: [agents, schema, quality, validation]
---

# Schema Quality Evaluation Criteria

**Purpose**: Comprehensive criteria for evaluating agent output schema quality (JSON Schema, base-agent.schema.json extensions)

**Audience**: claude-code-ecosystem, claude-code-ecosystem, schema designers

**Scope**: Quality metrics for Claude Code agent schemas extending base-agent.schema.json

---

## Quick Reference

| **Criterion** | **Target** | **Validation** |
|---------------|------------|----------------|
| Documentation Completeness | 100% properties documented | Every field has 'description', objects have 'title' |
| Type Specificity | 100% explicit types | No 'any', all fields typed |
| Constraint Coverage | 90%+ constrained | Numerics have bounds, strings have lengths, enums used |
| Composition Clarity | allOf for extensions | Clear inheritance via base-agent.schema.json |
| Validation Accuracy | Conditional logic correct | if/then/else for status-dependent requirements |
| Error Reporting | Location tuples + messages | ValidationError provides precise paths |
| Security Compliance | No auto-decoding | No regex catastrophic backtracking |
| Reusability Factor | <20% duplication | Common patterns in base schema |
| Format Validation | Appropriate formats | date-time, URI, email use 'format' keyword |
| Evolution Support | Backward compatible | New fields optional, versioning strategy |
| Cross-Field Validation | Dependencies explicit | Model-level validators for field relationships |
| Serialization Consistency | model_dump() matches schema | Output structure matches expected format |
| Performance | <5 levels nesting | Avoid deep hierarchies |
| Interoperability | JSON Schema 2020-12 | Follows standard specification |

**Overall Score**: Sum of (criterion_pass × weight) → 0-100 scale

---

## 14 Evaluation Criteria

### 1. Documentation Completeness

**Definition**: Every schema property has clear, actionable documentation.

**Validation**:
- ✅ Every property has 'description' field (not empty)
- ✅ Complex objects have 'title' field for context
- ✅ Enums include explanation of each value
- ✅ Examples provided for non-obvious structures

**Scoring**:
- 100%: All properties documented with descriptions, titles, examples
- 75%: All properties have descriptions, missing some titles/examples
- 50%: 50-75% properties documented
- 25%: <50% properties documented
- 0%: No documentation

**Examples**:
```json
✅ GOOD:
{
  "confidence": {
    "type": "number",
    "description": "Agent's confidence in output quality (0.0-1.0 scale). <0.5 indicates uncertainty requiring escalation.",
    "minimum": 0.0,
    "maximum": 1.0,
    "examples": [0.85, 0.62, 0.91]
  }
}

❌ BAD:
{
  "confidence": {
    "type": "number"
  }
}
```

**Weight**: 15% (critical for maintainability)

---

### 2. Type Specificity

**Definition**: All fields have explicit, appropriate types (no 'any' or missing types).

**Validation**:
- ✅ Every property declares type (string, number, boolean, object, array, null)
- ✅ No 'any' or equivalent vague types
- ✅ Integers use "type": "integer" (not just "number")
- ✅ Nullable fields use oneOf with null type

**Scoring**:
- 100%: All properties have explicit, appropriate types
- 75%: 90%+ properties typed, minor gaps
- 50%: 75-90% properties typed
- 25%: <75% properties typed
- 0%: Widespread missing types or 'any' usage

**Examples**:
```json
✅ GOOD:
{
  "status": {
    "type": "string",
    "enum": ["SUCCESS", "FAILURE"]
  },
  "findings_count": {
    "type": "integer",
    "minimum": 0
  }
}

❌ BAD:
{
  "status": {},
  "findings_count": {
    "type": "number"  // Should be "integer"
  }
}
```

**Weight**: 12% (foundation for validation)

---

### 3. Constraint Coverage

**Definition**: Appropriate constraints applied (bounds, lengths, patterns, enums).

**Validation**:
- ✅ Numeric fields have minimum/maximum where applicable
- ✅ String fields have minLength/maxLength for bounded data
- ✅ Arrays have minItems/maxItems where appropriate
- ✅ Enums used for finite value sets (not open strings)
- ✅ Patterns (regex) for structured strings (UUIDs, emails)

**Scoring**:
- 100%: 95%+ applicable fields constrained
- 75%: 80-94% applicable fields constrained
- 50%: 60-79% constrained
- 25%: 40-59% constrained
- 0%: <40% constrained

**Examples**:
```json
✅ GOOD:
{
  "agent": {
    "type": "string",
    "minLength": 1,
    "maxLength": 50
  },
  "priority": {
    "type": "string",
    "enum": ["P1", "P2", "P3", "P4"]
  }
}

❌ BAD:
{
  "agent": {
    "type": "string"  // No length constraints
  },
  "priority": {
    "type": "string"  // Should be enum
  }
}
```

**Weight**: 10% (data quality enforcement)

---

### 4. Composition Clarity

**Definition**: Schema composition (allOf, anyOf, oneOf) used correctly with clear inheritance.

**Validation**:
- ✅ Extensions use allOf with base-agent.schema.json reference
- ✅ Polymorphic types use oneOf with discriminator
- ✅ No ambiguous composition (mixing allOf/anyOf incorrectly)
- ✅ Inheritance chain documented in comments

**Scoring**:
- 100%: Clear composition, correct usage, documented inheritance
- 75%: Composition correct but minimal documentation
- 50%: Some composition issues (ambiguous allOf/anyOf)
- 25%: Incorrect composition usage
- 0%: No composition or broken inheritance

**Examples**:
```json
✅ GOOD:
{
  "$schema": "http://json-schema.org/draft/2020-12/schema#",
  "title": "Researcher Library Output",
  "allOf": [
    {"$ref": ".claude/docs/schemas/base-agent.schema.json"},
    {
      "properties": {
        "agent_specific_output": {
          "type": "object",
          "properties": {
            "findings": {"type": "array"}
          }
        }
      }
    }
  ]
}

❌ BAD:
{
  // No base schema extension, duplicates base fields
  "properties": {
    "status": {"type": "string"},  // Should inherit from base
    "confidence": {"type": "number"}  // Should inherit from base
  }
}
```

**Weight**: 10% (maintainability, reusability)

---

### 5. Validation Accuracy

**Definition**: Conditional validation logic correctly implements state-dependent requirements.

**Validation**:
- ✅ if/then/else used for status-dependent fields (SUCCESS → agent_specific_output, FAILURE → failure_details)
- ✅ Conditional logic tested with valid/invalid examples
- ✅ No circular dependencies in conditions
- ✅ Edge cases handled (e.g., PARTIAL status)

**Scoring**:
- 100%: All conditional logic correct, edge cases handled
- 75%: Core logic correct, minor edge case gaps
- 50%: Some conditional logic issues
- 25%: Significant validation gaps
- 0%: No conditional validation or broken logic

**Examples**:
```json
✅ GOOD:
{
  "if": {
    "properties": {"status": {"const": "SUCCESS"}}
  },
  "then": {
    "required": ["agent_specific_output"]
  },
  "else": {
    "if": {"properties": {"status": {"const": "FAILURE"}}},
    "then": {"required": ["failure_details"]}
  }
}

❌ BAD:
{
  // No conditional validation - both SUCCESS and FAILURE could omit required fields
  "properties": {
    "status": {"enum": ["SUCCESS", "FAILURE"]}
  }
}
```

**Weight**: 10% (correctness critical)

---

### 6. Error Reporting Quality

**Definition**: Schema validation errors provide precise, actionable feedback.

**Validation**:
- ✅ Validation errors include field path (location tuples)
- ✅ Error messages are clear, actionable
- ✅ Custom error types used for domain-specific failures
- ✅ Context provided for constraint violations

**Scoring**:
- 100%: Precise location, clear messages, custom types, context
- 75%: Good location and messages, minimal custom types
- 50%: Basic error reporting, generic messages
- 25%: Vague errors, poor location info
- 0%: No structured error reporting

**Examples**:
```python
✅ GOOD:
@field_validator('confidence', mode='after')
@classmethod
def validate_confidence(cls, v: float) -> float:
    if not 0.0 <= v <= 1.0:
        raise ValueError(
            f'Confidence must be 0.0-1.0 scale (agent self-assessment). '
            f'Got {v}. Use 0.5 for uncertain, 0.85+ for high confidence.'
        )
    return v

# Error output: "agent_specific_output.confidence: Confidence must be 0.0-1.0 scale..."

❌ BAD:
# Generic validation with vague error
if v < 0 or v > 1:
    raise ValueError('Invalid value')

# Error output: "Invalid value" (no field path, no context)
```

**Weight**: 8% (debugging efficiency)

---

### 7. Security Compliance

**Definition**: Schema avoids security anti-patterns (auto-decoding, regex DoS, code injection).

**Validation**:
- ✅ No automatic content decoding (base64, base16)
- ✅ Regex patterns tested against catastrophic backtracking
- ✅ No code evaluation in validation logic
- ✅ Input sanitization for untrusted sources

**Scoring**:
- 100%: All security best practices followed
- 50%: Minor issues (inefficient regex)
- 0%: Critical vulnerabilities (auto-decode, code eval)

**Examples**:
```json
✅ GOOD:
{
  "file_path": {
    "type": "string",
    "pattern": "^[a-zA-Z0-9/_.-]+$",  // Simple, safe regex
    "description": "Path validation (no auto-decoding)"
  }
}

❌ BAD:
{
  "file_path": {
    "type": "string",
    "pattern": "(a+)+b",  // Catastrophic backtracking risk
    "contentEncoding": "base64"  // Auto-decodes untrusted input
  }
}
```

**Weight**: 10% (security critical)

---

### 8. Reusability Factor

**Definition**: Common patterns extracted to base schema, minimal duplication.

**Validation**:
- ✅ <20% field duplication across agent schemas
- ✅ Base schema contains common meta-flags (status, confidence, timestamps)
- ✅ Shared structures use $ref (not copy-paste)
- ✅ Agent-specific fields in agent_specific_output (not root)

**Scoring**:
- 100%: <10% duplication, excellent reuse
- 75%: 10-20% duplication, good reuse
- 50%: 20-40% duplication
- 25%: 40-60% duplication
- 0%: >60% duplication (copy-paste schema design)

**Weight**: 8% (maintainability)

---

### 9. Format Validation

**Definition**: Appropriate 'format' keywords used for structured strings.

**Validation**:
- ✅ Timestamps use "format": "date-time" (ISO 8601)
- ✅ URLs use "format": "uri"
- ✅ Emails use "format": "email"
- ✅ UUIDs use "format": "uuid"

**Scoring**:
- 100%: All applicable fields use format keywords
- 50%: 50-99% applicable fields
- 0%: <50% or missing critical formats

**Examples**:
```json
✅ GOOD:
{
  "execution_timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "ISO 8601 UTC timestamp"
  },
  "source_url": {
    "type": "string",
    "format": "uri"
  }
}

❌ BAD:
{
  "execution_timestamp": {
    "type": "string"  // No format validation
  }
}
```

**Weight**: 5%

---

### 10. Contract Evolution Support

**Definition**: Schema supports backward-compatible evolution.

**Validation**:
- ✅ New fields added as optional (not required)
- ✅ Versioning strategy documented ($schema or version field)
- ✅ Deprecated fields marked with description
- ✅ Breaking changes avoided or documented

**Scoring**:
- 100%: Clear versioning, backward compatible, deprecated fields marked
- 75%: Versioning present, mostly compatible
- 50%: Some evolution support
- 0%: No versioning, breaking changes

**Weight**: 6%

---

### 11. Cross-Field Validation

**Definition**: Field dependencies explicitly validated (model-level validators).

**Validation**:
- ✅ Dependent fields validated together (e.g., confidence + iteration_support)
- ✅ Model-level validators for complex constraints
- ✅ Mutually exclusive fields enforced
- ✅ Conditional requirements based on other fields

**Scoring**:
- 100%: All cross-field dependencies validated
- 75%: Most dependencies validated
- 50%: Some cross-field validation
- 0%: No cross-field validation

**Weight**: 6%

---

### 12. Serialization Consistency

**Definition**: Schema matches actual serialized output structure.

**Validation**:
- ✅ model_dump() output matches schema expectations
- ✅ No extra fields in output (additionalProperties: false or controlled)
- ✅ No missing required fields in practice
- ✅ Field names match (no alias mismatches)

**Scoring**:
- 100%: Perfect schema-output alignment
- 75%: Minor discrepancies (extra optional fields)
- 50%: Some structural mismatches
- 0%: Schema doesn't match output

**Weight**: 5%

---

### 13. Performance Consideration

**Definition**: Schema design avoids performance anti-patterns.

**Validation**:
- ✅ Nesting depth <5 levels (avoid deep hierarchies)
- ✅ Efficient validator types (after > wrap for most cases)
- ✅ No excessive regex complexity
- ✅ Lazy validation where appropriate

**Scoring**:
- 100%: All performance best practices
- 75%: Minor inefficiencies
- 50%: Some performance issues
- 0%: Significant performance problems

**Weight**: 3%

---

### 14. Interoperability

**Definition**: Schema follows JSON Schema 2020-12 or OpenAPI 3.x standards.

**Validation**:
- ✅ $schema declaration present (2020-12)
- ✅ Standard keywords used correctly
- ✅ No vendor-specific extensions (unless documented)
- ✅ Compatible with standard validators

**Scoring**:
- 100%: Full standard compliance
- 75%: Minor deviations (well-documented)
- 50%: Some non-standard usage
- 0%: Incompatible with standards

**Weight**: 2%

---

## Scoring Formula

```
schema_quality_score = sum(criterion_score × weight for all 14 criteria)

Grade:
A: 90-100 (Excellent)
B: 80-89 (Good)
C: 70-79 (Acceptable)
D: 60-69 (Needs Improvement)
F: <60 (Poor)
```

---

## Integration with Agent Analysis

**claude-code-ecosystem.md** should validate schemas against these 14 criteria during agent creation and review.

**claude-code-ecosystem.md** references this guide when evaluating schema quality as part of structural validation.

**See Also**:
- `.claude/docs/schemas/base-agent.schema.json` - Base schema all agents extend
- `.claude/docs/01-guides/agents/agent-standards-extended.md` - Two-state model requirements
- Pydantic documentation - Validation implementation patterns
- JSON Schema specification - Standard keywords and composition

---

**Version**: 1.0
**Source**: JSON Schema specification + Pydantic best practices + Worker 4 research findings
