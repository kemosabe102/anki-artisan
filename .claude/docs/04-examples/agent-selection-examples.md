# Agent Selection Examples

## Purpose

Detailed scenario examples demonstrating the 7 frameworks from agent-selection-guide.md. Each example includes:

- Scenario description
- Framework application
- Decision rationale
- Alternative considerations

**Reference**: See `.claude/docs/guides/agent-selection-guide.md` for framework principles and quick reference.

---

## Framework 1: Domain-First Thinking - Examples

### Example 1.1: Agent Creation in .claude/agents/

**Scenario**: "Create intent-analyzer agent in `.claude/agents/intent-analyzer.md`"

**Analysis**:

- Keywords present: "create" (could suggest development)
- Domain signal: `.claude/agents/**` path
- **Decision**: claude-code-ecosystem (domain ownership trumps keyword)

**Rationale**: The `.claude/agents/**` directory signals agent lifecycle work, which requires:

- Prompt engineering patterns
- Agent simulation and evaluation
- Anthropic's best practices for agent design
- The 9-criteria quality matrix
- Workflow integration patterns

claude-code-ecosystem has developed expertise in these specific areas through repeated work on agent definitions. development can edit .md files technically, but lacks the domain-specific expertise.

---

### Example 1.2: Claude Code Configuration Update

**Scenario**: "Update output style in `.claude/output-style.md`"

**Analysis**:

- Keywords present: "update" (could suggest development)
- Domain signal: `.claude/**` path (non-agents)
- **Decision**: claude-code (domain ownership)

**Rationale**: Claude Code configuration requires understanding of:

- Claude Code system architecture
- Slash command structure and invocation patterns
- Hook lifecycle and event handling
- Schema validation and structure
- Integration between agents, commands, and hooks

---

### Example 1.3: Payment Processing Implementation

**Scenario**: "Implement payment processing feature in `packages/payments/processor.py`"

**Analysis**:

- Work type: Creation (new functionality)
- Domain: Main codebase (packages/\*\*)
- Agent: development

**Rationale**: Main codebase domain for creation work. development specializes in:

- Implementing features that don't exist yet
- Building new code from specifications
- Adding new capabilities to existing systems
- Writing implementation code for defined requirements

---

### Example 1.4: SPEC.md Creation

**Scenario**: "Create SPEC.md in `docs/01-planning/specifications/feature-x/SPEC.md`"

**Analysis**:

- Keyword: "create" (might suggest development)
- Domain: `docs/**` (documentation domain)
- File pattern: `**/SPEC.md`
- **Decision**: /spec command (specification creation)

**Rationale**: Documentation domain requires:

- Specification structure (SPEC.md format)
- Requirements clarity and testability
- Component breakdown
- Planning metadata (regenerative development)
- Separating HOW from WHAT/WHY

/spec command handles this workflow. development creates code, not specifications.

---

## Framework 2: Work Type Recognition - Examples

### Example 2.1: Creation Work

**Scenario**: "Implement payment processing feature in `packages/payments/processor.py`"

**Analysis**:

- Work type: Creation (new functionality)
- Domain: Main codebase (packages/\*\*)
- Language signals: "implement", "new feature"
- Emphasis on: **newness**, construction
- Agent: development

**Characteristics of Creation Work**:

- Building a feature that doesn't exist yet
- Writing new code from specifications
- Implementing defined requirements
- Adding new capabilities

---

### Example 2.2: Investigation Work

**Scenario**: "Debug why login tests are failing in `tests/auth/test_login.py`"

**Analysis**:

- Work type: Investigation (unknown cause)
- Domain: Main codebase (tests/\*\*)
- Language signals: "debug", "why", "failing"
- Emphasis on: **discovery and understanding**
- Agent: development

**Characteristics of Investigation Work**:

- Discovering root causes of failures
- Understanding why tests aren't passing
- Researching patterns in existing code
- Analyzing why behavior is unexpected

---

### Example 2.3: Improvement Work

**Scenario**: "Refactor auth module to improve separation of concerns in `packages/auth/`"

**Analysis**:

- Work type: Improvement (structural)
- Domain: Main codebase (packages/\*\*)
- Language signals: "refactor", "improve structure"
- Emphasis on: **making existing things better**

**Characteristics of Improvement Work**:

- Restructuring code for better organization
- Optimizing performance
- Improving modularity and separation of concerns
- Refactoring without changing behavior

