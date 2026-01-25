# TDD Feature Chunking Guide

**Goal:** Break large features into testable chunks before starting the RED-GREEN-REFACTOR cycle.

---

## 1A: Feature Definition

- [ ] Feature has a clear, specific scope (not vague)
- [ ] Feature can be tested independently
- [ ] Feature doesn't depend on incomplete upstream work
- [ ] You've written a 1-2 sentence acceptance criteria
- [ ] Example acceptance criteria: "User can filter todos by status, and unfiltered count matches displayed count"

---

## 1B: Break into Chunks

- [ ] Identify the smallest testable piece (MVP chunk)
- [ ] Each chunk should be 40-90 minutes of work
- [ ] Chunks should be implementable in isolation or with minimal setup
- [ ] Order chunks by dependency (build from bottom-up)
- [ ] Document chunks in `WORKFLOW_STATUS.md` or feature branch description

**Example chunk breakdown for "User authentication":**
```
Chunk 1: Password hashing function (no DB needed)
Chunk 2: User model with password validation
Chunk 3: Login endpoint accepts credentials
Chunk 4: Login endpoint validates against DB
Chunk 5: Login endpoint returns JWT token
Chunk 6: Protected routes check JWT token
```

---

## 1C: Setup

- [ ] Testing framework installed and working
- [ ] Test runner configured for your language
- [ ] Sample test can run successfully
- [ ] Database/services mocked or available for testing
- [ ] Branch created: `feature/your-feature-name`
