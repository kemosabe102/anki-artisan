# Gauntlet Agents: Architecture & Design Principles

---

This document contains all architectural guidance, design principles, testing strategy, and code review standards for the Gauntlet Agents project.

## System Architecture

### Current: Simplified Design (MVP)

**Thin LLM layer** with code-first workers:

- **Code Workers:** Deterministic functions for data fetching and calculations
- **Single LLM Agent:** ReportWriterAgent for narrative generation only
- **Parallel Execution:** Simple async orchestration with timeouts
- **Direct Function Calls:** No agent-to-agent communication

**Details:** `docs/00-project/SIMPLIFICATION_PLAN.md`

### Future: Complex Multi-Agent System

**Three-layer architecture** (planned enhancement):

1. **LangGraph:** Workflow orchestration and state persistence
2. **A2A Protocol:** Standardized inter-agent communication
3. **Pydantic AI:** Individual agent implementations

**Full specification:** `docs/00-project/SPEC.md` and `docs/02-architecture/ARCHITECTURE.md`

### 🚨 MANDATORY: Technical PM Review for Architecture Changes

**BEFORE making ANY architectural changes, MUST obtain Technical PM approval for:**

#### **Architectural Changes Requiring Technical PM Review:**

- **Component Removal**: Deleting entire modules, classes, or service implementations
- **Interface Changes**: Modifying how components interact with each other
- **Pattern Standardization**: Consolidating multiple implementations into single patterns
- **External Integrations**: Adding external data sources or integrations
- **System Boundaries**: Modifying the worker/agent boundary or orchestration patterns
- **Structural Changes**: Proposing significant structural changes to module organization
- **Technology Decisions**: Evaluating trade-offs between simplicity and features
- **Legacy Code Removal**: Removing deprecated or unused code that might have future usage plans

#### **Required Documentation for Technical PM Review:**

1. **Current State Analysis**:
   - What components/implementations currently exist
   - How each component is used (or if unused)
   - Dependencies and integration points
2. **Proposed Changes**:
   - What will be removed/modified/added
   - Rationale for the architectural decision
   - Impact on existing functionality
3. **Risk Assessment**:
   - Potential breaking changes
   - Migration requirements if needed
   - Functionality that might be lost
4. **Alternative Approaches Considered**:
   - Why this approach was chosen over alternatives
   - Context7 research supporting the decision

#### **Process - Lightweight Architectural Decision Records (ADR)**:

1. **Document Architecture Change** in feature definition document or simple ADR write-up
2. **Research with Context7** for industry best practices
3. **Create Brief ADR** including:
   - Current state and usage analysis
   - Proposed changes with rationale
   - Risk assessment and alternatives considered
   - Context7 research supporting the decision
4. **Present to Technical PM** for lightweight review (not heavyweight bureaucracy)
5. **Obtain Approval** before implementation
6. **Document Decision** in `docs/02-architecture/decisions/` for future reference

**ADR Template**: Use the standardized template at `docs/02-architecture/decisions/adr-template.md` for consistency. See `adr-001-llm-module-consolidation.md` for an example of the template in use.

**Exception**: Minor refactoring within existing patterns doesn't require review, but when in doubt, ask for review.

#### **Retrospective Note - LLM Module Cleanup (2025-08-30)**:

During code review implementation, multiple duplicate Gemini implementations (GeminiClient, GeminiStrategy, GeminiLLMFactory, SimpleLLMService, simple_factory.py) were removed without prior Technical PM review. **✅ Technical PM APPROVED (2025-08-30)**: The consolidation was deemed correct and well-executed, eliminating architectural anti-patterns and technical debt while standardizing on modern pydantic_ai best practices. The cleanup resolved critical event-loop blocking issues and exception contract violations. **Going forward, all architectural changes require Technical PM approval as outlined above, but this decision demonstrated excellent architectural judgment.**

### Directory Structure

