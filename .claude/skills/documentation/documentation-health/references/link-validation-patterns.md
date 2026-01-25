# Link Validation Patterns

## Markdown Link Extraction

### Primary Pattern

```regex
\[.*?\]\((.*?)\)
```

**Captures**: Link target from `[text](target)` syntax

**Examples**:
- `[Guide](./guide.md)` → captures `./guide.md`
- `[API](https://api.example.com)` → captures `https://api.example.com`
- `[Section](#introduction)` → captures `#introduction`

### Edge Cases

**Reference-style links**:
```regex
\[.*?\]:\s*(.+)$
```
Captures link definitions like `[ref]: https://example.com`

**Inline code with links** (exclude):
```regex
`\[.*?\]\(.*?\)`
```
Ignore links within backticks to avoid false positives

**HTML anchor tags**:
```regex
<a\s+href=["']([^"']+)["']
```
Extract href attribute from HTML `<a>` tags

## Link Type Classification

### Internal Links

**Patterns**:
- `./relative/path.md` - Relative from current file
- `../parent/path.md` - Relative with parent traversal
- `/absolute/from/root.md` - Absolute from repo root
- `path.md` - Same directory (no prefix)

**Validation**:
1. Resolve path relative to current file location
2. Check file existence with Read tool
3. If anchor included (`#section`), validate section header exists

### External Links

**Patterns**:
- `http://example.com`
- `https://secure.example.com`
- `ftp://files.example.com`

**Validation** (optional, resource-intensive):
1. HTTP HEAD request to check availability
2. Timeout: 5 seconds
3. Success: Status codes 200-299
4. Redirect: Follow up to 3 redirects
5. Failure: 404, 500, timeout

**Note**: Tier 1 marks external links as `external_unchecked`. Tier 2 can optionally validate.

### Anchor Links

**Patterns**:
- `#section-name` - Internal to current file
- `file.md#section-name` - External file with section

**Validation**:
1. Extract section name (remove `#`)
2. Search target file for matching header
3. Header patterns: `# Section Name`, `## Section Name`, etc.
4. Match algorithm: Convert to lowercase, replace spaces with hyphens

**Example**:
- Link: `guide.md#getting-started`
- Valid headers: `# Getting Started`, `## Getting Started`
- Invalid: `# Getting-Started` (manual slug doesn't match)

## HTTP Validation Details

### Request Configuration

```javascript
{
  method: 'HEAD',
  timeout: 5000,
  followRedirects: true,
  maxRedirects: 3,
  headers: {
    'User-Agent': 'Documentation-Health-Validator/1.0'
  }
}
```

### Status Code Handling

| Range | Classification | Action |
|-------|----------------|--------|
| 200-299 | Valid | Mark as `valid` |
| 300-399 | Redirect | Follow and recheck |
| 400-499 | Client error | Mark as `broken` |
| 500-599 | Server error | Mark as `external_error` (recheck later) |
| Timeout | Network issue | Mark as `external_unchecked` |

### Rate Limiting

**Protection**: Max 5 concurrent external validations, 100ms delay between requests

**Rationale**: Avoid overwhelming external servers or triggering rate limits

## Validation Output Format

```json
{
  "link": "https://example.com/page",
  "type": "external",
  "status": "valid",
  "status_code": 200,
  "response_time_ms": 234
}
```

```json
{
  "link": "./missing-file.md",
  "type": "internal",
  "status": "broken",
  "error": "File not found"
}
```

```json
{
  "link": "guide.md#invalid-section",
  "type": "anchor",
  "status": "broken",
  "error": "Section header not found in target file"
}
```
