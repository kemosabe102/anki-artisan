# Node Reliability Examples

## Example Finding

```markdown
### N-001: Missing Precondition
- **Category**: Invariant Core
- **Severity**: HIGH
- **Evidence**: `normalizer.py:23` - No validation before processing
- **Recommendation**: Add input validation guard clause
```
