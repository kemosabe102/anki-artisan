# Agent Delegation Patterns for Test Execution

**Category**: development
**Domain**: Multi-agent coordination and delegation decision-making
**Confidence**: 0.93
**Last Updated**: 2025-10-26T00:00:00Z
**Agent**: code-quality

---

## Overview

Test execution failures require intelligent routing to appropriate fix agents based on failure categorization. The code-quality agent uses delegation patterns to coordinate with debugger (application bugs), code-quality (test bugs and flaky tests), code-quality (test quality), and orchestrator (environment issues), ensuring efficient problem resolution.

**Key Concepts**:

- **Delegation Decision Tree**: Algorithmic routing based on failure category
- **Structured Delegation Output**: Standardized format for orchestrator coordination
- **Integration Points**: Coordination protocols with specialized fix agents

---

## Core Frameworks

### Framework 1: Delegation Decision Tree

**Purpose**: Provide algorithmic routing from failure category to appropriate fix agent

**When to Use**:

- After test failure categorization completes
- When generating delegation plan for orchestrator
- During multi-failure batch processing

**Components**:

1. **TEST_BUG → code-quality or self-fix**
   - Simple assertion fixes → self-fix (code-quality capability)
   - Fixture redesign → code-quality
   - Test isolation issues → code-quality
   - Mock configuration → code-quality

2. **APPLICATION_BUG → debugger**
   - Business logic failures → debugger
   - Runtime exceptions in app code → debugger
   - Unexpected behavior → debugger
   - Algorithm errors → debugger

3. **ENVIRONMENT → orchestrator**
   - Missing dependencies → orchestrator (package installation)
   - Configuration issues → orchestrator (config file updates)
   - Database setup → orchestrator (infra coordination)

4. **FLAKY_TEST → code-quality**
   - Timing issues → code-quality (redesign with proper sync)
   - Random data → code-quality (add seeding/mocking)
   - Shared state → code-quality (improve isolation)

**How to Apply**:

1. Receive categorized failures from categorization workflow
2. Apply decision tree to each failure
3. Generate delegation instruction with agent, context, and confidence
4. Group delegations by target agent for batch processing
5. Return delegation plan to orchestrator

**Example from Codebase**:

```python
from typing import Literal, Dict, List
from dataclasses import dataclass

@dataclass
class DelegationInstruction:
    """Structured delegation output for orchestrator."""
    target_agent: Literal["debugger", "code-quality", "orchestrator", "self"]
    failure_category: str
    test_path: str
    context: Dict
    confidence: float
    rationale: str

def generate_delegation_decision(
    failure_category: str,
    failure_details: Dict,
    confidence: float
) -> DelegationInstruction:
    """
    Apply delegation decision tree.

    Args:
        failure_category: TEST_BUG, APPLICATION_BUG, ENVIRONMENT, FLAKY_TEST
        failure_details: Parsed pytest failure information
        confidence: Categorization confidence score

    Returns:
        Delegation instruction for orchestrator
    """
    test_path = failure_details.get("nodeid", "")
    longrepr = failure_details.get("call", {}).get("longrepr", "")

    # Decision tree routing
    if failure_category == "APPLICATION_BUG":
        return DelegationInstruction(
            target_agent="debugger",
            failure_category=failure_category,
            test_path=test_path,
            context={
                "error_message": longrepr,
                "stack_trace": failure_details.get("call", {}).get("traceback", []),
                "function": extract_function_from_trace(failure_details)
            },
            confidence=confidence,
            rationale="Application logic failure requires debugger's hypothesis-driven approach"
        )

    elif failure_category == "TEST_BUG":
        # Check if simple assertion fix
        if is_simple_assertion_fix(failure_details):
            return DelegationInstruction(
                target_agent="self",
                failure_category=failure_category,
                test_path=test_path,
                context={"fix_type": "assertion_update"},
                confidence=0.85,
                rationale="Simple assertion fix can be handled by code-quality"
            )
        else:
            return DelegationInstruction(
                target_agent="code-quality",
                failure_category=failure_category,
                test_path=test_path,
                context={
                    "redesign_needed": True,
                    "indicators": extract_flakiness_indicators(failure_details)
                },
                confidence=confidence,
                rationale="Test redesign requires code-quality expertise"
            )

    elif failure_category == "ENVIRONMENT":
        return DelegationInstruction(
            target_agent="orchestrator",
            failure_category=failure_category,
            test_path=test_path,
            context={
                "missing_dependency": extract_missing_dependency(longrepr),
                "installation_command": generate_install_command(longrepr)
            },
            confidence=confidence,
            rationale="Infrastructure issue requires orchestrator coordination"
        )

    elif failure_category == "FLAKY_TEST":
        return DelegationInstruction(
            target_agent="code-quality",
            failure_category=failure_category,
            test_path=test_path,
            context={
                "flakiness_indicators": extract_flakiness_indicators(failure_details),
                "failure_rate": failure_details.get("failure_rate", 0.0),
                "recommendations": generate_flaky_fix_recommendations(failure_details)
            },
            confidence=confidence,
            rationale="Flaky test requires code-quality redesign for reliability"
        )

    else:
        # Unknown category - escalate
        return DelegationInstruction(
            target_agent="orchestrator",
            failure_category="UNKNOWN",
            test_path=test_path,
            context={"manual_review_required": True},
            confidence=0.0,
            rationale="Unknown failure category requires manual investigation"
        )
```

