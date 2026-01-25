# Observability Checklist (Operator Hat)

**Source**: `.claude/docs/01-guides/review/operational-edge-reliability.md`

## Log Quality

### OB-001: Why Logs
- **Check**: Logs explain "why" not just "what"
- **Severity**: MEDIUM
- **Evidence**: Log statements with context values
- **Pass**: `"Retrying request (attempt 3/5, last_error=timeout)"`
- **Fail**: `"Retrying request"`

### OB-002: Log Levels
- **Check**: Appropriate log levels used
- **Severity**: LOW
- **Evidence**: logger.info/warning/error usage
- **Pass**: ERROR for failures, INFO for flow, DEBUG for details
- **Fail**: Everything at INFO or DEBUG

### OB-003: Structured Logging
- **Check**: Machine-parseable log format
- **Severity**: LOW
- **Evidence**: JSON logging, key-value pairs
- **Pass**: Structured fields extractable
- **Fail**: Unstructured prose only

## Metric Exposure

### OB-004: Feature Metrics
- **Check**: New features expose operational metrics
- **Severity**: LOW
- **Evidence**: Counter/gauge/histogram registration
- **Pass**: Queue size, latency, success rate tracked
- **Fail**: No metrics for new functionality

### OB-005: SLI Coverage
- **Check**: Service Level Indicators measurable
- **Severity**: MEDIUM
- **Evidence**: Latency, error rate, throughput metrics
- **Pass**: Key SLIs have corresponding metrics
- **Fail**: SLIs not measurable from metrics

## Configurability

### OB-006: Kill Switches
- **Check**: Feature can be disabled without deploy
- **Severity**: MEDIUM
- **Evidence**: Feature flags, config-based toggles
- **Pass**: Runtime disable possible
- **Fail**: Requires code change to disable

### OB-007: Tunable Parameters
- **Check**: Hardcoded values moved to config
- **Severity**: MEDIUM
- **Evidence**: Magic numbers, hardcoded timeouts
- **Pass**: Values in config, environment variables
- **Fail**: Hardcoded values require code change
