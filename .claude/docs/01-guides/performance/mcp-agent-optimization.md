# MCP Tool Configuration & Optimization

---

This document contains MCP (Model Context Protocol) configuration guidance and token optimization strategies for the Gauntlet Agents project.

## MCP Token Optimization [MANDATORY]

**CRITICAL ISSUE:** MCP servers load ALL available tools, consuming 79k tokens (39.5% of context).
**ROOT CAUSE:** Loading ~70+ unused GitHub/Azure tools instead of essential subset.
**TARGET:** Reduce to ~15-20k tokens (75% reduction) by loading only required tools.

### Implementation Status

**Date:** 2025-10-10
**Status:** Architecture constraint identified, workaround documented

**Key Finding:** Claude Code MCP architecture has two layers:

1. **MCP Server Configuration** (loads tools into context) - Controls what tools exist
2. **settings.json Permissions** (filters tool usage) - Controls what Claude can use

**Current State:**

- `.claude/settings.json` correctly has ONLY Context7 tools in permissions (2 tools):
  - `mcp__context7__resolve-library-id`
  - `mcp__context7__get-library-docs`
- No GitHub, Azure, or Hugging Face tools in permissions list
- ✅ Permissions layer is already optimized

**Root Cause Analysis:**
The 79k token overhead comes from **MCP server-level tool loading**, not from settings.json permissions. Even if tools aren't in the `allow` list, MCP servers load ALL available tools into Claude's context at session start.

**Limitation:** Claude Code v1.0.111 does not support selective tool loading at the MCP server configuration level. The MCP server sends its entire tool catalog to Claude Code, regardless of which tools are actually used.

**Token Breakdown (Estimated):**

- Context7 (2 tools): ~2,000 tokens ✅ Correct
- GitHub (50+ tools): ~35,000 tokens ❌ Loaded but unused
- Azure (20+ tools): ~25,000 tokens ❌ Loaded but unused
- Hugging Face (N tools): ~10,000 tokens ❌ Loaded but unused
- Filesystem, Memory, Notion, Fetch: ~7,000 tokens ✅ Needed
- **Total:** ~79,000 tokens

**Recommended Actions:**

1. **Short-term Workaround (Implemented):**
   - Settings.json permissions already restrict usage to essential tools
   - Token consumption unavoidable but usage is controlled
   - Document this limitation for future reference

2. **Medium-term Solution (Pending Claude Code Update):**
   - Wait for Claude Code to support selective MCP server tool loading
   - File feature request with Anthropic for per-tool server configuration
   - Example desired syntax:
     ```json
     {
       "mcpServers": {
         "github": {
           "enabled": true,
           "tools": ["get_me", "list_repositories", "get_file_contents"]
         }
       }
     }
     ```

3. **Alternative Approach (If Needed):**
   - Disable unused MCP servers entirely in Claude Code settings
   - Re-enable only when needed for specific workflows
   - Trade-off: Manual server management vs automatic context reduction

**Expected Savings (if selective loading supported):**

- From: 79,000 tokens (39.5% of context)
- To: 15,000-20,000 tokens (7.5-10% of context)
- Reduction: ~60,000 tokens (75% reduction)

### Essential MCP Tools Only

**GitHub Tools (Keep 7 of 50+):**

```
mcp__github__get_me                    # User profile for authentication context
mcp__github__list_repositories         # Repository discovery and listing
mcp__github__get_file_contents         # Reading code and documentation
mcp__github__list_commits              # Git history and change tracking
mcp__github__list_branches             # Branch management for workflows
mcp__github__search_code               # Code pattern discovery
mcp__github__search_repositories       # Project discovery
```

**Azure Tools (Keep 3 of 20+):**

```
mcp__azure__keyvault                   # Secret management (stated requirement)
mcp__azure__redis                      # Caching layer (stated requirement)
mcp__azure__postgres                   # Database access (stated requirement)
```

**Context7 Tools (Keep All - Essential):**

```
mcp__context7__resolve-library-id      # Library ID resolution
mcp__context7__get-library-docs        # Implementation pattern research
```

### Tools to REMOVE (Context Bloat)

**GitHub (Remove ~43 tools):**

- All PR/issue management: `create_pull_request`, `merge_pull_request`, `update_issue`
- All code review tools: `create_pending_pull_request_review`, `submit_pending_pull_request_review`
- All workflow automation: `run_workflow`, `cancel_workflow_run`, `rerun_workflow_run`
- All repository management: `create_repository`, `fork_repository`, `delete_file`

**Azure (Remove ~17 services):**

