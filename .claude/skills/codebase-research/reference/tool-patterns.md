# Tool Patterns Reference

Comprehensive patterns for Glob, Grep, and Read tools in codebase research.

---

## Glob Patterns

### Find Files by Extension

```bash
# Python files
Glob("**/*.py")

# TypeScript/JavaScript
Glob("**/*.{ts,tsx,js,jsx}")

# Configuration files
Glob("**/*.{json,yaml,yml,toml}")

# Markdown documentation
Glob("**/*.md")

# Test files only
Glob("**/test_*.py")
Glob("**/*_test.py")
```

### Find Files by Name Patterns

```bash
# Find specific filename anywhere
Glob("**/config.py")
Glob("**/settings.json")

# Find files starting with prefix
Glob("**/base_*.py")

# Find files in specific directories
Glob("src/**/*.py")
Glob("packages/core/**/*.py")
```

### Find Configuration Files

```bash
# Environment configs
Glob("**/.env*")
Glob("**/config.{json,yaml,yml}")

# Package configs
Glob("**/pyproject.toml")
Glob("**/package.json")

# CI/CD configs
Glob(".github/**/*.{yml,yaml}")
```

---

## Grep Patterns

### Function Definitions

```bash
# Python function definition
Grep("^def function_name", output_mode="content", -n=true)

# Python async function
Grep("^async def ", output_mode="content", type="py")

# JavaScript/TypeScript function
Grep("^(export )?(async )?function ", output_mode="content", type="js")
```

### Class Definitions

```bash
# Python class
Grep("^class ClassName", output_mode="content", -n=true)

# Python class with inheritance
Grep("^class.*\(.*\):", output_mode="content", type="py")

# TypeScript class
Grep("^(export )?(abstract )?class ", output_mode="content", type="ts")
```

### Import Statements

```bash
# Python imports (all)
Grep("^import |^from ", output_mode="content", type="py", -n=true)

# Import specific module
Grep("from module_name import", output_mode="files_with_matches")

# Find all importers of a symbol
Grep("from .* import.*SymbolName", output_mode="files_with_matches")
```

### Class Hierarchies

```bash
# Find all classes inheriting from BaseClass
Grep("class.*\(.*BaseClass.*\)", output_mode="content", type="py")

# Find interface implementations (TypeScript)
Grep("class.*implements.*Interface", output_mode="content", type="ts")
```

### TODO/FIXME Tracking

```bash
# Find all TODOs
Grep("TODO", output_mode="content", -n=true, -i=true)

# Find FIXMEs with context
Grep("FIXME", output_mode="content", -A=2, -B=1)

# Count technical debt markers
Grep("TODO|FIXME|HACK|XXX", output_mode="count")
```

### Usage Patterns

```bash
# Word boundary match (precise)
Grep("\bClassName\b", output_mode="files_with_matches")

# Case-insensitive search
Grep("pattern", output_mode="content", -i=true)

# With context lines
Grep("pattern", output_mode="content", -A=2, -B=2, head_limit=5)

# Count occurrences
Grep("pattern", output_mode="count")

# Limit results
Grep("pattern", output_mode="files_with_matches", head_limit=20)
```

---

## Read Strategies

### Reading Large Files

```bash
# Read first 100 lines
Read("/path/to/file.py", limit=100, offset=0)

# Read next 100 lines (pagination)
Read("/path/to/file.py", limit=100, offset=100)
```

### Chunking Strategy

**When to chunk**:
- File > 500 lines: Read in 200-line chunks
- File > 1000 lines: Read header (50 lines) + targeted sections

**Chunking pattern**:
```python
1. Read(file, limit=50, offset=0)  # Header: imports, classes
2. Grep to find line numbers of interest
3. Read(file, limit=100, offset=target_line-10)  # Context around target
```

### Strategic Reading

```bash
# Read imports and exports only (top of file)
Read("/path/to/module.py", limit=30, offset=0)

# Read class definition (after finding line number via Grep)
Read("/path/to/module.py", limit=50, offset=45)

# Read test file to understand usage
Read("tests/test_feature.py", limit=100, offset=0)
```

---

## BlastRadius Analysis Patterns

### Finding All Callers

```bash
# Step 1: Find direct imports
Grep("from.*target_module.*import", output_mode="files_with_matches")

# Step 2: Find usage in those files
Grep("\btarget_function\b", output_mode="content", -n=true)

# Step 3: Count call sites
Grep("target_function\(", output_mode="count")
```

### Finding All Callees

```bash
# Step 1: Read the focal file
Read("/path/to/focal_file.py", limit=200, offset=0)

# Step 2: Extract all imports
Grep("^import |^from ", output_mode="content", path="/path/to/focal_file.py")

# Step 3: For each imported module, find its definition
Grep("^def|^class", output_mode="content", path="/path/to/imported_module.py")
```

---

## Dependency Mapping Techniques

### Import Graph Construction

```python
# Pseudo-code for import graph
imports_map = {}

# Phase 1: Find all Python files
files = Glob("**/*.py")

# Phase 2: For each file, extract imports
for file in files:
    imports = Grep("^from (.*) import|^import (.*)", 
                   output_mode="content", path=file)
    imports_map[file] = parse_imports(imports)

# Phase 3: Build dependency graph
dependency_graph = {
    file: [resolve_module(imp) for imp in imports_map[file]]
    for file in files
}
```

### Export Detection

```bash
# Python: Find __all__ exports
Grep("__all__.*=", output_mode="content", -A=5)

# Python: Find public APIs (not starting with _)
Grep("^def [^_]|^class [^_]", output_mode="content")

# TypeScript: Find exports
Grep("^export ", output_mode="content", type="ts")
```

---

## Pattern Selection Guide

| Goal | Tool Sequence | Pattern |
|------|---------------|---------|
| Find definition | Grep to Read | `^def function_name` then Read file at line |
| Find all usages | Grep (count) to Grep (files) to Read top 3 | `\bsymbol\b` |
| Map dependencies | Glob to Grep (imports) to Build graph | `^from .* import` |
| Find similar code | Grep (pattern) to Read to Compare | Structural pattern |
| Assess blast radius | Grep (importers) to Grep (usages) to Count | Import + usage patterns |

---

## Quick Reference

```bash
# Most common patterns
Glob("**/*.py")                               # All Python files
Grep("^class|^def", output_mode="content")    # All definitions
Grep("from .* import", output_mode="content") # All imports
Grep("\bsymbol\b", output_mode="count")     # Usage count
Read(file, limit=50, offset=0)                # Read file header
```
