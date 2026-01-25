#!/bin/bash
# Check Dockerfile for forbidden references (solution.sh, tests/, etc.)

DOCKERFILE="$1"

if [ -z "$DOCKERFILE" ]; then
    echo "Usage: $0 <dockerfile>"
    exit 1
fi

if [ ! -f "$DOCKERFILE" ]; then
    echo "Dockerfile not found: $DOCKERFILE"
    exit 1
fi

# Forbidden patterns that would leak solution or tests
FORBIDDEN_PATTERNS=(
    "COPY.*solution"
    "COPY.*tests/"
    "ADD.*solution"
    "ADD.*tests/"
    "COPY.*test_outputs"
    "COPY.*run-tests"
)

FOUND_FORBIDDEN=false

for pattern in "${FORBIDDEN_PATTERNS[@]}"; do
    if grep -qE "$pattern" "$DOCKERFILE"; then
        echo "Forbidden reference found: $pattern"
        FOUND_FORBIDDEN=true
    fi
done

if $FOUND_FORBIDDEN; then
    exit 1
fi

exit 0
