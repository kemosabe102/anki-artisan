# Kubernetes Manifest Editing Protocol

**Purpose**: Platform-aware protocol for safely editing Kubernetes manifests with validation and rollback.

**When to Use**: When updating ConfigMaps, Secrets, Deployments, or any Kubernetes manifest file.

---

## Platform Detection

**Check `Platform: win32` in `<env>` block at session startup** to determine editing approach.

---

## Protocol Steps

### 1. Read Current Manifest

```python
Read("k8s/local/deployment.yaml")
```

### 2. Edit Manifest

Use available file operation tools. MCP tools preferred for YAML (better special character handling), but built-in `Edit` works for most cases.

**Using built-in Edit**:
```python
Edit(
    file_path="k8s/local/deployment.yaml",
    old_string="old_yaml_content",
    new_string="new_yaml_content"
)
```

**Using MCP tools (when configured)**:
```python
mcp__desktop-commander__edit_block(
    file_path="k8s/local/deployment.yaml",
    old_string="old_yaml_content",
    new_string="new_yaml_content"
)
```

**Chunking**: All modifications should be ≤30 lines per operation. For larger files, use sequential edits/writes.

### 3. Validate Change (Dry-Run)

```bash
AGENT_NAME=k8s-deployment bash scripts/deployment/validate-k8s-manifests.sh --mode=standard gauntlet-agents k8s/local
```

### 4. Apply Change with Script

```bash
AGENT_NAME=k8s-deployment bash scripts/deployment/deploy-local-k8s.sh
```

Script applies manifests using kubectl apply -k internally.

### 5. Verify Rollout

```bash
AGENT_NAME=k8s-deployment kubectl rollout status deployment/<name> -n <namespace>
```

---

## Validation Mode Selection (Decision Tree)

| Scenario | Mode | Rationale |
|----------|------|-----------|
| Quick syntax check before editing | `--mode=quick` | Fast client-side only, no cluster access needed |
| Pre-deployment validation | `--mode=standard` | Client + server validation, catches immutable field issues |
| CI/CD pipeline validation | `--mode=full` | Comprehensive with kustomize build check |
| Post-edit verification | `--mode=standard --verbose` | Detailed error messages for debugging |
| Show deployment diff | `--mode=standard --diff` | Preview changes before applying |

**Command Examples**:

```bash
# Quick syntax check (2-3 seconds)
AGENT_NAME=k8s-deployment bash scripts/deployment/validate-k8s-manifests.sh --mode=quick gauntlet-agents k8s/local

# Standard validation with verbose output (5-7 seconds)
AGENT_NAME=k8s-deployment bash scripts/deployment/validate-k8s-manifests.sh --mode=standard --verbose gauntlet-agents k8s/local

# Full validation with diff preview (7-10 seconds)
AGENT_NAME=k8s-deployment bash scripts/deployment/validate-k8s-manifests.sh --mode=full --diff gauntlet-agents k8s/local
```

**Exit Codes**:
- `0` - All validations passed
- `1` - Client-side validation failed (syntax error)
- `2` - Server-side validation failed (schema error, immutable field)
- `3` - Kustomize build failed (kustomization.yaml error)
- `4` - Prerequisites missing (kubectl not found, cluster unreachable)

---

## Why Dedicated Tools for YAML

**YAML Special Characters**: Kubernetes manifests contain many shell special characters:

- Environment variables: `$(VAR)`, `${VAR}`
- Redirection-like syntax: `<none>`, `<unset>`
- Multi-line strings with complex indentation
- Quotes, colons, pipes (`|`, `>`), anchors (`&`, `*`)

**Dedicated tools (Edit, Write, or MCP equivalents) handle these automatically**:

- No shell escaping issues
- Direct file manipulation without subprocess overhead
- Proper handling of multi-line YAML content
- Atomic operations

---

## Correct Order

**CRITICAL**: Edit BEFORE validation, not after:

- ❌ **WRONG**: Read → Dry-run → Edit → Apply (validates old content)
- ✅ **CORRECT**: Read → Edit → Dry-run → Apply (validates new content)

**Rationale**: Dry-run must validate the CHANGED manifest, not the original.

---

## Common YAML Validation Failures

**Exit code 1** (client-side):
- Indentation errors
- Invalid field names
- Type mismatches
- Invalid enum values

**Exit code 2** (server-side):
- Immutable field changes
- Selector updates
- ClusterIP changes

**Exit code 3** (kustomize):
- kustomization.yaml syntax errors
- Missing resource references

**Exit code 4** (prerequisites):
- kubectl not found
- Cluster unreachable
- kustomization.yaml missing

**If validation script reports errors**:
- Check exit code to classify error type
- Run with `--verbose` flag for detailed error messages
- Re-run with `--no-validate` flag if false positive (rare)

---

## ConfigMap Update Example

```bash
# 1. Read current ConfigMap
Read("k8s/local/configmap.yaml")

# 2. Edit manifest (use available tool)
Edit(
    file_path="k8s/local/configmap.yaml",
    old_string="old_config_value",
    new_string="new_config_value"
)

# 3. Validate change BEFORE applying
AGENT_NAME=k8s-deployment bash scripts/deployment/validate-k8s-manifests.sh --mode=standard gauntlet-agents k8s/local

# 4. Apply with script
AGENT_NAME=k8s-deployment bash scripts/deployment/deploy-local-k8s.sh

# 5. Trigger rollout (ConfigMaps aren't hot-reloaded)
AGENT_NAME=k8s-deployment kubectl rollout restart deployment/<name>
```

---

## Secret Rotation Example (Immutability Enforcement)

```bash
# Secrets are immutable by default (best practice)

# 1. Regenerate secrets
AGENT_NAME=k8s-deployment bash scripts/deployment/setup-k8s-secrets.sh --rotate-db-password

# 2. Update manifest to reference new secret version (use available tool)
Edit("k8s/local/deployment.yaml", old_secret_ref, new_secret_ref)

# 3. Validate change BEFORE applying (prevention over recovery)
AGENT_NAME=k8s-deployment bash scripts/deployment/validate-k8s-manifests.sh --mode=standard gauntlet-agents k8s/local

# 4. Apply with script
AGENT_NAME=k8s-deployment bash scripts/deployment/deploy-local-k8s.sh

# 5. Cleanup if needed
AGENT_NAME=k8s-deployment bash scripts/deployment/deploy-local-k8s.sh --cleanup  # uses kubectl delete internally
```

Prevents race conditions and ensures atomic updates.

---

**See Also**:
- `.claude/docs/guides/file-operation-protocol.md` - General file editing protocol
- `scripts/deployment/validate-k8s-manifests.sh` - Validation script
