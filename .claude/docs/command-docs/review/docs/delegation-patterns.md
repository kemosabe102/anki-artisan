# Delegation Patterns for /review Command

Exact Task() call syntax for each phase of the review workflow.

---

## Phase 2: File Batching (via source-control)

The source-control agent's file grouping capability is used here. It analyzes git status output and groups files based on:
- Change type (modifications, additions, deletions)
- Language/file type
- Directory proximity

```
Task(
  subagent_type="source-control",
  description="Group files for review batching",
  prompt="Analyze and group these files into review batches:

    Files: {file_list}
    
    Requirements:
    - Max 5 files per batch
    - Group by language first, then directory proximity
    - Consider change type for logical grouping
    
    Return: {batches: [{batch_id, language, agent, files, file_count}]}"
)
```

**Expected Output**:
```json
{
  "batches": [
    {
      "batch_id": 1,
      "language": "Python",
      "agent": "code-quality",
      "files": ["src/auth.py", "src/validation.py"],
      "file_count": 2
    }
  ]
}
```

---

## Phase 3: Multi-Agent Review

### Core Agent: Language Reviewer

```
Task(
  subagent_type="code-quality",
  description="Review Python files for quality issues",
  prompt="Review code files for quality issues:

    Files: {batch.files}
    Focus: {focus_param}  # security|performance|quality|design|all
    Mode: {mode_param}    # quick|comprehensive
    
    For each finding include:
    - location (file:line)
    - severity (Critical|High|Medium|Low|Nit)
    - confidence (0.0-1.0)
    - message (clear description)
    - recommendation (actionable fix)
    - verification_command (deterministic check)
    
    Return: {findings: [], summary: {total, by_severity}}"
)
```

### Core Agent: Tech Debt

```
Task(
  subagent_type="tech-debt-investigator",
  description="Analyze technical debt in review files",
  prompt="Analyze technical debt in files:

    Files: {all_files}
    
    Calculate:
    - debt_score (0-100)
    - TDR (Technical Debt Ratio)
    - Hotspots (files with most debt)
    - Category breakdown (duplication, complexity, coupling, etc.)
    
    Return: {debt_score, tdr, hotspots: [], categories: {}, recommendations: []}"
)
```

### Core Agent: Security Scanner

```
Task(
  subagent_type="sast-scanner",
  description="Security scan for vulnerabilities",
  prompt="Security scan for vulnerabilities:

    Files: {all_files}
    Depth: {mode_param}  # quick|comprehensive
    
    Check for:
    - OWASP Top 10 (2021)
    - LLM Top 10 (2023) if applicable
    - Hardcoded secrets
    - Injection vulnerabilities
    - Authentication/authorization issues
    
    Return: {vulnerabilities: [], severity_counts: {}, owasp_coverage: {}}"
)
```

### Dynamic Agent Selection (Future)

**Current Status**: Dynamic agents not yet implemented. Skip this section during execution.

```python
# FUTURE: Calculate confidence for optional agents when available
# confidence = (domain_fit * 0.6) + (unique_value * 0.3) + (cost_efficiency * 0.1)
#
# Planned agents (not yet available):
# - design-pattern-reviewer
# - performance-reviewer  
# - api-contract-reviewer
#
# For now: Use only 3 core agents (code-quality, tech-debt-investigator, sast-scanner)
```

---

## Phase 4: Confidence Investigation

### Context7 Research (0.75-0.89 confidence)

```
# Step 1: Resolve library
mcp__context7__resolve-library-id(library_name="fastapi")
# Returns: "/fastapi/fastapi"

# Step 2: Fetch relevant docs
mcp__context7__get-library-docs(
  library_id="/fastapi/fastapi",
  topic="async dependency injection"
)
# Validate finding against official documentation
```

### Perplexity Escalation (< 0.75 confidence)

```
mcp__plugin_perplexity_perplexity__perplexity_search(
  query="Is using requests.get() in async Python functions a blocking issue?",
  focus="comprehensive"
)
# Cross-reference with OWASP, PEP, RFC standards
```

---

## Parallel Launch Pattern

**Launch all core agents in single message**:

```
Launching 3 core review agents in parallel...

Task(subagent_type='code-quality', prompt={...})
Task(subagent_type='tech-debt-investigator', prompt={...})
Task(subagent_type='sast-scanner', prompt={...})
```

**Dynamic agents (FUTURE - not yet implemented)**:

```
# FUTURE: When dynamic agents are available, add if confidence > 0.8
# Example (not yet implemented):
# Task(subagent_type='design-pattern-reviewer', prompt={...})
# Task(subagent_type='performance-reviewer', prompt={...})
```

**Total**: 3 agents in parallel per review (core only until dynamic agents implemented)
