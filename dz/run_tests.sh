#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

ARGS=()
browser_set=false
skip_next=false

for arg in "$@"; do
  if $skip_next; then
    ARGS+=("--selenium-browser" "$arg")
    browser_set=true
    skip_next=false
    continue
  fi

  case "$arg" in
    --headed)
      ARGS+=("--selenium-headed")
      ;;
    --browser)
      skip_next=true
      ;;
    --browser=*)
      ARGS+=("--selenium-browser=${arg#*=}")
      browser_set=true
      ;;
    --selenium-browser|--selenium-browser=*)
      ARGS+=("$arg")
      browser_set=true
      ;;
    *)
      ARGS+=("$arg")
      ;;
  esac
done

if ! $browser_set; then
  ARGS=(--selenium-browser chrome "${ARGS[@]}")
fi

python3 -m pytest -c pytest.ini tests/selenium_tests "${ARGS[@]}"

echo ""
echo "Allure results saved to allure-results/"
echo "Generate report: allure serve allure-results"