- `mcp__azure__datadog`, `mcp__azure__bicepschema`, `mcp__azure__cosmos`
- `mcp__azure__aks`, `mcp__azure__acr`, `mcp__azure__foundry`
- All services except KeyVault, Redis, Postgres

**Hugging Face (Remove All):**

- Not needed for financial analysis workflow
- All `mcp__hugging-face__*` tools

### MCP Configuration Enforcement

**CLAUDE.md Rule:** Only use the essential tools listed above. Any usage of removed tools indicates configuration drift and must be corrected.

**Usage Patterns:**

- **GitHub:** "Getting and listing things" only - no repository modification
- **Azure:** KeyVault, Redis, Postgres access only - no infrastructure management
- **Context7:** Research and library documentation - maintain current usage

## Context7 Response Size Optimization [CRITICAL FOR CONTEXT MANAGEMENT]

### Problem Analysis

**Issue:** Context7 returns 15k+ tokens despite setting token limits (e.g., requesting 8000 tokens, receiving 15000+ actual tokens)
**Root Cause:** Context7 token limits are suggestions, not hard limits - server prioritizes content completeness over token constraints
**Impact:** Context window bloat, reduced conversation capacity, slower processing

### Optimization Techniques

#### 1. Topic Specificity Strategy

**Principle:** Narrow, specific topics yield smaller, more actionable responses than broad documentation requests

**Examples:**

```python
# ❌ BAD: Broad topic (15k+ tokens)
get-library-docs("/open-telemetry/opentelemetry-python",
                topic="Python FastAPI instrumentation patterns",
                tokens=8000)

# ✅ GOOD: Specific implementation focus (3k tokens)
get-library-docs("/open-telemetry/opentelemetry-python",
                topic="FastAPI auto_instrumentation setup steps",
                tokens=2000)
```

#### 2. Progressive Research Pattern

**Principle:** Multiple small, targeted queries instead of single comprehensive requests

**Implementation:**

```python
# Instead of one large query, use sequence of focused queries:
# Query 1: Basic setup
get-library-docs("/library/project", topic="installation setup", tokens=2000)

# Query 2: Configuration
get-library-docs("/library/project", topic="configuration examples", tokens=2000)

# Query 3: Integration patterns
get-library-docs("/library/project", topic="integration patterns", tokens=2000)

# Total: ~9k focused tokens vs ~20k+ comprehensive dump
```

#### 3. Question-Driven Query Formation

**Principle:** Frame queries as specific implementation questions rather than topic areas

**Patterns:**

- **Instead of:** `topic="error handling"`
- **Use:** `topic="how to handle timeout errors"`
- **Instead of:** `topic="API documentation"`
- **Use:** `topic="POST request authentication examples"`
- **Instead of:** `topic="testing patterns"`
- **Use:** `topic="mock external API calls"`

#### 4. Context7 Query Templates

**Basic Setup Pattern:**

```python
get-library-docs("/{org}/{project}",
                topic="{library} installation and basic setup",
                tokens=2000)
```

**Configuration Pattern:**

```python
get-library-docs("/{org}/{project}",
                topic="{library} configuration file examples",
                tokens=2000)
```

**Integration Pattern:**

```python
get-library-docs("/{org}/{project}",
                topic="integrate {library} with {framework}",
                tokens=2000)
```

**Troubleshooting Pattern:**

```python
get-library-docs("/{org}/{project}",
                topic="{library} common error solutions",
                tokens=2000)
```

### Advanced Optimization Strategies

#### Library-Specific Optimization

**High-volume libraries** (OpenTelemetry, FastAPI, LangChain) tend to return larger responses:

- Use narrower topics
- Focus on specific use cases
- Leverage sub-library IDs when available

#### Response Size Prediction

**2k token requests typically return:** 3-4k tokens
**5k token requests typically return:** 6-8k tokens  
**8k token requests typically return:** 10-15k tokens

**Planning rule:** Budget 1.5x requested tokens for actual consumption

#### Emergency Context Management

If Context7 response exceeds expectations:

1. **Immediately switch to WebSearch** for targeted queries
2. **Use specific search terms** like "[library] [specific-feature] example 2025"
3. **Extract only implementation snippets** from WebSearch results
4. **Document size deviation** for future query refinement

## researcher-external Agent Integration [RECOMMENDED]

### When to Use researcher-external Agent vs Direct Context7 Tools

**RECOMMENDED APPROACH**: Use researcher-external agent for all library documentation and web research.

**researcher-external Agent** (Preferred):

