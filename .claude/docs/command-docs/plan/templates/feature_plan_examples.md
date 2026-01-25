# Feature Plan Examples - Real Patterns

This document shows real examples of how to structure features for different types of projects and problems.

## Example 1: API Backend Feature

**Project**: Chat Application API
**Feature**: User authentication system

```json
{
  "id": "AUTH_001",
  "category": "functional",
  "description": "User signup with email validation and password hashing",
  "steps": [
    "Create User model with email, password_hash, created_at fields",
    "Implement password validation: min 8 chars, 1 uppercase, 1 number, 1 special char",
    "Hash password using bcrypt with salt (cost factor 12)",
    "Create POST /api/v1/auth/signup endpoint",
    "Validate email format using regex",
    "Check for duplicate email in database",
    "Create user record and return JWT token",
    "Write unit tests covering valid and invalid inputs",
    "Write integration test for full signup flow",
    "Test password hashing produces different hashes for same password"
  ],
  "acceptance_criteria": [
    "POST /api/v1/auth/signup accepts {email, password}",
    "Returns 201 with {token, user_id} on success",
    "Returns 400 with error message if password too weak",
    "Returns 409 if email already exists",
    "Returns 400 if email format invalid",
    "Password never stored in plain text (verified in DB)",
    "Same password hashes to different values each time",
    "JWT token can be used for subsequent authenticated requests",
    "All unit tests passing (>90% code coverage)",
    "Integration test verifies full signup → login flow"
  ],
  "passes": false,
  "estimated_hours": 2.5
}
```

## Example 2: Data Processing Feature

**Project**: ETL Pipeline
**Feature**: CSV data validation and transformation

```json
{
  "id": "ETL_TRANSFORM_001",
  "category": "functional",
  "description": "Validate CSV structure and normalize data types",
  "steps": [
    "Create CSVValidator class with schema definition",
    "Implement column count validation (must match schema)",
    "Implement required field check (no null in required columns)",
    "Implement data type conversion (string → int, date)",
    "Handle missing values: replace with specified default",
    "Create normalization for string fields (trim, lowercase)",
    "Create date parsing with support for multiple formats",
    "Write unit tests for each validation rule",
    "Write unit tests for edge cases (empty file, malformed dates)",
    "Write integration test: load real CSV, verify transformation"
  ],
  "acceptance_criteria": [
    "CSVValidator rejects file with wrong column count",
    "Rejects file with null in required columns",
    "Converts string columns to int where specified",
    "Parses dates in format YYYY-MM-DD correctly",
    "Parses dates in format MM/DD/YYYY correctly",
    "Replaces missing values with specified defaults",
    "Normalizes strings (removes leading/trailing spaces)",
    "All 12 unit tests passing",
    "Integration test succeeds with sample_data.csv",
    "Transformation preserves data integrity (no loss)"
  ],
  "passes": false,
  "estimated_hours": 2.0
}
```

## Example 3: UI Component Feature

**Project**: React Dashboard
**Feature**: Interactive chart with zoom and filter

```json
{
  "id": "UI_CHART_001",
  "category": "functional",
  "description": "Time-series chart component with zoom and date range filter",
  "steps": [
    "Create Chart component using D3.js/Recharts",
    "Implement data prop (array of {date, value} objects)",
    "Add x-axis as date, y-axis as values",
    "Implement brush control for date range selection",
    "Implement onFilterChange callback when user selects range",
    "Add zoom animation when range selected",
    "Implement date range input fields (alternative to brush)",
    "Add loading state (skeleton/spinner while data fetches)",
    "Write unit tests for data rendering",
    "Test in browser for visual correctness and interactions"
  ],
  "acceptance_criteria": [
    "Chart renders 50+ data points without performance issues",
    "Brush control allows selecting date range",
    "onFilterChange fires with correct date range",
    "Zoom animation completes in <500ms",
    "Date input fields accept YYYY-MM-DD format",
    "Typing in date field updates chart in real-time",
    "Loading state displays while data prop is null",
    "Responsive: works on mobile (375px) and desktop (1920px)",
    "Accessibility: keyboard navigation works (arrow keys)",
    "No console errors or warnings"
  ],
  "passes": false,
  "estimated_hours": 3.0
}
```

## Example 4: Testing Feature

**Project**: Any Project
**Feature**: Comprehensive test suite for existing code

```json
{
  "id": "TEST_SUITE_001",
  "category": "testing",
  "description": "Unit tests for order processing module with 90% code coverage",
  "steps": [
    "Create test_order_creation.py test file",
    "Write test for valid order creation (happy path)",
    "Write test for order with invalid customer ID",
    "Write test for order with out-of-stock items",
    "Write test for applying discount codes",
    "Write test for calculating tax based on state",
    "Write test for zero-quantity items (rejected)",
    "Write test for negative prices (rejected)",
    "Run coverage report and identify uncovered lines",
    "Add tests for uncovered code paths",
    "Verify 90%+ coverage achieved"
  ],
  "acceptance_criteria": [
    "Test file exists: tests/test_order_processing.py",
    "All 8 test cases pass",
    "Test uses mocks for database calls (no real DB)",
    "Test uses fixtures for sample order data",
    "Code coverage report shows >90%",
    "No flaky tests (consistent pass/fail)",
    "Test execution time <5 seconds",
    "All assertions have descriptive failure messages",
    "Edge cases tested (empty orders, max price)",
    "CI/CD runs tests on every commit"
  ],
  "passes": false,
  "estimated_hours": 2.0
}
```

