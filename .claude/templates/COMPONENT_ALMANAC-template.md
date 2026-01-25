---
title: "[PROJECT_NAME] Component Almanac"
date: [YYYY-MM-DD]
status: ACTIVE
tags: [project, reference]
---
<!--
USAGE INSTRUCTIONS:
===================
This template helps you create a Component Almanac - a comprehensive reference guide
for AI coding agents (and humans) to understand existing functionality in your codebase.

PURPOSE: Prevent code duplication by documenting reusable components, patterns, and utilities.

HOW TO USE:
1. Copy this template to docs/00-project/COMPONENT_ALMANAC.md in your project
2. Replace [PROJECT_NAME] and [PLACEHOLDERS] with your project-specific information
3. Add sections for each major subsystem in your codebase
4. For each component, document: Location, Purpose, Key Features, Usage Example
5. Update regularly as new components are added
6. AI agents should CHECK THIS FILE BEFORE CREATING NEW CODE

CUSTOMIZATION:
- Keep sections that match your architecture (Core Infrastructure, Data Connectors, etc.)
- Add new sections for domain-specific components
- Remove sections that don't apply to your project
- Update the Table of Contents when adding/removing sections

For guidance on maintaining this file, see:
- docs/00-project/SPEC.md (for architecture context)
- docs/04-guides/development/coding-guidelines.md (for code standards)
-->

# [PROJECT_NAME] Component Almanac

**Purpose:** A comprehensive reference guide for AI coding agents to understand and leverage existing functionality in the [PROJECT_NAME] codebase, preventing duplication and promoting code reuse.

**Last Updated:** [YYYY-MM-DD]

---

## Table of Contents

<!--
Customize this table of contents based on your project structure.
Below are common categories - adjust to match your architecture.
-->

