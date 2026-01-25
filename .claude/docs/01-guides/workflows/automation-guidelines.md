# Claude Code Workflow Automation Guidelines

**Last Updated**: 2025-09-21
**Guidelines Version**: 1.0.0

## Overview

This document provides comprehensive guidelines for building automation within the Claude Code workflow ecosystem, focusing on hooks, validation rules, progress tracking, and integration patterns.

## Claude Code Hook Development

### Hook Architecture Principles

#### **Security-First Design**

```python
# REQUIRED: Input validation and sanitization
def validate_input(user_input):
    """Validate and sanitize all external input."""
    # Whitelist approach - only allow known good inputs
    # Escape special characters
    # Validate file paths are within project boundaries
    pass

# REQUIRED: Use absolute paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# FORBIDDEN: Never use user input directly in shell commands
# BAD: subprocess.run(f"git {user_input}")
# GOOD: subprocess.run(["git", "status"], cwd=PROJECT_ROOT)
```

#### **Graceful Degradation**

```python
def main():
    """Hook main function with graceful error handling."""
    try:
        # Hook logic here
        result = perform_validation()

        if result['success']:
            sys.exit(0)  # Allow operation
        else:
            print(json.dumps(result['error_info']))
            sys.exit(1)  # Block operation

    except Exception as e:
        # Log error but don't block workflow
        print(f"Hook automation failed: {e}", file=sys.stderr)
        sys.exit(0)  # Allow workflow to continue
```

#### **Non-Blocking Philosophy**

- **Validation hooks** MAY block operations (return exit code 1)
- **Progress tracking hooks** MUST NOT block (always exit code 0)
- **Notification hooks** MUST NOT block (always exit code 0)
- **All hooks** MUST handle errors gracefully

### Hook Types and Patterns

#### **1. Validation Hooks** (PreToolUse, UserPromptSubmit)

**Purpose**: Validate input, enforce rules, prevent invalid operations

**Template**:

```python
#!/usr/bin/env python3
"""
[Hook Name] Validation Hook
Validates [specific aspect] before allowing operation to proceed.
"""

import sys
import json
from pathlib import Path

def validate_operation(context):
    """Validate the operation against defined rules."""
    validation_results = {
        'success': True,
        'errors': [],
        'warnings': [],
        'guidance': []
    }

    # Validation logic here
    # Example: File path validation
    if not is_valid_path(context.get('file_path')):
        validation_results['success'] = False
        validation_results['errors'].append("Invalid file path")
        validation_results['guidance'].append("Use paths within project boundaries")

    return validation_results

def main():
    """Main validation execution."""
    context = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}

    try:
        results = validate_operation(context)

        if results['success']:
            if results['warnings']:
                print(json.dumps({'warnings': results['warnings']}))
            sys.exit(0)  # Allow operation
        else:
            print(json.dumps({
                'errors': results['errors'],
                'guidance': results['guidance']
            }))
            sys.exit(1)  # Block operation

    except Exception as e:
        # Graceful degradation - allow operation
        print(f"Validation hook failed: {e}", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
```

**Example Applications**:

- File path boundary validation
- Tool permission enforcement
- Input sanitization
- Security rule enforcement

#### **2. Progress Tracking Hooks** (PostToolUse, SessionEnd)

**Purpose**: Automatic progress updates and status synchronization

**Template**:

```python
#!/usr/bin/env python3
"""
[Hook Name] Progress Tracking Hook
Automatically updates progress tracking systems based on workflow events.
"""

import sys
import json
from datetime import datetime
from pathlib import Path

def detect_completion_event(context):
    """Detect if a trackable completion event occurred."""
    # Detection logic here
    # Example: Sub-agent completion detection
    if 'sub_agent_result' in context and context['sub_agent_result'].get('status') == 'SUCCESS':
        return {
            'event_type': 'sub_agent_completion',
            'agent': context['sub_agent_result']['agent'],
            'task': context['sub_agent_result']['task'],
            'timestamp': datetime.utcnow().isoformat(),
            'result': context['sub_agent_result']
        }
    return None

def update_living_sprint(completion_event):
    """Update living sprint with completion information."""
    living_sprint_path = Path("docs/00-project/LIVING_SPRINT.md")

    if not living_sprint_path.exists():
        return False

    try:
        # Read current content
        content = living_sprint_path.read_text()

        # Generate progress update
        update = generate_progress_update(completion_event)

        # Insert progress update (implementation specific)
        updated_content = insert_progress_update(content, update)

        # Write updated content
        living_sprint_path.write_text(updated_content)

        return True
    except Exception as e:
        print(f"Living sprint update failed: {e}", file=sys.stderr)
        return False

def main():
    """Main progress tracking execution."""
    context = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}

    try:
        completion_event = detect_completion_event(context)

        if completion_event:
            # Update all relevant tracking systems
            update_living_sprint(completion_event)
            update_roadmap_status(completion_event)
            update_startup_eval_cache(completion_event)

        # Always allow workflow to continue
        sys.exit(0)

    except Exception as e:
        # Non-blocking error handling
        print(f"Progress tracking failed: {e}", file=sys.stderr)
        sys.exit(0)  # Always allow workflow to continue

if __name__ == "__main__":
    main()
```

**Example Applications**:

- Living sprint progress updates
- Roadmap status synchronization
- Completion event logging
- Status cache invalidation

#### **3. Context Enhancement Hooks** (SessionStart, UserPromptSubmit)

**Purpose**: Add context and improve Claude's understanding

**Template**:

```python
#!/usr/bin/env python3
"""
[Hook Name] Context Enhancement Hook
Adds relevant context to improve Claude's understanding and workflow efficiency.
"""

import sys
import json
from pathlib import Path

def load_project_context():
    """Load relevant project context for Claude."""
    context = {}

    try:
        # Load living sprint status
        living_sprint = Path("docs/00-project/LIVING_SPRINT.md")
        if living_sprint.exists():
            context['current_sprint'] = extract_current_focus(living_sprint.read_text())

        # Load developer identity
        dev_identity = Path(".claude/developer-identity.json")
        if dev_identity.exists():
            context['developer'] = json.loads(dev_identity.read_text())

        # Load active roadmap items
        context['active_roadmap'] = load_active_roadmap_items()

    except Exception as e:
        print(f"Context loading failed: {e}", file=sys.stderr)

    return context

def generate_context_summary(context):
    """Generate human-readable context summary."""
    summary_parts = []

    if 'current_sprint' in context:
        summary_parts.append(f"Current Focus: {context['current_sprint']['title']}")
        summary_parts.append(f"Status: {context['current_sprint']['status']}")

    if 'developer' in context and context['developer'].get('codename'):
        summary_parts.append(f"Developer: {context['developer']['codename']}")

    if 'active_roadmap' in context:
        ready_items = [item for item in context['active_roadmap'] if item['status'] == 'ready']
        summary_parts.append(f"Ready Roadmap Items: {len(ready_items)}")

    return "\n".join(summary_parts)

def main():
    """Main context enhancement execution."""
    try:
        context = load_project_context()
        summary = generate_context_summary(context)

        if summary:
            # Output context for Claude
            print(json.dumps({
                'context_summary': summary,
                'detailed_context': context
            }))

        sys.exit(0)  # Always non-blocking

    except Exception as e:
        print(f"Context enhancement failed: {e}", file=sys.stderr)
        sys.exit(0)  # Always allow workflow to continue

if __name__ == "__main__":
    main()
```

**Example Applications**:

- Project status context loading
- Developer workflow personalization
- Current focus summarization
- Available action recommendations

### Hook Configuration

#### **Basic Hook Configuration**

