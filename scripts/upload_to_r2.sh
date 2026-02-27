#!/bin/bash
# Upload staged pattern files to Cloudflare R2
#
# Prerequisites:
#   - wrangler CLI installed: npm install -g wrangler
#   - Authenticated: wrangler login
#
# Usage:
#   ./scripts/upload_to_r2.sh [domain]
#
# Examples:
#   ./scripts/upload_to_r2.sh          # Upload all domains
#   ./scripts/upload_to_r2.sh urban    # Upload only urban patterns

set -euo pipefail

BUCKET="commons-patterns"
STAGING_DIR="$(dirname "$0")/../r2-staging"

if [ ! -d "$STAGING_DIR" ]; then
  echo "ERROR: R2 staging directory not found at $STAGING_DIR"
  echo "Run build_patterns.py first to generate staged files."
  exit 1
fi

upload_domain() {
  local domain=$1
  local domain_dir="$STAGING_DIR/$domain"

  if [ ! -d "$domain_dir" ]; then
    echo "  SKIP: No staged files for domain '$domain'"
    return
  fi

  local count=$(ls "$domain_dir"/*.md 2>/dev/null | wc -l)
  echo "  Uploading $count patterns for domain '$domain'..."

  # Upload in batches of 100 for efficiency
  local uploaded=0
  for file in "$domain_dir"/*.md; do
    local slug=$(basename "$file" .md)
    local key="patterns/$domain/$slug.md"

    wrangler r2 object put "$BUCKET/$key" --file "$file" --content-type "text/markdown" 2>/dev/null

    uploaded=$((uploaded + 1))
    if [ $((uploaded % 100)) -eq 0 ]; then
      echo "    ... $uploaded / $count uploaded"
    fi
  done

  echo "  Done: $uploaded patterns uploaded for '$domain'"
}

echo "=== Commons Engineering — R2 Pattern Upload ==="
echo ""

if [ $# -gt 0 ]; then
  # Upload specific domain
  upload_domain "$1"
else
  # Upload all domains
  for domain_dir in "$STAGING_DIR"/*/; do
    domain=$(basename "$domain_dir")
    upload_domain "$domain"
  done
fi

echo ""
echo "Upload complete!"
