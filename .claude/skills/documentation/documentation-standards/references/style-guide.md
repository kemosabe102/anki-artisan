# Documentation Style Guide

Comprehensive style rules and terminology standards for Gauntlet Agents documentation.

---

## Voice and Tone

### Imperative Voice

Use imperative mood for all instructions and directives.

**CORRECT**:
- "Run the test suite"
- "Install dependencies"
- "Configure the database"
- "Review the output"

**INCORRECT**:
- "You should run the test suite"
- "Dependencies should be installed"
- "The database needs to be configured"
- "Please review the output"

### Active Voice

Prefer active voice for clarity and directness.

**CORRECT**:
- "The agent processes requests"
- "The system validates inputs"
- "The orchestrator delegates tasks"

**INCORRECT**:
- "Requests are processed by the agent"
- "Inputs are validated by the system"
- "Tasks are delegated by the orchestrator"

**EXCEPTIONS** (passive voice acceptable):
- Actor is unknown or irrelevant: "Tokens are consumed during processing"
- Emphasizing the object: "The configuration file is loaded at startup"
- Scientific/technical descriptions: "Data is encrypted using AES-256"

### Present Tense

Use present tense for describing system behavior and facts.

**CORRECT**:
- "The system validates user input"
- "The agent sends requests to the API"
- "The database stores historical data"

**INCORRECT**:
- "The system will validate user input"
- "The agent will send requests to the API"
- "The database will store historical data"

**EXCEPTION**: Use future tense for roadmap items and planned features:
- "Version 2.0 will include multi-region support"

---

## Terminology Glossary

Standardized terms for consistent usage across all documentation.

### Core Concepts

| Term | Use | Avoid |
|------|-----|-------|
| agent | Autonomous task executor | worker, runner, process |
| orchestrator | Main coordination entity | coordinator, manager |
| skill | Reusable domain knowledge module | capability, plugin |
| task | Unit of work | job, action, operation |
| workflow | Multi-step process | pipeline, sequence |

### Technical Terms

| Term | Use | Avoid |
|------|-----|-------|
| API | Application Programming Interface | api, Api |
| database | Lowercase unless proper name | Database, DB |
| PostgreSQL | Proper capitalization | Postgres, postgres, postgresql |
| TimescaleDB | Proper capitalization | Timescale, timescale |
| OODA loop | All caps for acronym | ooda, Ooda |
| Context Quality (CQ) | Use full form first, then abbreviation | context quality score |

### Actions and Operations

| Term | Use | Avoid | Context |
|------|-----|-------|---------|
| delegate | Transfer work to agent | assign, hand off | Orchestrator to agent |
| invoke | Call a skill or function | execute, run | Skill invocation |
| spawn | Create new agent instance | launch, start, create | Agent creation |
| validate | Check correctness | verify, check | Input/output validation |
| verify | Confirm operation success | validate, check | Test verification |

### File and Code References

| Element | Format | Example |
|---------|--------|---------|
| File paths | Backticks, forward slashes | `docs/guides/setup.md` |
| Function names | Backticks with parens | `calculate_score()` |
| Class names | Backticks, PascalCase | `AgentOrchestrator` |
| Variables | Backticks, snake_case | `context_quality` |
| Constants | Backticks, SCREAMING_CASE | `MAX_AGENTS` |
| Commands | Backticks | `uv run pytest` |

---

## Capitalization Rules

### Headings

Use **sentence case** for all headings:
- ✅ "Getting started with agents"
- ❌ "Getting Started With Agents"

**EXCEPTIONS**:
- Proper nouns: "PostgreSQL configuration"
- Acronyms: "API reference guide"
- Code identifiers: "The AgentOrchestrator class"

### Lists

Capitalize first word of each list item:
```markdown
- First item starts with capital
- Second item also capitalized
- Third item continues pattern
```

**EXCEPTION**: List of code elements follows code conventions:
```markdown
- `function_name()` - Calculates the score
- `ClassName` - Handles orchestration
- `CONSTANT_NAME` - Maximum retry count
```

---

## Punctuation

### Oxford Comma

Always use the Oxford comma in lists:
- ✅ "Read, validate, and process the data"
- ❌ "Read, validate and process the data"

### Code Elements

Do NOT use backticks for:
- Emphasis (use **bold** or *italic*)
- URLs or links
- Generic technical terms without specific reference

USE backticks for:
- Specific file paths: `docs/SPEC.md`
- Function/method names: `process_request()`
- Class names: `AgentOrchestrator`
- Variable names: `context_quality`
- Command names: `uv run pytest`

### Periods

Omit periods in list items unless they are complete sentences:
```markdown
- Configure the database
- Run migrations
- Verify the connection works. This ensures everything is set up correctly.
```

---

## Abbreviations and Acronyms

### First Use

Define abbreviations on first use:
- ✅ "Context Quality (CQ) measures domain understanding"
- ❌ "CQ measures domain understanding"

### Common Abbreviations

**OK to use without definition** (project-specific):
- OODA (Observe, Orient, Decide, Act)
- TDD (Test-Driven Development)
- API (Application Programming Interface)
- CI/CD (Continuous Integration/Continuous Deployment)

**Define on first use**:
- ASC (Agent Selection Confidence)
- CQ (Context Quality)
- RCA (Root Cause Analysis)

---

## Examples and Code

### Example Headings

Use descriptive headings that explain what the example demonstrates:

- ✅ "Example: Delegating to multiple agents in parallel"
- ❌ "Example 1"

### Code Comments

Include comments in code examples to explain non-obvious logic:
```python
# Calculate weighted score across multiple dimensions
score = (domain * 0.4) + (pattern * 0.3) + (dependency * 0.2)
```

### Runnable Examples

Provide complete, executable code when possible:
```python
# Complete example with imports
from packages.core.orchestrator import Orchestrator

# Setup
orchestrator = Orchestrator()

# Execute
result = orchestrator.delegate_task(task_id="example")

# Verify
assert result.status == "completed"
```

---

## Writing for Different Audiences

### User Documentation

- Focus on WHAT and HOW
- Use concrete examples
- Minimize jargon
- Include screenshots/diagrams where helpful

### Developer Documentation

- Focus on WHY and WHEN
- Include API references
- Link to source code
- Provide architecture context

### API Reference

- Be concise and precise
- Include all parameters (required/optional)
- Show request and response examples
- List error codes and meanings
