# Edge Reliability Examples

## Example Finding

```markdown
### E-001: Missing Timeout
- **Category**: Temporal Edge
- **Severity**: HIGH
- **Evidence**: `perplexity_provider.py:45` - `httpx.get(url)` without timeout
- **Recommendation**: Add `timeout=30` parameter
```
