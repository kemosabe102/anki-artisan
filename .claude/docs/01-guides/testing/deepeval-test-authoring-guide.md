---
name: deepeval-test-authoring-guide
description: Guide for writing DeepEval tests for Claude Code agents
date: 2025-12-03
status: ACTIVE
---

# DeepEval Test Authoring Guide

> **Status**: ACTIVE - Validated against DeepEval documentation

## Overview

This guide explains how to write DeepEval tests for evaluating Claude Code agents. DeepEval is an LLM evaluation framework that provides metrics and assertions specifically designed for testing AI/LLM outputs.

### What We Have

| Component | Location | Purpose |
|-----------|----------|---------|
| Metrics Infrastructure | `packages/evaluations/` | Captures test results -> Prometheus -> Grafana |
| Pytest Plugin | `packages/evaluations/pytest_plugin.py` | Auto-instruments tests with OTEL metrics |
| Quality Gates | `scripts/quality_gate_check.py` | Blocks agent creation if quality thresholds fail |
| Dashboards | Grafana @ http://localhost:30030 | Visualize pass rates, quality scores |

### What This Guide Covers

- DeepEval test structure and syntax
- Creating golden test datasets
- Organizing tests by agent
- Quality metrics and assertions

---

## Quick Start

### Step 1: Create a Golden Dataset

Create a JSON file in `tests/evaluations/golden_datasets/<agent-name>/`:

```json
{
  "agent": "development",
  "category": "basic_function",
  "version": "1.0",
  "goldens": [
    {
      "input": "Create a function that returns the sum of two numbers",
      "expected_output": "def add(a: int, b: int) -> int:\n    return a + b",
      "context": ["File: utils/math.py", "Python 3.10+"],
      "additional_metadata": {"difficulty": "easy"}
    }
  ]
}
```

### Step 2: Write a DeepEval Test

Create `tests/evaluations/test_<agent_name>.py`:

```python
import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.metrics import GEval
from tests.evaluations.conftest import load_golden_dataset

# Choose your runner:
# - ClaudeCodeRunner: Test through CLI orchestration
# - SDKAgentRunner: Test code-built agents directly
from tests.evaluations.conftest import ClaudeCodeRunner  # or SDKAgentRunner

class TestMyAgent:
    @pytest.fixture
    def runner(self):
        # For orchestration testing (validates agent selection)
        return ClaudeCodeRunner()
        # OR for direct agent testing:
        # return SDKAgentRunner(agent_fn=my_agent_function, agent_name="my-agent")
    
    @pytest.fixture
    def test_cases(self):
        return load_golden_dataset("development/basic_function.json")
    
    @pytest.mark.deepeval
    def test_basic_function(self, runner, test_cases):
        for golden in test_cases["goldens"]:
            result = runner.run(
                task=golden["input"],
                context=golden["context"],
                expected_agent="development"  # Only for ClaudeCodeRunner
            )
            
            assert result["success"], f"Failed: {result.get('error')}"
            
            # For ClaudeCodeRunner, also verify routing
            if hasattr(runner, 'run') and 'matched_expected' in result:
                assert result["matched_expected"], \
                    f"Wrong agent: {result['agent_used']}"
            
            # Quality metrics apply to both runners
            test_case = LLMTestCase(
                input=golden["input"],
                actual_output=result["response"],
                expected_output=golden.get("expected_output"),
                context=golden["context"]
            )
            
            quality = GEval(
                name="CodeQuality",
                evaluation_steps=[
                    "Check if code is syntactically valid",
                    "Verify function meets requirements"
                ],
                evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
                threshold=0.7
            )
            
            assert_test(test_case, [quality])
```

### Step 3: Run the Test

```bash
# IMPORTANT: Use deepeval CLI, not pytest
DEEPEVAL_METRICS_ENABLED=true uv run deepeval test run tests/evaluations/test_my_agent.py

# With verbose output
DEEPEVAL_METRICS_ENABLED=true uv run deepeval test run tests/evaluations/ -v
```

---

## DeepEval Background

DeepEval provides:
1. **Test Cases** - Input/output pairs with expected behaviors via `LLMTestCase`
2. **Metrics** - Built-in evaluation metrics (faithfulness, relevance, task completion, etc.)
3. **Assertions** - Pass/fail criteria based on metric thresholds
4. **Datasets** - Collections of `Golden` objects for batch evaluation


### Key Concepts

```python
from deepeval import evaluate
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.metrics import AnswerRelevancyMetric, GEval

# A test case represents one evaluation scenario
# NOTE: context must be List[str], not a single string
test_case = LLMTestCase(
    input="What is the capital of France?",
    actual_output="The capital of France is Paris.",
    expected_output="Paris",  # Optional: for comparison metrics
    context=["Geography question", "European capitals"]  # List[str] format
)

# GEval requires evaluation_params using LLMTestCaseParams enum
metric = GEval(
    name="Accuracy",
    evaluation_steps=[
        "Check if the answer correctly identifies the capital city",
        "Verify the response is factually accurate"
    ],
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
    threshold=0.7
)

# Evaluate runs the metrics against test cases
evaluate([test_case], [metric])
```