- **Use for**: All library documentation, API references, implementation patterns
- **Benefits**:
  - 4-phase workflow (Parse → Research → Compress → Return)
  - 3-round search strategy optimized for Context7 (<15s)
  - Built-in compression (15:1 ratio for verbose docs)
  - Quality heuristics (trust score ≥7, snippets ≥100)
  - Confidence scoring (0.90 target)
- **When**: Any library research need (setup, patterns, best practices)

**Direct Context7 Tools** (Fallback):

- **Use for**: Quick lookups when researcher-external unavailable
- **Tools**: `mcp__context7__resolve-library-id`, `mcp__context7__get-library-docs`
- **When**: Simple validation, emergency queries, agent-driven context gathering

### researcher-external Workflow

```markdown
User: "How do I implement FastAPI dependency injection?"
↓
Claude Code: Delegate to [researcher-external]
↓
researcher-external:

1. Parse query → library="fastapi", topic="dependency injection"
2. Research (3 rounds):
   - resolve-library-id("/fastapi/fastapi")
   - get-library-docs(topic="dependency injection patterns", tokens=5000)
   - get-library-docs(topic="Depends usage examples", tokens=2000)
3. Compress findings (15:1 ratio)
4. Return structured response with examples
   ↓
   Claude Code: Synthesizes answer for user
```

### Context7 Best Practices (for Direct Usage)

When using Context7 tools directly (not through researcher-external):

1. **Always use resolve-library-id first** (unless user provides exact `/org/project` format)
2. **Apply topic specificity** (narrow topics → smaller responses)
3. **Use progressive research** (multiple small queries vs one large dump)
4. **Frame as questions** ("how to X" vs "X documentation")
5. **Budget 1.5x tokens** (requests return more than specified)

## Context7 Token Allocation Strategy

### Dynamic Token Allocation

**Purpose:** Prevent token waste while ensuring adequate research depth for different use cases.

**Token Limits by Research Type:**

#### Basic Validation (2000 tokens)

**Use cases:**

- Quick pattern existence checks
- Simple library feature confirmation
- Basic compatibility validation
- "Does X support Y?" queries

**Examples:**

```
get-library-docs("/pydantic/pydantic", topic="validation", tokens=2000)
get-library-docs("/pytest-dev/pytest", topic="fixtures", tokens=2000)
```

#### Standard Research (5000 tokens) [DEFAULT]

**Use cases:**

- Normal implementation research
- API usage patterns and examples
- Configuration and setup guidance
- Common integration patterns

**Examples:**

```
get-library-docs("/fastapi/fastapi", topic="dependency injection", tokens=5000)
get-library-docs("/langchain-ai/langgraph", topic="workflow orchestration", tokens=5000)
```

#### Deep Analysis (8000 tokens)

**Use cases:**

- Comprehensive architectural research
- Complex integration patterns
- Performance optimization strategies
- Security and best practices analysis

**Examples:**

```
get-library-docs("/openai/openai-python", topic="streaming responses", tokens=8000)
get-library-docs("/anthropics/anthropic-sdk-python", topic="async patterns", tokens=8000)
```

### Implementation Guidelines

1. **Start with standard (5000)** for most research needs
2. **Use basic (2000)** for simple validation queries
3. **Escalate to deep (8000)** only for complex architectural decisions
4. **Progressive research:** Start basic, then deeper if more detail needed
5. **Document token choice rationale** in commit messages when non-standard

### Research Quality Metrics

- **Token efficiency:** Aim for actionable insights per token consumed
- **Research completeness:** Ensure adequate depth for implementation confidence
- **Follow-up reduction:** Minimize need for additional research rounds

---

## MCP Server Deep Dives

This section provides detailed documentation for the 5 core MCP servers used in the Gauntlet Agents project: Context7, Fetch, Filesystem, Memory, and Notion.

## Context7 MCP Server [LIBRARY DOCUMENTATION]

### Essential Tools Configuration

**Context7 Tools (Keep 2 of 2):**

```
mcp__context7__resolve-library-id      # Match library names to Context7 IDs
mcp__context7__get-library-docs        # Retrieve version-specific documentation
```

**Purpose:** Official library documentation retrieval with quality scoring and version-specific lookup.

### Context7 Core Capabilities

**Tool: resolve-library-id**

- **Purpose:** Convert friendly library names to Context7-compatible library IDs
- **Parameters:** libraryName (string, required)
- **Returns:** List with id, trust_score (recommend ≥7), snippet_count (recommend ≥100), description, versions

**Tool: get-library-docs**

- **Purpose:** Retrieve version-specific documentation with topic focusing
- **Parameters:**
  - context7CompatibleLibraryID (required, format: /org/project or /org/project/version)
  - topic (optional, 2-4 word phrases)
  - tokens (optional, default: 5000, min: 1000)