## Example 5: Infrastructure Feature

**Project**: Web Application
**Feature**: Docker containerization and Kubernetes deployment

```json
{
  "id": "INFRA_DOCKER_001",
  "category": "infrastructure",
  "description": "Create Docker image and test containerized app",
  "steps": [
    "Create Dockerfile with Python 3.11 base image",
    "Copy source code and requirements.txt into image",
    "Install dependencies using pip",
    "Set working directory and expose port 5000",
    "Create health check endpoint in app",
    "Build image: docker build -t app:v1.0 .",
    "Test image builds without errors",
    "Run container and verify app responds to requests",
    "Test environment variables are passed correctly",
    "Verify container starts in <5 seconds"
  ],
  "acceptance_criteria": [
    "Dockerfile exists and is syntactically valid",
    "Docker image builds successfully",
    "Image size <500MB (optimized)",
    "Container starts without errors",
    "App responds to HTTP requests on port 5000",
    "Health check endpoint returns 200 OK",
    "Environment variables (DATABASE_URL, etc.) loaded correctly",
    "Container can be stopped gracefully",
    "No security vulnerabilities in base image (docker scan)",
    "Image works on both Intel and ARM architectures"
  ],
  "passes": false,
  "estimated_hours": 1.5
}
```

## Example 6: Documentation Feature

**Project**: Any Project
**Feature**: API documentation with examples

```json
{
  "id": "DOCS_API_001",
  "category": "documentation",
  "description": "Create API documentation with request/response examples",
  "steps": [
    "Create docs/API.md file",
    "Document base URL and authentication method",
    "Document each endpoint: GET /users, POST /users, etc.",
    "For each endpoint: describe parameters, response format",
    "Add curl example for each endpoint",
    "Add JSON request/response examples",
    "Document error responses with status codes",
    "Add rate limiting documentation",
    "Create quick-start guide for new developers",
    "Add troubleshooting FAQ section"
  ],
  "acceptance_criteria": [
    "All 5 endpoints documented",
    "Each endpoint has curl example",
    "Request/response JSON examples are valid and tested",
    "All required parameters documented",
    "All response fields documented",
    "Error codes and messages documented",
    "Rate limiting limits clearly stated",
    "Quick-start explains first API call in <5 minutes",
    "No broken links or typos",
    "Documentation can be rendered as HTML (markdown valid)"
  ],
  "passes": false,
  "estimated_hours": 1.5
}
```

## Example 7: Complex Multi-Step Feature

**Project**: Smart Fear & Greed Indicator (from your example)
**Feature**: Market Regime Classification (Regime Component)

```json
{
  "id": "REGIME_CLASSIFICATION_001",
  "category": "functional",
  "description": "Classify market as Bull/Bear/Neutral based on SPX vs 200-day SMA",
  "steps": [
    "Fetch current SPX price from Yahoo Finance",
    "Fetch SPX 200-day simple moving average",
    "Calculate percentage difference: (SPX - SMA) / SMA * 100",
    "Classify regime: >+2% = Bull, <-2% = Bear, else Neutral",
    "Create RegimeClassifier class with calculate_regime() method",
    "Implement error handling for missing data",
    "Create unit test for Bull regime classification (SPX +3%)",
    "Create unit test for Bear regime classification (SPX -3%)",
    "Create unit test for Neutral regime classification (SPX +0.5%)",
    "Create unit test for edge cases (SPX exactly at +2%, -2%)",
    "Verify deterministic behavior (same date → same result)"
  ],
  "acceptance_criteria": [
    "RegimeClassifier.calculate_regime() returns 'Bull', 'Bear', or 'Neutral'",
    "Bull threshold: SPX > SMA + 2%",
    "Bear threshold: SPX < SMA - 2%",
    "Neutral range: SMA - 2% ≤ SPX ≤ SMA + 2%",
    "Calculation deterministic (tested with historical dates)",
    "All 5 unit tests passing",
    "Edge case tests verify exact boundary conditions",
    "Handles missing data gracefully (returns None, not error)",
    "Percentage calculation verified manually against known dates",
    "Unit tests cover Jan 2, 2024 test date with expected result"
  ],
  "passes": false,
  "estimated_hours": 1.5
}
```

## Example 8: Bug Fix Feature

**Project**: Any Project
**Feature**: Fix critical bug in payment processing