---

## Test Structure

### Directory Organization

```
tests/
├── evaluations/                    # DeepEval agent tests
│   ├── __init__.py
│   ├── conftest.py                # Shared fixtures, golden data loaders
│   ├── golden_datasets/           # Golden test data by agent
│   │   ├── development/
│   │   │   ├── basic_function.json
│   │   │   ├── error_handling.json
│   │   │   └── refactoring.json
│   │   ├── code-quality/
│   │   │   ├── security_issues.json
│   │   │   └── code_quality.json
│   │   └── debugger/
│   │       ├── simple_bugs.json
│   │       └── complex_bugs.json
│   ├── test_python_code_implementer.py
│   ├── test_python_code_reviewer.py
│   └── test_debugger.py
└── unit/                          # Traditional unit tests
└── integration/                   # Integration tests
```


### Golden Dataset Format

Use DeepEval's native `Golden` structure for test datasets:

**Example** (`golden_datasets/development/basic_function.json`):
```json
{
  "agent": "development",
  "category": "basic_function", 
  "version": "1.0",
  "goldens": [
    {
      "input": "Create a function that calculates factorial of a number. Handle negative numbers and use iteration.",
      "expected_output": "def factorial(n: int) -> int:\n    \"\"\"Calculate factorial using iteration.\"\"\"\n    if n < 0:\n        raise ValueError(\"Factorial not defined for negative numbers\")\n    result = 1\n    for i in range(2, n + 1):\n        result *= i\n    return result",
      "context": ["File: utils/math.py", "Project uses Python 3.10+", "Must include type hints"],
      "additional_metadata": {
        "difficulty": "easy",
        "handles_edge_cases": ["negative input", "zero", "large numbers"],
        "required_patterns": ["input validation", "docstring"]
      }
    }
  ]
}
```

**Key Fields**:
- `input`: The task/prompt given to the agent
- `expected_output`: Reference implementation or expected response
- `context`: List[str] of contextual information (file paths, constraints, etc.)
- `additional_metadata`: Custom fields for test categorization and filtering

---

## Writing DeepEval Tests

### Basic Test Structure

**IMPORTANT**: Use `deepeval test run` instead of `pytest` for DeepEval tests:

```bash
# CORRECT: Use deepeval CLI
deepeval test run tests/evaluations/test_python_code_implementer.py

# WRONG: Do not use pytest directly for DeepEval
# pytest tests/evaluations/
```


```python
# tests/evaluations/test_python_code_implementer.py

import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.metrics import (
    AnswerRelevancyMetric,
    GEval,
    TaskCompletionMetric,
    ToolCorrectnessMetric,
)
from deepeval.tracing import observe, update_current_span

from tests.evaluations.conftest import load_golden_dataset, run_agent


class TestPythonCodeImplementer:
    """DeepEval tests for development agent."""
    
    @pytest.fixture
    def basic_function_cases(self):
        """Load golden test cases for basic function implementation."""
        return load_golden_dataset("development/basic_function.json")
    
    @pytest.mark.deepeval
    def test_creates_valid_function(self, basic_function_cases):
        """Agent should create syntactically valid, working functions."""
        for golden in basic_function_cases["goldens"]:
            # Run the agent with tracing
            actual_output = run_agent(
                agent="development",
                task=golden["input"],
                context=golden["context"]
            )
            
            # Create DeepEval test case
            # NOTE: context must be List[str]
            test_case = LLMTestCase(
                input=golden["input"],
                actual_output=actual_output,
                expected_output=golden.get("expected_output"),
                context=golden["context"],  # Already List[str] from golden
            )
            
            # Define metrics with proper GEval syntax
            relevancy = AnswerRelevancyMetric(threshold=0.7)
            
            # GEval requires evaluation_params with LLMTestCaseParams enum
            code_quality = GEval(
                name="CodeQuality",
                evaluation_steps=[
                    "Check if the code is syntactically valid Python",
                    "Verify proper function structure with docstrings",
                    "Assess adherence to PEP 8 style guidelines",
                    "Check for appropriate error handling"
                ],
                evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
                threshold=0.75
            )
            
            # Assert passes all metrics
            assert_test(test_case, [relevancy, code_quality])
```


### Agent Invocation with Tracing

DeepEval tests need to invoke agents and capture their output. We support two runner types:

| Runner | Use Case | Tests |
|--------|----------|-------|
| `ClaudeCodeRunner` | CLI-based orchestration | Agent selection + execution |
| `SDKAgentRunner` | Code-built agents | Direct agent execution |

---

#### ClaudeCodeRunner (CLI-Based)

Tests through Claude Code CLI, validating orchestration and agent selection:

```python
from deepeval.tracing import observe, update_current_span
from deepeval.metrics import TaskCompletionMetric
import json
import subprocess
import re
from pathlib import Path
from typing import Optional
from abc import ABC, abstractmethod

class BaseAgentRunner(ABC):
    """Abstract base for agent runners."""
    
    @abstractmethod
    def run(self, task: str, context: list[str], **kwargs) -> dict:
        """Execute task and return results."""
        pass

class ClaudeCodeRunner(BaseAgentRunner):
    """
    Run tasks through Claude Code CLI for orchestration testing.
    
    Tests the full pipeline:
    1. Orchestrator receives task
    2. Orchestrator selects agent based on descriptions
    3. Selected agent executes task
    4. Result returned for evaluation
    
    Use this to validate:
    - Agent descriptions trigger correct selection
    - End-to-end orchestration behavior
    - Full pipeline produces expected results
    """
    
    def __init__(self, working_dir: Optional[str] = None, timeout: int = 300):
        self.working_dir = working_dir or str(Path.cwd())
        self.timeout = timeout
    
    @observe(metrics=[TaskCompletionMetric()])
    def run(
        self,
        task: str,
        context: list[str],
        expected_agent: Optional[str] = None
    ) -> dict:
        """
        Execute task through Claude Code orchestrator.
        
        Args:
            task: The task/prompt to execute
            context: List of contextual strings
            expected_agent: Optional - verify this agent was selected
            
        Returns:
            dict with keys:
                - response: str - The agent's output
                - agent_used: str - Which agent was selected
                - matched_expected: bool - Whether expected_agent matched
                - cost: float - API cost
                - duration: float - Execution time
                - success: bool - Whether execution succeeded
        """
        context_str = "\n".join(f"- {c}" for c in context)
        full_prompt = f"""Context:
{context_str}

Task:
{task}

IMPORTANT: At the end of your response, include:
AGENT_USED: <name of the agent that executed this task>"""
        
        cmd = [
            "claude", "-p", full_prompt,
            "--output-format", "json",
            "--verbose"
        ]
        
        try:
            result = subprocess.run(
                cmd, cwd=self.working_dir,
                capture_output=True, text=True,
                timeout=self.timeout, check=True
            )
            
            output = json.loads(result.stdout)
            response_text = output.get("response", result.stdout)
            
            # Extract agent name
            agent_used = None
            match = re.search(r'AGENT_USED:\s*(\S+)', response_text)
            if match:
                agent_used = match.group(1)
            
            update_current_span(
                agent_used=agent_used,
                expected_agent=expected_agent,
                cost=output.get("cost", 0)
            )
            
            return {
                "response": response_text,
                "agent_used": agent_used,
                "matched_expected": (agent_used == expected_agent) if expected_agent else True,
                "cost": output.get("cost", 0),
                "duration": output.get("duration", 0),
                "success": True
            }
            
        except subprocess.TimeoutExpired:
            return {"response": "", "agent_used": None, "matched_expected": False,
                    "cost": 0, "duration": self.timeout, "success": False,
                    "error": f"Timeout after {self.timeout}s"}
        except Exception as e:
            return {"response": "", "agent_used": None, "matched_expected": False,
                    "cost": 0, "duration": 0, "success": False, "error": str(e)}
```

---

#### SDKAgentRunner (Code-Based)

Tests agents built programmatically using Anthropic SDK or custom implementations:

```python
from anthropic import Anthropic
from typing import Callable, Any

class SDKAgentRunner(BaseAgentRunner):
    """
    Run tasks using code-built agents (SDK or custom).
    
    Use this to test:
    - Custom agent implementations
    - Anthropic SDK-based agents
    - Any callable that processes tasks
    
    Example agents:
    - Direct Anthropic API calls
    - LangChain agents
    - Custom agent classes
    """
    
    def __init__(
        self,
        agent_fn: Callable[[str, list[str]], str],
        agent_name: str = "custom-agent"
    ):
        """
        Args:
            agent_fn: Function that takes (task, context) and returns response string
            agent_name: Name for tracing/logging
        """
        self.agent_fn = agent_fn
        self.agent_name = agent_name
    
    @observe(metrics=[TaskCompletionMetric()])
    def run(
        self,
        task: str,
        context: list[str],
        **kwargs
    ) -> dict:
        """
        Execute task using the provided agent function.
        
        Args:
            task: The task/prompt to execute
            context: List of contextual strings
            
        Returns:
            dict with keys:
                - response: str - The agent's output
                - agent_used: str - The agent name
                - success: bool - Whether execution succeeded
        """
        try:
            response = self.agent_fn(task, context)
            
            update_current_span(agent_name=self.agent_name)
            
            return {
                "response": response,
                "agent_used": self.agent_name,
                "matched_expected": True,  # N/A for direct agents
                "success": True
            }
        except Exception as e:
            return {
                "response": "",
                "agent_used": self.agent_name,
                "matched_expected": False,
                "success": False,
                "error": str(e)
            }


# Example: Anthropic SDK agent
def create_anthropic_agent(system_prompt: str, model: str = "claude-sonnet-4-20250514"):
    """Factory to create an Anthropic SDK-based agent function."""
    client = Anthropic()
    
    def agent_fn(task: str, context: list[str]) -> str:
        context_str = "\n".join(context)
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": f"Context:\n{context_str}\n\nTask:\n{task}"
            }]
        )
        return response.content[0].text
    
    return agent_fn


# Example: Custom agent class wrapper
def wrap_agent_class(agent_instance: Any, method_name: str = "execute"):
    """Wrap an agent class instance as a callable."""
    def agent_fn(task: str, context: list[str]) -> str:
        method = getattr(agent_instance, method_name)
        return method(task=task, context=context)
    return agent_fn
```

