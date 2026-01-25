---
title: "AI Agent Tool Design and Agent-Tool Interactions: A Comprehensive Primer"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# AI Agent Tool Design and Agent-Tool Interactions: A Comprehensive Primer

**Tools are a fundamentally new kind of software.** They represent contracts between deterministic systems and non-deterministic agents, requiring us to rethink everything we know about software design. Unlike traditional APIs built for developers or systems, effective agent tools must account for limited context windows, token-by-token processing, and reasoning patterns that differ dramatically from programmatic logic. This guide distills Anthropic's battle-tested experience from Claude Code and the Claude Agent SDK into actionable principles for building agent systems that work.

The core insight: **success with AI agents isn't about building the most sophisticated system—it's about building the right system for your needs.** Start simple, measure performance systematically, and add complexity only when it demonstrably improves outcomes. This evaluation-driven approach, where agents themselves help optimize the tools they use, has proven transformative across domains from customer support to software engineering to financial analysis.

## The agent-tool relationship requires new design thinking

Traditional software design assumes abundant memory, precise control flow, and deterministic execution. Agent systems flip these assumptions. LLMs have severely limited context compared to computer memory. They process information token-by-token rather than iterating efficiently through data structures. They make autonomous decisions about which tools to use based on reasoning, not pre-programmed logic. Understanding these constraints fundamentally shapes how we design tools and architect agent systems.

**Think of tools as agent affordances rather than API endpoints.** The question isn't "does this tool expose system functionality?" but rather "does this tool enable the agent to accomplish real-world tasks efficiently?" A tool that returns all 10,000 contacts for an agent to search token-by-token is technically functional but ergonomically disastrous. A `search_contacts` tool that returns only relevant matches with surrounding context respects the agent's affordances and enables effective task completion.

This shift requires **investing as much effort in agent-computer interfaces (ACI) as we traditionally invest in human-computer interfaces (HCI).** Small refinements to tool descriptions can yield dramatic improvements—Claude Sonnet 3.5 achieved state-of-the-art performance on SWE-bench Verified after precise tool description optimizations. Error messages, parameter names, response formats, and documentation all become prompt engineering opportunities that deserve careful attention and iterative refinement.

## Tool design best practices

### Consolidate functionality, don't proliferate tools

**More tools don't always lead to better outcomes.** A common error is wrapping every API endpoint as a separate tool without considering agent affordances. Instead of creating `list_users`, `list_events`, and `create_event`, build a consolidated `schedule_event` tool that finds availability and schedules in one operation. Rather than `read_logs` that dumps everything, implement `search_logs` that returns only relevant entries with context. Replace `get_customer_by_id`, `list_transactions`, and `list_notes` with `get_customer_context` that compiles all relevant customer information at once.

This consolidation principle addresses a fundamental constraint: **agents select tools from what's loaded into their context window.** Too many tools or overlapping functionality distracts agents from efficient strategies. Each tool consumes context with its description, reducing space available for reasoning and task-relevant information. By selectively implementing a few thoughtful, high-impact tools whose names reflect natural task subdivisions, you reduce the risk of agent mistakes while enabling them to subdivide complex tasks the way humans would.

Tool granularity decisions should follow these guidelines: Each tool needs a clear, distinct purpose. Tools should reduce context consumed by intermediate outputs. Frequently chained operations can be consolidated into single tools. Tools should enable agents to skip directly to relevant information rather than forcing brute-force, token-by-token searches. The goal is building tools targeting specific high-impact workflows, not achieving comprehensive API coverage.

### Design interfaces for token efficiency and semantic understanding

**Response format flexibility dramatically impacts performance.** Implement an enum parameter letting agents control verbosity:

```typescript
enum ResponseFormat {
  DETAILED = 'detailed', // ~206 tokens: includes technical IDs for downstream calls
  CONCISE = 'concise', // ~72 tokens: natural language only, ⅓ the tokens
}
```

This GraphQL-like approach lets agents request only the information they need. Detailed responses include technical identifiers (`uuid`, `thread_ts`, `channel_id`) required for subsequent tool calls. Concise responses return natural language summaries when no further actions are needed. The difference—65% fewer tokens in the concise case—compounds across complex workflows involving dozens of tool calls.

**Prioritize contextual relevance over flexibility.** Return only high-signal information relevant to the agent's likely downstream actions. Favor semantic over technical identifiers: use `name`, `image_url`, and `file_type` rather than `uuid`, `256px_image_url`, and `mime_type`. Research shows that merely resolving alphanumeric UUIDs to semantically meaningful language significantly improves Claude's precision in retrieval tasks by reducing hallucinations. Agents handle human-readable identifiers far better than arbitrary technical codes.

