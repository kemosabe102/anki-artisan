# Implement Command Examples

Usage examples and workflow demonstrations for the `/implement` command.

## Files

| File | Purpose |
|------|---------|
| `usage-examples.md` | Complete workflow examples with expected outputs |

## Quick Examples

### Basic Usage
```bash
/implement docs/01-planning/features/006-opentelemetry/
```

### Single Plan
```bash
/implement docs/01-planning/features/006-opentelemetry/ --plan=001
```

### Resume After Failure
```bash
/implement docs/01-planning/features/006-opentelemetry/ --resume
```

### Skip Blocked Tasks
```bash
/implement docs/01-planning/features/006-opentelemetry/ --skip-tasks=T009,T010,T011
```

### Dry Run (Preview)
```bash
/implement docs/01-planning/features/006-opentelemetry/ --dry-run
```

## See Also

- `usage-examples.md` - Full workflow scenarios
- `../docs/error-handling.md` - Recovery options
- `../docs/workflow-phases.md` - Phase details