---

#### Choosing a Runner

| Scenario | Runner | Why |
|----------|--------|-----|
| Test orchestrator agent selection | `ClaudeCodeRunner` | Validates routing logic |
| Test agent description quality | `ClaudeCodeRunner` | Reveals if descriptions need improvement |
| Test custom Python agent | `SDKAgentRunner` | Direct execution, no CLI overhead |
| Test Anthropic SDK agent | `SDKAgentRunner` | Direct API calls |
| Test LangChain/custom framework | `SDKAgentRunner` | Wrap with `agent_fn` |
| CI/CD pipeline (fast) | `SDKAgentRunner` | Lower latency, no CLI spawn |
| CI/CD pipeline (full validation) | `ClaudeCodeRunner` | Complete orchestration test |

---

#### RunnerFactory (Simplified Creation)

Use the Factory pattern to simplify runner instantiation:

```python
from enum import Enum
from typing import Optional, Callable

class RunnerType(Enum):
    """Available runner types."""
    CLI = "cli"           # ClaudeCodeRunner - orchestration testing
    SDK = "sdk"           # SDKAgentRunner - direct agent testing
    ANTHROPIC = "anthropic"  # Pre-configured Anthropic SDK agent

class RunnerFactory:
    """
    Factory for creating agent runners.
    
    Simplifies runner creation by abstracting configuration details.
    Follows the Factory design pattern for extensibility.
    
    Example:
        # Simple creation
        runner = RunnerFactory.create(RunnerType.CLI)
        
        # With configuration
        runner = RunnerFactory.create(
            RunnerType.SDK,
            agent_fn=my_custom_agent,
            agent_name="my-agent"
        )
    """
    
    @staticmethod
    def create(
        runner_type: RunnerType,
        *,
        # CLI runner options
        working_dir: Optional[str] = None,
        timeout: int = 300,
        # SDK runner options
        agent_fn: Optional[Callable[[str, list[str]], str]] = None,
        agent_name: str = "custom-agent",
        # Anthropic runner options
        system_prompt: Optional[str] = None,
        model: str = "claude-sonnet-4-20250514"
    ) -> BaseAgentRunner:
        """
        Create a runner instance based on type.
        
        Args:
            runner_type: Type of runner to create
            working_dir: Working directory (CLI only)
            timeout: Execution timeout in seconds (CLI only)
            agent_fn: Agent function (SDK only)
            agent_name: Name for tracing (SDK only)
            system_prompt: System prompt (Anthropic only)
            model: Model to use (Anthropic only)
            
        Returns:
            Configured runner instance
            
        Raises:
            ValueError: If required parameters are missing
        """
        if runner_type == RunnerType.CLI:
            return ClaudeCodeRunner(
                working_dir=working_dir,
                timeout=timeout
            )
        
        elif runner_type == RunnerType.SDK:
            if agent_fn is None:
                raise ValueError("SDK runner requires agent_fn parameter")
            return SDKAgentRunner(
                agent_fn=agent_fn,
                agent_name=agent_name
            )
        
        elif runner_type == RunnerType.ANTHROPIC:
            if system_prompt is None:
                raise ValueError("Anthropic runner requires system_prompt parameter")
            agent_fn = create_anthropic_agent(
                system_prompt=system_prompt,
                model=model
            )
            return SDKAgentRunner(
                agent_fn=agent_fn,
                agent_name=f"anthropic-{model.split('-')[1]}"
            )
        
        else:
            raise ValueError(f"Unknown runner type: {runner_type}")


# Usage in tests with fixtures
class TestWithFactory:
    @pytest.fixture
    def runner(self):
        """Create runner using factory."""
        return RunnerFactory.create(RunnerType.CLI)
    
    @pytest.fixture
    def fast_runner(self):
        """Create SDK runner for faster tests."""
        return RunnerFactory.create(
            RunnerType.ANTHROPIC,
            system_prompt="You are a Python expert.",
            model="claude-sonnet-4-20250514"
        )
```

---

#### Adapter Pattern (Third-Party Integration)

Use the Adapter pattern to integrate third-party runners or frameworks:

```python
from typing import Protocol

class AgentRunnerProtocol(Protocol):
    """Protocol defining the runner interface for type checking."""
    
    def run(self, task: str, context: list[str], **kwargs) -> dict:
        """Execute task and return results."""
        ...


class LangChainAgentAdapter(BaseAgentRunner):
    """
    Adapter for LangChain agents.
    
    Wraps a LangChain agent to conform to our BaseAgentRunner interface.
    Follows the Adapter design pattern for third-party integration.
    
    Example:
        from langchain.agents import AgentExecutor
        
        langchain_agent = AgentExecutor(...)
        runner = LangChainAgentAdapter(langchain_agent)
        result = runner.run(task="...", context=[...])
    """
    
    def __init__(self, langchain_agent, agent_name: str = "langchain-agent"):
        """
        Args:
            langchain_agent: LangChain AgentExecutor instance
            agent_name: Name for tracing/logging
        """
        self.langchain_agent = langchain_agent
        self.agent_name = agent_name
    
    def run(self, task: str, context: list[str], **kwargs) -> dict:
        """
        Execute task using LangChain agent.
        
        Adapts LangChain's invoke() API to our standard interface.
        """
        try:
            # LangChain uses different input format
            context_str = "\n".join(context)
            langchain_input = {
                "input": f"Context:\n{context_str}\n\nTask:\n{task}"
            }
            
            # LangChain returns dict with 'output' key
            result = self.langchain_agent.invoke(langchain_input)
            
            return {
                "response": result.get("output", str(result)),
                "agent_used": self.agent_name,
                "matched_expected": True,
                "success": True
            }
        except Exception as e:
            return {
                "response": "",
                "agent_used": self.agent_name,
                "matched_expected": False,
                "success": False,
                "error": str(e)
            }


class CrewAIAgentAdapter(BaseAgentRunner):
    """
    Adapter for CrewAI agents.
    
    Example:
        from crewai import Crew
        
        crew = Crew(agents=[...], tasks=[...])
        runner = CrewAIAgentAdapter(crew)
    """
    
    def __init__(self, crew, agent_name: str = "crewai-agent"):
        self.crew = crew
        self.agent_name = agent_name
    
    def run(self, task: str, context: list[str], **kwargs) -> dict:
        """Execute task using CrewAI."""
        try:
            # CrewAI uses kickoff() method
            result = self.crew.kickoff(inputs={
                "task": task,
                "context": context
            })
            
            return {
                "response": str(result),
                "agent_used": self.agent_name,
                "matched_expected": True,
                "success": True
            }
        except Exception as e:
            return {
                "response": "",
                "agent_used": self.agent_name,
                "matched_expected": False,
                "success": False,
                "error": str(e)
            }


# Register adapters with factory
class ExtendedRunnerFactory(RunnerFactory):
    """Extended factory with third-party adapter support."""
    
    _adapters: dict = {}
    
    @classmethod
    def register_adapter(cls, name: str, adapter_class: type):
        """Register a third-party adapter."""
        cls._adapters[name] = adapter_class
    
    @classmethod
    def create_adapter(cls, name: str, agent_instance, **kwargs) -> BaseAgentRunner:
        """Create an adapter instance."""
        if name not in cls._adapters:
            raise ValueError(f"Unknown adapter: {name}. Registered: {list(cls._adapters.keys())}")
        return cls._adapters[name](agent_instance, **kwargs)


# Register adapters
ExtendedRunnerFactory.register_adapter("langchain", LangChainAgentAdapter)
ExtendedRunnerFactory.register_adapter("crewai", CrewAIAgentAdapter)

# Usage
# runner = ExtendedRunnerFactory.create_adapter("langchain", my_langchain_agent)
```

---

#### Architecture Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DUAL RUNNER ARCHITECTURE                              │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────────┐
                              │  RunnerFactory   │  ◀── Factory Pattern
                              │  (simplified     │
                              │   creation)      │
                              └────────┬─────────┘
                                       │
                                       ▼
                         ┌─────────────────────────┐
                         │    BaseAgentRunner      │  ◀── Strategy Pattern
                         │    (abstract base)      │      (common interface)
                         └────────────┬────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              │                       │                       │
              ▼                       ▼                       ▼
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │ ClaudeCodeRunner│    │  SDKAgentRunner │    │  *Adapter*      │  ◀── Adapter
    │ (CLI-based)     │    │  (code-based)   │    │  (3rd party)    │      Pattern
    └─────────────────┘    └─────────────────┘    └─────────────────┘
           │                       │                       │
           ▼                       ▼                       ▼
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │ Orchestration   │    │ Direct agent    │    │ LangChain,      │
    │ + agent select  │    │ execution       │    │ CrewAI, etc.    │
    └─────────────────┘    └─────────────────┘    └─────────────────┘

Design Patterns Used:
• Strategy Pattern: BaseAgentRunner defines interchangeable algorithms
• Factory Pattern: RunnerFactory simplifies object creation
• Adapter Pattern: Wraps third-party agents to conform to interface
• Dependency Injection: Runners injected via pytest fixtures
```

### Testing Agent Selection (ClaudeCodeRunner)

Use `ClaudeCodeRunner` to validate orchestrator routing:

```python
import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.metrics import GEval
from tests.evaluations.conftest import ClaudeCodeRunner

class TestAgentSelection:
    """Validate orchestrator routes tasks to correct agents."""
    
    @pytest.fixture
    def runner(self):
        return ClaudeCodeRunner(working_dir="C:/Users/kemos/Repos/gauntlet-agents")
    
    @pytest.mark.deepeval
    def test_implementation_routes_correctly(self, runner):
        """Implementation tasks should route to development."""
        result = runner.run(
            task="Create a function that validates email addresses",
            context=["File: utils/validators.py", "Python 3.10+"],
            expected_agent="development"
        )
        
        assert result["success"], f"Execution failed: {result.get('error')}"
        assert result["matched_expected"], \
            f"Expected development, got {result['agent_used']}"