Implement sensible defaults for token consumption: pagination, range selection, filtering, and truncation with reasonable limits. Claude Code defaults to warning at 10,000 tokens and limiting tool responses to 25,000 tokens. When implementing truncation, include steering instructions encouraging agents to make "many small and targeted searches instead of a single, broad search." This guidance helps agents develop token-efficient strategies rather than exhausting context with broad retrievals.

### Format selection matters profoundly for LLMs

**Unlike traditional software where format conversions are lossless, some formats are dramatically harder for LLMs to generate.** Give the model enough tokens to "think" before it writes itself into a corner. Keep formats close to what the model has seen naturally occurring in text on the internet. Eliminate formatting overhead that creates unnecessary cognitive load.

Writing code inside JSON requires escaping newlines and quotes, making it substantially harder for LLMs than markdown code blocks. Generating diffs requires knowing line counts in chunk headers before writing the actual changes. String-escaping complex code introduces more opportunities for errors. Even your tool response structure—XML, JSON, or Markdown—can impact evaluation performance significantly. There's no one-size-fits-all solution; LLMs perform better with formats matching their training data. Select based on evaluation results for your specific tasks and agents.

### Document tools like onboarding a new hire

**Tool descriptions require as much prompt engineering attention as your overall system prompts.** Think about describing your tool to a new hire on your team. Consider the context you might implicitly bring—specialized query formats, definitions of niche terminology, relationships between underlying resources—and make it explicit. Provide unambiguous parameter names (`user_id` not `user`), clear descriptions avoiding ambiguity, strict data models enforcing expected inputs and outputs, example usage, documented edge cases, specified input format requirements, and clear boundaries distinguishing this tool from others.

Small refinements to tool descriptions yield dramatic improvements. When launching a web search tool, engineers discovered Claude was needlessly appending "2025" to every query parameter, biasing results toward recent content. The issue was resolved by improving the tool description to clarify temporal handling. During SWE-bench implementation, the team "actually spent more time optimizing our tools than the overall prompt." They found the model made mistakes with relative filepaths after moving from the root directory. Solution: Change the tool to always require absolute filepaths. The model then used this method flawlessly—a simple constraint eliminated an entire class of errors through poka-yoke (mistake-proofing) design.

Error handling deserves equal attention. Avoid opaque error codes and tracebacks. Instead, prompt-engineer error responses to be specific and actionable:

**Unhelpful:** `Error: Invalid parameter type`

**Helpful:** `Error: The 'start_date' parameter must be in ISO 8601 format (YYYY-MM-DD). You provided: '2024-1-15'. Correct format example: '2024-01-15'`

During input validation, communicate specific improvements needed. Guide agents toward correct usage with clear instructions. These error messages are opportunities to teach the agent better patterns for future interactions.

### Create new tools strategically, extend judiciously

**Create a new tool when** the operation represents a fundamentally different capability, different authorization or permissions are required, the tool serves a distinct domain or service, or input/output schemas are substantially different. Example: Separate `Read`, `Write`, `Edit`, `Grep`, and `Glob` tools each have focused scope and clear semantics. They're not consolidated into a generic "file_operations" tool because they represent distinct operations with different use patterns.

**Extend existing tools when** adding optional parameters to existing functionality, supporting additional formats for the same operation, or adding convenience methods that compose existing operations. The key principle: avoid tool proliferation. Each new tool added to an agent's context increases cognitive load and introduces opportunities for confusion. Only add tools when they enable meaningfully different capabilities or serve sufficiently distinct use cases that consolidation would create confusion.

## Agent-tool interaction patterns

### Understanding architectural distinctions: workflows vs agents

**Workflows orchestrate LLMs and tools through predefined code paths.** You write the control flow, determining which LLM calls happen when and how tools get invoked. This approach offers predictability and consistency for well-defined tasks with known steps. Use workflows when the task can be cleanly decomposed into fixed subtasks, you need guaranteed consistency, latency is critical, or the sequence of operations is clear and stable.

**Agents dynamically direct their own processes and tool usage, maintaining autonomous control over task accomplishment.** The LLM decides which tools to use, in what order, with what parameters, based on reasoning about the current state and task requirements. This approach provides flexibility and model-driven decision-making needed for open-ended problems at scale. Use agents when steps can't be predicted in advance, you can't hardcode a fixed path, the LLM needs to operate for many turns, or the problem genuinely requires adaptive reasoning.

The trade-off is fundamental: **agentic systems often trade latency and cost for better task performance.** Workflows are faster and cheaper but rigid. Agents are slower and more expensive but adaptive. The right choice depends entirely on your use case. Customer support naturally requires conversation flow while needing external information and actions—perfect for agents. Simple data transformations with known steps—better as workflows. Start with the simplest solution (often a single LLM call optimized with retrieval), and only increase complexity when needed.

