#!/usr/bin/env bash
# One-time setup for the tailor-resume skill: create a local venv and install
# python-docx. Safe to re-run (idempotent). No system dependencies beyond python3.
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$DIR/.venv"

if [[ ! -d "$VENV" ]]; then
  echo "Creating venv at $VENV ..."
  python3 -m venv "$VENV"
fi

"$VENV/bin/pip" install --quiet --upgrade pip
"$VENV/bin/pip" install --quiet -r "$DIR/requirements.txt"

"$VENV/bin/python" -c "import docx; print('python-docx', docx.__version__, 'ready')"
echo "tailor-resume setup complete."