```
workers/               # Code-first data workers (quant.py, qual.py)
apps/agent_*/          # LLM agent implementations (intake, quantitative, report_writer)
domain/models/         # Core business models, facts, and state definitions
services/              # Orchestration layer:
  orchestrator/        #   - simple_orchestrator.py (CURRENT: simplified async)
  api/                 #   - orchestrator.py (FUTURE: complex LangGraph)
packages/core/         # Shared utilities (config, llm, qual connectors)
cli/                   # Command-line interface and workflow entry point
tests/                 # Unit, integration, and debug test suites
scripts/               # Development, testing, and deployment automation
prompts/               # LLM prompt templates organized by agent
docs/                  # Documentation organized by category (see 00-project/, 01-architecture/, etc.)
```

### Essential Technologies

- **Python 3.13+:** Async/await for parallel execution
- **Pydantic:** Type-safe data contracts and validation
- **pytest:** Comprehensive testing with markers
- **UV:** Fast package management
- **OpenAI/Gemini:** LLM providers for narrative generation
- **Context7 MCP:** Ultimate source of truth for implementation patterns. If project docs conflict with Context7, follow Context7 and add an item on the todo list to update project docs

**Technical patterns:** `docs/03-implementation/components/state-management-patterns.md`

## Design Principles

### Core Principles (from docs/00-project/SPEC.md)

- **Verifiability**: All outputs must be traceable to source data
- **Transparency**: Agent logic must be explicit, not a black box
- **Conservative Analysis**: Err on caution with low confidence data
- **No Direct Financial Advice**: Only provide analytical outputs, not trading recommendations

### Development Principles

- **Don't Reinvent the Wheel**: Always prefer well-maintained third-party libraries over custom implementations
  - Example: Use `pydantic-settings` instead of custom environment variable loading
  - Example: Use `httpx` instead of custom HTTP client code
  - Example: Use `SQLAlchemy` instead of custom database abstraction
  - Rationale: Reduces maintenance burden, improves reliability, leverages community expertise
  - Exception: Only implement custom solutions when no suitable library exists or when library adds excessive complexity

- **Remove Legacy Code Aggressively**: We are pre-production with no external dependencies
  - Delete unused code immediately - don't comment it out
  - Break backward compatibility freely when improving architecture
  - Remove deprecated patterns as soon as better ones are implemented
  - No need to maintain multiple versions or migration paths
  - Rationale: Clean codebase over compatibility; we can always break things to make them better

**Complete design principles:** `docs/04-guides/code-review/Python Code Review Framework v2.md`

## Testing Strategy

The codebase uses pytest with markers for test categorization:

- `@pytest.mark.unit` - Fast, isolated tests
- `@pytest.mark.integration` - Tests with dependencies
- `@pytest.mark.e2e` - Full workflow tests
- `@pytest.mark.llm` - LLM integration tests

### Test Directory Structure:

- `tests/` - Unit tests (test\_\*.py)
- `tests/integration/` - Integration tests with real APIs and workflows
- `tests/debug/` - Debug and troubleshooting tests

### Test Maintenance Philosophy:

- **Never skip tests** - Either fix them or delete them
- **Broken test = immediate action** - Fix it now or remove it
- **No commented-out tests** - Delete tests that aren't providing value
- **Rationale:** Every test should be green and valuable; skipped tests create false confidence

**Coverage requirement:** 80% minimum

**Complete testing guidelines:** `docs/04-guides/code-review/` testing frameworks

## Code Review Standards [DESIGN-FIRST]

### Mandatory Design Checks

**1. General Code Design Practices**

