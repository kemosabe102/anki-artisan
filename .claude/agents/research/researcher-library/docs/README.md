# researcher-library Documentation

Supporting documentation for the library documentation research specialist agent.

## Contents

| File | Purpose |
|------|---------|
| `context7-integration.md` | Context7 MCP workflow, 3-round search strategy, quality validation |
| `domain-expertise.md` | Library research methodology, compression patterns, termination rules |

## Quick Reference

- **Primary Tool**: Context7 MCP (resolve-library-id, get-library-docs)
- **Supplementary Tool**: WebFetch (only when Context7 partial coverage)
- **Quality Thresholds**: trust>=7, snippets>=100 (exception: trust>=9 allows snippets>=80)
- **Performance Target**: <15 seconds total
- **Compression Target**: 15:1 minimum
