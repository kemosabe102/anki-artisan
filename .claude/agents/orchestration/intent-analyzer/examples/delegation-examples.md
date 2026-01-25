# Intent Analyzer Delegation Examples

How the orchestrator invokes intent-analyzer and processes its outputs.

---

## Example 1: Simple Single-Intent (No Task Graph)

**Input Request**:
```
"Read the authentication service file and explain how it works"
```

**Analysis**:
- Action verbs: ["explain"] (single intent)
- Entity count: 1 (auth service file)
- Domain scope: packages/core/auth/ (inferred)
- Intent clarity: 0.90 (clear request)
- Multi-intent: FALSE

**Output (SUCCESS)**:
```json
{
  "status": "SUCCESS",
  "agent": "intent-analyzer",
  "confidence": 0.9,
  "agent_specific_output": {
    "intent_analysis": {
      "intents": [{
        "intent_id": "I000",
        "action_verb": "explain",
        "target": "authentication service",
        "domain_scope": "packages/core/auth/",
        "entity_count": 1,
        "execution_order": 1,
        "depends_on": [],
        "implicit": false
      }],
      "task_graph": null,
      "implicit_requirements": [],
      "intent_clarity": 0.9,
      "multi_intent": false,
      "compression_ratio": 4.2
    }
  }
}
```


**Orchestrator Action**: Handle directly (no task graph needed, simple read + explain)

---

## Example 2: Multi-Intent Request (Task Graph)

**Input Request**:
```
"Research JWT best practices and implement a new authentication service
in packages/core/auth/. Make sure it integrates with the existing user database."
```

**Analysis**:
- Action verbs: ["research", "implement", "integrate"] (3 intents)
- Entity count: 3 (JWT patterns, auth service, user database)
- Domain scope: packages/core/auth/
- Intent clarity: 0.85
- Multi-intent: TRUE

**Output (SUCCESS)**:
```json
{
  "status": "SUCCESS",
  "agent": "intent-analyzer",
  "confidence": 0.85,
  "agent_specific_output": {
    "intent_analysis": {
      "intents": [
        {"intent_id": "I000", "action_verb": "research", "target": "JWT best practices", "domain_scope": "external", "execution_order": 1, "depends_on": [], "implicit": false},
        {"intent_id": "I001", "action_verb": "implement", "target": "AuthService", "domain_scope": "packages/core/auth/", "execution_order": 2, "depends_on": ["I000"], "implicit": false},
        {"intent_id": "I002", "action_verb": "test", "target": "AuthService", "domain_scope": "tests/core/auth/", "execution_order": 3, "depends_on": ["I001"], "implicit": true}
      ],
      "task_graph": {
        "nodes": ["I000", "I001", "I002"],
        "edges": [
          {"from": "I000", "to": "I001", "type": "sequential"},
          {"from": "I001", "to": "I002", "type": "sequential"}
        ],
        "parallel_groups": [],
        "sequential_chain": ["I000", "I001", "I002"]
      },
      "implicit_requirements": [{
        "requirement_id": "I002",
        "action": "test",
        "target": "AuthService",
        "rationale": "Feature implementation requires test coverage per CLAUDE.md (>80% coverage)"
      }],
      "intent_clarity": 0.85,
      "multi_intent": true,
      "compression_ratio": 3.5
    }
  }
}
```


**Orchestrator Action**:
1. Spawn researcher-external for JWT best practices (I000)
2. Wait for completion, then spawn python-code-implementer for AuthService (I001)
3. Wait for completion, then spawn test-creator for tests (I002)

---

## Example 3: Ambiguous Request (FAILURE)

**Input Request**:
```
"Update the auth system and make it better"
```

**Analysis**:
- Action verbs: ["update"] (vague)
- Entity count: 1 (auth system - ambiguous scope)
- Domain scope: UNCLEAR
- Intent clarity: 0.35 (very vague)
- Multi-intent: UNCLEAR

**Output (FAILURE)**:
```json
{
  "status": "FAILURE",
  "agent": "intent-analyzer",
  "confidence": 0.35,
  "failure_details": {
    "failure_type": "ambiguous_intent",
    "reasons": [
      "Action verb 'update' is ambiguous (could be fix, enhance, refactor)",
      "Target 'auth system' spans multiple domains",
      "'Make it better' lacks specific success criteria"
    ],
    "clarification_questions": [
      "Are you fixing a bug, adding a feature, or improving existing functionality?",
      "Which auth component: core service, API endpoints, or agent authentication?",
      "What specific improvement: performance, security, UX, or code quality?"
    ],
    "recovery_suggestions": [
      "Use specific action verb: 'fix auth bug', 'implement JWT support'",
      "Specify exact component: 'packages/core/auth/service.py'",
      "Define success criteria: 'improve login speed by 50%'"
    ],
    "partial_analysis": {
      "action_verbs_found": ["update"],
      "possible_domains": ["packages/core/auth/", "packages/api/auth/"],
      "intent_clarity": 0.35
    }
  }
}
```

**Orchestrator Action**: Present clarification questions to user, retry after response