**Source**: Research synthesis from multi-agent coordination patterns

---

### Framework 2: Structured Delegation Output Format

**Purpose**: Standardize delegation information for orchestrator processing

**When to Use**:

- When returning delegation plan to orchestrator
- When documenting agent coordination protocols
- When validating delegation completeness

**Components**:

1. **delegation_required**: Boolean flag (true if delegation needed)
2. **target_agent**: Agent identifier ("debugger", "code-quality", "orchestrator")
3. **failure_category**: Category from categorization step
4. **confidence**: Delegation confidence score (0.0-1.0)
5. **evidence**: Array of reasoning points supporting delegation
6. **context**: Agent-specific context dictionary

**How to Apply**:

1. Generate DelegationInstruction for each failure
2. Validate all required fields present
3. Calculate delegation confidence (combines categorization confidence + routing confidence)
4. Format as structured output according to schema
5. Return to orchestrator for execution

**Example from Codebase**:

```python
from typing import Dict, List, TypedDict

class DelegationOutput(TypedDict):
    """Structured delegation output schema."""
    delegation_required: bool
    delegations: List[Dict]
    summary: str
    total_failures: int
    delegated_count: int
    self_handled_count: int

def format_delegation_output(
    instructions: List[DelegationInstruction]
) -> DelegationOutput:
    """
    Format delegation instructions for orchestrator.

    Args:
        instructions: List of delegation decisions

    Returns:
        Structured delegation output
    """
    delegations = []
    self_handled = 0

    for instruction in instructions:
        if instruction.target_agent == "self":
            self_handled += 1
            continue

        delegations.append({
            "target_agent": instruction.target_agent,
            "failure_category": instruction.failure_category,
            "test_path": instruction.test_path,
            "confidence": instruction.confidence,
            "evidence": [instruction.rationale],
            "context": instruction.context
        })

    return DelegationOutput(
        delegation_required=len(delegations) > 0,
        delegations=delegations,
        summary=f"{len(delegations)} failures delegated, {self_handled} handled internally",
        total_failures=len(instructions),
        delegated_count=len(delegations),
        self_handled_count=self_handled
    )

# Example output
"""
{
    "delegation_required": true,
    "delegations": [
        {
            "target_agent": "debugger",
            "failure_category": "APPLICATION_BUG",
            "test_path": "tests/unit/test_auth.py::test_login_flow",
            "confidence": 0.85,
            "evidence": [
                "Application logic failure in packages/core/auth.py",
                "RuntimeError indicates unexpected behavior"
            ],
            "context": {
                "error_message": "RuntimeError: Invalid token format",
                "stack_trace": [...],
                "function": "validate_token"
            }
        },
        {
            "target_agent": "code-quality",
            "failure_category": "FLAKY_TEST",
            "test_path": "tests/integration/test_api.py::test_concurrent_requests",
            "confidence": 0.78,
            "evidence": [
                "Failure rate 40% over 5 runs",
                "Timing issues detected: time.sleep(0.5)",
                "No proper async synchronization"
            ],
            "context": {
                "flakiness_indicators": {
                    "timing_issues": ["time.sleep(0.5)"],
                    "random_data": []
                },
                "failure_rate": 0.40,
                "recommendations": [
                    "Remove time.sleep",
                    "Add proper async event waiting",
                    "Mock external API calls"
                ]
            }
        }
    ],
    "summary": "2 failures delegated, 1 handled internally",
    "total_failures": 3,
    "delegated_count": 2,
    "self_handled_count": 1
}
"""
```

**Source**: Base-agent schema standards, code-quality output specification

---

### Framework 3: Integration Points with Specialized Agents

**Purpose**: Define coordination protocols for each agent relationship

**When to Use**:

- When implementing delegation to specific agent
- When validating delegation context completeness
- When troubleshooting delegation failures

**Components**:

**1. debugger Integration**