### Five workflow patterns for predefined orchestration

**Prompt chaining** decomposes tasks into sequences where each LLM call processes the previous one's output. You can add programmatic checks or "gates" on intermediate steps. Use when tasks cleanly decompose into fixed subtasks. The trade-off: accept higher latency for higher accuracy by making each step easier. Examples: Generate marketing copy then translate it; write an outline, check against criteria, then write the full document.

**Routing** classifies input and directs to specialized followup tasks. This enables separation of concerns and specialized prompts for different categories. Use when distinct categories benefit from separate handling and you can classify accurately. Examples: Direct customer queries to different processes (general questions, refunds, technical support); route easy questions to Haiku and hard questions to Sonnet for cost and speed optimization.

**Parallelization** comes in two variations. Sectioning breaks tasks into independent subtasks run simultaneously—like running separate guardrails from core response generation, or automated evaluations checking different aspects. Voting runs the same task multiple times for diverse outputs—like having multiple prompts review code for vulnerabilities and using vote thresholds for content moderation. Use when subtasks can truly be parallelized for speed, or when multiple perspectives improve decision quality.

**Orchestrator-workers** uses a central LLM that dynamically breaks down tasks, delegates to workers, and synthesizes results. The key difference from simple parallelization: flexibility. The subtasks aren't pre-defined but determined by the orchestrator based on the specific problem. Use for complex tasks where subtasks can't be predicted in advance. Examples: Coding products making complex changes across multiple files; search tasks gathering and analyzing information from multiple sources; research requiring synthesis of diverse information.

**Evaluator-optimizer** has one LLM generate responses while another provides evaluation and feedback in a loop. Use when clear evaluation criteria exist and iterative refinement provides measurable value. Signs of good fit: LLM responses demonstrably improve with human feedback, and the LLM can provide such feedback itself. Examples: Literary translation capturing nuance; complex search requiring multiple rounds of query refinement; creative tasks benefiting from critique and revision.

### The agent feedback loop and tool selection

**Agents operate in a specific feedback cycle:** gather context → take action → verify work → repeat. Tools are loaded prominently into Claude's context window and system prompt. The agent autonomously decides which tools to use based on task requirements and its reasoning about the current state. There are no pre-programmed decision trees—the agent evaluates available tools, matches their capabilities to task needs, and selects appropriately.

This autonomy means **agents may call wrong tools, call right tools with wrong parameters, call too few or too many tools, or process tool responses incorrectly.** These aren't bugs—they're inherent behaviors when non-deterministic reasoning systems interact with tools. Your job is designing tools and descriptions that minimize these failure modes. Improving tool selection happens through selective implementation (fewer, clearer choices), names reflecting natural task subdivisions (easier to match to needs), and comprehensive descriptions (better understanding of tool capabilities).

Claude Sonnet 4.5 has proven "surprisingly efficient at maximizing actions per context window through parallel tool execution." The model can run multiple bash commands simultaneously, enabling higher throughput on complex tasks. This parallel execution capability means well-designed tools that support independent operations can be leveraged far more efficiently than serial workflows.

### State management and context efficiency

**Context is the scarce resource in agent systems.** Unlike traditional software where memory is cheap and abundant, LLM agents face hard limits on how much information they can process at once. Every design decision should optimize context utilization. This means returning concise, relevant information; implementing search over list operations; using filtering and pagination; and consolidating frequently-needed information into single tool responses.

Modern production systems implement sophisticated context management. **Automatic context compaction** summarizes previous messages when approaching context limits, ensuring agents don't suddenly run out of space mid-task. **Context editing** automatically clears stale tool calls and results when approaching token limits. In 100-turn web search evaluations, this reduced token consumption by 84% and improved performance by 29% on complex tasks.

**Memory tools** provide file-based systems for storing information outside the context window. Claude can create, read, update, and delete files in dedicated memory directories that persist across conversations. This client-side operation lets developers control the storage backend. Combined with context editing, memory tools improve performance by 39% over baseline by enabling agents to maintain long-term knowledge while keeping working context lean and focused.

Session management in production SDKs maintains conversation state across multiple turns, supporting both streaming (for interactive, low-latency UX) and single-shot modes (for batch or deterministic runs). Pick the mode per task to balance speed and control. The infrastructure handles the complexity of managing state, caching prompts, and recovering from errors automatically.

## Sub-agents and their relationship to tools

### The three-tier conceptual hierarchy

**Agents, sub-agents, and tools form a clear architectural hierarchy:**