```json
{
  "hooks": {
    "PreToolUse": {
      "matchers": ["Write:*.py", "Edit:*.py"],
      "command": ["python", ".claude/hooks/validate-python-changes.py"]
    },
    "PostToolUse": {
      "matchers": ["*"],
      "command": ["python", ".claude/hooks/track-progress.py"]
    },
    "SessionStart": {
      "command": ["python", ".claude/hooks/startup-eval.py"]
    }
  }
}
```

#### **Advanced Hook Configuration**

```json
{
  "hooks": {
    "UserPromptSubmit": {
      "matchers": ["/spec*", "/plan*", "/tasks*"],
      "command": ["python", ".claude/hooks/workflow-context.py"],
      "timeout": 5000,
      "env": {
        "WORKFLOW_MODE": "development",
        "CONTEXT_LEVEL": "enhanced"
      }
    },
    "PreToolUse": {
      "matchers": ["Write:.claude/agents/*", "Edit:.claude/agents/*"],
      "command": ["python", ".claude/hooks/validate-agent-changes.py"],
      "block_on_failure": true
    }
  }
}
```

## Automation Design Patterns

### 1. **Event-Driven Automation Pattern**

**Use Case**: React to specific events in the workflow

**Pattern**:

```python
class WorkflowEventHandler:
    """Handle workflow events with appropriate automation."""

    def __init__(self):
        self.event_handlers = {
            'sub_agent_completion': self.handle_sub_agent_completion,
            'workflow_stage_change': self.handle_stage_change,
            'quality_gate_passed': self.handle_quality_gate,
            'error_occurred': self.handle_error
        }

    def handle_event(self, event_type, event_data):
        """Handle event with appropriate automation."""
        handler = self.event_handlers.get(event_type)
        if handler:
            try:
                return handler(event_data)
            except Exception as e:
                self.log_error(f"Event handling failed: {e}")
                return self.graceful_fallback(event_type, event_data)
```

**Benefits**:

- Decoupled event handling
- Extensible automation system
- Graceful error handling
- Clear event contracts

### 2. **State Synchronization Pattern**

**Use Case**: Keep multiple systems synchronized automatically

**Pattern**:

```python
class StateSynchronizer:
    """Synchronize state across multiple workflow systems."""

    def __init__(self):
        self.sync_targets = [
            LivingSprinterSyncer(),
            RoadmapSyncer(),
            StartupEvalSyncer(),
            WorkflowRegistrySyncer()
        ]

    def synchronize_state(self, state_change):
        """Synchronize state change across all targets."""
        results = []

        for syncer in self.sync_targets:
            try:
                result = syncer.sync(state_change)
                results.append(('success', syncer.name, result))
            except Exception as e:
                results.append(('error', syncer.name, str(e)))
                # Continue with other syncers

        return results
```

**Benefits**:

- Consistent state across systems
- Failure isolation
- Extensible synchronization
- Comprehensive result tracking

### 3. **Validation Pipeline Pattern**

**Use Case**: Multi-stage validation with clear pass/fail criteria

**Pattern**:

```python
class ValidationPipeline:
    """Multi-stage validation with clear criteria."""

    def __init__(self):
        self.validators = [
            SchemaValidator(),
            SecurityValidator(),
            QualityValidator(),
            IntegrationValidator()
        ]

    def validate(self, input_data):
        """Run validation pipeline with detailed results."""
        results = {
            'overall_success': True,
            'validator_results': [],
            'errors': [],
            'warnings': [],
            'guidance': []
        }

        for validator in self.validators:
            try:
                validator_result = validator.validate(input_data)
                results['validator_results'].append(validator_result)

                if not validator_result['success']:
                    results['overall_success'] = False
                    results['errors'].extend(validator_result.get('errors', []))

                results['warnings'].extend(validator_result.get('warnings', []))
                results['guidance'].extend(validator_result.get('guidance', []))

            except Exception as e:
                results['overall_success'] = False
                results['errors'].append(f"Validator {validator.name} failed: {e}")

        return results
```

**Benefits**:

- Comprehensive validation
- Clear failure reasons
- Actionable guidance
- Extensible validation rules

## Progress Tracking Automation

### Automatic Living Sprint Updates

