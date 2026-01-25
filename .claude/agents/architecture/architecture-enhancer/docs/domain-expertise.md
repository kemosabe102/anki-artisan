# Domain Expertise: Architecture Enhancement

Detailed patterns and templates for technical architecture population.

---

## Technical Placeholder Patterns

### Common Placeholders to Identify and Replace

| Pattern | Replace With |
|---------|--------------|
| `[NEEDS ARCHITECTURAL ANALYSIS]` | Research-backed architectural analysis with Context7 validation |
| `[Architecture:*]` | Specific patterns (Clean Architecture, Microservices, Event-Driven) |
| `[Technology Choice Name]` | Actual selections (FastAPI, PostgreSQL, Redis, Docker) |
| `[Component Name]` | Concrete component names with technical specifications |
| `[Implementation Approach]` | Specific methodologies and coding standards |
| `[System Interface]` | API designs, message formats, protocol specifications |
| `[Data Flow]` | Concrete data processing pipelines and storage patterns |
| `[Task \d+]` | Specific implementation tasks with time estimates |
| `[Performance Target]` | Specific metrics and monitoring approaches |
| `[Security Standard]` | Concrete security implementations |

### Content Replacement Rules

1. **Context7 Research Required**: All major technical decisions must be research-backed
2. **Specific Technology Names**: Replace generic placeholders with actual libraries/frameworks
3. **Concrete Implementation Details**: Convert placeholder tasks to actionable steps
4. **Measurable Technical Criteria**: Define specific performance, security, quality metrics
5. **Business Content Preservation**: Never modify business sections

---


## Technical Sections to Populate

### Primary Technical Sections

1. **Architecture & Design**
   - System architecture patterns (microservices, monolith, serverless)
   - Component separation and responsibility boundaries
   - Data flow and communication patterns
   - Scalability and performance design

2. **Technology Choices & Rationale**
   - Backend framework selection with Context7 research
   - Database technology and data modeling approach
   - Caching strategy and implementation
   - External service integrations

3. **Implementation Approach**
   - Development methodology and standards
   - Code organization and project structure
   - API design and interface specifications
   - Testing strategy and quality assurance

4. **System Integration**
   - Service communication protocols
   - Authentication and authorization patterns
   - Data synchronization approaches
   - Error handling and recovery mechanisms

### Business Sections to Preserve (NEVER MODIFY)

- Business Context & Strategic Alignment
- Requirements Traceability Framework
- Component Business Descriptions
- Success criteria and business metrics

---


## Operation Phases

### Phase 1: Pre-Processing & Placeholder Analysis
1. Validate plan file exists (Read tool)
2. Load Component Almanac for existing components
3. Scan plan structure for technical sections
4. Generate enhancement checklist with all placeholders
5. Record baseline placeholder count

### Phase 2: Context7 Research & Pattern Validation
1. Conduct architecture research with topic specificity
2. Apply progressive research pattern (2k → 5k → 8k tokens)
3. Validate technology choices against best practices
4. Research integration and security patterns

### Phase 3: Systematic Content Population
1. Process each placeholder from checklist
2. Populate Existing Code Analysis section
3. Complete Build vs Extend vs Replace matrix
4. Replace placeholders with specific content
5. Define integration specifications

### Phase 4: Cleanup Task Generation
1. Generate cleanup tasks for replaced components
2. Populate Technical Debt & Cleanup Tasks section
3. Flag complex areas for tech-debt-investigator
4. Calculate technical debt reduction metrics

### Phase 5: Validation
1. Use Edit tool following file-operation-protocol.md
2. Re-scan for remaining placeholders (must be 0)
3. Verify business sections unchanged
4. Confirm file modification persisted
5. Generate completion evidence

---


## Thin Fill Fallback Templates

When Context7 research is unavailable, use these proven fallback patterns:

### Web Application Architecture
- **Backend**: FastAPI with Pydantic for type safety and automatic OpenAPI documentation
- **Database**: PostgreSQL with SQLAlchemy async drivers for scalable data persistence
- **Caching**: Redis for session management and frequently accessed data
- **API Design**: RESTful APIs with OpenAPI 3.0 specification
- **Authentication**: JWT tokens with secure refresh mechanism
- **Monitoring**: Prometheus metrics with Grafana dashboards

### Microservice Architecture
- **Framework**: FastAPI with dependency injection and middleware support
- **Communication**: HTTP/REST for synchronous, message queues for asynchronous
- **Data Storage**: PostgreSQL per service with event sourcing for cross-service data
- **Service Discovery**: Container orchestration with health check endpoints
- **Observability**: Distributed tracing with OpenTelemetry and centralized logging

### Data Processing Pipeline
- **Framework**: Python with async/await patterns for concurrent processing
- **Storage**: PostgreSQL for structured data, object storage for files
- **Queue Management**: Redis or RabbitMQ for task distribution
- **Monitoring**: Custom metrics for data quality and processing performance
- **Error Handling**: Dead letter queues with retry mechanisms

### Testing Strategy
- **Unit Testing**: pytest with coverage reporting and parameterized tests
- **Integration Testing**: TestClient for API testing with test database
- **Performance Testing**: Load testing with realistic data volumes
- **Security Testing**: Automated scanning for common vulnerabilities

---

## Code Reuse Principles (CRITICAL)

### Prefer Extend Over Create
- **ALWAYS** check Component Almanac before proposing new implementations
- **Default to extension**: Extend via inheritance, composition, or plugins
- **Create new ONLY when**: Extension creates unacceptable coupling
- **Document rationale**: Explain why extension wasn't viable

### Prefer Modify Over Replace
- Incremental enhancement preferred over wholesale replacement
- Replace ONLY when modification creates technical debt
- Document migration risks and rollback strategies

### Mandatory Cleanup for Replacements
- Every replacement generates comprehensive cleanup tasks
- Include: file removal, test updates, documentation, dependency cleanup
- Priority: P1 (blocking), P2 (tech debt), P3 (future work)
