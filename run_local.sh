#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

PORT="${1:-8000}"

if [ ! -d .venv ]; then
    python3 -m venv .venv
fi

.venv/bin/pip install --upgrade pip --quiet
.venv/bin/pip install -r requirements.txt --quiet

.venv/bin/python scripts/make_charts.py

.venv/bin/mkdocs build --strict
.venv/bin/sphinx-build -b html sphinx sphinx/_build/html
rm -rf site/sphinx
cp -r sphinx/_build/html site/sphinx

echo
echo "MkDocs:       http://localhost:${PORT}/"
echo "MkDocs P2:    http://localhost:${PORT}/stress/"
echo "Sphinx P2:    http://localhost:${PORT}/sphinx/stress/"
echo

.venv/bin/python -m http.server "$PORT" -d site
