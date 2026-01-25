# FileGrouper Heuristics

**Purpose**: 7 heuristics for intelligent semantic commit grouping with >90% accuracy target

---

## Confidence Thresholds

| Score | Classification | Action |
|-------|----------------|--------|
| 0.90+ | High confidence | Auto-group recommended |
| 0.80-0.89 | Medium confidence | Review suggested |
| 0.75-0.79 | Low confidence | User confirmation required |
| <0.75 | Very low | Reject grouping, fallback to manual |

---

## Heuristic 0: Semantic Categorization (Confidence: 2.0)

**CRITICAL RULE**: Categorize ALL files by semantic domain BEFORE applying structural heuristics.

**Purpose**: Ensure files are grouped by domain first (API, Database, UI, etc.), then by structural relationships within domains.

**9 Semantic Categories**:

| Category | Directory Patterns | Extensions | Content Patterns | Priority |
|----------|-------------------|------------|------------------|----------|
| claude_code | `.claude/agents/`, `.claude/skills/`, `.claude/commands/`, `.claude/hooks/` | `.md`, `.py`, `.json` | - | 95 |
| database | `migrations/`, `models/`, `schema/`, `sql/` | `.sql`, `.alembic` | `CREATE TABLE`, `sqlalchemy`, `peewee` | 100 |
| api | `routes/`, `handlers/`, `api/`, `controllers/`, `endpoints/` | - | `@app.route`, `@router.`, `FastAPI`, `Flask` | 90 |
| ui | `components/`, `pages/`, `views/`, `styles/`, `ui/` | `.tsx`, `.jsx`, `.vue`, `.css`, `.scss` | `React`, `useState` | 85 |
| config | `config/`, `settings/` | `.env*`, `.ini`, `.cfg`, `.yaml`, `.toml` | - | 80 |
| tests | `tests/`, `test/`, `__tests__/` | `test_*.py`, `*_test.py`, `*.spec.*` | - | 75 |
| docs | `docs/`, `documentation/` | `.md`, `.rst`, `.txt` | - | 70 |
| infrastructure | `k8s/`, `terraform/`, `docker/`, `.github/`, `ci/` | `.tf`, `Dockerfile*` | - | 65 |
| code | Fallback | - | - | 0 |

**Detection Algorithm**:
```python
def categorize_file(filepath: str) -> str:
    # Check categories by priority (highest first)
    for category, rules in sorted(CATEGORIES.items(), key=lambda x: x[1]["priority"], reverse=True):
        if matches_directory(filepath, rules["directory_patterns"]):
            return category
        if matches_extension(filepath, rules["extensions"]):
            return category
        if matches_content(filepath, rules["content_patterns"]):
            return category
    return "code"  # Fallback
```

**CRITICAL**: Files are NEVER grouped across categories. API files stay with API, Database with Database, etc.

---

## Heuristic 1: Test-Implementation Pairing (Confidence: 0.90)

**Pattern**: Match implementation files with their corresponding test files.

```
{module}.py + test_{module}.py
{component}/{file}.py + {component}/tests/test_{file}.py
```

**Examples**:
- `auth.py` + `test_auth.py` -> Group together (feat/fix/refactor)
- `api/users.py` + `api/tests/test_users.py` -> Group together
- `.claude/agents/source-control.md` + `schemas/source-control.schema.json` -> Group together

**Detection**: Filename pattern matching with test_ prefix or /tests/ directory.


---

## Heuristic 2: Directory Scope (Confidence: 0.75)

**Pattern**: Files in the same directory with functional coupling.

```
All files in .claude/agents/ -> Group by agent lifecycle
All files in docs/01-planning/specifications/ -> Group by documentation scope
All files in scripts/ -> Group by tooling purpose
```

**Examples**:
- All modified files in `.claude/agents/dev-tools/` -> Single agent update commit
- All files in `packages/core/models/` -> Data model changes commit

**Detection**: Common directory prefix analysis.

---

## Heuristic 3: Functional Coupling (Confidence: 0.80)

**Pattern**: Files that implement related features based on dependencies.

**Detection Methods**:
1. **Import analysis**: File A imports File B
2. **Naming similarity**: `user_service.py` + `user_repository.py`
3. **Commit history**: Often changed together (git log analysis)

**Examples**:
- `auth_service.py` + `auth_middleware.py` + `auth_utils.py` -> Group together
- `user_model.py` + `user_schema.py` + `user_validator.py` -> Group together


---

## Heuristic 4: Change Type Separation (Confidence: 1.0)

**CRITICAL RULE**: NEVER mix change types in the same commit.

