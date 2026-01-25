# Delegation Patterns

Task() call templates for the feature-design-workflow skill.

**Legend**: ⚡ Parallel execution | 🔗 Sequential execution

---

## OBSERVE Phase - Context Gathering

### Explore Existing Patterns

**Agent**: `researcher-codebase` ⚡

```python
Task(
    subagent_type="researcher-codebase",
    prompt="""Explore existing patterns for feature: {feature_name}

    Context:
    - Feature description: {feature_description}
    - Target directory: {target_directory}
    
    Search for:
    1. Similar implementations in the codebase
    2. Related interfaces and abstractions
    3. Existing utilities that could be reused
    4. Naming conventions in the target area
    
    Expected output:
    {
        "similar_implementations": [
            {"file": "path/to/file.py", "relevance": 0.85, "pattern": "description"}
        ],
        "reusable_components": [],
        "naming_conventions": {},
        "recommendations": []
    }"""
)
```


### Research Best Practices

**Agent**: `researcher-external` ⚡

```python
Task(
    subagent_type="researcher-external",
    prompt="""Research best practices for feature: {feature_name}

    Context:
    - Technology stack: {tech_stack}
    - Feature requirements: {requirements}
    
    Research topics:
    1. Industry best practices for this feature type
    2. Common pitfalls and anti-patterns
    3. Security considerations
    4. Performance optimization strategies
    
    Expected output:
    {
        "best_practices": [],
        "anti_patterns": [],
        "security_considerations": [],
        "performance_tips": [],
        "sources": []
    }"""
)
```

**Note**: Use `researcher-external` via Context7 FIRST for official docs (free), then Perplexity for community patterns (paid).

---

## ORIENT Phase - Design Validation

### Validate Design Decisions

**Agent**: `architectureer` ⚡

```python
Task(
    subagent_type="architectureer",
    prompt="""Validate architecture for feature: {feature_name}

    Context:
    - Proposed design: {design_document}
    - Target location: {target_directory}
    - Dependencies: {dependencies}
    
    Evaluate:
    1. Alignment with existing architecture patterns
    2. Separation of concerns
    3. Interface design quality
    4. Dependency management
    5. Scalability considerations
    
    Expected output:
    {
        "alignment_score": 0.0-1.0,
        "concerns": [
            {"category": "coupling|cohesion|complexity", "issue": "description", "severity": "HIGH|MEDIUM|LOW"}
        ],
        "recommendations": [],
        "status": "APPROVED" | "WARN" | "BLOCKED"
    }"""
)
```

### Review Requirements Completeness

**Agent**: `planning` ⚡

```python
Task(
    subagent_type="planning",
    prompt="""Review specification for feature: {feature_name}

    Context:
    - Specification file: {spec_file}
    - Related requirements: {requirements}
    
    Validate:
    1. Completeness of acceptance criteria
    2. Edge cases coverage
    3. Error handling requirements
    4. Integration points clarity
    5. Testability of requirements
    
    Expected output:
    {
        "completeness_score": 0.0-1.0,
        "missing_requirements": [],
        "ambiguous_items": [],
        "edge_cases_needed": [],
        "status": "APPROVED" | "WARN" | "BLOCKED"
    }"""
)
```

### Assess Implementation Complexity

**Agent**: `tech-debt-investigator` ⚡

```python
Task(
    subagent_type="tech-debt-investigator",
    prompt="""Assess complexity for feature: {feature_name}

    Context:
    - Target files: {target_files}
    - Proposed changes: {change_summary}
    
    Analyze:
    1. Cyclomatic complexity impact
    2. Coupling to existing modules
    3. Technical debt introduction risk
    4. Maintenance burden estimate
    
    Expected output:
    {
        "complexity_score": 0.0-1.0,
        "debt_risk": "LOW|MEDIUM|HIGH",
        "coupling_issues": [],
        "maintenance_concerns": [],
        "refactoring_suggestions": [],
        "status": "APPROVED" | "WARN" | "BLOCKED"
    }"""
)
```

---

## DECIDE Phase - Test Planning

### Generate Test Specifications

**Agent**: `code-quality` 🔗

