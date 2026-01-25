# Domain Expertise: Gauntlet Agents Logging

**Purpose**: OTLP format specifics and Gauntlet-Agents logging context

---

## OpenTelemetry OTLP Log Format

**Critical Understanding**: Gauntlet Agents uses OpenTelemetry OTLP format for structured logging, NOT JSON lines.

### Log Structure

**OTLP Format**:
- **Body**: Plain text message (e.g., "Blocked Bash command")
- **Attributes**: Structured data as separate indexed labels
- **Example attributes**: `security_event_command`, `security_event_reason`, `hook_name`

**NOT JSON Format**:
```logql
# WRONG - Will cause JSONParserErr
{service_namespace="gauntlet-agents"} | json | security_event_command!=""

# CORRECT - Access attributes directly as labels
{service_namespace="gauntlet-agents"} | security_event_command!=""
```

---

## Common OTLP Attributes

### Security Events (from `.claude/hooks/security-validate-command.py`)

| Attribute | Description | Example |
|-----------|-------------|---------|
| `security_event_command` | The blocked command | `rm -rf /` |
| `security_event_reason` | Why it was blocked | `Destructive command` |
| `security_event_hook_name` | Hook that detected it | `security-validate-command` |
| `security_event_detected_issues` | Array of issue types | `["destructive", "banned"]` |

### Standard OTLP Resource Attributes

| Attribute | Description | Example |
|-----------|-------------|---------|
| `service_name` | Service identifier | `orchestrator` |
| `service_namespace` | Namespace | `gauntlet-agents` |
| `hook_name` | Hook that generated log | `startup-eval` |
| `component` | Component identifier | `agent-architect` |

---

## Query Patterns for OTLP

### Direct Attribute Filtering
```logql
{service_namespace="gauntlet-agents"}
  | security_event_command!=""
  | security_event_reason!=""
```

### Line Formatting with Attributes
```logql
{service_namespace="gauntlet-agents"}
  | security_event_command!=""
  | line_format "BLOCKED: {{.security_event_command}} | Reason: {{.security_event_reason}}"
```


### Aggregation by Attribute
```logql
topk(10, sum by (security_event_command)(
  count_over_time({service_namespace="gauntlet-agents"}
    | security_event_command!=""
    [$__range])
))
```

---

## Anti-Patterns for OTLP

### Never Use `| json` Parser

- Loki automatically indexes OTLP attributes as labels
- The body is plain text, not JSON
- Using `| json` causes: `JSONParserErr: Value looks like object but can't find closing '}' symbol`

### Invalid Label Filter Syntax
```logql
# WRONG - Boolean operators not valid in label filters
| hook_name!="" or agent_name=~"claude-code.*"

# CORRECT - Use multiple separate filters
| hook_name!=""
| agent_name=~"claude-code.*"
```

---

## When to Use JSON Parser

Only use `| json` when:
- Logs are explicitly formatted as JSON lines (not OTLP)
- Log body contains a JSON object (not just attributes)
- You need to parse nested JSON within the log message

**For Gauntlet Agents logs**: Never use `| json` - all structured data is in OTLP attributes.

---

## Real-World Examples (from logs-dashboard.json)

### Security Hook Logs (TSV + Regexp)
```logql
{service_namespace="gauntlet-agents"} 
  |~ "(?i)blocked" 
  | regexp "^(?P<ts>[^\t]+)\t(?P<level>[^\t]+)\t(?P<msg>.+)$"
```

### Negative Filtering
```logql
{service_namespace="gauntlet-agents"} 
  != "Blocked Bash command"
```

### Label Promotion for Aggregation
```logql
{service_namespace="gauntlet-agents"}
  | label_format command="{{.command}}"
```

---

## Sources

- Gauntlet Agents codebase: `.claude/hooks/security-validate-command.py`
- Dashboard patterns: `k8s/local/grafana/dashboards/logs-dashboard.json`
- OpenTelemetry specification: https://opentelemetry.io/docs/specs/otel/logs/