#### **Sub-Agent Completion Tracking**

```python
def track_sub_agent_completion(agent_result):
    """Track sub-agent completion and update living sprint."""
    if agent_result.get('status') != 'SUCCESS':
        return  # Only track successful completions

    completion_info = {
        'timestamp': datetime.utcnow().isoformat(),
        'agent': agent_result['agent'],
        'task': agent_result.get('task', 'Unknown task'),
        'outcome': agent_result.get('summary', 'Task completed'),
        'artifacts': agent_result.get('artifacts', [])
    }

    # Update living sprint with completion
    update_living_sprint_progress(completion_info)

    # Update roadmap if applicable
    if 'roadmap_item' in agent_result:
        update_roadmap_progress(agent_result['roadmap_item'], completion_info)
```

#### **Milestone Achievement Detection**

```python
def detect_milestone_achievement(completion_info):
    """Detect if completion represents a significant milestone."""
    milestones = {
        'feature_specification_complete': {
            'pattern': r'specification.*complete',
            'weight': 5,
            'next_action': 'Ready for /plan command'
        },
        'technical_plan_complete': {
            'pattern': r'technical.*plan.*complete',
            'weight': 8,
            'next_action': 'Ready for /tasks command'
        },
        'implementation_complete': {
            'pattern': r'implementation.*complete',
            'weight': 15,
            'next_action': 'Ready for code review'
        }
    }

    for milestone_name, milestone_config in milestones.items():
        if re.search(milestone_config['pattern'], completion_info['outcome'], re.IGNORECASE):
            return {
                'milestone': milestone_name,
                'weight': milestone_config['weight'],
                'next_action': milestone_config['next_action'],
                'completion_info': completion_info
            }

    return None
```

### Cross-Document Synchronization

#### **Consistency Validation**

```python
class DocumentConsistencyValidator:
    """Validate consistency across workflow documents."""

    def __init__(self):
        self.document_relationships = {
            'living_sprint': {
                'roadmap_dependencies': ['current_focus', 'active_items'],
                'startup_eval_dependencies': ['developer_status', 'recommendations']
            },
            'roadmap': {
                'living_sprint_dependencies': ['item_assignments', 'progress_status']
            },
            'workflow_registry': {
                'command_dependencies': ['available_workflows', 'maturity_levels']
            }
        }

    def validate_consistency(self):
        """Validate consistency across all related documents."""
        validation_results = {
            'consistent': True,
            'inconsistencies': [],
            'recommendations': []
        }

        for doc_name, relationships in self.document_relationships.items():
            doc_validation = self.validate_document_relationships(doc_name, relationships)

            if not doc_validation['consistent']:
                validation_results['consistent'] = False
                validation_results['inconsistencies'].extend(doc_validation['issues'])
                validation_results['recommendations'].extend(doc_validation['fixes'])

        return validation_results
```

#### **Automatic Synchronization**

```python
def synchronize_documents(change_event):
    """Automatically synchronize documents based on change events."""
    sync_rules = {
        'living_sprint_update': [
            'update_startup_eval_cache',
            'validate_roadmap_consistency',
            'update_workflow_recommendations'
        ],
        'roadmap_item_status_change': [
            'update_living_sprint_if_assigned',
            'update_startup_eval_recommendations',
            'refresh_workflow_discovery'
        ],
        'workflow_registry_update': [
            'update_command_documentation',
            'refresh_startup_eval_commands',
            'validate_workflow_dependencies'
        ]
    }

    sync_actions = sync_rules.get(change_event['type'], [])

    for action in sync_actions:
        try:
            execute_sync_action(action, change_event)
        except Exception as e:
            log_sync_error(action, change_event, e)
            # Continue with other sync actions
```

## Quality Assurance Automation

### Automated Quality Gates

#### **Schema Validation Gate**

