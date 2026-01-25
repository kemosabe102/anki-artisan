---
title: "Golden Agent & Schema Standards"
date: 2025-11-08
status: ACTIVE
tags: [agents, claude-docs]
---
# Golden Agent & Schema Standards

**Purpose**: Reference standards for creating and validating agents and schemas in the Claude Code ecosystem.

**Last Updated**: 2025-10-19
**Template Version**: 5.0 - Anthropic Research Integration Edition

---

## Overview

This guide provides concrete examples of excellent agent and schema design based on actual implementations that have been validated and scored highly. Use these as references when creating new agents or schemas, or when reviewing existing ones for quality improvements.

**Golden Examples**:

- **Agent**: `researcher-codebase.md` (94/100) - Comprehensive worker pattern with inline schema examples
- **Schema**: `feature-analyzer.schema.json` (96/100) - Perfect base extension with nested output structure

---

## Golden Agent: researcher-codebase.md

**File**: `.claude/agents/researcher-codebase.md`
**Score**: 94/100
**Use As Template For**: Agent structure, inline schema examples, base pattern extension, tool usage patterns

### Why This Is Golden

1. **Perfect Header Structure** (Lines 1-8)
   - YAML frontmatter only
   - `**Extends**: base-agent-pattern.md` declared inline (line 4)
   - No extra `---` separators
   - Tools as comma-separated string (line 7)

2. **Inline Schema Examples** (Lines 32-158)
   - Shows actual JSON structures in agent markdown
   - Developers can understand output without reading schema file separately
   - Both SUCCESS and FAILURE examples provided with realistic field values

3. **Base Pattern Extension** (Lines 176-204)
   - Explicitly lists inherited vs specialized capabilities
   - Documents token savings (~1,150 tokens)
   - No duplication of base pattern sections
   - Clear separation of agent-specific vs inherited capabilities

4. **Concrete Tool Patterns** (Lines 429-469)
   - Every tool has actionable examples with expected outcomes
   - Shows progressive narrowing strategy (broad → narrow → precise → deep)
   - Explains when to use each tool pattern

### Key Sections to Emulate

#### 1. Perfect YAML Frontmatter (Lines 1-8)

```yaml
---
name: researcher-codebase
description: Codebase research worker performing deep code analysis, architecture investigation, and implementation pattern discovery with intelligent compression for researcher-lead.
**Extends**: base-agent-pattern.md
model: opus
color: cyan
tools: Read, Glob, Grep, mcp__context7__resolve-library-id, mcp__context7__get-library-docs
---
```

**Why This Works**:

- ✅ Single YAML block (lines 1-8)
- ✅ Tools as comma-separated string (NOT YAML list)
- ✅ Inline base pattern extension declaration (`**Extends**: base-agent-pattern.md`)
- ✅ Descriptive name with domain prefix (`researcher-codebase`)
- ✅ Clear, focused description (one sentence explaining role)

#### 2. Inline Schema Examples (Lines 32-88)

```json
{
  "findings": {
    "key_insights": [
      {
        "insight": "Key finding about codebase",
        "confidence": 0.9,
        "evidence": "src/module/file.py:123",
        "sources": ["file1.py", "file2.py"]
      }
    ],
    "patterns_discovered": [
      {
        "pattern": "Pattern name",
        "instances": 12,
        "example": "src/example.py:45",
        "description": "What the pattern does"
      }
    ],
    "architecture": {
      "structure": "3-tier: API → Service → Repository",
      "key_files": ["main.py", "service.py"],
      "dependencies": ["dep1", "dep2"]
    }
  },
  "compression_stats": {
    "files_analyzed": 45,
    "lines_reviewed": 12000,
    "findings_returned": 20,
    "compression_ratio": "600:1"
  }
}
```

**Why This Works**:

- ✅ Realistic example values (not `"string"` or `123`)
- ✅ Shows nested structure clearly
- ✅ Explains what each field contains
- ✅ Developers can understand output format without reading schema file

#### 3. Base Pattern Extension Declaration (Lines 176-204)