---

### Example 2.4: Read-Only Analysis Mode - Security Assessment

**Scenario**: "Analyze authentication code for security vulnerabilities"

**Analysis**:

- Domain: `packages/**` (auth code)
- Work Type: Analysis (security assessment)
- Mode: Read-only (no fixes, just report)
- **Decision**: code-quality (security analysis expertise) OR development (pattern analysis) in read-only mode
- **Why not development**: Work type is analysis, not implementation

**Language Signals for Analysis Mode**:

- "analyze", "investigate", "assess", "review", "evaluate"
- "understand patterns", "discover issues", "identify gaps"
- Emphasis on discovery and reporting, NOT making changes

---

### Example 2.5: Read-Only Analysis Mode - Agent Duplication

**Scenario**: "Analyze agent definitions for duplication"

**Analysis**:

- Domain: `.claude/agents/**`
- Work Type: Analysis (duplication detection)
- Mode: Read-only (report findings)
- **Decision**: claude-code-ecosystem (agent domain expert) in read-only mode
- **Why not researcher-codebase**: claude-code-ecosystem has deeper agent-specific expertise

---

### Example 2.6: Read-Only Analysis Mode - Plan Quality

**Scenario**: "Analyze plan quality and completeness"

**Analysis**:

- Domain: `docs/**` plans
- Work Type: Analysis (quality assessment)
- Mode: Read-only review
- **Decision**: planning (business alignment) + architecture (technical quality)
- **Why not planning**: Work type is assessment, not enhancement

---

### Example 2.7: The "Fix" Ambiguity - Unknown Cause

**Scenario**: "Fix failing tests" (root cause unknown)

**Analysis**:

- This is investigation work (need to discover why)
- Agent: development

**Rationale**: Without knowing why tests are failing, this is discovery-based work. development specializes in hypothesis-driven investigation.

---

### Example 2.8: The "Fix" Ambiguity - Known Cause

**Scenario**: "Fix failing tests" (root cause is known: missing null check in LoginService)

**Analysis**:

- This is implementation work (apply known solution)
- Agent: development

**Rationale**: Root cause is specified ("missing null check"). This is straightforward implementation, not investigation.

---

### Example 2.9: Test Work Disambiguation - Create Tests

**Scenario**: "Create tests for new feature"

**Analysis**:

- Writing test code
- Agent: code-quality

**Characteristics**: Test generation, coverage analysis, test design

---

### Example 2.10: Test Work Disambiguation - Run Tests

**Scenario**: "Run tests and report failures"

**Analysis**:

- Executing test suite and analyzing results
- Agent: code-quality

**Characteristics**: Test execution, failure categorization, delegation routing

---

### Example 2.11: Test Work Disambiguation - Fix Failing Tests (Unknown)

**Scenario**: "Fix failing tests" (unknown cause)

**Analysis**:

- Debugging test failures
- Agent: development

**Characteristics**: Root cause discovery, hypothesis testing

---

### Example 2.12: Test Work Disambiguation - Fix Failing Tests (Known)

**Scenario**: "Fix failing tests" (known issue in implementation)

**Analysis**:

- Fixing the code being tested
- Agent: development

**Characteristics**: Apply known fix to implementation code

---

## Framework 3: Agent Expertise Mapping - Examples

### Example 3.1: Anti-Pattern - development for Everything

**Anti-Pattern**: "development can edit any Python file, so use it for everything in packages/\*\*"

**Why It's Wrong**:

- development specializes in **creating new code** (implementation work)
- development specializes in **investigating failures** (discovery work)

Both can technically edit Python files, but their **expertise differs**. development knows implementation patterns but doesn't have development's hypothesis-driven investigation framework.

**Better Approach**: Match work type to expertise specialization.

---

### Example 3.2: Anti-Pattern - File Type Matching

**Anti-Pattern**: "Anyone can edit Markdown files in `.claude/agents/`, so use development"

**Why It's Wrong**:

- Technical capability: Yes, development can edit .md files
- Domain expertise: No, development doesn't have claude-code-ecosystem's understanding of:
  - Prompt engineering patterns
  - Agent simulation and evaluation
  - The 9-criteria quality matrix
  - Workflow integration patterns
  - Anthropic's agent design best practices

**Better Approach**: Don't ask "who can edit this file type?" Ask "who has expertise in this file's domain?"

