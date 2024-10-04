#!/bin/bash
#String filter for $APPL_TOP file
#Version: 0.5
#!/bin/bash

# Check if the file argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <input_file>"
    exit 1
fi

# Check if the input file exists
if [ ! -f "$1" ]; then
    echo "Input file not found!"
    exit 1
fi

# Prompt the user for the output file path
read -p "Please enter the output file path: " output_file

# Filter out lines containing '2024' and save to the output file
grep -v '2024' "$1" > "$output_file"

# Inform the user of successful completion
echo "Filtered output saved to $output_file"



# Check if the file argument is provided
#if [ -z "$1" ]; then
 #   echo "Usage: $0 <file>"
  #  exit 1
#fi

# Check if the file exists
#if [ ! -f "$1" ]; then
#    echo "File not found!"
 #   exit 1
#fi

# Filter out lines containing '2024' from the file
#grep -v '2024' "$1"