```python
def validate_workflow_schemas(workflow_data):
    """Validate workflow data against defined schemas."""
    schema_path = Path(".claude/docs/schemas/workflow.result.schema.json")

    if not schema_path.exists():
        return {'success': False, 'error': 'Schema not found'}

    try:
        schema = json.loads(schema_path.read_text())
        jsonschema.validate(workflow_data, schema)
        return {'success': True}
    except jsonschema.ValidationError as e:
        return {
            'success': False,
            'error': f'Schema validation failed: {e.message}',
            'guidance': 'Check workflow output format against schema'
        }
```

#### **Integration Health Gate**

```python
def validate_integration_health():
    """Validate health of workflow integrations."""
    health_checks = {
        'sub_agent_availability': check_sub_agent_availability,
        'context7_connectivity': check_context7_connectivity,
        'document_accessibility': check_document_accessibility,
        'hook_functionality': check_hook_functionality
    }

    health_results = {}
    overall_health = True

    for check_name, check_function in health_checks.items():
        try:
            result = check_function()
            health_results[check_name] = result
            if not result['healthy']:
                overall_health = False
        except Exception as e:
            health_results[check_name] = {'healthy': False, 'error': str(e)}
            overall_health = False

    return {
        'overall_health': overall_health,
        'individual_results': health_results,
        'recommendations': generate_health_recommendations(health_results)
    }
```

### Performance Monitoring

#### **Workflow Performance Tracking**

```python
class WorkflowPerformanceTracker:
    """Track workflow performance metrics."""

    def __init__(self):
        self.metrics = {
            'execution_times': {},
            'success_rates': {},
            'bottleneck_points': {},
            'error_patterns': {}
        }

    def track_workflow_execution(self, workflow_name, start_time, end_time, success):
        """Track individual workflow execution."""
        execution_time = end_time - start_time

        # Update execution times
        if workflow_name not in self.metrics['execution_times']:
            self.metrics['execution_times'][workflow_name] = []
        self.metrics['execution_times'][workflow_name].append(execution_time)

        # Update success rates
        if workflow_name not in self.metrics['success_rates']:
            self.metrics['success_rates'][workflow_name] = {'total': 0, 'successful': 0}

        self.metrics['success_rates'][workflow_name]['total'] += 1
        if success:
            self.metrics['success_rates'][workflow_name]['successful'] += 1

    def analyze_performance(self):
        """Analyze performance data for insights."""
        analysis = {
            'average_execution_times': {},
            'success_rate_percentages': {},
            'performance_recommendations': []
        }

        # Calculate averages and success rates
        for workflow_name in self.metrics['execution_times']:
            times = self.metrics['execution_times'][workflow_name]
            analysis['average_execution_times'][workflow_name] = sum(times) / len(times)

            success_data = self.metrics['success_rates'][workflow_name]
            success_rate = success_data['successful'] / success_data['total']
            analysis['success_rate_percentages'][workflow_name] = success_rate * 100

            # Generate recommendations
            if success_rate < 0.9:
                analysis['performance_recommendations'].append(
                    f"Investigate {workflow_name} reliability (success rate: {success_rate:.1%})"
                )

            avg_time = analysis['average_execution_times'][workflow_name]
            if avg_time > 300:  # 5 minutes
                analysis['performance_recommendations'].append(
                    f"Optimize {workflow_name} performance (avg time: {avg_time:.1f}s)"
                )

        return analysis
```

## Security Considerations

### Input Validation and Sanitization

#### **Strict Input Validation**

```python
def validate_and_sanitize_input(user_input, input_type):
    """Validate and sanitize user input with strict rules."""
    validators = {
        'file_path': validate_file_path,
        'command_argument': validate_command_argument,
        'json_data': validate_json_data,
        'workflow_name': validate_workflow_name
    }

    validator = validators.get(input_type)
    if not validator:
        raise ValueError(f"Unknown input type: {input_type}")

    return validator(user_input)

def validate_file_path(file_path):
    """Validate file path for security and boundaries."""
    # Convert to Path object for safe handling
    path = Path(file_path).resolve()

    # Ensure path is within project boundaries
    project_root = Path(__file__).resolve().parent.parent.parent
    if not str(path).startswith(str(project_root)):
        raise ValueError("File path outside project boundaries")

    # Block sensitive paths
    sensitive_patterns = [
        r'\.git/',
        r'\.ssh/',
        r'/etc/',
        r'/home/[^/]+/\.',
        r'__pycache__'
    ]

    for pattern in sensitive_patterns:
        if re.search(pattern, str(path)):
            raise ValueError(f"Access to sensitive path blocked: {path}")

    return path
```

