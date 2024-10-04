#!/bin/bash
#String filter for $APPL_TOP file
#Version: 0.5
# Check if the file argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <file>"
    exit 1
fi

# Check if the file exists
if [ ! -f "$1" ]; then
    echo "File not found!"
    exit 1
fi

# Filter out lines containing '2024' from the file
grep -v '2024' "$1"
