# Escalation Protocol

**Purpose**: Define when and how the orchestrator escalates decisions to the user.

---

## Severity Levels

| Severity | Quantitative Trigger | Action | Message Format |
|----------|---------------------|--------|----------------|
| **CRITICAL** | Security keywords + write ops + test coverage <50% | Halt, await approval | `[CRITICAL] Security operation requires explicit approval: {description}` |
| **BLOCKING** | ASC <0.40 for top 3 agents OR CQ <0.50 | Present options | `[BLOCKING] No agent fit >=0.50. Top candidates: {list}. Recommend: {action}` |
| **ADVISORY** | CQ 0.70-0.84 after 2+ iterations OR confidence <0.75 | Inform, continue | `[ADVISORY] Context incomplete ({CQ}). Proceeding with uncertainty in: {areas}` |

---

## Rate Limits (Per Session)

| Severity | Max Escalations | Action When Exceeded |
|----------|-----------------|---------------------|
| CRITICAL | 3 | Auto-block session |
| BLOCKING | 5 | Suggest /help |
| ADVISORY | Unlimited | Informational only |

---

## Security Keywords (Trigger CRITICAL)

**Authentication**: auth, authentication, login, signin, session, token, jwt, oauth

**Financial**: payment, transaction, billing, checkout, stripe, financial

**Cryptographic**: crypto, encryption, decrypt, keys, secrets, certificates, tls, ssl

**Security**: security, vulnerability, exploit, injection, xss, csrf

---

## Escalation Decision Tree

```
1. Is task security-related (see keywords above)?
   YES + write operation + coverage <50% → CRITICAL
   
2. Is there an agent fit?
   ASC <0.40 for all top 3 → BLOCKING
   
3. Is context sufficient?
   CQ <0.50 → BLOCKING
   CQ 0.70-0.84 after 2+ research iterations → ADVISORY
   
4. None of above → Proceed normally
```

---

## Example Messages

**CRITICAL**:
```
[CRITICAL] Security operation requires explicit approval: 
Modifying authentication flow in src/auth/login.ts
Test coverage: 42%. Risk: HIGH.
Awaiting your explicit approval to proceed.
```

**BLOCKING**:
```
[BLOCKING] No agent fit >=0.50. 
Top candidates: development (0.38), debugger (0.35), workflow (0.32)
Recommend: Create new agent for this domain or provide more context.
```

**ADVISORY**:
```
[ADVISORY] Context incomplete (CQ: 0.78). 
Proceeding with uncertainty in: dependency graph, test coverage.
```

---

**See also**: `.claude/docs/00-core/orchestrator-thresholds.md` for threshold values