#### **Command Injection Prevention**

```python
def safe_command_execution(command, args, cwd=None):
    """Execute commands safely with injection prevention."""
    # Use subprocess with argument list (not shell)
    cmd_list = [command] + args

    # Validate command is in allowed list
    allowed_commands = ['git', 'python', 'uv', 'pytest']
    if command not in allowed_commands:
        raise ValueError(f"Command not allowed: {command}")

    # Set safe working directory
    if cwd is None:
        cwd = Path(__file__).resolve().parent.parent.parent

    try:
        result = subprocess.run(
            cmd_list,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30,  # Prevent hanging
            check=False  # Don't raise on non-zero exit
        )
        return result
    except subprocess.TimeoutExpired:
        raise RuntimeError("Command execution timed out")
```

### Access Control

#### **Hook Permission Model**

```python
def check_hook_permissions(hook_name, requested_operations):
    """Check if hook has permission for requested operations."""
    hook_permissions = load_hook_permissions()

    if hook_name not in hook_permissions:
        return {'allowed': False, 'reason': 'Hook not registered'}

    permissions = hook_permissions[hook_name]

    for operation in requested_operations:
        if operation not in permissions['allowed_operations']:
            return {
                'allowed': False,
                'reason': f'Operation not permitted: {operation}'
            }

    return {'allowed': True}

def load_hook_permissions():
    """Load hook permissions from configuration."""
    return {
        'validate-python-changes': {
            'allowed_operations': ['read_file', 'validate_syntax'],
            'file_patterns': ['*.py'],
            'can_block': True
        },
        'track-progress': {
            'allowed_operations': ['read_file', 'write_file'],
            'file_patterns': ['docs/00-project/LIVING_SPRINT.md'],
            'can_block': False
        },
        'startup-eval': {
            'allowed_operations': ['read_file'],
            'file_patterns': ['docs/**/*.md', '.claude/**/*.json'],
            'can_block': False
        }
    }
```

## Testing Automation

### Hook Testing Framework

#### **Hook Test Template**

```python
import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Import hook under test
sys.path.append(str(Path(__file__).parent.parent / "hooks"))
import validate_python_changes

class TestValidatePythonChangesHook(unittest.TestCase):
    """Test suite for Python validation hook."""

    def setUp(self):
        """Set up test environment."""
        self.test_context = {
            'file_path': 'test_file.py',
            'operation': 'Write',
            'content': 'print("Hello, World!")'
        }

    def test_valid_python_file_passes(self):
        """Test that valid Python file passes validation."""
        result = validate_python_changes.validate_operation(self.test_context)
        self.assertTrue(result['success'])
        self.assertEqual(len(result['errors']), 0)

    def test_invalid_syntax_fails(self):
        """Test that invalid Python syntax fails validation."""
        self.test_context['content'] = 'print("Hello, World!"'  # Missing closing paren
        result = validate_python_changes.validate_operation(self.test_context)
        self.assertFalse(result['success'])
        self.assertGreater(len(result['errors']), 0)

    def test_security_violation_fails(self):
        """Test that security violations fail validation."""
        self.test_context['content'] = 'import os; os.system("rm -rf /")'
        result = validate_python_changes.validate_operation(self.test_context)
        self.assertFalse(result['success'])
        self.assertIn('security', ' '.join(result['errors']).lower())

    @patch('sys.exit')
    def test_main_function_success(self, mock_exit):
        """Test main function with successful validation."""
        with patch('validate_python_changes.validate_operation', return_value={'success': True}):
            validate_python_changes.main()
            mock_exit.assert_called_with(0)

    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_function_failure(self, mock_print, mock_exit):
        """Test main function with validation failure."""
        with patch('validate_python_changes.validate_operation',
                  return_value={'success': False, 'errors': ['Test error']}):
            validate_python_changes.main()
            mock_exit.assert_called_with(1)
            mock_print.assert_called()

if __name__ == '__main__':
    unittest.main()
```

