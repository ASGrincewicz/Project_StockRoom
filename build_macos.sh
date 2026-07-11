#!/usr/bin/env bash
#
# Build the Stockroom App into a standalone macOS executable.
#
# The application uses `match`/`case` syntax and therefore requires
# Python 3.10+. This script creates an isolated build virtual environment,
# installs PyInstaller, produces a one-file executable and places a writable
# copy of the `data/` folder next to it.
#
# Usage:
#   ./build_macos.sh
#
# Output:
#   venv/dist/StockroomApp        <- the standalone executable
#   venv/dist/data/               <- writable CSV data used by the app
#
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="${PROJECT_ROOT}/venv"
BUILD_ENV="${PROJECT_ROOT}/build_env"

# Pick a Python 3.10+ interpreter. Check PATH first, then common install
# locations (Homebrew is often not on PATH in non-interactive shells).
PYTHON=""
for candidate in \
    python3.13 python3.12 python3.11 python3.10 \
    /opt/homebrew/bin/python3.13 /opt/homebrew/bin/python3.12 \
    /opt/homebrew/bin/python3.11 /opt/homebrew/bin/python3.10 \
    /usr/local/bin/python3.13 /usr/local/bin/python3.12 \
    /usr/local/bin/python3.11 /usr/local/bin/python3.10; do
    if command -v "${candidate}" >/dev/null 2>&1; then
        PYTHON="$(command -v "${candidate}")"
        break
    fi
done

if [ -z "${PYTHON}" ]; then
    echo "ERROR: Python 3.10+ is required but was not found on PATH." >&2
    echo "Install it (e.g. 'brew install python@3.13') and re-run." >&2
    exit 1
fi

echo "Using interpreter: ${PYTHON} ($(${PYTHON} --version))"

# Create / reuse an isolated build environment.
if [ ! -x "${BUILD_ENV}/bin/pyinstaller" ]; then
    echo "Creating build virtual environment..."
    "${PYTHON}" -m venv "${BUILD_ENV}"
    "${BUILD_ENV}/bin/pip" install --quiet --upgrade pip pyinstaller
fi

# Build the one-file executable.
cd "${SRC_DIR}"
"${BUILD_ENV}/bin/pyinstaller" \
    --noconfirm \
    --clean \
    --onefile \
    --name StockroomApp \
    --paths . \
    Main.py

# Ship a writable copy of the data folder next to the executable.
if [ -d "${SRC_DIR}/data" ]; then
    rm -rf "${SRC_DIR}/dist/data"
    cp -R "${SRC_DIR}/data" "${SRC_DIR}/dist/data"
fi

echo ""
echo "Build complete."
echo "Executable: ${SRC_DIR}/dist/StockroomApp"
echo "Data dir:   ${SRC_DIR}/dist/data"