- **Note:** Server often returns MORE than requested (requires compression)

### When to Use Context7

✅ **Use for:**

- Official documentation lookup
- Version-specific features
- API references and migration guides
- Code generation with current APIs

❌ **NOT for:**

- Local codebase analysis (use researcher-codebase)
- Community tutorials (use researcher-external with web search)
- Unindexed libraries

### Context7 Best Practices

**Token Management:**

- Use specific topics: "async field validation" (good) vs "documentation" (bad)
- Progressive allocation: 2k → 5k → 8k only if needed
- Multiple small queries > single large query
- Implement 15:1 compression ratio

**Quality Checks:**

- trust_score ≥7, snippet_count ≥100
- If insufficient → researcher-external auto-escalates to Perplexity

**Configuration (NPX):**

```json
{
  "command": "npx",
  "args": ["-y", "@upstash/context7-mcp", "--api-key", "KEY"]
}
```

**Windows Fix (Timeout):**

```json
{
  "command": "cmd",
  "args": ["/c", "npx", "-y", "@upstash/context7-mcp", "--api-key", "KEY"]
}
```

---

## Fetch MCP Server [WEB CONTENT]

### Essential Tools Configuration

**Fetch Tools (Keep 1 of 1):**

```
mcp__fetch__fetch    # Retrieve web content as markdown
```

### Fetch Core Capabilities

**Tool: fetch**

- **Parameters:**
  - url (required): Web page URL
  - max_length (optional, default: 5000): Character limit
  - start_index (optional): Pagination starting point
  - raw (optional, default: false): Get HTML instead of markdown
- **Returns:** Processed markdown or raw HTML

### When to Use Fetch

✅ **Use for:**

- Web documentation for AI analysis
- Extracting document sections
- Processing content in chunks
- Quick public page summaries

❌ **NOT for:**

- JavaScript-heavy SPAs (limited JS execution)
- Authentication-required content
- Large file downloads

⚠️ **Security Warning:** Can access local/internal IPs - configure carefully

### Fetch Best Practices

**Configuration (uvx):**

```json
{
  "command": "uvx",
  "args": ["mcp-server-fetch"]
}
```

**Optimization:**

- Use max_length to limit response size
- Use start_index for pagination
- Set raw=true for custom parsing

**Token Allocation:**

- Quick lookup: max_length=2000
- Standard page: max_length=5000 (default)
- Full article: max_length=10000+

---

## Filesystem MCP Server [FILE OPERATIONS]

### Essential Tools Configuration

**Filesystem Tools (Keep 12 of 12):**

```
read_text_file, read_media_file, read_multiple_files
write_file, edit_file
create_directory, list_directory, list_directory_with_sizes, directory_tree
list_allowed_directories, move_file, search_files, get_file_info
```

### Filesystem Core Capabilities

**Reading:** read_text_file (with head/tail), read_media_file (base64), read_multiple_files (batch)
**Writing:** write_file (create/overwrite), edit_file (pattern-based with dryRun)
**Directories:** create_directory, list\*, directory_tree (with excludePatterns)
**Operations:** move_file, search_files (glob patterns), get_file_info

### When to Use Filesystem

✅ **Use for:**

- AI code generation workflows
- Controlled development environments
- File analysis & pattern scanning
- Project setup & scaffolding
- Refactoring with pattern-based edits

❌ **NOT for:**

- Unrestricted filesystem access
- Binary manipulation (read-only as base64)
- Real-time file watching
- System-wide operations

### Filesystem Best Practices

**Security (Explicit Permissions):**

```json
{
  "args": [
    "-y",
    "@modelcontextprotocol/server-filesystem",
    "/Users/username/projects/my-project",
    "/Users/username/reference/docs"
  ]
}
```

**Safe Editing Protocol:**

1. get_file_info(path) → Validate exists
2. read_text_file(path) → Load current content
3. edit_file(path, edits, dryRun: true) → Preview
4. Review diff output
5. edit_file(path, edits, dryRun: false) → Apply

**Performance:**

- Use excludePatterns: ["node_modules", ".git", "dist"]
- Prefer directory_tree over recursive list_directory
- Use head/tail for large logs
- Batch with read_multiple_files

**Token Allocation:**

- Single file: ~500-2000 tokens
- Directory listing: ~100-500 tokens
- Directory tree: ~500-5000 tokens (deep hierarchies)

---

## Memory MCP Server [KNOWLEDGE GRAPH]

### Essential Tools Configuration

**Memory Tools (Keep 9 of 9):**