---

### Example 3.3: claude-code-ecosystem Expertise

**claude-code-ecosystem** has expertise in:

- Prompt engineering (how to structure agent prompts)
- Agent evaluation (the 9-criteria matrix)
- Simulation-driven development
- Agent lifecycle (create → evaluate → update)
- Context7 integration for agent knowledge

**Key Point**: This expertise doesn't transfer to Python implementation or specification writing.

---

### Example 3.4: development Expertise

**development** has expertise in:

- Python implementation patterns
- Code organization in packages/\*\*
- Testing strategies for features
- Integration with existing code
- Pre-flight standards compliance

**Key Point**: This expertise doesn't transfer to agent prompt design or specification structure.

---

### Example 3.5: /spec Command Expertise

**/spec command** has expertise in:

- Specification structure (SPEC.md format)
- Requirements clarity and testability
- Component breakdown
- Planning metadata (regenerative development)
- Separating HOW from WHAT/WHY

**Key Point**: This expertise doesn't transfer to code implementation or agent design.

---

### Example 3.6: Read-Only Research Worker - Authentication Analysis

**Scenario**: "Analyze authentication failure patterns in test suite (READ-ONLY - no fixes)"

**Delegation** (for researcher-lead):

```json
{
  "worker_type": "development",
  "worker_id": "debugger_auth_analysis",
  "specific_objective": "Analyze authentication failure patterns in test suite (READ-ONLY - no fixes)",
  "output_format": "Report: common failure types, frequency, affected test files",
  "tool_guidance": {
    "mode": "read-only",
    "tools": ["Read", "Grep"],
    "exclusions": ["Write", "Edit", "implementation"]
  }
}
```

**Rationale**: development has domain expertise in authentication patterns within `packages/**` and `tests/**`. In read-only mode, they provide targeted analysis without implementing fixes.

---

## Framework 4: Multi-Agent Decision Framework - Examples

### Example 4.1: Sequential Pipeline - Secure Payment Feature

**Scenario**: Creating a secure payment feature

**Pattern**: Sequential pipeline (dependencies between steps)

**Steps**:

1. **researcher-external** - Research OWASP payment security patterns and Stripe SDK best practices (context gathering)
3. **development** - Implement with researched patterns (creation)
4. **code-quality** - Create comprehensive test suite (generation)
5. **code-quality** - Validate test execution (validation)
6. **code-quality** - Security-focused code review (quality gate)

**Why Sequential**: Each step builds on the previous. Can't implement securely without research. Can't test before implementation. Can't review before code exists.

**Recognition Pattern**: Dependencies between steps. Output of step N is input to step N+1.

---

### Example 4.2: Parallel Validation - Implementation Plan Review

**Scenario**: Reviewing an implementation plan

**Pattern**: Parallel validation (independent perspectives)

**Agents** (all review in parallel):

- **planning** - Business alignment, ROI, strategic fit, requirements coverage
- **architecture** - Technical feasibility, NFRs, technology choices, production readiness
- **tech-debt-investigator** - Duplicate detection, cleanup needs, debt implications

**Why Parallel**: Each brings a different lens to the same plan. Reviews are independent—planning doesn't need to wait for architecture.

**Recognition Pattern**: Same input artifact, different evaluation criteria, no dependencies between reviews.

---

### Example 4.3: Research-Then-Act - Caching Implementation

**Scenario**: "Add caching to API endpoints" when unfamiliar with existing caching patterns

**Pattern**: Research-then-act (context gathering before action)

**Steps**:

1. **researcher-codebase** - Discover existing caching patterns in the codebase
2. **development** - Implement using discovered patterns (higher confidence, consistent with existing approach)

**Why Research First**: Without research, development might implement caching differently from existing patterns, creating inconsistency or duplicating utilities.

**Recognition Pattern**:

- Unfamiliar domain or pattern
- Risk of duplicating existing functionality
- Need to understand "how we do this here" before acting

---

### Example 4.4: Single Agent Sufficiency - Simple Test Creation

**Scenario**: "Create unit tests for login feature in `tests/auth/test_login.py`"

**Analysis**:

- Clear domain: tests/\*\*
- Clear work type: test creation
- Clear agent: code-quality
- No need for multi-agent (unless feature is security-critical, then add code-quality after)

**When Single Agent Suffices**:

- Domain is clear and matches agent expertise perfectly
- Task is well-defined with no ambiguity
- Risk is low (not security-critical)
- No cross-domain work involved
- Context is sufficient

---

## Framework 5: Context-Aware Selection - Examples

### Example 5.1: Single-File Assumption Trap

**Anti-Pattern**: Task mentions one file → assume it's a simple one-file change → assign implementation agent directly

**Scenario**: "Change `packages/auth/login.py`"

**Reality Check** - Changing login.py might affect:

- 10 other files that import it
- Test files that verify its behavior
- Config files that reference it
- Other modules that depend on its interface

**The Hidden Complexity**: What looks like a one-file task might have a "context radius" of many related files.

**Decision Framework**:

- **1 file, truly isolated** (utility function, new module):
  - Direct to implementation agent

- **1 file + context of 5-10 related files**:
  - researcher-codebase first (understand dependencies)
  - Then implementation agent with context

- **2-4 files mentioned in task**:
  - researcher-codebase for synthesis (understand relationships)
  - Then implementation agent

- **5+ files mentioned**:
  - researcher-codebase for pattern discovery (find common themes)
  - Possibly multiple implementation agents in parallel

**Why This Matters**: Implementation without context often leads to:

- Breaking existing functionality
- Inconsistent patterns with rest of codebase
- Duplicating utilities that already exist
- Missing edge cases that existing code handles

---

### Example 5.2: Security Context Trigger - Password Reset

**Scenario**: "Implement password reset in `packages/auth/reset.py`"

**High-Risk Domain**: Authentication/Authorization

**Required Pattern**: researcher-external (OWASP/security best practices) → implementation agent → code-quality (security lens)

**Steps**:

1. **researcher-external** - Research OWASP authentication patterns, password reset best practices
2. **development** - Implement with security patterns
3. **code-quality** - Security-focused review

**Why Automatic**: Security mistakes are expensive. Even experienced developers miss security issues. Research establishes the right patterns before writing vulnerable code.

**Key Point**: Even if reset.py is a single new file, the security context requires research-then-implement.

---

### Example 5.3: Context Quality Assessment

**High Context Quality** (can proceed directly):

- Task includes detailed requirements
- Patterns are explicitly specified
- Dependencies are listed
- Examples are provided
- Clear acceptance criteria

**Low Context Quality** (gather context first):

- Task is vague ("improve auth")
- No patterns specified
- Unknown dependencies
- No examples
- Ambiguous success criteria

**Recognition Pattern**: If you're uncertain about approach or scope, context gathering is the first task.

---

## Framework 6: Disambiguation Principles - Examples

### Example 6.1: Domain Ownership - CLAUDE.md Update

**Scenario**: "Update agent list in CLAUDE.md"

**Analysis**:

- Technical capability: Many agents can edit Markdown files
- Domain ownership: CLAUDE.md is Claude Code configuration
- Domain owner: **claude-code**
- **Decision**: claude-code (domain ownership wins)

**Why This Principle**: Domain owners understand:

- The structure and conventions of their domain
- The implications of changes in their domain
- Common pitfalls in their domain
- How their domain integrates with others

---

### Example 6.2: Closest Expertise Match - Bug with Unknown Cause

**Scenario**: "Fix bug in auth.py where login fails with 500 error"

**Agents That Could Technically Do This**:

- development (expertise: investigation, root cause analysis)
- development (expertise: implementation, code writing)

**Analysis**:

- Is root cause known? → No, "login fails with 500 error" doesn't specify why
- Is this investigation work? → Yes, need to discover why
- **Closest expertise**: development (investigation is their specialization)
- **Decision**: development

**Alternative Scenario**: "Fix known bug in auth.py where missing null check causes 500 error"

- Is root cause known? → Yes, "missing null check" is specific
- Is this investigation work? → No, it's straightforward implementation
- **Closest expertise**: development (implementation is their specialization)
- **Decision**: development

**Why This Principle**: The agent whose expertise most closely matches the work type will do the highest quality work in the least time.

---

### Example 6.3: Least Assumptions - Vague Quality Improvement

**Scenario**: "Improve code quality in payment.py"

**What "improve" could mean**:

- Add comments and documentation
- Restructure for better organization
- Fix bugs
- Optimize performance
- Add error handling
- All of the above?

**Agents That Could Handle This**:

- code-quality (assumption: you want feedback on issues)
- development (assumption: you want new code added)
- development (assumption: there are bugs to fix)