```markdown
## Base Agent Pattern Extension

**This agent EXTENDS**: `.claude/docs/guides/base-agent-pattern.md`

**Specialized Focus**: Codebase research with intelligent compression and pattern discovery

**Agent-Specific Capabilities**:

- Three-phase search strategy (Discovery → Mapping → Validation)
- Progressive narrowing (Broad → Narrow → Precise → Deep)
- Intelligent compression (10:1 minimum ratio)
- Pattern-based synthesis (not exhaustive listing)
- Termination rules ("good enough" philosophy)

**Inherited from Base Pattern**:

- Knowledge Base Integration (context gathering hierarchy)
- Pre-Flight Checklist (comprehensive task assessment)
- Core Workflow Structure (6-phase lifecycle)
- Error Recovery Patterns (retry logic, graceful degradation)
- Parallel Execution Awareness (when to parallelize/serialize)
- Validation Checklist (lifecycle, core requirements, quality assurance)

**Token Savings**: Using base pattern reduces this agent by ~1,150 tokens through inheritance
```

**Why This Works**:

- ✅ Clear separation of specialized vs inherited capabilities
- ✅ Quantified token savings (motivates using pattern)
- ✅ No duplication of base pattern sections
- ✅ Developers know what's unique to this agent vs what's inherited

#### 4. Concrete Tool Usage Patterns (Lines 429-469)

```markdown
### Finding Definitions

# Class definition

Grep("^class ClassName", output_mode="content", -n=true)

# Function definition

Grep("^def function_name", output_mode="content", -n=true)

### Finding Usage

# Word boundary (precise)

Grep("\\bClassName\\b", output_mode="files_with_matches")

# With context

Grep("ClassName", output_mode="content", -A=2, -B=2, head_limit=5)

# Count references

Grep("ClassName", output_mode="count")

### Progressive Narrowing

1. Broad: `Glob("**/*.py")` + `Grep(pattern, head_limit=20)`
2. Narrow: `Grep(pattern, type="py", glob="src/**")`
3. Precise: `Grep("\\bpattern\\b", output_mode="content", -n=true)`
4. Deep: `Read(top 3-5 files)`
```

**Why This Works**:

- ✅ Every tool pattern has actionable example with expected outcome
- ✅ Shows parameter usage (output_mode, -n, -A/-B, head_limit)
- ✅ Explains progression strategy (broad → narrow → precise → deep)
- ✅ Developers can copy-paste and adapt patterns

#### 5. Iteration Support Structure (Lines 102-130)

```json
"iteration_support": {
  "open_questions": [
    {
      "question": "How does the authentication middleware handle token refresh in distributed deployments?",
      "context": "Found token validation logic but refresh mechanism unclear in multi-instance scenarios",
      "priority": "high",
      "suggested_approach": "researcher-external for distributed auth best practices and framework-specific docs (auto-routes)"
    }
  ],
  "confidence_breakdown": {
    "overall_confidence": 0.78,
    "confidence_factors": {
      "code_coverage": 0.70,
      "pattern_clarity": 0.85,
      "documentation_quality": 0.60
    },
    "low_confidence_rationale": [
      "Authentication code spread across 12 files with inconsistent patterns",
      "Token refresh logic only partially implemented in 4 of 12 files",
      "No inline documentation explaining distributed deployment strategy"
    ],
    "confidence_improvement_actions": [
      "Search for auth middleware tests to understand expected behavior",
      "Research framework-specific distributed auth patterns",
      "Review deployment configuration for multi-instance auth setup"
    ]
  }
}
```

**Why This Works**:

- ✅ Specific questions with context (not vague "need more info")
- ✅ Priority-based triage (high, medium, low)
- ✅ Suggested approach guides orchestrator on next steps
- ✅ Quantified confidence breakdown (code_coverage, pattern_clarity, documentation_quality)
- ✅ Actionable improvement actions (not just "investigate more")

---

## Golden Schema: feature-analyzer.schema.json

**File**: `.claude/docs/schemas/feature-analyzer.schema.json`
**Score**: 96/100
**Use As Template For**: Base extension, nested output structure, failure details, field descriptions

### Why This Is Golden

1. **Perfect Base Extension** (Lines 1-8)
   - Uses `"extends": "base-agent.schema.json"` with `allOf` pattern
   - Proper `oneOf [Success, Failure]` structure
   - All meta-flags inherited correctly

2. **Comprehensive agent_specific_output** (Lines 62-292)
   - Nested objects with clear hierarchy
   - `comparison_matrix`, `separation_report`, `integration_architecture`, `alignment_assessment`, `recommended_action`
   - Every level has required fields specification