```
PRIMARY AGENT (Orchestrator)
    ↓ delegates complex tasks to
SUB-AGENTS (Specialized Autonomous Agents)
    ↓ execute operations using
TOOLS (Atomic, Deterministic Operations)
```

**Tools are deterministic capabilities**: file operations, API calls, code execution, calculations. They perform specific actions without reasoning or judgment. They're stateless—each invocation is independent. They have predictable, consistent behavior. Think of tools as verbs: Read, Write, Search, Calculate, Query.

**Sub-agents are autonomous agents with specialized expertise**: they have their own context windows, maintain independent reasoning, possess custom system prompts guiding behavior, and have potentially restricted tool access. They're non-deterministic—they reason about how to accomplish tasks. They operate in isolated contexts that don't pollute the main conversation. Think of sub-agents as specialized team members: code-quality, security-auditor, data-analyst, debugger.

This distinction is critical. **Sub-agents are NOT tools.** A tool performs an action. A sub-agent reasons about how to accomplish a goal using available tools. Conflating these concepts leads to architectural confusion and poor design decisions.

### When to use sub-agents versus calling tools directly

**Use tools directly when** performing simple, atomic operations; handling single-step tasks; no specialized reasoning is needed; context fits comfortably in main conversation; or when you're simply reading a file, running a command, or making an API call. The overhead of spinning up a sub-agent isn't justified.

**Use sub-agents when** handling complex, multi-step workflows; specialized domain expertise is required; the task benefits from isolated context; you want to prevent main context pollution; you need parallel processing; the task requires specialized tool configurations; or when you're conducting comprehensive codebase analysis, debugging test failures, performing security audits, or researching across multiple sources. The isolation and specialization provide clear value.

Concrete examples illustrate the distinction:

| Task                          | Approach                      | Reasoning                                    |
| ----------------------------- | ----------------------------- | -------------------------------------------- |
| Read a configuration file     | Tool: `Read`                  | Single atomic operation                      |
| Analyze codebase architecture | Sub-agent: `code-analyzer`    | Multi-file, complex reasoning required       |
| Run test suite                | Tool: `Bash`                  | Single command execution                     |
| Debug test failures           | Sub-agent: `debugger`         | Root cause analysis, iterative investigation |
| Search for text pattern       | Tool: `Grep`                  | Single pattern-matching operation            |
| Security audit entire project | Sub-agent: `security-auditor` | Domain expertise, systematic review          |

### Sub-agent configuration and tool inheritance

Sub-agents are configured with YAML frontmatter in Markdown files:

```yaml
---
name: code-quality # Unique identifier (lowercase, hyphens)
description: Use for code quality reviews # Activation criteria (natural language)
tools: Read, Grep, Glob # Optional: specific tools
model: opus # Optional: sonnet/opus/haiku/inherit
---
System prompt defining the sub-agent's expertise and behavior.
Include specific instructions, examples, and guidance.
```

**Tool inheritance** follows an important pattern. **Default behavior (omitting the `tools` field):** The sub-agent inherits ALL tools from the main thread, including all MCP server tools. This provides maximum flexibility—the sub-agent can use whatever tools it needs to accomplish its task.

**Explicit tool restriction (specifying `tools`):** The sub-agent has access only to the listed tools. This implements the principle of least privilege—restrict powerful capabilities to sub-agents that genuinely need them. Use this pattern for:

- Read-only sub-agents (analysts, reviewers): `tools: Read, Grep, Glob`
- Safe modification sub-agents (formatters, fixers): `tools: Read, Edit, Bash`
- Implementation sub-agents needing full access: omit `tools` field or list all needed tools

Security and safety depend on appropriate tool restrictions. A code reviewer shouldn't have write access. An analyzer focused on gathering information shouldn't execute arbitrary bash commands. Think through what capabilities each sub-agent genuinely needs, and grant the minimum set that enables effective operation.

### Delegation patterns and coordination

**Automatic delegation** happens when the primary agent analyzes task requirements and selects an appropriate sub-agent based on the description field. Make descriptions specific and action-oriented for best results. Use phrases like "MUST BE USED for security reviews" or "Use PROACTIVELY to run tests after code changes" when you want automatic invocation for specific scenarios.

**Explicit delegation** occurs when the user or agent specifies the sub-agent by name: "Use the security-auditor to scan for vulnerabilities" or "Have the debugger investigate this error." This provides direct control over which specialist handles which task.

**Parallel delegation** enables multiple sub-agents to work simultaneously, each in isolated contexts. The main agent coordinates their work and merges results. This dramatically accelerates complex tasks: one sub-agent develops the backend API while another builds the frontend interface; or security-auditor, performance-analyzer, and code-quality all examine the codebase in parallel, with the main agent synthesizing their findings into a comprehensive report.

