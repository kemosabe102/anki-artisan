# Delegation Examples: Architecture Enhancer

Sample orchestrator delegation patterns for architecture-enhancer agent.

---

## Example 1: Simple Architecture Section Population

**Scenario**: Plan has `[Architecture.*]` placeholders needing population.

**Orchestrator Delegation**:
```markdown
Task(architecture-enhancer,
  "Populate the Architecture & Design section in docs/01-planning/features/PLAN-auth-service.md.
   Focus on: microservices patterns, FastAPI best practices, PostgreSQL integration.
   Research depth: standard")
```

**Expected Output**:
- Architecture section with specific patterns (Clean Architecture, Repository Pattern)
- Technology rationale with Context7 sources
- Component boundaries and responsibilities
- Zero `[Architecture.*]` placeholders remaining

---

## Example 2: Full Plan Enhancement with Research

**Scenario**: New feature plan needs complete technical architecture.

**Orchestrator Delegation**:
```markdown
Task(architecture-enhancer,
  "Enhance docs/01-planning/features/PLAN-data-pipeline.md with full technical architecture.

   Architecture context:
   - System type: data_pipeline
   - Tech stack preferences: Python 3.13, Redis Streams, PostgreSQL
   - Performance requirements: 10k events/sec throughput, <100ms latency
   - Integration: existing auth service, user database

   Research depth: deep
   Validate completion: true")
```

**Expected Output**:
- All technical sections populated with Context7-researched content
- Event-driven architecture patterns applied
- Performance optimization strategies documented
- Integration specifications with existing services
- Cleanup tasks if replacing existing components

---

## Example 3: Multi-Placeholder Replacement with Cleanup

**Scenario**: Plan references outdated components that need replacement.

**Orchestrator Delegation**:
```markdown
Task(architecture-enhancer,
  "Enhance docs/01-planning/features/PLAN-user-management.md.

   Special focus:
   1. Check Component Almanac for reuse opportunities
   2. Generate cleanup tasks for any replaced components
   3. Document extend vs replace decisions with rationale

   Architecture context:
   - System type: api_service
   - Integration: existing auth, user_database, notification_service

   Research depth: standard")
```


**Expected Output**:
- Technical sections with code reuse analysis
- Build vs Extend vs Replace decision matrix populated
- Cleanup tasks section with:
  - Files to remove (paths, line counts)
  - Tests to update
  - Documentation changes needed
  - Estimated effort per cleanup item
- Tech debt reduction metrics

---

## Example 4: NFR-Focused Enhancement

**Scenario**: Plan needs non-functional requirements populated.

**Orchestrator Delegation**:
```markdown
Task(architecture-enhancer,
  "Populate NFR sections in docs/01-planning/features/PLAN-payment-gateway.md.

   Focus areas:
   - Performance: response time, throughput targets
   - Security: PCI-DSS compliance patterns
   - Availability: 99.99% uptime requirements
   - Scalability: horizontal scaling approach

   Research depth: deep (security-critical)")
```

**Expected Output**:
- Performance targets with monitoring strategy
- Security patterns with Context7-validated approaches
- Availability architecture (failover, redundancy)
- Scalability design (load balancing, caching)
- All `[NFR.*]` placeholders replaced

---

## Input Schema Reference

See `../schemas/architecture-enhancer.schema.json` for complete input/output contract.

**Required Fields**:
- `plan_file_path`: Path to existing plan file
- `context`: Enhancement requirements and focus
- `execution_timestamp`: ISO 8601 UTC timestamp

**Optional Fields**:
- `architecture_context`: System type, tech preferences, performance requirements
- `research_depth`: basic | standard (default) | deep
- `validate_completion`: true (default) | false
