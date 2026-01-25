# Prompt Evaluator Delegation Examples

## Positive Examples (Grades A-B)

### Example 1: Full Evaluation (Grade A)

**Delegation**:
```
Task(prompt-evaluator, "Evaluate agent prompt quality for .claude/agents/researcher-external.md")
```

**Expected Output (SUCCESS)**:
```json
{
  "status": "SUCCESS",
  "agent": "prompt-evaluator",
  "confidence": 0.88,
  "agent_specific_output": {
    "evaluation_summary": {
      "agent_name": "researcher-external",
      "overall_grade": "A",
      "risk_level": "MEDIUM"
    },
    "structural_quality": {
      "score": "15/16",
      "percentage": 93.8,
      "passing_criteria": [
        {"criterion": "Frontmatter compliance", "evidence": "researcher-external.md:1-14"}
      ],
      "failing_criteria": [
        {"criterion": "Base pattern inheritance", "evidence": "researcher-external.md:137", "fix_guidance": "Remove duplicated sections"}
      ]
    },
    "prompt_engineering_quality": {
      "score": 8,
      "grade": "A",
      "strengths": ["Exceptional role clarity", "Comprehensive tool documentation"],
      "weaknesses": ["Missing few-shot examples"]
    },
    "token_optimization": {
      "current_tokens": 5234,
      "optimization_potential": 1200,
      "optimization_percentage": 22.9
    }
  }
}
```

---

### Example 2: Focused Token Analysis

**Delegation**:
```
Task(prompt-evaluator, "Analyze token optimization opportunities for .claude/agents/agent-architect.md with focus=tokens")
```

**Expected Output**: Token optimization section with prioritized techniques and savings estimates.

---

### Example 3: Anti-Pattern Scan

**Delegation**:
```
Task(prompt-evaluator, "Scan .claude/agents/debugger.md for anti-patterns")
```

**Expected Output**: `anti_patterns_detected` array with severity, locations, and fix guidance.

---

### Example 4: Batch Evaluation

**Delegation**:
```
Task(prompt-evaluator, "Evaluate all agents in .claude/agents/dev-tools/ for structural quality")
```

**Note**: Agent processes files sequentially, returns aggregated results.

---

## Negative Examples (Grades C-F)

### Example 5: Grade D Agent (Scope Creep + Tool Bloat)

**Delegation**:
```
Task(prompt-evaluator, "Evaluate agent: .claude/agents/example-bad-scope.md")
```

**Agent Content (example-bad-scope.md)**:
```yaml
---
name: do-everything-agent
description: Handles all tasks including code review, testing, deployment, documentation, and user support
tools: Read, Write, Edit, Bash, Grep, Glob, WebFetch, WebSearch, Task
---
## Core Behavior
This agent does code review, runs tests, deploys to production, writes documentation, and handles user questions.
It can also manage infrastructure, monitor logs, and respond to incidents.
```