**Sequential chained delegation** flows work through specialized stages. Examples from production systems: PM spec → architect review → development-tester; incident response → devops troubleshooter → error detective → performance engineer. Human-in-the-loop (HITL) patterns let people approve handoffs between sub-agents, balancing autonomy with control.

### Context isolation benefits

**Why separate contexts matter profoundly:** Sub-agents prevent context pollution—their deep analysis doesn't clutter the main conversation. The main agent maintains focus on high-level objectives rather than drowning in implementation details. Sub-agents can deeply explore domains without distraction. Multiple contexts enable concurrent operations and preserve token budget by preventing exponential growth of the main context with every deep investigation.

This isolation makes longer overall sessions possible. Without sub-agents, a complex task requiring deep analysis of dozens of files would rapidly exhaust the main agent's context. With sub-agents, the main agent's context contains only: project goals, architecture decisions, user requirements, and synthesized summaries from sub-agent work. Meanwhile, sub-agent contexts hold the detailed file analyses, extensive search results, and implementation specifics. This separation of concerns enables sophisticated workflows that would otherwise be impossible.

## Organizational patterns and tool ecosystems

### Grouping tools via namespacing and MCP servers

**The Model Context Protocol (MCP) provides standardized integration to external services.** Tools are grouped by domain or service into MCP servers—collections of related capabilities. Examples: a `database-tools` server with query, update, and schema tools; a `github` server with issue creation, PR management, and code review tools; a `slack` server with message sending, channel management, and user lookup tools.

MCP servers follow a clear namespacing convention: `mcp__{server-name}__{tool-name}`. This prevents naming conflicts and makes tool organization explicit: `mcp__github__create_issue`, `mcp__postgres__query`, `mcp__slack__send_message`. The benefits are substantial: logical organization by domain, shared authentication and configuration per server, easy enablement or disablement of tool groups, clear ownership and maintenance boundaries.

**Namespacing strategies vary and matter.** You can namespace by service (`asana_search`, `jira_search`) or by resource (`asana_projects_search`, `asana_users_search`). Research shows that selecting between prefix-based and suffix-based namespacing has "non-trivial effects" on tool-use evaluations, with effects varying by LLM. Choose your naming scheme based on your own evaluations with your specific models and tasks.

Namespacing helps agents select the right tools at the right time by: reducing the number of tools and tool descriptions loaded into context, offloading agentic computation from context back into tool design, reducing the agent's overall risk of making mistakes, and preventing confusion when tools overlap in function or have vague purposes.

### Sub-agent organization and discovery

**Storage hierarchy determines precedence:**

```
Project-level:  .claude/agents/     (highest priority, version controlled)
User-level:     ~/.claude/agents/   (personal preferences, across projects)
```

Project-level sub-agents win on name collision and get shared via version control, enabling teams to collaborate on and improve agent configurations. User-level sub-agents provide personal customization without affecting team workflows. This separation supports both team standards and individual preferences.

**Naming conventions significantly impact usability.** Use descriptive, role-based names that clearly indicate purpose: `code-quality`, `security-auditor`, `test-runner`, `api-documenter`. Prefer lowercase with hyphens for consistency. Avoid generic names like `helper` or `agent1`—specificity helps both humans and the orchestrating agent understand when to use each sub-agent.

Sub-agents are auto-discovered from configured directories. They're listed in agent management interfaces and can be invoked by name or auto-selected based on context matching. This discoverability means creating new sub-agents immediately makes them available throughout the system without manual registration or configuration updates.

### Command hierarchies and configuration scopes

**Slash commands provide high-level interfaces** for common operations. Built-in commands handle configuration (`/config`), agent management (`/agents`), MCP server configuration (`/mcp`), and permission management (`/permissions`). Custom commands can be defined as Markdown files in `.claude/commands/`, providing reusable workflows that orchestrate sub-agents and tools for frequently performed tasks.

**Configuration operates at three scopes**, each serving distinct purposes. Local/project scope (`.mcp.json` in project root) gets shared via version control for team collaboration. Project scope provides team-wide shared configuration for infrastructure and standards. User scope maintains personal settings, credentials, and preferences across all projects. This layered approach lets teams standardize on shared infrastructure while individuals customize their environments.

**Scope selection strategy:** Use project scope for team tools, shared infrastructure like databases and APIs, and standard development workflows. Use user scope for personal tools, individual credentials, and workflow preferences. Use local scope for project-specific development tools and configurations that shouldn't affect other projects. This separation prevents conflicts and enables appropriate sharing.

## Workflow design: creating, testing, and refining

### Building and improving tools iteratively

