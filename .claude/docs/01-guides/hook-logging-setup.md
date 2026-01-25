---
title: "Hook Logging Setup Guide"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Hook Logging Setup Guide

**Purpose**: Enable OTLP logging in Claude Code hooks to send logs to Loki via OTLP Collector

**Status**: Infrastructure ready, hooks need instrumentation

---

## Quick Start (5 Minutes)

### 1. Set Environment Variables

Add to your shell profile (`.bashrc`, `.zshrc`, or PowerShell profile):

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:30317
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_SERVICE_NAME=claude-code-hooks
export HOOK_LOG_FORMAT=text
export HOOK_LOG_LEVEL=INFO
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_INSECURE=true
```

**Windows PowerShell**:

```powershell
$env:OTEL_EXPORTER_OTLP_ENDPOINT = "http://localhost:30317"
$env:OTEL_EXPORTER_OTLP_PROTOCOL = "grpc"
$env:OTEL_SERVICE_NAME = "claude-code-hooks"
$env:HOOK_LOG_FORMAT = "text"
$env:HOOK_LOG_LEVEL = "INFO"
$env:OTEL_LOGS_EXPORTER = "otlp"
$env:OTEL_EXPORTER_OTLP_INSECURE = "true"
```

### 2. Install OpenTelemetry Dependencies

```bash
uv add opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp-proto-grpc
```

### 3. Instrument a Hook (Example: `startup-eval.py`)

**Add at the top of the hook file**:

```python
import logging
from opentelemetry import logs as otel_logs
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk.logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk.logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource

# Configure OTLP logging (do this once at module level)
def setup_otlp_logging():
    """Initialize OTLP logging for hooks."""
    resource = Resource.create({
        "service.name": "claude-code-hooks",
        "service.namespace": "gauntlet-agents",
        "deployment.environment": "local"
    })

    logger_provider = LoggerProvider(resource=resource)
    otel_logs.set_logger_provider(logger_provider)

    otlp_exporter = OTLPLogExporter(
        endpoint="http://localhost:30317",
        insecure=True
    )
    logger_provider.add_log_record_processor(
        BatchLogRecordProcessor(otlp_exporter)
    )

    handler = LoggingHandler(
        level=logging.INFO,
        logger_provider=logger_provider
    )

    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

# Initialize logger
logger = setup_otlp_logging()

# Use logger in your hook
def main():
    logger.info("Hook execution started", extra={
        "hook_name": "startup-eval.py",
        "event_type": "hook_start"
    })

    try:
        # Your hook logic here
        result = perform_validation()
        logger.info("Hook execution completed", extra={
            "hook_name": "startup-eval.py",
            "event_type": "hook_complete",
            "result": str(result)
        })
    except Exception as e:
        logger.error("Hook execution failed", extra={
            "hook_name": "startup-eval.py",
            "event_type": "hook_error",
            "error": str(e)
        }, exc_info=True)
        raise
```

### 4. Verify Logs in Grafana

1. **Access Grafana**: `http://localhost:30030` (admin/admin)
2. **Navigate to Explore**
3. **Select Loki datasource**
4. **Run LogQL query**:
   ```
   {service_name="claude-code-hooks"}
   ```
5. **Should see logs** from instrumented hooks

---

## Structured Logging Best Practices

### Use Structured Attributes

**DO** - Use `extra` parameter for structured fields:

```python
logger.info("Tool decision made", extra={
    "tool_name": "Bash",
    "decision": "accept",
    "source": "config",
    "session_id": session_id,
    "user_id": user_id
})
```

**DON'T** - Embed data in log message:

```python
logger.info(f"Tool decision: {tool_name} {decision} from {source}")  # Hard to query
```

### Recommended Attributes for All Hooks

```python
{
    "hook_name": "startup-eval.py",          # Required: Identifies hook
    "session_id": "uuid",                    # Recommended: Groups logs by session
    "user_id": "hash",                       # Optional: User identification
    "event_type": "hook_start|hook_complete|hook_error",  # Required: Event classification
    "duration_ms": 1234,                     # Recommended: Performance tracking
    "tool_name": "Bash",                     # Optional: Tool context
    "command": "kubectl get pods",           # Optional: Command context
    "exit_code": 0,                          # Optional: Result status
    "error": "exception message"             # Required for errors
}
```

### Log Levels

| Level       | Use For                                                              |
| ----------- | -------------------------------------------------------------------- |
| **DEBUG**   | Detailed diagnostic info (function entry/exit, variable values)      |
| **INFO**    | Normal operational events (hook start/complete, tool decisions)      |
| **WARNING** | Unusual but handled conditions (deprecated features, fallback logic) |
| **ERROR**   | Errors that need investigation (exceptions, validation failures)     |

---

## LogQL Query Examples (Grafana Explore)

### All Hook Logs

```
{service_name="claude-code-hooks"}
```

### Logs by Hook Name

```
{service_name="claude-code-hooks"} |= "startup-eval.py"
```

### Error Logs Only