3. **Complete failure_details** (Lines 317-372)
   - `failure_type` enum with specific values
   - `reasons` array with actionable descriptions
   - `recovery_suggestions` for orchestrator with effort estimates
   - `partial_results`, `research_attempted`, `next_steps`

4. **Excellent Field Descriptions** (Throughout)
   - Every field has description with examples
   - Proper enum constraints for status fields
   - Validation rules (minimum, maximum) where appropriate

### Key Patterns to Emulate

#### 1. Perfect Base Extension Pattern (Lines 1-39)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Feature Analyzer Agent Schema",
  "description": "Schema for feature-analyzer agent analyzing feature specifications for overlaps, conflicts, and integration strategies",
  "version": "1.0.0",
  "type": "object",
  "extends": "base-agent.schema.json",
  "properties": {
    "input": {
      "type": "object",
      "description": "Input for feature analysis operation",
      "properties": {
        "context": {
          "type": "string",
          "description": "Analysis context and instructions"
        },
        "feature_paths": {
          "type": "array",
          "items": { "type": "string" },
          "minItems": 2,
          "description": "Array of 2+ paths to feature specifications in docs/01-planning/specifications/**"
        },
        "execution_timestamp": {
          "type": "string",
          "format": "date-time",
          "description": "ISO 8601 UTC timestamp from orchestrator (mandatory)"
        }
      },
      "required": ["context", "feature_paths", "execution_timestamp"]
    },
    "output": {
      "type": "object",
      "oneOf": [
        {
          "title": "Success Output",
          "properties": {
            "status": { "const": "SUCCESS" },
            "agent": { "const": "feature-analyzer" }
            // ... agent_specific_output
          }
        },
        {
          "title": "Failure Output",
          "properties": {
            "status": { "const": "FAILURE" },
            "agent": { "const": "feature-analyzer" }
            // ... failure_details
          }
        }
      ]
    }
  }
}
```

**Why This Works**:

- ✅ Clear `extends` declaration at top level
- ✅ `oneOf [Success, Failure]` two-state model
- ✅ Input validation with required fields and type constraints
- ✅ Execution timestamp mandatory from orchestrator
- ✅ Agent-specific const for agent name

#### 2. Nested Output Structure with Clear Hierarchy (Lines 62-292)

```json
"agent_specific_output": {
  "type": "object",
  "properties": {
    "comparison_matrix": {
      "type": "object",
      "description": "Feature comparison with overlap analysis",
      "properties": {
        "features": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": { "type": "string" },
              "core_responsibility": { "type": "string" },
              "entities": {
                "type": "array",
                "items": { "type": "string" }
              },
              "workflows": {
                "type": "array",
                "items": { "type": "string" }
              }
            },
            "required": ["name", "core_responsibility", "entities", "workflows"]
          }
        },
        "overlap_analysis": {
          "type": "object",
          "properties": {
            "responsibility_overlap_pct": {
              "type": "number",
              "minimum": 0,
              "maximum": 100
            },
            "conflict": { "type": "boolean" },
            "synergy": { "type": "boolean" },
            "synergy_type": {
              "type": "string",
              "enum": ["foundational_application", "competing_alternatives", "complementary_layers", "independent_modules", "none"]
            }
          },
          "required": ["responsibility_overlap_pct", "conflict", "synergy"]
        }
      },
      "required": ["features", "overlap_analysis"]
    },
    "separation_report": {
      // ... nested structure
    },
    "integration_architecture": {
      // ... nested structure
    }
  },
  "required": ["comparison_matrix", "separation_report", "integration_architecture"]
}
```

**Why This Works**:

- ✅ Clear nesting hierarchy (3-4 levels deep)
- ✅ Required fields at each level
- ✅ Validation rules (minimum, maximum, enum)
- ✅ Every object has description explaining purpose
- ✅ Array items have structured schemas (not just `type: "string"`)

#### 3. Comprehensive Failure Details (Lines 317-372)

```json
"failure_details": {
  "type": "object",
  "properties": {
    "failure_type": {
      "type": "string",
      "enum": ["missing_context", "file_access_error", "circular_dependency", "validation_error", "insufficient_data"]
    },
    "reasons": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Specific reasons why analysis failed"
    },
    "recovery_suggestions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "suggestion": { "type": "string" },
          "effort_estimate": { "type": "string" },
          "confidence": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          }
        },
        "required": ["suggestion", "effort_estimate", "confidence"]
      }
    },
    "partial_results": {
      "type": "object",
      "description": "Work completed before failure",
      "properties": {
        "comparison_matrix": {
          "type": "object",
          "properties": {
            "features_loaded": { "type": "number" },
            "responsibility_mapping": { "type": "string" },
            "overlap_detection": { "type": "string" }
          }
        }
      }
    },
    "research_attempted": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Read/Grep operations performed, patterns investigated"
    },
    "next_steps": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Actionable recommendations for orchestrator"
    }
  },
  "required": ["failure_type", "reasons", "recovery_suggestions", "next_steps"]
}
```

**Why This Works**:

- ✅ Specific failure_type enum (not generic "error")
- ✅ Recovery suggestions with effort estimates and confidence
- ✅ Partial results capture work before failure
- ✅ Research attempted shows what was tried
- ✅ Next steps guide orchestrator on recovery path

#### 4. Actionable Field Descriptions (Throughout)

```json
"comparison_scope": {
  "type": "string",
  "enum": ["full", "quick"],
  "default": "full",
  "description": "Analysis depth: full (7-phase methodology) or quick (responsibility mapping + overlap detection only)"
}