```

### Testing Code-Built Agents (SDKAgentRunner)

Use `SDKAgentRunner` to test agents you build in code:

```python
from tests.evaluations.conftest import SDKAgentRunner, create_anthropic_agent

class TestCustomAgent:
    """Test a custom code-built agent."""
    
    @pytest.fixture
    def runner(self):
        # Create agent with custom system prompt
        agent_fn = create_anthropic_agent(
            system_prompt="You are a Python code generator. Return only valid Python code.",
            model="claude-sonnet-4-20250514"
        )
        return SDKAgentRunner(agent_fn=agent_fn, agent_name="python-generator")
    
    @pytest.mark.deepeval
    def test_generates_valid_code(self, runner):
        """Agent should generate syntactically valid Python."""
        result = runner.run(
            task="Create a function that calculates factorial",
            context=["Use iteration, not recursion", "Include type hints"]
        )
        
        assert result["success"], f"Execution failed: {result.get('error')}"
        
        test_case = LLMTestCase(
            input="Create a function that calculates factorial",
            actual_output=result["response"],
            context=["Use iteration", "Include type hints"]
        )
        
        code_quality = GEval(
            name="CodeQuality",
            evaluation_steps=[
                "Check if output contains valid Python function",
                "Verify factorial logic is present",
                "Check for type hints"
            ],
            evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
            threshold=0.7
        )
        
        assert_test(test_case, [code_quality])
```

**When Agent Selection Fails**

If `matched_expected` is `False`, it indicates the agent's description needs improvement:

1. Check `.claude/agents/<agent-name>.md` description section
2. Look for ambiguous language that could match other agents
3. Add more specific trigger keywords
4. Consider the orchestrator's ASC (Agent Selection Confidence) calculation

Example fix for poor routing:
```markdown
# Before (too generic)
description: "Handles Python code tasks"

# After (specific triggers)
description: "Implements new Python functions, classes, and modules. Use for: create function, add feature, implement module, write code. NOT for: reviewing existing code, debugging, testing."
```

### Testing Different Scenarios

**Scenario categories by agent type:**

| Agent Type | Scenario Categories |
|------------|---------------------|
| development | Basic functions, Classes, Error handling, Async code, Refactoring |
| code-quality | Security issues, Performance, Code style, Best practices, Edge cases |
| debugger | Syntax errors, Logic bugs, Runtime errors, Integration issues |
| code-quality | Unit tests, Integration tests, Edge case coverage, Mocking |


### Quality Metrics

**Metric mapping for agent evaluation:**

| Our Metric | DeepEval Equivalent | Description |
|------------|---------------------|-------------|
| `task_completion` | `TaskCompletionMetric` | Whether agent completed the assigned task |
| `tool_correctness` | `ToolCorrectnessMetric` | Validates correct tool usage by agents |
| `code_quality_score` | `GEval` with custom evaluation_steps | Overall code quality assessment |
| `error_handling_score` | `GEval` with error handling steps | Proper exception handling |
| `efficiency_score` | `GEval` with efficiency steps | Code performance/efficiency |
| `pass_rate_percent` | Built-in pass/fail aggregation | Test pass rate |

**Example GEval configurations:**

```python
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams

# Code quality metric
code_quality = GEval(
    name="CodeQuality",
    evaluation_steps=[
        "Check if the code is syntactically valid Python",
        "Verify proper function structure with docstrings",
        "Assess adherence to PEP 8 style guidelines",
        "Check for appropriate error handling"
    ],
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
    threshold=0.75
)

# Error handling metric
error_handling = GEval(
    name="ErrorHandling",
    evaluation_steps=[
        "Check for try/except blocks around risky operations",
        "Verify specific exception types are caught (not bare except)",
        "Assess error messages for clarity and helpfulness",
        "Check for proper cleanup in finally blocks if needed"
    ],
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
    threshold=0.70
)


# Efficiency metric
efficiency = GEval(
    name="Efficiency",
    evaluation_steps=[
        "Check for appropriate algorithm complexity",
        "Verify no unnecessary loops or redundant operations",
        "Assess memory usage patterns",
        "Check for proper use of generators/iterators where appropriate"
    ],
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
    threshold=0.70
)
```

### Complete `run_agent()` Implementation

The following implementation tests through Claude Code's orchestrator to validate both agent selection and task execution:

```python
import json
import subprocess
import re
from pathlib import Path
from typing import Optional