- [ ] Single Responsibility Principle - each function/class does one thing
- [ ] DRY (Don't Repeat Yourself) - no code duplication
- [ ] Clean interfaces - clear contracts between components
- [ ] Proper error handling - no silent failures
- [ ] Testability - code structured for easy testing

**2. Object-Oriented Design**

- [ ] SOLID principles applied appropriately
- [ ] Composition over inheritance where suitable
- [ ] Proper encapsulation - no leaky abstractions
- [ ] Design patterns used correctly (Factory, Strategy, Observer, etc.)

**3. Dynamic Language Best Practices**

- [ ] Type hints on all functions and methods
- [ ] Pydantic models for data validation
- [ ] Async/await used correctly without blocking
- [ ] Context managers for resource management
- [ ] List comprehensions and generators for efficiency

**4. Python-Specific Standards**

- [ ] PEP 8 compliance (via Ruff)
- [ ] Pythonic idioms (enumerate, zip, unpacking)
- [ ] Proper use of decorators and descriptors
- [ ] No mutable default arguments

**Detailed checklists:** See Design Standards by Category above

## Code Review Feedback Tracking [CONTINUOUS IMPROVEMENT]

### Purpose & Goals

Track code review feedback to identify patterns, eliminate false positives, and systematically improve code quality. This data-driven approach helps us:

- **Identify recurring issues** that need systematic fixes (tooling, documentation, training)
- **Filter false positives** that waste review time
- **Measure improvement** in code quality over time
- **Prioritize quality investments** based on actual feedback trends

### Feedback Collection Process [MANDATORY]

**During Code Review Resolution:**

1. **Log ALL feedback** in `docs/04-guides/code-review/feedback-log.md` using the standard format
2. **Categorize feedback** as: Valid Fix, False Positive, Clarification, or Enhancement
3. **Record resolution** and any systematic changes made
4. **Update prevention measures** if pattern emerges (tools, documentation, process)

**Log Entry Format:**

```markdown
### [YYYY-MM-DD] - [Sprint/Feature Name]

**Reviewer:** [Human/AI]  
**Files:** [file1.py, file2.py]

**Feedback:** [Original feedback text]
**Category:** [Valid Fix | False Positive | Clarification | Enhancement]
**Resolution:** [What was changed/clarified]
**Pattern Notes:** [If recurring issue, note previous occurrences]
**Prevention Action:** [Tool/doc/process change needed, if any]

---
```

### Feedback Categories

**Valid Fix:** Legitimate issue requiring code changes

- Security vulnerabilities, logic errors, performance issues
- Missing error handling, incorrect implementations
- Architectural improvements, testability issues

**False Positive:** Incorrect feedback that doesn't require changes

- Misunderstanding of requirements or existing patterns
- Suggestions that conflict with project architecture
- Style preferences that conflict with established standards

**Clarification:** Request for explanation or documentation

- Code comments, documentation updates
- Clarifying design decisions or trade-offs
- Explaining complex business logic

**Enhancement:** Suggestions for improvement beyond core requirements

- Performance optimizations, code elegance
- Additional features or capabilities
- Better tooling or development experience

### Monthly Review Process

**Every month, analyze feedback log for:**

1. **Most frequent feedback categories** - focus improvement efforts
2. **False positive patterns** - update reviewer guidance
3. **Recurring valid issues** - implement systematic fixes (linting rules, templates, documentation)
4. **Review effectiveness** - measure feedback quality and code improvement trends

**Systematic Improvement Actions:**

- **High-frequency issues** → Add to pre-commit validation pipeline
- **Common false positives** → Update CLAUDE.md reviewer guidance sections
- **Recurring patterns** → Create templates, code generators, or documentation
- **Tool gaps** → Add linting rules, formatters, or static analysis checks

### Integration with Development Workflow

**Pre-Code Review:** Check recent feedback log for common issues in your change type
**During Code Review:** Reference feedback log for context on similar issues  
**Post-Code Review:** ALWAYS update feedback log before marking review complete
**Sprint Retrospective:** Review feedback trends and implement systematic improvements

This continuous improvement cycle ensures code quality improves systematically rather than addressing issues reactively.

## Testability Principles

**Code must be testable from day one:**

- **Dependency Injection:** Pass dependencies as parameters, not hardcoded imports
- **Pure Functions:** Separate I/O from business logic
- **Small Units:** Each function/method should do one thing (SRP)
- **Clear Interfaces:** Use type hints and Pydantic models for contracts

**Development flow:** Implement → Review → Test → Refactor

**Details:** See `docs/04-guides/code-review/` for testability patterns

## Security Implementation

- **Never hardcode secrets** - Use environment variables or secret management
- **Validate all inputs** - Every Pydantic model is a security boundary
- **Structured logging** - JSON with timestamp, level, message for observability
- **No sys.path manipulation** - Use proper package imports

## Operational Boundaries

- Never perform trading actions or give direct financial advice
- Only connect to whitelisted data providers
- Monitor and alert on SLO breaches ($5 cost, 30 min time)
- Require human approval for destructive operations
- Pin all dependencies to specific versions

**Complete operational procedures:** `docs/00-project/PLAYBOOK.md`
