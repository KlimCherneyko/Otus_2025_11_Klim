#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

python3 -m pytest -c pytest.ini --clean-alluredir "$@"

echo ""
echo "Allure results saved to allure-results/"
echo "Generate report: allure serve allure-results"