"feature_paths": {
  "type": "array",
  "items": { "type": "string" },
  "minItems": 2,
  "description": "Array of 2+ paths to feature specifications in docs/01-planning/specifications/**"
}

"confidence": {
  "type": "number",
  "minimum": 0,
  "maximum": 1,
  "description": "Confidence in integration recommendation"
}
```

**Why This Works**:

- ✅ Description explains what value means (not just field name)
- ✅ Includes examples of valid values
- ✅ Explains validation rules (minItems, minimum, maximum)
- ✅ Shows what different enum values mean
- ✅ Developers can understand schema without reading agent file

---

## Validation Checklist

Use this checklist when creating new agents or schemas to ensure they meet golden standards:

### Agent Checklist

**Header & Structure**:

- [ ] File starts with YAML frontmatter (`---...---`) on line 1 (no warning headers)
- [ ] No extra `---` separators beyond frontmatter
- [ ] Tools field is comma-separated string (NOT YAML list): `tools: Read, Write, Edit`
- [ ] Color is one of: purple, blue, green, yellow, red
- [ ] Description is 1-2 sentences max (focused and clear)

**Base Pattern Extension**:

- [ ] Includes "Base Agent Pattern Extension" section
- [ ] Lists specialized capabilities (agent-specific only)
- [ ] Lists inherited capabilities (from base-agent-pattern.md)
- [ ] Documents token savings (~1,150 tokens)
- [ ] No duplication of base pattern sections

**Schema Integration**:

- [ ] Schema Reference section points to `.claude/docs/schemas/[agent-name].schema.json`
- [ ] Inline examples of agent_specific_output (SUCCESS case)
- [ ] Inline examples of failure_details (FAILURE case)
- [ ] Examples use realistic values (not placeholders)

**Tool Usage Patterns**:

- [ ] Every tool has concrete usage examples
- [ ] Examples show parameter usage (output_mode, -n, head_limit, etc.)
- [ ] Explains when to use each pattern
- [ ] Shows progressive strategies (broad → narrow → precise)

**Section Ordering**:

- [ ] YAML frontmatter (line 1)
- [ ] Role & Boundaries
- [ ] Schema Reference
- [ ] Permissions
- [ ] File Operation Protocol
- [ ] Base Agent Pattern Extension
- [ ] Primary Responsibilities
- [ ] Workflow Operations
- [ ] Tool Usage Patterns
- [ ] Error Recovery Patterns
- [ ] Integration Points
- [ ] Quality Standards
- [ ] Validation Checklist

### Schema Checklist

**Base Extension**:

- [ ] File exists at `.claude/docs/schemas/[agent-name].schema.json`
- [ ] Uses `"extends": "base-agent.schema.json"` with `allOf` pattern
- [ ] Includes `oneOf [Success, Failure]` structure
- [ ] Agent name matches: `"agent": { "const": "agent-name" }`

**Input Structure**:

- [ ] Input object with description
- [ ] Required fields array includes: `context`, `execution_timestamp`
- [ ] Type validation for all input fields
- [ ] Descriptions explain format and examples

**Success Output (agent_specific_output)**:

- [ ] Nested structure with clear hierarchy
- [ ] Required fields specified at each level
- [ ] Every field has actionable description
- [ ] Enum constraints for status/type fields
- [ ] Validation rules (minimum, maximum, minItems) where appropriate

**Failure Output (failure_details)**:

- [ ] `failure_type` enum with specific values (not generic)
- [ ] `reasons` array with specific failure reasons
- [ ] `recovery_suggestions` with effort estimates and confidence
- [ ] `partial_results` captures work before failure
- [ ] `research_attempted` shows what was tried
- [ ] `next_steps` provides actionable orchestrator guidance

**Field Quality**:

- [ ] Every field has description (no missing descriptions)
- [ ] Descriptions explain what value means (not just repeat field name)
- [ ] Enum values have explanation of differences
- [ ] Examples included in descriptions where helpful
- [ ] Type constraints appropriate for field purpose

---

## Common Anti-Patterns to Avoid

Learn from these common mistakes and follow the correct patterns instead:

### ❌ Wrong: Extra --- Separators

**Problem**: Multiple `---` blocks break YAML parsing

```yaml
---
name: agent-name
description: Agent description
---