**Least Assumptions**:

- **code-quality**: Provides feedback on what could be improved, doesn't change code
- **Others**: All assume a specific type of improvement and make changes

**Decision**: code-quality (least invasive, provides information that clarifies what "improve" means)

**Why This Principle**: Vague tasks benefit from starting with feedback. code-quality's output clarifies what improvements are needed, then you can delegate to the appropriate specialist (development, development) with clear direction.

**Sequential Pattern**: Ambiguous request → code-quality (clarify) → specific agent (implement)

---

### Example 6.4: Combining Principles - Schema Update

**Scenario**: "Update schema validation in `.claude/docs/schemas/agent-schema.json`"

**Check Each Principle**:

1. **Domain Ownership**: `.claude/docs/schemas/**` - Could be claude-code-ecosystem (agent schemas) or claude-code (Claude Code schemas). Let's check further.

2. **Closest Expertise**: "agent-schema.json" specifically → agent schemas → claude-code-ecosystem has deepest expertise in agent-related artifacts

3. **Decision**: claude-code-ecosystem (domain + expertise align)

**No Need for Principles 3 & 4**: Clear answer from domain and expertise.

---

## Framework 7: Anti-Patterns to Avoid - Examples

### Anti-Pattern 1: Default to Most Familiar Agent

**Mistake**: Always choosing development because it's used most often or appears most frequently in task histories.

**Why It's Wrong**:

- Familiarity ≠ Best Fit
- Each agent exists because they bring specialized expertise
- Defaulting to one agent ignores the value of specialization
- Creates the original problem (development overweighting)

**Real Example**: "Review code quality in auth module"

- Familiar choice: development (it does lots of things)
- Right choice: code-quality (specialized in quality review)

**Better Approach**: Let domain and work type guide selection based on expertise match, not habit or frequency of use.

**Self-Check**: "Am I choosing this agent because it's the right expertise, or because it's the one I think of first?"

---

### Anti-Pattern 2: Ignore Domain Boundaries

**Mistake**: Using development for `.claude/agents/**` work because "it can edit Markdown files" or "it writes code and prompts are kind of like code."

**Why It's Wrong**:

- Technical capability (editing .md files) ≠ Domain expertise (agent prompt engineering)
- development hasn't developed claude-code-ecosystem's expertise in:
  - Prompt engineering patterns
  - Agent evaluation criteria
  - Simulation-driven development
  - Anthropic's best practices
- Ignoring boundaries produces lower quality work

**Real Example**: "Create sentiment-analyzer agent in `.claude/agents/sentiment-analyzer.md`"

- Wrong: development (can edit .md files)
- Right: claude-code-ecosystem (domain specialist for agent lifecycle)

**Better Approach**: Domain boundaries are hard boundaries. They exist for a reason. Respect specializations regardless of file format.

**Self-Check**: "Am I choosing based on file type capability, or based on domain expertise?"

---

### Anti-Pattern 3: Single Agent for Cross-Domain Tasks

**Mistake**: "Implement user authentication with tests and documentation" → assign to development for everything.

**Why It's Wrong**:

- Forces one agent to work across multiple domains:
  - `packages/**` (implementation) - development's domain
  - `tests/**` (testing) - code-quality's and code-quality's domain
  - `docs/**` (documentation) - documentation agents' domain
- Each part gets lower quality than using the specialist
- Documentation specialists know specification structure better than development
- code-quality knows test design patterns better than development
- code-quality knows test execution patterns better than development

**Better Approach**: Decompose cross-domain tasks into specialist sequences.

**Correct Decomposition**:

- T001 [code-quality] Create test suite in `tests/auth/`
- T002 [development] Implement authentication in `packages/auth/`
- T003 [code-quality] Validate tests pass
- T004 [code-quality] Security-focused review
- T005 [/spec] Document authentication flow in `docs/auth-spec.md`

**Self-Check**: "Does this task span multiple domains? Should I decompose it?"

---

### Anti-Pattern 4: Keyword Matching Without Context

**Mistake**: Task contains "create" → automatically assign development without considering what's being created or where.

**Why It's Wrong**:

- "Create SPEC.md" and "Create auth.py" both contain "create"
- But they need different specialists:
  - "Create SPEC.md" → /spec command (specification domain)
  - "Create auth.py" → development (main codebase domain)