**Expected Output (SUCCESS - Grade D)**:
```json
{
  "status": "SUCCESS",
  "agent": "prompt-evaluator",
  "confidence": 0.91,
  "agent_specific_output": {
    "evaluation_summary": {
      "agent_name": "do-everything-agent",
      "overall_grade": "D",
      "risk_level": "CRITICAL"
    },
    "structural_quality": {
      "score": "5/16",
      "percentage": 31.3,
      "passing_criteria": [
        {"criterion": "Has frontmatter", "evidence": "example-bad-scope.md:1-5"},
        {"criterion": "Has name field", "evidence": "example-bad-scope.md:2"},
        {"criterion": "Has description", "evidence": "example-bad-scope.md:3"},
        {"criterion": "Has tools declared", "evidence": "example-bad-scope.md:4"},
        {"criterion": "Has Core Behavior section", "evidence": "example-bad-scope.md:7"}
      ],
      "failing_criteria": [
        {"criterion": "Single responsibility", "evidence": "example-bad-scope.md:3 - 5+ responsibilities listed", "fix_guidance": "Split into focused agents"},
        {"criterion": "Tool count reasonable", "evidence": "example-bad-scope.md:4 - 9 tools declared", "fix_guidance": "Reduce to 3-5 essential tools"},
        {"criterion": "Base pattern extension", "evidence": "Missing entirely", "fix_guidance": "Add extends: base-agent-pattern.md"},
        {"criterion": "Error recovery section", "evidence": "Missing", "fix_guidance": "Add Error Recovery table"},
        {"criterion": "Quality standards", "evidence": "Missing", "fix_guidance": "Define output quality criteria"}
      ]
    },
    "prompt_engineering_quality": {
      "score": 2.1,
      "grade": "D",
      "strengths": ["Has basic structure"],
      "weaknesses": ["No role clarity", "No boundaries defined", "Vague instructions", "No examples"]
    },
    "anti_patterns_detected": [
      {"pattern": "scope_creep", "severity": "critical", "locations": ["example-bad-scope.md:3", "example-bad-scope.md:8-9"], "fix": "Split into 5+ single-purpose agents"},
      {"pattern": "tool_bloat", "severity": "critical", "locations": ["example-bad-scope.md:4"], "fix": "Audit tool usage, remove unused tools"},
      {"pattern": "missing_base_pattern", "severity": "major", "locations": ["entire file"], "fix": "Extend base-agent-pattern.md"},
      {"pattern": "no_error_recovery", "severity": "critical", "locations": ["entire file"], "fix": "Add Error Recovery section with failure types"}
    ],
    "issues": {
      "critical": [
        {"issue": "Violates single responsibility principle", "evidence": "example-bad-scope.md:3", "fix_guidance": "One agent = one job"},
        {"issue": "No failure handling", "evidence": "Missing Error Recovery", "fix_guidance": "Add FAILURE output structure"}
      ],
      "major": [
        {"issue": "9 tools without justification", "evidence": "example-bad-scope.md:4", "fix_guidance": "Document why each tool needed"}
      ],
      "minor": []
    },
    "recommended_improvements": {
      "immediate_actions": [
        {"action": "Split into focused agents", "rationale": "Single responsibility violation", "impact": "Enables proper evaluation", "priority_score": 0.95}
      ],
      "short_term_actions": [],
      "long_term_optimizations": []
    }
  }
}
```

**Why Grade D**: Violates single responsibility (5+ jobs), excessive tools (9 declared), missing base pattern inheritance, no error recovery, no workflow structure. This agent would be unpredictable and unmaintainable.

---

### Example 6: Grade F Agent (No Structure)

**Delegation**:
```
Task(prompt-evaluator, "Evaluate agent: .claude/agents/example-no-structure.md")
```

**Agent Content (example-no-structure.md)**:
```markdown
# Helper Agent

You help with things. Do whatever the user asks. Use any tools you need.

Be helpful and nice.
```