--- # ← WRONG: Extra separator after frontmatter

# Role & Boundaries
```

**Impact**: Claude Code fails to parse frontmatter, agent won't load properly

### ✅ Right: Single YAML Block

```yaml
---
name: agent-name
description: Agent description
tools: Read, Write, Edit
---
# Role & Boundaries  # ← Immediately after frontmatter (no extra ---)
```

---

### ❌ Wrong: Tools as YAML List

**Problem**: YAML list format breaks sub-agent tool access

```yaml
tools: [Read, Write, Edit] # ← WRONG: YAML list syntax
```

or

```yaml
tools: # ← WRONG: YAML multi-line list
  - Read
  - Write
  - Edit
```

**Impact**: Sub-agents can't access tools properly, delegation fails

### ✅ Right: Tools as Comma-Separated String

```yaml
tools: Read, Write, Edit # ← CORRECT: Comma-separated string
```

or for long tool lists:

```yaml
tools: Read, Write, Edit, Glob, Grep, WebFetch, mcp__context7__resolve-library-id # ← CORRECT
```

---

### ❌ Wrong: Duplicating Base Pattern Sections

**Problem**: Copies entire sections from base-agent-pattern.md (adds ~1,150 tokens)

```markdown
## Knowledge Base Integration

**Pre-Work Assessment**:

- Review orchestrator context for task requirements...
  [990 tokens duplicated from base-agent-pattern.md]

## Pre-Flight Checklist

**Comprehensive Task Assessment**:

1. Schema Loading...
   [430 tokens duplicated from base-agent-pattern.md]
```

**Impact**:

- Wastes ~1,150 tokens per agent
- Creates maintenance burden (must update all agents when base pattern changes)
- Makes agent harder to read (buries unique capabilities)

### ✅ Right: Referencing Base Pattern

```markdown
## Base Agent Pattern Extension

**This agent EXTENDS**: `.claude/docs/guides/base-agent-pattern.md`

**Specialized Focus**: Codebase research with intelligent compression and pattern discovery

**Agent-Specific Capabilities**:

- Three-phase search strategy (Discovery → Mapping → Validation)
- Progressive narrowing (Broad → Narrow → Precise → Deep)
- Intelligent compression (10:1 minimum ratio)

**Inherited from Base Pattern**:

- Knowledge Base Integration (context gathering hierarchy)
- Pre-Flight Checklist (comprehensive task assessment)
- Core Workflow Structure (6-phase lifecycle)
- Error Recovery Patterns (retry logic, graceful degradation)