- Keywords are hints, not rules
- Context (domain, work type) matters more than individual words

**Real Example**: "Create agent evaluation in `.claude/agents/evaluator.md`"

- Keyword: "create" (suggests development)
- Domain: `.claude/agents/**` (agent lifecycle)
- Work type: Agent creation
- **Right choice**: claude-code-ecosystem (domain + work type override keyword)

**Better Approach**:

1. Don't start with keywords
2. Start with domain (Framework 1)
3. Then work type (Framework 2)
4. Keywords can confirm, but domain/work type determine

**Self-Check**: "Am I pattern matching words, or understanding the task's nature?"

---

### Anti-Pattern 5: Ignore Security Context

**Mistake**: Treating authentication, payment processing, or data privacy tasks like any other implementation.

**Why It's Wrong**:

- Security domains have specific patterns and pitfalls
- General implementation agents might not know OWASP guidelines
- Security mistakes are expensive (data breaches, compliance violations, reputation damage)
- "Move fast and break things" doesn't apply to security

**Real Example**: "Implement OAuth login in `packages/auth/oauth.py`"

- Wrong: development alone (might implement insecurely)
- Right: researcher-external (OWASP patterns) → development (secure implementation) → code-quality (security validation)

**Security Domains Requiring Research**:

- Authentication/Authorization
- Payment processing
- Cryptography
- Session management
- Input validation
- Data privacy/PII
- External API keys/secrets

**Better Approach**: Recognize security context → automatically trigger research-then-implement-then-review pattern.

**Self-Check**: "Is this security-sensitive? Do I need research and additional validation?"

---

### Anti-Pattern 6: Assume Simple Based on File Count

**Mistake**: "Only touching one file, so it's simple" → assign directly to implementation agent without context gathering.

**Why It's Wrong**:

- One file might have 20 dependents
- Changing a model file affects all services using it
- Modifying a utility affects all callers
- "Simple" based on file count ≠ simple based on impact

**Real Example**: "Update User model in `packages/models/user.py`"

- Looks simple: one file
- Reality: 15 services import User model
- Impact: Need to understand all usages before changing

**Better Approach**: Even for "one file", ask:

- How many files depend on this?
- What's the impact radius?
- Should I gather context first?

If impact is unclear, start with researcher-codebase.

**Self-Check**: "Am I confusing file count with complexity?"

---

### Anti-Pattern 7: No Default Fallback → Default to development

**Mistake**: "I don't know which agent to use, so I'll default to development since it's versatile."

**Why It's Wrong**:

- This is exactly how development became overweighted
- Defaulting to any agent for ambiguous cases hides the ambiguity
- Forces an agent to work outside their expertise
- Produces lower quality work

**Better Approach**: If agent selection is genuinely ambiguous after applying all frameworks, **mark for manual review** rather than defaulting.

**Return**: "Agent selection ambiguous. Considered agents: X, Y, Z. Disambiguation needed: [specific question]"

**Why This Is Better**:

- Makes ambiguity visible
- Forces clarification of requirements
- Prevents systematic misassignment
- Ensures right agent for the actual (clarified) task

**Self-Check**: "Am I defaulting because I'm certain, or because I don't want to say 'I don't know'?"

---

### Anti-Pattern 8: Orchestrator Direct Execution Instead of Delegation

**Mistake**: Orchestrator executes tasks directly (searches docs, reads files, runs commands) instead of delegating to domain specialist agents.

**Why It's Wrong**:

- Violates the CARDINAL RULE: "Orchestrator orchestrates. DELEGATE EVERYTHING"
- Bypasses domain expertise that specialists provide
- User says "please do X" or "you should do X" → orchestrator misinterprets as "you personally execute this"
- Results in lower quality work compared to specialist agents
- Prevents proper task tracking and multi-agent synthesis

**Root Cause - User Language Misinterpretation**:

User phrases that mean "delegate to agents" (NOT "execute directly"):
- "please do X"
- "you should do X"
- "I need you to do X"
- "do X for me"
- "help me do X"

**Only execute directly when**:
- User explicitly says "don't use agents" or "you handle this directly"
- Task is pure orchestration (spawning agents, synthesizing results)
- No suitable agent exists (confidence <0.5) AND task is trivial (<2 min)

**Real Example**: "Please look at our plugin distribution system and understand how we need to move our plugin exports from services/api to packages/tools"