- **Input Context**: error_message, stack_trace, function, test_path
- **Coordination**: code-quality → debugger → code-quality re-validation
- **Success Criteria**: Test passes after debugger fix
- **Retry Logic**: Max 3 debugger attempts before escalation

**2. code-quality Integration**

- **Input Context**: test_path, redesign_reason, indicators, recommendations
- **Coordination**: code-quality → code-quality → code-quality N-run validation
- **Success Criteria**: Test reliable (failure_rate ≤0.15) after redesign
- **Retry Logic**: Max 2 code-quality attempts before manual review

**3. orchestrator Integration**

- **Input Context**: missing_dependency, installation_command, config_issue
- **Coordination**: code-quality → orchestrator → code-quality re-run
- **Success Criteria**: Environment issue resolved, test passes
- **Retry Logic**: Single orchestrator attempt (infra fixes not retryable)

**How to Apply**:

1. Select integration protocol based on target_agent
2. Extract required context fields for agent
3. Include success criteria in delegation
4. Implement retry logic for transient failures
5. Track delegation outcomes for learning

**Example from Codebase**:

```python
from typing import Optional

class AgentCoordinator:
    """Coordinate code-quality with fix agents."""

    def delegate_to_debugger(
        self,
        test_path: str,
        error_message: str,
        stack_trace: List[str],
        function: str,
        max_retries: int = 3
    ) -> bool:
        """
        Delegate application bug fix to debugger.

        Returns:
            True if fix successful, False otherwise
        """
        for attempt in range(max_retries):
            # Call debugger
            fix_result = debugger.fix_application_bug(
                file=extract_file_from_function(function),
                function=function,
                error_message=error_message,
                stack_trace=stack_trace
            )

            if not fix_result.success:
                continue

            # Re-validate test
            test_result = run_test(test_path)
            if test_result.passed:
                return True

        return False  # Max retries exhausted

    def delegate_to_test_creator(
        self,
        test_path: str,
        redesign_reason: str,
        indicators: Dict,
        recommendations: List[str],
        max_retries: int = 2
    ) -> bool:
        """
        Delegate test redesign to code-quality.

        Returns:
            True if redesign successful and reliable, False otherwise
        """
        for attempt in range(max_retries):
            # Call code-quality
            redesign_result = test_creator.redesign_test(
                test_path=test_path,
                reason=redesign_reason,
                indicators=indicators,
                recommendations=recommendations
            )

            if not redesign_result.success:
                continue

            # Validate with N-run
            failure_rate, _ = validate_test_repeatability(test_path, n_runs=10)
            if failure_rate <= 0.15:
                return True

        return False  # Max retries exhausted

    def delegate_to_orchestrator(
        self,
        test_path: str,
        missing_dependency: Optional[str] = None,
        installation_command: Optional[str] = None
    ) -> bool:
        """
        Escalate environment issue to orchestrator.

        Returns:
            True if environment fixed, False otherwise
        """
        # Single attempt (infra fixes not retryable)
        if missing_dependency:
            fix_result = orchestrator.install_dependency(
                dependency=missing_dependency,
                command=installation_command
            )
        else:
            fix_result = orchestrator.fix_environment_issue(
                test_path=test_path
            )

        if not fix_result.success:
            return False

        # Re-run test
        test_result = run_test(test_path)
        return test_result.passed
```

**Source**: Multi-agent coordination patterns, orchestrator workflow guide

---

## Processes & Workflows

### Workflow 1: End-to-End Delegation Pipeline

**Trigger Conditions**:

- Test failures categorized and ready for delegation
- Delegation plan needs generation

**Steps**:

1. **Receive Categorized Failures**
   - **Input**: List of (failure, category, confidence) tuples
   - **Output**: Validated categorizations
   - **Rationale**: Starting point for delegation decisions

   ```python
   categorized_failures = [
       (failure1, "APPLICATION_BUG", 0.85),
       (failure2, "FLAKY_TEST", 0.78),
       (failure3, "TEST_BUG", 0.90)
   ]
   ```

2. **Apply Delegation Decision Tree**
   - **Input**: Categorized failure
   - **Output**: DelegationInstruction
   - **Rationale**: Route each failure to appropriate agent

   ```python
   instructions = []
   for failure, category, confidence in categorized_failures:
       instruction = generate_delegation_decision(category, failure, confidence)
       instructions.append(instruction)
   ```

3. **Group by Target Agent**
   - **Input**: List of DelegationInstructions
   - **Output**: Grouped delegations by agent
   - **Rationale**: Enable batch processing per agent

   ```python
   grouped = {
       "debugger": [],
       "code-quality": [],
       "orchestrator": [],
       "self": []
   }
   for instruction in instructions:
       grouped[instruction.target_agent].append(instruction)
   ```