**Token Savings**: Using base pattern reduces this agent by ~1,150 tokens through inheritance
```

**Benefits**:

- Saves ~1,150 tokens per agent
- Single source of truth for common patterns
- Highlights unique capabilities
- Easier maintenance

---

### ❌ Wrong: Generic Schema Descriptions

**Problem**: Descriptions repeat field name without explaining value

```json
{
  "confidence": {
    "type": "number",
    "description": "The confidence" // ← WRONG: Doesn't explain what this means
  },
  "status": {
    "type": "string",
    "description": "Status of the operation" // ← WRONG: Too vague
  },
  "features": {
    "type": "array",
    "description": "Array of features" // ← WRONG: Doesn't explain structure
  }
}
```

**Impact**: Developers must read agent file to understand schema, slows development

### ✅ Right: Actionable Schema Descriptions

```json
{
  "confidence": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "description": "Confidence in integration recommendation (0.0-1.0). >0.85 = high confidence, 0.70-0.85 = moderate, <0.70 = low"
  },
  "status": {
    "type": "string",
    "enum": ["SUCCESS", "FAILURE"],
    "description": "Operation result: SUCCESS with agent_specific_output populated, or FAILURE with failure_details populated"
  },
  "features": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "core_responsibility": { "type": "string" }
      }
    },
    "description": "Array of 2+ feature objects with name and core_responsibility extracted from SPEC.md files"
  }
}
```

**Benefits**:

- Developers understand schema without reading agent file
- Clear validation rules and expected formats
- Examples and ranges for numeric fields
- Enum values explained

---

### ❌ Wrong: Vague Failure Details

**Problem**: Generic failure information doesn't help orchestrator recover

```json
{
  "failure_details": {
    "failure_type": "error", // ← WRONG: Too generic
    "reasons": ["Something went wrong"], // ← WRONG: Not actionable
    "recovery_suggestions": ["Try again"] // ← WRONG: No guidance
  }
}
```

**Impact**: Orchestrator can't make informed recovery decisions, must escalate to human

### ✅ Right: Specific Failure Details with Recovery Guidance

```json
{
  "failure_details": {
    "failure_type": "file_access_error", // ← CORRECT: Specific failure type
    "reasons": [
      "docs/01-planning/specifications/feature-001/SPEC.md not found",
      "docs/01-planning/specifications/feature-002/SPEC.md exists but empty"
    ],
    "recovery_suggestions": [
      {
        "suggestion": "Verify feature paths exist: run Glob('docs/01-planning/specifications/**/SPEC.md')",
        "effort_estimate": "30 seconds",
        "confidence": 0.95
      },
      {
        "suggestion": "Check for typos in feature directory names or missing SPEC.md files",
        "effort_estimate": "1 minute",
        "confidence": 0.85
      }
    ],
    "partial_results": {
      "comparison_matrix": {
        "features_loaded": 1, // ← Shows what succeeded before failure
        "responsibility_mapping": "Feature 001 loaded successfully",
        "overlap_detection": "N/A - only 1 feature loaded"
      }
    },
    "research_attempted": [
      "Read('docs/01-planning/specifications/feature-001/SPEC.md') - SUCCESS",
      "Read('docs/01-planning/specifications/feature-002/SPEC.md') - FAILURE: file not found"
    ],
    "next_steps": [
      "Verify file paths with orchestrator",
      "Re-run analysis with corrected paths",
      "Consider using feature-path validation before delegation"
    ]
  }
}
```

**Benefits**:

- Orchestrator knows exactly what failed
- Recovery suggestions have effort estimates (cost-aware decision)
- Partial results show what succeeded (can resume)
- Research attempted shows debugging path
- Next steps provide actionable guidance

---

### ❌ Wrong: Missing Required Fields in Schema

**Problem**: Schema doesn't specify required fields at nested levels

```json
{
  "comparison_matrix": {
    "type": "object",
    "properties": {
      "features": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "name": { "type": "string" },
            "core_responsibility": { "type": "string" },
            "entities": { "type": "array" }
          }
          // ← WRONG: Missing "required" array
        }
      },
      "overlap_analysis": {
        "type": "object",
        "properties": {
          "responsibility_overlap_pct": { "type": "number" },
          "conflict": { "type": "boolean" }
        }
        // ← WRONG: Missing "required" array
      }
    }
    // ← WRONG: Missing "required" array at top level
  }
}
```

**Impact**: Validation can't catch missing fields, agents can return incomplete outputs

### ✅ Right: Required Fields at All Levels

```json
{
  "comparison_matrix": {
    "type": "object",
    "properties": {
      "features": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "name": { "type": "string" },
            "core_responsibility": { "type": "string" },
            "entities": { "type": "array" }
          },
          "required": ["name", "core_responsibility", "entities"] // ← CORRECT
        }
      },
      "overlap_analysis": {
        "type": "object",
        "properties": {
          "responsibility_overlap_pct": { "type": "number" },
          "conflict": { "type": "boolean" }
        },
        "required": ["responsibility_overlap_pct", "conflict"] // ← CORRECT
      }
    },
    "required": ["features", "overlap_analysis"] // ← CORRECT
  }
}
```

**Benefits**:

- Validation catches incomplete outputs
- Clear contract for agent developers
- Prevents partial/broken responses

---

## Quick Reference: Golden Patterns

### Agent Header Pattern

```yaml
---
name: descriptive-agent-name  # Use domain prefix (researcher-, feature-, etc.)
description: One sentence describing agent purpose and capabilities
**Extends**: base-agent-pattern.md  # Include if using base pattern
model: opus  # opus (recommended) | sonnet | haiku | inherit
color: purple  # Visual identifier
tools: Read, Write, Edit, Glob, Grep  # Comma-separated string (NOT YAML list)
---
```

### Inline Schema Example Pattern

````markdown
### agent_specific_output (SUCCESS)

```json
{
  "findings": {
    "key_insights": [
      {
        "insight": "Realistic example value",
        "confidence": 0.9,
        "evidence": "src/file.py:123"
      }
    ],
    "compression_stats": {
      "files_analyzed": 45,
      "compression_ratio": "600:1"
    }
  }
}
```
````

### Base Pattern Extension Pattern

```markdown
## Base Agent Pattern Extension

