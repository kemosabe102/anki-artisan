# Desktop Commander MCP Best Practices

## File Writing Strategy
- **ALWAYS chunk files** into 25-30 line pieces maximum
- This is standard practice, not an emergency measure
- First write: `write_file(path, chunk1, {mode: 'rewrite'})`
- Subsequent writes: `write_file(path, chunk2, {mode: 'append'})`

## File Reading
- Use `read_file` for specific files (NOT cat/head/tail)
- Use `offset` and `length` parameters for large files
- Prefer absolute paths over relative paths

## File Search
- Use `start_search` for pattern matching (NOT find/grep commands)
- Choose correct `searchType`: `files` (by name) or `content` (text search)
- Use `literalSearch: true` for code patterns with special characters

## File Editing
- Use `edit_block` for surgical changes (NOT sed/awk)
- Include minimal context (1-3 lines) for unique identification
- Make multiple small edits rather than one large replacement

## General Rules
- Always use absolute paths for reliability
- Paths auto-normalize (forward/backward slashes both work)
- Avoid `cd` commands (don't persist) - use absolute paths instead