4. **Format Delegation Output**
   - **Input**: Grouped instructions
   - **Output**: Structured DelegationOutput
   - **Rationale**: Standardize for orchestrator consumption

   ```python
   delegation_output = format_delegation_output(instructions)
   ```

5. **Execute Self-Handled Fixes**
   - **Input**: Instructions with target_agent="self"
   - **Output**: Fix results
   - **Rationale**: Handle simple fixes without delegation

   ```python
   for instruction in grouped["self"]:
       apply_simple_assertion_fix(instruction)
   ```

6. **Return Delegation Plan**
   - **Input**: DelegationOutput
   - **Output**: JSON response to orchestrator
   - **Rationale**: Enable orchestrator to spawn fix agents
   ```python
   return {
       "status": "SUCCESS",
       "delegation_output": delegation_output
   }
   ```

**Success Criteria**:

- ✅ All failures routed to appropriate agent
- ✅ Delegation output validates against schema
- ✅ Self-handled fixes applied successfully

**Failure Handling**:

- If delegation decision unclear (confidence <0.5), escalate to orchestrator
- If self-fix fails, convert to code-quality delegation
- If grouping fails, delegate individually

**Example Execution**:

```
Input: 5 categorized failures
→ Step 1: Receive → 2 APP_BUG, 1 FLAKY, 1 TEST_BUG, 1 ENV
→ Step 2: Apply tree → 5 DelegationInstructions generated
→ Step 3: Group → {debugger: 2, code-quality: 2, orchestrator: 1}
→ Step 4: Format → DelegationOutput with 5 delegations
→ Step 5: Self-handled → 0 (none marked as self)
→ Step 6: Return → orchestrator receives delegation plan
→ Result: orchestrator spawns 2 debugger + 2 code-quality + 1 orchestrator task
```

---

### Workflow 2: Delegation Execution with Retry Logic

**Trigger Conditions**:

- Orchestrator executes delegation plan
- Agent coordination required

**Steps**:

1. **Select Agent Integration Protocol**
   - **Input**: target_agent from delegation
   - **Output**: Integration function
   - **Rationale**: Use appropriate coordination pattern

   ```python
   if target_agent == "debugger":
       handler = delegate_to_debugger
   elif target_agent == "code-quality":
       handler = delegate_to_test_creator
   ```

2. **Execute Delegation**
   - **Input**: Delegation context
   - **Output**: Fix result
   - **Rationale**: Invoke specialized agent

   ```python
   result = handler(**instruction.context)
   ```

3. **Validate Fix**
   - **Input**: Fix result, test_path
   - **Output**: Validation outcome
   - **Rationale**: Ensure fix actually resolves failure

   ```python
   if target_agent == "debugger":
       validation = run_test(test_path)
   elif target_agent == "code-quality":
       validation = validate_test_repeatability(test_path, n_runs=10)
   ```

4. **Handle Retry Logic**
   - **Input**: Validation outcome, retry count
   - **Output**: Retry decision
   - **Rationale**: Allow transient failures without escalation

   ```python
   if not validation.success and retry_count < max_retries:
       retry_count += 1
       goto step_2()
   elif not validation.success:
       escalate_to_orchestrator()
   ```

5. **Record Outcome**
   - **Input**: Final validation result
   - **Output**: Delegation outcome record
   - **Rationale**: Track success rates for learning
   ```python
   record_delegation_outcome(
       agent=target_agent,
       success=validation.success,
       attempts=retry_count + 1
   )
   ```

**Success Criteria**:

- ✅ Fix validated with test passing
- ✅ Retry logic applied appropriately
- ✅ Outcome recorded for metrics

**Failure Handling**:

- If max retries exhausted, escalate with retry history
- If validation fails unexpectedly, report to user
- If agent unavailable, defer delegation

**Example Execution**:

```
Delegation: debugger for APPLICATION_BUG
→ Step 1: Select → delegate_to_debugger function
→ Step 2: Execute → debugger.fix_application_bug(...)
→ Step 3: Validate → run_test() → FAILED
→ Step 4: Retry → retry_count=1, execute again
→ Step 2: Execute → debugger.fix_application_bug(...) [second attempt]
→ Step 3: Validate → run_test() → PASSED
→ Step 5: Record → success=True, attempts=2
→ Result: Fix successful after 2 attempts
```

---

## Decision Trees

### Decision 1: Agent Selection by Failure Category