def run_agent(
    task: str,
    context: list[str],
    expected_agent: Optional[str] = None,
    timeout: int = 300
) -> dict:
    """
    Execute a task through Claude Code orchestrator for DeepEval testing.
    
    This tests the FULL orchestration pipeline:
    1. Orchestrator analyzes the task
    2. Orchestrator selects agent based on descriptions in .claude/agents/
    3. Selected agent executes the task
    4. Response returned for metric evaluation
    
    Args:
        task: The task/prompt to execute
        context: List of contextual strings (file paths, constraints)
        expected_agent: Optional agent name - validates correct routing
        timeout: Timeout in seconds. Default: 300
        
    Returns:
        dict containing:
            - response (str): The agent's output text
            - agent_used (str): Which agent the orchestrator selected
            - matched_expected (bool): Whether expected_agent matched actual
            - cost (float): API cost for the execution
            - duration (float): Execution time in seconds
            - success (bool): Whether execution completed without error
            
    Raises:
        TimeoutError: If execution exceeds timeout
        RuntimeError: If Claude Code CLI fails
        
    Example:
        >>> result = run_agent(
        ...     task="Create a function that calculates factorial",
        ...     context=["File: utils/math.py", "Python 3.10+"],
        ...     expected_agent="development"
        ... )
        >>> assert result["matched_expected"], f"Wrong agent: {result['agent_used']}"
        >>> assert "def factorial" in result["response"]
    """
    # Default to repo root
    working_dir = str(Path(__file__).parent.parent.parent.parent.parent)
    
    # Build context-enhanced prompt
    context_str = "\n".join(f"- {c}" for c in context)
    full_prompt = f"""Context:
{context_str}

Task:
{task}

IMPORTANT: Include at the end of your response:
AGENT_USED: <the agent name that executed this task>"""
    
    cmd = [
        "claude",
        "-p", full_prompt,
        "--output-format", "json",
        "--verbose"
    ]
    
    try:
        result = subprocess.run(
            cmd,
            cwd=working_dir,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True
        )
        
        output = json.loads(result.stdout)
        response_text = output.get("response", result.stdout)
        
        # Extract agent name from response
        agent_used = None
        agent_match = re.search(r'AGENT_USED:\s*(\S+)', response_text)
        if agent_match:
            agent_used = agent_match.group(1)
        
        return {
            "response": response_text,
            "agent_used": agent_used,
            "matched_expected": (agent_used == expected_agent) if expected_agent else True,
            "cost": output.get("cost", 0),
            "duration": output.get("duration", 0),
            "success": True
        }
        
    except subprocess.TimeoutExpired as e:
        raise TimeoutError(f"Orchestrator execution exceeded {timeout}s") from e
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Claude Code CLI failed (exit {e.returncode}): {e.stderr}") from e
    except json.JSONDecodeError:
        # Fall back if JSON parsing fails
        return {
            "response": result.stdout,
            "agent_used": None,
            "matched_expected": False,
            "cost": 0,
            "duration": 0,
            "success": True
        }
```

---

## Test Structure Best Practices

### Dataset Patterns

**EvaluationDataset with Goldens** (recommended for production):

```python
from deepeval.dataset import EvaluationDataset, Golden

dataset = EvaluationDataset(goldens=[
    Golden(
        input="What is your refund policy?",
        expected_output="30-day full refund",
        context=["Policy: 30-day full refund, no questions"]
    )
])

# Iterate with automatic metric application
for golden in dataset.evals_iterator():
    result = your_agent(golden.input)
```

**Conversational Goldens** (for multi-turn agents):

```python
from deepeval.dataset import ConversationalGolden, EvaluationDataset

dataset = EvaluationDataset(goldens=[
    ConversationalGolden(scenario="User asking for help with error message")
])
```

### Metric Selection Guide

| Use Case | Recommended Metrics |
|----------|---------------------|
| Code generation | `GEval(name="CodeQuality", ...)` + `TaskCompletionMetric` |
| RAG/retrieval | `FaithfulnessMetric`, `ContextualRelevancyMetric`, `ContextualRecallMetric` |
| Conversational | `AnswerRelevancyMetric`, `ConversationRelevancyMetric` |
| Safety/compliance | Custom `GEval` with safety-focused steps |

### GEval Writing Tips

1. **Use `evaluation_steps` for complex criteria** (not `criteria`):
   ```python
   GEval(
       name="SecurityAudit",
       evaluation_steps=[
           "Check for SQL injection vulnerabilities",
           "Verify input validation is present",
           "Assess error handling for security leaks"
       ],
       evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
       threshold=0.8
   )
   ```

2. **Be specific in steps** - vague steps produce inconsistent scores

3. **Include negative checks** - "Penalize if X is missing" helps calibration

### Parallel Execution

```bash
# Run with 4 parallel processes for faster CI
deepeval test run tests/evaluations/ -n 4
```

---

## Running DeepEval Tests

### Local Execution

```bash
# Run all DeepEval tests (use deepeval CLI, not pytest)
DEEPEVAL_METRICS_ENABLED=true uv run deepeval test run tests/evaluations/

# Run tests for specific agent
DEEPEVAL_METRICS_ENABLED=true uv run deepeval test run tests/evaluations/test_python_code_implementer.py

