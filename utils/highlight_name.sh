#!/bin/bash
# Script to highlight your name in bibliography files

# Navigate to generated_bibfiles directory
cd generated_bibfiles || exit

# Create backup copies
for file in *.bib; do
    echo "Backing up ${file}"
    cp "$file" "$file.backup"
done

# Replace different variations of your name with bold formatting
for file in *.bib; do
    sed -i.tmp 's/Imami, Ali S\./\\textbf{Imami, Ali S.}/g' "$file"
    sed -i.tmp 's/Imami, Ali Sajid/\\textbf{Imami, Ali Sajid}/g' "$file"
    sed -i.tmp 's/Imami, A\. S\./\\textbf{Imami, A. S.}/g' "$file"
    sed -i.tmp 's/A. Imami/\\textbf{A. Imami}/g' "$file"
    sed -i.tmp 's/{\\textbf{Imami, Ali S\.}} and/{\\textbf{Imami, Ali S.}} and/g' "$file"
    rm "$file.tmp"
done

echo "Name highlighting applied to all .bib files"
echo "Backup files created with .backup extension"
