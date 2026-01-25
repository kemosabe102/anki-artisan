---
name: plan-risk-assessment
description: >
  Use this skill when analyzing plan steps for risk factors and research needs.
  Detects novel technology, security implications, state complexity, and generates
  research recommendations with MUST/SHOULD/COULD prioritization.
  Trigger keywords: risk assessment, research needs, plan risk, step analysis, research priority.
---

# Plan Risk Assessment

*Analyze plan steps for risk factors and generate prioritized research recommendations*

## Contents

- [Risk Assessment Overview](#risk-assessment-overview)
- [Risk Detection Factors](#risk-detection-factors)
- [Risk Score Calculation](#risk-score-calculation)
- [Priority Classification](#priority-classification)
- [Research Topic Generation](#research-topic-generation)
- [Detection Heuristics](#detection-heuristics)
- [Output Contract](#output-contract)
- [Anti-Patterns](#anti-patterns)
- [Quick Reference](#quick-reference)

---



## Risk Assessment Overview

**Position in Workflow Chain**:
```
plan-intake -> plan-context-synthesis -> plan-risk-assessment (THIS) -> plan-generation -> plan-validation -> plan-presentation
```

**Purpose**: Analyze synthesized plan context to identify steps requiring research before implementation. Outputs prioritized research recommendations that inform plan generation decisions.

### Assessment Flow

```
Synthesized Context Input
    |
+---------------------------------------------------------------+
| STEP 1: Step Extraction                                        |
|   -> Parse feature list from plan-context-synthesis output     |
|   -> Extract steps array from each feature                     |
|   -> Collect technology mentions from description              |
+---------------------------------------------------------------+
    |
+---------------------------------------------------------------+
| STEP 2: Risk Factor Detection                                  |
|   -> Apply 7 detection heuristics per step                     |
|   -> Flag detected factors with confidence scores              |
|   -> Track source text for each detection                      |
+---------------------------------------------------------------+
    |
+---------------------------------------------------------------+
| STEP 3: Risk Score Calculation                                 |
|   -> Apply weighted formula: sum(factors) / 7 * weights        |
|   -> security_implications weight: 2.0                         |
|   -> external_api weight: 1.5                                  |
|   -> all others weight: 1.0                                    |
+---------------------------------------------------------------+
    |
+---------------------------------------------------------------+
| STEP 4: Priority Classification                                |
|   -> MUST: risk_score >= 0.7 OR security_implications          |
|   -> SHOULD: risk_score >= 0.4 AND < 0.7                       |
|   -> COULD: risk_score < 0.4                                   |
+---------------------------------------------------------------+
    |
+---------------------------------------------------------------+
| STEP 5: Research Topic Generation                              |
|   -> Map detected factors to research topic templates          |
|   -> Substitute specific technologies/concerns into templates  |
|   -> Generate rationale for each recommendation                |
+---------------------------------------------------------------+
    |
Research Recommendations Output
```

### Prerequisites

- **Required Input**: Output from plan-context-synthesis skill
- **Required Data**: Feature list with steps, technology mentions, SPEC sections
- **Reference**: COMPONENT_ALMANAC.md for known vs novel technology detection

---



## Risk Detection Factors

**7 Risk Factors** detected in plan steps:

| Factor | Weight | Description | Detection Triggers |
|--------|--------|-------------|-------------------|
| `novel_technology` | 1.0 | Unfamiliar libraries/frameworks not in COMPONENT_ALMANAC.md | New packages, unfamiliar APIs, "first time using" |
| `external_api` | 1.5 | Third-party API dependencies requiring integration | API calls, webhooks, OAuth, external services |
| `security_implications` | 2.0 | Auth, crypto, data handling, secrets management | Password, token, encrypt, auth, credential, secret |
| `state_complexity` | 1.0 | Multi-component state management, side effects | State sync, transactions, cache invalidation |
| `performance_critical` | 1.0 | Latency/throughput requirements mentioned | Milliseconds, throughput, latency, real-time |
| `edge_case_density` | 1.0 | Error paths, boundary conditions, validation | Edge case, error handling, validation, boundary |
| `cross_cutting` | 1.0 | Logging, monitoring, transactions, observability | Logging, metrics, tracing, audit, observability |

### Factor Weight Rationale

- **security_implications (2.0)**: Security failures have highest blast radius. Always MUST priority.
- **external_api (1.5)**: External dependencies introduce integration risk and version constraints.
- **others (1.0)**: Standard risk factors with equal weight.

---



## Risk Score Calculation

### Formula

```
risk_score = weighted_factor_sum / max_possible_score

WHERE:
  weighted_factor_sum = sum(detected_factor_weight for each detected factor)
  max_possible_score = sum(all_factor_weights) = 1.0 + 1.5 + 2.0 + 1.0 + 1.0 + 1.0 + 1.0 = 8.5

WEIGHTS:
  novel_technology:     1.0
  external_api:         1.5
  security_implications: 2.0
  state_complexity:     1.0
  performance_critical: 1.0
  edge_case_density:    1.0
  cross_cutting:        1.0
```

### Calculation Algorithm

```python
def calculate_risk_score(detected_factors: list[str]) -> float:
    """
    Calculate risk score from detected factors.
    
    Args:
        detected_factors: List of factor names detected in step
        
    Returns:
        Risk score between 0.0 and 1.0
    """
    weights = {
        "novel_technology": 1.0,
        "external_api": 1.5,
        "security_implications": 2.0,
        "state_complexity": 1.0,
        "performance_critical": 1.0,
        "edge_case_density": 1.0,
        "cross_cutting": 1.0
    }
    
    max_score = sum(weights.values())  # 8.5
    
    weighted_sum = sum(
        weights.get(factor, 0.0) 
        for factor in detected_factors
    )
    
    risk_score = weighted_sum / max_score
    
    return round(risk_score, 3)
```



### Score Examples

| Detected Factors | Weighted Sum | Risk Score | Priority |
|------------------|--------------|------------|----------|
| `security_implications` only | 2.0 | 0.235 | MUST (security override) |
| `external_api`, `state_complexity` | 2.5 | 0.294 | COULD |
| `novel_technology`, `external_api`, `security_implications` | 4.5 | 0.529 | SHOULD |
| `security_implications`, `external_api`, `state_complexity`, `edge_case_density` | 5.5 | 0.647 | SHOULD |
| All 7 factors | 8.5 | 1.0 | MUST |
| `novel_technology`, `external_api`, `performance_critical`, `edge_case_density`, `cross_cutting` | 5.5 | 0.647 | SHOULD |
| `external_api`, `security_implications`, `state_complexity`, `performance_critical`, `edge_case_density` | 6.5 | 0.765 | MUST |

---

## Priority Classification

### Classification Logic

```python
def classify_priority(risk_score: float, detected_factors: list[str]) -> str:
    """
    Classify research priority based on risk score and factors.
    
    Priority Rules:
      MUST:   risk_score >= 0.7 OR security_implications present
      SHOULD: risk_score >= 0.4 AND < 0.7
      COULD:  risk_score < 0.4
    
    Args:
        risk_score: Calculated risk score (0.0-1.0)
        detected_factors: List of detected factor names
        
    Returns:
        Priority string: "MUST", "SHOULD", or "COULD"
    """
    # Security override: Always MUST regardless of score
    if "security_implications" in detected_factors:
        return "MUST"
    
    # Score-based classification
    if risk_score >= 0.7:
        return "MUST"
    elif risk_score >= 0.4:
        return "SHOULD"
    else:
        return "COULD"
```



### Priority Thresholds

| Priority | Score Threshold | Override Condition | Action |
|----------|-----------------|-------------------|--------|
| **MUST** | >= 0.7 | OR `security_implications` present | Research required before implementation |
| **SHOULD** | >= 0.4, < 0.7 | None | Research recommended, can proceed with caution |
| **COULD** | < 0.4 | None | Research optional, low-risk implementation |

### Security Override Rationale

Security implications always trigger MUST priority regardless of score because:
1. Security failures have organization-wide blast radius
2. Security debt is expensive to remediate post-implementation
3. Compliance requirements may mandate pre-implementation review
4. Attack surface expansion requires explicit acknowledgment

---

## Research Topic Generation

### Factor-to-Topic Mapping

Each detected risk factor maps to specific research topic templates:

```python
RESEARCH_TOPIC_TEMPLATES = {
    "novel_technology": [
        "Best practices for {technology}",
        "{technology} common pitfalls and anti-patterns",
        "{technology} integration patterns in Python"
    ],
    "external_api": [
        "{api} rate limiting and backoff strategies",
        "{api} error handling patterns",
        "{api} authentication and credential management",
        "{api} SDK vs REST API comparison"
    ],
    "security_implications": [
        "OWASP guidelines for {concern}",
        "Security audit checklist for {concern}",
        "{concern} vulnerability patterns",
        "Secure {concern} implementation in Python"
    ],
    "state_complexity": [
        "State management patterns for {context}",
        "Transaction handling in {context}",
        "Cache invalidation strategies for {context}",
        "Eventual consistency patterns"
    ],
    "performance_critical": [
        "Performance optimization for {operation}",
        "Latency reduction techniques for {operation}",
        "Throughput scaling patterns",
        "Profiling and benchmarking {operation}"
    ],
    "edge_case_density": [
        "Edge case testing strategies",
        "Boundary condition validation patterns",
        "Error recovery patterns for {context}",
        "Defensive programming techniques"
    ],
    "cross_cutting": [
        "Observability patterns for {concern}",
        "Structured logging best practices",
        "Distributed tracing implementation",
        "Metrics and alerting for {concern}"
    ]
}
```

### Topic Generation Algorithm

```python
def generate_research_topics(
    step_id: str,
    detected_factors: list[str],
    context: dict
) -> list[str]:
    """
    Generate research topics from detected factors.
    
    Args:
        step_id: Identifier for the step being analyzed
        detected_factors: List of detected risk factor names
        context: Dict with keys like 'technology', 'api', 'concern', 'operation'
        
    Returns:
        List of research topic strings with substitutions applied
    """
    topics = []
    
    for factor in detected_factors:
        templates = RESEARCH_TOPIC_TEMPLATES.get(factor, [])
        
        for template in templates[:2]:  # Limit to 2 topics per factor
            # Substitute context values into template
            topic = template.format(
                technology=context.get("technology", "unknown technology"),
                api=context.get("api", "external API"),
                concern=context.get("concern", "security concern"),
                context=context.get("context", "application context"),
                operation=context.get("operation", "critical operation")
            )
            topics.append(topic)
    
    return topics
```



---

## Detection Heuristics

### Pattern-Based Detection

Each risk factor uses keyword patterns and context analysis for detection.

```python
DETECTION_PATTERNS = {
    "novel_technology": {
        "keywords": [
            "new library", "first time", "unfamiliar", "experimental",
            "prototype", "poc", "proof of concept", "emerging"
        ],
        "negative_check": "component_almanac_lookup",
        "description": "Technology not found in COMPONENT_ALMANAC.md"
    },
    "external_api": {
        "keywords": [
            "api", "webhook", "oauth", "rest", "graphql", "grpc",
            "third-party", "external service", "integration", "sdk"
        ],
        "patterns": [
            r"https?://api\.", r"\.com/api", r"api\..*\.com"
        ],
        "description": "External API dependency detected"
    },
    "security_implications": {
        "keywords": [
            "password", "token", "secret", "credential", "auth",
            "encrypt", "decrypt", "hash", "salt", "jwt", "oauth",
            "permission", "role", "access control", "sanitize",
            "injection", "xss", "csrf", "certificate", "ssl", "tls"
        ],
        "description": "Security-sensitive operation detected"
    },
    "state_complexity": {
        "keywords": [
            "state", "stateful", "cache", "session", "transaction",
            "sync", "synchronize", "consistency", "concurrent",
            "race condition", "mutex", "lock", "atomic", "rollback"
        ],
        "description": "Complex state management detected"
    },
    "performance_critical": {
        "keywords": [
            "latency", "throughput", "performance", "millisecond",
            "real-time", "realtime", "fast", "optimize", "benchmark",
            "scalable", "concurrent", "parallel", "async"
        ],
        "patterns": [
            r"\d+\s*ms", r"\d+\s*milliseconds", r"<\s*\d+\s*second"
        ],
        "description": "Performance requirement detected"
    },
    "edge_case_density": {
        "keywords": [
            "edge case", "boundary", "validation", "error handling",
            "exception", "fallback", "retry", "timeout", "null",
            "empty", "invalid", "malformed", "overflow", "underflow"
        ],
        "description": "High edge case density detected"
    },
    "cross_cutting": {
        "keywords": [
            "logging", "log", "metrics", "monitoring", "tracing",
            "observability", "audit", "telemetry", "instrumentation",
            "alerting", "dashboard", "prometheus", "grafana"
        ],
        "description": "Cross-cutting concern detected"
    }
}
```



### Detection Algorithm

```python
def detect_risk_factors(
    step_text: str,
    feature_description: str,
    component_almanac: set[str]
) -> list[dict]:
    """
    Detect risk factors in a plan step.
    
    Args:
        step_text: The step description text
        feature_description: Parent feature description for context
        component_almanac: Set of known component/technology names
        
    Returns:
        List of detected factors with metadata:
        [{"factor": str, "confidence": float, "source_text": str}]
    """
    combined_text = f"{step_text} {feature_description}".lower()
    detected = []
    
    for factor_name, config in DETECTION_PATTERNS.items():
        # Keyword matching
        keywords = config.get("keywords", [])
        matched_keywords = [kw for kw in keywords if kw in combined_text]
        
        if matched_keywords:
            # Calculate confidence based on keyword density
            confidence = min(len(matched_keywords) / 3, 1.0)
            
            # Special case: novel_technology negative check
            if factor_name == "novel_technology":
                # Extract technology names and check against almanac
                tech_mentions = extract_technology_names(combined_text)
                novel_techs = [t for t in tech_mentions if t not in component_almanac]
                
                if not novel_techs:
                    continue  # Not novel if all techs are known
                    
                confidence = min(len(novel_techs) / 2, 1.0)
            
            detected.append({
                "factor": factor_name,
                "confidence": round(confidence, 2),
                "source_text": matched_keywords[0],
                "description": config.get("description", "")
            })
    
    return detected
```



### Novel Technology Detection

```python
def extract_technology_names(text: str) -> list[str]:
    """
    Extract potential technology/library names from text.
    
    Patterns detected:
      - CamelCase words (likely class/library names)
      - Words ending in common suffixes (.js, -py, etc.)
      - Known technology patterns (redis, postgres, etc.)
    """
    technologies = []
    
    # CamelCase pattern
    camel_pattern = r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b'
    technologies.extend(re.findall(camel_pattern, text))
    
    # Common technology suffixes
    suffix_pattern = r'\b\w+(?:\.js|\.py|-js|-py|DB|MQ|API)\b'
    technologies.extend(re.findall(suffix_pattern, text, re.I))
    
    # Known technology keywords
    known_techs = [
        "redis", "postgres", "postgresql", "mongodb", "mysql",
        "kafka", "rabbitmq", "celery", "docker", "kubernetes",
        "fastapi", "flask", "django", "sqlalchemy", "pydantic"
    ]
    for tech in known_techs:
        if tech in text.lower():
            technologies.append(tech)
    
    return list(set(technologies))


def check_component_almanac(technology: str, almanac_path: str) -> bool:
    """
    Check if technology exists in COMPONENT_ALMANAC.md.
    
    Returns True if technology is known (not novel).
    """
    # Load almanac content (cached)
    almanac_content = read_cached_file(almanac_path).lower()
    
    return technology.lower() in almanac_content
```

---



## Output Contract

### Input Contract

Expects output from `plan-context-synthesis` skill:

```json
{
  "status": "SUCCESS",
  "feature_name": "string",
  "functional_requirements": [
    {
      "id": "FR-XXX",
      "description": "string",
      "priority": "Must|Should|Could|Won't",
      "acceptance_criteria": ["string"],
      "steps": ["string"]
    }
  ],
  "non_functional_requirements": [
    {
      "id": "NFR-XXX",
      "description": "string",
      "category": "performance|security|reliability"
    }
  ],
  "complexity_classification": "SIMPLE|COMPLICATED|COMPLEX|CHAOTIC",
  "dependencies": {
    "internal": ["FR-XXX -> FR-YYY"],
    "external": ["library-name"],
    "blockers": []
  }
}
```



### Output Contract

```json
{
  "status": "SUCCESS",
  "research_recommendations": [
    {
      "step_id": "FR-001-step-2",
      "risk_factors": ["security_implications", "external_api"],
      "risk_score": 0.412,
      "priority": "MUST",
      "research_topics": [
        "OWASP guidelines for authentication",
        "Security audit checklist for JWT handling",
        "OAuth 2.0 rate limiting and backoff strategies",
        "OAuth 2.0 error handling patterns"
      ],
      "rationale": "Step involves JWT token handling with external OAuth provider, requiring security review before implementation"
    },
    {
      "step_id": "FR-003-step-1",
      "risk_factors": ["novel_technology", "state_complexity"],
      "risk_score": 0.235,
      "priority": "COULD",
      "research_topics": [
        "Best practices for Redis caching",
        "Redis common pitfalls and anti-patterns",
        "State management patterns for distributed cache"
      ],
      "rationale": "First use of Redis in codebase for session state"
    }
  ],
  "summary": {
    "total_steps_analyzed": 24,
    "steps_with_risks": 8,
    "must_count": 3,
    "should_count": 4,
    "could_count": 1
  },
  "metadata": {
    "assessed_at": "2025-01-01T10:30:00Z",
    "component_almanac_version": "2025-01-01",
    "assessor_version": "1.0.0"
  }
}
```



### Failure Response

```json
{
  "status": "FAILURE",
  "error_code": "MISSING_CONTEXT_INPUT|NO_STEPS_FOUND|ALMANAC_UNAVAILABLE",
  "error_message": "Human-readable error description",
  "recovery_action": "Suggested fix for the error",
  "partial_data": {
    "steps_analyzed": 5,
    "last_successful_step": "FR-002-step-3"
  }
}
```

### Error Codes

| Code | Condition | Recovery Action |
|------|-----------|-----------------|
| `MISSING_CONTEXT_INPUT` | No plan-context-synthesis output provided | Run plan-context-synthesis first |
| `NO_STEPS_FOUND` | No steps array in any FR | Ensure SPEC.md has step-level detail |
| `ALMANAC_UNAVAILABLE` | Cannot read COMPONENT_ALMANAC.md | Check file path, proceed without novel_technology detection |
| `INVALID_FR_STRUCTURE` | FR entries missing required fields | Validate plan-context-synthesis output |

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `step_id` | string | Yes | Format: `{FR-ID}-step-{N}` or feature step identifier |
| `risk_factors` | array | Yes | List of detected factor names from 7 factors |
| `risk_score` | number | Yes | Calculated score 0.0-1.0 |
| `priority` | string | Yes | MUST, SHOULD, or COULD classification |
| `research_topics` | array | Yes | Generated topic strings with substitutions |
| `rationale` | string | Yes | Human-readable explanation of why research is needed |

---



## Examples

### Example 1: Security-Critical Step

**Input Step**:
```
FR-005: Implement user authentication
Step 2: Generate JWT tokens with refresh token rotation
```

**Detection Results**:
```json
{
  "step_id": "FR-005-step-2",
  "risk_factors": ["security_implications", "state_complexity"],
  "risk_score": 0.353,
  "priority": "MUST",
  "research_topics": [
    "OWASP guidelines for JWT handling",
    "Security audit checklist for token rotation",
    "State management patterns for refresh tokens",
    "Token revocation strategies"
  ],
  "rationale": "JWT token generation with refresh rotation involves security-sensitive cryptographic operations and stateful token management"
}
```

**Priority Determination**: MUST (security_implications override, regardless of 0.353 score)

---

### Example 2: External API Integration

**Input Step**:
```
FR-012: Integrate payment processing
Step 1: Implement Stripe SDK for payment intent creation
```

**Detection Results**:
```json
{
  "step_id": "FR-012-step-1",
  "risk_factors": ["external_api", "security_implications"],
  "risk_score": 0.412,
  "priority": "MUST",
  "research_topics": [
    "Stripe rate limiting and backoff strategies",
    "Stripe error handling patterns",
    "OWASP guidelines for payment processing",
    "PCI-DSS compliance for payment integration"
  ],
  "rationale": "External payment API integration with security implications requires thorough understanding of Stripe patterns and PCI compliance"
}
```



### Example 3: Low-Risk Step

**Input Step**:
```
FR-002: Add user profile page
Step 3: Create profile display component with avatar
```

**Detection Results**:
```json
{
  "step_id": "FR-002-step-3",
  "risk_factors": [],
  "risk_score": 0.0,
  "priority": "COULD",
  "research_topics": [],
  "rationale": "Standard UI component with no detected risk factors"
}
```

**Priority Determination**: COULD (score 0.0, no risk factors detected)

---

### Example 4: Performance-Critical with Edge Cases

**Input Step**:
```
FR-008: Implement real-time data streaming
Step 2: Handle WebSocket reconnection with exponential backoff under 100ms latency requirement
```

**Detection Results**:
```json
{
  "step_id": "FR-008-step-2",
  "risk_factors": ["performance_critical", "edge_case_density", "state_complexity"],
  "risk_score": 0.353,
  "priority": "COULD",
  "research_topics": [
    "Performance optimization for WebSocket connections",
    "Latency reduction techniques for real-time streaming",
    "Edge case testing strategies",
    "Error recovery patterns for connection handling",
    "State management patterns for reconnection logic"
  ],
  "rationale": "Real-time streaming with strict latency requirements and reconnection handling requires performance tuning and edge case coverage"
}
```

**Priority Determination**: COULD (score 0.353 < 0.4 threshold, no security override)

---



## Anti-Patterns

### NEVER DO

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|----------------|------------------|
| Skip security factor detection | Security issues have highest blast radius | Always check security_implications patterns |
| Ignore COMPONENT_ALMANAC.md | Cannot detect novel vs known technologies | Load and check almanac for novel_technology |
| Equal weights for all factors | Security/API risks are higher impact | Use weighted scoring (security: 2.0, API: 1.5) |
| Generate topics without context | Generic topics are not actionable | Substitute specific tech/concern into templates |
| Override MUST for security | Allows security risks to slip through | Security always triggers MUST, no exceptions |
| Assess without FR steps | Missing granular risk analysis | Require steps array in each FR |
| Skip rationale generation | User cannot understand recommendation | Always explain why research is needed |
| Hardcode risk thresholds | Different projects have different risk tolerance | Use configurable thresholds with defaults |

### Detection Anti-Patterns

```
# WRONG: Checking only exact keyword matches
if "security" in text:
    return ["security_implications"]

# CORRECT: Check multiple related keywords with confidence
security_keywords = ["password", "token", "auth", "encrypt", "credential"]
matches = [kw for kw in security_keywords if kw in text.lower()]
if matches:
    confidence = min(len(matches) / 3, 1.0)
    return [{"factor": "security_implications", "confidence": confidence}]
```

### Scoring Anti-Patterns

```
# WRONG: Simple count without weights
risk_score = len(detected_factors) / 7

# CORRECT: Weighted calculation
weights = {"security_implications": 2.0, "external_api": 1.5, ...}
weighted_sum = sum(weights[f] for f in detected_factors)
risk_score = weighted_sum / sum(weights.values())
```

### Priority Anti-Patterns

```
# WRONG: Score-only classification
if risk_score >= 0.7:
    return "MUST"

# CORRECT: Security override + score classification
if "security_implications" in detected_factors:
    return "MUST"  # Security always MUST
if risk_score >= 0.7:
    return "MUST"
```

---



## Quick Reference

```
PLAN RISK ASSESSMENT PROTOCOL:

  Position in Chain:
    plan-intake -> plan-context-synthesis -> plan-risk-assessment -> plan-generation -> plan-validation -> plan-presentation

  Pipeline Steps (in order):
    1. Step Extraction      -> Parse steps from FR features
    2. Risk Factor Detection -> Apply 7 heuristics per step
    3. Risk Score Calculation -> Weighted formula
    4. Priority Classification -> MUST/SHOULD/COULD
    5. Topic Generation      -> Map factors to research topics

  7 RISK FACTORS:
    novel_technology     (1.0) -> Unfamiliar libs not in COMPONENT_ALMANAC.md
    external_api         (1.5) -> Third-party API dependencies
    security_implications (2.0) -> Auth, crypto, secrets, data handling
    state_complexity     (1.0) -> Multi-component state, transactions
    performance_critical (1.0) -> Latency/throughput requirements
    edge_case_density    (1.0) -> Error paths, boundary conditions
    cross_cutting        (1.0) -> Logging, monitoring, observability

  RISK SCORE FORMULA:
    score = sum(detected_factor_weights) / 8.5 (max possible)

  PRIORITY THRESHOLDS:
    MUST:   score >= 0.7 OR security_implications detected
    SHOULD: score >= 0.4 AND < 0.7
    COULD:  score < 0.4

  SECURITY OVERRIDE:
    security_implications ALWAYS triggers MUST, regardless of score

  RESEARCH TOPIC TEMPLATES:
    novel_technology     -> "Best practices for {tech}", "{tech} pitfalls"
    external_api         -> "{api} rate limiting", "{api} error handling"
    security_implications -> "OWASP guidelines for {concern}", "Security audit for {concern}"
    state_complexity     -> "State management for {context}", "Transaction handling"
    performance_critical -> "Performance optimization for {op}", "Latency reduction"
    edge_case_density    -> "Edge case testing strategies", "Boundary validation"
    cross_cutting        -> "Observability patterns", "Structured logging"

  INPUT CONTRACT:
    {
      functional_requirements: [{id, description, steps[], ...}],
      non_functional_requirements: [...],
      dependencies: {external: [...]}
    }

  OUTPUT CONTRACT:
    {
      research_recommendations: [{step_id, risk_factors[], risk_score, priority, research_topics[], rationale}],
      summary: {total_steps_analyzed, steps_with_risks, must_count, should_count, could_count}
    }

  ERROR CODES:
    MISSING_CONTEXT_INPUT  -> Run plan-context-synthesis first
    NO_STEPS_FOUND         -> Ensure SPEC.md has step-level detail
    ALMANAC_UNAVAILABLE    -> Proceed without novel_technology detection

  ALWAYS CHECK:
    - Security factor detection (highest priority)
    - COMPONENT_ALMANAC.md for novel technology detection
    - Weighted scoring (not simple count)
    - Rationale for each recommendation

  NEXT STEP:
    Pass research_recommendations to plan-generation for informed decisions
```

---



## Related Skills

| Skill | Relationship |
|-------|--------------|
| [plan-context-synthesis](../plan-context-synthesis/SKILL.md) | Upstream - provides synthesized context for analysis |
| [plan-generation](../plan-generation/SKILL.md) | Downstream - receives research recommendations |
| [plan-validation](../plan-validation/SKILL.md) | Downstream - validates generated plan |
| [codebase-research](../codebase-research/SKILL.md) | Reference - COMPONENT_ALMANAC.md discovery |
| [library-research](../library-research/SKILL.md) | Execution - performs actual research for MUST topics |

---

## Cross-References

### Documentation

| Document | Purpose |
|----------|---------|
| [COMPONENT_ALMANAC.md](../../../docs/00-project/COMPONENT_ALMANAC.md) | Known component registry for novel technology detection |
| [Thinking Frameworks](../../docs/00-core/frameworks/README.md) | Analysis frameworks for risk assessment |
| [Agent Selection Guide](../../docs/01-guides/agents/agent-selection-guide.md) | Agent assignment for research execution |

### Algorithm Cross-References

| Algorithm | Source Skill | Usage in This Skill |
|-----------|--------------|---------------------|
| Section Detection | plan-context-synthesis | Input parsing |
| FR Extraction | plan-context-synthesis | Step discovery |
| Complexity Classification | plan-context-synthesis | Context for risk weighting |

---

## Thinking Frameworks

**Full Catalog**: [Thinking Frameworks README](../../docs/00-core/frameworks/README.md)

**Most Relevant for Plan Risk Assessment**:

| Framework | When to Use |
|-----------|-------------|
| [Pre-Mortem](../../docs/00-core/frameworks/strategy.md) | Anticipate implementation risks before they occur |
| [SCAMPER](../../docs/00-core/frameworks/creative.md) | Generate research topic variations |
| [Systems Thinking](../../docs/00-core/frameworks/analysis.md) | Understand cross-cutting concern impacts |
| [Cynefin](../../docs/00-core/frameworks/analysis.md) | Match risk level to complexity domain |

> **Selection Tip**: risk anticipation -> Pre-Mortem, topic generation -> SCAMPER, cross-cutting -> Systems, complexity -> Cynefin

