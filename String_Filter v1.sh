#!/bin/bash

# Prompt the user to enter the file path
read -p "Please enter the file path: " file_path

# Check if the file exists
if [ ! -f "$file_path" ]; then
    echo "File not found!"
    exit 1
fi

# Filter out lines containing '2024' from the file
grep -v '2024' "$file_path"