**Wrong Approach** (Anti-Pattern):
- Orchestrator: Directly searches docs, reads files, runs export commands, validates structure
- Result: Work completed but without specialist expertise or proper coordination

**Right Approach** (Delegation Pattern):
1. **OBSERVE**: Parse request → Multi-step investigation + implementation task
2. **ORIENT**: Context_Quality assessment → Determine research needs
3. **DECIDE**: Select specialists:
   - researcher-codebase (investigate plugin distribution patterns, understand requirements)
   - development (execute export, update imports)
   - code-quality (validate structure, check for issues)
4. **ACT**: Delegate → Track → Synthesize results → Report to user

**Why Delegation Is Better**:
- researcher-codebase: Pattern discovery expertise (10:1 compression, comprehensive analysis)
- development: Implementation patterns (pre-flight validation, error handling)
- code-quality: Quality standards (PEP8, security, maintainability)
- Orchestrator: Synthesis across specialist findings + conflict resolution

**Key Principle**: Domain expertise > task simplicity. Even "simple" multi-step tasks should be delegated if specialists exist for that domain.

**Better Approach**: Apply OODA loop → Calculate confidence scores → Delegate to appropriate specialists → Synthesize results

**Self-Check**: "Am I orchestrating (delegating to specialists) or executing (doing the work myself)?"

---

## Practice Examples

### Example P1: "Fix the failing login tests"

**Apply Frameworks**:

1. **Domain**: `tests/**` (testing domain)

2. **Work Type**: "Fix" + "failing" → Investigation or implementation?
   - Is cause known? Not stated.
   - Assume unknown → Investigation work

3. **Agent Expertise**: development (investigation specialist)

4. **Multi-Agent?**: Not needed initially (can add if debugging reveals implementation issues)

5. **Context**: Test failure output will provide context

6. **Decision**: development

**Alternative Scenario**: "Fix the failing login tests (missing null check in LoginService)"

- Cause is known ("missing null check")
- Work type: Implementation (apply known fix)
- **Decision**: development

---

### Example P2: "Create payment processing feature"

**Apply Frameworks**:

1. **Domain**: `packages/**` (main codebase)

2. **Work Type**: Creation (new feature)

3. **Agent Expertise**: development... but wait

4. **Multi-Agent?**: Check criticality
   - Payment processing → HIGH CRITICALITY
   - Security-sensitive domain
   - **Multi-agent required**

5. **Context**: Need security research

6. **Pattern**: Sequential pipeline
   - researcher-external (OWASP payment patterns, payment SDK best practices)
   - development (secure implementation)
   - code-quality (comprehensive test design)
   - code-quality (test validation)
   - code-quality (security-focused review)

7. **Decision**: Multi-agent sequential pipeline

---

### Example P3: "Update CLAUDE.md with new agent list"

**Apply Frameworks**:

1. **Domain**: `CLAUDE.md` (Claude Code configuration)

2. **Domain Specialist**: claude-code

3. **Work Type**: Update (modification)

4. **Disambiguation**: Could others edit Markdown? Yes, technically
   - **But domain ownership principle**: claude-code owns CLAUDE.md

5. **Decision**: claude-code (domain ownership)

---

### Example P4: "Analyze patterns in authentication code"

**Apply Frameworks**:

1. **Domain**: `packages/**` likely (main codebase)

2. **Work Type**: Investigation (analysis, pattern discovery)

3. **Multi-file?**: Probably (authentication code spans files)

4. **Agent Expertise**: researcher-codebase (pattern discovery specialist)

5. **Context**: This IS context gathering

6. **Decision**: researcher-codebase

**Why not development?**: Work type is investigation, not creation.

**Why not development?**: Not fixing failures, discovering patterns.

---

## Summary

These examples demonstrate the 7 frameworks in action:

1. **Domain-First Thinking** - File location reveals domain
2. **Work Type Recognition** - Creation vs investigation vs analysis
3. **Agent Expertise Mapping** - Domain expertise > technical capability
4. **Multi-Agent Decisions** - Sequential, parallel, or research-then-act
5. **Context-Aware Selection** - Context quality assessment
6. **Disambiguation Principles** - Domain ownership > closest expertise > least assumptions
7. **Anti-Patterns** - Common mistakes to avoid

**Key Takeaway**: Agent selection is about understanding domain, work type, and expertise alignment—not keyword matching or defaults.
