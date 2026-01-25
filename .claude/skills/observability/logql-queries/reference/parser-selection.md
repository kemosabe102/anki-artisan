# Parser Selection Guide

Detailed reference for LogQL parser selection with benchmarks and examples.

## Table of Contents

- [Performance Benchmarks](#performance-benchmarks)
- [JSON Parser Details](#json-parser-details)
- [Logfmt Parser Details](#logfmt-parser-details)
- [Pattern Parser Details](#pattern-parser-details)
- [Regexp Parser Details](#regexp-parser-details)
- [Format Detection](#format-detection)
- [Decision Flowchart](#decision-flowchart)
- [Combining Parsers](#combining-parsers)
- [Performance Optimization](#performance-optimization)
- [Common Regex Patterns](#common-regex-patterns)

---

## Performance Benchmarks

Based on Grafana Labs benchmarks (2023):

| Parser | Throughput (lines/sec) | Relative Speed | Memory Overhead |
|--------|------------------------|----------------|-----------------|
| json | 1,000,000 | 100x | Low |
| logfmt | 1,000,000 | 100x | Low |
| pattern | 100,000 | 10x | Medium |
| regexp | 10,000 | 1x (baseline) | High |

**Source**: Grafana Labs LogQL Performance Guide

---

## JSON Parser Details

### Syntax

```logql
| json [<label>=<expression>, ...]
```

### When to Use

- Logs emitted in JSON format
- Structured application logs
- API response logs

### Examples

```logql
# Basic - extract all top-level fields
{job="api"} | json

# Selective - extract specific fields
{job="api"} | json status, message, latency_ms

# Nested - extract from nested objects
{job="api"} | json err="error.message", code="error.code"

# With array index
{job="api"} | json first_tag="tags[0]"
```

### Gotchas

- Fails silently on non-JSON lines (line skipped)
- OTLP logs are NOT JSON - use OTLP attribute access instead
- Large JSON objects increase memory usage

---

## Logfmt Parser Details

### Syntax

```logql
| logfmt [<label>=<expression>, ...]
```

### When to Use

- Logs in key=value format
- Go application logs (common default)
- Structured logs without JSON overhead

### Example Log Format

```
level=info msg="request completed" status=200 duration=1.5s user_id=12345
```

### Examples

```logql
# Basic - extract all fields
{job="go-app"} | logfmt

# Selective extraction
{job="go-app"} | logfmt level, status, duration

# Rename fields
{job="go-app"} | logfmt http_status="status"
```

### Gotchas

- Quoted values supported: `msg="hello world"`
- Whitespace in values must be quoted
- Boolean values parsed as strings

---

## Pattern Parser Details

### Syntax

```logql
| pattern `<pattern_expression>`
```

### Pattern Syntax

- `<field>` - Capture into named field
- `<_>` - Discard (don't capture)
- Literal text - Match exactly

### When to Use

- Consistent log structure
- Space or delimiter-separated fields
- Faster than regexp for simple patterns

### Examples

```logql
# Apache/Nginx access log
| pattern `<ip> - <user> [<timestamp>] "<method> <path> <_>" <status> <bytes>`

# Custom application log
| pattern `[<level>] <timestamp> - <message>`

# With discards
| pattern `<_> <_> <level>: <message>`
```

### Gotchas

- Pattern must match entire line or extraction fails
- No regex support - purely positional
- Best for known, consistent formats

---

## Regexp Parser Details

### Syntax

```logql
| regexp `<regex_with_named_groups>`
```

### When to Use

- Complex or irregular log formats
- Legacy systems with varied output
- When other parsers cannot match

### Examples

```logql
# ISO timestamp and level extraction
| regexp `(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}) \[(?P<level>\w+)\] (?P<message>.*)`

# IP address extraction
| regexp `(?P<client_ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})`

# Optional field
| regexp `(?P<required>\w+)(?: (?P<optional>\w+))?`
```

### Gotchas

- 100x slower than json/logfmt - use sparingly
- Complex regex increases CPU usage
- Named groups required for field extraction
- Test regex with sample logs before production use

---

## Format Detection

### How to Identify Log Format

| Log Characteristic | Likely Format | Recommended Parser |
|--------------------|---------------|-------------------|
| Starts with `{` | JSON | `json` |
| Contains `key=value` pairs | logfmt | `logfmt` |
| Fixed positional fields | Structured | `pattern` |
| Irregular/mixed | Legacy | `regexp` |
| OTLP/OpenTelemetry | OTLP | Direct attribute access |

### Quick Detection Query

```logql
# Sample logs to identify format
{job="target"} | limit 10
```

Examine output and select parser accordingly.

---

## Decision Flowchart

```
                    ┌─────────────────┐
                    │ Examine Sample  │
                    │     Logs        │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
        ┌─────▼─────┐                 ┌─────▼─────┐
        │ Starts    │                 │ key=value │
        │ with {?   │                 │ pairs?    │
        └─────┬─────┘                 └─────┬─────┘
              │                             │
         YES  │  NO                    YES  │  NO
              │                             │
        ┌─────▼─────┐                 ┌─────▼─────┐
        │   json    │                 │  logfmt   │
        └───────────┘                 └───────────┘
              
              NO from both
                   │
        ┌──────────▼──────────┐
        │ Consistent delim?   │
        └──────────┬──────────┘
                   │
              YES  │  NO
                   │
        ┌──────────▼────┐    ┌──────────▼────┐
        │   pattern     │    │    regexp     │
        │ (10x faster)  │    │ (last resort) │
        └───────────────┘    └───────────────┘
```

---

## Combining Parsers

### Multi-Stage Parsing

```logql
# Parse outer JSON, then inner logfmt in a field
{job="api"} 
  | json 
  | line_format "{{.metadata}}"
  | logfmt
```

### Conditional Parsing

```logql
# Different formats in same stream
{job="mixed"}
  | json 
  | __error__=""  # Only keep successfully parsed lines
```

---

## Performance Optimization

### Pre-Filter Always

```logql
# GOOD: Filter before parse
{job="api"} |= "error" | json

# BAD: Parse everything
{job="api"} | json | level="error"
```

### Selective Field Extraction

```logql
# GOOD: Only extract needed fields
{job="api"} | json status, message

# BAD: Extract everything
{job="api"} | json
```

### Use `__error__` for Error Handling

```logql
# Skip malformed lines
{job="api"} | json | __error__=""

# Find parsing errors
{job="api"} | json | __error__!=""
```

---

## Common Regex Patterns

### Timestamps

```regex
# ISO 8601
(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?)

# Common log format
(?P<timestamp>\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2} [+-]\d{4})
```

### IP Addresses

```regex
# IPv4
(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})

# IPv4 with port
(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(?P<port>\d+)
```

### Log Levels

```regex
# Bracketed level
\[(?P<level>DEBUG|INFO|WARN|ERROR|FATAL)\]

# Unbracketed
(?P<level>DEBUG|INFO|WARN|ERROR|FATAL):
```

### UUIDs

```regex
(?P<uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})
```
