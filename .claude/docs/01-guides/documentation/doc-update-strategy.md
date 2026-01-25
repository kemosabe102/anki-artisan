# Document Update Strategy Guide

## Adaptive Thresholds

Choose update mode based on relative impact to file size:

### **Chunked Mode**

- **Threshold**: ≤5% of lines OR ≤5 anchors
- **Process**: Section-by-section patches with validation
- **Use Case**: Small, targeted changes to specific sections

### **Batched Mode**

- **Threshold**: ≤15% of lines OR ≤12 anchors
- **Process**: Grouped edits with atomic commits
- **Use Case**: Moderate changes affecting multiple related sections

### **Recreate Mode**

- **Threshold**: >15% of lines OR >12 anchors
- **Process**: New version with atomic swap
- **Use Case**: Major restructuring or comprehensive updates

## Threshold Selection Logic

1. **Calculate both metrics**: line percentage and anchor count
2. **Use smaller threshold**: Choose mode based on whichever threshold is reached first
3. **Relative sizing**: Small files favor anchor limits, large files favor percentages
4. **Document rationale**: Always record why specific threshold was chosen

## Post-Edit Validation

After any update mode:

- **Check anchors**: Verify all internal links still work
- **Validate links**: Ensure cross-references remain accurate
- **Schema compliance**: Confirm document structure follows templates
- **V&V criteria**: Validate against acceptance criteria from spec

## Update Report Format

```yaml
doc_update_strategy:
  mode: 'chunked|batched|recreate'
  threshold_basis: 'anchor_count|line_percentage'
  file_size_lines: 450
  affected_anchors: 3
  affected_percentage: 0.04
  rationale: '3 anchors < 5 anchor limit, choose chunked mode'
```

## Risk Assessment

- **Chunked**: Low risk, isolated changes
- **Batched**: Medium risk, coordinate related changes
- **Recreate**: High risk, comprehensive validation required
