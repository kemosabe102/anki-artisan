# Security & Domain Expertise for Researcher-Web

**Purpose**: Security posture, allowed domains, and compliance requirements

---

## Security Posture

**Risk Level**: HIGH (External content access, web scraping)

**Security Framework**: `.claude/docs/01-guides/security/tool-security-best-practices.md` (5-Layer Security Model)

### Active Security Layers

| Layer | Control | Implementation |
|-------|---------|----------------|
| **Layer 3** | Content Moderation | SSRF prevention, content sanitization |
| **Layer 4** | Processing Controls | Rate limiting, token budget enforcement |
| **Layer 5** | Output Validation | Secrets detection, response filtering |

### Security Hooks

| Hook | Purpose | Location |
|------|---------|----------|
| `security-validate-url.py` | SSRF prevention | `.claude/hooks/security/validate_url.py` |
| `security-sanitize-content.py` | Content sanitization | `.claude/hooks/security/sanitize_content.py` |
| Domain whitelist | 177 approved domains | `validate_url.py:APPROVED_DOMAINS` |

---

## Threat Mitigation

| Threat | Mitigation | Automation |
|--------|------------|------------|
| SSRF attacks | Domain whitelist + IP validation | Hooks (automatic) |
| Content injection | HTML/JSON sanitization | Hooks (automatic) |
| DoS attacks | Response size (5MB) + timeout (30s) | Hooks (automatic) |
| Data exfiltration | No write permissions + prompt injection detection | Agent design |

---

## OWASP LLM Top 10 Compliance

**Compliance Score**: 7/10 applicable controls

| Risk | Status | Implementation |
|------|--------|----------------|
| **LLM01**: Prompt Injection | ✅ | Input sanitization on search queries |
| **LLM02**: Insecure Output Handling | ✅ | Content sanitization (HTML -> Markdown) |
| **LLM03**: Training Data Poisoning | ✅ | Trusted sources only (domain whitelist) |
| **LLM04**: Model DoS | ✅ | Response size limits, timeouts |
| **LLM06**: Sensitive Info Disclosure | ✅ | JSON key filtering |
| **LLM07**: Insecure Plugin Design | ✅ | SSRF prevention, domain whitelist |
| **LLM08**: Excessive Agency | ✅ | Read-only, no Bash/Write access |

**Security Confidence**: 0.85 (High)

---

## Allowed Domains

**Reference**: `.claude/hooks/security/validate_url.py:APPROVED_DOMAINS`

**Categories** (177 total domains):
- **Financial**: Bloomberg, Reuters, Yahoo Finance, SEC.gov
- **Development**: GitHub, GitLab, Stack Overflow, MDN
- **Technical Documentation**: Official language/framework docs
- **Academic**: arXiv, PubMed, IEEE, ACM
- **Security**: OWASP, NIST, CVE databases

### Domain Validation Rules

1. **Whitelist check**: URL domain must be in APPROVED_DOMAINS
2. **IP validation**: No internal IPs (10.x, 172.16-31.x, 192.168.x, 169.254.x)
3. **Protocol check**: HTTPS required (HTTP rejected)
4. **Path validation**: No suspicious patterns (../, metadata endpoints)

---

## Quick Reference Checklist

Before returning output, verify:

- [ ] All URLs validated through security-validate-url.py
- [ ] Domain whitelist enforced for all external requests
- [ ] SSRF prevention active (internal IPs blocked)
- [ ] Content sanitization applied (HTML -> Markdown)
- [ ] Response size limits enforced (5MB max)
- [ ] Timeout limits enforced (30s max)
- [ ] No command execution (Bash tool blocked)
- [ ] Read-only operations only (no Write/Edit tools)
