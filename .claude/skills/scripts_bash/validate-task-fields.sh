#!/bin/bash
# Validate task configuration file (task.yaml or task.toml)

CONFIG_FILE="$1"

if [ -z "$CONFIG_FILE" ]; then
    echo "Usage: $0 <config-file>"
    exit 1
fi

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Config file not found: $CONFIG_FILE"
    exit 1
fi

# Determine format based on extension
if [[ "$CONFIG_FILE" == *.toml ]]; then
    # Harbor format - check for required TOML fields
    REQUIRED_FIELDS=("author_name" "author_email" "difficulty")
    for field in "${REQUIRED_FIELDS[@]}"; do
        if ! grep -q "$field" "$CONFIG_FILE"; then
            echo "Missing required field: $field"
            exit 1
        fi
    done
elif [[ "$CONFIG_FILE" == *.yaml ]] || [[ "$CONFIG_FILE" == *.yml ]]; then
    # Tasks format - check for required YAML fields
    REQUIRED_FIELDS=("instruction:" "author_name:" "author_email:")
    for field in "${REQUIRED_FIELDS[@]}"; do
        if ! grep -q "$field" "$CONFIG_FILE"; then
            echo "Missing required field: $field"
            exit 1
        fi
    done
else
    echo "Unknown config format: $CONFIG_FILE"
    exit 1
fi

exit 0