```json
{
  "id": "BUGFIX_001",
  "category": "bug_fix",
  "description": "Fix: Negative refunds incorrectly calculating tax",
  "steps": [
    "Reproduce bug: create refund for $100 order, verify calculation",
    "Identify root cause: tax calculation multiplying by negative amount",
    "Review code in payment_processor.py line 145-155",
    "Implement fix: use abs(amount) in tax calculation",
    "Write unit test that reproduces original bug",
    "Verify test now passes with fix",
    "Run full test suite to verify no regression",
    "Test manual scenario: refund $50 from $100 order",
    "Verify tax calculated correctly for refund",
    "Create regression test so bug doesn't reoccur"
  ],
  "acceptance_criteria": [
    "Original bug reproduced and documented",
    "Root cause identified and explained",
    "Code fix is minimal (single line preferred)",
    "Test case added to prevent regression",
    "All existing tests still pass",
    "Manual testing confirms fix works",
    "No side effects (other refunds work correctly)",
    "Performance not impacted",
    "Customer-facing behavior is correct",
    "Fix deployed to production without issues"
  ],
  "passes": false,
  "estimated_hours": 1.0
}
```

## Example 9: Performance Optimization Feature

**Project**: Web Application
**Feature**: Optimize database queries for report generation

```json
{
  "id": "PERF_OPT_001",
  "category": "performance",
  "description": "Reduce report generation time from 45s to <10s using query optimization",
  "steps": [
    "Profile current report generation query",
    "Identify slow query: N+1 problem in user/orders join",
    "Add database indexes on foreign keys",
    "Rewrite query using eager loading (JOIN vs separate queries)",
    "Test query execution time on production data",
    "Implement query result caching (1-hour TTL)",
    "Write performance benchmark test",
    "Measure before/after execution time",
    "Verify report accuracy not affected by changes",
    "Document optimization for future reference"
  ],
  "acceptance_criteria": [
    "Report generation time reduced from 45s to <10s",
    "95th percentile performance: <15 seconds",
    "Database indexes created successfully",
    "No additional memory usage (caching contained)",
    "Report output identical to before optimization",
    "Benchmark test documents performance improvement",
    "All existing tests still pass",
    "Query uses 1 database call instead of 500+",
    "CPU usage reduced by >50%",
    "No data accuracy regressions"
  ],
  "passes": false,
  "estimated_hours": 2.5
}
```

## Example 10: Integration Feature

**Project**: Multi-service Application
**Feature**: Integrate payment service with accounting system

```json
{
  "id": "INTEGRATION_PAYMENT_001",
  "category": "functional",
  "description": "Create webhook handler to sync payments to accounting ledger",
  "steps": [
    "Review payment service API documentation and webhook format",
    "Create POST /webhooks/payment endpoint",
    "Implement signature verification for webhook payload",
    "Parse webhook: extract payment_id, amount, status",
    "Create JournalEntry in accounting system",
    "Map payment type to accounting categories",
    "Implement idempotency check (same webhook twice = one entry)",
    "Add error handling and retry logic",
    "Write unit tests for webhook parsing and validation",
    "Write integration test with mock payment service",
    "Test end-to-end: simulate payment → verify ledger entry"
  ],
  "acceptance_criteria": [
    "POST /webhooks/payment receives and processes webhook",
    "Webhook signature verified correctly",
    "Journal entry created for each payment",
    "Mapping of payment type to accounting category correct",
    "Duplicate webhooks create only one ledger entry",
    "Payment of $100 creates correct accounting entries (debit/credit balanced)",
    "All unit tests passing (>85% coverage)",
    "Integration test passes",
    "Error responses logged and don't crash system",
    "Latency <500ms per webhook (non-blocking)"
  ],
  "passes": false,
  "estimated_hours": 3.0
}
```

## Common Patterns Across Examples

**Pattern 1: Steps + Criteria Alignment**
- Each step produces something verifiable
- Each criterion tests something from the steps
- No criterion tests something not implemented by steps

**Pattern 2: Concrete, Not Abstract**
- ❌ "Implement authentication" (too vague)
- ✅ "Create POST /auth/login endpoint accepting {username, password}, returning JWT"

**Pattern 3: Progressive Detail**
- Start high-level (what to build)
- Get progressively concrete (how to verify)
- Include specific test data, edge cases, exact thresholds

**Pattern 4: Time Estimates**
- 0.5-1h: Tiny features (one class, simple test)
- 1-2h: Small features (complete module, good test coverage)
- 2-3h: Medium features (multi-component, integration tests)
- 3h+: Split into smaller features

**Pattern 5: Test Coverage**
- Unit tests: individual functions/methods
- Integration tests: components working together
- End-to-end tests: user perspective
- All three levels for robust verification

## Using These Examples

1. **For new projects**: Choose the example closest to your type (API, data, UI, etc.)
2. **Customize for your domain**: Change names, add domain-specific criteria
3. **Keep the structure**: steps → acceptance_criteria pattern is universal
4. **Adjust time estimates**: Your team may be faster/slower (track actual time for calibration)
5. **Break large features**: If >3 hours, split into multiple 1-2 hour features

---

**Key Insight**: Good features are independently implementable and verifiable. They don't require other features to be complete (except for dependencies noted in the plan). This enables parallel work and prevents blocking.
