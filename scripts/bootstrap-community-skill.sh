#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

mkdir -p skills/loxone
for f in config actions pv-mapping; do
  src="skills/loxone/${f}.example.json"
  dst="skills/loxone/${f}.json"
  if [[ -f "$src" && ! -f "$dst" ]]; then
    cp "$src" "$dst"
    echo "created: $dst"
  fi
done

echo "Done. Edit skills/loxone/*.json and create credentials files before running scripts."