# Run with verbose output
DEEPEVAL_METRICS_ENABLED=true uv run deepeval test run tests/evaluations/ -v
```

### Viewing Results

1. **Console**: DeepEval CLI output shows pass/fail with metric scores
2. **Grafana Dashboard**: http://localhost:30030/d/deepeval-metrics
3. **Quality Gate Check**: `uv run python scripts/quality_gate_check.py`
4. **Confident AI Dashboard**: If configured, results sync to confident-ai.com

---

## Test Case Count Recommendations

The number of test cases depends on agent complexity:

| Agent Complexity | Test Cases per Category | Total Recommended |
|------------------|------------------------|-------------------|
| Simple agents | 15-30 | Start under 100 |
| Medium complexity | 30-50 | 100-250 |
| Complex agents | 50-100+ | 250-500+ |

**Guidelines**:
- Start with under 100 total test cases
- Expand based on coverage gaps identified during testing
- Focus on edge cases and failure modes
- Prioritize scenarios that have caused issues in production


---

## Creating Golden Test Datasets

### Recommended Approach: Hybrid

Use a combination of approaches for comprehensive coverage:

1. **Manual Curation** (Core scenarios)
   - Developers create test cases based on real agent interactions
   - High quality, targeted scenarios
   - Use for critical paths and known edge cases

2. **Synthetic Generation** (Edge cases)
   - Use LLM to generate diverse test cases
   - Human review and curation required
   - Scalable for expanding coverage

3. **Production Sampling** (Validation)
   - Sample real agent interactions from production logs
   - Anonymize and curate for test datasets
   - Validates synthetic tests against real usage

### Golden Dataset Versioning

Store datasets with version directories for baseline management:

```
golden_datasets/
├── development/
│   ├── v1/                    # Initial baseline
│   │   └── basic_function.json
│   └── v2/                    # After improvements
│       └── basic_function.json
```

---

## Resolved Questions

### RESOLVED: DeepEval API and Pytest Integration

**Q**: What's the actual pytest integration syntax?
**A**: Use `deepeval test run` CLI instead of `pytest`. The DeepEval CLI provides proper metric collection and reporting.

```bash
# Correct
deepeval test run tests/evaluations/

# Incorrect
pytest tests/evaluations/
```


### RESOLVED: GEval Syntax Requirements

**Q**: How do we create custom GEval criteria for our quality scores?
**A**: GEval requires `evaluation_params` using the `LLMTestCaseParams` enum:

```python
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams

code_quality = GEval(
    name="CodeQuality",
    evaluation_steps=[
        "Check if the code is syntactically valid Python",
        "Verify proper function structure with docstrings"
    ],
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],  # REQUIRED
    threshold=0.75
)
```

### RESOLVED: LLMTestCase Context Format

**Q**: What format should context use in LLMTestCase?
**A**: The `context` parameter must be `List[str]`, not a single string:

```python
# Correct
test_case = LLMTestCase(
    input="...",
    actual_output="...",
    context=["File: utils/math.py", "Project uses Python 3.10+"]
)

# Incorrect
test_case = LLMTestCase(
    input="...",
    actual_output="...",
    context="File: utils/math.py"  # Wrong: single string
)
```

### RESOLVED: Agent Invocation for Testing

**Q**: How do we programmatically invoke agents for testing?
**A**: Use the `@observe` decorator for tracing:

```python
from deepeval.tracing import observe, update_current_span
from deepeval.metrics import TaskCompletionMetric

@observe(metrics=[TaskCompletionMetric()])
def run_agent(agent: str, task: str, context: list[str]) -> str:
    # Agent logic here
    return result
```


### RESOLVED: Built-in Metrics for Agents

**Q**: Which DeepEval built-in metrics should we use?
**A**: Key built-in metrics for agent evaluation:

| Metric | Purpose |
|--------|---------|
| `TaskCompletionMetric` | Evaluates whether the agent completed its task |
| `ToolCorrectnessMetric` | Validates correct tool usage by agents |
| `AnswerRelevancyMetric` | Checks relevance of output to input |
| `FaithfulnessMetric` | Verifies output accuracy against context |
| `GEval` | Custom evaluation with user-defined steps |

### RESOLVED: Test Case Count

**Q**: How many test cases per agent/scenario?
**A**: 
- Simple agents: 15-30 per category
- Medium complexity: 30-50 per category
- Complex agents: 50-100+ per category
- Start with under 100 total, expand based on coverage gaps

---

## Remaining Considerations

### CI/CD Integration

- Run DeepEval tests in CI using `deepeval test run`
- Consider cost/time budget per run (LLM calls are expensive)
- Handle flaky tests with retry logic and threshold tolerance

### Baseline Management

- Establish baselines by running tests against known-good agent versions
- Update golden datasets when agent behavior intentionally changes
- Monitor metric drift over time via Grafana dashboards

---

## Related Documentation

- [DeepEval Evaluation Runbook](./deepeval-evaluation-runbook.md) - Metrics infrastructure usage
- [DeepEval Prometheus OTEL Integration](./deepeval_prometheus_otel_integration.md) - Technical integration details
- [Agent Selection Guide](../agents/agent-selection-guide.md) - Agent capabilities reference

---


## References

- [DeepEval Documentation](https://docs.confident-ai.com/)
- [DeepEval GitHub](https://github.com/confident-ai/deepeval)
- [DeepEval Metrics Reference](https://docs.confident-ai.com/docs/metrics-introduction)
- [DeepEval Tracing](https://docs.confident-ai.com/docs/tracing-introduction)