```
{service_name="claude-code-hooks"} | level="ERROR"
```

### Tool Decisions

```
{service_name="claude-code-hooks"} |= "tool_decision"
```

### Logs by Session ID

```
{service_name="claude-code-hooks"} |= "session_id=\"a816b700-5262-487d-982c-375dce23e400\""
```

### Hook Performance (duration > 1s)

```
{service_name="claude-code-hooks"} | json | duration_ms > 1000
```

### Failed Hook Executions

```
{service_name="claude-code-hooks"} |= "hook_error"
```

---

## Validation Checklist

After instrumenting hooks, verify the end-to-end flow:

- [ ] Environment variables set in shell profile
- [ ] OpenTelemetry dependencies installed (`uv add opentelemetry-*`)
- [ ] Hook instrumented with OTLP logging setup
- [ ] Run hook and check logs appear in Grafana Explore
- [ ] Verify OTLP Collector metrics show log exports: `curl http://localhost:30889/metrics | grep otelcol_exporter_sent_log_records`
- [ ] Verify Loki has logs: `curl 'http://localhost:30100/loki/api/v1/query_range?query={service_name="claude-code-hooks"}'`

---

## Troubleshooting

### Logs Not Appearing in Grafana

**Check OTLP Collector Logs**:

```bash
kubectl logs -n gauntlet-agents -l app=otel-collector --tail=50
```

Look for errors related to `otlphttp/loki` exporter.

**Check Loki Logs**:

```bash
kubectl logs -n gauntlet-agents loki-0 --tail=50
```

Look for OTLP ingestion errors.

**Verify OTLP Endpoint**:

```bash
# Test gRPC endpoint
grpcurl -plaintext localhost:30317 list

# Check metrics for export failures
curl http://localhost:30889/metrics | grep otelcol_exporter_send_failed_log_records
```

### "Connection Refused" Error

**Cause**: OTLP Collector not running or wrong endpoint.

**Fix**:

1. Check OTLP Collector pod: `kubectl get pods -n gauntlet-agents -l app=otel-collector`
2. Verify service: `kubectl get svc -n gauntlet-agents otel-collector-service`
3. Check NodePort: Should be 30317 for gRPC, 30318 for HTTP

### "No Logs in Loki" but OTLP Collector Healthy

**Cause**: Loki exporter configuration issue.

**Fix**:

1. Check OTLP Collector config: `kubectl get cm -n gauntlet-agents otel-collector-config -o yaml`
2. Verify logs pipeline includes `exporters: [otlphttp/loki, debug]`
3. Check Loki OTLP endpoint: `curl http://localhost:30100/ready`

---

## Performance Considerations

### Batch Processing

OTLP Collector uses batch processing to reduce network overhead:

- **Batch size**: 8192 log records (configured in `k8s/local/otel-collector.yaml`)
- **Timeout**: 200ms max wait for partial batches
- **Max batch size**: 10000 to prevent HTTP 4xx errors

**Implication**: Logs may have up to 200ms delay before appearing in Loki.

### Memory Limits

OTLP Collector has memory limits to prevent OOM:

- **Memory limit**: 256Mi
- **Memory limiter**: 224Mi (87.5% of container)
- **Spike buffer**: 32Mi (12.5%)

**Implication**: Very high log volume (>10k logs/sec) may trigger memory pressure. Monitor with:

```bash
kubectl top pods -n gauntlet-agents -l app=otel-collector
```

### Retention Policy

Loki retains logs for 7 days in local development:

- **Retention period**: 168h (7 days)
- **Compaction interval**: 10m
- **Storage**: PersistentVolume (5Gi)

**Implication**: Logs older than 7 days are automatically deleted. Increase retention in `k8s/local/loki.yaml` if needed.

---

## Next Steps

1. **Instrument All Hooks**:
   - `startup-eval.py` - Session initialization
   - `phase-summary.py` - Phase execution tracking
   - `security/validate_command.py` - Security validation events
   - `capture-command-context.py` - Command context logging

2. **Create Grafana Dashboard**:
   - Hook execution timeline
   - Error rate by hook
   - Session-based log aggregation
   - Tool decision logs

3. **Set Up Alerting**:
   - High error rate (>5% of hook executions fail)
   - OTLP export failures (Loki unreachable)
   - Hook performance degradation (duration >5s)

4. **Extend to Other Components**:
   - Agent logs (development, debugger, etc.)
   - API request logs (gauntlet-api)
   - Test execution logs (code-quality)

---

## References

- **Validation Report**: `LOGGING-FLOW-VALIDATION-REPORT.md`
- **Validation Script**: `scripts/validate_logging_flow.py`
- **OTLP Collector Config**: `k8s/local/otel-collector.yaml`
- **Loki Config**: `k8s/local/loki.yaml`
- **Grafana Datasources**: `k8s/local/grafana.yaml` (grafana-config ConfigMap)

---

**Last Updated**: 2025-10-31
**Status**: Infrastructure ready, hooks need instrumentation