```
IF failure_category == "APPLICATION_BUG"
  THEN target_agent = "debugger"
  BECAUSE application logic failures require hypothesis-driven debugging

ELSE IF failure_category == "TEST_BUG"
  THEN analyze_test_bug_type()
    IF simple_assertion_fix
      THEN target_agent = "self"
      BECAUSE code-quality can handle simple assertion updates
    ELSE IF fixture_issue OR test_redesign_needed
      THEN target_agent = "code-quality"
      BECAUSE complex test issues require code-quality expertise

ELSE IF failure_category == "ENVIRONMENT"
  THEN target_agent = "orchestrator"
  BECAUSE infrastructure issues require orchestrator coordination

ELSE IF failure_category == "FLAKY_TEST"
  THEN target_agent = "code-quality"
  BECAUSE flaky tests require test redesign for reliability

ELSE IF failure_category == "UNKNOWN"
  THEN target_agent = "orchestrator"
  ACTION = escalate_for_manual_review()
  BECAUSE unknown failures need human investigation
```

**Example Scenarios**:

1. **Scenario**: APPLICATION_BUG in auth.py with RuntimeError → **Decision**: debugger (app logic debugging)
2. **Scenario**: TEST_BUG with simple assertion mismatch → **Decision**: self (quick fix)
3. **Scenario**: TEST_BUG with fixture scope issue → **Decision**: code-quality (redesign needed)
4. **Scenario**: ENVIRONMENT with ModuleNotFoundError → **Decision**: orchestrator (install dependency)
5. **Scenario**: FLAKY_TEST with 40% failure rate → **Decision**: code-quality (reliability improvement)

---

### Decision 2: Retry Strategy by Agent

```
IF target_agent == "debugger"
  THEN max_retries = 3
  BECAUSE debugger may need multiple hypothesis iterations

ELSE IF target_agent == "code-quality"
  THEN max_retries = 2
  BECAUSE test redesign should succeed in 1-2 attempts

ELSE IF target_agent == "orchestrator"
  THEN max_retries = 1
  BECAUSE infrastructure fixes are not retryable

ELSE IF target_agent == "self"
  THEN max_retries = 1
  BECAUSE simple fixes succeed immediately or delegate
```

**Example Scenarios**:

1. **Scenario**: debugger fix attempt 1 fails → **Decision**: retry (up to 3 attempts)
2. **Scenario**: code-quality redesign attempt 1 fails N-run validation → **Decision**: retry once, then escalate
3. **Scenario**: orchestrator dependency install fails → **Decision**: escalate immediately (infra issues not retryable)

---

### Decision 3: Self-Fix Capability Assessment

```
IF failure_category == "TEST_BUG"
  THEN analyze_fix_complexity()

  IF exception_type == "AssertionError"
      AND assertion_is_simple_equality
      AND fix_is_obvious_value_update
    THEN can_self_fix = True
    BECAUSE simple assertion updates don't require code-quality

  ELSE IF exception_type == "FixtureNotFound"
    THEN can_self_fix = False
    BECAUSE fixture issues require code-quality redesign

  ELSE IF exception_type == "ScopeMismatch"
    THEN can_self_fix = False
    BECAUSE scope issues require code-quality expertise

  ELSE
    THEN can_self_fix = False
    BECAUSE default to delegation for unclear cases
```

**Example Scenarios**:

1. **Scenario**: AssertionError `assert result == 5` but result is 6 → **Decision**: self-fix (update expected value)
2. **Scenario**: FixtureNotFound for missing `auth_client` → **Decision**: delegate to code-quality (fixture design)
3. **Scenario**: AssertionError with complex mock validation → **Decision**: delegate to code-quality (test logic redesign)

---

### Decision 4: ENVIRONMENT Error Handling

**Characteristics**: Missing dependencies, configuration errors, setup failures

**Routing Decision**: Orchestrator escalation (user intervention required)

**Context Provided**:

- Error message with missing dependency/config details
- Recovery suggestions (install commands, config fixes)
- Environment validation commands

**Example Delegation**:

```json
{
  "category": "ENVIRONMENT",
  "next_step": "Environment setup required: Missing pytest dependency. Run 'uv add --dev pytest' to resolve.",
  "priority": "critical",
  "rationale": "Test execution blocked by missing dependency - requires user intervention",
  "affected_tests": ["tests/unit/test_auth.py::test_login"]
}
```

**Recovery Steps**:

1. Parse error message for missing dependency name
2. Suggest installation command (uv add, pip install, etc.)
3. Include environment validation command
4. Escalate to orchestrator for user confirmation

---

### Decision 5: FLAKY_TEST Error Handling

**Characteristics**: Non-deterministic failures, timing-dependent behavior

**Next Step Description**: Fix test isolation and timing dependencies

**Common Fixes**:

- Remove shared state between tests
- Add explicit timeout controls
- Mock time-sensitive functions (datetime.now, random.seed)
- Use fixtures for database state cleanup