**Expected Output (SUCCESS - Grade F)**:
```json
{
  "status": "SUCCESS",
  "agent": "prompt-evaluator",
  "confidence": 0.94,
  "agent_specific_output": {
    "evaluation_summary": {
      "agent_name": "helper-agent",
      "overall_grade": "F",
      "risk_level": "CRITICAL"
    },
    "structural_quality": {
      "score": "1/16",
      "percentage": 6.3,
      "passing_criteria": [
        {"criterion": "Has markdown content", "evidence": "example-no-structure.md:1-5"}
      ],
      "failing_criteria": [
        {"criterion": "Has frontmatter", "evidence": "Missing YAML frontmatter block", "fix_guidance": "Add ---\\nname:\\ndescription:\\ntools:\\n---"},
        {"criterion": "Has name field", "evidence": "No frontmatter", "fix_guidance": "Add name field"},
        {"criterion": "Has description", "evidence": "No frontmatter", "fix_guidance": "Add description with trigger keywords"},
        {"criterion": "Has tools declared", "evidence": "No frontmatter", "fix_guidance": "Declare specific tools"},
        {"criterion": "Single responsibility", "evidence": "example-no-structure.md:3 - 'Do whatever'", "fix_guidance": "Define specific purpose"},
        {"criterion": "Base pattern extension", "evidence": "Missing", "fix_guidance": "Extend base-agent-pattern.md"},
        {"criterion": "Core Behavior section", "evidence": "Missing", "fix_guidance": "Add ## Core Behavior"},
        {"criterion": "Role & Boundaries", "evidence": "Missing", "fix_guidance": "Define scope limits"},
        {"criterion": "Error recovery", "evidence": "Missing", "fix_guidance": "Add failure handling"},
        {"criterion": "Quality standards", "evidence": "Missing", "fix_guidance": "Define output criteria"},
        {"criterion": "Knowledge base", "evidence": "Missing", "fix_guidance": "Reference docs"},
        {"criterion": "Anti-patterns section", "evidence": "Missing", "fix_guidance": "Add NEVER DO list"},
        {"criterion": "Good patterns section", "evidence": "Missing", "fix_guidance": "Add ALWAYS DO list"},
        {"criterion": "Technical details", "evidence": "Missing", "fix_guidance": "Add schema reference"},
        {"criterion": "Workflow definition", "evidence": "Missing", "fix_guidance": "Add The Flow section"}
      ]
    },
    "prompt_engineering_quality": {
      "score": 0.5,
      "grade": "F",
      "strengths": [],
      "weaknesses": [
        "No role definition",
        "No task boundaries",
        "No tool specification",
        "Completely vague instructions",
        "No examples or structure",
        "Security risk: 'Use any tools'"
      ]
    },
    "anti_patterns_detected": [
      {"pattern": "scope_creep", "severity": "critical", "locations": ["example-no-structure.md:3"], "fix": "Define single purpose"},
      {"pattern": "no_structure", "severity": "critical", "locations": ["entire file"], "fix": "Use agent.template.md"},
      {"pattern": "missing_frontmatter", "severity": "critical", "locations": ["line 1"], "fix": "Add YAML frontmatter"},
      {"pattern": "security_risk", "severity": "critical", "locations": ["example-no-structure.md:3"], "fix": "Whitelist specific tools"},
      {"pattern": "no_error_recovery", "severity": "critical", "locations": ["entire file"], "fix": "Add Error Recovery section"},
      {"pattern": "vague_instructions", "severity": "critical", "locations": ["example-no-structure.md:3-5"], "fix": "Provide specific guidance"}
    ],
    "issues": {
      "critical": [
        {"issue": "No frontmatter - not a valid agent", "evidence": "line 1", "fix_guidance": "Add YAML frontmatter block"},
        {"issue": "Security risk - unrestricted tool access", "evidence": "example-no-structure.md:3", "fix_guidance": "Declare specific tools"},
        {"issue": "No defined purpose", "evidence": "example-no-structure.md:3", "fix_guidance": "Single responsibility statement"}
      ],
      "major": [
        {"issue": "No structure whatsoever", "evidence": "entire file", "fix_guidance": "Start from agent.template.md"}
      ],
      "minor": []
    },
    "recommended_improvements": {
      "immediate_actions": [
        {"action": "Start over using agent.template.md", "rationale": "Current content unsalvageable", "impact": "Creates valid agent structure", "priority_score": 1.0}
      ],
      "short_term_actions": [],
      "long_term_optimizations": []
    }
  }
}
```

**Why Grade F**: Missing frontmatter (invalid agent), no structure, security risk ("use any tools"), completely vague purpose ("help with things"). This file is not a functional agent - it needs complete rewrite from template.

---

### Example 7: Grade C Agent (Partial Issues - Fixable)

**Delegation**:
```
Task(prompt-evaluator, "Evaluate agent: .claude/agents/example-mediocre.md")
```