```python
Task(
    subagent_type="code-quality",
    prompt="""Generate test specifications for feature: {feature_name}

    Context:
    - Feature specification: {spec_file}
    - Implementation plan: {implementation_plan}
    - Target test file: {test_file}
    
    Generate:
    1. Unit test cases for each function
    2. Integration test scenarios
    3. Edge case coverage
    4. Error handling tests
    5. Mock requirements
    
    Expected output:
    {
        "test_file": "path/to/test_file.py",
        "test_cases": [
            {"name": "test_function_name", "type": "unit|integration", "description": "what it tests"}
        ],
        "mocks_required": [],
        "coverage_estimate": 0.0-1.0,
        "priority_order": []
    }
    
    IMPORTANT: Generate test SPECIFICATIONS only. Do NOT write test code yet."""
)
```

**Note**: Test specifications should be approved before implementation begins (TDD approach).

---

## ACT Phase - Implementation

### Write Production Code

**Agent**: `development` 🔗

```python
Task(
    subagent_type="development",
    prompt="""Implement feature: {feature_name}

    Context:
    - Target file: {target_file}  # ONE file per Task
    - Specification: {spec_summary}
    - Test file: {test_file}
    - Dependencies: {dependencies}
    
    Implementation requirements:
    1. Follow existing code patterns in {target_directory}
    2. Include type hints (strict typing, no Any)
    3. Add Google-style docstrings for public APIs
    4. Handle errors explicitly
    5. Ensure test file passes after implementation
    
    Expected output:
    {
        "file": "path/to/file.py",
        "functions_added": [],
        "classes_added": [],
        "imports_added": [],
        "status": "COMPLETE" | "PARTIAL" | "BLOCKED",
        "blockers": []
    }
    
    CRITICAL: Implement ONE file at a time for retryability."""
)
```

**File-Scoped Delegation**: For multi-file features, spawn parallel Tasks:

```python
# Parallel implementation of independent files
parallel([
    Task(subagent_type="development", prompt=impl_prompt(file1)),
    Task(subagent_type="development", prompt=impl_prompt(file2)),
    Task(subagent_type="development", prompt=impl_prompt(file3)),
])  # Max 5 parallel
```

### Review Code Quality

**Agent**: `code-quality` ⚡

```python
Task(
    subagent_type="code-quality",
    prompt="""Review implementation for feature: {feature_name}

    Context:
    - File to review: {target_file}  # ONE file per Task
    - Specification: {spec_summary}
    - Related test file: {test_file}
    
    Review criteria:
    1. Correctness: Does it meet the specification?
    2. Security: Any vulnerabilities? (injection, auth bypass, data exposure)
    3. Performance: Any obvious bottlenecks?
    4. Maintainability: Clear, readable, documented?
    5. Test coverage: Are tests adequate?
    
    Focus on BLOCKING issues only. Do NOT flag:
    - Style preferences
    - Minor improvements
    - "Nice to have" changes
    
    Expected output:
    {
        "file": "path/to/file.py",
        "status": "APPROVED" | "WARN" | "BLOCKED",
        "issues": [
            {"severity": "BLOCKING|WARNING", "line": 42, "issue": "description", "fix": "suggestion"}
        ],
        "issue_count": 0
    }"""
)
```

### Run Test Suites

**Agent**: `code-quality` 🔗

```python
Task(
    subagent_type="code-quality",
    prompt="""Execute tests for feature: {feature_name}

    Context:
    - Test file: {test_file}
    - Implementation file: {target_file}
    
    Execute:
    1. Run: uv run pytest {test_file} -v --tb=short
    2. Capture output and parse results
    3. If failures, extract error details
    
    Expected output:
    {
        "test_file": "path/to/test_file.py",
        "total_tests": 10,
        "passed": 9,
        "failed": 1,
        "skipped": 0,
        "failures": [
            {"test": "test_name", "error": "assertion message", "traceback": "short trace"}
        ],
        "coverage": 0.85,
        "status": "PASS" | "FAIL"
    }"""
)
```

### Fix Failing Tests/Issues

**Agent**: `debugger` 🔗

