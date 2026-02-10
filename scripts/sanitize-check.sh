#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-.}"
cd "$ROOT"
echo "Running sanitizer leak check in: $(pwd)"
if grep -RInE --exclude-dir=.git \
  --exclude='*.png' --exclude='*.jpg' --exclude='*.jpeg' --exclude='*.gif' \
  '(192\.168\.|10\.[0-9]{1,3}\.|172\.(1[6-9]|2[0-9]|3[0-1])\.|caf6be745611|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}|"password"\s*:\s*"[^"]+")' \
  skills/loxone README.md; then
  echo "❌ Potential sensitive data found."
  exit 1
fi
echo "✅ No obvious leaks found."