**This agent EXTENDS**: `.claude/docs/guides/base-agent-pattern.md`

**Specialized Focus**: [Agent's unique capability]

**Agent-Specific Capabilities**:

- [Unique capability 1]
- [Unique capability 2]

**Inherited from Base Pattern**:

- Knowledge Base Integration
- Pre-Flight Checklist
- Core Workflow Structure
- Error Recovery Patterns

**Token Savings**: Using base pattern reduces this agent by ~1,150 tokens through inheritance
```

### Tool Pattern Example

```markdown
### Finding Definitions

# Class definition

Grep("^class ClassName", output_mode="content", -n=true)

### Finding Usage

# Word boundary (precise)

Grep("\\bClassName\\b", output_mode="files_with_matches")

# With context

Grep("ClassName", output_mode="content", -A=2, -B=2, head_limit=5)
```

### Schema Base Extension Pattern

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Agent Name Schema",
  "description": "Schema for [agent-name] performing [operation]",
  "version": "1.0.0",
  "type": "object",
  "extends": "base-agent.schema.json",
  "properties": {
    "output": {
      "type": "object",
      "oneOf": [
        {
          "title": "Success Output",
          "properties": {
            "status": { "const": "SUCCESS" },
            "agent": { "const": "agent-name" },
            "agent_specific_output": {
              // ... nested structure
            }
          }
        },
        {
          "title": "Failure Output",
          "properties": {
            "status": { "const": "FAILURE" },
            "agent": { "const": "agent-name" },
            "failure_details": {
              // ... failure structure
            }
          }
        }
      ]
    }
  }
}
```

### Failure Details Pattern

```json
{
  "failure_details": {
    "failure_type": "specific_failure_type",
    "reasons": ["Specific reason 1", "Specific reason 2"],
    "recovery_suggestions": [
      {
        "suggestion": "Actionable recovery step",
        "effort_estimate": "30 seconds",
        "confidence": 0.95
      }
    ],
    "partial_results": {
      "work_completed": "Description of partial progress"
    },
    "research_attempted": ["Tool('operation') - SUCCESS/FAILURE: details"],
    "next_steps": ["Actionable recommendation for orchestrator"]
  }
}
```

---

## File References

**Golden Examples**:

- **Agent**: `.claude/agents/researcher-codebase.md` (94/100)
- **Schema**: `.claude/docs/schemas/feature-analyzer.schema.json` (96/100)

**Supporting Documents**:

- **Template**: `.claude/templates/agent.template.md` (v5.0)
- **Base Pattern**: `.claude/docs/guides/base-agent-pattern.md`
- **Base Schema**: `.claude/docs/schemas/base-agent.schema.json`
- **File Operation Protocol**: `.claude/docs/guides/file-operation-protocol.md`
- **Agent Standards**: `.claude/docs/agent-standards-extended.md`

---

**This guide provides concrete, actionable examples for creating high-quality agents and schemas. Use researcher-codebase.md and feature-analyzer.schema.json as reference implementations when building new agents or reviewing existing ones for quality improvements.**