```python
Task(
    subagent_type="debugger",
    prompt="""Debug failing tests for feature: {feature_name}

    Context:
    - Test file: {test_file}
    - Implementation file: {target_file}
    - Failure details: {failure_details}
    
    Debug process:
    1. Analyze the failure traceback
    2. Identify root cause (implementation bug vs test bug)
    3. Propose fix with rationale
    4. Apply fix to appropriate file
    5. Re-run test to verify
    
    Expected output:
    {
        "root_cause": "description of the issue",
        "fix_location": "implementation|test",
        "file_modified": "path/to/file.py",
        "changes_made": "description of fix",
        "verification": "PASS" | "FAIL",
        "status": "RESOLVED" | "ESCALATE"
    }
    
    If ESCALATE, provide detailed analysis for human review."""
)
```

---

## Parallel Execution Patterns

### OBSERVE Phase (All Parallel) ⚡

```python
# Launch research agents in parallel
observe_results = parallel([
    Task(subagent_type="researcher-codebase", prompt=codebase_prompt),
    Task(subagent_type="researcher-external", prompt=web_prompt),
])
```

### ORIENT Phase (All Parallel) ⚡

```python
# Launch validation agents in parallel
orient_results = parallel([
    Task(subagent_type="architectureer", prompt=arch_prompt),
    Task(subagent_type="planning", prompt=spec_prompt),
    Task(subagent_type="tech-debt-investigator", prompt=debt_prompt),
])
```

### ACT Phase (Sequential with Parallel Reviews) 🔗⚡

```python
# Sequential: Implementation -> Review -> Test -> Debug
for file in implementation_files:
    # 1. Implement (sequential per file)
    impl_result = Task(subagent_type="development", prompt=impl_prompt(file))
    
    if impl_result.status == "BLOCKED":
        escalate(impl_result)
        continue
    
    # 2. Review (parallel for multiple reviewers)
    review_results = parallel([
        Task(subagent_type="code-quality", prompt=review_prompt(file)),
    ])
    
    # 3. Test (sequential - must complete before debug)
    test_result = Task(subagent_type="code-quality", prompt=test_prompt(file))
    
    # 4. Debug if needed (sequential)
    if test_result.status == "FAIL":
        debug_result = Task(subagent_type="debugger", prompt=debug_prompt(file, test_result))
```

---

## Error Handling Notes


| Agent | On Failure | Recovery Action |
|-------|------------|-----------------|
| `researcher-codebase` | No patterns found | Proceed with `researcher-external` only |
| `researcher-external` | Search fails | Use cached patterns or escalate |
| `architectureer` | BLOCKED status | Present concerns to user for decision |
| `planning` | BLOCKED status | Request spec clarification from user |
| `tech-debt-investigator` | HIGH debt risk | Suggest refactoring before implementation |
| `code-quality` | Incomplete specs | Return to ORIENT phase |
| `development` | BLOCKED status | Escalate with detailed blockers |
| `code-quality` | BLOCKED status | Require fixes before proceeding |
| `code-quality` | FAIL status | Delegate to `debugger` |
| `debugger` | ESCALATE status | Present to user with full analysis |

### Retry Policy

```python
MAX_RETRIES = 3

def execute_with_retry(task, max_retries=MAX_RETRIES):
    for attempt in range(max_retries):
        result = task()
        if result.status != "BLOCKED":
            return result
        if attempt < max_retries - 1:
            # Modify prompt with previous failure context
            task.prompt = add_failure_context(task.prompt, result)
    return escalate(result)
```

---

## Variable Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `{feature_name}` | Short feature identifier | `user-authentication` |
| `{feature_description}` | Full feature description | `Add JWT-based auth...` |
| `{target_directory}` | Implementation location | `packages/core/auth/` |
| `{target_file}` | Single file path | `packages/core/auth/jwt.py` |
| `{test_file}` | Corresponding test file | `tests/unit/test_jwt.py` |
| `{spec_file}` | Specification document | `docs/01-planning/auth-spec.md` |
| `{tech_stack}` | Technology context | `Python 3.11, FastAPI, UV` |
| `{dependencies}` | Required dependencies | `pyjwt, passlib` |
| `{requirements}` | Feature requirements list | `[req1, req2, ...]` |