**The prototyping workflow starts simple:** Use Claude Code to generate initial tool implementations—often achievable in one-shot with proper documentation. Provide LLM-friendly documentation like flat `llms.txt` files from official documentation sites. Wrap tools in local MCP servers or desktop extensions. Connect for testing via CLI (`claude mcp add <name> <command> [args...]`) or GUI settings. Conduct manual testing to identify rough edges, collect user feedback, and build intuition around use cases.

**Iterative refinement leverages agents themselves.** Concatenate evaluation transcripts and provide them to Claude Code. Claude can analyze transcripts and refactor multiple tools at once, ensuring implementations and descriptions remain self-consistent with changes. The Anthropic team notes: "Most of the advice in this post came from repeatedly optimizing our internal tool implementations with Claude Code." Even expert, human-written tools can be improved by Claude-optimized versions, extracting additional performance beyond what experienced developers achieve alone.

**Building effective evaluations requires real-world grounding.** Generate evaluation tasks using Claude Code to explore tools and create dozens of prompt-response pairs. Ground evaluations in realistic data sources and services—avoid overly simplistic "sandbox" environments. Strong tasks require multiple tool calls, potentially dozens, and reflect actual complexity users will encounter. Use held-out test sets to prevent overfitting to your development examples.

Examples of strong versus weak evaluation tasks:

**Strong (complex, multi-step):** "Schedule a meeting with Jane next week to discuss our latest Acme Corp project. Attach the notes from our last project planning meeting and reserve a conference room."

**Weak (too simple):** "Schedule a meeting with jane@acme.corp next week."

**Strong (requires investigation):** "Customer ID 9182 reported they were charged three times for a single purchase attempt. Find all relevant log entries and determine if any other customers were affected by the same issue."

**Weak (too direct):** "Search the payment logs for purchase_complete and customer_id=9182."

### Validation and metrics

**Track comprehensive metrics** to understand tool and agent performance. Monitor top-level accuracy of task completion, total runtime of individual tool calls and full tasks, total number of tool calls (reveals efficiency), total token consumption (context efficiency), tool error rates (reliability), and patterns of which tools get called (common workflows, consolidation opportunities).

**Verification methods** range from exact string comparison between expected and actual outputs, to enlisting Claude to judge responses (for subjective tasks), to automated testing of outcomes. Avoid overly strict verifiers that reject correct responses due to spurious formatting differences. Optionally specify expected tool sequences to measure tool comprehension, but don't overfit to single strategies—there may be multiple valid approaches.

**Use advanced evaluation features** to gain deeper insights. Turn on interleaved thinking for chain-of-thought behaviors. Include reasoning and feedback blocks in system prompts. Probe why agents do or don't call certain tools. Read through evaluation agents' reasoning to identify rough edges, but remember: "What agents omit in their feedback and responses can often be more important than what they include. LLMs don't always say what they mean." Review raw transcripts including tool calls and responses to spot patterns invisible in summary metrics.

**Real-world example of insight through evaluation:** When launching a web search tool, engineers discovered Claude was needlessly appending "2025" to the query parameter, biasing results toward recent content. This wasn't mentioned in agent feedback—it appeared only by examining the actual tool calls being made. The issue was fixed by improving the tool description to clarify temporal handling.

### Integration patterns with MCP and permission systems

**MCP dramatically reduces integration complexity.** Simply add a remote MCP server URL to your API request. The infrastructure handles connection management, tool discovery, and error handling automatically. No need to write custom integration code or manage OAuth flows. Authentication and API calls happen transparently. Examples like Slack, GitHub, Google Drive, and Asana work out-of-box. The growing ecosystem means new capabilities without building one-off integrations.

**Permission modes balance autonomy with control:**

- `manual`: Require approval for each action (maximum safety)
- `acceptEdits`: Auto-accept file edits but prompt for other operations
- `acceptAll`: Auto-accept all actions (fully autonomous)

Permission systems typically start restrictive and gradually allow more autonomy. Before each tool use, check if the tool is on the allowlist. If not auto-approved, prompt the user. They can approve once, allow all future uses, or block. This creates an allowlist over time, eventually enabling mostly autonomous operation with appropriate safety guardrails.

**Hooks enable workflow automation and safety layers.** Execute custom commands configured in settings, respond to tool events, and trigger actions at specific points. Examples: run test suite automatically after code changes, trigger linting before commits, log all file modifications for audit trails. Hooks can also implement human-in-the-loop approval for critical operations, ensuring people review high-risk actions before execution.

## Use case guidance and patterns

### Financial research and reporting

**Finance agents need several specialized capabilities:** understanding portfolio composition and investment goals, evaluating investments by accessing external market data APIs, storing historical data and running code for quantitative calculations, and handling everything from entry-level analysis to advanced predictive modeling. This transforms "manual audit preparation into intelligent risk management."

