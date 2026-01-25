#!/bin/bash
# Check that all provided files contain the Terminal-Bench canary string

CANARY_PATTERN="terminal-bench-canary"

if [ $# -eq 0 ]; then
    echo "Usage: $0 <file1> [file2] ..."
    exit 1
fi

MISSING_CANARY=false

for file in "$@"; do
    if [ ! -f "$file" ]; then
        echo "File not found: $file"
        MISSING_CANARY=true
        continue
    fi
    
    if ! grep -q "$CANARY_PATTERN" "$file"; then
        echo "Missing canary string in: $file"
        MISSING_CANARY=true
    fi
done

if $MISSING_CANARY; then
    exit 1
fi

exit 0
