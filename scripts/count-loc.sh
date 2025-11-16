#!/bin/bash
# ⒸAngelaMos | 2025 | CertGames.com

set -e

echo "Starting LOC counting process..."

REPOS_JSON="scripts/repos.json"
TEMP_DIR=$(mktemp -d)
OUTPUT_FILE="loc-data.json"

echo "Temporary directory: $TEMP_DIR"

cd "$TEMP_DIR"

echo "Cloning repositories..."
jq -r '.repos[]' "../$REPOS_JSON" | while read -r repo; do
    echo "  Cloning $repo..."
    git clone --depth 1 "https://github.com/$repo.git" "$(basename $repo)" 2>/dev/null || echo "Failed to clone $repo"
done

echo "Running tokei to count lines of code..."
tokei . --output json --exclude '*.md' '*.txt' 'README*' 'LICENSE*' > "../$OUTPUT_FILE"

echo "Cleaning up temporary directory..."
cd ..
rm -rf "$TEMP_DIR"

echo "LOC counting complete! Results saved to $OUTPUT_FILE"

cat "$OUTPUT_FILE" | jq '.'
