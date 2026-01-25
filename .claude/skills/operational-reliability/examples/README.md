# Operational Reliability Examples

## Example Finding

```markdown
### O-001: Missing Log Context
- **Category**: Observability
- **Severity**: MEDIUM
- **Evidence**: `handler.py:67` - `logger.error("Request failed")`
- **Recommendation**: Include request_id and error details
```