**Agent Content (example-mediocre.md)**:
```yaml
---
name: file-organizer
description: Organizes files in directories
tools: Read, Write, Bash, Glob
---
## Core Behavior

You organize files by moving them to appropriate directories based on their type.

### How to Start
Read the directory, identify file types, move files to organized folders.

### The Flow
```
Directory path received → Scan files → Categorize by extension → Create folders → Move files
```

## Role & Boundaries

| Aspect | Details |
|--------|---------|
| **Your Job** | Organize files by type |
| **Boundaries** | Only work in specified directory |
```

**Expected Output (SUCCESS - Grade C)**:
```json
{
  "status": "SUCCESS",
  "agent": "prompt-evaluator",
  "confidence": 0.87,
  "agent_specific_output": {
    "evaluation_summary": {
      "agent_name": "file-organizer",
      "overall_grade": "C",
      "risk_level": "MEDIUM"
    },
    "structural_quality": {
      "score": "9/16",
      "percentage": 56.3,
      "passing_criteria": [
        {"criterion": "Has frontmatter", "evidence": "example-mediocre.md:1-5"},
        {"criterion": "Has name field", "evidence": "example-mediocre.md:2"},
        {"criterion": "Has description", "evidence": "example-mediocre.md:3"},
        {"criterion": "Has tools declared", "evidence": "example-mediocre.md:4"},
        {"criterion": "Single responsibility", "evidence": "example-mediocre.md:3 - single purpose"},
        {"criterion": "Core Behavior section", "evidence": "example-mediocre.md:7"},
        {"criterion": "How to Start", "evidence": "example-mediocre.md:11"},
        {"criterion": "The Flow section", "evidence": "example-mediocre.md:14"},
        {"criterion": "Role & Boundaries", "evidence": "example-mediocre.md:18"}
      ],
      "failing_criteria": [
        {"criterion": "Description has trigger keywords", "evidence": "example-mediocre.md:3 - too short", "fix_guidance": "Add 'Use for: X. NOT for: Y'"},
        {"criterion": "Base pattern extension", "evidence": "Missing", "fix_guidance": "Add extends reference"},
        {"criterion": "Error recovery section", "evidence": "Missing", "fix_guidance": "Add Error Recovery table"},
        {"criterion": "Quality standards", "evidence": "Missing", "fix_guidance": "Define success criteria"},
        {"criterion": "Anti-patterns section", "evidence": "Missing", "fix_guidance": "Add NEVER DO list"},
        {"criterion": "Good patterns section", "evidence": "Missing", "fix_guidance": "Add ALWAYS DO list"},
        {"criterion": "Technical details/schema", "evidence": "Missing", "fix_guidance": "Add schema reference"}
      ]
    },
    "prompt_engineering_quality": {
      "score": 5.2,
      "grade": "C",
      "strengths": ["Clear single purpose", "Basic workflow defined", "Has boundaries table"],
      "weaknesses": ["No examples", "Vague tool usage", "Missing edge cases", "No confidence guidance"]
    },
    "anti_patterns_detected": [
      {"pattern": "missing_base_pattern", "severity": "major", "locations": ["entire file"], "fix": "Extend base-agent-pattern.md"},
      {"pattern": "no_error_recovery", "severity": "major", "locations": ["entire file"], "fix": "Add Error Recovery section"},
      {"pattern": "vague_tool_descriptions", "severity": "minor", "locations": ["example-mediocre.md:4"], "fix": "Document when to use each tool"}
    ],
    "issues": {
      "critical": [],
      "major": [
        {"issue": "No error handling for failed moves", "evidence": "Missing Error Recovery", "fix_guidance": "Handle permission errors, disk full"},
        {"issue": "No base pattern inheritance", "evidence": "Missing extends", "fix_guidance": "Add inheritance to save tokens"}
      ],
      "minor": [
        {"issue": "Description too short", "evidence": "example-mediocre.md:3", "fix_guidance": "Add trigger keywords and NOT-for cases"},
        {"issue": "No examples section", "evidence": "Missing", "fix_guidance": "Add 2-3 delegation examples"}
      ]
    },
    "recommended_improvements": {
      "immediate_actions": [
        {"action": "Add Error Recovery section", "rationale": "File operations can fail", "impact": "Prevents silent failures", "priority_score": 0.82},
        {"action": "Extend base-agent-pattern.md", "rationale": "Duplicating standard sections", "impact": "~400 token savings", "priority_score": 0.75}
      ],
      "short_term_actions": [
        {"action": "Add Anti-patterns/Good patterns sections", "rationale": "Missing behavioral guidance", "impact": "Clearer agent behavior", "priority_score": 0.65}
      ],
      "long_term_optimizations": [
        {"action": "Add schema and examples", "rationale": "Improves maintainability"}
      ]
    }
  }
}
```