**Types** (from Conventional Commits spec):
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructuring without behavior change
- `docs`: Documentation only
- `test`: Adding or updating tests
- `build`: Build system or dependency changes
- `style`: Code style/formatting changes
- `chore`: Maintenance tasks
- `ci`: CI/CD pipeline changes
- `perf`: Performance improvements
- `revert`: Revert previous commit
- `wip`: Work in progress

**Examples**:
- `auth.py` (feat) + `docs/auth.md` (docs) -> SEPARATE groups
- Always separate even if functionally related

---

## Heuristic 5: Dependency Ordering (Confidence: 0.85)

**Pattern**: Commits should respect dependency order (foundation first).

**Detection**:
- Import analysis: Foundation -> Dependent
- Build system: Core -> Extensions


**Examples**:
```
Group 1: base_model.py (foundation)
Group 2: user_model.py (depends on base_model)
Group 3: user_api.py (depends on user_model)
```

**Commit Order**: Groups must be committed in dependency order.

---

## Heuristic 6: UV Dependency Management (Confidence: 0.95)

**Pattern**: `pyproject.toml` + `uv.lock` changes for dependency updates.

**Rules**:
1. ALWAYS group `pyproject.toml` + `uv.lock` together
2. ALWAYS separate from application code
3. Change type based on section modified

**Type Detection**:
- `[dependencies]` or `[dev-dependencies]` changed -> `build` type
- `[tool.*]` section changed -> `chore` type

**Examples**:
- `pyproject.toml` + `uv.lock` -> Group together (`build: update deps`)
- `pyproject.toml [tool.uv]` only -> Separate group (`chore: config`)

**Warning**: If `uv.lock` changed WITHOUT `pyproject.toml` -> Flag for lockfile regeneration.

---

## Application Priority

Heuristics are applied in strict order:

| Order | Heuristic | Confidence | Can Skip? |
|-------|-----------|------------|-----------|
| 0 | Semantic Categorization | 2.0 | Never |
| 1 | Change Type Separation | 1.0 | Never |
| 2 | UV Dependency Management | 0.95 | Never |
| 3 | Test-Implementation Pairing | 0.90 | Never |
| 4 | Dependency Ordering | 0.85 | If no deps |
| 5 | Functional Coupling | 0.80 | If no coupling |
| 6 | Directory Scope | 0.75 | Always last |

---

## Conflict Resolution Rules

When multiple heuristics produce contradictory grouping recommendations, apply these resolution rules:

### Resolution Priority (Highest Wins)

| Conflict | Winner | Rationale |
|----------|--------|-----------|
| Semantic Categorization vs ANY other | Semantic Categorization | NEVER mix domains - domain isolation is absolute |
| Change Type Separation vs ANY other (within category) | Change Type Separation | NEVER mix commit types - type purity is absolute |
| UV Dependency vs Directory Scope | UV Dependency | Isolate dependency changes from application code |
| Test-Implementation vs Directory Scope | Test-Implementation | Keep test+implementation together within same type |
| Functional Coupling vs Directory Scope | Functional Coupling | Import relationships > physical proximity |

### Decision Algorithm

Apply heuristics in this order to resolve conflicts:

0. **ZEROTH**: Apply Semantic Categorization - split ALL files by domain (API/Database/UI/etc.)
1. **FIRST**: Within each category, apply Change Type Separation - split by type (feat/fix/docs/etc.)
2. **SECOND**: Within each type group, apply UV Dependency Management - isolate pyproject.toml + uv.lock
3. **THIRD**: Within remaining groups, apply Test-Implementation Pairing
4. **FOURTH**: Apply Dependency Ordering to determine commit sequence
5. **FIFTH**: Apply Functional Coupling for remaining ungrouped files
6. **SIXTH**: Apply Directory Scope as final fallback


### Conflict Detection

Flag a conflict when:
- Two heuristics recommend different groupings for the same file
- Confidence scores differ by >0.15 between competing heuristics

**On conflict detection**: Use winner from Resolution Priority table, log the conflict in `grouping_rationale`.

### Example: Conflict Resolution

**Scenario**: `auth.py` (feat) modified with `test_auth.py` (test)

- Test-Implementation Pairing (0.90): Group together
- Change Type Separation (1.0): Split into separate commits

**Resolution**: Change Type wins (absolute rule)
- Group 1: `auth.py` -> `feat(auth): implement authentication`
- Group 2: `test_auth.py` -> `test(auth): add authentication tests`

**Rationale logged**: "Change Type Separation override: test file separated from implementation despite Test-Impl pairing signal"

---

## Confidence Calculation

**Per-Group Confidence**: Average of all heuristics applied to that group.

**Overall Confidence**: Weighted average of all group confidences.

```
group_confidence = sum(heuristic_confidence) / count(heuristics_applied)
overall_confidence = sum(group_confidence * group_file_count) / total_files
```