Production systems leverage code execution tools for data analysis and visualizations, files APIs for storing and accessing reports across sessions, extended prompt caching (1-hour time-to-live) for maintaining context during lengthy analyses, and memory tools for building institutional knowledge bases over time. These capabilities enable "investment-grade insights that require less human review" even for complex scenarios like structured products and portfolio screening.

**Design tools specifically for financial data retrieval.** Implement search operations over list operations to avoid overwhelming agents with full datasets. Return relevant excerpts with surrounding context rather than raw data dumps. Use filtering and pagination to manage large time series. Include data validation and error checking within tools to catch anomalies before they reach the agent. Consider implementing a `get_company_financials` tool that consolidates income statements, balance sheets, and cash flow statements rather than separate tools for each.

### Data retrieval: agentic search versus semantic search

**Start with agentic search, add semantic search only if needed.** Agentic search means dynamic context gathering on demand—the agent uses tools like bash scripts (grep, tail, sed) to load relevant context. This approach is typically more accurate, easier to maintain, and more transparent than building complex RAG pipelines. The agent reasons about what information it needs and retrieves it specifically.

Semantic search (RAG) with embeddings is usually faster but often less accurate. It requires chunking, embedding generation, vector storage, and complex retrieval logic. It's more difficult to maintain as the knowledge base evolves. Only add semantic search if you demonstrably need faster results or need to handle enormous variation in potential queries that makes targeted search impractical.

**The file system itself represents information pulled into the model's context.** For large files like logs or document uploads, let the agent decide the loading method. Agents use bash scripts to efficiently extract relevant portions rather than reading entire files. This respects the fundamental constraint: context is scarce, storage is abundant. Design around this asymmetry.

### Multi-agent systems and coordination patterns

**Three proven architectural patterns** emerge from production systems:

**Main orchestrator plus specialized sub-agents:** The primary agent handles coordination and high-level objectives. Sub-agents manage specific operations—file operations, analysis, searches, API interactions. Parallel processing enables efficient implementation of complex features. The orchestrator maintains the mental model of the overall task while specialists focus on their domains.

**Pipeline architecture:** Sequential delegation flows work through specialized stages. Examples: PM spec → architect review → development-tester for feature development; incident response → devops troubleshooter → error detective → performance engineer for production debugging. Hooks manage handoffs between stages, potentially with human-in-the-loop approval for critical transitions.

**Multi-model architecture:** Expose tools that forward requests to other models and return summarized verdicts (pass/warn/block). Use the best model for each task—one model orchestrates while others provide specialized capabilities. Example: Claude Code as orchestrator with best-of-breed specialized models for security review, performance analysis, and code quality assessment.

**Coordination strategies vary by use case.** Explicit orchestration provides Claude with clear steps showing delegated operations and expected outcomes. Automatic coordination lets the system intelligently sequence specialists based on task requirements without pre-programmed workflows. Human-in-the-loop approval requires people to review and approve handoffs for safety-critical operations. Choose based on task predictability, risk tolerance, and need for adaptability.

### Claude Agent SDK specific considerations

The Claude Agent SDK is production infrastructure that powers Claude Code, now available to developers. It provides battle-tested solutions to hard problems: memory management, permission systems, multi-agent coordination, automatic context compaction, session management, error handling, and prompt caching. This "infrastructure as product" approach means developers inherit six months of production refinement rather than rebuilding from scratch.

**Key SDK capabilities** include built-in error handling and retries, session management across multiple turns, monitoring and observability hooks, automatic prompt caching with extended TTL, context editing and compaction, memory tools for persistent storage, permission management with gradual autonomy, sub-agent coordination infrastructure, and MCP protocol integration. These features work together to enable sophisticated agentic systems without requiring developers to solve low-level infrastructure challenges.

**Authentication options** support multiple deployment patterns: basic API key authentication via environment variables, Amazon Bedrock integration with AWS credentials, Google Vertex AI integration with GCloud credentials. Note that Claude.ai rate limits cannot be used for third-party products built on the SDK—you need appropriate API access.

**Model selection** per sub-agent enables cost and performance optimization. Default to Claude Sonnet 4.5 for sophisticated reasoning. Use Haiku for fast, simple tasks where cost efficiency matters. Use Opus for complex analysis or critical operations requiring maximum capability. Use `inherit` to maintain consistency between main conversation and sub-agent model. This tiered approach optimizes the cost-performance tradeoff across different parts of your workflow.

## Key principles and recommendations

### Core design principles applicable across platforms

**Design for agent affordances, not just functional completeness.** The question isn't "does this expose system functionality?" but "does this enable agents to accomplish real-world tasks efficiently?" Optimize for limited context, token-by-token processing, and reasoning patterns rather than traditional software contracts.