1. [System Architecture Overview](#system-architecture-overview)
2. [Core Infrastructure](#core-infrastructure)
3. [Data Connectors & Integrations](#data-connectors--integrations)
4. [Business Logic & Domain Models](#business-logic--domain-models)
5. [Utilities & Helper Functions](#utilities--helper-functions)
6. [Testing Infrastructure](#testing-infrastructure)
7. [Component Integration Patterns](#component-integration-patterns)

---

## System Architecture Overview

<!--
Provide a high-level overview of your system architecture.
This helps agents understand how components fit together.
-->

The [PROJECT_NAME] system implements a **[ARCHITECTURE_PATTERN]** architecture with [NUMBER] primary layers:

1. **[Layer 1 Name]** - [Brief description of layer purpose]
2. **[Layer 2 Name]** - [Brief description of layer purpose]
3. **[Layer 3 Name]** - [Brief description of layer purpose]

### Key Design Principles

<!--
List 3-5 key architectural principles that guide component design.
These help agents make decisions consistent with your architecture.
-->

- **[Principle 1]:** [Brief explanation]
- **[Principle 2]:** [Brief explanation]
- **[Principle 3]:** [Brief explanation]

---

## Core Infrastructure

<!--
Document foundational infrastructure components that other parts of the system depend on.
Examples: Configuration, logging, error handling, dependency injection, caching.
-->

### Configuration Management

<!--
How is configuration managed in your project?
Include environment variables, config files, feature flags, etc.
-->

#### [Configuration Component Name]

**Location:** `[path/to/configuration/module]`

**Purpose:** [What configuration problems does this solve?]

**Key Features:**
- [Feature 1 with brief description]
- [Feature 2 with brief description]
- [Feature 3 with brief description]

**Usage Example:**

```python
# Example code showing how to use this component
from [your_project].config import [ConfigClass]

config = [ConfigClass].get_instance()
api_key = config.get_secret("API_KEY")
```

**Related Files:**
- `[path/to/related/file1.py]` - [Brief description]
- `[path/to/related/file2.py]` - [Brief description]

See `[path/to/implementation.py]` for complete implementation.

---

### Logging & Observability

<!--
Document logging infrastructure, metrics collection, and tracing capabilities.
-->

#### [Logging Component Name]

**Location:** `[path/to/logging/module]`

**Purpose:** [What logging capabilities does this provide?]

**Key Features:**
- [Feature 1 with brief description]
- [Feature 2 with brief description]
- [Feature 3 with brief description]

**Usage Example:**

```python
# Example of how to use structured logging
from [your_project].logging import get_logger

logger = get_logger(__name__)
logger.info("Operation completed", extra={
    "operation_id": "12345",
    "duration_ms": 250,
    "status": "success"
})
```

See `[path/to/implementation.py]` for complete implementation.

---

### Error Handling

<!--
Document standard error handling patterns and custom exception classes.
-->

#### [Error Handling Component Name]

**Location:** `[path/to/errors/module]`

**Purpose:** [What error handling capabilities does this provide?]

**Key Features:**
- [Feature 1 with brief description]
- [Feature 2 with brief description]

**Usage Example:**

```python
# Example of using custom exceptions
from [your_project].errors import [CustomException]

try:
    result = perform_operation()
except [CustomException] as e:
    logger.error(f"Operation failed: {e}", exc_info=True)
    # Handle error appropriately
```

---

## Data Connectors & Integrations

<!--
Document components that connect to external systems, APIs, databases, etc.
For each connector, document: Purpose, API usage, authentication, rate limiting, caching.
-->

### [Connector Protocol/Base Class]

<!--
If you have a standard protocol or base class for connectors, document it here.
-->

**Location:** `[path/to/connector/protocol.py]`

**Purpose:** [What does this protocol define?]

**Key Features:**
- [Feature 1 with brief description]
- [Feature 2 with brief description]

**Standard Interface:**

```python
# Example of the connector protocol/interface
class [ConnectorProtocol]:
    async def fetch_data(self, input: [InputType]) -> [ResultType]:
        """[Docstring explaining the interface]"""
        ...
```

---

### [Specific Connector Name] Connector

<!--
Document each specific external integration.
EXAMPLE: REST API Connector, Database Connector, S3 Storage Connector, etc.
-->

**Location:** `[path/to/specific/connector.py]`

**Purpose:** [What external service does this connect to and why?]

**Key Features:**
- [Feature 1 with brief description]
- [Feature 2 with brief description]
- [Feature 3 with brief description]

**Authentication:** [How does this handle authentication?]

**Rate Limiting:** [Any rate limit handling?]

**Caching:** [Is caching implemented? TTL?]

**Usage Example:**

```python
# Example of using this connector
from [your_project].connectors import [ConnectorClass]

connector = [ConnectorClass](api_key="...")
result = await connector.fetch_data(input_param="value")
print(f"Received {len(result.data)} items")
```

**Configuration:**
- Environment variable: `[ENV_VAR_NAME]`
- Config file: `[config/file/path.yml]`

See `[path/to/implementation.py]` for complete implementation.

---

## Business Logic & Domain Models

<!--
Document core business logic and domain models.
This helps agents understand the data structures and business rules.
-->

### Domain Models

<!--
Document key data models used throughout the system.
-->

#### [Model Name]

**Location:** `[path/to/models/model.py]`

**Purpose:** [What business concept does this model represent?]

**Key Fields:**
- `[field_name]` ([type]): [Description of what this field represents]
- `[field_name]` ([type]): [Description of what this field represents]

**Validation Rules:**
- [Rule 1: Description]
- [Rule 2: Description]

**Usage Example:**

```python
# Example of creating and using this model
from [your_project].models import [ModelName]

instance = [ModelName](
    field1="value1",
    field2="value2"
)
# Validation happens automatically
```

---

### Business Logic Components

<!--
Document components that implement core business rules and workflows.
-->

#### [Business Logic Component Name]

**Location:** `[path/to/business/logic.py]`

**Purpose:** [What business function does this implement?]

**Key Operations:**
- `[operation_name]()`: [What this operation does]
- `[operation_name]()`: [What this operation does]

**Usage Example:**

```python
# Example of using this business logic
from [your_project].business import [ComponentName]

processor = [ComponentName]()
result = await processor.[operation_name](input_data)
```

---

## Utilities & Helper Functions

<!--
Document reusable utility functions and helper modules.
These prevent duplicating common operations.
-->

### [Utility Category Name]

<!--
Group utilities by category (e.g., String Utilities, Date Utilities, Validation Utilities)
-->

**Location:** `[path/to/utils/utility.py]`

**Purpose:** [What common operations do these utilities provide?]

**Available Functions:**

| Function Name | Purpose | Example Usage |
| :------------ | :------ | :------------ |
| `[function_name]()` | [What it does] | `result = [function_name](input)` |
| `[function_name]()` | [What it does] | `result = [function_name](input)` |
| `[function_name]()` | [What it does] | `result = [function_name](input)` |

**Usage Example:**

```python
# Example of using utility functions
from [your_project].utils import [utility_function]

cleaned_data = [utility_function](raw_data)
```

---

## Testing Infrastructure

<!--
Document testing utilities, fixtures, mocks, and test helpers.
This helps agents write tests consistent with existing patterns.
-->

### Test Fixtures

**Location:** `[path/to/tests/fixtures.py]`

**Purpose:** [What common test setup does this provide?]

**Available Fixtures:**

| Fixture Name | Purpose | Scope |
| :----------- | :------ | :---- |
| `[fixture_name]` | [What test data/setup it provides] | [function/module/session] |
| `[fixture_name]` | [What test data/setup it provides] | [function/module/session] |

**Usage Example:**

```python
# Example of using test fixtures
def test_example(fixture_name):
    result = function_under_test(fixture_name)
    assert result.is_valid
```

---

### Test Utilities

**Location:** `[path/to/tests/utils.py]`

**Purpose:** [What testing utilities are available?]

**Available Helpers:**
- `[helper_function]()`: [What it does for tests]
- `[helper_function]()`: [What it does for tests]

---

## Component Integration Patterns

<!--
Document common patterns for integrating multiple components.
This helps agents understand best practices for component composition.
-->

### Pattern: [Integration Pattern Name]

**Use Case:** [When should this pattern be used?]

**Components Involved:**
- [Component 1] - [Role in pattern]
- [Component 2] - [Role in pattern]

**Implementation:**

```python
# Example showing the integration pattern
from [your_project] import [Component1], [Component2]

# Step 1: Initialize components
comp1 = [Component1](config)
comp2 = [Component2](config)

# Step 2: Coordinate between components
result1 = await comp1.process(input_data)
result2 = await comp2.transform(result1)

# Step 3: Combine results
final_result = combine(result1, result2)
```

**Benefits:**
- [Benefit 1 of this pattern]
- [Benefit 2 of this pattern]

**Caveats:**
- [Important consideration or limitation]

---

## Adding New Components

<!--
Provide guidance for developers adding new components to the almanac.
-->

When adding a new component to this almanac:

1. **Choose the appropriate section** - Core Infrastructure, Data Connectors, etc.
2. **Document the essentials**:
   - Location (file path)
   - Purpose (what problem it solves)
   - Key features (3-5 bullet points)
   - Usage example (working code snippet)
   - Related files/components
3. **Update the Table of Contents** if adding a new section
4. **Keep descriptions concise** - aim for clarity over completeness
5. **Include working code examples** - agents learn best from examples
6. **Link to implementation** - reference the actual source file

---

## Component Reference Quick Links

<!--
Optional: Provide a flat list of all components for quick reference.
Useful when the almanac grows large.
-->

### All Components (Alphabetical)

| Component | Location | Primary Purpose |
| :-------- | :------- | :-------------- |
| [Component Name] | `[path]` | [Brief purpose] |
| [Component Name] | `[path]` | [Brief purpose] |
| [Component Name] | `[path]` | [Brief purpose] |

---

**Document Maintenance:**

This document should be updated whenever:
- New reusable components are added to the codebase
- Existing components undergo significant API changes
- Integration patterns change or new patterns emerge
- Component locations or file structures are refactored

**Last Major Revision:** [YYYY-MM-DD] by [Author Name]

<!--
END OF TEMPLATE

Remember:
1. This is a LIVING DOCUMENT - keep it updated!
2. AI agents should CHECK HERE FIRST before creating new utilities
3. Focus on REUSABLE components, not application-specific code
4. Include WORKING CODE EXAMPLES - they're the most helpful
5. Link to actual implementation files for complete details
-->