```
create_entities, delete_entities, open_nodes
add_observations, delete_observations
create_relations, delete_relations
search_nodes, read_graph
```

### Memory Core Capabilities

**Entities:** create (with type + observations), delete (cascade relations), open (retrieve specific)
**Observations:** add (append facts), delete (remove facts)
**Relations:** create (directed, active voice), delete
**Search:** search_nodes (query-based), read_graph (entire graph)

### When to Use Memory

✅ **Use for:**

- Cross-session persistence
- User personalization
- Relationship tracking
- Context accumulation over time

❌ **NOT for:**

- Vector similarity (use Pinecone/Weaviate)
- Multi-user isolation (no scoping)
- Real-time collaboration (no sync)
- Audit trails (no history)
- Large-scale deployment (JSON storage)

### Memory Best Practices

**Configuration (NPX):**

```json
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-memory"],
  "env": { "MEMORY_FILE_PATH": "/custom/path/memory.json" }
}
```

**Data Structure:**

- **Atomic observations:** Discrete facts ("Speaks Spanish" not "Speaks Spanish and French and graduated 2019")
- **Active voice relations:** "works_at" not "employed_by"
- **Unique names:** "John_Smith" (underscores)

**Workflow:**

1. User Identification → Create entity
2. Memory Retrieval (start) → search_nodes/open_nodes
3. Memory Capture (during) → Monitor 5 categories (Identity, Behaviors, Preferences, Goals, Relationships)
4. Memory Update (end) → create_relations, add_observations

**Limitations:**

- No versioning (permanent overwrites)
- No access control (all accessible)
- Local storage only
- JSON format (limited scale)

**Token Allocation:**

- Entity creation: ~50-200 tokens
- Search queries: ~200-1000 tokens
- read_graph: ~1000-10000+ tokens (entire graph)

---

## Notion MCP Server [WORKSPACE INTEGRATION]

### Essential Tools Configuration

**Notion Tools (Keep 15 of 15):**

```
notion-search, notion-fetch
notion-create-pages, notion-update-page, notion-move-pages, notion-duplicate-page
notion-create-database, notion-update-database
notion-create-comment, notion-get-comments
notion-get-teams, notion-get-users, notion-get-self, notion-get-user
```

### Notion Core Capabilities

**Search:** notion-search (workspace + connected sources like Slack/GitHub/Jira, supports filters)
**Pages:** create, update (properties/content), move, duplicate, fetch
**Databases:** create (with schema), update (schema/display), fetch
**Comments:** create, get
**Users/Teams:** get-teams, get-users, get-self, get-user

### When to Use Notion

✅ **Use for:**

- Knowledge base management
- Project tracking (database CRUD)
- Team collaboration
- Content migration (bulk page creation)
- Workspace automation
- Research compilation

❌ **NOT for:**

- Real-time chat (use Slack)
- Large file storage (size limits)
- Complex calculations (compute externally)

### Notion Best Practices

**Authentication:**

```json
{
  "env": { "NOTION_API_KEY": "secret_..." }
}
```

**Page Creation:**

- Always include title property
- Use Notion-flavored Markdown (callouts, toggles, tables, databases)
- Fetch database schema first (get exact property names)
- Use data_source_id for multi-source databases (not database_id)

**Database Updates:**

- Cannot delete/create title properties
- Max one unique_id property
- Use null to remove: {"Old Property": null}
- Rename: {"Status": {"name": "Project Status"}}

**Common Issues:**

- "Page Not Found" → Share page with integration in Notion UI
- Search returns nothing → Notion AI required for connected sources
- Multi-source confusion → Use notion-fetch to get data_source_id

**Token Allocation:**

- Page creation: ~500-2000 tokens
- Database fetch: ~1000-5000 tokens
- Search results: ~500-3000 tokens

---

## MCP Server Selection Guide

| Use Case                | Recommended                   | Alternative        |
| ----------------------- | ----------------------------- | ------------------ |
| Library docs            | Context7 (researcher-external) | researcher-external |
| Web content             | Fetch                         | researcher-external |
| File operations         | Filesystem                    | Bash (limited)     |
| Cross-session memory    | Memory                        | Notion (team)      |
| Documentation workspace | Notion                        | Filesystem (local) |

**Integration Patterns:**

**Research → Documentation:**
Context7 (gather) → Filesystem (local files) → Notion (team pages)

**Code Generation → Validation:**
Context7 (patterns) → Filesystem (write/edit) → researcher-codebase (validate)

**Knowledge Management:**
Memory (personal context) → Notion (team knowledge) → Fetch (import content)