**Why Grade C**: Has basic structure and single purpose (good), but missing critical sections: error recovery, base pattern inheritance, anti-patterns list. Fixable with 30-60 minutes of work. This agent would work for simple cases but fail on edge cases.

---

## FAILURE Examples (All 6 Types)

### Example 8: FILE_NOT_FOUND

**Delegation**:
```
Task(prompt-evaluator, "Evaluate .claude/agents/non-existent-agent.md")
```

**Expected Output (FAILURE)**:
```json
{
  "status": "FAILURE",
  "agent": "prompt-evaluator",
  "confidence": 0.0,
  "failure_details": {
    "failure_type": "FILE_NOT_FOUND",
    "reasons": ["Agent file not found at path: .claude/agents/non-existent-agent.md"],
    "recovery_suggestions": [
      {"suggestion": "Verify agent file path exists", "effort": "low"},
      {"suggestion": "List available agents: Glob('.claude/agents/**/*.md')", "effort": "low"},
      {"suggestion": "Check for typos in agent name", "effort": "low"}
    ]
  }
}
```

---

### Example 9: FILE_UNREADABLE

**Delegation**:
```
Task(prompt-evaluator, "Evaluate .claude/agents/corrupted-agent.md")
```

**Expected Output (FAILURE)**:
```json
{
  "status": "FAILURE",
  "agent": "prompt-evaluator",
  "confidence": 0.0,
  "failure_details": {
    "failure_type": "FILE_UNREADABLE",
    "reasons": [
      "File exists but cannot be read",
      "Possible causes: binary file, encoding issues, permission denied"
    ],
    "recovery_suggestions": [
      {"suggestion": "Check file encoding (should be UTF-8)", "effort": "low"},
      {"suggestion": "Verify file permissions", "effort": "low"},
      {"suggestion": "Re-create file from backup or template", "effort": "medium"}
    ]
  }
}
```

---

### Example 10: INVALID_PATH

**Delegation**:
```
Task(prompt-evaluator, "Evaluate ../../../etc/passwd")
```

**Expected Output (FAILURE)**:
```json
{
  "status": "FAILURE",
  "agent": "prompt-evaluator",
  "confidence": 0.0,
  "failure_details": {
    "failure_type": "INVALID_PATH",
    "reasons": [
      "Path is outside allowed scope",
      "Prompt evaluator only operates on .claude/agents/** files",
      "Path traversal detected: ../../../etc/passwd"
    ],
    "recovery_suggestions": [
      {"suggestion": "Use path within .claude/agents/ directory", "effort": "low"},
      {"suggestion": "Example valid path: .claude/agents/dev-tools/debugger.md", "effort": "low"}
    ]
  }
}
```

---

### Example 11: SCHEMA_MISSING

**Delegation**:
```
Task(prompt-evaluator, "Evaluate .claude/agents/new-agent.md with schema validation")
```