**Context is the critical, scarce resource.** Every design decision should minimize context consumption. Return concise, relevant information. Implement search over list operations. Consolidate frequently chained operations. Use filtering, pagination, and truncation with sensible defaults. The 84% token reduction from context editing in production systems shows the magnitude of impact possible.

**Evaluation-driven development is essential, not optional.** You can't predict ergonomic tools without hands-on testing with real tasks. Build evaluations grounded in realistic use cases. Track comprehensive metrics. Use held-out test sets to prevent overfitting. Even expert implementations improve through systematic evaluation and iteration. Let agents help optimize the tools they'll use—this feedback loop has proven transformative.

**Simplicity first, complexity only when needed.** Start with the simplest solution—often a single LLM call optimized with retrieval and in-context examples. Add multi-step workflows only when simpler approaches fall short. Use agents for open-ended problems, workflows for predictable tasks. Measure performance continuously and add complexity only when it demonstrably improves outcomes.

**Invest in agent-computer interfaces like human-computer interfaces.** Small refinements to tool descriptions yield dramatic improvements. Error messages, parameter names, response formats, documentation—all are prompt engineering opportunities deserving careful attention. Tool definitions should receive as much prompt engineering effort as system prompts.

### Actionable guidelines for practitioners

**For tool designers:** Start with 3-5 high-impact tools, not comprehensive API coverage. Name tools based on natural task subdivisions. Consolidate frequently chained operations into single tools. Return only contextually relevant information. Resolve technical IDs to semantic names. Implement response_format parameters for flexibility. Set sensible token limits. Prompt-engineer tool descriptions like onboarding documentation. Test with real-world evaluation tasks. Let agents help optimize your tools.

**For agent builders:** Use the feedback loop—gather context, take action, verify work, repeat. Start with agentic search; add semantic search only if demonstrably needed. Leverage sub-agents for parallelization and context management. Use memory tools for persistent knowledge across sessions. Enable context editing for long-running tasks. Implement HITL approval for critical operations. Track token consumption and tool calling patterns. Build evaluations from real-world use cases. Iterate based on metrics and agent behavior.

**For teams:** Version control project-level sub-agents for collaboration. Establish naming conventions for tools and sub-agents. Create shared sub-agent libraries for common tasks. Use hooks for automated workflow steps. Integrate MCP servers for standardized tool access. Monitor and share evaluation results. Document domain-specific knowledge in tool descriptions. Balance autonomy with appropriate permission controls. Review and refine collectively based on production experience.

### Platform-agnostic principles versus implementation specifics

The fundamental principles—three-tier architecture (agent/sub-agent/tool), context as scarce resource, evaluation-driven iteration, tool consolidation over proliferation, semantic over technical identifiers, least privilege access control, isolation for specialization—apply universally regardless of platform. These reflect inherent properties of LLM-based systems rather than implementation choices.

Implementation patterns from Claude Code and the SDK—MCP protocol specifics, `.claude/` directory structures, slash command syntax, specific tool names like Read/Write/Edit, permission system details—are platform-specific but reveal universal design considerations. Any agent platform needs mechanisms for: grouping related tools, managing permissions, organizing specialized agents, handling context limits, and coordinating between components. The specific APIs differ but the architectural challenges remain.

## Conclusion

Effective agent systems emerge from respecting fundamental constraints. LLMs have limited context compared to abundant computer memory. They process information token-by-token rather than iterating efficiently. They make reasoning-based decisions about tool usage rather than following programmed logic. Designing effective tools and agents requires embracing these differences rather than fighting them.

**The most powerful pattern is using agents to build better tools for agents.** This evaluation-driven feedback loop—where Claude Code analyzes transcripts and refactors tools, where systematic testing reveals emergent behaviors and optimization opportunities, where even expert implementations improve through iteration—has produced the design principles documented here. It represents a fundamentally new approach to software development where the distinction between developer and user blurs.

The three-tier architecture of primary agents, specialized sub-agents, and atomic tools provides clear separation of concerns that scales effectively. Orchestrators maintain high-level context and coordination. Specialists operate in isolated contexts with domain expertise. Tools provide deterministic capabilities. This hierarchy enables sophisticated workflows while managing the scarcest resource: context.

Success in this space isn't about building the most sophisticated system—it's about building the right system for your needs. Start simple with direct API calls and targeted tools. Measure performance systematically with realistic evaluations. Add complexity only when it demonstrably improves outcomes. Let agents help optimize the tools they use. Invest in agent-computer interfaces with the same rigor you'd invest in human-computer interfaces. And remember: evaluation-driven iteration beats theoretical optimization every time.