### Integration Testing

#### **Workflow Integration Tests**

```python
class TestWorkflowIntegration(unittest.TestCase):
    """Test workflow integration points."""

    def test_feature_development_workflow_integration(self):
        """Test complete feature development workflow."""
        # Test /spec → /plan → /tasks → /implement integration
        workflow_steps = [
            ('specify', {'feature': 'test feature'}),
            ('plan', {'specification': 'generated_spec.md'}),
            ('tasks', {'plan': 'generated_plan.md'}),
            ('implement', {'tasks': 'generated_tasks.md'})
        ]

        for step_name, step_input in workflow_steps:
            with self.subTest(step=step_name):
                result = execute_workflow_step(step_name, step_input)
                self.assertEqual(result['status'], 'SUCCESS')
                self.assertIn('artifacts', result)

    def test_progress_tracking_integration(self):
        """Test progress tracking across workflow completion."""
        # Simulate sub-agent completion
        completion_event = {
            'agent': 'development',
            'task': 'feature implementation',
            'status': 'SUCCESS',
            'artifacts': ['implementation.py']
        }

        # Test progress tracking hook
        with patch('track_progress.update_living_sprint') as mock_update:
            track_progress.handle_completion_event(completion_event)
            mock_update.assert_called_once()

    def test_cross_document_consistency(self):
        """Test cross-document consistency validation."""
        # Test that changes in one document are reflected in related documents
        living_sprint_update = {
            'current_focus': 'New feature implementation',
            'status': 'In Progress'
        }

        consistency_result = validate_document_consistency(living_sprint_update)
        self.assertTrue(consistency_result['consistent'])
        self.assertEqual(len(consistency_result['inconsistencies']), 0)
```

## Troubleshooting Automation

### Common Issues and Automated Solutions

#### **Hook Failure Recovery**

```python
def handle_hook_failure(hook_name, error, context):
    """Handle hook failures with appropriate recovery."""
    recovery_strategies = {
        'timeout': lambda: reschedule_hook_execution(hook_name, context),
        'permission_denied': lambda: fallback_to_manual_process(hook_name, context),
        'dependency_unavailable': lambda: graceful_degradation(hook_name, context),
        'validation_error': lambda: provide_error_guidance(hook_name, error, context)
    }

    error_type = classify_error(error)
    recovery_function = recovery_strategies.get(error_type, default_recovery)

    try:
        return recovery_function()
    except Exception as recovery_error:
        log_recovery_failure(hook_name, error, recovery_error)
        return default_fallback(hook_name, context)
```

#### **Performance Degradation Detection**

```python
def monitor_automation_performance():
    """Monitor automation performance and detect degradation."""
    performance_thresholds = {
        'hook_execution_time': 5.0,  # seconds
        'success_rate': 0.95,  # 95%
        'error_rate': 0.05,  # 5%
        'timeout_rate': 0.01  # 1%
    }

    current_metrics = collect_performance_metrics()

    alerts = []
    for metric, threshold in performance_thresholds.items():
        if current_metrics[metric] > threshold:
            alerts.append({
                'metric': metric,
                'current_value': current_metrics[metric],
                'threshold': threshold,
                'severity': 'high' if current_metrics[metric] > threshold * 1.5 else 'medium'
            })

    if alerts:
        handle_performance_alerts(alerts)

    return alerts
```

---

**These automation guidelines provide comprehensive patterns for building reliable, secure, and maintainable automation within the Claude Code workflow ecosystem.**
