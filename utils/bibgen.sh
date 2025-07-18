#!/bin/bash
# Simple bibliography processing workflow

INPUT_BIB="$1"
OUTPUT_DIR="${2:-output}"

if [[ -z "$INPUT_BIB" ]]; then
    echo "Usage: $0 input.bib [output_dir]"
    exit 1
fi

echo "Processing $INPUT_BIB → $OUTPUT_DIR"

# Step 1: Standardize
bibtool -r bibtool.rsc "$INPUT_BIB" -o standardized.bib

# Step 2: Split by publication type
uv run utils/generate_bibfiles.py standardized.bib "$OUTPUT_DIR" --prefix pub:

# Step 3: Split by topic
uv run utils/generate_bibfiles.py standardized.bib "$OUTPUT_DIR" --prefix topic:

# Cleanup
rm standardized.bib

echo "Done! Files in $OUTPUT_DIR/"