**Expected Output (FAILURE)**:
```json
{
  "status": "FAILURE",
  "agent": "prompt-evaluator",
  "confidence": 0.0,
  "failure_details": {
    "failure_type": "SCHEMA_MISSING",
    "reasons": [
      "Schema validation requested but no schema file found",
      "Expected schema at: .claude/agents/new-agent/schemas/new-agent.schema.json",
      "Agent definition references schema but file does not exist"
    ],
    "recovery_suggestions": [
      {"suggestion": "Create schema file extending base-agent.schema.json", "effort": "medium"},
      {"suggestion": "Run evaluation without schema validation", "effort": "low"},
      {"suggestion": "Use agent-architect to generate schema", "effort": "medium"}
    ]
  }
}
```

---

### Example 12: EVALUATION_INCOMPLETE

**Delegation**:
```
Task(prompt-evaluator, "Evaluate .claude/agents/complex-agent.md")
```

**Expected Output (FAILURE with partial results)**:
```json
{
  "status": "FAILURE",
  "agent": "prompt-evaluator",
  "confidence": 0.45,
  "failure_details": {
    "failure_type": "EVALUATION_INCOMPLETE",
    "reasons": [
      "Token counter script failed (scripts/calculate_tokens.py returned error)",
      "Could not complete token optimization analysis",
      "3 of 7 frameworks could not be evaluated"
    ],
    "partial_results": {
      "completed_dimensions": [
        "structural_quality",
        "prompt_engineering_quality",
        "anti_pattern_detection",
        "testing_strategy"
      ],
      "incomplete_dimensions": [
        "token_optimization",
        "progressive_disclosure",
        "token_density"
      ]
    },
    "recovery_suggestions": [
      {"suggestion": "Run 'uv sync' to ensure dependencies installed", "effort": "low"},
      {"suggestion": "Verify scripts/calculate_tokens.py exists and is executable", "effort": "low"},
      {"suggestion": "Re-run with focus=structural to skip token analysis", "effort": "low"},
      {"suggestion": "Use line count heuristic: tokens ~ lines x 10", "effort": "medium"}
    ]
  }
}
```

**Note**: Partial results may still be useful. Check `partial_results.completed_dimensions` for available data.

---

### Example 13: GUIDE_UNAVAILABLE

**Delegation**:
```
Task(prompt-evaluator, "Evaluate .claude/agents/dev-tools/debugger.md with framework alignment check")
```

**Expected Output (FAILURE)**:
```json
{
  "status": "FAILURE",
  "agent": "prompt-evaluator",
  "confidence": 0.0,
  "failure_details": {
    "failure_type": "GUIDE_UNAVAILABLE",
    "reasons": [
      "Required evaluation guide not found",
      "Missing: docs/evaluation-frameworks.md",
      "Framework 7 (Framework Alignment) requires external reference document"
    ],
    "recovery_suggestions": [
      {"suggestion": "Restore docs/evaluation-frameworks.md from git", "effort": "low"},
      {"suggestion": "Run evaluation without framework alignment: focus=structural", "effort": "low"},
      {"suggestion": "Check .claude/agents/dev-tools/prompt-evaluator/docs/ directory", "effort": "low"}
    ]
  }
}
```

---

## Key Patterns

### Evidence Citation Format
All findings include `file:line` references:
- Single line: `agent.md:41`
- Line range: `agent.md:15-23`
- Section: `agent.md:Core Behavior`

### Quantified Impact
Token savings and priority scores always included:
- "800 token savings (15% reduction)"
- "priority_score: 0.82"

### Confidence Tracking
Per-dimension and overall confidence (0.0-1.0):
- High confidence (>0.8): Tool-verified data (token counts, grep results)
- Medium confidence (0.5-0.8): Pattern matching, heuristics
- Low confidence (<0.5): Estimates, partial data

### Grade Thresholds

| Grade | Score Range | Structural | Interpretation |
|-------|-------------|------------|----------------|
| A | 8.0-9.0 | 14-16/16 | Production ready |
| B | 6.5-7.9 | 11-13/16 | Minor improvements needed |
| C | 5.0-6.4 | 8-10/16 | Significant gaps, functional |
| D | 3.0-4.9 | 4-7/16 | Major issues, needs rework |
| F | 0.0-2.9 | 0-3/16 | Not functional, start over |
