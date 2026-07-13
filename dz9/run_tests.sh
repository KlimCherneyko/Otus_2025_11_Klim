#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

ARGS=()
for arg in "$@"; do
  if [[ "$arg" == "--headed" ]]; then
    ARGS+=("--selenium-headed")
  else
    ARGS+=("$arg")
  fi
done

if ((${#ARGS[@]})); then
  python3 -m pytest -c "pytest.ini" "tests/selenium_tests" --selenium-browser chrome "${ARGS[@]}"
else
  python3 -m pytest -c "pytest.ini" "tests/selenium_tests" --selenium-browser chrome
fi

echo ""
echo "Allure results saved to allure-results/"
echo "Generate report: allure serve allure-results"