**Example Delegation**:

```json
{
  "category": "FLAKY_TEST",
  "next_step": "Fix test isolation and timing dependencies in authentication tests",
  "priority": "high",
  "rationale": "Test shows non-deterministic failures - likely timing or shared state issue",
  "affected_tests": ["tests/unit/test_auth.py::test_session_timeout"],
  "suggested_approach": "Add explicit timeout controls and mock datetime.now calls"
}
```

**Detection Indicators**:

- Test passes/fails inconsistently across runs
- Error messages mention timing, race conditions, or state pollution
- Failures disappear when tests run in isolation
- Different results in different environments

---

## Best Practices

### Practice 1: Confidence-Weighted Delegation

**Principle**: Use categorization confidence to determine delegation aggressiveness

**Implementation**:

- High confidence (≥0.8) → Immediate delegation
- Medium confidence (0.5-0.79) → Delegation with monitoring
- Low confidence (<0.5) → Escalate to orchestrator for manual routing

**Benefits**:

- ✅ Prevents incorrect delegations from low-confidence categorizations
- ✅ Enables monitoring of medium-confidence delegations
- ✅ Maintains system reliability

**Trade-offs**:

- ⚠️ May increase manual review burden
- ⚠️ Requires confidence calibration

**Example**:

```python
# ✅ Correct: Confidence-weighted delegation
category, confidence = categorize_failure(failure)
if confidence >= 0.8:
    delegate_immediately(category, failure)
elif confidence >= 0.5:
    delegate_with_monitoring(category, failure)
else:
    escalate_to_orchestrator(failure, reason="low_confidence_categorization")

# ❌ Wrong: Ignore confidence
category, confidence = categorize_failure(failure)
delegate_immediately(category, failure)  # May be wrong!
```

---

### Practice 2: Batch Delegation by Agent

**Principle**: Group delegations by target agent for efficient parallel execution

**Implementation**:

- Collect all delegation instructions
- Group by target_agent
- Delegate all instances to same agent in single call or parallel tasks
- Aggregate results for unified reporting

**Benefits**:

- ✅ Reduces orchestrator overhead
- ✅ Enables parallel execution optimization
- ✅ Simplifies result aggregation

**Trade-offs**:

- ⚠️ Requires agent to handle batch operations
- ⚠️ May delay urgent fixes waiting for batch

**Example**:

```python
# ✅ Preferred: Batch delegation
grouped = group_by_target_agent(instructions)
results = []
for agent, batch in grouped.items():
    if len(batch) > 1:
        # Batch delegation
        result = delegate_batch(agent, batch)
    else:
        # Single delegation
        result = delegate_single(agent, batch[0])
    results.append(result)

# ❌ Anti-Pattern: Sequential individual delegations
for instruction in instructions:
    delegate_single(instruction.target_agent, instruction)  # Inefficient!
```

---

### Practice 3: Structured Context Preservation

**Principle**: Preserve all relevant failure context when delegating to enable effective fixes

**Implementation**:

- Extract complete failure details from pytest JSON report
- Include error message, stack trace, function, test path
- Add agent-specific context (indicators for code-quality, function for debugger)
- Validate context completeness before delegation

**Benefits**:

- ✅ Fix agents have all information needed
- ✅ Reduces back-and-forth between agents
- ✅ Improves fix success rate

**Trade-offs**:

- ⚠️ Larger delegation payloads
- ⚠️ Requires context extraction logic

**Example**:

```python
# ✅ Preferred: Complete context
delegation = DelegationInstruction(
    target_agent="debugger",
    context={
        "error_message": failure["call"]["longrepr"],
        "stack_trace": failure["call"]["traceback"],
        "function": extract_function_from_trace(failure),
        "test_path": failure["nodeid"],
        "file": extract_file_from_trace(failure)
    },
    ...
)

# ❌ Anti-Pattern: Minimal context
delegation = DelegationInstruction(
    target_agent="debugger",
    context={"error": "Test failed"},  # Not enough info!
    ...
)
```

---

## Anti-Patterns

### Anti-Pattern 1: No Retry Logic for Transient Failures

**Problem**: Treating all delegation failures as permanent when some are transient

**Detection**:

- 🔴 Single delegation attempt without retry
- 🔴 Immediate escalation on first failure
- 🔴 No differentiation between transient and permanent failures

**Consequences**:

- ❌ Valid fixes rejected due to transient issues
- ❌ Increased manual intervention burden
- ❌ Lower fix success rate

**Better Approach**:

```python
✅ Preferred Pattern:
# Retry logic with max attempts
max_retries = 3 if agent == "debugger" else 2
for attempt in range(max_retries):
    result = delegate_to_agent(agent, context)
    if result.success:
        return True
    time.sleep(1)  # Brief delay between retries
return False  # Max retries exhausted

❌ Anti-Pattern:
# No retry logic
result = delegate_to_agent(agent, context)
if not result.success:
    escalate_immediately()  # Give up too soon!
```

**Migration Strategy**:

1. Add retry counters to delegation execution
2. Implement agent-specific max retry counts
3. Add delay between retries
4. Track retry patterns to optimize counts

---

### Anti-Pattern 2: Unclear Delegation Evidence

**Problem**: Delegating without clear reasoning makes debugging delegation failures difficult

**Detection**:

- 🔴 Empty evidence array in delegation output
- 🔴 Generic rationale like "needs fixing"
- 🔴 No traceability from categorization to delegation

**Consequences**:

- ❌ Fix agents lack context for why delegated
- ❌ Difficult to debug wrong delegations
- ❌ Lower user trust in automation

**Better Approach**:

```python
✅ Preferred Pattern:
delegation = DelegationInstruction(
    target_agent="debugger",
    evidence=[
        "Application logic failure in packages/core/auth.py:45",
        "RuntimeError indicates unexpected token format",
        "Stack trace shows failure in validate_token function",
        "Categorization confidence: 0.85"
    ],
    rationale="Application bug requires debugger's hypothesis-driven debugging approach"
)

❌ Anti-Pattern:
delegation = DelegationInstruction(
    target_agent="debugger",
    evidence=[],  # No evidence!
    rationale="needs fixing"  # Too generic!
)
```

**Migration Strategy**:

1. Audit all delegation generation code for evidence collection
2. Add rationale templates per category
3. Include categorization confidence in evidence
4. Validate evidence completeness before delegation

---

## Integration Points

### Integration 1: orchestrator Agent

**Relationship**: code-quality returns delegation plan to orchestrator for execution

**Coordination Pattern**:

- code-quality generates delegation plan with structured output
- orchestrator receives plan and spawns specialized agents in parallel
- orchestrator aggregates fix results and returns to code-quality
- code-quality validates all fixes with final test run

**Example Usage**:

```python
# code-quality generates delegation plan
delegation_output = generate_delegation_plan(categorized_failures)

# Return to orchestrator
return {
    "status": "SUCCESS",
    "agent_specific_output": {
        "delegation_output": delegation_output
    }
}

# orchestrator processes delegation plan
for delegation in delegation_output["delegations"]:
    if delegation["target_agent"] == "debugger":
        Task(agent="debugger", prompt=f"Fix application bug: {delegation['context']}")
    elif delegation["target_agent"] == "code-quality":
        Task(agent="code-quality", prompt=f"Redesign test: {delegation['context']}")

# Aggregate results
all_fixes_successful = all(task.result.success for task in tasks)
```

**Dependencies**:

- orchestrator depends on delegation output schema consistency
- code-quality depends on orchestrator executing delegations
- Both share delegation instruction format

---

### Integration 2: debugger Agent

**Relationship**: code-quality delegates application bug fixes to debugger

**Coordination Pattern**:

- code-quality categorizes failure as APPLICATION_BUG
- code-quality extracts error details and delegates to debugger
- debugger applies hypothesis-driven debugging and fixes app code
- debugger returns to code-quality for re-validation
- code-quality re-runs test to confirm fix

**Example Usage**:

```python
# code-quality delegation
delegation = DelegationInstruction(
    target_agent="debugger",
    context={
        "file": "packages/core/auth.py",
        "function": "validate_token",
        "error_message": "RuntimeError: Invalid token format",
        "stack_trace": [...],
        "test_path": "tests/unit/test_auth.py::test_login_flow"
    }
)

# debugger processing
fix_result = debugger.fix_application_bug(**delegation.context)

# code-quality validation
if fix_result.success:
    validation = run_test(delegation.context["test_path"])
    return validation.passed
```

**Dependencies**:

- debugger depends on complete error context from code-quality
- code-quality depends on debugger's fix quality
- Both share error detail schema

---

### Integration 3: code-quality Agent

**Relationship**: code-quality delegates test redesign to code-quality

**Coordination Pattern**:

- code-quality categorizes failure as TEST_BUG or FLAKY_TEST
- code-quality extracts flakiness indicators and recommendations
- code-quality redesigns test for reliability
- code-quality returns to code-quality for N-run validation
- code-quality validates reliability improvement

**Example Usage**:

```python
# code-quality delegation
delegation = DelegationInstruction(
    target_agent="code-quality",
    context={
        "test_path": "tests/integration/test_api.py::test_concurrent_requests",
        "redesign_reason": "FLAKY_TEST",
        "indicators": {
            "timing_issues": ["time.sleep(0.5)"],
            "random_data": []
        },
        "recommendations": [
            "Remove time.sleep",
            "Add proper async event waiting",
            "Mock external API calls"
        ]
    }
)

# code-quality processing
redesign_result = test_creator.redesign_test(**delegation.context)

# code-quality N-run validation
if redesign_result.success:
    failure_rate, _ = validate_test_repeatability(
        delegation.context["test_path"],
        n_runs=10
    )
    return failure_rate <= 0.15  # Reliable threshold
```

**Dependencies**:

- code-quality depends on indicator accuracy from code-quality
- code-quality depends on code-quality's redesign quality
- Both share indicator schema and recommendation format

---

## Validation & Quality Checks

### Check 1: Delegation Routing Accuracy

**What to Validate**: Failures routed to correct agent based on category

**Validation Method**:

1. Create test dataset of 50+ failures with known correct routing
2. Run delegation decision tree on all failures
3. Compare routing to ground truth
4. Calculate accuracy: `correct_routes / total_failures`

**Pass Criteria**: Routing accuracy ≥95%
**Fail Criteria**: Accuracy <90%

**Remediation**: Review incorrect routes, adjust decision tree logic

---

### Check 2: Context Completeness Validation

**What to Validate**: All delegations include required context fields

**Validation Method**:

1. Generate sample delegations for each target agent
2. Validate context against agent's required fields
3. Check for missing or empty fields

**Pass Criteria**: 100% of delegations have complete context
**Fail Criteria**: Any delegation missing required fields

**Remediation**: Add context extraction logic for missing fields

---

## Common Pitfalls & Solutions

| Pitfall               | Detection                                      | Solution                                                                       |
| --------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------ |
| No retry logic        | Single delegation attempt per failure          | Add agent-specific retry logic (debugger: 3, code-quality: 2, orchestrator: 1) |
| Unclear evidence      | Empty evidence arrays in delegation output     | Add categorization confidence, failure details, and rationale to evidence      |
| Missing context       | Delegations fail due to incomplete information | Validate context completeness before delegation, extract all required fields   |
| Sequential delegation | Processing delegations one at a time           | Group by target agent and delegate in batches for parallel execution           |
| Ignoring confidence   | Using low-confidence categorizations           | Enforce 0.5 confidence threshold, escalate low-confidence to orchestrator      |

---

## Tools & Resources

### Recommended Tools

1. **Task API**
   - **Purpose**: Spawn specialized agents for delegation execution
   - **When to Use**: When orchestrator executes delegation plan
   - **Documentation**: Claude Code API docs

2. **pytest-json-report**
   - **Purpose**: Provides structured failure details for context extraction
   - **When to Use**: All test executions requiring delegation
   - **Documentation**: https://pypi.org/project/pytest-json-report/

### Learning Resources

1. **Multi-Agent Coordination Patterns**: `.claude/docs/orchestrator-workflow.md`
   - **Topic**: Agent coordination, delegation strategies
   - **Quality**: High

2. **Base Agent Schema**: `.claude/docs/schemas/base-agent.schema.json`
   - **Topic**: Standardized agent output format
   - **Quality**: High

---

## Glossary

- **Delegation**: Routing failure to appropriate fix agent with context
- **Delegation Decision Tree**: Algorithm mapping failure category to target agent
- **DelegationInstruction**: Structured data object containing delegation details
- **DelegationOutput**: Standardized format for returning delegation plan to orchestrator
- **Retry Logic**: Allowing multiple fix attempts before escalation
- **Context Preservation**: Including all relevant failure details in delegation

---

## Sources & References

1. Multi-Agent Coordination Patterns: `.claude/docs/orchestrator-workflow.md`
   - Accessed: 2025-10-26
   - Confidence: 0.95

2. Base Agent Schema: `.claude/docs/schemas/base-agent.schema.json`
   - Accessed: 2025-10-26
   - Confidence: 0.95

3. Industry Best Practices - Agent Delegation: Research synthesis
   - Accessed: 2025-10-26
   - Confidence: 0.90

---

## Changelog

- **2025-10-26**: Initial documentation created (confidence: 0.93)

---

## Related Documentation

- `.claude/docs/guides/code-quality/testing-failure-categorization.md`: Failure categorization methodology
- `.claude/docs/guides/code-quality/development-pytest-framework.md`: pytest execution framework
- `.claude/docs/guides/code-quality/testing-flaky-detection.md`: Flaky test detection
- `.claude/docs/orchestrator-workflow.md`: Orchestrator coordination patterns
